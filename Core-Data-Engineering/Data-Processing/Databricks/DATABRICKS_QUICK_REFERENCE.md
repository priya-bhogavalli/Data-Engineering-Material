# Databricks Quick Reference for Data Engineering

## Cluster Management

### Cluster Configuration
```python
# Cluster settings
cluster_config = {
    "cluster_name": "data-engineering-cluster",
    "spark_version": "11.3.x-scala2.12",
    "node_type_id": "i3.xlarge",
    "driver_node_type_id": "i3.xlarge",
    "num_workers": 2,
    "autoscale": {
        "min_workers": 1,
        "max_workers": 8
    },
    "auto_termination_minutes": 120
}

# Spark configuration
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.databricks.delta.optimizeWrite.enabled", "true")
```

### Cluster Types
```python
# All-Purpose Cluster - Interactive analysis
# Job Cluster - Automated workloads
# SQL Warehouse - SQL queries and BI tools

# Check cluster info
cluster_id = spark.conf.get("spark.databricks.clusterUsageTags.clusterId")
print(f"Current cluster: {cluster_id}")
```

## Data Sources and Formats

### Reading Data
```python
# Delta Lake
df = spark.read.format("delta").load("/delta/table_path")
df = spark.table("catalog.schema.table_name")

# Parquet
df = spark.read.format("parquet").load("/path/to/parquet")

# JSON
df = spark.read.format("json").load("/path/to/json")
df = spark.read.option("multiLine", "true").json("/path/to/json")

# CSV
df = spark.read.format("csv").option("header", "true").load("/path/to/csv")

# JDBC
df = spark.read.format("jdbc") \
    .option("url", "jdbc:postgresql://host:port/db") \
    .option("dbtable", "table_name") \
    .option("user", "username") \
    .option("password", "password") \
    .load()

# Kafka
df = spark.read.format("kafka") \
    .option("kafka.bootstrap.servers", "host:port") \
    .option("subscribe", "topic_name") \
    .load()
```

### Writing Data
```python
# Delta Lake
df.write.format("delta").mode("overwrite").save("/delta/table_path")
df.write.format("delta").mode("append").saveAsTable("catalog.schema.table")

# Partitioned write
df.write.format("delta").partitionBy("year", "month").save("/delta/partitioned")

# With options
df.write.format("delta") \
  .option("mergeSchema", "true") \
  .mode("append") \
  .save("/delta/table")

# Other formats
df.write.format("parquet").mode("overwrite").save("/path/to/parquet")
df.write.format("json").mode("overwrite").save("/path/to/json")
```

## Delta Lake Operations

### Basic Operations
```python
from delta.tables import DeltaTable

# Create Delta table
df.write.format("delta").saveAsTable("my_table")

# Read with version
df = spark.read.format("delta").option("versionAsOf", 0).load("/delta/table")

# Read with timestamp
df = spark.read.format("delta").option("timestampAsOf", "2024-01-01").load("/delta/table")

# Table history
spark.sql("DESCRIBE HISTORY my_table").show()

# Table details
spark.sql("DESCRIBE DETAIL my_table").show()
```

### MERGE Operations
```python
# Upsert with merge
deltaTable = DeltaTable.forPath(spark, "/delta/table")

deltaTable.alias("target").merge(
    source_df.alias("source"),
    "target.id = source.id"
).whenMatchedUpdate(set={
    "name": "source.name",
    "updated_at": "current_timestamp()"
}).whenNotMatchedInsert(values={
    "id": "source.id",
    "name": "source.name",
    "created_at": "current_timestamp()"
}).execute()

# Conditional merge
deltaTable.alias("target").merge(
    source_df.alias("source"),
    "target.id = source.id"
).whenMatchedUpdate(
    condition="target.version < source.version",
    set={"name": "source.name", "version": "source.version"}
).whenNotMatchedInsert(
    values={"id": "source.id", "name": "source.name", "version": "source.version"}
).execute()
```

### Optimization
```python
# Optimize table
spark.sql("OPTIMIZE my_table")

# Z-order optimization
spark.sql("OPTIMIZE my_table ZORDER BY (column1, column2)")

# Vacuum old files
spark.sql("VACUUM my_table RETAIN 168 HOURS")  # 7 days

# Auto-optimize settings
spark.conf.set("spark.databricks.delta.optimizeWrite.enabled", "true")
spark.conf.set("spark.databricks.delta.autoCompact.enabled", "true")
```

## Streaming

### Structured Streaming
```python
# Read stream
streaming_df = spark.readStream \
    .format("delta") \
    .load("/delta/streaming_source")

# Write stream
query = streaming_df.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/delta/checkpoints/stream1") \
    .trigger(processingTime="10 seconds") \
    .start("/delta/streaming_target")

# Monitor stream
query.status
query.lastProgress
query.stop()
```

