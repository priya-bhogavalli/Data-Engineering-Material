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
```python
from pyspark import SparkContext
sc = SparkContext()

# Create RDD
rdd = sc.parallelize([1, 2, 3, 4, 5])
squared = rdd.map(lambda x: x ** 2)  # Transformation
result = squared.collect()  # Action
print(result)
# Output: [1, 4, 9, 16, 25]
```

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
# +--------+-----------+------------------+
# |category|total_value|         avg_score|
# +--------+-----------+------------------+
# |    high|        350|              81.5|
# |     low|         80|              92.0|
# +--------+-----------+------------------+
```

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

## 📊 When to Use Spark
- **Large datasets**: > 1GB, distributed processing needed
- **Complex transformations**: Multiple joins, aggregations
- **Batch processing**: ETL jobs, data warehousing
- **Stream processing**: Real-time data processing
- **Machine learning**: MLlib for distributed ML

## 🎯 Interview Focus Areas
1. **Architecture**: Driver, executors, cluster managers
2. **Data structures**: RDD vs DataFrame vs Dataset
3. **Lazy evaluation**: Transformations vs actions
4. **Performance**: Partitioning, caching, broadcast
5. **SQL integration**: Spark SQL, Catalyst optimizer
6. **Streaming**: Structured streaming concepts
7. **Deployment**: Cluster modes, resource management

## 📚 Quick References
- [Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API](https://spark.apache.org/docs/latest/api/python/)
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [Structured Streaming](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)