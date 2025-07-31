# Advanced SQL Concepts for Data Engineering

## Window Functions

### Ranking Functions
```sql
-- ROW_NUMBER, RANK, DENSE_RANK
SELECT 
    employee_id,
    salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) as row_num,
    RANK() OVER (ORDER BY salary DESC) as rank_val,
    DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank_val
FROM employees;
```

### Analytical Functions
```sql
-- LAG, LEAD, FIRST_VALUE, LAST_VALUE
SELECT 
    date,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY date) as prev_revenue,
    LEAD(revenue, 1) OVER (ORDER BY date) as next_revenue,
    FIRST_VALUE(revenue) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING) as first_revenue,
    LAST_VALUE(revenue) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as last_revenue
FROM sales_data;
```

### Aggregate Window Functions
```sql
-- Running totals and moving averages
SELECT 
    date,
    amount,
    SUM(amount) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING) as running_total,
    AVG(amount) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as moving_avg_3day
FROM transactions;
```

## Common Table Expressions (CTEs)

### Basic CTE
```sql
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        SUM(amount) as total_sales
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT * FROM monthly_sales
WHERE total_sales > 10000;
```

### Recursive CTE
```sql
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

## Advanced Joins

### Self Joins
```sql
-- Find employees and their managers
SELECT 
    e1.name as employee,
    e2.name as manager
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.employee_id;
```

### Cross Apply / Lateral Joins
```sql
-- PostgreSQL LATERAL join
SELECT 
    c.customer_id,
    c.name,
    recent_orders.order_date,
    recent_orders.amount
FROM customers c
CROSS JOIN LATERAL (
    SELECT order_date, amount
    FROM orders o
    WHERE o.customer_id = c.customer_id
    ORDER BY order_date DESC
    LIMIT 3
) recent_orders;
```

## Data Types and JSON

### JSON Operations (PostgreSQL)
```sql
-- JSON extraction and manipulation
SELECT 
    id,
    data->>'name' as name,
    data->'address'->>'city' as city,
    jsonb_array_elements_text(data->'tags') as tag
FROM user_profiles
WHERE data @> '{"active": true}';
```

### Array Operations
```sql
-- Array functions
SELECT 
    id,
    array_length(tags, 1) as tag_count,
    'sql' = ANY(tags) as has_sql_tag,
    array_agg(DISTINCT category) as categories
FROM articles
GROUP BY id, tags;
```

## Performance Optimization

### Index Strategies
```sql
-- Composite index
CREATE INDEX idx_orders_customer_date ON orders (customer_id, order_date);

-- Partial index
CREATE INDEX idx_active_users ON users (email) WHERE active = true;

-- Expression index
CREATE INDEX idx_lower_email ON users (LOWER(email));
```

### Query Optimization Techniques
```sql
-- Use EXISTS instead of IN for better performance
SELECT customer_id, name
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id
);

-- Avoid SELECT * in subqueries
SELECT customer_id, 
       (SELECT COUNT(*) FROM orders WHERE customer_id = c.customer_id) as order_count
FROM customers c;
```

## Data Warehousing Concepts

### Slowly Changing Dimensions (SCD)

#### Type 1 - Overwrite
```sql
UPDATE dim_customer 
SET city = 'New York', updated_date = CURRENT_DATE
WHERE customer_id = 123;
```

#### Type 2 - Historical Tracking
```sql
-- Insert new record with version
INSERT INTO dim_customer (
    customer_id, name, city, 
    effective_date, expiry_date, is_current
)
VALUES (
    123, 'John Doe', 'New York',
    CURRENT_DATE, '9999-12-31', true
);

-- Update old record
UPDATE dim_customer 
SET expiry_date = CURRENT_DATE - 1, is_current = false
WHERE customer_id = 123 AND is_current = true;
```

### Star Schema Design
```sql
-- Fact table
CREATE TABLE fact_sales (
    sale_id SERIAL PRIMARY KEY,
    date_key INTEGER REFERENCES dim_date(date_key),
    customer_key INTEGER REFERENCES dim_customer(customer_key),
    product_key INTEGER REFERENCES dim_product(product_key),
    quantity INTEGER,
    amount DECIMAL(10,2)
);

