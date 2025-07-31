-- SQL Performance Optimization Examples
-- This file contains practical examples of query optimization techniques

-- =====================================================
-- 1. INDEX OPTIMIZATION EXAMPLES
-- =====================================================

-- Example: Slow query without proper indexing
-- SLOW VERSION
SELECT customer_id, name, email
FROM customers 
WHERE city = 'New York' 
  AND registration_date >= '2023-01-01'
  AND status = 'active';

-- Create composite index for better performance
CREATE INDEX idx_customers_city_date_status 
ON customers (city, registration_date, status);

-- Alternative: Covering index (includes all needed columns)
CREATE INDEX idx_customers_covering 
ON customers (city, registration_date, status) 
INCLUDE (customer_id, name, email);

-- Partial index for frequently queried subset
CREATE INDEX idx_customers_active_city 
ON customers (city, registration_date) 
WHERE status = 'active';

-- =====================================================
-- 2. JOIN OPTIMIZATION
-- =====================================================

-- SLOW VERSION: Multiple joins without proper indexing
SELECT 
    c.customer_id,
    c.name,
    o.order_date,
    oi.product_id,
    p.product_name,
    oi.quantity * oi.unit_price as line_total
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE c.city = 'Chicago'
  AND o.order_date >= '2023-01-01';

-- OPTIMIZED VERSION: With proper indexes and query restructuring
-- First, create necessary indexes
CREATE INDEX idx_customers_city ON customers (city);
CREATE INDEX idx_orders_customer_date ON orders (customer_id, order_date);
CREATE INDEX idx_order_items_order_product ON order_items (order_id, product_id);
CREATE INDEX idx_products_id ON products (product_id);

-- Optimized query with filtered subquery
WITH chicago_customers AS (
    SELECT customer_id, name
    FROM customers 
    WHERE city = 'Chicago'
),
recent_orders AS (
    SELECT customer_id, order_id, order_date
    FROM orders 
    WHERE order_date >= '2023-01-01'
      AND customer_id IN (SELECT customer_id FROM chicago_customers)
)
SELECT 
    cc.customer_id,
    cc.name,
    ro.order_date,
    oi.product_id,
    p.product_name,
    oi.quantity * oi.unit_price as line_total
FROM chicago_customers cc
JOIN recent_orders ro ON cc.customer_id = ro.customer_id
JOIN order_items oi ON ro.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id;

-- =====================================================
-- 3. SUBQUERY OPTIMIZATION
-- =====================================================

-- SLOW VERSION: Correlated subquery
SELECT 
    customer_id,
    name,
    (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.customer_id) as order_count,
    (SELECT SUM(amount) FROM orders o WHERE o.customer_id = c.customer_id) as total_spent
FROM customers c
WHERE status = 'active';

-- OPTIMIZED VERSION: Using window functions
WITH customer_stats AS (
    SELECT 
        c.customer_id,
        c.name,
        c.status,
        COUNT(o.order_id) as order_count,
        COALESCE(SUM(o.amount), 0) as total_spent
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    WHERE c.status = 'active'
    GROUP BY c.customer_id, c.name, c.status
)
SELECT customer_id, name, order_count, total_spent
FROM customer_stats;

-- Alternative: Using EXISTS instead of IN for better performance
-- SLOW VERSION
SELECT customer_id, name
FROM customers
WHERE customer_id IN (
    SELECT customer_id 
    FROM orders 
    WHERE order_date >= '2023-01-01'
);

-- OPTIMIZED VERSION
SELECT customer_id, name
FROM customers c
WHERE EXISTS (
    SELECT 1 
    FROM orders o 
    WHERE o.customer_id = c.customer_id 
      AND o.order_date >= '2023-01-01'
);

-- =====================================================
-- 4. PAGINATION OPTIMIZATION
-- =====================================================

-- SLOW VERSION: OFFSET/LIMIT for large datasets
SELECT customer_id, name, email, registration_date
FROM customers
ORDER BY registration_date DESC
OFFSET 10000 LIMIT 20;

-- OPTIMIZED VERSION: Cursor-based pagination
-- First page
SELECT customer_id, name, email, registration_date
FROM customers
ORDER BY registration_date DESC, customer_id DESC
LIMIT 20;

-- Subsequent pages (using last seen values)
SELECT customer_id, name, email, registration_date
FROM customers
WHERE (registration_date, customer_id) < ('2023-05-15 10:30:00', 12345)
ORDER BY registration_date DESC, customer_id DESC
LIMIT 20;

-- Alternative: Using ROW_NUMBER() with filtering
WITH numbered_customers AS (
    SELECT 
        customer_id, 
        name, 
        email, 
        registration_date,
        ROW_NUMBER() OVER (ORDER BY registration_date DESC) as rn
    FROM customers
    WHERE registration_date >= '2023-01-01'  -- Add filters early
)
SELECT customer_id, name, email, registration_date
FROM numbered_customers
WHERE rn BETWEEN 10001 AND 10020;

