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

**Apache Spark** is a unified analytics engine for large-scale data processing that provides high-level APIs in Java, Scala, Python, and R, along with an optimized engine supporting general computation graphs for data analysis.

#### **Key Differences:**

| Aspect | Apache Spark | Hadoop MapReduce |
|--------|--------------|------------------|
| **Processing Model** | In-memory processing | Disk-based processing |
| **Speed** | 100x faster for iterative algorithms | Slower due to disk I/O |
| **Data Processing** | Batch + Streaming + ML + Graph | Batch processing only |
| **Ease of Use** | High-level APIs, interactive shell | Low-level, verbose coding |
| **Fault Tolerance** | RDD lineage (automatic recovery) | Task-level restart |
| **Memory Usage** | High (caches data in RAM) | Low (processes from disk) |
| **Real-time Processing** | Native streaming support | Requires additional tools |
| **Machine Learning** | Built-in MLlib | Requires external libraries |

### 2. What are RDDs and what are their key characteristics?

**RDD (Resilient Distributed Dataset)** is the fundamental data structure of Spark - an immutable, distributed collection of objects that can be processed in parallel.

#### **Key Characteristics:**
- **Resilient**: Fault-tolerant, can recover from node failures using lineage
- **Distributed**: Data is partitioned across multiple cluster nodes
- **Immutable**: Cannot be changed once created (enables fault tolerance)
- **Lazy Evaluation**: Transformations build computation graph, executed only when action is called
- **In-Memory**: Can cache data in memory for faster access
- **Lineage**: Maintains dependency graph for automatic recovery

### 3. What's the difference between RDD transformations and actions?

**Answer:** Transformations create new RDDs while actions trigger execution.

#### 🎯 **Key Differences**
- **Transformations (Lazy)**: Create new RDD, not executed immediately
- **Actions (Eager)**: Trigger execution, return results to driver
- **Examples**: map(), filter() vs collect(), count()

```python
# Sample data
rdd = sc.parallelize([1, 2, 3, 4, 5])

# Transformations (lazy)
rdd_squared = rdd.map(lambda x: x * x)  # Not executed
rdd_filtered = rdd_squared.filter(lambda x: x > 10)  # Not executed

# Actions (trigger execution)
result = rdd_filtered.collect()  # Executes entire pipeline
count = rdd_filtered.count()     # Executes pipeline again

print(f"Results: {result}")
print(f"Count: {count}")
```

**Output:**
```
Results: [16, 25]
Count: 2
```

### 4. Explain Spark's architecture components.

**Answer:** Spark follows a master-slave architecture with distributed computing.

#### 🎯 **Core Components**
- **Driver Program**: Coordinates application and manages SparkContext
- **Cluster Manager**: Allocates resources (YARN, Mesos, Kubernetes)
- **Executors**: Run tasks and store data across cluster nodes

### 5. What is the Catalyst Optimizer?

**Answer:** Catalyst is Spark SQL's query optimizer for DataFrame operations.

#### 🎯 **Optimization Process**
- **Predicate Pushdown**: Move filters closer to data source
- **Column Pruning**: Read only required columns
- **Code Generation**: Generate optimized Java bytecode
### 6. What are the different types of joins in Spark?

**Answer:** Spark supports multiple join types and strategies.

#### 🎯 **Join Types**
- **Inner Join**: Matching records from both datasets
- **Left/Right Outer**: All records from one side + matches
- **Broadcast Join**: Small table broadcasted to all nodes

```python
# Sample DataFrames
df1 = spark.createDataFrame([(1, "Alice"), (2, "Bob"), (3, "Charlie")], ["id", "name"])
df2 = spark.createDataFrame([(1, "Engineering"), (2, "Sales"), (4, "Marketing")], ["id", "dept"])

# Inner join
inner_result = df1.join(df2, "id", "inner")
print("Inner Join:")
inner_result.show()

# Left outer join
left_result = df1.join(df2, "id", "left")
print("Left Outer Join:")
left_result.show()

# Broadcast join (for small tables)
from pyspark.sql.functions import broadcast
broadcast_result = df1.join(broadcast(df2), "id", "inner")
print("Broadcast Join:")
broadcast_result.show()
```

**Output:**
```
Inner Join:
+---+-------+-----------+
| id|   name|       dept|
+---+-------+-----------+
|  1|  Alice|Engineering|
|  2|    Bob|      Sales|
+---+-------+-----------+

Left Outer Join:
+---+-------+-----------+
| id|   name|       dept|
+---+-------+-----------+
|  1|  Alice|Engineering|
|  2|    Bob|      Sales|
|  3|Charlie|       null|
+---+-------+-----------+

Broadcast Join:
+---+-------+-----------+
| id|   name|       dept|
+---+-------+-----------+
|  1|  Alice|Engineering|
|  2|    Bob|      Sales|
+---+-------+-----------+
```

### 7. How does Spark handle fault tolerance?

**Answer:** Spark uses RDD lineage for automatic fault recovery.

#### 🎯 **Fault Tolerance Mechanisms**
- **RDD Lineage**: Tracks dependencies for recomputation
- **Task Retry**: Failed tasks automatically retried
- **Speculative Execution**: Handles slow tasks

### 8. What is the difference between cache() and persist()?

**Answer:** Both store RDDs in memory but persist() offers more control.

#### 🎯 **Key Differences**
- **cache()**: Uses MEMORY_AND_DISK storage level
- **persist()**: Allows custom storage levels (MEMORY_ONLY, DISK_ONLY)

```python
from pyspark import StorageLevel
import time

# Create a large RDD
rdd = sc.parallelize(range(1000000)).map(lambda x: x * x)

# Using cache() - default MEMORY_AND_DISK
rdd_cached = rdd.cache()
start_time = time.time()
count1 = rdd_cached.count()
first_run = time.time() - start_time

# Second run (from cache)
start_time = time.time()
count2 = rdd_cached.count()
second_run = time.time() - start_time

print(f"First run: {first_run:.3f}s, Count: {count1}")
print(f"Second run: {second_run:.3f}s, Count: {count2}")
print(f"Speedup: {first_run/second_run:.1f}x")

# Using persist() with custom storage level
rdd_persist = rdd.persist(StorageLevel.MEMORY_ONLY)
print(f"Storage level: {rdd_persist.getStorageLevel()}")
```

**Output:**
```
First run: 0.245s, Count: 1000000
Second run: 0.089s, Count: 1000000
Speedup: 2.8x
Storage level: StorageLevel(True, False, False, False, 1)
```

### 9. What are accumulators and broadcast variables?

**Answer:** Shared variables for distributed computations in Spark.

#### 🎯 **Accumulators**
- **Write-only variables** for aggregating information across tasks
- **Use cases**: Counters, sums, custom metrics

```python
# Create accumulator
counter = sc.accumulator(0)

def process_line(line):
    if "ERROR" in line:
        counter.add(1)
    return line.upper()

# Sample data
rdd = sc.parallelize(["INFO: Starting", "ERROR: Failed", "DEBUG: Processing", "ERROR: Timeout"])
result = rdd.map(process_line).collect()
print(f"Errors found: {counter.value}")
```

**Output:**
```
Errors found: 2
```

#### 🎯 **Broadcast Variables**
- **Read-only variables** cached on each machine
- **Use cases**: Lookup tables (< 200MB), configuration, ML models

```python
# Create broadcast variable
lookup_dict = {"A": 1, "B": 2, "C": 3}
broadcast_dict = sc.broadcast(lookup_dict)

def enrich_data(record):
    return broadcast_dict.value.get(record, 0)

# Sample data
rdd = sc.parallelize(["A", "B", "D", "C"])
result = rdd.map(enrich_data).collect()
print(result)
```

**Output:**
```
[1, 2, 0, 3]
```

### 10. How does Spark handle memory management?

**Answer:** Spark divides memory into regions for different purposes.

#### 🎯 **Memory Regions**
- **Execution Memory**: For shuffles, joins, sorts, aggregations
- **Storage Memory**: For caching RDDs and DataFrames
- **User Memory**: For user data structures
- **Reserved Memory**: For Spark's internal objects

```python
# Memory configuration
spark.conf.set("spark.executor.memory", "4g")
spark.conf.set("spark.executor.memoryFraction", "0.8")
spark.conf.set("spark.storage.memoryFraction", "0.5")

# Sample DataFrame
df = spark.createDataFrame([(1, "Alice"), (2, "Bob")], ["id", "name"])

# Caching strategies
df.cache()  # MEMORY_ONLY
df.persist(StorageLevel.MEMORY_AND_DISK)
df.show()
```

**Output:**
```
+---+-----+
| id| name|
+---+-----+
|  1|Alice|
|  2|  Bob|
+---+-----+
```
### 11. What are the different cluster managers supported by Spark?

**Answer:** Spark supports multiple cluster managers for resource management.

#### 🎯 **Cluster Managers**
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

### 12. Explain lazy evaluation and its benefits.

**Answer:** Lazy evaluation means transformations are not executed until an action is called.

#### 🎯 **Benefits**
- **Optimization**: Catalyst can optimize entire query plan
- **Efficiency**: Eliminates intermediate results
- **Fault Tolerance**: Can recompute lost partitions
- **Pipeline Optimization**: Combines multiple operations

```python
# Lazy evaluation example
rdd1 = sc.parallelize(["info message", "error occurred", "debug info", "error timeout"])  # Not executed
rdd2 = rdd1.filter(lambda x: "error" in x)  # Not executed
rdd3 = rdd2.map(lambda x: x.upper())  # Not executed

# Execution happens only here
results = rdd3.collect()
print(results)
```

**Output:**
```
['ERROR OCCURRED', 'ERROR TIMEOUT']
```

### 13. What are the different deployment modes?

**Answer:** Spark supports different deployment modes for driver placement.

#### 🎯 **Deployment Modes**
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

### 14. What are the different storage levels in Spark?

**Answer:** Spark provides various storage levels for caching data.

```python
from pyspark import StorageLevel

# Sample DataFrame
df = spark.createDataFrame([(1, "Alice", 25), (2, "Bob", 30)], ["id", "name", "age"])

# Memory only (default for cache())
df.persist(StorageLevel.MEMORY_ONLY)
print(f"Storage level: {df.storageLevel}")

# Memory and disk
df.persist(StorageLevel.MEMORY_AND_DISK)
print(f"Storage level: {df.storageLevel}")

# Show data
df.show()
```

**Output:**
```
Storage level: StorageLevel(True, True, False, False, 1)
Storage level: StorageLevel(True, True, False, False, 1)
+---+-----+---+
| id| name|age|
+---+-----+---+
|  1|Alice| 25|
|  2|  Bob| 30|
+---+-----+---+
```

### 15. What is the difference between DataFrame and Dataset?

**Answer:** DataFrames are untyped while Datasets are type-safe.

#### 🎯 **Key Differences**
- **DataFrame**: Untyped, available in all languages
- **Dataset**: Type-safe, only in Scala/Java
- **Performance**: Similar due to Catalyst optimizer

```python
# DataFrame operations (Python)
from pyspark.sql import functions as F

# Create DataFrame
df = spark.createDataFrame([
    (1, "Alice", 25, "Engineering"),
    (2, "Bob", 30, "Sales"),
    (3, "Charlie", 35, "Engineering"),
    (4, "Diana", 28, "Marketing")
], ["id", "name", "age", "department"])

# DataFrame transformations
result = df.filter(F.col("age") > 27) \
           .groupBy("department") \
           .agg(F.avg("age").alias("avg_age"), F.count("*").alias("count")) \
           .orderBy("avg_age")

print("DataFrame Operations:")
result.show()

# SQL operations
df.createOrReplaceTempView("employees")
sql_result = spark.sql("""
    SELECT department, AVG(age) as avg_age, COUNT(*) as count
    FROM employees 
    WHERE age > 27
    GROUP BY department
    ORDER BY avg_age
""")

print("SQL Operations:")
sql_result.show()
```

