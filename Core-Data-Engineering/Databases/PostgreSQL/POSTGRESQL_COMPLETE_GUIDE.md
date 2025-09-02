# PostgreSQL Complete Guide for Data Engineering

## 🎯 What is PostgreSQL?

PostgreSQL is an **advanced open-source relational database** known for its reliability, feature robustness, and performance. It's often called "the world's most advanced open source database" and is widely used in data engineering for its ACID compliance, extensibility, and support for both relational and non-relational data.

### Key Characteristics
- **ACID Compliant**: Full transaction support with strong consistency
- **Extensible**: Custom data types, functions, and operators
- **Standards Compliant**: Follows SQL standards closely
- **JSON Support**: Native JSON and JSONB data types
- **Advanced Features**: Window functions, CTEs, full-text search
- **High Performance**: Sophisticated query optimizer and indexing

## 🏗️ Architecture Overview

### PostgreSQL Architecture
```
┌─────────────────────────────────────────────────────────┐
│                   Client Applications                    │
│        (psql, pgAdmin, Application Drivers)             │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                 PostgreSQL Server                       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│  │   Parser    │ │  Planner    │ │  Executor   │       │
│  └─────────────┘ └─────────────┘ └─────────────┘       │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                   Storage Engine                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│  │Buffer Cache │ │   WAL       │ │Data Files   │       │
│  └─────────────┘ └─────────────┘ └─────────────┘       │
└─────────────────────────────────────────────────────────┘
```

**Client Layer**: Applications and tools connecting to PostgreSQL
**Server Layer**: Query processing, planning, and execution
**Storage Layer**: Data persistence, caching, and transaction logging

## 💾 Core Concepts

### 1. Data Types and Schema Design
```sql
-- Comprehensive data types example
CREATE TABLE comprehensive_example (
    -- Numeric types
    id SERIAL PRIMARY KEY,
    big_id BIGSERIAL,
    price DECIMAL(10,2),
    quantity INTEGER,
    weight REAL,
    precise_weight DOUBLE PRECISION,
    
    -- Text types
    username VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    status CHAR(1) DEFAULT 'A',
    
    -- Date/Time types
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    birth_date DATE,
    duration INTERVAL,
    
    -- JSON types
    settings JSONB,
    metadata JSON,
    
    -- Array types
    tags TEXT[],
    scores INTEGER[],
    
    -- UUID type
    uuid_field UUID DEFAULT gen_random_uuid(),
    
    -- Boolean
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Network types
    ip_address INET,
    mac_address MACADDR,
    
    -- Geometric types
    location POINT,
    area POLYGON
);

-- Constraints and indexes
ALTER TABLE comprehensive_example 
ADD CONSTRAINT check_price_positive CHECK (price > 0),
ADD CONSTRAINT check_status_valid CHECK (status IN ('A', 'I', 'P'));

CREATE INDEX idx_username_lower ON comprehensive_example(LOWER(username));
CREATE INDEX idx_settings_gin ON comprehensive_example USING GIN(settings);
CREATE INDEX idx_tags_gin ON comprehensive_example USING GIN(tags);
```

