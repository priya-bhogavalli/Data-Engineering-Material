# Design Patterns Best Practices

## General Principles

### 1. SOLID Principles Integration
Design patterns should support SOLID principles:

**Single Responsibility Principle (SRP)**:
```python
# Good: Each class has one responsibility
class DataExtractor:
    def extract(self, source): pass

class DataValidator:
    def validate(self, data): pass

class DataTransformer:
    def transform(self, data): pass

# Bad: One class doing everything
class DataProcessor:
    def extract_and_validate_and_transform(self, source): pass
```

**Open/Closed Principle (OCP)**:
```python
# Strategy pattern supports OCP
class DataProcessor:
    def __init__(self, strategy):
        self._strategy = strategy
    
    def process(self, data):
        return self._strategy.process(data)

# Adding new strategies without modifying existing code
class NewProcessingStrategy:
    def process(self, data):
        return "new processing logic"
```

### 2. Favor Composition Over Inheritance
```python
# Good: Composition with Strategy pattern
class DataPipeline:
    def __init__(self, extractor, transformer, loader):
        self._extractor = extractor
        self._transformer = transformer
        self._loader = loader

# Avoid: Deep inheritance hierarchies
class CSVToJSONToDBPipeline(CSVPipeline, JSONPipeline, DBPipeline):
    pass  # Complex inheritance
```

### 3. Program to Interfaces, Not Implementations
```python
from abc import ABC, abstractmethod

# Define interfaces
class DataSource(ABC):
    @abstractmethod
    def read_data(self): pass

class FileDataSource(DataSource):
    def read_data(self):
        return "file data"

class DatabaseDataSource(DataSource):
    def read_data(self):
        return "database data"

# Client code works with interface
def process_data(source: DataSource):
    data = source.read_data()
    return f"Processing: {data}"
```

## Pattern-Specific Best Practices

### Creational Patterns

#### Singleton Pattern
**Best Practices**:
```python
import threading
from typing import Optional

class DatabaseConnection:
    _instance: Optional['DatabaseConnection'] = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self._connection = self._create_connection()
            self.initialized = True
    
    def _create_connection(self):
        # Expensive connection creation
        return "database_connection"

# Testing-friendly singleton
class ConfigurableSingleton:
    _instance = None
    
    @classmethod
    def get_instance(cls, config=None):
        if cls._instance is None or config:
            cls._instance = cls(config)
        return cls._instance
```

**Avoid**:
- Global state that makes testing difficult
- Singletons that do too much (violate SRP)
- Hard-coded dependencies

#### Factory Pattern
**Best Practices**:
```python
from typing import Dict, Type
from abc import ABC, abstractmethod

class DataProcessor(ABC):
    @abstractmethod
    def process(self, data): pass

class ProcessorFactory:
    _processors: Dict[str, Type[DataProcessor]] = {}
    
    @classmethod
    def register(cls, name: str, processor_class: Type[DataProcessor]):
        cls._processors[name] = processor_class
    
    @classmethod
    def create(cls, processor_type: str, **kwargs) -> DataProcessor:
        if processor_type not in cls._processors:
            raise ValueError(f"Unknown processor type: {processor_type}")
        return cls._processors[processor_type](**kwargs)

# Registration decorator
def processor(name: str):
    def decorator(cls):
        ProcessorFactory.register(name, cls)
        return cls
    return decorator

@processor("csv")
class CSVProcessor(DataProcessor):
    def process(self, data):
        return f"Processing CSV: {data}"
```

**Avoid**:
- Large if-elif chains in factory methods
- Factories that create unrelated objects
- Hard-coded object creation logic

#### Builder Pattern
**Best Practices**:
```python
from typing import Optional, List

class DataPipeline:
    def __init__(self):
        self.source: Optional[str] = None
        self.transformations: List[str] = []
        self.destination: Optional[str] = None
        self.config: dict = {}

class DataPipelineBuilder:
    def __init__(self):
        self._pipeline = DataPipeline()
    
    def source(self, source: str):
        self._pipeline.source = source
        return self
    
    def transform(self, transformation: str):
        self._pipeline.transformations.append(transformation)
        return self
    
    def destination(self, destination: str):
        self._pipeline.destination = destination
        return self
    
    def config(self, **kwargs):
        self._pipeline.config.update(kwargs)
        return self
    
    def build(self) -> DataPipeline:
        self._validate()
        pipeline = self._pipeline
        self._pipeline = DataPipeline()  # Reset for next build
        return pipeline
    
    def _validate(self):
        if not self._pipeline.source:
            raise ValueError("Source is required")
        if not self._pipeline.destination:
            raise ValueError("Destination is required")

# Usage
pipeline = (DataPipelineBuilder()
           .source("database")
           .transform("clean")
           .transform("validate")
           .destination("warehouse")
           .config(batch_size=1000, timeout=30)
           .build())
```

### Structural Patterns