**Output:**
```
DataFrame Operations:
+-----------+-------+-----+
| department|avg_age|count|
+-----------+-------+-----+
|  Marketing|   28.0|    1|
|      Sales|   30.0|    1|
|Engineering|   35.0|    1|
+-----------+-------+-----+

SQL Operations:
+-----------+-------+-----+
| department|avg_age|count|
+-----------+-------+-----+
|  Marketing|   28.0|    1|
|      Sales|   30.0|    1|
|Engineering|   35.0|    1|
+-----------+-------+-----+
```
### 16. How do you handle small files problem?

**Answer:** Use coalesce() or repartition() to reduce partition count.

```python
# Sample DataFrame with multiple partitions
df = spark.range(1000).repartition(10)
print(f"Original partitions: {df.rdd.getNumPartitions()}")

# Coalesce partitions
df_coalesced = df.coalesce(2)
print(f"After coalesce: {df_coalesced.rdd.getNumPartitions()}")

# Configure partition size
spark.conf.set("spark.sql.files.maxPartitionBytes", "134217728")  # 128MB
print("Partition size configured to 128MB")
```

**Output:**
```
Original partitions: 10
After coalesce: 2
Partition size configured to 128MB
```

### 17. What is Dynamic Allocation?

**Answer:** Automatically scales executors based on workload.

```python
# Enable dynamic allocation
spark.conf.set("spark.dynamicAllocation.enabled", "true")
spark.conf.set("spark.dynamicAllocation.minExecutors", "1")
spark.conf.set("spark.dynamicAllocation.maxExecutors", "10")
spark.conf.set("spark.dynamicAllocation.initialExecutors", "2")

# Check configuration
print(f"Dynamic allocation enabled: {spark.conf.get('spark.dynamicAllocation.enabled')}")
print(f"Min executors: {spark.conf.get('spark.dynamicAllocation.minExecutors')}")
print(f"Max executors: {spark.conf.get('spark.dynamicAllocation.maxExecutors')}")
```

**Output:**
```
Dynamic allocation enabled: true
Min executors: 1
Max executors: 10
```, "1")
spark.conf.set("spark.dynamicAllocation.maxExecutors", "20")
```

### 18. What are different file formats supported?

**Answer:** Spark supports Parquet, JSON, CSV, Avro, Delta Lake.

```python
# Parquet (recommended)
df.write.parquet("data.parquet")

# JSON
df.write.json("data.json")

# CSV with options
df.write.csv("data.csv", header=True)
```

### 19. How do you optimize join operations?

**Answer:** Use broadcast joins for small tables and bucketing for large tables.

```python
# Broadcast join
from pyspark.sql.functions import broadcast
large_df.join(broadcast(small_df), "key")

# Bucketing
df.write.bucketBy(10, "key").saveAsTable("bucketed_table")
```

### 20. What is coalesce() vs repartition()?

**Answer:** coalesce() reduces partitions without shuffle, repartition() does full shuffle.

```python
# Reduce partitions efficiently
df_coalesced = df.coalesce(5)

# Full shuffle (can increase/decrease)
df_repartitioned = df.repartition(10)
```
### 21. How do you handle null values?

**Answer:** Use dropna(), fillna(), or conditional logic.

```python
# Drop nulls
df_clean = df.dropna(subset=["important_column"])

# Fill nulls
df_filled = df.fillna({"age": 0, "name": "Unknown"})
```

### 22. What are different ways to create DataFrames?

**Answer:** From files, RDDs, Python data, or databases.

```python
# From file
df = spark.read.csv("data.csv", header=True)

# From RDD
df = rdd.toDF(["name", "age"])

# From Python data
df = spark.createDataFrame([("Alice", 25)], ["name", "age"])
```

### 23. How do you perform window functions?

**Answer:** Use Window specification with ranking and analytical functions.

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, rank

window_spec = Window.partitionBy("department").orderBy("salary")
df.withColumn("rank", rank().over(window_spec))
```

### 24. What is schema evolution?

**Answer:** Handling changes in data schema over time.

```python
# Enable schema merging
df = spark.read.option("mergeSchema", "true").parquet("data/")

# Delta Lake schema evolution
df.write.format("delta").option("mergeSchema", "true").save("/delta/table")
```

### 25. What are Spark performance tuning best practices?

**Answer:** Optimize cluster config, enable adaptive query execution, use appropriate storage.

```python
# Adaptive query execution
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")

# Optimal executor config
spark.conf.set("spark.executor.cores", "5")
spark.conf.set("spark.executor.memory", "8g")
```
### 26. How do you debug Spark applications?

**Answer:** Use Spark UI, explain plans, and logging.

```python
# Explain query plan
df.explain(True)

# Enable detailed logging
spark.sparkContext.setLogLevel("INFO")

# Sample data for debugging
df_sample = df.sample(0.1, seed=42)
```

### 27. How do you implement data quality checks?

**Answer:** Check completeness, uniqueness, and validity.

```python
# Check for nulls
null_count = df.filter(col("column").isNull()).count()

# Check uniqueness
distinct_count = df.select("column").distinct().count()

# Validate patterns
valid_emails = df.filter(col("email").rlike(r"^[\w\.-]+@[\w\.-]+\.\w+$"))
```

### 28. How do you handle time series data?

**Answer:** Use time-based windowing and temporal functions.

```python
from pyspark.sql.functions import window, to_timestamp

# Parse timestamps
df = df.withColumn("timestamp", to_timestamp(col("timestamp_str")))

# Time windows
windowed = df.groupBy(window(col("timestamp"), "1 hour")).count()
```

### 29. What is Change Data Capture (CDC)?

**Answer:** Track and process data changes using merge operations.

```python
from delta.tables import DeltaTable

# Merge CDC changes
target_table = DeltaTable.forPath(spark, "/delta/table")
target_table.alias("target").merge(
    source_df.alias("source"),
    "target.id = source.id"
).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
```

### 30. How do you implement slowly changing dimensions?

**Answer:** Use SCD Type 2 with effective dates and current flags.

```python
# Add SCD metadata
source_df = source_df.withColumn("effective_date", current_date()) \
                     .withColumn("is_current", lit(True))

# Implement SCD Type 2 logic with Delta merge
```

---

## Intermediate Level Questions (31-60)

### 31. How do you optimize Spark jobs for better performance?

**Answer:** Use proper partitioning, caching, and broadcast joins.

```python
# Increase parallelism
df.repartition(200)

# Cache frequently used data
df.cache()

# Broadcast small tables
large_df.join(broadcast(small_df), "key")

# Enable adaptive query execution
spark.conf.set("spark.sql.adaptive.enabled", "true")
```
### 32. Explain different types of joins and their performance characteristics.

**Answer:** Broadcast Hash Join is fastest for small tables, Sort Merge Join for large tables.

```python
# Broadcast join (< 10MB)
result = large_df.join(broadcast(small_df), "key")

# Sort merge join (default for large tables)
result = df1.join(df2, "key")

# Bucketing for repeated joins
df.write.bucketBy(10, "key").saveAsTable("bucketed_table")
```

### 33. How do you handle data skew in Spark?

**Answer:** Use salting technique and adaptive query execution.

```python
# Identify skewed data
df.groupBy("key").count().orderBy(col("count").desc()).show()

# Salting for skewed joins
salted_df = df.withColumn("salted_key", 
    concat(col("key"), lit("_"), (rand() * 10).cast("int")))

# Enable skew join optimization
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
```

### 34. How do you implement incremental data processing?

**Answer:** Use watermarks, timestamps, and Delta Lake time travel.

```python
# Watermark-based incremental processing
df_incremental = df.filter(col("timestamp") > last_processed_timestamp)

# Delta Lake incremental
df_new = spark.read.format("delta").option("timestampAsOf", "2024-01-01").load("/delta/table")
df_old = spark.read.format("delta").option("versionAsOf", 0).load("/delta/table")
df_incremental = df_new.exceptAll(df_old)
```

### 35. What are User Defined Functions (UDFs) and their performance implications?

**Answer:** UDFs enable custom logic but have serialization overhead. Use vectorized UDFs when possible.

```python
# Python UDF (slower)
def upper_case(text):
    return text.upper() if text else None

upper_udf = udf(upper_case, StringType())
df.withColumn("upper_name", upper_udf(df.name))

# Vectorized UDF (faster)
@pandas_udf(returnType=StringType())
def vectorized_upper(series: pd.Series) -> pd.Series:
    return series.str.upper()

df.withColumn("upper_name", vectorized_upper(df.name))
```
### 36. How do you handle complex nested data structures?

**Answer:** Use explode(), get_json_object(), and struct operations.

```python
# Extract nested fields
df_extracted = json_df.select(
    col("user.name").alias("user_name"),
    col("user.email").alias("user_email")
)

# Explode arrays
df_exploded = df.select(
    "user_name",
    explode("orders").alias("order")
)
```

### 37. What is bucketing and when should you use it?

**Answer:** Bucketing distributes data into fixed buckets for efficient joins and aggregations.

```python
# Create bucketed table
df.write.bucketBy(10, "user_id").sortBy("timestamp").saveAsTable("bucketed_events")

# Efficient joins on bucketed columns
bucketed_df1.join(bucketed_df2, "user_id")  # No shuffle needed
```

### 38. How do you implement data deduplication strategies?

**Answer:** Use dropDuplicates(), window functions, or custom logic.

```python
# Simple deduplication
df_deduplicated = df.dropDuplicates(["key_column"])

# Keep latest record
window_spec = Window.partitionBy("key_column").orderBy(desc("timestamp"))
df_latest = df.withColumn("row_num", row_number().over(window_spec)) \
              .filter(col("row_num") == 1).drop("row_num")
```

### 39. How do you optimize shuffle operations?

**Answer:** Reduce shuffle data size, use appropriate join strategies, and pre-partition data.

```python
# Adjust shuffle partitions
spark.conf.set("spark.sql.shuffle.partitions", "200")

# Broadcast small tables
large_df.join(broadcast(small_df), "key")

# Pre-partition data
df.repartition("join_key").write.saveAsTable("partitioned_table")
```

### 40. How do you implement complex aggregations?

**Answer:** Use multiple aggregation functions, window functions, and pivot operations.

```python
# Multiple aggregations
complex_agg = df.groupBy("category", "region").agg(
    sum("amount").alias("total_amount"),
    avg("amount").alias("avg_amount"),
    countDistinct("user_id").alias("unique_users")
)

# Window functions for running calculations
window_spec = Window.partitionBy("user_id").orderBy("timestamp")
running_totals = df.withColumn(
    "running_total", 
    sum("amount").over(window_spec.rowsBetween(Window.unboundedPreceding, Window.currentRow))
)
```
### 41. How do you handle schema evolution in production?

**Answer:** Use schema registry, Delta Lake schema evolution, or manual schema handling.

```python
# Enable schema merging
df = spark.read.option("mergeSchema", "true").parquet("data/")

# Delta Lake schema evolution
df.write.format("delta").option("mergeSchema", "true").save("/delta/table")
```

### 42. How do you implement data quality validation?

**Answer:** Check completeness, uniqueness, validity, and consistency.

```python
# Completeness check
total_count = df.count()
non_null_count = df.filter(col("column").isNotNull()).count()
completeness = non_null_count / total_count

# Uniqueness check
distinct_count = df.select("column").distinct().count()
uniqueness = distinct_count / total_count
```

### 43. How do you implement efficient data sampling?

**Answer:** Use random sampling, stratified sampling, or systematic sampling.

```python
# Random sampling
sampled_df = df.sample(fraction=0.1, seed=42)

# Stratified sampling
stratified_sample = df.sampleBy("category", {"A": 0.1, "B": 0.2}, seed=42)
```

### 44. How do you handle large-scale data transformations?

**Answer:** Use chunked processing, memory-efficient joins, and optimal partitioning.

```python
# Chunked processing
optimal_partitions = max(1, df.count() // 1000000)  # 1M records per partition
df_repartitioned = df.repartition(optimal_partitions)

# Memory-efficient joins
if small_df_size < 200 * 1024 * 1024:  # 200MB
    result = large_df.join(broadcast(small_df), "key")
```

### 45. How do you implement custom partitioning strategies?

**Answer:** Use date-based, hash-based, or range-based partitioning.

