# SQL Key Concepts for Data Engineering

## 📋 Table of Contents

1. [Overview](#-overview)
2. [SQL Theoretical Concepts](#-sql-theoretical-concepts)
3. [Data Types & Structures](#-data-types--structures)
4. [Basic Query Operations](#-basic-query-operations)
5. [Joins & Relationships](#-joins--relationships)
6. [Aggregations & Grouping](#-aggregations--grouping)
7. [Window Functions](#-window-functions)
8. [Subqueries & CTEs](#-subqueries--ctes)
9. [Data Modification](#-data-modification)
10. [Indexes & Performance](#-indexes--performance)
11. [Transactions & ACID](#-transactions--acid)
12. [Best Practices](#-best-practices)
13. [Interview Focus Areas](#-interview-focus-areas)

---

## 🎯 Overview

SQL (Structured Query Language) is the foundation of data engineering. It's used for querying, manipulating, and managing relational databases, making it essential for data extraction, transformation, and analysis.

**Key Benefits:**
- **Universal**: Works across all major database systems
- **Declarative**: Describe what you want, not how to get it
- **Powerful**: Handle complex data operations efficiently
- **Scalable**: From small datasets to petabyte-scale warehouses
- **Standard**: ANSI SQL ensures portability

## 📚 Related Documents

- **[SQL Advanced Database Engineering](./SQL_ADVANCED_DATABASE_ENGINEERING.md)** - Production patterns, optimization, security
- **[SQL Quick Reference](./SQL_QUICK_REFERENCE.md)** - Essential commands and patterns
- **[SQL Interview Questions](./SQL_INTERVIEW_QUESTIONS.md)** - Common interview questions

## 🧠 SQL Theoretical Concepts

### Relational Model Fundamentals

**Tables (Relations):**
A table represents an entity and consists of rows (tuples) and columns (attributes). Each table must have a primary key to uniquely identify rows.

```sql
-- Example: Users table structure
CREATE TABLE users (
    user_id INT PRIMARY KEY,           -- Unique identifier
    username VARCHAR(50) NOT NULL,     -- Required field
    email VARCHAR(100) UNIQUE,         -- Must be unique
    created_at TIMESTAMP DEFAULT NOW(), -- Auto-populated
    is_active BOOLEAN DEFAULT TRUE     -- Default value
);

-- Insert sample data
INSERT INTO users (user_id, username, email) VALUES
(1, 'alice', 'alice@example.com'),
(2, 'bob', 'bob@example.com'),
(3, 'charlie', 'charlie@example.com');

-- View the data
SELECT * FROM users;
-- Output:
-- user_id | username | email              | created_at          | is_active
-- 1       | alice    | alice@example.com  | 2024-01-01 10:00:00 | true
-- 2       | bob      | bob@example.com    | 2024-01-01 10:00:01 | true
-- 3       | charlie  | charlie@example.com| 2024-01-01 10:00:02 | true
```

**Normalization:**
The process of organizing data to reduce redundancy and improve data integrity.

```sql
-- Before normalization (1NF violation - repeating groups)
CREATE TABLE orders_bad (
    order_id INT,
    customer_name VARCHAR(100),
    product1 VARCHAR(100),
    product2 VARCHAR(100),
    product3 VARCHAR(100)
);

-- After normalization (proper design)
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date DATE
);

CREATE TABLE order_items (
    order_id INT REFERENCES orders(order_id),
    product_name VARCHAR(100),
    quantity INT,
    PRIMARY KEY (order_id, product_name)
);
```

### Query Execution Process

**SQL Query Execution Order:**
Understanding how SQL processes queries helps write efficient code.

```sql
-- Logical execution order (not syntax order)
SELECT customer_name, COUNT(*) as order_count    -- 5. SELECT
FROM customers c                                  -- 1. FROM
JOIN orders o ON c.customer_id = o.customer_id   -- 2. JOIN
WHERE o.order_date >= '2024-01-01'              -- 3. WHERE
GROUP BY customer_name                           -- 4. GROUP BY
HAVING COUNT(*) > 2                             -- 6. HAVING
ORDER BY order_count DESC                       -- 7. ORDER BY
LIMIT 10;                                       -- 8. LIMIT

-- This query finds customers with more than 2 orders since 2024
-- Output example:
-- customer_name | order_count
-- Alice         | 5
-- Bob           | 3
```

## 📊 Data Types & Structures

### Numeric Types

```sql
-- Integer types
CREATE TABLE numeric_examples (
    small_int SMALLINT,      -- -32,768 to 32,767
    regular_int INT,         -- -2 billion to 2 billion
    big_int BIGINT,         -- Very large integers
    
    -- Decimal types (exact precision)
    price DECIMAL(10,2),     -- 10 digits total, 2 after decimal
    rate NUMERIC(5,4),       -- 5 digits total, 4 after decimal
    
    -- Floating point (approximate)
    measurement FLOAT,       -- Single precision
    calculation DOUBLE       -- Double precision
);

-- Insert examples
INSERT INTO numeric_examples VALUES
(100, 1000000, 9223372036854775807, 999.99, 0.1234, 3.14159, 2.718281828);

-- Demonstrate precision differences
SELECT 
    price,
    price + 0.001 as price_plus,           -- Exact arithmetic
    measurement,
    measurement + 0.001 as measurement_plus -- Approximate arithmetic
FROM numeric_examples;
```

### String Types

```sql
-- String type examples
CREATE TABLE string_examples (
    fixed_char CHAR(10),        -- Fixed length, padded with spaces
    variable_char VARCHAR(100), -- Variable length, up to 100 chars
    long_text TEXT,            -- Unlimited length text
    json_data JSON             -- JSON data type (PostgreSQL/MySQL)
);

-- String operations
SELECT 
    'Hello' || ' ' || 'World' as concatenation,           -- Hello World
    UPPER('data engineering') as uppercase,               -- DATA ENGINEERING
    LOWER('SQL QUERIES') as lowercase,                    -- sql queries
    LENGTH('Hello World') as string_length,               -- 11
    SUBSTRING('Hello World', 1, 5) as substring,          -- Hello
    REPLACE('Hello World', 'World', 'SQL') as replaced;   -- Hello SQL
```

### Date and Time Types

```sql
-- Date/time examples
CREATE TABLE datetime_examples (
    just_date DATE,                    -- 2024-01-01
    just_time TIME,                    -- 14:30:00
    date_and_time TIMESTAMP,           -- 2024-01-01 14:30:00
    with_timezone TIMESTAMPTZ          -- 2024-01-01 14:30:00+00
);

-- Date operations
SELECT 
    CURRENT_DATE as today,                                    -- 2024-01-01
    CURRENT_TIMESTAMP as now,                                 -- 2024-01-01 14:30:00
    DATE '2024-01-01' + INTERVAL '30 days' as thirty_days_later, -- 2024-01-31
    EXTRACT(YEAR FROM CURRENT_DATE) as current_year,          -- 2024
    EXTRACT(MONTH FROM CURRENT_DATE) as current_month,        -- 1
    DATE_TRUNC('month', CURRENT_DATE) as month_start;         -- 2024-01-01
```

## 🔍 Basic Query Operations

### SELECT Fundamentals

```sql
-- Create sample data
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(50),
    salary DECIMAL(10,2),
    hire_date DATE
);

INSERT INTO employees VALUES
(1, 'Alice Johnson', 'Engineering', 75000, '2022-01-15'),
(2, 'Bob Smith', 'Marketing', 65000, '2022-03-20'),
(3, 'Charlie Brown', 'Engineering', 80000, '2021-11-10'),
(4, 'Diana Prince', 'HR', 70000, '2023-02-01'),
(5, 'Eve Wilson', 'Engineering', 85000, '2021-08-15');

-- Basic SELECT operations
SELECT name, salary FROM employees;
-- Output:
-- name          | salary
-- Alice Johnson | 75000
-- Bob Smith     | 65000
-- Charlie Brown | 80000
-- Diana Prince  | 70000
-- Eve Wilson    | 85000

-- SELECT with calculations
SELECT 
    name,
    salary,
    salary * 12 as annual_salary,
    salary * 0.1 as monthly_bonus
FROM employees;

-- Conditional logic with CASE
SELECT 
    name,
    salary,
    CASE 
        WHEN salary >= 80000 THEN 'Senior'
        WHEN salary >= 70000 THEN 'Mid-level'
        ELSE 'Junior'
    END as level
FROM employees;
-- Output:
-- name          | salary | level
-- Alice Johnson | 75000  | Mid-level
-- Bob Smith     | 65000  | Junior
-- Charlie Brown | 80000  | Senior
-- Diana Prince  | 70000  | Mid-level
-- Eve Wilson    | 85000  | Senior
```

### Filtering with WHERE

```sql
-- Basic filtering
SELECT name, department, salary 
FROM employees 
WHERE department = 'Engineering';
-- Output:
-- name          | department  | salary
-- Alice Johnson | Engineering | 75000
-- Charlie Brown | Engineering | 80000
-- Eve Wilson    | Engineering | 85000

-- Multiple conditions
SELECT name, salary 
FROM employees 
WHERE department = 'Engineering' 
  AND salary > 75000;
-- Output:
-- name          | salary
-- Charlie Brown | 80000
-- Eve Wilson    | 85000

-- Range filtering
SELECT name, hire_date 
FROM employees 
WHERE hire_date BETWEEN '2022-01-01' AND '2022-12-31';
-- Output:
-- name          | hire_date
-- Alice Johnson | 2022-01-15
-- Bob Smith     | 2022-03-20

-- Pattern matching
SELECT name 
FROM employees 
WHERE name LIKE '%Johnson%';
-- Output:
-- name
-- Alice Johnson

-- NULL handling
SELECT name, department 
FROM employees 
WHERE department IS NOT NULL;
```

### Sorting with ORDER BY

```sql
-- Sort by salary (ascending by default)
SELECT name, salary 
FROM employees 
ORDER BY salary;
-- Output:
-- name          | salary
-- Bob Smith     | 65000
-- Diana Prince  | 70000
-- Alice Johnson | 75000
-- Charlie Brown | 80000
-- Eve Wilson    | 85000

-- Sort by multiple columns
SELECT name, department, salary 
FROM employees 
ORDER BY department, salary DESC;
-- Output:
-- name          | department  | salary
-- Eve Wilson    | Engineering | 85000
-- Charlie Brown | Engineering | 80000
-- Alice Johnson | Engineering | 75000
-- Diana Prince  | HR          | 70000
-- Bob Smith     | Marketing   | 65000
```

## 🔗 Joins & Relationships

### Inner Joins

```sql
-- Create related tables
CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(50),
    manager_id INT
);

CREATE TABLE projects (
    project_id INT PRIMARY KEY,
    project_name VARCHAR(100),
    dept_id INT,
    budget DECIMAL(12,2)
);

-- Insert sample data
INSERT INTO departments VALUES
(1, 'Engineering', 3),
(2, 'Marketing', 2),
(3, 'HR', 4);

INSERT INTO projects VALUES
(101, 'Website Redesign', 1, 50000),
(102, 'Mobile App', 1, 75000),
(103, 'Marketing Campaign', 2, 25000),
(104, 'HR System', 3, 30000);

-- Inner join - only matching records
SELECT 
    e.name,
    d.dept_name,
    p.project_name,
    p.budget
FROM employees e
INNER JOIN departments d ON e.department = d.dept_name
INNER JOIN projects p ON d.dept_id = p.dept_id;
-- Output:
-- name          | dept_name   | project_name      | budget
-- Alice Johnson | Engineering | Website Redesign  | 50000
-- Alice Johnson | Engineering | Mobile App        | 75000
-- Charlie Brown | Engineering | Website Redesign  | 50000
-- Charlie Brown | Engineering | Mobile App        | 75000
-- Eve Wilson    | Engineering | Website Redesign  | 50000
-- Eve Wilson    | Engineering | Mobile App        | 75000
-- Bob Smith     | Marketing   | Marketing Campaign| 25000
-- Diana Prince  | HR          | HR System         | 30000
```

### Outer Joins

```sql
-- Left join - all records from left table
SELECT 
    e.name,
    d.dept_name,
    d.manager_id
FROM employees e
LEFT JOIN departments d ON e.department = d.dept_name;

-- Right join - all records from right table
SELECT 
    e.name,
    d.dept_name
FROM employees e
RIGHT JOIN departments d ON e.department = d.dept_name;

-- Full outer join - all records from both tables
SELECT 
    e.name,
    d.dept_name
FROM employees e
FULL OUTER JOIN departments d ON e.department = d.dept_name;
```

### Self Joins

```sql
-- Find employees and their managers
ALTER TABLE employees ADD COLUMN manager_id INT;

UPDATE employees SET manager_id = 3 WHERE emp_id IN (1, 5);
UPDATE employees SET manager_id = 2 WHERE emp_id = 4;

SELECT 
    e.name as employee,
    m.name as manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.emp_id;
-- Output:
-- employee      | manager
-- Alice Johnson | Charlie Brown
-- Bob Smith     | null
-- Charlie Brown | null
-- Diana Prince  | Bob Smith
-- Eve Wilson    | Charlie Brown
```

## 📈 Aggregations & Grouping

### Basic Aggregations

```sql
-- Common aggregate functions
SELECT 
    COUNT(*) as total_employees,
    COUNT(manager_id) as employees_with_managers,
    AVG(salary) as average_salary,
    MIN(salary) as minimum_salary,
    MAX(salary) as maximum_salary,
    SUM(salary) as total_payroll
FROM employees;
-- Output:
-- total_employees | employees_with_managers | average_salary | minimum_salary | maximum_salary | total_payroll
-- 5               | 3                       | 75000          | 65000          | 85000          | 375000
```

### GROUP BY Operations

```sql
-- Group by department
SELECT 
    department,
    COUNT(*) as employee_count,
    AVG(salary) as avg_salary,
    MIN(hire_date) as earliest_hire,
    MAX(hire_date) as latest_hire
FROM employees
GROUP BY department
ORDER BY avg_salary DESC;
-- Output:
-- department  | employee_count | avg_salary | earliest_hire | latest_hire
-- Engineering | 3              | 80000      | 2021-08-15    | 2022-01-15
-- HR          | 1              | 70000      | 2023-02-01    | 2023-02-01
-- Marketing   | 1              | 65000      | 2022-03-20    | 2022-03-20
```

### HAVING Clause

```sql
-- Filter groups with HAVING
SELECT 
    department,
    COUNT(*) as employee_count,
    AVG(salary) as avg_salary
FROM employees
GROUP BY department
HAVING COUNT(*) > 1 AND AVG(salary) > 70000;
-- Output:
-- department  | employee_count | avg_salary
-- Engineering | 3              | 80000
```

## 🪟 Window Functions

### Basic Window Functions

```sql
-- Ranking functions
SELECT 
    name,
    department,
    salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) as row_num,
    RANK() OVER (ORDER BY salary DESC) as rank,
    DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank
FROM employees;
-- Output:
-- name          | department  | salary | row_num | rank | dense_rank
-- Eve Wilson    | Engineering | 85000  | 1       | 1    | 1
-- Charlie Brown | Engineering | 80000  | 2       | 2    | 2
-- Alice Johnson | Engineering | 75000  | 3       | 3    | 3
-- Diana Prince  | HR          | 70000  | 4       | 4    | 4
-- Bob Smith     | Marketing   | 65000  | 5       | 5    | 5
```

### Partitioned Window Functions

```sql
-- Ranking within departments
SELECT 
    name,
    department,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank,
    AVG(salary) OVER (PARTITION BY department) as dept_avg_salary
FROM employees;
-- Output:
-- name          | department  | salary | dept_rank | dept_avg_salary
-- Eve Wilson    | Engineering | 85000  | 1         | 80000
-- Charlie Brown | Engineering | 80000  | 2         | 80000
-- Alice Johnson | Engineering | 75000  | 3         | 80000
-- Diana Prince  | HR          | 70000  | 1         | 70000
-- Bob Smith     | Marketing   | 65000  | 1         | 65000
```

### Running Totals and Moving Averages

```sql
-- Running totals and moving averages
SELECT 
    name,
    salary,
    SUM(salary) OVER (ORDER BY hire_date) as running_total,
    AVG(salary) OVER (ORDER BY hire_date ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) as moving_avg
FROM employees
ORDER BY hire_date;
-- Output shows cumulative salary costs and 3-point moving averages
```

## 🔄 Subqueries & CTEs

### Subqueries

```sql
-- Scalar subquery
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
-- Output:
-- name          | salary
-- Charlie Brown | 80000
-- Eve Wilson    | 85000

-- Correlated subquery
SELECT 
    e1.name,
    e1.department,
    e1.salary
FROM employees e1
WHERE e1.salary > (
    SELECT AVG(e2.salary)
    FROM employees e2
    WHERE e2.department = e1.department
);
```

### Common Table Expressions (CTEs)

```sql
-- Simple CTE
WITH dept_stats AS (
    SELECT 
        department,
        COUNT(*) as emp_count,
        AVG(salary) as avg_salary
    FROM employees
    GROUP BY department
)
SELECT 
    department,
    emp_count,
    avg_salary,
    CASE 
        WHEN avg_salary > 75000 THEN 'High Pay'
        WHEN avg_salary > 65000 THEN 'Medium Pay'
        ELSE 'Low Pay'
    END as pay_category
FROM dept_stats;
-- Output:
-- department  | emp_count | avg_salary | pay_category
-- Engineering | 3         | 80000      | High Pay
-- HR          | 1         | 70000      | Medium Pay
-- Marketing   | 1         | 65000      | Low Pay
```

### Recursive CTEs

```sql
-- Recursive CTE for organizational hierarchy
WITH RECURSIVE org_chart AS (
    -- Base case: top-level managers
    SELECT emp_id, name, manager_id, 0 as level
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive case: employees with managers
    SELECT e.emp_id, e.name, e.manager_id, oc.level + 1
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.emp_id
)
SELECT 
    REPEAT('  ', level) || name as hierarchy,
    level
FROM org_chart
ORDER BY level, name;
```

## ✏️ Data Modification

### INSERT Operations

```sql
-- Single row insert
INSERT INTO employees (emp_id, name, department, salary, hire_date)
VALUES (6, 'Frank Miller', 'Sales', 68000, '2024-01-01');

-- Multiple row insert
INSERT INTO employees VALUES
(7, 'Grace Lee', 'Sales', 72000, '2024-01-15'),
(8, 'Henry Davis', 'Engineering', 78000, '2024-02-01');

-- Insert from SELECT
INSERT INTO employees (emp_id, name, department, salary, hire_date)
SELECT 
    emp_id + 100,
    'Temp ' || name,
    'Temporary',
    salary * 0.8,
    CURRENT_DATE
FROM employees
WHERE department = 'Engineering';
```

### UPDATE Operations

```sql
-- Simple update
UPDATE employees 
SET salary = salary * 1.1 
WHERE department = 'Engineering';

-- Update with joins
UPDATE employees 
SET salary = salary * 1.05
FROM departments d
WHERE employees.department = d.dept_name 
  AND d.dept_id = 1;

-- Conditional update
UPDATE employees
SET salary = CASE 
    WHEN salary < 70000 THEN salary * 1.15
    WHEN salary < 80000 THEN salary * 1.10
    ELSE salary * 1.05
END;
```

### DELETE Operations

```sql
-- Simple delete
DELETE FROM employees 
WHERE hire_date < '2022-01-01';

-- Delete with subquery
DELETE FROM employees
WHERE salary < (SELECT AVG(salary) FROM employees);

-- Delete with joins
DELETE e
FROM employees e
JOIN departments d ON e.department = d.dept_name
WHERE d.dept_id = 3;
```

## 📊 Indexes & Performance

### Index Types and Usage

```sql
-- Primary key index (automatically created)
CREATE TABLE products (
    product_id INT PRIMARY KEY,  -- Clustered index
    name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2)
);

-- Single column index
CREATE INDEX idx_products_category ON products(category);

-- Composite index
CREATE INDEX idx_products_category_price ON products(category, price);

-- Unique index
CREATE UNIQUE INDEX idx_products_name ON products(name);

-- Partial index (PostgreSQL)
CREATE INDEX idx_expensive_products ON products(price) 
WHERE price > 1000;
```

### Query Performance Analysis

```sql
-- Use EXPLAIN to analyze query performance
EXPLAIN ANALYZE
SELECT p.name, p.price
FROM products p
WHERE p.category = 'Electronics'
  AND p.price > 500
ORDER BY p.price DESC;

-- Example output interpretation:
-- Seq Scan on products  (cost=0.00..25.00 rows=5 width=36) (actual time=0.123..0.456 rows=3 loops=1)
--   Filter: ((category = 'Electronics') AND (price > 500))
--   Rows Removed by Filter: 97
-- Planning Time: 0.234 ms
-- Execution Time: 0.567 ms
```

## 🔒 Transactions & ACID

### Transaction Basics

```sql
-- Basic transaction
BEGIN;
    UPDATE employees SET salary = salary * 1.1 WHERE department = 'Engineering';
    INSERT INTO salary_history (emp_id, old_salary, new_salary, change_date)
    SELECT emp_id, salary / 1.1, salary, CURRENT_DATE
    FROM employees WHERE department = 'Engineering';
COMMIT;

-- Transaction with rollback
BEGIN;
    DELETE FROM employees WHERE emp_id = 1;
    -- Oops, wrong employee!
ROLLBACK;  -- Undoes the delete
```

### Isolation Levels

```sql
-- Set transaction isolation level
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

BEGIN;
    SELECT COUNT(*) FROM employees;  -- Sees committed data only
    -- Other transactions can modify data
    SELECT COUNT(*) FROM employees;  -- Might see different count
COMMIT;

-- Serializable isolation (highest level)
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN;
    -- This transaction sees a consistent snapshot
    SELECT AVG(salary) FROM employees;
    UPDATE employees SET salary = salary * 1.1;
COMMIT;
```

## 📋 Best Practices

### Query Writing Best Practices

```sql
-- ✅ Good: Use meaningful aliases
SELECT 
    e.name as employee_name,
    d.dept_name as department,
    p.project_name
FROM employees e
JOIN departments d ON e.department = d.dept_name
JOIN projects p ON d.dept_id = p.dept_id;

-- ❌ Bad: No aliases, unclear intent
SELECT employees.name, departments.dept_name, projects.project_name
FROM employees, departments, projects
WHERE employees.department = departments.dept_name
  AND departments.dept_id = projects.dept_id;

-- ✅ Good: Use EXISTS for existence checks
SELECT name FROM employees e
WHERE EXISTS (
    SELECT 1 FROM projects p 
    JOIN departments d ON p.dept_id = d.dept_id
    WHERE d.dept_name = e.department
);

-- ❌ Bad: Use IN with subquery (can be slower)
SELECT name FROM employees
WHERE department IN (
    SELECT d.dept_name FROM projects p
    JOIN departments d ON p.dept_id = d.dept_id
);
```

### Performance Optimization

```sql
-- ✅ Good: Filter early, join late
WITH high_salary_employees AS (
    SELECT emp_id, name, department
    FROM employees
    WHERE salary > 75000  -- Filter first
)
SELECT hse.name, d.dept_name
FROM high_salary_employees hse
JOIN departments d ON hse.department = d.dept_name;

-- ✅ Good: Use appropriate data types
CREATE TABLE optimized_table (
    id INT NOT NULL,                    -- Not BIGINT if not needed
    status CHAR(1),                     -- Not VARCHAR(50) for single char
    created_date DATE,                  -- Not TIMESTAMP if time not needed
    amount DECIMAL(10,2)                -- Not FLOAT for money
);
```

## 🎯 Interview Focus Areas

### Essential Concepts to Master

1. **JOIN Types**: INNER, LEFT, RIGHT, FULL OUTER, CROSS
2. **Aggregations**: GROUP BY, HAVING, window functions
3. **Subqueries**: Correlated vs non-correlated, EXISTS vs IN
4. **Indexes**: When to use, types, performance impact
5. **Transactions**: ACID properties, isolation levels
6. **Performance**: Query optimization, execution plans

### Common Interview Questions

**Q: What's the difference between WHERE and HAVING?**
```sql
-- WHERE filters rows before grouping
SELECT department, AVG(salary)
FROM employees
WHERE salary > 70000  -- Filter individual rows first
GROUP BY department;

-- HAVING filters groups after grouping
SELECT department, AVG(salary)
FROM employees
GROUP BY department
HAVING AVG(salary) > 70000;  -- Filter groups based on aggregate
```

**Q: Explain the difference between UNION and UNION ALL**
```sql
-- UNION removes duplicates (slower)
SELECT name FROM employees WHERE department = 'Engineering'
UNION
SELECT name FROM employees WHERE salary > 75000;

-- UNION ALL keeps duplicates (faster)
SELECT name FROM employees WHERE department = 'Engineering'
UNION ALL
SELECT name FROM employees WHERE salary > 75000;
```

**Q: How do you find the second highest salary?**
```sql
-- Method 1: Using window functions (preferred)
SELECT DISTINCT salary
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) as rank
    FROM employees
) ranked
WHERE rank = 2;

-- Method 2: Using subquery
SELECT MAX(salary)
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
```

### Practice Exercises

**Exercise 1: Complex Joins**
```sql
-- Find employees working on projects with budgets > $40,000
SELECT DISTINCT
    e.name,
    e.salary,
    p.project_name,
    p.budget
FROM employees e
JOIN departments d ON e.department = d.dept_name
JOIN projects p ON d.dept_id = p.dept_id
WHERE p.budget > 40000
ORDER BY e.salary DESC;
```

**Exercise 2: Window Functions**
```sql
-- Calculate running total of salaries by hire date
SELECT 
    name,
    hire_date,
    salary,
    SUM(salary) OVER (ORDER BY hire_date) as running_total,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_salary_rank
FROM employees
ORDER BY hire_date;
```

## 🚀 Next Steps

After mastering these SQL concepts:

1. **Advanced Topics**: Study [SQL Advanced Database Engineering](./SQL_ADVANCED_DATABASE_ENGINEERING.md)
2. **Practice**: Use [SQL Quick Reference](./SQL_QUICK_REFERENCE.md) for daily operations
3. **Specialization**: Learn database-specific features (PostgreSQL, MySQL, SQL Server)
4. **Integration**: Combine with Python, Spark, and other data tools
5. **Performance**: Master query optimization and database tuning

SQL is the foundation of data engineering - master it well! 🎯