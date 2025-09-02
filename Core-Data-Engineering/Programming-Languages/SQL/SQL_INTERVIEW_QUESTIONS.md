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
JOINs are fundamental SQL operations for combining data from multiple tables, essential for data engineering workflows.

**Conceptual Understanding:**
- **INNER JOIN**: Returns only records that have matching values in both tables (intersection)
- **LEFT JOIN**: Returns all records from the left table, plus matching records from the right table (NULL for non-matches)
- **RIGHT JOIN**: Returns all records from the right table, plus matching records from the left table
- **FULL OUTER JOIN**: Returns all records when there's a match in either table (union)

**Use Cases:**
- **INNER JOIN**: When you need only customers who have placed orders
- **LEFT JOIN**: When you need all customers, regardless of whether they've placed orders
- **Performance**: INNER JOINs are typically faster as they return fewer rows

```sql
-- INNER JOIN - only customers with orders
SELECT c.name, o.order_date FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;

-- LEFT JOIN - all customers, including those without orders  
SELECT c.name, o.order_date FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
```

### 2. Explain the difference between WHERE and HAVING clauses
**Answer:**
These clauses serve different purposes in SQL's logical execution order and are crucial for effective data filtering.

**Conceptual Differences:**
- **WHERE**: Filters individual rows before grouping (row-level filtering)
- **HAVING**: Filters grouped results after aggregation (group-level filtering)
- **Execution Order**: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
- **Performance**: WHERE is faster as it reduces data before expensive grouping operations

**When to Use:**
- **WHERE**: Filter raw data (e.g., "employees with salary > 50000")
- **HAVING**: Filter aggregated results (e.g., "departments with more than 5 employees")

**Data Engineering Context:**
In ETL pipelines, use WHERE for data extraction filtering and HAVING for analytical aggregations.

```sql
-- WHERE: Filter before grouping
SELECT department, COUNT(*) FROM employees 
WHERE salary > 50000 GROUP BY department;

-- HAVING: Filter after grouping
SELECT department, COUNT(*) FROM employees 
GROUP BY department HAVING COUNT(*) > 5;
```

### 3. What are the different types of SQL constraints?
**Answer:**
Constraints enforce data integrity rules at the database level, ensuring data quality and consistency.

**Types and Purposes:**
- **PRIMARY KEY**: Unique identifier for each row (entity integrity)
- **FOREIGN KEY**: Links to primary key in another table (referential integrity)
- **UNIQUE**: Ensures column values are unique (domain integrity)
- **NOT NULL**: Prevents null values (domain integrity)
- **CHECK**: Validates data based on custom conditions (domain integrity)
- **DEFAULT**: Sets default value when none provided

**Data Engineering Benefits:**
- Prevents bad data from entering the system
- Maintains relationships between tables
- Reduces need for application-level validation
- Improves query optimizer performance

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
ACID properties ensure database reliability and data integrity, critical for data engineering systems handling financial, healthcare, or other sensitive data.

- **Atomicity**: All operations in a transaction succeed or fail as a single unit ("all or nothing")
- **Consistency**: Database transitions from one valid state to another, maintaining all constraints and rules
- **Isolation**: Concurrent transactions execute independently without interfering with each other
- **Durability**: Once committed, changes persist permanently even after system crashes or power failures

**Real-world Example**: Bank transfer - debit from account A and credit to account B must both succeed or both fail (atomicity), maintain account balance constraints (consistency), not interfere with other transfers (isolation), and persist after completion (durability).

### 5. What's the difference between DELETE, TRUNCATE, and DROP?
**Answer:**
These commands remove data at different levels with varying performance and safety characteristics.

**Conceptual Differences:**
- **DELETE**: Removes specific rows based on conditions
- **TRUNCATE**: Removes all rows from a table
- **DROP**: Removes the entire table structure and data

**Key Characteristics:**
- **DELETE**: Transactional (can rollback), triggers fire, slower, logs each row
- **TRUNCATE**: Faster, minimal logging, resets identity counters, no triggers
- **DROP**: Removes table from database catalog, frees storage immediately

**Data Engineering Usage:**
- **DELETE**: Data cleanup, removing specific records
- **TRUNCATE**: Clearing staging tables in ETL processes
- **DROP**: Removing temporary tables, schema changes

```sql
DELETE FROM employees WHERE department = 'Sales';  -- Conditional removal
TRUNCATE TABLE temp_data;                          -- Clear all data
DROP TABLE old_table;                              -- Remove table entirely
```

### 6. Explain different types of indexes
**Answer:**
Indexes are database objects that improve query performance by creating shortcuts to data.

**Types and Characteristics:**
- **Clustered Index**: Physically reorders table data (one per table, usually primary key)
- **Non-clustered Index**: Separate structure pointing to data rows (multiple allowed)
- **Composite Index**: Multiple columns (order matters for query optimization)
- **Unique Index**: Enforces uniqueness while providing fast lookups
- **Partial Index**: Only indexes rows meeting specific conditions
- **Covering Index**: Includes additional columns to avoid table lookups

**Performance Impact:**
- **Benefits**: Faster SELECT queries, efficient sorting and grouping
- **Costs**: Slower INSERT/UPDATE/DELETE, additional storage space
- **Strategy**: Index frequently queried columns, avoid over-indexing

```sql
CREATE INDEX idx_customer ON orders(customer_id);           -- Basic
CREATE INDEX idx_customer_date ON orders(customer_id, order_date); -- Composite
CREATE INDEX idx_active_orders ON orders(order_date) WHERE status = 'ACTIVE'; -- Partial
```

### 7. What are aggregate functions? Give examples
**Answer:**
Aggregate functions perform calculations on multiple rows and return a single result, essential for data analysis and reporting.

**Common Functions:**
- **COUNT()**: Number of rows (COUNT(*) includes NULLs, COUNT(column) excludes NULLs)
- **SUM()**: Total of numeric values
- **AVG()**: Average of numeric values (excludes NULLs)
- **MIN()/MAX()**: Minimum/maximum values
- **STDDEV()**: Standard deviation for statistical analysis

**Data Engineering Applications:**
- Data quality checks (counting nulls, duplicates)
- Business metrics calculation (revenue, averages)
- Statistical analysis for data profiling
- ETL validation (comparing source vs target counts)

**Important Notes:**
- Most aggregate functions ignore NULL values
- Use with GROUP BY for category-wise aggregations
- Can be used in HAVING clauses for filtering groups

```sql
SELECT COUNT(*) as total_records, COUNT(DISTINCT customer_id) as unique_customers,
       SUM(order_amount) as total_revenue, AVG(order_amount) as average_order
FROM orders;
```

### 8. What are the different types of SQL commands?
**Answer:**
SQL commands are categorized by their purpose and functionality in database operations.

**Command Categories:**
- **DDL (Data Definition Language)**: CREATE, ALTER, DROP, TRUNCATE
  - Purpose: Define and modify database structure
  - Usage: Schema changes, table creation, index management

- **DML (Data Manipulation Language)**: INSERT, UPDATE, DELETE, SELECT
  - Purpose: Manipulate data within tables
  - Usage: CRUD operations, data retrieval

- **DCL (Data Control Language)**: GRANT, REVOKE
  - Purpose: Control access permissions
  - Usage: User management, security

- **TCL (Transaction Control Language)**: COMMIT, ROLLBACK, SAVEPOINT
  - Purpose: Manage database transactions
  - Usage: Ensure data consistency, handle errors

**Data Engineering Context:**
DDL for pipeline setup, DML for data processing, DCL for security, TCL for data integrity.

### 9. Explain the SQL execution order
**Answer:**
Understanding SQL's logical execution order is crucial for writing efficient queries and debugging performance issues.

**Logical Execution Order:**
1. **FROM** - Identify and join tables
2. **WHERE** - Filter individual rows
3. **GROUP BY** - Group rows for aggregation
4. **HAVING** - Filter grouped results
5. **SELECT** - Choose and compute columns
6. **ORDER BY** - Sort the result set
7. **LIMIT/OFFSET** - Limit number of results

**Why This Matters:**
- **Performance**: WHERE filters before expensive operations like GROUP BY
- **Aliases**: Can't use SELECT aliases in WHERE (not executed yet)
- **Optimization**: Query optimizer uses this order for execution planning
- **Debugging**: Understanding order helps identify why queries fail

**Data Engineering Impact:**
Optimize ETL queries by filtering early (WHERE) before aggregating (GROUP BY).

### 10. What is the difference between CHAR and VARCHAR?
**Answer:**
CHAR and VARCHAR are string data types with different storage and performance characteristics.

**Key Differences:**
- **CHAR(n)**: Fixed-length, always uses n bytes, pads with spaces
- **VARCHAR(n)**: Variable-length, uses only needed space plus length overhead

**Performance Considerations:**
- **CHAR**: Faster for fixed-size data (codes, flags), predictable storage
- **VARCHAR**: More storage efficient, better for variable-length text

**Use Cases:**
- **CHAR**: Country codes (US, UK), status flags (Y/N), fixed IDs
- **VARCHAR**: Names, descriptions, email addresses, variable text

**Data Engineering Best Practices:**
- Use CHAR for lookup tables with fixed codes
- Use VARCHAR for user-generated content
- Consider TEXT for very long strings

```sql
CREATE TABLE codes (country_code CHAR(2));     -- Always 2 characters
CREATE TABLE users (name VARCHAR(100));        -- Variable length names
```

### 11. Explain NULL values and how to handle them
**Answer:**
NULL represents missing, unknown, or inapplicable data in databases, requiring special handling in queries.

**NULL Characteristics:**
- **Not equal to anything**: NULL ≠ NULL (use IS NULL, not = NULL)
- **Three-valued logic**: TRUE, FALSE, UNKNOWN
- **Aggregate behavior**: Most functions ignore NULLs (except COUNT(*))
- **Arithmetic**: Any operation with NULL returns NULL

**Handling Strategies:**
- **COALESCE()**: Return first non-NULL value
- **NULLIF()**: Return NULL if values are equal
- **CASE WHEN**: Conditional logic for NULL handling
- **IS NULL/IS NOT NULL**: Proper NULL comparison

**Data Engineering Considerations:**
- Data quality: High NULL percentages indicate data issues
- ETL processing: Handle NULLs during transformation
- Analytics: Decide whether to exclude or substitute NULLs

```sql
SELECT name, COALESCE(bonus, 0) as bonus_amount,
       CASE WHEN bonus IS NULL THEN 'No bonus' ELSE 'Has bonus' END as status
FROM employees WHERE salary IS NOT NULL;
```

### 12. What are SQL data types and their categories?
**Answer:**
SQL data types define the kind of data that can be stored in columns, affecting storage, performance, and operations.

**Numeric Types:**
- **INTEGER/BIGINT**: Whole numbers (use BIGINT for large values)
- **DECIMAL/NUMERIC**: Exact precision (financial data)
- **FLOAT/DOUBLE**: Approximate precision (scientific calculations)

**String Types:**
- **CHAR**: Fixed-length strings
- **VARCHAR**: Variable-length strings
- **TEXT/CLOB**: Large text objects

**Date/Time Types:**
- **DATE**: Date only (YYYY-MM-DD)
- **TIME**: Time only (HH:MM:SS)
- **TIMESTAMP**: Date and time with timezone support

**Other Types:**
- **BOOLEAN**: TRUE/FALSE/NULL
- **BINARY/BLOB**: Binary data (images, files)
- **JSON**: Structured data (PostgreSQL, MySQL)
- **ARRAY**: Array data (PostgreSQL)

**Selection Criteria:**
Choose based on data nature, storage requirements, and query patterns.

### 13. Explain the concept of database transactions
**Answer:**
Transactions are logical units of work that ensure data consistency and integrity through ACID properties.

**ACID Properties:**
- **Atomicity**: All operations succeed or fail together ("all or nothing")
- **Consistency**: Database moves from one valid state to another
- **Isolation**: Concurrent transactions don't interfere with each other
- **Durability**: Committed changes persist permanently

**Transaction States:**
- **BEGIN**: Start transaction
- **COMMIT**: Make changes permanent
- **ROLLBACK**: Undo all changes
- **SAVEPOINT**: Create rollback points within transactions

**Data Engineering Applications:**
- ETL processes: Ensure data consistency during loads
- Batch processing: Group related operations
- Error handling: Rollback on failures
- Data migration: Maintain integrity during transfers

**Best Practices:**
- Keep transactions short to avoid locks
- Handle errors with proper rollback logic
- Use appropriate isolation levels

```sql
BEGIN TRANSACTION;
    UPDATE accounts SET balance = balance - 1000 WHERE account_id = 1;
    UPDATE accounts SET balance = balance + 1000 WHERE account_id = 2;
COMMIT; -- or ROLLBACK on error
```

### 14. What is the difference between RANK() and DENSE_RANK()?
**Answer:**
These window functions assign rankings to rows, but handle ties differently.

**Key Differences:**
- **RANK()**: Leaves gaps after ties (1, 1, 3, 4)
- **DENSE_RANK()**: No gaps after ties (1, 1, 2, 3)
- **ROW_NUMBER()**: Always unique, arbitrary order for ties (1, 2, 3, 4)

**Use Cases:**
- **RANK()**: Traditional ranking (Olympic medals, competition standings)
- **DENSE_RANK()**: Category rankings where gaps don't matter
- **ROW_NUMBER()**: Pagination, unique identifiers

**Data Engineering Applications:**
- Top-N analysis per group
- Data deduplication (ROW_NUMBER() = 1)
- Performance rankings and percentiles
- Quality scoring systems

```sql
SELECT name, salary,
    RANK() OVER (ORDER BY salary DESC) as rank_with_gaps,
    DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank,
    ROW_NUMBER() OVER (ORDER BY salary DESC) as row_num
FROM employees;
-- Result: Alice(100k):1,1,1  Bob(100k):1,1,2  Carol(90k):3,2,3
```

### 15. How do you handle case-sensitive searches?
**Answer:**
Case sensitivity in SQL depends on database collation settings and requires specific techniques for consistent behavior.

**Database Behavior:**
- **MySQL**: Case-insensitive by default (depends on collation)
- **PostgreSQL**: Case-sensitive by default
- **SQL Server**: Depends on collation settings
- **Oracle**: Case-sensitive by default

**Techniques:**
- **UPPER()/LOWER()**: Convert to same case for comparison
- **ILIKE**: Case-insensitive LIKE (PostgreSQL)
- **BINARY**: Force case-sensitive comparison (MySQL)
- **Collation**: Specify comparison rules explicitly

**Performance Considerations:**
- Functions on columns prevent index usage
- Create functional indexes: `CREATE INDEX idx_name_lower ON customers(LOWER(name))`
- Use full-text search for complex text matching

**Data Engineering Best Practices:**
- Standardize case during ETL processes
- Use consistent collation across environments
- Document case sensitivity requirements

```sql
-- Case-insensitive search (portable)
SELECT * FROM customers WHERE UPPER(name) = UPPER('john');
-- PostgreSQL specific
SELECT * FROM customers WHERE name ILIKE '%john%';
```

## Intermediate Level Questions (16-35)

### 16. What are window functions and how do they differ from aggregate functions?
**Answer:**
Window functions perform calculations across related rows while preserving individual row details, making them powerful for analytical queries.

**Conceptual Differences:**
- **Aggregate Functions**: Collapse multiple rows into single result per group
- **Window Functions**: Maintain all original rows while adding calculated columns
- **Grouping**: Aggregates use GROUP BY, windows use OVER clause
- **Result Set**: Aggregates reduce rows, windows preserve row count

**Common Window Functions:**
- **Ranking**: ROW_NUMBER(), RANK(), DENSE_RANK()
- **Analytical**: LAG(), LEAD(), FIRST_VALUE(), LAST_VALUE()
- **Aggregate**: SUM(), AVG(), COUNT() with OVER clause
- **Statistical**: NTILE(), PERCENT_RANK(), CUME_DIST()

**Data Engineering Applications:**
- Running totals and moving averages
- Ranking and percentile calculations
- Time-series analysis (lag/lead comparisons)
- Deduplication (ROW_NUMBER() = 1)

**Performance**: Often more efficient than self-joins for analytical queries

```sql
-- Window function - keeps all rows
SELECT name, salary, 
       AVG(salary) OVER (PARTITION BY department) as dept_avg,
       RANK() OVER (ORDER BY salary DESC) as salary_rank
FROM employees;
``` ### 17. Explain different types of JOINs with examples
**Answer:**
JOINs combine data from multiple tables based on relationships, each type serving different analytical needs.

**JOIN Types and Use Cases:**
- **INNER JOIN**: Only matching records (customers with orders)
- **LEFT JOIN**: All left table records + matches (all customers, with/without orders)
- **RIGHT JOIN**: All right table records + matches (all orders, with/without customer info)
- **FULL OUTER JOIN**: All records from both tables (complete dataset)
- **CROSS JOIN**: Cartesian product (every combination)
- **SELF JOIN**: Table joined to itself (hierarchical data)

**Performance Considerations:**
- **INNER JOIN**: Fastest, smallest result set
- **OUTER JOINs**: Slower, larger result sets
- **Index Strategy**: Index join columns for better performance
- **Join Order**: Query optimizer determines optimal sequence

**Data Engineering Applications:**
- Data integration from multiple sources
- Fact-dimension table relationships
- Hierarchical data processing
- Data quality checks (finding orphaned records)

```sql
-- Most common patterns
SELECT c.name, o.amount FROM customers c
INNER JOIN orders o ON c.id = o.customer_id;  -- Only customers with orders

SELECT c.name, COALESCE(o.amount, 0) FROM customers c  
LEFT JOIN orders o ON c.id = o.customer_id;   -- All customers
```

### 18. What are CTEs (Common Table Expressions) and when to use them?
**Answer:**
CTEs create temporary named result sets that improve query readability and enable recursive operations.

**Types and Benefits:**
- **Simple CTE**: Named subquery for better readability
- **Recursive CTE**: Handle hierarchical data (org charts, categories)
- **Multiple CTEs**: Break complex logic into manageable steps
- **Reusability**: Reference same CTE multiple times in query

**Advantages over Subqueries:**
- **Readability**: Named, logical query structure
- **Maintainability**: Easier to debug and modify
- **Performance**: Can be more efficient than repeated subqueries
- **Recursion**: Only way to handle recursive queries in standard SQL

**Data Engineering Use Cases:**
- Data transformation pipelines
- Hierarchical data processing (bill of materials, org structures)
- Complex analytical queries
- Data quality checks with multiple steps

**Best Practices:**
- Use descriptive CTE names
- Keep CTEs focused on single purpose
- Consider materialized views for frequently used CTEs

```sql
-- Simple CTE for readability
WITH high_earners AS (
    SELECT department, name, salary FROM employees WHERE salary > 80000
)
SELECT department, COUNT(*) FROM high_earners GROUP BY department;

-- Recursive CTE for hierarchy
WITH RECURSIVE org_chart AS (
    SELECT employee_id, name, manager_id, 1 as level FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.employee_id, e.name, e.manager_id, oc.level + 1
    FROM employees e JOIN org_chart oc ON e.manager_id = oc.employee_id
)
SELECT * FROM org_chart ORDER BY level;
```

### 19. Explain UNION vs UNION ALL
**Answer:**
UNION operations combine result sets from multiple queries, with different handling of duplicate rows.

**Key Differences:**
- **UNION**: Removes duplicate rows, performs implicit DISTINCT
- **UNION ALL**: Keeps all rows including duplicates
- **Performance**: UNION ALL is faster (no deduplication overhead)
- **Use Cases**: UNION for unique results, UNION ALL for complete datasets

**Requirements:**
- Same number of columns in all queries
- Compatible data types in corresponding positions
- Column names from first query used in result

**Data Engineering Applications:**
- Combining data from multiple sources/tables
- Historical vs current data integration
- Partitioned table queries
- Data migration and consolidation

**Performance Considerations:**
- UNION requires sorting for deduplication
- UNION ALL is preferred when duplicates are acceptable
- Consider using DISTINCT separately if needed

**Best Practice**: Use UNION ALL unless you specifically need to remove duplicates

```sql
-- UNION - removes duplicates (slower)
SELECT name FROM customers UNION SELECT name FROM suppliers;

-- UNION ALL - keeps duplicates (faster)
SELECT customer_id, 'current' as source FROM current_orders
UNION ALL  
SELECT customer_id, 'historical' as source FROM historical_orders;
```

### 20. What are subqueries and their types?
**Answer:**
```sql
-- Scalar subquery - returns single value
SELECT name, salary,
       salary - (SELECT AVG(salary) FROM employees) as salary_diff
FROM employees;

-- Correlated subquery - references outer query
SELECT name, salary
FROM employees e1
WHERE salary > (SELECT AVG(salary) 
                FROM employees e2 
                WHERE e2.department = e1.department);

-- EXISTS subquery - checks for existence
SELECT name
FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);

-- IN subquery - membership test
SELECT name
FROM employees
WHERE department_id IN (SELECT id FROM departments WHERE location = 'New York');

-- ANY/ALL subqueries
SELECT name, salary
FROM employees
WHERE salary > ANY (SELECT salary FROM employees WHERE department = 'Sales');

SELECT name, salary
FROM employees
WHERE salary > ALL (SELECT salary FROM employees WHERE department = 'Sales');
``` - keeps all rows, adds calculated column
SELECT 
    name,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department) as dept_avg_salary,
    salary - AVG(salary) OVER (PARTITION BY department) as salary_diff_from_avg,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank
FROM employees;

-- Running totals and moving averages
SELECT 
    order_date,
    order_amount,
    SUM(order_amount) OVER (ORDER BY order_date ROWS UNBOUNDED PRECEDING) as running_total,
    AVG(order_amount) OVER (ORDER BY order_date ROWS 2 PRECEDING) as moving_avg_3_days
FROM orders
ORDER BY order_date; - keeps all rows
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
### 21. How do you handle duplicate records?
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

-- Remove duplicates using DISTINCT
SELECT DISTINCT customer_id, product_id, order_date
FROM orders;

-- Keep latest record per group
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) as rn
    FROM orders
) ranked
WHERE rn = 1;
```

### 22. Explain database normalization and its forms
**Answer:**
Normalization reduces data redundancy and improves data integrity.

**1NF (First Normal Form):**
- Atomic values (no repeating groups)
- Each column contains single value

**2NF (Second Normal Form):**
- Must be in 1NF
- No partial dependencies on composite primary key

**3NF (Third Normal Form):**
- Must be in 2NF
- No transitive dependencies

```sql
-- Unnormalized table
CREATE TABLE orders_bad (
    order_id INT,
    customer_name VARCHAR(100),
    customer_address VARCHAR(200),
    product1 VARCHAR(50),
    product2 VARCHAR(50),
    product3 VARCHAR(50)
);

-- Normalized tables (3NF)
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    address VARCHAR(200)
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    name VARCHAR(50),
    price DECIMAL(10,2)
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
```

### 23. What are stored procedures and functions?
**Answer:**
```sql
-- Stored Procedure
CREATE OR REPLACE PROCEDURE update_employee_salary(
    emp_id INT,
    new_salary DECIMAL(10,2)
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE employees 
    SET salary = new_salary,
        updated_date = CURRENT_TIMESTAMP
    WHERE employee_id = emp_id;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Employee % not found', emp_id;
    END IF;
END;
$$;

-- Call procedure
CALL update_employee_salary(123, 75000.00);

-- Function
CREATE OR REPLACE FUNCTION calculate_bonus(
    emp_salary DECIMAL(10,2),
    performance_rating INT
)
RETURNS DECIMAL(10,2)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN CASE 
        WHEN performance_rating >= 4 THEN emp_salary * 0.15
        WHEN performance_rating >= 3 THEN emp_salary * 0.10
        WHEN performance_rating >= 2 THEN emp_salary * 0.05
        ELSE 0
    END;
END;
$$;

-- Use function
SELECT name, salary, 
       calculate_bonus(salary, performance_rating) as bonus
FROM employees;
```

### 24. Explain triggers and their types
**Answer:**
```sql
-- BEFORE INSERT trigger
CREATE OR REPLACE FUNCTION audit_employee_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO employee_audit (employee_id, action, timestamp)
        VALUES (NEW.employee_id, 'INSERT', NOW());
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO employee_audit (employee_id, action, old_salary, new_salary, timestamp)
        VALUES (NEW.employee_id, 'UPDATE', OLD.salary, NEW.salary, NOW());
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO employee_audit (employee_id, action, timestamp)
        VALUES (OLD.employee_id, 'DELETE', NOW());
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Create triggers
CREATE TRIGGER employee_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON employees
    FOR EACH ROW EXECUTE FUNCTION audit_employee_changes();

-- BEFORE UPDATE trigger for validation
CREATE OR REPLACE FUNCTION validate_salary_increase()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.salary > OLD.salary * 1.5 THEN
        RAISE EXCEPTION 'Salary increase cannot exceed 50%';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER salary_validation_trigger
    BEFORE UPDATE ON employees
    FOR EACH ROW EXECUTE FUNCTION validate_salary_increase();
```

### 25. How do you optimize SQL queries?
**Answer:**
```sql
-- 1. Use appropriate indexes
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- 2. Avoid SELECT *
SELECT customer_id, order_date, amount FROM orders;  -- Good
SELECT * FROM orders;  -- Avoid

-- 3. Use WHERE clause effectively
SELECT * FROM orders WHERE order_date >= '2023-01-01';  -- Good
SELECT * FROM orders WHERE YEAR(order_date) = 2023;    -- Avoid (not sargable)

-- 4. Use EXISTS instead of IN for large datasets
SELECT * FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);

-- 5. Use LIMIT for large result sets
SELECT * FROM orders ORDER BY order_date DESC LIMIT 100;

-- 6. Optimize JOINs
-- Use smaller table as driving table
SELECT c.name, o.amount
FROM small_customers c
JOIN large_orders o ON c.id = o.customer_id;

-- 7. Use UNION ALL instead of UNION when duplicates are acceptable
SELECT name FROM customers
UNION ALL
SELECT name FROM suppliers;
```

### 26. What is the difference between clustered and non-clustered indexes?
**Answer:**
**Clustered Index:**
- Physically reorders table data
- One per table (usually primary key)
- Faster for range queries
- Slower for inserts/updates

**Non-clustered Index:**
- Separate structure pointing to data rows
- Multiple per table allowed
- Faster for exact matches
- Additional storage overhead

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

-- Query execution plans will show index usage
EXPLAIN SELECT * FROM orders WHERE customer_id = 123;
```

