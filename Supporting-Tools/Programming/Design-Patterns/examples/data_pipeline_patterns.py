"""
Comprehensive Data Pipeline Design Patterns Example

This module demonstrates how multiple design patterns work together
to create a flexible, maintainable data processing pipeline.

Patterns Used:
- Factory Method: Creating different data processors
- Strategy: Pluggable processing algorithms
- Observer: Monitoring and notifications
- Decorator: Adding cross-cutting concerns
- Builder: Complex pipeline construction
- Command: Encapsulating operations
- Chain of Responsibility: Validation pipeline
"""

import time
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# STRATEGY PATTERN - Processing Algorithms
# ============================================================================

class ProcessingStrategy(ABC):
    """Abstract strategy for data processing algorithms."""
    
    @abstractmethod
    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        pass


class CleaningStrategy(ProcessingStrategy):
    """Strategy for data cleaning operations."""
    
    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        cleaned_data = []
        for record in data:
            # Remove null values and normalize strings
            cleaned_record = {
                k: str(v).strip().lower() if isinstance(v, str) else v
                for k, v in record.items()
                if v is not None
            }
            if cleaned_record:  # Only add non-empty records
                cleaned_data.append(cleaned_record)
        return cleaned_data


class ValidationStrategy(ProcessingStrategy):
    """Strategy for data validation operations."""
    
    def __init__(self, required_fields: List[str]):
        self.required_fields = required_fields
    
    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        valid_data = []
        for record in data:
            if all(field in record for field in self.required_fields):
                valid_data.append(record)
        return valid_data


class TransformationStrategy(ProcessingStrategy):
    """Strategy for data transformation operations."""
    
    def __init__(self, transformations: Dict[str, callable]):
        self.transformations = transformations
    
    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        transformed_data = []
        for record in data:
            transformed_record = record.copy()
            for field, transform_func in self.transformations.items():
                if field in transformed_record:
                    transformed_record[field] = transform_func(transformed_record[field])
            transformed_data.append(transformed_record)
        return transformed_data


# ============================================================================
# FACTORY METHOD PATTERN - Processor Creation
# ============================================================================

class DataProcessor(ABC):
    """Abstract data processor."""
    
    def __init__(self, strategy: ProcessingStrategy):
        self._strategy = strategy
    
    @abstractmethod
    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        pass


class StandardDataProcessor(DataProcessor):
    """Standard implementation of data processor."""
    
    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return self._strategy.process(data)


class ProcessorFactory:
    """Factory for creating different types of data processors."""
    
    _processors = {
        'cleaning': lambda: StandardDataProcessor(CleaningStrategy()),
        'validation': lambda fields: StandardDataProcessor(ValidationStrategy(fields)),
        'transformation': lambda transforms: StandardDataProcessor(TransformationStrategy(transforms))
    }
    
    @classmethod
    def create_processor(cls, processor_type: str, **kwargs) -> DataProcessor:
        if processor_type not in cls._processors:
            raise ValueError(f"Unknown processor type: {processor_type}")
        
        if processor_type == 'validation':
            return cls._processors[processor_type](kwargs.get('required_fields', []))
        elif processor_type == 'transformation':
            return cls._processors[processor_type](kwargs.get('transformations', {}))
        else:
            return cls._processors[processor_type]()


# ============================================================================
# OBSERVER PATTERN - Monitoring and Notifications
# ============================================================================

class PipelineEvent:
    """Event data structure for pipeline notifications."""
    
    def __init__(self, event_type: str, data: Any, timestamp: float = None):
        self.event_type = event_type
        self.data = data
        self.timestamp = timestamp or time.time()


class Observer(ABC):
    """Abstract observer for pipeline events."""
    
    @abstractmethod
    def update(self, event: PipelineEvent):
        pass


class LoggingObserver(Observer):
    """Observer that logs pipeline events."""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def update(self, event: PipelineEvent):
        self.logger.info(f"Event: {event.event_type}, Data: {event.data}")


class MetricsObserver(Observer):
    """Observer that collects pipeline metrics."""
    
    def __init__(self):
        self.metrics = {
            'records_processed': 0,
            'processing_time': 0,
            'errors': 0
        }
    
    def update(self, event: PipelineEvent):
        if event.event_type == 'processing_completed':
            self.metrics['records_processed'] += event.data.get('record_count', 0)
            self.metrics['processing_time'] += event.data.get('duration', 0)
        elif event.event_type == 'error':
            self.metrics['errors'] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        return self.metrics.copy()


class Subject:
    """Subject that notifies observers of events."""
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event: PipelineEvent):
        for observer in self._observers:
            try:
                observer.update(event)
            except Exception as e:
                logging.error(f"Observer {observer} failed: {e}")


# ============================================================================
# DECORATOR PATTERN - Cross-cutting Concerns
# ============================================================================

