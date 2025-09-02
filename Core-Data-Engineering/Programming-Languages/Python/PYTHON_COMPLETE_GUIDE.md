# Python Complete Guide for Data Engineers

## 🎯 **Overview**
Python is the primary programming language for data engineering, offering powerful libraries, clean syntax, and excellent ecosystem support. This comprehensive guide covers everything from fundamentals to advanced production patterns specifically tailored for data engineering applications.

**What You'll Learn:**
- Core Python concepts and data structures
- Object-oriented programming for data systems
- Performance optimization techniques
- Error handling and logging best practices
- Concurrency and parallelism patterns
- Production deployment strategies
- Data engineering specific patterns

**Target Audience:**
- Data Engineers (1-10+ years experience)
- Software Engineers transitioning to data
- Data Scientists needing production skills
- DevOps Engineers working with data systems

## 📋 Table of Contents

1. [Core Data Structures](#1-core-data-structures)
2. [Functions and Decorators](#2-functions-and-decorators)
3. [Object-Oriented Programming](#3-object-oriented-programming)
4. [Error Handling](#4-error-handling)
5. [File I/O and Data Formats](#5-file-io-and-data-formats)
6. [Generators and Iterators](#6-generators-and-iterators)
7. [Context Managers](#7-context-managers)
8. [Concurrency and Parallelism](#8-concurrency-and-parallelism)
9. [Performance Optimization](#9-performance-optimization)
10. [Production Best Practices](#10-production-best-practices)

---

## 1. Core Data Structures

### Lists - Dynamic Arrays
**When to use**: Ordered data that needs modification, data processing pipelines

```python
# Data Engineering Examples
transaction_ids = [1001, 1002, 1003, 1004, 1005]

# Adding new transactions
transaction_ids.append(1006)
transaction_ids.extend([1007, 1008, 1009])

# Data transformation with list comprehensions
api_ready_ids = [f"TXN_{id}" for id in transaction_ids]
high_value_txns = [id for id in transaction_ids if id > 1005]

# Performance: List comprehensions are 2-3x faster than loops
# Critical when processing millions of records
```

### Dictionaries - Hash Maps
**When to use**: Key-value lookups, configuration, caching, data indexing

```python
# Configuration management
pipeline_config = {
    'source_database': 'postgresql://prod-db:5432/sales',
    'target_warehouse': 's3://data-lake/processed/',
    'batch_size': 10000,
    'retry_attempts': 3
}

# O(1) customer lookup for real-time transactions
customer_data = {
    'CUST001': {'name': 'John Doe', 'tier': 'Premium', 'credit_limit': 50000},
    'CUST002': {'name': 'Jane Smith', 'tier': 'Gold', 'credit_limit': 25000}
}

customer_info = customer_data.get('CUST001', {'tier': 'Basic', 'credit_limit': 1000})

# Dictionary comprehensions for data transformation
squared_amounts = {txn_id: amount**2 for txn_id, amount in transaction_amounts.items()}
```

### Sets - Unique Collections
**When to use**: Deduplication, membership testing, set operations

```python
# Data deduplication
unique_customer_ids = set(all_customer_ids)

# Fast membership testing O(1) vs O(n) for lists
valid_statuses = {'active', 'pending', 'suspended'}
if customer_status in valid_statuses:
    process_customer()

# Set operations for data analysis
customers_2023 = {1, 2, 3, 4, 5}
customers_2024 = {3, 4, 5, 6, 7}
returning_customers = customers_2023 & customers_2024  # Intersection
new_customers = customers_2024 - customers_2023       # Difference
```

### Tuples - Immutable Sequences
**When to use**: Fixed data structures, function returns, database records

```python
# Database record representation
user_record = ('john_doe', 'john@example.com', 25, 'active')

# Named tuples for structured data
from collections import namedtuple
DataPoint = namedtuple('DataPoint', ['timestamp', 'value', 'source'])
data_point = DataPoint('2023-01-01', 42.5, 'sensor_1')

# Function returns
def get_statistics(data):
    return (min(data), max(data), sum(data)/len(data))

min_val, max_val, avg_val = get_statistics(transaction_amounts)
```

---

## 2. Functions and Decorators

### Function Design Patterns
```python
def process_data(data, transform_func=None, **kwargs):
    """Process data with optional transformation and flexible configuration."""
    if transform_func:
        data = transform_func(data)
    
    batch_size = kwargs.get('batch_size', 1000)
    debug = kwargs.get('debug', False)
    
    if debug:
        print(f"Processing {len(data)} records in batches of {batch_size}")
    
    return data

# Lambda functions for simple operations
multiply = lambda x, y: x * y
filter_positive = lambda x: x > 0
```

### Decorators for Data Engineering
```python
import time
import functools
from typing import Callable, Any

def timing_decorator(func: Callable) -> Callable:
    """Measure function execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

def retry_decorator(max_attempts: int = 3, delay: float = 1.0):
    """Retry function on failure with configurable parameters."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator

@timing_decorator
@retry_decorator(max_attempts=3, delay=2.0)
def fetch_data_from_api(url: str):
    # API call implementation
    pass
```

### Caching Decorator
```python
def cache_results(max_size: int = 128):
    """Simple caching decorator with size limit."""
    def decorator(func: Callable) -> Callable:
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(sorted(kwargs.items()))
            
            if key in cache:
                print(f"Cache hit for {func.__name__}")
                return cache[key]
            
            result = func(*args, **kwargs)
            
            if len(cache) >= max_size:
                oldest_key = next(iter(cache))
                del cache[oldest_key]
            
            cache[key] = result
            return result
        
        wrapper.cache_info = lambda: {'size': len(cache), 'max_size': max_size}
        wrapper.cache_clear = lambda: cache.clear()
        return wrapper
    return decorator

@cache_results(max_size=10)
def expensive_calculation(n: int) -> int:
    """Simulate expensive computation."""
    time.sleep(0.1)
    return sum(i**2 for i in range(n))
```

---

## 3. Object-Oriented Programming

### Class Design for Data Systems
```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class DataProcessor:
    """Base data processor with configurable settings."""
    
    def __init__(self, name: str, source_type: str):
        self.name = name
        self.source_type = source_type
        self.processed_count = 0
        self.errors = []
    
    def process_batch(self, data: list) -> list:
        """Process a batch of data."""
        try:
            processed_data = [item * 2 for item in data if isinstance(item, (int, float))]
            self.processed_count += len(processed_data)
            return processed_data
        except Exception as e:
            self.errors.append(str(e))
            return []
    
    def get_stats(self) -> dict:
        """Get processing statistics."""
        return {
            'name': self.name,
            'source_type': self.source_type,
            'processed_count': self.processed_count,
            'error_count': len(self.errors)
        }
```

### Inheritance and Polymorphism
```python
# Abstract base class for data sources
class DataSource(ABC):
    """Base class for all data sources."""
    
    def __init__(self, name: str, connection_string: str):
        self.name = name
        self.connection_string = connection_string
        self.is_connected = False
        self.records_processed = 0
    
    @abstractmethod
    def connect(self) -> bool:
        """Connect to data source."""
        pass
    
    @abstractmethod
    def read_data(self, limit: int = None) -> List[Dict[str, Any]]:
        """Read data from source."""
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return {
            'name': self.name,
            'connected': self.is_connected,
            'records_processed': self.records_processed
        }

# Concrete implementations
class CSVDataSource(DataSource):
    """Specialized data source for CSV files."""
    
    def __init__(self, name: str, file_path: str, delimiter: str = ','):
        super().__init__(name, file_path)
        self.delimiter = delimiter
        self.headers = []
    
    def connect(self) -> bool:
        """Connect to CSV file."""
        print(f"Reading CSV headers from {self.connection_string}")
        self.headers = ['id', 'name', 'amount', 'date']
        self.is_connected = True
        return True
    
    def read_data(self, limit: int = None) -> List[Dict[str, str]]:
        """Read CSV data."""
        if not self.is_connected:
            raise ConnectionError("Not connected to data source")
        
        data = [
            {'id': '1', 'name': 'John', 'amount': '100.50', 'date': '2024-01-01'},
            {'id': '2', 'name': 'Jane', 'amount': '250.75', 'date': '2024-01-02'}
        ]
        
        if limit:
            data = data[:limit]
        
        self.records_processed += len(data)
        return data

class DatabaseSource(DataSource):
    """Specialized data source for databases."""
    
    def __init__(self, name: str, connection_string: str, table_name: str):
        super().__init__(name, connection_string)
        self.table_name = table_name
        self.query_cache = {}
    
    def connect(self) -> bool:
        """Connect to database."""
        print(f"Establishing database connection pool")
        self.is_connected = True
        return True
    
    def read_data(self, limit: int = None) -> List[Dict[str, Any]]:
        """Execute query and return data."""
        if not self.is_connected:
            raise ConnectionError("Database not connected")
        
        result = [
            {'customer_id': 1, 'total_orders': 5, 'total_amount': 1250.00},
            {'customer_id': 2, 'total_orders': 3, 'total_amount': 750.50}
        ]
        
        self.records_processed += len(result)
        return result
```

### Encapsulation and Properties
```python
class DatabaseConnection:
    """Encapsulated database connection with controlled access."""
    
    def __init__(self, host: str, port: int, database: str):
        self.host = host
        self.database = database
        self._port = port  # Protected
        self.__connection_string = f"postgresql://{host}:{port}/{database}"  # Private
        self.__is_connected = False
        self.__connection_pool_size = 10
    
    @property
    def is_connected(self) -> bool:
        """Check if connected (read-only access)."""
        return self.__is_connected
    
    @property
    def connection_info(self) -> dict:
        """Get connection info without exposing sensitive details."""
        return {
            'host': self.host,
            'database': self.database,
            'port': self._port,
            'connected': self.__is_connected
        }
    
    @property
    def pool_size(self) -> int:
        return self.__connection_pool_size
    
    @pool_size.setter
    def pool_size(self, size: int):
        if 1 <= size <= 100:
            self.__connection_pool_size = size
        else:
            raise ValueError("Pool size must be between 1 and 100")
    
    def connect(self) -> bool:
        """Establish database connection."""
        print(f"Connected to {self.database} on {self.host}")
        self.__is_connected = True
        return True
```

---

## 4. Error Handling

### Exception Hierarchy
```python
# Custom exception hierarchy for data processing
class DataProcessingError(Exception):
    """Base exception for data processing errors."""
    pass

class DataValidationError(DataProcessingError):
    """Raised when data validation fails."""
    def __init__(self, message: str, invalid_records: list = None):
        super().__init__(message)
        self.invalid_records = invalid_records or []

class DataSourceError(DataProcessingError):
    """Raised when data source is unavailable or corrupted."""
    pass

class DataTransformationError(DataProcessingError):
    """Raised when data transformation fails."""
    pass
```

### Comprehensive Error Handling
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_data_processing(data, processor_func):
    """Process data with comprehensive error handling."""
    try:
        # Validate input
        if not data:
            raise DataValidationError("Input data is empty")
        
        # Process data
        result = processor_func(data)
        
        # Validate output
        if not result:
            logger.warning("Processing returned empty result")
        
        return result
        
    except DataValidationError as ve:
        logger.error(f"Validation error: {ve}")
        raise
    except FileNotFoundError as fe:
        logger.error(f"File not found: {fe}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during processing: {e}")
        raise
    finally:
        logger.info("Processing attempt completed")

def validate_data(data):
    """Validate data and raise custom exceptions."""
    invalid_records = []
    for i, record in enumerate(data):
        if not isinstance(record, dict) or 'id' not in record:
            invalid_records.append(i)
    
    if invalid_records:
        raise DataValidationError(
            f"Found {len(invalid_records)} invalid records",
            invalid_records
        )
```

---

## 5. File I/O and Data Formats

### Efficient File Processing
```python
import json
from datetime import datetime

# Safe file reading with encoding handling
def read_file_safely(file_path: str, encoding: str = 'utf-8'):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return file.read()
    except UnicodeDecodeError:
        # Fallback to different encoding
        with open(file_path, 'r', encoding='latin-1') as file:
            return file.read()

# Processing large files line by line
def process_large_file(file_path: str, processor_func):
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):
            try:
                processed = processor_func(line.strip())
                yield processed
            except Exception as e:
                print(f"Error processing line {line_num}: {e}")

# JSON operations with custom encoder
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def save_to_json(data, file_path: str):
    with open(file_path, 'w') as file:
        json.dump(data, file, cls=DateTimeEncoder, indent=2)

def load_from_json(file_path: str):
    with open(file_path, 'r') as file:
        return json.load(file)
```

---

## 6. Generators and Iterators

### Memory-Efficient Data Processing
```python
def read_csv_chunks(file_path: str, chunk_size: int = 1000):
    """Read CSV file in chunks to save memory."""
    import csv
    
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        chunk = []
        
        for row in reader:
            chunk.append(row)
            
            if len(chunk) >= chunk_size:
                yield chunk
                chunk = []
        
        # Yield remaining records
        if chunk:
            yield chunk

def fibonacci_generator(n: int):
    """Generate Fibonacci sequence up to n numbers."""
    a, b = 0, 1
    count = 0
    
    while count < n:
        yield a
        a, b = b, a + b
        count += 1

# Custom iterator for batch processing
class DataBatch:
    """Custom iterator for batch processing."""
    
    def __init__(self, data: list, batch_size: int):
        self.data = data
        self.batch_size = batch_size
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration
        
        batch = self.data[self.index:self.index + self.batch_size]
        self.index += self.batch_size
        return batch

# Usage
for chunk in read_csv_chunks('large_file.csv', chunk_size=500):
    process_chunk(chunk)

for batch in DataBatch(data, batch_size=10):
    print(f"Processing batch of {len(batch)} items")
```

---

## 7. Context Managers

### Resource Management
```python
from contextlib import contextmanager
import time

# Built-in context managers
with open('data.txt', 'r') as file:
    content = file.read()
# File automatically closed

# Custom context manager class
class DatabaseTransaction:
    """Context manager for database transactions."""
    
    def __init__(self, connection):
        self.connection = connection
        self.transaction = None
    
    def __enter__(self):
        self.transaction = self.connection.begin()
        return self.transaction
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.transaction.commit()
        else:
            self.transaction.rollback()
        return False

# Context manager using decorator
@contextmanager
def timing_context(operation_name: str):
    """Context manager for timing operations."""
    start_time = time.time()
    print(f"Starting {operation_name}")
    
    try:
        yield
    finally:
        end_time = time.time()
        print(f"{operation_name} completed in {end_time - start_time:.2f} seconds")

# Usage
with timing_context("Data Processing"):
    # Your data processing code here
    time.sleep(2)
```

---

## 8. Concurrency and Parallelism

### Threading for I/O-bound Tasks
```python
import threading
import concurrent.futures
import requests

def fetch_url(url: str):
    """Fetch data from URL."""
    response = requests.get(url)
    return response.status_code, len(response.content)

def parallel_fetch(urls: list, max_workers: int = 5):
    """Fetch multiple URLs in parallel."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}
        
        results = {}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                status_code, content_length = future.result()
                results[url] = {'status': status_code, 'size': content_length}
            except Exception as e:
                results[url] = {'error': str(e)}
        
        return results
```

### Multiprocessing for CPU-bound Tasks
```python
import multiprocessing
from multiprocessing import Pool
import math

def cpu_intensive_task(n: int):
    """CPU-intensive calculation."""
    result = 0
    for i in range(n):
        result += math.sqrt(i)
    return result

def parallel_processing(data: list, num_processes: int = None):
    """Process data in parallel using multiple processes."""
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()
    
    with Pool(processes=num_processes) as pool:
        results = pool.map(cpu_intensive_task, data)
    
    return results

# Usage
if __name__ == '__main__':
    data = [100000, 200000, 300000, 400000]
    results = parallel_processing(data)
    print(f"Results: {results}")
```

### Async/Await for I/O Operations
```python
import asyncio
import aiohttp

async def fetch_data_async(session: aiohttp.ClientSession, url: str):
    """Fetch data asynchronously."""
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return {'url': url, 'status': 'success', 'data': data}
            else:
                return {'url': url, 'status': 'error', 'error': f'HTTP {response.status}'}
    except Exception as e:
        return {'url': url, 'status': 'error', 'error': str(e)}

async def fetch_multiple_async(urls: list):
    """Fetch multiple URLs asynchronously."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data_async(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    return results

# Usage
urls = ['https://api1.com/data', 'https://api2.com/data']
results = asyncio.run(fetch_multiple_async(urls))
```

---

## 9. Performance Optimization

### Built-in Functions and Optimizations
```python
import time
import numpy as np

# Use built-ins and list comprehensions
def slow_sum_squares(numbers):
    """Slow: Manual loop"""
    result = []
    for num in numbers:
        result.append(num ** 2)
    return sum(result)

def fast_sum_squares(numbers):
    """Fast: List comprehension + built-in sum"""
    return sum(num ** 2 for num in numbers)

def fastest_sum_squares(numbers):
    """Fastest: NumPy vectorization"""
    arr = np.array(numbers)
    return np.sum(arr ** 2)

# Choose right data structures
def find_common_elements_slow(list1, list2):
    """Slow: O(n*m) complexity"""
    common = []
    for item in list1:
        if item in list2:  # Linear search in list
            common.append(item)
    return common

def find_common_elements_fast(list1, list2):
    """Fast: O(n+m) complexity using sets"""
    return list(set(list1) & set(list2))

# Memory-efficient processing
def process_large_dataset_bad(size):
    """Memory-intensive approach"""
    data = [i**2 for i in range(size)]  # All in memory
    return sum(data)

def process_large_dataset_good(size):
    """Memory-efficient approach"""
    return sum(i**2 for i in range(size))  # Generator
```

### Caching and Memoization
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_calculation(n):
    """Cached expensive function"""
    time.sleep(0.1)  # Simulate expensive operation
    return sum(i ** 2 for i in range(n))

# Custom cache implementation
class CustomCache:
    def __init__(self, max_size=100):
        self.cache = {}
        self.max_size = max_size
        self.access_order = []
    
    def get(self, key, compute_func):
        if key in self.cache:
            # Move to end (most recently used)
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        
        # Compute and cache result
        result = compute_func(key)
        
        if len(self.cache) >= self.max_size:
            # Remove least recently used
            oldest = self.access_order.pop(0)
            del self.cache[oldest]
        
        self.cache[key] = result
        self.access_order.append(key)
        return result
```

---

## 10. Production Best Practices

### Logging and Monitoring
```python
import logging
import traceback
from functools import wraps

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def handle_errors(func):
    """Decorator to handle and log errors comprehensively."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.info(f"Starting execution of {func.__name__}")
            result = func(*args, **kwargs)
            logger.info(f"Successfully completed {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            raise
    return wrapper

@handle_errors
def process_data_safely(data):
    """Process data with comprehensive error handling."""
    if not data:
        raise ValueError("Input data cannot be empty")
    
    return [item * 2 for item in data if item is not None]
```

### Configuration Management
```python
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class DatabaseConfig:
    """Database configuration with environment variable support."""
    host: str = "localhost"
    port: int = 5432
    database: str = "mydb"
    username: str = "user"
    password: str = "password"
    
    @classmethod
    def from_env(cls):
        """Create config from environment variables."""
        return cls(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '5432')),
            database=os.getenv('DB_NAME', 'mydb'),
            username=os.getenv('DB_USER', 'user'),
            password=os.getenv('DB_PASSWORD', 'password')
        )

# Usage
config = DatabaseConfig.from_env()
```

### Testing Patterns
```python
import unittest
from unittest.mock import patch, MagicMock

class TestDataProcessor(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_data = [
            {'id': 1, 'name': 'Alice', 'age': 30},
            {'id': 2, 'name': 'Bob', 'age': 25}
        ]
    
    def test_data_processing(self):
        """Test data processing functionality."""
        result = process_data(self.sample_data)
        self.assertEqual(len(result), 2)
        self.assertTrue(all('processed' in record for record in result))
    
    @patch('requests.get')
    def test_api_call(self, mock_get):
        """Test API call with mocking."""
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'success'}
        mock_get.return_value = mock_response
        
        result = fetch_data_from_api('http://example.com')
        self.assertEqual(result['status'], 'success')

if __name__ == '__main__':
    unittest.main()
```

### Type Hints and Documentation
```python
from typing import List, Dict, Optional, Union, Callable, Any
from dataclasses import dataclass

def process_records(
    records: List[Dict[str, Any]], 
    filter_func: Optional[Callable[[Dict], bool]] = None,
    batch_size: int = 1000
) -> List[Dict[str, Any]]:
    """
    Process a list of records with optional filtering.
    
    Args:
        records: List of record dictionaries
        filter_func: Optional function to filter records
        batch_size: Number of records to process at once
    
    Returns:
        List of processed records
    
    Raises:
        ValueError: If records list is empty
    """
    if not records:
        raise ValueError("Records list cannot be empty")
    
    if filter_func:
        records = [r for r in records if filter_func(r)]
    
    # Process in batches
    processed = []
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        processed.extend(batch)
    
    return processed

@dataclass
class DataConfig:
    """Configuration for data processing."""
    source_path: str
    output_path: str
    batch_size: int = 1000
    enable_validation: bool = True
    retry_count: int = 3
```

This comprehensive guide provides the foundation for building robust, scalable, and maintainable Python applications for data engineering workloads. Each section includes practical examples and real-world patterns commonly used in production data systems.