### 27. Explain CASE statements and their usage
**Answer:**
```sql
-- Simple CASE
SELECT name, salary,
    CASE department
        WHEN 'Sales' THEN salary * 1.1
        WHEN 'Engineering' THEN salary * 1.15
        WHEN 'Marketing' THEN salary * 1.05
        ELSE salary
    END as adjusted_salary
FROM employees;

-- Searched CASE
SELECT name, salary,
    CASE 
        WHEN salary >= 100000 THEN 'Senior'
        WHEN salary >= 70000 THEN 'Mid-level'
        WHEN salary >= 40000 THEN 'Junior'
        ELSE 'Entry-level'
    END as level,
    CASE 
        WHEN performance_rating >= 4 THEN 'Excellent'
        WHEN performance_rating >= 3 THEN 'Good'
        WHEN performance_rating >= 2 THEN 'Satisfactory'
        ELSE 'Needs Improvement'
    END as performance
FROM employees;

-- CASE in WHERE clause
SELECT * FROM orders
WHERE 
    CASE 
        WHEN EXTRACT(MONTH FROM order_date) IN (11, 12) THEN amount > 1000
        ELSE amount > 500
    END;

-- CASE for conditional aggregation
SELECT 
    department,
    COUNT(*) as total_employees,
    COUNT(CASE WHEN salary > 80000 THEN 1 END) as high_earners,
    COUNT(CASE WHEN performance_rating >= 4 THEN 1 END) as top_performers
FROM employees
GROUP BY department;
```

### 28. What are views and materialized views?
**Answer:**
```sql
-- Regular View - virtual table
CREATE VIEW high_value_customers AS
SELECT c.customer_id, c.name, SUM(o.amount) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING SUM(o.amount) > 10000;

-- Use view
SELECT * FROM high_value_customers WHERE name LIKE 'A%';

-- Materialized View - physically stored
CREATE MATERIALIZED VIEW monthly_sales_summary AS
SELECT 
    DATE_TRUNC('month', order_date) as month,
    COUNT(*) as order_count,
    SUM(amount) as total_sales,
    AVG(amount) as avg_order_value
FROM orders
GROUP BY DATE_TRUNC('month', order_date);

-- Refresh materialized view
REFRESH MATERIALIZED VIEW monthly_sales_summary;

-- Updatable view
CREATE VIEW active_employees AS
SELECT employee_id, name, salary, department
FROM employees
WHERE status = 'ACTIVE'
WITH CHECK OPTION;

-- Updates through view
UPDATE active_employees SET salary = 85000 WHERE employee_id = 123;
```

### 29. How do you handle date and time operations?
**Answer:**
```sql
-- Date arithmetic
SELECT 
    order_date,
    order_date + INTERVAL '30 days' as due_date,
    order_date - INTERVAL '1 week' as week_ago,
    AGE(CURRENT_DATE, order_date) as order_age
FROM orders;

-- Date functions
SELECT 
    EXTRACT(YEAR FROM order_date) as year,
    EXTRACT(MONTH FROM order_date) as month,
    EXTRACT(DAY FROM order_date) as day,
    EXTRACT(DOW FROM order_date) as day_of_week,
    DATE_TRUNC('month', order_date) as month_start,
    DATE_PART('quarter', order_date) as quarter
FROM orders;

-- Date formatting
SELECT 
    TO_CHAR(order_date, 'YYYY-MM-DD') as formatted_date,
    TO_CHAR(order_date, 'Month DD, YYYY') as readable_date,
    TO_CHAR(created_timestamp, 'YYYY-MM-DD HH24:MI:SS') as timestamp_str
FROM orders;

-- Time zone handling
SELECT 
    created_timestamp AT TIME ZONE 'UTC' as utc_time,
    created_timestamp AT TIME ZONE 'America/New_York' as ny_time,
    CURRENT_TIMESTAMP as local_time,
    NOW() AT TIME ZONE 'UTC' as current_utc
FROM orders;

-- Date ranges and filtering
SELECT * FROM orders
WHERE order_date BETWEEN '2023-01-01' AND '2023-12-31'
  AND EXTRACT(DOW FROM order_date) NOT IN (0, 6);  -- Exclude weekends
```

### 30. Explain string functions and operations
**Answer:**
```sql
-- String manipulation
SELECT 
    UPPER(name) as uppercase_name,
    LOWER(email) as lowercase_email,
    INITCAP(address) as proper_case_address,
    LENGTH(description) as desc_length,
    TRIM(BOTH ' ' FROM name) as trimmed_name
FROM customers;

-- String extraction and modification
SELECT 
    SUBSTRING(phone FROM 1 FOR 3) as area_code,
    LEFT(name, 10) as short_name,
    RIGHT(email, 10) as email_suffix,
    REPLACE(phone, '-', '') as clean_phone,
    CONCAT(first_name, ' ', last_name) as full_name
FROM customers;

-- Pattern matching
SELECT * FROM customers
WHERE name LIKE 'John%'           -- Starts with 'John'
   OR email LIKE '%@gmail.com'    -- Ends with '@gmail.com'
   OR phone ~ '^[0-9]{3}-[0-9]{3}-[0-9]{4}$';  -- Regex pattern

-- String aggregation
SELECT 
    department,
    STRING_AGG(name, ', ' ORDER BY name) as employee_list,
    ARRAY_AGG(salary ORDER BY salary DESC) as salary_array
FROM employees
GROUP BY department;

-- JSON string operations
SELECT 
    data->>'name' as extracted_name,
    data->'address'->>'city' as city,
    JSON_EXTRACT_PATH_TEXT(data, 'contact', 'email') as email
FROM user_profiles
WHERE data ? 'active';  -- Check if JSON key exists
```

### 31. What are table partitioning strategies?
**Answer:**
```sql
-- Range partitioning by date
CREATE TABLE orders (
    order_id SERIAL,
    customer_id INT,
    order_date DATE,
    amount DECIMAL(10,2)
) PARTITION BY RANGE (order_date);

-- Create partitions
CREATE TABLE orders_2023_q1 PARTITION OF orders
    FOR VALUES FROM ('2023-01-01') TO ('2023-04-01');

CREATE TABLE orders_2023_q2 PARTITION OF orders
    FOR VALUES FROM ('2023-04-01') TO ('2023-07-01');

-- Hash partitioning
CREATE TABLE customers (
    customer_id SERIAL,
    name VARCHAR(100),
    email VARCHAR(100)
) PARTITION BY HASH (customer_id);

CREATE TABLE customers_p1 PARTITION OF customers
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);

CREATE TABLE customers_p2 PARTITION OF customers
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);

-- List partitioning
CREATE TABLE sales (
    sale_id SERIAL,
    region VARCHAR(20),
    amount DECIMAL(10,2)
) PARTITION BY LIST (region);

CREATE TABLE sales_north PARTITION OF sales
    FOR VALUES IN ('North', 'Northeast', 'Northwest');

CREATE TABLE sales_south PARTITION OF sales
    FOR VALUES IN ('South', 'Southeast', 'Southwest');
```

### 32. How do you implement data validation in SQL?
**Answer:**
```sql
-- Check constraints
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    salary DECIMAL(10,2) CHECK (salary > 0 AND salary <= 1000000),
    hire_date DATE CHECK (hire_date <= CURRENT_DATE),
    department VARCHAR(50) CHECK (department IN ('Sales', 'Engineering', 'Marketing', 'HR')),
    age INT CHECK (age BETWEEN 18 AND 65)
);

-- Domain constraints
CREATE DOMAIN email_type AS VARCHAR(100)
CHECK (VALUE ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

CREATE DOMAIN phone_type AS VARCHAR(15)
CHECK (VALUE ~ '^\+?[1-9]\d{1,14}$');

CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    email email_type,
    phone phone_type
);

-- Validation functions
CREATE OR REPLACE FUNCTION validate_credit_card(card_number TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    -- Luhn algorithm implementation
    RETURN LENGTH(card_number) BETWEEN 13 AND 19 
           AND card_number ~ '^[0-9]+$';
END;
$$ LANGUAGE plpgsql;

-- Use in check constraint
ALTER TABLE payments 
ADD CONSTRAINT valid_card_number 
CHECK (validate_credit_card(card_number));
```

### 33. Explain transaction isolation levels
**Answer:**
Transaction isolation levels control how transactions interact with each other:

**READ UNCOMMITTED:**
- Lowest isolation level
- Allows dirty reads, non-repeatable reads, phantom reads

**READ COMMITTED:**
- Default in most databases
- Prevents dirty reads
- Allows non-repeatable reads and phantom reads

**REPEATABLE READ:**
- Prevents dirty reads and non-repeatable reads
- Allows phantom reads

**SERIALIZABLE:**
- Highest isolation level
- Prevents all phenomena
- May cause more deadlocks

```sql
-- Set isolation level
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- Example of isolation level effects
-- Session 1
BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;
SELECT balance FROM accounts WHERE account_id = 1;  -- Returns 1000

-- Session 2 (concurrent)
BEGIN TRANSACTION;
UPDATE accounts SET balance = 1500 WHERE account_id = 1;
COMMIT;

-- Session 1 continues
SELECT balance FROM accounts WHERE account_id = 1;  -- Returns 1500 (non-repeatable read)
COMMIT;

-- Serializable example
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SELECT COUNT(*) FROM orders WHERE order_date = CURRENT_DATE;
-- If another transaction inserts orders with today's date,
-- this transaction may fail with serialization error
COMMIT;
```

### 34. What are database locks and their types?
**Answer:**
```sql
-- Explicit locking
BEGIN TRANSACTION;

-- Shared lock (read lock)
SELECT * FROM accounts WHERE account_id = 1 FOR SHARE;

-- Exclusive lock (write lock)
SELECT * FROM accounts WHERE account_id = 1 FOR UPDATE;

-- Lock specific rows
UPDATE accounts 
SET balance = balance - 100 
WHERE account_id = 1;  -- Implicit exclusive lock

COMMIT;

-- Lock timeout handling
SET lock_timeout = '5s';

-- Deadlock example and prevention
-- Session 1
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;
COMMIT;

-- Session 2 (potential deadlock)
BEGIN;
UPDATE accounts SET balance = balance - 50 WHERE account_id = 2;
UPDATE accounts SET balance = balance + 50 WHERE account_id = 1;
COMMIT;

-- Prevent deadlock by consistent ordering
-- Both sessions should lock accounts in same order (by account_id)
```

### 35. How do you handle hierarchical data in SQL?
**Answer:**
```sql
-- Adjacency List Model
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    parent_id INT REFERENCES categories(id)
);

-- Find all subcategories using recursive CTE
WITH RECURSIVE category_tree AS (
    -- Base case: root categories
    SELECT id, name, parent_id, 0 as level, ARRAY[id] as path
    FROM categories
    WHERE parent_id IS NULL
    
    UNION ALL
    
    -- Recursive case: child categories
    SELECT c.id, c.name, c.parent_id, ct.level + 1, ct.path || c.id
    FROM categories c
    JOIN category_tree ct ON c.parent_id = ct.id
    WHERE NOT c.id = ANY(ct.path)  -- Prevent cycles
)
SELECT 
    REPEAT('  ', level) || name as indented_name,
    level,
    path
FROM category_tree
ORDER BY path;

-- Nested Set Model (alternative approach)
CREATE TABLE categories_nested (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    lft INT,
    rgt INT
);

-- Find all descendants
SELECT child.*
FROM categories_nested parent, categories_nested child
WHERE child.lft BETWEEN parent.lft AND parent.rgt
  AND parent.id = 1;  -- Parent category ID

-- Find path to root
SELECT parent.*
FROM categories_nested parent, categories_nested child
WHERE child.lft BETWEEN parent.lft AND parent.rgt
  AND child.id = 5  -- Child category ID
ORDER BY parent.lft;

-- Materialized Path Model
CREATE TABLE categories_path (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    path VARCHAR(500)  -- e.g., '/1/3/7/'
);

-- Find all descendants
SELECT * FROM categories_path
WHERE path LIKE '/1/3/%';

-- Find ancestors
SELECT * FROM categories_path c1
WHERE '/1/3/7/' LIKE c1.path || '%';
```

## Advanced Level Questions (36-50)

### 36. Explain query execution plans and how to read them
**Answer:**
Query execution plans show how the database engine executes a query, crucial for performance optimization.

```sql
-- PostgreSQL execution plan
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) 
SELECT c.name, COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.created_date >= '2023-01-01'
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) > 5
ORDER BY order_count DESC;

-- Key elements to analyze:
-- 1. Node types: Seq Scan, Index Scan, Hash Join, etc.
-- 2. Cost estimates: startup cost..total cost
-- 3. Actual time: actual time=start..end
-- 4. Rows: rows=estimated vs actual
-- 5. Buffers: shared hit/read/written

-- SQL Server execution plan
SET STATISTICS IO ON;
SET STATISTICS TIME ON;

SELECT c.name, COUNT(o.order_id)
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.created_date >= '2023-01-01'
GROUP BY c.customer_id, c.name;

-- Common plan operators:
-- - Table Scan: reads entire table
-- - Index Seek: uses index efficiently
-- - Index Scan: reads entire index
-- - Hash Match: hash join operation
-- - Nested Loops: nested loop join
-- - Sort: sorting operation
```

### 37. What are database statistics and how do they affect performance?
**Answer:**
Database statistics help the query optimizer make informed decisions about execution plans.

```sql
-- Update statistics (PostgreSQL)
ANALYZE customers;
ANALYZE orders;

-- Detailed statistics
ANALYZE VERBOSE customers;

-- Auto-vacuum and statistics
-- PostgreSQL automatically updates statistics, but manual updates may be needed
-- after large data changes

-- View statistics information
SELECT 
    schemaname,
    tablename,
    n_tup_ins,
    n_tup_upd,
    n_tup_del,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables;

-- SQL Server statistics
UPDATE STATISTICS customers WITH FULLSCAN;

-- View statistics information
SELECT 
    s.name AS statistics_name,
    c.name AS column_name,
    s.stats_date AS last_updated
FROM sys.stats s
JOIN sys.stats_columns sc ON s.object_id = sc.object_id AND s.stats_id = sc.stats_id
JOIN sys.columns c ON sc.object_id = c.object_id AND sc.column_id = c.column_id
WHERE s.object_id = OBJECT_ID('customers');

-- Histogram and density information
DBCC SHOW_STATISTICS('customers', 'IX_customers_created_date');
```

### 38. How do you implement slowly changing dimensions (SCD)?
**Answer:**
SCDs handle changes to dimension data in data warehouses.

```sql
-- SCD Type 1: Overwrite (no history)
UPDATE customer_dim 
SET address = 'New Address',
    phone = 'New Phone',
    updated_date = CURRENT_TIMESTAMP
WHERE customer_id = 123;

-- SCD Type 2: Add new record (full history)
CREATE TABLE customer_dim_scd2 (
    surrogate_key SERIAL PRIMARY KEY,
    customer_id INT,
    name VARCHAR(100),
    address VARCHAR(200),
    phone VARCHAR(20),
    effective_date DATE,
    expiry_date DATE,
    is_current BOOLEAN,
    version_number INT
);

-- Insert new version
INSERT INTO customer_dim_scd2 (
    customer_id, name, address, phone, 
    effective_date, expiry_date, is_current, version_number
)
SELECT 
    customer_id, name, 'New Address', 'New Phone',
    CURRENT_DATE, '9999-12-31', TRUE, 
    COALESCE(MAX(version_number), 0) + 1
FROM customer_dim_scd2
WHERE customer_id = 123;

-- Update previous version
UPDATE customer_dim_scd2 
SET expiry_date = CURRENT_DATE - 1,
    is_current = FALSE
WHERE customer_id = 123 
  AND is_current = TRUE 
  AND surrogate_key != (SELECT MAX(surrogate_key) 
                        FROM customer_dim_scd2 
                        WHERE customer_id = 123);

-- SCD Type 3: Add new column (limited history)
ALTER TABLE customer_dim 
ADD COLUMN previous_address VARCHAR(200),
ADD COLUMN address_change_date DATE;

UPDATE customer_dim 
SET previous_address = address,
    address = 'New Address',
    address_change_date = CURRENT_DATE
WHERE customer_id = 123;

-- SCD Type 4: History table
CREATE TABLE customer_dim_history (
    customer_id INT,
    name VARCHAR(100),
    address VARCHAR(200),
    phone VARCHAR(20),
    change_date DATE,
    change_type VARCHAR(10)
);

-- Trigger for history tracking
CREATE OR REPLACE FUNCTION track_customer_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE' THEN
        INSERT INTO customer_dim_history
        SELECT OLD.*, CURRENT_DATE, 'UPDATE';
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO customer_dim_history
        SELECT OLD.*, CURRENT_DATE, 'DELETE';
    END IF;
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;
```

### 39. Explain data warehousing concepts: Facts, Dimensions, Star Schema
**Answer:**
```sql
-- Dimension Tables (descriptive attributes)
CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,  -- Surrogate key
    customer_id INT,                  -- Natural key
    name VARCHAR(100),
    address VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    customer_segment VARCHAR(20),
    effective_date DATE,
    expiry_date DATE,
    is_current BOOLEAN
);

CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id INT,
    product_name VARCHAR(100),
    category VARCHAR(50),
    subcategory VARCHAR(50),
    brand VARCHAR(50),
    unit_price DECIMAL(10,2)
);

CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,  -- YYYYMMDD format
    full_date DATE,
    year INT,
    quarter INT,
    month INT,
    month_name VARCHAR(20),
    day_of_month INT,
    day_of_week INT,
    day_name VARCHAR(20),
    is_weekend BOOLEAN,
    is_holiday BOOLEAN
);

-- Fact Table (measurable events)
CREATE TABLE fact_sales (
    sales_key SERIAL PRIMARY KEY,
    customer_key INT REFERENCES dim_customer(customer_key),
    product_key INT REFERENCES dim_product(product_key),
    date_key INT REFERENCES dim_date(date_key),
    -- Measures
    quantity INT,
    unit_price DECIMAL(10,2),
    discount_amount DECIMAL(10,2),
    sales_amount DECIMAL(10,2),
    cost_amount DECIMAL(10,2),
    profit_amount DECIMAL(10,2)
);

-- Star Schema Query Example
SELECT 
    dc.country,
    dp.category,
    dd.year,
    dd.quarter,
    SUM(fs.sales_amount) as total_sales,
    SUM(fs.profit_amount) as total_profit,
    COUNT(*) as transaction_count
FROM fact_sales fs
JOIN dim_customer dc ON fs.customer_key = dc.customer_key
JOIN dim_product dp ON fs.product_key = dp.product_key
JOIN dim_date dd ON fs.date_key = dd.date_key
WHERE dd.year = 2023
  AND dc.country = 'USA'
GROUP BY dc.country, dp.category, dd.year, dd.quarter
ORDER BY total_sales DESC;

-- Snowflake Schema (normalized dimensions)
CREATE TABLE dim_product_category (
    category_key SERIAL PRIMARY KEY,
    category_name VARCHAR(50),
    category_description TEXT
);

CREATE TABLE dim_product_snowflake (
    product_key SERIAL PRIMARY KEY,
    product_id INT,
    product_name VARCHAR(100),
    category_key INT REFERENCES dim_product_category(category_key),
    brand VARCHAR(50),
    unit_price DECIMAL(10,2)
);
```

### 40. How do you handle large dataset operations efficiently?
**Answer:**
```sql
-- Batch processing for large updates
DO $$
DECLARE
    batch_size INT := 10000;
    total_updated INT := 0;
    rows_updated INT;
BEGIN
    LOOP
        UPDATE large_table 
        SET status = 'PROCESSED'
        WHERE id IN (
            SELECT id FROM large_table 
            WHERE status = 'PENDING'
            LIMIT batch_size
        );
        
        GET DIAGNOSTICS rows_updated = ROW_COUNT;
        total_updated := total_updated + rows_updated;
        
        RAISE NOTICE 'Updated % rows, total: %', rows_updated, total_updated;
        
        EXIT WHEN rows_updated = 0;
        
        -- Optional: commit and start new transaction
        COMMIT;
        BEGIN;
    END LOOP;
END $$;

-- Bulk insert with COPY
COPY large_table (col1, col2, col3)
FROM '/path/to/data.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',');

-- Parallel processing
-- Create partitioned table for parallel operations
CREATE TABLE sales_partitioned (
    id SERIAL,
    sale_date DATE,
    amount DECIMAL(10,2)
) PARTITION BY RANGE (sale_date);

-- Parallel index creation
CREATE INDEX CONCURRENTLY idx_large_table_date ON large_table(created_date);

-- Use CTEs for complex operations
WITH batch_data AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) as rn
    FROM large_table
    WHERE status = 'PENDING'
),
batched AS (
    SELECT id, CEIL(rn::FLOAT / 10000) as batch_num
    FROM batch_data
)
UPDATE large_table 
SET batch_id = batched.batch_num
FROM batched
WHERE large_table.id = batched.id;

-- Memory-efficient aggregation
SELECT 
    date_trunc('month', order_date) as month,
    SUM(amount) as monthly_total
FROM orders
WHERE order_date >= '2023-01-01'
GROUP BY date_trunc('month', order_date)
ORDER BY month;

-- Streaming aggregation for very large datasets
CREATE MATERIALIZED VIEW monthly_sales AS
SELECT 
    date_trunc('month', order_date) as month,
    COUNT(*) as order_count,
    SUM(amount) as total_amount
FROM orders
GROUP BY date_trunc('month', order_date);

-- Refresh incrementally
REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_sales;
```
### 41. What are database sharding strategies?
**Answer:**
```sql
-- Horizontal sharding by customer ID
-- Shard 1: customers 1-1000
CREATE TABLE customers_shard1 (
    customer_id INT CHECK (customer_id BETWEEN 1 AND 1000),
    name VARCHAR(100),
    email VARCHAR(100)
);

-- Shard 2: customers 1001-2000
CREATE TABLE customers_shard2 (
    customer_id INT CHECK (customer_id BETWEEN 1001 AND 2000),
    name VARCHAR(100),
    email VARCHAR(100)
);

-- Hash-based sharding
CREATE OR REPLACE FUNCTION get_shard_id(customer_id INT)
RETURNS INT AS $$
BEGIN
    RETURN (customer_id % 4) + 1;
END;
$$ LANGUAGE plpgsql;

-- Range-based sharding by date
CREATE TABLE orders_2023_q1 (
    order_id SERIAL,
    order_date DATE CHECK (order_date >= '2023-01-01' AND order_date < '2023-04-01'),
    customer_id INT,
    amount DECIMAL(10,2)
);

-- Directory-based sharding lookup
CREATE TABLE shard_directory (
    customer_id_range_start INT,
    customer_id_range_end INT,
    shard_name VARCHAR(50),
    connection_string VARCHAR(200)
);

-- Cross-shard query example
SELECT 'shard1' as shard, COUNT(*) as customer_count FROM customers_shard1
UNION ALL
SELECT 'shard2' as shard, COUNT(*) as customer_count FROM customers_shard2;
```

### 42. Explain database replication types and strategies
**Answer:**
```sql
-- Master-Slave Replication Setup (PostgreSQL)
-- On Master server
ALTER SYSTEM SET wal_level = 'replica';
ALTER SYSTEM SET max_wal_senders = 3;
ALTER SYSTEM SET wal_keep_segments = 64;

-- Create replication user
CREATE USER replicator REPLICATION LOGIN CONNECTION LIMIT 1 ENCRYPTED PASSWORD 'password';

-- On Slave server - streaming replication
-- pg_basebackup -h master_host -D /var/lib/postgresql/data -U replicator -v -P -W

-- Master-Master (Multi-Master) considerations
-- Conflict resolution strategies:
-- 1. Last-write-wins
-- 2. Application-level conflict resolution
-- 3. Timestamp-based resolution

-- Read replica query routing
-- Application logic to route reads to replicas
SELECT customer_id, name FROM customers_replica WHERE status = 'ACTIVE';

-- Write to master only
INSERT INTO customers (name, email) VALUES ('John Doe', 'john@example.com');

-- Monitoring replication lag
SELECT 
    client_addr,
    state,
    pg_wal_lsn_diff(pg_current_wal_lsn(), sent_lsn) as send_lag,
    pg_wal_lsn_diff(sent_lsn, flush_lsn) as flush_lag
FROM pg_stat_replication;
```

### 43. How do you implement database backup and recovery strategies?
**Answer:**
```sql
-- Full backup (PostgreSQL)
-- pg_dump -h localhost -U postgres -d mydb > backup_full.sql

-- Incremental backup using WAL archiving
ALTER SYSTEM SET archive_mode = 'on';
ALTER SYSTEM SET archive_command = 'cp %p /backup/archive/%f';

-- Point-in-time recovery
-- pg_restore -h localhost -U postgres -d mydb_restored backup_full.sql
-- Recovery up to specific time:
-- recovery_target_time = '2023-12-01 14:30:00'

-- Logical backup with specific tables
-- pg_dump -h localhost -U postgres -t customers -t orders mydb > partial_backup.sql

-- SQL Server backup strategies
-- Full backup
BACKUP DATABASE MyDatabase 
TO DISK = 'C:\Backup\MyDatabase_Full.bak'
WITH FORMAT, COMPRESSION;

-- Differential backup
BACKUP DATABASE MyDatabase 
TO DISK = 'C:\Backup\MyDatabase_Diff.bak'
WITH DIFFERENTIAL, COMPRESSION;

-- Transaction log backup
BACKUP LOG MyDatabase 
TO DISK = 'C:\Backup\MyDatabase_Log.trn';

-- Restore sequence
RESTORE DATABASE MyDatabase 
FROM DISK = 'C:\Backup\MyDatabase_Full.bak'
WITH NORECOVERY;

RESTORE DATABASE MyDatabase 
FROM DISK = 'C:\Backup\MyDatabase_Diff.bak'
WITH NORECOVERY;

RESTORE LOG MyDatabase 
FROM DISK = 'C:\Backup\MyDatabase_Log.trn'
WITH RECOVERY;

-- Backup verification
RESTORE VERIFYONLY 
FROM DISK = 'C:\Backup\MyDatabase_Full.bak';

-- Automated backup script
CREATE OR REPLACE FUNCTION automated_backup()
RETURNS void AS $$
DECLARE
    backup_file TEXT;
BEGIN
    backup_file := '/backup/db_' || to_char(now(), 'YYYY_MM_DD_HH24_MI_SS') || '.sql';
    
    PERFORM pg_dump('mydb', backup_file);
    
    -- Clean old backups (keep last 7 days)
    PERFORM pg_delete_old_backups('/backup/', 7);
    
    -- Log backup completion
    INSERT INTO backup_log (backup_date, backup_file, status)
    VALUES (now(), backup_file, 'SUCCESS');
END;
$$ LANGUAGE plpgsql;
```

