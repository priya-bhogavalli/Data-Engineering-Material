# Apache Kafka Key Concepts

## 1. Kafka Fundamentals
**What is Kafka**: A distributed streaming platform that provides high-throughput, low-latency platform for handling real-time data feeds.

**Core Capabilities**:
- **Publish-Subscribe**: Messaging system for real-time data streams
- **Storage**: Distributed, fault-tolerant storage of streams
- **Processing**: Real-time stream processing with Kafka Streams

**Key Components**:
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Producers  │───▶│   Brokers   │───▶│  Consumers  │
│             │    │  (Topics)   │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
                          │
                   ┌─────────────┐
                   │  ZooKeeper  │
                   │ (Metadata)  │
                   └─────────────┘
```

## 2. Topics and Partitions
**Topics**: Named streams of records, similar to database tables or folders.

**Partitions**: Topics are split into partitions for scalability and parallelism.

```bash
# Create topic with multiple partitions
kafka-topics.sh --create \
    --topic user-events \
    --partitions 6 \
    --replication-factor 3 \
    --bootstrap-server localhost:9092
```

**Partition Strategy**:
```python
# Producer with custom partitioner
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    # Partition by user_id for ordered processing per user
    partitioner=lambda key, all_partitions, available: hash(key) % len(all_partitions)
)

# Send message with key for partitioning
producer.send('user-events', 
              key=b'user123', 
              value={'user_id': 'user123', 'action': 'login', 'timestamp': '2024-01-15T10:00:00Z'})
```

**Partition Layout**:
```
Topic: user-events (6 partitions, replication factor 3)

Partition 0: [msg1] [msg4] [msg7] ...
Partition 1: [msg2] [msg5] [msg8] ...
Partition 2: [msg3] [msg6] [msg9] ...
Partition 3: [msg10] [msg13] ...
Partition 4: [msg11] [msg14] ...
Partition 5: [msg12] [msg15] ...

Each partition replicated across 3 brokers
```

## 3. Producers
**What they are**: Applications that publish records to Kafka topics.

**Producer Configuration**:
```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['broker1:9092', 'broker2:9092', 'broker3:9092'],
    
    # Serialization
    key_serializer=lambda k: k.encode('utf-8'),
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    
    # Reliability settings
    acks='all',                    # Wait for all replicas to acknowledge
    retries=3,                     # Retry failed sends
    retry_backoff_ms=1000,         # Wait between retries
    
    # Performance settings
    batch_size=16384,              # Batch size in bytes
    linger_ms=10,                  # Wait time to batch messages
    buffer_memory=33554432,        # Total memory for buffering
    
    # Compression
    compression_type='gzip'        # Compress messages
)
```

**Sending Messages**:
```python
# Synchronous send
try:
    future = producer.send('user-events', 
                          key='user123',
                          value={'action': 'purchase', 'amount': 99.99})
    record_metadata = future.get(timeout=10)
    print(f"Message sent to {record_metadata.topic} partition {record_metadata.partition}")
except Exception as e:
    print(f"Failed to send message: {e}")

# Asynchronous send with callback
def on_send_success(record_metadata):
    print(f"Message sent to {record_metadata.topic}:{record_metadata.partition}:{record_metadata.offset}")

def on_send_error(excp):
    print(f"Failed to send message: {excp}")

producer.send('user-events', value={'action': 'view'}).add_callback(on_send_success).add_errback(on_send_error)

# Flush and close
producer.flush()  # Ensure all messages are sent
producer.close()
```

**Idempotent Producer**:
```python
# Exactly-once semantics
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    enable_idempotence=True,       # Prevent duplicate messages
    acks='all',
    retries=2147483647,            # Max retries
    max_in_flight_requests_per_connection=5
)
```

## 4. Consumers and Consumer Groups
**What they are**: Applications that read records from Kafka topics.

**Consumer Configuration**:
```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'user-events',
    bootstrap_servers=['localhost:9092'],
    
    # Consumer group
    group_id='analytics-group',
    
    # Deserialization
    key_deserializer=lambda k: k.decode('utf-8') if k else None,
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    
    # Offset management
    auto_offset_reset='earliest',   # Start from beginning if no offset
    enable_auto_commit=True,        # Automatically commit offsets
    auto_commit_interval_ms=5000,   # Commit interval
    
    # Performance
    fetch_min_bytes=1024,          # Minimum bytes to fetch
    fetch_max_wait_ms=500,         # Maximum wait time
    max_poll_records=500           # Maximum records per poll
)
```

**Consuming Messages**:
```python
# Simple consumption
for message in consumer:
    print(f"Topic: {message.topic}")
    print(f"Partition: {message.partition}")
    print(f"Offset: {message.offset}")
    print(f"Key: {message.key}")
    print(f"Value: {message.value}")
    print(f"Timestamp: {message.timestamp}")

