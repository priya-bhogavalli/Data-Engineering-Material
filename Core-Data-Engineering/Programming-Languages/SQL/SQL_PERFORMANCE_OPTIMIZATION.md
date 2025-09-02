# SQL Performance Optimization for Data Engineering

## 📋 Table of Contents

1. [Index Optimization](#index-optimization)
2. [Query Optimization](#query-optimization)
3. [Partitioning Strategies](#partitioning-strategies)
4. [Memory and Configuration](#memory-and-configuration)
5. [Advanced Optimization Techniques](#advanced-optimization-techniques)
6. [Monitoring and Analysis](#monitoring-and-analysis)
7. [Best Practices](#best-practices)

---

## Overview

SQL performance optimization is critical for data engineering workflows, especially when dealing with large datasets and complex analytical queries. This guide provides comprehensive strategies and techniques to optimize SQL performance across different database systems.

**Key Performance Factors:**
- **Indexing Strategy**: Proper index design and maintenance
- **Query Structure**: Efficient query writing and optimization
- **Data Organization**: Partitioning and data layout
- **System Configuration**: Memory and parameter tuning
- **Hardware Resources**: CPU, memory, and storage optimization

---

## Index Optimization

### Understanding Index Types

Indexes are data structures that improve query performance by providing fast access paths to table data. Choosing the right index type is crucial for optimal performance.

### Index Types and Usage

**B-tree Indexes (Default)**
- **Best for**: Equality and range queries, sorting operations
- **Use cases**: Primary keys, foreign keys, frequently queried columns
- **Performance**: Excellent for `=`, `<`, `>`, `BETWEEN`, `ORDER BY`

```sql
-- B-tree indexes (default) - most common and versatile
CREATE INDEX idx_customer_id ON orders(customer_id);
CREATE INDEX idx_order_date ON orders(order_date);

-- Excellent for range queries
SELECT * FROM orders 
WHERE order_date BETWEEN '2023-01-01' AND '2023-12-31';
```

**Composite Indexes**
- **Purpose**: Multiple columns in single index
- **Column order matters**: Most selective column first
- **Use cases**: Multi-column WHERE clauses, complex filtering

```sql
-- Composite indexes - column order is critical
CREATE INDEX idx_order_date_status ON orders(order_date, status);
CREATE INDEX idx_customer_date_amount ON orders(customer_id, order_date, amount);

-- This query can use the composite index efficiently
SELECT * FROM orders 
WHERE order_date >= '2023-01-01' 
AND status = 'completed';

-- Index usage rules:
-- ✅ Uses index: WHERE order_date = '2023-01-01'
-- ✅ Uses index: WHERE order_date = '2023-01-01' AND status = 'completed'
-- ❌ Cannot use index efficiently: WHERE status = 'completed' (skips first column)
```

**Partial Indexes**
- **Purpose**: Index only subset of rows meeting condition
- **Benefits**: Smaller index size, faster maintenance
- **Use cases**: Filtering on status flags, active records

```sql
-- Partial indexes - index only relevant rows
CREATE INDEX idx_active_customers ON customers(customer_id) 
WHERE status = 'active';

CREATE INDEX idx_pending_orders ON orders(order_date) 
WHERE status = 'pending';

CREATE INDEX idx_high_value_orders ON orders(customer_id, order_date)
WHERE amount > 1000;

-- Queries that benefit from partial indexes
SELECT * FROM customers WHERE status = 'active' AND customer_id = 12345;
SELECT * FROM orders WHERE status = 'pending' ORDER BY order_date;
```

**Covering Indexes (Include Columns)**
- **Purpose**: Include additional columns in index leaf pages
- **Benefits**: Avoid table lookups for covered columns
- **Use cases**: Frequently accessed columns in SELECT clause

```sql
-- Covering indexes - avoid table lookups
CREATE INDEX idx_order_summary ON orders(customer_id) 
INCLUDE (order_date, total_amount, status);

-- This query can be satisfied entirely from the index
SELECT customer_id, order_date, total_amount, status
FROM orders 
WHERE customer_id = 12345;

-- PostgreSQL syntax
CREATE INDEX idx_customer_orders ON orders(customer_id) 
INCLUDE (order_date, amount);

-- SQL Server syntax  
CREATE INDEX idx_customer_orders ON orders(customer_id) 
INCLUDE (order_date, amount);
```

**Specialized Index Types**

```sql
-- Hash indexes (PostgreSQL) - equality only
CREATE INDEX idx_customer_hash ON orders USING HASH(customer_id);

-- GIN indexes for full-text search and arrays
CREATE INDEX idx_product_tags ON products USING GIN(tags);

-- GiST indexes for geometric and full-text data
CREATE INDEX idx_location ON stores USING GIST(location);

-- Functional indexes
CREATE INDEX idx_customer_email_lower ON customers(LOWER(email));
CREATE INDEX idx_order_year ON orders(EXTRACT(YEAR FROM order_date));
```

### Index Maintenance and Monitoring

Proper index maintenance is crucial for sustained performance. Indexes can become fragmented over time and may not be used as expected.

**Index Usage Analysis**
```sql
-- PostgreSQL: Analyze index usage patterns
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as index_scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Find unused indexes (potential candidates for removal)
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND schemaname = 'public'
ORDER BY pg_relation_size(indexrelid) DESC;

-- SQL Server: Index usage statistics
SELECT 
    i.name AS index_name,
    s.user_seeks,
    s.user_scans,
    s.user_lookups,
    s.user_updates
FROM sys.dm_db_index_usage_stats s
JOIN sys.indexes i ON s.object_id = i.object_id AND s.index_id = i.index_id
WHERE s.database_id = DB_ID()
ORDER BY s.user_seeks + s.user_scans + s.user_lookups DESC;
```

**Index Maintenance Operations**
```sql
-- PostgreSQL: Rebuild fragmented indexes
REINDEX INDEX idx_customer_id;
REINDEX TABLE orders; -- Rebuild all indexes on table

-- SQL Server: Rebuild fragmented indexes
ALTER INDEX idx_customer_id ON orders REBUILD;
ALTER INDEX ALL ON orders REBUILD; -- Rebuild all indexes

-- Check index fragmentation (SQL Server)
SELECT 
    i.name AS index_name,
    ips.avg_fragmentation_in_percent,
    ips.page_count
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'DETAILED') ips
JOIN sys.indexes i ON ips.object_id = i.object_id AND ips.index_id = i.index_id
WHERE ips.avg_fragmentation_in_percent > 10
ORDER BY ips.avg_fragmentation_in_percent DESC;

-- Update statistics for query optimizer
ANALYZE customers; -- PostgreSQL
UPDATE STATISTICS customers; -- SQL Server

-- Automatic maintenance scheduling
-- PostgreSQL: Use pg_cron extension
SELECT cron.schedule('reindex-job', '0 2 * * 0', 'REINDEX TABLE orders;');

-- Monitor index bloat (PostgreSQL)
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) as size,
    CASE WHEN pg_relation_size(indexrelid) > 0 THEN
        ROUND(100 * (pg_relation_size(indexrelid) - 
              pg_relation_size(indexrelid, 'main')) / 
              pg_relation_size(indexrelid)::numeric, 2)
    ELSE 0 END as bloat_percentage
FROM pg_stat_user_indexes
WHERE pg_relation_size(indexrelid) > 1024 * 1024 -- > 1MB
ORDER BY pg_relation_size(indexrelid) DESC;
```

## Query Optimization

### Understanding Query Execution

Query optimization involves understanding how the database engine processes queries and making strategic decisions to improve performance.

**Query Execution Process:**
1. **Parsing**: SQL syntax validation
2. **Optimization**: Query plan generation
3. **Execution**: Plan execution with data retrieval
4. **Result**: Data returned to client

### Join Optimization

Joins are often the most expensive operations in queries. Optimizing join strategies can dramatically improve performance.

**Join Types and Performance Characteristics:**

```sql
-- INNER JOIN - fastest, smallest result set
SELECT c.name, o.order_date, o.amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE c.status = 'active';

-- LEFT JOIN - all records from left table
SELECT c.name, COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;

-- Avoid unnecessary joins - only join what you need
-- BAD: Joining tables not used in SELECT or WHERE
SELECT c.name, c.email
FROM customers c
JOIN addresses a ON c.customer_id = a.customer_id  -- Unnecessary join
WHERE c.status = 'active';

-- GOOD: Only join what's needed
SELECT c.name, c.email
FROM customers c
WHERE c.status = 'active';
```

**Join Optimization Strategies:**

```sql
-- 1. Use appropriate join order (smaller table first)
-- Query optimizer usually handles this, but you can hint
SELECT /*+ USE_NL(c o) */ c.name, o.amount
FROM small_customers c
JOIN large_orders o ON c.customer_id = o.customer_id;

-- 2. Filter early to reduce join dataset
SELECT c.name, o.amount
FROM customers c
JOIN (
    SELECT customer_id, amount 
    FROM orders 
    WHERE order_date >= '2023-01-01'  -- Filter before join
) o ON c.customer_id = o.customer_id
WHERE c.status = 'active';  -- Filter before join

-- 3. Use EXISTS instead of JOIN when you don't need joined data
-- Find customers who have placed orders
SELECT c.name, c.email
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id
);

-- 4. Use proper indexes on join columns
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_customers_status ON customers(status);

-- 5. Consider denormalization for frequently joined data
-- Instead of always joining customers and orders
CREATE TABLE order_summary AS
SELECT 
    o.order_id,
    o.customer_id,
    c.customer_name,  -- Denormalized
    c.customer_email, -- Denormalized
    o.order_date,
    o.amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;
```

**Join Algorithm Hints:**

```sql
-- PostgreSQL: Force specific join algorithms
SET enable_nestloop = off;  -- Disable nested loop joins
SET enable_hashjoin = off;  -- Disable hash joins
SET enable_mergejoin = off; -- Disable merge joins

-- SQL Server: Join hints
SELECT c.name, o.amount
FROM customers c
INNER HASH JOIN orders o ON c.customer_id = o.customer_id;

SELECT c.name, o.amount
FROM customers c
INNER MERGE JOIN orders o ON c.customer_id = o.customer_id;
```

### WHERE Clause Optimization

The WHERE clause is critical for query performance as it determines which rows are processed. Optimizing WHERE clauses can dramatically reduce query execution time.

**Indexable WHERE Conditions:**

```sql
-- ✅ GOOD: Use indexed columns directly
SELECT * FROM orders WHERE customer_id = 12345;
SELECT * FROM orders WHERE order_date >= '2023-01-01';
SELECT * FROM orders WHERE status = 'completed';

-- ✅ GOOD: Range queries on indexed columns
SELECT * FROM orders 
WHERE order_date BETWEEN '2023-01-01' AND '2023-12-31'
AND amount > 100;

-- ✅ GOOD: Use leading columns of composite indexes
CREATE INDEX idx_customer_date ON orders(customer_id, order_date);
SELECT * FROM orders WHERE customer_id = 12345; -- Uses index
SELECT * FROM orders WHERE customer_id = 12345 AND order_date >= '2023-01-01'; -- Uses index
```

**Non-Indexable WHERE Conditions (Avoid These):**

```sql
-- ❌ BAD: Functions on indexed columns prevent index usage
SELECT * FROM orders WHERE YEAR(order_date) = 2023;
SELECT * FROM customers WHERE UPPER(name) = 'JOHN DOE';
SELECT * FROM orders WHERE amount * 1.1 > 1000;

-- ✅ GOOD: Rewrite to make columns indexable
SELECT * FROM orders 
WHERE order_date >= '2023-01-01' AND order_date < '2024-01-01';

SELECT * FROM customers WHERE name = 'John Doe'; -- Use functional index if needed
CREATE INDEX idx_customer_name_upper ON customers(UPPER(name));

SELECT * FROM orders WHERE amount > 1000 / 1.1;
```

**Subquery Optimization:**

```sql
-- EXISTS vs IN performance comparison

-- ✅ GOOD: Use EXISTS for existence checks (often faster)
SELECT * FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id
);

-- ❌ SLOWER: IN with subquery (can be slower for large datasets)
SELECT * FROM customers
WHERE customer_id IN (
    SELECT customer_id FROM orders
);

-- ✅ GOOD: IN with small, static lists
SELECT * FROM orders 
WHERE status IN ('pending', 'processing', 'shipped');

-- ✅ GOOD: NOT EXISTS vs NOT IN (handles NULLs correctly)
SELECT * FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id
);

-- ❌ PROBLEMATIC: NOT IN with potential NULLs
SELECT * FROM customers
WHERE customer_id NOT IN (
    SELECT customer_id FROM orders  -- If any customer_id is NULL, returns no rows
);
```

**WHERE Clause Best Practices:**

```sql
-- 1. Filter early and aggressively
SELECT c.name, o.amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.status = 'active'          -- Filter customers first
  AND o.order_date >= '2023-01-01' -- Filter orders first
  AND o.amount > 100;              -- Additional filtering

-- 2. Use most selective conditions first (query optimizer usually handles this)
SELECT * FROM orders
WHERE customer_id = 12345     -- Most selective (assuming unique customer)
  AND status = 'completed'    -- Less selective
  AND amount > 0;             -- Least selective

-- 3. Avoid OR conditions that span different columns (consider UNION)
-- ❌ SLOWER: OR across different columns
SELECT * FROM customers 
WHERE status = 'vip' OR total_orders > 100;

-- ✅ FASTER: Use UNION for different conditions
SELECT * FROM customers WHERE status = 'vip'
UNION
SELECT * FROM customers WHERE total_orders > 100;

-- 4. Use appropriate data types in comparisons
SELECT * FROM orders WHERE customer_id = 12345;    -- INT comparison
SELECT * FROM orders WHERE customer_id = '12345';  -- Avoid string to int conversion
```

## Partitioning Strategies

### Understanding Table Partitioning

Partitioning divides large tables into smaller, more manageable pieces while maintaining the logical view of a single table. This improves query performance, maintenance operations, and enables parallel processing.

**Benefits of Partitioning:**
- **Query Performance**: Partition pruning eliminates irrelevant partitions
- **Maintenance**: Operations on individual partitions are faster
- **Parallel Processing**: Operations can run on multiple partitions simultaneously
- **Storage Management**: Archive old partitions, different storage tiers
- **Backup/Recovery**: Partition-level backup and recovery options

### Table Partitioning Types

**Range Partitioning (Most Common)**
- **Best for**: Time-series data, sequential values
- **Use cases**: Orders by date, logs by timestamp, sales by period

```sql
-- PostgreSQL: Range partitioning by date
CREATE TABLE orders (
    order_id SERIAL,
    customer_id INT,
    order_date DATE,
    amount DECIMAL(10,2)
) PARTITION BY RANGE (order_date);

-- Create monthly partitions
CREATE TABLE orders_2023_01 PARTITION OF orders
FOR VALUES FROM ('2023-01-01') TO ('2023-02-01');

CREATE TABLE orders_2023_02 PARTITION OF orders
FOR VALUES FROM ('2023-02-01') TO ('2023-03-01');

CREATE TABLE orders_2023_03 PARTITION OF orders
FOR VALUES FROM ('2023-03-01') TO ('2023-04-01');

-- Automated partition creation
CREATE OR REPLACE FUNCTION create_monthly_partition(
    table_name TEXT,
    start_date DATE
)
RETURNS void AS $$
DECLARE
    partition_name TEXT;
    end_date DATE;
BEGIN
    partition_name := table_name || '_' || to_char(start_date, 'YYYY_MM');
    end_date := start_date + INTERVAL '1 month';
    
    EXECUTE format(
        'CREATE TABLE %I PARTITION OF %I FOR VALUES FROM (%L) TO (%L)',
        partition_name, table_name, start_date, end_date
    );
END;
$$ LANGUAGE plpgsql;

-- Create partitions for the next 12 months
SELECT create_monthly_partition('orders', generate_series(
    '2024-01-01'::date,
    '2024-12-01'::date,
    '1 month'::interval
)::date);
```

**Hash Partitioning**
- **Best for**: Even data distribution, parallel processing
- **Use cases**: Large tables without natural partitioning key

```sql
-- PostgreSQL: Hash partitioning for even distribution
CREATE TABLE customers (
    customer_id SERIAL,
    name VARCHAR(100),
    email VARCHAR(100)
) PARTITION BY HASH (customer_id);

-- Create 4 hash partitions
CREATE TABLE customers_h0 PARTITION OF customers
FOR VALUES WITH (MODULUS 4, REMAINDER 0);

CREATE TABLE customers_h1 PARTITION OF customers
FOR VALUES WITH (MODULUS 4, REMAINDER 1);

CREATE TABLE customers_h2 PARTITION OF customers
FOR VALUES WITH (MODULUS 4, REMAINDER 2);

CREATE TABLE customers_h3 PARTITION OF customers
FOR VALUES WITH (MODULUS 4, REMAINDER 3);

-- Queries will be distributed across all partitions
SELECT * FROM customers WHERE customer_id = 12345;
```

**List Partitioning**
- **Best for**: Discrete values, geographic regions, categories
- **Use cases**: Orders by region, products by category

```sql
-- PostgreSQL: List partitioning by region
CREATE TABLE sales (
    sale_id SERIAL,
    region VARCHAR(20),
    amount DECIMAL(10,2),
    sale_date DATE
) PARTITION BY LIST (region);

-- Create regional partitions
CREATE TABLE sales_north_america PARTITION OF sales
FOR VALUES IN ('US', 'CA', 'MX');

CREATE TABLE sales_europe PARTITION OF sales
FOR VALUES IN ('UK', 'DE', 'FR', 'IT', 'ES');

CREATE TABLE sales_asia PARTITION OF sales
FOR VALUES IN ('JP', 'CN', 'IN', 'KR');

CREATE TABLE sales_other PARTITION OF sales
DEFAULT; -- Catch-all for unlisted values

-- Queries will only access relevant partitions
SELECT * FROM sales WHERE region = 'US'; -- Only accesses sales_north_america
```

**Multi-Level Partitioning**

```sql
-- PostgreSQL: Partition by range, then by list
CREATE TABLE sales_data (
    sale_id SERIAL,
    sale_date DATE,
    region VARCHAR(20),
    amount DECIMAL(10,2)
) PARTITION BY RANGE (sale_date);

-- Create yearly partitions
CREATE TABLE sales_2023 PARTITION OF sales_data
FOR VALUES FROM ('2023-01-01') TO ('2024-01-01')
PARTITION BY LIST (region);

-- Create regional sub-partitions within 2023
CREATE TABLE sales_2023_us PARTITION OF sales_2023
FOR VALUES IN ('US');

CREATE TABLE sales_2023_eu PARTITION OF sales_2023
FOR VALUES IN ('UK', 'DE', 'FR');
```

### Partition Pruning and Optimization

Partition pruning is the process where the query optimizer eliminates partitions that cannot contain relevant data, dramatically improving query performance.

**Understanding Partition Pruning:**

```sql
-- ✅ GOOD: Query that enables partition pruning
SELECT * FROM orders 
WHERE order_date >= '2023-06-01' 
AND order_date < '2023-07-01';
-- Only accesses orders_2023_06 partition

-- ✅ GOOD: Exact partition match
SELECT * FROM orders 
WHERE order_date = '2023-06-15';
-- Only accesses orders_2023_06 partition

-- ❌ BAD: Functions prevent partition pruning
SELECT * FROM orders 
WHERE EXTRACT(MONTH FROM order_date) = 6;
-- Accesses ALL partitions

-- ✅ GOOD: Rewrite to enable pruning
SELECT * FROM orders 
WHERE order_date >= '2023-06-01' 
AND order_date < '2023-07-01';

-- Check partition pruning in execution plan
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM orders 
WHERE order_date >= '2023-06-01' 
AND order_date < '2023-07-01';
```

**Partition-wise Operations:**

```sql
-- Enable partition-wise joins and aggregates (PostgreSQL)
SET enable_partitionwise_join = on;
SET enable_partitionwise_aggregate = on;

-- Partition-wise join example
SELECT o.order_id, c.customer_name
FROM orders o  -- Partitioned by order_date
JOIN customers c ON o.customer_id = c.customer_id  -- Partitioned by customer_id
WHERE o.order_date >= '2023-06-01';

-- Partition-wise aggregate
SELECT 
    DATE_TRUNC('month', order_date) as month,
    COUNT(*) as order_count,
    SUM(amount) as total_amount
FROM orders
WHERE order_date >= '2023-01-01'
GROUP BY DATE_TRUNC('month', order_date);
```

**Partition Maintenance:**

```sql
-- Automated partition maintenance
CREATE OR REPLACE FUNCTION maintain_partitions()
RETURNS void AS $$
DECLARE
    current_month DATE;
    partition_name TEXT;
BEGIN
    -- Create next month's partition
    current_month := DATE_TRUNC('month', CURRENT_DATE + INTERVAL '1 month');
    partition_name := 'orders_' || to_char(current_month, 'YYYY_MM');
    
    -- Check if partition exists
    IF NOT EXISTS (
        SELECT 1 FROM pg_tables 
        WHERE tablename = partition_name
    ) THEN
        PERFORM create_monthly_partition('orders', current_month);
    END IF;
    
    -- Drop old partitions (older than 2 years)
    FOR partition_name IN 
        SELECT tablename 
        FROM pg_tables 
        WHERE tablename LIKE 'orders_____' 
        AND tablename < 'orders_' || to_char(CURRENT_DATE - INTERVAL '2 years', 'YYYY_MM')
    LOOP
        EXECUTE 'DROP TABLE ' || partition_name;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Schedule partition maintenance
SELECT cron.schedule('partition-maintenance', '0 1 1 * *', 'SELECT maintain_partitions();');
```

## Memory and Configuration

### Understanding Database Memory

Proper memory configuration is crucial for optimal database performance. Different memory areas serve different purposes and should be tuned based on workload characteristics.

### PostgreSQL Memory Configuration

```sql
-- Core memory settings (postgresql.conf)
-- shared_buffers: Database cache (25% of RAM for dedicated server)
shared_buffers = 2GB

-- effective_cache_size: OS + DB cache estimate (75% of total RAM)
effective_cache_size = 6GB

-- work_mem: Memory per sort/hash operation (start with 4MB)
work_mem = 16MB

-- maintenance_work_mem: Memory for maintenance operations
maintenance_work_mem = 256MB

-- wal_buffers: Write-ahead log buffers
wal_buffers = 16MB

-- max_connections: Maximum concurrent connections
max_connections = 200

-- Connection and query-specific settings
-- Set work_mem per session for large operations
SET work_mem = '256MB';

-- Monitor memory usage
SELECT 
    name,
    setting,
    unit,
    context
FROM pg_settings 
WHERE name IN (
    'shared_buffers',
    'effective_cache_size', 
    'work_mem',
    'maintenance_work_mem'
);

-- Check buffer cache hit ratio
SELECT 
    ROUND(
        (sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read))) * 100, 2
    ) as cache_hit_ratio
FROM pg_statio_user_tables;
```

### SQL Server Memory Configuration

```sql
-- Set maximum server memory (leave 2-4GB for OS)
EXEC sp_configure 'max server memory (MB)', 6144;
RECONFIGURE;

-- Set minimum server memory
EXEC sp_configure 'min server memory (MB)', 2048;
RECONFIGURE;

-- Check current memory usage
SELECT 
    counter_name,
    cntr_value / 1024 as value_mb
FROM sys.dm_os_performance_counters
WHERE counter_name IN (
    'Total Server Memory (KB)',
    'Target Server Memory (KB)',
    'Buffer cache hit ratio'
);

-- Monitor memory pressure
SELECT 
    type,
    pages_kb,
    pages_in_use_kb
FROM sys.dm_os_memory_clerks
WHERE pages_kb > 1024
ORDER BY pages_kb DESC;
```

### Query Plan Analysis

Execution plans show how the database engine processes queries and are essential for performance optimization.

**PostgreSQL Execution Plans:**

```sql
-- Basic execution plan
EXPLAIN SELECT * FROM orders WHERE customer_id = 12345;

-- Detailed execution plan with actual statistics
EXPLAIN (ANALYZE, BUFFERS, VERBOSE, FORMAT JSON) 
SELECT c.name, COUNT(o.order_id)
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.status = 'active'
GROUP BY c.customer_id, c.name;

-- Key metrics to analyze:
-- 1. Cost estimates vs actual time
-- 2. Rows estimated vs actual rows
-- 3. Buffer usage (shared hit/read/written)
-- 4. Join algorithms used
-- 5. Index usage

-- Auto-explain for slow queries
LOAD 'auto_explain';
SET auto_explain.log_min_duration = 1000; -- Log queries > 1 second
SET auto_explain.log_analyze = true;
SET auto_explain.log_buffers = true;
```

**SQL Server Execution Plans:**

```sql
-- Enable execution plan and I/O statistics
SET STATISTICS IO ON;
SET STATISTICS TIME ON;
SET SHOWPLAN_ALL ON;

SELECT c.name, COUNT(o.order_id)
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.status = 'active'
GROUP BY c.customer_id, c.name;

-- Query Store for historical performance
SELECT 
    q.query_id,
    qt.query_sql_text,
    rs.avg_duration / 1000 as avg_duration_ms,
    rs.avg_cpu_time / 1000 as avg_cpu_time_ms,
    rs.avg_logical_io_reads
FROM sys.query_store_query q
JOIN sys.query_store_query_text qt ON q.query_text_id = qt.query_text_id
JOIN sys.query_store_runtime_stats rs ON q.query_id = rs.query_id
WHERE rs.avg_duration > 1000000 -- > 1 second
ORDER BY rs.avg_duration DESC;
```

## Advanced Optimization Techniques

### Materialized Views and Precomputed Results

Materialized views store query results physically, providing fast access to complex aggregations.

```sql
-- Create materialized view for expensive aggregations
CREATE MATERIALIZED VIEW customer_summary AS
SELECT 
    c.customer_id,
    c.name,
    c.email,
    COUNT(o.order_id) as total_orders,
    SUM(o.amount) as total_spent,
    AVG(o.amount) as avg_order_value,
    MAX(o.order_date) as last_order_date,
    MIN(o.order_date) as first_order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.email;

-- Create indexes on materialized view
CREATE INDEX idx_customer_summary_total_spent ON customer_summary(total_spent);
CREATE INDEX idx_customer_summary_last_order ON customer_summary(last_order_date);

-- Refresh strategies
-- 1. Manual refresh
REFRESH MATERIALIZED VIEW customer_summary;

-- 2. Concurrent refresh (PostgreSQL)
REFRESH MATERIALIZED VIEW CONCURRENTLY customer_summary;

-- 3. Scheduled refresh
SELECT cron.schedule('refresh-customer-summary', '0 2 * * *', 
    'REFRESH MATERIALIZED VIEW CONCURRENTLY customer_summary;');

-- 4. Incremental refresh function
CREATE OR REPLACE FUNCTION refresh_customer_summary_incremental()
RETURNS void AS $$
BEGIN
    -- Delete changed customers
    DELETE FROM customer_summary cs
    WHERE EXISTS (
        SELECT 1 FROM customers c
        WHERE c.customer_id = cs.customer_id
        AND c.updated_at > (SELECT last_refresh FROM mv_refresh_log WHERE view_name = 'customer_summary')
    );
    
    -- Insert updated data
    INSERT INTO customer_summary
    SELECT 
        c.customer_id,
        c.name,
        c.email,
        COUNT(o.order_id) as total_orders,
        SUM(o.amount) as total_spent,
        AVG(o.amount) as avg_order_value,
        MAX(o.order_date) as last_order_date,
        MIN(o.order_date) as first_order_date
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    WHERE c.updated_at > (SELECT last_refresh FROM mv_refresh_log WHERE view_name = 'customer_summary')
    GROUP BY c.customer_id, c.name, c.email;
    
    -- Update refresh log
    UPDATE mv_refresh_log 
    SET last_refresh = CURRENT_TIMESTAMP 
    WHERE view_name = 'customer_summary';
END;
$$ LANGUAGE plpgsql;
```

### Query Rewriting and Optimization

```sql
-- 1. Subquery to JOIN conversion
-- SLOW: Correlated subquery
SELECT c.name, c.email
FROM customers c
WHERE (
    SELECT COUNT(*) 
    FROM orders o 
    WHERE o.customer_id = c.customer_id
) > 5;

-- FAST: Convert to JOIN
SELECT DISTINCT c.name, c.email
FROM customers c
JOIN (
    SELECT customer_id
    FROM orders
    GROUP BY customer_id
    HAVING COUNT(*) > 5
) o ON c.customer_id = o.customer_id;

-- 2. Window functions for ranking
-- Instead of multiple subqueries
SELECT 
    customer_id,
    order_date,
    amount,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) as order_rank,
    SUM(amount) OVER (PARTITION BY customer_id) as customer_total
FROM orders;

-- 3. Common Table Expressions for readability and performance
WITH high_value_customers AS (
    SELECT customer_id
    FROM orders
    GROUP BY customer_id
    HAVING SUM(amount) > 10000
),
recent_orders AS (
    SELECT customer_id, order_id, amount
    FROM orders
    WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
)
SELECT 
    c.name,
    COUNT(ro.order_id) as recent_orders,
    SUM(ro.amount) as recent_total
FROM customers c
JOIN high_value_customers hvc ON c.customer_id = hvc.customer_id
LEFT JOIN recent_orders ro ON c.customer_id = ro.customer_id
GROUP BY c.customer_id, c.name;
```

### Parallel Query Processing

```sql
-- PostgreSQL: Enable parallel queries
SET max_parallel_workers_per_gather = 4;
SET parallel_tuple_cost = 0.1;
SET parallel_setup_cost = 1000;

-- Force parallel execution
SET force_parallel_mode = on;

-- Queries that benefit from parallelization
SELECT 
    DATE_TRUNC('month', order_date) as month,
    COUNT(*) as order_count,
    SUM(amount) as total_amount
FROM orders
WHERE order_date >= '2023-01-01'
GROUP BY DATE_TRUNC('month', order_date);

-- Check parallel execution in plan
EXPLAIN (ANALYZE, BUFFERS) 
SELECT COUNT(*) FROM large_table;
```

### Batch Processing Optimization

```sql
-- Efficient batch processing
CREATE OR REPLACE FUNCTION process_orders_batch(
    batch_size INTEGER DEFAULT 10000
)
RETURNS INTEGER AS $$
DECLARE
    processed_count INTEGER := 0;
    batch_count INTEGER;
BEGIN
    LOOP
        -- Process batch with explicit transaction control
        WITH batch AS (
            SELECT order_id
            FROM orders
            WHERE status = 'pending'
            ORDER BY order_id
            LIMIT batch_size
            FOR UPDATE SKIP LOCKED  -- Avoid blocking
        )
        UPDATE orders
        SET 
            status = 'processing',
            processed_at = CURRENT_TIMESTAMP
        FROM batch
        WHERE orders.order_id = batch.order_id;
        
        GET DIAGNOSTICS batch_count = ROW_COUNT;
        processed_count := processed_count + batch_count;
        
        -- Exit if no more records to process
        EXIT WHEN batch_count = 0;
        
        -- Optional: commit and start new transaction
        COMMIT;
        BEGIN;
    END LOOP;
    
    RETURN processed_count;
END;
$$ LANGUAGE plpgsql;
```

## Monitoring and Analysis

### Performance Monitoring Setup

Continuous monitoring is essential for maintaining optimal database performance and identifying issues before they impact users.

**PostgreSQL Monitoring:**

```sql
-- Enable query statistics collection
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Configure in postgresql.conf
-- shared_preload_libraries = 'pg_stat_statements'
-- pg_stat_statements.max = 10000
-- pg_stat_statements.track = all

-- Top slow queries
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    max_time,
    stddev_time,
    rows,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements
WHERE mean_time > 100  -- Queries averaging > 100ms
ORDER BY mean_time DESC
LIMIT 20;

-- Index usage statistics
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
WHERE idx_scan > 0
ORDER BY idx_scan DESC;

-- Table statistics
SELECT 
    schemaname,
    tablename,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes,
    n_live_tup as live_tuples,
    n_dead_tup as dead_tuples,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables
ORDER BY n_tup_ins + n_tup_upd + n_tup_del DESC;

-- Connection and activity monitoring
SELECT 
    pid,
    usename,
    application_name,
    client_addr,
    state,
    query_start,
    now() - query_start as duration,
    query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY query_start;
```

**SQL Server Monitoring:**

```sql
-- Enable Query Store
ALTER DATABASE YourDatabase SET QUERY_STORE = ON;
ALTER DATABASE YourDatabase SET QUERY_STORE (
    OPERATION_MODE = READ_WRITE,
    DATA_FLUSH_INTERVAL_SECONDS = 900,
    INTERVAL_LENGTH_MINUTES = 60,
    MAX_STORAGE_SIZE_MB = 1000
);

-- Top resource-consuming queries
SELECT TOP 20
    q.query_id,
    qt.query_sql_text,
    rs.count_executions,
    rs.avg_duration / 1000.0 as avg_duration_ms,
    rs.avg_cpu_time / 1000.0 as avg_cpu_time_ms,
    rs.avg_logical_io_reads,
    rs.avg_physical_io_reads
FROM sys.query_store_query q
JOIN sys.query_store_query_text qt ON q.query_text_id = qt.query_text_id
JOIN sys.query_store_runtime_stats rs ON q.query_id = rs.query_id
WHERE rs.last_execution_time >= DATEADD(day, -7, GETDATE())
ORDER BY rs.avg_duration DESC;

-- Index usage and missing indexes
SELECT 
    i.name as index_name,
    s.user_seeks,
    s.user_scans,
    s.user_lookups,
    s.user_updates,
    s.last_user_seek,
    s.last_user_scan
FROM sys.dm_db_index_usage_stats s
JOIN sys.indexes i ON s.object_id = i.object_id AND s.index_id = i.index_id
WHERE s.database_id = DB_ID()
ORDER BY s.user_seeks + s.user_scans + s.user_lookups DESC;

-- Wait statistics
SELECT TOP 20
    wait_type,
    wait_time_ms,
    max_wait_time_ms,
    signal_wait_time_ms,
    waiting_tasks_count
FROM sys.dm_os_wait_stats
WHERE wait_type NOT IN (
    'CLR_SEMAPHORE', 'LAZYWRITER_SLEEP', 'RESOURCE_QUEUE',
    'SLEEP_TASK', 'SLEEP_SYSTEMTASK', 'SQLTRACE_BUFFER_FLUSH',
    'WAITFOR', 'LOGMGR_QUEUE', 'CHECKPOINT_QUEUE'
)
ORDER BY wait_time_ms DESC;
```

### Automated Performance Alerts

```sql
-- PostgreSQL: Create performance monitoring function
CREATE OR REPLACE FUNCTION check_performance_metrics()
RETURNS TABLE(
    metric_name TEXT,
    current_value NUMERIC,
    threshold NUMERIC,
    status TEXT,
    recommendation TEXT
) AS $$
BEGIN
    -- Check cache hit ratio
    RETURN QUERY
    SELECT 
        'Cache Hit Ratio'::TEXT,
        ROUND(
            (sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read))) * 100, 2
        ),
        95.0,
        CASE 
            WHEN (sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read))) * 100 >= 95 
            THEN 'OK' 
            ELSE 'WARNING' 
        END,
        CASE 
            WHEN (sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read))) * 100 < 95 
            THEN 'Consider increasing shared_buffers or adding indexes'
            ELSE 'Cache performance is good'
        END
    FROM pg_statio_user_tables
    WHERE heap_blks_read > 0;
    
    -- Check for long-running queries
    RETURN QUERY
    SELECT 
        'Long Running Queries'::TEXT,
        COUNT(*)::NUMERIC,
        5.0,
        CASE WHEN COUNT(*) > 5 THEN 'CRITICAL' ELSE 'OK' END,
        CASE 
            WHEN COUNT(*) > 5 
            THEN 'Review and optimize slow queries'
            ELSE 'Query performance is acceptable'
        END
    FROM pg_stat_activity
    WHERE state = 'active'
      AND now() - query_start > INTERVAL '5 minutes';
    
    -- Check connection usage
    RETURN QUERY
    SELECT 
        'Connection Usage'::TEXT,
        COUNT(*)::NUMERIC,
        (SELECT setting::NUMERIC * 0.8 FROM pg_settings WHERE name = 'max_connections'),
        CASE 
            WHEN COUNT(*) > (SELECT setting::NUMERIC * 0.8 FROM pg_settings WHERE name = 'max_connections') 
            THEN 'WARNING' 
            ELSE 'OK' 
        END,
        CASE 
            WHEN COUNT(*) > (SELECT setting::NUMERIC * 0.8 FROM pg_settings WHERE name = 'max_connections') 
            THEN 'Consider connection pooling or increasing max_connections'
            ELSE 'Connection usage is normal'
        END
    FROM pg_stat_activity;
END;
$$ LANGUAGE plpgsql;

-- Schedule performance checks
SELECT cron.schedule('performance-check', '*/15 * * * *', 
    'SELECT * FROM check_performance_metrics();');
```

## Best Practices

### Query Writing Best Practices

**1. SELECT Statement Optimization:**

```sql
-- ✅ GOOD: Select only needed columns
SELECT customer_id, name, email FROM customers WHERE status = 'active';

-- ❌ BAD: Select all columns unnecessarily
SELECT * FROM customers WHERE status = 'active';

-- ✅ GOOD: Use LIMIT for large result sets
SELECT customer_id, name FROM customers ORDER BY created_date DESC LIMIT 100;

-- ✅ GOOD: Use appropriate data types in WHERE clauses
SELECT * FROM orders WHERE customer_id = 12345;  -- INT
SELECT * FROM orders WHERE order_date = '2023-01-01'::DATE;  -- DATE
```

**2. JOIN Optimization:**

```sql
-- ✅ GOOD: Filter before joining
SELECT c.name, o.amount
FROM (
    SELECT customer_id, name 
    FROM customers 
    WHERE status = 'active'
) c
JOIN (
    SELECT customer_id, amount 
    FROM orders 
    WHERE order_date >= '2023-01-01'
) o ON c.customer_id = o.customer_id;

-- ✅ GOOD: Use appropriate join types
SELECT c.name, COUNT(o.order_id)
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id  -- Use LEFT JOIN when you need all customers
GROUP BY c.customer_id, c.name;

-- ✅ GOOD: Index join columns
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_customers_status ON customers(status);
```

**3. Subquery Optimization:**

```sql
-- ✅ GOOD: Use EXISTS for existence checks
SELECT customer_id, name
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id 
    AND o.order_date >= '2023-01-01'
);

-- ✅ GOOD: Use window functions instead of correlated subqueries
SELECT 
    customer_id,
    order_date,
    amount,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) as order_rank
FROM orders;
```

### Index Design Best Practices

**1. Index Strategy:**

```sql
-- ✅ GOOD: Create indexes on frequently queried columns
CREATE INDEX idx_customers_email ON customers(email);  -- Login queries
CREATE INDEX idx_orders_date ON orders(order_date);    -- Date range queries
CREATE INDEX idx_orders_status ON orders(status);     -- Status filtering

-- ✅ GOOD: Composite indexes for multi-column queries
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
-- Supports: WHERE customer_id = ? AND order_date >= ?
-- Also supports: WHERE customer_id = ?

-- ✅ GOOD: Include frequently selected columns
CREATE INDEX idx_orders_customer_covering ON orders(customer_id) 
INCLUDE (order_date, amount, status);
```

**2. Index Maintenance:**

```sql
-- Regular index maintenance schedule
CREATE OR REPLACE FUNCTION maintain_indexes()
RETURNS void AS $$
BEGIN
    -- Reindex heavily updated tables weekly
    IF EXTRACT(DOW FROM CURRENT_DATE) = 0 THEN  -- Sunday
        REINDEX TABLE orders;
        REINDEX TABLE customers;
    END IF;
    
    -- Update statistics daily
    ANALYZE orders;
    ANALYZE customers;
    ANALYZE products;
END;
$$ LANGUAGE plpgsql;

-- Schedule maintenance
SELECT cron.schedule('index-maintenance', '0 2 * * *', 'SELECT maintain_indexes();');
```

---

## Summary

SQL performance optimization is an ongoing process that requires:

1. **Proper Indexing**: Create and maintain appropriate indexes
2. **Query Optimization**: Write efficient queries and analyze execution plans
3. **System Configuration**: Tune memory and database parameters
4. **Monitoring**: Continuously monitor performance metrics
5. **Testing**: Regular performance testing and validation
6. **Maintenance**: Scheduled maintenance and optimization tasks

**Key Takeaways:**
- Index the right columns with the right strategy
- Write queries that can use indexes effectively
- Monitor and analyze query performance regularly
- Configure database memory appropriately for your workload
- Use partitioning for very large tables
- Implement automated monitoring and alerting
- Test performance changes before deploying to production

**Remember**: Performance optimization is workload-specific. What works for one application may not work for another. Always test changes in a representative environment before applying them to production.