#### Decorator Pattern
**Best Practices**:
```python
from functools import wraps
import time
import logging

# Function decorator approach
def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logging.info(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper

# Class decorator approach
class LoggingDecorator:
    def __init__(self, component):
        self._component = component
        self._logger = logging.getLogger(component.__class__.__name__)
    
    def __getattr__(self, name):
        attr = getattr(self._component, name)
        if callable(attr):
            return self._create_logged_method(attr, name)
        return attr
    
    def _create_logged_method(self, method, method_name):
        def logged_method(*args, **kwargs):
            self._logger.info(f"Calling {method_name}")
            try:
                result = method(*args, **kwargs)
                self._logger.info(f"{method_name} completed successfully")
                return result
            except Exception as e:
                self._logger.error(f"{method_name} failed: {e}")
                raise
        return logged_method

# Stackable decorators
@timing_decorator
@logging_decorator
def process_data(data):
    return f"Processed: {data}"
```

#### Adapter Pattern
**Best Practices**:
```python
# Object adapter (composition)
class LegacyDataAdapter:
    def __init__(self, legacy_system):
        self._legacy_system = legacy_system
    
    def get_data(self):
        # Adapt legacy interface to modern interface
        legacy_data = self._legacy_system.retrieve_legacy_data()
        return self._convert_to_modern_format(legacy_data)
    
    def _convert_to_modern_format(self, legacy_data):
        # Conversion logic
        return {"data": legacy_data, "format": "modern"}

# Two-way adapter
class BidirectionalAdapter:
    def __init__(self, system_a, system_b):
        self._system_a = system_a
        self._system_b = system_b
    
    def a_to_b(self, data):
        return self._system_b.process(self._convert_a_to_b(data))
    
    def b_to_a(self, data):
        return self._system_a.process(self._convert_b_to_a(data))
```

### Behavioral Patterns

#### Observer Pattern
**Best Practices**:
```python
from typing import List, Protocol
from abc import ABC, abstractmethod

class Observer(Protocol):
    def update(self, event): pass

class Subject:
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event):
        # Create a copy to avoid issues if observers modify the list
        for observer in self._observers[:]:
            try:
                observer.update(event)
            except Exception as e:
                # Log error but continue notifying other observers
                logging.error(f"Observer {observer} failed: {e}")

# Event-driven approach
class EventBus:
    def __init__(self):
        self._handlers = {}
    
    def subscribe(self, event_type: str, handler):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
    
    def publish(self, event_type: str, event_data):
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                try:
                    handler(event_data)
                except Exception as e:
                    logging.error(f"Handler failed for {event_type}: {e}")
```

#### Strategy Pattern
**Best Practices**:
```python
from typing import Dict, Type
from abc import ABC, abstractmethod

class ProcessingStrategy(ABC):
    @abstractmethod
    def process(self, data): pass

class StrategyRegistry:
    _strategies: Dict[str, Type[ProcessingStrategy]] = {}
    
    @classmethod
    def register(cls, name: str, strategy_class: Type[ProcessingStrategy]):
        cls._strategies[name] = strategy_class
    
    @classmethod
    def get_strategy(cls, name: str) -> ProcessingStrategy:
        if name not in cls._strategies:
            raise ValueError(f"Unknown strategy: {name}")
        return cls._strategies[name]()

# Context with strategy validation
class DataProcessor:
    def __init__(self, strategy_name: str):
        self._strategy = StrategyRegistry.get_strategy(strategy_name)
    
    def process(self, data):
        if not data:
            raise ValueError("Data cannot be empty")
        return self._strategy.process(data)
    
    def change_strategy(self, strategy_name: str):
        self._strategy = StrategyRegistry.get_strategy(strategy_name)

# Strategy with configuration
class ConfigurableStrategy(ProcessingStrategy):
    def __init__(self, **config):
        self.config = config
    
    def process(self, data):
        # Use configuration in processing
        return f"Processing with config: {self.config}"
```

## Performance Best Practices

### 1. Lazy Initialization
```python
class ExpensiveResource:
    def __init__(self):
        self._resource = None
    
    @property
    def resource(self):
        if self._resource is None:
            self._resource = self._create_expensive_resource()
        return self._resource
    
    def _create_expensive_resource(self):
        # Expensive initialization
        return "expensive_resource"
```

### 2. Object Pooling
```python
from queue import Queue
import threading

class ConnectionPool:
    def __init__(self, max_connections=10):
        self._pool = Queue(maxsize=max_connections)
        self._lock = threading.Lock()
        
        # Pre-populate pool
        for _ in range(max_connections):
            self._pool.put(self._create_connection())
    
    def get_connection(self):
        return self._pool.get()
    
    def return_connection(self, connection):
        self._pool.put(connection)
    
    def _create_connection(self):
        return "database_connection"

# Context manager for automatic return
from contextlib import contextmanager

@contextmanager
def get_connection(pool):
    connection = pool.get_connection()
    try:
        yield connection
    finally:
        pool.return_connection(connection)
```

