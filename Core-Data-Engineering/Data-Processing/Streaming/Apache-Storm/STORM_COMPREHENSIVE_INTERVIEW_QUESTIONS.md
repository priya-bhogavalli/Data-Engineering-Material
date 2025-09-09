
### Q1: What is Apache Storm and what problems does it solve?
**Answer:**
Apache Storm is a distributed real-time computation system for processing unbounded streams of data with guaranteed message processing.

**Key Problems Solved:**
- **Real-time Processing**: Sub-second latency for stream processing
- **Fault Tolerance**: Automatic failover and message replay
- **Scalability**: Horizontal scaling across commodity hardware
- **Guaranteed Processing**: At-least-once or exactly-once semantics
- **Language Agnostic**: Support for multiple programming languages

**Core Features:**
- Tuple-based data model
- Directed Acyclic Graph (DAG) topologies
- Automatic parallelization
- Built-in fault tolerance
- Integration with queuing systems

### Q2: Explain Storm's data model and key abstractions
**Answer:**
**Storm Data Model:**

**1. Tuple**: Immutable list of named values
```java
// Tuple example
Values tuple = new Values("user123", "login", System.currentTimeMillis());
collector.emit(tuple);
```

**2. Stream**: Unbounded sequence of tuples
```java
// Declare output streams
@Override
public void declareOutputFields(OutputFieldsDeclarer declarer) {
    declarer.declare(new Fields("user_id", "action", "timestamp"));
}
```

**3. Spout**: Source of streams (data ingestion)
```java
public class KafkaSpout extends BaseRichSpout {
    @Override
    public void nextTuple() {
        // Emit tuples from Kafka
        String message = kafkaConsumer.poll();
        collector.emit(new Values(message));
    }
}
```

**4. Bolt**: Processing logic for streams
```java
public class ProcessingBolt extends BaseRichBolt {
    @Override
    public void execute(Tuple tuple) {
        String data = tuple.getStringByField("data");
        String processed = processData(data);
        collector.emit(tuple, new Values(processed));
        collector.ack(tuple);
    }
}
```

**5. Topology**: Network of spouts and bolts
```java
TopologyBuilder builder = new TopologyBuilder();
builder.setSpout("kafka-spout", new KafkaSpout(), 2);
builder.setBolt("process-bolt", new ProcessingBolt(), 4)
       .shuffleGrouping("kafka-spout");
```

### Q3: What are the differences between Storm and Spark Streaming?
**Answer:**
**Storm vs Spark Streaming:**

| Aspect | Storm | Spark Streaming |
|--------|-------|-----------------|
| **Processing Model** | True streaming (tuple-by-tuple) | Micro-batching |
| **Latency** | Sub-second (milliseconds) | Seconds |
| **Throughput** | Lower | Higher |
| **Fault Tolerance** | Record-level acknowledgment | RDD lineage |
| **State Management** | External state stores | In-memory + checkpointing |
| **Language Support** | Java, Python, Clojure | Scala, Java, Python |
| **Learning Curve** | Steeper | Easier (if familiar with Spark) |
| **Use Cases** | Real-time alerts, fraud detection | Near real-time analytics |

**When to Use Storm:**
- Ultra-low latency requirements (< 100ms)
- Simple event processing
- Real-time alerting systems
- Fraud detection

**When to Use Spark Streaming:**
- Complex analytics on streams
- Integration with Spark ecosystem
- Higher throughput requirements
- Batch + streaming unified processing

---

## 🏗️ Architecture & Components

### Q4: Explain Storm cluster architecture
**Answer:**
**Storm Cluster Components:**

```
Client → Nimbus ← → ZooKeeper ← → Supervisor → Worker → Executor → Task
```

**1. Nimbus (Master Node)**
- Distributes code across cluster
- Assigns tasks to machines
- Monitors failures and reassigns tasks
- Stateless (state stored in ZooKeeper)

**2. Supervisor (Worker Node)**
- Listens for work assignments
- Starts/stops worker processes
- Manages local resources

**3. Worker Process**
- JVM process executing topology tasks
- Runs multiple executors
- Handles message passing

**4. Executor**
- Thread spawned by worker process
- Runs one or more tasks
- Handles tuple routing

**5. Task**
- Actual processing unit (spout/bolt instance)
- Processes tuples
- Maintains state

**6. ZooKeeper**
- Coordinates cluster state
- Stores topology metadata
- Handles leader election

### Q5: How does Storm handle fault tolerance?
**Answer:**
**Storm Fault Tolerance Mechanisms:**

**1. Message Acknowledgment:**
```java
public class ReliableBolt extends BaseRichBolt {
    @Override
    public void execute(Tuple tuple) {
        try {
            // Process tuple
            String result = processData(tuple.getString(0));
            collector.emit(tuple, new Values(result));
            collector.ack(tuple); // Acknowledge successful processing
        } catch (Exception e) {
            collector.fail(tuple); // Mark tuple as failed
        }
    }
}
```

**2. Tuple Tree Tracking:**
```java
// Storm tracks tuple lineage
collector.emit(tuple, new Values(data)); // Anchored emit
// vs
collector.emit(new Values(data)); // Unanchored emit
```

**3. Timeout and Replay:**
```java
Config conf = new Config();
conf.setMessageTimeoutSecs(30); // Tuple timeout
conf.setMaxSpoutPending(1000);  // Max unacked tuples
```

**4. Worker Process Recovery:**
- Supervisor automatically restarts failed workers
- Tasks redistributed across available workers
- No data loss due to message replay

**5. Nimbus High Availability:**
```yaml
# storm.yaml
nimbus.seeds: ["nimbus1", "nimbus2", "nimbus3"]
nimbus.ha.enabled: true
```

### Q6: Explain Storm's parallelism model
**Answer:**
**Storm Parallelism Levels:**

**1. Topology Level:**
```java
Config conf = new Config();
conf.setNumWorkers(4); // 4 worker processes across cluster
```

**2. Component Level (Parallelism Hint):**
```java
builder.setSpout("spout", new MySpout(), 2);    // 2 executors
builder.setBolt("bolt", new MyBolt(), 4);       // 4 executors
```

**3. Task Level:**
```java
builder.setBolt("bolt", new MyBolt(), 4)
       .setNumTasks(8); // 8 tasks across 4 executors (2 tasks per executor)
```

