# Apache Kafka Best Practices for Data Engineering

## Topic Design and Configuration

### Topic Creation
```bash
# Create topic with appropriate partitions and replication
kafka-topics.sh --create \
  --topic user-events \
  --partitions 12 \
  --replication-factor 3 \
  --config retention.ms=604800000 \
  --config compression.type=snappy \
  --bootstrap-server localhost:9092
```

### Partition Strategy
```python
from kafka import KafkaProducer
import json

# Custom partitioner for even distribution
def custom_partitioner(key_bytes, all_partitions, available_partitions):
    if key_bytes is None:
        return random.choice(available_partitions)
    return hash(key_bytes) % len(all_partitions)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    partitioner=custom_partitioner,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Send with key for ordered processing
producer.send('user-events', 
              key=user_id.encode('utf-8'),
              value={'event': 'login', 'timestamp': time.time()})
```

## Producer Optimization

### Batch Configuration
```python
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    # Batching for throughput
    batch_size=16384,
    linger_ms=10,
    buffer_memory=33554432,
    
    # Compression
    compression_type='snappy',
    
    # Reliability
    acks='all',
    retries=3,
    max_in_flight_requests_per_connection=1,
    
    # Serialization
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
```

### Error Handling
```python
import logging
from kafka.errors import KafkaError

def send_with_callback(topic, key, value):
    try:
        future = producer.send(topic, key=key, value=value)
        record_metadata = future.get(timeout=10)
        logging.info(f"Message sent to {record_metadata.topic} "
                    f"partition {record_metadata.partition} "
                    f"offset {record_metadata.offset}")
    except KafkaError as e:
        logging.error(f"Failed to send message: {e}")
        # Implement retry logic or dead letter queue
```

## Consumer Optimization

### Consumer Configuration
```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'user-events',
    bootstrap_servers=['localhost:9092'],
    group_id='analytics-group',
    
    # Offset management
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    
    # Performance tuning
    fetch_min_bytes=1024,
    fetch_max_wait_ms=500,
    max_poll_records=500,
    
    # Deserialization
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)
```

### Manual Commit Strategy
```python
def process_messages():
    for message in consumer:
        try:
            # Process message
            process_event(message.value)
            
            # Commit offset after successful processing
            consumer.commit_async()
            
        except Exception as e:
            logging.error(f"Error processing message: {e}")
            # Handle error - retry, dead letter queue, etc.
            
        # Periodic synchronous commit for reliability
        if message.offset % 100 == 0:
            consumer.commit()
```

## Stream Processing with Kafka Streams

### Stream Processing Topology
```java
Properties props = new Properties();
props.put(StreamsConfig.APPLICATION_ID_CONFIG, "user-analytics");
props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");

StreamsBuilder builder = new StreamsBuilder();

// Input stream
KStream<String, UserEvent> events = builder.stream("user-events");

// Filtering and transformation
KStream<String, UserEvent> loginEvents = events
    .filter((key, event) -> "login".equals(event.getEventType()))
    .mapValues(event -> enrichEvent(event));

// Aggregation with windowing
KTable<Windowed<String>, Long> loginCounts = loginEvents
    .groupByKey()
    .windowedBy(TimeWindows.of(Duration.ofMinutes(5)))
    .count();

// Output to topic
loginCounts.toStream()
    .to("login-counts", Produced.with(WindowedSerdes.timeWindowedSerdeFrom(String.class), Serdes.Long()));

KafkaStreams streams = new KafkaStreams(builder.build(), props);
streams.start();
```

## Monitoring and Operations

### JMX Metrics
```python
# Monitor key metrics
import jmxquery

# Producer metrics
producer_metrics = [
    "kafka.producer:type=producer-metrics,client-id=*:record-send-rate",
    "kafka.producer:type=producer-metrics,client-id=*:batch-size-avg",
    "kafka.producer:type=producer-metrics,client-id=*:compression-rate-avg"
]

# Consumer metrics
consumer_metrics = [
    "kafka.consumer:type=consumer-fetch-manager-metrics,client-id=*:records-consumed-rate",
    "kafka.consumer:type=consumer-coordinator-metrics,client-id=*:commit-latency-avg",
    "kafka.consumer:type=consumer-fetch-manager-metrics,client-id=*:fetch-latency-avg"
]
```

### Health Checks
```python
from kafka.admin import KafkaAdminClient, ConfigResource, ConfigResourceType

def check_kafka_health():
    admin_client = KafkaAdminClient(
        bootstrap_servers=['localhost:9092']
    )
    
    try:
        # Check cluster metadata
        metadata = admin_client.describe_cluster()
        
        # Check topic configurations
        topics = admin_client.list_topics()
        
        # Check consumer group status
        groups = admin_client.describe_consumer_groups(['analytics-group'])
        
        return {
            'cluster_id': metadata.cluster_id,
            'topics_count': len(topics),
            'consumer_groups': len(groups)
        }
    except Exception as e:
        logging.error(f"Kafka health check failed: {e}")
        return None
```

## Security Configuration

### SSL/SASL Configuration
```python
# Producer with SSL and SASL
producer = KafkaProducer(
    bootstrap_servers=['localhost:9093'],
    security_protocol='SASL_SSL',
    sasl_mechanism='PLAIN',
    sasl_plain_username='user',
    sasl_plain_password='password',
    ssl_cafile='/path/to/ca-cert',
    ssl_certfile='/path/to/client-cert',
    ssl_keyfile='/path/to/client-key'
)

# Consumer with SSL and SASL
consumer = KafkaConsumer(
    'secure-topic',
    bootstrap_servers=['localhost:9093'],
    security_protocol='SASL_SSL',
    sasl_mechanism='PLAIN',
    sasl_plain_username='user',
    sasl_plain_password='password',
    ssl_cafile='/path/to/ca-cert'
)
```

### ACL Configuration
```bash
# Create ACLs for topic access
kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2181 \
  --add --allow-principal User:analytics-user \
  --operation Read --operation Write \
  --topic user-events

# Create ACLs for consumer group
kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2181 \
  --add --allow-principal User:analytics-user \
  --operation Read \
  --group analytics-group
```