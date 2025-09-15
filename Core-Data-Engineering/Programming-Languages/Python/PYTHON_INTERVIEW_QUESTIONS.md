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

*Questions 1-30 completed (Basic Level). Intermediate level questions 21-30 cover advanced language features and optimization techniques.*

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

### 11. What are Python list comprehensions and how do they compare to traditional loops?

**Answer:** List comprehensions provide a concise way to create lists using a single line of code.

```python
def demonstrate_list_comprehensions():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Traditional loop
    squares_loop = []
    for x in numbers:
        squares_loop.append(x ** 2)
    
    # List comprehension
    squares_comp = [x ** 2 for x in numbers]
    
    print(f"Loop result: {squares_loop}")
    print(f"Comprehension result: {squares_comp}")
    
    # Conditional list comprehensions
    evens = [x for x in numbers if x % 2 == 0]
    print(f"Even numbers: {evens}")
    
    # Dictionary comprehension
    word_lengths = {word: len(word) for word in ['python', 'data', 'engineering']}
    print(f"Word lengths: {word_lengths}")

demonstrate_list_comprehensions()
```

### 12. Explain Python's exception handling and best practices.

**Answer:** Exception handling allows graceful error management using try/except blocks.

```python
def demonstrate_exception_handling():
    def safe_divide(a, b):
        try:
            result = a / b
            return result
        except ZeroDivisionError:
            print("Cannot divide by zero")
            return None
        except TypeError:
            print("Invalid types for division")
            return None
    
    class DataValidationError(Exception):
        def __init__(self, message, field_name=None):
            self.message = message
            self.field_name = field_name
            super().__init__(self.message)
    
    print(safe_divide(10, 2))
    print(safe_divide(10, 0))

demonstrate_exception_handling()
```

### 13. What are Python modules and packages?

**Answer:** Modules are Python files containing code, while packages are directories containing multiple modules.

```python
# Example module structure:
# my_data_package/
# ├── __init__.py
# ├── extractors.py
# └── transformers.py

# extractors.py
def extract_from_csv(file_path):
    import pandas as pd
    return pd.read_csv(file_path)

# __init__.py
from .extractors import extract_from_csv
__version__ = "1.0.0"
```

### 14. What is the difference between shallow and deep copy?

**Answer:** Shallow copy creates a new object but references nested objects, while deep copy creates independent copies.

```python
import copy

def demonstrate_copy_behavior():
    original = {'users': [{'name': 'Alice'}], 'config': {'timeout': 30}}
    
    shallow = copy.copy(original)
    deep = copy.deepcopy(original)
    
    # Modify nested object
    original['users'][0]['name'] = 'Modified'
    
    print(f"Original: {original}")
    print(f"Shallow: {shallow}")   # Nested objects changed
    print(f"Deep: {deep}")        # Unchanged

demonstrate_copy_behavior()
```

### 15. Explain Python's `__str__` and `__repr__` methods.

**Answer:** `__str__` provides human-readable string representation, while `__repr__` provides unambiguous representation for developers.

```python
class DataRecord:
    def __init__(self, id, value, category):
        self.id = id
        self.value = value
        self.category = category
    
    def __str__(self):
        return f"Record {self.id}: {self.value} ({self.category})"
    
    def __repr__(self):
        return f"DataRecord(id={self.id!r}, value={self.value!r}, category={self.category!r})"

# Usage
record = DataRecord(1, 100.5, "sales")
print(str(record))   # Human-readable
print(repr(record))  # Developer representation
```

### 16. What are Python's magic methods (dunder methods)?

**Answer:** Magic methods are special methods with double underscores that define how objects behave with built-in operations.

```python
class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        return self.data[index]
    
    def __setitem__(self, index, value):
        self.data[index] = value
    
    def __contains__(self, item):
        return item in self.data
    
    def __add__(self, other):
        return DataProcessor(self.data + other.data)

# Usage
processor = DataProcessor([1, 2, 3, 4, 5])
print(len(processor))      # Calls __len__
print(processor[0])       # Calls __getitem__
print(3 in processor)     # Calls __contains__
```

### 17. Explain Python's property decorator and descriptors.

**Answer:** Properties provide controlled access to attributes, while descriptors define how attribute access is handled.