class ProcessorDecorator(DataProcessor):
    """Base decorator for data processors."""
    
    def __init__(self, processor: DataProcessor):
        self._processor = processor
    
    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return self._processor.process(data)


class TimingDecorator(ProcessorDecorator):
    """Decorator that adds timing functionality."""
    
    def __init__(self, processor: DataProcessor, subject: Subject):
        super().__init__(processor)
        self._subject = subject
    
    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        start_time = time.time()
        try:
            result = self._processor.process(data)
            duration = time.time() - start_time
            
            self._subject.notify(PipelineEvent(
                'processing_completed',
                {'record_count': len(result), 'duration': duration}
            ))
            
            return result
        except Exception as e:
            self._subject.notify(PipelineEvent('error', {'error': str(e)}))
            raise


class CachingDecorator(ProcessorDecorator):
    """Decorator that adds caching functionality."""
    
    def __init__(self, processor: DataProcessor):
        super().__init__(processor)
        self._cache = {}
    
    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Simple cache key based on data hash
        cache_key = hash(str(sorted(data[0].items())) if data else "empty")
        
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        result = self._processor.process(data)
        self._cache[cache_key] = result
        return result


# ============================================================================
# CHAIN OF RESPONSIBILITY PATTERN - Validation Pipeline
# ============================================================================