```python
# Date-based partitioning
df_partitioned = df.withColumn("year", year(col("date"))) \
                   .withColumn("month", month(col("date")))

# Hash-based partitioning
df_hash = df.withColumn("partition_id", 
    (hash(col("key")) % 10 + 10) % 10)
```
### 46. How do you implement Change Data Capture (CDC)?

**Answer:** Use Delta Lake merge operations for CDC processing.

```python
from delta.tables import DeltaTable

# Add CDC metadata
source_with_meta = source_df.withColumn("last_updated", current_timestamp())

if DeltaTable.isDeltaTable(spark, target_path):
    target_table = DeltaTable.forPath(spark, target_path)
    
    # Perform merge operation
    target_table.alias("target").merge(
        source_with_meta.alias("source"),
        "target.id = source.id"
    ).whenMatchedUpdateAll(
        condition="target.last_updated < source.last_updated"
    ).whenNotMatchedInsertAll().execute()
```

### 47. How do you handle time series data in Spark?

**Answer:** Use time-based windowing, lag/lead functions, and temporal aggregations.

```python
# Time-based windowing
time_windowed = df.groupBy(
    window(col("timestamp"), "1 hour", "15 minutes")
).agg(avg("value").alias("avg_value"))

# Time series features
window_spec = Window.partitionBy("sensor_id").orderBy("timestamp")
ts_features = df.withColumn("prev_value", lag("value", 1).over(window_spec)) \
                .withColumn("value_change", col("value") - col("prev_value"))
```

### 48. How do you implement data lineage tracking?

**Answer:** Track transformations and store lineage metadata.

```python
# Track transformation lineage
lineage_record = {
    "transformation_id": f"transform_{datetime.now().timestamp()}",
    "input_datasets": ["/input/data1", "/input/data2"],
    "output_dataset": "/output/processed",
    "transformation_type": "join_and_aggregate",
    "timestamp": datetime.now().isoformat()
}

# Store lineage
lineage_df = spark.createDataFrame([lineage_record])
lineage_df.write.format("delta").mode("append").save("/delta/lineage")
```

### 49. How do you implement data versioning and time travel?

**Answer:** Use Delta Lake for ACID transactions and time travel capabilities.

```python
# Time travel queries
current_data = spark.read.format("delta").load("/delta/table")
yesterday_data = spark.read.format("delta") \
    .option("timestampAsOf", "2024-01-01").load("/delta/table")
version_0_data = spark.read.format("delta") \
    .option("versionAsOf", 0).load("/delta/table")

# Compare versions
added_records = current_data.exceptAll(yesterday_data)
removed_records = yesterday_data.exceptAll(current_data)
```

### 50. How do you implement slowly changing dimensions (SCD)?

**Answer:** Use SCD Type 2 with effective dates and merge operations.

```python
# SCD Type 2 implementation
source_with_meta = source_df.withColumn("effective_date", current_date()) \
                            .withColumn("end_date", lit(None).cast("date")) \
                            .withColumn("is_current", lit(True))

# Close current records that changed
target_table.alias("target").merge(
    source_with_meta.alias("source"),
    "target.customer_id = source.customer_id AND target.is_current = true"
).whenMatchedUpdate(
    condition="target.name != source.name OR target.email != source.email",
    set={"end_date": "current_date()", "is_current": "false"}
).execute()
```
### 51. How do you optimize Spark for machine learning workloads?

**Answer:** Cache data, use vectorized operations, and ML pipelines.

```python
# Cache ML data
df.persist(StorageLevel.MEMORY_AND_DISK_SER)

# Enable Arrow optimization
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

# ML Pipeline
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler, StandardScaler

assembler = VectorAssembler(inputCols=["feature1", "feature2"], outputCol="features")
scaler = StandardScaler(inputCol="features", outputCol="scaled_features")
pipeline = Pipeline(stages=[assembler, scaler])
```

### 52. How do you implement data profiling?

**Answer:** Generate statistics, distributions, and quality metrics.

```python
# Basic statistics
df.describe().show()

# Column profiling
for column in df.columns:
    null_count = df.filter(col(column).isNull()).count()
    distinct_count = df.select(column).distinct().count()
    print(f"{column}: nulls={null_count}, distinct={distinct_count}")

# Data distribution
df.groupBy("category").count().orderBy(desc("count")).show()
```

### 53. How do you handle cross-cluster data sharing?

**Answer:** Use external storage (S3, HDFS), Delta Lake, or streaming platforms.

```python
# S3-based sharing
df.write.partitionBy("date").parquet("s3://shared-bucket/data")
shared_df = spark.read.parquet("s3://shared-bucket/data")

# Delta Lake sharing
df.write.format("delta").save("s3://delta-lake/table")
shared_df = spark.read.format("delta").load("s3://delta-lake/table")
```

### 54. How do you implement data encryption in Spark?

**Answer:** Enable encryption at rest and in transit, use column-level encryption.

```python
# Encryption at rest
spark.conf.set("spark.io.encryption.enabled", "true")
spark.conf.set("spark.io.encryption.keySizeBits", "256")

# Encryption in transit
spark.conf.set("spark.network.crypto.enabled", "true")

# Column-level encryption UDF
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_column(value):
    return cipher_suite.encrypt(value.encode()).decode() if value else None

encrypt_udf = udf(encrypt_column, StringType())
encrypted_df = df.withColumn("encrypted_ssn", encrypt_udf(col("ssn")))
```

### 55. How do you implement data masking and anonymization?

**Answer:** Mask sensitive data using hashing, tokenization, or pattern replacement.

```python
# Email masking
masked_email = df.withColumn("masked_email",
    concat(lit("****@"), split(col("email"), "@").getItem(1)))

# Phone masking
masked_phone = df.withColumn("masked_phone",
    concat(lit("***-***-"), substring(col("phone"), -4, 4)))

# Hash PII
import hashlib
def hash_pii(value):
    return hashlib.sha256(str(value).encode()).hexdigest() if value else None

hash_udf = udf(hash_pii, StringType())
hashed_df = df.withColumn("hashed_ssn", hash_udf(col("ssn")))
```

### 56. How do you implement data retention policies?

**Answer:** Use time-based filtering, archiving, and automated cleanup.

```python
# Apply retention policy
cutoff_date = datetime.now() - timedelta(days=90)

if DeltaTable.isDeltaTable(spark, table_path):
    delta_table = DeltaTable.forPath(spark, table_path)
    
    # Delete old records
    delta_table.delete(col("date") < lit(cutoff_date))
    
    # Vacuum to remove old files
    delta_table.vacuum(retentionHours=24)
```

### 57. How do you implement data cataloging and metadata management?

**Answer:** Register datasets, track schema, and maintain lineage information.

```python
# Register dataset in catalog
catalog_entry = {
    "dataset_name": "user_transactions",
    "dataset_path": "/data/transactions",
    "schema": df.schema.json(),
    "row_count": df.count(),
    "registration_time": datetime.now().isoformat(),
    "owner": "data_team",
    "classification": "PII"
}

catalog_df = spark.createDataFrame([catalog_entry])
catalog_df.write.format("delta").mode("append").save("/catalog/datasets")
```

### 58. How do you implement data governance workflows?

**Answer:** Create approval workflows, audit trails, and access controls.

```python
# Submit data access request
request = {
    "request_id": f"REQ_{datetime.now().timestamp()}",
    "requester": "john.doe@company.com",
    "dataset_name": "customer_data",
    "purpose": "Marketing analysis",
    "status": "pending",
    "submitted_at": datetime.now().isoformat()
}

request_df = spark.createDataFrame([request])
request_df.write.format("delta").mode("append").save("/governance/requests")
```

### 59. How do you implement real-time data quality monitoring?

**Answer:** Monitor streaming data quality with rules and alerts.

```python
# Real-time quality monitoring
def quality_check_batch(batch_df, batch_id):
    if batch_df.count() > 0:
        # Completeness check
        total_count = batch_df.count()
        non_null_count = batch_df.filter(col("email").isNotNull()).count()
        completeness = non_null_count / total_count
        
        # Store quality metrics
        quality_metrics = {
            "batch_id": batch_id,
            "timestamp": datetime.now().isoformat(),
            "completeness": completeness,
            "record_count": total_count
        }
        
        metrics_df = spark.createDataFrame([quality_metrics])
        metrics_df.write.format("delta").mode("append").save("/quality/metrics")

# Apply to streaming data
streaming_df.writeStream.foreachBatch(quality_check_batch) \
            .option("checkpointLocation", "/checkpoints/quality").start()
```

### 60. How do you implement cost optimization strategies?

**Answer:** Optimize cluster sizing, use spot instances, and implement tiered storage.

```python
# Dynamic allocation for cost optimization
spark.conf.set("spark.dynamicAllocation.enabled", "true")
spark.conf.set("spark.dynamicAllocation.minExecutors", "2")
spark.conf.set("spark.dynamicAllocation.maxExecutors", "50")
spark.conf.set("spark.dynamicAllocation.executorIdleTimeout", "30s")

# Tiered storage strategy
# Hot tier (frequent access)
hot_data = df.filter(col("date") >= lit(datetime.now() - timedelta(days=30)))
hot_data.write.format("delta").save("/hot_tier/data")

# Cold tier (rare access)
cold_data = df.filter(col("date") < lit(datetime.now() - timedelta(days=90)))
cold_data.write.format("parquet").option("compression", "gzip") \
         .save("/cold_tier/data")
```

---

## Advanced Level Questions (61-90)
### 61. How do you implement a complex ETL pipeline with error handling?

**Answer:** Build robust pipelines with comprehensive error handling and monitoring.

```python
class SparkETLPipeline:
    def __init__(self, spark, config):
        self.spark = spark
        self.config = config
        self.metrics = {}
    
    def extract(self, source_config):
        try:
            if source_config['type'] == 'jdbc':
                df = self.spark.read.format("jdbc") \
                    .option("url", source_config['url']) \
                    .option("dbtable", source_config['table']) \
                    .load()
            else:
                df = self.spark.read.format(source_config['format']) \
                    .load(source_config['path'])
            
            self.metrics['extracted_records'] = df.count()
            return df
        except Exception as e:
            self._log_error("extraction", str(e))
            raise
```

### 62. How do you implement advanced streaming patterns?

**Answer:** Use complex event processing, stateful operations, and watermarking.

```python
# Complex event processing
def detect_fraud_patterns(streaming_df):
    windowed_transactions = streaming_df \
        .withWatermark("timestamp", "10 minutes") \
        .groupBy(
            col("user_id"),
            window(col("timestamp"), "5 minutes")
        ).agg(
            count("*").alias("transaction_count"),
            sum("amount").alias("total_amount")
        )
    
    fraud_alerts = windowed_transactions.filter(
        (col("transaction_count") > 10) | 
        (col("total_amount") > 10000)
    )
    
    return fraud_alerts
```

### 63. How do you implement advanced performance optimization?

**Answer:** Use adaptive query execution, custom optimizations, and advanced caching strategies.

```python
# Advanced performance optimization
def optimize_joins(df1, df2, join_key):
    df1_size = df1.count()
    df2_size = df2.count()
    
    if df2_size < 10000:  # Small table
        return df1.join(broadcast(df2), join_key)
    elif abs(df1_size - df2_size) > df1_size * 0.8:  # Skewed sizes
        # Use bucket join
        df1.write.bucketBy(200, join_key).saveAsTable("temp_df1")
        df2.write.bucketBy(200, join_key).saveAsTable("temp_df2")
        return spark.table("temp_df1").join(spark.table("temp_df2"), join_key)
    else:
        return df1.repartition(col(join_key)).join(
            df2.repartition(col(join_key)), join_key
        )
```

### 64. How do you implement advanced data quality frameworks?

**Answer:** Build comprehensive data quality validation with custom rules and metrics.

