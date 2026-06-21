# Databricks notebook source
# MAGIC %md
# MAGIC # Silver Layer — Deduplicated, Schema-Enforced Upserts
# MAGIC
# MAGIC Reads new Bronze records as a stream and `MERGE INTO` a Silver Delta table.
# MAGIC Silver is where we start enforcing a contract: a fixed schema, deduplication on
# MAGIC business key, and late-arriving update handling via `order_updated_at`.
# MAGIC
# MAGIC Using `MERGE` instead of a plain append means re-running the job (or replaying a
# MAGIC checkpoint after a failure) is idempotent — the same source row never creates a
# MAGIC duplicate in Silver, and a row that arrives twice with different values takes the
# MAGIC most recent one.

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window
from delta.tables import DeltaTable

dbutils.widgets.text("bronze_table", "lakehouse.bronze.raw_orders")
dbutils.widgets.text("silver_table", "lakehouse.silver.orders")
dbutils.widgets.text("checkpoint_path", "/Volumes/lakehouse/silver/orders/_checkpoint")

bronze_table = dbutils.widgets.get("bronze_table")
silver_table = dbutils.widgets.get("silver_table")
checkpoint_path = dbutils.widgets.get("checkpoint_path")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Enforce schema + business rules
# MAGIC
# MAGIC Bronze is permissive (schema evolves freely). Silver is not: explicit casts,
# MAGIC required-field filtering, and a hard reject of orders with a non-positive amount —
# MAGIC these are the kind of data-quality gates that belong in Silver, not Gold, so bad
# MAGIC rows never reach business-facing aggregates.

# COMMAND ----------

def clean_batch(df):
    return (
        df.select(
            F.col("order_id").cast("string"),
            F.col("customer_id").cast("string"),
            F.col("order_amount").cast("decimal(18,2)").alias("order_amount"),
            F.col("currency").cast("string"),
            F.to_timestamp("order_created_at").alias("order_created_at"),
            F.to_timestamp("order_updated_at").alias("order_updated_at"),
            F.col("status").cast("string"),
            F.col("_ingested_at"),
        )
        .filter(F.col("order_id").isNotNull())
        .filter(F.col("order_amount") > 0)
        # if the same order_id appears more than once in a single micro-batch,
        # keep only the most recently updated version before merging
        .withColumn(
            "_rn",
            F.row_number().over(
                Window.partitionBy("order_id").orderBy(F.col("order_updated_at").desc())
            ),
        )
        .filter(F.col("_rn") == 1)
        .drop("_rn")
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## Upsert via `foreachBatch`
# MAGIC
# MAGIC Streaming `MERGE` requires `foreachBatch` — there's no native streaming merge sink.
# MAGIC The merge condition only updates when the incoming row is strictly newer than what's
# MAGIC already in Silver, which protects against an out-of-order replay overwriting a
# MAGIC newer record with a stale one.

# COMMAND ----------

def upsert_to_silver(micro_batch_df, batch_id):
    cleaned = clean_batch(micro_batch_df)
    if not spark.catalog.tableExists(silver_table):
        cleaned.write.format("delta").saveAsTable(silver_table)
        return

    target = DeltaTable.forName(spark, silver_table)
    (
        target.alias("t")
        .merge(cleaned.alias("s"), "t.order_id = s.order_id")
        .whenMatchedUpdateAll(condition="s.order_updated_at > t.order_updated_at")
        .whenNotMatchedInsertAll()
        .execute()
    )

# COMMAND ----------

(
    spark.readStream.table(bronze_table)
    .writeStream.foreachBatch(upsert_to_silver)
    .option("checkpointLocation", checkpoint_path)
    .trigger(availableNow=True)
    .start()
    .awaitTermination()
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Verify no duplicate business keys made it into Silver

# COMMAND ----------

dupes = (
    spark.table(silver_table)
    .groupBy("order_id")
    .count()
    .filter("count > 1")
)
assert dupes.count() == 0, "Duplicate order_id found in Silver — merge logic regressed"
print("Silver dedup check passed.")
