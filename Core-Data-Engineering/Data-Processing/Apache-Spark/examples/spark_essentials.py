"""
Apache Spark Essential Examples
Minimal code demonstrating core Spark concepts
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count, when
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

# Initialize Spark
spark = SparkSession.builder \
    .appName("SparkEssentials") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

# 1. Basic DataFrame Operations
def basic_operations():
    """Essential DataFrame operations"""
    # Read data
    df = spark.read.csv("data.csv", header=True, inferSchema=True)
    
    # Basic transformations
    filtered = df.filter(col("amount") > 100)
    selected = filtered.select("id", "amount", "category")
    
    # Show results
    selected.show(10)
    print(f"Total records: {selected.count()}")

# 2. Aggregations and Grouping
def aggregation_example():
    """Common aggregation patterns"""
    df = spark.read.csv("sales.csv", header=True, inferSchema=True)
    
    # Group by and aggregate
    summary = df.groupBy("category") \
        .agg(
            sum("amount").alias("total_sales"),
            avg("amount").alias("avg_sales"),
            count("*").alias("transaction_count")
        )
    
    summary.orderBy(col("total_sales").desc()).show()

# 3. Joins
def join_example():
    """Basic join operations"""
    customers = spark.read.csv("customers.csv", header=True, inferSchema=True)
    orders = spark.read.csv("orders.csv", header=True, inferSchema=True)
    
    # Inner join
    result = customers.join(orders, "customer_id", "inner")
    
    # Select specific columns
    final = result.select("customer_name", "order_amount", "order_date")
    final.show()

# 4. Window Functions
def window_example():
    """Window function example"""
    from pyspark.sql.window import Window
    from pyspark.sql.functions import row_number, rank
    
    df = spark.read.csv("sales.csv", header=True, inferSchema=True)
    
    # Define window
    window = Window.partitionBy("category").orderBy(col("amount").desc())
    
    # Add ranking
    ranked = df.withColumn("rank", rank().over(window))
    
    # Top 3 per category
    top3 = ranked.filter(col("rank") <= 3)
    top3.show()

# 5. Data Cleaning
def data_cleaning():
    """Common data cleaning operations"""
    df = spark.read.csv("raw_data.csv", header=True, inferSchema=True)
    
    # Remove nulls and duplicates
    cleaned = df.dropna() \
        .dropDuplicates() \
        .filter(col("amount") > 0)
    
    # Add derived columns
    final = cleaned.withColumn(
        "amount_category",
        when(col("amount") < 100, "small")
        .when(col("amount") < 1000, "medium")
        .otherwise("large")
    )
    
    return final

# 6. Spark SQL
def sql_example():
    """Using Spark SQL"""
    df = spark.read.csv("data.csv", header=True, inferSchema=True)
    
    # Register as temp view
    df.createOrReplaceTempView("sales")
    
    # Use SQL
    result = spark.sql("""
        SELECT category, 
               SUM(amount) as total,
               COUNT(*) as transactions
        FROM sales
        WHERE amount > 50
        GROUP BY category
        ORDER BY total DESC
    """)
    
    result.show()

# 7. Streaming Example
def streaming_example():
    """Basic structured streaming"""
    # Read from Kafka (example)
    stream_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "sales_topic") \
        .load()
    
    # Process stream
    processed = stream_df.selectExpr("CAST(value AS STRING)") \
        .groupBy("value") \
        .count()
    
    # Write to console
    query = processed.writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()
    
    return query

# 8. Performance Optimization
def optimization_example():
    """Performance optimization techniques"""
    df = spark.read.parquet("large_dataset.parquet")
    
    # Cache frequently used DataFrame
    df.cache()
    
    # Repartition for better parallelism
    df_repartitioned = df.repartition(10, "partition_column")
    
    # Use broadcast for small lookup tables
    small_df = spark.read.csv("lookup.csv", header=True)
    broadcast_df = spark.sparkContext.broadcast(small_df.collect())
    
    return df_repartitioned

# Usage
if __name__ == "__main__":
    # Run examples
    basic_operations()
    aggregation_example()
    join_example()
    
    # Clean up
    spark.stop()