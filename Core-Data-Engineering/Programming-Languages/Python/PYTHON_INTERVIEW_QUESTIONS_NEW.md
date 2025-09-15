# Python Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-50)](#basic-level-questions-1-50)
2. [Intermediate Level Questions (51-100)](#intermediate-level-questions-51-100)
3. [Advanced Level Questions (101-150)](#advanced-level-questions-101-150)
4. [Architecture & Performance (151-200)](#architecture--performance-151-200)
5. [Data Engineering Specific (201-250)](#data-engineering-specific-201-250)
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
# Example: Simple data pipeline
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

print(simple_etl_pipeline())
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
    
    return "Memory management demonstrated"

print(demonstrate_memory_management())
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

def cpu_intensive_task(n):
    """CPU-bound task affected by GIL"""
    total = 0
    for i in range(n):
        total += i ** 2
    return total

def io_intensive_task(duration):
    """I/O-bound task less affected by GIL"""
    time.sleep(duration)
    return f"Completed after {duration}s"

def compare_threading_vs_multiprocessing():
    tasks = [1000000, 1000000, 1000000, 1000000]
    
    # Threading (limited by GIL for CPU tasks)
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        thread_results = list(executor.map(cpu_intensive_task, tasks))
    thread_time = time.time() - start
    
    # Multiprocessing (bypasses GIL)
    start = time.time()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        process_results = list(executor.map(cpu_intensive_task, tasks))
    process_time = time.time() - start
    
    print(f"Threading time: {thread_time:.2f}s")
    print(f"Multiprocessing time: {process_time:.2f}s")
    print(f"Multiprocessing speedup: {thread_time/process_time:.2f}x")

compare_threading_vs_multiprocessing()
```

### 4. Explain the difference between lists, tuples, and sets.

**Answer:** Different data structures with distinct characteristics and use cases.

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
    
    # Performance comparison
    import time
    
    # List membership test (O(n))
    large_list = list(range(10000))
    start = time.time()
    result = 9999 in large_list
    list_time = time.time() - start
    
    # Set membership test (O(1))
    large_set = set(range(10000))
    start = time.time()
    result = 9999 in large_set
    set_time = time.time() - start
    
    print(f"List membership: {list_time:.6f}s")
    print(f"Set membership: {set_time:.6f}s")
    print(f"Set is {list_time/set_time:.0f}x faster")

compare_data_structures()
```

### 5. What are Python decorators and how do you use them?

**Answer:** Decorators are functions that modify or enhance other functions without changing their source code.

```python
from functools import wraps
import time

# Basic decorator
def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

# Decorator with parameters
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

# Class-based decorator
class CacheDecorator:
    def __init__(self, func):
        self.func = func
        self.cache = {}
    
    def __call__(self, *args):
        if args in self.cache:
            print(f"Cache hit for {args}")
            return self.cache[args]
        
        result = self.func(*args)
        self.cache[args] = result
        print(f"Cache miss for {args}")
        return result

# Usage examples
@timing_decorator
@retry_decorator(max_attempts=3, delay=0.5)
def unreliable_function(x):
    import random
    if random.random() < 0.7:  # 70% chance of failure
        raise ValueError("Random failure")
    return x ** 2

@CacheDecorator
def expensive_calculation(n):
    time.sleep(0.1)  # Simulate expensive operation
    return sum(range(n))

# Test decorators
try:
    result = unreliable_function(5)
    print(f"Result: {result}")
except ValueError as e:
    print(f"Function failed: {e}")

# Test caching
result1 = expensive_calculation(1000)  # Cache miss
result2 = expensive_calculation(1000)  # Cache hit
```

### 6. Explain Python's `*args` and `**kwargs`.

**Answer:** `*args` and `**kwargs` allow functions to accept variable numbers of arguments.

```python
def demonstrate_args_kwargs():
    # *args - Variable positional arguments
    def sum_all(*args):
        print(f"Received args: {args}")
        return sum(args)
    
    # **kwargs - Variable keyword arguments
    def process_data(**kwargs):
        print(f"Received kwargs: {kwargs}")
        for key, value in kwargs.items():
            print(f"{key}: {value}")
    
    # Combined usage
    def flexible_function(required_arg, *args, default_param="default", **kwargs):
        print(f"Required: {required_arg}")
        print(f"Optional args: {args}")
        print(f"Default param: {default_param}")
        print(f"Keyword args: {kwargs}")
    
    # Function that accepts and forwards arguments
    def wrapper_function(*args, **kwargs):
        print("Before calling target function")
        result = target_function(*args, **kwargs)
        print("After calling target function")
        return result
    
    def target_function(a, b, c=None):
        return f"a={a}, b={b}, c={c}"
    
    # Examples
    print("=== *args example ===")
    total = sum_all(1, 2, 3, 4, 5)
    print(f"Sum: {total}")
    
    print("\n=== **kwargs example ===")
    process_data(name="Alice", age=30, city="New York")
    
    print("\n=== Combined example ===")
    flexible_function("required", 1, 2, 3, default_param="custom", extra="value")
    
    print("\n=== Forwarding arguments ===")
    result = wrapper_function("hello", "world", c="!")
    print(f"Result: {result}")

demonstrate_args_kwargs()
```

### 7. What are Python generators and why are they useful?

**Answer:** Generators are functions that yield values one at a time, providing memory-efficient iteration.

```python
import sys

def demonstrate_generators():
    # Generator function
    def fibonacci_generator(n):
        a, b = 0, 1
        count = 0
        while count < n:
            yield a
            a, b = b, a + b
            count += 1
    
    # Generator expression
    squares_gen = (x**2 for x in range(1000000))
    
    # Compare memory usage: list vs generator
    def memory_comparison():
        # List approach - loads everything into memory
        squares_list = [x**2 for x in range(100000)]
        list_size = sys.getsizeof(squares_list)
        
        # Generator approach - generates on demand
        squares_gen = (x**2 for x in range(100000))
        gen_size = sys.getsizeof(squares_gen)
        
        print(f"List size: {list_size:,} bytes")
        print(f"Generator size: {gen_size:,} bytes")
        print(f"Memory savings: {list_size/gen_size:.0f}x")
    
    # Practical example: Processing large files
    def read_large_file(filename):
        """Memory-efficient file reading"""
        with open(filename, 'r') as file:
            for line_num, line in enumerate(file, 1):
                yield line_num, line.strip()
    
    # Pipeline of generators
    def data_pipeline(data):
        # Filter even numbers
        evens = (x for x in data if x % 2 == 0)
        
        # Square the numbers
        squared = (x**2 for x in evens)
        
        # Take first 10
        limited = (x for i, x in enumerate(squared) if i < 10)
        
        return limited
    
    # Examples
    print("=== Fibonacci Generator ===")
    fib_gen = fibonacci_generator(10)
    fib_numbers = list(fib_gen)
    print(f"First 10 Fibonacci numbers: {fib_numbers}")
    
    print("\n=== Memory Comparison ===")
    memory_comparison()
    
    print("\n=== Generator Pipeline ===")
    data = range(100)
    pipeline = data_pipeline(data)
    results = list(pipeline)
    print(f"Pipeline results: {results}")
    
    # Generator state
    print("\n=== Generator State ===")
    gen = fibonacci_generator(5)
    print(f"First call: {next(gen)}")
    print(f"Second call: {next(gen)}")
    print(f"Remaining: {list(gen)}")

demonstrate_generators()
```

### 8. Explain Python's context managers and the `with` statement.

**Answer:** Context managers ensure proper resource management using `__enter__` and `__exit__` methods.

```python
import contextlib
import time

def demonstrate_context_managers():
    # Built-in context manager
    def file_example():
        with open('example.txt', 'w') as file:
            file.write('Hello, World!')
        # File automatically closed here
    
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
            self.connection = None
            return False  # Don't suppress exceptions
    
    # Context manager using contextlib
    @contextlib.contextmanager
    def timing_context(operation_name):
        print(f"Starting {operation_name}")
        start_time = time.time()
        try:
            yield start_time
        finally:
            end_time = time.time()
            print(f"{operation_name} took {end_time - start_time:.4f} seconds")
    
    # Multiple context managers
    @contextlib.contextmanager
    def managed_resource(name):
        print(f"Acquiring {name}")
        try:
            yield name
        finally:
            print(f"Releasing {name}")
    
    # Examples
    print("=== Custom Context Manager ===")
    with DatabaseConnection("postgresql://localhost:5432/db") as conn:
        print(f"Using connection: {conn}")
        # Simulate some work
        time.sleep(0.1)
    
    print("\n=== Timing Context Manager ===")
    with timing_context("data processing"):
        # Simulate processing
        total = sum(range(100000))
        print(f"Calculated sum: {total}")
    
    print("\n=== Multiple Context Managers ===")
    with managed_resource("Resource1"), managed_resource("Resource2"):
        print("Using both resources")
    
    # Exception handling in context managers
    print("\n=== Exception Handling ===")
    try:
        with DatabaseConnection("postgresql://localhost:5432/db") as conn:
            print(f"Using connection: {conn}")
            raise ValueError("Something went wrong!")
    except ValueError as e:
        print(f"Caught exception: {e}")

demonstrate_context_managers()
```

### 9. What is the difference between `==` and `is` in Python?

**Answer:** `==` compares values while `is` compares object identity (memory location).

```python
def demonstrate_equality_vs_identity():
    # Value equality vs identity
    a = [1, 2, 3]
    b = [1, 2, 3]
    c = a
    
    print("=== Lists ===")
    print(f"a == b: {a == b}")  # True (same values)
    print(f"a is b: {a is b}")  # False (different objects)
    print(f"a is c: {a is c}")  # True (same object)
    print(f"id(a): {id(a)}")
    print(f"id(b): {id(b)}")
    print(f"id(c): {id(c)}")
    
    # Small integers are cached
    print("\n=== Small Integers (cached) ===")
    x = 100
    y = 100
    print(f"x == y: {x == y}")  # True
    print(f"x is y: {x is y}")  # True (cached)
    
    # Large integers are not cached
    print("\n=== Large Integers (not cached) ===")
    x = 1000
    y = 1000
    print(f"x == y: {x == y}")  # True
    print(f"x is y: {x is y}")  # False (not cached)
    
    # String interning
    print("\n=== Strings ===")
    s1 = "hello"
    s2 = "hello"
    s3 = "hel" + "lo"
    print(f"s1 == s2: {s1 == s2}")  # True
    print(f"s1 is s2: {s1 is s2}")  # True (interned)
    print(f"s1 is s3: {s1 is s3}")  # True (interned)
    
    # None comparison (always use 'is')
    print("\n=== None Comparison ===")
    value = None
    print(f"value == None: {value == None}")  # True but not recommended
    print(f"value is None: {value is None}")  # True and recommended
    
    # Custom class example
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age
        
        def __eq__(self, other):
            if isinstance(other, Person):
                return self.name == other.name and self.age == other.age
            return False
    
    print("\n=== Custom Objects ===")
    person1 = Person("Alice", 30)
    person2 = Person("Alice", 30)
    person3 = person1
    
    print(f"person1 == person2: {person1 == person2}")  # True (custom __eq__)
    print(f"person1 is person2: {person1 is person2}")  # False (different objects)
    print(f"person1 is person3: {person1 is person3}")  # True (same object)

demonstrate_equality_vs_identity()
```

### 10. Explain Python's lambda functions and their use cases.

**Answer:** Lambda functions are anonymous functions defined using the `lambda` keyword.

```python
def demonstrate_lambda_functions():
    # Basic lambda functions
    square = lambda x: x ** 2
    add = lambda x, y: x + y
    
    print(f"Square of 5: {square(5)}")
    print(f"Add 3 and 4: {add(3, 4)}")
    
    # Lambda with built-in functions
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # map() with lambda
    squared = list(map(lambda x: x ** 2, numbers))
    print(f"Squared numbers: {squared}")
    
    # filter() with lambda
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"Even numbers: {evens}")
    
    # sorted() with lambda
    words = ['python', 'java', 'c++', 'javascript', 'go']
    sorted_by_length = sorted(words, key=lambda x: len(x))
    print(f"Sorted by length: {sorted_by_length}")
    
    # Lambda in data processing
    employees = [
        {'name': 'Alice', 'age': 30, 'salary': 70000},
        {'name': 'Bob', 'age': 25, 'salary': 60000},
        {'name': 'Charlie', 'age': 35, 'salary': 80000}
    ]
    
    # Sort by salary
    by_salary = sorted(employees, key=lambda emp: emp['salary'])
    print(f"Sorted by salary: {[emp['name'] for emp in by_salary]}")
    
    # Filter high earners
    high_earners = list(filter(lambda emp: emp['salary'] > 65000, employees))
    print(f"High earners: {[emp['name'] for emp in high_earners]}")
    
    # Lambda limitations and alternatives
    print("\n=== Lambda Limitations ===")
    
    # Lambda can only contain expressions, not statements
    # This won't work: lambda x: print(x)  # print is a statement
    
    # Alternative: regular function
    def process_and_print(x):
        result = x ** 2
        print(f"Processing {x} -> {result}")
        return result
    
    # Lambda in closures
    def create_multiplier(factor):
        return lambda x: x * factor
    
    double = create_multiplier(2)
    triple = create_multiplier(3)
    
    print(f"Double 5: {double(5)}")
    print(f"Triple 5: {triple(5)}")
    
    # Lambda with conditional expressions
    max_func = lambda a, b: a if a > b else b
    print(f"Max of 10 and 7: {max_func(10, 7)}")
    
    # Complex lambda (not recommended)
    complex_lambda = lambda x: x ** 2 if x > 0 else -x ** 2 if x < 0 else 0
    print(f"Complex lambda results: {[complex_lambda(x) for x in [-2, 0, 2]]}")

demonstrate_lambda_functions()
```

### 11. What are Python's built-in data types?

**Answer:** Python provides several built-in data types for different purposes.

```python
def demonstrate_builtin_types():
    # Numeric types
    integer_num = 42
    float_num = 3.14159
    complex_num = 3 + 4j
    
    print("=== Numeric Types ===")
    print(f"Integer: {integer_num} (type: {type(integer_num)})")
    print(f"Float: {float_num} (type: {type(float_num)})")
    print(f"Complex: {complex_num} (type: {type(complex_num)})")
    
    # Sequence types
    string_val = "Hello, World!"
    list_val = [1, 2, 3, 'mixed', True]
    tuple_val = (1, 2, 3)
    range_val = range(5)
    
    print("\n=== Sequence Types ===")
    print(f"String: {string_val} (type: {type(string_val)})")
    print(f"List: {list_val} (type: {type(list_val)})")
    print(f"Tuple: {tuple_val} (type: {type(tuple_val)})")
    print(f"Range: {list(range_val)} (type: {type(range_val)})")
    
    # Mapping type
    dict_val = {'name': 'Alice', 'age': 30, 'city': 'New York'}
    
    print("\n=== Mapping Type ===")
    print(f"Dictionary: {dict_val} (type: {type(dict_val)})")
    
    # Set types
    set_val = {1, 2, 3, 4, 5}
    frozenset_val = frozenset([1, 2, 3, 4, 5])
    
    print("\n=== Set Types ===")
    print(f"Set: {set_val} (type: {type(set_val)})")
    print(f"Frozenset: {frozenset_val} (type: {type(frozenset_val)})")
    
    # Boolean type
    bool_true = True
    bool_false = False
    
    print("\n=== Boolean Type ===")
    print(f"True: {bool_true} (type: {type(bool_true)})")
    print(f"False: {bool_false} (type: {type(bool_false)})")
    
    # Binary types
    bytes_val = b'Hello'
    bytearray_val = bytearray(b'Hello')
    memoryview_val = memoryview(bytes_val)
    
    print("\n=== Binary Types ===")
    print(f"Bytes: {bytes_val} (type: {type(bytes_val)})")
    print(f"Bytearray: {bytearray_val} (type: {type(bytearray_val)})")
    print(f"Memoryview: {memoryview_val} (type: {type(memoryview_val)})")
    
    # None type
    none_val = None
    
    print("\n=== None Type ===")
    print(f"None: {none_val} (type: {type(none_val)})")
    
    # Type checking and conversion
    print("\n=== Type Checking and Conversion ===")
    
    # isinstance() for type checking
    print(f"isinstance(42, int): {isinstance(42, int)}")
    print(f"isinstance('hello', str): {isinstance('hello', str)}")
    print(f"isinstance([1, 2, 3], (list, tuple)): {isinstance([1, 2, 3], (list, tuple))}")
    
    # Type conversion
    print(f"int('42'): {int('42')}")
    print(f"float('3.14'): {float('3.14')}")
    print(f"str(42): {str(42)}")
    print(f"list('hello'): {list('hello')}")
    print(f"tuple([1, 2, 3]): {tuple([1, 2, 3])}")
    print(f"set([1, 2, 2, 3]): {set([1, 2, 2, 3])}")

demonstrate_builtin_types()
```

### 12. How do you handle exceptions in Python?

**Answer:** Python uses try-except blocks for exception handling with optional else and finally clauses.

```python
import logging

def demonstrate_exception_handling():
    # Basic exception handling
    def basic_exception_handling():
        try:
            result = 10 / 0
        except ZeroDivisionError as e:
            print(f"Caught ZeroDivisionError: {e}")
            result = float('inf')
        
        return result
    
    # Multiple exception types
    def multiple_exceptions(data, index):
        try:
            # Could raise IndexError or TypeError
            result = data[index] * 2
            return result
        except IndexError:
            print("Index out of range")
            return None
        except TypeError:
            print("Invalid data type")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    # Exception hierarchy
    def exception_hierarchy():
        try:
            # This could raise various exceptions
            value = int(input("Enter a number: "))
            result = 100 / value
        except ValueError:
            print("Invalid number format")
        except ZeroDivisionError:
            print("Cannot divide by zero")
        except Exception as e:
            print(f"Other error: {e}")
        else:
            print(f"Result: {result}")
        finally:
            print("Cleanup code always runs")
    
    # Custom exceptions
    class DataValidationError(Exception):
        def __init__(self, message, error_code=None):
            super().__init__(message)
            self.error_code = error_code
    
    class DataProcessingError(Exception):
        pass
    
    def validate_and_process_data(data):
        try:
            # Validation
            if not isinstance(data, list):
                raise DataValidationError("Data must be a list", "INVALID_TYPE")
            
            if len(data) == 0:
                raise DataValidationError("Data cannot be empty", "EMPTY_DATA")
            
            # Processing
            result = []
            for item in data:
                if not isinstance(item, (int, float)):
                    raise DataProcessingError(f"Invalid item type: {type(item)}")
                result.append(item ** 2)
            
            return result
            
        except DataValidationError as e:
            logging.error(f"Validation error: {e} (Code: {e.error_code})")
            raise
        except DataProcessingError as e:
            logging.error(f"Processing error: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise
    
    # Context manager for exception handling
    class ExceptionLogger:
        def __init__(self, operation_name):
            self.operation_name = operation_name
        
        def __enter__(self):
            print(f"Starting {self.operation_name}")
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type:
                print(f"Exception in {self.operation_name}: {exc_val}")
                # Log the exception but don't suppress it
                return False
            else:
                print(f"Successfully completed {self.operation_name}")
    
    # Examples
    print("=== Basic Exception Handling ===")
    result = basic_exception_handling()
    print(f"Result: {result}")
    
    print("\n=== Multiple Exceptions ===")
    test_cases = [
        ([1, 2, 3], 1),      # Valid
        ([1, 2, 3], 5),      # IndexError
        ("not a list", 0),   # TypeError
    ]
    
    for data, index in test_cases:
        result = multiple_exceptions(data, index)
        print(f"Data: {data}, Index: {index}, Result: {result}")
    
    print("\n=== Custom Exceptions ===")
    test_data = [
        [1, 2, 3, 4],        # Valid
        [],                  # Empty
        "not a list",        # Invalid type
        [1, 2, "invalid"],   # Invalid item
    ]
    
    for data in test_data:
        try:
            result = validate_and_process_data(data)
            print(f"Success: {data} -> {result}")
        except (DataValidationError, DataProcessingError) as e:
            print(f"Error processing {data}: {e}")
    
    print("\n=== Exception Context Manager ===")
    with ExceptionLogger("data processing"):
        # This will succeed
        processed = [x ** 2 for x in range(5)]
        print(f"Processed: {processed}")
    
    try:
        with ExceptionLogger("failing operation"):
            # This will fail
            result = 1 / 0
    except ZeroDivisionError:
        print("Handled division by zero")

demonstrate_exception_handling()
```
# Python Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-50)](#basic-level-questions-1-50)
2. [Intermediate Level Questions (51-100)](#intermediate-level-questions-51-100)
3. [Advanced Level Questions (101-150)](#advanced-level-questions-101-150)
4. [Architecture & Performance (151-200)](#architecture--performance-151-200)
5. [Data Engineering Specific (201-250)](#data-engineering-specific-201-250)
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
# Example: Simple data pipeline
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

print(simple_etl_pipeline())
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
    
    return "Memory management demonstrated"

print(demonstrate_memory_management())
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
import concurrent.futures

def cpu_intensive_task(n):
    """CPU-bound task affected by GIL"""
    total = 0
    for i in range(n):
        total += i ** 2
    return total

def io_intensive_task(duration):
    """I/O-bound task less affected by GIL"""
    time.sleep(duration)
    return f"Completed after {duration}s"

def compare_threading_vs_multiprocessing():
    tasks = [1000000, 1000000, 1000000, 1000000]
    
    # Threading (limited by GIL for CPU tasks)
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        thread_results = list(executor.map(cpu_intensive_task, tasks))
    thread_time = time.time() - start
    
    # Multiprocessing (bypasses GIL)
    start = time.time()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        process_results = list(executor.map(cpu_intensive_task, tasks))
    process_time = time.time() - start
    
    print(f"Threading time: {thread_time:.2f}s")
    print(f"Multiprocessing time: {process_time:.2f}s")
    print(f"Multiprocessing speedup: {thread_time/process_time:.2f}x")

compare_threading_vs_multiprocessing()
```

### 4. Explain the difference between lists, tuples, and sets.

**Answer:** Different data structures with distinct characteristics and use cases.

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
    
    # Performance comparison
    import time
    
    # List membership test (O(n))
    large_list = list(range(10000))
    start = time.time()
    result = 9999 in large_list
    list_time = time.time() - start
    
    # Set membership test (O(1))
    large_set = set(range(10000))
    start = time.time()
    result = 9999 in large_set
    set_time = time.time() - start
    
    print(f"List membership: {list_time:.6f}s")
    print(f"Set membership: {set_time:.6f}s")
    print(f"Set is {list_time/set_time:.0f}x faster")

compare_data_structures()
```

### 5. What are Python decorators and how do you use them?

**Answer:** Decorators are functions that modify or enhance other functions without changing their source code.

```python
from functools import wraps
import time

# Basic decorator
def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

# Decorator with parameters
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

# Class-based decorator
class CacheDecorator:
    def __init__(self, func):
        self.func = func
        self.cache = {}
    
    def __call__(self, *args):
        if args in self.cache:
            print(f"Cache hit for {args}")
            return self.cache[args]
        
        result = self.func(*args)
        self.cache[args] = result
        print(f"Cache miss for {args}")
        return result

# Usage examples
@timing_decorator
@retry_decorator(max_attempts=3, delay=0.5)
def unreliable_function(x):
    import random
    if random.random() < 0.7:  # 70% chance of failure
        raise ValueError("Random failure")
    return x ** 2

@CacheDecorator
def expensive_calculation(n):
    time.sleep(0.1)  # Simulate expensive operation
    return sum(range(n))

# Test decorators
try:
    result = unreliable_function(5)
    print(f"Result: {result}")
except ValueError as e:
    print(f"Function failed: {e}")

# Test caching
result1 = expensive_calculation(1000)  # Cache miss
result2 = expensive_calculation(1000)  # Cache hit
```

### 6. Explain Python's `*args` and `**kwargs`.

**Answer:** `*args` and `**kwargs` allow functions to accept variable numbers of arguments.

```python
def demonstrate_args_kwargs():
    # *args - Variable positional arguments
    def sum_all(*args):
        print(f"Received args: {args}")
        return sum(args)
    
    # **kwargs - Variable keyword arguments
    def process_data(**kwargs):
        print(f"Received kwargs: {kwargs}")
        for key, value in kwargs.items():
            print(f"{key}: {value}")
    
    # Combined usage
    def flexible_function(required_arg, *args, default_param="default", **kwargs):
        print(f"Required: {required_arg}")
        print(f"Optional args: {args}")
        print(f"Default param: {default_param}")
        print(f"Keyword args: {kwargs}")
    
    # Function that accepts and forwards arguments
    def wrapper_function(*args, **kwargs):
        print("Before calling target function")
        result = target_function(*args, **kwargs)
        print("After calling target function")
        return result
    
    def target_function(a, b, c=None):
        return f"a={a}, b={b}, c={c}"
    
    # Examples
    print("=== *args example ===")
    total = sum_all(1, 2, 3, 4, 5)
    print(f"Sum: {total}")
    
    print("\n=== **kwargs example ===")
    process_data(name="Alice", age=30, city="New York")
    
    print("\n=== Combined example ===")
    flexible_function("required", 1, 2, 3, default_param="custom", extra="value")
    
    print("\n=== Forwarding arguments ===")
    result = wrapper_function("hello", "world", c="!")
    print(f"Result: {result}")

demonstrate_args_kwargs()
```

### 7. What are Python generators and why are they useful?

**Answer:** Generators are functions that yield values one at a time, providing memory-efficient iteration.

```python
import sys

def demonstrate_generators():
    # Generator function
    def fibonacci_generator(n):
        a, b = 0, 1
        count = 0
        while count < n:
            yield a
            a, b = b, a + b
            count += 1
    
    # Generator expression
    squares_gen = (x**2 for x in range(1000000))
    
    # Compare memory usage: list vs generator
    def memory_comparison():
        # List approach - loads everything into memory
        squares_list = [x**2 for x in range(100000)]
        list_size = sys.getsizeof(squares_list)
        
        # Generator approach - generates on demand
        squares_gen = (x**2 for x in range(100000))
        gen_size = sys.getsizeof(squares_gen)
        
        print(f"List size: {list_size:,} bytes")
        print(f"Generator size: {gen_size:,} bytes")
        print(f"Memory savings: {list_size/gen_size:.0f}x")
    
    # Practical example: Processing large files
    def read_large_file(filename):
        """Memory-efficient file reading"""
        with open(filename, 'r') as file:
            for line_num, line in enumerate(file, 1):
                yield line_num, line.strip()
    
    # Pipeline of generators
    def data_pipeline(data):
        # Filter even numbers
        evens = (x for x in data if x % 2 == 0)
        
        # Square the numbers
        squared = (x**2 for x in evens)
        
        # Take first 10
        limited = (x for i, x in enumerate(squared) if i < 10)
        
        return limited
    
    # Examples
    print("=== Fibonacci Generator ===")
    fib_gen = fibonacci_generator(10)
    fib_numbers = list(fib_gen)
    print(f"First 10 Fibonacci numbers: {fib_numbers}")
    
    print("\n=== Memory Comparison ===")
    memory_comparison()
    
    print("\n=== Generator Pipeline ===")
    data = range(100)
    pipeline = data_pipeline(data)
    results = list(pipeline)
    print(f"Pipeline results: {results}")
    
    # Generator state
    print("\n=== Generator State ===")
    gen = fibonacci_generator(5)
    print(f"First call: {next(gen)}")
    print(f"Second call: {next(gen)}")
    print(f"Remaining: {list(gen)}")

demonstrate_generators()
```

### 8. Explain Python's context managers and the `with` statement.

**Answer:** Context managers ensure proper resource management using `__enter__` and `__exit__` methods.

```python
import contextlib
import time

def demonstrate_context_managers():
    # Built-in context manager
    def file_example():
        with open('example.txt', 'w') as file:
            file.write('Hello, World!')
        # File automatically closed here
    
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
            self.connection = None
            return False  # Don't suppress exceptions
    
    # Context manager using contextlib
    @contextlib.contextmanager
    def timing_context(operation_name):
        print(f"Starting {operation_name}")
        start_time = time.time()
        try:
            yield start_time
        finally:
            end_time = time.time()
            print(f"{operation_name} took {end_time - start_time:.4f} seconds")
    
    # Multiple context managers
    @contextlib.contextmanager
    def managed_resource(name):
        print(f"Acquiring {name}")
        try:
            yield name
        finally:
            print(f"Releasing {name}")
    
    # Examples
    print("=== Custom Context Manager ===")
    with DatabaseConnection("postgresql://localhost:5432/db") as conn:
        print(f"Using connection: {conn}")
        # Simulate some work
        time.sleep(0.1)
    
    print("\n=== Timing Context Manager ===")
    with timing_context("data processing"):
        # Simulate processing
        total = sum(range(100000))
        print(f"Calculated sum: {total}")
    
    print("\n=== Multiple Context Managers ===")
    with managed_resource("Resource1"), managed_resource("Resource2"):
        print("Using both resources")
    
    # Exception handling in context managers
    print("\n=== Exception Handling ===")
    try:
        with DatabaseConnection("postgresql://localhost:5432/db") as conn:
            print(f"Using connection: {conn}")
            raise ValueError("Something went wrong!")
    except ValueError as e:
        print(f"Caught exception: {e}")

demonstrate_context_managers()
```

### 9. What is the difference between `==` and `is` in Python?

**Answer:** `==` compares values while `is` compares object identity (memory location).

```python
def demonstrate_equality_vs_identity():
    # Value equality vs identity
    a = [1, 2, 3]
    b = [1, 2, 3]
    c = a
    
    print("=== Lists ===")
    print(f"a == b: {a == b}")  # True (same values)
    print(f"a is b: {a is b}")  # False (different objects)
    print(f"a is c: {a is c}")  # True (same object)
    print(f"id(a): {id(a)}")
    print(f"id(b): {id(b)}")
    print(f"id(c): {id(c)}")
    
    # Small integers are cached
    print("\n=== Small Integers (cached) ===")
    x = 100
    y = 100
    print(f"x == y: {x == y}")  # True
    print(f"x is y: {x is y}")  # True (cached)
    
    # Large integers are not cached
    print("\n=== Large Integers (not cached) ===")
    x = 1000
    y = 1000
    print(f"x == y: {x == y}")  # True
    print(f"x is y: {x is y}")  # False (not cached)
    
    # String interning
    print("\n=== Strings ===")
    s1 = "hello"
    s2 = "hello"
    s3 = "hel" + "lo"
    print(f"s1 == s2: {s1 == s2}")  # True
    print(f"s1 is s2: {s1 is s2}")  # True (interned)
    print(f"s1 is s3: {s1 is s3}")  # True (interned)
    
    # None comparison (always use 'is')
    print("\n=== None Comparison ===")
    value = None
    print(f"value == None: {value == None}")  # True but not recommended
    print(f"value is None: {value is None}")  # True and recommended
    
    # Custom class example
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age
        
        def __eq__(self, other):
            if isinstance(other, Person):
                return self.name == other.name and self.age == other.age
            return False
    
    print("\n=== Custom Objects ===")
    person1 = Person("Alice", 30)
    person2 = Person("Alice", 30)
    person3 = person1
    
    print(f"person1 == person2: {person1 == person2}")  # True (custom __eq__)
    print(f"person1 is person2: {person1 is person2}")  # False (different objects)
    print(f"person1 is person3: {person1 is person3}")  # True (same object)

demonstrate_equality_vs_identity()
```

### 10. Explain Python's lambda functions and their use cases.

**Answer:** Lambda functions are anonymous functions defined using the `lambda` keyword.

```python
def demonstrate_lambda_functions():
    # Basic lambda functions
    square = lambda x: x ** 2
    add = lambda x, y: x + y
    
    print(f"Square of 5: {square(5)}")
    print(f"Add 3 and 4: {add(3, 4)}")
    
    # Lambda with built-in functions
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # map() with lambda
    squared = list(map(lambda x: x ** 2, numbers))
    print(f"Squared numbers: {squared}")
    
    # filter() with lambda
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"Even numbers: {evens}")
    
    # sorted() with lambda
    words = ['python', 'java', 'c++', 'javascript', 'go']
    sorted_by_length = sorted(words, key=lambda x: len(x))
    print(f"Sorted by length: {sorted_by_length}")
    
    # Lambda in data processing
    employees = [
        {'name': 'Alice', 'age': 30, 'salary': 70000},
        {'name': 'Bob', 'age': 25, 'salary': 60000},
        {'name': 'Charlie', 'age': 35, 'salary': 80000}
    ]
    
    # Sort by salary
    by_salary = sorted(employees, key=lambda emp: emp['salary'])
    print(f"Sorted by salary: {[emp['name'] for emp in by_salary]}")
    
    # Filter high earners
    high_earners = list(filter(lambda emp: emp['salary'] > 65000, employees))
    print(f"High earners: {[emp['name'] for emp in high_earners]}")
    
    # Lambda limitations and alternatives
    print("\n=== Lambda Limitations ===")
    
    # Lambda can only contain expressions, not statements
    # This won't work: lambda x: print(x)  # print is a statement
    
    # Alternative: regular function
    def process_and_print(x):
        result = x ** 2
        print(f"Processing {x} -> {result}")
        return result
    
    # Lambda in closures
    def create_multiplier(factor):
        return lambda x: x * factor
    
    double = create_multiplier(2)
    triple = create_multiplier(3)
    
    print(f"Double 5: {double(5)}")
    print(f"Triple 5: {triple(5)}")
    
    # Lambda with conditional expressions
    max_func = lambda a, b: a if a > b else b
    print(f"Max of 10 and 7: {max_func(10, 7)}")
    
    # Complex lambda (not recommended)
    complex_lambda = lambda x: x ** 2 if x > 0 else -x ** 2 if x < 0 else 0
    print(f"Complex lambda results: {[complex_lambda(x) for x in [-2, 0, 2]]}")

demonstrate_lambda_functions()
```

### 11. What are Python's built-in data types?

**Answer:** Python provides several built-in data types for different purposes.

```python
def demonstrate_builtin_types():
    # Numeric types
    integer_num = 42
    float_num = 3.14159
    complex_num = 3 + 4j
    
    print("=== Numeric Types ===")
    print(f"Integer: {integer_num} (type: {type(integer_num)})")
    print(f"Float: {float_num} (type: {type(float_num)})")
    print(f"Complex: {complex_num} (type: {type(complex_num)})")
    
    # Sequence types
    string_val = "Hello, World!"
    list_val = [1, 2, 3, 'mixed', True]
    tuple_val = (1, 2, 3)
    range_val = range(5)
    
    print("\n=== Sequence Types ===")
    print(f"String: {string_val} (type: {type(string_val)})")
    print(f"List: {list_val} (type: {type(list_val)})")
    print(f"Tuple: {tuple_val} (type: {type(tuple_val)})")
    print(f"Range: {list(range_val)} (type: {type(range_val)})")
    
    # Mapping type
    dict_val = {'name': 'Alice', 'age': 30, 'city': 'New York'}
    
    print("\n=== Mapping Type ===")
    print(f"Dictionary: {dict_val} (type: {type(dict_val)})")
    
    # Set types
    set_val = {1, 2, 3, 4, 5}
    frozenset_val = frozenset([1, 2, 3, 4, 5])
    
    print("\n=== Set Types ===")
    print(f"Set: {set_val} (type: {type(set_val)})")
    print(f"Frozenset: {frozenset_val} (type: {type(frozenset_val)})")
    
    # Boolean type
    bool_true = True
    bool_false = False
    
    print("\n=== Boolean Type ===")
    print(f"True: {bool_true} (type: {type(bool_true)})")
    print(f"False: {bool_false} (type: {type(bool_false)})")
    
    # Binary types
    bytes_val = b'Hello'
    bytearray_val = bytearray(b'Hello')
    memoryview_val = memoryview(bytes_val)
    
    print("\n=== Binary Types ===")
    print(f"Bytes: {bytes_val} (type: {type(bytes_val)})")
    print(f"Bytearray: {bytearray_val} (type: {type(bytearray_val)})")
    print(f"Memoryview: {memoryview_val} (type: {type(memoryview_val)})")
    
    # None type
    none_val = None
    
    print("\n=== None Type ===")
    print(f"None: {none_val} (type: {type(none_val)})")
    
    # Type checking and conversion
    print("\n=== Type Checking and Conversion ===")
    
    # isinstance() for type checking
    print(f"isinstance(42, int): {isinstance(42, int)}")
    print(f"isinstance('hello', str): {isinstance('hello', str)}")
    print(f"isinstance([1, 2, 3], (list, tuple)): {isinstance([1, 2, 3], (list, tuple))}")
    
    # Type conversion
    print(f"int('42'): {int('42')}")
    print(f"float('3.14'): {float('3.14')}")
    print(f"str(42): {str(42)}")
    print(f"list('hello'): {list('hello')}")
    print(f"tuple([1, 2, 3]): {tuple([1, 2, 3])}")
    print(f"set([1, 2, 2, 3]): {set([1, 2, 2, 3])}")

demonstrate_builtin_types()
```

### 12. How do you handle exceptions in Python?

**Answer:** Python uses try-except blocks for exception handling with optional else and finally clauses.

```python
import logging

def demonstrate_exception_handling():
    # Basic exception handling
    def basic_exception_handling():
        try:
            result = 10 / 0
        except ZeroDivisionError as e:
            print(f"Caught ZeroDivisionError: {e}")
            result = float('inf')
        
        return result
    
    # Multiple exception types
    def multiple_exceptions(data, index):
        try:
            # Could raise IndexError or TypeError
            result = data[index] * 2
            return result
        except IndexError:
            print("Index out of range")
            return None
        except TypeError:
            print("Invalid data type")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    # Exception hierarchy
    def exception_hierarchy():
        try:
            # This could raise various exceptions
            value = int(input("Enter a number: "))
            result = 100 / value
        except ValueError:
            print("Invalid number format")
        except ZeroDivisionError:
            print("Cannot divide by zero")
        except Exception as e:
            print(f"Other error: {e}")
        else:
            print(f"Result: {result}")
        finally:
            print("Cleanup code always runs")
    
    # Custom exceptions
    class DataValidationError(Exception):
        def __init__(self, message, error_code=None):
            super().__init__(message)
            self.error_code = error_code
    
    class DataProcessingError(Exception):
        pass
    
    def validate_and_process_data(data):
        try:
            # Validation
            if not isinstance(data, list):
                raise DataValidationError("Data must be a list", "INVALID_TYPE")
            
            if len(data) == 0:
                raise DataValidationError("Data cannot be empty", "EMPTY_DATA")
            
            # Processing
            result = []
            for item in data:
                if not isinstance(item, (int, float)):
                    raise DataProcessingError(f"Invalid item type: {type(item)}")
                result.append(item ** 2)
            
            return result
            
        except DataValidationError as e:
            logging.error(f"Validation error: {e} (Code: {e.error_code})")
            raise
        except DataProcessingError as e:
            logging.error(f"Processing error: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise
    
    # Context manager for exception handling
    class ExceptionLogger:
        def __init__(self, operation_name):
            self.operation_name = operation_name
        
        def __enter__(self):
            print(f"Starting {self.operation_name}")
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type:
                print(f"Exception in {self.operation_name}: {exc_val}")
                # Log the exception but don't suppress it
                return False
            else:
                print(f"Successfully completed {self.operation_name}")
    
    # Examples
    print("=== Basic Exception Handling ===")
    result = basic_exception_handling()
    print(f"Result: {result}")
    
    print("\n=== Multiple Exceptions ===")
    test_cases = [
        ([1, 2, 3], 1),      # Valid
        ([1, 2, 3], 5),      # IndexError
        ("not a list", 0),   # TypeError
    ]
    
    for data, index in test_cases:
        result = multiple_exceptions(data, index)
        print(f"Data: {data}, Index: {index}, Result: {result}")
    
    print("\n=== Custom Exceptions ===")
    test_data = [
        [1, 2, 3, 4],        # Valid
        [],                  # Empty
        "not a list",        # Invalid type
        [1, 2, "invalid"],   # Invalid item
    ]
    
    for data in test_data:
        try:
            result = validate_and_process_data(data)
            print(f"Success: {data} -> {result}")
        except (DataValidationError, DataProcessingError) as e:
            print(f"Error processing {data}: {e}")
    
    print("\n=== Exception Context Manager ===")
    with ExceptionLogger("data processing"):
        # This will succeed
        processed = [x ** 2 for x in range(5)]
        print(f"Processed: {processed}")
    
    try:
        with ExceptionLogger("failing operation"):
            # This will fail
            result = 1 / 0
    except ZeroDivisionError:
        print("Handled division by zero")

demonstrate_exception_handling()
```

### 13. What are list comprehensions and how do they work?

**Answer:** List comprehensions provide a concise way to create lists using a single line of code.

```python
def demonstrate_list_comprehensions():
    # Basic list comprehension
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Traditional approach
    squares_traditional = []
    for x in numbers:
        squares_traditional.append(x ** 2)
    
    # List comprehension approach
    squares_comprehension = [x ** 2 for x in numbers]
    
    print(f"Traditional: {squares_traditional}")
    print(f"Comprehension: {squares_comprehension}")
    
    # List comprehension with condition
    even_squares = [x ** 2 for x in numbers if x % 2 == 0]
    print(f"Even squares: {even_squares}")
    
    # Multiple conditions
    filtered_numbers = [x for x in numbers if x > 3 and x < 8]
    print(f"Filtered (3 < x < 8): {filtered_numbers}")
    
    # Nested list comprehensions
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    
    # Flatten matrix
    flattened = [item for row in matrix for item in row]
    print(f"Flattened matrix: {flattened}")
    
    # Transpose matrix
    transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
    print(f"Transposed matrix: {transposed}")
    
    # Dictionary comprehension
    word_lengths = {word: len(word) for word in ['python', 'data', 'engineering']}
    print(f"Word lengths: {word_lengths}")
    
    # Set comprehension
    unique_lengths = {len(word) for word in ['python', 'data', 'engineering', 'code']}
    print(f"Unique lengths: {unique_lengths}")
    
    # Generator expression (memory efficient)
    large_squares = (x ** 2 for x in range(1000000))
    print(f"Generator created for {sum(1 for _ in range(1000000))} items")
    
    # Complex example: Processing CSV-like data
    data = [
        "Alice,30,Engineering,75000",
        "Bob,25,Sales,60000", 
        "Charlie,35,Engineering,80000",
        "Diana,28,Marketing,65000"
    ]
    
    # Parse and filter employees
    employees = [
        {
            'name': row.split(',')[0],
            'age': int(row.split(',')[1]),
            'department': row.split(',')[2],
            'salary': int(row.split(',')[3])
        }
        for row in data
    ]
    
    # High earners in Engineering
    high_earning_engineers = [
        emp['name'] for emp in employees 
        if emp['department'] == 'Engineering' and emp['salary'] > 70000
    ]
    
    print(f"High earning engineers: {high_earning_engineers}")
    
    # Conditional expressions in comprehensions
    salary_categories = [
        'High' if emp['salary'] > 70000 else 'Medium' if emp['salary'] > 60000 else 'Low'
        for emp in employees
    ]
    print(f"Salary categories: {salary_categories}")
    
    # Performance comparison
    import time
    
    # List comprehension
    start = time.time()
    comp_result = [x ** 2 for x in range(100000)]
    comp_time = time.time() - start
    
    # Traditional loop
    start = time.time()
    loop_result = []
    for x in range(100000):
        loop_result.append(x ** 2)
    loop_time = time.time() - start
    
    # map() function
    start = time.time()
    map_result = list(map(lambda x: x ** 2, range(100000)))
    map_time = time.time() - start
    
    print(f"\nPerformance comparison:")
    print(f"List comprehension: {comp_time:.4f}s")
    print(f"Traditional loop: {loop_time:.4f}s")
    print(f"Map function: {map_time:.4f}s")

demonstrate_list_comprehensions()
```

### 14. Explain Python's module and package system.

**Answer:** Python's module system allows code organization and reusability through modules and packages.

```python
# Module example (save as math_utils.py)
"""
Math utilities module
"""

def add(a, b):
    """Add two numbers"""
    return a + b

def multiply(a, b):
    """Multiply two numbers"""
    return a * b

def factorial(n):
    """Calculate factorial"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# Module-level variable
PI = 3.14159

# Module-level code (runs when imported)
print(f"Math utils module loaded. PI = {PI}")

def demonstrate_module_system():
    # Different ways to import
    
    # 1. Import entire module
    import math
    print(f"math.sqrt(16): {math.sqrt(16)}")
    
    # 2. Import specific functions
    from math import sqrt, pow
    print(f"sqrt(25): {sqrt(25)}")
    print(f"pow(2, 3): {pow(2, 3)}")
    
    # 3. Import with alias
    import math as m
    print(f"m.pi: {m.pi}")
    
    # 4. Import all (not recommended)
    # from math import *
    
    # Module attributes
    print(f"Math module name: {math.__name__}")
    print(f"Math module file: {math.__file__}")
    
    # Custom module usage (if math_utils.py exists)
    try:
        import math_utils
        result = math_utils.add(5, 3)
        print(f"Custom module result: {result}")
    except ImportError:
        print("Custom module not found")
    
    # Package structure example
    """
    my_package/
        __init__.py
        module1.py
        module2.py
        subpackage/
            __init__.py
            submodule.py
    """
    
    # Relative imports (within package)
    # from . import module1
    # from ..parent_package import module
    # from .subpackage import submodule
    
    # Module search path
    import sys
    print(f"Module search paths: {sys.path[:3]}...")  # Show first 3 paths
    
    # Dynamically import modules
    import importlib
    
    # Import module by name
    json_module = importlib.import_module('json')
    data = json_module.dumps({'key': 'value'})
    print(f"Dynamic import result: {data}")
    
    # Reload module (useful in development)
    # importlib.reload(math_utils)
    
    # Check if module is available
    def is_module_available(module_name):
        try:
            importlib.import_module(module_name)
            return True
        except ImportError:
            return False
    
    print(f"pandas available: {is_module_available('pandas')}")
    print(f"numpy available: {is_module_available('numpy')}")
    
    # Module as script vs import
    if __name__ == "__main__":
        print("This code runs only when script is executed directly")
    else:
        print("This code runs when module is imported")

demonstrate_module_system()

# Package __init__.py example
"""
# __init__.py content
from .module1 import function1
from .module2 import function2

__version__ = "1.0.0"
__all__ = ['function1', 'function2']

# Package-level initialization
print("Package initialized")
"""

# Advanced module concepts
def advanced_module_concepts():
    # Module caching
    import sys
    print(f"Loaded modules count: {len(sys.modules)}")
    
    # Module attributes
    import os
    print(f"OS module attributes: {[attr for attr in dir(os) if not attr.startswith('_')][:5]}")
    
    # Namespace packages (Python 3.3+)
    # Allow packages to be split across multiple directories
    
    # Module finder and loader customization
    class CustomFinder:
        def find_spec(self, name, path, target=None):
            if name == 'custom_module':
                # Return custom module spec
                pass
            return None
    
    # Install custom finder
    # sys.meta_path.insert(0, CustomFinder())
    
    print("Advanced module concepts demonstrated")

advanced_module_concepts()
```

### 15. What is the difference between shallow and deep copy?

**Answer:** Shallow copy creates a new object but references to nested objects, while deep copy creates completely independent copies.

```python
import copy

def demonstrate_copy_differences():
    # Original nested data structure
    original = {
        'name': 'Alice',
        'scores': [85, 90, 78],
        'address': {
            'street': '123 Main St',
            'city': 'New York'
        }
    }
    
    # Assignment (no copy)
    assigned = original
    
    # Shallow copy
    shallow = copy.copy(original)
    # or shallow = original.copy()
    
    # Deep copy
    deep = copy.deepcopy(original)
    
    print("=== Original Data ===")
    print(f"Original: {original}")
    print(f"Assigned: {assigned}")
    print(f"Shallow: {shallow}")
    print(f"Deep: {deep}")
    
    # Test identity
    print("\n=== Identity Tests ===")
    print(f"original is assigned: {original is assigned}")
    print(f"original is shallow: {original is shallow}")
    print(f"original is deep: {original is deep}")
    
    # Test nested object identity
    print(f"original['scores'] is shallow['scores']: {original['scores'] is shallow['scores']}")
    print(f"original['scores'] is deep['scores']: {original['scores'] is deep['scores']}")
    
    # Modify top-level attribute
    print("\n=== Modifying Top-Level Attribute ===")
    original['name'] = 'Bob'
    
    print(f"Original name: {original['name']}")
    print(f"Assigned name: {assigned['name']}")  # Changed (same object)
    print(f"Shallow name: {shallow['name']}")    # Unchanged (different object)
    print(f"Deep name: {deep['name']}")          # Unchanged (different object)
    
    # Modify nested list
    print("\n=== Modifying Nested List ===")
    original['scores'].append(95)
    
    print(f"Original scores: {original['scores']}")
    print(f"Assigned scores: {assigned['scores']}")  # Changed (same reference)
    print(f"Shallow scores: {shallow['scores']}")    # Changed (same reference)
    print(f"Deep scores: {deep['scores']}")          # Unchanged (different reference)
    
    # Modify nested dictionary
    print("\n=== Modifying Nested Dictionary ===")
    original['address']['city'] = 'Boston'
    
    print(f"Original city: {original['address']['city']}")
    print(f"Assigned city: {assigned['address']['city']}")  # Changed
    print(f"Shallow city: {shallow['address']['city']}")    # Changed
    print(f"Deep city: {deep['address']['city']}")          # Unchanged
    
    # List copying examples
    print("\n=== List Copying Examples ===")
    
    original_list = [[1, 2, 3], [4, 5, 6]]
    
    # Different ways to create shallow copies
    shallow_list1 = original_list.copy()
    shallow_list2 = original_list[:]
    shallow_list3 = list(original_list)
    
    # Deep copy
    deep_list = copy.deepcopy(original_list)
    
    # Modify nested list
    original_list[0].append(4)
    
    print(f"Original: {original_list}")
    print(f"Shallow copy 1: {shallow_list1}")  # Changed
    print(f"Shallow copy 2: {shallow_list2}")  # Changed
    print(f"Shallow copy 3: {shallow_list3}")  # Changed
    print(f"Deep copy: {deep_list}")           # Unchanged
    
    # Custom objects with copy
    class Person:
        def __init__(self, name, hobbies):
            self.name = name
            self.hobbies = hobbies
        
        def __copy__(self):
            # Custom shallow copy
            return Person(self.name, self.hobbies)
        
        def __deepcopy__(self, memo):
            # Custom deep copy
            return Person(copy.deepcopy(self.name, memo), 
                         copy.deepcopy(self.hobbies, memo))
        
        def __repr__(self):
            return f"Person('{self.name}', {self.hobbies})"
    
    print("\n=== Custom Object Copying ===")
    
    person1 = Person("Alice", ["reading", "swimming"])
    person2 = copy.copy(person1)
    person3 = copy.deepcopy(person1)
    
    # Modify original
    person1.hobbies.append("cycling")
    
    print(f"Original: {person1}")
    print(f"Shallow copy: {person2}")  # Hobbies list shared
    print(f"Deep copy: {person3}")     # Independent hobbies list
    
    # Performance comparison
    import time
    
    large_data = {'data': [list(range(1000)) for _ in range(100)]}
    
    # Shallow copy timing
    start = time.time()
    for _ in range(100):
        shallow_copy = copy.copy(large_data)
    shallow_time = time.time() - start
    
    # Deep copy timing
    start = time.time()
    for _ in range(100):
        deep_copy = copy.deepcopy(large_data)
    deep_time = time.time() - start
    
    print(f"\n=== Performance Comparison ===")
    print(f"Shallow copy time: {shallow_time:.4f}s")
    print(f"Deep copy time: {deep_time:.4f}s")
    print(f"Deep copy is {deep_time/shallow_time:.1f}x slower")

demonstrate_copy_differences()
```