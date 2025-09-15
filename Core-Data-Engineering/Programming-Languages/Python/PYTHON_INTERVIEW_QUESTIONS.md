# Python Interview Questions for Data Engineers

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
# Example: Simple ETL pipeline
import pandas as pd
from sqlalchemy import create_engine

def simple_etl_pipeline():
    # Extract
    df = pd.read_csv('source_data.csv')
    
    # Transform
    df['processed_date'] = pd.to_datetime(df['date'])
    df['amount_usd'] = df['amount'] * df['exchange_rate']
    
    # Load
    engine = create_engine('postgresql://user:pass@localhost/db')
    df.to_sql('processed_data', engine, if_exists='append', index=False)
    
    return f"Processed {len(df)} records"
```

### 2. Explain Python's memory management and garbage collection.

**Answer:** Python uses reference counting with cycle detection for memory management.

**Key Components:**
- **Reference Counting**: Tracks number of references to each object
- **Garbage Collector**: Handles circular references using generational collection
- **Memory Pools**: Optimizes allocation for small objects (< 512 bytes)
- **Object Interning**: Caches small integers and strings

```python
import gc
import sys

def demonstrate_memory_management():
    # Reference counting example
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
    
    # Check garbage collection
    print(f"Objects before GC: {len(gc.get_objects())}")
    collected = gc.collect()
    print(f"Objects collected: {collected}")
    
    return "Memory management demonstrated"
```

### 3. What is the Global Interpreter Lock (GIL) and how does it affect performance?

**Answer:** The GIL is a mutex that prevents multiple native threads from executing Python bytecodes simultaneously.

**Impact on Performance:**
- **CPU-bound tasks**: Limited to single-core performance
- **I/O-bound tasks**: Less affected due to GIL release during I/O operations
- **Threading limitations**: True parallelism not possible for CPU tasks

**Workarounds:**
```python
import threading
import multiprocessing
import time
import concurrent.futures

def cpu_intensive_task(n):
    """CPU-bound task affected by GIL"""
    total = 0
    for i in range(n):
        total += i ** 2
    return total

def compare_concurrency_approaches():
    tasks = [1000000] * 4
    
    # Sequential execution
    start = time.time()
    sequential_results = [cpu_intensive_task(n) for n in tasks]
    sequential_time = time.time() - start
    
    # Threading (limited by GIL)
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        thread_results = list(executor.map(cpu_intensive_task, tasks))
    thread_time = time.time() - start
    
    # Multiprocessing (bypasses GIL)
    start = time.time()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        process_results = list(executor.map(cpu_intensive_task, tasks))
    process_time = time.time() - start
    
    print(f"Sequential: {sequential_time:.2f}s")
    print(f"Threading: {thread_time:.2f}s")
    print(f"Multiprocessing: {process_time:.2f}s")
    print(f"Multiprocessing speedup: {sequential_time/process_time:.2f}x")
```

### 4. Explain the difference between lists, tuples, sets, and dictionaries.

**Answer:** Python's core data structures have different characteristics and use cases.

```python
def compare_data_structures():
    # Lists - Ordered, mutable, allow duplicates
    numbers_list = [1, 2, 3, 2, 4]
    numbers_list.append(5)
    numbers_list[0] = 10
    print(f"List: {numbers_list}")
    
    # Tuples - Ordered, immutable, allow duplicates
    coordinates = (10.5, 20.3, 10.5)
    # coordinates[0] = 15  # Error: tuples are immutable
    print(f"Tuple: {coordinates}")
    
    # Sets - Unordered, mutable, unique elements only
    unique_numbers = {1, 2, 3, 2, 4}  # Duplicate 2 removed
    unique_numbers.add(5)
    print(f"Set: {unique_numbers}")
    
    # Dictionaries - Key-value pairs, ordered (Python 3.7+)
    person = {'name': 'Alice', 'age': 30, 'city': 'NYC'}
    person['email'] = 'alice@example.com'
    print(f"Dict: {person}")
    
    # Performance comparison
    import time
    
    # List membership test O(n)
    large_list = list(range(100000))
    start = time.time()
    result = 99999 in large_list
    list_time = time.time() - start
    
    # Set membership test O(1)
    large_set = set(range(100000))
    start = time.time()
    result = 99999 in large_set
    set_time = time.time() - start
    
    print(f"List lookup: {list_time:.6f}s")
    print(f"Set lookup: {set_time:.6f}s")
    print(f"Set is {list_time/set_time:.0f}x faster")
```

### 5. What are Python decorators and how do you use them in data engineering?

**Answer:** Decorators are functions that modify or enhance other functions without changing their source code.

```python
from functools import wraps
import time
import logging

# Timing decorator for performance monitoring
def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

# Retry decorator for fault tolerance
def retry_decorator(max_attempts=3, delay=1):
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
                    time.sleep(delay)
        return wrapper
    return decorator

