# Apache Spark - Key Concepts

## 🎯 What is Apache Spark?
Apache Spark is a unified analytics engine for large-scale data processing, providing high-level APIs for distributed computing. It's designed to be fast (up to 100x faster than Hadoop MapReduce), easy to use, and supports multiple programming languages (Scala, Java, Python, R).

## 🔑 Core Concepts

### 1. Spark Architecture

**Driver Program**: The main program that creates SparkContext and coordinates the entire Spark application. It:
- Converts user program into tasks
- Schedules tasks on executors
- Stores metadata about the application

**Executors**: Worker processes that:
- Run individual tasks
- Store data for the application
- Report status back to the driver
- Each executor has multiple cores and memory

**Cluster Manager**: Resource management system that allocates resources across applications:
- **Standalone**: Spark's built-in cluster manager
- **YARN**: Hadoop's resource manager
- **Kubernetes**: Container orchestration platform
- **Mesos**: General cluster resource manager

**SparkContext**: Entry point for Spark functionality, creates RDDs and manages the application

**SparkSession**: Unified entry point (Spark 2.0+) that combines SparkContext, SQLContext, and HiveContext

### 2. Core Data Structures

#### RDD (Resilient Distributed Dataset)
**Definition**: Fundamental data structure of Spark - an immutable, distributed collection of objects that can be processed in parallel.

**Key Properties**:
- **Resilient**: Fault-tolerant, can recover from node failures
- **Distributed**: Data is spread across multiple nodes
- **Dataset**: Collection of partitioned data
- **Immutable**: Cannot be changed once created
- **Lazy Evaluation**: Transformations are not executed until an action is called

**Lineage**: RDDs maintain information about how they were derived from other RDDs, enabling fault recovery

##### 🔒 Why Are RDDs Immutable?

**Q: Why can't we modify RDDs directly? What's the benefit of immutability?**

**A: RDD immutability is essential for distributed computing reliability and performance:**

**1. Fault Tolerance & Recovery**
```python
from pyspark import SparkContext
sc = SparkContext()

# Original RDD
rdd1 = sc.parallelize([1, 2, 3, 4, 5])
print(f"Original RDD: {rdd1.collect()}")
# Output: Original RDD: [1, 2, 3, 4, 5]

# Transformation creates NEW RDD (doesn't modify original)
rdd2 = rdd1.map(lambda x: x * 2)
rdd3 = rdd2.filter(lambda x: x > 5)

print(f"Original still unchanged: {rdd1.collect()}")
# Output: Original still unchanged: [1, 2, 3, 4, 5]
print(f"Final result: {rdd3.collect()}")
# Output: Final result: [6, 8, 10]

# If rdd3 fails, Spark can recreate it using lineage:
# rdd1 -> map -> filter (original rdd1 is unchanged)
```

**2. Thread Safety in Distributed Environment**
```python
# Multiple tasks can safely read the same RDD partition
rdd = sc.parallelize([1, 2, 3, 4, 5], 2)  # 2 partitions

# These operations run in parallel safely
result1 = rdd.map(lambda x: x * 2)     # Task 1
result2 = rdd.filter(lambda x: x > 3)  # Task 2

print(f"Doubled: {result1.collect()}")
# Output: Doubled: [2, 4, 6, 8, 10]
print(f"Filtered: {result2.collect()}")
# Output: Filtered: [4, 5]
print(f"Original safe: {rdd.collect()}")
# Output: Original safe: [1, 2, 3, 4, 5]
# No race conditions because RDD cannot be modified
```

**3. Enables Lazy Evaluation & Optimization**
```python
# Transformations build computation graph without execution
rdd1 = sc.parallelize([1, 2, 3, 4, 5])
rdd2 = rdd1.map(lambda x: x * 2)      # Not executed yet
rdd3 = rdd2.filter(lambda x: x > 5)   # Not executed yet

print("Transformations defined, but not executed yet")
# Output: Transformations defined, but not executed yet

# Immutability allows Spark to optimize entire pipeline
result = rdd3.collect()  # Now executes optimized plan
print(f"Optimized result: {result}")
# Output: Optimized result: [6, 8, 10]
```

**4. Safe Caching & Reuse**
```python
# Safe to cache immutable RDDs
rdd = sc.parallelize([1, 2, 3, 4, 5])
cached_rdd = rdd.map(lambda x: x * 2).cache()

# Multiple actions can safely use cached data
count = cached_rdd.count()
sum_val = cached_rdd.sum()
max_val = cached_rdd.max()

print(f"Count: {count}, Sum: {sum_val}, Max: {max_val}")
# Output: Count: 5, Sum: 30, Max: 10
# All operations use the same cached, immutable data
```

