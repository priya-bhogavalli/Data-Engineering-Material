#!/usr/bin/env python3
"""
PySpark Data Processing Examples with Expected Outputs

This file demonstrates common PySpark operations with clear examples
of what the output should look like for each operation.
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import Window
import pyspark.sql.functions as F

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("DataProcessingExamples") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .getOrCreate()

# =====================================================
# 1. BASIC DATA LOADING AND EXPLORATION
# =====================================================

def create_sample_data():
    """Create sample datasets for demonstration."""
    
    # Sample sales data
    sales_data = [
        (1, "2023-01-15", 101, "Electronics", 1299.99, 2),
        (2, "2023-01-16", 102, "Clothing", 89.50, 1),
        (3, "2023-01-17", 103, "Electronics", 599.99, 1),
        (4, "2023-01-18", 101, "Books", 29.99, 3),
        (5, "2023-01-19", 104, "Electronics", 899.99, 1),
        (6, "2023-01-20", 102, "Clothing", 149.99, 2),
        (7, "2023-01-21", 105, "Books", 19.99, 1),
        (8, "2023-01-22", 103, "Electronics", 1599.99, 1),
    ]
    
    sales_schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("order_date", StringType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("category", StringType(), True),
        StructField("amount", DoubleType(), True),
        StructField("quantity", IntegerType(), True)
    ])
    
    sales_df = spark.createDataFrame(sales_data, sales_schema)
    
    # Sample customer data
    customer_data = [
        (101, "John Smith", "Premium", "2022-03-15"),
        (102, "Jane Doe", "Standard", "2022-07-20"),
        (103, "Bob Johnson", "Premium", "2021-11-10"),
        (104, "Alice Brown", "Standard", "2023-01-05"),
        (105, "Charlie Wilson", "Basic", "2022-12-01")
    ]
    
    customer_schema = StructType([
        StructField("customer_id", IntegerType(), True),
        StructField("customer_name", StringType(), True),
        StructField("tier", StringType(), True),
        StructField("signup_date", StringType(), True)
    ])
    
    customer_df = spark.createDataFrame(customer_data, customer_schema)
    
    return sales_df, customer_df

# Create sample data
sales_df, customer_df = create_sample_data()

print("=== BASIC DATA EXPLORATION ===")
print("\nSales DataFrame Schema:")
sales_df.printSchema()
# Output: Shows schema with column names and types

print("\nSales DataFrame Sample:")
sales_df.show()
# Output: 8 rows of sales data with order_id, date, customer_id, category, amount, quantity

print("\nCustomer DataFrame Sample:")
customer_df.show()
# Output: 5 rows of customer data with customer_id, name, tier, signup_date

"""
EXPECTED OUTPUT:

=== BASIC DATA EXPLORATION ===

Sales DataFrame Schema:
root
 |-- order_id: integer (nullable = true)
 |-- order_date: string (nullable = true)
 |-- customer_id: integer (nullable = true)
 |-- category: string (nullable = true)
 |-- amount: double (nullable = true)
 |-- quantity: integer (nullable = true)

Sales DataFrame Sample:
+--------+----------+-----------+-----------+-------+--------+
|order_id|order_date|customer_id|   category| amount|quantity|
+--------+----------+-----------+-----------+-------+--------+
|       1|2023-01-15|        101|Electronics|1299.99|       2|
|       2|2023-01-16|        102|   Clothing|   89.5|       1|
|       3|2023-01-17|        103|Electronics| 599.99|       1|
|       4|2023-01-18|        101|      Books|  29.99|       3|
|       5|2023-01-19|        104|Electronics| 899.99|       1|
|       6|2023-01-20|        102|   Clothing| 149.99|       2|
|       7|2023-01-21|        105|      Books|  19.99|       1|
|       8|2023-01-22|        103|Electronics|1599.99|       1|
+--------+----------+-----------+-----------+-------+--------+

