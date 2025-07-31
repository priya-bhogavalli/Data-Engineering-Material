# Apache Spark Quick Reference for Data Engineering

## Spark Session Setup

### Scala
```scala
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

// Basic session
val spark = SparkSession.builder()
  .appName("DataEngineering")
  .master("local[*]")
  .getOrCreate()

// Optimized session
val spark = SparkSession.builder()
  .appName("DataEngineering")
  .config("spark.sql.adaptive.enabled", "true")
  .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
  .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
  .getOrCreate()
```

### Python
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder \
    .appName("DataEngineering") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()
```

## Data Reading/Writing

### Reading Data
```scala
// Parquet
val df = spark.read.parquet("path/to/file.parquet")

// CSV with schema
val df = spark.read
  .option("header", "true")
  .option("inferSchema", "true")
  .csv("path/to/file.csv")

// JSON
val df = spark.read.json("path/to/file.json")

// Delta Lake
val df = spark.read.format("delta").load("path/to/delta-table")

// JDBC
val df = spark.read
  .format("jdbc")
  .option("url", "jdbc:postgresql://localhost/test")
  .option("dbtable", "table_name")
  .option("user", "username")
  .option("password", "password")
  .load()
```

### Writing Data
```scala
// Parquet with partitioning
df.write
  .mode("overwrite")
  .partitionBy("year", "month")
  .parquet("output/path")

// Delta Lake with optimization
df.write
  .format("delta")
  .option("optimizeWrite", "true")
  .mode("overwrite")
  .save("output/path")

// JDBC
df.write
  .format("jdbc")
  .option("url", "jdbc:postgresql://localhost/test")
  .option("dbtable", "output_table")
  .mode("append")
  .save()
```

## DataFrame Operations

### Basic Operations
```scala
// Show data
df.show(20, truncate = false)
df.printSchema()
df.count()
df.columns
df.dtypes

// Select columns
df.select("col1", "col2")
df.select($"col1", $"col2".alias("new_name"))

// Filter rows
df.filter($"age" > 25)
df.where($"age" > 25 && $"status" === "active")

// Add/modify columns
df.withColumn("new_col", $"old_col" * 2)
df.withColumnRenamed("old_name", "new_name")

// Drop columns/rows
df.drop("unwanted_col")
df.dropna() // Drop rows with null values
df.dropDuplicates(Seq("col1", "col2"))
```

### Aggregations
```scala
// Basic aggregations
df.groupBy("category").count()
df.groupBy("category").agg(
  avg("amount").alias("avg_amount"),
  sum("quantity").alias("total_quantity"),
  max("date").alias("latest_date")
)

// Multiple grouping columns
df.groupBy("category", "region").sum("sales")

// Pivot operations
df.groupBy("customer").pivot("product").sum("amount")
```

### Joins
```scala
// Inner join (default)
df1.join(df2, "common_column")
df1.join(df2, $"df1.id" === $"df2.customer_id")

// Different join types
df1.join(df2, Seq("key"), "left")
df1.join(df2, Seq("key"), "right")
df1.join(df2, Seq("key"), "outer")
df1.join(df2, Seq("key"), "left_anti")

// Broadcast join
import org.apache.spark.sql.functions.broadcast
large_df.join(broadcast(small_df), "key")
```

## Common Functions

### String Functions
```scala
// String operations
df.withColumn("upper_name", upper($"name"))
df.withColumn("trimmed", trim($"text"))
df.withColumn("length", length($"text"))
df.withColumn("substring", substring($"text", 1, 5))

// Pattern matching
df.filter($"email".rlike(".*@gmail\\.com"))
df.withColumn("clean_phone", regexp_replace($"phone", "[^\\d]", ""))

// String splitting
df.withColumn("name_parts", split($"full_name", " "))
df.withColumn("first_name", split($"full_name", " ")(0))
```

### Date/Time Functions
```scala
// Date operations
df.withColumn("current_date", current_date())
df.withColumn("current_timestamp", current_timestamp())
df.withColumn("year", year($"date_column"))
df.withColumn("month", month($"date_column"))
df.withColumn("day", dayofmonth($"date_column"))

// Date arithmetic
df.withColumn("days_ago", datediff(current_date(), $"date_column"))
df.withColumn("future_date", date_add($"date_column", 30))

// Date formatting
df.withColumn("formatted_date", date_format($"timestamp", "yyyy-MM-dd"))
```

### Conditional Logic
```scala
// When/otherwise (case statements)
df.withColumn("category",
  when($"amount" > 1000, "high")
    .when($"amount" > 100, "medium")
    .otherwise("low")
)

// Null handling
df.withColumn("filled_col", coalesce($"col1", $"col2", lit("default")))
df.withColumn("is_null", $"column".isNull)
df.withColumn("not_null", $"column".isNotNull)
```

### Array/Map Functions
```scala
// Array operations
df.withColumn("array_size", size($"array_column"))
df.withColumn("first_element", $"array_column"(0))
df.withColumn("exploded", explode($"array_column"))

