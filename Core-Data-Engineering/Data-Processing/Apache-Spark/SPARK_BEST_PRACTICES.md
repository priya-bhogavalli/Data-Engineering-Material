# Apache Spark Best Practices for Data Engineering

## 1. Cluster Configuration and Resource Management

### Optimal Resource Allocation
```bash
# Executor configuration for large datasets
spark-submit \
  --master yarn \
  --deploy-mode cluster \
  --executor-memory 8g \
  --executor-cores 4 \
  --num-executors 20 \
  --driver-memory 4g \
  --driver-cores 2 \
  --conf spark.executor.memoryFraction=0.8 \
  --conf spark.sql.shuffle.partitions=400 \
  application.py

# Dynamic allocation for variable workloads
--conf spark.dynamicAllocation.enabled=true \
--conf spark.dynamicAllocation.minExecutors=5 \
--conf spark.dynamicAllocation.maxExecutors=50 \
--conf spark.dynamicAllocation.initialExecutors=10
```

### Memory Management Best Practices
```scala
// Optimal memory configuration
val spark = SparkSession.builder()
  .appName("OptimizedSparkApp")
  .config("spark.executor.memory", "8g")
  .config("spark.executor.memoryFraction", "0.8")
  .config("spark.storage.memoryFraction", "0.6")
  .config("spark.shuffle.memoryFraction", "0.2")
  .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
  .getOrCreate()

// Register custom classes for Kryo serialization
spark.conf.set("spark.kryo.registrator", "com.company.MyKryoRegistrator")
```

## 2. Data Partitioning Strategies

### Optimal Partitioning
```scala
import org.apache.spark.sql.functions._

// Partition by frequently filtered columns
df.write
  .partitionBy("year", "month", "day")
  .mode("overwrite")
  .parquet("output/partitioned_data")

// Repartition for better distribution
val optimizedDF = df.repartition(200, col("customer_id"))

// Coalesce to reduce small files
val coalescedDF = df.coalesce(50)

// Check partition distribution
df.rdd.mapPartitions(iter => Iterator(iter.size)).collect()
```

### Partition Size Guidelines
```scala
// Optimal partition size: 128MB - 1GB
def calculateOptimalPartitions(dataSize: Long, targetPartitionSize: Long = 128 * 1024 * 1024): Int = {
  Math.max(1, (dataSize / targetPartitionSize).toInt)
}

// Custom partitioner for skewed data
class CustomPartitioner(numPartitions: Int) extends Partitioner {
  override def getPartition(key: Any): Int = {
    key match {
      case k: String => 
        // Custom logic for string keys
        Math.abs(k.hashCode) % numPartitions
      case _ => 
        Math.abs(key.hashCode) % numPartitions
    }
  }
}
```

## 3. Performance Optimization Techniques

### Catalyst Optimizer Utilization
```scala
// Use DataFrame API for Catalyst optimization
val optimizedQuery = df
  .filter(col("status") === "active")
  .select("customer_id", "amount", "date")
  .groupBy("customer_id")
  .agg(sum("amount").as("total_amount"))

// Avoid RDD operations when possible
// Bad: df.rdd.map(row => ...).toDF()
// Good: df.withColumn("new_col", expr("existing_col * 2"))

// Enable cost-based optimization
spark.conf.set("spark.sql.cbo.enabled", "true")
spark.conf.set("spark.sql.statistics.histogram.enabled", "true")
```

### Join Optimization
```scala
// Broadcast small tables (< 10MB)
val broadcastDF = broadcast(smallDF)
val result = largeDF.join(broadcastDF, "key")

// Use appropriate join hints
val result = largeDF.hint("broadcast").join(smallDF, "key")

// Optimize join order - smaller tables first
val result = df1
  .join(broadcast(smallestDF), "key1")
  .join(mediumDF, "key2")
  .join(largestDF, "key3")

// Bucketed joins for large tables
df.write
  .bucketBy(10, "customer_id")
  .sortBy("transaction_date")
  .saveAsTable("bucketed_transactions")
```

