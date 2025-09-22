# Apache Flink Best Practices

## 1. Performance Optimization

### Memory Management
```java
// Optimal memory configuration
Configuration config = new Configuration();
config.setString("taskmanager.memory.process.size", "4g");
config.setString("taskmanager.memory.flink.size", "3.2g");
config.setFloat("taskmanager.memory.network.fraction", 0.15f);
config.setFloat("taskmanager.memory.managed.fraction", 0.4f);

// Enable object reuse for better performance
env.getConfig().enableObjectReuse();
```

### Parallelism Tuning
```java
// Set appropriate parallelism
env.setParallelism(Runtime.getRuntime().availableProcessors() * 2);
env.setMaxParallelism(128); // For future scaling

// Operator-specific parallelism
stream.map(new MapFunction()).setParallelism(16);
stream.keyBy().window().aggregate().setParallelism(8);
```

### Serialization Optimization
```java
// Register custom serializers
env.getConfig().registerKryoType(CustomEvent.class);
env.getConfig().registerTypeWithKryoSerializer(
    CustomEvent.class, CustomEventSerializer.class);

// Use Avro for complex objects
env.getConfig().enableForceAvro();
```

## 2. State Management

### State Backend Configuration
```java
// RocksDB for large state
RocksDBStateBackend rocksDBBackend = new RocksDBStateBackend("s3://flink-state/");
rocksDBBackend.setIncremental(true);
rocksDBBackend.setPredefinedOptions(PredefinedOptions.SPINNING_DISK_OPTIMIZED);
env.setStateBackend(rocksDBBackend);

// State TTL configuration
StateTtlConfig ttlConfig = StateTtlConfig
    .newBuilder(Time.hours(24))
    .setUpdateType(StateTtlConfig.UpdateType.OnCreateAndWrite)
    .setStateVisibility(StateTtlConfig.StateVisibility.NeverReturnExpired)
    .cleanupIncrementally(10, true)
    .build();
```

### Efficient State Usage
```java
public class EfficientStateFunction extends KeyedProcessFunction<String, Event, Result> {
    
    // Use appropriate state type
    private ValueState<Long> countState;
    private MapState<String, Double> aggregateState;
    private ListState<Event> bufferState;
    
    @Override
    public void open(Configuration parameters) {
        // Configure state with TTL
        ValueStateDescriptor<Long> countDesc = 
            new ValueStateDescriptor<>("count", Long.class, 0L);
        countDesc.enableTimeToLive(ttlConfig);
        countState = getRuntimeContext().getState(countDesc);
    }
    
    @Override
    public void processElement(Event event, Context ctx, Collector<Result> out) {
        // Efficient state access
        Long count = countState.value();
        countState.update(count + 1);
        
        // Clear state when no longer needed
        if (count > 1000) {
            countState.clear();
        }
    }
}
```

## 3. Checkpointing and Fault Tolerance

### Checkpoint Configuration
```java
// Production checkpoint settings
env.enableCheckpointing(60000, CheckpointingMode.EXACTLY_ONCE);
env.getCheckpointConfig().setMinPauseBetweenCheckpoints(30000);
env.getCheckpointConfig().setCheckpointTimeout(300000);
env.getCheckpointConfig().setMaxConcurrentCheckpoints(1);
env.getCheckpointConfig().setTolerableCheckpointFailureNumber(3);

// Externalized checkpoints
env.getCheckpointConfig().setExternalizedCheckpointCleanup(
    CheckpointConfig.ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION
);

// Checkpoint storage
env.getCheckpointConfig().setCheckpointStorage("s3://flink-checkpoints/");
```

### Restart Strategies
```java
// Exponential delay restart
env.setRestartStrategy(RestartStrategies.exponentialDelayRestart(
    Time.seconds(1),    // initial backoff
    Time.minutes(10),   // max backoff
    1.2,               // backoff multiplier
    Time.minutes(5),   // reset backoff threshold
    0.1                // jitter factor
));

// Fixed delay restart
env.setRestartStrategy(RestartStrategies.fixedDelayRestart(
    3,                 // max attempts
    Time.seconds(30)   // delay between attempts
));
```

## 4. Windowing Best Practices

### Efficient Window Operations
```java
// Use appropriate window type
DataStream<Event> windowed = stream
    .keyBy(Event::getKey)
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .allowedLateness(Time.minutes(1))
    .sideOutputLateData(lateDataTag)
    .aggregate(new EfficientAggregator());

// Custom window function for complex logic
public class EfficientWindowFunction 
    extends ProcessWindowFunction<Event, Result, String, TimeWindow> {
    
    @Override
    public void process(String key, Context context, 
                       Iterable<Event> elements, Collector<Result> out) {
        
        // Efficient processing
        long count = 0;
        double sum = 0;
        
        for (Event event : elements) {
            count++;
            sum += event.getValue();
        }
        
        out.collect(new Result(key, count, sum / count));
    }
}
```

