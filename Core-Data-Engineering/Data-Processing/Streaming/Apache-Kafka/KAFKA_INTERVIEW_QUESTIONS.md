# Apache Kafka Interview Questions

## Table of Contents

1. [Basic Kafka Concepts](#basic-kafka-concepts)
2. [Kafka Architecture](#kafka-architecture)
3. [Producers and Consumers](#producers-and-consumers)
4. [Performance and Scaling](#performance-and-scaling)
5. [Data Engineering Use Cases](#data-engineering-use-cases)

---

## Basic Kafka Concepts

### Q1: What is Apache Kafka and what problems does it solve?

**Answer:**
Apache Kafka is a distributed streaming platform designed for high-throughput, fault-tolerant, real-time data streaming. It solves problems of data integration, real-time processing, and building event-driven architectures.

**Key Problems Solved:**
- **Data Integration**: Connect multiple systems with decoupled architecture
- **Real-time Processing**: Handle high-volume streaming data
- **Scalability**: Horizontal scaling for massive throughput
- **Fault Tolerance**: Distributed replication and durability
- **Event Sourcing**: Store and replay events for system recovery

**Code Example:**
```python
from kafka import KafkaProducer, KafkaConsumer
import json

# Producer example
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Send message
message = {
    'user_id': 12345,
    'event': 'page_view',
    'timestamp': '2023-01-15T10:30:00Z',
    'page': '/products'
}

producer.send('user_events', message)
producer.flush()
print("Message sent successfully")
# Output: Message sent successfully

# Consumer example
consumer = KafkaConsumer(
    'user_events',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    print(f"Received: {message.value}")
    break
# Output: Received: {'user_id': 12345, 'event': 'page_view', 'timestamp': '2023-01-15T10:30:00Z', 'page': '/products'}
```

### Q2: Explain Kafka's key components and terminology.

**Answer:**
Kafka consists of several key components that work together to provide distributed streaming capabilities.

**Core Components:**
- **Topic**: Category of messages (like a database table)
- **Partition**: Ordered sequence within a topic for scalability
- **Broker**: Kafka server that stores and serves data
- **Producer**: Application that sends messages to topics
- **Consumer**: Application that reads messages from topics
- **Consumer Group**: Set of consumers working together
- **Offset**: Unique identifier for each message in a partition

**Code Example:**
```bash
# Create topic with multiple partitions
kafka-topics.sh --create \
  --topic user_events \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 2

# List topics
kafka-topics.sh --list --bootstrap-server localhost:9092
# Output: user_events

# Describe topic
kafka-topics.sh --describe \
  --topic user_events \
  --bootstrap-server localhost:9092
# Output: Topic: user_events	PartitionCount: 3	ReplicationFactor: 2
```

```python
# Python example showing partitioning
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    # Custom partitioner based on user_id
    partitioner=lambda key, all_partitions, available: hash(key) % len(all_partitions)
)

# Messages with same key go to same partition
for i in range(5):
    message = {'user_id': f'user_{i%2}', 'data': f'message_{i}'}
    producer.send('user_events', value=message, key=f'user_{i%2}'.encode())

producer.flush()
print("Messages sent to partitions based on user_id")
# Output: Messages sent to partitions based on user_id
```

### Q3: What is the difference between Kafka and traditional message queues?

**Answer:**
Kafka differs from traditional message queues in architecture, durability, and consumption patterns.

**Key Differences:**
- **Persistence**: Kafka stores messages on disk vs in-memory queues
- **Consumption**: Multiple consumers can read same message vs single consumption
- **Ordering**: Partition-level ordering vs global ordering
- **Scalability**: Horizontal scaling through partitions vs vertical scaling
- **Retention**: Configurable retention vs immediate deletion after consumption

**Code Example:**
```python
# Traditional queue behavior simulation
import queue
import threading

# Traditional queue - message consumed once
traditional_queue = queue.Queue()
traditional_queue.put("message1")
traditional_queue.put("message2")

# Only one consumer gets each message
consumer1_msg = traditional_queue.get()
consumer2_msg = traditional_queue.get()
print(f"Consumer1: {consumer1_msg}, Consumer2: {consumer2_msg}")
# Output: Consumer1: message1, Consumer2: message2

# Kafka behavior - multiple consumers can read same messages
from kafka import KafkaConsumer
import json

# Consumer Group 1
consumer_group1 = KafkaConsumer(
    'user_events',
    bootstrap_servers=['localhost:9092'],
    group_id='analytics_team',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Consumer Group 2 - can read same messages
consumer_group2 = KafkaConsumer(
    'user_events',
    bootstrap_servers=['localhost:9092'],
    group_id='ml_team',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Both consumer groups can process same messages independently")
# Output: Both consumer groups can process same messages independently
```

## Kafka Architecture

### Q4: Explain Kafka's distributed architecture and how it ensures fault tolerance.

**Answer:**
Kafka's distributed architecture uses replication, leader election, and partitioning to ensure high availability and fault tolerance.

**Architecture Components:**
- **Cluster**: Multiple brokers working together
- **Replication**: Each partition has multiple replicas across brokers
- **Leader/Follower**: One leader handles reads/writes, followers replicate
- **ZooKeeper/KRaft**: Coordination and metadata management
- **ISR**: In-Sync Replicas for consistency

**Code Example:**
```bash
# Create topic with replication
kafka-topics.sh --create \
  --topic critical_events \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 3 \
  --config min.insync.replicas=2

# Check replica distribution
kafka-topics.sh --describe \
  --topic critical_events \
  --bootstrap-server localhost:9092
# Output shows leader and replica assignments across brokers
```

```python
# Producer with fault tolerance configuration
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['broker1:9092', 'broker2:9092', 'broker3:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    # Fault tolerance settings
    acks='all',  # Wait for all in-sync replicas
    retries=3,   # Retry failed sends
    retry_backoff_ms=1000,
    # Idempotence to prevent duplicates
    enable_idempotence=True,
    # Batch settings for efficiency
    batch_size=16384,
    linger_ms=10
)

# Send with error handling
try:
    future = producer.send('critical_events', {
        'event_id': 'evt_001',
        'data': 'critical_business_event'
    })
    
    # Wait for acknowledgment
    record_metadata = future.get(timeout=10)
    print(f"Message sent to partition {record_metadata.partition} at offset {record_metadata.offset}")
    # Output: Message sent to partition 1 at offset 42
    
except Exception as e:
    print(f"Failed to send message: {e}")

producer.close()
```

### Q5: How does Kafka handle message ordering and delivery guarantees?

**Answer:**
Kafka provides different levels of ordering and delivery guarantees depending on configuration and usage patterns.

**Ordering Guarantees:**
- **Partition Level**: Messages within a partition are strictly ordered
- **Topic Level**: No global ordering across partitions
- **Key-based**: Messages with same key go to same partition

**Delivery Guarantees:**
- **At Most Once**: May lose messages, no duplicates
- **At Least Once**: No message loss, may have duplicates
- **Exactly Once**: No loss, no duplicates (with idempotent producers)

**Code Example:**
```python
from kafka import KafkaProducer, KafkaConsumer
import json
import time

# Exactly-once producer configuration
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    # Exactly-once semantics
    enable_idempotence=True,
    acks='all',
    retries=2147483647,  # Max retries
    max_in_flight_requests_per_connection=5,
    # Transactional settings
    transactional_id='my-transactional-id'
)

# Initialize transactions
producer.init_transactions()

try:
    # Begin transaction
    producer.begin_transaction()
    
    # Send messages in transaction
    for i in range(3):
        message = {
            'order_id': f'order_{i}',
            'amount': 100.0 + i,
            'timestamp': time.time()
        }
        producer.send('orders', value=message, key=f'order_{i}'.encode())
    
    # Commit transaction
    producer.commit_transaction()
    print("Transaction committed successfully")
    # Output: Transaction committed successfully
    
except Exception as e:
    # Abort transaction on error
    producer.abort_transaction()
    print(f"Transaction aborted: {e}")

# Consumer with exactly-once processing
consumer = KafkaConsumer(
    'orders',
    bootstrap_servers=['localhost:9092'],
    group_id='order_processor',
    # Exactly-once consumption
    isolation_level='read_committed',
    enable_auto_commit=False,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Manual offset management for exactly-once
for message in consumer:
    try:
        # Process message
        order = message.value
        print(f"Processing order: {order['order_id']}")
        
        # Simulate processing
        time.sleep(0.1)
        
        # Commit offset after successful processing
        consumer.commit()
        print(f"Order {order['order_id']} processed successfully")
        
    except Exception as e:
        print(f"Error processing message: {e}")
        # Don't commit offset on error
        break
```

## Producers and Consumers

### Q6: How do you optimize Kafka producer performance?

**Answer:**
Producer performance optimization involves batching, compression, partitioning strategy, and proper configuration tuning.

**Optimization Strategies:**
- **Batching**: Group messages for efficient network usage
- **Compression**: Reduce network and storage overhead
- **Async Sending**: Non-blocking message sending
- **Partitioning**: Distribute load across partitions
- **Connection Pooling**: Reuse connections efficiently

**Code Example:**
```python
from kafka import KafkaProducer
import json
import time
import threading
from concurrent.futures import ThreadPoolExecutor

class OptimizedKafkaProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            
            # Performance optimizations
            batch_size=32768,        # Larger batches
            linger_ms=20,           # Wait for batches to fill
            compression_type='snappy',  # Compress messages
            buffer_memory=67108864,  # 64MB buffer
            
            # Throughput vs latency trade-off
            acks=1,                 # Leader acknowledgment only
            retries=3,
            retry_backoff_ms=100,
            
            # Connection settings
            connections_max_idle_ms=540000,
            request_timeout_ms=30000
        )
    
    def send_batch_async(self, topic, messages):
        """Send messages asynchronously with callbacks"""
        futures = []
        
        for message in messages:
            future = self.producer.send(
                topic, 
                value=message,
                # Partition by user_id for even distribution
                key=str(message.get('user_id', '')).encode()
            )
            
            # Add callback for monitoring
            future.add_callback(self.on_send_success)
            future.add_errback(self.on_send_error)
            futures.append(future)
        
        return futures
    
    def on_send_success(self, record_metadata):
        """Callback for successful sends"""
        print(f"Message sent to {record_metadata.topic}[{record_metadata.partition}] at offset {record_metadata.offset}")
    
    def on_send_error(self, exception):
        """Callback for send errors"""
        print(f"Failed to send message: {exception}")
    
    def benchmark_throughput(self, topic, num_messages=10000):
        """Benchmark producer throughput"""
        messages = []
        for i in range(num_messages):
            message = {
                'user_id': i % 1000,
                'event': 'page_view',
                'timestamp': time.time(),
                'data': f'event_data_{i}'
            }
            messages.append(message)
        
        start_time = time.time()
        
        # Send messages in batches
        batch_size = 1000
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            
            for i in range(0, len(messages), batch_size):
                batch = messages[i:i + batch_size]
                future = executor.submit(self.send_batch_async, topic, batch)
                futures.append(future)
            
            # Wait for all batches to complete
            for future in futures:
                future.result()
        
        # Flush remaining messages
        self.producer.flush()
        
        end_time = time.time()
        duration = end_time - start_time
        throughput = num_messages / duration
        
        print(f"Sent {num_messages} messages in {duration:.2f} seconds")
        print(f"Throughput: {throughput:.2f} messages/second")
        # Output: Sent 10000 messages in 2.34 seconds
        # Output: Throughput: 4273.50 messages/second
    
    def close(self):
        self.producer.close()

# Usage example
producer = OptimizedKafkaProducer()

# Benchmark performance
producer.benchmark_throughput('performance_test', 5000)

producer.close()
```

### Q7: How do you implement consumer groups and handle rebalancing?

**Answer:**
Consumer groups enable parallel processing and automatic load balancing. Rebalancing redistributes partitions when consumers join or leave the group.

**Consumer Group Concepts:**
- **Partition Assignment**: Each partition assigned to one consumer in group
- **Rebalancing**: Redistribution when group membership changes
- **Coordination**: Group coordinator manages assignments
- **Offset Management**: Track processing progress per partition

**Code Example:**
```python
from kafka import KafkaConsumer
import json
import time
import threading
import signal
import sys

class KafkaConsumerGroup:
    def __init__(self, group_id, topics, consumer_id):
        self.group_id = group_id
        self.consumer_id = consumer_id
        self.running = True
        
        self.consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=['localhost:9092'],
            group_id=group_id,
            
            # Consumer group settings
            enable_auto_commit=False,  # Manual offset management
            auto_offset_reset='earliest',
            session_timeout_ms=30000,
            heartbeat_interval_ms=10000,
            max_poll_interval_ms=300000,
            
            # Rebalancing settings
            partition_assignment_strategy=['RoundRobinAssignor'],
            
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        
        # Set up graceful shutdown
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
    
    def on_assign(self, consumer, partitions):
        """Callback when partitions are assigned"""
        partition_list = [f"{tp.topic}[{tp.partition}]" for tp in partitions]
        print(f"Consumer {self.consumer_id} assigned partitions: {partition_list}")
    
    def on_revoke(self, consumer, partitions):
        """Callback when partitions are revoked (before rebalancing)"""
        partition_list = [f"{tp.topic}[{tp.partition}]" for tp in partitions]
        print(f"Consumer {self.consumer_id} revoking partitions: {partition_list}")
        
        # Commit offsets before rebalancing
        try:
            consumer.commit()
            print(f"Consumer {self.consumer_id} committed offsets before rebalancing")
        except Exception as e:
            print(f"Error committing offsets: {e}")
    
    def process_message(self, message):
        """Process individual message"""
        try:
            # Simulate processing time
            time.sleep(0.1)
            
            data = message.value
            print(f"Consumer {self.consumer_id} processed: {data.get('event_id', 'unknown')}")
            
            return True
        except Exception as e:
            print(f"Error processing message: {e}")
            return False
    
    def start_consuming(self):
        """Start consuming messages"""
        print(f"Consumer {self.consumer_id} starting...")
        
        # Subscribe with rebalance callbacks
        self.consumer.subscribe(
            self.consumer.subscription(),
            on_assign=self.on_assign,
            on_revoke=self.on_revoke
        )
        
        try:
            while self.running:
                # Poll for messages
                message_batch = self.consumer.poll(timeout_ms=1000)
                
                if message_batch:
                    for topic_partition, messages in message_batch.items():
                        for message in messages:
                            if not self.running:
                                break
                            
                            success = self.process_message(message)
                            
                            if success:
                                # Commit offset for this message
                                self.consumer.commit_async({
                                    topic_partition: message.offset + 1
                                })
                            else:
                                print(f"Failed to process message at offset {message.offset}")
                                # Could implement retry logic here
                
                # Handle rebalancing
                if not self.running:
                    break
                    
        except Exception as e:
            print(f"Consumer {self.consumer_id} error: {e}")
        finally:
            self.consumer.close()
            print(f"Consumer {self.consumer_id} closed")
    
    def shutdown(self, signum, frame):
        """Graceful shutdown"""
        print(f"Consumer {self.consumer_id} shutting down...")
        self.running = False

# Simulate consumer group with multiple consumers
def run_consumer(group_id, topics, consumer_id):
    consumer = KafkaConsumerGroup(group_id, topics, consumer_id)
    consumer.start_consuming()

# Start multiple consumers in the same group
if __name__ == "__main__":
    group_id = "data_processing_group"
    topics = ["user_events", "order_events"]
    
    # Start 3 consumers in separate threads
    threads = []
    for i in range(3):
        consumer_id = f"consumer_{i}"
        thread = threading.Thread(
            target=run_consumer,
            args=(group_id, topics, consumer_id)
        )
        thread.daemon = True
        thread.start()
        threads.append(thread)
        
        # Stagger startup to see rebalancing
        time.sleep(2)
    
    print("All consumers started. Press Ctrl+C to stop.")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down all consumers...")
        
    # Wait for threads to complete
    for thread in threads:
        thread.join(timeout=5)
    
    print("All consumers stopped")
```

## Performance and Scaling

### Q8: How do you monitor and troubleshoot Kafka performance issues?

**Answer:**
Kafka monitoring involves tracking key metrics for brokers, producers, consumers, and topics to identify bottlenecks and performance issues.

**Key Metrics:**
- **Broker**: CPU, memory, disk I/O, network throughput
- **Producer**: Send rate, batch size, error rate, latency
- **Consumer**: Lag, throughput, rebalance frequency
- **Topic**: Message rate, partition distribution, retention

**Code Example:**
```python
from kafka import KafkaConsumer, KafkaProducer
from kafka.admin import KafkaAdminClient, ConfigResource, ConfigResourceType
import json
import time
import psutil
import threading

class KafkaMonitor:
    def __init__(self, bootstrap_servers):
        self.bootstrap_servers = bootstrap_servers
        self.admin_client = KafkaAdminClient(
            bootstrap_servers=bootstrap_servers
        )
        
    def get_consumer_lag(self, group_id, topic):
        """Calculate consumer lag for a group"""
        consumer = KafkaConsumer(
            bootstrap_servers=self.bootstrap_servers,
            group_id=group_id
        )
        
        # Get partition metadata
        partitions = consumer.partitions_for_topic(topic)
        if not partitions:
            return {}
        
        # Get current offsets (latest)
        topic_partitions = [TopicPartition(topic, p) for p in partitions]
        latest_offsets = consumer.end_offsets(topic_partitions)
        
        # Get committed offsets (consumer position)
        committed_offsets = consumer.committed(set(topic_partitions))
        
        lag_info = {}
        total_lag = 0
        
        for tp in topic_partitions:
            latest = latest_offsets.get(tp, 0)
            committed = committed_offsets.get(tp)
            committed_offset = committed.offset if committed else 0
            
            lag = latest - committed_offset
            lag_info[f"partition_{tp.partition}"] = {
                'latest_offset': latest,
                'committed_offset': committed_offset,
                'lag': lag
            }
            total_lag += lag
        
        consumer.close()
        
        return {
            'topic': topic,
            'group_id': group_id,
            'total_lag': total_lag,
            'partitions': lag_info
        }
    
    def get_broker_metrics(self):
        """Get broker performance metrics"""
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Network I/O
        network = psutil.net_io_counters()
        
        return {
            'timestamp': time.time(),
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_available_gb': memory.available / (1024**3),
            'disk_percent': disk.percent,
            'disk_free_gb': disk.free / (1024**3),
            'network_bytes_sent': network.bytes_sent,
            'network_bytes_recv': network.bytes_recv
        }
    
    def monitor_producer_performance(self, producer, duration_seconds=60):
        """Monitor producer performance metrics"""
        start_time = time.time()
        message_count = 0
        error_count = 0
        
        def send_callback(record_metadata):
            nonlocal message_count
            message_count += 1
        
        def error_callback(exception):
            nonlocal error_count
            error_count += 1
            print(f"Producer error: {exception}")
        
        # Send test messages
        while time.time() - start_time < duration_seconds:
            try:
                message = {
                    'timestamp': time.time(),
                    'data': f'test_message_{message_count}'
                }
                
                future = producer.send('performance_test', value=message)
                future.add_callback(send_callback)
                future.add_errback(error_callback)
                
                time.sleep(0.01)  # 100 messages per second
                
            except Exception as e:
                error_count += 1
                print(f"Send error: {e}")
        
        # Wait for pending sends
        producer.flush()
        
        duration = time.time() - start_time
        throughput = message_count / duration
        error_rate = error_count / (message_count + error_count) if (message_count + error_count) > 0 else 0
        
        return {
            'duration_seconds': duration,
            'messages_sent': message_count,
            'errors': error_count,
            'throughput_msg_per_sec': throughput,
            'error_rate_percent': error_rate * 100
        }
    
    def comprehensive_health_check(self):
        """Comprehensive Kafka cluster health check"""
        health_report = {
            'timestamp': time.time(),
            'broker_metrics': self.get_broker_metrics(),
            'cluster_metadata': {},
            'topic_health': {}
        }
        
        try:
            # Get cluster metadata
            metadata = self.admin_client.describe_cluster()
            health_report['cluster_metadata'] = {
                'cluster_id': metadata.cluster_id,
                'controller': metadata.controller.id if metadata.controller else None,
                'broker_count': len(metadata.brokers)
            }
            
            # Check topic configurations
            consumer = KafkaConsumer(bootstrap_servers=self.bootstrap_servers)
            topics = consumer.topics()
            
            for topic in list(topics)[:5]:  # Check first 5 topics
                try:
                    partitions = consumer.partitions_for_topic(topic)
                    health_report['topic_health'][topic] = {
                        'partition_count': len(partitions) if partitions else 0,
                        'status': 'healthy' if partitions else 'no_partitions'
                    }
                except Exception as e:
                    health_report['topic_health'][topic] = {
                        'status': 'error',
                        'error': str(e)
                    }
            
            consumer.close()
            
        except Exception as e:
            health_report['cluster_error'] = str(e)
        
        return health_report

# Performance monitoring example
def run_performance_monitoring():
    monitor = KafkaMonitor(['localhost:9092'])
    
    # Create producer for testing
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    print("Starting Kafka performance monitoring...")
    
    # Monitor producer performance
    print("Testing producer performance...")
    producer_metrics = monitor.monitor_producer_performance(producer, 30)
    print(f"Producer throughput: {producer_metrics['throughput_msg_per_sec']:.2f} msg/sec")
    print(f"Error rate: {producer_metrics['error_rate_percent']:.2f}%")
    
    # Check consumer lag
    print("Checking consumer lag...")
    lag_info = monitor.get_consumer_lag('test_group', 'performance_test')
    print(f"Total consumer lag: {lag_info.get('total_lag', 0)} messages")
    
    # Comprehensive health check
    print("Running health check...")
    health = monitor.comprehensive_health_check()
    print(f"Cluster health - Brokers: {health['cluster_metadata'].get('broker_count', 0)}")
    print(f"CPU usage: {health['broker_metrics']['cpu_percent']:.1f}%")
    print(f"Memory usage: {health['broker_metrics']['memory_percent']:.1f}%")
    
    producer.close()

if __name__ == "__main__":
    run_performance_monitoring()
```

## Data Engineering Use Cases

### Q9: How do you implement a real-time data pipeline using Kafka?

**Answer:**
Real-time data pipelines use Kafka as the central nervous system, connecting data sources, processing engines, and destinations with fault-tolerant streaming.

**Code Example:**
```python
from kafka import KafkaProducer, KafkaConsumer
import json
import time
import threading
from datetime import datetime
import pandas as pd
import sqlite3

class RealTimeDataPipeline:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',
            retries=3
        )
        
        # Initialize database for processed data
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for processed data"""
        self.conn = sqlite3.connect('analytics.db', check_same_thread=False)
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS user_metrics (
                user_id INTEGER,
                event_count INTEGER,
                last_activity TIMESTAMP,
                total_value REAL,
                PRIMARY KEY (user_id)
            )
        ''')
        self.conn.commit()
    
    def data_ingestion_layer(self):
        """Simulate data ingestion from various sources"""
        print("Starting data ingestion...")
        
        # Simulate user events
        user_events = [
            {'user_id': 1, 'event': 'login', 'timestamp': time.time()},
            {'user_id': 1, 'event': 'page_view', 'page': '/products', 'timestamp': time.time()},
            {'user_id': 2, 'event': 'purchase', 'amount': 99.99, 'timestamp': time.time()},
            {'user_id': 1, 'event': 'logout', 'timestamp': time.time()},
            {'user_id': 3, 'event': 'signup', 'timestamp': time.time()}
        ]
        
        for event in user_events:
            self.producer.send('raw_events', value=event)
            print(f"Ingested: {event}")
            time.sleep(1)
        
        self.producer.flush()
        print("Data ingestion completed")
    
    def stream_processing_layer(self):
        """Process streaming data and enrich events"""
        print("Starting stream processing...")
        
        consumer = KafkaConsumer(
            'raw_events',
            bootstrap_servers=['localhost:9092'],
            group_id='stream_processor',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest'
        )
        
        for message in consumer:
            event = message.value
            
            # Enrich event with additional data
            enriched_event = self.enrich_event(event)
            
            # Route to appropriate topic based on event type
            if event['event'] in ['purchase', 'signup']:
                self.producer.send('business_events', value=enriched_event)
            else:
                self.producer.send('user_activity', value=enriched_event)
            
            print(f"Processed: {enriched_event}")
            
            # Break after processing some events for demo
            if message.offset > 10:
                break
        
        consumer.close()
        print("Stream processing completed")
    
    def enrich_event(self, event):
        """Enrich events with additional context"""
        enriched = event.copy()
        enriched['processed_at'] = time.time()
        enriched['date'] = datetime.fromtimestamp(event['timestamp']).strftime('%Y-%m-%d')
        
        # Add user segment based on user_id
        if event['user_id'] <= 10:
            enriched['user_segment'] = 'premium'
        else:
            enriched['user_segment'] = 'standard'
        
        return enriched
    
    def analytics_layer(self):
        """Consume processed events and generate analytics"""
        print("Starting analytics processing...")
        
        consumer = KafkaConsumer(
            'business_events',
            'user_activity',
            bootstrap_servers=['localhost:9092'],
            group_id='analytics_processor',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest'
        )
        
        user_metrics = {}
        
        for message in consumer:
            event = message.value
            user_id = event['user_id']
            
            # Update user metrics
            if user_id not in user_metrics:
                user_metrics[user_id] = {
                    'event_count': 0,
                    'total_value': 0.0,
                    'last_activity': event['timestamp']
                }
            
            user_metrics[user_id]['event_count'] += 1
            user_metrics[user_id]['last_activity'] = max(
                user_metrics[user_id]['last_activity'],
                event['timestamp']
            )
            
            if event['event'] == 'purchase':
                user_metrics[user_id]['total_value'] += event.get('amount', 0)
            
            # Update database
            self.update_user_metrics(user_id, user_metrics[user_id])
            
            print(f"Analytics updated for user {user_id}: {user_metrics[user_id]}")
            
            # Break after processing some events for demo
            if message.offset > 5:
                break
        
        consumer.close()
        print("Analytics processing completed")
    
    def update_user_metrics(self, user_id, metrics):
        """Update user metrics in database"""
        self.conn.execute('''
            INSERT OR REPLACE INTO user_metrics 
            (user_id, event_count, last_activity, total_value)
            VALUES (?, ?, ?, ?)
        ''', (
            user_id,
            metrics['event_count'],
            datetime.fromtimestamp(metrics['last_activity']),
            metrics['total_value']
        ))
        self.conn.commit()
    
    def run_pipeline(self):
        """Run the complete data pipeline"""
        print("Starting Real-Time Data Pipeline...")
        
        # Start components in separate threads
        threads = []
        
        # Data ingestion
        ingestion_thread = threading.Thread(target=self.data_ingestion_layer)
        threads.append(ingestion_thread)
        
        # Stream processing (start after small delay)
        processing_thread = threading.Thread(target=lambda: (time.sleep(2), self.stream_processing_layer()))
        threads.append(processing_thread)
        
        # Analytics (start after processing begins)
        analytics_thread = threading.Thread(target=lambda: (time.sleep(4), self.analytics_layer()))
        threads.append(analytics_thread)
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        # Show final results
        self.show_results()
        
        print("Pipeline execution completed")
    
    def show_results(self):
        """Display final analytics results"""
        cursor = self.conn.execute('SELECT * FROM user_metrics')
        results = cursor.fetchall()
        
        print("\n=== Final Analytics Results ===")
        for row in results:
            print(f"User {row[0]}: {row[1]} events, ${row[3]:.2f} total value, last active: {row[2]}")
    
    def cleanup(self):
        """Cleanup resources"""
        self.producer.close()
        self.conn.close()

# Run the pipeline
if __name__ == "__main__":
    pipeline = RealTimeDataPipeline()
    
    try:
        pipeline.run_pipeline()
    finally:
        pipeline.cleanup()
```

---

## Key Takeaways

1. **Distributed Streaming**: Kafka provides fault-tolerant, scalable message streaming
2. **Partitioning Strategy**: Proper partitioning ensures scalability and ordering
3. **Consumer Groups**: Enable parallel processing with automatic load balancing
4. **Delivery Guarantees**: Configure based on requirements (at-most-once, at-least-once, exactly-once)
5. **Performance Tuning**: Optimize batching, compression, and connection settings
6. **Monitoring**: Track lag, throughput, and system metrics for health
7. **Real-time Pipelines**: Central component for event-driven architectures
8. **Fault Tolerance**: Replication and proper configuration ensure reliability