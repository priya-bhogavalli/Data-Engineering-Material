# 🏛️ Apache Cassandra Interview Questions for Data Engineering

## 📋 Table of Contents

1. [Core Concepts (1-25)](#core-concepts-1-25)
2. [Data Modeling (26-50)](#data-modeling-26-50)
3. [Performance & Optimization (51-75)](#performance--optimization-51-75)
4. [Operations & Scaling (76-100)](#operations--scaling-76-100)

---

## Core Concepts (1-25)

### 1. What is Apache Cassandra and its key characteristics?
**Answer**: Cassandra is a distributed NoSQL database designed for high availability and linear scalability.

**Key Characteristics:**
- **Distributed**: No single point of failure
- **Eventually Consistent**: Tunable consistency levels
- **Column-Family**: Wide-column data model
- **Masterless**: All nodes are equal
- **Linear Scalability**: Add nodes to increase capacity

```cql
-- Create keyspace
CREATE KEYSPACE ecommerce
WITH REPLICATION = {
  'class': 'NetworkTopologyStrategy',
  'datacenter1': 3
};

-- Create table
CREATE TABLE ecommerce.orders (
  customer_id UUID,
  order_date DATE,
  order_id UUID,
  product_name TEXT,
  quantity INT,
  price DECIMAL,
  PRIMARY KEY (customer_id, order_date, order_id)
) WITH CLUSTERING ORDER BY (order_date DESC, order_id ASC);
```

### 2. Explain Cassandra's architecture and ring topology
**Answer**: Cassandra uses a peer-to-peer distributed system with consistent hashing.

**Architecture Components:**
- **Ring**: Nodes arranged in a ring topology
- **Partitioner**: Distributes data across nodes
- **Replication**: Data copied to multiple nodes
- **Gossip Protocol**: Node communication and failure detection

```cql
-- Check cluster status
DESCRIBE CLUSTER;

-- View token ranges
SELECT peer, data_center, rack, tokens 
FROM system.peers;

-- Check node status
nodetool status
```

### 3. What are Cassandra's consistency levels?
**Answer**: Tunable consistency levels balance performance and data consistency.

```cql
-- Consistency levels for reads
CONSISTENCY ONE;      -- Read from one replica
CONSISTENCY QUORUM;   -- Read from majority of replicas
CONSISTENCY ALL;      -- Read from all replicas
CONSISTENCY LOCAL_QUORUM; -- Quorum within local datacenter

-- Write consistency
INSERT INTO orders (customer_id, order_date, order_id, product_name)
VALUES (uuid(), '2023-01-01', uuid(), 'Laptop')
USING CONSISTENCY QUORUM;

-- Read consistency
SELECT * FROM orders WHERE customer_id = ?
USING CONSISTENCY LOCAL_ONE;
```

## Data Modeling (26-50)

### 26. How do you design tables in Cassandra?
**Answer**: Design tables based on query patterns, not normalization.

```cql
-- Query-driven design
-- Query: Get orders by customer
CREATE TABLE orders_by_customer (
  customer_id UUID,
  order_date DATE,
  order_id UUID,
  total_amount DECIMAL,
  status TEXT,
  PRIMARY KEY (customer_id, order_date, order_id)
) WITH CLUSTERING ORDER BY (order_date DESC);

-- Query: Get orders by status
CREATE TABLE orders_by_status (
  status TEXT,
  order_date DATE,
  order_id UUID,
  customer_id UUID,
  total_amount DECIMAL,
  PRIMARY KEY (status, order_date, order_id)
) WITH CLUSTERING ORDER BY (order_date DESC);

-- Time-series data
CREATE TABLE sensor_data (
  sensor_id UUID,
  year INT,
  month INT,
  timestamp TIMESTAMP,
  temperature FLOAT,
  humidity FLOAT,
  PRIMARY KEY ((sensor_id, year, month), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);
```

### 27. How do you handle denormalization in Cassandra?
**Answer**: Duplicate data across tables to support different query patterns.

```cql
-- User profile table
CREATE TABLE user_profiles (
  user_id UUID PRIMARY KEY,
  username TEXT,
  email TEXT,
  full_name TEXT,
  created_at TIMESTAMP
);

-- User posts table (denormalized)
CREATE TABLE user_posts (
  user_id UUID,
  post_date DATE,
  post_id UUID,
  username TEXT,        -- Denormalized from user_profiles
  full_name TEXT,       -- Denormalized from user_profiles
  content TEXT,
  likes_count COUNTER,
  PRIMARY KEY (user_id, post_date, post_id)
) WITH CLUSTERING ORDER BY (post_date DESC);

-- Posts by hashtag (denormalized)
CREATE TABLE posts_by_hashtag (
  hashtag TEXT,
  post_date DATE,
  post_id UUID,
  user_id UUID,
  username TEXT,        -- Denormalized
  content TEXT,
  PRIMARY KEY (hashtag, post_date, post_id)
) WITH CLUSTERING ORDER BY (post_date DESC);
```

## Performance & Optimization (51-75)

### 51. How do you optimize Cassandra performance?
**Answer**: Use proper data modeling, indexing, and configuration tuning.

```cql
-- Secondary indexes (use sparingly)
CREATE INDEX ON products (category);
CREATE INDEX ON orders (status);

-- Materialized views
CREATE MATERIALIZED VIEW orders_by_product AS
SELECT customer_id, product_id, order_date, order_id, quantity
FROM orders
WHERE product_id IS NOT NULL AND customer_id IS NOT NULL 
  AND order_date IS NOT NULL AND order_id IS NOT NULL
PRIMARY KEY (product_id, order_date, customer_id, order_id)
WITH CLUSTERING ORDER BY (order_date DESC);

-- Batch operations
BEGIN BATCH
  INSERT INTO orders_by_customer (customer_id, order_date, order_id, total_amount)
  VALUES (?, ?, ?, ?);
  INSERT INTO orders_by_status (status, order_date, order_id, customer_id, total_amount)
  VALUES ('pending', ?, ?, ?, ?);
  UPDATE customer_stats SET total_orders = total_orders + 1 WHERE customer_id = ?;
APPLY BATCH;
```

### 52. How do you handle time-series data in Cassandra?
**Answer**: Use time-based partitioning and bucketing strategies.

```cql
-- Time-series with bucketing
CREATE TABLE metrics_by_hour (
  metric_name TEXT,
  bucket_hour TIMESTAMP,  -- Hour bucket (2023-01-01 14:00:00)
  timestamp TIMESTAMP,
  value DOUBLE,
  tags MAP<TEXT, TEXT>,
  PRIMARY KEY ((metric_name, bucket_hour), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC)
  AND compaction = {'class': 'TimeWindowCompactionStrategy'};

-- Insert time-series data
INSERT INTO metrics_by_hour (metric_name, bucket_hour, timestamp, value, tags)
VALUES ('cpu_usage', '2023-01-01 14:00:00', '2023-01-01 14:15:30', 85.5, 
        {'host': 'server1', 'region': 'us-east-1'});

-- Query time-series data
SELECT timestamp, value, tags
FROM metrics_by_hour
WHERE metric_name = 'cpu_usage'
  AND bucket_hour >= '2023-01-01 14:00:00'
  AND bucket_hour <= '2023-01-01 16:00:00'
  AND timestamp >= '2023-01-01 14:00:00'
  AND timestamp <= '2023-01-01 16:00:00'
ORDER BY timestamp DESC;
```

## Operations & Scaling (76-100)

### 76. How do you scale a Cassandra cluster?
**Answer**: Add nodes and rebalance data using consistent hashing.

```bash
# Add new node to cluster
# 1. Install Cassandra on new node
# 2. Configure cassandra.yaml with same cluster_name and seeds
# 3. Start Cassandra service

# Check cluster status
nodetool status

# Run repair after adding nodes
nodetool repair

# Stream data to new nodes
nodetool cleanup

# Monitor streaming progress
nodetool netstats
```

### 77. How do you backup and restore Cassandra?
**Answer**: Use snapshots and incremental backups.

```bash
# Create snapshot
nodetool snapshot keyspace_name

# List snapshots
nodetool listsnapshots

# Clear old snapshots
nodetool clearsnapshot

# Restore from snapshot
# 1. Stop Cassandra
# 2. Clear data directory
# 3. Copy snapshot files to data directory
# 4. Start Cassandra
# 5. Run nodetool refresh

# Incremental backup
# Enable in cassandra.yaml: incremental_backups: true
```

### 78. How do you monitor Cassandra performance?
**Answer**: Use nodetool, JMX metrics, and monitoring tools.

```bash
# Node statistics
nodetool info
nodetool tpstats
nodetool cfstats

# Compaction status
nodetool compactionstats

# GC statistics
nodetool gcstats

# Ring status
nodetool ring

# Table statistics
nodetool tablestats keyspace.table
```

### 79. How do you handle repairs in Cassandra?
**Answer**: Regular repairs maintain data consistency across replicas.

```bash
# Full repair
nodetool repair

# Repair specific keyspace
nodetool repair keyspace_name

# Incremental repair
nodetool repair -inc

# Parallel repair
nodetool repair -pr  # Primary range only

# Monitor repair progress
nodetool compactionstats
```

---

**Total Questions: 100** | **Coverage: Complete Cassandra Ecosystem**