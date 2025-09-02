# Apache Kafka Complete Guide for Data Engineering

## 🎯 What is Apache Kafka?

Apache Kafka is a **distributed streaming platform** designed for building real-time data pipelines and streaming applications. It's the backbone of modern data architectures, enabling high-throughput, fault-tolerant, and scalable data streaming.

### Key Characteristics
- **Distributed**: Scales horizontally across multiple servers
- **Fault-Tolerant**: Replicates data across multiple brokers
- **High-Throughput**: Handles millions of messages per second
- **Low-Latency**: Sub-millisecond message delivery
- **Persistent**: Stores streams of records durably

## 💾 Core Concepts

### 1. Kafka Architecture
```
┌─────────────────────────────────────────────────────────┐
│                    Kafka Cluster                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│  │  Broker 1   │ │  Broker 2   │ │  Broker 3   │       │
│  │             │ │             │ │             │       │
│  │ Topic A     │ │ Topic A     │ │ Topic B     │       │
│  │ Partition 0 │ │ Partition 1 │ │ Partition 0 │       │
│  └─────────────┘ └─────────────┘ └─────────────┘       │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                    ZooKeeper                            │
│           (Cluster Coordination)                        │
└─────────────────────────────────────────────────────────┘
```

### 2. Key Components
```bash
# Topics and Partitions
kafka-topics.sh --create \
  --topic user-events \
  --partitions 3 \
  --replication-factor 2 \
  --bootstrap-server localhost:9092

# List topics
kafka-topics.sh --list --bootstrap-server localhost:9092

# Describe topic
kafka-topics.sh --describe \
  --topic user-events \
  --bootstrap-server localhost:9092
```

### 3. Producers and Consumers
```python
# Producer example
from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: k.encode('utf-8') if k else None,
    acks='all',  # Wait for all replicas
    retries=3,
    batch_size=16384,
    linger_ms=10
)

# Send messages
for i in range(100):
    message = {
        'user_id': f'user_{i}',
        'event_type': 'page_view',
        'timestamp': int(time.time()),
        'page': f'/page_{i % 10}'
    }
    
    producer.send(
        topic='user-events',
        key=f'user_{i}',
        value=message
    )

producer.flush()
producer.close()

# Consumer example
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'user-events',
    bootstrap_servers=['localhost:9092'],
    group_id='analytics-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    key_deserializer=lambda k: k.decode('utf-8') if k else None,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    auto_commit_interval_ms=1000
)

for message in consumer:
    print(f"Key: {message.key}")
    print(f"Value: {message.value}")
    print(f"Partition: {message.partition}")
    print(f"Offset: {message.offset}")
```

## 🔧 Data Engineering Workflows

### 1. Real-time ETL Pipeline
```python
from kafka import KafkaConsumer, KafkaProducer
import json
import logging

class RealTimeETL:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'raw-events',
            bootstrap_servers=['localhost:9092'],
            group_id='etl-processor',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    
    def transform_event(self, raw_event):
        """Transform raw event data"""
        return {
            'user_id': raw_event.get('user_id'),
            'event_type': raw_event.get('event_type'),
            'processed_timestamp': int(time.time()),
            'enriched_data': self.enrich_event(raw_event)
        }
    
    def enrich_event(self, event):
        """Add additional context to event"""
        # Simulate enrichment logic
        return {
            'user_segment': 'premium' if event.get('user_id', '').endswith('1') else 'standard',
            'event_category': self.categorize_event(event.get('event_type'))
        }
    
    def categorize_event(self, event_type):
        categories = {
            'page_view': 'engagement',
            'purchase': 'conversion',
            'signup': 'acquisition'
        }
        return categories.get(event_type, 'other')
    
    def process_events(self):
        """Main processing loop"""
        for message in self.consumer:
            try:
                # Transform the event
                transformed_event = self.transform_event(message.value)
                
                # Send to processed events topic
                self.producer.send('processed-events', transformed_event)
                
                # Send to specific topic based on event type
                event_type = transformed_event.get('event_type')
                if event_type:
                    self.producer.send(f'{event_type}-events', transformed_event)
                
                logging.info(f"Processed event: {transformed_event['user_id']}")
                
            except Exception as e:
                logging.error(f"Error processing event: {e}")
                # Send to dead letter queue
                self.producer.send('failed-events', {
                    'original_message': message.value,
                    'error': str(e),
                    'timestamp': int(time.time())
                })

# Usage
etl_processor = RealTimeETL()
etl_processor.process_events()
```