```python
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius
    
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature cannot be below absolute zero")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        return (self._celsius * 9/5) + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9

# Usage
temp = Temperature(25)
print(f"Celsius: {temp.celsius}")
print(f"Fahrenheit: {temp.fahrenheit}")
temp.fahrenheit = 100
print(f"New Celsius: {temp.celsius}")
```

### 18. What is the difference between `@staticmethod` and `@classmethod`?

**Answer:** `@staticmethod` doesn't receive any automatic arguments, while `@classmethod` receives the class as the first argument.

```python
class DataValidator:
    validation_rules = {'min_length': 3, 'max_length': 50}
    
    def __init__(self, name):
        self.name = name
    
    @staticmethod
    def is_valid_email(email):
        """Static method - utility function"""
        return '@' in email and '.' in email
    
    @classmethod
    def from_config(cls, config_dict):
        """Class method - alternative constructor"""
        name = config_dict.get('validator_name', 'default')
        return cls(name)
    
    @classmethod
    def get_validation_rule(cls, rule_name):
        """Class method - access class attributes"""
        return cls.validation_rules.get(rule_name)
    
    def validate_instance(self, data):
        """Instance method - access instance attributes"""
        return len(data) >= self.validation_rules['min_length']

# Usage
print(DataValidator.is_valid_email('test@example.com'))  # Static method
validator = DataValidator.from_config({'validator_name': 'email_validator'})  # Class method
print(DataValidator.get_validation_rule('min_length'))  # Class method
```

### 19. Explain Python's multiple inheritance and Method Resolution Order (MRO).

**Answer:** Multiple inheritance allows a class to inherit from multiple parent classes. MRO determines the order in which methods are resolved.

```python
class DataExtractor:
    def extract(self):
        return "Extracting data"
    
    def process(self):
        return "DataExtractor processing"

class DataTransformer:
    def transform(self):
        return "Transforming data"
    
    def process(self):
        return "DataTransformer processing"

class DataLoader:
    def load(self):
        return "Loading data"
    
    def process(self):
        return "DataLoader processing"

class ETLPipeline(DataExtractor, DataTransformer, DataLoader):
    def run_pipeline(self):
        return f"{self.extract()} -> {self.transform()} -> {self.load()}"
    
    def process(self):
        return "ETLPipeline processing"

# Usage
pipeline = ETLPipeline()
print(pipeline.run_pipeline())
print(pipeline.process())  # Uses ETLPipeline's method
print(ETLPipeline.__mro__)  # Method Resolution Order
```

### 20. What are Python's iterators and how do you create custom iterators?

**Answer:** Iterators are objects that implement the iterator protocol with `__iter__` and `__next__` methods.

```python
class DataBatchIterator:
    def __init__(self, data, batch_size):
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

class DataStream:
    def __init__(self, data):
        self.data = data
    
    def __iter__(self):
        return DataBatchIterator(self.data, batch_size=3)

# Usage
data_stream = DataStream(list(range(10)))
for batch in data_stream:
    print(f"Processing batch: {batch}")

# Manual iteration
iterator = iter(data_stream)
print(f"First batch: {next(iterator)}")
print(f"Second batch: {next(iterator)}")
```

---

## Intermediate Level Questions (51-100)

### 21. Explain Python's asyncio and asynchronous programming.

**Answer:** Asyncio enables asynchronous programming using async/await syntax for concurrent I/O operations.

```python
import asyncio
import aiohttp
import time

async def fetch_data(session, url):
    """Asynchronous HTTP request"""
    async with session.get(url) as response:
        return await response.text()

async def process_urls_async(urls):
    """Process multiple URLs concurrently"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    return results

def process_urls_sync(urls):
    """Process URLs synchronously for comparison"""
    import requests
    results = []
    for url in urls:
        response = requests.get(url)
        results.append(response.text)
    return results

# Async data processing pipeline
async def async_data_pipeline():
    # Simulate async data extraction
    async def extract_data():
        await asyncio.sleep(1)  # Simulate I/O
        return [1, 2, 3, 4, 5]
    
    # Simulate async data transformation
    async def transform_data(data):
        await asyncio.sleep(0.5)  # Simulate processing
        return [x * 2 for x in data]
    
    # Simulate async data loading
    async def load_data(data):
        await asyncio.sleep(0.5)  # Simulate I/O
        return f"Loaded {len(data)} records"
    
    # Run pipeline
    raw_data = await extract_data()
    transformed_data = await transform_data(raw_data)
    result = await load_data(transformed_data)
    return result

# Usage
result = asyncio.run(async_data_pipeline())
print(result)
```

