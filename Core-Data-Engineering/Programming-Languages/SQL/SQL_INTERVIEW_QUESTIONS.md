# SQL Interview Questions for Data Engineering

## 📋 Table of Contents

1. [Basic Level Questions (1-15)](#basic-level-questions-1-15)
2. [Intermediate Level Questions (16-35)](#intermediate-level-questions-16-35)
3. [Advanced Level Questions (36-50)](#advanced-level-questions-36-50)
4. [Database Design & Architecture (51-65)](#database-design--architecture-51-65)
5. [Performance & Optimization (66-80)](#performance--optimization-66-80)
6. [Data Engineering Scenarios (81-100)](#data-engineering-scenarios-81-100)
7. [Theoretical & Conceptual Questions (101-120)](#theoretical--conceptual-questions-101-120)

---

## Basic Level Questions (1-15)

### 1. What's the difference between INNER JOIN and LEFT JOIN?
**Answer:**
- **INNER JOIN**: Returns only matching records from both tables
- **LEFT JOIN**: Returns all records from left table + matching records from right table

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

### 2. Explain the difference between WHERE and HAVING clauses
**Answer:**
- **WHERE**: Filters rows before grouping
- **HAVING**: Filters groups after GROUP BY

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

### 3. What are the different types of SQL constraints?
**Answer:**
- **PRIMARY KEY**: Unique identifier for each row
- **FOREIGN KEY**: Links to primary key in another table
- **UNIQUE**: Ensures column values are unique
- **NOT NULL**: Prevents null values
- **CHECK**: Validates data based on condition
- **DEFAULT**: Sets default value

```sql
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    salary DECIMAL(10,2) CHECK (salary > 0),
    department_id INT REFERENCES departments(id),
    hire_date DATE DEFAULT CURRENT_DATE
);
```

### 4. Explain ACID properties in databases
**Answer:**
- **Atomicity**: All operations in transaction succeed or fail together
- **Consistency**: Database remains in valid state after transaction
- **Isolation**: Concurrent transactions don't interfere with each other
- **Durability**: Committed changes persist even after system failure

### 5. What's the difference between DELETE, TRUNCATE, and DROP?
**Answer:**
```sql
-- DELETE: Removes specific rows, can be rolled back, triggers fire
DELETE FROM employees WHERE department = 'Sales';

-- TRUNCATE: Removes all rows, faster, can't be rolled back, no triggers
TRUNCATE TABLE temp_data;

-- DROP: Removes entire table structure and data
DROP TABLE old_table;
```

### 6. Explain different types of indexes
**Answer:**
```sql
-- Clustered Index (Primary Key)
CREATE TABLE orders (
    order_id INT PRIMARY KEY  -- Clustered index
);

-- Non-clustered Index
CREATE INDEX idx_customer ON orders(customer_id);

-- Composite Index
CREATE INDEX idx_customer_date ON orders(customer_id, order_date);

-- Unique Index
CREATE UNIQUE INDEX idx_email ON customers(email);

-- Partial Index
CREATE INDEX idx_active_orders ON orders(order_date) 
WHERE status = 'ACTIVE';
```

### 7. What are aggregate functions? Give examples
**Answer:**
```sql
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(order_amount) as total_revenue,
    AVG(order_amount) as average_order,
    MIN(order_date) as first_order,
    MAX(order_date) as last_order,
    STDDEV(order_amount) as amount_std_dev
FROM orders;
```

### 8. What are the different types of SQL commands?
**Answer:**
- **DDL (Data Definition Language)**: CREATE, ALTER, DROP, TRUNCATE
- **DML (Data Manipulation Language)**: INSERT, UPDATE, DELETE, SELECT
- **DCL (Data Control Language)**: GRANT, REVOKE
- **TCL (Transaction Control Language)**: COMMIT, ROLLBACK, SAVEPOINT

### 9. Explain the SQL execution order
**Answer:**
Logical execution order:
1. **FROM** - Identify tables
2. **WHERE** - Filter rows
3. **GROUP BY** - Group rows
4. **HAVING** - Filter groups
5. **SELECT** - Choose columns
6. **ORDER BY** - Sort results
7. **LIMIT** - Limit results

### 10. What is the difference between CHAR and VARCHAR?
**Answer:**
- **CHAR(n)**: Fixed-length, pads with spaces, faster for fixed-size data
- **VARCHAR(n)**: Variable-length, no padding, more storage efficient

```sql
-- CHAR always uses full length
CREATE TABLE test_char (code CHAR(5));
INSERT INTO test_char VALUES ('ABC');  -- Stored as 'ABC  '

-- VARCHAR uses only needed space
CREATE TABLE test_varchar (name VARCHAR(50));
INSERT INTO test_varchar VALUES ('John');  -- Stored as 'John'
```

### 11. Explain NULL values and how to handle them
**Answer:**
```sql
-- NULL comparisons
SELECT * FROM employees WHERE salary IS NULL;
SELECT * FROM employees WHERE salary IS NOT NULL;

-- NULL in calculations
SELECT 
    name,
    salary,
    bonus,
    salary + COALESCE(bonus, 0) as total_compensation,
    CASE WHEN bonus IS NULL THEN 'No bonus' ELSE 'Has bonus' END as bonus_status
FROM employees;

-- NULL with aggregate functions
SELECT 
    COUNT(*) as total_rows,
    COUNT(bonus) as non_null_bonus,
    AVG(bonus) as avg_bonus  -- Ignores NULLs
FROM employees;
```

### 12. What are SQL data types and their categories?
**Answer:**
**Numeric Types:**
- INTEGER, BIGINT, DECIMAL, FLOAT, DOUBLE

**String Types:**
- CHAR, VARCHAR, TEXT, CLOB

**Date/Time Types:**
- DATE, TIME, TIMESTAMP, DATETIME

**Boolean:**
- BOOLEAN (TRUE/FALSE/NULL)

**Binary:**
- BINARY, VARBINARY, BLOB

### 13. Explain the concept of database transactions
**Answer:**
```sql
-- Transaction example
BEGIN TRANSACTION;

    UPDATE accounts SET balance = balance - 1000 WHERE account_id = 1;
    UPDATE accounts SET balance = balance + 1000 WHERE account_id = 2;
    
    -- Check if both updates were successful
    IF @@ERROR = 0
        COMMIT TRANSACTION;
    ELSE
        ROLLBACK TRANSACTION;
```

### 14. What is the difference between RANK() and DENSE_RANK()?
**Answer:**
```sql
SELECT 
    name,
    salary,
    RANK() OVER (ORDER BY salary DESC) as rank_with_gaps,
    DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank,
    ROW_NUMBER() OVER (ORDER BY salary DESC) as row_num
FROM employees;

-- Example output:
-- Name    Salary  Rank  Dense_Rank  Row_Num
-- Alice   100000    1       1         1
-- Bob     100000    1       1         2  
-- Carol    90000    3       2         3
-- Dave     80000    4       3         4
```

### 15. How do you handle case-sensitive searches?
**Answer:**
```sql
-- Case-sensitive search (depends on collation)
SELECT * FROM customers WHERE name = 'John';  -- May or may not match 'john'

-- Force case-sensitive
SELECT * FROM customers WHERE BINARY name = 'John';

-- Case-insensitive search
SELECT * FROM customers WHERE UPPER(name) = UPPER('john');
SELECT * FROM customers WHERE LOWER(name) = 'john';

-- Using LIKE with case handling
SELECT * FROM customers WHERE name ILIKE '%john%';  -- PostgreSQL
SELECT * FROM customers WHERE UPPER(name) LIKE '%JOHN%';  -- Universal
```

## Intermediate Level Questions (16-35)

### 16. What are window functions and how do they differ from aggregate functions?
**Answer:**
Window functions perform calculations across related rows without collapsing the result set.

```sql
-- Aggregate function - collapses to one row per group
SELECT department, AVG(salary)
FROM employees
GROUP BY department;

-- Window function - keeps all rows
SELECT 
    name,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department) as dept_avg_salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as salary_rank
FROM employees;
```

### 17. How would you find the second highest salary in each department?
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

### 18. Write a query to calculate running totals
**Answer:**
```sql
-- Running total of sales by date
SELECT 
    sale_date,
    daily_sales,
    SUM(daily_sales) OVER (ORDER BY sale_date) as running_total
FROM (
    SELECT 
        sale_date,
        SUM(amount) as daily_sales
    FROM sales
    GROUP BY sale_date
) daily_summary
ORDER BY sale_date;

-- Running total with reset by category
SELECT 
    category,
    sale_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY category 
        ORDER BY sale_date 
        ROWS UNBOUNDED PRECEDING
    ) as category_running_total
FROM sales
ORDER BY category, sale_date;
```

### 19. How do you handle duplicate records in a table?
**Answer:**
```sql
-- Method 1: Using ROW_NUMBER() to identify duplicates
WITH duplicates AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY email, phone 
               ORDER BY created_date DESC
           ) as rn
    FROM customers
)
-- Keep most recent record
SELECT * FROM duplicates WHERE rn = 1;

-- Method 2: Remove duplicates using DELETE
DELETE FROM customers
WHERE id NOT IN (
    SELECT MIN(id)
    FROM customers
    GROUP BY email, phone
);

-- Method 3: Create clean table
CREATE TABLE customers_clean AS
SELECT DISTINCT ON (email, phone) *
FROM customers
ORDER BY email, phone, created_date DESC;
```

### 20. Explain Common Table Expressions (CTEs) with examples
**Answer:**
```sql
-- Simple CTE
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
        SUM(order_amount) as total_spent
    FROM orders
    GROUP BY customer_id
),
customer_segments AS (
    SELECT 
        customer_id,
        CASE 
            WHEN total_spent > 10000 THEN 'Premium'
            WHEN total_spent > 5000 THEN 'Gold'
            ELSE 'Silver'
        END as segment
    FROM customer_metrics
)
SELECT 
    c.customer_name,
    cm.order_count,
    cs.segment
FROM customers c
JOIN customer_metrics cm ON c.customer_id = cm.customer_id
JOIN customer_segments cs ON c.customer_id = cs.customer_id;
```

### 21. What's the difference between UNION and UNION ALL?
**Answer:**
```sql
-- UNION removes duplicates (slower)
SELECT customer_id, 'Premium' as segment FROM premium_customers
UNION
SELECT customer_id, 'Regular' as segment FROM regular_customers;

-- UNION ALL keeps duplicates (faster)
SELECT customer_id, 'Premium' as segment FROM premium_customers
UNION ALL
SELECT customer_id, 'Regular' as segment FROM regular_customers;
```

### 22. How do you optimize a slow-running query?
**Answer:**
1. **Analyze execution plan**
2. **Add appropriate indexes**
3. **Rewrite query logic**
4. **Use LIMIT for large result sets**

```sql
-- Before optimization
SELECT c.name, COUNT(o.order_id)
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.registration_date >= '2023-01-01'
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) > 5;

-- After optimization
-- 1. Add indexes
CREATE INDEX idx_customers_reg_date ON customers(registration_date);
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- 2. Rewrite query
WITH active_customers AS (
    SELECT customer_id, name
    FROM customers
    WHERE registration_date >= '2023-01-01'
),
customer_order_counts AS (
    SELECT 
        ac.customer_id,
        ac.name,
        COUNT(o.order_id) as order_count
    FROM active_customers ac
    LEFT JOIN orders o ON ac.customer_id = o.customer_id
    GROUP BY ac.customer_id, ac.name
)
SELECT customer_id, name, order_count
FROM customer_order_counts
WHERE order_count > 5;
```

### 23. Explain different types of subqueries
**Answer:**
```sql
-- Scalar subquery (returns single value)
SELECT 
    customer_name,
    total_orders,
    (SELECT AVG(order_count) FROM customer_summary) as avg_orders
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

### 24. What are stored procedures and functions? How do they differ?
**Answer:**
```sql
-- Stored Procedure (performs actions, can have multiple result sets)
CREATE PROCEDURE GetCustomerOrders(
    IN customer_id INT,
    OUT total_orders INT,
    OUT total_amount DECIMAL(10,2)
)
BEGIN
    SELECT COUNT(*), SUM(order_amount)
    INTO total_orders, total_amount
    FROM orders
    WHERE customer_id = customer_id;
    
    SELECT * FROM orders WHERE customer_id = customer_id;
END;

-- Function (returns single value)
CREATE FUNCTION CalculateDiscount(order_amount DECIMAL(10,2))
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE discount DECIMAL(10,2);
    
    IF order_amount > 1000 THEN
        SET discount = order_amount * 0.10;
    ELSEIF order_amount > 500 THEN
        SET discount = order_amount * 0.05;
    ELSE
        SET discount = 0;
    END IF;
    
    RETURN discount;
END;
```

### 25. Explain database triggers and their types
**Answer:**
```sql
-- BEFORE INSERT trigger for data validation
CREATE TRIGGER validate_employee_salary
BEFORE INSERT ON employees
FOR EACH ROW
BEGIN
    IF NEW.salary < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Salary cannot be negative';
    END IF;
    
    IF NEW.email NOT LIKE '%@%' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid email format';
    END IF;
END;

-- AFTER UPDATE trigger for audit logging
CREATE TRIGGER audit_salary_changes
AFTER UPDATE ON employees
FOR EACH ROW
BEGIN
    IF OLD.salary != NEW.salary THEN
        INSERT INTO salary_audit_log (
            employee_id, old_salary, new_salary, 
            changed_by, changed_at
        ) VALUES (
            NEW.employee_id, OLD.salary, NEW.salary,
            USER(), NOW()
        );
    END IF;
END;
```

### 26. How do you handle hierarchical data in SQL?
**Answer:**
```sql
-- Adjacency List Model
CREATE TABLE categories (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    parent_id INT REFERENCES categories(id)
);

-- Find all descendants using recursive CTE
WITH RECURSIVE category_tree AS (
    SELECT id, name, parent_id, 0 as level
    FROM categories
    WHERE parent_id IS NULL
    
    UNION ALL
    
    SELECT c.id, c.name, c.parent_id, ct.level + 1
    FROM categories c
    JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree ORDER BY level, name;

-- Nested Set Model (alternative approach)
CREATE TABLE categories_nested (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    lft INT,
    rgt INT
);

-- Find all descendants in nested set
SELECT child.*
FROM categories_nested parent
JOIN categories_nested child ON child.lft BETWEEN parent.lft AND parent.rgt
WHERE parent.name = 'Electronics';
```

### 27. What are materialized views and when would you use them?
**Answer:**
```sql
-- Create materialized view for expensive aggregations
CREATE MATERIALIZED VIEW monthly_sales_summary AS
SELECT 
    DATE_TRUNC('month', order_date) as month,
    product_category,
    COUNT(*) as order_count,
    SUM(order_amount) as total_sales,
    AVG(order_amount) as avg_order_value
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY DATE_TRUNC('month', order_date), product_category;

-- Refresh materialized view
REFRESH MATERIALIZED VIEW monthly_sales_summary;

-- Use cases:
-- 1. Complex aggregations that take long to compute
-- 2. Data that doesn't change frequently
-- 3. Reporting and analytics queries
-- 4. Improving query performance for dashboards
```

### 28. Explain different types of table relationships
**Answer:**
```sql
-- One-to-One (1:1)
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50)
);

CREATE TABLE user_profiles (
    user_id INT PRIMARY KEY REFERENCES users(user_id),
    first_name VARCHAR(50),
    last_name VARCHAR(50)
);

-- One-to-Many (1:N)
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date DATE
);

-- Many-to-Many (M:N)
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(100)
);

CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(100)
);

CREATE TABLE enrollments (
    student_id INT REFERENCES students(student_id),
    course_id INT REFERENCES courses(course_id),
    enrollment_date DATE,
    PRIMARY KEY (student_id, course_id)
);
```

### 29. How do you implement pagination in SQL?
**Answer:**
```sql
-- Method 1: OFFSET and LIMIT (can be slow for large offsets)
SELECT *
FROM products
ORDER BY product_id
LIMIT 20 OFFSET 100;  -- Page 6 (20 records per page)

-- Method 2: Cursor-based pagination (more efficient)
SELECT *
FROM products
WHERE product_id > 100  -- Last ID from previous page
ORDER BY product_id
LIMIT 20;

-- Method 3: Window functions for pagination info
WITH paginated_products AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (ORDER BY product_id) as row_num,
        COUNT(*) OVER () as total_count
    FROM products
    WHERE category = 'Electronics'
)
SELECT 
    *,
    CEIL(total_count / 20.0) as total_pages,
    CEIL(row_num / 20.0) as current_page
FROM paginated_products
WHERE row_num BETWEEN 21 AND 40;  -- Page 2
```

### 30. What is the difference between clustered and non-clustered indexes?
**Answer:**
**Clustered Index:**
- Physical ordering of data matches index order
- One per table (usually primary key)
- Data pages stored in order of index key
- Faster for range queries

**Non-clustered Index:**
- Logical ordering, separate from physical storage
- Multiple allowed per table
- Contains pointers to data rows
- Faster for specific lookups

```sql
-- Clustered index (implicit with PRIMARY KEY)
CREATE TABLE orders (
    order_id INT PRIMARY KEY,  -- Clustered index
    customer_id INT,
    order_date DATE
);

-- Non-clustered indexes
CREATE INDEX idx_customer ON orders(customer_id);
CREATE INDEX idx_date ON orders(order_date);
CREATE INDEX idx_customer_date ON orders(customer_id, order_date);
```

### 31. How do you handle time zones in SQL?
**Answer:**
```sql
-- Store timestamps in UTC
CREATE TABLE events (
    event_id INT PRIMARY KEY,
    event_name VARCHAR(100),
    event_time TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'UTC')
);

-- Convert time zones in queries
SELECT 
    event_name,
    event_time,
    event_time AT TIME ZONE 'America/New_York' as ny_time,
    event_time AT TIME ZONE 'Europe/London' as london_time,
    event_time AT TIME ZONE 'Asia/Tokyo' as tokyo_time
FROM events;

-- Filter by local time
SELECT *
FROM events
WHERE (event_time AT TIME ZONE 'America/New_York')::DATE = '2024-01-15';
```

### 32. Explain SQL injection and how to prevent it
**Answer:**
```sql
-- Vulnerable code (DON'T DO THIS)
-- query = "SELECT * FROM users WHERE username = '" + username + "'"

-- Safe approaches:

-- 1. Parameterized queries/Prepared statements
PREPARE user_lookup AS
SELECT * FROM users WHERE username = $1 AND password = $2;

EXECUTE user_lookup('john_doe', 'hashed_password');

-- 2. Input validation and sanitization
-- Validate input length, format, allowed characters

-- 3. Stored procedures with parameters
CREATE PROCEDURE GetUser(
    IN p_username VARCHAR(50),
    IN p_password VARCHAR(255)
)
BEGIN
    SELECT * FROM users 
    WHERE username = p_username AND password = p_password;
END;

-- 4. Escape special characters
-- Use database-specific escaping functions
```

### 33. How do you implement soft deletes in SQL?
**Answer:**
```sql
-- Add deleted_at column
ALTER TABLE customers 
ADD COLUMN deleted_at TIMESTAMP NULL,
ADD COLUMN deleted_by INT NULL;

-- Soft delete (update instead of delete)
UPDATE customers 
SET deleted_at = NOW(), deleted_by = 123
WHERE customer_id = 456;

-- Query active records only
SELECT * FROM customers WHERE deleted_at IS NULL;

-- Create view for active records
CREATE VIEW active_customers AS
SELECT * FROM customers WHERE deleted_at IS NULL;

-- Restore soft-deleted record
UPDATE customers 
SET deleted_at = NULL, deleted_by = NULL
WHERE customer_id = 456;

-- Hard delete old soft-deleted records
DELETE FROM customers 
WHERE deleted_at < NOW() - INTERVAL '1 year';
```

### 34. What are database locks and isolation levels?
**Answer:**
```sql
-- Lock types:
-- Shared Lock (S): Multiple readers, no writers
-- Exclusive Lock (X): Single writer, no readers
-- Update Lock (U): Prevents deadlocks during updates

-- Isolation levels:
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;  -- Dirty reads possible
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;    -- Default in most DBs
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;   -- Consistent reads
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;      -- Strictest, slowest

-- Example of lock usage
BEGIN TRANSACTION;
    SELECT * FROM accounts WHERE account_id = 123 FOR UPDATE;  -- Exclusive lock
    UPDATE accounts SET balance = balance - 100 WHERE account_id = 123;
COMMIT;

-- Deadlock prevention
BEGIN TRANSACTION;
    -- Always acquire locks in same order
    SELECT * FROM accounts WHERE account_id = 123 FOR UPDATE;
    SELECT * FROM accounts WHERE account_id = 456 FOR UPDATE;
    
    UPDATE accounts SET balance = balance - 100 WHERE account_id = 123;
    UPDATE accounts SET balance = balance + 100 WHERE account_id = 456;
COMMIT;
```

### 35. How do you implement database auditing?
**Answer:**
```sql
-- Create audit table
CREATE TABLE audit_log (
    audit_id SERIAL PRIMARY KEY,
    table_name VARCHAR(50),
    operation VARCHAR(10),  -- INSERT, UPDATE, DELETE
    record_id INT,
    old_values JSONB,
    new_values JSONB,
    changed_by VARCHAR(50),
    changed_at TIMESTAMP DEFAULT NOW()
);

-- Audit trigger function (PostgreSQL)
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, operation, record_id, new_values, changed_by)
        VALUES (TG_TABLE_NAME, 'INSERT', NEW.id, row_to_json(NEW), current_user);
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, operation, record_id, old_values, new_values, changed_by)
        VALUES (TG_TABLE_NAME, 'UPDATE', NEW.id, row_to_json(OLD), row_to_json(NEW), current_user);
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (table_name, operation, record_id, old_values, changed_by)
        VALUES (TG_TABLE_NAME, 'DELETE', OLD.id, row_to_json(OLD), current_user);
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Apply audit trigger to tables
CREATE TRIGGER customers_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON customers
FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();
```

## Advanced Level Questions (36-50)

### 36. Write a query to find gaps in sequential data
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

### 37. Implement a pivot table in SQL
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

-- Using PIVOT (SQL Server/Oracle syntax)
SELECT *
FROM (
    SELECT product_name, quarter, sales_amount
    FROM quarterly_sales
) src
PIVOT (
    SUM(sales_amount)
    FOR quarter IN ([Q1], [Q2], [Q3], [Q4])
) pvt;
```