### Watermark Strategies
```java
// Bounded out-of-orderness
WatermarkStrategy<Event> watermarkStrategy = WatermarkStrategy
    .<Event>forBoundedOutOfOrderness(Duration.ofSeconds(10))
    .withTimestampAssigner((event, timestamp) -> event.getTimestamp())
    .withIdleness(Duration.ofMinutes(1));

// Custom watermark generator
public class CustomWatermarkGenerator implements WatermarkGenerator<Event> {
    private long maxTimestamp = Long.MIN_VALUE;
    private final long outOfOrdernessMillis = 5000;
    
    @Override
    public void onEvent(Event event, long eventTimestamp, WatermarkOutput output) {
        maxTimestamp = Math.max(maxTimestamp, eventTimestamp);
    }
    
    @Override
    public void onPeriodicEmit(WatermarkOutput output) {
        output.emitWatermark(new Watermark(maxTimestamp - outOfOrdernessMillis));
    }
}
```

## 5. Resource Management

### Slot Sharing and Resource Groups
```java
// Organize operators by resource requirements
stream
    .map(new CPUIntensiveFunction())
    .slotSharingGroup("cpu-intensive")
    .setParallelism(16)
    .keyBy(Event::getKey)
    .process(new MemoryIntensiveFunction())
    .slotSharingGroup("memory-intensive")
    .setParallelism(8)
    .addSink(new IOIntensiveSink())
    .slotSharingGroup("io-intensive")
    .setParallelism(4);

// Resource specifications
ResourceSpec resourceSpec = ResourceSpec.newBuilder()
    .setCpuCores(2.0)
    .setHeapMemoryInMB(2048)
    .setDirectMemoryInMB(512)
    .build();

stream.setResources(resourceSpec);
```

### Network Buffer Tuning
```java
Configuration config = new Configuration();
config.setString("taskmanager.network.memory.fraction", "0.15");
config.setString("taskmanager.network.memory.min", "128mb");
config.setString("taskmanager.network.memory.max", "1gb");
config.setInteger("taskmanager.network.numberOfBuffers", 8192);
```

## 6. Monitoring and Observability

### Metrics Configuration
```java
// Enable comprehensive metrics
Configuration config = new Configuration();
config.setString("metrics.reporters", "prometheus,jmx");
config.setString("metrics.reporter.prometheus.class", 
    "org.apache.flink.metrics.prometheus.PrometheusReporter");
config.setString("metrics.reporter.prometheus.port", "9249");

// Custom metrics
public class MetricsCollectingFunction extends RichMapFunction<Event, Event> {
    private Counter processedRecords;
    private Histogram processingLatency;
    private Gauge<Double> currentLoad;
    
    @Override
    public void open(Configuration parameters) {
        MetricGroup metricGroup = getRuntimeContext().getMetricGroup();
        
        processedRecords = metricGroup.counter("processed_records");
        processingLatency = metricGroup.histogram("processing_latency");
        currentLoad = metricGroup.gauge("current_load", this::calculateLoad);
    }
    
    @Override
    public Event map(Event event) throws Exception {
        long startTime = System.currentTimeMillis();
        
        // Process event
        Event result = processEvent(event);
        
        // Update metrics
        processedRecords.inc();
        processingLatency.update(System.currentTimeMillis() - startTime);
        
        return result;
    }
}
```

### Health Checks
```java
public class HealthCheckFunction extends RichMapFunction<Event, Event> {
    private Gauge<String> healthStatus;
    private long lastHealthCheck;
    
    @Override
    public void open(Configuration parameters) {
        MetricGroup healthGroup = getRuntimeContext().getMetricGroup()
            .addGroup("health");
        
        healthStatus = healthGroup.gauge("status", this::getHealthStatus);
        lastHealthCheck = System.currentTimeMillis();
    }
    
    private String getHealthStatus() {
        long timeSinceLastCheck = System.currentTimeMillis() - lastHealthCheck;
        
        if (timeSinceLastCheck > 60000) {
            return "UNHEALTHY";
        } else if (timeSinceLastCheck > 30000) {
            return "WARNING";
        } else {
            return "HEALTHY";
        }
    }
}
```

## 7. Security Best Practices

### SSL/TLS Configuration
```yaml
# flink-conf.yaml
security.ssl.enabled: true
security.ssl.keystore: /path/to/keystore.jks
security.ssl.keystore-password: ${KEYSTORE_PASSWORD}
security.ssl.truststore: /path/to/truststore.jks
security.ssl.truststore-password: ${TRUSTSTORE_PASSWORD}

# Internal communication
security.ssl.internal.enabled: true
security.ssl.internal.keystore: /path/to/internal-keystore.jks
security.ssl.internal.keystore-password: ${INTERNAL_KEYSTORE_PASSWORD}

# REST API
security.ssl.rest.enabled: true
security.ssl.rest.keystore: /path/to/rest-keystore.jks
security.ssl.rest.keystore-password: ${REST_KEYSTORE_PASSWORD}
```

