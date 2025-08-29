# Python Best Practices for Data Engineering

## Table of Contents

1. [Code Style and Formatting](#code-style-and-formatting)
   - [PEP 8 Compliance](#pep-8-compliance)
   - [Import Organization](#import-organization)
   - [Naming Conventions](#naming-conventions)
2. [Error Handling and Logging](#error-handling-and-logging)
   - [Comprehensive Error Handling](#comprehensive-error-handling)
   - [Retry Logic with Exponential Backoff](#retry-logic-with-exponential-backoff)
3. [Type Hints and Documentation](#type-hints-and-documentation)
   - [Comprehensive Type Hints](#comprehensive-type-hints)
   - [Documentation Standards](#documentation-standards)
4. [Performance Optimization](#performance-optimization)
   - [Memory-Efficient Data Processing](#memory-efficient-data-processing)
   - [Database Best Practices](#database-best-practices)
5. [Testing Best Practices](#testing-best-practices)
   - [Comprehensive Testing Strategy](#comprehensive-testing-strategy)
6. [Security Best Practices](#security-best-practices)
   - [Secure Coding Practices](#secure-coding-practices)
7. [Project Structure and Organization](#project-structure-and-organization)
   - [Recommended Project Structure](#recommended-project-structure)
   - [Configuration Management](#configuration-management)

---

## Code Style and Formatting

### PEP 8 Compliance
```python
# Good: Clear, readable variable names
user_count = 100
database_connection = get_db_connection()
processed_records = []

# Bad: Unclear abbreviations
uc = 100
db_conn = get_db_connection()
pr = []

# Good: Proper spacing and line length
def process_user_data(user_id: int, 
                     include_history: bool = False,
                     max_records: int = 1000) -> Dict[str, Any]:
    """Process user data with optional parameters."""
    pass

# Bad: Poor spacing and too long
def process_user_data(user_id:int,include_history:bool=False,max_records:int=1000)->Dict[str,Any]:
    pass
```

### Import Organization
```python
# Standard library imports first
import os
import sys
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any

# Third-party imports second
import pandas as pd
import numpy as np
import requests
from sqlalchemy import create_engine

# Local application imports last
from .database import DatabaseManager
from .utils import validate_data, clean_text
from ..config import settings
```

### Naming Conventions
```python
# Constants: UPPER_CASE_WITH_UNDERSCORES
MAX_RETRY_ATTEMPTS = 3
DEFAULT_TIMEOUT = 30
DATABASE_URL = "postgresql://localhost/mydb"

# Classes: PascalCase
class DataProcessor:
    pass

class DatabaseConnectionManager:
    pass

# Functions and variables: snake_case
def process_csv_file(file_path: str) -> pd.DataFrame:
    pass

def calculate_user_metrics(user_data: Dict) -> Dict:
    pass

# Private methods: leading underscore
class DataPipeline:
    def _validate_input(self, data):
        pass
    
    def _transform_data(self, data):
        pass
```

## Error Handling and Logging

### Comprehensive Error Handling
```python
import logging
from typing import Optional
from contextlib import contextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_pipeline.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Custom exceptions for better error handling
class DataProcessingError(Exception):
    """Raised when data processing fails."""
    pass

class DataValidationError(DataProcessingError):
    """Raised when data validation fails."""
    def __init__(self, message: str, invalid_records: List = None):
        super().__init__(message)
        self.invalid_records = invalid_records or []

# Proper error handling with context
@contextmanager
def error_handler(operation_name: str):
    """Context manager for consistent error handling."""
    try:
        logger.info(f"Starting {operation_name}")
        yield
        logger.info(f"Successfully completed {operation_name}")
    except Exception as e:
        logger.error(f"Failed {operation_name}: {str(e)}", exc_info=True)
        raise

def process_data_safely(data: List[Dict]) -> Optional[List[Dict]]:
    """Process data with comprehensive error handling."""
    if not data:
        logger.warning("No data provided for processing")
        return None
    
    try:
        with error_handler("data processing"):
            # Validate input
            if not all(isinstance(record, dict) for record in data):
                raise DataValidationError("All records must be dictionaries")
            
            # Process data
            processed_data = []
            for i, record in enumerate(data):
                try:
                    processed_record = transform_record(record)
                    processed_data.append(processed_record)
                except Exception as e:
                    logger.warning(f"Failed to process record {i}: {e}")
                    continue  # Skip invalid records
            
            if not processed_data:
                raise DataProcessingError("No records were successfully processed")
            
            return processed_data
            
    except DataValidationError:
        raise  # Re-raise validation errors
    except Exception as e:
        logger.error(f"Unexpected error in data processing: {e}")
        return None
```

### Retry Logic with Exponential Backoff
```python
import time
import random
from functools import wraps
from typing import Callable, Type, Tuple

def retry_with_backoff(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """Decorator for retrying functions with exponential backoff."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_attempts - 1:
                        logger.error(f"Max retry attempts reached for {func.__name__}")
                        raise
                    
                    # Calculate delay with exponential backoff
                    delay = min(base_delay * (backoff_factor ** attempt), max_delay)
                    
                    # Add jitter to prevent thundering herd
                    if jitter:
                        delay *= (0.5 + random.random() * 0.5)
                    
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_attempts} failed for {func.__name__}: {e}. "
                        f"Retrying in {delay:.2f}s..."
                    )
                    time.sleep(delay)
            
            raise last_exception
        
        return wrapper
    return decorator

# Usage
@retry_with_backoff(
    max_attempts=3,
    base_delay=1.0,
    exceptions=(ConnectionError, TimeoutError)
)
def fetch_data_from_api(url: str) -> Dict:
    """Fetch data from API with retry logic."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()
```

## Type Hints and Documentation

### Comprehensive Type Hints
```python
from typing import (
    List, Dict, Optional, Union, Callable, Any, 
    TypeVar, Generic, Protocol, Literal
)
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Type variables for generic functions
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

# Protocol for duck typing
class Processable(Protocol):
    def process(self) -> Dict[str, Any]:
        ...

# Generic data processor
class DataProcessor(Generic[T]):
    def __init__(self, data: List[T]):
        self.data = data
    
    def process_batch(self, 
                     processor: Callable[[T], Dict[str, Any]],
                     batch_size: int = 1000) -> List[Dict[str, Any]]:
        """Process data in batches with type safety."""
        results = []
        for i in range(0, len(self.data), batch_size):
            batch = self.data[i:i + batch_size]
            batch_results = [processor(item) for item in batch]
            results.extend(batch_results)
        return results

# Dataclass for structured data
@dataclass
class UserRecord:
    id: int
    name: str
    email: str
    age: Optional[int] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

# Function with comprehensive type hints
def aggregate_user_data(
    users: List[UserRecord],
    group_by: Literal['age_group', 'domain'] = 'age_group',
    include_metadata: bool = False
) -> Dict[str, Dict[str, Union[int, float]]]:
    """
    Aggregate user data by specified grouping.
    
    Args:
        users: List of user records to aggregate
        group_by: How to group users ('age_group' or 'domain')
        include_metadata: Whether to include metadata in results
    
    Returns:
        Dictionary with aggregated statistics by group
    
    Raises:
        ValueError: If group_by parameter is invalid
    """
    if group_by not in ['age_group', 'domain']:
        raise ValueError(f"Invalid group_by value: {group_by}")
    
    # Implementation here
    pass
```

### Documentation Standards
```python
def process_sales_data(
    data_path: str,
    output_format: Literal['csv', 'parquet', 'json'] = 'parquet',
    date_range: Optional[Tuple[str, str]] = None,
    filters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Process sales data from file and apply transformations.
    
    This function reads sales data from the specified path, applies optional
    filters and date range restrictions, then outputs the processed data
    in the requested format.
    
    Args:
        data_path: Path to the input sales data file. Supports CSV, JSON, and Parquet.
        output_format: Format for output file. Defaults to 'parquet' for efficiency.
        date_range: Optional tuple of (start_date, end_date) in 'YYYY-MM-DD' format.
                   If provided, filters data to this date range.
        filters: Optional dictionary of column filters. Keys are column names,
                values are filter criteria (e.g., {'region': 'US', 'amount': '>1000'}).
    
    Returns:
        Dictionary containing:
            - 'output_path': Path to the processed output file
            - 'record_count': Number of records processed
            - 'processing_time': Time taken in seconds
            - 'summary_stats': Basic statistics about the processed data
    
    Raises:
        FileNotFoundError: If the input data file doesn't exist
        ValueError: If date_range format is invalid or output_format is unsupported
        DataProcessingError: If data processing fails due to data quality issues
    
    Example:
        >>> result = process_sales_data(
        ...     'sales_2023.csv',
        ...     output_format='parquet',
        ...     date_range=('2023-01-01', '2023-12-31'),
        ...     filters={'region': 'US'}
        ... )
        >>> print(f"Processed {result['record_count']} records")
    
    Note:
        Large files (>1GB) are processed in chunks to manage memory usage.
        Progress is logged every 10,000 records.
    """
    pass
```

## Performance Optimization

### Memory-Efficient Data Processing
```python
import gc
from typing import Iterator, Generator
import psutil
import os

def get_memory_usage() -> float:
    """Get current memory usage in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

def process_large_file_efficiently(file_path: str, 
                                 chunk_size: int = 10000) -> Generator[Dict, None, None]:
    """
    Process large files in memory-efficient chunks.
    
    Args:
        file_path: Path to the large file
        chunk_size: Number of records to process at once
    
    Yields:
        Processed data chunks
    """
    logger.info(f"Starting to process {file_path} with chunk size {chunk_size}")
    initial_memory = get_memory_usage()
    
    try:
        # Use pandas chunking for CSV files
        for chunk_num, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size)):
            logger.debug(f"Processing chunk {chunk_num + 1}")
            
            # Process chunk
            processed_chunk = transform_dataframe(chunk)
            
            # Yield results
            yield processed_chunk.to_dict('records')
            
            # Memory management
            del chunk, processed_chunk
            
            # Force garbage collection every 10 chunks
            if chunk_num % 10 == 0:
                gc.collect()
                current_memory = get_memory_usage()
                logger.info(f"Memory usage: {current_memory:.1f}MB "
                           f"(+{current_memory - initial_memory:.1f}MB)")
    
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")
        raise
    
    finally:
        # Final cleanup
        gc.collect()
        final_memory = get_memory_usage()
        logger.info(f"Processing complete. Final memory: {final_memory:.1f}MB")

# Efficient data structures
def use_appropriate_data_structures():
    """Examples of choosing efficient data structures."""
    
    # Use sets for membership testing (O(1) vs O(n) for lists)
    valid_ids = {1, 2, 3, 4, 5}  # Instead of [1, 2, 3, 4, 5]
    if user_id in valid_ids:  # O(1) operation
        pass
    
    # Use deque for frequent insertions/deletions at ends
    from collections import deque
    queue = deque()  # Instead of list for queue operations
    queue.appendleft(item)  # O(1) vs O(n) for list.insert(0, item)
    
    # Use defaultdict to avoid key existence checks
    from collections import defaultdict
    counts = defaultdict(int)  # Instead of regular dict
    counts[key] += 1  # No need to check if key exists
    
    # Use Counter for counting operations
    from collections import Counter
    word_counts = Counter(words)  # More efficient than manual counting
```

### Database Best Practices
```python
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
import pandas as pd

class DatabaseManager:
    """Efficient database connection management."""
    
    def __init__(self, connection_string: str):
        # Configure connection pool
        self.engine = create_engine(
            connection_string,
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,  # Validate connections
            pool_recycle=3600,   # Recycle connections every hour
            echo=False  # Set to True for SQL debugging
        )
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = self.engine.connect()
        try:
            yield conn
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def execute_query_efficiently(self, query: str, params: Dict = None) -> pd.DataFrame:
        """Execute query with proper resource management."""
        with self.get_connection() as conn:
            # Use parameterized queries to prevent SQL injection
            if params:
                result = pd.read_sql(text(query), conn, params=params)
            else:
                result = pd.read_sql(query, conn)
            
            return result
    
    def bulk_insert_efficiently(self, df: pd.DataFrame, table_name: str, 
                               batch_size: int = 10000):
        """Efficient bulk insert with batching."""
        with self.get_connection() as conn:
            # Use pandas to_sql with method='multi' for efficiency
            df.to_sql(
                table_name,
                conn,
                if_exists='append',
                index=False,
                method='multi',  # Use executemany for better performance
                chunksize=batch_size
            )
            
            logger.info(f"Inserted {len(df)} records into {table_name}")

# Efficient data loading patterns
def load_data_efficiently(file_paths: List[str]) -> pd.DataFrame:
    """Load multiple files efficiently."""
    dataframes = []
    
    for file_path in file_paths:
        # Use appropriate pandas options for efficiency
        df = pd.read_csv(
            file_path,
            dtype_backend='pyarrow',  # Use Arrow backend for better performance
            engine='pyarrow',         # Faster CSV parsing
            low_memory=False          # Read entire file for consistent dtypes
        )
        dataframes.append(df)
    
    # Efficient concatenation
    result = pd.concat(dataframes, ignore_index=True, copy=False)
    
    # Optimize memory usage
    result = optimize_dataframe_memory(result)
    
    return result

def optimize_dataframe_memory(df: pd.DataFrame) -> pd.DataFrame:
    """Optimize DataFrame memory usage."""
    for col in df.columns:
        col_type = df[col].dtype
        
        if col_type != 'object':
            c_min = df[col].min()
            c_max = df[col].max()
            
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
            
            elif str(col_type)[:5] == 'float':
                if c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
        
        else:
            # Convert string columns to category if beneficial
            if df[col].nunique() / len(df) < 0.5:  # Less than 50% unique values
                df[col] = df[col].astype('category')
    
    return df
```

## Testing Best Practices

### Comprehensive Testing Strategy
```python
import pytest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
from typing import Any, Dict, List

class TestDataProcessor:
    """Test class following pytest conventions."""
    
    @pytest.fixture
    def sample_data(self) -> List[Dict[str, Any]]:
        """Fixture providing sample test data."""
        return [
            {'id': 1, 'name': 'John', 'age': 30, 'city': 'NYC'},
            {'id': 2, 'name': 'Jane', 'age': 25, 'city': 'LA'},
            {'id': 3, 'name': 'Bob', 'age': 35, 'city': 'Chicago'}
        ]
    
    @pytest.fixture
    def data_processor(self):
        """Fixture providing DataProcessor instance."""
        return DataProcessor()
    
    def test_process_valid_data(self, data_processor, sample_data):
        """Test processing with valid data."""
        result = data_processor.process(sample_data)
        
        assert result is not None
        assert len(result) == len(sample_data)
        assert all('processed' in record for record in result)
    
    def test_process_empty_data(self, data_processor):
        """Test processing with empty data."""
        result = data_processor.process([])
        
        assert result == []
    
    def test_process_invalid_data(self, data_processor):
        """Test processing with invalid data."""
        invalid_data = [{'invalid': 'data'}]
        
        with pytest.raises(DataValidationError) as exc_info:
            data_processor.process(invalid_data)
        
        assert "validation failed" in str(exc_info.value).lower()
    
    @patch('requests.get')
    def test_api_call_with_mock(self, mock_get, data_processor):
        """Test API calls using mocks."""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {'status': 'success', 'data': []}
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Test the function
        result = data_processor.fetch_external_data('http://api.example.com')
        
        # Assertions
        assert result['status'] == 'success'
        mock_get.assert_called_once_with('http://api.example.com')
    
    @pytest.mark.parametrize("age,expected_group", [
        (20, 'young'),
        (35, 'middle'),
        (65, 'senior'),
        (5, 'child')
    ])
    def test_age_grouping(self, data_processor, age, expected_group):
        """Test age grouping with multiple parameters."""
        result = data_processor.categorize_age(age)
        assert result == expected_group
    
    def test_database_integration(self, data_processor):
        """Integration test with database."""
        # Use test database
        test_db_url = "sqlite:///:memory:"
        
        with patch.object(data_processor, 'db_url', test_db_url):
            # Setup test data
            data_processor.create_test_tables()
            data_processor.insert_test_data()
            
            # Test the functionality
            result = data_processor.query_data()
            
            assert len(result) > 0
            assert 'id' in result[0]

# Property-based testing with Hypothesis
from hypothesis import given, strategies as st

class TestDataValidation:
    """Property-based testing examples."""
    
    @given(st.lists(st.integers(min_value=0, max_value=100)))
    def test_sum_is_always_positive(self, numbers):
        """Test that sum of positive numbers is always positive."""
        result = sum(numbers)
        assert result >= 0
    
    @given(st.text(min_size=1, max_size=100))
    def test_string_processing_never_fails(self, text):
        """Test that string processing handles any input."""
        result = process_text(text)
        assert isinstance(result, str)
        assert len(result) >= 0

# Performance testing
import time
import pytest

def test_performance_benchmark():
    """Test performance requirements."""
    large_dataset = generate_large_dataset(100000)
    
    start_time = time.time()
    result = process_large_dataset(large_dataset)
    end_time = time.time()
    
    processing_time = end_time - start_time
    
    # Assert performance requirements
    assert processing_time < 10.0  # Should complete within 10 seconds
    assert len(result) == len(large_dataset)

# Test configuration
@pytest.fixture(scope="session")
def test_config():
    """Session-wide test configuration."""
    return {
        'test_db_url': 'sqlite:///:memory:',
        'test_api_base': 'http://test.api.com',
        'timeout': 30
    }
```

## Security Best Practices

### Secure Coding Practices
```python
import os
import secrets
import hashlib
from cryptography.fernet import Fernet
from typing import Optional

class SecureDataHandler:
    """Secure data handling practices."""
    
    def __init__(self):
        # Use environment variables for sensitive data
        self.api_key = os.getenv('API_KEY')
        if not self.api_key:
            raise ValueError("API_KEY environment variable not set")
        
        # Generate secure encryption key
        self.encryption_key = self._get_or_create_key()
        self.cipher = Fernet(self.encryption_key)
    
    def _get_or_create_key(self) -> bytes:
        """Get encryption key from secure storage."""
        key_file = os.getenv('ENCRYPTION_KEY_FILE', '.encryption_key')
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            # Generate new key
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            os.chmod(key_file, 0o600)  # Restrict file permissions
            return key
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data."""
        encrypted_data = self.cipher.encrypt(data.encode())
        return encrypted_data.decode()
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data."""
        decrypted_data = self.cipher.decrypt(encrypted_data.encode())
        return decrypted_data.decode()
    
    def hash_password(self, password: str) -> str:
        """Securely hash passwords."""
        # Use a random salt
        salt = secrets.token_hex(32)
        
        # Hash password with salt
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt.encode(),
            100000  # iterations
        )
        
        return f"{salt}:{password_hash.hex()}"
    
    def verify_password(self, password: str, stored_hash: str) -> bool:
        """Verify password against stored hash."""
        try:
            salt, hash_hex = stored_hash.split(':')
            
            password_hash = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode(),
                salt.encode(),
                100000
            )
            
            return secrets.compare_digest(hash_hex, password_hash.hex())
        except ValueError:
            return False

# Input validation and sanitization
import re
from html import escape

def validate_and_sanitize_input(user_input: str, 
                               input_type: str = 'general') -> Optional[str]:
    """Validate and sanitize user input."""
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string")
    
    # Remove null bytes and control characters
    sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', user_input)
    
    # Trim whitespace
    sanitized = sanitized.strip()
    
    # Type-specific validation
    if input_type == 'email':
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, sanitized):
            raise ValueError("Invalid email format")
    
    elif input_type == 'sql_identifier':
        # Only allow alphanumeric and underscore for SQL identifiers
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', sanitized):
            raise ValueError("Invalid SQL identifier")
    
    elif input_type == 'html':
        # Escape HTML to prevent XSS
        sanitized = escape(sanitized)
    
    return sanitized if sanitized else None

# Secure database queries
def execute_safe_query(connection, query: str, params: Dict = None):
    """Execute database query safely with parameterization."""
    # Always use parameterized queries
    if params:
        # Validate parameter names to prevent injection
        for param_name in params.keys():
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', param_name):
                raise ValueError(f"Invalid parameter name: {param_name}")
        
        return connection.execute(query, params)
    else:
        return connection.execute(query)
```

## Project Structure and Organization

### Recommended Project Structure
```
data_engineering_project/
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── logging_config.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── extractors/
│   │   ├── transformers/
│   │   └── loaders/
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── file_utils.py
│   │   └── validation.py
│   └── pipelines/
│       ├── __init__.py
│       ├── daily_etl.py
│       └── streaming_pipeline.py
├── tests/
│   ├── __init__.py
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── docs/
├── scripts/
├── requirements.txt
├── setup.py
├── README.md
├── .gitignore
├── .pre-commit-config.yaml
└── pyproject.toml
```

### Configuration Management
```python
# config/settings.py
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class DatabaseConfig:
    host: str
    port: int
    database: str
    username: str
    password: str
    
    @property
    def connection_string(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

@dataclass
class AppConfig:
    # Environment
    environment: str = os.getenv('ENVIRONMENT', 'development')
    debug: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Database
    database: DatabaseConfig = None
    
    # API settings
    api_timeout: int = int(os.getenv('API_TIMEOUT', '30'))
    max_retries: int = int(os.getenv('MAX_RETRIES', '3'))
    
    # Processing settings
    batch_size: int = int(os.getenv('BATCH_SIZE', '1000'))
    max_workers: int = int(os.getenv('MAX_WORKERS', '4'))
    
    def __post_init__(self):
        if self.database is None:
            self.database = DatabaseConfig(
                host=os.getenv('DB_HOST', 'localhost'),
                port=int(os.getenv('DB_PORT', '5432')),
                database=os.getenv('DB_NAME', 'mydb'),
                username=os.getenv('DB_USER', 'user'),
                password=os.getenv('DB_PASSWORD', 'password')
            )

# Load configuration
config = AppConfig()
```

These best practices ensure your Python code is:
- **Maintainable**: Clear structure and documentation
- **Reliable**: Comprehensive error handling and testing
- **Secure**: Proper input validation and data protection
- **Performant**: Efficient algorithms and resource usage
- **Professional**: Following industry standards and conventions