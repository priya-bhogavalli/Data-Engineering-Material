# Data Processing Key Concepts for Data Engineering

## 1. Batch vs Stream Processing
**What they are**: Two fundamental paradigms for processing data with different timing characteristics.

**Batch Processing**:
- Processes large volumes of data at scheduled intervals
- Higher latency but higher throughput
- Suitable for historical analysis, ETL jobs, reporting

**Stream Processing**:
- Processes data in real-time as it arrives
- Lower latency but potentially lower throughput
- Suitable for real-time analytics, monitoring, alerts

```python
# Batch processing example with Apache Spark
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("BatchProcessing").getOrCreate()

# Read large dataset
df = spark.read.parquet("s3://data-lake/sales/2024/")

# Process in batches
daily_sales = df.groupBy("date", "region") \
    .agg({"amount": "sum", "quantity": "sum"}) \
    .orderBy("date")

# Write results
daily_sales.write.mode("overwrite").parquet("s3://data-warehouse/daily_sales/")

# Stream processing example with Kafka
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'user-events',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Process events in real-time
for message in consumer:
    event = message.value
    
    # Real-time processing
    if event['event_type'] == 'purchase':
        update_user_profile(event['user_id'], event['amount'])
        send_recommendation(event['user_id'])
        
    elif event['event_type'] == 'fraud_alert':
        trigger_immediate_alert(event)
```

## 2. ETL vs ELT
**What they are**: Two approaches to data integration with different transformation timing.

**ETL (Extract, Transform, Load)**:
- Transform data before loading into target system
- Suitable for structured data and predefined transformations
- Traditional data warehousing approach

**ELT (Extract, Load, Transform)**:
- Load raw data first, then transform in target system
- Leverages target system's processing power
- Modern data lake approach

```python
# ETL Example
class ETLPipeline:
    def extract(self, source):
        """Extract data from source system"""
        return source.get_data()
    
    def transform(self, raw_data):
        """Transform data before loading"""
        # Clean data
        cleaned_data = self.clean_data(raw_data)
        
        # Apply business rules
        transformed_data = self.apply_business_rules(cleaned_data)
        
        # Aggregate data
        aggregated_data = self.aggregate_data(transformed_data)
        
        return aggregated_data
    
    def load(self, transformed_data, target):
        """Load transformed data to target"""
        target.insert_data(transformed_data)

# ELT Example
class ELTPipeline:
    def extract_and_load(self, source, target):
        """Extract and load raw data"""
        raw_data = source.get_data()
        target.insert_raw_data(raw_data)
    
    def transform_in_target(self, target):
        """Transform data in target system"""
        target.execute_sql("""
            CREATE TABLE transformed_sales AS
            SELECT 
                customer_id,
                DATE_TRUNC('month', order_date) as month,
                SUM(amount) as total_amount,
                COUNT(*) as order_count
            FROM raw_sales
            WHERE order_date >= '2024-01-01'
            GROUP BY customer_id, DATE_TRUNC('month', order_date)
        """)
```

## 3. Data Partitioning Strategies
**What it is**: Dividing large datasets into smaller, manageable chunks for parallel processing.

**Types**:
- **Range Partitioning**: Based on value ranges
- **Hash Partitioning**: Based on hash function
- **Round-Robin**: Evenly distributed
- **Custom Partitioning**: Business logic based

```python
# Spark DataFrame partitioning
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month

spark = SparkSession.builder.appName("Partitioning").getOrCreate()

# Read data
df = spark.read.parquet("s3://raw-data/transactions/")

# Range partitioning by date
df_partitioned = df.repartition(col("transaction_date"))

# Hash partitioning by customer_id
df_hash_partitioned = df.repartition(200, col("customer_id"))

# Custom partitioning function
def custom_partitioner(key):
    if key.startswith('VIP'):
        return 0  # VIP customers to partition 0
    elif key.startswith('PREMIUM'):
        return 1  # Premium customers to partition 1
    else:
        return hash(key) % 10  # Regular customers distributed

# Write with partitioning
df.write \
  .partitionBy("year", "month") \
  .mode("overwrite") \
  .parquet("s3://processed-data/transactions/")

# Partition pruning for efficient queries
filtered_df = spark.read.parquet("s3://processed-data/transactions/") \
    .filter((col("year") == 2024) & (col("month") == 1))
```

