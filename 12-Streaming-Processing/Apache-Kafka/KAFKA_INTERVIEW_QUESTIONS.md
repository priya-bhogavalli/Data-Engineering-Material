# Apache Kafka Interview Questions

## Basic Level Questions (1-3 years experience)

### 1. What is Apache Kafka and why is it used in data engineering?
**Answer**: Apache Kafka is a distributed streaming platform that provides high-throughput, fault-tolerant, and scalable messaging capabilities.

**Key Use Cases in Data Engineering**:
- **Real-time Data Pipelines**: Stream data between systems
- **Event Sourcing**: Store and replay events
- **Log Aggregation**: Collect logs from multiple services
- **Stream Processing**: Process data in real-time
- **Microservices Communication**: Decouple services

**Core Components**:
- **Producer**: Publishes messages to topics
- **Consumer**: Reads messages from topics
- **Broker**: Kafka server that stores and serves messages
- **Topic**: Category/feed of messages
- **Partition**: Ordered sequence of messages within a topic

```python
# Simple Producer Example
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Send message
producer.send('user-events', {
    'user_id': 123,
    'event': 'login',
    'timestamp': '2024-01-01T10:00:00Z'
})

producer.flush()
producer.close()
```

### 2. Explain Kafka Topics and Partitions
**Answer**: Topics are categories of messages, and partitions are ordered sequences within topics that enable parallelism and scalability.

**Key Concepts**:
- **Topic**: Logical grouping of messages (e.g., "user-events", "order-updates")
- **Partition**: Physical division of a topic for parallel processing
- **Offset**: Unique identifier for each message within a partition
- **Replication**: Copies of partitions across multiple brokers

```bash
# Create topic with 3 partitions and replication factor 2
kafka-topics.sh --create \
  --bootstrap-server localhost:9092 \
  --topic user-events \
  --partitions 3 \
  --replication-factor 2

# List topics
kafka-topics.sh --list --bootstrap-server localhost:9092

# Describe topic
kafka-topics.sh --describe \
  --bootstrap-server localhost:9092 \
  --topic user-events
```

**Partition Strategy**:
```python
from kafka import KafkaProducer
from kafka.partitioner import RoundRobinPartitioner, Murmur2Partitioner

# Custom partitioner
class UserPartitioner:
    def __call__(self, key, all_partitions, available_partitions):
        if key is None:
            return random.choice(available_partitions)
        # Hash user_id to partition
        return hash(key) % len(all_partitions)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    partitioner=UserPartitioner(),
    key_serializer=str.encode,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Messages with same key go to same partition
producer.send('user-events', key='user_123', value={'event': 'login'})
```

### 3. How do Kafka Producers work?
**Answer**: Producers publish messages to Kafka topics with configurable delivery semantics and performance optimizations.

```python
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import logging

class DataProducer:
    def __init__(self, bootstrap_servers, topic):
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            # Serialization
            key_serializer=str.encode,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            
            # Performance settings
            batch_size=16384,  # Batch size in bytes
            linger_ms=10,      # Wait time to batch messages
            buffer_memory=33554432,  # Total memory for buffering
            
            # Reliability settings
            acks='all',        # Wait for all replicas to acknowledge
            retries=3,         # Number of retries
            retry_backoff_ms=100,
            
            # Compression
            compression_type='gzip'
        )
    
    def send_message(self, key, value):
        """Send message with error handling."""
        try:
            # Asynchronous send
            future = self.producer.send(self.topic, key=key, value=value)
            
            # Optional: Wait for result
            record_metadata = future.get(timeout=10)
            
            logging.info(f"Message sent to {record_metadata.topic} "
                        f"partition {record_metadata.partition} "
                        f"offset {record_metadata.offset}")
            
        except KafkaError as e:
            logging.error(f"Failed to send message: {e}")
            raise
    
    def send_batch(self, messages):
        """Send multiple messages efficiently."""
        for key, value in messages:
            self.producer.send(self.topic, key=key, value=value)
        
        # Flush to ensure all messages are sent
        self.producer.flush()
    
    def close(self):
        self.producer.close()

# Usage
producer = DataProducer(['localhost:9092'], 'user-events')

# Send single message
producer.send_message('user_123', {
    'user_id': 123,
    'action': 'purchase',
    'amount': 99.99,
    'timestamp': '2024-01-01T10:00:00Z'
})

# Send batch
messages = [
    ('user_124', {'user_id': 124, 'action': 'login'}),
    ('user_125', {'user_id': 125, 'action': 'logout'})
]
producer.send_batch(messages)
producer.close()
```