**Key Benefits Summary:**
- **Fault Recovery**: Can recreate lost partitions using lineage
- **Concurrency**: No locks needed for parallel access
- **Consistency**: Data never changes unexpectedly
- **Optimization**: Enables query planning and optimization
- **Debugging**: Predictable behavior and easier troubleshooting
- **Caching**: Safe to store and reuse data across operations

**Basic RDD Example:**
```python
# Create RDD
rdd = sc.parallelize([1, 2, 3, 4, 5])
squared = rdd.map(lambda x: x ** 2)  # Transformation
result = squared.collect()  # Action
print(result)
# Output: [1, 4, 9, 16, 25]
```

##### 🛠️ Complete RDD Functions Reference

**Q: What are all the available RDD functions and how do they work?**

**A: RDD functions are categorized into Transformations (lazy) and Actions (eager):**

**🔄 TRANSFORMATIONS (Return new RDD)**

**Element-wise Transformations:**
```python
rdd = sc.parallelize([1, 2, 3, 4, 5])

# map() - Apply function to each element
mapped = rdd.map(lambda x: x * 2)
print(mapped.collect())
# Output: [2, 4, 6, 8, 10]

# filter() - Keep elements that satisfy condition
filtered = rdd.filter(lambda x: x > 2)
print(filtered.collect())
# Output: [3, 4, 5]

# flatMap() - Apply function and flatten results
text_rdd = sc.parallelize(["hello world", "spark python"])
words = text_rdd.flatMap(lambda line: line.split())
print(words.collect())
# Output: ['hello', 'world', 'spark', 'python']

# mapPartitions() - Apply function to each partition
def process_partition(iterator):
    return [sum(iterator)]
partition_sums = rdd.mapPartitions(process_partition)
print(partition_sums.collect())
# Output: [15] (sum of all elements)
```

**Set Operations:**
```python
rdd1 = sc.parallelize([1, 2, 3, 4])
rdd2 = sc.parallelize([3, 4, 5, 6])

# union() - Combine RDDs
unioned = rdd1.union(rdd2)
print(unioned.collect())
# Output: [1, 2, 3, 4, 3, 4, 5, 6]

# intersection() - Common elements
intersected = rdd1.intersection(rdd2)
print(intersected.collect())
# Output: [3, 4]

# subtract() - Elements in first but not second
subtracted = rdd1.subtract(rdd2)
print(subtracted.collect())
# Output: [1, 2]

# distinct() - Remove duplicates
dups = sc.parallelize([1, 1, 2, 2, 3, 3])
unique = dups.distinct()
print(unique.collect())
# Output: [1, 2, 3]
```

**Key-Value Transformations:**
```python
# Create key-value RDD
kv_rdd = sc.parallelize([("a", 1), ("b", 2), ("a", 3), ("b", 4)])

# reduceByKey() - Reduce values for each key
reduced = kv_rdd.reduceByKey(lambda x, y: x + y)
print(reduced.collect())
# Output: [('a', 4), ('b', 6)]

# groupByKey() - Group values by key
grouped = kv_rdd.groupByKey()
print([(k, list(v)) for k, v in grouped.collect()])
# Output: [('a', [1, 3]), ('b', [2, 4])]

# mapValues() - Apply function to values only
mapped_values = kv_rdd.mapValues(lambda x: x * 10)
print(mapped_values.collect())
# Output: [('a', 10), ('b', 20), ('a', 30), ('b', 40)]

# keys() and values() - Extract keys or values
print(kv_rdd.keys().collect())
# Output: ['a', 'b', 'a', 'b']
print(kv_rdd.values().collect())
# Output: [1, 2, 3, 4]
```

**Join Operations:**
```python
rdd1 = sc.parallelize([("a", 1), ("b", 2), ("c", 3)])
rdd2 = sc.parallelize([("a", "x"), ("b", "y"), ("d", "z")])

# join() - Inner join
joined = rdd1.join(rdd2)
print(joined.collect())
# Output: [('a', (1, 'x')), ('b', (2, 'y'))]

# leftOuterJoin() - Left outer join
left_joined = rdd1.leftOuterJoin(rdd2)
print(left_joined.collect())
# Output: [('a', (1, 'x')), ('b', (2, 'y')), ('c', (3, None))]

# rightOuterJoin() - Right outer join
right_joined = rdd1.rightOuterJoin(rdd2)
print(right_joined.collect())
# Output: [('a', (1, 'x')), ('b', (2, 'y')), ('d', (None, 'z'))]
```

