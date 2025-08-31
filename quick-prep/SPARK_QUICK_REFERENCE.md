# ⚡ Spark Quick Reference for Data Engineering

## 🏗️ **Core Architecture**
```
Spark Application
├── Driver Program (SparkContext)
├── Cluster Manager (YARN/Mesos/Standalone)
└── Executors (Worker nodes)

RDD → DataFrame → Dataset
├── RDD: Low-level, functional programming
├── DataFrame: Structured data with schema
└── Dataset: Type-safe DataFrames (Scala/Java)
```

## 🐍 **PySpark Essentials**
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count, avg

# Initialize Spark
spark = SparkSession.builder.appName("DataEngineering").getOrCreate()

# Read data
df = spark.read.csv("path/to/file.csv", header=True, inferSchema=True)
df = spark.read.parquet("path/to/file.parquet")
df = spark.read.json("path/to/file.json")

# Basic operations
df.show(10)                    # Display first 10 rows
df.printSchema()               # Show schema
df.count()                     # Count rows
df.select("col1", "col2")      # Select columns
df.filter(col("age") > 25)     # Filter rows
df.groupBy("department").agg(avg("salary"))  # Group and aggregate
```

## 🔄 **Transformations vs Actions**
```python
# Transformations (lazy evaluation)
df.select()
df.filter()
df.groupBy()
df.join()
df.withColumn()

# Actions (trigger execution)
df.show()
df.collect()
df.count()
df.write.parquet()
```

## 🔗 **Joins**
```python
# Inner join (default)
df1.join(df2, "common_column")
df1.join(df2, df1.id == df2.user_id)

# Other join types
df1.join(df2, "key", "left")      # left outer
df1.join(df2, "key", "right")     # right outer
df1.join(df2, "key", "outer")     # full outer
df1.join(df2, "key", "anti")      # anti join
```

## 📊 **Window Functions**
```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, rank, lag

window = Window.partitionBy("department").orderBy("salary")

df.withColumn("rank", rank().over(window)) \
  .withColumn("prev_salary", lag("salary").over(window))
```

## 💾 **Data Formats & Storage**
```python
# Parquet (recommended for analytics)
df.write.mode("overwrite").parquet("path/to/output")

# Delta Lake (ACID transactions)
df.write.format("delta").mode("overwrite").save("path/to/delta-table")

# Partitioning for performance
df.write.partitionBy("year", "month").parquet("path/to/partitioned")
```

## ⚡ **Performance Optimization**
```python
# Caching for reused DataFrames
df.cache()  # or df.persist()

# Broadcast small tables
from pyspark.sql.functions import broadcast
large_df.join(broadcast(small_df), "key")

# Repartition for better parallelism
df.repartition(200)  # Increase partitions
df.coalesce(10)      # Decrease partitions (no shuffle)

# Bucketing for joins
df.write.bucketBy(10, "user_id").saveAsTable("bucketed_table")
```

## 🔧 **Configuration Tuning**
```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
```

## 🚨 **Common Pitfalls**
- **Small files problem**: Use coalesce() before writing
- **Data skew**: Use salting or custom partitioning
- **Memory issues**: Increase driver/executor memory
- **Shuffle operations**: Minimize with proper partitioning
- **Collect() on large data**: Use show() or write() instead