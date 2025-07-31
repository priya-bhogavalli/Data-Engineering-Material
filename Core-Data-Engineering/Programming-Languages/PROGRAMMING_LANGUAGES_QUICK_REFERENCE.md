# Programming Languages Quick Reference

## Python Essentials

### Data Structures
```python
# Lists
my_list = [1, 2, 3, 4]
my_list.append(5)
my_list.extend([6, 7])
my_list.remove(3)

# Dictionaries
my_dict = {'name': 'John', 'age': 30}
my_dict['city'] = 'New York'
my_dict.get('salary', 0)

# Sets
my_set = {1, 2, 3, 4}
my_set.add(5)
my_set.update([6, 7])

# Tuples
my_tuple = (1, 2, 3)
```

### List Comprehensions
```python
# Basic list comprehension
squares = [x**2 for x in range(10)]

# With condition
evens = [x for x in range(20) if x % 2 == 0]

# Dictionary comprehension
word_lengths = {word: len(word) for word in ['hello', 'world']}

# Set comprehension
unique_lengths = {len(word) for word in ['hello', 'world', 'hello']}
```

### Functions and Decorators
```python
# Function with default arguments
def process_data(data, format='json', validate=True):
    if validate:
        # validation logic
        pass
    return data

# Lambda functions
multiply = lambda x, y: x * y
sorted_data = sorted(data, key=lambda x: x['timestamp'])

# Decorators
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Execution time: {time.time() - start}")
        return result
    return wrapper

@timing_decorator
def slow_function():
    time.sleep(1)
```

### File I/O
```python
# Reading files
with open('data.txt', 'r') as file:
    content = file.read()

# Writing files
with open('output.txt', 'w') as file:
    file.write('Hello, World!')

# JSON operations
import json
with open('data.json', 'r') as file:
    data = json.load(file)

with open('output.json', 'w') as file:
    json.dump(data, file, indent=2)
```

### Pandas Essentials
```python
import pandas as pd

# Creating DataFrames
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
df = pd.read_csv('data.csv')

# Basic operations
df.head()
df.info()
df.describe()
df.shape

# Filtering
df[df['column'] > 5]
df.query('column > 5')

# Grouping
df.groupby('category').sum()
df.groupby('category').agg({'amount': ['sum', 'mean']})

# Merging
pd.merge(df1, df2, on='key')
df1.join(df2, on='key')
```

## SQL Essentials

### Basic Queries
```sql
-- SELECT
SELECT column1, column2 FROM table_name;
SELECT * FROM table_name WHERE condition;
SELECT DISTINCT column FROM table_name;

-- Filtering
SELECT * FROM customers WHERE age > 25;
SELECT * FROM orders WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31';
SELECT * FROM products WHERE name LIKE '%phone%';
SELECT * FROM customers WHERE city IN ('New York', 'London');

-- Sorting
SELECT * FROM customers ORDER BY age DESC;
SELECT * FROM orders ORDER BY customer_id, order_date;
```

### Joins
```sql
-- INNER JOIN
SELECT c.name, o.order_date
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;

-- LEFT JOIN
SELECT c.name, o.order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;

-- Multiple joins
SELECT c.name, o.order_date, p.product_name
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id;
```

### Aggregations
```sql
-- Basic aggregations
SELECT COUNT(*) FROM customers;
SELECT AVG(amount) FROM orders;
SELECT SUM(amount) FROM orders WHERE order_date >= '2024-01-01';

-- GROUP BY
SELECT customer_id, COUNT(*) as order_count, SUM(amount) as total
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 5;

-- Window functions
SELECT 
    customer_id,
    order_date,
    amount,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as order_sequence,
    SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date) as running_total
FROM orders;
```

### Common Table Expressions (CTEs)
```sql
WITH customer_summary AS (
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        SUM(amount) as total_amount
    FROM orders
    GROUP BY customer_id
)
SELECT c.name, cs.order_count, cs.total_amount
FROM customers c
JOIN customer_summary cs ON c.customer_id = cs.customer_id
WHERE cs.total_amount > 1000;
```

## PySpark Essentials

### SparkSession
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Create SparkSession
spark = SparkSession.builder \
    .appName("DataEngineering") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()
