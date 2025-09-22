# Apache Beam Best Practices

## 1. Pipeline Design Principles

### Unified Batch and Streaming
```python
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

def create_unified_pipeline(is_streaming=False):
    """Create pipeline that works for both batch and streaming."""
    
    options = PipelineOptions([
        '--runner=DataflowRunner' if is_streaming else '--runner=DirectRunner',
        '--streaming' if is_streaming else '',
        '--project=my-project',
        '--region=us-central1'
    ])
    
    with beam.Pipeline(options=options) as pipeline:
        if is_streaming:
            # Streaming source
            data = (pipeline 
                   | 'Read Stream' >> beam.io.ReadFromPubSub(topic='projects/my-project/topics/input'))
        else:
            # Batch source
            data = (pipeline 
                   | 'Read Batch' >> beam.io.ReadFromText('gs://my-bucket/input/*'))
        
        # Same processing logic for both
        processed = (data
                    | 'Parse' >> beam.Map(parse_json)
                    | 'Filter' >> beam.Filter(lambda x: x.get('amount', 0) > 0)
                    | 'Transform' >> beam.Map(enrich_data)
                    | 'Window' >> beam.WindowInto(beam.window.FixedWindows(300))  # 5-min windows
                    | 'Aggregate' >> beam.CombinePerKey(sum))
        
        if is_streaming:
            # Streaming sink
            (processed 
             | 'Write Stream' >> beam.io.WriteToPubSub(topic='projects/my-project/topics/output'))
        else:
            # Batch sink
            (processed 
             | 'Write Batch' >> beam.io.WriteToText('gs://my-bucket/output/results'))

def parse_json(element):
    import json
    try:
        return json.loads(element)
    except:
        return {}

def enrich_data(element):
    element['processed_at'] = beam.utils.timestamp.Timestamp.now().to_rfc3339()
    return element
```

### Composite Transforms
```python
class ProcessSalesData(beam.PTransform):
    """Reusable composite transform for sales data processing."""
    
    def __init__(self, validation_rules=None):
        self.validation_rules = validation_rules or {}
    
    def expand(self, pcoll):
        return (pcoll
               | 'Parse JSON' >> beam.Map(self._parse_json)
               | 'Validate' >> beam.Filter(self._validate_record)
               | 'Enrich' >> beam.Map(self._enrich_record)
               | 'Format' >> beam.Map(self._format_output))
    
    def _parse_json(self, element):
        import json
        try:
            return json.loads(element)
        except json.JSONDecodeError:
            return None
    
    def _validate_record(self, record):
        if not record:
            return False
        
        required_fields = ['customer_id', 'amount', 'timestamp']
        return all(field in record for field in required_fields)
    
    def _enrich_record(self, record):
        # Add derived fields
        record['amount_category'] = 'high' if record['amount'] > 1000 else 'low'
        record['processing_time'] = beam.utils.timestamp.Timestamp.now().to_rfc3339()
        return record
    
    def _format_output(self, record):
        return f"{record['customer_id']},{record['amount']},{record['amount_category']}"

# Usage
with beam.Pipeline() as pipeline:
    sales_data = (pipeline
                 | 'Read Sales' >> beam.io.ReadFromText('sales/*.json')
                 | 'Process Sales' >> ProcessSalesData()
                 | 'Write Results' >> beam.io.WriteToText('output/processed_sales'))
```

## 2. Performance Optimization

### Memory Management
```java
// Efficient DoFn with resource management
public class OptimizedProcessingDoFn extends DoFn<InputEvent, OutputEvent> {
    
    private transient DatabaseConnection connection;
    private transient ObjectMapper jsonMapper;
    private final Counter processedCounter = Metrics.counter("processing", "events");
    
    @Setup
    public void setup() {
        // Initialize expensive resources once per worker
        connection = DatabaseConnectionPool.getConnection();
        jsonMapper = new ObjectMapper();
        jsonMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
    }
    
    @ProcessElement
    public void processElement(ProcessContext c) {
        InputEvent input = c.element();
        
        try {
            // Efficient processing with minimal object creation
            OutputEvent output = processEvent(input);
            c.output(output);
            processedCounter.inc();
            
        } catch (Exception e) {
            // Handle errors gracefully
            LOG.warn("Failed to process event: " + input.getId(), e);
        }
    }
    
    @Teardown
    public void teardown() {
        // Clean up resources
        if (connection != null) {
            connection.close();
        }
    }
    
    private OutputEvent processEvent(InputEvent input) {
        // Reuse objects where possible
        return OutputEvent.builder()
            .setId(input.getId())
            .setProcessedData(transformData(input.getData()))
            .setTimestamp(Instant.now())
            .build();
    }
}
```

