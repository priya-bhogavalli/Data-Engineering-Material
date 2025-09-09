
### Q1: What is Apache Hadoop and what are its core components?
**Answer:**
Apache Hadoop is an open-source framework for distributed storage and processing of large datasets across clusters of computers. It's designed to scale from single servers to thousands of machines.

**Core Components:**
- **HDFS (Hadoop Distributed File System)**: Distributed storage system
- **MapReduce**: Programming model for processing large datasets
- **YARN (Yet Another Resource Negotiator)**: Resource management and job scheduling
- **Hadoop Common**: Common utilities and libraries

**Key Features:**
- Fault tolerance through data replication
- Horizontal scalability
- Cost-effective storage for big data
- Schema-on-read approach

### Q2: Explain the difference between Hadoop 1.x and Hadoop 2.x
**Answer:**
**Hadoop 1.x:**
- Only MapReduce for processing
- JobTracker as single point of failure
- Limited to batch processing
- Resource management tied to MapReduce

**Hadoop 2.x:**
- Introduced YARN for resource management
- Supports multiple processing engines (Spark, Tez, etc.)
- Better fault tolerance with ResourceManager HA
- Improved scalability and performance
- Federation support for NameNode

### Q3: What are the advantages and disadvantages of Hadoop?
**Answer:**
**Advantages:**
- Cost-effective for large-scale data storage
- Horizontal scalability
- Fault tolerance through replication
- Open-source with large community
- Handles structured and unstructured data
- Schema-on-read flexibility

**Disadvantages:**
- High latency (not suitable for real-time processing)
- Complex setup and maintenance
- Not efficient for small datasets
- Limited support for iterative algorithms
- Security challenges in early versions

---

## 💾 HDFS (Hadoop Distributed File System)

### Q4: Explain HDFS architecture and its components
**Answer:**
**HDFS Architecture:**
- **NameNode**: Master node storing metadata
- **DataNodes**: Worker nodes storing actual data blocks
- **Secondary NameNode**: Assists NameNode with checkpointing

**Key Concepts:**
- Files split into blocks (default 128MB in Hadoop 2.x)
- Each block replicated 3 times by default
- NameNode maintains file system namespace
- DataNodes send heartbeats to NameNode

```
Client → NameNode (metadata) → DataNodes (data blocks)
```

### Q5: What is the default block size in HDFS and why?
**Answer:**
**Default Block Size:**
- Hadoop 1.x: 64MB
- Hadoop 2.x+: 128MB

**Reasons for Large Block Size:**
- Minimizes seek time
- Reduces metadata overhead on NameNode
- Efficient for large file processing
- Better network utilization
- Optimal for MapReduce processing

**Trade-offs:**
- Large blocks: Better for big files, wasteful for small files
- Small blocks: More metadata overhead, increased NameNode memory usage

### Q6: Explain HDFS read and write operations
**Answer:**
**HDFS Write Process:**
1. Client contacts NameNode for file creation
2. NameNode checks permissions and creates metadata
3. Client receives list of DataNodes for first block
4. Client writes to first DataNode in pipeline
5. Data replicated to other DataNodes in pipeline
6. Process repeats for subsequent blocks

**HDFS Read Process:**
1. Client contacts NameNode for file location
2. NameNode returns list of DataNodes with blocks
3. Client reads directly from nearest DataNode
4. If DataNode fails, client tries next replica

### Q7: What is NameNode and what happens if it fails?
**Answer:**
**NameNode:**
- Master daemon managing file system namespace
- Stores metadata in memory for fast access
- Maintains edit logs and fsimage files
- Single point of failure in Hadoop 1.x

**NameNode Failure Impact:**
- Entire cluster becomes inaccessible
- No new files can be created
- Existing data becomes unreachable

**Solutions:**
- **Secondary NameNode**: Periodic checkpointing (not failover)
- **NameNode HA**: Active/Standby configuration with shared storage
- **Federation**: Multiple NameNodes for different namespaces

### Q8: Explain HDFS Federation
**Answer:**
**HDFS Federation:**
Multiple independent NameNodes managing different portions of the namespace.

**Benefits:**
- Horizontal scaling of NameNode
- Namespace isolation
- Better performance
- Fault isolation