### 2. Stream Processing with Kafka Streams
```python
# Using confluent-kafka for stream processing
from confluent_kafka import Consumer, Producer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer, JSONDeserializer
import json

class StreamProcessor:
    def __init__(self):
        self.consumer_config = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'stream-processor',
            'auto.offset.reset': 'earliest'
        }
        
        self.producer_config = {
            'bootstrap.servers': 'localhost:9092'
        }
        
        self.consumer = Consumer(self.consumer_config)
        self.producer = Producer(self.producer_config)
    
    def process_user_activity_stream(self):
        """Process user activity stream with windowing"""
        self.consumer.subscribe(['user-activity'])
        
        user_sessions = {}  # In-memory session tracking
        
        try:
            while True:
                msg = self.consumer.poll(1.0)
                
                if msg is None:
                    continue
                
                if msg.error():
                    print(f"Consumer error: {msg.error()}")
                    continue
                
                # Parse message
                event = json.loads(msg.value().decode('utf-8'))
                user_id = event.get('user_id')
                timestamp = event.get('timestamp')
                
                # Update session tracking
                if user_id not in user_sessions:
                    user_sessions[user_id] = {
                        'session_start': timestamp,
                        'last_activity': timestamp,
                        'event_count': 0,
                        'events': []
                    }
                
                session = user_sessions[user_id]
                session['last_activity'] = timestamp
                session['event_count'] += 1
                session['events'].append(event)
                
                # Check for session timeout (5 minutes)
                if timestamp - session['last_activity'] > 300:
                    # Session ended, send summary
                    session_summary = {
                        'user_id': user_id,
                        'session_duration': session['last_activity'] - session['session_start'],
                        'total_events': session['event_count'],
                        'session_end': timestamp
                    }
                    
                    self.producer.produce(
                        'user-sessions',
                        key=user_id,
                        value=json.dumps(session_summary)
                    )
                    
                    # Clean up session
                    del user_sessions[user_id]
                
                self.producer.poll(0)
                
        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()
```

## ⚡ Performance Optimization

### 1. Producer Optimization
```python
# High-performance producer configuration
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    
    # Batching for throughput
    batch_size=32768,  # 32KB batches
    linger_ms=20,      # Wait up to 20ms to fill batch
    
    # Compression
    compression_type='snappy',  # or 'gzip', 'lz4'
    
    # Reliability
    acks='all',        # Wait for all replicas
    retries=3,
    retry_backoff_ms=100,
    
    # Memory management
    buffer_memory=67108864,  # 64MB buffer
    max_block_ms=60000,      # Block for 60s if buffer full
    
    # Serialization
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Async sending with callbacks
def delivery_callback(err, msg):
    if err:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}] @ {msg.offset()}')

# Send with callback
producer.send('events', {'key': 'value'}).add_callback(delivery_callback)
```

### 2. Consumer Optimization
```python
# High-performance consumer configuration
consumer = KafkaConsumer(
    'events',
    bootstrap_servers=['localhost:9092'],
    group_id='high-perf-consumer',
    
    # Fetching optimization
    fetch_min_bytes=50000,      # Wait for 50KB before returning
    fetch_max_wait_ms=500,      # Max wait 500ms
    max_partition_fetch_bytes=1048576,  # 1MB per partition
    
    # Processing optimization
    max_poll_records=1000,      # Process up to 1000 records per poll
    max_poll_interval_ms=300000,  # 5 minutes max processing time
    
    # Offset management
    enable_auto_commit=False,   # Manual commit for better control
    auto_offset_reset='earliest',
    
    # Deserialization
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Batch processing
messages = []
for message in consumer:
    messages.append(message)
    
    # Process in batches of 100
    if len(messages) >= 100:
        process_batch(messages)
        consumer.commit()  # Commit after successful processing
        messages = []
```

