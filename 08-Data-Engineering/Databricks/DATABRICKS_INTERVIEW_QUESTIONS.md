# Databricks Interview Questions for Data Engineering

## Basic Level Questions (1-8)

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

## Intermediate Level Questions (9-16)

### 9. Implement a medallion architecture in Databricks
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

### 10. How do you implement Change Data Capture (CDC) in Databricks?
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

### 11. How do you handle streaming data in Databricks?
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

# Stream processing with watermarking
def process_with_watermark():
    streaming_df = spark.readStream.format("delta").load("/delta/streaming/events")
    
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
        .option("checkpointLocation", "/delta/checkpoints/windowed") \
        .start("/delta/aggregated/windowed_counts")
    
    return query
```

### 12. Implement data quality checks in Databricks
**Answer:**
```python
from pyspark.sql.functions import *

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
    
    # Convert to DataFrame for analysis
    results_df = spark.createDataFrame(results)
    
    # Log results to Delta Lake
    results_df.withColumn("check_timestamp", current_timestamp()) \
              .write.format("delta").mode("append").save("/delta/data_quality/results")
    
    return results_df

# Usage
df = spark.read.format("delta").load("/delta/silver/customers")
quality_results = data_quality_checks(df, "customers")
quality_results.show()
```

### 13. How do you implement slowly changing dimensions (SCD) in Databricks?
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
source_df = spark.read.format("delta").load("/delta/staging/customers")
implement_scd_type2(
    source_df, 
    "/delta/dimensions/dim_customer",
    "customer_id",
    ["name", "email", "address"]
)
```

### 14. How do you monitor and troubleshoot Databricks jobs?
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
        df = spark.read.format("delta").load("/delta/source")
        processed_df = df.transform(your_transformation_logic)
        processed_df.write.format("delta").mode("overwrite").save("/delta/target")
        
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
        metrics_df.write.format("delta").mode("append").save("/delta/monitoring/job_metrics")

# Performance monitoring
def analyze_query_performance():
    """Analyze Spark query performance"""
    
    # Enable query execution metrics
    spark.conf.set("spark.sql.queryExecutionListeners", 
                   "org.apache.spark.sql.util.QueryExecutionMetricsListener")
    
    # Query with explain plan
    df = spark.sql("SELECT * FROM delta.`/delta/large_table` WHERE date >= '2024-01-01'")
    df.explain(True)  # Show physical plan
    
    # Analyze partition pruning
    spark.sql("DESCRIBE DETAIL delta.`/delta/large_table`").show()
    
    # Check file sizes and optimization opportunities
    spark.sql("DESCRIBE HISTORY delta.`/delta/large_table`").show()
```

### 15. How do you implement data lineage tracking in Databricks?
**Answer:**
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

# Unity Catalog lineage (automatic)
def query_unity_catalog_lineage():
    """Query built-in Unity Catalog lineage"""
    
    # Get table lineage
    lineage_query = """
    SELECT 
        source_table_full_name,
        target_table_full_name,
        created_at,
        created_by
    FROM system.access.table_lineage
    WHERE target_table_full_name = 'catalog.schema.table'
    """
    
    lineage_df = spark.sql(lineage_query)
    return lineage_df
```

### 16. How do you handle schema evolution in Databricks?
**Answer:**
```python
def handle_schema_evolution():
    """Implement schema evolution strategies"""
    
    # Enable schema evolution in Delta Lake
    spark.conf.set("spark.databricks.delta.schema.autoMerge.enabled", "true")
    
    # Read with schema evolution
    df = spark.read.format("delta").load("/delta/evolving_table")
    
    # Add new columns safely
    if "new_column" not in df.columns:
        df = df.withColumn("new_column", lit(None).cast("string"))
    
    # Handle column type changes
    def safe_cast_column(df, column_name, target_type):
        try:
            return df.withColumn(column_name, col(column_name).cast(target_type))
        except Exception as e:
            print(f"Failed to cast {column_name} to {target_type}: {e}")
            return df
    
    # Schema validation before write
    def validate_schema(df, expected_schema):
        current_schema = df.schema
        
        for field in expected_schema.fields:
            if field.name not in [f.name for f in current_schema.fields]:
                df = df.withColumn(field.name, lit(None).cast(field.dataType))
        
        return df
    
    # Write with merge schema
    df.write.format("delta") \
      .option("mergeSchema", "true") \
      .mode("append") \
      .save("/delta/evolving_table")

# Schema registry integration
def register_schema():
    """Register and version schemas"""
    
    schema_info = {
        "table_name": "user_events",
        "schema_version": "v2",
        "schema_json": df.schema.json(),
        "created_at": current_timestamp(),
        "created_by": dbutils.notebook.entry_point.getDbutils().notebook().getContext().userName().get()
    }
    
    schema_df = spark.createDataFrame([schema_info])
    schema_df.write.format("delta").mode("append").save("/delta/metadata/schemas")
```

