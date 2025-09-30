# ⚡ Apache Kafka - Quick Reference

[![Kafka Version](https://img.shields.io/badge/Kafka-3.6+-blue)](https://kafka.apache.org/)
[![Quick Reference](https://img.shields.io/badge/Type-Quick%20Reference-green)](https://github.com/yourusername/Data-Engineering-Material)

> **Essential Kafka commands, configurations, and troubleshooting for daily operations**

## 🚀 Quick Start Commands

### 📋 Topic Management
```bash
# Create topic
kafka-topics --create --topic my-topic --partitions 3 --replication-factor 2 --bootstrap-server localhost:9092

# List topics
kafka-topics --list --bootstrap-server localhost:9092

# Describe topic
kafka-topics --describe --topic my-topic --bootstrap-server localhost:9092

# Delete topic
kafka-topics --delete --topic my-topic --bootstrap-server localhost:9092
```

### 📤 Producer Commands
```bash
# Console producer
kafka-console-producer --topic my-topic --bootstrap-server localhost:9092

# Producer with key
kafka-console-producer --topic my-topic --property "key.separator=:" --property "parse.key=true" --bootstrap-server localhost:9092
```

### 📥 Consumer Commands
```bash
# Console consumer (from latest)
kafka-console-consumer --topic my-topic --bootstrap-server localhost:9092

# Consumer from beginning
kafka-console-consumer --topic my-topic --from-beginning --bootstrap-server localhost:9092

# Consumer with key
kafka-console-consumer --topic my-topic --property print.key=true --property key.separator=":" --bootstrap-server localhost:9092
```

---

## ⚙️ Essential Configurations

### 🔧 Producer Config
```python
producer_config = {
    "bootstrap.servers": "localhost:9092",
    "key.serializer": "org.apache.kafka.common.serialization.StringSerializer",
    "value.serializer": "org.apache.kafka.common.serialization.StringSerializer",
    "acks": "all",
    "retries": 3,
    "batch.size": 16384,
    "linger.ms": 5
}
```

### 🔧 Consumer Config
```python
consumer_config = {
    "bootstrap.servers": "localhost:9092", 
    "group.id": "my-group",
    "key.deserializer": "org.apache.kafka.common.serialization.StringDeserializer",
    "value.deserializer": "org.apache.kafka.common.serialization.StringDeserializer",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": "false"
}
```

---

## 📊 Monitoring Commands

### 📈 Consumer Groups
```bash
# List consumer groups
kafka-consumer-groups --list --bootstrap-server localhost:9092

# Describe consumer group
kafka-consumer-groups --describe --group my-group --bootstrap-server localhost:9092

# Reset offsets
kafka-consumer-groups --reset-offsets --group my-group --topic my-topic --to-earliest --execute --bootstrap-server localhost:9092
```

### 📊 Performance Metrics
```bash
# Producer performance test
kafka-producer-perf-test --topic my-topic --num-records 100000 --record-size 1024 --throughput 10000 --producer-props bootstrap.servers=localhost:9092

# Consumer performance test  
kafka-consumer-perf-test --topic my-topic --messages 100000 --bootstrap-server localhost:9092
```

---

## 🔍 Troubleshooting

### ⚠️ Common Issues
```python
common_issues = {
    "consumer_lag": {
        "symptom": "Messages not processed in time",
        "check": "kafka-consumer-groups --describe --group my-group",
        "solutions": ["Scale consumers", "Optimize processing", "Increase partitions"]
    },
    "under_replicated": {
        "symptom": "Data durability at risk", 
        "check": "kafka-topics --describe --under-replicated-partitions",
        "solutions": ["Check broker health", "Restart failed brokers", "Reassign partitions"]
    },
    "disk_full": {
        "symptom": "Broker stops accepting messages",
        "check": "df -h /kafka-logs",
        "solutions": ["Clean old logs", "Reduce retention", "Add storage"]
    }
}
```

### 🔧 Debug Commands
```bash
# Check log segments
kafka-dump-log --files /kafka-logs/my-topic-0/00000000000000000000.log --print-data-log

# Verify consumer position
kafka-run-class kafka.tools.ConsumerOffsetChecker --zookeeper localhost:2181 --group my-group

# Check broker logs
tail -f /kafka-logs/server.log
```

---

## 🎯 Performance Tuning

### ⚡ High Throughput
```python
high_throughput = {
    "producer": {
        "batch.size": 65536,
        "linger.ms": 20,
        "compression.type": "lz4",
        "acks": "1"
    },
    "consumer": {
        "fetch.min.bytes": 50000,
        "max.poll.records": 2000
    }
}
```

### 🚀 Low Latency  
```python
low_latency = {
    "producer": {
        "batch.size": 0,
        "linger.ms": 0,
        "acks": "1"
    },
    "consumer": {
        "fetch.min.bytes": 1,
        "max.poll.records": 100
    }
}
```

---

## 🔒 Security Quick Setup

### 🛡️ SASL/PLAIN
```bash
# Server config
security.inter.broker.protocol=SASL_PLAINTEXT
sasl.mechanism.inter.broker.protocol=PLAIN
sasl.enabled.mechanisms=PLAIN

# Client config  
security.protocol=SASL_PLAINTEXT
sasl.mechanism=PLAIN
sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username="user" password="password";
```

---

## 📚 Useful Scripts

### 🔄 Topic Backup
```bash
#!/bin/bash
# Backup topic data
kafka-console-consumer --topic $1 --from-beginning --bootstrap-server localhost:9092 > backup_$1_$(date +%Y%m%d).txt
```

### 📊 Health Check
```bash
#!/bin/bash
# Basic health check
echo "=== Broker Status ==="
kafka-broker-api-versions --bootstrap-server localhost:9092

echo "=== Topic Count ==="
kafka-topics --list --bootstrap-server localhost:9092 | wc -l

echo "=== Consumer Groups ==="
kafka-consumer-groups --list --bootstrap-server localhost:9092
```

---

## 🎯 Common Patterns

### 🔄 Exactly-Once Processing
```python
# Producer
producer_props = {
    "enable.idempotence": "true",
    "acks": "all", 
    "retries": 2147483647,
    "transactional.id": "my-producer"
}

# Consumer
consumer_props = {
    "isolation.level": "read_committed",
    "enable.auto.commit": "false"
}
```

### 📊 Stream Processing
```python
# Kafka Streams config
streams_config = {
    "application.id": "my-stream-app",
    "bootstrap.servers": "localhost:9092",
    "default.key.serde": "org.apache.kafka.common.serialization.Serdes$StringSerde",
    "default.value.serde": "org.apache.kafka.common.serialization.Serdes$StringSerde"
}
```

---

## 🚨 Emergency Procedures

### 🔥 Broker Down
```bash
# 1. Check broker status
systemctl status kafka

# 2. Check logs
tail -f /kafka-logs/server.log

# 3. Restart broker
systemctl restart kafka

# 4. Verify cluster health
kafka-topics --describe --under-replicated-partitions --bootstrap-server localhost:9092
```

### 💾 Data Recovery
```bash
# 1. Stop consumers
# 2. Reset offsets to specific timestamp
kafka-consumer-groups --reset-offsets --group my-group --topic my-topic --to-datetime 2024-01-01T00:00:00.000 --execute --bootstrap-server localhost:9092

# 3. Restart consumers
```

---

## 📖 Quick Links

- **[Kafka Key Concepts](./KAFKA_KEY_CONCEPTS.md)** - Fundamentals and architecture
- **[Advanced Patterns](./KAFKA_ADVANCED_STREAMING_ARCHITECTURE.md)** - Production optimization
- **[Official Docs](https://kafka.apache.org/documentation/)** - Complete documentation
- **[Confluent Docs](https://docs.confluent.io/)** - Enterprise features

---

**💡 Pro Tip**: Always test configuration changes in development before applying to production!

Happy streaming! 🌊✨