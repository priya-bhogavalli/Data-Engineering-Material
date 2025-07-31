# Design Patterns Interview Questions

## Basic Level Questions (1-5 years experience)

### 1. What are Design Patterns and why are they important?
**Answer**: Design patterns are reusable solutions to commonly occurring problems in software design. They represent best practices and provide a common vocabulary for developers.

**Key Benefits**:
- Code reusability and maintainability
- Common vocabulary for development teams
- Proven solutions to recurring problems
- Improved code organization and structure

### 2. Explain the Singleton Pattern with a practical example
**Answer**: Singleton ensures a class has only one instance and provides global access to it.

```python
class DatabaseConnection:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.connection = self._create_connection()
            self.initialized = True
```

### 3. What is the Factory Pattern and when would you use it?
**Answer**: Factory pattern creates objects without specifying their exact classes, delegating instantiation to subclasses.

```python
class DataProcessorFactory:
    @staticmethod
    def create_processor(data_type):
        if data_type == "csv":
            return CSVProcessor()
        elif data_type == "json":
            return JSONProcessor()
        elif data_type == "xml":
            return XMLProcessor()
        else:
            raise ValueError(f"Unknown data type: {data_type}")
```

### 4. Explain the Observer Pattern
**Answer**: Observer pattern defines a one-to-many dependency between objects so that when one object changes state, all dependents are notified.

```python
class DataPipeline:
    def __init__(self):
        self._observers = []
        self._status = "idle"
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def notify(self):
        for observer in self._observers:
            observer.update(self._status)
    
    def set_status(self, status):
        self._status = status
        self.notify()
```

### 5. What is the Strategy Pattern?
**Answer**: Strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable.

```python
class DataValidator:
    def __init__(self, strategy):
        self._strategy = strategy
    
    def validate(self, data):
        return self._strategy.validate(data)

class EmailValidationStrategy:
    def validate(self, data):
        return "@" in data and "." in data

class PhoneValidationStrategy:
    def validate(self, data):
        return data.isdigit() and len(data) == 10
```

## Intermediate Level Questions (3-7 years experience)

### 6. Explain the Decorator Pattern and its use in data processing
**Answer**: Decorator pattern allows behavior to be added to objects dynamically without altering their structure.

```python
class DataProcessor:
    def process(self, data):
        return data

class LoggingDecorator:
    def __init__(self, processor):
        self._processor = processor
    
    def process(self, data):
        print(f"Processing {len(data)} records")
        result = self._processor.process(data)
        print("Processing completed")
        return result

class ValidationDecorator:
    def __init__(self, processor):
        self._processor = processor
    
    def process(self, data):
        if not data:
            raise ValueError("Empty data")
        return self._processor.process(data)
```

### 7. How would you implement the Command Pattern for ETL operations?
**Answer**: Command pattern encapsulates requests as objects, allowing you to parameterize clients with different requests.

```python
class ETLCommand:
    def execute(self):
        pass
    
    def undo(self):
        pass

class ExtractCommand(ETLCommand):
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
    
    def execute(self):
        data = self.source.extract()
        self.destination.store(data)
        return data

class ETLInvoker:
    def __init__(self):
        self._commands = []
    
    def add_command(self, command):
        self._commands.append(command)
    
    def execute_all(self):
        results = []
        for command in self._commands:
            results.append(command.execute())
        return results
```

### 8. Explain the Builder Pattern for complex data pipeline construction
**Answer**: Builder pattern constructs complex objects step by step, allowing different representations of the same construction process.

```python
class DataPipelineBuilder:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self._pipeline = DataPipeline()
        return self
    
    def add_source(self, source):
        self._pipeline.source = source
        return self
    
    def add_transformation(self, transformation):
        self._pipeline.transformations.append(transformation)
        return self
    
    def add_destination(self, destination):
        self._pipeline.destination = destination
        return self
    
    def build(self):
        pipeline = self._pipeline
        self.reset()
        return pipeline

# Usage
pipeline = (DataPipelineBuilder()
           .add_source(CSVSource("data.csv"))
           .add_transformation(CleaningTransformation())
           .add_transformation(ValidationTransformation())
           .add_destination(DatabaseDestination())
           .build())
```

