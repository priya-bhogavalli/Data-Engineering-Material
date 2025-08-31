# CockroachDB - Interview Questions

## Basic Questions

### 1. What is CockroachDB and how does it differ from traditional databases?
**Answer:** CockroachDB is a distributed SQL database that combines the benefits of traditional RDBMS (ACID transactions, SQL) with horizontal scalability and fault tolerance. Unlike traditional databases that scale vertically, CockroachDB scales horizontally across multiple nodes while maintaining strong consistency and ACID properties.

### 2. What does "NewSQL" mean in the context of CockroachDB?
**Answer:** NewSQL refers to databases that provide the scalability of NoSQL systems while maintaining the ACID properties and SQL interface of traditional relational databases. CockroachDB is NewSQL because it offers:
- Horizontal scaling like NoSQL
- ACID transactions like traditional SQL
- Standard SQL interface
- Strong consistency guarantees

### 3. How does CockroachDB achieve fault tolerance?
**Answer:** CockroachDB achieves fault tolerance through:
- **Replication**: Each data range is replicated across multiple nodes (default 3)
- **Consensus Protocol**: Uses Raft algorithm for leader election and consistency
- **Automatic Failover**: Surviving replicas elect new leaders automatically
- **Self-Healing**: Failed nodes are automatically replaced and data rebalanced

## Intermediate Questions

### 4. Explain CockroachDB's data distribution model.
**Answer:** CockroachDB uses a range-based distribution model:
- **Ranges**: Data is split into contiguous key ranges (64MB default)
- **Replicas**: Each range has multiple replicas across different nodes
- **Leaseholder**: One replica per range handles all reads and writes
- **Followers**: Other replicas receive updates and can become leaseholders
- **Automatic Splitting**: Ranges split when they grow too large
- **Rebalancing**: System automatically moves ranges to balance load

### 5. How does CockroachDB handle transactions across multiple nodes?
**Answer:** CockroachDB uses distributed transactions with:
- **Two-Phase Commit (2PC)**: Ensures atomicity across nodes
- **Transaction Coordinator**: Manages distributed transaction state
- **Write Intents**: Provisional writes that become committed or aborted
- **Timestamp Ordering**: Uses hybrid logical clocks for ordering
- **Serializable Isolation**: Strongest isolation level by default

### 6. What are the trade-offs of using CockroachDB?
**Answer:**
**Advantages:**
- Horizontal scalability
- Strong consistency
- Fault tolerance
- SQL compatibility

**Trade-offs:**
- Higher latency than single-node databases
- More complex operational overhead
- Network dependency for distributed operations
- Higher resource usage due to replication

## Advanced Questions

### 7. How would you optimize query performance in CockroachDB?
**Answer:**
- **Indexing**: Create appropriate secondary indexes
- **Query Planning**: Use EXPLAIN to analyze query plans
- **Data Locality**: Use geo-partitioning for regional data
- **Connection Pooling**: Reuse database connections
- **Batch Operations**: Group multiple operations together
- **Schema Design**: Design tables to minimize cross-node joins
- **Monitoring**: Use built-in metrics to identify bottlenecks

### 8. Explain CockroachDB's approach to multi-region deployments.
**Answer:**
```sql
-- Create a multi-region database
CREATE DATABASE myapp PRIMARY REGION 'us-east1' 
REGIONS 'us-west1', 'europe-west1';

-- Create regional tables
CREATE TABLE users (
    id UUID PRIMARY KEY,
    region STRING,
    name STRING
) LOCALITY REGIONAL BY ROW ON region;

-- Create global tables
CREATE TABLE products (
    id UUID PRIMARY KEY,
    name STRING,
    price DECIMAL
) LOCALITY GLOBAL;
```

Features:
- **Regional Tables**: Data stays in specific regions
- **Global Tables**: Replicated across all regions
- **Follow-the-Workload**: Data moves closer to access patterns
- **Geo-Partitioning**: Compliance with data residency requirements

### 9. How does CockroachDB handle schema changes in a distributed environment?
**Answer:** CockroachDB uses online schema changes:
- **Non-Blocking**: Schema changes don't block reads/writes
- **Gradual Rollout**: Changes applied incrementally across nodes
- **Backfill Process**: Data backfilled in background for new columns/indexes
- **Rollback Safety**: Changes can be rolled back if issues occur
- **Version Gates**: Ensures all nodes support new schema before activation

### 10. What monitoring and observability features does CockroachDB provide?
**Answer:**
- **Admin UI**: Built-in web interface for cluster monitoring
- **Metrics**: Comprehensive metrics for performance and health
- **SQL Activity**: Query performance and execution statistics
- **Node Status**: Individual node health and resource usage
- **Alerting**: Integration with external monitoring systems
- **Distributed Tracing**: Track queries across multiple nodes
- **Logs**: Structured logging for debugging and auditing

Example monitoring query:
```sql
-- Check cluster health
SELECT node_id, address, is_live, is_available 
FROM crdb_internal.gossip_liveness;

-- Monitor query performance
SELECT query, count, avg_latency 
FROM crdb_internal.statement_statistics 
ORDER BY avg_latency DESC LIMIT 10;
```