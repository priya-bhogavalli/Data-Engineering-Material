# SQL Performance Optimization for Data Engineering

## Index Optimization

### Index Types and Usage
```sql
-- B-tree indexes (default)
CREATE INDEX idx_customer_id ON orders(customer_id);

-- Composite indexes
CREATE INDEX idx_order_date_status ON orders(order_date, status);

-- Partial indexes
CREATE INDEX idx_active_customers ON customers(customer_id) 
WHERE status = 'active';

-- Covering indexes
CREATE INDEX idx_order_summary ON orders(customer_id) 
INCLUDE (order_date, total_amount);
```

### Index Maintenance
```sql
-- Analyze index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Rebuild fragmented indexes
ALTER INDEX idx_customer_id REBUILD;

-- Update statistics
ANALYZE customers;
```

## Query Optimization

### Join Optimization
```sql
-- Use appropriate join types
SELECT c.name, COUNT(o.order_id)
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;

-- Avoid unnecessary joins
-- Bad: joining tables not used in SELECT or WHERE
-- Good: only join what's needed
SELECT c.name, c.email
FROM customers c
WHERE c.status = 'active';
```

### WHERE Clause Optimization
```sql
-- Use indexed columns in WHERE
SELECT * FROM orders WHERE customer_id = 12345;

-- Avoid functions on indexed columns
-- Bad: WHERE YEAR(order_date) = 2023
-- Good: WHERE order_date >= '2023-01-01' AND order_date < '2024-01-01'

-- Use EXISTS instead of IN for subqueries
SELECT * FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);
```

## Partitioning Strategies

### Table Partitioning
```sql
-- Range partitioning by date
CREATE TABLE orders_2023 PARTITION OF orders
FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');

-- Hash partitioning
CREATE TABLE customers_hash PARTITION OF customers
FOR VALUES WITH (MODULUS 4, REMAINDER 0);

-- List partitioning
CREATE TABLE orders_us PARTITION OF orders
FOR VALUES IN ('US', 'CA', 'MX');
```

### Partition Pruning
```sql
-- Query that uses partition pruning
SELECT * FROM orders 
WHERE order_date >= '2023-06-01' 
AND order_date < '2023-07-01';

-- Enable partition-wise joins
SET enable_partitionwise_join = on;
SET enable_partitionwise_aggregate = on;
```

## Memory and Configuration

### Memory Settings
```sql
-- PostgreSQL memory configuration
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB

-- SQL Server memory configuration
sp_configure 'max server memory', 8192;
RECONFIGURE;
```

### Query Plan Analysis
```sql
-- PostgreSQL execution plan
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM orders WHERE customer_id = 12345;

-- SQL Server execution plan
SET STATISTICS IO ON;
SELECT * FROM orders WHERE customer_id = 12345;
```