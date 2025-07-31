# Design Patterns Big4 Interview Questions

## Google Interview Questions

### 1. Design a distributed data processing system that can handle failures gracefully
**Scenario**: You need to build a system that processes petabytes of data across thousands of machines, with automatic failure recovery and load balancing.

**Solution using Multiple Patterns**:

```python
# Command Pattern + Chain of Responsibility + Observer
class DistributedProcessingSystem:
    def __init__(self):
        self._nodes = []
        self._observers = []
        self._command_queue = PriorityQueue()
        self._failure_detector = FailureDetector()
        
    def add_node(self, node):
        self._nodes.append(node)
        self._failure_detector.monitor(node)
    
    def submit_job(self, job):
        command = ProcessingCommand(job, self._select_nodes(job.requirements))
        self._command_queue.put((job.priority, command))
    
    def _select_nodes(self, requirements):
        # Strategy pattern for node selection
        selector = NodeSelectorFactory.create_selector(requirements.type)
        return selector.select(self._nodes, requirements)

class ProcessingCommand:
    def __init__(self, job, nodes):
        self.job = job
        self.nodes = nodes
        self.backup_nodes = []
    
    def execute(self):
        try:
            return self._execute_on_nodes()
        except NodeFailureException as e:
            return self._handle_failure(e)
    
    def _execute_on_nodes(self):
        # Template Method pattern
        self._prepare_nodes()
        results = self._distribute_work()
        return self._aggregate_results(results)
    
    def _handle_failure(self, failure):
        # Chain of Responsibility for failure handling
        handler_chain = self._build_failure_handler_chain()
        return handler_chain.handle(failure)

# Observer pattern for monitoring
class SystemMonitor:
    def update(self, event):
        if event.type == "NODE_FAILURE":
            self._trigger_failover(event.node)
        elif event.type == "LOAD_HIGH":
            self._scale_up(event.metrics)
```

**Key Patterns Used**:
- **Command Pattern**: Encapsulates job execution requests
- **Observer Pattern**: Monitors system health and failures
- **Strategy Pattern**: Different node selection algorithms
- **Chain of Responsibility**: Hierarchical failure handling
- **Template Method**: Standardized job execution flow

### 2. Design a real-time analytics system with pluggable data sources and sinks
**Scenario**: Build a system like Google Analytics that can ingest data from multiple sources, apply transformations, and output to various destinations.

**Solution**:

```python
# Abstract Factory + Strategy + Decorator + Observer
class AnalyticsSystemFactory:
    @staticmethod
    def create_system(config):
        if config.deployment == "cloud":
            return CloudAnalyticsSystem()
        elif config.deployment == "on_premise":
            return OnPremiseAnalyticsSystem()
        else:
            return HybridAnalyticsSystem()

class AnalyticsSystem:
    def __init__(self):
        self._pipeline_builder = PipelineBuilder()
        self._plugin_registry = PluginRegistry()
        self._observers = []
    
    def create_pipeline(self, config):
        # Builder pattern for complex pipeline construction
        builder = self._pipeline_builder
        
        # Add sources
        for source_config in config.sources:
            source = self._plugin_registry.create_source(source_config)
            builder.add_source(source)
        
        # Add transformations with decorators
        for transform_config in config.transformations:
            transform = self._plugin_registry.create_transformation(transform_config)
            # Decorator pattern for adding monitoring, caching, etc.
            transform = MonitoringDecorator(transform)
            transform = CachingDecorator(transform)
            builder.add_transformation(transform)
        
        # Add sinks
        for sink_config in config.sinks:
            sink = self._plugin_registry.create_sink(sink_config)
            builder.add_sink(sink)
        
        return builder.build()

# Plugin architecture using Strategy pattern
class PluginRegistry:
    def __init__(self):
        self._sources = {}
        self._transformations = {}
        self._sinks = {}
    
    def register_source(self, name, source_class):
        self._sources[name] = source_class
    
    def create_source(self, config):
        source_class = self._sources[config.type]
        return source_class(config.parameters)

# Decorator pattern for cross-cutting concerns
class MonitoringDecorator:
    def __init__(self, component):
        self._component = component
        self._metrics = MetricsCollector()
    
    def process(self, data):
        start_time = time.time()
        try:
            result = self._component.process(data)
            self._metrics.record_success(time.time() - start_time)
            return result
        except Exception as e:
            self._metrics.record_failure(e)
            raise

# State pattern for pipeline lifecycle management
class PipelineState:
    def start(self, pipeline): pass
    def pause(self, pipeline): pass
    def stop(self, pipeline): pass

class RunningState(PipelineState):
    def pause(self, pipeline):
        pipeline.set_state(PausedState())
        pipeline.pause_processing()
```