### 3. Topic Configuration
```bash
# Create optimized topic
kafka-topics.sh --create \
  --topic high-throughput-events \
  --partitions 12 \
  --replication-factor 3 \
  --config min.insync.replicas=2 \
  --config unclean.leader.election.enable=false \
  --config retention.ms=604800000 \
  --config segment.ms=86400000 \
  --config compression.type=snappy \
  --bootstrap-server localhost:9092
```

## 🔒 Security and Monitoring

### 1. Security Configuration
```properties
# server.properties for secure Kafka
listeners=SASL_SSL://localhost:9093
security.inter.broker.protocol=SASL_SSL
sasl.mechanism.inter.broker.protocol=PLAIN
sasl.enabled.mechanisms=PLAIN

# SSL configuration
ssl.keystore.location=/path/to/kafka.server.keystore.jks
ssl.keystore.password=keystore_password
ssl.key.password=key_password
ssl.truststore.location=/path/to/kafka.server.truststore.jks
ssl.truststore.password=truststore_password

# ACL configuration
authorizer.class.name=kafka.security.authorizer.AclAuthorizer
super.users=User:admin
```

### 2. Monitoring and Metrics
```python
# Custom metrics collection
from kafka import KafkaConsumer
import time
import logging

class KafkaMonitor:
    def __init__(self):
        self.consumer = KafkaConsumer(
            bootstrap_servers=['localhost:9092'],
            group_id='monitor-group'
        )
        
    def monitor_lag(self, topic, group_id):
        """Monitor consumer lag"""
        from kafka.admin import KafkaAdminClient, ConfigResource, ConfigResourceType
        
        admin_client = KafkaAdminClient(
            bootstrap_servers=['localhost:9092']
        )
        
        # Get partition metadata
        metadata = self.consumer.list_consumer_group_offsets(group_id)
        
        for topic_partition, offset_metadata in metadata.items():
            if topic_partition.topic == topic:
                # Get high water mark
                high_water_mark = self.consumer.get_partition_metadata(
                    topic_partition.topic, 
                    topic_partition.partition
                ).high_water_mark
                
                lag = high_water_mark - offset_metadata.offset
                
                print(f"Partition {topic_partition.partition}: Lag = {lag}")
                
                # Alert if lag is too high
                if lag > 10000:
                    logging.warning(f"High lag detected: {lag} messages")
    
    def collect_broker_metrics(self):
        """Collect broker-level metrics"""
        # This would typically integrate with JMX or monitoring tools
        metrics = {
            'messages_per_second': self.get_message_rate(),
            'bytes_per_second': self.get_byte_rate(),
            'request_latency': self.get_request_latency(),
            'error_rate': self.get_error_rate()
        }
        
        return metrics
```

## 🎯 Best Practices Summary

### 1. Design Best Practices
- **Partition Strategy**: Use meaningful keys for even distribution
- **Topic Naming**: Use consistent naming conventions (e.g., `domain.entity.event`)
- **Schema Evolution**: Use Schema Registry for backward compatibility
- **Retention Policy**: Set appropriate retention based on use case

### 2. Performance Best Practices
- **Batch Processing**: Use batching for both producers and consumers
- **Compression**: Enable compression (snappy/lz4) for better throughput
- **Partitioning**: Right-size partitions (aim for 10-100 MB/partition/day)
- **Replication**: Use replication factor of 3 for production

### 3. Operational Best Practices
- **Monitoring**: Monitor lag, throughput, and error rates
- **Alerting**: Set up alerts for high lag and broker failures
- **Backup**: Regular backup of ZooKeeper and Kafka logs
- **Capacity Planning**: Monitor disk usage and plan for growth

### 4. Security Best Practices
- **Authentication**: Use SASL for client authentication
- **Authorization**: Implement ACLs for topic-level access control
- **Encryption**: Use SSL/TLS for data in transit
- **Network Security**: Isolate Kafka cluster in private networks

This guide provides essential Kafka knowledge for data engineering. Focus on understanding partitioning, consumer groups, and stream processing patterns for building robust real-time data pipelines.