### 22. What are Python metaclasses and when would you use them?

**Answer:** Metaclasses are classes whose instances are classes themselves. They control class creation and behavior.

```python
class DataModelMeta(type):
    """Metaclass for data models with automatic validation"""
    
    def __new__(mcs, name, bases, attrs):
        # Add validation methods to all data model classes
        if name != 'BaseDataModel':
            attrs['_fields'] = {k: v for k, v in attrs.items() 
                              if not k.startswith('_') and not callable(v)}
            attrs['validate'] = mcs.create_validator(attrs['_fields'])
        
        return super().__new__(mcs, name, bases, attrs)
    
    @staticmethod
    def create_validator(fields):
        def validate(self):
            for field_name, expected_type in fields.items():
                value = getattr(self, field_name, None)
                if value is not None and not isinstance(value, expected_type):
                    raise TypeError(f"{field_name} must be {expected_type.__name__}")
            return True
        return validate

class BaseDataModel(metaclass=DataModelMeta):
    pass

class User(BaseDataModel):
    name: str = ""
    age: int = 0
    email: str = ""
    
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

# Usage
user = User("Alice", 30, "alice@example.com")
print(user.validate())  # Automatically added by metaclass
print(user._fields)     # Automatically detected fields
```

### 23. Explain Python's descriptor protocol in detail.

**Answer:** Descriptors define how attribute access is customized using `__get__`, `__set__`, and `__delete__` methods.

```python
class ValidatedAttribute:
    """Descriptor for validated attributes"""
    
    def __init__(self, validator_func, default=None):
        self.validator_func = validator_func
        self.default = default
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f'_{name}'
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name, self.default)
    
    def __set__(self, instance, value):
        if not self.validator_func(value):
            raise ValueError(f"Invalid value for {self.name}: {value}")
        setattr(instance, self.private_name, value)
    
    def __delete__(self, instance):
        delattr(instance, self.private_name)

class DataRecord:
    # Descriptors for validated attributes
    user_id = ValidatedAttribute(lambda x: isinstance(x, int) and x > 0)
    amount = ValidatedAttribute(lambda x: isinstance(x, (int, float)) and x >= 0)
    category = ValidatedAttribute(lambda x: isinstance(x, str) and len(x) > 0)
    
    def __init__(self, user_id, amount, category):
        self.user_id = user_id
        self.amount = amount
        self.category = category

# Usage
record = DataRecord(123, 99.99, "purchase")
print(f"User ID: {record.user_id}")

try:
    record.amount = -10  # Will raise ValueError
except ValueError as e:
    print(f"Validation error: {e}")
```

### 24. What are Python's weak references and when are they useful?

**Answer:** Weak references allow you to refer to an object without preventing it from being garbage collected.

```python
import weakref
import gc

class DataCache:
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()
        self._callbacks = weakref.WeakKeyDictionary()
    
    def get_or_create(self, key, factory_func):
        """Get cached object or create new one"""
        obj = self._cache.get(key)
        if obj is None:
            obj = factory_func()
            self._cache[key] = obj
            # Register cleanup callback
            weakref.finalize(obj, self._cleanup_callback, key)
        return obj
    
    def _cleanup_callback(self, key):
        print(f"Object with key '{key}' was garbage collected")

class ExpensiveDataProcessor:
    def __init__(self, data_id):
        self.data_id = data_id
        self.processed_data = [i ** 2 for i in range(1000)]  # Expensive computation
        print(f"Created processor for data_id: {data_id}")
    
    def __del__(self):
        print(f"Processor {self.data_id} is being destroyed")

# Observer pattern with weak references
class DataPublisher:
    def __init__(self):
        self._observers = weakref.WeakSet()
    
    def add_observer(self, observer):
        self._observers.add(observer)
    
    def notify(self, data):
        # Observers can be garbage collected without explicit removal
        for observer in self._observers:
            observer.update(data)

class DataObserver:
    def __init__(self, name):
        self.name = name
    
    def update(self, data):
        print(f"Observer {self.name} received: {data}")

# Usage examples
cache = DataCache()

# Create and cache objects
processor1 = cache.get_or_create("data1", lambda: ExpensiveDataProcessor("data1"))
processor2 = cache.get_or_create("data1", lambda: ExpensiveDataProcessor("data1"))  # Returns cached

print(f"Same object: {processor1 is processor2}")

# When objects go out of scope, they can be garbage collected
del processor1, processor2
gc.collect()  # Force garbage collection
```

