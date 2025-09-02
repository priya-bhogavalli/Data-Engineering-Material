# 🧱 Databricks - Comprehensive Interview Questions (100+ Questions)

## 📋 Table of Contents

1. [Basic Level Questions (1-25)](#basic-level-questions-1-25)
2. [Intermediate Level Questions (26-50)](#intermediate-level-questions-26-50)
3. [Advanced Level Questions (51-75)](#advanced-level-questions-51-75)
4. [Architecture & Performance (76-100)](#architecture--performance-76-100)
5. [Scenario-Based Questions (101-110)](#scenario-based-questions-101-110)

---

## Basic Level Questions (1-25)

### 1. What is Databricks and how does it differ from Apache Spark?
**Answer:**
Databricks is a unified analytics platform built on Apache Spark that provides:
- Managed Spark clusters with auto-scaling
- Collaborative notebooks with multiple language support
- Built-in data visualization and ML capabilities
- Delta Lake for reliable data lakes
- MLflow for ML lifecycle management

```python
# Databricks notebook cell
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("DataEngineering").getOrCreate()

# Read data from Delta Lake
df = spark.read.format("delta").load("/mnt/data/customers")
df.show()
```

### 2. Explain Delta Lake and its key features
**Answer:**
Delta Lake is an open-source storage layer that brings ACID transactions to Apache Spark and big data workloads.

Key features:
- **ACID Transactions**: Ensures data consistency
- **Schema Evolution**: Handle schema changes gracefully
- **Time Travel**: Query historical versions of data
- **Upserts**: Merge operations for data updates

```python
# Create Delta table
df.write.format("delta").mode("overwrite").save("/delta/customers")

# Time travel query
historical_df = spark.read.format("delta").option("versionAsOf", 0).load("/delta/customers")

# Upsert operation
from delta.tables import DeltaTable
deltaTable = DeltaTable.forPath(spark, "/delta/customers")
deltaTable.alias("customers").merge(
    updates.alias("updates"),
    "customers.id = updates.id"
).whenMatchedUpdate(set = {
    "name": "updates.name",
    "email": "updates.email"
}).whenNotMatchedInsert(values = {
    "id": "updates.id",
    "name": "updates.name",
    "email": "updates.email"
}).execute()
```

### 3. What are Databricks clusters and their types?
**Answer:**
- **All-Purpose Clusters**: Interactive analysis, shared across users
- **Job Clusters**: Automated workloads, terminated after job completion
- **SQL Warehouses**: Optimized for SQL queries and BI tools

```python
# Cluster configuration example
cluster_config = {
    "cluster_name": "data-engineering-cluster",
    "spark_version": "11.3.x-scala2.12",
    "node_type_id": "i3.xlarge",
    "num_workers": 2,
    "autoscale": {
        "min_workers": 1,
        "max_workers": 8
    }
}
```

### 4. How do you mount external storage in Databricks?
**Answer:**
```python
# Mount S3 bucket
dbutils.fs.mount(
    source="s3a://my-bucket/data",
    mount_point="/mnt/data",
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
        "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/tenant-id/oauth2/token"
    }
)
```

### 5. What is Unity Catalog in Databricks?
**Answer:**
Unity Catalog is a unified governance solution for data and AI assets across Databricks workspaces.

Features:
- Centralized access control
- Data lineage tracking
- Data discovery and search
- Cross-workspace data sharing

```sql
-- Create catalog and schema
CREATE CATALOG production;
CREATE SCHEMA production.sales;

-- Grant permissions
GRANT USE CATALOG ON CATALOG production TO `data-engineers`;
GRANT CREATE TABLE ON SCHEMA production.sales TO `data-engineers`;

-- Create managed table
CREATE TABLE production.sales.customers (
    id BIGINT,
    name STRING,
    email STRING,
    created_at TIMESTAMP
) USING DELTA;
```

### 6. How do you handle secrets in Databricks?
**Answer:**
```python
# Create secret scope (CLI command)
# databricks secrets create-scope --scope my-scope

# Store secret (CLI command)
# databricks secrets put --scope my-scope --key db-password

# Access secrets in notebook
password = dbutils.secrets.get(scope="my-scope", key="db-password")

# Use in connection
jdbc_url = "jdbc:postgresql://hostname:5432/database"
connection_properties = {
    "user": "username",
    "password": password,
    "driver": "org.postgresql.Driver"
}

df = spark.read.jdbc(jdbc_url, "table_name", properties=connection_properties)
```

### 7. What are Databricks workflows and how do you create them?
**Answer:**
Databricks Workflows (formerly Jobs) orchestrate data processing tasks.

```python
# Job configuration
job_config = {
    "name": "ETL Pipeline",
    "tasks": [
        {
            "task_key": "extract",
            "notebook_task": {
                "notebook_path": "/Shared/etl/extract",
                "base_parameters": {"date": "2024-01-01"}
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
    ]
}
```

### 8. How do you optimize Databricks performance?
**Answer:**
```python
# Enable adaptive query execution
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")

# Optimize file sizes
spark.conf.set("spark.sql.files.maxPartitionBytes", "134217728")  # 128MB

# Cache frequently used data
df.cache()

# Use Delta Lake optimizations
# OPTIMIZE command for file compaction
spark.sql("OPTIMIZE delta.`/path/to/table`")

# Z-ORDER for data skipping
spark.sql("OPTIMIZE delta.`/path/to/table` ZORDER BY (column1, column2)")

# Partition pruning
partitioned_df = df.where("date >= '2024-01-01'")
```

### 9. What is the Databricks File System (DBFS)?
**Answer:**
DBFS is a distributed file system mounted into Databricks workspaces.

```python
# List DBFS contents
dbutils.fs.ls("/")

# Copy files
dbutils.fs.cp("/mnt/source/file.csv", "/mnt/destination/file.csv")

# Remove files
dbutils.fs.rm("/mnt/temp/", True)  # Recursive delete

# Read file content
content = dbutils.fs.head("/mnt/data/sample.txt")
print(content)
```

### 10. How do you work with notebooks in Databricks?
**Answer:**
```python
# Run another notebook
result = dbutils.notebook.run("/path/to/notebook", 60, {"param1": "value1"})

# Exit with value
dbutils.notebook.exit("success")

# Get notebook parameters
param_value = dbutils.widgets.get("parameter_name")

# Create widgets
dbutils.widgets.text("start_date", "2024-01-01", "Start Date")
dbutils.widgets.dropdown("environment", "dev", ["dev", "staging", "prod"], "Environment")
```

### 11. What are Databricks libraries and how do you manage them?
**Answer:**
```python
# Install library via UI or cluster configuration
# Or use %pip magic command in notebook

%pip install pandas==1.3.0
%pip install custom-package

# Import and use
import pandas as pd
import custom_package

# Check installed packages
%pip list
```

### 12. How do you connect to external databases from Databricks?
**Answer:**
```python
# PostgreSQL connection
postgres_df = spark.read.format("jdbc") \
    .option("url", "jdbc:postgresql://hostname:5432/database") \
    .option("dbtable", "customers") \
    .option("user", "username") \
    .option("password", "password") \
    .option("driver", "org.postgresql.Driver") \
    .load()

# SQL Server connection
sqlserver_df = spark.read.format("jdbc") \
    .option("url", "jdbc:sqlserver://hostname:1433;database=mydb") \
    .option("dbtable", "orders") \
    .option("user", "username") \
    .option("password", "password") \
    .load()

# Write back to database
df.write.format("jdbc") \
    .option("url", "jdbc:postgresql://hostname:5432/database") \
    .option("dbtable", "processed_data") \
    .option("user", "username") \
    .option("password", "password") \
    .mode("overwrite") \
    .save()
```

### 13. What is Databricks Runtime and its versions?
**Answer:**
Databricks Runtime is the set of core components that run on Databricks clusters.

Types:
- **Standard Runtime**: Core Spark functionality
- **ML Runtime**: Pre-installed ML libraries
- **Genomics Runtime**: Bioinformatics tools
- **Light Runtime**: Minimal footprint for simple workloads

```python
# Check runtime version
print(spark.version)
print(spark.conf.get("spark.databricks.clusterUsageTags.sparkVersion"))
```

### 14. How do you handle data formats in Databricks?
**Answer:**
```python
# Read various formats
# Parquet
parquet_df = spark.read.parquet("/mnt/data/parquet_files/")

# JSON
json_df = spark.read.json("/mnt/data/json_files/")

# CSV with options
csv_df = spark.read.option("header", "true") \
    .option("inferSchema", "true") \
    .option("delimiter", ",") \
    .csv("/mnt/data/csv_files/")

# Avro
avro_df = spark.read.format("avro").load("/mnt/data/avro_files/")

# Delta Lake
delta_df = spark.read.format("delta").load("/mnt/data/delta_table/")

# Write in different formats
df.write.mode("overwrite").parquet("/mnt/output/parquet/")
df.write.mode("overwrite").json("/mnt/output/json/")
df.write.format("delta").mode("overwrite").save("/mnt/output/delta/")
```

### 15. What are Databricks widgets and how do you use them?
**Answer:**
```python
# Create different widget types
dbutils.widgets.text("input_path", "/mnt/default", "Input Path")
dbutils.widgets.dropdown("environment", "dev", ["dev", "staging", "prod"], "Environment")
dbutils.widgets.multiselect("regions", "us-east-1", ["us-east-1", "us-west-2", "eu-west-1"], "Regions")

# Get widget values
input_path = dbutils.widgets.get("input_path")
environment = dbutils.widgets.get("environment")
regions = dbutils.widgets.get("regions").split(",")

# Use in code
df = spark.read.parquet(input_path)
if environment == "prod":
    df = df.filter(col("status") == "active")

# Remove widgets
dbutils.widgets.removeAll()
```

### 16. How do you implement error handling in Databricks?
**Answer:**
```python
def safe_data_processing():
    try:
        # Data processing logic
        df = spark.read.parquet("/mnt/data/input/")
        
        # Validate data
        if df.count() == 0:
            raise ValueError("Input dataset is empty")
        
        # Process data
        result_df = df.groupBy("category").count()
        
        # Write results
        result_df.write.mode("overwrite").parquet("/mnt/data/output/")
        
        return "Success"
        
    except Exception as e:
        # Log error
        print(f"Error in data processing: {str(e)}")
        
        # Write to error log
        error_df = spark.createDataFrame([(str(e), current_timestamp())], ["error_message", "timestamp"])
        error_df.write.mode("append").parquet("/mnt/logs/errors/")
        
        # Re-raise or handle gracefully
        raise e

# Usage
try:
    result = safe_data_processing()
    print(result)
except Exception as e:
    dbutils.notebook.exit(f"FAILED: {str(e)}")
```

### 17. What is Auto Loader in Databricks?
**Answer:**
Auto Loader incrementally and efficiently processes new data files as they arrive in cloud storage.

```python
# Basic Auto Loader setup
df = spark.readStream.format("cloudFiles") \
    .option("cloudFiles.format", "json") \
    .option("cloudFiles.schemaLocation", "/mnt/schema/") \
    .load("/mnt/data/input/")

# Write stream
query = df.writeStream \
    .format("delta") \
    .option("checkpointLocation", "/mnt/checkpoints/") \
    .start("/mnt/data/output/")

# Auto Loader with schema evolution
df = spark.readStream.format("cloudFiles") \
    .option("cloudFiles.format", "json") \
    .option("cloudFiles.schemaLocation", "/mnt/schema/") \
    .option("cloudFiles.schemaEvolutionMode", "addNewColumns") \
    .load("/mnt/data/input/")
```

### 18. How do you work with streaming data in Databricks?
**Answer:**
```python
# Read streaming data
streaming_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "events") \
    .load()

# Parse JSON data
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
    StructField("user_id", IntegerType()),
    StructField("event_type", StringType()),
    StructField("timestamp", StringType())
])

parsed_df = streaming_df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

# Write to Delta Lake
query = parsed_df.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/mnt/checkpoints/events") \
    .start("/mnt/delta/events")

query.awaitTermination()
```

### 19. What are Databricks SQL warehouses?
**Answer:**
SQL warehouses are compute resources for running SQL queries and connecting BI tools.

```sql
-- Create SQL warehouse via UI or API
-- Connect BI tools like Tableau, Power BI

-- Query data
SELECT 
    category,
    COUNT(*) as count,
    AVG(price) as avg_price
FROM products
GROUP BY category
ORDER BY count DESC;

-- Create views for BI consumption
CREATE VIEW sales_summary AS
SELECT 
    DATE_TRUNC('month', order_date) as month,
    region,
    SUM(amount) as total_sales
FROM orders
GROUP BY DATE_TRUNC('month', order_date), region;
```

### 20. How do you implement data quality checks in Databricks?
**Answer:**
```python
from pyspark.sql.functions import col, count, when, isnan, isnull

def data_quality_checks(df, table_name):
    """Comprehensive data quality validation"""
    
    results = []
    total_rows = df.count()
    
    # Null checks
    for column in df.columns:
        null_count = df.filter(col(column).isNull()).count()
        null_percentage = (null_count / total_rows) * 100
        
        results.append({
            "table": table_name,
            "check": f"null_check_{column}",
            "passed": null_percentage < 5,
            "value": null_percentage,
            "threshold": 5
        })
    
    # Duplicate checks
    duplicate_count = df.count() - df.dropDuplicates().count()
    results.append({
        "table": table_name,
        "check": "duplicate_check",
        "passed": duplicate_count == 0,
        "value": duplicate_count,
        "threshold": 0
    })
    
    # Custom business rules
    if "email" in df.columns:
        invalid_emails = df.filter(~col("email").rlike(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")).count()
        results.append({
            "table": table_name,
            "check": "email_format_check",
            "passed": invalid_emails == 0,
            "value": invalid_emails,
            "threshold": 0
        })
    
    return spark.createDataFrame(results)

# Usage
df = spark.read.format("delta").load("/mnt/data/customers")
quality_results = data_quality_checks(df, "customers")
quality_results.show()
```

### 21. What is MLflow and how does it integrate with Databricks?
**Answer:**
MLflow is an open-source platform for managing ML lifecycle, fully integrated with Databricks.

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Start MLflow experiment
mlflow.set_experiment("/Shared/ml_experiments/customer_churn")

with mlflow.start_run():
    # Train model
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    
    # Make predictions
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    # Log parameters and metrics
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("accuracy", accuracy)
    
    # Log model
    mlflow.sklearn.log_model(model, "model")
    
    # Log artifacts
    mlflow.log_artifact("feature_importance.png")

# Load model for inference
model_uri = "runs:/<run_id>/model"
loaded_model = mlflow.sklearn.load_model(model_uri)
```

### 22. How do you handle large datasets in Databricks?
**Answer:**
```python
# Optimize for large datasets
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")

# Partition data appropriately
large_df = spark.read.parquet("/mnt/data/large_dataset/")

# Check current partitions
print(f"Current partitions: {large_df.rdd.getNumPartitions()}")

# Repartition if needed
optimal_partitions = large_df.count() // 1000000  # 1M records per partition
if optimal_partitions > large_df.rdd.getNumPartitions():
    large_df = large_df.repartition(optimal_partitions)

# Use broadcast joins for small tables
small_df = spark.read.parquet("/mnt/data/small_lookup/")
result = large_df.join(broadcast(small_df), "key")

# Cache intermediate results
large_df.cache()

# Use columnar formats
large_df.write.mode("overwrite").parquet("/mnt/data/optimized/")
```

### 23. What are Databricks repos and how do you use them?
**Answer:**
Databricks Repos provide Git integration for version control of notebooks and code.

```python
# Clone repository
# Via UI: Repos -> Add Repo -> Git URL

# Work with notebooks in repo
# Edit, commit, push changes via UI

# Use repo files in notebooks
%run ./utils/helper_functions

# Import modules from repo
import sys
sys.path.append("/Workspace/Repos/username/repo_name/src")
from my_module import my_function

# Programmatic Git operations
import subprocess

def git_commit_and_push(message):
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", message])
    subprocess.run(["git", "push"])
```

### 24. How do you implement data lineage in Databricks?
**Answer:**
```python
def track_data_lineage():
    """Implement custom data lineage tracking"""
    
    lineage_info = {
        "job_id": spark.conf.get("spark.databricks.clusterUsageTags.jobId", "interactive"),
        "notebook_path": dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get(),
        "timestamp": current_timestamp(),
        "user": dbutils.notebook.entry_point.getDbutils().notebook().getContext().userName().get()
    }
    
    # Track input sources
    input_sources = [
        {"path": "/mnt/data/raw/events", "type": "parquet", "operation": "read"},
        {"path": "/mnt/data/raw/users", "type": "delta", "operation": "read"}
    ]
    
    # Track output targets
    output_targets = [
        {"path": "/mnt/data/processed/user_events", "type": "delta", "operation": "write"}
    ]
    
    # Create lineage record
    lineage_record = {
        **lineage_info,
        "input_sources": input_sources,
        "output_targets": output_targets,
        "transformation_logic": "Join events with user data and apply business rules"
    }
    
    # Store lineage information
    lineage_df = spark.createDataFrame([lineage_record])
    lineage_df.write.format("delta").mode("append").save("/mnt/metadata/lineage")

# Unity Catalog lineage (automatic)
def query_unity_catalog_lineage():
    """Query built-in Unity Catalog lineage"""
    
    lineage_query = """
    SELECT 
        source_table_full_name,
        target_table_full_name,
        created_at,
        created_by
    FROM system.access.table_lineage
    WHERE target_table_full_name = 'catalog.schema.table'
    """
    
    return spark.sql(lineage_query)
```

### 25. What are Databricks feature stores?
**Answer:**
Feature stores centralize feature engineering and serving for ML.

```python
from databricks.feature_store import FeatureStoreClient

fs = FeatureStoreClient()

# Create feature table
def create_user_features():
    user_features = spark.sql("""
        SELECT 
            user_id,
            COUNT(*) as total_events_30d,
            AVG(session_duration) as avg_session_duration,
            MAX(last_activity) as last_activity_date,
            current_timestamp() as feature_timestamp
        FROM user_events 
        WHERE event_date >= current_date() - 30
        GROUP BY user_id
    """)
    
    fs.create_table(
        name="ml.user_features",
        primary_keys=["user_id"],
        df=user_features,
        description="User behavioral features for ML models"
    )

# Use features in training
feature_lookups = [
    FeatureLookup(
        table_name="ml.user_features",
        lookup_key="user_id"
    )
]

training_set = fs.create_training_set(
    df=spark.table("ml.training_labels"),
    feature_lookups=feature_lookups,
    label="target"
)

training_df = training_set.load_df()
```

---

## Intermediate Level Questions (26-50)

### 26. Implement a medallion architecture in Databricks
**Answer:**
```python
# Bronze Layer - Raw data ingestion
def ingest_bronze_data():
    raw_df = spark.read.format("json").load("/mnt/raw-data/")
    
    # Add metadata columns
    bronze_df = raw_df.withColumn("ingestion_timestamp", current_timestamp()) \
                     .withColumn("source_file", input_file_name())
    
    # Write to Delta Lake
    bronze_df.write.format("delta").mode("append").save("/mnt/delta/bronze/events")

# Silver Layer - Cleaned and validated data
def process_silver_data():
    bronze_df = spark.read.format("delta").load("/mnt/delta/bronze/events")
    
    # Data cleaning and validation
    silver_df = bronze_df.filter(col("user_id").isNotNull()) \
                         .withColumn("event_date", to_date(col("timestamp"))) \
                         .dropDuplicates(["user_id", "event_id"])
    
    # Write to silver layer
    silver_df.write.format("delta").mode("overwrite").save("/mnt/delta/silver/events")

# Gold Layer - Business aggregations
def create_gold_aggregations():
    silver_df = spark.read.format("delta").load("/mnt/delta/silver/events")
    
    # Business metrics
    daily_metrics = silver_df.groupBy("event_date", "event_type") \
                            .agg(count("*").alias("event_count"),
                                 countDistinct("user_id").alias("unique_users"))
    
    daily_metrics.write.format("delta").mode("overwrite").save("/mnt/delta/gold/daily_metrics")
```

### 27. How do you implement Change Data Capture (CDC) in Databricks?
**Answer:**
```python
from delta.tables import DeltaTable

def process_cdc_data(source_path, target_path):
    # Read CDC data
    cdc_df = spark.read.format("delta").load(source_path)
    
    # Create or get target table
    if DeltaTable.isDeltaTable(spark, target_path):
        target_table = DeltaTable.forPath(spark, target_path)
    else:
        # Create initial table
        initial_df = cdc_df.filter(col("operation") == "INSERT")
        initial_df.write.format("delta").save(target_path)
        target_table = DeltaTable.forPath(spark, target_path)
    
    # Process different operations
    inserts = cdc_df.filter(col("operation") == "INSERT")
    updates = cdc_df.filter(col("operation") == "UPDATE")
    deletes = cdc_df.filter(col("operation") == "DELETE")
    
    # Apply changes
    if updates.count() > 0:
        target_table.alias("target").merge(
            updates.alias("updates"),
            "target.id = updates.id"
        ).whenMatchedUpdateAll().execute()
    
    if inserts.count() > 0:
        target_table.alias("target").merge(
            inserts.alias("inserts"),
            "target.id = inserts.id"
        ).whenNotMatchedInsertAll().execute()
    
    if deletes.count() > 0:
        target_table.alias("target").merge(
            deletes.alias("deletes"),
            "target.id = deletes.id"
        ).whenMatchedDelete().execute()
```

### 28. How do you handle streaming data in Databricks?
**Answer:**
```python
# Structured Streaming with Delta Lake
def process_streaming_data():
    # Read from Kafka
    streaming_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "events") \
        .load()
    
    # Parse JSON data
    parsed_df = streaming_df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")
    
    # Write to Delta Lake with checkpointing
    query = parsed_df.writeStream \
        .format("delta") \
        .outputMode("append") \
        .option("checkpointLocation", "/mnt/checkpoints/events") \
        .trigger(processingTime="10 seconds") \
        .start("/mnt/delta/streaming/events")
    
    return query

# Stream processing with watermarking
def process_with_watermark():
    streaming_df = spark.readStream.format("delta").load("/mnt/delta/streaming/events")
    
    # Add watermark for late data handling
    watermarked_df = streaming_df.withWatermark("timestamp", "10 minutes")
    
    # Windowed aggregation
    windowed_counts = watermarked_df.groupBy(
        window(col("timestamp"), "5 minutes"),
        col("event_type")
    ).count()
    
    query = windowed_counts.writeStream \
        .format("delta") \
        .outputMode("update") \
        .option("checkpointLocation", "/mnt/checkpoints/windowed") \
        .start("/mnt/delta/aggregated/windowed_counts")
    
    return query
```

### 29. How do you implement slowly changing dimensions (SCD) in Databricks?
**Answer:**
```python
from delta.tables import DeltaTable

def implement_scd_type2(source_df, target_path, business_key, scd_columns):
    """Implement SCD Type 2 using Delta Lake merge"""
    
    # Add SCD metadata to source
    source_with_meta = source_df.withColumn("effective_date", current_date()) \
                                .withColumn("end_date", lit(None).cast("date")) \
                                .withColumn("is_current", lit(True))
    
    if DeltaTable.isDeltaTable(spark, target_path):
        target_table = DeltaTable.forPath(spark, target_path)
        
        # Identify changed records
        merge_condition = f"target.{business_key} = source.{business_key} AND target.is_current = true"
        
        # Build change detection condition
        change_conditions = [f"target.{col} != source.{col}" for col in scd_columns]
        change_condition = " OR ".join(change_conditions)
        
        # Merge operation
        target_table.alias("target").merge(
            source_with_meta.alias("source"),
            merge_condition
        ).whenMatchedUpdate(
            condition = change_condition,
            set = {
                "end_date": "current_date()",
                "is_current": "false"
            }
        ).whenNotMatchedInsert(
            values = {col: f"source.{col}" for col in source_with_meta.columns}
        ).execute()
        
        # Insert new versions of changed records
        changed_records = source_with_meta.alias("source").join(
            target_table.toDF().alias("target"),
            (col(f"source.{business_key}") == col(f"target.{business_key}")) &
            (col("target.end_date") == current_date()),
            "inner"
        ).select("source.*")
        
        if changed_records.count() > 0:
            changed_records.write.format("delta").mode("append").save(target_path)
    
    else:
        # Initial load
        source_with_meta.write.format("delta").save(target_path)

# Usage
source_df = spark.read.format("delta").load("/mnt/staging/customers")
implement_scd_type2(
    source_df, 
    "/mnt/dimensions/dim_customer",
    "customer_id",
    ["name", "email", "address"]
)
```

### 30. How do you monitor and troubleshoot Databricks jobs?
**Answer:**
```python
# Job monitoring with custom metrics
def monitor_job_execution():
    """Custom job monitoring and alerting"""
    
    # Log job metrics
    job_metrics = {
        "job_id": dbutils.widgets.get("job_id"),
        "start_time": datetime.now(),
        "cluster_id": spark.conf.get("spark.databricks.clusterUsageTags.clusterId"),
        "records_processed": 0,
        "status": "running"
    }
    
    try:
        # Your ETL logic here
        df = spark.read.format("delta").load("/mnt/source")
        processed_df = df.transform(your_transformation_logic)
        processed_df.write.format("delta").mode("overwrite").save("/mnt/target")
        
        job_metrics["records_processed"] = processed_df.count()
        job_metrics["status"] = "success"
        
    except Exception as e:
        job_metrics["status"] = "failed"
        job_metrics["error_message"] = str(e)
        
        # Send alert
        send_alert(f"Job {job_metrics['job_id']} failed: {str(e)}")
        raise
    
    finally:
        job_metrics["end_time"] = datetime.now()
        job_metrics["duration_minutes"] = (job_metrics["end_time"] - job_metrics["start_time"]).total_seconds() / 60
        
        # Log to monitoring table
        metrics_df = spark.createDataFrame([job_metrics])
        metrics_df.write.format("delta").mode("append").save("/mnt/monitoring/job_metrics")

# Performance monitoring
def analyze_query_performance():
    """Analyze Spark query performance"""
    
    # Enable query execution metrics
    spark.conf.set("spark.sql.queryExecutionListeners", 
                   "org.apache.spark.sql.util.QueryExecutionMetricsListener")
    
    # Query with explain plan
    df = spark.sql("SELECT * FROM delta.`/mnt/large_table` WHERE date >= '2024-01-01'")
    df.explain(True)  # Show physical plan
    
    # Analyze partition pruning
    spark.sql("DESCRIBE DETAIL delta.`/mnt/large_table`").show()
    
    # Check file sizes and optimization opportunities
    spark.sql("DESCRIBE HISTORY delta.`/mnt/large_table`").show()
```

---

*[Continue with remaining 70+ questions covering Advanced Level, Architecture & Performance, and Scenario-Based sections...]*