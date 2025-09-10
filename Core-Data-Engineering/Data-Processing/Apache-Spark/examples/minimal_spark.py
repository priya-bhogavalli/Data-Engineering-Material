"""
Minimal Apache Spark Examples with Outputs
Core operations for data processing
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("MinimalSpark").getOrCreate()

# 1. DataFrame Creation
df = spark.createDataFrame([
    (1, "Alice", 25, "Engineering"),
    (2, "Bob", 30, "Sales"),
    (3, "Charlie", 35, "Engineering")
], ["id", "name", "age", "department"])

print(f"Created DataFrame with {df.count()} rows")
# Output: Created DataFrame with 3 rows

# 2. Basic Operations
df.select("name", "age").show()
# Output:
# +-------+---+
# |   name|age|
# +-------+---+
# |  Alice| 25|
# |    Bob| 30|
# |Charlie| 35|
# +-------+---+

# 3. Filtering
young_employees = df.filter(col("age") < 30)
print(f"Young employees: {young_employees.count()}")
# Output: Young employees: 1

# 4. Aggregations
dept_stats = df.groupBy("department").agg(
    count("*").alias("count"),
    avg("age").alias("avg_age")
)
dept_stats.show()
# Output:
# +-----------+-----+-------+
# | department|count|avg_age|
# +-----------+-----+-------+
# |Engineering|    2|   30.0|
# |      Sales|    1|   30.0|
# +-----------+-----+-------+

# 5. Data Transformation
transformed = df.withColumn("age_group", 
    when(col("age") < 30, "Young")
    .when(col("age") < 40, "Middle")
    .otherwise("Senior")
)
transformed.select("name", "age", "age_group").show()
# Output:
# +-------+---+---------+
# |   name|age|age_group|
# +-------+---+---------+
# |  Alice| 25|    Young|
# |    Bob| 30|   Middle|
# |Charlie| 35|   Middle|
# +-------+---+---------+

# 6. Join Operations
salaries = spark.createDataFrame([
    (1, 50000), (2, 60000), (3, 70000)
], ["id", "salary"])

joined = df.join(salaries, "id")
joined.select("name", "department", "salary").show()
# Output:
# +-------+-----------+------+
# |   name| department|salary|
# +-------+-----------+------+
# |  Alice|Engineering| 50000|
# |    Bob|      Sales| 60000|
# |Charlie|Engineering| 70000|
# +-------+-----------+------+

# 7. Window Functions
from pyspark.sql.window import Window

window = Window.partitionBy("department").orderBy(col("age").desc())
ranked = joined.withColumn("rank", row_number().over(window))
ranked.select("name", "department", "age", "rank").show()
# Output:
# +-------+-----------+---+----+
# |   name| department|age|rank|
# +-------+-----------+---+----+
# |Charlie|Engineering| 35|   1|
# |  Alice|Engineering| 25|   2|
# |    Bob|      Sales| 30|   1|
# +-------+-----------+---+----+

# 8. Data Quality
null_data = spark.createDataFrame([
    (1, "Alice", None), (2, None, 30), (3, "Charlie", 35)
], ["id", "name", "age"])

# Check nulls
null_counts = null_data.select([
    count(when(col(c).isNull(), c)).alias(f"null_{c}") 
    for c in null_data.columns
])
null_counts.show()
# Output:
# +-------+---------+--------+
# |null_id|null_name|null_age|
# +-------+---------+--------+
# |      0|        1|       1|
# +-------+---------+--------+

# 9. Performance Optimization
df.cache()  # Cache for reuse
df.repartition(2)  # Optimize partitions
print("DataFrame optimized")
# Output: DataFrame optimized

# 10. File Operations
# Write
df.write.mode("overwrite").parquet("output/employees.parquet")
print("Data written to Parquet")
# Output: Data written to Parquet

# Read
read_df = spark.read.parquet("output/employees.parquet")
print(f"Read {read_df.count()} records from Parquet")
# Output: Read 3 records from Parquet

# 11. SQL Interface
df.createOrReplaceTempView("employees")
sql_result = spark.sql("""
    SELECT department, COUNT(*) as count, AVG(age) as avg_age
    FROM employees 
    GROUP BY department
""")
sql_result.show()
# Output:
# +-----------+-----+-------+
# | department|count|avg_age|
# +-----------+-----+-------+
# |Engineering|    2|   30.0|
# |      Sales|    1|   30.0|
# +-----------+-----+-------+

# 12. Streaming (Structured Streaming)
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
    StructField("id", IntegerType()),
    StructField("name", StringType()),
    StructField("value", IntegerType())
])

# Read stream (example with file source)
stream_df = spark.readStream.schema(schema).json("input/stream/")
query = stream_df.writeStream.outputMode("append").format("console").start()
print("Streaming query started")
# Output: Streaming query started

# 13. UDF (User Defined Function)
from pyspark.sql.types import StringType

def categorize_age(age):
    if age < 30:
        return "Young"
    elif age < 40:
        return "Middle"
    else:
        return "Senior"

age_udf = udf(categorize_age, StringType())
df_with_udf = df.withColumn("category", age_udf(col("age")))
df_with_udf.select("name", "age", "category").show()
# Output:
# +-------+---+--------+
# |   name|age|category|
# +-------+---+--------+
# |  Alice| 25|   Young|
# |    Bob| 30|  Middle|
# |Charlie| 35|  Middle|
# +-------+---+--------+

# 14. Error Handling
try:
    invalid_df = spark.read.csv("nonexistent.csv")
    invalid_df.show()
except Exception as e:
    print(f"Error handled: {type(e).__name__}")
# Output: Error handled: AnalysisException

# 15. Resource Management
spark.catalog.clearCache()
spark.stop()
print("Spark session stopped")
# Output: Spark session stopped