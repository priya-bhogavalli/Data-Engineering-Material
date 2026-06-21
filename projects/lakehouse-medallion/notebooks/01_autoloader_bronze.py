# Databricks notebook source
# MAGIC %md
# MAGIC # Bronze Layer — Auto Loader Streaming Ingest
# MAGIC
# MAGIC Ingests raw JSON order events landing in cloud object storage into a Bronze Delta
# MAGIC table using **Auto Loader** (`cloudFiles`). Auto Loader is preferred over a plain
# MAGIC `spark.read` batch job here because:
# MAGIC - it incrementally discovers new files without listing the whole directory each run
# MAGIC - it tracks processed files in its own checkpoint (no external state store needed)
# MAGIC - schema inference + evolution is built in, so upstream producers can add fields
# MAGIC   without breaking the pipeline

# COMMAND ----------

from pyspark.sql import functions as F

dbutils.widgets.text("source_path", "/Volumes/lakehouse/bronze/raw_orders/landing")
dbutils.widgets.text("checkpoint_path", "/Volumes/lakehouse/bronze/raw_orders/_checkpoint")
dbutils.widgets.text("schema_path", "/Volumes/lakehouse/bronze/raw_orders/_schema")
dbutils.widgets.text("target_table", "lakehouse.bronze.raw_orders")

source_path = dbutils.widgets.get("source_path")
checkpoint_path = dbutils.widgets.get("checkpoint_path")
schema_path = dbutils.widgets.get("schema_path")
target_table = dbutils.widgets.get("target_table")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Stream definition
# MAGIC
# MAGIC `cloudFiles.schemaEvolutionMode = "addNewColumns"` lets new fields show up in the
# MAGIC bronze table automatically instead of failing the stream — bronze is meant to be a
# MAGIC faithful, append-only copy of the source, so we don't want to reject data on schema
# MAGIC drift. Schema enforcement happens downstream in Silver.

# COMMAND ----------

raw_stream = (
    spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", schema_path)
    .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
    .option("cloudFiles.inferColumnTypes", "true")
    .option("cloudFiles.maxFilesPerTrigger", 1000)
    .load(source_path)
    .withColumn("_ingested_at", F.current_timestamp())
    .withColumn("_source_file", F.col("_metadata.file_path"))
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Write to Bronze
# MAGIC
# MAGIC `availableNow=True` runs the stream as a scheduled batch-like job that processes
# MAGIC everything currently available then stops — this is the right trigger mode for a
# MAGIC job orchestrated by Databricks Workflows/DAB on a cron schedule, rather than a
# MAGIC continuously-running cluster.

# COMMAND ----------

(
    raw_stream.writeStream.format("delta")
    .option("checkpointLocation", checkpoint_path)
    .option("mergeSchema", "true")
    .trigger(availableNow=True)
    .toTable(target_table)
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Sanity check
# MAGIC
# MAGIC Confirms rows landed and that `_ingested_at` / `_source_file` lineage columns are
# MAGIC populated — these are what Silver dedup logic and audits key off later.

# COMMAND ----------

display(
    spark.table(target_table)
    .groupBy(F.to_date("_ingested_at").alias("ingest_date"))
    .agg(F.count("*").alias("row_count"))
    .orderBy("ingest_date")
)
