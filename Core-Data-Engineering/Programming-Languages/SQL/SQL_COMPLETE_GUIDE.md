# SQL Complete Guide for Data Engineering

## 🎯 Overview
Comprehensive guide covering SQL fundamentals, advanced concepts, performance optimization, and data engineering best practices.

## 📋 Table of Contents

1. [SQL Fundamentals](#1-sql-fundamentals)
2. [Data Definition Language (DDL)](#2-data-definition-language-ddl)
3. [Data Manipulation Language (DML)](#3-data-manipulation-language-dml)
4. [Joins & Relationships](#4-joins--relationships)
5. [Advanced SQL Features](#5-advanced-sql-features)
6. [Performance Optimization](#6-performance-optimization)
7. [Best Practices](#7-best-practices)
8. [Interview Questions](#8-interview-questions)
9. [Data Engineering Patterns](#9-data-engineering-patterns)

---

## 1. SQL Fundamentals

### Basic Query Structure
```sql
SELECT column1, column2
FROM table_name
WHERE condition
GROUP BY column1
HAVING group_condition
ORDER BY column1
LIMIT number;
```

### Data Types
```sql
-- Numeric Types
INTEGER, BIGINT, DECIMAL(10,2), FLOAT, DOUBLE

-- String Types
VARCHAR(255), CHAR(10), TEXT

-- Date/Time Types
DATE, TIME, TIMESTAMP, DATETIME

-- Boolean
BOOLEAN (TRUE/FALSE/NULL)

-- JSON (PostgreSQL/MySQL)
JSON, JSONB
```

### Basic Operations
```sql
-- Arithmetic
SELECT price * quantity as total_amount FROM order_items;

-- String operations
SELECT UPPER(name), LENGTH(email), SUBSTRING(phone, 1, 3) FROM customers;

-- Date operations
SELECT EXTRACT(YEAR FROM order_date), DATE_TRUNC('month', order_date) FROM orders;

-- Conditional logic
SELECT 
    name,
    CASE 
        WHEN salary >= 100000 THEN 'Senior'
        WHEN salary >= 70000 THEN 'Mid-level'
        ELSE 'Junior'
    END as level
FROM employees;
```

---

## 2. Data Definition Language (DDL)

### Creating Tables
```sql
-- Basic table creation
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(200) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    registration_date DATE DEFAULT CURRENT_DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT chk_email_format CHECK (email LIKE '%@%'),
    CONSTRAINT chk_phone_length CHECK (LENGTH(phone) >= 10)
);

-- Create table with foreign key
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    order_amount DECIMAL(10,2) CHECK (order_amount > 0),
    status VARCHAR(20) DEFAULT 'pending',
    
    CONSTRAINT fk_orders_customer 
        FOREIGN KEY (customer_id) 
        REFERENCES customers(customer_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);
```

### Indexes
```sql
-- Single column index
CREATE INDEX idx_customers_email ON customers(email);

-- Composite index
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- Partial index
CREATE INDEX idx_active_customers ON customers(customer_id) 
WHERE is_active = TRUE;

-- Covering index
CREATE INDEX idx_orders_covering ON orders(customer_id, order_date) 
INCLUDE (order_amount, status);
```

### Altering Tables
```sql
-- Add column
ALTER TABLE customers ADD COLUMN last_login TIMESTAMP;

-- Modify column
ALTER TABLE customers ALTER COLUMN phone TYPE VARCHAR(25);

-- Add constraint
ALTER TABLE customers ADD CONSTRAINT fk_customer_segment 
    FOREIGN KEY (segment_id) REFERENCES customer_segments(id);

-- Drop constraint
ALTER TABLE customers DROP CONSTRAINT chk_phone_length;
```

---

## 3. Data Manipulation Language (DML)

### INSERT Operations
```sql
-- Single row insert
INSERT INTO customers (customer_name, email, phone)
VALUES ('John Doe', 'john@example.com', '555-1234');

-- Multiple row insert
INSERT INTO customers (customer_name, email, phone) VALUES
    ('Alice Smith', 'alice@example.com', '555-2345'),
    ('Bob Johnson', 'bob@example.com', '555-3456');

-- Insert from SELECT
INSERT INTO customer_summary (customer_id, total_orders, total_amount)
SELECT 
    customer_id,
    COUNT(*) as total_orders,
    SUM(order_amount) as total_amount
FROM orders
WHERE order_date >= '2024-01-01'
GROUP BY customer_id;

-- UPSERT (PostgreSQL)
INSERT INTO customers (customer_name, email, phone)
VALUES ('John Doe', 'john@example.com', '555-1234')
ON CONFLICT (email) 
DO UPDATE SET 
    customer_name = EXCLUDED.customer_name,
    phone = EXCLUDED.phone,
    updated_at = CURRENT_TIMESTAMP;
```

### UPDATE Operations
```sql
-- Simple update
UPDATE customers 
SET phone = '555-9999'
WHERE customer_id = 1;

-- Update with JOIN
UPDATE customers c
SET segment_id = s.id
FROM customer_segments s
WHERE c.total_spent BETWEEN s.min_spent AND s.max_spent;

-- Conditional update
UPDATE orders
SET status = CASE 
    WHEN order_date < CURRENT_DATE - INTERVAL '30 days' THEN 'archived'
    WHEN payment_status = 'paid' THEN 'completed'
    ELSE status
END;
```

### DELETE Operations
```sql
-- Simple delete
DELETE FROM customers WHERE is_active = FALSE;

-- Delete with subquery
DELETE FROM orders 
WHERE customer_id IN (
    SELECT customer_id 
    FROM customers 
    WHERE registration_date < '2020-01-01'
);
```

---

## 4. Joins & Relationships

### Join Types
```sql
-- INNER JOIN - only matching records
SELECT c.customer_name, o.order_date, o.order_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;

-- LEFT JOIN - all customers, matched orders
SELECT c.customer_name, COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name;

-- RIGHT JOIN - all orders, matched customers
SELECT COALESCE(c.customer_name, 'Unknown') as customer_name, o.order_date
FROM customers c
RIGHT JOIN orders o ON c.customer_id = o.customer_id;

-- FULL OUTER JOIN - all records from both tables
SELECT c.customer_name, o.order_date
FROM customers c
FULL OUTER JOIN orders o ON c.customer_id = o.customer_id;

-- SELF JOIN - join table to itself
SELECT e1.name as employee, e2.name as manager
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.employee_id;
```

### Complex Joins
```sql
-- Multiple table joins
SELECT 
    c.customer_name,
    o.order_date,
    p.product_name,
    oi.quantity,
    oi.unit_price
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date >= '2024-01-01';
```

---

## 5. Advanced SQL Features

### Window Functions
```sql
-- Ranking functions
SELECT 
    customer_name,
    order_amount,
    ROW_NUMBER() OVER (ORDER BY order_amount DESC) as unique_rank,
    RANK() OVER (ORDER BY order_amount DESC) as standard_rank,
    DENSE_RANK() OVER (ORDER BY order_amount DESC) as dense_rank,
    PERCENT_RANK() OVER (ORDER BY order_amount DESC) as percentile
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;

-- Partition by category
SELECT 
    product_name,
    category,
    price,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC) as price_rank_in_category
FROM products;

-- Running totals and moving averages
SELECT 
    order_date,
    order_amount,
    SUM(order_amount) OVER (ORDER BY order_date ROWS UNBOUNDED PRECEDING) as running_total,
    AVG(order_amount) OVER (ORDER BY order_date ROWS 2 PRECEDING) as moving_avg_3day
FROM orders
ORDER BY order_date;

-- Lead and Lag functions
SELECT 
    order_date,
    order_amount,
    LAG(order_amount, 1) OVER (ORDER BY order_date) as prev_amount,
    LEAD(order_amount, 1) OVER (ORDER BY order_date) as next_amount,
    order_amount - LAG(order_amount, 1) OVER (ORDER BY order_date) as amount_change
FROM orders
ORDER BY order_date;
```

### Common Table Expressions (CTEs)
```sql
-- Basic CTE
WITH high_value_customers AS (
    SELECT 
        customer_id,
        customer_name,
        SUM(order_amount) as total_spent
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY customer_id, customer_name
    HAVING SUM(order_amount) > 10000
)
SELECT 
    customer_name,
    total_spent,
    total_spent * 0.05 as loyalty_bonus
FROM high_value_customers
ORDER BY total_spent DESC;

-- Multiple CTEs
WITH 
customer_metrics AS (
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        SUM(order_amount) as total_spent,
        AVG(order_amount) as avg_order_value
    FROM orders
    GROUP BY customer_id
),
customer_segments AS (
    SELECT 
        customer_id,
        CASE 
            WHEN total_spent > 10000 THEN 'Premium'
            WHEN total_spent > 5000 THEN 'Gold'
            WHEN total_spent > 1000 THEN 'Silver'
            ELSE 'Bronze'
        END as segment
    FROM customer_metrics
)
SELECT 
    c.customer_name,
    cm.order_count,
    cm.total_spent,
    cs.segment
FROM customers c
JOIN customer_metrics cm ON c.customer_id = cm.customer_id
JOIN customer_segments cs ON c.customer_id = cs.customer_id;

-- Recursive CTE
WITH RECURSIVE employee_hierarchy AS (
    -- Base case: top-level managers
    SELECT 
        employee_id,
        employee_name,
        manager_id,
        1 as level,
        employee_name as path
    FROM employees 
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive case
    SELECT 
        e.employee_id,
        e.employee_name,
        e.manager_id,
        eh.level + 1,
        eh.path || ' -> ' || e.employee_name
    FROM employees e
    INNER JOIN employee_hierarchy eh ON e.manager_id = eh.employee_id
)
SELECT 
    employee_name,
    level,
    path
FROM employee_hierarchy
ORDER BY level, employee_name;
```

### Subqueries
```sql
-- Scalar subquery
SELECT 
    customer_name,
    total_orders,
    (SELECT AVG(order_count) FROM customer_summary) as avg_orders_all_customers
FROM customer_summary;

-- Correlated subquery
SELECT customer_name
FROM customers c
WHERE (
    SELECT COUNT(*)
    FROM orders o
    WHERE o.customer_id = c.customer_id
) > 5;

-- EXISTS subquery
SELECT customer_name
FROM customers c
WHERE EXISTS (
    SELECT 1 
    FROM orders o 
    WHERE o.customer_id = c.customer_id
);

-- IN subquery
SELECT product_name
FROM products
WHERE category_id IN (
    SELECT category_id 
    FROM categories 
    WHERE category_name IN ('Electronics', 'Books')
);
```

### Aggregation Functions
```sql
-- Basic aggregations
SELECT 
    COUNT(*) as total_orders,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(order_amount) as total_revenue,
    AVG(order_amount) as average_order_value,
    MIN(order_date) as first_order,
    MAX(order_date) as last_order,
    STDDEV(order_amount) as amount_std_dev
FROM orders;

-- GROUP BY with HAVING
SELECT 
    customer_id,
    COUNT(*) as order_count,
    SUM(order_amount) as total_spent,
    AVG(order_amount) as avg_order_value
FROM orders
WHERE order_date >= '2024-01-01'
GROUP BY customer_id
HAVING COUNT(*) >= 5 AND SUM(order_amount) > 1000
ORDER BY total_spent DESC;

-- Advanced grouping (ROLLUP, CUBE)
SELECT 
    COALESCE(region, 'All Regions') as region,
    COALESCE(category, 'All Categories') as category,
    SUM(sales_amount) as total_sales
FROM sales
GROUP BY ROLLUP(region, category)
ORDER BY region, category;
```

---

## 6. Performance Optimization

### Index Strategies
```sql
-- Analyze query performance
EXPLAIN (ANALYZE, BUFFERS) 
SELECT c.name, COUNT(o.order_id)
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.registration_date >= '2023-01-01'
GROUP BY c.customer_id, c.name;

-- Create appropriate indexes
CREATE INDEX idx_customers_reg_date ON customers(registration_date);
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- Composite index for common query patterns
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- Partial index for filtered queries
CREATE INDEX idx_active_orders ON orders(order_date) 
WHERE status = 'ACTIVE';
```

### Query Optimization Techniques
```sql
-- Use EXISTS instead of IN for better performance
-- Faster
SELECT * FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);

-- Slower for large datasets
SELECT * FROM customers 
WHERE customer_id IN (SELECT customer_id FROM orders);

-- Avoid functions in WHERE clause
-- Slower
SELECT * FROM orders WHERE YEAR(order_date) = 2024;

-- Faster
SELECT * FROM orders 
WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01';

-- Use LIMIT for large result sets
SELECT * FROM orders 
ORDER BY order_date DESC 
LIMIT 100;
```

### Statistics and Maintenance
```sql
-- Update table statistics
ANALYZE customers;
ANALYZE orders;

-- Check table and index sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Monitor index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

---

## 7. Best Practices

### Code Style
```sql
-- Use consistent formatting and naming
SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) as order_count,
    SUM(o.order_amount) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.registration_date >= '2024-01-01'
  AND c.status = 'active'
GROUP BY 
    c.customer_id,
    c.customer_name
HAVING COUNT(o.order_id) > 0
ORDER BY total_spent DESC;

-- Use meaningful table and column names
CREATE TABLE customer_orders (  -- Good: descriptive
    customer_id INTEGER,
    order_date DATE,
    total_amount DECIMAL(10,2)
);

-- Avoid abbreviations
CREATE TABLE cust_ord (  -- Bad: unclear
    cid INTEGER,
    dt DATE,
    amt DECIMAL(10,2)
);
```

### Data Quality
```sql
-- Use constraints for data validation
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    registration_date DATE DEFAULT CURRENT_DATE,
    
    -- Check constraints
    CONSTRAINT chk_email_format CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT chk_phone_format CHECK (phone ~ '^\+?[1-9]\d{1,14}$' OR phone IS NULL),
    CONSTRAINT chk_registration_date CHECK (registration_date <= CURRENT_DATE)
);

-- Data quality checks
SELECT 
    COUNT(*) as total_records,
    COUNT(customer_name) as non_null_names,
    COUNT(*) - COUNT(customer_name) as null_names,
    ROUND((COUNT(*) - COUNT(customer_name))::DECIMAL / COUNT(*) * 100, 2) as null_percentage
FROM customers;
```

### Security
```sql
-- Use parameterized queries (application level)
-- Good: SELECT * FROM customers WHERE customer_id = $1;
-- Bad:  SELECT * FROM customers WHERE customer_id = ' + user_input + ';

-- Create role-based access control
CREATE ROLE data_analyst;
CREATE ROLE data_engineer;

-- Grant appropriate permissions
GRANT SELECT ON ALL TABLES IN SCHEMA public TO data_analyst;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO data_engineer;

-- Row-level security
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;

CREATE POLICY customer_isolation ON customers
    FOR ALL TO application_role
    USING (tenant_id = current_setting('app.current_tenant_id')::INT);
```

---

## 8. Interview Questions

### Basic Level

#### 1. What's the difference between INNER JOIN and LEFT JOIN?
**Answer:**
- **INNER JOIN**: Returns only records that have matching values in both tables
- **LEFT JOIN**: Returns all records from the left table, plus matching records from the right table (NULL for non-matches)

```sql
-- INNER JOIN - only customers with orders
SELECT c.name, o.order_date
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;

-- LEFT JOIN - all customers, including those without orders
SELECT c.name, o.order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
```

#### 2. Explain the difference between WHERE and HAVING clauses
**Answer:**
- **WHERE**: Filters individual rows before any grouping occurs
- **HAVING**: Filters grouped results after GROUP BY aggregation
- **Execution Order**: WHERE → GROUP BY → HAVING → SELECT → ORDER BY

```sql
-- WHERE filters individual rows
SELECT department, COUNT(*)
FROM employees
WHERE salary > 50000
GROUP BY department;

-- HAVING filters grouped results
SELECT department, COUNT(*)
FROM employees
GROUP BY department
HAVING COUNT(*) > 5;
```

#### 3. What are window functions and how do they differ from aggregate functions?
**Answer:**
Window functions perform calculations across related rows without collapsing the result set.

```sql
-- Aggregate function - collapses to one row per group
SELECT department, AVG(salary)
FROM employees
GROUP BY department;

-- Window function - keeps all rows, adds calculated column
SELECT 
    name,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department) as dept_avg_salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank
FROM employees;
```

### Intermediate Level

#### 4. How do you find the second highest salary in each department?
**Answer:**
```sql
-- Method 1: Using ROW_NUMBER()
WITH ranked_salaries AS (
    SELECT 
        employee_id,
        name,
        department,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rn
    FROM employees
)
SELECT employee_id, name, department, salary
FROM ranked_salaries
WHERE rn = 2;

-- Method 2: Using DENSE_RANK() (handles ties better)
WITH ranked_salaries AS (
    SELECT 
        employee_id,
        name,
        department,
        salary,
        DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) as rank
    FROM employees
)
SELECT employee_id, name, department, salary
FROM ranked_salaries
WHERE rank = 2;
```

#### 5. How do you handle duplicate records?
**Answer:**
```sql
-- Find duplicates
SELECT email, COUNT(*)
FROM customers
GROUP BY email
HAVING COUNT(*) > 1;

-- Remove duplicates using ROW_NUMBER()
WITH duplicates AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY email ORDER BY created_date DESC) as rn
    FROM customers
)
DELETE FROM customers
WHERE id IN (SELECT id FROM duplicates WHERE rn > 1);

-- Keep latest record per group
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) as rn
    FROM orders
) ranked
WHERE rn = 1;
```

### Advanced Level

#### 6. Implement a pivot table in SQL
**Answer:**
```sql
-- Pivot sales data by quarter
SELECT 
    product_name,
    SUM(CASE WHEN quarter = 'Q1' THEN sales_amount ELSE 0 END) as Q1_sales,
    SUM(CASE WHEN quarter = 'Q2' THEN sales_amount ELSE 0 END) as Q2_sales,
    SUM(CASE WHEN quarter = 'Q3' THEN sales_amount ELSE 0 END) as Q3_sales,
    SUM(CASE WHEN quarter = 'Q4' THEN sales_amount ELSE 0 END) as Q4_sales,
    SUM(sales_amount) as total_sales
FROM quarterly_sales
GROUP BY product_name
ORDER BY total_sales DESC;
```

#### 7. Write a query to find gaps in sequential data
**Answer:**
```sql
-- Find missing order IDs in sequence
WITH order_sequence AS (
    SELECT 
        order_id,
        LAG(order_id) OVER (ORDER BY order_id) as prev_order_id
    FROM orders
    ORDER BY order_id
),
gaps AS (
    SELECT 
        prev_order_id + 1 as gap_start,
        order_id - 1 as gap_end
    FROM order_sequence
    WHERE order_id - prev_order_id > 1
)
SELECT 
    gap_start,
    gap_end,
    gap_end - gap_start + 1 as missing_count
FROM gaps;
```

---

## 9. Data Engineering Patterns

### ETL/ELT Patterns
```sql
-- Staging table approach
CREATE TABLE staging_customers (
    LIKE customers INCLUDING ALL
);

-- Load data into staging
COPY staging_customers FROM '/path/to/data.csv' WITH CSV HEADER;

-- Validate and transform
INSERT INTO customers (customer_id, customer_name, email, updated_at)
SELECT customer_id, customer_name, email, CURRENT_TIMESTAMP
FROM staging_customers
WHERE email IS NOT NULL AND email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
ON CONFLICT (customer_id) 
DO UPDATE SET
    customer_name = EXCLUDED.customer_name,
    email = EXCLUDED.email,
    updated_at = EXCLUDED.updated_at;
```

### Slowly Changing Dimensions (SCD Type 2)
```sql
-- SCD Type 2 implementation
CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    customer_name VARCHAR(200) NOT NULL,
    email VARCHAR(255),
    effective_date DATE NOT NULL,
    end_date DATE,
    is_current BOOLEAN DEFAULT TRUE
);