## Amazon Interview Questions

### 3. Design a data warehouse ETL system that can handle schema evolution
**Scenario**: Build an ETL system for Amazon's data warehouse that can automatically adapt to changing data schemas without breaking existing pipelines.

**Solution**:

```python
# Adapter + Visitor + Strategy + Memento patterns
class SchemaEvolutionETL:
    def __init__(self):
        self._schema_registry = SchemaRegistry()
        self._adapters = {}
        self._version_manager = SchemaVersionManager()
    
    def process_data(self, data, source_schema_version):
        current_schema = self._schema_registry.get_latest_schema()
        source_schema = self._schema_registry.get_schema(source_schema_version)
        
        if source_schema_version != current_schema.version:
            adapter = self._get_adapter(source_schema_version, current_schema.version)
            data = adapter.adapt(data)
        
        return self._transform_data(data, current_schema)
    
    def _get_adapter(self, from_version, to_version):
        adapter_key = f"{from_version}->{to_version}"
        if adapter_key not in self._adapters:
            self._adapters[adapter_key] = SchemaAdapter(from_version, to_version)
        return self._adapters[adapter_key]

# Adapter pattern for schema compatibility
class SchemaAdapter:
    def __init__(self, from_version, to_version):
        self.from_version = from_version
        self.to_version = to_version
        self._migration_strategy = self._select_migration_strategy()
    
    def adapt(self, data):
        return self._migration_strategy.migrate(data, self.from_version, self.to_version)
    
    def _select_migration_strategy(self):
        # Strategy pattern for different migration approaches
        if self._is_backward_compatible():
            return BackwardCompatibleMigration()
        elif self._requires_data_transformation():
            return DataTransformationMigration()
        else:
            return BreakingChangeMigration()

# Visitor pattern for schema analysis
class SchemaVisitor:
    def visit_field(self, field): pass
    def visit_table(self, table): pass
    def visit_database(self, database): pass

class CompatibilityAnalyzer(SchemaVisitor):
    def __init__(self):
        self.compatibility_issues = []
    
    def visit_field(self, field):
        if field.is_required and not field.has_default:
            self.compatibility_issues.append(f"Required field {field.name} without default")
    
    def visit_table(self, table):
        for field in table.fields:
            field.accept(self)

# Memento pattern for rollback capability
class SchemaMemento:
    def __init__(self, schema_state, data_state, pipeline_state):
        self._schema_state = schema_state
        self._data_state = data_state
        self._pipeline_state = pipeline_state
    
    def restore(self):
        return self._schema_state, self._data_state, self._pipeline_state

class ETLCheckpoint:
    def __init__(self):
        self._checkpoints = []
    
    def create_checkpoint(self, etl_system):
        checkpoint = SchemaMemento(
            etl_system.get_schema_state(),
            etl_system.get_data_state(),
            etl_system.get_pipeline_state()
        )
        self._checkpoints.append(checkpoint)
        return len(self._checkpoints) - 1
    
    def rollback_to_checkpoint(self, etl_system, checkpoint_id):
        if checkpoint_id < len(self._checkpoints):
            checkpoint = self._checkpoints[checkpoint_id]
            etl_system.restore_state(checkpoint.restore())
```

