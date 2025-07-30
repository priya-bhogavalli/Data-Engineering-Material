# PySpark Key Concepts

## 1. Spark Architecture
**Components**:
- **Driver**: Main program coordinating execution
- **Executors**: Worker processes running tasks
- **Cluster Manager**: Resource allocation (YARN, Mesos, K8s)

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("DataProcessing") \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.cores", "2") \
    .getOrCreate()
```

## 2. RDDs (Resilient Distributed Datasets)
```python
# Create RDD
rdd = spark.sparkContext.parallelize([1, 2, 3, 4, 5])
text_rdd = spark.sparkContext.textFile("hdfs://data.txt")

# Transformations (lazy)
filtered = rdd.filter(lambda x: x > 2)
mapped = rdd.map(lambda x: x * 2)
flat_mapped = text_rdd.flatMap(lambda line: line.split())

# Actions (trigger execution)
result = filtered.collect()
count = rdd.count()
first_element = rdd.first()
```

## 3. DataFrames
```python
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Create DataFrame
df = spark.read.csv("data.csv", header=True, inferSchema=True)
df = spark.read.json("data.json")
df = spark.read.parquet("data.parquet")

# Schema definition
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])

# Basic operations
df.select("name", "age").show()
df.filter(F.col("age") > 25).show()
df.groupBy("department").agg(F.avg("salary")).show()
df.orderBy(F.desc("salary")).show()
```

## 4. SQL Operations
```python
# Register as temp view
df.createOrReplaceTempView("employees")

# SQL queries
result = spark.sql("""
    SELECT department, AVG(salary) as avg_salary
    FROM employees
    WHERE age > 25
    GROUP BY department
    ORDER BY avg_salary DESC
""")

# Window functions
from pyspark.sql.window import Window

window_spec = Window.partitionBy("department").orderBy(F.desc("salary"))
df.withColumn("rank", F.row_number().over(window_spec)).show()
```

## 5. Data Processing Patterns
```python
# ETL Pipeline
def process_sales_data():
    # Extract
    raw_df = spark.read.csv("sales.csv", header=True)
    
    # Transform
    cleaned_df = raw_df \
        .filter(F.col("amount") > 0) \
        .withColumn("date", F.to_date("date_str", "yyyy-MM-dd")) \
        .withColumn("year", F.year("date")) \
        .groupBy("year", "product") \
        .agg(F.sum("amount").alias("total_sales"))
    
    # Load
    cleaned_df.write.mode("overwrite").parquet("output/sales_summary")

# Streaming
stream_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "events") \
    .load()

query = stream_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()
```

## 6. Performance Optimization
```python
# Caching
df.cache()
df.persist(StorageLevel.MEMORY_AND_DISK)

# Partitioning
df.repartition(4, "department")
df.coalesce(2)

# Broadcast joins
from pyspark.sql.functions import broadcast
large_df.join(broadcast(small_df), "key")

# Bucketing
df.write.bucketBy(4, "user_id").saveAsTable("bucketed_table")
```

## 7. UDFs and Complex Types
```python
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

# User Defined Function
@udf(returnType=StringType())
def categorize_age(age):
    if age < 18: return "Minor"
    elif age < 65: return "Adult"
    else: return "Senior"

df.withColumn("age_category", categorize_age("age")).show()

# Working with arrays and maps
df.withColumn("tags", F.split("tag_string", ",")) \
  .withColumn("tag_count", F.size("tags")) \
  .show()
```

## 8. Streaming Processing
```python
# Structured Streaming
streaming_df = spark.readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

word_counts = streaming_df \
    .select(F.explode(F.split("value", " ")).alias("word")) \
    .groupBy("word") \
    .count()

query = word_counts.writeStream \
    .outputMode("complete") \
    .format("console") \
    .trigger(processingTime='10 seconds') \
    .start()
```

## 9. Configuration and Tuning
```python
# Spark configuration
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")

# Memory management
spark.conf.set("spark.executor.memory", "8g")
spark.conf.set("spark.executor.memoryFraction", "0.8")
spark.conf.set("spark.sql.shuffle.partitions", "200")
```

## 10. Error Handling and Monitoring
```python
# Exception handling
try:
    df = spark.read.csv("data.csv")
    result = df.count()
except Exception as e:
    print(f"Error processing data: {e}")
    spark.stop()

# Monitoring
print(f"Partitions: {df.rdd.getNumPartitions()}")
df.explain(True)  # Show execution plan
spark.sparkContext.getConf().getAll()  # Show configuration
```