### Hot Key Mitigation
```java
public class HotKeyMitigationExample {
    
    public static PCollection<KV<String, ProcessedEvent>> mitigateHotKeys(
            PCollection<KV<String, Event>> input) {
        
        return input
            .apply("Detect and Distribute Hot Keys", ParDo.of(new DoFn<KV<String, Event>, KV<String, Event>>() {
                
                private final Set<String> knownHotKeys = ImmutableSet.of("popular_key", "trending_topic");
                
                @ProcessElement
                public void processElement(ProcessContext c) {
                    KV<String, Event> element = c.element();
                    String originalKey = element.getKey();
                    Event event = element.getValue();
                    
                    String newKey;
                    if (knownHotKeys.contains(originalKey) || isHotKey(originalKey, event)) {
                        // Distribute hot keys across multiple partitions
                        int partition = Math.abs(event.getId().hashCode()) % 10;
                        newKey = originalKey + "_partition_" + partition;
                    } else {
                        newKey = originalKey;
                    }
                    
                    c.output(KV.of(newKey, event));
                }
                
                private boolean isHotKey(String key, Event event) {
                    // Dynamic hot key detection logic
                    return event.getVolume() > 1000;
                }
            }))
            .apply("Process Events", ParDo.of(new ProcessEventDoFn()))
            .apply("Merge Partitioned Results", ParDo.of(new DoFn<KV<String, ProcessedEvent>, KV<String, ProcessedEvent>>() {
                @ProcessElement
                public void processElement(ProcessContext c) {
                    KV<String, ProcessedEvent> element = c.element();
                    String key = element.getKey();
                    
                    // Remove partition suffix for final output
                    if (key.contains("_partition_")) {
                        key = key.substring(0, key.indexOf("_partition_"));
                    }
                    
                    c.output(KV.of(key, element.getValue()));
                }
            }));
    }
}
```

### Efficient Windowing
```python
def optimized_windowing_pipeline():
    """Demonstrate efficient windowing patterns."""
    
    with beam.Pipeline() as pipeline:
        events = (pipeline 
                 | 'Read Events' >> beam.io.ReadFromPubSub(topic='events')
                 | 'Parse Events' >> beam.Map(json.loads)
                 | 'Add Timestamps' >> beam.Map(lambda x: beam.window.TimestampedValue(x, x['timestamp'])))
        
        # Efficient fixed windows with early triggers
        windowed_events = (events
                          | 'Fixed Windows' >> beam.WindowInto(
                              beam.window.FixedWindows(300),  # 5-minute windows
                              trigger=beam.transforms.trigger.AfterWatermark(
                                  early=beam.transforms.trigger.AfterProcessingTime(60),  # Early firing every minute
                                  late=beam.transforms.trigger.AfterProcessingTime(300)   # Late firing every 5 minutes
                              ),
                              accumulation_mode=beam.transforms.trigger.AccumulationMode.ACCUMULATING,
                              allowed_lateness=1800  # Allow 30 minutes of late data
                          ))
        
        # Efficient aggregation
        aggregated = (windowed_events
                     | 'Key by Type' >> beam.Map(lambda x: (x['event_type'], x))
                     | 'Count by Type' >> beam.combiners.Count.PerKey()
                     | 'Format Results' >> beam.Map(lambda kv: f"{kv[0]}: {kv[1]}"))
        
        # Batch output for efficiency
        (aggregated 
         | 'Write Results' >> beam.io.WriteToText(
             'gs://output-bucket/results',
             num_shards=10,  # Parallel writes
             shard_name_template='_SSSSS-of-NNNNN'
         ))
```

## 3. Error Handling and Monitoring

