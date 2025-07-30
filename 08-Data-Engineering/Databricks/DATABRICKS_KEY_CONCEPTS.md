# Databricks Key Concepts

## 1. Databricks Platform Overview
**What is Databricks**: A unified analytics platform that combines data engineering, data science, and machine learning on a cloud-based Apache Spark platform.

**Core Components**:
- **Workspace**: Collaborative environment for notebooks, jobs, and data
- **Clusters**: Managed Spark compute resources
- **Jobs**: Scheduled or triggered data processing workflows
- **Delta Lake**: Open-source storage layer for data lakes
- **MLflow**: Machine learning lifecycle management
- **Unity Catalog**: Unified governance for data and AI assets

**Architecture**:
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Data Sources  │───▶│   Delta Lake     │───▶│   Analytics     │
│   - S3/ADLS     │    │   - Bronze       │    │   - Dashboards  │
│   - Databases   │    │   - Silver       │    │   - ML Models   │
│   - Streaming   │    │   - Gold         │    │   - Reports     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 2. Clusters
**What they are**: Managed compute resources that run Spark applications.

**Cluster Types**:

### All-Purpose Clusters
```python
# Interactive development and exploration
cluster_config = {
    "cluster_name": "data-exploration",
    "spark_version": "13.3.x-scala2.12",
    "node_type_id": "i3.xlarge",
    "num_workers": 2,
    "autoscale": {
        "min_workers": 1,
        "max_workers": 8
    },
    "auto_termination_minutes": 120
}
```

### Job Clusters
```python
# Automated workloads
job_cluster_config = {
    "new_cluster": {
        "spark_version": "13.3.x-scala2.12",
        "node_type_id": "i3.large",
        "num_workers": 4,
        "spark_conf": {
            "spark.sql.adaptive.enabled": "true",
            "spark.sql.adaptive.coalescePartitions.enabled": "true"
        }
    }
}
```

**Cluster Optimization**:
```python
# Spark configuration for performance
spark_conf = {
    # Adaptive Query Execution
    "spark.sql.adaptive.enabled": "true",
    "spark.sql.adaptive.coalescePartitions.enabled": "true",
    
    # Memory optimization
    "spark.executor.memory": "8g",
    "spark.executor.cores": "4",
    "spark.executor.memoryFraction": "0.8",
    
    # Delta Lake optimizations
    "spark.databricks.delta.optimizeWrite.enabled": "true",
    "spark.databricks.delta.autoCompact.enabled": "true"
}
```

## 3. Delta Lake
**What it is**: Open-source storage layer that brings ACID transactions to Apache Spark and big data workloads.

**Key Features**:
- **ACID Transactions**: Ensures data consistency
- **Schema Evolution**: Handle schema changes gracefully
- **Time Travel**: Query historical versions of data
- **Upserts**: Merge operations for data updates
- **Streaming**: Real-time data ingestion and processing

**Creating Delta Tables**:
```python
# Create Delta table from DataFrame
df = spark.read.parquet("s3://bucket/raw-data/")
df.write.format("delta").mode("overwrite").save("/delta/customers")

# Create managed Delta table
df.write.format("delta").mode("overwrite").saveAsTable("customers")

# Create external Delta table
spark.sql("""
    CREATE TABLE customers
    USING DELTA
    LOCATION 's3://bucket/delta/customers'
    AS SELECT * FROM parquet.`s3://bucket/raw-data/customers.parquet`