### 2. Advanced Querying
```sql
-- Window functions for analytics
SELECT 
    employee_id,
    department,
    salary,
    -- Ranking functions
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rank,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dense_rank,
    PERCENT_RANK() OVER (PARTITION BY department ORDER BY salary) as percentile,
    
    -- Aggregate window functions
    AVG(salary) OVER (PARTITION BY department) as dept_avg,
    SUM(salary) OVER (PARTITION BY department) as dept_total,
    COUNT(*) OVER (PARTITION BY department) as dept_count,
    
    -- Offset functions
    LAG(salary, 1) OVER (PARTITION BY department ORDER BY hire_date) as prev_salary,
    LEAD(salary, 1) OVER (PARTITION BY department ORDER BY hire_date) as next_salary,
    
    -- Frame functions
    SUM(salary) OVER (
        PARTITION BY department 
        ORDER BY hire_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_total
FROM employees;

-- Common Table Expressions (CTEs)
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        SUM(amount) as total_sales,
        COUNT(*) as order_count
    FROM orders
    WHERE order_date >= '2024-01-01'
    GROUP BY DATE_TRUNC('month', order_date)
),
sales_with_growth AS (
    SELECT 
        month,
        total_sales,
        order_count,
        LAG(total_sales) OVER (ORDER BY month) as prev_month_sales,
        (total_sales - LAG(total_sales) OVER (ORDER BY month)) / 
        NULLIF(LAG(total_sales) OVER (ORDER BY month), 0) * 100 as growth_rate
    FROM monthly_sales
)
SELECT 
    month,
    total_sales,
    order_count,
    ROUND(growth_rate, 2) as growth_percentage
FROM sales_with_growth
ORDER BY month;

-- Recursive CTEs for hierarchical data
WITH RECURSIVE employee_hierarchy AS (
    -- Base case: top-level managers
    SELECT 
        employee_id, 
        name, 
        manager_id, 
        1 as level,
        name::TEXT as path
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive case: employees with managers
    SELECT 
        e.employee_id, 
        e.name, 
        e.manager_id, 
        eh.level + 1,
        eh.path || ' -> ' || e.name
    FROM employees e
    JOIN employee_hierarchy eh ON e.manager_id = eh.employee_id
    WHERE eh.level < 10  -- Prevent infinite recursion
)
SELECT 
    level,
    REPEAT('  ', level - 1) || name as indented_name,
    path
FROM employee_hierarchy 
ORDER BY path;
```

### 3. JSON Operations
```sql
-- JSON data manipulation
CREATE TABLE user_profiles (
    user_id SERIAL PRIMARY KEY,
    profile JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert JSON data
INSERT INTO user_profiles (profile) VALUES 
('{
    "name": "John Doe",
    "age": 30,
    "email": "john@example.com",
    "preferences": {
        "theme": "dark",
        "notifications": {
            "email": true,
            "sms": false,
            "push": true
        }
    },
    "tags": ["developer", "postgresql", "data"]
}');

-- Query JSON data
SELECT 
    user_id,
    profile->>'name' as name,
    profile->>'email' as email,
    (profile->>'age')::INTEGER as age,
    profile->'preferences'->>'theme' as theme,
    profile->'preferences'->'notifications'->>'email' as email_notifications
FROM user_profiles
WHERE profile->'preferences'->'notifications'->>'email' = 'true';

-- JSON aggregation and building
SELECT 
    jsonb_build_object(
        'total_users', COUNT(*),
        'avg_age', AVG((profile->>'age')::INTEGER),
        'themes', jsonb_agg(DISTINCT profile->'preferences'->>'theme'),
        'users', jsonb_agg(
            jsonb_build_object(
                'name', profile->>'name',
                'email', profile->>'email'
            )
        )
    ) as summary
FROM user_profiles;

-- Update JSON fields
UPDATE user_profiles 
SET profile = profile || '{"last_login": "2024-01-15T10:30:00Z"}'
WHERE user_id = 1;

-- Remove JSON keys
UPDATE user_profiles 
SET profile = profile - 'temporary_field'
WHERE user_id = 1;

-- JSON path queries (PostgreSQL 12+)
SELECT 
    user_id,
    jsonb_path_query(profile, '$.preferences.notifications.*') as notifications,
    jsonb_path_query_array(profile, '$.tags[*]') as tags_array
FROM user_profiles;
```

