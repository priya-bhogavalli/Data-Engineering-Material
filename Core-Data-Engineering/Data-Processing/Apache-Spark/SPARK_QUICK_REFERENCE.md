# Spark Quick Reference for Data Engineering

## 📋 Table of Contents

1. [Essential Operations](#-essential-operations)
2. [DataFrame API](#-dataframe-api)
3. [Spark SQL](#-spark-sql)
4. [RDD Operations](#-rdd-operations)
5. [Configuration Settings](#-configuration-settings)
6. [Performance Tuning](#-performance-tuning)
7. [Common Patterns](#-common-patterns)
8. [Troubleshooting](#-troubleshooting)

---

## ⚡ Essential Operations

### SparkSession Creation
```python
from pyspark.sql import SparkSession

# Basic session
spark = SparkSession.builder \
    .appName("DataEngineering") \
    .getOrCreate()

# Optimized session
spark = SparkSession.builder \
    .appName("OptimizedApp") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.cores", "4") \
    .getOrCreate()
```

### Reading Data
```python
# CSV
df = spark.read.option("header", "true").csv("path/to/file.csv")

# JSON
df = spark.read.json("path/to/file.json")

# Parquet (recommended)
df = spark.read.parquet("path/to/file.parquet")

# Database
df = spark.read.format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/db") \
    .option("dbtable", "table_name") \
    .option("user", "username") \
    .option("password", "password") \
    .load()
```

### Writing Data
```python
# Parquet (best performance)
df.write.mode("overwrite").parquet("output/path")

# CSV
df.write.mode("overwrite").option("header", "true").csv("output/path")

# Partitioned write
df.write.partitionBy("year", "month").parquet("output/path")

# Database
df.write.format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/db") \
    .option("dbtable", "output_table") \
    .mode("overwrite") \
    .save()
```

## 📊 DataFrame API

### Basic Operations
```python
from pyspark.sql.functions import *

# Select columns
df.select("col1", "col2")
df.select(col("col1"), col("col2").alias("renamed"))

# Filter rows
df.filter(col("age") > 25)
df.where((col("status") == "active") & (col("amount") > 100))

# Add/modify columns
df.withColumn("new_col", col("existing_col") * 2)
df.withColumnRenamed("old_name", "new_name")

# Drop columns
df.drop("unwanted_col")
df.drop("col1", "col2")
```

### Aggregations
```python
# Group by aggregations
df.groupBy("category").agg(
    sum("amount").alias("total"),
    avg("price").alias("avg_price"),
    count("*").alias("count")
)

# Window functions
from pyspark.sql.window import Window

window = Window.partitionBy("department").orderBy("salary")
df.withColumn("rank", row_number().over(window))

# Global aggregations
df.agg(
    sum("amount").alias("total_amount"),
    max("date").alias("latest_date")
)
```

### Joins
```python
# Inner join
df1.join(df2, "common_column")
df1.join(df2, df1.id == df2.user_id)

# Left join
df1.join(df2, "key", "left")

# Broadcast join (for small tables)
df1.join(broadcast(df2), "key")
```

## 🗄️ Spark SQL

### Basic Queries
```sql
-- Register DataFrame as view
df.createOrReplaceTempView("sales")

-- Simple select
SELECT product, SUM(amount) as total
FROM sales
WHERE date >= '2024-01-01'
GROUP BY product
ORDER BY total DESC

-- Window functions
SELECT 
    employee,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as rank
FROM employees

-- Complex aggregations
SELECT 
    department,
    COUNT(*) as emp_count,
    AVG(salary) as avg_salary,
    PERCENTILE_APPROX(salary, 0.5) as median_salary
FROM employees
GROUP BY department
```

### Advanced SQL
```sql
-- CTEs
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', date) as month,
        SUM(amount) as total
    FROM sales
    GROUP BY DATE_TRUNC('month', date)
)
SELECT * FROM monthly_sales WHERE total > 10000

-- Pivot
SELECT * FROM (
    SELECT category, month, amount FROM sales
) PIVOT (
    SUM(amount) FOR month IN ('Jan', 'Feb', 'Mar')
)
```

## 🔄 RDD Operations

### Creating RDDs
```python
# From collection
rdd = spark.sparkContext.parallelize([1, 2, 3, 4, 5])

# From file
rdd = spark.sparkContext.textFile("path/to/file.txt")

# From DataFrame
rdd = df.rdd
```

### Transformations
```python
# Map
rdd.map(lambda x: x * 2)

# Filter
rdd.filter(lambda x: x > 10)

# FlatMap
rdd.flatMap(lambda x: x.split(" "))

# ReduceByKey
key_value_rdd.reduceByKey(lambda a, b: a + b)

# GroupByKey (avoid if possible, use reduceByKey)
key_value_rdd.groupByKey()
```

### Actions
```python
# Collect (brings all data to driver)
result = rdd.collect()

# Take first n elements
first_10 = rdd.take(10)

# Count
count = rdd.count()

# Reduce
total = rdd.reduce(lambda a, b: a + b)

# Save to file
rdd.saveAsTextFile("output/path")
```

## ⚙️ Configuration Settings

### Memory Configuration
```python
spark.conf.set("spark.executor.memory", "4g")
spark.conf.set("spark.driver.memory", "2g")
spark.conf.set("spark.executor.memoryFraction", "0.8")
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
```

### Performance Settings
```python
# Adaptive Query Execution
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")

# Broadcast threshold
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "100MB")

# Shuffle partitions
spark.conf.set("spark.sql.shuffle.partitions", "200")
```

### Serialization
```python
spark.conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
```

## 🚀 Performance Tuning

### Caching
```python
# Cache in memory
df.cache()

# Persist with storage level
from pyspark import StorageLevel
df.persist(StorageLevel.MEMORY_AND_DISK)

# Unpersist when done
df.unpersist()
```

### Partitioning
```python
# Repartition (full shuffle)
df.repartition(10)
df.repartition("column_name")

# Coalesce (reduce partitions)
df.coalesce(5)

# Check partitions
df.rdd.getNumPartitions()
```

### Broadcast Variables
```python
# Broadcast small lookup tables
lookup_dict = {"A": 1, "B": 2, "C": 3}
broadcast_lookup = spark.sparkContext.broadcast(lookup_dict)

# Use in transformations
def enrich_data(value):
    return broadcast_lookup.value.get(value, 0)

df.withColumn("enriched", udf(enrich_data)("column"))
```

## 🎯 Common Patterns

### ETL Pipeline
```python
def etl_pipeline(input_path, output_path):
    # Extract
    df = spark.read.parquet(input_path)
    
    # Transform
    cleaned_df = df.filter(col("amount") > 0) \
                   .withColumn("processed_date", current_date()) \
                   .dropDuplicates()
    
    # Load
    cleaned_df.write.mode("overwrite").parquet(output_path)
    
    return cleaned_df.count()
```

### Data Quality Checks
```python
def data_quality_checks(df):
    checks = {}
    
    # Null checks
    checks["null_counts"] = {col: df.filter(col(col).isNull()).count() 
                            for col in df.columns}
    
    # Duplicate check
    checks["duplicates"] = df.count() - df.dropDuplicates().count()
    
    # Range checks
    checks["negative_amounts"] = df.filter(col("amount") < 0).count()
    
    return checks
```

### Incremental Processing
```python
def incremental_load(source_path, target_path, watermark_col):
    # Read existing data to get max watermark
    try:
        existing_df = spark.read.parquet(target_path)
        max_watermark = existing_df.agg(max(watermark_col)).collect()[0][0]
    except:
        max_watermark = "1900-01-01"
    
    # Read new data
    new_df = spark.read.parquet(source_path) \
                  .filter(col(watermark_col) > max_watermark)
    
    # Append new data
    new_df.write.mode("append").parquet(target_path)
    
    return new_df.count()
```

## 🔧 Troubleshooting

### Common Issues
```python
# OutOfMemoryError
# Solution: Increase executor memory or reduce data per partition
spark.conf.set("spark.executor.memory", "8g")
df.repartition(100)  # More partitions = less data per partition

# Slow joins
# Solution: Use broadcast joins for small tables
df1.join(broadcast(df2), "key")

# Data skew
# Solution: Salt the keys
df.withColumn("salted_key", concat(col("key"), lit("_"), 
                                  (rand() * 10).cast("int")))

# Too many small files
# Solution: Coalesce before writing
df.coalesce(10).write.parquet("output")
```

### Monitoring
```python
# Check execution plan
df.explain()
df.explain(True)  # Extended plan

# Monitor job progress
spark.sparkContext.statusTracker().getActiveJobIds()

# Check cache status
spark.catalog.isCached("table_name")
```

### Memory Issues
```python
# Check current configuration
spark.sparkContext.getConf().getAll()

# Monitor memory usage
for executor in spark.sparkContext.statusTracker().getExecutorInfos():
    print(f"Executor {executor.executorId}: {executor.memoryUsed}/{executor.maxMemory}")
```

## 🔗 Quick Links

- **[Spark Key Concepts](./SPARK_KEY_CONCEPTS.md)** - Complete fundamentals
- **[Spark Advanced Big Data Processing](./SPARK_ADVANCED_BIG_DATA_PROCESSING.md)** - Production patterns
- **[Spark Interview Questions](./SPARK_INTERVIEW_QUESTIONS_COMPLETE.md)** - Interview preparation

This quick reference covers the most commonly used Spark operations for daily data engineering tasks.