**Parallelism Configuration:**
```java
TopologyBuilder builder = new TopologyBuilder();

// Spout with 2 executors
builder.setSpout("kafka-spout", new KafkaSpout(), 2);

// Bolt with 4 executors, 8 tasks
builder.setBolt("process-bolt", new ProcessingBolt(), 4)
       .setNumTasks(8)
       .shuffleGrouping("kafka-spout");

// Aggregation bolt with 2 executors
builder.setBolt("aggregate-bolt", new AggregateBolt(), 2)
       .fieldsGrouping("process-bolt", new Fields("key"));

Config conf = new Config();
conf.setNumWorkers(3); // Distribute across 3 worker processes
```

**Dynamic Rebalancing:**
```bash
# Rebalance running topology
storm rebalance topology-name -n 5 -e spout=3 -e bolt=10
```

---

## 💻 Topology Development

### Q7: How do you implement a basic Storm topology?
**Answer:**
**Basic Storm Topology Implementation:**

**1. Spout Implementation:**
```java
public class NumberSpout extends BaseRichSpout {
    private SpoutOutputCollector collector;
    private Random random;
    
    @Override
    public void open(Map conf, TopologyContext context, SpoutOutputCollector collector) {
        this.collector = collector;
        this.random = new Random();
    }
    
    @Override
    public void nextTuple() {
        int number = random.nextInt(100);
        collector.emit(new Values(number), number); // messageId for acking
        Utils.sleep(100); // Throttle emission
    }
    
    @Override
    public void ack(Object messageId) {
        // Message successfully processed
        System.out.println("Acked: " + messageId);
    }
    
    @Override
    public void fail(Object messageId) {
        // Message failed, re-emit
        System.out.println("Failed: " + messageId);
        collector.emit(new Values((Integer) messageId), messageId);
    }
    
    @Override
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        declarer.declare(new Fields("number"));
    }
}
```

**2. Bolt Implementation:**
```java
public class SquareBolt extends BaseRichBolt {
    private OutputCollector collector;
    
    @Override
    public void prepare(Map conf, TopologyContext context, OutputCollector collector) {
        this.collector = collector;
    }
    
    @Override
    public void execute(Tuple tuple) {
        try {
            int number = tuple.getIntegerByField("number");
            int square = number * number;
            
            // Emit result (anchored to input tuple)
            collector.emit(tuple, new Values(number, square));
            collector.ack(tuple);
        } catch (Exception e) {
            collector.fail(tuple);
        }
    }
    
    @Override
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        declarer.declare(new Fields("number", "square"));
    }
}
```

**3. Topology Assembly:**
```java
public class SquareTopology {
    public static void main(String[] args) throws Exception {
        TopologyBuilder builder = new TopologyBuilder();
        
        // Add spout
        builder.setSpout("number-spout", new NumberSpout(), 1);
        
        // Add processing bolt
        builder.setBolt("square-bolt", new SquareBolt(), 2)
               .shuffleGrouping("number-spout");
        
        // Add output bolt
        builder.setBolt("print-bolt", new PrintBolt(), 1)
               .globalGrouping("square-bolt");
        
        Config conf = new Config();
        conf.setDebug(true);
        
        if (args != null && args.length > 0) {
            // Submit to cluster
            conf.setNumWorkers(3);
            StormSubmitter.submitTopology(args[0], conf, builder.createTopology());
        } else {
            // Run locally
            LocalCluster cluster = new LocalCluster();
            cluster.submitTopology("square-topology", conf, builder.createTopology());
            Utils.sleep(10000);
            cluster.killTopology("square-topology");
            cluster.shutdown();
        }
    }
}
```

### Q8: Explain different stream groupings in Storm
**Answer:**
**Storm Stream Groupings:**

**1. Shuffle Grouping (Random Distribution):**
```java
builder.setBolt("process-bolt", new ProcessBolt(), 4)
       .shuffleGrouping("input-spout");
// Tuples randomly distributed across bolt tasks
```

**2. Fields Grouping (Hash Partitioning):**
```java
builder.setBolt("aggregate-bolt", new AggregateBolt(), 3)
       .fieldsGrouping("process-bolt", new Fields("user_id"));
// Same user_id always goes to same bolt task
```

**3. All Grouping (Broadcast):**
```java
builder.setBolt("config-bolt", new ConfigBolt(), 2)
       .allGrouping("config-spout");
// All tuples sent to all bolt tasks
```

**4. Global Grouping (Single Task):**
```java
builder.setBolt("global-counter", new CounterBolt(), 3)
       .globalGrouping("input-spout");
// All tuples go to single bolt task (lowest task id)
```

**5. None Grouping (Same as Shuffle):**
```java
builder.setBolt("process-bolt", new ProcessBolt(), 4)
       .noneGrouping("input-spout");
```

**6. Direct Grouping (Producer Decides):**
```java
// In producer bolt
collector.emitDirect(taskId, tuple, new Values(data));

// In topology
builder.setBolt("target-bolt", new TargetBolt(), 2)
       .directGrouping("producer-bolt");
```

**7. Local or Shuffle Grouping:**
```java
builder.setBolt("process-bolt", new ProcessBolt(), 4)
       .localOrShuffleGrouping("input-spout");
// Prefer local tasks, fallback to shuffle
```

**8. Custom Grouping:**
```java
public class CustomGrouping implements CustomStreamGrouping {
    @Override
    public void prepare(WorkerTopologyContext context, GlobalStreamId stream, List<Integer> targetTasks) {
        this.targetTasks = targetTasks;
    }
    
    @Override
    public List<Integer> chooseTasks(int taskId, List<Object> values) {
        // Custom logic to choose target tasks
        String key = (String) values.get(0);
        int hash = key.hashCode();
        int index = Math.abs(hash) % targetTasks.size();
        return Arrays.asList(targetTasks.get(index));
    }
}

builder.setBolt("custom-bolt", new CustomBolt(), 3)
       .customGrouping("input-spout", new CustomGrouping());
```

### Q9: How do you handle state management in Storm?
**Answer:**
**Storm State Management Approaches:**

**1. External State Stores:**
```java
public class StatefulBolt extends BaseRichBolt {
    private Jedis redis;
    private OutputCollector collector;
    
    @Override
    public void prepare(Map conf, TopologyContext context, OutputCollector collector) {
        this.collector = collector;
        this.redis = new Jedis("localhost", 6379);
    }
    
    @Override
    public void execute(Tuple tuple) {
        String key = tuple.getStringByField("key");
        String value = tuple.getStringByField("value");
        
        // Read current state
        String currentValue = redis.get(key);
        
        // Update state
        String newValue = updateValue(currentValue, value);
        redis.set(key, newValue);
        
        collector.emit(tuple, new Values(key, newValue));
        collector.ack(tuple);
    }
}
```

