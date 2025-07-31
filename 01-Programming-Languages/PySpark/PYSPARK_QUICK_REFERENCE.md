# PySpark Quick Reference for Data Engineering

## SparkSession Setup

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Basic session
spark = SparkSession.builder \
    .appName("DataEngineering") \
    .getOrCreate()

# Optimized session
spark = SparkSession.builder \
    .appName("DataEngineering") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .getOrCreate()
```

## Data Reading/Writing

### Reading Data
```python
# Parquet
df = spark.read.parquet("path/to/file.parquet")

# CSV with options
df = spark.read.option("header", "true") \
    .option("inferSchema", "true") \
    .csv("path/to/file.csv")

# JSON
df = spark.read.json("path/to/file.json")

# Delta
df = spark.read.format("delta").load("path/to/delta-table")

# Database
df = spark.read.format("jdbc") \
    .option("url", "jdbc:postgresql://localhost/test") \
    .option("dbtable", "table_name") \
    .option("user", "username") \
    .option("password", "password") \
    .load()
```

### Writing Data
```python
# Parquet
df.write.mode("overwrite").parquet("output/path")

# Partitioned write
df.write.partitionBy("year", "month").parquet("output/path")

# Delta with optimization
df.write.format("delta") \
    .option("optimizeWrite", "true") \
    .mode("overwrite") \
    .save("output/path")

# Database
df.write.format("jdbc") \
    .option("url", "jdbc:postgresql://localhost/test") \
    .option("dbtable", "output_table") \
    .option("user", "username") \
    .option("password", "password") \
    .mode("append") \
    .save()
```

## DataFrame Operations

### Basic Operations
```python
# Show data
df.show(20, truncate=False)
df.printSchema()
df.count()
df.columns
df.dtypes

# Select columns
df.select("col1", "col2")
df.select(col("col1"), col("col2").alias("new_name"))

# Filter rows
df.filter(col("age") > 25)
df.where((col("age") > 25) & (col("status") == "active"))

# Add/modify columns
df.withColumn("new_col", col("old_col") * 2)
df.withColumnRenamed("old_name", "new_name")

# Drop columns/rows
df.drop("unwanted_col")
df.dropna()  # Drop rows with null values
df.dropDuplicates(["col1", "col2"])
```

### Aggregations
```python
# Basic aggregations
df.groupBy("category").count()
df.groupBy("category").agg(
    avg("amount").alias("avg_amount"),
    sum("quantity").alias("total_quantity"),
    max("date").alias("latest_date")
)

# Multiple grouping columns
df.groupBy("category", "region").sum("sales")

# Pivot operations
df.groupBy("customer").pivot("product").sum("amount")
```

### Joins
```python
# Inner join (default)
df1.join(df2, "common_column")
df1.join(df2, df1.id == df2.customer_id)

# Different join types
df1.join(df2, "key", "left")
df1.join(df2, "key", "right")
df1.join(df2, "key", "outer")
df1.join(df2, "key", "left_anti")  # Left anti join

# Broadcast join for small tables
from pyspark.sql.functions import broadcast
large_df.join(broadcast(small_df), "key")
```

## Common Functions

### String Functions
```python
from pyspark.sql.functions import *

# String operations
df.withColumn("upper_name", upper(col("name")))
df.withColumn("trimmed", trim(col("text")))
df.withColumn("length", length(col("text")))
df.withColumn("substring", substring(col("text"), 1, 5))

# Pattern matching
df.filter(col("email").rlike(r".*@gmail\.com"))
df.withColumn("clean_phone", regexp_replace(col("phone"), r"[^\d]", ""))

# String splitting
df.withColumn("name_parts", split(col("full_name"), " "))
df.withColumn("first_name", split(col("full_name"), " ")[0])
```

### Date/Time Functions
```python
# Date operations
df.withColumn("current_date", current_date())
df.withColumn("current_timestamp", current_timestamp())
df.withColumn("year", year(col("date_column")))
df.withColumn("month", month(col("date_column")))
df.withColumn("day", dayofmonth(col("date_column")))

# Date arithmetic
df.withColumn("days_ago", datediff(current_date(), col("date_column")))
df.withColumn("future_date", date_add(col("date_column"), 30))