**Architecture:**
```
Namespace1 → NameNode1 → DataNodes (Block Pool 1)
Namespace2 → NameNode2 → DataNodes (Block Pool 2)
```

**Use Cases:**
- Large clusters with multiple applications
- Different departments with separate namespaces
- Improved scalability beyond single NameNode limits

---

## 🔄 MapReduce

### Q9: Explain MapReduce programming model
**Answer:**
**MapReduce Phases:**
1. **Map Phase**: Process input data and emit key-value pairs
2. **Shuffle & Sort**: Group and sort intermediate data
3. **Reduce Phase**: Process grouped data and produce final output

**Example - Word Count:**
```java
// Map Function
map(String line) {
    for (String word : line.split(" ")) {
        emit(word, 1);
    }
}

// Reduce Function
reduce(String word, List<Integer> counts) {
    int sum = 0;
    for (int count : counts) {
        sum += count;
    }
    emit(word, sum);
}
```

### Q10: What are the different phases in MapReduce job execution?
**Answer:**
**MapReduce Job Execution Phases:**

1. **Input Split**: Divide input into logical splits
2. **Map Phase**: Execute map tasks on splits
3. **Combiner** (optional): Local aggregation
4. **Partition**: Determine which reducer gets which keys
5. **Shuffle**: Transfer map outputs to reducers
6. **Sort**: Sort data by key for each reducer
7. **Reduce Phase**: Execute reduce tasks
8. **Output**: Write final results to HDFS

**Data Flow:**
```
Input → Split → Map → Combine → Partition → Shuffle → Sort → Reduce → Output
```

### Q11: What is the role of JobTracker and TaskTracker?
**Answer:**
**JobTracker (Hadoop 1.x):**
- Master daemon for job scheduling
- Monitors TaskTrackers and job progress
- Handles job submission and resource allocation
- Single point of failure

**TaskTracker (Hadoop 1.x):**
- Slave daemon running on worker nodes
- Executes map and reduce tasks
- Reports progress to JobTracker
- Manages local task execution

**Limitations:**
- JobTracker bottleneck for large clusters
- Fixed slot allocation (map/reduce slots)
- Poor resource utilization

**Replaced by YARN in Hadoop 2.x**

### Q12: Explain Combiner in MapReduce
**Answer:**
**Combiner:**
Local aggregation function running on mapper nodes before shuffle phase.

**Purpose:**
- Reduce network traffic
- Improve job performance
- Pre-aggregate data locally

**Requirements:**
- Must be associative and commutative
- Same interface as Reducer
- Optional component

**Example:**
```java
// Word Count - Combiner same as Reducer
public class WordCountCombiner extends Reducer<Text, IntWritable, Text, IntWritable> {
    public void reduce(Text key, Iterable<IntWritable> values, Context context) {
        int sum = 0;
        for (IntWritable value : values) {
            sum += value.get();
        }
        context.write(key, new IntWritable(sum));
    }
}
```

---

## 🎛️ YARN (Yet Another Resource Negotiator)

### Q13: What is YARN and how does it differ from MapReduce 1.0?
**Answer:**
**YARN (Hadoop 2.x):**
Resource management layer separating resource management from application logic.

**Key Components:**
- **ResourceManager**: Global resource scheduler
- **NodeManager**: Per-node resource manager
- **ApplicationMaster**: Per-application resource negotiator
- **Container**: Resource allocation unit

**Differences from MapReduce 1.0:**
| Aspect | MapReduce 1.0 | YARN |
|--------|---------------|------|
| Resource Management | JobTracker | ResourceManager |
| Task Execution | TaskTracker | NodeManager |
| Scalability | Limited (~4000 nodes) | Higher (~10000+ nodes) |
| Multi-tenancy | No | Yes |
| Processing Types | Only MapReduce | Multiple (Spark, Tez, etc.) |

### Q14: Explain YARN architecture and workflow
**Answer:**
**YARN Architecture:**
```
Client → ResourceManager → NodeManager → Container → ApplicationMaster
```

**Workflow:**
1. Client submits application to ResourceManager
2. ResourceManager allocates container for ApplicationMaster
3. ApplicationMaster registers with ResourceManager
4. ApplicationMaster requests resources for tasks
5. ResourceManager allocates containers on NodeManagers
6. ApplicationMaster launches tasks in containers
7. Tasks report progress to ApplicationMaster
8. ApplicationMaster reports to ResourceManager