**Sorting and Sampling:**
```python
rdd = sc.parallelize([3, 1, 4, 1, 5, 9, 2, 6])

# sortBy() - Sort by key function
sorted_rdd = rdd.sortBy(lambda x: x)
print(sorted_rdd.collect())
# Output: [1, 1, 2, 3, 4, 5, 6, 9]

# sample() - Random sample
sampled = rdd.sample(False, 0.5, seed=42)  # 50% sample
print(f"Sample: {sampled.collect()}")
# Output: Sample: [3, 1, 5, 2] (varies due to randomness)

# takeSample() - Take exact number of samples
samples = rdd.takeSample(False, 3, seed=42)
print(f"3 samples: {samples}")
# Output: 3 samples: [4, 1, 9]
```

**⚡ ACTIONS (Return values to driver)**

**Collection Actions:**
```python
rdd = sc.parallelize([1, 2, 3, 4, 5])

# collect() - Return all elements
print(rdd.collect())
# Output: [1, 2, 3, 4, 5]

# take(n) - Return first n elements
print(rdd.take(3))
# Output: [1, 2, 3]

# first() - Return first element
print(rdd.first())
# Output: 1

# top(n) - Return top n elements
print(rdd.top(3))
# Output: [5, 4, 3]

# takeOrdered(n) - Return smallest n elements
print(rdd.takeOrdered(3))
# Output: [1, 2, 3]
```

**Aggregation Actions:**
```python
rdd = sc.parallelize([1, 2, 3, 4, 5])

# count() - Count elements
print(rdd.count())
# Output: 5

# sum() - Sum all elements
print(rdd.sum())
# Output: 15

# min() and max() - Min/max values
print(f"Min: {rdd.min()}, Max: {rdd.max()}")
# Output: Min: 1, Max: 5

# mean() - Average
print(rdd.mean())
# Output: 3.0

# reduce() - Reduce with function
product = rdd.reduce(lambda x, y: x * y)
print(product)
# Output: 120

# fold() - Fold with initial value
folded = rdd.fold(0, lambda x, y: x + y)
print(folded)
# Output: 15
```

**Statistical Actions:**
```python
rdd = sc.parallelize([1, 2, 3, 4, 5, 1, 2, 3])

# countByValue() - Count occurrences of each value
print(dict(rdd.countByValue()))
# Output: {1: 2, 2: 2, 3: 2, 4: 1, 5: 1}

# stats() - Statistical summary
stats = rdd.stats()
print(f"Count: {stats.count()}, Mean: {stats.mean()}, StdDev: {stats.stdev():.2f}")
# Output: Count: 8, Mean: 2.625, StdDev: 1.41
```

**Key-Value Actions:**
```python
kv_rdd = sc.parallelize([("a", 1), ("b", 2), ("a", 3)])

# countByKey() - Count values per key
print(dict(kv_rdd.countByKey()))
# Output: {'a': 2, 'b': 1}

# collectAsMap() - Collect as dictionary
print(kv_rdd.collectAsMap())
# Output: {'a': 3, 'b': 2} (last value per key)

# lookup(key) - Get values for specific key
print(kv_rdd.lookup("a"))
# Output: [1, 3]
```

**I/O Actions:**
```python
rdd = sc.parallelize(["line1", "line2", "line3"])

# saveAsTextFile() - Save to text files
rdd.saveAsTextFile("output_text")
print("Saved to output_text/ directory")
# Output: Saved to output_text/ directory

# foreach() - Apply function to each element (no return)
rdd.foreach(lambda x: print(f"Processing: {x}"))
# Output: Processing: line1
#         Processing: line2
#         Processing: line3
```

**🎯 Quick Reference Summary:**

**Most Common Transformations:**
- `map()`, `filter()`, `flatMap()`, `distinct()`
- `reduceByKey()`, `groupByKey()`, `join()`
- `union()`, `intersection()`, `sortBy()`

**Most Common Actions:**
- `collect()`, `count()`, `take()`, `first()`
- `reduce()`, `sum()`, `min()`, `max()`
- `saveAsTextFile()`, `foreach()`

#### DataFrame
**Definition**: Higher-level abstraction built on top of RDDs, representing a distributed collection of data organized into named columns (like a table in relational database).

**Key Features**:
- **Schema**: Has a defined structure with column names and types
- **Catalyst Optimizer**: Automatic query optimization
- **Language Agnostic**: Same API across Scala, Java, Python, R
- **Integration**: Works with various data sources (JSON, Parquet, JDBC, etc.)
- **Performance**: More efficient than RDDs due to optimizations
```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("DataProcessing").getOrCreate()

# Create DataFrame from sample data
data = [("Alice", 150, "Engineering"), ("Bob", 80, "Sales"), ("Charlie", 200, "Engineering")]
df = spark.createDataFrame(data, ["name", "salary", "department"])

# Filter and select
result = df.select("name", "salary").filter(df.salary > 100)
result.show()
# Output:
# +-------+------+
# |   name|salary|
# +-------+------+
# |  Alice|   150|
# |Charlie|   200|
# +-------+------+
```