### 38. Write a recursive CTE to handle hierarchical data
**Answer:**
```sql
-- Employee hierarchy with levels
WITH RECURSIVE employee_hierarchy AS (
    -- Base case: top-level managers
    SELECT 
        employee_id,
        name,
        manager_id,
        1 as level,
        CAST(name AS VARCHAR(1000)) as hierarchy_path
    FROM employees 
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive case: employees with managers
    SELECT 
        e.employee_id,
        e.name,
        e.manager_id,
        eh.level + 1,
        CONCAT(eh.hierarchy_path, ' -> ', e.name)
    FROM employees e
    INNER JOIN employee_hierarchy eh ON e.manager_id = eh.employee_id
)
SELECT 
    employee_id,
    name,
    level,
    hierarchy_path,
    REPEAT('  ', level - 1) || name as indented_name
FROM employee_hierarchy
ORDER BY hierarchy_path;
```

### 39. Design a query for slowly changing dimensions (SCD Type 2)
**Answer:**
```sql
-- SCD Type 2 implementation for customer dimension
MERGE customer_dim AS target
USING (
    SELECT 
        customer_id,
        name,
        address,
        phone,
        CURRENT_DATE as effective_date
    FROM customer_staging
) AS source
ON target.customer_id = source.customer_id 
   AND target.is_current = 'Y'

-- When customer exists and data changed
WHEN MATCHED AND (
    target.name != source.name OR 
    target.address != source.address OR 
    target.phone != source.phone
) THEN
    UPDATE SET 
        is_current = 'N',
        end_date = CURRENT_DATE - 1

-- When customer doesn't exist
WHEN NOT MATCHED THEN
    INSERT (
        customer_id, name, address, phone,
        effective_date, end_date, is_current, version
    )
    VALUES (
        source.customer_id, source.name, source.address, source.phone,
        source.effective_date, '9999-12-31', 'Y', 1
    );
```