// Array aggregations
df.withColumn("array_col", collect_list($"item"))
df.withColumn("unique_array", collect_set($"item"))

// Map operations
df.withColumn("map_keys", map_keys($"map_column"))
df.withColumn("map_values", map_values($"map_column"))
```

## Window Functions

```scala
import org.apache.spark.sql.expressions.Window

// Define window specification
val windowSpec = Window.partitionBy("category").orderBy("date")

// Ranking functions
df.withColumn("row_number", row_number().over(windowSpec))
df.withColumn("rank", rank().over(windowSpec))
df.withColumn("dense_rank", dense_rank().over(windowSpec))

// Aggregate functions over windows
df.withColumn("running_sum", sum("amount").over(windowSpec))
df.withColumn("moving_avg", avg("amount").over(
  windowSpec.rowsBetween(-2, 0) // 3-row moving average
))

// Lead/Lag functions
df.withColumn("previous_value", lag("amount", 1).over(windowSpec))
df.withColumn("next_value", lead("amount", 1).over(windowSpec))

// First/Last values
df.withColumn("first_in_group", first("amount").over(windowSpec))
df.withColumn("last_in_group", last("amount").over(windowSpec))
```

## Performance Optimization

### Caching and Persistence
```scala
import org.apache.spark.storage.StorageLevel

// Cache DataFrame
val cachedDF = df.cache() // MEMORY_AND_DISK by default
val memoryOnlyDF = df.persist(StorageLevel.MEMORY_ONLY)
val diskOnlyDF = df.persist(StorageLevel.DISK_ONLY)

// Unpersist when done
cachedDF.unpersist()
```

### Partitioning
```scala
// Check partitions
df.rdd.getNumPartitions

// Repartition (causes shuffle)
val repartitionedDF = df.repartition(10)
val repartitionedByCol = df.repartition($"column_name")

// Coalesce (reduces partitions, minimal shuffle)
val coalescedDF = df.coalesce(5)

// Partition when writing
df.write.partitionBy("year", "month").parquet("output")
```

### Broadcast Variables and Accumulators
```scala
// Broadcast variables (read-only)
val broadcastVar = spark.sparkContext.broadcast(Map("key" -> "value"))
// Use: broadcastVar.value

// Accumulators (write-only from workers)
val accumulator = spark.sparkContext.longAccumulator("My Accumulator")
// Use: accumulator.add(1)
// Read: accumulator.value
```

## RDD Operations

### Creating RDDs
```scala
// From collection
val rdd = spark.sparkContext.parallelize(Seq(1, 2, 3, 4, 5))

// From file
val textRDD = spark.sparkContext.textFile("path/to/file.txt")

// From DataFrame
val rddFromDF = df.rdd
```

### Transformations
```scala
// Map operations
val mappedRDD = rdd.map(x => x * 2)
val flatMappedRDD = rdd.flatMap(x => x.toString.toCharArray)

// Filter operations
val filteredRDD = rdd.filter(x => x > 2)

// Key-value operations
val pairRDD = rdd.map(x => (x, x * x))
val groupedRDD = pairRDD.groupByKey()
val reducedRDD = pairRDD.reduceByKey(_ + _)

// Joins
val joinedRDD = pairRDD1.join(pairRDD2)
```

### Actions
```scala
// Collect results
val results = rdd.collect()
val firstElement = rdd.first()
val sample = rdd.take(10)

// Aggregations
val count = rdd.count()
val sum = rdd.reduce(_ + _)
val aggregated = rdd.aggregate(0)(_ + _, _ + _)

// Save to file
rdd.saveAsTextFile("output/path")
```

## Spark SQL

### Creating Views
```scala
// Register DataFrame as temporary view
df.createOrReplaceTempView("my_table")

// Global temporary view
df.createGlobalTempView("global_table")

// SQL queries
val result = spark.sql("SELECT * FROM my_table WHERE age > 25")
```

### Common SQL Operations
```sql
-- Basic queries
SELECT customer_id, amount, date 
FROM transactions 
WHERE status = 'completed';

-- Aggregations
SELECT category, COUNT(*) as count, AVG(amount) as avg_amount
FROM transactions 
GROUP BY category;

-- Window functions
SELECT 
  customer_id,
  amount,
  ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY date) as rn
FROM transactions;

-- CTEs
WITH high_value_customers AS (
  SELECT customer_id, SUM(amount) as total_amount
  FROM transactions
  GROUP BY customer_id
  HAVING SUM(amount) > 10000
)
SELECT * FROM high_value_customers;
```

## Streaming

### Structured Streaming
```scala
// Read stream
val streamDF = spark
  .readStream
  .format("kafka")
  .option("kafka.bootstrap.servers", "localhost:9092")
  .option("subscribe", "topic_name")
  .load()

// Process stream
val processedStream = streamDF
  .select(from_json($"value".cast("string"), schema).alias("data"))
  .select("data.*")

// Write stream
val query = processedStream
  .writeStream
  .outputMode("append")
  .format("console")
  .trigger(Trigger.ProcessingTime("10 seconds"))
  .start()

