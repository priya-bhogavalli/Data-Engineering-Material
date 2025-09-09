
### Q1: What is Apache HBase and what problems does it solve?
**Answer:**
Apache HBase is a distributed, scalable, NoSQL database built on top of Hadoop HDFS, modeled after Google's Bigtable.

**Key Problems Solved:**
- **Random Access**: Fast read/write access to large datasets
- **Scalability**: Horizontal scaling across commodity hardware
- **Real-time Queries**: Low-latency access to big data
- **Sparse Data**: Efficient storage of sparse datasets
- **Strong Consistency**: ACID properties for row-level operations

**Core Features:**
- Column-family data model
- Automatic sharding and load balancing
- Built-in versioning and timestamps
- Integration with Hadoop ecosystem
- Strong consistency guarantees

### Q2: Explain HBase data model and key concepts
**Answer:**
**HBase Data Model:**

```
Table
├── Row Key (Byte Array)
├── Column Family 1
│   ├── Column Qualifier 1 → Cell (Value + Timestamp)
│   └── Column Qualifier 2 → Cell (Value + Timestamp)
└── Column Family 2
    ├── Column Qualifier 1 → Cell (Value + Timestamp)
    └── Column Qualifier 2 → Cell (Value + Timestamp)
```

**Key Concepts:**

1. **Table**: Collection of rows
2. **Row Key**: Unique identifier for each row (byte array)
3. **Column Family**: Group of related columns
4. **Column Qualifier**: Specific column within family
5. **Cell**: Intersection of row and column (value + timestamp)
6. **Timestamp**: Version identifier for cell values

**Example:**
```java
// Table: user_profiles
// Row Key: user123
// Column Families: personal_info, preferences
// Columns: personal_info:name, personal_info:email, preferences:theme

Put put = new Put(Bytes.toBytes("user123"));
put.addColumn(Bytes.toBytes("personal_info"), Bytes.toBytes("name"), 
              Bytes.toBytes("John Doe"));
put.addColumn(Bytes.toBytes("personal_info"), Bytes.toBytes("email"), 
              Bytes.toBytes("john@example.com"));
put.addColumn(Bytes.toBytes("preferences"), Bytes.toBytes("theme"), 
              Bytes.toBytes("dark"));
```

### Q3: What are the differences between HBase and traditional RDBMS?
**Answer:**
**HBase vs RDBMS Comparison:**

| Aspect | HBase | RDBMS |
|--------|-------|-------|
| **Data Model** | Column-family, sparse | Relational, structured |
| **Schema** | Schema-less, flexible | Fixed schema |
| **ACID** | Row-level ACID | Full ACID compliance |
| **Scalability** | Horizontal scaling | Vertical scaling |
| **Joins** | No joins | Complex joins supported |
| **Indexes** | Row key only | Multiple indexes |
| **Consistency** | Strong consistency | ACID consistency |
| **Query Language** | API-based | SQL |

**When to Use HBase:**
- Large datasets (TB/PB scale)
- Sparse data with varying columns
- High write throughput requirements
- Real-time random access patterns
- Integration with Hadoop ecosystem

**When to Use RDBMS:**
- Complex queries with joins
- ACID transactions across tables
- Structured data with fixed schema
- Reporting and analytics
- Smaller datasets with complex relationships

---

## 🏗️ Architecture & Components

### Q4: Explain HBase architecture and its components
**Answer:**
**HBase Architecture:**

```
Client → ZooKeeper ← HMaster
  ↓         ↓         ↓
RegionServer ← → RegionServer ← → RegionServer
  ↓              ↓              ↓
HDFS         HDFS           HDFS
```

**Key Components:**

1. **HMaster**
   - Coordinates RegionServers
   - Handles table operations (create, delete, alter)
   - Load balancing and failover
   - Metadata management

2. **RegionServer**
   - Serves data for assigned regions
   - Handles read/write requests
   - Manages WAL (Write-Ahead Log)
   - Compaction and splitting

3. **ZooKeeper**
   - Coordinates distributed operations
   - Stores cluster metadata
   - Leader election for HMaster
   - RegionServer registration

4. **HDFS**
   - Underlying storage system
   - Stores HFiles and WAL
   - Provides fault tolerance

### Q5: What are HBase regions and how do they work?
**Answer:**
**HBase Regions:**

A region is a contiguous range of rows in a table, served by a single RegionServer.

**Region Characteristics:**
- Contains rows from start key to end key
- Default size: 10GB (configurable)
- Automatically split when size threshold reached
- Load balanced across RegionServers

**Region Lifecycle:**
```java
// 1. Table Creation
Admin admin = connection.getAdmin();
TableDescriptor tableDesc = TableDescriptorBuilder.newBuilder(TableName.valueOf("users"))
    .setColumnFamily(ColumnFamilyDescriptorBuilder.of("info"))
    .build();
admin.createTable(tableDesc);

// 2. Region Assignment
// HMaster assigns regions to RegionServers

// 3. Region Splitting (automatic)
// When region exceeds size threshold:
// Region [startKey, endKey) → [startKey, splitKey) + [splitKey, endKey)

// 4. Load Balancing
admin.balancer(); // Manual trigger
```

**Region Management:**
```bash
# View region information
hbase shell
> list_regions 'users'
> major_compact 'users'
> split 'users', 'row_key_split_point'
```

### Q6: Explain HBase read and write paths
**Answer:**
**HBase Write Path:**

1. **Client Request**: Client sends Put request
2. **WAL Write**: Write to Write-Ahead Log first
3. **MemStore**: Data written to in-memory store
4. **Acknowledgment**: Success returned to client
5. **Flush**: MemStore flushed to HFile when full
6. **Compaction**: HFiles merged periodically

```java
// Write operation
Put put = new Put(Bytes.toBytes("row1"));
put.addColumn(Bytes.toBytes("cf"), Bytes.toBytes("col"), Bytes.toBytes("value"));
table.put(put);

// Write path: Client → WAL → MemStore → HFile
```

**HBase Read Path:**

1. **Client Request**: Client sends Get/Scan request
2. **Block Cache**: Check in-memory cache first
3. **MemStore**: Check current in-memory data
4. **HFiles**: Read from disk files if needed
5. **Merge Results**: Combine data from multiple sources
6. **Return**: Send result to client

```java
// Read operation
Get get = new Get(Bytes.toBytes("row1"));
Result result = table.get(get);

// Read path: Client → Block Cache → MemStore → HFiles
```