### 44. What are database connection pooling and its benefits?
**Answer:**
```sql
-- Connection pooling configuration (pgbouncer example)
-- /etc/pgbouncer/pgbouncer.ini
/*
[databases]
mydb = host=localhost port=5432 dbname=mydb

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
max_db_connections = 100
*/

-- Application connection with pooling (Python example)
/*
import psycopg2.pool

# Create connection pool
connection_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=5,
    maxconn=20,
    host='localhost',
    database='mydb',
    user='username',
    password='password'
)

# Get connection from pool
conn = connection_pool.getconn()
cursor = conn.cursor()
cursor.execute("SELECT * FROM customers LIMIT 10")
results = cursor.fetchall()

# Return connection to pool
connection_pool.putconn(conn)
*/

-- Monitor connection usage
SELECT 
    datname,
    numbackends,
    xact_commit,
    xact_rollback,
    blks_read,
    blks_hit,
    tup_returned,
    tup_fetched
FROM pg_stat_database
WHERE datname = 'mydb';

-- Active connections
SELECT 
    pid,
    usename,
    application_name,
    client_addr,
    state,
    query_start,
    query
FROM pg_stat_activity
WHERE state = 'active';

-- Connection limits and settings
SHOW max_connections;
SHOW shared_buffers;
SHOW work_mem;

-- Kill long-running connections
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle in transaction'
  AND query_start < now() - interval '1 hour';
```

### 45. How do you handle database migrations and schema changes?
**Answer:**
```sql
-- Version-controlled migrations
-- Migration 001: Create initial tables
-- File: 001_create_customers.sql
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE migration_history (
    version VARCHAR(20) PRIMARY KEY,
    description TEXT,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO migration_history (version, description)
VALUES ('001', 'Create customers table');

-- Migration 002: Add new column
-- File: 002_add_customer_phone.sql
ALTER TABLE customers 
ADD COLUMN phone VARCHAR(20);

UPDATE migration_history 
SET applied_at = CURRENT_TIMESTAMP 
WHERE version = '002';

-- Migration 003: Data migration
-- File: 003_normalize_phone_numbers.sql
UPDATE customers 
SET phone = REGEXP_REPLACE(phone, '[^0-9]', '', 'g')
WHERE phone IS NOT NULL;

-- Rollback migration
-- File: 003_rollback.sql
-- Store original data before migration for rollback
CREATE TABLE customers_phone_backup AS
SELECT id, phone FROM customers WHERE phone IS NOT NULL;

-- Safe schema changes with minimal downtime
-- 1. Add new column (nullable)
ALTER TABLE orders ADD COLUMN new_status VARCHAR(20);

-- 2. Populate new column
UPDATE orders SET new_status = 
    CASE 
        WHEN status = 1 THEN 'PENDING'
        WHEN status = 2 THEN 'COMPLETED'
        WHEN status = 3 THEN 'CANCELLED'
    END;

-- 3. Make column NOT NULL after population
ALTER TABLE orders ALTER COLUMN new_status SET NOT NULL;

-- 4. Drop old column
ALTER TABLE orders DROP COLUMN status;

-- 5. Rename new column
ALTER TABLE orders RENAME COLUMN new_status TO status;

-- Blue-green deployment migration
-- Create new table structure
CREATE TABLE customers_v2 (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    address JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Migrate data
INSERT INTO customers_v2 (id, name, email, phone, created_at)
SELECT id, name, email, phone, created_at FROM customers;

-- Switch tables atomically
BEGIN;
ALTER TABLE customers RENAME TO customers_old;
ALTER TABLE customers_v2 RENAME TO customers;
COMMIT;

-- Migration validation
CREATE OR REPLACE FUNCTION validate_migration()
RETURNS BOOLEAN AS $$
DECLARE
    old_count INT;
    new_count INT;
BEGIN
    SELECT COUNT(*) INTO old_count FROM customers_old;
    SELECT COUNT(*) INTO new_count FROM customers;
    
    IF old_count != new_count THEN
        RAISE EXCEPTION 'Migration validation failed: row count mismatch';
    END IF;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
```

### 46. Explain database security best practices
**Answer:**
```sql
-- User and role management
CREATE ROLE data_reader;
CREATE ROLE data_writer;
CREATE ROLE data_admin;

-- Grant permissions to roles
GRANT SELECT ON ALL TABLES IN SCHEMA public TO data_reader;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO data_writer;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO data_admin;

-- Create users and assign roles
CREATE USER analyst WITH PASSWORD 'secure_password';
CREATE USER app_user WITH PASSWORD 'app_password';
CREATE USER dba WITH PASSWORD 'admin_password';

GRANT data_reader TO analyst;
GRANT data_writer TO app_user;
GRANT data_admin TO dba;

-- Row-level security (RLS)
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;

-- Policy for users to see only their own data
CREATE POLICY customer_isolation ON customers
    FOR ALL TO app_user
    USING (customer_id = current_setting('app.current_customer_id')::INT);

-- Column-level security
GRANT SELECT (id, name, email) ON customers TO data_reader;
-- Exclude sensitive columns like SSN, credit_card

-- Data masking for non-production environments
CREATE OR REPLACE FUNCTION mask_email(email TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN CASE 
        WHEN email IS NULL THEN NULL
        ELSE SUBSTRING(email FROM 1 FOR 2) || '***@' || 
             SUBSTRING(email FROM POSITION('@' IN email) + 1)
    END;
END;
$$ LANGUAGE plpgsql;

-- Create masked view for development
CREATE VIEW customers_masked AS
SELECT 
    id,
    name,
    mask_email(email) as email,
    'XXX-XXX-' || RIGHT(phone, 4) as phone
FROM customers;

-- Audit logging
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(50),
    operation VARCHAR(10),
    user_name VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    old_values JSONB,
    new_values JSONB
);

-- Audit trigger
CREATE OR REPLACE FUNCTION audit_trigger()
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
    FOR EACH ROW EXECUTE FUNCTION audit_trigger();

-- Encryption at rest and in transit
-- SSL/TLS configuration
ALTER SYSTEM SET ssl = 'on';
ALTER SYSTEM SET ssl_cert_file = 'server.crt';
ALTER SYSTEM SET ssl_key_file = 'server.key';

-- Column-level encryption
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Encrypt sensitive data
INSERT INTO customers (name, email, ssn_encrypted)
VALUES ('John Doe', 'john@example.com', 
        pgp_sym_encrypt('123-45-6789', 'encryption_key'));

-- Decrypt data
SELECT name, email, 
       pgp_sym_decrypt(ssn_encrypted, 'encryption_key') as ssn
FROM customers;
```

### 47. What are database design patterns and anti-patterns?
**Answer:**
```sql
-- GOOD PATTERNS

-- 1. Proper normalization
-- Normalized design (3NF)
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE addresses (
    address_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    street VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    address_type VARCHAR(20) -- 'billing', 'shipping'
);

-- 2. Surrogate keys
CREATE TABLE products (
    product_key SERIAL PRIMARY KEY,  -- Surrogate key
    product_code VARCHAR(20) UNIQUE, -- Natural key
    name VARCHAR(100),
    price DECIMAL(10,2)
);

-- 3. Audit columns
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) DEFAULT current_user,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(50) DEFAULT current_user
);

-- 4. Soft deletes
ALTER TABLE customers ADD COLUMN deleted_at TIMESTAMP;
ALTER TABLE customers ADD COLUMN is_active BOOLEAN DEFAULT TRUE;

-- Instead of DELETE
UPDATE customers SET deleted_at = CURRENT_TIMESTAMP, is_active = FALSE
WHERE customer_id = 123;

-- ANTI-PATTERNS TO AVOID

-- 1. EAV (Entity-Attribute-Value) - avoid when possible
-- BAD: Generic attribute table
CREATE TABLE entity_attributes (
    entity_id INT,
    attribute_name VARCHAR(50),
    attribute_value TEXT
);

-- GOOD: Proper columns
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10,2),
    weight DECIMAL(8,2),
    color VARCHAR(20)
);

-- 2. Polymorphic associations - avoid
-- BAD: Generic foreign key
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    commentable_id INT,
    commentable_type VARCHAR(50), -- 'Product', 'Order', etc.
    content TEXT
);

-- GOOD: Separate tables or specific foreign keys
CREATE TABLE product_comments (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(product_id),
    content TEXT
);

-- 3. Storing delimited values in single column
-- BAD: Comma-separated values
CREATE TABLE orders_bad (
    order_id SERIAL PRIMARY KEY,
    product_ids TEXT  -- '1,2,3,4'
);

-- GOOD: Junction table
CREATE TABLE order_items (
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity INT,
    PRIMARY KEY (order_id, product_id)
);

-- 4. Using FLOAT for money
-- BAD: Precision issues
CREATE TABLE products_bad (
    price FLOAT  -- Can cause rounding errors
);

-- GOOD: Use DECIMAL
CREATE TABLE products_good (
    price DECIMAL(10,2)  -- Exact precision
);

-- 5. Not using constraints
-- BAD: No validation
CREATE TABLE employees_bad (
    salary INT,
    email VARCHAR(100)
);

-- GOOD: Proper constraints
CREATE TABLE employees_good (
    salary DECIMAL(10,2) CHECK (salary > 0),
    email VARCHAR(100) UNIQUE NOT NULL 
        CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);
```

### 48. How do you implement database monitoring and alerting?
**Answer:**
```sql
-- Performance monitoring queries
-- Long-running queries
SELECT 
    pid,
    now() - pg_stat_activity.query_start AS duration,
    query,
    state
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes'
  AND state = 'active';

-- Database size monitoring
SELECT 
    datname,
    pg_size_pretty(pg_database_size(datname)) as size
FROM pg_database
ORDER BY pg_database_size(datname) DESC;

-- Table size monitoring
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as table_size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - 
                   pg_relation_size(schemaname||'.'||tablename)) as index_size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 10;

-- Index usage monitoring
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch,
    idx_scan
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Unused indexes
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND schemaname = 'public';

-- Connection monitoring
SELECT 
    state,
    COUNT(*) as connection_count
FROM pg_stat_activity
GROUP BY state;

-- Blocking queries
SELECT 
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS blocking_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.DATABASE IS NOT DISTINCT FROM blocked_locks.DATABASE
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
    AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
    AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
    AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
    AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
    AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
    AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
    AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.GRANTED;

-- Create monitoring views
CREATE VIEW db_health_check AS
SELECT 
    'Database Size' as metric,
    pg_size_pretty(pg_database_size(current_database())) as value,
    CASE 
        WHEN pg_database_size(current_database()) > 100 * 1024^3 THEN 'WARNING'
        ELSE 'OK'
    END as status
UNION ALL
SELECT 
    'Active Connections' as metric,
    COUNT(*)::TEXT as value,
    CASE 
        WHEN COUNT(*) > 80 THEN 'CRITICAL'
        WHEN COUNT(*) > 60 THEN 'WARNING'
        ELSE 'OK'
    END as status
FROM pg_stat_activity
WHERE state = 'active'
UNION ALL
SELECT 
    'Long Running Queries' as metric,
    COUNT(*)::TEXT as value,
    CASE 
        WHEN COUNT(*) > 5 THEN 'CRITICAL'
        WHEN COUNT(*) > 2 THEN 'WARNING'
        ELSE 'OK'
    END as status
FROM pg_stat_activity
WHERE state = 'active'
  AND (now() - query_start) > interval '10 minutes';

-- Alerting function
CREATE OR REPLACE FUNCTION check_db_alerts()
RETURNS TABLE(alert_type TEXT, message TEXT, severity TEXT) AS $$
BEGIN
    -- Check for long-running queries
    RETURN QUERY
    SELECT 
        'Long Running Query'::TEXT,
        'Query running for ' || (now() - query_start)::TEXT || ': ' || 
        LEFT(query, 100)::TEXT,
        'WARNING'::TEXT
    FROM pg_stat_activity
    WHERE state = 'active'
      AND (now() - query_start) > interval '30 minutes';
    
    -- Check for high connection count
    IF (SELECT COUNT(*) FROM pg_stat_activity) > 90 THEN
        RETURN QUERY SELECT 
            'High Connection Count'::TEXT,
            'Current connections: ' || (SELECT COUNT(*) FROM pg_stat_activity)::TEXT,
            'CRITICAL'::TEXT;
    END IF;
    
    -- Check for blocking queries
    RETURN QUERY
    SELECT 
        'Blocking Query'::TEXT,
        'PID ' || blocking_locks.pid::TEXT || ' blocking PID ' || blocked_locks.pid::TEXT,
        'CRITICAL'::TEXT
    FROM pg_catalog.pg_locks blocked_locks
    JOIN pg_catalog.pg_locks blocking_locks ON (
        blocking_locks.locktype = blocked_locks.locktype AND
        blocking_locks.pid != blocked_locks.pid
    )
    WHERE NOT blocked_locks.granted
    LIMIT 5;
END;
$$ LANGUAGE plpgsql;

-- Automated monitoring job
CREATE OR REPLACE FUNCTION run_monitoring_job()
RETURNS void AS $$
DECLARE
    alert_record RECORD;
BEGIN
    FOR alert_record IN SELECT * FROM check_db_alerts() LOOP
        -- Log alert
        INSERT INTO monitoring_alerts (alert_type, message, severity, created_at)
        VALUES (alert_record.alert_type, alert_record.message, 
                alert_record.severity, CURRENT_TIMESTAMP);
        
        -- Send notification (implement based on your system)
        -- PERFORM send_notification(alert_record.message);
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

### 49. Explain database testing strategies
**Answer:**
```sql
-- Unit testing for database functions
-- Test function
CREATE OR REPLACE FUNCTION calculate_order_total(order_id INT)
RETURNS DECIMAL(10,2) AS $$
DECLARE
    total DECIMAL(10,2);
BEGIN
    SELECT SUM(quantity * unit_price) INTO total
    FROM order_items
    WHERE order_items.order_id = calculate_order_total.order_id;
    
    RETURN COALESCE(total, 0);
END;
$$ LANGUAGE plpgsql;

-- Test cases
DO $$
DECLARE
    test_order_id INT;
    expected_total DECIMAL(10,2) := 150.00;
    actual_total DECIMAL(10,2);
BEGIN
    -- Setup test data
    INSERT INTO orders (customer_id, order_date) 
    VALUES (1, CURRENT_DATE) RETURNING order_id INTO test_order_id;
    
    INSERT INTO order_items (order_id, product_id, quantity, unit_price)
    VALUES 
        (test_order_id, 1, 2, 50.00),
        (test_order_id, 2, 1, 50.00);
    
    -- Execute test
    SELECT calculate_order_total(test_order_id) INTO actual_total;
    
    -- Assert
    IF actual_total != expected_total THEN
        RAISE EXCEPTION 'Test failed: expected %, got %', expected_total, actual_total;
    ELSE
        RAISE NOTICE 'Test passed: calculate_order_total';
    END IF;
    
    -- Cleanup
    DELETE FROM order_items WHERE order_id = test_order_id;
    DELETE FROM orders WHERE order_id = test_order_id;
END $$;

-- Integration testing
-- Test complete order workflow
CREATE OR REPLACE FUNCTION test_order_workflow()
RETURNS void AS $$
DECLARE
    customer_id INT;
    order_id INT;
    product_id INT;
    initial_stock INT;
    final_stock INT;
BEGIN
    -- Setup
    INSERT INTO customers (name, email) 
    VALUES ('Test Customer', 'test@example.com') 
    RETURNING customer_id INTO customer_id;
    
    INSERT INTO products (name, price, stock_quantity)
    VALUES ('Test Product', 25.00, 100)
    RETURNING product_id INTO product_id;
    
    SELECT stock_quantity INTO initial_stock 
    FROM products WHERE products.product_id = test_order_workflow.product_id;
    
    -- Test order creation
    INSERT INTO orders (customer_id, order_date)
    VALUES (customer_id, CURRENT_DATE)
    RETURNING order_id INTO order_id;
    
    INSERT INTO order_items (order_id, product_id, quantity, unit_price)
    VALUES (order_id, product_id, 5, 25.00);
    
    -- Test stock update trigger (assuming it exists)
    SELECT stock_quantity INTO final_stock 
    FROM products WHERE products.product_id = test_order_workflow.product_id;
    
    -- Assertions
    IF final_stock != initial_stock - 5 THEN
        RAISE EXCEPTION 'Stock update failed: expected %, got %', 
                       initial_stock - 5, final_stock;
    END IF;
    
    -- Cleanup
    DELETE FROM order_items WHERE order_id = test_order_workflow.order_id;
    DELETE FROM orders WHERE orders.order_id = test_order_workflow.order_id;
    DELETE FROM products WHERE products.product_id = test_order_workflow.product_id;
    DELETE FROM customers WHERE customers.customer_id = test_order_workflow.customer_id;
    
    RAISE NOTICE 'Order workflow test passed';
END;
$$ LANGUAGE plpgsql;

-- Performance testing
-- Load test function
CREATE OR REPLACE FUNCTION performance_test_insert(num_records INT)
RETURNS TABLE(operation TEXT, duration INTERVAL, records_per_second NUMERIC) AS $$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    i INT;
BEGIN
    start_time := clock_timestamp();
    
    FOR i IN 1..num_records LOOP
        INSERT INTO test_table (name, value)
        VALUES ('Test Record ' || i, random() * 1000);
    END LOOP;
    
    end_time := clock_timestamp();
    
    RETURN QUERY SELECT 
        'INSERT'::TEXT,
        end_time - start_time,
        num_records / EXTRACT(EPOCH FROM (end_time - start_time));
END;
$$ LANGUAGE plpgsql;

-- Data quality tests
CREATE OR REPLACE FUNCTION test_data_quality()
RETURNS TABLE(test_name TEXT, status TEXT, details TEXT) AS $$
BEGIN
    -- Test for NULL values in required fields
    RETURN QUERY
    SELECT 
        'Required Fields Check'::TEXT,
        CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END,
        'Found ' || COUNT(*) || ' records with NULL required fields'
    FROM customers
    WHERE name IS NULL OR email IS NULL;
    
    -- Test for duplicate emails
    RETURN QUERY
    SELECT 
        'Duplicate Email Check'::TEXT,
        CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END,
        'Found ' || COUNT(*) || ' duplicate emails'
    FROM (
        SELECT email, COUNT(*)
        FROM customers
        GROUP BY email
        HAVING COUNT(*) > 1
    ) duplicates;
    
    -- Test for referential integrity
    RETURN QUERY
    SELECT 
        'Referential Integrity Check'::TEXT,
        CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END,
        'Found ' || COUNT(*) || ' orphaned order records'
    FROM orders o
    LEFT JOIN customers c ON o.customer_id = c.customer_id
    WHERE c.customer_id IS NULL;
    
    -- Test for data ranges
    RETURN QUERY
    SELECT 
        'Data Range Check'::TEXT,
        CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END,
        'Found ' || COUNT(*) || ' records with invalid salary ranges'
    FROM employees
    WHERE salary < 0 OR salary > 1000000;
END;
$$ LANGUAGE plpgsql;

