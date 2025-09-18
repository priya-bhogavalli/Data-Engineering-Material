# 🗄️ Apache HBase Interview Questions & Answers

## 📋 Table of Contents
- [Basic Concepts](#basic-concepts)
- [Architecture](#architecture)
- [Data Model](#data-model)
- [Operations](#operations)
- [Performance](#performance)
- [Advanced Topics](#advanced-topics)

---

## Basic Concepts

### 1. What is Apache HBase and its key features?
**Answer:**
HBase is a distributed, column-oriented NoSQL database built on Hadoop HDFS.

**Key Features:**
- **Column-family storage**: Data organized in column families
- **Horizontal scalability**: Scales across commodity hardware
- **Strong consistency**: ACID properties for single-row operations
- **Automatic sharding**: Data automatically partitioned
- **Hadoop integration**: Built on HDFS

### 2. What is the HBase data model?
**Answer:**
HBase uses a sparse, distributed, persistent multi-dimensional sorted map.

**Structure:**
```
Table
├── Row Key (Primary Key)
├── Column Family 1
│   ├── Column Qualifier 1
│   └── Column Qualifier 2
└── Column Family 2
    ├── Column Qualifier 1
    └── Column Qualifier 2
```

**Example:**
```
Row: user123
CF: personal
  name: "John Doe"
  age: "30"
CF: contact
  email: "john@example.com"
  phone: "555-1234"
```

### 3. Explain HBase architecture components.
**Answer:**
**Master Components:**
- **HMaster**: Coordinates cluster, manages regions
- **ZooKeeper**: Coordination service, configuration management

**Region Components:**
- **RegionServer**: Serves data for regions
- **Region**: Contiguous range of rows
- **Store**: Column family within region
- **MemStore**: In-memory write buffer
- **HFile**: Persistent storage on HDFS

### 4. What is a Region in HBase?
**Answer:**
A Region is a contiguous range of rows stored together.

**Characteristics:**
- Contains subset of table's rows
- Served by single RegionServer
- Split when size threshold reached
- Basic unit of scalability

**Region Split:**
```
Original Region: [A-Z]
After Split:
├── Region 1: [A-M]
└── Region 2: [N-Z]
```

### 5. What are Column Families in HBase?
**Answer:**
Column Families group related columns together.

**Properties:**
- Defined at table creation
- All columns in family stored together
- Different storage properties per family
- Optimized for access patterns

**Example:**
```bash
create 'users', 'personal', 'contact', 'preferences'
```

---

## Architecture

### 6. How does HBase handle reads and writes?
**Answer:**
**Write Path:**
1. Write to WAL (Write-Ahead Log)
2. Write to MemStore
3. Flush to HFile when MemStore full
4. Compaction merges HFiles

**Read Path:**
1. Check MemStore
2. Check HFiles
3. Merge results
4. Return latest version

### 7. What is the role of ZooKeeper in HBase?
**Answer:**
ZooKeeper provides coordination services:

**Functions:**
- **Configuration management**: Cluster configuration
- **Leader election**: HMaster election
- **Region assignment**: Track region locations
- **Synchronization**: Distributed coordination

### 8. Explain HBase compaction process.
**Answer:**
**Minor Compaction:**
- Merges smaller HFiles
- Removes deleted cells
- Automatic process

**Major Compaction:**
- Merges all HFiles in store
- Removes all deleted/expired data
- Resource intensive

**Configuration:**
```xml
<property>
  <name>hbase.hstore.compaction.min</name>
  <value>3</value>
</property>
```

### 9. What is WAL in HBase?
**Answer:**
Write-Ahead Log ensures durability.

**Process:**
1. Write operation logged to WAL
2. Data written to MemStore
3. WAL provides recovery mechanism
4. Replayed during crash recovery

### 10. How does HBase achieve fault tolerance?
**Answer:**
**Mechanisms:**
- **HDFS replication**: Data replicated across nodes
- **WAL recovery**: Replay logs after failure
- **Region reassignment**: Failed regions moved to healthy servers
- **ZooKeeper coordination**: Failure detection and recovery

---

## Data Model

### 11. How do you design row keys in HBase?
**Answer:**
**Best Practices:**
- **Avoid hotspotting**: Don't use sequential keys
- **Salt prefixes**: Add random prefix for distribution
- **Reverse timestamps**: For time-series data
- **Composite keys**: Combine multiple attributes

**Examples:**
```bash
# Bad: Sequential
user001, user002, user003

# Good: Salted
a_user001, b_user002, c_user003

# Good: Reverse timestamp
user123_9999999999-timestamp
```

### 12. What are HBase filters and how to use them?
**Answer:**
Filters reduce data transferred from server to client.

**Common Filters:**
```java
// Row key filter
Filter rowFilter = new PrefixFilter(Bytes.toBytes("user"));

// Column value filter
Filter valueFilter = new SingleColumnValueFilter(
    Bytes.toBytes("cf"), 
    Bytes.toBytes("age"),
    CompareOp.GREATER, 
    Bytes.toBytes("25")
);

// Combine filters
FilterList filterList = new FilterList(
    FilterList.Operator.MUST_PASS_ALL,
    rowFilter, valueFilter
);
```

### 13. How do you handle versioning in HBase?
**Answer:**
HBase maintains multiple versions of each cell.

**Configuration:**
```bash
# Set max versions
alter 'users', {NAME => 'personal', VERSIONS => 5}

# Get specific version
get 'users', 'user123', {COLUMN => 'personal:name', VERSIONS => 3}
```

**Version Management:**
- Latest version returned by default
- Older versions garbage collected
- TTL can be set for automatic cleanup

### 14. What are HBase coprocessors?
**Answer:**
Coprocessors enable server-side processing.

**Types:**
- **Observer**: Triggered by events (like triggers)
- **Endpoint**: Custom RPC services

**Example Observer:**
```java
public class AuditCoprocessor extends BaseRegionObserver {
    @Override
    public void prePut(ObserverContext<RegionCoprocessorEnvironment> e,
                       Put put, WALEdit edit, Durability durability) {
        // Log all puts
        LOG.info("Put operation: " + put.toString());
    }
}
```

### 15. How do you implement secondary indexes in HBase?
**Answer:**
**Approaches:**
1. **Manual indexing**: Create separate index tables
2. **Phoenix**: SQL layer with automatic indexing
3. **Coprocessors**: Custom indexing logic

**Manual Index Example:**
```bash
# Main table
create 'users', 'data'

# Index table (email -> rowkey)
create 'users_email_index', 'ref'

# Application maintains both tables
put 'users', 'user123', 'data:email', 'john@example.com'
put 'users_email_index', 'john@example.com', 'ref:rowkey', 'user123'
```

---

## Operations

### 16. How do you create and manage tables in HBase?
**Answer:**
**Table Operations:**
```bash
# Create table
create 'users', 'personal', 'contact'

# List tables
list

# Describe table
describe 'users'

# Alter table
alter 'users', {NAME => 'personal', TTL => 86400}

# Drop table
disable 'users'
drop 'users'
```

### 17. How do you perform CRUD operations in HBase?
**Answer:**
**Basic Operations:**
```bash
# Create/Update (Put)
put 'users', 'user123', 'personal:name', 'John Doe'
put 'users', 'user123', 'personal:age', '30'

# Read (Get)
get 'users', 'user123'
get 'users', 'user123', 'personal:name'

# Scan
scan 'users'
scan 'users', {STARTROW => 'user100', ENDROW => 'user200'}

# Delete
delete 'users', 'user123', 'personal:age'
deleteall 'users', 'user123'
```

### 18. How do you bulk load data into HBase?
**Answer:**
**Methods:**
1. **Put operations**: Direct API calls
2. **Bulk load**: Generate HFiles and load
3. **Import tools**: CSV/TSV import utilities

**Bulk Load Process:**
```bash
# Generate HFiles using MapReduce
hadoop jar hbase-server.jar importtsv \
  -Dimporttsv.columns=HBASE_ROW_KEY,personal:name,personal:age \
  -Dimporttsv.bulk.output=/tmp/hfiles \
  users /input/data.tsv

# Load HFiles into HBase
hadoop jar hbase-server.jar completebulkload /tmp/hfiles users
```

### 19. How do you backup and restore HBase data?
**Answer:**
**Backup Methods:**
1. **Export/Import**: Table-level backup
2. **Snapshots**: Point-in-time copies
3. **Replication**: Live backup to another cluster

**Snapshot Operations:**
```bash
# Create snapshot
snapshot 'users', 'users_backup_20240301'

# List snapshots
list_snapshots

# Restore from snapshot
disable 'users'
restore_snapshot 'users_backup_20240301'
enable 'users'

# Clone from snapshot
clone_snapshot 'users_backup_20240301', 'users_restored'
```

### 20. How do you monitor HBase performance?
**Answer:**
**Monitoring Tools:**
- **HBase Master UI**: Web interface
- **RegionServer UI**: Region-level metrics
- **Ganglia/Nagios**: External monitoring
- **JMX metrics**: Programmatic access

**Key Metrics:**
```bash
# Region server metrics
hbase hbck
hbase regionserver

# Table statistics
hbase org.apache.hadoop.hbase.util.HBaseConfTool

# Performance counters
- Read/Write request rates
- Region split/compaction rates
- Memory usage
- GC performance
```

---

## Performance

### 21. How do you optimize HBase performance?
**Answer:**
**Optimization Strategies:**

**1. Schema Design:**
- Proper row key design
- Appropriate column families
- Optimal block size

**2. Configuration Tuning:**
```xml
<!-- Increase heap size -->
<property>
  <name>hbase.regionserver.global.memstore.size</name>
  <value>0.4</value>
</property>

<!-- Optimize compaction -->
<property>
  <name>hbase.hstore.compaction.throughput.lower.bound</name>
  <value>50000000</value>
</property>
```

**3. Hardware Optimization:**
- SSD for WAL
- Sufficient RAM for MemStore
- Network bandwidth

### 22. What causes hotspotting in HBase and how to avoid it?
**Answer:**
**Causes:**
- Sequential row keys
- Timestamp-based keys
- Uneven data distribution

**Solutions:**
```bash
# Salt row keys
Original: user_20240301_001
Salted: a_user_20240301_001

# Reverse timestamps
Original: user_1709251200_data
Reversed: user_8290748800_data

# Hash prefixes
Original: user123
Hashed: md5(user123)[0:2]_user123
```

### 23. How do you tune HBase for write-heavy workloads?
**Answer:**
**Write Optimizations:**

**1. MemStore Configuration:**
```xml
<property>
  <name>hbase.regionserver.global.memstore.size</name>
  <value>0.6</value>
</property>
```

**2. WAL Configuration:**
```xml
<property>
  <name>hbase.regionserver.hlog.blocksize</name>
  <value>134217728</value>
</property>
```

**3. Compaction Settings:**
```xml
<property>
  <name>hbase.hstore.compaction.min</name>
  <value>5</value>
</property>
```

### 24. How do you optimize HBase for read performance?
**Answer:**
**Read Optimizations:**

**1. Block Cache:**
```xml
<property>
  <name>hfile.block.cache.size</name>
  <value>0.25</value>
</property>
```

**2. Bloom Filters:**
```bash
alter 'users', {NAME => 'personal', BLOOMFILTER => 'ROW'}
```

**3. Compression:**
```bash
alter 'users', {NAME => 'personal', COMPRESSION => 'SNAPPY'}
```

### 25. What are HBase best practices for production?
**Answer:**
**Production Guidelines:**

**1. Hardware:**
- Dedicated RegionServer nodes
- SSD for WAL storage
- Sufficient RAM (64GB+)

**2. Configuration:**
- Tune GC settings
- Optimize heap sizes
- Configure proper timeouts

**3. Monitoring:**
- Set up alerting
- Monitor key metrics
- Regular health checks

---

## Advanced Topics

### 26. How does HBase replication work?
**Answer:**
**Replication Types:**
- **Master-Slave**: One-way replication
- **Master-Master**: Bi-directional replication

**Setup:**
```bash
# Enable replication
add_peer '1', 'zk1,zk2,zk3:2181:/hbase'

# Enable table replication
alter 'users', {REPLICATION_SCOPE => 1}

# Check replication status
status 'replication'
```

### 27. What is Phoenix and how does it integrate with HBase?
**Answer:**
Phoenix provides SQL interface over HBase.

**Features:**
- **SQL queries**: Standard SQL syntax
- **Secondary indexes**: Automatic index management
- **Views**: Logical table abstractions
- **JDBC driver**: Standard database connectivity

**Example:**
```sql
-- Create Phoenix table
CREATE TABLE users (
    id VARCHAR PRIMARY KEY,
    name VARCHAR,
    age INTEGER
);

-- Query with SQL
SELECT name, age FROM users WHERE age > 25;
```

### 28. How do you implement time-series data in HBase?
**Answer:**
**Design Pattern:**
```bash
# Row key: metric_name + reverse_timestamp
# Example: cpu_usage_9999999999999-1709251200

create 'metrics', 'data'

# Put time-series data
put 'metrics', 'cpu_usage_9999998290748800', 'data:value', '85.5'
put 'metrics', 'cpu_usage_9999998290748801', 'data:value', '87.2'

# Scan recent data (reverse timestamp ensures latest first)
scan 'metrics', {STARTROW => 'cpu_usage_9999998290748000'}
```

### 29. How do you handle large objects in HBase?
**Answer:**
**Strategies:**
1. **MOB (Medium Object)**: Built-in support for objects 100KB-10MB
2. **External storage**: Store references, data in HDFS/S3
3. **Chunking**: Split large objects into smaller pieces

**MOB Configuration:**
```bash
# Enable MOB for column family
alter 'documents', {NAME => 'content', IS_MOB => true, MOB_THRESHOLD => 102400}
```

### 30. What are the differences between HBase and Cassandra?
**Answer:**
| Feature | HBase | Cassandra |
|---------|-------|-----------|
| **Consistency** | Strong | Tunable |
| **Architecture** | Master-slave | Peer-to-peer |
| **Data Model** | Column-family | Wide-column |
| **Query Language** | API/Phoenix | CQL |
| **Hadoop Integration** | Native | Limited |

### 31. How do you migrate data from RDBMS to HBase?
**Answer:**
**Migration Steps:**
1. **Schema mapping**: RDBMS tables to HBase tables
2. **Row key design**: Convert primary keys
3. **Data extraction**: Export from RDBMS
4. **Data transformation**: Format for HBase
5. **Bulk load**: Import into HBase

**Example:**
```bash
# Export from MySQL
mysqldump --tab=/tmp/export database_name table_name

# Transform to HBase format
# Convert CSV to HBase puts or bulk load format

# Bulk load into HBase
hbase org.apache.hadoop.hbase.mapreduce.ImportTsv \
  -Dimporttsv.columns=HBASE_ROW_KEY,cf:col1,cf:col2 \
  table_name /input/data
```

### 32. How do you implement security in HBase?
**Answer:**
**Security Features:**
1. **Authentication**: Kerberos integration
2. **Authorization**: ACL-based permissions
3. **Encryption**: Data at rest and in transit

**Configuration:**
```xml
<!-- Enable security -->
<property>
  <name>hbase.security.authentication</name>
  <value>kerberos</value>
</property>

<property>
  <name>hbase.security.authorization</name>
  <value>true</value>
</property>
```

**ACL Management:**
```bash
# Grant permissions
grant 'user1', 'RW', 'users'
grant 'user2', 'R', 'users', 'personal'

# Revoke permissions
revoke 'user1', 'users'
```

### 33. How do you troubleshoot HBase performance issues?
**Answer:**
**Common Issues:**

**1. Slow Reads:**
- Check block cache hit ratio
- Verify bloom filter usage
- Monitor compaction status

**2. Slow Writes:**
- Check MemStore flush frequency
- Monitor WAL sync times
- Verify region distribution

**3. RegionServer Issues:**
- Monitor GC performance
- Check memory usage
- Verify network connectivity

**Diagnostic Commands:**
```bash
# Check cluster health
hbase hbck

# Monitor region distribution
hbase org.apache.hadoop.hbase.util.HRegionsMover

# Check table statistics
hbase org.apache.hadoop.hbase.util.HBaseConfTool
```

### 34. What are HBase anti-patterns to avoid?
**Answer:**
**Anti-patterns:**

**1. Poor Row Key Design:**
- Sequential keys causing hotspots
- Keys too long or too short
- Non-uniform distribution

**2. Schema Issues:**
- Too many column families
- Inappropriate data types
- Missing compression

**3. Operational Mistakes:**
- Running major compaction during peak hours
- Insufficient monitoring
- Poor capacity planning

### 35. How do you scale HBase clusters?
**Answer:**
**Scaling Strategies:**

**1. Horizontal Scaling:**
```bash
# Add RegionServer nodes
# Regions automatically redistributed
# Linear scalability for most workloads
```

**2. Vertical Scaling:**
- Increase memory per node
- Add more CPU cores
- Upgrade to faster storage

**3. Pre-splitting:**
```bash
# Pre-split table for better distribution
create 'users', 'data', {SPLITS => ['row10', 'row20', 'row30']}
```

**Monitoring Scale:**
- Track region count per server
- Monitor request distribution
- Watch for hotspotting

---

*This comprehensive guide covers 35+ essential Apache HBase interview questions with detailed answers and practical examples for data engineering interviews.*