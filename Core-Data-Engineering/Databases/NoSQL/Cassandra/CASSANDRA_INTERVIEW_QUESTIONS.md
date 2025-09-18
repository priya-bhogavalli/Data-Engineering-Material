# 🗄️ Apache Cassandra Interview Questions & Answers

## 📋 Table of Contents
- [Basic Concepts](#basic-concepts)
- [Architecture & Design](#architecture--design)
- [Data Modeling](#data-modeling)
- [Performance & Optimization](#performance--optimization)
- [Operations & Maintenance](#operations--maintenance)
- [Advanced Topics](#advanced-topics)
- [Real-World Scenarios](#real-world-scenarios)

---

## Basic Concepts

### 1. What is Apache Cassandra and what are its key characteristics?
**Answer:**
Apache Cassandra is a distributed NoSQL database designed for handling large amounts of data across commodity servers with no single point of failure.

**Key Characteristics:**
- **Distributed**: Data spread across multiple nodes
- **Decentralized**: No master-slave architecture
- **Fault-tolerant**: Handles node failures gracefully
- **Scalable**: Linear scalability with node addition
- **Eventually consistent**: Tunable consistency levels
- **Column-family**: Wide-column store data model

**Use Cases:**
- Time-series data
- IoT applications
- Real-time analytics
- High-write workloads

### 2. Explain Cassandra's ring architecture and how data is distributed.
**Answer:**
Cassandra uses a ring architecture where nodes are arranged in a logical ring.

**Key Components:**
```
Ring Structure:
Node A (Token: 0-25)
Node B (Token: 26-50)
Node C (Token: 51-75)
Node D (Token: 76-100)
```

**Data Distribution:**
- **Consistent Hashing**: Uses hash function to determine data placement
- **Token Ranges**: Each node responsible for token range
- **Partition Key**: Determines which node stores data
- **Replication**: Data copied to multiple nodes

**Benefits:**
- No single point of failure
- Automatic load balancing
- Easy scaling

### 3. What is the difference between a partition key and clustering key?
**Answer:**
**Partition Key:**
- Determines which node stores the data
- Used for data distribution across cluster
- Cannot be changed after insert

**Clustering Key:**
- Determines sort order within partition
- Used for range queries
- Can have multiple clustering columns

**Example:**
```sql
CREATE TABLE user_events (
    user_id UUID,           -- Partition Key
    event_time TIMESTAMP,   -- Clustering Key
    event_type TEXT,        -- Clustering Key
    data TEXT,
    PRIMARY KEY (user_id, event_time, event_type)
);
```

### 4. Explain Cassandra's consistency levels and when to use each.
**Answer:**
**Read Consistency Levels:**
- **ONE**: Read from one replica (fastest, least consistent)
- **QUORUM**: Read from majority of replicas
- **ALL**: Read from all replicas (slowest, most consistent)
- **LOCAL_QUORUM**: Quorum within local datacenter

**Write Consistency Levels:**
- **ONE**: Write to one replica
- **QUORUM**: Write to majority of replicas
- **ALL**: Write to all replicas

**Usage Guidelines:**
```sql
-- High availability, eventual consistency
SELECT * FROM users WHERE id = ? CONSISTENCY ONE;

-- Balanced consistency and performance
SELECT * FROM users WHERE id = ? CONSISTENCY QUORUM;

-- Strong consistency (rare use)
SELECT * FROM users WHERE id = ? CONSISTENCY ALL;
```

### 5. What is eventual consistency in Cassandra?
**Answer:**
Eventual consistency means that all replicas will eventually have the same data, but not necessarily at the same time.

**Key Concepts:**
- **Asynchronous Replication**: Updates propagated asynchronously
- **Conflict Resolution**: Last-write-wins using timestamps
- **Read Repair**: Inconsistencies fixed during reads
- **Anti-entropy Repair**: Background process to sync replicas

**Example Scenario:**
```
Time T1: Write to Node A (value = 100)
Time T2: Read from Node B (value = old_value)
Time T3: Read from Node B (value = 100) // Eventually consistent
```

---

## Architecture & Design

### 6. Describe Cassandra's write path and how writes are handled.
**Answer:**
**Write Path Steps:**
1. **Commit Log**: Write logged for durability
2. **Memtable**: Data written to in-memory structure
3. **SSTable**: Memtable flushed to disk when full
4. **Compaction**: SSTables merged and optimized

**Write Process:**
```
Client Write Request
    ↓
Commit Log (Durability)
    ↓
Memtable (Memory)
    ↓
SSTable (Disk) - When Memtable Full
    ↓
Compaction (Background)
```

**Performance Characteristics:**
- Writes are very fast (append-only)
- No read-before-write required
- Optimized for write-heavy workloads

### 7. Explain Cassandra's read path and read performance optimization.
**Answer:**
**Read Path Steps:**
1. **Check Memtable**: Look for data in memory
2. **Check SSTables**: Search disk-based SSTables
3. **Merge Results**: Combine data from multiple sources
4. **Return Latest**: Use timestamp for conflict resolution

**Read Optimizations:**
```sql
-- Bloom Filters: Quickly eliminate SSTables
-- Partition Summary: Locate partition in SSTable
-- Partition Index: Find exact location
-- Data: Retrieve actual data
```

**Performance Factors:**
- Number of SSTables affects read performance
- Compaction reduces SSTable count
- Caching improves read speed

### 8. What are SSTables and how do they work?
**Answer:**
**SSTable (Sorted String Table):**
- Immutable disk-based data structure
- Contains sorted key-value pairs
- Written when Memtable is full

**SSTable Components:**
```
SSTable Structure:
├── Data File (.db)
├── Index File (.idx)
├── Bloom Filter (.bf)
├── Statistics (.stats)
└── Summary (.sum)
```

**Characteristics:**
- **Immutable**: Never modified after creation
- **Sorted**: Keys stored in sorted order
- **Compressed**: Optional compression
- **Timestamped**: Each cell has timestamp

### 9. Describe the compaction process in Cassandra.
**Answer:**
**Compaction Purpose:**
- Merge multiple SSTables into fewer SSTables
- Remove deleted data (tombstones)
- Improve read performance
- Reclaim disk space

**Compaction Strategies:**
```sql
-- Size Tiered Compaction (Default)
ALTER TABLE users WITH compaction = {
    'class': 'SizeTieredCompactionStrategy',
    'max_threshold': 32,
    'min_threshold': 4
};

-- Leveled Compaction (Read-heavy)
ALTER TABLE users WITH compaction = {
    'class': 'LeveledCompactionStrategy',
    'sstable_size_in_mb': 160
};
```

**When Compaction Occurs:**
- Background process
- Triggered by SSTable count/size
- Can be manually initiated

### 10. What is the gossip protocol in Cassandra?
**Answer:**
**Gossip Protocol:**
- Peer-to-peer communication protocol
- Nodes exchange state information
- Maintains cluster membership and health

**Information Exchanged:**
```
Gossip Information:
├── Node Status (UP/DOWN)
├── Load Information
├── Schema Versions
├── Token Ownership
└── Datacenter/Rack Info
```

**Gossip Process:**
1. Every second, each node gossips with 1-3 other nodes
2. Nodes exchange their view of cluster state
3. Information propagates throughout cluster
4. Failure detection and recovery

---

## Data Modeling

### 11. What are the key principles of Cassandra data modeling?
**Answer:**
**Core Principles:**
1. **Query-Driven Design**: Model based on queries, not entities
2. **Denormalization**: Duplicate data for query efficiency
3. **Partition Design**: Keep related data together
4. **Avoid JOINs**: No cross-partition operations

**Design Process:**
```sql
-- Step 1: Identify Queries
-- Q1: Get user profile by user_id
-- Q2: Get user posts by user_id, ordered by time
-- Q3: Get posts by tag

-- Step 2: Design Tables for Each Query
CREATE TABLE user_profiles (
    user_id UUID PRIMARY KEY,
    name TEXT,
    email TEXT
);

CREATE TABLE user_posts (
    user_id UUID,
    post_time TIMESTAMP,
    post_id UUID,
    content TEXT,
    PRIMARY KEY (user_id, post_time)
) WITH CLUSTERING ORDER BY (post_time DESC);

CREATE TABLE posts_by_tag (
    tag TEXT,
    post_time TIMESTAMP,
    post_id UUID,
    user_id UUID,
    content TEXT,
    PRIMARY KEY (tag, post_time)
) WITH CLUSTERING ORDER BY (post_time DESC);
```

### 12. How do you handle one-to-many relationships in Cassandra?
**Answer:**
**Approach 1: Clustering Columns**
```sql
-- User has many orders
CREATE TABLE user_orders (
    user_id UUID,
    order_date TIMESTAMP,
    order_id UUID,
    total DECIMAL,
    status TEXT,
    PRIMARY KEY (user_id, order_date, order_id)
) WITH CLUSTERING ORDER BY (order_date DESC);
```

**Approach 2: Collection Types**
```sql
-- User has many email addresses
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    name TEXT,
    emails SET<TEXT>
);
```

**Approach 3: Separate Table with Denormalization**
```sql
-- Orders table with user info duplicated
CREATE TABLE orders (
    order_id UUID PRIMARY KEY,
    user_id UUID,
    user_name TEXT,  -- Denormalized
    order_date TIMESTAMP,
    total DECIMAL
);
```

### 13. What are collection types in Cassandra and when should you use them?
**Answer:**
**Collection Types:**

**SET:**
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    name TEXT,
    interests SET<TEXT>
);

-- Usage
INSERT INTO users (user_id, name, interests) 
VALUES (uuid(), 'John', {'music', 'sports', 'travel'});

-- Add to set
UPDATE users SET interests = interests + {'reading'} 
WHERE user_id = ?;
```

**LIST:**
```sql
CREATE TABLE playlists (
    playlist_id UUID PRIMARY KEY,
    name TEXT,
    songs LIST<TEXT>
);

-- Append to list
UPDATE playlists SET songs = songs + ['song1'] 
WHERE playlist_id = ?;
```

**MAP:**
```sql
CREATE TABLE user_preferences (
    user_id UUID PRIMARY KEY,
    settings MAP<TEXT, TEXT>
);

-- Update map
UPDATE user_preferences 
SET settings['theme'] = 'dark' 
WHERE user_id = ?;
```

**Limitations:**
- Collections have size limits (64KB)
- Not suitable for large datasets
- Limited query capabilities

### 14. How do you model time-series data in Cassandra?
**Answer:**
**Time-Series Pattern:**
```sql
-- IoT sensor data
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

**Key Design Decisions:**
- **Partition Key**: Include time component to distribute data
- **Clustering Key**: Use timestamp for time ordering
- **Bucketing**: Group by time periods (day/month/year)

**Query Examples:**
```sql
-- Get recent data for sensor
SELECT * FROM sensor_data 
WHERE sensor_id = ? AND year = 2024 AND month = 3
ORDER BY timestamp DESC LIMIT 100;

-- Get data for time range
SELECT * FROM sensor_data 
WHERE sensor_id = ? AND year = 2024 AND month = 3
AND timestamp >= '2024-03-01' AND timestamp < '2024-03-02';
```

### 15. What are secondary indexes in Cassandra and their limitations?
**Answer:**
**Secondary Indexes:**
Allow queries on non-primary key columns.

**Creation:**
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    name TEXT,
    email TEXT,
    age INT
);

-- Create secondary index
CREATE INDEX ON users (email);
CREATE INDEX ON users (age);

-- Query using secondary index
SELECT * FROM users WHERE email = 'john@example.com';
SELECT * FROM users WHERE age = 25;
```

**Limitations:**
- **Performance**: Can be slow on large datasets
- **Cardinality**: Work best with low-cardinality data
- **Distribution**: Index queries hit all nodes
- **Maintenance**: Overhead for writes

**Alternatives:**
- Materialized views
- Denormalized tables
- Application-level indexing

---

## Performance & Optimization

### 16. How do you optimize Cassandra for write-heavy workloads?
**Answer:**
**Write Optimization Strategies:**

**1. Hardware Optimization:**
```yaml
# cassandra.yaml
commitlog_sync: batch
commitlog_sync_batch_window_in_ms: 2
concurrent_writes: 128
memtable_flush_writers: 4
```

**2. Data Model Optimization:**
```sql
-- Use appropriate partition key distribution
CREATE TABLE events (
    event_date DATE,
    event_hour INT,
    event_id UUID,
    data TEXT,
    PRIMARY KEY ((event_date, event_hour), event_id)
);
```

**3. Compaction Strategy:**
```sql
-- Size-tiered for write-heavy
ALTER TABLE events WITH compaction = {
    'class': 'SizeTieredCompactionStrategy',
    'max_threshold': 32
};
```

**4. Consistency Level:**
```sql
-- Use ONE for maximum write performance
INSERT INTO events (...) VALUES (...) USING CONSISTENCY ONE;
```

### 17. How do you optimize Cassandra for read-heavy workloads?
**Answer:**
**Read Optimization Strategies:**

**1. Compaction Strategy:**
```sql
-- Leveled compaction for read-heavy
ALTER TABLE users WITH compaction = {
    'class': 'LeveledCompactionStrategy',
    'sstable_size_in_mb': 160
};
```

**2. Caching:**
```yaml
# cassandra.yaml
row_cache_size_in_mb: 1024
key_cache_size_in_mb: 512
```

**3. Data Model:**
```sql
-- Minimize partition size
-- Use clustering keys for range queries
CREATE TABLE user_activity (
    user_id UUID,
    activity_date DATE,
    activity_time TIMESTAMP,
    activity_type TEXT,
    PRIMARY KEY ((user_id, activity_date), activity_time)
);
```

**4. Read Consistency:**
```sql
-- Use LOCAL_ONE for better performance
SELECT * FROM users WHERE id = ? CONSISTENCY LOCAL_ONE;
```

### 18. What causes hot spots in Cassandra and how do you avoid them?
**Answer:**
**Hot Spot Causes:**
- Poor partition key selection
- Uneven data distribution
- Time-based partition keys
- Sequential writes

**Avoidance Strategies:**

**1. Better Partition Key Design:**
```sql
-- Bad: Sequential partition key
CREATE TABLE logs (
    log_date DATE PRIMARY KEY,
    message TEXT
);

-- Good: Distributed partition key
CREATE TABLE logs (
    bucket INT,
    log_date DATE,
    log_time TIMESTAMP,
    message TEXT,
    PRIMARY KEY ((bucket, log_date), log_time)
);
```

**2. Hash-Based Distribution:**
```sql
-- Use hash of natural key
CREATE TABLE user_sessions (
    user_hash INT,  -- hash(user_id) % 100
    user_id UUID,
    session_start TIMESTAMP,
    session_data TEXT,
    PRIMARY KEY ((user_hash, user_id), session_start)
);
```

**3. Time Bucketing:**
```sql
-- Distribute time-series data
CREATE TABLE metrics (
    metric_name TEXT,
    bucket INT,     -- hour % 24
    timestamp TIMESTAMP,
    value DOUBLE,
    PRIMARY KEY ((metric_name, bucket), timestamp)
);
```

### 19. How do you monitor Cassandra performance?
**Answer:**
**Key Metrics to Monitor:**

**1. Node Metrics:**
```bash
# nodetool commands
nodetool status          # Cluster status
nodetool tpstats         # Thread pool statistics
nodetool cfstats         # Column family statistics
nodetool netstats        # Network statistics
```

**2. JVM Metrics:**
```bash
# GC monitoring
nodetool gcstats
jstat -gc <pid>

# Heap usage
nodetool info
```

**3. Performance Metrics:**
- **Read/Write Latency**: 95th percentile response times
- **Throughput**: Operations per second
- **Compaction**: Pending compactions
- **Cache Hit Rates**: Row cache and key cache effectiveness

**4. Monitoring Tools:**
```yaml
# DataStax OpsCenter
# Prometheus + Grafana
# Custom JMX monitoring
```

### 20. What are tombstones in Cassandra and how do they affect performance?
**Answer:**
**Tombstones:**
Markers for deleted data that remain until compaction.

**Types of Tombstones:**
```sql
-- Row tombstone
DELETE FROM users WHERE user_id = ?;

-- Column tombstone
UPDATE users SET email = null WHERE user_id = ?;

-- Range tombstone
DELETE FROM user_events 
WHERE user_id = ? AND event_time < '2024-01-01';
```

**Performance Impact:**
- Slow down read queries
- Consume memory and disk space
- Affect compaction performance

**Mitigation Strategies:**
```yaml
# cassandra.yaml
gc_grace_seconds: 864000  # 10 days default
tombstone_warn_threshold: 1000
tombstone_failure_threshold: 100000

# Table-level settings
ALTER TABLE users WITH gc_grace_seconds = 86400;  # 1 day
```

**Best Practices:**
- Avoid frequent deletes
- Use TTL instead of explicit deletes
- Monitor tombstone ratios
- Regular compaction

---

## Operations & Maintenance

### 21. How do you add a new node to a Cassandra cluster?
**Answer:**
**Node Addition Process:**

**1. Prepare New Node:**
```yaml
# cassandra.yaml
cluster_name: 'MyCluster'
seeds: "existing_node1,existing_node2"
listen_address: new_node_ip
rpc_address: new_node_ip
```

**2. Start Node:**
```bash
# Start Cassandra service
sudo service cassandra start

# Monitor bootstrap progress
nodetool netstats
```

**3. Verify Addition:**
```bash
# Check cluster status
nodetool status

# Verify ring
nodetool ring
```

**4. Run Cleanup (Optional):**
```bash
# Remove unnecessary data from existing nodes
nodetool cleanup
```

**Bootstrap Process:**
- New node receives token range
- Data streamed from existing replicas
- Node becomes available after bootstrap

### 22. How do you handle node failures in Cassandra?
**Answer:**
**Failure Detection:**
```bash
# Check node status
nodetool status
# DN = Down, UN = Up Normal

# Check gossip info
nodetool gossipinfo
```

**Temporary Failure:**
```bash
# Node will automatically rejoin
# Hinted handoff handles missed writes
# Read repair fixes inconsistencies
```

**Permanent Failure:**
```bash
# Remove failed node
nodetool removenode <node_id>

# Replace failed node
# 1. Start new node with replace_address
# 2. Bootstrap will restore data
```

**Configuration:**
```yaml
# cassandra.yaml
hinted_handoff_enabled: true
max_hint_window_in_ms: 10800000  # 3 hours
```

### 23. What is repair in Cassandra and when should you run it?
**Answer:**
**Repair Purpose:**
Ensures data consistency across replicas by comparing and synchronizing data.

**Types of Repair:**
```bash
# Full repair (all data)
nodetool repair

# Incremental repair (changed data only)
nodetool repair -inc

# Repair specific keyspace
nodetool repair keyspace_name

# Repair specific table
nodetool repair keyspace_name table_name
```

**When to Run Repair:**
- **Regular Schedule**: Within gc_grace_seconds period
- **After Node Outage**: When node rejoins cluster
- **Data Inconsistency**: When read repair indicates issues
- **Before Major Operations**: Node decommission/replacement

**Best Practices:**
```bash
# Run repair weekly or bi-weekly
# Use incremental repair for efficiency
# Monitor repair progress
# Avoid running repair on all nodes simultaneously
```

### 24. How do you backup and restore Cassandra data?
**Answer:**
**Backup Strategies:**

**1. Snapshot Backup:**
```bash
# Create snapshot
nodetool snapshot keyspace_name

# List snapshots
nodetool listsnapshots

# Clear old snapshots
nodetool clearsnapshot
```

**2. Incremental Backup:**
```yaml
# cassandra.yaml
incremental_backups: true
```

**3. Full Cluster Backup:**
```bash
#!/bin/bash
# Backup script
for node in node1 node2 node3; do
    ssh $node "nodetool snapshot"
    rsync -av $node:/var/lib/cassandra/data/ /backup/$node/
done
```

**Restore Process:**
```bash
# Stop Cassandra
sudo service cassandra stop

# Restore data files
cp -r /backup/data/* /var/lib/cassandra/data/

# Fix permissions
chown -R cassandra:cassandra /var/lib/cassandra/data/

# Start Cassandra
sudo service cassandra start

# Run repair
nodetool repair
```

### 25. How do you upgrade a Cassandra cluster?
**Answer:**
**Upgrade Process:**

**1. Pre-Upgrade Preparation:**
```bash
# Backup cluster
nodetool snapshot

# Check cluster health
nodetool status
nodetool describecluster

# Review release notes
# Test upgrade on staging environment
```

**2. Rolling Upgrade:**
```bash
# For each node:
# 1. Stop Cassandra
sudo service cassandra stop

# 2. Install new version
sudo apt-get update
sudo apt-get install cassandra=new_version

# 3. Start Cassandra
sudo service cassandra start

# 4. Verify node is up
nodetool status

# 5. Wait for node to be fully operational
# 6. Proceed to next node
```

**3. Post-Upgrade:**
```bash
# Run repair on all nodes
nodetool repair

# Update schema if needed
# Run upgradesstables if required
nodetool upgradesstables
```

**Best Practices:**
- Upgrade one node at a time
- Monitor logs during upgrade
- Have rollback plan ready
- Test thoroughly in staging

---

## Advanced Topics

### 26. What are materialized views in Cassandra?
**Answer:**
**Materialized Views:**
Automatically maintained denormalized views of base table data.

**Creation:**
```sql
-- Base table
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    name TEXT,
    email TEXT,
    age INT,
    city TEXT
);

-- Materialized view
CREATE MATERIALIZED VIEW users_by_city AS
SELECT user_id, name, email, age, city
FROM users
WHERE city IS NOT NULL AND user_id IS NOT NULL
PRIMARY KEY (city, user_id);
```

**Benefits:**
- Automatic maintenance
- Query flexibility
- Consistent with base table

**Limitations:**
- Write performance impact
- Limited WHERE clause options
- All primary key columns must be selected

**Usage:**
```sql
-- Query by city
SELECT * FROM users_by_city WHERE city = 'New York';
```

### 27. How does Cassandra handle concurrent writes and conflicts?
**Answer:**
**Conflict Resolution:**
Cassandra uses **Last-Write-Wins** (LWW) with timestamps.

**Timestamp Resolution:**
```sql
-- Explicit timestamp
INSERT INTO users (user_id, name) 
VALUES (?, 'John') 
USING TIMESTAMP 1640995200000000;

-- System timestamp (default)
INSERT INTO users (user_id, name) VALUES (?, 'Jane');
```

**Conflict Scenarios:**
```sql
-- Time T1: Write name = 'John' (timestamp: 100)
-- Time T2: Write name = 'Jane' (timestamp: 200)
-- Result: name = 'Jane' (higher timestamp wins)
```

**Lightweight Transactions (LWT):**
```sql
-- Conditional insert
INSERT INTO users (user_id, name) 
VALUES (?, 'John') 
IF NOT EXISTS;

-- Conditional update
UPDATE users SET name = 'Jane' 
WHERE user_id = ? 
IF name = 'John';
```

**LWT Characteristics:**
- Uses Paxos consensus protocol
- Provides linearizable consistency
- Higher latency than regular writes

### 28. What is the difference between Cassandra and traditional RDBMS?
**Answer:**
**Architecture Differences:**

| Aspect | Cassandra | RDBMS |
|--------|-----------|-------|
| **Architecture** | Distributed, P2P | Centralized, Master-Slave |
| **Consistency** | Eventually Consistent | ACID Compliant |
| **Scalability** | Horizontal | Vertical (primarily) |
| **Schema** | Flexible | Fixed |
| **Joins** | No Joins | Full JOIN support |
| **Transactions** | Limited (LWT) | Full ACID transactions |

**Data Model Differences:**
```sql
-- RDBMS Normalized Design
CREATE TABLE users (id, name, email);
CREATE TABLE orders (id, user_id, amount);
CREATE TABLE order_items (order_id, product_id, quantity);

-- Cassandra Denormalized Design
CREATE TABLE user_orders (
    user_id UUID,
    order_date TIMESTAMP,
    order_id UUID,
    amount DECIMAL,
    items LIST<TEXT>,
    PRIMARY KEY (user_id, order_date)
);
```

**When to Choose Cassandra:**
- High write throughput required
- Need linear scalability
- Geographic distribution
- Can tolerate eventual consistency

**When to Choose RDBMS:**
- Complex queries and joins needed
- Strong consistency required
- Existing SQL expertise
- Smaller scale applications

### 29. How do you implement pagination in Cassandra?
**Answer:**
**Token-Based Pagination:**
```sql
-- Initial query
SELECT token(user_id), user_id, name, email 
FROM users 
LIMIT 10;

-- Next page using token
SELECT token(user_id), user_id, name, email 
FROM users 
WHERE token(user_id) > <last_token_from_previous_page>
LIMIT 10;
```

**Time-Based Pagination:**
```sql
-- For time-series data
SELECT * FROM user_events 
WHERE user_id = ? 
AND event_time < <last_event_time>
ORDER BY event_time DESC 
LIMIT 10;
```

**Application Implementation:**
```python
def get_users_page(page_token=None, page_size=10):
    if page_token:
        query = """
        SELECT token(user_id), user_id, name, email 
        FROM users 
        WHERE token(user_id) > ? 
        LIMIT ?
        """
        rows = session.execute(query, [page_token, page_size])
    else:
        query = """
        SELECT token(user_id), user_id, name, email 
        FROM users 
        LIMIT ?
        """
        rows = session.execute(query, [page_size])
    
    users = []
    next_token = None
    
    for row in rows:
        users.append({
            'user_id': row.user_id,
            'name': row.name,
            'email': row.email
        })
        next_token = row.system_token_user_id
    
    return users, next_token
```

### 30. What are the best practices for Cassandra schema design?
**Answer:**
**Schema Design Best Practices:**

**1. Query-First Design:**
```sql
-- Start with queries, then design tables
-- Q1: Get user profile
-- Q2: Get user's recent posts
-- Q3: Get posts by tag

-- Design separate table for each query pattern
```

**2. Partition Size Guidelines:**
```sql
-- Keep partitions under 100MB
-- Avoid unbounded partitions
-- Use time bucketing for time-series data

CREATE TABLE user_events (
    user_id UUID,
    year INT,
    month INT,
    event_time TIMESTAMP,
    event_data TEXT,
    PRIMARY KEY ((user_id, year, month), event_time)
);
```

**3. Clustering Key Design:**
```sql
-- Use clustering keys for:
-- - Sorting requirements
-- - Range queries
-- - Uniqueness within partition

CREATE TABLE products (
    category TEXT,
    price DECIMAL,
    product_id UUID,
    name TEXT,
    PRIMARY KEY (category, price, product_id)
) WITH CLUSTERING ORDER BY (price DESC);
```

**4. Avoid Anti-Patterns:**
```sql
-- DON'T: Large collections
-- DON'T: Unbounded row growth
-- DON'T: High cardinality secondary indexes
-- DON'T: Frequent updates to same row
```

**5. Denormalization Strategy:**
```sql
-- Duplicate data for query efficiency
-- Maintain consistency at application level
-- Use batch statements for related updates

BEGIN BATCH
    INSERT INTO users (user_id, name, email) VALUES (?, ?, ?);
    INSERT INTO users_by_email (email, user_id, name) VALUES (?, ?, ?);
APPLY BATCH;
```

---

## Real-World Scenarios

### 31. Design a Cassandra schema for a social media application.
**Answer:**
**Requirements Analysis:**
- User profiles and posts
- Timeline feeds
- Following relationships
- Post interactions (likes, comments)

**Schema Design:**
```sql
-- User profiles
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    username TEXT,
    email TEXT,
    full_name TEXT,
    bio TEXT,
    created_at TIMESTAMP
);

-- User posts
CREATE TABLE user_posts (
    user_id UUID,
    post_time TIMESTAMP,
    post_id UUID,
    content TEXT,
    media_urls LIST<TEXT>,
    likes_count COUNTER,
    PRIMARY KEY (user_id, post_time, post_id)
) WITH CLUSTERING ORDER BY (post_time DESC);

-- Timeline feed (denormalized)
CREATE TABLE user_timeline (
    user_id UUID,
    post_time TIMESTAMP,
    post_id UUID,
    author_id UUID,
    author_username TEXT,
    content TEXT,
    PRIMARY KEY (user_id, post_time, post_id)
) WITH CLUSTERING ORDER BY (post_time DESC);

-- Following relationships
CREATE TABLE user_following (
    user_id UUID,
    following_id UUID,
    followed_at TIMESTAMP,
    PRIMARY KEY (user_id, following_id)
);

CREATE TABLE user_followers (
    user_id UUID,
    follower_id UUID,
    followed_at TIMESTAMP,
    PRIMARY KEY (user_id, follower_id)
);

-- Post interactions
CREATE TABLE post_likes (
    post_id UUID,
    user_id UUID,
    liked_at TIMESTAMP,
    PRIMARY KEY (post_id, user_id)
);
```

**Query Examples:**
```sql
-- Get user timeline
SELECT * FROM user_timeline 
WHERE user_id = ? 
ORDER BY post_time DESC 
LIMIT 20;

-- Get user's posts
SELECT * FROM user_posts 
WHERE user_id = ? 
ORDER BY post_time DESC 
LIMIT 10;

-- Check if user likes post
SELECT * FROM post_likes 
WHERE post_id = ? AND user_id = ?;
```

### 32. How would you handle a time-series IoT data scenario with millions of sensors?
**Answer:**
**Scenario Requirements:**
- Millions of IoT sensors
- High write throughput (1M+ writes/sec)
- Time-based queries
- Data retention policies

**Schema Design:**
```sql
-- Raw sensor data with time bucketing
CREATE TABLE sensor_data (
    sensor_id UUID,
    bucket_hour TIMESTAMP,  -- Hour bucket for distribution
    timestamp TIMESTAMP,
    temperature FLOAT,
    humidity FLOAT,
    pressure FLOAT,
    battery_level FLOAT,
    PRIMARY KEY ((sensor_id, bucket_hour), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC)
AND default_time_to_live = 2592000;  -- 30 days TTL

-- Aggregated hourly data
CREATE TABLE sensor_hourly_stats (
    sensor_id UUID,
    hour TIMESTAMP,
    avg_temperature FLOAT,
    min_temperature FLOAT,
    max_temperature FLOAT,
    avg_humidity FLOAT,
    sample_count INT,
    PRIMARY KEY (sensor_id, hour)
) WITH CLUSTERING ORDER BY (hour DESC)
AND default_time_to_live = 7776000;  -- 90 days TTL

-- Daily aggregations
CREATE TABLE sensor_daily_stats (
    sensor_id UUID,
    date DATE,
    avg_temperature FLOAT,
    min_temperature FLOAT,
    max_temperature FLOAT,
    PRIMARY KEY (sensor_id, date)
) WITH CLUSTERING ORDER BY (date DESC);
```

**Write Optimization:**
```python
# Batch writes for efficiency
from cassandra.cluster import Cluster
from cassandra.concurrent import execute_concurrent_with_args

def write_sensor_batch(session, sensor_data_batch):
    query = """
    INSERT INTO sensor_data 
    (sensor_id, bucket_hour, timestamp, temperature, humidity, pressure, battery_level)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    
    # Prepare arguments
    args_list = []
    for data in sensor_data_batch:
        bucket_hour = data['timestamp'].replace(minute=0, second=0, microsecond=0)
        args_list.append((
            data['sensor_id'], bucket_hour, data['timestamp'],
            data['temperature'], data['humidity'], 
            data['pressure'], data['battery_level']
        ))
    
    # Execute concurrent writes
    execute_concurrent_with_args(session, query, args_list, concurrency=50)
```

**Query Patterns:**
```sql
-- Recent data for sensor
SELECT * FROM sensor_data 
WHERE sensor_id = ? 
AND bucket_hour >= '2024-03-01 10:00:00'
ORDER BY timestamp DESC 
LIMIT 100;

-- Hourly aggregates
SELECT * FROM sensor_hourly_stats 
WHERE sensor_id = ? 
AND hour >= '2024-03-01' 
AND hour < '2024-03-02'
ORDER BY hour DESC;
```

### 33. Design a Cassandra solution for a real-time analytics dashboard.
**Answer:**
**Requirements:**
- Real-time metrics ingestion
- Dashboard queries with low latency
- Multiple aggregation levels
- High availability

**Schema Design:**
```sql
-- Real-time events
CREATE TABLE events (
    event_type TEXT,
    bucket_minute TIMESTAMP,
    event_time TIMESTAMP,
    event_id UUID,
    user_id UUID,
    properties MAP<TEXT, TEXT>,
    PRIMARY KEY ((event_type, bucket_minute), event_time, event_id)
) WITH CLUSTERING ORDER BY (event_time DESC);

-- Minute-level aggregations
CREATE TABLE metrics_by_minute (
    metric_name TEXT,
    timestamp TIMESTAMP,
    value BIGINT,
    PRIMARY KEY (metric_name, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);

-- Hour-level aggregations
CREATE TABLE metrics_by_hour (
    metric_name TEXT,
    timestamp TIMESTAMP,
    value BIGINT,
    PRIMARY KEY (metric_name, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);

-- Dashboard widgets
CREATE TABLE dashboard_widgets (
    dashboard_id UUID,
    widget_id UUID,
    widget_type TEXT,
    config MAP<TEXT, TEXT>,
    position INT,
    PRIMARY KEY (dashboard_id, position, widget_id)
);
```

**Real-time Processing:**
```python
# Stream processing for aggregations
import asyncio
from datetime import datetime, timedelta

class MetricsAggregator:
    def __init__(self, session):
        self.session = session
        self.minute_counters = {}
    
    async def process_event(self, event):
        # Update real-time counters
        minute_key = event['timestamp'].replace(second=0, microsecond=0)
        metric_key = f"{event['type']}_{minute_key}"
        
        if metric_key not in self.minute_counters:
            self.minute_counters[metric_key] = 0
        self.minute_counters[metric_key] += 1
        
        # Flush counters every minute
        await self.flush_if_needed(minute_key)
    
    async def flush_if_needed(self, current_minute):
        cutoff = current_minute - timedelta(minutes=1)
        
        for key, count in list(self.minute_counters.items()):
            if key.endswith(str(cutoff)):
                # Write to Cassandra
                metric_name = key.split('_')[0]
                await self.write_metric(metric_name, cutoff, count)
                del self.minute_counters[key]
    
    async def write_metric(self, metric_name, timestamp, value):
        query = """
        INSERT INTO metrics_by_minute (metric_name, timestamp, value)
        VALUES (?, ?, ?)
        """
        await self.session.execute_async(query, [metric_name, timestamp, value])
```

**Dashboard Queries:**
```sql
-- Real-time metrics (last hour)
SELECT timestamp, value 
FROM metrics_by_minute 
WHERE metric_name = 'page_views' 
AND timestamp >= ?
ORDER BY timestamp DESC;

-- Historical trends (last 24 hours)
SELECT timestamp, value 
FROM metrics_by_hour 
WHERE metric_name = 'user_signups' 
AND timestamp >= ?
ORDER BY timestamp DESC;
```

### 34. How would you migrate data from a relational database to Cassandra?
**Answer:**
**Migration Strategy:**

**1. Analysis Phase:**
```sql
-- Analyze existing RDBMS schema
-- Identify query patterns
-- Determine data relationships
-- Estimate data volumes

-- Example: E-commerce RDBMS
SELECT table_name, table_rows 
FROM information_schema.tables 
WHERE table_schema = 'ecommerce';
```

**2. Schema Mapping:**
```sql
-- RDBMS Schema
CREATE TABLE users (id, name, email, created_at);
CREATE TABLE orders (id, user_id, total, order_date);
CREATE TABLE order_items (order_id, product_id, quantity, price);

-- Cassandra Schema (Query-Driven)
-- Q1: Get user orders
CREATE TABLE user_orders (
    user_id UUID,
    order_date TIMESTAMP,
    order_id UUID,
    total DECIMAL,
    items LIST<FROZEN<order_item>>,
    PRIMARY KEY (user_id, order_date, order_id)
) WITH CLUSTERING ORDER BY (order_date DESC);

-- Q2: Get order details
CREATE TABLE orders (
    order_id UUID PRIMARY KEY,
    user_id UUID,
    user_name TEXT,  -- Denormalized
    total DECIMAL,
    order_date TIMESTAMP,
    items LIST<FROZEN<order_item>>
);
```

**3. Migration Process:**
```python
# ETL Pipeline
import pandas as pd
from cassandra.cluster import Cluster

class DatabaseMigrator:
    def __init__(self, mysql_conn, cassandra_session):
        self.mysql_conn = mysql_conn
        self.cassandra_session = cassandra_session
    
    def migrate_users_orders(self):
        # Extract from MySQL
        query = """
        SELECT u.id, u.name, u.email,
               o.id as order_id, o.total, o.order_date,
               oi.product_id, oi.quantity, oi.price
        FROM users u
        JOIN orders o ON u.id = o.user_id
        JOIN order_items oi ON o.id = oi.order_id
        ORDER BY u.id, o.order_date
        """
        
        df = pd.read_sql(query, self.mysql_conn)
        
        # Transform and group by order
        orders_grouped = df.groupby(['id', 'order_id'])
        
        # Load into Cassandra
        for (user_id, order_id), group in orders_grouped:
            items = []
            for _, row in group.iterrows():
                items.append({
                    'product_id': row['product_id'],
                    'quantity': row['quantity'],
                    'price': row['price']
                })
            
            # Insert into Cassandra
            self.insert_user_order(
                user_id, order_id, 
                group.iloc[0]['total'],
                group.iloc[0]['order_date'],
                items
            )
    
    def insert_user_order(self, user_id, order_id, total, order_date, items):
        query = """
        INSERT INTO user_orders 
        (user_id, order_date, order_id, total, items)
        VALUES (?, ?, ?, ?, ?)
        """
        self.cassandra_session.execute(
            query, [user_id, order_date, order_id, total, items]
        )
```

**4. Validation:**
```python
def validate_migration():
    # Count validation
    mysql_count = mysql_cursor.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    cassandra_count = cassandra_session.execute(
        "SELECT COUNT(*) FROM user_orders"
    ).one()[0]
    
    assert mysql_count == cassandra_count
    
    # Data validation
    sample_orders = cassandra_session.execute(
        "SELECT * FROM user_orders LIMIT 100"
    )
    
    for order in sample_orders:
        # Verify against source data
        mysql_order = mysql_cursor.execute(
            "SELECT * FROM orders WHERE id = ?", [order.order_id]
        ).fetchone()
        
        assert order.total == mysql_order['total']
```

### 35. How do you handle data consistency across multiple Cassandra datacenters?
**Answer:**
**Multi-Datacenter Setup:**

**1. Replication Strategy:**
```sql
-- Create keyspace with multi-DC replication
CREATE KEYSPACE ecommerce 
WITH REPLICATION = {
    'class': 'NetworkTopologyStrategy',
    'DC1': 3,  -- 3 replicas in DC1
    'DC2': 3,  -- 3 replicas in DC2
    'DC3': 2   -- 2 replicas in DC3
};
```

**2. Consistency Levels:**
```sql
-- Local consistency (within DC)
SELECT * FROM users WHERE id = ? CONSISTENCY LOCAL_QUORUM;

-- Cross-DC consistency (when needed)
SELECT * FROM users WHERE id = ? CONSISTENCY EACH_QUORUM;

-- Write to local DC only
INSERT INTO users (...) VALUES (...) CONSISTENCY LOCAL_QUORUM;
```

**3. Application Configuration:**
```python
from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy

# Configure DC-aware load balancing
cluster = Cluster(
    contact_points=['dc1-node1', 'dc1-node2'],
    load_balancing_policy=DCAwareRoundRobinPolicy(
        local_dc='DC1',
        used_hosts_per_remote_dc=1
    )
)

session = cluster.connect('ecommerce')

# Use local consistency for reads
def get_user(user_id):
    query = "SELECT * FROM users WHERE user_id = ?"
    return session.execute(query, [user_id], 
                          consistency_level=ConsistencyLevel.LOCAL_QUORUM)

# Use EACH_QUORUM for critical writes
def create_order(order_data):
    query = "INSERT INTO orders (...) VALUES (...)"
    session.execute(query, order_data,
                   consistency_level=ConsistencyLevel.EACH_QUORUM)
```

**4. Conflict Resolution:**
```python
# Handle cross-DC conflicts with timestamps
def update_user_with_timestamp(user_id, updates):
    timestamp = int(time.time() * 1000000)  # microseconds
    
    query = """
    UPDATE users 
    SET name = ?, email = ? 
    WHERE user_id = ? 
    USING TIMESTAMP ?
    """
    
    session.execute(query, [
        updates['name'], 
        updates['email'], 
        user_id, 
        timestamp
    ])
```

**5. Monitoring Cross-DC Health:**
```bash
# Check cross-DC streaming
nodetool netstats

# Monitor repair across DCs
nodetool repair -dc DC1

# Check gossip state
nodetool gossipinfo
```

**Best Practices:**
- Use LOCAL_QUORUM for most operations
- Reserve EACH_QUORUM for critical data
- Monitor cross-DC latency
- Plan for network partitions
- Regular cross-DC repairs

---

*This comprehensive guide covers 35 essential Apache Cassandra interview questions with detailed answers, practical examples, and real-world scenarios to help you succeed in your data engineering interviews.*