-- Test framework setup
CREATE TABLE test_results (
    test_id SERIAL PRIMARY KEY,
    test_name VARCHAR(100),
    test_type VARCHAR(50),
    status VARCHAR(20),
    details TEXT,
    execution_time INTERVAL,
    run_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Test runner
CREATE OR REPLACE FUNCTION run_all_tests()
RETURNS void AS $$
DECLARE
    test_record RECORD;
    start_time TIMESTAMP;
    end_time TIMESTAMP;
BEGIN
    start_time := clock_timestamp();
    
    -- Run data quality tests
    FOR test_record IN SELECT * FROM test_data_quality() LOOP
        INSERT INTO test_results (test_name, test_type, status, details, execution_time)
        VALUES (test_record.test_name, 'Data Quality', test_record.status, 
                test_record.details, clock_timestamp() - start_time);
    END LOOP;
    
    -- Run unit tests
    PERFORM test_order_workflow();
    
    end_time := clock_timestamp();
    
    RAISE NOTICE 'All tests completed in %', end_time - start_time;
END;
$$ LANGUAGE plpgsql;
```

### 50. How do you implement database disaster recovery?
**Answer:**
```sql
-- Disaster Recovery Planning

-- 1. Hot Standby Setup (PostgreSQL Streaming Replication)
-- Primary server configuration
ALTER SYSTEM SET wal_level = 'replica';
ALTER SYSTEM SET max_wal_senders = 10;
ALTER SYSTEM SET wal_keep_segments = 100;
ALTER SYSTEM SET synchronous_standby_names = 'standby1,standby2';

-- Create replication slots for guaranteed WAL retention
SELECT pg_create_physical_replication_slot('standby1_slot');
SELECT pg_create_physical_replication_slot('standby2_slot');

-- Standby server recovery configuration
-- recovery.conf (or postgresql.conf in newer versions)
/*
standby_mode = 'on'
primary_conninfo = 'host=primary_server port=5432 user=replicator'
primary_slot_name = 'standby1_slot'
restore_command = 'cp /archive/%f %p'
*/

-- 2. Point-in-Time Recovery (PITR) Setup
-- Enable WAL archiving
ALTER SYSTEM SET archive_mode = 'on';
ALTER SYSTEM SET archive_command = 'rsync %p backup_server:/archive/%f';

-- Create base backup
-- pg_basebackup -h primary_server -D /backup/base -U replicator -v -P -W

-- Recovery procedure
-- 1. Stop database service
-- 2. Restore base backup
-- 3. Create recovery.conf with target time
/*
restore_command = 'cp /archive/%f %p'
recovery_target_time = '2023-12-01 14:30:00'
recovery_target_action = 'promote'
*/

-- 3. Cross-Region Disaster Recovery
-- Automated backup to remote location
CREATE OR REPLACE FUNCTION disaster_recovery_backup()
RETURNS void AS $$
DECLARE
    backup_file TEXT;
    remote_location TEXT := 's3://disaster-recovery-bucket/';
BEGIN
    -- Create timestamped backup
    backup_file := 'dr_backup_' || to_char(now(), 'YYYY_MM_DD_HH24_MI_SS') || '.sql';
    
    -- Perform backup (pseudo-code)
    PERFORM pg_dump_to_file('/tmp/' || backup_file);
    
    -- Upload to remote storage
    PERFORM upload_to_s3('/tmp/' || backup_file, remote_location || backup_file);
    
    -- Verify backup integrity
    PERFORM verify_backup_integrity(remote_location || backup_file);
    
    -- Log backup completion
    INSERT INTO dr_backup_log (backup_file, backup_date, status, location)
    VALUES (backup_file, now(), 'SUCCESS', remote_location || backup_file);
    
    -- Cleanup local file
    PERFORM delete_local_file('/tmp/' || backup_file);
END;
$$ LANGUAGE plpgsql;

-- 4. Failover Procedures
-- Automated failover script
CREATE OR REPLACE FUNCTION initiate_failover()
RETURNS void AS $$
DECLARE
    primary_status BOOLEAN;
    standby_lag INTERVAL;
BEGIN
    -- Check primary server status
    SELECT check_primary_server_health() INTO primary_status;
    
    IF NOT primary_status THEN
        -- Check standby lag
        SELECT pg_last_wal_receive_lsn() - pg_last_wal_replay_lsn() INTO standby_lag;
        
        IF standby_lag < interval '1 minute' THEN
            -- Promote standby to primary
            PERFORM pg_promote();
            
            -- Update DNS/load balancer
            PERFORM update_dns_to_new_primary();
            
            -- Notify administrators
            PERFORM send_failover_notification('Automatic failover completed');
            
            -- Log failover event
            INSERT INTO failover_log (event_type, timestamp, details)
            VALUES ('AUTOMATIC_FAILOVER', now(), 'Standby promoted to primary');
        ELSE
            -- Manual intervention required
            PERFORM send_alert('Manual failover required - standby lag too high');
        END IF;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- 5. Recovery Testing
-- Regular DR drill procedure
CREATE OR REPLACE FUNCTION disaster_recovery_drill()
RETURNS TABLE(test_step TEXT, status TEXT, duration INTERVAL, notes TEXT) AS $$
DECLARE
    start_time TIMESTAMP;
    step_start TIMESTAMP;
    test_db_name TEXT := 'dr_test_' || extract(epoch from now())::TEXT;
BEGIN
    start_time := clock_timestamp();
    
    -- Step 1: Restore from backup
    step_start := clock_timestamp();
    PERFORM restore_database_from_backup(test_db_name);
    RETURN QUERY SELECT 
        'Database Restore'::TEXT,
        'SUCCESS'::TEXT,
        clock_timestamp() - step_start,
        'Restored to database: ' || test_db_name;
    
    -- Step 2: Verify data integrity
    step_start := clock_timestamp();
    PERFORM verify_data_integrity(test_db_name);
    RETURN QUERY SELECT 
        'Data Integrity Check'::TEXT,
        'SUCCESS'::TEXT,
        clock_timestamp() - step_start,
        'All integrity checks passed';
    
    -- Step 3: Test application connectivity
    step_start := clock_timestamp();
    PERFORM test_application_connectivity(test_db_name);
    RETURN QUERY SELECT 
        'Application Connectivity'::TEXT,
        'SUCCESS'::TEXT,
        clock_timestamp() - step_start,
        'Application successfully connected';
    
    -- Step 4: Performance validation
    step_start := clock_timestamp();
    PERFORM run_performance_tests(test_db_name);
    RETURN QUERY SELECT 
        'Performance Validation'::TEXT,
        'SUCCESS'::TEXT,
        clock_timestamp() - step_start,
        'Performance within acceptable limits';
    
    -- Cleanup test database
    PERFORM drop_database(test_db_name);
    
    -- Overall summary
    RETURN QUERY SELECT 
        'DR Drill Complete'::TEXT,
        'SUCCESS'::TEXT,
        clock_timestamp() - start_time,
        'All tests passed successfully';
END;
$$ LANGUAGE plpgsql;

-- 6. Recovery Time Objective (RTO) and Recovery Point Objective (RPO) Monitoring
CREATE TABLE dr_metrics (
    metric_date DATE PRIMARY KEY,
    rpo_minutes INT,  -- How much data loss is acceptable
    rto_minutes INT,  -- How long recovery should take
    actual_backup_frequency_minutes INT,
    last_successful_backup TIMESTAMP,
    last_dr_test_date DATE,
    dr_test_success BOOLEAN
);

-- Monitor and alert on DR metrics
CREATE OR REPLACE FUNCTION check_dr_compliance()
RETURNS TABLE(metric TEXT, status TEXT, details TEXT) AS $$
BEGIN
    -- Check backup frequency vs RPO
    RETURN QUERY
    SELECT 
        'RPO Compliance'::TEXT,
        CASE 
            WHEN EXTRACT(EPOCH FROM (now() - last_successful_backup))/60 <= rpo_minutes 
            THEN 'COMPLIANT' 
            ELSE 'NON_COMPLIANT' 
        END,
        'Last backup: ' || last_successful_backup::TEXT || 
        ', RPO: ' || rpo_minutes || ' minutes'
    FROM dr_metrics 
    WHERE metric_date = CURRENT_DATE;
    
    -- Check DR test recency
    RETURN QUERY
    SELECT 
        'DR Test Recency'::TEXT,
        CASE 
            WHEN last_dr_test_date >= CURRENT_DATE - INTERVAL '90 days' 
            THEN 'COMPLIANT' 
            ELSE 'NON_COMPLIANT' 
        END,
        'Last DR test: ' || last_dr_test_date::TEXT
    FROM dr_metrics 
    WHERE metric_date = CURRENT_DATE;
END;
$$ LANGUAGE plpgsql;
```
## Database Design & Architecture (51-65)

### 51. How do you design a scalable database schema?
**Answer:**
```sql
-- Horizontal partitioning strategy
CREATE TABLE orders_2023 (
    order_id BIGSERIAL,
    customer_id BIGINT,
    order_date DATE,
    amount DECIMAL(12,2),
    status VARCHAR(20)
) PARTITION BY RANGE (order_date);

CREATE TABLE orders_2023_q1 PARTITION OF orders_2023
    FOR VALUES FROM ('2023-01-01') TO ('2023-04-01');

-- Vertical partitioning for large tables
CREATE TABLE customer_core (
    customer_id BIGSERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE customer_profile (
    customer_id BIGINT PRIMARY KEY REFERENCES customer_core(customer_id),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone VARCHAR(20),
    address TEXT,
    preferences JSONB
);

-- Read replicas for scaling reads
-- Master for writes, replicas for reads
-- Application routing logic needed
```

### 52. What is database denormalization and when to use it?
**Answer:**
```sql
-- Normalized design (3NF)
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date DATE,
    total_amount DECIMAL(10,2)
);

-- Denormalized for performance (reporting table)
CREATE TABLE order_summary_denorm (
    order_id INT PRIMARY KEY,
    customer_id INT,
    customer_name VARCHAR(100),  -- Denormalized
    customer_email VARCHAR(100), -- Denormalized
    order_date DATE,
    total_amount DECIMAL(10,2),
    order_count_ytd INT,         -- Denormalized aggregate
    customer_lifetime_value DECIMAL(12,2) -- Denormalized aggregate
);

-- Materialized view for denormalization
CREATE MATERIALIZED VIEW customer_order_summary AS
SELECT 
    c.customer_id,
    c.name,
    c.email,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as lifetime_value,
    MAX(o.order_date) as last_order_date,
    AVG(o.total_amount) as avg_order_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.email;

-- Refresh strategy
REFRESH MATERIALIZED VIEW CONCURRENTLY customer_order_summary;
```

### 53. How do you implement database versioning and migrations?
**Answer:**
```sql
-- Migration tracking table
CREATE TABLE schema_migrations (
    version VARCHAR(20) PRIMARY KEY,
    description TEXT,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    applied_by VARCHAR(50) DEFAULT current_user,
    checksum VARCHAR(64)
);

-- Migration script template
-- V001__create_initial_schema.sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO schema_migrations (version, description, checksum)
VALUES ('001', 'Create initial schema', 'abc123def456');

-- V002__add_user_profile.sql
ALTER TABLE users ADD COLUMN first_name VARCHAR(50);
ALTER TABLE users ADD COLUMN last_name VARCHAR(50);
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

INSERT INTO schema_migrations (version, description, checksum)
VALUES ('002', 'Add user profile fields', 'def456ghi789');

-- Rollback script
-- V002__rollback.sql
ALTER TABLE users DROP COLUMN IF EXISTS phone;
ALTER TABLE users DROP COLUMN IF EXISTS last_name;
ALTER TABLE users DROP COLUMN IF EXISTS first_name;

DELETE FROM schema_migrations WHERE version = '002';

-- Migration validation
CREATE OR REPLACE FUNCTION validate_migration(target_version VARCHAR(20))
RETURNS BOOLEAN AS $$
DECLARE
    current_version VARCHAR(20);
    migration_exists BOOLEAN;
BEGIN
    -- Get current version
    SELECT version INTO current_version 
    FROM schema_migrations 
    ORDER BY applied_at DESC 
    LIMIT 1;
    
    -- Check if target migration exists
    SELECT EXISTS(
        SELECT 1 FROM schema_migrations 
        WHERE version = target_version
    ) INTO migration_exists;
    
    RETURN migration_exists AND target_version > current_version;
END;
$$ LANGUAGE plpgsql;
```

### 54. What are database design patterns for multi-tenancy?
**Answer:**
```sql
-- Pattern 1: Shared Database, Shared Schema (Row-level isolation)
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    name VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Row Level Security for tenant isolation
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON customers
    FOR ALL TO application_role
    USING (tenant_id = current_setting('app.current_tenant_id')::UUID);

-- Pattern 2: Shared Database, Separate Schemas
CREATE SCHEMA tenant_abc123;
CREATE SCHEMA tenant_def456;

-- Create tables in tenant schemas
CREATE TABLE tenant_abc123.customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE tenant_def456.customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

-- Pattern 3: Separate Databases
-- Database per tenant approach
-- tenant_abc123_db, tenant_def456_db, etc.

-- Connection routing logic needed in application
CREATE OR REPLACE FUNCTION get_tenant_database(tenant_id UUID)
RETURNS TEXT AS $$
BEGIN
    RETURN 'tenant_' || replace(tenant_id::TEXT, '-', '') || '_db';
END;
$$ LANGUAGE plpgsql;

-- Tenant management table (in master database)
CREATE TABLE tenants (
    tenant_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_name VARCHAR(100) NOT NULL,
    database_name VARCHAR(100),
    schema_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'ACTIVE'
);
```

### 55. How do you design for high availability and fault tolerance?
**Answer:**
```sql
-- Master-Slave replication setup
-- Master configuration
ALTER SYSTEM SET wal_level = 'replica';
ALTER SYSTEM SET max_wal_senders = 5;
ALTER SYSTEM SET wal_keep_segments = 32;

-- Create replication user
CREATE USER replicator REPLICATION LOGIN ENCRYPTED PASSWORD 'secure_password';

-- Slave configuration (recovery.conf)
/*
standby_mode = 'on'
primary_conninfo = 'host=master_ip port=5432 user=replicator password=secure_password'
restore_command = 'cp /archive/%f %p'
*/

-- Health check function
CREATE OR REPLACE FUNCTION database_health_check()
RETURNS TABLE(
    component TEXT,
    status TEXT,
    details TEXT,
    last_check TIMESTAMP
) AS $$
BEGIN
    -- Check replication lag
    RETURN QUERY
    SELECT 
        'Replication Lag'::TEXT,
        CASE 
            WHEN pg_is_in_recovery() THEN 'SLAVE'
            ELSE 'MASTER'
        END,
        CASE 
            WHEN pg_is_in_recovery() THEN
                'Lag: ' || (
                    EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp()))
                )::TEXT || ' seconds'
            ELSE 'N/A (Master)'
        END,
        now();
    
    -- Check disk space
    RETURN QUERY
    SELECT 
        'Disk Space'::TEXT,
        CASE 
            WHEN pg_size_pretty(pg_database_size(current_database()))::TEXT ~ 'GB$' 
            THEN 'WARNING'
            ELSE 'OK'
        END,
        'Database size: ' || pg_size_pretty(pg_database_size(current_database())),
        now();
    
    -- Check connection count
    RETURN QUERY
    SELECT 
        'Connections'::TEXT,
        CASE 
            WHEN (SELECT count(*) FROM pg_stat_activity) > 80 THEN 'WARNING'
            ELSE 'OK'
        END,
        'Active connections: ' || (SELECT count(*) FROM pg_stat_activity)::TEXT,
        now();
END;
$$ LANGUAGE plpgsql;

-- Automatic failover script
CREATE OR REPLACE FUNCTION initiate_failover()
RETURNS BOOLEAN AS $$
DECLARE
    is_master BOOLEAN;
    replication_lag INTERVAL;
BEGIN
    -- Check if this is currently a slave
    SELECT NOT pg_is_in_recovery() INTO is_master;
    
    IF is_master THEN
        RAISE NOTICE 'Already running as master';
        RETURN FALSE;
    END IF;
    
    -- Check replication lag
    SELECT now() - pg_last_xact_replay_timestamp() INTO replication_lag;
    
    IF replication_lag > INTERVAL '5 minutes' THEN
        RAISE WARNING 'Replication lag too high: %', replication_lag;
    END IF;
    
    -- Promote to master
    PERFORM pg_promote();
    
    RAISE NOTICE 'Failover initiated - promoted to master';
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
```

### 56. What is database connection pooling and how to implement it?
**Answer:**
```sql
-- Connection pool monitoring
CREATE VIEW connection_pool_stats AS
SELECT 
    datname,
    usename,
    application_name,
    state,
    COUNT(*) as connection_count,
    MAX(backend_start) as oldest_connection,
    MIN(backend_start) as newest_connection
FROM pg_stat_activity
WHERE pid <> pg_backend_pid()
GROUP BY datname, usename, application_name, state;

-- Connection pool configuration (pgbouncer example)
/*
[databases]
production_db = host=localhost port=5432 dbname=production

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
max_db_connections = 100
reserve_pool_size = 5
reserve_pool_timeout = 3
server_reset_query = DISCARD ALL
server_check_query = SELECT 1
server_check_delay = 30
*/

-- Application-level connection pooling (Python example)
/*
import psycopg2.pool

class DatabasePool:
    def __init__(self):
        self.pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=5,
            maxconn=20,
            host='localhost',
            database='production',
            user='app_user',
            password='password'
        )
    
    def get_connection(self):
        return self.pool.getconn()
    
    def return_connection(self, conn):
        self.pool.putconn(conn)
    
    def close_all_connections(self):
        self.pool.closeall()
*/

-- Monitor connection usage
CREATE OR REPLACE FUNCTION monitor_connections()
RETURNS TABLE(
    metric TEXT,
    current_value INT,
    threshold INT,
    status TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'Total Connections'::TEXT,
        (SELECT count(*)::INT FROM pg_stat_activity),
        100,
        CASE 
            WHEN (SELECT count(*) FROM pg_stat_activity) > 80 THEN 'WARNING'
            WHEN (SELECT count(*) FROM pg_stat_activity) > 90 THEN 'CRITICAL'
            ELSE 'OK'
        END;
    
    RETURN QUERY
    SELECT 
        'Idle Connections'::TEXT,
        (SELECT count(*)::INT FROM pg_stat_activity WHERE state = 'idle'),
        50,
        CASE 
            WHEN (SELECT count(*) FROM pg_stat_activity WHERE state = 'idle') > 40 THEN 'WARNING'
            ELSE 'OK'
        END;
END;
$$ LANGUAGE plpgsql;
```

### 57. How do you implement database caching strategies?
**Answer:**
```sql
-- Query result caching with Redis
-- Application-level caching logic

-- Database-level caching with materialized views
CREATE MATERIALIZED VIEW popular_products_cache AS
SELECT 
    p.product_id,
    p.name,
    p.price,
    COUNT(oi.order_id) as order_count,
    SUM(oi.quantity) as total_sold,
    AVG(r.rating) as avg_rating
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
LEFT JOIN reviews r ON p.product_id = r.product_id
WHERE p.status = 'ACTIVE'
GROUP BY p.product_id, p.name, p.price
HAVING COUNT(oi.order_id) > 100
ORDER BY order_count DESC;

-- Refresh strategy
CREATE OR REPLACE FUNCTION refresh_product_cache()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY popular_products_cache;
    
    -- Log refresh
    INSERT INTO cache_refresh_log (view_name, refresh_time, status)
    VALUES ('popular_products_cache', now(), 'SUCCESS');
END;
$$ LANGUAGE plpgsql;

-- Scheduled refresh
-- Use pg_cron or external scheduler
-- SELECT cron.schedule('refresh-cache', '0 */6 * * *', 'SELECT refresh_product_cache();');

-- Cache invalidation triggers
CREATE OR REPLACE FUNCTION invalidate_product_cache()
RETURNS TRIGGER AS $$
BEGIN
    -- Mark cache as stale
    UPDATE cache_status 
    SET is_stale = TRUE, 
        last_invalidated = now()
    WHERE cache_name = 'popular_products_cache';
    
    -- Optionally refresh immediately for critical updates
    IF TG_OP = 'UPDATE' AND OLD.status != NEW.status THEN
        PERFORM refresh_product_cache();
    END IF;
    
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER product_cache_invalidation
    AFTER INSERT OR UPDATE OR DELETE ON products
    FOR EACH ROW EXECUTE FUNCTION invalidate_product_cache();

-- Cache hit ratio monitoring
CREATE VIEW cache_performance AS
SELECT 
    'Buffer Cache Hit Ratio' as metric,
    ROUND(
        (sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read))) * 100, 2
    ) as hit_ratio_percent
FROM pg_statio_user_tables
WHERE heap_blks_read > 0;
```

### 58. What are database design considerations for GDPR compliance?
**Answer:**
```sql
-- Data classification and tagging
CREATE TABLE data_classification (
    table_name VARCHAR(100),
    column_name VARCHAR(100),
    data_type VARCHAR(50),
    classification VARCHAR(20), -- 'PII', 'SENSITIVE', 'PUBLIC'
    retention_period INTERVAL,
    anonymization_required BOOLEAN,
    PRIMARY KEY (table_name, column_name)
);

-- Insert classification data
INSERT INTO data_classification VALUES
('customers', 'email', 'VARCHAR', 'PII', INTERVAL '7 years', TRUE),
('customers', 'phone', 'VARCHAR', 'PII', INTERVAL '7 years', TRUE),
('customers', 'name', 'VARCHAR', 'PII', INTERVAL '7 years', TRUE),
('orders', 'order_date', 'DATE', 'PUBLIC', INTERVAL '10 years', FALSE);

-- Right to be forgotten implementation
CREATE OR REPLACE FUNCTION anonymize_customer_data(customer_email VARCHAR)
RETURNS BOOLEAN AS $$
DECLARE
    customer_record RECORD;
    anonymized_id TEXT;
BEGIN
    -- Find customer
    SELECT * INTO customer_record 
    FROM customers 
    WHERE email = customer_email;
    
    IF NOT FOUND THEN
        RAISE NOTICE 'Customer not found: %', customer_email;
        RETURN FALSE;
    END IF;
    
    -- Generate anonymized ID
    anonymized_id := 'ANON_' || extract(epoch from now())::TEXT;
    
    -- Anonymize customer data
    UPDATE customers 
    SET 
        email = anonymized_id || '@anonymized.com',
        name = 'Anonymized User',
        phone = NULL,
        address = NULL,
        anonymized_at = now(),
        anonymized_reason = 'GDPR_REQUEST'
    WHERE customer_id = customer_record.customer_id;
    
    -- Keep order history but anonymize personal references
    UPDATE orders 
    SET customer_notes = 'ANONYMIZED'
    WHERE customer_id = customer_record.customer_id
      AND customer_notes IS NOT NULL;
    
    -- Log the anonymization
    INSERT INTO gdpr_requests (
        request_type, 
        customer_id, 
        original_email, 
        processed_at, 
        status
    ) VALUES (
        'RIGHT_TO_BE_FORGOTTEN',
        customer_record.customer_id,
        customer_email,
        now(),
        'COMPLETED'
    );
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

-- Data export for data portability
CREATE OR REPLACE FUNCTION export_customer_data(customer_email VARCHAR)
RETURNS JSON AS $$
DECLARE
    customer_data JSON;
BEGIN
    SELECT json_build_object(
        'personal_info', json_build_object(
            'name', c.name,
            'email', c.email,
            'phone', c.phone,
            'address', c.address,
            'created_at', c.created_at
        ),
        'orders', (
            SELECT json_agg(json_build_object(
                'order_id', o.order_id,
                'order_date', o.order_date,
                'total_amount', o.total_amount,
                'status', o.status
            ))
            FROM orders o
            WHERE o.customer_id = c.customer_id
        ),
        'preferences', c.preferences
    ) INTO customer_data
    FROM customers c
    WHERE c.email = customer_email;
    
    -- Log the export request
    INSERT INTO gdpr_requests (
        request_type,
        customer_email,
        processed_at,
        status
    ) VALUES (
        'DATA_EXPORT',
        customer_email,
        now(),
        'COMPLETED'
    );
    
    RETURN customer_data;
END;
$$ LANGUAGE plpgsql;

-- Automated data retention
CREATE OR REPLACE FUNCTION apply_data_retention()
RETURNS void AS $$
DECLARE
    classification_record RECORD;
    delete_count INT;
BEGIN
    FOR classification_record IN 
        SELECT DISTINCT table_name, retention_period 
        FROM data_classification 
        WHERE retention_period IS NOT NULL
    LOOP
        -- Delete old records based on retention policy
        EXECUTE format(
            'DELETE FROM %I WHERE created_at < now() - %L',
            classification_record.table_name,
            classification_record.retention_period
        );
        
        GET DIAGNOSTICS delete_count = ROW_COUNT;
        
        -- Log retention action
        INSERT INTO retention_log (
            table_name,
            retention_period,
            records_deleted,
            executed_at
        ) VALUES (
            classification_record.table_name,
            classification_record.retention_period,
            delete_count,
            now()
        );
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Consent management
CREATE TABLE consent_records (
    consent_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    consent_type VARCHAR(50), -- 'MARKETING', 'ANALYTICS', 'FUNCTIONAL'
    consent_given BOOLEAN,
    consent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    consent_method VARCHAR(50), -- 'WEB_FORM', 'EMAIL', 'PHONE'
    ip_address INET,
    user_agent TEXT
);

-- Audit trail for GDPR compliance
CREATE TABLE gdpr_audit_log (
    audit_id SERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    record_id INT,
    action VARCHAR(50), -- 'ACCESS', 'MODIFY', 'DELETE', 'EXPORT'
    user_id VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    details JSONB
);
```

### 59. How do you design for database scalability patterns?
**Answer:**
```sql
-- Horizontal sharding implementation
CREATE TABLE shard_map (
    shard_id INT PRIMARY KEY,
    shard_name VARCHAR(50),
    connection_string TEXT,
    min_hash_value BIGINT,
    max_hash_value BIGINT,
    status VARCHAR(20) DEFAULT 'ACTIVE'
);

-- Sharding function
CREATE OR REPLACE FUNCTION get_shard_id(entity_id BIGINT)
RETURNS INT AS $$
DECLARE
    hash_value BIGINT;
    shard_record RECORD;
BEGIN
    -- Calculate hash
    hash_value := abs(hashtext(entity_id::TEXT));
    
    -- Find appropriate shard
    SELECT shard_id INTO shard_record
    FROM shard_map
    WHERE hash_value BETWEEN min_hash_value AND max_hash_value
      AND status = 'ACTIVE'
    LIMIT 1;
    
    RETURN shard_record.shard_id;
END;
$$ LANGUAGE plpgsql;

-- Vertical partitioning for large tables
-- Hot data (frequently accessed)
CREATE TABLE user_sessions_hot (
    session_id UUID PRIMARY KEY,
    user_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
) PARTITION BY RANGE (created_at);

-- Cold data (archived)
CREATE TABLE user_sessions_cold (
    session_id UUID PRIMARY KEY,
    user_id BIGINT NOT NULL,
    created_at TIMESTAMP,
    ended_at TIMESTAMP,
    session_duration INTERVAL,
    total_page_views INT
);

-- Read replica routing
CREATE OR REPLACE FUNCTION route_query(query_type VARCHAR)
RETURNS TEXT AS $$
BEGIN
    CASE query_type
        WHEN 'READ' THEN
            RETURN 'replica_connection_string';
        WHEN 'write' THEN
            RETURN 'master_connection_string';
        WHEN 'analytics' THEN
            RETURN 'analytics_replica_connection_string';
        ELSE
            RETURN 'master_connection_string';
    END CASE;
END;
$$ LANGUAGE plpgsql;

-- Database connection load balancing
CREATE TABLE connection_pools (
    pool_name VARCHAR(50) PRIMARY KEY,
    connection_string TEXT,
    max_connections INT,
    current_connections INT DEFAULT 0,
    pool_type VARCHAR(20), -- 'MASTER', 'REPLICA', 'ANALYTICS'
    weight INT DEFAULT 1,
    status VARCHAR(20) DEFAULT 'ACTIVE'
);

-- Auto-scaling trigger
CREATE OR REPLACE FUNCTION check_scaling_needs()
RETURNS void AS $$
DECLARE
    cpu_usage FLOAT;
    connection_count INT;
    avg_query_time FLOAT;
BEGIN
    -- Get current metrics
    SELECT COUNT(*) INTO connection_count FROM pg_stat_activity;
    
    -- Check if scaling is needed
    IF connection_count > 80 THEN
        -- Trigger scale-out notification
        INSERT INTO scaling_events (event_type, metric_value, threshold, timestamp)
        VALUES ('SCALE_OUT_NEEDED', connection_count, 80, now());
    END IF;
    
    -- Check query performance
    SELECT AVG(mean_time) INTO avg_query_time
    FROM pg_stat_statements
    WHERE calls > 100;
    
    IF avg_query_time > 1000 THEN -- 1 second
        INSERT INTO scaling_events (event_type, metric_value, threshold, timestamp)
        VALUES ('PERFORMANCE_DEGRADATION', avg_query_time, 1000, now());
    END IF;
END;
$$ LANGUAGE plpgsql;
```

### 60. What are microservices database patterns?
**Answer:**
```sql
-- Database per Service pattern
-- Service 1: User Service Database
CREATE DATABASE user_service_db;

-- Service 2: Order Service Database  
CREATE DATABASE order_service_db;

-- Service 3: Inventory Service Database
CREATE DATABASE inventory_service_db;

-- Saga pattern for distributed transactions
-- Order saga implementation
CREATE TABLE saga_transactions (
    saga_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    saga_type VARCHAR(50),
    status VARCHAR(20), -- 'STARTED', 'COMPLETED', 'FAILED', 'COMPENSATING'
    current_step INT DEFAULT 1,
    total_steps INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payload JSONB
);

CREATE TABLE saga_steps (
    step_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    saga_id UUID REFERENCES saga_transactions(saga_id),
    step_number INT,
    service_name VARCHAR(50),
    action VARCHAR(50),
    compensation_action VARCHAR(50),
    status VARCHAR(20), -- 'PENDING', 'COMPLETED', 'FAILED', 'COMPENSATED'
    request_payload JSONB,
    response_payload JSONB,
    executed_at TIMESTAMP,
    compensated_at TIMESTAMP
);

-- Saga orchestrator function
CREATE OR REPLACE FUNCTION execute_order_saga(order_data JSONB)
RETURNS UUID AS $$
DECLARE
    saga_id UUID;
    step_record RECORD;
BEGIN
    -- Create saga transaction
    INSERT INTO saga_transactions (saga_type, total_steps, payload)
    VALUES ('CREATE_ORDER', 4, order_data)
    RETURNING saga_transactions.saga_id INTO saga_id;
    
    -- Define saga steps
    INSERT INTO saga_steps (saga_id, step_number, service_name, action, compensation_action)
    VALUES 
        (saga_id, 1, 'inventory_service', 'reserve_items', 'release_items'),
        (saga_id, 2, 'payment_service', 'charge_payment', 'refund_payment'),
        (saga_id, 3, 'shipping_service', 'create_shipment', 'cancel_shipment'),
        (saga_id, 4, 'order_service', 'create_order', 'cancel_order');
    
    -- Execute first step
    PERFORM execute_saga_step(saga_id, 1);
    
    RETURN saga_id;
END;
$$ LANGUAGE plpgsql;

-- Event sourcing pattern
CREATE TABLE event_store (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_id UUID NOT NULL,
    aggregate_type VARCHAR(50) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_version INT NOT NULL,
    event_data JSONB NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(aggregate_id, event_version)
);

-- Event projection for read models
CREATE MATERIALIZED VIEW order_projection AS
SELECT 
    aggregate_id as order_id,
    (event_data->>'customer_id')::UUID as customer_id,
    (event_data->>'total_amount')::DECIMAL as total_amount,
    CASE 
        WHEN event_type = 'OrderCreated' THEN 'CREATED'
        WHEN event_type = 'OrderPaid' THEN 'PAID'
        WHEN event_type = 'OrderShipped' THEN 'SHIPPED'
        WHEN event_type = 'OrderCancelled' THEN 'CANCELLED'
    END as status,
    created_at
FROM event_store
WHERE aggregate_type = 'Order'
  AND event_type IN ('OrderCreated', 'OrderPaid', 'OrderShipped', 'OrderCancelled');

