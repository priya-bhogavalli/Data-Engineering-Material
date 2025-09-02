# Databricks Complete Guide for Data Engineering

## 🎯 Overview
Comprehensive guide covering Databricks platform, Delta Lake, performance optimization, and data engineering best practices.

## 📋 Table of Contents

1. [Platform Overview](#1-platform-overview)
2. [Core Concepts](#2-core-concepts)
3. [Delta Lake](#3-delta-lake)
4. [Performance Optimization](#4-performance-optimization)
5. [Security & Governance](#5-security--governance)
6. [Best Practices](#6-best-practices)
7. [Interview Questions](#7-interview-questions)
8. [Advanced Topics](#8-advanced-topics)

---

## 1. Platform Overview

### What is Databricks
Unified analytics platform that combines data engineering, data science, and machine learning on a cloud-based Apache Spark platform.

**Core Components:**
- **Workspace**: Collaborative environment for notebooks, jobs, and data
- **Clusters**: Managed Spark compute resources
- **Jobs**: Scheduled or triggered data processing workflows
- **Delta Lake**: Open-source storage layer for data lakes
- **MLflow**: Machine learning lifecycle management
- **Unity Catalog**: Unified governance for data and AI assets

**Architecture:**
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Data Sources  │───▶│   Delta Lake     │───▶│   Analytics     │
│   - S3/ADLS     │    │   - Bronze       │    │   - Dashboards  │
│   - Databases   │    │   - Silver       │    │   - ML Models   │
│   - Streaming   │    │   - Gold         │    │   - Reports     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

---

## 2. Core Concepts

### Clusters

**Cluster Types:**

#### All-Purpose Clusters
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

#### Job Clusters
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

### Notebooks

**Magic Commands:**
```python
# SQL queries
%sql
SELECT COUNT(*) FROM customers WHERE created_date >= '2024-01-01'

# File system operations
%fs ls /mnt/data/

# Shell commands
%sh ls -la /tmp/

# Widgets for parameterization
dbutils.widgets.text("start_date", "2024-01-01", "Start Date")
dbutils.widgets.dropdown("environment", "dev", ["dev", "staging", "prod"], "Environment")

start_date = dbutils.widgets.get("start_date")
environment = dbutils.widgets.get("environment")
```

### Unity Catalog

**Three-Level Namespace:**
```sql
-- catalog.schema.table
SELECT * FROM production.sales.customers;
SELECT * FROM development.analytics.user_metrics;

-- Create catalog and schema
CREATE CATALOG IF NOT EXISTS production;
CREATE SCHEMA IF NOT EXISTS production.sales;

-- Grant permissions
GRANT USE CATALOG ON CATALOG production TO `data-engineers`;
GRANT USE SCHEMA ON SCHEMA production.sales TO `analysts`;
GRANT SELECT ON TABLE production.sales.customers TO `reporting-team`;
```

---

## 3. Delta Lake

### Key Features
- **ACID Transactions**: Ensures data consistency
- **Schema Evolution**: Handle schema changes gracefully
- **Time Travel**: Query historical versions of data
- **Upserts**: Merge operations for data updates
- **Streaming**: Real-time data ingestion and processing

### Creating Delta Tables
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

### Delta Operations
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

### Time Travel
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

### Medallion Architecture

#### Bronze Layer (Raw Data)
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

#### Silver Layer (Cleaned Data)
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

#### Gold Layer (Business Logic)
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

---

## 4. Performance Optimization

### Cluster Optimization
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

### Partitioning
```python
# Partition by date for time-series data
df.write.format("delta").partitionBy("date").mode("overwrite").save("/delta/events")

# Multi-level partitioning
df.write.format("delta").partitionBy("year", "month").mode("overwrite").save("/delta/sales")
```

### Z-Ordering
```sql
-- Optimize table layout for better query performance
OPTIMIZE customers ZORDER BY (customer_id, registration_date);

-- Auto-optimize
ALTER TABLE customers SET TBLPROPERTIES (
    'delta.autoOptimize.optimizeWrite' = 'true',
    'delta.autoOptimize.autoCompact' = 'true'
);
```

### Caching
```python
# Cache frequently accessed data
df.cache()
df.count()  # Trigger caching

# Persist with storage level
from pyspark import StorageLevel
df.persist(StorageLevel.MEMORY_AND_DISK_SER)
```

### Broadcast Joins
```python
from pyspark.sql.functions import broadcast

# Broadcast small dimension tables
large_df.join(broadcast(small_df), "key")
```

---

## 5. Security & Governance

### Access Control
```sql
-- Create service principal
CREATE SERVICE PRINCIPAL 'etl-service-principal';
GRANT MODIFY ON SCHEMA production.raw TO SERVICE PRINCIPAL 'etl-service-principal';

-- Row-level security
CREATE FUNCTION mask_pii(user_role STRING, sensitive_data STRING)
RETURNS STRING
LANGUAGE SQL
RETURN CASE 
    WHEN user_role = 'admin' THEN sensitive_data
    WHEN user_role = 'analyst' THEN CONCAT(LEFT(sensitive_data, 3), '***')
    ELSE '***'
END;
```

### Secrets Management
```python
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

### Data Lineage
```python
def track_data_lineage():
    """Implement custom data lineage tracking"""
    
    lineage_info = {
        "job_id": dbutils.widgets.get("job_id"),
        "notebook_path": dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get(),
        "timestamp": current_timestamp(),
        "user": dbutils.notebook.entry_point.getDbutils().notebook().getContext().userName().get()
    }
    
    # Track input sources
    input_sources = [
        {"path": "/delta/bronze/events", "type": "delta", "operation": "read"},
        {"path": "/delta/bronze/users", "type": "delta", "operation": "read"}
    ]
    
    # Track output targets
    output_targets = [
        {"path": "/delta/silver/user_events", "type": "delta", "operation": "write"}
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
    lineage_df.write.format("delta").mode("append").save("/delta/metadata/lineage")
```

---

## 6. Best Practices

### Cluster Management
```python
# Optimal cluster settings
cluster_config = {
    "cluster_name": "production-etl-cluster",
    "spark_version": "11.3.x-scala2.12",  # Use LTS versions
    "node_type_id": "i3.xlarge",  # Memory-optimized for data processing
    "driver_node_type_id": "i3.xlarge",
    "num_workers": 2,
    "autoscale": {
        "min_workers": 1,
        "max_workers": 8
    },
    "auto_termination_minutes": 30,  # Prevent idle costs
    "enable_elastic_disk": True
}
```

### Data Quality Framework
```python
def validate_data_quality(df, table_name, rules):
    """Generic data quality validation"""
    
    results = []
    total_records = df.count()
    
    for rule_name, rule_condition in rules.items():
        if rule_name == "null_check":
            for column in rule_condition:
                null_count = df.filter(col(column).isNull()).count()
                null_percentage = (null_count / total_records) * 100
                
                results.append({
                    "table": table_name,
                    "rule": f"null_check_{column}",
                    "passed": null_percentage < 5,  # < 5% nulls allowed
                    "value": null_percentage,
                    "threshold": 5
                })
        
        elif rule_name == "duplicate_check":
            duplicate_count = total_records - df.dropDuplicates(rule_condition).count()
            results.append({
                "table": table_name,
                "rule": "duplicate_check",
                "passed": duplicate_count == 0,
                "value": duplicate_count,
                "threshold": 0
            })
    
    return results
```

### Schema Evolution
```python
def handle_schema_evolution():
    """Implement schema evolution strategies"""
    
    # Enable schema evolution in Delta Lake
    spark.conf.set("spark.databricks.delta.schema.autoMerge.enabled", "true")
    
    # Write with merge schema
    df.write.format("delta") \
      .option("mergeSchema", "true") \
      .mode("append") \
      .save("/delta/evolving_table")
```

### Cost Optimization
```python
def optimize_costs():
    """Cost optimization strategies"""
    
    # Cluster auto-termination
    cluster_configs = {
        "interactive_clusters": {
            "auto_termination_minutes": 30,  # Short for development
            "enable_elastic_disk": True
        },
        "job_clusters": {
            "auto_termination_minutes": 0,   # Terminate immediately after job
            "spot_instances": True           # Use spot instances for cost savings
        }
    }
    
    return cluster_configs
```

---

## 7. Interview Questions

### Basic Level (1-8)

#### 1. What is Databricks and how does it differ from Apache Spark?
**Answer:**
Databricks is a unified analytics platform built on Apache Spark that provides:
- Managed Spark clusters with auto-scaling
- Collaborative notebooks with multiple language support
- Built-in data visualization and ML capabilities
- Delta Lake for reliable data lakes
- MLflow for ML lifecycle management

#### 2. Explain Delta Lake and its key features
**Answer:**
Delta Lake is an open-source storage layer that brings ACID transactions to Apache Spark and big data workloads.

Key features:
- **ACID Transactions**: Ensures data consistency
- **Schema Evolution**: Handle schema changes gracefully
- **Time Travel**: Query historical versions of data
- **Upserts**: Merge operations for data updates

#### 3. What are Databricks clusters and their types?
**Answer:**
- **All-Purpose Clusters**: Interactive analysis, shared across users
- **Job Clusters**: Automated workloads, terminated after job completion
- **SQL Warehouses**: Optimized for SQL queries and BI tools

#### 4. How do you mount external storage in Databricks?
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
```

#### 5. What is Unity Catalog in Databricks?
**Answer:**
Unity Catalog is a unified governance solution for data and AI assets across Databricks workspaces.

Features:
- Centralized access control
- Data lineage tracking
- Data discovery and search
- Cross-workspace data sharing

#### 6. How do you handle secrets in Databricks?
**Answer:**
```python
# Access secrets in notebook
password = dbutils.secrets.get(scope="my-scope", key="db-password")

# Use in connection
connection_properties = {
    "user": "username",
    "password": password,
    "driver": "org.postgresql.Driver"
}
```

#### 7. What are Databricks workflows and how do you create them?
**Answer:**
Databricks Workflows (formerly Jobs) orchestrate data processing tasks.

```python
job_config = {
    "name": "ETL Pipeline",
    "tasks": [
        {
            "task_key": "extract",
            "notebook_task": {
                "notebook_path": "/Shared/etl/extract",
                "base_parameters": {"date": "2024-01-01"}
            }
        }
    ]
}
```

#### 8. How do you optimize Databricks performance?
**Answer:**
```python
# Enable adaptive query execution
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")

# Cache frequently used data
df.cache()

# Use Delta Lake optimizations
spark.sql("OPTIMIZE delta.`/path/to/table`")
spark.sql("OPTIMIZE delta.`/path/to/table` ZORDER BY (column1, column2)")
```

### Intermediate Level (9-16)

#### 9. Implement a medallion architecture in Databricks
**Answer:**
```python
# Bronze Layer - Raw data ingestion
def ingest_bronze_data():
    raw_df = spark.read.format("json").load("/mnt/raw-data/")
    
    # Add metadata columns
    bronze_df = raw_df.withColumn("ingestion_timestamp", current_timestamp()) \
                     .withColumn("source_file", input_file_name())
    
    # Write to Delta Lake
    bronze_df.write.format("delta").mode("append").save("/delta/bronze/events")

# Silver Layer - Cleaned and validated data
def process_silver_data():
    bronze_df = spark.read.format("delta").load("/delta/bronze/events")
    
    # Data cleaning and validation
    silver_df = bronze_df.filter(col("user_id").isNotNull()) \
                         .withColumn("event_date", to_date(col("timestamp"))) \
                         .dropDuplicates(["user_id", "event_id"])
    
    # Write to silver layer
    silver_df.write.format("delta").mode("overwrite").save("/delta/silver/events")

# Gold Layer - Business aggregations
def create_gold_aggregations():
    silver_df = spark.read.format("delta").load("/delta/silver/events")
    
    # Business metrics
    daily_metrics = silver_df.groupBy("event_date", "event_type") \
                            .agg(count("*").alias("event_count"),
                                 countDistinct("user_id").alias("unique_users"))
    
    daily_metrics.write.format("delta").mode("overwrite").save("/delta/gold/daily_metrics")
```

#### 10. How do you implement Change Data Capture (CDC) in Databricks?
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
    updates = cdc_df.filter(col("operation") == "UPDATE")
    
    # Apply changes
    if updates.count() > 0:
        target_table.alias("target").merge(
            updates.alias("updates"),
            "target.id = updates.id"
        ).whenMatchedUpdateAll().execute()
```

#### 11. How do you handle streaming data in Databricks?
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
        .option("checkpointLocation", "/delta/checkpoints/events") \
        .trigger(processingTime="10 seconds") \
        .start("/delta/streaming/events")
    
    return query
```

#### 12. Implement data quality checks in Databricks
**Answer:**
```python
def data_quality_checks(df, table_name):
    """Comprehensive data quality validation"""
    
    results = []
    
    # Null checks
    total_rows = df.count()
    for column in df.columns:
        null_count = df.filter(col(column).isNull()).count()
        null_percentage = (null_count / total_rows) * 100
        
        results.append({
            "table": table_name,
            "check": f"null_check_{column}",
            "passed": null_percentage < 5,  # Less than 5% nulls
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
    
    # Convert to DataFrame for analysis
    results_df = spark.createDataFrame(results)
    
    # Log results to Delta Lake
    results_df.withColumn("check_timestamp", current_timestamp()) \
              .write.format("delta").mode("append").save("/delta/data_quality/results")
    
    return results_df
```

### Advanced Level (17-20)

#### 17. Implement a real-time ML feature store in Databricks
**Answer:**
```python
from databricks.feature_store import FeatureStoreClient

def create_feature_store():
    """Create and manage ML feature store"""
    
    fs = FeatureStoreClient()
    
    # Calculate user features
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
    
    # Create feature table
    fs.create_table(
        name="ml.user_features",
        primary_keys=["user_id"],
        df=user_features,
        description="User behavioral features for ML models"
    )
```

#### 18. Implement advanced Delta Lake optimization strategies
**Answer:**
```python
def advanced_delta_optimization():
    """Advanced Delta Lake optimization techniques"""
    
    # Auto-optimize with optimized writes
    spark.conf.set("spark.databricks.delta.optimizeWrite.enabled", "true")
    spark.conf.set("spark.databricks.delta.autoCompact.enabled", "true")
    
    # Liquid clustering (Databricks Runtime 13.3+)
    spark.sql("""
        CREATE TABLE clustered_events (
            user_id BIGINT,
            event_type STRING,
            event_date DATE,
            event_data STRING
        ) USING DELTA
        CLUSTER BY (event_date, event_type)
    """)
    
    # Bloom filter optimization
    def create_bloom_filters(table_path, bloom_columns):
        """Create bloom filters for better data skipping"""
        
        for column in bloom_columns:
            spark.sql(f"""
                ALTER TABLE delta.`{table_path}` 
                SET TBLPROPERTIES (
                    'delta.bloomFilter.{column}.enabled' = 'true',
                    'delta.bloomFilter.{column}.fpp' = '0.1'
                )
            """)
```

#### 19. Implement multi-cloud data architecture with Databricks
**Answer:**
```python
def multi_cloud_architecture():
    """Implement multi-cloud data architecture"""
    
    # AWS configuration
    def setup_aws_integration():
        # Mount S3 with cross-account access
        dbutils.fs.mount(
            source="s3a://cross-account-bucket/data",
            mount_point="/mnt/aws-data",
            extra_configs={
                "fs.s3a.aws.credentials.provider": "org.apache.hadoop.fs.s3a.auth.AssumedRoleCredentialProvider",
                "fs.s3a.assumed.role.arn": "arn:aws:iam::account:role/CrossAccountRole"
            }
        )
        
        return spark.read.format("jdbc") \
            .option("url", "jdbc:postgresql://aws-rds.region.rds.amazonaws.com:5432/db") \
            .option("dbtable", "customers") \
            .load()
    
    # Cross-cloud data synchronization
    def sync_cross_cloud_data():
        aws_data = setup_aws_integration()
        
        # Write to central Delta Lake
        aws_data.write.format("delta") \
            .mode("overwrite") \
            .save("/mnt/unified/multi_cloud_data")
```

#### 20. Implement advanced security and governance in Databricks
**Answer:**
```python
def implement_advanced_security():
    """Advanced security and governance implementation"""
    
    # Row-level security with Unity Catalog
    def setup_row_level_security():
        spark.sql("""
            CREATE FUNCTION mask_pii(user_role STRING, sensitive_data STRING)
            RETURNS STRING
            LANGUAGE SQL
            RETURN CASE 
                WHEN user_role = 'admin' THEN sensitive_data
                WHEN user_role = 'analyst' THEN CONCAT(LEFT(sensitive_data, 3), '***')
                ELSE '***'
            END
        """)
        
        # Create view with row-level security
        spark.sql("""
            CREATE VIEW secure_customers AS
            SELECT 
                customer_id,
                mask_pii(current_user(), email) as email,
                mask_pii(current_user(), phone) as phone,
                name,
                created_date
            FROM customers
            WHERE 
                CASE 
                    WHEN is_member('data_engineers') THEN TRUE
                    WHEN is_member('analysts') AND region = 'US' THEN TRUE
                    ELSE FALSE
                END
        """)
    
    # Audit logging
    def setup_audit_logging():
        audit_info = {
            "user": dbutils.notebook.entry_point.getDbutils().notebook().getContext().userName().get(),
            "notebook": dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get(),
            "timestamp": current_timestamp(),
            "action": "data_access",
            "resource": "/delta/sensitive/customer_data"
        }
        
        audit_df = spark.createDataFrame([audit_info])
        audit_df.write.format("delta").mode("append").save("/delta/audit/access_logs")
```

---

## 8. Advanced Topics

### Streaming Processing
```python
# Stream-Stream Joins
def stream_stream_joins():
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
    
    return joined
```

### MLflow Integration
```python
import mlflow
import mlflow.sklearn

# Experiment Tracking
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

# Model Registry
model_uri = f"runs:/{run_id}/random_forest_model"
mlflow.register_model(model_uri, "customer_churn_model")
```

### Monitoring and Troubleshooting
```python
def monitor_job_execution():
    """Custom job monitoring and alerting"""
    
    job_metrics = {
        "job_id": dbutils.widgets.get("job_id"),
        "start_time": datetime.now(),
        "cluster_id": spark.conf.get("spark.databricks.clusterUsageTags.clusterId"),
        "records_processed": 0,
        "status": "running"
    }
    
    try:
        # Your ETL logic here
        df = spark.read.format("delta").load("/delta/source")
        processed_df = df.transform(your_transformation_logic)
        processed_df.write.format("delta").mode("overwrite").save("/delta/target")
        
        job_metrics["records_processed"] = processed_df.count()
        job_metrics["status"] = "success"
        
    except Exception as e:
        job_metrics["status"] = "failed"
        job_metrics["error_message"] = str(e)
        raise
    
    finally:
        job_metrics["end_time"] = datetime.now()
        
        # Log to monitoring table
        metrics_df = spark.createDataFrame([job_metrics])
        metrics_df.write.format("delta").mode("append").save("/delta/monitoring/job_metrics")
```

---

## 🔗 Quick Reference Links

- **Official Documentation**: [docs.databricks.com](https://docs.databricks.com)
- **Delta Lake**: [delta.io](https://delta.io)
- **MLflow**: [mlflow.org](https://mlflow.org)
- **Unity Catalog**: [docs.databricks.com/unity-catalog](https://docs.databricks.com/unity-catalog)
- **Community**: [community.databricks.com](https://community.databricks.com)

---

**Remember**: Always test configurations in development environments before applying to production workloads. Regularly review and update practices as Databricks continues to evolve.