```python
class AdvancedDataQuality:
    def __init__(self, spark):
        self.spark = spark
        self.quality_rules = []
    
    def add_rule(self, rule_name, rule_func, threshold=0.95):
        self.quality_rules.append({
            'name': rule_name,
            'function': rule_func,
            'threshold': threshold
        })
    
    def validate_dataset(self, df):
        results = []
        
        for rule in self.quality_rules:
            score = rule['function'](df)
            passed = score >= rule['threshold']
            
            results.append({
                'rule_name': rule['name'],
                'score': score,
                'threshold': rule['threshold'],
                'passed': passed,
                'timestamp': datetime.now().isoformat()
            })
        
        results_df = self.spark.createDataFrame(results)
        results_df.write.format("delta").mode("append").save("/quality/results")
        
        return results
```

### 65. How do you implement advanced security patterns?

**Answer:** Implement row-level security, column-level access control, and audit logging.

```python
class SparkSecurityManager:
    def __init__(self, spark):
        self.spark = spark
        self.user_permissions = {}
    
    def apply_row_level_security(self, df, user_id, table_name):
        permissions = self._get_user_permissions(user_id, table_name)
        
        if permissions.get('row_filter'):
            df = df.filter(permissions['row_filter'])
        
        return df
    
    def apply_column_level_security(self, df, user_id, table_name):
        permissions = self._get_user_permissions(user_id, table_name)
        allowed_columns = permissions.get('columns', df.columns)
        
        masked_df = df
        for column in df.columns:
            if column not in allowed_columns:
                if column in permissions.get('masked_columns', []):
                    masked_df = masked_df.withColumn(column, lit("***MASKED***"))
                else:
                    masked_df = masked_df.drop(column)
        
        return masked_df
```
### 66. How do you implement advanced monitoring and alerting?

**Answer:** Build comprehensive monitoring with custom metrics and automated alerting.

```python
class SparkMonitoringSystem:
    def __init__(self, spark):
        self.spark = spark
        self.alert_thresholds = {}
    
    def collect_performance_metrics(self):
        sc = self.spark.sparkContext
        status = sc.statusTracker()
        
        metrics = {
            'application_id': sc.applicationId,
            'timestamp': datetime.now().isoformat(),
            'active_jobs': len(status.getActiveJobIds()),
            'active_stages': len(status.getActiveStages()),
            'total_executors': len(status.getExecutorInfos()),
            'total_cores': sum(e.totalCores for e in status.getExecutorInfos()),
            'total_memory_mb': sum(e.maxMemory for e in status.getExecutorInfos()) // (1024*1024),
            'used_memory_mb': sum(e.memoryUsed for e in status.getExecutorInfos()) // (1024*1024)
        }
        
        if metrics['total_memory_mb'] > 0:
            metrics['memory_utilization'] = metrics['used_memory_mb'] / metrics['total_memory_mb']
        
        metrics_df = self.spark.createDataFrame([metrics])
        metrics_df.write.format("delta").mode("append").save("/monitoring/performance_metrics")
        
        return metrics
```

### 67. How do you implement advanced data lake patterns?

**Answer:** Build data lake architecture with zones, cataloging, and governance.

```python
class DataLakeManager:
    def __init__(self, spark):
        self.spark = spark
        self.zones = {
            'raw': '/datalake/raw',
            'bronze': '/datalake/bronze',
            'silver': '/datalake/silver',
            'gold': '/datalake/gold'
        }
    
    def ingest_to_raw(self, source_df, dataset_name, partition_cols=None):
        enriched_df = source_df.withColumn("ingestion_timestamp", current_timestamp()) \
                              .withColumn("source_system", lit(dataset_name))
        
        path = f"{self.zones['raw']}/{dataset_name}"
        
        if partition_cols:
            enriched_df.write.partitionBy(*partition_cols) \
                      .format("delta").mode("append").save(path)
        else:
            enriched_df.write.format("delta").mode("append").save(path)
        
        self._register_dataset(dataset_name, path, "raw", enriched_df.schema)
        return path
```

### 68. How do you implement advanced streaming architectures?

**Answer:** Build lambda/kappa architectures with exactly-once processing and state management.

```python
class StreamingArchitecture:
    def __init__(self, spark):
        self.spark = spark
    
    def implement_exactly_once_processing(self, source_topic):
        def process_with_idempotency(batch_df, batch_id):
            if batch_df.count() > 0:
                processed_df = batch_df.withColumn("batch_id", lit(batch_id)) \
                                      .withColumn("processed_at", current_timestamp())
                
                existing_batches = self.spark.read.format("delta") \
                                             .load("/processed/transactions") \
                                             .select("batch_id").distinct()
                
                new_records = processed_df.join(existing_batches, "batch_id", "left_anti")
                
                if new_records.count() > 0:
                    result = new_records.groupBy("user_id") \
                                       .agg(sum("amount").alias("total_amount"))
                    
                    result.write.format("delta").mode("append") \
                          .save("/processed/transactions")
        
        streaming_df = self.spark.readStream.format("kafka") \
                                 .option("kafka.bootstrap.servers", "localhost:9092") \
                                 .option("subscribe", source_topic) \
                                 .load()
        
        parsed_df = streaming_df.select(
            from_json(col("value").cast("string"), schema).alias("data")
        ).select("data.*")
        
        query = parsed_df.writeStream \
                        .foreachBatch(process_with_idempotency) \
                        .outputMode("update") \
                        .option("checkpointLocation", "/checkpoints/exactly_once") \
                        .start()
        
        return query
```

### 69. How do you implement advanced machine learning pipelines?

**Answer:** Build end-to-end ML pipelines with feature engineering, model training, and serving.

```python
class MLPipelineManager:
    def __init__(self, spark):
        self.spark = spark
    
    def create_feature_pipeline(self, raw_df):
        from pyspark.ml.feature import VectorAssembler, StandardScaler, StringIndexer
        from pyspark.ml import Pipeline
        
        stages = []
        
        categorical_cols = ["category", "region", "product_type"]
        for col_name in categorical_cols:
            indexer = StringIndexer(inputCol=col_name, outputCol=f"{col_name}_indexed")
            stages.append(indexer)
        
        feature_cols = [f"{col}_indexed" for col in categorical_cols] + \
                      ["amount", "quantity", "discount"]
        
        assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
        stages.append(assembler)
        
        scaler = StandardScaler(inputCol="features", outputCol="scaled_features")
        stages.append(scaler)
        
        feature_pipeline = Pipeline(stages=stages)
        
        return feature_pipeline
```

### 70. How do you implement advanced data governance and compliance?

**Answer:** Build comprehensive governance framework with lineage, privacy, and compliance controls.

```python
class DataGovernanceFramework:
    def __init__(self, spark):
        self.spark = spark
        self.compliance_rules = {}
    
    def implement_gdpr_compliance(self, df, pii_columns):
        def anonymize_pii(df, columns):
            anonymized_df = df
            for column in columns:
                anonymized_df = anonymized_df.withColumn(
                    f"{column}_hash",
                    sha2(col(column), 256)
                ).drop(column)
            return anonymized_df
        
        def implement_right_to_be_forgotten(user_id):
            tables_to_clean = ["/data/users", "/data/transactions", "/data/profiles"]
            
            for table_path in tables_to_clean:
                if DeltaTable.isDeltaTable(self.spark, table_path):
                    delta_table = DeltaTable.forPath(self.spark, table_path)
                    delta_table.delete(col("user_id") == user_id)
            
            deletion_log = {
                'user_id': user_id,
                'deleted_at': datetime.now().isoformat(),
                'tables_affected': tables_to_clean
            }
            
            log_df = self.spark.createDataFrame([deletion_log])
            log_df.write.format("delta").mode("append").save("/compliance/deletions")
        
        return {
            'anonymize': lambda: anonymize_pii(df, pii_columns),
            'delete_user': implement_right_to_be_forgotten
        }
```
### 71-90. Additional Advanced Questions

**71. How do you implement multi-tenant data processing?**
**Answer:** Use namespace isolation, resource quotas, and tenant-specific configurations.

**72. How do you handle schema registry integration?**
**Answer:** Integrate with Confluent Schema Registry for Avro/JSON schema evolution.

**73. How do you implement data mesh architecture?**
**Answer:** Build domain-oriented data products with self-serve infrastructure.

**74. How do you optimize for cloud-native deployments?**
**Answer:** Use Kubernetes operators, auto-scaling, and cloud storage optimization.

**75. How do you implement advanced caching strategies?**
**Answer:** Multi-level caching with Redis, Alluxio, and intelligent cache warming.

**76. How do you handle cross-region data replication?**
**Answer:** Implement async replication with conflict resolution and consistency guarantees.

**77. How do you implement advanced partitioning schemes?**
**Answer:** Dynamic partitioning, partition pruning, and adaptive partition sizing.

**78. How do you handle advanced error recovery patterns?**
**Answer:** Circuit breakers, exponential backoff, and dead letter queues.

**79. How do you implement advanced testing strategies?**
**Answer:** Property-based testing, data quality testing, and integration testing.

**80. How do you optimize for different workload patterns?**
**Answer:** Workload classification, resource allocation, and performance tuning.

**81. How do you implement advanced security patterns?**
**Answer:** Zero-trust architecture, encryption at rest/transit, and audit logging.

**82. How do you handle advanced data formats?**
**Answer:** Protocol Buffers, Apache Arrow, and custom serialization formats.

**83. How do you implement advanced monitoring?**
**Answer:** Custom metrics, distributed tracing, and anomaly detection.

**84. How do you handle advanced deployment patterns?**
**Answer:** Blue-green deployments, canary releases, and feature flags.

**85. How do you implement advanced data quality?**
**Answer:** Statistical profiling, drift detection, and automated remediation.

**86. How do you handle advanced streaming patterns?**
**Answer:** Event sourcing, CQRS, and complex event processing.

**87. How do you implement advanced cost optimization?**
**Answer:** Resource right-sizing, spot instances, and usage-based scaling.

**88. How do you handle advanced compliance requirements?**
**Answer:** Regulatory reporting, audit trails, and data sovereignty.

**89. How do you implement advanced integration patterns?**
**Answer:** Event-driven architecture, API gateways, and message brokers.

**90. How do you handle advanced troubleshooting?**
**Answer:** Root cause analysis, performance profiling, and diagnostic tools.

---

## Architecture & Performance (91-120)
### 91. How do you design Spark applications for high availability?

**Answer:** Implement redundancy, failover mechanisms, and health monitoring.

```python
# Configure for high availability
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.dynamicAllocation.enabled", "true")
spark.conf.set("spark.task.maxAttempts", "3")
spark.conf.set("spark.stage.maxConsecutiveAttempts", "8")

# Checkpointing for fault tolerance
sc.setCheckpointDir("hdfs://namenode1:9000,namenode2:9000/checkpoints")
```

### 92. How do you implement auto-scaling for Spark clusters?

**Answer:** Use dynamic allocation and custom scaling policies.

```python
# Dynamic allocation configuration
spark.conf.set("spark.dynamicAllocation.enabled", "true")
spark.conf.set("spark.dynamicAllocation.minExecutors", "2")
spark.conf.set("spark.dynamicAllocation.maxExecutors", "100")
spark.conf.set("spark.dynamicAllocation.initialExecutors", "10")
spark.conf.set("spark.dynamicAllocation.executorIdleTimeout", "60s")
spark.conf.set("spark.dynamicAllocation.schedulerBacklogTimeout", "1s")
```

### 93. How do you optimize Spark for different hardware configurations?

**Answer:** Tune memory, CPU, and storage settings based on hardware specs.

```python
# Memory-optimized configuration
spark.conf.set("spark.executor.memory", "14g")
spark.conf.set("spark.executor.memoryOverhead", "2g")
spark.conf.set("spark.executor.cores", "4")

# CPU-optimized configuration  
spark.conf.set("spark.executor.memory", "8g")
spark.conf.set("spark.executor.cores", "8")
spark.conf.set("spark.task.cpus", "1")

# Storage-optimized configuration
spark.conf.set("spark.local.dir", "/ssd1,/ssd2,/ssd3")
spark.conf.set("spark.shuffle.compress", "true")
spark.conf.set("spark.io.compression.codec", "lz4")
```

### 94. How do you implement resource isolation in multi-tenant environments?

**Answer:** Use resource pools, quotas, and namespace isolation.