### 25. Explain Python's `functools` module and its key functions.

**Answer:** The `functools` module provides utilities for working with higher-order functions and operations on callable objects.

```python
from functools import wraps, lru_cache, partial, reduce, singledispatch
import time

# @wraps preserves function metadata
def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

# @lru_cache for memoization
@lru_cache(maxsize=128)
def expensive_calculation(n):
    """Fibonacci with memoization"""
    if n < 2:
        return n
    return expensive_calculation(n-1) + expensive_calculation(n-2)

# partial for function currying
def process_data(data, multiplier, offset):
    return [x * multiplier + offset for x in data]

# Create specialized functions
double_and_add_ten = partial(process_data, multiplier=2, offset=10)
triple_data = partial(process_data, multiplier=3, offset=0)

# reduce for aggregations
numbers = [1, 2, 3, 4, 5]
total = reduce(lambda x, y: x + y, numbers)
product = reduce(lambda x, y: x * y, numbers)

# singledispatch for function overloading
@singledispatch
def process_input(data):
    raise NotImplementedError(f"Cannot process type {type(data)}")

@process_input.register
def _(data: list):
    return f"Processing list with {len(data)} items"

@process_input.register
def _(data: dict):
    return f"Processing dict with keys: {list(data.keys())}"

@process_input.register
def _(data: str):
    return f"Processing string: '{data}'"

# Usage examples
print(f"Fibonacci(10): {expensive_calculation(10)}")  # Cached after first call
print(f"Doubled and offset: {double_and_add_ten([1, 2, 3])}")
print(f"Total: {total}, Product: {product}")
print(process_input([1, 2, 3]))
print(process_input({"a": 1, "b": 2}))
print(process_input("hello"))
```

### 26. Explain Python's `collections` module and its key data structures.

**Answer:** The `collections` module provides specialized container datatypes.

```python
from collections import defaultdict, Counter, deque, namedtuple, OrderedDict
from collections import ChainMap

def demonstrate_collections():
    # defaultdict - provides default values for missing keys
    dd = defaultdict(list)
    dd['fruits'].append('apple')
    dd['fruits'].append('banana')
    print(f"defaultdict: {dict(dd)}")
    
    # Counter - counts hashable objects
    data = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple']
    counter = Counter(data)
    print(f"Counter: {counter}")
    print(f"Most common: {counter.most_common(2)}")
    
    # deque - double-ended queue for efficient append/pop
    dq = deque([1, 2, 3])
    dq.appendleft(0)  # Add to left
    dq.append(4)      # Add to right
    print(f"deque: {dq}")
    
    # namedtuple - tuple with named fields
    Person = namedtuple('Person', ['name', 'age', 'city'])
    person = Person('Alice', 30, 'NYC')
    print(f"namedtuple: {person.name}, {person.age}")
    
    # ChainMap - combines multiple dicts
    dict1 = {'a': 1, 'b': 2}
    dict2 = {'b': 3, 'c': 4}
    chain = ChainMap(dict1, dict2)
    print(f"ChainMap: {dict(chain)}")  # dict1 takes precedence

demonstrate_collections()
```

### 27. What is the difference between `staticmethod` and `classmethod`?

**Answer:** `@staticmethod` doesn't receive class/instance, `@classmethod` receives class as first argument.

