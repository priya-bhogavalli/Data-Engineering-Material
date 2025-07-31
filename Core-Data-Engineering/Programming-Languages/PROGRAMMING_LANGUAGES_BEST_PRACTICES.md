# Programming Languages Best Practices for Data Engineering

## Python Best Practices

### 1. Code Organization and Structure

#### Project Structure
```
data_pipeline/
├── src/
│   ├── __init__.py
│   ├── extractors/
│   │   ├── __init__.py
│   │   ├── api_extractor.py
│   │   └── database_extractor.py
│   ├── transformers/
│   │   ├── __init__.py
│   │   └── data_cleaner.py
│   ├── loaders/
│   │   ├── __init__.py
│   │   └── database_loader.py
│   └── utils/
│       ├── __init__.py
│       ├── config.py
│       └── logger.py
├── tests/
├── config/
├── requirements.txt
└── setup.py
```

#### Configuration Management
```python
# config/config.py
import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class DatabaseConfig:
    host: str
    port: int
    database: str
    username: str
    password: str
    
    @classmethod
    def from_env(cls):
        return cls(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 5432)),
            database=os.getenv('DB_NAME'),
            username=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )

@dataclass
class PipelineConfig:
    batch_size: int = 1000
    max_retries: int = 3
    timeout_seconds: int = 300
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]):
        return cls(**config_dict)

# Usage
db_config = DatabaseConfig.from_env()
pipeline_config = PipelineConfig(batch_size=5000)
```

### 2. Error Handling and Logging

#### Robust Error Handling
```python
import logging
import traceback
from functools import wraps
from typing import Optional, Callable, Any

def handle_exceptions(
    default_return: Any = None,
    reraise: bool = False,
    log_error: bool = True
):
    """Decorator for consistent exception handling."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_error:
                    logging.error(f"Error in {func.__name__}: {str(e)}")
                    logging.debug(traceback.format_exc())
                
                if reraise:
                    raise
                
                return default_return
        return wrapper
    return decorator

# Custom exceptions
class DataPipelineError(Exception):
    """Base exception for data pipeline errors."""
    pass

class DataValidationError(DataPipelineError):
    """Raised when data validation fails."""
    pass

class DataExtractionError(DataPipelineError):
    """Raised when data extraction fails."""
    pass

# Usage
@handle_exceptions(default_return=[], log_error=True)
def extract_data_from_api(url: str) -> list:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
```

#### Structured Logging
```python
import logging
import json
from datetime import datetime
from typing import Dict, Any

class StructuredLogger:
    """Structured logging for data pipelines."""
    
    def __init__(self, name: str, level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # JSON formatter
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
            '"logger": "%(name)s", "message": "%(message)s"}'
        )
        
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_pipeline_start(self, pipeline_name: str, config: Dict[str, Any]):
        self.logger.info(json.dumps({
            "event": "pipeline_start",
            "pipeline_name": pipeline_name,
            "config": config,
            "timestamp": datetime.now().isoformat()
        }))
    
    def log_data_quality_check(self, table_name: str, metrics: Dict[str, Any]):
        self.logger.info(json.dumps({
            "event": "data_quality_check",
            "table_name": table_name,
            "metrics": metrics,
            "timestamp": datetime.now().isoformat()
        }))
    
    def log_error(self, error_type: str, error_message: str, context: Dict[str, Any] = None):
        self.logger.error(json.dumps({
            "event": "error",
            "error_type": error_type,
            "error_message": error_message,
            "context": context or {},
            "timestamp": datetime.now().isoformat()
        }))

# Usage
logger = StructuredLogger("data_pipeline")
logger.log_pipeline_start("customer_etl", {"batch_size": 1000})
```

### 3. Data Processing Optimization

#### Memory-Efficient Processing
```python
import pandas as pd
from typing import Iterator, Callable
import gc

def process_large_csv_in_chunks(
    file_path: str,
    chunk_size: int = 10000,
    processor: Callable[[pd.DataFrame], pd.DataFrame] = None
) -> Iterator[pd.DataFrame]:
    """Process large CSV files in chunks to manage memory."""
    
    chunk_reader = pd.read_csv(file_path, chunksize=chunk_size)
    
    for chunk in chunk_reader:
        if processor:
            processed_chunk = processor(chunk)
        else:
            processed_chunk = chunk
        
        yield processed_chunk
        
        # Force garbage collection
        gc.collect()

def optimize_dataframe_memory(df: pd.DataFrame) -> pd.DataFrame:
    """Optimize DataFrame memory usage."""
    
    # Convert object columns to category if beneficial
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / len(df) < 0.5:  # Less than 50% unique values
            df[col] = df[col].astype('category')
    
    # Downcast numeric types
    for col in df.select_dtypes(include=['int']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    
    for col in df.select_dtypes(include=['float']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')
    
    return df

# Usage
def clean_customer_data(chunk: pd.DataFrame) -> pd.DataFrame:
    chunk = chunk.dropna(subset=['customer_id'])
    chunk['email'] = chunk['email'].str.lower()
    return optimize_dataframe_memory(chunk)

for processed_chunk in process_large_csv_in_chunks(
    'large_customer_data.csv',
    chunk_size=50000,
    processor=clean_customer_data
):
    # Process each chunk
    processed_chunk.to_sql('customers', engine, if_exists='append')
```

