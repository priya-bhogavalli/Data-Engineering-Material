# SQL Quick Reference for Data Engineering

## 📋 Table of Contents

1. [Essential Queries](#-essential-queries)
2. [Join Patterns](#-join-patterns)
3. [Aggregation Functions](#-aggregation-functions)
4. [Window Functions](#-window-functions)
5. [Date/Time Operations](#-datetime-operations)
6. [String Functions](#-string-functions)
7. [Data Modification](#-data-modification)
8. [Performance Tips](#-performance-tips)
9. [Common Patterns](#-common-patterns)

---

## ⚡ Essential Queries

### Basic SELECT Operations
```sql
-- Select specific columns
SELECT customer_id, customer_name, email FROM customers;

-- Select with conditions
SELECT * FROM orders WHERE order_date >= '2024-01-01';

-- Select with multiple conditions
SELECT * FROM products 
WHERE price > 100 AND category = 'Electronics';

-- Select with sorting
SELECT * FROM employees ORDER BY salary DESC, hire_date ASC;

-- Select with limit
SELECT * FROM customers ORDER BY created_at DESC LIMIT 10;

-- Select distinct values
SELECT DISTINCT department FROM employees;

-- Select with calculated columns
SELECT 
    product_name,
    price,
    price * 0.9 as discounted_price,
    CASE 
        WHEN price > 1000 THEN 'Expensive'
        WHEN price > 100 THEN 'Moderate'
        ELSE 'Cheap'
    END as price_category
FROM products;
```

### Filtering Patterns
```sql
-- Range filtering
SELECT * FROM orders 
WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31';

-- List filtering
SELECT * FROM customers 
WHERE country IN ('USA', 'Canada', 'Mexico');

-- Pattern matching
SELECT * FROM customers WHERE email LIKE '%@gmail.com';
SELECT * FROM products WHERE name ILIKE '%laptop%';  -- Case insensitive

-- NULL handling
SELECT * FROM customers WHERE phone IS NOT NULL;
SELECT * FROM orders WHERE notes IS NULL;

-- Exists filtering
SELECT * FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id
);
```

## 🔗 Join Patterns

### Basic Joins
```sql
-- Inner join
SELECT c.customer_name, o.order_date, o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;

-- Left join (all customers, even without orders)
SELECT c.customer_name, COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name;

-- Right join
SELECT c.customer_name, o.order_date
FROM customers c
RIGHT JOIN orders o ON c.customer_id = o.customer_id;

-- Full outer join
SELECT c.customer_name, o.order_date
FROM customers c
FULL OUTER JOIN orders o ON c.customer_id = o.customer_id;
```

### Advanced Join Patterns
```sql
-- Multiple joins
SELECT 
    c.customer_name,
    o.order_date,
    p.product_name,
    oi.quantity,
    oi.price
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id;

-- Self join (employees and managers)
SELECT 
    e.employee_name,
    m.employee_name as manager_name
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id;

-- Cross join (cartesian product)
SELECT s.size, c.color
FROM sizes s
CROSS JOIN colors c;
```

## 📊 Aggregation Functions

### Basic Aggregations
```sql
-- Count records
SELECT COUNT(*) as total_customers FROM customers;
SELECT COUNT(DISTINCT country) as unique_countries FROM customers;

-- Sum and average
SELECT 
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as average_order_value,
    MIN(total_amount) as smallest_order,
    MAX(total_amount) as largest_order
FROM orders;

-- Group by with aggregations
SELECT 
    country,
    COUNT(*) as customer_count,
    AVG(age) as average_age
FROM customers
GROUP BY country
ORDER BY customer_count DESC;

-- Having clause (filter groups)
SELECT 
    category,
    COUNT(*) as product_count,
    AVG(price) as avg_price
FROM products
GROUP BY category
HAVING COUNT(*) > 5 AND AVG(price) > 100;
```

### Advanced Aggregations
```sql
-- Multiple grouping levels
SELECT 
    EXTRACT(YEAR FROM order_date) as year,
    EXTRACT(MONTH FROM order_date) as month,
    COUNT(*) as order_count,
    SUM(total_amount) as monthly_revenue
FROM orders
GROUP BY EXTRACT(YEAR FROM order_date), EXTRACT(MONTH FROM order_date)
ORDER BY year, month;

-- Conditional aggregation
SELECT 
    customer_id,
    COUNT(*) as total_orders,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_orders,
    COUNT(CASE WHEN status = 'cancelled' THEN 1 END) as cancelled_orders,
    SUM(CASE WHEN status = 'completed' THEN total_amount ELSE 0 END) as completed_revenue
FROM orders
GROUP BY customer_id;
```

## 🪟 Window Functions

### Ranking Functions
```sql
-- Row number, rank, dense rank
SELECT 
    employee_name,
    department,
    salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) as row_num,
    RANK() OVER (ORDER BY salary DESC) as rank,
    DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank
FROM employees;

-- Ranking within partitions
SELECT 
    employee_name,
    department,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank
FROM employees;

-- Percentile functions
SELECT 
    employee_name,
    salary,
    NTILE(4) OVER (ORDER BY salary) as salary_quartile,
    PERCENT_RANK() OVER (ORDER BY salary) as salary_percentile
FROM employees;
```

### Analytical Functions
```sql
-- Running totals and moving averages
SELECT 
    order_date,
    total_amount,
    SUM(total_amount) OVER (ORDER BY order_date) as running_total,
    AVG(total_amount) OVER (ORDER BY order_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7day
FROM orders
ORDER BY order_date;

-- Lead and lag functions
SELECT 
    order_date,
    total_amount,
    LAG(total_amount, 1) OVER (ORDER BY order_date) as previous_amount,
    LEAD(total_amount, 1) OVER (ORDER BY order_date) as next_amount,
    total_amount - LAG(total_amount, 1) OVER (ORDER BY order_date) as amount_change
FROM orders
ORDER BY order_date;

-- First and last values
SELECT 
    customer_id,
    order_date,
    total_amount,
    FIRST_VALUE(total_amount) OVER (PARTITION BY customer_id ORDER BY order_date) as first_order_amount,
    LAST_VALUE(total_amount) OVER (PARTITION BY customer_id ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as last_order_amount
FROM orders;
```

## 📅 Date/Time Operations

### Date Functions
```sql
-- Current date and time
SELECT 
    CURRENT_DATE as today,
    CURRENT_TIME as now_time,
    CURRENT_TIMESTAMP as now_timestamp,
    NOW() as now_function;

-- Date arithmetic
SELECT 
    order_date,
    order_date + INTERVAL '30 days' as due_date,
    order_date - INTERVAL '1 week' as week_ago,
    AGE(CURRENT_DATE, order_date) as order_age
FROM orders;

-- Extract date parts
SELECT 
    order_date,
    EXTRACT(YEAR FROM order_date) as year,
    EXTRACT(MONTH FROM order_date) as month,
    EXTRACT(DAY FROM order_date) as day,
    EXTRACT(DOW FROM order_date) as day_of_week,  -- 0=Sunday
    EXTRACT(DOY FROM order_date) as day_of_year
FROM orders;

-- Date truncation
SELECT 
    order_date,
    DATE_TRUNC('month', order_date) as month_start,
    DATE_TRUNC('week', order_date) as week_start,
    DATE_TRUNC('day', order_date) as day_start
FROM orders;
```

### Date Formatting
```sql
-- Format dates
SELECT 
    order_date,
    TO_CHAR(order_date, 'YYYY-MM-DD') as iso_date,
    TO_CHAR(order_date, 'Mon DD, YYYY') as formatted_date,
    TO_CHAR(order_date, 'Day, Month DD, YYYY') as full_date
FROM orders;

-- Parse dates from strings
SELECT 
    TO_DATE('2024-01-15', 'YYYY-MM-DD') as parsed_date,
    TO_TIMESTAMP('2024-01-15 14:30:00', 'YYYY-MM-DD HH24:MI:SS') as parsed_timestamp;
```

## 🔤 String Functions

### Basic String Operations
```sql
-- String manipulation
SELECT 
    customer_name,
    UPPER(customer_name) as uppercase,
    LOWER(customer_name) as lowercase,
    INITCAP(customer_name) as title_case,
    LENGTH(customer_name) as name_length,
    TRIM(customer_name) as trimmed
FROM customers;

-- String concatenation
SELECT 
    first_name,
    last_name,
    first_name || ' ' || last_name as full_name,
    CONCAT(first_name, ' ', last_name) as full_name_concat
FROM customers;

-- Substring operations
SELECT 
    email,
    SUBSTRING(email FROM 1 FOR POSITION('@' IN email) - 1) as username,
    SUBSTRING(email FROM POSITION('@' IN email) + 1) as domain,
    LEFT(email, 3) as first_three,
    RIGHT(email, 3) as last_three
FROM customers;
```

### Pattern Matching and Replacement
```sql
-- String replacement
SELECT 
    phone,
    REPLACE(phone, '-', '') as phone_no_dashes,
    REGEXP_REPLACE(phone, '[^0-9]', '', 'g') as digits_only
FROM customers;

-- Pattern matching
SELECT * FROM customers 
WHERE email ~ '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$';  -- Email regex

-- String splitting
SELECT 
    full_address,
    SPLIT_PART(full_address, ',', 1) as street,
    SPLIT_PART(full_address, ',', 2) as city,
    SPLIT_PART(full_address, ',', 3) as state
FROM addresses;
```

## ✏️ Data Modification

### INSERT Operations
```sql
-- Single row insert
INSERT INTO customers (customer_name, email, country)
VALUES ('John Doe', 'john@example.com', 'USA');

-- Multiple row insert
INSERT INTO products (product_name, category, price) VALUES
('Laptop Pro', 'Electronics', 1299.99),
('Wireless Mouse', 'Electronics', 29.99),
('Office Chair', 'Furniture', 199.99);

-- Insert from select
INSERT INTO customer_backup (customer_id, customer_name, email)
SELECT customer_id, customer_name, email
FROM customers
WHERE created_at >= '2024-01-01';

-- Insert with conflict handling (PostgreSQL)
INSERT INTO products (product_id, product_name, price)
VALUES (1, 'Updated Product', 99.99)
ON CONFLICT (product_id) 
DO UPDATE SET 
    product_name = EXCLUDED.product_name,
    price = EXCLUDED.price,
    updated_at = CURRENT_TIMESTAMP;
```

### UPDATE Operations
```sql
-- Simple update
UPDATE customers 
SET email = 'newemail@example.com'
WHERE customer_id = 123;

-- Update with calculations
UPDATE products 
SET price = price * 1.1,
    updated_at = CURRENT_TIMESTAMP
WHERE category = 'Electronics';

-- Update with joins
UPDATE orders 
SET status = 'shipped'
FROM customers c
WHERE orders.customer_id = c.customer_id
  AND c.country = 'USA'
  AND orders.status = 'processing';

-- Conditional update
UPDATE employees
SET salary = CASE 
    WHEN performance_rating >= 4.5 THEN salary * 1.15
    WHEN performance_rating >= 3.5 THEN salary * 1.10
    WHEN performance_rating >= 2.5 THEN salary * 1.05
    ELSE salary
END,
bonus = CASE 
    WHEN performance_rating >= 4.0 THEN salary * 0.1
    ELSE 0
END;
```

### DELETE Operations
```sql
-- Simple delete
DELETE FROM customers WHERE last_login < '2023-01-01';

-- Delete with joins
DELETE o FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE c.status = 'inactive';

-- Delete with subquery
DELETE FROM products 
WHERE product_id IN (
    SELECT product_id FROM order_items 
    GROUP BY product_id 
    HAVING COUNT(*) = 0
);
```

## 🚀 Performance Tips

### Query Optimization
```sql
-- Use indexes effectively
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
CREATE INDEX idx_products_category_price ON products(category, price);

-- Use EXISTS instead of IN for large subqueries
-- ✅ Preferred
SELECT * FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);

-- ❌ Slower for large datasets
SELECT * FROM customers c
WHERE c.customer_id IN (SELECT customer_id FROM orders);

-- Use LIMIT for large result sets
SELECT * FROM orders 
ORDER BY order_date DESC 
LIMIT 100;

-- Use appropriate data types
-- ✅ Good
CREATE TABLE optimized (
    id INT,
    status CHAR(1),
    amount DECIMAL(10,2)
);

-- ❌ Wasteful
CREATE TABLE wasteful (
    id BIGINT,
    status VARCHAR(255),
    amount FLOAT
);
```

### Common Anti-Patterns to Avoid
```sql
-- ❌ Avoid SELECT *
SELECT * FROM large_table;  -- Bad

-- ✅ Select only needed columns
SELECT customer_id, customer_name FROM customers;  -- Good

-- ❌ Avoid functions in WHERE clause
SELECT * FROM orders WHERE YEAR(order_date) = 2024;  -- Bad

-- ✅ Use range conditions
SELECT * FROM orders WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01';  -- Good

-- ❌ Avoid OR conditions on different columns
SELECT * FROM products WHERE category = 'Electronics' OR price > 1000;  -- Bad

-- ✅ Use UNION for better performance
SELECT * FROM products WHERE category = 'Electronics'
UNION
SELECT * FROM products WHERE price > 1000;  -- Good
```

## 🎯 Common Patterns

### Data Analysis Patterns
```sql
-- Top N analysis
SELECT customer_id, customer_name, total_spent
FROM (
    SELECT 
        c.customer_id,
        c.customer_name,
        SUM(o.total_amount) as total_spent,
        RANK() OVER (ORDER BY SUM(o.total_amount) DESC) as spending_rank
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name
) ranked
WHERE spending_rank <= 10;

-- Cohort analysis
SELECT 
    DATE_TRUNC('month', first_order_date) as cohort_month,
    DATE_TRUNC('month', order_date) as order_month,
    COUNT(DISTINCT customer_id) as customers
FROM (
    SELECT 
        customer_id,
        order_date,
        MIN(order_date) OVER (PARTITION BY customer_id) as first_order_date
    FROM orders
) cohort_data
GROUP BY cohort_month, order_month
ORDER BY cohort_month, order_month;

-- Running calculations
SELECT 
    order_date,
    daily_revenue,
    SUM(daily_revenue) OVER (ORDER BY order_date) as cumulative_revenue,
    AVG(daily_revenue) OVER (ORDER BY order_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7day
FROM (
    SELECT 
        order_date,
        SUM(total_amount) as daily_revenue
    FROM orders
    GROUP BY order_date
) daily_totals
ORDER BY order_date;
```

### Data Quality Checks
```sql
-- Find duplicates
SELECT email, COUNT(*) as duplicate_count
FROM customers
GROUP BY email
HAVING COUNT(*) > 1;

-- Find missing relationships
SELECT c.customer_id, c.customer_name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.customer_id IS NULL;

-- Data validation
SELECT 
    'Invalid Email' as issue,
    COUNT(*) as count
FROM customers 
WHERE email NOT LIKE '%@%.%'
UNION ALL
SELECT 
    'Negative Price' as issue,
    COUNT(*) as count
FROM products 
WHERE price < 0
UNION ALL
SELECT 
    'Future Order Date' as issue,
    COUNT(*) as count
FROM orders 
WHERE order_date > CURRENT_DATE;
```

## 🔗 Quick Links

- **[SQL Key Concepts](./SQL_KEY_CONCEPTS.md)** - Complete fundamentals
- **[SQL Advanced Database Engineering](./SQL_ADVANCED_DATABASE_ENGINEERING.md)** - Production patterns
- **[SQL Interview Questions](./SQL_INTERVIEW_QUESTIONS.md)** - Interview preparation

This quick reference covers the most commonly used SQL patterns and operations for daily data engineering tasks.