-- CQRS pattern implementation
-- Command side (write model)
CREATE TABLE order_commands (
    command_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    command_type VARCHAR(50),
    aggregate_id UUID,
    command_data JSONB,
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Query side (read model)
CREATE TABLE order_read_model (
    order_id UUID PRIMARY KEY,
    customer_id UUID,
    order_number VARCHAR(50),
    status VARCHAR(20),
    total_amount DECIMAL(12,2),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Outbox pattern for reliable messaging
CREATE TABLE outbox_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_id UUID NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB NOT NULL,
    published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP
);

-- Publish events function
CREATE OR REPLACE FUNCTION publish_outbox_events()
RETURNS void AS $$
DECLARE
    event_record RECORD;
BEGIN
    FOR event_record IN 
        SELECT * FROM outbox_events 
        WHERE published = FALSE 
        ORDER BY created_at 
        LIMIT 100
    LOOP
        -- Publish to message broker (implementation specific)
        -- PERFORM publish_to_kafka(event_record.event_type, event_record.event_data);
        
        -- Mark as published
        UPDATE outbox_events 
        SET published = TRUE, published_at = now()
        WHERE event_id = event_record.event_id;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```
### 61. How do you implement database change data capture (CDC)?
**Answer:**
```sql
-- Trigger-based CDC
CREATE TABLE customer_changes (
    change_id SERIAL PRIMARY KEY,
    customer_id INT,
    operation VARCHAR(10), -- 'INSERT', 'UPDATE', 'DELETE'
    old_values JSONB,
    new_values JSONB,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_by VARCHAR(50) DEFAULT current_user
);

CREATE OR REPLACE FUNCTION capture_customer_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO customer_changes (customer_id, operation, new_values)
        VALUES (NEW.customer_id, 'INSERT', row_to_json(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO customer_changes (customer_id, operation, old_values, new_values)
        VALUES (NEW.customer_id, 'UPDATE', row_to_json(OLD), row_to_json(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO customer_changes (customer_id, operation, old_values)
        VALUES (OLD.customer_id, 'DELETE', row_to_json(OLD));
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER customer_cdc_trigger
    AFTER INSERT OR UPDATE OR DELETE ON customers
    FOR EACH ROW EXECUTE FUNCTION capture_customer_changes();

-- Log-based CDC using WAL
-- Enable logical replication
ALTER SYSTEM SET wal_level = 'logical';
ALTER SYSTEM SET max_replication_slots = 4;
ALTER SYSTEM SET max_wal_senders = 4;

-- Create publication for CDC
CREATE PUBLICATION cdc_publication FOR TABLE customers, orders, products;

-- Create replication slot
SELECT pg_create_logical_replication_slot('cdc_slot', 'pgoutput');

-- CDC consumer function
CREATE OR REPLACE FUNCTION process_cdc_changes()
RETURNS void AS $$
DECLARE
    change_record RECORD;
BEGIN
    -- Get changes from replication slot
    FOR change_record IN 
        SELECT * FROM pg_logical_slot_get_changes('cdc_slot', NULL, NULL)
    LOOP
        -- Process change based on operation
        CASE 
            WHEN change_record.data LIKE '%INSERT%' THEN
                PERFORM handle_insert_change(change_record.data);
            WHEN change_record.data LIKE '%UPDATE%' THEN
                PERFORM handle_update_change(change_record.data);
            WHEN change_record.data LIKE '%DELETE%' THEN
                PERFORM handle_delete_change(change_record.data);
        END CASE;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Timestamp-based CDC
CREATE OR REPLACE FUNCTION get_changes_since(since_timestamp TIMESTAMP)
RETURNS TABLE(
    table_name TEXT,
    operation TEXT,
    record_data JSONB,
    change_timestamp TIMESTAMP
) AS $$
BEGIN
    -- Get customer changes
    RETURN QUERY
    SELECT 
        'customers'::TEXT,
        cc.operation::TEXT,
        cc.new_values,
        cc.changed_at
    FROM customer_changes cc
    WHERE cc.changed_at > since_timestamp;
    
    -- Add other tables as needed
    -- RETURN QUERY SELECT ...
END;
$$ LANGUAGE plpgsql;
```

### 62. What are database anti-patterns to avoid?
**Answer:**
```sql
-- ANTI-PATTERN 1: God Object/Wide Table
-- BAD: Single table with too many columns
CREATE TABLE user_everything (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    -- Profile info
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    birth_date DATE,
    -- Address info
    street VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(50),
    -- Preferences (50+ columns)
    pref_color VARCHAR(20),
    pref_theme VARCHAR(20)
    -- ... many more columns
);

-- GOOD: Normalized design
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE user_profiles (
    user_id INT PRIMARY KEY REFERENCES users(user_id),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    birth_date DATE
);

-- ANTI-PATTERN 2: Polymorphic Associations
-- BAD: Generic foreign key
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    commentable_id INT,
    commentable_type VARCHAR(50), -- 'Post', 'Photo', 'Video'
    content TEXT
);

-- GOOD: Specific associations
CREATE TABLE post_comments (
    id SERIAL PRIMARY KEY,
    post_id INT REFERENCES posts(id),
    content TEXT
);

CREATE TABLE photo_comments (
    id SERIAL PRIMARY KEY,
    photo_id INT REFERENCES photos(id),
    content TEXT
);

-- ANTI-PATTERN 3: Entity-Attribute-Value (EAV)
-- BAD: Generic attribute storage
CREATE TABLE object_attributes (
    object_id INT,
    attribute_name VARCHAR(50),
    attribute_value TEXT
);

-- GOOD: Proper columns or JSON for flexibility
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10,2),
    attributes JSONB -- For flexible attributes
);

-- ANTI-PATTERN 4: Implicit Columns
-- BAD: Storing multiple values in one column
CREATE TABLE orders_bad (
    order_id SERIAL PRIMARY KEY,
    product_ids TEXT -- '1,2,3,4'
);

-- GOOD: Proper junction table
CREATE TABLE order_items (
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity INT,
    PRIMARY KEY (order_id, product_id)
);

-- ANTI-PATTERN 5: Fear of Unknown (NULL phobia)
-- BAD: Using magic values instead of NULL
UPDATE customers SET phone = 'N/A' WHERE phone IS NULL;
UPDATE customers SET birth_date = '1900-01-01' WHERE birth_date IS NULL;

-- GOOD: Embrace NULL for unknown values
SELECT name, COALESCE(phone, 'Not provided') as phone_display
FROM customers;

-- ANTI-PATTERN 6: Keyless Entry
-- BAD: No primary key
CREATE TABLE log_entries (
    timestamp TIMESTAMP,
    message TEXT,
    level VARCHAR(10)
);

-- GOOD: Always have a primary key
CREATE TABLE log_entries (
    log_id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    message TEXT,
    level VARCHAR(10)
);
```

### 63. How do you design for database observability and monitoring?
**Answer:**
```sql
-- Performance metrics collection
CREATE TABLE performance_metrics (
    metric_id SERIAL PRIMARY KEY,
    metric_name VARCHAR(100),
    metric_value DECIMAL(15,4),
    metric_unit VARCHAR(20),
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tags JSONB
);

-- Collect database metrics
CREATE OR REPLACE FUNCTION collect_db_metrics()
RETURNS void AS $$
BEGIN
    -- Connection metrics
    INSERT INTO performance_metrics (metric_name, metric_value, metric_unit, tags)
    SELECT 
        'active_connections',
        COUNT(*),
        'count',
        json_build_object('state', state)
    FROM pg_stat_activity
    GROUP BY state;
    
    -- Query performance metrics
    INSERT INTO performance_metrics (metric_name, metric_value, metric_unit, tags)
    SELECT 
        'avg_query_time',
        mean_time,
        'milliseconds',
        json_build_object('query_hash', queryid::TEXT)
    FROM pg_stat_statements
    WHERE calls > 10
    ORDER BY mean_time DESC
    LIMIT 10;
    
    -- Database size metrics
    INSERT INTO performance_metrics (metric_name, metric_value, metric_unit, tags)
    SELECT 
        'database_size',
        pg_database_size(datname),
        'bytes',
        json_build_object('database', datname)
    FROM pg_database
    WHERE datname NOT IN ('template0', 'template1', 'postgres');
    
    -- Cache hit ratio
    INSERT INTO performance_metrics (metric_name, metric_value, metric_unit)
    SELECT 
        'cache_hit_ratio',
        ROUND(
            (sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read))) * 100, 2
        ),
        'percentage'
    FROM pg_statio_user_tables
    WHERE heap_blks_read > 0;
END;
$$ LANGUAGE plpgsql;

-- Query performance monitoring
CREATE VIEW slow_queries AS
SELECT 
    queryid,
    query,
    calls,
    total_time,
    mean_time,
    max_time,
    stddev_time,
    rows,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements
WHERE mean_time > 100 -- Queries taking more than 100ms on average
ORDER BY mean_time DESC;

-- Lock monitoring
CREATE VIEW current_locks AS
SELECT 
    pl.pid,
    pa.usename,
    pa.application_name,
    pl.locktype,
    pl.mode,
    pl.granted,
    pa.query_start,
    pa.query
FROM pg_locks pl
JOIN pg_stat_activity pa ON pl.pid = pa.pid
WHERE NOT pl.granted
ORDER BY pa.query_start;

-- Blocking queries detection
CREATE OR REPLACE FUNCTION detect_blocking_queries()
RETURNS TABLE(
    blocked_pid INT,
    blocked_user TEXT,
    blocking_pid INT,
    blocking_user TEXT,
    blocked_query TEXT,
    blocking_query TEXT,
    block_duration INTERVAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        blocked_locks.pid::INT,
        blocked_activity.usename::TEXT,
        blocking_locks.pid::INT,
        blocking_activity.usename::TEXT,
        blocked_activity.query::TEXT,
        blocking_activity.query::TEXT,
        (now() - blocked_activity.query_start)::INTERVAL
    FROM pg_catalog.pg_locks blocked_locks
    JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
    JOIN pg_catalog.pg_locks blocking_locks ON (
        blocking_locks.locktype = blocked_locks.locktype AND
        blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database AND
        blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation AND
        blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page AND
        blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple AND
        blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid AND
        blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid AND
        blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid AND
        blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid AND
        blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid AND
        blocking_locks.pid != blocked_locks.pid
    )
    JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
    WHERE NOT blocked_locks.granted;
END;
$$ LANGUAGE plpgsql;

-- Alerting system
CREATE TABLE alert_rules (
    rule_id SERIAL PRIMARY KEY,
    rule_name VARCHAR(100),
    metric_name VARCHAR(100),
    threshold_value DECIMAL(15,4),
    comparison_operator VARCHAR(10), -- '>', '<', '>=', '<=', '='
    severity VARCHAR(20), -- 'INFO', 'WARNING', 'CRITICAL'
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE alerts (
    alert_id SERIAL PRIMARY KEY,
    rule_id INT REFERENCES alert_rules(rule_id),
    metric_value DECIMAL(15,4),
    threshold_value DECIMAL(15,4),
    severity VARCHAR(20),
    message TEXT,
    triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'ACTIVE' -- 'ACTIVE', 'RESOLVED', 'ACKNOWLEDGED'
);

-- Alert evaluation function
CREATE OR REPLACE FUNCTION evaluate_alerts()
RETURNS void AS $$
DECLARE
    rule_record RECORD;
    current_value DECIMAL(15,4);
    alert_triggered BOOLEAN;
BEGIN
    FOR rule_record IN SELECT * FROM alert_rules WHERE is_active = TRUE LOOP
        -- Get current metric value
        SELECT metric_value INTO current_value
        FROM performance_metrics
        WHERE metric_name = rule_record.metric_name
        ORDER BY collected_at DESC
        LIMIT 1;
        
        -- Evaluate threshold
        alert_triggered := CASE rule_record.comparison_operator
            WHEN '>' THEN current_value > rule_record.threshold_value
            WHEN '<' THEN current_value < rule_record.threshold_value
            WHEN '>=' THEN current_value >= rule_record.threshold_value
            WHEN '<=' THEN current_value <= rule_record.threshold_value
            WHEN '=' THEN current_value = rule_record.threshold_value
            ELSE FALSE
        END;
        
        -- Create alert if triggered
        IF alert_triggered THEN
            INSERT INTO alerts (rule_id, metric_value, threshold_value, severity, message)
            VALUES (
                rule_record.rule_id,
                current_value,
                rule_record.threshold_value,
                rule_record.severity,
                format('%s: %s %s %s (current: %s)',
                    rule_record.rule_name,
                    rule_record.metric_name,
                    rule_record.comparison_operator,
                    rule_record.threshold_value,
                    current_value
                )
            );
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Health check endpoint
CREATE OR REPLACE FUNCTION database_health_check()
RETURNS JSON AS $$
DECLARE
    health_status JSON;
BEGIN
    SELECT json_build_object(
        'status', 'healthy',
        'timestamp', now(),
        'metrics', json_build_object(
            'active_connections', (SELECT count(*) FROM pg_stat_activity),
            'database_size_mb', (SELECT pg_size_pretty(pg_database_size(current_database()))),
            'cache_hit_ratio', (
                SELECT ROUND(
                    (sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read))) * 100, 2
                )
                FROM pg_statio_user_tables
                WHERE heap_blks_read > 0
            ),
            'slow_queries_count', (SELECT count(*) FROM slow_queries),
            'blocking_queries_count', (SELECT count(*) FROM detect_blocking_queries())
        )
    ) INTO health_status;
    
    RETURN health_status;