```python
class DataProcessor:
    default_batch_size = 1000
    
    def __init__(self, name):
        self.name = name
    
    @staticmethod
    def validate_data(data):
        """Static method - utility function"""
        return isinstance(data, (list, tuple)) and len(data) > 0
    
    @classmethod
    def create_default(cls):
        """Class method - alternative constructor"""
        return cls("DefaultProcessor")
    
    @classmethod
    def get_batch_size(cls):
        """Class method - access class attributes"""
        return cls.default_batch_size
    
    def process(self, data):
        """Instance method - access instance attributes"""
        if self.validate_data(data):
            return f"{self.name} processed {len(data)} items"
        return "Invalid data"

# Usage
print(DataProcessor.validate_data([1, 2, 3]))  # Static method
processor = DataProcessor.create_default()      # Class method
print(DataProcessor.get_batch_size())          # Class method
print(processor.process([1, 2, 3, 4, 5]))      # Instance method
```

### 28. Explain Python's multiple inheritance and Method Resolution Order (MRO).

**Answer:** Multiple inheritance allows inheriting from multiple classes. MRO determines method lookup order.

```python
class DataExtractor:
    def extract(self):
        return "Extracting data"
    
    def process(self):
        return "DataExtractor processing"

class DataTransformer:
    def transform(self):
        return "Transforming data"
    
    def process(self):
        return "DataTransformer processing"

class DataLoader:
    def load(self):
        return "Loading data"
    
    def process(self):
        return "DataLoader processing"

# Multiple inheritance
class ETLPipeline(DataExtractor, DataTransformer, DataLoader):
    def run_pipeline(self):
        return f"{self.extract()} -> {self.transform()} -> {self.load()}"
    
    def process(self):
        # Call parent methods using super()
        return f"ETLPipeline: {super().process()}"

# Diamond problem resolution
class Base:
    def method(self):
        return "Base"

class A(Base):
    def method(self):
        return f"A -> {super().method()}"

class B(Base):
    def method(self):
        return f"B -> {super().method()}"

class C(A, B):
    def method(self):
        return f"C -> {super().method()}"

# Usage
pipeline = ETLPipeline()
print(pipeline.run_pipeline())
print(pipeline.process())  # Uses ETLPipeline's method
print(f"MRO: {ETLPipeline.__mro__}")

c = C()
print(c.method())  # C -> A -> B -> Base
print(f"C MRO: {C.__mro__}")
```

### 29. What are Python's iterators and how do you create custom iterators?

**Answer:** Iterators implement `__iter__` and `__next__` methods for custom iteration.

```python
class DataBatchIterator:
    def __init__(self, data, batch_size):
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
        
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return result

# Iterator vs Iterable
class DataStream:
    def __init__(self, data):
        self.data = data
    
    def __iter__(self):
        return DataBatchIterator(self.data, batch_size=3)

# Usage
data_stream = DataStream(list(range(10)))
for batch in data_stream:
    print(f"Processing batch: {batch}")

# Fibonacci iterator
fib = FibonacciIterator(10)
for num in fib:
    print(num, end=" ")
print()

# Manual iteration
iterator = iter(data_stream)
print(f"First batch: {next(iterator)}")
print(f"Second batch: {next(iterator)}")
```

### 30. Explain Python's `__slots__` and memory optimization.

**Answer:** `__slots__` restricts instance attributes and reduces memory usage.

```python
import sys

class RegularClass:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class SlottedClass:
    __slots__ = ['x', 'y', 'z']
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

def compare_memory_usage():
    # Create instances
    regular = RegularClass(1, 2, 3)
    slotted = SlottedClass(1, 2, 3)
    
    # Memory comparison
    regular_size = sys.getsizeof(regular) + sys.getsizeof(regular.__dict__)
    slotted_size = sys.getsizeof(slotted)
    
    print(f"Regular class size: {regular_size} bytes")
    print(f"Slotted class size: {slotted_size} bytes")
    print(f"Memory savings: {regular_size - slotted_size} bytes")
    
    # Attribute access speed (slots are faster)
    import timeit
    
    regular_time = timeit.timeit(lambda: regular.x, number=1000000)
    slotted_time = timeit.timeit(lambda: slotted.x, number=1000000)
    
    print(f"Regular access time: {regular_time:.4f}s")
    print(f"Slotted access time: {slotted_time:.4f}s")
    
    # Slots prevent dynamic attribute creation
    try:
        regular.new_attr = "allowed"
        print("Regular class: dynamic attribute added")
    except AttributeError:
        print("Regular class: dynamic attribute failed")
    
    try:
        slotted.new_attr = "not allowed"
        print("Slotted class: dynamic attribute added")
    except AttributeError:
        print("Slotted class: dynamic attribute prevented")

# Data class with slots for large datasets
class DataPoint:
    __slots__ = ['timestamp', 'value', 'category']
    
    def __init__(self, timestamp, value, category):
        self.timestamp = timestamp
        self.value = value
        self.category = category
    
    def __repr__(self):
        return f"DataPoint({self.timestamp}, {self.value}, {self.category})"

compare_memory_usage()
```

