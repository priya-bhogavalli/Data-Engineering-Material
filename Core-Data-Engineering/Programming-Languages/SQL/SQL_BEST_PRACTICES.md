# SQL Best Practices for Data Engineering

## Code Style and Formatting

### Naming Conventions
```sql
-- Use descriptive, lowercase names with underscores
-- Good
CREATE TABLE customer_orders (
    customer_id INTEGER,
    order_date DATE,
    total_amount DECIMAL(10,2)
);

-- Avoid abbreviations and unclear names
-- Bad
CREATE TABLE cust_ord (
    cid INTEGER,
    dt DATE,
    amt DECIMAL(10,2)
);

-- Table names should be plural nouns
CREATE TABLE employees;      -- Good
CREATE TABLE employee;       -- Avoid

-- Column names should be singular
customer_id                  -- Good
customers_id                 -- Avoid

-- Use consistent prefixes for related tables
fact_sales, dim_customer, dim_product    -- Good for data warehouse
sales_fact, customer_dim, product_dim    -- Also acceptable
```

### SQL Formatting
```sql
-- Use consistent indentation and line breaks
-- Good
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(o.order_id) as order_count,
    SUM(o.total_amount) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.registration_date >= '2024-01-01'
  AND c.status = 'active'
GROUP BY 
    c.customer_id,
    c.first_name,
    c.last_name
HAVING COUNT(o.order_id) > 0
ORDER BY total_spent DESC;

-- Align keywords and use consistent capitalization
-- Keywords in UPPERCASE, identifiers in lowercase
SELECT customer_id, first_name
FROM customers
WHERE status = 'active';

-- Use meaningful aliases
SELECT 
    c.customer_name,
    o.order_date,
    oi.quantity
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id;
```

### Comments and Documentation
```sql
-- Use comments to explain complex logic
-- Calculate customer lifetime value using 12-month rolling window
WITH customer_metrics AS (
    SELECT 
        customer_id,
        -- Total orders in last 12 months
        COUNT(*) as order_count,
        -- Average days between orders
        AVG(EXTRACT(DAYS FROM order_date - LAG(order_date) OVER (
            PARTITION BY customer_id ORDER BY order_date
        ))) as avg_days_between_orders
    FROM orders
    WHERE order_date >= CURRENT_DATE - INTERVAL '12 months'
    GROUP BY customer_id
)
SELECT * FROM customer_metrics;

-- Document table purposes and relationships
/*
Customer dimension table for data warehouse
- Contains current and historical customer information
- SCD Type 2 implementation with effective/end dates
- Primary key: customer_key (surrogate key)
- Business key: customer_id (from source system)
*/
CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    customer_name VARCHAR(200) NOT NULL,
    -- ... other columns
    effective_date DATE NOT NULL,
    end_date DATE,
    is_current BOOLEAN DEFAULT TRUE
);
```

## Query Optimization

### Index Strategy
```sql
-- Create indexes for frequently queried columns
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);

-- Use composite indexes for multi-column queries
-- Order matters: most selective column first
CREATE INDEX idx_orders_status_date ON orders(status, order_date);

-- Use covering indexes to avoid table lookups
CREATE INDEX idx_orders_customer_covering 
ON orders(customer_id, order_date) 
INCLUDE (total_amount, status);

-- Create partial indexes for filtered queries
CREATE INDEX idx_active_customers 
ON customers(last_name) 
WHERE status = 'active';

-- Monitor and drop unused indexes
-- They slow down INSERT/UPDATE/DELETE operations
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0;  -- Never used indexes
```

### Query Writing Best Practices
```sql
-- Use EXISTS instead of IN for better performance with large datasets
-- Good
SELECT customer_name
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id
);

-- Less efficient for large datasets
SELECT customer_name
FROM customers c
WHERE customer_id IN (
    SELECT customer_id FROM orders
);

-- Avoid functions in WHERE clauses - they prevent index usage
-- Bad
SELECT * FROM orders 
WHERE YEAR(order_date) = 2024;

-- Good
SELECT * FROM orders 
WHERE order_date >= '2024-01-01' 
  AND order_date < '2025-01-01';

-- Use LIMIT to prevent accidentally large result sets
SELECT * FROM large_table 
ORDER BY created_date DESC 
LIMIT 1000;

-- Use specific column names instead of SELECT *
-- Good
SELECT customer_id, customer_name, email FROM customers;

-- Avoid (wastes network bandwidth and memory)
SELECT * FROM customers;
```

