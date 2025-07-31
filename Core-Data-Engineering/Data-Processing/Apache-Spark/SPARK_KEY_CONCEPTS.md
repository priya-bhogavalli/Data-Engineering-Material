# Apache Spark Key Concepts

## 1. RDD (Resilient Distributed Dataset)
**What it is**: The fundamental data structure of Spark - an immutable, distributed collection of objects that can be processed in parallel.

**Key Properties**:
- **Resilient**: Fault-tolerant through lineage tracking
- **Distributed**: Partitioned across cluster nodes
- **Immutable**: Cannot be changed once created
- **Lazy Evaluation**: Transformations not executed until action called

**Creating RDDs**:
```python
from pyspark import SparkContext

sc = SparkContext()

# From Python collection
data = [1, 2, 3, 4, 5]
rdd = sc.parallelize(data, numSlices=4)

# From external file
text_rdd = sc.textFile("hdfs://path/to/file.txt")
json_rdd = sc.textFile("s3://bucket/data.json")

# From existing RDD
filtered_rdd = rdd.filter(lambda x: x > 2)
```

**RDD Operations**:
- **Transformations**: Return new RDD (map, filter, flatMap)
- **Actions**: Return values to driver (collect, count, save)

## 2. DataFrame and Dataset
**What they are**: Higher-level abstractions built on RDDs with schema information and query optimization.

**DataFrame Advantages**:
- **Schema**: Structured data with named columns
- **Catalyst Optimizer**: Query optimization engine
- **Code Generation**: Runtime code generation for performance
- **Language Agnostic**: Same API across Scala, Java, Python, R

**Creating DataFrames**:
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("DataFrameExample").getOrCreate()

# From file
df = spark.read.csv("path/to/file.csv", header=True, inferSchema=True)
df = spark.read.json("path/to/file.json")
df = spark.read.parquet("path/to/file.parquet")

# From RDD with schema
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("city", StringType(), True)
])

df = spark.createDataFrame(rdd, schema)

# From SQL query
df.createOrReplaceTempView("people")
result_df = spark.sql("SELECT name, age FROM people WHERE age > 21")
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
**Critical Concept**: Spark uses lazy evaluation - transformations are not executed until an action is called.

**Transformations (Lazy)**:
```python
# RDD transformations
mapped_rdd = rdd.map(lambda x: x * 2)
filtered_rdd = rdd.filter(lambda x: x > 5)
flat_mapped_rdd = rdd.flatMap(lambda x: x.split(" "))

# DataFrame transformations
df_filtered = df.filter(df.age > 21)
df_selected = df.select("name", "salary")
df_grouped = df.groupBy("department").agg({"salary": "avg"})

# Nothing executed yet - just building computation graph
```

**Actions (Eager)**:
```python
# RDD actions - trigger execution
result = rdd.collect()          # Bring all data to driver
count = rdd.count()             # Count elements
first = rdd.first()             # Get first element
sample = rdd.take(5)            # Get first 5 elements
rdd.saveAsTextFile("output/")   # Save to file

# DataFrame actions - trigger execution
df.show()                       # Display data
df.count()                      # Count rows
df.collect()                    # Bring all data to driver
df.write.csv("output/")         # Save to file
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