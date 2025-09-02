# Apache Spark Complete Guide for Data Engineers

## 🎯 **Overview**
Apache Spark is a unified analytics engine for large-scale data processing that has revolutionized big data processing. This comprehensive guide covers everything from basic concepts to advanced production patterns.

**What You'll Learn:**
- Core Spark architecture and components
- RDDs, DataFrames, and Datasets
- Performance optimization techniques
- Streaming and real-time processing
- Machine learning pipelines
- Production deployment and monitoring
- Best practices and troubleshooting

**Target Audience:**
- Data Engineers (1-10+ years experience)
- Big Data Developers
- Data Scientists working with large datasets
- DevOps Engineers managing Spark clusters

## 📋 Table of Contents

1. [Core Architecture](#1-core-architecture)
2. [Data Structures](#2-data-structures)
3. [Transformations and Actions](#3-transformations-and-actions)
4. [Performance Optimization](#4-performance-optimization)
5. [Spark SQL and DataFrames](#5-spark-sql-and-dataframes)
6. [Streaming Processing](#6-streaming-processing)
7. [Machine Learning](#7-machine-learning)
8. [Production Deployment](#8-production-deployment)
9. [Monitoring and Debugging](#9-monitoring-and-debugging)
10. [Best Practices](#10-best-practices)

---

## 1. Core Architecture

### Spark Components
**Driver Program**: Coordinates the application and manages the SparkContext
**Cluster Manager**: Manages resources (YARN, Mesos, Kubernetes, Standalone)
**Executors**: Run tasks and store data across cluster nodes
**Tasks**: Units of work sent to executors

```python
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf

# Create SparkSession (recommended for Spark 2.0+)
spark = SparkSession.builder \
    .appName("DataProcessingApp") \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.cores", "4") \
    .getOrCreate()

# Access SparkContext
sc = spark.sparkContext

# Basic configuration
conf = SparkConf() \
    .setAppName("MyApp") \
    .setMaster("local[*]") \
    .set("spark.executor.memory", "2g")
```

### Cluster Managers
```bash
# Standalone cluster
spark-submit --master spark://master:7077 app.py

# YARN cluster
spark-submit --master yarn --deploy-mode cluster app.py

# Kubernetes
spark-submit --master k8s://https://kubernetes-api app.py

# Local mode (development)
spark-submit --master local[*] app.py
```

---

## 2. Data Structures

### RDD (Resilient Distributed Dataset)
**The fundamental data structure - immutable, distributed, fault-tolerant**

```python
# Creating RDDs
rdd = sc.parallelize([1, 2, 3, 4, 5])
text_rdd = sc.textFile("hdfs://data/logs.txt")

# RDD operations
filtered_rdd = rdd.filter(lambda x: x > 2)
mapped_rdd = rdd.map(lambda x: x * 2)
reduced_result = rdd.reduce(lambda a, b: a + b)

# Key-value RDDs
pairs_rdd = rdd.map(lambda x: (x, x * x))
grouped_rdd = pairs_rdd.groupByKey()
reduced_by_key = pairs_rdd.reduceByKey(lambda a, b: a + b)
```

### DataFrames and Datasets
**Structured data with schema and optimization**

```python
# Creating DataFrames
df = spark.read.csv("data.csv", header=True, inferSchema=True)
df = spark.read.json("data.json")
df = spark.read.parquet("data.parquet")

# From RDD
rdd_df = spark.createDataFrame(rdd, schema)

# DataFrame operations
filtered_df = df.filter(df.age > 25)
selected_df = df.select("name", "age")
grouped_df = df.groupBy("department").count()

# SQL interface
df.createOrReplaceTempView("employees")
result = spark.sql("SELECT * FROM employees WHERE age > 25")
```

### Schema Definition
```python
from pyspark.sql.types import *

# Explicit schema
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("salary", DecimalType(10,2), True)
])

df = spark.read.schema(schema).csv("data.csv")
```

---

## 3. Transformations and Actions

### Lazy Evaluation
**Transformations are lazy - only executed when an action is called**

```python
# Transformations (lazy)
df1 = df.filter(df.age > 25)  # Not executed
df2 = df1.select("name", "salary")  # Not executed
df3 = df2.groupBy("department").avg("salary")  # Not executed

# Actions (trigger execution)
df3.show()  # Executes entire pipeline
df3.collect()  # Brings all data to driver
df3.count()  # Returns count
df3.write.parquet("output")  # Saves to storage
```

### Common Transformations
```python
# Filter and select
df.filter(col("age") > 25)
df.select("name", "age", (col("salary") * 1.1).alias("new_salary"))

# Joins
df1.join(df2, df1.id == df2.user_id, "inner")
df1.join(broadcast(small_df), "key")  # Broadcast join

# Aggregations
df.groupBy("department").agg(
    avg("salary").alias("avg_salary"),
    max("salary").alias("max_salary"),
    count("*").alias("employee_count")
)

# Window functions
from pyspark.sql.window import Window
window_spec = Window.partitionBy("department").orderBy(desc("salary"))
df.withColumn("rank", row_number().over(window_spec))
```

---

## 4. Performance Optimization

### Caching and Persistence
```python
from pyspark import StorageLevel

# Cache frequently accessed data
df.cache()  # MEMORY_ONLY
df.persist(StorageLevel.MEMORY_AND_DISK)
df.persist(StorageLevel.MEMORY_ONLY_SER)

# Remove from cache
df.unpersist()

# Check if cached
df.is_cached
```

### Partitioning
```python
# Check partitions
print(f"Partitions: {df.rdd.getNumPartitions()}")

# Repartition (can increase or decrease)
df_repartitioned = df.repartition(10)
df_repartitioned = df.repartition("department")

# Coalesce (only decrease)
df_coalesced = df.coalesce(5)

# Custom partitioning for RDDs
key_value_rdd.partitionBy(4)
```

### Join Optimization
```python
# Broadcast joins for small tables
from pyspark.sql.functions import broadcast
large_df.join(broadcast(small_df), "key")

# Bucketing for repeated joins
df.write.bucketBy(10, "user_id").saveAsTable("users_bucketed")

# Sort-merge joins (default for large tables)
df1.join(df2, "key")  # Automatically chooses best strategy
```

### Data Skew Handling
```python
# Salting technique for skewed joins
from pyspark.sql.functions import rand, concat, lit

# Add salt to skewed keys
salted_df1 = df1.withColumn("salted_key", 
    concat(col("key"), lit("_"), (rand() * 10).cast("int")))

# Replicate smaller table
salted_df2 = df2.crossJoin(spark.range(10).select(col("id").alias("salt")))
salted_df2 = salted_df2.withColumn("salted_key", 
    concat(col("key"), lit("_"), col("salt")))

# Join on salted keys
result = salted_df1.join(salted_df2, "salted_key")
```

### Configuration Tuning
```python
# Memory configuration
spark.conf.set("spark.executor.memory", "4g")
spark.conf.set("spark.executor.cores", "4")
spark.conf.set("spark.executor.instances", "10")

# Adaptive Query Execution (Spark 3.0+)
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")

# Shuffle optimization
spark.conf.set("spark.sql.shuffle.partitions", "400")
spark.conf.set("spark.shuffle.compress", "true")
spark.conf.set("spark.shuffle.spill.compress", "true")
```

---

## 5. Spark SQL and DataFrames

### Built-in Functions
```python
from pyspark.sql.functions import *

# String functions
df.select(
    upper(col("name")).alias("upper_name"),
    length(col("name")).alias("name_length"),
    regexp_replace(col("email"), "@.*", "@company.com").alias("masked_email")
)

# Date functions
df.select(
    current_date().alias("today"),
    date_add(col("hire_date"), 30).alias("probation_end"),
    datediff(current_date(), col("hire_date")).alias("days_employed")
)

# Aggregation functions
df.groupBy("department").agg(
    avg("salary").alias("avg_salary"),
    stddev("salary").alias("salary_stddev"),
    percentile_approx("salary", 0.5).alias("median_salary")
)
```

### User Defined Functions (UDFs)
```python
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

# Python UDF
def categorize_age(age):
    if age < 18: return "Minor"
    elif age < 65: return "Adult"
    else: return "Senior"

categorize_udf = udf(categorize_age, StringType())
df.withColumn("age_category", categorize_udf(col("age")))

# Pandas UDF (vectorized, faster)
from pyspark.sql.functions import pandas_udf
import pandas as pd

@pandas_udf(returnType=StringType())
def vectorized_categorize(ages: pd.Series) -> pd.Series:
    return ages.apply(lambda age: 
        "Minor" if age < 18 else 
        "Adult" if age < 65 else 
        "Senior"
    )

df.withColumn("age_category", vectorized_categorize(col("age")))
```

---

## 6. Streaming Processing

### Structured Streaming
```python
# Read from Kafka
streaming_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "input_topic") \
    .load()

# Process streaming data
processed_df = streaming_df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

# Windowed aggregations
from pyspark.sql.functions import window

windowed_counts = processed_df \
    .withWatermark("timestamp", "10 minutes") \
    .groupBy(
        window(col("timestamp"), "5 minutes"),
        col("event_type")
    ).count()

# Write stream
query = windowed_counts.writeStream \
    .outputMode("update") \
    .format("console") \
    .trigger(processingTime="10 seconds") \
    .start()

query.awaitTermination()
```

### Stream Processing Patterns
```python
# Stateful processing
def update_state(key, values, state):
    if state.exists():
        current_count = state.get()
    else:
        current_count = 0
    
    new_count = current_count + sum(values)
    state.update(new_count)
    return new_count

stateful_stream = streaming_df.mapGroupsWithState(
    update_state,
    outputMode="update",
    timeoutConf=GroupStateTimeout.ProcessingTimeTimeout
)
```

---

## 7. Machine Learning

### ML Pipelines
```python
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler, StringIndexer, StandardScaler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator

# Feature engineering
indexers = [StringIndexer(inputCol=col, outputCol=f"{col}_indexed")
            for col in ["category", "region"]]

assembler = VectorAssembler(
    inputCols=["age", "income", "category_indexed", "region_indexed"],
    outputCol="features_raw"
)

scaler = StandardScaler(inputCol="features_raw", outputCol="features")

# Model
rf = RandomForestClassifier(featuresCol="features", labelCol="label")

# Pipeline
pipeline = Pipeline(stages=indexers + [assembler, scaler, rf])

# Train
model = pipeline.fit(train_df)

# Predict
predictions = model.transform(test_df)

# Evaluate
evaluator = BinaryClassificationEvaluator()
auc = evaluator.evaluate(predictions)
```

### Hyperparameter Tuning
```python
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

paramGrid = ParamGridBuilder() \
    .addGrid(rf.numTrees, [10, 20, 30]) \
    .addGrid(rf.maxDepth, [5, 10, 15]) \
    .build()

crossval = CrossValidator(
    estimator=pipeline,
    estimatorParamMaps=paramGrid,
    evaluator=evaluator,
    numFolds=3
)

cv_model = crossval.fit(train_df)
```

---

## 8. Production Deployment

### Cluster Configuration
```bash
# YARN deployment
spark-submit \
    --master yarn \
    --deploy-mode cluster \
    --executor-memory 4g \
    --executor-cores 4 \
    --num-executors 10 \
    --driver-memory 2g \
    --conf spark.sql.adaptive.enabled=true \
    --conf spark.sql.adaptive.coalescePartitions.enabled=true \
    my_app.py

# Kubernetes deployment
spark-submit \
    --master k8s://https://k8s-apiserver-host:port \
    --deploy-mode cluster \
    --name spark-pi \
    --conf spark.executor.instances=5 \
    --conf spark.kubernetes.container.image=my-spark:latest \
    my_app.py
```

### Dynamic Allocation
```python
# Enable dynamic allocation
spark.conf.set("spark.dynamicAllocation.enabled", "true")
spark.conf.set("spark.dynamicAllocation.minExecutors", "1")
spark.conf.set("spark.dynamicAllocation.maxExecutors", "20")
spark.conf.set("spark.dynamicAllocation.initialExecutors", "5")
```

---

## 9. Monitoring and Debugging

### Spark UI and Metrics
```python
# Access Spark UI at http://driver:4040

# Explain query plans
df.explain(True)  # All phases
df.explain("cost")  # Cost-based optimization

# Custom metrics
from pyspark.util import AccumulatorParam

class ListAccumulatorParam(AccumulatorParam):
    def zero(self, value):
        return []
    
    def addInPlace(self, list1, list2):
        return list1 + list2

error_accumulator = sc.accumulator([], ListAccumulatorParam())

def process_with_error_tracking(record):
    try:
        return process_record(record)
    except Exception as e:
        error_accumulator.add([str(e)])
        return None

rdd.map(process_with_error_tracking).collect()
print(f"Errors: {error_accumulator.value}")
```

### Performance Analysis
```python
def analyze_performance(spark_context):
    """Analyze Spark application performance"""
    status = spark_context.statusTracker()
    
    # Application metrics
    app_info = {
        "application_id": spark_context.applicationId,
        "start_time": spark_context.startTime,
        "executors": len(status.getExecutorInfos()),
        "active_stages": len(status.getActiveStages()),
        "active_jobs": len(status.getActiveJobIds())
    }
    
    # Stage metrics
    for stage in status.getActiveStages():
        stage_info = {
            "stage_id": stage.stageId,
            "num_tasks": stage.numTasks,
            "shuffle_read": stage.shuffleReadBytes,
            "shuffle_write": stage.shuffleWriteBytes
        }
        print(f"Stage {stage.stageId}: {stage_info}")
    
    return app_info
```

---

## 10. Best Practices

### Data Processing Best Practices
```python
# 1. Use appropriate file formats
df.write.parquet("output")  # Columnar format for analytics
df.write.option("compression", "snappy").parquet("output")

# 2. Partition data appropriately
df.write.partitionBy("year", "month").parquet("output")

# 3. Cache frequently accessed data
df.cache()
df.persist(StorageLevel.MEMORY_AND_DISK_SER)

# 4. Use broadcast for small lookup tables
result = large_df.join(broadcast(small_df), "key")

# 5. Avoid collect() on large datasets
# Use write operations or take(n) instead
df.write.mode("overwrite").parquet("output")
sample_data = df.take(100)

# 6. Use built-in functions over UDFs
# Built-in functions are optimized and faster
df.withColumn("upper_name", upper(col("name")))  # Good
df.withColumn("upper_name", udf_upper(col("name")))  # Avoid if possible
```

### Resource Management
```python
# Right-size executors
# Rule of thumb: 2-4 cores per executor, 2-8GB memory per executor

# Monitor garbage collection
spark.conf.set("spark.executor.extraJavaOptions", 
               "-XX:+UseG1GC -XX:MaxGCPauseMillis=200")

# Use appropriate storage levels
# MEMORY_ONLY: Fast access, high memory usage
# MEMORY_AND_DISK: Balanced approach
# MEMORY_ONLY_SER: Compact but slower deserialization
```

### Error Handling
```python
def resilient_processing(df, process_func, max_retries=3):
    """Process data with automatic retry on failure"""
    
    for attempt in range(max_retries):
        try:
            return process_func(df)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            else:
                print(f"Attempt {attempt + 1} failed, retrying...")
                time.sleep(2 ** attempt)  # Exponential backoff

# Usage
result = resilient_processing(df, lambda x: x.groupBy("key").count())
```

### Code Organization
```python
class SparkETLJob:
    def __init__(self, spark):
        self.spark = spark
    
    def extract(self, source_config):
        """Extract data from source"""
        return self.spark.read.format(source_config['format']).load(source_config['path'])
    
    def transform(self, df, transformations):
        """Apply transformations"""
        for transform in transformations:
            df = transform(df)
        return df
    
    def load(self, df, target_config):
        """Load data to target"""
        df.write.format(target_config['format']).mode(target_config['mode']).save(target_config['path'])
    
    def run(self, config):
        """Run complete ETL pipeline"""
        df = self.extract(config['source'])
        df = self.transform(df, config['transformations'])
        self.load(df, config['target'])
```

This comprehensive guide provides the foundation for building robust, scalable, and efficient Spark applications for data engineering workloads.