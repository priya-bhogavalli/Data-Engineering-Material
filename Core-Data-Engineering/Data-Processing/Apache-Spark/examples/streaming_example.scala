import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.streaming.Trigger
import org.apache.spark.sql.types._

object StreamingExample {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("StreamingExample")
      .master("local[*]")
      .getOrCreate()

    // Schema for incoming data
    val schema = StructType(Seq(
      StructField("timestamp", TimestampType, true),
      StructField("user_id", StringType, true),
      StructField("event_type", StringType, true),
      StructField("value", DoubleType, true)
    ))

    // Read from Kafka
    val kafkaStream = spark
      .readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", "localhost:9092")
      .option("subscribe", "events")
      .load()

    // Parse JSON and apply schema
    val parsedStream = kafkaStream
      .select(from_json(col("value").cast("string"), schema).alias("data"))
      .select("data.*")

    // Windowed aggregations
    val windowedCounts = parsedStream
      .withWatermark("timestamp", "10 minutes")
      .groupBy(
        window(col("timestamp"), "5 minutes"),
        col("event_type")
      )
      .count()

    // Write to console
    val query = windowedCounts
      .writeStream
      .outputMode("update")
      .format("console")
      .trigger(Trigger.ProcessingTime("30 seconds"))
      .start()

    query.awaitTermination()
  }
}