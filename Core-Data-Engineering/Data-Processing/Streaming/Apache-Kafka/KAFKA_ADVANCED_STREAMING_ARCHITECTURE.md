# 🚀 Apache Kafka - Advanced Streaming Architecture

[![Kafka Version](https://img.shields.io/badge/Kafka-3.6+-blue)](https://kafka.apache.org/)
[![Difficulty](https://img.shields.io/badge/Difficulty-Advanced-red)](https://github.com/yourusername/Data-Engineering-Material)
[![Production Ready](https://img.shields.io/badge/Production-Ready-green)](https://github.com/yourusername/Data-Engineering-Material)

> **Production-grade Kafka patterns, performance optimization, and enterprise streaming architectures**

## 📋 Table of Contents

1. [Performance Optimization](#-performance-optimization)
2. [Advanced Producer Patterns](#-advanced-producer-patterns)
3. [Consumer Optimization](#-consumer-optimization)
4. [Cluster Management](#-cluster-management)
5. [Security & Compliance](#-security--compliance)
6. [Monitoring & Observability](#-monitoring--observability)
7. [Disaster Recovery](#-disaster-recovery)
8. [Multi-Cluster Patterns](#-multi-cluster-patterns)

---

## ⚡ Performance Optimization

### 🎯 Throughput Optimization

```python
# High-throughput producer configuration
high_throughput_producer = {
    "batch.size": 65536,  # 64KB batches
    "linger.ms": 20,      # Wait 20ms for batching
    "compression.type": "lz4",  # Fast compression
    "buffer.memory": 134217728,  # 128MB buffer
    "max.in.flight.requests.per.connection": 5,
    "acks": "1"  # Leader acknowledgment only
}

# High-throughput consumer configuration  
high_throughput_consumer = {
    "fetch.min.bytes": 50000,  # Fetch at least 50KB
    "fetch.max.wait.ms": 500,  # Max wait 500ms
    "max.partition.fetch.bytes": 2097152,  # 2MB per partition
    "max.poll.records": 2000   # Process 2000 records per poll
}
```

### 🚀 Low-Latency Optimization

```python
# Low-latency producer configuration
low_latency_producer = {
    "batch.size": 0,      # No batching
    "linger.ms": 0,       # Send immediately
    "compression.type": "none",  # No compression overhead
    "acks": "1",          # Balance between speed and durability
    "max.in.flight.requests.per.connection": 1  # Ordering guarantee
}

# Low-latency consumer configuration
low_latency_consumer = {
    "fetch.min.bytes": 1,     # Fetch immediately
    "fetch.max.wait.ms": 0,   # No waiting
    "max.poll.records": 100   # Small batches for quick processing
}
```

---

## 📤 Advanced Producer Patterns

### 🔄 Idempotent Producer

```python
# Exactly-once producer configuration
exactly_once_producer = {
    "enable.idempotence": "true",
    "acks": "all",
    "retries": 2147483647,  # Max retries
    "max.in.flight.requests.per.connection": 5,
    "transactional.id": "my-transactional-producer"
}

# Transactional producer pattern
def transactional_producer_pattern():
    """
    Pattern for exactly-once processing with transactions
    """
    steps = [
        "producer.initTransactions()",
        "producer.beginTransaction()",
        "producer.send(record1)",
        "producer.send(record2)", 
        "producer.commitTransaction() / abortTransaction()"
    ]
    return steps
```

### 🎯 Custom Partitioner

```python
# Custom partitioning strategy
class CustomPartitioner:
    def partition(self, topic, key, key_bytes, value, value_bytes, cluster):
        """
        Custom partitioning logic for specific business requirements
        """
        if key is None:
            return 0
        
        # Route VIP customers to dedicated partition
        if key.startswith("VIP_"):
            return 0
        
        # Hash-based partitioning for regular customers
        return hash(key) % cluster.partition_count_for_topic(topic)
```

---

## 📥 Consumer Optimization

### 🔄 Advanced Consumer Patterns

```python
# Manual offset management pattern
def manual_offset_management():
    """
    Pattern for precise offset control
    """
    consumer_config = {
        "enable.auto.commit": "false",
        "isolation.level": "read_committed"  # For transactional messages
    }
    
    processing_pattern = [
        "records = consumer.poll(timeout)",
        "for record in records:",
        "  process_record(record)",
        "  store_offset(record.topic, record.partition, record.offset)",
        "consumer.commitSync(stored_offsets)"
    ]
    
    return consumer_config, processing_pattern
```

### 🎯 Consumer Rebalancing Optimization

```python
# Cooperative rebalancing configuration
cooperative_rebalancing = {
    "partition.assignment.strategy": "org.apache.kafka.clients.consumer.CooperativeStickyAssignor",
    "session.timeout.ms": 45000,  # Longer session timeout
    "heartbeat.interval.ms": 15000,  # Regular heartbeats
    "max.poll.interval.ms": 600000   # 10 minutes processing time
}
```

---

## 🏗️ Cluster Management

### 📊 Capacity Planning

```python
def capacity_planning_calculator():
    """
    Calculate Kafka cluster capacity requirements
    """
    requirements = {
        "messages_per_second": 100000,
        "message_size_bytes": 1024,
        "retention_days": 7,
        "replication_factor": 3
    }
    
    # Calculate storage requirements
    daily_data_gb = (requirements["messages_per_second"] * 
                    requirements["message_size_bytes"] * 
                    86400) / (1024**3)
    
    total_storage_gb = (daily_data_gb * 
                       requirements["retention_days"] * 
                       requirements["replication_factor"])
    
    # Calculate broker requirements
    brokers_needed = max(3, requirements["replication_factor"])
    storage_per_broker_gb = total_storage_gb / brokers_needed
    
    return {
        "daily_data_gb": round(daily_data_gb, 2),
        "total_storage_gb": round(total_storage_gb, 2),
        "brokers_needed": brokers_needed,
        "storage_per_broker_gb": round(storage_per_broker_gb, 2)
    }

print("Capacity Planning:", capacity_planning_calculator())
```

### 🔧 Cluster Scaling Strategies

```python
# Scaling patterns
scaling_strategies = {
    "horizontal_scaling": {
        "add_brokers": "Add new brokers to cluster",
        "partition_reassignment": "Redistribute partitions across brokers",
        "replication_increase": "Increase replication factor for durability"
    },
    "vertical_scaling": {
        "increase_memory": "More RAM for page cache",
        "faster_storage": "SSD for better I/O performance", 
        "more_cpu_cores": "Handle more concurrent connections"
    }
}
```

---

## 🔒 Security & Compliance

### 🛡️ Authentication & Authorization

```python
# SASL/SSL configuration
security_config = {
    "security.protocol": "SASL_SSL",
    "sasl.mechanism": "PLAIN",
    "sasl.jaas.config": "org.apache.kafka.common.security.plain.PlainLoginModule required username='user' password='password';",
    "ssl.truststore.location": "/path/to/truststore.jks",
    "ssl.truststore.password": "truststore-password"
}

# ACL patterns for authorization
acl_patterns = {
    "topic_access": "kafka-acls --authorizer-properties zookeeper.connect=localhost:2181 --add --allow-principal User:alice --operation Read --topic my-topic",
    "consumer_group": "kafka-acls --authorizer-properties zookeeper.connect=localhost:2181 --add --allow-principal User:alice --operation Read --group my-group",
    "producer_access": "kafka-acls --authorizer-properties zookeeper.connect=localhost:2181 --add --allow-principal User:bob --operation Write --topic my-topic"
}
```

### 🔐 Encryption Patterns

```python
# End-to-end encryption configuration
encryption_config = {
    "ssl.protocol": "TLSv1.2",
    "ssl.enabled.protocols": "TLSv1.2",
    "ssl.cipher.suites": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
    "ssl.endpoint.identification.algorithm": "https"
}
```

---

## 📊 Monitoring & Observability

### 📈 Key Metrics to Monitor

```python
# Critical Kafka metrics
critical_metrics = {
    "broker_metrics": [
        "kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec",
        "kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec", 
        "kafka.network:type=RequestMetrics,name=TotalTimeMs,request=Produce",
        "kafka.server:type=ReplicaManager,name=LeaderCount"
    ],
    "consumer_metrics": [
        "kafka.consumer:type=consumer-fetch-manager-metrics,client-id=*,attribute=records-lag-max",
        "kafka.consumer:type=consumer-coordinator-metrics,client-id=*,attribute=commit-latency-avg"
    ],
    "producer_metrics": [
        "kafka.producer:type=producer-metrics,client-id=*,attribute=record-send-rate",
        "kafka.producer:type=producer-metrics,client-id=*,attribute=batch-size-avg"
    ]
}
```

### 🚨 Alerting Thresholds

```python
# Production alerting thresholds
alerting_thresholds = {
    "consumer_lag": {
        "warning": 10000,   # 10K messages behind
        "critical": 100000  # 100K messages behind
    },
    "disk_usage": {
        "warning": 80,      # 80% disk usage
        "critical": 90      # 90% disk usage
    },
    "under_replicated_partitions": {
        "warning": 1,       # Any under-replicated partitions
        "critical": 10      # 10+ under-replicated partitions
    }
}
```

---

## 🔄 Disaster Recovery

### 💾 Backup Strategies

```python
# Backup and recovery patterns
backup_strategies = {
    "mirror_maker": {
        "description": "Replicate topics to secondary cluster",
        "use_case": "Cross-datacenter replication",
        "configuration": {
            "consumer.config": "source-cluster.properties",
            "producer.config": "target-cluster.properties",
            "whitelist": "topic1,topic2"
        }
    },
    "confluent_replicator": {
        "description": "Enterprise replication solution",
        "features": ["Schema preservation", "Offset translation", "Monitoring"]
    },
    "topic_snapshots": {
        "description": "Point-in-time topic backups",
        "tools": ["kafka-dump-log", "Custom backup scripts"]
    }
}
```

### 🔄 Recovery Procedures

```python
# Disaster recovery runbook
recovery_procedures = {
    "broker_failure": [
        "1. Identify failed broker",
        "2. Check if leader partitions affected", 
        "3. Replace broker with same broker.id",
        "4. Restore data from replicas",
        "5. Verify cluster health"
    ],
    "complete_cluster_loss": [
        "1. Provision new cluster",
        "2. Restore topics from backup",
        "3. Reset consumer offsets",
        "4. Validate data integrity",
        "5. Resume applications"
    ]
}
```

---

## 🌐 Multi-Cluster Patterns

### 🔄 Cross-Cluster Replication

```python
# Multi-cluster architecture patterns
multi_cluster_patterns = {
    "active_passive": {
        "description": "Primary cluster with standby for DR",
        "failover_time": "Minutes to hours",
        "complexity": "Low"
    },
    "active_active": {
        "description": "Multiple active clusters with bidirectional replication", 
        "failover_time": "Seconds",
        "complexity": "High"
    },
    "hub_spoke": {
        "description": "Central hub with regional spokes",
        "use_case": "Global data distribution",
        "complexity": "Medium"
    }
}
```

### 🎯 Conflict Resolution

```python
# Conflict resolution strategies for multi-cluster
conflict_resolution = {
    "timestamp_based": "Use message timestamp for conflict resolution",
    "cluster_priority": "Assign priority to clusters",
    "application_logic": "Handle conflicts in application layer",
    "last_writer_wins": "Simple but may lose data"
}
```

---

## 🎓 Production Checklist

### ✅ Pre-Production Validation

```python
production_checklist = {
    "performance": [
        "Load testing completed",
        "Latency requirements validated", 
        "Throughput targets achieved",
        "Resource utilization optimized"
    ],
    "reliability": [
        "Replication factor ≥ 3",
        "min.insync.replicas ≥ 2",
        "Backup procedures tested",
        "Disaster recovery validated"
    ],
    "security": [
        "Authentication enabled",
        "Authorization configured",
        "Encryption in transit/at rest",
        "Security audit completed"
    ],
    "monitoring": [
        "Metrics collection setup",
        "Alerting rules configured",
        "Dashboards created",
        "Runbooks documented"
    ]
}

print("Production Readiness Checklist:")
for category, items in production_checklist.items():
    print(f"\n{category.upper()}:")
    for item in items:
        print(f"  ☐ {item}")
```

Remember: **Production Kafka requires careful planning and monitoring!** These patterns will help you build robust, scalable streaming architectures.

Happy streaming! 🌊✨