**2. In-Memory State (Non-persistent):**
```java
public class CounterBolt extends BaseRichBolt {
    private Map<String, Long> counters;
    
    @Override
    public void prepare(Map conf, TopologyContext context, OutputCollector collector) {
        this.counters = new HashMap<>();
    }
    
    @Override
    public void execute(Tuple tuple) {
        String key = tuple.getStringByField("key");
        Long count = counters.getOrDefault(key, 0L);
        counters.put(key, count + 1);
        
        collector.emit(tuple, new Values(key, count + 1));
        collector.ack(tuple);
    }
}
```

**3. Trident State (Transactional):**
```java
TridentTopology topology = new TridentTopology();
TridentState wordCounts = topology.newStream("spout", spout)
    .each(new Fields("sentence"), new Split(), new Fields("word"))
    .groupBy(new Fields("word"))
    .persistentAggregate(new MemoryMapState.Factory(), new Count(), new Fields("count"));
```

**4. Database Integration:**
```java
public class DatabaseBolt extends BaseRichBolt {
    private Connection connection;
    
    @Override
    public void prepare(Map conf, TopologyContext context, OutputCollector collector) {
        String url = "jdbc:postgresql://localhost:5432/stormdb";
        connection = DriverManager.getConnection(url, "user", "password");
    }
    
    @Override
    public void execute(Tuple tuple) {
        try {
            String sql = "INSERT INTO events (id, data, timestamp) VALUES (?, ?, ?)";
            PreparedStatement stmt = connection.prepareStatement(sql);
            stmt.setString(1, tuple.getStringByField("id"));
            stmt.setString(2, tuple.getStringByField("data"));
            stmt.setTimestamp(3, new Timestamp(System.currentTimeMillis()));
            stmt.executeUpdate();
            
            collector.ack(tuple);
        } catch (SQLException e) {
            collector.fail(tuple);
        }
    }
}
```

---

## 🌊 Stream Processing

### Q10: How do you implement windowing in Storm?
**Answer:**
**Storm Windowing Implementation:**

**1. Time-based Windows:**
```java
public class WindowedBolt extends BaseWindowedBolt {
    @Override
    public void execute(TupleWindow inputWindow) {
        List<Tuple> tuples = inputWindow.get();
        
        // Process all tuples in window
        int sum = 0;
        for (Tuple tuple : tuples) {
            sum += tuple.getIntegerByField("value");
        }
        
        // Emit aggregated result
        collector.emit(new Values(sum, tuples.size()));
        
        // Ack all tuples in window
        for (Tuple tuple : tuples) {
            collector.ack(tuple);
        }
    }
    
    @Override
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        declarer.declare(new Fields("sum", "count"));
    }
}

// Configure windowing
builder.setBolt("windowed-bolt", new WindowedBolt(), 1)
       .withWindow(Duration.seconds(10), Duration.seconds(5)) // 10s window, 5s slide
       .shuffleGrouping("input-spout");
```

**2. Count-based Windows:**
```java
builder.setBolt("count-windowed-bolt", new CountWindowedBolt(), 1)
       .withWindow(new Count(100), new Count(50)) // 100 tuples window, 50 tuples slide
       .shuffleGrouping("input-spout");
```

**3. Custom Windowing:**
```java
public class CustomWindowedBolt extends BaseWindowedBolt {
    @Override
    public void execute(TupleWindow inputWindow) {
        List<Tuple> newTuples = inputWindow.getNew();      // New tuples in this window
        List<Tuple> expiredTuples = inputWindow.getExpired(); // Expired tuples
        List<Tuple> allTuples = inputWindow.get();         // All tuples in window
        
        // Custom windowing logic
        processWindow(newTuples, expiredTuples, allTuples);
    }
}
```

**4. Watermark-based Processing:**
```java
public class WatermarkBolt extends BaseRichBolt {
    private long watermark = 0;
    private Map<Long, List<Tuple>> timeWindows = new TreeMap<>();
    
    @Override
    public void execute(Tuple tuple) {
        long timestamp = tuple.getLongByField("timestamp");
        
        // Update watermark
        watermark = Math.max(watermark, timestamp - 5000); // 5 second delay
        
        // Add tuple to appropriate window
        long windowStart = (timestamp / 10000) * 10000; // 10 second windows
        timeWindows.computeIfAbsent(windowStart, k -> new ArrayList<>()).add(tuple);
        
        // Process completed windows
        Iterator<Map.Entry<Long, List<Tuple>>> iterator = timeWindows.entrySet().iterator();
        while (iterator.hasNext()) {
            Map.Entry<Long, List<Tuple>> entry = iterator.next();
            if (entry.getKey() + 10000 <= watermark) {
                processWindow(entry.getValue());
                iterator.remove();
            }
        }
        
        collector.ack(tuple);
    }
}
```

### Q11: How do you implement exactly-once processing in Storm?
**Answer:**
**Exactly-Once Processing Strategies:**

**1. Trident Framework:**
```java
TridentTopology topology = new TridentTopology();

// Trident provides exactly-once semantics
topology.newStream("kafka-spout", kafkaSpout)
    .each(new Fields("str"), new Split(), new Fields("word"))
    .groupBy(new Fields("word"))
    .persistentAggregate(new MemoryMapState.Factory(), new Count(), new Fields("count"));
```

**2. Transactional Spouts:**
```java
public class TransactionalKafkaSpout implements ITransactionalSpout<TransactionMetadata> {
    @Override
    public ITransactionalSpout.Coordinator<TransactionMetadata> getCoordinator(Map conf, TopologyContext context) {
        return new KafkaCoordinator();
    }
    
    @Override
    public ITransactionalSpout.Emitter<TransactionMetadata> getEmitter(Map conf, TopologyContext context) {
        return new KafkaEmitter();
    }
    
    private class KafkaCoordinator implements ITransactionalSpout.Coordinator<TransactionMetadata> {
        @Override
        public TransactionMetadata initializeTransaction(long txid, TransactionMetadata prevMetadata) {
            // Initialize transaction with unique ID
            return new TransactionMetadata(txid, getKafkaOffsets());
        }
    }
}
```

