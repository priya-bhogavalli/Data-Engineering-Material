# 🎨 Python Design Patterns - Real World Analogies & Simple Examples

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Design Patterns](https://img.shields.io/badge/Patterns-23-green.svg)](https://en.wikipedia.org/wiki/Design_Patterns)

> **Master Python design patterns through real-world analogies and practical data engineering examples**

## 🎯 Quick Reference

| Pattern Type | Count | Use Cases | Data Engineering Examples |
|--------------|-------|-----------|---------------------------|
| **[Creational](#-creational-patterns)** | 5 | Object creation | Database connections, data parsers |
| **[Structural](#-structural-patterns)** | 7 | Object composition | Data adapters, API wrappers |
| **[Behavioral](#-behavioral-patterns)** | 11 | Object interaction | ETL pipelines, event handling |

---

## 🏗️ Creational Patterns

### 1. Singleton Pattern
**🏠 Real-World Analogy**: Like having only one CEO in a company - there can be only one instance.

**Data Engineering Use Case**: Database connection manager, configuration settings

```python
class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = "Connected to DB"
        return cls._instance

# Usage
db1 = DatabaseConnection()
db2 = DatabaseConnection()
print(db1 is db2)  # True - same instance
```

### 2. Factory Pattern
**🏭 Real-World Analogy**: Like a car factory that produces different car models based on specifications.

**Data Engineering Use Case**: Creating different data parsers based on file type

```python
class DataParser:
    @staticmethod
    def create_parser(file_type):
        parsers = {
            'csv': CSVParser(),
            'json': JSONParser(),
            'xml': XMLParser()
        }
        return parsers.get(file_type, CSVParser())

class CSVParser:
    def parse(self, data): return data.split(',')

class JSONParser:
    def parse(self, data): return eval(data)  # Simplified

# Usage
parser = DataParser.create_parser('csv')
result = parser.parse("name,age,city")
```

### 3. Builder Pattern
**🏗️ Real-World Analogy**: Like building a house step by step - foundation, walls, roof.

**Data Engineering Use Case**: Building complex SQL queries or ETL pipelines

```python
class SQLQueryBuilder:
    def __init__(self):
        self.query = ""
    
    def select(self, fields):
        self.query += f"SELECT {fields} "
        return self
    
    def from_table(self, table):
        self.query += f"FROM {table} "
        return self
    
    def where(self, condition):
        self.query += f"WHERE {condition} "
        return self
    
    def build(self):
        return self.query.strip()

# Usage
query = (SQLQueryBuilder()
         .select("name, age")
         .from_table("users")
         .where("age > 18")
         .build())
print(query)  # SELECT name, age FROM users WHERE age > 18
```

### 4. Prototype Pattern
**🐑 Real-World Analogy**: Like cloning sheep - creating copies of existing objects.

**Data Engineering Use Case**: Cloning data processing configurations

```python
import copy

class DataProcessingConfig:
    def __init__(self, batch_size=1000, timeout=30):
        self.batch_size = batch_size
        self.timeout = timeout
        self.filters = []
    
    def clone(self):
        return copy.deepcopy(self)

# Usage
base_config = DataProcessingConfig()
base_config.filters = ['remove_nulls', 'validate_email']

prod_config = base_config.clone()
prod_config.batch_size = 5000
```

### 5. Abstract Factory Pattern
**🏪 Real-World Analogy**: Like different furniture stores (IKEA, Ashley) that make complete furniture sets.

**Data Engineering Use Case**: Creating cloud service families (AWS, Azure, GCP)

```python
class CloudServiceFactory:
    def create_storage(self): pass
    def create_compute(self): pass

class AWSFactory(CloudServiceFactory):
    def create_storage(self): return "S3"
    def create_compute(self): return "EC2"

class AzureFactory(CloudServiceFactory):
    def create_storage(self): return "Blob Storage"
    def create_compute(self): return "Virtual Machine"

# Usage
factory = AWSFactory()
storage = factory.create_storage()  # S3
compute = factory.create_compute()  # EC2
```

---

## 🔧 Structural Patterns

### 6. Adapter Pattern
**🔌 Real-World Analogy**: Like a power adapter that lets you plug US devices into European outlets.

**Data Engineering Use Case**: Adapting different API responses to a common format

```python
class LegacyDataAPI:
    def get_user_info(self):
        return "John|25|Engineer"

class ModernDataAPI:
    def get_user_data(self):
        return {"name": "John", "age": 25, "job": "Engineer"}

class LegacyAPIAdapter:
    def __init__(self, legacy_api):
        self.legacy_api = legacy_api
    
    def get_user_data(self):
        data = self.legacy_api.get_user_info().split('|')
        return {"name": data[0], "age": int(data[1]), "job": data[2]}

# Usage
legacy = LegacyDataAPI()
adapter = LegacyAPIAdapter(legacy)
user_data = adapter.get_user_data()  # Returns dict format
```

### 7. Decorator Pattern
**🎁 Real-World Analogy**: Like gift wrapping - adding features without changing the original item.

**Data Engineering Use Case**: Adding logging, caching, or validation to data functions

```python
def log_execution(func):
    def wrapper(*args, **kwargs):
        print(f"Executing {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Completed {func.__name__}")
        return result
    return wrapper

def cache_result(func):
    cache = {}
    def wrapper(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return wrapper

@log_execution
@cache_result
def expensive_calculation(n):
    return sum(range(n))

# Usage
result = expensive_calculation(1000)  # Logs and caches
result = expensive_calculation(1000)  # Uses cache
```

### 8. Facade Pattern
**🏢 Real-World Analogy**: Like a hotel concierge who handles all your requests without you knowing the details.

**Data Engineering Use Case**: Simplifying complex data processing operations

```python
class DataProcessingFacade:
    def __init__(self):
        self.extractor = DataExtractor()
        self.transformer = DataTransformer()
        self.loader = DataLoader()
    
    def process_data(self, source, destination):
        data = self.extractor.extract(source)
        clean_data = self.transformer.transform(data)
        self.loader.load(clean_data, destination)
        return "Data processing completed"

class DataExtractor:
    def extract(self, source): return f"Data from {source}"

class DataTransformer:
    def transform(self, data): return f"Cleaned {data}"

class DataLoader:
    def load(self, data, dest): print(f"Loaded {data} to {dest}")

# Usage
processor = DataProcessingFacade()
processor.process_data("database", "warehouse")
```

### 9. Composite Pattern
**🌳 Real-World Analogy**: Like a company org chart - employees and departments can contain other employees/departments.

**Data Engineering Use Case**: Building hierarchical data structures or nested transformations

```python
class DataComponent:
    def process(self): pass

class DataField(DataComponent):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def process(self):
        return f"{self.name}: {self.value}"

class DataRecord(DataComponent):
    def __init__(self, name):
        self.name = name
        self.children = []
    
    def add(self, component):
        self.children.append(component)
    
    def process(self):
        results = [child.process() for child in self.children]
        return f"{self.name} -> {results}"

# Usage
record = DataRecord("User")
record.add(DataField("name", "John"))
record.add(DataField("age", 25))
print(record.process())  # User -> ['name: John', 'age: 25']
```

### 10. Proxy Pattern
**🚪 Real-World Analogy**: Like a security guard who controls access to a building.

**Data Engineering Use Case**: Controlling access to expensive resources or adding security

```python
class ExpensiveDataService:
    def get_data(self):
        print("Fetching expensive data...")
        return "Important data"

class DataServiceProxy:
    def __init__(self):
        self._service = None
        self._cache = None
    
    def get_data(self):
        if self._cache:
            print("Returning cached data")
            return self._cache
        
        if not self._service:
            self._service = ExpensiveDataService()
        
        self._cache = self._service.get_data()
        return self._cache

# Usage
proxy = DataServiceProxy()
data1 = proxy.get_data()  # Fetches from service
data2 = proxy.get_data()  # Returns from cache
```

### 11. Bridge Pattern
**🌉 Real-World Analogy**: Like a bridge connecting two cities - separates interface from implementation.

**Data Engineering Use Case**: Separating data processing logic from storage implementation

```python
class DataStorage:
    def save(self, data): pass

class FileStorage(DataStorage):
    def save(self, data):
        return f"Saved to file: {data}"

class DatabaseStorage(DataStorage):
    def save(self, data):
        return f"Saved to DB: {data}"

class DataProcessor:
    def __init__(self, storage):
        self.storage = storage
    
    def process_and_save(self, data):
        processed = f"Processed: {data}"
        return self.storage.save(processed)

# Usage
file_processor = DataProcessor(FileStorage())
db_processor = DataProcessor(DatabaseStorage())

result1 = file_processor.process_and_save("user_data")
result2 = db_processor.process_and_save("user_data")
```

### 12. Flyweight Pattern
**📚 Real-World Analogy**: Like a library where books are shared among readers instead of everyone owning copies.

**Data Engineering Use Case**: Sharing common data transformation rules

```python
class TransformationRule:
    def __init__(self, rule_type):
        self.rule_type = rule_type
    
    def apply(self, data, context):
        return f"{self.rule_type} applied to {data} with {context}"

class TransformationFactory:
    _rules = {}
    
    @classmethod
    def get_rule(cls, rule_type):
        if rule_type not in cls._rules:
            cls._rules[rule_type] = TransformationRule(rule_type)
        return cls._rules[rule_type]

# Usage
rule1 = TransformationFactory.get_rule("uppercase")
rule2 = TransformationFactory.get_rule("uppercase")
print(rule1 is rule2)  # True - same instance shared

result = rule1.apply("hello", {"locale": "en"})
```

---

## 🎭 Behavioral Patterns

### 13. Observer Pattern
**📺 Real-World Analogy**: Like TV broadcasting - when news breaks, all subscribed viewers get notified.

**Data Engineering Use Case**: Notifying systems when data pipeline events occur

```python
class DataPipelineSubject:
    def __init__(self):
        self._observers = []
        self._state = None
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def notify(self):
        for observer in self._observers:
            observer.update(self._state)
    
    def set_state(self, state):
        self._state = state
        self.notify()

class EmailNotifier:
    def update(self, state):
        print(f"Email: Pipeline {state}")

class SlackNotifier:
    def update(self, state):
        print(f"Slack: Pipeline {state}")

# Usage
pipeline = DataPipelineSubject()
pipeline.attach(EmailNotifier())
pipeline.attach(SlackNotifier())
pipeline.set_state("completed")  # Notifies all observers
```

### 14. Strategy Pattern
**🎯 Real-World Analogy**: Like choosing different routes to work - car, bus, or bike based on conditions.

**Data Engineering Use Case**: Choosing different data processing strategies based on data size

```python
class ProcessingStrategy:
    def process(self, data): pass

class BatchProcessing(ProcessingStrategy):
    def process(self, data):
        return f"Batch processing {len(data)} records"

class StreamProcessing(ProcessingStrategy):
    def process(self, data):
        return f"Stream processing {len(data)} records"

class DataProcessor:
    def __init__(self, strategy):
        self.strategy = strategy
    
    def set_strategy(self, strategy):
        self.strategy = strategy
    
    def process_data(self, data):
        return self.strategy.process(data)

# Usage
processor = DataProcessor(BatchProcessing())
result1 = processor.process_data([1, 2, 3, 4, 5])

processor.set_strategy(StreamProcessing())
result2 = processor.process_data([1, 2, 3])
```

### 15. Command Pattern
**📋 Real-World Analogy**: Like a restaurant order - the waiter takes your order (command) and the kitchen executes it.

**Data Engineering Use Case**: Queuing and executing data operations

```python
class DataCommand:
    def execute(self): pass
    def undo(self): pass

class ExtractCommand(DataCommand):
    def __init__(self, source):
        self.source = source
    
    def execute(self):
        return f"Extracted data from {self.source}"
    
    def undo(self):
        return f"Undoing extraction from {self.source}"

class TransformCommand(DataCommand):
    def __init__(self, data):
        self.data = data
    
    def execute(self):
        return f"Transformed {self.data}"
    
    def undo(self):
        return f"Undoing transformation of {self.data}"

class DataPipelineInvoker:
    def __init__(self):
        self.commands = []
    
    def add_command(self, command):
        self.commands.append(command)
    
    def execute_all(self):
        results = []
        for command in self.commands:
            results.append(command.execute())
        return results

# Usage
pipeline = DataPipelineInvoker()
pipeline.add_command(ExtractCommand("database"))
pipeline.add_command(TransformCommand("user_data"))
results = pipeline.execute_all()
```

### 16. State Pattern
**🚦 Real-World Analogy**: Like a traffic light that changes behavior based on its current state (red, yellow, green).

**Data Engineering Use Case**: Managing data pipeline states

```python
class PipelineState:
    def start(self, pipeline): pass
    def stop(self, pipeline): pass

class IdleState(PipelineState):
    def start(self, pipeline):
        print("Starting pipeline...")
        pipeline.state = RunningState()
    
    def stop(self, pipeline):
        print("Pipeline already stopped")

class RunningState(PipelineState):
    def start(self, pipeline):
        print("Pipeline already running")
    
    def stop(self, pipeline):
        print("Stopping pipeline...")
        pipeline.state = IdleState()

class DataPipeline:
    def __init__(self):
        self.state = IdleState()
    
    def start(self):
        self.state.start(self)
    
    def stop(self):
        self.state.stop(self)

# Usage
pipeline = DataPipeline()
pipeline.start()  # Starting pipeline...
pipeline.start()  # Pipeline already running
pipeline.stop()   # Stopping pipeline...
```

### 17. Template Method Pattern
**📝 Real-World Analogy**: Like a recipe template - the steps are defined, but ingredients can vary.

**Data Engineering Use Case**: Defining ETL pipeline template with customizable steps

```python
class ETLTemplate:
    def process(self):
        data = self.extract()
        transformed = self.transform(data)
        self.load(transformed)
    
    def extract(self): pass  # Abstract method
    def transform(self, data): pass  # Abstract method
    def load(self, data): pass  # Abstract method

class CSVETLPipeline(ETLTemplate):
    def extract(self):
        return "CSV data extracted"
    
    def transform(self, data):
        return f"Transformed {data}"
    
    def load(self, data):
        print(f"Loaded {data} to warehouse")

class JSONETL Pipeline(ETLTemplate):
    def extract(self):
        return "JSON data extracted"
    
    def transform(self, data):
        return f"Parsed and transformed {data}"
    
    def load(self, data):
        print(f"Loaded {data} to data lake")

# Usage
csv_pipeline = CSVETLPipeline()
csv_pipeline.process()

json_pipeline = JSONETLPipeline()
json_pipeline.process()
```

### 18. Chain of Responsibility Pattern
**🏭 Real-World Analogy**: Like an assembly line where each worker handles a specific task and passes it to the next.

**Data Engineering Use Case**: Data validation and cleaning pipeline

```python
class DataHandler:
    def __init__(self):
        self.next_handler = None
    
    def set_next(self, handler):
        self.next_handler = handler
        return handler
    
    def handle(self, data):
        if self.next_handler:
            return self.next_handler.handle(data)
        return data

class NullValueHandler(DataHandler):
    def handle(self, data):
        if data is None:
            return "DEFAULT_VALUE"
        return super().handle(data)

class EmailValidationHandler(DataHandler):
    def handle(self, data):
        if "@" not in str(data):
            return f"invalid_{data}"
        return super().handle(data)

class UpperCaseHandler(DataHandler):
    def handle(self, data):
        return super().handle(str(data).upper())

# Usage
null_handler = NullValueHandler()
email_handler = EmailValidationHandler()
upper_handler = UpperCaseHandler()

null_handler.set_next(email_handler).set_next(upper_handler)

result = null_handler.handle("user@example.com")  # USER@EXAMPLE.COM
```

### 19. Iterator Pattern
**📖 Real-World Analogy**: Like reading a book page by page - you access elements sequentially without knowing the internal structure.

**Data Engineering Use Case**: Iterating through large datasets without loading everything into memory

```python
class DatasetIterator:
    def __init__(self, dataset):
        self.dataset = dataset
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index >= len(self.dataset):
            raise StopIteration
        value = self.dataset[self.index]
        self.index += 1
        return value

class LargeDataset:
    def __init__(self, data):
        self.data = data
    
    def __iter__(self):
        return DatasetIterator(self.data)

# Usage
dataset = LargeDataset([1, 2, 3, 4, 5])
for item in dataset:
    print(f"Processing: {item}")
```

### 20. Mediator Pattern
**🏢 Real-World Analogy**: Like an air traffic controller coordinating multiple planes - centralized communication.

**Data Engineering Use Case**: Coordinating communication between different data services

```python
class DataServiceMediator:
    def __init__(self):
        self.services = {}
    
    def register_service(self, name, service):
        self.services[name] = service
        service.mediator = self
    
    def notify(self, sender, event, data):
        if event == "data_ready":
            if "processor" in self.services:
                self.services["processor"].process_data(data)
        elif event == "processing_complete":
            if "storage" in self.services:
                self.services["storage"].store_data(data)

class DataExtractor:
    def __init__(self):
        self.mediator = None
    
    def extract_data(self):
        data = "extracted_data"
        self.mediator.notify(self, "data_ready", data)

class DataProcessor:
    def __init__(self):
        self.mediator = None
    
    def process_data(self, data):
        processed = f"processed_{data}"
        self.mediator.notify(self, "processing_complete", processed)

class DataStorage:
    def store_data(self, data):
        print(f"Stored: {data}")

# Usage
mediator = DataServiceMediator()
extractor = DataExtractor()
processor = DataProcessor()
storage = DataStorage()

mediator.register_service("extractor", extractor)
mediator.register_service("processor", processor)
mediator.register_service("storage", storage)

extractor.extract_data()  # Triggers the entire pipeline
```

### 21. Memento Pattern
**💾 Real-World Analogy**: Like saving game progress - you can restore to a previous state if needed.

**Data Engineering Use Case**: Saving and restoring data processing states for rollback

```python
class DataProcessingMemento:
    def __init__(self, state):
        self.state = state

class DataProcessor:
    def __init__(self):
        self.data = []
        self.processed_count = 0
    
    def add_data(self, item):
        self.data.append(item)
        self.processed_count += 1
    
    def save_state(self):
        return DataProcessingMemento({
            'data': self.data.copy(),
            'processed_count': self.processed_count
        })
    
    def restore_state(self, memento):
        self.data = memento.state['data']
        self.processed_count = memento.state['processed_count']
    
    def get_status(self):
        return f"Data: {self.data}, Count: {self.processed_count}"

# Usage
processor = DataProcessor()
processor.add_data("item1")
processor.add_data("item2")

# Save checkpoint
checkpoint = processor.save_state()
print(processor.get_status())  # Data: ['item1', 'item2'], Count: 2

processor.add_data("item3")
print(processor.get_status())  # Data: ['item1', 'item2', 'item3'], Count: 3

# Restore to checkpoint
processor.restore_state(checkpoint)
print(processor.get_status())  # Data: ['item1', 'item2'], Count: 2
```

### 22. Visitor Pattern
**🏥 Real-World Analogy**: Like a doctor visiting patients - the doctor (visitor) performs different operations on different types of patients.

**Data Engineering Use Case**: Applying different operations to different data types

```python
class DataVisitor:
    def visit_csv_data(self, csv_data): pass
    def visit_json_data(self, json_data): pass
    def visit_xml_data(self, xml_data): pass

class ValidationVisitor(DataVisitor):
    def visit_csv_data(self, csv_data):
        return f"Validating CSV: {csv_data.content}"
    
    def visit_json_data(self, json_data):
        return f"Validating JSON: {json_data.content}"
    
    def visit_xml_data(self, xml_data):
        return f"Validating XML: {xml_data.content}"

class TransformationVisitor(DataVisitor):
    def visit_csv_data(self, csv_data):
        return f"Transforming CSV to DataFrame: {csv_data.content}"
    
    def visit_json_data(self, json_data):
        return f"Transforming JSON to Dict: {json_data.content}"

class DataElement:
    def accept(self, visitor): pass

class CSVData(DataElement):
    def __init__(self, content):
        self.content = content
    
    def accept(self, visitor):
        return visitor.visit_csv_data(self)

class JSONData(DataElement):
    def __init__(self, content):
        self.content = content
    
    def accept(self, visitor):
        return visitor.visit_json_data(self)

# Usage
csv_data = CSVData("name,age\nJohn,25")
json_data = JSONData('{"name": "John", "age": 25}')

validator = ValidationVisitor()
transformer = TransformationVisitor()

print(csv_data.accept(validator))     # Validating CSV: name,age\nJohn,25
print(json_data.accept(transformer))  # Transforming JSON to Dict: {"name": "John", "age": 25}
```

### 23. Interpreter Pattern
**🗣️ Real-World Analogy**: Like a language translator who interprets sentences word by word according to grammar rules.

**Data Engineering Use Case**: Interpreting and executing data query expressions

```python
class Expression:
    def interpret(self, context): pass

class NumberExpression(Expression):
    def __init__(self, number):
        self.number = number
    
    def interpret(self, context):
        return self.number

class AddExpression(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def interpret(self, context):
        return self.left.interpret(context) + self.right.interpret(context)

class MultiplyExpression(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def interpret(self, context):
        return self.left.interpret(context) * self.right.interpret(context)

# Usage - Building expression: (5 + 3) * 2
five = NumberExpression(5)
three = NumberExpression(3)
two = NumberExpression(2)

add_expr = AddExpression(five, three)
multiply_expr = MultiplyExpression(add_expr, two)

result = multiply_expr.interpret({})  # 16
print(f"Result: {result}")
```

---

## 🎯 Pattern Selection Guide

### By Use Case

| Use Case | Recommended Patterns | Why |
|----------|---------------------|-----|
| **Database Connections** | Singleton, Factory | Single instance, different DB types |
| **API Integration** | Adapter, Facade | Uniform interface, simplify complexity |
| **Data Processing** | Strategy, Template Method | Different algorithms, common workflow |
| **Event Handling** | Observer, Mediator | Loose coupling, centralized communication |
| **Pipeline Building** | Builder, Chain of Responsibility | Step-by-step construction, sequential processing |
| **Caching/Optimization** | Proxy, Flyweight | Control access, share resources |
| **State Management** | State, Memento | Behavior changes, rollback capability |

### By Problem Type

| Problem | Pattern | Example |
|---------|---------|---------|
| Too many if-else statements | Strategy | Different processing algorithms |
| Complex object creation | Factory/Builder | Database connections, queries |
| Need to add features dynamically | Decorator | Logging, caching, validation |
| Tight coupling between classes | Observer, Mediator | Event notifications |
| Need to traverse collections | Iterator | Large datasets |
| Complex subsystem interface | Facade | ETL operations |

---

## 🚀 Best Practices

### 1. **Don't Overuse Patterns**
```python
# ❌ Overengineered
class SimpleDataProcessorFactoryBuilderSingleton:
    pass

# ✅ Simple and clear
def process_data(data):
    return data.upper()
```

### 2. **Choose Based on Problem, Not Pattern**
```python
# ❌ Pattern for pattern's sake
class DataSingleton:  # Unnecessary complexity
    pass

# ✅ Solve actual problems
class DatabasePool:  # Actual need for single instance
    pass
```

### 3. **Keep It Readable**
```python
# ✅ Clear intent
class EmailNotificationStrategy:
    def send(self, message):
        return f"Email: {message}"

# ✅ Simple factory
def create_notifier(type):
    return {'email': EmailNotifier(), 'sms': SMSNotifier()}[type]
```

---

## 📚 Quick Reference

### Pattern Cheat Sheet
```python
# Creational
singleton = DatabaseConnection()  # One instance
parser = ParserFactory.create('csv')  # Object creation
query = QueryBuilder().select().from_table().build()  # Step by step

# Structural  
adapter = APIAdapter(legacy_api)  # Interface compatibility
@cache_decorator  # Add functionality
def expensive_function(): pass

# Behavioral
subject.attach(observer)  # Event notification
processor.set_strategy(batch_strategy)  # Algorithm selection
pipeline.add_command(extract_cmd)  # Action queuing
```

### Common Data Engineering Patterns
```python
# ETL Pipeline with Template Method
class ETLPipeline:
    def run(self):
        data = self.extract()
        transformed = self.transform(data)
        self.load(transformed)

# Data Processing with Strategy
class DataProcessor:
    def __init__(self, strategy):
        self.strategy = strategy
    
    def process(self, data):
        return self.strategy.process(data)

# Event-Driven with Observer
class DataPipeline:
    def __init__(self):
        self.observers = []
    
    def notify_completion(self):
        for observer in self.observers:
            observer.on_complete()
```

---

**Remember**: Design patterns are tools, not rules. Use them when they solve real problems and make your code more maintainable, not just because they exist! 🎯