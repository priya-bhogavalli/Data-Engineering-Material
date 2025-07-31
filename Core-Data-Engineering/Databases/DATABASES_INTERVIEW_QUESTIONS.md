# Database Interview Questions for Data Engineering

## Basic Level (0-2 years)

### 1. What is the difference between SQL and NoSQL databases?
**Answer:**
- **SQL Databases (RDBMS)**:
  - Structured data with fixed schema
  - ACID compliance
  - Vertical scaling
  - Examples: PostgreSQL, MySQL, Oracle
- **NoSQL Databases**:
  - Flexible schema
  - Horizontal scaling
  - Eventually consistent
  - Types: Document, Key-Value, Column-family, Graph

### 2. Explain ACID properties in databases.
**Answer:**
- **Atomicity**: All operations in a transaction succeed or fail together
- **Consistency**: Database remains in valid state after transactions
- **Isolation**: Concurrent transactions don't interfere with each other
- **Durability**: Committed changes persist even after system failure

### 3. What are database indexes and why are they important?
**Answer:**
Indexes are data structures that improve query performance by creating shortcuts to data.
- **Benefits**: Faster SELECT queries, efficient sorting
- **Drawbacks**: Slower INSERT/UPDATE/DELETE, additional storage
- **Types**: B-tree, Hash, Bitmap, Partial

```sql
-- Create index
CREATE INDEX idx_customer_email ON customers(email);

-- Composite index
CREATE INDEX idx_order_date_status ON orders(order_date, status);
```

## Intermediate Level (2-5 years)

### 4. Explain different types of database joins with examples.
**Answer:**
```sql
-- INNER JOIN: Returns matching records from both tables
SELECT c.name, o.order_date
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;

-- LEFT JOIN: All records from left table, matching from right
SELECT c.name, o.order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;

-- RIGHT JOIN: All records from right table, matching from left
SELECT c.name, o.order_date
FROM customers c
RIGHT JOIN orders o ON c.customer_id = o.customer_id;

-- FULL OUTER JOIN: All records from both tables
SELECT c.name, o.order_date
FROM customers c
FULL OUTER JOIN orders o ON c.customer_id = o.customer_id;
```

### 5. What is database normalization and denormalization?
**Answer:**
**Normalization**: Process of organizing data to reduce redundancy
- **1NF**: Atomic values, no repeating groups
- **2NF**: 1NF + no partial dependencies
- **3NF**: 2NF + no transitive dependencies

**Denormalization**: Intentionally introducing redundancy for performance
- Used in data warehouses
- Improves read performance
- Increases storage requirements

### 6. Explain different isolation levels in databases.
**Answer:**
- **READ UNCOMMITTED**: Lowest isolation, dirty reads possible
- **READ COMMITTED**: Prevents dirty reads
- **REPEATABLE READ**: Prevents dirty and non-repeatable reads
- **SERIALIZABLE**: Highest isolation, prevents all phenomena

```sql
-- Set isolation level
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

## Advanced Level (5+ years)

### 7. How would you design a database for high availability and disaster recovery?
**Answer:**
**High Availability Strategies:**
- **Master-Slave Replication**: Read replicas for load distribution
- **Master-Master Replication**: Multiple write nodes
- **Clustering**: Shared storage with multiple nodes
- **Load Balancing**: Distribute connections across nodes

**Disaster Recovery:**
- **Backup Strategies**: Full, incremental, differential backups
- **Point-in-Time Recovery**: Transaction log backups
- **Geographic Replication**: Cross-region data replication
- **RTO/RPO Planning**: Recovery time and data loss objectives

```python
# Example backup strategy
def backup_strategy():
    # Full backup weekly
    schedule_full_backup(frequency="weekly", day="sunday")
    
    # Incremental backup daily
    schedule_incremental_backup(frequency="daily")
    
    # Transaction log backup every 15 minutes
    schedule_log_backup(frequency="15min")
    
    # Cross-region replication
    setup_geo_replication(
        primary_region="us-east-1",
        secondary_region="us-west-2",
        replication_lag="5min"
    )
