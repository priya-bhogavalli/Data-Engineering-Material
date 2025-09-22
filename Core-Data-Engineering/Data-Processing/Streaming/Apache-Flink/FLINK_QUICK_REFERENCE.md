# Apache Flink Quick Reference

## Core Concepts

### Stream Processing Pipeline
```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

DataStream<String> stream = env.socketTextStream("localhost", 9999);
DataStream<Tuple2<String, Integer>> counts = stream
    .flatMap(new Tokenizer())
    .keyBy(value -> value.f0)
    .window(TumblingProcessingTimeWindows.of(Time.seconds(5)))
    .sum(1);

counts.print();
env.execute("Word Count");
```

### Basic Transformations
```java
// Map
stream.map(value -> value.toUpperCase())

// Filter
stream.filter(value -> value.length() > 5)

// FlatMap
stream.flatMap((value, out) -> {
    for (String word : value.split(" ")) {
        out.collect(word);
    }
})

// KeyBy and Reduce
stream.keyBy(Event::getKey).reduce((a, b) -> new Event(a.getKey(), a.getValue() + b.getValue()))
```

## Windowing

### Window Types
```java
// Tumbling windows
.window(TumblingProcessingTimeWindows.of(Time.minutes(5)))
.window(TumblingEventTimeWindows.of(Time.minutes(5)))

// Sliding windows
.window(SlidingProcessingTimeWindows.of(Time.minutes(10), Time.minutes(5)))
.window(SlidingEventTimeWindows.of(Time.minutes(10), Time.minutes(5)))

// Session windows
.window(ProcessingTimeSessionWindows.withGap(Time.minutes(10)))
.window(EventTimeSessionWindows.withGap(Time.minutes(10)))

// Count windows
.countWindow(100)
.countWindow(100, 50) // sliding count window
```

### Window Functions
```java
// Aggregate function
.aggregate(new AggregateFunction<Event, Accumulator, Result>() {
    public Accumulator createAccumulator() { return new Accumulator(); }
    public Accumulator add(Event event, Accumulator acc) { return acc.add(event); }
    public Result getResult(Accumulator acc) { return acc.getResult(); }
    public Accumulator merge(Accumulator a, Accumulator b) { return a.merge(b); }
})

// Process window function
.process(new ProcessWindowFunction<Event, Result, String, TimeWindow>() {
    public void process(String key, Context context, Iterable<Event> elements, Collector<Result> out) {
        // Custom window processing logic
    }
})
```

## State Management

### Keyed State
```java
public class StatefulFunction extends KeyedProcessFunction<String, Event, Result> {
    private ValueState<Long> countState;
    private ListState<Event> eventListState;
    private MapState<String, Double> mapState;
    
    @Override
    public void open(Configuration parameters) {
        ValueStateDescriptor<Long> countDescriptor = 
            new ValueStateDescriptor<>("count", Long.class, 0L);
        countState = getRuntimeContext().getState(countDescriptor);
        
        ListStateDescriptor<Event> listDescriptor = 
            new ListStateDescriptor<>("events", Event.class);
        eventListState = getRuntimeContext().getListState(listDescriptor);
        
        MapStateDescriptor<String, Double> mapDescriptor = 
            new MapStateDescriptor<>("map", String.class, Double.class);
        mapState = getRuntimeContext().getMapState(mapDescriptor);
    }
    
    @Override
    public void processElement(Event event, Context ctx, Collector<Result> out) {
        // Use state
        Long count = countState.value();
        countState.update(count + 1);
        
        eventListState.add(event);
        mapState.put(event.getKey(), event.getValue());
    }
}
```

### State TTL
```java
StateTtlConfig ttlConfig = StateTtlConfig
    .newBuilder(Time.hours(1))
    .setUpdateType(StateTtlConfig.UpdateType.OnCreateAndWrite)
    .setStateVisibility(StateTtlConfig.StateVisibility.NeverReturnExpired)
    .cleanupIncrementally(10, true)
    .build();

ValueStateDescriptor<String> descriptor = new ValueStateDescriptor<>("state", String.class);
descriptor.enableTimeToLive(ttlConfig);
```

## Event Time and Watermarks

### Watermark Strategy
```java
WatermarkStrategy<Event> watermarkStrategy = WatermarkStrategy
    .<Event>forBoundedOutOfOrderness(Duration.ofSeconds(10))
    .withTimestampAssigner((event, timestamp) -> event.getTimestamp())
    .withIdleness(Duration.ofMinutes(1));

stream.assignTimestampsAndWatermarks(watermarkStrategy);
```

