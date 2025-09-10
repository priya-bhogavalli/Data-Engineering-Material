# Python 100 Interview Questions for Data Engineering

## Basic Python (Questions 1-20)

### 1. What is the difference between list and tuple?
**Answer:** Lists are mutable, tuples are immutable. Lists use [], tuples use ().

### 2. Explain Python's GIL (Global Interpreter Lock).
**Answer:** GIL prevents multiple threads from executing Python code simultaneously, limiting true parallelism for CPU-bound tasks.

### 3. What are Python decorators?
**Answer:** Functions that modify or extend behavior of other functions without changing their code.
```python
def my_decorator(func):
    def wrapper():
        print("Before")
        func()
        print("After")
    return wrapper
```

### 4. Difference between `==` and `is`?
**Answer:** `==` compares values, `is` compares object identity (memory location).

### 5. What is list comprehension?
**Answer:** Concise way to create lists: `[x*2 for x in range(5)]`

### 6. Explain `*args` and `**kwargs`.
**Answer:** `*args` passes variable number of positional arguments, `**kwargs` passes variable number of keyword arguments.

### 7. What is the difference between `append()` and `extend()`?
**Answer:** `append()` adds single element, `extend()` adds multiple elements from iterable.

### 8. How does Python memory management work?
**Answer:** Uses reference counting and garbage collection for cyclic references.

### 9. What are Python generators?
**Answer:** Functions that yield values one at a time, memory efficient for large datasets.
```python
def my_gen():
    for i in range(1000000):
        yield i
```

### 10. Explain the difference between shallow and deep copy.
**Answer:** Shallow copy creates new object but references to nested objects remain. Deep copy creates completely independent copy.

### 11. What is the `with` statement used for?
**Answer:** Context management, ensures proper resource cleanup (file handling, database connections).

### 12. How do you handle exceptions in Python?
**Answer:** Using try/except blocks:
```python
try:
    risky_operation()
except SpecificError as e:
    handle_error(e)
finally:
    cleanup()
```

### 13. What is the difference between `range()` and `xrange()` in Python 2/3?
**Answer:** Python 2: `range()` returns list, `xrange()` returns iterator. Python 3: only `range()` exists, returns iterator.

### 14. Explain Python's `lambda` functions.
**Answer:** Anonymous functions for simple operations: `lambda x: x*2`

### 15. What is the purpose of `__init__.py`?
**Answer:** Makes directory a Python package, can contain initialization code.

### 16. How do you create a virtual environment?
**Answer:** `python -m venv myenv` then activate with `myenv\Scripts\activate` (Windows) or `source myenv/bin/activate` (Unix).

### 17. What is the difference between `staticmethod` and `classmethod`?
**Answer:** `@staticmethod` doesn't receive class/instance reference. `@classmethod` receives class as first argument.

### 18. Explain Python's duck typing.
**Answer:** "If it walks like a duck and quacks like a duck, it's a duck" - objects are used based on behavior, not type.

### 19. What is the `enumerate()` function?
**Answer:** Returns index and value pairs: `for i, val in enumerate(list):`

### 20. How do you reverse a string in Python?
**Answer:** `string[::-1]` or `''.join(reversed(string))`

## Data Structures & Algorithms (Questions 21-40)

### 21. How do you remove duplicates from a list?
**Answer:** `list(set(my_list))` or `list(dict.fromkeys(my_list))` (preserves order)

### 22. What is the time complexity of dictionary operations?
**Answer:** Average O(1) for get/set/delete, worst case O(n) due to hash collisions.

### 23. How do you sort a dictionary by values?
**Answer:** `sorted(dict.items(), key=lambda x: x[1])`

### 24. Explain the difference between `collections.defaultdict` and regular dict.
**Answer:** `defaultdict` automatically creates missing keys with default values.

