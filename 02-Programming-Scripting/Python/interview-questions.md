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

### Q6: How do you optimize Python code for data processing?

**Answer:**
1. **Use vectorized operations** (NumPy, Pandas)
2. **List comprehensions** over loops
3. **Built-in functions** (map, filter, reduce)
4. **Caching** with functools.lru_cache
5. **Profile code** with cProfile
6. **Use appropriate data structures**

```python
# Slow
result = []
for item in data:
    if condition(item):
        result.append(transform(item))

# Fast
result = [transform(item) for item in data if condition(item)]
```

## Advanced Questions

### Q7: Implement a decorator for retry logic in data pipeline operations.

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

### Q8: How would you implement a thread-safe singleton pattern for database connections?

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

### Q9: Explain context managers and implement a custom one for database transactions.

**Answer:**
Context managers ensure proper resource management using `__enter__` and `__exit__` methods.

```python
class DatabaseTransaction:
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

# Usage
with DatabaseTransaction(connection) as trans:
    # Database operations
    connection.execute("INSERT INTO table VALUES (...)")
    # Auto-commit on success, rollback on exception
```

### Q10: How would you implement a data validation framework using Python?

**Answer:**
```python
from abc import ABC, abstractmethod
from typing import Any, List, Dict
import pandas as pd

class ValidationRule(ABC):
    @abstractmethod
    def validate(self, data: Any) -> Dict[str, Any]:
        pass

class NotNullRule(ValidationRule):
    def __init__(self, column: str):
        self.column = column
    
    def validate(self, df: pd.DataFrame) -> Dict[str, Any]:
        null_count = df[self.column].isnull().sum()
        return {
            'rule': 'NotNull',
            'column': self.column,
            'passed': null_count == 0,
            'null_count': null_count
        }

class DataValidator:
    def __init__(self):
        self.rules: List[ValidationRule] = []
    
    def add_rule(self, rule: ValidationRule):
        self.rules.append(rule)
    
    def validate(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        results = []
        for rule in self.rules:
            results.append(rule.validate(data))
        return results

# Usage
validator = DataValidator()
validator.add_rule(NotNullRule('customer_id'))
results = validator.validate(df)
```

## Scenario-Based Questions

### Q11: Design a Python solution for processing streaming data from Kafka.

**Answer:**
```python
from kafka import KafkaConsumer
import json
import logging
from typing import Callable

class StreamProcessor:
    def __init__(self, topic: str, bootstrap_servers: List[str]):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self.processors: List[Callable] = []
    
    def add_processor(self, processor: Callable):
        self.processors.append(processor)
    
    def start_processing(self):
        for message in self.consumer:
            try:
                data = message.value
                for processor in self.processors:
                    data = processor(data)
                self.handle_processed_data(data)
            except Exception as e:
                logging.error(f"Processing failed: {e}")
    
    def handle_processed_data(self, data):
        # Send to downstream system
        pass

# Usage
processor = StreamProcessor('user-events', ['localhost:9092'])
processor.add_processor(lambda x: {**x, 'processed_at': time.time()})
processor.start_processing()
```

## Performance & Optimization Questions

### Q12: Compare different methods for reading large CSV files in Python.

**Answer:**
```python
import pandas as pd
import csv
import time

# Method 1: Pandas (convenient but memory-intensive)
df = pd.read_csv('large_file.csv')

# Method 2: Pandas with chunking (memory-efficient)
chunk_size = 10000
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    process_chunk(chunk)

# Method 3: Built-in csv module (fastest for simple operations)
with open('large_file.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        process_row(row)

# Method 4: Dask (parallel processing)
import dask.dataframe as dd
df = dd.read_csv('large_file.csv')
result = df.compute()
```

**Performance comparison:**
- csv module: Fastest for simple operations
- Pandas chunking: Good balance of features and memory usage
- Dask: Best for parallel processing on large datasets
- Regular Pandas: Fastest for small-medium files that fit in memory