# Apache Flink Advanced Interview Questions & Answers

## 📋 Table of Contents
1. [Stream Processing Architecture](#stream-processing-architecture)
2. [State Management](#state-management)
3. [Windowing & Time](#windowing--time)
4. [Fault Tolerance](#fault-tolerance)
5. [Performance Optimization](#performance-optimization)

---

## Stream Processing Architecture

### 1. How does Flink's streaming architecture differ from micro-batch systems?

**Answer:**
Flink uses true streaming with continuous processing, unlike micro-batch systems that process data in small batches.

**Architecture Comparison:**
```java
// Flink: True streaming - record-by-record processing
DataStream<Event> events = env.addSource(new KafkaSource<>());
events
    .keyBy(Event::getUserId)
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .aggregate(new EventAggregator())
    .addSink(new ElasticsearchSink<>());

// Micro-batch: Processes small batches every interval
// SparkStreaming example (for comparison)
JavaDStream<Event> events = jssc.receiverStream(new KafkaReceiver());
events
    .window(Durations.minutes(5), Durations.seconds(10))
    .foreachRDD(rdd -> rdd.foreach(record -> process(record)));
```

**Key Differences:**
| Aspect | Flink (True Streaming) | Micro-batch |
|--------|------------------------|-------------|
| **Latency** | Sub-millisecond | Seconds |
| **Processing Model** | Continuous | Batch intervals |
| **Memory Usage** | Constant | Spikes per batch |
| **Backpressure** | Natural | Batch boundaries |

### 2. Explain Flink's execution model and task scheduling.

**Answer:**
Flink uses a dataflow execution model with parallel task execution across distributed workers.

**Execution Graph:**
```java
// JobGraph → ExecutionGraph → Physical execution
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
env.setParallelism(4);

DataStream<String> source = env.addSource(new KafkaSource<>())
    .setParallelism(2);  // 2 source tasks

DataStream<ProcessedEvent> processed = source
    .map(new EventProcessor())
    .setParallelism(4);  // 4 map tasks

processed
    .keyBy(ProcessedEvent::getKey)
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))
    .aggregate(new EventAggregator())
    .setParallelism(2)   // 2 window tasks
    .addSink(new OutputSink())
    .setParallelism(1);  // 1 sink task
```

**Task Execution:**
```
TaskManager 1:
├── Source Task (1/2)
├── Map Task (1/4)
├── Map Task (2/4)
└── Window Task (1/2)

TaskManager 2:
├── Source Task (2/2)
├── Map Task (3/4)
├── Map Task (4/4)
├── Window Task (2/2)
└── Sink Task (1/1)
```

---

## State Management

### 3. How do you implement and manage keyed state in Flink?

**Answer:**
Flink provides multiple state primitives for managing keyed state with automatic partitioning and fault tolerance.

**State Types and Usage:**
```java
public class StatefulProcessor extends KeyedProcessFunction<String, Event, Alert> {
    
    // Value State: Single value per key
    private transient ValueState<Long> countState;
    
    // List State: List of values per key
    private transient ListState<Event> eventHistoryState;
    
    // Map State: Key-value pairs per key
    private transient MapState<String, Double> metricsState;
    
    // Reducing State: Aggregated value per key
    private transient ReducingState<Long> sumState;
    
    @Override
    public void open(Configuration parameters) {
        // Initialize value state
        ValueStateDescriptor<Long> countDescriptor = 
            new ValueStateDescriptor<>("count", Long.class, 0L);
        countState = getRuntimeContext().getState(countDescriptor);
        
        // Initialize list state
        ListStateDescriptor<Event> historyDescriptor = 
            new ListStateDescriptor<>("history", Event.class);
        eventHistoryState = getRuntimeContext().getListState(historyDescriptor);
        
        // Initialize map state
        MapStateDescriptor<String, Double> metricsDescriptor = 
            new MapStateDescriptor<>("metrics", String.class, Double.class);
        metricsState = getRuntimeContext().getMapState(metricsDescriptor);
        
        // Initialize reducing state
        ReducingStateDescriptor<Long> sumDescriptor = 
            new ReducingStateDescriptor<>("sum", Long::sum, Long.class);
        sumState = getRuntimeContext().getReducingState(sumDescriptor);
    }
    
    @Override
    public void processElement(Event event, Context context, Collector<Alert> out) 
            throws Exception {
        
        // Update count state
        Long currentCount = countState.value();
        countState.update(currentCount + 1);
        
        // Add to history (with size limit)
        eventHistoryState.add(event);
        List<Event> history = new ArrayList<>();
        eventHistoryState.get().forEach(history::add);
        if (history.size() > 100) {
            eventHistoryState.clear();
            history.subList(0, 50).forEach(e -> {
                try { eventHistoryState.add(e); } catch (Exception ex) {}
            });
        }
        
        // Update metrics
        metricsState.put("avg_value", event.getValue());
        metricsState.put("last_update", (double) System.currentTimeMillis());
        
        // Update sum
        sumState.add(event.getValue().longValue());
        
        // Generate alert based on state
        if (currentCount > 100 && sumState.get() > 10000) {
            out.collect(new Alert(context.getCurrentKey(), "High activity detected"));
        }
        
        // Set timer for cleanup
        context.timerService().registerEventTimeTimer(
            context.timestamp() + Duration.ofHours(1).toMillis()
        );
    }
    
    @Override
    public void onTimer(long timestamp, OnTimerContext ctx, Collector<Alert> out) 
            throws Exception {
        // Cleanup old state
        eventHistoryState.clear();
        metricsState.clear();
    }
}
```

### 4. How do you implement custom state backends and optimize state performance?

**Answer:**
Flink supports multiple state backends with different performance characteristics and configuration options.

**State Backend Configuration:**
```java
// RocksDB State Backend for large state
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

RocksDBStateBackend rocksDBStateBackend = new RocksDBStateBackend(
    "hdfs://namenode:port/flink/checkpoints", true);

// Performance tuning
rocksDBStateBackend.setDbStoragePath("/tmp/rocksdb");
rocksDBStateBackend.setPredefinedOptions(PredefinedOptions.SPINNING_DISK_OPTIMIZED);

// Custom RocksDB options
rocksDBStateBackend.setRocksDBOptions(new RocksDBOptionsFactory() {
    @Override
    public DBOptions createDBOptions(DBOptions currentOptions, 
                                   Collection<AutoCloseable> handlesToClose) {
        return currentOptions
            .setIncreaseParallelism(4)
            .setUseFsync(false)
            .setMaxBackgroundCompactions(4);
    }
    
    @Override
    public ColumnFamilyOptions createColumnOptions(ColumnFamilyOptions currentOptions,
                                                 Collection<AutoCloseable> handlesToClose) {
        return currentOptions
            .setTableFormatConfig(new BlockBasedTableConfig()
                .setBlockCacheSize(256 * 1024 * 1024)  // 256MB
                .setBlockSize(128 * 1024))              // 128KB
            .setCompactionStyle(CompactionStyle.LEVEL)
            .setLevelCompactionDynamicLevelBytes(true);
    }
});

env.setStateBackend(rocksDBStateBackend);
```

**Custom State Backend:**
```java
public class CustomStateBackend extends AbstractStateBackend {
    private final String checkpointPath;
    private final boolean asyncSnapshots;
    
    public CustomStateBackend(String checkpointPath, boolean asyncSnapshots) {
        this.checkpointPath = checkpointPath;
        this.asyncSnapshots = asyncSnapshots;
    }
    
    @Override
    public <K> AbstractKeyedStateBackend<K> createKeyedStateBackend(
            Environment env,
            JobID jobID,
            String operatorIdentifier,
            TypeSerializer<K> keySerializer,
            int numberOfKeyGroups,
            KeyGroupRange keyGroupRange,
            TaskKvStateRegistry kvStateRegistry,
            TtlTimeProvider ttlTimeProvider,
            MetricGroup metricGroup,
            Collection<KeyedStateHandle> stateHandles,
            CloseableRegistry cancelStreamRegistry) throws Exception {
        
        return new CustomKeyedStateBackend<>(
            kvStateRegistry,
            keySerializer,
            env.getUserClassLoader(),
            numberOfKeyGroups,
            keyGroupRange,
            asyncSnapshots,
            env.getExecutionConfig(),
            ttlTimeProvider,
            metricGroup,
            stateHandles,
            cancelStreamRegistry
        );
    }
    
    @Override
    public OperatorStateBackend createOperatorStateBackend(
            Environment env,
            String operatorIdentifier,
            Collection<OperatorStateHandle> stateHandles,
            CloseableRegistry cancelStreamRegistry) throws Exception {
        
        return new DefaultOperatorStateBackendBuilder(
            env.getUserClassLoader(),
            env.getExecutionConfig(),
            asyncSnapshots,
            stateHandles,
            cancelStreamRegistry
        ).build();
    }
}
```

---

## Windowing & Time

### 5. How do you handle complex windowing scenarios with custom triggers?

**Answer:**
Flink provides flexible windowing with custom triggers for complex event-time processing scenarios.

**Custom Trigger Implementation:**
```java
public class CustomEventTrigger extends Trigger<Event, TimeWindow> {
    private final long maxCount;
    private final long maxLateness;
    
    // State to track event count per window
    private final ReducingStateDescriptor<Long> countStateDescriptor =
        new ReducingStateDescriptor<>("count", Long::sum, Long.class);
    
    public CustomEventTrigger(long maxCount, long maxLateness) {
        this.maxCount = maxCount;
        this.maxLateness = maxLateness;
    }
    
    @Override
    public TriggerResult onElement(Event element, long timestamp, 
                                 TimeWindow window, TriggerContext ctx) throws Exception {
        
        // Register window end timer
        ctx.registerEventTimeTimer(window.getEnd());
        
        // Register cleanup timer for late events
        ctx.registerEventTimeTimer(window.getEnd() + maxLateness);
        
        // Update count state
        ReducingState<Long> countState = ctx.getPartitionedState(countStateDescriptor);
        countState.add(1L);
        
        // Trigger if count threshold reached
        if (countState.get() >= maxCount) {
            return TriggerResult.FIRE_AND_PURGE;
        }
        
        // Check for early firing conditions
        if (shouldFireEarly(element, window, ctx)) {
            return TriggerResult.FIRE;
        }
        
        return TriggerResult.CONTINUE;
    }
    
    @Override
    public TriggerResult onEventTime(long time, TimeWindow window, TriggerContext ctx) 
            throws Exception {
        
        if (time == window.getEnd()) {
            // Window end reached - fire
            return TriggerResult.FIRE_AND_PURGE;
        } else if (time == window.getEnd() + maxLateness) {
            // Cleanup time reached - purge
            return TriggerResult.PURGE;
        }
        
        return TriggerResult.CONTINUE;
    }
    
    @Override
    public TriggerResult onProcessingTime(long time, TimeWindow window, TriggerContext ctx) 
            throws Exception {
        return TriggerResult.CONTINUE;
    }
    
    @Override
    public void clear(TimeWindow window, TriggerContext ctx) throws Exception {
        ctx.getPartitionedState(countStateDescriptor).clear();
        ctx.deleteEventTimeTimer(window.getEnd());
        ctx.deleteEventTimeTimer(window.getEnd() + maxLateness);
    }
    
    private boolean shouldFireEarly(Event element, TimeWindow window, TriggerContext ctx) {
        // Custom logic for early firing
        return element.getPriority() > 0.8 || 
               (System.currentTimeMillis() - window.getStart()) > 30000;
    }
}

// Usage with custom window
DataStream<Event> events = env.addSource(new EventSource());

events
    .keyBy(Event::getUserId)
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .trigger(new CustomEventTrigger(1000, Time.minutes(1).toMilliseconds()))
    .aggregate(new EventAggregator())
    .addSink(new ResultSink());
```

### 6. How do you implement session windows with custom session gap logic?

**Answer:**
Session windows group events based on activity gaps, with custom logic for determining session boundaries.

**Custom Session Window Implementation:**
```java
public class CustomSessionWindows extends WindowAssigner<Object, TimeWindow> {
    private final long sessionTimeout;
    private final SessionGapExtractor<Object> gapExtractor;
    
    public CustomSessionWindows(long sessionTimeout, SessionGapExtractor<Object> gapExtractor) {
        this.sessionTimeout = sessionTimeout;
        this.gapExtractor = gapExtractor;
    }
    
    @Override
    public Collection<TimeWindow> assignWindows(Object element, long timestamp, 
                                              WindowAssignerContext context) {
        // Custom gap calculation based on element
        long gap = gapExtractor.extractGap(element);
        
        return Collections.singletonList(new TimeWindow(timestamp, timestamp + gap));
    }
    
    @Override
    public Trigger<Object, TimeWindow> getDefaultTrigger(StreamExecutionEnvironment env) {
        return EventTimeTrigger.create();
    }
    
    @Override
    public TypeSerializer<TimeWindow> getWindowSerializer(ExecutionConfig executionConfig) {
        return new TimeWindow.Serializer();
    }
    
    @Override
    public boolean isEventTime() {
        return true;
    }
    
    // Custom session gap extractor
    public interface SessionGapExtractor<T> extends Serializable {
        long extractGap(T element);
    }
}

// Advanced session window with merging
public class AdaptiveSessionWindows extends MergingWindowAssigner<Event, TimeWindow> {
    private final long minSessionGap;
    private final long maxSessionGap;
    
    @Override
    public Collection<TimeWindow> assignWindows(Event element, long timestamp, 
                                              WindowAssignerContext context) {
        // Adaptive gap based on event characteristics
        long gap = calculateAdaptiveGap(element);
        return Collections.singletonList(new TimeWindow(timestamp, timestamp + gap));
    }
    
    @Override
    public void mergeWindows(Collection<TimeWindow> windows, 
                           MergeCallback<TimeWindow> callback) {
        
        List<TimeWindow> sortedWindows = new ArrayList<>(windows);
        sortedWindows.sort(Comparator.comparing(TimeWindow::getStart));
        
        List<TimeWindow> merged = new ArrayList<>();
        TimeWindow currentWindow = null;
        
        for (TimeWindow window : sortedWindows) {
            if (currentWindow == null) {
                currentWindow = window;
            } else if (shouldMerge(currentWindow, window)) {
                // Merge windows
                currentWindow = new TimeWindow(
                    currentWindow.getStart(),
                    Math.max(currentWindow.getEnd(), window.getEnd())
                );
            } else {
                merged.add(currentWindow);
                currentWindow = window;
            }
        }
        
        if (currentWindow != null) {
            merged.add(currentWindow);
        }
        
        // Notify about merges
        if (merged.size() < windows.size()) {
            callback.merge(windows, merged.get(0));
        }
    }
    
    private long calculateAdaptiveGap(Event element) {
        // Adaptive gap based on user activity level
        double activityScore = element.getActivityScore();
        
        if (activityScore > 0.8) {
            return minSessionGap;  // High activity - short gap
        } else if (activityScore < 0.2) {
            return maxSessionGap;  // Low activity - long gap
        } else {
            // Linear interpolation
            return (long) (minSessionGap + (maxSessionGap - minSessionGap) * (1 - activityScore));
        }
    }
    
    private boolean shouldMerge(TimeWindow window1, TimeWindow window2) {
        // Custom merge logic
        return window1.getEnd() >= window2.getStart() - minSessionGap;
    }
}
```

---

## Fault Tolerance

### 7. How do you implement exactly-once processing with custom sources and sinks?

**Answer:**
Exactly-once processing requires careful coordination between sources, Flink's checkpointing, and transactional sinks.

**Exactly-Once Source:**
```java
public class ExactlyOnceKafkaSource extends RichParallelSourceFunction<Event> 
        implements CheckpointedFunction {
    
    private volatile boolean running = true;
    private transient KafkaConsumer<String, String> consumer;
    private transient ListState<Tuple2<Integer, Long>> offsetState;
    private Map<Integer, Long> currentOffsets = new HashMap<>();
    
    @Override
    public void initializeState(FunctionInitializationContext context) throws Exception {
        // Initialize offset state
        offsetState = context.getOperatorStateStore().getListState(
            new ListStateDescriptor<>("kafka-offsets", 
                TypeInformation.of(new TypeHint<Tuple2<Integer, Long>>() {}))
        );
        
        // Restore offsets from state
        if (context.isRestored()) {
            for (Tuple2<Integer, Long> offset : offsetState.get()) {
                currentOffsets.put(offset.f0, offset.f1);
            }
        }
    }
    
    @Override
    public void snapshotState(FunctionSnapshotContext context) throws Exception {
        // Save current offsets to state
        offsetState.clear();
        for (Map.Entry<Integer, Long> entry : currentOffsets.entrySet()) {
            offsetState.add(Tuple2.of(entry.getKey(), entry.getValue()));
        }
    }
    
    @Override
    public void run(SourceContext<Event> ctx) throws Exception {
        // Initialize Kafka consumer with saved offsets
        initializeConsumer();
        
        while (running) {
            ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
            
            for (ConsumerRecord<String, String> record : records) {
                synchronized (ctx.getCheckpointLock()) {
                    // Emit event within checkpoint lock
                    Event event = parseEvent(record.value());
                    ctx.collect(event);
                    
                    // Update offset tracking
                    currentOffsets.put(record.partition(), record.offset() + 1);
                }
            }
        }
    }
    
    private void initializeConsumer() {
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("group.id", "flink-exactly-once");
        props.put("enable.auto.commit", "false");  // Manual offset management
        
        consumer = new KafkaConsumer<>(props);
        consumer.subscribe(Arrays.asList("input-topic"));
        
        // Seek to saved offsets
        for (Map.Entry<Integer, Long> entry : currentOffsets.entrySet()) {
            TopicPartition partition = new TopicPartition("input-topic", entry.getKey());
            consumer.seek(partition, entry.getValue());
        }
    }
}
```

**Two-Phase Commit Sink:**
```java
public class ExactlyOnceDatabaseSink extends TwoPhaseCommitSinkFunction<Event, 
        DatabaseTransaction, Void> {
    
    private final String jdbcUrl;
    private final String username;
    private final String password;
    
    @Override
    protected DatabaseTransaction beginTransaction() throws Exception {
        // Start database transaction
        Connection connection = DriverManager.getConnection(jdbcUrl, username, password);
        connection.setAutoCommit(false);
        
        return new DatabaseTransaction(connection, UUID.randomUUID().toString());
    }
    
    @Override
    protected void invoke(DatabaseTransaction transaction, Event event, Context context) 
            throws Exception {
        // Write to database within transaction
        PreparedStatement stmt = transaction.getConnection().prepareStatement(
            "INSERT INTO events (id, user_id, event_type, timestamp, data) VALUES (?, ?, ?, ?, ?)"
        );
        
        stmt.setString(1, event.getId());
        stmt.setString(2, event.getUserId());
        stmt.setString(3, event.getEventType());
        stmt.setTimestamp(4, new Timestamp(event.getTimestamp()));
        stmt.setString(5, event.getData());
        
        stmt.executeUpdate();
        stmt.close();
    }
    
    @Override
    protected DatabaseTransaction recoverAndCommit(DatabaseTransaction transaction) 
            throws Exception {
        // Recover and commit transaction
        if (transaction != null && transaction.getConnection() != null) {
            transaction.getConnection().commit();
            transaction.getConnection().close();
        }
        return null;
    }
    
    @Override
    protected void recoverAndAbort(DatabaseTransaction transaction) throws Exception {
        // Recover and abort transaction
        if (transaction != null && transaction.getConnection() != null) {
            transaction.getConnection().rollback();
            transaction.getConnection().close();
        }
    }
    
    @Override
    protected DatabaseTransaction recoverAndCommit(DatabaseTransaction transaction) 
            throws Exception {
        return recoverAndCommit(transaction);
    }
}

// Transaction wrapper
public class DatabaseTransaction {
    private final Connection connection;
    private final String transactionId;
    
    public DatabaseTransaction(Connection connection, String transactionId) {
        this.connection = connection;
        this.transactionId = transactionId;
    }
    
    // Getters
    public Connection getConnection() { return connection; }
    public String getTransactionId() { return transactionId; }
}
```

---

## Performance Optimization

### 8. How do you optimize Flink applications for high throughput and low latency?

**Answer:**
Performance optimization involves tuning multiple aspects including parallelism, memory management, and network configuration.

**Parallelism and Resource Optimization:**
```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// Global parallelism
env.setParallelism(16);

// Buffer timeout for low latency
env.setBufferTimeout(1);  // 1ms

// Restart strategy
env.setRestartStrategy(RestartStrategies.fixedDelayRestart(
    3,  // number of restart attempts
    Time.of(10, TimeUnit.SECONDS)  // delay
));

DataStream<Event> events = env
    .addSource(new OptimizedKafkaSource())
    .setParallelism(8)  // Source parallelism
    .rebalance()  // Redistribute for load balancing
    .map(new FastEventProcessor())
    .setParallelism(16)  // Processing parallelism
    .keyBy(Event::getPartitionKey)
    .window(TumblingEventTimeWindows.of(Time.seconds(10)))
    .aggregate(new OptimizedAggregator())
    .setParallelism(8)  // Window parallelism
    .addSink(new OptimizedSink())
    .setParallelism(4);  // Sink parallelism
```

**Memory and Serialization Optimization:**
```java
// Custom serializer for better performance
public class EventSerializer extends TypeSerializer<Event> {
    
    @Override
    public void serialize(Event record, DataOutputView target) throws IOException {
        // Optimized serialization
        target.writeUTF(record.getId());
        target.writeUTF(record.getUserId());
        target.writeLong(record.getTimestamp());
        target.writeInt(record.getData().length);
        target.write(record.getData());
    }
    
    @Override
    public Event deserialize(DataInputView source) throws IOException {
        // Optimized deserialization
        String id = source.readUTF();
        String userId = source.readUTF();
        long timestamp = source.readLong();
        int dataLength = source.readInt();
        byte[] data = new byte[dataLength];
        source.readFully(data);
        
        return new Event(id, userId, timestamp, data);
    }
    
    // Other required methods...
}

// Register custom serializer
env.getConfig().registerTypeWithKryoSerializer(Event.class, EventSerializer.class);

// Memory configuration
Configuration config = new Configuration();
config.setString("taskmanager.memory.process.size", "4g");
config.setString("taskmanager.memory.flink.size", "3g");
config.setString("taskmanager.memory.managed.fraction", "0.4");
config.setString("taskmanager.memory.network.fraction", "0.1");
```

**Async I/O for External Lookups:**
```java
public class AsyncDatabaseLookup extends RichAsyncFunction<Event, EnrichedEvent> {
    private transient DatabaseClient client;
    private transient ExecutorService executor;
    
    @Override
    public void open(Configuration parameters) throws Exception {
        // Initialize async database client
        client = new DatabaseClient("jdbc:postgresql://localhost:5432/lookup");
        executor = Executors.newFixedThreadPool(20);
    }
    
    @Override
    public void asyncInvoke(Event input, ResultFuture<EnrichedEvent> resultFuture) 
            throws Exception {
        
        CompletableFuture
            .supplyAsync(() -> {
                try {
                    // Async database lookup
                    UserProfile profile = client.getUserProfile(input.getUserId());
                    return new EnrichedEvent(input, profile);
                } catch (Exception e) {
                    throw new RuntimeException(e);
                }
            }, executor)
            .whenComplete((result, throwable) -> {
                if (throwable != null) {
                    resultFuture.completeExceptionally(throwable);
                } else {
                    resultFuture.complete(Collections.singleton(result));
                }
            });
    }
    
    @Override
    public void timeout(Event input, ResultFuture<EnrichedEvent> resultFuture) 
            throws Exception {
        // Handle timeout - return event without enrichment
        resultFuture.complete(Collections.singleton(new EnrichedEvent(input, null)));
    }
}

// Usage with async I/O
AsyncDataStream.unorderedWait(
    events,
    new AsyncDatabaseLookup(),
    5000,  // 5 second timeout
    TimeUnit.MILLISECONDS,
    100    // Max async requests
);
```

### 9. How do you implement custom metrics and monitoring for Flink applications?

**Answer:**
Custom metrics provide insights into application performance and business logic execution.

**Custom Metrics Implementation:**
```java
public class MetricsCollectingProcessor extends RichMapFunction<Event, ProcessedEvent> {
    
    private transient Counter eventCounter;
    private transient Histogram processingTimeHistogram;
    private transient Gauge<Long> backlogGauge;
    private transient Meter errorRate;
    
    private volatile long currentBacklog = 0;
    
    @Override
    public void open(Configuration parameters) throws Exception {
        // Register metrics
        MetricGroup metricGroup = getRuntimeContext().getMetricGroup()
            .addGroup("custom")
            .addGroup("processor");
        
        // Counter for processed events
        eventCounter = metricGroup.counter("events_processed");
        
        // Histogram for processing time distribution
        processingTimeHistogram = metricGroup.histogram("processing_time", 
            new DescriptiveStatisticsHistogram(1000));
        
        // Gauge for current backlog
        backlogGauge = metricGroup.gauge("current_backlog", () -> currentBacklog);
        
        // Meter for error rate
        errorRate = metricGroup.meter("error_rate", new MeterView(60));
    }
    
    @Override
    public ProcessedEvent map(Event event) throws Exception {
        long startTime = System.nanoTime();
        
        try {
            // Process event
            ProcessedEvent result = processEvent(event);
            
            // Update metrics
            eventCounter.inc();
            long processingTime = System.nanoTime() - startTime;
            processingTimeHistogram.update(processingTime / 1_000_000); // Convert to ms
            
            // Update backlog (example logic)
            currentBacklog = calculateBacklog();
            
            return result;
            
        } catch (Exception e) {
            errorRate.markEvent();
            throw e;
        }
    }
    
    private ProcessedEvent processEvent(Event event) {
        // Business logic here
        return new ProcessedEvent(event.getId(), event.getData().toUpperCase());
    }
    
    private long calculateBacklog() {
        // Calculate current processing backlog
        return System.currentTimeMillis() - lastProcessedTimestamp;
    }
}

// Custom metric reporter
public class CustomMetricReporter implements MetricReporter {
    private ScheduledExecutorService executor;
    private MetricRegistry registry;
    
    @Override
    public void open(MetricConfig config) {
        executor = Executors.newSingleThreadScheduledExecutor();
        registry = new MetricRegistry();
        
        // Schedule metric reporting
        executor.scheduleAtFixedRate(this::reportMetrics, 0, 30, TimeUnit.SECONDS);
    }
    
    @Override
    public void notifyOfAddedMetric(Metric metric, String metricName, MetricGroup group) {
        String fullName = group.getMetricIdentifier(metricName);
        registry.register(fullName, metric);
    }
    
    @Override
    public void notifyOfRemovedMetric(Metric metric, String metricName, MetricGroup group) {
        String fullName = group.getMetricIdentifier(metricName);
        registry.remove(fullName);
    }
    
    private void reportMetrics() {
        // Send metrics to external system (Prometheus, InfluxDB, etc.)
        for (Map.Entry<String, Metric> entry : registry.getMetrics().entrySet()) {
            String name = entry.getKey();
            Metric metric = entry.getValue();
            
            if (metric instanceof Counter) {
                sendCounterMetric(name, ((Counter) metric).getCount());
            } else if (metric instanceof Gauge) {
                sendGaugeMetric(name, ((Gauge<?>) metric).getValue());
            } else if (metric instanceof Histogram) {
                HistogramStatistics stats = ((Histogram) metric).getStatistics();
                sendHistogramMetric(name, stats);
            }
        }
    }
    
    private void sendCounterMetric(String name, long value) {
        // Implementation to send to monitoring system
    }
    
    private void sendGaugeMetric(String name, Object value) {
        // Implementation to send to monitoring system
    }
    
    private void sendHistogramMetric(String name, HistogramStatistics stats) {
        // Implementation to send to monitoring system
    }
}
```

---

## Summary

Advanced Apache Flink capabilities include:

1. **True Streaming**: Continuous processing with sub-millisecond latency
2. **Sophisticated State Management**: Multiple state types with automatic partitioning
3. **Flexible Windowing**: Custom triggers and session windows
4. **Exactly-Once Processing**: End-to-end consistency guarantees
5. **Performance Optimization**: Async I/O, custom serialization, and comprehensive monitoring