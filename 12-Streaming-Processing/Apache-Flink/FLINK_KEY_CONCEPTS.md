# Apache Flink Key Concepts

## 1. Flink Architecture
**Components**:
- **JobManager**: Coordinates distributed execution
- **TaskManager**: Execute tasks and manage memory
- **Client**: Submits jobs to cluster

**Processing Model**:
```java
// Stream processing pipeline
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

## 2. DataStream API
```java
// Basic transformations
DataStream<String> input = env.fromElements("a", "b", "c");

// Map transformation
DataStream<String> mapped = input.map(value -> value.toUpperCase());

// Filter transformation
DataStream<String> filtered = input.filter(value -> value.length() > 1);

// FlatMap transformation
DataStream<String> words = input.flatMap(new FlatMapFunction<String, String>() {
    @Override
    public void flatMap(String sentence, Collector<String> out) {
        for (String word : sentence.split(" ")) {
            out.collect(word);
        }
    }
});

// KeyBy and aggregations
DataStream<Tuple2<String, Integer>> wordCounts = words
    .map(word -> Tuple2.of(word, 1))
    .keyBy(value -> value.f0)
    .sum(1);
```

## 3. Event Time and Watermarks
```java
// Event time configuration
env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime);

// Watermark strategy
WatermarkStrategy<MyEvent> watermarkStrategy = WatermarkStrategy
    .<MyEvent>forBoundedOutOfOrderness(Duration.ofSeconds(5))
    .withTimestampAssigner((event, timestamp) -> event.getTimestamp());

DataStream<MyEvent> stream = env
    .addSource(new MyEventSource())
    .assignTimestampsAndWatermarks(watermarkStrategy);

// Late data handling
OutputTag<MyEvent> lateOutputTag = new OutputTag<MyEvent>("late-data"){};

SingleOutputStreamOperator<MyEvent> processedStream = stream
    .keyBy(MyEvent::getKey)
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .allowedLateness(Time.minutes(1))
    .sideOutputLateData(lateOutputTag)
    .process(new MyWindowFunction());

DataStream<MyEvent> lateStream = processedStream.getSideOutput(lateOutputTag);
```

## 4. Windowing
```java
// Tumbling windows
stream
    .keyBy(value -> value.f0)
    .window(TumblingProcessingTimeWindows.of(Time.minutes(5)))
    .sum(1);

// Sliding windows
stream
    .keyBy(value -> value.f0)
    .window(SlidingProcessingTimeWindows.of(Time.minutes(10), Time.minutes(5)))
    .sum(1);

// Session windows
stream
    .keyBy(value -> value.f0)
    .window(ProcessingTimeSessionWindows.withGap(Time.minutes(10)))
    .sum(1);

// Custom window function
public class MyWindowFunction implements WindowFunction<Tuple2<String, Integer>, String, String, TimeWindow> {
    @Override
    public void apply(String key, TimeWindow window, Iterable<Tuple2<String, Integer>> input, Collector<String> out) {
        int count = 0;
        for (Tuple2<String, Integer> value : input) {
            count += value.f1;
        }
        out.collect("Key: " + key + ", Count: " + count + ", Window: " + window);
    }
}
```

## 5. State Management
```java
// Keyed state
public class CounterProcessFunction extends KeyedProcessFunction<String, String, String> {
    private ValueState<Integer> countState;
    
    @Override
    public void open(Configuration parameters) {
        ValueStateDescriptor<Integer> descriptor = new ValueStateDescriptor<>(
            "counter", Integer.class, 0);
        countState = getRuntimeContext().getState(descriptor);
    }
    
    @Override
    public void processElement(String value, Context ctx, Collector<String> out) throws Exception {
        Integer currentCount = countState.value();
        currentCount++;
        countState.update(currentCount);
        
        if (currentCount >= 10) {
            out.collect("Key " + ctx.getCurrentKey() + " reached count of " + currentCount);
            countState.clear();
        }
    }
}

// List state
ListStateDescriptor<String> descriptor = new ListStateDescriptor<>("events", String.class);
ListState<String> listState = getRuntimeContext().getListState(descriptor);

// Map state
MapStateDescriptor<String, Integer> mapDescriptor = new MapStateDescriptor<>("counts", String.class, Integer.class);
MapState<String, Integer> mapState = getRuntimeContext().getMapState(mapDescriptor);
```

## 6. Checkpointing and Fault Tolerance
```java
// Enable checkpointing
env.enableCheckpointing(5000); // Checkpoint every 5 seconds

// Checkpoint configuration
CheckpointConfig config = env.getCheckpointConfig();
config.setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE);
config.setMinPauseBetweenCheckpoints(500);
config.setCheckpointTimeout(60000);
config.setMaxConcurrentCheckpoints(1);
config.enableExternalizedCheckpoints(CheckpointConfig.ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION);