## 4. Data Serialization Formats
**What they are**: Methods to convert data structures into formats suitable for storage or transmission.

**Common Formats**:
- **JSON**: Human-readable, schema-flexible
- **Avro**: Schema evolution, compact binary
- **Parquet**: Columnar, optimized for analytics
- **ORC**: Optimized Row Columnar

```python
# Working with different serialization formats
import json
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from fastavro import writer, reader, parse_schema

# JSON serialization
data = {'customer_id': 123, 'name': 'John Doe', 'orders': [1, 2, 3]}
json_str = json.dumps(data)
parsed_data = json.loads(json_str)

# Parquet with pandas
df = pd.DataFrame({
    'customer_id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'amount': [100.0, 200.0, 150.0]
})

# Write to Parquet
df.to_parquet('customers.parquet', compression='snappy')

# Read from Parquet
df_read = pd.read_parquet('customers.parquet')

# Avro schema and serialization
avro_schema = {
    "type": "record",
    "name": "Customer",
    "fields": [
        {"name": "customer_id", "type": "int"},
        {"name": "name", "type": "string"},
        {"name": "email", "type": ["null", "string"], "default": None}
    ]
}

# Write Avro
records = [
    {"customer_id": 1, "name": "Alice", "email": "alice@example.com"},
    {"customer_id": 2, "name": "Bob", "email": None}
]

with open('customers.avro', 'wb') as out:
    writer(out, parse_schema(avro_schema), records)

# Read Avro
with open('customers.avro', 'rb') as fo:
    for record in reader(fo):
        print(record)
```

## 5. Data Quality and Validation
**What it is**: Ensuring data meets quality standards and business requirements.

**Quality Dimensions**:
- **Completeness**: No missing values
- **Accuracy**: Correct values
- **Consistency**: Same format across sources
- **Timeliness**: Data is current
- **Validity**: Conforms to business rules

```python
# Data quality framework
import pandas as pd
from typing import Dict, List, Any

class DataQualityChecker:
    def __init__(self):
        self.quality_rules = []
    
    def add_completeness_check(self, columns: List[str], threshold: float = 0.95):
        """Check for missing values"""
        def check(df):
            results = {}
            for col in columns:
                completeness = df[col].notna().sum() / len(df)
                results[f"{col}_completeness"] = {
                    "passed": completeness >= threshold,
                    "score": completeness,
                    "threshold": threshold
                }
            return results
        
        self.quality_rules.append(("completeness", check))
    
    def add_uniqueness_check(self, columns: List[str]):
        """Check for duplicate values"""
        def check(df):
            results = {}
            for col in columns:
                unique_ratio = df[col].nunique() / len(df)
                results[f"{col}_uniqueness"] = {
                    "passed": unique_ratio == 1.0,
                    "score": unique_ratio,
                    "duplicates": len(df) - df[col].nunique()
                }
            return results
        
        self.quality_rules.append(("uniqueness", check))
    
    def add_range_check(self, column: str, min_val: float, max_val: float):
        """Check value ranges"""
        def check(df):
            in_range = df[column].between(min_val, max_val).sum()
            total = len(df)
            score = in_range / total if total > 0 else 0
            
            return {
                f"{column}_range": {
                    "passed": score == 1.0,
                    "score": score,
                    "violations": total - in_range,
                    "range": f"[{min_val}, {max_val}]"
                }
            }
        
        self.quality_rules.append(("range", check))
    
    def run_checks(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Run all quality checks"""
        all_results = {}
        
        for rule_type, check_func in self.quality_rules:
            try:
                results = check_func(df)
                all_results.update(results)
            except Exception as e:
                all_results[f"{rule_type}_error"] = str(e)
        
        # Calculate overall quality score
        passed_checks = sum(1 for r in all_results.values() 
                          if isinstance(r, dict) and r.get("passed", False))
        total_checks = len([r for r in all_results.values() if isinstance(r, dict)])
        
        overall_score = passed_checks / total_checks if total_checks > 0 else 0
        
        return {
            "overall_quality_score": overall_score,
            "detailed_results": all_results
        }

# Usage
quality_checker = DataQualityChecker()
quality_checker.add_completeness_check(['customer_id', 'email'], threshold=0.95)
quality_checker.add_uniqueness_check(['customer_id'])
quality_checker.add_range_check('age', 0, 120)

# Run checks on data
df = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5],
    'email': ['a@test.com', 'b@test.com', None, 'd@test.com', 'e@test.com'],
    'age': [25, 30, 35, 150, 28]  # 150 is out of range
})

results = quality_checker.run_checks(df)
print(f"Overall Quality Score: {results['overall_quality_score']:.2%}")
```