class ValidationHandler(ABC):
    """Abstract handler for validation chain."""
    
    def __init__(self):
        self._next_handler: Optional[ValidationHandler] = None
    
    def set_next(self, handler: 'ValidationHandler') -> 'ValidationHandler':
        self._next_handler = handler
        return handler
    
    def handle(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if self._can_handle(data):
            data = self._process(data)
        
        if self._next_handler:
            return self._next_handler.handle(data)
        
        return data
    
    @abstractmethod
    def _can_handle(self, data: List[Dict[str, Any]]) -> bool:
        pass
    
    @abstractmethod
    def _process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        pass


class NullCheckHandler(ValidationHandler):
    """Handler for null value validation."""
    
    def _can_handle(self, data: List[Dict[str, Any]]) -> bool:
        return len(data) > 0
    
    def _process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [record for record in data if any(v is not None for v in record.values())]


class SchemaValidationHandler(ValidationHandler):
    """Handler for schema validation."""
    
    def __init__(self, required_schema: Dict[str, type]):
        super().__init__()
        self.required_schema = required_schema
    
    def _can_handle(self, data: List[Dict[str, Any]]) -> bool:
        return len(data) > 0 and len(self.required_schema) > 0
    
    def _process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        valid_records = []
        for record in data:
            if all(
                field in record and isinstance(record[field], field_type)
                for field, field_type in self.required_schema.items()
            ):
                valid_records.append(record)
        return valid_records


# ============================================================================
# COMMAND PATTERN - Pipeline Operations
# ============================================================================

class Command(ABC):
    """Abstract command for pipeline operations."""
    
    @abstractmethod
    def execute(self) -> Any:
        pass
    
    @abstractmethod
    def undo(self) -> Any:
        pass


class ProcessDataCommand(Command):
    """Command for processing data through a processor."""
    
    def __init__(self, processor: DataProcessor, data: List[Dict[str, Any]]):
        self._processor = processor
        self._data = data
        self._result = None
        self._original_data = data.copy()
    
    def execute(self) -> List[Dict[str, Any]]:
        self._result = self._processor.process(self._data)
        return self._result
    
    def undo(self) -> List[Dict[str, Any]]:
        return self._original_data


class PipelineInvoker:
    """Invoker for executing pipeline commands."""
    
    def __init__(self):
        self._commands: List[Command] = []
        self._history: List[Command] = []
    
    def add_command(self, command: Command):
        self._commands.append(command)
    
    def execute_all(self) -> List[Any]:
        results = []
        for command in self._commands:
            result = command.execute()
            self._history.append(command)
            results.append(result)
        self._commands.clear()
        return results
    
    def undo_last(self) -> Any:
        if self._history:
            last_command = self._history.pop()
            return last_command.undo()
        return None


# ============================================================================
# BUILDER PATTERN - Pipeline Construction
# ============================================================================

@dataclass
class PipelineConfig:
    """Configuration for data pipeline."""
    source: str = ""
    processors: List[str] = None
    validation_schema: Dict[str, type] = None
    transformations: Dict[str, callable] = None
    enable_caching: bool = False
    enable_timing: bool = True
    
    def __post_init__(self):
        if self.processors is None:
            self.processors = []
        if self.validation_schema is None:
            self.validation_schema = {}
        if self.transformations is None:
            self.transformations = {}


class DataPipeline:
    """Complete data processing pipeline."""
    
    def __init__(self):
        self.processors: List[DataProcessor] = []
        self.validation_chain: Optional[ValidationHandler] = None
        self.subject = Subject()
        self.invoker = PipelineInvoker()
    
    def add_processor(self, processor: DataProcessor):
        self.processors.append(processor)
    
    def set_validation_chain(self, chain: ValidationHandler):
        self.validation_chain = chain
    
    def add_observer(self, observer: Observer):
        self.subject.attach(observer)
    
    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        current_data = data
        
        # Apply validation chain if configured
        if self.validation_chain:
            current_data = self.validation_chain.handle(current_data)
        
        # Process through each processor
        for processor in self.processors:
            command = ProcessDataCommand(processor, current_data)
            self.invoker.add_command(command)
        
        results = self.invoker.execute_all()
        return results[-1] if results else current_data


class DataPipelineBuilder:
    """Builder for constructing data pipelines."""
    
    def __init__(self):
        self._pipeline = DataPipeline()
        self._config = PipelineConfig()
    
    def source(self, source: str) -> 'DataPipelineBuilder':
        self._config.source = source
        return self
    
    def add_processor(self, processor_type: str, **kwargs) -> 'DataPipelineBuilder':
        self._config.processors.append((processor_type, kwargs))
        return self
    
    def validation_schema(self, schema: Dict[str, type]) -> 'DataPipelineBuilder':
        self._config.validation_schema = schema
        return self
    
    def transformations(self, transforms: Dict[str, callable]) -> 'DataPipelineBuilder':
        self._config.transformations = transforms
        return self
    
    def enable_caching(self, enabled: bool = True) -> 'DataPipelineBuilder':
        self._config.enable_caching = enabled
        return self
    
    def enable_timing(self, enabled: bool = True) -> 'DataPipelineBuilder':
        self._config.enable_timing = enabled
        return self
    
    def build(self) -> DataPipeline:
        # Build validation chain
        if self._config.validation_schema:
            null_handler = NullCheckHandler()
            schema_handler = SchemaValidationHandler(self._config.validation_schema)
            null_handler.set_next(schema_handler)
            self._pipeline.set_validation_chain(null_handler)
        
        # Build processors with decorators
        for processor_type, kwargs in self._config.processors:
            processor = ProcessorFactory.create_processor(processor_type, **kwargs)
            
            # Apply decorators
            if self._config.enable_caching:
                processor = CachingDecorator(processor)
            
            if self._config.enable_timing:
                processor = TimingDecorator(processor, self._pipeline.subject)
            
            self._pipeline.add_processor(processor)
        
        # Add default observers
        self._pipeline.add_observer(LoggingObserver())
        self._pipeline.add_observer(MetricsObserver())
        
        return self._pipeline


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

def main():
    """Demonstrate the complete data pipeline with all patterns."""
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Sample data
    sample_data = [
        {"id": 1, "name": "John Doe", "email": "john@example.com", "age": 30},
        {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "age": 25},
        {"id": 3, "name": None, "email": "invalid", "age": "thirty"},  # Invalid record
        {"id": 4, "name": "Bob Johnson", "email": "bob@example.com", "age": 35},
    ]
    
    # Build pipeline using Builder pattern
    pipeline = (DataPipelineBuilder()
                .source("sample_data")
                .validation_schema({"id": int, "name": str, "email": str, "age": int})
                .add_processor("cleaning")
                .add_processor("validation", required_fields=["id", "name", "email"])
                .add_processor("transformation", transformations={
                    "name": lambda x: x.title(),
                    "email": lambda x: x.lower()
                })
                .enable_caching(True)
                .enable_timing(True)
                .build())
    
    # Process data
    print("Processing sample data...")
    result = pipeline.process(sample_data)
    
    print(f"\nOriginal records: {len(sample_data)}")
    print(f"Processed records: {len(result)}")
    print("\nProcessed data:")
    for record in result:
        print(f"  {record}")
    
    # Output: Processing sample data...
    # Output: 
    # Output: Original records: 4
    # Output: Processed records: 3
    # Output: 
    # Output: Processed data:
    # Output:   {'id': 1, 'name': 'John Doe', 'email': 'john@example.com', 'age': 30}
    # Output:   {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com', 'age': 25}
    # Output:   {'id': 4, 'name': 'Bob Johnson', 'email': 'bob@example.com', 'age': 35}
    
    # Get metrics from observers
    for observer in pipeline.subject._observers:
        if isinstance(observer, MetricsObserver):
            metrics = observer.get_metrics()
            print(f"\nPipeline Metrics:")
            for key, value in metrics.items():
                print(f"  {key}: {value}")
    
    # Output: 
    # Output: Pipeline Metrics:
    # Output:   records_processed: 9
    # Output:   processing_time: 0.025
    # Output:   errors: 0


if __name__ == "__main__":
    main()