### Comprehensive Error Handling
```java
public class RobustProcessingPipeline {
    
    public static void createRobustPipeline(Pipeline pipeline) {
        // Define output tags for different result types
        final TupleTag<ProcessedEvent> successTag = new TupleTag<ProcessedEvent>(){};
        final TupleTag<FailedEvent> errorTag = new TupleTag<FailedEvent>(){};
        final TupleTag<String> deadLetterTag = new TupleTag<String>(){};
        
        PCollection<String> input = pipeline
            .apply("Read Input", TextIO.read().from("gs://input-bucket/*"));
        
        // Process with comprehensive error handling
        PCollectionTuple results = input
            .apply("Process with Error Handling", ParDo.of(new DoFn<String, ProcessedEvent>() {
                
                private final Counter successCounter = Metrics.counter("processing", "success");
                private final Counter errorCounter = Metrics.counter("processing", "errors");
                private final Counter deadLetterCounter = Metrics.counter("processing", "dead_letters");
                
                @ProcessElement
                public void processElement(ProcessContext c) {
                    String element = c.element();
                    
                    try {
                        // Attempt to parse and validate
                        Event event = parseEvent(element);
                        if (isValid(event)) {
                            ProcessedEvent processed = processEvent(event);
                            c.output(successTag, processed);
                            successCounter.inc();
                        } else {
                            // Invalid but parseable data
                            FailedEvent failed = new FailedEvent(element, "Validation failed", Instant.now());
                            c.output(errorTag, failed);
                            errorCounter.inc();
                        }
                        
                    } catch (ParseException e) {
                        // Unparseable data goes to dead letter queue
                        c.output(deadLetterTag, element);
                        deadLetterCounter.inc();
                        
                    } catch (Exception e) {
                        // Other processing errors
                        FailedEvent failed = new FailedEvent(element, e.getMessage(), Instant.now());
                        c.output(errorTag, failed);
                        errorCounter.inc();
                    }
                }
            }).withOutputTags(successTag, TupleTagList.of(errorTag, deadLetterTag)));
        
        // Handle successful processing
        results.get(successTag)
            .apply("Write Success", TextIO.write().to("gs://output-bucket/success/"));
        
        // Handle processing errors (retryable)
        results.get(errorTag)
            .apply("Write Errors", TextIO.write().to("gs://output-bucket/errors/"));
        
        // Handle dead letters (non-retryable)
        results.get(deadLetterTag)
            .apply("Write Dead Letters", TextIO.write().to("gs://output-bucket/dead-letters/"));
    }
}
```

### Monitoring and Alerting
```java
public class MonitoringBestPractices {
    
    public static class MonitoredDoFn extends DoFn<InputEvent, OutputEvent> {
        
        // Comprehensive metrics
        private final Counter elementsProcessed = Metrics.counter("pipeline", "elements_processed");
        private final Counter processingErrors = Metrics.counter("pipeline", "processing_errors");
        private final Distribution processingLatency = Metrics.distribution("pipeline", "processing_latency_ms");
        private final Gauge<Long> currentBacklog = Metrics.gauge("pipeline", "current_backlog");
        
        // Business metrics
        private final Counter highValueTransactions = Metrics.counter("business", "high_value_transactions");
        private final Distribution transactionAmounts = Metrics.distribution("business", "transaction_amounts");
        
        @ProcessElement
        public void processElement(ProcessContext c) {
            long startTime = System.currentTimeMillis();
            
            try {
                InputEvent input = c.element();
                
                // Process the element
                OutputEvent output = processEvent(input);
                
                // Update metrics
                elementsProcessed.inc();
                processingLatency.update(System.currentTimeMillis() - startTime);
                
                // Business metrics
                if (output.getAmount() > 10000) {
                    highValueTransactions.inc();
                }
                transactionAmounts.update((long) output.getAmount());
                
                c.output(output);
                
            } catch (Exception e) {
                processingErrors.inc();
                throw e;
            }
        }
        
        @StartBundle
        public void startBundle() {
            // Update backlog metric (example)
            currentBacklog.set(getCurrentBacklogSize());
        }
        
        private long getCurrentBacklogSize() {
            // Implementation to get current backlog size
            return 0L;
        }
    }
    
    // Health check transform
    public static class HealthCheckTransform extends PTransform<PCollection<String>, PCollection<HealthStatus>> {
        
        @Override
        public PCollection<HealthStatus> expand(PCollection<String> input) {
            return input
                .apply("Add Health Check", ParDo.of(new DoFn<String, HealthStatus>() {
                    
                    private final Gauge<String> healthStatus = Metrics.gauge("health", "status");
                    
                    @ProcessElement
                    public void processElement(ProcessContext c) {
                        try {
                            // Perform health checks
                            boolean isHealthy = performHealthChecks();
                            
                            HealthStatus status = new HealthStatus(
                                isHealthy ? "HEALTHY" : "UNHEALTHY",
                                Instant.now(),
                                getHealthDetails()
                            );
                            
                            healthStatus.set(status.getStatus());
                            c.output(status);
                            
                        } catch (Exception e) {
                            healthStatus.set("ERROR");
                            c.output(new HealthStatus("ERROR", Instant.now(), e.getMessage()));
                        }
                    }
                    
                    private boolean performHealthChecks() {
                        // Check external dependencies
                        // Check processing latency
                        // Check error rates
                        return true;
                    }
                    
                    private String getHealthDetails() {
                        return "All systems operational";
                    }
                }));
        }
    }
}
```