// State backend configuration
env.setStateBackend(new HashMapStateBackend());
env.getCheckpointConfig().setCheckpointStorage("hdfs://namenode:port/flink-checkpoints");

// Restart strategy
env.setRestartStrategy(RestartStrategies.fixedDelayRestart(3, Time.of(10, TimeUnit.SECONDS)));
```

## 7. Connectors
```java
// Kafka source
FlinkKafkaConsumer<String> kafkaSource = new FlinkKafkaConsumer<>(
    "input-topic",
    new SimpleStringSchema(),
    properties);

DataStream<String> stream = env.addSource(kafkaSource);

// Kafka sink
FlinkKafkaProducer<String> kafkaSink = new FlinkKafkaProducer<>(
    "output-topic",
    new SimpleStringSchema(),
    properties);

stream.addSink(kafkaSink);

// JDBC sink
JdbcSink.sink(
    "INSERT INTO sales (customer_id, amount, timestamp) VALUES (?, ?, ?)",
    (statement, sale) -> {
        statement.setString(1, sale.getCustomerId());
        statement.setDouble(2, sale.getAmount());
        statement.setTimestamp(3, Timestamp.valueOf(sale.getTimestamp()));
    },
    JdbcExecutionOptions.builder()
        .withBatchSize(1000)
        .withBatchIntervalMs(200)
        .withMaxRetries(5)
        .build(),
    new JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
        .withUrl("jdbc:postgresql://localhost:5432/mydb")
        .withDriverName("org.postgresql.Driver")
        .withUsername("user")
        .withPassword("password")
        .build()
);
```

## 8. Complex Event Processing (CEP)
```java
// Pattern definition
Pattern<Event, ?> pattern = Pattern.<Event>begin("start")
    .where(SimpleCondition.of(event -> event.getType().equals("LOGIN")))
    .next("middle")
    .where(SimpleCondition.of(event -> event.getType().equals("PURCHASE")))
    .within(Time.minutes(10));

// Pattern stream
PatternStream<Event> patternStream = CEP.pattern(eventStream.keyBy(Event::getUserId), pattern);

// Extract matches
DataStream<Alert> alerts = patternStream.select(
    (PatternSelectFunction<Event, Alert>) pattern -> {
        Event login = pattern.get("start").get(0);
        Event purchase = pattern.get("middle").get(0);
        return new Alert(login.getUserId(), "Suspicious activity detected");
    }
);

// Complex patterns
Pattern<Event, ?> complexPattern = Pattern.<Event>begin("first")
    .where(SimpleCondition.of(event -> event.getValue() > 100))
    .followedBy("second")
    .where(SimpleCondition.of(event -> event.getValue() < 50))
    .times(2, 4) // Between 2 and 4 occurrences
    .within(Time.hours(1));
```

## 9. Table API and SQL
```java
// Table environment
StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env);

// Register table
tableEnv.createTemporaryView("sales", salesStream, $("customer_id"), $("amount"), $("timestamp"));

// SQL query
Table result = tableEnv.sqlQuery(
    "SELECT customer_id, SUM(amount) as total_amount " +
    "FROM sales " +
    "GROUP BY customer_id, TUMBLE(timestamp, INTERVAL '1' HOUR)"
);

// Convert back to stream
DataStream<Row> resultStream = tableEnv.toAppendStream(result, Row.class);

// Window aggregation with Table API
Table windowedTable = tableEnv.from("sales")
    .window(Tumble.over(lit(1).hour()).on($("timestamp")).as("w"))
    .groupBy($("customer_id"), $("w"))
    .select($("customer_id"), $("amount").sum().as("total_amount"));
```

## 10. Performance Optimization
```java
// Parallelism configuration
env.setParallelism(4);
stream.map(new MyMapFunction()).setParallelism(8);

// Memory configuration
Configuration config = new Configuration();
config.setString("taskmanager.memory.process.size", "4g");
config.setString("taskmanager.memory.flink.size", "3g");

// Operator chaining
stream
    .map(new MapFunction1()).name("map1")
    .map(new MapFunction2()).name("map2").disableChaining()
    .filter(new FilterFunction()).name("filter");

// Async I/O
AsyncFunction<String, String> asyncFunction = new AsyncFunction<String, String>() {
    @Override
    public void asyncInvoke(String input, ResultFuture<String> resultFuture) {
        CompletableFuture.supplyAsync(() -> {
            // Async operation (e.g., database lookup)
            return enrichData(input);
        }).thenAccept(result -> resultFuture.complete(Collections.singleton(result)));
    }
};

DataStream<String> enrichedStream = AsyncDataStream.unorderedWait(
    stream, asyncFunction, 1000, TimeUnit.MILLISECONDS, 100);

// Resource optimization
env.getConfig().setLatencyTrackingInterval(1000);
env.getConfig().enableObjectReuse();
```