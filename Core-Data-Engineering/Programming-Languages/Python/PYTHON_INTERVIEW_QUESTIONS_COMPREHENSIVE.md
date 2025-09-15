# Python Interview Questions for Data Engineering

## 🎯 **Quick Navigation & Study Guide**

### 📊 **Interview Success Metrics**
- **Fundamentals Mastery**: 95%+ accuracy on basic Python concepts
- **Data Engineering Focus**: Understanding of data processing libraries and patterns
- **Performance Optimization**: Ability to write efficient, scalable Python code
- **Real-World Application**: Practical experience with ETL, APIs, and data pipelines
- **Advanced Concepts**: Decorators, generators, context managers, and concurrency

### 🔥 **Most Critical Topics for Data Engineers**
1. **Data Structures & Algorithms** - Lists, dicts, sets, comprehensions
2. **Object-Oriented Programming** - Classes, inheritance, magic methods
3. **Functional Programming** - Lambda, map/filter/reduce, decorators
4. **Memory Management** - GIL, garbage collection, optimization
5. **Concurrency** - Threading, multiprocessing, asyncio
6. **Data Processing** - Pandas, NumPy integration patterns
7. **Database Integration** - SQLAlchemy, connection management
8. **Error Handling** - Exception management in data pipelines

---

## 📋 Table of Contents

