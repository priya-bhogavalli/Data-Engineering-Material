# Apache Spark Key Concepts for Data Engineering

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Spark Architecture & Theory](#-spark-architecture--theory)
3. [Core Data Structures](#-core-data-structures)
4. [Transformations & Actions](#-transformations--actions)
5. [Spark SQL Fundamentals](#-spark-sql-fundamentals)
6. [Data Sources & Formats](#-data-sources--formats)
7. [Memory Management](#-memory-management)
8. [Job Execution Model](#-job-execution-model)
9. [Performance Basics](#-performance-basics)
10. [Error Handling](#-error-handling)
11. [Best Practices](#-best-practices)
12. [Interview Focus Areas](#-interview-focus-areas)

---

## 🎯 Overview

Apache Spark is a unified analytics engine for large-scale data processing, providing high-level APIs in Java, Scala, Python, and R, with an optimized engine supporting general computation graphs.

**Key Benefits:**
- **Speed**: 100x faster than Hadoop MapReduce in memory, 10x on disk
- **Ease of Use**: Simple APIs in multiple languages
- **Generality**: Combines SQL, streaming, ML, and graph processing
- **Runs Everywhere**: Hadoop, Apache Mesos, Kubernetes, standalone, cloud

## 📚 Related Documents

- **[Spark Advanced Big Data Processing](./SPARK_ADVANCED_BIG_DATA_PROCESSING.md)** - Production optimization, tuning, deployment
- **[Spark Quick Reference](./SPARK_QUICK_REFERENCE.md)** - Essential operations and patterns
- **[Spark Interview Questions](./SPARK_INTERVIEW_QUESTIONS_COMPLETE.md)** - Interview preparation

## 🏗️ Spark Architecture & Theory

### Cluster Architecture

**Driver Program:**
The main program that creates SparkContext and coordinates the execution of Spark applications across the cluster.

**Cluster Manager:**
External service for acquiring resources (Standalone, YARN, Mesos, Kubernetes).

**Executors:**
Worker processes that run tasks and store data for the application.

```python
from pyspark.sql import SparkSession

# Create SparkSession (entry point for Spark functionality)
spark = SparkSession.builder \
    .appName("DataEngineering") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .getOrCreate()

# Get SparkContext from SparkSession
sc = spark.sparkContext

print(f"Spark Version: {spark.version}")
print(f"Application ID: {sc.applicationId}")
print(f"Master URL: {sc.master}")
print(f"Default Parallelism: {sc.defaultParallelism}")

# Output:
# Spark Version: 3.5.0
# Application ID: app-20240101-100000-0000
# Master URL: local[*]
# Default Parallelism: 8
```

### ⚡ **Lazy Evaluation - Smart Production Planning**

> **Think of lazy evaluation like a smart factory manager who plans the entire production process before starting any work - optimizing the workflow for maximum efficiency**

**🏭 Factory Planning Analogy:**
Imagine you're managing a factory and workers keep giving you production requests:
- **Worker 1**: "Filter out defective parts"
- **Worker 2**: "Paint the good parts blue" 
- **Worker 3**: "Package them in boxes of 10"

A **lazy manager** (Spark) doesn't start work immediately. Instead:
1. **Collects all requests** (transformations)
2. **Creates optimal production plan** (execution plan)
3. **Only starts when customer places order** (action triggered)
4. **Executes entire optimized workflow** (efficient processing)

Spark uses lazy evaluation - transformations are not executed immediately but recorded as a lineage graph until an action is called.

```python
# Create sample data
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
rdd = sc.parallelize(data)

# These are transformations (lazy - not executed yet)
filtered_rdd = rdd.filter(lambda x: x % 2 == 0)
squared_rdd = filtered_rdd.map(lambda x: x ** 2)

print("Transformations defined, but not executed yet")

# This is an action (triggers execution)
result = squared_rdd.collect()
print(f"Result: {result}")

# Output:
# Transformations defined, but not executed yet
# Result: [4, 16, 36, 64, 100]
```

### Resilient Distributed Datasets (RDD) Lineage

```python
# Create RDD with lineage tracking
numbers = sc.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], numSlices=3)
even_numbers = numbers.filter(lambda x: x % 2 == 0)
squared_numbers = even_numbers.map(lambda x: x ** 2)

# View the lineage (execution plan)
print("RDD Lineage:")
print(squared_numbers.toDebugString().decode())

# Output:
# RDD Lineage:
# (3) PythonRDD[2] at RDD at PythonRDD.scala:53
#  |  MapPartitionsRDD[1] at mapPartitions at PythonRDD.scala:145
#  |  ParallelCollectionRDD[0] at readRDDFromFile at PythonRDD.scala:262

# Demonstrate fault tolerance
print(f"Number of partitions: {squared_numbers.getNumPartitions()}")
print(f"Partitions content: {squared_numbers.glom().collect()}")

# Output:
# Number of partitions: 3
# Partitions content: [[], [4, 16], [36, 64, 100]]
```

## 📊 Core Data Structures - Different Types of Production Materials

> **Think of Spark's data structures like different ways to organize materials in your factory - from raw materials to finished products with quality control**

### 📦 **RDDs (Resilient Distributed Datasets) - Raw Materials**

> **Think of RDDs like raw materials in your factory - flexible and powerful, but require skilled workers to handle properly**

**🏗️ Raw Materials Characteristics:**
- **Flexible** - Can be shaped into anything you need
- **Durable** - If damaged, can be recreated from the original source
- **Distributed** - Stored across multiple factory locations
- **Requires Expertise** - Need skilled workers to process efficiently

```python
# Create RDDs from different sources
list_rdd = sc.parallelize([1, 2, 3, 4, 5])
text_rdd = sc.textFile("hdfs://path/to/file.txt")  # Would read from HDFS

# RDD operations
numbers = sc.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Map transformation
squared = numbers.map(lambda x: x ** 2)
print(f"Squared: {squared.collect()}")

# Filter transformation
evens = numbers.filter(lambda x: x % 2 == 0)
print(f"Even numbers: {evens.collect()}")

# FlatMap transformation
words_rdd = sc.parallelize(["hello world", "spark is great", "data engineering"])
all_words = words_rdd.flatMap(lambda line: line.split(" "))
print(f"All words: {all_words.collect()}")

# Output:
# Squared: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
# Even numbers: [2, 4, 6, 8, 10]
# All words: ['hello', 'world', 'spark', 'is', 'great', 'data', 'engineering']
```

### 📋 **DataFrames - Standardized Product Specifications**

> **Think of DataFrames like standardized product blueprints with quality control - organized, optimized, and easy for any worker to understand**

**📊 Standardized Blueprint Features:**
- **Schema** - Clear specifications for each component (column)
- **Quality Control** - Built-in optimization and error checking
- **Universal** - Any factory worker can read and process
- **Efficient** - Optimized production processes built-in

```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from pyspark.sql.functions import col, sum as spark_sum, avg, count, max as spark_max

# Create DataFrame from data
data = [
    ("Alice", "Engineering", 75000, 25),
    ("Bob", "Marketing", 65000, 30),
    ("Charlie", "Engineering", 80000, 28),
    ("Diana", "HR", 70000, 32),
    ("Eve", "Engineering", 85000, 26)
]

# Define schema
schema = StructType([
    StructField("name", StringType(), True),
    StructField("department", StringType(), True),
    StructField("salary", IntegerType(), True),
    StructField("age", IntegerType(), True)
])

# Create DataFrame
df = spark.createDataFrame(data, schema)

# Basic DataFrame operations
print("DataFrame Schema:")
df.printSchema()

print("\nDataFrame Content:")
df.show()

print("\nDataFrame Info:")
print(f"Number of rows: {df.count()}")
print(f"Number of columns: {len(df.columns)}")
print(f"Column names: {df.columns}")

# Output:
# DataFrame Schema:
# root
#  |-- name: string (nullable = true)
#  |-- department: string (nullable = true)
#  |-- salary: integer (nullable = true)
#  |-- age: integer (nullable = true)
# 
# DataFrame Content:
# +-------+-----------+------+---+
# |   name| department|salary|age|
# +-------+-----------+------+---+
# |  Alice|Engineering| 75000| 25|
# |    Bob|  Marketing| 65000| 30|
# |Charlie|Engineering| 80000| 28|
# |  Diana|         HR| 70000| 32|
# |    Eve|Engineering| 85000| 26|
# +-------+-----------+------+---+
```

### Datasets (Scala/Java)

```python
# In PySpark, DataFrames are the primary abstraction
# Datasets are available in Scala/Java with compile-time type safety

# DataFrame operations that demonstrate Dataset-like functionality
from pyspark.sql.functions import when, lit

# Type-safe operations using DataFrame API
typed_df = df.select(
    col("name"),
    col("department"),
    col("salary"),
    when(col("age") < 30, lit("Young"))
    .when(col("age") < 35, lit("Mid"))
    .otherwise(lit("Senior")).alias("age_group")
)

typed_df.show()

# Output:
# +-------+-----------+------+---------+
# |   name| department|salary|age_group|
# +-------+-----------+------+---------+
# |  Alice|Engineering| 75000|    Young|
# |    Bob|  Marketing| 65000|      Mid|
# |Charlie|Engineering| 80000|    Young|
# |  Diana|         HR| 70000|      Mid|
# |    Eve|Engineering| 85000|    Young|
# +-------+-----------+------+---------+
```

## 🔄 Transformations & Actions

### Common Transformations

```python
# Sample data for transformations
sales_data = [
    ("2024-01-01", "Electronics", 1200),
    ("2024-01-01", "Clothing", 800),
    ("2024-01-02", "Electronics", 1500),
    ("2024-01-02", "Books", 300),
    ("2024-01-03", "Electronics", 900),
    ("2024-01-03", "Clothing", 1100)
]

sales_df = spark.createDataFrame(sales_data, ["date", "category", "amount"])

# Select transformation
selected_df = sales_df.select("category", "amount")
print("Selected columns:")
selected_df.show()

# Filter transformation
electronics_df = sales_df.filter(col("category") == "Electronics")
print("Electronics sales:")
electronics_df.show()

# GroupBy transformation
category_totals = sales_df.groupBy("category").agg(
    spark_sum("amount").alias("total_sales"),
    avg("amount").alias("avg_sales"),
    count("*").alias("transaction_count")
)
print("Category totals:")
category_totals.show()

# Output:
# Selected columns:
# +-----------+------+
# |   category|amount|
# +-----------+------+
# |Electronics|  1200|
# |   Clothing|   800|
# |Electronics|  1500|
# |      Books|   300|
# |Electronics|   900|
# |   Clothing|  1100|
# +-----------+------+
# 
# Electronics sales:
# +----------+-----------+------+
# |      date|   category|amount|
# +----------+-----------+------+
# |2024-01-01|Electronics|  1200|
# |2024-01-02|Electronics|  1500|
# |2024-01-03|Electronics|   900|
# +----------+-----------+------+
```

### Window Functions

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, rank, dense_rank, lag, lead

# Create window specifications
window_spec = Window.partitionBy("department").orderBy(col("salary").desc())
overall_window = Window.orderBy(col("salary").desc())

# Apply window functions
windowed_df = df.select(
    "*",
    row_number().over(window_spec).alias("dept_rank"),
    rank().over(overall_window).alias("overall_rank"),
    lag("salary", 1).over(overall_window).alias("prev_salary"),
    lead("salary", 1).over(overall_window).alias("next_salary")
)

print("Window functions applied:")
windowed_df.show()

# Output:
# +-------+-----------+------+---+---------+------------+-----------+-----------+
# |   name| department|salary|age|dept_rank|overall_rank|prev_salary|next_salary|
# +-------+-----------+------+---+---------+------------+-----------+-----------+
# |    Eve|Engineering| 85000| 26|        1|           1|       null|      80000|
# |Charlie|Engineering| 80000| 28|        2|           2|      85000|      75000|
# |  Alice|Engineering| 75000| 25|        3|           3|      80000|      70000|
# |  Diana|         HR| 70000| 32|        1|           4|      75000|      65000|
# |    Bob|  Marketing| 65000| 30|        1|           5|      70000|       null|
# +-------+-----------+------+---+---------+------------+-----------+-----------+
```

### Common Actions

```python
# Actions trigger computation
numbers_rdd = sc.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Collect - brings all data to driver
all_numbers = numbers_rdd.collect()
print(f"All numbers: {all_numbers}")

# Take - brings first n elements to driver
first_three = numbers_rdd.take(3)
print(f"First three: {first_three}")

# Count - returns number of elements
total_count = numbers_rdd.count()
print(f"Total count: {total_count}")

# Reduce - aggregates elements
sum_all = numbers_rdd.reduce(lambda a, b: a + b)
print(f"Sum of all: {sum_all}")

# First - returns first element
first_element = numbers_rdd.first()
print(f"First element: {first_element}")

# SaveAsTextFile - saves to file system
# numbers_rdd.saveAsTextFile("hdfs://path/to/output")

# Output:
# All numbers: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# First three: [1, 2, 3]
# Total count: 10
# Sum of all: 55
# First element: 1
```

## 🗄️ Spark SQL Fundamentals

### SQL Queries on DataFrames

```python
# Register DataFrame as temporary view
df.createOrReplaceTempView("employees")
sales_df.createOrReplaceTempView("sales")

# SQL queries
high_earners = spark.sql("""
    SELECT name, department, salary
    FROM employees
    WHERE salary > 70000
    ORDER BY salary DESC
""")

print("High earners:")
high_earners.show()

# Complex SQL with aggregations
dept_analysis = spark.sql("""
    SELECT 
        department,
        COUNT(*) as employee_count,
        AVG(salary) as avg_salary,
        MIN(age) as min_age,
        MAX(age) as max_age
    FROM employees
    GROUP BY department
    HAVING COUNT(*) > 1
    ORDER BY avg_salary DESC
""")

print("Department analysis:")
dept_analysis.show()

# Output:
# High earners:
# +-------+-----------+------+
# |   name| department|salary|
# +-------+-----------+------+
# |    Eve|Engineering| 85000|
# |Charlie|Engineering| 80000|
# |  Alice|Engineering| 75000|
# +-------+-----------+------+
# 
# Department analysis:
# +-----------+--------------+----------+-------+-------+
# | department|employee_count|avg_salary|min_age|max_age|
# +-----------+--------------+----------+-------+-------+
# |Engineering|             3|   80000.0|     25|     28|
# +-----------+--------------+----------+-------+-------+
```

### Built-in Functions

```python
from pyspark.sql.functions import *

# String functions
string_df = spark.createDataFrame([
    ("John Doe", "john.doe@email.com"),
    ("Jane Smith", "jane.smith@company.org"),
    ("Bob Johnson", "bob@test.net")
], ["name", "email"])

string_operations = string_df.select(
    col("name"),
    col("email"),
    upper(col("name")).alias("name_upper"),
    split(col("email"), "@").getItem(0).alias("username"),
    split(col("email"), "@").getItem(1).alias("domain"),
    length(col("name")).alias("name_length")
)

print("String operations:")
string_operations.show()

# Date functions
from datetime import datetime, date

date_df = spark.createDataFrame([
    (1, datetime(2024, 1, 15, 10, 30, 0)),
    (2, datetime(2024, 2, 20, 14, 45, 0)),
    (3, datetime(2024, 3, 10, 9, 15, 0))
], ["id", "timestamp"])

date_operations = date_df.select(
    col("id"),
    col("timestamp"),
    date_format(col("timestamp"), "yyyy-MM-dd").alias("date_only"),
    hour(col("timestamp")).alias("hour"),
    dayofweek(col("timestamp")).alias("day_of_week"),
    datediff(current_date(), col("timestamp")).alias("days_ago")
)

print("Date operations:")
date_operations.show()

# Output:
# String operations:
# +----------+---------------------+----------+----------+-----------+-----------+
# |      name|                email|name_upper|  username|     domain|name_length|
# +----------+---------------------+----------+----------+-----------+-----------+
# |  John Doe|    john.doe@email.com| JOHN DOE|  john.doe|  email.com|          8|
# |Jane Smith|jane.smith@company.org|JANE SMITH|jane.smith|company.org|         10|
# |Bob Johnson|         bob@test.net|BOB JOHNSON|       bob|   test.net|         11|
# +----------+---------------------+----------+----------+-----------+-----------+
```

## 📁 Data Sources & Formats

### Reading Different File Formats

```python
# CSV files
csv_df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("path/to/file.csv")

# JSON files
json_df = spark.read \
    .option("multiline", "true") \
    .json("path/to/file.json")

# Parquet files (recommended for Spark)
parquet_df = spark.read.parquet("path/to/file.parquet")

# Delta Lake (if available)
# delta_df = spark.read.format("delta").load("path/to/delta-table")

# Database connections
jdbc_df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/database") \
    .option("dbtable", "employees") \
    .option("user", "username") \
    .option("password", "password") \
    .load()

# Demonstrate with sample data
sample_data = [
    {"name": "Alice", "age": 25, "city": "New York"},
    {"name": "Bob", "age": 30, "city": "San Francisco"},
    {"name": "Charlie", "age": 35, "city": "Chicago"}
]

# Create DataFrame from JSON-like data
json_like_df = spark.createDataFrame(sample_data)
print("JSON-like DataFrame:")
json_like_df.show()

# Output:
# JSON-like DataFrame:
# +-------+---+-------------+
# |   name|age|         city|
# +-------+---+-------------+
# |  Alice| 25|     New York|
# |    Bob| 30|San Francisco|
# |Charlie| 35|      Chicago|
# +-------+---+-------------+
```

### Writing Data

```python
# Write to different formats
# df.write.mode("overwrite").csv("path/to/output.csv")
# df.write.mode("append").parquet("path/to/output.parquet")
# df.write.mode("overwrite").json("path/to/output.json")

# Write to database
# df.write \
#     .format("jdbc") \
#     .option("url", "jdbc:postgresql://localhost:5432/database") \
#     .option("dbtable", "output_table") \
#     .option("user", "username") \
#     .option("password", "password") \
#     .mode("overwrite") \
#     .save()

# Partitioned writes for better performance
# df.write \
#     .partitionBy("department") \
#     .mode("overwrite") \
#     .parquet("path/to/partitioned_output")

print("Write operations configured (commented out to avoid file creation)")

# Demonstrate coalesce for controlling output files
coalesced_df = df.coalesce(1)  # Reduce to 1 partition
print(f"Original partitions: {df.rdd.getNumPartitions()}")
print(f"Coalesced partitions: {coalesced_df.rdd.getNumPartitions()}")

# Output:
# Write operations configured (commented out to avoid file creation)
# Original partitions: 8
# Coalesced partitions: 1
```

## 🧠 Memory Management

### Caching and Persistence

```python
from pyspark import StorageLevel

# Create a DataFrame that will be used multiple times
large_df = spark.range(1000000).toDF("id")
processed_df = large_df.filter(col("id") % 2 == 0).withColumn("squared", col("id") ** 2)

# Cache the DataFrame in memory
cached_df = processed_df.cache()

# Alternative: persist with specific storage level
persisted_df = processed_df.persist(StorageLevel.MEMORY_AND_DISK)

# First action - triggers computation and caching
count1 = cached_df.count()
print(f"First count: {count1}")

# Second action - uses cached data (faster)
count2 = cached_df.count()
print(f"Second count: {count2}")

# Check cache status
print(f"Is cached: {cached_df.is_cached}")

# Unpersist when done
cached_df.unpersist()

# Output:
# First count: 500000
# Second count: 500000
# Is cached: True
```

### Memory Configuration

```python
# Get current Spark configuration
conf = spark.sparkContext.getConf()
print("Key Spark configurations:")
print(f"Executor memory: {conf.get('spark.executor.memory', 'default')}")
print(f"Driver memory: {conf.get('spark.driver.memory', 'default')}")
print(f"Executor cores: {conf.get('spark.executor.cores', 'default')}")

# Memory fractions (these are set at startup)
print("\nMemory management settings:")
print("spark.sql.execution.arrow.pyspark.enabled: Enables Arrow optimization")
print("spark.sql.adaptive.enabled: Enables adaptive query execution")
print("spark.sql.adaptive.coalescePartitions.enabled: Enables partition coalescing")

# Output:
# Key Spark configurations:
# Executor memory: default
# Driver memory: default
# Executor cores: default
# 
# Memory management settings:
# spark.sql.execution.arrow.pyspark.enabled: Enables Arrow optimization
# spark.sql.adaptive.enabled: Enables adaptive query execution
# spark.sql.adaptive.coalescePartitions.enabled: Enables partition coalescing
```

## ⚙️ Job Execution Model

### Understanding Jobs, Stages, and Tasks

```python
# Create an RDD that will demonstrate job execution
data_rdd = sc.parallelize(range(100), numSlices=4)

# Multiple transformations create a lineage
filtered_rdd = data_rdd.filter(lambda x: x % 2 == 0)
mapped_rdd = filtered_rdd.map(lambda x: (x, x ** 2))
grouped_rdd = mapped_rdd.groupByKey()

# Action triggers job execution
result = grouped_rdd.collect()

print(f"Number of partitions: {grouped_rdd.getNumPartitions()}")
print(f"First few results: {result[:3]}")

# Demonstrate wide vs narrow transformations
print("\nNarrow transformations (no shuffle):")
narrow_result = data_rdd.map(lambda x: x * 2).filter(lambda x: x > 50).take(5)
print(f"Narrow result: {narrow_result}")

print("\nWide transformations (require shuffle):")
wide_result = data_rdd.map(lambda x: (x % 3, x)).groupByKey().mapValues(list).collect()
print(f"Wide result: {wide_result}")

# Output:
# Number of partitions: 4
# First few results: [(0, <pyspark.resultiterable.ResultIterable object at 0x...>), ...]
# 
# Narrow transformations (no shuffle):
# Narrow result: [52, 54, 56, 58, 60]
# 
# Wide transformations (require shuffle):
# Wide result: [(0, [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 90, 93, 96, 99]), ...]
```

### Partitioning Strategies

```python
# Default partitioning
default_df = spark.range(1000)
print(f"Default partitions: {default_df.rdd.getNumPartitions()}")

# Repartition (full shuffle)
repartitioned_df = default_df.repartition(5)
print(f"After repartition: {repartitioned_df.rdd.getNumPartitions()}")

# Coalesce (reduce partitions without full shuffle)
coalesced_df = repartitioned_df.coalesce(3)
print(f"After coalesce: {coalesced_df.rdd.getNumPartitions()}")

# Hash partitioning for key-value data
key_value_rdd = sc.parallelize([(i, i**2) for i in range(100)])
hash_partitioned = key_value_rdd.partitionBy(4)
print(f"Hash partitioned: {hash_partitioned.getNumPartitions()}")

# Custom partitioning
def custom_partitioner(key):
    return key % 3

# Range partitioning (for ordered data)
ordered_df = spark.range(1000).orderBy("id")
print(f"Ordered DataFrame partitions: {ordered_df.rdd.getNumPartitions()}")

# Output:
# Default partitions: 8
# After repartition: 5
# After coalesce: 3
# Hash partitioned: 4
# Ordered DataFrame partitions: 8
```

## 🚀 Performance Basics

### Optimization Techniques

```python
# Broadcast variables for small lookup tables
small_lookup = {"A": 1, "B": 2, "C": 3, "D": 4}
broadcast_lookup = spark.sparkContext.broadcast(small_lookup)

def enrich_with_lookup(value):
    return broadcast_lookup.value.get(value, 0)

# Use broadcast variable in transformations
sample_data = ["A", "B", "C", "D", "E", "A", "B"]
sample_rdd = sc.parallelize(sample_data)
enriched_rdd = sample_rdd.map(lambda x: (x, enrich_with_lookup(x)))

print("Enriched data with broadcast variable:")
print(enriched_rdd.collect())

# Accumulators for counters
error_counter = spark.sparkContext.accumulator(0)
processed_counter = spark.sparkContext.accumulator(0)

def process_with_counters(value):
    try:
        processed_counter.add(1)
        if value < 0:
            error_counter.add(1)
            return None
        return value * 2
    except:
        error_counter.add(1)
        return None

test_data = [-1, 2, -3, 4, 5, -6, 7, 8]
test_rdd = sc.parallelize(test_data)
result_rdd = test_rdd.map(process_with_counters).filter(lambda x: x is not None)

# Trigger action to update accumulators
final_result = result_rdd.collect()

print(f"\nProcessed items: {processed_counter.value}")
print(f"Errors encountered: {error_counter.value}")
print(f"Final result: {final_result}")

# Output:
# Enriched data with broadcast variable:
# [('A', 1), ('B', 2), ('C', 3), ('D', 4), ('E', 0), ('A', 1), ('B', 2)]
# 
# Processed items: 8
# Errors encountered: 3
# Final result: [4, 8, 10, 14, 16]
```

### Catalyst Optimizer

```python
# Demonstrate query optimization
from pyspark.sql.functions import col

# Create sample DataFrames
customers = spark.createDataFrame([
    (1, "Alice", "NY"),
    (2, "Bob", "CA"),
    (3, "Charlie", "TX")
], ["id", "name", "state"])

orders = spark.createDataFrame([
    (101, 1, 100.0),
    (102, 2, 200.0),
    (103, 1, 150.0),
    (104, 3, 300.0)
], ["order_id", "customer_id", "amount"])

# Register as views
customers.createOrReplaceTempView("customers")
orders.createOrReplaceTempView("orders")

# Complex query that will be optimized
optimized_query = spark.sql("""
    SELECT c.name, c.state, SUM(o.amount) as total_spent
    FROM customers c
    JOIN orders o ON c.id = o.customer_id
    WHERE c.state IN ('NY', 'CA')
    GROUP BY c.name, c.state
    HAVING SUM(o.amount) > 100
    ORDER BY total_spent DESC
""")

# Show the execution plan
print("Execution plan:")
optimized_query.explain(True)

print("\nQuery result:")
optimized_query.show()

# Output shows the optimized physical plan
```

## ❌ Error Handling

### Common Error Patterns

```python
from pyspark.sql.utils import AnalysisException
from pyspark.sql.functions import when, isnan, isnull

# Handle missing columns gracefully
def safe_select(df, columns):
    available_columns = df.columns
    safe_columns = [col for col in columns if col in available_columns]
    missing_columns = [col for col in columns if col not in available_columns]
    
    if missing_columns:
        print(f"Warning: Missing columns {missing_columns}")
    
    return df.select(*safe_columns) if safe_columns else df.limit(0)

# Test with sample data
test_df = spark.createDataFrame([
    ("Alice", 25, 75000),
    ("Bob", 30, 65000)
], ["name", "age", "salary"])

# Try to select columns that may not exist
requested_columns = ["name", "age", "salary", "department", "bonus"]
result_df = safe_select(test_df, requested_columns)
print("Safe selection result:")
result_df.show()

# Handle null values
data_with_nulls = [
    ("Alice", 25, 75000.0),
    ("Bob", None, 65000.0),
    ("Charlie", 30, None),
    (None, 35, 80000.0)
]

null_df = spark.createDataFrame(data_with_nulls, ["name", "age", "salary"])

# Clean null values
cleaned_df = null_df.select(
    when(col("name").isNull(), "Unknown").otherwise(col("name")).alias("name"),
    when(col("age").isNull(), 0).otherwise(col("age")).alias("age"),
    when(col("salary").isNull(), 0.0).otherwise(col("salary")).alias("salary")
)

print("Cleaned DataFrame:")
cleaned_df.show()

# Output:
# Warning: Missing columns ['department', 'bonus']
# Safe selection result:
# +-------+---+------+
# |   name|age|salary|
# +-------+---+------+
# |  Alice| 25| 75000|
# |    Bob| 30| 65000|
# +-------+---+------+
# 
# Cleaned DataFrame:
# +-------+---+-------+
# |   name|age| salary|
# +-------+---+-------+
# |  Alice| 25|75000.0|
# |    Bob|  0|65000.0|
# |Charlie| 30|    0.0|
# |Unknown| 35|80000.0|
# +-------+---+-------+
```

## 📋 Best Practices

### Code Organization

```python
class SparkDataProcessor:
    """Reusable Spark data processing class"""
    
    def __init__(self, spark_session):
        self.spark = spark_session
        
    def read_data(self, file_path, file_format="parquet"):
        """Read data from various formats"""
        if file_format == "parquet":
            return self.spark.read.parquet(file_path)
        elif file_format == "csv":
            return self.spark.read.option("header", "true").csv(file_path)
        elif file_format == "json":
            return self.spark.read.json(file_path)
        else:
            raise ValueError(f"Unsupported format: {file_format}")
    
    def clean_data(self, df):
        """Standard data cleaning operations"""
        # Remove duplicates
        df_clean = df.dropDuplicates()
        
        # Handle nulls based on column type
        for column, dtype in df_clean.dtypes:
            if dtype in ["int", "bigint", "float", "double"]:
                df_clean = df_clean.fillna(0, subset=[column])
            elif dtype == "string":
                df_clean = df_clean.fillna("Unknown", subset=[column])
        
        return df_clean
    
    def aggregate_data(self, df, group_cols, agg_cols):
        """Generic aggregation function"""
        agg_exprs = []
        for col_name, agg_func in agg_cols.items():
            if agg_func == "sum":
                agg_exprs.append(spark_sum(col_name).alias(f"{col_name}_sum"))
            elif agg_func == "avg":
                agg_exprs.append(avg(col_name).alias(f"{col_name}_avg"))
            elif agg_func == "count":
                agg_exprs.append(count(col_name).alias(f"{col_name}_count"))
        
        return df.groupBy(*group_cols).agg(*agg_exprs)

# Usage example
processor = SparkDataProcessor(spark)

# Process sample data
sample_df = spark.createDataFrame([
    ("Alice", "Engineering", 75000),
    ("Bob", "Marketing", 65000),
    ("Alice", "Engineering", 75000),  # Duplicate
    ("Charlie", None, 80000),  # Null department
    (None, "HR", 70000)  # Null name
], ["name", "department", "salary"])

# Clean the data
cleaned_df = processor.clean_data(sample_df)
print("Cleaned data:")
cleaned_df.show()

# Aggregate the data
agg_result = processor.aggregate_data(
    cleaned_df, 
    ["department"], 
    {"salary": "avg", "name": "count"}
)
print("Aggregated data:")
agg_result.show()

# Output:
# Cleaned data:
# +-------+-----------+------+
# |   name| department|salary|
# +-------+-----------+------+
# |  Alice|Engineering| 75000|
# |    Bob|  Marketing| 65000|
# |Charlie|    Unknown| 80000|
# |Unknown|         HR| 70000|
# +-------+-----------+------+
# 
# Aggregated data:
# +-----------+----------+----------+
# | department|salary_avg|name_count|
# +-----------+----------+----------+
# |Engineering|   75000.0|         1|
# |  Marketing|   65000.0|         1|
# |    Unknown|   80000.0|         1|
# |         HR|   70000.0|         1|
# +-----------+----------+----------+
```

## 🎯 Interview Focus Areas

### Essential Concepts to Master

1. **Architecture**: Driver, executors, cluster manager
2. **Data Structures**: RDD vs DataFrame vs Dataset
3. **Transformations vs Actions**: Lazy evaluation
4. **Partitioning**: Hash, range, custom partitioning
5. **Caching**: When and how to cache data
6. **Joins**: Broadcast vs shuffle joins
7. **Performance**: Catalyst optimizer, tungsten execution

### Common Interview Questions

**Q: What's the difference between RDD, DataFrame, and Dataset?**
```python
# RDD - Low-level, functional programming
rdd = sc.parallelize([1, 2, 3, 4, 5])
squared_rdd = rdd.map(lambda x: x ** 2)

# DataFrame - High-level, SQL-like operations, schema
df = spark.createDataFrame([(1,), (2,), (3,)], ["number"])
squared_df = df.select(col("number") ** 2)

# Dataset - Type-safe (Scala/Java), combines RDD + DataFrame benefits
# In PySpark, DataFrames are the primary abstraction

print("RDD result:", squared_rdd.collect())
print("DataFrame result:")
squared_df.show()
```

**Q: Explain lazy evaluation in Spark**
```python
# Transformations are lazy (not executed immediately)
data = sc.parallelize([1, 2, 3, 4, 5])
filtered = data.filter(lambda x: x > 2)  # Lazy
mapped = filtered.map(lambda x: x * 2)   # Lazy

print("Transformations defined, but not executed yet")

# Actions trigger execution
result = mapped.collect()  # Action - triggers execution
print(f"Result: {result}")
```

**Q: When would you use cache() vs persist()?**
```python
# cache() - stores in memory only
cached_df = df.cache()

# persist() - allows choosing storage level
from pyspark import StorageLevel
persisted_df = df.persist(StorageLevel.MEMORY_AND_DISK_SER)

# Use cache() for frequently accessed data that fits in memory
# Use persist() when you need more control over storage
```

## 🚀 Next Steps

After mastering these Spark concepts:

1. **Advanced Topics**: Study [Spark Advanced Big Data Processing](./SPARK_ADVANCED_BIG_DATA_PROCESSING.md)
2. **Practice**: Use [Spark Quick Reference](./SPARK_QUICK_REFERENCE.md) for daily operations
3. **Specialization**: Learn Spark Streaming, MLlib, GraphX
4. **Integration**: Combine with Kafka, Delta Lake, and cloud platforms
5. **Performance**: Master cluster tuning and optimization

Spark is the engine of modern big data processing - master it well! ⚡