# Apache Cassandra Interview Questions

## Table of Contents

1. [Basic Cassandra Questions](#basic-cassandra-questions)
2. [Architecture & Data Model](#architecture--data-model)
3. [Data Modeling](#data-modeling)
4. [Consistency & Replication](#consistency--replication)
5. [Performance & Optimization](#performance--optimization)
6. [Operations & Maintenance](#operations--maintenance)
7. [Security & Monitoring](#security--monitoring)
8. [Scenario-Based Questions](#scenario-based-questions)

---

## Basic Cassandra Questions

### 1. What is Apache Cassandra and what are its key characteristics?
**Answer:**
Apache Cassandra is a distributed NoSQL database designed to handle large amounts of data across many commodity servers.

**Key Characteristics:**
- **Distributed**: No single point of failure, peer-to-peer architecture
- **Scalable**: Linear scalability by adding more nodes
- **High Availability**: Designed for 99.99% uptime
- **Fault Tolerant**: Handles node failures gracefully
- **Tunable Consistency**: Configurable consistency levels
- **Column-Family**: Wide-column store data model

### 2. How does Cassandra differ from relational databases?
**Answer:**
- **Schema**: Flexible schema vs. rigid schema
- **ACID**: Eventually consistent vs. ACID compliant
- **Scaling**: Horizontal scaling vs. vertical scaling
- **Joins**: No joins vs. complex join operations
- **CAP Theorem**: AP (Availability + Partition tolerance) vs. CA
- **Data Model**: Column-family vs. relational tables

### 3. What are the main use cases for Cassandra?
**Answer:**
- **Time-series Data**: IoT sensors, metrics, logs
- **Real-time Analytics**: User activity tracking, recommendations
- **Messaging**: Chat applications, notification systems
- **Content Management**: Media storage, content delivery
- **Financial Services**: Fraud detection, transaction processing
- **Gaming**: Player data, leaderboards, session management

### 4. Explain Cassandra's position in the CAP theorem.
**Answer:**
Cassandra chooses **Availability** and **Partition tolerance** over Consistency:
- **Availability**: System remains operational during node failures
- **Partition Tolerance**: Continues to operate despite network partitions
- **Eventual Consistency**: Data becomes consistent over time
- **Tunable**: Can adjust consistency levels per operation

### 5. What is the difference between Cassandra and other NoSQL databases?
**Answer:**
**vs. MongoDB:**
- Cassandra: Column-family, AP system, linear scaling
- MongoDB: Document store, CP system, master-slave architecture

**vs. HBase:**
- Cassandra: Peer-to-peer, no single point of failure
- HBase: Master-slave architecture, depends on HDFS

**vs. DynamoDB:**
- Cassandra: Open source, self-managed
- DynamoDB: Managed service, proprietary

## Architecture & Data Model

### 6. Explain Cassandra's ring architecture.
**Answer:**
- **Ring Topology**: Nodes arranged in a logical ring
- **Consistent Hashing**: Data distributed using hash values
- **Token Ranges**: Each node responsible for a range of tokens
- **No Master**: All nodes are equal, no single point of failure
- **Gossip Protocol**: Nodes communicate cluster state via gossip

### 7. What are the key components of Cassandra architecture?
**Answer:**
- **Node**: Individual Cassandra instance
- **Cluster**: Collection of nodes
- **Data Center**: Logical grouping of nodes
- **Rack**: Physical grouping within data center
- **Keyspace**: Top-level namespace (like database)
- **Column Family/Table**: Container for data (like table)

### 8. How does data partitioning work in Cassandra?
**Answer:**
- **Partition Key**: Determines which node stores the data
- **Consistent Hashing**: Maps partition keys to token ranges
- **Virtual Nodes (vnodes)**: Each physical node owns multiple token ranges
- **Replication**: Data replicated to multiple nodes based on replication factor
- **Partitioner**: Algorithm that converts partition key to token

### 9. What are virtual nodes (vnodes) and their benefits?
**Answer:**
Virtual nodes allow each physical node to own multiple token ranges:
- **Better Load Distribution**: More even data distribution
- **Faster Bootstrapping**: New nodes get data from multiple sources
- **Improved Fault Tolerance**: Failure impact spread across more nodes
- **Easier Operations**: Simplified cluster management
- **Default**: 256 vnodes per physical node by default

### 10. Explain Cassandra's data model hierarchy.
**Answer:**
```
Cluster → Keyspace → Table → Partition → Row → Column
```
- **Cluster**: Entire Cassandra deployment
- **Keyspace**: Namespace with replication settings
- **Table**: Column family with defined schema
- **Partition**: Group of rows with same partition key
- **Row**: Individual record identified by primary key
- **Column**: Name-value pair with timestamp

## Data Modeling

### 11. What is a primary key in Cassandra and its components?
**Answer:**
Primary key consists of:
- **Partition Key**: Determines data distribution (required)
- **Clustering Columns**: Determines sort order within partition (optional)

```sql
CREATE TABLE user_events (
    user_id UUID,           -- Partition key
    event_time TIMESTAMP,   -- Clustering column
    event_type TEXT,        -- Clustering column
    data TEXT,
    PRIMARY KEY (user_id, event_time, event_type)
);
```

### 12. What are the principles of Cassandra data modeling?
**Answer:**
1. **Query-Driven Design**: Model based on query patterns, not entities
2. **Denormalization**: Duplicate data to avoid joins
3. **One Table Per Query**: Each query should ideally use one table
4. **Minimize Partitions**: Keep related data in same partition when possible
5. **Avoid Large Partitions**: Keep partitions under 100MB
6. **Leverage Clustering**: Use clustering columns for sorting and filtering

### 13. How do you handle one-to-many relationships in Cassandra?
**Answer:**
**Option 1: Clustering Columns**
```sql
-- Orders table
CREATE TABLE orders_by_user (
    user_id UUID,
    order_date TIMESTAMP,
    order_id UUID,
    total DECIMAL,
    PRIMARY KEY (user_id, order_date, order_id)
);
```

**Option 2: Collection Types**
```sql
-- User with order IDs
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    name TEXT,
    order_ids SET<UUID>
);
```

### 14. What are collection types in Cassandra?
**Answer:**
- **Set**: Unordered collection of unique values
- **List**: Ordered collection allowing duplicates
- **Map**: Key-value pairs

```sql
CREATE TABLE user_profile (
    user_id UUID PRIMARY KEY,
    tags SET<TEXT>,           -- Set of tags
    scores LIST<INT>,         -- List of scores
    preferences MAP<TEXT, TEXT> -- Key-value preferences
);
```

### 15. How do you model time-series data in Cassandra?
**Answer:**
```sql
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
- Use time-based partition keys to distribute data
- Include time components in partition key for even distribution
- Use clustering columns for time-based sorting

## Consistency & Replication

### 16. What are consistency levels in Cassandra?
**Answer:**
**Write Consistency:**
- **ONE**: Write to one replica
- **QUORUM**: Write to majority of replicas
- **ALL**: Write to all replicas
- **LOCAL_QUORUM**: Majority in local data center

**Read Consistency:**
- **ONE**: Read from one replica
- **QUORUM**: Read from majority of replicas
- **ALL**: Read from all replicas
- **LOCAL_ONE**: Read from local data center

### 17. How does replication work in Cassandra?
**Answer:**
- **Replication Factor**: Number of copies of each piece of data
- **Replication Strategy**: How replicas are distributed
  - **SimpleStrategy**: Single data center
  - **NetworkTopologyStrategy**: Multiple data centers
- **Coordinator Node**: Handles read/write requests
- **Replica Nodes**: Store copies of the data

### 18. What is eventual consistency and how does Cassandra achieve it?
**Answer:**
Eventual consistency means all replicas will eventually have the same data:
- **Anti-entropy Repair**: Background process to sync replicas
- **Read Repair**: Fixes inconsistencies during read operations
- **Hinted Handoff**: Stores writes for temporarily unavailable nodes
- **Merkle Trees**: Used during repair to identify differences

### 19. Explain the concept of quorum in Cassandra.
**Answer:**
Quorum = (Replication Factor / 2) + 1
- **Purpose**: Ensures strong consistency when needed
- **Read + Write Quorum**: Guarantees consistency
- **Example**: RF=3, Quorum=2
- **Trade-off**: Higher consistency vs. lower availability

### 20. What is read repair and when does it occur?
**Answer:**
Read repair fixes inconsistencies during read operations:
- **Foreground**: Synchronous repair during read (read_repair_chance)
- **Background**: Asynchronous repair after read (dclocal_read_repair_chance)
- **Process**: Coordinator compares responses from replicas
- **Automatic**: Triggered when inconsistencies detected

## Performance & Optimization

### 21. How do you optimize Cassandra performance?
**Answer:**
**Data Modeling:**
- Design for query patterns
- Avoid large partitions
- Use appropriate clustering order

**Hardware:**
- Use SSDs for better I/O performance
- Sufficient RAM for caching
- Network bandwidth for replication

**Configuration:**
- Tune JVM heap size
- Configure compaction strategies
- Optimize cache settings

### 22. What are compaction strategies in Cassandra?
**Answer:**
- **SizeTieredCompactionStrategy (STCS)**: Default, good for write-heavy workloads
- **LeveledCompactionStrategy (LCS)**: Better for read-heavy workloads
- **TimeWindowCompactionStrategy (TWCS)**: Optimal for time-series data
- **DateTieredCompactionStrategy (DTCS)**: Deprecated, replaced by TWCS

### 23. How do you handle large partitions in Cassandra?
**Answer:**
- **Identify**: Use nodetool tablehistograms to find large partitions
- **Redesign**: Change partition key to distribute data better
- **Bucketing**: Add time or hash components to partition key
- **Monitoring**: Set up alerts for partition size thresholds
- **Mitigation**: Use pagination for large partition reads

### 24. What caching mechanisms does Cassandra provide?
**Answer:**
- **Row Cache**: Caches entire rows in memory
- **Key Cache**: Caches partition key locations
- **Counter Cache**: Caches counter values
- **Chunk Cache**: Caches compressed data chunks
- **OS Page Cache**: Operating system level caching

### 25. How do you monitor Cassandra performance?
**Answer:**
**Key Metrics:**
- **Latency**: Read/write response times
- **Throughput**: Operations per second
- **Compaction**: Pending compactions
- **Memory**: Heap usage, GC metrics
- **Disk**: I/O utilization, space usage

**Tools:**
- **nodetool**: Built-in monitoring commands
- **JMX**: Java Management Extensions
- **DataStax OpsCenter**: Commercial monitoring solution
- **Prometheus + Grafana**: Open source monitoring stack

## Operations & Maintenance

### 26. How do you add a new node to a Cassandra cluster?
**Answer:**
1. **Install Cassandra**: Set up Cassandra on new node
2. **Configure**: Update cassandra.yaml with cluster settings
3. **Bootstrap**: Start node, it will automatically join cluster
4. **Stream Data**: Node receives data based on token assignment
5. **Verify**: Check cluster status with nodetool status
6. **Cleanup**: Run nodetool cleanup on existing nodes

### 27. What is the process for removing a node from Cassandra?
**Answer:**
**Planned Removal (Decommission):**
```bash
nodetool decommission
```
- Streams data to other nodes
- Updates token assignments
- Graceful removal

**Unplanned Removal (Remove):**
```bash
nodetool removenode <node-id>
```
- For failed nodes that can't be restarted
- Requires manual intervention

### 28. How do you perform backups in Cassandra?
**Answer:**
**Snapshot Backup:**
```bash
nodetool snapshot keyspace_name
```
- Creates hard links to SSTable files
- Point-in-time backup
- Minimal performance impact

**Incremental Backup:**
- Enable incremental_backups in cassandra.yaml
- Automatically backs up new SSTables
- Requires more storage space

### 29. What is repair in Cassandra and when should you run it?
**Answer:**
Repair ensures data consistency across replicas:
```bash
nodetool repair keyspace_name
```
- **Full Repair**: Compares all replicas
- **Incremental Repair**: Only repairs changed data
- **Frequency**: Run within gc_grace_seconds (default 10 days)
- **Types**: Primary range repair vs. full repair

### 30. How do you handle node failures in Cassandra?
**Answer:**
**Temporary Failure:**
- **Hinted Handoff**: Stores writes for failed node
- **Read Repair**: Fixes inconsistencies on reads
- **Automatic Recovery**: Node catches up when restored

**Permanent Failure:**
- **Replace Node**: Bootstrap replacement with same token
- **Remove Node**: Use nodetool removenode
- **Restore from Backup**: If data recovery needed

## Security & Monitoring

### 31. What security features does Cassandra provide?
**Answer:**
- **Authentication**: Internal authentication or LDAP integration
- **Authorization**: Role-based access control (RBAC)
- **Encryption**: SSL/TLS for client-server and inter-node communication
- **Audit Logging**: Track database access and operations
- **Network Security**: Configure firewall rules and network isolation

### 32. How do you implement role-based access control in Cassandra?
**Answer:**
```sql
-- Create role
CREATE ROLE data_analyst WITH PASSWORD = 'password' AND LOGIN = true;

-- Grant permissions
GRANT SELECT ON keyspace.table TO data_analyst;
GRANT MODIFY ON keyspace.table TO data_engineer;

-- Create role hierarchy
CREATE ROLE admin WITH SUPERUSER = true;
GRANT data_analyst TO admin;
```

### 33. What are the key configuration files in Cassandra?
**Answer:**
- **cassandra.yaml**: Main configuration file
- **cassandra-env.sh**: JVM and environment settings
- **logback.xml**: Logging configuration
- **cassandra-rackdc.properties**: Data center and rack information
- **jvm.options**: JVM-specific options (Cassandra 3.0+)

## Scenario-Based Questions

### 34. You're building a social media feed. How would you model it in Cassandra?
**Answer:**
```sql
-- User timeline (pull model)
CREATE TABLE user_timeline (
    user_id UUID,
    post_time TIMESTAMP,
    post_id UUID,
    author_id UUID,
    content TEXT,
    PRIMARY KEY (user_id, post_time, post_id)
) WITH CLUSTERING ORDER BY (post_time DESC);

-- User posts
CREATE TABLE posts_by_user (
    author_id UUID,
    post_time TIMESTAMP,
    post_id UUID,
    content TEXT,
    PRIMARY KEY (author_id, post_time, post_id)
) WITH CLUSTERING ORDER BY (post_time DESC);
```

### 35. Your Cassandra cluster is experiencing high latency. How do you troubleshoot?
**Answer:**
1. **Check System Resources**: CPU, memory, disk I/O
2. **Analyze GC Logs**: Look for long garbage collection pauses
3. **Review Compaction**: Check for pending compactions
4. **Examine Query Patterns**: Identify expensive queries
5. **Check Network**: Inter-node communication latency
6. **Review Data Model**: Look for large partitions or hot spots
7. **Monitor Metrics**: Use nodetool and JMX metrics

### 36. How would you migrate data from a relational database to Cassandra?
**Answer:**
1. **Analyze Current Schema**: Understand relationships and query patterns
2. **Design Cassandra Model**: Create query-driven data model
3. **Data Transformation**: Write ETL scripts to transform data
4. **Migration Strategy**: Choose between big bang or gradual migration
5. **Validation**: Verify data integrity and completeness
6. **Application Changes**: Update application to use Cassandra drivers
7. **Performance Testing**: Validate performance meets requirements
8. **Monitoring**: Set up monitoring and alerting

### 37. You need to implement a distributed counter system. How would you design it?
**Answer:**
```sql
CREATE TABLE page_views (
    page_id UUID,
    view_count COUNTER,
    PRIMARY KEY (page_id)
);

-- Increment counter
UPDATE page_views SET view_count = view_count + 1 WHERE page_id = ?;
```
**Considerations:**
- Use counter data type for atomic increments
- Understand eventual consistency of counters
- Consider using time-based bucketing for high-frequency counters
- Implement counter repair strategies

---

## Key Takeaways for Interviews

1. **Architecture**: Understand distributed, peer-to-peer architecture
2. **Data Modeling**: Master query-driven design principles
3. **Consistency**: Know consistency levels and replication strategies
4. **Performance**: Focus on optimization techniques and monitoring
5. **Operations**: Understand cluster management and maintenance procedures
6. **CAP Theorem**: Know Cassandra's position (AP) and implications
7. **Use Cases**: Be familiar with time-series and high-scale scenarios
8. **Troubleshooting**: Practice identifying and resolving common issues