## 4. Testing Strategies

### Unit Testing
```java
@Test
public void testProcessingDoFn() throws Exception {
    // Create test DoFn
    ProcessEventDoFn fn = new ProcessEventDoFn();
    
    // Test successful processing
    DoFnTester<InputEvent, OutputEvent> fnTester = DoFnTester.of(fn);
    
    InputEvent input = new InputEvent("test-id", "test-data", Instant.now());
    List<OutputEvent> outputs = fnTester.processBundle(input);
    
    assertEquals(1, outputs.size());
    assertEquals("test-id", outputs.get(0).getId());
}

@Test
public void testPipelineWithTestStream() {
    Pipeline pipeline = TestPipeline.create();
    
    // Create test data with timestamps
    TestStream<String> testStream = TestStream.create(StringUtf8Coder.of())
        .addElements("event1", "event2")
        .advanceWatermarkTo(Instant.ofEpochSecond(100))
        .addElements("event3")
        .advanceWatermarkToInfinity();
    
    PCollection<String> input = pipeline.apply("Test Input", testStream);
    
    PCollection<String> output = input
        .apply("Process", ParDo.of(new ProcessStringDoFn()));
    
    // Assert expected outputs
    PAssert.that(output).containsInAnyOrder("processed-event1", "processed-event2", "processed-event3");
    
    pipeline.run();
}
```

### Integration Testing
```java
@Test
public void testEndToEndPipeline() {
    // Use TestPipeline for integration testing
    TestPipelineOptions options = TestPipelineOptions.fromArgs(
        "--runner=DirectRunner",
        "--tempLocation=gs://test-bucket/temp"
    );
    
    Pipeline pipeline = TestPipeline.create(options);
    
    // Use real I/O with test data
    PCollection<String> input = pipeline
        .apply("Read Test Data", TextIO.read().from("gs://test-bucket/input/*"));
    
    PCollection<String> output = input
        .apply("Process", new ProcessingTransform());
    
    // Write to test output location
    output.apply("Write Results", TextIO.write().to("gs://test-bucket/output/"));
    
    PipelineResult result = pipeline.run();
    result.waitUntilFinish();
    
    // Verify output files
    verifyOutputFiles("gs://test-bucket/output/");
}
```

## 5. Deployment and Operations

### CI/CD Pipeline
```yaml
# .github/workflows/beam-pipeline.yml
name: Beam Pipeline CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up JDK 11
      uses: actions/setup-java@v2
      with:
        java-version: '11'
        distribution: 'adopt'
    
    - name: Run unit tests
      run: mvn test
    
    - name: Run integration tests
      run: mvn verify -Pintegration-tests
    
    - name: Build pipeline JAR
      run: mvn clean package -DskipTests

  deploy-staging:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - name: Deploy to staging
      run: |
        gcloud dataflow jobs run staging-pipeline \
          --gcs-location gs://templates/pipeline-template \
          --region us-central1 \
          --parameters inputTopic=projects/project/topics/staging-input,outputTopic=projects/project/topics/staging-output

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    steps:
    - name: Deploy to production
      run: |
        gcloud dataflow jobs run production-pipeline \
          --gcs-location gs://templates/pipeline-template \
          --region us-central1 \
          --parameters inputTopic=projects/project/topics/prod-input,outputTopic=projects/project/topics/prod-output
```