**Benefits:**
- Better resource utilization
- Support for multiple processing frameworks
- Improved fault tolerance
- Enhanced scalability

### Q15: What are the different schedulers in YARN?
**Answer:**
**YARN Schedulers:**

1. **FIFO Scheduler**
   - First-in-first-out job execution
   - Simple but not suitable for shared clusters
   - No resource sharing between applications

2. **Capacity Scheduler**
   - Hierarchical queues with guaranteed capacity
   - Resource sharing within queues
   - Preemption support
   - Good for multi-tenant environments

3. **Fair Scheduler**
   - Fair sharing of resources among applications
   - Dynamic resource allocation
   - Preemption for fairness
   - Suitable for interactive workloads

**Configuration Example:**
```xml
<property>
    <name>yarn.resourcemanager.scheduler.class</name>
    <value>org.apache.hadoop.yarn.server.resourcemanager.scheduler.capacity.CapacityScheduler</value>
</property>
```

---

## 🔧 Hadoop Ecosystem

### Q16: Explain the Hadoop ecosystem and its components
**Answer:**
**Core Hadoop Ecosystem:**

**Data Storage:**
- **HDFS**: Distributed file system
- **HBase**: NoSQL database on HDFS
- **Kudu**: Columnar storage for analytics

**Data Processing:**
- **MapReduce**: Batch processing framework
- **Spark**: In-memory processing engine
- **Tez**: Directed acyclic graph framework
- **Storm**: Real-time stream processing

**Data Access:**
- **Hive**: SQL-like query language
- **Pig**: High-level scripting language
- **Impala**: Real-time SQL queries
- **Drill**: Schema-free SQL query engine

**Data Integration:**
- **Sqoop**: RDBMS to Hadoop data transfer
- **Flume**: Log data collection
- **Kafka**: Distributed streaming platform

**Coordination & Management:**
- **ZooKeeper**: Coordination service
- **Oozie**: Workflow scheduler
- **Ambari**: Cluster management
- **YARN**: Resource management

### Q17: What is the difference between Hive and Pig?
**Answer:**
**Apache Hive:**
- SQL-like query language (HiveQL)
- Schema-on-read data warehouse
- Better for analysts familiar with SQL
- Declarative language
- Automatic optimization

**Apache Pig:**
- High-level scripting language (Pig Latin)
- Procedural data flow language
- Better for developers and data engineers
- More control over data processing
- Manual optimization required

**Comparison:**
| Aspect | Hive | Pig |
|--------|------|-----|
| Language | SQL-like (HiveQL) | Scripting (Pig Latin) |
| Learning Curve | Easy for SQL users | Moderate |
| Optimization | Automatic | Manual |
| Use Case | Data warehousing | ETL processing |
| Schema | Required | Optional |

### Q18: Explain Sqoop and its use cases
**Answer:**
**Apache Sqoop:**
Tool for transferring data between Hadoop and relational databases.

**Key Features:**
- Bulk data transfer
- Parallel import/export
- Incremental imports
- Compression support
- Integration with Hive/HBase

**Import Process:**
```bash
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --target-dir /user/data/customers \
  --num-mappers 4
```

**Export Process:**
```bash
sqoop export \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers_export \
  --export-dir /user/data/customers
```

**Use Cases:**
- Data migration to Hadoop
- ETL processes
- Data synchronization
- Backup and archival

---

## ⚡ Performance & Optimization

### Q19: How do you optimize MapReduce job performance?
**Answer:**
**MapReduce Optimization Strategies:**

**1. Input Optimization:**
- Use appropriate input formats
- Optimize block size for data
- Minimize small files
- Use compression

**2. Map Phase Optimization:**
- Increase map tasks for better parallelism
- Use combiners to reduce shuffle data
- Optimize map output compression
- Tune buffer sizes

**3. Reduce Phase Optimization:**
- Balance reducer workload
- Use appropriate number of reducers
- Optimize sort buffer size
- Enable reduce-side joins when appropriate