**Optimization Strategies:**
- **Bloom Filters**: Skip HFiles that don't contain row
- **Block Cache**: Cache frequently accessed blocks
- **Compression**: Reduce I/O with compression
- **Prefetching**: Read ahead for sequential scans

---

## 📊 Data Model & Operations

### Q7: How do you design an effective row key in HBase?
**Answer:**
**Row Key Design Principles:**

1. **Avoid Hotspotting**
```java
// Bad: Sequential keys cause hotspotting
String badRowKey = timestamp + "_" + userId; // All writes go to one region

// Good: Distribute writes across regions
String goodRowKey = userId + "_" + timestamp; // Distributes by user
String saltedRowKey = (userId.hashCode() % 100) + "_" + userId + "_" + timestamp;
```

2. **Optimize for Access Patterns**
```java
// Time-series data with reverse timestamp
long reverseTimestamp = Long.MAX_VALUE - System.currentTimeMillis();
String timeSeriesKey = deviceId + "_" + reverseTimestamp;

// Hierarchical data
String hierarchicalKey = country + "_" + state + "_" + city + "_" + userId;
```

3. **Keep Keys Short**
```java
// Bad: Long descriptive keys
String longKey = "user_profile_personal_information_" + userId;

// Good: Short, efficient keys
String shortKey = "up_" + userId; // Use abbreviations
```

**Row Key Patterns:**

1. **Salting**: Add random prefix to distribute load
2. **Field Promotion**: Move discriminating fields to front
3. **Reverse Timestamp**: For time-series data
4. **Composite Keys**: Combine multiple fields

### Q8: Explain HBase CRUD operations with examples
**Answer:**
**HBase CRUD Operations:**

**1. Create (Put):**
```java
// Single put
Put put = new Put(Bytes.toBytes("row1"));
put.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col1"), Bytes.toBytes("value1"));
put.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col2"), Bytes.toBytes("value2"));
table.put(put);

// Batch puts
List<Put> puts = new ArrayList<>();
for (int i = 0; i < 1000; i++) {
    Put batchPut = new Put(Bytes.toBytes("row" + i));
    batchPut.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("data"), 
                      Bytes.toBytes("value" + i));
    puts.add(batchPut);
}
table.put(puts);
```

**2. Read (Get/Scan):**
```java
// Single get
Get get = new Get(Bytes.toBytes("row1"));
get.addFamily(Bytes.toBytes("cf1")); // Specify column family
Result result = table.get(get);

// Extract values
byte[] value = result.getValue(Bytes.toBytes("cf1"), Bytes.toBytes("col1"));
String stringValue = Bytes.toString(value);

// Scan range
Scan scan = new Scan();
scan.setStartRow(Bytes.toBytes("row1"));
scan.setStopRow(Bytes.toBytes("row100"));
scan.addFamily(Bytes.toBytes("cf1"));

ResultScanner scanner = table.getScanner(scan);
for (Result r : scanner) {
    // Process each result
    String rowKey = Bytes.toString(r.getRow());
    // Extract column values
}
scanner.close();
```

**3. Update (Put with existing row key):**
```java
// Update existing row
Put update = new Put(Bytes.toBytes("row1"));
update.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col1"), 
                Bytes.toBytes("updated_value"));
table.put(update);

// Conditional update
Put conditionalPut = new Put(Bytes.toBytes("row1"));
conditionalPut.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col1"), 
                        Bytes.toBytes("new_value"));

boolean success = table.checkAndPut(Bytes.toBytes("row1"), 
    Bytes.toBytes("cf1"), Bytes.toBytes("col1"), 
    Bytes.toBytes("old_value"), conditionalPut);
```

**4. Delete:**
```java
// Delete entire row
Delete delete = new Delete(Bytes.toBytes("row1"));
table.delete(delete);

// Delete specific column
Delete columnDelete = new Delete(Bytes.toBytes("row1"));
columnDelete.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col1"));
table.delete(columnDelete);

// Delete column family
Delete familyDelete = new Delete(Bytes.toBytes("row1"));
familyDelete.addFamily(Bytes.toBytes("cf1"));
table.delete(familyDelete);

// Conditional delete
boolean deleted = table.checkAndDelete(Bytes.toBytes("row1"), 
    Bytes.toBytes("cf1"), Bytes.toBytes("col1"), 
    Bytes.toBytes("expected_value"), delete);
```

### Q9: How do you handle versioning in HBase?
**Answer:**
**HBase Versioning:**

**1. Version Configuration:**
```java
// Set max versions for column family
ColumnFamilyDescriptor cfDesc = ColumnFamilyDescriptorBuilder
    .newBuilder(Bytes.toBytes("cf1"))
    .setMaxVersions(5) // Keep 5 versions
    .setMinVersions(1) // Keep at least 1 version
    .setTimeToLive(86400) // TTL in seconds (24 hours)
    .build();
```

**2. Writing Versions:**
```java
// Write with automatic timestamp
Put put1 = new Put(Bytes.toBytes("row1"));
put1.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col1"), 
              Bytes.toBytes("version1"));
table.put(put1);

Thread.sleep(1000); // Wait 1 second

// Write another version
Put put2 = new Put(Bytes.toBytes("row1"));
put2.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col1"), 
              Bytes.toBytes("version2"));
table.put(put2);

// Write with explicit timestamp
Put put3 = new Put(Bytes.toBytes("row1"));
put3.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col1"), 
              1640995200000L, Bytes.toBytes("specific_time_version"));
table.put(put3);
```

**3. Reading Versions:**
```java
// Get latest version (default)
Get get = new Get(Bytes.toBytes("row1"));
Result result = table.get(get);

// Get all versions
Get getAllVersions = new Get(Bytes.toBytes("row1"));
getAllVersions.setMaxVersions(); // Get all versions
Result allVersionsResult = table.get(getAllVersions);

// Iterate through versions
NavigableMap<byte[], NavigableMap<Long, byte[]>> familyMap = 
    allVersionsResult.getMap().get(Bytes.toBytes("cf1"));
NavigableMap<Long, byte[]> columnMap = familyMap.get(Bytes.toBytes("col1"));

for (Map.Entry<Long, byte[]> entry : columnMap.entrySet()) {
    long timestamp = entry.getKey();
    String value = Bytes.toString(entry.getValue());
    System.out.println("Timestamp: " + timestamp + ", Value: " + value);
}

// Get specific version
Get getSpecificVersion = new Get(Bytes.toBytes("row1"));
getSpecificVersion.setTimeStamp(1640995200000L);
Result specificResult = table.get(getSpecificVersion);
```

---

## ⚡ Performance & Optimization