### Configuration Management
```java
public class ConfigurationBestPractices {
    
    // Use pipeline options for configuration
    public interface MyPipelineOptions extends PipelineOptions {
        @Description("Input topic")
        @Validation.Required
        String getInputTopic();
        void setInputTopic(String value);
        
        @Description("Output topic")
        @Validation.Required
        String getOutputTopic();
        void setOutputTopic(String value);
        
        @Description("Processing timeout in seconds")
        @Default.Integer(300)
        Integer getProcessingTimeout();
        void setProcessingTimeout(Integer value);
        
        @Description("Enable debug mode")
        @Default.Boolean(false)
        Boolean getDebugMode();
        void setDebugMode(Boolean value);
    }
    
    public static void main(String[] args) {
        MyPipelineOptions options = PipelineOptionsFactory.fromArgs(args)
            .withValidation()
            .as(MyPipelineOptions.class);
        
        Pipeline pipeline = Pipeline.create(options);
        
        // Use configuration throughout pipeline
        PCollection<String> input = pipeline
            .apply("Read Input", PubsubIO.readStrings().fromTopic(options.getInputTopic()));
        
        PCollection<String> processed = input
            .apply("Process", ParDo.of(new ConfigurableProcessDoFn(options)));
        
        processed
            .apply("Write Output", PubsubIO.writeStrings().to(options.getOutputTopic()));
        
        pipeline.run();
    }
    
    public static class ConfigurableProcessDoFn extends DoFn<String, String> {
        private final MyPipelineOptions options;
        
        public ConfigurableProcessDoFn(MyPipelineOptions options) {
            this.options = options;
        }
        
        @ProcessElement
        public void processElement(ProcessContext c) {
            String input = c.element();
            
            if (options.getDebugMode()) {
                LOG.info("Processing element: " + input);
            }
            
            // Use timeout configuration
            String processed = processWithTimeout(input, options.getProcessingTimeout());
            c.output(processed);
        }
    }
}
```

## 6. Security and Compliance

### Data Privacy and Security
```java
public class SecurityBestPractices {
    
    // Data masking transform
    public static class DataMaskingDoFn extends DoFn<CustomerRecord, CustomerRecord> {
        
        @ProcessElement
        public void processElement(ProcessContext c) {
            CustomerRecord record = c.element();
            
            // Mask sensitive data
            CustomerRecord masked = CustomerRecord.builder()
                .setId(record.getId())
                .setName(maskName(record.getName()))
                .setEmail(maskEmail(record.getEmail()))
                .setPhone(maskPhone(record.getPhone()))
                .setAddress(record.getAddress()) // Keep address for analytics
                .build();
            
            c.output(masked);
        }
        
        private String maskName(String name) {
            if (name == null || name.length() < 2) return "***";
            return name.charAt(0) + "***" + name.charAt(name.length() - 1);
        }
        
        private String maskEmail(String email) {
            if (email == null || !email.contains("@")) return "***@***.com";
            String[] parts = email.split("@");
            return parts[0].charAt(0) + "***@" + parts[1];
        }
        
        private String maskPhone(String phone) {
            if (phone == null || phone.length() < 4) return "***-***-****";
            return "***-***-" + phone.substring(phone.length() - 4);
        }
    }
    
    // Audit logging transform
    public static class AuditLoggingDoFn extends DoFn<DataRecord, DataRecord> {
        
        @ProcessElement
        public void processElement(ProcessContext c) {
            DataRecord record = c.element();
            
            // Log data access for compliance
            AuditLog auditLog = AuditLog.builder()
                .setUserId(getCurrentUserId())
                .setAction("DATA_PROCESSED")
                .setResourceId(record.getId())
                .setTimestamp(Instant.now())
                .setDetails("Record processed in pipeline")
                .build();
            
            // Send to audit system
            sendToAuditSystem(auditLog);
            
            c.output(record);
        }
        
        private String getCurrentUserId() {
            // Get current user context
            return "pipeline-service-account";
        }
        
        private void sendToAuditSystem(AuditLog log) {
            // Send to compliance audit system
        }
    }
}
```

This comprehensive best practices guide covers all major aspects of Apache Beam development, from pipeline design to production deployment and security considerations.