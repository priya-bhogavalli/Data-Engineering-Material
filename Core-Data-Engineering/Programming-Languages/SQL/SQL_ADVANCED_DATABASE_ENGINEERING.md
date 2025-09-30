# SQL Advanced Database Engineering

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Query Optimization](#-query-optimization)
3. [Advanced Indexing Strategies](#-advanced-indexing-strategies)
4. [Stored Procedures & Functions](#-stored-procedures--functions)
5. [Database Design Patterns](#-database-design-patterns)
6. [Performance Tuning](#-performance-tuning)
7. [Security & Permissions](#-security--permissions)
8. [Backup & Recovery](#-backup--recovery)
9. [Monitoring & Maintenance](#-monitoring--maintenance)
10. [Enterprise Patterns](#-enterprise-patterns)

---

## 🎯 Overview

This document covers advanced SQL concepts for production database engineering, including optimization, security, and enterprise-scale patterns essential for data engineering roles.

**Prerequisites:** Complete [SQL Key Concepts](./SQL_KEY_CONCEPTS.md) for foundational knowledge.

## 📚 Related Documents

- **[SQL Key Concepts](./SQL_KEY_CONCEPTS.md)** - Fundamental SQL concepts and theory
- **[SQL Quick Reference](./SQL_QUICK_REFERENCE.md)** - Essential commands and patterns
- **[SQL Interview Questions](./SQL_INTERVIEW_QUESTIONS.md)** - Interview preparation

## ⚡ Query Optimization

### Execution Plan Analysis

```sql
-- Analyze query performance with EXPLAIN
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT 
    c.customer_name,
    COUNT(o.order_id) as order_count,
    SUM(oi.quantity * oi.price) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
WHERE c.registration_date >= '2023-01-01'
GROUP BY c.customer_id, c.customer_name
HAVING SUM(oi.quantity * oi.price) > 1000
ORDER BY total_spent DESC;

-- Optimization techniques
-- 1. Add indexes on join columns
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_customers_registration_date ON customers(registration_date);

-- 2. Rewrite with CTE for better readability and potential optimization
WITH customer_orders AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        o.order_id
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    WHERE c.registration_date >= '2023-01-01'
),
order_totals AS (
    SELECT 
        co.customer_id,
        co.customer_name,
        COUNT(co.order_id) as order_count,
        COALESCE(SUM(oi.quantity * oi.price), 0) as total_spent
    FROM customer_orders co
    LEFT JOIN order_items oi ON co.order_id = oi.order_id
    GROUP BY co.customer_id, co.customer_name
)
SELECT * FROM order_totals
WHERE total_spent > 1000
ORDER BY total_spent DESC;
```

### Query Rewriting Techniques

```sql
-- Optimize EXISTS vs IN
-- ✅ Preferred: EXISTS (stops at first match)
SELECT customer_name
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id 
    AND o.order_date >= '2024-01-01'
);

-- ❌ Slower: IN with subquery
SELECT customer_name
FROM customers c
WHERE c.customer_id IN (
    SELECT o.customer_id FROM orders o 
    WHERE o.order_date >= '2024-01-01'
);

-- Optimize UNION vs UNION ALL
-- ✅ Use UNION ALL when duplicates are acceptable (faster)
SELECT 'Q1' as quarter, SUM(amount) as total
FROM sales WHERE quarter = 1
UNION ALL
SELECT 'Q2' as quarter, SUM(amount) as total
FROM sales WHERE quarter = 2;

-- Window functions vs self-joins
-- ✅ Preferred: Window function
SELECT 
    employee_id,
    salary,
    salary - LAG(salary) OVER (ORDER BY hire_date) as salary_increase
FROM employees;

-- ❌ Slower: Self-join
SELECT 
    e1.employee_id,
    e1.salary,
    e1.salary - e2.salary as salary_increase
FROM employees e1
LEFT JOIN employees e2 ON e1.hire_date > e2.hire_date
WHERE e2.hire_date = (
    SELECT MAX(hire_date) 
    FROM employees e3 
    WHERE e3.hire_date < e1.hire_date
);
```

## 🔍 Advanced Indexing Strategies

### Composite Index Design

```sql
-- Create sample table for indexing examples
CREATE TABLE user_activities (
    user_id INT,
    activity_date DATE,
    activity_type VARCHAR(50),
    duration_minutes INT,
    device_type VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Composite index design principles
-- 1. Most selective column first
CREATE INDEX idx_activities_user_date_type 
ON user_activities(user_id, activity_date, activity_type);

-- 2. Support multiple query patterns
-- This index supports:
-- - WHERE user_id = ?
-- - WHERE user_id = ? AND activity_date = ?
-- - WHERE user_id = ? AND activity_date = ? AND activity_type = ?

-- Query that uses the index efficiently
SELECT COUNT(*)
FROM user_activities
WHERE user_id = 12345
  AND activity_date BETWEEN '2024-01-01' AND '2024-01-31'
  AND activity_type = 'login';

-- Covering index (includes all needed columns)
CREATE INDEX idx_activities_covering
ON user_activities(user_id, activity_date) 
INCLUDE (activity_type, duration_minutes);

-- This query can be satisfied entirely from the index
SELECT activity_type, SUM(duration_minutes)
FROM user_activities
WHERE user_id = 12345 AND activity_date = '2024-01-01'
GROUP BY activity_type;
```

### Specialized Index Types

```sql
-- Partial indexes (PostgreSQL)
CREATE INDEX idx_active_users 
ON users(last_login_date) 
WHERE is_active = true;

-- Expression indexes
CREATE INDEX idx_users_email_lower 
ON users(LOWER(email));

-- This query can use the expression index
SELECT * FROM users WHERE LOWER(email) = 'alice@example.com';

-- GIN index for JSON data (PostgreSQL)
CREATE TABLE user_preferences (
    user_id INT,
    preferences JSONB
);

CREATE INDEX idx_preferences_gin ON user_preferences USING GIN(preferences);

-- Query JSON data efficiently
SELECT user_id 
FROM user_preferences 
WHERE preferences @> '{"theme": "dark"}';

-- Full-text search index
CREATE INDEX idx_products_search 
ON products USING GIN(to_tsvector('english', name || ' ' || description));

-- Full-text search query
SELECT * FROM products
WHERE to_tsvector('english', name || ' ' || description) 
      @@ to_tsquery('english', 'laptop & gaming');
```

## 🔧 Stored Procedures & Functions

### Advanced Function Patterns

```sql
-- Table-valued function for reusable logic
CREATE OR REPLACE FUNCTION get_customer_metrics(
    p_customer_id INT,
    p_start_date DATE DEFAULT NULL,
    p_end_date DATE DEFAULT NULL
)
RETURNS TABLE (
    metric_name VARCHAR(50),
    metric_value DECIMAL(15,2),
    metric_date DATE
) AS $$
BEGIN
    -- Set default dates if not provided
    p_start_date := COALESCE(p_start_date, CURRENT_DATE - INTERVAL '1 year');
    p_end_date := COALESCE(p_end_date, CURRENT_DATE);
    
    RETURN QUERY
    WITH customer_stats AS (
        SELECT 
            COUNT(DISTINCT o.order_id) as total_orders,
            SUM(oi.quantity * oi.price) as total_spent,
            AVG(oi.quantity * oi.price) as avg_order_value,
            MAX(o.order_date) as last_order_date
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.customer_id = p_customer_id
          AND o.order_date BETWEEN p_start_date AND p_end_date
    )
    SELECT 'Total Orders'::VARCHAR(50), total_orders::DECIMAL(15,2), p_end_date
    FROM customer_stats
    UNION ALL
    SELECT 'Total Spent'::VARCHAR(50), total_spent, p_end_date
    FROM customer_stats
    UNION ALL
    SELECT 'Average Order Value'::VARCHAR(50), avg_order_value, p_end_date
    FROM customer_stats;
END;
$$ LANGUAGE plpgsql;

-- Usage
SELECT * FROM get_customer_metrics(12345, '2024-01-01', '2024-12-31');
```

### Error Handling and Transactions

```sql
-- Robust stored procedure with error handling
CREATE OR REPLACE FUNCTION process_bulk_orders(
    p_orders JSON
)
RETURNS TABLE (
    order_id INT,
    status VARCHAR(20),
    message TEXT
) AS $$
DECLARE
    order_record RECORD;
    v_order_id INT;
    v_error_message TEXT;
BEGIN
    -- Process each order in the JSON array
    FOR order_record IN 
        SELECT * FROM json_to_recordset(p_orders) AS x(
            customer_id INT,
            items JSON,
            order_date DATE
        )
    LOOP
        BEGIN
            -- Start savepoint for each order
            SAVEPOINT order_processing;
            
            -- Insert order
            INSERT INTO orders (customer_id, order_date, status)
            VALUES (order_record.customer_id, order_record.order_date, 'pending')
            RETURNING orders.order_id INTO v_order_id;
            
            -- Insert order items
            INSERT INTO order_items (order_id, product_id, quantity, price)
            SELECT 
                v_order_id,
                (item->>'product_id')::INT,
                (item->>'quantity')::INT,
                (item->>'price')::DECIMAL(10,2)
            FROM json_array_elements(order_record.items) AS item;
            
            -- Update order status
            UPDATE orders SET status = 'confirmed' WHERE orders.order_id = v_order_id;
            
            -- Return success
            RETURN QUERY SELECT v_order_id, 'SUCCESS'::VARCHAR(20), 'Order processed successfully'::TEXT;
            
        EXCEPTION WHEN OTHERS THEN
            -- Rollback to savepoint
            ROLLBACK TO SAVEPOINT order_processing;
            
            -- Get error details
            GET STACKED DIAGNOSTICS v_error_message = MESSAGE_TEXT;
            
            -- Return error
            RETURN QUERY SELECT 
                COALESCE(v_order_id, -1), 
                'ERROR'::VARCHAR(20), 
                v_error_message::TEXT;
        END;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

## 🏗️ Database Design Patterns

### Temporal Data Patterns

```sql
-- Slowly Changing Dimension (SCD) Type 2
CREATE TABLE customer_history (
    customer_key SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    customer_name VARCHAR(100),
    email VARCHAR(100),
    address TEXT,
    valid_from TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    valid_to TIMESTAMP DEFAULT '9999-12-31 23:59:59',
    is_current BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Function to handle SCD Type 2 updates
CREATE OR REPLACE FUNCTION update_customer_scd2(
    p_customer_id INT,
    p_customer_name VARCHAR(100),
    p_email VARCHAR(100),
    p_address TEXT
)
RETURNS VOID AS $$
BEGIN
    -- Close current record
    UPDATE customer_history 
    SET valid_to = CURRENT_TIMESTAMP,
        is_current = FALSE
    WHERE customer_id = p_customer_id 
      AND is_current = TRUE;
    
    -- Insert new record
    INSERT INTO customer_history (
        customer_id, customer_name, email, address
    ) VALUES (
        p_customer_id, p_customer_name, p_email, p_address
    );
END;
$$ LANGUAGE plpgsql;

-- Event sourcing pattern
CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    aggregate_id UUID NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB NOT NULL,
    event_version INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(aggregate_id, event_version)
);

-- Materialized view for current state
CREATE MATERIALIZED VIEW customer_current_state AS
WITH latest_events AS (
    SELECT 
        aggregate_id,
        event_data,
        ROW_NUMBER() OVER (PARTITION BY aggregate_id ORDER BY event_version DESC) as rn
    FROM events
    WHERE event_type IN ('CustomerCreated', 'CustomerUpdated')
)
SELECT 
    aggregate_id as customer_id,
    event_data->>'name' as customer_name,
    event_data->>'email' as email,
    event_data->>'address' as address
FROM latest_events
WHERE rn = 1;

-- Refresh the materialized view
REFRESH MATERIALIZED VIEW customer_current_state;
```

### Partitioning Strategies

```sql
-- Range partitioning by date
CREATE TABLE sales_data (
    sale_id SERIAL,
    sale_date DATE NOT NULL,
    customer_id INT,
    amount DECIMAL(10,2),
    product_id INT
) PARTITION BY RANGE (sale_date);

-- Create partitions for each quarter
CREATE TABLE sales_data_2024_q1 PARTITION OF sales_data
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE sales_data_2024_q2 PARTITION OF sales_data
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

CREATE TABLE sales_data_2024_q3 PARTITION OF sales_data
    FOR VALUES FROM ('2024-07-01') TO ('2024-10-01');

CREATE TABLE sales_data_2024_q4 PARTITION OF sales_data
    FOR VALUES FROM ('2024-10-01') TO ('2025-01-01');

-- Hash partitioning for even distribution
CREATE TABLE user_sessions (
    session_id UUID PRIMARY KEY,
    user_id INT NOT NULL,
    session_start TIMESTAMP,
    session_end TIMESTAMP,
    page_views INT
) PARTITION BY HASH (user_id);

-- Create hash partitions
CREATE TABLE user_sessions_0 PARTITION OF user_sessions
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);

CREATE TABLE user_sessions_1 PARTITION OF user_sessions
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);

CREATE TABLE user_sessions_2 PARTITION OF user_sessions
    FOR VALUES WITH (MODULUS 4, REMAINDER 2);

CREATE TABLE user_sessions_3 PARTITION OF user_sessions
    FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

## 🚀 Performance Tuning

### Connection Pooling and Resource Management

```sql
-- Configure connection pooling (PostgreSQL example)
-- postgresql.conf settings
/*
max_connections = 200
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
*/

-- Monitor connection usage
SELECT 
    state,
    COUNT(*) as connection_count,
    AVG(EXTRACT(EPOCH FROM (now() - state_change))) as avg_duration_seconds
FROM pg_stat_activity 
WHERE state IS NOT NULL
GROUP BY state;

-- Find long-running queries
SELECT 
    pid,
    now() - pg_stat_activity.query_start AS duration,
    query,
    state
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes'
  AND state = 'active'
ORDER BY duration DESC;
```

### Query Performance Monitoring

```sql
-- Create performance monitoring views
CREATE VIEW slow_queries AS
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements
WHERE calls > 100
ORDER BY mean_time DESC;

-- Index usage statistics
CREATE VIEW index_usage AS
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch,
    idx_scan,
    CASE 
        WHEN idx_scan = 0 THEN 'Never used'
        WHEN idx_scan < 100 THEN 'Rarely used'
        ELSE 'Frequently used'
    END as usage_category
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Table bloat analysis
CREATE VIEW table_bloat AS
WITH constants AS (
    SELECT current_setting('block_size')::numeric AS bs, 23 AS hdr, 4 AS ma
),
bloat_info AS (
    SELECT
        ma,bs,schemaname,tablename,
        (datawidth+(hdr+ma-(case when hdr%ma=0 THEN ma ELSE hdr%ma END)))::numeric AS datahdr,
        (maxfracsum*(nullhdr+ma-(case when nullhdr%ma=0 THEN ma ELSE nullhdr%ma END))) AS nullhdr2
    FROM (
        SELECT
            schemaname, tablename, hdr, ma, bs,
            SUM((1-null_frac)*avg_width) AS datawidth,
            MAX(null_frac) AS maxfracsum,
            hdr+(
                SELECT 1+count(*)/8
                FROM pg_stats s2
                WHERE null_frac<>0 AND s2.schemaname = s.schemaname AND s2.tablename = s.tablename
            ) AS nullhdr
        FROM pg_stats s, constants
        GROUP BY 1,2,3,4,5
    ) AS foo
)
SELECT
    schemaname, tablename,
    cc.relpages, bs,
    CEIL((cc.reltuples*((datahdr+ma-
        (CASE WHEN datahdr%ma=0 THEN ma ELSE datahdr%ma END))+nullhdr2+4))/(bs-20::float)) AS otta,
    COALESCE(c2.relpages,0) AS relpages,
    COALESCE(c2.relpages,0)*bs AS size_bytes,
    CASE WHEN cc.relpages < otta THEN 0 ELSE bs*(cc.relpages-otta)::bigint END AS bloat_bytes,
    CASE WHEN cc.relpages < otta THEN 0 ELSE ((cc.relpages-otta)::float*100/cc.relpages) END AS bloat_ratio
FROM bloat_info
JOIN pg_class cc ON cc.relname = bloat_info.tablename
JOIN pg_namespace nn ON cc.relnamespace = nn.oid AND nn.nspname = bloat_info.schemaname AND nn.nspname <> 'information_schema'
LEFT JOIN pg_class c2 ON cc.reltoastrelid = c2.oid
WHERE cc.relkind = 'r'
ORDER BY bloat_bytes DESC;
```

## 🔒 Security & Permissions

### Role-Based Access Control

```sql
-- Create roles hierarchy
CREATE ROLE data_readers;
CREATE ROLE data_writers;
CREATE ROLE data_admins;

-- Grant basic permissions
GRANT CONNECT ON DATABASE analytics TO data_readers;
GRANT USAGE ON SCHEMA public TO data_readers;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO data_readers;

-- Grant write permissions
GRANT data_readers TO data_writers;
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO data_writers;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO data_writers;

-- Grant admin permissions
GRANT data_writers TO data_admins;
GRANT CREATE ON SCHEMA public TO data_admins;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO data_admins;

-- Create specific user accounts
CREATE USER analyst_alice WITH PASSWORD 'secure_password_123';
CREATE USER developer_bob WITH PASSWORD 'secure_password_456';
CREATE USER admin_charlie WITH PASSWORD 'secure_password_789';

-- Assign roles
GRANT data_readers TO analyst_alice;
GRANT data_writers TO developer_bob;
GRANT data_admins TO admin_charlie;

-- Row-level security
CREATE POLICY customer_data_policy ON customers
    FOR ALL TO data_readers
    USING (customer_id = current_setting('app.current_customer_id')::INT);

ALTER TABLE customers ENABLE ROW LEVEL SECURITY;
```

### Data Encryption and Masking

```sql
-- Column-level encryption (PostgreSQL with pgcrypto)
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Create table with encrypted columns
CREATE TABLE sensitive_data (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50),
    email_encrypted BYTEA,  -- Encrypted email
    ssn_encrypted BYTEA,    -- Encrypted SSN
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert encrypted data
INSERT INTO sensitive_data (username, email_encrypted, ssn_encrypted)
VALUES (
    'alice',
    pgp_sym_encrypt('alice@example.com', 'encryption_key'),
    pgp_sym_encrypt('123-45-6789', 'encryption_key')
);

-- Query encrypted data
SELECT 
    username,
    pgp_sym_decrypt(email_encrypted, 'encryption_key') as email,
    pgp_sym_decrypt(ssn_encrypted, 'encryption_key') as ssn
FROM sensitive_data
WHERE username = 'alice';

-- Data masking view for non-privileged users
CREATE VIEW customers_masked AS
SELECT 
    customer_id,
    customer_name,
    CASE 
        WHEN current_user IN ('admin_charlie', 'developer_bob') 
        THEN email
        ELSE REGEXP_REPLACE(email, '(.{2}).*(@.*)', '\1***\2')
    END as email,
    CASE 
        WHEN current_user = 'admin_charlie'
        THEN phone
        ELSE REGEXP_REPLACE(phone, '(.{3}).*(.{4})', '\1-***-\2')
    END as phone
FROM customers;
```

## 💾 Backup & Recovery

### Automated Backup Strategies

```sql
-- Point-in-time recovery setup (PostgreSQL)
-- postgresql.conf settings
/*
wal_level = replica
archive_mode = on
archive_command = 'cp %p /backup/archive/%f'
max_wal_senders = 3
checkpoint_completion_target = 0.9
*/

-- Create backup script (would be in shell/batch file)
/*
#!/bin/bash
BACKUP_DIR="/backup/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

# Full backup
pg_basebackup -D $BACKUP_DIR -Ft -z -P -U backup_user

# Logical backup for specific schemas
pg_dump -h localhost -U backup_user -n public -n analytics \
        --format=custom --compress=9 \
        analytics_db > $BACKUP_DIR/logical_backup.dump

# Cleanup old backups (keep 7 days)
find /backup -type d -mtime +7 -exec rm -rf {} \;
*/

-- Recovery verification queries
CREATE OR REPLACE FUNCTION verify_backup_integrity()
RETURNS TABLE (
    table_name TEXT,
    row_count BIGINT,
    last_modified TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        t.table_name::TEXT,
        (xpath('//row/c/text()', 
               query_to_xml(format('SELECT COUNT(*) as c FROM %I.%I', 
                                 t.table_schema, t.table_name), 
                           false, true, '')))[1]::text::BIGINT as row_count,
        COALESCE(
            (SELECT MAX(last_modified) 
             FROM information_schema.tables t2 
             WHERE t2.table_name = t.table_name), 
            CURRENT_TIMESTAMP
        ) as last_modified
    FROM information_schema.tables t
    WHERE t.table_schema = 'public'
      AND t.table_type = 'BASE TABLE'
    ORDER BY t.table_name;
END;
$$ LANGUAGE plpgsql;
```

### Disaster Recovery Procedures

```sql
-- Create disaster recovery monitoring
CREATE TABLE dr_checkpoints (
    checkpoint_id SERIAL PRIMARY KEY,
    checkpoint_name VARCHAR(100),
    last_backup_time TIMESTAMP,
    backup_size_bytes BIGINT,
    verification_status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Automated DR health check
CREATE OR REPLACE FUNCTION dr_health_check()
RETURNS TABLE (
    check_name TEXT,
    status TEXT,
    details TEXT,
    last_check TIMESTAMP
) AS $$
BEGIN
    -- Check backup freshness
    RETURN QUERY
    SELECT 
        'Backup Freshness'::TEXT,
        CASE 
            WHEN MAX(created_at) > CURRENT_TIMESTAMP - INTERVAL '24 hours' 
            THEN 'HEALTHY'::TEXT
            ELSE 'WARNING'::TEXT
        END,
        'Last backup: ' || MAX(created_at)::TEXT,
        CURRENT_TIMESTAMP
    FROM dr_checkpoints;
    
    -- Check replication lag (if applicable)
    RETURN QUERY
    SELECT 
        'Replication Lag'::TEXT,
        CASE 
            WHEN pg_last_wal_receive_lsn() = pg_last_wal_replay_lsn() 
            THEN 'HEALTHY'::TEXT
            ELSE 'WARNING'::TEXT
        END,
        'Lag: ' || (pg_wal_lsn_diff(pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn()) / 1024)::TEXT || ' KB',
        CURRENT_TIMESTAMP;
    
    -- Check disk space
    RETURN QUERY
    SELECT 
        'Disk Space'::TEXT,
        'HEALTHY'::TEXT,  -- Would implement actual disk space check
        'Available space sufficient'::TEXT,
        CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql;
```

## 📊 Monitoring & Maintenance

### Automated Maintenance Tasks

```sql
-- Create maintenance log table
CREATE TABLE maintenance_log (
    log_id SERIAL PRIMARY KEY,
    task_name VARCHAR(100),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status VARCHAR(20),
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Automated statistics update
CREATE OR REPLACE FUNCTION update_table_statistics()
RETURNS VOID AS $$
DECLARE
    table_record RECORD;
    start_time TIMESTAMP;
    end_time TIMESTAMP;
BEGIN
    start_time := CURRENT_TIMESTAMP;
    
    FOR table_record IN 
        SELECT schemaname, tablename 
        FROM pg_tables 
        WHERE schemaname = 'public'
    LOOP
        BEGIN
            EXECUTE format('ANALYZE %I.%I', table_record.schemaname, table_record.tablename);
            
            INSERT INTO maintenance_log (task_name, start_time, end_time, status, details)
            VALUES (
                'ANALYZE ' || table_record.tablename,
                start_time,
                CURRENT_TIMESTAMP,
                'SUCCESS',
                'Statistics updated successfully'
            );
            
        EXCEPTION WHEN OTHERS THEN
            INSERT INTO maintenance_log (task_name, start_time, end_time, status, details)
            VALUES (
                'ANALYZE ' || table_record.tablename,
                start_time,
                CURRENT_TIMESTAMP,
                'ERROR',
                SQLERRM
            );
        END;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Index maintenance
CREATE OR REPLACE FUNCTION reindex_fragmented_indexes()
RETURNS VOID AS $$
DECLARE
    index_record RECORD;
BEGIN
    -- Find indexes with high fragmentation
    FOR index_record IN
        SELECT 
            schemaname,
            tablename,
            indexname
        FROM pg_stat_user_indexes
        WHERE idx_scan > 0  -- Only reindex used indexes
          AND pg_relation_size(indexrelid) > 1024 * 1024  -- Larger than 1MB
    LOOP
        BEGIN
            EXECUTE format('REINDEX INDEX CONCURRENTLY %I.%I', 
                          index_record.schemaname, 
                          index_record.indexname);
            
            INSERT INTO maintenance_log (task_name, start_time, end_time, status, details)
            VALUES (
                'REINDEX ' || index_record.indexname,
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP,
                'SUCCESS',
                'Index rebuilt successfully'
            );
            
        EXCEPTION WHEN OTHERS THEN
            INSERT INTO maintenance_log (task_name, start_time, end_time, status, details)
            VALUES (
                'REINDEX ' || index_record.indexname,
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP,
                'ERROR',
                SQLERRM
            );
        END;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

## 🏢 Enterprise Patterns

### Multi-Tenant Architecture

```sql
-- Schema-based multi-tenancy
CREATE SCHEMA tenant_1;
CREATE SCHEMA tenant_2;
CREATE SCHEMA tenant_3;

-- Create identical table structure in each schema
DO $$
DECLARE
    tenant_schema TEXT;
BEGIN
    FOR tenant_schema IN SELECT unnest(ARRAY['tenant_1', 'tenant_2', 'tenant_3'])
    LOOP
        EXECUTE format('
            CREATE TABLE %I.customers (
                customer_id SERIAL PRIMARY KEY,
                customer_name VARCHAR(100),
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )', tenant_schema);
        
        EXECUTE format('
            CREATE TABLE %I.orders (
                order_id SERIAL PRIMARY KEY,
                customer_id INT REFERENCES %I.customers(customer_id),
                order_date DATE,
                total_amount DECIMAL(10,2)
            )', tenant_schema, tenant_schema);
    END LOOP;
END;
$$;

-- Row-level multi-tenancy alternative
CREATE TABLE multi_tenant_customers (
    customer_id SERIAL PRIMARY KEY,
    tenant_id INT NOT NULL,
    customer_name VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create tenant-specific views
CREATE VIEW tenant_1_customers AS
SELECT customer_id, customer_name, email, created_at
FROM multi_tenant_customers
WHERE tenant_id = 1;

-- Tenant isolation function
CREATE OR REPLACE FUNCTION set_tenant_context(p_tenant_id INT)
RETURNS VOID AS $$
BEGIN
    PERFORM set_config('app.tenant_id', p_tenant_id::TEXT, false);
END;
$$ LANGUAGE plpgsql;

-- Row-level security for tenant isolation
CREATE POLICY tenant_isolation ON multi_tenant_customers
    FOR ALL TO PUBLIC
    USING (tenant_id = current_setting('app.tenant_id')::INT);

ALTER TABLE multi_tenant_customers ENABLE ROW LEVEL SECURITY;
```

### Data Archiving Strategies

```sql
-- Create archive tables
CREATE TABLE orders_archive (
    LIKE orders INCLUDING ALL
);

-- Partition archive table by year
ALTER TABLE orders_archive 
ADD CONSTRAINT orders_archive_date_check 
CHECK (order_date < CURRENT_DATE - INTERVAL '1 year');

-- Automated archiving function
CREATE OR REPLACE FUNCTION archive_old_orders()
RETURNS INTEGER AS $$
DECLARE
    archived_count INTEGER;
    cutoff_date DATE;
BEGIN
    cutoff_date := CURRENT_DATE - INTERVAL '2 years';
    
    -- Move old orders to archive
    WITH archived_orders AS (
        DELETE FROM orders 
        WHERE order_date < cutoff_date
        RETURNING *
    )
    INSERT INTO orders_archive 
    SELECT * FROM archived_orders;
    
    GET DIAGNOSTICS archived_count = ROW_COUNT;
    
    -- Log the archiving operation
    INSERT INTO maintenance_log (task_name, start_time, end_time, status, details)
    VALUES (
        'Archive Old Orders',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP,
        'SUCCESS',
        format('Archived %s orders older than %s', archived_count, cutoff_date)
    );
    
    RETURN archived_count;
END;
$$ LANGUAGE plpgsql;

-- Schedule archiving (would use cron or scheduler)
-- SELECT cron.schedule('archive-orders', '0 2 * * 0', 'SELECT archive_old_orders();');
```

This advanced SQL documentation provides production-ready patterns for enterprise database engineering, covering optimization, security, monitoring, and maintenance essential for data engineering roles.