##### 🆚 RDD vs DataFrame Comparison

**Q: What are the key differences between RDD and DataFrame? When should I use each?**

**A: Here's a comprehensive comparison:**

| **Aspect** | **RDD** | **DataFrame** |
|------------|---------|---------------|
| **🏢 Abstraction Level** | Low-level, functional programming | High-level, SQL-like operations |
| **📊 Schema** | No schema, unstructured data | Structured with defined schema |
| **⚡ Performance** | Slower due to serialization overhead | Faster with Catalyst optimizer |
| **🛠️ Optimization** | No automatic optimization | Automatic query optimization |
| **📝 API Style** | Functional (map, filter, reduce) | SQL + DataFrame operations |
| **🌍 Language Support** | Scala, Java, Python | Scala, Java, Python, R, SQL |
| **💾 Memory Usage** | Higher due to Java object overhead | Lower with Tungsten execution |
| **🔍 Type Safety** | Compile-time type safety (Scala/Java) | Runtime type checking |
| **📈 Ease of Use** | More complex, requires functional programming | Easier, SQL-like syntax |
| **🔗 Data Sources** | Limited built-in support | Rich data source API |
| **📊 Analytics** | Manual aggregations | Built-in analytical functions |
| **🔄 Lazy Evaluation** | Yes | Yes |
| **🛡️ Fault Tolerance** | Lineage-based recovery | Lineage-based recovery |
| **📝 Code Readability** | More verbose | More concise and readable |

**📊 Performance Comparison Example:**
```python
# Same operation: Filter and sum salaries > 100
data = [("Alice", 150), ("Bob", 80), ("Charlie", 200), ("David", 120)]

# RDD Approach
rdd = sc.parallelize(data)
rdd_result = rdd.filter(lambda x: x[1] > 100).map(lambda x: x[1]).sum()
print(f"RDD Result: {rdd_result}")
# Output: RDD Result: 470

# DataFrame Approach (More optimized)
df = spark.createDataFrame(data, ["name", "salary"])
df_result = df.filter(df.salary > 100).agg({"salary": "sum"}).collect()[0][0]
print(f"DataFrame Result: {df_result}")
# Output: DataFrame Result: 470

# DataFrame with SQL (Even more readable)
df.createOrReplaceTempView("employees")
sql_result = spark.sql("SELECT SUM(salary) FROM employees WHERE salary > 100").collect()[0][0]
print(f"SQL Result: {sql_result}")
# Output: SQL Result: 470
```

**🔍 Type Safety Comparison:**
```python
# RDD - Runtime errors possible
rdd = sc.parallelize([1, 2, "three", 4])
try:
    result = rdd.map(lambda x: x * 2).collect()
    print(result)
except Exception as e:
    print(f"RDD Error: {e}")
# Output: RDD Error: can't multiply sequence by non-int of type 'int'

# DataFrame - Schema validation
from pyspark.sql.types import StructType, StructField, IntegerType
schema = StructType([StructField("value", IntegerType(), True)])
try:
    df = spark.createDataFrame([(1,), (2,), ("three",), (4,)], schema)
    df.show()
except Exception as e:
    print(f"DataFrame Error: {e}")
# Output: DataFrame Error: invalid literal for int() with base 10: 'three'
```

**💾 Memory Usage Comparison:**
```python
# Create large dataset for comparison
large_data = [(i, f"name_{i}", i * 100) for i in range(100000)]

# RDD memory usage (higher)
rdd = sc.parallelize(large_data)
rdd.cache()
print(f"RDD partitions: {rdd.getNumPartitions()}")
# Output: RDD partitions: 8

# DataFrame memory usage (lower with Tungsten)
df = spark.createDataFrame(large_data, ["id", "name", "value"])
df.cache()
print(f"DataFrame partitions: {df.rdd.getNumPartitions()}")
# Output: DataFrame partitions: 8
print(f"DataFrame optimized storage: Tungsten binary format")
# Output: DataFrame optimized storage: Tungsten binary format
```

**🎯 When to Use Each:**

**Use RDD When:**
- Working with unstructured data (text files, binary data)
- Need fine-grained control over data distribution
- Complex data transformations not easily expressed in SQL
- Working with non-tabular data formats
- Need compile-time type safety (Scala/Java)

**Use DataFrame When:**
- Working with structured/semi-structured data
- Need better performance and optimization
- Want SQL-like operations and readability
- Integrating with various data sources
- Building analytical applications
- Team has SQL background

