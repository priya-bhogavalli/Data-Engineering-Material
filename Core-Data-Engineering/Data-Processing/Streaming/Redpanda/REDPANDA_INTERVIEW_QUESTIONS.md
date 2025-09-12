# Redpanda - Comprehensive Interview Questions

## Table of Contents
1. [Core Concepts](#core-concepts)
2. [Architecture & Performance](#architecture--performance)
3. [Kafka Compatibility](#kafka-compatibility)
4. [Configuration & Deployment](#configuration--deployment)
5. [Monitoring & Operations](#monitoring--operations)
6. [Security & Compliance](#security--compliance)
7. [Performance Optimization](#performance-optimization)
8. [Real-World Scenarios](#real-world-scenarios)

---

## Core Concepts

### 1. What is Redpanda and how does it differ from Apache Kafka?

**Answer:**
Redpanda is a modern streaming platform that's Kafka-compatible but built from scratch in C++ for better performance and operational simplicity.

**Key Differences:**

| Aspect | Apache Kafka | Redpanda |
|--------|--------------|----------|
| **Language** | Java/Scala | C++ |
| **Dependencies** | Requires ZooKeeper | No external dependencies |
| **Latency** | ~2-5ms | Sub-millisecond |
| **Memory Usage** | High (JVM overhead) | Low (native binary) |
| **Operational Complexity** | High | Low |
| **Compatibility** | Native Kafka | Kafka API compatible |

**Performance Benefits:**
```bash
# Kafka typical latency
P99 latency: 5-10ms
Throughput: 1M msgs/sec per broker

# Redpanda typical latency  
P99 latency: <1ms
Throughput: 10M+ msgs/sec per broker
```

### 2. Explain Redpanda's architecture and how it achieves low latency.

**Answer:**
**Architecture Components:**

1. **Raft Consensus**: Built-in consensus without ZooKeeper
2. **Seastar Framework**: Async I/O and CPU scheduling
3. **Thread-per-Core**: Eliminates context switching
4. **Zero-Copy I/O**: Direct memory access
5. **Vectorized Processing**: SIMD optimizations

**Low Latency Techniques:**
```cpp
// Thread-per-core architecture
class redpanda_core {
    // Each core runs independently
    seastar::reactor core_reactor;
    
    // No shared state between cores
    thread_local partition_manager partitions;
    
    // Zero-copy message handling
    seastar::future<> handle_produce(message_batch batch) {
        return write_to_log(std::move(batch))  // No copying
            .then([](auto result) {
                return send_response(result);
            });
    }
};

// Vectorized batch processing
void process_message_batch(const std::vector<message>& batch) {
    // Process multiple messages simultaneously
    for (size_t i = 0; i < batch.size(); i += VECTOR_SIZE) {
        process_vector(batch.data() + i, VECTOR_SIZE);
    }
}
```

### 3. How does Redpanda handle consensus without ZooKeeper?

**Answer:**
**Built-in Raft Consensus:**

Redpanda uses the Raft consensus algorithm for:
- Leader election
- Metadata management
- Configuration changes
- Partition management

**Raft Implementation:**
```python
# Simplified Raft concepts in Redpanda
class RaftNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.state = "follower"  # follower, candidate, leader
        self.current_term = 0
        self.voted_for = None
        self.log = []
    
    def start_election(self):
        self.state = "candidate"
        self.current_term += 1
        self.voted_for = self.node_id
        
        # Request votes from other nodes
        votes = self.request_votes()
        
        if votes > len(self.cluster) // 2:
            self.state = "leader"
            self.send_heartbeats()
    
    def append_entries(self, entries):
        # Leader replicates entries to followers
        for follower in self.followers:
            follower.replicate(entries)
```

**Benefits over ZooKeeper:**
- Fewer moving parts
- Lower operational overhead
- Faster metadata operations
- Built-in high availability

### 4. What is the Seastar framework and how does Redpanda use it?

**Answer:**
**Seastar Framework** is a high-performance async application framework that Redpanda uses for:

**Key Features:**
1. **Thread-per-Core**: Each CPU core runs independently
2. **Async I/O**: Non-blocking operations
3. **Zero-Copy**: Direct memory access
4. **NUMA-Aware**: Optimized for modern hardware

**Implementation:**
```cpp
// Seastar-based message handling
seastar::future<produce_response> 
handle_produce_request(produce_request req) {
    return seastar::with_scheduling_group(
        redpanda_scheduling_group, [req = std::move(req)] {
            // Process on dedicated core
            return partition_manager::instance()
                .get_partition(req.topic, req.partition)
                .then([req](auto partition) {
                    return partition->append(req.records);
                });
        });
}

// Memory management
class message_buffer {
    seastar::temporary_buffer<char> data;
    
public:
    // Zero-copy construction
    message_buffer(seastar::temporary_buffer<char> buf) 
        : data(std::move(buf)) {}
    
    // Direct memory access
    const char* get_data() const { return data.get(); }
    size_t size() const { return data.size(); }
};
```

### 5. How does Redpanda achieve Kafka API compatibility?

**Answer:**
**Compatibility Layers:**

1. **Protocol Compatibility**: Implements Kafka wire protocol
2. **Client Compatibility**: Works with existing Kafka clients
3. **Admin API**: Compatible with Kafka admin operations
4. **Consumer Groups**: Full consumer group protocol support

**API Implementation:**
```python
# Kafka client works seamlessly with Redpanda
from kafka import KafkaProducer, KafkaConsumer

# Producer - no code changes needed
producer = KafkaProducer(
    bootstrap_servers=['redpanda-broker:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

producer.send('my-topic', {'message': 'Hello Redpanda'})

# Consumer - identical to Kafka
consumer = KafkaConsumer(
    'my-topic',
    bootstrap_servers=['redpanda-broker:9092'],
    group_id='my-consumer-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    print(f"Received: {message.value}")
```

**Supported Kafka Features:**
- Producer/Consumer APIs
- Kafka Streams compatibility
- Kafka Connect integration
- Schema Registry support
- SASL/SSL authentication

---

## Architecture & Performance

### 6. How do you benchmark Redpanda performance compared to Kafka?

**Answer:**
**Benchmarking Setup:**

```bash
# Redpanda performance test
rpk topic create benchmark-topic --partitions 12 --replicas 3

# Producer benchmark
rpk topic produce benchmark-topic \
    --brokers redpanda-cluster:9092 \
    --batch-size 1000 \
    --throughput 100000 \
    --record-size 1024

# Consumer benchmark  
rpk topic consume benchmark-topic \
    --brokers redpanda-cluster:9092 \
    --group benchmark-group \
    --offset earliest
```

**Performance Comparison:**
```python
# Benchmark results comparison
benchmark_results = {
    "kafka": {
        "p99_latency_ms": 8.5,
        "throughput_msgs_sec": 850000,
        "cpu_usage_percent": 75,
        "memory_usage_gb": 4.2
    },
    "redpanda": {
        "p99_latency_ms": 0.8,
        "throughput_msgs_sec": 2100000,
        "cpu_usage_percent": 45,
        "memory_usage_gb": 1.8
    }
}

# Performance improvement
latency_improvement = (
    benchmark_results["kafka"]["p99_latency_ms"] / 
    benchmark_results["redpanda"]["p99_latency_ms"]
)  # ~10x improvement

throughput_improvement = (
    benchmark_results["redpanda"]["throughput_msgs_sec"] / 
    benchmark_results["kafka"]["throughput_msgs_sec"]
)  # ~2.5x improvement
```

### 7. What are Redpanda's resource requirements and scaling characteristics?

**Answer:**
**Resource Requirements:**

```yaml
# Minimum requirements
minimum_specs:
  cpu_cores: 2
  memory_gb: 4
  storage_gb: 100
  network_gbps: 1

# Production recommendations
production_specs:
  cpu_cores: 16+
  memory_gb: 32+
  storage_type: NVMe SSD
  storage_gb: 1000+
  network_gbps: 10+
```

**Scaling Patterns:**
```python
# Horizontal scaling
def scale_redpanda_cluster():
    # Add new brokers
    new_brokers = [
        "redpanda-4.cluster.local:9092",
        "redpanda-5.cluster.local:9092"
    ]
    
    # Automatic partition rebalancing
    for broker in new_brokers:
        add_broker_to_cluster(broker)
        trigger_partition_rebalance()
    
    # Monitor rebalancing progress
    while rebalancing_in_progress():
        monitor_cluster_health()
        time.sleep(30)

# Vertical scaling considerations
scaling_guidelines = {
    "cpu_scaling": "Linear improvement up to 32 cores",
    "memory_scaling": "Diminishing returns after 64GB",
    "storage_scaling": "NVMe provides 10x improvement over HDD",
    "network_scaling": "Bottleneck at 25Gbps+ throughput"
}
```

---

## Configuration & Deployment

### 8. How do you deploy and configure a Redpanda cluster?

**Answer:**
**Docker Deployment:**

```yaml
# docker-compose.yml
version: '3.8'
services:
  redpanda-1:
    image: redpandadata/redpanda:latest
    container_name: redpanda-1
    command:
      - redpanda
      - start
      - --node-id=1
      - --kafka-addr=PLAINTEXT://0.0.0.0:9092
      - --advertise-kafka-addr=PLAINTEXT://redpanda-1:9092
      - --pandaproxy-addr=0.0.0.0:8082
      - --advertise-pandaproxy-addr=redpanda-1:8082
      - --rpc-addr=0.0.0.0:33145
      - --advertise-rpc-addr=redpanda-1:33145
      - --seeds=redpanda-1:33145,redpanda-2:33145,redpanda-3:33145
    ports:
      - "9092:9092"
      - "8082:8082"
    volumes:
      - redpanda-1-data:/var/lib/redpanda/data

  redpanda-2:
    image: redpandadata/redpanda:latest
    container_name: redpanda-2
    command:
      - redpanda
      - start
      - --node-id=2
      - --kafka-addr=PLAINTEXT://0.0.0.0:9092
      - --advertise-kafka-addr=PLAINTEXT://redpanda-2:9092
      - --seeds=redpanda-1:33145,redpanda-2:33145,redpanda-3:33145
    ports:
      - "9093:9092"

volumes:
  redpanda-1-data:
  redpanda-2-data:
  redpanda-3-data:
```

**Kubernetes Deployment:**
```yaml
# redpanda-cluster.yaml
apiVersion: cluster.redpanda.com/v1alpha1
kind: Cluster
metadata:
  name: redpanda-cluster
spec:
  image: "redpandadata/redpanda"
  version: "latest"
  replicas: 3
  resources:
    requests:
      cpu: 2
      memory: 4Gi
    limits:
      cpu: 4
      memory: 8Gi
  storage:
    capacity: 100Gi
    storageClassName: fast-ssd
  configuration:
    kafka_api:
      - address: "0.0.0.0"
        port: 9092
    admin_api:
      - address: "0.0.0.0"
        port: 9644
    rpc_server:
      address: "0.0.0.0"
      port: 33145
```

### 9. What are the key configuration parameters for Redpanda optimization?

**Answer:**
**Performance Configuration:**

```yaml
# redpanda.yaml
redpanda:
  # Core performance settings
  developer_mode: false
  
  # Memory settings
  memory: 8GB
  reserve_memory: 1GB
  
  # CPU settings
  smp: 8  # Number of cores to use
  
  # Storage settings
  data_directory: /var/lib/redpanda/data
  
  # Network settings
  kafka_api:
    - address: 0.0.0.0
      port: 9092
  
  # Replication settings
  default_topic_replications: 3
  min_version: 0
  
  # Batch settings
  batch_max_bytes: 1048576  # 1MB
  max_compacted_log_segment_size: 134217728  # 128MB
  
  # Retention settings
  log_retention_bytes: 1073741824  # 1GB
  log_retention_ms: 604800000  # 7 days
  
  # Compaction settings
  log_compaction_interval_ms: 10000
  compacted_log_segment_size: 134217728
```

**Tuning Parameters:**
```python
# Performance tuning guide
tuning_parameters = {
    "high_throughput": {
        "batch_max_bytes": 16777216,  # 16MB
        "linger_ms": 100,
        "compression_type": "lz4",
        "acks": 1
    },
    "low_latency": {
        "batch_max_bytes": 1024,  # 1KB
        "linger_ms": 0,
        "compression_type": "none",
        "acks": 1
    },
    "balanced": {
        "batch_max_bytes": 1048576,  # 1MB
        "linger_ms": 10,
        "compression_type": "snappy",
        "acks": 1
    }
}
```

---

## Monitoring & Operations

### 10. How do you monitor Redpanda cluster health and performance?

**Answer:**
**Monitoring Tools:**

1. **rpk (Redpanda CLI)**: Built-in monitoring commands
2. **Prometheus Metrics**: Native metrics export
3. **Grafana Dashboards**: Visualization
4. **Admin API**: REST API for monitoring

**Monitoring Commands:**
```bash
# Cluster status
rpk cluster info

# Topic metrics
rpk topic list
rpk topic describe my-topic

# Consumer group monitoring
rpk group list
rpk group describe my-consumer-group

# Partition status
rpk topic partitions my-topic

# Performance metrics
rpk cluster logdirs describe
```

**Prometheus Integration:**
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'redpanda'
    static_configs:
      - targets: ['redpanda-1:9644', 'redpanda-2:9644', 'redpanda-3:9644']
    metrics_path: /metrics
    scrape_interval: 30s
```

**Key Metrics to Monitor:**
```python
key_metrics = {
    "throughput": [
        "redpanda_kafka_request_bytes_total",
        "redpanda_kafka_request_latency_seconds"
    ],
    "storage": [
        "redpanda_storage_log_size_bytes",
        "redpanda_storage_log_segments_total"
    ],
    "replication": [
        "redpanda_cluster_partition_under_replicated_replicas",
        "redpanda_raft_recovery_partition_movement_available_bandwidth"
    ],
    "consumer_lag": [
        "redpanda_kafka_consumer_lag_sum",
        "redpanda_kafka_consumer_lag_max"
    ]
}
```

### 11. How do you handle Redpanda cluster maintenance and upgrades?

**Answer:**
**Rolling Upgrade Process:**

```bash
# 1. Check cluster health
rpk cluster health

# 2. Upgrade one node at a time
for node in redpanda-1 redpanda-2 redpanda-3; do
    echo "Upgrading $node"
    
    # Graceful shutdown
    rpk cluster maintenance enable $node
    
    # Wait for partition leadership migration
    sleep 30
    
    # Stop the node
    systemctl stop redpanda
    
    # Update binary/container
    update_redpanda_binary
    
    # Start the node
    systemctl start redpanda
    
    # Wait for node to rejoin
    wait_for_node_ready $node
    
    # Disable maintenance mode
    rpk cluster maintenance disable $node
    
    # Verify cluster health
    rpk cluster health
done
```

**Backup and Recovery:**
```bash
# Backup topic data
rpk topic create backup-topic --config cleanup.policy=compact
rpk topic produce backup-topic < original-topic-data.json

# Backup cluster metadata
rpk cluster config export > cluster-config-backup.yaml

# Recovery process
rpk cluster config import cluster-config-backup.yaml
rpk topic consume backup-topic > recovered-data.json
```

---

## Real-World Scenarios

### 12. Design a high-throughput event streaming architecture using Redpanda.

**Answer:**
**Architecture:**
```
Event Sources → Load Balancer → Redpanda Cluster → Stream Processors → Destinations
     ↓              ↓              ↓                    ↓               ↓
Web Apps → HAProxy → 3-node → Kafka Streams → Analytics DB
IoT Devices        → Cluster → Flink Jobs   → Data Lake
APIs                        → Custom Apps  → Real-time Dashboard
```

**Implementation:**
```python
# High-throughput producer
from kafka import KafkaProducer
import json
import asyncio

class HighThroughputProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=['redpanda-1:9092', 'redpanda-2:9092', 'redpanda-3:9092'],
            batch_size=65536,  # 64KB batches
            linger_ms=10,      # Small batching delay
            compression_type='lz4',
            acks=1,            # Leader acknowledgment only
            retries=3,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    
    async def send_events(self, events):
        futures = []
        for event in events:
            future = self.producer.send('high-throughput-topic', event)
            futures.append(future)
        
        # Wait for all sends to complete
        await asyncio.gather(*[self.wait_for_future(f) for f in futures])
    
    async def wait_for_future(self, future):
        return future.get(timeout=10)

# Stream processing with Kafka Streams
stream_processing_topology = """
StreamsBuilder builder = new StreamsBuilder();

KStream<String, Event> events = builder.stream("high-throughput-topic");

// Real-time aggregations
KTable<String, Long> eventCounts = events
    .groupByKey()
    .windowedBy(TimeWindows.of(Duration.ofMinutes(1)))
    .count();

// Anomaly detection
KStream<String, Alert> alerts = events
    .filter((key, event) -> isAnomalous(event))
    .mapValues(event -> createAlert(event));

// Output streams
eventCounts.toStream().to("metrics-topic");
alerts.to("alerts-topic");
"""
```

### 13. How would you migrate from Kafka to Redpanda with zero downtime?

**Answer:**
**Migration Strategy:**

```python
# Phase 1: Dual-write setup
class DualWriteProducer:
    def __init__(self):
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=['kafka-1:9092', 'kafka-2:9092']
        )
        self.redpanda_producer = KafkaProducer(
            bootstrap_servers=['redpanda-1:9092', 'redpanda-2:9092']
        )
    
    def send_message(self, topic, message):
        # Send to both systems
        kafka_future = self.kafka_producer.send(topic, message)
        redpanda_future = self.redpanda_producer.send(topic, message)
        
        # Wait for both to succeed
        kafka_future.get(timeout=10)
        redpanda_future.get(timeout=10)

# Phase 2: Consumer migration
class MigrationConsumer:
    def __init__(self, phase="kafka"):
        if phase == "kafka":
            self.consumer = KafkaConsumer(
                bootstrap_servers=['kafka-1:9092']
            )
        elif phase == "redpanda":
            self.consumer = KafkaConsumer(
                bootstrap_servers=['redpanda-1:9092']
            )
        elif phase == "dual":
            # Read from both and deduplicate
            self.kafka_consumer = KafkaConsumer(
                bootstrap_servers=['kafka-1:9092']
            )
            self.redpanda_consumer = KafkaConsumer(
                bootstrap_servers=['redpanda-1:9092']
            )
    
    def consume_with_deduplication(self):
        seen_messages = set()
        
        for message in self.consumer:
            message_id = generate_message_id(message)
            if message_id not in seen_messages:
                seen_messages.add(message_id)
                yield message

# Phase 3: Complete migration
migration_phases = {
    "phase_1": "Setup Redpanda cluster and dual-write",
    "phase_2": "Migrate consumers one by one",
    "phase_3": "Switch producers to Redpanda-only",
    "phase_4": "Decommission Kafka cluster"
}
```

This comprehensive set of Redpanda interview questions covers all essential aspects from core concepts to real-world migration scenarios, highlighting its performance advantages and Kafka compatibility.