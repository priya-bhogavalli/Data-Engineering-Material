# PostgreSQL Key Concepts

## 1. PostgreSQL Fundamentals
**What is PostgreSQL**: Advanced open-source relational database with strong ACID compliance and extensibility.

**Key Features**:
- ACID transactions
- JSON/JSONB support
- Full-text search
- Window functions
- Custom data types
- Extensible with plugins

```sql
-- Connect to database
\c database_name
\l  -- List databases
\dt -- List tables
\d table_name -- Describe table
```

## 2. Data Types
```sql
-- Numeric types
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    price DECIMAL(10,2),
    quantity INTEGER,
    weight REAL
);

-- Text types
CREATE TABLE users (
    id UUID DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    bio TEXT,
    status CHAR(1) DEFAULT 'A'
);

-- Date/Time types
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    event_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    event_date DATE,
    duration INTERVAL
);

-- JSON types
CREATE TABLE user_preferences (
    user_id INTEGER,
    settings JSONB,
    metadata JSON
);
```

## 3. Advanced Queries
```sql
-- Window functions
SELECT 
    employee_id,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department) as dept_avg,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rank
FROM employees;

-- CTEs (Common Table Expressions)
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        SUM(amount) as total_sales
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
),
growth_rates AS (
    SELECT 
        month,
        total_sales,
        LAG(total_sales) OVER (ORDER BY month) as prev_month_sales,
        (total_sales - LAG(total_sales) OVER (ORDER BY month)) / 
        LAG(total_sales) OVER (ORDER BY month) * 100 as growth_rate
    FROM monthly_sales
)
SELECT * FROM growth_rates WHERE growth_rate > 10;

-- Recursive CTEs
WITH RECURSIVE employee_hierarchy AS (
    -- Base case
    SELECT employee_id, name, manager_id, 1 as level
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive case
    SELECT e.employee_id, e.name, e.manager_id, eh.level + 1
    FROM employees e
    JOIN employee_hierarchy eh ON e.manager_id = eh.employee_id
)
SELECT * FROM employee_hierarchy ORDER BY level, name;
```

## 4. JSON Operations
```sql
-- Insert JSON data
INSERT INTO user_preferences (user_id, settings) VALUES 
(1, '{"theme": "dark", "notifications": {"email": true, "sms": false}}');

-- Query JSON data
SELECT user_id, settings->>'theme' as theme
FROM user_preferences
WHERE settings->'notifications'->>'email' = 'true';

-- JSON aggregation
SELECT 
    jsonb_agg(
        jsonb_build_object(
            'name', name,
            'email', email,
            'department', department
        )
    ) as employees_json
FROM employees
WHERE department = 'Engineering';

-- Update JSON fields
UPDATE user_preferences 
SET settings = settings || '{"language": "en"}'
WHERE user_id = 1;

-- JSON path queries
SELECT user_id, jsonb_path_query(settings, '$.notifications.*') as notification_settings
FROM user_preferences;
```

## 5. Indexing Strategies
```sql
-- B-tree index (default)
CREATE INDEX idx_users_email ON users(email);

-- Partial index
CREATE INDEX idx_active_users ON users(username) WHERE status = 'A';

-- Composite index
CREATE INDEX idx_orders_date_status ON orders(order_date, status);

-- GIN index for JSON
CREATE INDEX idx_user_settings ON user_preferences USING GIN(settings);

-- Full-text search index
CREATE INDEX idx_products_search ON products USING GIN(to_tsvector('english', name || ' ' || description));

-- Expression index
CREATE INDEX idx_users_lower_email ON users(LOWER(email));

-- Check index usage
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM users WHERE email = 'user@example.com';
```

