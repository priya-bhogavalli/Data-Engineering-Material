# HBase - Interview Questions

## Basic Questions

### 1. What is HBase and how does it differ from traditional RDBMS?
**Answer:** HBase is a distributed, column-oriented NoSQL database built on Hadoop HDFS. Unlike RDBMS, it provides:
- Schema-less design with column families
- Horizontal scaling across commodity hardware
- No ACID transactions across multiple rows
- Optimized for sparse data and high write throughput

### 2. Explain HBase's data model.
**Answer:** HBase data model consists of:
- **Tables**: Collections of rows
- **Row Key**: Unique identifier (sorted lexicographically)
- **Column Families**: Groups of related columns (defined at table creation)
- **Columns**: Individual data fields within families
- **Cells**: Data at row/column intersection with timestamp
- **Versions**: Multiple timestamped versions per cell

### 3. What are the main components of HBase architecture?
**Answer:**
- **HMaster**: Manages metadata, region assignments, schema changes
- **RegionServer**: Stores and serves data regions
- **Regions**: Horizontal partitions of tables
- **ZooKeeper**: Coordinates cluster state and configuration
- **HDFS**: Underlying distributed file system

## Intermediate Questions

### 4. How does HBase handle data distribution and scaling?
**Answer:** HBase uses automatic sharding:
- Tables split into regions based on row key ranges
- Regions distributed across RegionServers
- Auto-splitting when regions exceed size threshold
- Load balancing moves regions between servers
- Linear scaling by adding more RegionServers

### 5. What is a RegionServer and what does it do?
**Answer:** RegionServer is the worker node that:
- Hosts multiple regions of different tables
- Handles read/write requests for its regions
- Manages MemStore (write cache) and HFiles (storage)
- Performs compactions and region splits
- Communicates with HMaster for coordination

### 6. Explain HBase's write path.
**Answer:** HBase write process:
1. Client writes to WAL (Write-Ahead Log) for durability
2. Data written to MemStore (in-memory buffer)
3. When MemStore fills, flush to HFile on HDFS
4. Multiple HFiles compacted periodically
5. Region splits when size threshold exceeded

## Advanced Questions

### 7. How would you design row keys for optimal HBase performance?
**Answer:** Row key design principles:
```java
// Bad: Sequential keys cause hotspotting
rowkey = timestamp + userid

// Good: Distribute load with hash prefix
rowkey = hash(userid) + timestamp + userid

// Good: Reverse timestamp for recent data access
rowkey = userid + (Long.MAX_VALUE - timestamp)
```
- Avoid sequential patterns
- Distribute writes across regions
- Consider access patterns
- Keep keys reasonably short

### 8. What are HBase coprocessors and when would you use them?
**Answer:** Coprocessors are server-side processing extensions:
- **Observer**: Triggered by data events (like database triggers)
- **Endpoint**: Custom RPC services (like stored procedures)

Use cases:
- Secondary indexing
- Data aggregation
- Access control
- Data validation

```java
// Observer example
public class AuditObserver extends BaseRegionObserver {
  @Override
  public void postPut(ObserverContext<RegionCoprocessorEnvironment> e,
                      Put put, WALEdit edit, Durability durability) {
    // Log all puts for auditing
    auditLog.info("Put operation: " + put.toString());
  }
}
```

### 9. How do you handle HBase performance tuning?
**Answer:** Performance optimization strategies:
- **Schema Design**: Proper column family design
- **Row Key Design**: Avoid hotspotting
- **Region Sizing**: Optimal region size (1-10GB)
- **Compaction**: Tune major/minor compaction
- **Memory**: Configure heap and off-heap memory
- **Caching**: Block cache and Bloom filters
- **Compression**: Use appropriate compression algorithms

### 10. What are the limitations of HBase?
**Answer:**
- **No SQL**: No standard SQL interface (without Phoenix)
- **No Transactions**: No multi-row ACID transactions
- **Single Point of Failure**: HMaster dependency
- **Complex Operations**: No joins or complex queries
- **Operational Complexity**: Requires Hadoop expertise
- **Memory Requirements**: High memory usage for optimal performance