### 40. How would you implement data quality checks in SQL?
**Answer:**
```sql
-- Comprehensive data quality check
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

### 41. Write a query to calculate customer lifetime value (CLV)
**Answer:**
```sql
WITH customer_metrics AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        c.registration_date,
        COUNT(DISTINCT o.order_id) as total_orders,
        SUM(o.order_amount) as total_spent,
        AVG(o.order_amount) as avg_order_value,
        MIN(o.order_date) as first_order_date,
        MAX(o.order_date) as last_order_date,
        -- Calculate customer lifespan in days
        EXTRACT(DAYS FROM (MAX(o.order_date) - MIN(o.order_date))) + 1 as lifespan_days
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.order_id IS NOT NULL
    GROUP BY c.customer_id, c.customer_name, c.registration_date
),
customer_clv AS (
    SELECT 
        customer_id,
        customer_name,
        total_orders,
        total_spent,
        avg_order_value,
        lifespan_days,
        -- Calculate purchase frequency (orders per day)
        CASE 
            WHEN lifespan_days > 0 THEN total_orders::DECIMAL / lifespan_days
            ELSE 0
        END as purchase_frequency,
        -- Calculate CLV using simple formula: AOV * Purchase Frequency * Lifespan
        CASE 
            WHEN lifespan_days > 0 THEN 
                avg_order_value * (total_orders::DECIMAL / lifespan_days) * lifespan_days
            ELSE total_spent
        END as customer_lifetime_value
    FROM customer_metrics
)
SELECT 
    customer_name,
    total_orders,
    total_spent,
    ROUND(avg_order_value, 2) as avg_order_value,
    lifespan_days,
    ROUND(purchase_frequency, 4) as purchase_frequency,
    ROUND(customer_lifetime_value, 2) as clv,
    -- Segment customers based on CLV
    CASE 
        WHEN customer_lifetime_value > 10000 THEN 'High Value'
        WHEN customer_lifetime_value > 5000 THEN 'Medium Value'
        WHEN customer_lifetime_value > 1000 THEN 'Low Value'
        ELSE 'Very Low Value'
    END as clv_segment