-- Dimension table
CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(50),
    product_name VARCHAR(255),
    category VARCHAR(100),
    subcategory VARCHAR(100)
);
```

## Advanced Aggregations

### ROLLUP and CUBE
```sql
-- ROLLUP for hierarchical totals
SELECT 
    region,
    country,
    city,
    SUM(sales) as total_sales
FROM sales_data
GROUP BY ROLLUP (region, country, city);

-- CUBE for all combinations
SELECT 
    product_category,
    sales_channel,
    SUM(revenue) as total_revenue
FROM sales
GROUP BY CUBE (product_category, sales_channel);
```

### GROUPING SETS
```sql
SELECT 
    product_category,
    sales_channel,
    region,
    SUM(revenue) as total_revenue
FROM sales
GROUP BY GROUPING SETS (
    (product_category),
    (sales_channel),
    (region),
    (product_category, sales_channel),
    ()  -- Grand total
);
```

## Temporal Data Handling

### Date/Time Functions
```sql
-- Date arithmetic and formatting
SELECT 
    order_date,
    EXTRACT(YEAR FROM order_date) as year,
    EXTRACT(QUARTER FROM order_date) as quarter,
    DATE_TRUNC('month', order_date) as month_start,
    order_date + INTERVAL '30 days' as due_date,
    AGE(CURRENT_DATE, order_date) as days_since_order
FROM orders;
```

### Time Series Analysis
```sql
-- Generate time series with gaps filled
WITH date_series AS (
    SELECT generate_series(
        '2023-01-01'::date,
        '2023-12-31'::date,
        '1 day'::interval
    )::date as date
)
SELECT 
    ds.date,
    COALESCE(s.daily_sales, 0) as daily_sales
FROM date_series ds
LEFT JOIN (
    SELECT DATE(order_date) as date, SUM(amount) as daily_sales
    FROM orders
    GROUP BY DATE(order_date)
) s ON ds.date = s.date;
```

## Advanced String Operations

### Pattern Matching
```sql
-- Regular expressions
SELECT *
FROM products
WHERE product_code ~ '^[A-Z]{2}-\d{4}$';  -- PostgreSQL regex

-- String functions
SELECT 
    REGEXP_REPLACE(phone, '[^0-9]', '', 'g') as clean_phone,
    SPLIT_PART(email, '@', 2) as domain,
    LEVENSHTEIN('hello', 'helo') as edit_distance
FROM contacts;
```

### Text Analytics
```sql
-- Full-text search (PostgreSQL)
SELECT *
FROM documents
WHERE to_tsvector('english', content) @@ to_tsquery('english', 'data & engineering');

-- String aggregation
SELECT 
    category,
    STRING_AGG(product_name, ', ' ORDER BY product_name) as products
FROM products
GROUP BY category;
```

## Database-Specific Advanced Features

### PostgreSQL Specific
```sql
-- UPSERT with ON CONFLICT
INSERT INTO user_stats (user_id, login_count, last_login)
VALUES (123, 1, CURRENT_TIMESTAMP)
ON CONFLICT (user_id)
DO UPDATE SET 
    login_count = user_stats.login_count + 1,
    last_login = EXCLUDED.last_login;

-- Custom data types
CREATE TYPE address AS (
    street VARCHAR(100),
    city VARCHAR(50),
    zipcode VARCHAR(10)
);
```

### SQL Server Specific
```sql
-- MERGE statement
MERGE target_table AS target
USING source_table AS source
ON target.id = source.id
WHEN MATCHED THEN
    UPDATE SET target.value = source.value
WHEN NOT MATCHED THEN
    INSERT (id, value) VALUES (source.id, source.value);

