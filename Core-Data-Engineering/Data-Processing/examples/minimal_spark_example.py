#!/usr/bin/env python3
"""
Minimal Spark Example - Data Processing Pipeline
Output: Processed sales data with aggregations
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count

# Initialize Spark
spark = SparkSession.builder.appName("MinimalExample").getOrCreate()

# Sample data
data = [
    ("Electronics", "Laptop", 1200, "2024-01-15"),
    ("Electronics", "Phone", 800, "2024-01-16"),
    ("Clothing", "Shirt", 50, "2024-01-15"),
    ("Clothing", "Pants", 80, "2024-01-16"),
    ("Electronics", "Tablet", 400, "2024-01-17")
]

# Create DataFrame
df = spark.createDataFrame(data, ["category", "product", "price", "date"])

# Process data
result = df.groupBy("category").agg(
    sum("price").alias("total_sales"),
    avg("price").alias("avg_price"),
    count("product").alias("product_count")
)

# Show results
result.show()

# Output:
# +-----------+-----------+---------+-------------+
# |   category|total_sales|avg_price|product_count|
# +-----------+-----------+---------+-------------+
# |Electronics|       2400|    800.0|            3|
# |   Clothing|        130|     65.0|            2|
# +-----------+-----------+---------+-------------+

spark.stop()