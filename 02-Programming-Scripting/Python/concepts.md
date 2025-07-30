# Python for Data Engineering - Core Concepts

## Overview
Python is the most popular programming language for data engineering due to its simplicity, extensive libraries, and strong community support.

## Key Concepts

### 1. Data Structures
- **Lists**: Ordered, mutable collections
- **Dictionaries**: Key-value pairs for fast lookups
- **Sets**: Unordered collections of unique elements
- **Tuples**: Immutable ordered collections

### 2. Essential Libraries for Data Engineering

#### Data Manipulation
- **Pandas**: Data analysis and manipulation
- **NumPy**: Numerical computing
- **Polars**: Fast DataFrame library (alternative to Pandas)

#### Database Connectivity
- **SQLAlchemy**: SQL toolkit and ORM
- **psycopg2**: PostgreSQL adapter
- **pymongo**: MongoDB driver

#### Cloud SDKs
- **boto3**: AWS SDK
- **azure-storage-blob**: Azure Blob Storage
- **google-cloud-storage**: GCP Storage

#### Data Processing
- **PySpark**: Apache Spark Python API
- **Dask**: Parallel computing library
- **Ray**: Distributed computing framework

### 3. File Handling
```python
# Reading different file formats
import pandas as pd
import json

# CSV files
df = pd.read_csv('data.csv')

# JSON files
with open('data.json', 'r') as f:
    data = json.load(f)

# Parquet files
df = pd.read_parquet('data.parquet')
```

### 4. Error Handling
```python
try:
    # Risky operation
    result = process_data(data)
except FileNotFoundError:
    print("File not found")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    # Cleanup code
    cleanup_resources()
```

### 5. Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("Processing started")
```

### 6. Configuration Management
```python
import os
from configparser import ConfigParser

# Environment variables
db_host = os.getenv('DB_HOST', 'localhost')

# Config files
config = ConfigParser()
config.read('config.ini')
db_port = config.getint('database', 'port')
```

### 7. Virtual Environments
```bash
# Create virtual environment
python -m venv data_eng_env

# Activate (Windows)
data_eng_env\Scripts\activate

# Activate (Linux/Mac)
source data_eng_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Best Practices

1. **Code Organization**: Use modules and packages
2. **Documentation**: Write clear docstrings
3. **Testing**: Implement unit tests with pytest
4. **Type Hints**: Use type annotations for better code clarity
5. **PEP 8**: Follow Python style guidelines
6. **Virtual Environments**: Isolate project dependencies

## Performance Considerations

- Use list comprehensions over loops when possible
- Leverage NumPy for numerical operations
- Consider Polars for large dataset operations
- Use generators for memory-efficient processing
- Profile code with cProfile for optimization