## Advanced Level Questions (17-20)

### 17. Implement a real-time ML feature store in Databricks
**Answer:**
```python
from databricks.feature_store import FeatureStoreClient

def create_feature_store():
    """Create and manage ML feature store"""
    
    fs = FeatureStoreClient()
    
    # Create feature table
    def create_user_features():
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
    
    # Update features in real-time
    def update_streaming_features():
        streaming_df = spark.readStream.format("delta").load("/delta/streaming/events")
        
        # Calculate incremental features
        incremental_features = streaming_df.groupBy("user_id") \
            .agg(count("*").alias("event_count"),
                 max("timestamp").alias("last_activity"))
        
        # Write to feature store
        query = fs.write_table(
            name="ml.user_features",
            df=incremental_features,
            mode="merge"
        )
        
        return query
    
    # Feature serving for online inference
    def serve_features_online():
        # Get features for model inference
        feature_lookups = [
            FeatureLookup(
                table_name="ml.user_features",
                lookup_key="user_id"
            )
        ]
        
        # Create training set
        training_set = fs.create_training_set(
            df=spark.table("ml.training_labels"),
            feature_lookups=feature_lookups,
            label="target",
            exclude_columns=["feature_timestamp"]
        )
        
        return training_set.load_df()
```

### 18. Implement advanced Delta Lake optimization strategies
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
    
    # Predictive optimization
    spark.sql("ALTER TABLE delta.`/delta/large_table` SET TBLPROPERTIES ('delta.autoOptimize.optimizeWrite' = 'true')")
    
    # Custom optimization strategy
    def optimize_table_partitions(table_path, partition_columns):
        """Custom partition optimization"""
        
        # Analyze partition distribution
        df = spark.read.format("delta").load(table_path)
        partition_stats = df.groupBy(*partition_columns).count().collect()
        
        # Identify skewed partitions
        avg_count = sum(row['count'] for row in partition_stats) / len(partition_stats)
        skewed_partitions = [row for row in partition_stats if row['count'] > avg_count * 2]
        
        if skewed_partitions:
            print(f"Found {len(skewed_partitions)} skewed partitions")
            
            # Repartition skewed data
            for partition in skewed_partitions:
                partition_filter = " AND ".join([f"{col} = '{partition[col]}'" for col in partition_columns])
                
                partition_df = df.filter(partition_filter)
                optimal_partitions = max(1, partition_df.count() // 1000000)  # 1M records per partition
                
                repartitioned_df = partition_df.repartition(optimal_partitions)
                
                # Write back optimized partition
                repartitioned_df.write.format("delta") \
                    .mode("overwrite") \
                    .option("replaceWhere", partition_filter) \
                    .save(table_path)
    
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
    
    # Usage
    optimize_table_partitions("/delta/events", ["event_date", "event_type"])
    create_bloom_filters("/delta/events", ["user_id", "session_id"])
```

### 19. Implement multi-cloud data architecture with Databricks
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
                "fs.s3a.assumed.role.arn": "arn:aws:iam::account:role/CrossAccountRole",
                "fs.s3a.assumed.role.session.name": "databricks-session"
            }
        )
        
        # Read from AWS RDS
        aws_df = spark.read.format("jdbc") \
            .option("url", "jdbc:postgresql://aws-rds.region.rds.amazonaws.com:5432/db") \
            .option("dbtable", "customers") \
            .option("user", dbutils.secrets.get("aws", "rds-user")) \
            .option("password", dbutils.secrets.get("aws", "rds-password")) \
            .load()
        
        return aws_df
    
    # Azure configuration
    def setup_azure_integration():
        # Mount Azure Data Lake
        dbutils.fs.mount(
            source="abfss://container@storage.dfs.core.windows.net/",
            mount_point="/mnt/azure-data",
            extra_configs={
                "fs.azure.account.auth.type": "OAuth",
                "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
                "fs.azure.account.oauth2.client.id": dbutils.secrets.get("azure", "client-id"),
                "fs.azure.account.oauth2.client.secret": dbutils.secrets.get("azure", "client-secret"),
                "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/tenant/oauth2/token"
            }
        )
        
        # Read from Azure SQL
        azure_df = spark.read.format("jdbc") \
            .option("url", "jdbc:sqlserver://server.database.windows.net:1433;database=db") \
            .option("dbtable", "orders") \
            .option("user", dbutils.secrets.get("azure", "sql-user")) \
            .option("password", dbutils.secrets.get("azure", "sql-password")) \
            .load()
        
        return azure_df
    
    # GCP configuration
    def setup_gcp_integration():
        # Configure GCS access
        spark.conf.set("fs.gs.auth.service.account.enable", "true")
        spark.conf.set("fs.gs.auth.service.account.json.keyfile", "/path/to/keyfile.json")
        
        # Read from BigQuery
        gcp_df = spark.read.format("bigquery") \
            .option("table", "project.dataset.table") \
            .option("credentialsFile", "/path/to/keyfile.json") \
            .load()
        
        return gcp_df
    
    # Cross-cloud data synchronization
    def sync_cross_cloud_data():
        aws_data = setup_aws_integration()
        azure_data = setup_azure_integration()
        gcp_data = setup_gcp_integration()
        
        # Merge data from multiple clouds
        unified_data = aws_data.unionByName(azure_data).unionByName(gcp_data)
        
        # Write to central Delta Lake
        unified_data.write.format("delta") \
            .mode("overwrite") \
            .save("/mnt/unified/multi_cloud_data")
        
        return unified_data
```

### 20. Implement advanced security and governance in Databricks
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
    
    # Column-level encryption
    def implement_column_encryption():
        from cryptography.fernet import Fernet
        
        # Generate encryption key (store in Key Vault)
        key = dbutils.secrets.get("encryption", "column-key")
        cipher = Fernet(key.encode())
        
        def encrypt_column(value):
            if value is None:
                return None
            return cipher.encrypt(value.encode()).decode()
        
        def decrypt_column(encrypted_value):
            if encrypted_value is None:
                return None
            return cipher.decrypt(encrypted_value.encode()).decode()
        
        # Register UDFs
        encrypt_udf = udf(encrypt_column, StringType())
        decrypt_udf = udf(decrypt_column, StringType())
        
        # Encrypt sensitive data
        encrypted_df = df.withColumn("encrypted_ssn", encrypt_udf(col("ssn"))) \
                        .drop("ssn")
        
        return encrypted_df
    
    # Audit logging
    def setup_audit_logging():
        audit_info = {
            "user": dbutils.notebook.entry_point.getDbutils().notebook().getContext().userName().get(),
            "notebook": dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get(),
            "cluster_id": spark.conf.get("spark.databricks.clusterUsageTags.clusterId"),
            "timestamp": current_timestamp(),
            "action": "data_access",
            "resource": "/delta/sensitive/customer_data"
        }
        
        audit_df = spark.createDataFrame([audit_info])
        audit_df.write.format("delta").mode("append").save("/delta/audit/access_logs")
    
    # Data classification and tagging
    def classify_sensitive_data():
        # Scan for PII patterns
        pii_patterns = {
            "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "ssn": r"\d{3}-\d{2}-\d{4}",
            "phone": r"\d{3}-\d{3}-\d{4}",
            "credit_card": r"\d{4}-\d{4}-\d{4}-\d{4}"
        }
        
        classification_results = []
        
        for column in df.columns:
            sample_data = df.select(column).limit(1000).collect()
            
            for pii_type, pattern in pii_patterns.items():
                matches = sum(1 for row in sample_data if row[column] and re.match(pattern, str(row[column])))
                
                if matches > len(sample_data) * 0.8:  # 80% match threshold
                    classification_results.append({
                        "table": "customers",
                        "column": column,
                        "classification": pii_type,
                        "confidence": matches / len(sample_data),
                        "timestamp": current_timestamp()
                    })
        
        # Store classification results
        classification_df = spark.createDataFrame(classification_results)
        classification_df.write.format("delta").mode("append").save("/delta/governance/data_classification")
        
        return classification_results
```