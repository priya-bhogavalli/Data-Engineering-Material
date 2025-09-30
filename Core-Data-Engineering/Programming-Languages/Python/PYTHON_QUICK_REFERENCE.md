# Python Quick Reference for Data Engineering

## 📋 Table of Contents

1. [Essential Syntax](#-essential-syntax)
2. [Data Structures](#-data-structures)
3. [Functions & Decorators](#-functions--decorators)
4. [File Operations](#-file-operations)
5. [Database Operations](#-database-operations)
6. [Error Handling](#-error-handling)
7. [Performance Tips](#-performance-tips)
8. [Common Patterns](#-common-patterns)

---

## ⚡ Essential Syntax

### Variables & Types
```python
# Basic types
name: str = "pipeline"
count: int = 1000
rate: float = 0.95
active: bool = True

# Multiple assignment
host, port, db = "localhost", 5432, "analytics"

# Type checking
isinstance(count, int)  # True
type(rate).__name__     # 'float'
```

### String Operations
```python
# F-strings (preferred)
f"Processing {count} records at {rate*100}%"

# String methods
text.strip().lower().split(',')
text.replace('old', 'new')
'_'.join(['a', 'b', 'c'])  # 'a_b_c'
```

### Control Flow
```python
# Conditional
result = "large" if size > 1000 else "small"

# Loops
for i, item in enumerate(items):
    print(f"{i}: {item}")

# List comprehension
squares = [x**2 for x in range(10) if x % 2 == 0]

# Dict comprehension
{k: v.upper() for k, v in data.items() if v}
```

## 📊 Data Structures

### Lists
```python
# Creation & operations
data = [1, 2, 3]
data.append(4)              # [1, 2, 3, 4]
data.extend([5, 6])         # [1, 2, 3, 4, 5, 6]
data.insert(0, 0)           # [0, 1, 2, 3, 4, 5, 6]

# Slicing
data[1:4]      # [1, 2, 3]
data[-2:]      # [5, 6]
data[::2]      # [0, 2, 4, 6]
```

### Dictionaries
```python
# Creation & access
config = {"host": "localhost", "port": 5432}
config.get("timeout", 30)           # Safe access with default
config.setdefault("ssl", True)      # Set if not exists
config.update({"user": "admin"})    # Merge dictionaries

# Iteration
for key, value in config.items():
    print(f"{key}: {value}")
```

### Sets
```python
# Operations
set1 = {1, 2, 3}
set2 = {3, 4, 5}

set1 | set2        # Union: {1, 2, 3, 4, 5}
set1 & set2        # Intersection: {3}
set1 - set2        # Difference: {1, 2}
set1 ^ set2        # Symmetric difference: {1, 2, 4, 5}
```

### Advanced Collections
```python
from collections import defaultdict, Counter, deque

# Auto-initializing dict
dd = defaultdict(list)
dd['key'].append('value')  # No KeyError

# Counting
counter = Counter(['a', 'b', 'a', 'c', 'b', 'a'])
counter.most_common(2)  # [('a', 3), ('b', 2)]

# Efficient queue
queue = deque([1, 2, 3])
queue.appendleft(0)     # [0, 1, 2, 3]
queue.pop()             # 3, queue is [0, 1, 2]
```

## 🔧 Functions & Decorators

### Function Basics
```python
def process_data(data: list, batch_size: int = 1000) -> dict:
    """Process data in batches"""
    return {"processed": len(data), "batches": len(data) // batch_size}

# Lambda functions
square = lambda x: x**2
sorted_data = sorted(data, key=lambda x: x['timestamp'])
```

### Common Decorators
```python
from functools import wraps
import time

# Timing decorator
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__}: {time.time() - start:.4f}s")
        return result
    return wrapper

# Retry decorator
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
                    time.sleep(1)
        return wrapper
    return decorator

# Usage
@timer
@retry(max_attempts=3)
def api_call():
    # Your function here
    pass
```

### Generators
```python
# Generator function
def read_large_file(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip()

# Generator expression
squares = (x**2 for x in range(1000000))  # Memory efficient

# Usage
for line in read_large_file('huge_file.txt'):
    process_line(line)  # Process one line at a time
```

## 📁 File Operations

### Basic File I/O
```python
# Reading files
with open('data.txt', 'r') as f:
    content = f.read()          # Entire file
    lines = f.readlines()       # List of lines
    
    # Line by line (memory efficient)
    for line in f:
        process(line.strip())

# Writing files
with open('output.txt', 'w') as f:
    f.write('Hello World\n')
    f.writelines(['line1\n', 'line2\n'])
```

### JSON Operations
```python
import json

# Read JSON
with open('config.json') as f:
    config = json.load(f)

# Write JSON
with open('output.json', 'w') as f:
    json.dump(data, f, indent=2)

# String operations
json_str = json.dumps(data, indent=2)
data = json.loads(json_str)
```

### CSV Operations
```python
import csv

# Read CSV
with open('data.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['column_name'])

# Write CSV
with open('output.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'name', 'value'])
    writer.writeheader()
    writer.writerows(data)
```

## 🗄️ Database Operations

### SQLite
```python
import sqlite3

with sqlite3.connect('database.db') as conn:
    cursor = conn.cursor()
    
    # Execute query
    cursor.execute("SELECT * FROM users WHERE age > ?", (25,))
    results = cursor.fetchall()
    
    # Insert data
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("John", 30))
    conn.commit()
```

### Using Pandas
```python
import pandas as pd

# Read from database
df = pd.read_sql_query("SELECT * FROM users", connection)

# Write to database
df.to_sql('users', connection, if_exists='append', index=False)

# Basic operations
df.head()                    # First 5 rows
df.info()                    # Data types and info
df.describe()                # Statistical summary
df.groupby('category').sum() # Group and aggregate
```

## ⚠️ Error Handling

### Basic Exception Handling
```python
try:
    result = risky_operation()
except ValueError as e:
    print(f"Value error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
else:
    print("Success!")
finally:
    cleanup()
```

### Custom Exceptions
```python
class DataValidationError(Exception):
    def __init__(self, field, value, message):
        self.field = field
        self.value = value
        super().__init__(f"{field}: {message} (got: {value})")

# Usage
if not isinstance(user_id, int):
    raise DataValidationError('user_id', user_id, 'must be integer')
```

### Context Managers
```python
# File context manager
with open('file.txt') as f:
    data = f.read()  # File automatically closed

# Custom context manager
from contextlib import contextmanager

@contextmanager
def timer_context(name):
    start = time.time()
    print(f"Starting {name}")
    try:
        yield
    finally:
        print(f"{name} took {time.time() - start:.4f}s")

# Usage
with timer_context("data processing"):
    process_data()
```

## 🚀 Performance Tips

### Memory Optimization
```python
# Use generators for large datasets
def process_large_data():
    for item in large_dataset:
        yield transform(item)

# Use __slots__ for memory-efficient classes
class DataPoint:
    __slots__ = ['x', 'y', 'timestamp']
    def __init__(self, x, y, timestamp):
        self.x = x
        self.y = y
        self.timestamp = timestamp
```

### List Operations
```python
# Efficient list operations
# Good: List comprehension
squares = [x**2 for x in range(1000)]

# Better: Generator for large data
squares_gen = (x**2 for x in range(1000000))

# Avoid: Repeated append in loop
# Bad
result = []
for x in data:
    result.append(transform(x))

# Good
result = [transform(x) for x in data]
```

### Dictionary Operations
```python
# Efficient dictionary operations
# Use get() with default
value = config.get('timeout', 30)

# Use setdefault() for initialization
config.setdefault('retries', []).append(attempt)

# Use collections.defaultdict for auto-initialization
from collections import defaultdict
groups = defaultdict(list)
for item in data:
    groups[item.category].append(item)
```

## 🎯 Common Patterns

### Data Processing Pipeline
```python
def create_pipeline(*functions):
    """Create a data processing pipeline"""
    def pipeline(data):
        for func in functions:
            data = func(data)
        return data
    return pipeline

# Usage
process = create_pipeline(
    lambda x: x.strip(),
    lambda x: x.lower(),
    lambda x: x.replace(' ', '_')
)

result = process("  Hello World  ")  # "hello_world"
```

### Batch Processing
```python
def batch_process(items, batch_size=1000):
    """Process items in batches"""
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        yield process_batch(batch)

# Usage
for result in batch_process(large_dataset, batch_size=500):
    save_result(result)
```

### Configuration Management
```python
import os
from dataclasses import dataclass

@dataclass
class Config:
    host: str = os.getenv('DB_HOST', 'localhost')
    port: int = int(os.getenv('DB_PORT', '5432'))
    database: str = os.getenv('DB_NAME', 'analytics')
    
    @classmethod
    def from_env(cls):
        return cls()

# Usage
config = Config.from_env()
```

### Logging Setup
```python
import logging

# Basic logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Usage
logger.info("Processing started")
logger.error("Error occurred", exc_info=True)
```

## 🔗 Quick Links

- **[Python Key Concepts](./PYTHON_KEY_CONCEPTS.md)** - Complete fundamentals
- **[Advanced Data Engineering](./PYTHON_ADVANCED_DATA_ENGINEERING.md)** - Production patterns
- **[Interview Questions](./PYTHON_INTERVIEW_QUESTIONS.md)** - Interview preparation

## 📚 Essential Libraries

```python
# Data processing
import pandas as pd
import numpy as np

# File formats
import json
import csv
import yaml

# Database
import sqlite3
import sqlalchemy

# HTTP requests
import requests

# Date/time
from datetime import datetime, timedelta
import time

# System
import os
import sys
from pathlib import Path

# Collections
from collections import defaultdict, Counter, deque
from typing import List, Dict, Optional, Union
```

## 🔄 Async Patterns

### Async Database Operations
```python
import asyncio
import aiofiles

# Async file processing
async def process_large_file(filename):
    async with aiofiles.open(filename, 'r') as f:
        async for line in f:
            yield line.strip()

# Async batch processing
async def batch_process(items, batch_size=100):
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        await process_batch_async(batch)

# Usage
async def main():
    async for line in process_large_file('data.txt'):
        await process_line(line)

# asyncio.run(main())
```

### Concurrent Processing
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

# I/O bound tasks
async def concurrent_io():
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=4) as executor:
        tasks = [loop.run_in_executor(executor, io_task, data) for data in datasets]
        results = await asyncio.gather(*tasks)
    return results
```

This quick reference covers the most commonly used Python patterns and operations for data engineering tasks.