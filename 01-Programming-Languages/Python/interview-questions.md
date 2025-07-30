# Python Interview Questions for Data Engineering

## Basic Questions

### Q1: What are the key differences between lists and tuples in Python?

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

### Q2: Explain the difference between `==` and `is` operators.

**Answer:**
- `==` compares values (equality)
- `is` compares object identity (same object in memory)

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)  # True (same values)
print(a is b)  # False (different objects)
print(a is c)  # True (same object)
```

### Q3: What is the Global Interpreter Lock (GIL) and how does it affect data processing?

**Answer:**
The GIL is a mutex that prevents multiple native threads from executing Python bytecodes simultaneously. This affects:
- **CPU-bound tasks**: Limited to single-core performance
- **I/O-bound tasks**: Less affected due to GIL release during I/O
- **Solutions**: Use multiprocessing, async/await, or libraries like NumPy that release GIL

## Intermediate Questions

### Q4: How would you handle large datasets that don't fit in memory?

**Answer:**
Several approaches:
1. **Chunking with Pandas**:
```python
chunk_size = 10000
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    process_chunk(chunk)
```

2. **Dask for parallel processing**:
```python
import dask.dataframe as dd
df = dd.read_csv('large_file.csv')
result = df.groupby('column').sum().compute()
```

3. **Generators for memory efficiency**:
```python
def read_large_file(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            yield process_line(line)
```

### Q5: Explain the difference between deep copy and shallow copy.

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

### Q6: Implement a decorator for retry logic in data pipeline operations.

**Answer:**
```python
import time
import functools
from typing import Callable, Any

def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            attempts = 0
            current_delay = delay
            
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    
                    print(f"Attempt {attempts} failed: {e}. Retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff
            
        return wrapper
    return decorator

# Usage
@retry(max_attempts=3, delay=1.0, backoff=2.0)
def fetch_data_from_api():
    # API call that might fail
    pass
```

### Q7: How would you implement a thread-safe singleton pattern for database connections?

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