# Date formatting
df.withColumn("formatted_date", date_format(col("timestamp"), "yyyy-MM-dd"))
```

### Conditional Logic
```python
# When/otherwise (case statements)
df.withColumn("category",
    when(col("amount") > 1000, "high")
    .when(col("amount") > 100, "medium")
    .otherwise("low")
)

# Null handling
df.withColumn("filled_col", coalesce(col("col1"), col("col2"), lit("default")))
df.withColumn("is_null", col("column").isNull())
df.withColumn("not_null", col("column").isNotNull())
```

### Array/Map Functions
```python
# Array operations
df.withColumn("array_size", size(col("array_column")))
df.withColumn("first_element", col("array_column")[0])
df.withColumn("exploded", explode(col("array_column")))

# Array aggregations
df.withColumn("array_col", collect_list(col("item")))
df.withColumn("unique_array", collect_set(col("item")))

# Map operations
df.withColumn("map_keys", map_keys(col("map_column")))
df.withColumn("map_values", map_values(col("map_column")))
```

## Window Functions

```python
from pyspark.sql.window import Window

# Define window specification
window_spec = Window.partitionBy("category").orderBy("date")

# Ranking functions
df.withColumn("row_number", row_number().over(window_spec))
df.withColumn("rank", rank().over(window_spec))
df.withColumn("dense_rank", dense_rank().over(window_spec))

# Aggregate functions over windows
df.withColumn("running_sum", sum("amount").over(window_spec))
df.withColumn("moving_avg", avg("amount").over(
    window_spec.rowsBetween(-2, 0)  # 3-row moving average
))

# Lead/Lag functions
df.withColumn("previous_value", lag("amount", 1).over(window_spec))
df.withColumn("next_value", lead("amount", 1).over(window_spec))

# First/Last values
df.withColumn("first_in_group", first("amount").over(window_spec))
df.withColumn("last_in_group", last("amount").over(window_spec))
```

## Performance Optimization

### Caching and Persistence
```python
from pyspark import StorageLevel

# Cache DataFrame
df.cache()  # Same as MEMORY_AND_DISK
df.persist(StorageLevel.MEMORY_ONLY)
df.persist(StorageLevel.DISK_ONLY)

# Unpersist when done
df.unpersist()

# Check what's cached
spark.catalog.listTables()
```

### Partitioning
```python
# Check partitions
df.rdd.getNumPartitions()

# Repartition (causes shuffle)
df_repartitioned = df.repartition(10)
df_repartitioned = df.repartition("column_name")

# Coalesce (reduces partitions, minimal shuffle)
df_coalesced = df.coalesce(5)

# Partition when writing
df.write.partitionBy("year", "month").parquet("output")
```

### Broadcast Variables and Accumulators
```python
# Broadcast variables (read-only)
broadcast_var = spark.sparkContext.broadcast({"key": "value"})
# Use: broadcast_var.value

# Accumulators (write-only from workers)
accumulator = spark.sparkContext.accumulator(0)
# Use: accumulator.add(1)
# Read: accumulator.value
```

## Data Quality and Validation

### Null Handling
```python
# Check for nulls
null_counts = df.select([
    sum(col(c).isNull().cast("int")).alias(c) 
    for c in df.columns
]).collect()[0].asDict()

# Fill nulls
df.fillna({"numeric_col": 0, "string_col": "unknown"})
df.fillna(0)  # Fill all numeric nulls with 0

# Drop nulls
df.dropna()  # Drop rows with any null
df.dropna(subset=["important_col"])  # Drop if specific column is null
df.dropna(thresh=2)  # Drop if less than 2 non-null values
```

### Data Validation
```python
# Basic statistics
df.describe().show()
df.summary("count", "mean", "stddev", "min", "25%", "75%", "max").show()

# Data profiling
def profile_column(df, column):
    return df.select(
        count(col(column)).alias("count"),
        countDistinct(col(column)).alias("distinct_count"),
        sum(col(column).isNull().cast("int")).alias("null_count"),
        min(col(column)).alias("min_value"),
        max(col(column)).alias("max_value")
    ).collect()[0]
```

## UDFs (User Defined Functions)

### Regular UDFs
```python
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType, IntegerType