### Q10: What are HBase performance optimization techniques?
**Answer:**
**HBase Performance Optimization:**

**1. Table Design Optimization:**
```java
// Optimize column families
TableDescriptor tableDesc = TableDescriptorBuilder
    .newBuilder(TableName.valueOf("optimized_table"))
    .setColumnFamily(ColumnFamilyDescriptorBuilder
        .newBuilder(Bytes.toBytes("cf1"))
        .setCompressionType(Compression.Algorithm.SNAPPY) // Enable compression
        .setBloomFilterType(BloomType.ROW) // Enable bloom filters
        .setBlockCacheEnabled(true) // Enable block cache
        .setBlocksize(65536) // Optimize block size
        .build())
    .build();
```

**2. Batch Operations:**
```java
// Batch puts for better throughput
List<Put> puts = new ArrayList<>();
for (int i = 0; i < 10000; i++) {
    Put put = new Put(Bytes.toBytes("row" + i));
    put.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("data"), 
                 Bytes.toBytes("value" + i));
    puts.add(put);
    
    // Batch every 1000 operations
    if (puts.size() == 1000) {
        table.put(puts);
        puts.clear();
    }
}
if (!puts.isEmpty()) {
    table.put(puts);
}
```

**3. Scan Optimization:**
```java
// Optimized scan
Scan scan = new Scan();
scan.setCaching(1000); // Cache 1000 rows
scan.setBatch(100); // Batch size for columns
scan.addFamily(Bytes.toBytes("cf1")); // Specify column family
scan.setFilter(new PageFilter(10000)); // Limit results

// Use filters to reduce data transfer
FilterList filterList = new FilterList(FilterList.Operator.MUST_PASS_ALL);
filterList.addFilter(new SingleColumnValueFilter(
    Bytes.toBytes("cf1"), Bytes.toBytes("status"), 
    CompareOperator.EQUAL, Bytes.toBytes("active")));
filterList.addFilter(new PrefixFilter(Bytes.toBytes("user_")));
scan.setFilter(filterList);
```

**4. Connection Management:**
```java
// Use connection pooling
Configuration config = HBaseConfiguration.create();
config.set("hbase.zookeeper.quorum", "zk1,zk2,zk3");
config.setInt("hbase.client.scanner.caching", 1000);
config.setInt("hbase.client.write.buffer", 2097152); // 2MB buffer

Connection connection = ConnectionFactory.createConnection(config);
// Reuse connection across operations
Table table = connection.getTable(TableName.valueOf("my_table"));
```

### Q11: Explain HBase compaction process
**Answer:**
**HBase Compaction:**

**Types of Compaction:**

1. **Minor Compaction**
   - Merges small HFiles into larger ones
   - Removes deleted cells and expired TTL data
   - Runs automatically based on configuration

2. **Major Compaction**
   - Merges all HFiles in a region
   - Removes all deleted and expired data
   - Rewrites all data (I/O intensive)

**Compaction Configuration:**
```xml
<!-- hbase-site.xml -->
<property>
    <name>hbase.hstore.compaction.min</name>
    <value>3</value> <!-- Minimum files for minor compaction -->
</property>

<property>
    <name>hbase.hstore.compaction.max</name>
    <value>10</value> <!-- Maximum files for minor compaction -->
</property>

<property>
    <name>hbase.hregion.majorcompaction</name>
    <value>604800000</value> <!-- Major compaction interval (7 days) -->
</property>
```

**Manual Compaction:**
```bash
# HBase shell commands
major_compact 'table_name'
compact 'table_name'
major_compact 'table_name', 'column_family'

# Specific region compaction
major_compact 'table_name,start_key,region_id'
```

**Compaction Monitoring:**
```java
// Monitor compaction via JMX or Admin API
Admin admin = connection.getAdmin();
CompactionState state = admin.getCompactionState(TableName.valueOf("my_table"));
System.out.println("Compaction state: " + state);
```

### Q12: How do you handle HBase hotspotting?
**Answer:**
**HBase Hotspotting Solutions:**

**1. Row Key Design:**
```java
// Problem: Sequential keys
String hotspotKey = timestamp + "_" + userId; // All recent data in one region

// Solution 1: Salting
String saltedKey = (userId.hashCode() % 100) + "_" + userId + "_" + timestamp;

// Solution 2: Reverse timestamp
long reverseTimestamp = Long.MAX_VALUE - System.currentTimeMillis();
String reversedKey = userId + "_" + reverseTimestamp;

// Solution 3: Hash prefix
String hashedKey = MD5Hash.digest(userId).toString().substring(0, 8) + "_" + userId;
```

**2. Pre-splitting Tables:**
```java
// Create table with pre-defined splits
byte[][] splits = new byte[10][];
for (int i = 0; i < 10; i++) {
    splits[i] = Bytes.toBytes(String.format("%02d", i));
}

TableDescriptor tableDesc = TableDescriptorBuilder
    .newBuilder(TableName.valueOf("pre_split_table"))
    .setColumnFamily(ColumnFamilyDescriptorBuilder.of("cf1"))
    .build();

admin.createTable(tableDesc, splits);
```

**3. Load Balancing:**
```bash
# Manual load balancing
hbase shell
> balance_switch true
> balancer

# Move specific region
> move 'region_name', 'target_server'
```

**4. Monitoring Hotspots:**
```java
// Monitor region load
ClusterMetrics metrics = admin.getClusterMetrics();
for (ServerMetrics serverMetrics : metrics.getLiveServerMetrics().values()) {
    System.out.println("Server: " + serverMetrics.getServerName());
    System.out.println("Request count: " + serverMetrics.getRequestCount());
    System.out.println("Region count: " + serverMetrics.getRegionMetrics().size());
}
```

---

## 🔒 Security & Administration

### Q13: How do you implement security in HBase?
**Answer:**
**HBase Security Implementation:**

**1. Authentication:**
```xml
<!-- hbase-site.xml -->
<property>
    <name>hbase.security.authentication</name>
    <value>kerberos</value>
</property>

<property>
    <name>hbase.security.authorization</name>
    <value>true</value>
</property>

<property>
    <name>hbase.master.kerberos.principal</name>
    <value>hbase/_HOST@REALM.COM</value>
</property>
```

**2. Authorization:**
```bash
# Grant permissions
hbase shell
> grant 'user1', 'RW', 'table1'
> grant 'user2', 'R', 'table1', 'cf1'
> grant 'admin_group', 'RWXCA', 'table1'

# Revoke permissions
> revoke 'user1', 'table1'

# List permissions
> user_permission 'table1'
```

