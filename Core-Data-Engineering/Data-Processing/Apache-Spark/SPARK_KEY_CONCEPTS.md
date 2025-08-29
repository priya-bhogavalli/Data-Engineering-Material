# Apache Spark Key Concepts

## 📋 Table of Contents

1. [RDD (Resilient Distributed Dataset)](#1-rdd-resilient-distributed-dataset)
   - [Key Properties](#key-properties)
   - [Creating RDDs](#creating-rdds)
   - [RDD Operations](#rdd-operations)
2. [DataFrame and Dataset](#2-dataframe-and-dataset)
   - [DataFrame Advantages](#dataframe-advantages)
   - [Creating DataFrames](#creating-dataframes)
   - [DataFrame Operations](#dataframe-operations)
3. [Transformations vs Actions](#3-transformations-vs-actions)
   - [Transformations (Lazy)](#transformations-lazy)
   - [Actions (Eager)](#actions-eager)
   - [Why Lazy Evaluation](#why-lazy-evaluation)
4. [Partitioning](#4-partitioning)
   - [Default Partitioning](#default-partitioning)
   - [Manual Partitioning](#manual-partitioning)
   - [Custom Partitioning](#custom-partitioning)
5. [Caching and Persistence](#5-caching-and-persistence)
   - [When to Cache](#when-to-cache)
   - [Storage Levels](#storage-levels)
   - [Cache Management](#cache-management)
6. [Spark SQL](#6-spark-sql)
   - [SQL Interface](#sql-interface)
   - [Built-in Functions](#built-in-functions)
7. [Joins](#7-joins)
   - [Join Types](#join-types)
   - [Join Optimization](#join-optimization)
8. [User Defined Functions (UDFs)](#8-user-defined-functions-udfs)
   - [Python UDFs](#python-udfs)
   - [Vectorized UDFs (Pandas UDFs)](#vectorized-udfs-pandas-udfs)
9. [Configuration and Tuning](#9-configuration-and-tuning)
   - [Memory Configuration](#memory-configuration)
   - [Performance Tuning](#performance-tuning)
10. [Structured Streaming](#10-structured-streaming)
    - [Basic Streaming](#basic-streaming)
    - [Windowed Aggregations](#windowed-aggregations)
11. [Error Handling and Debugging](#11-error-handling-and-debugging)
    - [Exception Handling](#exception-handling)
    - [Debugging Techniques](#debugging-techniques)
12. [Best Practices](#12-best-practices)
    - [Data Processing](#data-processing)
    - [Resource Management](#resource-management)
    - [Code Organization](#code-organization)

---

## 1. RDD (Resilient Distributed Dataset)
**What it is**: The fundamental data structure of Spark - an immutable, distributed collection of objects that can be processed in parallel across a cluster of machines.

**Real-World Analogy**: Think of RDD like a massive Excel spreadsheet that's split across multiple computers. Each computer holds a portion of the data, but they all work together to process the entire dataset.

**Key Properties**:
- **Resilient**: If one computer fails, Spark can recreate the lost data using lineage (recipe of transformations)
- **Distributed**: Data is automatically split across multiple machines for parallel processing
- **Immutable**: Once created, data cannot be modified (like a read-only file)
- **Lazy Evaluation**: Operations are planned but not executed until you actually need the results

**Real-World Example**: Processing 1TB of customer transaction logs
```python
# Instead of loading 1TB into one machine's memory (impossible),
# Spark splits it across 100 machines, each handling 10GB
transaction_logs = sc.textFile("s3://company-data/transactions/2024/")
# This doesn't actually read the data yet - just creates a plan
```

**Creating RDDs - Real Examples**:
```python
from pyspark import SparkContext

sc = SparkContext()

# Example 1: Processing customer IDs for a marketing campaign
customer_ids = [12345, 67890, 11111, 22222, 33333]
customer_rdd = sc.parallelize(customer_ids, numSlices=4)
# Splits customer IDs across 4 partitions for parallel processing

# Example 2: Analyzing web server logs
log_rdd = sc.textFile("s3://company-logs/apache-logs/2024-01-*")
# Reads all January 2024 log files from S3

# Example 3: Processing e-commerce transaction data
transaction_rdd = sc.textFile("hdfs://data/transactions.json")
# Reads transaction data from Hadoop distributed file system

# Example 4: Creating derived datasets
high_value_customers = customer_rdd.filter(lambda id: id > 50000)
# Creates new RDD with only high-value customer IDs
```

**Real Business Scenario**: 
```python
# A retail company wants to analyze 5 years of sales data (500GB)
# Traditional approach: Would crash most single machines
# Spark approach: Distributes across 50 machines, each handling 10GB

sales_data = sc.textFile("s3://retail-data/sales/year=*/month=*/")
# Automatically discovers and loads all sales files
# Data stays distributed - never loaded into single machine memory
```

**RDD Operations**:
- **Transformations**: Return new RDD (map, filter, flatMap)
- **Actions**: Return values to driver (collect, count, save)

## 2. DataFrame and Dataset
**What they are**: Think of DataFrames as "smart spreadsheets" - they have column names, data types, and Spark automatically optimizes how to process them.

**Real-World Analogy**: If RDDs are like raw text files, DataFrames are like Excel spreadsheets with headers, data validation, and built-in formulas.

**Why DataFrames are Better for Most Use Cases**:
- **Schema**: Like database tables - columns have names and types (CustomerID: Integer, Name: String)
- **Catalyst Optimizer**: Spark's "smart assistant" that rewrites your queries to run faster
- **Code Generation**: Spark writes optimized Java code at runtime for your specific query
- **Language Agnostic**: Same operations work in Python, Scala, Java, R, and SQL

**Performance Impact**: DataFrames are typically 2-5x faster than RDDs for the same operations due to optimization.

**Creating DataFrames - Real Business Examples**:
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("CustomerAnalytics").getOrCreate()

# Example 1: Loading customer data from CSV (most common scenario)
customers_df = spark.read.csv(
    "s3://company-data/customers.csv", 
    header=True,           # First row contains column names
    inferSchema=True       # Automatically detect data types
)
# Result: DataFrame with proper column names and types

# Example 2: Loading transaction logs from JSON
transactions_df = spark.read.json("s3://logs/transactions/2024-01-*")
# Automatically handles nested JSON structure

# Example 3: Loading optimized data from Parquet (fastest format)
sales_df = spark.read.parquet("s3://warehouse/sales_data/")
# Parquet includes schema and is compressed - loads 10x faster than CSV

# Example 4: Creating DataFrame with explicit schema (for data quality)
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DecimalType

# Define exact schema for financial data (prevents data type errors)
financial_schema = StructType([
    StructField("account_id", StringType(), False),      # Not nullable
    StructField("balance", DecimalType(10,2), False),    # Exact precision for money
    StructField("customer_name", StringType(), True),    # Can be null
    StructField("credit_score", IntegerType(), True)
])

accounts_df = spark.createDataFrame(raw_data_rdd, financial_schema)

# Example 5: Using SQL on DataFrames (familiar to analysts)
customers_df.createOrReplaceTempView("customers")
high_value_customers = spark.sql("""
    SELECT customer_id, name, total_spent
    FROM customers 
    WHERE total_spent > 10000 
    ORDER BY total_spent DESC
""")
```

**Real Performance Example**:
```python
# Processing 1 billion customer records
# CSV: 45 minutes to load
# Parquet: 4 minutes to load (same data, optimized format)
# This is why data engineers prefer Parquet for large datasets
```

**DataFrame Operations**:
```python
# Selecting columns
df.select("name", "age").show()
df.select(col("name"), (col("age") + 1).alias("next_age")).show()

# Filtering
df.filter(df.age > 21).show()
df.where(col("city") == "New York").show()

# Grouping and aggregation
df.groupBy("city").count().show()
df.groupBy("city").agg(avg("age"), max("age")).show()

# Joining
df1.join(df2, df1.id == df2.user_id, "inner").show()
```

## 3. Transformations vs Actions
**Critical Concept**: Spark is like a lazy chef - it plans the entire meal (transformations) but doesn't start cooking until you ask for the food (actions).

**Why This Matters**: Lazy evaluation allows Spark to optimize the entire workflow before executing anything, often making operations 10x faster.

**Real-World Analogy**: 
- **Transformations** = Writing a recipe (planning)
- **Actions** = Actually cooking the meal (execution)

**Transformations (Lazy) - Just Planning**:
```python
# Example: Analyzing employee data for HR department
employees_df = spark.read.csv("s3://hr-data/employees.csv", header=True)

# Step 1: Filter active employees (PLANNING - not executed yet)
active_employees = employees_df.filter(employees_df.status == "Active")

# Step 2: Select relevant columns (PLANNING - not executed yet)
employee_summary = active_employees.select("name", "department", "salary")

# Step 3: Calculate average salary by department (PLANNING - not executed yet)
dept_averages = employee_summary.groupBy("department").agg({"salary": "avg"})

# At this point: NO DATA HAS BEEN PROCESSED YET!
# Spark has just created an execution plan
```

**Real Business Impact**:
```python
# Without lazy evaluation: Each step would scan the entire dataset
# With lazy evaluation: Spark combines all steps into one optimized scan
# Result: 5x faster execution on large datasets
```

**Actions (Eager) - Actually Execute the Plan**:
```python
# NOW we trigger execution with actions

# Action 1: Show results (triggers entire computation)
dept_averages.show()
# Output:
# +----------+----------+
# |department|avg_salary|
# +----------+----------+
# |Engineering|  95000.0|
# |Marketing  |  75000.0|
# |Sales      |  65000.0|
# +----------+----------+

# Action 2: Count records (triggers execution again)
num_departments = dept_averages.count()
print(f"Number of departments: {num_departments}")

# Action 3: Save results (triggers execution again)
dept_averages.write.mode("overwrite").csv("s3://reports/dept-salaries/")

# ⚠️ IMPORTANT: Each action re-executes the entire plan!
# Solution: Cache intermediate results (see caching section)
```

**Common Actions in Real Projects**:
```python
# Data Quality Check
print(f"Total customers: {customers_df.count()}")
print(f"Customers with email: {customers_df.filter(col('email').isNotNull()).count()}")

# Export for Business Intelligence
customer_metrics.write.mode("overwrite").parquet("s3://bi-data/customer-metrics/")

# Real-time Dashboard
top_products.show(20)  # Show top 20 products

# Machine Learning Pipeline
features_array = ml_features.collect()  # ⚠️ Use carefully - brings all data to driver
```

**Performance Tip**:
```python
# ❌ BAD: Multiple actions without caching
result1 = expensive_computation.count()     # Executes full pipeline
result2 = expensive_computation.show()      # Executes full pipeline again

# ✅ GOOD: Cache then use multiple actions
expensive_computation.cache()               # Cache the result
result1 = expensive_computation.count()     # Executes and caches
result2 = expensive_computation.show()      # Uses cached data
```

**Why Lazy Evaluation**:
- **Optimization**: Catalyst can optimize entire query plan
- **Efficiency**: Avoid unnecessary computations
- **Fault Tolerance**: Can replay transformations if partition lost

## 4. Partitioning
**What it is**: How data is distributed across cluster nodes for parallel processing.

**Default Partitioning**:
```python
# Check number of partitions
print(f"Partitions: {rdd.getNumPartitions()}")
print(f"Partitions: {df.rdd.getNumPartitions()}")

# Default partitioning rules
# - Files: One partition per file block (typically 128MB)
# - Collections: Based on spark.default.parallelism
```

**Manual Partitioning**:
```python
# Repartition (can increase or decrease)
repartitioned_rdd = rdd.repartition(10)
repartitioned_df = df.repartition(8)

# Coalesce (only decrease partitions)
coalesced_rdd = rdd.coalesce(4)
coalesced_df = df.coalesce(2)

# Partition by column (DataFrame)
partitioned_df = df.repartition("department")
```

**Custom Partitioning**:
```python
# Hash partitioning for key-value RDDs
key_value_rdd = rdd.map(lambda x: (x % 10, x))
partitioned_rdd = key_value_rdd.partitionBy(4)

# Range partitioning
from pyspark import RangePartitioner
partitioner = RangePartitioner(4, key_value_rdd)
range_partitioned = key_value_rdd.partitionBy(4, partitioner)
```

## 5. Caching and Persistence
**What it is**: Storing intermediate results in memory or disk for reuse across multiple actions.

**When to Cache**:
- RDD/DataFrame used multiple times
- Expensive computations (joins, aggregations)
- Iterative algorithms (machine learning)

**Storage Levels**:
```python
from pyspark import StorageLevel

# Memory only (default for cache())
df.cache()  # Same as df.persist(StorageLevel.MEMORY_ONLY)

# Memory and disk
df.persist(StorageLevel.MEMORY_AND_DISK)

# Disk only
df.persist(StorageLevel.DISK_ONLY)

# Serialized in memory (more compact)
df.persist(StorageLevel.MEMORY_ONLY_SER)

# With replication
df.persist(StorageLevel.MEMORY_AND_DISK_2)
```

**Cache Management**:
```python
# Check if cached
df.is_cached

# Remove from cache
df.unpersist()

# Cache with custom storage level
df.persist(StorageLevel.MEMORY_AND_DISK_SER)
```

## 6. Spark SQL
**What it is**: Module for working with structured data using SQL queries and DataFrame API.

**SQL Interface**:
```python
# Register DataFrame as temporary view
df.createOrReplaceTempView("employees")

# Execute SQL queries
result = spark.sql("""
    SELECT department, AVG(salary) as avg_salary
    FROM employees
    WHERE age > 25
    GROUP BY department
    ORDER BY avg_salary DESC
""")

result.show()
```

**Built-in Functions**:
```python
from pyspark.sql.functions import *

# String functions
df.select(
    upper(col("name")).alias("upper_name"),
    length(col("name")).alias("name_length")
).show()

# Date functions
df.select(
    current_date().alias("today"),
    date_add(col("hire_date"), 30).alias("probation_end")
).show()

# Aggregation functions
df.groupBy("department").agg(
    avg("salary").alias("avg_salary"),
    max("salary").alias("max_salary"),
    count("*").alias("employee_count")
).show()

# Window functions
from pyspark.sql.window import Window

window_spec = Window.partitionBy("department").orderBy(desc("salary"))
df.select(
    "*",
    row_number().over(window_spec).alias("salary_rank"),
    dense_rank().over(window_spec).alias("salary_dense_rank")
).show()
```

## 7. Joins
**What they are**: Operations to combine data from multiple DataFrames based on common keys.

**Join Types**:
```python
# Inner join (default)
result = df1.join(df2, df1.id == df2.user_id)
result = df1.join(df2, df1.id == df2.user_id, "inner")

# Left outer join
result = df1.join(df2, df1.id == df2.user_id, "left")

# Right outer join
result = df1.join(df2, df1.id == df2.user_id, "right")

# Full outer join
result = df1.join(df2, df1.id == df2.user_id, "outer")

# Left semi join (like EXISTS)
result = df1.join(df2, df1.id == df2.user_id, "left_semi")

# Left anti join (like NOT EXISTS)
result = df1.join(df2, df1.id == df2.user_id, "left_anti")
```

**Join Optimization**:
```python
# Broadcast join for small tables
from pyspark.sql.functions import broadcast

large_df.join(broadcast(small_df), "key")

# Bucket joins for large tables
df1.write.bucketBy(4, "key").saveAsTable("bucketed_table1")
df2.write.bucketBy(4, "key").saveAsTable("bucketed_table2")
```

## 8. User Defined Functions (UDFs)
**What they are**: Custom functions to extend Spark's built-in functionality.

**Python UDFs**:
```python
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType, IntegerType

# Simple UDF
def categorize_age(age):
    if age < 18:
        return "Minor"
    elif age < 65:
        return "Adult"
    else:
        return "Senior"

categorize_udf = udf(categorize_age, StringType())

# Use UDF
df.select("name", "age", categorize_udf("age").alias("category")).show()

# Register UDF for SQL
spark.udf.register("categorize_age", categorize_age, StringType())
spark.sql("SELECT name, age, categorize_age(age) as category FROM people").show()
```

**Vectorized UDFs (Pandas UDFs)**:
```python
from pyspark.sql.functions import pandas_udf
import pandas as pd

# Pandas UDF (much faster than regular UDF)
@pandas_udf(returnType=StringType())
def vectorized_categorize(ages: pd.Series) -> pd.Series:
    return ages.apply(lambda age: 
        "Minor" if age < 18 else 
        "Adult" if age < 65 else 
        "Senior"
    )

df.select("name", "age", vectorized_categorize("age").alias("category")).show()
```

## 9. Configuration and Tuning
**Critical Settings**: Key configurations for performance optimization.

**Memory Configuration**:
```python
spark = SparkSession.builder \
    .appName("OptimizedApp") \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.cores", "4") \
    .config("spark.executor.instances", "10") \
    .config("spark.driver.memory", "2g") \
    .config("spark.driver.maxResultSize", "1g") \
    .getOrCreate()
```

**Performance Tuning**:
```python
# Adaptive Query Execution (Spark 3.0+)
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")

# Serialization
spark.conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")

# Shuffle optimization
spark.conf.set("spark.sql.shuffle.partitions", "200")  # Default 200
spark.conf.set("spark.sql.adaptive.shuffle.targetPostShuffleInputSize", "64MB")

# Arrow optimization for Pandas
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
```

## 10. Structured Streaming
**What it is**: Scalable and fault-tolerant stream processing engine built on Spark SQL.

**Basic Streaming**:
```python
# Read streaming data
streaming_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "input_topic") \
    .load()

# Process streaming data
processed_df = streaming_df \
    .select(col("value").cast("string").alias("message")) \
    .filter(col("message").contains("ERROR"))

# Write streaming output
query = processed_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .trigger(processingTime='10 seconds') \
    .start()

query.awaitTermination()
```

**Windowed Aggregations**:
```python
from pyspark.sql.functions import window

# Tumbling window
windowed_df = streaming_df \
    .groupBy(
        window(col("timestamp"), "10 minutes"),
        col("category")
    ) \
    .count()

# Sliding window
sliding_df = streaming_df \
    .groupBy(
        window(col("timestamp"), "10 minutes", "5 minutes"),
        col("category")
    ) \
    .count()
```

## 11. Error Handling and Debugging
**Common Patterns**: Handling failures and debugging Spark applications.

**Exception Handling**:
```python
try:
    result = df.collect()
except Exception as e:
    print(f"Spark job failed: {e}")
    # Log error details
    spark.sparkContext.setLogLevel("ERROR")
```

**Debugging Techniques**:
```python
# Explain query plan
df.explain(True)

# Show execution plan
df.queryExecution.executedPlan

# Cache intermediate results for debugging
intermediate_df = df.filter(col("status") == "active")
intermediate_df.cache()
print(f"Filtered records: {intermediate_df.count()}")

# Sample data for testing
sample_df = df.sample(0.1, seed=42)
```

## 12. Best Practices
**Performance and Reliability**: Key practices for production Spark applications.

**Data Processing**:
- Use DataFrames/Datasets over RDDs
- Leverage built-in functions over UDFs
- Cache frequently accessed data
- Use appropriate file formats (Parquet for analytics)

**Resource Management**:
- Right-size executors (2-5 cores per executor)
- Monitor memory usage and GC
- Use dynamic allocation when possible
- Set appropriate timeouts

**Code Organization**:
- Separate business logic from Spark code
- Use configuration files for parameters
- Implement proper logging
- Write unit tests for transformations