### 4. Performance Optimization
```sql
-- Index strategies
-- B-tree index (default, good for equality and range queries)
CREATE INDEX idx_orders_date ON orders(order_date);

-- Partial index (smaller, faster for filtered queries)
CREATE INDEX idx_active_users ON users(username) WHERE status = 'active';

-- Composite index (multiple columns)
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- Expression index
CREATE INDEX idx_users_lower_email ON users(LOWER(email));

-- GIN index for JSON
CREATE INDEX idx_user_profiles_gin ON user_profiles USING GIN(profile);

-- GIN index for arrays
CREATE INDEX idx_product_tags ON products USING GIN(tags);

-- Full-text search index
CREATE INDEX idx_products_fts ON products 
USING GIN(to_tsvector('english', name || ' ' || description));

-- Analyze query performance
EXPLAIN (ANALYZE, BUFFERS, VERBOSE) 
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= '2024-01-01'
GROUP BY u.id, u.name
HAVING COUNT(o.id) > 5;

-- Table partitioning for large datasets
CREATE TABLE sales_partitioned (
    id SERIAL,
    sale_date DATE NOT NULL,
    amount DECIMAL(10,2),
    customer_id INTEGER,
    region VARCHAR(50)
) PARTITION BY RANGE (sale_date);

-- Create partitions
CREATE TABLE sales_2024_q1 PARTITION OF sales_partitioned
FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE sales_2024_q2 PARTITION OF sales_partitioned
FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- Partition pruning example
SELECT * FROM sales_partitioned 
WHERE sale_date BETWEEN '2024-02-01' AND '2024-02-29';
```

### 5. Stored Procedures and Functions
```sql
-- PL/pgSQL function with error handling
CREATE OR REPLACE FUNCTION process_order(
    p_customer_id INTEGER,
    p_items JSONB
) RETURNS TABLE(order_id INTEGER, total_amount DECIMAL) AS $$
DECLARE
    v_order_id INTEGER;
    v_total DECIMAL(10,2) := 0;
    v_item JSONB;
    v_product_price DECIMAL(10,2);
    v_quantity INTEGER;
BEGIN
    -- Start transaction
    BEGIN
        -- Create order
        INSERT INTO orders (customer_id, order_date, status)
        VALUES (p_customer_id, CURRENT_DATE, 'pending')
        RETURNING id INTO v_order_id;
        
        -- Process each item
        FOR v_item IN SELECT * FROM jsonb_array_elements(p_items)
        LOOP
            v_quantity := (v_item->>'quantity')::INTEGER;
            
            -- Get product price
            SELECT price INTO v_product_price
            FROM products 
            WHERE id = (v_item->>'product_id')::INTEGER;
            
            IF v_product_price IS NULL THEN
                RAISE EXCEPTION 'Product not found: %', v_item->>'product_id';
            END IF;
            
            -- Insert order item
            INSERT INTO order_items (order_id, product_id, quantity, price)
            VALUES (v_order_id, (v_item->>'product_id')::INTEGER, v_quantity, v_product_price);
            
            v_total := v_total + (v_quantity * v_product_price);
        END LOOP;
        
        -- Update order total
        UPDATE orders SET total_amount = v_total WHERE id = v_order_id;
        
        RETURN QUERY SELECT v_order_id, v_total;
        
    EXCEPTION
        WHEN OTHERS THEN
            RAISE EXCEPTION 'Error processing order: %', SQLERRM;
    END;
END;
$$ LANGUAGE plpgsql;

-- Trigger function for audit logging
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, operation, new_data, timestamp)
        VALUES (TG_TABLE_NAME, TG_OP, row_to_json(NEW), CURRENT_TIMESTAMP);
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, operation, old_data, new_data, timestamp)
        VALUES (TG_TABLE_NAME, TG_OP, row_to_json(OLD), row_to_json(NEW), CURRENT_TIMESTAMP);
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (table_name, operation, old_data, timestamp)
        VALUES (TG_TABLE_NAME, TG_OP, row_to_json(OLD), CURRENT_TIMESTAMP);
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to tables
CREATE TRIGGER users_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON users
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();
```

## 🔧 Data Engineering Workflows