### Late Data Handling
```java
OutputTag<Event> lateOutputTag = new OutputTag<Event>("late-data"){};

SingleOutputStreamOperator<Result> result = stream
    .keyBy(Event::getKey)
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .allowedLateness(Time.minutes(1))
    .sideOutputLateData(lateOutputTag)
    .process(new WindowProcessFunction());

DataStream<Event> lateStream = result.getSideOutput(lateOutputTag);
```

## Connectors

### Kafka
```java
// Kafka Consumer
Properties props = new Properties();
props.setProperty("bootstrap.servers", "localhost:9092");
props.setProperty("group.id", "flink-group");

FlinkKafkaConsumer<String> consumer = new FlinkKafkaConsumer<>(
    "input-topic", new SimpleStringSchema(), props);

DataStream<String> stream = env.addSource(consumer);

// Kafka Producer
FlinkKafkaProducer<String> producer = new FlinkKafkaProducer<>(
    "output-topic", new SimpleStringSchema(), props);

stream.addSink(producer);
```

### JDBC
```java
// JDBC Sink
stream.addSink(JdbcSink.sink(
    "INSERT INTO table (id, name, value) VALUES (?, ?, ?)",
    (statement, event) -> {
        statement.setLong(1, event.getId());
        statement.setString(2, event.getName());
        statement.setDouble(3, event.getValue());
    },
    JdbcExecutionOptions.builder()
        .withBatchSize(1000)
        .withBatchIntervalMs(200)
        .withMaxRetries(5)
        .build(),
    new JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
        .withUrl("jdbc:postgresql://localhost:5432/db")
        .withDriverName("org.postgresql.Driver")
        .withUsername("user")
        .withPassword("password")
        .build()
));
```

## Checkpointing

### Configuration
```java
// Enable checkpointing
env.enableCheckpointing(5000, CheckpointingMode.EXACTLY_ONCE);

CheckpointConfig config = env.getCheckpointConfig();
config.setMinPauseBetweenCheckpoints(500);
config.setCheckpointTimeout(60000);
config.setMaxConcurrentCheckpoints(1);
config.setExternalizedCheckpointCleanup(
    CheckpointConfig.ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION);

// State backend
env.setStateBackend(new HashMapStateBackend());
env.getCheckpointConfig().setCheckpointStorage("hdfs://namenode:port/checkpoints");
```

### Restart Strategy
```java
env.setRestartStrategy(RestartStrategies.fixedDelayRestart(3, Time.seconds(10)));
env.setRestartStrategy(RestartStrategies.exponentialDelayRestart(
    Time.seconds(1), Time.minutes(10), 1.2, Time.minutes(5), 0.1));
```

## Table API and SQL

### Table Environment
```java
StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env);

// Register table
tableEnv.createTemporaryView("events", eventStream, 
    $("user_id"), $("amount"), $("timestamp"));

// SQL query
Table result = tableEnv.sqlQuery(
    "SELECT user_id, SUM(amount) as total " +
    "FROM events " +
    "GROUP BY user_id, TUMBLE(timestamp, INTERVAL '1' HOUR)");

// Convert back to stream
DataStream<Row> resultStream = tableEnv.toAppendStream(result, Row.class);
```

### Window Aggregations
```sql
-- Tumbling window
SELECT 
    TUMBLE_START(timestamp, INTERVAL '1' HOUR) as window_start,
    COUNT(*) as event_count,
    SUM(amount) as total_amount
FROM events
GROUP BY TUMBLE(timestamp, INTERVAL '1' HOUR)

-- Sliding window
SELECT 
    HOP_START(timestamp, INTERVAL '5' MINUTE, INTERVAL '1' HOUR) as window_start,
    AVG(amount) as avg_amount
FROM events
GROUP BY HOP(timestamp, INTERVAL '5' MINUTE, INTERVAL '1' HOUR)

-- Session window
SELECT 
    SESSION_START(timestamp, INTERVAL '30' MINUTE) as session_start,
    COUNT(*) as session_events
FROM events
GROUP BY SESSION(timestamp, INTERVAL '30' MINUTE)
```

## Complex Event Processing (CEP)