### JOIN Optimization
```sql
-- Put most selective conditions in WHERE clause, not JOIN
-- Good
SELECT c.customer_name, o.order_date
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE c.status = 'active'
  AND o.order_date >= '2024-01-01';

-- Less optimal
SELECT c.customer_name, o.order_date
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
    AND c.status = 'active'
    AND o.order_date >= '2024-01-01';

-- Use appropriate JOIN types
-- INNER JOIN when you need matching records from both tables
-- LEFT JOIN when you need all records from left table
-- Avoid CROSS JOIN unless specifically needed
```

## Data Quality and Integrity

### Constraint Implementation
```sql
-- Use appropriate constraints to ensure data quality
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    registration_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'active',
    
    -- Check constraints for data validation
    CONSTRAINT chk_email_format CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT chk_phone_format CHECK (phone ~ '^\+?[1-9]\d{1,14}$' OR phone IS NULL),
    CONSTRAINT chk_status_values CHECK (status IN ('active', 'inactive', 'suspended')),
    CONSTRAINT chk_registration_date CHECK (registration_date <= CURRENT_DATE)
);

-- Use foreign key constraints to maintain referential integrity
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    
    CONSTRAINT fk_orders_customer 
        FOREIGN KEY (customer_id) 
        REFERENCES customers(customer_id)
        ON DELETE RESTRICT  -- Prevent deletion of customers with orders
        ON UPDATE CASCADE   -- Update order records if customer_id changes
);
```

### Data Validation Queries
```sql
-- Create reusable data quality checks
-- Check for duplicate records
SELECT 
    email,
    COUNT(*) as duplicate_count
FROM customers
GROUP BY email
HAVING COUNT(*) > 1;

-- Check for null values in critical columns
SELECT 
    COUNT(*) as total_records,
    COUNT(customer_name) as non_null_names,
    COUNT(*) - COUNT(customer_name) as null_names,
    ROUND((COUNT(*) - COUNT(customer_name))::DECIMAL / COUNT(*) * 100, 2) as null_percentage
FROM customers;

-- Check referential integrity
SELECT COUNT(*)
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;  -- Orders without valid customers

-- Check data ranges and business rules
SELECT 
    COUNT(*) as invalid_orders
FROM orders
WHERE order_date > CURRENT_DATE  -- Future orders
   OR total_amount < 0           -- Negative amounts
   OR total_amount > 1000000;    -- Suspiciously high amounts
```

## Security Best Practices

### Access Control
```sql
-- Create role-based access control
-- Create roles for different user types
CREATE ROLE data_analyst;
CREATE ROLE data_engineer;
CREATE ROLE application_user;

-- Grant appropriate permissions
-- Read-only access for analysts
GRANT SELECT ON ALL TABLES IN SCHEMA public TO data_analyst;
GRANT USAGE ON SCHEMA public TO data_analyst;

-- Full access for engineers
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO data_engineer;
GRANT ALL PRIVILEGES ON SCHEMA public TO data_engineer;

-- Limited access for applications
GRANT SELECT, INSERT, UPDATE ON customers TO application_user;
GRANT SELECT, INSERT, UPDATE ON orders TO application_user;

-- Create users and assign roles
CREATE USER analyst_john WITH PASSWORD 'secure_password';
GRANT data_analyst TO analyst_john;
```