### 1. ETL Pipeline Implementation
```sql
-- Create staging and target tables
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS warehouse;

-- Staging table for raw data
CREATE TABLE staging.raw_sales (
    id SERIAL PRIMARY KEY,
    raw_data JSONB,
    source_file VARCHAR(255),
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension tables
CREATE TABLE warehouse.dim_customers (
    customer_key SERIAL PRIMARY KEY,
    customer_id INTEGER UNIQUE,
    customer_name VARCHAR(100),
    email VARCHAR(100),
    registration_date DATE,
    customer_segment VARCHAR(50),
    is_active BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Fact table
CREATE TABLE warehouse.fact_sales (
    sale_key SERIAL PRIMARY KEY,
    customer_key INTEGER REFERENCES warehouse.dim_customers(customer_key),
    sale_date DATE,
    product_id INTEGER,
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ETL stored procedure
CREATE OR REPLACE FUNCTION etl_process_sales()
RETURNS TEXT AS $$
DECLARE
    v_processed_count INTEGER := 0;
    v_error_count INTEGER := 0;
    v_start_time TIMESTAMP := CURRENT_TIMESTAMP;
BEGIN
    -- Process staging data
    WITH processed_sales AS (
        SELECT 
            (raw_data->>'customer_id')::INTEGER as customer_id,
            (raw_data->>'sale_date')::DATE as sale_date,
            (raw_data->>'product_id')::INTEGER as product_id,
            (raw_data->>'quantity')::INTEGER as quantity,
            (raw_data->>'unit_price')::DECIMAL(10,2) as unit_price,
            (raw_data->>'total_amount')::DECIMAL(12,2) as total_amount
        FROM staging.raw_sales
        WHERE raw_data IS NOT NULL
    )
    INSERT INTO warehouse.fact_sales (
        customer_key, sale_date, product_id, quantity, unit_price, total_amount
    )
    SELECT 
        dc.customer_key,
        ps.sale_date,
        ps.product_id,
        ps.quantity,
        ps.unit_price,
        ps.total_amount
    FROM processed_sales ps
    JOIN warehouse.dim_customers dc ON ps.customer_id = dc.customer_id
    WHERE ps.customer_id IS NOT NULL
      AND ps.sale_date IS NOT NULL
      AND ps.total_amount > 0;
    
    GET DIAGNOSTICS v_processed_count = ROW_COUNT;
    
    -- Log ETL run
    INSERT INTO etl_log (process_name, start_time, end_time, records_processed, status)
    VALUES ('etl_process_sales', v_start_time, CURRENT_TIMESTAMP, v_processed_count, 'SUCCESS');
    
    RETURN 'Processed ' || v_processed_count || ' sales records';
    
EXCEPTION
    WHEN OTHERS THEN
        INSERT INTO etl_log (process_name, start_time, end_time, error_message, status)
        VALUES ('etl_process_sales', v_start_time, CURRENT_TIMESTAMP, SQLERRM, 'ERROR');
        
        RAISE EXCEPTION 'ETL process failed: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;
```