#### Parallel Processing
```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import cpu_count
import asyncio
import aiohttp
from typing import List

def parallel_api_requests(urls: List[str], max_workers: int = 10) -> List[dict]:
    """Make parallel API requests using ThreadPoolExecutor."""
    
    def fetch_data(url: str) -> dict:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(fetch_data, urls))
    
    return results

async def async_api_requests(urls: List[str]) -> List[dict]:
    """Make asynchronous API requests."""
    
    async def fetch_data(session: aiohttp.ClientSession, url: str) -> dict:
        async with session.get(url) as response:
            return await response.json()
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    
    return results

def parallel_data_processing(data_chunks: List[pd.DataFrame]) -> List[pd.DataFrame]:
    """Process data chunks in parallel using ProcessPoolExecutor."""
    
    def process_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
        # CPU-intensive processing
        return chunk.groupby('category').agg({
            'amount': ['sum', 'mean', 'count'],
            'quantity': 'sum'
        }).reset_index()
    
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        results = list(executor.map(process_chunk, data_chunks))
    
    return results
```

## SQL Best Practices

### 1. Query Optimization

#### Efficient Query Patterns
```sql
-- Use EXISTS instead of IN for better performance
SELECT customer_id, name
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id 
    AND o.order_date >= '2024-01-01'
);

-- Use LIMIT with ORDER BY for pagination
SELECT customer_id, name, email
FROM customers
ORDER BY customer_id
LIMIT 50 OFFSET 100;

-- Use window functions instead of self-joins
SELECT 
    customer_id,
    order_date,
    amount,
    LAG(amount) OVER (PARTITION BY customer_id ORDER BY order_date) as prev_amount,
    SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date 
                      ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_total
FROM orders;

-- Use CTEs for complex queries
WITH customer_metrics AS (
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        SUM(amount) as total_spent,
        AVG(amount) as avg_order_value
    FROM orders
    WHERE order_date >= '2024-01-01'
    GROUP BY customer_id
),
high_value_customers AS (
    SELECT customer_id
    FROM customer_metrics
    WHERE total_spent > 1000
)
SELECT c.name, cm.total_spent, cm.order_count
FROM customers c
JOIN customer_metrics cm ON c.customer_id = cm.customer_id
JOIN high_value_customers hvc ON c.customer_id = hvc.customer_id;
```

#### Index Strategy
```sql
-- Composite indexes for multi-column queries
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- Partial indexes for filtered queries
CREATE INDEX idx_active_customers ON customers(name) WHERE status = 'active';

-- Covering indexes to avoid table lookups
CREATE INDEX idx_orders_covering ON orders(customer_id) 
INCLUDE (order_date, amount, status);

-- Function-based indexes
CREATE INDEX idx_customer_email_lower ON customers(LOWER(email));
```

### 2. Data Quality and Constraints

#### Data Validation
```sql
-- Use CHECK constraints for data validation
ALTER TABLE orders 
ADD CONSTRAINT chk_order_amount CHECK (amount > 0);

ALTER TABLE customers 
ADD CONSTRAINT chk_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

-- Use NOT NULL constraints appropriately
ALTER TABLE orders ALTER COLUMN customer_id SET NOT NULL;
ALTER TABLE orders ALTER COLUMN order_date SET NOT NULL;

-- Use foreign key constraints for referential integrity
ALTER TABLE orders 
ADD CONSTRAINT fk_orders_customer 
FOREIGN KEY (customer_id) REFERENCES customers(customer_id);
```

## PySpark Best Practices

### 1. Performance Optimization

#### Efficient Spark Operations
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Configure Spark for optimal performance
spark = SparkSession.builder \
    .appName("DataEngineering") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.sql.adaptive.skewJoin.enabled", "true") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .getOrCreate()

