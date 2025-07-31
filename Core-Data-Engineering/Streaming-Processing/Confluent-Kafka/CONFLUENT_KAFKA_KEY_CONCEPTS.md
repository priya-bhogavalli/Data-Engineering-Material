# Confluent Kafka Key Concepts

## 1. Enterprise Kafka Platform
**What it is**: Enterprise-grade streaming platform built on Apache Kafka with additional tools and managed services.

**Confluent Components**:
- **Apache Kafka**: Core streaming platform
- **Schema Registry**: Schema management and evolution
- **Kafka Connect**: Data integration framework
- **ksqlDB**: Stream processing with SQL
- **Control Center**: Management and monitoring UI
- **Confluent Cloud**: Fully managed Kafka service

## 2. Schema Registry
**Purpose**: Centralized schema management for Kafka topics with schema evolution support.

**Schema Registration**:
```bash
# Register Avro schema
curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  --data '{
    "schema": "{
      \"type\": \"record\",
      \"name\": \"Customer\",
      \"fields\": [
        {\"name\": \"id\", \"type\": \"int\"},
        {\"name\": \"name\", \"type\": \"string\"},
        {\"name\": \"email\", \"type\": \"string\"}
      ]
    }"
  }' \
  http://localhost:8081/subjects/customers-value/versions
```

**Schema Evolution**:
```json
// Version 1
{
  "type": "record",
  "name": "Customer",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "name", "type": "string"}
  ]
}

// Version 2 (backward compatible)
{
  "type": "record",
  "name": "Customer", 
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": ["null", "string"], "default": null}
  ]
}
```

**Producer with Schema Registry**:
```python
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

# Schema Registry configuration
schema_registry_conf = {
    'url': 'http://localhost:8081'
}

# Producer configuration
producer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'schema.registry.url': 'http://localhost:8081'
}

# Value schema
value_schema = """
{
  "type": "record",
  "name": "Customer",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": "string"}
  ]
}
"""

producer = AvroProducer(producer_conf, default_value_schema=value_schema)

# Produce message
producer.produce(
    topic='customers',
    value={
        'id': 123,
        'name': 'John Doe',
        'email': 'john@example.com'
    }
)
producer.flush()
```

## 3. Kafka Connect
**Purpose**: Framework for connecting Kafka with external systems for data integration.

**Source Connector Configuration**:
```json
{
  "name": "mysql-source-connector",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
    "connection.url": "jdbc:mysql://localhost:3306/sales",
    "connection.user": "kafka_user",
    "connection.password": "password",
    "table.whitelist": "customers,orders",
    "mode": "incrementing",
    "incrementing.column.name": "id",
    "topic.prefix": "mysql-",
    "poll.interval.ms": 5000,
    "transforms": "createKey,extractInt",
    "transforms.createKey.type": "org.apache.kafka.connect.transforms.ValueToKey",
    "transforms.createKey.fields": "id",
    "transforms.extractInt.type": "org.apache.kafka.connect.transforms.ExtractField$Key",
    "transforms.extractInt.field": "id"
  }
}
```

**Sink Connector Configuration**:
```json
{
  "name": "s3-sink-connector",
  "config": {
    "connector.class": "io.confluent.connect.s3.S3SinkConnector",
    "tasks.max": "3",
    "topics": "customers,orders",
    "s3.region": "us-west-2",
    "s3.bucket.name": "kafka-data-lake",
    "s3.part.size": 5242880,
    "flush.size": 1000,
    "storage.class": "io.confluent.connect.s3.storage.S3Storage",
    "format.class": "io.confluent.connect.s3.format.parquet.ParquetFormat",
    "partitioner.class": "io.confluent.connect.storage.partitioner.TimeBasedPartitioner",
    "partition.duration.ms": 3600000,
    "path.format": "year=YYYY/month=MM/day=dd/hour=HH",
    "locale": "US",
    "timezone": "UTC"
  }
}
```

**Deploy Connector**:
```bash
# Deploy source connector
curl -X POST -H "Content-Type: application/json" \
  --data @mysql-source-connector.json \
  http://localhost:8083/connectors

# Check connector status
curl http://localhost:8083/connectors/mysql-source-connector/status

# Pause/Resume connector
curl -X PUT http://localhost:8083/connectors/mysql-source-connector/pause
curl -X PUT http://localhost:8083/connectors/mysql-source-connector/resume
```

