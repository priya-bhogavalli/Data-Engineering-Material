# PostgreSQL Interview Questions

## Basic Level Questions (1-3 years experience)

### 1. What is PostgreSQL and why is it popular for data engineering?
**Answer**: PostgreSQL is an advanced open-source relational database with strong ACID compliance, extensibility, and support for both SQL and NoSQL features.

**Key Benefits for Data Engineering**:
- **ACID Compliance**: Reliable transactions for data integrity
- **JSON Support**: Handle semi-structured data natively
- **Extensibility**: Custom functions, data types, and operators
- **Parallel Processing**: Efficient query execution
- **Replication**: Built-in streaming replication

```sql
-- Example: Creating a data warehouse table
CREATE TABLE sales_fact (
    sale_id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    sale_date DATE NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(12,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Partitioning for large datasets
CREATE TABLE sales_fact_2024 PARTITION OF sales_fact
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

-- Indexes for performance
CREATE INDEX idx_sales_date ON sales_fact (sale_date);
CREATE INDEX idx_sales_customer ON sales_fact (customer_id);
CREATE INDEX idx_sales_metadata ON sales_fact USING GIN (metadata);
```

### 2. Explain PostgreSQL data types and their use cases
**Answer**: PostgreSQL offers rich data types including traditional SQL types and advanced types for complex data.

```sql
-- Numeric types
CREATE TABLE product_metrics (
    product_id INTEGER,
    price DECIMAL(10,2),        -- Exact decimal
    rating REAL,                -- Single precision float
    views BIGINT,               -- Large integers
    conversion_rate DOUBLE PRECISION
);

-- Text types
CREATE TABLE user_data (
    user_id UUID DEFAULT gen_random_uuid(),
    username VARCHAR(50) NOT NULL,
    bio TEXT,                   -- Unlimited length
    preferences JSONB,          -- Binary JSON
    tags TEXT[]                 -- Array of text
);

-- Date/Time types
CREATE TABLE events (
    event_id SERIAL,
    event_name VARCHAR(100),
    event_date DATE,
    event_time TIME,
    event_timestamp TIMESTAMP WITH TIME ZONE,
    duration INTERVAL
);

-- Advanced types
CREATE TABLE locations (
    location_id SERIAL,
    name VARCHAR(100),
    coordinates POINT,          -- Geometric point
    area POLYGON,              -- Geometric polygon
    ip_range INET,             -- Network address
    mac_address MACADDR
);

-- Custom types
CREATE TYPE order_status AS ENUM ('pending', 'processing', 'shipped', 'delivered');

CREATE TABLE orders (
    order_id SERIAL,
    status order_status DEFAULT 'pending',
    order_data JSONB
);
```

### 3. How do you optimize PostgreSQL queries?
**Answer**: Use proper indexing, query analysis, and optimization techniques.

```sql
-- Query analysis
EXPLAIN ANALYZE 
SELECT p.product_name, SUM(s.total_amount) as revenue
FROM sales_fact s
JOIN products p ON s.product_id = p.product_id
WHERE s.sale_date >= '2024-01-01'
GROUP BY p.product_id, p.product_name
ORDER BY revenue DESC;

-- Index optimization
CREATE INDEX CONCURRENTLY idx_sales_date_product 
ON sales_fact (sale_date, product_id);

-- Partial indexes
CREATE INDEX idx_active_users 
ON users (user_id) 
WHERE status = 'active';

-- Expression indexes
CREATE INDEX idx_lower_email 
ON users (LOWER(email));

-- Covering indexes
CREATE INDEX idx_sales_covering 
ON sales_fact (product_id) 
INCLUDE (total_amount, sale_date);

-- Query optimization techniques
-- Use CTEs for complex queries
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', sale_date) as month,
        product_id,
        SUM(total_amount) as monthly_revenue
    FROM sales_fact
    WHERE sale_date >= '2024-01-01'
    GROUP BY 1, 2
),
top_products AS (
    SELECT product_id, SUM(monthly_revenue) as total_revenue
    FROM monthly_sales
    GROUP BY product_id
    ORDER BY total_revenue DESC
    LIMIT 10
)
SELECT p.product_name, tp.total_revenue
FROM top_products tp
JOIN products p ON tp.product_id = p.product_id;
```

### 4. How do you handle JSON data in PostgreSQL?
**Answer**: PostgreSQL provides native JSON and JSONB support with rich operators and functions.