### 4. How do Kafka Consumers work?
**Answer**: Consumers read messages from topics, with support for consumer groups for parallel processing and fault tolerance.

```python
from kafka import KafkaConsumer
import json
import logging

class DataConsumer:
    def __init__(self, topics, bootstrap_servers, group_id):
        self.consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            
            # Deserialization
            key_deserializer=lambda k: k.decode('utf-8') if k else None,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            
            # Consumer settings
            auto_offset_reset='earliest',  # Start from beginning if no offset
            enable_auto_commit=False,      # Manual commit for reliability
            max_poll_records=500,          # Max records per poll
            session_timeout_ms=30000,      # Session timeout
            heartbeat_interval_ms=3000,    # Heartbeat interval
        )
    
    def consume_messages(self):
        """Consume messages with manual commit."""
        try:
            for message in self.consumer:
                try:
                    # Process message
                    self.process_message(message)
                    
                    # Commit offset after successful processing
                    self.consumer.commit()
                    
                except Exception as e:
                    logging.error(f"Error processing message: {e}")
                    # Handle error (retry, dead letter queue, etc.)
                    
        except KeyboardInterrupt:
            logging.info("Consumer interrupted")
        finally:
            self.consumer.close()
    
    def process_message(self, message):
        """Process individual message."""
        logging.info(f"Processing message from topic {message.topic} "
                    f"partition {message.partition} offset {message.offset}")
        
        key = message.key
        value = message.value
        
        # Business logic here
        if value.get('action') == 'purchase':
            self.handle_purchase(value)
        elif value.get('action') == 'login':
            self.handle_login(value)
    
    def handle_purchase(self, data):
        """Handle purchase event."""
        user_id = data['user_id']
        amount = data['amount']
        logging.info(f"User {user_id} purchased ${amount}")
        # Update database, send notifications, etc.
    
    def handle_login(self, data):
        """Handle login event."""
        user_id = data['user_id']
        logging.info(f"User {user_id} logged in")
        # Update user session, analytics, etc.

# Usage
consumer = DataConsumer(
    topics=['user-events'],
    bootstrap_servers=['localhost:9092'],
    group_id='user-event-processor'
)

consumer.consume_messages()
```

### 5. What are Consumer Groups and how do they work?
**Answer**: Consumer groups enable parallel processing by distributing partitions among multiple consumers, providing scalability and fault tolerance.

```python
# Multiple consumers in same group
import threading
from kafka import KafkaConsumer

def create_consumer(group_id, consumer_id):
    """Create consumer instance."""
    consumer = KafkaConsumer(
        'user-events',
        bootstrap_servers=['localhost:9092'],
        group_id=group_id,
        client_id=f'consumer-{consumer_id}',
        auto_offset_reset='earliest',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    
    print(f"Consumer {consumer_id} started")
    
    for message in consumer:
        print(f"Consumer {consumer_id} processed message: {message.value}")
        # Simulate processing time
        time.sleep(1)

# Start multiple consumers in same group
group_id = 'parallel-processors'
threads = []

for i in range(3):  # 3 consumers in same group
    thread = threading.Thread(
        target=create_consumer,
        args=(group_id, i)
    )
    thread.start()
    threads.append(thread)

# Each consumer will get different partitions
# If topic has 3 partitions and 3 consumers, each gets 1 partition
```

**Consumer Group Management**:
```bash
# List consumer groups
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list

# Describe consumer group
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group user-event-processor --describe

# Reset consumer group offset
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group user-event-processor --topic user-events \
  --reset-offsets --to-earliest --execute
```