### 25. What is `collections.Counter`?
**Answer:** Subclass of dict for counting hashable objects.
```python
from collections import Counter
Counter(['a', 'b', 'a', 'c', 'b', 'a'])  # Counter({'a': 3, 'b': 2, 'c': 1})
```

### 26. How do you implement a stack in Python?
**Answer:** Use list with `append()` and `pop()` methods.

### 27. How do you implement a queue in Python?
**Answer:** Use `collections.deque` with `append()` and `popleft()`.

### 28. What is the difference between `heapq.heappush()` and `heapq.heappushpop()`?
**Answer:** `heappush()` adds element, `heappushpop()` adds element then pops smallest.

### 29. How do you find the intersection of two lists?
**Answer:** `list(set(list1) & set(list2))` or `[x for x in list1 if x in list2]`

### 30. What is binary search and how to implement it?
**Answer:** O(log n) search in sorted array:
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

### 31. How do you flatten a nested list?
**Answer:** 
```python
def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result
```

### 32. What is the difference between `bisect.bisect_left()` and `bisect.bisect_right()`?
**Answer:** `bisect_left()` finds leftmost insertion point, `bisect_right()` finds rightmost insertion point for duplicates.

### 33. How do you implement LRU cache?
**Answer:** Use `functools.lru_cache` decorator or implement with `collections.OrderedDict`.

### 34. What is the time complexity of list operations?
**Answer:** Access: O(1), Insert/Delete at end: O(1), Insert/Delete at beginning: O(n), Search: O(n)

### 35. How do you merge two sorted lists?
**Answer:**
```python
def merge_sorted(list1, list2):
    result = []
    i = j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            result.append(list1[i])
            i += 1
        else:
            result.append(list2[j])
            j += 1
    result.extend(list1[i:])
    result.extend(list2[j:])
    return result
```

### 36. What is `itertools.groupby()`?
**Answer:** Groups consecutive elements by key function:
```python
from itertools import groupby
data = [1, 1, 2, 2, 2, 3]
for key, group in groupby(data):
    print(key, list(group))
```

### 37. How do you find the most frequent element in a list?
**Answer:** `max(set(lst), key=lst.count)` or use `Counter.most_common(1)`

### 38. What is the difference between `sort()` and `sorted()`?
**Answer:** `sort()` modifies list in-place, `sorted()` returns new sorted list.

### 39. How do you implement a circular buffer?
**Answer:** Use `collections.deque` with `maxlen` parameter.

### 40. What is the space complexity of recursive algorithms?
**Answer:** O(n) for call stack depth, where n is recursion depth.
## Data Engineering Libraries (Questions 41-60)

### 41. What is pandas and its key data structures?
**Answer:** Data manipulation library. Key structures: DataFrame (2D) and Series (1D).

### 42. How do you read a CSV file in pandas?
**Answer:** `pd.read_csv('file.csv', sep=',', header=0)`

### 43. What is the difference between `loc` and `iloc` in pandas?
**Answer:** `loc` uses labels/boolean indexing, `iloc` uses integer position indexing.

### 44. How do you handle missing data in pandas?
**Answer:** `dropna()`, `fillna()`, `interpolate()`, or `isna()` to detect.

### 45. What is pandas `groupby()` operation?
**Answer:** Groups data by column values for aggregation:
```python
df.groupby('category').agg({'sales': 'sum', 'quantity': 'mean'})
```

### 46. How do you merge DataFrames in pandas?
**Answer:** `pd.merge()`, `pd.concat()`, or `df.join()` methods.

### 47. What is NumPy and why is it faster than pure Python?
**Answer:** Numerical computing library. Faster due to C implementation and vectorized operations.

### 48. How do you create a NumPy array?
**Answer:** `np.array([1,2,3])`, `np.zeros(5)`, `np.ones((3,3))`, `np.arange(10)`

### 49. What is broadcasting in NumPy?
**Answer:** Automatic element-wise operations on arrays of different shapes.

### 50. How do you reshape a NumPy array?
**Answer:** `arr.reshape(new_shape)` or `np.reshape(arr, new_shape)`

