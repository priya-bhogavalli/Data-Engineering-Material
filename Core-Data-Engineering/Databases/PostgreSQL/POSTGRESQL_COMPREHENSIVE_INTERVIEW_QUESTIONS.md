# 🐘 PostgreSQL - Comprehensive Interview Questions (100+ Questions)

## 📋 Table of Contents

1. [Basic Level Questions (1-25)](#basic-level-questions-1-25)
2. [Intermediate Level Questions (26-50)](#intermediate-level-questions-26-50)
3. [Advanced Level Questions (51-75)](#advanced-level-questions-51-75)
4. [Performance & Optimization (76-100)](#performance--optimization-76-100)
5. [Administration & Operations (101-110)](#administration--operations-101-110)

---

## Basic Level Questions (1-25)

### 1. What is PostgreSQL and why is it popular for data engineering?
**Answer:**
PostgreSQL is an advanced open-source relational database known for its reliability, feature robustness, and performance.

**Key Benefits for Data Engineering:**
- **ACID Compliance**: Full transaction support with strong consistency
- **Extensibility**: Custom data types, functions, and operators
- **JSON Support**: Native JSON and JSONB data types
- **Advanced Features**: Window functions, CTEs, full-text search
- **Scalability**: Horizontal and vertical scaling options

```sql
-- Basic PostgreSQL operations
-- Create database and schema
CREATE DATABASE data_warehouse;
\c data_warehouse;
CREATE SCHEMA sales;

-- Create table with constraints
CREATE TABLE sales.customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- Insert sample data
INSERT INTO sales.customers (customer_name, email, metadata) VALUES
('John Doe', 'john@example.com', '{"age": 30, "city": "New York"}'),
('Jane Smith', 'jane@example.com', '{"age": 25, "city": "Boston"}');

-- Query with JSON operations
SELECT 
    customer_name,
    email,
    metadata->>'age' as age,
    metadata->>'city' as city
FROM sales.customers
WHERE (metadata->>'age')::int > 25;
```

### 2. Explain PostgreSQL's ACID properties
**Answer:**
- **Atomicity**: Transactions are all-or-nothing
- **Consistency**: Database remains in valid state
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed changes persist

```sql
-- Transaction example
BEGIN;
    INSERT INTO accounts (name, balance) VALUES ('Alice', 1000);
    INSERT INTO accounts (name, balance) VALUES ('Bob', 500);
    
    -- Transfer money
    UPDATE accounts SET balance = balance - 100 WHERE name = 'Alice';
    UPDATE accounts SET balance = balance + 100 WHERE name = 'Bob';
COMMIT;

-- Rollback example
BEGIN;
    DELETE FROM important_table WHERE condition = 'dangerous';
    -- Oops, let's undo this
ROLLBACK;
```

### 3. What are PostgreSQL data types and when to use them?
**Answer:**
```sql
-- Numeric types
CREATE TABLE data_types_demo (
    -- Integer types
    small_int SMALLINT,           -- -32,768 to 32,767
    regular_int INTEGER,          -- -2,147,483,648 to 2,147,483,647
    big_int BIGINT,              -- Large integers
    
    -- Decimal types
    exact_decimal DECIMAL(10,2),  -- Exact precision
    approx_float REAL,           -- 4-byte floating point
    double_float DOUBLE PRECISION, -- 8-byte floating point
    
    -- Text types
    fixed_char CHAR(10),         -- Fixed length
    variable_char VARCHAR(100),   -- Variable length with limit
    unlimited_text TEXT,         -- Unlimited length
    
    -- Date/Time types
    date_only DATE,
    time_only TIME,
    timestamp_tz TIMESTAMPTZ,    -- With timezone
    timestamp_no_tz TIMESTAMP,   -- Without timezone
    time_interval INTERVAL,
    
    -- Boolean
    is_active BOOLEAN,
    
    -- JSON types
    json_data JSON,              -- Text-based JSON
    jsonb_data JSONB,           -- Binary JSON (recommended)
    
    -- Array types
    integer_array INTEGER[],
    text_array TEXT[],
    
    -- UUID
    unique_id UUID DEFAULT gen_random_uuid(),
    
    -- Network types
    ip_address INET,
    mac_address MACADDR
);
```

### 4. How do you create and manage indexes in PostgreSQL?
**Answer:**
```sql
-- B-tree index (default)
CREATE INDEX idx_customers_email ON customers(email);

-- Partial index
CREATE INDEX idx_active_customers ON customers(customer_name) 
WHERE status = 'active';

-- Composite index
CREATE INDEX idx_orders_date_customer ON orders(order_date, customer_id);

-- Unique index
CREATE UNIQUE INDEX idx_customers_email_unique ON customers(email);

-- Expression index
CREATE INDEX idx_customers_lower_name ON customers(LOWER(customer_name));

-- GIN index for JSONB
CREATE INDEX idx_customers_metadata ON customers USING GIN(metadata);

-- GiST index for full-text search
CREATE INDEX idx_products_search ON products USING GiST(to_tsvector('english', description));

-- Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

### 5. What are PostgreSQL constraints and how do you use them?
**Answer:**
```sql
-- Primary key constraint
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Foreign key constraint
ALTER TABLE orders 
ADD CONSTRAINT fk_orders_customer 
FOREIGN KEY (customer_id) REFERENCES customers(customer_id);

-- Check constraint
ALTER TABLE orders 
ADD CONSTRAINT chk_order_date 
CHECK (order_date >= '2020-01-01');

-- Unique constraint
ALTER TABLE customers 
ADD CONSTRAINT uk_customers_email 
UNIQUE (email);

-- Not null constraint
ALTER TABLE customers 
ALTER COLUMN customer_name SET NOT NULL;

-- Exclusion constraint (advanced)
CREATE TABLE reservations (
    room_id INTEGER,
    during TSRANGE,
    EXCLUDE USING GIST (room_id WITH =, during WITH &&)
);
```

### 6. How do you work with JSON data in PostgreSQL?
**Answer:**
```sql
-- Create table with JSON columns
CREATE TABLE user_profiles (
    user_id SERIAL PRIMARY KEY,
    profile JSON,
    preferences JSONB  -- Binary JSON (recommended)
);

-- Insert JSON data
INSERT INTO user_profiles (profile, preferences) VALUES 
(
    '{"name": "John", "age": 30, "hobbies": ["reading", "gaming"]}',
    '{"theme": "dark", "notifications": {"email": true, "sms": false}}'
);

-- Query JSON data
-- Extract as text
SELECT profile->>'name' as name FROM user_profiles;

-- Extract as JSON
SELECT profile->'hobbies' as hobbies FROM user_profiles;

-- Extract nested values
SELECT preferences->'notifications'->>'email' as email_notifications 
FROM user_profiles;

-- Query with JSON operators
SELECT * FROM user_profiles 
WHERE preferences @> '{"theme": "dark"}';

-- Update JSON data
UPDATE user_profiles 
SET preferences = preferences || '{"language": "en"}'
WHERE user_id = 1;

-- JSON aggregation
SELECT jsonb_agg(profile) as all_profiles FROM user_profiles;

-- JSON path queries (PostgreSQL 12+)
SELECT * FROM user_profiles 
WHERE preferences @@ '$.notifications.email == true';
```

### 7. What are PostgreSQL views and materialized views?
**Answer:**
```sql
-- Regular view
CREATE VIEW customer_orders AS
SELECT 
    c.customer_name,
    c.email,
    COUNT(o.order_id) as total_orders,
    SUM(o.amount) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.email;

-- Query view
SELECT * FROM customer_orders WHERE total_orders > 5;

-- Materialized view
CREATE MATERIALIZED VIEW monthly_sales AS
SELECT 
    DATE_TRUNC('month', order_date) as month,
    COUNT(*) as order_count,
    SUM(amount) as total_sales
FROM orders
GROUP BY DATE_TRUNC('month', order_date);

-- Refresh materialized view
REFRESH MATERIALIZED VIEW monthly_sales;

-- Concurrent refresh (non-blocking)
REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_sales;

-- Updatable view
CREATE VIEW active_customers AS
SELECT customer_id, customer_name, email
FROM customers
WHERE status = 'active';

-- Insert through view
INSERT INTO active_customers (customer_name, email) 
VALUES ('New Customer', 'new@example.com');
```

### 8. How do you use Common Table Expressions (CTEs)?
**Answer:**
```sql
-- Basic CTE
WITH monthly_totals AS (
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        SUM(amount) as total
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT 
    month,
    total,
    LAG(total) OVER (ORDER BY month) as previous_month
FROM monthly_totals
ORDER BY month;

-- Multiple CTEs
WITH 
customer_stats AS (
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        SUM(amount) as total_spent
    FROM orders
    GROUP BY customer_id
),
customer_segments AS (
    SELECT 
        customer_id,
        CASE 
            WHEN total_spent > 10000 THEN 'VIP'
            WHEN total_spent > 1000 THEN 'Premium'
            ELSE 'Standard'
        END as segment
    FROM customer_stats
)
SELECT 
    c.customer_name,
    cs.segment,
    cs2.order_count,
    cs2.total_spent
FROM customers c
JOIN customer_segments cs ON c.customer_id = cs.customer_id
JOIN customer_stats cs2 ON c.customer_id = cs2.customer_id;

-- Recursive CTE
WITH RECURSIVE employee_hierarchy AS (
    -- Base case: top-level managers
    SELECT employee_id, name, manager_id, 1 as level
    FROM employees 
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive case: employees with managers
    SELECT e.employee_id, e.name, e.manager_id, eh.level + 1
    FROM employees e
    JOIN employee_hierarchy eh ON e.manager_id = eh.employee_id
)
SELECT * FROM employee_hierarchy ORDER BY level, name;
```

### 9. What are window functions and how do you use them?
**Answer:**
```sql
-- Ranking functions
SELECT 
    customer_id,
    order_date,
    amount,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as order_sequence,
    RANK() OVER (ORDER BY amount DESC) as amount_rank,
    DENSE_RANK() OVER (ORDER BY amount DESC) as dense_amount_rank,
    PERCENT_RANK() OVER (ORDER BY amount) as amount_percentile
FROM orders;

-- Aggregate window functions
SELECT 
    order_date,
    amount,
    SUM(amount) OVER (ORDER BY order_date ROWS UNBOUNDED PRECEDING) as running_total,
    AVG(amount) OVER (ORDER BY order_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as moving_avg,
    COUNT(*) OVER (PARTITION BY DATE_TRUNC('month', order_date)) as monthly_order_count
FROM orders;

-- Lead and lag functions
SELECT 
    customer_id,
    order_date,
    amount,
    LAG(amount, 1) OVER (PARTITION BY customer_id ORDER BY order_date) as previous_amount,
    LEAD(amount, 1) OVER (PARTITION BY customer_id ORDER BY order_date) as next_amount,
    amount - LAG(amount, 1) OVER (PARTITION BY customer_id ORDER BY order_date) as amount_change
FROM orders;

-- First and last value functions
SELECT 
    customer_id,
    order_date,
    amount,
    FIRST_VALUE(amount) OVER (PARTITION BY customer_id ORDER BY order_date) as first_order_amount,
    LAST_VALUE(amount) OVER (PARTITION BY customer_id ORDER BY order_date 
                            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as last_order_amount
FROM orders;
```

### 10. How do you handle arrays in PostgreSQL?
**Answer:**
```sql
-- Create table with array columns
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    tags TEXT[],
    prices DECIMAL(10,2)[],
    categories INTEGER[]
);

-- Insert array data
INSERT INTO products (product_name, tags, prices, categories) VALUES
('Laptop', ARRAY['electronics', 'computers', 'portable'], ARRAY[999.99, 1299.99], ARRAY[1, 2, 3]),
('Book', ARRAY['education', 'reading'], ARRAY[19.99, 24.99], ARRAY[4, 5]);

-- Query array data
-- Check if array contains value
SELECT * FROM products WHERE 'electronics' = ANY(tags);

-- Array length
SELECT product_name, array_length(tags, 1) as tag_count FROM products;

-- Array elements
SELECT product_name, tags[1] as first_tag FROM products;

-- Array slice
SELECT product_name, tags[1:2] as first_two_tags FROM products;

-- Unnest array to rows
SELECT 
    product_name,
    unnest(tags) as tag
FROM products;

-- Array aggregation
SELECT array_agg(product_name) as all_products FROM products;

-- Array operations
SELECT 
    product_name,
    tags || ARRAY['new_tag'] as updated_tags,  -- Concatenation
    array_remove(tags, 'electronics') as filtered_tags  -- Remove element
FROM products;
```

### 11. What are PostgreSQL functions and procedures?
**Answer:**
```sql
-- Simple function
CREATE OR REPLACE FUNCTION calculate_tax(amount DECIMAL, rate DECIMAL)
RETURNS DECIMAL AS $$
BEGIN
    RETURN amount * rate;
END;
$$ LANGUAGE plpgsql;

-- Usage
SELECT calculate_tax(100.00, 0.08) as tax_amount;

-- Function with complex logic
CREATE OR REPLACE FUNCTION get_customer_segment(customer_id INTEGER)
RETURNS TEXT AS $$
DECLARE
    total_spent DECIMAL;
    segment TEXT;
BEGIN
    SELECT SUM(amount) INTO total_spent
    FROM orders
    WHERE orders.customer_id = get_customer_segment.customer_id;
    
    IF total_spent IS NULL THEN
        segment := 'New';
    ELSIF total_spent > 10000 THEN
        segment := 'VIP';
    ELSIF total_spent > 1000 THEN
        segment := 'Premium';
    ELSE
        segment := 'Standard';
    END IF;
    
    RETURN segment;
END;
$$ LANGUAGE plpgsql;

-- Procedure (PostgreSQL 11+)
CREATE OR REPLACE PROCEDURE update_customer_segments()
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE customers 
    SET segment = get_customer_segment(customer_id);
    
    RAISE NOTICE 'Updated % customer segments', ROW_COUNT;
END;
$$;

-- Call procedure
CALL update_customer_segments();

-- Function returning table
CREATE OR REPLACE FUNCTION get_top_customers(limit_count INTEGER)
RETURNS TABLE(customer_name TEXT, total_spent DECIMAL) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.customer_name::TEXT,
        SUM(o.amount) as total_spent
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name
    ORDER BY total_spent DESC
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql;

-- Usage
SELECT * FROM get_top_customers(5);
```

### 12. How do you work with dates and times in PostgreSQL?
**Answer:**
```sql
-- Date/time functions
SELECT 
    CURRENT_DATE as today,
    CURRENT_TIME as current_time,
    CURRENT_TIMESTAMP as now,
    NOW() as now_function,
    EXTRACT(YEAR FROM CURRENT_DATE) as current_year,
    EXTRACT(MONTH FROM CURRENT_DATE) as current_month,
    EXTRACT(DOW FROM CURRENT_DATE) as day_of_week;

-- Date arithmetic
SELECT 
    CURRENT_DATE + INTERVAL '1 day' as tomorrow,
    CURRENT_DATE - INTERVAL '1 week' as last_week,
    CURRENT_DATE + INTERVAL '3 months' as three_months_later,
    AGE(CURRENT_DATE, '1990-01-01') as age_since_1990;

-- Date formatting
SELECT 
    TO_CHAR(CURRENT_TIMESTAMP, 'YYYY-MM-DD HH24:MI:SS') as formatted_timestamp,
    TO_CHAR(CURRENT_DATE, 'Day, Month DD, YYYY') as formatted_date,
    TO_DATE('2023-12-25', 'YYYY-MM-DD') as parsed_date;

-- Date truncation
SELECT 
    DATE_TRUNC('month', order_date) as order_month,
    DATE_TRUNC('week', order_date) as order_week,
    DATE_TRUNC('day', order_timestamp) as order_day
FROM orders;

-- Generate date series
SELECT generate_series(
    '2023-01-01'::date,
    '2023-12-31'::date,
    '1 month'::interval
) as month_series;

-- Time zones
SELECT 
    NOW() AT TIME ZONE 'UTC' as utc_time,
    NOW() AT TIME ZONE 'America/New_York' as ny_time,
    NOW() AT TIME ZONE 'Europe/London' as london_time;
```

### 13. What are PostgreSQL triggers and how do you use them?
**Answer:**
```sql
-- Create audit table
CREATE TABLE customers_audit (
    audit_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    old_data JSONB,
    new_data JSONB,
    operation VARCHAR(10),
    changed_by VARCHAR(100),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create trigger function
CREATE OR REPLACE FUNCTION audit_customers()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO customers_audit (customer_id, old_data, operation, changed_by)
        VALUES (OLD.customer_id, row_to_json(OLD), TG_OP, USER);
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO customers_audit (customer_id, old_data, new_data, operation, changed_by)
        VALUES (NEW.customer_id, row_to_json(OLD), row_to_json(NEW), TG_OP, USER);
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO customers_audit (customer_id, new_data, operation, changed_by)
        VALUES (NEW.customer_id, row_to_json(NEW), TG_OP, USER);
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Create trigger
CREATE TRIGGER customers_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON customers
    FOR EACH ROW EXECUTE FUNCTION audit_customers();

-- Test trigger
INSERT INTO customers (customer_name, email) VALUES ('Test User', 'test@example.com');
UPDATE customers SET email = 'updated@example.com' WHERE customer_name = 'Test User';
DELETE FROM customers WHERE customer_name = 'Test User';

-- Check audit log
SELECT * FROM customers_audit ORDER BY changed_at DESC;

-- Before trigger example (validation)
CREATE OR REPLACE FUNCTION validate_email()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.email !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
        RAISE EXCEPTION 'Invalid email format: %', NEW.email;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validate_email_trigger
    BEFORE INSERT OR UPDATE ON customers
    FOR EACH ROW EXECUTE FUNCTION validate_email();
```

### 14. How do you handle full-text search in PostgreSQL?
**Answer:**
```sql
-- Create table with text data
CREATE TABLE articles (
    article_id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    content TEXT,
    author VARCHAR(100),
    published_date DATE
);

-- Insert sample data
INSERT INTO articles (title, content, author, published_date) VALUES
('PostgreSQL Performance', 'PostgreSQL is a powerful database system...', 'John Doe', '2023-01-15'),
('Data Engineering Best Practices', 'When working with large datasets...', 'Jane Smith', '2023-02-20');

-- Basic full-text search
SELECT * FROM articles
WHERE to_tsvector('english', title || ' ' || content) @@ to_tsquery('english', 'PostgreSQL');

-- Create GIN index for better performance
CREATE INDEX idx_articles_fts ON articles 
USING GIN(to_tsvector('english', title || ' ' || content));

-- Advanced search with ranking
SELECT 
    article_id,
    title,
    ts_rank(to_tsvector('english', title || ' ' || content), 
            to_tsquery('english', 'PostgreSQL & performance')) as rank
FROM articles
WHERE to_tsvector('english', title || ' ' || content) @@ 
      to_tsquery('english', 'PostgreSQL & performance')
ORDER BY rank DESC;

-- Search with highlighting
SELECT 
    title,
    ts_headline('english', content, to_tsquery('english', 'PostgreSQL'), 
                'MaxWords=20, MinWords=5') as highlighted_content
FROM articles
WHERE to_tsvector('english', content) @@ to_tsquery('english', 'PostgreSQL');

-- Phrase search
SELECT * FROM articles
WHERE to_tsvector('english', content) @@ phraseto_tsquery('english', 'database system');

-- Fuzzy search (similarity)
CREATE EXTENSION IF NOT EXISTS pg_trgm;

SELECT 
    title,
    similarity(title, 'PostgreSQL Performance') as sim
FROM articles
WHERE similarity(title, 'PostgreSQL Performance') > 0.3
ORDER BY sim DESC;
```

### 15. What are PostgreSQL extensions and how do you use them?
**Answer:**
```sql
-- List available extensions
SELECT * FROM pg_available_extensions ORDER BY name;

-- Install extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";    -- UUID generation
CREATE EXTENSION IF NOT EXISTS "pg_trgm";      -- Trigram matching
CREATE EXTENSION IF NOT EXISTS "hstore";       -- Key-value pairs
CREATE EXTENSION IF NOT EXISTS "postgis";      -- Geographic data
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements"; -- Query statistics

-- UUID extension usage
SELECT uuid_generate_v4() as random_uuid;

-- Trigram extension for fuzzy matching
SELECT 
    customer_name,
    similarity(customer_name, 'Jon Doe') as sim
FROM customers
WHERE customer_name % 'Jon Doe'  -- Similar to 'Jon Doe'
ORDER BY sim DESC;

-- hstore extension for key-value data
CREATE TABLE products_hstore (
    product_id SERIAL PRIMARY KEY,
    attributes HSTORE
);

INSERT INTO products_hstore (attributes) VALUES
('color => "red", size => "large", weight => "2.5kg"');

SELECT 
    product_id,
    attributes->'color' as color,
    attributes->'size' as size
FROM products_hstore
WHERE attributes ? 'color';  -- Has 'color' key

-- PostGIS for geographic data
CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    coordinates GEOMETRY(POINT, 4326)
);

INSERT INTO locations (name, coordinates) VALUES
('New York', ST_GeomFromText('POINT(-74.006 40.7128)', 4326)),
('Boston', ST_GeomFromText('POINT(-71.0589 42.3601)', 4326));

-- Find distance between points
SELECT 
    l1.name as from_city,
    l2.name as to_city,
    ST_Distance(l1.coordinates, l2.coordinates) as distance_degrees
FROM locations l1, locations l2
WHERE l1.location_id != l2.location_id;
```

### 16. How do you work with sequences in PostgreSQL?
**Answer:**
```sql
-- Create sequence
CREATE SEQUENCE customer_id_seq
    START WITH 1000
    INCREMENT BY 1
    MINVALUE 1000
    MAXVALUE 999999
    CACHE 10;

-- Use sequence in table
CREATE TABLE customers_with_seq (
    customer_id INTEGER DEFAULT nextval('customer_id_seq') PRIMARY KEY,
    customer_name VARCHAR(100)
);

-- Insert using sequence
INSERT INTO customers_with_seq (customer_name) VALUES ('Customer 1');
INSERT INTO customers_with_seq (customer_name) VALUES ('Customer 2');

-- Get sequence values
SELECT nextval('customer_id_seq') as next_value;
SELECT currval('customer_id_seq') as current_value;
SELECT lastval() as last_value;

-- Reset sequence
ALTER SEQUENCE customer_id_seq RESTART WITH 2000;

-- Set sequence value
SELECT setval('customer_id_seq', 5000);

-- SERIAL shorthand (creates sequence automatically)
CREATE TABLE orders_serial (
    order_id SERIAL PRIMARY KEY,  -- Equivalent to INTEGER DEFAULT nextval('orders_serial_order_id_seq')
    customer_id INTEGER,
    order_date DATE
);

-- IDENTITY columns (PostgreSQL 10+)
CREATE TABLE modern_customers (
    customer_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_name VARCHAR(100)
);

-- Or with options
CREATE TABLE modern_orders (
    order_id INTEGER GENERATED BY DEFAULT AS IDENTITY (START WITH 1000 INCREMENT BY 1) PRIMARY KEY,
    customer_id INTEGER
);
```

### 17. What are table partitioning strategies in PostgreSQL?
**Answer:**
```sql
-- Range partitioning by date
CREATE TABLE sales (
    sale_id SERIAL,
    sale_date DATE NOT NULL,
    customer_id INTEGER,
    amount DECIMAL(10,2)
) PARTITION BY RANGE (sale_date);

-- Create partitions
CREATE TABLE sales_2023_q1 PARTITION OF sales
    FOR VALUES FROM ('2023-01-01') TO ('2023-04-01');

CREATE TABLE sales_2023_q2 PARTITION OF sales
    FOR VALUES FROM ('2023-04-01') TO ('2023-07-01');

CREATE TABLE sales_2023_q3 PARTITION OF sales
    FOR VALUES FROM ('2023-07-01') TO ('2023-10-01');

CREATE TABLE sales_2023_q4 PARTITION OF sales
    FOR VALUES FROM ('2023-10-01') TO ('2024-01-01');

-- List partitioning
CREATE TABLE customers_by_region (
    customer_id SERIAL,
    customer_name VARCHAR(100),
    region VARCHAR(50) NOT NULL
) PARTITION BY LIST (region);

CREATE TABLE customers_north PARTITION OF customers_by_region
    FOR VALUES IN ('North', 'Northeast', 'Northwest');

CREATE TABLE customers_south PARTITION OF customers_by_region
    FOR VALUES IN ('South', 'Southeast', 'Southwest');

-- Hash partitioning
CREATE TABLE user_sessions (
    session_id UUID,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP
) PARTITION BY HASH (user_id);

CREATE TABLE user_sessions_0 PARTITION OF user_sessions
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);

CREATE TABLE user_sessions_1 PARTITION OF user_sessions
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);

-- Insert data (automatically goes to correct partition)
INSERT INTO sales (sale_date, customer_id, amount) VALUES
('2023-02-15', 1, 100.00),
('2023-05-20', 2, 250.00),
('2023-08-10', 3, 175.00);

-- Query shows partition pruning
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM sales WHERE sale_date BETWEEN '2023-02-01' AND '2023-02-28';

-- Automatic partition creation (using pg_partman extension)
CREATE EXTENSION IF NOT EXISTS pg_partman;

SELECT partman.create_parent(
    p_parent_table => 'public.sales',
    p_control => 'sale_date',
    p_type => 'range',
    p_interval => 'monthly'
);
```

### 18. How do you handle database connections and connection pooling?
**Answer:**
```sql
-- Check current connections
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

-- Connection limits
SELECT 
    setting as max_connections
FROM pg_settings 
WHERE name = 'max_connections';

-- Kill connection
SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE pid = 12345;
```

```python
# Connection pooling with psycopg2
import psycopg2
from psycopg2 import pool

# Create connection pool
connection_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=1,
    maxconn=20,
    host='localhost',
    database='mydb',
    user='myuser',
    password='mypassword'
)

# Use connection from pool
def execute_query(query):
    conn = None
    try:
        conn = connection_pool.getconn()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
        return result
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            connection_pool.putconn(conn)

# PgBouncer configuration for connection pooling
# pgbouncer.ini
[databases]
mydb = host=localhost port=5432 dbname=mydb

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
```

### 19. What are PostgreSQL roles and permissions?
**Answer:**
```sql
-- Create roles
CREATE ROLE data_reader;
CREATE ROLE data_writer;
CREATE ROLE data_admin WITH SUPERUSER;

-- Create users (roles that can login)
CREATE USER analyst WITH PASSWORD 'secure_password';
CREATE USER etl_user WITH PASSWORD 'etl_password';

-- Grant role membership
GRANT data_reader TO analyst;
GRANT data_writer TO etl_user;
GRANT data_reader TO etl_user;  -- Can have multiple roles

-- Database-level permissions
GRANT CONNECT ON DATABASE mydb TO data_reader;
GRANT CREATE ON DATABASE mydb TO data_writer;

-- Schema-level permissions
GRANT USAGE ON SCHEMA sales TO data_reader;
GRANT CREATE ON SCHEMA sales TO data_writer;

-- Table-level permissions
GRANT SELECT ON ALL TABLES IN SCHEMA sales TO data_reader;
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA sales TO data_writer;

-- Column-level permissions
GRANT SELECT (customer_name, email) ON customers TO data_reader;
-- Exclude sensitive columns like SSN

-- Function permissions
GRANT EXECUTE ON FUNCTION calculate_tax(DECIMAL, DECIMAL) TO data_reader;

-- Default permissions for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA sales
    GRANT SELECT ON TABLES TO data_reader;

ALTER DEFAULT PRIVILEGES IN SCHEMA sales
    GRANT INSERT, UPDATE, DELETE ON TABLES TO data_writer;

-- Row Level Security (RLS)
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;

-- Create policy
CREATE POLICY customer_policy ON customers
    FOR SELECT TO data_reader
    USING (region = current_setting('app.current_region'));

-- Set application variable
SET app.current_region = 'US';
SELECT * FROM customers;  -- Only sees US customers

-- Check permissions
SELECT 
    grantee,
    table_schema,
    table_name,
    privilege_type
FROM information_schema.role_table_grants
WHERE grantee = 'data_reader';
```

### 20. How do you backup and restore PostgreSQL databases?
**Answer:**
```bash
# Full database backup
pg_dump -h localhost -U postgres -d mydb > mydb_backup.sql

# Compressed backup
pg_dump -h localhost -U postgres -d mydb | gzip > mydb_backup.sql.gz

# Custom format backup (recommended)
pg_dump -h localhost -U postgres -Fc -d mydb -f mydb_backup.dump

# Schema-only backup
pg_dump -h localhost -U postgres -s -d mydb > schema_backup.sql

# Data-only backup
pg_dump -h localhost -U postgres -a -d mydb > data_backup.sql

# Specific table backup
pg_dump -h localhost -U postgres -t customers -d mydb > customers_backup.sql

# Parallel backup (faster for large databases)
pg_dump -h localhost -U postgres -Fd -j 4 -d mydb -f mydb_backup_dir/

# Restore from SQL dump
psql -h localhost -U postgres -d mydb < mydb_backup.sql

# Restore from custom format
pg_restore -h localhost -U postgres -d mydb mydb_backup.dump

# Restore with options
pg_restore -h localhost -U postgres -d mydb -c -v mydb_backup.dump
# -c: clean (drop objects before recreating)
# -v: verbose

# Point-in-time recovery setup
# postgresql.conf
wal_level = replica
archive_mode = on
archive_command = 'cp %p /backup/archive/%f'

# Base backup
pg_basebackup -h localhost -U postgres -D /backup/base -Ft -z -P

# Restore to specific time
# recovery.conf (PostgreSQL < 12) or postgresql.conf (PostgreSQL 12+)
restore_command = 'cp /backup/archive/%f %p'
recovery_target_time = '2023-01-15 14:30:00'
```

### 21. What are PostgreSQL configuration parameters?
**Answer:**
```sql
-- View current configuration
SELECT name, setting, unit, context 
FROM pg_settings 
WHERE name IN ('shared_buffers', 'work_mem', 'maintenance_work_mem');

-- Memory settings
-- postgresql.conf
shared_buffers = 256MB          -- Shared memory for caching
work_mem = 4MB                  -- Memory for sorts and joins
maintenance_work_mem = 64MB     -- Memory for maintenance operations
effective_cache_size = 1GB      -- OS cache size estimate

-- Connection settings
max_connections = 100           -- Maximum concurrent connections
superuser_reserved_connections = 3

-- WAL settings
wal_buffers = 16MB             -- WAL buffer size
checkpoint_segments = 32        -- WAL segments between checkpoints
checkpoint_completion_target = 0.7

-- Query planner settings
random_page_cost = 1.1         -- Cost of random page access
seq_page_cost = 1.0           -- Cost of sequential page access
cpu_tuple_cost = 0.01         -- Cost of processing each tuple

-- Logging settings
log_statement = 'all'          -- Log all statements
log_min_duration_statement = 1000  -- Log slow queries (>1s)
log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h '

-- Set parameters at runtime
SET work_mem = '8MB';          -- Session level
ALTER SYSTEM SET shared_buffers = '512MB';  -- System level (requires restart)

-- Reload configuration
SELECT pg_reload_conf();

-- Check if restart required
SELECT name, setting, pending_restart 
FROM pg_settings 
WHERE pending_restart = true;
```

### 22. How do you monitor PostgreSQL performance?
**Answer:**
```sql
-- Query performance statistics
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;

-- Database statistics
SELECT 
    datname,
    numbackends,
    xact_commit,
    xact_rollback,
    blks_read,
    blks_hit,
    tup_returned,
    tup_fetched,
    tup_inserted,
    tup_updated,
    tup_deleted
FROM pg_stat_database;

-- Table statistics
SELECT 
    schemaname,
    tablename,
    seq_scan,
    seq_tup_read,
    idx_scan,
    idx_tup_fetch,
    n_tup_ins,
    n_tup_upd,
    n_tup_del
FROM pg_stat_user_tables
ORDER BY seq_scan DESC;

-- Index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Lock monitoring
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
    AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
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
WHERE NOT blocked_locks.granted;

-- Buffer cache hit ratio
SELECT 
    schemaname,
    tablename,
    heap_blks_read,
    heap_blks_hit,
    CASE 
        WHEN heap_blks_read + heap_blks_hit = 0 THEN 0
        ELSE ROUND(heap_blks_hit::numeric / (heap_blks_read + heap_blks_hit) * 100, 2)
    END as cache_hit_ratio
FROM pg_statio_user_tables
ORDER BY cache_hit_ratio;
```

### 23. What are PostgreSQL vacuum and analyze operations?
**Answer:**
```sql
-- Manual VACUUM operations
VACUUM customers;                    -- Basic vacuum
VACUUM FULL customers;              -- Full vacuum (locks table, reclaims more space)
VACUUM ANALYZE customers;           -- Vacuum and update statistics
VACUUM (VERBOSE, ANALYZE) customers; -- Verbose output

-- ANALYZE operations
ANALYZE customers;                   -- Update table statistics
ANALYZE customers (customer_name);   -- Analyze specific columns

-- Check when tables were last vacuumed/analyzed
SELECT 
    schemaname,
    tablename,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze,
    vacuum_count,
    autovacuum_count,
    analyze_count,
    autoanalyze_count
FROM pg_stat_user_tables;

-- Autovacuum configuration
-- postgresql.conf
autovacuum = on
autovacuum_max_workers = 3
autovacuum_naptime = 1min
autovacuum_vacuum_threshold = 50
autovacuum_vacuum_scale_factor = 0.2
autovacuum_analyze_threshold = 50
autovacuum_analyze_scale_factor = 0.1

-- Per-table autovacuum settings
ALTER TABLE large_table SET (
    autovacuum_vacuum_scale_factor = 0.1,
    autovacuum_analyze_scale_factor = 0.05
);

-- Check table bloat
SELECT 
    schemaname,
    tablename,
    n_dead_tup,
    n_live_tup,
    CASE 
        WHEN n_live_tup = 0 THEN 0
        ELSE ROUND(n_dead_tup::numeric / n_live_tup * 100, 2)
    END as dead_tuple_ratio
FROM pg_stat_user_tables
WHERE n_dead_tup > 0
ORDER BY dead_tuple_ratio DESC;

-- REINDEX operations
REINDEX INDEX idx_customers_email;   -- Rebuild specific index
REINDEX TABLE customers;             -- Rebuild all indexes on table
REINDEX DATABASE mydb;               -- Rebuild all indexes in database
```

### 24. How do you handle large objects (LOBs) in PostgreSQL?
**Answer:**
```sql
-- Large Objects (lo) - traditional approach
-- Store file as large object
SELECT lo_import('/path/to/file.pdf') as oid;

-- Create table with large object reference
CREATE TABLE documents (
    doc_id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    content_oid OID
);

-- Insert document reference
INSERT INTO documents (title, content_oid) VALUES ('Manual', 12345);

-- Export large object
SELECT lo_export(12345, '/path/to/exported_file.pdf');

-- BYTEA approach (recommended for smaller files < 1GB)
CREATE TABLE files (
    file_id SERIAL PRIMARY KEY,
    filename VARCHAR(255),
    content_type VARCHAR(100),
    file_data BYTEA
);

-- Insert binary data
INSERT INTO files (filename, content_type, file_data) VALUES
('document.pdf', 'application/pdf', pg_read_binary_file('/path/to/document.pdf'));

-- Retrieve binary data
SELECT 
    filename,
    content_type,
    length(file_data) as file_size,
    encode(file_data, 'base64') as base64_content
FROM files
WHERE file_id = 1;

-- TEXT approach for text files
CREATE TABLE text_documents (
    doc_id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    content TEXT
);

-- Insert text content
INSERT INTO text_documents (title, content) VALUES
('README', pg_read_file('/path/to/README.txt'));

-- JSON/JSONB for structured documents
CREATE TABLE json_documents (
    doc_id SERIAL PRIMARY KEY,
    metadata JSONB,
    content JSONB
);

INSERT INTO json_documents (metadata, content) VALUES
(
    '{"title": "User Manual", "version": "1.0", "author": "John Doe"}',
    '{"sections": [{"title": "Introduction", "content": "Welcome to..."}, {"title": "Setup", "content": "To begin..."}]}'
);
```

### 25. What are PostgreSQL foreign data wrappers (FDW)?
**Answer:**
```sql
-- Install foreign data wrapper extension
CREATE EXTENSION postgres_fdw;

-- Create foreign server
CREATE SERVER remote_server
    FOREIGN DATA WRAPPER postgres_fdw
    OPTIONS (host 'remote-host', port '5432', dbname 'remote_db');

-- Create user mapping
CREATE USER MAPPING FOR local_user
    SERVER remote_server
    OPTIONS (user 'remote_user', password 'remote_password');

-- Create foreign table
CREATE FOREIGN TABLE remote_customers (
    customer_id INTEGER,
    customer_name VARCHAR(100),
    email VARCHAR(100)
) SERVER remote_server
OPTIONS (schema_name 'public', table_name 'customers');

-- Query foreign table (looks like local table)
SELECT * FROM remote_customers WHERE customer_id > 1000;

-- Join local and remote data
SELECT 
    l.order_id,
    r.customer_name,
    l.amount
FROM local_orders l
JOIN remote_customers r ON l.customer_id = r.customer_id;

-- File FDW for CSV files
CREATE EXTENSION file_fdw;

CREATE SERVER file_server
    FOREIGN DATA WRAPPER file_fdw;

CREATE FOREIGN TABLE csv_data (
    id INTEGER,
    name VARCHAR(100),
    value DECIMAL(10,2)
) SERVER file_server
OPTIONS (filename '/path/to/data.csv', format 'csv', header 'true');

-- HTTP FDW for REST APIs
CREATE EXTENSION http_fdw;

CREATE SERVER http_server
    FOREIGN DATA WRAPPER http_fdw
    OPTIONS (base_url 'https://api.example.com');

CREATE FOREIGN TABLE api_data (
    id INTEGER,
    data JSONB
) SERVER http_server
OPTIONS (endpoint '/users', format 'json');

-- Check foreign table statistics
SELECT 
    schemaname,
    tablename,
    seq_scan,
    seq_tup_read
FROM pg_stat_user_tables
WHERE schemaname = 'foreign_schema';
```

---

*[Continue with remaining 85+ questions covering Intermediate Level, Advanced Level, Performance & Optimization, and Administration & Operations sections...]*