**4. Configuration Tuning:**
```xml
<!-- Increase heap size -->
<property>
    <name>mapreduce.map.java.opts</name>
    <value>-Xmx2048m</value>
</property>

<!-- Enable compression -->
<property>
    <name>mapreduce.map.output.compress</name>
    <value>true</value>
</property>

<!-- Tune buffer size -->
<property>
    <name>mapreduce.task.io.sort.mb</name>
    <value>256</value>
</property>
```

### Q20: What are the best practices for HDFS performance?
**Answer:**
**HDFS Performance Best Practices:**

**1. Block Size Optimization:**
- Use larger blocks (128MB+) for big files
- Consider workload patterns
- Balance metadata overhead

**2. Replication Strategy:**
- Default replication factor: 3
- Adjust based on criticality
- Consider rack awareness

**3. DataNode Configuration:**
- Distribute DataNodes across racks
- Use multiple disks per DataNode
- Configure appropriate heap sizes

**4. Network Optimization:**
- Use high-bandwidth networks
- Implement rack awareness
- Optimize network topology

**5. File Management:**
- Avoid small files
- Use sequence files for small data
- Implement file archiving strategies
- Regular cleanup of temporary files

**Configuration Example:**
```xml
<property>
    <name>dfs.blocksize</name>
    <value>268435456</value> <!-- 256MB -->
</property>

<property>
    <name>dfs.replication</name>
    <value>3</value>
</property>
```

---

## 🔒 Security & Administration

### Q21: What are the security features in Hadoop?
**Answer:**
**Hadoop Security Features:**

**1. Authentication:**
- Kerberos integration
- LDAP/Active Directory support
- Token-based authentication

**2. Authorization:**
- HDFS permissions (POSIX-like)
- Access Control Lists (ACLs)
- Ranger for fine-grained policies

**3. Encryption:**
- Data at rest encryption
- Data in transit encryption
- Transparent Data Encryption (TDE)

**4. Auditing:**
- Comprehensive audit logs
- Integration with SIEM systems
- Compliance reporting

**Security Configuration:**
```xml
<!-- Enable security -->
<property>
    <name>hadoop.security.authentication</name>
    <value>kerberos</value>
</property>

<!-- Enable authorization -->
<property>
    <name>hadoop.security.authorization</name>
    <value>true</value>
</property>
```

### Q22: How do you monitor Hadoop cluster health?
**Answer:**
**Hadoop Monitoring Approaches:**

**1. Native Web UIs:**
- NameNode UI (port 9870)
- ResourceManager UI (port 8088)
- DataNode UIs
- Job History Server

**2. Command Line Tools:**
```bash
# Check cluster health
hdfs dfsadmin -report

# Check HDFS status
hdfs fsck /

# Monitor YARN applications
yarn application -list

# Check node status
yarn node -list
```

**3. Monitoring Tools:**
- **Ambari**: Cluster management and monitoring
- **Cloudera Manager**: Enterprise monitoring
- **Ganglia**: Distributed monitoring system
- **Nagios**: Infrastructure monitoring

**4. Key Metrics:**
- HDFS utilization and health
- DataNode availability
- Job success/failure rates
- Resource utilization
- Network and disk I/O

---

## 🔧 Troubleshooting

### Q23: How do you troubleshoot common Hadoop issues?
**Answer:**
**Common Issues and Solutions:**

**1. NameNode Issues:**
- **Safe Mode**: `hdfs dfsadmin -safemode leave`
- **Metadata Corruption**: Restore from backup
- **Out of Memory**: Increase heap size

**2. DataNode Issues:**
- **DataNode Not Starting**: Check disk space and permissions
- **Block Corruption**: `hdfs fsck -delete-corrupted`
- **Network Issues**: Verify connectivity and DNS

**3. Job Failures:**
- **Out of Memory**: Increase container memory
- **Slow Performance**: Check data skew and resource allocation
- **Task Failures**: Review task logs and error messages

**4. YARN Issues:**
- **Resource Shortage**: Adjust queue configurations
- **ApplicationMaster Failures**: Check AM logs
- **Container Issues**: Verify NodeManager health

**Troubleshooting Commands:**
```bash
# Check HDFS health
hdfs fsck /

# View job logs
yarn logs -applicationId application_id

# Check cluster status
hdfs dfsadmin -report

# Monitor resource usage
yarn top
```