END;
$$ LANGUAGE plpgsql;
```

### 64. How do you implement database disaster recovery testing?
**Answer:**
```sql
-- DR test framework
CREATE TABLE dr_test_scenarios (
    scenario_id SERIAL PRIMARY KEY,
    scenario_name VARCHAR(100),
    description TEXT,
    test_type VARCHAR(50), -- 'BACKUP_RESTORE', 'FAILOVER', 'SPLIT_BRAIN'
    expected_rto_minutes INT, -- Recovery Time Objective
    expected_rpo_minutes INT, -- Recovery Point Objective
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE dr_test_executions (
    execution_id SERIAL PRIMARY KEY,
    scenario_id INT REFERENCES dr_test_scenarios(scenario_id),
    test_start_time TIMESTAMP,
    test_end_time TIMESTAMP,
    actual_rto_minutes INT,
    actual_rpo_minutes INT,
    status VARCHAR(20), -- 'RUNNING', 'PASSED', 'FAILED'
    test_results JSONB,
    notes TEXT
);

-- Backup restore test
CREATE OR REPLACE FUNCTION test_backup_restore(backup_file TEXT)
RETURNS JSON AS $$
DECLARE
    test_db_name TEXT;
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    test_result JSON;
    record_count_original INT;
    record_count_restored INT;
BEGIN
    start_time := clock_timestamp();
    test_db_name := 'dr_test_' || extract(epoch from now())::TEXT;
    
    -- Create test database
    EXECUTE format('CREATE DATABASE %I', test_db_name);
    
    -- Restore backup
    EXECUTE format('pg_restore -d %I %L', test_db_name, backup_file);
    
    -- Verify data integrity
    EXECUTE format('SELECT count(*) FROM %I.customers', test_db_name) INTO record_count_restored;
    SELECT count(*) INTO record_count_original FROM customers;
    
    end_time := clock_timestamp();
    
    -- Build test result
    SELECT json_build_object(
        'test_type', 'BACKUP_RESTORE',
        'duration_minutes', EXTRACT(EPOCH FROM (end_time - start_time)) / 60,
        'original_record_count', record_count_original,
        'restored_record_count', record_count_restored,
        'data_integrity_check', record_count_original = record_count_restored,
        'backup_file', backup_file,
        'test_database', test_db_name
    ) INTO test_result;
    
    -- Cleanup test database
    EXECUTE format('DROP DATABASE %I', test_db_name);
    
    RETURN test_result;
END;
$$ LANGUAGE plpgsql;

-- Failover test
CREATE OR REPLACE FUNCTION test_failover_scenario()
RETURNS JSON AS $$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    failover_successful BOOLEAN;
    test_result JSON;
BEGIN
    start_time := clock_timestamp();
    
    -- Simulate primary failure
    -- In real scenario, this would involve stopping primary server
    
    -- Check if standby can be promoted
    BEGIN
        -- Attempt to promote standby (pseudo-code)
        -- PERFORM pg_promote();
        failover_successful := TRUE;
    EXCEPTION WHEN OTHERS THEN
        failover_successful := FALSE;
    END;
    
    end_time := clock_timestamp();
    
    SELECT json_build_object(
        'test_type', 'FAILOVER',
        'duration_minutes', EXTRACT(EPOCH FROM (end_time - start_time)) / 60,
        'failover_successful', failover_successful,
        'new_primary_status', 'ACTIVE', -- Check actual status
        'replication_lag_seconds', 0 -- Check actual lag
    ) INTO test_result;
    
    RETURN test_result;
END;
$$ LANGUAGE plpgsql;

-- Comprehensive DR test suite
CREATE OR REPLACE FUNCTION run_dr_test_suite()
RETURNS TABLE(
    test_name TEXT,
    status TEXT,
    duration_minutes NUMERIC,
    rto_met BOOLEAN,
    rpo_met BOOLEAN,
    details JSON
) AS $$
DECLARE
    scenario_record RECORD;
    execution_id INT;
    test_start TIMESTAMP;
    test_end TIMESTAMP;
    test_results JSON;
BEGIN
    FOR scenario_record IN 
        SELECT * FROM dr_test_scenarios WHERE is_active = TRUE
    LOOP
        test_start := clock_timestamp();
        
        -- Insert test execution record
        INSERT INTO dr_test_executions (scenario_id, test_start_time, status)
        VALUES (scenario_record.scenario_id, test_start, 'RUNNING')
        RETURNING execution_id INTO execution_id;
        
        -- Execute test based on type
        CASE scenario_record.test_type
            WHEN 'BACKUP_RESTORE' THEN
                test_results := test_backup_restore('/backup/latest.sql');
            WHEN 'FAILOVER' THEN
                test_results := test_failover_scenario();
            ELSE
                test_results := json_build_object('error', 'Unknown test type');
        END CASE;
        
        test_end := clock_timestamp();
        
        -- Update execution record
        UPDATE dr_test_executions
        SET 
            test_end_time = test_end,
            actual_rto_minutes = EXTRACT(EPOCH FROM (test_end - test_start)) / 60,
            status = CASE WHEN test_results->>'error' IS NULL THEN 'PASSED' ELSE 'FAILED' END,
            test_results = test_results
        WHERE dr_test_executions.execution_id = run_dr_test_suite.execution_id;
        
        -- Return test result
        RETURN QUERY SELECT 
            scenario_record.scenario_name::TEXT,
            CASE WHEN test_results->>'error' IS NULL THEN 'PASSED' ELSE 'FAILED' END::TEXT,
            EXTRACT(EPOCH FROM (test_end - test_start)) / 60,
            (EXTRACT(EPOCH FROM (test_end - test_start)) / 60) <= scenario_record.expected_rto_minutes,
            TRUE, -- RPO check would be more complex
            test_results;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Automated DR testing schedule
CREATE OR REPLACE FUNCTION schedule_dr_tests()
RETURNS void AS $$
BEGIN
    -- Weekly backup restore test
    IF EXTRACT(DOW FROM now()) = 1 THEN -- Monday
        PERFORM run_dr_test_suite();
    END IF;
    
    -- Monthly failover test
    IF EXTRACT(DAY FROM now()) = 1 THEN -- First day of month
        PERFORM test_failover_scenario();
    END IF;
    
    -- Log scheduled execution
    INSERT INTO dr_test_log (test_date, test_type, status)
    VALUES (now(), 'SCHEDULED', 'COMPLETED');
END;
$$ LANGUAGE plpgsql;
```

### 65. What are database capacity planning strategies?
**Answer:**
```sql
-- Capacity metrics collection
CREATE TABLE capacity_metrics (
    metric_id SERIAL PRIMARY KEY,
    metric_date DATE,
    database_size_bytes BIGINT,
    table_count INT,
    index_count INT,
    connection_count_max INT,
    connection_count_avg DECIMAL(8,2),
    query_count_daily BIGINT,
    cpu_usage_avg DECIMAL(5,2),
    memory_usage_avg DECIMAL(5,2),
    disk_io_read_mb DECIMAL(12,2),
    disk_io_write_mb DECIMAL(12,2)
);

-- Collect daily capacity metrics
CREATE OR REPLACE FUNCTION collect_capacity_metrics()
RETURNS void AS $$
DECLARE
    today_date DATE := CURRENT_DATE;
BEGIN
    INSERT INTO capacity_metrics (
        metric_date,
        database_size_bytes,
        table_count,
        index_count,
        connection_count_max,
        connection_count_avg,
        query_count_daily
    )
    SELECT 
        today_date,
        pg_database_size(current_database()),
        (SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public'),
        (SELECT count(*) FROM pg_indexes WHERE schemaname = 'public'),
        (SELECT max(numbackends) FROM pg_stat_database WHERE datname = current_database()),
        (SELECT avg(numbackends) FROM pg_stat_database WHERE datname = current_database()),
        (SELECT sum(calls) FROM pg_stat_statements)
    ON CONFLICT (metric_date) DO UPDATE SET
        database_size_bytes = EXCLUDED.database_size_bytes,
        table_count = EXCLUDED.table_count,
        index_count = EXCLUDED.index_count,
        connection_count_max = EXCLUDED.connection_count_max,
        connection_count_avg = EXCLUDED.connection_count_avg,
        query_count_daily = EXCLUDED.query_count_daily;
END;
$$ LANGUAGE plpgsql;

-- Growth trend analysis
CREATE OR REPLACE FUNCTION analyze_growth_trends(days_back INT DEFAULT 90)
RETURNS TABLE(
    metric_name TEXT,
    current_value DECIMAL,
    growth_rate_daily DECIMAL,
    projected_30_days DECIMAL,
    projected_90_days DECIMAL,
    projected_365_days DECIMAL
) AS $$
BEGIN
    -- Database size growth
    RETURN QUERY
    WITH growth_calc AS (
        SELECT 
            database_size_bytes::DECIMAL / (1024*1024*1024) as size_gb,
            metric_date,
            LAG(database_size_bytes::DECIMAL / (1024*1024*1024)) OVER (ORDER BY metric_date) as prev_size_gb
        FROM capacity_metrics
        WHERE metric_date >= CURRENT_DATE - days_back
        ORDER BY metric_date
    )
    SELECT 
        'Database Size (GB)'::TEXT,
        (SELECT size_gb FROM growth_calc ORDER BY metric_date DESC LIMIT 1),
        AVG(size_gb - prev_size_gb) as daily_growth,
        (SELECT size_gb FROM growth_calc ORDER BY metric_date DESC LIMIT 1) + (AVG(size_gb - prev_size_gb) * 30),
        (SELECT size_gb FROM growth_calc ORDER BY metric_date DESC LIMIT 1) + (AVG(size_gb - prev_size_gb) * 90),
        (SELECT size_gb FROM growth_calc ORDER BY metric_date DESC LIMIT 1) + (AVG(size_gb - prev_size_gb) * 365)
    FROM growth_calc
    WHERE prev_size_gb IS NOT NULL;
    
    -- Connection count growth
    RETURN QUERY
    WITH conn_growth AS (
        SELECT 
            connection_count_avg,
            metric_date,
            LAG(connection_count_avg) OVER (ORDER BY metric_date) as prev_conn_avg
        FROM capacity_metrics
        WHERE metric_date >= CURRENT_DATE - days_back
        ORDER BY metric_date
    )
    SELECT 
        'Average Connections'::TEXT,
        (SELECT connection_count_avg FROM conn_growth ORDER BY metric_date DESC LIMIT 1),
        AVG(connection_count_avg - prev_conn_avg),
        (SELECT connection_count_avg FROM conn_growth ORDER BY metric_date DESC LIMIT 1) + (AVG(connection_count_avg - prev_conn_avg) * 30),
        (SELECT connection_count_avg FROM conn_growth ORDER BY metric_date DESC LIMIT 1) + (AVG(connection_count_avg - prev_conn_avg) * 90),
        (SELECT connection_count_avg FROM conn_growth ORDER BY metric_date DESC LIMIT 1) + (AVG(connection_count_avg - prev_conn_avg) * 365)
    FROM conn_growth
    WHERE prev_conn_avg IS NOT NULL;
END;
$$ LANGUAGE plpgsql;

-- Capacity threshold alerts
CREATE TABLE capacity_thresholds (
    threshold_id SERIAL PRIMARY KEY,
    metric_name VARCHAR(100),
    warning_threshold DECIMAL(15,4),
    critical_threshold DECIMAL(15,4),
    threshold_unit VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE
);

-- Insert default thresholds
INSERT INTO capacity_thresholds (metric_name, warning_threshold, critical_threshold, threshold_unit) VALUES
('database_size_gb', 800, 900, 'GB'),
('connection_count_max', 80, 95, 'count'),
('cpu_usage_avg', 70, 85, 'percentage'),
('memory_usage_avg', 75, 90, 'percentage'),
('disk_usage_percentage', 80, 90, 'percentage');

-- Check capacity thresholds
CREATE OR REPLACE FUNCTION check_capacity_thresholds()
RETURNS TABLE(
    metric_name TEXT,
    current_value DECIMAL,
    threshold_type TEXT,
    threshold_value DECIMAL,
    severity TEXT
) AS $$
DECLARE
    threshold_record RECORD;
    current_metric_value DECIMAL;
BEGIN
    FOR threshold_record IN SELECT * FROM capacity_thresholds WHERE is_active = TRUE LOOP
        -- Get current metric value
        CASE threshold_record.metric_name
            WHEN 'database_size_gb' THEN
                SELECT database_size_bytes::DECIMAL / (1024*1024*1024) INTO current_metric_value
                FROM capacity_metrics ORDER BY metric_date DESC LIMIT 1;
            WHEN 'connection_count_max' THEN
                SELECT connection_count_max INTO current_metric_value
                FROM capacity_metrics ORDER BY metric_date DESC LIMIT 1;
            -- Add other metrics as needed
        END CASE;
        
        -- Check thresholds
        IF current_metric_value >= threshold_record.critical_threshold THEN
            RETURN QUERY SELECT 
                threshold_record.metric_name::TEXT,
                current_metric_value,
                'CRITICAL'::TEXT,
                threshold_record.critical_threshold,
                'CRITICAL'::TEXT;
        ELSIF current_metric_value >= threshold_record.warning_threshold THEN
            RETURN QUERY SELECT 
                threshold_record.metric_name::TEXT,
                current_metric_value,
                'WARNING'::TEXT,
                threshold_record.warning_threshold,
                'WARNING'::TEXT;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Capacity planning recommendations
CREATE OR REPLACE FUNCTION generate_capacity_recommendations()
RETURNS TABLE(
    recommendation_type TEXT,
    priority TEXT,
    description TEXT,
    estimated_timeline TEXT,
    estimated_cost_impact TEXT
) AS $$
DECLARE
    db_size_gb DECIMAL;
    growth_rate DECIMAL;
    connection_usage DECIMAL;
BEGIN
    -- Get current metrics
    SELECT database_size_bytes::DECIMAL / (1024*1024*1024) INTO db_size_gb
    FROM capacity_metrics ORDER BY metric_date DESC LIMIT 1;
    
    SELECT growth_rate_daily INTO growth_rate
    FROM analyze_growth_trends(30) 
    WHERE metric_name = 'Database Size (GB)';
    
    -- Storage recommendations
    IF db_size_gb > 500 AND growth_rate > 1 THEN
        RETURN QUERY SELECT 
            'Storage Upgrade'::TEXT,
            'HIGH'::TEXT,
            'Database size is ' || db_size_gb::TEXT || 'GB with ' || growth_rate::TEXT || 'GB daily growth. Consider storage expansion.'::TEXT,
            '30-60 days'::TEXT,
            'Medium'::TEXT;
    END IF;
    
    -- Performance recommendations
    IF (SELECT connection_count_max FROM capacity_metrics ORDER BY metric_date DESC LIMIT 1) > 80 THEN
        RETURN QUERY SELECT 
            'Connection Pool Optimization'::TEXT,
            'MEDIUM'::TEXT,
            'High connection count detected. Consider connection pooling or read replicas.'::TEXT,
            '2-4 weeks'::TEXT,
            'Low'::TEXT;
    END IF;
    
    -- Archival recommendations
    IF db_size_gb > 1000 THEN
        RETURN QUERY SELECT 
            'Data Archival Strategy'::TEXT,
            'MEDIUM'::TEXT,
            'Large database size. Implement data archival for historical data.'::TEXT,
            '4-8 weeks'::TEXT,
            'Low'::TEXT;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Automated capacity reporting
CREATE OR REPLACE FUNCTION generate_capacity_report()
RETURNS JSON AS $$
DECLARE
    report JSON;
BEGIN
    SELECT json_build_object(
        'report_date', CURRENT_DATE,
        'current_metrics', (
            SELECT json_build_object(
                'database_size_gb', database_size_bytes::DECIMAL / (1024*1024*1024),
                'table_count', table_count,
                'connection_count_max', connection_count_max,
                'query_count_daily', query_count_daily
            )
            FROM capacity_metrics 
            ORDER BY metric_date DESC 
            LIMIT 1
        ),
        'growth_trends', (
            SELECT json_agg(
                json_build_object(
                    'metric', metric_name,
                    'current_value', current_value,
                    'daily_growth_rate', growth_rate_daily,
                    'projected_30_days', projected_30_days
                )
            )
            FROM analyze_growth_trends(30)
        ),
        'threshold_alerts', (
            SELECT json_agg(
                json_build_object(
                    'metric', metric_name,
                    'current_value', current_value,
                    'severity', severity,
                    'threshold_value', threshold_value
                )
            )
            FROM check_capacity_thresholds()
        ),
        'recommendations', (
            SELECT json_agg(
                json_build_object(
                    'type', recommendation_type,
                    'priority', priority,
                    'description', description,
                    'timeline', estimated_timeline
                )
            )
            FROM generate_capacity_recommendations()
        )
    ) INTO report;
    
    RETURN report;
END;
$$ LANGUAGE plpgsql;
```
## Performance & Optimization (66-80)

### 66. How do you identify and fix slow queries?
**Answer:**
```sql
-- Enable query statistics
-- PostgreSQL
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';
ALTER SYSTEM SET pg_stat_statements.track = 'all';

-- Find slow queries
SELECT 
    queryid,
    LEFT(query, 100) as query_preview,
    calls,
    total_time,
    mean_time,
    max_time,
    stddev_time,
    rows,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements
WHERE mean_time > 1000 -- Queries taking more than 1 second
ORDER BY mean_time DESC
LIMIT 20;

-- Query optimization example
-- BEFORE: Inefficient query
SELECT c.name, COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.created_date >= '2023-01-01'
GROUP BY c.customer_id, c.name
ORDER BY order_count DESC;

-- Check execution plan
EXPLAIN (ANALYZE, BUFFERS) 
SELECT c.name, COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.created_date >= '2023-01-01'
GROUP BY c.customer_id, c.name
ORDER BY order_count DESC;

-- AFTER: Optimized with proper indexes
CREATE INDEX CONCURRENTLY idx_customers_created_date ON customers(created_date);
CREATE INDEX CONCURRENTLY idx_orders_customer_id ON orders(customer_id);

-- Further optimization with covering index
CREATE INDEX CONCURRENTLY idx_customers_created_name 
ON customers(created_date, customer_id) INCLUDE (name)
WHERE created_date >= '2023-01-01';

-- Query rewrite for better performance
WITH customer_orders AS (
    SELECT 
        c.customer_id,
        c.name,
        COUNT(o.order_id) as order_count
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    WHERE c.created_date >= '2023-01-01'
    GROUP BY c.customer_id, c.name
)
SELECT name, order_count
FROM customer_orders
ORDER BY order_count DESC;

-- Monitoring query performance over time
CREATE TABLE query_performance_history (
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    queryid BIGINT,
    query_text TEXT,
    calls BIGINT,
    total_time DOUBLE PRECISION,
    mean_time DOUBLE PRECISION,
    hit_percent DOUBLE PRECISION
);

-- Function to capture query stats
CREATE OR REPLACE FUNCTION capture_query_stats()
RETURNS void AS $$
BEGIN
    INSERT INTO query_performance_history (queryid, query_text, calls, total_time, mean_time, hit_percent)
    SELECT 
        queryid,
        LEFT(query, 500),
        calls,
        total_time,
        mean_time,
        100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0)
    FROM pg_stat_statements
    WHERE calls > 100 AND mean_time > 100;
    
    -- Reset stats after capture
    SELECT pg_stat_statements_reset();
END;
$$ LANGUAGE plpgsql;
```

### 67. What are database indexing strategies and best practices?
**Answer:**
```sql
-- B-Tree indexes (default)
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_orders_date ON orders(order_date);

-- Composite indexes (order matters)
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
CREATE INDEX idx_orders_date_customer ON orders(order_date, customer_id);

-- Covering indexes (include additional columns)
CREATE INDEX idx_orders_customer_covering 
ON orders(customer_id) INCLUDE (order_date, total_amount);

-- Partial indexes (with WHERE clause)
CREATE INDEX idx_active_orders ON orders(order_date) 
WHERE status = 'ACTIVE';

CREATE INDEX idx_recent_orders ON orders(customer_id, order_date)
WHERE order_date >= CURRENT_DATE - INTERVAL '30 days';

-- Functional indexes
CREATE INDEX idx_customers_email_lower ON customers(LOWER(email));
CREATE INDEX idx_orders_year ON orders(EXTRACT(YEAR FROM order_date));

-- Hash indexes (for equality only)
CREATE INDEX idx_customers_status_hash ON customers USING HASH(status);

-- GIN indexes (for arrays, JSON, full-text search)
CREATE INDEX idx_products_tags ON products USING GIN(tags);
CREATE INDEX idx_customers_preferences ON customers USING GIN(preferences);

-- Full-text search indexes
ALTER TABLE products ADD COLUMN search_vector tsvector;
UPDATE products SET search_vector = to_tsvector('english', name || ' ' || description);
CREATE INDEX idx_products_search ON products USING GIN(search_vector);

-- Index usage monitoring
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

-- Unused indexes detection
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexrelname NOT LIKE '%_pkey'
ORDER BY pg_relation_size(indexrelid) DESC;

-- Index maintenance
-- Rebuild fragmented indexes
REINDEX INDEX CONCURRENTLY idx_customers_email;

-- Update statistics
ANALYZE customers;

-- Check index bloat
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size,
    CASE 
        WHEN pg_relation_size(indexrelid) > 100 * 1024 * 1024 THEN 'Consider REINDEX'
        ELSE 'OK'
    END as recommendation
FROM pg_stat_user_indexes
WHERE pg_relation_size(indexrelid) > 10 * 1024 * 1024
ORDER BY pg_relation_size(indexrelid) DESC;

-- Index creation strategy
CREATE OR REPLACE FUNCTION create_optimal_indexes()
RETURNS void AS $$
BEGIN
    -- Analyze query patterns first
    -- Create indexes based on WHERE clauses
    CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_status 
    ON orders(status) WHERE status IN ('PENDING', 'PROCESSING');
    
    -- Create indexes for JOIN conditions
    CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_order_items_order_id 
    ON order_items(order_id);
    
    -- Create indexes for ORDER BY clauses
    CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_created_desc 
    ON orders(created_at DESC);
    
    -- Create composite indexes for common query patterns
    CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_customer_status_date 
    ON orders(customer_id, status, order_date);
END;
$$ LANGUAGE plpgsql;
```

### 68. How do you optimize database queries for large datasets?
**Answer:**
```sql
-- Pagination optimization
-- INEFFICIENT: OFFSET with large values
SELECT * FROM orders 
ORDER BY order_date DESC 
OFFSET 100000 LIMIT 20;

-- EFFICIENT: Cursor-based pagination
SELECT * FROM orders 
WHERE order_date < '2023-06-01 10:30:00'
ORDER BY order_date DESC 
LIMIT 20;

-- Keyset pagination
SELECT * FROM orders 
WHERE (order_date, order_id) < ('2023-06-01 10:30:00', 12345)
ORDER BY order_date DESC, order_id DESC
LIMIT 20;

-- Batch processing for large updates
DO $$
DECLARE
    batch_size INT := 10000;
    processed INT := 0;
    total_rows INT;
BEGIN
    SELECT COUNT(*) INTO total_rows FROM large_table WHERE status = 'PENDING';
    
    WHILE processed < total_rows LOOP
        UPDATE large_table 
        SET status = 'PROCESSED', updated_at = NOW()
        WHERE ctid IN (
            SELECT ctid FROM large_table 
            WHERE status = 'PENDING'
            LIMIT batch_size
        );
        
        processed := processed + batch_size;
        
        -- Commit batch and provide progress
        COMMIT;
        RAISE NOTICE 'Processed % of % rows', processed, total_rows;
        
        -- Optional: pause between batches
        PERFORM pg_sleep(0.1);
    END LOOP;
END $$;

-- Partitioning for large tables
CREATE TABLE orders_partitioned (
    order_id BIGSERIAL,
    customer_id BIGINT,
    order_date DATE,
    amount DECIMAL(12,2),
    status VARCHAR(20)
) PARTITION BY RANGE (order_date);

-- Create monthly partitions
CREATE TABLE orders_2023_01 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2023-01-01') TO ('2023-02-01');

CREATE TABLE orders_2023_02 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2023-02-01') TO ('2023-03-01');

-- Automatic partition creation
CREATE OR REPLACE FUNCTION create_monthly_partition(table_name TEXT, start_date DATE)
RETURNS void AS $$
DECLARE
    partition_name TEXT;
    end_date DATE;
BEGIN
    partition_name := table_name || '_' || to_char(start_date, 'YYYY_MM');
    end_date := start_date + INTERVAL '1 month';
    
    EXECUTE format(
        'CREATE TABLE %I PARTITION OF %I FOR VALUES FROM (%L) TO (%L)',
        partition_name, table_name, start_date, end_date
    );
    
    -- Create indexes on partition
    EXECUTE format(
        'CREATE INDEX %I ON %I (customer_id, order_date)',
        'idx_' || partition_name || '_customer_date',
        partition_name
    );
END;
$$ LANGUAGE plpgsql;

-- Parallel query execution
SET max_parallel_workers_per_gather = 4;
SET parallel_tuple_cost = 0.1;
SET parallel_setup_cost = 1000;

-- Force parallel execution for large aggregations
SELECT /*+ PARALLEL(4) */ 
    customer_id,
    COUNT(*) as order_count,
    SUM(amount) as total_amount
FROM orders_large
WHERE order_date >= '2023-01-01'
GROUP BY customer_id;

-- Materialized views for complex aggregations
CREATE MATERIALIZED VIEW customer_summary AS
SELECT 
    c.customer_id,
    c.name,
    c.email,
    COUNT(o.order_id) as total_orders,
    SUM(o.amount) as lifetime_value,
    AVG(o.amount) as avg_order_value,
    MAX(o.order_date) as last_order_date,
    MIN(o.order_date) as first_order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.email;

-- Incremental refresh strategy
CREATE OR REPLACE FUNCTION refresh_customer_summary_incremental()
RETURNS void AS $$
DECLARE
    last_refresh TIMESTAMP;
BEGIN
    -- Get last refresh time
    SELECT last_refresh_time INTO last_refresh 
    FROM materialized_view_refresh_log 
    WHERE view_name = 'customer_summary';
    
    -- Refresh only changed data
    DELETE FROM customer_summary_temp;
    
    INSERT INTO customer_summary_temp
    SELECT 
        c.customer_id,
        c.name,
        c.email,
        COUNT(o.order_id) as total_orders,
        SUM(o.amount) as lifetime_value,
        AVG(o.amount) as avg_order_value,
        MAX(o.order_date) as last_order_date,
        MIN(o.order_date) as first_order_date
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    WHERE c.updated_at > last_refresh 
       OR o.updated_at > last_refresh
    GROUP BY c.customer_id, c.name, c.email;
    
    -- Merge changes
    MERGE INTO customer_summary cs
    USING customer_summary_temp cst ON cs.customer_id = cst.customer_id
    WHEN MATCHED THEN UPDATE SET
        total_orders = cst.total_orders,
        lifetime_value = cst.lifetime_value,
        avg_order_value = cst.avg_order_value,
        last_order_date = cst.last_order_date
    WHEN NOT MATCHED THEN INSERT VALUES (
        cst.customer_id, cst.name, cst.email, cst.total_orders,
        cst.lifetime_value, cst.avg_order_value, cst.last_order_date, cst.first_order_date
    );
    
    -- Update refresh log
    UPDATE materialized_view_refresh_log 
    SET last_refresh_time = NOW()
    WHERE view_name = 'customer_summary';
END;
$$ LANGUAGE plpgsql;

-- Query optimization with hints and statistics
-- Update table statistics
ANALYZE orders;
ANALYZE customers;

-- Set work memory for large sorts
SET work_mem = '256MB';

-- Optimize join order
SELECT /*+ LEADING(c o) USE_HASH(o) */
    c.name,
    COUNT(o.order_id)
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.created_date >= '2023-01-01'
GROUP BY c.customer_id, c.name;
```

### 69. What are database caching and buffer management strategies?
**Answer:**
```sql
-- Buffer pool configuration
-- PostgreSQL shared_buffers setting
ALTER SYSTEM SET shared_buffers = '4GB';  -- 25% of RAM typically
ALTER SYSTEM SET effective_cache_size = '12GB';  -- Total available cache
ALTER SYSTEM SET work_mem = '256MB';  -- Per-operation memory
ALTER SYSTEM SET maintenance_work_mem = '1GB';  -- For maintenance operations

-- Monitor buffer cache performance
SELECT 
    'Buffer Cache Hit Ratio' as metric,
    ROUND(
        (sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read))) * 100, 2
    ) as hit_ratio_percent
FROM pg_statio_user_tables
WHERE heap_blks_read > 0;

-- Detailed buffer usage by table
SELECT 
    schemaname,
    tablename,
    heap_blks_read,
    heap_blks_hit,
    ROUND(
        (heap_blks_hit::DECIMAL / (heap_blks_hit + heap_blks_read)) * 100, 2
    ) as hit_ratio,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as table_size
FROM pg_statio_user_tables
WHERE heap_blks_read > 0
ORDER BY heap_blks_read DESC;

-- Application-level caching with Redis
-- Cache frequently accessed data
CREATE OR REPLACE FUNCTION get_customer_with_cache(customer_id INT)
RETURNS JSON AS $$
DECLARE
    cache_key TEXT;
    cached_result TEXT;
    customer_data JSON;
BEGIN
    cache_key := 'customer:' || customer_id;
    
    -- Try to get from cache first (pseudo-code)
    -- cached_result := redis_get(cache_key);
    
    IF cached_result IS NOT NULL THEN
        RETURN cached_result::JSON;
    END IF;
    
    -- Get from database
    SELECT json_build_object(
        'customer_id', customer_id,
        'name', name,
        'email', email,
        'total_orders', (
            SELECT COUNT(*) FROM orders WHERE orders.customer_id = customers.customer_id
        ),
        'lifetime_value', (
            SELECT SUM(amount) FROM orders WHERE orders.customer_id = customers.customer_id
        )
    ) INTO customer_data
    FROM customers
    WHERE customers.customer_id = get_customer_with_cache.customer_id;
    
    -- Cache the result (pseudo-code)
    -- PERFORM redis_set(cache_key, customer_data::TEXT, 3600); -- 1 hour TTL
    
    RETURN customer_data;
END;
$$ LANGUAGE plpgsql;

-- Query result caching
CREATE TABLE query_cache (
    cache_key VARCHAR(255) PRIMARY KEY,
    query_result TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    hit_count INT DEFAULT 0
);

CREATE OR REPLACE FUNCTION get_cached_query_result(
    query_hash VARCHAR(255),
    ttl_seconds INT DEFAULT 3600
)
RETURNS TEXT AS $$
DECLARE
    cached_result TEXT;
BEGIN
    SELECT query_result INTO cached_result
    FROM query_cache
    WHERE cache_key = query_hash
      AND expires_at > NOW();
    
    IF FOUND THEN
        -- Update hit count
        UPDATE query_cache 
        SET hit_count = hit_count + 1
        WHERE cache_key = query_hash;
        
        RETURN cached_result;
    END IF;
    
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION cache_query_result(
    query_hash VARCHAR(255),
    result TEXT,
    ttl_seconds INT DEFAULT 3600
)
RETURNS void AS $$
BEGIN
    INSERT INTO query_cache (cache_key, query_result, expires_at)
    VALUES (query_hash, result, NOW() + (ttl_seconds || ' seconds')::INTERVAL)
    ON CONFLICT (cache_key) DO UPDATE SET
        query_result = EXCLUDED.query_result,
        expires_at = EXCLUDED.expires_at,
        created_at = NOW();
END;
$$ LANGUAGE plpgsql;

-- Buffer management for large operations
-- Optimize for sequential scans
SET seq_page_cost = 1.0;
SET random_page_cost = 4.0;

-- For SSD storage
SET seq_page_cost = 1.0;
SET random_page_cost = 1.1;

-- Memory settings for different workloads
-- OLTP workload
ALTER SYSTEM SET shared_buffers = '2GB';
ALTER SYSTEM SET work_mem = '64MB';
ALTER SYSTEM SET maintenance_work_mem = '512MB';

-- Analytics workload
ALTER SYSTEM SET shared_buffers = '8GB';
ALTER SYSTEM SET work_mem = '512MB';
ALTER SYSTEM SET maintenance_work_mem = '2GB';

-- Cache warming strategies
CREATE OR REPLACE FUNCTION warm_cache()
RETURNS void AS $$
BEGIN
    -- Pre-load frequently accessed tables
    PERFORM COUNT(*) FROM customers;
    PERFORM COUNT(*) FROM products;
    PERFORM COUNT(*) FROM orders WHERE order_date >= CURRENT_DATE - INTERVAL '30 days';
    
    -- Pre-load common queries
    PERFORM customer_id, COUNT(*) 
    FROM orders 
    WHERE order_date >= CURRENT_DATE - INTERVAL '7 days'
    GROUP BY customer_id;
    
    RAISE NOTICE 'Cache warming completed';
END;
$$ LANGUAGE plpgsql;

-- Cache invalidation strategies
CREATE OR REPLACE FUNCTION invalidate_customer_cache()
RETURNS TRIGGER AS $$
BEGIN
    -- Invalidate application cache (pseudo-code)
    -- PERFORM redis_delete('customer:' || COALESCE(NEW.customer_id, OLD.customer_id));
    
    -- Invalidate query cache
    DELETE FROM query_cache 
    WHERE cache_key LIKE '%customer%' || COALESCE(NEW.customer_id, OLD.customer_id) || '%';
    
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER customer_cache_invalidation
    AFTER INSERT OR UPDATE OR DELETE ON customers
    FOR EACH ROW EXECUTE FUNCTION invalidate_customer_cache();
```

### 70. How do you implement database connection optimization?
**Answer:**
```sql
-- Connection pooling configuration
-- pgbouncer.ini example
/*
[databases]
production = host=localhost port=5432 dbname=production

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
max_db_connections = 100
reserve_pool_size = 5
reserve_pool_timeout = 3
server_reset_query = DISCARD ALL
server_check_query = SELECT 1
server_check_delay = 30
log_connections = 1
log_disconnections = 1
*/

-- Monitor connection usage
CREATE VIEW connection_stats AS
SELECT 
    datname,
    usename,
    application_name,
    state,
    COUNT(*) as connection_count,
    MAX(backend_start) as oldest_connection,
    AVG(EXTRACT(EPOCH FROM (now() - backend_start))) as avg_connection_age_seconds
FROM pg_stat_activity
WHERE pid <> pg_backend_pid()
GROUP BY datname, usename, application_name, state;

-- Connection health monitoring
CREATE OR REPLACE FUNCTION monitor_connection_health()
RETURNS TABLE(
    metric TEXT,
    current_value INT,
    threshold INT,
    status TEXT,
    recommendation TEXT
) AS $$
BEGIN
    -- Total connections
    RETURN QUERY
    SELECT 
        'Total Connections'::TEXT,
        (SELECT count(*)::INT FROM pg_stat_activity),
        100,
        CASE 
            WHEN (SELECT count(*) FROM pg_stat_activity) > 90 THEN 'CRITICAL'
            WHEN (SELECT count(*) FROM pg_stat_activity) > 80 THEN 'WARNING'
            ELSE 'OK'
        END,
        CASE 
            WHEN (SELECT count(*) FROM pg_stat_activity) > 80 THEN 'Implement connection pooling'
            ELSE 'Connection usage is healthy'
        END;
    
    -- Idle connections
    RETURN QUERY
    SELECT 
        'Idle Connections'::TEXT,
        (SELECT count(*)::INT FROM pg_stat_activity WHERE state = 'idle'),
        50,
        CASE 
            WHEN (SELECT count(*) FROM pg_stat_activity WHERE state = 'idle') > 40 THEN 'WARNING'
            ELSE 'OK'
        END,
        CASE 
            WHEN (SELECT count(*) FROM pg_stat_activity WHERE state = 'idle') > 40 THEN 'Review connection timeout settings'
            ELSE 'Idle connection count is acceptable'
        END;
    
    -- Long-running connections
    RETURN QUERY
    SELECT 
        'Long Running Connections'::TEXT,
        (SELECT count(*)::INT FROM pg_stat_activity 
         WHERE state = 'active' AND (now() - query_start) > INTERVAL '5 minutes'),
        5,
        CASE 
            WHEN (SELECT count(*) FROM pg_stat_activity 
                  WHERE state = 'active' AND (now() - query_start) > INTERVAL '5 minutes') > 3 THEN 'WARNING'
            ELSE 'OK'
        END,
        'Monitor for potential blocking queries';
END;
$$ LANGUAGE plpgsql;

-- Connection cleanup
CREATE OR REPLACE FUNCTION cleanup_idle_connections(max_idle_time INTERVAL DEFAULT '1 hour')
RETURNS INT AS $$
DECLARE
    terminated_count INT := 0;
    conn_record RECORD;
BEGIN
    FOR conn_record IN 
        SELECT pid, usename, application_name, backend_start
        FROM pg_stat_activity
        WHERE state = 'idle'
          AND (now() - backend_start) > max_idle_time
          AND pid <> pg_backend_pid()
    LOOP
        -- Terminate idle connection
        PERFORM pg_terminate_backend(conn_record.pid);
        terminated_count := terminated_count + 1;
        
        -- Log termination
        INSERT INTO connection_cleanup_log (pid, username, application_name, idle_duration, terminated_at)
        VALUES (conn_record.pid, conn_record.usename, conn_record.application_name, 
                now() - conn_record.backend_start, now());
    END LOOP;
    
    RETURN terminated_count;
END;
$$ LANGUAGE plpgsql;

-- Connection load balancing
CREATE TABLE connection_pools (
    pool_id SERIAL PRIMARY KEY,
    pool_name VARCHAR(50),
    host VARCHAR(100),
    port INT,
    database_name VARCHAR(50),
    max_connections INT,
    current_connections INT DEFAULT 0,
    pool_type VARCHAR(20), -- 'MASTER', 'REPLICA', 'ANALYTICS'
    weight INT DEFAULT 1,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    last_health_check TIMESTAMP
);

CREATE OR REPLACE FUNCTION get_optimal_connection_pool(query_type VARCHAR DEFAULT 'READ')
RETURNS TEXT AS $$
DECLARE
    selected_pool RECORD;
BEGIN
    -- Select pool based on query type and current load
    SELECT * INTO selected_pool
    FROM connection_pools
    WHERE status = 'ACTIVE'
      AND (
          (query_type = 'read' AND pool_type IN ('REPLICA', 'MASTER')) OR
          (query_type = 'write' AND pool_type = 'MASTER') OR
          (query_type = 'analytics' AND pool_type = 'ANALYTICS')
      )
      AND current_connections < max_connections
    ORDER BY 
        (current_connections::FLOAT / max_connections) ASC,  -- Least loaded first
        weight DESC  -- Higher weight preferred
    LIMIT 1;
    
    IF FOUND THEN
        -- Update connection count
        UPDATE connection_pools 
        SET current_connections = current_connections + 1
        WHERE pool_id = selected_pool.pool_id;
        
        RETURN selected_pool.host || ':' || selected_pool.port || '/' || selected_pool.database_name;
    ELSE
        RAISE EXCEPTION 'No available connection pool for query type: %', query_type;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Connection retry logic
CREATE OR REPLACE FUNCTION execute_with_retry(
    sql_query TEXT,
    max_retries INT DEFAULT 3,
    retry_delay INTERVAL DEFAULT '1 second'
)
RETURNS BOOLEAN AS $$
DECLARE
    attempt INT := 1;
    success BOOLEAN := FALSE;