**3. Cell-level Security:**
```java
// Set cell visibility
Put put = new Put(Bytes.toBytes("row1"));
put.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("sensitive_data"), 
             Bytes.toBytes("secret_value"));
put.setCellVisibility(new CellVisibility("SECRET"));
table.put(put);

// Read with authorizations
Scan scan = new Scan();
scan.setAuthorizations(new Authorizations("SECRET", "PUBLIC"));
ResultScanner scanner = table.getScanner(scan);
```

**4. Encryption:**
```xml
<!-- Enable encryption at rest -->
<property>
    <name>hbase.crypto.keyprovider</name>
    <value>org.apache.hadoop.crypto.key.JavaKeyStoreProvider</value>
</property>

<property>
    <name>hbase.crypto.keyprovider.parameters</name>
    <value>jceks://file/path/to/keystore.jceks</value>
</property>
```

### Q14: How do you backup and restore HBase data?
**Answer:**
**HBase Backup and Restore:**

**1. Export/Import:**
```bash
# Export table data
hbase org.apache.hadoop.hbase.mapreduce.Export \
  table_name /backup/table_name_export

# Import table data
hbase org.apache.hadoop.hbase.mapreduce.Import \
  table_name /backup/table_name_export
```

**2. Snapshot-based Backup:**
```bash
# Create snapshot
hbase shell
> snapshot 'table_name', 'snapshot_name'

# List snapshots
> list_snapshots

# Clone from snapshot
> clone_snapshot 'snapshot_name', 'new_table_name'

# Restore from snapshot
> disable 'table_name'
> restore_snapshot 'snapshot_name'
> enable 'table_name'

# Export snapshot to another cluster
hbase org.apache.hadoop.hbase.snapshot.ExportSnapshot \
  -snapshot snapshot_name \
  -copy-to hdfs://remote-cluster/backup/
```

**3. Incremental Backup:**
```bash
# Enable replication for incremental backup
hbase shell
> add_peer '1', 'zk1,zk2,zk3:2181:/hbase'
> enable_table_replication 'table_name'

# Monitor replication lag
> status 'replication'
```

**4. Automated Backup Script:**
```bash
#!/bin/bash
# hbase-backup.sh
TABLE_NAME=$1
BACKUP_DIR="/backup/hbase/$(date +%Y%m%d)"

# Create backup directory
hdfs dfs -mkdir -p $BACKUP_DIR

# Create snapshot
echo "snapshot '$TABLE_NAME', '${TABLE_NAME}_$(date +%Y%m%d_%H%M%S)'" | hbase shell

# Export snapshot
hbase org.apache.hadoop.hbase.snapshot.ExportSnapshot \
  -snapshot ${TABLE_NAME}_$(date +%Y%m%d_%H%M%S) \
  -copy-to $BACKUP_DIR

echo "Backup completed: $BACKUP_DIR"
```

---

## 🔗 Integration & Use Cases

### Q15: How does HBase integrate with other Hadoop ecosystem tools?
**Answer:**
**HBase Integration:**

**1. Spark Integration:**
```scala
// Spark-HBase connector
import org.apache.spark.sql.SparkSession
import org.apache.hadoop.hbase.spark.HBaseContext

val spark = SparkSession.builder().appName("HBase-Spark").getOrCreate()
val hbaseContext = new HBaseContext(spark.sparkContext, hbaseConfig)

// Read from HBase
val hbaseRDD = hbaseContext.hbaseRDD(TableName.valueOf("my_table"), scan)

// Write to HBase
val putRDD = spark.sparkContext.parallelize(puts)
hbaseContext.bulkPut(putRDD, TableName.valueOf("my_table"), putFunction)
```

**2. Hive Integration:**
```sql
-- Create external Hive table backed by HBase
CREATE EXTERNAL TABLE hive_hbase_table (
    key string,
    name string,
    email string
)
STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
WITH SERDEPROPERTIES (
    "hbase.columns.mapping" = ":key,cf1:name,cf1:email"
)
TBLPROPERTIES ("hbase.table.name" = "hbase_table");

-- Query HBase data via Hive
SELECT * FROM hive_hbase_table WHERE key LIKE 'user%';
```

**3. Phoenix Integration:**
```sql
-- Create Phoenix view over HBase table
CREATE VIEW "my_table" (
    pk VARCHAR PRIMARY KEY,
    "cf1"."name" VARCHAR,
    "cf1"."email" VARCHAR
);

-- SQL queries on HBase
SELECT * FROM "my_table" WHERE pk = 'user123';
CREATE INDEX idx_email ON "my_table"("cf1"."email");
```

**4. MapReduce Integration:**
```java
// MapReduce job reading from HBase
public class HBaseMapReduceJob {
    public static void main(String[] args) throws Exception {
        Configuration conf = HBaseConfiguration.create();
        Job job = Job.getInstance(conf, "hbase-mapreduce");
        
        Scan scan = new Scan();
        scan.addFamily(Bytes.toBytes("cf1"));
        
        TableMapReduceUtil.initTableMapperJob(
            "source_table", scan, MyMapper.class, 
            Text.class, IntWritable.class, job);
            
        TableMapReduceUtil.initTableReducerJob(
            "target_table", MyReducer.class, job);
            
        job.waitForCompletion(true);
    }
}
```

### Q16: Design a real-time analytics system using HBase
**Answer:**
**Real-time Analytics System Design:**

**1. Data Model:**
```java
// Time-series data table
// Row Key: metric_name + reverse_timestamp + server_id
// Column Family: data (value, tags, metadata)

public class MetricsRowKey {
    public static String buildRowKey(String metric, long timestamp, String serverId) {
        long reverseTimestamp = Long.MAX_VALUE - timestamp;
        return metric + "_" + String.format("%019d", reverseTimestamp) + "_" + serverId;
    }
}

// User activity table  
// Row Key: user_id + reverse_timestamp
// Column Families: events, profile, aggregates

public class UserActivityRowKey {
    public static String buildRowKey(String userId, long timestamp) {
        long reverseTimestamp = Long.MAX_VALUE - timestamp;
        return userId + "_" + String.format("%019d", reverseTimestamp);
    }
}
```