### 26. How do you handle large datasets that don't fit in memory?

**Answer:** Use chunking, streaming, or distributed processing techniques.

```python
import pandas as pd
from typing import Iterator

def process_large_csv_in_chunks(filename: str, chunk_size: int = 10000) -> Iterator[pd.DataFrame]:
    """Process large CSV files in chunks"""
    for chunk in pd.read_csv(filename, chunksize=chunk_size):
        # Process each chunk
        processed_chunk = chunk.dropna()
        processed_chunk['processed_date'] = pd.to_datetime(processed_chunk['date'])
        yield processed_chunk

def streaming_file_processor(filename: str):
    """Stream process large files line by line"""
    with open(filename, 'r') as file:
        for line_num, line in enumerate(file, 1):
            # Process line
            processed_line = line.strip().upper()
            
            # Yield every 1000 lines to manage memory
            if line_num % 1000 == 0:
                yield processed_line

# Usage with Dask for parallel processing
try:
    import dask.dataframe as dd
    
    def process_with_dask(filename: str):
        # Read large file with Dask
        df = dd.read_csv(filename)
        
        # Lazy operations
        processed = df.dropna().map_partitions(
            lambda x: x.assign(processed_date=pd.to_datetime(x['date']))
        )
        
        # Compute result
        return processed.compute()
except ImportError:
    print("Dask not available")
```

### 27. What is the difference between `append()` and `extend()` for lists?

**Answer:** `append()` adds a single element, `extend()` adds multiple elements from an iterable.

```python
def demonstrate_append_vs_extend():
    # append() - adds single element
    list1 = [1, 2, 3]
    list1.append([4, 5])  # Adds the entire list as one element
    print(f"After append: {list1}")  # [1, 2, 3, [4, 5]]
    
    # extend() - adds elements from iterable
    list2 = [1, 2, 3]
    list2.extend([4, 5])  # Adds each element individually
    print(f"After extend: {list2}")  # [1, 2, 3, 4, 5]
    
    # Performance comparison for building large lists
    import time
    
    # Using append (slower)
    start = time.time()
    result1 = []
    for i in range(10000):
        result1.append(i)
    append_time = time.time() - start
    
    # Using extend (faster for multiple elements)
    start = time.time()
    result2 = []
    result2.extend(range(10000))
    extend_time = time.time() - start
    
    print(f"Append time: {append_time:.4f}s")
    print(f"Extend time: {extend_time:.4f}s")
    
    # Alternative: list comprehension (often fastest)
    start = time.time()
    result3 = [i for i in range(10000)]
    comprehension_time = time.time() - start
    
    print(f"Comprehension time: {comprehension_time:.4f}s")
```

### 28. Explain Python's `enumerate()` and `zip()` functions.

**Answer:** `enumerate()` adds indices to iterables, `zip()` combines multiple iterables.