### Q24: What are the common causes of MapReduce job failures?
**Answer:**
**Common MapReduce Job Failure Causes:**

**1. Resource Issues:**
- Insufficient memory allocation
- Container memory limits exceeded
- Disk space shortage

**2. Data Issues:**
- Input data corruption
- Schema mismatches
- Missing input files

**3. Code Issues:**
- Runtime exceptions
- Infinite loops
- Memory leaks

**4. Configuration Issues:**
- Incorrect parameter settings
- Classpath problems
- Version incompatibilities

**5. Infrastructure Issues:**
- Network failures
- Hardware failures
- DataNode unavailability

**Debugging Approach:**
1. Check application logs
2. Review task attempt logs
3. Verify input data integrity
4. Validate configuration settings
5. Monitor resource utilization

---

## 🌟 Real-world Scenarios

### Q25: Design a Hadoop solution for processing web logs
**Answer:**
**Web Log Processing Solution:**

**Requirements:**
- Process 100GB+ daily web logs
- Extract user behavior patterns
- Generate daily/hourly reports
- Store results for analytics

**Architecture:**
```
Web Servers → Flume → HDFS → MapReduce/Spark → Hive → BI Tools
```

**Implementation Steps:**

1. **Data Ingestion:**
```bash
# Flume configuration for log collection
agent.sources.r1.type = spooldir
agent.sources.r1.spoolDir = /var/log/apache
agent.sinks.k1.type = hdfs
agent.sinks.k1.hdfs.path = /data/weblogs/%Y/%m/%d
```

2. **Data Processing:**
```java
// MapReduce job for log analysis
public class WebLogAnalyzer {
    public static class LogMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
        public void map(LongWritable key, Text value, Context context) {
            // Parse log entry and extract required fields
            String[] fields = value.toString().split(" ");
            String ip = fields[0];
            String url = fields[6];
            context.write(new Text(ip + "," + url), new IntWritable(1));
        }
    }
}
```

3. **Data Storage:**
```sql
-- Hive table for processed logs
CREATE TABLE web_logs (
    ip_address STRING,
    url STRING,
    timestamp STRING,
    status_code INT,
    bytes_sent BIGINT
) PARTITIONED BY (date_partition STRING)
STORED AS PARQUET;
```

### Q26: How would you migrate from traditional RDBMS to Hadoop?
**Answer:**
**RDBMS to Hadoop Migration Strategy:**

**Phase 1: Assessment**
- Analyze current data volume and growth
- Identify data types and access patterns
- Evaluate existing ETL processes
- Assess query complexity and frequency

**Phase 2: Architecture Design**
```
RDBMS → Sqoop → HDFS → Processing Layer → Analytics Layer
```

**Phase 3: Implementation**

1. **Data Migration:**
```bash
# Incremental data import
sqoop import \
  --connect jdbc:oracle:thin:@server:1521:db \
  --table SALES \
  --incremental append \
  --check-column CREATED_DATE \
  --last-value '2023-01-01'
```

2. **Schema Design:**
```sql
-- Hive external table
CREATE EXTERNAL TABLE sales_data (
    sale_id BIGINT,
    customer_id BIGINT,
    product_id BIGINT,
    sale_amount DECIMAL(10,2),
    sale_date DATE
) PARTITIONED BY (year INT, month INT)
STORED AS PARQUET
LOCATION '/data/sales/';
```

3. **ETL Transformation:**
- Convert stored procedures to MapReduce/Spark jobs
- Implement data quality checks
- Create automated workflows with Oozie

**Phase 4: Validation & Optimization**
- Data quality validation
- Performance benchmarking
- Query optimization
- User training and documentation

---

## 📚 Additional Resources

### Recommended Reading
- "Hadoop: The Definitive Guide" by Tom White
- "MapReduce Design Patterns" by Donald Miner
- Apache Hadoop Official Documentation

### Hands-on Practice
- Cloudera Quickstart VM
- Hortonworks Sandbox
- AWS EMR
- Google Cloud Dataproc

### Certifications
- Cloudera Certified Developer for Apache Hadoop (CCDH)
- Hortonworks Certified Developer (HDPCD)
- MapR Certified Hadoop Developer

---

*This comprehensive guide covers essential Hadoop interview questions. Practice with real datasets and hands-on exercises to reinforce your understanding.*