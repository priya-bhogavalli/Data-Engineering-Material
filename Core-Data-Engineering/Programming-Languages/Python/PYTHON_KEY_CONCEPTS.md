# Python Key Concepts for Data Engineering

## 📋 Table of Contents

1. [Data Structures](#1-data-structures)
   - [Lists - Ordered, Mutable Collections](#1-customer-data-lookup-o1-performance---instant)
   - [Dictionaries - Key-Value Mappings](#1-customer-data-lookup-o1-performance---instant)
   - [Sets - Unique Collections](#1-customer-data-lookup-o1-performance---instant)
   - [Tuples - Immutable Ordered Collections](#1-customer-data-lookup-o1-performance---instant)
2. [Functions and Decorators](#2-functions-and-decorators)
   - [Function Definitions](#test-the-function)
   - [Decorators - Function Wrappers](#1-customer-data-lookup-o1-performance---instant)
3. [Object-Oriented Programming](#3-object-oriented-programming)
   - [Class Definition](#class-definition)
   - [Inheritance and Polymorphism](#2-functions-and-decorators)
4. [Error Handling](#4-error-handling)
   - [Try-Except Patterns](#try-except-patterns)
5. [File I/O and Data Formats](#5-file-io-and-data-formats)
   - [Text Files](#reading-files)
   - [JSON Operations](#data-cleaning-operations)
6. [Generators and Iterators](#6-generators-and-iterators)
   - [Generator Functions](#2-functions-and-decorators)
   - [Iterator Protocol](#iterator-protocol)
7. [Context Managers](#7-context-managers)
   - [Built-in Context Managers](#7-context-managers)
   - [Custom Context Managers](#7-context-managers)
8. [Concurrency and Parallelism](#8-concurrency-and-parallelism)
   - [Threading for I/O-bound Tasks](#python-key-concepts-for-data-engineering)
   - [Multiprocessing for CPU-bound Tasks](#python-key-concepts-for-data-engineering)
9. [Type Hints and Documentation](#9-type-hints-and-documentation)
   - [Type Hints](#9-type-hints-and-documentation)
10. [Testing](#10-testing)
    - [Unit Testing](#10-testing)
    - [Pytest (Alternative Testing Framework)](#10-testing)

---

## 1. Data Structures
**What they are**: Data structures are like different types of containers for your data - each optimized for specific tasks, just like how you use different containers in your kitchen.

**Real-World Analogy**: 
- **Lists** = Shopping list (ordered, can add/remove items)
- **Dictionaries** = Phone book (look up by name to get number)
- **Sets** = Guest list (no duplicates allowed)
- **Tuples** = GPS coordinates (fixed, can't change)

**Why Critical for Data Engineering**: Choosing the wrong data structure is like using a spoon to cut steak - it works, but it's painfully slow. The right choice can make your code 100x faster.

**Performance Impact**: Processing 1 million records with the right data structure takes seconds; with the wrong one, it takes hours.

**When to use**: 
- Lists for ordered data that needs modification
- Dictionaries for key-value lookups and configuration
- Sets for deduplication and membership testing
- Tuples for immutable structured data

> 📚 **For comprehensive coverage of Python data structures, see [PYTHON_DATA_STRUCTURES.md](./PYTHON_DATA_STRUCTURES.md)**
> 
> This includes:
> - Built-in types (lists, dicts, sets, tuples, strings)
> - Collections module (Counter, defaultdict, deque, namedtuple)
> - Advanced structures (heaps, queues, arrays)
> - Performance comparisons and best practices
> - Real-world examples for data engineering

**Lists - Ordered, Mutable Collections**:
```python
# Real Data Engineering Example: Processing customer transaction IDs
transaction_ids = [1001, 1002, 1003, 1004, 1005]

# Adding new transactions as they come in
transaction_ids.append(1006)                    # New transaction
transaction_ids.extend([1007, 1008, 1009])     # Batch of transactions
transaction_ids.insert(0, 1000)                # Insert at beginning

# Data cleaning operations
transaction_ids.remove(1003)                   # Remove cancelled transaction
last_transaction = transaction_ids.pop()        # Get and remove last

# Real Business Scenarios with List Comprehensions:

# 1. Data Transformation: Convert IDs to strings for API calls
api_ready_ids = [f"TXN_{id}" for id in transaction_ids]
print(f"API ready IDs: {api_ready_ids[:3]}...")
# Output: API ready IDs: ['TXN_1000', 'TXN_1001', 'TXN_1002']...

# 2. Data Filtering: Find high-value transactions (ID > 1005)
high_value_txns = [id for id in transaction_ids if id > 1005]
print(f"High value transactions: {high_value_txns}")
# Output: High value transactions: [1006, 1007, 1008]
# Business use: Flag for manual review

# 3. Complex Processing: Create transaction batches for processing
batch_matrix = [[batch_id * 100 + i for i in range(10)] 
                for batch_id in range(5)]
# Creates 5 batches of 10 transaction IDs each

# Performance Note: List comprehensions are 2-3x faster than loops
# Critical when processing millions of records
```

**Dictionaries - Key-Value Mappings**:
```python
# Real Example: Data Pipeline Configuration
pipeline_config = {
    'source_database': 'postgresql://prod-db:5432/sales',
    'target_warehouse': 's3://data-lake/processed/',
    'batch_size': 10000,
    'retry_attempts': 3,
    'timeout_seconds': 300
}

# Dynamic configuration updates
pipeline_config['last_run'] = '2024-01-15 10:30:00'     # Add new setting
batch_size = pipeline_config.get('batch_size', 1000)    # Safe access with fallback
pipeline_config.update({                                 # Bulk updates
    'debug_mode': True,
    'log_level': 'INFO'
})

# Real Business Scenarios:

# 1. Customer Data Lookup (O(1) performance - instant!)
customer_data = {
    'CUST001': {'name': 'John Doe', 'tier': 'Premium', 'credit_limit': 50000},
    'CUST002': {'name': 'Jane Smith', 'tier': 'Gold', 'credit_limit': 25000},
    'CUST003': {'name': 'Bob Johnson', 'tier': 'Silver', 'credit_limit': 10000}
}

# Lightning-fast customer lookup for real-time transactions
customer_info = customer_data.get('CUST001', {'tier': 'Basic', 'credit_limit': 1000})
print(f"Customer info: {customer_info}")
# Output: Customer info: {'name': 'John Doe', 'tier': 'Premium', 'credit_limit': 50000}

# 2. Data Transformation: Square transaction amounts for analysis
transaction_amounts = {1001: 150.50, 1002: 299.99, 1003: 75.25}
squared_amounts = {txn_id: amount**2 for txn_id, amount in transaction_amounts.items()}
print(f"Squared amounts: {squared_amounts}")
# Output: Squared amounts: {1001: 22650.25, 1002: 89994.0001, 1003: 5662.5625}

# 3. Configuration Filtering: Extract only numeric settings
numeric_settings = {k: v for k, v in pipeline_config.items() if isinstance(v, (int, float))}
print(f"Numeric settings: {numeric_settings}")
# Output: Numeric settings: {'batch_size': 10000, 'retry_attempts': 3, 'timeout_seconds': 300}

# Why Dictionaries Rock for Data Engineering:
# - O(1) lookup time (instant, even with millions of keys)
# - Perfect for caching expensive computations
# - Ideal for configuration management
# - Essential for data deduplication
```

**Sets - Unique Collections**:
```python
# Set operations for data deduplication
unique_ids = {1, 2, 3, 4, 5}
unique_ids.add(6)
unique_ids.update([7, 8, 9])

# Set operations
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}
intersection = set1 & set2      # {3, 4}
union = set1 | set2             # {1, 2, 3, 4, 5, 6}
difference = set1 - set2        # {1, 2}
```

**Tuples - Immutable Ordered Collections**:
```python
# Tuples for fixed data structures
coordinates = (10.5, 20.3)
database_config = ('localhost', 5432, 'mydb', 'user')

# Named tuples for structured data
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)
print(f"X: {p.x}, Y: {p.y}")
# Output: X: 10, Y: 20
```

## 2. Functions and Decorators
**What they are**: Functions are reusable blocks of code that perform specific tasks. Decorators are a powerful feature that allows you to modify or extend function behavior without changing the function's code.

**Why important**: Functions promote code reusability and modularity, essential for maintaining large data pipelines. Decorators enable cross-cutting concerns like logging, timing, retry logic, and authentication without cluttering business logic.

**When to use**:
- Functions for any repeatable logic
- Decorators for logging, timing, retries, authentication
- Lambda functions for simple transformations in map/filter operations

**Function Definitions**:
```python
def process_data(data, transform_func=None, **kwargs):
    """Process data with optional transformation."""
    if transform_func:
        data = transform_func(data)
    
    # Use kwargs for flexible configuration
    batch_size = kwargs.get('batch_size', 1000)
    debug = kwargs.get('debug', False)
    
    if debug:
        print(f"Processing {len(data)} records in batches of {batch_size}")
    
    return data

# Lambda functions for simple operations
multiply = lambda x, y: x * y
filter_positive = lambda x: x > 0
```

**Decorators - Function Wrappers**:
```python
import time
import functools
from typing import Callable, Any

def timing_decorator(func: Callable) -> Callable:
    """Measure function execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return wrapper

def retry_decorator(max_attempts: int = 3, delay: float = 1.0):
    """Retry function on failure."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator

# Usage
@timing_decorator
@retry_decorator(max_attempts=3, delay=2.0)
def fetch_data_from_api(url: str):
    # API call implementation
    pass
```

## 3. Object-Oriented Programming

**What it is**: Object-Oriented Programming (OOP) is a programming paradigm that organizes code into classes and objects, modeling real-world entities and their interactions.

**Why crucial for Data Engineering**: 
- **Modularity**: Break complex data pipelines into manageable components
- **Reusability**: Create reusable data processing components
- **Maintainability**: Easier to debug and extend large systems
- **Abstraction**: Hide complex implementation details behind simple interfaces

**Real-world analogy**: Think of classes as blueprints (like a house blueprint) and objects as actual instances (actual houses built from that blueprint).

### Classes and Objects

**What they are**: 
- **Class**: A blueprint or template that defines the structure and behavior of objects
- **Object**: An instance of a class - the actual "thing" created from the blueprint

**Key concepts**:
- **Attributes**: Data stored in the object (like variables)
- **Methods**: Functions that belong to the class and operate on the object's data
- **Constructor (`__init__`)**: Special method that initializes new objects

```python
class DataProcessor:
    """A class for processing data with configurable settings."""
    
    # Class attribute (shared by all instances)
    default_batch_size = 1000
    
    def __init__(self, name: str, source_type: str):
        """Constructor - initializes a new DataProcessor object."""
        # Instance attributes (unique to each object)
        self.name = name
        self.source_type = source_type
        self.processed_count = 0
        self.errors = []
    
    def process_batch(self, data: list) -> list:
        """Process a batch of data."""
        try:
            # Simulate data processing
            processed_data = [item * 2 for item in data if isinstance(item, (int, float))]
            self.processed_count += len(processed_data)
            return processed_data
        except Exception as e:
            self.errors.append(str(e))
            return []
    
    def get_stats(self) -> dict:
        """Get processing statistics."""
        return {
            'name': self.name,
            'source_type': self.source_type,
            'processed_count': self.processed_count,
            'error_count': len(self.errors)
        }

# Creating objects (instances) from the class
processor1 = DataProcessor("Sales Data Processor", "CSV")
processor2 = DataProcessor("Customer Data Processor", "JSON")

# Using the objects
data_batch = [10, 20, 30, 40, 50]
result1 = processor1.process_batch(data_batch)
result2 = processor2.process_batch([5, 15, 25])

print(f"Processor 1 result: {result1}")
print(f"Processor 1 stats: {processor1.get_stats()}")
print(f"Processor 2 stats: {processor2.get_stats()}")
# Output: Processor 1 result: [20, 40, 60, 80, 100]
# Output: Processor 1 stats: {'name': 'Sales Data Processor', 'source_type': 'CSV', 'processed_count': 5, 'error_count': 0}
# Output: Processor 2 stats: {'name': 'Customer Data Processor', 'source_type': 'JSON', 'processed_count': 3, 'error_count': 0}
```

### Encapsulation

**What it is**: Encapsulation is the practice of bundling data and methods together while controlling access to the internal details of an object.

**Why important**: 
- **Data Protection**: Prevents external code from directly modifying internal state
- **Interface Stability**: Changes to internal implementation don't break external code
- **Validation**: Control how data is set and retrieved

**Python conventions**:
- **Public**: Normal attributes/methods (e.g., `self.name`)
- **Protected**: Single underscore prefix (e.g., `self._internal_data`) - convention only
- **Private**: Double underscore prefix (e.g., `self.__secret`) - name mangling

```python
class DatabaseConnection:
    """Encapsulated database connection with controlled access."""
    
    def __init__(self, host: str, port: int, database: str):
        # Public attributes
        self.host = host
        self.database = database
        
        # Protected attribute (internal use, but accessible)
        self._port = port
        
        # Private attributes (strongly encapsulated)
        self.__connection_string = f"postgresql://{host}:{port}/{database}"
        self.__is_connected = False
        self.__connection_pool_size = 10
    
    # Public method - part of the interface
    def connect(self) -> bool:
        """Establish database connection."""
        if self._validate_connection_params():
            self.__is_connected = True
            print(f"Connected to {self.database} on {self.host}")
            return True
        return False
    
    # Protected method (internal helper)
    def _validate_connection_params(self) -> bool:
        """Validate connection parameters."""
        return bool(self.host and self._port and self.database)
    
    # Private method (implementation detail)
    def __create_connection_pool(self):
        """Create connection pool - internal implementation."""
        return f"Pool of {self.__connection_pool_size} connections"
    
    # Property - controlled access to private data
    @property
    def is_connected(self) -> bool:
        """Check if connected (read-only access)."""
        return self.__is_connected
    
    @property
    def connection_info(self) -> dict:
        """Get connection info without exposing sensitive details."""
        return {
            'host': self.host,
            'database': self.database,
            'port': self._port,
            'connected': self.__is_connected
        }
    
    # Setter with validation
    @property
    def pool_size(self) -> int:
        return self.__connection_pool_size
    
    @pool_size.setter
    def pool_size(self, size: int):
        if 1 <= size <= 100:
            self.__connection_pool_size = size
        else:
            raise ValueError("Pool size must be between 1 and 100")

# Using encapsulation
db = DatabaseConnection("localhost", 5432, "sales_db")

# Public interface usage
db.connect()
print(f"Connection status: {db.is_connected}")
print(f"Connection info: {db.connection_info}")

# Controlled access through properties
db.pool_size = 20
print(f"Pool size: {db.pool_size}")

# Output: Connected to sales_db on localhost
# Output: Connection status: True
# Output: Connection info: {'host': 'localhost', 'database': 'sales_db', 'port': 5432, 'connected': True}
# Output: Pool size: 20
```

### Inheritance

**What it is**: Inheritance allows a class to inherit attributes and methods from another class, creating a parent-child relationship.

**Why powerful**: 
- **Code Reuse**: Don't repeat common functionality
- **Hierarchical Organization**: Model real-world relationships
- **Extensibility**: Add new features while keeping existing ones

**Key concepts**:
- **Parent/Base/Super class**: The class being inherited from
- **Child/Derived/Sub class**: The class that inherits
- **Method Override**: Child class provides its own implementation
- **super()**: Access parent class methods

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any

# Base class for all data sources
class DataSource:
    """Base class for all data sources."""
    
    def __init__(self, name: str, connection_string: str):
        self.name = name
        self.connection_string = connection_string
        self.is_connected = False
        self.records_processed = 0
    
    def connect(self) -> bool:
        """Base connection logic."""
        print(f"Establishing connection to {self.name}...")
        self.is_connected = True
        return True
    
    def disconnect(self):
        """Base disconnection logic."""
        print(f"Disconnecting from {self.name}")
        self.is_connected = False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return {
            'name': self.name,
            'connected': self.is_connected,
            'records_processed': self.records_processed
        }

# Child class for CSV files
class CSVDataSource(DataSource):
    """Specialized data source for CSV files."""
    
    def __init__(self, name: str, file_path: str, delimiter: str = ','):
        # Call parent constructor
        super().__init__(name, file_path)
        self.delimiter = delimiter
        self.headers = []
    
    def connect(self) -> bool:
        """Override parent method with CSV-specific logic."""
        # Call parent method first
        super().connect()
        print(f"Reading CSV headers from {self.connection_string}")
        # Simulate reading headers
        self.headers = ['id', 'name', 'amount', 'date']
        return True
    
    def read_data(self, limit: int = None) -> List[Dict[str, str]]:
        """CSV-specific method."""
        if not self.is_connected:
            raise ConnectionError("Not connected to data source")
        
        # Simulate reading CSV data
        data = [
            {'id': '1', 'name': 'John', 'amount': '100.50', 'date': '2024-01-01'},
            {'id': '2', 'name': 'Jane', 'amount': '250.75', 'date': '2024-01-02'}
        ]
        
        if limit:
            data = data[:limit]
        
        self.records_processed += len(data)
        return data

# Child class for databases
class DatabaseSource(DataSource):
    """Specialized data source for databases."""
    
    def __init__(self, name: str, connection_string: str, table_name: str):
        super().__init__(name, connection_string)
        self.table_name = table_name
        self.query_cache = {}
    
    def connect(self) -> bool:
        """Override with database-specific connection."""
        super().connect()
        print(f"Establishing database connection pool")
        print(f"Setting default table to {self.table_name}")
        return True
    
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Database-specific method."""
        if not self.is_connected:
            raise ConnectionError("Database not connected")
        
        # Check cache first
        if query in self.query_cache:
            print(f"Returning cached result for query")
            return self.query_cache[query]
        
        # Simulate query execution
        print(f"Executing: {query}")
        result = [
            {'customer_id': 1, 'total_orders': 5, 'total_amount': 1250.00},
            {'customer_id': 2, 'total_orders': 3, 'total_amount': 750.50}
        ]
        
        # Cache the result
        self.query_cache[query] = result
        self.records_processed += len(result)
        return result

# Using inheritance
csv_source = CSVDataSource("Sales CSV", "/data/sales.csv")
db_source = DatabaseSource("Sales DB", "postgresql://localhost/sales", "orders")

# Both inherit connect() but with different behaviors
csv_source.connect()
db_source.connect()

# Use specialized methods
csv_data = csv_source.read_data(limit=1)
db_data = db_source.execute_query("SELECT customer_id, COUNT(*) FROM orders GROUP BY customer_id")

# Both inherit get_stats()
print(f"CSV stats: {csv_source.get_stats()}")
print(f"DB stats: {db_source.get_stats()}")

# Output: Establishing connection to Sales CSV...
# Output: Reading CSV headers from /data/sales.csv
# Output: Establishing connection to Sales DB...
# Output: Establishing database connection pool
# Output: Setting default table to orders
# Output: Executing: SELECT customer_id, COUNT(*) FROM orders GROUP BY customer_id
# Output: CSV stats: {'name': 'Sales CSV', 'connected': True, 'records_processed': 1}
# Output: DB stats: {'name': 'Sales DB', 'connected': True, 'records_processed': 2}
```

### Polymorphism

**What it is**: Polymorphism allows objects of different classes to be treated as objects of a common base class, while each maintains its own specific behavior.

**Why powerful**: 
- **Flexibility**: Write code that works with multiple types
- **Extensibility**: Add new types without changing existing code
- **Clean Architecture**: Depend on abstractions, not concrete implementations

```python
from typing import List, Protocol

# Protocol for polymorphic behavior (Python 3.8+)
class Processable(Protocol):
    def process(self, data: List[Any]) -> List[Any]:
        ...
    
    def get_name(self) -> str:
        ...

# Different processors with same interface
class NumberProcessor:
    def process(self, data: List[Any]) -> List[Any]:
        return [x * 2 for x in data if isinstance(x, (int, float))]
    
    def get_name(self) -> str:
        return "Number Processor"

class StringProcessor:
    def process(self, data: List[Any]) -> List[Any]:
        return [str(x).upper() for x in data if isinstance(x, str)]
    
    def get_name(self) -> str:
        return "String Processor"

class FilterProcessor:
    def __init__(self, condition):
        self.condition = condition
    
    def process(self, data: List[Any]) -> List[Any]:
        return [x for x in data if self.condition(x)]
    
    def get_name(self) -> str:
        return "Filter Processor"

# Polymorphic function - works with any processor
def run_data_pipeline(processors: List[Processable], data: List[Any]) -> List[Any]:
    """Run data through multiple processors polymorphically."""
    result = data
    
    for processor in processors:
        print(f"Running {processor.get_name()}...")
        result = processor.process(result)
        print(f"Result: {result}")
    
    return result

# Create different processor instances
processors = [
    FilterProcessor(lambda x: isinstance(x, (int, float, str))),  # Filter valid types
    NumberProcessor(),                                            # Process numbers
    StringProcessor()                                            # Process strings
]

# Mixed data
input_data = [1, 2, "hello", 3.5, "world", None, 4, "python"]

# Run polymorphic pipeline
final_result = run_data_pipeline(processors, input_data)
print(f"Final result: {final_result}")

# Output: Running Filter Processor...
# Output: Result: [1, 2, 'hello', 3.5, 'world', 4, 'python']
# Output: Running Number Processor...
# Output: Result: [2, 4, 7.0, 8]
# Output: Running String Processor...
# Output: Result: []
# Output: Final result: []
```

### Abstract Classes

**What they are**: Abstract classes define a common interface that subclasses must implement, ensuring consistent behavior across related classes.

**Why important**: 
- **Contract Enforcement**: Guarantee that subclasses implement required methods
- **Design Clarity**: Make intentions explicit in the code
- **Framework Building**: Create extensible architectures

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Any

# Abstract base class
class DataValidator(ABC):
    """Abstract base class for data validators."""
    
    def __init__(self, name: str):
        self.name = name
        self.validation_errors = []
    
    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Abstract method - must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def get_error_message(self) -> str:
        """Abstract method for error messages."""
        pass
    
    # Concrete method (shared by all subclasses)
    def reset_errors(self):
        """Clear validation errors."""
        self.validation_errors.clear()
    
    def has_errors(self) -> bool:
        """Check if there are validation errors."""
        return len(self.validation_errors) > 0

# Concrete implementations
class EmailValidator(DataValidator):
    def validate(self, data: str) -> bool:
        if not isinstance(data, str):
            self.validation_errors.append("Email must be a string")
            return False
        
        if "@" not in data or "." not in data:
            self.validation_errors.append("Invalid email format")
            return False
        
        return True
    
    def get_error_message(self) -> str:
        return f"Email validation failed: {', '.join(self.validation_errors)}"

class RangeValidator(DataValidator):
    def __init__(self, name: str, min_val: float, max_val: float):
        super().__init__(name)
        self.min_val = min_val
        self.max_val = max_val
    
    def validate(self, data: Any) -> bool:
        if not isinstance(data, (int, float)):
            self.validation_errors.append("Value must be numeric")
            return False
        
        if not (self.min_val <= data <= self.max_val):
            self.validation_errors.append(f"Value must be between {self.min_val} and {self.max_val}")
            return False
        
        return True
    
    def get_error_message(self) -> str:
        return f"Range validation failed: {', '.join(self.validation_errors)}"

# Validation framework using abstract classes
class DataValidationFramework:
    def __init__(self):
        self.validators: List[DataValidator] = []
    
    def add_validator(self, validator: DataValidator):
        self.validators.append(validator)
    
    def validate_record(self, record: Dict[str, Any]) -> Dict[str, List[str]]:
        errors = {}
        
        for validator in self.validators:
            validator.reset_errors()
            field_name = validator.name
            
            if field_name in record:
                is_valid = validator.validate(record[field_name])
                if not is_valid:
                    errors[field_name] = validator.validation_errors.copy()
        
        return errors

# Using the abstract class framework
framework = DataValidationFramework()
framework.add_validator(EmailValidator("email"))
framework.add_validator(RangeValidator("age", 0, 120))
framework.add_validator(RangeValidator("salary", 0, 1000000))

# Test data
test_records = [
    {"email": "john@example.com", "age": 30, "salary": 50000},
    {"email": "invalid-email", "age": -5, "salary": 2000000},
    {"email": "jane@company.org", "age": 25, "salary": 75000}
]

for i, record in enumerate(test_records):
    errors = framework.validate_record(record)
    if errors:
        print(f"Record {i+1} validation errors: {errors}")
    else:
        print(f"Record {i+1} is valid")

# Output: Record 1 is valid
# Output: Record 2 validation errors: {'email': ['Invalid email format'], 'age': ['Value must be between 0 and 120'], 'salary': ['Value must be between 0 and 1000000']}
# Output: Record 3 is valid
```

## 4. Error Handling
**What it is**: A systematic approach to anticipating, catching, and handling errors that occur during program execution.

**Why important**: Data pipelines often deal with unreliable external systems, malformed data, and network issues. Proper error handling ensures pipelines are resilient, can recover from failures, and provide meaningful feedback for debugging.

**When to use**:
- Always in production data pipelines
- When dealing with external APIs or databases
- File I/O operations
- Data validation and transformation steps

**Try-Except Patterns**:
```python
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_data_processing(data, processor_func):
    """Process data with comprehensive error handling."""
    try:
        # Validate input
        if not data:
            raise ValueError("Input data is empty")
        
        # Process data
        result = processor_func(data)
        
        # Validate output
        if not result:
            logger.warning("Processing returned empty result")
        
        return result
        
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise
    except FileNotFoundError as fe:
        logger.error(f"File not found: {fe}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during processing: {e}")
        raise
    finally:
        # Cleanup code always runs
        logger.info("Processing attempt completed")

# Custom exceptions
class DataValidationError(Exception):
    """Raised when data validation fails."""
    def __init__(self, message, invalid_records=None):
        super().__init__(message)
        self.invalid_records = invalid_records or []

def validate_data(data):
    invalid_records = []
    for i, record in enumerate(data):
        if not isinstance(record, dict) or 'id' not in record:
            invalid_records.append(i)
    
    if invalid_records:
        raise DataValidationError(
            f"Found {len(invalid_records)} invalid records",
            invalid_records
        )
```

## 5. File I/O and Data Formats
**What it is**: Operations for reading from and writing to files in various formats like text, CSV, JSON, and binary formats.

**Why important**: Data engineers constantly work with files - reading source data, writing processed results, and handling configuration files. Efficient file I/O is crucial for performance, especially with large datasets.

**When to use**:
- Reading source data files (CSV, JSON, XML)
- Writing processed data to storage
- Configuration management
- Logging and audit trails
- Batch processing workflows

**Text Files**:
```python
# Reading files
def read_file_safely(file_path: str, encoding: str = 'utf-8'):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return file.read()
    except UnicodeDecodeError:
        # Fallback to different encoding
        with open(file_path, 'r', encoding='latin-1') as file:
            return file.read()

# Writing files
def write_data_to_file(data: list, file_path: str):
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in data:
            file.write(f"{item}\n")

# Processing large files line by line
def process_large_file(file_path: str, processor_func):
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):
            try:
                processed = processor_func(line.strip())
                yield processed
            except Exception as e:
                print(f"Error processing line {line_num}: {e}")
```

**JSON Operations**:
```python
import json
from datetime import datetime

# Custom JSON encoder for complex types
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def save_to_json(data, file_path: str):
    with open(file_path, 'w') as file:
        json.dump(data, file, cls=DateTimeEncoder, indent=2)

def load_from_json(file_path: str):
    with open(file_path, 'r') as file:
        return json.load(file)

# Streaming JSON for large files
import ijson

def process_large_json(file_path: str):
    with open(file_path, 'rb') as file:
        # Parse JSON objects one by one
        objects = ijson.items(file, 'item')
        for obj in objects:
            yield obj
```

## 6. Generators and Iterators
**What they are**: Generators are functions that yield values one at a time, creating iterators that produce items on-demand rather than storing them all in memory.

**Why important**: Essential for processing large datasets that don't fit in memory. Generators enable streaming data processing, reduce memory usage, and improve performance in data pipelines.

**When to use**:
- Processing large files line by line
- Streaming data from APIs
- ETL pipelines with large datasets
- Real-time data processing
- Memory-constrained environments

**Generator Functions**:
```python
def read_csv_chunks(file_path: str, chunk_size: int = 1000):
    """Read CSV file in chunks to save memory."""
    import csv
    
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        chunk = []
        
        for row in reader:
            chunk.append(row)
            
            if len(chunk) >= chunk_size:
                yield chunk
                chunk = []
        
        # Yield remaining records
        if chunk:
            yield chunk

def fibonacci_generator(n: int):
    """Generate Fibonacci sequence up to n numbers."""
    a, b = 0, 1
    count = 0
    
    while count < n:
        yield a
        a, b = b, a + b
        count += 1

# Usage
for chunk in read_csv_chunks('large_file.csv', chunk_size=500):
    process_chunk(chunk)
```

**Iterator Protocol**:
```python
class DataBatch:
    """Custom iterator for batch processing."""
    
    def __init__(self, data: list, batch_size: int):
        self.data = data
        self.batch_size = batch_size
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration
        
        batch = self.data[self.index:self.index + self.batch_size]
        self.index += self.batch_size
        return batch

# Usage
data = list(range(100))
for batch in DataBatch(data, batch_size=10):
    print(f"Processing batch of {len(batch)} items")
```

## 7. Context Managers
**What they are**: Objects that define runtime context for executing code blocks, ensuring proper resource acquisition and cleanup.

**Why important**: Critical for managing resources like file handles, database connections, and network connections. They guarantee cleanup even when errors occur, preventing resource leaks in long-running data pipelines.

**When to use**:
- File operations
- Database connections
- Network connections
- Temporary resource allocation
- Transaction management
- Timing operations

**Built-in Context Managers**:
```python
# File handling
with open('data.txt', 'r') as file:
    content = file.read()
# File automatically closed

# Database connections
import sqlite3
with sqlite3.connect('database.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
# Connection automatically closed
```

**Custom Context Managers**:
```python
from contextlib import contextmanager
import time

class DatabaseTransaction:
    """Context manager for database transactions."""
    
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

@contextmanager
def timing_context(operation_name: str):
    """Context manager for timing operations."""
    start_time = time.time()
    print(f"Starting {operation_name}")
    
    try:
        yield
    finally:
        end_time = time.time()
        print(f"{operation_name} completed in {end_time - start_time:.2f} seconds")

# Usage
with timing_context("Data Processing"):
    # Your data processing code here
    time.sleep(2)
```

## 8. Concurrency and Parallelism
**What they are**: Techniques for executing multiple tasks simultaneously. Concurrency handles multiple tasks at once (not necessarily simultaneously), while parallelism executes tasks simultaneously on multiple cores.

**Why important**: Data processing often involves I/O-bound operations (API calls, file reads) and CPU-bound tasks (data transformations). Proper use of concurrency and parallelism can dramatically improve pipeline performance.

**When to use**:
- Threading for I/O-bound tasks (API calls, file operations)
- Multiprocessing for CPU-bound tasks (data transformations)
- Async/await for high-concurrency I/O operations
- Parallel data processing and ETL operations

**Threading for I/O-bound Tasks**:
```python
import threading
import concurrent.futures
import requests

def fetch_url(url: str):
    """Fetch data from URL."""
    response = requests.get(url)
    return response.status_code, len(response.content)

def parallel_fetch(urls: list, max_workers: int = 5):
    """Fetch multiple URLs in parallel."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}
        
        # Collect results
        results = {}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                status_code, content_length = future.result()
                results[url] = {'status': status_code, 'size': content_length}
            except Exception as e:
                results[url] = {'error': str(e)}
        
        return results
```

**Multiprocessing for CPU-bound Tasks**:
```python
import multiprocessing
from multiprocessing import Pool
import math

def cpu_intensive_task(n: int):
    """CPU-intensive calculation."""
    result = 0
    for i in range(n):
        result += math.sqrt(i)
    return result

def parallel_processing(data: list, num_processes: int = None):
    """Process data in parallel using multiple processes."""
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()
    
    with Pool(processes=num_processes) as pool:
        results = pool.map(cpu_intensive_task, data)
    
    return results

# Usage
if __name__ == '__main__':
    data = [100000, 200000, 300000, 400000]
    results = parallel_processing(data)
    print(f"Results: {results}")
```

## 9. Type Hints and Documentation
**What they are**: Type hints provide static type information to make code more readable and enable better tooling. Documentation includes docstrings, comments, and external documentation.

**Why important**: In data engineering, code is often complex and maintained by teams. Type hints catch errors early, improve IDE support, and make code self-documenting. Good documentation is essential for maintaining data pipelines and onboarding team members.

**When to use**:
- All production code should have type hints
- Public APIs and functions need comprehensive documentation
- Complex data transformations require clear explanations
- Team environments where code is shared

**Type Hints**:
```python
from typing import List, Dict, Optional, Union, Callable, Any
from dataclasses import dataclass

def process_records(
    records: List[Dict[str, Any]], 
    filter_func: Optional[Callable[[Dict], bool]] = None,
    batch_size: int = 1000
) -> List[Dict[str, Any]]:
    """
    Process a list of records with optional filtering.
    
    Args:
        records: List of record dictionaries
        filter_func: Optional function to filter records
        batch_size: Number of records to process at once
    
    Returns:
        List of processed records
    
    Raises:
        ValueError: If records list is empty
    """
    if not records:
        raise ValueError("Records list cannot be empty")
    
    if filter_func:
        records = [r for r in records if filter_func(r)]
    
    # Process in batches
    processed = []
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        processed.extend(batch)
    
    return processed

@dataclass
class DataConfig:
    """Configuration for data processing."""
    source_path: str
    output_path: str
    batch_size: int = 1000
    enable_validation: bool = True
    retry_count: int = 3
```

## 10. Testing
**What it is**: The practice of writing code to verify that your application code works correctly under various conditions.

**Why important**: Data pipelines process critical business data, and bugs can have serious consequences. Testing ensures data quality, catches regressions, and provides confidence when making changes to production systems.

**When to use**:
- Unit tests for individual functions and classes
- Integration tests for data pipeline components
- End-to-end tests for complete workflows
- Data validation tests for quality assurance
- Performance tests for optimization

**Unit Testing**:
```python
import unittest
from unittest.mock import patch, MagicMock

class TestDataProcessor(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_data = [
            {'id': 1, 'name': 'Alice', 'age': 30},
            {'id': 2, 'name': 'Bob', 'age': 25},
            {'id': 3, 'name': 'Charlie', 'age': 35}
        ]
    
    def test_filter_by_age(self):
        """Test age filtering functionality."""
        result = filter_by_age(self.sample_data, min_age=30)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(person['age'] >= 30 for person in result))
    
    def test_empty_data_handling(self):
        """Test handling of empty data."""
        with self.assertRaises(ValueError):
            process_records([])
    
    @patch('requests.get')
    def test_api_call(self, mock_get):
        """Test API call with mocking."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'success'}
        mock_get.return_value = mock_response
        
        # Test the function
        result = fetch_data_from_api('http://example.com')
        self.assertEqual(result['status'], 'success')
        mock_get.assert_called_once_with('http://example.com')

if __name__ == '__main__':
    unittest.main()
```

**Pytest (Alternative Testing Framework)**:
```python
import pytest
from unittest.mock import patch

@pytest.fixture
def sample_data():
    """Test data fixture."""
    return [
        {'id': 1, 'name': 'Alice', 'age': 30},
        {'id': 2, 'name': 'Bob', 'age': 25}
    ]

def test_data_processing(sample_data):
    """Test data processing with fixture."""
    result = process_data(sample_data)
    assert len(result) == 2
    assert all('processed' in record for record in result)

@pytest.mark.parametrize("age,expected_count", [
    (25, 2),
    (30, 1),
    (40, 0)
])
def test_age_filter_parametrized(sample_data, age, expected_count):
    """Parametrized test for age filtering."""
    result = filter_by_age(sample_data, min_age=age)
    assert len(result) == expected_count
```