# Manual offset management
consumer = KafkaConsumer(
    'user-events',
    group_id='manual-commit-group',
    enable_auto_commit=False
)

for message in consumer:
    try:
        # Process message
        process_user_event(message.value)
        
        # Manually commit offset
        consumer.commit()
    except Exception as e:
        print(f"Error processing message: {e}")
        # Don't commit on error - message will be reprocessed
```

**Consumer Groups**:
```python
# Multiple consumers in same group share partitions
# Consumer 1
consumer1 = KafkaConsumer('user-events', group_id='processing-group')

# Consumer 2 (same group)
consumer2 = KafkaConsumer('user-events', group_id='processing-group')

# Partition assignment example:
# Topic: user-events (6 partitions)
# Consumer 1: partitions 0, 1, 2
# Consumer 2: partitions 3, 4, 5
```

## 5. Brokers and Clusters
**Brokers**: Kafka servers that store and serve data.

**Cluster Configuration**:
```properties
# server.properties
broker.id=1
listeners=PLAINTEXT://broker1:9092
log.dirs=/var/kafka-logs

# Replication
default.replication.factor=3
min.insync.replicas=2

# Log retention
log.retention.hours=168        # 7 days
log.retention.bytes=1073741824 # 1GB per partition
log.segment.bytes=1073741824   # 1GB segments

# Performance
num.network.threads=8
num.io.threads=8
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
```

**Replication**:
```
Topic: orders (replication factor 3)

Partition 0:
├── Leader: Broker 1
├── Replica: Broker 2
└── Replica: Broker 3

Partition 1:
├── Leader: Broker 2
├── Replica: Broker 1
└── Replica: Broker 3

Partition 2:
├── Leader: Broker 3
├── Replica: Broker 1
└── Replica: Broker 2
```

## 6. Kafka Streams
**What it is**: Java library for building real-time streaming applications.

**Stream Processing Topology**:
```java
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.KTable;

StreamsBuilder builder = new StreamsBuilder();

// Source stream
KStream<String, String> userEvents = builder.stream("user-events");

// Transform stream
KStream<String, String> processedEvents = userEvents
    .filter((key, value) -> value.contains("purchase"))
    .mapValues(value -> value.toUpperCase())
    .selectKey((key, value) -> extractUserId(value));

// Aggregate to table
KTable<String, Long> userPurchaseCounts = processedEvents
    .groupByKey()
    .count();

// Output to topic
userPurchaseCounts.toStream().to("user-purchase-counts");

// Start application
KafkaStreams streams = new KafkaStreams(builder.build(), props);
streams.start();
```

**Windowing Operations**:
```java
// Time-based windowing
KTable<Windowed<String>, Long> windowedCounts = userEvents
    .groupByKey()
    .windowedBy(TimeWindows.of(Duration.ofMinutes(5)))
    .count();

// Session windowing
KTable<Windowed<String>, Long> sessionCounts = userEvents
    .groupByKey()
    .windowedBy(SessionWindows.with(Duration.ofMinutes(30)))
    .count();
```

**Stream-Table Joins**:
```java
// Stream-table join
KStream<String, String> enrichedEvents = userEvents
    .leftJoin(userProfiles, 
              (event, profile) -> enrichEvent(event, profile));

// Stream-stream join
KStream<String, String> correlatedEvents = clickStream
    .join(impressionStream,
          (click, impression) -> correlateEvents(click, impression),
          JoinWindows.of(Duration.ofMinutes(5)));
