# SQL Key Concepts for Data Engineering

## 1. Data Definition Language (DDL)
**What it is**: Commands that define and modify database structure and schema.

**CREATE Statements**:
```sql
-- Create database
CREATE DATABASE data_warehouse;

-- Create table with constraints
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(200) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    registration_date DATE DEFAULT CURRENT_DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT chk_email CHECK (email LIKE '%@%'),
    CONSTRAINT chk_phone CHECK (LENGTH(phone) >= 10)
);

-- Create index for performance
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_reg_date ON customers(registration_date);

-- Create composite index
CREATE INDEX idx_customers_name_date ON customers(customer_name, registration_date);
```

**ALTER Statements**:
```sql
-- Add column
ALTER TABLE customers ADD COLUMN last_login TIMESTAMP;

-- Modify column
ALTER TABLE customers ALTER COLUMN phone TYPE VARCHAR(25);

-- Add constraint
ALTER TABLE customers ADD CONSTRAINT fk_customer_segment 
    FOREIGN KEY (segment_id) REFERENCES customer_segments(id);

-- Drop constraint
ALTER TABLE customers DROP CONSTRAINT chk_phone;
```

**DROP and TRUNCATE**:
```sql
-- Drop table (removes structure and data)
DROP TABLE IF EXISTS temp_customers;

-- Truncate table (removes data, keeps structure)
TRUNCATE TABLE staging_data;

-- Drop index
DROP INDEX idx_customers_phone;
```

## 2. Data Manipulation Language (DML)
**What it is**: Commands for inserting, updating, deleting, and querying data.

**INSERT Operations**:
```sql
-- Single row insert
INSERT INTO customers (customer_name, email, phone)
VALUES ('John Doe', 'john@example.com', '555-1234');

-- Multiple row insert
INSERT INTO customers (customer_name, email, phone) VALUES
    ('Alice Smith', 'alice@example.com', '555-2345'),
    ('Bob Johnson', 'bob@example.com', '555-3456'),
    ('Carol Brown', 'carol@example.com', '555-4567');

-- Insert from SELECT (ETL pattern)
INSERT INTO customer_summary (customer_id, total_orders, total_amount)
SELECT 
    customer_id,
    COUNT(*) as total_orders,
    SUM(order_amount) as total_amount
FROM orders
WHERE order_date >= '2024-01-01'
GROUP BY customer_id;

-- Insert with conflict handling (PostgreSQL)
INSERT INTO customers (customer_name, email, phone)
VALUES ('John Doe', 'john@example.com', '555-1234')
ON CONFLICT (email) 
DO UPDATE SET 
    customer_name = EXCLUDED.customer_name,
    phone = EXCLUDED.phone,
    updated_at = CURRENT_TIMESTAMP;
```

**UPDATE Operations**:
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

**DELETE Operations**:
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

-- Delete with JOIN (PostgreSQL)
DELETE FROM order_items oi
USING orders o
WHERE oi.order_id = o.order_id 
  AND o.status = 'cancelled';
```

## 3. Joins and Relationships
**What they are**: Operations to combine data from multiple tables based on relationships.

**INNER JOIN**:
```sql
-- Basic inner join
SELECT 
    c.customer_name,
    o.order_date,
    o.order_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;

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
INNER JOIN products p ON oi.product_id = p.product_id;
```

**OUTER JOINS**:
```sql
-- LEFT JOIN - all customers, even without orders
SELECT 
    c.customer_name,
    COUNT(o.order_id) as order_count,
    COALESCE(SUM(o.order_amount), 0) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name;

-- RIGHT JOIN - all orders, even if customer deleted
SELECT 
    COALESCE(c.customer_name, 'Unknown') as customer_name,
    o.order_date,
    o.order_amount
FROM customers c
RIGHT JOIN orders o ON c.customer_id = o.customer_id;

-- FULL OUTER JOIN - all records from both tables
SELECT 
    COALESCE(c.customer_name, 'No Customer') as customer_name,
    COALESCE(o.order_date, 'No Order') as order_date
FROM customers c
FULL OUTER JOIN orders o ON c.customer_id = o.customer_id;
```

**SELF JOIN**:
```sql
-- Find employees and their managers
SELECT 
    e.employee_name,
    m.employee_name as manager_name
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id;

-- Find customers in same city
SELECT 
    c1.customer_name as customer1,
    c2.customer_name as customer2,
    c1.city