**📈 Migration Example:**
```python
# Converting RDD operations to DataFrame
# RDD approach
text_rdd = sc.textFile("logs.txt")
word_counts_rdd = text_rdd.flatMap(lambda line: line.split()) \
                         .map(lambda word: (word, 1)) \
                         .reduceByKey(lambda a, b: a + b)
print("RDD word count completed")
# Output: RDD word count completed

# DataFrame approach (more optimized)
from pyspark.sql.functions import split, explode, count
df = spark.read.text("logs.txt")
word_counts_df = df.select(explode(split(df.value, " ")).alias("word")) \
                   .groupBy("word").count() \
                   .orderBy("count", ascending=False)
print("DataFrame word count completed with optimization")
# Output: DataFrame word count completed with optimization
```

**📉 Performance Benchmark Results:**
- **DataFrame**: 2-5x faster than RDD for structured data operations
- **Memory**: 40-60% less memory usage with Tungsten
- **CPU**: Better CPU utilization with code generation
- **I/O**: Optimized data source connectors

#### Dataset (Scala/Java)
**Definition**: Type-safe version of DataFrame that combines the benefits of RDDs (type safety) with the optimizations of DataFrames.

**Key Features**:
- **Type Safety**: Compile-time type checking
- **Object-Oriented**: Work with domain objects
- **Performance**: Catalyst optimizer + Tungsten execution engine
- **Encoders**: Efficient serialization between JVM objects and Spark's internal format
```scala
case class Person(name: String, age: Int)
val ds = spark.read.json("people.json").as[Person]
ds.filter(_.age > 21).show()
// Output:
// +-----+---+
// | name|age|
// +-----+---+
// | John| 25|
// |Sarah| 30|
// +-----+---+
```

### 3. Transformations vs Actions

#### Transformations (Lazy)
**Definition**: Operations that create a new RDD/DataFrame from an existing one. They are lazy, meaning they don't execute immediately but build up a computation graph.

**Characteristics**:
- **Lazy Evaluation**: Not executed until an action is called
- **Lineage**: Build dependency graph for fault tolerance
- **Optimization**: Allow Spark to optimize the entire pipeline

**Types**:
- **Narrow**: Each input partition contributes to only one output partition (map, filter)
- **Wide**: Input partitions contribute to multiple output partitions (groupBy, join)
```python
# These don't execute immediately (lazy evaluation)
df_filtered = df.filter(df.age > 21)
df_selected = df_filtered.select("name", "age")
df_grouped = df_selected.groupBy("age").count()

# Only when action is called:
df_grouped.show()
# Output:
# +---+-----+
# |age|count|
# +---+-----+
# | 25|    1|
# | 30|    2|
# +---+-----+
```

#### Actions (Eager)
**Definition**: Operations that trigger the execution of transformations and return results to the driver program or write data to external storage.

**Characteristics**:
- **Eager Evaluation**: Execute immediately when called
- **Trigger Computation**: Cause the entire DAG to be executed
- **Return Values**: Produce concrete results (not RDDs/DataFrames)
```python
# These trigger execution
df.show()           # Display data
# Output:
# +-------+---+----------+
# |   name|age|department|
# +-------+---+----------+
# |  Alice| 25|Engineering|
# |    Bob| 30|     Sales|
# |Charlie| 35|Engineering|
# +-------+---+----------+

print(df.count())   # Count rows
# Output: 3

result = df.collect()  # Collect to driver
print(result)
# Output: [Row(name='Alice', age=25, department='Engineering'), ...]

df.write.csv("output")  # Write to storage
# Output: Files written to output/ directory
```

### 4. Common Operations

#### Data Loading
```python
# Various formats
df_csv = spark.read.csv("employees.csv", header=True, inferSchema=True)
print(f"CSV rows: {df_csv.count()}")
# Output: CSV rows: 1000

df_json = spark.read.json("users.json")
df_json.printSchema()
# Output:
# root
#  |-- name: string (nullable = true)
#  |-- age: long (nullable = true)

df_parquet = spark.read.parquet("sales.parquet")
print(f"Parquet partitions: {df_parquet.rdd.getNumPartitions()}")
# Output: Parquet partitions: 4

df_table = spark.read.table("warehouse.customers")
df_table.show(3)
# Output: First 3 rows of the table
```