Customer DataFrame Sample:
+-----------+-------------+--------+----------+
|customer_id|customer_name|    tier|signup_date|
+-----------+-------------+--------+----------+
|        101|   John Smith| Premium| 2022-03-15|
|        102|     Jane Doe|Standard| 2022-07-20|
|        103|  Bob Johnson| Premium| 2021-11-10|
|        104|  Alice Brown|Standard| 2023-01-05|
|        105|Charlie Wilson|   Basic| 2022-12-01|
+-----------+-------------+--------+----------+
"""

# =====================================================
# 2. DATA TRANSFORMATIONS AND AGGREGATIONS
# =====================================================

print("\n=== DATA TRANSFORMATIONS ===")

# Add calculated columns
sales_with_total = sales_df.withColumn(
    "total_amount", 
    col("amount") * col("quantity")
).withColumn(
    "order_date_parsed", 
    to_date(col("order_date"), "yyyy-MM-dd")
)

print("\nSales with calculated total amount:")
sales_with_total.select("order_id", "amount", "quantity", "total_amount").show()
# Output: Shows calculated total_amount = amount * quantity for each order

# Aggregations by category
category_summary = sales_with_total.groupBy("category").agg(
    count("order_id").alias("total_orders"),
    sum("total_amount").alias("total_revenue"),
    avg("total_amount").alias("avg_order_value"),
    max("total_amount").alias("max_order_value")
).orderBy(desc("total_revenue"))

print("\nCategory Summary:")
category_summary.show()
# Output: Electronics: 4 orders, $6099.95 revenue; Clothing: 2 orders, $389.48; Books: 2 orders, $109.96

"""
EXPECTED OUTPUT:

=== DATA TRANSFORMATIONS ===

Sales with calculated total amount:
+--------+-------+--------+------------+
|order_id| amount|quantity|total_amount|
+--------+-------+--------+------------+
|       1|1299.99|       2|     2599.98|
|       2|   89.5|       1|        89.5|
|       3| 599.99|       1|      599.99|
|       4|  29.99|       3|       89.97|
|       5| 899.99|       1|      899.99|
|       6| 149.99|       2|      299.98|
|       7|  19.99|       1|       19.99|
|       8|1599.99|       1|     1599.99|
+--------+-------+--------+------------+

Category Summary:
+-----------+------------+-------------+------------------+---------------+
|   category|total_orders|total_revenue|   avg_order_value|max_order_value|
+-----------+------------+-------------+------------------+---------------+
|Electronics|           4|      6099.95|1524.9875000000002|        2599.98|
|   Clothing|           2|       389.48|            194.74|         299.98|
|      Books|           2|       109.96|             54.98|          89.97|
+-----------+------------+-------------+------------------+---------------+
"""

# =====================================================
# 3. JOINS AND WINDOW FUNCTIONS
# =====================================================

print("\n=== JOINS AND WINDOW FUNCTIONS ===")

# Join sales with customer data
enriched_sales = sales_with_total.join(
    customer_df, 
    on="customer_id", 
    how="inner"
)

print("\nEnriched Sales Data:")
enriched_sales.select("order_id", "customer_name", "tier", "category", "total_amount").show()
# Output: Sales data joined with customer names and tiers

# Window functions - running totals and rankings
window_spec = Window.partitionBy("customer_id").orderBy("order_date_parsed")
customer_window = Window.partitionBy("customer_id")

sales_with_analytics = enriched_sales.withColumn(
    "running_total", 
    sum("total_amount").over(window_spec)
).withColumn(
    "order_rank", 
    row_number().over(window_spec)
).withColumn(
    "customer_total_spent", 
    sum("total_amount").over(customer_window)
)

print("\nSales with Window Functions:")
sales_with_analytics.select(
    "customer_name", "order_date", "total_amount", 
    "running_total", "order_rank", "customer_total_spent"
).orderBy("customer_id", "order_date").show()
# Output: Shows running totals, order ranks, and customer total spending

"""
EXPECTED OUTPUT:

=== JOINS AND WINDOW FUNCTIONS ===

Enriched Sales Data:
+--------+-------------+--------+-----------+------------+
|order_id|customer_name|    tier|   category|total_amount|
+--------+-------------+--------+-----------+------------+
|       1|   John Smith| Premium|Electronics|     2599.98|
|       4|   John Smith| Premium|      Books|       89.97|
|       2|     Jane Doe|Standard|   Clothing|        89.5|
|       6|     Jane Doe|Standard|   Clothing|      299.98|
|       3|  Bob Johnson| Premium|Electronics|      599.99|
|       8|  Bob Johnson| Premium|Electronics|     1599.99|
|       5|  Alice Brown|Standard|Electronics|      899.99|
|       7|Charlie Wilson|   Basic|      Books|       19.99|
+--------+-------------+--------+-----------+------------+

