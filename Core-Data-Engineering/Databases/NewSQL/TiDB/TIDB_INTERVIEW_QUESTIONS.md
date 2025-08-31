# TiDB - Interview Questions

## Basic Questions

### 1. What is TiDB and what makes it unique?
**Answer:** TiDB is an open-source, distributed SQL database that supports HTAP (Hybrid Transactional/Analytical Processing) workloads. It's unique because it combines MySQL compatibility with horizontal scalability and provides both row-based (TiKV) and columnar (TiFlash) storage in a single system.

### 2. Explain TiDB's HTAP architecture.
**Answer:** TiDB's HTAP architecture consists of:
- **TiKV**: Row-based storage for OLTP workloads
- **TiFlash**: Columnar storage for OLAP workloads  
- **Real-time sync**: Automatic data replication between stores
- **Unified SQL**: Single interface for both transactional and analytical queries

### 3. What are the main components of TiDB?
**Answer:**
- **TiDB Server**: Stateless SQL layer with MySQL compatibility
- **TiKV**: Distributed key-value storage engine
- **PD**: Placement Driver for metadata and scheduling
- **TiFlash**: Columnar storage for analytics

## Intermediate Questions

### 4. How does TiDB handle distributed transactions?
**Answer:** TiDB uses a two-phase commit protocol with:
- **Optimistic concurrency**: Default transaction model
- **Pessimistic mode**: Available for MySQL compatibility
- **Snapshot isolation**: Default isolation level
- **Automatic retry**: Handles transaction conflicts

### 5. What is the difference between optimistic and pessimistic transaction modes in TiDB?
**Answer:**
- **Optimistic**: Reads without locks, validates at commit, retries on conflicts
- **Pessimistic**: Acquires locks during execution, similar to MySQL behavior
- **Use cases**: Optimistic for low-conflict workloads, pessimistic for high-conflict

### 6. How does TiDB achieve high availability?
**Answer:**
- **Raft consensus**: Each region replicated using Raft protocol
- **Automatic failover**: Leader election when nodes fail
- **Multi-AZ deployment**: Replicas across availability zones
- **Self-healing**: Automatic recovery and rebalancing

## Advanced Questions

### 7. How would you optimize analytical queries in TiDB?
**Answer:**
```sql
-- Use TiFlash for analytical queries
SELECT /*+ READ_FROM_STORAGE(TIFLASH[table_name]) */ 
  region, COUNT(*), AVG(amount)
FROM sales 
WHERE date >= '2023-01-01'
GROUP BY region;

-- Create TiFlash replicas
ALTER TABLE sales SET TIFLASH REPLICA 1;
```

### 8. Explain TiDB's data distribution and sharding model.
**Answer:**
- **Regions**: Data split into 96MB regions by default
- **Auto-sharding**: Automatic partitioning based on key ranges
- **Raft groups**: Each region forms a Raft group
- **Rebalancing**: PD automatically balances regions across nodes

### 9. How would you migrate from MySQL to TiDB?
**Answer:**
- **Assessment**: Analyze MySQL schema and queries
- **Compatibility**: Check for unsupported features
- **Migration tools**: Use TiDB Data Migration (DM) or Dumpling
- **Testing**: Validate functionality and performance
- **Cutover**: Plan minimal downtime migration strategy

### 10. What monitoring and troubleshooting tools does TiDB provide?
**Answer:**
- **TiDB Dashboard**: Web-based cluster monitoring
- **Grafana**: Pre-built dashboards for metrics
- **Prometheus**: Metrics collection and alerting
- **TiUP**: Cluster deployment and management
- **Slow query log**: Identify performance issues