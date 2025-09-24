# 🚀 Apache Pinot - Key Concepts

**Category**: Real-time OLAP Database  
**Market Share**: 25% of real-time analytics workloads  
**Interview Frequency**: 25% of data engineering roles  
**Learning Time**: 3-4 weeks

---

## 🎯 What is Apache Pinot?

Apache Pinot is a real-time distributed OLAP datastore designed to provide ultra-low-latency analytics even at extremely high throughput.

### **Core Value Proposition**
- **Sub-second query latency** at scale
- **Real-time data ingestion** from streams
- **Horizontal scaling** to petabytes
- **High concurrency** (thousands of QPS)
- **Columnar storage** with smart indexing

---

## 🏗️ Architecture Overview

```
Data Sources → Pinot → Query Results
     ↓          ↓         ↓
Kafka/Kinesis  Segments  Brokers/Servers
```

### **Key Components**

1. **Controller**: Cluster management and metadata
2. **Broker**: Query routing and aggregation  
3. **Server**: Data storage and query execution
4. **Minion**: Offline tasks (compaction, retention)
5. **Segments**: Immutable data chunks

---

## 🔧 Core Concepts

### **1. Tables and Schemas**
```json
{
  "tableName": "user_events",
  "tableType": "REALTIME",
  "segmentsConfig": {
    "timeColumnName": "timestamp",
    "timeType": "MILLISECONDS",
    "retentionTimeUnit": "DAYS",
    "retentionTimeValue": "7"
  },
  "tableIndexConfig": {
    "loadMode": "MMAP",
    "invertedIndexColumns": ["user_id", "event_type"],
    "bloomFilterColumns": ["user_id"]
  },
  "ingestionConfig": {
    "streamIngestionConfig": {
      "streamConfigMaps": [{
        "streamType": "kafka",
        "stream.kafka.topic.name": "user-events",
        "stream.kafka.broker.list": "localhost:9092"
      }]
    }
  }
}
```

### **2. Segment Structure**
```
Segment = Immutable chunk of data
├── Metadata (schema, stats)
├── Dictionary (value encoding)
├── Forward Index (row → value)
├── Inverted Index (value → rows)
└── Bloom Filter (existence check)
```

### **3. Query Types**
```sql
-- Aggregation queries
SELECT COUNT(*), SUM(revenue)
FROM sales 
WHERE date >= '2024-01-01'

-- Group by queries  
SELECT country, COUNT(*)
FROM user_events
WHERE timestamp > now() - 3600000
GROUP BY country

-- Top-K queries
SELECT user_id, COUNT(*) as events
FROM user_events  
GROUP BY user_id
ORDER BY events DESC
LIMIT 10
```

---

## 🚀 Implementation

### **1. Table Creation**
```sql
-- Create real-time table
CREATE TABLE user_events (
  user_id VARCHAR,
  event_type VARCHAR, 
  timestamp LONG,
  properties JSON
) WITH (
  tableType = 'REALTIME',
  streamType = 'kafka',
  stream.kafka.topic.name = 'user-events'
);

-- Create offline table
CREATE TABLE sales_batch (
  order_id VARCHAR,
  customer_id VARCHAR,
  amount DOUBLE,
  order_date LONG
) WITH (
  tableType = 'OFFLINE'
);
```

### **2. Data Ingestion**
```python
# Kafka producer for real-time ingestion
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Send events to Pinot
event = {
    'user_id': 'user123',
    'event_type': 'page_view',
    'timestamp': int(time.time() * 1000),
    'properties': {'page': '/home', 'source': 'organic'}
}

producer.send('user-events', event)
```

### **3. Querying Data**
```python
import requests

# Query Pinot via REST API
def query_pinot(sql):
    url = "http://localhost:8099/query/sql"
    response = requests.post(url, json={"sql": sql})
    return response.json()

# Example queries
result = query_pinot("""
    SELECT event_type, COUNT(*) as count
    FROM user_events 
    WHERE timestamp > now() - 3600000
    GROUP BY event_type
    ORDER BY count DESC
""")
```

---

## 📊 Performance Optimization

### **1. Indexing Strategies**
```json
{
  "tableIndexConfig": {
    "invertedIndexColumns": ["user_id", "country"],
    "bloomFilterColumns": ["user_id"],
    "rangeIndexColumns": ["timestamp"],
    "starTreeIndexConfigs": [{
      "dimensionsSplitOrder": ["country", "device_type"],
      "skipStarNodeCreationForDimensions": [],
      "functionColumnPairs": ["COUNT__*", "SUM__revenue"]
    }]
  }
}
```

