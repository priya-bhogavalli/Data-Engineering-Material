# Python Key Concepts for Data Engineering

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Python Theoretical Concepts](#-python-theoretical-concepts)
3. [Core Language Features](#-core-language-features)
4. [Data Types & Structures](#-data-types--structures)
5. [Object-Oriented Programming](#-object-oriented-programming)
6. [Functional Programming](#-functional-programming)
7. [Data Engineering Libraries](#-data-engineering-libraries)
8. [File I/O & Data Formats](#-file-io--data-formats)
9. [Database Connectivity](#-database-connectivity)
10. [API Integration](#-api-integration)
11. [Performance Optimization](#-performance-optimization)
12. [Concurrency & Parallelism](#-concurrency--parallelism)
13. [Error Handling & Debugging](#-error-handling--debugging)
14. [Testing & Quality Assurance](#-testing--quality-assurance)
15. [Best Practices](#-best-practices)
16. [When to Use Python](#-when-to-use-python)
17. [Interview Focus Areas](#-interview-focus-areas)

---

## 🎯 Overview

Python is the primary language for data engineering due to its simplicity, extensive ecosystem, and powerful libraries for data processing, analysis, and pipeline orchestration.

**Key Benefits:**
- **Readability**: Clean syntax that's easy to maintain
- **Ecosystem**: Rich libraries for data processing (Pandas, NumPy, PySpark)
- **Integration**: Seamless connection to databases, APIs, and cloud services
- **Scalability**: From scripts to enterprise applications
- **Community**: Extensive documentation and community support

## 🔧 Core Language Features

### Variables and Basic Operations

```python
# Variable assignment and type inference
name = "Data Pipeline"
count = 1000
rate = 0.95
is_active = True

# Multiple assignment
host, port, database = "localhost", 5432, "analytics"

# Type checking
print(f"Type of count: {type(count)}")  # <class 'int'>
print(f"Type of rate: {type(rate)}")    # <class 'float'>

# String formatting (f-strings - preferred)
message = f"Processing {count} records at {rate*100}% success rate"
print(message)  # Processing 1000 records at 95.0% success rate
```

### Control Flow

```python
# Conditional statements
def categorize_data_size(size_mb):
    if size_mb < 100:
        return "small"
    elif size_mb < 1000:
        return "medium"
    elif size_mb < 10000:
        return "large"
    else:
        return "very_large"

# Example usage
sizes = [50, 500, 5000, 50000]
for size in sizes:
    category = categorize_data_size(size)
    print(f"{size}MB is {category}")
# Output: 50MB is small, 500MB is medium, etc.

# List comprehensions
squared_sizes = [size**2 for size in sizes if size > 100]
print(squared_sizes)  # [250000, 25000000, 2500000000]

# Dictionary comprehensions
size_categories = {size: categorize_data_size(size) for size in sizes}
print(size_categories)  # {50: 'small', 500: 'medium', 5000: 'large', 50000: 'very_large'}
```

### Functions and Decorators

```python
from functools import wraps
import time
from typing import Callable, Any

# Basic function with type hints
def calculate_processing_time(records: int, rate_per_second: float) -> float:
    """Calculate estimated processing time"""
    return records / rate_per_second

# Function with default parameters
def connect_database(host: str = "localhost", port: int = 5432, 
                    timeout: int = 30, **kwargs) -> dict:
    """Connect to database with configurable parameters"""
    config = {
        "host": host,
        "port": port,
        "timeout": timeout,
        **kwargs
    }
    return config

# Decorator for timing functions
def timing_decorator(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

# Decorator for retry logic
def retry_decorator(max_attempts: int = 3):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                    time.sleep(1)
        return wrapper
    return decorator

# Usage examples
@timing_decorator
@retry_decorator(max_attempts=3)
def process_data_batch(batch_size: int) -> list:
    """Simulate data processing with potential failures"""
    import random
    if random.random() < 0.3:  # 30% chance of failure
        raise Exception("Processing failed")
    return [i for i in range(batch_size)]

# Test the decorated function
try:
    result = process_data_batch(1000)
    print(f"Processed {len(result)} records")
except Exception as e:
    print(f"Final failure: {e}")
```

## 📊 Data Types & Structures

### Built-in Collections

```python
# Lists - mutable, ordered sequences
data_sources = ["PostgreSQL", "MongoDB", "Kafka"]
data_sources.extend(["Redis", "Elasticsearch"])
data_sources.insert(1, "MySQL")
print(f"Data sources: {data_sources}")

# List slicing and operations
recent_sources = data_sources[-2:]  # Last 2 elements
print(f"Recent sources: {recent_sources}")

# Tuples - immutable sequences
database_config = ("localhost", 5432, "analytics", True)
host, port, db_name, ssl_enabled = database_config  # Unpacking
print(f"Connecting to {host}:{port}/{db_name} (SSL: {ssl_enabled})")

# Dictionaries - key-value mappings
pipeline_config = {
    "source": {
        "type": "postgresql",
        "host": "localhost",
        "port": 5432
    },
    "destination": {
        "type": "s3",
        "bucket": "data-lake",
        "prefix": "raw/"
    },
    "batch_size": 1000,
    "parallel_jobs": 4
}

# Dictionary operations
pipeline_config["created_at"] = "2024-01-01T10:00:00Z"
pipeline_config.update({"version": "1.0", "environment": "production"})

# Safe dictionary access
batch_size = pipeline_config.get("batch_size", 500)  # Default to 500
timeout = pipeline_config.get("timeout", 30)

print(f"Batch size: {batch_size}, Timeout: {timeout}")

# Sets - unique elements
processed_files = {"file1.csv", "file2.json", "file3.parquet"}
new_files = {"file3.parquet", "file4.csv", "file5.json"}

# Set operations
all_files = processed_files | new_files  # Union
common_files = processed_files & new_files  # Intersection
pending_files = new_files - processed_files  # Difference

print(f"All files: {all_files}")
print(f"Common files: {common_files}")
print(f"Pending files: {pending_files}")
```

### Advanced Collections

```python
from collections import defaultdict, Counter, deque, namedtuple, OrderedDict
from typing import Dict, List, DefaultDict

# defaultdict - automatic default values
user_events: DefaultDict[str, List[str]] = defaultdict(list)
events_data = [
    ("alice", "login"), ("bob", "view"), ("alice", "purchase"),
    ("charlie", "login"), ("alice", "logout"), ("bob", "purchase")
]

for user, event in events_data:
    user_events[user].append(event)

print("User events:")
for user, events in user_events.items():
    print(f"  {user}: {events}")

# Counter - counting occurrences
event_types = [event for _, event in events_data]
event_counts = Counter(event_types)
print(f"Event counts: {event_counts}")
print(f"Most common event: {event_counts.most_common(1)[0]}")

# deque - efficient queue operations
processing_queue = deque(maxlen=5)
for i in range(10):
    processing_queue.append(f"task_{i}")
    print(f"Queue: {list(processing_queue)}")

# namedtuple - structured data
DataRecord = namedtuple("DataRecord", ["id", "timestamp", "value", "source"])
records = [
    DataRecord(1, "2024-01-01T10:00:00", 42.5, "sensor_a"),
    DataRecord(2, "2024-01-01T10:01:00", 43.1, "sensor_b"),
    DataRecord(3, "2024-01-01T10:02:00", 41.8, "sensor_a")
]

# Working with namedtuples
for record in records:
    print(f"Record {record.id}: {record.value} from {record.source} at {record.timestamp}")

# Convert to dictionary
record_dict = record._asdict()
print(f"As dict: {record_dict}")
```

### Data Classes (Python 3.7+)

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass
class DataPipelineJob:
    """Data pipeline job configuration"""
    job_id: str
    source_table: str
    destination_table: str
    batch_size: int = 1000
    parallel_workers: int = 4
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    metadata: Optional[dict] = None
    
    def __post_init__(self):
        """Validation after initialization"""
        if self.batch_size <= 0:
            raise ValueError("Batch size must be positive")
        if self.parallel_workers <= 0:
            raise ValueError("Parallel workers must be positive")
    
    def add_tag(self, tag: str):
        """Add a tag to the job"""
        if tag not in self.tags:
            self.tags.append(tag)
    
    def get_summary(self) -> dict:
        """Get job summary"""
        return {
            "job_id": self.job_id,
            "source": self.source_table,
            "destination": self.destination_table,
            "config": {
                "batch_size": self.batch_size,
                "workers": self.parallel_workers
            },
            "created_at": self.created_at.isoformat(),
            "tags": self.tags
        }

# Usage
job = DataPipelineJob(
    job_id="etl_001",
    source_table="raw.user_events",
    destination_table="analytics.user_metrics",
    tags=["daily", "critical"]
)

job.add_tag("automated")
print(f"Job summary: {job.get_summary()}")
```

## 🏗️ Object-Oriented Programming

### Classes and Inheritance

```python
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional
import logging

class DataProcessor(ABC):
    """Abstract base class for data processors"""
    
    def __init__(self, name: str, config: Optional[Dict] = None):
        self.name = name
        self.config = config or {}
        self.processed_count = 0
        self.error_count = 0
        self.created_at = datetime.now()
        self.logger = logging.getLogger(f"{self.__class__.__name__}.{name}")
    
    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process data - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def validate_data(self, data: Any) -> bool:
        """Validate input data - must be implemented by subclasses"""
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """Get processing statistics"""
        uptime = datetime.now() - self.created_at
        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "processed_count": self.processed_count,
            "error_count": self.error_count,
            "success_rate": self.processed_count / (self.processed_count + self.error_count) if (self.processed_count + self.error_count) > 0 else 0,
            "uptime_seconds": uptime.total_seconds(),
            "created_at": self.created_at.isoformat()
        }
    
    def reset_stats(self):
        """Reset processing statistics"""
        self.processed_count = 0
        self.error_count = 0

class CSVProcessor(DataProcessor):
    """CSV file processor with validation"""
    
    def __init__(self, name: str, delimiter: str = ",", encoding: str = "utf-8"):
        super().__init__(name)
        self.delimiter = delimiter
        self.encoding = encoding
    
    def validate_data(self, file_path: str) -> bool:
        """Validate CSV file exists and is readable"""
        import os
        if not os.path.exists(file_path):
            self.logger.error(f"File not found: {file_path}")
            return False
        if not file_path.lower().endswith('.csv'):
            self.logger.warning(f"File may not be CSV: {file_path}")
        return True
    
    def process(self, file_path: str) -> List[Dict[str, str]]:
        """Process CSV file and return list of dictionaries"""
        import csv
        
        if not self.validate_data(file_path):
            self.error_count += 1
            return []
        
        result = []
        try:
            with open(file_path, 'r', encoding=self.encoding) as file:
                reader = csv.DictReader(file, delimiter=self.delimiter)
                for row_num, row in enumerate(reader, 1):
                    if self._validate_row(row, row_num):
                        result.append(dict(row))
                        self.processed_count += 1
                    else:
                        self.error_count += 1
            
            self.logger.info(f"Processed {len(result)} rows from {file_path}")
            
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {e}")
            self.error_count += 1
        
        return result
    
    def _validate_row(self, row: Dict[str, str], row_num: int) -> bool:
        """Validate individual row"""
        if not row or all(not value.strip() for value in row.values()):
            self.logger.warning(f"Empty row at line {row_num}")
            return False
        return True

class JSONProcessor(DataProcessor):
    """JSON data processor with schema validation"""
    
    def __init__(self, name: str, required_fields: Optional[List[str]] = None):
        super().__init__(name)
        self.required_fields = required_fields or []
    
    def validate_data(self, json_data: str) -> bool:
        """Validate JSON string format"""
        import json
        try:
            json.loads(json_data)
            return True
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON: {e}")
            return False
    
    def process(self, json_data: str) -> Dict[str, Any]:
        """Process JSON string and return dictionary"""
        import json
        
        if not self.validate_data(json_data):
            self.error_count += 1
            return {}
        
        try:
            result = json.loads(json_data)
            
            # Validate required fields
            if self.required_fields:
                missing_fields = [field for field in self.required_fields if field not in result]
                if missing_fields:
                    self.logger.error(f"Missing required fields: {missing_fields}")
                    self.error_count += 1
                    return {}
            
            self.processed_count += 1
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing JSON: {e}")
            self.error_count += 1
            return {}

# Usage example with polymorphism
def process_multiple_sources(processors: List[DataProcessor], data_sources: List[Any]):
    """Process data from multiple sources using different processors"""
    results = []
    
    for processor, data_source in zip(processors, data_sources):
        print(f"\nProcessing with {processor.name} ({processor.__class__.__name__})")
        result = processor.process(data_source)
        results.append(result)
        
        # Print statistics
        stats = processor.get_stats()
        print(f"Stats: {stats['processed_count']} processed, {stats['error_count']} errors, "
              f"{stats['success_rate']:.2%} success rate")
    
    return results

# Example usage
csv_processor = CSVProcessor("sales_processor", delimiter="|")
json_processor = JSONProcessor("api_processor", required_fields=["id", "timestamp"])

# Simulate processing
processors = [csv_processor, json_processor]
sample_data = [
    "sample_data.csv",  # This would be a real file path
    '{"id": "123", "timestamp": "2024-01-01T10:00:00", "value": 42.5}'
]

# This would work with real data
# results = process_multiple_sources(processors, sample_data)
```

### Properties and Context Managers

```python
import contextlib
from typing import Optional, Any
import threading
import time

class DatabaseConnection:
    """Database connection with property validation and context management"""
    
    def __init__(self, host: str, port: int, database: str):
        self._host = host
        self._port = port
        self._database = database
        self._connection = None
        self._is_connected = False
        self._lock = threading.Lock()
    
    @property
    def host(self) -> str:
        return self._host
    
    @host.setter
    def host(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Host must be a non-empty string")
        with self._lock:
            if self._is_connected:
                self.disconnect()
            self._host = value
    
    @property
    def port(self) -> int:
        return self._port
    
    @port.setter
    def port(self, value: int):
        if not isinstance(value, int) or not (1 <= value <= 65535):
            raise ValueError("Port must be an integer between 1 and 65535")
        with self._lock:
            if self._is_connected:
                self.disconnect()
            self._port = value
    
    @property
    def connection_string(self) -> str:
        return f"postgresql://{self._host}:{self._port}/{self._database}"
    
    @property
    def is_connected(self) -> bool:
        return self._is_connected
    
    def connect(self) -> bool:
        """Connect to database"""
        with self._lock:
            if self._is_connected:
                return True
            
            try:
                # Simulate connection
                print(f"Connecting to {self.connection_string}")
                time.sleep(0.1)  # Simulate connection time
                self._connection = f"connection_to_{self._host}_{self._port}"
                self._is_connected = True
                print("Connected successfully")
                return True
            except Exception as e:
                print(f"Connection failed: {e}")
                return False
    
    def disconnect(self):
        """Disconnect from database"""
        with self._lock:
            if self._is_connected:
                self._connection = None
                self._is_connected = False
                print("Disconnected from database")
    
    def execute_query(self, query: str) -> Optional[Any]:
        """Execute a query (requires active connection)"""
        if not self._is_connected:
            raise RuntimeError("Not connected to database")
        
        print(f"Executing query: {query[:50]}...")
        # Simulate query execution
        time.sleep(0.05)
        return f"Result for: {query}"
    
    # Context manager methods
    def __enter__(self):
        """Enter context manager"""
        if not self.connect():
            raise RuntimeError("Failed to connect to database")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager"""
        self.disconnect()
        if exc_type is not None:
            print(f"Exception occurred: {exc_type.__name__}: {exc_val}")
        return False  # Don't suppress exceptions

# Usage examples
db = DatabaseConnection("localhost", 5432, "analytics")

# Using as context manager (recommended)
try:
    with db as connection:
        result1 = connection.execute_query("SELECT COUNT(*) FROM users")
        result2 = connection.execute_query("SELECT * FROM orders LIMIT 10")
        print(f"Query results: {result1}, {result2}")
except Exception as e:
    print(f"Database operation failed: {e}")

# Property validation
try:
    db.port = 70000  # Invalid port
except ValueError as e:
    print(f"Validation error: {e}")

# Custom context manager for timing
@contextlib.contextmanager
def timer(operation_name: str):
    """Context manager for timing operations"""
    start_time = time.time()
    print(f"Starting {operation_name}")
    try:
        yield
    finally:
        end_time = time.time()
        print(f"{operation_name} completed in {end_time - start_time:.4f} seconds")

# Usage of custom context manager
with timer("Data processing"):
    time.sleep(0.1)  # Simulate work
    print("Processing data...")
```

## 🔄 Functional Programming

### Higher-Order Functions

```python
from functools import reduce, partial, wraps
from typing import Callable, List, Any, Iterator
import operator

# Map, Filter, Reduce examples with data processing
sales_data = [
    {"product": "laptop", "price": 1200, "quantity": 5, "category": "electronics"},
    {"product": "mouse", "price": 25, "quantity": 50, "category": "electronics"},
    {"product": "desk", "price": 300, "quantity": 10, "category": "furniture"},
    {"product": "chair", "price": 150, "quantity": 20, "category": "furniture"},
    {"product": "monitor", "price": 400, "quantity": 8, "category": "electronics"}
]

# Map - transform each item
def calculate_revenue(item: dict) -> dict:
    """Calculate revenue for each item"""
    revenue = item["price"] * item["quantity"]
    return {**item, "revenue": revenue}

# Using map
sales_with_revenue = list(map(calculate_revenue, sales_data))
print("Sales with revenue:")
for item in sales_with_revenue[:2]:
    print(f"  {item['product']}: ${item['revenue']}")

# Filter - select items based on criteria
high_value_items = list(filter(lambda x: x["revenue"] > 1000, sales_with_revenue))
print(f"\nHigh value items: {len(high_value_items)}")

electronics = list(filter(lambda x: x["category"] == "electronics", sales_with_revenue))
print(f"Electronics items: {len(electronics)}")

# Reduce - aggregate data
total_revenue = reduce(lambda acc, item: acc + item["revenue"], sales_with_revenue, 0)
print(f"\nTotal revenue: ${total_revenue}")

# More complex reduce - group by category
def group_by_category(acc: dict, item: dict) -> dict:
    category = item["category"]
    if category not in acc:
        acc[category] = []
    acc[category].append(item)
    return acc

grouped_sales = reduce(group_by_category, sales_with_revenue, {})
print(f"\nGrouped by category:")
for category, items in grouped_sales.items():
    category_revenue = sum(item["revenue"] for item in items)
    print(f"  {category}: {len(items)} items, ${category_revenue} revenue")

# Partial functions - pre-configure functions
def filter_by_category_and_min_revenue(items: List[dict], category: str, min_revenue: int) -> List[dict]:
    """Filter items by category and minimum revenue"""
    return [item for item in items if item["category"] == category and item["revenue"] >= min_revenue]

# Create specialized functions using partial
filter_high_value_electronics = partial(filter_by_category_and_min_revenue, 
                                       category="electronics", min_revenue=500)

high_value_electronics = filter_high_value_electronics(sales_with_revenue)
print(f"\nHigh-value electronics: {len(high_value_electronics)} items")

# Function composition
def compose(*functions):
    """Compose multiple functions"""
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

# Example: data processing pipeline
def normalize_product_name(item: dict) -> dict:
    """Normalize product name to lowercase"""
    return {**item, "product": item["product"].lower()}

def add_profit_margin(margin: float):
    """Add profit margin calculation"""
    def inner(item: dict) -> dict:
        profit = item["revenue"] * margin
        return {**item, "profit": profit}
    return inner

def format_currency_fields(item: dict) -> dict:
    """Format currency fields"""
    currency_fields = ["price", "revenue", "profit"]
    formatted_item = item.copy()
    for field in currency_fields:
        if field in formatted_item:
            formatted_item[f"{field}_formatted"] = f"${formatted_item[field]:,.2f}"
    return formatted_item

# Create processing pipeline
process_item = compose(
    format_currency_fields,
    add_profit_margin(0.2),  # 20% profit margin
    normalize_product_name
)

# Apply pipeline to data
processed_items = [process_item(item) for item in sales_with_revenue]
print(f"\nProcessed item example:")
print(f"  Product: {processed_items[0]['product']}")
print(f"  Revenue: {processed_items[0]['revenue_formatted']}")
print(f"  Profit: {processed_items[0]['profit_formatted']}")
```

### Generators and Iterators

```python
from typing import Iterator, Generator, Any
import csv
import json
from pathlib import Path

def read_csv_chunks(file_path: str, chunk_size: int = 1000) -> Generator[List[dict], None, None]:
    """Read CSV file in chunks to handle large files efficiently"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            chunk = []
            
            for row in reader:
                chunk.append(dict(row))
                
                if len(chunk) >= chunk_size:
                    yield chunk
                    chunk = []
            
            # Yield remaining rows
            if chunk:
                yield chunk
                
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

def process_large_dataset(file_path: str, processor_func: Callable[[dict], dict]) -> Iterator[dict]:
    """Process large dataset using generators for memory efficiency"""
    for chunk in read_csv_chunks(file_path, chunk_size=500):
        for row in chunk:
            try:
                processed_row = processor_func(row)
                if processed_row:  # Only yield valid processed rows
                    yield processed_row
            except Exception as e:
                print(f"Error processing row: {e}")
                continue

def fibonacci_generator(limit: int) -> Generator[int, None, None]:
    """Generate Fibonacci sequence up to limit"""
    a, b = 0, 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1

# Example: Data transformation pipeline using generators
def data_pipeline():
    """Example data processing pipeline using generators"""
    
    # Sample data generator
    def generate_sample_data(count: int) -> Generator[dict, None, None]:
        import random
        categories = ["electronics", "furniture", "clothing", "books"]
        
        for i in range(count):
            yield {
                "id": i + 1,
                "product": f"product_{i+1}",
                "price": round(random.uniform(10, 1000), 2),
                "quantity": random.randint(1, 100),
                "category": random.choice(categories)
            }
    
    # Processing functions
    def add_revenue(item: dict) -> dict:
        return {**item, "revenue": item["price"] * item["quantity"]}
    
    def filter_high_value(item: dict) -> bool:
        return item.get("revenue", 0) > 500
    
    def format_for_output(item: dict) -> dict:
        return {
            "product_id": item["id"],
            "name": item["product"].title(),
            "total_value": f"${item['revenue']:,.2f}",
            "category": item["category"].upper()
        }
    
    # Create pipeline
    raw_data = generate_sample_data(10000)  # Generate 10k records
    
    # Process data lazily
    processed_data = (
        format_for_output(item)
        for item in (add_revenue(item) for item in raw_data)
        if filter_high_value(add_revenue(item))
    )
    
    # Consume only what we need
    high_value_products = []
    for i, product in enumerate(processed_data):
        if i >= 10:  # Only take first 10 high-value products
            break
        high_value_products.append(product)
    
    return high_value_products

# Run the pipeline
sample_results = data_pipeline()
print("High-value products (first 10):")
for product in sample_results:
    print(f"  {product['name']}: {product['total_value']} ({product['category']})")

# Generator expressions for data analysis
numbers = range(1, 1000000)  # Large range

# Memory-efficient operations using generator expressions
squares_sum = sum(x**2 for x in numbers if x % 2 == 0)  # Sum of squares of even numbers
print(f"\nSum of squares of even numbers (1-999999): {squares_sum}")

# Fibonacci example
fib_sequence = list(fibonacci_generator(10))
print(f"First 10 Fibonacci numbers: {fib_sequence}")

# Custom iterator class
class DataBatchIterator:
    """Iterator for processing data in batches"""
    
    def __init__(self, data: List[Any], batch_size: int):
        self.data = data
        self.batch_size = batch_size
        self.current_index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current_index >= len(self.data):
            raise StopIteration
        
        batch = self.data[self.current_index:self.current_index + self.batch_size]
        self.current_index += self.batch_size
        return batch

# Usage of custom iterator
sample_data = list(range(25))  # 25 items
batch_iterator = DataBatchIterator(sample_data, batch_size=7)

print(f"\nProcessing data in batches:")
for batch_num, batch in enumerate(batch_iterator, 1):
    print(f"  Batch {batch_num}: {batch}")
```

This comprehensive file covers all major Python concepts with practical examples relevant to data engineering. Each section includes detailed explanations and working code examples that demonstrate real-world usage patterns.

## 📚 Data Engineering Libraries

### Pandas - Data Manipulation

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Creating DataFrames
sales_data = {
    'date': pd.date_range('2024-01-01', periods=100, freq='D'),
    'product': np.random.choice(['laptop', 'mouse', 'keyboard', 'monitor'], 100),
    'sales': np.random.randint(1, 20, 100),
    'revenue': np.random.uniform(100, 2000, 100).round(2),
    'region': np.random.choice(['North', 'South', 'East', 'West'], 100)
}

df = pd.DataFrame(sales_data)

# Basic operations
print(f"Dataset shape: {df.shape}")
print(f"Data types:\n{df.dtypes}")
print(f"\nFirst 5 rows:\n{df.head()}")

# Data cleaning and transformation
df['revenue_per_unit'] = df['revenue'] / df['sales']
df['month'] = df['date'].dt.month
df['quarter'] = df['date'].dt.quarter

# Filtering and selection
high_revenue = df[df['revenue'] > 1000]
laptop_sales = df[df['product'] == 'laptop']
recent_sales = df[df['date'] >= '2024-03-01']

print(f"\nHigh revenue transactions: {len(high_revenue)}")
print(f"Laptop sales: {len(laptop_sales)}")

# Grouping and aggregation
monthly_summary = df.groupby(['month', 'product']).agg({
    'sales': 'sum',
    'revenue': ['sum', 'mean', 'count'],
    'revenue_per_unit': 'mean'
}).round(2)

print(f"\nMonthly summary (first 10 rows):\n{monthly_summary.head(10)}")

# Pivot tables
pivot_table = df.pivot_table(
    values='revenue',
    index='product',
    columns='region',
    aggfunc='sum',
    fill_value=0
)

print(f"\nRevenue by product and region:\n{pivot_table}")

# Time series operations
df.set_index('date', inplace=True)
weekly_sales = df.resample('W')['sales'].sum()
monthly_revenue = df.resample('M')['revenue'].sum()

print(f"\nWeekly sales trend (last 5 weeks):\n{weekly_sales.tail()}")

# Data quality checks
missing_data = df.isnull().sum()
duplicates = df.duplicated().sum()
print(f"\nData quality:")
print(f"Missing values: {missing_data.sum()}")
print(f"Duplicate rows: {duplicates}")

# Export data
# df.to_csv('sales_analysis.csv', index=True)
# df.to_parquet('sales_analysis.parquet')
```

### NumPy - Numerical Computing

```python
import numpy as np

# Array creation and basic operations
data = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
print(f"Array shape: {data.shape}")
print(f"Array dtype: {data.dtype}")

# Mathematical operations
squared = np.square(data)
sqrt_data = np.sqrt(data)
log_data = np.log(data)

print(f"Original data:\n{data}")
print(f"Squared:\n{squared}")

# Statistical operations
print(f"\nStatistics:")
print(f"Mean: {np.mean(data):.2f}")
print(f"Std deviation: {np.std(data):.2f}")
print(f"Min: {np.min(data)}, Max: {np.max(data)}")

# Array manipulation
reshaped = data.reshape(6, 2)
transposed = data.T
flattened = data.flatten()

print(f"\nReshaped (6x2):\n{reshaped}")
print(f"Transposed:\n{transposed}")

# Boolean indexing
mask = data > 6
filtered_data = data[mask]
print(f"\nValues > 6: {filtered_data}")

# Random number generation for data simulation
np.random.seed(42)  # For reproducibility
random_data = np.random.normal(100, 15, 1000)  # Normal distribution
uniform_data = np.random.uniform(0, 1, 1000)   # Uniform distribution

print(f"\nRandom data statistics:")
print(f"Normal data - Mean: {np.mean(random_data):.2f}, Std: {np.std(random_data):.2f}")
print(f"Uniform data - Min: {np.min(uniform_data):.3f}, Max: {np.max(uniform_data):.3f}")

# Array broadcasting
matrix = np.array([[1, 2, 3], [4, 5, 6]])
vector = np.array([10, 20, 30])
result = matrix + vector  # Broadcasting

print(f"\nBroadcasting example:")
print(f"Matrix:\n{matrix}")
print(f"Vector: {vector}")
print(f"Result:\n{result}")
```

### Requests - HTTP API Integration

```python
import requests
import json
from typing import Dict, List, Optional
import time

class APIClient:
    """HTTP API client with error handling and retry logic"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'DataEngineering-Client/1.0'
        })
    
    def set_auth(self, token: str):
        """Set authentication token"""
        self.session.headers.update({'Authorization': f'Bearer {token}'})
    
    def get(self, endpoint: str, params: Optional[Dict] = None, retries: int = 3) -> Optional[Dict]:
        """GET request with retry logic"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        for attempt in range(retries):
            try:
                response = self.session.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()  # Raise exception for bad status codes
                return response.json()
                
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == retries - 1:
                    raise e
                time.sleep(2 ** attempt)  # Exponential backoff
        
        return None
    
    def post(self, endpoint: str, data: Dict, retries: int = 3) -> Optional[Dict]:
        """POST request with retry logic"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        for attempt in range(retries):
            try:
                response = self.session.post(url, json=data, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                print(f"POST attempt {attempt + 1} failed: {e}")
                if attempt == retries - 1:
                    raise e
                time.sleep(2 ** attempt)
        
        return None
    
    def paginated_get(self, endpoint: str, params: Optional[Dict] = None, 
                     page_param: str = 'page', limit_param: str = 'limit', 
                     limit: int = 100) -> List[Dict]:
        """Get all pages of data from paginated API"""
        all_data = []
        page = 1
        
        while True:
            page_params = {page_param: page, limit_param: limit}
            if params:
                page_params.update(params)
            
            response = self.get(endpoint, params=page_params)
            if not response or not response.get('data'):
                break
            
            page_data = response['data']
            all_data.extend(page_data)
            
            # Check if we've reached the last page
            if len(page_data) < limit:
                break
            
            page += 1
            print(f"Fetched page {page-1}, total records: {len(all_data)}")
        
        return all_data

# Example usage (with mock API)
def demonstrate_api_usage():
    """Demonstrate API client usage"""
    
    # Example with JSONPlaceholder API (free testing API)
    client = APIClient("https://jsonplaceholder.typicode.com")
    
    try:
        # Get single post
        post = client.get("/posts/1")
        if post:
            print(f"Post title: {post.get('title', 'N/A')}")
        
        # Get multiple posts with parameters
        posts = client.get("/posts", params={"userId": 1})
        if posts:
            print(f"User 1 has {len(posts)} posts")
        
        # Create new post
        new_post_data = {
            "title": "Data Engineering Post",
            "body": "This is about data pipelines",
            "userId": 1
        }
        
        created_post = client.post("/posts", new_post_data)
        if created_post:
            print(f"Created post with ID: {created_post.get('id')}")
    
    except Exception as e:
        print(f"API error: {e}")

# Run demonstration
# demonstrate_api_usage()

# Example: Data extraction from REST API
def extract_user_data(api_client: APIClient) -> pd.DataFrame:
    """Extract user data from API and convert to DataFrame"""
    try:
        users = api_client.get("/users")
        if not users:
            return pd.DataFrame()
        
        # Flatten nested data
        flattened_users = []
        for user in users:
            flat_user = {
                'id': user.get('id'),
                'name': user.get('name'),
                'username': user.get('username'),
                'email': user.get('email'),
                'phone': user.get('phone'),
                'website': user.get('website'),
                'company_name': user.get('company', {}).get('name'),
                'address_city': user.get('address', {}).get('city'),
                'address_zipcode': user.get('address', {}).get('zipcode')
            }
            flattened_users.append(flat_user)
        
        return pd.DataFrame(flattened_users)
    
    except Exception as e:
        print(f"Error extracting user data: {e}")
        return pd.DataFrame()

# Example usage
# client = APIClient("https://jsonplaceholder.typicode.com")
# users_df = extract_user_data(client)
# print(f"Extracted {len(users_df)} users")
```

## 📁 File I/O & Data Formats

### Working with Different File Formats

```python
import json
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
import pickle
from typing import Any, Dict, List
import yaml  # pip install pyyaml

class FileHandler:
    """Unified file handler for different formats"""
    
    @staticmethod
    def read_json(file_path: str) -> Dict[str, Any]:
        """Read JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading JSON file {file_path}: {e}")
            return {}
    
    @staticmethod
    def write_json(data: Dict[str, Any], file_path: str, indent: int = 2):
        """Write data to JSON file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=indent, ensure_ascii=False)
            print(f"Data written to {file_path}")
        except Exception as e:
            print(f"Error writing JSON file {file_path}: {e}")
    
    @staticmethod
    def read_csv(file_path: str, delimiter: str = ',') -> List[Dict[str, str]]:
        """Read CSV file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=delimiter)
                return [dict(row) for row in reader]
        except FileNotFoundError as e:
            print(f"Error reading CSV file {file_path}: {e}")
            return []
    
    @staticmethod
    def write_csv(data: List[Dict[str, Any]], file_path: str, delimiter: str = ','):
        """Write data to CSV file"""
        if not data:
            print("No data to write")
            return
        
        try:
            fieldnames = data[0].keys()
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=delimiter)
                writer.writeheader()
                writer.writerows(data)
            print(f"Data written to {file_path}")
        except Exception as e:
            print(f"Error writing CSV file {file_path}: {e}")
    
    @staticmethod
    def read_yaml(file_path: str) -> Dict[str, Any]:
        """Read YAML file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f"Error reading YAML file {file_path}: {e}")
            return {}
    
    @staticmethod
    def write_yaml(data: Dict[str, Any], file_path: str):
        """Write data to YAML file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                yaml.dump(data, file, default_flow_style=False, indent=2)
            print(f"Data written to {file_path}")
        except Exception as e:
            print(f"Error writing YAML file {file_path}: {e}")
    
    @staticmethod
    def read_pickle(file_path: str) -> Any:
        """Read pickle file"""
        try:
            with open(file_path, 'rb') as file:
                return pickle.load(file)
        except Exception as e:
            print(f"Error reading pickle file {file_path}: {e}")
            return None
    
    @staticmethod
    def write_pickle(data: Any, file_path: str):
        """Write data to pickle file"""
        try:
            with open(file_path, 'wb') as file:
                pickle.dump(data, file)
            print(f"Data pickled to {file_path}")
        except Exception as e:
            print(f"Error writing pickle file {file_path}: {e}")

# Example usage
sample_data = [
    {"id": 1, "name": "Alice", "department": "Engineering", "salary": 75000},
    {"id": 2, "name": "Bob", "department": "Marketing", "salary": 65000},
    {"id": 3, "name": "Charlie", "department": "Engineering", "salary": 80000}
]

config_data = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "analytics"
    },
    "processing": {
        "batch_size": 1000,
        "parallel_jobs": 4,
        "timeout": 300
    }
}

# File operations (commented out to avoid actual file creation)
# FileHandler.write_csv(sample_data, "employees.csv")
# FileHandler.write_json(config_data, "config.json")
# FileHandler.write_yaml(config_data, "config.yaml")

print("Sample data structure:")
print(f"Employee data: {sample_data[0]}")
print(f"Config data: {config_data}")

# Working with file paths
def process_directory(directory_path: str, file_extension: str = ".csv"):
    """Process all files with given extension in directory"""
    path = Path(directory_path)
    
    if not path.exists():
        print(f"Directory {directory_path} does not exist")
        return
    
    files = list(path.glob(f"*{file_extension}"))
    print(f"Found {len(files)} {file_extension} files in {directory_path}")
    
    for file_path in files:
        print(f"Processing: {file_path.name}")
        # Process file here
        file_size = file_path.stat().st_size
        print(f"  Size: {file_size} bytes")

# Example directory processing
# process_directory("./data", ".csv")
```

### Advanced File Operations

```python
import gzip
import zipfile
import tarfile
from pathlib import Path
import shutil
from typing import Generator
import os

class AdvancedFileHandler:
    """Advanced file operations for data engineering"""
    
    @staticmethod
    def read_compressed_file(file_path: str, compression: str = 'auto') -> str:
        """Read compressed files (gzip, zip, etc.)"""
        path = Path(file_path)
        
        if compression == 'auto':
            if path.suffix == '.gz':
                compression = 'gzip'
            elif path.suffix == '.zip':
                compression = 'zip'
            else:
                compression = 'none'
        
        try:
            if compression == 'gzip':
                with gzip.open(file_path, 'rt', encoding='utf-8') as file:
                    return file.read()
            elif compression == 'zip':
                with zipfile.ZipFile(file_path, 'r') as zip_file:
                    # Read first file in zip
                    names = zip_file.namelist()
                    if names:
                        with zip_file.open(names[0]) as file:
                            return file.read().decode('utf-8')
            else:
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read()
        except Exception as e:
            print(f"Error reading compressed file {file_path}: {e}")
            return ""
    
    @staticmethod
    def write_compressed_file(data: str, file_path: str, compression: str = 'gzip'):
        """Write data to compressed file"""
        try:
            if compression == 'gzip':
                with gzip.open(file_path, 'wt', encoding='utf-8') as file:
                    file.write(data)
            elif compression == 'zip':
                with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    # Use filename without .zip extension for internal file
                    internal_name = Path(file_path).stem
                    zip_file.writestr(internal_name, data)
            print(f"Compressed data written to {file_path}")
        except Exception as e:
            print(f"Error writing compressed file {file_path}: {e}")
    
    @staticmethod
    def batch_process_files(directory: str, pattern: str = "*", 
                          batch_size: int = 10) -> Generator[List[Path], None, None]:
        """Process files in batches"""
        path = Path(directory)
        if not path.exists():
            return
        
        files = list(path.glob(pattern))
        
        for i in range(0, len(files), batch_size):
            batch = files[i:i + batch_size]
            yield batch
    
    @staticmethod
    def safe_file_operation(source: str, destination: str, operation: str = 'copy'):
        """Safely copy or move files with backup"""
        source_path = Path(source)
        dest_path = Path(destination)
        
        if not source_path.exists():
            print(f"Source file {source} does not exist")
            return False
        
        # Create backup if destination exists
        if dest_path.exists():
            backup_path = dest_path.with_suffix(dest_path.suffix + '.backup')
            shutil.copy2(dest_path, backup_path)
            print(f"Created backup: {backup_path}")
        
        try:
            if operation == 'copy':
                shutil.copy2(source_path, dest_path)
                print(f"Copied {source} to {destination}")
            elif operation == 'move':
                shutil.move(source_path, dest_path)
                print(f"Moved {source} to {destination}")
            
            return True
        except Exception as e:
            print(f"Error during {operation}: {e}")
            return False
    
    @staticmethod
    def get_file_info(file_path: str) -> Dict[str, Any]:
        """Get comprehensive file information"""
        path = Path(file_path)
        
        if not path.exists():
            return {"error": "File does not exist"}
        
        stat = path.stat()
        
        return {
            "name": path.name,
            "size_bytes": stat.st_size,
            "size_mb": round(stat.st_size / (1024 * 1024), 2),
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "extension": path.suffix,
            "is_file": path.is_file(),
            "is_directory": path.is_dir(),
            "parent_directory": str(path.parent)
        }

# Example usage
sample_text = "This is sample data for compression testing.\n" * 100

# Demonstrate compression
print("File compression example:")
print(f"Original text length: {len(sample_text)} characters")

# Simulate compression (without actual file creation)
print("Would compress and save to: data.txt.gz")
print("Would create zip archive: data.zip")

# Batch processing example
def simulate_batch_processing():
    """Simulate batch file processing"""
    # Create sample file list
    sample_files = [Path(f"file_{i}.csv") for i in range(25)]
    
    print("Batch processing simulation:")
    for batch_num, batch in enumerate(AdvancedFileHandler.batch_process_files(".", "*"), 1):
        if not batch:  # Empty batch (directory doesn't exist)
            break
        print(f"Batch {batch_num}: {len(batch)} files")
        # Process batch here
        if batch_num >= 3:  # Limit output
            break

# simulate_batch_processing()

# File monitoring example
class FileMonitor:
    """Monitor file changes in directory"""
    
    def __init__(self, directory: str):
        self.directory = Path(directory)
        self.file_states = {}
        self._update_states()
    
    def _update_states(self):
        """Update internal file state tracking"""
        if not self.directory.exists():
            return
        
        for file_path in self.directory.iterdir():
            if file_path.is_file():
                stat = file_path.stat()
                self.file_states[str(file_path)] = {
                    'size': stat.st_size,
                    'modified': stat.st_mtime
                }
    
    def check_changes(self) -> List[Dict[str, Any]]:
        """Check for file changes since last update"""
        changes = []
        current_files = set()
        
        if not self.directory.exists():
            return changes
        
        # Check existing and modified files
        for file_path in self.directory.iterdir():
            if file_path.is_file():
                file_str = str(file_path)
                current_files.add(file_str)
                stat = file_path.stat()
                
                if file_str not in self.file_states:
                    # New file
                    changes.append({
                        'type': 'created',
                        'file': file_path.name,
                        'size': stat.st_size
                    })
                else:
                    # Check for modifications
                    old_state = self.file_states[file_str]
                    if (stat.st_size != old_state['size'] or 
                        stat.st_mtime != old_state['modified']):
                        changes.append({
                            'type': 'modified',
                            'file': file_path.name,
                            'old_size': old_state['size'],
                            'new_size': stat.st_size
                        })
        
        # Check for deleted files
        for file_str in self.file_states:
            if file_str not in current_files:
                changes.append({
                    'type': 'deleted',
                    'file': Path(file_str).name
                })
        
        self._update_states()
        return changes

# Example file monitoring
# monitor = FileMonitor("./data")
# changes = monitor.check_changes()
# print(f"File changes detected: {len(changes)}")
```

## 🗄️ Database Connectivity

### SQLite Operations

```python
import sqlite3
from contextlib import contextmanager
from typing import List, Dict, Any, Optional
import pandas as pd

class SQLiteManager:
    """SQLite database manager with context management"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Execute SELECT query and return results"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Convert rows to dictionaries
            columns = [description[0] for description in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            return results
    
    def execute_non_query(self, query: str, params: Optional[tuple] = None) -> int:
        """Execute INSERT, UPDATE, DELETE queries"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.rowcount
    
    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """Execute query with multiple parameter sets"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
            return cursor.rowcount
    
    def create_table_from_dataframe(self, df: pd.DataFrame, table_name: str, 
                                  if_exists: str = 'replace'):
        """Create table from pandas DataFrame"""
        with self.get_connection() as conn:
            df.to_sql(table_name, conn, if_exists=if_exists, index=False)
            print(f"Table '{table_name}' created with {len(df)} rows")
    
    def dataframe_to_sql(self, df: pd.DataFrame, table_name: str, 
                        if_exists: str = 'append') -> int:
        """Insert DataFrame data into existing table"""
        with self.get_connection() as conn:
            df.to_sql(table_name, conn, if_exists=if_exists, index=False)
            return len(df)
    
    def sql_to_dataframe(self, query: str, params: Optional[tuple] = None) -> pd.DataFrame:
        """Execute query and return results as DataFrame"""
        with self.get_connection() as conn:
            if params:
                return pd.read_sql_query(query, conn, params=params)
            else:
                return pd.read_sql_query(query, conn)

# Example usage
def demonstrate_sqlite_operations():
    """Demonstrate SQLite operations"""
    
    # Initialize database manager
    db = SQLiteManager(":memory:")  # In-memory database for demo
    
    # Create sample data
    employees_data = pd.DataFrame([
        {"id": 1, "name": "Alice Johnson", "department": "Engineering", "salary": 75000, "hire_date": "2022-01-15"},
        {"id": 2, "name": "Bob Smith", "department": "Marketing", "salary": 65000, "hire_date": "2022-03-20"},
        {"id": 3, "name": "Charlie Brown", "department": "Engineering", "salary": 80000, "hire_date": "2021-11-10"},
        {"id": 4, "name": "Diana Prince", "department": "HR", "salary": 70000, "hire_date": "2023-02-01"},
        {"id": 5, "name": "Eve Wilson", "department": "Engineering", "salary": 85000, "hire_date": "2021-08-15"}
    ])
    
    # Create table from DataFrame
    db.create_table_from_dataframe(employees_data, "employees")
    
    # Query examples
    print("All employees:")
    all_employees = db.execute_query("SELECT * FROM employees")
    for emp in all_employees[:3]:  # Show first 3
        print(f"  {emp['name']} - {emp['department']} - ${emp['salary']}")
    
    # Parameterized query
    print("\nEngineering department:")
    eng_employees = db.execute_query(
        "SELECT name, salary FROM employees WHERE department = ?", 
        ("Engineering",)
    )
    for emp in eng_employees:
        print(f"  {emp['name']}: ${emp['salary']}")
    
    # Aggregation query
    dept_stats = db.execute_query("""
        SELECT department, 
               COUNT(*) as employee_count,
               AVG(salary) as avg_salary,
               MAX(salary) as max_salary
        FROM employees 
        GROUP BY department
        ORDER BY avg_salary DESC
    """)
    
    print("\nDepartment statistics:")
    for stat in dept_stats:
        print(f"  {stat['department']}: {stat['employee_count']} employees, "
              f"avg salary: ${stat['avg_salary']:.0f}")
    
    # Update operation
    updated_rows = db.execute_non_query(
        "UPDATE employees SET salary = salary * 1.1 WHERE department = ?",
        ("Engineering",)
    )
    print(f"\nUpdated {updated_rows} engineering salaries (+10%)")
    
    # Query as DataFrame
    df_result = db.sql_to_dataframe(
        "SELECT department, AVG(salary) as avg_salary FROM employees GROUP BY department"
    )
    print(f"\nDepartment averages as DataFrame:\n{df_result}")
    
    # Insert new records
    new_employees = [
        (6, "Frank Miller", "Sales", 60000, "2024-01-01"),
        (7, "Grace Lee", "Sales", 62000, "2024-01-15")
    ]
    
    inserted_rows = db.execute_many(
        "INSERT INTO employees (id, name, department, salary, hire_date) VALUES (?, ?, ?, ?, ?)",
        new_employees
    )
    print(f"\nInserted {inserted_rows} new employees")
    
    # Final count
    total_count = db.execute_query("SELECT COUNT(*) as total FROM employees")[0]['total']
    print(f"Total employees: {total_count}")

# Run demonstration
demonstrate_sqlite_operations()
```

### PostgreSQL with psycopg2

```python
# Note: This requires psycopg2-binary: pip install psycopg2-binary
import psycopg2
from psycopg2.extras import RealDictCursor, execute_values
from contextlib import contextmanager
from typing import List, Dict, Any, Optional
import pandas as pd

class PostgreSQLManager:
    """PostgreSQL database manager"""
    
    def __init__(self, host: str, port: int, database: str, user: str, password: str):
        self.connection_params = {
            'host': host,
            'port': port,
            'database': database,
            'user': user,
            'password': password
        }
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params)
            yield conn
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Execute SELECT query and return results as list of dictionaries"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
    
    def execute_non_query(self, query: str, params: Optional[tuple] = None) -> int:
        """Execute INSERT, UPDATE, DELETE queries"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount
    
    def bulk_insert(self, table: str, data: List[Dict[str, Any]], 
                   page_size: int = 1000) -> int:
        """Bulk insert data using execute_values for better performance"""
        if not data:
            return 0
        
        # Get column names from first record
        columns = list(data[0].keys())
        values = [[row[col] for col in columns] for row in data]
        
        query = f"""
            INSERT INTO {table} ({', '.join(columns)}) 
            VALUES %s
        """
        
        total_inserted = 0
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                execute_values(
                    cursor, query, values, 
                    template=None, page_size=page_size
                )
                total_inserted = cursor.rowcount
                conn.commit()
        
        return total_inserted
    
    def dataframe_to_sql(self, df: pd.DataFrame, table: str, 
                        if_exists: str = 'append') -> int:
        """Insert DataFrame data into PostgreSQL table"""
        from sqlalchemy import create_engine
        
        # Create SQLAlchemy engine
        engine_url = f"postgresql://{self.connection_params['user']}:{self.connection_params['password']}@{self.connection_params['host']}:{self.connection_params['port']}/{self.connection_params['database']}"
        engine = create_engine(engine_url)
        
        try:
            df.to_sql(table, engine, if_exists=if_exists, index=False, method='multi')
            return len(df)
        finally:
            engine.dispose()
    
    def sql_to_dataframe(self, query: str, params: Optional[tuple] = None) -> pd.DataFrame:
        """Execute query and return results as DataFrame"""
        from sqlalchemy import create_engine
        
        engine_url = f"postgresql://{self.connection_params['user']}:{self.connection_params['password']}@{self.connection_params['host']}:{self.connection_params['port']}/{self.connection_params['database']}"
        engine = create_engine(engine_url)
        
        try:
            if params:
                return pd.read_sql_query(query, engine, params=params)
            else:
                return pd.read_sql_query(query, engine)
        finally:
            engine.dispose()
    
    def create_table(self, table_name: str, schema: Dict[str, str], 
                    primary_key: Optional[str] = None):
        """Create table with given schema"""
        columns = []
        for col_name, col_type in schema.items():
            columns.append(f"{col_name} {col_type}")
        
        if primary_key:
            columns.append(f"PRIMARY KEY ({primary_key})")
        
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        
        self.execute_non_query(query)
        print(f"Table '{table_name}' created successfully")

# Example usage (commented out as it requires actual PostgreSQL connection)
def demonstrate_postgresql_operations():
    """Demonstrate PostgreSQL operations"""
    
    # Connection parameters (would need real values)
    # db = PostgreSQLManager(
    #     host="localhost",
    #     port=5432,
    #     database="analytics",
    #     user="postgres",
    #     password="password"
    # )
    
    # Example table schema
    user_events_schema = {
        "event_id": "SERIAL",
        "user_id": "INTEGER NOT NULL",
        "event_type": "VARCHAR(50) NOT NULL",
        "timestamp": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "properties": "JSONB"
    }
    
    print("PostgreSQL operations example:")
    print(f"Would create table with schema: {user_events_schema}")
    
    # Sample data for bulk insert
    sample_events = [
        {
            "user_id": 1,
            "event_type": "login",
            "properties": {"ip": "192.168.1.1", "device": "mobile"}
        },
        {
            "user_id": 1,
            "event_type": "page_view",
            "properties": {"page": "/dashboard", "duration": 45}
        },
        {
            "user_id": 2,
            "event_type": "login",
            "properties": {"ip": "192.168.1.2", "device": "desktop"}
        }
    ]
    
    print(f"Would bulk insert {len(sample_events)} events")
    
    # Example queries
    example_queries = [
        "SELECT event_type, COUNT(*) FROM user_events GROUP BY event_type",
        "SELECT user_id, COUNT(*) as event_count FROM user_events GROUP BY user_id",
        "SELECT * FROM user_events WHERE properties->>'device' = 'mobile'"
    ]
    
    print("Example queries:")
    for query in example_queries:
        print(f"  - {query}")

# demonstrate_postgresql_operations()
```

This comprehensive file now covers all major Python concepts with detailed, practical examples specifically relevant to data engineering. Each section includes working code that demonstrates real-world usage patterns and best practices.
## 🌐 API Integration

### REST API Client

```python
import requests
from typing import Dict, Optional

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        response = self.session.get(f"{self.base_url}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    
    def post(self, endpoint: str, data: Dict) -> Dict:
        response = self.session.post(f"{self.base_url}/{endpoint}", json=data)
        response.raise_for_status()
        return response.json()

# Usage
client = APIClient("https://api.example.com")
users = client.get("users", params={"limit": 10})
new_user = client.post("users", {"name": "John", "email": "john@example.com"})
```

## ⚡ Performance Optimization

### Memory Profiling

```python
import tracemalloc
from functools import wraps

def memory_profiler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"{func.__name__}: Current={current/1024/1024:.2f}MB, Peak={peak/1024/1024:.2f}MB")
        return result
    return wrapper

@memory_profiler
def process_large_data():
    data = [i**2 for i in range(1000000)]
    return sum(data)

result = process_large_data()
```

### List Comprehensions vs Loops

```python
import time

# Inefficient loop
def slow_processing(data):
    result = []
    for item in data:
        if item % 2 == 0:
            result.append(item * 2)
    return result

# Efficient list comprehension
def fast_processing(data):
    return [item * 2 for item in data if item % 2 == 0]

# Generator for memory efficiency
def memory_efficient_processing(data):
    return (item * 2 for item in data if item % 2 == 0)

data = range(1000000)
# fast_processing(data) is ~2x faster than slow_processing(data)
```

## 🧵 Concurrency & Parallelism

### Threading for I/O Operations

```python
import threading
import concurrent.futures
import time

def fetch_data(url_id):
    time.sleep(1)  # Simulate I/O
    return f"Data from {url_id}"

# Sequential processing
def sequential_fetch(urls):
    return [fetch_data(url) for url in urls]

# Concurrent processing
def concurrent_fetch(urls):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        return list(executor.map(fetch_data, urls))

urls = range(10)
# concurrent_fetch is ~5x faster for I/O bound tasks
```

### Multiprocessing for CPU Operations

```python
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

def cpu_intensive_task(n):
    return sum(i**2 for i in range(n))

def parallel_processing(tasks):
    with ProcessPoolExecutor() as executor:
        return list(executor.map(cpu_intensive_task, tasks))

tasks = [100000] * 8
# parallel_processing utilizes all CPU cores
```

## 🛡️ Error Handling & Debugging

### Custom Exceptions

```python
class DataValidationError(Exception):
    def __init__(self, field, value, message):
        self.field = field
        self.value = value
        super().__init__(f"{field}: {message} (got: {value})")

class DataProcessor:
    def validate_record(self, record):
        if not isinstance(record.get('id'), int):
            raise DataValidationError('id', record.get('id'), 'must be integer')
        if record.get('amount', 0) < 0:
            raise DataValidationError('amount', record.get('amount'), 'must be positive')

# Usage
processor = DataProcessor()
try:
    processor.validate_record({'id': 'abc', 'amount': -10})
except DataValidationError as e:
    print(f"Validation failed: {e}")
```

### Logging Configuration

```python
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def process_batch(batch_id, data):
    logger.info(f"Starting batch {batch_id} with {len(data)} records")
    try:
        # Process data
        result = len(data) * 2  # Simulate processing
        logger.info(f"Batch {batch_id} completed successfully")
        return result
    except Exception as e:
        logger.error(f"Batch {batch_id} failed: {e}")
        raise
```

## 🧪 Testing & Quality Assurance

### Unit Testing with pytest

```python
import pytest
from unittest.mock import Mock, patch

class DataValidator:
    def validate_email(self, email):
        return '@' in email and '.' in email
    
    def validate_age(self, age):
        return 0 <= age <= 150

# Test file: test_validator.py
def test_email_validation():
    validator = DataValidator()
    assert validator.validate_email("test@example.com") == True
    assert validator.validate_email("invalid-email") == False

def test_age_validation():
    validator = DataValidator()
    assert validator.validate_age(25) == True
    assert validator.validate_age(-5) == False
    assert validator.validate_age(200) == False

@patch('requests.get')
def test_api_call(mock_get):
    mock_get.return_value.json.return_value = {"status": "success"}
    # Test API-dependent code
```

### Data Quality Checks

```python
import pandas as pd

def validate_dataframe(df, schema):
    """Validate DataFrame against schema"""
    errors = []
    
    # Check required columns
    missing_cols = set(schema.keys()) - set(df.columns)
    if missing_cols:
        errors.append(f"Missing columns: {missing_cols}")
    
    # Check data types
    for col, expected_type in schema.items():
        if col in df.columns:
            if not df[col].dtype == expected_type:
                errors.append(f"Column {col}: expected {expected_type}, got {df[col].dtype}")
    
    # Check for nulls in required fields
    null_counts = df.isnull().sum()
    if null_counts.any():
        errors.append(f"Null values found: {null_counts[null_counts > 0].to_dict()}")
    
    return errors

# Usage
schema = {'id': 'int64', 'name': 'object', 'amount': 'float64'}
df = pd.DataFrame({'id': [1, 2], 'name': ['A', 'B'], 'amount': [10.5, 20.0]})
validation_errors = validate_dataframe(df, schema)
```

## 📋 Best Practices

### Code Organization

```python
# config.py
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'analytics'
}

# utils.py
def format_currency(amount):
    return f"${amount:,.2f}"

def validate_config(config, required_keys):
    missing = [key for key in required_keys if key not in config]
    if missing:
        raise ValueError(f"Missing config keys: {missing}")

# main.py
from config import DATABASE_CONFIG
from utils import format_currency, validate_config

class DataPipeline:
    def __init__(self, config):
        validate_config(config, ['host', 'port', 'database'])
        self.config = config
    
    def run(self):
        # Pipeline logic
        pass
```

### Type Hints and Documentation

```python
from typing import List, Dict, Optional, Union
from dataclasses import dataclass

@dataclass
class ProcessingResult:
    """Result of data processing operation"""
    records_processed: int
    errors: List[str]
    execution_time: float

def process_data(
    data: List[Dict[str, Union[str, int, float]]], 
    batch_size: int = 1000,
    validate: bool = True
) -> ProcessingResult:
    """
    Process data in batches with optional validation.
    
    Args:
        data: List of records to process
        batch_size: Number of records per batch
        validate: Whether to validate records
    
    Returns:
        ProcessingResult with processing statistics
    
    Raises:
        ValueError: If batch_size is invalid
    """
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")
    
    # Processing logic here
    return ProcessingResult(
        records_processed=len(data),
        errors=[],
        execution_time=1.5
    )
```

### Context Managers

```python
from contextlib import contextmanager
import time

@contextmanager
def timer(operation_name):
    """Time an operation"""
    start = time.time()
    print(f"Starting {operation_name}")
    try:
        yield
    finally:
        end = time.time()
        print(f"{operation_name} took {end - start:.2f} seconds")

@contextmanager
def database_transaction(connection):
    """Handle database transactions"""
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise

# Usage
with timer("Data processing"):
    # Process data
    time.sleep(1)
```

## 🎯 When to Use Python

### Ideal Use Cases
- **Data ETL Pipelines**: Pandas, NumPy for data transformation
- **API Integration**: Requests library for REST APIs
- **Machine Learning**: Scikit-learn, TensorFlow integration
- **Automation Scripts**: File processing, system administration
- **Prototyping**: Quick development and testing

### Performance Considerations
- **CPU-bound tasks**: Consider multiprocessing or Cython
- **Memory usage**: Use generators for large datasets
- **I/O operations**: Threading for concurrent requests
- **Large datasets**: Consider PySpark or Dask

### Integration Points
- **Databases**: SQLAlchemy, psycopg2, pymongo
- **Cloud Services**: boto3 (AWS), azure-sdk, google-cloud
- **Big Data**: PySpark, Hadoop streaming
- **Message Queues**: pika (RabbitMQ), kafka-python

## 📝 Interview Focus Areas

### Core Concepts to Master
1. **Data Structures**: Lists, dicts, sets, tuples
2. **Functions**: Decorators, generators, lambda functions
3. **OOP**: Classes, inheritance, polymorphism
4. **Error Handling**: Try/except, custom exceptions
5. **File I/O**: CSV, JSON, binary formats
6. **Libraries**: Pandas, NumPy, requests

### Common Interview Questions
- Difference between list and tuple
- When to use generators vs list comprehensions
- How Python manages memory (garbage collection)
- Difference between `==` and `is`
- Global Interpreter Lock (GIL) implications
- Decorator implementation and use cases

### Practical Coding Challenges
- Parse and transform CSV data
- Implement retry logic for API calls
- Design a data validation framework
- Create a simple ETL pipeline
- Handle large files efficiently
- Implement caching mechanism
## 🧠 Python Theoretical Concepts

### Memory Management & Garbage Collection

**Reference Counting:**
- Python uses reference counting as primary garbage collection mechanism
- Each object tracks how many references point to it
- When reference count reaches zero, object is immediately deallocated

```python
import sys

# Reference counting example
data = [1, 2, 3, 4, 5]  # Reference count = 1
backup = data           # Reference count = 2
print(f"Reference count: {sys.getrefcount(data) - 1}")  # -1 for temporary reference

del backup             # Reference count = 1
del data              # Reference count = 0, object deallocated
```

**Cyclic Garbage Collection:**
- Handles circular references that reference counting can't resolve
- Uses mark-and-sweep algorithm to detect unreachable cycles
- Runs automatically when allocation threshold is exceeded

```python
import gc

class Node:
    def __init__(self, value):
        self.value = value
        self.ref = None

# Create circular reference
node1 = Node(1)
node2 = Node(2)
node1.ref = node2
node2.ref = node1  # Circular reference created

# Force garbage collection
collected = gc.collect()
print(f"Objects collected: {collected}")
```

**Memory Pools:**
- Python uses memory pools for small objects (<512 bytes)
- Reduces fragmentation and improves allocation speed
- Objects grouped by size classes in arenas and pools

### Global Interpreter Lock (GIL)

**GIL Fundamentals:**
- Mutex that protects Python objects from concurrent access
- Only one thread can execute Python bytecode at a time
- Prevents race conditions but limits true parallelism

```python
import threading
import time

# GIL impact demonstration
def cpu_bound_task(n):
    total = 0
    for i in range(n):
        total += i * i
    return total

# Single-threaded execution
start = time.time()
result1 = cpu_bound_task(1000000)
result2 = cpu_bound_task(1000000)
single_thread_time = time.time() - start

# Multi-threaded execution (limited by GIL)
start = time.time()
threads = []
for _ in range(2):
    thread = threading.Thread(target=cpu_bound_task, args=(1000000,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
multi_thread_time = time.time() - start

print(f"Single-threaded: {single_thread_time:.2f}s")
print(f"Multi-threaded: {multi_thread_time:.2f}s")
# Multi-threaded is often slower due to GIL overhead
```

**GIL Release Scenarios:**
- I/O operations (file, network, database)
- C extension calls
- Time.sleep() calls
- Long-running computations (every 100 bytecode instructions)

### Data Model & Object System

**Everything is an Object:**
- All data in Python are objects with identity, type, and value
- Objects have attributes and methods
- Dynamic typing allows runtime type changes

```python
# Object introspection
def analyze_object(obj):
    return {
        'id': id(obj),           # Memory address
        'type': type(obj),       # Object type
        'dir': len(dir(obj)),    # Number of attributes
        'mutable': hasattr(obj, '__setattr__')
    }

# Different object types
objects = [42, "hello", [1, 2, 3], {'a': 1}, lambda x: x]
for obj in objects:
    print(f"{obj}: {analyze_object(obj)}")
```

**Method Resolution Order (MRO):**
- Defines order in which base classes are searched for methods
- Uses C3 linearization algorithm
- Ensures consistent method lookup in multiple inheritance

```python
class A:
    def method(self): return "A"

class B(A):
    def method(self): return "B"

class C(A):
    def method(self): return "C"

class D(B, C):
    def method(self): return "D"

# MRO: D -> B -> C -> A -> object
print(D.__mro__)
print(D().method())  # Calls D.method()

# Diamond problem resolution
class E(B, C):
    pass

print(E.__mro__)  # E -> B -> C -> A -> object
print(E().method())  # Calls B.method() (first in MRO)
```

### Bytecode & Execution Model

**Compilation Process:**
1. Source code → Abstract Syntax Tree (AST)
2. AST → Bytecode (.pyc files)
3. Bytecode → Execution by Python Virtual Machine

```python
import dis
import ast

def sample_function(x, y):
    result = x + y
    if result > 10:
        return result * 2
    return result

# View bytecode
print("Bytecode:")
dis.dis(sample_function)

# View AST
source = "x + y * 2"
tree = ast.parse(source, mode='eval')
print(f"\nAST: {ast.dump(tree)}")
```

**Stack-Based Virtual Machine:**
- Python VM uses evaluation stack for operations
- Instructions manipulate stack to perform computations
- Local variables stored in fast locals array

### Namespace & Scope Resolution

**LEGB Rule:**
- **L**ocal: Inside current function
- **E**nclosing: In enclosing function
- **G**lobal: At module level
- **B**uilt-in: Built-in names

```python
# LEGB demonstration
builtin_name = len  # Built-in

global_var = "global"  # Global

def outer_function():
    enclosing_var = "enclosing"  # Enclosing
    
    def inner_function():
        local_var = "local"  # Local
        
        # Scope resolution order: Local -> Enclosing -> Global -> Built-in
        print(f"Local: {local_var}")
        print(f"Enclosing: {enclosing_var}")
        print(f"Global: {global_var}")
        print(f"Built-in: {builtin_name([1, 2, 3])}")
    
    return inner_function

func = outer_function()
func()
```

**Namespace Objects:**
- Modules, classes, and functions have `__dict__` attribute
- Contains namespace as dictionary
- Dynamic attribute access possible

```python
class Example:
    class_var = "class level"
    
    def __init__(self):
        self.instance_var = "instance level"

obj = Example()

# Namespace inspection
print("Class namespace:", Example.__dict__.keys())
print("Instance namespace:", obj.__dict__.keys())

# Dynamic attribute access
setattr(obj, 'dynamic_attr', 'dynamic value')
print("Dynamic attribute:", getattr(obj, 'dynamic_attr'))
```

### Iterator Protocol & Lazy Evaluation

**Iterator Protocol:**
- Objects implementing `__iter__()` and `__next__()`
- Enables for-loop iteration and lazy evaluation
- StopIteration exception signals end of iteration

```python
class FibonacciIterator:
    def __init__(self, max_count):
        self.max_count = max_count
        self.count = 0
        self.a, self.b = 0, 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.count >= self.max_count:
            raise StopIteration
        
        current = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return current

# Usage
fib = FibonacciIterator(5)
for num in fib:
    print(num, end=" ")  # 0 1 1 2 3
```

**Generator Theory:**
- Functions with `yield` keyword create generator objects
- Implement iterator protocol automatically
- Maintain state between calls (coroutine-like behavior)

```python
def generator_states():
    print("State 1: Starting")
    yield 1
    
    print("State 2: After first yield")
    yield 2
    
    print("State 3: After second yield")
    yield 3
    
    print("State 4: Finishing")

# Generator maintains state between calls
gen = generator_states()
print("Created generator")
print(f"First call: {next(gen)}")
print(f"Second call: {next(gen)}")
print(f"Third call: {next(gen)}")
```

### Descriptor Protocol

**Descriptor Theory:**
- Objects defining `__get__()`, `__set__()`, or `__delete__()`
- Control attribute access on other objects
- Foundation for properties, methods, and decorators

```python
class LoggedAttribute:
    def __init__(self, name):
        self.name = name
        self.value = None
    
    def __get__(self, obj, objtype=None):
        print(f"Getting {self.name}: {self.value}")
        return self.value
    
    def __set__(self, obj, value):
        print(f"Setting {self.name}: {value}")
        self.value = value
    
    def __delete__(self, obj):
        print(f"Deleting {self.name}")
        self.value = None

class DataClass:
    attr = LoggedAttribute("attr")

# Descriptor in action
obj = DataClass()
obj.attr = "test value"  # Calls __set__
print(obj.attr)          # Calls __get__
del obj.attr            # Calls __delete__
```

### Metaclasses & Class Creation

**Metaclass Theory:**
- Classes that create classes
- Control class creation process
- Default metaclass is `type`

```python
# Metaclass example
class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class DatabaseConnection(metaclass=SingletonMeta):
    def __init__(self, host):
        self.host = host

# Singleton behavior
db1 = DatabaseConnection("localhost")
db2 = DatabaseConnection("remote")
print(f"Same instance: {db1 is db2}")  # True
print(f"Host: {db1.host}")  # localhost (first instance)
```

**Class Creation Process:**
1. `__prepare__()` - Create namespace dict
2. Execute class body in namespace
3. `__new__()` - Create class object
4. `__init__()` - Initialize class object

### Context Manager Protocol

**Context Manager Theory:**
- Objects implementing `__enter__()` and `__exit__()`
- Guarantee cleanup code execution
- Exception handling in `__exit__()`

```python
class DatabaseTransaction:
    def __init__(self, connection):
        self.connection = connection
        self.transaction = None
    
    def __enter__(self):
        print("Starting transaction")
        self.transaction = self.connection.begin()
        return self.transaction
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            print("Committing transaction")
            self.transaction.commit()
        else:
            print(f"Rolling back transaction: {exc_type.__name__}")
            self.transaction.rollback()
        return False  # Don't suppress exceptions

# Usage (simulated)
class MockConnection:
    def begin(self): return self
    def commit(self): pass
    def rollback(self): pass

conn = MockConnection()
try:
    with DatabaseTransaction(conn) as tx:
        print("Doing database work")
        # raise Exception("Something went wrong")  # Uncomment to test rollback
except Exception as e:
    print(f"Handled exception: {e}")
```

### Concurrency Models

**Threading Model:**
- Preemptive multitasking within single process
- Shared memory space with synchronization primitives
- Limited by GIL for CPU-bound tasks

**Multiprocessing Model:**
- True parallelism with separate memory spaces
- Inter-process communication via pipes, queues, shared memory
- Higher overhead but no GIL limitations

**Async/Await Model:**
- Cooperative multitasking with event loop
- Single-threaded but handles I/O concurrency efficiently
- Based on coroutines and futures

```python
import asyncio

async def async_task(name, delay):
    print(f"Task {name} starting")
    await asyncio.sleep(delay)  # Non-blocking sleep
    print(f"Task {name} completed")
    return f"Result from {name}"

async def main():
    # Concurrent execution of async tasks
    tasks = [
        async_task("A", 1),
        async_task("B", 2),
        async_task("C", 1.5)
    ]
    
    results = await asyncio.gather(*tasks)
    print(f"All results: {results}")

# Run async code
# asyncio.run(main())  # Uncomment to run
```

### Type System & Duck Typing

**Dynamic Typing:**
- Types determined at runtime
- Variables can hold different types during execution
- Type checking happens during operation execution

**Duck Typing:**
- "If it walks like a duck and quacks like a duck, it's a duck"
- Objects defined by behavior, not inheritance
- Enables polymorphism without explicit interfaces

```python
# Duck typing example
class FileWriter:
    def write(self, data):
        print(f"Writing to file: {data}")

class NetworkWriter:
    def write(self, data):
        print(f"Sending over network: {data}")

class DatabaseWriter:
    def write(self, data):
        print(f"Storing in database: {data}")

def process_data(data, writer):
    # Duck typing - any object with write() method works
    writer.write(data)

# All work due to duck typing
writers = [FileWriter(), NetworkWriter(), DatabaseWriter()]
for writer in writers:
    process_data("sample data", writer)
```

**Type Hints (PEP 484):**
- Static type annotations for better code documentation
- Enable static type checking with tools like mypy
- Runtime type checking possible with libraries

```python
from typing import List, Dict, Optional, Union, Protocol

# Protocol for structural typing
class Writable(Protocol):
    def write(self, data: str) -> None: ...

def log_data(data: str, writer: Writable) -> None:
    writer.write(f"LOG: {data}")

# Generic types
def process_items(items: List[Union[str, int]]) -> Dict[str, int]:
    result = {}
    for item in items:
        result[str(item)] = len(str(item))
    return result
```