FROM customer_clv
ORDER BY customer_lifetime_value DESC;
```

### 42. How do you handle JSON data in SQL?
**Answer:**
```sql
-- PostgreSQL JSON operations
CREATE TABLE user_profiles (
    user_id SERIAL PRIMARY KEY,
    profile_data JSONB
);

-- Insert JSON data
INSERT INTO user_profiles (profile_data) VALUES 
('{"name": "John", "age": 30, "skills": ["SQL", "Python"], "address": {"city": "NYC", "zip": "10001"}}');

-- Query JSON fields
SELECT 
    user_id,
    profile_data->>'name' as name,
    (profile_data->>'age')::int as age,
    profile_data->'address'->>'city' as city
FROM user_profiles;

-- Query JSON arrays
SELECT user_id, skill
FROM user_profiles,
     jsonb_array_elements_text(profile_data->'skills') as skill;

-- Update JSON data
UPDATE user_profiles 
SET profile_data = profile_data || '{"last_login": "2024-01-15"}'
WHERE user_id = 1;

-- Index on JSON fields
CREATE INDEX idx_profile_name ON user_profiles USING GIN ((profile_data->>'name'));
```

### 43. How do you implement data versioning in SQL?
**Answer:**
```sql
-- Temporal table approach
CREATE TABLE products (
    product_id INT,
    name VARCHAR(255),
    price DECIMAL(10,2),
    version_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    version_end TIMESTAMP DEFAULT '9999-12-31 23:59:59',
    is_current BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (product_id, version_start)
);

-- Insert new version
CREATE OR REPLACE FUNCTION update_product_version(
    p_product_id INT,
    p_name VARCHAR(255),
    p_price DECIMAL(10,2)
)
RETURNS void AS $$
BEGIN
    -- End current version
    UPDATE products 
    SET version_end = CURRENT_TIMESTAMP, is_current = FALSE
    WHERE product_id = p_product_id AND is_current = TRUE;
    
    -- Insert new version
    INSERT INTO products (product_id, name, price)
    VALUES (p_product_id, p_name, p_price);
END;
$$ LANGUAGE plpgsql;

-- Query current version
SELECT * FROM products WHERE is_current = TRUE;

-- Query version at specific time
SELECT * FROM products 
WHERE product_id = 1 
  AND '2024-01-01' BETWEEN version_start AND version_end;