```python
def demonstrate_enumerate_and_zip():
    # enumerate() - adds index to iterable
    data = ['apple', 'banana', 'cherry']
    
    for index, value in enumerate(data):
        print(f"Index {index}: {value}")
    
    # enumerate with custom start
    for index, value in enumerate(data, start=1):
        print(f"Item {index}: {value}")
    
    # zip() - combines multiple iterables
    names = ['Alice', 'Bob', 'Charlie']
    ages = [25, 30, 35]
    cities = ['NYC', 'LA', 'Chicago']
    
    for name, age, city in zip(names, ages, cities):
        print(f"{name} is {age} years old and lives in {city}")
    
    # zip() stops at shortest iterable
    numbers1 = [1, 2, 3, 4, 5]
    numbers2 = [10, 20, 30]  # Shorter list
    
    result = list(zip(numbers1, numbers2))
    print(f"Zipped result: {result}")  # [(1, 10), (2, 20), (3, 30)]
    
    # zip() for parallel processing
    def process_parallel_data(data1, data2):
        results = []
        for item1, item2 in zip(data1, data2):
            # Process paired items
            result = item1 * item2
            results.append(result)
        return results
    
    # Unzip using zip with *
    pairs = [(1, 'a'), (2, 'b'), (3, 'c')]
    numbers, letters = zip(*pairs)
    print(f"Numbers: {numbers}, Letters: {letters}")
```

### 29. What are Python's magic methods (dunder methods)?

**Answer:** Magic methods are special methods with double underscores that define object behavior.

```python
class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    def __len__(self):
        """Called by len()"""
        return len(self.data)
    
    def __getitem__(self, index):
        """Called by obj[index]"""
        return self.data[index]
    
    def __setitem__(self, index, value):
        """Called by obj[index] = value"""
        self.data[index] = value
    
    def __contains__(self, item):
        """Called by 'item in obj'"""
        return item in self.data
    
    def __str__(self):
        """Called by str() and print()"""
        return f"DataProcessor with {len(self.data)} items"
    
    def __repr__(self):
        """Called by repr() and in REPL"""
        return f"DataProcessor({self.data!r})"
    
    def __add__(self, other):
        """Called by +"""
        if isinstance(other, DataProcessor):
            return DataProcessor(self.data + other.data)
        return NotImplemented
    
    def __eq__(self, other):
        """Called by =="""
        if isinstance(other, DataProcessor):
            return self.data == other.data
        return False
    
    def __iter__(self):
        """Called by for loops and iter()"""
        return iter(self.data)
    
    def __call__(self, transform_func):
        """Makes object callable"""
        return DataProcessor([transform_func(item) for item in self.data])

# Usage examples
processor = DataProcessor([1, 2, 3, 4, 5])
print(len(processor))        # Calls __len__
print(processor[0])         # Calls __getitem__
print(3 in processor)       # Calls __contains__
print(str(processor))       # Calls __str__

# Callable object
squared = processor(lambda x: x ** 2)
print(squared.data)         # [1, 4, 9, 16, 25]
```

### 30. Explain Python's property decorator and descriptors.

**Answer:** Properties provide controlled access to attributes with getter/setter methods.

```python
class DataRecord:
    def __init__(self, value):
        self._value = value
        self._processed = False
    
    @property
    def value(self):
        """Getter for value"""
        return self._value
    
    @value.setter
    def value(self, new_value):
        """Setter with validation"""
        if not isinstance(new_value, (int, float)):
            raise TypeError("Value must be numeric")
        if new_value < 0:
            raise ValueError("Value must be non-negative")
        self._value = new_value
        self._processed = False  # Reset processed flag
    
    @property
    def processed_value(self):
        """Computed property"""
        if not self._processed:
            self._processed_value = self._value * 1.1  # Apply 10% markup
            self._processed = True
        return self._processed_value
    
    @property
    def is_processed(self):
        """Read-only property"""
        return self._processed

# Descriptor example
class ValidatedAttribute:
    def __init__(self, validator_func, default=None):
        self.validator_func = validator_func
        self.default = default
    
    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f'_{name}'
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name, self.default)
    
    def __set__(self, instance, value):
        if not self.validator_func(value):
            raise ValueError(f"Invalid value for {self.name}: {value}")
        setattr(instance, self.private_name, value)

class Customer:
    # Using descriptors for validation
    email = ValidatedAttribute(lambda x: '@' in str(x) and '.' in str(x))
    age = ValidatedAttribute(lambda x: isinstance(x, int) and 0 <= x <= 150)
    
    def __init__(self, email, age):
        self.email = email
        self.age = age

# Usage
record = DataRecord(100)
print(f"Original value: {record.value}")
print(f"Processed value: {record.processed_value}")

customer = Customer("alice@example.com", 30)
print(f"Customer: {customer.email}, Age: {customer.age}")
```