**2. Real-time Ingestion:**
```java
public class RealTimeIngestionService {
    private Connection hbaseConnection;
    private Table metricsTable;
    private Table userActivityTable;
    
    public void ingestMetric(String metric, double value, String serverId, Map<String, String> tags) {
        long timestamp = System.currentTimeMillis();
        String rowKey = MetricsRowKey.buildRowKey(metric, timestamp, serverId);
        
        Put put = new Put(Bytes.toBytes(rowKey));
        put.addColumn(Bytes.toBytes("data"), Bytes.toBytes("value"), 
                     Bytes.toBytes(Double.toString(value)));
        put.addColumn(Bytes.toBytes("data"), Bytes.toBytes("timestamp"), 
                     Bytes.toBytes(Long.toString(timestamp)));
        
        // Add tags
        for (Map.Entry<String, String> tag : tags.entrySet()) {
            put.addColumn(Bytes.toBytes("data"), Bytes.toBytes("tag_" + tag.getKey()), 
                         Bytes.toBytes(tag.getValue()));
        }
        
        try {
            metricsTable.put(put);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    public void ingestUserEvent(String userId, String eventType, Map<String, Object> eventData) {
        long timestamp = System.currentTimeMillis();
        String rowKey = UserActivityRowKey.buildRowKey(userId, timestamp);
        
        Put put = new Put(Bytes.toBytes(rowKey));
        put.addColumn(Bytes.toBytes("events"), Bytes.toBytes("type"), 
                     Bytes.toBytes(eventType));
        put.addColumn(Bytes.toBytes("events"), Bytes.toBytes("timestamp"), 
                     Bytes.toBytes(Long.toString(timestamp)));
        
        // Add event data
        for (Map.Entry<String, Object> entry : eventData.entrySet()) {
            put.addColumn(Bytes.toBytes("events"), Bytes.toBytes(entry.getKey()), 
                         Bytes.toBytes(entry.getValue().toString()));
        }
        
        try {
            userActivityTable.put(put);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

**3. Real-time Queries:**
```java
public class RealTimeQueryService {
    private Connection hbaseConnection;
    
    public List<MetricPoint> getMetricHistory(String metric, String serverId, 
                                            long startTime, long endTime) throws IOException {
        Table table = hbaseConnection.getTable(TableName.valueOf("metrics"));
        
        // Build scan range
        long reverseEndTime = Long.MAX_VALUE - endTime;
        long reverseStartTime = Long.MAX_VALUE - startTime;
        
        String startRowKey = metric + "_" + String.format("%019d", reverseEndTime) + "_" + serverId;
        String endRowKey = metric + "_" + String.format("%019d", reverseStartTime) + "_" + serverId;
        
        Scan scan = new Scan();
        scan.setStartRow(Bytes.toBytes(startRowKey));
        scan.setStopRow(Bytes.toBytes(endRowKey));
        scan.addFamily(Bytes.toBytes("data"));
        
        List<MetricPoint> points = new ArrayList<>();
        ResultScanner scanner = table.getScanner(scan);
        
        for (Result result : scanner) {
            String value = Bytes.toString(result.getValue(Bytes.toBytes("data"), Bytes.toBytes("value")));
            String timestamp = Bytes.toString(result.getValue(Bytes.toBytes("data"), Bytes.toBytes("timestamp")));
            
            points.add(new MetricPoint(Long.parseLong(timestamp), Double.parseDouble(value)));
        }
        
        scanner.close();
        return points;
    }
    
    public List<UserEvent> getUserActivity(String userId, long startTime, long endTime) throws IOException {
        Table table = hbaseConnection.getTable(TableName.valueOf("user_activity"));
        
        long reverseEndTime = Long.MAX_VALUE - endTime;
        long reverseStartTime = Long.MAX_VALUE - startTime;
        
        String startRowKey = userId + "_" + String.format("%019d", reverseEndTime);
        String endRowKey = userId + "_" + String.format("%019d", reverseStartTime);
        
        Scan scan = new Scan();
        scan.setStartRow(Bytes.toBytes(startRowKey));
        scan.setStopRow(Bytes.toBytes(endRowKey));
        scan.addFamily(Bytes.toBytes("events"));
        
        List<UserEvent> events = new ArrayList<>();
        ResultScanner scanner = table.getScanner(scan);
        
        for (Result result : scanner) {
            String eventType = Bytes.toString(result.getValue(Bytes.toBytes("events"), Bytes.toBytes("type")));
            String timestamp = Bytes.toString(result.getValue(Bytes.toBytes("events"), Bytes.toBytes("timestamp")));
            
            UserEvent event = new UserEvent(eventType, Long.parseLong(timestamp));
            
            // Extract additional event data
            NavigableMap<byte[], byte[]> familyMap = result.getFamilyMap(Bytes.toBytes("events"));
            for (Map.Entry<byte[], byte[]> entry : familyMap.entrySet()) {
                String qualifier = Bytes.toString(entry.getKey());
                if (!qualifier.equals("type") && !qualifier.equals("timestamp")) {
                    event.addProperty(qualifier, Bytes.toString(entry.getValue()));
                }
            }
            
            events.add(event);
        }
        
        scanner.close();
        return events;
    }
}
```

---

## 🔧 Troubleshooting

### Q17: What are common HBase issues and how do you resolve them?
**Answer:**
**Common HBase Issues:**

**1. RegionServer Crashes:**
```bash
# Check RegionServer logs
tail -f /var/log/hbase/hbase-hbase-regionserver-*.log

# Common causes and solutions:
# - OutOfMemoryError: Increase heap size
export HBASE_HEAPSIZE=8G

# - Too many regions: Increase region size
hbase.hregion.max.filesize=10737418240  # 10GB

# - GC issues: Tune GC settings
export HBASE_OPTS="-XX:+UseG1GC -XX:MaxGCPauseMillis=200"
```

**2. Slow Queries:**
```java
// Enable query logging
Configuration conf = HBaseConfiguration.create();
conf.setBoolean("hbase.regionserver.slowlog.buffer.enabled", true);
conf.setLong("hbase.regionserver.slowlog.slowquery.threshold", 1000); // 1 second

// Optimize scans
Scan scan = new Scan();
scan.setCaching(1000); // Increase caching
scan.setBatch(100); // Set batch size
scan.addFamily(Bytes.toBytes("cf1")); // Specify column family
scan.setFilter(new PageFilter(10000)); // Limit results
```

**3. Region Hotspotting:**
```bash
# Identify hot regions
hbase shell
> status 'detailed'

# Manual region splitting
> split 'table_name', 'split_point'

# Load balancing
> balancer
```

**4. Compaction Issues:**
```bash
# Monitor compaction queue
echo "dump" | nc regionserver_host 16030 | grep -i compact

# Manual compaction
hbase shell
> major_compact 'table_name'