```

### 44. How do you handle large-scale data aggregations?
**Answer:**
```sql
-- Incremental aggregation approach
CREATE TABLE daily_sales_summary (
    summary_date DATE PRIMARY KEY,
    total_orders INT,
    total_revenue DECIMAL(15,2),
    avg_order_value DECIMAL(10,2),
    unique_customers INT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Incremental update function
CREATE OR REPLACE FUNCTION update_daily_summary(target_date DATE)
RETURNS void AS $$
BEGIN
    INSERT INTO daily_sales_summary (
        summary_date, total_orders, total_revenue, 
        avg_order_value, unique_customers
    )
    SELECT 
        target_date,
        COUNT(*) as total_orders,
        SUM(order_amount) as total_revenue,
        AVG(order_amount) as avg_order_value,
        COUNT(DISTINCT customer_id) as unique_customers
    FROM orders 
    WHERE DATE(order_date) = target_date
    ON CONFLICT (summary_date) 
    DO UPDATE SET
        total_orders = EXCLUDED.total_orders,
        total_revenue = EXCLUDED.total_revenue,
        avg_order_value = EXCLUDED.avg_order_value,
        unique_customers = EXCLUDED.unique_customers,
        last_updated = CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql;

-- Parallel processing for large datasets
WITH monthly_partitions AS (
    SELECT generate_series(
        DATE_TRUNC('month', '2023-01-01'::date),
        DATE_TRUNC('month', '2023-12-31'::date),
        INTERVAL '1 month'
    ) as month_start
)
SELECT 
    month_start,
    COUNT(*) as orders_count,
    SUM(order_amount) as total_revenue
FROM monthly_partitions mp
JOIN orders o ON DATE_TRUNC('month', o.order_date) = mp.month_start
GROUP BY month_start
ORDER BY month_start;
```

### 45. How do you implement database connection pooling concepts in SQL?
**Answer:**
```sql
-- Connection monitoring and management
CREATE TABLE connection_pool_stats (
    pool_name VARCHAR(50),
    active_connections INT,
    idle_connections INT,
    max_connections INT,
    wait_count INT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Monitor active connections
SELECT 
    datname as database,
    usename as username,
    client_addr,
    state,
    COUNT(*) as connection_count
FROM pg_stat_activity 
WHERE state IS NOT NULL
GROUP BY datname, usename, client_addr, state;

-- Long-running query detection
SELECT 
    pid,
    usename,
    datname,
    query_start,
    NOW() - query_start as duration,
    state,
    LEFT(query, 100) as query_preview
FROM pg_stat_activity 
WHERE state = 'active'
  AND NOW() - query_start > INTERVAL '5 minutes'
ORDER BY duration DESC;

-- Kill long-running queries (use with caution)
-- SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid = <pid>;
```

### 46. How do you implement data lineage tracking in SQL?
**Answer:**
```sql
-- Data lineage metadata tables
CREATE TABLE data_sources (
    source_id SERIAL PRIMARY KEY,
    source_name VARCHAR(255),
    source_type VARCHAR(50), -- 'table', 'view', 'file', 'api'
    connection_string TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE data_transformations (
    transformation_id SERIAL PRIMARY KEY,
    transformation_name VARCHAR(255),
    transformation_sql TEXT,
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE data_lineage (
    lineage_id SERIAL PRIMARY KEY,
    source_id INT REFERENCES data_sources(source_id),
    target_id INT REFERENCES data_sources(source_id),
    transformation_id INT REFERENCES data_transformations(transformation_id),
    dependency_type VARCHAR(50), -- 'direct', 'indirect', 'derived'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Track lineage for a transformation
INSERT INTO data_lineage (source_id, target_id, transformation_id, dependency_type)
VALUES 
(1, 3, 1, 'direct'),  -- customers -> customer_summary
(2, 3, 1, 'direct');  -- orders -> customer_summary

-- Query upstream dependencies
WITH RECURSIVE lineage_upstream AS (
    -- Base case: direct dependencies
    SELECT 
        dl.source_id,
        ds.source_name,
        1 as level
    FROM data_lineage dl
    JOIN data_sources ds ON dl.source_id = ds.source_id
    WHERE dl.target_id = 3  -- customer_summary table
    
    UNION ALL
    
    -- Recursive case: indirect dependencies
    SELECT 
        dl.source_id,
        ds.source_name,
        lu.level + 1
    FROM data_lineage dl
    JOIN data_sources ds ON dl.source_id = ds.source_id
    JOIN lineage_upstream lu ON dl.target_id = lu.source_id
    WHERE lu.level < 5  -- Prevent infinite recursion
)
SELECT DISTINCT source_name, level
FROM lineage_upstream
ORDER BY level, source_name;
```

### 47. How do you implement data masking for sensitive information?
**Answer:**
```sql
-- Data masking functions
CREATE OR REPLACE FUNCTION mask_email(email TEXT)
RETURNS TEXT AS $$
BEGIN
    IF email IS NULL OR email = '' THEN
        RETURN email;
    END IF;
    
    RETURN CONCAT(
        LEFT(email, 2),
        REPEAT('*', LENGTH(SPLIT_PART(email, '@', 1)) - 2),
        '@',
        REPEAT('*', LENGTH(SPLIT_PART(email, '@', 2)) - 4),
        RIGHT(SPLIT_PART(email, '@', 2), 4)
    );
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION mask_phone(phone TEXT)
RETURNS TEXT AS $$
BEGIN
    IF phone IS NULL OR LENGTH(phone) < 4 THEN
        RETURN phone;
    END IF;
    
    RETURN CONCAT(
        REPEAT('X', LENGTH(phone) - 4),
        RIGHT(phone, 4)
    );
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION mask_credit_card(card_number TEXT)
RETURNS TEXT AS $$
BEGIN
    IF card_number IS NULL OR LENGTH(card_number) < 4 THEN
        RETURN card_number;
    END IF;
    
    RETURN CONCAT(
        REPEAT('*', LENGTH(card_number) - 4),
        RIGHT(card_number, 4)
    );
END;
$$ LANGUAGE plpgsql;

-- Create masked view for non-production environments
CREATE VIEW customers_masked AS
SELECT 
    customer_id,
    CASE 
        WHEN current_setting('app.environment') = 'production' THEN name
        ELSE 'Customer_' || customer_id
    END as name,
    mask_email(email) as email,
    mask_phone(phone) as phone,
    -- Keep non-sensitive data as-is
    city,
    state,
    registration_date
FROM customers;

-- Dynamic data masking based on user role
CREATE OR REPLACE FUNCTION get_customer_data(p_customer_id INT)
RETURNS TABLE(
    customer_id INT,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20)
) AS $$
BEGIN
    IF current_user IN ('admin', 'data_engineer') THEN
        -- Return unmasked data for privileged users
        RETURN QUERY
        SELECT c.customer_id, c.name, c.email, c.phone
        FROM customers c
        WHERE c.customer_id = p_customer_id;
    ELSE
        -- Return masked data for regular users
        RETURN QUERY
        SELECT 
            c.customer_id,
            'Customer_' || c.customer_id as name,
            mask_email(c.email) as email,
            mask_phone(c.phone) as phone
        FROM customers c
        WHERE c.customer_id = p_customer_id;
    END IF;
END;
$$ LANGUAGE plpgsql;
```

### 48. How do you implement database monitoring and alerting?
**Answer:**
```sql
-- Database health monitoring tables
CREATE TABLE db_health_metrics (
    metric_id SERIAL PRIMARY KEY,
    metric_name VARCHAR(100),
    metric_value DECIMAL(15,2),
    threshold_warning DECIMAL(15,2),
    threshold_critical DECIMAL(15,2),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE db_alerts (
    alert_id SERIAL PRIMARY KEY,
    alert_type VARCHAR(50),
    severity VARCHAR(20) CHECK (severity IN ('info', 'warning', 'critical')),
    message TEXT,
    is_resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

-- Function to collect database metrics
CREATE OR REPLACE FUNCTION collect_db_metrics()
RETURNS void AS $$
DECLARE
    db_size BIGINT;
    active_connections INT;
    slow_queries INT;
    table_bloat DECIMAL(5,2);
BEGIN
    -- Database size
    SELECT pg_database_size(current_database()) INTO db_size;
    INSERT INTO db_health_metrics (metric_name, metric_value, threshold_warning, threshold_critical)
    VALUES ('database_size_bytes', db_size, 50000000000, 100000000000); -- 50GB warning, 100GB critical
    
    -- Active connections
    SELECT COUNT(*) INTO active_connections
    FROM pg_stat_activity 
    WHERE state = 'active';
    INSERT INTO db_health_metrics (metric_name, metric_value, threshold_warning, threshold_critical)
    VALUES ('active_connections', active_connections, 80, 95);
    
    -- Slow queries (queries running > 5 minutes)
    SELECT COUNT(*) INTO slow_queries
    FROM pg_stat_activity 
    WHERE state = 'active' 
      AND NOW() - query_start > INTERVAL '5 minutes';
    INSERT INTO db_health_metrics (metric_name, metric_value, threshold_warning, threshold_critical)
    VALUES ('slow_queries', slow_queries, 5, 10);
    
    -- Check for alerts
    PERFORM check_and_create_alerts();
END;
$$ LANGUAGE plpgsql;

-- Function to check metrics and create alerts
CREATE OR REPLACE FUNCTION check_and_create_alerts()
RETURNS void AS $$
DECLARE
    metric_record RECORD;
    alert_severity VARCHAR(20);
BEGIN
    FOR metric_record IN 
        SELECT * FROM db_health_metrics 
        WHERE recorded_at >= NOW() - INTERVAL '5 minutes'
    LOOP
        IF metric_record.metric_value >= metric_record.threshold_critical THEN
            alert_severity := 'critical';
        ELSIF metric_record.metric_value >= metric_record.threshold_warning THEN
            alert_severity := 'warning';
        ELSE
            CONTINUE;
        END IF;
        
        -- Create alert if not already exists
        INSERT INTO db_alerts (alert_type, severity, message)
        SELECT 
            metric_record.metric_name,
            alert_severity,
            FORMAT('%s is %s (threshold: %s)', 
                   metric_record.metric_name, 
                   metric_record.metric_value,
                   CASE WHEN alert_severity = 'critical' 
                        THEN metric_record.threshold_critical 
                        ELSE metric_record.threshold_warning END)
        WHERE NOT EXISTS (
            SELECT 1 FROM db_alerts 
            WHERE alert_type = metric_record.metric_name 
              AND is_resolved = FALSE
        );
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Query current alerts
SELECT 
    alert_type,
    severity,
    message,
    created_at,
    EXTRACT(EPOCH FROM (NOW() - created_at))/60 as minutes_active
FROM db_alerts 
WHERE is_resolved = FALSE
ORDER BY 
    CASE severity 
        WHEN 'critical' THEN 1 
        WHEN 'warning' THEN 2 
        ELSE 3 
    END,
    created_at DESC;
```

### 49. How do you implement cross-database queries and federation?
**Answer:**
```sql
-- Foreign Data Wrapper (PostgreSQL)
-- Install and create extension
CREATE EXTENSION postgres_fdw;

-- Create foreign server
CREATE SERVER remote_db
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host 'remote-host', port '5432', dbname 'remote_database');

-- Create user mapping
CREATE USER MAPPING FOR current_user
SERVER remote_db
OPTIONS (user 'remote_user', password 'remote_password');

-- Create foreign table
CREATE FOREIGN TABLE remote_orders (
    order_id INT,
    customer_id INT,
    order_date DATE,
    order_amount DECIMAL(10,2)
)
SERVER remote_db
OPTIONS (schema_name 'public', table_name 'orders');

-- Query across databases
SELECT 
    c.customer_name,
    COUNT(ro.order_id) as total_orders,
    SUM(ro.order_amount) as total_spent
FROM customers c  -- Local table
JOIN remote_orders ro ON c.customer_id = ro.customer_id  -- Remote table
GROUP BY c.customer_id, c.customer_name;

-- Database link approach (Oracle-style concept)
-- Create materialized view for cross-database aggregation
CREATE MATERIALIZED VIEW cross_db_summary AS
SELECT 
    'local' as source_db,
    COUNT(*) as order_count,
    SUM(order_amount) as total_amount
FROM orders
UNION ALL
SELECT 
    'remote' as source_db,
    COUNT(*) as order_count,
    SUM(order_amount) as total_amount
FROM remote_orders;

-- Refresh cross-database summary
REFRESH MATERIALIZED VIEW cross_db_summary;
```

### 50. How do you implement database disaster recovery and high availability?
**Answer:**
```sql
-- Replication monitoring (PostgreSQL)
SELECT 
    client_addr,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    write_lag,
    flush_lag,
    replay_lag
FROM pg_stat_replication;

-- Backup verification
CREATE TABLE backup_verification (
    backup_id SERIAL PRIMARY KEY,
    backup_date DATE,
    backup_type VARCHAR(20), -- 'full', 'incremental', 'differential'
    backup_size BIGINT,
    backup_location TEXT,
    verification_status VARCHAR(20), -- 'pending', 'success', 'failed'
    verification_date TIMESTAMP,
    restore_test_date TIMESTAMP,
    notes TEXT
);

-- Recovery Point Objective (RPO) monitoring
CREATE OR REPLACE FUNCTION check_rpo_compliance()
RETURNS TABLE(
    metric_name TEXT,
    current_lag INTERVAL,
    rpo_target INTERVAL,
    is_compliant BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'replication_lag'::TEXT,
        COALESCE(MAX(replay_lag), INTERVAL '0') as current_lag,
        INTERVAL '5 minutes' as rpo_target,
        COALESCE(MAX(replay_lag), INTERVAL '0') <= INTERVAL '5 minutes' as is_compliant
    FROM pg_stat_replication;
    
    RETURN QUERY
    SELECT 
        'last_backup_age'::TEXT,
        NOW() - MAX(backup_date)::timestamp as current_lag,
        INTERVAL '24 hours' as rpo_target,
        NOW() - MAX(backup_date)::timestamp <= INTERVAL '24 hours' as is_compliant
    FROM backup_verification
    WHERE verification_status = 'success';
END;
$$ LANGUAGE plpgsql;

-- Failover readiness check
CREATE OR REPLACE FUNCTION failover_readiness_check()
RETURNS TABLE(
    check_name TEXT,
    status TEXT,
    details TEXT
) AS $$
BEGIN
    -- Check replication status
    RETURN QUERY
    SELECT 
        'replication_status'::TEXT,
        CASE WHEN COUNT(*) > 0 THEN 'OK' ELSE 'FAIL' END,
        FORMAT('%s replicas connected', COUNT(*))
    FROM pg_stat_replication
    WHERE state = 'streaming';
    
    -- Check backup recency
    RETURN QUERY
    SELECT 
        'backup_recency'::TEXT,
        CASE 
            WHEN MAX(backup_date) >= CURRENT_DATE - 1 THEN 'OK'
            ELSE 'FAIL'
        END,
        FORMAT('Last backup: %s', MAX(backup_date))
    FROM backup_verification
    WHERE verification_status = 'success';
    
    -- Check disk space
    RETURN QUERY
    SELECT 
        'disk_space'::TEXT,
        CASE 
            WHEN pg_database_size(current_database()) < pg_tablespace_size('pg_default') * 0.8 
            THEN 'OK'
            ELSE 'WARNING'
        END,
        FORMAT('Database size: %s', pg_size_pretty(pg_database_size(current_database())));
END;
$$ LANGUAGE plpgsql;

-- Execute readiness check
SELECT * FROM failover_readiness_check();
```

## Data Engineering Specific Questions

### 51. How would you design a data pipeline using SQL?
**Answer:**
```sql
-- ETL Pipeline Example
-- 1. Extract: Create staging tables
CREATE TABLE staging_orders AS
SELECT * FROM source_system.orders
WHERE modified_date >= CURRENT_DATE - 1;

-- 2. Transform: Clean and enrich data
CREATE TABLE transformed_orders AS
SELECT 
    order_id,
    customer_id,
    order_date,
    CASE 
        WHEN order_amount < 0 THEN 0 
        ELSE order_amount 
    END as order_amount,
    UPPER(TRIM(status)) as status,
    CURRENT_TIMESTAMP as processed_at
FROM staging_orders
WHERE order_date IS NOT NULL
  AND customer_id IS NOT NULL;

-- 3. Load: Insert into target table
INSERT INTO fact_orders (
    order_id, customer_id, order_date, 
    order_amount, status, processed_at
)
SELECT * FROM transformed_orders
ON CONFLICT (order_id) 
DO UPDATE SET
    order_amount = EXCLUDED.order_amount,
    status = EXCLUDED.status,
    processed_at = EXCLUDED.processed_at;
```

### 52. How do you handle large datasets efficiently?
**Answer:**
```sql
-- 1. Partitioning
CREATE TABLE orders_partitioned (
    order_id BIGINT,
    customer_id INT,
    order_date DATE,
    order_amount DECIMAL(10,2)
) PARTITION BY RANGE (order_date);

-- Create monthly partitions
CREATE TABLE orders_2024_01 PARTITION OF orders_partitioned
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- 2. Indexing strategy
CREATE INDEX idx_orders_customer_date 
ON orders_partitioned (customer_id, order_date);

-- 3. Query optimization for large datasets
SELECT customer_id, SUM(order_amount)
FROM orders_partitioned
WHERE order_date BETWEEN '2024-01-01' AND '2024-01-31'
  AND customer_id IN (SELECT customer_id FROM active_customers)
GROUP BY customer_id
LIMIT 1000;
```

### 53. Explain database normalization with examples
**Answer:**
```sql
-- Unnormalized table (0NF)
CREATE TABLE orders_unnormalized (
    order_id INT,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100),
    customer_phone VARCHAR(20),
    product_names TEXT,  -- "Product1, Product2, Product3"
    product_prices TEXT  -- "10.99, 25.50, 15.75"
);

-- First Normal Form (1NF) - Atomic values
CREATE TABLE orders_1nf (
    order_id INT,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100),
    customer_phone VARCHAR(20),
    product_name VARCHAR(100),
    product_price DECIMAL(10,2)
);

-- Second Normal Form (2NF) - Remove partial dependencies
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100),
    customer_phone VARCHAR(20)
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    product_price DECIMAL(10,2)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date DATE
);

CREATE TABLE order_items (
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity INT,
    PRIMARY KEY (order_id, product_id)
);

-- Third Normal Form (3NF) - Remove transitive dependencies
CREATE TABLE categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(100)
);

ALTER TABLE products 
ADD COLUMN category_id INT REFERENCES categories(category_id);
```

---

## 🎯 **Conceptual & Theoretical Questions**

### 25. What are the different types of database relationships?
**Answer:**
**Relationship Types:**
- **One-to-One (1:1)**: Each record in table A relates to exactly one record in table B
- **One-to-Many (1:M)**: One record in table A relates to multiple records in table B
- **Many-to-Many (M:M)**: Multiple records in table A relate to multiple records in table B

```sql
-- One-to-One: User and Profile
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50)
);