FROM customers c1
INNER JOIN customers c2 ON c1.city = c2.city AND c1.customer_id < c2.customer_id;
```

## 4. Window Functions
**What they are**: Functions that perform calculations across related rows without collapsing the result set.

**Ranking Functions**:
```sql
SELECT 
    customer_name,
    order_date,
    order_amount,
    -- Ranking functions
    ROW_NUMBER() OVER (ORDER BY order_amount DESC) as row_num,
    RANK() OVER (ORDER BY order_amount DESC) as rank,
    DENSE_RANK() OVER (ORDER BY order_amount DESC) as dense_rank,
    PERCENT_RANK() OVER (ORDER BY order_amount DESC) as percent_rank
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;

-- Partition by category
SELECT 
    product_name,
    category,
    price,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC) as price_rank_in_category
FROM products;
```

**Aggregate Window Functions**:
```sql
SELECT 
    order_date,
    order_amount,
    -- Running totals
    SUM(order_amount) OVER (ORDER BY order_date) as running_total,
    
    -- Moving averages
    AVG(order_amount) OVER (
        ORDER BY order_date 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) as moving_avg_3day,
    
    -- Cumulative count
    COUNT(*) OVER (ORDER BY order_date) as cumulative_orders
FROM orders
ORDER BY order_date;
```

**Lead and Lag Functions**:
```sql
SELECT 
    order_date,
    order_amount,
    -- Previous and next values
    LAG(order_amount, 1) OVER (ORDER BY order_date) as prev_amount,
    LEAD(order_amount, 1) OVER (ORDER BY order_date) as next_amount,
    
    -- Calculate differences
    order_amount - LAG(order_amount, 1) OVER (ORDER BY order_date) as amount_change
FROM orders
ORDER BY order_date;
```

## 5. Common Table Expressions (CTEs)
**What they are**: Named temporary result sets that exist within the scope of a single statement.

**Basic CTE**:
```sql
-- Simple CTE for readability
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
```

**Multiple CTEs**:
```sql
WITH 
-- Customer metrics
customer_metrics AS (
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        SUM(order_amount) as total_spent,
        AVG(order_amount) as avg_order_value
    FROM orders
    GROUP BY customer_id
),
-- Customer segments
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
```

**Recursive CTE**:
```sql
-- Organizational hierarchy
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

## 6. Aggregation and Grouping
**What they are**: Functions and clauses for summarizing and grouping data.

**Basic Aggregation**:
```sql
SELECT 
    COUNT(*) as total_orders,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(order_amount) as total_revenue,
    AVG(order_amount) as average_order_value,
    MIN(order_date) as first_order,
    MAX(order_date) as last_order,
    STDDEV(order_amount) as amount_std_dev
FROM orders;
```

**GROUP BY with HAVING**:
```sql
-- Customer analysis
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
```

**Advanced Grouping**:
```sql
-- ROLLUP for subtotals
SELECT 
    COALESCE(region, 'All Regions') as region,
    COALESCE(category, 'All Categories') as category,
    SUM(sales_amount) as total_sales
FROM sales
GROUP BY ROLLUP(region, category)
ORDER BY region, category;

-- CUBE for all combinations
SELECT 
    COALESCE(region, 'All') as region,
    COALESCE(category, 'All') as category,
    COALESCE(quarter, 'All') as quarter,
    SUM(sales_amount) as total_sales
FROM sales
GROUP BY CUBE(region, category, quarter);

-- GROUPING SETS for specific combinations
SELECT 
    region,
    category,
    quarter,
    SUM(sales_amount) as total_sales
FROM sales
GROUP BY GROUPING SETS (
    (region),
    (category),
    (region, category),
    ()  -- Grand total
);
```

## 7. Subqueries and Correlated Queries
**What they are**: Queries nested within other queries for complex data retrieval.

**Scalar Subqueries**:
```sql
-- Single value subquery
SELECT 
    customer_name,
    total_orders,
    (SELECT AVG(order_count) FROM customer_summary) as avg_orders_all_customers,
    total_orders - (SELECT AVG(order_count) FROM customer_summary) as orders_vs_average
FROM customer_summary;
```

**EXISTS and NOT EXISTS**:
```sql
-- Customers with orders
SELECT customer_name
FROM customers c
WHERE EXISTS (
    SELECT 1 
    FROM orders o 
    WHERE o.customer_id = c.customer_id
);

-- Customers without orders
SELECT customer_name
FROM customers c
WHERE NOT EXISTS (
    SELECT 1 
    FROM orders o 
    WHERE o.customer_id = c.customer_id
);
```

**Correlated Subqueries**:
```sql
-- Customers with above-average spending
SELECT 
    customer_name,
    (SELECT SUM(order_amount) 
     FROM orders o 
     WHERE o.customer_id = c.customer_id) as total_spent
FROM customers c
WHERE (
    SELECT SUM(order_amount) 
    FROM orders o 
    WHERE o.customer_id = c.customer_id
) > (
    SELECT AVG(customer_total) 
    FROM (
        SELECT SUM(order_amount) as customer_total
        FROM orders
        GROUP BY customer_id
    ) avg_calc
);
```