### 51. What is the difference between `copy()` and `view()` in NumPy?
**Answer:** `copy()` creates independent array, `view()` creates new array object sharing same data.

### 52. How do you handle large datasets that don't fit in memory?
**Answer:** Use chunking with `pd.read_csv(chunksize=1000)` or Dask for parallel processing.

### 53. What is Dask and when would you use it?
**Answer:** Parallel computing library for larger-than-memory datasets. Use when pandas becomes too slow/memory-intensive.

### 54. How do you optimize pandas operations?
**Answer:** Use vectorized operations, avoid loops, use categorical data types, optimize dtypes.

### 55. What is the difference between `apply()` and `map()` in pandas?
**Answer:** `apply()` works on Series/DataFrame, `map()` only on Series and maps values.

### 56. How do you pivot data in pandas?
**Answer:** `df.pivot_table()` or `df.pivot()` to reshape data from long to wide format.

### 57. What is `pd.cut()` and `pd.qcut()`?
**Answer:** `cut()` bins data into equal-width intervals, `qcut()` bins into equal-frequency quantiles.

### 58. How do you handle datetime data in pandas?
**Answer:** `pd.to_datetime()`, `dt` accessor for datetime operations, `pd.date_range()` for sequences.

### 59. What is the difference between `merge()` and `join()` in pandas?
**Answer:** `merge()` is more flexible with multiple join keys, `join()` is simpler for index-based joins.

### 60. How do you optimize memory usage in pandas?
**Answer:** Use appropriate dtypes, categorical for strings, downcast numeric types, use `pd.read_csv()` dtype parameter.

## Database & SQL Integration (Questions 61-75)

### 61. How do you connect to a database in Python?
**Answer:** Use database-specific drivers: `psycopg2` for PostgreSQL, `pymongo` for MongoDB, `sqlite3` for SQLite.

### 62. What is SQLAlchemy?
**Answer:** Python SQL toolkit and ORM providing database abstraction layer.

### 63. How do you execute SQL queries in Python?
**Answer:**
```python
import sqlite3
conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()
cursor.execute("SELECT * FROM table")
results = cursor.fetchall()
```

### 64. What is the difference between `fetchone()`, `fetchmany()`, and `fetchall()`?
**Answer:** `fetchone()` returns single row, `fetchmany(n)` returns n rows, `fetchall()` returns all rows.

### 65. How do you handle database transactions in Python?
**Answer:** Use context managers or explicit `commit()`/`rollback()` calls.

### 66. What is connection pooling and why is it important?
**Answer:** Reuses database connections to improve performance and manage resources efficiently.

### 67. How do you prevent SQL injection in Python?
**Answer:** Use parameterized queries: `cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))`

### 68. What is the difference between `psycopg2` and `asyncpg`?
**Answer:** `psycopg2` is synchronous PostgreSQL adapter, `asyncpg` is asynchronous with better performance.

### 69. How do you bulk insert data into a database?
**Answer:** Use `executemany()` or database-specific bulk methods like `copy_from()` in PostgreSQL.

### 70. What is an ORM and its advantages/disadvantages?
**Answer:** Object-Relational Mapping. Advantages: abstraction, security. Disadvantages: performance overhead, complexity.

### 71. How do you handle database migrations in Python?
**Answer:** Use tools like Alembic (SQLAlchemy) or Django migrations.

### 72. What is the difference between ACID and BASE properties?
**Answer:** ACID (Atomicity, Consistency, Isolation, Durability) for RDBMS. BASE (Basically Available, Soft state, Eventual consistency) for NoSQL.

### 73. How do you optimize database queries in Python applications?
**Answer:** Use indexes, query optimization, connection pooling, caching, and avoid N+1 queries.

### 74. What is database sharding?
**Answer:** Horizontal partitioning of data across multiple databases to improve performance and scalability.

