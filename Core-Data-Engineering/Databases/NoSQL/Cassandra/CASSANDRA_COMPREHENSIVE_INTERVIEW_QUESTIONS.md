# Cassandra Comprehensive Interview Questions for Data Engineering

## 📋 Table of Contents

1. [Core Concepts Questions (1-25)](#core-concepts-questions-1-25)
2. [Data Modeling Questions (26-50)](#data-modeling-questions-26-50)
3. [Performance & Operations (51-75)](#performance--operations-51-75)
4. [Advanced Topics (76-100)](#advanced-topics-76-100)

---

## 🎯 **Introduction**

Apache Cassandra is a distributed NoSQL database designed for handling large amounts of data across many commodity servers, providing high availability with no single point of failure.

**Why Cassandra is Critical for Data Engineers:**
- **Linear Scalability**: Add nodes to increase capacity
- **High Availability**: No single point of failure
- **Eventual Consistency**: Tunable consistency levels
- **Write Optimization**: Optimized for write-heavy workloads
- **Multi-datacenter Support**: Built-in replication across datacenters

---

## Core Concepts Questions (1-25)

### 1. What is Apache Cassandra and how does it differ from relational databases?
**Answer**: 
Cassandra is a distributed NoSQL database designed for scalability and high availability.

**Key Differences:**

| Aspect | Cassandra | Relational Databases |
|--------|-----------|---------------------|
| **Data Model** | Wide-column store | Relational tables |
| **Schema** | Flexible schema | Fixed schema |
| **ACID Properties** | Eventually consistent | ACID compliant |
| **Scaling** | Horizontal scaling | Vertical scaling |
| **Joins** | No joins | Complex joins supported |
| **CAP Theorem** | AP (Availability + Partition tolerance) | CA (Consistency + Availability) |

```cql
-- Cassandra CQL example
CREATE KEYSPACE ecommerce 
WITH replication = {
  'class': 'SimpleStrategy',
  'replication_factor': 3
};

CREATE TABLE ecommerce.orders (
  customer_id UUID,
  order_date DATE,
  order_id UUID,
  product_name TEXT,
  quantity INT,
  price DECIMAL,
  PRIMARY KEY (customer_id, order_date, order_id)
);
```

### 2. Explain Cassandra's architecture and key components.
**Answer**: 
Cassandra uses a peer-to-peer distributed architecture:

**Core Components:**
- **Node**: Individual Cassandra server
- **Cluster**: Collection of nodes
- **Ring**: Logical arrangement of nodes
- **Gossip Protocol**: Node communication mechanism
- **Snitch**: Determines network topology
- **Partitioner**: Distributes data across nodes

**Architecture Diagram:**
```
    Node A ←→ Node B
      ↑         ↓
    Node D ←→ Node C
    
Each node:
- Stores data partitions
- Handles read/write requests
- Participates in gossip protocol
- Maintains replica data
```

### 3. What is the CAP theorem and how does Cassandra implement it?
**Answer**: 
CAP theorem states you can only guarantee two of: Consistency, Availability, Partition tolerance.

**Cassandra's CAP Implementation:**
- **Partition Tolerance**: Always maintained (distributed system)
- **Availability**: Prioritized over consistency
- **Consistency**: Tunable consistency levels

```cql
-- Tunable consistency examples
-- Strong consistency
SELECT * FROM orders WHERE customer_id = ? 
USING CONSISTENCY QUORUM;

-- Eventual consistency
SELECT * FROM orders WHERE customer_id = ? 
USING CONSISTENCY ONE;

-- Write with consistency level
INSERT INTO orders (customer_id, order_date, order_id, product_name)
VALUES (?, ?, ?, ?)
USING CONSISTENCY ALL;
```

**Consistency Levels:**
- **ONE**: Any single replica
- **QUORUM**: Majority of replicas
- **ALL**: All replicas
- **LOCAL_QUORUM**: Majority in local datacenter

### 4. How does data partitioning work in Cassandra?
**Answer**: 
Cassandra uses consistent hashing for data distribution:

**Partitioning Process:**
1. **Partition Key**: Determines which node stores data
2. **Hash Function**: Converts partition key to token
3. **Token Ring**: Maps tokens to nodes
4. **Replication**: Copies data to multiple nodes

```cql
-- Partition key examples
CREATE TABLE user_profiles (
  user_id UUID,           -- Partition key
  name TEXT,
  email TEXT,
  created_date TIMESTAMP,
  PRIMARY KEY (user_id)
);

-- Composite partition key
CREATE TABLE time_series_data (
  sensor_id TEXT,
  date DATE,              -- Partition key components
  timestamp TIMESTAMP,    -- Clustering key
  temperature DOUBLE,
  humidity DOUBLE,
  PRIMARY KEY ((sensor_id, date), timestamp)
);
```

**Token Distribution:**
```bash
# View token ranges
nodetool ring

# Check partition key token
SELECT token(user_id), user_id FROM user_profiles;
```

### 5. What are clustering keys and how do they work?
**Answer**: 
Clustering keys determine data ordering within partitions:

```cql
-- Clustering key example
CREATE TABLE user_events (
  user_id UUID,
  event_time TIMESTAMP,
  event_type TEXT,
  event_data TEXT,
  PRIMARY KEY (user_id, event_time, event_type)
);
-- user_id: partition key
-- event_time, event_type: clustering keys
```

**Clustering Benefits:**
- **Ordering**: Data sorted by clustering keys
- **Range Queries**: Efficient range scans
- **Uniqueness**: Combined with partition key for uniqueness

```cql
-- Efficient range queries with clustering
SELECT * FROM user_events 
WHERE user_id = ? 
  AND event_time >= '2024-01-01'
  AND event_time < '2024-02-01'
ORDER BY event_time DESC;
```

### 6. How does replication work in Cassandra?
**Answer**: 
Cassandra replicates data across multiple nodes for fault tolerance:

**Replication Strategies:**
```cql
-- Simple Strategy (single datacenter)
CREATE KEYSPACE simple_ks 
WITH replication = {
  'class': 'SimpleStrategy',
  'replication_factor': 3
};

-- Network Topology Strategy (multi-datacenter)
CREATE KEYSPACE multi_dc_ks 
WITH replication = {
  'class': 'NetworkTopologyStrategy',
  'datacenter1': 3,
  'datacenter2': 2
};
```

**Replica Placement:**
- **Primary Replica**: Node determined by partition key hash
- **Additional Replicas**: Next N nodes in ring
- **Rack Awareness**: Distributes replicas across racks

```bash
# Check replica locations
nodetool getendpoints keyspace_name table_name partition_key
```

### 7. What are the different consistency levels in Cassandra?
**Answer**: 
Consistency levels control read/write behavior:

**Write Consistency Levels:**
```cql
-- Write to all replicas
INSERT INTO users (id, name) VALUES (?, ?)
USING CONSISTENCY ALL;

-- Write to majority of replicas
INSERT INTO users (id, name) VALUES (?, ?)
USING CONSISTENCY QUORUM;

-- Write to any single replica
INSERT INTO users (id, name) VALUES (?, ?)
USING CONSISTENCY ONE;
```

**Read Consistency Levels:**
```cql
-- Read from all replicas
SELECT * FROM users WHERE id = ?
USING CONSISTENCY ALL;

-- Read from majority
SELECT * FROM users WHERE id = ?
USING CONSISTENCY QUORUM;

-- Read from fastest replica
SELECT * FROM users WHERE id = ?
USING CONSISTENCY ONE;
```

**Consistency Level Matrix:**
| Level | Replicas | Use Case |
|-------|----------|----------|
| ONE | 1 | High performance, eventual consistency |
| QUORUM | Majority | Balanced consistency/performance |
| ALL | All | Strong consistency, lower availability |
| LOCAL_QUORUM | Local DC majority | Multi-DC with local consistency |

### 8. How do you handle data modeling in Cassandra?
**Answer**: 
Cassandra data modeling is query-driven:

**Modeling Principles:**
1. **Denormalization**: Duplicate data for query efficiency
2. **Query-First Design**: Model based on access patterns
3. **Partition Size**: Keep partitions under 100MB
4. **Avoid Hot Partitions**: Distribute load evenly

```cql
-- Query-driven modeling example
-- Query: Get user's recent orders
CREATE TABLE orders_by_user (
  user_id UUID,
  order_date DATE,
  order_id UUID,
  total_amount DECIMAL,
  status TEXT,
  PRIMARY KEY (user_id, order_date, order_id)
) WITH CLUSTERING ORDER BY (order_date DESC, order_id ASC);

-- Query: Get orders by status
CREATE TABLE orders_by_status (
  status TEXT,
  order_date DATE,
  order_id UUID,
  user_id UUID,
  total_amount DECIMAL,
  PRIMARY KEY (status, order_date, order_id)
) WITH CLUSTERING ORDER BY (order_date DESC);
```

### 9. What are secondary indexes and when should you use them?
**Answer**: 
Secondary indexes allow queries on non-primary key columns:

```cql
-- Create secondary index
CREATE INDEX ON users (email);
CREATE INDEX ON orders (status);

-- Query using secondary index
SELECT * FROM users WHERE email = 'user@example.com';
SELECT * FROM orders WHERE status = 'pending';
```

**When to Use Secondary Indexes:**
- **Low Cardinality**: Columns with few distinct values
- **Small Result Sets**: Queries returning few rows
- **Infrequent Queries**: Not performance-critical queries

**Alternatives to Secondary Indexes:**
```cql
-- Materialized views (preferred)
CREATE MATERIALIZED VIEW users_by_email AS
  SELECT * FROM users
  WHERE email IS NOT NULL
  PRIMARY KEY (email, user_id);

-- Manual denormalization
CREATE TABLE user_lookup_by_email (
  email TEXT,
  user_id UUID,
  name TEXT,
  PRIMARY KEY (email)
);
```

### 10. How does Cassandra handle writes and reads?
**Answer**: 
Cassandra optimizes for write performance:

**Write Path:**
1. **Commit Log**: Write-ahead log for durability
2. **Memtable**: In-memory structure
3. **SSTable**: Immutable disk files
4. **Compaction**: Merge SSTables

```cql
-- Write operations
INSERT INTO users (id, name, email, created_at)
VALUES (uuid(), 'John Doe', 'john@example.com', toTimestamp(now()));

-- Upsert behavior (INSERT/UPDATE same syntax)
UPDATE users SET email = 'newemail@example.com' WHERE id = ?;
```

**Read Path:**
1. **Memtable Check**: Check in-memory data
2. **SSTable Scan**: Read from disk files
3. **Merge Results**: Combine data from multiple sources
4. **Return Latest**: Based on timestamp

```cql
-- Read operations
SELECT * FROM users WHERE id = ?;

-- Range queries (requires clustering key)
SELECT * FROM user_events 
WHERE user_id = ? 
  AND event_time >= ? 
  AND event_time <= ?;
```

---

## Data Modeling Questions (26-50)

### 26. How do you design tables for time-series data?
**Answer**: 
Time-series data requires careful partitioning strategy:

```cql
-- Time-series table design
CREATE TABLE sensor_data (
  sensor_id TEXT,
  bucket DATE,           -- Partition by day/hour
  timestamp TIMESTAMP,
  temperature DOUBLE,
  humidity DOUBLE,
  pressure DOUBLE,
  PRIMARY KEY ((sensor_id, bucket), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);

-- Bucketing strategy for high-volume data
CREATE TABLE metrics_by_hour (
  metric_name TEXT,
  hour_bucket TIMESTAMP,  -- Truncated to hour
  timestamp TIMESTAMP,
  value DOUBLE,
  tags MAP<TEXT, TEXT>,
  PRIMARY KEY ((metric_name, hour_bucket), timestamp)
);
```

**Time-Series Best Practices:**
- **Bucket Data**: Partition by time periods
- **TTL Usage**: Automatic data expiration
- **Compaction Strategy**: Use TimeWindowCompactionStrategy

```cql
-- TTL for automatic cleanup
INSERT INTO sensor_data (sensor_id, bucket, timestamp, temperature)
VALUES (?, ?, ?, ?)
USING TTL 2592000; -- 30 days

-- Table-level TTL
CREATE TABLE logs (
  id UUID,
  message TEXT,
  timestamp TIMESTAMP,
  PRIMARY KEY (id)
) WITH default_time_to_live = 604800; -- 7 days
```

### 27. How do you handle many-to-many relationships?
**Answer**: 
Cassandra handles many-to-many through denormalization:

```cql
-- Many-to-many: Users and Groups
-- Table 1: Users by Group
CREATE TABLE users_by_group (
  group_id UUID,
  user_id UUID,
  user_name TEXT,
  joined_date TIMESTAMP,
  role TEXT,
  PRIMARY KEY (group_id, user_id)
);

-- Table 2: Groups by User
CREATE TABLE groups_by_user (
  user_id UUID,
  group_id UUID,
  group_name TEXT,
  joined_date TIMESTAMP,
  role TEXT,
  PRIMARY KEY (user_id, group_id)
);
```

**Maintaining Consistency:**
```cql
-- Use batches for atomic updates
BEGIN BATCH
  INSERT INTO users_by_group (group_id, user_id, user_name, joined_date, role)
  VALUES (?, ?, ?, ?, ?);
  
  INSERT INTO groups_by_user (user_id, group_id, group_name, joined_date, role)
  VALUES (?, ?, ?, ?, ?);
APPLY BATCH;
```

### 28. How do you implement counters in Cassandra?
**Answer**: 
Cassandra provides distributed counters:

```cql
-- Counter table
CREATE TABLE page_views (
  page_url TEXT,
  view_count COUNTER,
  PRIMARY KEY (page_url)
);

-- Counter operations
UPDATE page_views SET view_count = view_count + 1 
WHERE page_url = '/home';

UPDATE page_views SET view_count = view_count + 5 
WHERE page_url = '/products';

-- Read counter
SELECT page_url, view_count FROM page_views;
```

**Counter Limitations:**
- Cannot mix counters with other column types
- Cannot use INSERT statements
- Eventual consistency issues
- Cannot reset to specific value

**Alternative Approaches:**
```cql
-- Time-based counting
CREATE TABLE page_view_events (
  page_url TEXT,
  hour_bucket TIMESTAMP,
  view_id UUID,
  user_id UUID,
  timestamp TIMESTAMP,
  PRIMARY KEY ((page_url, hour_bucket), view_id)
);

-- Aggregate in application
SELECT COUNT(*) FROM page_view_events 
WHERE page_url = ? AND hour_bucket = ?;
```

---

## Performance & Operations (51-75)

### 51. How do you optimize Cassandra performance?
**Answer**: 
Performance optimization involves multiple strategies:

**Hardware Optimization:**
```yaml
# cassandra.yaml optimizations
# Memory settings
memtable_heap_space_in_mb: 2048
memtable_offheap_space_in_mb: 2048

# Disk settings
commitlog_directory: /fast-ssd/commitlog
data_file_directories: [/data-ssd/data]

# Network settings
rpc_server_type: sync
rpc_min_threads: 16
rpc_max_threads: 2048
```

**Query Optimization:**
```cql
-- Use partition key in WHERE clause
SELECT * FROM orders WHERE customer_id = ?; -- Good

-- Avoid full table scans
SELECT * FROM orders; -- Bad

-- Use clustering key for range queries
SELECT * FROM user_events 
WHERE user_id = ? 
  AND event_time >= ? 
  AND event_time <= ?; -- Good

-- Limit result size
SELECT * FROM large_table WHERE id = ? LIMIT 100;
```

**Compaction Strategy:**
```cql
-- Size-tiered compaction (default)
ALTER TABLE users WITH compaction = {
  'class': 'SizeTieredCompactionStrategy',
  'max_threshold': 32,
  'min_threshold': 4
};

-- Leveled compaction (read-heavy)
ALTER TABLE user_profiles WITH compaction = {
  'class': 'LeveledCompactionStrategy',
  'sstable_size_in_mb': 160
};

-- Time window compaction (time-series)
ALTER TABLE sensor_data WITH compaction = {
  'class': 'TimeWindowCompactionStrategy',
  'compaction_window_unit': 'DAYS',
  'compaction_window_size': 1
};
```

### 52. How do you monitor Cassandra clusters?
**Answer**: 
Monitoring involves multiple tools and metrics:

**Key Metrics to Monitor:**
```bash
# Node status
nodetool status

# Ring information
nodetool ring

# Compaction stats
nodetool compactionstats

# Thread pool stats
nodetool tpstats

# GC stats
nodetool gcstats

# Heap usage
nodetool info
```

**JMX Metrics:**
```java
// Key JMX metrics to monitor
org.apache.cassandra.metrics:type=Storage,name=Load
org.apache.cassandra.metrics:type=ClientRequest,scope=Read,name=Latency
org.apache.cassandra.metrics:type=ClientRequest,scope=Write,name=Latency
org.apache.cassandra.metrics:type=Compaction,name=PendingTasks
org.apache.cassandra.metrics:type=DroppedMessage,scope=MUTATION,name=Dropped
```

**Monitoring Setup:**
```yaml
# Prometheus configuration
- job_name: 'cassandra'
  static_configs:
    - targets: ['cassandra1:7070', 'cassandra2:7070', 'cassandra3:7070']
  metrics_path: /metrics
  scrape_interval: 15s
```

### 53. How do you handle backup and restore in Cassandra?
**Answer**: 
Cassandra provides multiple backup strategies:

**Snapshot Backups:**
```bash
# Create snapshot
nodetool snapshot -t backup_20240115 keyspace_name

# List snapshots
nodetool listsnapshots

# Clear old snapshots
nodetool clearsnapshot -t backup_20240115

# Restore from snapshot
# 1. Stop Cassandra
# 2. Copy snapshot files to data directory
# 3. Start Cassandra
# 4. Run repair
nodetool repair
```

**Incremental Backups:**
```yaml
# Enable incremental backups in cassandra.yaml
incremental_backups: true

# Backup files created in backups/ directory
# Copy incremental backup files regularly
```

**Point-in-Time Recovery:**
```bash
# Using commit log replay
# 1. Restore from snapshot
# 2. Replay commit logs from backup time
# 3. Truncate to specific timestamp

# Automated backup script
#!/bin/bash
KEYSPACE="ecommerce"
BACKUP_DIR="/backups/$(date +%Y%m%d_%H%M%S)"

# Create snapshot
nodetool snapshot -t "backup_$(date +%Y%m%d_%H%M%S)" $KEYSPACE

# Copy to backup location
mkdir -p $BACKUP_DIR
cp -r /var/lib/cassandra/data/$KEYSPACE/*/snapshots/* $BACKUP_DIR/

# Upload to cloud storage
aws s3 sync $BACKUP_DIR s3://cassandra-backups/
```

### 54. How do you handle cluster scaling?
**Answer**: 
Cassandra supports horizontal scaling:

**Adding Nodes:**
```bash
# 1. Install Cassandra on new node
# 2. Configure cassandra.yaml
cluster_name: 'Production Cluster'
seeds: "existing_node1,existing_node2"
listen_address: new_node_ip
rpc_address: new_node_ip

# 3. Start Cassandra
sudo service cassandra start

# 4. Check cluster status
nodetool status

# 5. Run cleanup on existing nodes
nodetool cleanup
```

**Removing Nodes:**
```bash
# Graceful node removal
nodetool decommission

# Force removal (if node is down)
nodetool removenode node_id

# Check status
nodetool status
```

**Rebalancing Data:**
```bash
# After adding/removing nodes
nodetool repair -pr  # Primary range repair
nodetool cleanup     # Remove unnecessary data
```

---

## Advanced Topics (76-100)

### 76. How do you implement multi-datacenter replication?
**Answer**: 
Multi-datacenter setup provides geographic distribution:

**Network Topology Strategy:**
```cql
CREATE KEYSPACE global_app 
WITH replication = {
  'class': 'NetworkTopologyStrategy',
  'us_east': 3,
  'us_west': 3,
  'europe': 2
};
```

**Snitch Configuration:**
```yaml
# cassandra.yaml
endpoint_snitch: GossipingPropertyFileSnitch

# cassandra-rackdc.properties
dc=us_east
rack=rack1
```

**Cross-DC Consistency:**
```cql
-- Local consistency (within datacenter)
SELECT * FROM users WHERE id = ?
USING CONSISTENCY LOCAL_QUORUM;

-- Global consistency (across datacenters)
SELECT * FROM users WHERE id = ?
USING CONSISTENCY EACH_QUORUM;
```

**DC-Aware Load Balancing:**
```java
// Java driver configuration
Cluster cluster = Cluster.builder()
    .addContactPoint("127.0.0.1")
    .withLoadBalancingPolicy(
        DCAwareRoundRobinPolicy.builder()
            .withLocalDc("us_east")
            .build())
    .build();
```

### 77. How do you implement security in Cassandra?
**Answer**: 
Cassandra provides comprehensive security features:

**Authentication:**
```yaml
# cassandra.yaml
authenticator: PasswordAuthenticator
authorizer: CassandraAuthorizer

# Enable SSL
client_encryption_options:
  enabled: true
  keystore: /path/to/keystore
  keystore_password: password
```

**User Management:**
```cql
-- Create users
CREATE USER admin WITH PASSWORD 'admin_password' SUPERUSER;
CREATE USER app_user WITH PASSWORD 'app_password';

-- Grant permissions
GRANT SELECT ON KEYSPACE ecommerce TO app_user;
GRANT MODIFY ON TABLE ecommerce.orders TO app_user;

-- Revoke permissions
REVOKE SELECT ON KEYSPACE ecommerce FROM app_user;
```

**Role-Based Access Control:**
```cql
-- Create roles
CREATE ROLE read_only;
CREATE ROLE data_analyst;

-- Grant permissions to roles
GRANT SELECT ON ALL KEYSPACES TO read_only;
GRANT SELECT, MODIFY ON KEYSPACE analytics TO data_analyst;

-- Assign roles to users
GRANT read_only TO app_user;
GRANT data_analyst TO analyst_user;
```

### 78. How do you handle data consistency and conflict resolution?
**Answer**: 
Cassandra uses timestamps for conflict resolution:

**Last-Write-Wins:**
```cql
-- Cassandra uses timestamps for conflict resolution
INSERT INTO users (id, name, email) 
VALUES (?, ?, ?) 
USING TIMESTAMP 1642291200000000; -- Microseconds

-- Higher timestamp wins
UPDATE users SET name = 'Updated Name' 
WHERE id = ? 
USING TIMESTAMP 1642291260000000;
```

**Lightweight Transactions (Compare-and-Set):**
```cql
-- Conditional inserts
INSERT INTO users (id, name, email) 
VALUES (?, ?, ?) 
IF NOT EXISTS;

-- Conditional updates
UPDATE users SET email = ? 
WHERE id = ? 
IF email = 'old@example.com';

-- Check result
-- Applied: true/false
-- Existing data if not applied
```

**Application-Level Consistency:**
```java
// Version-based optimistic locking
public class User {
    private UUID id;
    private String name;
    private String email;
    private long version;
    
    public void updateWithVersion(String newEmail) {
        PreparedStatement stmt = session.prepare(
            "UPDATE users SET email = ?, version = ? " +
            "WHERE id = ? IF version = ?");
        
        ResultSet rs = session.execute(stmt.bind(
            newEmail, version + 1, id, version));
        
        if (!rs.one().getBool("[applied]")) {
            throw new OptimisticLockException();
        }
        
        this.email = newEmail;
        this.version++;
    }
}
```

---

## 📚 **Cassandra Study Guide & Best Practices**

### 🎯 **Essential Cassandra Concepts for Data Engineers**

#### **Core Architecture Understanding**
1. **Distributed Architecture**: Peer-to-peer, no single point of failure
2. **Consistent Hashing**: Data distribution across nodes
3. **Replication Strategy**: Data redundancy and availability
4. **Gossip Protocol**: Node communication and failure detection
5. **Tunable Consistency**: Balance between consistency and availability

#### **Data Modeling Mastery**
1. **Query-Driven Design**: Model based on access patterns
2. **Denormalization**: Duplicate data for query efficiency
3. **Partition Key Selection**: Ensure even data distribution
4. **Clustering Key Usage**: Enable range queries and ordering
5. **Secondary Index Alternatives**: Materialized views and manual denormalization

#### **Performance Optimization**
1. **Compaction Strategies**: Choose based on workload patterns
2. **Memory Management**: Optimize memtable and cache settings
3. **Disk I/O**: Separate commit log and data directories
4. **Query Patterns**: Avoid anti-patterns like full table scans
5. **Monitoring**: Track key metrics and performance indicators

### 🚀 **Production-Ready Cassandra Patterns**

#### **High Availability Configuration**
```yaml
# Multi-datacenter setup
endpoint_snitch: GossipingPropertyFileSnitch
num_tokens: 256
auto_bootstrap: true

# Replication
CREATE KEYSPACE production 
WITH replication = {
  'class': 'NetworkTopologyStrategy',
  'datacenter1': 3,
  'datacenter2': 2
};
```

#### **Monitoring and Alerting**
```bash
# Key metrics to monitor
- Node availability and health
- Read/write latency percentiles
- Compaction pending tasks
- Heap memory usage
- Disk space utilization
- Dropped mutations
```

### 🎓 **Interview Preparation Strategy**

#### **Technical Depth Levels**
1. **Basic (Entry Level)**: Core concepts, basic CQL, simple data modeling
2. **Intermediate (2-3 years)**: Advanced modeling, performance tuning, operations
3. **Advanced (3-5 years)**: Multi-DC setup, security, troubleshooting
4. **Expert (5+ years)**: Architecture design, custom solutions, optimization

#### **Common Interview Categories**
1. **Fundamentals** (25%): Architecture, CAP theorem, consistency levels
2. **Data Modeling** (30%): Table design, partitioning, clustering
3. **Operations** (25%): Monitoring, backup/restore, scaling
4. **Advanced Topics** (20%): Multi-DC, security, performance tuning

### 🔗 **Essential Resources**

- **Official Documentation**: [Cassandra Documentation](https://cassandra.apache.org/doc/)
- **Data Modeling**: [Cassandra Data Modeling Guide](https://cassandra.apache.org/doc/latest/data_modeling/)
- **Operations**: [Cassandra Operations Guide](https://cassandra.apache.org/doc/latest/operating/)
- **Best Practices**: [DataStax Best Practices](https://docs.datastax.com/en/dse-planning/doc/)

---

**Remember**: Cassandra mastery requires understanding distributed systems concepts and query-driven data modeling. Focus on building scalable, highly available applications with proper data distribution and consistency management.