```

### DataFrame Operations
```python
# Reading data
df = spark.read.csv("data.csv", header=True, inferSchema=True)
df = spark.read.parquet("data.parquet")
df = spark.read.table("database.table")

# Basic operations
df.show()
df.printSchema()
df.count()
df.columns

# Selecting and filtering
df.select("col1", "col2")
df.filter(col("amount") > 100)
df.where(col("status") == "active")

# Adding columns
df.withColumn("new_col", col("old_col") * 2)
df.withColumnRenamed("old_name", "new_name")

# Grouping and aggregating
df.groupBy("category").agg(
    sum("amount").alias("total"),
    avg("amount").alias("average"),
    count("*").alias("count")
)
```

### Joins and Unions
```python
# Joins
df1.join(df2, "common_column", "inner")
df1.join(df2, df1.id == df2.customer_id, "left")

# Broadcast join for small tables
from pyspark.sql.functions import broadcast
large_df.join(broadcast(small_df), "key")

# Union
df1.union(df2)
df1.unionByName(df2)
```

### Window Functions
```python
from pyspark.sql.window import Window

# Define window specification
window_spec = Window.partitionBy("customer_id").orderBy("order_date")

# Apply window functions
df.withColumn("row_number", row_number().over(window_spec)) \
  .withColumn("running_total", sum("amount").over(window_spec)) \
  .withColumn("lag_amount", lag("amount", 1).over(window_spec))
```

### UDFs (User Defined Functions)
```python
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

# Regular UDF
def extract_domain(email):
    return email.split('@')[1] if '@' in email else None

extract_domain_udf = udf(extract_domain, StringType())
df.withColumn("domain", extract_domain_udf(col("email")))

# Pandas UDF (vectorized)
from pyspark.sql.functions import pandas_udf
import pandas as pd

@pandas_udf(returnType=StringType())
def extract_domain_pandas(emails: pd.Series) -> pd.Series:
    return emails.str.split('@').str[1]

df.withColumn("domain", extract_domain_pandas(col("email")))
```

### Writing Data
```python
# Write to different formats
df.write.mode("overwrite").csv("output.csv", header=True)
df.write.mode("append").parquet("output.parquet")
df.write.mode("overwrite").saveAsTable("database.table")

# Partitioned writes
df.write.partitionBy("year", "month").parquet("partitioned_output")

# Write with options
df.write \
  .option("compression", "gzip") \
  .mode("overwrite") \
  .parquet("compressed_output")
```

## Common Patterns

### Error Handling
```python
# Python
try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Specific error: {e}")
    handle_specific_error()
except Exception as e:
    logger.error(f"General error: {e}")
    handle_general_error()
finally:
    cleanup()

# PySpark
try:
    df = spark.read.csv("data.csv")
    df.show()
except Exception as e:
    print(f"Error reading CSV: {e}")
    df = spark.createDataFrame([], schema)
```

### Configuration Management
```python
# Using environment variables
import os
DATABASE_URL = os.getenv('DATABASE_URL', 'default_url')

# Using config files
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
db_host = config['database']['host']

# Using dataclasses
from dataclasses import dataclass

@dataclass
class Config:
    database_url: str
    batch_size: int = 1000
    max_retries: int = 3
```

### Logging
```python
import logging

# Basic logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("Processing started")
logger.error("An error occurred")

# Structured logging
import json
logger.info(json.dumps({
    "event": "data_processed",
    "records": 1000,
    "duration": 45.2
}))
```

### Testing
```python
import pytest
import pandas as pd

def test_data_transformation():
    # Arrange
    input_data = pd.DataFrame({'value': [1, 2, 3]})
    expected = pd.DataFrame({'value': [2, 4, 6]})
    
    # Act
    result = transform_data(input_data)
    
    # Assert
    pd.testing.assert_frame_equal(result, expected)

# PySpark testing
def test_spark_transformation(spark):
    # Create test DataFrame
    test_data = [(1, "A"), (2, "B")]
    df = spark.createDataFrame(test_data, ["id", "category"])
    
    # Apply transformation
    result = df.filter(col("id") > 1)
    
    # Assert
    assert result.count() == 1
```