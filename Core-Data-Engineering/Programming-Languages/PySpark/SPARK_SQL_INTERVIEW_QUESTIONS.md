# Spark SQL Interview Questions for Data Engineering

## 🎯 Overview
Spark SQL is Apache Spark's module for working with structured data using SQL queries and DataFrame API. It provides a programming abstraction called DataFrames and can act as a distributed SQL query engine.

## 📋 Table of Contents
1. [Basic Concepts (1-20)](#basic-concepts-1-20)
2. [DataFrame Operations (21-40)](#dataframe-operations-21-40)
3. [Performance Optimization (41-60)](#performance-optimization-41-60)
4. [Advanced Features (61-80)](#advanced-features-61-80)
5. [Integration & Deployment (81-100)](#integration--deployment-81-100)

---

## Basic Concepts (1-20)

### 1. What is Spark SQL and how does it differ from traditional SQL?
**Answer:** Spark SQL is a module for structured data processing that provides SQL interface to Spark. Key differences:
- **Distributed**: Runs across cluster nodes
- **In-memory**: Caches data in memory for faster processing
- **Schema-on-read**: Flexible schema handling
- **Integration**: Works with various data sources (Parquet, JSON, Hive, JDBC)

```sql
-- Traditional SQL (single machine)
SELECT customer_id, SUM(amount) FROM sales GROUP BY customer_id;

-- Spark SQL (distributed)
spark.sql("""
    SELECT customer_id, SUM(amount) 
    FROM sales 
    GROUP BY customer_id
""").show()
```

### 2. What is the Catalyst Optimizer?
**Answer:** Catalyst is Spark SQL's query optimizer that automatically optimizes SQL queries and DataFrame operations.

**Optimization phases:**
1. **Logical Plan**: Parse SQL to logical plan
2. **Optimized Logical Plan**: Apply rule-based optimizations
3. **Physical Plan**: Generate physical execution plans
4. **Code Generation**: Generate Java bytecode

```python
# View execution plan
df.explain(True)  # Shows all optimization phases
```

### 3. How do you create and register temporary views?
**Answer:** Temporary views allow SQL queries on DataFrames.

```python
# Create DataFrame
df = spark.read.parquet("sales.parquet")

# Register temporary view
df.createOrReplaceTempView("sales")

# Use in SQL
result = spark.sql("SELECT * FROM sales WHERE amount > 1000")

# Global temporary view (accessible across sessions)
df.createGlobalTempView("global_sales")
spark.sql("SELECT * FROM global_temp.global_sales")
```

### 4. What are the different ways to create DataFrames?
**Answer:** Multiple methods to create DataFrames:

```python
# From files
df = spark.read.csv("file.csv", header=True, inferSchema=True)
df = spark.read.json("file.json")
df = spark.read.parquet("file.parquet")

# From RDD
rdd = spark.sparkContext.parallelize([(1, "Alice"), (2, "Bob")])
df = spark.createDataFrame(rdd, ["id", "name"])

# From Python data
data = [("Alice", 25), ("Bob", 30)]
df = spark.createDataFrame(data, ["name", "age"])

# From SQL query
df = spark.sql("SELECT * FROM existing_table")
```

### 5. How do you handle schema in Spark SQL?
**Answer:** Schema can be inferred or explicitly defined:

```python
from pyspark.sql.types import *

# Infer schema (slower for large files)
df = spark.read.option("inferSchema", "true").csv("file.csv")

# Define explicit schema (faster)
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])
df = spark.read.schema(schema).csv("file.csv")

# View schema
df.printSchema()
df.dtypes  # List of (column_name, data_type)
```

### 6. What is the difference between DataFrame and Dataset?
**Answer:** 
- **DataFrame**: Untyped API, runtime type checking
- **Dataset**: Typed API with compile-time type safety (Scala/Java only)

```scala
// Scala - Dataset with type safety
case class Person(name: String, age: Int)
val ds: Dataset[Person] = df.as[Person]

// Python only has DataFrame (untyped)
df = spark.createDataFrame(data, schema)
```

### 7. How do you perform joins in Spark SQL?
**Answer:** Multiple join types and syntaxes:

```python
# DataFrame API
result = df1.join(df2, "common_column")
result = df1.join(df2, df1.id == df2.user_id, "left")

# SQL syntax
spark.sql("""
    SELECT a.*, b.name 
    FROM table_a a
    LEFT JOIN table_b b ON a.id = b.user_id
""")

# Join types: inner, left, right, outer, cross, semi, anti
```

### 8. What are built-in functions in Spark SQL?
**Answer:** Extensive library of built-in functions:

```python
from pyspark.sql.functions import *

# String functions
df.select(upper(col("name")), length(col("name")))

# Date functions
df.select(current_date(), date_add(col("date"), 30))

# Aggregate functions
df.groupBy("category").agg(sum("amount"), avg("price"), count("*"))

# Window functions
from pyspark.sql.window import Window
window = Window.partitionBy("department").orderBy("salary")
df.withColumn("rank", row_number().over(window))
```

### 9. How do you handle null values in Spark SQL?
**Answer:** Multiple approaches for null handling:

```python
# Check for nulls
df.filter(col("column").isNull())
df.filter(col("column").isNotNull())

# Drop nulls
df.dropna()  # Drop rows with any null
df.dropna(subset=["important_col"])  # Drop if specific column is null

# Fill nulls
df.fillna({"age": 0, "name": "Unknown"})
df.na.fill({"salary": df.agg(avg("salary")).collect()[0][0]})

# Replace with conditions
df.withColumn("clean_age", when(col("age").isNull(), 0).otherwise(col("age")))
```

### 10. What is the difference between collect() and take()?
**Answer:**
- **collect()**: Returns all rows to driver (dangerous for large datasets)
- **take(n)**: Returns first n rows to driver

```python
# Collect all (use carefully)
all_data = df.collect()

# Take first 10 rows
sample_data = df.take(10)

# Show first 20 rows (doesn't return to driver)
df.show(20)

# Count without collecting data
row_count = df.count()
```

## DataFrame Operations (21-40)

### 21. How do you perform aggregations in Spark SQL?
**Answer:** Multiple aggregation methods:

```python
# Basic aggregations
df.groupBy("category").count()
df.groupBy("category").sum("amount")
df.groupBy("category").agg({"amount": "sum", "quantity": "avg"})

# Multiple aggregations
df.groupBy("category").agg(
    sum("amount").alias("total_amount"),
    avg("price").alias("avg_price"),
    count("*").alias("count")
)

# SQL aggregations
spark.sql("""
    SELECT category, 
           SUM(amount) as total,
           AVG(price) as avg_price,
           COUNT(*) as count
    FROM sales 
    GROUP BY category
""")
```

### 22. How do you use window functions in Spark SQL?
**Answer:** Window functions perform calculations across related rows:

```python
from pyspark.sql.window import Window

# Define window
window = Window.partitionBy("department").orderBy("salary")

# Ranking functions
df.withColumn("rank", row_number().over(window))
df.withColumn("dense_rank", dense_rank().over(window))
df.withColumn("percent_rank", percent_rank().over(window))

# Aggregate functions over window
df.withColumn("running_sum", sum("salary").over(window))
df.withColumn("moving_avg", avg("salary").over(window.rowsBetween(-2, 0)))

# Lead/Lag functions
df.withColumn("next_salary", lead("salary", 1).over(window))
df.withColumn("prev_salary", lag("salary", 1).over(window))
```

### 23. How do you pivot and unpivot data?
**Answer:** Reshape data between wide and long formats:

```python
# Pivot (long to wide)
pivot_df = df.groupBy("customer_id").pivot("product_category").sum("amount")

# Unpivot (wide to long) - using stack
unpivot_df = df.select("id", 
    expr("stack(3, 'col1', col1, 'col2', col2, 'col3', col3) as (category, value)")
)

# SQL pivot
spark.sql("""
    SELECT customer_id,
           SUM(CASE WHEN category = 'Electronics' THEN amount END) as Electronics,
           SUM(CASE WHEN category = 'Clothing' THEN amount END) as Clothing
    FROM sales
    GROUP BY customer_id
""")
```

### 24. How do you work with arrays and maps in Spark SQL?
**Answer:** Complex data type operations:

```python
from pyspark.sql.functions import *

# Array operations
df.withColumn("array_size", size(col("tags")))
df.withColumn("first_tag", col("tags")[0])
df.select(explode(col("tags")).alias("tag"))

# Map operations
df.withColumn("map_keys", map_keys(col("properties")))
df.withColumn("map_values", map_values(col("properties")))
df.withColumn("property_value", col("properties")["key1"])

# Create arrays and maps
df.withColumn("new_array", array(col("col1"), col("col2")))
df.withColumn("new_map", create_map(lit("key1"), col("value1")))
```

### 25. How do you perform set operations in Spark SQL?
**Answer:** Union, intersection, and difference operations:

```python
# Union (includes duplicates)
union_df = df1.union(df2)

# Union distinct (removes duplicates)
union_distinct_df = df1.union(df2).distinct()

# Intersection
intersect_df = df1.intersect(df2)

# Difference (except)
diff_df = df1.subtract(df2)  # In df1 but not in df2

# SQL set operations
spark.sql("""
    SELECT * FROM table1
    UNION ALL
    SELECT * FROM table2
""")
```

## Performance Optimization (41-60)

### 41. How do you optimize Spark SQL queries?
**Answer:** Multiple optimization techniques:

```python
# 1. Use appropriate file formats
df.write.parquet("optimized.parquet")  # Columnar, compressed

# 2. Partition data
df.write.partitionBy("year", "month").parquet("partitioned_data")

# 3. Cache frequently used DataFrames
df.cache()
df.persist(StorageLevel.MEMORY_AND_DISK)

# 4. Broadcast small tables
from pyspark.sql.functions import broadcast
result = large_df.join(broadcast(small_df), "key")

# 5. Use column pruning
df.select("needed_columns").filter(condition)

# 6. Enable adaptive query execution
spark.conf.set("spark.sql.adaptive.enabled", "true")
```

### 42. What is predicate pushdown and how does it work?
**Answer:** Optimization that pushes filter conditions down to data source:

```python
# Spark automatically pushes filters to data source
df = spark.read.parquet("large_dataset.parquet")
filtered_df = df.filter(col("date") >= "2023-01-01")

# This filter is pushed to Parquet reader, reducing I/O
# Only relevant data is read from storage

# Manual optimization - filter early
df.filter(col("partition_column") == "value").select("needed_columns")
```

### 43. How do you handle data skew in Spark SQL?
**Answer:** Techniques to handle uneven data distribution:

```python
# 1. Salting for skewed joins
from pyspark.sql.functions import rand, concat, lit

# Add random salt to skewed keys
df_salted = df.withColumn("salted_key", 
    concat(col("skewed_key"), lit("_"), (rand() * 100).cast("int"))
)

# 2. Broadcast join for small skewed dimension
broadcast_join = large_df.join(broadcast(small_skewed_df), "key")

# 3. Separate processing for skewed keys
skewed_data = df.filter(col("key").isin(skewed_keys))
normal_data = df.filter(~col("key").isin(skewed_keys))

# 4. Increase parallelism
spark.conf.set("spark.sql.shuffle.partitions", "400")
```

### 44. What is bucketing and when should you use it?
**Answer:** Pre-partitioning data by hash of column values:

```python
# Write bucketed table
df.write \
  .bucketBy(10, "customer_id") \
  .sortBy("order_date") \
  .saveAsTable("bucketed_orders")

# Benefits:
# - Avoids shuffle for joins on bucketed columns
# - Efficient sampling
# - Better performance for aggregations

# Use when:
# - Frequent joins on same columns
# - Large tables that are joined repeatedly
# - Need consistent partitioning across tables
```

### 45. How do you monitor and debug Spark SQL performance?
**Answer:** Multiple monitoring approaches:

```python
# 1. Explain plans
df.explain()  # Physical plan
df.explain(True)  # All plans (logical, optimized, physical)

# 2. Query execution time
import time
start_time = time.time()
result = df.count()
execution_time = time.time() - start_time

# 3. Spark UI analysis
# - Jobs tab: Overall job progress
# - Stages tab: Task-level details
# - Storage tab: Cached data
# - SQL tab: Query plans and metrics

# 4. Enable query execution metrics
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
```

## Advanced Features (61-80)

### 61. How do you work with nested data structures?
**Answer:** Handle JSON and complex nested data:

```python
# Read nested JSON
df = spark.read.json("nested_data.json")

# Access nested fields
df.select("user.name", "user.address.city")

# Flatten nested structures
df.select(
    col("id"),
    col("user.name").alias("user_name"),
    col("user.address.city").alias("city")
)

# Work with arrays of structs
df.select(explode(col("orders")).alias("order"))
df.select("customer_id", "orders.order_id", "orders.amount")
```

### 62. How do you implement custom aggregations?
**Answer:** Create user-defined aggregate functions:

```python
from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import DoubleType
import pandas as pd

# Pandas UDF for custom aggregation
@pandas_udf(returnType=DoubleType())
def weighted_average(values, weights):
    return (values * weights).sum() / weights.sum()

# Use in aggregation
result = df.groupBy("category").agg(
    weighted_average(col("price"), col("quantity")).alias("weighted_avg_price")
)
```

### 63. How do you handle streaming data with Spark SQL?
**Answer:** Structured Streaming with SQL interface:

```python
# Read streaming data
stream_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "topic") \
    .load()

# Process with SQL
stream_df.createOrReplaceTempView("stream_data")
result = spark.sql("""
    SELECT window(timestamp, '1 minute') as window,
           count(*) as count
    FROM stream_data
    GROUP BY window(timestamp, '1 minute')
""")

# Write stream
query = result.writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()
```

### 64. How do you work with Delta Lake in Spark SQL?
**Answer:** ACID transactions and versioning:

```python
# Write Delta table
df.write.format("delta").save("delta-table")

# Read Delta table
delta_df = spark.read.format("delta").load("delta-table")

# SQL operations on Delta
spark.sql("CREATE TABLE delta_table USING DELTA LOCATION 'delta-table'")

# Time travel
spark.sql("SELECT * FROM delta_table VERSION AS OF 1")
spark.sql("SELECT * FROM delta_table TIMESTAMP AS OF '2023-01-01'")

# Merge operations
spark.sql("""
    MERGE INTO target_table t
    USING source_table s ON t.id = s.id
    WHEN MATCHED THEN UPDATE SET *
    WHEN NOT MATCHED THEN INSERT *
""")
```

### 65. How do you optimize joins in Spark SQL?
**Answer:** Various join optimization strategies:

```python
# 1. Broadcast Hash Join (small table < 10MB)
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "10MB")
result = large_df.join(broadcast(small_df), "key")

# 2. Sort Merge Join (large tables)
# Automatically chosen for equi-joins on large tables

# 3. Bucket Join (pre-partitioned tables)
df1.write.bucketBy(10, "join_key").saveAsTable("table1")
df2.write.bucketBy(10, "join_key").saveAsTable("table2")

# 4. Join hints in SQL
spark.sql("""
    SELECT /*+ BROADCAST(small_table) */ *
    FROM large_table l
    JOIN small_table s ON l.id = s.id
""")
```

## Integration & Deployment (81-100)

### 81. How do you connect Spark SQL to external databases?
**Answer:** JDBC connectivity for various databases:

```python
# Read from database
df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/mydb") \
    .option("dbtable", "employees") \
    .option("user", "username") \
    .option("password", "password") \
    .load()

# Write to database
df.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/mydb") \
    .option("dbtable", "results") \
    .option("user", "username") \
    .option("password", "password") \
    .mode("overwrite") \
    .save()

# Partition reads for large tables
df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/mydb") \
    .option("dbtable", "large_table") \
    .option("partitionColumn", "id") \
    .option("lowerBound", "1") \
    .option("upperBound", "1000000") \
    .option("numPartitions", "10") \
    .load()
```

### 82. How do you work with Hive in Spark SQL?
**Answer:** Integration with Hive metastore and tables:

```python
# Enable Hive support
spark = SparkSession.builder \
    .appName("HiveIntegration") \
    .enableHiveSupport() \
    .getOrCreate()

# Access Hive tables
df = spark.sql("SELECT * FROM hive_database.hive_table")

# Create Hive table
spark.sql("""
    CREATE TABLE hive_table (
        id INT,
        name STRING,
        age INT
    ) USING HIVE
    PARTITIONED BY (year INT)
""")

# Insert into Hive table
df.write.mode("append").insertInto("hive_database.hive_table")
```

### 83. How do you handle schema evolution?
**Answer:** Managing changing data schemas:

```python
# Schema merging for Parquet
df = spark.read.option("mergeSchema", "true").parquet("evolving_data")

# Handle missing columns
from pyspark.sql.functions import lit
df_with_defaults = df.select(
    "*",
    lit(None).cast("string").alias("new_column") if "new_column" not in df.columns else col("new_column")
)

# Delta Lake automatic schema evolution
df.write.format("delta").option("mergeSchema", "true").mode("append").save("delta-table")
```

### 84. How do you implement data quality checks?
**Answer:** Validation and quality assurance:

```python
# Data quality checks
def data_quality_check(df):
    total_rows = df.count()
    
    # Null checks
    null_counts = df.select([
        sum(col(c).isNull().cast("int")).alias(f"{c}_nulls") 
        for c in df.columns
    ]).collect()[0].asDict()
    
    # Duplicate checks
    duplicate_count = df.count() - df.distinct().count()
    
    # Range checks
    invalid_ages = df.filter((col("age") < 0) | (col("age") > 150)).count()
    
    return {
        "total_rows": total_rows,
        "null_counts": null_counts,
        "duplicates": duplicate_count,
        "invalid_ages": invalid_ages
    }

# Apply checks
quality_report = data_quality_check(df)
```

### 85. How do you deploy Spark SQL applications?
**Answer:** Various deployment modes and configurations:

```python
# Submit Spark application
# spark-submit --master yarn --deploy-mode cluster app.py

# Configuration for production
spark = SparkSession.builder \
    .appName("ProductionApp") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
    .getOrCreate()

# Resource allocation
# --executor-memory 4g
# --executor-cores 4
# --num-executors 10
# --driver-memory 2g
```

### 86. How do you handle security in Spark SQL?
**Answer:** Authentication, authorization, and encryption:

```python
# Kerberos authentication
spark = SparkSession.builder \
    .config("spark.security.credentials.hive.enabled", "true") \
    .config("spark.sql.hive.metastore.jars", "builtin") \
    .getOrCreate()

# Column-level security
spark.sql("""
    CREATE VIEW secure_view AS
    SELECT id, name,
           CASE WHEN current_user() = 'admin' THEN salary ELSE NULL END as salary
    FROM employees
""")

# Row-level security
spark.sql("""
    CREATE VIEW user_data AS
    SELECT * FROM all_data
    WHERE user_id = current_user()
""")
```

### 87. How do you test Spark SQL applications?
**Answer:** Unit testing and integration testing:

```python
import pytest
from pyspark.sql import SparkSession

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder \
        .appName("test") \
        .master("local[2]") \
        .getOrCreate()

def test_data_transformation(spark):
    # Create test data
    test_data = [(1, "Alice", 100), (2, "Bob", 200)]
    df = spark.createDataFrame(test_data, ["id", "name", "amount"])
    
    # Apply transformation
    result = df.filter(col("amount") > 150)
    
    # Assert results
    assert result.count() == 1
    assert result.collect()[0]["name"] == "Bob"

def test_sql_query(spark):
    df = spark.createDataFrame([(1, 100), (2, 200)], ["id", "amount"])
    df.createOrReplaceTempView("test_table")
    
    result = spark.sql("SELECT SUM(amount) as total FROM test_table")
    assert result.collect()[0]["total"] == 300
```

### 88. How do you handle configuration management?
**Answer:** Externalize and manage configurations:

```python
import configparser

# Configuration file (config.ini)
config = configparser.ConfigParser()
config.read('config.ini')

# Spark configuration from file
spark = SparkSession.builder \
    .appName(config['app']['name']) \
    .config("spark.sql.shuffle.partitions", config['spark']['shuffle_partitions']) \
    .config("spark.executor.memory", config['spark']['executor_memory']) \
    .getOrCreate()

# Environment-specific configs
import os
env = os.getenv('ENVIRONMENT', 'dev')
database_url = config[f'database_{env}']['url']
```

### 89. How do you implement incremental data processing?
**Answer:** Process only new or changed data:

```python
# Watermark-based incremental processing
def incremental_process(spark, last_processed_timestamp):
    # Read new data
    new_data = spark.read.parquet("input_data") \
        .filter(col("timestamp") > last_processed_timestamp)
    
    # Process new data
    processed = new_data.groupBy("category").agg(sum("amount"))
    
    # Merge with existing results
    existing = spark.read.parquet("results")
    
    # Upsert logic
    result = existing.union(processed) \
        .groupBy("category") \
        .agg(sum("sum(amount)").alias("total_amount"))
    
    # Save results
    result.write.mode("overwrite").parquet("results")
    
    return new_data.agg(max("timestamp")).collect()[0][0]

# Delta Lake merge for incremental updates
spark.sql("""
    MERGE INTO target t
    USING source s ON t.id = s.id
    WHEN MATCHED THEN UPDATE SET *
    WHEN NOT MATCHED THEN INSERT *
""")
```

### 90. How do you optimize memory usage in Spark SQL?
**Answer:** Memory management and optimization:

```python
# 1. Appropriate storage levels
df.persist(StorageLevel.MEMORY_AND_DISK_SER)  # Serialized storage

# 2. Unpersist unused DataFrames
df.unpersist()

# 3. Optimize data types
df = df.select(
    col("id").cast("int"),  # Use smaller types
    col("amount").cast("decimal(10,2)")
)

# 4. Column pruning
df.select("needed_columns").filter(condition)

# 5. Memory configuration
spark.conf.set("spark.executor.memory", "4g")
spark.conf.set("spark.executor.memoryFraction", "0.8")
spark.conf.set("spark.sql.execution.arrow.maxRecordsPerBatch", "1000")
```

### 91. How do you handle time zones in Spark SQL?
**Answer:** Time zone handling and conversions:

```python
from pyspark.sql.functions import *

# Set session timezone
spark.conf.set("spark.sql.session.timeZone", "UTC")

# Convert between timezones
df.withColumn("utc_time", to_utc_timestamp(col("local_time"), "PST"))
df.withColumn("local_time", from_utc_timestamp(col("utc_time"), "EST"))

# SQL timezone functions
spark.sql("""
    SELECT 
        timestamp_col,
        to_utc_timestamp(timestamp_col, 'PST') as utc_time,
        from_utc_timestamp(timestamp_col, 'EST') as est_time
    FROM events
""")
```

### 92. How do you work with machine learning in Spark SQL?
**Answer:** Integration with MLlib and ML pipelines:

```python
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression

# Prepare features using SQL
features_df = spark.sql("""
    SELECT 
        feature1, feature2, feature3,
        target
    FROM training_data
    WHERE target IS NOT NULL
""")

# Create feature vector
assembler = VectorAssembler(
    inputCols=["feature1", "feature2", "feature3"],
    outputCol="features"
)
ml_df = assembler.transform(features_df)

# Train model
lr = LinearRegression(featuresCol="features", labelCol="target")
model = lr.fit(ml_df)

# Apply model using SQL
model.transform(ml_df).createOrReplaceTempView("predictions")
spark.sql("SELECT *, prediction - target as error FROM predictions")
```

### 93. How do you implement data lineage tracking?
**Answer:** Track data flow and transformations:

```python
# Custom lineage tracking
class LineageTracker:
    def __init__(self):
        self.lineage = []
    
    def track_transformation(self, source, target, operation):
        self.lineage.append({
            "source": source,
            "target": target,
            "operation": operation,
            "timestamp": datetime.now()
        })
    
    def get_lineage(self, table):
        return [l for l in self.lineage if l["target"] == table]

# Usage
tracker = LineageTracker()
tracker.track_transformation("raw_data", "cleaned_data", "data_cleaning")
tracker.track_transformation("cleaned_data", "aggregated_data", "aggregation")

# Delta Lake automatic lineage
spark.sql("DESCRIBE HISTORY delta_table")
```

### 94. How do you handle large result sets?
**Answer:** Manage memory and performance for large outputs:

```python
# 1. Use iterators instead of collect()
def process_large_result(df):
    for row in df.toLocalIterator():
        process_row(row)

# 2. Write to storage instead of collecting
df.write.mode("overwrite").parquet("large_results")

# 3. Use sampling for analysis
sample_df = df.sample(0.1, seed=42)
sample_df.show()

# 4. Partition output
df.write.partitionBy("date").parquet("partitioned_output")

# 5. Use coalesce to control file count
df.coalesce(10).write.parquet("output")
```

### 95. How do you implement custom data sources?
**Answer:** Create custom data source connectors:

```python
# Custom data source (simplified example)
class CustomDataSource:
    def __init__(self, spark, path):
        self.spark = spark
        self.path = path
    
    def read(self):
        # Custom read logic
        data = self.custom_read_logic(self.path)
        return self.spark.createDataFrame(data)
    
    def write(self, df, mode="overwrite"):
        # Custom write logic
        data = df.collect()
        self.custom_write_logic(data, self.path, mode)

# Usage
custom_source = CustomDataSource(spark, "custom://path")
df = custom_source.read()
```

### 96. How do you optimize for cloud storage?
**Answer:** Cloud-specific optimizations:

```python
# S3 optimizations
spark.conf.set("spark.hadoop.fs.s3a.multipart.size", "104857600")  # 100MB
spark.conf.set("spark.hadoop.fs.s3a.fast.upload", "true")
spark.conf.set("spark.hadoop.fs.s3a.block.size", "134217728")  # 128MB

# Azure optimizations
spark.conf.set("spark.hadoop.fs.azure.account.key.account.dfs.core.windows.net", "key")

# GCS optimizations
spark.conf.set("spark.hadoop.google.cloud.auth.service.account.enable", "true")

# Partition pruning for cloud storage
df.write.partitionBy("year", "month", "day").parquet("s3a://bucket/data")
```

### 97. How do you handle data governance?
**Answer:** Implement data governance policies:

```python
# Data classification
def classify_data(df):
    sensitive_columns = ["ssn", "credit_card", "email"]
    
    for col_name in df.columns:
        if col_name in sensitive_columns:
            df = df.withColumn(col_name, 
                when(current_user() == "admin", col(col_name))
                .otherwise(lit("***REDACTED***"))
            )
    return df

# Data retention policy
def apply_retention_policy(df, retention_days=365):
    cutoff_date = date_sub(current_date(), retention_days)
    return df.filter(col("created_date") >= cutoff_date)

# Audit logging
def log_data_access(table_name, user, operation):
    audit_log = spark.createDataFrame([
        (table_name, user, operation, current_timestamp())
    ], ["table", "user", "operation", "timestamp"])
    
    audit_log.write.mode("append").parquet("audit_logs")
```

### 98. How do you implement disaster recovery?
**Answer:** Backup and recovery strategies:

```python
# Automated backups
def backup_table(table_name, backup_location):
    df = spark.table(table_name)
    backup_path = f"{backup_location}/{table_name}/{datetime.now().strftime('%Y%m%d')}"
    df.write.mode("overwrite").parquet(backup_path)
    
    # Keep only last 30 days of backups
    cleanup_old_backups(backup_location, table_name, 30)

# Cross-region replication
def replicate_data(source_path, target_path):
    df = spark.read.parquet(source_path)
    df.write.mode("overwrite").parquet(target_path)

# Recovery verification
def verify_recovery(original_path, recovered_path):
    original = spark.read.parquet(original_path)
    recovered = spark.read.parquet(recovered_path)
    
    assert original.count() == recovered.count()
    assert original.subtract(recovered).count() == 0
```

### 99. How do you handle multi-tenancy?
**Answer:** Isolate data and resources for multiple tenants:

```python
# Tenant-based data isolation
def get_tenant_data(tenant_id):
    return spark.sql(f"""
        SELECT * FROM multi_tenant_table 
        WHERE tenant_id = '{tenant_id}'
    """)

# Row-level security
spark.sql("""
    CREATE VIEW tenant_view AS
    SELECT * FROM all_data
    WHERE tenant_id = current_user()
""")

# Resource isolation
def create_tenant_session(tenant_id):
    return SparkSession.builder \
        .appName(f"tenant_{tenant_id}") \
        .config("spark.sql.warehouse.dir", f"/warehouse/tenant_{tenant_id}") \
        .config("spark.executor.instances", "2") \
        .getOrCreate()
```

### 100. How do you implement real-time analytics?
**Answer:** Combine batch and streaming for real-time insights:

```python
# Lambda architecture implementation
def lambda_architecture():
    # Batch layer - historical data
    batch_df = spark.read.parquet("historical_data")
    batch_results = batch_df.groupBy("category").agg(sum("amount"))
    
    # Speed layer - real-time data
    stream_df = spark.readStream.format("kafka").load()
    stream_results = stream_df.groupBy("category").agg(sum("amount"))
    
    # Serving layer - combine results
    def merge_results(batch_df, stream_df):
        return batch_df.union(stream_df) \
            .groupBy("category") \
            .agg(sum("sum(amount)").alias("total"))
    
    # Write real-time results
    query = stream_results.writeStream \
        .foreachBatch(lambda df, epoch: merge_and_save(df, batch_results)) \
        .start()
    
    return query

# Kappa architecture - streaming only
def kappa_architecture():
    stream_df = spark.readStream.format("kafka").load()
    
    # Windowed aggregations
    windowed_results = stream_df \
        .withWatermark("timestamp", "10 minutes") \
        .groupBy(
            window(col("timestamp"), "1 minute"),
            col("category")
        ).agg(sum("amount"))
    
    # Write to serving layer
    query = windowed_results.writeStream \
        .outputMode("update") \
        .format("delta") \
        .option("checkpointLocation", "checkpoints") \
        .start("real_time_results")
    
    return query
```

---

## 🎯 Summary

This comprehensive guide covers 100 essential Spark SQL interview questions across:

- **Basic Concepts**: DataFrames, Catalyst optimizer, temporary views
- **DataFrame Operations**: Joins, aggregations, window functions
- **Performance Optimization**: Caching, broadcasting, predicate pushdown
- **Advanced Features**: Nested data, streaming, Delta Lake
- **Integration & Deployment**: JDBC, Hive, security, testing

Each question includes practical code examples and real-world scenarios to help you master Spark SQL for data engineering interviews and production environments.