### 9. What is the Adapter Pattern and how is it useful in data integration?
**Answer**: Adapter pattern allows incompatible interfaces to work together by wrapping an existing class with a new interface.

```python
class LegacyDataSource:
    def get_legacy_data(self):
        return "legacy,data,format"

class ModernDataProcessor:
    def process(self, data_dict):
        return {k: v.upper() for k, v in data_dict.items()}

class LegacyDataAdapter:
    def __init__(self, legacy_source):
        self._legacy_source = legacy_source
    
    def get_data(self):
        legacy_data = self._legacy_source.get_legacy_data()
        # Convert legacy format to modern format
        fields = legacy_data.split(',')
        return {f"field_{i}": field for i, field in enumerate(fields)}
```

### 10. How would you use the Template Method Pattern for ETL processes?
**Answer**: Template Method defines the skeleton of an algorithm in a base class, letting subclasses override specific steps.

```python
class ETLTemplate:
    def execute(self):
        data = self.extract()
        transformed_data = self.transform(data)
        self.load(transformed_data)
    
    def extract(self):
        raise NotImplementedError
    
    def transform(self, data):
        raise NotImplementedError
    
    def load(self, data):
        raise NotImplementedError

class CSVToDBETL(ETLTemplate):
    def extract(self):
        return pd.read_csv("source.csv")
    
    def transform(self, data):
        return data.dropna().reset_index(drop=True)
    
    def load(self, data):
        data.to_sql("target_table", connection, if_exists="replace")
```

## Advanced Level Questions (5+ years experience)

### 11. Explain the Composite Pattern for hierarchical data structures
**Answer**: Composite pattern composes objects into tree structures to represent part-whole hierarchies.

```python
class DataComponent:
    def process(self):
        pass
    
    def add(self, component):
        pass
    
    def remove(self, component):
        pass

class DataLeaf(DataComponent):
    def __init__(self, data):
        self._data = data
    
    def process(self):
        return f"Processing {self._data}"

class DataComposite(DataComponent):
    def __init__(self):
        self._children = []
    
    def add(self, component):
        self._children.append(component)
    
    def remove(self, component):
        self._children.remove(component)
    
    def process(self):
        results = []
        for child in self._children:
            results.append(child.process())
        return results
```

### 12. How would you implement the Chain of Responsibility Pattern for data validation?
**Answer**: Chain of Responsibility passes requests along a chain of handlers until one handles it.

```python
class ValidationHandler:
    def __init__(self):
        self._next_handler = None
    
    def set_next(self, handler):
        self._next_handler = handler
        return handler
    
    def handle(self, data):
        if self._can_handle(data):
            return self._process(data)
        elif self._next_handler:
            return self._next_handler.handle(data)
        else:
            raise ValueError("No handler found for data")
    
    def _can_handle(self, data):
        raise NotImplementedError
    
    def _process(self, data):
        raise NotImplementedError

class NullCheckHandler(ValidationHandler):
    def _can_handle(self, data):
        return data is not None
    
    def _process(self, data):
        if any(pd.isna(data)):
            raise ValueError("Null values found")
        return data

class TypeCheckHandler(ValidationHandler):
    def _can_handle(self, data):
        return hasattr(data, 'dtype')
    
    def _process(self, data):
        if data.dtype == 'object':
            raise ValueError("Invalid data type")
        return data
```

### 13. Explain the State Pattern for data pipeline state management
**Answer**: State pattern allows an object to alter its behavior when its internal state changes.

```python
class PipelineState:
    def start(self, pipeline):
        pass
    
    def pause(self, pipeline):
        pass
    
    def stop(self, pipeline):
        pass

class IdleState(PipelineState):
    def start(self, pipeline):
        print("Starting pipeline")
        pipeline.set_state(RunningState())

class RunningState(PipelineState):
    def pause(self, pipeline):
        print("Pausing pipeline")
        pipeline.set_state(PausedState())
    
    def stop(self, pipeline):
        print("Stopping pipeline")
        pipeline.set_state(IdleState())

class DataPipeline:
    def __init__(self):
        self._state = IdleState()
    
    def set_state(self, state):
        self._state = state
    
    def start(self):
        self._state.start(self)
```

