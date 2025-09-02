# SQL for Data Engineering - Key Concepts

## 🎯 What is SQL in Data Engineering?
SQL (Structured Query Language) is essential for data extraction, transformation, and analysis in relational databases and data warehouses.

## 🔑 Core Concepts

### 1. Data Retrieval (SELECT)
```sql
-- Basic SELECT
SELECT column1, column2 FROM table_name;

-- Filtering
SELECT * FROM sales WHERE amount > 1000 AND date >= '2023-01-01';

-- Sorting
SELECT * FROM customers ORDER BY created_date DESC, name ASC;

-- Limiting results
SELECT * FROM products LIMIT 10;
```

### 2. Aggregations and Grouping
```sql
-- Basic aggregations
SELECT 
    COUNT(*) as total_orders,
    SUM(amount) as total_revenue,
    AVG(amount) as avg_order_value,
    MAX(amount) as largest_order,
    MIN(amount) as smallest_order
FROM orders;

-- GROUP BY
SELECT 
    category,
    COUNT(*) as product_count,
    AVG(price) as avg_price
FROM products
GROUP BY category
HAVING COUNT(*) > 5;
```

### 3. Joins
```sql
-- INNER JOIN
SELECT c.name, o.amount, o.order_date
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;

-- LEFT JOIN
SELECT c.name, COALESCE(o.amount, 0) as amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;

-- Multiple joins
SELECT c.name, o.amount, p.product_name
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN products p ON o.product_id = p.product_id;
```

### 4. Window Functions
```sql
-- Ranking
SELECT 
    name,
    salary,
    RANK() OVER (ORDER BY salary DESC) as salary_rank,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank
FROM employees;

-- Running totals
SELECT 
    date,
    amount,
    SUM(amount) OVER (ORDER BY date) as running_total
FROM daily_sales;

-- Moving averages
SELECT 
    date,
    amount,
    AVG(amount) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7day
FROM daily_sales;
```

### 5. Common Table Expressions (CTEs)
```sql
-- Basic CTE
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        SUM(amount) as total_sales
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT * FROM monthly_sales WHERE total_sales > 10000;

-- Recursive CTE (for hierarchical data)
WITH RECURSIVE employee_hierarchy AS (
    SELECT employee_id, name, manager_id, 1 as level
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    SELECT e.employee_id, e.name, e.manager_id, eh.level + 1
    FROM employees e
    JOIN employee_hierarchy eh ON e.manager_id = eh.employee_id
)
SELECT * FROM employee_hierarchy;
```

### 6. Data Modification
```sql
-- INSERT
INSERT INTO customers (name, email, created_date)
VALUES ('John Doe', 'john@example.com', CURRENT_DATE);

-- UPDATE
UPDATE products 
SET price = price * 1.1 
WHERE category = 'electronics';

-- DELETE
DELETE FROM orders 
WHERE order_date < '2022-01-01';

-- UPSERT (PostgreSQL)
INSERT INTO products (id, name, price)
VALUES (1, 'Widget', 10.00)
ON CONFLICT (id) 
DO UPDATE SET price = EXCLUDED.price;
```

## 🔄 Advanced Patterns

### 1. Data Quality Checks
```sql
-- Find duplicates
SELECT email, COUNT(*) 
FROM customers 
GROUP BY email 
HAVING COUNT(*) > 1;

-- Check for nulls
SELECT 
    COUNT(*) as total_rows,
    COUNT(email) as non_null_emails,
    COUNT(*) - COUNT(email) as null_emails
FROM customers;

-- Data validation
SELECT *
FROM orders
WHERE amount <= 0 OR customer_id IS NULL;
```

### 2. Date/Time Operations
```sql
-- Date arithmetic
SELECT 
    order_date,
    order_date + INTERVAL '30 days' as due_date,
    EXTRACT(YEAR FROM order_date) as order_year,
    DATE_TRUNC('month', order_date) as order_month
FROM orders;

-- Time-based aggregations
SELECT 
    DATE_TRUNC('week', order_date) as week,
    COUNT(*) as orders_per_week
FROM orders
GROUP BY DATE_TRUNC('week', order_date)
ORDER BY week;
```