Sales with Window Functions:
+-------------+----------+------------+-------------+----------+--------------------+
|customer_name|order_date|total_amount|running_total|order_rank|customer_total_spent|
+-------------+----------+------------+-------------+----------+--------------------+
|   John Smith|2023-01-15|     2599.98|      2599.98|         1|             2689.95|
|   John Smith|2023-01-18|       89.97|      2689.95|         2|             2689.95|
|     Jane Doe|2023-01-16|        89.5|         89.5|         1|              389.48|
|     Jane Doe|2023-01-20|      299.98|       389.48|         2|              389.48|
|  Bob Johnson|2023-01-17|      599.99|       599.99|         1|             2199.98|
|  Bob Johnson|2023-01-22|     1599.99|      2199.98|         2|             2199.98|
|  Alice Brown|2023-01-19|      899.99|       899.99|         1|              899.99|
|Charlie Wilson|2023-01-21|       19.99|        19.99|         1|               19.99|
+-------------+----------+------------+-------------+----------+--------------------+
"""

# =====================================================
# 4. ADVANCED ANALYTICS - CUSTOMER SEGMENTATION
# =====================================================

print("\n=== CUSTOMER SEGMENTATION ===")

# Calculate customer metrics
customer_metrics = enriched_sales.groupBy("customer_id", "customer_name", "tier").agg(
    count("order_id").alias("total_orders"),
    sum("total_amount").alias("total_spent"),
    avg("total_amount").alias("avg_order_value"),
    max("order_date_parsed").alias("last_order_date"),
    min("order_date_parsed").alias("first_order_date")
).withColumn(
    "days_since_last_order",
    datediff(current_date(), col("last_order_date"))
)

# Create customer segments based on RFM-like analysis
customer_segments = customer_metrics.withColumn(
    "segment",
    when((col("total_spent") >= 2000) & (col("total_orders") >= 2), "VIP")
    .when((col("total_spent") >= 1000) & (col("total_orders") >= 2), "High Value")
    .when(col("total_orders") >= 2, "Loyal")
    .when(col("total_spent") >= 500, "Medium Value")
    .otherwise("New/Low Value")
)

print("\nCustomer Segmentation:")
customer_segments.select(
    "customer_name", "total_orders", "total_spent", 
    "avg_order_value", "segment"
).orderBy(desc("total_spent")).show()
# Output: John Smith (VIP), Bob Johnson (High Value), Alice Brown (Medium Value), etc.

# Segment summary
segment_summary = customer_segments.groupBy("segment").agg(
    count("customer_id").alias("customer_count"),
    sum("total_spent").alias("segment_revenue"),
    avg("total_spent").alias("avg_customer_value")
).orderBy(desc("segment_revenue"))

print("\nSegment Summary:")
segment_summary.show()
# Output: Revenue by customer segment - VIP: $2689.95, High Value: $2199.98, etc.

"""
EXPECTED OUTPUT:

=== CUSTOMER SEGMENTATION ===

Customer Segmentation:
+-------------+------------+-----------+------------------+----------+
|customer_name|total_orders|total_spent|   avg_order_value|   segment|
+-------------+------------+-----------+------------------+----------+
|   John Smith|           2|    2689.95|1344.9750000000001|       VIP|
|  Bob Johnson|           2|    2199.98|           1099.99|High Value|
|  Alice Brown|           1|     899.99|            899.99|Medium Value|
|     Jane Doe|           2|     389.48|            194.74|     Loyal|
|Charlie Wilson|           1|      19.99|             19.99|New/Low Value|
+-------------+------------+-----------+------------------+----------+

