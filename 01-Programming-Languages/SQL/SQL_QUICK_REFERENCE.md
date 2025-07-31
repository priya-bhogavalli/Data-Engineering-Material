# SQL Quick Reference for Data Engineering

## Table of Contents
1. [Data Definition Language (DDL)](#data-definition-language-ddl)
2. [Data Manipulation Language (DML)](#data-manipulation-language-dml)
3. [Query Fundamentals](#query-fundamentals)
4. [Joins](#joins)
5. [Aggregate Functions](#aggregate-functions)
6. [Window Functions](#window-functions)
7. [Common Table Expressions (CTEs)](#common-table-expressions-ctes)
8. [Subqueries](#subqueries)
9. [String Functions](#string-functions)
10. [Date/Time Functions](#datetime-functions)
11. [Conditional Logic](#conditional-logic)
12. [Data Types](#data-types)
13. [Indexes](#indexes)
14. [Constraints](#constraints)
15. [Performance Optimization](#performance-optimization)

## Data Definition Language (DDL)

### CREATE TABLE
```sql
-- Basic table creation
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    hire_date DATE DEFAULT CURRENT_DATE,
    salary DECIMAL(10,2) CHECK (salary > 0),
    department_id INTEGER REFERENCES departments(id)
);

-- Table with multiple constraints
CREATE TABLE orders (
    order_id BIGSERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    total_amount DECIMAL(12,2) NOT NULL,
    
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customers(id),
    CONSTRAINT chk_status CHECK (status IN ('pending', 'confirmed', 'shipped', 'delivered')),
    CONSTRAINT chk_amount CHECK (total_amount >= 0)
);
```

### ALTER TABLE
```sql
-- Add column
ALTER TABLE employees ADD COLUMN phone VARCHAR(20);

-- Modify column
ALTER TABLE employees ALTER COLUMN salary TYPE DECIMAL(12,2);

-- Add constraint
ALTER TABLE employees ADD CONSTRAINT chk_email CHECK (email LIKE '%@%');

-- Drop column
ALTER TABLE employees DROP COLUMN phone;

-- Rename column
ALTER TABLE employees RENAME COLUMN first_name TO fname;
```

### CREATE INDEX
```sql
-- Single column index
CREATE INDEX idx_employees_last_name ON employees(last_name);

-- Composite index
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- Unique index
CREATE UNIQUE INDEX idx_employees_email ON employees(email);

-- Partial index
CREATE INDEX idx_active_employees ON employees(department_id) 
WHERE status = 'active';

-- Expression index
CREATE INDEX idx_employees_full_name ON employees(LOWER(first_name || ' ' || last_name));
```

## Data Manipulation Language (DML)

### INSERT
```sql
-- Single row insert
INSERT INTO employees (first_name, last_name, email, salary)
VALUES ('John', 'Doe', 'john@example.com', 50000);

-- Multiple row insert
INSERT INTO employees (first_name, last_name, email, salary) VALUES
    ('Jane', 'Smith', 'jane@example.com', 55000),
    ('Bob', 'Johnson', 'bob@example.com', 48000);

-- Insert from SELECT
INSERT INTO employee_backup
SELECT * FROM employees WHERE hire_date < '2020-01-01';

-- Insert with conflict handling (PostgreSQL)
INSERT INTO employees (email, first_name, last_name)
VALUES ('john@example.com', 'John', 'Doe')
ON CONFLICT (email) 
DO UPDATE SET 
    first_name = EXCLUDED.first_name,
    last_name = EXCLUDED.last_name;
```

### UPDATE
```sql
-- Simple update
UPDATE employees 
SET salary = 55000 
WHERE employee_id = 1;

-- Update with calculation
UPDATE employees 
SET salary = salary * 1.05 
WHERE department_id = 2;

-- Update with JOIN
UPDATE employees e
SET department_name = d.name
FROM departments d
WHERE e.department_id = d.id;

-- Conditional update
UPDATE orders
SET status = CASE 
    WHEN order_date < CURRENT_DATE - INTERVAL '30 days' THEN 'archived'
    WHEN payment_status = 'paid' THEN 'completed'
    ELSE status
END;
```

### DELETE
```sql
-- Simple delete
DELETE FROM employees WHERE status = 'inactive';

-- Delete with subquery
DELETE FROM orders 
WHERE customer_id IN (
    SELECT id FROM customers WHERE status = 'deleted'
);

-- Delete with JOIN (PostgreSQL)
DELETE FROM order_items oi
USING orders o
WHERE oi.order_id = o.order_id 
  AND o.status = 'cancelled';
```

## Query Fundamentals

### SELECT Basics
```sql
-- Basic SELECT
SELECT first_name, last_name, salary FROM employees;

-- SELECT with aliases
SELECT 
    first_name AS fname,
    last_name AS lname,
    salary * 12 AS annual_salary
FROM employees;

-- DISTINCT values
SELECT DISTINCT department_id FROM employees;

-- LIMIT and OFFSET
SELECT * FROM employees 
ORDER BY salary DESC 
LIMIT 10 OFFSET 20;
```

### WHERE Clause
```sql
-- Basic conditions
SELECT * FROM employees WHERE salary > 50000;

-- Multiple conditions
SELECT * FROM employees 
WHERE salary BETWEEN 40000 AND 60000 
  AND department_id IN (1, 2, 3);

-- Pattern matching
SELECT * FROM employees WHERE last_name LIKE 'Sm%';

-- NULL handling
SELECT * FROM employees WHERE phone IS NOT NULL;

-- Date conditions
SELECT * FROM orders 
WHERE order_date >= '2024-01-01' 
  AND order_date < '2024-02-01';
```

### ORDER BY
```sql
-- Single column
SELECT * FROM employees ORDER BY salary DESC;

-- Multiple columns
SELECT * FROM employees 
ORDER BY department_id ASC, salary DESC;

-- Order by expression
SELECT * FROM employees 
ORDER BY LENGTH(last_name), last_name;
```

## Joins

### INNER JOIN
```sql
SELECT 
    e.first_name,
    e.last_name,
    d.department_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.id;
```

### LEFT JOIN
```sql
SELECT 
    c.customer_name,
    COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name;
```

### RIGHT JOIN
```sql
SELECT 
    d.department_name,
    COUNT(e.employee_id) as employee_count
FROM employees e
RIGHT JOIN departments d ON e.department_id = d.id
GROUP BY d.id, d.department_name;
```

### FULL OUTER JOIN
```sql
SELECT 
    COALESCE(c.customer_name, 'No Customer') as customer,
    COALESCE(o.order_id, 'No Order') as order_info
FROM customers c
FULL OUTER JOIN orders o ON c.customer_id = o.customer_id;
```

### SELF JOIN
```sql
-- Employee and manager relationship
SELECT 
    e.first_name as employee,
    m.first_name as manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id;
```

### CROSS JOIN
```sql
-- Cartesian product
SELECT 
    p.product_name,
    c.category_name
FROM products p
CROSS JOIN categories c;
```

## Aggregate Functions

### Basic Aggregates
```sql
SELECT 
    COUNT(*) as total_employees,
    COUNT(DISTINCT department_id) as unique_departments,
    SUM(salary) as total_payroll,
    AVG(salary) as average_salary,
    MIN(hire_date) as earliest_hire,
    MAX(salary) as highest_salary,
    STDDEV(salary) as salary_std_dev
FROM employees;
```

### GROUP BY
```sql
SELECT 
    department_id,
    COUNT(*) as employee_count,
    AVG(salary) as avg_salary,
    MIN(salary) as min_salary,
    MAX(salary) as max_salary
FROM employees
GROUP BY department_id
ORDER BY avg_salary DESC;
```

### HAVING
```sql
SELECT 
    department_id,
    COUNT(*) as employee_count,
    AVG(salary) as avg_salary
FROM employees
GROUP BY department_id
HAVING COUNT(*) > 5 AND AVG(salary) > 50000;
```

### Advanced Grouping
```sql
-- ROLLUP for subtotals
SELECT 
    COALESCE(department, 'All Departments') as department,
    COALESCE(job_title, 'All Titles') as job_title,
    COUNT(*) as employee_count,
    SUM(salary) as total_salary
FROM employees
GROUP BY ROLLUP(department, job_title);

-- CUBE for all combinations
SELECT 
    department,
    job_title,
    location,
    COUNT(*) as employee_count
FROM employees
GROUP BY CUBE(department, job_title, location);
```

## Window Functions

### Ranking Functions
```sql
SELECT 
    employee_id,
    first_name,
    last_name,
    salary,
    department_id,
    ROW_NUMBER() OVER (ORDER BY salary DESC) as row_num,
    RANK() OVER (ORDER BY salary DESC) as rank,
    DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank,
    PERCENT_RANK() OVER (ORDER BY salary DESC) as percent_rank,
    NTILE(4) OVER (ORDER BY salary DESC) as quartile
FROM employees;
```

### Partition by Department
```sql
SELECT 
    employee_id,
    first_name,
    department_id,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) as dept_rank,
    AVG(salary) OVER (PARTITION BY department_id) as dept_avg_salary,
    salary - AVG(salary) OVER (PARTITION BY department_id) as salary_diff_from_avg
FROM employees;
```

### Running Totals and Moving Averages
```sql
SELECT 
    order_date,
    daily_sales,
    SUM(daily_sales) OVER (ORDER BY order_date) as running_total,
    AVG(daily_sales) OVER (
        ORDER BY order_date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as moving_avg_7_days,
    LAG(daily_sales, 1) OVER (ORDER BY order_date) as prev_day_sales,
    LEAD(daily_sales, 1) OVER (ORDER BY order_date) as next_day_sales
FROM daily_sales_summary;
```

### First/Last Value
```sql
SELECT 
    employee_id,
    hire_date,
    salary,
    FIRST_VALUE(salary) OVER (ORDER BY hire_date) as first_hire_salary,
    LAST_VALUE(salary) OVER (
        ORDER BY hire_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as last_hire_salary
FROM employees;
```

## Common Table Expressions (CTEs)

### Basic CTE
```sql
WITH high_earners AS (
    SELECT employee_id, first_name, last_name, salary
    FROM employees
    WHERE salary > 75000
)
SELECT 
    he.first_name,
    he.last_name,
    he.salary,
    d.department_name
FROM high_earners he
JOIN departments d ON he.department_id = d.id;
```

### Multiple CTEs
```sql
WITH 
department_stats AS (
    SELECT 
        department_id,
        COUNT(*) as emp_count,
        AVG(salary) as avg_salary
    FROM employees
    GROUP BY department_id
),
high_performing_depts AS (
    SELECT department_id
    FROM department_stats
    WHERE emp_count > 10 AND avg_salary > 60000
)
SELECT 
    e.first_name,
    e.last_name,
    e.salary,
    ds.avg_salary as dept_avg
FROM employees e
JOIN department_stats ds ON e.department_id = ds.department_id
JOIN high_performing_depts hpd ON e.department_id = hpd.department_id;
```

### Recursive CTE
```sql
WITH RECURSIVE employee_hierarchy AS (
    -- Base case: top-level managers
    SELECT 
        employee_id,
        first_name,
        last_name,
        manager_id,
        1 as level,
        first_name || ' ' || last_name as path
    FROM employees 
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive case
    SELECT 
        e.employee_id,
        e.first_name,
        e.last_name,
        e.manager_id,
        eh.level + 1,
        eh.path || ' -> ' || e.first_name || ' ' || e.last_name
    FROM employees e
    INNER JOIN employee_hierarchy eh ON e.manager_id = eh.employee_id
)
SELECT * FROM employee_hierarchy ORDER BY level, path;
```

## Subqueries

### Scalar Subquery
```sql
SELECT 
    employee_id,
    first_name,
    salary,
    (SELECT AVG(salary) FROM employees) as company_avg_salary,
    salary - (SELECT AVG(salary) FROM employees) as diff_from_avg
FROM employees;
```

### EXISTS
```sql
-- Employees with dependents
SELECT first_name, last_name
FROM employees e
WHERE EXISTS (
    SELECT 1 
    FROM dependents d 
    WHERE d.employee_id = e.employee_id
);
```

### IN Subquery
```sql
-- Employees in high-performing departments
SELECT first_name, last_name, department_id
FROM employees
WHERE department_id IN (
    SELECT department_id
    FROM departments
    WHERE performance_rating > 4.0
);
```

### Correlated Subquery
```sql
-- Employees earning above department average
SELECT 
    first_name,
    last_name,
    salary,
    department_id
FROM employees e1
WHERE salary > (
    SELECT AVG(salary)
    FROM employees e2
    WHERE e2.department_id = e1.department_id
);
```

## String Functions

### Basic String Operations
```sql
SELECT 
    first_name,
    last_name,
    -- Concatenation
    first_name || ' ' || last_name as full_name,
    CONCAT(first_name, ' ', last_name) as full_name_concat,
    
    -- Case conversion
    UPPER(first_name) as first_name_upper,
    LOWER(last_name) as last_name_lower,
    INITCAP(first_name || ' ' || last_name) as proper_case,
    
    -- Length and substring
    LENGTH(first_name) as first_name_length,
    SUBSTRING(first_name, 1, 3) as first_three_chars,
    LEFT(first_name, 2) as first_two_chars,
    RIGHT(last_name, 3) as last_three_chars
FROM employees;
```

### String Cleaning and Formatting
```sql
SELECT 
    email,
    phone,
    -- Trimming
    TRIM(first_name) as trimmed_name,
    LTRIM(first_name) as left_trimmed,
    RTRIM(first_name) as right_trimmed,
    
    -- Replace and translate
    REPLACE(phone, '-', '') as phone_no_dashes,
    TRANSLATE(phone, '()-', '') as phone_clean,
    
    -- Padding
    LPAD(employee_id::TEXT, 6, '0') as padded_id,
    RPAD(first_name, 15, '.') as padded_name
FROM employees;
```

### Pattern Matching
```sql
-- LIKE patterns
SELECT * FROM employees WHERE last_name LIKE 'Sm%';
SELECT * FROM employees WHERE first_name LIKE '_ohn';
SELECT * FROM employees WHERE email LIKE '%@gmail.com';

-- ILIKE (case-insensitive)
SELECT * FROM employees WHERE first_name ILIKE 'john';

-- Regular expressions (PostgreSQL)
SELECT * FROM employees WHERE email ~ '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$';
SELECT * FROM employees WHERE phone ~ '^\d{3}-\d{3}-\d{4}$';
```

### String Aggregation
```sql
-- String aggregation (PostgreSQL)
SELECT 
    department_id,
    STRING_AGG(first_name || ' ' || last_name, ', ' ORDER BY last_name) as employee_list
FROM employees
GROUP BY department_id;

-- Array aggregation
SELECT 
    department_id,
    ARRAY_AGG(first_name ORDER BY first_name) as first_names
FROM employees
GROUP BY department_id;
```

## Date/Time Functions

### Current Date/Time
```sql
SELECT 
    CURRENT_DATE as today,
    CURRENT_TIME as current_time,
    CURRENT_TIMESTAMP as now,
    NOW() as now_function,
    EXTRACT(EPOCH FROM NOW()) as unix_timestamp;
```

### Date Arithmetic
```sql
SELECT 
    hire_date,
    hire_date + INTERVAL '1 year' as one_year_later,
    hire_date - INTERVAL '30 days' as thirty_days_before,
    CURRENT_DATE - hire_date as days_since_hire,
    AGE(CURRENT_DATE, hire_date) as time_since_hire
FROM employees;
```

### Date Extraction
```sql
SELECT 
    hire_date,
    EXTRACT(YEAR FROM hire_date) as hire_year,
    EXTRACT(MONTH FROM hire_date) as hire_month,
    EXTRACT(DAY FROM hire_date) as hire_day,
    EXTRACT(DOW FROM hire_date) as day_of_week, -- 0=Sunday
    EXTRACT(DOY FROM hire_date) as day_of_year,
    EXTRACT(WEEK FROM hire_date) as week_number,
    EXTRACT(QUARTER FROM hire_date) as quarter
FROM employees;
```

### Date Formatting
```sql
SELECT 
    hire_date,
    TO_CHAR(hire_date, 'YYYY-MM-DD') as iso_date,
    TO_CHAR(hire_date, 'Month DD, YYYY') as formatted_date,
    TO_CHAR(hire_date, 'Day') as day_name,
    TO_CHAR(hire_date, 'Mon') as month_abbrev,
    TO_CHAR(hire_date, 'YYYY-Q') as year_quarter
FROM employees;
```

### Date Truncation
```sql
SELECT 
    order_date,
    DATE_TRUNC('day', order_date) as day_start,
    DATE_TRUNC('week', order_date) as week_start,
    DATE_TRUNC('month', order_date) as month_start,
    DATE_TRUNC('quarter', order_date) as quarter_start,
    DATE_TRUNC('year', order_date) as year_start
FROM orders;
```

## Conditional Logic

### CASE Statements
```sql
SELECT 
    employee_id,
    first_name,
    salary,
    CASE 
        WHEN salary > 80000 THEN 'High'
        WHEN salary > 50000 THEN 'Medium'
        ELSE 'Low'
    END as salary_category,
    
    CASE department_id
        WHEN 1 THEN 'Engineering'
        WHEN 2 THEN 'Sales'
        WHEN 3 THEN 'Marketing'
        ELSE 'Other'
    END as department_name
FROM employees;
```

### COALESCE and NULLIF
```sql
SELECT 
    first_name,
    last_name,
    phone,
    email,
    -- Handle NULL values
    COALESCE(phone, email, 'No contact info') as contact,
    COALESCE(middle_name, '') as middle_name_clean,
    
    -- Convert empty strings to NULL
    NULLIF(phone, '') as phone_clean,
    NULLIF(TRIM(middle_name), '') as middle_name_null_if_empty
FROM employees;
```

### GREATEST and LEAST
```sql
SELECT 
    employee_id,
    salary,
    bonus,
    commission,
    GREATEST(salary, bonus, commission) as highest_compensation,
    LEAST(salary, bonus, commission) as lowest_compensation
FROM employees;
```

## Data Types

### Numeric Types
```sql
-- Integer types
SMALLINT    -- -32,768 to 32,767
INTEGER     -- -2,147,483,648 to 2,147,483,647
BIGINT      -- -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807

-- Auto-incrementing
SERIAL      -- Auto-incrementing integer
BIGSERIAL   -- Auto-incrementing bigint

-- Decimal types
DECIMAL(10,2)   -- Exact decimal with 10 digits, 2 after decimal
NUMERIC(10,2)   -- Same as DECIMAL
REAL            -- Single precision floating point
DOUBLE PRECISION -- Double precision floating point
```

### Character Types
```sql
-- Character types
CHAR(10)        -- Fixed length, padded with spaces
VARCHAR(100)    -- Variable length with limit
TEXT            -- Variable length without limit

-- Example usage
CREATE TABLE example (
    id SERIAL PRIMARY KEY,
    code CHAR(5),           -- Always 5 characters
    name VARCHAR(100),      -- Up to 100 characters
    description TEXT        -- Unlimited length
);
```

### Date/Time Types
```sql
-- Date and time types
DATE            -- Date only (YYYY-MM-DD)
TIME            -- Time only (HH:MM:SS)
TIMESTAMP       -- Date and time
TIMESTAMPTZ     -- Date and time with timezone
INTERVAL        -- Time interval

-- Example usage
CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    event_date DATE,
    start_time TIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duration INTERVAL
);
```

### Boolean and Other Types
```sql
-- Boolean
BOOLEAN         -- TRUE, FALSE, or NULL

-- JSON types (PostgreSQL)
JSON            -- JSON data, stored as text
JSONB           -- Binary JSON, more efficient

-- Array types (PostgreSQL)
INTEGER[]       -- Array of integers
TEXT[]          -- Array of text values

-- UUID type
UUID            -- Universally unique identifier
```

## Indexes

### Index Types
```sql
-- B-tree index (default)
CREATE INDEX idx_employees_last_name ON employees(last_name);

-- Hash index (equality only)
CREATE INDEX idx_employees_id_hash ON employees USING HASH(employee_id);

-- GIN index (for arrays, JSON, full-text search)
CREATE INDEX idx_products_tags ON products USING GIN(tags);

-- GiST index (for geometric data, full-text search)
CREATE INDEX idx_locations_point ON locations USING GIST(coordinates);
```

### Index Strategies
```sql
-- Composite index (order matters)
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- Covering index (includes additional columns)
CREATE INDEX idx_employees_dept_salary 
ON employees(department_id) 
INCLUDE (salary, hire_date);

-- Partial index (with WHERE condition)
CREATE INDEX idx_active_employees 
ON employees(last_name) 
WHERE status = 'active';

-- Expression index
CREATE INDEX idx_employees_full_name 
ON employees(LOWER(first_name || ' ' || last_name));

-- Unique index
CREATE UNIQUE INDEX idx_employees_email ON employees(email);
```

## Constraints

### Primary Key
```sql
-- Single column primary key
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Composite primary key
CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    PRIMARY KEY (order_id, product_id)
);
```

### Foreign Key
```sql
-- Basic foreign key
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    department_id INTEGER REFERENCES departments(id)
);

-- Foreign key with actions
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    department_id INTEGER,
    CONSTRAINT fk_department 
        FOREIGN KEY (department_id) 
        REFERENCES departments(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
```

### Check Constraints
```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2),
    category VARCHAR(50),
    
    -- Simple check
    CONSTRAINT chk_price_positive CHECK (price > 0),
    
    -- Complex check
    CONSTRAINT chk_category CHECK (category IN ('Electronics', 'Clothing', 'Books')),
    
    -- Multi-column check
    CONSTRAINT chk_discount CHECK (
        (discount_percent IS NULL) OR 
        (discount_percent >= 0 AND discount_percent <= 100)
    )
);
```

### Unique Constraints
```sql
-- Single column unique
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE,
    username VARCHAR(50) UNIQUE
);

-- Multi-column unique
CREATE TABLE user_preferences (
    user_id INTEGER,
    preference_key VARCHAR(50),
    preference_value TEXT,
    UNIQUE(user_id, preference_key)
);
```

## Performance Optimization

### Query Optimization Tips
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
SELECT * FROM products 
ORDER BY created_date DESC 
LIMIT 100;
```

### Index Usage
```sql
-- Check index usage
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM employees WHERE last_name = 'Smith';

-- Force index usage (hint-based, varies by database)
SELECT /*+ INDEX(employees, idx_employees_last_name) */ 
* FROM employees WHERE last_name = 'Smith';
```

### Table Partitioning
```sql
-- Range partitioning by date
CREATE TABLE sales (
    sale_id BIGSERIAL,
    sale_date DATE NOT NULL,
    amount DECIMAL(10,2),
    customer_id INTEGER
) PARTITION BY RANGE (sale_date);

-- Create partitions
CREATE TABLE sales_2024_q1 PARTITION OF sales
FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE sales_2024_q2 PARTITION OF sales
FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- Hash partitioning
CREATE TABLE user_data (
    user_id BIGINT,
    data JSONB
) PARTITION BY HASH (user_id);

CREATE TABLE user_data_0 PARTITION OF user_data
FOR VALUES WITH (MODULUS 4, REMAINDER 0);
```

### Materialized Views
```sql
-- Create materialized view
CREATE MATERIALIZED VIEW monthly_sales_summary AS
SELECT 
    DATE_TRUNC('month', sale_date) as month,
    COUNT(*) as total_sales,
    SUM(amount) as total_revenue,
    AVG(amount) as avg_sale_amount
FROM sales
GROUP BY DATE_TRUNC('month', sale_date);

-- Refresh materialized view
REFRESH MATERIALIZED VIEW monthly_sales_summary;

-- Concurrent refresh (PostgreSQL)
REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_sales_summary;
```

### Query Analysis
```sql
-- Analyze query performance
EXPLAIN SELECT * FROM employees WHERE department_id = 1;

-- Detailed analysis with execution stats
EXPLAIN (ANALYZE, BUFFERS, VERBOSE) 
SELECT e.first_name, d.department_name
FROM employees e
JOIN departments d ON e.department_id = d.id
WHERE e.salary > 50000;

-- Update table statistics
ANALYZE employees;
ANALYZE;  -- Analyze all tables
```