**3. Idempotent Operations:**
```java
public class IdempotentBolt extends BaseRichBolt {
    private Set<String> processedIds;
    
    @Override
    public void execute(Tuple tuple) {
        String messageId = tuple.getStringByField("id");
        
        // Check if already processed
        if (processedIds.contains(messageId)) {
            collector.ack(tuple);
            return;
        }
        
        // Process message
        processMessage(tuple);
        processedIds.add(messageId);
        
        collector.ack(tuple);
    }
}
```

**4. Database Transactions:**
```java
public class TransactionalBolt extends BaseRichBolt {
    @Override
    public void execute(Tuple tuple) {
        Connection conn = null;
        try {
            conn = dataSource.getConnection();
            conn.setAutoCommit(false);
            
            // Check if already processed
            String messageId = tuple.getStringByField("id");
            if (isAlreadyProcessed(conn, messageId)) {
                collector.ack(tuple);
                return;
            }
            
            // Process message in transaction
            processMessage(conn, tuple);
            markAsProcessed(conn, messageId);
            
            conn.commit();
            collector.ack(tuple);
        } catch (Exception e) {
            if (conn != null) conn.rollback();
            collector.fail(tuple);
        }
    }
}
```

---

## ⚡ Performance & Scalability

### Q12: How do you optimize Storm topology performance?
**Answer:**
**Storm Performance Optimization:**

**1. Parallelism Tuning:**
```java
Config conf = new Config();
conf.setNumWorkers(8); // Increase worker processes

// Optimize component parallelism
builder.setSpout("kafka-spout", new KafkaSpout(), 4);
builder.setBolt("process-bolt", new ProcessBolt(), 16) // High parallelism for CPU-intensive
       .shuffleGrouping("kafka-spout");
builder.setBolt("output-bolt", new OutputBolt(), 4)   // Lower parallelism for I/O
       .shuffleGrouping("process-bolt");
```

**2. Batch Processing:**
```java
public class BatchingBolt extends BaseRichBolt {
    private List<Tuple> batch = new ArrayList<>();
    private static final int BATCH_SIZE = 100;
    
    @Override
    public void execute(Tuple tuple) {
        batch.add(tuple);
        
        if (batch.size() >= BATCH_SIZE) {
            processBatch(batch);
            for (Tuple t : batch) {
                collector.ack(t);
            }
            batch.clear();
        }
    }
    
    private void processBatch(List<Tuple> tuples) {
        // Batch processing logic
        List<String> data = tuples.stream()
            .map(t -> t.getStringByField("data"))
            .collect(Collectors.toList());
        
        // Bulk database operation
        bulkInsert(data);
    }
}
```

**3. Memory Management:**
```java
Config conf = new Config();
conf.put(Config.WORKER_HEAP_MEMORY_MB, 2048);
conf.put(Config.TOPOLOGY_COMPONENT_RESOURCES_ONHEAP_MEMORY_MB, 512);

// JVM tuning
conf.put(Config.TOPOLOGY_WORKER_CHILDOPTS, 
    "-Xmx2g -XX:+UseG1GC -XX:MaxGCPauseMillis=200");
```

**4. Serialization Optimization:**
```java
// Use Kryo serialization
conf.registerSerialization(MyClass.class, MyClassSerializer.class);
conf.setKryoFactory(MyKryoFactory.class);
```

**5. Topology Configuration:**
```java
Config conf = new Config();
conf.setMaxSpoutPending(1000);           // Limit unacked tuples
conf.setMessageTimeoutSecs(30);          // Tuple timeout
conf.put(Config.TOPOLOGY_RECEIVER_BUFFER_SIZE, 8);
conf.put(Config.TOPOLOGY_TRANSFER_BUFFER_SIZE, 32);
conf.put(Config.TOPOLOGY_EXECUTOR_RECEIVE_BUFFER_SIZE, 16384);
conf.put(Config.TOPOLOGY_EXECUTOR_SEND_BUFFER_SIZE, 16384);
```

### Q13: How do you monitor Storm topologies?
**Answer:**
**Storm Monitoring Strategies:**

**1. Storm UI Metrics:**
```bash
# Access Storm UI
http://nimbus-host:8080

# Key metrics to monitor:
# - Topology summary (uptime, workers, executors)
# - Spout metrics (emitted, transferred, acked, failed)
# - Bolt metrics (executed, process latency, capacity)
# - Error messages and exceptions
```

**2. JMX Monitoring:**
```java
// Enable JMX in storm.yaml
supervisor.childopts: "-Xmx1024m -Dcom.sun.management.jmxremote"

// Custom metrics in bolts
public class MonitoredBolt extends BaseRichBolt {
    private transient CountMetric countMetric;
    private transient ReducedMetric latencyMetric;
    
    @Override
    public void prepare(Map conf, TopologyContext context, OutputCollector collector) {
        this.countMetric = new CountMetric();
        this.latencyMetric = new ReducedMetric(new MeanReducer());
        
        context.registerMetric("execute-count", countMetric, 60);
        context.registerMetric("execute-latency", latencyMetric, 60);
    }
    
    @Override
    public void execute(Tuple tuple) {
        long startTime = System.currentTimeMillis();
        
        // Process tuple
        processData(tuple);
        
        long latency = System.currentTimeMillis() - startTime;
        countMetric.incr();
        latencyMetric.update(latency);
        
        collector.ack(tuple);
    }
}
```

**3. External Monitoring:**
```java
// Graphite integration
public class GraphiteMetricsBolt extends BaseRichBolt {
    private GraphiteReporter reporter;
    
    @Override
    public void prepare(Map conf, TopologyContext context, OutputCollector collector) {
        Graphite graphite = new Graphite(new InetSocketAddress("graphite-host", 2003));
        reporter = GraphiteReporter.forRegistry(MetricRegistry.shared())
            .prefixedWith("storm.topology")
            .build(graphite);
        reporter.start(30, TimeUnit.SECONDS);
    }
}
```

**4. Health Check Script:**
```bash
#!/bin/bash
# storm-health-check.sh

TOPOLOGY_NAME=$1
STORM_UI_HOST="localhost:8080"

# Check topology status
STATUS=$(curl -s "http://$STORM_UI_HOST/api/v1/topology/summary" | \
         jq -r ".topologies[] | select(.name==\"$TOPOLOGY_NAME\") | .status")

if [ "$STATUS" != "ACTIVE" ]; then
    echo "CRITICAL: Topology $TOPOLOGY_NAME is $STATUS"
    exit 2
fi

# Check error count
ERRORS=$(curl -s "http://$STORM_UI_HOST/api/v1/topology/$TOPOLOGY_NAME" | \
         jq -r '.topologyStats[0].failed')

if [ "$ERRORS" -gt 100 ]; then
    echo "WARNING: High error count: $ERRORS"
    exit 1
fi

echo "OK: Topology $TOPOLOGY_NAME is healthy"
exit 0
```