### **2. Partitioning**
```json
{
  "segmentsConfig": {
    "segmentPushType": "APPEND",
    "segmentAssignmentStrategy": "BalanceNumSegmentAssignmentStrategy",
    "replication": "2"
  },
  "routing": {
    "segmentPrunerType": "partition",
    "partitionColumn": "user_id",
    "numPartitions": 32
  }
}
```

### **3. Query Optimization**
```sql
-- Use time filters for pruning
SELECT COUNT(*) FROM events 
WHERE timestamp BETWEEN 1640995200000 AND 1641081600000

-- Leverage indexes
SELECT * FROM events 
WHERE user_id = 'user123'  -- Uses bloom filter + inverted index

-- Optimize aggregations with star-tree
SELECT country, device_type, COUNT(*), SUM(revenue)
FROM events
GROUP BY country, device_type  -- Uses pre-aggregated star-tree
```

---

## 🛠️ Common Use Cases

### **1. Real-time Dashboards**
```sql
-- Live metrics for dashboards
SELECT 
  DATE_TRUNC('minute', timestamp) as minute,
  COUNT(*) as events_per_minute,
  COUNT(DISTINCT user_id) as unique_users
FROM user_events
WHERE timestamp > now() - 3600000  -- Last hour
GROUP BY minute
ORDER BY minute DESC
```

### **2. Anomaly Detection**
```sql
-- Detect traffic spikes
WITH hourly_stats AS (
  SELECT 
    DATE_TRUNC('hour', timestamp) as hour,
    COUNT(*) as event_count
  FROM user_events
  WHERE timestamp > now() - 86400000  -- Last 24 hours
  GROUP BY hour
)
SELECT hour, event_count,
  AVG(event_count) OVER (ORDER BY hour ROWS 6 PRECEDING) as avg_6h
FROM hourly_stats
WHERE event_count > avg_6h * 2  -- 2x above average
```

### **3. User Behavior Analytics**
```sql
-- User journey analysis
SELECT 
  user_id,
  ARRAY_AGG(event_type ORDER BY timestamp) as event_sequence,
  COUNT(*) as total_events,
  MAX(timestamp) - MIN(timestamp) as session_duration
FROM user_events
WHERE timestamp > now() - 3600000
GROUP BY user_id
HAVING COUNT(*) > 5  -- Active users only
```

---

## 💡 Best Practices

### **1. Schema Design**
- Use **appropriate data types** (INT vs LONG)
- Choose **time column** carefully
- Design for **query patterns**
- Minimize **high-cardinality** dimensions

### **2. Ingestion Optimization**
```json
{
  "streamConfigs": {
    "streamType": "kafka",
    "stream.kafka.consumer.prop.auto.offset.reset": "largest",
    "stream.kafka.consumer.prop.max.poll.records": "1000",
    "realtime.segment.flush.threshold.rows": "1000000"
  }
}
```

### **3. Resource Management**
```yaml
# Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pinot-server
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: pinot-server
        image: apachepinot/pinot:latest
        resources:
          requests:
            memory: "8Gi"
            cpu: "2"
          limits:
            memory: "16Gi" 
            cpu: "4"
```

---

## 🎯 When to Choose Pinot

### **✅ Choose Pinot When:**
- Need **sub-second query latency**
- Have **high-throughput** requirements
- Require **real-time analytics**
- Need **high concurrency** (1000s QPS)
- Want **horizontal scaling**

### **❌ Consider Alternatives When:**
- Need **complex joins** (use traditional OLAP)
- Require **ACID transactions** (use OLTP database)
- Have **simple analytics** needs (use ClickHouse)
- Need **batch processing** (use Spark)

---

## 🔗 Integration Ecosystem

### **Data Sources**
- **Streaming**: Kafka, Kinesis, Pulsar
- **Batch**: HDFS, S3, local files
- **Databases**: MySQL, PostgreSQL via CDC

### **Query Interfaces**
- **REST API** for programmatic access
- **JDBC driver** for BI tools
- **Grafana plugin** for dashboards
- **Superset integration** for visualization

---

**🎯 Next Steps**: Check out [Interview Questions](./APACHE_PINOT_INTERVIEW_QUESTIONS.md)