### 14. How would you use the Proxy Pattern for data access control?
**Answer**: Proxy pattern provides a placeholder/surrogate for another object to control access to it.

```python
class DataAccess:
    def read_data(self, table):
        pass

class DatabaseAccess(DataAccess):
    def read_data(self, table):
        return f"Reading from {table}"

class SecureDataProxy(DataAccess):
    def __init__(self, real_access, user_permissions):
        self._real_access = real_access
        self._permissions = user_permissions
    
    def read_data(self, table):
        if self._check_permission(table):
            return self._real_access.read_data(table)
        else:
            raise PermissionError(f"Access denied to {table}")
    
    def _check_permission(self, table):
        return table in self._permissions
```

### 15. Explain the Facade Pattern for complex data processing systems
**Answer**: Facade pattern provides a simplified interface to a complex subsystem.

```python
class DataProcessingFacade:
    def __init__(self):
        self._extractor = DataExtractor()
        self._transformer = DataTransformer()
        self._validator = DataValidator()
        self._loader = DataLoader()
    
    def process_data(self, source, destination):
        # Simplified interface for complex operations
        try:
            data = self._extractor.extract(source)
            cleaned_data = self._transformer.clean(data)
            validated_data = self._validator.validate(cleaned_data)
            transformed_data = self._transformer.transform(validated_data)
            self._loader.load(transformed_data, destination)
            return "Processing completed successfully"
        except Exception as e:
            return f"Processing failed: {str(e)}"
```

### 16. How would you implement the Memento Pattern for pipeline state recovery?
**Answer**: Memento pattern captures and externalizes an object's internal state for later restoration.

```python
class PipelineMemento:
    def __init__(self, state, processed_records, current_step):
        self._state = state
        self._processed_records = processed_records
        self._current_step = current_step
    
    def get_state(self):
        return self._state, self._processed_records, self._current_step

class DataPipeline:
    def __init__(self):
        self._state = "idle"
        self._processed_records = 0
        self._current_step = 0
    
    def create_memento(self):
        return PipelineMemento(self._state, self._processed_records, self._current_step)
    
    def restore_from_memento(self, memento):
        self._state, self._processed_records, self._current_step = memento.get_state()

class PipelineCaretaker:
    def __init__(self):
        self._mementos = []
    
    def save_checkpoint(self, pipeline):
        self._mementos.append(pipeline.create_memento())
    
    def restore_checkpoint(self, pipeline, checkpoint_index):
        if 0 <= checkpoint_index < len(self._mementos):
            pipeline.restore_from_memento(self._mementos[checkpoint_index])
```

### 17. Explain the Visitor Pattern for data structure traversal
**Answer**: Visitor pattern separates algorithms from the objects on which they operate.

```python
class DataElement:
    def accept(self, visitor):
        pass

class CSVData(DataElement):
    def __init__(self, data):
        self.data = data
    
    def accept(self, visitor):
        return visitor.visit_csv(self)

class JSONData(DataElement):
    def __init__(self, data):
        self.data = data
    
    def accept(self, visitor):
        return visitor.visit_json(self)

class DataVisitor:
    def visit_csv(self, csv_data):
        pass
    
    def visit_json(self, json_data):
        pass

class ValidationVisitor(DataVisitor):
    def visit_csv(self, csv_data):
        return len(csv_data.data) > 0
    
    def visit_json(self, json_data):
        return isinstance(csv_data.data, dict)

class TransformationVisitor(DataVisitor):
    def visit_csv(self, csv_data):
        return csv_data.data.upper()
    
    def visit_json(self, json_data):
        return {k: str(v).upper() for k, v in json_data.data.items()}
```

### 18. How would you use the Abstract Factory Pattern for multi-cloud data processing?
**Answer**: Abstract Factory provides an interface for creating families of related objects.

