# Design Patterns Quick Reference

## Creational Patterns

### Singleton
**Purpose**: Ensure only one instance exists
```python
class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### Factory Method
**Purpose**: Create objects without specifying exact classes
```python
class ProcessorFactory:
    @staticmethod
    def create(type):
        if type == "csv": return CSVProcessor()
        elif type == "json": return JSONProcessor()
```

### Abstract Factory
**Purpose**: Create families of related objects
```python
class CloudFactory:
    def create_storage(self): pass
    def create_compute(self): pass

class AWSFactory(CloudFactory):
    def create_storage(self): return S3Storage()
    def create_compute(self): return EC2Compute()
```

### Builder
**Purpose**: Construct complex objects step by step
```python
class PipelineBuilder:
    def __init__(self):
        self.pipeline = Pipeline()
    
    def add_source(self, source):
        self.pipeline.source = source
        return self
    
    def build(self):
        return self.pipeline
```

### Prototype
**Purpose**: Clone existing objects
```python
import copy

class DataProcessor:
    def clone(self):
        return copy.deepcopy(self)
```

## Structural Patterns

### Adapter
**Purpose**: Make incompatible interfaces work together
```python
class LegacyAdapter:
    def __init__(self, legacy_system):
        self.legacy = legacy_system
    
    def modern_method(self):
        return self.legacy.old_method()
```

### Bridge
**Purpose**: Separate abstraction from implementation
```python
class DataSource:
    def __init__(self, implementation):
        self.impl = implementation
    
    def get_data(self):
        return self.impl.fetch_data()
```

### Composite
**Purpose**: Treat individual and composite objects uniformly
```python
class DataComponent:
    def process(self): pass

class DataLeaf(DataComponent):
    def process(self): return "leaf data"

class DataComposite(DataComponent):
    def __init__(self):
        self.children = []
    
    def process(self):
        return [child.process() for child in self.children]
```

### Decorator
**Purpose**: Add behavior to objects dynamically
```python
class LoggingDecorator:
    def __init__(self, processor):
        self.processor = processor
    
    def process(self, data):
        print("Processing started")
        result = self.processor.process(data)
        print("Processing completed")
        return result
```

### Facade
**Purpose**: Provide simplified interface to complex subsystem
```python
class DataProcessingFacade:
    def __init__(self):
        self.extractor = DataExtractor()
        self.transformer = DataTransformer()
        self.loader = DataLoader()
    
    def process(self, source, destination):
        data = self.extractor.extract(source)
        processed = self.transformer.transform(data)
        self.loader.load(processed, destination)
```

### Flyweight
**Purpose**: Share common parts of objects to save memory
```python
class ProcessorFlyweight:
    def __init__(self, algorithm):
        self.algorithm = algorithm
    
    def process(self, context_data):
        return f"{self.algorithm}: {context_data}"

class ProcessorFactory:
    _flyweights = {}
    
    @classmethod
    def get_processor(cls, algorithm):
        if algorithm not in cls._flyweights:
            cls._flyweights[algorithm] = ProcessorFlyweight(algorithm)
        return cls._flyweights[algorithm]
```

### Proxy
**Purpose**: Control access to another object
```python
class DataProxy:
    def __init__(self, real_data, user_permissions):
        self.real_data = real_data
        self.permissions = user_permissions
    
    def access_data(self, user):
        if user in self.permissions:
            return self.real_data.get_data()
        raise PermissionError("Access denied")
```

## Behavioral Patterns

### Chain of Responsibility
**Purpose**: Pass requests along chain of handlers
```python
class Handler:
    def __init__(self):
        self.next_handler = None
    
    def set_next(self, handler):
        self.next_handler = handler
        return handler
    
    def handle(self, request):
        if self.can_handle(request):
            return self.process(request)
        elif self.next_handler:
            return self.next_handler.handle(request)
```

### Command
**Purpose**: Encapsulate requests as objects
```python
class Command:
    def execute(self): pass
    def undo(self): pass

class ProcessCommand(Command):
    def __init__(self, processor, data):
        self.processor = processor
        self.data = data
    
    def execute(self):
        return self.processor.process(self.data)
```

### Iterator
**Purpose**: Access elements sequentially without exposing structure
```python
class DataIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration
        result = self.data[self.index]
        self.index += 1
        return result
```

### Mediator
**Purpose**: Define how objects interact with each other
```python
class DataMediator:
    def __init__(self):
        self.components = []
    
    def register(self, component):
        self.components.append(component)
    
    def notify(self, sender, event):
        for component in self.components:
            if component != sender:
                component.handle_event(event)
```

### Memento
**Purpose**: Capture and restore object state
```python
class Memento:
    def __init__(self, state):
        self._state = state
    
    def get_state(self):
        return self._state

class Originator:
    def __init__(self):
        self._state = None
    
    def create_memento(self):
        return Memento(self._state)
    
    def restore_from_memento(self, memento):
        self._state = memento.get_state()