## 4. ksqlDB
**Purpose**: Stream processing engine that enables real-time data processing using SQL syntax.

**Create Streams and Tables**:
```sql
-- Create stream from topic
CREATE STREAM customers_stream (
    id INT,
    name VARCHAR,
    email VARCHAR,
    created_at BIGINT
) WITH (
    KAFKA_TOPIC='customers',
    VALUE_FORMAT='AVRO',
    TIMESTAMP='created_at'
);

-- Create table from stream
CREATE TABLE customers_table AS
SELECT 
    id,
    LATEST_BY_OFFSET(name) AS name,
    LATEST_BY_OFFSET(email) AS email
FROM customers_stream
GROUP BY id
EMIT CHANGES;
```

**Stream Processing Queries**:
```sql
-- Filter and transform
CREATE STREAM high_value_orders AS
SELECT 
    order_id,
    customer_id,
    amount,
    CASE 
        WHEN amount > 1000 THEN 'HIGH'
        WHEN amount > 500 THEN 'MEDIUM'
        ELSE 'LOW'
    END AS priority
FROM orders_stream
WHERE amount > 100
EMIT CHANGES;

-- Windowed aggregations
CREATE TABLE hourly_sales AS
SELECT 
    customer_id,
    WINDOWSTART AS window_start,
    WINDOWEND AS window_end,
    COUNT(*) AS order_count,
    SUM(amount) AS total_amount
FROM orders_stream
WINDOW TUMBLING (SIZE 1 HOUR)
GROUP BY customer_id
EMIT CHANGES;

-- Join streams
CREATE STREAM enriched_orders AS
SELECT 
    o.order_id,
    o.amount,
    c.name AS customer_name,
    c.email AS customer_email
FROM orders_stream o
LEFT JOIN customers_table c ON o.customer_id = c.id
EMIT CHANGES;
```

**User-Defined Functions (UDFs)**:
```java
@UdfDescription(name = "mask_email", description = "Masks email addresses")
public class MaskEmailUdf {
    
    @Udf(description = "Masks the local part of an email address")
    public String maskEmail(final String email) {
        if (email == null || !email.contains("@")) {
            return email;
        }
        
        String[] parts = email.split("@");
        String localPart = parts[0];
        String domain = parts[1];
        
        if (localPart.length() <= 2) {
            return "**@" + domain;
        }
        
        return localPart.charAt(0) + "***" + localPart.charAt(localPart.length() - 1) + "@" + domain;
    }
}
```

## 5. Confluent Control Center
**Monitoring and Management**:
```yaml
# Key metrics monitored:
- Cluster health and performance
- Topic throughput and latency
- Consumer lag and performance
- Connector status and throughput
- Schema Registry usage
- ksqlDB query performance

# Alerting configuration:
alerts:
  - name: "High Consumer Lag"
    condition: "consumer_lag > 10000"
    action: "email_notification"
  - name: "Low Throughput"
    condition: "messages_per_second < 100"
    action: "slack_notification"
```

## 6. Security Features
**Authentication and Authorization**:
```properties
# SASL/SCRAM configuration
security.protocol=SASL_SSL
sasl.mechanism=SCRAM-SHA-256
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
    username="kafka-user" \
    password="password";

# SSL configuration
ssl.truststore.location=/path/to/kafka.client.truststore.jks
ssl.truststore.password=truststore-password
ssl.keystore.location=/path/to/kafka.client.keystore.jks
ssl.keystore.password=keystore-password
ssl.key.password=key-password
```

**Role-Based Access Control (RBAC)**:
```bash
# Create role binding
confluent iam rbac role-binding create \
    --principal User:alice \
    --role DeveloperRead \
    --resource Topic:customers \
    --kafka-cluster-id lkc-12345

# List role bindings
confluent iam rbac role-binding list \
    --principal User:alice \
    --kafka-cluster-id lkc-12345
```