```python
class CloudDataFactory:
    def create_storage(self):
        pass
    
    def create_compute(self):
        pass
    
    def create_database(self):
        pass

class AWSDataFactory(CloudDataFactory):
    def create_storage(self):
        return S3Storage()
    
    def create_compute(self):
        return EC2Compute()
    
    def create_database(self):
        return RDSDatabase()

class AzureDataFactory(CloudDataFactory):
    def create_storage(self):
        return BlobStorage()
    
    def create_compute(self):
        return AzureVM()
    
    def create_database(self):
        return AzureSQL()

class CloudDataProcessor:
    def __init__(self, factory):
        self.storage = factory.create_storage()
        self.compute = factory.create_compute()
        self.database = factory.create_database()
```

### 19. Explain the Bridge Pattern for data source abstraction
**Answer**: Bridge pattern separates abstraction from implementation, allowing both to vary independently.

```python
class DataSourceImplementation:
    def connect(self):
        pass
    
    def read_data(self):
        pass
    
    def close(self):
        pass

class DatabaseImplementation(DataSourceImplementation):
    def connect(self):
        return "Database connected"
    
    def read_data(self):
        return "Database data"
    
    def close(self):
        return "Database closed"

class FileImplementation(DataSourceImplementation):
    def connect(self):
        return "File opened"
    
    def read_data(self):
        return "File data"
    
    def close(self):
        return "File closed"

class DataSource:
    def __init__(self, implementation):
        self._implementation = implementation
    
    def get_data(self):
        self._implementation.connect()
        data = self._implementation.read_data()
        self._implementation.close()
        return data

class CachedDataSource(DataSource):
    def __init__(self, implementation):
        super().__init__(implementation)
        self._cache = {}
    
    def get_data(self):
        if 'data' not in self._cache:
            self._cache['data'] = super().get_data()
        return self._cache['data']
```

### 20. How would you implement the Flyweight Pattern for memory-efficient data processing?
**Answer**: Flyweight pattern minimizes memory usage by sharing efficiently among similar objects.

```python
class DataProcessorFlyweight:
    def __init__(self, algorithm_type):
        self._algorithm_type = algorithm_type
    
    def process(self, context_data):
        return f"Processing {context_data} with {self._algorithm_type}"

class DataProcessorFactory:
    _flyweights = {}
    
    @classmethod
    def get_processor(cls, algorithm_type):
        if algorithm_type not in cls._flyweights:
            cls._flyweights[algorithm_type] = DataProcessorFlyweight(algorithm_type)
        return cls._flyweights[algorithm_type]
    
    @classmethod
    def get_created_flyweights(cls):
        return len(cls._flyweights)

class DataContext:
    def __init__(self, data, algorithm_type):
        self._data = data
        self._processor = DataProcessorFactory.get_processor(algorithm_type)
    
    def process(self):
        return self._processor.process(self._data)
```

## System Design Questions

### 21. Design a data processing system using multiple design patterns
**Answer**: Combine multiple patterns for a robust, scalable system:

```python
# Factory + Strategy + Observer + Command
class DataProcessingSystem:
    def __init__(self):
        self._observers = []
        self._command_queue = []
        self._processor_factory = ProcessorFactory()
    
    def add_observer(self, observer):
        self._observers.append(observer)
    
    def notify_observers(self, event):
        for observer in self._observers:
            observer.update(event)
    
    def add_command(self, command):
        self._command_queue.append(command)
    
    def execute_commands(self):
        for command in self._command_queue:
            try:
                result = command.execute()
                self.notify_observers(f"Command executed: {result}")
            except Exception as e:
                self.notify_observers(f"Command failed: {e}")
```

### 22. How would you design a plugin architecture for data transformations?
**Answer**: Use Strategy + Factory + Registry patterns:

```python
class TransformationRegistry:
    _transformations = {}
    
    @classmethod
    def register(cls, name, transformation_class):
        cls._transformations[name] = transformation_class
    
    @classmethod
    def create_transformation(cls, name, **kwargs):
        if name in cls._transformations:
            return cls._transformations[name](**kwargs)
        raise ValueError(f"Unknown transformation: {name}")

def transformation(name):
    def decorator(cls):
        TransformationRegistry.register(name, cls)
        return cls
    return decorator

@transformation("normalize")
class NormalizationTransformation:
    def transform(self, data):
        return (data - data.mean()) / data.std()
```

This comprehensive set covers all major design patterns with practical data engineering examples, progressing from basic to advanced concepts with real-world applications.