### Caching Strategies
```scala
import org.apache.spark.storage.StorageLevel

// Cache frequently accessed DataFrames
val cachedDF = df.cache() // MEMORY_AND_DISK by default

// Choose appropriate storage level
val memoryOnlyDF = df.persist(StorageLevel.MEMORY_ONLY)
val diskOnlyDF = df.persist(StorageLevel.DISK_ONLY)
val serializedDF = df.persist(StorageLevel.MEMORY_ONLY_SER)

// Unpersist when no longer needed
cachedDF.unpersist()

// Cache at the right time - after expensive operations
val expensiveDF = df
  .join(largeTable, "key")
  .filter(complexCondition)
  .cache() // Cache here, not at the beginning

expensiveDF.count() // Trigger caching
```

## 4. Data Skew Handling

### Skew Detection and Mitigation
```scala
// Detect data skew
val skewAnalysis = df
  .groupBy("partition_key")
  .count()
  .orderBy(desc("count"))

skewAnalysis.show(20)

// Salting technique for skewed joins
import scala.util.Random

val saltedDF = df.withColumn("salted_key", 
  concat(col("skewed_key"), lit("_"), lit(Random.nextInt(10))))

// Separate processing for hot keys
val hotKeys = Array("key1", "key2", "key3")
val hotData = df.filter(col("key").isin(hotKeys: _*))
val normalData = df.filter(!col("key").isin(hotKeys: _*))

// Process separately and union
val hotResult = hotData.repartition(100, col("key"))
val normalResult = normalData.repartition(20, col("key"))
val finalResult = hotResult.union(normalResult)
```

### Adaptive Query Execution (AQE)
```scala
// Enable AQE for automatic optimization
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.localShuffleReader.enabled", "true")

// Configure skew join thresholds
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionFactor", "5")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "256MB")
```

## 5. I/O Optimization

### File Format Selection
```scala
// Parquet for analytical workloads
df.write
  .option("compression", "snappy")
  .mode("overwrite")
  .parquet("output/parquet_data")

// Delta Lake for ACID transactions
df.write
  .format("delta")
  .option("optimizeWrite", "true")
  .option("autoCompact", "true")
  .mode("overwrite")
  .save("output/delta_table")

// Avro for schema evolution
df.write
  .format("avro")
  .option("avroSchema", schema.toString)
  .mode("overwrite")
  .save("output/avro_data")
```

### Compression Strategies
```scala
// Configure compression for different formats
spark.conf.set("spark.sql.parquet.compression.codec", "snappy")
spark.conf.set("spark.sql.orc.compression.codec", "zlib")
spark.conf.set("spark.io.compression.codec", "lz4")

// Optimize for different use cases
// For storage optimization: gzip
// For processing speed: lz4 or snappy
// For network transfer: gzip or brotli
```

## 6. SQL Optimization

### Query Optimization Techniques
```sql
-- Use column pruning
SELECT customer_id, amount, date 
FROM transactions 
WHERE status = 'completed';

-- Predicate pushdown
SELECT * FROM (
  SELECT customer_id, amount 
  FROM transactions 
  WHERE amount > 100
) WHERE customer_id IN (1, 2, 3);

-- Optimize window functions
SELECT 
  customer_id,
  amount,
  ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY date) as rn
FROM transactions
QUALIFY rn = 1; -- Use QUALIFY when available

-- Use EXISTS instead of IN for better performance
SELECT * FROM customers c
WHERE EXISTS (
  SELECT 1 FROM transactions t 
  WHERE t.customer_id = c.customer_id
);
```

### Statistics and Cost-Based Optimization
```sql
-- Analyze tables for better query planning
ANALYZE TABLE transactions COMPUTE STATISTICS;
ANALYZE TABLE transactions COMPUTE STATISTICS FOR COLUMNS customer_id, amount, date;

-- Update statistics after major data changes
REFRESH TABLE transactions;

-- Check table statistics
DESCRIBE EXTENDED transactions;
```