# Define UDF
def categorize_age(age):
    if age < 18:
        return "minor"
    elif age < 65:
        return "adult"
    else:
        return "senior"

# Register UDF
categorize_udf = udf(categorize_age, StringType())

# Use UDF
df.withColumn("age_category", categorize_udf(col("age")))
```

### Pandas UDFs (Vectorized)
```python
from pyspark.sql.functions import pandas_udf
import pandas as pd

@pandas_udf(returnType=StringType())
def vectorized_categorize(ages: pd.Series) -> pd.Series:
    return ages.apply(lambda age: 
        "minor" if age < 18 else "adult" if age < 65 else "senior"
    )

df.withColumn("age_category", vectorized_categorize(col("age")))
```

## Streaming

### Basic Streaming
```python
# Read stream
stream_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "topic_name") \
    .load()

# Process stream
processed_stream = stream_df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

# Write stream
query = processed_stream.writeStream \
    .outputMode("append") \
    .format("console") \
    .trigger(processingTime="10 seconds") \
    .start()

query.awaitTermination()
```

### Windowed Aggregations
```python
# Time-based windows
windowed_counts = stream_df \
    .withWatermark("timestamp", "10 minutes") \
    .groupBy(
        window(col("timestamp"), "5 minutes"),
        col("category")
    ) \
    .count()
```

## Configuration Settings

### Common Spark Configurations
```python
# Memory settings
spark.conf.set("spark.executor.memory", "4g")
spark.conf.set("spark.driver.memory", "2g")
spark.conf.set("spark.executor.memoryFraction", "0.8")

# Parallelism
spark.conf.set("spark.sql.shuffle.partitions", "200")
spark.conf.set("spark.default.parallelism", "100")

# Adaptive Query Execution
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")

# Serialization
spark.conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")

# Dynamic allocation
spark.conf.set("spark.dynamicAllocation.enabled", "true")
spark.conf.set("spark.dynamicAllocation.minExecutors", "1")
spark.conf.set("spark.dynamicAllocation.maxExecutors", "20")
```

## Error Handling

### Try-Catch Patterns
```python
from pyspark.sql.utils import AnalysisException

try:
    df = spark.read.parquet("path/to/file")
    result = df.filter(col("date") > "2023-01-01").count()
except AnalysisException as e:
    print(f"Analysis error: {e}")
except Exception as e:
    print(f"General error: {e}")
finally:
    # Cleanup code
    pass
```

### Data Validation
```python
def validate_dataframe(df, required_columns):
    """Validate DataFrame structure"""
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")
    
    if df.count() == 0:
        raise ValueError("DataFrame is empty")
    
    return True
```

## Debugging and Monitoring

### Query Plans
```python
# Show execution plan
df.explain()
df.explain(True)  # Extended explanation
df.explain("cost")  # Cost-based explanation

# Show physical plan
df.queryExecution.executedPlan
```

### Monitoring
```python
# Check Spark UI
print(f"Spark UI: {spark.sparkContext.uiWebUrl}")

# Application info
print(f"Application ID: {spark.sparkContext.applicationId}")
print(f"Application Name: {spark.sparkContext.appName}")

# Executor info
executors = spark.sparkContext.statusTracker().getExecutorInfos()
for executor in executors:
    print(f"Executor {executor.executorId}: {executor.totalCores} cores")
```

## Testing

### Unit Testing Setup
```python
import pytest
from pyspark.sql import SparkSession

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder \
        .appName("test") \
        .master("local[2]") \
        .getOrCreate()

def test_transformation(spark):
    # Create test data
    test_data = [("Alice", 25), ("Bob", 30)]
    df = spark.createDataFrame(test_data, ["name", "age"])
    
    # Apply transformation
    result = df.filter(col("age") > 25)
    
    # Assert results
    assert result.count() == 1
    assert result.first().name == "Bob"
```

### Data Comparison
```python
def assert_dataframes_equal(df1, df2):
    """Compare two DataFrames"""
    assert df1.count() == df2.count()
    assert df1.columns == df2.columns
    assert df1.subtract(df2).count() == 0
    assert df2.subtract(df1).count() == 0
```