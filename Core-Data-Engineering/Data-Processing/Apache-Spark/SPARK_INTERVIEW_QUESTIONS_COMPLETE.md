# Apache Spark Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-30)](#basic-level-questions-1-30)
2. [Intermediate Level Questions (31-60)](#intermediate-level-questions-31-60)
3. [Advanced Level Questions (61-90)](#advanced-level-questions-61-90)
4. [Architecture & Performance (91-120)](#architecture--performance-91-120)
5. [Streaming & Real-time Processing (121-150)](#streaming--real-time-processing-121-150)
6. [Production & Operations (151-180)](#production--operations-151-180)
7. [Scenario-Based Questions (181-200)](#scenario-based-questions-181-200)

---

## Basic Level Questions (1-30)

### 1. What is Apache Spark and how does it differ from Hadoop MapReduce?

### 🎯 **Theoretical Foundation**

#### **Core Concepts**
- **In-Memory Computing**: Stores intermediate data in memory rather than disk for 100x speed improvement
- **Directed Acyclic Graph (DAG)**: Optimizes execution plans through intelligent task scheduling
- **Resilient Distributed Datasets (RDDs)**: Fault-tolerant distributed data structures with lineage tracking
- **Unified Engine**: Single platform for batch, streaming, ML, and graph processing
- **Lazy Evaluation**: Defers execution until actions are called, enabling optimization

#### **Historical Context**
- **2009**: Created at UC Berkeley AMPLab by Matei Zaharia
- **2010**: Open-sourced under BSD license
- **2013**: Became Apache top-level project
- **2014**: Spark 1.0 with Spark SQL and MLlib
- **2016**: Spark 2.0 with unified Dataset API
- **2020**: Spark 3.0 with adaptive query execution
- **2023**: Spark 3.4 with improved streaming and ML capabilities

#### **Architectural Principles**
- **Fault Tolerance**: Automatic recovery through RDD lineage without checkpointing
- **Horizontal Scalability**: Linear scaling across thousands of nodes
- **Multi-Language Support**: APIs in Scala, Java, Python, R, and SQL
- **Pluggable Architecture**: Support for multiple cluster managers and storage systems
- **Catalyst Optimizer**: Rule-based and cost-based query optimization

### 📈 **Comparative Analysis**

#### **Big Data Processing Framework Comparison Matrix**
| Feature | Apache Spark | Hadoop MapReduce | Apache Flink | Apache Storm |
|---------|--------------|------------------|--------------|---------------|
| **Processing Model** | Batch + Streaming | Batch only | Streaming-first | Stream only |
| **Memory Usage** | In-memory caching | Disk-based | Memory + disk | Memory-based |
| **Latency** | Sub-second | Minutes | Milliseconds | Milliseconds |
| **Fault Tolerance** | RDD lineage | Task restart | Checkpointing | At-least-once |
| **API Complexity** | High-level APIs | Low-level | Medium-level | Low-level |
| **Machine Learning** | MLlib built-in | External tools | FlinkML | None |
| **SQL Support** | Spark SQL | Hive integration | Flink SQL | None |
| **Ecosystem** | Very mature | Very mature | Growing | Limited |
| **Learning Curve** | Medium | High | High | Medium |
| **Resource Usage** | High memory | Low memory | Medium | Low |

#### **Performance Benchmarks**
```
Spark vs MapReduce Performance (100GB dataset):
┌─────────────────┬──────────────┬──────────────┬──────────────┐
| Workload        | Spark        | MapReduce    | Speedup      |
├─────────────────┼──────────────┼──────────────┼──────────────┤
| Word Count      | 2 minutes    | 15 minutes   | 7.5x         |
| Sort            | 3 minutes    | 45 minutes   | 15x          |
| Iterative ML    | 5 minutes    | 2 hours      | 24x          |
| Graph Analytics | 8 minutes    | 4 hours      | 30x          |
| Complex ETL     | 12 minutes   | 3 hours      | 15x          |
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

**Answer:**
Apache Spark is a unified analytics engine for large-scale data processing that has revolutionized big data processing.

**Key Differences:**
- **Speed**: Spark is 100x faster than MapReduce due to in-memory computing
- **Ease of Use**: High-level APIs in Java, Scala, Python, and R
- **Unified Platform**: Single platform for batch, streaming, ML, and graph processing
- **Memory Management**: Intelligent caching and memory management

```python
# Spark example - simple and fast
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("DataProcessing").getOrCreate()

df = spark.read.csv("data.csv", header=True, inferSchema=True)
result = df.filter(df.age > 25).groupBy("department").count()
result.show()
```

### 2. Explain Spark's architecture and core components

### 🎯 **Theoretical Foundation**

#### **Core Concepts**
- **Master-Worker Architecture**: Driver coordinates work across distributed executors
- **Resource Management**: Pluggable cluster managers handle resource allocation
- **Task Scheduling**: DAG scheduler optimizes task execution across stages
- **Data Locality**: Scheduler attempts to run tasks close to data
- **Dynamic Resource Allocation**: Automatically scales executors based on workload

#### **Component Interaction Flow**
```
Spark Architecture Data Flow:
┌────────────────────┬────────────────┬────────────────┐
| Component           | Responsibility     | Resource Usage   |
├────────────────────┼────────────────┼────────────────┤
| Driver Program      | Job coordination   | 1-4 GB RAM       |
| └─ SparkContext    | Entry point        | Minimal          |
| └─ DAG Scheduler   | Stage planning     | CPU intensive    |
| └─ Task Scheduler  | Task distribution  | Network I/O      |
| Cluster Manager     | Resource mgmt      | Varies by type   |
| └─ YARN           | Hadoop integration | 512MB-2GB        |
| └─ Kubernetes     | Container orchest  | 1-2GB            |
| └─ Standalone     | Simple deployment  | Minimal          |
| Executors           | Task execution     | 2-64GB RAM       |
| └─ JVM Process    | Isolated execution | High memory      |
| └─ Block Manager  | Data storage       | Memory + disk    |
| └─ Task Threads   | Parallel execution | CPU cores        |
└────────────────────┴────────────────┴────────────────┘
```

#### **Execution Model**
```
Spark Job Execution Lifecycle:
1. Application Submission → Driver Program Created
2. SparkContext Creation → Cluster Manager Contact
3. Resource Allocation → Executors Launched
4. Code Distribution → JAR/Python files sent
5. Task Scheduling → DAG → Stages → Tasks
6. Task Execution → Data Processing
7. Result Collection → Driver aggregates results
8. Resource Cleanup → Executors terminated
```

**Answer:**
**Core Components:**
- **Driver Program**: Coordinates the application and manages SparkContext
- **Cluster Manager**: Manages resources (YARN, Mesos, Kubernetes)
- **Executors**: Run tasks and store data across cluster nodes
- **Tasks**: Units of work sent to executors

```python
# SparkContext configuration
from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName("MyApp").setMaster("local[*]")
sc = SparkContext(conf=conf)

# Create RDD and process
rdd = sc.parallelize([1, 2, 3, 4, 5])
result = rdd.map(lambda x: x * 2).collect()
```

### 3. What are RDDs and their key characteristics?
**Answer:**
RDD (Resilient Distributed Dataset) is Spark's fundamental data structure.

**Key Characteristics:**
- **Immutable**: Cannot be changed after creation
- **Distributed**: Partitioned across cluster nodes
- **Fault-tolerant**: Automatically recovers from failures using lineage
- **Lazy Evaluation**: Computations deferred until action is called

```python
# RDD operations example
rdd = sc.textFile("file.txt")

# Transformations (lazy)
words = rdd.flatMap(lambda line: line.split(" "))
word_counts = words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

# Action (triggers execution)
results = word_counts.collect()
```

### 4. Explain the difference between transformations and actions
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
# Transformations (lazy)
df_filtered = df.filter(df.age > 25)  # Not executed
df_grouped = df_filtered.groupBy("department").count()  # Not executed

# Actions (trigger execution)
df_grouped.show()  # Executes entire pipeline
count = df.count()  # Executes computation
```

### 5. What is the Catalyst Optimizer?
**Answer:**
Catalyst is Spark SQL's query optimizer that uses rule-based optimization.

**Optimization Phases:**
1. **Logical Plan**: Parse SQL to logical plan
2. **Optimized Logical Plan**: Apply optimization rules
3. **Physical Plan**: Generate physical execution plans
4. **Code Generation**: Generate Java bytecode

```python
# Enable optimizations
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
```

### 7. What are the different cluster managers supported by Spark?
**Answer:**
**Cluster Managers:**
- **Standalone**: Spark's built-in cluster manager
- **YARN**: Hadoop's resource manager
- **Mesos**: General-purpose cluster manager
- **Kubernetes**: Container orchestration platform

```bash
# Different deployment modes
spark-submit --master spark://master:7077 app.py  # Standalone
spark-submit --master yarn --deploy-mode cluster app.py  # YARN
spark-submit --master k8s://https://kubernetes-api app.py  # Kubernetes
```

### 8. Explain lazy evaluation and its benefits
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

# Execution happens only here
results = rdd3.collect()
```

### 9. What are the different deployment modes?
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

### 10. What are the different storage levels in Spark?
**Answer:**
```python
from pyspark import StorageLevel

# Memory only (default for cache())
df.persist(StorageLevel.MEMORY_ONLY)

# Memory and disk
df.persist(StorageLevel.MEMORY_AND_DISK)

# Serialized in memory (more compact)
df.persist(StorageLevel.MEMORY_ONLY_SER)

# Disk only
df.persist(StorageLevel.DISK_ONLY)

# With replication
df.persist(StorageLevel.MEMORY_AND_DISK_2)
```

### 11. How does Spark handle fault tolerance?
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

### 12. What is the difference between DataFrame and Dataset?
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

### 13. What are accumulators and broadcast variables?
**Answer:**
```python
# Accumulators - write-only variables for aggregating information
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

### 14. How do you handle the small files problem?
**Answer:**
```python
# Problem: Many small files cause performance issues

# Solution 1: Coalesce partitions
df.coalesce(1).write.parquet("output")

# Solution 2: Repartition before writing
df.repartition(10).write.parquet("output")

# Solution 3: Use maxRecordsPerFile
df.write.option("maxRecordsPerFile", 100000).parquet("output")

# Solution 4: Configure partition size
spark.conf.set("spark.sql.files.maxPartitionBytes", "134217728")  # 128MB
```

### 15. What is Dynamic Allocation?
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

---

## Intermediate Level Questions (31-60)

### 31. How do you optimize Spark jobs for better performance?
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

# 5. Configure Spark properly
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
```

### 32. Explain different types of joins and their performance characteristics
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

# Use bucketing for repeated joins
df.write.bucketBy(10, "key").saveAsTable("bucketed_table")
```

### 33. How do you handle data skew in Spark?
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
```

### 34. How do you implement incremental data processing?
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

### 35. What are User Defined Functions (UDFs) and their performance implications?
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

---

## Advanced Level Questions (61-90)

### 61. How do you implement a complex ETL pipeline with error handling?
**Answer:**
```python
import logging
from datetime import datetime

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
                    .load()
            else:
                df = self.spark.read.format(source_config['format']) \
                    .load(source_config['path'])
            
            # Add extraction metadata
            df = df.withColumn("extraction_timestamp", current_timestamp())
            
            extraction_time = (datetime.now() - start_time).total_seconds()
            self.metrics['extraction_time'] = extraction_time
            self.metrics['extracted_records'] = df.count()
            
            return df
            
        except Exception as e:
            self.logger.error(f"Extraction failed: {str(e)}")
            self._log_error("extraction", str(e))
            raise
    
    def transform(self, df, transformations):
        """Apply transformations with error handling"""
        try:
            for transform in transformations:
                if transform['type'] == 'filter':
                    df = df.filter(transform['condition'])
                elif transform['type'] == 'aggregate':
                    df = df.groupBy(*transform['group_by']) \
                           .agg(*[eval(agg) for agg in transform['aggregations']])
            
            # Data quality validation
            df = self._validate_data_quality(df)
            return df
            
        except Exception as e:
            self.logger.error(f"Transformation failed: {str(e)}")
            raise
    
    def _validate_data_quality(self, df):
        """Validate data quality"""
        critical_columns = self.config.get('critical_columns', [])
        for column in critical_columns:
            null_count = df.filter(col(column).isNull()).count()
            if null_count > 0:
                self.logger.warning(f"Found {null_count} null values in {column}")
        return df
```

### 62. How do you implement slowly changing dimensions (SCD) in Spark?
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
        
        # Insert new versions for changed records
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

---

## Streaming & Real-time Processing (121-150)

### 121. How do you implement Structured Streaming for real-time analytics?
**Answer:**
```python
from pyspark.sql.functions import *

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

# Real-time aggregations with watermarking
windowed_counts = parsed_df \
    .withWatermark("timestamp", "10 minutes") \
    .groupBy(
        window(col("timestamp"), "5 minutes", "1 minute"),
        col("event_type")
    ).count()

# Write to multiple sinks
query1 = windowed_counts.writeStream \
    .outputMode("update") \
    .format("console") \
    .trigger(processingTime="10 seconds") \
    .start()

query2 = windowed_counts.writeStream \
    .outputMode("update") \
    .format("delta") \
    .option("checkpointLocation", "/checkpoints/events") \
    .start("/delta/event_counts")

# Wait for termination
query1.awaitTermination()
```

### 122. How do you handle late arriving data in streaming?
**Answer:**
```python
# Configure watermarking for late data
df_with_watermark = streaming_df \
    .withWatermark("event_time", "30 minutes")  # Allow 30 min late data

# Windowed aggregation with late data handling
result = df_with_watermark \
    .groupBy(
        window(col("event_time"), "10 minutes"),
        col("user_id")
    ) \
    .agg(
        count("*").alias("event_count"),
        sum("amount").alias("total_amount")
    )

# Output modes for handling updates
query = result.writeStream \
    .outputMode("update")  # Only output updated results \
    .format("delta") \
    .option("checkpointLocation", "/checkpoints/late_data") \
    .start("/delta/user_metrics")
```

---

## Production & Operations (151-180)

### 151. How do you monitor Spark applications in production?
**Answer:**
```python
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
            "active_jobs": len(status.getActiveJobIds())
        }
        
        return metrics
    
    def detect_performance_issues(self):
        """Detect common performance issues"""
        issues = []
        
        # Check for large shuffles
        stage_metrics = self.analyze_stage_performance()
        for stage in stage_metrics:
            if stage['shuffle_read_bytes'] > 1024**3:  # > 1GB
                issues.append({
                    "type": "large_shuffle",
                    "stage_id": stage['stage_id'],
                    "recommendation": "Consider repartitioning or broadcast joins"
                })
        
        return issues

# Usage
monitor = SparkMonitor(spark)
metrics = monitor.get_application_metrics()
issues = monitor.detect_performance_issues()
```

### 152. How do you implement auto-scaling for Spark clusters?
**Answer:**
```python
# Dynamic allocation configuration
spark.conf.set("spark.dynamicAllocation.enabled", "true")
spark.conf.set("spark.dynamicAllocation.minExecutors", "2")
spark.conf.set("spark.dynamicAllocation.maxExecutors", "100")
spark.conf.set("spark.dynamicAllocation.initialExecutors", "10")

# Scaling policies
spark.conf.set("spark.dynamicAllocation.executorIdleTimeout", "60s")
spark.conf.set("spark.dynamicAllocation.cachedExecutorIdleTimeout", "300s")
spark.conf.set("spark.dynamicAllocation.schedulerBacklogTimeout", "1s")
spark.conf.set("spark.dynamicAllocation.sustainedSchedulerBacklogTimeout", "5s")

# Custom scaling logic
def custom_scaling_logic(current_load, target_utilization=0.8):
    """Implement custom scaling based on workload"""
    if current_load > target_utilization:
        # Scale up
        return min(current_executors * 2, max_executors)
    elif current_load < target_utilization * 0.5:
        # Scale down
        return max(current_executors // 2, min_executors)
    return current_executors
```

---

## Scenario-Based Questions (181-200)

### 181. You have a 10TB dataset that needs to be processed daily. How would you design the Spark job?
**Answer:**
```python
# Design considerations for 10TB daily processing

# 1. Cluster sizing
# Assume 100GB per executor, need 100 executors
# With 4 cores per executor = 400 total cores
# Memory: 8GB per executor = 800GB total memory

spark_config = {
    "spark.executor.instances": "100",
    "spark.executor.cores": "4",
    "spark.executor.memory": "8g",
    "spark.executor.memoryOverhead": "1g",
    "spark.driver.memory": "4g",
    "spark.driver.maxResultSize": "2g"
}

# 2. Partitioning strategy
# Target 128MB per partition = ~80,000 partitions for 10TB
df = spark.read.parquet("s3://data/daily/")
df = df.repartition(80000)  # Or based on date columns

# 3. Incremental processing
def process_daily_data(date):
    """Process data for specific date"""
    daily_df = spark.read.parquet(f"s3://data/daily/date={date}")
    
    # Apply transformations
    processed_df = daily_df.filter(col("status") == "active") \
                           .groupBy("category", "region") \
                           .agg(sum("amount").alias("total_amount"))
    
    # Write with partitioning
    processed_df.write \
                .mode("overwrite") \
                .partitionBy("region") \
                .parquet(f"s3://processed/date={date}")

# 4. Error handling and monitoring
def robust_daily_processing(date, max_retries=3):
    """Process with retry logic"""
    for attempt in range(max_retries):
        try:
            process_daily_data(date)
            log_success_metrics(date, attempt + 1)
            break
        except Exception as e:
            if attempt == max_retries - 1:
                log_failure(date, str(e))
                raise
            time.sleep(60 * (attempt + 1))  # Exponential backoff
```

### 182. How would you optimize a Spark job that's running out of memory?
**Answer:**
```python
# Memory optimization strategies

# 1. Identify memory bottlenecks
def analyze_memory_usage(spark_context):
    """Analyze memory usage patterns"""
    status = spark_context.statusTracker()
    
    for executor in status.getExecutorInfos():
        memory_used = executor.memoryUsed
        max_memory = executor.maxMemory
        utilization = memory_used / max_memory
        
        if utilization > 0.9:
            print(f"Executor {executor.executorId} high memory: {utilization:.2%}")

# 2. Optimize caching strategy
def optimize_caching(df):
    """Use appropriate storage levels"""
    # Instead of MEMORY_ONLY (causes OOM)
    df.persist(StorageLevel.MEMORY_AND_DISK_SER)
    
    # Or use disk-based storage for large datasets
    df.persist(StorageLevel.DISK_ONLY)

# 3. Increase parallelism
def increase_parallelism(df):
    """Reduce data per partition"""
    # Check current partitions
    current_partitions = df.rdd.getNumPartitions()
    
    # Increase partitions to reduce memory per partition
    df_repartitioned = df.repartition(current_partitions * 4)
    return df_repartitioned

# 4. Optimize joins
def optimize_memory_intensive_joins(large_df, small_df):
    """Use broadcast joins to avoid shuffles"""
    # Broadcast small table (< 200MB)
    result = large_df.join(broadcast(small_df), "key")
    
    # For large-large joins, use bucketing
    large_df.write.bucketBy(200, "key").saveAsTable("large_bucketed")
    small_df.write.bucketBy(200, "key").saveAsTable("small_bucketed")
    
    return spark.table("large_bucketed").join(spark.table("small_bucketed"), "key")

# 5. Tune garbage collection
gc_options = [
    "-XX:+UseG1GC",
    "-XX:MaxGCPauseMillis=200",
    "-XX:G1HeapRegionSize=16m",
    "-XX:+UnlockExperimentalVMOptions",
    "-XX:+UseG1GC",
    "-XX:+G1UseAdaptiveIHOP"
]

spark.conf.set("spark.executor.extraJavaOptions", " ".join(gc_options))
```

### 183. Design a real-time fraud detection system using Spark Streaming
**Answer:**
```python
from pyspark.sql.functions import *
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier

def create_fraud_detection_pipeline():
    """Real-time fraud detection using Spark Streaming"""
    
    # 1. Read transaction stream
    transaction_stream = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "transactions") \
        .load()
    
    # 2. Parse and enrich transactions
    parsed_transactions = transaction_stream.select(
        from_json(col("value").cast("string"), transaction_schema).alias("data")
    ).select("data.*")
    
    # 3. Feature engineering
    enriched_transactions = parsed_transactions \
        .withColumn("hour_of_day", hour(col("timestamp"))) \
        .withColumn("day_of_week", dayofweek(col("timestamp"))) \
        .withColumn("amount_log", log(col("amount") + 1))
    
    # 4. Real-time aggregations (velocity features)
    velocity_features = enriched_transactions \
        .withWatermark("timestamp", "5 minutes") \
        .groupBy(
            col("user_id"),
            window(col("timestamp"), "10 minutes")
        ) \
        .agg(
            count("*").alias("txn_count_10min"),
            sum("amount").alias("total_amount_10min"),
            avg("amount").alias("avg_amount_10min")
        )
    
    # 5. Join with user profile (from static table)
    user_profiles = spark.read.table("user_profiles")
    
    features_df = enriched_transactions.join(
        velocity_features, 
        ["user_id", "timestamp"], 
        "left"
    ).join(
        broadcast(user_profiles), 
        "user_id", 
        "left"
    )
    
    # 6. Apply ML model for scoring
    def score_transactions(batch_df, batch_id):
        """Score transactions for fraud"""
        if batch_df.count() > 0:
            # Load pre-trained model
            model = RandomForestClassifier.load("/models/fraud_detection")
            
            # Prepare features
            feature_cols = ["amount_log", "hour_of_day", "day_of_week", 
                          "txn_count_10min", "user_risk_score"]
            assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
            
            features_df = assembler.transform(batch_df)
            predictions = model.transform(features_df)
            
            # Flag high-risk transactions
            fraud_alerts = predictions.filter(col("prediction") == 1.0)
            
            # Send alerts
            fraud_alerts.select("transaction_id", "user_id", "amount", "probability") \
                       .write \
                       .format("kafka") \
                       .option("kafka.bootstrap.servers", "localhost:9092") \
                       .option("topic", "fraud_alerts") \
                       .save()
            
            # Store results
            predictions.write \
                      .format("delta") \
                      .mode("append") \
                      .save("/delta/fraud_scores")
    
    # 7. Start streaming query
    query = features_df.writeStream \
        .foreachBatch(score_transactions) \
        .outputMode("update") \
        .option("checkpointLocation", "/checkpoints/fraud_detection") \
        .trigger(processingTime="30 seconds") \
        .start()
    
    return query

# Usage
fraud_detection_query = create_fraud_detection_pipeline()
fraud_detection_query.awaitTermination()
```

This comprehensive collection covers all aspects of Apache Spark for data engineering, from basic concepts to advanced production scenarios, providing practical examples and real-world implementation patterns.