#### Data Transformation
```python
from pyspark.sql.functions import col, when, sum, avg

# Sample data
data = [("A", 150, 85), ("B", 80, 92), ("C", 200, 78)]
df = spark.createDataFrame(data, ["name", "value", "score"])

# Column operations
df_new = df.withColumn("doubled", col("value") * 2)
df_new.show()
# Output:
# +----+-----+-----+-------+
# |name|value|score|doubled|
# +----+-----+-----+-------+
# |   A|  150|   85|    300|
# |   B|   80|   92|    160|
# |   C|  200|   78|    400|
# +----+-----+-----+-------+

df_cat = df.withColumn("category", when(col("value") > 100, "high").otherwise("low"))
df_cat.show()
# Output:
# +----+-----+-----+--------+
# |name|value|score|category|
# +----+-----+-----+--------+
# |   A|  150|   85|    high|
# |   B|   80|   92|     low|
# |   C|  200|   78|    high|
# +----+-----+-----+--------+

# Aggregations
result = df_cat.groupBy("category").agg(sum("value").alias("total_value"), avg("score").alias("avg_score"))
result.show()
# Output:
# +--------+-----------# Apache Spark Key Concepts for Data Engineering

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Core Components](#-core-components)
   - [RDDs (Resilient Distributed Datasets)](#rdds-resilient-distributed-datasets)
   - [DataFrames](#dataframes)
   - [Datasets](#datasets)
3. [Spark Architecture](#-spark-architecture)
4. [Spark SQL](#-spark-sql)
5. [Streaming (Structured Streaming)](#-streaming-structured-streaming)
6. [Performance Optimization](#-performance-optimization)
   - [Partitioning](#1-partitioning)
   - [Caching](#2-caching)
   - [Broadcast Variables](#3-broadcast-variables)
6. [Configuration](#️-configuration)
7. [When to Use Spark](#-when-to-use-spark)
8. [Interview Focus Areas](#-interview-focus-areas)
9. [Quick References](#-quick-references)

---

## 🎯 Overview

Apache Spark is a unified analytics engine for large-scale data processing with built-in modules for streaming, SQL, machine learning, and graph processing.

**Key Benefits:**
- **Speed**: 100x faster than Hadoop MapReduce due to in-memory computing
- **Ease of Use**: Simple APIs in Java, Scala, Python, and R
- **Generality**: Combines SQL, streaming, and complex analytics
- **Runs Everywhere**: YARN, Mesos, Kubernetes, standalone, or cloud

+------------------+
# |category|total_value|         avg_score|
# +--------+-----------+------------------+
# |    high|        350|              81.5|
# |     low|         80|              92.0|
# +--------+-----------+------------------+
```

## 📦 Core Components

### RDDs (Resilient Distributed Datasets)
**Definition**: Fundamental data structure of Spark - immutable distributed collection of objects.

**Key Characteristics**:
- **Immutable**: Cannot be changed after creation
- **Distributed**: Partitioned across cluster nodes
- **Fault-tolerant**: Recovers from failures using lineage
- **Lazy evaluation**: Computed only when actions are called

```python
# Create RDD
rdd = spark.sparkContext.parallelize([1, 2, 3, 4, 5])
print(f"RDD created with {rdd.count()} elements")
# Output: RDD created with 5 elements

# Transformations (lazy)
mapped_rdd = rdd.map(lambda x: x * 2)
filtered_rdd = mapped_rdd.filter(lambda x: x > 5)

# Action (triggers execution)
result = filtered_rdd.collect()
print(f"Result: {result}")
# Output: Result: [6, 8, 10]
```

### DataFrames
**Definition**: Distributed collection of data organized into named columns, similar to a table in relational database.

**Key Features**:
- **Schema**: Structured data with defined column types
- **Catalyst Optimization**: Automatic query optimization
- **SQL Support**: Can be queried using SQL syntax
- **Language Agnostic**: Same API across Python, Scala, Java, R

```python
# Create DataFrame
data = [("Alice", 25, "Engineer"), ("Bob", 30, "Manager"), ("Charlie", 35, "Analyst")]
df = spark.createDataFrame(data, ["name", "age", "role"])

# DataFrame operations
result = df.filter(df.age > 25).select("name", "role")
result.show()
# Output:
# +-------+-------+
# |   name|   role|
# +-------+-------+
# |    Bob|Manager|
# |Charlie|Analyst|
# +-------+-------+
```

### Datasets
**Definition**: Type-safe version of DataFrames (available in Scala/Java only, not Python).

**Key Features**:
- **Type Safety**: Compile-time type checking
- **Object-Oriented**: Work with JVM objects
- **Performance**: Same optimizations as DataFrames
- **Encoder**: Automatic serialization/deserialization

#### Data Saving
```python
# Write in various formats
df.write.mode("overwrite").csv("output.csv")
print("CSV files written to output.csv/")
# Output: CSV files written to output.csv/

df.write.mode("append").parquet("output.parquet")
print("Data appended to output.parquet/")
# Output: Data appended to output.parquet/

df.write.mode("overwrite").saveAsTable("database.employees")
print("Table database.employees created/updated")
# Output: Table database.employees created/updated
```

## 🚀 Spark SQL

**Definition**: Module for structured data processing that provides a programming interface for working with structured and semi-structured data.

