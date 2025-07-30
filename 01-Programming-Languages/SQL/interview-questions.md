# SQL Interview Questions for Data Engineering

## Basic Questions

### Q1: What's the difference between INNER JOIN and LEFT JOIN?

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

### Q2: Explain the difference between WHERE and HAVING clauses.

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

### Q3: What are window functions and how do they differ from aggregate functions?

**Answer:**
Window functions perform calculations across related rows without collapsing the result set, unlike aggregate functions.

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

## Intermediate Questions

### Q4: How would you find the second highest salary in each department?

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

### Q5: Write a query to calculate running totals.

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

### Q6: How do you handle duplicate records in a table?

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

## Advanced Questions

### Q7: Write a query to find gaps in sequential data.

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

### Q8: Implement a pivot table in SQL.

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

### Q9: Write a recursive CTE to handle hierarchical data.

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

### Q10: Design a query for slowly changing dimensions (SCD Type 2).

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

-- Insert new versions for changed records
INSERT INTO customer_dim (
    customer_id, name, address, phone,
    effective_date, end_date, is_current, version
)
SELECT 
    s.customer_id,
    s.name,
    s.address,
    s.phone,
    CURRENT_DATE,
    '9999-12-31',
    'Y',
    COALESCE(MAX(d.version), 0) + 1
FROM customer_staging s
INNER JOIN customer_dim d ON s.customer_id = d.customer_id
WHERE d.is_current = 'N' 
  AND d.end_date = CURRENT_DATE - 1
GROUP BY s.customer_id, s.name, s.address, s.phone;
```

## Performance Optimization Questions

### Q11: How would you optimize a slow-running query?

**Answer:**
1. **Analyze execution plan**
2. **Add appropriate indexes**
3. **Rewrite query logic**
4. **Partition large tables**

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

### Q12: Explain different types of indexes and when to use them.

**Answer:**
```sql
-- 1. Clustered Index (Primary Key)
CREATE TABLE orders (
    order_id INT PRIMARY KEY,  -- Clustered index
    customer_id INT,
    order_date DATE
);

-- 2. Non-clustered Index
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);

-- 3. Composite Index
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- 4. Covering Index
CREATE INDEX idx_orders_covering 
ON orders(customer_id, order_date) 
INCLUDE (order_amount, status);

-- 5. Partial Index
CREATE INDEX idx_active_orders 
ON orders(order_date) 
WHERE status = 'ACTIVE';

-- 6. Unique Index
CREATE UNIQUE INDEX idx_customers_email ON customers(email);
```