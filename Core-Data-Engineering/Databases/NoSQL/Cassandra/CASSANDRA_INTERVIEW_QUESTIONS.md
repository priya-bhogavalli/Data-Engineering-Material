# Apache Cassandra Interview Questions & Answers

## 📋 Table of Contents
1. [Core Concepts](#core-concepts)
2. [Data Modeling](#data-modeling)
3. [Architecture & Replication](#architecture--replication)
4. [Performance & Optimization](#performance--optimization)
5. [Operations & Monitoring](#operations--monitoring)

---

## Core Concepts

### 1. What is Apache Cassandra and when should you use it?

**Answer:**
Apache Cassandra is a distributed NoSQL database designed for handling large amounts of data across commodity servers with no single point of failure.

**Key Characteristics:**
- **Distributed**: Data spread across multiple nodes
- **Decentralized**: No master-slave architecture
- **Fault-tolerant**: Handles node failures gracefully
- **Scalable**: Linear scalability with node addition
- **Eventually consistent**: Tunable consistency levels

**Use Cases:**
```yaml
ideal_for:
  - High write throughput applications
  - Time-series data (IoT, logging, metrics)
  - Geographically distributed applications
  - Applications requiring 99.99% uptime
  - Large-scale data with predictable query patterns

not_ideal_for:
  - Complex queries with JOINs
  - ACID transactions across partitions
  - Frequent schema changes
  - Small datasets (<100GB)
  - Ad-hoc analytical queries
```

### 2. Explain Cassandra's data model and how it differs from relational databases.

**Answer:**
Cassandra uses a wide-column data model based on partition keys and clustering columns.

**Data Model Structure:**
```cql
-- Table structure
CREATE TABLE user_events (
    user_id UUID,           -- Partition key
    event_time TIMESTAMP,   -- Clustering column
    event_type TEXT,        -- Clustering column
    event_data MAP<TEXT, TEXT>,
    PRIMARY KEY (user_id, event_time, event_type)
);

-- Data organization
Partition: user_id = 123e4567-e89b-12d3-a456-426614174000
├── Row 1: event_time=2023-12-01T10:00:00, event_type='login'
├── Row 2: event_time=2023-12-01T10:15:00, event_type='page_view'
└── Row 3: event_time=2023-12-01T10:30:00, event_type='logout'
```

**Key Differences:**
| Aspect | Cassandra | RDBMS |
|--------|-----------|-------|
| **Data Model** | Wide-column | Relational tables |
| **Schema** | Flexible | Fixed |
| **Queries** | Limited, key-based | Complex SQL |
| **Consistency** | Tunable | ACID |
| **Scalability** | Horizontal | Vertical |
| **Joins** | Not supported | Supported |

---

## Data Modeling

### 3. How do you design effective partition keys in Cassandra?

**Answer:**
Partition key design is crucial for data distribution and query performance.

**Design Principles:**
```cql
-- Bad: Sequential keys (hotspotting)
CREATE TABLE bad_events (
    timestamp TIMESTAMP,  -- All writes go to one node
    user_id UUID,
    event_data TEXT,
    PRIMARY KEY (timestamp)
);

-- Good: Distributed keys
CREATE TABLE good_events (
    user_id UUID,         -- Distributes across nodes
    timestamp TIMESTAMP,
    event_data TEXT,
    PRIMARY KEY (user_id, timestamp)
);

-- Better: Composite partition key for even distribution
CREATE TABLE better_events (
    user_id UUID,
    date DATE,           -- Prevents large partitions
    timestamp TIMESTAMP,
    event_data TEXT,
    PRIMARY KEY ((user_id, date), timestamp)
);
```

**Partition Key Strategies:**
```cql
-- Time bucketing for time-series data
CREATE TABLE sensor_data (
    sensor_id UUID,
    bucket TEXT,        -- 'YYYY-MM-DD-HH'
    timestamp TIMESTAMP,
    temperature DOUBLE,
    humidity DOUBLE,
    PRIMARY KEY ((sensor_id, bucket), timestamp)
);

-- Hash-based distribution
CREATE TABLE user_sessions (
    user_hash INT,      -- hash(user_id) % 1000
    user_id UUID,
    session_start TIMESTAMP,
    session_data TEXT,
    PRIMARY KEY ((user_hash, user_id), session_start)
);
```

### 4. How do you handle different query patterns in Cassandra data modeling?

**Answer:**
Cassandra requires denormalization and multiple tables for different query patterns.

**Query-Driven Design:**
```cql
-- Query 1: Get user events by user_id and time range
CREATE TABLE events_by_user (
    user_id UUID,
    event_time TIMESTAMP,
    event_type TEXT,
    event_data MAP<TEXT, TEXT>,
    PRIMARY KEY (user_id, event_time)
) WITH CLUSTERING ORDER BY (event_time DESC);

-- Query 2: Get events by type and time range
CREATE TABLE events_by_type (
    event_type TEXT,
    event_time TIMESTAMP,
    user_id UUID,
    event_data MAP<TEXT, TEXT>,
    PRIMARY KEY (event_type, event_time)
) WITH CLUSTERING ORDER BY (event_time DESC);

-- Query 3: Get daily event counts by type
CREATE TABLE daily_event_counts (
    event_type TEXT,
    date DATE,
    hour INT,
    event_count COUNTER,
    PRIMARY KEY ((event_type, date), hour)
);
```

**Materialized Views:**
```cql
-- Base table
CREATE TABLE user_profiles (
    user_id UUID,
    email TEXT,
    name TEXT,
    city TEXT,
    created_at TIMESTAMP,
    PRIMARY KEY (user_id)
);

-- Materialized view for email lookups
CREATE MATERIALIZED VIEW users_by_email AS
    SELECT user_id, email, name, city, created_at
    FROM user_profiles
    WHERE email IS NOT NULL
    PRIMARY KEY (email, user_id);

-- Materialized view for city-based queries
CREATE MATERIALIZED VIEW users_by_city AS
    SELECT user_id, email, name, city, created_at
    FROM user_profiles
    WHERE city IS NOT NULL
    PRIMARY KEY (city, user_id);
```

---

## Architecture & Replication

### 5. Explain Cassandra's ring architecture and how data is distributed.

**Answer:**
Cassandra uses a peer-to-peer ring architecture where each node is responsible for a range of data.

**Ring Architecture:**
```
Cassandra Ring (4 nodes):
Node A: Token range 0 to 25
Node B: Token range 26 to 50
Node C: Token range 51 to 75
Node D: Token range 76 to 100

Data Distribution:
hash(partition_key) → token → responsible_node
```

**Token Assignment:**
```yaml
# Virtual nodes (vnodes) configuration
num_tokens: 256  # Each node gets 256 token ranges

# Benefits of vnodes:
- Better load distribution
- Faster bootstrap/decommission
- Improved fault tolerance
- Automatic load balancing
```

**Consistent Hashing:**
```python
# Simplified token calculation
import hashlib

def get_token(partition_key):
    """Calculate token for partition key"""
    hash_value = hashlib.md5(partition_key.encode()).hexdigest()
    return int(hash_value, 16) % (2**127)

def find_replicas(token, replication_factor=3):
    """Find replica nodes for token"""
    # Walk clockwise around ring to find RF nodes
    replicas = []
    current_token = token
    
    for _ in range(replication_factor):
        node = find_next_node(current_token)
        replicas.append(node)
        current_token = node.max_token + 1
    
    return replicas
```

### 6. How does Cassandra handle replication and consistency?

**Answer:**
Cassandra provides tunable consistency with multiple replication strategies.

**Replication Strategies:**
```cql
-- Simple Strategy (single datacenter)
CREATE KEYSPACE simple_ks WITH REPLICATION = {
    'class': 'SimpleStrategy',
    'replication_factor': 3
};

-- Network Topology Strategy (multi-datacenter)
CREATE KEYSPACE multi_dc_ks WITH REPLICATION = {
    'class': 'NetworkTopologyStrategy',
    'dc1': 3,
    'dc2': 2
};
```

**Consistency Levels:**
```cql
-- Write consistency levels
INSERT INTO users (id, name, email) VALUES (uuid(), 'John', 'john@example.com')
USING CONSISTENCY ONE;      -- Fast, least consistent
USING CONSISTENCY QUORUM;   -- Balanced
USING CONSISTENCY ALL;      -- Slow, most consistent

-- Read consistency levels
SELECT * FROM users WHERE id = ?
USING CONSISTENCY ONE;      -- Fast, potentially stale
USING CONSISTENCY QUORUM;   -- Balanced
USING CONSISTENCY ALL;      -- Slow, most current
```

**Consistency Formula:**
```
Strong Consistency: R + W > RF
Where:
- R = Read consistency level
- W = Write consistency level  
- RF = Replication factor

Example: RF=3, R=2, W=2 → 2+2 > 3 ✓ (Strong consistency)
```

---

## Performance & Optimization

### 7. How do you optimize Cassandra performance for read and write operations?

**Answer:**
Performance optimization involves proper data modeling, configuration tuning, and hardware considerations.

**Write Optimization:**
```yaml
# cassandra.yaml optimizations
commitlog_sync: periodic
commitlog_sync_period_in_ms: 10000
commitlog_segment_size_in_mb: 32

# Memtable settings
memtable_allocation_type: heap_buffers
memtable_heap_space_in_mb: 2048
memtable_offheap_space_in_mb: 2048

# Compaction strategy
compaction_strategy: LeveledCompactionStrategy
sstable_size_in_mb: 160
```

**Read Optimization:**
```cql
-- Use appropriate indexes
CREATE INDEX ON user_events (event_type);

-- Optimize with ALLOW FILTERING (use sparingly)
SELECT * FROM user_events 
WHERE user_id = ? AND event_type = 'login'
ALLOW FILTERING;

-- Use prepared statements
PREPARE get_user_events AS 
    SELECT * FROM user_events 
    WHERE user_id = ? AND event_time >= ? AND event_time <= ?;

EXECUTE get_user_events USING (uuid(), '2023-12-01', '2023-12-02');
```

**Batch Operations:**
```cql
-- Efficient batch writes (same partition)
BEGIN BATCH
    INSERT INTO user_events (user_id, event_time, event_type) 
    VALUES (?, ?, 'login');
    INSERT INTO user_events (user_id, event_time, event_type) 
    VALUES (?, ?, 'page_view');
    INSERT INTO user_events (user_id, event_time, event_type) 
    VALUES (?, ?, 'logout');
APPLY BATCH;

-- Avoid cross-partition batches (performance killer)
-- Bad: Different partition keys in same batch
```

### 8. How do you handle large partitions and hotspots in Cassandra?

**Answer:**
Large partitions and hotspots can severely impact performance and require specific mitigation strategies.

**Identifying Large Partitions:**
```bash
# Check partition sizes
nodetool cfstats keyspace.table

# Find large partitions
nodetool toppartitions keyspace.table 10

# Analyze with sstable tools
sstablekeys /var/lib/cassandra/data/keyspace/table/
```

**Mitigation Strategies:**
```cql
-- Strategy 1: Time bucketing
-- Before: Large partition
CREATE TABLE user_events_bad (
    user_id UUID,
    event_time TIMESTAMP,
    event_data TEXT,
    PRIMARY KEY (user_id, event_time)  -- Partition grows forever
);

-- After: Time-bucketed partitions
CREATE TABLE user_events_good (
    user_id UUID,
    time_bucket TEXT,    -- 'YYYY-MM-DD' or 'YYYY-MM'
    event_time TIMESTAMP,
    event_data TEXT,
    PRIMARY KEY ((user_id, time_bucket), event_time)
);

-- Strategy 2: Hash distribution
CREATE TABLE distributed_events (
    user_id UUID,
    bucket_id INT,       -- hash(user_id) % 100
    event_time TIMESTAMP,
    event_data TEXT,
    PRIMARY KEY ((user_id, bucket_id), event_time)
);
```

**Application-Level Solutions:**
```python
import hashlib
from datetime import datetime

class CassandraPartitionManager:
    def __init__(self, session):
        self.session = session
        
    def get_time_bucket(self, timestamp, bucket_type='daily'):
        """Generate time bucket for partitioning"""
        if bucket_type == 'daily':
            return timestamp.strftime('%Y-%m-%d')
        elif bucket_type == 'hourly':
            return timestamp.strftime('%Y-%m-%d-%H')
        elif bucket_type == 'monthly':
            return timestamp.strftime('%Y-%m')
    
    def get_hash_bucket(self, user_id, num_buckets=100):
        """Generate hash bucket for distribution"""
        hash_value = hashlib.md5(str(user_id).encode()).hexdigest()
        return int(hash_value, 16) % num_buckets
    
    def insert_event(self, user_id, event_time, event_data):
        """Insert with proper bucketing"""
        time_bucket = self.get_time_bucket(event_time)
        
        query = """
            INSERT INTO user_events (user_id, time_bucket, event_time, event_data)
            VALUES (?, ?, ?, ?)
        """
        self.session.execute(query, (user_id, time_bucket, event_time, event_data))
    
    def query_events(self, user_id, start_date, end_date):
        """Query across multiple buckets"""
        results = []
        current_date = start_date
        
        while current_date <= end_date:
            time_bucket = self.get_time_bucket(current_date)
            
            query = """
                SELECT * FROM user_events 
                WHERE user_id = ? AND time_bucket = ?
                AND event_time >= ? AND event_time <= ?
            """
            
            rows = self.session.execute(query, (user_id, time_bucket, start_date, end_date))
            results.extend(rows)
            
            current_date += timedelta(days=1)
        
        return results
```

---

## Operations & Monitoring

### 9. How do you monitor and maintain a Cassandra cluster?

**Answer:**
Comprehensive monitoring involves tracking key metrics and performing regular maintenance tasks.

**Key Metrics:**
```bash
# Node health
nodetool status
nodetool info
nodetool tpstats

# Performance metrics
nodetool cfstats keyspace.table
nodetool proxyhistograms
nodetool tablehistograms keyspace.table

# Compaction status
nodetool compactionstats
nodetool compactionhistory

# Repair status
nodetool repair keyspace.table
nodetool netstats
```

**Monitoring Script:**
```python
import subprocess
import json
from datetime import datetime

class CassandraMonitor:
    def __init__(self):
        self.metrics = {}
    
    def get_node_status(self):
        """Get cluster node status"""
        result = subprocess.run(['nodetool', 'status'], 
                              capture_output=True, text=True)
        
        nodes = []
        for line in result.stdout.split('\n')[5:]:  # Skip header
            if line.strip() and not line.startswith('--'):
                parts = line.split()
                if len(parts) >= 6:
                    nodes.append({
                        'status': parts[0],
                        'state': parts[1],
                        'address': parts[2],
                        'load': parts[3],
                        'tokens': parts[4],
                        'owns': parts[5],
                        'host_id': parts[6] if len(parts) > 6 else None
                    })
        
        return nodes
    
    def get_table_stats(self, keyspace, table):
        """Get table statistics"""
        result = subprocess.run(['nodetool', 'cfstats', f'{keyspace}.{table}'], 
                              capture_output=True, text=True)
        
        stats = {}
        for line in result.stdout.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                stats[key.strip()] = value.strip()
        
        return stats
    
    def check_cluster_health(self):
        """Comprehensive health check"""
        health_report = {
            'timestamp': datetime.now().isoformat(),
            'nodes': self.get_node_status(),
            'alerts': []
        }
        
        # Check for down nodes
        down_nodes = [node for node in health_report['nodes'] 
                     if node['status'] != 'UN']
        if down_nodes:
            health_report['alerts'].append({
                'severity': 'critical',
                'message': f'{len(down_nodes)} nodes are down',
                'nodes': down_nodes
            })
        
        # Check load distribution
        loads = [float(node['load'].replace('GB', '').replace('MB', '').replace('KB', '')) 
                for node in health_report['nodes'] if node['load'] != '?']
        
        if loads:
            avg_load = sum(loads) / len(loads)
            max_load = max(loads)
            
            if max_load > avg_load * 2:
                health_report['alerts'].append({
                    'severity': 'warning',
                    'message': 'Load imbalance detected',
                    'avg_load': avg_load,
                    'max_load': max_load
                })
        
        return health_report
```

### 10. How do you perform backup and disaster recovery for Cassandra?

**Answer:**
Cassandra backup strategies include snapshots, incremental backups, and cross-datacenter replication.

**Snapshot-based Backup:**
```bash
# Create snapshot
nodetool snapshot keyspace_name

# List snapshots
nodetool listsnapshots

# Clear old snapshots
nodetool clearsnapshot

# Automated backup script
#!/bin/bash
KEYSPACE="user_data"
BACKUP_DIR="/backup/cassandra"
DATE=$(date +%Y%m%d_%H%M%S)

# Create snapshot
nodetool snapshot $KEYSPACE -t backup_$DATE

# Copy snapshot files
for node_dir in /var/lib/cassandra/data/$KEYSPACE/*/snapshots/backup_$DATE/; do
    if [ -d "$node_dir" ]; then
        table_name=$(basename $(dirname $(dirname $node_dir)))
        mkdir -p $BACKUP_DIR/$DATE/$table_name
        cp $node_dir/* $BACKUP_DIR/$DATE/$table_name/
    fi
done

# Cleanup old backups (keep 7 days)
find $BACKUP_DIR -type d -mtime +7 -exec rm -rf {} \;
```

**Incremental Backup:**
```yaml
# cassandra.yaml
incremental_backups: true

# Backup script for incremental files
#!/bin/bash
KEYSPACE="user_data"
INCREMENTAL_DIR="/var/lib/cassandra/data/$KEYSPACE"
BACKUP_DIR="/backup/incremental"
DATE=$(date +%Y%m%d_%H%M%S)

# Copy incremental backup files
find $INCREMENTAL_DIR -name "backups" -type d | while read backup_path; do
    table_path=$(dirname $backup_path)
    table_name=$(basename $table_path)
    
    if [ "$(ls -A $backup_path)" ]; then
        mkdir -p $BACKUP_DIR/$DATE/$table_name
        cp $backup_path/* $BACKUP_DIR/$DATE/$table_name/
        rm $backup_path/*  # Clean up after copying
    fi
done
```

**Disaster Recovery:**
```bash
# Restore from snapshot
# 1. Stop Cassandra
sudo service cassandra stop

# 2. Clear existing data
rm -rf /var/lib/cassandra/data/keyspace_name

# 3. Restore snapshot files
mkdir -p /var/lib/cassandra/data/keyspace_name/table_name
cp /backup/20231201_120000/table_name/* /var/lib/cassandra/data/keyspace_name/table_name/

# 4. Fix ownership
chown -R cassandra:cassandra /var/lib/cassandra/data

# 5. Start Cassandra
sudo service cassandra start

# 6. Refresh schema
nodetool refresh keyspace_name table_name
```

**Cross-Datacenter Replication:**
```cql
-- Setup for disaster recovery
CREATE KEYSPACE user_data WITH REPLICATION = {
    'class': 'NetworkTopologyStrategy',
    'dc1': 3,  -- Primary datacenter
    'dc2': 3   -- Disaster recovery datacenter
};

-- Monitor replication lag
SELECT * FROM system.peers;
```

---

## Summary

Apache Cassandra provides distributed NoSQL database capabilities with:

1. **Distributed Architecture**: Linear scalability and no single point of failure
2. **Flexible Data Model**: Wide-column model for various use cases
3. **Tunable Consistency**: Balance between consistency and availability
4. **High Performance**: Optimized for write-heavy workloads
5. **Operational Simplicity**: Peer-to-peer architecture with automatic data distribution