### 3. Flyweight Optimization
```python
class DataProcessorFlyweight:
    def __init__(self, algorithm_type):
        self._algorithm_type = algorithm_type
        # Store only intrinsic state
    
    def process(self, extrinsic_data):
        # Use extrinsic data passed from context
        return f"Processing {extrinsic_data} with {self._algorithm_type}"

class FlyweightFactory:
    _flyweights = {}
    
    @classmethod
    def get_flyweight(cls, algorithm_type):
        if algorithm_type not in cls._flyweights:
            cls._flyweights[algorithm_type] = DataProcessorFlyweight(algorithm_type)
        return cls._flyweights[algorithm_type]
    
    @classmethod
    def get_flyweight_count(cls):
        return len(cls._flyweights)
```

## Testing Best Practices

### 1. Dependency Injection for Testability
```python
class DataService:
    def __init__(self, repository, validator=None):
        self._repository = repository
        self._validator = validator or DefaultValidator()
    
    def save_data(self, data):
        if not self._validator.validate(data):
            raise ValueError("Invalid data")
        return self._repository.save(data)

# Easy to test with mocks
def test_data_service():
    mock_repository = Mock()
    mock_validator = Mock()
    mock_validator.validate.return_value = True
    
    service = DataService(mock_repository, mock_validator)
    service.save_data("test_data")
    
    mock_validator.validate.assert_called_once_with("test_data")
    mock_repository.save.assert_called_once_with("test_data")
```

### 2. Factory for Test Objects
```python
class TestDataFactory:
    @staticmethod
    def create_user(name="test_user", email="test@example.com"):
        return User(name=name, email=email)
    
    @staticmethod
    def create_pipeline(source="test_source", destination="test_dest"):
        return DataPipeline(source=source, destination=destination)

# Builder for complex test objects
class TestPipelineBuilder:
    def __init__(self):
        self._pipeline = DataPipeline()
    
    def with_source(self, source):
        self._pipeline.source = source
        return self
    
    def with_error_handling(self):
        self._pipeline.error_handler = MockErrorHandler()
        return self
    
    def build(self):
        return self._pipeline
```

## Common Anti-Patterns and How to Avoid Them

### 1. God Object
**Problem**: One class doing too much
```python
# Bad
class DataProcessor:
    def extract_from_database(self): pass
    def extract_from_file(self): pass
    def validate_data(self): pass
    def transform_data(self): pass
    def load_to_warehouse(self): pass
    def send_notifications(self): pass
    def generate_reports(self): pass
```

**Solution**: Use multiple patterns
```python
# Good
class DataExtractor:
    def extract(self, source): pass

class DataValidator:
    def validate(self, data): pass

class DataTransformer:
    def transform(self, data): pass

class DataPipeline:
    def __init__(self, extractor, validator, transformer):
        self._extractor = extractor
        self._validator = validator
        self._transformer = transformer
```

### 2. Anemic Domain Model
**Problem**: Objects with no behavior, only data
```python
# Bad
class Order:
    def __init__(self):
        self.items = []
        self.total = 0
        self.status = "pending"

class OrderService:
    def calculate_total(self, order): pass
    def validate_order(self, order): pass
    def process_order(self, order): pass
```

**Solution**: Rich domain objects
```python
# Good
class Order:
    def __init__(self):
        self._items = []
        self._status = OrderStatus.PENDING
    
    def add_item(self, item):
        self._items.append(item)
    
    def calculate_total(self):
        return sum(item.price for item in self._items)
    
    def process(self):
        if self._is_valid():
            self._status = OrderStatus.PROCESSING
```

### 3. Overuse of Patterns
**Problem**: Using patterns where simple solutions suffice
```python
# Overkill for simple case
class SimpleCalculatorFactory:
    def create_calculator(self, type):
        if type == "basic":
            return BasicCalculator()

# Simple solution is better
def add(a, b):
    return a + b
```

## Documentation and Maintenance

### 1. Pattern Documentation
```python
class DataProcessor:
    """
    Implements the Strategy pattern for pluggable data processing algorithms.
    
    This class acts as the Context in the Strategy pattern, allowing
    different processing algorithms to be used interchangeably.
    
    Example:
        processor = DataProcessor(CleaningStrategy())
        result = processor.process(data)
    """
    
    def __init__(self, strategy: ProcessingStrategy):
        self._strategy = strategy
    
    def process(self, data):
        """Process data using the configured strategy."""
        return self._strategy.process(data)
```

### 2. Pattern Evolution
```python
# Version 1: Simple factory
class ProcessorFactory:
    @staticmethod
    def create(type):
        if type == "csv":
            return CSVProcessor()

# Version 2: Registry-based factory (more extensible)
class ProcessorFactory:
    _processors = {}
    
    @classmethod
    def register(cls, name, processor_class):
        cls._processors[name] = processor_class
    
    @classmethod
    def create(cls, name):
        return cls._processors[name]()
```

### 3. Monitoring and Metrics
```python
class MonitoredProcessor:
    def __init__(self, processor, metrics_collector):
        self._processor = processor
        self._metrics = metrics_collector
    
    def process(self, data):
        start_time = time.time()
        try:
            result = self._processor.process(data)
            self._metrics.record_success(time.time() - start_time)
            return result
        except Exception as e:
            self._metrics.record_failure(e)
            raise
```

Remember: Design patterns are tools to solve specific problems. Use them when they add value, not just because they exist. Always consider the trade-offs between flexibility, complexity, and maintainability.