BEGIN
    WHILE attempt <= max_retries AND NOT success LOOP
        BEGIN
            EXECUTE sql_query;
            success := TRUE;
        EXCEPTION 
            WHEN connection_exception THEN
                IF attempt = max_retries THEN
                    RAISE;
                END IF;
                
                RAISE NOTICE 'Connection failed, attempt % of %, retrying in %', 
                            attempt, max_retries, retry_delay;
                
                PERFORM pg_sleep(EXTRACT(EPOCH FROM retry_delay));
                attempt := attempt + 1;
        END;
    END LOOP;
    
    RETURN success;
END;
$$ LANGUAGE plpgsql;

-- Connection metrics collection
CREATE TABLE connection_metrics (
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_connections INT,
    active_connections INT,
    idle_connections INT,
    waiting_connections INT,
    max_connections_used INT,
    avg_connection_duration INTERVAL
);

CREATE OR REPLACE FUNCTION collect_connection_metrics()
RETURNS void AS $$
BEGIN
    INSERT INTO connection_metrics (
        total_connections,
        active_connections,
        idle_connections,
        waiting_connections,
        max_connections_used,
        avg_connection_duration
    )
    SELECT 
        COUNT(*),
        COUNT(*) FILTER (WHERE state = 'active'),
        COUNT(*) FILTER (WHERE state = 'idle'),
        COUNT(*) FILTER (WHERE wait_event IS NOT NULL),
        (SELECT setting::INT FROM pg_settings WHERE name = 'max_connections'),
        AVG(now() - backend_start)
    FROM pg_stat_activity
    WHERE pid <> pg_backend_pid();
END;
$$ LANGUAGE plpgsql;
```

### 71. What are query execution plan optimization techniques?
**Answer:**
```sql
-- Execution plan analysis
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) 
SELECT c.name, o.order_date, o.amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.created_date >= '2023-01-01'
  AND o.amount > 1000
ORDER BY o.order_date DESC
LIMIT 100;

-- Key execution plan elements to analyze:
-- 1. Node types and their costs
-- 2. Actual vs estimated rows
-- 3. Buffer usage (shared hit/read)
-- 4. Execution time breakdown

-- Plan optimization techniques

-- 1. Index optimization
-- Before: Sequential scan
SELECT * FROM orders WHERE customer_id = 123;

-- After: Index scan
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- 2. Join optimization
-- Force nested loop for small result sets
SELECT /*+ USE_NL(c o) */ c.name, o.amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.customer_id IN (1, 2, 3);

-- Force hash join for large datasets
SELECT /*+ USE_HASH(c o) */ c.name, COUNT(o.order_id)
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;

-- 3. Subquery optimization
-- Inefficient correlated subquery
SELECT c.name
FROM customers c
WHERE (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.customer_id) > 5;

-- Optimized with JOIN
SELECT DISTINCT c.name
FROM customers c
JOIN (
    SELECT customer_id
    FROM orders
    GROUP BY customer_id
    HAVING COUNT(*) > 5
) o ON c.customer_id = o.customer_id;

-- 4. Partition pruning
-- Query that uses partition pruning
SELECT * FROM orders_partitioned
WHERE order_date BETWEEN '2023-06-01' AND '2023-06-30';

-- 5. Statistics optimization
-- Update statistics for better estimates
ANALYZE customers;
ANALYZE orders;

-- Set statistics target for better histograms
ALTER TABLE orders ALTER COLUMN amount SET STATISTICS 1000;
ANALYZE orders;

-- 6. Query rewriting for optimization
-- Original query with multiple OR conditions
SELECT * FROM products
WHERE category = 'Electronics' 
   OR category = 'Computers'
   OR category = 'Software';

-- Optimized with IN clause
SELECT * FROM products
WHERE category IN ('Electronics', 'Computers', 'Software');

-- 7. CTE optimization
-- Materialized CTE for complex calculations
WITH RECURSIVE category_hierarchy AS (
    SELECT category_id, parent_id, name, 1 as level
    FROM categories
    WHERE parent_id IS NULL
    
    UNION ALL
    
    SELECT c.category_id, c.parent_id, c.name, ch.level + 1
    FROM categories c
    JOIN category_hierarchy ch ON c.parent_id = ch.category_id
)
SELECT * FROM category_hierarchy;

-- 8. Window function optimization
-- Efficient ranking query
SELECT 
    customer_id,
    order_date,
    amount,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) as rn
FROM orders
QUALIFY rn <= 3;  -- Get top 3 orders per customer

-- Plan comparison function
CREATE OR REPLACE FUNCTION compare_query_plans(
    query1 TEXT,
    query2 TEXT
)
RETURNS TABLE(
    query_version TEXT,
    total_cost NUMERIC,
    execution_time NUMERIC,
    buffer_hits BIGINT,
    buffer_reads BIGINT
) AS $$
DECLARE
    plan1 JSON;
    plan2 JSON;
BEGIN
    -- Get execution plans
    EXECUTE 'EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) ' || query1 INTO plan1;
    EXECUTE 'EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) ' || query2 INTO plan2;
    
    -- Extract metrics from plans
    RETURN QUERY
    SELECT 
        'Query 1'::TEXT,
        (plan1->0->'Plan'->>'Total Cost')::NUMERIC,
        (plan1->0->'Execution Time')::NUMERIC,
        (plan1->0->'Plan'->>'Shared Hit Blocks')::BIGINT,
        (plan1->0->'Plan'->>'Shared Read Blocks')::BIGINT
    UNION ALL
    SELECT 
        'Query 2'::TEXT,
        (plan2->0->'Plan'->>'Total Cost')::NUMERIC,
        (plan2->0->'Execution Time')::NUMERIC,
        (plan2->0->'Plan'->>'Shared Hit Blocks')::BIGINT,
        (plan2->0->'Plan'->>'Shared Read Blocks')::BIGINT;
END;
$$ LANGUAGE plpgsql;

-- Automatic plan analysis
CREATE OR REPLACE FUNCTION analyze_slow_queries()
RETURNS TABLE(
    queryid BIGINT,
    query_text TEXT,
    calls BIGINT,
    mean_time NUMERIC,
    optimization_suggestions TEXT[]
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        pss.queryid,
        LEFT(pss.query, 200),
        pss.calls,
        pss.mean_time,
        ARRAY[
            CASE 
                WHEN pss.shared_blks_hit::FLOAT / (pss.shared_blks_hit + pss.shared_blks_read) < 0.9 
                THEN 'Consider adding indexes to improve buffer hit ratio'
            END,
            CASE 
                WHEN pss.mean_time > 1000 
                THEN 'Query takes over 1 second on average - review execution plan'
            END,
            CASE 
                WHEN pss.calls > 10000 AND pss.mean_time > 100
                THEN 'High-frequency slow query - prime candidate for optimization'
            END
        ]::TEXT[]
    FROM pg_stat_statements pss
    WHERE pss.mean_time > 100
    ORDER BY pss.mean_time DESC;
END;
$$ LANGUAGE plpgsql;
```

### 72. How do you handle database locks and concurrency?
**Answer:**
```sql
-- Lock monitoring and analysis
SELECT 
    pl.locktype,
    pl.mode,
    pl.granted,
    pl.pid,
    pa.usename,
    pa.query_start,
    pa.query
FROM pg_locks pl
JOIN pg_stat_activity pa ON pl.pid = pa.pid
WHERE NOT pl.granted
ORDER BY pa.query_start;

-- Detect blocking queries
CREATE VIEW blocking_queries AS
SELECT 
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS blocking_statement,
    blocked_activity.application_name AS blocked_application
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON (
    blocking_locks.locktype = blocked_locks.locktype AND
    blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database AND
    blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation AND
    blocking_locks.pid != blocked_locks.pid
)
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;

-- Lock timeout configuration
SET lock_timeout = '30s';
SET deadlock_timeout = '1s';

-- Explicit locking strategies
-- 1. Advisory locks for application-level coordination
SELECT pg_advisory_lock(12345);  -- Exclusive lock
SELECT pg_advisory_lock_shared(12345);  -- Shared lock
SELECT pg_advisory_unlock(12345);

-- 2. Row-level locking
BEGIN;
SELECT * FROM accounts WHERE account_id = 123 FOR UPDATE;
UPDATE accounts SET balance = balance - 100 WHERE account_id = 123;
COMMIT;

-- 3. Table-level locking
BEGIN;
LOCK TABLE inventory IN EXCLUSIVE MODE;
-- Perform complex inventory operations
COMMIT;

-- Deadlock prevention strategies
-- 1. Consistent lock ordering
CREATE OR REPLACE FUNCTION transfer_funds(
    from_account INT,
    to_account INT,
    amount DECIMAL(10,2)
)
RETURNS BOOLEAN AS $$
DECLARE
    first_account INT;
    second_account INT;
BEGIN
    -- Always lock accounts in ascending order to prevent deadlocks
    IF from_account < to_account THEN
        first_account := from_account;
        second_account := to_account;
    ELSE
        first_account := to_account;
        second_account := from_account;
    END IF;
    
    -- Lock accounts in consistent order
    PERFORM * FROM accounts WHERE account_id = first_account FOR UPDATE;
    PERFORM * FROM accounts WHERE account_id = second_account FOR UPDATE;
    
    -- Perform transfer
    UPDATE accounts SET balance = balance - amount WHERE account_id = from_account;
    UPDATE accounts SET balance = balance + amount WHERE account_id = to_account;
    
    RETURN TRUE;
EXCEPTION
    WHEN deadlock_detected THEN
        RAISE NOTICE 'Deadlock detected, transaction rolled back';
        RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

-- Optimistic locking with version numbers
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10,2),
    version_number INT DEFAULT 1,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION update_product_optimistic(
    p_product_id INT,
    p_name VARCHAR(100),
    p_price DECIMAL(10,2),
    p_expected_version INT
)
RETURNS BOOLEAN AS $$
DECLARE
    rows_affected INT;
BEGIN
    UPDATE products 
    SET 
        name = p_name,
        price = p_price,
        version_number = version_number + 1,
        updated_at = CURRENT_TIMESTAMP
    WHERE product_id = p_product_id 
      AND version_number = p_expected_version;
    
    GET DIAGNOSTICS rows_affected = ROW_COUNT;
    
    IF rows_affected = 0 THEN
        RAISE EXCEPTION 'Optimistic lock failure: Product % was modified by another transaction', p_product_id;
    END IF;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

-- Lock monitoring and alerting
CREATE TABLE lock_monitoring_log (
    log_id SERIAL PRIMARY KEY,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    blocking_pid INT,
    blocked_pid INT,
    lock_type VARCHAR(50),
    lock_mode VARCHAR(50),
    blocking_query TEXT,
    blocked_query TEXT,
    duration INTERVAL
);

CREATE OR REPLACE FUNCTION monitor_locks()
RETURNS void AS $$
DECLARE
    lock_record RECORD;
BEGIN
    FOR lock_record IN SELECT * FROM blocking_queries LOOP
        INSERT INTO lock_monitoring_log (
            blocking_pid,
            blocked_pid,
            blocking_query,
            blocked_query,
            duration
        ) VALUES (
            lock_record.blocking_pid,
            lock_record.blocked_pid,
            lock_record.blocking_statement,
            lock_record.blocked_statement,
            now() - (SELECT query_start FROM pg_stat_activity WHERE pid = lock_record.blocked_pid)
        );
        
        -- Alert if lock duration exceeds threshold
        IF (now() - (SELECT query_start FROM pg_stat_activity WHERE pid = lock_record.blocked_pid)) > INTERVAL '5 minutes' THEN
            -- Send alert (implementation specific)
            RAISE WARNING 'Long-running lock detected: PID % blocking PID % for %', 
                         lock_record.blocking_pid, 
                         lock_record.blocked_pid,
                         now() - (SELECT query_start FROM pg_stat_activity WHERE pid = lock_record.blocked_pid);
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Concurrency control patterns
-- 1. Read-committed isolation level (default)
BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;
-- Allows non-repeatable reads but prevents dirty reads

-- 2. Repeatable read isolation level
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- Prevents non-repeatable reads and dirty reads

-- 3. Serializable isolation level
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- Prevents all phenomena but may cause serialization failures

-- Handle serialization failures
CREATE OR REPLACE FUNCTION execute_serializable_transaction(
    transaction_sql TEXT,
    max_retries INT DEFAULT 3
)
RETURNS BOOLEAN AS $$
DECLARE
    attempt INT := 1;
    success BOOLEAN := FALSE;
BEGIN
    WHILE attempt <= max_retries AND NOT success LOOP
        BEGIN
            EXECUTE 'BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE';
            EXECUTE transaction_sql;
            EXECUTE 'COMMIT';
            success := TRUE;
        EXCEPTION 
            WHEN serialization_failure THEN
                EXECUTE 'ROLLBACK';
                IF attempt = max_retries THEN
                    RAISE;
                END IF;
                
                -- Exponential backoff
                PERFORM pg_sleep(0.1 * (2 ^ attempt));
                attempt := attempt + 1;
        END;
    END LOOP;
    
    RETURN success;
END;
$$ LANGUAGE plpgsql;
```

### 17. Explain different types of subqueries
**Answer:**
Subqueries are nested queries that provide powerful data filtering and analysis capabilities. Understanding their types and performance implications is crucial for complex data engineering tasks.

**Types:**
- **Scalar Subquery**: Returns single value
- **Row Subquery**: Returns single row with multiple columns
- **Column Subquery**: Returns single column with multiple rows
- **Table Subquery**: Returns multiple rows and columns
- **Correlated vs Non-correlated**: Whether inner query depends on outer query

```sql
-- Scalar subquery
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- Column subquery with IN
SELECT name FROM employees
WHERE department_id IN (SELECT id FROM departments WHERE location = 'NYC');

-- Correlated subquery
SELECT name, salary
FROM employees e1
WHERE salary > (SELECT AVG(salary) FROM employees e2 WHERE e2.department_id = e1.department_id);

-- EXISTS subquery
SELECT c.name
FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);
```

### 18. What is the difference between UNION and UNION ALL?
**Answer:**
UNION operations combine result sets from multiple queries, essential for data consolidation in ETL processes.

**Key Differences:**
- **UNION**: Removes duplicate rows, slower due to sorting/deduplication
- **UNION ALL**: Keeps all rows including duplicates, faster performance
- **Column Requirements**: Same number of columns with compatible data types
- **Use Cases**: UNION for data deduplication, UNION ALL for performance when duplicates don't matter

```sql
-- UNION - removes duplicates
SELECT customer_id FROM orders_2023
UNION
SELECT customer_id FROM orders_2024;

-- UNION ALL - keeps duplicates, faster
SELECT customer_id FROM orders_2023
UNION ALL
SELECT customer_id FROM orders_2024;

-- Multiple table union
SELECT 'Q1' as quarter, SUM(amount) as total FROM q1_sales
UNION ALL
SELECT 'Q2', SUM(amount) FROM q2_sales
UNION ALL
SELECT 'Q3', SUM(amount) FROM q3_sales;
```

### 19. Explain the concept of database normalization
**Answer:**
Normalization is the process of organizing database structure to reduce redundancy and improve data integrity. Critical for designing efficient data warehouses and operational systems.

**Normal Forms:**
- **1NF**: Atomic values, no repeating groups
- **2NF**: 1NF + no partial dependencies on composite keys
- **3NF**: 2NF + no transitive dependencies
- **BCNF**: 3NF + every determinant is a candidate key

**Benefits**: Reduced storage, improved consistency, easier maintenance
**Trade-offs**: More complex queries, potential performance impact

```sql
-- Unnormalized table (violates 1NF)
CREATE TABLE bad_orders (
    order_id INT,
    customer_name VARCHAR(100),
    products VARCHAR(500)  -- Multiple products in one field
);

-- Normalized structure
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
    product_id INT,
    quantity INT,
    PRIMARY KEY (order_id, product_id)
);
```

### 20. What are CTEs (Common Table Expressions) and when would you use them?
**Answer:**
CTEs provide a way to create temporary named result sets that improve query readability and enable recursive operations. Essential for complex analytical queries in data engineering.

**Benefits:**
- **Readability**: Break complex queries into logical steps
- **Reusability**: Reference the same subquery multiple times
- **Recursion**: Enable hierarchical data processing
- **Maintainability**: Easier to debug and modify

```sql
-- Basic CTE
WITH high_value_customers AS (
    SELECT customer_id, SUM(order_amount) as total_spent
    FROM orders
    GROUP BY customer_id
    HAVING SUM(order_amount) > 10000
)
SELECT c.name, hvc.total_spent
FROM customers c
JOIN high_value_customers hvc ON c.customer_id = hvc.customer_id;

-- Multiple CTEs
WITH 
monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        SUM(amount) as monthly_total
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
),
avg_monthly AS (
    SELECT AVG(monthly_total) as avg_monthly_sales
    FROM monthly_sales
)
SELECT 
    ms.month,
    ms.monthly_total,
    ms.monthly_total - am.avg_monthly_sales as variance
FROM monthly_sales ms
CROSS JOIN avg_monthly am;

-- Recursive CTE for hierarchical data
WITH RECURSIVE employee_hierarchy AS (
    -- Base case
    SELECT employee_id, name, manager_id, 1 as level
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive case
    SELECT e.employee_id, e.name, e.manager_id, eh.level + 1
    FROM employees e
    JOIN employee_hierarchy eh ON e.manager_id = eh.employee_id
)
SELECT * FROM employee_hierarchy ORDER BY level, name;
```

### 21. What is the difference between clustered and non-clustered indexes?
**Answer:**
Understanding index types is crucial for database performance optimization in data engineering systems.

**Clustered Index:**
- **Physical Storage**: Data rows stored in order of index key
- **Limitation**: Only one per table (usually primary key)
- **Performance**: Faster for range queries and sorting
- **Storage**: Index and data stored together

**Non-clustered Index:**
- **Logical Structure**: Separate structure pointing to data rows
- **Multiple Allowed**: Can have many per table
- **Performance**: Faster for specific lookups
- **Storage**: Index stored separately from data

```sql
-- Clustered index (automatically created with PRIMARY KEY)
CREATE TABLE orders (
    order_id INT PRIMARY KEY,  -- Clustered index
    customer_id INT,
    order_date DATE
);

-- Non-clustered indexes
CREATE INDEX idx_customer ON orders(customer_id);
CREATE INDEX idx_date ON orders(order_date);
CREATE INDEX idx_customer_date ON orders(customer_id, order_date);

-- Check index usage
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM orders WHERE customer_id = 123;
```

### 22. Explain the CASE statement and its variations
**Answer:**
CASE statements provide conditional logic in SQL, essential for data transformation and business rule implementation in ETL processes.

**Types:**
- **Simple CASE**: Compares expression to specific values
- **Searched CASE**: Uses boolean conditions for more complex logic
- **Use Cases**: Data categorization, conditional aggregation, pivot operations

```sql
-- Simple CASE
SELECT 
    name,
    salary,
    CASE department
        WHEN 'IT' THEN 'Technology'
        WHEN 'HR' THEN 'Human Resources'
        WHEN 'FIN' THEN 'Finance'
        ELSE 'Other'
    END as department_full_name
FROM employees;

-- Searched CASE with conditions
SELECT 
    name,
    salary,
    CASE 
        WHEN salary >= 100000 THEN 'Senior'
        WHEN salary >= 70000 THEN 'Mid-level'
        WHEN salary >= 40000 THEN 'Junior'
        ELSE 'Entry-level'
    END as salary_band,
    CASE 
        WHEN EXTRACT(YEAR FROM hire_date) >= 2020 THEN 'New Hire'
        WHEN EXTRACT(YEAR FROM hire_date) >= 2015 THEN 'Experienced'
        ELSE 'Veteran'
    END as tenure_category
FROM employees;

-- CASE in aggregation (pivot-like operation)
SELECT 
    department,
    COUNT(*) as total_employees,
    SUM(CASE WHEN salary >= 80000 THEN 1 ELSE 0 END) as high_earners,
    SUM(CASE WHEN gender = 'F' THEN 1 ELSE 0 END) as female_count,
    AVG(CASE WHEN department = 'IT' THEN salary END) as avg_it_salary
FROM employees
GROUP BY department;
```

### 23. What are stored procedures and their advantages/disadvantages?
**Answer:**
Stored procedures are precompiled SQL code blocks stored in the database, important for data engineering workflows and business logic encapsulation.

**Advantages:**
- **Performance**: Precompiled and cached execution plans
- **Security**: Controlled data access, SQL injection prevention
- **Reusability**: Centralized business logic
- **Network Traffic**: Reduced data transfer

**Disadvantages:**
- **Portability**: Database-specific syntax
- **Version Control**: Harder to manage in source control
- **Debugging**: Limited debugging capabilities
- **Scalability**: Can become bottleneck

```sql
-- PostgreSQL stored procedure
CREATE OR REPLACE FUNCTION calculate_employee_bonus(
    emp_id INTEGER,
    bonus_percentage DECIMAL
) RETURNS DECIMAL AS $$
DECLARE
    current_salary DECIMAL;
    bonus_amount DECIMAL;
BEGIN
    -- Get current salary
    SELECT salary INTO current_salary
    FROM employees
    WHERE employee_id = emp_id;
    
    -- Calculate bonus
    bonus_amount := current_salary * (bonus_percentage / 100);
    
    -- Update employee record
    UPDATE employees
    SET bonus = bonus_amount
    WHERE employee_id = emp_id;
    
    RETURN bonus_amount;
END;
$$ LANGUAGE plpgsql;

-- Call the procedure
SELECT calculate_employee_bonus(123, 10.5);

-- SQL Server stored procedure with error handling
CREATE PROCEDURE ProcessMonthlyOrders
    @month INT,
    @year INT
AS
BEGIN
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Process orders
        UPDATE orders 
        SET status = 'PROCESSED'
        WHERE MONTH(order_date) = @month 
        AND YEAR(order_date) = @year
        AND status = 'PENDING';
        
        -- Log processing
        INSERT INTO processing_log (process_date, records_processed)
        VALUES (GETDATE(), @@ROWCOUNT);
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
```

### 24. Explain database triggers and their types
**Answer:**
Triggers are special stored procedures that automatically execute in response to database events, crucial for maintaining data integrity and audit trails in data systems.

**Types by Timing:**
- **BEFORE**: Execute before the triggering event
- **AFTER**: Execute after the triggering event
- **INSTEAD OF**: Replace the triggering event (views only)

**Types by Event:**
- **INSERT**: New row creation
- **UPDATE**: Row modification
- **DELETE**: Row removal

```sql
-- Audit trigger - tracks changes
CREATE TABLE employee_audit (
    audit_id SERIAL PRIMARY KEY,
    employee_id INT,
    old_salary DECIMAL,
    new_salary DECIMAL,
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_by VARCHAR(100)
);

CREATE OR REPLACE FUNCTION audit_salary_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE' AND OLD.salary != NEW.salary THEN
        INSERT INTO employee_audit (employee_id, old_salary, new_salary, changed_by)
        VALUES (NEW.employee_id, OLD.salary, NEW.salary, USER);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER salary_audit_trigger
    AFTER UPDATE ON employees
    FOR EACH ROW
    EXECUTE FUNCTION audit_salary_changes();

-- Validation trigger - enforce business rules
CREATE OR REPLACE FUNCTION validate_salary_increase()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE' AND NEW.salary > OLD.salary * 1.5 THEN
        RAISE EXCEPTION 'Salary increase cannot exceed 50%';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER salary_validation_trigger
    BEFORE UPDATE ON employees
    FOR EACH ROW
    EXECUTE FUNCTION validate_salary_increase();

-- Auto-update trigger - maintain derived data
CREATE OR REPLACE FUNCTION update_order_total()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE orders 
    SET total_amount = (
        SELECT SUM(quantity * unit_price)
        FROM order_items
        WHERE order_id = NEW.order_id
    )
    WHERE order_id = NEW.order_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER order_total_trigger
    AFTER INSERT OR UPDATE OR DELETE ON order_items
    FOR EACH ROW
    EXECUTE FUNCTION update_order_total();
```

### 25. What is the difference between correlated and non-correlated subqueries?
**Answer:**
Understanding subquery types is essential for writing efficient analytical queries and avoiding performance bottlenecks in data processing.

**Non-correlated Subquery:**
- **Independence**: Inner query executes once, independent of outer query
- **Performance**: Generally faster, can be cached
- **Use Cases**: Static filtering, lookup values

**Correlated Subquery:**
- **Dependency**: Inner query references outer query columns
- **Performance**: Executes once per outer row, potentially slower
- **Use Cases**: Row-by-row comparisons, complex filtering

```sql
-- Non-correlated subquery - executes once
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- Correlated subquery - executes for each row
SELECT name, salary, department
FROM employees e1
WHERE salary > (
    SELECT AVG(salary)
    FROM employees e2
    WHERE e2.department = e1.department
);

-- EXISTS with correlated subquery
SELECT c.customer_name
FROM customers c
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.customer_id
    AND o.order_date >= '2024-01-01'
);

-- Performance comparison - correlated vs window function
-- Slower correlated approach
SELECT 
    name,
    salary,
    (SELECT AVG(salary) FROM employees e2 WHERE e2.department = e1.department) as dept_avg
FROM employees e1;

-- Faster window function approach
SELECT 
    name,
    salary,
    AVG(salary) OVER (PARTITION BY department) as dept_avg
FROM employees;
```

### 26. Explain the concept of database views and their types
**Answer:**
Views are virtual tables that provide abstraction layers over complex queries, essential for data security, simplification, and maintaining consistent business logic across applications.

**Types:**
- **Simple Views**: Based on single table
- **Complex Views**: Multiple tables, aggregations, functions
- **Materialized Views**: Physically stored, refreshed periodically
- **Updatable Views**: Allow INSERT/UPDATE/DELETE operations

**Benefits:**
- **Security**: Hide sensitive columns/rows
- **Simplification**: Abstract complex joins
- **Consistency**: Centralized business logic
- **Performance**: Materialized views cache results

```sql
-- Simple view - hide sensitive data
CREATE VIEW employee_public AS
SELECT 
    employee_id,
    name,
    department,
    hire_date
FROM employees;

