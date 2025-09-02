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

## 💾 Core Concepts

### 1. Data Types and Schema Design
```sql
-- Comprehensive data types example
CREATE TABLE comprehensive_example (
    -- Numeric types
    id SERIAL PRIMARY KEY,
    price DECIMAL(10,2),
    quantity INTEGER,
    weight REAL,
    
    -- Text types
    username VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    status CHAR(1) DEFAULT 'A',
    
    -- Date/Time types
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
    is_active BOOLEAN DEFAULT TRUE
);
```

### 2. Advanced Querying
```sql
-- Window functions for analytics
SELECT 
    employee_id,
    department,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rank,
    AVG(salary) OVER (PARTITION BY department) as dept_avg,
    LAG(salary, 1) OVER (PARTITION BY department ORDER BY hire_date) as prev_salary
FROM employees;

-- Common Table Expressions (CTEs)
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        SUM(amount) as total_sales
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT 
    month,
    total_sales,
    LAG(total_sales) OVER (ORDER BY month) as prev_month_sales
FROM monthly_sales;

-- Recursive CTEs for hierarchical data
WITH RECURSIVE employee_hierarchy AS (
    SELECT employee_id, name, manager_id, 1 as level
    FROM employees WHERE manager_id IS NULL
    
    UNION ALL
    
    SELECT e.employee_id, e.name, e.manager_id, eh.level + 1
    FROM employees e
    JOIN employee_hierarchy eh ON e.manager_id = eh.employee_id
)
SELECT * FROM employee_hierarchy ORDER BY level, name;
```

### 3. JSON Operations
```sql
-- JSON data manipulation
CREATE TABLE user_profiles (
    user_id SERIAL PRIMARY KEY,
    profile JSONB
);

-- Insert and query JSON data
INSERT INTO user_profiles (profile) VALUES 
('{"name": "John", "age": 30, "preferences": {"theme": "dark"}}');

SELECT 
    user_id,
    profile->>'name' as name,
    profile->'preferences'->>'theme' as theme
FROM user_profiles
WHERE profile->'preferences'->>'theme' = 'dark';

-- JSON aggregation
SELECT jsonb_agg(profile) as all_profiles FROM user_profiles;
```

### 4. Performance Optimization
```sql
-- Index strategies
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_active_users ON users(username) WHERE status = 'active';
CREATE INDEX idx_user_profiles_gin ON user_profiles USING GIN(profile);

-- Table partitioning
CREATE TABLE sales_partitioned (
    id SERIAL,
    sale_date DATE NOT NULL,
    amount DECIMAL(10,2)
) PARTITION BY RANGE (sale_date);

CREATE TABLE sales_2024_q1 PARTITION OF sales_partitioned
FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');
```

## 🔧 Data Engineering Workflows

### 1. ETL Pipeline Implementation
```sql
-- ETL stored procedure
CREATE OR REPLACE FUNCTION etl_process_sales()
RETURNS TEXT AS $$
DECLARE
    v_processed_count INTEGER := 0;
BEGIN
    INSERT INTO warehouse.fact_sales (customer_key, sale_date, amount)
    SELECT dc.customer_key, s.sale_date, s.amount
    FROM staging.raw_sales s
    JOIN warehouse.dim_customers dc ON s.customer_id = dc.customer_id;
    
    GET DIAGNOSTICS v_processed_count = ROW_COUNT;
    RETURN 'Processed ' || v_processed_count || ' records';
END;
$$ LANGUAGE plpgsql;
```

### 2. Data Quality Framework
```sql
-- Data quality check function
CREATE OR REPLACE FUNCTION check_data_quality(p_table_name VARCHAR)
RETURNS TABLE(rule_type TEXT, passed BOOLEAN, message TEXT) AS $$
BEGIN
    -- Null checks
    RETURN QUERY
    SELECT 'null_check'::TEXT, 
           (SELECT COUNT(*) FROM information_schema.tables WHERE table_name = p_table_name) > 0,
           'Table exists check'::TEXT;
END;
$$ LANGUAGE plpgsql;
```

## 📊 Monitoring and Maintenance

### 1. Performance Monitoring
```sql
-- Query performance monitoring
SELECT 
    query,
    calls,
    total_time,
    mean_time
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;

-- Index usage analysis
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

## 🎯 Best Practices Summary

### 1. Schema Design
- Use appropriate data types to minimize storage
- Implement proper constraints for data integrity
- Use JSONB over JSON for better performance

### 2. Query Optimization
- Use EXPLAIN ANALYZE to understand execution plans
- Create indexes on frequently queried columns
- Leverage window functions for analytics

### 3. Performance
- Regular VACUUM and ANALYZE operations
- Monitor query performance with pg_stat_statements
- Use connection pooling for high-concurrency applications

### 4. Security
- Use role-based access control
- Implement Row Level Security for multi-tenant apps
- Encrypt sensitive data

This guide provides essential PostgreSQL knowledge for data engineering. Focus on JSON support, window functions, and proper indexing for optimal performance.