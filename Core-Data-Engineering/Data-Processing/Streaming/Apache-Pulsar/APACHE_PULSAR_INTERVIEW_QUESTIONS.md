# Apache Pulsar Interview Questions & Answers

## 📋 Table of Contents
1. [Basic Concepts](#basic-concepts)
2. [Architecture & Components](#architecture--components)
3. [Messaging Patterns](#messaging-patterns)
4. [Performance & Scalability](#performance--scalability)
5. [Administration & Operations](#administration--operations)
6. [Integration & Ecosystem](#integration--ecosystem)
7. [Real-world Scenarios](#real-world-scenarios)

---

## Basic Concepts

### 1. What is Apache Pulsar and how does it differ from Apache Kafka?

**Answer:**
Apache Pulsar is a cloud-native, distributed messaging and streaming platform designed for high-performance, low-latency messaging with built-in multi-tenancy and geo-replication.

**Key Differences from Kafka:**

| Feature | Apache Pulsar | Apache Kafka |
|---------|---------------|--------------|
| **Architecture** | Layered (Compute + Storage) | Monolithic |
| **Storage** | BookKeeper (separate) | Local disk |
| **Multi-tenancy** | Native support | Limited |
| **Geo-replication** | Built-in | Requires MirrorMaker |
| **Message Ordering** | Per-key ordering | Partition-level |
| **Schema Evolution** | Built-in schema registry | External schema registry |

**Pulsar Advantages:**
```python
# Native multi-tenancy
tenant = "retail"
namespace = "orders"
topic = f"persistent://{tenant}/{namespace}/order-events"

# Built-in schema support
from pulsar.schema import Record, String, Integer

class Order(Record):
    order_id = Integer()
    customer_id = String()
    amount = Integer()

producer = client.create_producer(topic, schema=Order)
```

### 2. Explain Pulsar's layered architecture and its benefits.

**Answer:**
Pulsar uses a layered architecture that separates compute (serving) and storage layers, providing better scalability and operational flexibility.

**Architecture Layers:**

1. **Serving Layer (Brokers):**
   - Handle client connections
   - Manage topic ownership
   - Route messages
   - Stateless and horizontally scalable

2. **Storage Layer (BookKeeper):**
   - Persistent message storage
   - Replication and durability
   - Independent scaling from brokers

3. **Coordination Layer (ZooKeeper):**
   - Metadata management
   - Service discovery
   - Configuration management

**Benefits of Layered Architecture:**
```yaml
# Independent Scaling
brokers:
  - Can scale based on throughput needs
  - No data rebalancing required
  
bookies:
  - Scale based on storage requirements
  - Data remains available during scaling

# Operational Benefits
maintenance:
  - Upgrade brokers without data migration
  - Replace failed nodes without data loss
  - Better resource utilization
```

### 3. What are Pulsar's key messaging concepts?

**Answer:**
Pulsar organizes messaging around several key concepts that provide structure and multi-tenancy.

**Core Concepts:**

1. **Tenant**: Top-level namespace for organizations
2. **Namespace**: Grouping of topics with policies
3. **Topic**: Message destination/source
4. **Subscription**: Consumer group equivalent
5. **Message**: Unit of data with metadata

**Hierarchical Structure:**
```
persistent://tenant/namespace/topic
└── Tenant: retail
    └── Namespace: orders
        └── Topic: order-events
            ├── Subscription: analytics-team
            ├── Subscription: billing-service
            └── Subscription: inventory-service
```

**Topic Types:**
```python
# Persistent topics (default)
persistent_topic = "persistent://retail/orders/order-events"

# Non-persistent topics (in-memory)
non_persistent_topic = "non-persistent://retail/orders/notifications"

# Partitioned topics
partitioned_topic = "persistent://retail/orders/high-volume-orders"
```

---

## Architecture & Components

### 4. Explain the role of BookKeeper in Pulsar's architecture.

**Answer:**
Apache BookKeeper is Pulsar's distributed storage system that provides durable, consistent, and high-performance log storage.

**BookKeeper Components:**

1. **Bookies**: Storage nodes that store ledger entries
2. **Ledgers**: Immutable, append-only log segments
3. **Entries**: Individual messages within ledgers
4. **Metadata Store**: Ledger metadata and bookie information

**How BookKeeper Works:**
```
Message Flow:
Producer → Broker → BookKeeper Ensemble → Multiple Bookies
                                      ↓
                              Acknowledgment Chain
```

**Replication Model:**
```python
# Ensemble configuration
ensemble_size = 3      # Total bookies for ledger
write_quorum = 2       # Bookies to write to
ack_quorum = 2         # Bookies to acknowledge

# Example: E=3, Qw=2, Qa=2
# Message written to 2 out of 3 bookies
# Acknowledged when 2 bookies confirm write
```

**Benefits:**
- **Durability**: Configurable replication
- **Consistency**: Strict ordering guarantees
- **Performance**: Parallel writes to multiple bookies
- **Scalability**: Independent storage scaling

### 5. How does Pulsar handle message routing and load balancing?

**Answer:**
Pulsar uses dynamic topic assignment and intelligent load balancing to distribute topics across brokers efficiently.

**Topic Assignment:**
```python
# Automatic topic assignment
# Pulsar automatically assigns topics to least-loaded brokers

# Manual topic assignment (if needed)
admin = PulsarAdmin("http://localhost:8080")
admin.topics().create_partitioned_topic(
    "persistent://retail/orders/high-volume", 
    num_partitions=8
)
```

**Load Balancing Strategies:**

1. **Least Loaded**: Assign to broker with lowest load
2. **Round Robin**: Distribute evenly across brokers
3. **Consistent Hashing**: Deterministic assignment

**Dynamic Load Balancing:**
```yaml
# Broker load metrics
cpu_usage: 45%
memory_usage: 60%
network_throughput: 100MB/s
topic_count: 150
bundle_count: 75

# Automatic bundle splitting
- When topic becomes hot
- Split into smaller bundles
- Redistribute across brokers
```

**Producer Routing:**
```python
# Key-based routing
producer = client.create_producer(
    "persistent://retail/orders/events",
    message_routing_mode=PartitionsRoutingMode.CustomPartition,
    message_router=lambda msg: hash(msg.partition_key) % num_partitions
)

# Round-robin routing
producer = client.create_producer(
    "persistent://retail/orders/events",
    message_routing_mode=PartitionsRoutingMode.RoundRobinPartition
)
```

### 6. What are Pulsar Functions and how do they work?

**Answer:**
Pulsar Functions provide serverless compute capabilities for stream processing directly within the Pulsar ecosystem.

**Function Characteristics:**
- **Serverless**: No infrastructure management
- **Event-driven**: Triggered by messages
- **Multi-language**: Java, Python, Go support
- **Stateful**: Built-in state management

**Function Example:**
```python
# Python Pulsar Function
from pulsar import Function

class OrderProcessor(Function):
    def process(self, input, context):
        import json
        
        # Parse input message
        order = json.loads(input)
        
        # Business logic
        if order['amount'] > 1000:
            # High-value order processing
            processed_order = {
                'order_id': order['order_id'],
                'status': 'high_value',
                'priority': 'urgent',
                'amount': order['amount']
            }
            
            # Log to context
            context.get_logger().info(f"Processing high-value order: {order['order_id']}")
            
            return json.dumps(processed_order)
        
        return None  # Filter out low-value orders
```

**Function Deployment:**
```bash
# Deploy function
pulsar-admin functions create \
  --py order_processor.py \
  --classname OrderProcessor \
  --inputs persistent://retail/orders/raw \
  --output persistent://retail/orders/processed \
  --name order-processor
```

**Function Types:**
1. **Transformation**: Modify message content
2. **Filtering**: Route based on conditions
3. **Enrichment**: Add external data
4. **Aggregation**: Combine multiple messages

---

## Messaging Patterns

### 7. Explain different subscription types in Pulsar.

**Answer:**
Pulsar supports multiple subscription types to handle different messaging patterns and consumer requirements.

**Subscription Types:**

1. **Exclusive**: Single consumer per subscription
```python
consumer = client.subscribe(
    "persistent://retail/orders/events",
    subscription_name="billing-service",
    subscription_type=SubscriptionType.Exclusive
)
```

2. **Shared**: Multiple consumers, round-robin delivery
```python
consumer = client.subscribe(
    "persistent://retail/orders/events",
    subscription_name="analytics-workers",
    subscription_type=SubscriptionType.Shared
)
```

3. **Failover**: Active-passive consumer setup
```python
consumer = client.subscribe(
    "persistent://retail/orders/events",
    subscription_name="primary-processor",
    subscription_type=SubscriptionType.Failover,
    consumer_name="primary-consumer"
)
```

4. **Key_Shared**: Partition by message key
```python
consumer = client.subscribe(
    "persistent://retail/orders/events",
    subscription_name="customer-processors",
    subscription_type=SubscriptionType.Key_Shared
)
```

**Use Cases:**
| Type | Use Case | Message Ordering | Parallelism |
|------|----------|------------------|-------------|
| Exclusive | Single processor | Full ordering | None |
| Shared | Load balancing | No ordering | High |
| Failover | High availability | Full ordering | Active-passive |
| Key_Shared | Keyed processing | Per-key ordering | High |

### 8. How does Pulsar handle message acknowledgment and retention?

**Answer:**
Pulsar provides flexible acknowledgment mechanisms and retention policies to ensure message delivery and storage management.

**Acknowledgment Types:**

1. **Individual Acknowledgment:**
```python
while True:
    msg = consumer.receive()
    try:
        # Process message
        process_order(msg.data())
        
        # Acknowledge individual message
        consumer.acknowledge(msg)
    except Exception as e:
        # Negative acknowledgment (retry)
        consumer.negative_acknowledge(msg)
```

2. **Cumulative Acknowledgment:**
```python
messages = []
for i in range(10):
    msg = consumer.receive()
    messages.append(msg)

# Process batch
process_batch(messages)

# Acknowledge up to last message
consumer.acknowledge_cumulative(messages[-1])
```

**Retention Policies:**
```python
# Configure retention
admin.namespaces().set_retention(
    "retail/orders",
    RetentionPolicies(
        retention_time_in_minutes=7*24*60,  # 7 days
        retention_size_in_mb=1024*1024      # 1TB
    )
)

# Backlog quotas
admin.namespaces().set_backlog_quota(
    "retail/orders",
    BacklogQuota(
        limit=500*1024*1024*1024,  # 500GB
        policy=RetentionPolicy.producer_exception
    )
)
```

**Message TTL:**
```python
# Producer with TTL
producer = client.create_producer(
    "persistent://retail/orders/events",
    message_routing_mode=PartitionsRoutingMode.RoundRobinPartition
)

# Send message with TTL
producer.send(
    message_data,
    deliver_after=timedelta(minutes=5),  # Delayed delivery
    event_timestamp=int(time.time() * 1000)
)
```

---

## Performance & Scalability

### 9. How do you optimize Pulsar performance for high-throughput scenarios?

**Answer:**
Optimizing Pulsar for high throughput involves tuning multiple components across the entire stack.

**Producer Optimization:**
```python
# Batching configuration
producer = client.create_producer(
    "persistent://retail/orders/high-volume",
    batching_enabled=True,
    batching_max_messages=1000,
    batching_max_publish_delay_ms=10,
    compression_type=CompressionType.LZ4,
    send_timeout_ms=30000
)

# Async sending
def send_callback(res, msg_id):
    if res:
        print(f"Message sent successfully: {msg_id}")
    else:
        print(f"Failed to send message: {res}")

producer.send_async(message_data, callback=send_callback)
```

**Consumer Optimization:**
```python
# Receiver queue and prefetch
consumer = client.subscribe(
    "persistent://retail/orders/high-volume",
    subscription_name="high-throughput-processor",
    consumer_type=ConsumerType.Shared,
    receiver_queue_size=10000,
    max_total_receiver_queue_size_across_partitions=50000
)

# Batch receiving
while True:
    messages = consumer.batch_receive()
    process_batch([msg.data() for msg in messages])
    for msg in messages:
        consumer.acknowledge(msg)
```

**Broker Configuration:**
```yaml
# broker.conf optimizations
managedLedgerDefaultEnsembleSize=3
managedLedgerDefaultWriteQuorum=2
managedLedgerDefaultAckQuorum=2
managedLedgerCacheSizeMB=2048
managedLedgerCacheEvictionWatermark=0.9

# Network and I/O
nettyMaxFrameSizeBytes=5242880
maxMessageSize=5242880
```

**BookKeeper Optimization:**
```yaml
# bookie.conf optimizations
journalMaxSizeMB=2048
ledgerStorageClass=org.apache.bookkeeper.bookie.storage.ldb.DbLedgerStorage
dbStorage_writeCacheMaxSizeMb=512
dbStorage_readAheadCacheMaxSizeMb=256
```

### 10. How does Pulsar handle geo-replication and disaster recovery?

**Answer:**
Pulsar provides built-in geo-replication capabilities for disaster recovery and global data distribution.

**Geo-Replication Setup:**
```bash
# Create clusters
pulsar-admin clusters create \
  --url http://us-west-broker:8080 \
  --broker-url pulsar://us-west-broker:6650 \
  us-west

pulsar-admin clusters create \
  --url http://us-east-broker:8080 \
  --broker-url pulsar://us-east-broker:6650 \
  us-east

# Configure tenant with multiple clusters
pulsar-admin tenants create retail \
  --allowed-clusters us-west,us-east \
  --admin-roles admin
```

**Namespace Replication:**
```bash
# Enable replication for namespace
pulsar-admin namespaces set-clusters retail/orders \
  --clusters us-west,us-east

# Set replication policies
pulsar-admin namespaces set-replication-clusters retail/orders \
  --clusters us-west,us-east
```

**Application Code:**
```python
# Producer in US-West
us_west_client = pulsar.Client("pulsar://us-west-broker:6650")
producer = us_west_client.create_producer(
    "persistent://retail/orders/global-events"
)

# Consumer in US-East (receives replicated messages)
us_east_client = pulsar.Client("pulsar://us-east-broker:6650")
consumer = us_east_client.subscribe(
    "persistent://retail/orders/global-events",
    subscription_name="us-east-processor"
)
```

**Disaster Recovery Strategies:**
1. **Active-Active**: Both regions process messages
2. **Active-Passive**: Failover to secondary region
3. **Multi-Master**: Independent processing with sync

---

## Administration & Operations

### 11. How do you monitor and troubleshoot Pulsar clusters?

**Answer:**
Effective monitoring and troubleshooting require understanding Pulsar's metrics, logs, and diagnostic tools.

**Key Metrics to Monitor:**

1. **Broker Metrics:**
```bash
# Broker health check
curl http://broker:8080/admin/v2/brokers/health

# Topic statistics
pulsar-admin topics stats persistent://retail/orders/events

# Broker load
pulsar-admin brokers list-dynamic-configuration
```

2. **BookKeeper Metrics:**
```bash
# Bookie health
curl http://bookie:8000/heartbeat

# Ledger information
curl http://bookie:8000/api/v1/ledger/list
```

**Monitoring Setup:**
```yaml
# Prometheus configuration
- job_name: 'pulsar-broker'
  static_configs:
    - targets: ['broker1:8080', 'broker2:8080']
  metrics_path: /metrics

- job_name: 'pulsar-bookie'
  static_configs:
    - targets: ['bookie1:8000', 'bookie2:8000']
  metrics_path: /metrics
```

**Common Issues and Solutions:**

1. **High Latency:**
```bash
# Check broker load
pulsar-admin brokers monitoring-metrics

# Analyze topic backlog
pulsar-admin topics stats-internal persistent://retail/orders/events

# Solution: Scale brokers or optimize consumers
```

2. **Message Backlog:**
```bash
# Check subscription backlog
pulsar-admin topics subscriptions persistent://retail/orders/events

# Reset subscription position
pulsar-admin topics reset-cursor \
  persistent://retail/orders/events \
  --subscription analytics-team \
  --time 2023-01-01T00:00:00Z
```

### 12. How do you perform Pulsar cluster upgrades and maintenance?

**Answer:**
Pulsar's layered architecture enables rolling upgrades with minimal downtime.

**Upgrade Strategy:**

1. **BookKeeper Upgrade (Storage Layer):**
```bash
# Upgrade bookies one by one
# 1. Stop bookie
systemctl stop bookkeeper

# 2. Upgrade software
# Install new version

# 3. Start bookie
systemctl start bookkeeper

# 4. Verify bookie health
curl http://bookie:8000/heartbeat
```

2. **Broker Upgrade (Serving Layer):**
```bash
# Rolling broker upgrade
# 1. Drain broker traffic
pulsar-admin brokers update-dynamic-config \
  --config loadBalancerEnabled \
  --value false

# 2. Stop broker
systemctl stop pulsar-broker

# 3. Upgrade and restart
systemctl start pulsar-broker

# 4. Re-enable load balancing
pulsar-admin brokers update-dynamic-config \
  --config loadBalancerEnabled \
  --value true
```

**Maintenance Best Practices:**
```yaml
pre_upgrade:
  - Backup ZooKeeper metadata
  - Document current configuration
  - Test upgrade in staging environment
  - Plan rollback strategy

during_upgrade:
  - Monitor cluster health
  - Verify message flow
  - Check consumer lag
  - Monitor error rates

post_upgrade:
  - Validate all services
  - Run integration tests
  - Monitor for 24 hours
  - Update documentation
```

---

## Integration & Ecosystem

### 13. How do you integrate Pulsar with Apache Spark for stream processing?

**Answer:**
Pulsar integrates with Spark through connectors for both batch and streaming processing.

**Spark Streaming Integration:**
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Create Spark session
spark = SparkSession.builder \
    .appName("PulsarSparkStreaming") \
    .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoint") \
    .getOrCreate()

# Define schema
order_schema = StructType([
    StructField("order_id", StringType(), True),
    StructField("customer_id", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("timestamp", TimestampType(), True)
])

# Read from Pulsar
df = spark \
    .readStream \
    .format("pulsar") \
    .option("service.url", "pulsar://localhost:6650") \
    .option("admin.url", "http://localhost:8080") \
    .option("topic", "persistent://retail/orders/events") \
    .load()

# Process messages
processed_df = df \
    .select(from_json(col("value").cast("string"), order_schema).alias("order")) \
    .select("order.*") \
    .withWatermark("timestamp", "10 minutes") \
    .groupBy(
        window(col("timestamp"), "5 minutes"),
        col("customer_id")
    ) \
    .agg(
        sum("amount").alias("total_amount"),
        count("*").alias("order_count")
    )

# Write results back to Pulsar
query = processed_df \
    .selectExpr("to_json(struct(*)) AS value") \
    .writeStream \
    .format("pulsar") \
    .option("service.url", "pulsar://localhost:6650") \
    .option("admin.url", "http://localhost:8080") \
    .option("topic", "persistent://retail/analytics/customer-summary") \
    .outputMode("update") \
    .start()

query.awaitTermination()
```

### 14. How do you implement schema evolution in Pulsar?

**Answer:**
Pulsar provides built-in schema registry and evolution capabilities to handle changing data structures.

**Schema Definition:**
```python
from pulsar.schema import Record, String, Integer, Float, Boolean

# Initial schema version
class OrderV1(Record):
    order_id = String()
    customer_id = String()
    amount = Float()

# Evolved schema (backward compatible)
class OrderV2(Record):
    order_id = String()
    customer_id = String()
    amount = Float()
    currency = String(default="USD")  # New field with default
    priority = Boolean(default=False)  # New field with default
```

**Schema Evolution Types:**
```python
# Producer with schema evolution
producer = client.create_producer(
    "persistent://retail/orders/events",
    schema=OrderV2
)

# Consumer with schema compatibility
consumer = client.subscribe(
    "persistent://retail/orders/events",
    subscription_name="order-processor",
    schema=OrderV2,
    schema_compatibility_check=True
)
```

**Schema Management:**
```bash
# Upload schema
pulsar-admin schemas upload \
  persistent://retail/orders/events \
  --filename order_schema_v2.json

# Get schema info
pulsar-admin schemas get persistent://retail/orders/events

# Schema compatibility check
pulsar-admin schemas compatibility-check \
  persistent://retail/orders/events \
  --filename new_schema.json
```

**Evolution Strategies:**
1. **Backward Compatible**: New consumers can read old messages
2. **Forward Compatible**: Old consumers can read new messages
3. **Full Compatible**: Both backward and forward compatible

---

## Real-world Scenarios

### 15. Design a real-time analytics pipeline using Pulsar for an e-commerce platform.

**Answer:**
A comprehensive real-time analytics pipeline handling multiple event types with different processing requirements.

**Architecture Overview:**
```
Web App → Pulsar → [Functions] → Analytics DB
Mobile App ↗     ↓
                Spark Streaming → Data Lake
                ↓
                ML Models → Recommendations
```

**Implementation:**

1. **Event Ingestion:**
```python
# Event producer service
class EventProducer:
    def __init__(self):
        self.client = pulsar.Client("pulsar://localhost:6650")
        self.producers = {
            'page_views': self.client.create_producer(
                "persistent://ecommerce/analytics/page-views",
                schema=PageViewSchema
            ),
            'purchases': self.client.create_producer(
                "persistent://ecommerce/analytics/purchases",
                schema=PurchaseSchema
            ),
            'cart_events': self.client.create_producer(
                "persistent://ecommerce/analytics/cart-events",
                schema=CartEventSchema
            )
        }
    
    def send_page_view(self, user_id, page, timestamp):
        event = PageView(
            user_id=user_id,
            page=page,
            timestamp=timestamp,
            session_id=generate_session_id()
        )
        self.producers['page_views'].send(event)
    
    def send_purchase(self, user_id, order_id, items, total):
        event = Purchase(
            user_id=user_id,
            order_id=order_id,
            items=items,
            total=total,
            timestamp=int(time.time() * 1000)
        )
        self.producers['purchases'].send(event)
```

2. **Real-time Processing Functions:**
```python
# Session aggregation function
class SessionAggregator(Function):
    def process(self, input, context):
        page_view = json.loads(input)
        
        # Get or create session state
        session_key = f"session:{page_view['session_id']}"
        session_data = context.get_state(session_key) or {
            'page_count': 0,
            'start_time': page_view['timestamp'],
            'pages': []
        }
        
        # Update session
        session_data['page_count'] += 1
        session_data['pages'].append(page_view['page'])
        session_data['last_activity'] = page_view['timestamp']
        
        # Store updated state
        context.put_state(session_key, session_data)
        
        # Emit session update
        return json.dumps({
            'session_id': page_view['session_id'],
            'user_id': page_view['user_id'],
            'duration': session_data['last_activity'] - session_data['start_time'],
            'page_count': session_data['page_count'],
            'pages': session_data['pages']
        })
```

3. **Stream Processing with Spark:**
```python
# Real-time recommendations
def process_recommendations():
    # Read purchase events
    purchases_df = spark \
        .readStream \
        .format("pulsar") \
        .option("service.url", "pulsar://localhost:6650") \
        .option("topic", "persistent://ecommerce/analytics/purchases") \
        .load()
    
    # Process for recommendations
    recommendations_df = purchases_df \
        .select(from_json(col("value").cast("string"), purchase_schema).alias("purchase")) \
        .select("purchase.*") \
        .withWatermark("timestamp", "1 hour") \
        .groupBy(
            window(col("timestamp"), "10 minutes"),
            col("user_id")
        ) \
        .agg(
            collect_list("items").alias("recent_items"),
            sum("total").alias("total_spent")
        )
    
    # Generate recommendations and send back to Pulsar
    query = recommendations_df \
        .writeStream \
        .foreachBatch(generate_and_send_recommendations) \
        .outputMode("update") \
        .start()
    
    return query
```

### 16. How would you handle a scenario where you need to process 1 million messages per second with Pulsar?

**Answer:**
Processing 1M messages/second requires careful architecture design and optimization across all components.

**Scaling Strategy:**

1. **Cluster Sizing:**
```yaml
# Recommended cluster configuration
brokers: 12-15 nodes
bookies: 15-20 nodes
zookeeper: 5 nodes (dedicated)

# Hardware specifications
broker_specs:
  cpu: 16+ cores
  memory: 64GB+
  network: 10Gbps+
  
bookie_specs:
  cpu: 8+ cores
  memory: 32GB+
  storage: NVMe SSD
  network: 10Gbps+
```

2. **Topic Partitioning:**
```python
# Create highly partitioned topics
admin.topics().create_partitioned_topic(
    "persistent://high-volume/events/user-actions",
    num_partitions=100
)

# Distribute producers across partitions
producers = []
for i in range(10):  # 10 producer instances
    producer = client.create_producer(
        "persistent://high-volume/events/user-actions",
        batching_enabled=True,
        batching_max_messages=1000,
        batching_max_publish_delay_ms=1,
        compression_type=CompressionType.LZ4
    )
    producers.append(producer)
```

3. **Consumer Scaling:**
```python
# Shared subscription with many consumers
consumers = []
for i in range(50):  # 50 consumer instances
    consumer = client.subscribe(
        "persistent://high-volume/events/user-actions",
        subscription_name="high-throughput-processors",
        subscription_type=SubscriptionType.Shared,
        receiver_queue_size=10000,
        consumer_name=f"consumer-{i}"
    )
    consumers.append(consumer)

# Async processing
async def process_messages(consumer):
    while True:
        try:
            messages = await consumer.batch_receive_async()
            await process_batch_async(messages)
            for msg in messages:
                consumer.acknowledge(msg)
        except Exception as e:
            logger.error(f"Processing error: {e}")
```

4. **Performance Monitoring:**
```python
# Metrics collection
class PerformanceMonitor:
    def __init__(self):
        self.message_count = 0
        self.start_time = time.time()
        self.last_report = time.time()
    
    def record_message(self):
        self.message_count += 1
        
        current_time = time.time()
        if current_time - self.last_report >= 10:  # Report every 10 seconds
            elapsed = current_time - self.start_time
            rate = self.message_count / elapsed
            
            print(f"Processing rate: {rate:.2f} messages/second")
            print(f"Total processed: {self.message_count}")
            
            self.last_report = current_time
```

**Expected Performance:**
- **Throughput**: 1M+ messages/second
- **Latency**: <10ms end-to-end
- **Availability**: 99.99%
- **Durability**: Configurable replication

---

## Summary

Apache Pulsar is a modern messaging platform that addresses many limitations of traditional systems. Key areas to master:

1. **Architecture Understanding**: Layered design and component interactions
2. **Messaging Patterns**: Subscription types and delivery semantics
3. **Performance Optimization**: Scaling strategies and tuning parameters
4. **Operations**: Monitoring, troubleshooting, and maintenance
5. **Integration**: Ecosystem connectivity and stream processing
6. **Real-world Applications**: High-throughput, low-latency scenarios

Understanding these concepts will help you effectively leverage Pulsar for modern streaming architectures.