-- Update SCD Type 2
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
      AND (s.customer_name != d.customer_name OR s.email != d.email)
);

-- Insert new versions
INSERT INTO dim_customer (customer_id, customer_name, email, effective_date)
SELECT 
    s.customer_id,
    s.customer_name,
    s.email,
    CURRENT_DATE
FROM staging_customers s
WHERE s.customer_id IN (
    SELECT customer_id 
    FROM dim_customer 
    WHERE end_date = CURRENT_DATE - 1
);
```

### Data Quality Framework
```sql
-- Comprehensive data quality checks
WITH data_quality_checks AS (
    -- Check for duplicates
    SELECT 
        'Duplicate emails' as check_name,
        COUNT(*) as issue_count
    FROM (
        SELECT email, COUNT(*) as cnt
        FROM customers
        GROUP BY email
        HAVING COUNT(*) > 1
    ) duplicates
    
    UNION ALL
    
    -- Check for null values
    SELECT 
        'Null customer names' as check_name,
        COUNT(*) as issue_count
    FROM customers
    WHERE customer_name IS NULL
    
    UNION ALL
    
    -- Check for invalid data formats
    SELECT 
        'Invalid email formats' as check_name,
        COUNT(*) as issue_count
    FROM customers
    WHERE email NOT LIKE '%@%.%'
    
    UNION ALL
    
    -- Check for referential integrity
    SELECT 
        'Orders without customers' as check_name,
        COUNT(*) as issue_count
    FROM orders o
    LEFT JOIN customers c ON o.customer_id = c.customer_id
    WHERE c.customer_id IS NULL
)
SELECT 
    check_name,
    issue_count,
    CASE WHEN issue_count = 0 THEN 'PASS' ELSE 'FAIL' END as status