### SQL Injection Prevention
```sql
-- Use parameterized queries (application level)
-- Good (parameterized query example)
-- SELECT * FROM customers WHERE customer_id = $1;

-- Never concatenate user input directly
-- Bad example (vulnerable to SQL injection)
-- query = "SELECT * FROM customers WHERE name = '" + user_input + "'";

-- Use stored procedures for complex operations
CREATE OR REPLACE FUNCTION get_customer_orders(p_customer_id INTEGER)
RETURNS TABLE(order_id INTEGER, order_date DATE, total_amount DECIMAL) AS $$
BEGIN
    RETURN QUERY
    SELECT o.order_id, o.order_date, o.total_amount
    FROM orders o
    WHERE o.customer_id = p_customer_id
      AND o.status != 'deleted';
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### Data Masking and Privacy
```sql
-- Create views with masked sensitive data for non-production environments
CREATE VIEW customers_masked AS
SELECT 
    customer_id,
    'Customer_' || customer_id as customer_name,  -- Mask real names
    SUBSTRING(email, 1, 3) || '***@' || 
    SUBSTRING(email, POSITION('@' IN email) + 1) as email,  -- Mask email
    LEFT(phone, 3) || '-XXX-XXXX' as phone,  -- Mask phone
    registration_date,
    status
FROM customers;

-- Use row-level security for multi-tenant applications
ALTER TABLE customer_data ENABLE ROW LEVEL SECURITY;

CREATE POLICY customer_isolation ON customer_data
    FOR ALL TO application_role
    USING (tenant_id = current_setting('app.current_tenant')::INTEGER);
```

## Performance Monitoring

### Query Performance Analysis
```sql
-- Monitor slow queries (PostgreSQL example)
-- Enable pg_stat_statements extension
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Find slowest queries
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

-- Monitor table sizes and growth
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
    pg_total_relation_size(schemaname||'.'||tablename) as size_bytes
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY size_bytes DESC;

-- Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as index_scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

### Maintenance Tasks
```sql
-- Regular maintenance procedures
-- Update table statistics
ANALYZE customers;
ANALYZE orders;

-- Rebuild indexes if needed (PostgreSQL)
REINDEX INDEX idx_customers_email;

-- Clean up old data with proper archiving
-- Archive old orders before deletion
INSERT INTO orders_archive 
SELECT * FROM orders 
WHERE order_date < CURRENT_DATE - INTERVAL '7 years';

-- Delete archived data
DELETE FROM orders 
WHERE order_date < CURRENT_DATE - INTERVAL '7 years';

-- Vacuum tables to reclaim space (PostgreSQL)
VACUUM ANALYZE orders;
```

## Data Engineering Specific Practices

### ETL/ELT Best Practices
```sql
-- Use staging tables for data loading
CREATE TABLE staging_customers (
    LIKE customers INCLUDING ALL
);

-- Load data into staging first
COPY staging_customers FROM '/path/to/data.csv' WITH CSV HEADER;

-- Validate data before moving to production
-- Check for required fields
SELECT COUNT(*) FROM staging_customers WHERE customer_name IS NULL;

-- Check for duplicates
SELECT email, COUNT(*) 
FROM staging_customers 
GROUP BY email 
HAVING COUNT(*) > 1;

-- Use UPSERT operations for incremental loads
INSERT INTO customers (customer_id, customer_name, email, updated_at)
SELECT customer_id, customer_name, email, CURRENT_TIMESTAMP
FROM staging_customers
ON CONFLICT (customer_id) 
DO UPDATE SET
    customer_name = EXCLUDED.customer_name,
    email = EXCLUDED.email,
    updated_at = EXCLUDED.updated_at;
```