### Pattern Definition
```java
Pattern<Event, ?> pattern = Pattern.<Event>begin("start")
    .where(SimpleCondition.of(event -> event.getType().equals("LOGIN")))
    .next("middle")
    .where(SimpleCondition.of(event -> event.getType().equals("PURCHASE")))
    .within(Time.minutes(10));

PatternStream<Event> patternStream = CEP.pattern(
    eventStream.keyBy(Event::getUserId), pattern);

DataStream<Alert> alerts = patternStream.select(
    (PatternSelectFunction<Event, Alert>) match -> {
        Event login = match.get("start").get(0);
        Event purchase = match.get("middle").get(0);
        return new Alert(login.getUserId(), "Purchase after login");
    });
```

### Complex Patterns
```java
// Quantifiers
Pattern.<Event>begin("start")
    .where(condition)
    .times(2, 4)  // between 2 and 4 occurrences
    .optional()   // optional pattern
    .oneOrMore()  // one or more occurrences

// Conditions
Pattern.<Event>begin("start")
    .where(SimpleCondition.of(event -> event.getValue() > 100))
    .or(SimpleCondition.of(event -> event.getType().equals("SPECIAL")))

// Contiguity
Pattern.<Event>begin("start")
    .next("middle")           // strict contiguity
    .followedBy("end")        // relaxed contiguity
    .followedByAny("final")   // non-deterministic relaxed contiguity
    .notNext("unwanted")      // strict until
    .notFollowedBy("ignored") // relaxed until
```

## Performance Tuning

### Parallelism
```java
env.setParallelism(4);
stream.map(new MapFunction()).setParallelism(8);
stream.keyBy().window().aggregate().setParallelism(2);
```

### Memory Configuration
```java
Configuration config = new Configuration();
config.setString("taskmanager.memory.process.size", "4g");
config.setString("taskmanager.memory.flink.size", "3g");
config.setFloat("taskmanager.memory.network.fraction", 0.15f);
config.setFloat("taskmanager.memory.managed.fraction", 0.4f);
```

### Object Reuse
```java
env.getConfig().enableObjectReuse();
env.getConfig().setLatencyTrackingInterval(1000);
```

## Monitoring

### Metrics
```java
public class MetricsFunction extends RichMapFunction<Event, Event> {
    private Counter counter;
    private Histogram histogram;
    private Gauge<Long> gauge;
    
    @Override
    public void open(Configuration parameters) {
        MetricGroup metricGroup = getRuntimeContext().getMetricGroup();
        counter = metricGroup.counter("events_processed");
        histogram = metricGroup.histogram("processing_time");
        gauge = metricGroup.gauge("queue_size", () -> getQueueSize());
    }
    
    @Override
    public Event map(Event event) throws Exception {
        counter.inc();
        long startTime = System.currentTimeMillis();
        
        Event result = processEvent(event);
        
        histogram.update(System.currentTimeMillis() - startTime);
        return result;
    }
}
```

### Configuration
```yaml
# Prometheus metrics
metrics.reporters: prometheus
metrics.reporter.prometheus.class: org.apache.flink.metrics.prometheus.PrometheusReporter
metrics.reporter.prometheus.port: 9249

# JMX metrics
metrics.reporter.jmx.class: org.apache.flink.metrics.jmx.JMXReporter
metrics.reporter.jmx.port: 9999
```

## Common Patterns

### Enrichment
```java
// Async enrichment
AsyncDataStream.unorderedWait(
    stream,
    new AsyncEnrichmentFunction(),
    1000, TimeUnit.MILLISECONDS, 100);

// Broadcast enrichment
MapStateDescriptor<String, Config> configDescriptor = 
    new MapStateDescriptor<>("config", String.class, Config.class);

BroadcastStream<Config> configBroadcast = configStream.broadcast(configDescriptor);

stream.connect(configBroadcast)
    .process(new BroadcastProcessFunction<Event, Config, EnrichedEvent>() {
        // Implementation
    });
```

### Deduplication
```java
stream.keyBy(Event::getId)
    .process(new KeyedProcessFunction<String, Event, Event>() {
        private ValueState<Boolean> seen;
        
        @Override
        public void processElement(Event event, Context ctx, Collector<Event> out) {
            if (seen.value() == null) {
                seen.update(true);
                out.collect(event);
            }
        }
    });
```

### Session Analysis
```java
stream.keyBy(Event::getUserId)
    .window(EventTimeSessionWindows.withGap(Time.minutes(30)))
    .aggregate(new SessionAggregator());
```