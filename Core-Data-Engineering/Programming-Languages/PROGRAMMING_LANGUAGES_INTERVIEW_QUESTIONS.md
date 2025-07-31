# Programming Languages Interview Questions for Data Engineering

## Python for Data Engineering

### Basic Level (0-2 years)

#### 1. What are the key Python libraries used in data engineering?
**Answer:**
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **requests**: HTTP requests for APIs
- **sqlalchemy**: Database ORM
- **boto3**: AWS SDK
- **pyspark**: Apache Spark Python API
- **airflow**: Workflow orchestration
- **great_expectations**: Data quality testing

#### 2. Explain the difference between lists, tuples, and dictionaries in Python.
**Answer:**
```python
# List - mutable, ordered collection
my_list = [1, 2, 3, 4]
my_list.append(5)  # Can modify

# Tuple - immutable, ordered collection
my_tuple = (1, 2, 3, 4)
# my_tuple.append(5)  # Error - cannot modify

# Dictionary - mutable, key-value pairs
my_dict = {'name': 'John', 'age': 30}
my_dict['city'] = 'New York'  # Can modify
```

#### 3. How do you handle exceptions in Python?
**Answer:**
```python
def safe_divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Cannot divide by zero")
        return None
    except TypeError:
        print("Invalid data types")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
    finally:
        print("Division operation completed")
```

### Intermediate Level (2-5 years)

#### 4. Explain Python decorators and their use in data engineering.
**Answer:**
```python
import time
import functools
from datetime import datetime

def timing_decorator(func):
    """Decorator to measure function execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return wrapper

def retry_decorator(max_retries=3, delay=1):
    """Decorator to retry function on failure."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator

# Usage in data engineering
@timing_decorator
@retry_decorator(max_retries=3)
def extract_data_from_api(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
```

#### 5. How do you optimize Python code for large datasets?
**Answer:**
```python
import pandas as pd
import numpy as np
from multiprocessing import Pool
import dask.dataframe as dd

# 1. Use vectorized operations instead of loops
# Slow
def slow_calculation(df):
    result = []
    for index, row in df.iterrows():
        result.append(row['value'] * 2)
    return result

# Fast
def fast_calculation(df):
    return df['value'] * 2

# 2. Use chunking for large files
def process_large_csv(filename, chunk_size=10000):
    results = []
    for chunk in pd.read_csv(filename, chunksize=chunk_size):
        processed_chunk = chunk.groupby('category').sum()
        results.append(processed_chunk)
    return pd.concat(results)

# 3. Use Dask for out-of-core processing
def process_with_dask(filename):
    df = dd.read_csv(filename)
    result = df.groupby('category').value.sum().compute()
    return result

# 4. Parallel processing
def parallel_processing(data_list):
    with Pool() as pool:
        results = pool.map(process_single_item, data_list)
    return results
```

### Advanced Level (5+ years)