Segment Summary:
+-------------+---------------+----------------+------------------+
|      segment|customer_count|segment_revenue|avg_customer_value|
+-------------+---------------+----------------+------------------+
|          VIP|              1|         2689.95|           2689.95|
|   High Value|              1|         2199.98|           2199.98|
|Medium Value |              1|          899.99|            899.99|
|        Loyal|              1|          389.48|            389.48|
|New/Low Value|              1|           19.99|             19.99|
+-------------+---------------+----------------+------------------+
"""

# =====================================================
# 5. TIME SERIES ANALYSIS
# =====================================================

print("\n=== TIME SERIES ANALYSIS ===")

# Daily sales trends (simulated with more data)
extended_sales_data = [
    (9, "2023-01-23", 101, "Electronics", 799.99, 1),
    (10, "2023-01-24", 102, "Books", 39.99, 2),
    (11, "2023-01-25", 103, "Clothing", 199.99, 1),
    (12, "2023-01-26", 104, "Electronics", 1299.99, 1),
    (13, "2023-01-27", 105, "Books", 49.99, 1),
]

extended_df = spark.createDataFrame(extended_sales_data, sales_schema)
all_sales = sales_df.union(extended_df)

# Daily aggregations
daily_sales = all_sales.withColumn(
    "order_date_parsed", to_date(col("order_date"), "yyyy-MM-dd")
).withColumn(
    "total_amount", col("amount") * col("quantity")
).groupBy("order_date_parsed").agg(
    count("order_id").alias("daily_orders"),
    sum("total_amount").alias("daily_revenue"),
    avg("total_amount").alias("avg_order_value")
).orderBy("order_date_parsed")

print("\nDaily Sales Trends:")
daily_sales.show()

# Moving averages
window_3_days = Window.orderBy("order_date_parsed").rowsBetween(-2, 0)

daily_with_ma = daily_sales.withColumn(
    "revenue_3day_ma",
    avg("daily_revenue").over(window_3_days)
).withColumn(
    "orders_3day_ma",
    avg("daily_orders").over(window_3_days)
)

print("\nDaily Sales with 3-Day Moving Averages:")
daily_with_ma.select(
    "order_date_parsed", "daily_revenue", "revenue_3day_ma",
    "daily_orders", "orders_3day_ma"
).show()

"""
EXPECTED OUTPUT:

=== TIME SERIES ANALYSIS ===

Daily Sales Trends:
+-----------------+------------+-------------+------------------+
|order_date_parsed|daily_orders|daily_revenue|   avg_order_value|
+-----------------+------------+-------------+------------------+
|       2023-01-15|           1|      2599.98|           2599.98|
|       2023-01-16|           1|         89.5|              89.5|
|       2023-01-17|           1|       599.99|            599.99|
|       2023-01-18|           1|        89.97|             89.97|
|       2023-01-19|           1|       899.99|            899.99|
|       2023-01-20|           1|       299.98|            299.98|
|       2023-01-21|           1|        19.99|             19.99|
|       2023-01-22|           1|      1599.99|           1599.99|
|       2023-01-23|           1|       799.99|            799.99|
|       2023-01-24|           1|        79.98|             79.98|
|       2023-01-25|           1|       199.99|            199.99|
|       2023-01-26|           1|      1299.99|           1299.99|
|       2023-01-27|           1|        49.99|             49.99|
+-----------------+------------+-------------+------------------+

Daily Sales with 3-Day Moving Averages:
+-----------------+-------------+------------------+------------+------------------+
|order_date_parsed|daily_revenue|    revenue_3day_ma|daily_orders|    orders_3day_ma|
+-----------------+-------------+------------------+------------+------------------+
|       2023-01-15|      2599.98|           2599.98|           1|               1.0|
|       2023-01-16|         89.5|1344.7400000000002|           1|               1.0|
|       2023-01-17|       599.99| 1096.4900000000002|           1|               1.0|
|       2023-01-18|        89.97| 259.8200000000001|           1|               1.0|
|       2023-01-19|       899.99| 529.9833333333333|           1|               1.0|
|       2023-01-20|       299.98| 429.9800000000001|           1|               1.0|
|       2023-01-21|        19.99|206.65333333333334|           1|               1.0|
|       2023-01-22|      1599.99| 639.9866666666667|           1|               1.0|
|       2023-01-23|       799.99| 806.6566666666666|           1|               1.0|
|       2023-01-24|        79.98| 826.6533333333333|           1|               1.0|
|       2023-01-25|       199.99| 359.9866666666667|           1|               1.0|
|       2023-01-26|      1299.99| 526.6533333333334|           1|               1.0|
|       2023-01-27|        49.99| 516.6566666666667|           1|               1.0|
+-----------------+-------------+------------------+------------+------------------+
"""

# =====================================================
# 6. DATA QUALITY AND VALIDATION
# =====================================================

print("\n=== DATA QUALITY CHECKS ===")

# Check for nulls and data quality issues
quality_check = sales_df.select([
    count(when(col(c).isNull(), c)).alias(f"null_{c}") 
    for c in sales_df.columns
])

print("\nNull Value Counts:")
quality_check.show()

# Duplicate detection
duplicate_count = sales_df.count() - sales_df.dropDuplicates().count()
print(f"\nDuplicate Records: {duplicate_count}")

# Data validation rules
validation_results = sales_df.select(
    count(when(col("amount") <= 0, 1)).alias("negative_amounts"),
    count(when(col("quantity") <= 0, 1)).alias("invalid_quantities"),
    count(when(col("order_date").rlike(r"^\d{4}-\d{2}-\d{2}$"), 1)).alias("valid_dates"),
    count("*").alias("total_records")
)

print("\nData Validation Results:")
validation_results.show()

"""
EXPECTED OUTPUT:

=== DATA QUALITY CHECKS ===

Null Value Counts:
+----------+--------------+----------------+--------------+-----------+--------------+
|null_order_id|null_order_date|null_customer_id|null_category|null_amount|null_quantity|
+----------+--------------+----------------+--------------+-----------+--------------+
|         0|             0|               0|             0|          0|             0|
+----------+--------------+----------------+--------------+-----------+--------------+

Duplicate Records: 0

Data Validation Results:
+----------------+------------------+-----------+-------------+
|negative_amounts|invalid_quantities|valid_dates|total_records|
+----------------+------------------+-----------+-------------+
|               0|                 0|          8|            8|
+----------------+------------------+-----------+-------------+
"""

# =====================================================
# 7. PERFORMANCE OPTIMIZATION EXAMPLES
# =====================================================

print("\n=== PERFORMANCE OPTIMIZATION ===")

# Cache frequently used DataFrames
enriched_sales.cache()
print("DataFrame cached for better performance")

# Partition information
print(f"\nNumber of partitions: {enriched_sales.rdd.getNumPartitions()}")

# Repartition for better performance (if needed)
optimized_df = enriched_sales.repartition(2, "customer_id")
print(f"Repartitioned DataFrame partitions: {optimized_df.rdd.getNumPartitions()}")

# Show execution plan
print("\nExecution Plan for Category Summary:")
category_summary.explain(True)

"""
EXPECTED OUTPUT:

=== PERFORMANCE OPTIMIZATION ===

DataFrame cached for better performance

Number of partitions: 8

Repartitioned DataFrame partitions: 2

Execution Plan for Category Summary:
== Parsed Logical Plan ==
Sort [total_revenue#123 DESC NULLS LAST], true
+- Aggregate [category#15], [count(order_id#12) AS total_orders#119L, sum(total_amount#108) AS total_revenue#123, avg(total_amount#108) AS avg_order_value#127, max(total_amount#108) AS max_order_value#131]
   +- Project [order_id#12, order_date#13, customer_id#14, category#15, amount#16, quantity#17, (amount#16 * cast(quantity#17 as double)) AS total_amount#108, to_date(order_date#13, Some(yyyy-MM-dd)) AS order_date_parsed#109]
      +- LogicalRDD [order_id#12, order_date#13, customer_id#14, category#15, amount#16, quantity#17], false

== Analyzed Logical Plan ==
[Similar detailed plan...]

== Optimized Logical Plan ==
[Optimized plan with predicate pushdown and other optimizations...]

== Physical Plan ==
[Final physical execution plan...]
"""

# Clean up
spark.stop()

print("\n=== SPARK SESSION STOPPED ===")
print("All examples completed successfully!")

"""
FINAL OUTPUT:
=== SPARK SESSION STOPPED ===
All examples completed successfully!

Key Takeaways from this PySpark Example:
1. DataFrame operations are lazy - they build execution plans
2. Actions like show(), count(), collect() trigger execution
3. Window functions enable advanced analytics
4. Caching improves performance for reused DataFrames
5. Data quality checks are essential in production pipelines
6. Proper partitioning can significantly improve performance
"""