### 4. Design a recommendation system data pipeline with A/B testing capabilities
**Scenario**: Build a data pipeline that can serve different recommendation algorithms to different user segments for A/B testing.

**Solution**:

```python
# Strategy + Factory + Observer + Command patterns
class RecommendationPipeline:
    def __init__(self):
        self._algorithm_factory = AlgorithmFactory()
        self._experiment_manager = ExperimentManager()
        self._observers = []
        self._command_queue = []
    
    def get_recommendations(self, user_id, context):
        experiment = self._experiment_manager.get_experiment(user_id)
        algorithm = self._algorithm_factory.create_algorithm(experiment.algorithm_type)
        
        # Command pattern for tracking recommendations
        command = RecommendationCommand(user_id, algorithm, context, experiment)
        self._command_queue.append(command)
        
        recommendations = command.execute()
        
        # Observer pattern for metrics collection
        self._notify_observers(RecommendationEvent(user_id, experiment, recommendations))
        
        return recommendations

# Strategy pattern for different algorithms
class RecommendationAlgorithm:
    def recommend(self, user_id, context): pass

class CollaborativeFilteringAlgorithm(RecommendationAlgorithm):
    def recommend(self, user_id, context):
        similar_users = self._find_similar_users(user_id)
        return self._get_recommendations_from_similar_users(similar_users)

class ContentBasedAlgorithm(RecommendationAlgorithm):
    def recommend(self, user_id, context):
        user_preferences = self._get_user_preferences(user_id)
        return self._find_similar_content(user_preferences)

# Factory pattern for algorithm creation
class AlgorithmFactory:
    _algorithms = {
        'collaborative_filtering': CollaborativeFilteringAlgorithm,
        'content_based': ContentBasedAlgorithm,
        'hybrid': HybridAlgorithm,
        'deep_learning': DeepLearningAlgorithm
    }
    
    @classmethod
    def create_algorithm(cls, algorithm_type):
        if algorithm_type in cls._algorithms:
            return cls._algorithms[algorithm_type]()
        raise ValueError(f"Unknown algorithm type: {algorithm_type}")

# Command pattern for recommendation tracking
class RecommendationCommand:
    def __init__(self, user_id, algorithm, context, experiment):
        self.user_id = user_id
        self.algorithm = algorithm
        self.context = context
        self.experiment = experiment
        self.timestamp = time.time()
    
    def execute(self):
        recommendations = self.algorithm.recommend(self.user_id, self.context)
        self._log_recommendation(recommendations)
        return recommendations
    
    def _log_recommendation(self, recommendations):
        log_entry = {
            'user_id': self.user_id,
            'experiment_id': self.experiment.id,
            'algorithm': self.experiment.algorithm_type,
            'recommendations': recommendations,
            'timestamp': self.timestamp
        }
        RecommendationLogger.log(log_entry)
```

## Microsoft Interview Questions

### 5. Design a data synchronization system for distributed databases
**Scenario**: Build a system that keeps multiple database replicas in sync across different geographic regions, handling conflicts and network partitions.

**Solution**:

```python
# Observer + State + Command + Mediator patterns
class DistributedSyncSystem:
    def __init__(self):
        self._replicas = {}
        self._conflict_resolver = ConflictResolver()
        self._sync_mediator = SyncMediator()
        self._state = IdleState()
    
    def add_replica(self, region, replica):
        self._replicas[region] = replica
        replica.add_observer(self._sync_mediator)
    
    def sync_data(self, operation):
        sync_command = SyncCommand(operation, self._replicas, self._conflict_resolver)
        return self._state.handle_sync(self, sync_command)

# State pattern for sync system states
class SyncState:
    def handle_sync(self, system, command): pass
    def handle_conflict(self, system, conflict): pass
    def handle_partition(self, system, partition_info): pass

class IdleState(SyncState):
    def handle_sync(self, system, command):
        system.set_state(SyncingState())
        return command.execute()

class SyncingState(SyncState):
    def handle_sync(self, system, command):
        # Queue the command for later execution
        system.queue_command(command)
    
    def handle_conflict(self, system, conflict):
        system.set_state(ConflictResolutionState())
        return system.resolve_conflict(conflict)

class ConflictResolutionState(SyncState):
    def handle_sync(self, system, command):
        # Block sync operations during conflict resolution
        raise SyncBlockedException("Sync blocked due to conflict resolution")

# Command pattern for sync operations
class SyncCommand:
    def __init__(self, operation, replicas, conflict_resolver):
        self.operation = operation
        self.replicas = replicas
        self.conflict_resolver = conflict_resolver
        self.timestamp = time.time()
    
    def execute(self):
        results = {}
        conflicts = []
        
        for region, replica in self.replicas.items():
            try:
                result = replica.apply_operation(self.operation)
                results[region] = result
            except ConflictException as e:
                conflicts.append((region, e))
        
        if conflicts:
            return self.conflict_resolver.resolve(conflicts, self.operation)
        
        return results

# Mediator pattern for replica coordination
class SyncMediator:
    def __init__(self):
        self._replicas = []
        self._pending_operations = []
    
    def register_replica(self, replica):
        self._replicas.append(replica)
    
    def notify(self, sender, operation):
        # Coordinate sync across all replicas except sender
        for replica in self._replicas:
            if replica != sender:
                replica.receive_sync_operation(operation)
    
    def handle_network_partition(self, affected_replicas):
        # Implement partition tolerance strategy
        self._enter_partition_mode(affected_replicas)

# Observer pattern for change detection
class DatabaseReplica:
    def __init__(self, region):
        self.region = region
        self._observers = []
        self._vector_clock = VectorClock()
    
    def add_observer(self, observer):
        self._observers.append(observer)
    
    def apply_operation(self, operation):
        # Apply operation and notify observers
        result = self._execute_operation(operation)
        self._vector_clock.increment(self.region)
        
        for observer in self._observers:
            observer.notify(self, operation)
        
        return result
```

### 6. Design a data pipeline monitoring and alerting system
**Scenario**: Build a comprehensive monitoring system that can detect anomalies, predict failures, and automatically trigger remediation actions.

**Solution**:

```python
# Observer + Chain of Responsibility + Strategy + Command patterns
class PipelineMonitoringSystem:
    def __init__(self):
        self._monitors = []
        self._alert_chain = self._build_alert_chain()
        self._remediation_factory = RemediationFactory()
        self._observers = []
    
    def add_monitor(self, monitor):
        self._monitors.append(monitor)
        monitor.add_observer(self)
    
    def update(self, event):
        # Observer pattern - receive events from monitors
        alert = self._alert_chain.handle(event)
        if alert:
            self._trigger_remediation(alert)

# Chain of Responsibility for alert handling
class AlertHandler:
    def __init__(self):
        self._next_handler = None
    
    def set_next(self, handler):
        self._next_handler = handler
        return handler
    
    def handle(self, event):
        if self._can_handle(event):
            return self._process_alert(event)
        elif self._next_handler:
            return self._next_handler.handle(event)
        return None

class CriticalAlertHandler(AlertHandler):
    def _can_handle(self, event):
        return event.severity == "CRITICAL"
    
    def _process_alert(self, event):
        # Immediate notification and auto-remediation
        alert = Alert(event, priority="HIGH", auto_remediate=True)
        NotificationService.send_immediate(alert)
        return alert

class WarningAlertHandler(AlertHandler):
    def _can_handle(self, event):
        return event.severity == "WARNING"
    
    def _process_alert(self, event):
        # Aggregate warnings and send periodic notifications
        alert = Alert(event, priority="MEDIUM", auto_remediate=False)
        NotificationService.queue_for_batch(alert)
        return alert

# Strategy pattern for different monitoring strategies
class MonitoringStrategy:
    def monitor(self, pipeline_metrics): pass

class ThresholdMonitoring(MonitoringStrategy):
    def __init__(self, thresholds):
        self.thresholds = thresholds
    
    def monitor(self, metrics):
        violations = []
        for metric_name, value in metrics.items():
            if metric_name in self.thresholds:
                threshold = self.thresholds[metric_name]
                if value > threshold.max_value or value < threshold.min_value:
                    violations.append(ThresholdViolation(metric_name, value, threshold))
        return violations

class AnomalyDetectionMonitoring(MonitoringStrategy):
    def __init__(self, model):
        self.model = model
    
    def monitor(self, metrics):
        anomaly_score = self.model.predict_anomaly(metrics)
        if anomaly_score > 0.8:  # High anomaly score
            return [AnomalyDetection(metrics, anomaly_score)]
        return []

# Command pattern for remediation actions
class RemediationCommand:
    def execute(self): pass
    def undo(self): pass

class RestartPipelineCommand(RemediationCommand):
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.previous_state = None
    
    def execute(self):
        self.previous_state = self.pipeline.get_state()
        self.pipeline.restart()
        return f"Pipeline {self.pipeline.id} restarted"
    
    def undo(self):
        if self.previous_state:
            self.pipeline.restore_state(self.previous_state)

class ScaleUpCommand(RemediationCommand):
    def __init__(self, pipeline, scale_factor):
        self.pipeline = pipeline
        self.scale_factor = scale_factor
        self.original_capacity = None
    
    def execute(self):
        self.original_capacity = self.pipeline.get_capacity()
        new_capacity = self.original_capacity * self.scale_factor
        self.pipeline.set_capacity(new_capacity)
        return f"Pipeline scaled up to {new_capacity}"
    
    def undo(self):
        if self.original_capacity:
            self.pipeline.set_capacity(self.original_capacity)
```

