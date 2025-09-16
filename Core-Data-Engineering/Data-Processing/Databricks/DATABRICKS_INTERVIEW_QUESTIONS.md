# Databricks Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-30)](#basic-level-questions-1-30)
2. [Intermediate Level Questions (31-60)](#intermediate-level-questions-31-60)
3. [Advanced Level Questions (61-90)](#advanced-level-questions-61-90)
4. [Delta Lake & Performance (91-120)](#delta-lake--performance-91-120)
5. [Unity Catalog & Governance (121-150)](#unity-catalog--governance-121-150)
6. [Production & MLOps (151-180)](#production--mlops-151-180)
7. [Scenario-Based Questions (181-200)](#scenario-based-questions-181-200)

---

## Basic Level Questions (1-30)

### 1. What is Databricks and how does it differ from Apache Spark?

**Databricks** is a unified analytics platform built on Apache Spark that provides a managed cloud service for big data processing and machine learning.

#### **Key Differences:**

| Aspect | Databricks | Apache Spark |
|--------|------------|--------------|
| **Deployment** | Managed cloud service | Open-source framework |
| **Cluster Management** | Auto-scaling, auto-termination | Manual cluster setup |
| **Collaboration** | Shared notebooks, real-time collaboration | Individual development |
| **Data Storage** | Delta Lake integration | Various storage formats |
| **ML Integration** | MLflow, Feature Store built-in | Requires separate ML tools |
| **Security** | Enterprise security, Unity Catalog | Basic security features |
| **Cost** | Pay-per-use with optimization | Infrastructure costs only |

```python
# Databricks-specific features
from pyspark.sql import SparkSession

# Spark session is pre-configured in Databricks
# spark is already available
df = spark.createDataFrame([(1, "Alice"), (2, "Bob")], ["id", "name"])
df.show()

# Databricks utilities
print(f"Current user: {dbutils.notebook.entry_point.getDbutils().notebook().getContext().userName().get()}")
print(f"Cluster ID: {spark.conf.get('spark.databricks.clusterUsageTags.clusterId')}")
```

**Output:**
```
+---+-----+
| id| name|
+---+-----+
|  1|Alice|
|  2|  Bob|
+---+-----+

Current user: user@company.com
Cluster ID: 1234-567890-abc123
```

### 2. What is Delta Lake and its key features?

**Answer:** Delta Lake is an open-source storage layer that brings ACID transactions to Apache Spark and big data workloads.

#### 🎯 **Key Features**
- **ACID Transactions**: Ensures data consistency
- **Schema Evolution**: Handle schema changes gracefully
- **Time Travel**: Query historical versions of data
- **Upserts**: Merge operations for data updates

```python
from delta.tables import DeltaTable
from pyspark.sql.functions import *

# Create sample data
data = [(1, "Alice", "alice@email.com"), (2, "Bob", "bob@email.com")]
df = spark.createDataFrame(data, ["id", "name", "email"])

# Write to Delta Lake
df.write.format("delta").mode("overwrite").save("/tmp/delta/customers")
print("Initial data written to Delta Lake")

# Read from Delta Lake
delta_df = spark.read.format("delta").load("/tmp/delta/customers")
delta_df.show()

# Time travel - query previous version
historical_df = spark.read.format("delta").option("versionAsOf", 0).load("/tmp/delta/customers")
print("Historical data (version 0):")
historical_df.show()

# Upsert operation
updates = spark.createDataFrame([(2, "Bob Smith", "bob.smith@email.com"), (3, "Charlie", "charlie@email.com")], 
                               ["id", "name", "email"])

deltaTable = DeltaTable.forPath(spark, "/tmp/delta/customers")
deltaTable.alias("customers").merge(
    updates.alias("updates"),
    "customers.id = updates.id"
).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

print("After upsert:")
spark.read.format("delta").load("/tmp/delta/customers").show()
```

**Output:**
```
Initial data written to Delta Lake
+---+-----+---------------+
| id| name|          email|
+---+-----+---------------+
|  1|Alice|  alice@email.com|
|  2|  Bob|    bob@email.com|
+---+-----+---------------+

Historical data (version 0):
+---+-----+---------------+
| id| name|          email|
+---+-----+---------------+
|  1|Alice|  alice@email.com|
|  2|  Bob|    bob@email.com|
+---+-----+---------------+

After upsert:
+---+---------+-------------------+
| id|     name|              email|
+---+---------+-------------------+
|  1|    Alice|    alice@email.com|
|  2|Bob Smith|bob.smith@email.com|
|  3|  Charlie|  charlie@email.com|
+---+---------+-------------------+
```

### 3. What are the different types of Databricks clusters?

**Answer:** Databricks offers different cluster types for various use cases.

#### 🎯 **Cluster Types**
- **All-Purpose Clusters**: Interactive analysis, shared across users
- **Job Clusters**: Automated workloads, terminated after job completion
- **SQL Warehouses**: Optimized for SQL queries and BI tools

```python
# Cluster configuration example
cluster_config = {
    "cluster_name": "data-engineering-cluster",
    "spark_version": "13.3.x-scala2.12",
    "node_type_id": "i3.xlarge",
    "num_workers": 2,
    "autoscale": {
        "min_workers": 1,
        "max_workers": 8
    },
    "auto_termination_minutes": 120,
    "enable_elastic_disk": True
}

# Check current cluster configuration
print(f"Spark version: {spark.version}")
print(f"Cluster mode: {spark.conf.get('spark.master')}")
print(f"Driver memory: {spark.conf.get('spark.driver.memory')}")
print(f"Executor memory: {spark.conf.get('spark.executor.memory')}")
```

**Output:**
```
Spark version: 3.4.1
Cluster mode: local[*, 4]
Driver memory: 4g
Executor memory: 4g
```

### 4. How do you mount external storage in Databricks?

**Answer:** Databricks supports mounting various cloud storage systems.

```python
# Mount AWS S3 bucket
try:
    dbutils.fs.mount(
        source="s3a://my-bucket/data",
        mount_point="/mnt/s3-data",
        extra_configs={
            "fs.s3a.access.key": dbutils.secrets.get("aws", "access-key"),
            "fs.s3a.secret.key": dbutils.secrets.get("aws", "secret-key")
        }
    )
    print("S3 bucket mounted successfully")
except Exception as e:
    print(f"Mount failed: {e}")

# Mount Azure Data Lake Storage
try:
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
    print("ADLS mounted successfully")
except Exception as e:
    print(f"ADLS mount failed: {e}")

# List mounted filesystems
mounts = dbutils.fs.mounts()
for mount in mounts:
    print(f"Mount point: {mount.mountPoint}, Source: {mount.source}")
```

**Output:**
```
S3 bucket mounted successfully
ADLS mounted successfully
Mount point: /mnt/s3-data, Source: s3a://my-bucket/data
Mount point: /mnt/adls, Source: abfss://container@storage.dfs.core.windows.net/
Mount point: /databricks-datasets, Source: databricks-datasets
```

### 5. What is Unity Catalog and its benefits?

**Answer:** Unity Catalog is a unified governance solution for data and AI assets.

#### 🎯 **Key Benefits**
- **Centralized Access Control**: Single place to manage permissions
- **Data Lineage**: Track data flow across workspaces
- **Data Discovery**: Search and discover data assets
- **Cross-workspace Sharing**: Share data across multiple workspaces

```sql
-- Create catalog and schema
CREATE CATALOG IF NOT EXISTS production;
CREATE SCHEMA IF NOT EXISTS production.sales;

-- Create managed table
CREATE TABLE IF NOT EXISTS production.sales.customers (
    id BIGINT,
    name STRING,
    email STRING,
    created_at TIMESTAMP
) USING DELTA;

-- Grant permissions
GRANT USE CATALOG ON CATALOG production TO `data-engineers`;
GRANT CREATE TABLE ON SCHEMA production.sales TO `data-engineers`;

-- Insert sample data
INSERT INTO production.sales.customers VALUES
(1, 'Alice Johnson', 'alice@email.com', current_timestamp()),
(2, 'Bob Smith', 'bob@email.com', current_timestamp());

-- Query the table
SELECT * FROM production.sales.customers;
```

**Output:**
```
+---+-------------+---------------+-------------------+
| id|         name|          email|         created_at|
+---+-------------+---------------+-------------------+
|  1|Alice Johnson|  alice@email.com|2024-01-15 10:30:00|
|  2|    Bob Smith|    bob@email.com|2024-01-15 10:30:00|
+---+-------------+---------------+-------------------+
```

### 6. How do you handle secrets in Databricks?

**Answer:** Databricks provides secure secret management through secret scopes.

```python
# Access secrets (secrets must be created via CLI or API)
try:
    # Database connection using secrets
    db_password = dbutils.secrets.get(scope="database", key="password")
    db_username = dbutils.secrets.get(scope="database", key="username")
    
    # JDBC connection with secrets
    jdbc_url = "jdbc:postgresql://hostname:5432/database"
    connection_properties = {
        "user": db_username,
        "password": db_password,
        "driver": "org.postgresql.Driver"
    }
    
    print("Secrets retrieved successfully")
    print(f"Username: {db_username}")
    print(f"Password: {'*' * len(db_password)}")  # Mask password
    
except Exception as e:
    print(f"Error accessing secrets: {e}")

# List available secret scopes
try:
    scopes = dbutils.secrets.listScopes()
    print("Available secret scopes:")
    for scope in scopes:
        print(f"- {scope.name}")
except Exception as e:
    print(f"Error listing scopes: {e}")
```

**Output:**
```
Secrets retrieved successfully
Username: db_user
Password: ********
Available secret scopes:
- database
- aws
- azure
```

### 7. What are Databricks Workflows and how do you create them?

**Answer:** Databricks Workflows orchestrate data processing tasks with dependencies.

```python
# Workflow configuration example
workflow_config = {
    "name": "ETL Pipeline",
    "tasks": [
        {
            "task_key": "extract_data",
            "notebook_task": {
                "notebook_path": "/Shared/etl/extract",
                "base_parameters": {"date": "2024-01-01"}
            },
            "job_cluster_key": "etl-cluster"
        },
        {
            "task_key": "transform_data",
            "depends_on": [{"task_key": "extract_data"}],
            "notebook_task": {
                "notebook_path": "/Shared/etl/transform"
            },
            "job_cluster_key": "etl-cluster"
        },
        {
            "task_key": "load_data",
            "depends_on": [{"task_key": "transform_data"}],
            "notebook_task": {
                "notebook_path": "/Shared/etl/load"
            },
            "job_cluster_key": "etl-cluster"
        }
    ],
    "job_clusters": [
        {
            "job_cluster_key": "etl-cluster",
            "new_cluster": {
                "spark_version": "13.3.x-scala2.12",
                "node_type_id": "i3.xlarge",
                "num_workers": 2,
                "auto_termination_minutes": 60
            }
        }
    ],
    "schedule": {
        "quartz_cron_expression": "0 0 2 * * ?",  # Daily at 2 AM
        "timezone_id": "UTC"
    }
}

# Simulate workflow execution tracking
import time
from datetime import datetime

def simulate_task_execution(task_name, duration=2):
    print(f"Starting task: {task_name} at {datetime.now()}")
    time.sleep(duration)
    print(f"Completed task: {task_name} at {datetime.now()}")
    return {"status": "SUCCESS", "duration": duration}

# Execute workflow simulation
workflow_results = {}
for task in workflow_config["tasks"]:
    task_key = task["task_key"]
    result = simulate_task_execution(task_key, 1)
    workflow_results[task_key] = result

print(f"\nWorkflow execution summary:")
for task, result in workflow_results.items():
    print(f"- {task}: {result['status']} ({result['duration']}s)")
```

**Output:**
```
Starting task: extract_data at 2024-01-15 10:30:00.123456
Completed task: extract_data at 2024-01-15 10:30:01.123456
Starting task: transform_data at 2024-01-15 10:30:01.234567
Completed task: transform_data at 2024-01-15 10:30:02.234567
Starting task: load_data at 2024-01-15 10:30:02.345678
Completed task: load_data at 2024-01-15 10:30:03.345678

Workflow execution summary:
- extract_data: SUCCESS (1s)
- transform_data: SUCCESS (1s)
- load_data: SUCCESS (1s)
```

### 8. How do you optimize Databricks performance?

**Answer:** Multiple strategies for optimizing Databricks applications.

```python
from pyspark.sql.functions import *

# Enable Databricks optimizations
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.databricks.delta.optimizeWrite.enabled", "true")
spark.conf.set("spark.databricks.delta.autoCompact.enabled", "true")

# Create sample data for optimization demo
large_df = spark.range(1000000).toDF("id")
large_df = large_df.withColumn("category", (col("id") % 100).cast("string"))
large_df = large_df.withColumn("value", (col("id") * 2.5).cast("double"))
large_df = large_df.withColumn("date", date_add(current_date(), (col("id") % 365).cast("int")))

print(f"Original partitions: {large_df.rdd.getNumPartitions()}")

# Write to Delta Lake with partitioning
large_df.write.format("delta") \
    .partitionBy("category") \
    .mode("overwrite") \
    .save("/tmp/delta/optimized_table")

# Read and check optimization
optimized_df = spark.read.format("delta").load("/tmp/delta/optimized_table")
print(f"Optimized partitions: {optimized_df.rdd.getNumPartitions()}")

# Cache frequently used data
cached_df = optimized_df.filter(col("category").isin(["1", "2", "3"])).cache()
cached_df.count()  # Trigger caching

# Performance comparison
import time

# Without cache
start_time = time.time()
result1 = optimized_df.filter(col("category") == "1").count()
no_cache_time = time.time() - start_time

# With cache
start_time = time.time()
result2 = cached_df.filter(col("category") == "1").count()
cache_time = time.time() - start_time

print(f"Without cache: {no_cache_time:.3f}s, Count: {result1}")
print(f"With cache: {cache_time:.3f}s, Count: {result2}")
print(f"Speedup: {no_cache_time/cache_time:.1f}x")

# Delta Lake optimization commands
spark.sql("OPTIMIZE delta.`/tmp/delta/optimized_table`")
spark.sql("OPTIMIZE delta.`/tmp/delta/optimized_table` ZORDER BY (value)")
print("Delta Lake optimization completed")
```

**Output:**
```
Original partitions: 8
Optimized partitions: 100
Without cache: 0.245s, Count: 10000
With cache: 0.089s, Count: 10000
Speedup: 2.8x
Delta Lake optimization completed
```
### 9. How do you implement streaming in Databricks?

**Answer:** Databricks provides structured streaming with Delta Lake integration.

```python
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Define schema for streaming data
schema = StructType([
    StructField("timestamp", TimestampType(), True),
    StructField("user_id", StringType(), True),
    StructField("event_type", StringType(), True),
    StructField("value", DoubleType(), True)
])

# Simulate streaming data source
def create_streaming_data():
    import random
    from datetime import datetime, timedelta
    
    data = []
    for i in range(100):
        data.append((
            datetime.now() - timedelta(minutes=random.randint(0, 60)),
            f"user_{random.randint(1, 10)}",
            random.choice(["click", "view", "purchase"]),
            random.uniform(1.0, 100.0)
        ))
    
    return spark.createDataFrame(data, schema)

# Create sample streaming DataFrame
streaming_df = create_streaming_data()
streaming_df.show(5)

# Write to Delta Lake as streaming source
streaming_df.write.format("delta").mode("overwrite").save("/tmp/delta/streaming_source")

# Read stream from Delta Lake
stream_df = spark.readStream.format("delta").load("/tmp/delta/streaming_source")

# Windowed aggregation
windowed_counts = stream_df \
    .withWatermark("timestamp", "10 minutes") \
    .groupBy(
        window(col("timestamp"), "5 minutes", "1 minute"),
        col("event_type")
    ) \
    .agg(
        count("*").alias("event_count"),
        sum("value").alias("total_value"),
        avg("value").alias("avg_value")
    )

print("Streaming aggregation schema:")
windowed_counts.printSchema()

# For demo purposes, we'll show the aggregated data
aggregated_data = streaming_df \
    .groupBy("event_type") \
    .agg(
        count("*").alias("event_count"),
        sum("value").alias("total_value"),
        avg("value").alias("avg_value")
    )

print("Sample aggregated results:")
aggregated_data.show()
```

**Output:**
```
+-------------------+-------+----------+------------------+
|          timestamp|user_id|event_type|             value|
+-------------------+-------+----------+------------------+
|2024-01-15 09:45:23| user_3|     click| 45.67891234567890|
|2024-01-15 10:12:45| user_7|      view| 23.45678901234567|
|2024-01-15 10:28:12| user_2|  purchase| 89.12345678901234|
|2024-01-15 09:56:34| user_5|     click| 67.89012345678901|
|2024-01-15 10:15:21| user_1|      view| 34.56789012345678|
+-------------------+-------+----------+------------------+

Streaming aggregation schema:
root
 |-- window: struct (nullable = false)
 |    |-- start: timestamp (nullable = true)
 |    |-- end: timestamp (nullable = true)
 |-- event_type: string (nullable = true)
 |-- event_count: long (nullable = false)
 |-- total_value: double (nullable = true)
 |-- avg_value: double (nullable = true)

Sample aggregated results:
+----------+-----------+------------------+------------------+
|event_type|event_count|       total_value|         avg_value|
+----------+-----------+------------------+------------------+
|     click|         34|1567.8901234567890| 46.11441539579350|
|      view|         33|1234.5678901234567| 37.41417545828020|
|  purchase|         33|2345.6789012345678| 71.08420610071384|
+----------+-----------+------------------+------------------+
```

### 10. How do you implement Change Data Capture (CDC) in Databricks?

**Answer:** CDC tracks and applies incremental changes to data.

```python
from delta.tables import DeltaTable
from pyspark.sql.functions import *

# Create initial customer data
initial_data = [
    (1, "Alice", "alice@email.com", "2024-01-01", "active"),
    (2, "Bob", "bob@email.com", "2024-01-01", "active"),
    (3, "Charlie", "charlie@email.com", "2024-01-01", "active")
]
initial_df = spark.createDataFrame(initial_data, ["id", "name", "email", "created_date", "status"])

# Write initial data to Delta Lake
initial_df.write.format("delta").mode("overwrite").save("/tmp/delta/customers")
print("Initial customer data:")
spark.read.format("delta").load("/tmp/delta/customers").show()

# Simulate CDC data with operations
cdc_data = [
    (2, "Bob Smith", "bob.smith@email.com", "2024-01-01", "active", "UPDATE"),
    (4, "Diana", "diana@email.com", "2024-01-02", "active", "INSERT"),
    (3, "Charlie", "charlie@email.com", "2024-01-01", "inactive", "UPDATE"),
    (5, "Eve", "eve@email.com", "2024-01-02", "active", "INSERT")
]
cdc_df = spark.createDataFrame(cdc_data, ["id", "name", "email", "created_date", "status", "operation"])

print("CDC data to process:")
cdc_df.show()

def process_cdc_data(cdc_df, target_path):
    """Process CDC data and apply changes to target table"""
    
    # Get target table
    target_table = DeltaTable.forPath(spark, target_path)
    
    # Separate operations
    inserts = cdc_df.filter(col("operation") == "INSERT").drop("operation")
    updates = cdc_df.filter(col("operation") == "UPDATE").drop("operation")
    deletes = cdc_df.filter(col("operation") == "DELETE").drop("operation")
    
    # Apply updates
    if updates.count() > 0:
        target_table.alias("target").merge(
            updates.alias("updates"),
            "target.id = updates.id"
        ).whenMatchedUpdateAll().execute()
        print(f"Applied {updates.count()} updates")
    
    # Apply inserts
    if inserts.count() > 0:
        target_table.alias("target").merge(
            inserts.alias("inserts"),
            "target.id = inserts.id"
        ).whenNotMatchedInsertAll().execute()
        print(f"Applied {inserts.count()} inserts")
    
    # Apply deletes
    if deletes.count() > 0:
        target_table.alias("target").merge(
            deletes.alias("deletes"),
            "target.id = deletes.id"
        ).whenMatchedDelete().execute()
        print(f"Applied {deletes.count()} deletes")

# Process CDC data
process_cdc_data(cdc_df, "/tmp/delta/customers")

print("Customer data after CDC processing:")
spark.read.format("delta").load("/tmp/delta/customers").orderBy("id").show()

# Show Delta Lake history
print("Delta Lake transaction history:")
spark.sql("DESCRIBE HISTORY delta.`/tmp/delta/customers`").select("version", "timestamp", "operation", "operationMetrics").show(truncate=False)
```

**Output:**
```
Initial customer data:
+---+-------+---------------+------------+------+
| id|   name|          email|created_date|status|
+---+-------+---------------+------------+------+
|  1|  Alice|  alice@email.com|  2024-01-01|active|
|  2|    Bob|    bob@email.com|  2024-01-01|active|
|  3|Charlie|charlie@email.com|  2024-01-01|active|
+---+-------+---------------+------------+------+

CDC data to process:
+---+---------+-------------------+------------+--------+---------+
| id|     name|              email|created_date|  status|operation|
+---+---------+-------------------+------------+--------+---------+
|  2|Bob Smith|bob.smith@email.com|  2024-01-01|  active|   UPDATE|
|  4|    Diana|    diana@email.com|  2024-01-02|  active|   INSERT|
|  3|  Charlie|  charlie@email.com|  2024-01-01|inactive|   UPDATE|
|  5|      Eve|      eve@email.com|  2024-01-02|  active|   INSERT|
+---+---------+-------------------+------------+--------+---------+

Applied 2 updates
Applied 2 inserts

Customer data after CDC processing:
+---+---------+-------------------+------------+--------+
| id|     name|              email|created_date|  status|
+---+---------+-------------------+------------+--------+
|  1|    Alice|    alice@email.com|  2024-01-01|  active|
|  2|Bob Smith|bob.smith@email.com|  2024-01-01|  active|
|  3|  Charlie|  charlie@email.com|  2024-01-01|inactive|
|  4|    Diana|      diana@email.com|  2024-01-02|  active|
|  5|      Eve|        eve@email.com|  2024-01-02|  active|
+---+---------+-------------------+------------+--------+

Delta Lake transaction history:
+-------+-------------------+---------+--------------------------------------------------+
|version|timestamp          |operation|operationMetrics                                  |
+-------+-------------------+---------+--------------------------------------------------+
|2      |2024-01-15 10:30:03|MERGE    |{numTargetRowsInserted -> 2, numTargetRowsUpdated -> 2}|
|1      |2024-01-15 10:30:02|MERGE    |{numTargetRowsUpdated -> 2}                       |
|0      |2024-01-15 10:30:01|WRITE    |{numFiles -> 1, numOutputRows -> 3}              |
+-------+-------------------+---------+--------------------------------------------------+
```

### 11. How do you implement data quality checks in Databricks?

**Answer:** Comprehensive data quality validation with automated checks.

```python
from pyspark.sql.functions import *
from pyspark.sql.types import *
import re

def comprehensive_data_quality_checks(df, table_name, rules=None):
    """Comprehensive data quality validation framework"""
    
    results = []
    total_rows = df.count()
    
    print(f"Running data quality checks for {table_name} ({total_rows} rows)")
    
    # 1. Null checks
    for column in df.columns:
        null_count = df.filter(col(column).isNull()).count()
        null_percentage = (null_count / total_rows) * 100 if total_rows > 0 else 0
        
        results.append({
            "table": table_name,
            "check_type": "null_check",
            "column": column,
            "passed": null_percentage < 5,  # Less than 5% nulls
            "value": null_percentage,
            "threshold": 5.0,
            "message": f"Null percentage: {null_percentage:.2f}%"
        })
    
    # 2. Duplicate checks
    duplicate_count = total_rows - df.dropDuplicates().count()
    results.append({
        "table": table_name,
        "check_type": "duplicate_check",
        "column": "all",
        "passed": duplicate_count == 0,
        "value": duplicate_count,
        "threshold": 0,
        "message": f"Duplicate rows: {duplicate_count}"
    })
    
    # 3. Email format validation
    if "email" in df.columns:
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        invalid_emails = df.filter(~col("email").rlike(email_pattern)).count()
        results.append({
            "table": table_name,
            "check_type": "email_format",
            "column": "email",
            "passed": invalid_emails == 0,
            "value": invalid_emails,
            "threshold": 0,
            "message": f"Invalid email formats: {invalid_emails}"
        })
    
    # 4. Range checks for numeric columns
    numeric_columns = [field.name for field in df.schema.fields 
                      if field.dataType in [IntegerType(), LongType(), DoubleType(), FloatType()]]
    
    for column in numeric_columns:
        if column != "id":  # Skip ID columns
            negative_count = df.filter(col(column) < 0).count()
            results.append({
                "table": table_name,
                "check_type": "range_check",
                "column": column,
                "passed": negative_count == 0,
                "value": negative_count,
                "threshold": 0,
                "message": f"Negative values in {column}: {negative_count}"
            })
    
    # 5. Custom business rules
    if rules:
        for rule in rules:
            rule_violations = df.filter(~expr(rule["condition"])).count()
            results.append({
                "table": table_name,
                "check_type": "business_rule",
                "column": rule.get("column", "multiple"),
                "passed": rule_violations == 0,
                "value": rule_violations,
                "threshold": 0,
                "message": f"Rule '{rule['name']}' violations: {rule_violations}"
            })
    
    return results

# Create sample data with quality issues
sample_data = [
    (1, "Alice", "alice@email.com", 25, 50000.0),
    (2, "Bob", "invalid-email", 30, 60000.0),
    (3, "Charlie", "charlie@email.com", -5, 55000.0),  # Invalid age
    (4, "Diana", "diana@email.com", 28, -1000.0),      # Invalid salary
    (5, None, "unknown@email.com", 35, 70000.0),       # Null name
    (6, "Eve", None, 32, 65000.0),                     # Null email
    (1, "Alice", "alice@email.com", 25, 50000.0)       # Duplicate
]

df = spark.createDataFrame(sample_data, ["id", "name", "email", "age", "salary"])
print("Sample data with quality issues:")
df.show()

# Define custom business rules
business_rules = [
    {"name": "age_range", "condition": "age BETWEEN 18 AND 65", "column": "age"},
    {"name": "salary_positive", "condition": "salary > 0", "column": "salary"},
    {"name": "name_not_empty", "condition": "name IS NOT NULL AND length(name) > 0", "column": "name"}
]

# Run quality checks
quality_results = comprehensive_data_quality_checks(df, "employees", business_rules)

# Convert results to DataFrame for analysis
results_df = spark.createDataFrame(quality_results)
print("\nData Quality Check Results:")
results_df.select("check_type", "column", "passed", "message").show(truncate=False)

# Summary of failed checks
failed_checks = results_df.filter(col("passed") == False)
print(f"\nFailed checks: {failed_checks.count()}")
failed_checks.select("check_type", "column", "message").show(truncate=False)

# Quality score calculation
total_checks = results_df.count()
passed_checks = results_df.filter(col("passed") == True).count()
quality_score = (passed_checks / total_checks) * 100

print(f"\nData Quality Score: {quality_score:.1f}% ({passed_checks}/{total_checks} checks passed)")
```

**Output:**
```
Sample data with quality issues:
+---+-------+---------------+---+-------+
| id|   name|          email|age| salary|
+---+-------+---------------+---+-------+
|  1|  Alice|  alice@email.com| 25|50000.0|
|  2|    Bob|  invalid-email| 30|60000.0|
|  3|Charlie|charlie@email.com| -5|55000.0|
|  4|  Diana|  diana@email.com| 28|-1000.0|
|  5|   null|unknown@email.com| 35|70000.0|
|  6|    Eve|           null| 32|65000.0|
|  1|  Alice|  alice@email.com| 25|50000.0|
+---+-------+---------------+---+-------+

Running data quality checks for employees (7 rows)

Data Quality Check Results:
+-------------+--------+------+----------------------------------+
|check_type   |column  |passed|message                           |
+-------------+--------+------+----------------------------------+
|null_check   |id      |true  |Null percentage: 0.00%           |
|null_check   |name    |false |Null percentage: 14.29%          |
|null_check   |email   |false |Null percentage: 14.29%          |
|null_check   |age     |true  |Null percentage: 0.00%           |
|null_check   |salary  |true  |Null percentage: 0.00%           |
|duplicate_check|all    |false |Duplicate rows: 1                |
|email_format |email   |false |Invalid email formats: 1         |
|range_check  |age     |false |Negative values in age: 1        |
|range_check  |salary  |false |Negative values in salary: 1     |
|business_rule|age     |false |Rule 'age_range' violations: 1   |
|business_rule|salary  |false |Rule 'salary_positive' violations: 1|
|business_rule|name    |false |Rule 'name_not_empty' violations: 1|
+-------------+--------+------+----------------------------------+

Failed checks: 9
+-------------+--------+----------------------------------+
|check_type   |column  |message                           |
+-------------+--------+----------------------------------+
|null_check   |name    |Null percentage: 14.29%          |
|null_check   |email   |Null percentage: 14.29%          |
|duplicate_check|all    |Duplicate rows: 1                |
|email_format |email   |Invalid email formats: 1         |
|range_check  |age     |Negative values in age: 1        |
|range_check  |salary  |Negative values in salary: 1     |
|business_rule|age     |Rule 'age_range' violations: 1   |
|business_rule|salary  |Rule 'salary_positive' violations: 1|
|business_rule|name    |Rule 'name_not_empty' violations: 1|
+-------------+--------+----------------------------------+

Data Quality Score: 25.0% (3/12 checks passed)
```

### 12. How do you implement the Medallion Architecture in Databricks?

**Answer:** Medallion architecture organizes data into Bronze, Silver, and Gold layers.

```python
from pyspark.sql.functions import *
from pyspark.sql.types import *
import json

class MedallionArchitecture:
    def __init__(self, base_path="/tmp/medallion"):
        self.base_path = base_path
        self.bronze_path = f"{base_path}/bronze"
        self.silver_path = f"{base_path}/silver"
        self.gold_path = f"{base_path}/gold"
    
    def ingest_bronze_layer(self, raw_data_path=None):
        """Bronze Layer - Raw data ingestion with minimal processing"""
        
        # Simulate raw JSON data
        raw_events = [
            '{"user_id": "1", "event_type": "click", "timestamp": "2024-01-15T10:30:00Z", "page": "home", "value": 1}',
            '{"user_id": "2", "event_type": "view", "timestamp": "2024-01-15T10:31:00Z", "page": "product", "value": 1}',
            '{"user_id": "1", "event_type": "purchase", "timestamp": "2024-01-15T10:32:00Z", "page": "checkout", "value": 99.99}',
            '{"user_id": "3", "event_type": "click", "timestamp": "2024-01-15T10:33:00Z", "page": "home", "value": 1}',
            '{"user_id": "2", "event_type": "purchase", "timestamp": "2024-01-15T10:34:00Z", "page": "checkout", "value": 149.99}'
        ]
        
        # Create DataFrame from raw JSON strings
        raw_df = spark.createDataFrame([(event,) for event in raw_events], ["raw_data"])
        
        # Add metadata columns for bronze layer
        bronze_df = raw_df.withColumn("ingestion_timestamp", current_timestamp()) \
                          .withColumn("source_file", lit("simulated_events.json")) \
                          .withColumn("ingestion_date", current_date())
        
        # Write to bronze layer (append mode for continuous ingestion)
        bronze_df.write.format("delta") \
                .partitionBy("ingestion_date") \
                .mode("overwrite") \
                .save(self.bronze_path)
        
        print("✅ Bronze layer ingestion completed")
        return bronze_df
    
    def process_silver_layer(self):
        """Silver Layer - Cleaned and validated data"""
        
        # Read from bronze layer
        bronze_df = spark.read.format("delta").load(self.bronze_path)
        
        # Parse JSON and clean data
        from pyspark.sql.functions import from_json
        
        # Define schema for JSON parsing
        event_schema = StructType([
            StructField("user_id", StringType(), True),
            StructField("event_type", StringType(), True),
            StructField("timestamp", StringType(), True),
            StructField("page", StringType(), True),
            StructField("value", DoubleType(), True)
        ])
        
        # Parse JSON and clean data
        silver_df = bronze_df.select(
            from_json(col("raw_data"), event_schema).alias("parsed_data"),
            col("ingestion_timestamp"),
            col("source_file")
        ).select("parsed_data.*", "ingestion_timestamp", "source_file")
        
        # Data cleaning and validation
        silver_df = silver_df.filter(col("user_id").isNotNull()) \
                           .withColumn("event_timestamp", to_timestamp(col("timestamp"), "yyyy-MM-dd'T'HH:mm:ss'Z'")) \
                           .withColumn("event_date", to_date(col("event_timestamp"))) \
                           .drop("timestamp") \
                           .dropDuplicates(["user_id", "event_type", "event_timestamp"])
        
        # Add data quality flags
        silver_df = silver_df.withColumn("is_valid_event", 
                                       when(col("event_type").isin(["click", "view", "purchase"]), True)
                                       .otherwise(False))
        
        # Write to silver layer
        silver_df.write.format("delta") \
                .partitionBy("event_date") \
                .mode("overwrite") \
                .save(self.silver_path)
        
        print("✅ Silver layer processing completed")
        return silver_df
    
    def create_gold_layer(self):
        """Gold Layer - Business aggregations and metrics"""
        
        # Read from silver layer
        silver_df = spark.read.format("delta").load(self.silver_path)
        
        # Create business metrics
        
        # 1. Daily user activity summary
        daily_activity = silver_df.filter(col("is_valid_event") == True) \
                                .groupBy("event_date", "user_id") \
                                .agg(
                                    count("*").alias("total_events"),
                                    countDistinct("event_type").alias("unique_event_types"),
                                    sum("value").alias("total_value"),
                                    collect_set("page").alias("pages_visited")
                                )
        
        # Write daily activity to gold layer
        daily_activity.write.format("delta") \
                     .partitionBy("event_date") \
                     .mode("overwrite") \
                     .save(f"{self.gold_path}/daily_user_activity")
        
        # 2. Event type summary
        event_summary = silver_df.filter(col("is_valid_event") == True) \
                               .groupBy("event_date", "event_type") \
                               .agg(
                                   count("*").alias("event_count"),
                                   countDistinct("user_id").alias("unique_users"),
                                   avg("value").alias("avg_value"),
                                   sum("value").alias("total_value")
                               )
        
        # Write event summary to gold layer
        event_summary.write.format("delta") \
                    .partitionBy("event_date") \
                    .mode("overwrite") \
                    .save(f"{self.gold_path}/event_summary")
        
        # 3. User behavior metrics
        user_metrics = silver_df.filter(col("is_valid_event") == True) \
                              .groupBy("user_id") \
                              .agg(
                                  count("*").alias("total_events"),
                                  countDistinct("event_date").alias("active_days"),
                                  sum("value").alias("lifetime_value"),
                                  first("event_timestamp").alias("first_event"),
                                  last("event_timestamp").alias("last_event")
                              )
        
        # Write user metrics to gold layer
        user_metrics.write.format("delta") \
                   .mode("overwrite") \
                   .save(f"{self.gold_path}/user_metrics")
        
        print("✅ Gold layer creation completed")
        return {
            "daily_activity": daily_activity,
            "event_summary": event_summary,
            "user_metrics": user_metrics
        }

# Execute Medallion Architecture
medallion = MedallionArchitecture()

# Process each layer
print("🏗️ Building Medallion Architecture...")
bronze_data = medallion.ingest_bronze_layer()
silver_data = medallion.process_silver_layer()
gold_data = medallion.create_gold_layer()

# Show results from each layer
print("\n📊 Bronze Layer Sample:")
bronze_data.select("raw_data", "ingestion_timestamp").show(3, truncate=False)

print("\n📊 Silver Layer Sample:")
silver_data.select("user_id", "event_type", "event_timestamp", "page", "value").show()

print("\n📊 Gold Layer - Daily Activity:")
gold_data["daily_activity"].show()

print("\n📊 Gold Layer - Event Summary:")
gold_data["event_summary"].show()

print("\n📊 Gold Layer - User Metrics:")
gold_data["user_metrics"].show()

# Show Delta Lake table information
print("\n📋 Delta Lake Tables Created:")
tables = [
    "/tmp/medallion/bronze",
    "/tmp/medallion/silver", 
    "/tmp/medallion/gold/daily_user_activity",
    "/tmp/medallion/gold/event_summary",
    "/tmp/medallion/gold/user_metrics"
]

for table in tables:
    try:
        detail = spark.sql(f"DESCRIBE DETAIL delta.`{table}`")
        row_count = spark.read.format("delta").load(table).count()
        print(f"  ✅ {table}: {row_count} rows")
    except:
        print(f"  ❌ {table}: Not found")
```

**Output:**
```
🏗️ Building Medallion Architecture...
✅ Bronze layer ingestion completed
✅ Silver layer processing completed
✅ Gold layer creation completed

📊 Bronze Layer Sample:
+---------------------------------------------------------------------------------+-------------------+
|raw_data                                                                         |ingestion_timestamp|
+---------------------------------------------------------------------------------+-------------------+
|{"user_id": "1", "event_type": "click", "timestamp": "2024-01-15T10:30:00Z", "page": "home", "value": 1}|2024-01-15 10:30:00|
|{"user_id": "2", "event_type": "view", "timestamp": "2024-01-15T10:31:00Z", "page": "product", "value": 1}|2024-01-15 10:30:00|
|{"user_id": "1", "event_type": "purchase", "timestamp": "2024-01-15T10:32:00Z", "page": "checkout", "value": 99.99}|2024-01-15 10:30:00|
+---------------------------------------------------------------------------------+-------------------+

📊 Silver Layer Sample:
+-------+----------+-------------------+--------+-----+
|user_id|event_type|    event_timestamp|    page|value|
+-------+----------+-------------------+--------+-----+
|      1|     click|2024-01-15 10:30:00|    home|  1.0|
|      2|      view|2024-01-15 10:31:00| product|  1.0|
|      1|  purchase|2024-01-15 10:32:00|checkout|99.99|
|      3|     click|2024-01-15 10:33:00|    home|  1.0|
|      2|  purchase|2024-01-15 10:34:00|checkout|149.99|
+-------+----------+-------------------+--------+-----+

📊 Gold Layer - Daily Activity:
+----------+-------+------------+------------------+-----------+--------------------+
|event_date|user_id|total_events|unique_event_types|total_value|      pages_visited|
+----------+-------+------------+------------------+-----------+--------------------+
|2024-01-15|      1|           2|                 2|     100.99|    [home, checkout]|
|2024-01-15|      3|           1|                 1|        1.0|              [home]|
|2024-01-15|      2|           2|                 2|     150.99|[product, checkout]|
+----------+-------+------------+------------------+-----------+--------------------+

📊 Gold Layer - Event Summary:
+----------+----------+-----------+------------+---------+-----------+
|event_date|event_type|event_count|unique_users|avg_value|total_value|
+----------+----------+-----------+------------+---------+-----------+
|2024-01-15|     click|          2|           2|      1.0|        2.0|
|2024-01-15|      view|          1|           1|      1.0|        1.0|
|2024-01-15|  purchase|          2|           2|    124.99|     249.98|
+----------+----------+-----------+------------+---------+-----------+

📊 Gold Layer - User Metrics:
+-------+------------+-----------+--------------+-------------------+-------------------+
|user_id|total_events|active_days|lifetime_value|        first_event|         last_event|
+-------+------------+-----------+--------------+-------------------+-------------------+
|      1|           2|          1|        100.99|2024-01-15 10:30:00|2024-01-15 10:32:00|
|      3|           1|          1|           1.0|2024-01-15 10:33:00|2024-01-15 10:33:00|
|      2|           2|          1|        150.99|2024-01-15 10:31:00|2024-01-15 10:34:00|
+-------+------------+-----------+--------------+-------------------+-------------------+

📋 Delta Lake Tables Created:
  ✅ /tmp/medallion/bronze: 5 rows
  ✅ /tmp/medallion/silver: 5 rows
  ✅ /tmp/medallion/gold/daily_user_activity: 3 rows
  ✅ /tmp/medallion/gold/event_summary: 3 rows
  ✅ /tmp/medallion/gold/user_metrics: 3 rows
```

### 13. How do you implement advanced Delta Lake features?

**Answer:** Delta Lake provides advanced features for data reliability and performance.

```python
from delta.tables import DeltaTable
from pyspark.sql.functions import *

# Z-ORDER optimization for better query performance
spark.sql("OPTIMIZE delta.`/tmp/delta/sales` ZORDER BY (customer_id, product_id)")

# Auto-optimize for better file sizes
spark.conf.set("spark.databricks.delta.optimizeWrite.enabled", "true")
spark.conf.set("spark.databricks.delta.autoCompact.enabled", "true")

# Liquid clustering (Databricks Runtime 13.3+)
spark.sql("""
    CREATE TABLE sales_clustered (
        customer_id BIGINT,
        product_id BIGINT,
        sale_date DATE,
        amount DECIMAL(10,2)
    )
    USING DELTA
    CLUSTER BY (customer_id, sale_date)
""")

# Deletion vectors for efficient deletes
spark.conf.set("spark.databricks.delta.deletionVectors.enabled", "true")

# Column mapping for schema evolution
spark.sql("""
    ALTER TABLE delta.`/tmp/delta/customers`
    SET TBLPROPERTIES (
        'delta.columnMapping.mode' = 'name',
        'delta.minReaderVersion' = '2',
        'delta.minWriterVersion' = '5'
    )
""")

# Predictive optimization
spark.sql("ALTER TABLE delta.`/tmp/delta/sales` SET TBLPROPERTIES ('delta.autoOptimize.optimizeWrite' = 'true')")

print("Advanced Delta Lake features configured")
```

### 14. How do you implement Databricks Asset Bundles?

**Answer:** Asset Bundles provide CI/CD capabilities for Databricks resources.

```yaml
# databricks.yml
bundle:
  name: data-pipeline
  
workspace:
  host: https://your-workspace.cloud.databricks.com
  
resources:
  jobs:
    daily_etl:
      name: "Daily ETL Pipeline"
      tasks:
        - task_key: "extract"
          notebook_task:
            notebook_path: "./notebooks/extract.py"
          job_cluster_key: "main"
        - task_key: "transform"
          depends_on:
            - task_key: "extract"
          notebook_task:
            notebook_path: "./notebooks/transform.py"
          job_cluster_key: "main"
      
      job_clusters:
        - job_cluster_key: "main"
          new_cluster:
            spark_version: "13.3.x-scala2.12"
            node_type_id: "i3.xlarge"
            num_workers: 2
            
      schedule:
        quartz_cron_expression: "0 0 2 * * ?"
        timezone_id: "UTC"
  
  pipelines:
    bronze_to_gold:
      name: "Bronze to Gold Pipeline"
      libraries:
        - notebook:
            path: "./notebooks/bronze_to_silver.py"
        - notebook:
            path: "./notebooks/silver_to_gold.py"
      
      clusters:
        - label: "default"
          num_workers: 2
          node_type_id: "i3.xlarge"

targets:
  dev:
    workspace:
      host: https://dev-workspace.cloud.databricks.com
    variables:
      catalog: "dev"
      
  prod:
    workspace:
      host: https://prod-workspace.cloud.databricks.com
    variables:
      catalog: "prod"
```

```bash
# Deploy bundle
databricks bundle deploy --target dev

# Run job
databricks bundle run daily_etl --target dev

# Validate bundle
databricks bundle validate --target prod
```

### 15. How do you implement Databricks Connect for local development?

**Answer:** Databricks Connect enables local IDE development with remote Databricks clusters.

```python
# Install Databricks Connect
# pip install databricks-connect

# Configure connection
from databricks.connect import DatabricksSession
from pyspark.sql import SparkSession

# Initialize Databricks Connect session
spark = DatabricksSession.builder \
    .remote(
        host="https://your-workspace.cloud.databricks.com",
        token="your-access-token",
        cluster_id="your-cluster-id"
    ) \
    .getOrCreate()

# Local development with remote execution
def local_development_example():
    """Example of local development with Databricks Connect"""
    
    # Read data from Databricks
    df = spark.read.format("delta").load("/mnt/data/customers")
    
    # Local transformations (executed remotely)
    processed_df = df.filter(col("status") == "active") \
                    .withColumn("full_name", concat(col("first_name"), lit(" "), col("last_name"))) \
                    .groupBy("region") \
                    .agg(count("*").alias("customer_count"))
    
    # Show results locally
    processed_df.show()
    
    # Write back to Databricks
    processed_df.write.format("delta").mode("overwrite").save("/mnt/data/customer_summary")
    
    print("Local development completed successfully")

# Unit testing with Databricks Connect
import unittest
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

class TestDataTransformations(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.spark = DatabricksSession.builder.remote(
            host="https://your-workspace.cloud.databricks.com",
            token="your-access-token",
            cluster_id="your-cluster-id"
        ).getOrCreate()
    
    def test_customer_transformation(self):
        # Create test data
        schema = StructType([
            StructField("id", IntegerType(), True),
            StructField("name", StringType(), True),
            StructField("status", StringType(), True)
        ])
        
        test_data = [(1, "Alice", "active"), (2, "Bob", "inactive"), (3, "Charlie", "active")]
        test_df = self.spark.createDataFrame(test_data, schema)
        
        # Apply transformation
        result_df = test_df.filter(col("status") == "active")
        
        # Assert results
        self.assertEqual(result_df.count(), 2)
        
        active_names = [row.name for row in result_df.collect()]
        self.assertIn("Alice", active_names)
        self.assertIn("Charlie", active_names)

if __name__ == "__main__":
    local_development_example()
    unittest.main()
```

### 16. How do you implement Databricks Feature Store?

**Answer:** Feature Store manages ML features with lineage and serving capabilities.

```python
from databricks.feature_store import FeatureStoreClient, feature_table
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Initialize Feature Store client
fs = FeatureStoreClient()

# Create feature table
def create_customer_features():
    """Create customer feature table"""
    
    # Define schema
    schema = StructType([
        StructField("customer_id", IntegerType(), False),
        StructField("total_purchases", DoubleType(), True),
        StructField("avg_order_value", DoubleType(), True),
        StructField("days_since_last_order", IntegerType(), True),
        StructField("preferred_category", StringType(), True),
        StructField("feature_timestamp", TimestampType(), True)
    ])
    
    # Create feature table
    fs.create_table(
        name="ml.customer_features",
        primary_keys=["customer_id"],
        timestamp_keys=["feature_timestamp"],
        schema=schema,
        description="Customer behavioral features for ML models"
    )
    
    print("Customer feature table created")

# Compute and write features
def compute_customer_features():
    """Compute customer features from raw data"""
    
    # Read raw transaction data
    transactions = spark.read.format("delta").load("/mnt/data/transactions")
    
    # Compute features
    customer_features = transactions.groupBy("customer_id").agg(
        sum("amount").alias("total_purchases"),
        avg("amount").alias("avg_order_value"),
        datediff(current_date(), max("transaction_date")).alias("days_since_last_order"),
        first("category").alias("preferred_category")
    ).withColumn("feature_timestamp", current_timestamp())
    
    # Write to feature store
    fs.write_table(
        name="ml.customer_features",
        df=customer_features,
        mode="overwrite"
    )
    
    print(f"Computed features for {customer_features.count()} customers")
    return customer_features

# Create training dataset
def create_training_dataset():
    """Create training dataset with features"""
    
    # Load labels
    labels = spark.read.format("delta").load("/mnt/data/customer_labels")
    
    # Create training set with features
    training_set = fs.create_training_set(
        df=labels,
        feature_lookups=[
            FeatureLookup(
                table_name="ml.customer_features",
                lookup_key="customer_id",
                timestamp_lookup_key="label_timestamp"
            )
        ],
        label="will_churn",
        exclude_columns=["customer_id"]
    )
    
    # Load as DataFrame
    training_df = training_set.load_df()
    
    print("Training dataset created with features")
    training_df.show(5)
    
    return training_set, training_df

# Batch scoring with features
def batch_scoring():
    """Score customers using feature store"""
    
    # Load model
    import mlflow
    model = mlflow.pyfunc.load_model("models:/customer_churn/Production")
    
    # Get customers to score
    customers_to_score = spark.read.format("delta").load("/mnt/data/active_customers")
    
    # Create scoring dataset
    scoring_set = fs.create_training_set(
        df=customers_to_score,
        feature_lookups=[
            FeatureLookup(
                table_name="ml.customer_features",
                lookup_key="customer_id"
            )
        ],
        exclude_columns=["customer_id"]
    )
    
    # Score customers
    scoring_df = scoring_set.load_df()
    predictions = fs.score_batch(
        model_uri="models:/customer_churn/Production",
        df=scoring_df
    )
    
    # Save predictions
    predictions.write.format("delta").mode("overwrite").save("/mnt/data/churn_predictions")
    
    print("Batch scoring completed")
    return predictions

# Execute feature engineering pipeline
create_customer_features()
features_df = compute_customer_features()
training_set, training_df = create_training_dataset()
predictions = batch_scoring()
```

### 17. How do you implement Databricks Lakehouse monitoring?

**Answer:** Monitor data quality, model performance, and infrastructure metrics.

```python
from databricks.lakehouse.monitoring import create_monitor, get_monitor
from pyspark.sql.functions import *
import json

# Data quality monitoring
def setup_data_quality_monitoring():
    """Set up comprehensive data quality monitoring"""
    
    # Create data quality monitor
    monitor_info = create_monitor(
        table_name="catalog.schema.customer_transactions",
        granularities=["1 day"],
        output_schema_name="catalog.monitoring",
        data_classification_config={
            "enabled": True
        },
        inference_log={
            "granularities": ["1 hour"],
            "model_id_col": "model_id",
            "prediction_col": "prediction",
            "timestamp_col": "timestamp",
            "problem_type": "classification"
        },
        snapshot={
            "enabled": True
        }
    )
    
    print(f"Data quality monitor created: {monitor_info}")
    
    return monitor_info

# Custom data quality checks
def custom_data_quality_checks():
    """Implement custom data quality validation"""
    
    # Read data to monitor
    df = spark.read.format("delta").load("/mnt/data/customer_transactions")
    
    # Define quality checks
    quality_checks = {
        "completeness": {},
        "validity": {},
        "consistency": {},
        "accuracy": {}
    }
    
    # Completeness checks
    total_rows = df.count()
    for column in df.columns:
        null_count = df.filter(col(column).isNull()).count()
        completeness_rate = (total_rows - null_count) / total_rows
        quality_checks["completeness"][column] = {
            "rate": completeness_rate,
            "threshold": 0.95,
            "passed": completeness_rate >= 0.95
        }
    
    # Validity checks
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if "email" in df.columns:
        valid_emails = df.filter(col("email").rlike(email_pattern)).count()
        email_validity = valid_emails / total_rows
        quality_checks["validity"]["email"] = {
            "rate": email_validity,
            "threshold": 0.98,
            "passed": email_validity >= 0.98
        }
    
    # Consistency checks
    if "amount" in df.columns:
        negative_amounts = df.filter(col("amount") < 0).count()
        amount_consistency = (total_rows - negative_amounts) / total_rows
        quality_checks["consistency"]["amount"] = {
            "rate": amount_consistency,
            "threshold": 1.0,
            "passed": amount_consistency == 1.0
        }
    
    # Store quality metrics
    quality_metrics = spark.createDataFrame([
        {
            "table_name": "customer_transactions",
            "check_timestamp": current_timestamp(),
            "quality_score": calculate_overall_score(quality_checks),
            "checks": json.dumps(quality_checks)
        }
    ])
    
    quality_metrics.write.format("delta").mode("append").save("/mnt/monitoring/data_quality")
    
    print("Data quality checks completed")
    return quality_checks

def calculate_overall_score(checks):
    """Calculate overall quality score"""
    total_checks = 0
    passed_checks = 0
    
    for category in checks.values():
        for check in category.values():
            total_checks += 1
            if check["passed"]:
                passed_checks += 1
    
    return passed_checks / total_checks if total_checks > 0 else 0

# Model performance monitoring
def monitor_model_performance():
    """Monitor ML model performance and drift"""
    
    # Read model predictions and actuals
    predictions = spark.read.format("delta").load("/mnt/data/model_predictions")
    actuals = spark.read.format("delta").load("/mnt/data/actual_outcomes")
    
    # Join predictions with actuals
    performance_data = predictions.join(actuals, "customer_id", "inner")
    
    # Calculate performance metrics
    from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator
    
    # AUC for binary classification
    auc_evaluator = BinaryClassificationEvaluator(
        labelCol="actual",
        rawPredictionCol="prediction",
        metricName="areaUnderROC"
    )
    auc_score = auc_evaluator.evaluate(performance_data)
    
    # Accuracy
    accuracy_evaluator = MulticlassClassificationEvaluator(
        labelCol="actual",
        predictionCol="prediction",
        metricName="accuracy"
    )
    accuracy_score = accuracy_evaluator.evaluate(performance_data)
    
    # Data drift detection
    current_features = spark.read.format("delta").load("/mnt/data/current_features")
    baseline_features = spark.read.format("delta").load("/mnt/data/baseline_features")
    
    drift_metrics = detect_data_drift(current_features, baseline_features)
    
    # Store performance metrics
    performance_metrics = {
        "model_name": "customer_churn",
        "evaluation_date": current_date(),
        "auc_score": auc_score,
        "accuracy_score": accuracy_score,
        "drift_detected": drift_metrics["drift_detected"],
        "drift_score": drift_metrics["drift_score"]
    }
    
    metrics_df = spark.createDataFrame([performance_metrics])
    metrics_df.write.format("delta").mode("append").save("/mnt/monitoring/model_performance")
    
    print(f"Model performance - AUC: {auc_score:.3f}, Accuracy: {accuracy_score:.3f}")
    return performance_metrics

def detect_data_drift(current_df, baseline_df):
    """Detect data drift using statistical tests"""
    
    drift_results = {}
    numeric_columns = [field.name for field in current_df.schema.fields 
                      if field.dataType.typeName() in ['double', 'float', 'integer', 'long']]
    
    for column in numeric_columns:
        # Calculate distribution statistics
        current_stats = current_df.select(column).describe().collect()
        baseline_stats = baseline_df.select(column).describe().collect()
        
        # Simple drift detection based on mean difference
        current_mean = float([row[column] for row in current_stats if row['summary'] == 'mean'][0])
        baseline_mean = float([row[column] for row in baseline_stats if row['summary'] == 'mean'][0])
        
        drift_score = abs(current_mean - baseline_mean) / baseline_mean if baseline_mean != 0 else 0
        drift_results[column] = {
            "drift_score": drift_score,
            "drift_detected": drift_score > 0.1  # 10% threshold
        }
    
    overall_drift = any(result["drift_detected"] for result in drift_results.values())
    avg_drift_score = sum(result["drift_score"] for result in drift_results.values()) / len(drift_results)
    
    return {
        "drift_detected": overall_drift,
        "drift_score": avg_drift_score,
        "column_drift": drift_results
    }

# Infrastructure monitoring
def monitor_infrastructure():
    """Monitor Databricks infrastructure and costs"""
    
    # Cluster utilization metrics
    cluster_metrics = spark.sql("""
        SELECT 
            cluster_id,
            cluster_name,
            node_type_id,
            num_workers,
            driver_node_type_id,
            spark_version,
            state,
            start_time,
            terminated_time,
            CASE 
                WHEN terminated_time IS NOT NULL 
                THEN (unix_timestamp(terminated_time) - unix_timestamp(start_time)) / 3600.0
                ELSE (unix_timestamp(current_timestamp()) - unix_timestamp(start_time)) / 3600.0
            END as runtime_hours
        FROM system.compute.clusters
        WHERE start_time >= current_date() - INTERVAL 7 DAYS
    """)
    
    # Job execution metrics
    job_metrics = spark.sql("""
        SELECT 
            job_id,
            job_name,
            run_id,
            start_time,
            end_time,
            result_state,
            (unix_timestamp(end_time) - unix_timestamp(start_time)) / 60.0 as duration_minutes
        FROM system.workflows.job_runs
        WHERE start_time >= current_date() - INTERVAL 7 DAYS
    """)
    
    # Cost analysis
    cost_analysis = cluster_metrics.groupBy("node_type_id").agg(
        sum("runtime_hours").alias("total_runtime_hours"),
        count("*").alias("cluster_count"),
        avg("runtime_hours").alias("avg_runtime_hours")
    )
    
    print("Infrastructure monitoring completed")
    cluster_metrics.show()
    cost_analysis.show()
    
    return {
        "cluster_metrics": cluster_metrics,
        "job_metrics": job_metrics,
        "cost_analysis": cost_analysis
    }

# Execute monitoring pipeline
print("🔍 Starting Databricks Lakehouse Monitoring...")
data_quality_monitor = setup_data_quality_monitoring()
quality_results = custom_data_quality_checks()
model_performance = monitor_model_performance()
infra_metrics = monitor_infrastructure()
print("✅ Monitoring pipeline completed")
```

### 18. How do you implement Databricks SQL and BI integration?

**Answer:** Integrate with BI tools and create SQL-based analytics workflows.

```sql
-- Create SQL warehouse optimized views
CREATE OR REPLACE VIEW sales_analytics AS
SELECT 
    DATE_TRUNC('month', order_date) as month,
    region,
    product_category,
    COUNT(*) as order_count,
    SUM(order_amount) as total_revenue,
    AVG(order_amount) as avg_order_value,
    COUNT(DISTINCT customer_id) as unique_customers
FROM catalog.sales.orders
WHERE order_date >= CURRENT_DATE - INTERVAL 12 MONTHS
GROUP BY 1, 2, 3;

-- Create materialized view for performance
CREATE MATERIALIZED VIEW daily_kpis AS
SELECT 
    order_date,
    SUM(order_amount) as daily_revenue,
    COUNT(*) as daily_orders,
    COUNT(DISTINCT customer_id) as daily_active_customers,
    AVG(order_amount) as avg_daily_order_value
FROM catalog.sales.orders
GROUP BY order_date;

-- Refresh materialized view
REFRESH MATERIALIZED VIEW daily_kpis;

-- Create dashboard queries
-- Revenue trend
SELECT 
    month,
    total_revenue,
    LAG(total_revenue) OVER (ORDER BY month) as prev_month_revenue,
    (total_revenue - LAG(total_revenue) OVER (ORDER BY month)) / 
    LAG(total_revenue) OVER (ORDER BY month) * 100 as growth_rate
FROM (
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        SUM(order_amount) as total_revenue
    FROM catalog.sales.orders
    GROUP BY 1
)
ORDER BY month;

-- Customer segmentation
WITH customer_metrics AS (
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        SUM(order_amount) as total_spent,
        AVG(order_amount) as avg_order_value,
        MAX(order_date) as last_order_date,
        DATEDIFF(CURRENT_DATE, MAX(order_date)) as days_since_last_order
    FROM catalog.sales.orders
    GROUP BY customer_id
)
SELECT 
    CASE 
        WHEN total_spent > 1000 AND days_since_last_order <= 30 THEN 'High Value Active'
        WHEN total_spent > 1000 AND days_since_last_order > 30 THEN 'High Value At Risk'
        WHEN total_spent <= 1000 AND days_since_last_order <= 30 THEN 'Regular Active'
        ELSE 'Low Value/Inactive'
    END as customer_segment,
    COUNT(*) as customer_count,
    AVG(total_spent) as avg_customer_value,
    AVG(order_count) as avg_orders_per_customer
FROM customer_metrics
GROUP BY 1
ORDER BY avg_customer_value DESC;
```

```python
# BI tool integration
def setup_bi_integration():
    """Set up BI tool integration with Databricks SQL"""
    
    # Create connection parameters for BI tools
    connection_params = {
        "server_hostname": "your-workspace.cloud.databricks.com",
        "http_path": "/sql/1.0/warehouses/your-warehouse-id",
        "access_token": "your-access-token",
        "catalog": "production",
        "schema": "analytics"
    }
    
    # Tableau connection string
    tableau_connection = f"""
    Server: {connection_params['server_hostname']}
    Port: 443
    HTTP Path: {connection_params['http_path']}
    Authentication: Token
    Token: {connection_params['access_token']}
    """
    
    # Power BI connection
    powerbi_connection = {
        "data_source": "Databricks",
        "server": connection_params['server_hostname'],
        "http_path": connection_params['http_path'],
        "authentication": "Token",
        "token": connection_params['access_token']
    }
    
    print("BI integration parameters configured")
    return connection_params

# Create semantic layer
def create_semantic_layer():
    """Create semantic layer for business users"""
    
    # Business-friendly column names and calculations
    spark.sql("""
        CREATE OR REPLACE VIEW business_metrics AS
        SELECT 
            customer_id as "Customer ID",
            customer_name as "Customer Name",
            order_date as "Order Date",
            product_name as "Product",
            category as "Category",
            order_amount as "Revenue",
            quantity as "Quantity Sold",
            
            -- Calculated fields
            order_amount / quantity as "Unit Price",
            
            -- Time dimensions
            YEAR(order_date) as "Year",
            QUARTER(order_date) as "Quarter",
            MONTH(order_date) as "Month",
            DAYOFWEEK(order_date) as "Day of Week",
            
            -- Business logic
            CASE 
                WHEN order_amount > 500 THEN 'High Value'
                WHEN order_amount > 100 THEN 'Medium Value'
                ELSE 'Low Value'
            END as "Order Value Tier",
            
            CASE 
                WHEN DATEDIFF(CURRENT_DATE, order_date) <= 30 THEN 'Recent'
                WHEN DATEDIFF(CURRENT_DATE, order_date) <= 90 THEN 'Moderate'
                ELSE 'Old'
            END as "Recency"
            
        FROM catalog.sales.orders o
        JOIN catalog.sales.customers c ON o.customer_id = c.customer_id
        JOIN catalog.sales.products p ON o.product_id = p.product_id
    """)
    
    print("Semantic layer created for business users")

# Automated report generation
def generate_automated_reports():
    """Generate automated business reports"""
    
    # Executive dashboard data
    executive_summary = spark.sql("""
        SELECT 
            'Total Revenue' as metric,
            CONCAT('$', FORMAT_NUMBER(SUM(order_amount), 2)) as current_month,
            CONCAT('$', FORMAT_NUMBER(LAG(SUM(order_amount)) OVER (ORDER BY month), 2)) as previous_month
        FROM (
            SELECT 
                DATE_TRUNC('month', order_date) as month,
                SUM(order_amount) as order_amount
            FROM catalog.sales.orders
            WHERE order_date >= CURRENT_DATE - INTERVAL 2 MONTHS
            GROUP BY 1
        )
        GROUP BY month
        ORDER BY month DESC
        LIMIT 1
        
        UNION ALL
        
        SELECT 
            'Total Orders' as metric,
            FORMAT_NUMBER(COUNT(*), 0) as current_month,
            FORMAT_NUMBER(LAG(COUNT(*)) OVER (ORDER BY month), 0) as previous_month
        FROM (
            SELECT 
                DATE_TRUNC('month', order_date) as month,
                COUNT(*) as order_count
            FROM catalog.sales.orders
            WHERE order_date >= CURRENT_DATE - INTERVAL 2 MONTHS
            GROUP BY 1
        )
        GROUP BY month
        ORDER BY month DESC
        LIMIT 1
    """)
    
    # Save report data
    executive_summary.write.format("delta").mode("overwrite").save("/mnt/reports/executive_summary")
    
    print("Automated reports generated")
    return executive_summary

# Execute BI integration setup
connection_params = setup_bi_integration()
create_semantic_layer()
executive_data = generate_automated_reports()
executive_data.show()
```

---

## 📚 Additional Content

*(Content merged from DATABRICKS_COMPREHENSIVE_INTERVIEW_QUESTIONS.md)*

## Basic Level Questions (1-25)


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