### Kafka Streaming
```python
# Read from Kafka
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "topic_name") \
    .load()

# Parse Kafka messages
parsed_df = kafka_df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

# Write to Delta with deduplication
query = parsed_df.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/delta/checkpoints/kafka") \
    .trigger(processingTime="30 seconds") \
    .start("/delta/kafka_data")
```

### Watermarking
```python
# Add watermark for late data
watermarked_df = streaming_df.withWatermark("timestamp", "10 minutes")

# Windowed aggregation
windowed_counts = watermarked_df.groupBy(
    window(col("timestamp"), "5 minutes"),
    col("event_type")
).count()

# Write windowed results
query = windowed_counts.writeStream \
    .format("delta") \
    .outputMode("update") \
    .option("checkpointLocation", "/delta/checkpoints/windowed") \
    .start("/delta/windowed_counts")
```

## File System Operations

### DBFS Commands
```python
# List files
dbutils.fs.ls("/mnt/data/")

# Copy files
dbutils.fs.cp("/source/path", "/destination/path", recurse=True)

# Remove files
dbutils.fs.rm("/path/to/remove", recurse=True)

# Create directory
dbutils.fs.mkdirs("/new/directory")

# File info
dbutils.fs.head("/path/to/file", max_bytes=1000)
```

### Mounting Storage
```python
# Mount S3
dbutils.fs.mount(
    source="s3a://bucket-name/path",
    mount_point="/mnt/s3-data",
    extra_configs={
        "fs.s3a.access.key": dbutils.secrets.get("aws", "access-key"),
        "fs.s3a.secret.key": dbutils.secrets.get("aws", "secret-key")
    }
)

# Mount Azure Data Lake
dbutils.fs.mount(
    source="abfss://container@storage.dfs.core.windows.net/",
    mount_point="/mnt/adls",
    extra_configs={
        "fs.azure.account.auth.type": "OAuth",
        "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
        "fs.azure.account.oauth2.client.id": dbutils.secrets.get("azure", "client-id"),
        "fs.azure.account.oauth2.client.secret": dbutils.secrets.get("azure", "client-secret"),
        "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/tenant/oauth2/token"
    }
)

# Unmount
dbutils.fs.unmount("/mnt/mount-point")
```

## Secrets Management

### Secret Scopes
```bash
# CLI commands
databricks secrets create-scope --scope my-scope
databricks secrets put --scope my-scope --key my-key
databricks secrets list --scope my-scope
```

### Using Secrets
```python
# Get secret value
password = dbutils.secrets.get(scope="my-scope", key="db-password")

# List scopes
dbutils.secrets.listScopes()

# List keys in scope
dbutils.secrets.list("my-scope")
```

## Unity Catalog

### Catalog Operations
```sql
-- Create catalog
CREATE CATALOG production;

-- Use catalog
USE CATALOG production;

-- Create schema
CREATE SCHEMA production.sales;

-- Create table
CREATE TABLE production.sales.customers (
    id BIGINT,
    name STRING,
    email STRING
) USING DELTA;

-- Grant permissions
GRANT USE CATALOG ON CATALOG production TO `data-engineers`;
GRANT CREATE TABLE ON SCHEMA production.sales TO `data-engineers`;
```

### Data Governance
```python
# Table information
spark.sql("DESCRIBE EXTENDED catalog.schema.table").show()

# Column lineage
spark.sql("DESCRIBE HISTORY catalog.schema.table").show()

# Table properties
spark.sql("SHOW TBLPROPERTIES catalog.schema.table").show()
```

## Workflows and Jobs

### Job Configuration
```python
job_config = {
    "name": "ETL Pipeline",
    "tasks": [
        {
            "task_key": "extract",
            "notebook_task": {
                "notebook_path": "/Shared/etl/extract",
                "base_parameters": {"date": "{{job.start_date}}"}
            },
            "job_cluster_key": "etl-cluster"
        },
        {
            "task_key": "transform",
            "depends_on": [{"task_key": "extract"}],
            "notebook_task": {
                "notebook_path": "/Shared/etl/transform"
            },
            "job_cluster_key": "etl-cluster"
        }
    ],
    "job_clusters": [
        {
            "job_cluster_key": "etl-cluster",
            "new_cluster": {
                "spark_version": "11.3.x-scala2.12",
                "node_type_id": "i3.xlarge",
                "num_workers": 2
            }
        }
    ],
    "schedule": {
        "quartz_cron_expression": "0 0 9 * * ?",
        "timezone_id": "UTC"
    }
}
```

### Notebook Parameters
```python
# Get parameter values
dbutils.widgets.text("date", "2024-01-01")
date_param = dbutils.widgets.get("date")

# Remove widget
dbutils.widgets.remove("date")

# Exit notebook with value
dbutils.notebook.exit("Success")

# Run another notebook
result = dbutils.notebook.run("/path/to/notebook", 3600, {"param": "value"})
```

## Performance Optimization