### 75. How do you handle database connection errors?
**Answer:** Use try-except blocks, connection retry logic, and proper connection cleanup.

## Big Data & Distributed Computing (Questions 76-90)

### 76. What is Apache Spark and PySpark?
**Answer:** Spark is distributed computing framework, PySpark is Python API for Spark.

### 77. What are RDDs in Spark?
**Answer:** Resilient Distributed Datasets - immutable distributed collections with fault tolerance.

### 78. What is the difference between RDD and DataFrame in Spark?
**Answer:** DataFrames have schema and optimizations (Catalyst optimizer), RDDs are lower-level.

### 79. What are Spark transformations vs actions?
**Answer:** Transformations are lazy (map, filter), actions trigger execution (collect, count).

### 80. How do you handle large files in Python?
**Answer:** Read in chunks, use generators, stream processing, or distributed computing frameworks.

### 81. What is data partitioning in distributed systems?
**Answer:** Dividing data across multiple nodes for parallel processing and improved performance.

### 82. How do you optimize Spark jobs?
**Answer:** Proper partitioning, caching, avoiding shuffles, using broadcast variables, tuning parallelism.

### 83. What is the difference between `map()` and `flatMap()` in Spark?
**Answer:** `map()` returns one element per input, `flatMap()` can return multiple elements (flattens).

### 84. How do you handle skewed data in Spark?
**Answer:** Salting keys, custom partitioning, broadcast joins for small tables.

### 85. What is Spark SQL?
**Answer:** Module for structured data processing using SQL queries on DataFrames.

### 86. How do you read different file formats in Spark?
**Answer:** `spark.read.csv()`, `spark.read.json()`, `spark.read.parquet()`, etc.

### 87. What is the difference between `cache()` and `persist()` in Spark?
**Answer:** `cache()` stores in memory, `persist()` allows choosing storage level (memory, disk, etc.).

### 88. How do you handle streaming data in Python?
**Answer:** Use Apache Kafka with `kafka-python`, Spark Streaming, or Apache Flink.

### 89. What is Apache Kafka and how do you use it with Python?
**Answer:** Distributed streaming platform. Use `kafka-python` library for producers/consumers.

### 90. How do you monitor and debug distributed Python applications?
**Answer:** Use logging, metrics collection, distributed tracing, and monitoring tools like Spark UI.

## Performance & Optimization (Questions 91-100)

### 91. How do you profile Python code?
**Answer:** Use `cProfile`, `line_profiler`, `memory_profiler`, or `py-spy` for production.

### 92. What is the difference between multiprocessing and multithreading?
**Answer:** Multiprocessing uses separate processes (CPU-bound), multithreading uses threads (I/O-bound, limited by GIL).

### 93. How do you implement caching in Python?
**Answer:** Use `functools.lru_cache`, Redis, Memcached, or custom caching solutions.

### 94. What is asyncio and when to use it?
**Answer:** Asynchronous I/O framework for concurrent programming, best for I/O-bound tasks.

### 95. How do you optimize memory usage in Python?
**Answer:** Use generators, `__slots__`, appropriate data types, memory profiling, and garbage collection tuning.

### 96. What is the difference between `concurrent.futures` and `asyncio`?
**Answer:** `concurrent.futures` for parallel execution, `asyncio` for concurrent I/O operations.

### 97. How do you handle CPU-intensive tasks in Python?
**Answer:** Use multiprocessing, Cython, NumPy vectorization, or external libraries like Numba.

### 98. What is JIT compilation and how does Numba work?
**Answer:** Just-In-Time compilation translates Python to machine code. Numba uses LLVM for numerical functions.

### 99. How do you optimize pandas operations for large datasets?
**Answer:** Use chunking, appropriate dtypes, vectorized operations, and consider alternatives like Polars or Dask.

### 100. What are best practices for Python code optimization?
**Answer:** Profile first, use built-in functions, avoid premature optimization, choose right algorithms, use appropriate data structures.