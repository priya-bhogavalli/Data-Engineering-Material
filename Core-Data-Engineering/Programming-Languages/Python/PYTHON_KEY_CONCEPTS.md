# Python for Data Engineering - Key Concepts

## 🎯 What is Python in Data Engineering?
Python is the primary programming language for data engineering, used for building ETL pipelines, data processing, and automation.

## 🔑 Core Concepts

### 1. Data Structures
```python
# Lists - ordered, mutable collections
data = [1, 2, 3, 4, 5]
processed = [x * 2 for x in data if x > 2]  # [6, 8, 10]

# Dictionaries - key-value pairs for configuration
config = {
    'host': 'localhost',
    'port': 5432,
    'batch_size': 1000
}

# Sets - unique collections for deduplication
unique_ids = set([1, 2, 2, 3, 3])  # {1, 2, 3}
```

### 2. Functions and Error Handling
```python
def process_data(data, transform_func):
    """Process data with error handling"""
    try:
        return [transform_func(item) for item in data]
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        return []

# Decorator for logging
def log_execution(func):
    def wrapper(*args, **kwargs):
        logger.info(f"Executing {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

### 3. File and Database Operations
```python
import pandas as pd
import sqlalchemy as sa

# Read data
df = pd.read_csv('data.csv')
df = pd.read_sql('SELECT * FROM table', connection)

# Write data
df.to_csv('output.csv', index=False)
df.to_sql('table_name', connection, if_exists='append')
```

### 4. Configuration Management
```python
import os
from dataclasses import dataclass

@dataclass
class Config:
    db_host: str = os.getenv('DB_HOST', 'localhost')
    db_port: int = int(os.getenv('DB_PORT', '5432'))
    batch_size: int = int(os.getenv('BATCH_SIZE', '1000'))
```

## 🛠️ Essential Libraries

### Data Processing
- **pandas**: DataFrames and data manipulation
- **numpy**: Numerical operations
- **dask**: Parallel computing for large datasets

### Database Connectivity
- **sqlalchemy**: Database ORM and connections
- **psycopg2**: PostgreSQL driver
- **pymongo**: MongoDB driver

### API Development
- **fastapi**: Modern web framework
- **requests**: HTTP client library

### Cloud Integration
- **boto3**: AWS SDK
- **azure-sdk**: Azure services
- **google-cloud**: GCP services

## 🚀 Common Patterns

### ETL Pipeline Structure
```python
def etl_pipeline():
    # Extract
    data = extract_from_source()
    
    # Transform
    cleaned_data = transform_data(data)
    
    # Load
    load_to_destination(cleaned_data)
```

### Batch Processing
```python
def process_in_batches(data, batch_size=1000):
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        process_batch(batch)
```

### Configuration-Driven Processing
```python
def run_pipeline(config):
    source = get_data_source(config['source'])
    processors = [get_processor(p) for p in config['processors']]
    destination = get_destination(config['destination'])
    
    data = source.extract()
    for processor in processors:
        data = processor.transform(data)
    destination.load(data)
```

## 📊 When to Use Python
- **ETL/ELT pipelines**: Data extraction, transformation, loading
- **Data APIs**: RESTful services for data access
- **Automation**: Scheduled data processing jobs
- **Cloud integration**: AWS, Azure, GCP service automation
- **Real-time processing**: Stream processing with Kafka

## 🎯 Interview Focus Areas
1. **Data structures**: Lists, dicts, sets usage
2. **Error handling**: Try/except, logging patterns
3. **File operations**: CSV, JSON, Parquet processing
4. **Database connections**: SQLAlchemy, connection pooling
5. **Performance**: Memory management, batch processing
6. **Testing**: Unit tests, mocking, fixtures

## 📚 Quick References
- [Python Official Docs](https://docs.python.org/)
- [pandas Documentation](https://pandas.pydata.org/docs/)
- [SQLAlchemy Guide](https://docs.sqlalchemy.org/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)