```

### Observer
**Purpose**: Notify multiple objects about state changes
```python
class Subject:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def notify(self, event):
        for observer in self._observers:
            observer.update(event)

class Observer:
    def update(self, event):
        pass
```

### State
**Purpose**: Change object behavior based on internal state
```python
class State:
    def handle(self, context): pass

class IdleState(State):
    def handle(self, context):
        context.set_state(ProcessingState())

class Context:
    def __init__(self):
        self._state = IdleState()
    
    def set_state(self, state):
        self._state = state
    
    def request(self):
        self._state.handle(self)
```

### Strategy
**Purpose**: Define family of algorithms and make them interchangeable
```python
class Strategy:
    def execute(self, data): pass

class SortStrategy(Strategy):
    def execute(self, data):
        return sorted(data)

class FilterStrategy(Strategy):
    def execute(self, data):
        return [x for x in data if x > 0]

class Context:
    def __init__(self, strategy):
        self._strategy = strategy
    
    def execute_strategy(self, data):
        return self._strategy.execute(data)
```

### Template Method
**Purpose**: Define algorithm skeleton, let subclasses override steps
```python
class DataProcessor:
    def process(self):
        data = self.extract()
        transformed = self.transform(data)
        self.load(transformed)
    
    def extract(self): raise NotImplementedError
    def transform(self, data): return data  # Default implementation
    def load(self, data): raise NotImplementedError

class CSVProcessor(DataProcessor):
    def extract(self):
        return "CSV data"
    
    def load(self, data):
        print(f"Loading: {data}")
```

### Visitor
**Purpose**: Separate algorithms from object structure
```python
class Visitor:
    def visit_csv(self, element): pass
    def visit_json(self, element): pass

class Element:
    def accept(self, visitor): pass

class CSVElement(Element):
    def accept(self, visitor):
        return visitor.visit_csv(self)

class ValidationVisitor(Visitor):
    def visit_csv(self, element):
        return "CSV validation"
    
    def visit_json(self, element):
        return "JSON validation"
```

## Common Data Engineering Use Cases

### ETL Pipeline with Multiple Patterns
```python
# Factory + Strategy + Observer + Template Method
class ETLPipeline:
    def __init__(self):
        self.extractor_factory = ExtractorFactory()
        self.observers = []
    
    def create_pipeline(self, config):
        extractor = self.extractor_factory.create(config.source_type)
        strategy = self._select_strategy(config.processing_type)
        
        pipeline = ConcreteETLPipeline(extractor, strategy)
        
        for observer in self.observers:
            pipeline.attach(observer)
        
        return pipeline
```

### Data Validation Chain
```python
# Chain of Responsibility + Command
class ValidationChain:
    def __init__(self):
        self.null_check = NullCheckHandler()
        self.type_check = TypeCheckHandler()
        self.range_check = RangeCheckHandler()
        
        self.null_check.set_next(self.type_check).set_next(self.range_check)
    
    def validate(self, data):
        return self.null_check.handle(ValidationRequest(data))
```

### Configurable Data Processor
```python
# Builder + Strategy + Decorator
processor = (DataProcessorBuilder()
            .add_source(CSVSource("data.csv"))
            .add_strategy(CleaningStrategy())
            .add_decorator(LoggingDecorator)
            .add_decorator(CachingDecorator)
            .build())
```

### Plugin Architecture
```python
# Factory + Registry + Strategy
class PluginRegistry:
    _plugins = {}
    
    @classmethod
    def register(cls, name, plugin_class):
        cls._plugins[name] = plugin_class
    
    @classmethod
    def create_plugin(cls, name, **kwargs):
        return cls._plugins[name](**kwargs)

@plugin("csv_processor")
class CSVProcessor:
    def process(self, data):
        return "Processed CSV"
```

## Pattern Selection Guide

### When to Use Each Pattern

**Creational Patterns**:
- **Singleton**: Database connections, configuration managers
- **Factory**: Creating different data processors based on file type
- **Builder**: Complex pipeline construction with many optional components
- **Prototype**: Cloning expensive-to-create objects

**Structural Patterns**:
- **Adapter**: Integrating legacy systems with modern APIs
- **Decorator**: Adding cross-cutting concerns (logging, caching, monitoring)
- **Facade**: Simplifying complex data processing workflows
- **Proxy**: Access control, lazy loading, caching

**Behavioral Patterns**:
- **Observer**: Event-driven architectures, monitoring systems
- **Strategy**: Pluggable algorithms, A/B testing
- **Command**: Undo/redo operations, queuing operations
- **Chain of Responsibility**: Validation pipelines, error handling

### Anti-Patterns to Avoid

1. **Overuse of Singleton**: Can make testing difficult
2. **God Object**: Avoid classes that do too much
3. **Premature Optimization**: Don't add patterns until needed
4. **Pattern Overload**: Don't use patterns just because you can

### Performance Considerations

- **Flyweight**: Use for memory-intensive applications
- **Proxy**: Can add latency but improves security/caching
- **Decorator**: Multiple decorators can impact performance
- **Observer**: Many observers can slow down notifications