```sql
-- JSON vs JSONB
CREATE TABLE user_profiles (
    user_id SERIAL PRIMARY KEY,
    profile_data JSON,          -- Text-based storage
    preferences JSONB           -- Binary, indexed storage
);

-- JSON operations
INSERT INTO user_profiles (profile_data, preferences) VALUES 
('{"name": "John", "age": 30}', '{"theme": "dark", "notifications": true}');

-- Querying JSON data
SELECT user_id, profile_data->>'name' as name
FROM user_profiles
WHERE profile_data->>'age' = '30';

-- JSONB operators
SELECT user_id, preferences
FROM user_profiles
WHERE preferences ? 'theme'                    -- Key exists
  AND preferences->>'theme' = 'dark'           -- Value equals
  AND preferences @> '{"notifications": true}'; -- Contains

-- JSON aggregation
SELECT 
    jsonb_agg(
        jsonb_build_object(
            'user_id', user_id,
            'name', profile_data->>'name',
            'preferences', preferences
        )
    ) as users_summary
FROM user_profiles;

-- JSON path queries
SELECT user_id, jsonb_path_query(preferences, '$.notifications')
FROM user_profiles
WHERE jsonb_path_exists(preferences, '$.theme ? (@ == "dark")');

-- Updating JSON data
UPDATE user_profiles 
SET preferences = preferences || '{"language": "en"}'
WHERE user_id = 1;

-- Remove JSON key
UPDATE user_profiles 
SET preferences = preferences - 'old_setting'
WHERE user_id = 1;
```

### 5. Explain PostgreSQL transactions and isolation levels
**Answer**: PostgreSQL supports ACID transactions with configurable isolation levels.

```sql
-- Basic transaction
BEGIN;
    INSERT INTO orders (customer_id, total_amount) VALUES (123, 99.99);
    INSERT INTO order_items (order_id, product_id, quantity) 
    VALUES (currval('orders_order_id_seq'), 456, 2);
COMMIT;

-- Transaction with rollback
BEGIN;
    UPDATE inventory SET quantity = quantity - 5 WHERE product_id = 123;
    -- Check if quantity went negative
    IF (SELECT quantity FROM inventory WHERE product_id = 123) < 0 THEN
        ROLLBACK;
    ELSE
        COMMIT;
    END IF;

-- Isolation levels
-- Read Uncommitted
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;

-- Read Committed (default)
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- Repeatable Read
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- Serializable
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Savepoints for partial rollback
BEGIN;
    INSERT INTO audit_log (action, timestamp) VALUES ('start_process', NOW());
    SAVEPOINT sp1;
    
    UPDATE products SET price = price * 1.1 WHERE category = 'electronics';
    
    -- If something goes wrong, rollback to savepoint
    ROLLBACK TO SAVEPOINT sp1;
    
    -- Continue with different approach
    UPDATE products SET price = price * 1.05 WHERE category = 'electronics';
COMMIT;

-- Advisory locks for coordination
SELECT pg_advisory_lock(12345);
-- Critical section
SELECT pg_advisory_unlock(12345);
```

## Intermediate Level Questions (3-5 years experience)

### 6. How do you implement partitioning in PostgreSQL?
**Answer**: Use declarative partitioning for managing large tables efficiently.

```sql
-- Range partitioning by date
CREATE TABLE sales_data (
    sale_id BIGSERIAL,
    sale_date DATE NOT NULL,
    customer_id INTEGER,
    amount DECIMAL(10,2),
    region VARCHAR(50)
) PARTITION BY RANGE (sale_date);

-- Create partitions
CREATE TABLE sales_2024_q1 PARTITION OF sales_data
FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE sales_2024_q2 PARTITION OF sales_data
FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- Hash partitioning for even distribution
CREATE TABLE user_events (
    event_id BIGSERIAL,
    user_id INTEGER NOT NULL,
    event_type VARCHAR(50),
    event_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
) PARTITION BY HASH (user_id);

CREATE TABLE user_events_0 PARTITION OF user_events
FOR VALUES WITH (MODULUS 4, REMAINDER 0);

CREATE TABLE user_events_1 PARTITION OF user_events
FOR VALUES WITH (MODULUS 4, REMAINDER 1);

-- List partitioning by region
CREATE TABLE regional_sales (
    sale_id BIGSERIAL,
    region VARCHAR(50) NOT NULL,
    amount DECIMAL(10,2),
    sale_date DATE
) PARTITION BY LIST (region);

CREATE TABLE sales_north PARTITION OF regional_sales
FOR VALUES IN ('north', 'northeast', 'northwest');

CREATE TABLE sales_south PARTITION OF regional_sales
FOR VALUES IN ('south', 'southeast', 'southwest');

-- Automatic partition creation function
CREATE OR REPLACE FUNCTION create_monthly_partition(table_name TEXT, start_date DATE)
RETURNS VOID AS $$
DECLARE
    partition_name TEXT;
    end_date DATE;
BEGIN
    partition_name := table_name || '_' || TO_CHAR(start_date, 'YYYY_MM');
    end_date := start_date + INTERVAL '1 month';
    
    EXECUTE format('CREATE TABLE %I PARTITION OF %I FOR VALUES FROM (%L) TO (%L)',
                   partition_name, table_name, start_date, end_date);
END;
$$ LANGUAGE plpgsql;

-- Partition pruning example
EXPLAIN (ANALYZE, BUFFERS)
SELECT COUNT(*), AVG(amount)
FROM sales_data
WHERE sale_date BETWEEN '2024-02-01' AND '2024-02-29';
```