query.awaitTermination()
```

### Windowed Aggregations
```scala
// Time-based windows
val windowedCounts = streamDF
  .withWatermark("timestamp", "10 minutes")
  .groupBy(
    window($"timestamp", "5 minutes"),
    $"category"
  )
  .count()
```

## Configuration

### Common Spark Configurations
```scala
// Memory settings
spark.conf.set("spark.executor.memory", "4g")
spark.conf.set("spark.driver.memory", "2g")
spark.conf.set("spark.executor.memoryFraction", "0.8")

// Parallelism
spark.conf.set("spark.sql.shuffle.partitions", "200")
spark.conf.set("spark.default.parallelism", "100")

// Adaptive Query Execution
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")

// Serialization
spark.conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
```

### Submit Configuration
```bash
spark-submit \
  --master yarn \
  --deploy-mode cluster \
  --executor-memory 8g \
  --executor-cores 4 \
  --num-executors 20 \
  --driver-memory 4g \
  --conf spark.sql.adaptive.enabled=true \
  --conf spark.sql.adaptive.coalescePartitions.enabled=true \
  application.jar
```

## Data Quality and Validation

### Null Handling
```scala
// Check for nulls
val nullCounts = df.columns.map { colName =>
  colName -> df.filter(df(colName).isNull).count()
}.toMap

// Fill nulls
df.fillna(Map("numeric_col" -> 0, "string_col" -> "unknown"))
df.fillna(0) // Fill all numeric nulls with 0

// Drop nulls
df.dropna() // Drop rows with any null
df.dropna(Seq("important_col")) // Drop if specific column is null
```

### Data Validation
```scala
// Basic statistics
df.describe().show()
df.summary("count", "mean", "stddev", "min", "25%", "75%", "max").show()

// Custom validation
def validateDataFrame(df: DataFrame, requiredColumns: Seq[String]): Boolean = {
  val missingCols = requiredColumns.filterNot(df.columns.contains)
  if (missingCols.nonEmpty) {
    throw new IllegalArgumentException(s"Missing columns: ${missingCols.mkString(", ")}")
  }
  df.count() > 0
}
```

## UDFs (User Defined Functions)

### Scala UDFs
```scala
import org.apache.spark.sql.functions.udf

// Define UDF
val categorizeAge = udf((age: Int) => {
  if (age < 18) "minor"
  else if (age < 65) "adult"
  else "senior"
})

// Use UDF
df.withColumn("age_category", categorizeAge($"age"))

// Register for SQL
spark.udf.register("categorize_age", categorizeAge)
spark.sql("SELECT *, categorize_age(age) as age_category FROM my_table")
```

## Error Handling

### Try-Catch Patterns
```scala
import scala.util.{Try, Success, Failure}

// Safe DataFrame operations
def safeRead(path: String): Option[DataFrame] = {
  Try(spark.read.parquet(path)) match {
    case Success(df) => Some(df)
    case Failure(exception) => 
      println(s"Failed to read $path: ${exception.getMessage}")
      None
  }
}

// Handle malformed records
val df = spark.read
  .option("mode", "PERMISSIVE")
  .option("columnNameOfCorruptRecord", "_corrupt_record")
  .json("input/data.json")

val cleanDF = df.filter($"_corrupt_record".isNull).drop("_corrupt_record")
val corruptDF = df.filter($"_corrupt_record".isNotNull)
```

## Debugging and Monitoring

### Query Plans
```scala
// Show execution plan
df.explain()
df.explain(true) // Extended explanation
df.explain("cost") // Cost-based explanation

// Show physical plan
df.queryExecution.executedPlan
```

### Monitoring
```scala
// Check Spark UI
println(s"Spark UI: ${spark.sparkContext.uiWebUrl}")

// Application info
println(s"Application ID: ${spark.sparkContext.applicationId}")
println(s"Application Name: ${spark.sparkContext.appName}")

// Executor info
val executors = spark.sparkContext.statusTracker.getExecutorInfos
executors.foreach { executor =>
  println(s"Executor ${executor.executorId}: ${executor.totalCores} cores")
}
```

## Testing

### Unit Testing
```scala
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers

class DataTransformationTest extends AnyFlatSpec with Matchers {
  
  "Data transformation" should "correctly aggregate data" in {
    val spark = SparkSession.builder()
      .appName("test")
      .master("local[2]")
      .getOrCreate()
    
    import spark.implicits._
    
    val inputData = Seq(
      ("Alice", 25),
      ("Bob", 30)
    ).toDF("name", "age")
    
    val result = inputData.filter($"age" > 25)
    
    result.count() should be(1)
    result.first().getString(0) should be("Bob")
    
    spark.stop()
  }
}
```

### Data Comparison
```scala
def assertDataFramesEqual(df1: DataFrame, df2: DataFrame): Unit = {
  assert(df1.count() == df2.count())
  assert(df1.columns.sameElements(df2.columns))
  assert(df1.except(df2).count() == 0)
  assert(df2.except(df1).count() == 0)
}
```