## Meta (Facebook) Interview Questions

### 7. Design a real-time feature store for machine learning models
**Scenario**: Build a feature store that can serve features in real-time for ML models while maintaining consistency between batch and streaming features.

**Solution**:

```python
# Facade + Proxy + Strategy + Observer patterns
class FeatureStore:
    def __init__(self):
        self._batch_store = BatchFeatureStore()
        self._streaming_store = StreamingFeatureStore()
        self._cache = FeatureCache()
        self._consistency_manager = ConsistencyManager()
        self._observers = []
    
    def get_features(self, entity_id, feature_names, context=None):
        # Facade pattern - simplified interface for complex operations
        request = FeatureRequest(entity_id, feature_names, context)
        
        # Try cache first (Proxy pattern)
        cached_features = self._cache.get(request)
        if cached_features and self._is_cache_valid(cached_features):
            return cached_features
        
        # Fetch from appropriate store based on requirements
        features = self._fetch_features(request)
        
        # Cache the results
        self._cache.put(request, features)
        
        # Notify observers
        self._notify_observers(FeatureAccessEvent(request, features))
        
        return features
    
    def _fetch_features(self, request):
        if request.requires_real_time():
            return self._streaming_store.get_features(request)
        else:
            return self._batch_store.get_features(request)

# Proxy pattern for caching and access control
class FeatureCacheProxy:
    def __init__(self, feature_store, cache_ttl=300):
        self._feature_store = feature_store
        self._cache = {}
        self._cache_ttl = cache_ttl
        self._access_control = AccessController()
    
    def get_features(self, request):
        # Check access permissions
        if not self._access_control.can_access(request.user, request.feature_names):
            raise PermissionDeniedError("Access denied to requested features")
        
        # Check cache
        cache_key = self._generate_cache_key(request)
        if cache_key in self._cache:
            cached_entry = self._cache[cache_key]
            if time.time() - cached_entry.timestamp < self._cache_ttl:
                return cached_entry.features
        
        # Fetch from underlying store
        features = self._feature_store.get_features(request)
        
        # Update cache
        self._cache[cache_key] = CacheEntry(features, time.time())
        
        return features

# Strategy pattern for different feature computation strategies
class FeatureComputationStrategy:
    def compute(self, raw_data, feature_definition): pass

class BatchComputationStrategy(FeatureComputationStrategy):
    def compute(self, raw_data, feature_definition):
        # Batch processing using Spark/Hadoop
        return self._run_batch_job(raw_data, feature_definition)

class StreamingComputationStrategy(FeatureComputationStrategy):
    def compute(self, raw_data, feature_definition):
        # Real-time processing using Kafka Streams/Flink
        return self._process_stream(raw_data, feature_definition)

class OnDemandComputationStrategy(FeatureComputationStrategy):
    def compute(self, raw_data, feature_definition):
        # Compute features on-demand for low-latency serving
        return self._compute_immediately(raw_data, feature_definition)

# Observer pattern for feature lineage and monitoring
class FeatureObserver:
    def update(self, event): pass

class LineageTracker(FeatureObserver):
    def __init__(self):
        self._lineage_graph = LineageGraph()
    
    def update(self, event):
        if isinstance(event, FeatureComputationEvent):
            self._lineage_graph.add_dependency(
                event.output_feature,
                event.input_features,
                event.transformation
            )

class QualityMonitor(FeatureObserver):
    def __init__(self):
        self._quality_metrics = {}
    
    def update(self, event):
        if isinstance(event, FeatureAccessEvent):
            self._update_quality_metrics(event.features)
            self._check_data_drift(event.features)

# Template Method for feature pipeline execution
class FeaturePipeline:
    def execute(self, input_data):
        # Template method defining the algorithm structure
        validated_data = self.validate_input(input_data)
        raw_features = self.extract_features(validated_data)
        transformed_features = self.transform_features(raw_features)
        final_features = self.post_process(transformed_features)
        self.store_features(final_features)
        return final_features
    
    def validate_input(self, data):
        # Default implementation
        if not data:
            raise ValueError("Empty input data")
        return data
    
    def extract_features(self, data):
        # Must be implemented by subclasses
        raise NotImplementedError
    
    def transform_features(self, features):
        # Default implementation - no transformation
        return features
    
    def post_process(self, features):
        # Default implementation - no post-processing
        return features
    
    def store_features(self, features):
        # Must be implemented by subclasses
        raise NotImplementedError
```

