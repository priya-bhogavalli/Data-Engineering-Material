# Apache Flume - Comprehensive Interview Questions & Answers

## 📋 Table of Contents
1. [Core Concepts](#-core-concepts)
2. [Architecture & Components](#-architecture--components)
3. [Sources, Channels & Sinks](#-sources-channels--sinks)
4. [Configuration & Deployment](#-configuration--deployment)
5. [Performance & Reliability](#-performance--reliability)
6. [Integration & Use Cases](#-integration--use-cases)
7. [Troubleshooting](#-troubleshooting)
8. [Real-world Scenarios](#-real-world-scenarios)

---

## 🎯 Core Concepts

### Q1: What is Apache Flume and what problems does it solve?
**Answer:**
Apache Flume is a distributed, reliable service for efficiently collecting, aggregating, and moving large amounts of log data from many sources to a centralized data store.

**Key Problems Solved:**
- **Log Collection**: Centralized collection from distributed sources
- **Data Reliability**: Guaranteed delivery with transaction support
- **Scalability**: Handle high-volume data streams
- **Real-time Processing**: Near real-time data ingestion
- **Fault Tolerance**: Automatic failover and recovery

**Core Features:**
- Event-driven architecture
- Configurable topology
- Multiple source and sink types
- Channel-based buffering
- Load balancing and failover

### Q2: Explain Flume's event-driven architecture
**Answer:**
**Flume Event Structure:**
```java
public interface Event {
    Map<String, String> getHeaders();
    void setHeaders(Map<String, String> headers);
    byte[] getBody();
    void setBody(byte[] body);
}
```

**Event Flow:**
```
Source → Channel → Sink
```

**Event Characteristics:**
- **Headers**: Key-value metadata pairs
- **Body**: Actual data payload (byte array)
- **Immutable**: Events cannot be modified once created
- **Transactional**: Atomic operations across components

**Example Event:**
```java
Event event = EventBuilder.withBody("log message".getBytes());
event.getHeaders().put("timestamp", String.valueOf(System.currentTimeMillis()));
event.getHeaders().put("host", "web-server-01");
event.getHeaders().put("service", "nginx");
```

### Q3: What are the key components of Flume architecture?
**Answer:**
**Flume Components:**

1. **Agent**: JVM process hosting Source, Channel, and Sink
2. **Source**: Collects data from external systems
3. **Channel**: Temporary storage between Source and Sink
4. **Sink**: Delivers data to destination systems
5. **Event**: Unit of data flow

**Component Relationships:**
```
External Data → Source → Channel → Sink → Destination
```

**Multi-tier Architecture:**
```
Tier 1: Web Servers → Flume Agents → Collector Agents
Tier 2: Collector Agents → Storage Agents → HDFS/HBase
```

---

## 🏗️ Architecture & Components

### Q4: Explain different types of Flume sources
**Answer:**
**Flume Source Types:**

**1. Spooling Directory Source:**
```properties
# Monitors directory for new files
agent.sources.r1.type = spooldir
agent.sources.r1.spoolDir = /var/log/flume-spooling
agent.sources.r1.channels = c1
agent.sources.r1.fileHeader = true
agent.sources.r1.deletePolicy = immediate
```

**2. Taildir Source:**
```properties
# Tails multiple files with position tracking
agent.sources.r1.type = TAILDIR
agent.sources.r1.positionFile = /var/log/flume/taildir_position.json
agent.sources.r1.filegroups = f1 f2
agent.sources.r1.filegroups.f1 = /var/log/app1/.*log.*
agent.sources.r1.filegroups.f2 = /var/log/app2/.*log.*
```

**3. Kafka Source:**
```properties
# Consumes from Kafka topics
agent.sources.r1.type = org.apache.flume.sink.solr.morphline.MorphlineHandlerImpl$Builder
agent.sources.r1.kafka.bootstrap.servers = localhost:9092
agent.sources.r1.kafka.topics = web-logs
agent.sources.r1.kafka.consumer.group.id = flume-consumer
```

**4. HTTP Source:**
```properties
# Receives HTTP POST requests
agent.sources.r1.type = http
agent.sources.r1.port = 8080
agent.sources.r1.handler = org.apache.flume.sink.solr.morphline.MorphlineHandlerImpl$Builder
```

**5. Netcat Source:**
```properties
# TCP socket listener
agent.sources.r1.type = netcat
agent.sources.r1.bind = localhost
agent.sources.r1.port = 44444
```

### Q5: Explain different types of Flume channels
**Answer:**
**Flume Channel Types:**

**1. Memory Channel:**
```properties
# Fast but non-persistent
agent.channels.c1.type = memory
agent.channels.c1.capacity = 10000
agent.channels.c1.transactionCapacity = 1000
agent.channels.c1.byteCapacityBufferPercentage = 20
agent.channels.c1.byteCapacity = 800000
```

**2. File Channel:**
```properties
# Persistent and reliable
agent.channels.c1.type = file
agent.channels.c1.checkpointDir = /var/flume/checkpoint
agent.channels.c1.dataDirs = /var/flume/data
agent.channels.c1.maxFileSize = 2146435071
agent.channels.c1.capacity = 1000000
agent.channels.c1.transactionCapacity = 10000
```

**3. Spillable Memory Channel:**
```properties
# Memory with disk overflow
agent.channels.c1.type = spillablememory
agent.channels.c1.memoryCapacity = 10000
agent.channels.c1.overflowCapacity = 1000000
agent.channels.c1.byteCapacity = 800000
agent.channels.c1.checkpointDir = /var/flume/checkpoint
agent.channels.c1.dataDirs = /var/flume/data
```

**4. Kafka Channel:**
```properties
# Kafka-based channel
agent.channels.c1.type = org.apache.flume.channel.kafka.KafkaChannel
agent.channels.c1.kafka.bootstrap.servers = localhost:9092
agent.channels.c1.kafka.topic = flume-channel
agent.channels.c1.kafka.consumer.group.id = flume-consumer
```

**Channel Comparison:**
| Channel | Durability | Performance | Use Case |
|---------|------------|-------------|----------|
| Memory | Low | High | High throughput, data loss acceptable |
| File | High | Medium | Reliable delivery required |
| Spillable Memory | Medium | High | Best of both worlds |
| Kafka | High | High | Integration with Kafka ecosystem |

### Q6: Explain different types of Flume sinks
**Answer:**
**Flume Sink Types:**

**1. HDFS Sink:**
```properties
# Write to HDFS
agent.sinks.k1.type = hdfs
agent.sinks.k1.hdfs.path = /flume/events/%Y/%m/%d/%H
agent.sinks.k1.hdfs.filePrefix = events-
agent.sinks.k1.hdfs.round = true
agent.sinks.k1.hdfs.roundValue = 10
agent.sinks.k1.hdfs.roundUnit = minute
agent.sinks.k1.hdfs.rollInterval = 600
agent.sinks.k1.hdfs.rollSize = 268435456
agent.sinks.k1.hdfs.rollCount = 0
agent.sinks.k1.hdfs.fileType = DataStream
```

**2. HBase Sink:**
```properties
# Write to HBase
agent.sinks.k1.type = hbase
agent.sinks.k1.table = flume_table
agent.sinks.k1.columnFamily = cf
agent.sinks.k1.serializer = org.apache.flume.sink.hbase.RegexHbaseEventSerializer
agent.sinks.k1.serializer.regex = ^([^,]*),([^,]*),(.*)$
agent.sinks.k1.serializer.colNames = col1,col2,col3
```

**3. Kafka Sink:**
```properties
# Write to Kafka
agent.sinks.k1.type = org.apache.flume.sink.kafka.KafkaSink
agent.sinks.k1.kafka.bootstrap.servers = localhost:9092
agent.sinks.k1.kafka.topic = flume-topic
agent.sinks.k1.kafka.flumeBatchSize = 20
agent.sinks.k1.kafka.producer.acks = 1
```

**4. Elasticsearch Sink:**
```properties
# Write to Elasticsearch
agent.sinks.k1.type = elasticsearch
agent.sinks.k1.hostNames = localhost:9200
agent.sinks.k1.indexName = flume
agent.sinks.k1.indexType = logs
agent.sinks.k1.batchSize = 500
agent.sinks.k1.ttl = 5d
```

**5. File Roll Sink:**
```properties
# Write to local files
agent.sinks.k1.type = file_roll
agent.sinks.k1.sink.directory = /var/log/flume-output
agent.sinks.k1.sink.rollInterval = 30
agent.sinks.k1.sink.batchSize = 100
```

---

## 📊 Sources, Channels & Sinks

### Q7: How do you configure a multi-tier Flume topology?
**Answer:**
**Multi-tier Flume Configuration:**

**Tier 1 - Web Server Agent:**
```properties
# Agent configuration
agent1.sources = r1
agent1.sinks = k1
agent1.channels = c1

# Source configuration (Taildir)
agent1.sources.r1.type = TAILDIR
agent1.sources.r1.positionFile = /var/log/flume/taildir_position.json
agent1.sources.r1.filegroups = f1
agent1.sources.r1.filegroups.f1 = /var/log/nginx/access.log
agent1.sources.r1.channels = c1

# Channel configuration (Memory)
agent1.channels.c1.type = memory
agent1.channels.c1.capacity = 10000
agent1.channels.c1.transactionCapacity = 1000

# Sink configuration (Avro to Tier 2)
agent1.sinks.k1.type = avro
agent1.sinks.k1.hostname = collector-server
agent1.sinks.k1.port = 4141
agent1.sinks.k1.channel = c1
```

**Tier 2 - Collector Agent:**
```properties
# Agent configuration
agent2.sources = r1
agent2.sinks = k1
agent2.channels = c1

# Source configuration (Avro from Tier 1)
agent2.sources.r1.type = avro
agent2.sources.r1.channels = c1
agent2.sources.r1.bind = 0.0.0.0
agent2.sources.r1.port = 4141

# Channel configuration (File for reliability)
agent2.channels.c1.type = file
agent2.channels.c1.checkpointDir = /var/flume/checkpoint
agent2.channels.c1.dataDirs = /var/flume/data

# Sink configuration (HDFS)
agent2.sinks.k1.type = hdfs
agent2.sinks.k1.hdfs.path = /data/logs/%Y/%m/%d
agent2.sinks.k1.hdfs.filePrefix = web-logs-
agent2.sinks.k1.hdfs.rollInterval = 600
agent2.sinks.k1.channel = c1
```

### Q8: How do you implement load balancing and failover in Flume?
**Answer:**
**Load Balancing Configuration:**

**1. Load Balancing Sink Processor:**
```properties
# Agent with multiple sinks
agent.sources = r1
agent.sinks = k1 k2 k3
agent.channels = c1

# Source configuration
agent.sources.r1.type = spooldir
agent.sources.r1.spoolDir = /var/log/flume-spooling
agent.sources.r1.channels = c1

# Channel configuration
agent.channels.c1.type = memory
agent.channels.c1.capacity = 10000
agent.channels.c1.transactionCapacity = 1000

# Multiple sinks
agent.sinks.k1.type = avro
agent.sinks.k1.hostname = server1
agent.sinks.k1.port = 4141
agent.sinks.k1.channel = c1

agent.sinks.k2.type = avro
agent.sinks.k2.hostname = server2
agent.sinks.k2.port = 4141
agent.sinks.k2.channel = c1

agent.sinks.k3.type = avro
agent.sinks.k3.hostname = server3
agent.sinks.k3.port = 4141
agent.sinks.k3.channel = c1

# Load balancing sink processor
agent.sinkgroups = g1
agent.sinkgroups.g1.sinks = k1 k2 k3
agent.sinkgroups.g1.processor.type = load_balance
agent.sinkgroups.g1.processor.backoff = true
agent.sinkgroups.g1.processor.selector = round_robin
```

**2. Failover Sink Processor:**
```properties
# Failover configuration
agent.sinkgroups.g1.processor.type = failover
agent.sinkgroups.g1.processor.priority.k1 = 5
agent.sinkgroups.g1.processor.priority.k2 = 10
agent.sinkgroups.g1.processor.priority.k3 = 15
agent.sinkgroups.g1.processor.maxpenalty = 10000
```

**3. Channel Selector for Load Distribution:**
```properties
# Replicating channel selector
agent.sources.r1.selector.type = replicating
agent.sources.r1.channels = c1 c2 c3

# Multiplexing channel selector
agent.sources.r1.selector.type = multiplexing
agent.sources.r1.selector.header = state
agent.sources.r1.selector.mapping.CA = c1
agent.sources.r1.selector.mapping.NY = c2
agent.sources.r1.selector.default = c3
```

### Q9: How do you handle data serialization in Flume?
**Answer:**
**Flume Serialization:**

**1. HDFS Serializers:**
```properties
# Text serializer (default)
agent.sinks.k1.hdfs.serializer = text
agent.sinks.k1.hdfs.serializer.appendNewline = true

# Avro Event serializer
agent.sinks.k1.hdfs.serializer = avro_event
agent.sinks.k1.hdfs.serializer.compressionCodec = snappy

# Custom serializer
agent.sinks.k1.hdfs.serializer = com.example.CustomEventSerializer$Builder
```

**2. HBase Serializers:**
```properties
# Simple HBase serializer
agent.sinks.k1.serializer = org.apache.flume.sink.hbase.SimpleHbaseEventSerializer

# Regex HBase serializer
agent.sinks.k1.serializer = org.apache.flume.sink.hbase.RegexHbaseEventSerializer
agent.sinks.k1.serializer.regex = ^([^,]*),([^,]*),(.*)$
agent.sinks.k1.serializer.colNames = col1,col2,col3
agent.sinks.k1.serializer.rowKeyIndex = 0
```

**3. Custom Serializer Implementation:**
```java
public class CustomEventSerializer implements EventSerializer {
    private OutputStream out;
    
    @Override
    public void write(Event event) throws IOException {
        // Custom serialization logic
        String timestamp = event.getHeaders().get("timestamp");
        String host = event.getHeaders().get("host");
        String body = new String(event.getBody());
        
        String serialized = String.format("%s|%s|%s%n", timestamp, host, body);
        out.write(serialized.getBytes());
    }
    
    @Override
    public void flush() throws IOException {
        out.flush();
    }
    
    @Override
    public void beforeClose() throws IOException {
        // Cleanup before closing
    }
    
    public static class Builder implements EventSerializer.Builder {
        @Override
        public EventSerializer build(Context context, OutputStream out) {
            return new CustomEventSerializer(out);
        }
    }
}
```

---

## ⚙️ Configuration & Deployment

### Q10: How do you configure Flume agents for production deployment?
**Answer:**
**Production Flume Configuration:**

**1. JVM Configuration:**
```bash
# flume-env.sh
export JAVA_OPTS="-Xms2g -Xmx4g -XX:+UseG1GC -XX:MaxGCPauseMillis=200"
export JAVA_OPTS="$JAVA_OPTS -XX:+PrintGCDetails -XX:+PrintGCTimeStamps"
export JAVA_OPTS="$JAVA_OPTS -Xloggc:/var/log/flume/gc.log"
export JAVA_OPTS="$JAVA_OPTS -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=5"
```

**2. Agent Configuration:**
```properties
# Production agent configuration
agent.sources = r1
agent.sinks = k1
agent.channels = c1

# Source with error handling
agent.sources.r1.type = TAILDIR
agent.sources.r1.positionFile = /var/flume/taildir_position.json
agent.sources.r1.filegroups = f1
agent.sources.r1.filegroups.f1 = /var/log/app/*.log
agent.sources.r1.channels = c1
agent.sources.r1.interceptors = i1 i2
agent.sources.r1.interceptors.i1.type = timestamp
agent.sources.r1.interceptors.i2.type = host

# Reliable file channel
agent.channels.c1.type = file
agent.channels.c1.checkpointDir = /var/flume/checkpoint
agent.channels.c1.dataDirs = /var/flume/data1,/var/flume/data2
agent.channels.c1.maxFileSize = 2146435071
agent.channels.c1.capacity = 1000000
agent.channels.c1.transactionCapacity = 10000
agent.channels.c1.checkpointInterval = 3000
agent.channels.c1.useDualCheckpoints = true

# HDFS sink with proper configuration
agent.sinks.k1.type = hdfs
agent.sinks.k1.hdfs.path = /data/logs/%Y/%m/%d/%H
agent.sinks.k1.hdfs.filePrefix = app-logs-
agent.sinks.k1.hdfs.fileSuffix = .log
agent.sinks.k1.hdfs.rollInterval = 300
agent.sinks.k1.hdfs.rollSize = 134217728
agent.sinks.k1.hdfs.rollCount = 0
agent.sinks.k1.hdfs.batchSize = 1000
agent.sinks.k1.hdfs.threadsPoolSize = 10
agent.sinks.k1.hdfs.callTimeout = 30000
agent.sinks.k1.channel = c1
```

**3. Monitoring Configuration:**
```properties
# JMX monitoring
agent.sources.r1.type = org.apache.flume.source.jms.JMSSource
flume.monitoring.type = http
flume.monitoring.port = 34545
```

**4. Security Configuration:**
```properties
# Kerberos authentication
flume.security.kerberos.enabled = true
flume.security.kerberos.principal = flume/_HOST@REALM.COM
flume.security.kerberos.keytab = /etc/security/keytabs/flume.keytab
```

### Q11: How do you implement custom interceptors in Flume?
**Answer:**
**Custom Interceptor Implementation:**

**1. Interceptor Interface:**
```java
public class CustomInterceptor implements Interceptor {
    private static final Logger logger = LoggerFactory.getLogger(CustomInterceptor.class);
    
    @Override
    public void initialize() {
        // Initialization logic
        logger.info("Custom interceptor initialized");
    }
    
    @Override
    public Event intercept(Event event) {
        // Process single event
        Map<String, String> headers = event.getHeaders();
        
        // Add custom headers
        headers.put("processed_time", String.valueOf(System.currentTimeMillis()));
        headers.put("interceptor", "custom");
        
        // Modify body if needed
        String body = new String(event.getBody());
        if (body.contains("ERROR")) {
            headers.put("log_level", "ERROR");
            headers.put("priority", "HIGH");
        } else if (body.contains("WARN")) {
            headers.put("log_level", "WARN");
            headers.put("priority", "MEDIUM");
        } else {
            headers.put("log_level", "INFO");
            headers.put("priority", "LOW");
        }
        
        return event;
    }
    
    @Override
    public List<Event> intercept(List<Event> events) {
        // Process batch of events
        List<Event> interceptedEvents = new ArrayList<>();
        for (Event event : events) {
            Event intercepted = intercept(event);
            if (intercepted != null) {
                interceptedEvents.add(intercepted);
            }
        }
        return interceptedEvents;
    }
    
    @Override
    public void close() {
        // Cleanup resources
        logger.info("Custom interceptor closed");
    }
    
    public static class Builder implements Interceptor.Builder {
        private String customProperty;
        
        @Override
        public Interceptor build() {
            return new CustomInterceptor(customProperty);
        }
        
        @Override
        public void configure(Context context) {
            customProperty = context.getString("custom.property", "default");
        }
    }
}
```

**2. Configuration:**
```properties
# Use custom interceptor
agent.sources.r1.interceptors = i1
agent.sources.r1.interceptors.i1.type = com.example.CustomInterceptor$Builder
agent.sources.r1.interceptors.i1.custom.property = production
```

**3. Data Filtering Interceptor:**
```java
public class FilteringInterceptor implements Interceptor {
    private Pattern filterPattern;
    
    public FilteringInterceptor(String regex) {
        this.filterPattern = Pattern.compile(regex);
    }
    
    @Override
    public Event intercept(Event event) {
        String body = new String(event.getBody());
        
        // Filter out events that don't match pattern
        if (!filterPattern.matcher(body).find()) {
            return null; // Drop event
        }
        
        return event;
    }
    
    public static class Builder implements Interceptor.Builder {
        private String filterRegex;
        
        @Override
        public void configure(Context context) {
            filterRegex = context.getString("filter.regex", ".*");
        }
        
        @Override
        public Interceptor build() {
            return new FilteringInterceptor(filterRegex);
        }
    }
}
```

---

## ⚡ Performance & Reliability

### Q12: How do you optimize Flume performance?
**Answer:**
**Flume Performance Optimization:**

**1. Channel Optimization:**
```properties
# Memory channel for high throughput
agent.channels.c1.type = memory
agent.channels.c1.capacity = 100000
agent.channels.c1.transactionCapacity = 10000
agent.channels.c1.byteCapacityBufferPercentage = 20

# File channel optimization
agent.channels.c1.type = file
agent.channels.c1.dataDirs = /data1/flume,/data2/flume,/data3/flume
agent.channels.c1.checkpointInterval = 3000
agent.channels.c1.useDualCheckpoints = true
agent.channels.c1.backupCheckpointDir = /backup/flume/checkpoint
```

**2. Sink Optimization:**
```properties
# HDFS sink optimization
agent.sinks.k1.hdfs.batchSize = 1000
agent.sinks.k1.hdfs.threadsPoolSize = 20
agent.sinks.k1.hdfs.callTimeout = 30000
agent.sinks.k1.hdfs.rollSize = 268435456  # 256MB
agent.sinks.k1.hdfs.rollInterval = 0      # Disable time-based rolling
agent.sinks.k1.hdfs.idleTimeout = 300     # Close idle files

# HBase sink optimization
agent.sinks.k1.batchSize = 1000
agent.sinks.k1.coalesceIncrements = true
agent.sinks.k1.serializer.payloadColumn = payload
```

**3. JVM Tuning:**
```bash
# JVM optimization
export JAVA_OPTS="-Xms4g -Xmx8g"
export JAVA_OPTS="$JAVA_OPTS -XX:+UseG1GC"
export JAVA_OPTS="$JAVA_OPTS -XX:MaxGCPauseMillis=200"
export JAVA_OPTS="$JAVA_OPTS -XX:G1HeapRegionSize=16m"
export JAVA_OPTS="$JAVA_OPTS -XX:+UnlockExperimentalVMOptions"
export JAVA_OPTS="$JAVA_OPTS -XX:+UseCGroupMemoryLimitForHeap"
```

**4. Monitoring and Metrics:**
```properties
# Enable JMX monitoring
flume.monitoring.type = http
flume.monitoring.port = 34545

# Custom metrics
agent.sources.r1.type = org.apache.flume.instrumentation.MonitoredCounterGroup
```

### Q13: How do you ensure data reliability in Flume?
**Answer:**
**Flume Reliability Mechanisms:**

**1. Transactional Guarantees:**
```java
// Flume transaction example
Channel channel = getChannel();
Transaction transaction = channel.getTransaction();
transaction.begin();

try {
    // Put events into channel
    for (Event event : events) {
        channel.put(event);
    }
    transaction.commit();
} catch (Exception e) {
    transaction.rollback();
    throw e;
} finally {
    transaction.close();
}
```

**2. Reliable Channel Configuration:**
```properties
# File channel for durability
agent.channels.c1.type = file
agent.channels.c1.checkpointDir = /var/flume/checkpoint
agent.channels.c1.dataDirs = /var/flume/data
agent.channels.c1.useDualCheckpoints = true
agent.channels.c1.backupCheckpointDir = /backup/flume/checkpoint

# Spillable memory channel for performance + reliability
agent.channels.c1.type = spillablememory
agent.channels.c1.memoryCapacity = 10000
agent.channels.c1.overflowCapacity = 1000000
agent.channels.c1.checkpointDir = /var/flume/checkpoint
```

**3. Failover Configuration:**
```properties
# Sink group with failover
agent.sinkgroups = g1
agent.sinkgroups.g1.sinks = k1 k2
agent.sinkgroups.g1.processor.type = failover
agent.sinkgroups.g1.processor.priority.k1 = 5
agent.sinkgroups.g1.processor.priority.k2 = 10
agent.sinkgroups.g1.processor.maxpenalty = 10000
```

**4. Data Validation:**
```java
public class ValidationInterceptor implements Interceptor {
    @Override
    public Event intercept(Event event) {
        // Validate event structure
        if (event.getBody() == null || event.getBody().length == 0) {
            logger.warn("Dropping empty event");
            return null;
        }
        
        // Validate required headers
        Map<String, String> headers = event.getHeaders();
        if (!headers.containsKey("timestamp")) {
            headers.put("timestamp", String.valueOf(System.currentTimeMillis()));
        }
        
        return event;
    }
}
```

---

## 🔗 Integration & Use Cases

### Q14: How do you integrate Flume with Kafka?
**Answer:**
**Flume-Kafka Integration:**

**1. Kafka Source Configuration:**
```properties
# Consume from Kafka
agent.sources.r1.type = org.apache.flume.sink.solr.morphline.MorphlineHandlerImpl$Builder
agent.sources.r1.kafka.bootstrap.servers = localhost:9092
agent.sources.r1.kafka.topics = web-logs,app-logs
agent.sources.r1.kafka.consumer.group.id = flume-consumer-group
agent.sources.r1.kafka.consumer.auto.offset.reset = earliest
agent.sources.r1.kafka.consumer.enable.auto.commit = false
agent.sources.r1.batchSize = 1000
agent.sources.r1.batchDurationMillis = 1000
```

**2. Kafka Sink Configuration:**
```properties
# Produce to Kafka
agent.sinks.k1.type = org.apache.flume.sink.kafka.KafkaSink
agent.sinks.k1.kafka.bootstrap.servers = localhost:9092
agent.sinks.k1.kafka.topic = processed-logs
agent.sinks.k1.kafka.flumeBatchSize = 20
agent.sinks.k1.kafka.producer.acks = 1
agent.sinks.k1.kafka.producer.linger.ms = 1
agent.sinks.k1.kafka.producer.compression.type = snappy
```

**3. Kafka Channel Configuration:**
```properties
# Use Kafka as channel
agent.channels.c1.type = org.apache.flume.channel.kafka.KafkaChannel
agent.channels.c1.kafka.bootstrap.servers = localhost:9092
agent.channels.c1.kafka.topic = flume-channel
agent.channels.c1.kafka.consumer.group.id = flume-consumer
agent.channels.c1.parseAsFlumeEvent = false
```

**4. Stream Processing Pipeline:**
```properties
# Complete Kafka integration pipeline
# Source: Kafka → Channel: Memory → Sink: HDFS

agent.sources = kafka-source
agent.channels = mem-channel
agent.sinks = hdfs-sink

# Kafka source
agent.sources.kafka-source.type = org.apache.flume.sink.solr.morphline.MorphlineHandlerImpl$Builder
agent.sources.kafka-source.kafka.bootstrap.servers = kafka1:9092,kafka2:9092
agent.sources.kafka-source.kafka.topics = raw-logs
agent.sources.kafka-source.channels = mem-channel

# Memory channel
agent.channels.mem-channel.type = memory
agent.channels.mem-channel.capacity = 10000
agent.channels.mem-channel.transactionCapacity = 1000

# HDFS sink
agent.sinks.hdfs-sink.type = hdfs
agent.sinks.hdfs-sink.hdfs.path = /processed-logs/%Y/%m/%d
agent.sinks.hdfs-sink.hdfs.filePrefix = kafka-logs-
agent.sinks.hdfs-sink.channel = mem-channel
```

### Q15: How do you implement real-time log processing with Flume?
**Answer:**
**Real-time Log Processing Architecture:**

**1. Multi-tier Processing:**
```
Log Files → Flume Tier 1 → Flume Tier 2 → Real-time Processing → Storage
```

**2. Tier 1 Configuration (Log Collection):**
```properties
# Web server log collection
web-agent.sources = taildir-source
web-agent.channels = memory-channel
web-agent.sinks = avro-sink

# Taildir source for real-time file tailing
web-agent.sources.taildir-source.type = TAILDIR
web-agent.sources.taildir-source.positionFile = /var/flume/taildir_position.json
web-agent.sources.taildir-source.filegroups = f1
web-agent.sources.taildir-source.filegroups.f1 = /var/log/nginx/access.log
web-agent.sources.taildir-source.channels = memory-channel

# Add interceptors for enrichment
web-agent.sources.taildir-source.interceptors = i1 i2 i3
web-agent.sources.taildir-source.interceptors.i1.type = timestamp
web-agent.sources.taildir-source.interceptors.i2.type = host
web-agent.sources.taildir-source.interceptors.i3.type = regex_filter
web-agent.sources.taildir-source.interceptors.i3.searchPattern = .*ERROR.*|.*WARN.*
web-agent.sources.taildir-source.interceptors.i3.excludeEvents = false

# Memory channel for speed
web-agent.channels.memory-channel.type = memory
web-agent.channels.memory-channel.capacity = 10000
web-agent.channels.memory-channel.transactionCapacity = 1000

# Avro sink to tier 2
web-agent.sinks.avro-sink.type = avro
web-agent.sinks.avro-sink.hostname = processing-server
web-agent.sinks.avro-sink.port = 4141
web-agent.sinks.avro-sink.channel = memory-channel
```

**3. Tier 2 Configuration (Processing & Routing):**
```properties
# Processing server configuration
processing-agent.sources = avro-source
processing-agent.channels = file-channel kafka-channel
processing-agent.sinks = hdfs-sink kafka-sink

# Avro source from tier 1
processing-agent.sources.avro-source.type = avro
processing-agent.sources.avro-source.bind = 0.0.0.0
processing-agent.sources.avro-source.port = 4141
processing-agent.sources.avro-source.channels = file-channel kafka-channel

# Channel selector for routing
processing-agent.sources.avro-source.selector.type = multiplexing
processing-agent.sources.avro-source.selector.header = log_level
processing-agent.sources.avro-source.selector.mapping.ERROR = kafka-channel
processing-agent.sources.avro-source.selector.mapping.WARN = kafka-channel
processing-agent.sources.avro-source.selector.default = file-channel

# File channel for batch processing
processing-agent.channels.file-channel.type = file
processing-agent.channels.file-channel.checkpointDir = /var/flume/checkpoint
processing-agent.channels.file-channel.dataDirs = /var/flume/data

# Kafka channel for real-time alerts
processing-agent.channels.kafka-channel.type = org.apache.flume.channel.kafka.KafkaChannel
processing-agent.channels.kafka-channel.kafka.bootstrap.servers = localhost:9092
processing-agent.channels.kafka-channel.kafka.topic = alerts

# HDFS sink for batch storage
processing-agent.sinks.hdfs-sink.type = hdfs
processing-agent.sinks.hdfs-sink.hdfs.path = /logs/%Y/%m/%d/%H
processing-agent.sinks.hdfs-sink.hdfs.filePrefix = web-logs-
processing-agent.sinks.hdfs-sink.channel = file-channel

# Kafka sink for real-time processing
processing-agent.sinks.kafka-sink.type = org.apache.flume.sink.kafka.KafkaSink
processing-agent.sinks.kafka-sink.kafka.bootstrap.servers = localhost:9092
processing-agent.sinks.kafka-sink.kafka.topic = real-time-logs
processing-agent.sinks.kafka-sink.channel = kafka-channel
```

**4. Custom Event Processing:**
```java
public class LogProcessingInterceptor implements Interceptor {
    private static final Pattern IP_PATTERN = Pattern.compile("\\b(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\b");
    private static final Pattern ERROR_PATTERN = Pattern.compile("ERROR|FATAL|Exception");
    
    @Override
    public Event intercept(Event event) {
        String body = new String(event.getBody());
        Map<String, String> headers = event.getHeaders();
        
        // Extract IP address
        Matcher ipMatcher = IP_PATTERN.matcher(body);
        if (ipMatcher.find()) {
            headers.put("client_ip", ipMatcher.group());
        }
        
        // Classify log level
        if (ERROR_PATTERN.matcher(body).find()) {
            headers.put("log_level", "ERROR");
            headers.put("priority", "HIGH");
        } else if (body.contains("WARN")) {
            headers.put("log_level", "WARN");
            headers.put("priority", "MEDIUM");
        } else {
            headers.put("log_level", "INFO");
            headers.put("priority", "LOW");
        }
        
        // Add processing timestamp
        headers.put("processed_at", String.valueOf(System.currentTimeMillis()));
        
        return event;
    }
}
```

---

## 🔧 Troubleshooting

### Q16: What are common Flume issues and how do you resolve them?
**Answer:**
**Common Flume Issues:**

**1. Channel Full Issues:**
```bash
# Symptoms: Events backing up, OutOfMemoryError
# Check channel capacity
grep "Channel full" /var/log/flume/flume.log

# Solutions:
# Increase channel capacity
agent.channels.c1.capacity = 100000
agent.channels.c1.transactionCapacity = 10000

# Use file channel for larger capacity
agent.channels.c1.type = file
agent.channels.c1.capacity = 1000000

# Add more sinks for parallel processing
agent.sinks = k1 k2 k3
agent.sinkgroups.g1.processor.type = load_balance
```

**2. Sink Performance Issues:**
```bash
# Monitor sink performance
tail -f /var/log/flume/flume.log | grep "Sink\|batch"

# HDFS sink optimization
agent.sinks.k1.hdfs.batchSize = 1000
agent.sinks.k1.hdfs.threadsPoolSize = 20
agent.sinks.k1.hdfs.callTimeout = 30000

# HBase sink optimization
agent.sinks.k1.batchSize = 1000
agent.sinks.k1.coalesceIncrements = true
```

**3. Memory Issues:**
```bash
# Check JVM memory usage
jstat -gc <flume-pid>

# Increase heap size
export JAVA_OPTS="-Xms2g -Xmx4g"

# Use G1GC for better performance
export JAVA_OPTS="$JAVA_OPTS -XX:+UseG1GC -XX:MaxGCPauseMillis=200"
```

**4. File Channel Corruption:**
```bash
# Check for corruption
grep "corruption\|checkpoint" /var/log/flume/flume.log

# Recovery steps

### Q17: How do you monitor Flume agents in production?
**Answer:**
**Flume Monitoring Strategies:**

**1. JMX Monitoring:**
```properties
# Enable JMX
flume.monitoring.type = http
flume.monitoring.port = 34545

# Key JMX metrics:
# - CHANNEL.channel.c1.ChannelSize
# - SINK.sink.k1.EventDrainAttemptCount
# - SOURCE.source.r1.EventReceivedCount
```

**2. Custom Monitoring Script:**
```bash
#!/bin/bash
# flume-monitor.sh

FLUME_JMX_URL="http://localhost:34545/metrics"
ALERT_THRESHOLD=1000

# Check channel size
CHANNEL_SIZE=$(curl -s $FLUME_JMX_URL | jq '.CHANNEL.channel.c1.ChannelSize')

if [ $CHANNEL_SIZE -gt $ALERT_THRESHOLD ]; then
    echo "ALERT: Channel size is $CHANNEL_SIZE (threshold: $ALERT_THRESHOLD)"
    # Send alert notification
fi

# Check sink drain rate
DRAIN_RATE=$(curl -s $FLUME_JMX_URL | jq '.SINK.sink.k1.EventDrainSuccessCount')
echo "Sink drain rate: $DRAIN_RATE events/sec"

# Check source receive rate
RECEIVE_RATE=$(curl -s $FLUME_JMX_URL | jq '.SOURCE.source.r1.EventReceivedCount')
echo "Source receive rate: $RECEIVE_RATE events/sec"
```

**3. Log-based Monitoring:**
```bash
# Monitor key log patterns
tail -f /var/log/flume/flume.log | grep -E "ERROR|WARN|Channel full|OutOfMemory"

# Create alerts for critical issues
grep -i "exception\|error\|failed" /var/log/flume/flume.log | tail -10
```

**4. Health Check Script:**
```bash
#!/bin/bash
# flume-health-check.sh

FLUME_PID=$(pgrep -f "flume")
if [ -z "$FLUME_PID" ]; then
    echo "CRITICAL: Flume process not running"
    exit 2
fi

# Check if agent is processing events
RECENT_EVENTS=$(grep "Event" /var/log/flume/flume.log | tail -1)
if [ -z "$RECENT_EVENTS" ]; then
    echo "WARNING: No recent event processing"
    exit 1
fi

# Check disk space for file channels
DISK_USAGE=$(df /var/flume/data | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 90 ]; then
    echo "CRITICAL: Disk usage is ${DISK_USAGE}%"
    exit 2
fi

echo "OK: Flume agent is healthy"
exit 0
```

---

## 🌟 Real-world Scenarios

### Q18: Design a log aggregation system for microservices using Flume
**Answer:**
**Microservices Log Aggregation Architecture:**

**1. System Architecture:**
```
Microservices → Flume Agents → Kafka → Flume Processors → Storage/Analytics
```

**2. Service-level Agent Configuration:**
```properties
# Microservice log agent (deployed with each service)
service-agent.sources = log-source
service-agent.channels = kafka-channel
service-agent.sinks = kafka-sink

# Taildir source for service logs
service-agent.sources.log-source.type = TAILDIR
service-agent.sources.log-source.positionFile = /var/flume/positions/service_position.json
service-agent.sources.log-source.filegroups = f1
service-agent.sources.log-source.filegroups.f1 = /var/log/service/*.log
service-agent.sources.log-source.channels = kafka-channel

# Add service metadata
service-agent.sources.log-source.interceptors = i1 i2 i3
service-agent.sources.log-source.interceptors.i1.type = static
service-agent.sources.log-source.interceptors.i1.key = service_name
service-agent.sources.log-source.interceptors.i1.value = ${SERVICE_NAME}

service-agent.sources.log-source.interceptors.i2.type = static
service-agent.sources.log-source.interceptors.i2.key = environment
service-agent.sources.log-source.interceptors.i2.value = ${ENVIRONMENT}

service-agent.sources.log-source.interceptors.i3.type = timestamp

# Kafka channel for reliability
service-agent.channels.kafka-channel.type = org.apache.flume.channel.kafka.KafkaChannel
service-agent.channels.kafka-channel.kafka.bootstrap.servers = kafka1:9092,kafka2:9092,kafka3:9092
service-agent.channels.kafka-channel.kafka.topic = service-logs
service-agent.channels.kafka-channel.kafka.consumer.group.id = flume-${SERVICE_NAME}

# Kafka sink (optional, if using channel)
service-agent.sinks.kafka-sink.type = org.apache.flume.sink.kafka.KafkaSink
service-agent.sinks.kafka-sink.kafka.bootstrap.servers = kafka1:9092,kafka2:9092,kafka3:9092
service-agent.sinks.kafka-sink.kafka.topic = service-logs
service-agent.sinks.kafka-sink.channel = kafka-channel
```

**3. Central Processing Agent:**
```properties
# Central log processing agent
central-agent.sources = kafka-source
central-agent.channels = processing-channel error-channel
central-agent.sinks = hdfs-sink elasticsearch-sink alert-sink

# Kafka source
central-agent.sources.kafka-source.type = org.apache.flume.sink.solr.morphline.MorphlineHandlerImpl$Builder
central-agent.sources.kafka-source.kafka.bootstrap.servers = kafka1:9092,kafka2:9092,kafka3:9092
central-agent.sources.kafka-source.kafka.topics = service-logs
central-agent.sources.kafka-source.kafka.consumer.group.id = central-processor
central-agent.sources.kafka-source.channels = processing-channel error-channel

# Channel selector for routing
central-agent.sources.kafka-source.selector.type = multiplexing
central-agent.sources.kafka-source.selector.header = log_level
central-agent.sources.kafka-source.selector.mapping.ERROR = error-channel
central-agent.sources.kafka-source.selector.mapping.FATAL = error-channel
central-agent.sources.kafka-source.selector.default = processing-channel

# Processing channel for normal logs
central-agent.channels.processing-channel.type = file
central-agent.channels.processing-channel.checkpointDir = /var/flume/checkpoint/processing
central-agent.channels.processing-channel.dataDirs = /var/flume/data/processing

# Error channel for alerts
central-agent.channels.error-channel.type = memory
central-agent.channels.error-channel.capacity = 10000
central-agent.channels.error-channel.transactionCapacity = 1000

# HDFS sink for long-term storage
central-agent.sinks.hdfs-sink.type = hdfs
central-agent.sinks.hdfs-sink.hdfs.path = /logs/%{service_name}/%Y/%m/%d
central-agent.sinks.hdfs-sink.hdfs.filePrefix = %{service_name}-
central-agent.sinks.hdfs-sink.hdfs.rollInterval = 300
central-agent.sinks.hdfs-sink.hdfs.rollSize = 134217728
central-agent.sinks.hdfs-sink.channel = processing-channel

# Elasticsearch sink for search
central-agent.sinks.elasticsearch-sink.type = elasticsearch
central-agent.sinks.elasticsearch-sink.hostNames = es1:9200,es2:9200,es3:9200
central-agent.sinks.elasticsearch-sink.indexName = service-logs-%Y.%m.%d
central-agent.sinks.elasticsearch-sink.indexType = log
central-agent.sinks.elasticsearch-sink.channel = processing-channel

# Alert sink for errors
central-agent.sinks.alert-sink.type = http
central-agent.sinks.alert-sink.endpoint = http://alert-manager:9093/api/v1/alerts
central-agent.sinks.alert-sink.channel = error-channel
```

**4. Log Processing Interceptor:**
```java
public class MicroserviceLogInterceptor implements Interceptor {
    private static final Pattern LOG_PATTERN = Pattern.compile(
        "^(\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}\\.\\d{3})\\s+(\\w+)\\s+\\[([^\\]]+)\\]\\s+(.+)$"
    );
    
    @Override
    public Event intercept(Event event) {
        String body = new String(event.getBody());
        Map<String, String> headers = event.getHeaders();
        
        // Parse log format
        Matcher matcher = LOG_PATTERN.matcher(body);
        if (matcher.matches()) {
            headers.put("log_timestamp", matcher.group(1));
            headers.put("log_level", matcher.group(2));
            headers.put("thread", matcher.group(3));
            headers.put("message", matcher.group(4));
        }
        
        // Extract request ID if present
        if (body.contains("requestId=")) {
            Pattern requestIdPattern = Pattern.compile("requestId=([a-zA-Z0-9-]+)");
            Matcher requestIdMatcher = requestIdPattern.matcher(body);
            if (requestIdMatcher.find()) {
                headers.put("request_id", requestIdMatcher.group(1));
            }
        }
        
        // Extract user ID if present
        if (body.contains("userId=")) {
            Pattern userIdPattern = Pattern.compile("userId=([a-zA-Z0-9-]+)");
            Matcher userIdMatcher = userIdPattern.matcher(body);
            if (userIdMatcher.find()) {
                headers.put("user_id", userIdMatcher.group(1));
            }
        }
        
        // Add correlation ID for distributed tracing
        if (!headers.containsKey("correlation_id")) {
            headers.put("correlation_id", UUID.randomUUID().toString());
        }
        
        return event;
    }
}
```

### Q19: Implement a real-time fraud detection system using Flume
**Answer:**
**Real-time Fraud Detection System:**

**1. System Architecture:**
```
Transaction Sources → Flume → Real-time Processing → Alert System
                            ↓
                        Historical Storage
```

**2. Transaction Ingestion Configuration:**
```properties
# Transaction ingestion agent
fraud-agent.sources = transaction-source
fraud-agent.channels = realtime-channel batch-channel
fraud-agent.sinks = kafka-sink hdfs-sink

# HTTP source for transaction data
fraud-agent.sources.transaction-source.type = http
fraud-agent.sources.transaction-source.port = 8080
fraud-agent.sources.transaction-source.handler = org.apache.flume.sink.solr.morphline.MorphlineHandlerImpl$Builder
fraud-agent.sources.transaction-source.channels = realtime-channel batch-channel

# Add fraud detection interceptors
fraud-agent.sources.transaction-source.interceptors = i1 i2 i3
fraud-agent.sources.transaction-source.interceptors.i1.type = com.example.TransactionValidationInterceptor$Builder
fraud-agent.sources.transaction-source.interceptors.i2.type = com.example.FraudScoringInterceptor$Builder
fraud-agent.sources.transaction-source.interceptors.i3.type = com.example.RiskClassificationInterceptor$Builder

# Channel selector for routing
fraud-agent.sources.transaction-source.selector.type = multiplexing
fraud-agent.sources.transaction-source.selector.header = risk_level
fraud-agent.sources.transaction-source.selector.mapping.HIGH = realtime-channel
fraud-agent.sources.transaction-source.selector.mapping.MEDIUM = realtime-channel
fraud-agent.sources.transaction-source.selector.default = batch-channel

# Real-time channel for suspicious transactions
fraud-agent.channels.realtime-channel.type = memory
fraud-agent.channels.realtime-channel.capacity = 10000
fraud-agent.channels.realtime-channel.transactionCapacity = 1000

# Batch channel for normal transactions
fraud-agent.channels.batch-channel.type = file
fraud-agent.channels.batch-channel.checkpointDir = /var/flume/checkpoint/batch
fraud-agent.channels.batch-channel.dataDirs = /var/flume/data/batch

# Kafka sink for real-time processing
fraud-agent.sinks.kafka-sink.type = org.apache.flume.sink.kafka.KafkaSink
fraud-agent.sinks.kafka-sink.kafka.bootstrap.servers = kafka1:9092,kafka2:9092
fraud-agent.sinks.kafka-sink.kafka.topic = suspicious-transactions
fraud-agent.sinks.kafka-sink.channel = realtime-channel

# HDFS sink for batch processing
fraud-agent.sinks.hdfs-sink.type = hdfs
fraud-agent.sinks.hdfs-sink.hdfs.path = /transactions/%Y/%m/%d
fraud-agent.sinks.hdfs-sink.hdfs.filePrefix = transactions-
fraud-agent.sinks.hdfs-sink.channel = batch-channel
```

**3. Fraud Detection Interceptors:**
```java
public class FraudScoringInterceptor implements Interceptor {
    private static final Map<String, Double> COUNTRY_RISK_SCORES = new HashMap<>();
    static {
        COUNTRY_RISK_SCORES.put("US", 0.1);
        COUNTRY_RISK_SCORES.put("CA", 0.1);
        COUNTRY_RISK_SCORES.put("GB", 0.2);
        // Add more countries...
    }
    
    @Override
    public Event intercept(Event event) {
        try {
            String body = new String(event.getBody());
            JSONObject transaction = new JSONObject(body);
            Map<String, String> headers = event.getHeaders();
            
            double fraudScore = calculateFraudScore(transaction);
            headers.put("fraud_score", String.valueOf(fraudScore));
            
            // Classify risk level
            if (fraudScore > 0.8) {
                headers.put("risk_level", "HIGH");
            } else if (fraudScore > 0.5) {
                headers.put("risk_level", "MEDIUM");
            } else {
                headers.put("risk_level", "LOW");
            }
            
            return event;
        } catch (Exception e) {
            logger.error("Error processing transaction", e);
            return null;
        }
    }
    
    private double calculateFraudScore(JSONObject transaction) {
        double score = 0.0;
        
        // Amount-based scoring
        double amount = transaction.getDouble("amount");
        if (amount > 10000) score += 0.3;
        else if (amount > 5000) score += 0.2;
        else if (amount > 1000) score += 0.1;
        
        // Time-based scoring (unusual hours)
        int hour = getHourFromTimestamp(transaction.getString("timestamp"));
        if (hour < 6 || hour > 22) score += 0.2;
        
        // Location-based scoring
        String country = transaction.getString("country");
        score += COUNTRY_RISK_SCORES.getOrDefault(country, 0.5);
        
        // Velocity scoring (requires external cache/database)
        String userId = transaction.getString("user_id");
        int recentTransactionCount = getRecentTransactionCount(userId);
        if (recentTransactionCount > 10) score += 0.4;
        else if (recentTransactionCount > 5) score += 0.2;
        
        return Math.min(score, 1.0);
    }
}

public class RiskClassificationInterceptor implements Interceptor {
    @Override
    public Event intercept(Event event) {
        Map<String, String> headers = event.getHeaders();
        double fraudScore = Double.parseDouble(headers.get("fraud_score"));
        
        // Add additional risk indicators
        String body = new String(event.getBody());
        JSONObject transaction = new JSONObject(body);
        
        // Check for suspicious patterns
        if (isSuspiciousPattern(transaction)) {
            headers.put("suspicious_pattern", "true");
            headers.put("risk_level", "HIGH");
        }
        
        // Check blacklisted entities
        if (isBlacklisted(transaction)) {
            headers.put("blacklisted", "true");
            headers.put("risk_level", "HIGH");
        }
        
        // Add alert priority
        String riskLevel = headers.get("risk_level");
        if ("HIGH".equals(riskLevel)) {
            headers.put("alert_priority", "IMMEDIATE");
        } else if ("MEDIUM".equals(riskLevel)) {
            headers.put("alert_priority", "NORMAL");
        }
        
        return event;
    }
    
    private boolean isSuspiciousPattern(JSONObject transaction) {
        // Implement pattern detection logic
        // e.g., round amounts, specific merchant categories, etc.
        double amount = transaction.getDouble("amount");
        return amount % 100 == 0 && amount > 1000; // Round amounts over $1000
    }
    
    private boolean isBlacklisted(JSONObject transaction) {
        // Check against blacklist (external service/cache)
        String merchantId = transaction.getString("merchant_id");
        String cardNumber = transaction.getString("card_number");
        
        // Implement blacklist checking logic
        return false; // Placeholder
    }
}
```

**4. Alert Processing Configuration:**
```properties
# Alert processing agent
alert-agent.sources = kafka-source
alert-agent.channels = alert-channel
alert-agent.sinks = notification-sink investigation-sink

# Kafka source for suspicious transactions
alert-agent.sources.kafka-source.type = org.apache.flume.sink.solr.morphline.MorphlineHandlerImpl$Builder
alert-agent.sources.kafka-source.kafka.bootstrap.servers = kafka1:9092,kafka2:9092
alert-agent.sources.kafka-source.kafka.topics = suspicious-transactions
alert-agent.sources.kafka-source.kafka.consumer.group.id = fraud-alerts
alert-agent.sources.kafka-source.channels = alert-channel

# Memory channel for fast alert processing
alert-agent.channels.alert-channel.type = memory
alert-agent.channels.alert-channel.capacity = 10000
alert-agent.channels.alert-channel.transactionCapacity = 1000

# HTTP sink for immediate notifications
alert-agent.sinks.notification-sink.type = http
alert-agent.sinks.notification-sink.endpoint = http://alert-service:8080/alerts
alert-agent.sinks.notification-sink.channel = alert-channel

# Database sink for investigation queue
alert-agent.sinks.investigation-sink.type = jdbc
alert-agent.sinks.investigation-sink.driver = com.mysql.jdbc.Driver
alert-agent.sinks.investigation-sink.connectionString = jdbc:mysql://db:3306/fraud_db
alert-agent.sinks.investigation-sink.table = investigation_queue
alert-agent.sinks.investigation-sink.channel = alert-channel
```

---

## 📚 Additional Resources

### Best Practices Summary
1. **Reliability**: Use file channels for critical data paths
2. **Performance**: Optimize batch sizes and channel capacities
3. **Monitoring**: Implement comprehensive JMX and log monitoring
4. **Security**: Use proper authentication and encryption
5. **Scalability**: Design multi-tier architectures for large deployments

### Recommended Reading
- "Apache Flume: Distributed Log Collection for Hadoop" by Steve Hoffman
- Apache Flume Official Documentation
- "Hadoop: The Definitive Guide" - Flume chapter

### Hands-on Practice
- Local Flume cluster setup
- Kafka integration examples
- Custom interceptor development
- Real-time log processing pipelines

---

*This comprehensive guide covers essential Apache Flume concepts for data ingestion and streaming data engineering roles. Practice with real log data and complex topologies to master Flume operations.*