## 7. Streaming Best Practices

### Structured Streaming Optimization
```scala
// Optimal streaming configuration
val streamingQuery = spark
  .readStream
  .format("kafka")
  .option("kafka.bootstrap.servers", "localhost:9092")
  .option("subscribe", "input-topic")
  .option("maxOffsetsPerTrigger", 100000)
  .option("startingOffsets", "latest")
  .load()

// Watermarking for late data
val watermarkedDF = streamingDF
  .withWatermark("timestamp", "10 minutes")
  .groupBy(window(col("timestamp"), "5 minutes"), col("category"))
  .count()

// Optimize trigger intervals
val query = watermarkedDF
  .writeStream
  .outputMode("update")
  .trigger(Trigger.ProcessingTime("30 seconds"))
  .format("delta")
  .option("checkpointLocation", "checkpoints/streaming")
  .start("output/streaming_results")
```

### Checkpointing Strategy
```scala
// Configure checkpointing
spark.sparkContext.setCheckpointDir("hdfs://checkpoints")

// Checkpoint expensive RDDs
val expensiveRDD = data.map(complexTransformation).cache()
expensiveRDD.checkpoint()
expensiveRDD.count() // Trigger checkpointing

// Streaming checkpoint management
val checkpointLocation = "s3a://bucket/checkpoints/app-name"
// Clean up old checkpoints periodically
```

## 8. Memory Management and Garbage Collection

### JVM Tuning
```bash
# G1GC for large heaps
--conf spark.executor.extraJavaOptions="-XX:+UseG1GC -XX:MaxGCPauseMillis=200"

# Parallel GC for smaller heaps
--conf spark.executor.extraJavaOptions="-XX:+UseParallelGC"

# Memory debugging
--conf spark.executor.extraJavaOptions="-XX:+PrintGCDetails -XX:+PrintGCTimeStamps"

# Off-heap memory for caching
--conf spark.sql.columnVector.offheap.enabled=true
```

### Memory Monitoring
```scala
// Monitor memory usage
val memoryStatus = spark.sparkContext.getExecutorMemoryStatus
memoryStatus.foreach { case (executorId, (maxMem, remainingMem)) =>
  println(s"Executor $executorId: ${(maxMem - remainingMem) / 1024 / 1024}MB used of ${maxMem / 1024 / 1024}MB")
}

// Custom memory listener
class MemoryListener extends SparkListener {
  override def onExecutorMetricsUpdate(executorMetricsUpdate: SparkListenerExecutorMetricsUpdate): Unit = {
    // Log memory metrics
  }
}

spark.sparkContext.addSparkListener(new MemoryListener())
```

## 9. Error Handling and Fault Tolerance

### Robust Error Handling
```scala
import org.apache.spark.sql.catalyst.encoders.ExpressionEncoder
import org.apache.spark.sql.Encoder

// Handle malformed records
val df = spark.read
  .option("mode", "PERMISSIVE")
  .option("columnNameOfCorruptRecord", "_corrupt_record")
  .json("input/data.json")

// Filter out corrupt records
val cleanDF = df.filter(col("_corrupt_record").isNull).drop("_corrupt_record")
val corruptDF = df.filter(col("_corrupt_record").isNotNull)

// Custom exception handling in transformations
def safeTransformation(value: String): Option[Double] = {
  try {
    Some(value.toDouble)
  } catch {
    case _: NumberFormatException => None
  }
}

val safeUDF = udf(safeTransformation _)
val resultDF = df.withColumn("safe_value", safeUDF(col("string_value")))
```

### Retry Mechanisms
```scala
import scala.util.{Try, Success, Failure}
import scala.concurrent.duration._

def retryOperation[T](operation: => T, maxRetries: Int = 3, delay: Duration = 1.second): T = {
  def attempt(retriesLeft: Int): T = {
    Try(operation) match {
      case Success(result) => result
      case Failure(exception) if retriesLeft > 0 =>
        Thread.sleep(delay.toMillis)
        attempt(retriesLeft - 1)
      case Failure(exception) => throw exception
    }
  }
  attempt(maxRetries)
}

// Usage in Spark operations
val result = retryOperation {
  df.write.mode("overwrite").parquet("output/data")
}
```