## Intermediate Level Questions (3-5 years experience)

### 6. How do you handle message ordering in Kafka?
**Answer**: Kafka guarantees ordering within partitions. Use appropriate partitioning strategies to maintain order where needed.

```python
class OrderedProducer:
    def __init__(self, bootstrap_servers):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            key_serializer=str.encode,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            
            # Settings for ordering
            max_in_flight_requests_per_connection=1,  # Ensure ordering
            retries=3,
            acks='all'
        )
    
    def send_user_events(self, user_id, events):
        """Send events for a user in order."""
        # Use user_id as key to ensure all events for same user
        # go to same partition (maintaining order)
        
        for event in events:
            self.producer.send(
                'user-events',
                key=str(user_id),  # Same key = same partition
                value=event
            )
        
        self.producer.flush()  # Ensure all sent before returning

# Usage - events for same user will be ordered
producer = OrderedProducer(['localhost:9092'])

user_events = [
    {'action': 'login', 'timestamp': '2024-01-01T10:00:00Z'},
    {'action': 'view_product', 'timestamp': '2024-01-01T10:01:00Z'},
    {'action': 'add_to_cart', 'timestamp': '2024-01-01T10:02:00Z'},
    {'action': 'purchase', 'timestamp': '2024-01-01T10:03:00Z'}
]

producer.send_user_events(user_id=123, events=user_events)
```

**Global Ordering (Single Partition)**:
```python
# For global ordering, use single partition
# Trade-off: Lower throughput but guaranteed global order

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Create topic with single partition
# kafka-topics.sh --create --topic ordered-events --partitions 1

def send_ordered_event(event):
    """Send to single partition for global ordering."""
    producer.send('ordered-events', value=event)
```

### 7. How do you implement exactly-once semantics in Kafka?
**Answer**: Use Kafka's transactional API and idempotent producers for exactly-once processing.

```python
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError

class ExactlyOnceProcessor:
    def __init__(self, bootstrap_servers, transactional_id):
        # Transactional producer
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            transactional_id=transactional_id,
            enable_idempotence=True,
            acks='all',
            retries=3,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        # Initialize transactions
        self.producer.init_transactions()
        
        # Consumer for reading
        self.consumer = KafkaConsumer(
            'input-topic',
            bootstrap_servers=bootstrap_servers,
            group_id='exactly-once-group',
            enable_auto_commit=False,  # Manual commit within transaction
            isolation_level='read_committed',  # Only read committed messages
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
    
    def process_messages(self):
        """Process messages with exactly-once semantics."""
        for message in self.consumer:
            try:
                # Begin transaction
                self.producer.begin_transaction()
                
                # Process message
                processed_data = self.transform_message(message.value)
                
                # Send processed data
                self.producer.send('output-topic', value=processed_data)
                
                # Send consumer offsets as part of transaction
                offsets = {
                    TopicPartition(message.topic, message.partition): 
                    OffsetAndMetadata(message.offset + 1, None)
                }
                self.producer.send_offsets_to_transaction(
                    offsets, 
                    self.consumer.config['group_id']
                )
                
                # Commit transaction
                self.producer.commit_transaction()
                
            except Exception as e:
                # Abort transaction on error
                self.producer.abort_transaction()
                logging.error(f"Transaction aborted due to error: {e}")
                raise
    
    def transform_message(self, data):
        """Transform message data."""
        # Business logic here
        return {
            'processed_at': datetime.now().isoformat(),
            'original_data': data,
            'processed_value': data.get('value', 0) * 2
        }
    
    def close(self):
        self.consumer.close()
        self.producer.close()

# Usage
processor = ExactlyOnceProcessor(
    bootstrap_servers=['localhost:9092'],
    transactional_id='exactly-once-processor-1'
)

try:
    processor.process_messages()
finally:
    processor.close()
```

### 8. How do you monitor Kafka performance and health?
**Answer**: Use JMX metrics, monitoring tools, and custom health checks to monitor Kafka clusters.