### Kerberos Authentication
```yaml
# Kerberos configuration
security.kerberos.login.use-ticket-cache: true
security.kerberos.login.keytab: /path/to/flink.keytab
security.kerberos.login.principal: flink/hostname@REALM
security.kerberos.login.contexts: Client,KafkaClient
```

## 8. Testing Strategies

### Unit Testing
```java
@Test
public void testMapFunction() throws Exception {
    MapFunction<String, Integer> mapFunction = new StringLengthMapper();
    
    assertEquals(5, (int) mapFunction.map("hello"));
    assertEquals(0, (int) mapFunction.map(""));
}

@Test
public void testStatefulFunction() throws Exception {
    CountingMapFunction function = new CountingMapFunction();
    
    OneInputStreamOperatorTestHarness<String, Tuple2<String, Long>> testHarness =
        new OneInputStreamOperatorTestHarness<>(new StreamMap<>(function));
    
    testHarness.open();
    
    testHarness.processElement("hello", 1000L);
    testHarness.processElement("world", 2000L);
    
    Queue<Object> output = testHarness.getOutput();
    assertEquals(2, output.size());
    
    testHarness.close();
}
```

### Integration Testing
```java
@Test
public void testCompleteJob() throws Exception {
    MiniClusterWithClientResource flinkCluster = 
        new MiniClusterWithClientResource(
            new MiniClusterResourceConfiguration.Builder()
                .setNumberSlotsPerTaskManager(2)
                .setNumberTaskManagers(1)
                .build()
        );
    
    flinkCluster.before();
    
    try {
        StreamExecutionEnvironment env = 
            StreamExecutionEnvironment.getExecutionEnvironment();
        
        // Test pipeline
        DataStream<String> input = env.fromElements("a", "b", "c");
        input.map(String::toUpperCase).print();
        
        env.execute("Test Job");
        
    } finally {
        flinkCluster.after();
    }
}
```

## 9. Deployment Best Practices

### Kubernetes Deployment
```yaml
apiVersion: flink.apache.org/v1beta1
kind: FlinkDeployment
metadata:
  name: production-job
spec:
  image: flink:1.17.1-scala_2.12
  flinkVersion: v1_17
  flinkConfiguration:
    taskmanager.numberOfTaskSlots: "4"
    state.backend: rocksdb
    state.checkpoints.dir: s3://flink-checkpoints/
    high-availability: kubernetes
    restart-strategy: exponential-delay
    metrics.reporters: prometheus
  jobManager:
    resource:
      memory: "2048m"
      cpu: 1
    replicas: 2
  taskManager:
    resource:
      memory: "4096m"
      cpu: 2
    replicas: 6
  job:
    jarURI: s3://flink-jobs/job.jar
    parallelism: 24
    upgradeMode: savepoint
```

### CI/CD Pipeline
```yaml
# .github/workflows/flink-deploy.yml
name: Deploy Flink Job
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Build JAR
      run: mvn clean package
    
    - name: Upload to S3
      run: aws s3 cp target/job.jar s3://flink-jobs/
    
    - name: Create Savepoint
      run: |
        kubectl patch flinkdeployment production-job \
          --type='merge' -p='{"spec":{"job":{"savepointTriggerNonce":'$(date +%s)'}}}'
    
    - name: Update Deployment
      run: |
        kubectl patch flinkdeployment production-job \
          --type='merge' -p='{"spec":{"job":{"jarURI":"s3://flink-jobs/job.jar"}}}'
```

## 10. Troubleshooting Guide

### Common Issues and Solutions

#### High Checkpoint Duration
```java
// Reduce checkpoint size
env.getCheckpointConfig().setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE);
env.getCheckpointConfig().setMinPauseBetweenCheckpoints(30000);

// Use incremental checkpoints
RocksDBStateBackend rocksDBBackend = new RocksDBStateBackend("s3://checkpoints/");
rocksDBBackend.setIncremental(true);
```

#### Backpressure Issues
```java
// Monitor backpressure
MetricGroup metricGroup = getRuntimeContext().getMetricGroup();
Gauge<Double> backpressureRatio = metricGroup.gauge("backpressure_ratio", 
    this::calculateBackpressureRatio);

// Optimize parallelism
stream.setParallelism(calculateOptimalParallelism());

// Use async I/O for external calls
AsyncDataStream.unorderedWait(stream, asyncFunction, timeout, timeUnit, capacity);
```

#### Memory Issues
```java
// Tune memory allocation
Configuration config = new Configuration();
config.setString("taskmanager.memory.process.size", "8g");
config.setString("taskmanager.memory.managed.fraction", "0.6");

// Enable object reuse
env.getConfig().enableObjectReuse();

// Use efficient serializers
env.getConfig().registerKryoType(MyClass.class);
```

### Monitoring Checklist
- [ ] Checkpoint duration and size
- [ ] Backpressure indicators
- [ ] Memory usage and GC metrics
- [ ] Throughput and latency
- [ ] Error rates and exceptions
- [ ] Resource utilization
- [ ] Network I/O metrics
- [ ] State size growth