**Key Components**:
- **Catalyst Optimizer**: Rule-based query optimizer
- **Tungsten**: Execution engine for memory management and code generation
- **Data Sources API**: Unified interface for reading from various sources
- **Hive Integration**: Compatible with Hive metastore and HiveQL

### Using SQL Syntax
```python
# Sample sales data
sales_data = [("Electronics", 1000, "2023-06-01"), ("Clothing", 500, "2023-06-02"), 
              ("Electronics", 1500, "2023-06-03"), ("Books", 300, "2023-06-04")]
df = spark.createDataFrame(sales_data, ["category", "amount", "date"])

# Register DataFrame as temp view
df.createOrReplaceTempView("sales")

# Use SQL
result = spark.sql("""
    SELECT category, SUM(amount) as total
    FROM sales
    WHERE date >= '2023-01-01'
    GROUP BY category
    ORDER BY total DESC
""")

result.show()
# Output:
# +-----------+-----+
# |   category|total|
# +-----------+-----+
# |Electronics| 2500|
# |   Clothing|  500|
# |      Books|  300|
# +-----------+-----+
```

## 🏧 Spark Architecture

**Definition**: Master-slave architecture with driver program coordinating work across distributed executors.

**Core Components**:
- **Driver Program**: Coordinates the application, maintains SparkContext
- **Cluster Manager**: Manages resources (YARN, Mesos, Kubernetes, Standalone)
- **Executors**: Run tasks and store data on worker nodes
- **Tasks**: Units of work sent to executors

```python
# Check cluster information
print(f"Application ID: {spark.sparkContext.applicationId}")
print(f"Application Name: {spark.sparkContext.appName}")
print(f"Master URL: {spark.sparkContext.master}")
print(f"Spark Version: {spark.version}")

# Output:
# Application ID: app-20240101-123456-0001
# Application Name: MySparkApp
# Master URL: local[*]
# Spark Version: 3.4.0
```

## 🔄 Streaming (Structured Streaming)

**Definition**: Scalable and fault-tolerant stream processing engine built on Spark SQL, treating streaming data as unbounded tables.

**Key Concepts**:
- **Micro-batches**: Processes streaming data in small batches
- **Event Time**: Processing based on when events occurred
- **Watermarking**: Handling late-arriving data
- **Output Modes**: Complete, Append, Update
- **Checkpointing**: Fault tolerance through write-ahead logs

### Basic Streaming
```python
# Read stream from Kafka
stream_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "user_events") \
    .load()

# Process stream - parse JSON and count by category
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType

schema = StructType([StructField("category", StringType(), True)])
processed = stream_df.select(from_json(col("value").cast("string"), schema).alias("data")) \
    .select("data.category") \
    .groupBy("category").count()

# Write stream to console
query = processed.writeStream \
    .outputMode("complete") \
    .format("console") \
    .trigger(processingTime='10 seconds') \
    .start()

# Output (every 10 seconds):
# +----------+-----+
# |  category|count|
# +----------+-----+
# |     games|   45|
# |     music|   32|
# |     video|   78|
# +----------+-----+

query.awaitTermination()
```

## ⚡ Performance Optimization

**Definition**: Techniques to improve Spark application performance through better resource utilization, data organization, and execution strategies.

### 1. Partitioning
**Definition**: Dividing data into smaller, manageable chunks distributed across cluster nodes.

**Benefits**:
- **Parallelism**: More partitions = more parallel tasks
- **Data Locality**: Keep related data together
- **Reduced Shuffling**: Minimize data movement across network
```python
# Check current partitions
print(f"Original partitions: {df.rdd.getNumPartitions()}")
# Output: Original partitions: 2

# Repartition for better parallelism
df_repartitioned = df.repartition(10, "department")
print(f"After repartition: {df_repartitioned.rdd.getNumPartitions()}")
# Output: After repartition: 10

# Coalesce to reduce partitions (more efficient than repartition)
df_coalesced = df_repartitioned.coalesce(5)
print(f"After coalesce: {df_coalesced.rdd.getNumPartitions()}")
# Output: After coalesce: 5
```

### 2. Caching
**Definition**: Storing frequently accessed data in memory or disk to avoid recomputation.

**Storage Levels**:
- **MEMORY_ONLY**: Store in memory as deserialized objects
- **MEMORY_AND_DISK**: Spill to disk if memory is full
- **DISK_ONLY**: Store only on disk
- **MEMORY_ONLY_SER**: Store as serialized objects in memory
```python
from pyspark import StorageLevel

# Cache frequently used DataFrames
df.cache()  # Default: MEMORY_AND_DISK
print("DataFrame cached in memory")
# Output: DataFrame cached in memory

# Check if cached
print(f"Is cached: {df.is_cached}")
# Output: Is cached: True

# Persist with specific storage level
df.persist(StorageLevel.MEMORY_AND_DISK_SER)
print("DataFrame persisted with serialization")
# Output: DataFrame persisted with serialization

# Unpersist to free memory
df.unpersist()
print(f"Is cached after unpersist: {df.is_cached}")
# Output: Is cached after unpersist: False
```