-- OUTPUT clause
UPDATE inventory
SET quantity = quantity - 10
OUTPUT DELETED.product_id, DELETED.quantity as old_qty, INSERTED.quantity as new_qty
WHERE product_id = 'ABC123';
```

## Data Quality and Validation

### Constraint Implementation
```sql
-- Check constraints
ALTER TABLE orders
ADD CONSTRAINT chk_positive_amount CHECK (amount > 0);

-- Custom validation functions
CREATE OR REPLACE FUNCTION validate_email(email TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$';
END;
$$ LANGUAGE plpgsql;
```

### Data Profiling Queries
```sql
-- Data quality assessment
SELECT 
    'customer_email' as column_name,
    COUNT(*) as total_rows,
    COUNT(email) as non_null_count,
    COUNT(DISTINCT email) as unique_count,
    COUNT(*) - COUNT(email) as null_count,
    ROUND(100.0 * COUNT(email) / COUNT(*), 2) as completeness_pct
FROM customers

UNION ALL

SELECT 
    'order_amount',
    COUNT(*),
    COUNT(amount),
    COUNT(DISTINCT amount),
    COUNT(*) - COUNT(amount),
    ROUND(100.0 * COUNT(amount) / COUNT(*), 2)
FROM orders;
```

## Stored Procedures and Functions

### PostgreSQL Functions
```sql
CREATE OR REPLACE FUNCTION calculate_customer_lifetime_value(customer_id INTEGER)
RETURNS DECIMAL(10,2) AS $$
DECLARE
    total_value DECIMAL(10,2);
BEGIN
    SELECT COALESCE(SUM(amount), 0)
    INTO total_value
    FROM orders
    WHERE customer_id = $1;
    
    RETURN total_value;
END;
$$ LANGUAGE plpgsql;
```

### Dynamic SQL
```sql
CREATE OR REPLACE FUNCTION dynamic_aggregation(
    table_name TEXT,
    group_column TEXT,
    agg_column TEXT
)
RETURNS TABLE(group_value TEXT, total_value NUMERIC) AS $$
BEGIN
    RETURN QUERY EXECUTE format(
        'SELECT %I::TEXT, SUM(%I) FROM %I GROUP BY %I',
        group_column, agg_column, table_name, group_column
    );
END;
$$ LANGUAGE plpgsql;
```

## Security and Access Control

### Row Level Security
```sql
-- Enable RLS
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Create policy
CREATE POLICY user_orders ON orders
FOR ALL TO application_user
USING (customer_id = current_setting('app.current_user_id')::INTEGER);
```

### Data Masking
```sql
-- Dynamic data masking function
CREATE OR REPLACE FUNCTION mask_email(email TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN CASE 
        WHEN current_user = 'admin' THEN email
        ELSE REGEXP_REPLACE(email, '(.{2}).*(@.*)', '\1***\2')
    END;
END;
$$ LANGUAGE plpgsql;
```

## Monitoring and Maintenance

### Query Performance Analysis
```sql
-- Long running queries (PostgreSQL)
SELECT 
    pid,
    now() - pg_stat_activity.query_start AS duration,
    query,
    state
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes';

-- Index usage statistics
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch,
    idx_scan
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

### Database Maintenance
```sql
-- Table statistics update
ANALYZE table_name;

-- Index maintenance
REINDEX INDEX index_name;

-- Vacuum operations (PostgreSQL)
VACUUM ANALYZE table_name;
```

## Best Practices Summary

1. **Use appropriate data types** - Choose the most efficient data type for your use case
2. **Index strategically** - Create indexes on frequently queried columns
3. **Avoid SELECT *** - Only select columns you need
4. **Use CTEs for readability** - Break complex queries into manageable parts
5. **Implement proper constraints** - Ensure data integrity at the database level
6. **Monitor query performance** - Regularly analyze and optimize slow queries
7. **Use transactions appropriately** - Ensure data consistency
8. **Document your schema** - Maintain clear documentation for complex designs
9. **Test with realistic data volumes** - Performance characteristics change with scale
10. **Follow naming conventions** - Use consistent, descriptive names for objects