FROM data_quality_checks
ORDER BY issue_count DESC;
```

### Incremental Data Loading
```sql
-- Track last processed timestamp
CREATE TABLE etl_control (
    table_name VARCHAR(100) PRIMARY KEY,
    last_processed_timestamp TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Incremental load function
CREATE OR REPLACE FUNCTION incremental_load_orders()
RETURNS void AS $$
DECLARE
    last_timestamp TIMESTAMP;
BEGIN
    -- Get last processed timestamp
    SELECT last_processed_timestamp INTO last_timestamp
    FROM etl_control
    WHERE table_name = 'orders';
    
    -- If no previous run, start from beginning
    IF last_timestamp IS NULL THEN
        last_timestamp := '1900-01-01'::TIMESTAMP;
    END IF;
    
    -- Load new/updated records
    INSERT INTO orders_warehouse (order_id, customer_id, order_date, amount, loaded_at)
    SELECT 
        order_id, 
        customer_id, 
        order_date, 
        amount,
        CURRENT_TIMESTAMP
    FROM source_orders
    WHERE updated_at > last_timestamp
    ON CONFLICT (order_id) 
    DO UPDATE SET
        customer_id = EXCLUDED.customer_id,
        order_date = EXCLUDED.order_date,
        amount = EXCLUDED.amount,
        loaded_at = EXCLUDED.loaded_at;
    
    -- Update control table
    INSERT INTO etl_control (table_name, last_processed_timestamp)
    VALUES ('orders', CURRENT_TIMESTAMP)
    ON CONFLICT (table_name)
    DO UPDATE SET
        last_processed_timestamp = EXCLUDED.last_processed_timestamp,
        updated_at = CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql;
```

---

## 🔗 Quick Reference Links

- **PostgreSQL Documentation**: [postgresql.org/docs](https://www.postgresql.org/docs/)
- **MySQL Documentation**: [dev.mysql.com/doc](https://dev.mysql.com/doc/)
- **SQL Server Documentation**: [docs.microsoft.com/sql](https://docs.microsoft.com/en-us/sql/)
- **Oracle Documentation**: [docs.oracle.com/database](https://docs.oracle.com/en/database/)
- **SQL Standards**: [iso.org/standard/63555.html](https://www.iso.org/standard/63555.html)

---

**Key Takeaways:**
1. **Master the Fundamentals**: Joins, subqueries, window functions, and CTEs
2. **Optimize Performance**: Proper indexing, query tuning, and execution plans
3. **Ensure Data Quality**: Constraints, validation, and comprehensive testing
4. **Follow Best Practices**: Consistent formatting, meaningful names, and security
5. **Understand Advanced Features**: Window functions, recursive CTEs, and analytical queries
6. **Apply Data Engineering Patterns**: ETL/ELT, SCD, and incremental loading
7. **Monitor and Maintain**: Regular statistics updates, index maintenance, and performance monitoring