## 8. Data Types and Functions
**What they are**: Built-in data types and functions for data manipulation.

**String Functions**:
```sql
SELECT 
    customer_name,
    -- String manipulation
    UPPER(customer_name) as name_upper,
    LOWER(customer_name) as name_lower,
    LENGTH(customer_name) as name_length,
    SUBSTRING(customer_name, 1, 3) as name_prefix,
    
    -- String cleaning
    TRIM(customer_name) as name_trimmed,
    REPLACE(phone, '-', '') as phone_clean,
    
    -- Pattern matching
    CASE 
        WHEN email LIKE '%@gmail.com' THEN 'Gmail'
        WHEN email LIKE '%@yahoo.com' THEN 'Yahoo'
        ELSE 'Other'
    END as email_provider
FROM customers;
```

**Date and Time Functions**:
```sql
SELECT 
    order_date,
    -- Date extraction
    EXTRACT(YEAR FROM order_date) as order_year,
    EXTRACT(MONTH FROM order_date) as order_month,
    EXTRACT(DOW FROM order_date) as day_of_week,
    
    -- Date formatting
    TO_CHAR(order_date, 'YYYY-MM') as year_month,
    TO_CHAR(order_date, 'Day') as day_name,
    
    -- Date arithmetic
    order_date + INTERVAL '30 days' as due_date,
    CURRENT_DATE - order_date as days_since_order,
    
    -- Age calculation
    AGE(CURRENT_DATE, order_date) as order_age
FROM orders;
```

**Numeric Functions**:
```sql
SELECT 
    order_amount,
    -- Rounding
    ROUND(order_amount, 2) as amount_rounded,
    CEIL(order_amount) as amount_ceiling,
    FLOOR(order_amount) as amount_floor,
    
    -- Mathematical operations
    ABS(order_amount - 100) as difference_from_100,
    POWER(order_amount, 2) as amount_squared,
    SQRT(order_amount) as amount_sqrt,
    
    -- Conditional logic
    COALESCE(discount_amount, 0) as discount_clean,
    NULLIF(order_amount, 0) as amount_no_zero,
    GREATEST(order_amount, 50) as minimum_50
FROM orders;
```

## 9. Performance Optimization
**What it is**: Techniques to improve query execution speed and efficiency.

**Index Strategies**:
```sql
-- Single column index
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- Composite index (order matters)
CREATE INDEX idx_orders_date_status ON orders(order_date, status);

-- Partial index
CREATE INDEX idx_active_customers ON customers(customer_id) 
WHERE is_active = TRUE;

-- Expression index
CREATE INDEX idx_customers_email_lower ON customers(LOWER(email));

-- Covering index (includes additional columns)
CREATE INDEX idx_orders_covering ON orders(customer_id, order_date) 
INCLUDE (order_amount, status);
```

**Query Optimization Techniques**:
```sql
-- Use EXISTS instead of IN for better performance
-- Slower
SELECT * FROM customers 
WHERE customer_id IN (SELECT customer_id FROM orders);

-- Faster
SELECT * FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);

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

## 10. Data Quality and Constraints
**What they are**: Mechanisms to ensure data integrity and quality.

**Constraint Types**:
```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    category_id INTEGER NOT NULL,
    sku VARCHAR(50) UNIQUE NOT NULL,
    created_date DATE DEFAULT CURRENT_DATE,
    
    -- Check constraints
    CONSTRAINT chk_price_positive CHECK (price > 0),
    CONSTRAINT chk_sku_format CHECK (sku ~ '^[A-Z]{3}-[0-9]{4}$'),
    
    -- Foreign key constraint
    CONSTRAINT fk_category FOREIGN KEY (category_id) 
        REFERENCES categories(category_id) ON DELETE RESTRICT
);
```

**Data Validation Queries**:
```sql
-- Find duplicate records
SELECT 
    email,
    COUNT(*) as duplicate_count
FROM customers
GROUP BY email
HAVING COUNT(*) > 1;

-- Check for null values
SELECT 
    'customer_name' as column_name,
    COUNT(*) as null_count,
    COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customers) as null_percentage
FROM customers
WHERE customer_name IS NULL

UNION ALL

SELECT 
    'email' as column_name,
    COUNT(*) as null_count,
    COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customers) as null_percentage
FROM customers
WHERE email IS NULL;

-- Data quality summary
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT customer_id) as unique_customers,
    COUNT(email) as non_null_emails,
    COUNT(DISTINCT email) as unique_emails,
    MIN(registration_date) as earliest_registration,
    MAX(registration_date) as latest_registration
FROM customers;
```