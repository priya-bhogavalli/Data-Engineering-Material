# Apache Spark - Key Concepts

## 🎯 What is Apache Spark?
Apache Spark is a unified analytics engine for large-scale data processing, providing high-level APIs for distributed computing.

## 🔑 Core Concepts

### 1. Spark Architecture
- **Driver**: Coordinates the Spark application
- **Executors**: Run tasks on worker nodes
- **Cluster Manager**: Manages resources (YARN, Kubernetes, Standalone)

### 2. Core Data Structures

#### RDD (Resilient Distributed Dataset)
```python
from pyspark import SparkContext
sc = SparkContext()

# Create RDD
rdd = sc.parallelize([1, 2, 3, 4, 5])
squared = rdd.map(lambda x: x ** 2)  # Transformation
result = squared.collect()  # Action
```

#### DataFrame
```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("DataProcessing").getOrCreate()

# Create DataFrame
df = spark.read.csv("data.csv", header=True, inferSchema=True)
df.select("column1", "column2").filter(df.column1 > 100).show()
```

#### Dataset (Scala/Java)
```scala
case class Person(name: String, age: Int)
val ds = spark.read.json("people.json").as[Person]
ds.filter(_.age > 21).show()
```

### 3. Transformations vs Actions

#### Transformations (Lazy)
```python
# These don't execute immediately
df_filtered = df.filter(df.age > 21)
df_selected = df_filtered.select("name", "age")
df_grouped = df_selected.groupBy("age").count()
```

#### Actions (Eager)
```python
# These trigger execution
df.show()           # Display data
df.count()          # Count rows
df.collect()        # Collect to driver
df.write.csv("output")  # Write to storage
```

### 4. Common Operations

#### Data Loading
```python
# Various formats
df_csv = spark.read.csv("file.csv", header=True)
df_json = spark.read.json("file.json")
df_parquet = spark.read.parquet("file.parquet")
df_table = spark.read.table("database.table")
```

#### Data Transformation
```python
from pyspark.sql.functions import col, when, sum, avg

# Column operations
df.withColumn("new_col", col("old_col") * 2)
df.withColumn("category", when(col("value") > 100, "high").otherwise("low"))

# Aggregations
df.groupBy("category").agg(sum("amount"), avg("score"))

# Joins
df1.join(df2, df1.id == df2.id, "inner")
```

#### Data Saving
```python
# Write in various formats
df.write.mode("overwrite").csv("output.csv")
df.write.mode("append").parquet("output.parquet")
df.write.mode("overwrite").saveAsTable("database.table")
```

## 🚀 Spark SQL

### Using SQL Syntax
```python
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
```

## 🔄 Streaming (Structured Streaming)

### Basic Streaming
```python
# Read stream
stream_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "topic") \
    .load()

# Process stream
processed = stream_df.select("value").groupBy("category").count()

# Write stream
query = processed.writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()
```

## ⚡ Performance Optimization

### 1. Partitioning
```python
# Repartition for better parallelism
df.repartition(10, "partition_column")

# Coalesce to reduce partitions
df.coalesce(5)
```

### 2. Caching
```python
# Cache frequently used DataFrames
df.cache()
df.persist(StorageLevel.MEMORY_AND_DISK)
```

### 3. Broadcast Variables
```python
# Broadcast small lookup tables
broadcast_var = spark.sparkContext.broadcast(lookup_dict)
```

## 🛠️ Configuration

### Spark Session Configuration
```python
spark = SparkSession.builder \
    .appName("MyApp") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.cores", "2") \
    .getOrCreate()
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