### 3. String Operations
```sql
-- String manipulation
SELECT 
    UPPER(name) as name_upper,
    LENGTH(name) as name_length,
    SUBSTRING(email FROM POSITION('@' IN email) + 1) as domain,
    CONCAT(first_name, ' ', last_name) as full_name
FROM customers;

-- Pattern matching
SELECT * FROM products 
WHERE name ILIKE '%widget%' OR description ~ 'electronic.*device';
```

### 4. Conditional Logic
```sql
-- CASE statements
SELECT 
    name,
    amount,
    CASE 
        WHEN amount < 100 THEN 'Small'
        WHEN amount < 1000 THEN 'Medium'
        ELSE 'Large'
    END as order_size
FROM orders;

-- COALESCE for null handling
SELECT 
    name,
    COALESCE(phone, email, 'No contact') as contact_method
FROM customers;
```

## 🏗️ Data Engineering Patterns

### 1. ETL Transformations
```sql
-- Slowly Changing Dimension (Type 2)
INSERT INTO dim_customer_history
SELECT 
    customer_id,
    name,
    email,
    address,
    CURRENT_DATE as effective_date,
    '9999-12-31'::date as end_date,
    TRUE as is_current
FROM staging_customers
WHERE NOT EXISTS (
    SELECT 1 FROM dim_customer_history d
    WHERE d.customer_id = staging_customers.customer_id
    AND d.is_current = TRUE
);
```

### 2. Data Deduplication
```sql
-- Remove duplicates keeping latest record
DELETE FROM customers 
WHERE id NOT IN (
    SELECT MAX(id)
    FROM customers
    GROUP BY email
);
```

### 3. Pivot Operations
```sql
-- Pivot sales by month
SELECT 
    product_id,
    SUM(CASE WHEN EXTRACT(MONTH FROM order_date) = 1 THEN amount ELSE 0 END) as jan_sales,
    SUM(CASE WHEN EXTRACT(MONTH FROM order_date) = 2 THEN amount ELSE 0 END) as feb_sales,
    SUM(CASE WHEN EXTRACT(MONTH FROM order_date) = 3 THEN amount ELSE 0 END) as mar_sales
FROM orders
GROUP BY product_id;
```

## ⚡ Performance Optimization

### 1. Indexing Strategy
```sql
-- Create indexes for common queries
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
CREATE INDEX idx_products_category ON products(category);

-- Partial indexes
CREATE INDEX idx_active_customers ON customers(created_date) 
WHERE status = 'active';
```

### 2. Query Optimization
```sql
-- Use EXISTS instead of IN for large subqueries
SELECT * FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id
);

-- Limit data early in the pipeline
SELECT customer_id, SUM(amount)
FROM orders
WHERE order_date >= '2023-01-01'  -- Filter early
GROUP BY customer_id;
```

## 📊 When to Use SQL
- **Data extraction**: Querying databases and data warehouses
- **Data transformation**: ETL processes, data cleaning
- **Analytics**: Reporting, business intelligence
- **Data validation**: Quality checks, constraint enforcement
- **Performance analysis**: Query optimization, indexing

## 🎯 Interview Focus Areas
1. **Joins**: Inner, outer, self-joins
2. **Window functions**: Ranking, running totals, lag/lead
3. **CTEs**: Recursive queries, complex transformations
4. **Performance**: Indexing, query optimization
5. **Data types**: Handling dates, strings, nulls
6. **Aggregations**: GROUP BY, HAVING, statistical functions
7. **Subqueries**: Correlated vs non-correlated

## 📚 Quick References
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQL Standard Reference](https://www.iso.org/standard/63555.html)
- [Window Functions Guide](https://www.postgresql.org/docs/current/tutorial-window.html)
- [Query Performance Tips](https://www.postgresql.org/docs/current/performance-tips.html)