CREATE TABLE user_profiles (
    profile_id INT PRIMARY KEY,
    user_id INT UNIQUE REFERENCES users(user_id),
    bio TEXT
);

-- One-to-Many: Customer and Orders
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id)
);

-- Many-to-Many: Students and Courses (with junction table)
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(100)
);

CREATE TABLE enrollments (
    student_id INT REFERENCES students(student_id),
    course_id INT REFERENCES courses(course_id),
    enrollment_date DATE,
    PRIMARY KEY (student_id, course_id)
);
```

### 26. Explain different isolation levels in databases
**Answer:**
**Isolation Levels (from lowest to highest):**

1. **READ UNCOMMITTED**: Can read uncommitted changes (dirty reads)
2. **READ COMMITTED**: Only reads committed data (prevents dirty reads)
3. **REPEATABLE READ**: Same data returned for repeated reads (prevents non-repeatable reads)
4. **SERIALIZABLE**: Highest isolation, prevents phantom reads

```sql
-- Set isolation level
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- Example of isolation level effects
-- Session 1:
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
-- Transaction not committed yet

-- Session 2 with READ UNCOMMITTED:
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SELECT balance FROM accounts WHERE account_id = 1; -- Sees uncommitted change

-- Session 2 with READ COMMITTED:
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SELECT balance FROM accounts WHERE account_id = 1; -- Sees original value
```

### 27. What are database locks and their types?
**Answer:**
**Lock Types:**
- **Shared Lock (S)**: Multiple transactions can read, none can write
- **Exclusive Lock (X)**: Only one transaction can read/write
- **Intent Locks**: Indicate intention to acquire locks at lower level
- **Update Lock (U)**: Prevents deadlocks during update operations

**Lock Granularity:**
- **Row-level**: Locks individual rows
- **Page-level**: Locks database pages
- **Table-level**: Locks entire tables
- **Database-level**: Locks entire database

### 28. Explain the difference between clustered and non-clustered indexes
**Answer:**
**Clustered Index:**
- Physical ordering of data matches index order
- One per table (usually primary key)
- Data pages stored in order of index key
- Faster for range queries

**Non-Clustered Index:**
- Logical ordering separate from physical storage
- Multiple allowed per table
- Contains pointers to data rows
- Faster for specific value lookups

```sql
-- Clustered index (implicit with PRIMARY KEY)
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,  -- Clustered index
    name VARCHAR(100),
    department VARCHAR(50)
);

