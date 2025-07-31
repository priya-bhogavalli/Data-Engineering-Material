# SQL Interview Questions for Data Engineering

## Basic Level Questions (1-7)

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

## Intermediate Level Questions (8-15)

### 8. What are window functions and how do they differ from aggregate functions?
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

### 9. How would you find the second highest salary in each department?
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

### 10. Write a query to calculate running totals
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

### 11. How do you handle duplicate records in a table?
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

### 12. Explain Common Table Expressions (CTEs) with examples
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

### 13. What's the difference between UNION and UNION ALL?
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

### 14. How do you optimize a slow-running query?
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

### 15. Explain different types of subqueries
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

## Advanced Level Questions (16-21)

### 16. Write a query to find gaps in sequential data
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

### 17. Implement a pivot table in SQL
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

### 18. Write a recursive CTE to handle hierarchical data
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

### 19. Design a query for slowly changing dimensions (SCD Type 2)
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

### 20. How would you implement data quality checks in SQL?
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

### 21. Write a query to calculate customer lifetime value (CLV)
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

## Data Engineering Specific Questions

### 22. How would you design a data pipeline using SQL?
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

### 23. How do you handle large datasets efficiently?
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

### 24. Explain database normalization with examples
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