## 6. Error Handling and Recovery
**What it is**: Strategies to handle failures and ensure data processing reliability.

```python
# Robust error handling in data pipelines
import logging
import time
from functools import wraps
from typing import Callable, Any

class DataProcessingError(Exception):
    """Custom exception for data processing errors"""
    pass

def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """Decorator for retrying failed operations"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logging.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        logging.error(f"All {max_retries} attempts failed")
            
            raise last_exception
        return wrapper
    return decorator

class RobustDataProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.failed_records = []
    
    @retry_on_failure(max_retries=3, delay=2.0)
    def process_batch(self, data_batch):
        """Process a batch of data with error handling"""
        processed_records = []
        
        for record in data_batch:
            try:
                processed_record = self.process_single_record(record)
                processed_records.append(processed_record)
                
            except Exception as e:
                self.logger.error(f"Failed to process record {record.get('id', 'unknown')}: {e}")
                
                # Store failed record for later processing
                self.failed_records.append({
                    'record': record,
                    'error': str(e),
                    'timestamp': time.time()
                })
                
                # Continue processing other records
                continue
        
        return processed_records
    
    def process_single_record(self, record):
        """Process individual record with validation"""
        # Validate required fields
        required_fields = ['id', 'timestamp', 'value']
        for field in required_fields:
            if field not in record:
                raise DataProcessingError(f"Missing required field: {field}")
        
        # Business logic processing
        processed_record = {
            'id': record['id'],
            'processed_timestamp': time.time(),
            'original_value': record['value'],
            'processed_value': self.transform_value(record['value'])
        }
        
        return processed_record
    
    def transform_value(self, value):
        """Transform value with error handling"""
        try:
            # Example transformation
            if isinstance(value, str):
                return float(value) * 1.1
            elif isinstance(value, (int, float)):
                return value * 1.1
            else:
                raise ValueError(f"Cannot transform value of type {type(value)}")
        except ValueError as e:
            raise DataProcessingError(f"Value transformation failed: {e}")
    
    def retry_failed_records(self):
        """Retry processing failed records"""
        if not self.failed_records:
            return []
        
        retry_records = self.failed_records.copy()
        self.failed_records.clear()
        
        successful_retries = []
        for failed_record in retry_records:
            try:
                processed = self.process_single_record(failed_record['record'])
                successful_retries.append(processed)
                self.logger.info(f"Successfully retried record {failed_record['record']['id']}")
            except Exception as e:
                # Still failing, add back to failed records
                self.failed_records.append(failed_record)
                self.logger.error(f"Retry failed for record {failed_record['record']['id']}: {e}")
        
        return successful_retries

# Usage
processor = RobustDataProcessor()

# Sample data with some problematic records
sample_data = [
    {'id': 1, 'timestamp': '2024-01-01', 'value': '100.5'},
    {'id': 2, 'timestamp': '2024-01-01', 'value': 'invalid'},  # Will fail
    {'id': 3, 'timestamp': '2024-01-01'},  # Missing 'value' field
    {'id': 4, 'timestamp': '2024-01-01', 'value': 200.0}
]

# Process batch
processed = processor.process_batch(sample_data)
print(f"Successfully processed {len(processed)} records")
print(f"Failed records: {len(processor.failed_records)}")

# Retry failed records
retried = processor.retry_failed_records()
print(f"Successfully retried {len(retried)} records")
```