-- Non-clustered indexes
CREATE INDEX idx_name ON employees(name);  -- Non-clustered
CREATE INDEX idx_dept ON employees(department);  -- Non-clustered

-- Composite non-clustered index
CREATE INDEX idx_dept_name ON employees(department, name);
```

### 29. What is database sharding and when would you use it?
**Answer:**
**Sharding** is horizontal partitioning where data is distributed across multiple database instances.

**When to Use:**
- Database size exceeds single server capacity
- Query load exceeds single server performance
- Geographic distribution requirements
- Regulatory compliance (data locality)

**Sharding Strategies:**
```sql
-- Range-based sharding
-- Shard 1: customer_id 1-1000000
-- Shard 2: customer_id 1000001-2000000

-- Hash-based sharding
-- Shard = customer_id % number_of_shards

-- Directory-based sharding
CREATE TABLE shard_directory (
    customer_id INT,
    shard_id INT
);
```

### 30. Explain OLTP vs OLAP systems
**Answer:**
**OLTP (Online Transaction Processing):**
- Handles day-to-day transactions
- Normalized data structure
- Fast INSERT/UPDATE/DELETE operations
- High concurrency, low latency
- Examples: Order processing, banking systems

**OLAP (Online Analytical Processing):**
- Handles analytical queries
- Denormalized/dimensional data structure
- Complex SELECT operations with aggregations
- Lower concurrency, higher latency acceptable
- Examples: Data warehouses, reporting systems

```sql
-- OLTP query example
INSERT INTO orders (customer_id, product_id, quantity, order_date)
VALUES (12345, 67890, 2, CURRENT_DATE);

-- OLAP query example
SELECT 
    p.category,
    EXTRACT(YEAR FROM o.order_date) as year,
    EXTRACT(MONTH FROM o.order_date) as month,
    SUM(oi.quantity * oi.price) as total_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date >= '2023-01-01'
GROUP BY p.category, EXTRACT(YEAR FROM o.order_date), EXTRACT(MONTH FROM o.order_date)
ORDER BY year, month, total_revenue DESC;
```

---

## 🏗️ **Database Design & Architecture Questions**

### 31. How would you design a database schema for an e-commerce platform?
**Answer:**
```sql
-- Core entities
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_category_id INT REFERENCES categories(category_id),
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category_id INT REFERENCES categories(category_id),
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    stock_quantity INT DEFAULT 0 CHECK (stock_quantity >= 0),
    sku VARCHAR(100) UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE addresses (
    address_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    address_type VARCHAR(20) CHECK (address_type IN ('billing', 'shipping')),
    street_address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    is_default BOOLEAN DEFAULT FALSE
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    order_status VARCHAR(20) DEFAULT 'pending' 
        CHECK (order_status IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled')),
    total_amount DECIMAL(10,2) NOT NULL,
    shipping_address_id INT REFERENCES addresses(address_id),
    billing_address_id INT REFERENCES addresses(address_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    shipped_date TIMESTAMP,
    delivered_date TIMESTAMP
);

CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) GENERATED ALWAYS AS (quantity * unit_price) STORED
);

-- Indexes for performance
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_order_items_order ON order_items(order_id);
```

### 32. How do you handle database migrations and schema changes?
**Answer:**
```sql
-- Migration script example
-- Migration: 001_add_user_preferences.sql

-- Add new column with default value
ALTER TABLE users 
ADD COLUMN preferences JSONB DEFAULT '{}'::jsonb;

-- Create index on new column
CREATE INDEX idx_users_preferences ON users USING GIN (preferences);

-- Update existing records if needed
UPDATE users 
SET preferences = '{"notifications": true, "theme": "light"}'
WHERE preferences = '{}'::jsonb;

-- Migration tracking table
CREATE TABLE IF NOT EXISTS schema_migrations (
    version VARCHAR(255) PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO schema_migrations (version) VALUES ('001_add_user_preferences');
```

### 33. Explain database backup and recovery strategies
**Answer:**
**Backup Types:**
- **Full Backup**: Complete database copy
- **Incremental Backup**: Changes since last backup
- **Differential Backup**: Changes since last full backup
- **Transaction Log Backup**: Log file backups for point-in-time recovery

```sql
-- PostgreSQL backup examples
-- Full backup
pg_dump -h localhost -U postgres -d mydb > full_backup.sql

-- Compressed backup
pg_dump -h localhost -U postgres -Fc -d mydb > backup.dump

-- Restore from backup
psql -h localhost -U postgres -d mydb < full_backup.sql
pg_restore -h localhost -U postgres -d mydb backup.dump

-- Point-in-time recovery setup
-- Enable WAL archiving in postgresql.conf
-- wal_level = replica
-- archive_mode = on
-- archive_command = 'cp %p /path/to/archive/%f'
```

---

## 🔍 **Performance Tuning & Optimization Questions**

### 34. How do you identify and fix slow queries?
**Answer:**
**Identification Methods:**
1. **Query execution plans**
2. **Database performance monitoring**
3. **Slow query logs**
4. **Application performance monitoring**

```sql
-- Enable slow query logging (MySQL)
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;

-- Analyze query performance (PostgreSQL)
EXPLAIN (ANALYZE, BUFFERS) 
SELECT c.name, COUNT(o.order_id)
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.registration_date >= '2023-01-01'
GROUP BY c.customer_id, c.name;

-- Query optimization techniques
-- 1. Add appropriate indexes
CREATE INDEX idx_customers_reg_date ON customers(registration_date);
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- 2. Rewrite query to use EXISTS instead of JOIN when appropriate
SELECT c.name
FROM customers c
WHERE c.registration_date >= '2023-01-01'
  AND EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id
  );

-- 3. Use LIMIT for large result sets
SELECT * FROM large_table 
ORDER BY created_date DESC 
LIMIT 100;
```

### 35. What are database statistics and why are they important?
**Answer:**
**Database Statistics** help the query optimizer make informed decisions about execution plans.

```sql
-- Update table statistics (PostgreSQL)
ANALYZE customers;
ANALYZE orders;

-- View table statistics
SELECT 
    schemaname,
    tablename,
    n_tup_ins,
    n_tup_upd,
    n_tup_del,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables;

-- Manual statistics update for specific columns
ANALYZE customers (customer_id, registration_date);

-- Check if statistics are outdated
SELECT 
    tablename,
    n_tup_ins + n_tup_upd + n_tup_del as total_changes,
    last_analyze,
    CASE 
        WHEN last_analyze < CURRENT_DATE - INTERVAL '7 days' 
        THEN 'Statistics may be outdated'
        ELSE 'Statistics are current'
    END as status
FROM pg_stat_user_tables
WHERE schemaname = 'public';
```

---

## 🛡️ **Security & Compliance Questions**

### 36. How do you implement database security best practices?
**Answer:**
**Security Measures:**

```sql
-- 1. User access control
CREATE ROLE data_analyst;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO data_analyst;
GRANT USAGE ON SCHEMA public TO data_analyst;

CREATE ROLE data_engineer;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO data_engineer;

-- 2. Row-level security
ALTER TABLE customer_data ENABLE ROW LEVEL SECURITY;

CREATE POLICY customer_data_policy ON customer_data
FOR ALL TO data_analyst
USING (region = current_setting('app.user_region'));

-- 3. Column-level security (data masking)
CREATE VIEW customer_masked AS
SELECT 
    customer_id,
    name,
    CASE 
        WHEN current_user = 'admin' THEN email
        ELSE CONCAT(LEFT(email, 3), '***@***.com')
    END as email,
    CASE 
        WHEN current_user = 'admin' THEN phone
        ELSE 'XXX-XXX-' || RIGHT(phone, 4)
    END as phone