#### 6. Implement a data pipeline class with error handling and logging.
**Answer:**
```python
import logging
import traceback
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime

class DataPipelineStage(ABC):
    """Abstract base class for pipeline stages."""
    
    @abstractmethod
    def execute(self, data: Any) -> Any:
        pass
    
    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

class DataPipeline:
    """Data pipeline with error handling and logging."""
    
    def __init__(self, name: str, stages: List[DataPipelineStage]):
        self.name = name
        self.stages = stages
        self.logger = self._setup_logger()
        self.metrics = {
            'start_time': None,
            'end_time': None,
            'records_processed': 0,
            'errors': []
        }
    
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(f"pipeline_{self.name}")
        logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def execute(self, initial_data: Any) -> Optional[Any]:
        """Execute the complete pipeline."""
        self.metrics['start_time'] = datetime.now()
        self.logger.info(f"Starting pipeline: {self.name}")
        
        try:
            current_data = initial_data
            
            for i, stage in enumerate(self.stages):
                stage_name = stage.__class__.__name__
                self.logger.info(f"Executing stage {i+1}: {stage_name}")
                
                # Validate input data
                if not stage.validate(current_data):
                    raise ValueError(f"Data validation failed at stage: {stage_name}")
                
                # Execute stage
                current_data = stage.execute(current_data)
                
                self.logger.info(f"Stage {i+1} completed successfully")
            
            self.metrics['end_time'] = datetime.now()
            self.logger.info(f"Pipeline completed successfully")
            return current_data
            
        except Exception as e:
            self.metrics['end_time'] = datetime.now()
            error_info = {
                'stage': i+1 if 'i' in locals() else 0,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
            self.metrics['errors'].append(error_info)
            self.logger.error(f"Pipeline failed: {e}")
            return None
    
    def get_metrics(self) -> Dict:
        """Get pipeline execution metrics."""
        if self.metrics['start_time'] and self.metrics['end_time']:
            duration = self.metrics['end_time'] - self.metrics['start_time']
            self.metrics['duration_seconds'] = duration.total_seconds()
        
        return self.metrics

# Example implementation
class DataExtractionStage(DataPipelineStage):
    def __init__(self, source_config: Dict):
        self.source_config = source_config
    
    def validate(self, data: Any) -> bool:
        return 'source_path' in self.source_config
    
    def execute(self, data: Any) -> pd.DataFrame:
        return pd.read_csv(self.source_config['source_path'])

class DataTransformationStage(DataPipelineStage):
    def validate(self, data: Any) -> bool:
        return isinstance(data, pd.DataFrame) and not data.empty
    
    def execute(self, data: pd.DataFrame) -> pd.DataFrame:
        # Apply transformations
        cleaned_data = data.dropna()
        cleaned_data['processed_date'] = datetime.now()
        return cleaned_data

# Usage
pipeline = DataPipeline(
    name="customer_data_pipeline",
    stages=[
        DataExtractionStage({'source_path': 'customers.csv'}),
        DataTransformationStage()
    ]
)

result = pipeline.execute(None)
metrics = pipeline.get_metrics()
```

## SQL for Data Engineering

### Basic Level

#### 7. Write a query to find the second highest salary from an employees table.
**Answer:**
```sql
-- Method 1: Using LIMIT and OFFSET
SELECT salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 1;

-- Method 2: Using subquery
SELECT MAX(salary) as second_highest
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);

-- Method 3: Using window function
SELECT DISTINCT salary
FROM (
    SELECT salary, 
           DENSE_RANK() OVER (ORDER BY salary DESC) as rank
    FROM employees
) ranked
WHERE rank = 2;
```

#### 8. Explain the difference between UNION and UNION ALL.
**Answer:**
```sql
-- UNION removes duplicates
SELECT customer_id FROM orders_2023
UNION
SELECT customer_id FROM orders_2024;

-- UNION ALL keeps all records including duplicates
SELECT customer_id FROM orders_2023
UNION ALL
SELECT customer_id FROM orders_2024;
```

### Intermediate Level

#### 9. Write a query to calculate running totals using window functions.
**Answer:**
```sql
SELECT 
    order_date,
    customer_id,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_total,
    AVG(amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) as moving_avg_3_periods
FROM orders
ORDER BY customer_id, order_date;
```

#### 10. How would you optimize a slow-performing query?
**Answer:**
```sql
-- 1. Analyze execution plan
EXPLAIN (ANALYZE, BUFFERS) 
SELECT c.name, COUNT(o.order_id)
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.created_date >= '2024-01-01'
GROUP BY c.name;

-- 2. Add appropriate indexes
CREATE INDEX idx_customers_created_date ON customers(created_date);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- 3. Rewrite query for better performance
-- Instead of LEFT JOIN with COUNT, use EXISTS
SELECT c.name,
       (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.customer_id) as order_count
FROM customers c
WHERE c.created_date >= '2024-01-01';

-- 4. Use covering index
CREATE INDEX idx_customers_covering 
ON customers(created_date) 
INCLUDE (customer_id, name);
```