---

## 🔗 Integration & Use Cases

### Q14: How do you integrate Storm with Kafka?
**Answer:**
**Storm-Kafka Integration:**

**1. Kafka Spout Configuration:**
```java
// Storm-Kafka dependency
<dependency>
    <groupId>org.apache.storm</groupId>
    <artifactId>storm-kafka-client</artifactId>
    <version>2.4.0</version>
</dependency>

// Kafka spout setup
KafkaSpoutConfig<String, String> kafkaConf = KafkaSpoutConfig.builder("localhost:9092", "input-topic")
    .setGroupId("storm-consumer-group")
    .setOffsetCommitPeriodMs(30000)
    .setFirstPollOffsetStrategy(FirstPollOffsetStrategy.LATEST)
    .setMaxUncommittedOffsets(250)
    .setProcessingGuarantee(ProcessingGuarantee.AT_LEAST_ONCE)
    .build();

KafkaSpout<String, String> kafkaSpout = new KafkaSpout<>(kafkaConf);

TopologyBuilder builder = new TopologyBuilder();
builder.setSpout("kafka-spout", kafkaSpout, 2);
```

**2. Processing Pipeline:**
```java
public class KafkaProcessingTopology {
    public static void main(String[] args) throws Exception {
        TopologyBuilder builder = new TopologyBuilder();
        
        // Kafka spout
        KafkaSpoutConfig<String, String> kafkaConf = KafkaSpoutConfig
            .builder("kafka1:9092,kafka2:9092", "events")
            .setGroupId("storm-processors")
            .build();
        
        builder.setSpout("kafka-spout", new KafkaSpout<>(kafkaConf), 3);
        
        // JSON parsing bolt
        builder.setBolt("parse-bolt", new JsonParsingBolt(), 6)
               .shuffleGrouping("kafka-spout");
        
        // Enrichment bolt
        builder.setBolt("enrich-bolt", new EnrichmentBolt(), 4)
               .fieldsGrouping("parse-bolt", new Fields("user_id"));
        
        // Output to another Kafka topic
        builder.setBolt("kafka-output", new KafkaOutputBolt(), 2)
               .shuffleGrouping("enrich-bolt");
        
        Config conf = new Config();
        conf.setNumWorkers(3);
        StormSubmitter.submitTopology("kafka-processing", conf, builder.createTopology());
    }
}
```

**3. Kafka Output Bolt:**
```java
public class KafkaOutputBolt extends BaseRichBolt {
    private KafkaProducer<String, String> producer;
    private OutputCollector collector;
    
    @Override
    public void prepare(Map conf, TopologyContext context, OutputCollector collector) {
        this.collector = collector;
        
        Properties props = new Properties();
        props.put("bootstrap.servers", "kafka1:9092,kafka2:9092");
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("acks", "1");
        
        this.producer = new KafkaProducer<>(props);
    }
    
    @Override
    public void execute(Tuple tuple) {
        try {
            String key = tuple.getStringByField("key");
            String value = tuple.getStringByField("value");
            
            ProducerRecord<String, String> record = new ProducerRecord<>("output-topic", key, value);
            
            producer.send(record, (metadata, exception) -> {
                if (exception == null) {
                    collector.ack(tuple);
                } else {
                    collector.fail(tuple);
                }
            });
        } catch (Exception e) {
            collector.fail(tuple);
        }
    }
    
    @Override
    public void cleanup() {
        if (producer != null) {
            producer.close();
        }
    }
}
```

### Q15: Implement a real-time analytics system using Storm
**Answer:**
**Real-time Analytics System:**

**1. System Architecture:**
```
Data Sources → Kafka → Storm → Redis/HBase → Dashboard
```

**2. Analytics Topology:**
```java
public class RealTimeAnalyticsTopology {
    public static void main(String[] args) throws Exception {
        TopologyBuilder builder = new TopologyBuilder();
        
        // Kafka spout for event ingestion
        KafkaSpoutConfig<String, String> kafkaConf = KafkaSpoutConfig
            .builder("kafka:9092", "user-events")
            .setGroupId("analytics-consumer")
            .build();
        
        builder.setSpout("event-spout", new KafkaSpout<>(kafkaConf), 4);
        
        // Event parsing and validation
        builder.setBolt("parse-bolt", new EventParsingBolt(), 8)
               .shuffleGrouping("event-spout");
        
        // Real-time aggregations
        builder.setBolt("session-bolt", new SessionTrackingBolt(), 6)
               .fieldsGrouping("parse-bolt", new Fields("user_id"));
        
        builder.setBolt("metrics-bolt", new MetricsAggregationBolt(), 4)
               .fieldsGrouping("parse-bolt", new Fields("event_type"));
        
        // Windowed analytics
        builder.setBolt("windowed-analytics", new WindowedAnalyticsBolt(), 3)
               .withWindow(Duration.minutes(5), Duration.minutes(1))
               .shuffleGrouping("parse-bolt");
        
        // Output to storage
        builder.setBolt("redis-bolt", new RedisBolt(), 2)
               .shuffleGrouping("session-bolt")
               .shuffleGrouping("metrics-bolt")
               .shuffleGrouping("windowed-analytics");
        
        Config conf = new Config();
        conf.setNumWorkers(4);
        StormSubmitter.submitTopology("real-time-analytics", conf, builder.createTopology());
    }
}
```