### Slowly Changing Dimensions (SCD)
```sql
-- SCD Type 2 implementation
CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    customer_name VARCHAR(200) NOT NULL,
    email VARCHAR(255),
    address TEXT,
    effective_date DATE NOT NULL,
    end_date DATE,
    is_current BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SCD Type 2 merge procedure
CREATE OR REPLACE FUNCTION update_customer_dimension()
RETURNS void AS $$
BEGIN
    -- Close current records that have changed
    UPDATE dim_customer 
    SET 
        end_date = CURRENT_DATE - 1,
        is_current = FALSE
    WHERE customer_id IN (
        SELECT s.customer_id
        FROM staging_customers s
        INNER JOIN dim_customer d ON s.customer_id = d.customer_id
        WHERE d.is_current = TRUE
          AND (s.customer_name != d.customer_name 
               OR s.email != d.email 
               OR s.address != d.address)
    );
    
    -- Insert new records for changed customers
    INSERT INTO dim_customer (customer_id, customer_name, email, address, effective_date)
    SELECT 
        s.customer_id,
        s.customer_name,
        s.email,
        s.address,
        CURRENT_DATE
    FROM staging_customers s
    WHERE s.customer_id IN (
        SELECT customer_id 
        FROM dim_customer 
        WHERE end_date = CURRENT_DATE - 1
    );
    
    -- Insert completely new customers
    INSERT INTO dim_customer (customer_id, customer_name, email, address, effective_date)
    SELECT 
        s.customer_id,
        s.customer_name,
        s.email,
        s.address,
        CURRENT_DATE
    FROM staging_customers s
    WHERE s.customer_id NOT IN (
        SELECT DISTINCT customer_id FROM dim_customer
    );
END;
$$ LANGUAGE plpgsql;
```

### Data Lineage and Documentation
```sql
-- Document data transformations with comments
-- Source: customer_raw table from CRM system
-- Transformation: Clean phone numbers, standardize addresses
-- Target: dim_customer in data warehouse
CREATE VIEW customer_clean AS
SELECT 
    customer_id,
    TRIM(UPPER(customer_name)) as customer_name,
    LOWER(TRIM(email)) as email,
    -- Standardize phone format: remove all non-digits, add country code
    CASE 
        WHEN LENGTH(REGEXP_REPLACE(phone, '[^0-9]', '', 'g')) = 10 
        THEN '+1' || REGEXP_REPLACE(phone, '[^0-9]', '', 'g')
        ELSE phone
    END as phone_standardized,
    created_date
FROM customer_raw
WHERE email IS NOT NULL 
  AND email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$';

-- Create metadata tables for data lineage
CREATE TABLE data_lineage (
    lineage_id SERIAL PRIMARY KEY,
    source_table VARCHAR(100),
    target_table VARCHAR(100),
    transformation_logic TEXT,
    created_by VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Document transformations
INSERT INTO data_lineage (source_table, target_table, transformation_logic, created_by)
VALUES (
    'customer_raw',
    'dim_customer',
    'Clean and standardize customer data: normalize names to uppercase, emails to lowercase, standardize phone format',
    'data_engineer'
);
```

## Error Handling and Logging

### Transaction Management
```sql
-- Use transactions for data consistency
BEGIN;

-- Perform related operations together
INSERT INTO customers (customer_name, email) 
VALUES ('John Doe', 'john@example.com');

INSERT INTO customer_preferences (customer_id, preference_type, preference_value)
VALUES (LASTVAL(), 'newsletter', 'true');

-- Check if everything succeeded
-- COMMIT if successful, ROLLBACK if any errors
COMMIT;

-- Use savepoints for partial rollbacks
BEGIN;

INSERT INTO orders (customer_id, order_date) VALUES (1, CURRENT_DATE);
SAVEPOINT order_created;

INSERT INTO order_items (order_id, product_id, quantity) 
VALUES (LASTVAL(), 999, 1);  -- This might fail

-- If order_items insert fails, rollback to savepoint
-- ROLLBACK TO SAVEPOINT order_created;
-- Continue with other operations or commit the order without items

COMMIT;
```

### Error Logging
```sql
-- Create audit/log tables
CREATE TABLE data_processing_log (
    log_id SERIAL PRIMARY KEY,
    process_name VARCHAR(100),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status VARCHAR(20),  -- 'success', 'error', 'warning'
    records_processed INTEGER,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Log ETL processes
CREATE OR REPLACE FUNCTION log_etl_process(
    p_process_name VARCHAR(100),
    p_status VARCHAR(20),
    p_records_processed INTEGER DEFAULT NULL,
    p_error_message TEXT DEFAULT NULL
) RETURNS void AS $$
BEGIN
    INSERT INTO data_processing_log (
        process_name, 
        status, 
        records_processed, 
        error_message,
        end_time
    ) VALUES (
        p_process_name,
        p_status,
        p_records_processed,
        p_error_message,
        CURRENT_TIMESTAMP
    );
END;
$$ LANGUAGE plpgsql;

-- Usage example
-- SELECT log_etl_process('customer_dimension_update', 'success', 1500);
-- SELECT log_etl_process('order_fact_load', 'error', 0, 'Connection timeout to source system');
```

