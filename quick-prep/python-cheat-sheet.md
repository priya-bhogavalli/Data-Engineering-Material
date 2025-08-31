# 🐍 Python Cheat Sheet for Data Engineering

## 📊 **Data Structures**
```python
# Lists - ordered, mutable
data = [1, 2, 3]
data.append(4)

# Dicts - key-value pairs
config = {'host': 'localhost', 'port': 5432}

# Sets - unique values
unique_ids = {1, 2, 3}

# List comprehension
squares = [x**2 for x in range(10) if x % 2 == 0]
```

## 📁 **File Operations**
```python
# Read CSV
import pandas as pd
df = pd.read_csv('data.csv')

# Read JSON
import json
with open('config.json', 'r') as f:
    config = json.load(f)

# Write to file
with open('output.txt', 'w') as f:
    f.write('Hello World')
```

## 🔄 **Common Pandas Operations**
```python
# Basic operations
df.head()                    # First 5 rows
df.info()                    # Data types & null counts
df.describe()                # Summary statistics
df.groupby('column').sum()   # Group and aggregate
df.merge(df2, on='key')      # Join dataframes
df.drop_duplicates()         # Remove duplicates
```

## 🔌 **Database Connections**
```python
import psycopg2
import pandas as pd

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    database="mydb",
    user="user",
    password="password"
)

# Execute query
df = pd.read_sql("SELECT * FROM table", conn)
```

## ⚡ **Performance Tips**
- Use `iterrows()` sparingly - vectorized operations are faster
- Use `pd.read_csv(chunksize=1000)` for large files
- Use `df.query()` instead of boolean indexing for readability