**3. Session Tracking Bolt:**
```java
public class SessionTrackingBolt extends BaseRichBolt {
    private Map<String, UserSession> activeSessions;
    private OutputCollector collector;
    private static final long SESSION_TIMEOUT = 30 * 60 * 1000; // 30 minutes
    
    @Override
    public void prepare(Map conf, TopologyContext context, OutputCollector collector) {
        this.collector = collector;
        this.activeSessions = new HashMap<>();
        
        // Cleanup expired sessions periodically
        Timer timer = new Timer();
        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                cleanupExpiredSessions();
            }
        }, 60000, 60000); // Every minute
    }
    
    @Override
    public void execute(Tuple tuple) {
        String userId = tuple.getStringByField("user_id");
        String eventType = tuple.getStringByField("event_type");
        long timestamp = tuple.getLongByField("timestamp");
        
        UserSession session = activeSessions.get(userId);
        
        if (session == null || timestamp - session.getLastActivity() > SESSION_TIMEOUT) {
            // Start new session
            session = new UserSession(userId, timestamp);
            activeSessions.put(userId, session);
            
            collector.emit(tuple, new Values("session_start", userId, timestamp));
        }
        
        // Update session
        session.addEvent(eventType, timestamp);
        
        // Emit session metrics
        collector.emit(tuple, new Values("session_update", userId, 
                      session.getEventCount(), session.getDuration()));
        
        collector.ack(tuple);
    }
    
    private void cleanupExpiredSessions() {
        long now = System.currentTimeMillis();
        Iterator<Map.Entry<String, UserSession>> iterator = activeSessions.entrySet().iterator();
        
        while (iterator.hasNext()) {
            Map.Entry<String, UserSession> entry = iterator.next();
            if (now - entry.getValue().getLastActivity() > SESSION_TIMEOUT) {
                // Emit session end event
                collector.emit(new Values("session_end", entry.getKey(), 
                              entry.getValue().getEventCount(), entry.getValue().getDuration()));
                iterator.remove();
            }
        }
    }
}
```

**4. Windowed Analytics Bolt:**
```java
public class WindowedAnalyticsBolt extends BaseWindowedBolt {
    private OutputCollector collector;
    
    @Override
    public void prepare(Map conf, TopologyContext context, OutputCollector collector) {
        this.collector = collector;
    }
    
    @Override
    public void execute(TupleWindow inputWindow) {
        List<Tuple> tuples = inputWindow.get();
        
        // Calculate metrics for the window
        Map<String, Long> eventCounts = new HashMap<>();
        Map<String, Set<String>> uniqueUsers = new HashMap<>();
        long windowStart = Long.MAX_VALUE;
        long windowEnd = Long.MIN_VALUE;
        
        for (Tuple tuple : tuples) {
            String eventType = tuple.getStringByField("event_type");
            String userId = tuple.getStringByField("user_id");
            long timestamp = tuple.getLongByField("timestamp");
            
            // Count events by type
            eventCounts.merge(eventType, 1L, Long::sum);
            
            // Track unique users per event type
            uniqueUsers.computeIfAbsent(eventType, k -> new HashSet<>()).add(userId);
            
            // Track window boundaries
            windowStart = Math.min(windowStart, timestamp);
            windowEnd = Math.max(windowEnd, timestamp);
        }
        
        // Emit aggregated metrics
        for (Map.Entry<String, Long> entry : eventCounts.entrySet()) {
            String eventType = entry.getKey();
            long count = entry.getValue();
            int uniqueUserCount = uniqueUsers.get(eventType).size();
            
            collector.emit(new Values("window_metrics", eventType, count, 
                          uniqueUserCount, windowStart, windowEnd));
        }
        
        // Ack all tuples
        for (Tuple tuple : tuples) {
            collector.ack(tuple);
        }
    }
}
```

---

## 🔧 Troubleshooting

### Q16: What are common Storm issues and how do you resolve them?
**Answer:**
**Common Storm Issues:**

**1. Worker Process Crashes:**
```bash
# Check supervisor logs
tail -f /var/log/storm/supervisor.log

# Check worker logs
tail -f /var/log/storm/workers-artifacts/topology-name/port/worker.log

# Common causes and solutions:
# - OutOfMemoryError: Increase worker heap size
# - Serialization issues: Check custom serializers
# - Resource exhaustion: Monitor CPU/memory usage
```

**2. Tuple Timeout Issues:**
```java
// Increase tuple timeout
Config conf = new Config();
conf.setMessageTimeoutSecs(60); // Increase from default 30s

// Reduce max spout pending
conf.setMaxSpoutPending(100); // Reduce backpressure
```

**3. Performance Bottlenecks:**
```bash
# Check topology metrics in Storm UI
# Look for:
# - High process latency in bolts
# - Low capacity utilization
# - Failed tuples

# Solutions:
# - Increase parallelism for bottleneck components
# - Optimize bolt processing logic
# - Use appropriate stream grouping
```

**4. Memory Leaks:**
```java
// Proper resource cleanup
public class ResourceManagedBolt extends BaseRichBolt {
    private Connection dbConnection;
    
    @Override
    public void cleanup() {
        try {
            if (dbConnection != null && !dbConnection.isClosed()) {
                dbConnection.close();
            }
        } catch (SQLException e) {
            // Log error
        }
    }
}
```

### Q17: How do you debug Storm topologies?
**Answer:**
**Storm Debugging Strategies:**

**1. Enable Debug Mode:**
```java
Config conf = new Config();
conf.setDebug(true); // Enable debug logging
```

**2. Local Mode Testing:**
```java
public class TopologyDebugger {
    public static void main(String[] args) throws Exception {
        TopologyBuilder builder = new TopologyBuilder();
        // Build topology...
        
        Config conf = new Config();
        conf.setDebug(true);
        conf.setMaxTaskParallelism(1); // Single thread for debugging
        
        LocalCluster cluster = new LocalCluster();
        cluster.submitTopology("debug-topology", conf, builder.createTopology());
        
        Utils.sleep(30000); // Run for 30 seconds
        cluster.killTopology("debug-topology");
        cluster.shutdown();
    }
}
```

**3. Custom Logging:**
```java
public class DebuggingBolt extends BaseRichBolt {
    private static final Logger LOG = LoggerFactory.getLogger(DebuggingBolt.class);
    
    @Override
    public void execute(Tuple tuple) {
        LOG.info("Processing tuple: {}", tuple);
        
        try {
            // Processing logic
            String result = processData(tuple.getString(0));
            LOG.debug("Processed result: {}", result);
            
            collector.emit(tuple, new Values(result));
            collector.ack(tuple);
            LOG.debug("Tuple acked successfully");
        } catch (Exception e) {
            LOG.error("Error processing tuple: {}", tuple, e);
            collector.fail(tuple);
        }
    }
}
```

**4. Metrics and Monitoring:**
```java
public class MonitoredBolt extends BaseRichBolt {
    private transient CountMetric processedCount;
    private transient CountMetric errorCount;
    
    @Override
    public void prepare(Map conf, TopologyContext context, OutputCollector collector) {
        this.processedCount = new CountMetric();
        this.errorCount = new CountMetric();
        
        context.registerMetric("processed-count", processedCount, 60);
        context.registerMetric("error-count", errorCount, 60);
    }
    
    @Override
    public void execute(Tuple tuple) {
        try {
            processData(tuple);
            processedCount.incr();
            collector.ack(tuple);
        } catch (Exception e) {
            errorCount.incr();
            collector.fail(tuple);
        }
    }
}
```