### 3. Broadcast Variables
**Definition**: Read-only variables cached on each machine rather than shipping a copy with each task.

**Use Cases**:
- **Lookup Tables**: Small reference data used in joins
- **Configuration**: Application settings needed by all tasks
- **Machine Learning Models**: Trained models for prediction
```python
# Create lookup dictionary
lookup_dict = {"A": "Apple", "B": "Banana", "C": "Cherry"}

# Broadcast small lookup tables
broadcast_var = spark.sparkContext.broadcast(lookup_dict)
print(f"Broadcast variable created with {len(broadcast_var.value)} items")
# Output: Broadcast variable created with 3 items

# Use in transformations
def lookup_name(code):
    return broadcast_var.value.get(code, "Unknown")

# Apply to DataFrame
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

lookup_udf = udf(lookup_name, StringType())
data = [("A", 100), ("B", 200), ("C", 150)]
df = spark.createDataFrame(data, ["code", "value"])

result = df.withColumn("name", lookup_udf(df.code))
result.show()
# Output:
# +----+-----+------+
# |code|value|  name|
# +----+-----+------+
# |   A|  100| Apple|
# |   B|  200|Banana|
# |   C|  150|Cherry|
# +----+-----+------+
```

## 🛠️ Configuration

**Definition**: Settings that control Spark application behavior, resource allocation, and performance characteristics.

**Key Configuration Areas**:
- **Application Properties**: App name, master URL
- **Runtime Environment**: Executor memory, cores, instances
- **Shuffle Behavior**: Partitions, serialization
- **Spark SQL**: Adaptive query execution, join strategies

### Spark Session Configuration
```python
spark = SparkSession.builder \
    .appName("MyOptimizedApp") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.cores", "2") \
    .config("spark.sql.adaptive.skewJoin.enabled", "true") \
    .getOrCreate()

# Verify configuration
print(f"App Name: {spark.sparkContext.appName}")
# Output: App Name: MyOptimizedApp

print(f"Executor Memory: {spark.conf.get('spark.executor.memory')}")
# Output: Executor Memory: 4g

print(f"Adaptive Query Execution: {spark.conf.get('spark.sql.adaptive.enabled')}")
# Output: Adaptive Query Execution: true

# Check Spark version and configuration
print(f"Spark Version: {spark.version}")
# Output: Spark Version: 3.4.0
```

## 🤖 Machine Learning (MLlib)

**Definition**: Spark's scalable machine learning library providing common algorithms and utilities.

**Key Components**:
- **ML Pipelines**: High-level API for building ML workflows
- **Feature Engineering**: Transformers for data preparation
- **Algorithms**: Classification, regression, clustering, collaborative filtering
- **Model Selection**: Cross-validation and hyperparameter tuning

```python
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline

# Sample data
data = [(1.0, 2.0, 1), (2.0, 3.0, 0), (3.0, 4.0, 1)]
df = spark.createDataFrame(data, ["feature1", "feature2", "label"])

# Create ML pipeline
assembler = VectorAssembler(inputCols=["feature1", "feature2"], outputCol="features")
lr = LogisticRegression(featuresCol="features", labelCol="label")
pipeline = Pipeline(stages=[assembler, lr])

# Train model
model = pipeline.fit(df)
print("Model trained successfully")
# Output: Model trained successfully
```

## 📊 When to Use Spark
- **Large datasets**: > 1GB, distributed processing needed
- **Complex transformations**: Multiple joins, aggregations
- **Batch processing**: ETL jobs, data warehousing
- **Stream processing**: Real-time data processing
- **Machine learning**: MLlib for distributed ML

## 🎯 Interview Focus Areas
1. **Architecture**: Driver, executors, cluster managers
2. **Data structures**: RDD vs DataFrame vs Dataset comparison
3. **RDD Functions**: Complete list of transformations and actions
4. **Immutability**: Why RDDs are immutable and benefits
5. **Performance**: RDD vs DataFrame performance differences
6. **Lazy evaluation**: Transformations vs actions
7. **Optimization**: Catalyst optimizer and Tungsten engine
8. **SQL integration**: Spark SQL, DataFrame API
9. **Streaming**: Structured streaming concepts
10. **Deployment**: Cluster modes, resource management

## 📚 Quick References
- [Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API](https://spark.apache.org/docs/latest/api/python/)
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [Structured Streaming](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)