# Disable automatic major compaction during peak hours
> alter 'table_name', {NAME => 'cf1', CONFIGURATION => {'MAJOR_COMPACTION_PERIOD' => '0'}}
```

### Q18: How do you monitor HBase cluster health?
**Answer:**
**HBase Monitoring:**

**1. Web UI Monitoring:**
```bash
# HMaster Web UI
http://hmaster_host:16010

# RegionServer Web UI  
http://regionserver_host:16030

# Key metrics to monitor:
# - Region count per server
# - Request rate and latency
# - Compaction queue size
# - Block cache hit ratio
```

**2. JMX Metrics:**
```java
// Enable JMX
-Dcom.sun.management.jmxremote
-Dcom.sun.management.jmxremote.port=10102
-Dcom.sun.management.jmxremote.authenticate=false
-Dcom.sun.management.jmxremote.ssl=false

// Key JMX metrics:
// Hadoop:service=HBase,name=RegionServer,sub=Server
// - readRequestCount, writeRequestCount
// - blockCacheHitPercent, blockCacheCountHitPercent
// - compactionQueueLength, flushQueueLength
```

**3. Command Line Monitoring:**
```bash
# HBase shell status
hbase shell
> status
> status 'detailed'
> status 'simple'

# Table statistics
> describe 'table_name'
> count 'table_name'

# Region information
> list_regions 'table_name'
```

**4. Custom Monitoring Script:**
```bash
#!/bin/bash
# hbase-health-check.sh