```

### 8. Explain database sharding and its challenges.
**Answer:**
**Sharding**: Horizontal partitioning across multiple database instances

**Sharding Strategies:**
- **Range-based**: Partition by value ranges
- **Hash-based**: Use hash function to distribute data
- **Directory-based**: Lookup service for shard location

**Challenges:**
- **Cross-shard queries**: Complex joins across shards
- **Rebalancing**: Moving data when adding/removing shards
- **Hotspots**: Uneven data distribution
- **Consistency**: Maintaining ACID across shards

```python
class DatabaseSharding:
    def __init__(self, shard_count):
        self.shard_count = shard_count
        self.shards = [f"shard_{i}" for i in range(shard_count)]
    
    def get_shard(self, key):
        """Hash-based sharding."""
        import hashlib
        hash_value = int(hashlib.md5(str(key).encode()).hexdigest(), 16)
        return self.shards[hash_value % self.shard_count]
    
    def execute_query(self, query, shard_key=None):
        if shard_key:
            # Single shard query
            shard = self.get_shard(shard_key)
            return self.execute_on_shard(query, shard)
        else:
            # Cross-shard query
            results = []
            for shard in self.shards:
                result = self.execute_on_shard(query, shard)
                results.extend(result)
            return self.merge_results(results)
```

### 9. How do you handle database performance optimization?
**Answer:**
**Query Optimization:**
- **Execution Plan Analysis**: Use EXPLAIN to understand query execution
- **Index Optimization**: Create appropriate indexes
- **Query Rewriting**: Optimize SQL structure

**Database Tuning:**
- **Memory Configuration**: Buffer pools, cache sizes
- **I/O Optimization**: Storage configuration, file placement
- **Connection Pooling**: Manage database connections efficiently

```sql
-- Analyze query performance
EXPLAIN (ANALYZE, BUFFERS) 
SELECT c.name, COUNT(o.order_id)
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.created_date >= '2024-01-01'
GROUP BY c.name;

-- Create covering index
CREATE INDEX idx_customer_orders_covering 
ON customers(created_date) 
INCLUDE (customer_id, name);
```

### 10. Explain CAP theorem and its implications for distributed databases.
**Answer:**
**CAP Theorem**: In a distributed system, you can only guarantee two of:
- **Consistency**: All nodes see the same data simultaneously
- **Availability**: System remains operational
- **Partition Tolerance**: System continues despite network failures

**Database Classifications:**
- **CP Systems**: MongoDB, Redis Cluster (sacrifice availability)
- **AP Systems**: Cassandra, DynamoDB (sacrifice consistency)
- **CA Systems**: Traditional RDBMS (not truly distributed)

**Practical Implications:**
```python
# Example: Handling network partitions
class DistributedDatabase:
    def __init__(self, consistency_level="eventual"):
        self.consistency_level = consistency_level
        self.nodes = []
    
    def write_data(self, key, value):
        if self.consistency_level == "strong":
            # CP: Wait for all nodes to confirm
            return self.write_to_all_nodes(key, value)
        else:
            # AP: Write to available nodes
            return self.write_to_available_nodes(key, value)
    
    def read_data(self, key):
        if self.consistency_level == "strong":
            # Read from majority of nodes
            return self.read_with_quorum(key)
        else:
            # Read from any available node
            return self.read_from_any_node(key)
```

### 11. How would you implement a multi-tenant database architecture?
**Answer:**
**Approaches:**
1. **Separate Databases**: Complete isolation per tenant
2. **Shared Database, Separate Schemas**: Schema-level isolation
3. **Shared Database, Shared Schema**: Row-level isolation

**Implementation Example:**
```sql
-- Row-level security approach
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    customer_id INT,
    amount DECIMAL(10,2),
    order_date DATE
);

-- Create policy for tenant isolation
CREATE POLICY tenant_isolation ON orders
    FOR ALL TO application_role
    USING (tenant_id = current_setting('app.tenant_id')::UUID);

-- Enable row-level security
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
```

```python
# Application-level tenant handling
class MultiTenantDatabase:
    def __init__(self):
        self.connection_pool = {}
    
    def get_connection(self, tenant_id):
        if tenant_id not in self.connection_pool:
            # Create tenant-specific connection
            conn = create_connection()
            conn.execute(f"SET app.tenant_id = '{tenant_id}'")
            self.connection_pool[tenant_id] = conn
        return self.connection_pool[tenant_id]
    
    def execute_query(self, tenant_id, query):
        conn = self.get_connection(tenant_id)
        return conn.execute(query)
```

These questions cover the breadth of database knowledge required for data engineering roles, from basic concepts to advanced distributed systems design.