### 2. Data Quality Framework
```sql
-- Data quality rules table
CREATE TABLE data_quality_rules (
    rule_id SERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    column_name VARCHAR(100),
    rule_type VARCHAR(50),
    rule_definition TEXT,
    threshold_value DECIMAL,
    is_active BOOLEAN DEFAULT TRUE
);

-- Data quality results table
CREATE TABLE data_quality_results (
    result_id SERIAL PRIMARY KEY,
    rule_id INTEGER REFERENCES data_quality_rules(rule_id),
    check_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    passed BOOLEAN,
    actual_value DECIMAL,
    error_count INTEGER,
    total_count INTEGER
);

-- Data quality check function
CREATE OR REPLACE FUNCTION check_data_quality(p_table_name VARCHAR)
RETURNS TABLE(rule_id INTEGER, passed BOOLEAN, message TEXT) AS $$
DECLARE
    v_rule RECORD;
    v_sql TEXT;
    v_result RECORD;
    v_passed BOOLEAN;
    v_actual_value DECIMAL;
BEGIN
    FOR v_rule IN 
        SELECT * FROM data_quality_rules 
        WHERE table_name = p_table_name AND is_active = TRUE
    LOOP
        CASE v_rule.rule_type
            WHEN 'null_check' THEN
                v_sql := format('SELECT COUNT(*) as total, COUNT(%I) as non_null FROM %I',
                               v_rule.column_name, v_rule.table_name);
                EXECUTE v_sql INTO v_result;
                v_actual_value := (v_result.total - v_result.non_null) * 100.0 / v_result.total;
                v_passed := v_actual_value <= v_rule.threshold_value;
                
            WHEN 'duplicate_check' THEN
                v_sql := format('SELECT COUNT(*) as total, COUNT(DISTINCT %I) as unique_count FROM %I',
                               v_rule.column_name, v_rule.table_name);
                EXECUTE v_sql INTO v_result;
                v_actual_value := v_result.total - v_result.unique_count;
                v_passed := v_actual_value <= v_rule.threshold_value;
                
            WHEN 'range_check' THEN
                v_sql := format('SELECT COUNT(*) as violations FROM %I WHERE %s',
                               v_rule.table_name, v_rule.rule_definition);
                EXECUTE v_sql INTO v_result;
                v_actual_value := v_result.violations;
                v_passed := v_actual_value <= v_rule.threshold_value;
        END CASE;
        
        -- Log result
        INSERT INTO data_quality_results (rule_id, passed, actual_value)
        VALUES (v_rule.rule_id, v_passed, v_actual_value);
        
        RETURN QUERY SELECT v_rule.rule_id, v_passed, 
            format('Rule %s: %s (actual: %s, threshold: %s)', 
                   v_rule.rule_type, 
                   CASE WHEN v_passed THEN 'PASSED' ELSE 'FAILED' END,
                   v_actual_value, 
                   v_rule.threshold_value);
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

## 🔒 Security & Administration

### 1. User Management and Security
```sql
-- Create roles and users
CREATE ROLE data_engineers;
CREATE ROLE data_analysts;
CREATE ROLE data_scientists;

-- Grant privileges to roles
GRANT CONNECT ON DATABASE analytics TO data_analysts;
GRANT USAGE ON SCHEMA warehouse TO data_analysts;
GRANT SELECT ON ALL TABLES IN SCHEMA warehouse TO data_analysts;

-- Create users and assign roles
CREATE USER alice WITH PASSWORD 'secure_password';
GRANT data_engineers TO alice;

CREATE USER bob WITH PASSWORD 'secure_password';
GRANT data_analysts TO bob;

-- Row Level Security (RLS)
ALTER TABLE warehouse.fact_sales ENABLE ROW LEVEL SECURITY;

CREATE POLICY sales_region_policy ON warehouse.fact_sales
    FOR ALL TO data_analysts
    USING (region = current_setting('app.user_region', true));

-- Set user context
SELECT set_config('app.user_region', 'US', false);

-- Column-level security with views
CREATE VIEW warehouse.secure_customers AS
SELECT 
    customer_key,
    customer_name,
    CASE 
        WHEN current_user IN ('admin', 'data_engineer') THEN email
        ELSE REGEXP_REPLACE(email, '(.{2}).*(@.*)', '\1***\2')
    END as email,
    customer_segment
FROM warehouse.dim_customers;

GRANT SELECT ON warehouse.secure_customers TO data_analysts;
```

### 2. Backup and Recovery
```sql
-- Point-in-time recovery setup
-- Enable WAL archiving in postgresql.conf:
-- wal_level = replica
-- archive_mode = on
-- archive_command = 'cp %p /backup/archive/%f'

-- Create base backup
-- pg_basebackup -D /backup/base -Ft -z -P

-- Continuous archiving monitoring
CREATE TABLE backup_monitoring (
    backup_id SERIAL PRIMARY KEY,
    backup_type VARCHAR(20),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status VARCHAR(20),
    backup_size BIGINT,
    notes TEXT
);

-- Backup validation function
CREATE OR REPLACE FUNCTION validate_backup()
RETURNS TEXT AS $$
DECLARE
    v_last_wal_file TEXT;
    v_archive_status TEXT;
BEGIN
    -- Check WAL archiving status
    SELECT last_archived_wal, last_archived_time 
    INTO v_last_wal_file, v_archive_status
    FROM pg_stat_archiver;
    
    IF v_archive_status IS NULL OR 
       EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - v_archive_status)) > 3600 THEN
        RETURN 'WARNING: WAL archiving may be behind';
    END IF;
    
    RETURN 'Backup validation successful';