```python
import time
from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.admin import ConfigResource, ConfigResourceType

class KafkaMonitor:
    def __init__(self, bootstrap_servers):
        self.bootstrap_servers = bootstrap_servers
        self.admin_client = KafkaAdminClient(
            bootstrap_servers=bootstrap_servers
        )
    
    def check_cluster_health(self):
        """Check overall cluster health."""
        try:
            # Check if we can connect and get metadata
            metadata = self.admin_client.describe_cluster()
            
            health_status = {
                'cluster_id': metadata.cluster_id,
                'controller': metadata.controller,
                'brokers': len(metadata.brokers),
                'status': 'healthy'
            }
            
            return health_status
            
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
    
    def check_topic_health(self, topic_name):
        """Check specific topic health."""
        try:
            # Get topic metadata
            metadata = self.admin_client.describe_topics([topic_name])
            topic_metadata = metadata[topic_name]
            
            # Check partition health
            partition_health = []
            for partition in topic_metadata.partitions:
                partition_info = {
                    'partition_id': partition.partition,
                    'leader': partition.leader,
                    'replicas': len(partition.replicas),
                    'in_sync_replicas': len(partition.isr)
                }
                partition_health.append(partition_info)
            
            return {
                'topic': topic_name,
                'partitions': len(topic_metadata.partitions),
                'partition_details': partition_health,
                'status': 'healthy'
            }
            
        except Exception as e:
            return {
                'topic': topic_name,
                'status': 'unhealthy',
                'error': str(e)
            }
    
    def check_consumer_lag(self, group_id, topic):
        """Check consumer lag for a group."""
        try:
            # Create consumer to get current offsets
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=self.bootstrap_servers,
                group_id=group_id,
                enable_auto_commit=False
            )
            
            # Get partition assignments
            partitions = consumer.partitions_for_topic(topic)
            topic_partitions = [TopicPartition(topic, p) for p in partitions]
            
            # Get current offsets (latest available)
            end_offsets = consumer.end_offsets(topic_partitions)
            
            # Get committed offsets (consumer position)
            committed_offsets = consumer.committed(set(topic_partitions))
            
            lag_info = {}
            total_lag = 0
            
            for tp in topic_partitions:
                end_offset = end_offsets[tp]
                committed_offset = committed_offsets[tp]
                
                if committed_offset is not None:
                    lag = end_offset - committed_offset.offset
                else:
                    lag = end_offset  # No committed offset yet
                
                lag_info[f"partition_{tp.partition}"] = {
                    'end_offset': end_offset,
                    'committed_offset': committed_offset.offset if committed_offset else 0,
                    'lag': lag
                }
                total_lag += lag
            
            consumer.close()
            
            return {
                'group_id': group_id,
                'topic': topic,
                'total_lag': total_lag,
                'partition_lags': lag_info
            }
            
        except Exception as e:
            return {
                'group_id': group_id,
                'topic': topic,
                'error': str(e)
            }

# Usage
monitor = KafkaMonitor(['localhost:9092'])

# Check cluster health
cluster_health = monitor.check_cluster_health()
print(f"Cluster health: {cluster_health}")

# Check topic health
topic_health = monitor.check_topic_health('user-events')
print(f"Topic health: {topic_health}")

# Check consumer lag
lag_info = monitor.check_consumer_lag('user-event-processor', 'user-events')
print(f"Consumer lag: {lag_info}")
```

**Monitoring with External Tools**:
```yaml
# docker-compose.yml for Kafka monitoring stack
version: '3.8'

services:
  kafka:
    image: confluentinc/cp-kafka:latest
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      # Enable JMX for monitoring
      KAFKA_JMX_PORT: 9999
      KAFKA_JMX_HOSTNAME: localhost

  kafka-exporter:
    image: danielqsj/kafka-exporter
    command: --kafka.server=kafka:9092
    ports:
      - "9308:9308"
    depends_on:
      - kafka

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
```

### 9. How do you handle schema evolution in Kafka?
**Answer**: Use Schema Registry with Avro, JSON Schema, or Protobuf for managing schema evolution.