```

## 7. Schema Registry
**What it is**: Centralized schema management for Kafka messages.

**Avro Schema Example**:
```json
{
  "type": "record",
  "name": "UserEvent",
  "namespace": "com.company.events",
  "fields": [
    {"name": "user_id", "type": "string"},
    {"name": "event_type", "type": "string"},
    {"name": "timestamp", "type": "long"},
    {"name": "properties", "type": {"type": "map", "values": "string"}}
  ]
}
```

**Producer with Schema Registry**:
```python
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

# Schema Registry configuration
schema_registry_conf = {'url': 'http://localhost:8081'}

# Producer configuration
producer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'schema.registry.url': 'http://localhost:8081'
}

# Create producer
producer = AvroProducer(producer_conf, default_key_schema=key_schema, default_value_schema=value_schema)

# Send message
producer.produce(topic='user-events', 
                key={'user_id': 'user123'},
                value={'user_id': 'user123', 'event_type': 'login', 'timestamp': 1642248000000})
```

## 8. Kafka Connect
**What it is**: Framework for connecting Kafka with external systems.

**Source Connector (Database to Kafka)**:
```json
{
  "name": "mysql-source-connector",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
    "connection.url": "jdbc:mysql://localhost:3306/mydb",
    "connection.user": "kafka",
    "connection.password": "password",
    "table.whitelist": "users,orders",
    "mode": "incrementing",
    "incrementing.column.name": "id",
    "topic.prefix": "mysql-",
    "poll.interval.ms": 1000
  }
}
```

**Sink Connector (Kafka to S3)**:
```json
{
  "name": "s3-sink-connector",
  "config": {
    "connector.class": "io.confluent.connect.s3.S3SinkConnector",
    "topics": "user-events,order-events",
    "s3.bucket.name": "my-kafka-bucket",
    "s3.region": "us-west-2",
    "flush.size": "1000",
    "rotate.interval.ms": "60000",
    "format.class": "io.confluent.connect.s3.format.json.JsonFormat",
    "partitioner.class": "io.confluent.connect.storage.partitioner.TimeBasedPartitioner",
    "path.format": "year=YYYY/month=MM/day=dd/hour=HH"
  }
}
```

## 9. Monitoring and Operations
**Key Metrics**:
```bash
# Broker metrics
kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec
kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec
kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec

# Consumer lag
kafka.consumer:type=consumer-fetch-manager-metrics,client-id=*

# Producer metrics
kafka.producer:type=producer-metrics,client-id=*
```

**Monitoring Commands**:
```bash
# List topics
kafka-topics.sh --list --bootstrap-server localhost:9092

# Describe topic
kafka-topics.sh --describe --topic user-events --bootstrap-server localhost:9092

# Consumer group status
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group analytics-group --describe

# Check consumer lag
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group analytics-group --describe | grep LAG
```

**JMX Monitoring**:
```java
// Enable JMX in Kafka
export KAFKA_JMX_OPTS="-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.port=9999"
```

## 10. Performance Tuning
**Producer Optimization**:
```python
producer = KafkaProducer(
    # Throughput optimization
    batch_size=65536,              # Larger batches
    linger_ms=20,                  # Wait longer to batch
    compression_type='lz4',        # Fast compression
    
    # Reliability vs performance
    acks=1,                        # Leader acknowledgment only
    retries=0,                     # No retries for max throughput
    
    # Memory management
    buffer_memory=67108864,        # 64MB buffer
    max_block_ms=60000            # Block time for buffer full
)
```

**Consumer Optimization**:
```python
consumer = KafkaConsumer(
    # Fetch optimization
    fetch_min_bytes=50000,         # Larger minimum fetch
    fetch_max_wait_ms=100,         # Shorter wait time
    max_poll_records=1000,         # More records per poll
    
    # Processing optimization
    max_poll_interval_ms=600000,   # 10 minutes max processing time
    session_timeout_ms=30000,      # 30 second session timeout
    heartbeat_interval_ms=10000    # 10 second heartbeat
)
```

**Broker Tuning**:
```properties
# Network
num.network.threads=16
num.io.threads=16
socket.send.buffer.bytes=1048576
socket.receive.buffer.bytes=1048576

# Log
log.flush.interval.messages=10000
log.flush.interval.ms=1000
num.recovery.threads.per.data.dir=2

# Replication
replica.fetch.max.bytes=1048576
replica.socket.timeout.ms=30000
```