## 6. Performance Optimization
```sql
-- Analyze table statistics
ANALYZE users;
ANALYZE; -- All tables

-- Vacuum operations
VACUUM ANALYZE orders; -- Reclaim space and update stats
VACUUM FULL products;  -- Full vacuum (locks table)

-- Query optimization
EXPLAIN (ANALYZE, BUFFERS, VERBOSE) 
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= '2024-01-01'
GROUP BY u.id, u.name
HAVING COUNT(o.id) > 5;

-- Partition tables
CREATE TABLE sales_2024 (
    id SERIAL,
    sale_date DATE NOT NULL,
    amount DECIMAL(10,2),
    customer_id INTEGER
) PARTITION BY RANGE (sale_date);

CREATE TABLE sales_2024_q1 PARTITION OF sales_2024
FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE sales_2024_q2 PARTITION OF sales_2024
FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');
```

## 7. Transactions and Concurrency
```sql
-- Transaction control
BEGIN;
    INSERT INTO accounts (name, balance) VALUES ('Alice', 1000);
    INSERT INTO accounts (name, balance) VALUES ('Bob', 500);
COMMIT;

-- Savepoints
BEGIN;
    INSERT INTO orders (customer_id, amount) VALUES (1, 100);
    SAVEPOINT order_created;
    
    UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 1;
    -- If inventory update fails, rollback to savepoint
    ROLLBACK TO order_created;
    
    -- Continue with other operations
COMMIT;

-- Isolation levels
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Advisory locks
SELECT pg_advisory_lock(12345);
-- Perform critical operations
SELECT pg_advisory_unlock(12345);
```

## 8. Stored Procedures and Functions
```sql
-- PL/pgSQL function
CREATE OR REPLACE FUNCTION calculate_order_total(order_id INTEGER)
RETURNS DECIMAL(10,2) AS $$
DECLARE
    total DECIMAL(10,2) := 0;
    tax_rate DECIMAL(4,3) := 0.08;
BEGIN
    SELECT SUM(quantity * price) INTO total
    FROM order_items oi
    JOIN products p ON oi.product_id = p.id
    WHERE oi.order_id = $1;
    
    RETURN total * (1 + tax_rate);
END;
$$ LANGUAGE plpgsql;

-- Trigger function
CREATE OR REPLACE FUNCTION update_modified_time()
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_update_trigger
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_time();

-- Aggregate function
CREATE OR REPLACE FUNCTION median(numeric[])
RETURNS numeric AS $$
SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY unnest($1));
$$ LANGUAGE sql;
```

## 9. Replication and High Availability
```sql
-- Streaming replication setup (postgresql.conf)
wal_level = replica
max_wal_senders = 3
wal_keep_segments = 64
archive_mode = on
archive_command = 'cp %p /archive/%f'

-- Create replication user
CREATE USER replicator REPLICATION LOGIN PASSWORD 'password';

-- Monitor replication
SELECT 
    client_addr,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    sync_state
FROM pg_stat_replication;

-- Logical replication
CREATE PUBLICATION sales_pub FOR TABLE sales, customers;

-- On subscriber
CREATE SUBSCRIPTION sales_sub 
CONNECTION 'host=primary_host dbname=mydb user=replicator' 
PUBLICATION sales_pub;
```

## 10. Monitoring and Maintenance
```sql
-- Database statistics
SELECT 
    schemaname,
    tablename,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes,
    n_live_tup as live_rows,
    n_dead_tup as dead_rows
FROM pg_stat_user_tables
ORDER BY n_tup_ins + n_tup_upd + n_tup_del DESC;

-- Index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch,
    idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0;  -- Unused indexes

-- Long running queries
SELECT 
    pid,
    now() - pg_stat_activity.query_start AS duration,
    query,
    state
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes'
AND state = 'active';

-- Database size
SELECT 
    datname,
    pg_size_pretty(pg_database_size(datname)) as size
FROM pg_database
ORDER BY pg_database_size(datname) DESC;

-- Table bloat analysis
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as table_size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) as index_size
FROM pg_tables
WHERE schemaname NOT IN ('information_schema', 'pg_catalog')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```