---

## 🌟 Real-world Scenarios

### Q18: Design a fraud detection system using Storm
**Answer:**
**Real-time Fraud Detection System:**

**1. System Architecture:**
```
Transaction Stream → Storm → Rule Engine → Alert System
                          ↓
                    Feature Store → ML Model → Risk Score
```

**2. Fraud Detection Topology:**
```java
public class FraudDetectionTopology {
    public static void main(String[] args) throws Exception {
        TopologyBuilder builder = new TopologyBuilder();
        
        // Transaction input stream
        builder.setSpout("transaction-spout", new KafkaTransactionSpout(), 4);
        
        // Feature extraction
        builder.setBolt("feature-bolt", new FeatureExtractionBolt(), 8)
               .fieldsGrouping("transaction-spout", new Fields("user_id"));
        
        // Rule-based detection
        builder.setBolt("rules-bolt", new RulesEngineBolt(), 6)
               .shuffleGrouping("feature-bolt");
        
        // ML-based scoring
        builder.setBolt("ml-scoring-bolt", new MLScoringBolt(), 4)
               .shuffleGrouping("feature-bolt");
        
        // Decision aggregation
        builder.setBolt("decision-bolt", new DecisionBolt(), 2)
               .fieldsGrouping("rules-bolt", new Fields("transaction_id"))
               .fieldsGrouping("ml-scoring-bolt", new Fields("transaction_id"));
        
        // Alert generation
        builder.setBolt("alert-bolt", new AlertBolt(), 3)
               .shuffleGrouping("decision-bolt");
        
        Config conf = new Config();
        conf.setNumWorkers(5);
        StormSubmitter.submitTopology("fraud-detection", conf, builder.createTopology());
    }
}
```

**3. Feature Extraction Bolt:**
```java
public class FeatureExtractionBolt extends BaseRichBolt {
    private Jedis redis; // For user history
    private OutputCollector collector;
    
    @Override
    public void execute(Tuple tuple) {
        Transaction txn = (Transaction) tuple.getValueByField("transaction");
        
        // Extract basic features
        Map<String, Object> features = new HashMap<>();
        features.put("amount", txn.getAmount());
        features.put("merchant_category", txn.getMerchantCategory());
        features.put("hour_of_day", getHourOfDay(txn.getTimestamp()));
        features.put("day_of_week", getDayOfWeek(txn.getTimestamp()));
        
        // Historical features
        String userId = txn.getUserId();
        UserProfile profile = getUserProfile(userId);
        
        features.put("avg_transaction_amount", profile.getAvgTransactionAmount());
        features.put("transaction_count_last_hour", getTransactionCountLastHour(userId));
        features.put("unique_merchants_last_day", getUniqueMerchantsLastDay(userId));
        features.put("distance_from_home", calculateDistanceFromHome(txn, profile));
        
        // Velocity features
        features.put("amount_last_10_minutes", getAmountLast10Minutes(userId));
        features.put("failed_attempts_last_hour", getFailedAttemptsLastHour(userId));
        
        // Update user profile
        updateUserProfile(userId, txn);
        
        collector.emit(tuple, new Values(txn.getId(), txn, features));
        collector.ack(tuple);
    }
    
    private double calculateDistanceFromHome(Transaction txn, UserProfile profile) {
        if (profile.getHomeLocation() == null) return 0.0;
        
        return haversineDistance(
            profile.getHomeLocation().getLat(), profile.getHomeLocation().getLon(),
            txn.getLocation().getLat(), txn.getLocation().getLon()
        );
    }
}
```

**4. Rules Engine Bolt:**
```java
public class RulesEngineBolt extends BaseRichBolt {
    private List<FraudRule> rules;
    
    @Override
    public void prepare(Map conf, TopologyContext context, OutputCollector collector) {
        this.rules = loadFraudRules();
    }
    
    @Override
    public void execute(Tuple tuple) {
        String transactionId = tuple.getStringByField("transaction_id");
        Transaction txn = (Transaction) tuple.getValueByField("transaction");
        Map<String, Object> features = (Map<String, Object>) tuple.getValueByField("features");
        
        RuleResult result = new RuleResult(transactionId);
        
        for (FraudRule rule : rules) {
            if (rule.evaluate(txn, features)) {
                result.addTriggeredRule(rule.getName(), rule.getRiskScore());
            }
        }
        
        collector.emit(tuple, new Values(transactionId, "rules", result));
        collector.ack(tuple);
    }
    
    private List<FraudRule> loadFraudRules() {
        return Arrays.asList(
            new AmountThresholdRule(10000, 0.8), // High amount transactions
            new VelocityRule(5, 3600, 0.7),      // 5+ transactions in 1 hour
            new LocationRule(1000, 0.6),         // 1000+ km from home
            new TimeRule(Arrays.asList(2, 3, 4), 0.5), // Late night transactions
            new MerchantCategoryRule(Arrays.asList("ATM", "CASH_ADVANCE"), 0.4)
        );
    }
}
```

**5. ML Scoring Bolt:**
```java
public class MLScoringBolt extends BaseRichBolt {
    private MLModel fraudModel;
    
    @Override
    public void prepare(Map conf, TopologyContext context, OutputCollector collector) {
        // Load pre-trained model
        this.fraudModel = loadModel("/models/fraud_detection_model.pkl");
    }
    
    @Override
    public void execute(Tuple tuple) {
        String transactionId = tuple.getStringByField("transaction_id");
        Map<String, Object> features = (Map<String, Object>) tuple.getValueByField("features");
        
        // Prepare feature vector
        double[] featureVector = prepareFeatureVector(features);
        
        // Get fraud probability from ML model
        double fraudProbability = fraudModel.predict(featureVector);
        
        MLResult result = new MLResult(transactionId, fraudProbability);
        
        collector.emit(tuple, new Values(transactionId, "ml", result));
        collector.ack(tuple);
    }
    
    private double[] prepareFeatureVector(Map<String, Object> features) {
        // Convert features to normalized vector for ML model
        return new double[] {
            normalize((Double) features.get("amount"), 0, 50000),
            (Integer) features.get("hour_of_day") / 24.0,
            (Integer) features.get("day_of_week") / 7.0,
            normalize((Double) features.get("distance_from_home"), 0, 10000),
            normalize((Integer) features.get("transaction_count_last_hour"), 0, 20)
        };
    }
}
```