-- =====================================================
-- 5. AGGREGATION OPTIMIZATION
-- =====================================================

-- SLOW VERSION: Multiple passes over large table
SELECT 
    (SELECT COUNT(*) FROM orders WHERE status = 'completed') as completed_orders,
    (SELECT COUNT(*) FROM orders WHERE status = 'pending') as pending_orders,
    (SELECT COUNT(*) FROM orders WHERE status = 'cancelled') as cancelled_orders,
    (SELECT AVG(amount) FROM orders WHERE status = 'completed') as avg_completed_amount;

-- OPTIMIZED VERSION: Single pass with conditional aggregation
SELECT 
    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_orders,
    COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_orders,
    COUNT(CASE WHEN status = 'cancelled' THEN 1 END) as cancelled_orders,
    AVG(CASE WHEN status = 'completed' THEN amount END) as avg_completed_amount
FROM orders;

-- Complex aggregation with window functions
WITH daily_sales AS (
    SELECT 
        DATE(order_date) as sale_date,
        SUM(amount) as daily_total,
        COUNT(*) as daily_orders
    FROM orders
    WHERE order_date >= CURRENT_DATE - INTERVAL '90 days'
    GROUP BY DATE(order_date)
)
SELECT 
    sale_date,
    daily_total,
    daily_orders,
    -- Running totals
    SUM(daily_total) OVER (ORDER BY sale_date) as running_total,
    -- Moving averages
    AVG(daily_total) OVER (
        ORDER BY sale_date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as weekly_avg,
    -- Ranking
    RANK() OVER (ORDER BY daily_total DESC) as daily_rank
FROM daily_sales
ORDER BY sale_date;

-- =====================================================
-- 6. PARTITIONING EXAMPLES
-- =====================================================

-- Create partitioned table for large time-series data
CREATE TABLE sales_data (
    id SERIAL,
    sale_date DATE NOT NULL,
    customer_id INTEGER,
    amount DECIMAL(10,2),
    product_id INTEGER
) PARTITION BY RANGE (sale_date);

-- Create monthly partitions
CREATE TABLE sales_data_2023_01 PARTITION OF sales_data
    FOR VALUES FROM ('2023-01-01') TO ('2023-02-01');

CREATE TABLE sales_data_2023_02 PARTITION OF sales_data
    FOR VALUES FROM ('2023-02-01') TO ('2023-03-01');

-- Query optimization with partition pruning
-- This query will only scan the relevant partition
SELECT customer_id, SUM(amount) as total_sales
FROM sales_data
WHERE sale_date BETWEEN '2023-01-15' AND '2023-01-31'
GROUP BY customer_id;

-- =====================================================
-- 7. MATERIALIZED VIEW OPTIMIZATION
-- =====================================================

-- Create materialized view for expensive aggregations
CREATE MATERIALIZED VIEW mv_customer_summary AS
SELECT 
    customer_id,
    COUNT(*) as total_orders,
    SUM(amount) as total_spent,
    AVG(amount) as avg_order_value,
    MAX(order_date) as last_order_date,
    MIN(order_date) as first_order_date,
    EXTRACT(DAYS FROM (MAX(order_date) - MIN(order_date))) as customer_lifespan_days
FROM orders
GROUP BY customer_id;

-- Create index on materialized view
CREATE INDEX idx_mv_customer_summary_total_spent 
ON mv_customer_summary (total_spent DESC);

-- Use materialized view instead of expensive aggregation
-- SLOW VERSION
SELECT 
    c.customer_id,
    c.name,
    COUNT(o.order_id) as order_count,
    SUM(o.amount) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING SUM(o.amount) > 1000
ORDER BY SUM(o.amount) DESC;

-- OPTIMIZED VERSION using materialized view
SELECT 
    c.customer_id,
    c.name,
    mcs.total_orders as order_count,
    mcs.total_spent
FROM customers c
JOIN mv_customer_summary mcs ON c.customer_id = mcs.customer_id
WHERE mcs.total_spent > 1000
ORDER BY mcs.total_spent DESC;

-- =====================================================
-- 8. QUERY REWRITING FOR PERFORMANCE
-- =====================================================

-- SLOW VERSION: Complex WHERE clause
SELECT *
FROM products p
WHERE (p.category = 'Electronics' AND p.price > 100)
   OR (p.category = 'Books' AND p.price > 20)
   OR (p.category = 'Clothing' AND p.price > 50);

-- OPTIMIZED VERSION: Using UNION ALL
SELECT * FROM products WHERE category = 'Electronics' AND price > 100
UNION ALL
SELECT * FROM products WHERE category = 'Books' AND price > 20
UNION ALL
SELECT * FROM products WHERE category = 'Clothing' AND price > 50;

-- SLOW VERSION: NOT IN with NULLs
SELECT customer_id, name
FROM customers
WHERE customer_id NOT IN (
    SELECT customer_id FROM orders WHERE order_date >= '2023-01-01'
);

-- OPTIMIZED VERSION: LEFT JOIN with NULL check
SELECT c.customer_id, c.name
FROM customers c
LEFT JOIN (
    SELECT DISTINCT customer_id 
    FROM orders 
    WHERE order_date >= '2023-01-01'
) o ON c.customer_id = o.customer_id
WHERE o.customer_id IS NULL;

-- =====================================================
-- 9. BATCH PROCESSING OPTIMIZATION
-- =====================================================

-- Efficient batch update pattern
DO $$
DECLARE
    batch_size INTEGER := 1000;
    total_updated INTEGER := 0;
    batch_count INTEGER;
BEGIN
    LOOP
        -- Update in batches
        WITH batch_ids AS (
            SELECT customer_id
            FROM customers
            WHERE last_login_date < CURRENT_DATE - INTERVAL '30 days'
              AND status != 'inactive'
            LIMIT batch_size
        )
        UPDATE customers
        SET status = 'inactive',
            updated_at = CURRENT_TIMESTAMP
        WHERE customer_id IN (SELECT customer_id FROM batch_ids);
        
        GET DIAGNOSTICS batch_count = ROW_COUNT;
        total_updated := total_updated + batch_count;
        
        -- Exit if no more rows to update
        EXIT WHEN batch_count = 0;
        
        -- Optional: Add delay to prevent overwhelming the system
        PERFORM pg_sleep(0.1);
        
        -- Commit after each batch
        COMMIT;
    END LOOP;
    
    RAISE NOTICE 'Total rows updated: %', total_updated;
END $$;

-- =====================================================
-- 10. MONITORING AND ANALYSIS QUERIES
-- =====================================================

-- Query to identify slow queries (PostgreSQL)
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Index usage analysis
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch,
    idx_scan,
    CASE 
        WHEN idx_scan = 0 THEN 'Never Used'
        WHEN idx_scan < 10 THEN 'Rarely Used'
        ELSE 'Frequently Used'
    END as usage_category
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Table size and bloat analysis
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as table_size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) as index_size,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes,
    n_live_tup as live_tuples,
    n_dead_tup as dead_tuples,
    CASE 
        WHEN n_live_tup > 0 
        THEN round(100.0 * n_dead_tup / (n_live_tup + n_dead_tup), 2)
        ELSE 0 
    END as dead_tuple_percent
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Lock monitoring query
SELECT 
    pg_stat_activity.pid,
    pg_stat_activity.usename,
    pg_stat_activity.query,
    pg_locks.mode,
    pg_locks.locktype,
    pg_locks.granted,
    pg_stat_activity.query_start,
    now() - pg_stat_activity.query_start AS query_duration