## 7. Performance Optimization
**What it is**: Techniques to improve data processing speed and resource utilization.

```python
# Performance optimization techniques
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import pandas as pd
import numpy as np

class PerformanceOptimizer:
    def __init__(self):
        self.cpu_count = mp.cpu_count()
    
    def parallel_processing(self, data_chunks, process_func, use_processes=True):
        """Process data chunks in parallel"""
        if use_processes:
            # CPU-bound tasks
            with ProcessPoolExecutor(max_workers=self.cpu_count) as executor:
                results = list(executor.map(process_func, data_chunks))
        else:
            # I/O-bound tasks
            with ThreadPoolExecutor(max_workers=self.cpu_count * 2) as executor:
                results = list(executor.map(process_func, data_chunks))
        
        return results
    
    def vectorized_operations(self, df):
        """Use vectorized operations instead of loops"""
        # Slow: iterating through rows
        # for index, row in df.iterrows():
        #     df.at[index, 'result'] = row['value'] * 2 + 1
        
        # Fast: vectorized operation
        df['result'] = df['value'] * 2 + 1
        
        return df
    
    def memory_efficient_processing(self, file_path, chunk_size=10000):
        """Process large files in chunks"""
        results = []
        
        for chunk in pd.read_csv(file_path, chunksize=chunk_size):
            # Process chunk
            processed_chunk = self.process_chunk(chunk)
            results.append(processed_chunk)
            
            # Optional: write intermediate results to avoid memory issues
            # processed_chunk.to_csv(f'temp_chunk_{len(results)}.csv', index=False)
        
        # Combine results
        final_result = pd.concat(results, ignore_index=True)
        return final_result
    
    def process_chunk(self, chunk):
        """Process individual chunk efficiently"""
        # Use vectorized operations
        chunk['processed_value'] = chunk['value'].apply(lambda x: x * 1.1 if pd.notna(x) else 0)
        
        # Use built-in pandas functions
        chunk['category'] = pd.cut(chunk['value'], bins=[0, 50, 100, float('inf')], 
                                 labels=['low', 'medium', 'high'])
        
        return chunk
    
    def optimize_data_types(self, df):
        """Optimize data types to reduce memory usage"""
        # Convert object columns to category if cardinality is low
        for col in df.select_dtypes(include=['object']):
            if df[col].nunique() / len(df) < 0.5:  # Less than 50% unique values
                df[col] = df[col].astype('category')
        
        # Downcast numeric types
        for col in df.select_dtypes(include=['int64']):
            df[col] = pd.to_numeric(df[col], downcast='integer')
        
        for col in df.select_dtypes(include=['float64']):
            df[col] = pd.to_numeric(df[col], downcast='float')
        
        return df

# Usage example
optimizer = PerformanceOptimizer()

# Create sample data
sample_df = pd.DataFrame({
    'id': range(100000),
    'value': np.random.randn(100000),
    'category': np.random.choice(['A', 'B', 'C'], 100000)
})

# Optimize data types
optimized_df = optimizer.optimize_data_types(sample_df)

# Vectorized processing
processed_df = optimizer.vectorized_operations(optimized_df)

print(f"Original memory usage: {sample_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
print(f"Optimized memory usage: {optimized_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
```

These data processing concepts provide the foundation for building efficient, reliable, and scalable data engineering pipelines.