# Check HMaster
HMASTER_STATUS=$(curl -s http://hmaster:16010/master-status | grep -c "Master is initializing")
if [ $HMASTER_STATUS -gt 0 ]; then
    echo "WARNING: HMaster is initializing"
fi

# Check RegionServers
DEAD_SERVERS=$(curl -s http://hmaster:16010/master-status | grep -o "Dead RegionServers: [0-9]*" | cut -d: -f2 | tr -d ' ')
if [ $DEAD_SERVERS -gt 0 ]; then
    echo "CRITICAL: $DEAD_SERVERS dead RegionServers"
fi

# Check table availability
echo "list" | hbase shell -n 2>/dev/null | grep -q "TABLE"
if [ $? -eq 0 ]; then
    echo "OK: HBase is responding"
else
    echo "CRITICAL: HBase is not responding"
fi
```

---

## 🌟 Real-world Scenarios

### Q19: Design an IoT data storage system using HBase
**Answer:**
**IoT Data Storage System:**

**1. Data Model Design:**
```java
// Device telemetry table
// Row Key: device_id + reverse_timestamp
// Column Families: sensors, status, location

public class IoTDataModel {
    public static String buildTelemetryRowKey(String deviceId, long timestamp) {
        long reverseTimestamp = Long.MAX_VALUE - timestamp;
        return deviceId + "_" + String.format("%019d", reverseTimestamp);
    }
    
    // Device metadata table
    // Row Key: device_id
    // Column Families: info, config, maintenance
    
    // Aggregated data table (hourly/daily rollups)
    // Row Key: device_id + time_bucket
    // Column Families: hourly_stats, daily_stats
    
    public static String buildAggregateRowKey(String deviceId, String timeBucket) {
        return deviceId + "_" + timeBucket; // e.g., "device123_2023120115" for hourly
    }
}
```

**2. Data Ingestion Service:**
```java
public class IoTDataIngestionService {
    private Connection hbaseConnection;
    private Table telemetryTable;
    private Table deviceTable;
    private Table aggregateTable;
    
    public void ingestTelemetryData(String deviceId, Map<String, Double> sensorData, 
                                   Location location, DeviceStatus status) throws IOException {
        long timestamp = System.currentTimeMillis();
        String rowKey = IoTDataModel.buildTelemetryRowKey(deviceId, timestamp);
        
        Put put = new Put(Bytes.toBytes(rowKey));
        
        // Store sensor data
        for (Map.Entry<String, Double> sensor : sensorData.entrySet()) {
            put.addColumn(Bytes.toBytes("sensors"), Bytes.toBytes(sensor.getKey()), 
                         Bytes.toBytes(sensor.getValue().toString()));
        }
        
        // Store location
        put.addColumn(Bytes.toBytes("location"), Bytes.toBytes("latitude"), 
                     Bytes.toBytes(Double.toString(location.getLatitude())));
        put.addColumn(Bytes.toBytes("location"), Bytes.toBytes("longitude"), 
                     Bytes.toBytes(Double.toString(location.getLongitude())));
        
        // Store status
        put.addColumn(Bytes.toBytes("status"), Bytes.toBytes("battery_level"), 
                     Bytes.toBytes(Integer.toString(status.getBatteryLevel())));
        put.addColumn(Bytes.toBytes("status"), Bytes.toBytes("signal_strength"), 
                     Bytes.toBytes(Integer.toString(status.getSignalStrength())));
        
        telemetryTable.put(put);
        
        // Update device last seen
        updateDeviceLastSeen(deviceId, timestamp);
        
        // Trigger aggregation (async)
        triggerAggregation(deviceId, timestamp, sensorData);
    }
    
    private void updateDeviceLastSeen(String deviceId, long timestamp) throws IOException {
        Put put = new Put(Bytes.toBytes(deviceId));
        put.addColumn(Bytes.toBytes("info"), Bytes.toBytes("last_seen"), 
                     Bytes.toBytes(Long.toString(timestamp)));
        deviceTable.put(put);
    }
    
    private void triggerAggregation(String deviceId, long timestamp, Map<String, Double> sensorData) {
        // Implement hourly/daily aggregation logic
        CompletableFuture.runAsync(() -> {
            try {
                aggregateHourlyData(deviceId, timestamp, sensorData);
            } catch (IOException e) {
                e.printStackTrace();
            }
        });
    }
}
```

**3. Query Service:**
```java
public class IoTQueryService {
    private Connection hbaseConnection;
    
    public List<TelemetryReading> getDeviceTelemetry(String deviceId, long startTime, long endTime) 
            throws IOException {
        Table table = hbaseConnection.getTable(TableName.valueOf("device_telemetry"));
        
        long reverseEndTime = Long.MAX_VALUE - endTime;
        long reverseStartTime = Long.MAX_VALUE - startTime;
        
        String startRowKey = deviceId + "_" + String.format("%019d", reverseEndTime);
        String endRowKey = deviceId + "_" + String.format("%019d", reverseStartTime);
        
        Scan scan = new Scan();
        scan.setStartRow(Bytes.toBytes(startRowKey));
        scan.setStopRow(Bytes.toBytes(endRowKey));
        scan.setCaching(1000);
        
        List<TelemetryReading> readings = new ArrayList<>();
        ResultScanner scanner = table.getScanner(scan);
        
        for (Result result : scanner) {
            TelemetryReading reading = new TelemetryReading();
            reading.setDeviceId(deviceId);
            
            // Extract timestamp from row key
            String rowKey = Bytes.toString(result.getRow());
            long reverseTimestamp = Long.parseLong(rowKey.split("_")[1]);
            reading.setTimestamp(Long.MAX_VALUE - reverseTimestamp);
            
            // Extract sensor data
            NavigableMap<byte[], byte[]> sensorMap = result.getFamilyMap(Bytes.toBytes("sensors"));
            Map<String, Double> sensors = new HashMap<>();
            for (Map.Entry<byte[], byte[]> entry : sensorMap.entrySet()) {
                String sensorName = Bytes.toString(entry.getKey());
                Double sensorValue = Double.parseDouble(Bytes.toString(entry.getValue()));
                sensors.put(sensorName, sensorValue);
            }
            reading.setSensorData(sensors);
            
            readings.add(reading);
        }
        
        scanner.close();
        return readings;
    }
    
    public DeviceStats getDeviceStats(String deviceId, String timeBucket) throws IOException {
        Table table = hbaseConnection.getTable(TableName.valueOf("device_aggregates"));
        
        String rowKey = IoTDataModel.buildAggregateRowKey(deviceId, timeBucket);
        Get get = new Get(Bytes.toBytes(rowKey));
        Result result = table.get(get);
        
        if (result.isEmpty()) {
            return null;
        }
        
        DeviceStats stats = new DeviceStats();
        stats.setDeviceId(deviceId);
        stats.setTimeBucket(timeBucket);
        
        // Extract aggregated statistics
        NavigableMap<byte[], byte[]> statsMap = result.getFamilyMap(Bytes.toBytes("hourly_stats"));
        for (Map.Entry<byte[], byte[]> entry : statsMap.entrySet()) {
            String statName = Bytes.toString(entry.getKey());
            String statValue = Bytes.toString(entry.getValue());
            stats.addStat(statName, statValue);
        }
        
        return stats;
    }
}
```

### Q20: Implement a social media feed system using HBase
**Answer:**
**Social Media Feed System:**

**1. Data Model:**
```java
// User posts table
// Row Key: user_id + reverse_timestamp + post_id
// Column Families: content, metadata, engagement

// User timeline table (fan-out on write)
// Row Key: user_id + reverse_timestamp + original_post_id
// Column Families: post_data, author_info

// User followers table
// Row Key: user_id
// Column Family: followers (follower_id -> timestamp)

// User following table  
// Row Key: user_id
// Column Family: following (following_id -> timestamp)

public class SocialMediaDataModel {
    public static String buildPostRowKey(String userId, long timestamp, String postId) {
        long reverseTimestamp = Long.MAX_VALUE - timestamp;
        return userId + "_" + String.format("%019d", reverseTimestamp) + "_" + postId;
    }
    
    public static String buildTimelineRowKey(String userId, long timestamp, String originalPostId) {
        long reverseTimestamp = Long.MAX_VALUE - timestamp;
        return userId + "_" + String.format("%019d", reverseTimestamp) + "_" + originalPostId;
    }
}
```

**2. Post Publishing Service:**
```java
public class PostPublishingService {
    private Connection hbaseConnection;
    private Table postsTable;
    private Table timelineTable;
    private Table followersTable;
    
    public void publishPost(String userId, String content, List<String> mediaUrls, 
                           List<String> hashtags) throws IOException {
        String postId = UUID.randomUUID().toString();
        long timestamp = System.currentTimeMillis();
        
        // Store original post
        storePost(userId, postId, timestamp, content, mediaUrls, hashtags);
        
        // Fan-out to followers' timelines
        fanOutToFollowers(userId, postId, timestamp, content, mediaUrls, hashtags);
    }
    
    private void storePost(String userId, String postId, long timestamp, String content, 
                          List<String> mediaUrls, List<String> hashtags) throws IOException {
        String rowKey = SocialMediaDataModel.buildPostRowKey(userId, timestamp, postId);
        Put put = new Put(Bytes.toBytes(rowKey));
        
        // Store content
        put.addColumn(Bytes.toBytes("content"), Bytes.toBytes("text"), 
                     Bytes.toBytes(content));
        put.addColumn(Bytes.toBytes("content"), Bytes.toBytes("media_urls"), 
                     Bytes.toBytes(String.join(",", mediaUrls)));
        put.addColumn(Bytes.toBytes("content"), Bytes.toBytes("hashtags"), 
                     Bytes.toBytes(String.join(",", hashtags)));
        
        // Store metadata
        put.addColumn(Bytes.toBytes("metadata"), Bytes.toBytes("timestamp"), 
                     Bytes.toBytes(Long.toString(timestamp)));
        put.addColumn(Bytes.toBytes("metadata"), Bytes.toBytes("post_id"), 
                     Bytes.toBytes(postId));
        
        // Initialize engagement counters
        put.addColumn(Bytes.toBytes("engagement"), Bytes.toBytes("likes"), 
                     Bytes.toBytes("0"));
        put.addColumn(Bytes.toBytes("engagement"), Bytes.toBytes("comments"), 
                     Bytes.toBytes("0"));
        put.addColumn(Bytes.toBytes("engagement"), Bytes.toBytes("shares"), 
                     Bytes.toBytes("0"));
        
        postsTable.put(put);
    }
    
    private void fanOutToFollowers(String userId, String postId, long timestamp, 
                                  String content, List<String> mediaUrls, List<String> hashtags) 
                                  throws IOException {
        // Get followers list
        List<String> followers = getFollowers(userId);
        
        // Create timeline entries for each follower
        List<Put> timelinePuts = new ArrayList<>();
        for (String followerId : followers) {
            String timelineRowKey = SocialMediaDataModel.buildTimelineRowKey(followerId, timestamp, postId);
            Put timelinePut = new Put(Bytes.toBytes(timelineRowKey));
            
            // Store post data in timeline
            timelinePut.addColumn(Bytes.toBytes("post_data"), Bytes.toBytes("content"), 
                                 Bytes.toBytes(content));
            timelinePut.addColumn(Bytes.toBytes("post_data"), Bytes.toBytes("media_urls"), 
                                 Bytes.toBytes(String.join(",", mediaUrls)));
            timelinePut.addColumn(Bytes.toBytes("post_data"), Bytes.toBytes("hashtags"), 
                                 Bytes.toBytes(String.join(",", hashtags)));
            
            // Store author info
            timelinePut.addColumn(Bytes.toBytes("author_info"), Bytes.toBytes("user_id"), 
                                 Bytes.toBytes(userId));
            timelinePut.addColumn(Bytes.toBytes("author_info"), Bytes.toBytes("timestamp"), 
                                 Bytes.toBytes(Long.toString(timestamp)));
            timelinePut.addColumn(Bytes.toBytes("author_info"), Bytes.toBytes("post_id"), 
                                 Bytes.toBytes(postId));
            
            timelinePuts.add(timelinePut);
        }
        
        // Batch insert timeline entries
        if (!timelinePuts.isEmpty()) {
            timelineTable.put(timelinePuts);
        }
    }
    
    private List<String> getFollowers(String userId) throws IOException {
        Get get = new Get(Bytes.toBytes(userId));
        get.addFamily(Bytes.toBytes("followers"));
        Result result = followersTable.get(get);
        
        List<String> followers = new ArrayList<>();
        NavigableMap<byte[], byte[]> followersMap = result.getFamilyMap(Bytes.toBytes("followers"));
        
        for (Map.Entry<byte[], byte[]> entry : followersMap.entrySet()) {
            followers.add(Bytes.toString(entry.getKey()));
        }
        
        return followers;
    }
}
```

**3. Feed Retrieval Service:**
```java
public class FeedRetrievalService {
    private Connection hbaseConnection;
    private Table timelineTable;
    private Table postsTable;
    
    public List<Post> getUserTimeline(String userId, int limit, String lastPostId) throws IOException {
        Scan scan = new Scan();
        
        // Set start row
        if (lastPostId != null) {
            // Continue from last post for pagination
            scan.setStartRow(Bytes.toBytes(userId + "_" + lastPostId));
        } else {
            scan.setStartRow(Bytes.toBytes(userId + "_"));
        }
        
        // Set end row
        scan.setStopRow(Bytes.toBytes(userId + "_" + "~")); // ~ is after all numbers/letters
        
        scan.setCaching(limit);
        scan.setLimit(limit);
        
        List<Post> timeline = new ArrayList<>();
        ResultScanner scanner = timelineTable.getScanner(scan);
        
        for (Result result : scanner) {
            Post post = new Post();
            
            // Extract post data
            String content = Bytes.toString(result.getValue(Bytes.toBytes("post_data"), Bytes.toBytes("content")));
            String mediaUrls = Bytes.toString(result.getValue(Bytes.toBytes("post_data"), Bytes.toBytes("media_urls")));
            String hashtags = Bytes.toString(result.getValue(Bytes.toBytes("post_data"), Bytes.toBytes("hashtags")));
            
            post.setContent(content);
            post.setMediaUrls(Arrays.asList(mediaUrls.split(",")));
            post.setHashtags(Arrays.asList(hashtags.split(",")));
            
            // Extract author info
            String authorId = Bytes.toString(result.getValue(Bytes.toBytes("author_info"), Bytes.toBytes("user_id")));
            String timestamp = Bytes.toString(result.getValue(Bytes.toBytes("author_info"), Bytes.toBytes("timestamp")));
            String postId = Bytes.toString(result.getValue(Bytes.toBytes("author_info"), Bytes.toBytes("post_id")));
            
            post.setAuthorId(authorId);
            post.setTimestamp(Long.parseLong(timestamp));
            post.setPostId(postId);
            
            timeline.add(post);
        }
        
        scanner.close();
        return timeline;
    }
    
    public List<Post> getUserPosts(String userId, int limit) throws IOException {
        Scan scan = new Scan();
        scan.setStartRow(Bytes.toBytes(userId + "_"));
        scan.setStopRow(Bytes.toBytes(userId + "_" + "~"));
        scan.setCaching(limit);
        scan.setLimit(limit);
        
        List<Post> posts = new ArrayList<>();
        ResultScanner scanner = postsTable.getScanner(scan);
        
        for (Result result : scanner) {
            Post post = extractPostFromResult(result);
            posts.add(post);
        }
        
        scanner.close();
        return posts;
    }
    
    private Post extractPostFromResult(Result result) {
        Post post = new Post();
        
        // Extract content
        String content = Bytes.toString(result.getValue(Bytes.toBytes("content"), Bytes.toBytes("text")));
        String mediaUrls = Bytes.toString(result.getValue(Bytes.toBytes("content"), Bytes.toBytes("media_urls")));
        String hashtags = Bytes.toString(result.getValue(Bytes.toBytes("content"), Bytes.toBytes("hashtags")));
        
        post.setContent(content);
        if (mediaUrls != null && !mediaUrls.isEmpty()) {
            post.setMediaUrls(Arrays.asList(mediaUrls.split(",")));
        }
        if (hashtags != null && !hashtags.isEmpty()) {
            post.setHashtags(Arrays.asList(hashtags.split(",")));
        }
        
        // Extract metadata
        String timestamp = Bytes.toString(result.getValue(Bytes.toBytes("metadata"), Bytes.toBytes("timestamp")));
        String postId = Bytes.toString(result.getValue(Bytes.toBytes("metadata"), Bytes.toBytes("post_id")));
        
        post.setTimestamp(Long.parseLong(timestamp));
        post.setPostId(postId);
        
        // Extract engagement
        String likes = Bytes.toString(result.getValue(Bytes.toBytes("engagement"), Bytes.toBytes("likes")));
        String comments = Bytes.toString(result.getValue(Bytes.toBytes("engagement"), Bytes.toBytes("comments")));
        String shares = Bytes.toString(result.getValue(Bytes.toBytes("engagement"), Bytes.toBytes("shares")));
        
        post.setLikes(Integer.parseInt(likes));
        post.setComments(Integer.parseInt(comments));
        post.setShares(Integer.parseInt(shares));
        
        return post;
    }
}
```

---

## 📚 Additional Resources

### Best Practices Summary
1. **Row Key Design**: Avoid hotspotting with proper key distribution
2. **Column Families**: Keep families small and related
3. **Batch Operations**: Use bulk operations for better performance
4. **Monitoring**: Implement comprehensive monitoring and alerting
5. **Backup Strategy**: Regular snapshots and replication setup

### Recommended Reading
- "HBase: The Definitive Guide" by Lars George
- Apache HBase Official Documentation
- "Hadoop: The Definitive Guide" - HBase chapters

### Hands-on Practice
- Local HBase cluster setup
- Phoenix SQL layer integration
- Spark-HBase connector usage
- Real-time analytics implementations

---

*This comprehensive guide covers essential HBase concepts for NoSQL database and big data engineering roles. Practice with large datasets and real-time applications to master HBase operations.*