## PySpark for Data Engineering

### Basic Level

#### 11. Explain the difference between RDD, DataFrame, and Dataset in Spark.
**Answer:**
- **RDD (Resilient Distributed Dataset)**: Low-level API, functional programming
- **DataFrame**: Higher-level API with schema, SQL-like operations
- **Dataset**: Type-safe version of DataFrame (Scala/Java)

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum

spark = SparkSession.builder.appName("DataEngineering").getOrCreate()

# RDD example
rdd = spark.sparkContext.parallelize([1, 2, 3, 4, 5])
squared_rdd = rdd.map(lambda x: x ** 2)

# DataFrame example
df = spark.read.csv("data.csv", header=True, inferSchema=True)
result_df = df.filter(col("amount") > 100).groupBy("category").agg(spark_sum("amount"))
```

### Intermediate Level

#### 12. How do you handle skewed data in Spark?
**Answer:**
```python
from pyspark.sql.functions import rand, floor, concat, lit

def handle_skewed_join(large_df, small_df, join_key, salt_factor=10):
    """Handle skewed joins using salting technique."""
    
    # Add salt to large dataset
    salted_large = large_df.withColumn(
        "salt", floor(rand() * salt_factor)
    ).withColumn(
        "salted_key", concat(col(join_key), lit("_"), col("salt"))
    )
    
    # Replicate small dataset
    salt_range = spark.range(salt_factor).select(col("id").alias("salt"))
    salted_small = small_df.crossJoin(salt_range).withColumn(
        "salted_key", concat(col(join_key), lit("_"), col("salt"))
    )
    
    # Perform join on salted key
    result = salted_large.join(salted_small, "salted_key").drop("salt", "salted_key")
    
    return result

# Alternative: Use broadcast join for small tables
from pyspark.sql.functions import broadcast
result = large_df.join(broadcast(small_df), join_key)
```

### Advanced Level

#### 13. Implement a custom data source reader in PySpark.
**Answer:**
```python
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
import requests
import json

class APIDataSource:
    """Custom data source to read from REST API."""
    
    def __init__(self, spark_session):
        self.spark = spark_session
    
    def read_api_data(self, api_url, headers=None, params=None):
        """Read data from API and convert to DataFrame."""
        
        # Define schema
        schema = StructType([
            StructField("id", IntegerType(), True),
            StructField("name", StringType(), True),
            StructField("email", StringType(), True),
            StructField("created_at", StringType(), True)
        ])
        
        try:
            # Fetch data from API
            response = requests.get(api_url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Convert to DataFrame
            if isinstance(data, list):
                df = self.spark.createDataFrame(data, schema)
            else:
                # Handle paginated responses
                df = self._handle_paginated_response(api_url, headers, params, schema)
            
            return df
            
        except Exception as e:
            print(f"Error reading from API: {e}")
            return self.spark.createDataFrame([], schema)
    
    def _handle_paginated_response(self, base_url, headers, params, schema):
        """Handle paginated API responses."""
        all_data = []
        page = 1
        
        while True:
            paginated_params = params.copy() if params else {}
            paginated_params['page'] = page
            
            response = requests.get(base_url, headers=headers, params=paginated_params)
            response.raise_for_status()
            
            page_data = response.json()
            
            if not page_data.get('data'):
                break
                
            all_data.extend(page_data['data'])
            
            if not page_data.get('has_next_page'):
                break
                
            page += 1
        
        return self.spark.createDataFrame(all_data, schema)

# Usage
api_source = APIDataSource(spark)
df = api_source.read_api_data(
    "https://api.example.com/users",
    headers={"Authorization": "Bearer token"},
    params={"limit": 100}
)
```

These questions cover the essential programming concepts needed for data engineering roles, focusing on practical applications and real-world scenarios.