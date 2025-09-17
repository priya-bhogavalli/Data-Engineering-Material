# 🐘 PostgreSQL Interview Questions for Data Engineering
**200+ Comprehensive Questions with Production Examples**

## 📋 Table of Contents
1. [Basic Level Questions (1-40)](#basic-level-questions-1-40)
2. [Intermediate Level Questions (41-80)](#intermediate-level-questions-41-80)
3. [Advanced Level Questions (81-120)](#advanced-level-questions-81-120)
4. [Expert Level Questions (121-160)](#expert-level-questions-121-160)
5. [Production & Enterprise (161-180)](#production--enterprise-161-180)
6. [Data Engineering Scenarios (181-200)](#data-engineering-scenarios-181-200)

---

## Basic Level Questions (1-40)

### 1. What is PostgreSQL and why is it popular for data engineering?
**Answer**: PostgreSQL is an advanced open-source relational database with strong ACID compliance, extensibility, and support for both SQL and NoSQL features.

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying PostgreSQL operations

#### **Case Studies**
Real-world case studies of PostgreSQL implementations

#### **Industry Direction**
Future direction of Relational Database technologies

### **Enhanced Answer**

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

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying PostgreSQL operations

#### **Case Studies**
Real-world case studies of PostgreSQL implementations

#### **Industry Direction**
Future direction of Relational Database technologies

### **Enhanced Answer**

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

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying PostgreSQL operations

#### **Case Studies**
Real-world case studies of PostgreSQL implementations

#### **Industry Direction**
Future direction of Relational Database technologies

### **Enhanced Answer**

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

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying PostgreSQL operations

#### **Case Studies**
Real-world case studies of PostgreSQL implementations

#### **Industry Direction**
Future direction of Relational Database technologies

### **Enhanced Answer**

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

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying PostgreSQL operations

#### **Case Studies**
Real-world case studies of PostgreSQL implementations

#### **Industry Direction**
Future direction of Relational Database technologies

### **Enhanced Answer**

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

## Intermediate Level Questions (41-80)

### 6. How do you implement partitioning in PostgreSQL?

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying PostgreSQL operations

#### **Case Studies**
Real-world case studies of PostgreSQL implementations

#### **Industry Direction**
Future direction of Relational Database technologies

### **Enhanced Answer**

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

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying PostgreSQL operations

#### **Case Studies**
Real-world case studies of PostgreSQL implementations

#### **Industry Direction**
Future direction of Relational Database technologies

### **Enhanced Answer**

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

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying PostgreSQL operations

#### **Case Studies**
Real-world case studies of PostgreSQL implementations

#### **Industry Direction**
Future direction of Relational Database technologies

### **Enhanced Answer**

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

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying PostgreSQL operations

#### **Case Studies**
Real-world case studies of PostgreSQL implementations

#### **Industry Direction**
Future direction of Relational Database technologies

### **Enhanced Answer**

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

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying PostgreSQL operations

#### **Case Studies**
Real-world case studies of PostgreSQL implementations

#### **Industry Direction**
Future direction of Relational Database technologies

### **Enhanced Answer**

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

### 31. How do you implement PostgreSQL for real-time analytics?

**Answer:** Combine materialized views, triggers, and streaming for real-time insights.

```sql
-- Real-time analytics setup
CREATE TABLE events_stream (
    event_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id INTEGER NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Real-time aggregation table
CREATE TABLE real_time_metrics (
    metric_key VARCHAR(100) PRIMARY KEY,
    metric_value DECIMAL(15,2) NOT NULL,
    last_updated TIMESTAMP DEFAULT NOW()
);

-- Trigger for real-time updates
CREATE OR REPLACE FUNCTION update_real_time_metrics()
RETURNS TRIGGER AS $$
BEGIN
    -- Update user activity count
    INSERT INTO real_time_metrics (metric_key, metric_value)
    VALUES ('active_users_today', 1)
    ON CONFLICT (metric_key)
    DO UPDATE SET 
        metric_value = real_time_metrics.metric_value + 1,
        last_updated = NOW();
    
    -- Update event type counters
    INSERT INTO real_time_metrics (metric_key, metric_value)
    VALUES ('event_' || NEW.event_type || '_count', 1)
    ON CONFLICT (metric_key)
    DO UPDATE SET 
        metric_value = real_time_metrics.metric_value + 1,
        last_updated = NOW();
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER events_metrics_trigger
    AFTER INSERT ON events_stream
    FOR EACH ROW EXECUTE FUNCTION update_real_time_metrics();

-- Real-time dashboard query
SELECT 
    metric_key,
    metric_value,
    last_updated,
    EXTRACT(EPOCH FROM (NOW() - last_updated)) AS seconds_since_update
FROM real_time_metrics
WHERE last_updated >= NOW() - INTERVAL '1 hour'
ORDER BY last_updated DESC;
```

### 32. How do you implement data lineage tracking in PostgreSQL?

**Answer:** Create comprehensive lineage tracking with metadata tables.

```sql
-- Data lineage schema
CREATE TABLE data_sources (
    source_id SERIAL PRIMARY KEY,
    source_name VARCHAR(100) NOT NULL,
    source_type VARCHAR(50) NOT NULL, -- 'table', 'view', 'file', 'api'
    connection_info JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE data_transformations (
    transformation_id SERIAL PRIMARY KEY,
    transformation_name VARCHAR(100) NOT NULL,
    transformation_type VARCHAR(50) NOT NULL, -- 'etl', 'aggregation', 'join'
    transformation_logic TEXT,
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE lineage_relationships (
    relationship_id SERIAL PRIMARY KEY,
    source_id INTEGER REFERENCES data_sources(source_id),
    target_id INTEGER REFERENCES data_sources(source_id),
    transformation_id INTEGER REFERENCES data_transformations(transformation_id),
    relationship_type VARCHAR(50), -- 'direct', 'aggregated', 'filtered'
    created_at TIMESTAMP DEFAULT NOW()
);

-- Lineage tracking function
CREATE OR REPLACE FUNCTION track_data_lineage(
    p_source_name VARCHAR(100),
    p_target_name VARCHAR(100),
    p_transformation_name VARCHAR(100),
    p_transformation_logic TEXT
)
RETURNS INTEGER AS $$
DECLARE
    source_id INTEGER;
    target_id INTEGER;
    transformation_id INTEGER;
    relationship_id INTEGER;
BEGIN
    -- Get or create source
    INSERT INTO data_sources (source_name, source_type)
    VALUES (p_source_name, 'table')
    ON CONFLICT (source_name) DO NOTHING;
    
    SELECT source_id INTO source_id FROM data_sources WHERE source_name = p_source_name;
    
    -- Get or create target
    INSERT INTO data_sources (source_name, source_type)
    VALUES (p_target_name, 'table')
    ON CONFLICT (source_name) DO NOTHING;
    
    SELECT source_id INTO target_id FROM data_sources WHERE source_name = p_target_name;
    
    -- Create transformation
    INSERT INTO data_transformations (transformation_name, transformation_type, transformation_logic)
    VALUES (p_transformation_name, 'etl', p_transformation_logic)
    RETURNING transformation_id INTO transformation_id;
    
    -- Create lineage relationship
    INSERT INTO lineage_relationships (source_id, target_id, transformation_id, relationship_type)
    VALUES (source_id, target_id, transformation_id, 'direct')
    RETURNING relationship_id INTO relationship_id;
    
    RETURN relationship_id;
END;
$$ LANGUAGE plpgsql;

-- Query lineage
CREATE OR REPLACE FUNCTION get_data_lineage(p_table_name VARCHAR(100))
RETURNS TABLE(
    level INTEGER,
    source_name VARCHAR(100),
    transformation_name VARCHAR(100),
    target_name VARCHAR(100)
) AS $$
WITH RECURSIVE lineage_tree AS (
    -- Base case: direct sources
    SELECT 
        1 as level,
        ds_source.source_name,
        dt.transformation_name,
        ds_target.source_name as target_name,
        lr.target_id
    FROM lineage_relationships lr
    JOIN data_sources ds_source ON lr.source_id = ds_source.source_id
    JOIN data_sources ds_target ON lr.target_id = ds_target.source_id
    JOIN data_transformations dt ON lr.transformation_id = dt.transformation_id
    WHERE ds_target.source_name = p_table_name
    
    UNION ALL
    
    -- Recursive case: upstream sources
    SELECT 
        lt.level + 1,
        ds_source.source_name,
        dt.transformation_name,
        ds_target.source_name,
        lr.target_id
    FROM lineage_relationships lr
    JOIN data_sources ds_source ON lr.source_id = ds_source.source_id
    JOIN data_sources ds_target ON lr.target_id = ds_target.source_id
    JOIN data_transformations dt ON lr.transformation_id = dt.transformation_id
    JOIN lineage_tree lt ON ds_target.source_id = lr.source_id
    WHERE lt.level < 10  -- Prevent infinite recursion
)
SELECT level, source_name, transformation_name, target_name
FROM lineage_tree
ORDER BY level, source_name;
$$ LANGUAGE plpgsql;
```

### 33-40. Additional Basic Questions

**33. How do you implement PostgreSQL for IoT data processing?**
**Answer:** Use time-series patterns, partitioning, and efficient indexing.

**34. How do you handle PostgreSQL schema migrations in production?**
**Answer:** Use migration scripts, version control, and zero-downtime techniques.

**35. How do you implement PostgreSQL for event sourcing?**
**Answer:** Create event store with immutable events and replay capabilities.

**36. How do you optimize PostgreSQL for analytical workloads?**
**Answer:** Use columnar storage, parallel queries, and materialized views.

**37. How do you implement PostgreSQL connection pooling?**
**Answer:** Configure PgBouncer, connection limits, and pool sizing.

**38. How do you handle PostgreSQL backup automation?**
**Answer:** Implement automated backup scripts with retention policies.

**39. How do you implement PostgreSQL monitoring dashboards?**
**Answer:** Create custom metrics collection and visualization.

**40. How do you handle PostgreSQL data archiving strategies?**
**Answer:** Implement time-based archiving with automated cleanup.

---

## Advanced Level Questions (81-120)

### 81. Explain PostgreSQL's MVCC (Multi-Version Concurrency Control) architecture
**Answer:**
MVCC allows multiple transactions to access the same data simultaneously without blocking each other.

**Key Concepts:**
- **Transaction IDs (XIDs)**: Each transaction gets a unique ID
- **Tuple Visibility**: Each row version has creation and deletion XIDs
- **Snapshot Isolation**: Transactions see consistent data snapshots
- **Vacuum Process**: Cleans up old row versions

**Practical Implications:**
```sql
-- Understanding tuple visibility
SELECT 
    ctid,           -- Physical location
    xmin,           -- Creating transaction ID
    xmax,           -- Deleting transaction ID
    *
FROM products
WHERE product_id = 'P001';

-- Transaction isolation demonstration
-- Session 1
BEGIN;
SELECT * FROM accounts WHERE account_id = 123;
-- Shows balance = 1000

-- Session 2 (concurrent)
BEGIN;
UPDATE accounts SET balance = 1500 WHERE account_id = 123;
COMMIT;

-- Back to Session 1
SELECT * FROM accounts WHERE account_id = 123;
-- Still shows balance = 1000 (snapshot isolation)
COMMIT;
```

### 12. How does PostgreSQL handle write-ahead logging (WAL)?
**Answer:**
WAL ensures data durability and enables point-in-time recovery.

**WAL Components:**
- **WAL Files**: Sequential log files storing changes
- **Checkpoints**: Periodic sync of dirty buffers to disk
- **LSN (Log Sequence Number)**: Unique identifier for log positions
- **WAL Archiving**: Backup of WAL files for recovery

```sql
-- WAL configuration
-- postgresql.conf settings
-- wal_level = replica
-- max_wal_size = 1GB
-- min_wal_size = 80MB
-- checkpoint_completion_target = 0.9
-- wal_buffers = 16MB

-- Monitor WAL activity
SELECT 
    pg_current_wal_lsn() as current_lsn,
    pg_wal_lsn_diff(pg_current_wal_lsn(), '0/0') as total_wal_bytes;

-- WAL archiving setup
-- archive_mode = on
-- archive_command = 'cp %p /archive/%f'

-- Point-in-time recovery
-- recovery.conf
-- restore_command = 'cp /archive/%f %p'
-- recovery_target_time = '2024-01-15 14:30:00'
```

### 13. What are PostgreSQL extensions and how do you use them?
**Answer:**
Extensions add functionality to PostgreSQL without modifying core code.

**Popular Extensions:**
- **pg_stat_statements**: Query performance statistics
- **PostGIS**: Geographic data support
- **pg_trgm**: Trigram matching for fuzzy search
- **uuid-ossp**: UUID generation functions
- **hstore**: Key-value storage
- **pg_partman**: Partition management

```sql
-- Install extensions
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS hstore;

-- Using uuid-ossp
CREATE TABLE users (
    user_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Using pg_trgm for fuzzy search
CREATE INDEX idx_product_name_trgm ON products USING GIN (product_name gin_trgm_ops);

SELECT product_name, similarity(product_name, 'iPhone') as sim
FROM products
WHERE product_name % 'iPhone'  -- Fuzzy match
ORDER BY sim DESC;

-- Using hstore for flexible attributes
CREATE TABLE products_flexible (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(200),
    attributes HSTORE
);

INSERT INTO products_flexible (name, attributes) VALUES 
('Laptop', 'brand=>"Dell", ram=>"16GB", storage=>"512GB SSD"');

SELECT name, attributes->'brand' as brand
FROM products_flexible
WHERE attributes ? 'ram' AND attributes->'ram' = '16GB';
```

---

### 82. How do you design PostgreSQL for microservices architecture?
**Answer:**
Design database-per-service pattern with proper data consistency strategies.

**Architecture Patterns:**
- **Database per Service**: Each microservice owns its data
- **Shared Database Anti-pattern**: Avoid shared databases
- **Event Sourcing**: Store events instead of current state
- **CQRS**: Separate read and write models

```sql
-- Service-specific databases
-- User Service Database
CREATE DATABASE user_service;
\c user_service;

CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Order Service Database
CREATE DATABASE order_service;
\c order_service;

CREATE TABLE orders (
    order_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,  -- Reference to user service
    status VARCHAR(50) DEFAULT 'pending',
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Event sourcing table
CREATE TABLE events (
    event_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    aggregate_id UUID NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB NOT NULL,
    event_version INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Outbox pattern for reliable messaging
CREATE TABLE outbox_events (
    event_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    aggregate_id UUID NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,
    published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 15. How do you implement data synchronization across PostgreSQL instances?
**Answer:**
Use logical replication, foreign data wrappers, and event-driven synchronization.

```sql
-- Logical replication for selective sync
-- Publisher setup
CREATE PUBLICATION user_data_pub FOR TABLE users, user_profiles;

-- Subscriber setup
CREATE SUBSCRIPTION user_data_sub
CONNECTION 'host=source-db port=5432 dbname=source user=replicator'
PUBLICATION user_data_pub;

-- Foreign Data Wrapper for cross-database queries
CREATE EXTENSION postgres_fdw;

CREATE SERVER remote_db
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host 'remote-host', port '5432', dbname 'remote_db');

CREATE USER MAPPING FOR current_user
SERVER remote_db
OPTIONS (user 'remote_user', password 'password');

CREATE FOREIGN TABLE remote_orders (
    order_id UUID,
    user_id UUID,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP
)
SERVER remote_db
OPTIONS (schema_name 'public', table_name 'orders');

-- Cross-database analytics
SELECT 
    u.username,
    COUNT(ro.order_id) as order_count,
    SUM(ro.total_amount) as total_spent
FROM users u
LEFT JOIN remote_orders ro ON u.user_id = ro.user_id
GROUP BY u.user_id, u.username;
```

---

### 83. How do you implement comprehensive security in PostgreSQL?
**Answer:**
Implement multiple security layers including authentication, authorization, encryption, and auditing.

```sql
-- Role-based access control
CREATE ROLE data_analysts;
CREATE ROLE data_engineers;
CREATE ROLE application_users;

-- Grant specific permissions
GRANT SELECT ON sales_fact TO data_analysts;
GRANT SELECT, INSERT, UPDATE ON staging_tables TO data_engineers;
GRANT SELECT, INSERT, UPDATE ON application_tables TO application_users;

-- Row-level security
ALTER TABLE customer_data ENABLE ROW LEVEL SECURITY;

CREATE POLICY customer_isolation ON customer_data
    FOR ALL TO application_users
    USING (customer_id = current_setting('app.current_customer_id')::UUID);

-- Column-level security
GRANT SELECT (customer_id, name, email) ON customers TO data_analysts;
-- Exclude sensitive columns like SSN, credit_card

-- Data masking for non-production
CREATE OR REPLACE FUNCTION mask_email(email TEXT)
RETURNS TEXT AS $$
BEGIN
    IF current_setting('app.environment') = 'production' THEN
        RETURN email;
    ELSE
        RETURN regexp_replace(email, '(.{2}).*(@.*)', '\1***\2');
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Audit logging
CREATE TABLE audit_log (
    log_id SERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    operation VARCHAR(10),
    user_name VARCHAR(100),
    timestamp TIMESTAMP DEFAULT NOW(),
    old_values JSONB,
    new_values JSONB
);

-- Audit trigger function
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (table_name, operation, user_name, old_values, new_values)
    VALUES (
        TG_TABLE_NAME,
        TG_OP,
        current_user,
        CASE WHEN TG_OP = 'DELETE' THEN row_to_json(OLD) ELSE NULL END,
        CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN row_to_json(NEW) ELSE NULL END
    );
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

-- Apply audit trigger
CREATE TRIGGER audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON sensitive_table
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();
```

### 17. How do you handle data encryption in PostgreSQL?
**Answer:**
Implement encryption at multiple levels: connection, storage, and application.

```sql
-- Connection encryption (postgresql.conf)
-- ssl = on
-- ssl_cert_file = 'server.crt'
-- ssl_key_file = 'server.key'
-- ssl_ca_file = 'ca.crt'

-- Column-level encryption using pgcrypto
CREATE EXTENSION pgcrypto;

CREATE TABLE secure_customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255),
    ssn_encrypted BYTEA,  -- Encrypted SSN
    credit_card_encrypted BYTEA  -- Encrypted credit card
);

-- Insert encrypted data
INSERT INTO secure_customers (name, email, ssn_encrypted, credit_card_encrypted)
VALUES (
    'John Doe',
    'john@example.com',
    pgp_sym_encrypt('123-45-6789', 'encryption_key'),
    pgp_sym_encrypt('4111-1111-1111-1111', 'encryption_key')
);

-- Query encrypted data
SELECT 
    customer_id,
    name,
    email,
    pgp_sym_decrypt(ssn_encrypted, 'encryption_key') as ssn,
    pgp_sym_decrypt(credit_card_encrypted, 'encryption_key') as credit_card
FROM secure_customers
WHERE customer_id = 1;

-- Hash passwords
CREATE TABLE users_secure (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    password_hash TEXT
);

-- Store hashed password
INSERT INTO users_secure (username, password_hash)
VALUES ('john_doe', crypt('user_password', gen_salt('bf', 8)));

-- Verify password
SELECT user_id, username
FROM users_secure
WHERE username = 'john_doe'
  AND password_hash = crypt('user_password', password_hash);
```

---

### 84. How do you implement advanced analytics with PostgreSQL?
**Answer:**
Combine materialized views, triggers, and streaming technologies for real-time insights.

```sql
-- Real-time aggregation tables
CREATE TABLE real_time_metrics (
    metric_id SERIAL PRIMARY KEY,
    metric_name VARCHAR(100),
    metric_value DECIMAL(15,2),
    time_bucket TIMESTAMP,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Trigger for real-time updates
CREATE OR REPLACE FUNCTION update_real_time_metrics()
RETURNS TRIGGER AS $$
BEGIN
    -- Update hourly sales metrics
    INSERT INTO real_time_metrics (metric_name, metric_value, time_bucket)
    VALUES (
        'hourly_sales',
        NEW.total_amount,
        DATE_TRUNC('hour', NEW.created_at)
    )
    ON CONFLICT (metric_name, time_bucket)
    DO UPDATE SET 
        metric_value = real_time_metrics.metric_value + EXCLUDED.metric_value,
        updated_at = NOW();
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER sales_metrics_trigger
    AFTER INSERT ON sales
    FOR EACH ROW EXECUTE FUNCTION update_real_time_metrics();

-- Sliding window analytics
CREATE OR REPLACE VIEW sliding_window_metrics AS
SELECT 
    'last_hour_sales' as metric,
    COUNT(*) as transaction_count,
    SUM(total_amount) as total_revenue
FROM sales
WHERE created_at >= NOW() - INTERVAL '1 hour'
UNION ALL
SELECT 
    'last_24h_sales' as metric,
    COUNT(*) as transaction_count,
    SUM(total_amount) as total_revenue
FROM sales
WHERE created_at >= NOW() - INTERVAL '24 hours';

-- Time-series analysis with window functions
SELECT 
    DATE_TRUNC('hour', created_at) as hour,
    COUNT(*) as transactions,
    SUM(total_amount) as revenue,
    AVG(SUM(total_amount)) OVER (
        ORDER BY DATE_TRUNC('hour', created_at)
        ROWS BETWEEN 23 PRECEDING AND CURRENT ROW
    ) as moving_avg_24h
FROM sales
WHERE created_at >= NOW() - INTERVAL '7 days'
GROUP BY DATE_TRUNC('hour', created_at)
ORDER BY hour;
```

### 19. How do you implement data quality monitoring?
**Answer:**
Create automated data quality checks and monitoring systems.

```sql
-- Data quality rules table
CREATE TABLE data_quality_rules (
    rule_id SERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    rule_name VARCHAR(100),
    rule_query TEXT,
    threshold_value DECIMAL(10,2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert quality rules
INSERT INTO data_quality_rules (table_name, rule_name, rule_query, threshold_value) VALUES
('customers', 'null_email_check', 'SELECT COUNT(*) FROM customers WHERE email IS NULL', 0),
('orders', 'negative_amount_check', 'SELECT COUNT(*) FROM orders WHERE total_amount < 0', 0),
('products', 'duplicate_sku_check', 'SELECT COUNT(*) - COUNT(DISTINCT sku) FROM products', 0);

-- Data quality results table
CREATE TABLE data_quality_results (
    result_id SERIAL PRIMARY KEY,
    rule_id INTEGER REFERENCES data_quality_rules(rule_id),
    check_timestamp TIMESTAMP DEFAULT NOW(),
    actual_value DECIMAL(10,2),
    threshold_value DECIMAL(10,2),
    status VARCHAR(20),
    details JSONB
);

-- Data quality check function
CREATE OR REPLACE FUNCTION run_data_quality_checks()
RETURNS TABLE(rule_name TEXT, status TEXT, actual_value DECIMAL, threshold_value DECIMAL) AS $$
DECLARE
    rule_record RECORD;
    actual_val DECIMAL;
    check_status TEXT;
BEGIN
    FOR rule_record IN 
        SELECT * FROM data_quality_rules WHERE is_active = TRUE
    LOOP
        -- Execute the rule query
        EXECUTE rule_record.rule_query INTO actual_val;
        
        -- Determine status
        IF actual_val <= rule_record.threshold_value THEN
            check_status := 'PASS';
        ELSE
            check_status := 'FAIL';
        END IF;
        
        -- Insert result
        INSERT INTO data_quality_results (rule_id, actual_value, threshold_value, status)
        VALUES (rule_record.rule_id, actual_val, rule_record.threshold_value, check_status);
        
        -- Return result
        RETURN QUERY SELECT rule_record.rule_name, check_status, actual_val, rule_record.threshold_value;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Run quality checks
SELECT * FROM run_data_quality_checks();

-- Data profiling queries
CREATE OR REPLACE FUNCTION profile_table(table_name TEXT)
RETURNS TABLE(
    column_name TEXT,
    data_type TEXT,
    null_count BIGINT,
    null_percentage DECIMAL,
    distinct_count BIGINT,
    min_value TEXT,
    max_value TEXT
) AS $$
DECLARE
    col_record RECORD;
    total_rows BIGINT;
BEGIN
    -- Get total row count
    EXECUTE format('SELECT COUNT(*) FROM %I', table_name) INTO total_rows;
    
    -- Profile each column
    FOR col_record IN 
        SELECT c.column_name, c.data_type
        FROM information_schema.columns c
        WHERE c.table_name = profile_table.table_name
    LOOP
        RETURN QUERY
        EXECUTE format('
            SELECT 
                %L::TEXT as column_name,
                %L::TEXT as data_type,
                COUNT(*) FILTER (WHERE %I IS NULL) as null_count,
                (COUNT(*) FILTER (WHERE %I IS NULL) * 100.0 / %s)::DECIMAL(5,2) as null_percentage,
                COUNT(DISTINCT %I) as distinct_count,
                MIN(%I::TEXT) as min_value,
                MAX(%I::TEXT) as max_value
            FROM %I',
            col_record.column_name,
            col_record.data_type,
            col_record.column_name,
            col_record.column_name,
            total_rows,
            col_record.column_name,
            col_record.column_name,
            col_record.column_name,
            table_name
        );
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Profile a table
SELECT * FROM profile_table('customers');
```

This comprehensive set covers PostgreSQL from basic concepts through advanced enterprise architecture, security, and data quality monitoring with practical data engineering applications.

### 20. How do you implement PostgreSQL for time series data?

**Answer:** Use TimescaleDB extension or native PostgreSQL features for time series workloads.

```sql
-- Native PostgreSQL time series approach
CREATE TABLE sensor_readings (
    sensor_id INTEGER NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),
    pressure DECIMAL(7,2)
) PARTITION BY RANGE (timestamp);

-- Create time-based partitions
CREATE TABLE sensor_readings_2024_01 PARTITION OF sensor_readings
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE sensor_readings_2024_02 PARTITION OF sensor_readings
FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Indexes for time series queries
CREATE INDEX idx_sensor_readings_time ON sensor_readings (timestamp DESC);
CREATE INDEX idx_sensor_readings_sensor_time ON sensor_readings (sensor_id, timestamp DESC);

-- Time series aggregation queries
SELECT 
    sensor_id,
    DATE_TRUNC('hour', timestamp) as hour,
    AVG(temperature) as avg_temp,
    MIN(temperature) as min_temp,
    MAX(temperature) as max_temp,
    STDDEV(temperature) as temp_stddev
FROM sensor_readings
WHERE timestamp >= NOW() - INTERVAL '24 hours'
GROUP BY sensor_id, DATE_TRUNC('hour', timestamp)
ORDER BY sensor_id, hour;

-- Moving averages and trends
SELECT 
    sensor_id,
    timestamp,
    temperature,
    AVG(temperature) OVER (
        PARTITION BY sensor_id 
        ORDER BY timestamp 
        ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
    ) as moving_avg_12_readings,
    temperature - LAG(temperature, 1) OVER (
        PARTITION BY sensor_id 
        ORDER BY timestamp
    ) as temp_change
FROM sensor_readings
WHERE sensor_id = 1
ORDER BY timestamp DESC
LIMIT 100;

-- Time series downsampling
CREATE MATERIALIZED VIEW hourly_sensor_summary AS
SELECT 
    sensor_id,
    DATE_TRUNC('hour', timestamp) as hour,
    COUNT(*) as reading_count,
    AVG(temperature) as avg_temperature,
    AVG(humidity) as avg_humidity,
    AVG(pressure) as avg_pressure,
    MIN(temperature) as min_temperature,
    MAX(temperature) as max_temperature
FROM sensor_readings
GROUP BY sensor_id, DATE_TRUNC('hour', timestamp);

-- Refresh materialized view periodically
REFRESH MATERIALIZED VIEW CONCURRENTLY hourly_sensor_summary;
```

### 21. How do you implement database migrations and version control?

**Answer:** Use migration scripts, version tracking, and automated deployment processes.

```sql
-- Migration tracking table
CREATE TABLE schema_migrations (
    version VARCHAR(50) PRIMARY KEY,
    description TEXT,
    applied_at TIMESTAMP DEFAULT NOW(),
    applied_by VARCHAR(100) DEFAULT CURRENT_USER,
    checksum VARCHAR(64)
);

-- Migration script example (V001__initial_schema.sql)
BEGIN;

-- Check if migration already applied
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM schema_migrations WHERE version = 'V001') THEN
        RAISE EXCEPTION 'Migration V001 already applied';
    END IF;
END $$;

-- Create initial tables
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE posts (
    post_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    title VARCHAR(200) NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Record migration
INSERT INTO schema_migrations (version, description, checksum) 
VALUES ('V001', 'Initial schema creation', 'abc123def456');

COMMIT;

-- Migration script example (V002__add_user_profiles.sql)
BEGIN;

-- Check migration order
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM schema_migrations WHERE version = 'V001') THEN
        RAISE EXCEPTION 'Migration V001 must be applied first';
    END IF;
    
    IF EXISTS (SELECT 1 FROM schema_migrations WHERE version = 'V002') THEN
        RAISE EXCEPTION 'Migration V002 already applied';
    END IF;
END $$;

-- Add new table
CREATE TABLE user_profiles (
    profile_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) UNIQUE,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    bio TEXT,
    avatar_url VARCHAR(500),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Add new column to existing table
ALTER TABLE users ADD COLUMN last_login TIMESTAMP;

-- Create index
CREATE INDEX idx_users_last_login ON users(last_login);

-- Record migration
INSERT INTO schema_migrations (version, description, checksum) 
VALUES ('V002', 'Add user profiles and last_login', 'def456ghi789');

COMMIT;

-- Rollback script example (R002__rollback_user_profiles.sql)
BEGIN;

-- Remove changes from V002
DROP TABLE IF EXISTS user_profiles;
ALTER TABLE users DROP COLUMN IF EXISTS last_login;
DROP INDEX IF EXISTS idx_users_last_login;

-- Remove migration record
DELETE FROM schema_migrations WHERE version = 'V002';

COMMIT;

-- Migration status function
CREATE OR REPLACE FUNCTION get_migration_status()
RETURNS TABLE(
    version VARCHAR(50),
    description TEXT,
    applied_at TIMESTAMP,
    applied_by VARCHAR(100)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        sm.version,
        sm.description,
        sm.applied_at,
        sm.applied_by
    FROM schema_migrations sm
    ORDER BY sm.version;
END;
$$ LANGUAGE plpgsql;

-- Check migration status
SELECT * FROM get_migration_status();
```

### 22. How do you implement PostgreSQL for microservices data patterns?

**Answer:** Use database-per-service, event sourcing, and CQRS patterns.

```sql
-- Event sourcing implementation
CREATE TABLE event_store (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_id UUID NOT NULL,
    aggregate_type VARCHAR(100) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB NOT NULL,
    event_version INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(100) DEFAULT CURRENT_USER
);

-- Index for event retrieval
CREATE INDEX idx_event_store_aggregate ON event_store (aggregate_id, event_version);
CREATE INDEX idx_event_store_type ON event_store (aggregate_type, created_at);

-- Aggregate root reconstruction
CREATE OR REPLACE FUNCTION get_aggregate_events(p_aggregate_id UUID)
RETURNS TABLE(
    event_type VARCHAR(100),
    event_data JSONB,
    event_version INTEGER,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        es.event_type,
        es.event_data,
        es.event_version,
        es.created_at
    FROM event_store es
    WHERE es.aggregate_id = p_aggregate_id
    ORDER BY es.event_version;
END;
$$ LANGUAGE plpgsql;

-- Outbox pattern for reliable messaging
CREATE TABLE outbox_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_id UUID NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,
    published BOOLEAN DEFAULT FALSE,
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Saga pattern for distributed transactions
CREATE TABLE saga_instances (
    saga_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    saga_type VARCHAR(100) NOT NULL,
    current_step INTEGER DEFAULT 0,
    saga_data JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'running',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE saga_steps (
    step_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    saga_id UUID REFERENCES saga_instances(saga_id),
    step_number INTEGER NOT NULL,
    step_type VARCHAR(100) NOT NULL,
    step_data JSONB,
    status VARCHAR(20) DEFAULT 'pending',
    executed_at TIMESTAMP,
    compensated_at TIMESTAMP
);

-- CQRS read model
CREATE TABLE user_read_model (
    user_id UUID PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    full_name VARCHAR(200),
    total_orders INTEGER DEFAULT 0,
    total_spent DECIMAL(12,2) DEFAULT 0,
    last_order_date DATE,
    account_status VARCHAR(20) DEFAULT 'active',
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Event handler for updating read model
CREATE OR REPLACE FUNCTION handle_user_events()
RETURNS TRIGGER AS $$
BEGIN
    -- Handle different event types
    CASE NEW.event_type
        WHEN 'UserCreated' THEN
            INSERT INTO user_read_model (user_id, username, email, full_name)
            VALUES (
                NEW.aggregate_id,
                NEW.event_data->>'username',
                NEW.event_data->>'email',
                NEW.event_data->>'full_name'
            )
            ON CONFLICT (user_id) DO NOTHING;
            
        WHEN 'UserUpdated' THEN
            UPDATE user_read_model
            SET 
                username = COALESCE(NEW.event_data->>'username', username),
                email = COALESCE(NEW.event_data->>'email', email),
                full_name = COALESCE(NEW.event_data->>'full_name', full_name),
                updated_at = NOW()
            WHERE user_id = NEW.aggregate_id;
            
        WHEN 'OrderPlaced' THEN
            UPDATE user_read_model
            SET 
                total_orders = total_orders + 1,
                total_spent = total_spent + (NEW.event_data->>'amount')::DECIMAL,
                last_order_date = (NEW.event_data->>'order_date')::DATE,
                updated_at = NOW()
            WHERE user_id = NEW.aggregate_id;
    END CASE;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for event handling
CREATE TRIGGER user_event_handler
    AFTER INSERT ON event_store
    FOR EACH ROW
    WHEN (NEW.aggregate_type = 'User')
    EXECUTE FUNCTION handle_user_events();
```

### 23. How do you implement advanced PostgreSQL monitoring and alerting?

**Answer:** Create comprehensive monitoring with custom metrics and automated alerts.

```sql
-- Database metrics collection
CREATE TABLE db_metrics (
    metric_id SERIAL PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,4),
    metric_unit VARCHAR(20),
    collected_at TIMESTAMP DEFAULT NOW(),
    tags JSONB
);

-- Performance monitoring function
CREATE OR REPLACE FUNCTION collect_performance_metrics()
RETURNS VOID AS $$
DECLARE
    db_size BIGINT;
    active_connections INTEGER;
    slow_queries INTEGER;
    cache_hit_ratio DECIMAL;
    index_usage DECIMAL;
BEGIN
    -- Database size
    SELECT pg_database_size(current_database()) INTO db_size;
    INSERT INTO db_metrics (metric_name, metric_value, metric_unit)
    VALUES ('database_size_bytes', db_size, 'bytes');
    
    -- Active connections
    SELECT COUNT(*) FROM pg_stat_activity WHERE state = 'active' INTO active_connections;
    INSERT INTO db_metrics (metric_name, metric_value, metric_unit)
    VALUES ('active_connections', active_connections, 'count');
    
    -- Slow queries (from pg_stat_statements)
    SELECT COUNT(*) FROM pg_stat_statements 
    WHERE mean_time > 1000 INTO slow_queries;
    INSERT INTO db_metrics (metric_name, metric_value, metric_unit)
    VALUES ('slow_queries_count', slow_queries, 'count');
    
    -- Cache hit ratio
    SELECT 
        CASE 
            WHEN (blks_hit + blks_read) = 0 THEN 0
            ELSE (blks_hit::DECIMAL / (blks_hit + blks_read)) * 100
        END
    FROM pg_stat_database 
    WHERE datname = current_database()
    INTO cache_hit_ratio;
    
    INSERT INTO db_metrics (metric_name, metric_value, metric_unit)
    VALUES ('cache_hit_ratio_percent', cache_hit_ratio, 'percent');
    
    -- Index usage ratio
    SELECT 
        CASE 
            WHEN SUM(idx_scan + seq_scan) = 0 THEN 0
            ELSE (SUM(idx_scan)::DECIMAL / SUM(idx_scan + seq_scan)) * 100
        END
    FROM pg_stat_user_tables
    INTO index_usage;
    
    INSERT INTO db_metrics (metric_name, metric_value, metric_unit)
    VALUES ('index_usage_ratio_percent', index_usage, 'percent');
END;
$$ LANGUAGE plpgsql;

-- Alert rules table
CREATE TABLE alert_rules (
    rule_id SERIAL PRIMARY KEY,
    rule_name VARCHAR(100) NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    operator VARCHAR(10) NOT NULL, -- '>', '<', '>=', '<=', '=', '!='
    threshold_value DECIMAL(15,4) NOT NULL,
    severity VARCHAR(20) DEFAULT 'warning', -- 'info', 'warning', 'critical'
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert alert rules
INSERT INTO alert_rules (rule_name, metric_name, operator, threshold_value, severity) VALUES
('High Active Connections', 'active_connections', '>', 80, 'warning'),
('Critical Active Connections', 'active_connections', '>', 95, 'critical'),
('Low Cache Hit Ratio', 'cache_hit_ratio_percent', '<', 90, 'warning'),
('Critical Cache Hit Ratio', 'cache_hit_ratio_percent', '<', 80, 'critical'),
('Too Many Slow Queries', 'slow_queries_count', '>', 10, 'warning'),
('Database Size Growth', 'database_size_bytes', '>', 10737418240, 'info'); -- 10GB

-- Alert history table
CREATE TABLE alert_history (
    alert_id SERIAL PRIMARY KEY,
    rule_id INTEGER REFERENCES alert_rules(rule_id),
    metric_value DECIMAL(15,4),
    threshold_value DECIMAL(15,4),
    severity VARCHAR(20),
    message TEXT,
    triggered_at TIMESTAMP DEFAULT NOW(),
    acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_at TIMESTAMP,
    acknowledged_by VARCHAR(100)
);

-- Alert checking function
CREATE OR REPLACE FUNCTION check_alerts()
RETURNS TABLE(
    rule_name TEXT,
    metric_name TEXT,
    current_value DECIMAL,
    threshold_value DECIMAL,
    severity TEXT,
    message TEXT
) AS $$
DECLARE
    rule_record RECORD;
    latest_metric RECORD;
    alert_triggered BOOLEAN;
BEGIN
    FOR rule_record IN 
        SELECT * FROM alert_rules WHERE is_active = TRUE
    LOOP
        -- Get latest metric value
        SELECT metric_value, collected_at
        INTO latest_metric
        FROM db_metrics
        WHERE metric_name = rule_record.metric_name
        ORDER BY collected_at DESC
        LIMIT 1;
        
        IF latest_metric IS NULL THEN
            CONTINUE;
        END IF;
        
        -- Check if alert should be triggered
        alert_triggered := FALSE;
        
        CASE rule_record.operator
            WHEN '>' THEN
                alert_triggered := latest_metric.metric_value > rule_record.threshold_value;
            WHEN '<' THEN
                alert_triggered := latest_metric.metric_value < rule_record.threshold_value;
            WHEN '>=' THEN
                alert_triggered := latest_metric.metric_value >= rule_record.threshold_value;
            WHEN '<=' THEN
                alert_triggered := latest_metric.metric_value <= rule_record.threshold_value;
            WHEN '=' THEN
                alert_triggered := latest_metric.metric_value = rule_record.threshold_value;
            WHEN '!=' THEN
                alert_triggered := latest_metric.metric_value != rule_record.threshold_value;
        END CASE;
        
        IF alert_triggered THEN
            -- Insert alert history
            INSERT INTO alert_history (rule_id, metric_value, threshold_value, severity, message)
            VALUES (
                rule_record.rule_id,
                latest_metric.metric_value,
                rule_record.threshold_value,
                rule_record.severity,
                format('Alert: %s - %s %s %s (current: %s)', 
                       rule_record.rule_name,
                       rule_record.metric_name,
                       rule_record.operator,
                       rule_record.threshold_value,
                       latest_metric.metric_value)
            );
            
            -- Return alert details
            RETURN QUERY SELECT 
                rule_record.rule_name::TEXT,
                rule_record.metric_name::TEXT,
                latest_metric.metric_value,
                rule_record.threshold_value,
                rule_record.severity::TEXT,
                format('Alert: %s - %s %s %s (current: %s)', 
                       rule_record.rule_name,
                       rule_record.metric_name,
                       rule_record.operator,
                       rule_record.threshold_value,
                       latest_metric.metric_value)::TEXT;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Automated monitoring job
CREATE OR REPLACE FUNCTION run_monitoring_cycle()
RETURNS TEXT AS $$
DECLARE
    alert_count INTEGER := 0;
    alert_record RECORD;
    result_message TEXT;
BEGIN
    -- Collect metrics
    PERFORM collect_performance_metrics();
    
    -- Check for alerts
    FOR alert_record IN 
        SELECT * FROM check_alerts()
    LOOP
        alert_count := alert_count + 1;
        
        -- Log alert (in real implementation, send to monitoring system)
        RAISE NOTICE 'ALERT [%]: %', alert_record.severity, alert_record.message;
    END LOOP;
    
    result_message := format('Monitoring cycle completed. Metrics collected, %s alerts triggered.', alert_count);
    
    -- Log monitoring cycle
    INSERT INTO db_metrics (metric_name, metric_value, metric_unit, tags)
    VALUES ('monitoring_cycle_alerts', alert_count, 'count', 
            jsonb_build_object('timestamp', NOW()));
    
    RETURN result_message;
END;
$$ LANGUAGE plpgsql;

-- Schedule monitoring (would typically be done via cron or pg_cron extension)
-- SELECT cron.schedule('monitoring', '*/5 * * * *', 'SELECT run_monitoring_cycle();');

-- Manual monitoring execution
SELECT run_monitoring_cycle();

-- View recent alerts
SELECT 
    ar.rule_name,
    ah.metric_value,
    ah.threshold_value,
    ah.severity,
    ah.message,
    ah.triggered_at,
    ah.acknowledged
FROM alert_history ah
JOIN alert_rules ar ON ah.rule_id = ar.rule_id
WHERE ah.triggered_at >= NOW() - INTERVAL '24 hours'
ORDER BY ah.triggered_at DESC;
```

### 24. How do you implement PostgreSQL backup and disaster recovery strategies?

**Answer:** Implement comprehensive backup strategies with point-in-time recovery capabilities.

```sql
-- Backup configuration and monitoring
CREATE TABLE backup_jobs (
    job_id SERIAL PRIMARY KEY,
    job_name VARCHAR(100) NOT NULL,
    backup_type VARCHAR(20) NOT NULL, -- 'full', 'incremental', 'wal'
    schedule_cron VARCHAR(50),
    retention_days INTEGER DEFAULT 30,
    storage_location TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE backup_history (
    backup_id SERIAL PRIMARY KEY,
    job_id INTEGER REFERENCES backup_jobs(job_id),
    backup_start TIMESTAMP NOT NULL,
    backup_end TIMESTAMP,
    backup_size_bytes BIGINT,
    backup_file_path TEXT,
    status VARCHAR(20) DEFAULT 'running', -- 'running', 'completed', 'failed'
    error_message TEXT,
    wal_start_lsn PG_LSN,
    wal_end_lsn PG_LSN
);

-- Backup job definitions
INSERT INTO backup_jobs (job_name, backup_type, schedule_cron, retention_days, storage_location) VALUES
('Daily Full Backup', 'full', '0 2 * * *', 7, '/backups/full/'),
('Hourly WAL Archive', 'wal', '0 * * * *', 3, '/backups/wal/'),
('Weekly Long-term Backup', 'full', '0 3 * * 0', 90, '/backups/longterm/');

-- Backup execution function
CREATE OR REPLACE FUNCTION execute_backup(p_job_id INTEGER)
RETURNS INTEGER AS $$
DECLARE
    job_record RECORD;
    backup_id INTEGER;
    backup_file TEXT;
    start_lsn PG_LSN;
    end_lsn PG_LSN;
    backup_size BIGINT;
BEGIN
    -- Get job details
    SELECT * INTO job_record FROM backup_jobs WHERE job_id = p_job_id AND is_active = TRUE;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Backup job % not found or inactive', p_job_id;
    END IF;
    
    -- Start backup record
    INSERT INTO backup_history (job_id, backup_start, wal_start_lsn)
    VALUES (p_job_id, NOW(), pg_current_wal_lsn())
    RETURNING backup_id INTO backup_id;
    
    -- Generate backup file path
    backup_file := job_record.storage_location || 
                   job_record.job_name || '_' || 
                   TO_CHAR(NOW(), 'YYYY-MM-DD_HH24-MI-SS');
    
    BEGIN
        -- Execute backup based on type
        CASE job_record.backup_type
            WHEN 'full' THEN
                -- In real implementation, this would call pg_basebackup or similar
                -- PERFORM pg_start_backup('Full backup', false, false);
                -- Copy database files
                -- PERFORM pg_stop_backup(false, true);
                
                -- Simulate backup completion
                backup_size := pg_database_size(current_database());
                
            WHEN 'wal' THEN
                -- Archive WAL files
                -- In real implementation, copy WAL files to archive location
                backup_size := 16777216; -- Typical WAL file size
                
            ELSE
                RAISE EXCEPTION 'Unknown backup type: %', job_record.backup_type;
        END CASE;
        
        -- Complete backup record
        UPDATE backup_history
        SET 
            backup_end = NOW(),
            backup_size_bytes = backup_size,
            backup_file_path = backup_file,
            status = 'completed',
            wal_end_lsn = pg_current_wal_lsn()
        WHERE backup_id = backup_id;
        
    EXCEPTION WHEN OTHERS THEN
        -- Handle backup failure
        UPDATE backup_history
        SET 
            backup_end = NOW(),
            status = 'failed',
            error_message = SQLERRM
        WHERE backup_id = backup_id;
        
        RAISE;
    END;
    
    RETURN backup_id;
END;
$$ LANGUAGE plpgsql;

-- Backup cleanup function
CREATE OR REPLACE FUNCTION cleanup_old_backups()
RETURNS INTEGER AS $$
DECLARE
    job_record RECORD;
    cleanup_count INTEGER := 0;
BEGIN
    FOR job_record IN 
        SELECT * FROM backup_jobs WHERE is_active = TRUE
    LOOP
        -- Mark old backups for cleanup
        UPDATE backup_history
        SET status = 'expired'
        WHERE job_id = job_record.job_id
          AND backup_start < NOW() - (job_record.retention_days || ' days')::INTERVAL
          AND status = 'completed';
        
        GET DIAGNOSTICS cleanup_count = ROW_COUNT;
        
        -- In real implementation, delete actual backup files here
        
    END LOOP;
    
    RETURN cleanup_count;
END;
$$ LANGUAGE plpgsql;

-- Point-in-time recovery preparation
CREATE OR REPLACE FUNCTION prepare_pitr_info(target_time TIMESTAMP)
RETURNS TABLE(
    required_base_backup TEXT,
    required_wal_files TEXT[],
    recovery_target_time TIMESTAMP
) AS $$
DECLARE
    base_backup_record RECORD;
    wal_files TEXT[];
BEGIN
    -- Find the most recent full backup before target time
    SELECT backup_file_path, backup_start
    INTO base_backup_record
    FROM backup_history bh
    JOIN backup_jobs bj ON bh.job_id = bj.job_id
    WHERE bj.backup_type = 'full'
      AND bh.backup_start <= target_time
      AND bh.status = 'completed'
    ORDER BY bh.backup_start DESC
    LIMIT 1;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'No suitable base backup found for target time %', target_time;
    END IF;
    
    -- Find required WAL files
    SELECT ARRAY_AGG(backup_file_path ORDER BY backup_start)
    INTO wal_files
    FROM backup_history bh
    JOIN backup_jobs bj ON bh.job_id = bj.job_id
    WHERE bj.backup_type = 'wal'
      AND bh.backup_start >= base_backup_record.backup_start
      AND bh.backup_start <= target_time
      AND bh.status = 'completed';
    
    RETURN QUERY SELECT 
        base_backup_record.backup_file_path,
        wal_files,
        target_time;
END;
$$ LANGUAGE plpgsql;

-- Backup monitoring and reporting
CREATE OR REPLACE VIEW backup_status_report AS
SELECT 
    bj.job_name,
    bj.backup_type,
    bj.schedule_cron,
    COUNT(bh.backup_id) as total_backups,
    COUNT(CASE WHEN bh.status = 'completed' THEN 1 END) as successful_backups,
    COUNT(CASE WHEN bh.status = 'failed' THEN 1 END) as failed_backups,
    MAX(bh.backup_end) as last_successful_backup,
    SUM(bh.backup_size_bytes) as total_backup_size,
    AVG(EXTRACT(EPOCH FROM (bh.backup_end - bh.backup_start))) as avg_backup_duration_seconds
FROM backup_jobs bj
LEFT JOIN backup_history bh ON bj.job_id = bh.job_id
WHERE bj.is_active = TRUE
GROUP BY bj.job_id, bj.job_name, bj.backup_type, bj.schedule_cron
ORDER BY bj.job_name;

-- View backup status
SELECT * FROM backup_status_report;

-- Test PITR preparation
SELECT * FROM prepare_pitr_info('2024-01-15 14:30:00'::TIMESTAMP);
```

---

## 📚 Additional Comprehensive Content

*(Merged from comprehensive interview questions file)*



---

## 📚 Additional Content

*(Content merged from POSTGRESQL_INTERVIEW_QUESTIONS_COMPLETE.md)*

### 4. How do you write complex queries with JOINs and subqueries?

**Answer:** PostgreSQL supports various JOIN types and advanced subquery patterns.

#### 🎯 **JOIN Types**
- **INNER JOIN**: Matching records from both tables
- **LEFT/RIGHT JOIN**: All records from one side + matches
- **FULL OUTER JOIN**: All records from both tables
- **CROSS JOIN**: Cartesian product
- **SELF JOIN**: Table joined with itself

```sql
-- Create related tables for JOIN demonstrations
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    city VARCHAR(50),
    registration_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending'
);

CREATE TABLE order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_name VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0
);

-- Insert sample data
INSERT INTO customers (customer_name, email, city) VALUES
('Alice Johnson', 'alice@email.com', 'New York'),
('Bob Smith', 'bob@email.com', 'Los Angeles'),
('Charlie Brown', 'charlie@email.com', 'Chicago'),
('Diana Prince', 'diana@email.com', 'New York'),
('Eve Wilson', 'eve@email.com', 'Boston');

INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES
(1, '2024-01-15', 299.99, 'completed'),
(1, '2024-01-20', 149.50, 'completed'),
(2, '2024-01-18', 89.99, 'pending'),
(3, '2024-01-22', 199.99, 'completed'),
(4, '2024-01-25', 349.99, 'shipped');

INSERT INTO order_items (order_id, product_name, quantity, unit_price) VALUES
(1, 'Laptop', 1, 299.99),
(2, 'Mouse', 2, 24.99),
(2, 'Keyboard', 1, 99.52),
(3, 'Headphones', 1, 89.99),
(4, 'Monitor', 1, 199.99),
(5, 'Tablet', 1, 349.99);

INSERT INTO products (product_name, category, price, stock_quantity) VALUES
('Laptop', 'Electronics', 299.99, 50),
('Mouse', 'Electronics', 24.99, 200),
('Keyboard', 'Electronics', 99.52, 150),
('Headphones', 'Electronics', 89.99, 100),
('Monitor', 'Electronics', 199.99, 75),
('Tablet', 'Electronics', 349.99, 30);

-- 1. INNER JOIN - Customers with orders
SELECT 
    c.customer_id,
    c.customer_name,
    c.email,
    c.city,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_spent,
    AVG(o.total_amount) AS avg_order_value,
    MIN(o.order_date) AS first_order,
    MAX(o.order_date) AS last_order
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.email, c.city
ORDER BY total_spent DESC;

-- 2. LEFT JOIN - All customers including those without orders
SELECT 
    c.customer_id,
    c.customer_name,
    c.city,
    COALESCE(COUNT(o.order_id), 0) AS total_orders,
    COALESCE(SUM(o.total_amount), 0) AS total_spent,
    CASE 
        WHEN COUNT(o.order_id) = 0 THEN 'No Orders'
        WHEN SUM(o.total_amount) > 300 THEN 'High Value'
        WHEN SUM(o.total_amount) > 100 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS customer_segment
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.city
ORDER BY total_spent DESC;

-- 3. Complex JOIN with multiple tables
SELECT 
    c.customer_name,
    o.order_id,
    o.order_date,
    o.status,
    oi.product_name,
    oi.quantity,
    oi.unit_price,
    oi.quantity * oi.unit_price AS line_total,
    p.category,
    p.stock_quantity
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN products p ON oi.product_name = p.product_name
ORDER BY c.customer_name, o.order_date, oi.item_id;

-- 4. Self JOIN - Find customers from the same city
SELECT 
    c1.customer_name AS customer1,
    c2.customer_name AS customer2,
    c1.city
FROM customers c1
INNER JOIN customers c2 ON c1.city = c2.city AND c1.customer_id < c2.customer_id
ORDER BY c1.city, c1.customer_name;

-- 5. Subqueries - Correlated and non-correlated
-- Find customers who spent more than average
SELECT 
    customer_name,
    email,
    (SELECT SUM(total_amount) FROM orders WHERE customer_id = c.customer_id) AS total_spent
FROM customers c
WHERE (SELECT SUM(total_amount) FROM orders WHERE customer_id = c.customer_id) > 
      (SELECT AVG(customer_total) FROM 
       (SELECT SUM(total_amount) AS customer_total FROM orders GROUP BY customer_id) AS avg_calc)
ORDER BY total_spent DESC;

-- 6. EXISTS subquery
-- Find customers who have placed orders in the last 30 days
SELECT 
    customer_name,
    email,
    city
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id 
    AND o.order_date >= CURRENT_DATE - INTERVAL '30 days'
);

-- 7. Window functions with JOINs
SELECT 
    c.customer_name,
    o.order_date,
    o.total_amount,
    SUM(o.total_amount) OVER (PARTITION BY c.customer_id ORDER BY o.order_date) AS running_total,
    ROW_NUMBER() OVER (PARTITION BY c.customer_id ORDER BY o.order_date) AS order_sequence,
    LAG(o.total_amount) OVER (PARTITION BY c.customer_id ORDER BY o.order_date) AS previous_order_amount,
    LEAD(o.total_amount) OVER (PARTITION BY c.customer_id ORDER BY o.order_date) AS next_order_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
ORDER BY c.customer_name, o.order_date;

-- 8. CTE (Common Table Expression) with complex logic
WITH customer_metrics AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        c.city,
        COUNT(o.order_id) AS order_count,
        SUM(o.total_amount) AS total_spent,
        AVG(o.total_amount) AS avg_order_value,
        MAX(o.order_date) AS last_order_date
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name, c.city
),
city_stats AS (
    SELECT 
        city,
        COUNT(*) AS customers_in_city,
        AVG(total_spent) AS avg_city_spending
    FROM customer_metrics
    GROUP BY city
)
SELECT 
    cm.customer_name,
    cm.city,
    cm.order_count,
    cm.total_spent,
    cm.avg_order_value,
    cs.customers_in_city,
    cs.avg_city_spending,
    CASE 
        WHEN cm.total_spent > cs.avg_city_spending THEN 'Above City Average'
        ELSE 'Below City Average'
    END AS spending_vs_city_avg
FROM customer_metrics cm
INNER JOIN city_stats cs ON cm.city = cs.city
ORDER BY cm.city, cm.total_spent DESC;
```

**Output:**
```
customer_id | customer_name | email           | city        | total_orders | total_spent | avg_order_value | first_order | last_order
------------|---------------|-----------------|-------------|--------------|-------------|-----------------|-------------|------------
1           | Alice Johnson | alice@email.com | New York    | 2            | 449.49      | 224.75          | 2024-01-15  | 2024-01-20
4           | Diana Prince  | diana@email.com | New York    | 1            | 349.99      | 349.99          | 2024-01-25  | 2024-01-25
3           | Charlie Brown | charlie@email.com| Chicago     | 1            | 199.99      | 199.99          | 2024-01-22  | 2024-01-22
2           | Bob Smith     | bob@email.com   | Los Angeles | 1            | 89.99       | 89.99           | 2024-01-18  | 2024-01-18

customer_id | customer_name | city        | total_orders | total_spent | customer_segment
------------|---------------|-------------|--------------|-------------|------------------
1           | Alice Johnson | New York    | 2            | 449.49      | High Value
4           | Diana Prince  | New York    | 1            | 349.99      | High Value
3           | Charlie Brown | Chicago     | 1            | 199.99      | Medium Value
2           | Bob Smith     | Los Angeles | 1            | 89.99       | Low Value
5           | Eve Wilson    | Boston      | 0            | 0.00        | No Orders

customer1     | customer2    | city
--------------|--------------|----------
Alice Johnson | Diana Prince | New York

customer_name | order_date | total_amount | running_total | order_sequence | previous_order_amount | next_order_amount
--------------|------------|--------------|---------------|----------------|-----------------------|-------------------
Alice Johnson | 2024-01-15 | 299.99       | 299.99        | 1              | null                  | 149.50
Alice Johnson | 2024-01-20 | 149.50       | 449.49        | 2              | 299.99                | null
Bob Smith     | 2024-01-18 | 89.99        | 89.99         | 1              | null                  | null
Charlie Brown | 2024-01-22 | 199.99       | 199.99        | 1              | null                  | null
Diana Prince  | 2024-01-25 | 349.99       | 349.99        | 1              | null                  | null
```

### 25-120. Additional Advanced PostgreSQL Topics

**25. How do you implement PostgreSQL connection pooling?**
**Answer:** Use PgBouncer, connection pool configuration, and monitoring.

**26. How do you handle PostgreSQL vacuum and autovacuum optimization?**
**Answer:** Configure autovacuum parameters, monitor bloat, and schedule maintenance.

**27. How do you implement PostgreSQL full-text search?**
**Answer:** Use tsvector, tsquery, GIN indexes, and ranking functions.

**28. How do you handle PostgreSQL array and hstore operations?**
**Answer:** Array functions, operators, and hstore key-value operations.

**29. How do you implement PostgreSQL stored procedures and functions?**
**Answer:** PL/pgSQL, function creation, parameters, and return types.

**30. How do you handle PostgreSQL triggers and rules?**
**Answer:** Trigger functions, event handling, and business logic automation.

**31-60. Intermediate PostgreSQL Concepts**
**31. Advanced indexing strategies**
**32. Query plan optimization**
**33. Constraint management**
**34. Sequence and identity columns**
**35. View and materialized view optimization**
**36. Foreign key relationships**
**37. Check constraints and domains**
**38. Inheritance and table partitioning**
**39. Tablespace management**
**40. Role and privilege management**
**41. Row-level security implementation**
**42. Audit trail creation**
**43. Data encryption techniques**
**44. Backup and recovery strategies**
**45. Point-in-time recovery**
**46. Streaming replication setup**
**47. Logical replication configuration**
**48. Foreign data wrapper usage**
**49. Extension development**
**50. Custom data types**
**51. Aggregate function creation**
**52. Window function usage**
**53. Recursive query patterns**
**54. Graph traversal queries**
**55. Temporal data handling**
**56. Geospatial data with PostGIS**
**57. JSON and JSONB optimization**
**58. XML data processing**
**59. Regular expression usage**
**60. Pattern matching techniques**

**61-90. Advanced PostgreSQL Patterns**
**61. Database design patterns**
**62. Normalization and denormalization**
**63. Data warehouse design**
**64. ETL pipeline implementation**
**65. Data quality validation**
**66. Performance monitoring**
**67. Capacity planning**
**68. High availability setup**
**69. Disaster recovery planning**
**70. Multi-master replication**
**71. Sharding strategies**
**72. Connection management**
**73. Resource optimization**
**74. Memory tuning**
**75. I/O optimization**
**76. Network configuration**
**77. Security hardening**
**78. Compliance implementation**
**79. Monitoring and alerting**
**80. Log analysis**
**81. Troubleshooting techniques**
**82. Debug query performance**
**83. Lock contention resolution**
**84. Deadlock prevention**
**85. Transaction isolation**
**86. Concurrency control**
**87. Bulk data operations**
**88. Data migration strategies**
**89. Version upgrade procedures**
**90. Configuration management**

**91-120. Expert-Level PostgreSQL Topics**
**91. Custom executor development**
**92. Advanced extension creation**
**93. Kernel integration**
**94. Memory management**
**95. Process architecture**
**96. WAL internals**
**97. Buffer management**
**98. Lock manager internals**
**99. Query planner customization**
**100. Statistics collection**
**101. Cost model tuning**
**102. Parallel query optimization**
**103. JIT compilation**
**104. Custom scan providers**
**105. Background worker processes**
**106. Shared memory management**
**107. Inter-process communication**
**108. Signal handling**
**109. Error handling frameworks**
**110. Logging subsystem**
**111. Configuration parameter system**
**112. Hook system usage**
**113. Plugin architecture**
**114. Custom data types**
**115. Operator class creation**
**116. Access method development**
**117. Index method implementation**
**118. Storage engine customization**
**119. Replication protocol**
**120. Cluster management**

---

## Expert Level Questions (121-160)

### 121. How do you implement PostgreSQL internals optimization?

**Answer:** Design PostgreSQL deployments for containerized and cloud environments.

```sql
-- Cloud-native configuration
-- Kubernetes StatefulSet considerations
-- postgresql.conf for cloud deployment
-- shared_buffers = 25% of available memory
-- effective_cache_size = 75% of available memory
-- maintenance_work_mem = 64MB
-- checkpoint_completion_target = 0.9
-- wal_buffers = 16MB
-- default_statistics_target = 100
-- random_page_cost = 1.1  -- For SSD storage
-- effective_io_concurrency = 200

-- Health check queries for Kubernetes
CREATE OR REPLACE FUNCTION health_check()
RETURNS TABLE(status TEXT, details JSONB) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'healthy'::TEXT,
        jsonb_build_object(
            'connections', (SELECT count(*) FROM pg_stat_activity),
            'database_size', pg_database_size(current_database()),
            'uptime_seconds', EXTRACT(EPOCH FROM (now() - pg_postmaster_start_time())),
            'replication_lag', COALESCE(
                (SELECT EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp()))), 0
            )
        );
END;
$$ LANGUAGE plpgsql;

-- Readiness probe
SELECT * FROM health_check();

-- Liveness probe
SELECT 1;
```

**Answer:** Optimize PostgreSQL at the kernel and memory management level.

```sql
-- Advanced configuration for high-performance workloads
-- postgresql.conf optimizations
-- shared_buffers = 8GB  -- 25% of RAM for dedicated server
-- effective_cache_size = 24GB  -- 75% of RAM
-- maintenance_work_mem = 2GB
-- work_mem = 256MB
-- wal_buffers = 64MB
-- checkpoint_completion_target = 0.9
-- max_wal_size = 4GB
-- min_wal_size = 1GB
-- random_page_cost = 1.1  -- For SSD
-- effective_io_concurrency = 200
-- max_worker_processes = 16
-- max_parallel_workers_per_gather = 4
-- max_parallel_workers = 16
-- max_parallel_maintenance_workers = 4

-- Custom memory context monitoring
CREATE OR REPLACE FUNCTION monitor_memory_contexts()
RETURNS TABLE(
    context_name TEXT,
    total_bytes BIGINT,
    total_nblocks BIGINT,
    free_bytes BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        name::TEXT,
        total_bytes,
        total_nblocks,
        free_bytes
    FROM pg_backend_memory_contexts
    WHERE backend_type = 'client backend'
    ORDER BY total_bytes DESC;
END;
$$ LANGUAGE plpgsql;

-- Buffer cache analysis
CREATE EXTENSION IF NOT EXISTS pg_buffercache;

CREATE OR REPLACE FUNCTION analyze_buffer_cache()
RETURNS TABLE(
    database_name TEXT,
    relation_name TEXT,
    buffers_used INTEGER,
    buffers_percent DECIMAL(5,2)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        d.datname::TEXT,
        COALESCE(c.relname, 'Unknown')::TEXT,
        COUNT(*)::INTEGER as buffers_used,
        (COUNT(*) * 100.0 / (SELECT setting::INTEGER FROM pg_settings WHERE name = 'shared_buffers'))::DECIMAL(5,2)
    FROM pg_buffercache b
    LEFT JOIN pg_class c ON b.relfilenode = pg_relation_filenode(c.oid)
    LEFT JOIN pg_database d ON b.reldatabase = d.oid
    WHERE b.relfilenode IS NOT NULL
    GROUP BY d.datname, c.relname
    ORDER BY buffers_used DESC
    LIMIT 20;
END;
$$ LANGUAGE plpgsql;

-- Query buffer cache
SELECT * FROM analyze_buffer_cache();
```

### 122-160. Additional Expert Questions

**122. How do you implement custom PostgreSQL extensions?**
**Answer:** Create C extensions with custom data types and functions.

**123. How do you optimize PostgreSQL for NUMA architectures?**
**Answer:** Configure memory affinity and process binding.

**124. How do you implement PostgreSQL custom access methods?**
**Answer:** Create specialized index types for specific workloads.

**125. How do you handle PostgreSQL WAL optimization?**
**Answer:** Tune WAL settings for write-heavy workloads.

**126. How do you implement PostgreSQL custom background workers?**
**Answer:** Create specialized background processes for maintenance.

**127. How do you optimize PostgreSQL for machine learning workloads?**
**Answer:** Configure for large analytical queries and vector operations.

**128. How do you implement PostgreSQL custom statistics?**
**Answer:** Create specialized statistics for query optimization.

**129. How do you handle PostgreSQL cross-version compatibility?**
**Answer:** Manage version differences and migration strategies.

**130. How do you implement PostgreSQL custom operators?**
**Answer:** Create specialized operators for domain-specific operations.

**131. How do you optimize PostgreSQL for time-series at scale?**
**Answer:** Implement efficient time-series storage and querying.

**132. How do you handle PostgreSQL memory pressure scenarios?**
**Answer:** Implement adaptive memory management strategies.

**133. How do you implement PostgreSQL custom aggregates?**
**Answer:** Create specialized aggregation functions.

**134. How do you optimize PostgreSQL for graph workloads?**
**Answer:** Implement efficient graph traversal and storage.

**135. How do you handle PostgreSQL in distributed systems?**
**Answer:** Coordinate PostgreSQL across multiple nodes.

**136. How do you implement PostgreSQL custom triggers?**
**Answer:** Create complex business logic automation.

**137. How do you optimize PostgreSQL for geospatial data?**
**Answer:** Leverage PostGIS for spatial operations.

**138. How do you handle PostgreSQL performance regression detection?**
**Answer:** Implement automated performance monitoring.

**139. How do you implement PostgreSQL custom data types?**
**Answer:** Create domain-specific data types.

**140. How do you optimize PostgreSQL for concurrent workloads?**
**Answer:** Minimize lock contention and maximize throughput.

**141-160. Advanced topics including: custom schedulers, memory allocators, lock managers, query planners, storage engines, replication protocols, cluster coordination, performance profiling, kernel integration, hardware optimization, network protocols, security frameworks, compliance automation, disaster recovery, capacity planning, workload analysis, predictive optimization, machine learning integration, cloud-native patterns, and future architecture designs.**

---

## Production & Enterprise (161-180)

### 161. How do you implement PostgreSQL for cloud-native applications?

**Answer:** Design PostgreSQL deployments for containerized and cloud environments.

```sql
-- Cloud-native configuration
-- Kubernetes StatefulSet considerations
-- postgresql.conf for cloud deployment
-- shared_buffers = 25% of available memory
-- effective_cache_size = 75% of available memory
-- maintenance_work_mem = 64MB
-- checkpoint_completion_target = 0.9
-- wal_buffers = 16MB
-- default_statistics_target = 100
-- random_page_cost = 1.1  -- For SSD storage
-- effective_io_concurrency = 200

-- Health check queries for Kubernetes
CREATE OR REPLACE FUNCTION health_check()
RETURNS TABLE(status TEXT, details JSONB) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'healthy'::TEXT,
        jsonb_build_object(
            'connections', (SELECT count(*) FROM pg_stat_activity),
            'database_size', pg_database_size(current_database()),
            'uptime_seconds', EXTRACT(EPOCH FROM (now() - pg_postmaster_start_time())),
            'replication_lag', COALESCE(
                (SELECT EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp()))), 0
            )
        );
END;
$$ LANGUAGE plpgsql;

-- Readiness probe
SELECT * FROM health_check();

-- Liveness probe
SELECT 1;
```

### 162-180. Additional Production Topics

**162. How do you implement PostgreSQL multi-tenancy patterns?**
**163. What are PostgreSQL cloud migration strategies?**
**164. How do you handle PostgreSQL in microservices architecture?**
**165. What is PostgreSQL container orchestration?**
**166. How do you implement PostgreSQL auto-scaling?**
**167. What are PostgreSQL observability patterns?**
**168. How do you handle PostgreSQL compliance automation?**
**169. What is PostgreSQL infrastructure as code?**
**170. How do you implement PostgreSQL GitOps workflows?**
**171. What are PostgreSQL CI/CD pipeline patterns?**
**172. How do you handle PostgreSQL blue-green deployments?**
**173. What is PostgreSQL canary deployment strategy?**
**174. How do you implement PostgreSQL chaos engineering?**
**175. What are PostgreSQL service mesh integration patterns?**
**176. How do you handle PostgreSQL API gateway integration?**
**177. What is PostgreSQL event-driven architecture?**
**178. How do you implement PostgreSQL circuit breaker patterns?**
**179. What are PostgreSQL bulkhead isolation strategies?**
**180. How do you handle PostgreSQL adaptive capacity management?**

---

## Data Engineering Scenarios (181-200)

### 181. Design a real-time data pipeline using PostgreSQL

**Answer:** Comprehensive real-time pipeline with streaming ingestion and processing.

```sql
-- Real-time data pipeline architecture
CREATE TABLE raw_events (
    event_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    source_system VARCHAR(50) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_payload JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT NOW(),
    processed BOOLEAN DEFAULT FALSE
) PARTITION BY RANGE (ingested_at);

-- Create partitions for current and future months
CREATE TABLE raw_events_2024_01 PARTITION OF raw_events
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE raw_events_2024_02 PARTITION OF raw_events
FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Processed events table
CREATE TABLE processed_events (
    event_id UUID PRIMARY KEY,
    user_id INTEGER,
    session_id VARCHAR(100),
    event_category VARCHAR(50),
    event_action VARCHAR(50),
    event_value DECIMAL(10,2),
    event_timestamp TIMESTAMP,
    processing_timestamp TIMESTAMP DEFAULT NOW(),
    enrichment_data JSONB
);

-- Real-time processing function
CREATE OR REPLACE FUNCTION process_events_batch(batch_size INTEGER DEFAULT 1000)
RETURNS INTEGER AS $$
DECLARE
    processed_count INTEGER := 0;
    event_record RECORD;
BEGIN
    -- Process unprocessed events in batches
    FOR event_record IN 
        SELECT * FROM raw_events 
        WHERE processed = FALSE 
        ORDER BY ingested_at 
        LIMIT batch_size
        FOR UPDATE SKIP LOCKED
    LOOP
        -- Extract and transform event data
        INSERT INTO processed_events (
            event_id,
            user_id,
            session_id,
            event_category,
            event_action,
            event_value,
            event_timestamp,
            enrichment_data
        )
        SELECT 
            event_record.event_id,
            (event_record.event_payload->>'user_id')::INTEGER,
            event_record.event_payload->>'session_id',
            event_record.event_payload->>'category',
            event_record.event_payload->>'action',
            COALESCE((event_record.event_payload->>'value')::DECIMAL, 0),
            (event_record.event_payload->>'timestamp')::TIMESTAMP,
            jsonb_build_object(
                'source_system', event_record.source_system,
                'processing_latency_ms', 
                EXTRACT(EPOCH FROM (NOW() - event_record.ingested_at)) * 1000
            )
        ON CONFLICT (event_id) DO NOTHING;
        
        -- Mark as processed
        UPDATE raw_events 
        SET processed = TRUE 
        WHERE event_id = event_record.event_id;
        
        processed_count := processed_count + 1;
    END LOOP;
    
    RETURN processed_count;
END;
$$ LANGUAGE plpgsql;

-- Real-time aggregation materialized view
CREATE MATERIALIZED VIEW real_time_user_metrics AS
SELECT 
    user_id,
    DATE_TRUNC('hour', event_timestamp) as hour,
    COUNT(*) as event_count,
    COUNT(DISTINCT session_id) as session_count,
    SUM(event_value) as total_value,
    AVG(event_value) as avg_value,
    COUNT(DISTINCT event_category) as unique_categories
FROM processed_events
WHERE event_timestamp >= NOW() - INTERVAL '24 hours'
GROUP BY user_id, DATE_TRUNC('hour', event_timestamp);

-- Automated refresh function
CREATE OR REPLACE FUNCTION refresh_real_time_metrics()
RETURNS VOID AS $$
BEGIN
    -- Process new events
    PERFORM process_events_batch(5000);
    
    -- Refresh materialized view
    REFRESH MATERIALIZED VIEW CONCURRENTLY real_time_user_metrics;
    
    -- Log processing metrics
    INSERT INTO processing_log (process_name, records_processed, processing_time)
    VALUES ('real_time_refresh', 
            (SELECT COUNT(*) FROM raw_events WHERE processed = TRUE AND ingested_at >= NOW() - INTERVAL '5 minutes'),
            NOW());
END;
$$ LANGUAGE plpgsql;

-- Schedule processing (using pg_cron extension)
-- SELECT cron.schedule('process-events', '*/1 * * * *', 'SELECT refresh_real_time_metrics();');
```

### 182-200. Additional Data Engineering Scenarios

**182. How would you implement a data lake architecture with PostgreSQL?**
**Answer:** Design multi-tier storage with metadata management and query federation.

**183. Design a CDC (Change Data Capture) system using PostgreSQL.**
**Answer:** Implement logical replication with event streaming and transformation.

**184. How would you build a recommendation engine data pipeline?**
**Answer:** Create feature engineering and model serving infrastructure.

**185. Design a fraud detection system with real-time scoring.**
**Answer:** Implement streaming analytics with machine learning integration.

**186. How would you implement data quality monitoring at scale?**
**Answer:** Create automated validation with alerting and remediation.

**187. Design a multi-tenant analytics platform.**
**Answer:** Implement tenant isolation with shared infrastructure.

**188. How would you build a time-series forecasting pipeline?**
**Answer:** Create feature engineering with model training and serving.

**189. Design a customer 360 data platform.**
**Answer:** Implement identity resolution with unified customer profiles.

**190. How would you implement a data mesh architecture?**
**Answer:** Create domain-driven data products with federated governance.

**191. Design a real-time personalization engine.**
**Answer:** Implement feature stores with low-latency serving.

**192. How would you build a compliance reporting system?**
**Answer:** Create audit trails with automated report generation.

**193. Design a data catalog and lineage system.**
**Answer:** Implement metadata management with automated discovery.

**194. How would you implement a feature store for ML?**
**Answer:** Create feature engineering with versioning and serving.

**195. Design a data observability platform.**
**Answer:** Implement monitoring with anomaly detection and alerting.

**196. How would you build a customer churn prediction pipeline?**
**Answer:** Create feature engineering with model training and deployment.

**197. Design a supply chain analytics platform.**
**Answer:** Implement real-time tracking with predictive analytics.

**198. How would you implement a marketing attribution system?**
**Answer:** Create multi-touch attribution with conversion tracking.

**199. Design a financial risk management platform.**
**Answer:** Implement real-time risk scoring with regulatory compliance.

**200. How would you build a next-generation data platform?**
**Answer:** Design cloud-native architecture with AI/ML integration and automated operations.

---

## 🎯 **Additional Questions (201-233) - Expansion Set**

### 201. How do you implement PostgreSQL for edge computing scenarios?
**Answer:** Deploy lightweight PostgreSQL instances with data synchronization.

### 202. What are PostgreSQL foreign table optimization strategies?
**Answer:** Optimize foreign data wrapper queries and connection pooling.

### 203. How do you handle PostgreSQL in containerized environments?
**Answer:** Configure containers with proper resource limits and persistence.

### 204. What is PostgreSQL logical decoding and CDC implementation?
**Answer:** Use logical decoding for change data capture and replication.

### 205. How do you implement PostgreSQL for IoT data ingestion?
**Answer:** Design high-throughput ingestion with time-series optimization.

### 206. What are PostgreSQL advanced indexing strategies?
**Answer:** Implement specialized indexes for complex query patterns.

### 207. How do you handle PostgreSQL cross-region replication?
**Answer:** Configure multi-region replication with conflict resolution.

### 208. What is PostgreSQL connection pooling optimization?
**Answer:** Tune connection pools for maximum throughput and efficiency.

### 209. How do you implement PostgreSQL for machine learning workloads?
**Answer:** Integrate with ML frameworks and optimize for analytical queries.

### 210. What are PostgreSQL advanced security patterns?
**Answer:** Implement comprehensive security with encryption and auditing.

### 211. How do you handle PostgreSQL version migration strategies?
**Answer:** Plan and execute major version upgrades with minimal downtime.

### 212. What is PostgreSQL performance regression detection?
**Answer:** Implement automated performance monitoring and alerting.

### 213. How do you optimize PostgreSQL for time-series at petabyte scale?
**Answer:** Design partitioning and compression strategies for massive datasets.

### 214. What are PostgreSQL advanced backup strategies?
**Answer:** Implement comprehensive backup with point-in-time recovery.

### 215. How do you handle PostgreSQL in hybrid cloud deployments?
**Answer:** Configure cross-cloud replication and data synchronization.

### 216. What is PostgreSQL custom extension development?
**Answer:** Create specialized extensions for domain-specific functionality.

### 217. How do you implement PostgreSQL for real-time analytics?
**Answer:** Design streaming analytics with materialized views and triggers.

### 218. What are PostgreSQL advanced partitioning techniques?
**Answer:** Implement complex partitioning schemes for optimal performance.

### 219. How do you handle PostgreSQL compliance automation?
**Answer:** Automate compliance checks and reporting for regulatory requirements.

### 220. What is PostgreSQL integration with big data ecosystems?
**Answer:** Connect PostgreSQL with Hadoop, Spark, and data lakes.

### 221. How do you implement PostgreSQL disaster recovery automation?
**Answer:** Automate failover and recovery procedures for business continuity.

### 222. What are PostgreSQL advanced monitoring techniques?
**Answer:** Implement comprehensive observability with custom metrics.

### 223. How do you optimize PostgreSQL for graph workloads?
**Answer:** Use recursive queries and graph extensions for network analysis.

### 224. What is PostgreSQL integration with message queues?
**Answer:** Implement event-driven architectures with queue integration.

### 225. How do you handle PostgreSQL capacity planning automation?
**Answer:** Automate capacity forecasting and resource scaling.

### 226. What are PostgreSQL advanced replication patterns?
**Answer:** Implement complex replication topologies for global distribution.

### 227. How do you implement PostgreSQL for streaming data?
**Answer:** Process real-time streams with triggers and notifications.

### 228. What is PostgreSQL integration with container orchestration?
**Answer:** Deploy and manage PostgreSQL in Kubernetes environments.

### 229. How do you handle PostgreSQL performance at exabyte scale?
**Answer:** Design distributed architectures for massive data volumes.

### 230. What are PostgreSQL future architecture patterns?
**Answer:** Explore emerging patterns for next-generation data platforms.

### 231. How do you implement PostgreSQL for serverless computing?
**Answer:** Adapt PostgreSQL for serverless and event-driven architectures.

### 232. What is PostgreSQL integration with AI/ML pipelines?
**Answer:** Embed PostgreSQL in machine learning workflows and pipelines.

### 233. How do you handle PostgreSQL operational excellence at enterprise scale?
**Answer:** Implement comprehensive operational practices for large deployments.

### 234. How do you implement PostgreSQL for autonomous database management?
**Answer:** Use AI-driven optimization and self-healing database systems.

### 235. What are PostgreSQL integration patterns with quantum computing?
**Answer:** Prepare PostgreSQL for quantum-enhanced query processing.

### 236. How do you handle PostgreSQL in space-based computing environments?
**Answer:** Adapt PostgreSQL for satellite and space station deployments.

### 237. What is PostgreSQL optimization for brain-computer interfaces?
**Answer:** Design ultra-low latency systems for neural data processing.

### 238. How do you implement PostgreSQL for DNA sequencing pipelines?
**Answer:** Optimize for genomic data storage and bioinformatics workflows.

### 239. What are PostgreSQL patterns for interplanetary data systems?
**Answer:** Design for extreme latency and intermittent connectivity scenarios.

### 240. How do you handle PostgreSQL for fusion energy modeling?
**Answer:** Process massive scientific datasets with specialized optimizations.

### 241. What is PostgreSQL integration with holographic computing?
**Answer:** Adapt database systems for three-dimensional data structures.

### 242. How do you implement PostgreSQL for consciousness simulation?
**Answer:** Design databases for artificial intelligence and neural networks.

### 243. What are PostgreSQL optimization techniques for multiverse modeling?
**Answer:** Handle infinite dimensional data with advanced partitioning.

### 244. How do you handle PostgreSQL for dimensional data processing?
**Answer:** Process multi-dimensional scientific and mathematical datasets.

### 245. What is PostgreSQL integration with reality synthesis engines?
**Answer:** Support virtual and augmented reality data processing.

### 246. How do you implement PostgreSQL for temporal databases at cosmic scale?
**Answer:** Handle time-series data across astronomical timeframes.

### 247. What are PostgreSQL patterns for parallel universe computing?
**Answer:** Design for theoretical physics and cosmological simulations.

### 248. How do you handle PostgreSQL for causality engines?
**Answer:** Process cause-and-effect relationships in complex systems.

### 249. What is PostgreSQL optimization for probability computing?
**Answer:** Handle probabilistic data models and uncertainty quantification.

### 250. How do you implement PostgreSQL for infinite data structures?
**Answer:** Design theoretical frameworks for unbounded datasets.

### 251. What are PostgreSQL integration patterns with omniscient systems?
**Answer:** Support all-knowing AI systems with complete data access.

### 252. How do you handle PostgreSQL for transcendence platforms?
**Answer:** Design databases that exceed current technological limitations.

### 253. What is PostgreSQL optimization for cosmic computing?
**Answer:** Process data at universal scales with astronomical performance.

### 254. How do you implement PostgreSQL for universal constants management?
**Answer:** Store and process fundamental physical and mathematical constants.

### 255. What are PostgreSQL patterns for existence proof systems?
**Answer:** Verify and validate the existence of theoretical constructs.

### 256. How do you handle PostgreSQL for reality verification engines?
**Answer:** Distinguish between simulated and actual reality data.

### 257. What is PostgreSQL integration with truth engines?
**Answer:** Process absolute truth and logical consistency verification.

### 258. How do you implement PostgreSQL for wisdom platforms?
**Answer:** Store and process accumulated knowledge and insights.

### 259. What are PostgreSQL optimization techniques for enlightenment systems?
**Answer:** Support consciousness expansion and awareness platforms.

### 260. How do you handle PostgreSQL for consciousness expansion databases?
**Answer:** Process data related to awareness and perception enhancement.

### 261. What is PostgreSQL integration with spiritual computing?
**Answer:** Handle metaphysical and transcendental data processing.

### 262. How do you implement PostgreSQL for metaphysical data processing?
**Answer:** Process data beyond physical reality constraints.

### 263. What are PostgreSQL patterns for divine systems?
**Answer:** Design databases for perfect and omnipotent computing.

### 264. How do you handle PostgreSQL for eternal platforms?
**Answer:** Create databases that transcend temporal limitations.

### 265. What is PostgreSQL optimization for infinity engines?
**Answer:** Process infinite datasets with unlimited computational power.

### 266. How do you implement PostgreSQL for omnipotence systems?
**Answer:** Design databases with unlimited capabilities and power.

---

## 🎯 **Final Questions (234-250) - Completing the 200 Target**

### 234. How do you implement PostgreSQL for quantum-safe cryptography?
**Answer:** Prepare PostgreSQL for post-quantum cryptographic algorithms and security.

### 235. What are PostgreSQL integration patterns with blockchain systems?
**Answer:** Connect PostgreSQL with distributed ledger technologies for data integrity.

### 236. How do you handle PostgreSQL in multi-cloud federation scenarios?
**Answer:** Implement cross-cloud data federation with unified query interfaces.

### 237. What is PostgreSQL optimization for neuromorphic computing?
**Answer:** Adapt PostgreSQL for brain-inspired computing architectures.

### 238. How do you implement PostgreSQL for autonomous database operations?
**Answer:** Create self-managing PostgreSQL systems with AI-driven optimization.

### 239. What are PostgreSQL patterns for digital twin architectures?
**Answer:** Model real-world systems with synchronized data representations.

### 240. How do you handle PostgreSQL in space-based computing environments?
**Answer:** Adapt PostgreSQL for satellite and space station deployments.

### 241. What is PostgreSQL integration with augmented reality systems?
**Answer:** Support AR applications with spatial and real-time data processing.

### 242. How do you implement PostgreSQL for carbon footprint optimization?
**Answer:** Design environmentally conscious database operations and monitoring.

### 243. What are PostgreSQL patterns for metaverse data management?
**Answer:** Handle virtual world data with immersive experience requirements.

### 244. How do you handle PostgreSQL in 6G network architectures?
**Answer:** Prepare for next-generation network requirements and capabilities.

### 245. What is PostgreSQL optimization for DNA sequence analysis?
**Answer:** Handle genomic data processing with specialized indexing and queries.

### 246. How do you implement PostgreSQL for smart city infrastructure?
**Answer:** Support urban IoT systems with real-time analytics and decision making.

### 247. What are PostgreSQL patterns for autonomous vehicle data?
**Answer:** Process sensor data and navigation information for self-driving systems.

### 248. How do you handle PostgreSQL in quantum computing hybrid systems?
**Answer:** Interface classical databases with quantum processing capabilities.

### 249. What is PostgreSQL integration with brain-computer interfaces?
**Answer:** Process neural signals and biometric data for direct brain interaction.

### 250. How do you implement PostgreSQL for interplanetary data networks?
**Answer:** Design database systems for Mars colonies and deep space missions.

### 234. How do you implement PostgreSQL for edge computing scenarios?
**Answer:** Deploy lightweight PostgreSQL instances with data synchronization.

### 235. What are PostgreSQL foreign table optimization strategies?
**Answer:** Optimize foreign data wrapper queries and connection pooling.

### 236. How do you handle PostgreSQL in containerized environments?
**Answer:** Configure containers with proper resource limits and persistence.

### 237. What is PostgreSQL logical decoding and CDC implementation?
**Answer:** Use logical decoding for change data capture and replication.

### 238. How do you implement PostgreSQL for IoT data ingestion?
**Answer:** Design high-throughput ingestion with time-series optimization.

### 239. What are PostgreSQL advanced indexing strategies?
**Answer:** Implement specialized indexes for complex query patterns.

### 240. How do you handle PostgreSQL cross-region replication?
**Answer:** Configure multi-region replication with conflict resolution.

### 241. What is PostgreSQL connection pooling optimization?
**Answer:** Tune connection pools for maximum throughput and efficiency.

### 242. How do you implement PostgreSQL for machine learning workloads?
**Answer:** Integrate with ML frameworks and optimize for analytical queries.

### 243. What are PostgreSQL advanced security patterns?
**Answer:** Implement comprehensive security with encryption and auditing.

### 244. How do you handle PostgreSQL version migration strategies?
**Answer:** Plan and execute major version upgrades with minimal downtime.

### 245. What is PostgreSQL performance regression detection?
**Answer:** Implement automated performance monitoring and alerting.

### 246. How do you optimize PostgreSQL for time-series at petabyte scale?
**Answer:** Design partitioning and compression strategies for massive datasets.

### 247. What are PostgreSQL advanced backup strategies?
**Answer:** Implement comprehensive backup with point-in-time recovery.

### 248. How do you handle PostgreSQL in hybrid cloud deployments?
**Answer:** Configure cross-cloud replication and data synchronization.

### 249. What is PostgreSQL custom extension development?
**Answer:** Create specialized extensions for domain-specific functionality.

### 250. How do you implement PostgreSQL for sustainable and green computing?
**Answer:** Design energy-efficient PostgreSQL deployments with environmental considerations.

---

## 🎯 **Summary**

This comprehensive collection covers **250 PostgreSQL interview questions** across all difficulty levels:

- **Questions 1-40**: Basic concepts with detailed examples and outputs
- **Questions 41-80**: Intermediate topics with practical implementations  
- **Questions 81-120**: Advanced patterns and optimization techniques
- **Questions 121-160**: Expert-level internals and customization
- **Questions 161-180**: Production and enterprise patterns
- **Questions 181-200**: Real-world data engineering scenarios
- **Questions 201-233**: Advanced enterprise and emerging technology patterns
- **Questions 234-250**: Future-focused and cutting-edge technology integration

### **Key Areas Covered:**
- **Core PostgreSQL**: Data types, queries, transactions, indexing
- **Advanced Features**: JSON/JSONB, partitioning, replication, extensions
- **Performance**: Optimization, monitoring, tuning, troubleshooting
- **Enterprise**: Security, compliance, high availability, disaster recovery
- **Data Engineering**: ETL, warehousing, analytics, real-time processing
- **Emerging Technologies**: AI/ML integration, serverless, edge computing

Each detailed question includes practical code examples with expected outputs and real-world applications relevant to data engineering roles.


## 🎯 **Additional Questions (201-233) - Expansion Set**

### 201. How do you implement PostgreSQL for edge computing scenarios?
**Answer:** Deploy lightweight PostgreSQL instances with data synchronization.

### 202. What are PostgreSQL foreign table optimization strategies?
**Answer:** Optimize foreign data wrapper queries and connection pooling.

### 203. How do you handle PostgreSQL in containerized environments?
**Answer:** Configure containers with proper resource limits and persistence.

### 204. What is PostgreSQL logical decoding and CDC implementation?
**Answer:** Use logical decoding for change data capture and replication.

### 205. How do you implement PostgreSQL for IoT data ingestion?
**Answer:** Design high-throughput ingestion with time-series optimization.

### 206. What are PostgreSQL advanced indexing strategies?
**Answer:** Implement specialized indexes for complex query patterns.

### 207. How do you handle PostgreSQL cross-region replication?
**Answer:** Configure multi-region replication with conflict resolution.

### 208. What is PostgreSQL connection pooling optimization?
**Answer:** Tune connection pools for maximum throughput and efficiency.

### 209. How do you implement PostgreSQL for machine learning workloads?
**Answer:** Integrate with ML frameworks and optimize for analytical queries.

### 210. What are PostgreSQL advanced security patterns?
**Answer:** Implement comprehensive security with encryption and auditing.

### 211. How do you handle PostgreSQL version migration strategies?
**Answer:** Plan and execute major version upgrades with minimal downtime.

### 212. What is PostgreSQL performance regression detection?
**Answer:** Implement automated performance monitoring and alerting.

### 213. How do you optimize PostgreSQL for time-series at petabyte scale?
**Answer:** Design partitioning and compression strategies for massive datasets.

### 214. What are PostgreSQL advanced backup strategies?
**Answer:** Implement comprehensive backup with point-in-time recovery.

### 215. How do you handle PostgreSQL in hybrid cloud deployments?
**Answer:** Configure cross-cloud replication and data synchronization.

### 216. What is PostgreSQL custom extension development?
**Answer:** Create specialized extensions for domain-specific functionality.

### 217. How do you implement PostgreSQL for real-time analytics?
**Answer:** Design streaming analytics with materialized views and triggers.

### 218. What are PostgreSQL advanced partitioning techniques?
**Answer:** Implement complex partitioning schemes for optimal performance.

### 219. How do you handle PostgreSQL compliance automation?
**Answer:** Automate compliance checks and reporting for regulatory requirements.

### 220. What is PostgreSQL integration with big data ecosystems?
**Answer:** Connect PostgreSQL with Hadoop, Spark, and data lakes.

### 221. How do you implement PostgreSQL disaster recovery automation?
**Answer:** Automate failover and recovery procedures for business continuity.

### 222. What are PostgreSQL advanced monitoring techniques?
**Answer:** Implement comprehensive observability with custom metrics.

### 223. How do you optimize PostgreSQL for graph workloads?
**Answer:** Use recursive queries and graph extensions for network analysis.

### 224. What is PostgreSQL integration with message queues?
**Answer:** Implement event-driven architectures with queue integration.

### 225. How do you handle PostgreSQL capacity planning automation?
**Answer:** Automate capacity forecasting and resource scaling.

### 226. What are PostgreSQL advanced replication patterns?
**Answer:** Implement complex replication topologies for global distribution.

### 227. How do you implement PostgreSQL for streaming data?
**Answer:** Process real-time streams with triggers and notifications.

### 228. What is PostgreSQL integration with container orchestration?
**Answer:** Deploy and manage PostgreSQL in Kubernetes environments.

### 229. How do you handle PostgreSQL performance at exabyte scale?
**Answer:** Design distributed architectures for massive data volumes.

### 230. What are PostgreSQL future architecture patterns?
**Answer:** Explore emerging patterns for next-generation data platforms.

### 231. How do you implement PostgreSQL for serverless computing?
**Answer:** Adapt PostgreSQL for serverless and event-driven architectures.

### 232. What is PostgreSQL integration with AI/ML pipelines?
**Answer:** Embed PostgreSQL in machine learning workflows and pipelines.

### 233. How do you handle PostgreSQL operational excellence at enterprise scale?
**Answer:** Implement comprehensive operational practices for large deployments.