### 7. How do you implement replication and high availability?
**Answer**: Use streaming replication, logical replication, and connection pooling.

```sql
-- Streaming replication setup
-- On primary server (postgresql.conf)
-- wal_level = replica
-- max_wal_senders = 3
-- wal_keep_segments = 64

-- Create replication user
CREATE USER replicator REPLICATION LOGIN CONNECTION LIMIT 1 ENCRYPTED PASSWORD 'password';

-- pg_hba.conf entry
-- host replication replicator standby_ip/32 md5

-- On standby server
-- pg_basebackup -h primary_ip -D /var/lib/postgresql/data -U replicator -P -W

-- Logical replication for selective data sync
-- On publisher
CREATE PUBLICATION sales_pub FOR TABLE sales_data, products;

-- On subscriber
CREATE SUBSCRIPTION sales_sub 
CONNECTION 'host=publisher_ip dbname=mydb user=replicator password=password'
PUBLICATION sales_pub;

-- Monitor replication lag
SELECT 
    client_addr,
    state,
    pg_wal_lsn_diff(pg_current_wal_lsn(), sent_lsn) AS send_lag,
    pg_wal_lsn_diff(sent_lsn, flush_lsn) AS flush_lag
FROM pg_stat_replication;

-- Connection pooling with PgBouncer
-- pgbouncer.ini
-- [databases]
-- mydb = host=localhost port=5432 dbname=mydb
-- [pgbouncer]
-- pool_mode = transaction
-- max_client_conn = 100
-- default_pool_size = 25
```

### 8. How do you monitor and tune PostgreSQL performance?
**Answer**: Use built-in statistics, monitoring tools, and performance tuning techniques.

```sql
-- Enable query statistics
-- postgresql.conf
-- shared_preload_libraries = 'pg_stat_statements'
-- pg_stat_statements.track = all

-- Query performance analysis
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;

-- Index usage statistics
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch,
    idx_scan
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Table statistics
SELECT 
    schemaname,
    tablename,
    n_tup_ins,
    n_tup_upd,
    n_tup_del,
    n_live_tup,
    n_dead_tup,
    last_vacuum,
    last_autovacuum,
    last_analyze
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;

-- Connection and activity monitoring
SELECT 
    pid,
    usename,
    application_name,
    client_addr,
    state,
    query_start,
    state_change,
    query
FROM pg_stat_activity
WHERE state != 'idle';

-- Lock monitoring
SELECT 
    l.pid,
    l.mode,
    l.locktype,
    l.relation::regclass,
    l.granted,
    a.query
FROM pg_locks l
JOIN pg_stat_activity a ON l.pid = a.pid
WHERE NOT l.granted;

-- Vacuum and analyze automation
-- postgresql.conf tuning
-- autovacuum = on
-- autovacuum_max_workers = 3
-- autovacuum_naptime = 1min
-- autovacuum_vacuum_threshold = 50
-- autovacuum_analyze_threshold = 50

-- Manual maintenance
VACUUM ANALYZE sales_data;
REINDEX INDEX CONCURRENTLY idx_sales_date;
```

### 9. How do you implement data warehousing patterns?
**Answer**: Use dimensional modeling, ETL processes, and analytical functions.