### Spark Configuration
```python
# Adaptive Query Execution
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")

# Memory settings
spark.conf.set("spark.executor.memory", "8g")
spark.conf.set("spark.executor.cores", "4")
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

# Delta optimizations
spark.conf.set("spark.databricks.delta.optimizeWrite.enabled", "true")
spark.conf.set("spark.databricks.delta.autoCompact.enabled", "true")
```

### Caching
```python
# Cache DataFrame
df.cache()
df.persist(StorageLevel.MEMORY_AND_DISK)

# Unpersist
df.unpersist()

# Check cached tables
spark.catalog.listTables()
```

### Partitioning
```python
# Repartition
df_repartitioned = df.repartition(10)
df_repartitioned = df.repartition("column_name")

# Coalesce
df_coalesced = df.coalesce(5)

# Check partitions
print(f"Number of partitions: {df.rdd.getNumPartitions()}")
```

## SQL Analytics

### SQL Warehouses
```sql
-- Create SQL warehouse
CREATE WAREHOUSE analytics_warehouse
WITH (
    WAREHOUSE_SIZE = 'MEDIUM',
    AUTO_SUSPEND = 10,
    AUTO_RESUME = TRUE,
    MIN_CLUSTER_COUNT = 1,
    MAX_CLUSTER_COUNT = 3
);

-- Use warehouse
USE WAREHOUSE analytics_warehouse;
```

### Common SQL Patterns
```sql
-- Window functions
SELECT 
    customer_id,
    order_date,
    order_amount,
    SUM(order_amount) OVER (PARTITION BY customer_id ORDER BY order_date) as running_total,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) as order_rank
FROM orders;

-- CTEs
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        SUM(order_amount) as total_sales
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT * FROM monthly_sales ORDER BY month;

-- Pivot
SELECT *
FROM (
    SELECT customer_id, product_category, order_amount
    FROM orders
) PIVOT (
    SUM(order_amount)
    FOR product_category IN ('Electronics', 'Clothing', 'Books')
);
```

## Machine Learning

### MLflow Integration
```python
import mlflow
import mlflow.spark

# Start MLflow run
with mlflow.start_run():
    # Log parameters
    mlflow.log_param("num_trees", 100)
    
    # Log metrics
    mlflow.log_metric("accuracy", 0.95)
    
    # Log model
    mlflow.spark.log_model(model, "spark-model")
    
    # Log artifacts
    mlflow.log_artifact("model_summary.txt")
```

### Feature Store
```python
from databricks.feature_store import FeatureStoreClient

fs = FeatureStoreClient()

# Create feature table
fs.create_table(
    name="ml.customer_features",
    primary_keys=["customer_id"],
    df=feature_df,
    description="Customer behavioral features"
)

# Write features
fs.write_table(
    name="ml.customer_features",
    df=new_features_df,
    mode="merge"
)

# Read features
features_df = fs.read_table("ml.customer_features")
```

## Monitoring and Debugging

### Query Execution
```python
# Explain query plan
df.explain(True)

# Show query execution
df.show()

# Collect results
results = df.collect()

# Count records
count = df.count()
```

### Logging
```python
# Python logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Processing started")
logger.error("Error occurred", exc_info=True)

# Spark logs
spark.sparkContext.setLogLevel("INFO")
```

### Performance Monitoring
```python
# Query history
spark.sql("SELECT * FROM system.query.history WHERE start_time >= '2024-01-01'").show()

# Cluster metrics
spark.sql("SELECT * FROM system.compute.clusters").show()

# Job runs
spark.sql("SELECT * FROM system.workflow.job_runs WHERE start_time >= '2024-01-01'").show()
```

## Common Patterns

### Error Handling
```python
try:
    df = spark.read.format("delta").load("/delta/table")
    result = df.count()
    print(f"Successfully processed {result} records")
except Exception as e:
    print(f"Error processing data: {str(e)}")
    dbutils.notebook.exit("FAILED")
```

### Data Quality Checks
```python
def data_quality_check(df, table_name):
    total_rows = df.count()
    
    # Null checks
    null_counts = {}
    for column in df.columns:
        null_count = df.filter(col(column).isNull()).count()
        null_counts[column] = null_count
    
    # Duplicate check
    duplicate_count = total_rows - df.dropDuplicates().count()
    
    print(f"Table: {table_name}")
    print(f"Total rows: {total_rows}")
    print(f"Duplicates: {duplicate_count}")
    print(f"Null counts: {null_counts}")
    
    return null_counts, duplicate_count
```

### Incremental Processing
```python
def incremental_load(source_path, target_path, watermark_column):
    # Get last processed timestamp
    try:
        last_timestamp = spark.read.format("delta").load(target_path) \
            .agg(max(watermark_column)).collect()[0][0]
    except:
        last_timestamp = "1900-01-01"
    
    # Read incremental data
    incremental_df = spark.read.format("delta").load(source_path) \
        .filter(col(watermark_column) > last_timestamp)
    
    # Write incremental data
    incremental_df.write.format("delta").mode("append").save(target_path)
    
    return incremental_df.count()
```