""")
```

**Delta Operations**:
```python
from delta.tables import DeltaTable

# Load Delta table
delta_table = DeltaTable.forPath(spark, "/delta/customers")

# Upsert (Merge) operation
delta_table.alias("target").merge(
    updates_df.alias("source"),
    "target.customer_id = source.customer_id"
).whenMatchedUpdate(set={
    "email": "source.email",
    "last_updated": "source.last_updated"
}).whenNotMatchedInsert(values={
    "customer_id": "source.customer_id",
    "name": "source.name",
    "email": "source.email",
    "created_date": "source.created_date"
}).execute()

# Delete operation
delta_table.delete("status = 'inactive'")

# Update operation
delta_table.update(
    condition="city = 'Seattle'",
    set={"state": "'WA'"}
)
```

**Time Travel**:
```python
# Query historical data
df_yesterday = spark.read.format("delta").option("timestampAsOf", "2024-01-15").table("customers")

# Query by version
df_version_5 = spark.read.format("delta").option("versionAsOf", 5).table("customers")

# Restore table to previous version
spark.sql("RESTORE TABLE customers TO VERSION AS OF 5")

# View table history
spark.sql("DESCRIBE HISTORY customers").show()
```

## 4. Notebooks
**What they are**: Interactive documents that combine code, visualizations, and narrative text.

**Notebook Features**:
```python
# Magic commands
%sql
SELECT COUNT(*) FROM customers WHERE created_date >= '2024-01-01'

%fs ls /mnt/data/

%sh ls -la /tmp/

# Widgets for parameterization
dbutils.widgets.text("start_date", "2024-01-01", "Start Date")
dbutils.widgets.dropdown("environment", "dev", ["dev", "staging", "prod"], "Environment")

start_date = dbutils.widgets.get("start_date")
environment = dbutils.widgets.get("environment")
```

**Collaboration Features**:
```python
# Comments and discussions
# TODO: Optimize this query for better performance
df = spark.sql(f"""
    SELECT customer_id, SUM(order_total) as lifetime_value
    FROM orders 
    WHERE order_date >= '{start_date}'
    GROUP BY customer_id
