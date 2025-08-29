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

# Tuple example
my_tuple = (1, 2, 3)
# my_tuple.append(4)  # Error - tuples are immutable
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
print(sys.getsizeof(squares_list))  # ~200 bytes
print(sys.getsizeof(squares_gen))   # ~88 bytes
```

## Intermediate Questions

### 6. What are decorators and how do they work?
**Answer:**
Decorators are functions that modify or extend other functions without changing their code.
```python
def timing_decorator(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timing_decorator
def slow_function():
    time.sleep(1)
    return "Done"
```

### 7. Explain the difference between `*args` and `**kwargs`.
**Answer:**
```python
def example_function(*args, **kwargs):
    print("args:", args)      # Tuple of positional arguments
    print("kwargs:", kwargs)  # Dictionary of keyword arguments

example_function(1, 2, 3, name="John", age=30)
# args: (1, 2, 3)
# kwargs: {'name': 'John', 'age': 30}
```

### 8. What is the Global Interpreter Lock (GIL)?
**Answer:**
- **Definition**: Mutex that prevents multiple threads from executing Python code simultaneously
- **Impact**: Limits true parallelism in CPU-bound tasks
- **Workarounds**: Use multiprocessing, async/await, or C extensions
- **Why it exists**: Simplifies memory management and prevents race conditions

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
d.method()  # Prints "B"
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
print(shallow)  # [['X', 2, 3], [4, 5, 6]] - affected
print(deep)     # [[1, 2, 3], [4, 5, 6]] - not affected
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
```python
# Built-in context manager
with open('file.txt', 'r') as f:
    content = f.read()
# File automatically closed

# Custom context manager
class DatabaseConnection:
    def __enter__(self):
        print("Connecting to database")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing database connection")
        if exc_type:
            print(f"Exception occurred: {exc_val}")
        return False  # Don't suppress exceptions

# Using contextlib
from contextlib import contextmanager

@contextmanager
def timer():
    import time
    start = time.time()
    try:
        yield
    finally:
        print(f"Elapsed: {time.time() - start:.4f}s")
```

### 13. How would you implement a thread-safe singleton pattern for database connections?
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
cProfile.run('your_function()')

# 4. Use appropriate data structures
# Use set for O(1) membership testing
large_set = set(range(1000000))
if 500000 in large_set:  # O(1) average case
    pass

# Use dict for O(1) lookups
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
```python
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.order = []
    
    def get(self, key):
        if key in self.cache:
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return -1
    
    def put(self, key, value):
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest = self.order.pop(0)
            del self.cache[oldest]
        
        self.cache[key] = value
        self.order.append(key)
```

### 20. Write a function to find the most frequent elements in a large dataset.
**Answer:**
```python
from collections import Counter
import heapq

def top_k_frequent(data, k):
    # Method 1: Using Counter
    counter = Counter(data)
    return counter.most_common(k)

def top_k_frequent_heap(data, k):
    # Method 2: Using heap for memory efficiency
    counter = Counter(data)
    return heapq.nlargest(k, counter.items(), key=lambda x: x[1])

def top_k_frequent_streaming(data_stream, k, window_size=1000):
    # Method 3: For streaming data
    window = []
    counter = Counter()
    
    for item in data_stream:
        window.append(item)
        counter[item] += 1
        
        if len(window) > window_size:
            old_item = window.pop(0)
            counter[old_item] -= 1
            if counter[old_item] == 0:
                del counter[old_item]
        
        if len(window) % 100 == 0:  # Update every 100 items
            yield counter.most_common(k)
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