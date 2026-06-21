# Databricks notebook source
# MAGIC %md
# MAGIC # Gold Layer — Business Aggregates
# MAGIC
# MAGIC Builds the business-facing tables on top of Silver: daily revenue by currency and
# MAGIC a customer lifetime-value rollup. Gold tables are batch `CREATE OR REPLACE` rather
# MAGIC than streaming — they're cheap to fully recompute from Silver on each run, which is
# MAGIC simpler to reason about than incrementally maintaining aggregate state, and Silver
# MAGIC volume here doesn't justify the added complexity of incremental aggregation.

# COMMAND ----------

from pyspark.sql import functions as F

dbutils.widgets.text("silver_table", "lakehouse.silver.orders")
dbutils.widgets.text("gold_schema", "lakehouse.gold")

silver_table = dbutils.widgets.get("silver_table")
gold_schema = dbutils.widgets.get("gold_schema")

silver = spark.table(silver_table).filter(F.col("status") != "cancelled")

# COMMAND ----------

# MAGIC %md
# MAGIC ## `gold.daily_revenue`
# MAGIC
# MAGIC Partitioned implicitly by `order_date` via Liquid Clustering (see
# MAGIC `sql/liquid_clustering_vs_zorder.sql`) rather than a static `PARTITIONED BY`, since
# MAGIC daily volume is uneven and static date partitioning would create many small files
# MAGIC on low-volume days.

# COMMAND ----------

daily_revenue = (
    silver.withColumn("order_date", F.to_date("order_created_at"))
    .groupBy("order_date", "currency")
    .agg(
        F.sum("order_amount").alias("gross_revenue"),
        F.count("*").alias("order_count"),
        F.countDistinct("customer_id").alias("unique_customers"),
        F.round(F.avg("order_amount"), 2).alias("avg_order_value"),
    )
    .orderBy("order_date", "currency")
)

(
    daily_revenue.write.format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(f"{gold_schema}.daily_revenue")
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## `gold.customer_ltv`
# MAGIC
# MAGIC Lifetime value + recency segment. `days_since_last_order` is computed against
# MAGIC `current_date()` at run time, so this table is meant to be refreshed daily, not
# MAGIC treated as a point-in-time snapshot.

# COMMAND ----------

customer_ltv = (
    silver.groupBy("customer_id")
    .agg(
        F.sum("order_amount").alias("lifetime_value"),
        F.count("*").alias("lifetime_orders"),
        F.max("order_created_at").alias("last_order_at"),
        F.min("order_created_at").alias("first_order_at"),
    )
    .withColumn(
        "days_since_last_order",
        F.datediff(F.current_date(), F.to_date("last_order_at")),
    )
    .withColumn(
        "segment",
        F.when(F.col("days_since_last_order") <= 30, "active")
        .when(F.col("days_since_last_order") <= 90, "at_risk")
        .otherwise("churned"),
    )
)

(
    customer_ltv.write.format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(f"{gold_schema}.customer_ltv")
)

# COMMAND ----------

display(
    spark.table(f"{gold_schema}.customer_ltv")
    .groupBy("segment")
    .agg(F.count("*").alias("customers"), F.sum("lifetime_value").alias("total_ltv"))
    .orderBy(F.desc("total_ltv"))
)