```python
from confluent_kafka import Producer, Consumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer, AvroDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField

# Avro schema (version 1)
user_schema_v1 = """
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": "string"}
  ]
}
"""

# Avro schema (version 2 - backward compatible)
user_schema_v2 = """
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": "string"},
    {"name": "age", "type": ["null", "int"], "default": null}
  ]
}
"""

class SchemaEvolutionExample:
    def __init__(self, schema_registry_url, bootstrap_servers):
        # Schema Registry client
        self.schema_registry_client = SchemaRegistryClient({
            'url': schema_registry_url
        })
        
        # Register schemas
        self.register_schemas()
        
        # Kafka producer/consumer config
        self.kafka_config = {
            'bootstrap.servers': bootstrap_servers
        }
    
    def register_schemas(self):
        """Register schemas with Schema Registry."""
        # Register version 1
        self.schema_registry_client.register_schema(
            subject='user-value',
            schema=user_schema_v1
        )
        
        # Register version 2 (evolution)
        self.schema_registry_client.register_schema(
            subject='user-value',
            schema=user_schema_v2
        )
    
    def produce_with_schema(self, schema_version=2):
        """Produce messages with schema."""
        # Get schema
        if schema_version == 1:
            schema_str = user_schema_v1
        else:
            schema_str = user_schema_v2
        
        # Create serializer
        avro_serializer = AvroSerializer(
            self.schema_registry_client,
            schema_str
        )
        
        # Create producer
        producer = Producer(self.kafka_config)
        
        # Sample data
        if schema_version == 1:
            user_data = {
                'id': 123,
                'name': 'John Doe',
                'email': 'john@example.com'
            }
        else:
            user_data = {
                'id': 123,
                'name': 'John Doe',
                'email': 'john@example.com',
                'age': 30  # New field in v2
            }
        
        # Serialize and send
        serialized_data = avro_serializer(
            user_data,
            SerializationContext('user-topic', MessageField.VALUE)
        )
        
        producer.produce(
            topic='user-topic',
            value=serialized_data
        )
        
        producer.flush()
        producer.close()
    
    def consume_with_schema(self):
        """Consume messages with schema evolution support."""
        # Create deserializer (handles multiple schema versions)
        avro_deserializer = AvroDeserializer(
            self.schema_registry_client
        )
        
        # Create consumer
        consumer_config = {
            **self.kafka_config,
            'group.id': 'schema-evolution-group',
            'auto.offset.reset': 'earliest'
        }
        
        consumer = Consumer(consumer_config)
        consumer.subscribe(['user-topic'])
        
        try:
            while True:
                msg = consumer.poll(1.0)
                
                if msg is None:
                    continue
                
                if msg.error():
                    print(f"Consumer error: {msg.error()}")
                    continue
                
                # Deserialize (automatically handles schema evolution)
                user_data = avro_deserializer(
                    msg.value(),
                    SerializationContext('user-topic', MessageField.VALUE)
                )
                
                print(f"Received user: {user_data}")
                
                # Handle different schema versions
                if 'age' in user_data:
                    print(f"User age: {user_data['age']}")
                else:
                    print("Age not available (older schema version)")
                
        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()

# Usage
schema_example = SchemaEvolutionExample(
    schema_registry_url='http://localhost:8081',
    bootstrap_servers='localhost:9092'
)

# Produce with different schema versions
schema_example.produce_with_schema(schema_version=1)  # Old schema
schema_example.produce_with_schema(schema_version=2)  # New schema

# Consume (handles both versions)
schema_example.consume_with_schema()
```

### 10. How do you implement Kafka Streams for real-time processing?
**Answer**: Use Kafka Streams API for building real-time stream processing applications.