### Q19: Implement a real-time recommendation system using Storm
**Answer:**
**Real-time Recommendation System:**

**1. System Architecture:**
```
User Events → Storm → Feature Store → ML Model → Recommendations → Cache
```

**2. Recommendation Topology:**
```java
public class RecommendationTopology {
    public static void main(String[] args) throws Exception {
        TopologyBuilder builder = new TopologyBuilder();
        
        // User activity stream
        builder.setSpout("activity-spout", new UserActivitySpout(), 4);
        
        // User profile updates
        builder.setBolt("profile-bolt", new UserProfileBolt(), 6)
               .fieldsGrouping("activity-spout", new Fields("user_id"));
        
        // Item similarity computation
        builder.setBolt("similarity-bolt", new ItemSimilarityBolt(), 4)
               .fieldsGrouping("activity-spout", new Fields("item_id"));
        
        // Real-time recommendations
        builder.setBolt("recommendation-bolt", new RecommendationBolt(), 8)
               .fieldsGrouping("profile-bolt", new Fields("user_id"))
               .allGrouping("similarity-bolt");
        
        // Cache updates
        builder.setBolt("cache-bolt", new CacheBolt(), 3)
               .shuffleGrouping("recommendation-bolt");
        
        Config conf = new Config();
        conf.setNumWorkers(4);
        StormSubmitter.submitTopology("recommendations", conf, builder.createTopology());
    }
}
```

**3. User Profile Bolt:**
```java
public class UserProfileBolt extends BaseRichBolt {
    private Map<String, UserProfile> userProfiles;
    private Jedis redis;
    
    @Override
    public void execute(Tuple tuple) {
        String userId = tuple.getStringByField("user_id");
        String itemId = tuple.getStringByField("item_id");
        String action = tuple.getStringByField("action");
        double rating = tuple.getDoubleByField("rating");
        
        UserProfile profile = userProfiles.computeIfAbsent(userId, k -> loadUserProfile(k));
        
        // Update user preferences
        if ("view".equals(action)) {
            profile.addView(itemId);
        } else if ("purchase".equals(action)) {
            profile.addPurchase(itemId, rating);
        } else if ("rating".equals(action)) {
            profile.updateRating(itemId, rating);
        }
        
        // Update category preferences
        String category = getItemCategory(itemId);
        profile.updateCategoryPreference(category, rating);
        
        // Persist updated profile
        saveUserProfile(userId, profile);
        
        collector.emit(tuple, new Values(userId, profile));
        collector.ack(tuple);
    }
    
    private UserProfile loadUserProfile(String userId) {
        String profileJson = redis.get("user_profile:" + userId);
        return profileJson != null ? 
            JsonUtils.fromJson(profileJson, UserProfile.class) : 
            new UserProfile(userId);
    }
}
```

**4. Recommendation Bolt:**
```java
public class RecommendationBolt extends BaseRichBolt {
    private RecommendationEngine engine;
    private Map<String, ItemSimilarity> itemSimilarities;
    
    @Override
    public void execute(Tuple tuple) {
        if (tuple.getSourceComponent().equals("profile-bolt")) {
            handleProfileUpdate(tuple);
        } else if (tuple.getSourceComponent().equals("similarity-bolt")) {
            handleSimilarityUpdate(tuple);
        }
    }
    
    private void handleProfileUpdate(Tuple tuple) {
        String userId = tuple.getStringByField("user_id");
        UserProfile profile = (UserProfile) tuple.getValueByField("profile");
        
        // Generate recommendations
        List<Recommendation> recommendations = generateRecommendations(profile);
        
        collector.emit(tuple, new Values(userId, recommendations));
        collector.ack(tuple);
    }
    
    private List<Recommendation> generateRecommendations(UserProfile profile) {
        List<Recommendation> recommendations = new ArrayList<>();
        
        // Collaborative filtering
        List<String> similarUsers = findSimilarUsers(profile);
        for (String similarUser : similarUsers) {
            UserProfile similarProfile = loadUserProfile(similarUser);
            recommendations.addAll(getRecommendationsFromSimilarUser(profile, similarProfile));
        }
        
        // Content-based filtering
        for (String category : profile.getPreferredCategories()) {
            List<String> categoryItems = getItemsByCategory(category);
            for (String itemId : categoryItems) {
                if (!profile.hasInteractedWith(itemId)) {
                    double score = calculateContentScore(profile, itemId);
                    recommendations.add(new Recommendation(itemId, score, "content"));
                }
            }
        }
        
        // Item-to-item collaborative filtering
        for (String itemId : profile.getPurchasedItems()) {
            ItemSimilarity similarity = itemSimilarities.get(itemId);
            if (similarity != null) {
                for (Map.Entry<String, Double> entry : similarity.getSimilarItems().entrySet()) {
                    String similarItem = entry.getKey();
                    double score = entry.getValue() * profile.getRating(itemId);
                    recommendations.add(new Recommendation(similarItem, score, "item-item"));
                }
            }
        }
        
        // Rank and filter recommendations
        return recommendations.stream()
            .collect(Collectors.groupingBy(Recommendation::getItemId,
                Collectors.summingDouble(Recommendation::getScore)))
            .entrySet().stream()
            .map(entry -> new Recommendation(entry.getKey(), entry.getValue(), "combined"))
            .sorted((r1, r2) -> Double.compare(r2.getScore(), r1.getScore()))
            .limit(20)
            .collect(Collectors.toList());
    }
}
```

---

## 📚 Additional Resources

### Best Practices Summary
1. **Topology Design**: Keep processing logic simple and stateless
2. **Parallelism**: Balance parallelism with resource constraints
3. **Fault Tolerance**: Always ack/fail tuples appropriately
4. **Monitoring**: Implement comprehensive metrics and alerting
5. **Testing**: Use local mode for development and testing

### Recommended Reading
- "Storm Applied" by Sean Allen, Matthew Jankowski, Peter Pathirana
- Apache Storm Official Documentation
- "Real-Time Analytics with Storm and Cassandra" by Shilpi Saxena

### Hands-on Practice
- Local Storm cluster setup
- Kafka-Storm integration
- Trident framework usage
- Performance tuning exercises

---

*This comprehensive guide covers essential Apache Storm concepts for real-time stream processing and data engineering roles. Practice with real streaming data and complex topologies to master Storm development.*