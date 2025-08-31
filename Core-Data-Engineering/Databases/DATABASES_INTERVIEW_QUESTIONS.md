# 🗄️ Database Interview Questions for Data Engineering

## 📋 Table of Contents
1. [Basic Level (0-2 years)](#basic-level-0-2-years)
2. [Intermediate Level (2-5 years)](#intermediate-level-2-5-years)
3. [Advanced Level (5+ years)](#advanced-level-5-years)
4. [Conceptual & Theoretical Questions](#conceptual--theoretical-questions)
5. [Architecture & Design Questions](#architecture--design-questions)
6. [Performance & Optimization Questions](#performance--optimization-questions)
7. [Security & Compliance Questions](#security--compliance-questions)
8. [Data Modeling & Warehousing Questions](#data-modeling--warehousing-questions)
9. [Migration & Integration Questions](#migration--integration-questions)

---

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

---

## 🎯 **Conceptual & Theoretical Questions**

### 12. What are the different database storage engines and their use cases?
**Answer:**
**Storage Engine Types:**
- **InnoDB (MySQL)**: ACID compliant, row-level locking, foreign keys
- **MyISAM (MySQL)**: Fast reads, table-level locking, no transactions
- **Memory/HEAP**: In-memory storage, volatile data
- **Archive**: Compressed storage for historical data
- **LSM-Tree**: Write-optimized (Cassandra, RocksDB)
- **B-Tree**: Read-optimized traditional approach

### 13. Explain database connection pooling and its importance
**Answer:**
Connection pooling manages a cache of database connections to improve performance and resource utilization.

**Benefits:**
- Reduces connection overhead
- Controls resource usage
- Improves application scalability
- Handles connection failures gracefully

**Configuration Considerations:**
- Pool size based on concurrent users
- Connection timeout settings
- Idle connection cleanup
- Health check mechanisms

### 14. What is database partitioning and when should you use it?
**Answer:**
**Partitioning Types:**
- **Horizontal**: Split rows across partitions (sharding)
- **Vertical**: Split columns across partitions
- **Range**: Partition by value ranges
- **Hash**: Partition by hash function
- **List**: Partition by discrete values

**Use Cases:**
- Large tables (>100GB)
- Time-series data
- Geographically distributed data
- Improved query performance
- Parallel processing

### 15. How do database triggers work and what are their use cases?
**Answer:**
Triggers are special stored procedures that automatically execute in response to database events.

**Types:**
- **BEFORE**: Execute before the triggering event
- **AFTER**: Execute after the triggering event
- **INSTEAD OF**: Replace the triggering event (views)

**Use Cases:**
- Audit logging
- Data validation
- Automatic calculations
- Maintaining derived data
- Business rule enforcement

---

## 🏗️ **Architecture & Design Questions**

### 16. How would you design a database for a social media platform?
**Answer:**
**Key Requirements:**
- Billions of users and posts
- Real-time feeds
- High read/write throughput
- Global distribution

**Architecture Approach:**
```sql
-- User management (SQL for consistency)
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP
);

-- Posts (NoSQL for scalability)
-- Document structure in MongoDB/DynamoDB
{
    "post_id": "12345",
    "user_id": "67890",
    "content": "Hello world!",
    "timestamp": "2024-01-15T10:30:00Z",
    "likes": 150,
    "comments": [
        {
            "user_id": "11111",
            "content": "Great post!",
            "timestamp": "2024-01-15T10:35:00Z"
        }
    ]
}

-- Relationships (Graph database - Neo4j)
CREATE (u1:User {id: 12345, name: 'Alice'})
CREATE (u2:User {id: 67890, name: 'Bob'})
CREATE (u1)-[:FOLLOWS]->(u2)
```

**Scaling Strategy:**
- Shard users by geographic region
- Cache popular content in Redis
- Use CDN for media files
- Implement read replicas for feeds

### 17. Design a database schema for an e-commerce platform
**Answer:**
```sql
-- Core entities with proper relationships
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_category_id INT REFERENCES categories(category_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category_id INT REFERENCES categories(category_id),
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_status VARCHAR(20) DEFAULT 'pending',
    total_amount DECIMAL(10,2),
    shipping_address JSONB,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) GENERATED ALWAYS AS (quantity * unit_price) STORED
);

-- Indexes for performance
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_order_items_order ON order_items(order_id);
```

### 18. How would you handle real-time analytics in a database system?
**Answer:**
**Architecture Components:**
- **OLTP System**: Handle transactions
- **Change Data Capture (CDC)**: Track data changes
- **Stream Processing**: Real-time transformations
- **OLAP System**: Analytics queries

**Implementation:**
```python
# Real-time analytics pipeline
class RealTimeAnalytics:
    def __init__(self):
        self.kafka_producer = KafkaProducer()
        self.redis_client = Redis()
        self.clickhouse_client = ClickHouseClient()
    
    def capture_transaction(self, transaction_data):
        # Store in OLTP database
        self.store_transaction(transaction_data)
        
        # Send to stream for real-time processing
        self.kafka_producer.send('transactions', transaction_data)
        
        # Update real-time metrics in Redis
        self.update_realtime_metrics(transaction_data)
    
    def process_stream(self, transaction):
        # Calculate real-time aggregations
        hourly_sales = self.calculate_hourly_sales(transaction)
        product_popularity = self.update_product_metrics(transaction)
        
        # Store in analytical database
        self.clickhouse_client.insert({
            'timestamp': transaction['timestamp'],
            'sales_amount': transaction['amount'],
            'product_id': transaction['product_id'],
            'customer_segment': self.get_customer_segment(transaction['customer_id'])
        })
```

---

## 🔍 **Performance & Optimization Questions**

### 19. How do you identify and resolve database performance bottlenecks?
**Answer:**
**Identification Methods:**
- **Query Performance Monitoring**: Slow query logs
- **Resource Monitoring**: CPU, memory, I/O usage
- **Lock Analysis**: Blocking and deadlock detection
- **Index Usage Analysis**: Unused or inefficient indexes

**Resolution Strategies:**
```sql
-- 1. Identify slow queries
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;

-- 2. Analyze query execution
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT * FROM large_table WHERE indexed_column = 'value';

-- 3. Optimize with proper indexing
CREATE INDEX CONCURRENTLY idx_optimized 
ON large_table(indexed_column) 
WHERE active = true;

-- 4. Partition large tables
CREATE TABLE sales_2024 PARTITION OF sales
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

### 20. Explain database caching strategies
**Answer:**
**Caching Levels:**
- **Database Buffer Pool**: In-memory page cache
- **Query Result Cache**: Cache query results
- **Application Cache**: Redis, Memcached
- **CDN Cache**: Geographic content distribution

**Cache Patterns:**
```python
class DatabaseCache:
    def __init__(self):
        self.redis = Redis()
        self.db = Database()
    
    def cache_aside(self, key):
        """Cache-aside pattern"""
        # Try cache first
        cached_data = self.redis.get(key)
        if cached_data:
            return json.loads(cached_data)
        
        # Fetch from database
        data = self.db.query(f"SELECT * FROM table WHERE id = {key}")
        
        # Store in cache
        self.redis.setex(key, 3600, json.dumps(data))
        return data
    
    def write_through(self, key, data):
        """Write-through pattern"""
        # Write to database first
        self.db.insert(data)
        
        # Then update cache
        self.redis.setex(key, 3600, json.dumps(data))
    
    def write_behind(self, key, data):
        """Write-behind pattern"""
        # Write to cache immediately
        self.redis.setex(key, 3600, json.dumps(data))
        
        # Queue for async database write
        self.queue_for_db_write(data)
```

---

## 🛡️ **Security & Compliance Questions**

### 21. How do you implement database security best practices?
**Answer:**
**Security Layers:**
- **Network Security**: VPC, firewalls, SSL/TLS
- **Authentication**: Strong passwords, MFA, certificates
- **Authorization**: Role-based access control (RBAC)
- **Encryption**: At-rest and in-transit
- **Auditing**: Access logs, change tracking

**Implementation:**
```sql
-- 1. Create roles with minimal privileges
CREATE ROLE data_analyst;
GRANT SELECT ON sales_data TO data_analyst;
GRANT SELECT ON customer_summary TO data_analyst;

-- 2. Row-level security
CREATE POLICY customer_data_policy ON customers
    FOR ALL TO application_user
    USING (customer_id = current_setting('app.current_customer_id')::INT);

-- 3. Encrypt sensitive columns
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    email VARCHAR(100),
    ssn_encrypted BYTEA  -- Store encrypted SSN
);

-- 4. Audit trail
CREATE TABLE audit_log (
    log_id SERIAL PRIMARY KEY,
    table_name VARCHAR(50),
    operation VARCHAR(10),
    user_name VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    old_values JSONB,
    new_values JSONB
);
```

### 22. How do you handle data privacy and GDPR compliance?
**Answer:**
**GDPR Requirements:**
- **Right to Access**: Provide user's data
- **Right to Rectification**: Correct inaccurate data
- **Right to Erasure**: Delete user's data
- **Data Portability**: Export user's data
- **Privacy by Design**: Built-in privacy protection

**Implementation:**
```python
class GDPRCompliance:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def export_user_data(self, user_id):
        """Right to data portability"""
        user_data = {}
        
        # Collect data from all relevant tables
        tables = ['users', 'orders', 'preferences', 'activity_log']
        for table in tables:
            query = f"SELECT * FROM {table} WHERE user_id = %s"
            user_data[table] = self.db.execute(query, (user_id,))
        
        return self.anonymize_sensitive_data(user_data)
    
    def delete_user_data(self, user_id):
        """Right to erasure (Right to be forgotten)"""
        try:
            self.db.begin_transaction()
            
            # Delete from all tables
            delete_queries = [
                "DELETE FROM activity_log WHERE user_id = %s",
                "DELETE FROM preferences WHERE user_id = %s",
                "UPDATE orders SET customer_id = NULL WHERE customer_id = %s",
                "DELETE FROM users WHERE user_id = %s"
            ]
            
            for query in delete_queries:
                self.db.execute(query, (user_id,))
            
            # Log the deletion for compliance
            self.log_gdpr_action('DELETE', user_id)
            
            self.db.commit_transaction()
            
        except Exception as e:
            self.db.rollback_transaction()
            raise e
    
    def anonymize_user_data(self, user_id):
        """Alternative to deletion - anonymization"""
        anonymized_data = {
            'email': f'anonymized_{user_id}@deleted.com',
            'name': 'ANONYMIZED',
            'phone': None,
            'address': None
        }
        
        query = """
            UPDATE users 
            SET email = %s, name = %s, phone = %s, address = %s,
                anonymized_at = CURRENT_TIMESTAMP
            WHERE user_id = %s
        """
        
        self.db.execute(query, (*anonymized_data.values(), user_id))
```

---

## 📊 **Data Modeling & Warehousing Questions**

### 23. Explain dimensional modeling concepts (Star vs Snowflake schema)
**Answer:**
**Star Schema:**
- Central fact table surrounded by dimension tables
- Denormalized dimensions
- Better query performance
- More storage space

**Snowflake Schema:**
- Normalized dimension tables
- Reduced storage space
- More complex queries
- Better for data integrity

```sql
-- Star Schema Example
CREATE TABLE fact_sales (
    sale_id SERIAL PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    product_key INT REFERENCES dim_product(product_key),
    customer_key INT REFERENCES dim_customer(customer_key),
    store_key INT REFERENCES dim_store(store_key),
    quantity INT,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2)
);

CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(50),
    product_name VARCHAR(200),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100)
);

-- Snowflake Schema Example (normalized)
CREATE TABLE dim_product_normalized (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(50),
    product_name VARCHAR(200),
    category_key INT REFERENCES dim_category(category_key),
    brand_key INT REFERENCES dim_brand(brand_key)
);

CREATE TABLE dim_category (
    category_key SERIAL PRIMARY KEY,
    category_name VARCHAR(100),
    category_description TEXT
);
```

### 24. How do you handle slowly changing dimensions (SCD)?
**Answer:**
**SCD Types:**
- **Type 0**: No changes allowed
- **Type 1**: Overwrite old values
- **Type 2**: Create new record with version
- **Type 3**: Add new column for changes
- **Type 4**: Separate history table

**SCD Type 2 Implementation:**
```sql
-- SCD Type 2 with effective dates
CREATE TABLE dim_customer_scd2 (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(50),
    customer_name VARCHAR(100),
    address VARCHAR(200),
    phone VARCHAR(20),
    effective_date DATE,
    expiry_date DATE,
    is_current BOOLEAN DEFAULT TRUE,
    version_number INT DEFAULT 1
);

-- Procedure to handle SCD Type 2 updates
CREATE OR REPLACE FUNCTION update_customer_scd2(
    p_customer_id VARCHAR(50),
    p_new_name VARCHAR(100),
    p_new_address VARCHAR(200),
    p_new_phone VARCHAR(20)
)
RETURNS VOID AS $$
BEGIN
    -- Close current record
    UPDATE dim_customer_scd2
    SET expiry_date = CURRENT_DATE - 1,
        is_current = FALSE
    WHERE customer_id = p_customer_id
      AND is_current = TRUE;
    
    -- Insert new record
    INSERT INTO dim_customer_scd2 (
        customer_id, customer_name, address, phone,
        effective_date, expiry_date, is_current, version_number
    )
    SELECT 
        p_customer_id, p_new_name, p_new_address, p_new_phone,
        CURRENT_DATE, '9999-12-31', TRUE,
        COALESCE(MAX(version_number), 0) + 1
    FROM dim_customer_scd2
    WHERE customer_id = p_customer_id;
END;
$$ LANGUAGE plpgsql;
```

---

## 🔄 **Migration & Integration Questions**

### 25. How do you plan and execute a database migration?
**Answer:**
**Migration Planning:**
1. **Assessment**: Current system analysis
2. **Strategy**: Big bang vs phased approach
3. **Testing**: Comprehensive testing plan
4. **Rollback**: Contingency planning
5. **Monitoring**: Performance validation

**Migration Execution:**
```python
class DatabaseMigration:
    def __init__(self, source_db, target_db):
        self.source_db = source_db
        self.target_db = target_db
        self.migration_log = []
    
    def execute_migration(self):
        try:
            # 1. Pre-migration validation
            self.validate_source_data()
            
            # 2. Schema migration
            self.migrate_schema()
            
            # 3. Data migration with batching
            self.migrate_data_in_batches()
            
            # 4. Index and constraint creation
            self.create_indexes_and_constraints()
            
            # 5. Data validation
            self.validate_migrated_data()
            
            # 6. Performance testing
            self.run_performance_tests()
            
        except Exception as e:
            self.log_error(f"Migration failed: {e}")
            self.rollback_migration()
            raise
    
    def migrate_data_in_batches(self, batch_size=10000):
        tables = self.get_migration_tables()
        
        for table in tables:
            total_rows = self.source_db.count(table)
            batches = (total_rows // batch_size) + 1
            
            for batch_num in range(batches):
                offset = batch_num * batch_size
                
                # Extract batch from source
                batch_data = self.source_db.select(
                    table, limit=batch_size, offset=offset
                )
                
                # Transform data if needed
                transformed_data = self.transform_batch(batch_data, table)
                
                # Load into target
                self.target_db.bulk_insert(table, transformed_data)
                
                # Log progress
                self.log_progress(table, batch_num + 1, batches)
```

These comprehensive questions cover the full spectrum of database knowledge required for data engineering roles, from fundamental concepts to advanced distributed systems and real-world scenarios.