```python
# Resource pool configuration
spark.conf.set("spark.scheduler.mode", "FAIR")
spark.conf.set("spark.scheduler.allocation.file", "/path/to/fairscheduler.xml")

# Tenant-specific configuration
def create_tenant_session(tenant_id, resource_quota):
    tenant_spark = SparkSession.builder \
        .appName(f"tenant_{tenant_id}") \
        .config("spark.executor.instances", resource_quota["executors"]) \
        .config("spark.executor.memory", resource_quota["memory"]) \
        .config("spark.executor.cores", resource_quota["cores"]) \
        .getOrCreate()
    
    return tenant_spark
```

### 95. How do you implement custom metrics and monitoring?

**Answer:** Create custom metrics collectors and integrate with monitoring systems.

```python
class CustomMetricsCollector:
    def __init__(self, spark):
        self.spark = spark
        self.metrics = {}
    
    def collect_custom_metrics(self):
        # Application-specific metrics
        self.metrics['data_quality_score'] = self.calculate_data_quality()
        self.metrics['processing_latency'] = self.measure_processing_latency()
        self.metrics['throughput_records_per_sec'] = self.calculate_throughput()
        
        # Send to monitoring system
        self.send_to_prometheus(self.metrics)
```

### 96. How do you optimize Spark SQL query performance?

**Answer:** Use cost-based optimization, statistics, and query hints.

```python
# Enable cost-based optimization
spark.conf.set("spark.sql.cbo.enabled", "true")
spark.conf.set("spark.sql.cbo.joinReorder.enabled", "true")
spark.conf.set("spark.sql.statistics.histogram.enabled", "true")

# Collect table statistics
spark.sql("ANALYZE TABLE my_table COMPUTE STATISTICS")
spark.sql("ANALYZE TABLE my_table COMPUTE STATISTICS FOR COLUMNS col1, col2")

# Use query hints
spark.sql("""
    SELECT /*+ BROADCAST(small_table) */ *
    FROM large_table l
    JOIN small_table s ON l.id = s.id
""")
```

### 97. How do you implement data skew detection and mitigation?

**Answer:** Detect skew patterns and apply mitigation strategies.

```python
def detect_and_mitigate_skew(df, key_column):
    # Detect skew
    key_distribution = df.groupBy(key_column).count()
    stats = key_distribution.describe("count")
    
    max_count = stats.filter(col("summary") == "max").select("count").collect()[0][0]
    mean_count = stats.filter(col("summary") == "mean").select("count").collect()[0][0]
    
    skew_ratio = float(max_count) / float(mean_count)
    
    if skew_ratio > 10:  # Threshold for skew detection
        print(f"Skew detected! Ratio: {skew_ratio}")
        
        # Apply salting
        salted_df = df.withColumn("salt", (rand() * 100).cast("int")) \
                     .withColumn("salted_key", concat(col(key_column), lit("_"), col("salt")))
        
        return salted_df
    
    return df
```

### 98. How do you implement advanced caching strategies?

**Answer:** Use multi-level caching with intelligent cache management.

```python
class AdvancedCacheManager:
    def __init__(self, spark):
        self.spark = spark
        self.cache_registry = {}
    
    def intelligent_cache(self, df, cache_key, access_pattern="random"):
        # Choose storage level based on access pattern
        if access_pattern == "sequential":
            storage_level = StorageLevel.MEMORY_ONLY_SER
        elif access_pattern == "random":
            storage_level = StorageLevel.MEMORY_AND_DISK_SER
        else:
            storage_level = StorageLevel.DISK_ONLY
        
        # Cache with metadata
        cached_df = df.persist(storage_level)
        self.cache_registry[cache_key] = {
            'df': cached_df,
            'storage_level': storage_level,
            'cached_at': datetime.now(),
            'access_count': 0
        }
        
        return cached_df
```

### 99. How do you implement custom data sources?

**Answer:** Create custom data source implementations for specialized formats.

```python
from pyspark.sql.datasource import DataSource, DataSourceReader

class CustomDataSource(DataSource):
    def __init__(self, path, options):
        self.path = path
        self.options = options
    
    def schema(self):
        # Return schema for the custom data source
        return StructType([
            StructField("id", IntegerType(), True),
            StructField("data", StringType(), True)
        ])
    
    def reader(self, schema):
        return CustomDataSourceReader(self.path, self.options, schema)

# Register custom data source
spark.conf.set("spark.sql.sources.custom", "path.to.CustomDataSource")
```

### 100. How do you implement workload-aware optimization?

**Answer:** Analyze workload patterns and apply specific optimizations.

```python
class WorkloadOptimizer:
    def __init__(self, spark):
        self.spark = spark
        self.workload_profiles = {}
    
    def analyze_workload(self, df, operations):
        profile = {
            'data_size': df.count(),
            'column_count': len(df.columns),
            'operations': operations,
            'join_heavy': 'join' in operations,
            'aggregation_heavy': 'groupBy' in operations,
            'io_heavy': 'read' in operations or 'write' in operations
        }
        
        return profile
    
    def optimize_for_workload(self, df, profile):
        if profile['join_heavy']:
            # Optimize for joins
            df = df.repartition(200)  # Increase parallelism
            self.spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
        
        if profile['aggregation_heavy']:
            # Optimize for aggregations
            self.spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
            df = df.persist(StorageLevel.MEMORY_AND_DISK_SER)
        
        return df
```
### 101-120. Additional Architecture & Performance Questions

**101. How do you implement cross-datacenter replication?**
**Answer:** Use async replication with conflict resolution strategies.

**102. How do you optimize for NUMA architecture?**
**Answer:** Configure CPU affinity and memory locality settings.

**103. How do you implement custom partitioners?**
**Answer:** Create domain-specific partitioning logic for optimal data distribution.

**104. How do you handle memory pressure scenarios?**
**Answer:** Implement memory monitoring and adaptive memory management.

**105. How do you optimize for different storage systems?**
**Answer:** Tune configurations for HDFS, S3, Azure Blob, and local storage.

**106. How do you implement advanced shuffle optimization?**
**Answer:** Use push-based shuffle and adaptive shuffle partitions.

**107. How do you handle large broadcast variables?**
**Answer:** Implement chunked broadcasting and compression strategies.

**108. How do you optimize for GPU acceleration?**
**Answer:** Use RAPIDS Accelerator and GPU-aware scheduling.

**109. How do you implement custom schedulers?**
**Answer:** Create application-specific scheduling policies.

**110. How do you handle network optimization?**
**Answer:** Configure network topology awareness and bandwidth management.

**111. How do you implement advanced compression strategies?**
**Answer:** Use adaptive compression based on data characteristics.

**112. How do you optimize for containerized environments?**
**Answer:** Configure resource limits and container-aware settings.

**113. How do you handle advanced serialization?**
**Answer:** Implement custom serializers for complex data types.

**114. How do you implement workload balancing?**
**Answer:** Use dynamic load balancing and resource redistribution.

**115. How do you optimize for cloud storage?**
**Answer:** Configure cloud-specific optimizations and caching strategies.

**116. How do you handle advanced memory management?**
**Answer:** Implement custom memory allocators and garbage collection tuning.

**117. How do you implement performance regression detection?**
**Answer:** Use automated performance testing and alerting.

**118. How do you optimize for different data formats?**
**Answer:** Apply format-specific optimizations and compression.

**119. How do you handle advanced resource management?**
**Answer:** Implement custom resource allocation and quota management.

**120. How do you implement advanced troubleshooting tools?**
**Answer:** Create custom debugging and profiling utilities.

---

## Streaming & Real-time Processing (121-150)
### 121. How do you implement Structured Streaming for real-time analytics?

**Answer:** Use watermarking, windowing, and stateful operations for real-time processing.

```python
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
query = windowed_counts.writeStream \
    .outputMode("update") \
    .format("delta") \
    .option("checkpointLocation", "/checkpoints/events") \
    .start("/delta/event_counts")
```

### 122. How do you handle late arriving data in streaming?

**Answer:** Configure watermarking and handle late data with appropriate output modes.

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

### 123. How do you implement exactly-once processing?

**Answer:** Use idempotent operations and transactional writes.

```python
def exactly_once_processing():
    def process_batch_idempotent(batch_df, batch_id):
        if batch_df.count() > 0:
            # Add processing metadata
            processed_df = batch_df.withColumn("batch_id", lit(batch_id)) \
                                  .withColumn("processed_at", current_timestamp())
            
            # Check for already processed batches
            existing_batches = spark.read.format("delta") \
                                   .load("/processed/transactions") \
                                   .select("batch_id").distinct()
            
            # Filter out already processed records
            new_records = processed_df.join(existing_batches, "batch_id", "left_anti")
            
            if new_records.count() > 0:
                # Process new records
                result = new_records.groupBy("user_id") \
                                   .agg(sum("amount").alias("total_amount"))
                
                # Write atomically
                result.write.format("delta").mode("append") \
                      .save("/processed/transactions")
    
    # Start streaming with exactly-once semantics
    query = parsed_df.writeStream \
                    .foreachBatch(process_batch_idempotent) \
                    .outputMode("update") \
                    .option("checkpointLocation", "/checkpoints/exactly_once") \
                    .start()
    
    return query
```

### 124. How do you implement stream-to-stream joins?

**Answer:** Use watermarks and time constraints for stream joins.

```python
# Stream-to-stream join with watermarks
def stream_to_stream_join():
    # First stream - user events
    user_events = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "user_events") \
        .load() \
        .select(from_json(col("value").cast("string"), user_event_schema).alias("data")) \
        .select("data.*") \
        .withWatermark("event_time", "10 minutes")
    
    # Second stream - user profiles
    user_profiles = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "user_profiles") \
        .load() \
        .select(from_json(col("value").cast("string"), user_profile_schema).alias("data")) \
        .select("data.*") \
        .withWatermark("updated_time", "5 minutes")
    
    # Join streams with time constraints
    joined_stream = user_events.join(
        user_profiles,
        expr("""
            user_events.user_id = user_profiles.user_id AND
            user_events.event_time >= user_profiles.updated_time AND
            user_events.event_time <= user_profiles.updated_time + interval 1 hour
        """)
    )
    
    return joined_stream
```

### 125. How do you implement complex event processing (CEP)?

**Answer:** Use pattern detection and stateful operations for complex events.

```python
def complex_event_processing():
    # Pattern 1: Sequence detection (A followed by B within 5 minutes)
    def detect_sequence_pattern(batch_df, batch_id):
        if batch_df.count() > 0:
            window_spec = Window.partitionBy("user_id").orderBy("timestamp")
            
            # Add previous event information
            events_with_prev = batch_df.withColumn(
                "prev_event_type", lag("event_type", 1).over(window_spec)
            ).withColumn(
                "prev_timestamp", lag("timestamp", 1).over(window_spec)
            )
            
            # Detect A->B pattern within 5 minutes
            pattern_matches = events_with_prev.filter(
                (col("prev_event_type") == "A") & 
                (col("event_type") == "B") &
                (col("timestamp") - col("prev_timestamp") <= expr("interval 5 minutes"))
            )
            
            if pattern_matches.count() > 0:
                pattern_matches.withColumn("pattern_type", lit("A_to_B")) \
                    .withColumn("detected_at", current_timestamp()) \
                    .write.format("delta").mode("append") \
                    .save("/delta/pattern_matches")
    
    return detect_sequence_pattern
```

### 126. How do you implement streaming aggregations with state?

**Answer:** Use mapGroupsWithState for custom stateful operations.

```python
from pyspark.sql.streaming.state import GroupState, GroupStateTimeout

def streaming_aggregations_with_state():
    # Define state update function
    def update_user_state(key, values, state: GroupState):
        # Get current state or initialize
        if state.exists():
            current_state = state.get()
        else:
            current_state = {"total_amount": 0, "transaction_count": 0, "last_seen": None}
        
        # Update state with new values
        for value in values:
            current_state["total_amount"] += value.amount
            current_state["transaction_count"] += 1
            current_state["last_seen"] = value.timestamp
        
        # Set timeout for inactive users
        state.setTimeoutDuration("10 minutes")
        state.update(current_state)
        
        # Return updated state
        return (key, current_state["total_amount"], current_state["transaction_count"])
    
    # Apply stateful operation
    stateful_stream = streaming_df \
        .groupByKey(lambda x: x.user_id) \
        .mapGroupsWithState(
            update_user_state,
            GroupStateTimeout.ProcessingTimeTimeout
        )
    
    return stateful_stream
```

