# Python Key Concepts for Data Engineering

## 📋 Table of Contents

1. [Data Structures](#1-data-structures)
   - [Lists - Ordered, Mutable Collections](#1-customer-data-lookup-o1-performance---instant)
   - [Dictionaries - Key-Value Mappings](#1-customer-data-lookup-o1-performance---instant)
   - [Sets - Unique Collections](#1-customer-data-lookup-o1-performance---instant)
   - [Tuples - Immutable Ordered Collections](#1-customer-data-lookup-o1-performance---instant)
2. [Functions and Decorators](#2-functions-and-decorators)
   - [Function Definitions](#test-the-function)
   - [Decorators - Function Wrappers](#1-customer-data-lookup-o1-performance---instant)
3. [Object-Oriented Programming](#3-object-oriented-programming)
   - [Class Definition](#class-definition)
   - [Inheritance and Polymorphism](#2-functions-and-decorators)
4. [Error Handling](#4-error-handling)
   - [Try-Except Patterns](#try-except-patterns)
5. [File I/O and Data Formats](#5-file-io-and-data-formats)
   - [Text Files](#reading-files)
   - [JSON Operations](#data-cleaning-operations)
6. [Generators and Iterators](#6-generators-and-iterators)
   - [Generator Functions](#2-functions-and-decorators)
   - [Iterator Protocol](#iterator-protocol)
7. [Context Managers](#7-context-managers)
   - [Built-in Context Managers](#7-context-managers)
   - [Custom Context Managers](#7-context-managers)
8. [Concurrency and Parallelism](#8-concurrency-and-parallelism)
   - [Threading for I/O-bound Tasks](#python-key-concepts-for-data-engineering)
   - [Multiprocessing for CPU-bound Tasks](#python-key-concepts-for-data-engineering)
9. [Type Hints and Documentation](#9-type-hints-and-documentation)
   - [Type Hints](#9-type-hints-and-documentation)
10. [Testing](#10-testing)
    - [Unit Testing](#10-testing)
    - [Pytest (Alternative Testing Framework)](#10-testing)

---

## 1. Data Structures
**What they are**: Data structures are like different types of containers for your data - each optimized for specific tasks, just like how you use different containers in your kitchen.

**Real-World Analogy**: 
- **Lists** = Shopping list (ordered, can add/remove items)
- **Dictionaries** = Phone book (look up by name to get number)
- **Sets** = Guest list (no duplicates allowed)
- **Tuples** = GPS coordinates (fixed, can't change)

**Why Critical for Data Engineering**: Choosing the wrong data structure is like using a spoon to cut steak - it works, but it's painfully slow. The right choice can make your code 100x faster.

**Performance Impact**: Processing 1 million records with the right data structure takes seconds; with the wrong one, it takes hours.

**When to use**: 
- Lists for ordered data that needs modification
- Dictionaries for key-value lookups and configuration
- Sets for deduplication and membership testing
- Tuples for immutable structured data

> 📚 **For comprehensive coverage of Python data structures, see [PYTHON_DATA_STRUCTURES.md](./PYTHON_DATA_STRUCTURES.md)**
> 
> This includes:
> - Built-in types (lists, dicts, sets, tuples, strings)
> - Collections module (Counter, defaultdict, deque, namedtuple)
> - Advanced structures (heaps, queues, arrays)
> - Performance comparisons and best practices
> - Real-world examples for data engineering

**Lists - Ordered, Mutable Collections**:
```python
# Real Data Engineering Example: Processing customer transaction IDs
transaction_ids = [1001, 1002, 1003, 1004, 1005]

# Adding new transactions as they come in
transaction_ids.append(1006)                    # New transaction
transaction_ids.extend([1007, 1008, 1009])     # Batch of transactions
transaction_ids.insert(0, 1000)                # Insert at beginning

# Data cleaning operations
transaction_ids.remove(1003)                   # Remove cancelled transaction
last_transaction = transaction_ids.pop()        # Get and remove last

# Real Business Scenarios with List Comprehensions:

# 1. Data Transformation: Convert IDs to strings for API calls
api_ready_ids = [f"TXN_{id}" for id in transaction_ids]
# Result: ['TXN_1000', 'TXN_1001', 'TXN_1002', ...]

# 2. Data Filtering: Find high-value transactions (ID > 1005)
high_value_txns = [id for id in transaction_ids if id > 1005]
# Business use: Flag for manual review

# 3. Complex Processing: Create transaction batches for processing
batch_matrix = [[batch_id * 100 + i for i in range(10)] 
                for batch_id in range(5)]
# Creates 5 batches of 10 transaction IDs each

# Performance Note: List comprehensions are 2-3x faster than loops
# Critical when processing millions of records
```

**Dictionaries - Key-Value Mappings**:
```python
# Real Example: Data Pipeline Configuration
pipeline_config = {
    'source_database': 'postgresql://prod-db:5432/sales',
    'target_warehouse': 's3://data-lake/processed/',
    'batch_size': 10000,
    'retry_attempts': 3,
    'timeout_seconds': 300
}

# Dynamic configuration updates
pipeline_config['last_run'] = '2024-01-15 10:30:00'     # Add new setting
batch_size = pipeline_config.get('batch_size', 1000)    # Safe access with fallback
pipeline_config.update({                                 # Bulk updates
    'debug_mode': True,
    'log_level': 'INFO'
})

# Real Business Scenarios:

# 1. Customer Data Lookup (O(1) performance - instant!)
customer_data = {
    'CUST001': {'name': 'John Doe', 'tier': 'Premium', 'credit_limit': 50000},
    'CUST002': {'name': 'Jane Smith', 'tier': 'Gold', 'credit_limit': 25000},
    'CUST003': {'name': 'Bob Johnson', 'tier': 'Silver', 'credit_limit': 10000}
}

# Lightning-fast customer lookup for real-time transactions
customer_info = customer_data.get('CUST001', {'tier': 'Basic', 'credit_limit': 1000})

# 2. Data Transformation: Square transaction amounts for analysis
transaction_amounts = {1001: 150.50, 1002: 299.99, 1003: 75.25}
squared_amounts = {txn_id: amount**2 for txn_id, amount in transaction_amounts.items()}

# 3. Configuration Filtering: Extract only numeric settings
numeric_settings = {k: v for k, v in pipeline_config.items() if isinstance(v, (int, float))}
# Result: {'batch_size': 10000, 'retry_attempts': 3, 'timeout_seconds': 300}

# Why Dictionaries Rock for Data Engineering:
# - O(1) lookup time (instant, even with millions of keys)
# - Perfect for caching expensive computations
# - Ideal for configuration management
# - Essential for data deduplication
```

**Sets - Unique Collections**:
```python
# Set operations for data deduplication
unique_ids = {1, 2, 3, 4, 5}
unique_ids.add(6)
unique_ids.update([7, 8, 9])

# Set operations
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}
intersection = set1 & set2      # {3, 4}
union = set1 | set2             # {1, 2, 3, 4, 5, 6}
difference = set1 - set2        # {1, 2}
```

**Tuples - Immutable Ordered Collections**:
```python
# Tuples for fixed data structures
coordinates = (10.5, 20.3)
database_config = ('localhost', 5432, 'mydb', 'user')

# Named tuples for structured data
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)
print(f"X: {p.x}, Y: {p.y}")
```

## 2. Functions and Decorators
**What they are**: Functions are reusable blocks of code that perform specific tasks. Decorators are a powerful feature that allows you to modify or extend function behavior without changing the function's code.

**Why important**: Functions promote code reusability and modularity, essential for maintaining large data pipelines. Decorators enable cross-cutting concerns like logging, timing, retry logic, and authentication without cluttering business logic.

**When to use**:
- Functions for any repeatable logic
- Decorators for logging, timing, retries, authentication
- Lambda functions for simple transformations in map/filter operations

**Function Definitions**:
```python
def process_data(data, transform_func=None, **kwargs):
    """Process data with optional transformation."""
    if transform_func:
        data = transform_func(data)
    
    # Use kwargs for flexible configuration
    batch_size = kwargs.get('batch_size', 1000)
    debug = kwargs.get('debug', False)
    
    if debug:
        print(f"Processing {len(data)} records in batches of {batch_size}")
    
    return data

# Lambda functions for simple operations
multiply = lambda x, y: x * y
filter_positive = lambda x: x > 0
```

**Decorators - Function Wrappers**:
```python
import time
import functools
from typing import Callable, Any

def timing_decorator(func: Callable) -> Callable:
    """Measure function execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return wrapper

def retry_decorator(max_attempts: int = 3, delay: float = 1.0):
    """Retry function on failure."""
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

# Usage
@timing_decorator
@retry_decorator(max_attempts=3, delay=2.0)
def fetch_data_from_api(url: str):
    # API call implementation
    pass
```

## 3. Object-Oriented Programming
**What it is**: A programming paradigm that organizes code into classes and objects, encapsulating data and behavior together.

**Why important**: OOP enables building complex, maintainable data processing systems. It provides encapsulation, inheritance, and polymorphism, making code more organized and reusable. Essential for building data pipeline frameworks, ETL tools, and data processing engines.

**When to use**:
- Building data pipeline frameworks
- Creating reusable data processing components
- Implementing different data source connectors
- Managing complex state in data applications

**Class Definition**:
```python
class DataPipeline:
    """Data processing pipeline with configurable stages."""
    
    def __init__(self, name: str, config: dict):
        self.name = name
        self.config = config
        self._stages = []
        self._results = {}
    
    def add_stage(self, stage_name: str, processor: Callable):
        """Add processing stage to pipeline."""
        self._stages.append((stage_name, processor))
    
    def execute(self, data):
        """Execute all pipeline stages."""
        current_data = data
        
        for stage_name, processor in self._stages:
            print(f"Executing stage: {stage_name}")
            current_data = processor(current_data)
            self._results[stage_name] = len(current_data)
        
        return current_data
    
    @property
    def stage_results(self):
        """Get results from each stage."""
        return self._results
    
    def __str__(self):
        return f"DataPipeline(name={self.name}, stages={len(self._stages)})"
```

**Inheritance and Polymorphism**:
```python
from abc import ABC, abstractmethod

class DataSource(ABC):
    """Abstract base class for data sources."""
    
    @abstractmethod
    def extract(self) -> list:
        pass
    
    @abstractmethod
    def validate(self, data: list) -> bool:
        pass

class CSVDataSource(DataSource):
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def extract(self) -> list:
        import csv
        with open(self.file_path, 'r') as file:
            return list(csv.DictReader(file))
    
    def validate(self, data: list) -> bool:
        return len(data) > 0 and all(isinstance(row, dict) for row in data)

class APIDataSource(DataSource):
    def __init__(self, url: str, headers: dict = None):
        self.url = url
        self.headers = headers or {}
    
    def extract(self) -> list:
        import requests
        response = requests.get(self.url, headers=self.headers)
        return response.json()
    
    def validate(self, data: list) -> bool:
        return isinstance(data, list) and len(data) > 0
```

## 4. Error Handling
**What it is**: A systematic approach to anticipating, catching, and handling errors that occur during program execution.

**Why important**: Data pipelines often deal with unreliable external systems, malformed data, and network issues. Proper error handling ensures pipelines are resilient, can recover from failures, and provide meaningful feedback for debugging.

**When to use**:
- Always in production data pipelines
- When dealing with external APIs or databases
- File I/O operations
- Data validation and transformation steps

**Try-Except Patterns**:
```python
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_data_processing(data, processor_func):
    """Process data with comprehensive error handling."""
    try:
        # Validate input
        if not data:
            raise ValueError("Input data is empty")
        
        # Process data
        result = processor_func(data)
        
        # Validate output
        if not result:
            logger.warning("Processing returned empty result")
        
        return result
        
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise
    except FileNotFoundError as fe:
        logger.error(f"File not found: {fe}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during processing: {e}")
        raise
    finally:
        # Cleanup code always runs
        logger.info("Processing attempt completed")

# Custom exceptions
class DataValidationError(Exception):
    """Raised when data validation fails."""
    def __init__(self, message, invalid_records=None):
        super().__init__(message)
        self.invalid_records = invalid_records or []

def validate_data(data):
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

## 5. File I/O and Data Formats
**What it is**: Operations for reading from and writing to files in various formats like text, CSV, JSON, and binary formats.

**Why important**: Data engineers constantly work with files - reading source data, writing processed results, and handling configuration files. Efficient file I/O is crucial for performance, especially with large datasets.

**When to use**:
- Reading source data files (CSV, JSON, XML)
- Writing processed data to storage
- Configuration management
- Logging and audit trails
- Batch processing workflows

**Text Files**:
```python
# Reading files
def read_file_safely(file_path: str, encoding: str = 'utf-8'):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return file.read()
    except UnicodeDecodeError:
        # Fallback to different encoding
        with open(file_path, 'r', encoding='latin-1') as file:
            return file.read()

# Writing files
def write_data_to_file(data: list, file_path: str):
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in data:
            file.write(f"{item}\n")

# Processing large files line by line
def process_large_file(file_path: str, processor_func):
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):
            try:
                processed = processor_func(line.strip())
                yield processed
            except Exception as e:
                print(f"Error processing line {line_num}: {e}")
```

**JSON Operations**:
```python
import json
from datetime import datetime

# Custom JSON encoder for complex types
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

# Streaming JSON for large files
import ijson

def process_large_json(file_path: str):
    with open(file_path, 'rb') as file:
        # Parse JSON objects one by one
        objects = ijson.items(file, 'item')
        for obj in objects:
            yield obj
```

## 6. Generators and Iterators
**What they are**: Generators are functions that yield values one at a time, creating iterators that produce items on-demand rather than storing them all in memory.

**Why important**: Essential for processing large datasets that don't fit in memory. Generators enable streaming data processing, reduce memory usage, and improve performance in data pipelines.

**When to use**:
- Processing large files line by line
- Streaming data from APIs
- ETL pipelines with large datasets
- Real-time data processing
- Memory-constrained environments

**Generator Functions**:
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

# Usage
for chunk in read_csv_chunks('large_file.csv', chunk_size=500):
    process_chunk(chunk)
```

**Iterator Protocol**:
```python
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
data = list(range(100))
for batch in DataBatch(data, batch_size=10):
    print(f"Processing batch of {len(batch)} items")
```

## 7. Context Managers
**What they are**: Objects that define runtime context for executing code blocks, ensuring proper resource acquisition and cleanup.

**Why important**: Critical for managing resources like file handles, database connections, and network connections. They guarantee cleanup even when errors occur, preventing resource leaks in long-running data pipelines.

**When to use**:
- File operations
- Database connections
- Network connections
- Temporary resource allocation
- Transaction management
- Timing operations

**Built-in Context Managers**:
```python
# File handling
with open('data.txt', 'r') as file:
    content = file.read()
# File automatically closed

# Database connections
import sqlite3
with sqlite3.connect('database.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
# Connection automatically closed
```

**Custom Context Managers**:
```python
from contextlib import contextmanager
import time

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

## 8. Concurrency and Parallelism
**What they are**: Techniques for executing multiple tasks simultaneously. Concurrency handles multiple tasks at once (not necessarily simultaneously), while parallelism executes tasks simultaneously on multiple cores.

**Why important**: Data processing often involves I/O-bound operations (API calls, file reads) and CPU-bound tasks (data transformations). Proper use of concurrency and parallelism can dramatically improve pipeline performance.

**When to use**:
- Threading for I/O-bound tasks (API calls, file operations)
- Multiprocessing for CPU-bound tasks (data transformations)
- Async/await for high-concurrency I/O operations
- Parallel data processing and ETL operations

**Threading for I/O-bound Tasks**:
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
        # Submit all tasks
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}
        
        # Collect results
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

**Multiprocessing for CPU-bound Tasks**:
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

## 9. Type Hints and Documentation
**What they are**: Type hints provide static type information to make code more readable and enable better tooling. Documentation includes docstrings, comments, and external documentation.

**Why important**: In data engineering, code is often complex and maintained by teams. Type hints catch errors early, improve IDE support, and make code self-documenting. Good documentation is essential for maintaining data pipelines and onboarding team members.

**When to use**:
- All production code should have type hints
- Public APIs and functions need comprehensive documentation
- Complex data transformations require clear explanations
- Team environments where code is shared

**Type Hints**:
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

## 10. Testing
**What it is**: The practice of writing code to verify that your application code works correctly under various conditions.

**Why important**: Data pipelines process critical business data, and bugs can have serious consequences. Testing ensures data quality, catches regressions, and provides confidence when making changes to production systems.

**When to use**:
- Unit tests for individual functions and classes
- Integration tests for data pipeline components
- End-to-end tests for complete workflows
- Data validation tests for quality assurance
- Performance tests for optimization

**Unit Testing**:
```python
import unittest
from unittest.mock import patch, MagicMock

class TestDataProcessor(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_data = [
            {'id': 1, 'name': 'Alice', 'age': 30},
            {'id': 2, 'name': 'Bob', 'age': 25},
            {'id': 3, 'name': 'Charlie', 'age': 35}
        ]
    
    def test_filter_by_age(self):
        """Test age filtering functionality."""
        result = filter_by_age(self.sample_data, min_age=30)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(person['age'] >= 30 for person in result))
    
    def test_empty_data_handling(self):
        """Test handling of empty data."""
        with self.assertRaises(ValueError):
            process_records([])
    
    @patch('requests.get')
    def test_api_call(self, mock_get):
        """Test API call with mocking."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'success'}
        mock_get.return_value = mock_response
        
        # Test the function
        result = fetch_data_from_api('http://example.com')
        self.assertEqual(result['status'], 'success')
        mock_get.assert_called_once_with('http://example.com')

if __name__ == '__main__':
    unittest.main()
```

**Pytest (Alternative Testing Framework)**:
```python
import pytest
from unittest.mock import patch

@pytest.fixture
def sample_data():
    """Test data fixture."""
    return [
        {'id': 1, 'name': 'Alice', 'age': 30},
        {'id': 2, 'name': 'Bob', 'age': 25}
    ]

def test_data_processing(sample_data):
    """Test data processing with fixture."""
    result = process_data(sample_data)
    assert len(result) == 2
    assert all('processed' in record for record in result)

@pytest.mark.parametrize("age,expected_count", [
    (25, 2),
    (30, 1),
    (40, 0)
])
def test_age_filter_parametrized(sample_data, age, expected_count):
    """Parametrized test for age filtering."""
    result = filter_by_age(sample_data, min_age=age)
    assert len(result) == expected_count
```