# Data Processing Quick Reference

## Spark Commands
```python
# Session creation
spark = SparkSession.builder.appName("DataProcessing").getOrCreate()

# Read/Write
df = spark.read.parquet("path")
df.write.mode("overwrite").parquet("output")

# Transformations
df.select("col1", "col2").filter(col("amount") > 100)
df.groupBy("key").agg(sum("amount").alias("total"))

# Joins
df1.join(df2, "key", "inner")
```

## Streaming
```python
# Kafka streaming
df = spark.readStream.format("kafka").option("subscribe", "topic").load()
query = df.writeStream.format("console").start()
```

## Performance
```python
# Caching
df.cache()
df.repartition(200)
df.coalesce(10)
```