### 8. Design a data privacy and compliance system for user data
**Scenario**: Build a system that ensures user data privacy compliance (GDPR, CCPA) while maintaining data utility for analytics and ML.

**Solution**:

```python
# Decorator + Strategy + Chain of Responsibility + Command patterns
class PrivacyComplianceSystem:
    def __init__(self):
        self._privacy_policies = PolicyRegistry()
        self._anonymization_strategies = AnonymizationFactory()
        self._audit_logger = AuditLogger()
        self._consent_manager = ConsentManager()
    
    def process_data(self, data, processing_purpose, user_consent=None):
        # Chain of responsibility for compliance checks
        compliance_chain = self._build_compliance_chain()
        compliance_result = compliance_chain.handle(
            ComplianceRequest(data, processing_purpose, user_consent)
        )
        
        if not compliance_result.is_compliant:
            raise ComplianceViolationError(compliance_result.violations)
        
        # Apply privacy transformations
        processed_data = self._apply_privacy_transformations(
            data, compliance_result.required_transformations
        )
        
        # Log for audit
        self._audit_logger.log_processing(data, processed_data, processing_purpose)
        
        return processed_data

# Decorator pattern for privacy-preserving transformations
class PrivacyDecorator:
    def __init__(self, data_processor):
        self._data_processor = data_processor
    
    def process(self, data):
        return self._data_processor.process(data)

class AnonymizationDecorator(PrivacyDecorator):
    def __init__(self, data_processor, anonymization_strategy):
        super().__init__(data_processor)
        self._strategy = anonymization_strategy
    
    def process(self, data):
        anonymized_data = self._strategy.anonymize(data)
        return self._data_processor.process(anonymized_data)

class EncryptionDecorator(PrivacyDecorator):
    def __init__(self, data_processor, encryption_key):
        super().__init__(data_processor)
        self._encryption_key = encryption_key
    
    def process(self, data):
        encrypted_data = self._encrypt_sensitive_fields(data)
        return self._data_processor.process(encrypted_data)

# Strategy pattern for different anonymization techniques
class AnonymizationStrategy:
    def anonymize(self, data): pass

class KAnonymityStrategy(AnonymizationStrategy):
    def __init__(self, k=5):
        self.k = k
    
    def anonymize(self, data):
        # Implement k-anonymity algorithm
        return self._generalize_quasi_identifiers(data, self.k)

class DifferentialPrivacyStrategy(AnonymizationStrategy):
    def __init__(self, epsilon=1.0):
        self.epsilon = epsilon
    
    def anonymize(self, data):
        # Add calibrated noise for differential privacy
        return self._add_laplace_noise(data, self.epsilon)

class DataMaskingStrategy(AnonymizationStrategy):
    def __init__(self, masking_rules):
        self.masking_rules = masking_rules
    
    def anonymize(self, data):
        masked_data = data.copy()
        for field, rule in self.masking_rules.items():
            if field in masked_data:
                masked_data[field] = rule.apply(masked_data[field])
        return masked_data

# Chain of Responsibility for compliance checks
class ComplianceHandler:
    def __init__(self):
        self._next_handler = None
    
    def set_next(self, handler):
        self._next_handler = handler
        return handler
    
    def handle(self, request):
        result = self._check_compliance(request)
        if result.needs_further_check and self._next_handler:
            next_result = self._next_handler.handle(request)
            return result.merge(next_result)
        return result

class GDPRComplianceHandler(ComplianceHandler):
    def _check_compliance(self, request):
        violations = []
        required_transformations = []
        
        # Check lawful basis for processing
        if not self._has_lawful_basis(request):
            violations.append("No lawful basis for processing")
        
        # Check data minimization
        if self._violates_data_minimization(request):
            violations.append("Data minimization violation")
            required_transformations.append("field_filtering")
        
        # Check purpose limitation
        if self._violates_purpose_limitation(request):
            violations.append("Purpose limitation violation")
        
        return ComplianceResult(
            is_compliant=len(violations) == 0,
            violations=violations,
            required_transformations=required_transformations
        )

class CCPAComplianceHandler(ComplianceHandler):
    def _check_compliance(self, request):
        violations = []
        required_transformations = []
        
        # Check consumer rights
        if request.user_consent and request.user_consent.has_opt_out:
            violations.append("User has opted out of data processing")
        
        # Check data categories
        if self._contains_sensitive_personal_info(request.data):
            required_transformations.append("anonymization")
        
        return ComplianceResult(
            is_compliant=len(violations) == 0,
            violations=violations,
            required_transformations=required_transformations
        )

# Command pattern for data subject rights
class DataSubjectRightsCommand:
    def execute(self): pass
    def can_execute(self): pass

class DataDeletionCommand(DataSubjectRightsCommand):
    def __init__(self, user_id, data_stores):
        self.user_id = user_id
        self.data_stores = data_stores
        self.deleted_data = {}
    
    def execute(self):
        for store_name, store in self.data_stores.items():
            deleted = store.delete_user_data(self.user_id)
            self.deleted_data[store_name] = deleted
        
        return f"Deleted data for user {self.user_id} from {len(self.data_stores)} stores"
    
    def can_execute(self):
        # Check if deletion is legally required and technically feasible
        return all(store.supports_deletion() for store in self.data_stores.values())

class DataPortabilityCommand(DataSubjectRightsCommand):
    def __init__(self, user_id, data_stores, export_format="json"):
        self.user_id = user_id
        self.data_stores = data_stores
        self.export_format = export_format
    
    def execute(self):
        user_data = {}
        for store_name, store in self.data_stores.items():
            data = store.get_user_data(self.user_id)
            user_data[store_name] = data
        
        exporter = DataExporterFactory.create_exporter(self.export_format)
        return exporter.export(user_data)
```

These Big4 interview questions demonstrate advanced system design scenarios that require combining multiple design patterns to solve complex, real-world problems. Each solution shows how different patterns work together to create robust, scalable, and maintainable systems.