# Cache frequently used DataFrames
def cache_dataframe_strategically(df, storage_level="MEMORY_AND_DISK"):
    """Cache DataFrame with appropriate storage level."""
    from pyspark import StorageLevel
    
    storage_levels = {
        "MEMORY_ONLY": StorageLevel.MEMORY_ONLY,
        "MEMORY_AND_DISK": StorageLevel.MEMORY_AND_DISK,
        "DISK_ONLY": StorageLevel.DISK_ONLY
    }
    
    return df.persist(storage_levels.get(storage_level, StorageLevel.MEMORY_AND_DISK))

# Optimize joins
def optimize_join_strategy(large_df, small_df, join_key):
    """Optimize join strategy based on DataFrame sizes."""
    
    # Use broadcast join for small DataFrames
    small_df_count = small_df.count()
    
    if small_df_count < 1000000:  # Less than 1M records
        return large_df.join(broadcast(small_df), join_key)
    else:
        # Use bucketing for large-large joins
        return large_df.join(small_df, join_key)

# Efficient aggregations
def efficient_aggregations(df):
    """Perform efficient aggregations."""
    
    # Use built-in functions instead of UDFs
    result = df.groupBy("category") \
        .agg(
            sum("amount").alias("total_amount"),
            avg("amount").alias("avg_amount"),
            count("*").alias("record_count"),
            max("order_date").alias("latest_order")
        )
    
    return result
```

#### Custom UDFs and Performance
```python
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType, IntegerType

# Avoid UDFs when possible - use built-in functions
# Bad: UDF for simple operations
@udf(returnType=StringType())
def extract_domain_udf(email):
    return email.split('@')[1] if '@' in email else None

# Good: Use built-in functions
def extract_domain_builtin(df):
    return df.withColumn(
        "domain",
        regexp_extract(col("email"), r"@(.+)", 1)
    )

# When UDFs are necessary, optimize them
@udf(returnType=IntegerType())
def complex_calculation_udf(value1, value2, value3):
    """Complex business logic that can't be expressed with built-in functions."""
    # Minimize Python object creation
    # Use primitive types when possible
    result = int(value1 * 0.1 + value2 * 0.2 + value3 * 0.7)
    return result

# Vectorized UDFs for better performance (Pandas UDFs)
from pyspark.sql.functions import pandas_udf
import pandas as pd

@pandas_udf(returnType=StringType())
def vectorized_string_processing(emails: pd.Series) -> pd.Series:
    """Vectorized string processing using Pandas UDF."""
    return emails.str.extract(r'@(.+)')[0]
```

### 2. Data Pipeline Patterns

#### Reusable Pipeline Components
```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class SparkTransformer(ABC):
    """Abstract base class for Spark transformations."""
    
    @abstractmethod
    def transform(self, df: DataFrame) -> DataFrame:
        pass

class DataCleaner(SparkTransformer):
    """Clean and standardize data."""
    
    def __init__(self, columns_to_clean: list):
        self.columns_to_clean = columns_to_clean
    
    def transform(self, df: DataFrame) -> DataFrame:
        cleaned_df = df
        
        for column in self.columns_to_clean:
            if column in df.columns:
                cleaned_df = cleaned_df \
                    .withColumn(column, trim(col(column))) \
                    .withColumn(column, when(col(column) == "", None).otherwise(col(column)))
        
        return cleaned_df.dropna(subset=self.columns_to_clean)

class DataValidator(SparkTransformer):
    """Validate data quality."""
    
    def __init__(self, validation_rules: Dict[str, Any]):
        self.validation_rules = validation_rules
    
    def transform(self, df: DataFrame) -> DataFrame:
        validated_df = df
        
        for column, rules in self.validation_rules.items():
            if 'min_value' in rules:
                validated_df = validated_df.filter(col(column) >= rules['min_value'])
            
            if 'max_value' in rules:
                validated_df = validated_df.filter(col(column) <= rules['max_value'])
            
            if 'allowed_values' in rules:
                validated_df = validated_df.filter(col(column).isin(rules['allowed_values']))
        
        return validated_df

# Pipeline orchestration
class SparkPipeline:
    """Orchestrate Spark transformations."""
    
    def __init__(self, transformers: list):
        self.transformers = transformers
    
    def run(self, input_df: DataFrame) -> DataFrame:
        current_df = input_df
        
        for transformer in self.transformers:
            current_df = transformer.transform(current_df)
        
        return current_df

# Usage
pipeline = SparkPipeline([
    DataCleaner(['name', 'email']),
    DataValidator({
        'age': {'min_value': 0, 'max_value': 120},
        'status': {'allowed_values': ['active', 'inactive']}
    })
])

result_df = pipeline.run(input_df)
```

These best practices ensure maintainable, performant, and reliable data engineering code across Python, SQL, and PySpark environments.