## 7. Multi-Region Replication
**Cluster Linking**:
```bash
# Create cluster link
kafka-cluster-links --bootstrap-server source-cluster:9092 \
    --create --link disaster-recovery-link \
    --config bootstrap.servers=destination-cluster:9092

# Create mirror topic
kafka-mirrors --bootstrap-server destination-cluster:9092 \
    --create --mirror-topic customers \
    --link disaster-recovery-link \
    --replication-factor 3
```

**Replicator Configuration**:
```json
{
  "name": "replicator-connector",
  "config": {
    "connector.class": "io.confluent.connect.replicator.ReplicatorSourceConnector",
    "key.converter": "io.confluent.connect.replicator.util.ByteArrayConverter",
    "value.converter": "io.confluent.connect.replicator.util.ByteArrayConverter",
    "src.kafka.bootstrap.servers": "source-cluster:9092",
    "dest.kafka.bootstrap.servers": "destination-cluster:9092",
    "topic.whitelist": "customers,orders",
    "topic.preserve.partitions": "true",
    "topic.auto.create": "true",
    "topic.config.sync": "true"
  }
}
```

## 8. Performance Optimization
**Producer Optimization**:
```python
from confluent_kafka import Producer

# High-throughput producer configuration
producer_config = {
    'bootstrap.servers': 'localhost:9092',
    'batch.size': 65536,           # Larger batches
    'linger.ms': 10,               # Wait for batching
    'compression.type': 'snappy',   # Compression
    'acks': '1',                   # Faster acknowledgment
    'retries': 3,
    'max.in.flight.requests.per.connection': 5,
    'buffer.memory': 67108864      # 64MB buffer
}

producer = Producer(producer_config)
```

**Consumer Optimization**:
```python
from confluent_kafka import Consumer

# High-throughput consumer configuration
consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'high-throughput-group',
    'fetch.min.bytes': 50000,      # Larger fetch sizes
    'fetch.max.wait.ms': 500,      # Wait for more data
    'max.partition.fetch.bytes': 1048576,  # 1MB per partition
    'session.timeout.ms': 30000,
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_config)
```

## 9. Confluent Cloud
**Cloud-Native Kafka**:
```bash
# Install Confluent CLI
curl -sL --http1.1 https://cnfl.io/cli | sh -s -- latest

# Login to Confluent Cloud
confluent login --save

# Create cluster
confluent kafka cluster create my-cluster \
    --cloud aws \
    --region us-west-2 \
    --type basic

# Create API key
confluent api-key create --resource lkc-12345
```

**Terraform Configuration**:
```hcl
resource "confluent_kafka_cluster" "basic" {
  display_name = "basic_kafka_cluster"
  availability = "SINGLE_ZONE"
  cloud        = "AWS"
  region       = "us-west-2"
  basic {}
  
  environment {
    id = confluent_environment.staging.id
  }
}

resource "confluent_kafka_topic" "customers" {
  kafka_cluster {
    id = confluent_kafka_cluster.basic.id
  }
  topic_name    = "customers"
  partitions_count = 6
  rest_endpoint = confluent_kafka_cluster.basic.rest_endpoint
  
  config = {
    "cleanup.policy"    = "delete"
    "retention.ms"      = "604800000"  # 7 days
    "compression.type"  = "snappy"
  }
}
```

## 10. Monitoring and Observability
**JMX Metrics**:
```yaml
# Key producer metrics
kafka.producer:
  - record-send-rate
  - record-error-rate
  - request-latency-avg
  - batch-size-avg

# Key consumer metrics  
kafka.consumer:
  - records-consumed-rate
  - records-lag-max
  - fetch-latency-avg
  - commit-latency-avg

# Key broker metrics
kafka.server:
  - MessagesInPerSec
  - BytesInPerSec
  - BytesOutPerSec
  - RequestsPerSec
```

**Prometheus Integration**:
```yaml
# JMX Exporter configuration
rules:
  - pattern: kafka.server<type=(.+), name=(.+)PerSec\w*><>Count
    name: kafka_server_$1_$2_total
    type: COUNTER
  - pattern: kafka.server<type=(.+), name=(.+)PerSec\w*, topic=(.+)><>Count
    name: kafka_server_$1_$2_total
    labels:
      topic: "$3"
    type: COUNTER
```