# Databricks notebook source
# MAGIC %md
# MAGIC # Delta Live Tables — Declarative Medallion Pipeline
# MAGIC
# MAGIC An alternative to notebooks 01-03: the same bronze -> silver -> gold flow expressed
# MAGIC declaratively with DLT. The tradeoff vs the hand-written streaming/merge notebooks:
# MAGIC
# MAGIC | | Notebooks 01-03 | This DLT pipeline |
# MAGIC |---|---|---|
# MAGIC | Orchestration | Databricks Workflow runs each notebook as a task | DLT manages task ordering itself |
# MAGIC | Data quality | Manual `.filter()` calls | Declarative `@dlt.expect_*` with built-in metrics |
# MAGIC | Merge logic | Hand-written `foreachBatch` MERGE | `dlt.apply_changes` (DLT's CDC primitive) |
# MAGIC | Best for | Teams that want full control over merge/retry semantics | Teams that want less boilerplate and built-in lineage/quality UI |
# MAGIC
# MAGIC Both approaches are included in this project deliberately — an SA needs to be able
# MAGIC to recommend either depending on the customer's team maturity and how much control
# MAGIC they want over the merge semantics.

# COMMAND ----------

import dlt
from pyspark.sql import functions as F

SOURCE_PATH = "/Volumes/lakehouse/bronze/raw_orders/landing"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Bronze — streaming table, permissive

# COMMAND ----------

@dlt.table(
    name="bronze_orders",
    comment="Raw order events ingested via Auto Loader, no quality gates applied.",
    table_properties={"quality": "bronze"},
)
def bronze_orders():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.inferColumnTypes", "true")
        .load(SOURCE_PATH)
        .withColumn("_ingested_at", F.current_timestamp())
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## Silver — quality-gated, CDC-applied
# MAGIC
# MAGIC `@dlt.expect_or_drop` enforces the same two rules as the hand-written notebook
# MAGIC (`order_id` not null, `order_amount > 0`) but rows that fail are dropped *and*
# MAGIC counted in the pipeline's built-in data-quality metrics — visible in the DLT UI
# MAGIC without writing a separate monitoring query.

# COMMAND ----------

@dlt.view(comment="Bronze orders with basic type casting before quality checks.")
def orders_typed():
    return spark.readStream.table("LIVE.bronze_orders").select(
        F.col("order_id").cast("string"),
        F.col("customer_id").cast("string"),
        F.col("order_amount").cast("decimal(18,2)").alias("order_amount"),
        F.col("currency").cast("string"),
        F.to_timestamp("order_created_at").alias("order_created_at"),
        F.to_timestamp("order_updated_at").alias("order_updated_at"),
        F.col("status").cast("string"),
    )


dlt.create_streaming_table(
    name="silver_orders",
    comment="Deduplicated, quality-checked orders. One row per order_id.",
    table_properties={"quality": "silver"},
    expect_all_or_drop={
        "valid_order_id": "order_id IS NOT NULL",
        "positive_amount": "order_amount > 0",
    },
)

dlt.apply_changes(
    target="silver_orders",
    source="orders_typed",
    keys=["order_id"],
    sequence_by="order_updated_at",
    apply_as_deletes="status = 'cancelled'",
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Gold — same aggregate logic as notebook 03, materialized incrementally

# COMMAND ----------

@dlt.table(
    name="gold_daily_revenue",
    comment="Daily revenue by currency, computed from silver_orders.",
    table_properties={"quality": "gold"},
)
def gold_daily_revenue():
    return (
        dlt.read("silver_orders")
        .withColumn("order_date", F.to_date("order_created_at"))
        .groupBy("order_date", "currency")
        .agg(
            F.sum("order_amount").alias("gross_revenue"),
            F.count("*").alias("order_count"),
            F.countDistinct("customer_id").alias("unique_customers"),
        )
    )
