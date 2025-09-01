# Python Interview Questions

## Table of Contents

1. [Basic Python Questions](#basic-python-questions)
   - [Python 2 vs Python 3](#1-what-are-the-key-differences-between-python-2-and-python-3)
   - [Memory Management](#2-explain-pythons-memory-management-and-garbage-collection)
   - [is vs ==](#3-what-is-the-difference-between-is-and)
   - [Lists vs Tuples](#4-what-are-the-key-differences-between-lists-and-tuples-in-python)
   - [List Comprehensions vs Generators](#5-explain-list-comprehensions-vs-generator-expressions)
2. [Intermediate Questions](#intermediate-questions)
   - [Decorators](#6-what-are-decorators-and-how-do-they-work)
   - [*args and **kwargs](#1-what-are-the-key-differences-between-python-2-and-python-3)
   - [Global Interpreter Lock](#8-what-is-the-global-interpreter-lock-gil)
   - [Method Resolution Order](#9-explain-pythons-method-resolution-order-mro)
   - [Deep vs Shallow Copy](#10-explain-the-difference-between-deep-copy-and-shallow-copy)
3. [Advanced Questions](#advanced-questions)
   - [Singleton Pattern](#11-how-do-you-implement-a-singleton-pattern-in-python)
   - [Context Managers](#12-explain-context-managers-and-the-with-statement)
   - [Thread-Safe Singleton](#13-how-would-you-implement-a-thread-safe-singleton-pattern-for-database-connections)
4. [Data Engineering Specific Questions](#data-engineering-specific-questions)
   - [Large CSV Processing](#14-how-would-you-process-a-large-csv-file-that-doesnt-fit-in-memory)
   - [Database Connections](#15-how-do-you-handle-database-connections-efficiently)
   - [Async/Await](#16-explain-asyncawait-and-when-to-use-it-in-data-engineering)
   - [Performance Optimization](#performance-comparison-sync-vs-async)
   - [Error Handling and Logging](#error-handling-decorator-with-detailed-logging)
5. [Coding Challenges](#coding-challenges)
   - [LRU Cache Implementation](#19-implement-a-lru-cache-from-scratch)
   - [Most Frequent Elements](#20-write-a-function-to-find-the-most-frequent-elements-in-a-large-dataset)
   - [Data Pipeline Implementation](#21-implement-a-comprehensive-data-pipeline-with-error-handling-and-monitoring)

---

## Basic Python Questions

### 1. What are the key differences between Python 2 and Python 3?
**Answer:**
- **Print Statement**: Python 2 uses `print "hello"`, Python 3 uses `print("hello")`
- **Division**: Python 2 `/` is integer division, Python 3 `/` is float division
- **Unicode**: Python 3 has better Unicode support by default
- **Range**: Python 2 has `range()` and `xrange()`, Python 3 only has `range()` (lazy)
- **Input**: Python 2 has `raw_input()` and `input()`, Python 3 only has `input()`

### 2. Explain Python's memory management and garbage collection.
**Answer:**
- **Reference Counting**: Primary mechanism - objects deleted when reference count reaches 0
- **Cycle Detection**: Handles circular references that reference counting can't
- **Memory Pools**: Python uses memory pools for small objects to reduce fragmentation
- **Generational GC**: Objects are categorized into generations (0, 1, 2) based on survival

### 3. What is the difference between `is` and `==`?
**Answer:**
- **`==`**: Compares values (calls `__eq__` method)
- **`is`**: Compares object identity (memory location)
```python
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)  # True (same values)
print(a is b)  # False (different objects)

c = a
print(a is c)  # True (same object)
# Output: True
# Output: False
# Output: True
```

### 4. What are the key differences between lists and tuples in Python?
**Answer:**
- **Mutability**: Lists are mutable (can be modified), tuples are immutable
- **Performance**: Tuples are faster for iteration and access
- **Memory**: Tuples use less memory
- **Use cases**: Lists for dynamic data, tuples for fixed data structures

```python
# List example
my_list = [1, 2, 3]
my_list.append(4)  # Works
print(f"List after append: {my_list}")
# Output: List after append: [1, 2, 3, 4]

# Tuple example
my_tuple = (1, 2, 3)
print(f"Tuple: {my_tuple}")
# my_tuple.append(4)  # Error - tuples are immutable
# Output: Tuple: (1, 2, 3)
```

### 5. Explain list comprehensions vs generator expressions.
**Answer:**
```python
# List comprehension - creates list in memory
squares_list = [x**2 for x in range(10)]

# Generator expression - lazy evaluation
squares_gen = (x**2 for x in range(10))

# Memory usage
import sys
print(f"List size: {sys.getsizeof(squares_list)} bytes")
print(f"Generator size: {sys.getsizeof(squares_gen)} bytes")
# Output: List size: 200 bytes
# Output: Generator size: 88 bytes
```

## Intermediate Questions

### 6. What are decorators and how do they work?
**Answer:**
Decorators are a powerful Python feature that allows you to modify or extend the behavior of functions or classes without permanently modifying their code. They use the `@` syntax and are essentially functions that take another function as input and return a modified version.

```python
import time
from functools import wraps

# Basic decorator example
def timing_decorator(func):
    @wraps(func)  # Preserves original function metadata
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timing_decorator
def slow_function():
    """A function that takes some time to execute."""
    time.sleep(1)
    return "Done"

# Decorator with parameters
def retry(max_attempts=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    print(f"Attempt {attempt + 1} failed: {e}")
        return wrapper
    return decorator

@retry(max_attempts=3)
def unreliable_function():
    import random
    if random.random() < 0.7:
        raise Exception("Random failure")
    return "Success!"
```

### 7. Explain the difference between `*args` and `**kwargs`.
**Answer:**
```python
def example_function(*args, **kwargs):
    print("args:", args)      # Tuple of positional arguments
    print("kwargs:", kwargs)  # Dictionary of keyword arguments

example_function(1, 2, 3, name="John", age=30)
# Output: args: (1, 2, 3)
# Output: kwargs: {'name': 'John', 'age': 30}
```

### 8. What is the Global Interpreter Lock (GIL)?
**Answer:**
The Global Interpreter Lock (GIL) is a mutex that protects access to Python objects, preventing multiple native threads from executing Python bytecodes simultaneously. This is one of the most important concepts to understand for Python performance optimization.

**Key Points:**
- **Definition**: A mutex that prevents multiple threads from executing Python code simultaneously
- **Impact**: Limits true parallelism in CPU-bound tasks but doesn't affect I/O-bound tasks
- **Why it exists**: Simplifies memory management and prevents race conditions in CPython's reference counting
- **Workarounds**: Use multiprocessing for CPU-bound tasks, async/await for I/O-bound tasks, or C extensions

```python
import threading
import time
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# CPU-bound task that shows GIL limitations
def cpu_bound_task(n):
    """CPU-intensive task that will be limited by GIL in threading."""
    total = 0
    for i in range(n):
        total += i ** 2
    return total

# I/O-bound task where GIL is released
def io_bound_task(duration):
    """I/O task where GIL is released during sleep."""
    time.sleep(duration)
    return f"Completed after {duration} seconds"

# Demonstrate GIL impact
def compare_execution_methods():
    n = 500000
    
    # Single-threaded
    start = time.time()
    [cpu_bound_task(n) for _ in range(4)]
    single_time = time.time() - start
    
    # Multi-threaded (limited by GIL)
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(cpu_bound_task, [n] * 4))
    thread_time = time.time() - start
    
    # Multi-processing (bypasses GIL)
    start = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        list(executor.map(cpu_bound_task, [n] * 4))
    process_time = time.time() - start
    
    print(f"Single-threaded: {single_time:.2f}s")
    print(f"Multi-threaded: {thread_time:.2f}s (GIL limited)")
    print(f"Multi-processing: {process_time:.2f}s (GIL bypassed)")
```

### 9. Explain Python's method resolution order (MRO).
**Answer:**
```python
class A:
    def method(self): print("A")

class B(A):
    def method(self): print("B")

class C(A):
    def method(self): print("C")

class D(B, C):
    pass

# MRO: D -> B -> C -> A -> object
print(D.__mro__)
d = D()
d.method()
# Output: (<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)
# Output: B
```

### 10. Explain the difference between deep copy and shallow copy.
**Answer:**
- **Shallow copy**: Creates new object but references to nested objects remain
- **Deep copy**: Creates completely independent copy including nested objects

```python
import copy

original = [[1, 2, 3], [4, 5, 6]]
shallow = copy.copy(original)
deep = copy.deepcopy(original)

original[0][0] = 'X'
print(f"Shallow copy: {shallow}")
print(f"Deep copy: {deep}")
# Output: Shallow copy: [['X', 2, 3], [4, 5, 6]]
# Output: Deep copy: [[1, 2, 3], [4, 5, 6]]
```

## Advanced Questions

### 11. How do you implement a singleton pattern in Python?
**Answer:**
```python
class Singleton:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialized = True
            # Initialize here

# Alternative using decorator
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance
```

### 12. Explain context managers and the `with` statement.
**Answer:**
Context managers provide a way to allocate and release resources precisely when you want to. They're most commonly used with the `with` statement to ensure proper cleanup of resources like files, database connections, or locks.

**How Context Managers Work:**
- `__enter__()`: Called when entering the `with` block
- `__exit__()`: Called when exiting the `with` block (even if an exception occurs)

```python
import time
import threading
from contextlib import contextmanager

# Built-in context manager example
with open('file.txt', 'r') as f:
    content = f.read()
# File automatically closed, even if an exception occurs

# Custom context manager class
class DatabaseConnection:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None
    
    def __enter__(self):
        print(f"Connecting to database: {self.connection_string}")
        self.connection = f"Connected to {self.connection_string}"
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing database connection")
        if exc_type:
            print(f"Exception occurred: {exc_val}")
            print("Rolling back transaction")
        else:
            print("Committing transaction")
        self.connection = None
        return False  # Don't suppress exceptions

# Using contextlib decorator
@contextmanager
def timer(operation_name="Operation"):
    """Context manager to time operations."""
    start = time.time()
    try:
        print(f"Starting {operation_name}...")
        yield start
    finally:
        elapsed = time.time() - start
        print(f"{operation_name} completed in {elapsed:.4f}s")

# Usage examples
with timer("Data Processing"):
    time.sleep(1)
    data = [i**2 for i in range(10000)]

# Thread-safe context manager
class ThreadSafeResource:
    def __init__(self):
        self._lock = threading.Lock()
        self._resource = "shared_resource"
    
    def __enter__(self):
        self._lock.acquire()
        return self._resource
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._lock.release()
        return False
```

### 13. What's the difference between iterators and generators?
**Answer:**
Iterators and generators are both used for iteration, but they differ in implementation and memory usage.

**Iterator:**
- An object that implements `__iter__()` and `__next__()` methods
- Maintains state between calls
- Can be created from any iterable using `iter()`

**Generator:**
- A special type of iterator created using `yield` keyword
- Automatically implements iterator protocol
- Lazy evaluation - values computed on demand
- More memory efficient for large datasets

```python
# Iterator example
class NumberIterator:
    def __init__(self, max_num):
        self.max_num = max_num
        self.current = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current < self.max_num:
            self.current += 1
            return self.current
        raise StopIteration

# Generator function
def number_generator(max_num):
    current = 0
    while current < max_num:
        current += 1
        yield current

# Generator expression
numbers_gen = (x for x in range(1, 6))

# Usage comparison
iterator = NumberIterator(5)
generator = number_generator(5)

print("Iterator:", list(iterator))
print("Generator:", list(generator))
# Output: Iterator: [1, 2, 3, 4, 5]
# Output: Generator: [1, 2, 3, 4, 5]

# Memory efficiency demonstration
import sys

# List (all in memory)
numbers_list = [x**2 for x in range(10000)]

# Generator (lazy evaluation)
numbers_gen = (x**2 for x in range(10000))

print(f"List memory: {sys.getsizeof(numbers_list)} bytes")
print(f"Generator memory: {sys.getsizeof(numbers_gen)} bytes")
# Output: List memory: ~400KB
# Output: Generator memory: ~88 bytes
```

### 14. How would you implement a thread-safe singleton pattern for database connections?
**Answer:**
```python
import threading
from sqlalchemy import create_engine

class DatabaseConnection:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, connection_string: str = None):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.engine = create_engine(connection_string)
        return cls._instance
    
    def get_connection(self):
        return self.engine.connect()

# Usage
db1 = DatabaseConnection("postgresql://user:pass@localhost/db")
db2 = DatabaseConnection()  # Same instance
assert db1 is db2  # True
```

## Data Engineering Specific Questions

### 14. How would you process a large CSV file that doesn't fit in memory?
**Answer:**
```python
import pandas as pd

# Method 1: Chunking
def process_large_csv(filename, chunk_size=10000):
    for chunk in pd.read_csv(filename, chunksize=chunk_size):
        # Process each chunk
        processed_chunk = chunk.groupby('category').sum()
        yield processed_chunk

# Method 2: Iterator approach
def process_csv_iterator(filename):
    with open(filename, 'r') as f:
        header = next(f)
        for line in f:
            # Process line by line
            yield process_line(line)

# Method 3: Using Dask for parallel processing
import dask.dataframe as dd
df = dd.read_csv('large_file.csv')
result = df.groupby('category').sum().compute()
```

### 15. How do you handle database connections efficiently?
**Answer:**
```python
import sqlite3
from contextlib import contextmanager

# Connection pooling
class ConnectionPool:
    def __init__(self, database, max_connections=5):
        self.database = database
        self.pool = []
        self.max_connections = max_connections
    
    def get_connection(self):
        if self.pool:
            return self.pool.pop()
        return sqlite3.connect(self.database)
    
    def return_connection(self, conn):
        if len(self.pool) < self.max_connections:
            self.pool.append(conn)
        else:
            conn.close()

@contextmanager
def get_db_connection(pool):
    conn = pool.get_connection()
    try:
        yield conn
    finally:
        pool.return_connection(conn)
```

### 16. Explain async/await and when to use it in data engineering.
**Answer:**
Async/await enables concurrent execution of I/O-bound operations, crucial for data engineering tasks involving multiple API calls, file operations, or database queries.

```python
import asyncio
import aiohttp
import aiofiles
import time
from typing import List, Dict, Any

# Async HTTP requests with error handling
async def fetch_data(session: aiohttp.ClientSession, url: str, 
                    timeout: int = 30) -> Dict[str, Any]:
    """Fetch data from URL with timeout and error handling.
    
    Args:
        session: Aiohttp client session
        url: URL to fetch data from
        timeout: Request timeout in seconds
        
    Returns:
        Dictionary containing response data or error information
    """
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
            if response.status == 200:
                data = await response.json()
                return {'url': url, 'status': 'success', 'data': data}
            else:
                return {'url': url, 'status': 'error', 'error': f'HTTP {response.status}'}
    except asyncio.TimeoutError:
        return {'url': url, 'status': 'error', 'error': 'Timeout'}
    except Exception as e:
        return {'url': url, 'status': 'error', 'error': str(e)}

async def fetch_multiple_apis(urls: List[str], max_concurrent: int = 10) -> List[Dict[str, Any]]:
    """Fetch data from multiple APIs concurrently with rate limiting.
    
    Args:
        urls: List of URLs to fetch
        max_concurrent: Maximum number of concurrent requests
        
    Returns:
        List of results from all API calls
    """
    # Create semaphore to limit concurrent requests
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def fetch_with_semaphore(session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
        async with semaphore:
            return await fetch_data(session, url)
    
    # Configure session with connection pooling
    connector = aiohttp.TCPConnector(limit=100, limit_per_host=10)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch_with_semaphore(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Handle any exceptions that occurred
    processed_results = []
    for result in results:
        if isinstance(result, Exception):
            processed_results.append({
                'status': 'error', 
                'error': str(result)
            })
        else:
            processed_results.append(result)
    
    return processed_results

# Async file I/O with batch processing
async def process_files_batch(filenames: List[str], batch_size: int = 5) -> List[Dict[str, Any]]:
    """Process multiple files in batches to avoid overwhelming the system.
    
    Args:
        filenames: List of file paths to process
        batch_size: Number of files to process concurrently
        
    Returns:
        List of processing results
    """
    async def read_and_process_file(filename: str) -> Dict[str, Any]:
        """Read and process a single file."""
        try:
            async with aiofiles.open(filename, 'r', encoding='utf-8') as f:
                content = await f.read()
                
            # Simulate processing
            word_count = len(content.split())
            line_count = len(content.splitlines())
            
            return {
                'filename': filename,
                'status': 'success',
                'word_count': word_count,
                'line_count': line_count,
                'size_bytes': len(content.encode('utf-8'))
            }
        except Exception as e:
            return {
                'filename': filename,
                'status': 'error',
                'error': str(e)
            }
    
    results = []
    
    # Process files in batches
    for i in range(0, len(filenames), batch_size):
        batch = filenames[i:i + batch_size]
        batch_tasks = [read_and_process_file(filename) for filename in batch]
        batch_results = await asyncio.gather(*batch_tasks)
        results.extend(batch_results)
        
        # Optional: Add delay between batches to prevent overwhelming the system
        if i + batch_size < len(filenames):
            await asyncio.sleep(0.1)
    
    return results

# Async database operations
async def async_database_operations(queries: List[str]) -> List[Dict[str, Any]]:
    """Execute multiple database queries concurrently.
    
    Note: This example uses asyncpg for PostgreSQL. Adapt for your database.
    """
    import asyncpg  # pip install asyncpg
    
    async def execute_query(pool: asyncpg.Pool, query: str) -> Dict[str, Any]:
        """Execute a single query."""
        try:
            async with pool.acquire() as connection:
                result = await connection.fetch(query)
                return {
                    'query': query[:50] + '...' if len(query) > 50 else query,
                    'status': 'success',
                    'row_count': len(result),
                    'data': [dict(row) for row in result]
                }
        except Exception as e:
            return {
                'query': query[:50] + '...' if len(query) > 50 else query,
                'status': 'error',
                'error': str(e)
            }
    
    # Create connection pool
    pool = await asyncpg.create_pool(
        host='localhost',
        port=5432,
        user='username',
        password='password',
        database='dbname',
        min_size=1,
        max_size=10
    )
    
    try:
        # Execute all queries concurrently
        tasks = [execute_query(pool, query) for query in queries]
        results = await asyncio.gather(*tasks)
        return results
    finally:
        await pool.close()

# Performance comparison: sync vs async
def sync_api_calls(urls: List[str]) -> List[Dict[str, Any]]:
    """Synchronous API calls for comparison."""
    import requests
    
    results = []
    start_time = time.time()
    
    for url in urls:
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                results.append({
                    'url': url,
                    'status': 'success',
                    'data': response.json()
                })
            else:
                results.append({
                    'url': url,
                    'status': 'error',
                    'error': f'HTTP {response.status_code}'
                })
        except Exception as e:
            results.append({
                'url': url,
                'status': 'error',
                'error': str(e)
            })
    
    end_time = time.time()
    print(f"Sync execution time: {end_time - start_time:.2f} seconds")
    return results

async def async_api_calls(urls: List[str]) -> List[Dict[str, Any]]:
    """Asynchronous API calls for comparison."""
    start_time = time.time()
    results = await fetch_multiple_apis(urls)
    end_time = time.time()
    print(f"Async execution time: {end_time - start_time:.2f} seconds")
    return results

# Usage examples and when to use async/await in data engineering:
if __name__ == "__main__":
    # Example URLs for testing
    test_urls = [
        'https://jsonplaceholder.typicode.com/posts/1',
        'https://jsonplaceholder.typicode.com/posts/2',
        'https://jsonplaceholder.typicode.com/posts/3',
        'https://jsonplaceholder.typicode.com/posts/4',
        'https://jsonplaceholder.typicode.com/posts/5'
    ]
    
    # Compare sync vs async performance
    print("=== Performance Comparison ===")
    
    # Sync version
    sync_results = sync_api_calls(test_urls)
    print(f"Sync results: {len([r for r in sync_results if r['status'] == 'success'])} successful")
    
    # Async version
    async_results = asyncio.run(async_api_calls(test_urls))
    print(f"Async results: {len([r for r in async_results if r['status'] == 'success'])} successful")

# When to use async/await in data engineering:
# 
# 1. **Multiple API calls**: Fetching data from multiple REST APIs simultaneously
# 2. **File I/O operations**: Reading/writing multiple files concurrently
# 3. **Database operations**: Executing multiple queries in parallel
# 4. **ETL pipelines**: When stages involve I/O-bound operations
# 5. **Real-time data processing**: Handling multiple data streams
# 6. **Web scraping**: Scraping multiple websites concurrently
# 7. **Message queue processing**: Consuming from multiple queues
# 
# Benefits:
# - Significantly faster for I/O-bound operations
# - Better resource utilization
# - Improved scalability
# - Reduced blocking time
# 
# When NOT to use:
# - CPU-bound tasks (use multiprocessing instead)
# - Simple, single-threaded operations
# - When code complexity outweighs benefits


```

### 17. How do you optimize Python code for performance?
**Answer:**
Python performance optimization involves identifying bottlenecks and applying appropriate techniques:

```python
# 1. Use built-in functions and libraries
# Slow approach
result = []
for i in range(1000000):
    if i % 2 == 0:
        result.append(i * 2)

# Fast approach - list comprehension
result = [i * 2 for i in range(1000000) if i % 2 == 0]

# 2. Use NumPy for numerical operations
import numpy as np
# Slow - pure Python
python_list = list(range(1000000))
result = [x * 2 for x in python_list]

# Fast - NumPy vectorized operations
numpy_array = np.arange(1000000)
result = numpy_array * 2

# 3. Profile your code to identify bottlenecks
import cProfile
import time

def profile_function():
    # Example function to profile
    data = [i**2 for i in range(100000)]
    return sum(data)

cProfile.run('profile_function()')

# 4. Use appropriate data structures
# Use set for O(1) membership testing
large_set = set(range(1000000))
if 500000 in large_set:  # O(1) average case
    pass

# Use dict for O(1) lookups
lookup_dict = {item: index for index, item in enumerate(range(1000))}

# 5. Cache expensive operations
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(n):
    """Cache results of expensive computations."""
    return sum(i**2 for i in range(n))

# 6. Use generators for memory efficiency
def large_data_generator():
    """Generate data on-demand instead of storing in memory."""
    for i in range(1000000):
        yield i**2

# 7. Optimize string operations
# Slow - string concatenation
result = ""
for i in range(1000):
    result += str(i)

# Fast - join method
result = "".join(str(i) for i in range(1000))

# 8. Use local variables in loops
def slow_function(data):
    result = []
    for item in data:
        result.append(math.sqrt(item))  # Global lookup each time
    return result

def fast_function(data):
    import math
    sqrt = math.sqrt  # Local reference
    result = []
    for item in data:
        result.append(sqrt(item))
    return result

# 9. Performance measurement
def measure_performance():
    import timeit
    
    # Time different approaches
    list_comp_time = timeit.timeit(
        lambda: [i*2 for i in range(10000)], 
        number=100
    )
    
    loop_time = timeit.timeit(
        lambda: [i*2 for i in range(10000)], 
        number=100
    )
    
    print(f"List comprehension: {list_comp_time:.4f}s")
    print(f"Regular loop: {loop_time:.4f}s")

# Performance optimization checklist:
# - Profile first, optimize second
# - Use built-in functions when possible
# - Choose appropriate data structures
# - Minimize function call overhead
# - Use generators for large datasets
# - Cache expensive computations
# - Consider NumPy for numerical operations
# - Use multiprocessing for CPU-bound tasks
# - Use async/await for I/O-bound tasks
    pass

# Use dict for O(1) lookups
items = ['apple', 'banana', 'cherry']
lookup_dict = {item: index for index, item in enumerate(items)}

# 5. Cache expensive operations
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(n):
    """Cache results of expensive computations."""
    return sum(i**2 for i in range(n))
```

### 18. How do you handle errors and logging in production Python code?
**Answer:**
```python
import logging
import traceback
from functools import wraps
from typing import Callable, Any

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

# Error handling decorator with detailed logging
def handle_errors(func: Callable) -> Callable:
    """Decorator to handle and log errors comprehensively."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            logger.info(f"Starting execution of {func.__name__}")
            result = func(*args, **kwargs)
            logger.info(f"Successfully completed {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            logger.error(f"Function args: {args}, kwargs: {kwargs}")
            raise
    return wrapper

# Custom exception hierarchy for better error handling
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

# Retry mechanism with exponential backoff
import time
from functools import wraps

def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0, 
          exceptions: tuple = (Exception,)):
    """Retry decorator with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each failed attempt
        exceptions: Tuple of exceptions to catch and retry on
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            attempts = 0
            current_delay = delay
            
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts == max_attempts:
                        logger.error(f"Max retry attempts ({max_attempts}) reached for {func.__name__}")
                        raise e
                    
                    logger.warning(
                        f"Attempt {attempts}/{max_attempts} failed for {func.__name__}: {str(e)}. "
                        f"Retrying in {current_delay:.2f}s..."
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff
            
        return wrapper
    return decorator

# Usage example
@handle_errors
@retry(max_attempts=3, delay=1.0, backoff=2.0, exceptions=(ConnectionError, TimeoutError))
def process_data(data: list) -> dict:
    """Process data with comprehensive error handling and retry logic."""
    if not data:
        raise DataValidationError("Input data cannot be empty")
    
    # Simulate processing
    processed_count = len([item for item in data if item is not None])
    
    if processed_count == 0:
        raise DataValidationError("No valid records found in input data")
    
    logger.info(f"Successfully processed {processed_count} records")
    return {"processed_count": processed_count, "status": "success"}
```

## Coding Challenges

### 19. Implement a LRU Cache from scratch.
**Answer:**
```python
from typing import Optional, Any

class Node:
    """Doubly linked list node for LRU cache."""
    def __init__(self, key: Any = None, value: Any = None):
        self.key = key
        self.value = value
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None

class LRUCache:
    """Least Recently Used (LRU) Cache implementation.
    
    Uses a combination of hash map and doubly linked list for O(1) operations.
    """
    
    def __init__(self, capacity: int):
        """Initialize LRU cache with given capacity.
        
        Args:
            capacity: Maximum number of items the cache can hold
        """
        self.capacity = capacity
        self.cache = {}  # key -> node mapping
        
        # Create dummy head and tail nodes
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _add_node(self, node: Node) -> None:
        """Add node right after head."""
        node.prev = self.head
        node.next = self.head.next
        
        self.head.next.prev = node
        self.head.next = node
    
    def _remove_node(self, node: Node) -> None:
        """Remove an existing node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        
        prev_node.next = next_node
        next_node.prev = prev_node
    
    def _move_to_head(self, node: Node) -> None:
        """Move node to head (mark as recently used)."""
        self._remove_node(node)
        self._add_node(node)
    
    def _pop_tail(self) -> Node:
        """Remove and return the last node (least recently used)."""
        last_node = self.tail.prev
        self._remove_node(last_node)
        return last_node
    
    def get(self, key: Any) -> Any:
        """Get value by key and mark as recently used.
        
        Args:
            key: Key to look up
            
        Returns:
            Value associated with key, or -1 if not found
        """
        node = self.cache.get(key)
        
        if not node:
            return -1
        
        # Move accessed node to head (mark as recently used)
        self._move_to_head(node)
        return node.value
    
    def put(self, key: Any, value: Any) -> None:
        """Put key-value pair into cache.
        
        Args:
            key: Key to store
            value: Value to associate with key
        """
        node = self.cache.get(key)
        
        if not node:
            new_node = Node(key, value)
            
            if len(self.cache) >= self.capacity:
                # Remove least recently used item
                tail = self._pop_tail()
                del self.cache[tail.key]
            
            self.cache[key] = new_node
            self._add_node(new_node)
        else:
            # Update existing node
            node.value = value
            self._move_to_head(node)

# Usage example
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))  # Returns 1
cache.put(3, 3)      # Evicts key 2
print(cache.get(2))  # Returns -1 (not found)
```

### 20. Write a function to find the most frequent elements in a large dataset.
**Answer:**
```python
from collections import Counter, defaultdict
import heapq
from typing import List, Tuple, Iterator, Any

def top_k_frequent_basic(data: List[Any], k: int) -> List[Tuple[Any, int]]:
    """Find top k frequent elements using Counter.
    
    Time Complexity: O(n + k log n)
    Space Complexity: O(n)
    
    Args:
        data: List of elements
        k: Number of top frequent elements to return
        
    Returns:
        List of (element, frequency) tuples
    """
    counter = Counter(data)
    return counter.most_common(k)

def top_k_frequent_heap(data: List[Any], k: int) -> List[Tuple[Any, int]]:
    """Find top k frequent elements using min-heap for memory efficiency.
    
    Time Complexity: O(n + n log k)
    Space Complexity: O(n + k)
    
    Args:
        data: List of elements
        k: Number of top frequent elements to return
        
    Returns:
        List of (element, frequency) tuples
    """
    counter = Counter(data)
    
    # Use min-heap to keep only top k elements
    heap = []
    for element, freq in counter.items():
        if len(heap) < k:
            heapq.heappush(heap, (freq, element))
        elif freq > heap[0][0]:
            heapq.heapreplace(heap, (freq, element))
    
    # Convert to (element, frequency) format and sort by frequency desc
    result = [(element, freq) for freq, element in heap]
    return sorted(result, key=lambda x: x[1], reverse=True)

def top_k_frequent_streaming(data_stream: Iterator[Any], k: int, 
                           window_size: int = 1000) -> Iterator[List[Tuple[Any, int]]]:
    """Find top k frequent elements in streaming data with sliding window.
    
    Args:
        data_stream: Iterator of data elements
        k: Number of top frequent elements to return
        window_size: Size of sliding window
        
    Yields:
        List of (element, frequency) tuples for current window
    """
    window = []
    counter = Counter()
    
    for item in data_stream:
        # Add new item
        window.append(item)
        counter[item] += 1
        
        # Remove old item if window is full
        if len(window) > window_size:
            old_item = window.pop(0)
            counter[old_item] -= 1
            if counter[old_item] == 0:
                del counter[old_item]
        
        # Yield top k every 100 items (configurable)
        if len(window) % 100 == 0:
            yield counter.most_common(k)

def top_k_frequent_distributed(data: List[Any], k: int, num_partitions: int = 4) -> List[Tuple[Any, int]]:
    """Find top k frequent elements using map-reduce approach for large datasets.
    
    Args:
        data: List of elements
        k: Number of top frequent elements to return
        num_partitions: Number of partitions for parallel processing
        
    Returns:
        List of (element, frequency) tuples
    """
    from concurrent.futures import ProcessPoolExecutor
    import math
    
    def count_partition(partition_data: List[Any]) -> Counter:
        """Count frequencies in a data partition."""
        return Counter(partition_data)
    
    # Split data into partitions
    partition_size = math.ceil(len(data) / num_partitions)
    partitions = [data[i:i + partition_size] for i in range(0, len(data), partition_size)]
    
    # Process partitions in parallel
    with ProcessPoolExecutor(max_workers=num_partitions) as executor:
        partition_counters = list(executor.map(count_partition, partitions))
    
    # Merge results
    total_counter = Counter()
    for counter in partition_counters:
        total_counter.update(counter)
    
    return total_counter.most_common(k)

# Usage examples
data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4] * 1000

# Basic approach
top_basic = top_k_frequent_basic(data, 3)
print(f"Top 3 (basic): {top_basic}")

# Heap approach (memory efficient)
top_heap = top_k_frequent_heap(data, 3)
print(f"Top 3 (heap): {top_heap}")

# Streaming approach
data_stream = iter(data)
for window_top_k in top_k_frequent_streaming(data_stream, 3, window_size=500):
    print(f"Current window top 3: {window_top_k}")
    break  # Just show first result

# Distributed approach
top_distributed = top_k_frequent_distributed(data, 3, num_partitions=4)
print(f"Top 3 (distributed): {top_distributed}")
```

### 21. Implement a comprehensive data pipeline with error handling and monitoring.
**Answer:**
```python
import logging
import time
import json
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Dict, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import threading
from contextlib import contextmanager

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class PipelineStatus(Enum):
    """Enumeration of possible pipeline statuses."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class PipelineMetrics:
    """Comprehensive metrics for pipeline execution."""
    pipeline_id: str
    start_time: float = 0.0
    end_time: float = 0.0
    processed_records: int = 0
    failed_records: int = 0
    skipped_records: int = 0
    stage_metrics: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    @property
    def duration(self) -> float:
        """Calculate total execution duration."""
        return self.end_time - self.start_time if self.end_time > 0 else 0.0
    
    @property
    def total_records(self) -> int:
        """Calculate total number of records processed."""
        return self.processed_records + self.failed_records + self.skipped_records
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        total = self.total_records
        return (self.processed_records / total * 100) if total > 0 else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary for serialization."""
        return {
            'pipeline_id': self.pipeline_id,
            'duration': self.duration,
            'processed_records': self.processed_records,
            'failed_records': self.failed_records,
            'skipped_records': self.skipped_records,
            'success_rate': self.success_rate,
            'stage_metrics': self.stage_metrics,
            'errors': self.errors,
            'warnings': self.warnings
        }

class PipelineStage(ABC):
    """Abstract base class for pipeline stages."""
    
    def __init__(self, name: str, config: Dict[str, Any] = None):
        """Initialize pipeline stage.
        
        Args:
            name: Unique name for the stage
            config: Configuration dictionary for the stage
        """
        self.name = name
        self.config = config or {}
        self.logger = logging.getLogger(f"pipeline.{name}")
        self._metrics = {
            'start_time': 0.0,
            'end_time': 0.0,
            'processed_count': 0,
            'error_count': 0
        }
    
    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process data in this stage.
        
        Args:
            data: Input data to process
            
        Returns:
            Processed data
        """
        pass
    
    def validate_input(self, data: Any) -> bool:
        """Validate input data before processing.
        
        Args:
            data: Input data to validate
            
        Returns:
            True if data is valid, False otherwise
        """
        return data is not None
    
    def validate_output(self, data: Any) -> bool:
        """Validate output data after processing.
        
        Args:
            data: Output data to validate
            
        Returns:
            True if data is valid, False otherwise
        """
        return data is not None
    
    @contextmanager
    def _stage_timing(self):
        """Context manager for timing stage execution."""
        self._metrics['start_time'] = time.time()
        try:
            yield
        finally:
            self._metrics['end_time'] = time.time()
    
    def __call__(self, data: Any) -> Any:
        """Execute the stage with comprehensive error handling and monitoring.
        
        Args:
            data: Input data to process
            
        Returns:
            Processed data
            
        Raises:
            ValueError: If input validation fails
            RuntimeError: If processing fails
        """
        with self._stage_timing():
            self.logger.info(f"Starting stage: {self.name}")
            
            # Input validation
            if not self.validate_input(data):
                self._metrics['error_count'] += 1
                raise ValueError(f"Input validation failed for stage {self.name}")
            
            try:
                # Process data
                result = self.process(data)
                
                # Output validation
                if not self.validate_output(result):
                    self._metrics['error_count'] += 1
                    raise ValueError(f"Output validation failed for stage {self.name}")
                
                self._metrics['processed_count'] += 1
                self.logger.info(f"Successfully completed stage: {self.name}")
                return result
                
            except Exception as e:
                self._metrics['error_count'] += 1
                self.logger.error(f"Error in stage {self.name}: {str(e)}")
                raise RuntimeError(f"Stage {self.name} failed: {str(e)}") from e
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get stage execution metrics."""
        duration = self._metrics['end_time'] - self._metrics['start_time']
        return {
            **self._metrics,
            'duration': duration
        }

class DataPipeline:
    """Comprehensive data processing pipeline with monitoring and error handling."""
    
    def __init__(self, pipeline_id: str, stages: List[PipelineStage], 
                 config: Dict[str, Any] = None):
        """Initialize data pipeline.
        
        Args:
            pipeline_id: Unique identifier for the pipeline
            stages: List of pipeline stages to execute
            config: Pipeline configuration
        """
        self.pipeline_id = pipeline_id
        self.stages = stages
        self.config = config or {}
        self.metrics = PipelineMetrics(pipeline_id)
        self.logger = logging.getLogger(f"pipeline.{pipeline_id}")
        self.status = PipelineStatus.PENDING
        self._lock = threading.Lock()
    
    def add_stage(self, stage: PipelineStage) -> None:
        """Add a stage to the pipeline.
        
        Args:
            stage: Pipeline stage to add
        """
        with self._lock:
            self.stages.append(stage)
    
    def run(self, data: Any) -> Any:
        """Execute the complete pipeline.
        
        Args:
            data: Input data to process
            
        Returns:
            Final processed data
            
        Raises:
            RuntimeError: If pipeline execution fails
        """
        with self._lock:
            self.status = PipelineStatus.RUNNING
            self.metrics.start_time = time.time()
            
        self.logger.info(f"Starting pipeline execution: {self.pipeline_id}")
        
        try:
            current_data = data
            
            # Execute each stage
            for stage in self.stages:
                try:
                    current_data = stage(current_data)
                    
                    # Collect stage metrics
                    stage_metrics = stage.get_metrics()
                    self.metrics.stage_metrics[stage.name] = stage_metrics
                    
                except Exception as e:
                    self.metrics.failed_records += 1
                    error_msg = f"Stage {stage.name} failed: {str(e)}"
                    self.metrics.errors.append(error_msg)
                    self.logger.error(error_msg)
                    raise
            
            # Pipeline completed successfully
            self.metrics.processed_records += 1
            self.status = PipelineStatus.SUCCESS
            self.logger.info(f"Pipeline {self.pipeline_id} completed successfully")
            
            return current_data
            
        except Exception as e:
            self.status = PipelineStatus.FAILED
            self.logger.error(f"Pipeline {self.pipeline_id} failed: {str(e)}")
            raise RuntimeError(f"Pipeline execution failed: {str(e)}") from e
            
        finally:
            self.metrics.end_time = time.time()
            self._log_final_metrics()
    
    def _log_final_metrics(self) -> None:
        """Log final pipeline metrics."""
        metrics_dict = self.metrics.to_dict()
        self.logger.info(f"Pipeline metrics: {json.dumps(metrics_dict, indent=2)}")
    
    def get_status(self) -> PipelineStatus:
        """Get current pipeline status."""
        return self.status
    
    def get_metrics(self) -> PipelineMetrics:
        """Get comprehensive pipeline metrics."""
        return self.metrics

# Example implementation of specific stages
class ExtractStage(PipelineStage):
    """Stage for extracting data from various sources."""
    
    def process(self, data: Any) -> Dict[str, Any]:
        """Extract data and add metadata.
        
        Args:
            data: Raw input data
            
        Returns:
            Dictionary with extracted data and metadata
        """
        # Simulate data extraction
        extracted_data = {
            'raw_data': data,
            'extracted_at': datetime.now().isoformat(),
            'source': self.config.get('source', 'unknown'),
            'record_count': len(data) if isinstance(data, (list, dict)) else 1
        }
        
        self.logger.info(f"Extracted {extracted_data['record_count']} records")
        return extracted_data

class TransformStage(PipelineStage):
    """Stage for transforming extracted data."""
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform the extracted data.
        
        Args:
            data: Dictionary containing extracted data
            
        Returns:
            Dictionary with transformed data
        """
        raw_data = data['raw_data']
        
        # Apply transformations based on config
        transformations = self.config.get('transformations', [])
        transformed_data = raw_data
        
        for transform in transformations:
            if transform == 'uppercase' and isinstance(transformed_data, str):
                transformed_data = transformed_data.upper()
            elif transform == 'filter_nulls' and isinstance(transformed_data, list):
                transformed_data = [item for item in transformed_data if item is not None]
        
        result = {
            'transformed_data': transformed_data,
            'metadata': data,
            'transformed_at': datetime.now().isoformat(),
            'transformations_applied': transformations
        }
        
        self.logger.info(f"Applied {len(transformations)} transformations")
        return result

class LoadStage(PipelineStage):
    """Stage for loading transformed data to destination."""
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Load transformed data to destination.
        
        Args:
            data: Dictionary containing transformed data
            
        Returns:
            Dictionary with load results
        """
        destination = self.config.get('destination', 'default')
        
        # Simulate loading data
        load_result = {
            'status': 'loaded',
            'destination': destination,
            'loaded_at': datetime.now().isoformat(),
            'data': data['transformed_data'],
            'metadata': data['metadata']
        }
        
        self.logger.info(f"Successfully loaded data to {destination}")
        return load_result

# Usage example
if __name__ == "__main__":
    # Create pipeline stages with configuration
    extract_stage = ExtractStage(
        name="extract",
        config={'source': 'api_endpoint'}
    )
    
    transform_stage = TransformStage(
        name="transform",
        config={'transformations': ['uppercase', 'filter_nulls']}
    )
    
    load_stage = LoadStage(
        name="load",
        config={'destination': 'data_warehouse'}
    )
    
    # Create and execute pipeline
    pipeline = DataPipeline(
        pipeline_id="etl_pipeline_001",
        stages=[extract_stage, transform_stage, load_stage],
        config={'batch_size': 1000, 'retry_count': 3}
    )
    
    # Execute pipeline with sample data
    sample_data = ["hello", "world", None, "data", "engineering"]
    
    try:
        result = pipeline.run(sample_data)
        print(f"Pipeline result: {json.dumps(result, indent=2)}")
        
        # Get and display metrics
        metrics = pipeline.get_metrics()
        print(f"\nPipeline Metrics:")
        print(f"Duration: {metrics.duration:.2f} seconds")
        print(f"Success Rate: {metrics.success_rate:.1f}%")
        print(f"Processed Records: {metrics.processed_records}")
        
    except Exception as e:
        print(f"Pipeline failed: {e}")
        metrics = pipeline.get_metrics()
        print(f"Errors: {metrics.errors}")ering:
# - Multiple API calls
# - Concurrent file processing
# - Database operations with high I/O wait
```

### 17. How do you optimize Python code for performance?
**Answer:**
```python
# 1. Use built-in functions and libraries
# Slow
result = []
for i in range(1000000):
    if i % 2 == 0:
        result.append(i * 2)

# Fast
result = [i * 2 for i in range(1000000) if i % 2 == 0]

# 2. Use NumPy for numerical operations
import numpy as np
# Slow
python_list = list(range(1000000))
result = [x * 2 for x in python_list]

# Fast
numpy_array = np.arange(1000000)
result = numpy_array * 2

# 3. Profile your code
import cProfile
cProfile.run('your_function()')

# 4. Use appropriate data structures
# Use set for membership testing
large_set = set(range(1000000))
if 500000 in large_set:  # O(1) average case
    pass

# 5. Cache expensive operations
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(n):
    # Expensive computation
    return sum(i**2 for i in range(n))
```

### 18. How do you handle errors and logging in production Python code?
**Answer:**
```python
import logging
import traceback
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Error handling decorator
def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    return wrapper

# Custom exceptions
class DataProcessingError(Exception):
    """Custom exception for data processing errors"""
    pass

@handle_errors
def process_data(data):
    if not data:
        raise DataProcessingError("No data provided")
    
    logger.info(f"Processing {len(data)} records")
    # Process data
    logger.info("Data processing completed successfully")
    return processed_data

# Retry mechanism
import time
from functools import wraps

def retry(max_attempts=3, delay=1, backoff=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        logger.error(f"Max retry attempts reached for {func.__name__}")
                        raise
                    
                    logger.warning(f"Attempt {attempts} failed: {str(e)}. Retrying in {current_delay}s")
                    time.sleep(current_delay)
                    current_delay *= backoff
            
        return wrapper
    return decorator
```

## Coding Challenges

### 19. Implement a LRU Cache from scratch.
**Answer:**
LRU (Least Recently Used) Cache is a caching strategy that removes the least recently used items when the cache reaches its capacity. This is commonly asked in data engineering interviews as it demonstrates understanding of data structures and algorithms.

```python
from typing import Optional, Any

class Node:
    """Doubly linked list node for LRU cache."""
    def __init__(self, key: Any = None, value: Any = None):
        self.key = key
        self.value = value
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None

class LRUCache:
    """Efficient LRU Cache implementation using hash map + doubly linked list.
    
    Time Complexity: O(1) for both get and put operations
    Space Complexity: O(capacity)
    """
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> node mapping
        
        # Create dummy head and tail nodes
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _add_node(self, node: Node) -> None:
        """Add node right after head."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
    
    def _remove_node(self, node: Node) -> None:
        """Remove an existing node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
    
    def _move_to_head(self, node: Node) -> None:
        """Move node to head (mark as recently used)."""
        self._remove_node(node)
        self._add_node(node)
    
    def _pop_tail(self) -> Node:
        """Remove and return the last node (least recently used)."""
        last_node = self.tail.prev
        self._remove_node(last_node)
        return last_node
    
    def get(self, key: Any) -> Any:
        """Get value by key and mark as recently used."""
        node = self.cache.get(key)
        if not node:
            return -1
        
        # Move accessed node to head
        self._move_to_head(node)
        return node.value
    
    def put(self, key: Any, value: Any) -> None:
        """Put key-value pair into cache."""
        node = self.cache.get(key)
        
        if not node:
            new_node = Node(key, value)
            
            if len(self.cache) >= self.capacity:
                # Remove least recently used item
                tail = self._pop_tail()
                del self.cache[tail.key]
            
            self.cache[key] = new_node
            self._add_node(new_node)
        else:
            # Update existing node
            node.value = value
            self._move_to_head(node)
    
    def display(self) -> list:
        """Display cache contents from most to least recently used."""
        result = []
        current = self.head.next
        while current != self.tail:
            result.append((current.key, current.value))
            current = current.next
        return result

# Simple LRU Cache implementation (less efficient but easier to understand)
class SimpleLRUCache:
    """Simple LRU Cache using list for ordering (O(n) operations)."""
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.order = []  # Most recent at the end
    
    def get(self, key: Any) -> Any:
        if key in self.cache:
            # Move to end (most recent)
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return -1
    
    def put(self, key: Any, value: Any) -> None:
        if key in self.cache:
            # Update existing key
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            # Remove least recently used (first in order)
            oldest = self.order.pop(0)
            del self.cache[oldest]
        
        self.cache[key] = value
        self.order.append(key)

# Usage example and testing
if __name__ == "__main__":
    # Test efficient LRU Cache
    cache = LRUCache(3)
    
    cache.put(1, "one")
    cache.put(2, "two")
    cache.put(3, "three")
    print(f"Cache after adding 1,2,3: {cache.display()}")
    
    print(f"Get key 1: {cache.get(1)}")  # Should return "one"
    print(f"Cache after accessing 1: {cache.display()}")
    
    cache.put(4, "four")  # Should evict key 2
    print(f"Cache after adding 4: {cache.display()}")
    
    print(f"Get key 2: {cache.get(2)}")  # Should return -1 (not found)
```

### 20. Write a function to find the most frequent elements in a large dataset.
**Answer:**
Finding the most frequent elements is a common data engineering task, especially when dealing with large datasets that may not fit in memory. Here are several approaches depending on the constraints:

```python
from collections import Counter, defaultdict
import heapq
from typing import List, Tuple, Iterator, Any
import time

def top_k_frequent_basic(data: List[Any], k: int) -> List[Tuple[Any, int]]:
    """Basic approach using Counter - good for small to medium datasets.
    
    Time Complexity: O(n + k log n)
    Space Complexity: O(n)
    """
    counter = Counter(data)
    return counter.most_common(k)

def top_k_frequent_heap(data: List[Any], k: int) -> List[Tuple[Any, int]]:
    """Memory-efficient approach using min-heap.
    
    Time Complexity: O(n + n log k)
    Space Complexity: O(n + k) - better when k << n
    """
    counter = Counter(data)
    
    # Use min-heap to keep only top k elements
    heap = []
    for element, freq in counter.items():
        if len(heap) < k:
            heapq.heappush(heap, (freq, element))
        elif freq > heap[0][0]:
            heapq.heapreplace(heap, (freq, element))
    
    # Convert to (element, frequency) format and sort by frequency desc
    result = [(element, freq) for freq, element in heap]
    return sorted(result, key=lambda x: x[1], reverse=True)

def top_k_frequent_streaming(data_stream: Iterator[Any], k: int, 
                           window_size: int = 1000) -> Iterator[List[Tuple[Any, int]]]:
    """For streaming data with sliding window.
    
    Useful when data is too large to fit in memory or arrives continuously.
    """
    window = []
    counter = Counter()
    
    for item in data_stream:
        # Add new item
        window.append(item)
        counter[item] += 1
        
        # Remove old item if window is full
        if len(window) > window_size:
            old_item = window.pop(0)
            counter[old_item] -= 1
            if counter[old_item] == 0:
                del counter[old_item]
        
        # Yield top k every 100 items (configurable)
        if len(window) % 100 == 0:
            yield counter.most_common(k)

def top_k_frequent_distributed(data: List[Any], k: int, num_partitions: int = 4) -> List[Tuple[Any, int]]:
    """Distributed approach for very large datasets using map-reduce pattern.
    
    Simulates distributed processing by partitioning data.
    """
    from concurrent.futures import ProcessPoolExecutor
    import math
    
    def count_partition(partition_data: List[Any]) -> Counter:
        """Count frequencies in a data partition."""
        return Counter(partition_data)
    
    # Split data into partitions
    partition_size = math.ceil(len(data) / num_partitions)
    partitions = [data[i:i + partition_size] for i in range(0, len(data), partition_size)]
    
    # Process partitions in parallel
    with ProcessPoolExecutor(max_workers=num_partitions) as executor:
        partition_counters = list(executor.map(count_partition, partitions))
    
    # Merge results (reduce phase)
    total_counter = Counter()
    for counter in partition_counters:
        total_counter.update(counter)
    
    return total_counter.most_common(k)

def top_k_frequent_approximate(data_stream: Iterator[Any], k: int, 
                             error_rate: float = 0.01) -> List[Tuple[Any, int]]:
    """Approximate algorithm using Count-Min Sketch for very large streams.
    
    Trades accuracy for memory efficiency - useful for massive datasets.
    """
    # Simplified Count-Min Sketch implementation
    import hashlib
    import math
    
    # Calculate sketch dimensions
    width = math.ceil(math.e / error_rate)
    depth = math.ceil(math.log(1 / 0.01))  # 99% confidence
    
    # Initialize sketch matrix
    sketch = [[0] * width for _ in range(depth)]
    
    # Hash functions
    def hash_func(item, seed):
        return hash(str(item) + str(seed)) % width
    
    # Track actual items for final result
    item_tracker = defaultdict(int)
    
    # Process stream
    for item in data_stream:
        # Update sketch
        for i in range(depth):
            pos = hash_func(item, i)
            sketch[i][pos] += 1
        
        # Update tracker (with sampling to save memory)
        if hash(str(item)) % 100 == 0:  # Sample 1% of items
            item_tracker[item] += 100  # Estimate actual count
    
    # Estimate frequencies and return top k
    estimated_counts = []
    for item, sampled_count in item_tracker.items():
        # Get minimum count from sketch (Count-Min Sketch estimate)
        min_count = min(sketch[i][hash_func(item, i)] for i in range(depth))
        estimated_counts.append((item, min_count))
    
    return sorted(estimated_counts, key=lambda x: x[1], reverse=True)[:k]

# Performance comparison and usage examples
def compare_methods():
    """Compare different methods for finding frequent elements."""
    # Generate test data
    import random
    data = [random.choice(['A', 'B', 'C', 'D', 'E']) for _ in range(100000)]
    k = 3
    
    methods = [
        ("Basic Counter", top_k_frequent_basic),
        ("Heap-based", top_k_frequent_heap),
        ("Distributed", lambda d, k: top_k_frequent_distributed(d, k, 4))
    ]
    
    for name, method in methods:
        start_time = time.time()
        result = method(data, k)
        end_time = time.time()
        
        print(f"{name}:")
        print(f"  Time: {end_time - start_time:.4f}s")
        print(f"  Result: {result}")
        print()

# Real-world example: Log analysis
def analyze_web_logs(log_entries: List[str], k: int = 10) -> List[Tuple[str, int]]:
    """Analyze web server logs to find most frequent IP addresses."""
    import re
    
    # Extract IP addresses from log entries
    ip_pattern = r'^(\d+\.\d+\.\d+\.\d+)'
    ip_addresses = []
    
    for log_entry in log_entries:
        match = re.match(ip_pattern, log_entry)
        if match:
            ip_addresses.append(match.group(1))
    
    return top_k_frequent_basic(ip_addresses, k)

if __name__ == "__main__":
    # Example usage
    sample_data = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple', 'date']
    
    print("Sample data:", sample_data)
    print("Top 3 frequent items:", top_k_frequent_basic(sample_data, 3))
    
    # Performance comparison
    print("\n=== Performance Comparison ===")
    compare_methods()
    
    # Streaming example
    print("\n=== Streaming Example ===")
    def sample_stream():
        import random
        for _ in range(1000):
            yield random.choice(['X', 'Y', 'Z', 'W'])
    
    stream_results = list(top_k_frequent_streaming(sample_stream(), 2, window_size=100))
    print(f"Streaming results (last window): {stream_results[-1] if stream_results else 'No results'}")
```

### 21. Implement a data pipeline with error handling and monitoring.
**Answer:**
```python
import logging
import time
from abc import ABC, abstractmethod
from typing import Any, List, Optional
from dataclasses import dataclass

@dataclass
class PipelineMetrics:
    processed_records: int = 0
    failed_records: int = 0
    start_time: float = 0
    end_time: float = 0
    
    @property
    def duration(self):
        return self.end_time - self.start_time
    
    @property
    def success_rate(self):
        total = self.processed_records + self.failed_records
        return self.processed_records / total if total > 0 else 0

class PipelineStage(ABC):
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"pipeline.{name}")
    
    @abstractmethod
    def process(self, data: Any) -> Any:
        pass
    
    def __call__(self, data: Any) -> Any:
        self.logger.info(f"Starting stage: {self.name}")
        try:
            result = self.process(data)
            self.logger.info(f"Completed stage: {self.name}")
            return result
        except Exception as e:
            self.logger.error(f"Error in stage {self.name}: {str(e)}")
            raise

class DataPipeline:
    def __init__(self, stages: List[PipelineStage]):
        self.stages = stages
        self.metrics = PipelineMetrics()
        self.logger = logging.getLogger("pipeline")
    
    def run(self, data: Any) -> Any:
        self.metrics.start_time = time.time()
        
        try:
            current_data = data
            for stage in self.stages:
                current_data = stage(current_data)
            
            self.metrics.processed_records += 1
            return current_data
            
        except Exception as e:
            self.metrics.failed_records += 1
            self.logger.error(f"Pipeline failed: {str(e)}")
            raise
        finally:
            self.metrics.end_time = time.time()
    
    def get_metrics(self) -> PipelineMetrics:
        return self.metrics

# Example usage
class ExtractStage(PipelineStage):
    def process(self, data):
        # Extract data from source
        return {"raw_data": data, "extracted_at": time.time()}

class TransformStage(PipelineStage):
    def process(self, data):
        # Transform data
        transformed = data["raw_data"].upper()
        return {"transformed_data": transformed, "metadata": data}

class LoadStage(PipelineStage):
    def process(self, data):
        # Load data to destination
        self.logger.info(f"Loading: {data['transformed_data']}")
        return {"status": "loaded", "data": data}

# Create and run pipeline
pipeline = DataPipeline([
    ExtractStage("extract"),
    TransformStage("transform"),
    LoadStage("load")
])

result = pipeline.run("hello world")
metrics = pipeline.get_metrics()
print(f"Success rate: {metrics.success_rate:.2%}")
```

### 22. How do you implement multiprocessing for CPU-intensive data processing tasks?

**Answer:**
Multiprocessing bypasses the GIL limitation and enables true parallelism for CPU-bound tasks, essential for large-scale data processing.

**Code Example:**
```python
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed
import time
import numpy as np
from typing import List, Tuple, Any
import os

def cpu_intensive_task(data_chunk: List[int]) -> Tuple[int, float, int]:
    """Simulate CPU-intensive data processing.
    
    Args:
        data_chunk: List of integers to process
        
    Returns:
        Tuple of (sum, mean, max) of the chunk
    """
    # Simulate heavy computation
    result_sum = sum(x ** 2 for x in data_chunk)
    result_mean = sum(data_chunk) / len(data_chunk) if data_chunk else 0
    result_max = max(data_chunk) if data_chunk else 0
    
    return result_sum, result_mean, result_max

def process_large_dataset_multiprocessing(data: List[int], num_processes: int = None) -> dict:
    """Process large dataset using multiprocessing.
    
    Args:
        data: Large list of integers
        num_processes: Number of processes to use (default: CPU count)
        
    Returns:
        Dictionary with aggregated results
    """
    if num_processes is None:
        num_processes = mp.cpu_count()
    
    # Split data into chunks
    chunk_size = len(data) // num_processes
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    
    start_time = time.time()
    
    # Process chunks in parallel
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        # Submit all tasks
        future_to_chunk = {executor.submit(cpu_intensive_task, chunk): i 
                          for i, chunk in enumerate(chunks)}
        
        results = []
        for future in as_completed(future_to_chunk):
            chunk_idx = future_to_chunk[future]
            try:
                result = future.result()
                results.append((chunk_idx, result))
            except Exception as e:
                print(f"Chunk {chunk_idx} generated an exception: {e}")
    
    # Aggregate results
    total_sum = sum(result[1][0] for result in results)
    total_mean = sum(result[1][1] for result in results) / len(results)
    total_max = max(result[1][2] for result in results)
    
    end_time = time.time()
    
    return {
        'total_sum': total_sum,
        'average_mean': total_mean,
        'global_max': total_max,
        'processing_time': end_time - start_time,
        'num_processes': num_processes,
        'chunks_processed': len(results)
    }

# Shared memory example for large arrays
def process_numpy_array_shared_memory(array_size: int = 10000000) -> dict:
    """Process large NumPy array using shared memory."""
    
    def worker_function(shared_array, start_idx, end_idx, result_queue):
        """Worker function that processes part of shared array."""
        # Convert shared memory to numpy array
        np_array = np.frombuffer(shared_array.get_obj(), dtype=np.float64)
        
        # Process assigned slice
        slice_data = np_array[start_idx:end_idx]
        result = {
            'worker_id': os.getpid(),
            'start_idx': start_idx,
            'end_idx': end_idx,
            'sum': np.sum(slice_data),
            'mean': np.mean(slice_data),
            'std': np.std(slice_data)
        }
        result_queue.put(result)
    
    # Create shared memory array
    shared_array = mp.Array('d', array_size)  # 'd' for double (float64)
    
    # Initialize with random data
    np_array = np.frombuffer(shared_array.get_obj(), dtype=np.float64)
    np_array[:] = np.random.random(array_size)
    
    # Create processes
    num_processes = mp.cpu_count()
    chunk_size = array_size // num_processes
    processes = []
    result_queue = mp.Queue()
    
    start_time = time.time()
    
    # Start worker processes
    for i in range(num_processes):
        start_idx = i * chunk_size
        end_idx = start_idx + chunk_size if i < num_processes - 1 else array_size
        
        process = mp.Process(
            target=worker_function,
            args=(shared_array, start_idx, end_idx, result_queue)
        )
        processes.append(process)
        process.start()
    
    # Collect results
    results = []
    for _ in range(num_processes):
        results.append(result_queue.get())
    
    # Wait for all processes to complete
    for process in processes:
        process.join()
    
    end_time = time.time()
    
    # Aggregate results
    total_sum = sum(r['sum'] for r in results)
    weighted_mean = sum(r['mean'] * (r['end_idx'] - r['start_idx']) for r in results) / array_size
    
    return {
        'array_size': array_size,
        'total_sum': total_sum,
        'weighted_mean': weighted_mean,
        'processing_time': end_time - start_time,
        'num_processes': num_processes,
        'worker_results': results
    }

# Performance comparison
def compare_processing_methods(data_size: int = 1000000):
    """Compare single-threaded vs multiprocessing performance."""
    data = list(range(data_size))
    
    # Single-threaded processing
    start_time = time.time()
    single_result = cpu_intensive_task(data)
    single_time = time.time() - start_time
    
    # Multiprocessing
    multi_result = process_large_dataset_multiprocessing(data)
    multi_time = multi_result['processing_time']
    
    print(f"Data size: {data_size:,}")
    print(f"Single-threaded time: {single_time:.2f}s")
    print(f"Multiprocessing time: {multi_time:.2f}s")
    print(f"Speedup: {single_time / multi_time:.2f}x")
    print(f"Efficiency: {(single_time / multi_time) / mp.cpu_count() * 100:.1f}%")

if __name__ == "__main__":
    # Example usage
    compare_processing_methods(1000000)
    
    # Shared memory example
    shared_result = process_numpy_array_shared_memory(5000000)
    print(f"\nShared memory processing completed in {shared_result['processing_time']:.2f}s")
```

### 23. How do you implement custom iterators and generators for memory-efficient data processing?

**Answer:**
Custom iterators and generators enable processing of large datasets without loading everything into memory, crucial for big data applications.

**Code Example:**
```python
from typing import Iterator, Generator, Any, Optional
import csv
import json
import gzip
from pathlib import Path

class DataFileIterator:
    """Custom iterator for processing large data files line by line."""
    
    def __init__(self, file_path: str, file_type: str = 'csv', 
                 chunk_size: int = 1024, encoding: str = 'utf-8'):
        """Initialize file iterator.
        
        Args:
            file_path: Path to the data file
            file_type: Type of file ('csv', 'json', 'txt')
            chunk_size: Size of chunks to read
            encoding: File encoding
        """
        self.file_path = Path(file_path)
        self.file_type = file_type.lower()
        self.chunk_size = chunk_size
        self.encoding = encoding
        self._file_handle = None
        self._reader = None
        self._current_line = 0
    
    def __iter__(self) -> Iterator:
        """Return iterator object."""
        return self
    
    def __next__(self) -> dict:
        """Get next item from file."""
        if self._file_handle is None:
            self._open_file()
        
        try:
            if self.file_type == 'csv':
                row = next(self._reader)
                self._current_line += 1
                return dict(row)
            elif self.file_type == 'json':
                line = next(self._file_handle)
                self._current_line += 1
                return json.loads(line.strip())
            else:  # txt
                line = next(self._file_handle)
                self._current_line += 1
                return {'line_number': self._current_line, 'content': line.strip()}
                
        except StopIteration:
            self._close_file()
            raise StopIteration
    
    def _open_file(self):
        """Open file with appropriate handler."""
        if self.file_path.suffix == '.gz':
            self._file_handle = gzip.open(self.file_path, 'rt', encoding=self.encoding)
        else:
            self._file_handle = open(self.file_path, 'r', encoding=self.encoding)
        
        if self.file_type == 'csv':
            self._reader = csv.DictReader(self._file_handle)
    
    def _close_file(self):
        """Close file handle."""
        if self._file_handle:
            self._file_handle.close()
            self._file_handle = None
            self._reader = None
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self._close_file()

def batch_generator(iterable: Iterator, batch_size: int) -> Generator[list, None, None]:
    """Generate batches from an iterable.
    
    Args:
        iterable: Input iterable
        batch_size: Size of each batch
        
    Yields:
        Lists of items with specified batch size
    """
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    
    # Yield remaining items
    if batch:
        yield batch

def sliding_window_generator(iterable: Iterator, window_size: int) -> Generator[list, None, None]:
    """Generate sliding windows from an iterable.
    
    Args:
        iterable: Input iterable
        window_size: Size of sliding window
        
    Yields:
        Lists representing sliding windows
    """
    window = []
    for item in iterable:
        window.append(item)
        if len(window) > window_size:
            window.pop(0)
        if len(window) == window_size:
            yield window.copy()

class DataProcessor:
    """Memory-efficient data processor using generators."""
    
    def __init__(self, batch_size: int = 1000):
        self.batch_size = batch_size
    
    def filter_generator(self, data_iter: Iterator, 
                        filter_func: callable) -> Generator[Any, None, None]:
        """Filter data using generator.
        
        Args:
            data_iter: Input data iterator
            filter_func: Function to filter items
            
        Yields:
            Filtered items
        """
        for item in data_iter:
            if filter_func(item):
                yield item
    
    def transform_generator(self, data_iter: Iterator, 
                          transform_func: callable) -> Generator[Any, None, None]:
        """Transform data using generator.
        
        Args:
            data_iter: Input data iterator
            transform_func: Function to transform items
            
        Yields:
            Transformed items
        """
        for item in data_iter:
            try:
                transformed = transform_func(item)
                yield transformed
            except Exception as e:
                print(f"Error transforming item {item}: {e}")
                continue
    
    def aggregate_generator(self, data_iter: Iterator, 
                          key_func: callable, 
                          agg_func: callable) -> Generator[tuple, None, None]:
        """Aggregate data using generator with grouping.
        
        Args:
            data_iter: Input data iterator
            key_func: Function to extract grouping key
            agg_func: Function to aggregate values
            
        Yields:
            Tuples of (key, aggregated_value)
        """
        current_key = None
        current_group = []
        
        for item in data_iter:
            key = key_func(item)
            
            if current_key is None:
                current_key = key
            
            if key == current_key:
                current_group.append(item)
            else:
                # Yield aggregated result for previous group
                if current_group:
                    yield current_key, agg_func(current_group)
                
                # Start new group
                current_key = key
                current_group = [item]
        
        # Yield final group
        if current_group:
            yield current_key, agg_func(current_group)
    
    def process_pipeline(self, file_path: str, 
                        filter_func: Optional[callable] = None,
                        transform_func: Optional[callable] = None,
                        aggregate_key: Optional[callable] = None,
                        aggregate_func: Optional[callable] = None) -> Generator:
        """Complete processing pipeline using generators.
        
        Args:
            file_path: Path to input file
            filter_func: Optional filter function
            transform_func: Optional transform function
            aggregate_key: Optional aggregation key function
            aggregate_func: Optional aggregation function
            
        Yields:
            Processed data items
        """
        # Start with file iterator
        data_iter = DataFileIterator(file_path, 'csv')
        
        # Apply filter if provided
        if filter_func:
            data_iter = self.filter_generator(data_iter, filter_func)
        
        # Apply transformation if provided
        if transform_func:
            data_iter = self.transform_generator(data_iter, transform_func)
        
        # Apply aggregation if provided
        if aggregate_key and aggregate_func:
            data_iter = self.aggregate_generator(data_iter, aggregate_key, aggregate_func)
        
        # Process in batches
        for batch in batch_generator(data_iter, self.batch_size):
            yield batch

# Usage examples
def example_usage():
    """Demonstrate memory-efficient data processing."""
    
    # Example 1: Process large CSV file
    def is_valid_record(record):
        """Filter function to keep only valid records."""
        return record.get('amount', 0) > 0
    
    def normalize_record(record):
        """Transform function to normalize record."""
        return {
            'id': record.get('id', ''),
            'amount': float(record.get('amount', 0)),
            'category': record.get('category', '').upper()
        }
    
    def get_category(record):
        """Key function for aggregation."""
        return record['category']
    
    def sum_amounts(records):
        """Aggregation function to sum amounts."""
        return sum(record['amount'] for record in records)
    
    # Create processor
    processor = DataProcessor(batch_size=1000)
    
    # Process data pipeline
    print("Processing data pipeline...")
    batch_count = 0
    total_records = 0
    
    try:
        for batch in processor.process_pipeline(
            'large_data.csv',
            filter_func=is_valid_record,
            transform_func=normalize_record,
            aggregate_key=get_category,
            aggregate_func=sum_amounts
        ):
            batch_count += 1
            total_records += len(batch)
            
            # Process batch (e.g., save to database)
            print(f"Processed batch {batch_count} with {len(batch)} records")
            
            # Show sample of first batch
            if batch_count == 1:
                print(f"Sample data: {batch[:3]}")
    
    except FileNotFoundError:
        print("Demo file not found, creating sample data...")
        
        # Create sample data generator
        def sample_data_generator(num_records: int = 10000):
            """Generate sample data for demonstration."""
            import random
            categories = ['A', 'B', 'C', 'D']
            
            for i in range(num_records):
                yield {
                    'id': f'ID_{i:06d}',
                    'amount': random.uniform(10, 1000),
                    'category': random.choice(categories)
                }
        
        # Process sample data
        sample_iter = sample_data_generator(10000)
        filtered_iter = processor.filter_generator(sample_iter, is_valid_record)
        transformed_iter = processor.transform_generator(filtered_iter, normalize_record)
        
        # Process in batches
        for i, batch in enumerate(batch_generator(transformed_iter, 1000)):
            print(f"Sample batch {i+1}: {len(batch)} records")
            if i >= 2:  # Process only first 3 batches for demo
                break
    
    print(f"\nTotal batches processed: {batch_count}")
    print(f"Total records processed: {total_records}")

if __name__ == "__main__":
    example_usage()
```

### 24. How do you implement thread-safe data structures and handle concurrency?

**Answer:**
Thread-safe data structures prevent race conditions in multi-threaded environments, essential for concurrent data processing applications.

**Code Example:**
```python
import threading
import queue
import time
from typing import Any, Optional, Dict, List
from collections import defaultdict, deque
from contextlib import contextmanager
import weakref

class ThreadSafeCounter:
    """Thread-safe counter with atomic operations."""
    
    def __init__(self, initial_value: int = 0):
        self._value = initial_value
        self._lock = threading.RLock()  # Reentrant lock
    
    def increment(self, amount: int = 1) -> int:
        """Atomically increment counter."""
        with self._lock:
            self._value += amount
            return self._value
    
    def decrement(self, amount: int = 1) -> int:
        """Atomically decrement counter."""
        with self._lock:
            self._value -= amount
            return self._value
    
    def get(self) -> int:
        """Get current value."""
        with self._lock:
            return self._value
    
    def set(self, value: int) -> None:
        """Set counter value."""
        with self._lock:
            self._value = value
    
    def compare_and_swap(self, expected: int, new_value: int) -> bool:
        """Atomic compare and swap operation."""
        with self._lock:
            if self._value == expected:
                self._value = new_value
                return True
            return False

class ThreadSafeDict:
    """Thread-safe dictionary wrapper."""
    
    def __init__(self):
        self._dict = {}
        self._lock = threading.RWLock() if hasattr(threading, 'RWLock') else threading.RLock()
    
    def get(self, key: Any, default: Any = None) -> Any:
        """Thread-safe get operation."""
        with self._lock:
            return self._dict.get(key, default)
    
    def set(self, key: Any, value: Any) -> None:
        """Thread-safe set operation."""
        with self._lock:
            self._dict[key] = value
    
    def update(self, other: Dict[Any, Any]) -> None:
        """Thread-safe update operation."""
        with self._lock:
            self._dict.update(other)
    
    def pop(self, key: Any, default: Any = None) -> Any:
        """Thread-safe pop operation."""
        with self._lock:
            return self._dict.pop(key, default)
    
    def keys(self) -> List[Any]:
        """Get snapshot of keys."""
        with self._lock:
            return list(self._dict.keys())
    
    def items(self) -> List[tuple]:
        """Get snapshot of items."""
        with self._lock:
            return list(self._dict.items())
    
    def __len__(self) -> int:
        with self._lock:
            return len(self._dict)

class ThreadSafeQueue:
    """Enhanced thread-safe queue with additional features."""
    
    def __init__(self, maxsize: int = 0):
        self._queue = queue.Queue(maxsize=maxsize)
        self._stats_lock = threading.Lock()
        self._total_items_added = 0
        self._total_items_removed = 0
    
    def put(self, item: Any, block: bool = True, timeout: Optional[float] = None) -> None:
        """Put item in queue with statistics tracking."""
        self._queue.put(item, block=block, timeout=timeout)
        with self._stats_lock:
            self._total_items_added += 1
    
    def get(self, block: bool = True, timeout: Optional[float] = None) -> Any:
        """Get item from queue with statistics tracking."""
        item = self._queue.get(block=block, timeout=timeout)
        with self._stats_lock:
            self._total_items_removed += 1
        return item
    
    def qsize(self) -> int:
        """Get approximate queue size."""
        return self._queue.qsize()
    
    def empty(self) -> bool:
        """Check if queue is empty."""
        return self._queue.empty()
    
    def full(self) -> bool:
        """Check if queue is full."""
        return self._queue.full()
    
    def get_stats(self) -> Dict[str, int]:
        """Get queue statistics."""
        with self._stats_lock:
            return {
                'current_size': self.qsize(),
                'total_added': self._total_items_added,
                'total_removed': self._total_items_removed,
                'net_items': self._total_items_added - self._total_items_removed
            }

class ConnectionPool:
    """Thread-safe connection pool for database connections."""
    
    def __init__(self, create_connection_func: callable, 
                 max_connections: int = 10, 
                 timeout: float = 30.0):
        """Initialize connection pool.
        
        Args:
            create_connection_func: Function to create new connections
            max_connections: Maximum number of connections in pool
            timeout: Timeout for getting connections
        """
        self._create_connection = create_connection_func
        self._max_connections = max_connections
        self._timeout = timeout
        self._pool = queue.Queue(maxsize=max_connections)
        self._created_connections = 0
        self._lock = threading.Lock()
        self._active_connections = weakref.WeakSet()
    
    def get_connection(self):
        """Get connection from pool or create new one."""
        try:
            # Try to get existing connection
            connection = self._pool.get(block=False)
            return self._wrap_connection(connection)
        except queue.Empty:
            # Create new connection if under limit
            with self._lock:
                if self._created_connections < self._max_connections:
                    connection = self._create_connection()
                    self._created_connections += 1
                    return self._wrap_connection(connection)
            
            # Wait for available connection
            connection = self._pool.get(timeout=self._timeout)
            return self._wrap_connection(connection)
    
    def _wrap_connection(self, connection):
        """Wrap connection to automatically return to pool."""
        class PooledConnection:
            def __init__(self, conn, pool):
                self._conn = conn
                self._pool = pool
                self._returned = False
            
            def __getattr__(self, name):
                return getattr(self._conn, name)
            
            def close(self):
                if not self._returned:
                    self._pool._return_connection(self._conn)
                    self._returned = True
            
            def __enter__(self):
                return self
            
            def __exit__(self, exc_type, exc_val, exc_tb):
                self.close()
        
        wrapped = PooledConnection(connection, self)
        self._active_connections.add(wrapped)
        return wrapped
    
    def _return_connection(self, connection):
        """Return connection to pool."""
        try:
            self._pool.put(connection, block=False)
        except queue.Full:
            # Pool is full, close connection
            if hasattr(connection, 'close'):
                connection.close()
            with self._lock:
                self._created_connections -= 1
    
    def get_stats(self) -> Dict[str, int]:
        """Get pool statistics."""
        return {
            'pool_size': self._pool.qsize(),
            'created_connections': self._created_connections,
            'max_connections': self._max_connections,
            'active_connections': len(self._active_connections)
        }

# Producer-Consumer pattern with thread safety
class ProducerConsumerSystem:
    """Thread-safe producer-consumer system for data processing."""
    
    def __init__(self, queue_size: int = 100, num_consumers: int = 3):
        self.queue = ThreadSafeQueue(maxsize=queue_size)
        self.num_consumers = num_consumers
        self.running = threading.Event()
        self.running.set()
        self.consumers = []
        self.producer_thread = None
        self.stats = ThreadSafeCounter()
    
    def producer(self, data_generator: callable):
        """Producer function that generates data."""
        try:
            for item in data_generator():
                if not self.running.is_set():
                    break
                
                self.queue.put(item, timeout=1.0)
                self.stats.increment()
                
        except queue.Full:
            print("Queue is full, producer stopping")
        except Exception as e:
            print(f"Producer error: {e}")
        finally:
            # Signal end of data
            for _ in range(self.num_consumers):
                try:
                    self.queue.put(None, timeout=1.0)  # Sentinel value
                except queue.Full:
                    pass
    
    def consumer(self, consumer_id: int, process_func: callable):
        """Consumer function that processes data."""
        processed_count = 0
        
        try:
            while self.running.is_set():
                try:
                    item = self.queue.get(timeout=1.0)
                    
                    # Check for sentinel value
                    if item is None:
                        break
                    
                    # Process item
                    result = process_func(item)
                    processed_count += 1
                    
                    if processed_count % 100 == 0:
                        print(f"Consumer {consumer_id} processed {processed_count} items")
                        
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"Consumer {consumer_id} error: {e}")
                    
        finally:
            print(f"Consumer {consumer_id} finished, processed {processed_count} items")
    
    def start(self, data_generator: callable, process_func: callable):
        """Start producer-consumer system."""
        # Start producer
        self.producer_thread = threading.Thread(
            target=self.producer,
            args=(data_generator,)
        )
        self.producer_thread.start()
        
        # Start consumers
        for i in range(self.num_consumers):
            consumer_thread = threading.Thread(
                target=self.consumer,
                args=(i, process_func)
            )
            self.consumers.append(consumer_thread)
            consumer_thread.start()
    
    def stop(self):
        """Stop producer-consumer system."""
        self.running.clear()
        
        # Wait for producer to finish
        if self.producer_thread:
            self.producer_thread.join(timeout=5.0)
        
        # Wait for consumers to finish
        for consumer in self.consumers:
            consumer.join(timeout=5.0)
        
        # Print final statistics
        queue_stats = self.queue.get_stats()
        print(f"Final stats: {queue_stats}")
        print(f"Items produced: {self.stats.get()}")

# Usage example
def example_concurrent_processing():
    """Demonstrate thread-safe concurrent processing."""
    
    def data_generator():
        """Generate sample data."""
        for i in range(1000):
            yield {'id': i, 'value': i * 2, 'timestamp': time.time()}
            time.sleep(0.001)  # Simulate data generation delay
    
    def process_item(item):
        """Process individual item."""
        # Simulate processing time
        time.sleep(0.01)
        return {
            'processed_id': item['id'],
            'result': item['value'] ** 2,
            'processed_at': time.time()
        }
    
    # Create and start system
    system = ProducerConsumerSystem(queue_size=50, num_consumers=4)
    
    print("Starting producer-consumer system...")
    system.start(data_generator, process_item)
    
    # Let it run for a while
    time.sleep(5)
    
    # Stop system
    print("Stopping system...")
    system.stop()
    
    print("System stopped.")

if __name__ == "__main__":
    example_concurrent_processing()
```

### 25. How do you implement data validation and schema enforcement in Python?

**Answer:**
Data validation ensures data quality and consistency, critical for reliable data pipelines and analytics.

**Code Example:**
```python
from typing import Any, Dict, List, Optional, Union, Type
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from datetime import datetime, date
import re
import json
from enum import Enum

class ValidationError(Exception):
    """Custom exception for validation errors."""
    def __init__(self, field: str, value: Any, message: str):
        self.field = field
        self.value = value
        self.message = message
        super().__init__(f"Validation error for field '{field}': {message}")

class ValidationResult:
    """Result of validation operation."""
    def __init__(self):
        self.is_valid = True
        self.errors: List[ValidationError] = []
        self.warnings: List[str] = []
    
    def add_error(self, field: str, value: Any, message: str):
        """Add validation error."""
        self.is_valid = False
        self.errors.append(ValidationError(field, value, message))
    
    def add_warning(self, message: str):
        """Add validation warning."""
        self.warnings.append(message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            'is_valid': self.is_valid,
            'errors': [{
                'field': error.field,
                'value': error.value,
                'message': error.message
            } for error in self.errors],
            'warnings': self.warnings
        }

class Validator(ABC):
    """Abstract base class for validators."""
    
    @abstractmethod
    def validate(self, value: Any) -> ValidationResult:
        """Validate a value."""
        pass

class TypeValidator(Validator):
    """Validates data types."""
    
    def __init__(self, expected_type: Type, allow_none: bool = False):
        self.expected_type = expected_type
        self.allow_none = allow_none
    
    def validate(self, value: Any) -> ValidationResult:
        result = ValidationResult()
        
        if value is None and self.allow_none:
            return result
        
        if not isinstance(value, self.expected_type):
            result.add_error(
                'type_check',
                value,
                f"Expected {self.expected_type.__name__}, got {type(value).__name__}"
            )
        
        return result

class RangeValidator(Validator):
    """Validates numeric ranges."""
    
    def __init__(self, min_value: Optional[Union[int, float]] = None,
                 max_value: Optional[Union[int, float]] = None,
                 inclusive: bool = True):
        self.min_value = min_value
        self.max_value = max_value
        self.inclusive = inclusive
    
    def validate(self, value: Any) -> ValidationResult:
        result = ValidationResult()
        
        if not isinstance(value, (int, float)):
            result.add_error('range_check', value, "Value must be numeric")
            return result
        
        if self.min_value is not None:
            if self.inclusive and value < self.min_value:
                result.add_error('range_check', value, f"Value must be >= {self.min_value}")
            elif not self.inclusive and value <= self.min_value:
                result.add_error('range_check', value, f"Value must be > {self.min_value}")
        
        if self.max_value is not None:
            if self.inclusive and value > self.max_value:
                result.add_error('range_check', value, f"Value must be <= {self.max_value}")
            elif not self.inclusive and value >= self.max_value:
                result.add_error('range_check', value, f"Value must be < {self.max_value}")
        
        return result

class RegexValidator(Validator):
    """Validates strings against regex patterns."""
    
    def __init__(self, pattern: str, flags: int = 0):
        self.pattern = pattern
        self.regex = re.compile(pattern, flags)
    
    def validate(self, value: Any) -> ValidationResult:
        result = ValidationResult()
        
        if not isinstance(value, str):
            result.add_error('regex_check', value, "Value must be a string")
            return result
        
        if not self.regex.match(value):
            result.add_error('regex_check', value, f"Value does not match pattern: {self.pattern}")
        
        return result

class LengthValidator(Validator):
    """Validates string/list length."""
    
    def __init__(self, min_length: Optional[int] = None,
                 max_length: Optional[int] = None):
        self.min_length = min_length
        self.max_length = max_length
    
    def validate(self, value: Any) -> ValidationResult:
        result = ValidationResult()
        
        if not hasattr(value, '__len__'):
            result.add_error('length_check', value, "Value must have length")
            return result
        
        length = len(value)
        
        if self.min_length is not None and length < self.min_length:
            result.add_error('length_check', value, f"Length must be >= {self.min_length}")
        
        if self.max_length is not None and length > self.max_length:
            result.add_error('length_check', value, f"Length must be <= {self.max_length}")
        
        return result

class ChoiceValidator(Validator):
    """Validates value is in allowed choices."""
    
    def __init__(self, choices: List[Any]):
        self.choices = choices
    
    def validate(self, value: Any) -> ValidationResult:
        result = ValidationResult()
        
        if value not in self.choices:
            result.add_error('choice_check', value, f"Value must be one of: {self.choices}")
        
        return result

class DateValidator(Validator):
    """Validates date formats and ranges."""
    
    def __init__(self, date_format: str = '%Y-%m-%d',
                 min_date: Optional[date] = None,
                 max_date: Optional[date] = None):
        self.date_format = date_format
        self.min_date = min_date
        self.max_date = max_date
    
    def validate(self, value: Any) -> ValidationResult:
        result = ValidationResult()
        
        # Convert string to date if necessary
        if isinstance(value, str):
            try:
                parsed_date = datetime.strptime(value, self.date_format).date()
            except ValueError:
                result.add_error('date_format', value, f"Invalid date format, expected: {self.date_format}")
                return result
        elif isinstance(value, datetime):
            parsed_date = value.date()
        elif isinstance(value, date):
            parsed_date = value
        else:
            result.add_error('date_type', value, "Value must be a date, datetime, or date string")
            return result
        
        # Check date range
        if self.min_date and parsed_date < self.min_date:
            result.add_error('date_range', value, f"Date must be >= {self.min_date}")
        
        if self.max_date and parsed_date > self.max_date:
            result.add_error('date_range', value, f"Date must be <= {self.max_date}")
        
        return result

@dataclass
class FieldSchema:
    """Schema definition for a single field."""
    name: str
    validators: List[Validator] = field(default_factory=list)
    required: bool = True
    default: Any = None
    description: str = ""
    
    def validate(self, value: Any) -> ValidationResult:
        """Validate field value against all validators."""
        combined_result = ValidationResult()
        
        # Check if field is required
        if value is None:
            if self.required:
                combined_result.add_error(self.name, value, "Field is required")
                return combined_result
            else:
                return combined_result  # Optional field with None value is valid
        
        # Run all validators
        for validator in self.validators:
            result = validator.validate(value)
            if not result.is_valid:
                combined_result.is_valid = False
                combined_result.errors.extend(result.errors)
            combined_result.warnings.extend(result.warnings)
        
        return combined_result

class DataSchema:
    """Complete schema for data validation."""
    
    def __init__(self, name: str, fields: List[FieldSchema]):
        self.name = name
        self.fields = {field.name: field for field in fields}
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate complete data record."""
        combined_result = ValidationResult()
        
        # Check for unexpected fields
        unexpected_fields = set(data.keys()) - set(self.fields.keys())
        for field in unexpected_fields:
            combined_result.add_warning(f"Unexpected field: {field}")
        
        # Validate each field
        for field_name, field_schema in self.fields.items():
            field_value = data.get(field_name)
            
            field_result = field_schema.validate(field_value)
            if not field_result.is_valid:
                combined_result.is_valid = False
                combined_result.errors.extend(field_result.errors)
            combined_result.warnings.extend(field_result.warnings)
        
        return combined_result
    
    def validate_batch(self, data_list: List[Dict[str, Any]]) -> List[ValidationResult]:
        """Validate batch of records."""
        return [self.validate(record) for record in data_list]
    
    def clean_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean data by applying defaults and removing invalid fields."""
        cleaned = {}
        
        for field_name, field_schema in self.fields.items():
            if field_name in data:
                cleaned[field_name] = data[field_name]
            elif field_schema.default is not None:
                cleaned[field_name] = field_schema.default
        
        return cleaned

# Predefined common schemas
class CommonSchemas:
    """Collection of commonly used schemas."""
    
    @staticmethod
    def email_schema() -> DataSchema:
        """Schema for email validation."""
        return DataSchema('email', [
            FieldSchema(
                name='email',
                validators=[
                    TypeValidator(str),
                    RegexValidator(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
                    LengthValidator(max_length=254)
                ],
                description='Valid email address'
            )
        ])
    
    @staticmethod
    def user_schema() -> DataSchema:
        """Schema for user data validation."""
        return DataSchema('user', [
            FieldSchema(
                name='id',
                validators=[TypeValidator(int), RangeValidator(min_value=1)],
                description='Unique user ID'
            ),
            FieldSchema(
                name='username',
                validators=[
                    TypeValidator(str),
                    LengthValidator(min_length=3, max_length=50),
                    RegexValidator(r'^[a-zA-Z0-9_]+$')
                ],
                description='Username (alphanumeric and underscore only)'
            ),
            FieldSchema(
                name='email',
                validators=[
                    TypeValidator(str),
                    RegexValidator(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
                ],
                description='Valid email address'
            ),
            FieldSchema(
                name='age',
                validators=[TypeValidator(int), RangeValidator(min_value=0, max_value=150)],
                required=False,
                description='User age'
            ),
            FieldSchema(
                name='status',
                validators=[ChoiceValidator(['active', 'inactive', 'suspended'])],
                default='active',
                description='User account status'
            ),
            FieldSchema(
                name='created_at',
                validators=[DateValidator()],
                description='Account creation date'
            )
        ])
    
    @staticmethod
    def transaction_schema() -> DataSchema:
        """Schema for financial transaction validation."""
        return DataSchema('transaction', [
            FieldSchema(
                name='transaction_id',
                validators=[TypeValidator(str), LengthValidator(min_length=10, max_length=50)],
                description='Unique transaction identifier'
            ),
            FieldSchema(
                name='amount',
                validators=[TypeValidator((int, float)), RangeValidator(min_value=0.01)],
                description='Transaction amount (must be positive)'
            ),
            FieldSchema(
                name='currency',
                validators=[ChoiceValidator(['USD', 'EUR', 'GBP', 'JPY', 'CAD'])],
                description='Transaction currency'
            ),
            FieldSchema(
                name='transaction_type',
                validators=[ChoiceValidator(['debit', 'credit', 'transfer'])],
                description='Type of transaction'
            ),
            FieldSchema(
                name='timestamp',
                validators=[DateValidator('%Y-%m-%d %H:%M:%S')],
                description='Transaction timestamp'
            )
        ])

# Usage examples
def example_data_validation():
    """Demonstrate comprehensive data validation."""
    
    # Create user schema
    user_schema = CommonSchemas.user_schema()
    
    # Test data
    test_users = [
        {
            'id': 1,
            'username': 'john_doe',
            'email': 'john@example.com',
            'age': 30,
            'status': 'active',
            'created_at': '2023-01-15'
        },
        {
            'id': 'invalid',  # Invalid type
            'username': 'jd',  # Too short
            'email': 'invalid-email',  # Invalid format
            'age': -5,  # Invalid range
            'status': 'unknown',  # Invalid choice
            'created_at': '2023-13-45'  # Invalid date
        },
        {
            'id': 3,
            'username': 'jane_smith',
            'email': 'jane@example.com',
            # Missing required created_at
            'extra_field': 'unexpected'  # Unexpected field
        }
    ]
    
    print("Validating user data...")
    for i, user_data in enumerate(test_users):
        print(f"\n--- User {i+1} ---")
        result = user_schema.validate(user_data)
        
        if result.is_valid:
            print("✅ Valid data")
            cleaned_data = user_schema.clean_data(user_data)
            print(f"Cleaned data: {json.dumps(cleaned_data, indent=2)}")
        else:
            print("❌ Invalid data")
            for error in result.errors:
                print(f"  Error: {error.message}")
        
        if result.warnings:
            print("⚠️  Warnings:")
            for warning in result.warnings:
                print(f"  Warning: {warning}")
    
    # Batch validation example
    print("\n=== Batch Validation ===")
    batch_results = user_schema.validate_batch(test_users)
    valid_count = sum(1 for result in batch_results if result.is_valid)
    print(f"Valid records: {valid_count}/{len(test_users)}")
    
    # Transaction schema example
    print("\n=== Transaction Validation ===")
    transaction_schema = CommonSchemas.transaction_schema()
    
    transaction_data = {
        'transaction_id': 'TXN_123456789',
        'amount': 99.99,
        'currency': 'USD',
        'transaction_type': 'debit',
        'timestamp': '2023-01-15 14:30:00'
    }
    
    result = transaction_schema.validate(transaction_data)
    if result.is_valid:
        print("✅ Transaction data is valid")
    else:
        print("❌ Transaction data is invalid")
        for error in result.errors:
            print(f"  Error: {error.message}")

if __name__ == "__main__":
    example_data_validation()
```

---

---

## 🎯 **Conceptual & Theoretical Questions**

### 26. What are Python's design principles and philosophy?
**Answer:**
Python follows the "Zen of Python" (PEP 20) principles:
- **Beautiful is better than ugly**
- **Explicit is better than implicit**
- **Simple is better than complex**
- **Readability counts**
- **There should be one obvious way to do it**

### 27. Explain Python's object model and everything being an object
**Answer:**
In Python, everything is an object with:
- **Identity**: Unique identifier (id())
- **Type**: Defines operations (type())
- **Value**: The data itself

```python
# Everything is an object
print(type(5))          # <class 'int'>
print(type(len))        # <class 'builtin_function_or_method'>
print(type(int))        # <class 'type'>
print(hasattr(5, '__add__'))  # True
```

### 28. What are metaclasses and when would you use them?
**Answer:**
Metaclasses are "classes that create classes" - they define how classes are constructed.

```python
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = "Connected"

# Usage
db1 = Database()
db2 = Database()
print(db1 is db2)  # True
```

### 29. How does Python's import system work?
**Answer:**
Python's import system involves:
1. **Module Search**: sys.path directories
2. **Module Loading**: Compile .py to bytecode
3. **Module Caching**: Store in sys.modules
4. **Namespace Creation**: Execute module code

### 30. What are descriptors and how do they work?
**Answer:**
Descriptors define how attribute access is handled through `__get__`, `__set__`, and `__delete__` methods.

```python
class ValidatedAttribute:
    def __init__(self, validator):
        self.validator = validator
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value):
        if not self.validator(value):
            raise ValueError(f"Invalid value for {self.name}")
        obj.__dict__[self.name] = value

class Person:
    age = ValidatedAttribute(lambda x: isinstance(x, int) and x >= 0)
```

---

## 🏢 **System Design & Architecture Questions**

### 31. How would you design a scalable data processing system using Python?
**Answer:**
**Architecture Components:**
- **Message Queue**: Redis/RabbitMQ for task distribution
- **Worker Processes**: Celery for distributed processing
- **Data Storage**: PostgreSQL + Redis for caching
- **API Layer**: FastAPI for REST endpoints
- **Monitoring**: Prometheus + Grafana

### 32. Explain different Python deployment strategies
**Answer:**
**Deployment Options:**
- **Traditional**: Virtual environments + systemd
- **Containerized**: Docker + Kubernetes
- **Serverless**: AWS Lambda, Google Cloud Functions
- **Platform-as-a-Service**: Heroku, Google App Engine

### 33. How do you handle configuration management in Python applications?
**Answer:**
```python
# Using environment variables and config classes
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class DatabaseConfig:
    host: str = os.getenv('DB_HOST', 'localhost')
    port: int = int(os.getenv('DB_PORT', '5432'))
    username: str = os.getenv('DB_USER', 'postgres')
    password: str = os.getenv('DB_PASSWORD', '')
    database: str = os.getenv('DB_NAME', 'myapp')
    
    @property
    def connection_string(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

@dataclass
class AppConfig:
    debug: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    secret_key: str = os.getenv('SECRET_KEY', 'dev-key')
    database: DatabaseConfig = DatabaseConfig()
    redis_url: str = os.getenv('REDIS_URL', 'redis://localhost:6379')
```

---

## 🔍 **Debugging & Troubleshooting Questions**

### 34. How do you debug memory leaks in Python applications?
**Answer:**
**Tools and Techniques:**
- **memory_profiler**: Line-by-line memory usage
- **tracemalloc**: Built-in memory tracking
- **objgraph**: Object reference tracking
- **gc module**: Garbage collection analysis

```python
import tracemalloc
import gc

# Start tracing
tracemalloc.start()

# Your code here
data = [i for i in range(1000000)]

# Get memory usage
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage: {current / 1024 / 1024:.1f} MB")
print(f"Peak memory usage: {peak / 1024 / 1024:.1f} MB")

# Check for circular references
print(f"Garbage collection stats: {gc.get_stats()}")
```

### 35. What are common Python performance bottlenecks and solutions?
**Answer:**
**Common Bottlenecks:**
1. **String Concatenation**: Use join() instead of +=
2. **List Operations**: Use list comprehensions, avoid repeated append()
3. **Dictionary Lookups**: Use defaultdict, consider sets for membership
4. **Function Calls**: Minimize function call overhead
5. **I/O Operations**: Use async/await, connection pooling

---

## 🧪 **Testing & Quality Assurance Questions**

### 36. How do you implement comprehensive testing strategies in Python?
**Answer:**
**Testing Pyramid:**
- **Unit Tests**: Test individual functions/methods
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete workflows
- **Performance Tests**: Load and stress testing

```python
import pytest
from unittest.mock import Mock, patch

class TestDataProcessor:
    @pytest.fixture
    def sample_data(self):
        return [{'id': 1, 'value': 100}, {'id': 2, 'value': 200}]
    
    def test_process_data_success(self, sample_data):
        processor = DataProcessor()
        result = processor.process(sample_data)
        assert len(result) == 2
        assert result[0]['processed'] == True
    
    @patch('requests.get')
    def test_api_call_with_mock(self, mock_get):
        mock_get.return_value.json.return_value = {'status': 'success'}
        result = fetch_data_from_api('http://example.com')
        assert result['status'] == 'success'
    
    def test_error_handling(self):
        processor = DataProcessor()
        with pytest.raises(ValueError):
            processor.process(None)
```

### 37. How do you ensure code quality in Python projects?
**Answer:**
**Code Quality Tools:**
- **Linting**: pylint, flake8, black (formatting)
- **Type Checking**: mypy, pyright
- **Security**: bandit, safety
- **Complexity**: radon, mccabe
- **Documentation**: pydocstyle

---

## 🌐 **Integration & API Questions**

### 38. How do you design and implement RESTful APIs in Python?
**Answer:**
```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Data API", version="1.0.0")

class DataModel(BaseModel):
    id: int
    name: str
    value: float
    category: Optional[str] = None

class DataResponse(BaseModel):
    data: List[DataModel]
    total: int
    page: int
    per_page: int

@app.get("/data", response_model=DataResponse)
async def get_data(
    page: int = 1,
    per_page: int = 10,
    category: Optional[str] = None
):
    # Implement pagination and filtering
    filtered_data = filter_data(category) if category else get_all_data()
    paginated_data = paginate(filtered_data, page, per_page)
    
    return DataResponse(
        data=paginated_data,
        total=len(filtered_data),
        page=page,
        per_page=per_page
    )

@app.post("/data", response_model=DataModel)
async def create_data(data: DataModel):
    # Validate and create data
    created_data = create_data_record(data)
    return created_data
```

### 39. How do you handle authentication and authorization in Python web applications?
**Answer:**
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_role(required_role: str):
    def role_checker(current_user: str = Depends(verify_token)):
        user_roles = get_user_roles(current_user)
        if required_role not in user_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return role_checker

@app.get("/admin/data")
async def admin_only_endpoint(current_user: str = Depends(require_role("admin"))):
    return {"message": "Admin access granted", "user": current_user}
```

---

## 📊 **Data Engineering Specific Scenarios**

### 40. How would you implement a real-time data pipeline monitoring system?
**Answer:**
```python
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

class PipelineStatus(Enum):
    RUNNING = "running"
    FAILED = "failed"
    COMPLETED = "completed"
    PAUSED = "paused"

@dataclass
class PipelineMetrics:
    pipeline_id: str
    status: PipelineStatus
    records_processed: int
    records_failed: int
    processing_rate: float  # records per second
    last_updated: datetime
    error_message: str = None

class PipelineMonitor:
    def __init__(self):
        self.pipelines: Dict[str, PipelineMetrics] = {}
        self.alerts = []
        self.logger = logging.getLogger(__name__)
    
    async def monitor_pipeline(self, pipeline_id: str):
        """Monitor a specific pipeline"""
        while True:
            try:
                metrics = await self.collect_metrics(pipeline_id)
                self.pipelines[pipeline_id] = metrics
                
                # Check for alerts
                await self.check_alerts(metrics)
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Error monitoring pipeline {pipeline_id}: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    async def collect_metrics(self, pipeline_id: str) -> PipelineMetrics:
        """Collect metrics from pipeline"""
        # Implementation would connect to actual pipeline
        # This is a mock implementation
        return PipelineMetrics(
            pipeline_id=pipeline_id,
            status=PipelineStatus.RUNNING,
            records_processed=1000,
            records_failed=5,
            processing_rate=50.0,
            last_updated=datetime.now()
        )
    
    async def check_alerts(self, metrics: PipelineMetrics):
        """Check for alert conditions"""
        # High error rate
        if metrics.records_failed > 0:
            error_rate = metrics.records_failed / (metrics.records_processed + metrics.records_failed)
            if error_rate > 0.05:  # 5% error rate threshold
                await self.send_alert(f"High error rate in {metrics.pipeline_id}: {error_rate:.2%}")
        
        # Low processing rate
        if metrics.processing_rate < 10.0:  # Less than 10 records/second
            await self.send_alert(f"Low processing rate in {metrics.pipeline_id}: {metrics.processing_rate} rec/sec")
        
        # Pipeline failure
        if metrics.status == PipelineStatus.FAILED:
            await self.send_alert(f"Pipeline {metrics.pipeline_id} failed: {metrics.error_message}")
    
    async def send_alert(self, message: str):
        """Send alert notification"""
        self.alerts.append({
            'timestamp': datetime.now(),
            'message': message,
            'severity': 'high'
        })
        self.logger.warning(f"ALERT: {message}")
        # Could integrate with Slack, email, PagerDuty, etc.
```

### 41. How do you implement data lineage tracking in Python?
**Answer:**
```python
from typing import Dict, List, Set
from dataclasses import dataclass, field
from datetime import datetime
import json

@dataclass
class DataAsset:
    name: str
    asset_type: str  # table, file, api, etc.
    location: str
    schema: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DataTransformation:
    transformation_id: str
    name: str
    inputs: List[DataAsset]
    outputs: List[DataAsset]
    transformation_logic: str
    timestamp: datetime
    owner: str

class DataLineageTracker:
    def __init__(self):
        self.assets: Dict[str, DataAsset] = {}
        self.transformations: Dict[str, DataTransformation] = {}
        self.lineage_graph: Dict[str, Set[str]] = {}  # asset -> dependent assets
    
    def register_asset(self, asset: DataAsset):
        """Register a data asset"""
        self.assets[asset.name] = asset
        if asset.name not in self.lineage_graph:
            self.lineage_graph[asset.name] = set()
    
    def register_transformation(self, transformation: DataTransformation):
        """Register a data transformation"""
        self.transformations[transformation.transformation_id] = transformation
        
        # Update lineage graph
        for input_asset in transformation.inputs:
            for output_asset in transformation.outputs:
                self.lineage_graph[input_asset.name].add(output_asset.name)
    
    def get_upstream_dependencies(self, asset_name: str) -> Set[str]:
        """Get all upstream dependencies of an asset"""
        dependencies = set()
        
        def traverse_upstream(current_asset):
            for transformation in self.transformations.values():
                for output in transformation.outputs:
                    if output.name == current_asset:
                        for input_asset in transformation.inputs:
                            if input_asset.name not in dependencies:
                                dependencies.add(input_asset.name)
                                traverse_upstream(input_asset.name)
        
        traverse_upstream(asset_name)
        return dependencies
    
    def get_downstream_dependencies(self, asset_name: str) -> Set[str]:
        """Get all downstream dependencies of an asset"""
        dependencies = set()
        
        def traverse_downstream(current_asset):
            if current_asset in self.lineage_graph:
                for dependent in self.lineage_graph[current_asset]:
                    if dependent not in dependencies:
                        dependencies.add(dependent)
                        traverse_downstream(dependent)
        
        traverse_downstream(asset_name)
        return dependencies
    
    def get_impact_analysis(self, asset_name: str) -> Dict[str, Any]:
        """Analyze impact of changes to an asset"""
        return {
            'asset': asset_name,
            'upstream_dependencies': list(self.get_upstream_dependencies(asset_name)),
            'downstream_dependencies': list(self.get_downstream_dependencies(asset_name)),
            'transformations_affected': [
                t.transformation_id for t in self.transformations.values()
                if any(inp.name == asset_name for inp in t.inputs) or
                   any(out.name == asset_name for out in t.outputs)
            ]
        }
    
    def export_lineage(self) -> str:
        """Export lineage as JSON"""
        lineage_data = {
            'assets': {name: {
                'name': asset.name,
                'type': asset.asset_type,
                'location': asset.location,
                'schema': asset.schema,
                'metadata': asset.metadata
            } for name, asset in self.assets.items()},
            'transformations': {tid: {
                'id': t.transformation_id,
                'name': t.name,
                'inputs': [inp.name for inp in t.inputs],
                'outputs': [out.name for out in t.outputs],
                'logic': t.transformation_logic,
                'timestamp': t.timestamp.isoformat(),
                'owner': t.owner
            } for tid, t in self.transformations.items()}
        }
        return json.dumps(lineage_data, indent=2)
```

---

---

## 📚 **Study Guide & Key Takeaways**

### 🎯 **Essential Python Concepts for Data Engineering**

#### **Core Language Features**
1. **Object Model**: Everything is an object with identity, type, and value
2. **Memory Management**: Reference counting + garbage collection for cycles
3. **GIL Impact**: Understand when to use threading vs multiprocessing
4. **Decorators**: Function/class modification without changing source code
5. **Context Managers**: Resource management with `__enter__` and `__exit__`
6. **Generators**: Memory-efficient iteration for large datasets

#### **Performance & Optimization**
1. **Profiling First**: Use cProfile, memory_profiler to identify bottlenecks
2. **Data Structures**: Choose appropriate structures (set for membership, dict for lookups)
3. **Built-in Functions**: Leverage optimized C implementations
4. **NumPy**: Vectorized operations for numerical computing
5. **Caching**: Use `@lru_cache` for expensive computations
6. **String Operations**: Use `join()` instead of concatenation

#### **Concurrency Patterns**
1. **Threading**: Good for I/O-bound tasks (GIL released during I/O)
2. **Multiprocessing**: Required for CPU-bound parallelism
3. **Async/Await**: Excellent for concurrent I/O operations
4. **Thread Safety**: Use locks, queues, and thread-safe data structures

#### **Data Engineering Specific**
1. **Large Dataset Processing**: Generators, chunking, streaming approaches
2. **Memory Efficiency**: Avoid loading entire datasets into memory
3. **Error Handling**: Comprehensive exception handling with retries
4. **Data Validation**: Schema enforcement and quality checks
5. **Pipeline Design**: Modular, testable, and monitorable components
6. **Configuration**: Environment-based config management

### 🔧 **Practical Implementation Patterns**

#### **Data Processing Pipeline**
```python
# Key components for production pipelines:
1. Input validation and schema enforcement
2. Error handling with detailed logging
3. Progress monitoring and metrics collection
4. Graceful failure handling and recovery
5. Resource cleanup (connections, files, etc.)
6. Performance monitoring and alerting
```

#### **Performance Optimization Checklist**
```python
# Before optimizing:
1. Profile to identify actual bottlenecks
2. Measure current performance baseline
3. Set specific performance targets
4. Test optimizations with realistic data
5. Monitor production performance
```

### 📊 **Interview Preparation Strategy**

#### **Technical Depth Levels**
1. **Basic**: Syntax, data types, control structures
2. **Intermediate**: OOP, decorators, context managers, error handling
3. **Advanced**: Metaclasses, descriptors, async programming, performance
4. **Expert**: System design, architecture patterns, production concerns

#### **Common Interview Categories**
1. **Language Fundamentals** (20%): Core Python concepts
2. **Data Structures & Algorithms** (25%): Implementation and optimization
3. **System Design** (20%): Scalable architecture patterns
4. **Data Engineering Scenarios** (25%): Real-world problem solving
5. **Code Quality & Testing** (10%): Best practices and methodologies

### 🎓 **Recommended Study Path**

#### **Week 1-2: Fundamentals**
- Python object model and memory management
- Data types, collections, and comprehensions
- Functions, decorators, and context managers
- Error handling and logging

#### **Week 3-4: Advanced Concepts**
- Concurrency: threading, multiprocessing, async/await
- Performance optimization techniques
- Testing strategies and frameworks
- Code quality tools and practices

#### **Week 5-6: Data Engineering Focus**
- Large dataset processing patterns
- Pipeline design and monitoring
- Data validation and quality assurance
- Integration with databases and APIs

#### **Week 7-8: System Design & Practice**
- Scalable architecture patterns
- Production deployment considerations
- Mock interviews and coding challenges
- Real-world project implementation

### 🚀 **Next Steps**

1. **Practice Coding**: Implement the examples in this guide
2. **Build Projects**: Create end-to-end data pipelines
3. **Read Code**: Study open-source Python projects
4. **Join Communities**: Participate in Python and data engineering forums
5. **Stay Updated**: Follow Python enhancement proposals (PEPs)

### 📖 **Additional Resources**

- **Official Documentation**: [python.org](https://docs.python.org/)
- **Performance**: "High Performance Python" by Micha Gorelick
- **Concurrency**: "Effective Python" by Brett Slatkin
- **Data Engineering**: "Designing Data-Intensive Applications" by Martin Kleppmann
- **Testing**: "Test-Driven Development with Python" by Harry Percival

---

**Remember**: The best way to master Python for data engineering is through hands-on practice with real-world datasets and production scenarios. Focus on understanding the underlying concepts rather than memorizing syntax.