# Python Advanced Data Engineering Concepts

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Environment & Package Management](#-environment--package-management)
3. [Data Validation & Schema Management](#-data-validation--schema-management)
4. [Configuration Management](#-configuration-management)
5. [Logging & Monitoring](#-logging--monitoring)
6. [Data Pipeline Patterns](#-data-pipeline-patterns)
7. [Memory Optimization](#-memory-optimization)
8. [Security Best Practices](#-security-best-practices)
9. [Design Patterns for Data Engineering](#-design-patterns-for-data-engineering)
10. [Performance Optimization](#-performance-optimization)
11. [Big Data Integration](#-big-data-integration)

---

## 🎯 Overview

This document covers advanced Python concepts specifically for data engineering, including production-ready patterns, optimization techniques, and integration with big data ecosystems.

**Prerequisites:** Complete [Python Key Concepts](./PYTHON_KEY_CONCEPTS.md) first for foundational knowledge.

## 📚 Related Documents

- **[Python Key Concepts](./PYTHON_KEY_CONCEPTS.md)** - Fundamental Python concepts and theory
- **[Python Quick Reference](./PYTHON_QUICK_REFERENCE.md)** - Quick syntax and patterns reference
- **[Python Interview Questions](./PYTHON_INTERVIEW_QUESTIONS.md)** - Interview preparation

## 🐍 Environment & Package Management

### Virtual Environments

```python
# Create and manage virtual environments
import venv
import subprocess
import sys

def create_virtual_env(env_name: str):
    """Create a virtual environment"""
    venv.create(env_name, with_pip=True)
    print(f"Virtual environment '{env_name}' created")

# Command line usage:
# python -m venv data_pipeline_env
# source data_pipeline_env/bin/activate  # Linux/Mac
# data_pipeline_env\Scripts\activate     # Windows

# Install packages
# pip install pandas numpy sqlalchemy
```

### Requirements Management

```python
# requirements.txt example
"""
pandas==2.1.0
numpy==1.24.3
sqlalchemy==2.0.20
pydantic==2.3.0
python-dotenv==1.0.0
"""

# requirements-dev.txt for development
"""
-r requirements.txt
pytest==7.4.0
black==23.7.0
mypy==1.5.1
"""

# Install from requirements
# pip install -r requirements.txt
```

### Package Structure

```python
# data_pipeline/
# ├── __init__.py
# ├── config/
# │   ├── __init__.py
# │   └── settings.py
# ├── extractors/
# │   ├── __init__.py
# │   └── database.py
# ├── transformers/
# │   ├── __init__.py
# │   └── cleaner.py
# └── loaders/
#     ├── __init__.py
#     └── warehouse.py

# __init__.py
__version__ = "1.0.0"
__author__ = "Data Engineering Team"

from .config import settings
from .extractors import DatabaseExtractor
from .transformers import DataCleaner
from .loaders import WarehouseLoader

__all__ = ["settings", "DatabaseExtractor", "DataCleaner", "WarehouseLoader"]
```

## ✅ Data Validation & Schema Management

### Pydantic Models

```python
from pydantic import BaseModel, validator, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class DataSource(str, Enum):
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    MONGODB = "mongodb"
    S3 = "s3"

class UserEvent(BaseModel):
    user_id: int = Field(..., gt=0, description="User ID must be positive")
    event_type: str = Field(..., min_length=1, max_length=50)
    timestamp: datetime
    properties: Optional[dict] = None
    source: DataSource
    
    @validator('event_type')
    def validate_event_type(cls, v):
        allowed_events = ['login', 'logout', 'purchase', 'view', 'click']
        if v not in allowed_events:
            raise ValueError(f'Event type must be one of {allowed_events}')
        return v
    
    @validator('properties')
    def validate_properties(cls, v):
        if v and len(v) > 10:
            raise ValueError('Properties cannot have more than 10 keys')
        return v

# Usage
try:
    event = UserEvent(
        user_id=123,
        event_type="login",
        timestamp=datetime.now(),
        properties={"ip": "192.168.1.1"},
        source=DataSource.POSTGRESQL
    )
    print(f"Valid event: {event}")
    # Output: Valid event: user_id=123 event_type='login' timestamp=...
except Exception as e:
    print(f"Validation error: {e}")
```

### Schema Evolution

```python
from pydantic import BaseModel
from typing import Union

class UserEventV1(BaseModel):
    user_id: int
    event_type: str
    timestamp: datetime

class UserEventV2(BaseModel):
    user_id: int
    event_type: str
    timestamp: datetime
    session_id: Optional[str] = None  # New field
    
    class Config:
        # Allow extra fields for backward compatibility
        extra = "allow"

def migrate_event_schema(event_data: dict) -> UserEventV2:
    """Migrate old schema to new schema"""
    # Handle missing fields
    if 'session_id' not in event_data:
        event_data['session_id'] = None
    
    return UserEventV2(**event_data)

# Usage
old_event = {"user_id": 123, "event_type": "login", "timestamp": datetime.now()}
new_event = migrate_event_schema(old_event)
print(f"Migrated event: {new_event}")
# Output: Migrated event: user_id=123 event_type='login' ... session_id=None
```

## ⚙️ Configuration Management

### Environment-Based Configuration

```python
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class DatabaseConfig:
    host: str
    port: int
    database: str
    username: str
    password: str
    ssl_mode: str = "require"
    
    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        return cls(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            database=os.getenv("DB_NAME", "analytics"),
            username=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", ""),
            ssl_mode=os.getenv("DB_SSL_MODE", "require")
        )

@dataclass
class AppConfig:
    environment: str
    debug: bool
    batch_size: int
    max_workers: int
    database: DatabaseConfig
    
    @classmethod
    def load(cls) -> 'AppConfig':
        env = os.getenv("ENVIRONMENT", "development")
        return cls(
            environment=env,
            debug=env == "development",
            batch_size=int(os.getenv("BATCH_SIZE", "1000")),
            max_workers=int(os.getenv("MAX_WORKERS", "4")),
            database=DatabaseConfig.from_env()
        )

# Usage
config = AppConfig.load()
print(f"Environment: {config.environment}")
print(f"Database: {config.database.host}:{config.database.port}")
# Output: Environment: development
# Output: Database: localhost:5432
```

### Configuration Files

```python
import yaml
import json
from pathlib import Path

class ConfigManager:
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.configs = {}
    
    def load_yaml(self, filename: str) -> dict:
        """Load YAML configuration file"""
        file_path = self.config_dir / filename
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            self.configs[filename] = config
            return config
    
    def load_json(self, filename: str) -> dict:
        """Load JSON configuration file"""
        file_path = self.config_dir / filename
        with open(file_path, 'r') as file:
            config = json.load(file)
            self.configs[filename] = config
            return config
    
    def get_config(self, filename: str) -> dict:
        """Get cached configuration"""
        return self.configs.get(filename, {})

# config/database.yaml
"""
development:
  host: localhost
  port: 5432
  database: dev_analytics
  
production:
  host: prod-db.company.com
  port: 5432
  database: analytics
"""

# Usage
config_manager = ConfigManager()
db_config = config_manager.load_yaml("database.yaml")
env = os.getenv("ENVIRONMENT", "development")
db_settings = db_config[env]
print(f"Database settings: {db_settings}")
# Output: Database settings: {'host': 'localhost', 'port': 5432, 'database': 'dev_analytics'}
```

## 📊 Logging & Monitoring

### Structured Logging

```python
import logging
import json
from datetime import datetime
from typing import Dict, Any

class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured JSON logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add extra fields if present
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'job_id'):
            log_entry['job_id'] = record.job_id
            
        return json.dumps(log_entry)

def setup_logging(log_level: str = "INFO"):
    """Setup structured logging"""
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(StructuredFormatter())
    logger.addHandler(console_handler)
    
    # File handler
    file_handler = logging.FileHandler("pipeline.log")
    file_handler.setFormatter(StructuredFormatter())
    logger.addHandler(file_handler)

# Usage
setup_logging()
logger = logging.getLogger(__name__)

def process_user_data(user_id: int, data: dict):
    logger.info("Processing user data", extra={"user_id": user_id})
    try:
        # Process data
        result = len(data)
        logger.info("Data processed successfully", 
                   extra={"user_id": user_id, "record_count": result})
        return result
    except Exception as e:
        logger.error("Failed to process data", 
                    extra={"user_id": user_id, "error": str(e)})
        raise

# Test
process_user_data(123, {"name": "John", "age": 30})
# Output: {"timestamp": "2024-01-01T10:00:00.000000", "level": "INFO", ...}
```

### Performance Monitoring

```python
import time
import psutil
from functools import wraps
from typing import Callable

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
    
    def track_execution_time(self, func_name: str = None):
        """Decorator to track function execution time"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                
                try:
                    result = func(*args, **kwargs)
                    status = "success"
                except Exception as e:
                    result = None
                    status = "error"
                    raise
                finally:
                    end_time = time.time()
                    end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                    
                    metrics = {
                        "execution_time": end_time - start_time,
                        "memory_used": end_memory - start_memory,
                        "status": status,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    name = func_name or func.__name__
                    self.metrics[name] = metrics
                    
                    logger.info(f"Function {name} metrics", extra=metrics)
                
                return result
            return wrapper
        return decorator
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all collected metrics"""
        return self.metrics

# Usage
monitor = PerformanceMonitor()

@monitor.track_execution_time("data_processing")
def process_large_dataset(size: int):
    # Simulate processing
    data = list(range(size))
    return sum(x * x for x in data)

result = process_large_dataset(1000000)
print(f"Result: {result}")
print(f"Metrics: {monitor.get_metrics()}")
# Output: Result: 333332833333500000
# Output: Metrics: {'data_processing': {'execution_time': 0.123, 'memory_used': 45.2, ...}}
```

## 🔄 Data Pipeline Patterns

### ETL Pipeline Pattern

```python
from abc import ABC, abstractmethod
from typing import Any, List, Dict
import pandas as pd

class DataExtractor(ABC):
    @abstractmethod
    def extract(self) -> Any:
        pass

class DataTransformer(ABC):
    @abstractmethod
    def transform(self, data: Any) -> Any:
        pass

class DataLoader(ABC):
    @abstractmethod
    def load(self, data: Any) -> None:
        pass

class CSVExtractor(DataExtractor):
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def extract(self) -> pd.DataFrame:
        print(f"Extracting data from {self.file_path}")
        # Simulate CSV reading
        data = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35]
        })
        print(f"Extracted {len(data)} records")
        return data

class DataCleaner(DataTransformer):
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        print("Cleaning data...")
        # Remove duplicates
        cleaned = data.drop_duplicates()
        # Fill missing values
        cleaned = cleaned.fillna(0)
        print(f"Cleaned data: {len(cleaned)} records")
        return cleaned

class DatabaseLoader(DataLoader):
    def __init__(self, table_name: str):
        self.table_name = table_name
    
    def load(self, data: pd.DataFrame) -> None:
        print(f"Loading {len(data)} records to {self.table_name}")
        # Simulate database loading
        print("Data loaded successfully")

class ETLPipeline:
    def __init__(self, extractor: DataExtractor, 
                 transformer: DataTransformer, 
                 loader: DataLoader):
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader
    
    def run(self):
        """Execute the ETL pipeline"""
        print("Starting ETL pipeline...")
        
        # Extract
        raw_data = self.extractor.extract()
        
        # Transform
        clean_data = self.transformer.transform(raw_data)
        
        # Load
        self.loader.load(clean_data)
        
        print("ETL pipeline completed")

# Usage
pipeline = ETLPipeline(
    extractor=CSVExtractor("users.csv"),
    transformer=DataCleaner(),
    loader=DatabaseLoader("users_clean")
)

pipeline.run()
# Output: Starting ETL pipeline...
# Output: Extracting data from users.csv
# Output: Extracted 3 records
# Output: Cleaning data...
# Output: Cleaned data: 3 records
# Output: Loading 3 records to users_clean
# Output: Data loaded successfully
# Output: ETL pipeline completed
```

### Streaming Pipeline Pattern

```python
import asyncio
from asyncio import Queue
from typing import AsyncGenerator

class StreamProcessor:
    def __init__(self, batch_size: int = 100):
        self.batch_size = batch_size
        self.queue = Queue()
    
    async def produce_data(self) -> AsyncGenerator[dict, None]:
        """Simulate data stream"""
        for i in range(1000):
            yield {"id": i, "value": i * 2, "timestamp": time.time()}
            await asyncio.sleep(0.01)  # Simulate real-time data
    
    async def process_batch(self, batch: List[dict]):
        """Process a batch of data"""
        print(f"Processing batch of {len(batch)} items")
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        # Transform data
        processed = [{"id": item["id"], "doubled_value": item["value"] * 2} 
                    for item in batch]
        return processed
    
    async def run_stream_processing(self):
        """Run streaming data processing"""
        batch = []
        
        async for data_item in self.produce_data():
            batch.append(data_item)
            
            if len(batch) >= self.batch_size:
                processed_batch = await self.process_batch(batch)
                print(f"Processed batch: first item ID {processed_batch[0]['id']}")
                batch = []
        
        # Process remaining items
        if batch:
            processed_batch = await self.process_batch(batch)
            print(f"Processed final batch: {len(processed_batch)} items")

# Usage
async def main():
    processor = StreamProcessor(batch_size=50)
    await processor.run_stream_processing()

# asyncio.run(main())
print("Stream processing example ready")
# Output: Stream processing example ready
```

## 🚀 Memory Optimization

### Memory-Efficient Data Processing

```python
import sys
from typing import Iterator, Generator

class MemoryOptimizedProcessor:
    
    @staticmethod
    def process_large_file_generator(file_path: str) -> Generator[dict, None, None]:
        """Process large files using generators"""
        # Simulate file reading line by line
        for i in range(1000000):  # Simulate 1M records
            yield {"id": i, "data": f"record_{i}"}
    
    @staticmethod
    def batch_processor(data_generator: Generator, batch_size: int = 1000) -> Iterator[List[dict]]:
        """Process data in batches to control memory usage"""
        batch = []
        for item in data_generator:
            batch.append(item)
            if len(batch) >= batch_size:
                yield batch
                batch = []
        
        if batch:  # Process remaining items
            yield batch
    
    def process_with_memory_tracking(self, data_source: str):
        """Process data while tracking memory usage"""
        import tracemalloc
        
        tracemalloc.start()
        
        data_gen = self.process_large_file_generator(data_source)
        processed_count = 0
        
        for batch in self.batch_processor(data_gen, batch_size=5000):
            # Process batch
            processed_batch = [{"id": item["id"], "processed": True} for item in batch]
            processed_count += len(processed_batch)
            
            # Track memory every 10 batches
            if processed_count % 50000 == 0:
                current, peak = tracemalloc.get_traced_memory()
                print(f"Processed {processed_count} records")
                print(f"Current memory: {current / 1024 / 1024:.2f} MB")
                print(f"Peak memory: {peak / 1024 / 1024:.2f} MB")
        
        tracemalloc.stop()
        return processed_count

# Usage
processor = MemoryOptimizedProcessor()
total_processed = processor.process_with_memory_tracking("large_file.csv")
print(f"Total processed: {total_processed}")
# Output: Processed 50000 records
# Output: Current memory: 12.45 MB
# Output: Peak memory: 15.23 MB
# Output: ... (continues for all batches)
# Output: Total processed: 1000000
```

### Object Pooling

```python
from typing import List, Optional
import threading

class DatabaseConnection:
    def __init__(self, connection_id: int):
        self.connection_id = connection_id
        self.in_use = False
        print(f"Created connection {connection_id}")
    
    def execute_query(self, query: str):
        print(f"Connection {self.connection_id} executing: {query}")
        return f"Result from connection {self.connection_id}"
    
    def close(self):
        print(f"Closed connection {self.connection_id}")

class ConnectionPool:
    def __init__(self, pool_size: int = 5):
        self.pool_size = pool_size
        self.connections: List[DatabaseConnection] = []
        self.lock = threading.Lock()
        
        # Initialize pool
        for i in range(pool_size):
            self.connections.append(DatabaseConnection(i))
    
    def get_connection(self) -> Optional[DatabaseConnection]:
        """Get an available connection from pool"""
        with self.lock:
            for conn in self.connections:
                if not conn.in_use:
                    conn.in_use = True
                    print(f"Retrieved connection {conn.connection_id} from pool")
                    return conn
            
            print("No available connections in pool")
            return None
    
    def return_connection(self, connection: DatabaseConnection):
        """Return connection to pool"""
        with self.lock:
            connection.in_use = False
            print(f"Returned connection {connection.connection_id} to pool")
    
    def close_all(self):
        """Close all connections"""
        for conn in self.connections:
            conn.close()

# Usage
pool = ConnectionPool(pool_size=3)

# Get connections
conn1 = pool.get_connection()
conn2 = pool.get_connection()

if conn1:
    result1 = conn1.execute_query("SELECT * FROM users")
    print(f"Query result: {result1}")

if conn2:
    result2 = conn2.execute_query("SELECT * FROM orders")
    print(f"Query result: {result2}")

# Return connections
if conn1:
    pool.return_connection(conn1)
if conn2:
    pool.return_connection(conn2)

pool.close_all()

# Output: Created connection 0
# Output: Created connection 1
# Output: Created connection 2
# Output: Retrieved connection 0 from pool
# Output: Retrieved connection 1 from pool
# Output: Connection 0 executing: SELECT * FROM users
# Output: Query result: Result from connection 0
# Output: Connection 1 executing: SELECT * FROM orders
# Output: Query result: Result from connection 1
# Output: Returned connection 0 to pool
# Output: Returned connection 1 to pool
# Output: Closed connection 0
# Output: Closed connection 1
# Output: Closed connection 2
```

## 🔒 Security Best Practices

### Input Validation & Sanitization

```python
import re
import html
from typing import Any, Dict

class DataValidator:
    
    @staticmethod
    def validate_sql_input(input_string: str) -> str:
        """Validate and sanitize SQL input to prevent injection"""
        if not isinstance(input_string, str):
            raise ValueError("Input must be a string")
        
        # Remove dangerous SQL keywords
        dangerous_patterns = [
            r'\b(DROP|DELETE|INSERT|UPDATE|ALTER|CREATE)\b',
            r'[;\'"\\]',
            r'--',
            r'/\*.*?\*/'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, input_string, re.IGNORECASE):
                raise ValueError(f"Potentially dangerous SQL pattern detected: {pattern}")
        
        return input_string.strip()
    
    @staticmethod
    def sanitize_html_input(input_string: str) -> str:
        """Sanitize HTML input"""
        return html.escape(input_string)
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_data_types(data: Dict[str, Any], schema: Dict[str, type]) -> Dict[str, Any]:
        """Validate data types against schema"""
        validated_data = {}
        
        for field, expected_type in schema.items():
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
            
            value = data[field]
            if not isinstance(value, expected_type):
                try:
                    # Try to convert
                    validated_data[field] = expected_type(value)
                except (ValueError, TypeError):
                    raise ValueError(f"Field {field} must be of type {expected_type.__name__}")
            else:
                validated_data[field] = value
        
        return validated_data

# Usage
validator = DataValidator()

# SQL validation
try:
    safe_input = validator.validate_sql_input("user_name")
    print(f"Safe SQL input: {safe_input}")
    # Output: Safe SQL input: user_name
    
    dangerous_input = validator.validate_sql_input("'; DROP TABLE users; --")
except ValueError as e:
    print(f"Validation error: {e}")
    # Output: Validation error: Potentially dangerous SQL pattern detected: [;\'"\\]

# Data type validation
user_data = {"id": "123", "name": "John", "age": "30"}
schema = {"id": int, "name": str, "age": int}

try:
    validated = validator.validate_data_types(user_data, schema)
    print(f"Validated data: {validated}")
    # Output: Validated data: {'id': 123, 'name': 'John', 'age': 30}
except ValueError as e:
    print(f"Validation error: {e}")
```

### Secure Credential Management

```python
import os
import base64
from cryptography.fernet import Fernet
from typing import Dict, Optional

class SecureCredentialManager:
    def __init__(self, key: Optional[bytes] = None):
        if key is None:
            # Generate a new key (store this securely!)
            key = Fernet.generate_key()
        self.cipher = Fernet(key)
        self.key = key
    
    def encrypt_credential(self, credential: str) -> str:
        """Encrypt a credential"""
        encrypted = self.cipher.encrypt(credential.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt_credential(self, encrypted_credential: str) -> str:
        """Decrypt a credential"""
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_credential.encode())
        decrypted = self.cipher.decrypt(encrypted_bytes)
        return decrypted.decode()
    
    def get_database_config(self) -> Dict[str, str]:
        """Get database configuration with decrypted credentials"""
        # In production, these would be stored encrypted
        encrypted_password = os.getenv("DB_PASSWORD_ENCRYPTED")
        
        if encrypted_password:
            password = self.decrypt_credential(encrypted_password)
        else:
            password = os.getenv("DB_PASSWORD", "")
        
        return {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "5432"),
            "database": os.getenv("DB_NAME", "analytics"),
            "username": os.getenv("DB_USER", "postgres"),
            "password": password
        }

# Usage
# Generate and store key securely (one time setup)
key = Fernet.generate_key()
print(f"Encryption key (store securely): {key.decode()}")

credential_manager = SecureCredentialManager(key)

# Encrypt password
password = "super_secret_password"
encrypted_password = credential_manager.encrypt_credential(password)
print(f"Encrypted password: {encrypted_password}")

# Decrypt password
decrypted_password = credential_manager.decrypt_credential(encrypted_password)
print(f"Decrypted password: {decrypted_password}")

# Output: Encryption key (store securely): [base64 encoded key]
# Output: Encrypted password: [encrypted string]
# Output: Decrypted password: super_secret_password
```

## 🎨 Design Patterns for Data Engineering

### Factory Pattern for Data Sources

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class DataSource(ABC):
    @abstractmethod
    def connect(self) -> bool:
        pass
    
    @abstractmethod
    def read_data(self) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def close(self):
        pass

class PostgreSQLSource(DataSource):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.connection = None
    
    def connect(self) -> bool:
        print(f"Connecting to PostgreSQL: {self.config['host']}")
        self.connection = "postgresql_connection"
        return True
    
    def read_data(self) -> Dict[str, Any]:
        return {"source": "postgresql", "data": [1, 2, 3]}
    
    def close(self):
        print("Closing PostgreSQL connection")
        self.connection = None

class S3Source(DataSource):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client = None
    
    def connect(self) -> bool:
        print(f"Connecting to S3 bucket: {self.config['bucket']}")
        self.client = "s3_client"
        return True
    
    def read_data(self) -> Dict[str, Any]:
        return {"source": "s3", "data": ["file1.csv", "file2.json"]}
    
    def close(self):
        print("Closing S3 connection")
        self.client = None

class DataSourceFactory:
    _sources = {
        "postgresql": PostgreSQLSource,
        "s3": S3Source
    }
    
    @classmethod
    def create_source(cls, source_type: str, config: Dict[str, Any]) -> DataSource:
        if source_type not in cls._sources:
            raise ValueError(f"Unknown source type: {source_type}")
        
        source_class = cls._sources[source_type]
        return source_class(config)
    
    @classmethod
    def register_source(cls, source_type: str, source_class: type):
        """Register a new data source type"""
        cls._sources[source_type] = source_class

# Usage
pg_config = {"host": "localhost", "port": 5432, "database": "analytics"}
s3_config = {"bucket": "data-lake", "region": "us-east-1"}

# Create data sources using factory
pg_source = DataSourceFactory.create_source("postgresql", pg_config)
s3_source = DataSourceFactory.create_source("s3", s3_config)

# Use the sources
for source in [pg_source, s3_source]:
    source.connect()
    data = source.read_data()
    print(f"Data from {data['source']}: {data['data']}")
    source.close()

# Output: Connecting to PostgreSQL: localhost
# Output: Data from postgresql: [1, 2, 3]
# Output: Closing PostgreSQL connection
# Output: Connecting to S3 bucket: data-lake
# Output: Data from s3: ['file1.csv', 'file2.json']
# Output: Closing S3 connection
```

### Observer Pattern for Pipeline Monitoring

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime

class PipelineObserver(ABC):
    @abstractmethod
    def on_pipeline_start(self, pipeline_id: str):
        pass
    
    @abstractmethod
    def on_pipeline_complete(self, pipeline_id: str, metrics: Dict[str, Any]):
        pass
    
    @abstractmethod
    def on_pipeline_error(self, pipeline_id: str, error: str):
        pass

class LoggingObserver(PipelineObserver):
    def on_pipeline_start(self, pipeline_id: str):
        print(f"[LOG] Pipeline {pipeline_id} started at {datetime.now()}")
    
    def on_pipeline_complete(self, pipeline_id: str, metrics: Dict[str, Any]):
        print(f"[LOG] Pipeline {pipeline_id} completed. Metrics: {metrics}")
    
    def on_pipeline_error(self, pipeline_id: str, error: str):
        print(f"[LOG] Pipeline {pipeline_id} failed: {error}")

class MetricsObserver(PipelineObserver):
    def __init__(self):
        self.metrics_store = {}
    
    def on_pipeline_start(self, pipeline_id: str):
        self.metrics_store[pipeline_id] = {"start_time": datetime.now()}
    
    def on_pipeline_complete(self, pipeline_id: str, metrics: Dict[str, Any]):
        if pipeline_id in self.metrics_store:
            self.metrics_store[pipeline_id].update(metrics)
            self.metrics_store[pipeline_id]["status"] = "completed"
    
    def on_pipeline_error(self, pipeline_id: str, error: str):
        if pipeline_id in self.metrics_store:
            self.metrics_store[pipeline_id]["status"] = "failed"
            self.metrics_store[pipeline_id]["error"] = error

class DataPipeline:
    def __init__(self, pipeline_id: str):
        self.pipeline_id = pipeline_id
        self.observers: List[PipelineObserver] = []
    
    def add_observer(self, observer: PipelineObserver):
        self.observers.append(observer)
    
    def remove_observer(self, observer: PipelineObserver):
        self.observers.remove(observer)
    
    def notify_start(self):
        for observer in self.observers:
            observer.on_pipeline_start(self.pipeline_id)
    
    def notify_complete(self, metrics: Dict[str, Any]):
        for observer in self.observers:
            observer.on_pipeline_complete(self.pipeline_id, metrics)
    
    def notify_error(self, error: str):
        for observer in self.observers:
            observer.on_pipeline_error(self.pipeline_id, error)
    
    def run(self):
        self.notify_start()
        
        try:
            # Simulate pipeline execution
            print(f"Executing pipeline {self.pipeline_id}")
            import time
            time.sleep(0.1)  # Simulate work
            
            # Simulate success
            metrics = {"records_processed": 1000, "execution_time": 0.1}
            self.notify_complete(metrics)
            
        except Exception as e:
            self.notify_error(str(e))

# Usage
pipeline = DataPipeline("etl_001")

# Add observers
logging_observer = LoggingObserver()
metrics_observer = MetricsObserver()

pipeline.add_observer(logging_observer)
pipeline.add_observer(metrics_observer)

# Run pipeline
pipeline.run()

# Check metrics
print(f"Stored metrics: {metrics_observer.metrics_store}")

# Output: [LOG] Pipeline etl_001 started at 2024-01-01 10:00:00.123456
# Output: Executing pipeline etl_001
# Output: [LOG] Pipeline etl_001 completed. Metrics: {'records_processed': 1000, 'execution_time': 0.1}
# Output: Stored metrics: {'etl_001': {'start_time': datetime.datetime(2024, 1, 1, 10, 0, 0, 123456), 'records_processed': 1000, 'execution_time': 0.1, 'status': 'completed'}}
```

This document provides advanced Python concepts specifically tailored for data engineering, covering production-ready patterns, security, performance optimization, and integration techniques essential for building robust data systems.

## 🔄 Asynchronous Programming

### Async/Await Fundamentals

```python
import asyncio
import aiohttp
from typing import List, Dict, Any

class AsyncDataProcessor:
    def __init__(self, max_concurrent: int = 10):
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def fetch_data(self, url: str, session: aiohttp.ClientSession) -> Dict[str, Any]:
        async with self.semaphore:
            try:
                async with session.get(url) as response:
                    return await response.json() if response.status == 200 else {"error": response.status}
            except Exception as e:
                return {"error": str(e)}
    
    async def batch_process_urls(self, urls: List[str]) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_data(url, session) for url in urls]
            return await asyncio.gather(*tasks, return_exceptions=True)

# Usage
async def main():
    processor = AsyncDataProcessor(max_concurrent=5)
    urls = ["https://api.example.com/data/1", "https://api.example.com/data/2"]
    results = await processor.batch_process_urls(urls)
    print(f"Processed {len(results)} URLs")

# asyncio.run(main())
```

## 📦 Data Serialization Formats

### Advanced JSON and Parquet

```python
import json
import orjson  # pip install orjson
import pandas as pd
from datetime import datetime
from decimal import Decimal

class DataFormatHandler:
    @staticmethod
    def custom_json_encoder(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    @staticmethod
    def serialize_with_orjson(data) -> bytes:
        return orjson.dumps(data, default=DataFormatHandler.custom_json_encoder)
    
    @staticmethod
    def optimize_parquet_storage(df: pd.DataFrame) -> Dict[str, Any]:
        original_memory = df.memory_usage(deep=True).sum()
        
        # Convert object columns to category if beneficial
        for col in df.select_dtypes(include=['object']).columns:
            if df[col].nunique() / len(df) < 0.5:
                df[col] = df[col].astype('category')
        
        optimized_memory = df.memory_usage(deep=True).sum()
        return {
            'memory_reduction_percent': (original_memory - optimized_memory) / original_memory * 100,
            'original_memory_mb': original_memory / 1024 / 1024,
            'optimized_memory_mb': optimized_memory / 1024 / 1024
        }

# Usage
df = pd.DataFrame({'category': ['A', 'B', 'C'] * 1000, 'value': range(3000)})
handler = DataFormatHandler()
results = handler.optimize_parquet_storage(df)
print(f"Memory reduction: {results['memory_reduction_percent']:.1f}%")
```

## 🌐 Distributed Computing Integration

### Celery Task Queue

```python
from celery import Celery, chain, group
from typing import Dict, Any, List

app = Celery('data_pipeline')
app.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0'
)

@app.task(bind=True, max_retries=3)
def extract_data(self, source_config: Dict[str, Any]) -> Dict[str, Any]:
    try:
        # Simulate data extraction
        return {'source': source_config['source'], 'records': list(range(100))}
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)

@app.task
def transform_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'source': raw_data['source'],
        'processed_records': [x * 2 for x in raw_data['records'][:10]],
        'record_count': len(raw_data['records'])
    }

@app.task
def load_data(transformed_data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'source': transformed_data['source'],
        'loaded_records': transformed_data['record_count'],
        'status': 'success'
    }

class DistributedETLPipeline:
    def run_parallel_etl(self, source_configs: List[Dict[str, Any]]) -> str:
        etl_chains = []
        for config in source_configs:
            etl_chain = chain(extract_data.s(config), transform_data.s(), load_data.s())
            etl_chains.append(etl_chain)
        
        job = group(etl_chains).apply_async()
        return job.id

# Usage
pipeline = DistributedETLPipeline()
sources = [{'source': 'db1'}, {'source': 'db2'}]
job_id = pipeline.run_parallel_etl(sources)
print(f"Pipeline job ID: {job_id}")
```