END;
$$ LANGUAGE plpgsql;
```

## 📊 Monitoring and Maintenance

### 1. Performance Monitoring
```sql
-- Query performance monitoring
CREATE VIEW query_performance AS
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements
ORDER BY total_time DESC;

-- Index usage analysis
CREATE VIEW index_usage AS
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Table bloat monitoring
CREATE OR REPLACE FUNCTION check_table_bloat()
RETURNS TABLE(
    schema_name TEXT,
    table_name TEXT,
    bloat_ratio NUMERIC,
    waste_size TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        schemaname::TEXT,
        tablename::TEXT,
        CASE 
            WHEN pg_relation_size(schemaname||'.'||tablename) > 0 
            THEN (pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename))::NUMERIC / pg_relation_size(schemaname||'.'||tablename)
            ELSE 0
        END as bloat_ratio,
        pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) as waste_size
    FROM pg_tables
    WHERE schemaname NOT IN ('information_schema', 'pg_catalog')
    ORDER BY bloat_ratio DESC;
END;
$$ LANGUAGE plpgsql;

-- Connection monitoring
SELECT 
    datname,
    usename,
    application_name,
    client_addr,
    state,
    query_start,
    state_change,
    query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY query_start;
```

### 2. Automated Maintenance
```sql
-- Maintenance scheduling function
CREATE OR REPLACE FUNCTION run_maintenance()
RETURNS TEXT AS $$
DECLARE
    v_table RECORD;
    v_result TEXT := '';
BEGIN
    -- Auto-vacuum and analyze tables that need it
    FOR v_table IN 
        SELECT schemaname, tablename
        FROM pg_stat_user_tables
        WHERE n_dead_tup > 1000 OR analyze_count = 0
    LOOP
        EXECUTE format('VACUUM ANALYZE %I.%I', v_table.schemaname, v_table.tablename);
        v_result := v_result || format('Vacuumed %s.%s; ', v_table.schemaname, v_table.tablename);
    END LOOP;
    
    -- Update table statistics
    ANALYZE;
    
    -- Reindex if needed
    REINDEX DATABASE CONCURRENTLY current_database();
    
    RETURN COALESCE(v_result, 'No maintenance needed');
END;
$$ LANGUAGE plpgsql;
```

## 🎯 Best Practices Summary

### 1. Schema Design Best Practices
- **Use appropriate data types** to minimize storage and improve performance
- **Implement proper constraints** for data integrity
- **Design normalized schemas** but denormalize for performance when needed
- **Use JSONB over JSON** for better performance and indexing
- **Implement proper indexing strategy** based on query patterns

### 2. Query Optimization Best Practices
- **Use EXPLAIN ANALYZE** to understand query execution plans
- **Create indexes** on frequently queried columns
- **Use partial indexes** for filtered queries
- **Leverage window functions** instead of self-joins when possible
- **Use CTEs** for complex queries to improve readability

### 3. Performance Best Practices
- **Regular VACUUM and ANALYZE** to maintain table statistics
- **Monitor query performance** with pg_stat_statements
- **Use connection pooling** to manage database connections
- **Implement table partitioning** for very large tables
- **Configure PostgreSQL parameters** based on workload

### 4. Security Best Practices
- **Use role-based access control** with principle of least privilege
- **Implement Row Level Security** for multi-tenant applications
- **Encrypt sensitive data** at rest and in transit
- **Regular security audits** and access reviews
- **Use SSL connections** for all client connections

### 5. Maintenance Best Practices
- **Regular backups** with point-in-time recovery capability
- **Monitor disk space** and plan for growth
- **Keep PostgreSQL updated** with latest security patches
- **Monitor replication lag** in high-availability setups
- **Document schema changes** and maintain version control

This guide provides a comprehensive foundation for using PostgreSQL effectively in data engineering scenarios. Focus on understanding the advanced features like JSON support, window functions, and proper indexing strategies for optimal performance.