1. [Basic Level Questions (1-50)](#basic-level-questions-1-50)
2. [Intermediate Level Questions (51-100)](#intermediate-level-questions-51-100)
3. [Advanced Level Questions (101-150)](#advanced-level-questions-101-150)
4. [Architecture & Performance (151-200)](#architecture--performance-151-200)
5. [Data Processing & Libraries (201-250)](#data-processing--libraries-201-250)
6. [Production & Operations (251-300)](#production--operations-251-300)
7. [Scenario-Based Questions (301-350)](#scenario-based-questions-301-350)

---

## Basic Level Questions (1-50)

### 1. What is Python and why is it popular for data engineering?

**Answer:** Python is a high-level, interpreted programming language known for its simplicity and readability.

**Why Popular for Data Engineering:**
- **Readable Syntax**: Easy to write and maintain data pipelines
- **Rich Ecosystem**: Libraries like Pandas, NumPy, PySpark, Airflow
- **Integration**: Seamless connection with databases, APIs, cloud services
- **Community Support**: Large ecosystem and extensive documentation
- **Versatility**: Supports multiple programming paradigms

```python
# Simple ETL pipeline example
import pandas as pd
from sqlalchemy import create_engine

def etl_pipeline():
    # Extract
    df = pd.read_csv('data.csv')
    
    # Transform
    df['processed_date'] = pd.to_datetime(df['date'])
    df['amount_usd'] = df['amount'] * df['exchange_rate']
    
    # Load
    engine = create_engine('postgresql://user:pass@localhost/db')
    df.to_sql('processed_data', engine, if_exists='append')
```

### 2. Explain Python's memory management and garbage collection.

**Answer:** Python uses reference counting with cycle detection for memory management.

**Key Components:**
- **Reference Counting**: Tracks number of references to each object
- **Garbage Collector**: Handles circular references
- **Memory Pools**: Optimizes allocation for small objects

```python
import gc
import sys

def demonstrate_memory_management():
    # Reference counting
    data = [1, 2, 3, 4, 5]
    print(f"Reference count: {sys.getrefcount(data)}")
    
    # Create circular reference
    class Node:
        def __init__(self, value):
            self.value = value
            self.ref = None
    
    node1 = Node(1)
    node2 = Node(2)
    node1.ref = node2
    node2.ref = node1  # Circular reference
    
    # Force garbage collection
    collected = gc.collect()
    print(f"Objects collected: {collected}")
```

### 3. What is the Global Interpreter Lock (GIL) and how does it affect performance?

**Answer:** The GIL is a mutex that prevents multiple native threads from executing Python bytecodes simultaneously.

**Impact:**
- **CPU-bound tasks**: Limited to single-core performance
- **I/O-bound tasks**: Less affected due to GIL release during I/O
- **Workarounds**: Multiprocessing, async/await, C extensions

```python
import threading
import multiprocessing
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def cpu_task(n):
    return sum(i * i for i in range(n))

def compare_concurrency():
    tasks = [100000] * 4
    
    # Threading (limited by GIL)
    start = time.time()
    with ThreadPoolExecutor() as executor:
        thread_results = list(executor.map(cpu_task, tasks))
    thread_time = time.time() - start
    
    # Multiprocessing (bypasses GIL)
    start = time.time()
    with ProcessPoolExecutor() as executor:
        process_results = list(executor.map(cpu_task, tasks))
    process_time = time.time() - start
    
    print(f"Threading: {thread_time:.2f}s")
    print(f"Multiprocessing: {process_time:.2f}s")
```

### 4. Explain the difference between lists, tuples, and sets.

**Answer:** Different data structures with distinct characteristics and use cases.

```python
def compare_data_structures():
    # Lists - Ordered, mutable, allow duplicates
    numbers_list = [1, 2, 3, 2, 4]
    numbers_list.append(5)
    numbers_list[0] = 10
    
    # Tuples - Ordered, immutable, allow duplicates
    coordinates = (10.5, 20.3, 10.5)
    # coordinates[0] = 15  # Error: immutable
    
    # Sets - Unordered, mutable, unique elements
    unique_numbers = {1, 2, 3, 2, 4}  # Duplicate removed
    unique_numbers.add(5)
    
    # Performance comparison
    large_list = list(range(10000))
    large_set = set(range(10000))
    
    # List: O(n) lookup, Set: O(1) lookup
    print(f"9999 in list: {'9999' in large_list}")
    print(f"9999 in set: {'9999' in large_set}")
```

### 5. What are Python decorators and how do you use them?

**Answer:** Decorators are functions that modify or enhance other functions without changing their source code.

```python
from functools import wraps
import time

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

def retry_decorator(max_attempts=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}")
        return wrapper
    return decorator

@timing_decorator
@retry_decorator(max_attempts=3)
def data_processing_task():
    # Simulate data processing
    time.sleep(0.1)
    return "Processing complete"
```

### 6. Explain Python's `*args` and `**kwargs`.

**Answer:** `*args` and `**kwargs` allow functions to accept variable numbers of arguments.

```python
def demonstrate_args_kwargs():
    # *args - Variable positional arguments
    def process_data(*datasets):
        for i, dataset in enumerate(datasets):
            print(f"Processing dataset {i}: {len(dataset)} records")
    
    # **kwargs - Variable keyword arguments
    def configure_pipeline(**config):
        batch_size = config.get('batch_size', 1000)
        timeout = config.get('timeout', 30)
        print(f"Pipeline config: batch_size={batch_size}, timeout={timeout}")
    
    # Combined usage
    def flexible_etl(source, *transformations, **options):
        print(f"Source: {source}")
        print(f"Transformations: {transformations}")
        print(f"Options: {options}")
    
    # Usage examples
    process_data([1, 2, 3], [4, 5, 6], [7, 8, 9])
    configure_pipeline(batch_size=500, timeout=60, retry_count=3)
    flexible_etl("database", "clean", "validate", format="json", compress=True)
```

### 7. What are Python generators and why are they useful?

**Answer:** Generators are functions that yield values one at a time, providing memory-efficient iteration.

```python
def demonstrate_generators():
    # Generator function
    def read_large_file(filename):
        with open(filename, 'r') as file:
            for line in file:
                yield line.strip()
    
    # Generator expression
    squares = (x**2 for x in range(1000000))
    
    # Memory comparison
    def memory_efficient_processing():
        # Instead of loading all data into memory
        # data = [process_record(line) for line in open('huge_file.txt')]
        
        # Use generator for memory efficiency
        processed_data = (process_record(line) for line in open('huge_file.txt'))
        return processed_data
    
    # Pipeline of generators
    def data_pipeline(source):
        # Filter valid records
        valid_records = (record for record in source if is_valid(record))
        
        # Transform records
        transformed = (transform_record(record) for record in valid_records)
        
        # Batch records
        batch_size = 1000
        batch = []
        for record in transformed:
            batch.append(record)
            if len(batch) >= batch_size:
                yield batch
                batch = []
        if batch:
            yield batch

def process_record(record):
    return record.upper()

def is_valid(record):
    return len(record) > 0

def transform_record(record):
    return {"data": record, "processed": True}
```

### 8. Explain Python's context managers and the `with` statement.

**Answer:** Context managers ensure proper resource management using `__enter__` and `__exit__` methods.

```python
import contextlib
from contextlib import contextmanager

class DatabaseConnection:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None
    
    def __enter__(self):
        print(f"Connecting to {self.connection_string}")
        self.connection = f"Connected to {self.connection_string}"
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing database connection")
        if exc_type:
            print(f"Exception occurred: {exc_val}")
        self.connection = None
        return False  # Don't suppress exceptions

@contextmanager
def file_processor(filename):
    print(f"Opening file: {filename}")
    file_handle = open(filename, 'r')
    try:
        yield file_handle
    finally:
        print(f"Closing file: {filename}")
        file_handle.close()

# Usage examples
def demonstrate_context_managers():
    # Custom context manager
    with DatabaseConnection("postgresql://localhost/db") as conn:
        print(f"Using connection: {conn}")
    
    # Context manager decorator
    with file_processor("data.txt") as f:
        content = f.read()
    
    # Multiple context managers
    with open("input.txt") as infile, open("output.txt", "w") as outfile:
        outfile.write(infile.read().upper())
```

### 9. What is the difference between `==` and `is` in Python?

**Answer:** `==` compares values while `is` compares object identity (memory location).

```python
def demonstrate_equality_vs_identity():
    # Value equality vs identity
    a = [1, 2, 3]
    b = [1, 2, 3]
    c = a
    
    print(f"a == b: {a == b}")  # True (same values)
    print(f"a is b: {a is b}")  # False (different objects)
    print(f"a is c: {a is c}")  # True (same object)
    
    # Small integers are cached
    x = 100
    y = 100
    print(f"x is y: {x is y}")  # True (cached)
    
    # Large integers are not cached
    x = 1000
    y = 1000
    print(f"x is y: {x is y}")  # False (not cached)
    
    # None comparison (always use 'is')
    value = None
    print(f"value is None: {value is None}")  # Correct
    print(f"value == None: {value == None}")  # Works but not recommended
    
    # Custom equality
    class DataRecord:
        def __init__(self, id, data):
            self.id = id
            self.data = data
        
        def __eq__(self, other):
            return isinstance(other, DataRecord) and self.id == other.id
    
    record1 = DataRecord(1, "data")
    record2 = DataRecord(1, "different_data")
    print(f"record1 == record2: {record1 == record2}")  # True (same ID)
    print(f"record1 is record2: {record1 is record2}")  # False (different objects)
```

### 10. Explain Python's lambda functions and their use cases.

**Answer:** Lambda functions are anonymous functions defined using the `lambda` keyword.

```python
def demonstrate_lambda_functions():
    # Basic lambda functions
    square = lambda x: x ** 2
    add = lambda x, y: x + y
    
    # Lambda with built-in functions
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # map() with lambda
    squared = list(map(lambda x: x ** 2, numbers))
    
    # filter() with lambda
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    
    # sorted() with lambda
    employees = [
        {'name': 'Alice', 'salary': 70000},
        {'name': 'Bob', 'salary': 60000},
        {'name': 'Charlie', 'salary': 80000}
    ]
    
    # Sort by salary
    by_salary = sorted(employees, key=lambda emp: emp['salary'])
    
    # Data processing with lambda
    data_transformations = {
        'uppercase': lambda x: x.upper(),
        'lowercase': lambda x: x.lower(),
        'reverse': lambda x: x[::-1]
    }
    
    def apply_transformation(data, transform_name):
        transform_func = data_transformations.get(transform_name)
        return transform_func(data) if transform_func else data
    
    # Lambda in closures
    def create_multiplier(factor):
        return lambda x: x * factor
    
    double = create_multiplier(2)
    triple = create_multiplier(3)
    
    print(f"Double 5: {double(5)}")
    print(f"Triple 5: {triple(5)}")
```