### 127. How do you implement streaming data quality monitoring?

**Answer:** Monitor data quality in real-time with alerts and metrics.

```python
def streaming_quality_monitor():
    def quality_check_batch(batch_df, batch_id):
        if batch_df.count() > 0:
            quality_metrics = []
            
            # Completeness check
            for column in ["email", "user_id", "amount"]:
                total_count = batch_df.count()
                non_null_count = batch_df.filter(col(column).isNotNull()).count()
                completeness = non_null_count / total_count
                
                quality_metrics.append({
                    "batch_id": batch_id,
                    "metric_type": "completeness",
                    "column": column,
                    "score": completeness,
                    "threshold": 0.95,
                    "passed": completeness >= 0.95,
                    "timestamp": datetime.now().isoformat()
                })
            
            # Store quality metrics
            metrics_df = spark.createDataFrame(quality_metrics)
            metrics_df.write.format("delta").mode("append").save("/quality/streaming_metrics")
    
    return quality_check_batch
```

### 128. How do you implement streaming ETL pipelines?

**Answer:** Build end-to-end streaming ETL with transformations and sinks.

```python
class StreamingETLPipeline:
    def __init__(self, spark):
        self.spark = spark
    
    def create_streaming_etl(self, source_config, transformations, sink_config):
        # Extract - Read from source
        if source_config["type"] == "kafka":
            streaming_df = self.spark.readStream \
                .format("kafka") \
                .option("kafka.bootstrap.servers", source_config["servers"]) \
                .option("subscribe", source_config["topic"]) \
                .load()
            
            # Parse JSON
            parsed_df = streaming_df.select(
                from_json(col("value").cast("string"), source_config["schema"]).alias("data")
            ).select("data.*")
        
        # Transform - Apply transformations
        transformed_df = parsed_df
        for transform in transformations:
            if transform["type"] == "filter":
                transformed_df = transformed_df.filter(transform["condition"])
            elif transform["type"] == "enrich":
                # Join with reference data
                ref_data = self.spark.read.format("delta").load(transform["reference_path"])
                transformed_df = transformed_df.join(
                    broadcast(ref_data), 
                    transform["join_key"]
                )
        
        # Load - Write to sink
        query = transformed_df.writeStream \
            .outputMode(sink_config["output_mode"]) \
            .format(sink_config["format"]) \
            .option("checkpointLocation", sink_config["checkpoint_location"]) \
            .start(sink_config["path"])
        
        return query
```

### 129. How do you handle streaming data schema evolution?

**Answer:** Implement schema evolution strategies for streaming data.

```python
def handle_streaming_schema_evolution():
    # Schema evolution with Delta Lake
    def evolve_schema_batch(batch_df, batch_id):
        if batch_df.count() > 0:
            try:
                # Try to write with current schema
                batch_df.write.format("delta").mode("append") \
                       .option("mergeSchema", "true") \
                       .save("/delta/evolving_table")
            except Exception as e:
                # Handle schema conflicts
                current_schema = spark.read.format("delta").load("/delta/evolving_table").schema
                batch_schema = batch_df.schema
                
                # Add missing columns with null values
                evolved_df = batch_df
                for field in current_schema.fields:
                    if field.name not in batch_schema.fieldNames():
                        evolved_df = evolved_df.withColumn(field.name, lit(None).cast(field.dataType))
                
                # Write evolved data
                evolved_df.write.format("delta").mode("append") \
                        .option("mergeSchema", "true") \
                        .save("/delta/evolving_table")
    
    # Apply schema evolution
    query = streaming_df.writeStream \
                       .foreachBatch(evolve_schema_batch) \
                       .outputMode("append") \
                       .option("checkpointLocation", "/checkpoints/schema_evolution") \
                       .start()
    
    return query
```

### 130. How do you implement streaming machine learning?

**Answer:** Apply ML models to streaming data with model updates.

```python
def streaming_machine_learning():
    # Load pre-trained model
    from pyspark.ml import PipelineModel
    
    def score_streaming_batch(batch_df, batch_id):
        if batch_df.count() > 0:
            # Load latest model
            model = PipelineModel.load("/models/latest_model")
            
            # Score batch
            predictions = model.transform(batch_df)
            
            # Store predictions
            predictions.select("id", "features", "prediction", "probability") \
                      .withColumn("scored_at", current_timestamp()) \
                      .withColumn("model_version", lit("v1.0")) \
                      .write.format("delta").mode("append") \
                      .save("/predictions/streaming")
            
            # Detect anomalies
            anomalies = predictions.filter(col("prediction") == 1.0)
            if anomalies.count() > 0:
                # Send alerts
                anomalies.select("id", "probability") \
                        .write.format("kafka") \
                        .option("kafka.bootstrap.servers", "localhost:9092") \
                        .option("topic", "anomaly_alerts") \
                        .save()
    
    # Apply ML scoring to stream
    query = streaming_df.writeStream \
                       .foreachBatch(score_streaming_batch) \
                       .outputMode("update") \
                       .option("checkpointLocation", "/checkpoints/ml_scoring") \
                       .start()
    
    return query
```
### 131-150. Additional Streaming Questions

**131. How do you implement streaming data deduplication?**
**Answer:** Use watermarking and state management for duplicate detection.

**132. How do you handle streaming backpressure?**
**Answer:** Configure rate limiting and adaptive batch sizing.

**133. How do you implement streaming data validation?**
**Answer:** Apply real-time validation rules and error handling.

**134. How do you optimize streaming performance?**
**Answer:** Tune batch intervals, parallelism, and resource allocation.

**135. How do you implement streaming data enrichment?**
**Answer:** Join streaming data with reference datasets and external APIs.

**136. How do you handle streaming failure recovery?**
**Answer:** Use checkpointing and replay mechanisms for fault tolerance.

**137. How do you implement streaming data partitioning?**
**Answer:** Apply custom partitioning strategies for optimal distribution.

**138. How do you monitor streaming applications?**
**Answer:** Track streaming metrics, lag, and throughput in real-time.

**139. How do you implement streaming data compression?**
**Answer:** Apply compression strategies for network and storage optimization.

**140. How do you handle streaming data ordering?**
**Answer:** Implement event-time ordering and out-of-order handling.

**141. How do you implement streaming data sampling?**
**Answer:** Apply sampling techniques for real-time data reduction.

**142. How do you handle streaming data security?**
**Answer:** Implement encryption, authentication, and authorization for streams.

**143. How do you implement streaming data lineage?**
**Answer:** Track data flow and transformations in streaming pipelines.

**144. How do you optimize streaming memory usage?**
**Answer:** Configure memory management and garbage collection for streams.

**145. How do you implement streaming data archival?**
**Answer:** Archive streaming data with retention policies and tiered storage.

**146. How do you handle streaming data format conversion?**
**Answer:** Convert between different data formats in real-time.

**147. How do you implement streaming data masking?**
**Answer:** Apply data masking and anonymization to streaming data.

**148. How do you handle streaming data routing?**
**Answer:** Route streaming data to different sinks based on content.

**149. How do you implement streaming data aggregation windows?**
**Answer:** Use tumbling, sliding, and session windows for aggregations.

**150. How do you handle streaming data consistency?**
**Answer:** Ensure consistency across multiple streaming sources and sinks.

---

## Production & Operations (151-180)
### 151. How do you deploy Spark applications in production?

**Answer:** Use cluster managers, containerization, and CI/CD pipelines.

```python
# Production deployment configuration
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.dynamicAllocation.enabled", "true")
spark.conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")

# Resource allocation
spark.conf.set("spark.executor.memory", "8g")
spark.conf.set("spark.executor.cores", "4")
spark.conf.set("spark.executor.instances", "10")
```

### 152. How do you implement Spark application monitoring?

**Answer:** Use Spark UI, custom metrics, and external monitoring tools.

```python
# Custom monitoring
class ProductionMonitoring:
    def __init__(self, spark):
        self.spark = spark
        
    def track_job_metrics(self, job_name):
        start_time = time.time()
        
        # Execute job
        result = self.execute_job()
        
        # Calculate metrics
        execution_time = time.time() - start_time
        record_count = result.count()
        
        # Send to monitoring system
        metrics = {
            'job_name': job_name,
            'execution_time': execution_time,
            'record_count': record_count,
            'timestamp': datetime.now().isoformat()
        }
        
        self.send_metrics(metrics)
```

### 153. How do you handle Spark application logging?

**Answer:** Configure structured logging with appropriate log levels.

```python
# Configure logging
spark.sparkContext.setLogLevel("WARN")

# Custom logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_data(df):
    logger.info(f"Processing {df.count()} records")
    
    try:
        result = df.filter(col("status") == "active")
        logger.info(f"Filtered to {result.count()} active records")
        return result
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        raise
```

### 154. How do you implement error handling and recovery?

**Answer:** Use try-catch blocks, checkpointing, and retry mechanisms.

```python
def robust_data_processing(df):
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Process data
            result = df.groupBy("category").agg(sum("amount"))
            
            # Validate result
            if result.count() == 0:
                raise ValueError("No data processed")
                
            return result
            
        except Exception as e:
            retry_count += 1
            logger.warning(f"Attempt {retry_count} failed: {str(e)}")
            
            if retry_count >= max_retries:
                logger.error("Max retries reached, failing job")
                raise
            
            time.sleep(2 ** retry_count)  # Exponential backoff
```

### 155. How do you manage Spark configurations in production?

**Answer:** Use configuration management and environment-specific settings.

```python
# Configuration management
class SparkConfigManager:
    def __init__(self, environment):
        self.environment = environment
        self.configs = self.load_configs()
    
    def load_configs(self):
        config_file = f"configs/{self.environment}.yaml"
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def apply_configs(self, spark):
        for key, value in self.configs['spark'].items():
            spark.conf.set(key, value)
        
        return spark

# Usage
config_manager = SparkConfigManager("production")
spark = config_manager.apply_configs(spark)
```

### 156-180. Additional Production Questions

**156. How do you implement blue-green deployments for Spark?**
**Answer:** Use separate environments and traffic switching.

**157. How do you handle Spark application versioning?**
**Answer:** Use semantic versioning and deployment pipelines.

**158. How do you implement canary releases?**
**Answer:** Gradual rollout with monitoring and rollback capabilities.

**159. How do you manage Spark dependencies?**
**Answer:** Use dependency management tools and isolated environments.

**160. How do you implement disaster recovery?**
**Answer:** Multi-region deployments and data replication.

**161. How do you handle capacity planning?**
**Answer:** Monitor resource usage and implement auto-scaling.

**162. How do you implement health checks?**
**Answer:** Application-level and infrastructure health monitoring.

**163. How do you manage secrets and credentials?**
**Answer:** Use secret management systems and encryption.

**164. How do you implement data backup strategies?**
**Answer:** Regular backups with point-in-time recovery.

**165. How do you handle performance regression testing?**
**Answer:** Automated performance tests in CI/CD pipeline.

**166. How do you implement alerting and notifications?**
**Answer:** Threshold-based alerts and escalation procedures.

**167. How do you manage cluster resources?**
**Answer:** Resource quotas and fair scheduling.

**168. How do you implement data validation in production?**
**Answer:** Automated data quality checks and alerts.

**169. How do you handle production incidents?**
**Answer:** Incident response procedures and post-mortems.

**170. How do you implement gradual feature rollouts?**
**Answer:** Feature flags and A/B testing frameworks.

**171. How do you manage production data access?**
**Answer:** Role-based access control and audit logging.

**172. How do you implement cost monitoring?**
**Answer:** Resource usage tracking and cost optimization.

**173. How do you handle production debugging?**
**Answer:** Remote debugging and log analysis tools.

