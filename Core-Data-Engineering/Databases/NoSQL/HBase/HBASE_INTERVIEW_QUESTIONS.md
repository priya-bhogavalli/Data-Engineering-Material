# Apache HBase Interview Questions & Answers

## 📋 Table of Contents
1. [Core Concepts](#core-concepts)
2. [Architecture & Components](#architecture--components)
3. [Data Model & Operations](#data-model--operations)
4. [Performance & Optimization](#performance--optimization)
5. [Administration & Monitoring](#administration--monitoring)

---

## Core Concepts

### 1. What is Apache HBase and when should you use it?

**Answer:**
Apache HBase is a distributed, scalable, NoSQL database built on top of Hadoop HDFS, modeled after Google's Bigtable.

**Key Characteristics:**
- **Column-oriented**: Data stored in column families
- **Distributed**: Scales horizontally across commodity hardware
- **Consistent**: Strong consistency for reads and writes
- **Fault-tolerant**: Built on HDFS with automatic failover

**Use Cases:**
```yaml
ideal_for:
  - Large datasets (billions of rows, millions of columns)
  - Real-time read/write access
  - Sparse data with varying column structures
  - Time-series data and event logging
  - Random access patterns

not_ideal_for:
  - Complex queries and joins
  - ACID transactions across multiple rows
  - Small datasets (<1GB)
  - Ad-hoc analytics queries
```

### 2. How does HBase's data model work?

**Answer:**
HBase uses a sparse, distributed, persistent multi-dimensional sorted map.

**Data Model Structure:**
```
Table
├── Row Key (unique identifier)
├── Column Family 1
│   ├── Column Qualifier 1 → Cell (value + timestamp)
│   └── Column Qualifier 2 → Cell (value + timestamp)
└── Column Family 2
    ├── Column Qualifier 1 → Cell (value + timestamp)
    └── Column Qualifier 2 → Cell (value + timestamp)
```

**Example:**
```java
// Conceptual representation
Table: user_profiles
Row Key: user123
├── personal_info:name → "John Doe" (timestamp: 1640995200000)
├── personal_info:email → "john@example.com" (timestamp: 1640995200000)
├── activity:last_login → "2023-12-01" (timestamp: 1701388800000)
└── activity:page_views → "150" (timestamp: 1701388800000)
```

**Key Properties:**
- **Row Key**: Unique identifier, lexicographically sorted
- **Column Family**: Groups related columns, defined at table creation
- **Column Qualifier**: Specific column within a family
- **Cell**: Intersection of row, column family, and qualifier
- **Timestamp**: Version identifier for each cell value

---

## Architecture & Components

### 3. Explain HBase's architecture and key components.

**Answer:**
HBase follows a master-slave architecture with several key components.

**Architecture Overview:**
```
HBase Cluster:
├── HMaster (Master Server)
│   ├── Region assignment
│   ├── Schema changes
│   └── Load balancing
├── RegionServer (Slave Servers)
│   ├── Serve regions
│   ├── Handle client requests
│   └── Manage WAL and MemStore
├── ZooKeeper
│   ├── Coordination service
│   ├── Master election
│   └── Region metadata
└── HDFS (Storage Layer)
    ├── HFiles (data files)
    ├── WAL (Write-Ahead Log)
    └── Metadata
```

**Component Details:**
```java
// RegionServer components
RegionServer {
    - Regions[] (data partitions)
    - MemStore (in-memory write buffer)
    - BlockCache (read cache)
    - WAL (Write-Ahead Log)
    - Compaction processes
}

// Region structure
Region {
    - Start key and end key
    - Column families
    - HFiles (sorted data files)
    - MemStore per column family
}
```

### 4. How does HBase handle data distribution and load balancing?

**Answer:**
HBase automatically partitions tables into regions and distributes them across RegionServers.

**Region Management:**
```bash
# Region splitting
# When region size exceeds threshold (default 10GB)
Original Region: [startKey, endKey] → Split into:
├── Region 1: [startKey, splitKey]
└── Region 2: [splitKey, endKey]

# Load balancing
# HMaster monitors RegionServer load and reassigns regions
```

**Configuration:**
```xml
<!-- hbase-site.xml -->
<configuration>
    <property>
        <name>hbase.hregion.max.filesize</name>
        <value>10737418240</value> <!-- 10GB -->
    </property>
    <property>
        <name>hbase.hregion.majorcompaction</name>
        <value>604800000</value> <!-- 7 days -->
    </property>
</configuration>
```

**Manual Region Management:**
```bash
# Pre-split table for better distribution
create 'user_events', 'cf1', SPLITS => ['1000', '2000', '3000', '4000']

# Manual region splitting
split 'user_events', '2500'

# Move region to different server
move 'region_name', 'target_server'
```

---

## Data Model & Operations

### 5. How do you design an effective row key strategy?

**Answer:**
Row key design is crucial for HBase performance as it determines data distribution and access patterns.

**Row Key Design Principles:**
```java
// Bad: Sequential keys (hotspotting)
String badRowKey = timestamp + "_" + userId;  // All writes go to one region

// Good: Distributed keys
String goodRowKey = userId + "_" + timestamp;  // Distributes across regions

// Better: Salted keys for even distribution
String saltedRowKey = (userId.hashCode() % 100) + "_" + userId + "_" + timestamp;
```

**Common Patterns:**
```java
// Time-series data
public class TimeSeriesRowKey {
    // Reverse timestamp for recent data access
    public static String createRowKey(String entityId, long timestamp) {
        long reversedTimestamp = Long.MAX_VALUE - timestamp;
        return entityId + "_" + String.format("%019d", reversedTimestamp);
    }
}

// User activity tracking
public class UserActivityRowKey {
    public static String createRowKey(String userId, String date, String activityType) {
        // Hash prefix for distribution
        int hash = (userId + date).hashCode() % 1000;
        return String.format("%03d_%s_%s_%s", hash, userId, date, activityType);
    }
}
```

### 6. How do you perform CRUD operations in HBase?

**Answer:**
HBase provides APIs for Create, Read, Update, and Delete operations.

**Java API Operations:**
```java
import org.apache.hadoop.hbase.*;
import org.apache.hadoop.hbase.client.*;

public class HBaseOperations {
    private Connection connection;
    private Table table;
    
    public void setupConnection() throws IOException {
        Configuration config = HBaseConfiguration.create();
        connection = ConnectionFactory.createConnection(config);
        table = connection.getTable(TableName.valueOf("user_profiles"));
    }
    
    // CREATE/UPDATE (Put operation)
    public void putData(String rowKey, String family, String qualifier, String value) 
            throws IOException {
        Put put = new Put(Bytes.toBytes(rowKey));
        put.addColumn(Bytes.toBytes(family), Bytes.toBytes(qualifier), Bytes.toBytes(value));
        table.put(put);
    }
    
    // READ (Get operation)
    public String getData(String rowKey, String family, String qualifier) 
            throws IOException {
        Get get = new Get(Bytes.toBytes(rowKey));
        get.addColumn(Bytes.toBytes(family), Bytes.toBytes(qualifier));
        
        Result result = table.get(get);
        byte[] value = result.getValue(Bytes.toBytes(family), Bytes.toBytes(qualifier));
        return value != null ? Bytes.toString(value) : null;
    }
    
    // SCAN (Range queries)
    public void scanData(String startRow, String endRow) throws IOException {
        Scan scan = new Scan();
        scan.withStartRow(Bytes.toBytes(startRow));
        scan.withStopRow(Bytes.toBytes(endRow));
        
        ResultScanner scanner = table.getScanner(scan);
        for (Result result : scanner) {
            for (Cell cell : result.rawCells()) {
                System.out.println(
                    "Row: " + Bytes.toString(CellUtil.cloneRow(cell)) +
                    ", Family: " + Bytes.toString(CellUtil.cloneFamily(cell)) +
                    ", Qualifier: " + Bytes.toString(CellUtil.cloneQualifier(cell)) +
                    ", Value: " + Bytes.toString(CellUtil.cloneValue(cell))
                );
            }
        }
        scanner.close();
    }
    
    // DELETE
    public void deleteData(String rowKey) throws IOException {
        Delete delete = new Delete(Bytes.toBytes(rowKey));
        table.delete(delete);
    }
    
    // Batch operations
    public void batchOperations(List<Put> puts) throws IOException {
        table.put(puts);
    }
}
```

**HBase Shell Operations:**
```bash
# Create table
create 'user_profiles', 'personal_info', 'activity'

# Put data
put 'user_profiles', 'user123', 'personal_info:name', 'John Doe'
put 'user_profiles', 'user123', 'personal_info:email', 'john@example.com'
put 'user_profiles', 'user123', 'activity:last_login', '2023-12-01'

# Get data
get 'user_profiles', 'user123'
get 'user_profiles', 'user123', 'personal_info:name'

# Scan data
scan 'user_profiles'
scan 'user_profiles', {STARTROW => 'user100', ENDROW => 'user200'}

# Delete data
delete 'user_profiles', 'user123', 'personal_info:email'
deleteall 'user_profiles', 'user123'
```

---

## Performance & Optimization

### 7. How do you optimize HBase performance for read and write operations?

**Answer:**
HBase performance optimization involves multiple strategies across different components.

**Write Optimization:**
```java
// Batch writes for better throughput
public void optimizedWrites() throws IOException {
    List<Put> puts = new ArrayList<>();
    
    for (int i = 0; i < 1000; i++) {
        Put put = new Put(Bytes.toBytes("row" + i));
        put.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col1"), Bytes.toBytes("value" + i));
        puts.add(put);
    }
    
    // Batch write
    table.put(puts);
    
    // Disable WAL for bulk loads (use with caution)
    put.setDurability(Durability.SKIP_WAL);
}

// Configure write buffer
Configuration config = HBaseConfiguration.create();
config.setLong("hbase.client.write.buffer", 12 * 1024 * 1024); // 12MB buffer
```

**Read Optimization:**
```java
// Use filters to reduce data transfer
public void optimizedReads() throws IOException {
    Scan scan = new Scan();
    
    // Column family filter
    scan.addFamily(Bytes.toBytes("cf1"));
    
    // Value filter
    Filter valueFilter = new ValueFilter(CompareFilter.CompareOp.EQUAL, 
                                       new BinaryComparator(Bytes.toBytes("target_value")));
    scan.setFilter(valueFilter);
    
    // Limit results
    scan.setMaxResultSize(1024 * 1024); // 1MB
    scan.setCaching(100); // Cache 100 rows
    
    // Use bloom filters
    scan.setFilter(new BloomFilter());
}
```

**Configuration Tuning:**
```xml
<!-- hbase-site.xml optimizations -->
<configuration>
    <!-- MemStore settings -->
    <property>
        <name>hbase.hregion.memstore.flush.size</name>
        <value>134217728</value> <!-- 128MB -->
    </property>
    
    <!-- Block cache settings -->
    <property>
        <name>hfile.block.cache.size</name>
        <value>0.4</value> <!-- 40% of heap -->
    </property>
    
    <!-- Compaction settings -->
    <property>
        <name>hbase.hstore.compaction.min</name>
        <value>3</value>
    </property>
    
    <!-- Handler threads -->
    <property>
        <name>hbase.regionserver.handler.count</name>
        <value>100</value>
    </property>
</configuration>
```

### 8. How do you handle hotspotting in HBase?

**Answer:**
Hotspotting occurs when too many requests target a single region, causing performance bottlenecks.

**Identifying Hotspots:**
```bash
# Monitor region server metrics
hbase shell
> status 'detailed'

# Check region distribution
> list_regions 'table_name'

# Monitor request patterns
# Use HBase web UI: http://master:16010
```

**Prevention Strategies:**
```java
// 1. Salting row keys
public class SaltedRowKey {
    private static final int SALT_BUCKETS = 100;
    
    public static String createSaltedKey(String originalKey) {
        int salt = originalKey.hashCode() % SALT_BUCKETS;
        return String.format("%02d_%s", Math.abs(salt), originalKey);
    }
    
    public static String extractOriginalKey(String saltedKey) {
        return saltedKey.substring(3); // Remove salt prefix
    }
}

// 2. Reverse timestamp for time-series data
public static String createTimeSeriesKey(String entityId, long timestamp) {
    long reversedTimestamp = Long.MAX_VALUE - timestamp;
    return entityId + "_" + reversedTimestamp;
}

// 3. Hash-based distribution
public static String createHashedKey(String userId, String eventType) {
    int hash = (userId + eventType).hashCode() % 1000;
    return String.format("%03d_%s_%s", Math.abs(hash), userId, eventType);
}
```

**Table Pre-splitting:**
```bash
# Pre-split table to avoid hotspots
create 'events', 'cf1', SPLITS => ['100', '200', '300', '400', '500', '600', '700', '800', '900']

# Or use hex splits for better distribution
create 'events', 'cf1', SPLITS_FILE => 'splits.txt'
# splits.txt contains: 10, 20, 30, 40, 50, 60, 70, 80, 90, a0, b0, c0, d0, e0, f0
```

---

## Administration & Monitoring

### 9. How do you monitor and troubleshoot HBase clusters?

**Answer:**
Comprehensive monitoring involves multiple tools and metrics to ensure cluster health.

**Key Metrics to Monitor:**
```yaml
regionserver_metrics:
  - Request rate (reads/writes per second)
  - Request latency (95th, 99th percentile)
  - Region count per server
  - MemStore size and flush frequency
  - Block cache hit ratio
  - Compaction queue size

master_metrics:
  - Region assignment time
  - Dead region servers
  - Load balancer runs
  - Schema change operations

cluster_metrics:
  - HDFS usage and availability
  - ZooKeeper connectivity
  - Network I/O and disk I/O
  - JVM heap usage and GC frequency
```

**Monitoring Tools:**
```bash
# HBase built-in monitoring
# Web UI: http://master:16010 and http://regionserver:16030

# JMX metrics
jconsole # Connect to HBase processes

# Command line monitoring
hbase shell
> status 'detailed'
> list_regions 'table_name'

# Log analysis
tail -f /var/log/hbase/hbase-regionserver.log
grep -i "error\|exception\|warn" /var/log/hbase/*.log
```

**Performance Troubleshooting:**
```java
// Custom monitoring application
public class HBaseMonitor {
    public void checkRegionServerHealth(String serverName) {
        // Check region distribution
        Admin admin = connection.getAdmin();
        List<RegionInfo> regions = admin.getRegions(ServerName.valueOf(serverName));
        
        System.out.println("Regions on " + serverName + ": " + regions.size());
        
        // Check request metrics
        for (RegionInfo region : regions) {
            RegionMetrics metrics = admin.getRegionMetrics(region.getRegionName());
            System.out.println("Region: " + region.getRegionNameAsString() +
                             ", Read requests: " + metrics.getReadRequestCount() +
                             ", Write requests: " + metrics.getWriteRequestCount());
        }
    }
    
    public void checkTableHealth(String tableName) throws IOException {
        TableName table = TableName.valueOf(tableName);
        
        // Check if table is enabled
        if (!admin.isTableEnabled(table)) {
            System.out.println("Table " + tableName + " is disabled");
            return;
        }
        
        // Check region distribution
        List<RegionInfo> regions = admin.getRegions(table);
        Map<ServerName, Integer> serverRegionCount = new HashMap<>();
        
        for (RegionInfo region : regions) {
            ServerName server = admin.getRegionLocation(region.getRegionName()).getServerName();
            serverRegionCount.merge(server, 1, Integer::sum);
        }
        
        // Report distribution
        serverRegionCount.forEach((server, count) -> 
            System.out.println("Server: " + server + ", Regions: " + count));
    }
}
```

### 10. How do you perform backup and disaster recovery for HBase?

**Answer:**
HBase provides multiple backup and recovery mechanisms for data protection.

**Backup Strategies:**
```bash
# 1. Export/Import utility
hbase org.apache.hadoop.hbase.mapreduce.Export table_name /backup/table_name

# Import from backup
hbase org.apache.hadoop.hbase.mapreduce.Import table_name /backup/table_name

# 2. Snapshot-based backup
hbase shell
> snapshot 'table_name', 'snapshot_name'
> list_snapshots

# Export snapshot to different cluster
hbase org.apache.hadoop.hbase.snapshot.ExportSnapshot \
  -snapshot snapshot_name \
  -copy-to hdfs://backup-cluster:9000/hbase

# 3. Replication for real-time backup
# Enable replication
> add_peer '1', 'backup-cluster:2181:/hbase'
> enable_table_replication 'table_name'
```

**Disaster Recovery:**
```bash
# Restore from snapshot
hbase shell
> disable 'table_name'
> restore_snapshot 'snapshot_name'
> enable 'table_name'

# Clone table from snapshot
> clone_snapshot 'snapshot_name', 'new_table_name'

# Point-in-time recovery using WAL
hbase org.apache.hadoop.hbase.mapreduce.WALPlayer \
  /hbase/WALs/regionserver,port,timestamp \
  table_name
```

**Automated Backup Script:**
```bash
#!/bin/bash
# hbase_backup.sh

TABLE_NAME=$1
BACKUP_DIR="/backup/hbase/$(date +%Y%m%d)"
SNAPSHOT_NAME="${TABLE_NAME}_$(date +%Y%m%d_%H%M%S)"

# Create snapshot
echo "Creating snapshot: $SNAPSHOT_NAME"
hbase shell << EOF
snapshot '$TABLE_NAME', '$SNAPSHOT_NAME'
exit
EOF

# Export snapshot
echo "Exporting snapshot to: $BACKUP_DIR"
hbase org.apache.hadoop.hbase.snapshot.ExportSnapshot \
  -snapshot $SNAPSHOT_NAME \
  -copy-to $BACKUP_DIR

# Cleanup old snapshots (keep last 7 days)
hbase shell << EOF
list_snapshots '$TABLE_NAME.*'
EOF

echo "Backup completed: $SNAPSHOT_NAME"
```

---

## Summary

Apache HBase provides scalable NoSQL database capabilities with:

1. **Distributed Architecture**: Horizontal scaling across commodity hardware
2. **Column-oriented Storage**: Efficient storage for sparse data
3. **Strong Consistency**: ACID properties for single-row operations
4. **Real-time Access**: Low-latency reads and writes
5. **Hadoop Integration**: Built on HDFS with ecosystem tool compatibility