FROM pg_stat_activity
JOIN pg_locks ON pg_stat_activity.pid = pg_locks.pid
WHERE pg_stat_activity.state = 'active'
  AND pg_locks.granted = false
ORDER BY query_duration DESC;

-- =====================================================
-- PERFORMANCE OPTIMIZATION CHECKLIST
-- =====================================================

/*
1. INDEXING STRATEGY:
   - Create indexes on frequently queried columns
   - Use composite indexes for multi-column WHERE clauses
   - Consider covering indexes for SELECT columns
   - Use partial indexes for filtered queries
   - Monitor and remove unused indexes

2. QUERY OPTIMIZATION:
   - Use EXISTS instead of IN for subqueries
   - Avoid SELECT * in production queries
   - Use LIMIT to restrict result sets
   - Optimize JOIN order (smaller tables first)
   - Use appropriate data types

3. AGGREGATION OPTIMIZATION:
   - Use conditional aggregation instead of multiple queries
   - Consider materialized views for expensive aggregations
   - Use window functions instead of correlated subqueries
   - Implement proper GROUP BY strategies

4. LARGE TABLE STRATEGIES:
   - Implement table partitioning for time-series data
   - Use cursor-based pagination instead of OFFSET
   - Process data in batches for large operations
   - Consider archiving old data

5. MONITORING AND MAINTENANCE:
   - Regularly analyze query performance
   - Monitor index usage and effectiveness
   - Update table statistics regularly
   - Implement proper vacuum strategies (PostgreSQL)
   - Monitor lock contention and blocking queries

6. SCHEMA DESIGN:
   - Normalize appropriately (avoid over-normalization)
   - Use appropriate data types and constraints
   - Consider denormalization for read-heavy workloads
   - Implement proper foreign key relationships

7. CONNECTION AND RESOURCE MANAGEMENT:
   - Use connection pooling
   - Set appropriate timeout values
   - Monitor memory usage and buffer settings
   - Implement proper transaction boundaries
*/