-- Complex view - business logic abstraction
CREATE VIEW sales_summary AS
SELECT 
    c.customer_name,
    c.region,
    COUNT(o.order_id) as total_orders,
    SUM(o.order_amount) as total_spent,
    AVG(o.order_amount) as avg_order_value,
    MAX(o.order_date) as last_order_date,
    CASE 
        WHEN SUM(o.order_amount) >= 10000 THEN 'VIP'
        WHEN SUM(o.order_amount) >= 5000 THEN 'Premium'
        ELSE 'Standard'
    END as customer_tier
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.region;

-- Materialized view (PostgreSQL)
CREATE MATERIALIZED VIEW monthly_sales_mv AS
SELECT 
    DATE_TRUNC('month', order_date) as month,
    COUNT(*) as order_count,
    SUM(order_amount) as total_revenue,
    AVG(order_amount) as avg_order_value
FROM orders
GROUP BY DATE_TRUNC('month', order_date);

-- Refresh materialized view
REFRESH MATERIALIZED VIEW monthly_sales_mv;

-- Updatable view with check option
CREATE VIEW high_salary_employees AS
SELECT employee_id, name, salary, department
FROM employees
WHERE salary >= 80000
WITH CHECK OPTION;

-- This will work
UPDATE high_salary_employees SET salary = 85000 WHERE employee_id = 123;

-- This will fail due to CHECK OPTION
UPDATE high_salary_employees SET salary = 70000 WHERE employee_id = 123;
```

### 27. What are database functions and their types?
**Answer:**
Database functions are reusable code blocks that return values, essential for data transformation, calculations, and maintaining consistent business logic across queries.

**Types:**
- **Scalar Functions**: Return single value
- **Table-Valued Functions**: Return table/result set
- **Aggregate Functions**: Operate on multiple rows
- **Window Functions**: Analytical functions with OVER clause

**Built-in vs User-Defined:**
- **Built-in**: Provided by database system
- **User-Defined**: Custom functions for specific business logic

```sql
-- Scalar function - returns single value
CREATE OR REPLACE FUNCTION calculate_age(birth_date DATE)
RETURNS INTEGER AS $$
BEGIN
    RETURN EXTRACT(YEAR FROM AGE(birth_date));
END;
$$ LANGUAGE plpgsql;

-- Usage
SELECT name, birth_date, calculate_age(birth_date) as age
FROM employees;

-- Table-valued function - returns result set
CREATE OR REPLACE FUNCTION get_employees_by_department(dept_name VARCHAR)
RETURNS TABLE(
    employee_id INT,
    name VARCHAR,
    salary DECIMAL,
    hire_date DATE
) AS $$
BEGIN
    RETURN QUERY
    SELECT e.employee_id, e.name, e.salary, e.hire_date
    FROM employees e
    JOIN departments d ON e.department_id = d.department_id
    WHERE d.department_name = dept_name;
END;
$$ LANGUAGE plpgsql;

-- Usage
SELECT * FROM get_employees_by_department('IT');

-- Aggregate function (custom)
CREATE OR REPLACE FUNCTION median_salary(department_id INT)
RETURNS DECIMAL AS $$
DECLARE
    result DECIMAL;
BEGIN
    SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary)
    INTO result
    FROM employees
    WHERE department_id = department_id;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- String manipulation functions
SELECT 
    name,
    UPPER(name) as name_upper,
    LENGTH(name) as name_length,
    SUBSTRING(name, 1, 3) as name_prefix,
    CONCAT(name, ' - ', department) as full_info,
    REPLACE(email, '@company.com', '@newcompany.com') as new_email
FROM employees;

-- Date functions
SELECT 
    order_date,
    EXTRACT(YEAR FROM order_date) as order_year,
    EXTRACT(MONTH FROM order_date) as order_month,
    DATE_TRUNC('month', order_date) as month_start,
    AGE(CURRENT_DATE, order_date) as order_age,
    order_date + INTERVAL '30 days' as due_date
FROM orders;
```

### 28. Explain transaction isolation levels
**Answer:**
Isolation levels control how transactions interact with each other, crucial for maintaining data consistency in concurrent data processing systems.

**Isolation Levels (from least to most restrictive):**
- **READ UNCOMMITTED**: Can read uncommitted changes (dirty reads)
- **READ COMMITTED**: Only reads committed data (default in most systems)
- **REPEATABLE READ**: Same data returned in multiple reads within transaction
- **SERIALIZABLE**: Highest isolation, transactions appear to run sequentially

**Concurrency Problems:**
- **Dirty Read**: Reading uncommitted changes
- **Non-repeatable Read**: Different results in same transaction
- **Phantom Read**: New rows appear between reads

```sql
-- Set isolation level
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- Example of isolation level effects
-- Session 1
BEGIN;
UPDATE accounts SET balance = balance - 1000 WHERE account_id = 1;
-- Don't commit yet

-- Session 2 with READ UNCOMMITTED (can see uncommitted changes)
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SELECT balance FROM accounts WHERE account_id = 1; -- Shows reduced balance

-- Session 2 with READ COMMITTED (waits for commit)
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SELECT balance FROM accounts WHERE account_id = 1; -- Waits or shows original balance

-- Demonstrating phantom reads
-- Session 1
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN;
SELECT COUNT(*) FROM orders WHERE customer_id = 123; -- Returns 5

-- Session 2
INSERT INTO orders (customer_id, order_date, amount) 
VALUES (123, CURRENT_DATE, 100);
COMMIT;

-- Session 1 (still in transaction)
SELECT COUNT(*) FROM orders WHERE customer_id = 123; -- Still returns 5 (REPEATABLE READ)

-- With SERIALIZABLE
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN;
SELECT SUM(balance) FROM accounts; -- Takes shared lock
-- Any concurrent transaction trying to modify accounts will wait
COMMIT;
```

### 29. What is the difference between HAVING and WHERE with GROUP BY?
**Answer:**
Understanding when to use WHERE vs HAVING is fundamental for correct data aggregation and filtering in analytical queries.

**Key Differences:**
- **WHERE**: Filters individual rows before grouping
- **HAVING**: Filters grouped results after aggregation
- **Performance**: WHERE is faster as it reduces data before grouping
- **Usage**: WHERE for row-level conditions, HAVING for group-level conditions

```sql
-- WHERE filters before grouping (more efficient)
SELECT 
    department,
    COUNT(*) as employee_count,
    AVG(salary) as avg_salary
FROM employees
WHERE hire_date >= '2020-01-01'  -- Filter rows first
GROUP BY department
HAVING COUNT(*) > 5;  -- Then filter groups

-- Incorrect usage - this won't work
SELECT department, COUNT(*)
FROM employees
GROUP BY department
WHERE COUNT(*) > 5;  -- ERROR: WHERE cannot use aggregate functions

-- Complex example showing both
SELECT 
    department,
    COUNT(*) as total_employees,
    COUNT(CASE WHEN salary >= 80000 THEN 1 END) as high_earners,
    AVG(salary) as avg_salary,
    MAX(salary) as max_salary
FROM employees
WHERE status = 'ACTIVE'  -- Filter active employees only
  AND hire_date >= '2015-01-01'  -- Filter by hire date
GROUP BY department
HAVING COUNT(*) >= 10  -- Department must have at least 10 employees
  AND AVG(salary) > 60000  -- Average salary must be above 60k
  AND COUNT(CASE WHEN salary >= 80000 THEN 1 END) > 2;  -- At least 3 high earners

-- Performance comparison
-- Efficient - WHERE reduces data first
SELECT region, COUNT(*)
FROM sales
WHERE sale_date >= '2024-01-01'
GROUP BY region
HAVING COUNT(*) > 100;

-- Less efficient - processes all data then filters
SELECT region, COUNT(*)
FROM sales
GROUP BY region
HAVING COUNT(*) > 100
  AND MIN(sale_date) >= '2024-01-01';
```

### 30. Explain the concept of database partitioning
**Answer:**
Partitioning divides large tables into smaller, manageable pieces while maintaining logical unity. Essential for handling big data and improving query performance in data warehouses.

**Types:**
- **Horizontal Partitioning**: Split rows (range, hash, list)
- **Vertical Partitioning**: Split columns
- **Functional Partitioning**: Split by feature/module

**Benefits:**
- **Performance**: Parallel processing, partition elimination
- **Maintenance**: Easier backup, archiving, indexing
- **Scalability**: Handle larger datasets

```sql
-- Range partitioning by date (PostgreSQL)
CREATE TABLE sales (
    sale_id SERIAL,
    sale_date DATE,
    customer_id INT,
    amount DECIMAL(10,2)
) PARTITION BY RANGE (sale_date);

-- Create partitions
CREATE TABLE sales_2023 PARTITION OF sales
    FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');

CREATE TABLE sales_2024 PARTITION OF sales
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

-- Hash partitioning
CREATE TABLE customers (
    customer_id SERIAL,
    name VARCHAR(100),
    email VARCHAR(100)
) PARTITION BY HASH (customer_id);

CREATE TABLE customers_p1 PARTITION OF customers
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);

CREATE TABLE customers_p2 PARTITION OF customers
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);

-- List partitioning
CREATE TABLE orders (
    order_id SERIAL,
    region VARCHAR(20),
    order_date DATE,
    amount DECIMAL(10,2)
) PARTITION BY LIST (region);

CREATE TABLE orders_north PARTITION OF orders
    FOR VALUES IN ('North', 'Northeast', 'Northwest');

CREATE TABLE orders_south PARTITION OF orders
    FOR VALUES IN ('South', 'Southeast', 'Southwest');

-- Query showing partition elimination
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM sales 
WHERE sale_date BETWEEN '2024-01-01' AND '2024-03-31';
-- Only scans sales_2024 partition

-- Partition maintenance
-- Add new partition
CREATE TABLE sales_2025 PARTITION OF sales
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

-- Drop old partition
DROP TABLE sales_2022;

-- Manual partitioning (for databases without native support)
CREATE TABLE sales_2024_q1 AS
SELECT * FROM sales 
WHERE sale_date >= '2024-01-01' AND sale_date < '2024-04-01';

CREATE INDEX idx_sales_2024_q1_date ON sales_2024_q1(sale_date);

-- Union view for querying
CREATE VIEW sales_current AS
SELECT * FROM sales_2024_q1
UNION ALL
SELECT * FROM sales_2024_q2
UNION ALL
SELECT * FROM sales_2024_q3
UNION ALL
SELECT * FROM sales_2024_q4;
```

### 31. What are the different types of database relationships?
**Answer:**
Database relationships define how tables connect to each other, fundamental for proper database design and data integrity in relational systems.

**Relationship Types:**
- **One-to-One (1:1)**: Each record in table A relates to exactly one record in table B
- **One-to-Many (1:M)**: One record in table A relates to multiple records in table B
- **Many-to-Many (M:M)**: Multiple records in both tables can relate to each other
- **Self-Referencing**: Table relates to itself (hierarchical data)

```sql
-- One-to-One: Employee to Employee_Details
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE employee_details (
    employee_id INT PRIMARY KEY REFERENCES employees(employee_id),
    ssn VARCHAR(11),
    emergency_contact VARCHAR(100),
    medical_info TEXT
);

-- One-to-Many: Customer to Orders
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date DATE,
    total_amount DECIMAL(10,2)
);

-- Many-to-Many: Students to Courses (with junction table)
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100),
    credits INT
);

CREATE TABLE student_courses (
    student_id INT REFERENCES students(student_id),
    course_id INT REFERENCES courses(course_id),
    enrollment_date DATE,
    grade CHAR(2),
    PRIMARY KEY (student_id, course_id)
);

-- Self-Referencing: Employee hierarchy
CREATE TABLE employees_hierarchy (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    manager_id INT REFERENCES employees_hierarchy(employee_id),
    department VARCHAR(50)
);

-- Queries demonstrating relationships
-- One-to-Many: Customer with their orders
SELECT 
    c.name,
    c.email,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.email;

-- Many-to-Many: Students with their courses
SELECT 
    s.name as student_name,
    c.course_name,
    sc.grade,
    sc.enrollment_date
FROM students s
JOIN student_courses sc ON s.student_id = sc.student_id
JOIN courses c ON sc.course_id = c.course_id
ORDER BY s.name, c.course_name;

-- Self-Referencing: Employee hierarchy
WITH RECURSIVE org_chart AS (
    -- Base case: top-level managers
    SELECT employee_id, name, manager_id, 1 as level, name as path
    FROM employees_hierarchy
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive case: employees with managers
    SELECT 
        e.employee_id, 
        e.name, 
        e.manager_id, 
        oc.level + 1,
        oc.path || ' -> ' || e.name
    FROM employees_hierarchy e
    JOIN org_chart oc ON e.manager_id = oc.employee_id
)
SELECT * FROM org_chart ORDER BY level, name;
```

### 32. Explain the concept of database cursors
**Answer:**
Cursors provide row-by-row processing of query results, useful for complex data transformations that can't be handled with set-based operations.

**Types:**
- **Forward-Only**: Can only move forward through results
- **Scrollable**: Can move in any direction
- **Static**: Snapshot of data at cursor creation
- **Dynamic**: Reflects real-time changes

**Use Cases:**
- Complex row-by-row processing
- Iterative calculations
- Data migration with transformation

```sql
-- PostgreSQL cursor example
CREATE OR REPLACE FUNCTION process_large_dataset()
RETURNS VOID AS $$
DECLARE
    emp_cursor CURSOR FOR 
        SELECT employee_id, name, salary, department_id
        FROM employees
        WHERE status = 'ACTIVE'
        ORDER BY employee_id;
    
    emp_record RECORD;
    bonus_amount DECIMAL;
    processed_count INT := 0;
BEGIN
    -- Open cursor
    OPEN emp_cursor;
    
    -- Loop through results
    LOOP
        -- Fetch next row
        FETCH emp_cursor INTO emp_record;
        
        -- Exit when no more rows
        EXIT WHEN NOT FOUND;
        
        -- Complex processing logic
        IF emp_record.department_id = 1 THEN
            bonus_amount := emp_record.salary * 0.15;
        ELSIF emp_record.department_id = 2 THEN
            bonus_amount := emp_record.salary * 0.12;
        ELSE
            bonus_amount := emp_record.salary * 0.10;
        END IF;
        
        -- Update employee record
        UPDATE employees
        SET bonus = bonus_amount,
            last_processed = CURRENT_TIMESTAMP
        WHERE employee_id = emp_record.employee_id;
        
        processed_count := processed_count + 1;
        
        -- Commit every 1000 records
        IF processed_count % 1000 = 0 THEN
            COMMIT;
            RAISE NOTICE 'Processed % employees', processed_count;
        END IF;
    END LOOP;
    
    -- Close cursor
    CLOSE emp_cursor;
    
    RAISE NOTICE 'Total processed: % employees', processed_count;
END;
$$ LANGUAGE plpgsql;

-- SQL Server cursor example
DECLARE @employee_id INT, @salary DECIMAL(10,2), @bonus DECIMAL(10,2);

DECLARE salary_cursor CURSOR FOR
    SELECT employee_id, salary
    FROM employees
    WHERE department = 'Sales';

OPEN salary_cursor;

FETCH NEXT FROM salary_cursor INTO @employee_id, @salary;

WHILE @@FETCH_STATUS = 0
BEGIN
    -- Calculate bonus based on salary
    SET @bonus = @salary * 0.10;
    
    -- Update employee
    UPDATE employees
    SET bonus = @bonus
    WHERE employee_id = @employee_id;
    
    -- Fetch next row
    FETCH NEXT FROM salary_cursor INTO @employee_id, @salary;
END;

CLOSE salary_cursor;
DEALLOCATE salary_cursor;

-- Alternative: Set-based approach (usually preferred)
UPDATE employees
SET bonus = salary * 
    CASE 
        WHEN department_id = 1 THEN 0.15
        WHEN department_id = 2 THEN 0.12
        ELSE 0.10
    END,
    last_processed = CURRENT_TIMESTAMP
WHERE status = 'ACTIVE';
```

### 33. What is the difference between OLTP and OLAP systems?
**Answer:**
Understanding OLTP vs OLAP is crucial for designing appropriate database architectures for different business needs in data engineering.

**OLTP (Online Transaction Processing):**
- **Purpose**: Handle day-to-day business operations
- **Characteristics**: High concurrency, fast response, normalized data
- **Operations**: INSERT, UPDATE, DELETE focused
- **Examples**: Order processing, inventory management, CRM

**OLAP (Online Analytical Processing):**
- **Purpose**: Support business intelligence and analytics
- **Characteristics**: Complex queries, historical data, denormalized
- **Operations**: SELECT focused with aggregations
- **Examples**: Data warehouses, reporting systems, BI tools

```sql
-- OLTP Example: Order processing system
-- Normalized structure for fast transactions
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20),
    total_amount DECIMAL(10,2)
);

CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2)
);

-- OLTP queries - simple, fast
INSERT INTO orders (customer_id, status, total_amount)
VALUES (123, 'PENDING', 299.99);

UPDATE orders SET status = 'SHIPPED' WHERE order_id = 456;

SELECT * FROM orders WHERE customer_id = 123 AND status = 'PENDING';

-- OLAP Example: Sales data warehouse
-- Denormalized structure for fast analytics
CREATE TABLE sales_fact (
    sale_id BIGINT PRIMARY KEY,
    date_key INT,
    customer_key INT,
    product_key INT,
    store_key INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    cost_amount DECIMAL(10,2),
    profit_amount DECIMAL(10,2)
);

CREATE TABLE date_dimension (
    date_key INT PRIMARY KEY,
    full_date DATE,
    year INT,
    quarter INT,
    month INT,
    month_name VARCHAR(20),
    day_of_week INT,
    day_name VARCHAR(20),
    is_weekend BOOLEAN,
    is_holiday BOOLEAN
);

-- OLAP queries - complex analytics
SELECT 
    d.year,
    d.quarter,
    SUM(sf.total_amount) as total_revenue,
    SUM(sf.profit_amount) as total_profit,
    COUNT(DISTINCT sf.customer_key) as unique_customers,
    AVG(sf.total_amount) as avg_order_value
FROM sales_fact sf
JOIN date_dimension d ON sf.date_key = d.date_key
WHERE d.year IN (2023, 2024)
GROUP BY d.year, d.quarter
ORDER BY d.year, d.quarter;

-- Complex OLAP query with window functions
SELECT 
    d.month_name,
    d.year,
    SUM(sf.total_amount) as monthly_revenue,
    LAG(SUM(sf.total_amount)) OVER (ORDER BY d.year, d.month) as prev_month_revenue,
    (SUM(sf.total_amount) - LAG(SUM(sf.total_amount)) OVER (ORDER BY d.year, d.month)) / 
    LAG(SUM(sf.total_amount)) OVER (ORDER BY d.year, d.month) * 100 as growth_rate
FROM sales_fact sf
JOIN date_dimension d ON sf.date_key = d.date_key
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;
```

### 34. Explain the concept of database sharding
**Answer:**
Sharding is a horizontal partitioning strategy that distributes data across multiple database instances, essential for scaling large applications beyond single-server limitations.

**Sharding Strategies:**
- **Range-based**: Partition by value ranges
- **Hash-based**: Use hash function to distribute data
- **Directory-based**: Lookup service maps keys to shards
- **Geographic**: Partition by location

**Benefits & Challenges:**
- **Benefits**: Horizontal scalability, improved performance, fault isolation
- **Challenges**: Complex queries, rebalancing, consistency issues

```sql
-- Example: E-commerce platform sharding by customer_id

-- Shard 1: Customers 1-1000000
CREATE DATABASE ecommerce_shard1;
USE ecommerce_shard1;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY CHECK (customer_id BETWEEN 1 AND 1000000),
    name VARCHAR(100),
    email VARCHAR(100),
    region VARCHAR(50)
);

CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date DATE,
    total_amount DECIMAL(10,2)
);

-- Shard 2: Customers 1000001-2000000
CREATE DATABASE ecommerce_shard2;
USE ecommerce_shard2;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY CHECK (customer_id BETWEEN 1000001 AND 2000000),
    name VARCHAR(100),
    email VARCHAR(100),
    region VARCHAR(50)
);

CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date DATE,
    total_amount DECIMAL(10,2)
);

-- Application-level sharding logic (pseudocode)
/*
function getShardForCustomer(customer_id) {
    if (customer_id <= 1000000) return 'shard1';
    else if (customer_id <= 2000000) return 'shard2';
    else if (customer_id <= 3000000) return 'shard3';
    // ... more shards
}

function getCustomerOrders(customer_id) {
    shard = getShardForCustomer(customer_id);
    connection = getConnectionToShard(shard);
    return connection.query("SELECT * FROM orders WHERE customer_id = ?", customer_id);
}
*/

-- Hash-based sharding example
-- Shard determination: customer_id % 4
-- Shard 0: customer_id % 4 = 0
-- Shard 1: customer_id % 4 = 1
-- Shard 2: customer_id % 4 = 2
-- Shard 3: customer_id % 4 = 3

-- Cross-shard query challenges
-- This query would need to run on all shards and aggregate results
/*
SELECT 
    DATE_TRUNC('month', order_date) as month,
    COUNT(*) as total_orders,
    SUM(total_amount) as total_revenue
FROM orders
WHERE order_date >= '2024-01-01'
GROUP BY DATE_TRUNC('month', order_date);
*/

-- Shard rebalancing example
-- Moving data from overloaded shard to new shard
/*
-- Step 1: Create new shard
CREATE DATABASE ecommerce_shard5;

-- Step 2: Move subset of data
INSERT INTO ecommerce_shard5.customers
SELECT * FROM ecommerce_shard1.customers
WHERE customer_id BETWEEN 500001 AND 750000;

INSERT INTO ecommerce_shard5.orders
SELECT * FROM ecommerce_shard1.orders
WHERE customer_id BETWEEN 500001 AND 750000;

-- Step 3: Update application routing logic
-- Step 4: Remove moved data from original shard
DELETE FROM ecommerce_shard1.orders
WHERE customer_id BETWEEN 500001 AND 750000;

DELETE FROM ecommerce_shard1.customers
WHERE customer_id BETWEEN 500001 AND 750000;
*/

-- Federated query example (if supported)
CREATE SERVER shard1_server
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host 'shard1.example.com', port '5432', dbname 'ecommerce_shard1');

CREATE SERVER shard2_server
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host 'shard2.example.com', port '5432', dbname 'ecommerce_shard2');

-- Create foreign tables
CREATE FOREIGN TABLE shard1_orders (
    order_id BIGINT,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2)
) SERVER shard1_server OPTIONS (table_name 'orders');

CREATE FOREIGN TABLE shard2_orders (
    order_id BIGINT,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2)
) SERVER shard2_server OPTIONS (table_name 'orders');

-- Cross-shard query
SELECT 
    'Shard1' as shard,
    COUNT(*) as order_count,
    SUM(total_amount) as total_revenue
FROM shard1_orders
WHERE order_date >= '2024-01-01'
UNION ALL
SELECT 
    'Shard2' as shard,
    COUNT(*) as order_count,
    SUM(total_amount) as total_revenue
FROM shard2_orders
WHERE order_date >= '2024-01-01';
```

### 35. What are the different types of database locks?
**Answer:**
Database locks control concurrent access to data, preventing conflicts and maintaining consistency in multi-user environments. Understanding lock types is crucial for performance tuning and deadlock prevention.

**Lock Granularity:**
- **Row-level**: Locks individual rows
- **Page-level**: Locks database pages
- **Table-level**: Locks entire tables
- **Database-level**: Locks entire database

**Lock Types:**
- **Shared (S)**: Multiple readers allowed
- **Exclusive (X)**: Single writer, no readers
- **Intent**: Indicates intention to acquire finer-grained locks
- **Update (U)**: Prevents deadlocks during read-then-write operations

```sql
-- Explicit locking examples

-- Shared lock - multiple readers allowed
BEGIN;
SELECT * FROM accounts WHERE account_id = 123 FOR SHARE;
-- Other sessions can read but not modify
COMMIT;

-- Exclusive lock - single writer
BEGIN;
SELECT * FROM accounts WHERE account_id = 123 FOR UPDATE;
UPDATE accounts SET balance = balance - 100 WHERE account_id = 123;
COMMIT;

-- Lock timeout handling
SET lock_timeout = '5s';
BEGIN;
SELECT * FROM accounts WHERE account_id = 123 FOR UPDATE NOWAIT;
-- Fails immediately if lock not available
COMMIT;

-- Deadlock example and prevention
-- Session 1
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
-- Now tries to update account 2
UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;
COMMIT;

-- Session 2 (running concurrently)
BEGIN;
UPDATE accounts SET balance = balance - 50 WHERE account_id = 2;
-- Now tries to update account 1 - DEADLOCK!
UPDATE accounts SET balance = balance + 50 WHERE account_id = 1;
COMMIT;

-- Deadlock prevention - consistent ordering
-- Both sessions should acquire locks in same order
BEGIN;
UPDATE accounts SET balance = balance - 100 
WHERE account_id = LEAST(1, 2);  -- Always lock lower ID first
UPDATE accounts SET balance = balance + 100 
WHERE account_id = GREATEST(1, 2);  -- Then higher ID
COMMIT;

-- Lock monitoring queries
-- PostgreSQL
SELECT 
    l.locktype,
    l.database,
    l.relation::regclass,
    l.page,
    l.tuple,
    l.virtualxid,
    l.transactionid,
    l.mode,
    l.granted,
    a.query
FROM pg_locks l
LEFT JOIN pg_stat_activity a ON l.pid = a.pid
WHERE NOT l.granted;

-- SQL Server
SELECT 
    request_session_id,
    resource_type,
    resource_database_id,
    resource_description,
    request_mode,
    request_status
FROM sys.dm_tran_locks
WHERE request_status = 'WAIT';

-- Lock escalation example
-- SQL Server - prevent lock escalation
ALTER TABLE large_table SET (LOCK_ESCALATION = DISABLE);

-- Bulk operations with reduced locking
-- Use appropriate isolation levels
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SELECT COUNT(*) FROM large_table;  -- Dirty read, minimal locking

-- Advisory locks for application-level coordination
-- PostgreSQL advisory locks
SELECT pg_advisory_lock(12345);  -- Application-specific lock
-- Perform critical section work
SELECT pg_advisory_unlock(12345);

-- Try lock without waiting
SELECT pg_try_advisory_lock(12345);  -- Returns true if acquired

-- Session-level advisory lock (auto-released on disconnect)
SELECT pg_advisory_lock(12345);
```