```python
# Note: This is conceptual Python code. 
# Kafka Streams is primarily Java/Scala, but similar concepts apply

from kafka import KafkaConsumer, KafkaProducer
import json
from collections import defaultdict, deque
import time
import threading

class StreamProcessor:
    def __init__(self, bootstrap_servers, application_id):
        self.bootstrap_servers = bootstrap_servers
        self.application_id = application_id
        
        # State stores (in-memory for this example)
        self.state_store = defaultdict(dict)
        self.window_store = defaultdict(lambda: deque())
        
        # Consumer for input streams
        self.consumer = KafkaConsumer(
            bootstrap_servers=bootstrap_servers,
            group_id=application_id,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            auto_offset_reset='earliest'
        )
        
        # Producer for output streams
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    
    def process_user_events(self):
        """Process user events stream."""
        self.consumer.subscribe(['user-events'])
        
        for message in self.consumer:
            event = message.value
            user_id = event.get('user_id')
            action = event.get('action')
            timestamp = event.get('timestamp')
            
            # Stateful processing - count actions per user
            if user_id not in self.state_store:
                self.state_store[user_id] = {'login_count': 0, 'purchase_count': 0}
            
            if action == 'login':
                self.state_store[user_id]['login_count'] += 1
            elif action == 'purchase':
                self.state_store[user_id]['purchase_count'] += 1
            
            # Windowed aggregation - purchases in last 5 minutes
            self.add_to_window(user_id, action, timestamp)
            recent_purchases = self.count_recent_purchases(user_id)
            
            # Output processed event
            output_event = {
                'user_id': user_id,
                'total_logins': self.state_store[user_id]['login_count'],
                'total_purchases': self.state_store[user_id]['purchase_count'],
                'recent_purchases_5min': recent_purchases,
                'processed_at': time.time()
            }
            
            self.producer.send('user-stats', value=output_event)
            
            # Check for patterns (e.g., high-value customer)
            if recent_purchases >= 3:
                alert = {
                    'user_id': user_id,
                    'alert_type': 'high_activity',
                    'recent_purchases': recent_purchases,
                    'timestamp': time.time()
                }
                self.producer.send('user-alerts', value=alert)
    
    def add_to_window(self, user_id, action, timestamp):
        """Add event to time window."""
        if action == 'purchase':
            self.window_store[user_id].append(timestamp)
            
            # Clean old events (older than 5 minutes)
            cutoff_time = time.time() - 300  # 5 minutes
            while (self.window_store[user_id] and 
                   self.window_store[user_id][0] < cutoff_time):
                self.window_store[user_id].popleft()
    
    def count_recent_purchases(self, user_id):
        """Count purchases in recent window."""
        return len(self.window_store[user_id])
    
    def join_streams(self):
        """Example of stream-stream join."""
        # This would typically involve more complex coordination
        # between multiple input streams
        pass
    
    def close(self):
        self.consumer.close()
        self.producer.close()

# Usage
processor = StreamProcessor(
    bootstrap_servers=['localhost:9092'],
    application_id='user-event-processor'
)

try:
    processor.process_user_events()
finally:
    processor.close()
```

**Java Kafka Streams Example** (for reference):
```java
// Java Kafka Streams - more typical implementation
Properties props = new Properties();
props.put(StreamsConfig.APPLICATION_ID_CONFIG, "user-event-processor");
props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");

StreamsBuilder builder = new StreamsBuilder();

// Input stream
KStream<String, UserEvent> userEvents = builder.stream("user-events");

// Stateful processing - count by user
KTable<String, Long> userLoginCounts = userEvents
    .filter((key, event) -> "login".equals(event.getAction()))
    .groupBy((key, event) -> event.getUserId())
    .count();

// Windowed aggregation
KTable<Windowed<String>, Long> windowedCounts = userEvents
    .filter((key, event) -> "purchase".equals(event.getAction()))
    .groupBy((key, event) -> event.getUserId())
    .windowedBy(TimeWindows.of(Duration.ofMinutes(5)))
    .count();

// Output results
userLoginCounts.toStream().to("user-login-counts");
windowedCounts.toStream().to("user-purchase-windows");

KafkaStreams streams = new KafkaStreams(builder.build(), props);
streams.start();
```

This comprehensive set covers Kafka fundamentals through advanced stream processing concepts with practical data engineering examples.