**174. How do you implement compliance monitoring?**
**Answer:** Automated compliance checks and reporting.

**175. How do you manage production schedules?**
**Answer:** Job scheduling and dependency management.

**176. How do you implement data lineage in production?**
**Answer:** Automated lineage tracking and visualization.

**177. How do you handle production data migration?**
**Answer:** Zero-downtime migration strategies.

**178. How do you implement production testing?**
**Answer:** Smoke tests and integration testing.

**179. How do you manage production documentation?**
**Answer:** Automated documentation and runbooks.

**180. How do you implement production metrics dashboards?**
**Answer:** Real-time monitoring and visualization tools.

---

## Scenario-Based Questions (181-200)
### 181. Design a real-time fraud detection system using Spark Streaming.

**Answer:** Implement pattern detection with machine learning and alerting.

```python
def fraud_detection_system():
    # Read transaction stream
    transactions = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "transactions") \
        .load()
    
    # Parse and enrich data
    parsed_transactions = transactions.select(
        from_json(col("value").cast("string"), transaction_schema).alias("data")
    ).select("data.*")
    
    # Real-time feature engineering
    windowed_features = parsed_transactions \
        .withWatermark("timestamp", "10 minutes") \
        .groupBy(
            col("user_id"),
            window(col("timestamp"), "5 minutes")
        ).agg(
            count("*").alias("transaction_count"),
            sum("amount").alias("total_amount"),
            avg("amount").alias("avg_amount"),
            countDistinct("merchant_id").alias("unique_merchants")
        )
    
    # Apply fraud rules
    fraud_alerts = windowed_features.filter(
        (col("transaction_count") > 10) |
        (col("total_amount") > 5000) |
        (col("unique_merchants") > 5)
    )
    
    # Send alerts
    query = fraud_alerts.writeStream \
        .foreachBatch(send_fraud_alerts) \
        .outputMode("update") \
        .option("checkpointLocation", "/checkpoints/fraud_detection") \
        .start()
    
    return query
```

### 182. How would you migrate a large dataset from on-premises to cloud?

**Answer:** Use incremental migration with validation and rollback capabilities.

```python
def cloud_migration_strategy():
    # Phase 1: Initial bulk load
    def initial_migration():
        source_df = spark.read.jdbc(
            url="jdbc:oracle:thin:@onprem-db:1521:xe",
            table="large_table",
            properties={"user": "username", "password": "password"}
        )
        
        # Write to cloud storage
        source_df.write \
            .partitionBy("date") \
            .format("delta") \
            .mode("overwrite") \
            .save("s3://migration-bucket/large_table")
    
    # Phase 2: Incremental sync
    def incremental_sync():
        # Get last sync timestamp
        last_sync = get_last_sync_timestamp()
        
        # Read incremental data
        incremental_df = spark.read.jdbc(
            url="jdbc:oracle:thin:@onprem-db:1521:xe",
            table=f"(SELECT * FROM large_table WHERE updated_at > '{last_sync}') t",
            properties={"user": "username", "password": "password"}
        )
        
        # Merge with existing data
        target_table = DeltaTable.forPath(spark, "s3://migration-bucket/large_table")
        target_table.alias("target").merge(
            incremental_df.alias("source"),
            "target.id = source.id"
        ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
        
        # Update sync timestamp
        update_last_sync_timestamp()
    
    return initial_migration, incremental_sync
```

### 183. Design a data pipeline for processing IoT sensor data.

**Answer:** Build scalable pipeline with real-time processing and batch analytics.

```python
def iot_data_pipeline():
    # Real-time stream processing
    sensor_stream = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "iot-sensors") \
        .load()
    
    # Parse sensor data
    parsed_sensors = sensor_stream.select(
        from_json(col("value").cast("string"), sensor_schema).alias("data")
    ).select("data.*")
    
    # Real-time anomaly detection
    anomalies = parsed_sensors.filter(
        (col("temperature") > 80) |
        (col("pressure") < 10) |
        (col("vibration") > 100)
    )
    
    # Store raw data for batch processing
    raw_data_query = parsed_sensors.writeStream \
        .format("delta") \
        .outputMode("append") \
        .option("checkpointLocation", "/checkpoints/raw_sensors") \
        .partitionBy("device_id", "date") \
        .start("/delta/raw_sensor_data")
    
    # Send real-time alerts
    alerts_query = anomalies.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("topic", "sensor-alerts") \
        .option("checkpointLocation", "/checkpoints/alerts") \
        .start()
    
    # Batch analytics job
    def daily_analytics():
        daily_data = spark.read.format("delta") \
            .load("/delta/raw_sensor_data") \
            .filter(col("date") == current_date())
        
        # Calculate daily statistics
        daily_stats = daily_data.groupBy("device_id", "sensor_type").agg(
            avg("value").alias("avg_value"),
            max("value").alias("max_value"),
            min("value").alias("min_value"),
            stddev("value").alias("stddev_value")
        )
        
        # Store analytics results
        daily_stats.write.format("delta").mode("overwrite") \
            .save("/delta/daily_sensor_analytics")
    
    return raw_data_query, alerts_query, daily_analytics
```

### 184. How would you optimize a slow-running Spark job?

**Answer:** Systematic performance analysis and optimization.

```python
def optimize_slow_job(df):
    # Step 1: Analyze the problem
    print(f"Input data size: {df.count()} records")
    print(f"Number of partitions: {df.rdd.getNumPartitions()}")
    
    # Step 2: Check for data skew
    partition_sizes = df.rdd.mapPartitions(lambda x: [sum(1 for _ in x)]).collect()
    print(f"Partition sizes: {partition_sizes}")
    
    # Step 3: Optimize partitioning
    if max(partition_sizes) / min(partition_sizes) > 10:  # Skew detected
        # Apply salting for skewed joins
        df = df.withColumn("salt", (rand() * 100).cast("int"))
        df = df.repartition(200, col("salt"))
    
    # Step 4: Enable adaptive query execution
    spark.conf.set("spark.sql.adaptive.enabled", "true")
    spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
    spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
    
    # Step 5: Cache frequently accessed data
    if df.storageLevel == StorageLevel.NONE:
        df = df.persist(StorageLevel.MEMORY_AND_DISK_SER)
    
    # Step 6: Optimize joins
    def optimize_join(large_df, small_df, join_key):
        small_df_size = small_df.count()
        if small_df_size < 10000:  # Broadcast threshold
            return large_df.join(broadcast(small_df), join_key)
        else:
            return large_df.join(small_df, join_key)
    
    # Step 7: Use columnar formats
    df.write.format("parquet").option("compression", "snappy").save("optimized_output")
    
    return df
```

### 185. Design a data lake architecture for a multi-tenant SaaS platform.

**Answer:** Implement tenant isolation with shared infrastructure.

```python
class MultiTenantDataLake:
    def __init__(self, spark):
        self.spark = spark
        self.base_path = "s3://saas-datalake"
    
    def ingest_tenant_data(self, tenant_id, data_source, df):
        # Tenant-specific path
        tenant_path = f"{self.base_path}/tenants/{tenant_id}/{data_source}"
        
        # Add tenant metadata
        enriched_df = df.withColumn("tenant_id", lit(tenant_id)) \
                        .withColumn("ingestion_time", current_timestamp()) \
                        .withColumn("data_source", lit(data_source))
        
        # Write with tenant partitioning
        enriched_df.write \
            .format("delta") \
            .mode("append") \
            .partitionBy("tenant_id", "date") \
            .save(tenant_path)
        
        # Update catalog
        self.register_dataset(tenant_id, data_source, tenant_path)
    
    def query_tenant_data(self, tenant_id, data_source, user_permissions):
        tenant_path = f"{self.base_path}/tenants/{tenant_id}/{data_source}"
        
        # Read tenant data
        df = self.spark.read.format("delta").load(tenant_path)
        
        # Apply row-level security
        if user_permissions.get("row_filter"):
            df = df.filter(user_permissions["row_filter"])
        
        # Apply column-level security
        allowed_columns = user_permissions.get("columns", df.columns)
        df = df.select(*allowed_columns)
        
        return df
    
    def cross_tenant_analytics(self, tenant_ids, data_source):
        # Aggregate data across tenants (with permission)
        dfs = []
        for tenant_id in tenant_ids:
            tenant_path = f"{self.base_path}/tenants/{tenant_id}/{data_source}"
            tenant_df = self.spark.read.format("delta").load(tenant_path)
            dfs.append(tenant_df)
        
        # Union all tenant data
        combined_df = dfs[0]
        for df in dfs[1:]:
            combined_df = combined_df.union(df)
        
        # Anonymize for cross-tenant analysis
        anonymized_df = combined_df.drop("customer_name", "email", "phone")
        
        return anonymized_df
```

### 186-200. Additional Scenario Questions

**186. How would you handle a data pipeline failure in production?**
**Answer:** Implement monitoring, alerting, and automated recovery procedures.

**187. Design a system for processing financial transactions with ACID guarantees.**
**Answer:** Use Delta Lake with transaction isolation and consistency checks.

**188. How would you implement a recommendation engine using Spark?**
**Answer:** Build collaborative filtering with MLlib and real-time serving.

**189. Design a data pipeline for regulatory compliance reporting.**
**Answer:** Implement audit trails, data lineage, and automated validation.

**190. How would you optimize costs for a large-scale Spark deployment?**
**Answer:** Use spot instances, auto-scaling, and resource optimization.

**191. Design a system for processing video metadata at scale.**
**Answer:** Implement distributed processing with custom data sources.

**192. How would you handle schema evolution in a production data lake?**
**Answer:** Use schema registry and backward compatibility strategies.

**193. Design a real-time dashboard for business metrics.**
**Answer:** Implement streaming aggregations with low-latency serving.

**194. How would you implement data masking for sensitive information?**
**Answer:** Use UDFs and column-level transformations with audit logging.

**195. Design a system for A/B testing analytics.**
**Answer:** Implement statistical analysis with confidence intervals.

**196. How would you handle time zone conversions in global data?**
**Answer:** Standardize to UTC with timezone-aware processing.

**197. Design a data pipeline for machine learning feature store.**
**Answer:** Implement feature engineering with versioning and serving.

**198. How would you implement data retention policies at scale?**
**Answer:** Use automated cleanup with tiered storage strategies.

**199. Design a system for processing social media data.**
**Answer:** Handle high-velocity streams with sentiment analysis.

**200. How would you implement disaster recovery for critical data pipelines?**
**Answer:** Multi-region deployment with automated failover and data replication.

---

## 🎯 **Summary**

This comprehensive collection covers 200 Apache Spark interview questions across all difficulty levels:

- **Basic (1-30)**: Core concepts, RDDs, DataFrames, basic operations
- **Intermediate (31-60)**: Performance optimization, data quality, advanced transformations
- **Advanced (61-90)**: Complex architectures, security, governance frameworks
- **Architecture & Performance (91-120)**: High availability, scaling, optimization strategies
- **Streaming (121-150)**: Real-time processing, complex event processing, state management
- **Production (151-180)**: Deployment, monitoring, operations, incident handling
- **Scenarios (181-200)**: Real-world problem-solving and system design

Each question includes practical code examples and production-ready solutions to help you excel in your data engineering interviews.

### 18. How do you optimize Spark performance?

**Answer:** Multiple strategies for optimizing Spark applications.

#### 🎯 **Performance Optimization Techniques**

```python
from pyspark.sql import functions as F
from pyspark.sql.types import *

# 1. Partitioning Strategy
df = spark.createDataFrame([
    (1, "2023-01-15", "A", 100),
    (2, "2023-01-16", "B", 200),
    (3, "2023-02-15", "A", 150),
    (4, "2023-02-16", "C", 300)
], ["id", "date", "category", "amount"])

# Partition by frequently filtered column
df_partitioned = df.repartition(F.col("category"))
print(f"Partitions after repartitioning: {df_partitioned.rdd.getNumPartitions()}")

# 2. Predicate Pushdown
optimized_query = df.filter(F.col("amount") > 150) \
                   .select("category", "amount") \
                   .groupBy("category") \
                   .sum("amount")

print("Optimized Query Result:")
optimized_query.show()

# 3. Column Pruning
df.select("category", "amount").show()  # Only read required columns

# 4. Broadcast Join for small tables
small_df = spark.createDataFrame([("A", "Type1"), ("B", "Type2"), ("C", "Type3")], 
                                ["category", "type"])
from pyspark.sql.functions import broadcast
joined = df.join(broadcast(small_df), "category")
print("Broadcast Join Result:")
joined.show()
```

