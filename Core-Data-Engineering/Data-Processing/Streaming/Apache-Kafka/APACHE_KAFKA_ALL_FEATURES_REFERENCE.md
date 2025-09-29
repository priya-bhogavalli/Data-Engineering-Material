# Apache Kafka All Features Reference

## 🎯 Overview
Comprehensive reference for Apache Kafka features, APIs, deployment modes, performance tuning, and ecosystem integrations for distributed streaming platforms.

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Legend](#-legend)
3. [Core Components & Features](#️-core-components--features)
4. [Client APIs](#-client-apis)
5. [Deployment Modes Comparison](#-deployment-modes-comparison)
6. [Data Formats & Serialization](#-data-formats--serialization)
7. [Performance Optimization Features](#-performance-optimization-features)
8. [Configuration Categories](#-configuration-categories)
9. [Ecosystem Integrations](#-ecosystem-integrations)
10. [Performance Benchmarks & Limits](#-performance-benchmarks--limits)
11. [Monitoring & Debugging](#-monitoring--debugging)
12. [Common Issues & Solutions](#-common-issues--solutions)
13. [Version Compatibility](#-version-compatibility)
14. [Quick Reference Commands](#-quick-reference-commands)
15. [Related Resources](#-related-resources)

## 📍 Legend

### Component Status
- 🟢 **Stable** - Production-ready, fully supported
- 🟡 **Experimental** - Available but may change
- 🔴 **Alpha** - Early development, use with caution
- ⚫ **Deprecated** - Being phased out

### API Types
- **Producer** - Data publishing API
- **Consumer** - Data consumption API
- **Streams** - Stream processing API
- **Connect** - Integration framework
- **Admin** - Cluster management API

## 🏗️ Core Components & Features

| Component | Status | Description | Primary Use Cases | Key Features | Performance Notes |
|-----------|--------|-------------|-------------------|--------------|-------------------|
| **Kafka Broker** | 🟢 | Message storage and serving | Data persistence, replication | Log-based storage, partitioning | Optimized for sequential I/O |
| **ZooKeeper** | 🟢 | Cluster coordination | Metadata management, leader election | Consensus protocol, configuration | Being replaced by KRaft |
| **KRaft (Kafka Raft)** | 🟡 | Self-managed metadata | ZooKeeper replacement | Built-in consensus, simplified ops | Improved performance, fewer dependencies |
| **Producer API** | 🟢 | Data publishing | Event streaming, log aggregation | Async/sync publishing, batching | High throughput, configurable reliability |
| **Consumer API** | 🟢 | Data consumption | Stream processing, analytics | Consumer groups, offset management | Scalable consumption, fault tolerance |
| **Streams API** | 🟢 | Stream processing | Real-time analytics, transformations | Stateful/stateless processing, windowing | Exactly-once semantics, local state |
| **Connect API** | 🟢 | Data integration | ETL, system integration | Source/sink connectors, fault tolerance | Scalable, distributed processing |
| **Admin API** | 🟢 | Cluster management | Operations, monitoring | Topic management, configuration | Programmatic administration |

## 🔧 Client APIs

### Producer API Features
| Feature | Status | Description | Use Cases | Configuration |
|---------|--------|-------------|-----------|---------------|
| **Async Publishing** | 🟢 | Non-blocking message sending | High throughput applications | `acks`, `retries`, `batch.size` |
| **Sync Publishing** | 🟢 | Blocking message sending | Critical data, low latency | `acks=all`, `retries=MAX_INT` |
| **Batching** | 🟢 | Message grouping for efficiency | High volume scenarios | `batch.size`, `linger.ms` |
| **Compression** | 🟢 | Data compression | Network/storage optimization | `compression.type` (gzip, snappy, lz4, zstd) |
| **Partitioning** | 🟢 | Custom partition assignment | Load balancing, ordering | Custom partitioner, partition key |
| **Idempotent Producer** | 🟢 | Exactly-once delivery | Data consistency | `enable.idempotence=true` |
| **Transactions** | 🟢 | Multi-message atomicity | Exactly-once processing | `transactional.id` |
| **Schema Registry** | 🟢 | Schema evolution | Data governance | Confluent Schema Registry integration |

### Consumer API Features
| Feature | Status | Description | Use Cases | Configuration |
|---------|--------|-------------|-----------|---------------|
| **Consumer Groups** | 🟢 | Scalable consumption | Parallel processing | `group.id`, partition assignment |
| **Manual Offset Management** | 🟢 | Custom offset control | Exactly-once processing | `enable.auto.commit=false` |
| **Seek Operations** | 🟢 | Position control | Replay, recovery | `seek()`, `seekToBeginning()` |
| **Partition Assignment** | 🟢 | Custom partition mapping | Load balancing | Range, round-robin, sticky assignors |
| **Consumer Interceptors** | 🟢 | Message interception | Monitoring, transformation | Custom interceptor implementation |
| **Fetch Optimization** | 🟢 | Batch fetching | Performance tuning | `fetch.min.bytes`, `fetch.max.wait.ms` |
| **Heartbeat Management** | 🟢 | Group membership | Failure detection | `heartbeat.interval.ms`, `session.timeout.ms` |

### Streams API Features
| Feature | Status | Description | Use Cases | Key Concepts |
|---------|--------|-------------|-----------|--------------|
| **Stateless Processing** | 🟢 | Transformation without state | Filtering, mapping | `map()`, `filter()`, `flatMap()` |
| **Stateful Processing** | 🟢 | Aggregations with state | Windowing, joins | `aggregate()`, `reduce()`, `count()` |
| **Windowing** | 🟢 | Time-based grouping | Time series analysis | Tumbling, hopping, session windows |
| **Stream-Stream Joins** | 🟢 | Joining multiple streams | Data enrichment | Inner, left, outer joins |
| **Stream-Table Joins** | 🟢 | Stream enrichment | Lookup operations | KTable, GlobalKTable |
| **Exactly-Once Semantics** | 🟢 | Processing guarantees | Critical applications | `processing.guarantee=exactly_once_v2` |
| **Interactive Queries** | 🟢 | State store access | Real-time queries | Local state stores, RPC layer |
| **Topology Optimization** | 🟢 | Automatic optimization | Performance improvement | Automatic repartitioning, co-partitioning |

## 🚀 Deployment Modes Comparison

| Mode | Best For | Resource Management | Fault Tolerance | Scaling | Setup Complexity |
|------|----------|-------------------|-----------------|---------|------------------|
| **Single Node** | Development, testing | Manual | Limited | Manual | Minimal |
| **Multi-Broker Cluster** | Production | Manual/automated | High | Horizontal | Medium |
| **Docker/Containers** | Cloud deployments | Container orchestration | Medium | Container-based | Medium |
| **Kubernetes** | Cloud-native | K8s scheduler | High | Auto-scaling | High |
| **Confluent Cloud** | Fully managed | Cloud provider | High | Auto-scaling | Low |
| **Amazon MSK** | AWS managed | AWS managed | High | Auto-scaling | Low |
| **Azure Event Hubs** | Azure managed | Azure managed | High | Auto-scaling | Low |

## 📊 Data Formats & Serialization

| Format | Read Support | Write Support | Schema Evolution | Performance | Use Cases |
|--------|--------------|---------------|------------------|-------------|-----------|
| **Avro** | ✅ | ✅ | Excellent | High | Schema evolution, compact binary |
| **JSON** | ✅ | ✅ | Limited | Medium | Human readable, web APIs |
| **Protobuf** | ✅ | ✅ | Good | High | Cross-language, compact |
| **String/Text** | ✅ | ✅ | None | High | Simple messages, logs |
| **ByteArray** | ✅ | ✅ | None | Highest | Custom serialization |
| **Confluent Schema Registry** | ✅ | ✅ | Excellent | High | Enterprise schema management |
| **Apache Parquet** | ✅ | ✅ | Good | High | Analytics, columnar storage |
| **MessagePack** | ✅ | ✅ | Limited | High | Compact binary, cross-language |

## ⚡ Performance Optimization Features

| Feature | Category | Impact | Configuration | Use Cases |
|---------|----------|--------|---------------|-----------|
| **Partitioning Strategy** | Throughput | High | `num.partitions`, custom partitioner | Parallel processing, load balancing |
| **Replication Factor** | Reliability | Medium | `default.replication.factor` | Fault tolerance vs performance |
| **Batch Size Tuning** | Throughput | High | `batch.size`, `linger.ms` | High volume producers |
| **Compression** | Network/Storage | High | `compression.type` | Bandwidth optimization |
| **Producer Acks** | Reliability | Medium | `acks` (0, 1, all) | Durability vs latency trade-off |
| **Consumer Fetch Size** | Throughput | Medium | `fetch.min.bytes`, `max.poll.records` | Batch consumption optimization |
| **Log Compaction** | Storage | Medium | `cleanup.policy=compact` | Key-based deduplication |
| **Tiered Storage** | Cost | Medium | `remote.log.storage.system.enable` | Long-term retention |
| **Zero-Copy Transfers** | CPU | High | Automatic | Efficient data transfer |
| **Memory Mapping** | I/O | High | OS-level | Fast log access |

## 🔧 Configuration Categories

### Broker Configuration
| Parameter | Default | Description | Tuning Guidelines |
|-----------|---------|-------------|-------------------|
| `num.network.threads` | 3 | Network request threads | 8-16 for high throughput |
| `num.io.threads` | 8 | I/O threads | 2x number of disks |
| `socket.send.buffer.bytes` | 102400 | Socket send buffer | Increase for high throughput |
| `socket.receive.buffer.bytes` | 102400 | Socket receive buffer | Increase for high throughput |
| `socket.request.max.bytes` | 104857600 | Max request size | Adjust for large messages |
| `num.replica.fetchers` | 1 | Replica fetcher threads | Increase for many partitions |
| `replica.fetch.max.bytes` | 1048576 | Max replica fetch size | Balance with network capacity |

### Producer Configuration
| Parameter | Default | Description | Tuning Guidelines |
|-----------|---------|-------------|-------------------|
| `batch.size` | 16384 | Batch size in bytes | 32KB-64KB for high throughput |
| `linger.ms` | 0 | Batching delay | 5-100ms for throughput |
| `buffer.memory` | 33554432 | Producer buffer memory | Increase for high volume |
| `compression.type` | none | Compression algorithm | Use snappy or lz4 |
| `acks` | 1 | Acknowledgment level | all for durability |
| `retries` | 2147483647 | Retry attempts | High value with idempotence |
| `max.in.flight.requests.per.connection` | 5 | Concurrent requests | 1 for ordering, 5 for throughput |

### Consumer Configuration
| Parameter | Default | Description | Tuning Guidelines |
|-----------|---------|-------------|-------------------|
| `fetch.min.bytes` | 1 | Minimum fetch size | 1KB-1MB for batching |
| `fetch.max.wait.ms` | 500 | Max fetch wait time | Balance latency vs throughput |
| `max.poll.records` | 500 | Max records per poll | Adjust based on processing time |
| `session.timeout.ms` | 10000 | Session timeout | 6-30 seconds |
| `heartbeat.interval.ms` | 3000 | Heartbeat interval | 1/3 of session timeout |
| `max.poll.interval.ms` | 300000 | Max poll interval | Adjust for processing time |
| `auto.offset.reset` | latest | Offset reset policy | earliest for replay |

## 🌐 Ecosystem Integrations

| Tool/Platform | Integration Type | Kafka Component | Key Features | Setup Complexity |
|---------------|------------------|-----------------|--------------|------------------|
| **Apache Spark** | Stream Processing | Structured Streaming | Micro-batch processing, exactly-once | Medium |
| **Apache Flink** | Stream Processing | Flink Kafka Connector | Low latency, event time processing | Medium |
| **Apache Storm** | Stream Processing | Storm Kafka Spout | Real-time processing | Medium |
| **Elasticsearch** | Search & Analytics | Kafka Connect | Log analytics, search | Low |
| **Apache Cassandra** | Database | Kafka Connect | Event sourcing, time series | Medium |
| **MongoDB** | Document Database | Kafka Connect | Change data capture | Low |
| **PostgreSQL** | Relational Database | Debezium CDC | Change data capture | Medium |
| **Redis** | Caching | Kafka Connect | Real-time caching | Low |
| **Apache Hadoop** | Big Data | Kafka Connect | Batch processing integration | High |
| **Apache Airflow** | Workflow Orchestration | Kafka operators | Data pipeline orchestration | Medium |
| **Prometheus** | Monitoring | JMX metrics | System monitoring | Low |
| **Grafana** | Visualization | Kafka dashboards | Metrics visualization | Low |
| **Schema Registry** | Schema Management | Confluent Platform | Schema evolution, governance | Medium |
| **KSQL/ksqlDB** | Stream Processing | Confluent Platform | SQL-based stream processing | Low |
| **Kafka Streams** | Stream Processing | Native | Lightweight stream processing | Low |

## 📈 Performance Benchmarks & Limits

| Metric | Small Cluster (3 brokers) | Medium Cluster (10 brokers) | Large Cluster (50+ brokers) | Notes |
|--------|---------------------------|----------------------------|----------------------------|-------|
| **Max Throughput (MB/s)** | 100-500 | 1,000-5,000 | 10,000+ | Depends on hardware, network |
| **Max Messages/sec** | 100K-1M | 1M-10M | 10M+ | Message size dependent |
| **Max Partitions** | 1,000 | 10,000 | 100,000+ | Limited by ZooKeeper/KRaft |
| **Max Topics** | 100 | 1,000 | 10,000+ | Metadata overhead |
| **Max Consumers per Group** | 100 | 1,000 | 10,000+ | Network and coordination overhead |
| **Max Retention** | Days | Weeks | Months/Years | Storage dependent |
| **Max Message Size** | 1MB | 10MB | 100MB+ | Network and memory impact |
| **Replication Factor** | 3 | 3-5 | 3-7 | Balance durability vs performance |

## 🔍 Monitoring & Debugging

| Tool/Feature | Purpose | Access Method | Key Metrics | Best Practices |
|--------------|---------|---------------|-------------|----------------|
| **JMX Metrics** | Broker monitoring | JMX endpoints | Throughput, latency, errors | Export to monitoring systems |
| **Kafka Manager** | Cluster management | Web UI | Topic, consumer group status | Use for operational tasks |
| **Confluent Control Center** | Enterprise monitoring | Web UI | End-to-end monitoring | Commercial solution |
| **Kafka Tool** | Topic inspection | Desktop application | Message browsing, offset management | Development and debugging |
| **kafkacat/kcat** | Command-line tool | CLI | Message production/consumption | Lightweight testing |
| **Cruise Control** | Cluster balancing | REST API | Partition rebalancing | Automated operations |
| **Burrow** | Consumer lag monitoring | REST API | Consumer group lag | Open source lag monitoring |
| **Kafdrop** | Web UI | Browser | Topic and message browsing | Lightweight web interface |

## 🚨 Common Issues & Solutions

| Issue | Symptoms | Root Cause | Solution | Prevention |
|-------|----------|------------|----------|-----------|
| **High Consumer Lag** | Slow processing, growing queues | Slow consumers, insufficient parallelism | Scale consumers, optimize processing | Monitor lag, capacity planning |
| **Rebalancing Issues** | Frequent rebalances, processing delays | Consumer failures, network issues | Tune session timeouts, fix network | Stable consumers, proper timeouts |
| **Disk Space Issues** | Broker failures, log retention errors | Insufficient storage, retention misconfiguration | Increase storage, tune retention | Monitor disk usage, proper retention |
| **Network Partitions** | Split brain, data inconsistency | Network failures, firewall issues | Fix network, proper configuration | Network monitoring, redundancy |
| **Memory Issues** | OutOfMemoryError, GC pressure | Large messages, insufficient heap | Increase heap, optimize message size | Memory monitoring, message size limits |
| **ZooKeeper Issues** | Cluster instability, metadata corruption | ZooKeeper failures, network issues | Fix ZooKeeper, migrate to KRaft | ZooKeeper monitoring, KRaft migration |
| **Throughput Bottlenecks** | Low throughput, high latency | Poor configuration, hardware limits | Tune configuration, scale hardware | Performance testing, capacity planning |
| **Data Loss** | Missing messages | Improper acks configuration | Configure acks=all, proper replication | Durability settings, monitoring |

## 🔄 Version Compatibility

| Kafka Version | Release Date | Key Features | End of Support | Recommended For |
|---------------|--------------|--------------|----------------|-----------------|
| **3.6.x** | 2024 | KRaft improvements, performance | Active | Latest features, new deployments |
| **3.5.x** | 2023 | KRaft GA, tiered storage | Active | Production workloads |
| **3.4.x** | 2023 | KRaft improvements | Active | Stable production |
| **3.3.x** | 2022 | KRaft preview | Extended | Migration to KRaft |
| **3.2.x** | 2022 | Performance improvements | Extended | Stable ZooKeeper deployments |
| **3.1.x** | 2022 | KRaft early access | EOL | Development only |
| **2.8.x** | 2021 | KRaft experimental | EOL | Legacy compatibility |

## ⚡ Quick Reference Commands

### Kafka CLI Tools
```bash
# Create topic
kafka-topics.sh --create --topic my-topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1

# List topics
kafka-topics.sh --list --bootstrap-server localhost:9092

# Describe topic
kafka-topics.sh --describe --topic my-topic --bootstrap-server localhost:9092

# Produce messages
kafka-console-producer.sh --topic my-topic --bootstrap-server localhost:9092

# Consume messages
kafka-console-consumer.sh --topic my-topic --from-beginning --bootstrap-server localhost:9092

# Consumer groups
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group my-group
```

### Performance Tuning Commands
```bash
# Broker performance test
kafka-producer-perf-test.sh --topic test --num-records 1000000 --record-size 1024 --throughput 10000 --producer-props bootstrap.servers=localhost:9092

# Consumer performance test
kafka-consumer-perf-test.sh --topic test --messages 1000000 --bootstrap-server localhost:9092

# Log segment analysis
kafka-log-dirs.sh --bootstrap-server localhost:9092 --describe --json
```

### Configuration Examples
```properties
# High throughput producer
batch.size=65536
linger.ms=10
compression.type=snappy
acks=1

# Low latency producer
batch.size=0
linger.ms=0
acks=1

# Reliable producer
acks=all
retries=2147483647
enable.idempotence=true
```

## 📚 Related Resources

### Internal Links
- [Kafka Interview Questions](./KAFKA_COMPREHENSIVE_INTERVIEW_QUESTIONS.md)
- [Streaming Concepts](../STREAMING_KEY_CONCEPTS.md)
- [Confluent Kafka](../Confluent-Kafka/)
- [Message Queues Comparison](../DISTRIBUTED_MESSAGE_QUEUES_INTERVIEW_QUESTIONS.md)

### External Resources
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Confluent Documentation](https://docs.confluent.io/)
- [Kafka Improvement Proposals (KIPs)](https://cwiki.apache.org/confluence/display/KAFKA/Kafka+Improvement+Proposals)
- [Kafka Community](https://kafka.apache.org/contact)

## 🎓 Learning Path & Certification

| Level | Topics | Hands-on Projects | Skills Developed | Time Investment |
|-------|--------|-------------------|------------------|-----------------|
| **Beginner** | Basic concepts, CLI tools | Simple producer/consumer | Message handling, basic operations | 2-4 weeks |
| **Intermediate** | Streams API, Connect | Real-time analytics, ETL pipelines | Stream processing, integration | 2-3 months |
| **Advanced** | Performance tuning, operations | Production deployment, monitoring | Architecture, optimization | 4-6 months |
| **Expert** | Internals, custom components | Custom connectors, contributions | Deep expertise, leadership | 6+ months |

## 🆚 Kafka vs Alternatives

| Tool | Best For | Kafka Advantage | Alternative Advantage | When to Choose Kafka |
|------|---------|-----------------|----------------------|---------------------|
| **Apache Pulsar** | Multi-tenancy | Mature ecosystem | Better multi-tenancy | Established ecosystems |
| **Amazon Kinesis** | AWS environments | Open source, portable | Fully managed | Multi-cloud or on-premises |
| **Azure Event Hubs** | Azure environments | Broader ecosystem | Native Azure integration | Beyond Azure ecosystem |
| **Google Pub/Sub** | GCP environments | Self-managed | Serverless, auto-scaling | Control over infrastructure |
| **RabbitMQ** | Traditional messaging | Higher throughput | Easier setup, AMQP | High-throughput streaming |
| **Apache ActiveMQ** | Enterprise messaging | Modern architecture | JMS compliance | Event streaming use cases |

---

**Last Updated**: 2024  
**Kafka Version Coverage**: 2.8 - 3.6.x