""")

# Version control integration
# Notebooks can be synced with Git repositories
```

## 5. Jobs and Workflows
**What they are**: Automated execution of notebooks, JARs, or Python scripts.

**Job Configuration**:
```python
job_config = {
    "name": "daily_etl_pipeline",
    "new_cluster": {
        "spark_version": "13.3.x-scala2.12",
        "node_type_id": "i3.large",
        "num_workers": 4
    },
    "notebook_task": {
        "notebook_path": "/Shared/ETL/daily_pipeline",
        "base_parameters": {
            "environment": "prod",
            "date": "{{ds}}"
        }
    },
    "timeout_seconds": 3600,
    "max_retries": 2,
    "schedule": {
        "quartz_cron_expression": "0 0 2 * * ?",
        "timezone_id": "UTC"
    }
}
```

**Multi-task Jobs**:
```python
workflow_config = {
    "name": "data_pipeline_workflow",
    "tasks": [
        {
            "task_key": "extract_data",
            "notebook_task": {
                "notebook_path": "/ETL/extract"
            }
        },
        {
            "task_key": "transform_data",
            "notebook_task": {
                "notebook_path": "/ETL/transform"
            },
            "depends_on": [{"task_key": "extract_data"}]
        },
        {
            "task_key": "load_data",
            "notebook_task": {
                "notebook_path": "/ETL/load"
            },
            "depends_on": [{"task_key": "transform_data"}]
        }
    ]
}
```

## 6. Data Engineering Patterns
**Medallion Architecture (Bronze-Silver-Gold)**:

### Bronze Layer (Raw Data)
```python
# Ingest raw data with minimal processing
bronze_df = (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "/mnt/schema/bronze")
    .load("/mnt/raw-data/")
    .withColumn("ingestion_timestamp", current_timestamp())
    .withColumn("source_file", input_file_name())
)

bronze_df.writeStream.format("delta").outputMode("append").option("checkpointLocation", "/mnt/checkpoints/bronze").table("bronze.raw_events")
```

### Silver Layer (Cleaned Data)
```python
# Clean and standardize data
silver_df = spark.readStream.table("bronze.raw_events").select(
    col("event_id"),
    col("user_id").cast("long"),
    to_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss").alias("event_timestamp"),
    col("event_type"),
    from_json(col("properties"), schema).alias("parsed_properties")
).filter(col("user_id").isNotNull())

silver_df.writeStream.format("delta").outputMode("append").option("checkpointLocation", "/mnt/checkpoints/silver").table("silver.clean_events")
```

### Gold Layer (Business Logic)
```python
# Aggregate for business use cases
gold_df = spark.readStream.table("silver.clean_events").groupBy(
    window(col("event_timestamp"), "1 hour"),
    col("event_type")
).agg(
    count("*").alias("event_count"),
    countDistinct("user_id").alias("unique_users")
).select(
    col("window.start").alias("hour_start"),
    col("event_type"),
    col("event_count"),
    col("unique_users")
)

gold_df.writeStream.format("delta").outputMode("complete").option("checkpointLocation", "/mnt/checkpoints/gold").table("gold.hourly_metrics")
```

## 7. Streaming
**Structured Streaming with Delta Lake**:

```python
# Read streaming data
stream_df = (spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "user_events")
    .load()
)

# Process streaming data
processed_df = (stream_df
    .select(from_json(col("value").cast("string"), event_schema).alias("data"))
    .select("data.*")
    .withColumn("processing_time", current_timestamp())
    .withWatermark("event_timestamp", "10 minutes")
)

# Write to Delta table
query = (processed_df.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/mnt/checkpoints/events")
    .trigger(processingTime="30 seconds")
    .table("events")
)
```

**Stream-Stream Joins**:
```python
# Join two streams
impressions = spark.readStream.table("impressions").withWatermark("timestamp", "2 hours")
clicks = spark.readStream.table("clicks").withWatermark("timestamp", "3 hours")

joined = impressions.join(
    clicks,
    expr("""
        impressions.ad_id = clicks.ad_id AND
        clicks.timestamp >= impressions.timestamp AND
        clicks.timestamp <= impressions.timestamp + interval 1 hour
    """),
    "leftOuter"
)
```

## 8. Unity Catalog
**What it is**: Unified governance solution for data and AI assets across clouds.

**Three-Level Namespace**:
```sql
-- catalog.schema.table
SELECT * FROM production.sales.customers;
SELECT * FROM development.analytics.user_metrics;
```

**Creating Catalogs and Schemas**:
```sql
-- Create catalog
CREATE CATALOG IF NOT EXISTS production;

-- Create schema
CREATE SCHEMA IF NOT EXISTS production.sales;

-- Create managed table
CREATE TABLE production.sales.customers (
    customer_id BIGINT,
    name STRING,
    email STRING,
    created_at TIMESTAMP
) USING DELTA;
```

**Access Control**:
```sql
-- Grant permissions
GRANT USE CATALOG ON CATALOG production TO `data-engineers`;
GRANT USE SCHEMA ON SCHEMA production.sales TO `analysts`;
GRANT SELECT ON TABLE production.sales.customers TO `reporting-team`;

-- Create service principal
CREATE SERVICE PRINCIPAL 'etl-service-principal';
GRANT MODIFY ON SCHEMA production.raw TO SERVICE PRINCIPAL 'etl-service-principal';
```

## 9. Performance Optimization
**Partitioning**:
```python
# Partition by date for time-series data
df.write.format("delta").partitionBy("date").mode("overwrite").save("/delta/events")

# Multi-level partitioning
df.write.format("delta").partitionBy("year", "month").mode("overwrite").save("/delta/sales")
```

**Z-Ordering**:
```sql
-- Optimize table layout for better query performance
OPTIMIZE customers ZORDER BY (customer_id, registration_date);

-- Auto-optimize
ALTER TABLE customers SET TBLPROPERTIES (
    'delta.autoOptimize.optimizeWrite' = 'true',
    'delta.autoOptimize.autoCompact' = 'true'
);
```

**Caching**:
```python
# Cache frequently accessed data
df.cache()
df.count()  # Trigger caching

# Persist with storage level
from pyspark import StorageLevel
df.persist(StorageLevel.MEMORY_AND_DISK_SER)
```

**Broadcast Joins**:
```python
from pyspark.sql.functions import broadcast

# Broadcast small dimension tables
large_df.join(broadcast(small_df), "key")
```

## 10. MLflow Integration
**Experiment Tracking**:
```python
import mlflow
import mlflow.sklearn

# Start MLflow run
with mlflow.start_run():
    # Log parameters
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 6)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, max_depth=6)
    model.fit(X_train, y_train)
    
    # Log metrics
    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)
    
    # Log model
    mlflow.sklearn.log_model(model, "random_forest_model")
```

**Model Registry**:
```python
# Register model
model_uri = f"runs:/{run_id}/random_forest_model"
mlflow.register_model(model_uri, "customer_churn_model")

# Load model for inference
model = mlflow.sklearn.load_model("models:/customer_churn_model/Production")
predictions = model.predict(new_data)
```