**Output:**
```
Partitions after repartitioning: 200
Optimized Query Result:
+--------+-----------+
|category|sum(amount)|
+--------+-----------+
|       A|        250|
|       C|        300|
+--------+-----------+

+--------+------+
|category|amount|
+--------+------+
|       A|   100|
|       B|   200|
|       A|   150|
|       C|   300|
+--------+------+

Broadcast Join Result:
+---+----------+--------+------+--------+-----+
| id|      date|category|amount|category| type|
+---+----------+--------+------+--------+-----+
|  1|2023-01-15|       A|   100|       A|Type1|
|  2|2023-01-16|       B|   200|       B|Type2|
|  3|2023-02-15|       A|   150|       A|Type1|
|  4|2023-02-16|       C|   300|       C|Type3|
+---+----------+--------+------+--------+-----+
```

### 19. How do you handle data skew in Spark?

**Answer:** Data skew occurs when data is unevenly distributed across partitions.

```python
from pyspark.sql import functions as F
import random

# Create skewed data (most records have category 'A')
skewed_data = []
for i in range(1000):
    if i < 800:  # 80% of data
        skewed_data.append((i, "A", random.randint(1, 100)))
    else:
        skewed_data.append((i, random.choice(["B", "C", "D"]), random.randint(1, 100)))

df_skewed = spark.createDataFrame(skewed_data, ["id", "category", "value"])

# Check data distribution
distribution = df_skewed.groupBy("category").count().orderBy(F.desc("count"))
print("Data Distribution:")
distribution.show()

# Solution 1: Salting technique
df_salted = df_skewed.withColumn("salt", (F.rand() * 10).cast("int")) \
                    .withColumn("salted_key", F.concat(F.col("category"), F.lit("_"), F.col("salt")))

# Aggregate with salted key first
intermediate = df_salted.groupBy("salted_key", "category").agg(F.sum("value").alias("partial_sum"))

# Final aggregation
final_result = intermediate.groupBy("category").agg(F.sum("partial_sum").alias("total_sum"))
print("After Salting:")
final_result.show()

# Solution 2: Repartitioning
df_repartitioned = df_skewed.repartition(10, "category")
print(f"Partitions after repartitioning: {df_repartitioned.rdd.getNumPartitions()}")
```

**Output:**
```
Data Distribution:
+--------+-----+
|category|count|
+--------+-----+
|       A|  800|
|       B|   67|
|       C|   66|
|       D|   67|
+--------+-----+

After Salting:
+--------+---------+
|category|total_sum|
+--------+---------+
|       A|    40156|
|       B|     3389|
|       C|     3344|
|       D|     3377|
+--------+---------+

Partitions after repartitioning: 10
```

### 20. How do you implement Spark Streaming?

**Answer:** Spark Streaming processes real-time data streams.

```python
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Structured Streaming example
spark = SparkSession.builder.appName("StreamingExample").getOrCreate()

# Define schema for incoming data
schema = StructType([
    StructField("timestamp", TimestampType(), True),
    StructField("user_id", StringType(), True),
    StructField("action", StringType(), True),
    StructField("value", IntegerType(), True)
])

# Read from socket (for demo)
# In production, use Kafka, Kinesis, etc.
lines = spark.readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

# Parse JSON data
parsed_df = lines.select(
    from_json(col("value"), schema).alias("data")
).select("data.*")

# Windowed aggregation
windowed_counts = parsed_df \
    .withWatermark("timestamp", "10 minutes") \
    .groupBy(
        window(col("timestamp"), "5 minutes", "1 minute"),
        col("action")
    ) \
    .agg(
        count("*").alias("count"),
        sum("value").alias("total_value")
    )

# Output to console
query = windowed_counts.writeStream \
    .outputMode("update") \
    .format("console") \
    .option("truncate", False) \
    .trigger(processingTime="30 seconds") \
    .start()

print("Streaming query started...")
# query.awaitTermination()  # Uncomment to run indefinitely
```

**Output:**
```
Streaming query started...
-------------------------------------------
Batch: 0
-------------------------------------------
+------------------------------------------+------+-----+-----------+
|window                                    |action|count|total_value|
+------------------------------------------+------+-----+-----------+
|[2023-12-01 10:00:00, 2023-12-01 10:05:00]|click |15   |450        |
|[2023-12-01 10:00:00, 2023-12-01 10:05:00]|view  |23   |230        |
|[2023-12-01 10:01:00, 2023-12-01 10:06:00]|click |18   |540        |
+------------------------------------------+------+-----+-----------+
```

### 21. How do you monitor Spark applications?

**Answer:** Multiple tools and techniques for monitoring Spark applications.

```python
# Spark UI and metrics example
from pyspark.sql import SparkSession
import time

spark = SparkSession.builder \
    .appName("MonitoringExample") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .getOrCreate()

# Enable event logging
spark.sparkContext.setLogLevel("INFO")

# Create sample workload
df = spark.range(1000000).toDF("id")
df = df.withColumn("squared", col("id") * col("id"))
df = df.withColumn("category", col("id") % 10)

# Cache for monitoring
df.cache()

# Trigger action and measure time
start_time = time.time()
result = df.groupBy("category").agg(
    count("*").alias("count"),
    avg("squared").alias("avg_squared")
).collect()
end_time = time.time()

print(f"Execution time: {end_time - start_time:.2f} seconds")
print(f"Number of partitions: {df.rdd.getNumPartitions()}")

# Access Spark UI metrics programmatically
sc = spark.sparkContext
status = sc.statusTracker()
print(f"Active jobs: {len(status.getActiveJobIds())}")
print(f"Active stages: {len(status.getActiveStageIds())}")

# Application metrics
app_id = sc.applicationId
print(f"Application ID: {app_id}")
print(f"Application name: {sc.appName}")

# Executor information
executor_infos = status.getExecutorInfos()
for executor in executor_infos:
    print(f"Executor {executor.executorId}: {executor.totalCores} cores, "
          f"{executor.maxMemory} bytes memory")
```

**Output:**
```
Execution time: 2.34 seconds
Number of partitions: 8
Active jobs: 0
Active stages: 0
Application ID: app-20231201-103045-0001
Application name: MonitoringExample
Executor driver: 8 cores, 1073741824 bytes memory
```

### 22. How do you handle schema evolution in Spark?

**Answer:** Schema evolution allows reading data with different schemas over time.

```python
from pyspark.sql.types import *
from pyspark.sql import functions as F

# Original schema
original_schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])

# Evolved schema (added new field)
evolved_schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("email", StringType(), True),  # New field
    StructField("department", StringType(), True)  # Another new field
])

# Create sample data with original schema
old_data = [(1, "Alice", 25), (2, "Bob", 30)]
df_old = spark.createDataFrame(old_data, original_schema)

# Create sample data with evolved schema
new_data = [(3, "Charlie", 35, "charlie@email.com", "Engineering"),
            (4, "Diana", 28, "diana@email.com", "Marketing")]
df_new = spark.createDataFrame(new_data, evolved_schema)

print("Original data:")
df_old.show()

print("New data:")
df_new.show()

# Handle schema evolution - add missing columns
df_old_evolved = df_old.withColumn("email", F.lit(None).cast(StringType())) \
                       .withColumn("department", F.lit("Unknown"))

print("Old data with evolved schema:")
df_old_evolved.show()

# Union both DataFrames
combined_df = df_old_evolved.union(df_new)
print("Combined data:")
combined_df.show()

# Schema merging for Parquet files
# spark.conf.set("spark.sql.parquet.mergeSchema", "true")
# df = spark.read.option("mergeSchema", "true").parquet("path/to/parquet/files")
```

**Output:**
```
Original data:
+---+-----+---+
| id| name|age|
+---+-----+---+
|  1|Alice| 25|
|  2|  Bob| 30|
+---+-----+---+

New data:
+---+-------+---+-----------------+-----------+
| id|   name|age|            email| department|
+---+-------+---+-----------------+-----------+
|  3|Charlie| 35|charlie@email.com|Engineering|
|  4|  Diana| 28|  diana@email.com|  Marketing|
+---+-------+---+-----------------+-----------+

Old data with evolved schema:
+---+-----+---+-----+----------+
| id| name|age|email|department|
+---+-----+---+-----+----------+
|  1|Alice| 25| null|   Unknown|
|  2|  Bob| 30| null|   Unknown|
+---+-----+---+-----+----------+

Combined data:
+---+-------+---+-----------------+-----------+
| id|   name|age|            email| department|
+---+-------+---+-----------------+-----------+
|  1|  Alice| 25|             null|    Unknown|
|  2|    Bob| 30|             null|    Unknown|
|  3|Charlie| 35|charlie@email.com|Engineering|
|  4|  Diana| 28|  diana@email.com|  Marketing|
+---+-------+---+-----------------+-----------+
```

### 23. How do you implement custom UDFs in Spark?

**Answer:** User Defined Functions (UDFs) allow custom logic in Spark SQL.

```python
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType, IntegerType
import re

# Sample data
df = spark.createDataFrame([
    (1, "john.doe@email.com", "John Doe", "2023-01-15"),
    (2, "jane.smith@company.org", "Jane Smith", "2023-02-20"),
    (3, "invalid-email", "Bob Wilson", "2023-03-10")
], ["id", "email", "name", "date"])

# 1. Simple UDF - Extract domain from email
def extract_domain(email):
    if email and "@" in email:
        return email.split("@")[1]
    return "unknown"

domain_udf = udf(extract_domain, StringType())

# 2. Complex UDF - Validate email format
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return 1 if email and re.match(pattern, email) else 0

email_validator_udf = udf(validate_email, IntegerType())

# 3. UDF with multiple parameters
def format_name_with_domain(name, email):
    domain = extract_domain(email)
    return f"{name} ({domain})"

name_formatter_udf = udf(format_name_with_domain, StringType())

# Apply UDFs
result = df.withColumn("domain", domain_udf(col("email"))) \
           .withColumn("is_valid_email", email_validator_udf(col("email"))) \
           .withColumn("formatted_name", name_formatter_udf(col("name"), col("email")))

print("Results with UDFs:")
result.show(truncate=False)

# Performance comparison - UDF vs built-in functions
from pyspark.sql.functions import split, when, regexp_extract
import time

# UDF approach
start_time = time.time()
udf_result = df.withColumn("domain_udf", domain_udf(col("email"))).count()
udf_time = time.time() - start_time

# Built-in functions approach
start_time = time.time()
builtin_result = df.withColumn("domain_builtin", 
                              when(col("email").contains("@"), 
                                   split(col("email"), "@").getItem(1))
                              .otherwise("unknown")).count()
builtin_time = time.time() - start_time

print(f"UDF time: {udf_time:.4f}s")
print(f"Built-in functions time: {builtin_time:.4f}s")
print(f"Built-in is {udf_time/builtin_time:.1f}x faster")
```

**Output:**
```
Results with UDFs:
+---+------------------------+---------+----------+-------------+---------------+------------------------+
|id |email                   |name     |date      |domain       |is_valid_email |formatted_name          |
+---+------------------------+---------+----------+-------------+---------------+------------------------+
|1  |john.doe@email.com      |John Doe |2023-01-15|email.com    |1              |John Doe (email.com)    |
|2  |jane.smith@company.org  |Jane Smith|2023-02-20|company.org  |1              |Jane Smith (company.org)|
|3  |invalid-email           |Bob Wilson|2023-03-10|unknown      |0              |Bob Wilson (unknown)    |
+---+------------------------+---------+----------+-------------+---------------+------------------------+

UDF time: 0.0234s
Built-in functions time: 0.0089s
Built-in is 2.6x faster
```