FROM customers;

-- 4. Audit logging
CREATE TABLE audit_log (
    log_id SERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    operation VARCHAR(10),
    user_name VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
CREATE TRIGGER customers_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON customers
FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();
```

### 37. How do you handle PII (Personally Identifiable Information) in databases?
**Answer:**
```sql
-- 1. Data classification
CREATE TABLE data_classification (
    table_name VARCHAR(100),
    column_name VARCHAR(100),
    classification VARCHAR(20) CHECK (classification IN ('public', 'internal', 'confidential', 'restricted')),
    contains_pii BOOLEAN DEFAULT FALSE,
    retention_period INTERVAL
);

-- 2. PII encryption
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Encrypt sensitive data
INSERT INTO customers (name, email_encrypted, phone_encrypted)
VALUES (
    'John Doe',
    pgp_sym_encrypt('john@example.com', 'encryption_key'),
    pgp_sym_encrypt('555-1234', 'encryption_key')
);

-- Decrypt for authorized access
SELECT 
    name,
    pgp_sym_decrypt(email_encrypted, 'encryption_key') as email,
    pgp_sym_decrypt(phone_encrypted, 'encryption_key') as phone
FROM customers
WHERE customer_id = 123;

-- 3. Data anonymization for testing
CREATE TABLE customers_anonymized AS
SELECT 
    customer_id,
    'Customer_' || customer_id as name,
    'user' || customer_id || '@example.com' as email,
    '555-' || LPAD((customer_id % 10000)::text, 4, '0') as phone,
    registration_date,
    -- Keep non-PII data as-is
    city,
    state
FROM customers;

-- 4. Data retention and deletion
CREATE OR REPLACE FUNCTION cleanup_expired_data()
RETURNS void AS $$
BEGIN
    -- Delete old customer data based on retention policy
    DELETE FROM customers 
    WHERE last_activity_date < CURRENT_DATE - INTERVAL '7 years'
      AND account_status = 'inactive';
    
    -- Anonymize instead of delete for analytical purposes
    UPDATE customers 
    SET 
        email = 'anonymized_' || customer_id || '@deleted.com',
        phone = NULL,
        address = NULL
    WHERE last_activity_date < CURRENT_DATE - INTERVAL '5 years'
      AND account_status = 'inactive';
END;
$$ LANGUAGE plpgsql;

-- Schedule cleanup job
SELECT cron.schedule('cleanup-expired-data', '0 2 * * 0', 'SELECT cleanup_expired_data();');
```

---

## 📊 **Data Warehousing & Analytics Questions**

### 38. Explain star schema vs snowflake schema
**Answer:**
**Star Schema:**
- Central fact table surrounded by dimension tables
- Dimension tables are denormalized
- Simpler queries, better performance
- More storage space due to redundancy

**Snowflake Schema:**
- Dimension tables are normalized
- More complex structure with sub-dimensions
- Less storage space, more complex queries
- Better data integrity

```sql
-- Star Schema Example
CREATE TABLE fact_sales (
    sale_id SERIAL PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    product_key INT REFERENCES dim_product(product_key),
    customer_key INT REFERENCES dim_customer(customer_key),
    store_key INT REFERENCES dim_store(store_key),
    quantity INT,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2)
);

-- Denormalized dimension table (Star Schema)
CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(50),
    product_name VARCHAR(255),
    category_name VARCHAR(100),
    subcategory_name VARCHAR(100),
    brand_name VARCHAR(100),
    supplier_name VARCHAR(100)
);

-- Snowflake Schema - Normalized dimensions
CREATE TABLE dim_product_snowflake (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(50),
    product_name VARCHAR(255),
    category_key INT REFERENCES dim_category(category_key),
    brand_key INT REFERENCES dim_brand(brand_key)
);

CREATE TABLE dim_category (
    category_key SERIAL PRIMARY KEY,
    category_name VARCHAR(100),
    subcategory_key INT REFERENCES dim_subcategory(subcategory_key)
);

CREATE TABLE dim_subcategory (
    subcategory_key SERIAL PRIMARY KEY,
    subcategory_name VARCHAR(100)
);
```

### 39. How do you implement data quality monitoring in SQL?
**Answer:**
```sql
-- Comprehensive data quality framework
CREATE TABLE data_quality_rules (
    rule_id SERIAL PRIMARY KEY,
    rule_name VARCHAR(255),
    table_name VARCHAR(100),
    column_name VARCHAR(100),
    rule_type VARCHAR(50), -- 'completeness', 'uniqueness', 'validity', 'consistency'
    rule_sql TEXT,
    threshold_value DECIMAL(5,2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert quality rules
INSERT INTO data_quality_rules (rule_name, table_name, column_name, rule_type, rule_sql, threshold_value)
VALUES 
('Email completeness', 'customers', 'email', 'completeness', 
 'SELECT (COUNT(email)::DECIMAL / COUNT(*)) * 100 FROM customers', 95.0),
('Email uniqueness', 'customers', 'email', 'uniqueness',
 'SELECT (COUNT(DISTINCT email)::DECIMAL / COUNT(email)) * 100 FROM customers WHERE email IS NOT NULL', 100.0),
('Email format validity', 'customers', 'email', 'validity',
 'SELECT (COUNT(CASE WHEN email ~ ''^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'' THEN 1 END)::DECIMAL / COUNT(email)) * 100 FROM customers WHERE email IS NOT NULL', 98.0);

-- Data quality execution results
CREATE TABLE data_quality_results (
    result_id SERIAL PRIMARY KEY,
    rule_id INT REFERENCES data_quality_rules(rule_id),
    execution_date DATE DEFAULT CURRENT_DATE,
    actual_value DECIMAL(10,2),
    threshold_value DECIMAL(5,2),
    status VARCHAR(10) CHECK (status IN ('PASS', 'FAIL', 'WARNING')),
    record_count INT,
    execution_time_ms INT
);

-- Function to execute data quality checks
CREATE OR REPLACE FUNCTION execute_data_quality_checks()
RETURNS TABLE(
    rule_name VARCHAR(255),
    actual_value DECIMAL(10,2),
    threshold_value DECIMAL(5,2),
    status VARCHAR(10)
) AS $$
DECLARE
    rule_record RECORD;
    result_value DECIMAL(10,2);
    check_status VARCHAR(10);
BEGIN
    FOR rule_record IN 
        SELECT * FROM data_quality_rules WHERE is_active = TRUE
    LOOP
        -- Execute the rule SQL
        EXECUTE rule_record.rule_sql INTO result_value;
        
        -- Determine status
        IF result_value >= rule_record.threshold_value THEN
            check_status := 'PASS';
        ELSIF result_value >= rule_record.threshold_value * 0.9 THEN
            check_status := 'WARNING';
        ELSE
            check_status := 'FAIL';
        END IF;
        
        -- Insert result
        INSERT INTO data_quality_results (rule_id, actual_value, threshold_value, status)
        VALUES (rule_record.rule_id, result_value, rule_record.threshold_value, check_status);
        
        -- Return result
        RETURN QUERY SELECT rule_record.rule_name, result_value, rule_record.threshold_value, check_status;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Execute quality checks
SELECT * FROM execute_data_quality_checks();
```

---

## Key Takeaways

1. **SQL Fundamentals**: Master joins, subqueries, window functions, and CTEs
2. **Database Design**: Understand normalization, relationships, and schema design
3. **Performance Optimization**: Index strategies, query tuning, and execution plans
4. **Data Quality**: Implement comprehensive validation and monitoring frameworks
5. **Security**: Row-level security, data masking, and audit logging
6. **Transactions**: ACID properties, isolation levels, and concurrency control
7. **Advanced Features**: Window functions, recursive CTEs, and analytical queries
8. **Data Warehousing**: Star/snowflake schemas and dimensional modeling
9. **Scalability**: Partitioning, sharding, and distributed database concepts
10. **Backup & Recovery**: Disaster recovery planning and point-in-time recovery
11. **Compliance**: PII handling, data retention, and regulatory requirements
12. **Monitoring**: Performance metrics, slow query identification, and optimization
13. **Data Engineering**: ETL processes, data pipelines, and batch processing
14. **Analytics**: Complex aggregations, time-series analysis, and business metrics
15. **Modern SQL**: JSON handling, array operations, and NoSQL integration
```