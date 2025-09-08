# Apache Flink Comprehensive Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Core Architecture & Concepts (1-25)](#core-architecture--concepts-1-25)
2. [Stream Processing & Windows (26-50)](#stream-processing--windows-26-50)
3. [State Management & Checkpointing (51-75)](#state-management--checkpointing-51-75)
4. [Performance & Optimization (76-100)](#performance--optimization-76-100)
5. [Production & Operations (101-125)](#production--operations-101-125)
6. [Advanced Scenarios (126-150)](#advanced-scenarios-126-150)

---

## Core Architecture & Concepts (1-25)

### 1. What is Apache Flink and how does it differ from Apache Spark Streaming?
**Answer:**
Apache Flink is a distributed stream processing framework for stateful computations over unbounded and bounded data streams.

**Key Differences from Spark Streaming:**
- **True Streaming**: Flink processes events one-by-one, Spark uses micro-batches
- **Low Latency**: Sub-second latency vs seconds in Spark
- **Event Time Processing**: Native support for event time and watermarks
- **Exactly-Once Guarantees**: Built-in exactly-once processing semantics
- **Backpressure**: Automatic backpressure handling

```java
// Flink streaming example
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

DataStream<String> stream = env.socketTextStream("localhost", 9999);

DataStream<Tuple2<String, Integer>> counts = stream
    .flatMap(new LineSplitter())
    .keyBy(value -> value.f0)
    .window(TumblingProcessingTimeWindows.of(Time.seconds(5)))
    .sum(1);

counts.print();
env.execute("Word Count");
```

### 2. Explain Flink's runtime architecture and components
**Answer:**
**Flink Runtime Components:**
- **JobManager**: Coordinates distributed execution, scheduling, checkpointing
- **TaskManager**: Execute tasks, manage memory, handle network communication
- **Client**: Submits jobs to JobManager
- **Resource Manager**: Manages TaskManager slots and resources

**Execution Model:**
```java
// Job submission flow
public class FlinkJobSubmission {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        
        // Configure parallelism
        env.setParallelism(4);
        
        // Configure checkpointing
        env.enableCheckpointing(5000);
        
        // Build job graph
        DataStream<Event> events = env.addSource(new EventSource());
        events.keyBy(Event::getUserId)
              .process(new EventProcessor())
              .addSink(new EventSink());
        
        // Submit job
        env.execute("Event Processing Job");
    }
}
```

### 3. What are DataStreams and how do you create them?
**Answer:**
DataStream represents a stream of data elements in Flink.

**Creating DataStreams:**
```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// From collection
DataStream<Integer> numbers = env.fromCollection(Arrays.asList(1, 2, 3, 4, 5));

// From Kafka
Properties props = new Properties();
props.setProperty("bootstrap.servers", "localhost:9092");
props.setProperty("group.id", "flink-consumer");

DataStream<String> kafkaStream = env.addSource(
    new FlinkKafkaConsumer<>("events", new SimpleStringSchema(), props));

// From socket
DataStream<String> socketStream = env.socketTextStream("localhost", 9999);

// From file
DataStream<String> fileStream = env.readTextFile("hdfs://path/to/file");
```

### 4. Explain event time vs processing time in Flink
**Answer:**
**Event Time vs Processing Time:**
- **Event Time**: When event actually occurred (embedded in data)
- **Processing Time**: When event is processed by Flink
- **Ingestion Time**: When event enters Flink system

```java
// Configure event time
env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime);

// Assign timestamps and watermarks
DataStream<Event> eventsWithTimestamps = events
    .assignTimestampsAndWatermarks(
        WatermarkStrategy.<Event>forBoundedOutOfOrderness(Duration.ofSeconds(10))
            .withTimestampAssigner((event, timestamp) -> event.getTimestamp())
    );

// Window based on event time
eventsWithTimestamps
    .keyBy(Event::getUserId)
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .aggregate(new EventAggregator());
```

### 5. What are watermarks and how do they handle late data?
**Answer:**
Watermarks indicate progress in event time and handle out-of-order data.

**Watermark Strategies:**
```java
// Bounded out-of-orderness watermark
WatermarkStrategy<Event> watermarkStrategy = WatermarkStrategy
    .<Event>forBoundedOutOfOrderness(Duration.ofSeconds(10))
    .withTimestampAssigner((event, timestamp) -> event.getTimestamp());

// Custom watermark generator
public class CustomWatermarkGenerator implements WatermarkGenerator<Event> {
    private long maxTimestamp = Long.MIN_VALUE;
    private final long outOfOrdernessMillis = 10000; // 10 seconds
    
    @Override
    public void onEvent(Event event, long eventTimestamp, WatermarkOutput output) {
        maxTimestamp = Math.max(maxTimestamp, eventTimestamp);
    }
    
    @Override
    public void onPeriodicEmit(WatermarkOutput output) {
        output.emitWatermark(new Watermark(maxTimestamp - outOfOrdernessMillis));
    }
}

// Handle late data with side outputs
OutputTag<Event> lateDataTag = new OutputTag<Event>("late-data"){};

SingleOutputStreamOperator<Result> result = events
    .keyBy(Event::getUserId)
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .allowedLateness(Time.minutes(1))
    .sideOutputLateData(lateDataTag)
    .aggregate(new EventAggregator());

// Process late data separately
DataStream<Event> lateData = result.getSideOutput(lateDataTag);
```

---

## Stream Processing & Windows (26-50)

### 26. Explain different types of windows in Flink
**Answer:**
**Window Types:**

```java
// 1. Tumbling Windows (non-overlapping)
stream.keyBy(Event::getUserId)
      .window(TumblingEventTimeWindows.of(Time.minutes(5)))
      .aggregate(new CountAggregator());

// 2. Sliding Windows (overlapping)
stream.keyBy(Event::getUserId)
      .window(SlidingEventTimeWindows.of(Time.minutes(10), Time.minutes(2)))
      .aggregate(new SumAggregator());

// 3. Session Windows (gap-based)
stream.keyBy(Event::getUserId)
      .window(EventTimeSessionWindows.withGap(Time.minutes(30)))
      .aggregate(new SessionAggregator());

// 4. Global Windows (custom triggers)
stream.keyBy(Event::getUserId)
      .window(GlobalWindows.create())
      .trigger(CountTrigger.of(100))
      .aggregate(new BatchAggregator());

// 5. Custom Windows
public class CustomWindow extends Window {
    private final long start;
    private final long end;
    
    public CustomWindow(long start, long end) {
        this.start = start;
        this.end = end;
    }
    
    @Override
    public long maxTimestamp() {
        return end - 1;
    }
}
```

### 27. How do you implement custom window functions?
**Answer:**
**Custom Window Functions:**

```java
// ProcessWindowFunction for full window access
public class CustomWindowFunction 
    extends ProcessWindowFunction<Event, Result, String, TimeWindow> {
    
    @Override
    public void process(String key, Context context, 
                       Iterable<Event> elements, Collector<Result> out) {
        
        TimeWindow window = context.window();
        long count = 0;
        double sum = 0;
        
        for (Event event : elements) {
            count++;
            sum += event.getValue();
        }
        
        Result result = new Result(
            key, 
            window.getStart(), 
            window.getEnd(), 
            count, 
            sum / count
        );
        
        out.collect(result);
    }
}

// AggregateFunction for incremental aggregation
public class AverageAggregator implements AggregateFunction<Event, Tuple2<Double, Long>, Double> {
    
    @Override
    public Tuple2<Double, Long> createAccumulator() {
        return new Tuple2<>(0.0, 0L);
    }
    
    @Override
    public Tuple2<Double, Long> add(Event event, Tuple2<Double, Long> accumulator) {
        return new Tuple2<>(
            accumulator.f0 + event.getValue(),
            accumulator.f1 + 1L
        );
    }
    
    @Override
    public Double getResult(Tuple2<Double, Long> accumulator) {
        return accumulator.f0 / accumulator.f1;
    }
    
    @Override
    public Tuple2<Double, Long> merge(Tuple2<Double, Long> a, Tuple2<Double, Long> b) {
        return new Tuple2<>(a.f0 + b.f0, a.f1 + b.f1);
    }
}
```

### 28. How do you handle complex event processing (CEP) in Flink?
**Answer:**
**Complex Event Processing with FlinkCEP:**

```java
import org.apache.flink.cep.CEP;
import org.apache.flink.cep.PatternStream;
import org.apache.flink.cep.pattern.Pattern;
import org.apache.flink.cep.pattern.conditions.SimpleCondition;

// Define pattern
Pattern<Event, ?> pattern = Pattern.<Event>begin("start")
    .where(new SimpleCondition<Event>() {
        @Override
        public boolean filter(Event event) {
            return event.getType().equals("LOGIN");
        }
    })
    .next("middle")
    .where(new SimpleCondition<Event>() {
        @Override
        public boolean filter(Event event) {
            return event.getType().equals("PURCHASE");
        }
    })
    .within(Time.minutes(10));

// Apply pattern to stream
PatternStream<Event> patternStream = CEP.pattern(
    events.keyBy(Event::getUserId), 
    pattern
);

// Process matches
DataStream<Alert> alerts = patternStream.process(
    new PatternProcessFunction<Event, Alert>() {
        @Override
        public void processMatch(Map<String, List<Event>> match, 
                               Context ctx, Collector<Alert> out) {
            Event login = match.get("start").get(0);
            Event purchase = match.get("middle").get(0);
            
            out.collect(new Alert(
                login.getUserId(),
                "Suspicious activity detected",
                ctx.timestamp()
            ));
        }
    }
);
```

---

## State Management & Checkpointing (51-75)

### 51. Explain Flink's state management and different types of state
**Answer:**
**State Types in Flink:**

```java
// 1. Keyed State (scoped to key)
public class StatefulProcessor extends KeyedProcessFunction<String, Event, Result> {
    
    // Value State
    private ValueState<Long> countState;
    
    // List State
    private ListState<Event> eventHistory;
    
    // Map State
    private MapState<String, Long> categoryCount;
    
    @Override
    public void open(Configuration parameters) {
        // Initialize state descriptors
        ValueStateDescriptor<Long> countDescriptor = 
            new ValueStateDescriptor<>("count", Long.class);
        countState = getRuntimeContext().getState(countDescriptor);
        
        ListStateDescriptor<Event> historyDescriptor = 
            new ListStateDescriptor<>("history", Event.class);
        eventHistory = getRuntimeContext().getListState(historyDescriptor);
        
        MapStateDescriptor<String, Long> mapDescriptor = 
            new MapStateDescriptor<>("categoryCount", String.class, Long.class);
        categoryCount = getRuntimeContext().getMapState(mapDescriptor);
    }
    
    @Override
    public void processElement(Event event, Context ctx, Collector<Result> out) 
            throws Exception {
        
        // Update value state
        Long currentCount = countState.value();
        if (currentCount == null) currentCount = 0L;
        countState.update(currentCount + 1);
        
        // Update list state
        eventHistory.add(event);
        
        // Update map state
        String category = event.getCategory();
        Long categoryTotal = categoryCount.get(category);
        if (categoryTotal == null) categoryTotal = 0L;
        categoryCount.put(category, categoryTotal + 1);
        
        out.collect(new Result(ctx.getCurrentKey(), currentCount + 1));
    }
}

// 2. Operator State (scoped to operator)
public class StatefulSource implements SourceFunction<Event>, CheckpointedFunction {
    
    private ListState<Long> offsetState;
    private long currentOffset = 0;
    
    @Override
    public void snapshotState(FunctionSnapshotContext context) throws Exception {
        offsetState.clear();
        offsetState.add(currentOffset);
    }
    
    @Override
    public void initializeState(FunctionInitializationContext context) throws Exception {
        ListStateDescriptor<Long> descriptor = 
            new ListStateDescriptor<>("offset", Long.class);
        offsetState = context.getOperatorStateStore().getListState(descriptor);
        
        if (context.isRestored()) {
            for (Long offset : offsetState.get()) {
                currentOffset = offset;
            }
        }
    }
}
```

### 52. How do you configure and optimize checkpointing?
**Answer:**
**Checkpointing Configuration:**

```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// Enable checkpointing
env.enableCheckpointing(5000); // Checkpoint every 5 seconds

// Checkpoint configuration
CheckpointConfig checkpointConfig = env.getCheckpointConfig();

// Checkpoint mode
checkpointConfig.setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE);

// Minimum pause between checkpoints
checkpointConfig.setMinPauseBetweenCheckpoints(1000);

// Checkpoint timeout
checkpointConfig.setCheckpointTimeout(60000);

// Maximum concurrent checkpoints
checkpointConfig.setMaxConcurrentCheckpoints(1);

// Cleanup policy
checkpointConfig.enableExternalizedCheckpoints(
    CheckpointConfig.ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION);

// State backend configuration
env.setStateBackend(new RocksDBStateBackend("hdfs://checkpoints"));

// Advanced RocksDB tuning
RocksDBStateBackend rocksDBBackend = new RocksDBStateBackend("hdfs://checkpoints");
rocksDBBackend.setPredefinedOptions(PredefinedOptions.SPINNING_DISK_OPTIMIZED);
rocksDBBackend.setDbStoragePath("/tmp/rocksdb");
env.setStateBackend(rocksDBBackend);
```

### 53. How do you implement savepoints and state migration?
**Answer:**
**Savepoints and State Migration:**

```bash
# Create savepoint
flink savepoint <jobId> [targetDirectory]

# Stop job with savepoint
flink stop --savepointPath <savepointPath> <jobId>

# Restore from savepoint
flink run -s <savepointPath> <jarFile>

# List savepoints
flink list -s
```

**State Schema Evolution:**
```java
// Version 1 of state
public class UserStateV1 {
    public String userId;
    public long count;
}

// Version 2 with additional field
public class UserStateV2 {
    public String userId;
    public long count;
    public double average; // New field
    
    // Migration logic
    public static UserStateV2 fromV1(UserStateV1 v1) {
        UserStateV2 v2 = new UserStateV2();
        v2.userId = v1.userId;
        v2.count = v1.count;
        v2.average = 0.0; // Default value
        return v2;
    }
}

// Custom serializer for state evolution
public class UserStateSerializer extends TypeSerializerSingleton<UserState> {
    
    @Override
    public TypeSerializerSnapshot<UserState> snapshotConfiguration() {
        return new UserStateSerializerSnapshot();
    }
    
    public static class UserStateSerializerSnapshot 
            implements TypeSerializerSnapshot<UserState> {
        
        @Override
        public TypeSerializer<UserState> restoreSerializer() {
            return new UserStateSerializer();
        }
        
        @Override
        public TypeSerializerSchemaCompatibility<UserState> resolveSchemaCompatibility(
                TypeSerializer<UserState> newSerializer) {
            // Handle schema compatibility
            return TypeSerializerSchemaCompatibility.compatibleAsIs();
        }
    }
}
```

---

## Performance & Optimization (76-100)

### 76. How do you optimize Flink job performance?
**Answer:**
**Performance Optimization Strategies:**

```java
// 1. Parallelism tuning
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
env.setParallelism(16); // Set global parallelism

// Per-operator parallelism
stream.map(new MyMapFunction()).setParallelism(8);

// 2. Memory configuration
Configuration config = new Configuration();
config.setString("taskmanager.memory.process.size", "4g");
config.setString("taskmanager.memory.flink.size", "3g");
config.setString("taskmanager.memory.managed.fraction", "0.4");

// 3. Network buffer tuning
config.setString("taskmanager.network.memory.fraction", "0.1");
config.setString("taskmanager.network.memory.min", "64mb");
config.setString("taskmanager.network.memory.max", "1gb");

// 4. Operator chaining optimization
stream.map(new MapFunction1())
      .map(new MapFunction2()).disableChaining() // Disable chaining
      .keyBy(Event::getKey)
      .process(new ProcessFunction()).startNewChain(); // Start new chain

// 5. Async I/O for external lookups
AsyncFunction<Event, EnrichedEvent> asyncFunction = 
    new AsyncFunction<Event, EnrichedEvent>() {
        
        @Override
        public void asyncInvoke(Event input, ResultFuture<EnrichedEvent> resultFuture) {
            CompletableFuture<String> future = externalService.lookup(input.getId());
            
            future.whenComplete((result, throwable) -> {
                if (throwable == null) {
                    resultFuture.complete(Collections.singleton(
                        new EnrichedEvent(input, result)));
                } else {
                    resultFuture.completeExceptionally(throwable);
                }
            });
        }
    };

DataStream<EnrichedEvent> enrichedStream = AsyncDataStream.unorderedWait(
    stream, asyncFunction, 1000, TimeUnit.MILLISECONDS, 100);
```

### 77. How do you handle backpressure in Flink?
**Answer:**
**Backpressure Handling:**

```java
// 1. Monitor backpressure
// Use Flink Web UI or metrics to monitor backpressure

// 2. Increase parallelism
env.setParallelism(32); // Increase from 16 to 32

// 3. Optimize operators
public class OptimizedProcessFunction extends ProcessFunction<Event, Result> {
    
    @Override
    public void processElement(Event event, Context ctx, Collector<Result> out) {
        // Avoid expensive operations in hot path
        if (shouldProcess(event)) {
            Result result = processEvent(event);
            out.collect(result);
        }
    }
    
    private boolean shouldProcess(Event event) {
        // Quick filtering logic
        return event.getValue() > threshold;
    }
}

// 4. Buffer configuration
Configuration config = new Configuration();
config.setString("taskmanager.network.numberOfBuffers", "8192");
config.setString("taskmanager.network.bufferSizeInBytes", "32768");

// 5. Async processing for slow operations
public class AsyncEnrichmentFunction 
        implements AsyncFunction<Event, EnrichedEvent> {
    
    private final ExecutorService executor;
    
    @Override
    public void asyncInvoke(Event input, ResultFuture<EnrichedEvent> resultFuture) {
        CompletableFuture.supplyAsync(() -> {
            // Expensive operation
            return enrichEvent(input);
        }, executor).whenComplete((result, throwable) -> {
            if (throwable == null) {
                resultFuture.complete(Collections.singleton(result));
            } else {
                resultFuture.completeExceptionally(throwable);
            }
        });
    }
}
```

---

## Production & Operations (101-125)

### 101. How do you monitor Flink applications in production?
**Answer:**
**Comprehensive Monitoring Strategy:**

```java
// 1. Custom metrics
public class MetricsReportingFunction extends RichMapFunction<Event, Event> {
    
    private Counter eventCounter;
    private Histogram processingLatency;
    private Gauge<Long> currentTimestamp;
    
    @Override
    public void open(Configuration parameters) {
        this.eventCounter = getRuntimeContext()
            .getMetricGroup()
            .counter("events_processed");
            
        this.processingLatency = getRuntimeContext()
            .getMetricGroup()
            .histogram("processing_latency", new DescriptiveStatisticsHistogram(1000));
            
        this.currentTimestamp = getRuntimeContext()
            .getMetricGroup()
            .gauge("current_timestamp", () -> System.currentTimeMillis());
    }
    
    @Override
    public Event map(Event event) {
        long startTime = System.currentTimeMillis();
        
        // Process event
        Event processedEvent = processEvent(event);
        
        // Update metrics
        eventCounter.inc();
        processingLatency.update(System.currentTimeMillis() - startTime);
        
        return processedEvent;
    }
}

// 2. Health checks and alerting
public class HealthCheckSource implements SourceFunction<HealthCheck> {
    
    private volatile boolean running = true;
    
    @Override
    public void run(SourceContext<HealthCheck> ctx) throws Exception {
        while (running) {
            HealthCheck healthCheck = performHealthCheck();
            ctx.collect(healthCheck);
            Thread.sleep(30000); // Check every 30 seconds
        }
    }
    
    private HealthCheck performHealthCheck() {
        // Check external dependencies
        boolean kafkaHealthy = checkKafkaHealth();
        boolean dbHealthy = checkDatabaseHealth();
        
        return new HealthCheck(kafkaHealthy && dbHealthy, System.currentTimeMillis());
    }
}

// 3. Prometheus metrics integration
public class PrometheusMetricsReporter implements MetricReporter {
    
    private CollectorRegistry registry;
    private HTTPServer server;
    
    @Override
    public void open(MetricConfig config) {
        registry = new CollectorRegistry();
        try {
            server = new HTTPServer(9249);
        } catch (IOException e) {
            throw new RuntimeException("Failed to start Prometheus metrics server", e);
        }
    }
    
    @Override
    public void notifyOfAddedMetric(Metric metric, String metricName, MetricGroup group) {
        // Register metric with Prometheus
        if (metric instanceof Counter) {
            io.prometheus.client.Counter.build()
                .name(metricName)
                .help("Flink counter metric")
                .register(registry);
        }
    }
}
```

### 102. How do you implement disaster recovery for Flink jobs?
**Answer:**
**Disaster Recovery Strategy:**

```java
// 1. High availability configuration
Configuration config = new Configuration();
config.setString("high-availability", "zookeeper");
config.setString("high-availability.zookeeper.quorum", "zk1:2181,zk2:2181,zk3:2181");
config.setString("high-availability.storageDir", "hdfs://ha-storage");
config.setString("high-availability.cluster-id", "flink-cluster");

// 2. Automated job recovery
public class JobRecoveryManager {
    
    public void deployJobWithRecovery(String jarPath, String savepointPath) {
        try {
            // Deploy job with savepoint
            JobSubmissionResult result = client.submitJob(
                JobGraph.fromJobSpec(jarPath, savepointPath));
            
            // Monitor job health
            monitorJobHealth(result.getJobID());
            
        } catch (Exception e) {
            // Retry with exponential backoff
            scheduleRetry(jarPath, savepointPath, 1);
        }
    }
    
    private void scheduleRetry(String jarPath, String savepointPath, int attempt) {
        int delay = Math.min(300, 10 * (int) Math.pow(2, attempt)); // Max 5 min
        
        scheduler.schedule(() -> {
            if (attempt < MAX_RETRIES) {
                deployJobWithRecovery(jarPath, savepointPath);
            } else {
                alertOperations("Job recovery failed after " + MAX_RETRIES + " attempts");
            }
        }, delay, TimeUnit.SECONDS);
    }
}

// 3. Cross-region replication
public class CrossRegionReplication {
    
    public void setupReplication() {
        // Primary region job
        StreamExecutionEnvironment primaryEnv = 
            StreamExecutionEnvironment.getExecutionEnvironment();
        
        DataStream<Event> primaryStream = primaryEnv.addSource(new KafkaSource());
        
        // Replicate to secondary region
        primaryStream.addSink(new KafkaSink("secondary-region-topic"));
        
        // Secondary region standby job
        StreamExecutionEnvironment secondaryEnv = 
            StreamExecutionEnvironment.getExecutionEnvironment();
        
        DataStream<Event> secondaryStream = secondaryEnv.addSource(
            new KafkaSource("secondary-region-topic"));
        
        // Process in secondary region (standby mode)
        secondaryStream.addSink(new StandbySink());
    }
}
```

---

## Advanced Scenarios (126-150)

### 126. Design a real-time fraud detection system using Flink
**Answer:**
**Real-time Fraud Detection Architecture:**

```java
public class FraudDetectionJob {
    
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        
        // Configure for low latency
        env.setBufferTimeout(1);
        env.enableCheckpointing(30000);
        
        // Read transaction stream
        DataStream<Transaction> transactions = env.addSource(
            new FlinkKafkaConsumer<>("transactions", new TransactionSchema(), kafkaProps));
        
        // Assign timestamps and watermarks
        DataStream<Transaction> timestampedTransactions = transactions
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<Transaction>forBoundedOutOfOrderness(Duration.ofSeconds(5))
                    .withTimestampAssigner((transaction, timestamp) -> transaction.getTimestamp())
            );
        
        // Feature engineering
        DataStream<EnrichedTransaction> enrichedTransactions = timestampedTransactions
            .keyBy(Transaction::getUserId)
            .process(new TransactionEnrichmentFunction());
        
        // Real-time aggregations
        DataStream<UserMetrics> userMetrics = enrichedTransactions
            .keyBy(EnrichedTransaction::getUserId)
            .window(SlidingEventTimeWindows.of(Time.minutes(10), Time.minutes(1)))
            .aggregate(new UserMetricsAggregator());
        
        // Fraud detection rules
        DataStream<FraudAlert> fraudAlerts = enrichedTransactions
            .connect(userMetrics.broadcast(USER_METRICS_DESCRIPTOR))
            .process(new FraudDetectionFunction());
        
        // Output alerts
        fraudAlerts.addSink(new AlertSink());
        
        env.execute("Real-time Fraud Detection");
    }
}

// Transaction enrichment with state
public class TransactionEnrichmentFunction 
        extends KeyedProcessFunction<String, Transaction, EnrichedTransaction> {
    
    private ValueState<UserProfile> userProfileState;
    private ListState<Transaction> recentTransactions;
    
    @Override
    public void open(Configuration parameters) {
        userProfileState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("userProfile", UserProfile.class));
        
        recentTransactions = getRuntimeContext().getListState(
            new ListStateDescriptor<>("recentTransactions", Transaction.class));
    }
    
    @Override
    public void processElement(Transaction transaction, Context ctx, 
                             Collector<EnrichedTransaction> out) throws Exception {
        
        // Get user profile
        UserProfile profile = userProfileState.value();
        if (profile == null) {
            profile = loadUserProfile(transaction.getUserId());
            userProfileState.update(profile);
        }
        
        // Calculate velocity features
        List<Transaction> recent = new ArrayList<>();
        for (Transaction t : recentTransactions.get()) {
            if (transaction.getTimestamp() - t.getTimestamp() < 3600000) { // 1 hour
                recent.add(t);
            }
        }
        
        // Add current transaction
        recent.add(transaction);
        recentTransactions.update(recent);
        
        // Create enriched transaction
        EnrichedTransaction enriched = new EnrichedTransaction(
            transaction,
            profile,
            recent.size(), // Transaction count in last hour
            recent.stream().mapToDouble(Transaction::getAmount).sum() // Total amount
        );
        
        out.collect(enriched);
    }
}

// Fraud detection with ML model
public class FraudDetectionFunction extends KeyedBroadcastProcessFunction<
        String, EnrichedTransaction, UserMetrics, FraudAlert> {
    
    private final MapStateDescriptor<String, UserMetrics> USER_METRICS_DESCRIPTOR =
        new MapStateDescriptor<>("userMetrics", String.class, UserMetrics.class);
    
    @Override
    public void processElement(EnrichedTransaction transaction, ReadOnlyContext ctx, 
                             Collector<FraudAlert> out) throws Exception {
        
        // Get user metrics from broadcast state
        ReadOnlyBroadcastState<String, UserMetrics> broadcastState = 
            ctx.getBroadcastState(USER_METRICS_DESCRIPTOR);
        
        UserMetrics metrics = broadcastState.get(transaction.getUserId());
        
        // Apply fraud detection rules
        double fraudScore = calculateFraudScore(transaction, metrics);
        
        if (fraudScore > FRAUD_THRESHOLD) {
            FraudAlert alert = new FraudAlert(
                transaction.getTransactionId(),
                transaction.getUserId(),
                fraudScore,
                "High fraud score detected",
                System.currentTimeMillis()
            );
            
            out.collect(alert);
        }
    }
    
    @Override
    public void processBroadcastElement(UserMetrics metrics, Context ctx, 
                                      Collector<FraudAlert> out) throws Exception {
        // Update broadcast state with new metrics
        ctx.getBroadcastState(USER_METRICS_DESCRIPTOR).put(metrics.getUserId(), metrics);
    }
    
    private double calculateFraudScore(EnrichedTransaction transaction, UserMetrics metrics) {
        double score = 0.0;
        
        // Rule 1: Amount significantly higher than average
        if (transaction.getAmount() > metrics.getAverageAmount() * 5) {
            score += 0.3;
        }
        
        // Rule 2: Transaction from unusual location
        if (!transaction.getLocation().equals(metrics.getCommonLocation())) {
            score += 0.2;
        }
        
        // Rule 3: High velocity (many transactions in short time)
        if (transaction.getHourlyCount() > 10) {
            score += 0.4;
        }
        
        // Rule 4: Unusual time of day
        int hour = transaction.getHour();
        if (hour < 6 || hour > 22) {
            score += 0.1;
        }
        
        return Math.min(score, 1.0);
    }
}
```

This comprehensive Flink interview guide covers all essential aspects from basic concepts to advanced production scenarios, providing practical examples and real-world implementation patterns for data engineering roles.