# Logging decorator for audit trails
def log_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Executing {func.__name__} with args: {args}")
        try:
            result = func(*args, **kwargs)
            logging.info(f"{func.__name__} completed successfully")
            return result
        except Exception as e:
            logging.error(f"{func.__name__} failed: {e}")
            raise
    return wrapper

# Usage in data engineering
@timing_decorator
@retry_decorator(max_attempts=3, delay=2)
@log_execution
def process_data_batch(data_batch):
    # Simulate data processing
    if len(data_batch) == 0:
        raise ValueError("Empty data batch")
    
    processed = [item * 2 for item in data_batch]
    return processed

# Example usage
try:
    result = process_data_batch([1, 2, 3, 4, 5])
    print(f"Processed result: {result}")
except Exception as e:
    print(f"Processing failed: {e}")
```

### 6. Explain Python's `*args` and `**kwargs` with practical examples.

**Answer:** `*args` and `**kwargs` allow functions to accept variable numbers of arguments.

```python
def demonstrate_args_kwargs():
    # *args - Variable positional arguments
    def calculate_statistics(*args):
        if not args:
            return None
        
        total = sum(args)
        count = len(args)
        average = total / count
        
        return {
            'sum': total,
            'count': count,
            'average': average,
            'min': min(args),
            'max': max(args)
        }
    
    # **kwargs - Variable keyword arguments
    def create_database_connection(**kwargs):
        required_params = {'host', 'database', 'username'}
        provided_params = set(kwargs.keys())
        
        if not required_params.issubset(provided_params):
            missing = required_params - provided_params
            raise ValueError(f"Missing required parameters: {missing}")
        
        connection_string = (
            f"postgresql://{kwargs['username']}:{kwargs.get('password', '')}@"
            f"{kwargs['host']}:{kwargs.get('port', 5432)}/{kwargs['database']}"
        )
        
        return connection_string
    
    # Combined usage for flexible data processing
    def process_dataset(dataset_name, *transformations, **options):
        print(f"Processing dataset: {dataset_name}")
        print(f"Transformations: {transformations}")
        print(f"Options: {options}")
        
        # Apply transformations
        data = list(range(10))  # Sample data
        for transform in transformations:
            if transform == 'square':
                data = [x**2 for x in data]
            elif transform == 'filter_even':
                data = [x for x in data if x % 2 == 0]
        
        # Apply options
        if options.get('limit'):
            data = data[:options['limit']]
        
        return data
    
    # Examples
    print("=== Statistics Example ===")
    stats = calculate_statistics(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    print(f"Statistics: {stats}")
    
    print("\n=== Database Connection Example ===")
    conn_str = create_database_connection(
        host='localhost',
        database='warehouse',
        username='admin',
        password='secret',
        port=5432
    )
    print(f"Connection string: {conn_str}")
    
    print("\n=== Flexible Processing Example ===")
    result = process_dataset(
        'sales_data',
        'square',
        'filter_even',
        limit=5,
        format='json'
    )
    print(f"Processed data: {result}")

demonstrate_args_kwargs()
```

### 7. What are Python generators and why are they important for data engineering?

**Answer:** Generators are functions that yield values one at a time, providing memory-efficient iteration for large datasets.

```python
import sys
import csv

def demonstrate_generators():
    # Basic generator function
    def fibonacci_generator(n):
        a, b = 0, 1
        count = 0
        while count < n:
            yield a
            a, b = b, a + b
            count += 1
    
    # Generator for processing large files
    def read_large_csv(filename, chunk_size=1000):
        """Memory-efficient CSV reading"""
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            chunk = []
            
            for row in reader:
                chunk.append(row)
                if len(chunk) >= chunk_size:
                    yield chunk
                    chunk = []
            
            # Yield remaining rows
            if chunk:
                yield chunk
    
    # Data processing pipeline with generators
    def data_processing_pipeline(data_source):
        # Filter valid records
        def filter_valid(records):
            for record in records:
                if record.get('amount') and float(record['amount']) > 0:
                    yield record
        
        # Transform records
        def transform_records(records):
            for record in records:
                transformed = {
                    'id': record['id'],
                    'amount': float(record['amount']),
                    'processed_date': '2024-01-01',
                    'category': record.get('category', 'unknown')
                }
                yield transformed
        
        # Apply pipeline
        valid_records = filter_valid(data_source)
        transformed_records = transform_records(valid_records)
        
        return transformed_records
    
    # Memory comparison: list vs generator
    def memory_comparison():
        # List approach - loads everything into memory
        squares_list = [x**2 for x in range(1000000)]
        list_size = sys.getsizeof(squares_list)
        
        # Generator approach - generates on demand
        squares_gen = (x**2 for x in range(1000000))
        gen_size = sys.getsizeof(squares_gen)
        
        print(f"List size: {list_size:,} bytes")
        print(f"Generator size: {gen_size:,} bytes")
        print(f"Memory savings: {list_size/gen_size:.0f}x")
    
    # Examples
    print("=== Fibonacci Generator ===")
    fib_gen = fibonacci_generator(10)
    fib_numbers = list(fib_gen)
    print(f"First 10 Fibonacci numbers: {fib_numbers}")
    
    print("\n=== Memory Comparison ===")
    memory_comparison()
    
    print("\n=== Generator Pipeline ===")
    # Sample data
    sample_data = [
        {'id': '1', 'amount': '100.50', 'category': 'A'},
        {'id': '2', 'amount': '0', 'category': 'B'},
        {'id': '3', 'amount': '250.75', 'category': 'A'},
        {'id': '4', 'amount': '-50', 'category': 'C'},
    ]
    
    pipeline = data_processing_pipeline(sample_data)
    results = list(pipeline)
    print(f"Pipeline results: {results}")

demonstrate_generators()
```

### 8. Explain Python's context managers and the `with` statement.

**Answer:** Context managers ensure proper resource management using `__enter__` and `__exit__` methods.

```python
import contextlib
import time
import logging

def demonstrate_context_managers():
    # Custom context manager class
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
                # Log the error but don't suppress it
                logging.error(f"Database operation failed: {exc_val}")
            self.connection = None
            return False  # Don't suppress exceptions
    
    # Context manager using contextlib decorator
    @contextlib.contextmanager
    def timing_context(operation_name):
        print(f"Starting {operation_name}")
        start_time = time.time()
        try:
            yield start_time
        finally:
            end_time = time.time()
            print(f"{operation_name} took {end_time - start_time:.4f} seconds")
    
    # File processing context manager
    @contextlib.contextmanager
    def batch_file_processor(input_file, output_file, batch_size=1000):
        input_handle = None
        output_handle = None
        try:
            input_handle = open(input_file, 'r')
            output_handle = open(output_file, 'w')
            
            processor = {
                'input': input_handle,
                'output': output_handle,
                'batch_size': batch_size,
                'processed_count': 0
            }
            
            yield processor
            
        finally:
            if input_handle:
                input_handle.close()
            if output_handle:
                output_handle.close()
            print(f"Processed {processor.get('processed_count', 0)} records")
    
    # Multiple context managers
    @contextlib.contextmanager
    def managed_resource(name):
        print(f"Acquiring {name}")
        try:
            yield name
        finally:
            print(f"Releasing {name}")
    
    # Examples
    print("=== Database Context Manager ===")
    with DatabaseConnection("postgresql://localhost:5432/db") as conn:
        print(f"Using connection: {conn}")
        time.sleep(0.1)  # Simulate work
    
    print("\n=== Timing Context Manager ===")
    with timing_context("data processing"):
        total = sum(range(100000))
        print(f"Calculated sum: {total}")
    
    print("\n=== Multiple Context Managers ===")
    with managed_resource("Database"), managed_resource("Cache"):
        print("Using both resources")
    
    print("\n=== Exception Handling ===")
    try:
        with DatabaseConnection("postgresql://localhost:5432/db") as conn:
            print(f"Using connection: {conn}")
            raise ValueError("Simulated error!")
    except ValueError as e:
        print(f"Caught exception: {e}")

demonstrate_context_managers()
```

### 9. What is the difference between `==` and `is` in Python?

**Answer:** `==` compares values while `is` compares object identity (memory location).

```python
def demonstrate_equality_vs_identity():
    # Value equality vs identity with lists
    a = [1, 2, 3]
    b = [1, 2, 3]
    c = a
    
    print("=== Lists ===")
    print(f"a == b: {a == b}")  # True (same values)
    print(f"a is b: {a is b}")  # False (different objects)
    print(f"a is c: {a is c}")  # True (same object)
    print(f"id(a): {id(a)}, id(b): {id(b)}, id(c): {id(c)}")
    
    # Small integers are cached (-5 to 256)
    print("\n=== Small Integers (cached) ===")
    x = 100
    y = 100
    print(f"x == y: {x == y}")  # True
    print(f"x is y: {x is y}")  # True (cached)
    print(f"id(x): {id(x)}, id(y): {id(y)}")
    
    # Large integers are not cached
    print("\n=== Large Integers (not cached) ===")
    x = 1000
    y = 1000
    print(f"x == y: {x == y}")  # True
    print(f"x is y: {x is y}")  # False (not cached)
    print(f"id(x): {id(x)}, id(y): {id(y)}")
    
    # String interning
    print("\n=== Strings ===")
    s1 = "hello"
    s2 = "hello"
    s3 = "hel" + "lo"
    s4 = "hello world"
    s5 = "hello world"
    
    print(f"s1 == s2: {s1 == s2}")  # True
    print(f"s1 is s2: {s1 is s2}")  # True (interned)
    print(f"s1 is s3: {s1 is s3}")  # True (interned)
    print(f"s4 is s5: {s4 is s5}")  # May be True or False
    
    # None comparison (always use 'is')
    print("\n=== None Comparison ===")
    value = None
    print(f"value == None: {value == None}")  # True but not recommended
    print(f"value is None: {value is None}")  # True and recommended
    
    # Custom class with __eq__ method
    class DataRecord:
        def __init__(self, id, value):
            self.id = id
            self.value = value
        
        def __eq__(self, other):
            if isinstance(other, DataRecord):
                return self.id == other.id and self.value == other.value
            return False
        
        def __repr__(self):
            return f"DataRecord(id={self.id}, value={self.value})"
    
    print("\n=== Custom Objects ===")
    record1 = DataRecord(1, "data")
    record2 = DataRecord(1, "data")
    record3 = record1
    
    print(f"record1 == record2: {record1 == record2}")  # True (custom __eq__)
    print(f"record1 is record2: {record1 is record2}")  # False (different objects)
    print(f"record1 is record3: {record1 is record3}")  # True (same object)

demonstrate_equality_vs_identity()
```

### 10. Explain Python's lambda functions and their use cases in data processing.

**Answer:** Lambda functions are anonymous functions defined using the `lambda` keyword, useful for short, simple operations.

```python
def demonstrate_lambda_functions():
    # Basic lambda functions
    square = lambda x: x ** 2
    add = lambda x, y: x + y
    
    print(f"Square of 5: {square(5)}")
    print(f"Add 3 and 4: {add(3, 4)}")
    
    # Lambda with built-in functions for data processing
    sales_data = [
        {'product': 'laptop', 'price': 1200, 'quantity': 5},
        {'product': 'mouse', 'price': 25, 'quantity': 50},
        {'product': 'keyboard', 'price': 75, 'quantity': 20},
        {'product': 'monitor', 'price': 300, 'quantity': 8}
    ]
    
    # map() with lambda - calculate total value
    total_values = list(map(lambda item: item['price'] * item['quantity'], sales_data))
    print(f"Total values: {total_values}")
    
    # filter() with lambda - high-value items
    high_value_items = list(filter(lambda item: item['price'] > 100, sales_data))
    print(f"High-value items: {[item['product'] for item in high_value_items]}")
    
    # sorted() with lambda - sort by total value
    sorted_by_value = sorted(sales_data, key=lambda item: item['price'] * item['quantity'], reverse=True)
    print(f"Sorted by total value: {[item['product'] for item in sorted_by_value]}")
    
    # Data transformation pipeline
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Chain operations using lambda
    result = list(
        map(lambda x: x ** 2,                    # Square
            filter(lambda x: x % 2 == 0,         # Filter even
                   map(lambda x: x * 2, numbers) # Double
                  )
           )
    )
    print(f"Pipeline result: {result}")
    
    # Lambda in pandas-style operations (simulated)
    def apply_operation(data, operation):
        return [operation(item) for item in data]
    
    # Data cleaning operations
    raw_data = ['  Alice  ', '  BOB  ', '  charlie  ', '  DIANA  ']
    
    # Clean and normalize names
    cleaned_names = apply_operation(
        raw_data,
        lambda name: name.strip().title()
    )
    print(f"Cleaned names: {cleaned_names}")
    
    # Lambda with conditional expressions
    categorize_age = lambda age: 'child' if age < 18 else 'adult' if age < 65 else 'senior'
    ages = [5, 25, 45, 70, 15, 80]
    categories = list(map(categorize_age, ages))
    print(f"Age categories: {list(zip(ages, categories))}")
    
    # Lambda limitations and alternatives
    print("\n=== Lambda Limitations ===")
    
    # Lambda can only contain expressions, not statements
    # This won't work: lambda x: print(x)  # print is a statement
    
    # Alternative: regular function for complex logic
    def complex_data_processor(record):
        # Multiple statements and complex logic
        if not isinstance(record, dict):
            return None
        
        processed = {
            'id': record.get('id', 'unknown'),
            'value': record.get('value', 0) * 1.1,  # Apply 10% markup
            'category': record.get('category', 'default').upper(),
            'processed_at': '2024-01-01'
        }
        
        return processed
    
    # Lambda in closures for configuration
    def create_data_validator(min_value, max_value):
        return lambda x: min_value <= x <= max_value
    
    price_validator = create_data_validator(0, 10000)
    quantity_validator = create_data_validator(1, 1000)
    
    print(f"Price 500 valid: {price_validator(500)}")
    print(f"Quantity 2000 valid: {quantity_validator(2000)}")

demonstrate_lambda_functions()
```