## Testing and Validation

### Unit Testing for SQL
```sql
-- Create test data setup
CREATE SCHEMA IF NOT EXISTS test_data;

-- Test data for customer scenarios
CREATE TABLE test_data.customers_test AS
SELECT * FROM customers WHERE 1=0;  -- Copy structure only

INSERT INTO test_data.customers_test VALUES
(1, 'John Doe', 'john@example.com', '2024-01-01', 'active'),
(2, 'Jane Smith', 'jane@example.com', '2024-01-15', 'inactive'),
(3, 'Bob Johnson', 'bob@example.com', '2024-02-01', 'active');

-- Test function: validate customer segmentation logic
CREATE OR REPLACE FUNCTION test_customer_segmentation()
RETURNS TABLE(test_name TEXT, passed BOOLEAN, details TEXT) AS $$
BEGIN
    -- Test 1: Active customers should be included
    RETURN QUERY
    SELECT 
        'Active customers included'::TEXT,
        (SELECT COUNT(*) FROM customer_segments_view WHERE status = 'active') = 2,
        'Expected 2 active customers, got ' || (SELECT COUNT(*) FROM customer_segments_view WHERE status = 'active')::TEXT;
    
    -- Test 2: Inactive customers should be excluded
    RETURN QUERY
    SELECT 
        'Inactive customers excluded'::TEXT,
        (SELECT COUNT(*) FROM customer_segments_view WHERE status = 'inactive') = 0,
        'Expected 0 inactive customers in segments, got ' || (SELECT COUNT(*) FROM customer_segments_view WHERE status = 'inactive')::TEXT;
END;
$$ LANGUAGE plpgsql;

-- Run tests
SELECT * FROM test_customer_segmentation();
```

### Data Quality Tests
```sql
-- Create automated data quality checks
CREATE OR REPLACE FUNCTION run_data_quality_checks()
RETURNS TABLE(
    check_name TEXT,
    table_name TEXT,
    passed BOOLEAN,
    error_count INTEGER,
    details TEXT
) AS $$
BEGIN
    -- Check for null values in required fields
    RETURN QUERY
    SELECT 
        'Required fields not null'::TEXT,
        'customers'::TEXT,
        (SELECT COUNT(*) FROM customers WHERE customer_name IS NULL OR email IS NULL) = 0,
        (SELECT COUNT(*) FROM customers WHERE customer_name IS NULL OR email IS NULL)::INTEGER,
        'Found null values in required fields'::TEXT;
    
    -- Check for duplicate emails
    RETURN QUERY
    SELECT 
        'Unique email addresses'::TEXT,
        'customers'::TEXT,
        (SELECT COUNT(*) FROM (SELECT email FROM customers GROUP BY email HAVING COUNT(*) > 1) dups) = 0,
        (SELECT COUNT(*) FROM (SELECT email FROM customers GROUP BY email HAVING COUNT(*) > 1) dups)::INTEGER,
        'Found duplicate email addresses'::TEXT;
    
    -- Check referential integrity
    RETURN QUERY
    SELECT 
        'Valid customer references'::TEXT,
        'orders'::TEXT,
        (SELECT COUNT(*) FROM orders o LEFT JOIN customers c ON o.customer_id = c.customer_id WHERE c.customer_id IS NULL) = 0,
        (SELECT COUNT(*) FROM orders o LEFT JOIN customers c ON o.customer_id = c.customer_id WHERE c.customer_id IS NULL)::INTEGER,
        'Found orders with invalid customer references'::TEXT;
END;
$$ LANGUAGE plpgsql;

-- Schedule regular data quality checks
-- This would typically be called from an ETL tool or cron job
SELECT * FROM run_data_quality_checks();
```

Remember: These best practices should be adapted to your specific database system, organizational requirements, and use cases. Regular review and updates of these practices are essential as your data engineering needs evolve.