# Apache Spark Interview Questions for Data Engineering

## 📋 Table of Contents

1. [Basic Level Questions (1-25)](#basic-level-questions-1-25)
2. [Intermediate Level Questions (26-50)](#intermediate-level-questions-26-50)
3. [Advanced Level Questions (51-75)](#advanced-level-questions-51-75)
4. [Architecture & Performance (76-100)](#architecture--performance-76-100)
5. [Streaming & Real-time Processing (101-125)](#streaming--real-time-processing-101-125)
6. [Machine Learning & MLOps (126-150)](#machine-learning--mlops-126-150)
7. [Production & Operations (151-175)](#production--operations-151-175)
8. [Scenario-Based Questions (176-200)](#scenario-based-questions-176-200)

---

## Basic Level Questions (1-25)

### 1. What is Apache Spark and how does it differ from Hadoop MapReduce?
**Answer:**
Apache Spark is a unified analytics engine for large-scale data processing with built-in modules for streaming, SQL, machine learning, and graph processing.

**Key Differences:**
- **Speed**: Spark is 100x faster than MapReduce due to in-memory computing
- **Ease of Use**: High-level APIs in Java, Scala, Python, and R
- **Unified Platform**: Single platform for batch, streaming, ML, and graph processing
- **Memory Management**: Intelligent caching and memory management

```python
# Spark example
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("DataProcessing").getOrCreate()

# Read data
df = spark.read.csv("data.csv", header=True, inferSchema=True)

# Process data (lazy evaluation)
result = df.filter(df.age > 25).groupBy("department").count()

# Action triggers execution
result.show()
```

### 2. Explain Spark's architecture and core components
**Answer:**
**Core Components:**
- **Driver Program**: Coordinates the application
- **Cluster Manager**: Manages resources (YARN, Mesos, Kubernetes)
- **Executors**: Run tasks and store data
- **SparkContext**: Entry point for Spark functionality

```python
# SparkContext example
from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName("MyApp").setMaster("local[*]")
sc = SparkContext(conf=conf)

# Create RDD
rdd = sc.parallelize([1, 2, 3, 4, 5])
result = rdd.map(lambda x: x * 2).collect()
print(result)  # [2, 4, 6, 8, 10]
```

### 3. What are RDDs and their key characteristics?
**Answer:**
RDD (Resilient Distributed Dataset) is Spark's fundamental data structure.

**Key Characteristics:**
- **Immutable**: Cannot be changed after creation
- **Distributed**: Partitioned across cluster nodes
- **Fault-tolerant**: Automatically recovers from failures
- **Lazy Evaluation**: Computations are deferred until an action is called

```python
# RDD operations
rdd = sc.textFile("file.txt")

# Transformations (lazy)
words = rdd.flatMap(lambda line: line.split(" "))
word_counts = words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

# Action (triggers execution)
results = word_counts.collect()
```

### 4. Explain the difference between transformations and actions in Spark
**Answer:**
**Transformations:**
- Create new RDD from existing RDD
- Lazy evaluation (not executed immediately)
- Examples: map, filter, groupBy, join

**Actions:**
- Trigger execution of transformations
- Return results to driver or write to storage
- Examples: collect, count, save, show

```python
# Transformations
df_filtered = df.filter(df.age > 25)  # Lazy
df_grouped = df_filtered.groupBy("department").count()  # Lazy

# Actions
df_grouped.show()  # Triggers execution
count = df.count()  # Triggers execution
df_grouped.write.csv("output")  # Triggers execution
```

### 5. What is the Catalyst Optimizer in Spark SQL?
**Answer:**
Catalyst is Spark SQL's query optimizer that uses rule-based optimization.

**Optimization Phases:**
1. **Logical Plan**: Parse SQL to logical plan
2. **Optimized Logical Plan**: Apply optimization rules
3. **Physical Plan**: Generate physical execution plans
4. **Code Generation**: Generate Java bytecode

```python
# Enable cost-based optimization
spark.conf.set("spark.sql.cbo.enabled", "true")
spark.conf.set("spark.sql.adaptive.enabled", "true")

# View execution plan
df.explain(True)  # Shows all optimization phases
```

### 6. How does Spark handle memory management?
**Answer:**
Spark divides memory into regions:

**Memory Regions:**
- **Execution Memory**: For shuffles, joins, sorts, aggregations
- **Storage Memory**: For caching RDDs and DataFrames
- **User Memory**: For user data structures
- **Reserved Memory**: For Spark's internal objects

```python
# Memory configuration
spark.conf.set("spark.executor.memory", "4g")
spark.conf.set("spark.executor.memoryFraction", "0.8")
spark.conf.set("spark.storage.memoryFraction", "0.5")

# Caching strategies
df.cache()  # MEMORY_ONLY
df.persist(StorageLevel.MEMORY_AND_DISK)
df.unpersist()  # Remove from cache
```

### 7. What are the different cluster managers supported by Spark?
**Answer:**
**Cluster Managers:**
- **Standalone**: Spark's built-in cluster manager
- **YARN**: Hadoop's resource manager
- **Mesos**: General-purpose cluster manager
- **Kubernetes**: Container orchestration platform

```python
# Different deployment modes
# Standalone
spark-submit --master spark://master:7077 app.py

# YARN
spark-submit --master yarn --deploy-mode cluster app.py

# Kubernetes
spark-submit --master k8s://https://kubernetes-api app.py
```

### 8. Explain Spark's lazy evaluation and its benefits
**Answer:**
Lazy evaluation means transformations are not executed until an action is called.

**Benefits:**
- **Optimization**: Catalyst can optimize entire query plan
- **Efficiency**: Eliminates intermediate results
- **Fault Tolerance**: Can recompute lost partitions
- **Pipeline Optimization**: Combines multiple operations

```python
# Lazy evaluation example
rdd1 = sc.textFile("file1.txt")  # Not executed
rdd2 = rdd1.filter(lambda x: "error" in x)  # Not executed
rdd3 = rdd2.map(lambda x: x.upper())  # Not executed

# Only when action is called, entire pipeline executes
results = rdd3.collect()  # Execution happens here
```

### 9. What are the different deployment modes in Spark?
**Answer:**
**Deployment Modes:**
- **Client Mode**: Driver runs on client machine
- **Cluster Mode**: Driver runs on cluster worker node
- **Local Mode**: Single JVM for development/testing

```bash
# Client mode
spark-submit --deploy-mode client --master yarn app.py

# Cluster mode  
spark-submit --deploy-mode cluster --master yarn app.py

# Local mode
spark-submit --master local[*] app.py
```

### 10. Explain Spark SQL and its components
**Answer:**
**Spark SQL Components:**
- **DataFrame API**: Structured data abstraction
- **Dataset API**: Type-safe DataFrame (Scala/Java)
- **SQL Interface**: Standard SQL queries
- **Catalyst Optimizer**: Query optimization engine

```python
# DataFrame API
df = spark.read.json("data.json")
result = df.select("name", "age").filter(df.age > 21)

# SQL Interface
df.createOrReplaceTempView("people")
result = spark.sql("SELECT name, age FROM people WHERE age > 21")
```

### 11. What are the different storage levels in Spark?
**Answer:**
```python
from pyspark import StorageLevel

# Memory only (default for cache())
df.persist(StorageLevel.MEMORY_ONLY)

# Memory and disk
df.persist(StorageLevel.MEMORY_AND_DISK)

# Serialized in memory
df.persist(StorageLevel.MEMORY_ONLY_SER)

# Disk only
df.persist(StorageLevel.DISK_ONLY)

# With replication
df.persist(StorageLevel.MEMORY_AND_DISK_2)
```

### 12. How does Spark handle fault tolerance?
**Answer:**
**Fault Tolerance Mechanisms:**
- **RDD Lineage**: Recompute lost partitions using lineage graph
- **Checkpointing**: Persist RDD to reliable storage
- **Task Retry**: Automatically retry failed tasks
- **Speculative Execution**: Run duplicate tasks for slow nodes

```python
# Enable checkpointing
sc.setCheckpointDir("hdfs://checkpoint")
rdd.checkpoint()

# Configure task retries
spark.conf.set("spark.task.maxAttempts", "3")
spark.conf.set("spark.stage.maxConsecutiveAttempts", "8")
```

### 13. What is the difference between DataFrame and Dataset?
**Answer:**
**DataFrame vs Dataset:**
- **DataFrame**: Untyped, available in all languages
- **Dataset**: Type-safe, only in Scala/Java
- **Performance**: Similar performance due to Catalyst
- **Compile-time Safety**: Dataset provides compile-time type checking

```scala
// Dataset (Scala)
case class Person(name: String, age: Int)
val ds: Dataset[Person] = spark.read.json("people.json").as[Person]

// DataFrame (any language)
val df: DataFrame = spark.read.json("people.json")
```

### 14. Explain Spark's execution model
**Answer:**
**Execution Flow:**
1. **Job**: Triggered by action
2. **Stage**: Set of tasks that can run in parallel
3. **Task**: Unit of work sent to executor
4. **Shuffle**: Data exchange between stages

```python
# This creates multiple stages due to shuffle
rdd1 = sc.textFile("file1.txt")
rdd2 = sc.textFile("file2.txt")
joined = rdd1.join(rdd2)  # Shuffle boundary
result = joined.count()   # Action triggers job
```

### 15. What are accumulators and broadcast variables?
**Answer:**
```python
# Accumulators - write-only variables
counter = sc.accumulator(0)

def process_line(line):
    if "ERROR" in line:
        counter.add(1)
    return line.upper()

rdd.map(process_line).collect()
print(f"Errors found: {counter.value}")

# Broadcast variables - read-only shared data
lookup_dict = {"A": 1, "B": 2, "C": 3}
broadcast_dict = sc.broadcast(lookup_dict)

def enrich_data(record):
    return broadcast_dict.value.get(record, 0)

rdd.map(enrich_data).collect()
```

### 16. How do you handle small files problem in Spark?
**Answer:**
```python
# Problem: Many small files cause performance issues

# Solution 1: Coalesce partitions
df.coalesce(1).write.parquet("output")

# Solution 2: Repartition before writing
df.repartition(10).write.parquet("output")

# Solution 3: Use maxRecordsPerFile
df.write.option("maxRecordsPerFile", 100000).parquet("output")

# Solution 4: Combine small files during read
spark.conf.set("spark.sql.files.maxPartitionBytes", "134217728")  # 128MB
```

### 17. What is Dynamic Allocation in Spark?
**Answer:**
```python
# Enable dynamic allocation
spark.conf.set("spark.dynamicAllocation.enabled", "true")
spark.conf.set("spark.dynamicAllocation.minExecutors", "1")
spark.conf.set("spark.dynamicAllocation.maxExecutors", "20")
spark.conf.set("spark.dynamicAllocation.initialExecutors", "5")

# Configure scaling behavior
spark.conf.set("spark.dynamicAllocation.executorIdleTimeout", "60s")
spark.conf.set("spark.dynamicAllocation.schedulerBacklogTimeout", "1s")
```

### 18. Explain Spark's memory management
**Answer:**
**Memory Regions:**
- **Reserved Memory**: 300MB for system
- **User Memory**: User data structures (40% by default)
- **Spark Memory**: Execution + Storage (60% by default)
  - **Execution Memory**: Shuffles, joins, sorts
  - **Storage Memory**: Cached RDDs/DataFrames

```python
# Configure memory settings
spark.conf.set("spark.executor.memory", "4g")
spark.conf.set("spark.executor.memoryFraction", "0.8")
spark.conf.set("spark.storage.memoryFraction", "0.5")
spark.conf.set("spark.executor.extraJavaOptions", "-XX:+UseG1GC")
```

### 19. What are the different file formats supported by Spark?
**Answer:**
```python
# Text files
df = spark.read.text("data.txt")
df.write.text("output")

# CSV
df = spark.read.csv("data.csv", header=True, inferSchema=True)
df.write.csv("output", header=True)

# JSON
df = spark.read.json("data.json")
df.write.json("output")

# Parquet (recommended for analytics)
df = spark.read.parquet("data.parquet")
df.write.parquet("output")

# Delta Lake
df = spark.read.format("delta").load("delta-table")
df.write.format("delta").save("delta-table")

# Avro
df = spark.read.format("avro").load("data.avro")
df.write.format("avro").save("output")
```

### 20. How do you debug Spark applications?
**Answer:**
```python
# 1. Use Spark UI (port 4040)
# Access at http://driver-node:4040

# 2. Enable detailed logging
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.logLevel", "INFO")

# 3. Explain query plans
df.explain(True)  # Shows all optimization phases
df.explain("cost")  # Shows cost-based optimization

# 4. Use DataFrame/Dataset operations for better debugging
df.show()  # Display data
df.printSchema()  # Show schema
df.describe().show()  # Statistics

# 5. Cache intermediate results for debugging
intermediate_df = df.filter(condition).cache()
intermediate_df.count()  # Force caching
```

### 21. What is Adaptive Query Execution (AQE)?
**Answer:**
```python
# Enable AQE (Spark 3.0+)
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")

# AQE Features:
# 1. Dynamically coalesce shuffle partitions
# 2. Dynamically switch join strategies
# 3. Dynamically optimize skew joins

# Monitor AQE optimizations
df.explain("formatted")  # Shows AQE optimizations applied
```

### 22. How do you handle schema evolution in Spark?
**Answer:**
```python
# Enable schema merging for Parquet
df = spark.read.option("mergeSchema", "true").parquet("data")

# Handle schema evolution with Delta Lake
df.write.format("delta").option("mergeSchema", "true").save("delta-table")

# Explicit schema definition
from pyspark.sql.types import *

schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])

df = spark.read.schema(schema).json("data.json")
```

### 23. What are User Defined Functions (UDFs) and their performance implications?
**Answer:**
```python
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

# Python UDF (slower due to serialization)
def upper_case(text):
    return text.upper() if text else None

upper_udf = udf(upper_case, StringType())
df.withColumn("upper_name", upper_udf(df.name))

# Vectorized UDF (faster)
from pyspark.sql.functions import pandas_udf
import pandas as pd

@pandas_udf(returnType=StringType())
def vectorized_upper(series: pd.Series) -> pd.Series:
    return series.str.upper()

df.withColumn("upper_name", vectorized_upper(df.name))

# Built-in functions (fastest)
from pyspark.sql.functions import upper
df.withColumn("upper_name", upper(df.name))
```

### 24. How do you implement incremental data processing?
**Answer:**
```python
# Method 1: Using watermarks and timestamps
df_incremental = df.filter(col("timestamp") > last_processed_timestamp)

# Method 2: Using Delta Lake time travel
df_new = spark.read.format("delta").option("timestampAsOf", "2024-01-01").load("delta-table")
df_old = spark.read.format("delta").option("versionAsOf", 0).load("delta-table")
df_incremental = df_new.exceptAll(df_old)

# Method 3: Using checkpoint files
def process_incremental_data(checkpoint_path):
    # Read last checkpoint
    try:
        last_id = spark.read.text(checkpoint_path).collect()[0][0]
    except:
        last_id = 0
    
    # Process new data
    new_data = df.filter(col("id") > last_id)
    
    # Update checkpoint
    max_id = new_data.agg(max("id")).collect()[0][0]
    spark.createDataFrame([(str(max_id),)]).write.mode("overwrite").text(checkpoint_path)
    
    return new_data
```

### 25. What are the best practices for Spark application development?
**Answer:**
**Development Best Practices:**

```python
# 1. Use appropriate data formats
df.write.parquet("output")  # Columnar format for analytics

# 2. Partition data appropriately
df.write.partitionBy("year", "month").parquet("output")

# 3. Cache frequently accessed data
df.cache()  # or df.persist()

# 4. Use broadcast for small lookup tables
result = large_df.join(broadcast(small_df), "key")

# 5. Avoid collect() on large datasets
# Instead use write operations or take(n)

# 6. Use appropriate cluster sizing
# Rule of thumb: 2-4 cores per executor, 2-8GB memory per executor

# 7. Monitor and tune garbage collection
spark.conf.set("spark.executor.extraJavaOptions", "-XX:+UseG1GC -XX:MaxGCPauseMillis=200")

# 8. Use structured APIs (DataFrame/Dataset) over RDDs
# Better optimization and performance

# 9. Avoid UDFs when possible, use built-in functions
from pyspark.sql.functions import when, col
df.withColumn("category", when(col("age") < 18, "minor").otherwise("adult"))

# 10. Use appropriate join strategies
# Broadcast joins for small tables, sort-merge for large tables
```

## Intermediate Level Questions (26-50)

### 26. How do you optimize Spark jobs for better performance?
**Answer:**
```python
# 1. Proper partitioning
df.repartition(200)  # Increase parallelism
df.coalesce(10)      # Reduce partitions efficiently

# 2. Caching frequently used data
df.cache()
df.persist(StorageLevel.MEMORY_AND_DISK_SER)

# 3. Broadcast small tables
from pyspark.sql.functions import broadcast
large_df.join(broadcast(small_df), "key")

# 4. Use appropriate file formats
df.write.parquet("output")  # Columnar format
df.write.option("compression", "snappy").parquet("output")

# 5. Optimize joins
# Use bucketing for large joins
df.write.bucketBy(10, "user_id").saveAsTable("users_bucketed")

# 6. Configure Spark properly
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
```

### 27. Explain different types of joins in Spark and their performance characteristics
**Answer:**
```python
# 1. Broadcast Hash Join (fastest for small tables)
small_df = spark.table("small_table")  # < 10MB
large_df = spark.table("large_table")
result = large_df.join(broadcast(small_df), "key")

# 2. Sort Merge Join (default for large tables)
df1.join(df2, "key")  # Both tables are large

# 3. Shuffle Hash Join
spark.conf.set("spark.sql.join.preferSortMergeJoin", "false")

# Join optimization strategies
# Pre-partition data on join keys
df1.repartition("key").write.saveAsTable("table1_partitioned")
df2.repartition("key").write.saveAsTable("table2_partitioned")

# Use bucketing for repeated joins
df.write.bucketBy(10, "key").saveAsTable("bucketed_table")
```

### 11. How do you handle data skew in Spark?
**Answer:**
```python
# 1. Identify skewed data
df.groupBy("key").count().orderBy(col("count").desc()).show()

# 2. Salting technique for skewed joins
from pyspark.sql.functions import rand, col, concat, lit

# Add salt to skewed keys
salted_df1 = df1.withColumn("salted_key", 
    concat(col("key"), lit("_"), (rand() * 10).cast("int")))

# Replicate smaller table
salted_df2 = df2.select("*").crossJoin(
    spark.range(10).select(col("id").alias("salt")))
salted_df2 = salted_df2.withColumn("salted_key", 
    concat(col("key"), lit("_"), col("salt")))

# Join on salted keys
result = salted_df1.join(salted_df2, "salted_key")

# 3. Use adaptive query execution
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "256MB")
```

### 12. Explain Spark Streaming and its processing models
**Answer:**
```python
# Structured Streaming (recommended)
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("StreamingApp").getOrCreate()

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "topic") \
    .load()

# Process stream
processed_df = df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

# Windowed aggregation
windowed_counts = processed_df \
    .withWatermark("timestamp", "10 minutes") \
    .groupBy(
        window(col("timestamp"), "5 minutes"),
        col("event_type")
    ).count()

# Write stream
query = windowed_counts.writeStream \
    .outputMode("update") \
    .format("console") \
    .trigger(processingTime="10 seconds") \
    .start()

query.awaitTermination()
```

### 13. How do you implement checkpointing in Spark?
**Answer:**
```python
# RDD Checkpointing
sc.setCheckpointDir("hdfs://checkpoint")
rdd.checkpoint()  # Marks RDD for checkpointing
rdd.count()       # Triggers checkpointing

# Structured Streaming Checkpointing
query = df.writeStream \
    .format("delta") \
    .option("checkpointLocation", "/path/to/checkpoint") \
    .outputMode("append") \
    .start("/path/to/output")

# Custom checkpointing strategy
def checkpoint_strategy(df, checkpoint_interval=10):
    """Checkpoint every N transformations"""
    if hasattr(df, '_checkpoint_count'):
        df._checkpoint_count += 1
    else:
        df._checkpoint_count = 1
    
    if df._checkpoint_count % checkpoint_interval == 0:
        df.checkpoint()
    
    return df
```

### 14. Explain Spark's shuffle operations and how to optimize them
**Answer:**
```python
# Operations that cause shuffle
# groupBy, join, repartition, coalesce, distinct, etc.

# Shuffle optimization strategies
# 1. Reduce shuffle data
df.filter(condition).groupBy("key").count()  # Filter before groupBy

# 2. Increase parallelism
spark.conf.set("spark.sql.shuffle.partitions", "400")  # Default is 200

# 3. Use appropriate partitioning
df.repartition("key").write.partitionBy("date").parquet("output")

# 4. Optimize shuffle behavior
spark.conf.set("spark.shuffle.compress", "true")
spark.conf.set("spark.shuffle.spill.compress", "true")
spark.conf.set("spark.shuffle.service.enabled", "true")

# 5. Monitor shuffle metrics
def analyze_shuffle_metrics(spark_context):
    """Analyze shuffle read/write metrics"""
    status = spark_context.statusTracker()
    for stage in status.getActiveStages():
        print(f"Stage {stage.stageId}: "
              f"Shuffle Read: {stage.shuffleReadBytes}, "
              f"Shuffle Write: {stage.shuffleWriteBytes}")
```

### 15. How do you handle slowly changing dimensions (SCD) in Spark?
**Answer:**
```python
from delta.tables import DeltaTable

def implement_scd_type2(spark, source_df, target_path, business_key, scd_columns):
    """Implement SCD Type 2 using Delta Lake"""
    
    # Add SCD metadata
    source_with_meta = source_df.withColumn("effective_date", current_date()) \
                                .withColumn("end_date", lit(None).cast("date")) \
                                .withColumn("is_current", lit(True))
    
    if DeltaTable.isDeltaTable(spark, target_path):
        target_table = DeltaTable.forPath(spark, target_path)
        
        # Build change detection condition
        change_conditions = [f"target.{col} != source.{col}" for col in scd_columns]
        change_condition = " OR ".join(change_conditions)
        
        # Close current records that have changed
        target_table.alias("target").merge(
            source_with_meta.alias("source"),
            f"target.{business_key} = source.{business_key} AND target.is_current = true"
        ).whenMatchedUpdate(
            condition=change_condition,
            set={
                "end_date": "current_date()",
                "is_current": "false"
            }
        ).execute()
        
        # Insert new versions
        changed_records = source_with_meta.alias("source").join(
            target_table.toDF().filter(col("end_date") == current_date()).alias("target"),
            col(f"source.{business_key}") == col(f"target.{business_key}"),
            "inner"
        ).select("source.*")
        
        if changed_records.count() > 0:
            changed_records.write.format("delta").mode("append").save(target_path)
        
        # Insert completely new records
        target_table.alias("target").merge(
            source_with_meta.alias("source"),
            f"target.{business_key} = source.{business_key}"
        ).whenNotMatchedInsert(
            values={col: f"source.{col}" for col in source_with_meta.columns}
        ).execute()
    
    else:
        # Initial load
        source_with_meta.write.format("delta").save(target_path)

# Usage
implement_scd_type2(
    spark, 
    source_df, 
    "/delta/dim_customer",
    "customer_id",
    ["name", "email", "address"]
)
```

### 16. How do you implement data quality checks in Spark?
**Answer:**
```python
from pyspark.sql.functions import *

class DataQualityChecker:
    def __init__(self, spark):
        self.spark = spark
        self.results = []
    
    def check_null_values(self, df, columns, threshold=0.05):
        """Check for null values in specified columns"""
        total_count = df.count()
        
        for column in columns:
            null_count = df.filter(col(column).isNull()).count()
            null_percentage = null_count / total_count
            
            self.results.append({
                "check": f"null_check_{column}",
                "passed": null_percentage <= threshold,
                "value": null_percentage,
                "threshold": threshold
            })
    
    def check_duplicates(self, df, key_columns):
        """Check for duplicate records"""
        total_count = df.count()
        distinct_count = df.dropDuplicates(key_columns).count()
        duplicate_count = total_count - distinct_count
        
        self.results.append({
            "check": "duplicate_check",
            "passed": duplicate_count == 0,
            "value": duplicate_count,
            "threshold": 0
        })
    
    def check_data_freshness(self, df, date_column, max_age_hours=24):
        """Check data freshness"""
        max_date = df.agg(max(date_column)).collect()[0][0]
        hours_old = (datetime.now() - max_date).total_seconds() / 3600
        
        self.results.append({
            "check": "freshness_check",
            "passed": hours_old <= max_age_hours,
            "value": hours_old,
            "threshold": max_age_hours
        })
    
    def check_referential_integrity(self, child_df, parent_df, foreign_key, primary_key):
        """Check referential integrity"""
        orphaned_records = child_df.join(
            parent_df, 
            child_df[foreign_key] == parent_df[primary_key], 
            "left_anti"
        ).count()
        
        self.results.append({
            "check": "referential_integrity",
            "passed": orphaned_records == 0,
            "value": orphaned_records,
            "threshold": 0
        })
    
    def get_results(self):
        """Return data quality results as DataFrame"""
        return self.spark.createDataFrame(self.results)

# Usage
dq_checker = DataQualityChecker(spark)
dq_checker.check_null_values(df, ["customer_id", "email"])
dq_checker.check_duplicates(df, ["customer_id"])
dq_checker.check_data_freshness(df, "created_date")

results_df = dq_checker.get_results()
results_df.show()
```

## Advanced Level Questions (17-20)

### 17. How do you implement a custom data source in Spark?
**Answer:**
```python
# Custom data source implementation
from pyspark.sql.datasource import DataSource, DataSourceReader
from pyspark.sql.types import *

class CustomDataSource(DataSource):
    """Custom data source for reading proprietary format"""
    
    @classmethod
    def name(cls):
        return "custom-format"
    
    def schema(self):
        return StructType([
            StructField("id", IntegerType(), True),
            StructField("name", StringType(), True),
            StructField("value", DoubleType(), True)
        ])
    
    def reader(self, schema):
        return CustomDataSourceReader(schema, self.options)

class CustomDataSourceReader(DataSourceReader):
    def __init__(self, schema, options):
        self.schema = schema
        self.options = options
    
    def read(self, partition):
        # Custom logic to read data
        # Return iterator of Row objects
        for i in range(100):
            yield Row(id=i, name=f"name_{i}", value=float(i * 2))

# Register custom data source
spark.conf.set("spark.sql.sources.custom-format", 
               "path.to.CustomDataSource")

# Use custom data source
df = spark.read.format("custom-format").load()
```

### 18. Implement a complex ETL pipeline with error handling and monitoring
**Answer:**
```python
import logging
from datetime import datetime
from pyspark.sql.functions import *

class SparkETLPipeline:
    def __init__(self, spark, config):
        self.spark = spark
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.metrics = {}
    
    def extract(self, source_config):
        """Extract data from multiple sources"""
        try:
            self.logger.info(f"Starting extraction from {source_config['type']}")
            start_time = datetime.now()
            
            if source_config['type'] == 'jdbc':
                df = self.spark.read.format("jdbc") \
                    .option("url", source_config['url']) \
                    .option("dbtable", source_config['table']) \
                    .option("user", source_config['user']) \
                    .option("password", source_config['password']) \
                    .load()
            
            elif source_config['type'] == 'kafka':
                df = self.spark.readStream \
                    .format("kafka") \
                    .option("kafka.bootstrap.servers", source_config['servers']) \
                    .option("subscribe", source_config['topic']) \
                    .load()
            
            else:
                df = self.spark.read.format(source_config['format']) \
                    .load(source_config['path'])
            
            # Add extraction metadata
            df = df.withColumn("extraction_timestamp", current_timestamp()) \
                   .withColumn("source_system", lit(source_config['name']))
            
            extraction_time = (datetime.now() - start_time).total_seconds()
            self.metrics['extraction_time'] = extraction_time
            self.metrics['extracted_records'] = df.count()
            
            self.logger.info(f"Extracted {self.metrics['extracted_records']} records in {extraction_time}s")
            return df
            
        except Exception as e:
            self.logger.error(f"Extraction failed: {str(e)}")
            self._log_error("extraction", str(e))
            raise
    
    def transform(self, df, transformations):
        """Apply transformations with error handling"""
        try:
            self.logger.info("Starting transformations")
            start_time = datetime.now()
            
            for transform in transformations:
                if transform['type'] == 'filter':
                    df = df.filter(transform['condition'])
                
                elif transform['type'] == 'aggregate':
                    df = df.groupBy(*transform['group_by']) \
                           .agg(*[eval(agg) for agg in transform['aggregations']])
                
                elif transform['type'] == 'join':
                    other_df = self.spark.table(transform['table'])
                    df = df.join(other_df, transform['condition'], transform.get('how', 'inner'))
                
                elif transform['type'] == 'custom':
                    df = transform['function'](df)
            
            # Data quality validation
            df = self._validate_data_quality(df)
            
            transformation_time = (datetime.now() - start_time).total_seconds()
            self.metrics['transformation_time'] = transformation_time
            self.metrics['transformed_records'] = df.count()
            
            self.logger.info(f"Transformed to {self.metrics['transformed_records']} records in {transformation_time}s")
            return df
            
        except Exception as e:
            self.logger.error(f"Transformation failed: {str(e)}")
            self._log_error("transformation", str(e))
            raise
    
    def load(self, df, target_config):
        """Load data to target with error handling"""
        try:
            self.logger.info(f"Starting load to {target_config['type']}")
            start_time = datetime.now()
            
            if target_config['type'] == 'delta':
                df.write.format("delta") \
                  .mode(target_config.get('mode', 'append')) \
                  .option("mergeSchema", "true") \
                  .save(target_config['path'])
            
            elif target_config['type'] == 'jdbc':
                df.write.format("jdbc") \
                  .option("url", target_config['url']) \
                  .option("dbtable", target_config['table']) \
                  .option("user", target_config['user']) \
                  .option("password", target_config['password']) \
                  .mode(target_config.get('mode', 'append')) \
                  .save()
            
            load_time = (datetime.now() - start_time).total_seconds()
            self.metrics['load_time'] = load_time
            
            self.logger.info(f"Loaded data in {load_time}s")
            
        except Exception as e:
            self.logger.error(f"Load failed: {str(e)}")
            self._log_error("load", str(e))
            raise
    
    def _validate_data_quality(self, df):
        """Validate data quality"""
        # Check for null values in critical columns
        critical_columns = self.config.get('critical_columns', [])
        for column in critical_columns:
            null_count = df.filter(col(column).isNull()).count()
            if null_count > 0:
                self.logger.warning(f"Found {null_count} null values in {column}")
        
        # Check for duplicates
        total_count = df.count()
        distinct_count = df.dropDuplicates().count()
        if total_count != distinct_count:
            self.logger.warning(f"Found {total_count - distinct_count} duplicate records")
        
        return df
    
    def _log_error(self, stage, error_message):
        """Log errors to monitoring system"""
        error_record = {
            "pipeline_name": self.config['name'],
            "stage": stage,
            "error_message": error_message,
            "timestamp": datetime.now(),
            "metrics": self.metrics
        }
        
        error_df = self.spark.createDataFrame([error_record])
        error_df.write.format("delta").mode("append").save("/delta/monitoring/pipeline_errors")
    
    def run(self):
        """Run complete ETL pipeline"""
        try:
            # Extract
            df = self.extract(self.config['source'])
            
            # Transform
            df = self.transform(df, self.config['transformations'])
            
            # Load
            self.load(df, self.config['target'])
            
            # Log success metrics
            self._log_success_metrics()
            
        except Exception as e:
            self.logger.error(f"Pipeline failed: {str(e)}")
            raise
    
    def _log_success_metrics(self):
        """Log successful pipeline metrics"""
        metrics_record = {
            "pipeline_name": self.config['name'],
            "status": "success",
            "timestamp": datetime.now(),
            **self.metrics
        }
        
        metrics_df = self.spark.createDataFrame([metrics_record])
        metrics_df.write.format("delta").mode("append").save("/delta/monitoring/pipeline_metrics")

# Usage
config = {
    "name": "customer_etl",
    "source": {
        "type": "jdbc",
        "url": "jdbc:postgresql://localhost:5432/source",
        "table": "customers",
        "user": "user",
        "password": "password"
    },
    "transformations": [
        {"type": "filter", "condition": "age > 18"},
        {"type": "aggregate", "group_by": ["city"], "aggregations": ["count(*)"]}
    ],
    "target": {
        "type": "delta",
        "path": "/delta/customers",
        "mode": "overwrite"
    },
    "critical_columns": ["customer_id", "email"]
}

pipeline = SparkETLPipeline(spark, config)
pipeline.run()
```

### 19. How do you implement machine learning pipelines in Spark?
**Answer:**
```python
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler, StringIndexer, StandardScaler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

def create_ml_pipeline(spark):
    """Create comprehensive ML pipeline"""
    
    # Load data
    df = spark.read.parquet("/data/customer_features.parquet")
    
    # Feature engineering pipeline
    # Handle categorical variables
    indexers = [StringIndexer(inputCol=col, outputCol=f"{col}_indexed")
                for col in ["category", "region", "segment"]]
    
    # Assemble features
    feature_cols = ["age", "income", "category_indexed", "region_indexed", "segment_indexed"]
    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features_raw")
    
    # Scale features
    scaler = StandardScaler(inputCol="features_raw", outputCol="features")
    
    # Model
    rf = RandomForestClassifier(featuresCol="features", labelCol="label")
    
    # Create pipeline
    pipeline = Pipeline(stages=indexers + [assembler, scaler, rf])
    
    # Split data
    train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)
    
    # Hyperparameter tuning
    paramGrid = ParamGridBuilder() \
        .addGrid(rf.numTrees, [10, 20, 30]) \
        .addGrid(rf.maxDepth, [5, 10, 15]) \
        .build()
    
    evaluator = BinaryClassificationEvaluator()
    
    crossval = CrossValidator(estimator=pipeline,
                             estimatorParamMaps=paramGrid,
                             evaluator=evaluator,
                             numFolds=3)
    
    # Train model
    cv_model = crossval.fit(train_df)
    
    # Make predictions
    predictions = cv_model.transform(test_df)
    
    # Evaluate model
    auc = evaluator.evaluate(predictions)
    print(f"AUC: {auc}")
    
    # Save model
    cv_model.write().overwrite().save("/models/customer_churn_model")
    
    return cv_model, predictions

# Feature store integration
def create_feature_store_pipeline(spark):
    """Create features for ML feature store"""
    
    # Customer features
    customer_features = spark.sql("""
        SELECT 
            customer_id,
            age,
            income,
            registration_date,
            DATEDIFF(current_date(), registration_date) as days_since_registration,
            CASE 
                WHEN age < 25 THEN 'Young'
                WHEN age < 45 THEN 'Middle'
                ELSE 'Senior'
            END as age_group
        FROM customers
    """)
    
    # Transaction features
    transaction_features = spark.sql("""
        SELECT 
            customer_id,
            COUNT(*) as total_transactions,
            SUM(amount) as total_spent,
            AVG(amount) as avg_transaction_amount,
            MAX(transaction_date) as last_transaction_date,
            DATEDIFF(current_date(), MAX(transaction_date)) as days_since_last_transaction
        FROM transactions
        WHERE transaction_date >= date_sub(current_date(), 90)
        GROUP BY customer_id
    """)
    
    # Join features
    features = customer_features.join(transaction_features, "customer_id", "left")
    
    # Write to feature store
    features.write.format("delta").mode("overwrite").save("/feature_store/customer_features")
    
    return features

# Real-time scoring
def create_streaming_ml_pipeline(spark):
    """Create streaming ML pipeline for real-time scoring"""
    
    # Load trained model
    from pyspark.ml import PipelineModel
    model = PipelineModel.load("/models/customer_churn_model")
    
    # Read streaming data
    streaming_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "customer_events") \
        .load()
    
    # Parse and prepare features
    parsed_df = streaming_df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")
    
    # Apply model
    predictions = model.transform(parsed_df)
    
    # Write predictions
    query = predictions.select("customer_id", "prediction", "probability") \
        .writeStream \
        .format("delta") \
        .outputMode("append") \
        .option("checkpointLocation", "/checkpoints/ml_predictions") \
        .start("/delta/ml_predictions")
    
    return query

# Usage
model, predictions = create_ml_pipeline(spark)
features = create_feature_store_pipeline(spark)
streaming_query = create_streaming_ml_pipeline(spark)
```

### 20. How do you monitor and debug Spark applications in production?
**Answer:**
```python
import json
from datetime import datetime

class SparkMonitor:
    def __init__(self, spark):
        self.spark = spark
        self.sc = spark.sparkContext
    
    def get_application_metrics(self):
        """Get comprehensive application metrics"""
        status = self.sc.statusTracker()
        
        metrics = {
            "application_id": self.sc.applicationId,
            "application_name": self.sc.appName,
            "start_time": datetime.fromtimestamp(self.sc.startTime / 1000),
            "executor_infos": status.getExecutorInfos(),
            "active_stages": len(status.getActiveStages()),
            "active_jobs": len(status.getActiveJobIds()),
            "total_cores": sum([e.totalCores for e in status.getExecutorInfos()]),
            "total_memory": sum([e.maxMemory for e in status.getExecutorInfos()])
        }
        
        return metrics
    
    def analyze_stage_performance(self):
        """Analyze stage-level performance"""
        status = self.sc.statusTracker()
        
        stage_metrics = []
        for stage in status.getActiveStages():
            stage_info = {
                "stage_id": stage.stageId,
                "name": stage.name,
                "num_tasks": stage.numTasks,
                "num_active_tasks": stage.numActiveTasks,
                "num_complete_tasks": stage.numCompleteTasks,
                "num_failed_tasks": stage.numFailedTasks,
                "executor_run_time": stage.executorRunTime,
                "executor_cpu_time": stage.executorCpuTime,
                "shuffle_read_bytes": stage.shuffleReadBytes,
                "shuffle_write_bytes": stage.shuffleWriteBytes,
                "input_bytes": stage.inputBytes,
                "output_bytes": stage.outputBytes
            }
            stage_metrics.append(stage_info)
        
        return stage_metrics
    
    def detect_performance_issues(self):
        """Detect common performance issues"""
        issues = []
        
        # Check for data skew
        stage_metrics = self.analyze_stage_performance()
        for stage in stage_metrics:
            if stage['shuffle_read_bytes'] > 1024**3:  # > 1GB
                issues.append({
                    "type": "large_shuffle",
                    "stage_id": stage['stage_id'],
                    "shuffle_bytes": stage['shuffle_read_bytes'],
                    "recommendation": "Consider repartitioning or using broadcast joins"
                })
        
        # Check executor utilization
        app_metrics = self.get_application_metrics()
        if len(app_metrics['executor_infos']) > 1:
            cpu_utilization = []
            for executor in app_metrics['executor_infos']:
                if executor.totalCores > 0:
                    utilization = executor.activeTasks / executor.totalCores
                    cpu_utilization.append(utilization)
            
            avg_utilization = sum(cpu_utilization) / len(cpu_utilization)
            if avg_utilization < 0.5:
                issues.append({
                    "type": "low_cpu_utilization",
                    "avg_utilization": avg_utilization,
                    "recommendation": "Consider reducing number of executors or increasing parallelism"
                })
        
        return issues
    
    def log_metrics_to_monitoring_system(self):
        """Log metrics to external monitoring system"""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "application_metrics": self.get_application_metrics(),
            "stage_metrics": self.analyze_stage_performance(),
            "performance_issues": self.detect_performance_issues()
        }
        
        # Convert to DataFrame and save
        metrics_df = self.spark.createDataFrame([metrics])
        metrics_df.write.format("delta").mode("append").save("/delta/monitoring/spark_metrics")
        
        return metrics
    
    def setup_custom_metrics(self):
        """Setup custom metrics collection"""
        # Custom accumulator for business metrics
        record_counter = self.sc.accumulator(0)
        error_counter = self.sc.accumulator(0)
        
        def process_with_metrics(partition):
            """Process partition with custom metrics"""
            processed_records = 0
            errors = 0
            
            for record in partition:
                try:
                    # Process record
                    yield process_record(record)
                    processed_records += 1
                except Exception as e:
                    errors += 1
                    # Log error
                    yield {"error": str(e), "record": record}
            
            # Update accumulators
            record_counter.add(processed_records)
            error_counter.add(errors)
        
        return record_counter, error_counter, process_with_metrics

# Usage and monitoring setup
def setup_production_monitoring(spark):
    """Setup comprehensive production monitoring"""
    
    monitor = SparkMonitor(spark)
    
    # Enable Spark metrics
    spark.conf.set("spark.metrics.conf.*.sink.console.class", 
                   "org.apache.spark.metrics.sink.ConsoleSink")
    spark.conf.set("spark.metrics.conf.*.sink.console.period", "10")
    
    # Setup custom listeners
    class CustomSparkListener:
        def onApplicationStart(self, applicationStart):
            print(f"Application started: {applicationStart.appName}")
        
        def onJobEnd(self, jobEnd):
            if jobEnd.jobResult.isInstanceOf("JobFailed"):
                print(f"Job failed: {jobEnd.jobId}")
        
        def onStageCompleted(self, stageCompleted):
            stage_info = stageCompleted.stageInfo
            print(f"Stage {stage_info.stageId} completed in {stage_info.taskTime}ms")
    
    # Add listener
    spark.sparkContext.addSparkListener(CustomSparkListener())
    
    # Periodic monitoring
    def periodic_monitoring():
        """Run periodic monitoring checks"""
        metrics = monitor.log_metrics_to_monitoring_system()
        
        # Check for critical issues
        issues = monitor.detect_performance_issues()
        if issues:
            # Send alerts
            for issue in issues:
                if issue['type'] == 'large_shuffle':
                    send_alert(f"Large shuffle detected in stage {issue['stage_id']}")
    
    return monitor, periodic_monitoring

# Error handling and recovery
def implement_error_recovery(spark):
    """Implement error recovery strategies"""
    
    def resilient_processing(df, process_func, max_retries=3):
        """Process data with automatic retry on failure"""
        
        for attempt in range(max_retries):
            try:
                result = process_func(df)
                return result
            except Exception as e:
                if attempt == max_retries - 1:
                    # Log final failure
                    error_df = spark.createDataFrame([{
                        "error_type": type(e).__name__,
                        "error_message": str(e),
                        "attempt": attempt + 1,
                        "timestamp": datetime.now()
                    }])
                    error_df.write.format("delta").mode("append").save("/delta/errors")
                    raise e
                else:
                    print(f"Attempt {attempt + 1} failed, retrying...")
                    time.sleep(2 ** attempt)  # Exponential backoff
    
    return resilient_processing

# Usage
monitor, periodic_monitoring = setup_production_monitoring(spark)
resilient_processing = implement_error_recovery(spark)

# Run monitoring
metrics = monitor.log_metrics_to_monitoring_system()
periodic_monitoring()
```