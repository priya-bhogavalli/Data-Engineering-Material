# SQL for Data Engineering - Core Concepts

## Overview
SQL (Structured Query Language) is the standard language for managing and manipulating relational databases, essential for data engineers working with structured data.

## Key Concepts

### 1. Data Definition Language (DDL)
- **CREATE**: Create database objects (tables, indexes, views)
- **ALTER**: Modify existing database objects
- **DROP**: Delete database objects
- **TRUNCATE**: Remove all data from tables

### 2. Data Manipulation Language (DML)
- **SELECT**: Query data from tables
- **INSERT**: Add new records
- **UPDATE**: Modify existing records
- **DELETE**: Remove records

### 3. Data Control Language (DCL)
- **GRANT**: Give permissions to users
- **REVOKE**: Remove permissions from users

### 4. Transaction Control Language (TCL)
- **COMMIT**: Save changes permanently
- **ROLLBACK**: Undo changes
- **SAVEPOINT**: Create checkpoint in transaction

## Advanced SQL Concepts

### 1. Window Functions
```sql
-- Row number, rank, dense rank
SELECT 
    employee_id,
    salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) as row_num,
    RANK() OVER (ORDER BY salary DESC) as rank,
    DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank
FROM employees;

-- Moving averages
SELECT 
    date,
    sales,
    AVG(sales) OVER (
        ORDER BY date 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) as moving_avg_3day
FROM daily_sales;
```

### 2. Common Table Expressions (CTEs)
```sql
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
SELECT * FROM employee_hierarchy;
```

### 3. Pivot and Unpivot Operations
```sql
-- Pivot example (SQL Server/Oracle syntax)
SELECT *
FROM (
    SELECT year, quarter, sales
    FROM quarterly_sales
) src
PIVOT (
    SUM(sales)
    FOR quarter IN ([Q1], [Q2], [Q3], [Q4])
) pvt;
```

### 4. Advanced Joins
```sql
-- Self join for finding duplicates
SELECT a.id, a.email
FROM users a
JOIN users b ON a.email = b.email AND a.id != b.id;

-- Cross join for cartesian product
SELECT p.product_name, s.store_name
FROM products p
CROSS JOIN stores s;
```

## Data Engineering Specific SQL

### 1. Data Quality Checks
```sql
-- Check for duplicates
SELECT email, COUNT(*) as duplicate_count
FROM users
GROUP BY email
HAVING COUNT(*) > 1;

-- Check for null values
SELECT 
    COUNT(*) as total_rows,
    COUNT(email) as non_null_emails,
    COUNT(*) - COUNT(email) as null_emails,
    (COUNT(*) - COUNT(email)) * 100.0 / COUNT(*) as null_percentage
FROM users;
```

### 2. Data Profiling
```sql
-- Statistical summary
SELECT 
    COUNT(*) as row_count,
    COUNT(DISTINCT customer_id) as unique_customers,
    MIN(order_date) as earliest_order,
    MAX(order_date) as latest_order,
    AVG(order_amount) as avg_order_amount,
    STDDEV(order_amount) as stddev_order_amount
FROM orders;
```

### 3. Incremental Data Loading
```sql
-- Upsert pattern (MERGE statement)
MERGE target_table AS target
USING source_table AS source
ON target.id = source.id
WHEN MATCHED THEN
    UPDATE SET 
        target.name = source.name,
        target.updated_at = CURRENT_TIMESTAMP
WHEN NOT MATCHED THEN
    INSERT (id, name, created_at)
    VALUES (source.id, source.name, CURRENT_TIMESTAMP);
```

### 4. Slowly Changing Dimensions (SCD)
```sql
-- SCD Type 2 implementation
INSERT INTO dim_customer (
    customer_id,
    name,
    address,
    effective_date,
    expiry_date,
    is_current
)
SELECT 
    s.customer_id,
    s.name,
    s.address,
    CURRENT_DATE as effective_date,
    '9999-12-31' as expiry_date,
    'Y' as is_current
FROM staging_customer s
LEFT JOIN dim_customer d ON s.customer_id = d.customer_id AND d.is_current = 'Y'
WHERE d.customer_id IS NULL OR s.address != d.address;
```

## Performance Optimization

### 1. Indexing Strategies
```sql
-- Composite index for common query patterns
CREATE INDEX idx_orders_customer_date 
ON orders (customer_id, order_date);

-- Covering index
CREATE INDEX idx_orders_covering 
ON orders (customer_id, order_date) 
INCLUDE (order_amount, status);
```

### 2. Query Optimization
```sql
-- Use EXISTS instead of IN for better performance
SELECT customer_id, name
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id
);

-- Avoid functions in WHERE clause
-- Bad
SELECT * FROM orders WHERE YEAR(order_date) = 2023;
-- Good
SELECT * FROM orders WHERE order_date >= '2023-01-01' AND order_date < '2024-01-01';
```

### 3. Partitioning
```sql
-- Range partitioning by date
CREATE TABLE sales_partitioned (
    sale_id INT,
    sale_date DATE,
    amount DECIMAL(10,2)
)
PARTITION BY RANGE (YEAR(sale_date)) (
    PARTITION p2021 VALUES LESS THAN (2022),
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024)
);
```

## Database-Specific Features

### 1. PostgreSQL
- **JSONB**: Binary JSON data type
- **Arrays**: Native array support
- **Full-text search**: Built-in text search capabilities

### 2. SQL Server
- **SSIS Integration**: ETL capabilities
- **Columnstore indexes**: For analytical workloads
- **Temporal tables**: Built-in change tracking

### 3. Oracle
- **PL/SQL**: Procedural language
- **Materialized views**: Pre-computed query results
- **Flashback**: Point-in-time recovery

### 4. MySQL
- **Storage engines**: InnoDB, MyISAM
- **Replication**: Master-slave setup
- **Partitioning**: Horizontal partitioning support

## Best Practices

### 1. Code Organization
- Use consistent naming conventions
- Comment complex queries
- Format SQL for readability
- Use version control for SQL scripts

### 2. Performance
- Analyze execution plans
- Use appropriate indexes
- Avoid SELECT *
- Limit result sets when possible

### 3. Security
- Use parameterized queries
- Implement least privilege access
- Encrypt sensitive data
- Regular security audits

### 4. Data Integrity
- Use constraints (PRIMARY KEY, FOREIGN KEY, CHECK)
- Implement proper transaction handling
- Validate data before insertion
- Regular data quality checks