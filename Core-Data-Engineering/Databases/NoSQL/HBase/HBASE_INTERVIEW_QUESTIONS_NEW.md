# HBase Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions](#-basic-level-questions)
2. [Intermediate Level Questions](#-intermediate-level-questions)
3. [Advanced Level Questions](#-advanced-level-questions)
4. [Architecture & Performance](#-architecture--performance)
5. [Streaming & Real-time Processing](#-streaming--real-time-processing)
6. [Production & Operations](#-production--operations)
7. [Scenario-Based Questions](#-scenario-based-questions)

---

## 🟢 Basic Level Questions

### 1. What is Apache HBase and when should you use it?
**Answer**: Apache HBase is a distributed, scalable, NoSQL database built on top of Hadoop HDFS, modeled after Google's Bigtable. It provides real-time read/write access to large datasets.

**When to Use HBase:**
- Large datasets requiring random access (TB/PB scale)
- Real-time analytics with low-latency requirements
- Sparse data with varying column structures
- Time-series data storage (IoT, logs, metrics)
- Applications needing strong consistency

**Example Use Case:**
```java
// IoT sensor data storage
Put sensorData = new Put(Bytes.toBytes("sensor123_" + timestamp));
sensorData.addColumn(Bytes.toBytes("readings"), Bytes.toBytes("temperature"), 
                    Bytes.toBytes("23.5"));
sensorData.addColumn(Bytes.toBytes("readings"), Bytes.toBytes("humidity"), 
                    Bytes.toBytes("65.2"));
table.put(sensorData);
```

### 2. Explain HBase data model and key components
**Answer**: HBase uses a column-family data model with the following components:

**Data Model Structure:**
- **Table**: Collection of rows
- **Row Key**: Unique identifier (byte array)
- **Column Family**: Group of related columns
- **Column Qualifier**: Specific column within family
- **Cell**: Intersection of row and column (value + timestamp)
- **Timestamp**: Version identifier for cell values

```java
// Data model example
Table: user_profiles
Row Key: "user123"
Column Families: personal_info, preferences
Columns: personal_info:name, personal_info:email, preferences:theme

Put put = new Put(Bytes.toBytes("user123"));
put.addColumn(Bytes.toBytes("personal_info"), Bytes.toBytes("name"), 
              Bytes.toBytes("John Doe"));
put.addColumn(Bytes.toBytes("personal_info"), Bytes.toBytes("email"), 
              Bytes.toBytes("john@example.com"));
put.addColumn(Bytes.toBytes("preferences"), Bytes.toBytes("theme"), 
              Bytes.toBytes("dark"));
```

### 3. What are the main differences between HBase and RDBMS?
**Answer**: Key differences between HBase and traditional relational databases:

| Aspect | HBase | RDBMS |
|--------|-------|-------|
| **Data Model** | Column-family, sparse | Relational, structured |
| **Schema** | Schema-less, flexible | Fixed schema |
| **ACID** | Row-level ACID only | Full ACID compliance |
| **Scalability** | Horizontal scaling | Vertical scaling |
| **Joins** | No joins | Complex joins supported |
| **Indexes** | Row key only | Multiple indexes |
| **Query Language** | API-based | SQL |
| **Consistency** | Strong consistency | ACID consistency |

**When to Choose HBase:**
- Large datasets (TB/PB scale)
- High write throughput
- Sparse data structures
- Real-time random access patterns

### 4. Describe HBase architecture components
**Answer**: HBase architecture consists of several key components:

**Core Components:**
1. **HMaster**: Cluster coordinator and metadata manager
2. **RegionServer**: Handles data storage and retrieval
3. **ZooKeeper**: Coordination and configuration management
4. **HDFS**: Underlying distributed storage

```java
// Architecture flow
Client → ZooKeeper (metadata) → RegionServer (data) → HDFS (storage)

// Configuration example
Configuration conf = HBaseConfiguration.create();
conf.set("hbase.zookeeper.quorum", "zk1,zk2,zk3");
conf.set("hbase.master", "master1:16000");
```

### 5. How do you create tables and perform basic operations in HBase?
**Answer**: Basic HBase operations using Java API:

```java
// Create connection
Configuration conf = HBaseConfiguration.create();
Connection connection = ConnectionFactory.createConnection(conf);
Admin admin = connection.getAdmin();

// Create table
TableDescriptor tableDesc = TableDescriptorBuilder
    .newBuilder(TableName.valueOf("users"))
    .setColumnFamily(ColumnFamilyDescriptorBuilder.of("personal"))
    .setColumnFamily(ColumnFamilyDescriptorBuilder.of("preferences"))
    .build();
admin.createTable(tableDesc);

// Get table reference
Table table = connection.getTable(TableName.valueOf("users"));

// Put operation
Put put = new Put(Bytes.toBytes("user123"));
put.addColumn(Bytes.toBytes("personal"), Bytes.toBytes("name"), 
              Bytes.toBytes("John Doe"));
table.put(put);

// Get operation
Get get = new Get(Bytes.toBytes("user123"));
Result result = table.get(get);
String name = Bytes.toString(result.getValue(Bytes.toBytes("personal"), 
                                           Bytes.toBytes("name")));

// Scan operation
Scan scan = new Scan();
ResultScanner scanner = table.getScanner(scan);
for (Result r : scanner) {
    // Process results
}
scanner.close();
```

### 6. What are HBase regions and how do they work?
**Answer**: Regions are horizontal partitions of HBase tables that contain a contiguous range of rows.

**Region Characteristics:**
- Contains rows from start key to end key
- Default size: 10GB (configurable)
- Automatically split when size threshold reached
- Served by single RegionServer

```java
// Region management
Configuration conf = HBaseConfiguration.create();
conf.setLong("hbase.hregion.max.filesize", 10737418240L); // 10GB

// Pre-split table to avoid hotspotting
byte[][] splits = new byte[10][];
for (int i = 0; i < 10; i++) {
    splits[i] = Bytes.toBytes(String.format("%02d", i));
}
admin.createTable(tableDescriptor, splits);

// Manual region operations
admin.split(TableName.valueOf("users"), Bytes.toBytes("split_point"));
admin.majorCompact(TableName.valueOf("users"));
```

### 7. How do you design effective row keys in HBase?
**Answer**: Row key design is crucial for HBase performance and avoiding hotspotting.

**Design Principles:**
1. **Avoid Sequential Keys**: Prevent hotspotting
2. **Distribute Load**: Use salting or hashing
3. **Optimize for Access Patterns**: Consider query requirements
4. **Keep Keys Short**: Reduce storage overhead

```java
// Bad: Sequential keys (causes hotspotting)
String badKey = timestamp + "_" + userId; // All recent data in one region

// Good: Salted keys for distribution
public class RowKeyDesign {
    public static String createSaltedKey(String userId, long timestamp) {
        int salt = Math.abs(userId.hashCode()) % 100;
        return String.format("%02d_%s_%019d", salt, userId, 
                           Long.MAX_VALUE - timestamp);
    }
    
    // Composite key for range queries
    public static String createCompositeKey(String deviceId, long timestamp, String eventType) {
        return deviceId + "_" + (Long.MAX_VALUE - timestamp) + "_" + eventType;
    }
}
```

### 8. What are column families and how should they be designed?
**Answer**: Column families are groups of related columns that are stored together and have similar access patterns.

**Best Practices:**
- Keep number of column families small (2-3 per table)
- Group frequently accessed columns together
- Configure different properties per family

```java
// Good column family design
TableDescriptor tableDesc = TableDescriptorBuilder
    .newBuilder(TableName.valueOf("user_data"))
    .setColumnFamily(ColumnFamilyDescriptorBuilder
        .newBuilder(Bytes.toBytes("profile")) // Frequently accessed
        .setMaxVersions(1)
        .setCompressionType(Compression.Algorithm.SNAPPY)
        .setBloomFilterType(BloomType.ROW)
        .build())
    .setColumnFamily(ColumnFamilyDescriptorBuilder
        .newBuilder(Bytes.toBytes("activity")) // Different access pattern
        .setMaxVersions(10)
        .setTimeToLive(2592000) // 30 days TTL
        .build())
    .build();
```

### 9. How does HBase handle versioning?
**Answer**: HBase supports multiple versions of data for each cell, identified by timestamps.

```java
// Configure versioning
ColumnFamilyDescriptor cfDesc = ColumnFamilyDescriptorBuilder
    .newBuilder(Bytes.toBytes("cf1"))
    .setMaxVersions(5) // Keep 5 versions
    .setMinVersions(1) // Keep at least 1 version
    .build();

// Write multiple versions
Put put1 = new Put(Bytes.toBytes("row1"));
put1.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col1"), 
              Bytes.toBytes("version1"));
table.put(put1);

Thread.sleep(1000);

Put put2 = new Put(Bytes.toBytes("row1"));
put2.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col1"), 
              Bytes.toBytes("version2"));
table.put(put2);

// Read all versions
Get get = new Get(Bytes.toBytes("row1"));
get.setMaxVersions(); // Get all versions
Result result = table.get(get);

// Iterate through versions
NavigableMap<Long, byte[]> versions = result.getMap()
    .get(Bytes.toBytes("cf1"))
    .get(Bytes.toBytes("col1"));
    
for (Map.Entry<Long, byte[]> entry : versions.entrySet()) {
    long timestamp = entry.getKey();
    String value = Bytes.toString(entry.getValue());
    System.out.println("Timestamp: " + timestamp + ", Value: " + value);
}
```

### 10. What is the difference between Put and Get operations?
**Answer**: Put and Get are fundamental HBase operations for writing and reading data.

```java
// Put operation - Write data
Put put = new Put(Bytes.toBytes("row1"));
put.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col1"), 
              Bytes.toBytes("value1"));
put.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col2"), 
              Bytes.toBytes("value2"));
table.put(put);

// Batch puts for better performance
List<Put> puts = new ArrayList<>();
for (int i = 0; i < 1000; i++) {
    Put batchPut = new Put(Bytes.toBytes("row" + i));
    batchPut.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("data"), 
                      Bytes.toBytes("value" + i));
    puts.add(batchPut);
}
table.put(puts);

// Get operation - Read data
Get get = new Get(Bytes.toBytes("row1"));
get.addFamily(Bytes.toBytes("cf1")); // Specify column family
Result result = table.get(get);

// Extract values
byte[] value1 = result.getValue(Bytes.toBytes("cf1"), Bytes.toBytes("col1"));
String stringValue = Bytes.toString(value1);

// Check if row exists
boolean exists = !result.isEmpty();
```

---

## 🟡 Intermediate Level Questions

### 11. How do you implement efficient scanning in HBase?
**Answer**: Efficient scanning requires proper configuration and filtering to minimize data transfer and processing.

```java
public class EfficientScanning {
    public List<Result> optimizedScan(String startKey, String endKey, 
                                     String columnFamily) throws IOException {
        Scan scan = new Scan();
        
        // Set row range
        scan.setStartRow(Bytes.toBytes(startKey));
        scan.setStopRow(Bytes.toBytes(endKey));
        
        // Optimize performance
        scan.setCaching(1000); // Cache 1000 rows
        scan.setBatch(100); // Batch size for columns
        scan.addFamily(Bytes.toBytes(columnFamily)); // Specify column family
        
        // Use filters to reduce data transfer
        FilterList filters = new FilterList(FilterList.Operator.MUST_PASS_ALL);
        filters.addFilter(new PageFilter(10000)); // Limit results
        filters.addFilter(new SingleColumnValueFilter(
            Bytes.toBytes(columnFamily), 
            Bytes.toBytes("status"),
            CompareOperator.EQUAL, 
            Bytes.toBytes("active")
        ));
        scan.setFilter(filters);
        
        List<Result> results = new ArrayList<>();
        ResultScanner scanner = table.getScanner(scan);
        
        try {
            for (Result result : scanner) {
                results.add(result);
            }
        } finally {
            scanner.close(); // Always close scanner
        }
        
        return results;
    }
}
```

### 12. Explain HBase filters and their usage
**Answer**: HBase filters allow server-side data filtering to reduce network traffic and improve performance.

```java
public class HBaseFilters {
    
    // Single column value filter
    public void singleColumnValueFilter() throws IOException {
        Scan scan = new Scan();
        Filter filter = new SingleColumnValueFilter(
            Bytes.toBytes("cf1"),
            Bytes.toBytes("age"),
            CompareOperator.GREATER,
            Bytes.toBytes("25")
        );
        scan.setFilter(filter);
    }
    
    // Prefix filter
    public void prefixFilter() throws IOException {
        Scan scan = new Scan();
        Filter filter = new PrefixFilter(Bytes.toBytes("user_"));
        scan.setFilter(filter);
    }
    
    // Row key filter
    public void rowKeyFilter() throws IOException {
        Scan scan = new Scan();
        Filter filter = new RowFilter(
            CompareOperator.EQUAL,
            new RegexStringComparator("user_[0-9]+")
        );
        scan.setFilter(filter);
    }
    
    // Column prefix filter
    public void columnPrefixFilter() throws IOException {
        Scan scan = new Scan();
        Filter filter = new ColumnPrefixFilter(Bytes.toBytes("temp_"));
        scan.setFilter(filter);
    }
    
    // Multiple filters
    public void multipleFilters() throws IOException {
        Scan scan = new Scan();
        
        FilterList filterList = new FilterList(FilterList.Operator.MUST_PASS_ALL);
        filterList.addFilter(new PrefixFilter(Bytes.toBytes("user_")));
        filterList.addFilter(new SingleColumnValueFilter(
            Bytes.toBytes("cf1"), Bytes.toBytes("status"),
            CompareOperator.EQUAL, Bytes.toBytes("active")
        ));
        filterList.addFilter(new PageFilter(1000));
        
        scan.setFilter(filterList);
    }
    
    // Custom filter
    public void customFilter() throws IOException {
        Scan scan = new Scan();
        Filter filter = new ValueFilter(
            CompareOperator.GREATER,
            new BinaryComparator(Bytes.toBytes("threshold_value"))
        );
        scan.setFilter(filter);
    }
}
```

### 13. How do you handle bulk loading in HBase?
**Answer**: Bulk loading is the most efficient way to load large amounts of data into HBase.

```java
public class BulkLoading {
    
    // Method 1: Using ImportTsv and LoadIncrementalHFiles
    public void bulkLoadFromCSV() throws Exception {
        // Step 1: Generate HFiles using ImportTsv
        String[] importArgs = {
            "-Dimporttsv.columns=HBASE_ROW_KEY,cf1:col1,cf1:col2",
            "-Dimporttsv.bulk.output=/tmp/hfiles",
            "my_table",
            "/input/data.csv"
        };
        ImportTsv.main(importArgs);
        
        // Step 2: Load HFiles into HBase
        String[] loadArgs = {
            "/tmp/hfiles",
            "my_table"
        };
        LoadIncrementalHFiles.main(loadArgs);
    }
    
    // Method 2: Programmatic bulk loading
    public void programmaticBulkLoad(List<DataRecord> records) throws IOException {
        Configuration conf = HBaseConfiguration.create();
        Connection connection = ConnectionFactory.createConnection(conf);
        Table table = connection.getTable(TableName.valueOf("my_table"));
        
        // Prepare puts
        List<Put> puts = new ArrayList<>();
        for (DataRecord record : records) {
            Put put = new Put(Bytes.toBytes(record.getRowKey()));
            put.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col1"), 
                         Bytes.toBytes(record.getValue1()));
            put.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col2"), 
                         Bytes.toBytes(record.getValue2()));
            puts.add(put);
            
            // Batch every 10000 records
            if (puts.size() >= 10000) {
                table.put(puts);
                puts.clear();
            }
        }
        
        // Insert remaining records
        if (!puts.isEmpty()) {
            table.put(puts);
        }
        
        table.close();
        connection.close();
    }
    
    // Method 3: Using MapReduce for bulk loading
    public void mapReduceBulkLoad() throws Exception {
        Configuration conf = HBaseConfiguration.create();
        Job job = Job.getInstance(conf, "bulk-load");
        
        job.setJarByClass(BulkLoadMapper.class);
        job.setMapperClass(BulkLoadMapper.class);
        job.setMapOutputKeyClass(ImmutableBytesWritable.class);
        job.setMapOutputValueClass(Put.class);
        
        // Configure HFile output
        Table table = ConnectionFactory.createConnection(conf)
            .getTable(TableName.valueOf("my_table"));
        HFileOutputFormat2.configureIncrementalLoad(job, table, 
            table.getRegionLocator());
        
        FileInputFormat.addInputPath(job, new Path("/input/data"));
        FileOutputFormat.setOutputPath(job, new Path("/output/hfiles"));
        
        job.waitForCompletion(true);
        
        // Load generated HFiles
        LoadIncrementalHFiles loader = new LoadIncrementalHFiles(conf);
        loader.doBulkLoad(new Path("/output/hfiles"), 
            ConnectionFactory.createConnection(conf).getAdmin(), 
            table, table.getRegionLocator());
    }
}
```

### 14. What are coprocessors and how do you use them?
**Answer**: Coprocessors are server-side processing extensions that allow custom code execution within RegionServers.

```java
// Observer coprocessor example
public class AuditCoprocessor implements RegionObserver {
    
    @Override
    public void prePut(ObserverContext<RegionCoprocessorEnvironment> c, 
                      Put put, WALEdit edit, Durability durability) throws IOException {
        // Audit logging before put operation
        String rowKey = Bytes.toString(put.getRow());
        String timestamp = String.valueOf(System.currentTimeMillis());
        
        // Add audit column
        put.addColumn(Bytes.toBytes("audit"), Bytes.toBytes("modified_time"), 
                     Bytes.toBytes(timestamp));
        put.addColumn(Bytes.toBytes("audit"), Bytes.toBytes("modified_by"), 
                     Bytes.toBytes("system"));
    }
    
    @Override
    public void postPut(ObserverContext<RegionCoprocessorEnvironment> c, 
                       Put put, WALEdit edit, Durability durability) throws IOException {
        // Post-processing after put operation
        logAuditEvent("PUT", Bytes.toString(put.getRow()));
    }
    
    private void logAuditEvent(String operation, String rowKey) {
        // Log to external audit system
        System.out.println("Audit: " + operation + " on row " + rowKey);
    }
}

// Endpoint coprocessor example
public class StatisticsEndpoint extends StatisticsService implements CoprocessorService {
    
    @Override
    public void getRowCount(RpcController controller, 
                           StatisticsRequest request,
                           RpcCallback<StatisticsResponse> done) {
        
        RegionCoprocessorEnvironment env = (RegionCoprocessorEnvironment) getEnvironment();
        Region region = env.getRegion();
        
        long count = 0;
        try {
            Scan scan = new Scan();
            scan.setFilter(new KeyOnlyFilter());
            
            RegionScanner scanner = region.getScanner(scan);
            List<Cell> results = new ArrayList<>();
            
            while (scanner.next(results)) {
                count++;
                results.clear();
            }
            scanner.close();
            
        } catch (IOException e) {
            controller.setFailed(e.getMessage());
            return;
        }
        
        StatisticsResponse response = StatisticsResponse.newBuilder()
            .setRowCount(count)
            .build();
        done.run(response);
    }
}

// Deploy coprocessor
public void deployCoprocessor() throws IOException {
    Admin admin = connection.getAdmin();
    TableName tableName = TableName.valueOf("my_table");
    
    // Add coprocessor to table
    TableDescriptor tableDesc = admin.getDescriptor(tableName);
    TableDescriptorBuilder builder = TableDescriptorBuilder.newBuilder(tableDesc);
    builder.setCoprocessor("com.example.AuditCoprocessor");
    
    admin.disableTable(tableName);
    admin.modifyTable(builder.build());
    admin.enableTable(tableName);
}
```

### 15. How do you implement atomic operations in HBase?
**Answer**: HBase provides several mechanisms for atomic operations within single rows.

```java
public class AtomicOperations {
    
    // Check and Put
    public boolean conditionalUpdate(String rowKey, String expectedValue, 
                                   String newValue) throws IOException {
        return table.checkAndPut(
            Bytes.toBytes(rowKey),
            Bytes.toBytes("cf1"),
            Bytes.toBytes("status"),
            Bytes.toBytes(expectedValue),
            createPut(rowKey, newValue)
        );
    }
    
    // Check and Delete
    public boolean conditionalDelete(String rowKey, String expectedValue) throws IOException {
        Delete delete = new Delete(Bytes.toBytes(rowKey));
        return table.checkAndDelete(
            Bytes.toBytes(rowKey),
            Bytes.toBytes("cf1"),
            Bytes.toBytes("status"),
            Bytes.toBytes(expectedValue),
            delete
        );
    }
    
    // Increment operation
    public long incrementCounter(String rowKey, String column, long delta) throws IOException {
        return table.incrementColumnValue(
            Bytes.toBytes(rowKey),
            Bytes.toBytes("counters"),
            Bytes.toBytes(column),
            delta
        );
    }
    
    // Append operation
    public void appendToColumn(String rowKey, String column, String value) throws IOException {
        Append append = new Append(Bytes.toBytes(rowKey));
        append.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes(column), 
                        Bytes.toBytes(value));
        table.append(append);
    }
    
    // Row lock (deprecated in newer versions)
    public void atomicRowUpdate(String rowKey) throws IOException {
        // Use checkAndPut for atomic updates instead of row locks
        boolean success = false;
        int maxRetries = 10;
        int retries = 0;
        
        while (!success && retries < maxRetries) {
            // Get current value
            Get get = new Get(Bytes.toBytes(rowKey));
            Result result = table.get(get);
            
            if (result.isEmpty()) {
                // Row doesn't exist, create it
                Put put = createInitialPut(rowKey);
                success = table.checkAndPut(
                    Bytes.toBytes(rowKey),
                    Bytes.toBytes("cf1"),
                    Bytes.toBytes("version"),
                    null, // null means column doesn't exist
                    put
                );
            } else {
                // Row exists, update it
                String currentVersion = Bytes.toString(
                    result.getValue(Bytes.toBytes("cf1"), Bytes.toBytes("version"))
                );
                
                Put put = createUpdatedPut(rowKey, currentVersion);
                success = table.checkAndPut(
                    Bytes.toBytes(rowKey),
                    Bytes.toBytes("cf1"),
                    Bytes.toBytes("version"),
                    Bytes.toBytes(currentVersion),
                    put
                );
            }
            
            retries++;
            if (!success) {
                Thread.sleep(100); // Brief pause before retry
            }
        }
    }
    
    private Put createPut(String rowKey, String value) {
        Put put = new Put(Bytes.toBytes(rowKey));
        put.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("data"), 
                     Bytes.toBytes(value));
        return put;
    }
    
    private Put createInitialPut(String rowKey) {
        Put put = new Put(Bytes.toBytes(rowKey));
        put.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("version"), 
                     Bytes.toBytes("1"));
        put.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("created"), 
                     Bytes.toBytes(System.currentTimeMillis()));
        return put;
    }
    
    private Put createUpdatedPut(String rowKey, String currentVersion) {
        int newVersion = Integer.parseInt(currentVersion) + 1;
        Put put = new Put(Bytes.toBytes(rowKey));
        put.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("version"), 
                     Bytes.toBytes(String.valueOf(newVersion)));
        put.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("updated"), 
                     Bytes.toBytes(System.currentTimeMillis()));
        return put;
    }
}
```

---

I'll continue with the remaining sections in the next batch to avoid file freezing. Let me add the next batch of questions:
# HBase Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions](#-basic-level-questions)
2. [Intermediate Level Questions](#-intermediate-level-questions)
3. [Advanced Level Questions](#-advanced-level-questions)
4. [Architecture & Performance](#-architecture--performance)
5. [Streaming & Real-time Processing](#-streaming--real-time-processing)
6. [Production & Operations](#-production--operations)
7. [Scenario-Based Questions](#-scenario-based-questions)

---

## 🟢 Basic Level Questions

### 1. What is Apache HBase and when should you use it?
**Answer**: Apache HBase is a distributed, scalable, NoSQL database built on top of Hadoop HDFS, modeled after Google's Bigtable. It provides real-time read/write access to large datasets.

**When to Use HBase:**
- Large datasets requiring random access (TB/PB scale)
- Real-time analytics with low-latency requirements
- Sparse data with varying column structures
- Time-series data storage (IoT, logs, metrics)
- Applications needing strong consistency

**Example Use Case:**
```java
// IoT sensor data storage
Put sensorData = new Put(Bytes.toBytes("sensor123_" + timestamp));
sensorData.addColumn(Bytes.toBytes("readings"), Bytes.toBytes("temperature"), 
                    Bytes.toBytes("23.5"));
sensorData.addColumn(Bytes.toBytes("readings"), Bytes.toBytes("humidity"), 
                    Bytes.toBytes("65.2"));
table.put(sensorData);
```

### 2. Explain HBase data model and key components
**Answer**: HBase uses a column-family data model with the following components:

**Data Model Structure:**
- **Table**: Collection of rows
- **Row Key**: Unique identifier (byte array)
- **Column Family**: Group of related columns
- **Column Qualifier**: Specific column within family
- **Cell**: Intersection of row and column (value + timestamp)
- **Timestamp**: Version identifier for cell values

```java
// Data model example
Table: user_profiles
Row Key: "user123"
Column Families: personal_info, preferences
Columns: personal_info:name, personal_info:email, preferences:theme

Put put = new Put(Bytes.toBytes("user123"));
put.addColumn(Bytes.toBytes("personal_info"), Bytes.toBytes("name"), 
              Bytes.toBytes("John Doe"));
put.addColumn(Bytes.toBytes("personal_info"), Bytes.toBytes("email"), 
              Bytes.toBytes("john@example.com"));
put.addColumn(Bytes.toBytes("preferences"), Bytes.toBytes("theme"), 
              Bytes.toBytes("dark"));
```

### 3. What are the main differences between HBase and RDBMS?
**Answer**: Key differences between HBase and traditional relational databases:

| Aspect | HBase | RDBMS |
|--------|-------|-------|
| **Data Model** | Column-family, sparse | Relational, structured |
| **Schema** | Schema-less, flexible | Fixed schema |
| **ACID** | Row-level ACID only | Full ACID compliance |
| **Scalability** | Horizontal scaling | Vertical scaling |
| **Joins** | No joins | Complex joins supported |
| **Indexes** | Row key only | Multiple indexes |
| **Query Language** | API-based | SQL |
| **Consistency** | Strong consistency | ACID consistency |

**When to Choose HBase:**
- Large datasets (TB/PB scale)
- High write throughput
- Sparse data structures
- Real-time random access patterns

### 4. Describe HBase architecture components
**Answer**: HBase architecture consists of several key components:

**Core Components:**
1. **HMaster**: Cluster coordinator and metadata manager
2. **RegionServer**: Handles data storage and retrieval
3. **ZooKeeper**: Coordination and configuration management
4. **HDFS**: Underlying distributed storage

```java
// Architecture flow
Client → ZooKeeper (metadata) → RegionServer (data) → HDFS (storage)

// Configuration example
Configuration conf = HBaseConfiguration.create();
conf.set("hbase.zookeeper.quorum", "zk1,zk2,zk3");
conf.set("hbase.master", "master1:16000");
```

### 5. How do you create tables and perform basic operations in HBase?
**Answer**: Basic HBase operations using Java API:

```java
// Create connection
Configuration conf = HBaseConfiguration.create();
Connection connection = ConnectionFactory.createConnection(conf);
Admin admin = connection.getAdmin();

// Create table
TableDescriptor tableDesc = TableDescriptorBuilder
    .newBuilder(TableName.valueOf("users"))
    .setColumnFamily(ColumnFamilyDescriptorBuilder.of("personal"))
    .setColumnFamily(ColumnFamilyDescriptorBuilder.of("preferences"))
    .build();
admin.createTable(tableDesc);

// Get table reference
Table table = connection.getTable(TableName.valueOf("users"));

// Put operation
Put put = new Put(Bytes.toBytes("user123"));
put.addColumn(Bytes.toBytes("personal"), Bytes.toBytes("name"), 
              Bytes.toBytes("John Doe"));
table.put(put);

// Get operation
Get get = new Get(Bytes.toBytes("user123"));
Result result = table.get(get);
String name = Bytes.toString(result.getValue(Bytes.toBytes("personal"), 
                                           Bytes.toBytes("name")));

// Scan operation
Scan scan = new Scan();
ResultScanner scanner = table.getScanner(scan);
for (Result r : scanner) {
    // Process results
}
scanner.close();
```

### 6. What are HBase regions and how do they work?
**Answer**: Regions are horizontal partitions of HBase tables that contain a contiguous range of rows.

**Region Characteristics:**
- Contains rows from start key to end key
- Default size: 10GB (configurable)
- Automatically split when size threshold reached
- Served by single RegionServer

```java
// Region management
Configuration conf = HBaseConfiguration.create();
conf.setLong("hbase.hregion.max.filesize", 10737418240L); // 10GB

// Pre-split table to avoid hotspotting
byte[][] splits = new byte[10][];
for (int i = 0; i < 10; i++) {
    splits[i] = Bytes.toBytes(String.format("%02d", i));
}
admin.createTable(tableDescriptor, splits);

// Manual region operations
admin.split(TableName.valueOf("users"), Bytes.toBytes("split_point"));
admin.majorCompact(TableName.valueOf("users"));
```

### 7. How do you design effective row keys in HBase?
**Answer**: Row key design is crucial for HBase performance and avoiding hotspotting.

**Design Principles:**
1. **Avoid Sequential Keys**: Prevent hotspotting
2. **Distribute Load**: Use salting or hashing
3. **Optimize for Access Patterns**: Consider query requirements
4. **Keep Keys Short**: Reduce storage overhead

```java
// Bad: Sequential keys (causes hotspotting)
String badKey = timestamp + "_" + userId; // All recent data in one region

// Good: Salted keys for distribution
public class RowKeyDesign {
    public static String createSaltedKey(String userId, long timestamp) {
        int salt = Math.abs(userId.hashCode()) % 100;
        return String.format("%02d_%s_%019d", salt, userId, 
                           Long.MAX_VALUE - timestamp);
    }
    
    // Composite key for range queries
    public static String createCompositeKey(String deviceId, long timestamp, String eventType) {
        return deviceId + "_" + (Long.MAX_VALUE - timestamp) + "_" + eventType;
    }
}
```

### 8. What are column families and how should they be designed?
**Answer**: Column families are groups of related columns that are stored together and have similar access patterns.

**Best Practices:**
- Keep number of column families small (2-3 per table)
- Group frequently accessed columns together
- Configure different properties per family

```java
// Good column family design
TableDescriptor tableDesc = TableDescriptorBuilder
    .newBuilder(TableName.valueOf("user_data"))
    .setColumnFamily(ColumnFamilyDescriptorBuilder
        .newBuilder(Bytes.toBytes("profile")) // Frequently accessed
        .setMaxVersions(1)
        .setCompressionType(Compression.Algorithm.SNAPPY)
        .setBloomFilterType(BloomType.ROW)
        .build())
    .setColumnFamily(ColumnFamilyDescriptorBuilder
        .newBuilder(Bytes.toBytes("activity")) // Different access pattern
        .setMaxVersions(10)
        .setTimeToLive(2592000) // 30 days TTL
        .build())
    .build();
```

### 9. How does HBase handle versioning?
**Answer**: HBase supports multiple versions of data for each cell, identified by timestamps.

```java
// Configure versioning
ColumnFamilyDescriptor cfDesc = ColumnFamilyDescriptorBuilder
    .newBuilder(Bytes.toBytes("cf1"))
    .setMaxVersions(5) // Keep 5 versions
    .setMinVersions(1) // Keep at least 1 version
    .build();

// Write multiple versions
Put put1 = new Put(Bytes.toBytes("row1"));
put1.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col1"), 
              Bytes.toBytes("version1"));
table.put(put1);

Thread.sleep(1000);

Put put2 = new Put(Bytes.toBytes("row1"));
put2.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col1"), 
              Bytes.toBytes("version2"));
table.put(put2);

// Read all versions
Get get = new Get(Bytes.toBytes("row1"));
get.setMaxVersions(); // Get all versions
Result result = table.get(get);

// Iterate through versions
NavigableMap<Long, byte[]> versions = result.getMap()
    .get(Bytes.toBytes("cf1"))
    .get(Bytes.toBytes("col1"));
    
for (Map.Entry<Long, byte[]> entry : versions.entrySet()) {
    long timestamp = entry.getKey();
    String value = Bytes.toString(entry.getValue());
    System.out.println("Timestamp: " + timestamp + ", Value: " + value);
}
```

### 10. What is the difference between Put and Get operations?
**Answer**: Put and Get are fundamental HBase operations for writing and reading data.

```java
// Put operation - Write data
Put put = new Put(Bytes.toBytes("row1"));
put.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col1"), 
              Bytes.toBytes("value1"));
put.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col2"), 
              Bytes.toBytes("value2"));
table.put(put);

// Batch puts for better performance
List<Put> puts = new ArrayList<>();
for (int i = 0; i < 1000; i++) {
    Put batchPut = new Put(Bytes.toBytes("row" + i));
    batchPut.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("data"), 
                      Bytes.toBytes("value" + i));
    puts.add(batchPut);
}
table.put(puts);

// Get operation - Read data
Get get = new Get(Bytes.toBytes("row1"));
get.addFamily(Bytes.toBytes("cf1")); // Specify column family
Result result = table.get(get);

// Extract values
byte[] value1 = result.getValue(Bytes.toBytes("cf1"), Bytes.toBytes("col1"));
String stringValue = Bytes.toString(value1);

// Check if row exists
boolean exists = !result.isEmpty();
```

---

## 🟡 Intermediate Level Questions

### 11. How do you implement efficient scanning in HBase?
**Answer**: Efficient scanning requires proper configuration and filtering to minimize data transfer and processing.

```java
public class EfficientScanning {
    public List<Result> optimizedScan(String startKey, String endKey, 
                                     String columnFamily) throws IOException {
        Scan scan = new Scan();
        
        // Set row range
        scan.setStartRow(Bytes.toBytes(startKey));
        scan.setStopRow(Bytes.toBytes(endKey));
        
        // Optimize performance
        scan.setCaching(1000); // Cache 1000 rows
        scan.setBatch(100); // Batch size for columns
        scan.addFamily(Bytes.toBytes(columnFamily)); // Specify column family
        
        // Use filters to reduce data transfer
        FilterList filters = new FilterList(FilterList.Operator.MUST_PASS_ALL);
        filters.addFilter(new PageFilter(10000)); // Limit results
        filters.addFilter(new SingleColumnValueFilter(
            Bytes.toBytes(columnFamily), 
            Bytes.toBytes("status"),
            CompareOperator.EQUAL, 
            Bytes.toBytes("active")
        ));
        scan.setFilter(filters);
        
        List<Result> results = new ArrayList<>();
        ResultScanner scanner = table.getScanner(scan);
        
        try {
            for (Result result : scanner) {
                results.add(result);
            }
        } finally {
            scanner.close(); // Always close scanner
        }
        
        return results;
    }
}
```

### 12. Explain HBase filters and their usage
**Answer**: HBase filters allow server-side data filtering to reduce network traffic and improve performance.

```java
public class HBaseFilters {
    
    // Single column value filter
    public void singleColumnValueFilter() throws IOException {
        Scan scan = new Scan();
        Filter filter = new SingleColumnValueFilter(
            Bytes.toBytes("cf1"),
            Bytes.toBytes("age"),
            CompareOperator.GREATER,
            Bytes.toBytes("25")
        );
        scan.setFilter(filter);
    }
    
    // Prefix filter
    public void prefixFilter() throws IOException {
        Scan scan = new Scan();
        Filter filter = new PrefixFilter(Bytes.toBytes("user_"));
        scan.setFilter(filter);
    }
    
    // Row key filter
    public void rowKeyFilter() throws IOException {
        Scan scan = new Scan();
        Filter filter = new RowFilter(
            CompareOperator.EQUAL,
            new RegexStringComparator("user_[0-9]+")
        );
        scan.setFilter(filter);
    }
    
    // Column prefix filter
    public void columnPrefixFilter() throws IOException {
        Scan scan = new Scan();
        Filter filter = new ColumnPrefixFilter(Bytes.toBytes("temp_"));
        scan.setFilter(filter);
    }
    
    // Multiple filters
    public void multipleFilters() throws IOException {
        Scan scan = new Scan();
        
        FilterList filterList = new FilterList(FilterList.Operator.MUST_PASS_ALL);
        filterList.addFilter(new PrefixFilter(Bytes.toBytes("user_")));
        filterList.addFilter(new SingleColumnValueFilter(
            Bytes.toBytes("cf1"), Bytes.toBytes("status"),
            CompareOperator.EQUAL, Bytes.toBytes("active")
        ));
        filterList.addFilter(new PageFilter(1000));
        
        scan.setFilter(filterList);
    }
    
    // Custom filter
    public void customFilter() throws IOException {
        Scan scan = new Scan();
        Filter filter = new ValueFilter(
            CompareOperator.GREATER,
            new BinaryComparator(Bytes.toBytes("threshold_value"))
        );
        scan.setFilter(filter);
    }
}
```

### 13. How do you handle bulk loading in HBase?
**Answer**: Bulk loading is the most efficient way to load large amounts of data into HBase.

```java
public class BulkLoading {
    
    // Method 1: Using ImportTsv and LoadIncrementalHFiles
    public void bulkLoadFromCSV() throws Exception {
        // Step 1: Generate HFiles using ImportTsv
        String[] importArgs = {
            "-Dimporttsv.columns=HBASE_ROW_KEY,cf1:col1,cf1:col2",
            "-Dimporttsv.bulk.output=/tmp/hfiles",
            "my_table",
            "/input/data.csv"
        };
        ImportTsv.main(importArgs);
        
        // Step 2: Load HFiles into HBase
        String[] loadArgs = {
            "/tmp/hfiles",
            "my_table"
        };
        LoadIncrementalHFiles.main(loadArgs);
    }
    
    // Method 2: Programmatic bulk loading
    public void programmaticBulkLoad(List<DataRecord> records) throws IOException {
        Configuration conf = HBaseConfiguration.create();
        Connection connection = ConnectionFactory.createConnection(conf);
        Table table = connection.getTable(TableName.valueOf("my_table"));
        
        // Prepare puts
        List<Put> puts = new ArrayList<>();
        for (DataRecord record : records) {
            Put put = new Put(Bytes.toBytes(record.getRowKey()));
            put.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col1"), 
                         Bytes.toBytes(record.getValue1()));
            put.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col2"), 
                         Bytes.toBytes(record.getValue2()));
            puts.add(put);
            
            // Batch every 10000 records
            if (puts.size() >= 10000) {
                table.put(puts);
                puts.clear();
            }
        }
        
        // Insert remaining records
        if (!puts.isEmpty()) {
            table.put(puts);
        }
        
        table.close();
        connection.close();
    }
    
    // Method 3: Using MapReduce for bulk loading
    public void mapReduceBulkLoad() throws Exception {
        Configuration conf = HBaseConfiguration.create();
        Job job = Job.getInstance(conf, "bulk-load");
        
        job.setJarByClass(BulkLoadMapper.class);
        job.setMapperClass(BulkLoadMapper.class);
        job.setMapOutputKeyClass(ImmutableBytesWritable.class);
        job.setMapOutputValueClass(Put.class);
        
        // Configure HFile output
        Table table = ConnectionFactory.createConnection(conf)
            .getTable(TableName.valueOf("my_table"));
        HFileOutputFormat2.configureIncrementalLoad(job, table, 
            table.getRegionLocator());
        
        FileInputFormat.addInputPath(job, new Path("/input/data"));
        FileOutputFormat.setOutputPath(job, new Path("/output/hfiles"));
        
        job.waitForCompletion(true);
        
        // Load generated HFiles
        LoadIncrementalHFiles loader = new LoadIncrementalHFiles(conf);
        loader.doBulkLoad(new Path("/output/hfiles"), 
            ConnectionFactory.createConnection(conf).getAdmin(), 
            table, table.getRegionLocator());
    }
}
```

### 14. What are coprocessors and how do you use them?
**Answer**: Coprocessors are server-side processing extensions that allow custom code execution within RegionServers.

```java
// Observer coprocessor example
public class AuditCoprocessor implements RegionObserver {
    
    @Override
    public void prePut(ObserverContext<RegionCoprocessorEnvironment> c, 
                      Put put, WALEdit edit, Durability durability) throws IOException {
        // Audit logging before put operation
        String rowKey = Bytes.toString(put.getRow());
        String timestamp = String.valueOf(System.currentTimeMillis());
        
        // Add audit column
        put.addColumn(Bytes.toBytes("audit"), Bytes.toBytes("modified_time"), 
                     Bytes.toBytes(timestamp));
        put.addColumn(Bytes.toBytes("audit"), Bytes.toBytes("modified_by"), 
                     Bytes.toBytes("system"));
    }
    
    @Override
    public void postPut(ObserverContext<RegionCoprocessorEnvironment> c, 
                       Put put, WALEdit edit, Durability durability) throws IOException {
        // Post-processing after put operation
        logAuditEvent("PUT", Bytes.toString(put.getRow()));
    }
    
    private void logAuditEvent(String operation, String rowKey) {
        // Log to external audit system
        System.out.println("Audit: " + operation + " on row " + rowKey);
    }
}

// Endpoint coprocessor example
public class StatisticsEndpoint extends StatisticsService implements CoprocessorService {
    
    @Override
    public void getRowCount(RpcController controller, 
                           StatisticsRequest request,
                           RpcCallback<StatisticsResponse> done) {
        
        RegionCoprocessorEnvironment env = (RegionCoprocessorEnvironment) getEnvironment();
        Region region = env.getRegion();
        
        long count = 0;
        try {
            Scan scan = new Scan();
            scan.setFilter(new KeyOnlyFilter());
            
            RegionScanner scanner = region.getScanner(scan);
            List<Cell> results = new ArrayList<>();
            
            while (scanner.next(results)) {
                count++;
                results.clear();
            }
            scanner.close();
            
        } catch (IOException e) {
            controller.setFailed(e.getMessage());
            return;
        }
        
        StatisticsResponse response = StatisticsResponse.newBuilder()
            .setRowCount(count)
            .build();
        done.run(response);
    }
}

// Deploy coprocessor
public void deployCoprocessor() throws IOException {
    Admin admin = connection.getAdmin();
    TableName tableName = TableName.valueOf("my_table");
    
    // Add coprocessor to table
    TableDescriptor tableDesc = admin.getDescriptor(tableName);
    TableDescriptorBuilder builder = TableDescriptorBuilder.newBuilder(tableDesc);
    builder.setCoprocessor("com.example.AuditCoprocessor");
    
    admin.disableTable(tableName);
    admin.modifyTable(builder.build());
    admin.enableTable(tableName);
}
```

### 15. How do you implement atomic operations in HBase?
**Answer**: HBase provides several mechanisms for atomic operations within single rows.

```java
public class AtomicOperations {
    
    // Check and Put
    public boolean conditionalUpdate(String rowKey, String expectedValue, 
                                   String newValue) throws IOException {
        return table.checkAndPut(
            Bytes.toBytes(rowKey),
            Bytes.toBytes("cf1"),
            Bytes.toBytes("status"),
            Bytes.toBytes(expectedValue),
            createPut(rowKey, newValue)
        );
    }
    
    // Check and Delete
    public boolean conditionalDelete(String rowKey, String expectedValue) throws IOException {
        Delete delete = new Delete(Bytes.toBytes(rowKey));
        return table.checkAndDelete(
            Bytes.toBytes(rowKey),
            Bytes.toBytes("cf1"),
            Bytes.toBytes("status"),
            Bytes.toBytes(expectedValue),
            delete
        );
    }
    
    // Increment operation
    public long incrementCounter(String rowKey, String column, long delta) throws IOException {
        return table.incrementColumnValue(
            Bytes.toBytes(rowKey),
            Bytes.toBytes("counters"),
            Bytes.toBytes(column),
            delta
        );
    }
    
    // Append operation
    public void appendToColumn(String rowKey, String column, String value) throws IOException {
        Append append = new Append(Bytes.toBytes(rowKey));
        append.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes(column), 
                        Bytes.toBytes(value));
        table.append(append);
    }
    
    // Row lock (deprecated in newer versions)
    public void atomicRowUpdate(String rowKey) throws IOException {
        // Use checkAndPut for atomic updates instead of row locks
        boolean success = false;
        int maxRetries = 10;
        int retries = 0;
        
        while (!success && retries < maxRetries) {
            // Get current value
            Get get = new Get(Bytes.toBytes(rowKey));
            Result result = table.get(get);
            
            if (result.isEmpty()) {
                // Row doesn't exist, create it
                Put put = createInitialPut(rowKey);
                success = table.checkAndPut(
                    Bytes.toBytes(rowKey),
                    Bytes.toBytes("cf1"),
                    Bytes.toBytes("version"),
                    null, // null means column doesn't exist
                    put
                );
            } else {
                // Row exists, update it
                String currentVersion = Bytes.toString(
                    result.getValue(Bytes.toBytes("cf1"), Bytes.toBytes("version"))
                );
                
                Put put = createUpdatedPut(rowKey, currentVersion);
                success = table.checkAndPut(
                    Bytes.toBytes(rowKey),
                    Bytes.toBytes("cf1"),
                    Bytes.toBytes("version"),
                    Bytes.toBytes(currentVersion),
                    put
                );
            }
            
            retries++;
            if (!success) {
                Thread.sleep(100); // Brief pause before retry
            }
        }
    }
    
    private Put createPut(String rowKey, String value) {
        Put put = new Put(Bytes.toBytes(rowKey));
        put.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("data"), 
                     Bytes.toBytes(value));
        return put;
    }
    
    private Put createInitialPut(String rowKey) {
        Put put = new Put(Bytes.toBytes(rowKey));
        put.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("version"), 
                     Bytes.toBytes("1"));
        put.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("created"), 
                     Bytes.toBytes(System.currentTimeMillis()));
        return put;
    }
    
    private Put createUpdatedPut(String rowKey, String currentVersion) {
        int newVersion = Integer.parseInt(currentVersion) + 1;
        Put put = new Put(Bytes.toBytes(rowKey));
        put.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("version"), 
                     Bytes.toBytes(String.valueOf(newVersion)));
        put.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("updated"), 
                     Bytes.toBytes(System.currentTimeMillis()));
        return put;
    }
}
```

### 16. How do you handle data compression in HBase?
**Answer**: HBase supports multiple compression algorithms to reduce storage space and I/O.

```java
public class CompressionConfiguration {
    
    // Configure compression for column family
    public void configureCompression() throws IOException {
        Admin admin = connection.getAdmin();
        TableName tableName = TableName.valueOf("compressed_table");
        
        // Create table with compression
        TableDescriptor tableDesc = TableDescriptorBuilder
            .newBuilder(tableName)
            .setColumnFamily(ColumnFamilyDescriptorBuilder
                .newBuilder(Bytes.toBytes("cf1"))
                .setCompressionType(Compression.Algorithm.SNAPPY) // Fast compression
                .build())
            .setColumnFamily(ColumnFamilyDescriptorBuilder
                .newBuilder(Bytes.toBytes("cf2"))
                .setCompressionType(Compression.Algorithm.LZ4) // Faster compression
                .build())
            .setColumnFamily(ColumnFamilyDescriptorBuilder
                .newBuilder(Bytes.toBytes("cf3"))
                .setCompressionType(Compression.Algorithm.GZIP) // Better compression ratio
                .build())
            .build();
            
        admin.createTable(tableDesc);
    }
    
    // Modify existing table compression
    public void modifyCompression() throws IOException {
        Admin admin = connection.getAdmin();
        TableName tableName = TableName.valueOf("existing_table");
        
        // Get current table descriptor
        TableDescriptor currentDesc = admin.getDescriptor(tableName);
        
        // Create new descriptor with compression
        TableDescriptor newDesc = TableDescriptorBuilder
            .newBuilder(currentDesc)
            .modifyColumnFamily(ColumnFamilyDescriptorBuilder
                .newBuilder(currentDesc.getColumnFamily(Bytes.toBytes("cf1")))
                .setCompressionType(Compression.Algorithm.SNAPPY)
                .build())
            .build();
        
        // Apply changes
        admin.disableTable(tableName);
        admin.modifyTable(newDesc);
        admin.enableTable(tableName);
    }
    
    // Compression comparison
    public void compressionComparison() {
        /*
        Compression Algorithm Comparison:
        
        1. NONE: No compression
           - Pros: Fastest read/write, no CPU overhead
           - Cons: Largest storage size
           - Use case: High-performance scenarios with ample storage
        
        2. SNAPPY: Balanced compression
           - Pros: Good compression ratio, fast decompression
           - Cons: Moderate CPU usage
           - Use case: General purpose, recommended default
        
        3. LZ4: Fastest compression
           - Pros: Fastest compression/decompression
           - Cons: Lower compression ratio than SNAPPY
           - Use case: CPU-sensitive applications
        
        4. GZIP: Best compression ratio
           - Pros: Highest compression ratio
           - Cons: Slower compression/decompression, high CPU usage
           - Use case: Storage-constrained environments
        
        5. BZIP2: Highest compression
           - Pros: Best compression ratio
           - Cons: Slowest, highest CPU usage
           - Use case: Archival data, rarely accessed
        */
    }
}
```

### 17. What is Write-Ahead Log (WAL) and how does it work?
**Answer**: WAL ensures data durability by logging all changes before they're applied to the data store.

```java
public class WALConfiguration {
    
    // Configure WAL settings
    public void configureWAL() {
        Configuration conf = HBaseConfiguration.create();
        
        // WAL configuration
        conf.set("hbase.wal.provider", "filesystem"); // WAL provider
        conf.setLong("hbase.regionserver.hlog.blocksize", 134217728L); // 128MB blocks
        conf.setInt("hbase.regionserver.maxlogs", 32); // Max WAL files
        conf.setLong("hbase.regionserver.logroll.period", 3600000L); // 1 hour roll period
        
        // WAL compression
        conf.setBoolean("hbase.regionserver.wal.enablecompression", true);
        conf.set("hbase.regionserver.wal.compression", "snappy");
        
        // WAL durability levels
        conf.set("hbase.wal.sync.timeout", "10000"); // 10 seconds
    }
    
    // WAL durability levels
    public void walDurabilityLevels() throws IOException {
        // SKIP_WAL: Skip WAL entirely (fastest, no durability)
        Put putSkipWAL = new Put(Bytes.toBytes("row1"));
        putSkipWAL.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col1"), 
                            Bytes.toBytes("value1"));
        putSkipWAL.setDurability(Durability.SKIP_WAL);
        
        // ASYNC_WAL: Asynchronous WAL write (fast, eventual durability)
        Put putAsyncWAL = new Put(Bytes.toBytes("row2"));
        putAsyncWAL.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col1"), 
                             Bytes.toBytes("value2"));
        putAsyncWAL.setDurability(Durability.ASYNC_WAL);
        
        // SYNC_WAL: Synchronous WAL write (slower, immediate durability)
        Put putSyncWAL = new Put(Bytes.toBytes("row3"));
        putSyncWAL.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col1"), 
                            Bytes.toBytes("value3"));
        putSyncWAL.setDurability(Durability.SYNC_WAL);
        
        // FSYNC_WAL: Force sync to disk (slowest, strongest durability)
        Put putFsyncWAL = new Put(Bytes.toBytes("row4"));
        putFsyncWAL.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col1"), 
                             Bytes.toBytes("value4"));
        putFsyncWAL.setDurability(Durability.FSYNC_WAL);
    }
    
    // WAL recovery process
    public void walRecoveryProcess() {
        /*
        WAL Recovery Process:
        
        1. RegionServer failure detected
        2. HMaster assigns regions to other RegionServers
        3. New RegionServer reads WAL files
        4. Replays uncommitted operations from WAL
        5. Updates MemStore with recovered data
        6. Region becomes available for operations
        
        WAL Structure:
        - WAL Entry: Timestamp, Region, Table, Row Key, Column Family, Qualifier, Value
        - Sequence Number: Monotonically increasing number for ordering
        - WAL Key: Contains metadata about the operation
        - WAL Edit: Contains the actual data changes
        */
    }
}
```

### 18. How do you implement time-to-live (TTL) in HBase?
**Answer**: TTL automatically expires data after a specified time period.

```java
public class TTLConfiguration {
    
    // Configure TTL for column family
    public void configureTTL() throws IOException {
        Admin admin = connection.getAdmin();
        TableName tableName = TableName.valueOf("ttl_table");
        
        // Create table with TTL
        TableDescriptor tableDesc = TableDescriptorBuilder
            .newBuilder(tableName)
            .setColumnFamily(ColumnFamilyDescriptorBuilder
                .newBuilder(Bytes.toBytes("session_data"))
                .setTimeToLive(3600) // 1 hour TTL
                .setMaxVersions(1)
                .build())
            .setColumnFamily(ColumnFamilyDescriptorBuilder
                .newBuilder(Bytes.toBytes("cache_data"))
                .setTimeToLive(1800) // 30 minutes TTL
                .setMaxVersions(1)
                .build())
            .setColumnFamily(ColumnFamilyDescriptorBuilder
                .newBuilder(Bytes.toBytes("permanent_data"))
                .setTimeToLive(HConstants.FOREVER) // No TTL
                .setMaxVersions(5)
                .build())
            .build();
            
        admin.createTable(tableDesc);
    }
    
    // Modify TTL for existing table
    public void modifyTTL() throws IOException {
        Admin admin = connection.getAdmin();
        TableName tableName = TableName.valueOf("existing_table");
        
        // Get current descriptor
        TableDescriptor currentDesc = admin.getDescriptor(tableName);
        
        // Modify TTL
        TableDescriptor newDesc = TableDescriptorBuilder
            .newBuilder(currentDesc)
            .modifyColumnFamily(ColumnFamilyDescriptorBuilder
                .newBuilder(currentDesc.getColumnFamily(Bytes.toBytes("cf1")))
                .setTimeToLive(7200) // 2 hours
                .build())
            .build();
        
        admin.disableTable(tableName);
        admin.modifyTable(newDesc);
        admin.enableTable(tableName);
    }
    
    // TTL with versioning
    public void ttlWithVersioning() throws IOException {
        // Configure TTL with multiple versions
        ColumnFamilyDescriptor cfDesc = ColumnFamilyDescriptorBuilder
            .newBuilder(Bytes.toBytes("versioned_cf"))
            .setTimeToLive(86400) // 24 hours TTL
            .setMaxVersions(10) // Keep 10 versions
            .setMinVersions(2) // Keep at least 2 versions even if TTL expired
            .build();
        
        /*
        TTL Behavior with Versions:
        - TTL applies to individual cell versions
        - Expired versions are removed during compaction
        - MinVersions ensures minimum versions are kept regardless of TTL
        - MaxVersions limits total versions per cell
        */
    }
    
    // Custom TTL per cell
    public void customCellTTL() throws IOException {
        // Set custom TTL for specific cells
        long customTTL = System.currentTimeMillis() + (2 * 3600 * 1000); // 2 hours from now
        
        Put put = new Put(Bytes.toBytes("row1"));
        put.addColumn(Bytes.toBytes("cf1"), Bytes.toBytes("col1"), 
                     customTTL, Bytes.toBytes("value_with_custom_ttl"));
        
        table.put(put);
        
        /*
        Custom TTL Notes:
        - Cell-level TTL overrides column family TTL
        - Timestamp represents expiration time, not creation time
        - Useful for session data, temporary cache entries
        */
    }
    
    // TTL monitoring and cleanup
    public void ttlMonitoring() {
        /*
        TTL Cleanup Process:
        
        1. Automatic Cleanup:
           - Occurs during major compaction
           - Expired cells are removed from HFiles
           - No immediate cleanup (eventual consistency)
        
        2. Manual Cleanup:
           - Force major compaction to trigger cleanup
           - Use admin.majorCompact(tableName)
        
        3. Monitoring:
           - Check HBase metrics for expired data
           - Monitor compaction frequency
           - Verify storage reduction after cleanup
        */
    }
}
```

### 19. How do you implement secondary indexes in HBase?
**Answer**: HBase doesn't have native secondary indexes, but several approaches can provide similar functionality.

```java
public class SecondaryIndexes {
    
    // Manual secondary index implementation
    public class ManualSecondaryIndex {
        private Table mainTable;
        private Table indexTable;
        
        public ManualSecondaryIndex(Connection connection) throws IOException {
            this.mainTable = connection.getTable(TableName.valueOf("users"));
            this.indexTable = connection.getTable(TableName.valueOf("users_email_index"));
        }
        
        // Insert with index maintenance
        public void insertUser(String userId, String email, String name) throws IOException {
            // Insert into main table
            Put mainPut = new Put(Bytes.toBytes(userId));
            mainPut.addColumn(Bytes.toBytes("profile"), Bytes.toBytes("email"), 
                             Bytes.toBytes(email));
            mainPut.addColumn(Bytes.toBytes("profile"), Bytes.toBytes("name"), 
                             Bytes.toBytes(name));
            mainTable.put(mainPut);
            
            // Insert into index table (email -> userId)
            Put indexPut = new Put(Bytes.toBytes(email));
            indexPut.addColumn(Bytes.toBytes("index"), Bytes.toBytes("user_id"), 
                              Bytes.toBytes(userId));
            indexTable.put(indexPut);
        }
        
        // Query by email using index
        public String findUserByEmail(String email) throws IOException {
            // Look up userId in index table
            Get indexGet = new Get(Bytes.toBytes(email));
            Result indexResult = indexTable.get(indexGet);
            
            if (indexResult.isEmpty()) {
                return null;
            }
            
            String userId = Bytes.toString(
                indexResult.getValue(Bytes.toBytes("index"), Bytes.toBytes("user_id"))
            );
            
            // Get full user data from main table
            Get mainGet = new Get(Bytes.toBytes(userId));
            Result mainResult = mainTable.get(mainGet);
            
            return Bytes.toString(
                mainResult.getValue(Bytes.toBytes("profile"), Bytes.toBytes("name"))
            );
        }
        
        // Update with index maintenance
        public void updateUserEmail(String userId, String oldEmail, String newEmail) 
                throws IOException {
            // Update main table
            Put mainPut = new Put(Bytes.toBytes(userId));
            mainPut.addColumn(Bytes.toBytes("profile"), Bytes.toBytes("email"), 
                             Bytes.toBytes(newEmail));
            mainTable.put(mainPut);
            
            // Remove old index entry
            Delete oldIndexDelete = new Delete(Bytes.toBytes(oldEmail));
            indexTable.delete(oldIndexDelete);
            
            // Add new index entry
            Put newIndexPut = new Put(Bytes.toBytes(newEmail));
            newIndexPut.addColumn(Bytes.toBytes("index"), Bytes.toBytes("user_id"), 
                                 Bytes.toBytes(userId));
            indexTable.put(newIndexPut);
        }
    }
    
    // Phoenix secondary index (SQL layer)
    public void phoenixSecondaryIndex() throws SQLException {
        Connection phoenixConn = DriverManager.getConnection("jdbc:phoenix:localhost");
        
        // Create Phoenix view over HBase table
        String createView = """
            CREATE VIEW "users" (
                pk VARCHAR PRIMARY KEY,
                "profile"."name" VARCHAR,
                "profile"."email" VARCHAR,
                "profile"."age" INTEGER
            )
        """;
        phoenixConn.createStatement().execute(createView);
        
        // Create secondary index
        String createIndex = """
            CREATE INDEX users_email_idx ON "users"("profile"."email")
        """;
        phoenixConn.createStatement().execute(createIndex);
        
        // Query using index
        String query = """
            SELECT pk, "profile"."name" 
            FROM "users" 
            WHERE "profile"."email" = ?
        """;
        
        PreparedStatement stmt = phoenixConn.prepareStatement(query);
        stmt.setString(1, "john@example.com");
        ResultSet rs = stmt.executeQuery();
        
        while (rs.next()) {
            String userId = rs.getString(1);
            String name = rs.getString(2);
            System.out.println("User: " + userId + ", Name: " + name);
        }
    }
    
    // Coprocessor-based index
    public class IndexCoprocessor implements RegionObserver {
        
        @Override
        public void postPut(ObserverContext<RegionCoprocessorEnvironment> c, 
                           Put put, WALEdit edit, Durability durability) throws IOException {
            
            // Extract email from put operation
            byte[] email = put.get(Bytes.toBytes("profile"), Bytes.toBytes("email"))
                .get(0).getValueArray();
            
            if (email != null) {
                // Update index table
                Table indexTable = c.getEnvironment().getConnection()
                    .getTable(TableName.valueOf("users_email_index"));
                
                Put indexPut = new Put(email);
                indexPut.addColumn(Bytes.toBytes("index"), Bytes.toBytes("user_id"), 
                                  put.getRow());
                indexTable.put(indexPut);
                indexTable.close();
            }
        }
        
        @Override
        public void postDelete(ObserverContext<RegionCoprocessorEnvironment> c, 
                              Delete delete, WALEdit edit, Durability durability) 
                              throws IOException {
            
            // Get email before deletion for index cleanup
            Get get = new Get(delete.getRow());
            get.addColumn(Bytes.toBytes("profile"), Bytes.toBytes("email"));
            
            Result result = c.getEnvironment().getRegion().get(get);
            if (!result.isEmpty()) {
                byte[] email = result.getValue(Bytes.toBytes("profile"), 
                                             Bytes.toBytes("email"));
                
                if (email != null) {
                    // Remove from index table
                    Table indexTable = c.getEnvironment().getConnection()
                        .getTable(TableName.valueOf("users_email_index"));
                    
                    Delete indexDelete = new Delete(email);
                    indexTable.delete(indexDelete);
                    indexTable.close();
                }
            }
        }
    }
    
    // Global secondary index using separate table
    public class GlobalSecondaryIndex {
        
        public void createGlobalIndex() throws IOException {
            Admin admin = connection.getAdmin();
            
            // Create index table
            TableDescriptor indexTableDesc = TableDescriptorBuilder
                .newBuilder(TableName.valueOf("global_email_index"))
                .setColumnFamily(ColumnFamilyDescriptorBuilder
                    .newBuilder(Bytes.toBytes("refs"))
                    .build())
                .build();
            
            admin.createTable(indexTableDesc);
        }
        
        // Batch index update using MapReduce
        public void batchIndexUpdate() throws Exception {
            Configuration conf = HBaseConfiguration.create();
            Job job = Job.getInstance(conf, "build-secondary-index");
            
            job.setJarByClass(IndexBuilderMapper.class);
            job.setMapperClass(IndexBuilderMapper.class);
            job.setNumReduceTasks(0); // Map-only job
            
            Scan scan = new Scan();
            scan.addFamily(Bytes.toBytes("profile"));
            
            TableMapReduceUtil.initTableMapperJob(
                "users", scan, IndexBuilderMapper.class, 
                null, null, job);
            
            job.waitForCompletion(true);
        }
    }
}

// Index builder mapper for batch processing
class IndexBuilderMapper extends TableMapper<NullWritable, NullWritable> {
    private Table indexTable;
    
    @Override
    protected void setup(Context context) throws IOException {
        Configuration conf = context.getConfiguration();
        Connection connection = ConnectionFactory.createConnection(conf);
        indexTable = connection.getTable(TableName.valueOf("global_email_index"));
    }
    
    @Override
    protected void map(ImmutableBytesWritable rowKey, Result result, Context context) 
            throws IOException {
        
        byte[] email = result.getValue(Bytes.toBytes("profile"), Bytes.toBytes("email"));
        if (email != null) {
            Put indexPut = new Put(email);
            indexPut.addColumn(Bytes.toBytes("refs"), Bytes.toBytes("user_id"), 
                              rowKey.get());
            indexTable.put(indexPut);
        }
    }
    
    @Override
    protected void cleanup(Context context) throws IOException {
        if (indexTable != null) {
            indexTable.close();
        }
    }
}
```

### 20. How do you handle HBase security and authentication?
**Answer**: HBase provides multiple security mechanisms including authentication, authorization, and encryption.

```java
public class HBaseSecurity {
    
    // Kerberos authentication configuration
    public void configureKerberos() {
        Configuration conf = HBaseConfiguration.create();
        
        // Enable Kerberos authentication
        conf.set("hbase.security.authentication", "kerberos");
        conf.set("hbase.security.authorization", "true");
        
        // Kerberos principals
        conf.set("hbase.master.kerberos.principal", "hbase/_HOST@REALM.COM");
        conf.set("hbase.regionserver.kerberos.principal", "hbase/_HOST@REALM.COM");
        conf.set("hbase.zookeeper.kerberos.principal", "zookeeper/_HOST@REALM.COM");
        
        // Keytab files
        conf.set("hbase.master.keytab.file", "/etc/hbase/conf/hbase.keytab");
        conf.set("hbase.regionserver.keytab.file", "/etc/hbase/conf/hbase.keytab");
        
        // Client authentication
        System.setProperty("java.security.auth.login.config", "/etc/hbase/conf/jaas.conf");
        
        try {
            // Login using keytab
            UserGroupInformation.setConfiguration(conf);
            UserGroupInformation.loginUserFromKeytab("hbase-client@REALM.COM", 
                                                    "/etc/hbase/conf/client.keytab");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    // Authorization and permissions
    public void configureAuthorization() throws IOException {
        Admin admin = connection.getAdmin();
        
        // Grant table permissions
        admin.grant(new UserPermission("user1", 
            Permission.newBuilder(TableName.valueOf("users"))
                .withActions(Permission.Action.READ, Permission.Action.WRITE)
                .build()));
        
        // Grant column family permissions
        admin.grant(new UserPermission("user2",
            Permission.newBuilder(TableName.valueOf("users"))
                .withFamily(Bytes.toBytes("profile"))
                .withActions(Permission.Action.READ)
                .build()));
        
        // Grant global permissions
        admin.grant(new UserPermission("admin_user",
            Permission.newBuilder()
                .withActions(Permission.Action.ADMIN)
                .build()));
        
        // Revoke permissions
        admin.revoke(new UserPermission("user1",
            Permission.newBuilder(TableName.valueOf("users"))
                .withActions(Permission.Action.WRITE)
                .build()));
    }
    
    // Cell-level security (visibility labels)
    public void cellLevelSecurity() throws IOException {
        // Enable visibility labels
        Configuration conf = HBaseConfiguration.create();
        conf.set("hbase.coprocessor.master.classes", 
                "org.apache.hadoop.hbase.security.visibility.VisibilityController");
        conf.set("hbase.coprocessor.region.classes", 
                "org.apache.hadoop.hbase.security.visibility.VisibilityController");
        
        // Create table with visibility support
        TableDescriptor tableDesc = TableDescriptorBuilder
            .newBuilder(TableName.valueOf("secure_table"))
            .setColumnFamily(ColumnFamilyDescriptorBuilder.of("data"))
            .setCoprocessor("org.apache.hadoop.hbase.security.visibility.VisibilityController")
            .build();
        
        Admin admin = connection.getAdmin();
        admin.createTable(tableDesc);
        
        // Add visibility labels
        VisibilityLabelsRequest.Builder builder = VisibilityLabelsRequest.newBuilder();
        builder.addVisLabel(ByteString.copyFromUtf8("SECRET"));
        builder.addVisLabel(ByteString.copyFromUtf8("CONFIDENTIAL"));
        builder.addVisLabel(ByteString.copyFromUtf8("PUBLIC"));
        
        // Set user authorizations
        SetAuthsRequest authsRequest = SetAuthsRequest.newBuilder()
            .setUser(ByteString.copyFromUtf8("user1"))
            .addAuth(ByteString.copyFromUtf8("SECRET"))
            .addAuth(ByteString.copyFromUtf8("PUBLIC"))
            .build();
        
        // Write data with visibility labels
        Table table = connection.getTable(TableName.valueOf("secure_table"));
        
        Put secretPut = new Put(Bytes.toBytes("row1"));
        secretPut.addColumn(Bytes.toBytes("data"), Bytes.toBytes("secret_col"), 
                           Bytes.toBytes("secret_value"));
        secretPut.setCellVisibility(new CellVisibility("SECRET"));
        table.put(secretPut);
        
        Put publicPut = new Put(Bytes.toBytes("row2"));
        publicPut.addColumn(Bytes.toBytes("data"), Bytes.toBytes("public_col"), 
                           Bytes.toBytes("public_value"));
        publicPut.setCellVisibility(new CellVisibility("PUBLIC"));
        table.put(publicPut);
        
        // Read with authorizations
        Scan scan = new Scan();
        scan.setAuthorizations(new Authorizations("SECRET", "PUBLIC"));
        ResultScanner scanner = table.getScanner(scan);
        
        for (Result result : scanner) {
            // Process authorized results
        }
        scanner.close();
    }
    
    // Encryption configuration
    public void configureEncryption() throws IOException {
        // Encryption at rest
        Configuration conf = HBaseConfiguration.create();
        
        // Enable encryption
        conf.set("hbase.crypto.keyprovider", 
                "org.apache.hadoop.crypto.key.JavaKeyStoreProvider");
        conf.set("hbase.crypto.keyprovider.parameters", 
                "jceks://file/path/to/keystore.jceks");
        
        // Create encrypted table
        TableDescriptor tableDesc = TableDescriptorBuilder
            .newBuilder(TableName.valueOf("encrypted_table"))
            .setColumnFamily(ColumnFamilyDescriptorBuilder
                .newBuilder(Bytes.toBytes("encrypted_cf"))
                .setEncryptionType("AES")
                .setEncryptionKey("myEncryptionKey")
                .build())
            .build();
        
        Admin admin = connection.getAdmin();
        admin.createTable(tableDesc);
        
        // Encryption in transit (TLS/SSL)
        conf.setBoolean("hbase.ssl.enabled", true);
        conf.set("hbase.ssl.keystore.location", "/path/to/keystore.jks");
        conf.set("hbase.ssl.keystore.password", "keystore_password");
        conf.set("hbase.ssl.truststore.location", "/path/to/truststore.jks");
        conf.set("hbase.ssl.truststore.password", "truststore_password");
    }
    
    // Audit logging
    public void configureAuditLogging() {
        Configuration conf = HBaseConfiguration.create();
        
        // Enable audit logging
        conf.set("hbase.coprocessor.master.classes", 
                "org.apache.hadoop.hbase.security.access.AccessController");
        conf.set("hbase.coprocessor.region.classes", 
                "org.apache.hadoop.hbase.security.access.AccessController");
        
        // Audit log configuration
        conf.set("hbase.security.log.file", "/var/log/hbase/hbase-audit.log");
        conf.setBoolean("hbase.security.audit.log.enabled", true);
        
        /*
        Audit events logged:
        - Authentication attempts
        - Authorization decisions
        - Table operations (create, delete, alter)
        - Data access (read, write, delete)
        - Administrative actions
        */
    }
    
    // Secure client connection
    public Connection createSecureConnection() throws IOException {
        Configuration conf = HBaseConfiguration.create();
        
        // Kerberos authentication
        conf.set("hbase.security.authentication", "kerberos");
        conf.set("hadoop.security.authentication", "kerberos");
        
        // SSL/TLS encryption
        conf.setBoolean("hbase.ssl.enabled", true);
        conf.set("hbase.ssl.keystore.location", "/path/to/client-keystore.jks");
        conf.set("hbase.ssl.keystore.password", "password");
        
        // Create secure connection
        UserGroupInformation.setConfiguration(conf);
        UserGroupInformation ugi = UserGroupInformation.loginUserFromKeytabAndReturnUGI(
            "client@REALM.COM", "/path/to/client.keytab");
        
        return ugi.doAs(new PrivilegedExceptionAction<Connection>() {
            @Override
            public Connection run() throws IOException {
                return ConnectionFactory.createConnection(conf);
            }
        });
    }
}
```

---

I'll continue with the Advanced Level Questions and remaining sections in the next batch to complete the comprehensive interview questions file.
## 🔴 Advanced Level Questions

### 21. How do you design and implement a distributed counter system in HBase?
**Answer**: Distributed counters require careful design to avoid hotspotting while maintaining accuracy.

```java
public class DistributedCounter {
    
    // Sharded counter implementation
    public class ShardedCounter {
        private final int numShards;
        private final String counterName;
        private final Table counterTable;
        
        public ShardedCounter(String counterName, int numShards, Table counterTable) {
            this.counterName = counterName;
            this.numShards = numShards;
            this.counterTable = counterTable;
        }
        
        // Increment counter with random sharding
        public void increment(long delta) throws IOException {
            int shard = ThreadLocalRandom.current().nextInt(numShards);
            String rowKey = counterName + "_shard_" + String.format("%03d", shard);
            
            counterTable.incrementColumnValue(
                Bytes.toBytes(rowKey),
                Bytes.toBytes("counters"),
                Bytes.toBytes("value"),
                delta
            );
        }
        
        // Get total counter value
        public long getValue() throws IOException {
            long total = 0;
            
            // Scan all shards
            Scan scan = new Scan();
            scan.setStartRow(Bytes.toBytes(counterName + "_shard_"));
            scan.setStopRow(Bytes.toBytes(counterName + "_shard_" + "~"));
            scan.addFamily(Bytes.toBytes("counters"));
            
            ResultScanner scanner = counterTable.getScanner(scan);
            
            try {
                for (Result result : scanner) {
                    byte[] value = result.getValue(Bytes.toBytes("counters"), 
                                                 Bytes.toBytes("value"));
                    if (value != null) {
                        total += Bytes.toLong(value);
                    }
                }
            } finally {
                scanner.close();
            }
            
            return total;
        }
    }
}
```

### 22. How do you implement cross-datacenter replication in HBase?
**Answer**: HBase supports cross-datacenter replication for disaster recovery and geographic distribution.

```java
public class CrossDatacenterReplication {
    
    // Setup replication between clusters
    public void setupReplication() throws IOException {
        Admin admin = connection.getAdmin();
        
        // Add replication peer
        ReplicationPeerConfig peerConfig = ReplicationPeerConfig.newBuilder()
            .setClusterKey("zk1,zk2,zk3:2181:/hbase") // Remote cluster ZK
            .setReplicateAllUserTables(false) // Selective replication
            .build();
        
        admin.addReplicationPeer("peer1", peerConfig);
        
        // Enable replication for specific table
        TableName tableName = TableName.valueOf("replicated_table");
        admin.enableTableReplication(tableName);
    }
}
```

---

## 🏗️ Architecture & Performance

### 26. How do you optimize HBase performance for different workloads?
**Answer**: Performance optimization requires understanding workload patterns and tuning accordingly.

```java
public class PerformanceOptimization {
    
    // Read-heavy workload optimization
    public void optimizeForReads() {
        Configuration conf = HBaseConfiguration.create();
        
        // Increase block cache size
        conf.setFloat("hfile.block.cache.size", 0.4f); // 40% of heap
        
        // Enable bloom filters
        ColumnFamilyDescriptor cfDesc = ColumnFamilyDescriptorBuilder
            .newBuilder(Bytes.toBytes("cf1"))
            .setBloomFilterType(BloomType.ROW)
            .setBlockCacheEnabled(true)
            .build();
        
        // Optimize scan caching
        conf.setInt("hbase.client.scanner.caching", 1000);
        conf.setInt("hbase.client.scanner.max.result.size", 2097152); // 2MB
    }
    
    // Write-heavy workload optimization
    public void optimizeForWrites() {
        Configuration conf = HBaseConfiguration.create();
        
        // Increase MemStore size
        conf.setFloat("hbase.regionserver.global.memstore.size", 0.5f); // 50% of heap
        conf.setLong("hbase.hregion.memstore.flush.size", 268435456L); // 256MB
        
        // Optimize WAL
        conf.set("hbase.wal.provider", "asyncfs");
        conf.setBoolean("hbase.regionserver.wal.enablecompression", true);
        
        // Batch writes
        conf.setInt("hbase.client.write.buffer", 4194304); // 4MB buffer
    }
}
```

### 27. How do you handle HBase compaction strategies?
**Answer**: Compaction strategies significantly impact performance and should be tuned based on workload.

```java
public class CompactionStrategies {
    
    // Configure compaction policies
    public void configureCompactionPolicy() throws IOException {
        Admin admin = connection.getAdmin();
        TableName tableName = TableName.valueOf("my_table");
        
        TableDescriptor tableDesc = TableDescriptorBuilder
            .newBuilder(tableName)
            .setColumnFamily(ColumnFamilyDescriptorBuilder
                .newBuilder(Bytes.toBytes("cf1"))
                .setConfiguration("hbase.hstore.defaultengine.compactionpolicy.class", 
                                "org.apache.hadoop.hbase.regionserver.compactions.ExploringCompactionPolicy")
                .setConfiguration("hbase.hstore.compaction.min", "3")
                .setConfiguration("hbase.hstore.compaction.max", "10")
                .setConfiguration("hbase.hstore.compaction.ratio", "1.2")
                .build())
            .build();
        
        admin.modifyTable(tableDesc);
    }
    
    // Date-tiered compaction for time-series data
    public void configureDateTieredCompaction() throws IOException {
        Admin admin = connection.getAdmin();
        
        ColumnFamilyDescriptor cfDesc = ColumnFamilyDescriptorBuilder
            .newBuilder(Bytes.toBytes("timeseries"))
            .setConfiguration("hbase.hstore.defaultengine.compactionpolicy.class",
                            "org.apache.hadoop.hbase.regionserver.DateTieredStoreEngine")
            .setConfiguration("hbase.hstore.compaction.date.tiered.max.storefile.age.millis",
                            String.valueOf(7 * 24 * 60 * 60 * 1000L)) // 7 days
            .build();
    }
}
```

---

## 🌊 Streaming & Real-time Processing

### 28. How do you integrate HBase with Apache Kafka for real-time data ingestion?
**Answer**: Kafka-HBase integration enables real-time data streaming and storage.

```java
public class KafkaHBaseIntegration {
    
    // Kafka consumer writing to HBase
    public class KafkaToHBaseConsumer {
        private KafkaConsumer<String, String> consumer;
        private Table hbaseTable;
        
        public void processMessages() {
            Properties props = new Properties();
            props.put("bootstrap.servers", "localhost:9092");
            props.put("group.id", "hbase-consumer");
            props.put("key.deserializer", StringDeserializer.class.getName());
            props.put("value.deserializer", StringDeserializer.class.getName());
            
            consumer = new KafkaConsumer<>(props);
            consumer.subscribe(Arrays.asList("sensor-data"));
            
            while (true) {
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
                List<Put> puts = new ArrayList<>();
                
                for (ConsumerRecord<String, String> record : records) {
                    Put put = createPutFromRecord(record);
                    puts.add(put);
                    
                    // Batch every 1000 records
                    if (puts.size() >= 1000) {
                        hbaseTable.put(puts);
                        puts.clear();
                    }
                }
                
                // Insert remaining records
                if (!puts.isEmpty()) {
                    hbaseTable.put(puts);
                }
            }
        }
        
        private Put createPutFromRecord(ConsumerRecord<String, String> record) {
            // Parse JSON message
            ObjectMapper mapper = new ObjectMapper();
            JsonNode data = mapper.readTree(record.value());
            
            String deviceId = data.get("deviceId").asText();
            long timestamp = data.get("timestamp").asLong();
            
            String rowKey = deviceId + "_" + (Long.MAX_VALUE - timestamp);
            Put put = new Put(Bytes.toBytes(rowKey));
            
            // Add sensor readings
            JsonNode readings = data.get("readings");
            readings.fields().forEachRemaining(entry -> {
                put.addColumn(Bytes.toBytes("sensors"), 
                             Bytes.toBytes(entry.getKey()),
                             Bytes.toBytes(entry.getValue().asText()));
            });
            
            return put;
        }
    }
}
```

---

## 🔧 Production & Operations

### 29. How do you monitor and troubleshoot HBase in production?
**Answer**: Comprehensive monitoring and troubleshooting strategies for production HBase clusters.

```java
public class ProductionMonitoring {
    
    // JMX metrics collection
    public class HBaseMetricsCollector {
        
        public void collectRegionServerMetrics() throws IOException {
            Admin admin = connection.getAdmin();
            ClusterMetrics metrics = admin.getClusterMetrics();
            
            for (ServerMetrics serverMetrics : metrics.getLiveServerMetrics().values()) {
                System.out.println("Server: " + serverMetrics.getServerName());
                System.out.println("Request count: " + serverMetrics.getRequestCount());
                System.out.println("Read requests: " + serverMetrics.getReadRequestsCount());
                System.out.println("Write requests: " + serverMetrics.getWriteRequestsCount());
                
                // Region metrics
                for (RegionMetrics regionMetric : serverMetrics.getRegionMetrics().values()) {
                    System.out.println("Region: " + Bytes.toString(regionMetric.getRegionName()));
                    System.out.println("Store file size: " + regionMetric.getStoreFileSize());
                    System.out.println("Memstore size: " + regionMetric.getMemStoreSize());
                }
            }
        }
    }
    
    // Health checks
    public class HealthChecker {
        
        public boolean performHealthCheck() {
            try {
                // Check HMaster connectivity
                Admin admin = connection.getAdmin();
                admin.getClusterMetrics();
                
                // Check table availability
                TableName testTable = TableName.valueOf("health_check");
                if (admin.tableExists(testTable)) {
                    Table table = connection.getTable(testTable);
                    
                    // Perform read/write test
                    Put put = new Put(Bytes.toBytes("health_check_" + System.currentTimeMillis()));
                    put.addColumn(Bytes.toBytes("test"), Bytes.toBytes("status"), 
                                 Bytes.toBytes("ok"));
                    table.put(put);
                    
                    Get get = new Get(put.getRow());
                    Result result = table.get(get);
                    
                    return !result.isEmpty();
                }
                
                return true;
            } catch (Exception e) {
                System.err.println("Health check failed: " + e.getMessage());
                return false;
            }
        }
    }
}
```

---

## 🎯 Scenario-Based Questions

### 30. Design a real-time analytics system for IoT data using HBase
**Answer**: Complete IoT analytics system design with HBase as the storage layer.

```java
public class IoTAnalyticsSystem {
    
    // Data model for IoT sensors
    public class IoTDataModel {
        
        // Raw sensor data table
        // Row key: deviceId_reverseTimestamp_sensorType
        public void storeRawSensorData(String deviceId, String sensorType, 
                                     double value, long timestamp, 
                                     Map<String, String> metadata) throws IOException {
            
            String rowKey = deviceId + "_" + 
                          String.format("%019d", Long.MAX_VALUE - timestamp) + "_" + 
                          sensorType;
            
            Put put = new Put(Bytes.toBytes(rowKey));
            put.addColumn(Bytes.toBytes("readings"), Bytes.toBytes("value"), 
                         Bytes.toBytes(Double.toString(value)));
            put.addColumn(Bytes.toBytes("readings"), Bytes.toBytes("timestamp"), 
                         Bytes.toBytes(Long.toString(timestamp)));
            
            // Add metadata
            for (Map.Entry<String, String> entry : metadata.entrySet()) {
                put.addColumn(Bytes.toBytes("metadata"), Bytes.toBytes(entry.getKey()), 
                             Bytes.toBytes(entry.getValue()));
            }
            
            rawDataTable.put(put);
        }
        
        // Aggregated data table for analytics
        // Row key: deviceId_timeBucket_aggregationType
        public void storeAggregatedData(String deviceId, String aggregationType, 
                                      long timeBucket, Map<String, Double> aggregates) 
                                      throws IOException {
            
            String rowKey = deviceId + "_" + timeBucket + "_" + aggregationType;
            
            Put put = new Put(Bytes.toBytes(rowKey));
            
            for (Map.Entry<String, Double> entry : aggregates.entrySet()) {
                put.addColumn(Bytes.toBytes("aggregates"), Bytes.toBytes(entry.getKey()), 
                             Bytes.toBytes(entry.getValue().toString()));
            }
            
            put.addColumn(Bytes.toBytes("meta"), Bytes.toBytes("bucket_start"), 
                         Bytes.toBytes(Long.toString(timeBucket)));
            put.addColumn(Bytes.toBytes("meta"), Bytes.toBytes("bucket_end"), 
                         Bytes.toBytes(Long.toString(timeBucket + BUCKET_SIZE)));
            
            aggregatedDataTable.put(put);
        }
    }
    
    // Real-time query service
    public class RealTimeQueryService {
        
        public List<SensorReading> getRecentReadings(String deviceId, int minutes) 
                throws IOException {
            
            long endTime = System.currentTimeMillis();
            long startTime = endTime - (minutes * 60 * 1000);
            
            return getReadingsInTimeRange(deviceId, startTime, endTime);
        }
        
        public Map<String, Double> getAggregatedMetrics(String deviceId, 
                                                       String aggregationType, 
                                                       long timeBucket) throws IOException {
            
            String rowKey = deviceId + "_" + timeBucket + "_" + aggregationType;
            Get get = new Get(Bytes.toBytes(rowKey));
            Result result = aggregatedDataTable.get(get);
            
            Map<String, Double> metrics = new HashMap<>();
            
            if (!result.isEmpty()) {
                NavigableMap<byte[], byte[]> familyMap = 
                    result.getFamilyMap(Bytes.toBytes("aggregates"));
                
                for (Map.Entry<byte[], byte[]> entry : familyMap.entrySet()) {
                    String metricName = Bytes.toString(entry.getKey());
                    Double value = Double.parseDouble(Bytes.toString(entry.getValue()));
                    metrics.put(metricName, value);
                }
            }
            
            return metrics;
        }
    }
}
```

---

This comprehensive HBase interview questions guide covers essential concepts from basic to advanced levels, providing practical examples and real-world scenarios that data engineers encounter in production environments.