## 10. Monitoring and Observability

### Application Monitoring
```scala
// Custom metrics using accumulators
val errorCount = spark.sparkContext.longAccumulator("Error Count")
val processedRecords = spark.sparkContext.longAccumulator("Processed Records")

df.foreach { row =>
  try {
    // Process row
    processedRecords.add(1)
  } catch {
    case _: Exception => errorCount.add(1)
  }
}

println(s"Processed: ${processedRecords.value}, Errors: ${errorCount.value}")
```

### Performance Monitoring
```scala
// Query execution time tracking
val startTime = System.currentTimeMillis()
val result = df.groupBy("category").count().collect()
val executionTime = System.currentTimeMillis() - startTime
println(s"Query executed in ${executionTime}ms")

// Stage-level monitoring
spark.sparkContext.addSparkListener(new SparkListener {
  override def onStageCompleted(stageCompleted: SparkListenerStageCompleted): Unit = {
    val stageInfo = stageCompleted.stageInfo
    println(s"Stage ${stageInfo.stageId} completed in ${stageInfo.completionTime.get - stageInfo.submissionTime.get}ms")
  }
})
```

## 11. Security Best Practices

### Authentication and Authorization
```scala
// Kerberos authentication
spark.conf.set("spark.security.credentials.hbase.enabled", "true")
spark.conf.set("spark.security.credentials.hive.enabled", "true")

// SSL/TLS configuration
spark.conf.set("spark.ssl.enabled", "true")
spark.conf.set("spark.ssl.keyStore", "/path/to/keystore")
spark.conf.set("spark.ssl.keyStorePassword", "password")
spark.conf.set("spark.ssl.trustStore", "/path/to/truststore")
spark.conf.set("spark.ssl.trustStorePassword", "password")
```

### Data Encryption
```scala
// Encrypt shuffle data
spark.conf.set("spark.io.encryption.enabled", "true")
spark.conf.set("spark.io.encryption.keySizeBits", "256")

// Encrypt RDD data
spark.conf.set("spark.storage.encryption.enabled", "true")

// Column-level encryption (application level)
import org.apache.spark.sql.functions._

val encryptUDF = udf((data: String) => encrypt(data, secretKey))
val decryptUDF = udf((encryptedData: String) => decrypt(encryptedData, secretKey))

val encryptedDF = df.withColumn("encrypted_column", encryptUDF(col("sensitive_column")))
```

## 12. Testing and Validation

### Unit Testing Framework
```scala
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers
import org.apache.spark.sql.test.SharedSparkSession

class DataTransformationTest extends AnyFlatSpec with Matchers with SharedSparkSession {
  
  "Data transformation" should "correctly aggregate data" in {
    import spark.implicits._
    
    val inputData = Seq(
      ("A", 10),
      ("B", 20),
      ("A", 15)
    ).toDF("category", "value")
    
    val result = inputData.groupBy("category").sum("value")
    val resultMap = result.collect().map(row => row.getString(0) -> row.getLong(1)).toMap
    
    resultMap("A") should be(25)
    resultMap("B") should be(20)
  }
}
```

### Data Quality Validation
```scala
// Data quality checks
def validateDataQuality(df: DataFrame): Map[String, Any] = {
  val totalRows = df.count()
  val nullCounts = df.columns.map { col =>
    col -> df.filter(df(col).isNull).count()
  }.toMap
  
  Map(
    "total_rows" -> totalRows,
    "null_counts" -> nullCounts,
    "completeness" -> nullCounts.mapValues(nullCount => 1.0 - nullCount.toDouble / totalRows)
  )
}

// Schema validation
def validateSchema(df: DataFrame, expectedSchema: StructType): Boolean = {
  df.schema.fields.map(_.name).sorted == expectedSchema.fields.map(_.name).sorted
}
```