```sql
-- Dimensional model example
-- Fact table
CREATE TABLE sales_fact (
    sale_key BIGSERIAL PRIMARY KEY,
    date_key INTEGER REFERENCES dim_date(date_key),
    product_key INTEGER REFERENCES dim_product(product_key),
    customer_key INTEGER REFERENCES dim_customer(customer_key),
    store_key INTEGER REFERENCES dim_store(store_key),
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(12,2),
    discount_amount DECIMAL(10,2)
);

-- Dimension tables
CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    day INTEGER,
    day_of_week INTEGER,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN
);

CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(50) UNIQUE,
    product_name VARCHAR(200),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    unit_cost DECIMAL(10,2)
);

-- ETL process example
CREATE OR REPLACE FUNCTION load_sales_fact()
RETURNS VOID AS $$
BEGIN
    -- Extract and transform
    INSERT INTO sales_fact (
        date_key, product_key, customer_key, store_key,
        quantity, unit_price, total_amount, discount_amount
    )
    SELECT 
        dd.date_key,
        dp.product_key,
        dc.customer_key,
        ds.store_key,
        s.quantity,
        s.unit_price,
        s.total_amount,
        s.discount_amount
    FROM staging.sales s
    JOIN dim_date dd ON s.sale_date = dd.full_date
    JOIN dim_product dp ON s.product_id = dp.product_id
    JOIN dim_customer dc ON s.customer_id = dc.customer_id
    JOIN dim_store ds ON s.store_id = ds.store_id
    WHERE s.processed_flag = FALSE;
    
    -- Mark as processed
    UPDATE staging.sales SET processed_flag = TRUE WHERE processed_flag = FALSE;
END;
$$ LANGUAGE plpgsql;

-- Analytical queries
-- Window functions for analytics
SELECT 
    product_name,
    sale_date,
    total_amount,
    SUM(total_amount) OVER (
        PARTITION BY product_key 
        ORDER BY sale_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total,
    LAG(total_amount, 1) OVER (
        PARTITION BY product_key 
        ORDER BY sale_date
    ) AS previous_sale,
    RANK() OVER (
        PARTITION BY DATE_TRUNC('month', sale_date) 
        ORDER BY total_amount DESC
    ) AS monthly_rank
FROM sales_fact sf
JOIN dim_product dp ON sf.product_key = dp.product_key
JOIN dim_date dd ON sf.date_key = dd.date_key;

-- Materialized views for performance
CREATE MATERIALIZED VIEW monthly_sales_summary AS
SELECT 
    dd.year,
    dd.month,
    dp.category,
    COUNT(*) as transaction_count,
    SUM(sf.total_amount) as total_revenue,
    AVG(sf.total_amount) as avg_transaction_value
FROM sales_fact sf
JOIN dim_date dd ON sf.date_key = dd.date_key
JOIN dim_product dp ON sf.product_key = dp.product_key
GROUP BY dd.year, dd.month, dp.category;

-- Refresh materialized view
REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_sales_summary;
```

### 10. How do you handle large-scale data operations?
**Answer**: Use bulk operations, parallel processing, and efficient data loading techniques.

```sql
-- Bulk data loading with COPY
COPY sales_staging FROM '/path/to/sales_data.csv' 
WITH (FORMAT csv, HEADER true, DELIMITER ',');

-- Parallel bulk insert
INSERT INTO sales_fact 
SELECT * FROM sales_staging
WHERE batch_id = $1;

-- Upsert operations
INSERT INTO products (product_id, product_name, price)
VALUES ('P001', 'Widget A', 19.99)
ON CONFLICT (product_id) 
DO UPDATE SET 
    product_name = EXCLUDED.product_name,
    price = EXCLUDED.price,
    updated_at = NOW();

-- Batch processing with DO blocks
DO $$
DECLARE
    batch_size INTEGER := 10000;
    total_rows INTEGER;
    processed INTEGER := 0;
BEGIN
    SELECT COUNT(*) INTO total_rows FROM staging_table WHERE processed = FALSE;
    
    WHILE processed < total_rows LOOP
        WITH batch AS (
            SELECT id FROM staging_table 
            WHERE processed = FALSE 
            ORDER BY id 
            LIMIT batch_size
        )
        UPDATE staging_table 
        SET processed = TRUE 
        WHERE id IN (SELECT id FROM batch);
        
        processed := processed + batch_size;
        RAISE NOTICE 'Processed % of % rows', processed, total_rows;
        COMMIT;
    END LOOP;
END $$;

-- Parallel query execution
SET max_parallel_workers_per_gather = 4;
SET parallel_tuple_cost = 0.1;
SET parallel_setup_cost = 1000.0;

-- Large table maintenance
-- Partitioned table maintenance
SELECT schemaname, tablename, n_dead_tup
FROM pg_stat_user_tables 
WHERE n_dead_tup > 1000000;

-- Concurrent index creation
CREATE INDEX CONCURRENTLY idx_large_table_date 
ON large_table (created_date);
```

This comprehensive set covers PostgreSQL fundamentals through advanced data warehousing and performance optimization with practical data engineering examples.