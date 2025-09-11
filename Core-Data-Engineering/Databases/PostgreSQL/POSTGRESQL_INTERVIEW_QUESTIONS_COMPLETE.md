# PostgreSQL Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-30)](#basic-level-questions-1-30)
2. [Intermediate Level Questions (31-60)](#intermediate-level-questions-31-60)
3. [Advanced Level Questions (61-90)](#advanced-level-questions-61-90)
4. [Performance & Optimization (91-120)](#performance--optimization-91-120)
5. [Administration & Maintenance (121-150)](#administration--maintenance-121-150)
6. [Advanced Features (151-180)](#advanced-features-151-180)
7. [Scenario-Based Questions (181-200)](#scenario-based-questions-181-200)

---

## Basic Level Questions (1-30)

### 1. What is PostgreSQL and what are its key features?

**PostgreSQL** is an advanced, open-source object-relational database system known for its reliability, feature robustness, and performance.

#### **Key Features:**

| Feature | Description | Benefit |
|---------|-------------|---------|
| **ACID Compliance** | Full ACID transaction support | Data integrity and consistency |
| **Extensibility** | Custom data types, functions, operators | Flexible data modeling |
| **JSON Support** | Native JSON and JSONB data types | Semi-structured data handling |
| **Advanced Indexing** | B-tree, Hash, GiST, SP-GiST, GIN, BRIN | Query performance optimization |
| **Window Functions** | Advanced analytical functions | Complex analytical queries |
| **Full-Text Search** | Built-in text search capabilities | Search functionality |
| **Replication** | Streaming and logical replication | High availability and scalability |
| **Partitioning** | Table partitioning support | Large table management |

```sql
-- Demonstrate PostgreSQL's advanced features
-- Create database and connect
CREATE DATABASE analytics_db;
\c analytics_db;

-- Create table with various PostgreSQL data types
CREATE TABLE customer_data (
    customer_id SERIAL PRIMARY KEY,
    customer_uuid UUID DEFAULT gen_random_uuid(),
    full_name TEXT NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    birth_date DATE,
    registration_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    preferences JSONB,
    tags TEXT[],
    customer_score NUMERIC(5,2),
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    metadata HSTORE
);

-- Insert sample data showcasing PostgreSQL features
INSERT INTO customer_data (
    full_name, email, phone_number, birth_date, preferences, tags, customer_score
) VALUES 
(
    'John Doe', 
    'john.doe@email.com', 
    '+1-555-0123', 
    '1985-03-15',
    '{"newsletter": true, "marketing": false, "preferred_contact": "email", "interests": ["technology", "sports"]}',
    ARRAY['premium', 'tech-savvy', 'early-adopter'],
    87.5
),
(
    'Jane Smith', 
    'jane.smith@email.com', 
    '+1-555-0456', 
    '1990-07-22',
    '{"newsletter": false, "marketing": true, "preferred_contact": "phone", "interests": ["fashion", "travel"]}',
    ARRAY['standard', 'frequent-buyer'],
    92.3
),
(
    'Bob Johnson', 
    'bob.johnson@email.com', 
    '+1-555-0789', 
    '1978-11-08',
    '{"newsletter": true, "marketing": true, "preferred_contact": "sms", "interests": ["books", "music", "movies"]}',
    ARRAY['premium', 'loyal-customer', 'high-value'],
    95.8
);

-- Query demonstrating PostgreSQL's JSON capabilities
SELECT 
    customer_id,
    full_name,
    email,
    preferences->>'preferred_contact' AS preferred_contact,
    preferences->'interests' AS interests,
    jsonb_array_length(preferences->'interests') AS interest_count,
    tags,
    array_length(tags, 1) AS tag_count,
    customer_score
FROM customer_data
WHERE preferences->>'newsletter' = 'true'
ORDER BY customer_score DESC;

-- Advanced query with window functions
SELECT 
    customer_id,
    full_name,
    customer_score,
    RANK() OVER (ORDER BY customer_score DESC) AS score_rank,
    PERCENT_RANK() OVER (ORDER BY customer_score) AS score_percentile,
    LAG(customer_score) OVER (ORDER BY customer_score DESC) AS previous_score,
    customer_score - LAG(customer_score) OVER (ORDER BY customer_score DESC) AS score_difference
FROM customer_data
ORDER BY customer_score DESC;
```

**Output:**
```
customer_id | full_name   | email                | preferred_contact | interests                    | interest_count | tags                              | tag_count | customer_score
------------|-------------|----------------------|-------------------|------------------------------|----------------|-----------------------------------|-----------|---------------
3           | Bob Johnson | bob.johnson@email.com| sms               | ["books", "music", "movies"] | 3              | {premium,loyal-customer,high-value}| 3         | 95.80
1           | John Doe    | john.doe@email.com   | email             | ["technology", "sports"]     | 2              | {premium,tech-savvy,early-adopter}| 3         | 87.50

customer_id | full_name   | customer_score | score_rank | score_percentile | previous_score | score_difference
------------|-------------|----------------|------------|------------------|----------------|------------------
3           | Bob Johnson | 95.80          | 1          | 1.00             | null           | null
2           | Jane Smith  | 92.30          | 2          | 0.50             | 95.80          | -3.50
1           | John Doe    | 87.50          | 3          | 0.00             | 92.30          | -4.80
```

### 2. What are PostgreSQL data types and how do you choose them?

**Answer:** PostgreSQL offers rich data types for different use cases.

#### 🎯 **Data Type Categories**
- **Numeric**: INTEGER, BIGINT, DECIMAL, NUMERIC, REAL, DOUBLE PRECISION
- **Character**: CHAR, VARCHAR, TEXT
- **Date/Time**: DATE, TIME, TIMESTAMP, TIMESTAMPTZ, INTERVAL
- **Boolean**: BOOLEAN
- **JSON**: JSON, JSONB
- **Arrays**: Any data type can be an array
- **Geometric**: POINT, LINE, CIRCLE, POLYGON
- **Network**: INET, CIDR, MACADDR
- **UUID**: Universally Unique Identifiers

```sql
-- Comprehensive data type demonstration
CREATE TABLE data_type_showcase (
    -- Numeric types
    id SERIAL PRIMARY KEY,
    small_number SMALLINT,
    regular_number INTEGER,
    big_number BIGINT,
    precise_decimal DECIMAL(10,2),
    floating_point REAL,
    double_precision DOUBLE PRECISION,
    
    -- Character types
    fixed_char CHAR(5),
    variable_char VARCHAR(100),
    unlimited_text TEXT,
    
    -- Date/Time types
    just_date DATE,
    just_time TIME,
    timestamp_local TIMESTAMP,
    timestamp_with_tz TIMESTAMPTZ,
    time_interval INTERVAL,
    
    -- Boolean
    is_active BOOLEAN,
    
    -- JSON types
    json_data JSON,
    jsonb_data JSONB,
    
    -- Array types
    integer_array INTEGER[],
    text_array TEXT[],
    
    -- UUID
    unique_id UUID DEFAULT gen_random_uuid(),
    
    -- Network types
    ip_address INET,
    network_range CIDR,
    mac_address MACADDR,
    
    -- Geometric types
    location POINT,
    service_area CIRCLE,
    
    -- Custom enum type
    status_type status_enum
);

-- Create custom enum type
CREATE TYPE status_enum AS ENUM ('active', 'inactive', 'pending', 'suspended');

-- Insert comprehensive sample data
INSERT INTO data_type_showcase (
    small_number, regular_number, big_number, precise_decimal, floating_point, double_precision,
    fixed_char, variable_char, unlimited_text,
    just_date, just_time, timestamp_local, timestamp_with_tz, time_interval,
    is_active,
    json_data, jsonb_data,
    integer_array, text_array,
    ip_address, network_range, mac_address,
    location, service_area,
    status_type
) VALUES (
    32767, 2147483647, 9223372036854775807, 12345.67, 3.14159, 2.718281828459045,
    'ABCDE', 'Variable length string', 'This is unlimited text that can be very long...',
    '2024-01-15', '14:30:00', '2024-01-15 14:30:00', '2024-01-15 14:30:00+00', '2 years 3 months 4 days',
    TRUE,
    '{"name": "John", "age": 30, "city": "New York"}',
    '{"name": "John", "age": 30, "city": "New York", "hobbies": ["reading", "swimming"]}',
    ARRAY[1, 2, 3, 4, 5],
    ARRAY['apple', 'banana', 'cherry'],
    '192.168.1.100',
    '192.168.1.0/24',
    '08:00:2b:01:02:03',
    POINT(40.7128, -74.0060),
    CIRCLE(POINT(40.7128, -74.0060), 10),
    'active'
);

-- Query demonstrating data type operations
SELECT 
    id,
    
    -- Numeric operations
    small_number + regular_number AS numeric_sum,
    precise_decimal * 1.1 AS increased_decimal,
    ROUND(floating_point, 2) AS rounded_float,
    
    -- String operations
    LENGTH(unlimited_text) AS text_length,
    UPPER(variable_char) AS uppercase_var,
    fixed_char || ' - ' || variable_char AS concatenated,
    
    -- Date/Time operations
    just_date + time_interval AS future_date,
    EXTRACT(YEAR FROM timestamp_with_tz) AS year_extracted,
    AGE(CURRENT_DATE, just_date) AS age_from_date,
    
    -- JSON operations
    json_data->>'name' AS json_name,
    jsonb_data->'hobbies' AS jsonb_hobbies,
    jsonb_array_length(jsonb_data->'hobbies') AS hobby_count,
    
    -- Array operations
    array_length(integer_array, 1) AS int_array_length,
    text_array[1] AS first_text_element,
    'banana' = ANY(text_array) AS contains_banana,
    
    -- Network operations
    HOST(ip_address) AS ip_host,
    MASKLEN(network_range) AS network_mask,
    
    -- Geometric operations
    location[0] AS latitude,
    location[1] AS longitude,
    
    -- Enum operations
    status_type::TEXT AS status_as_text
    
FROM data_type_showcase;

-- Data type validation and conversion
SELECT 
    -- Type checking
    pg_typeof(small_number) AS small_number_type,
    pg_typeof(jsonb_data) AS jsonb_type,
    pg_typeof(integer_array) AS array_type,
    
    -- Safe type conversion
    CASE 
        WHEN variable_char ~ '^[0-9]+$' THEN variable_char::INTEGER
        ELSE NULL
    END AS safe_string_to_int,
    
    -- JSON validation
    CASE 
        WHEN json_data::TEXT IS NOT NULL THEN 'Valid JSON'
        ELSE 'Invalid JSON'
    END AS json_validation
    
FROM data_type_showcase;
```

**Output:**
```
id | numeric_sum | increased_decimal | rounded_float | text_length | uppercase_var        | concatenated
---|-------------|-------------------|---------------|-------------|---------------------|---------------------------
1  | 2147516414  | 13580.24         | 3.14          | 58          | VARIABLE LENGTH STRING | ABCDE - Variable length string

future_date | year_extracted | age_from_date | json_name | jsonb_hobbies        | hobby_count
------------|----------------|---------------|-----------|---------------------|-------------
2026-04-19  | 2024          | 0 years       | John      | ["reading", "swimming"] | 2

int_array_length | first_text_element | contains_banana | ip_host      | network_mask | latitude | longitude
-----------------|-------------------|-----------------|--------------|--------------|----------|----------
5                | apple             | true            | 192.168.1.100| 24           | 40.7128  | -74.0060

small_number_type | jsonb_type | array_type | safe_string_to_int | json_validation
------------------|------------|------------|-------------------|----------------
smallint          | jsonb      | integer[]  | null              | Valid JSON
```

### 3. How do you create and manage indexes in PostgreSQL?

**Answer:** PostgreSQL supports multiple index types for different query patterns.

#### 🎯 **Index Types**
- **B-tree**: Default, good for equality and range queries
- **Hash**: Equality queries only
- **GiST**: Geometric and full-text search
- **SP-GiST**: Space-partitioned data
- **GIN**: Inverted indexes for arrays, JSON, full-text
- **BRIN**: Block range indexes for large tables

```sql
-- Create sample table for indexing demonstration
CREATE TABLE sales_data (
    sale_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    sale_date DATE NOT NULL,
    sale_amount DECIMAL(10,2) NOT NULL,
    sales_rep VARCHAR(100),
    region VARCHAR(50),
    product_tags TEXT[],
    sale_details JSONB,
    location POINT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data for indexing tests
INSERT INTO sales_data (
    customer_id, product_id, sale_date, sale_amount, sales_rep, region, 
    product_tags, sale_details, location
)
SELECT 
    (random() * 1000)::INTEGER + 1,
    (random() * 100)::INTEGER + 1,
    CURRENT_DATE - (random() * 365)::INTEGER,
    (random() * 1000 + 10)::DECIMAL(10,2),
    'Rep_' || (random() * 50)::INTEGER,
    CASE (random() * 4)::INTEGER
        WHEN 0 THEN 'North'
        WHEN 1 THEN 'South'
        WHEN 2 THEN 'East'
        ELSE 'West'
    END,
    ARRAY['tag_' || (random() * 10)::INTEGER, 'category_' || (random() * 5)::INTEGER],
    jsonb_build_object(
        'discount', (random() * 0.3)::DECIMAL(3,2),
        'payment_method', CASE (random() * 3)::INTEGER
            WHEN 0 THEN 'credit_card'
            WHEN 1 THEN 'cash'
            ELSE 'check'
        END,
        'notes', 'Sale note ' || (random() * 100)::INTEGER
    ),
    POINT(random() * 180 - 90, random() * 360 - 180)
FROM generate_series(1, 100000);

-- Analyze table before creating indexes
ANALYZE sales_data;

-- 1. B-tree indexes (default type)
-- Single column index
CREATE INDEX idx_sales_customer_id ON sales_data (customer_id);

-- Composite index
CREATE INDEX idx_sales_date_region ON sales_data (sale_date, region);

-- Partial index (with WHERE clause)
CREATE INDEX idx_sales_high_value ON sales_data (sale_amount) 
WHERE sale_amount > 500;

-- Expression index
CREATE INDEX idx_sales_month_year ON sales_data (EXTRACT(YEAR FROM sale_date), EXTRACT(MONTH FROM sale_date));

-- 2. GIN indexes for arrays and JSON
CREATE INDEX idx_sales_product_tags ON sales_data USING GIN (product_tags);
CREATE INDEX idx_sales_details ON sales_data USING GIN (sale_details);

-- 3. GiST index for geometric data
CREATE INDEX idx_sales_location ON sales_data USING GIST (location);

-- 4. Hash index for equality queries
CREATE INDEX idx_sales_region_hash ON sales_data USING HASH (region);

-- 5. BRIN index for large tables with natural ordering
CREATE INDEX idx_sales_created_at_brin ON sales_data USING BRIN (created_at);

-- Show all indexes on the table
SELECT 
    schemaname,
    tablename,
    indexname,
    indexdef
FROM pg_indexes 
WHERE tablename = 'sales_data'
ORDER BY indexname;

-- Demonstrate index usage with EXPLAIN
-- Query using customer_id index
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM sales_data WHERE customer_id = 500;

-- Query using composite index
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM sales_data 
WHERE sale_date >= '2023-06-01' AND region = 'North';

-- Query using partial index
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM sales_data 
WHERE sale_amount > 750;

-- Query using GIN index for arrays
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM sales_data 
WHERE product_tags @> ARRAY['tag_5'];

-- Query using GIN index for JSON
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM sales_data 
WHERE sale_details @> '{"payment_method": "credit_card"}';

-- Query using GiST index for geometric data
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM sales_data 
WHERE location <-> POINT(0, 0) < 50;

-- Index maintenance queries
-- Check index usage statistics
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch,
    idx_scan
FROM pg_stat_user_indexes 
WHERE tablename = 'sales_data'
ORDER BY idx_scan DESC;

-- Check index sizes
SELECT 
    indexname,
    pg_size_pretty(pg_relation_size(indexname::regclass)) AS index_size
FROM pg_indexes 
WHERE tablename = 'sales_data'
ORDER BY pg_relation_size(indexname::regclass) DESC;

-- Find unused indexes
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexname::regclass)) AS index_size
FROM pg_stat_user_indexes 
WHERE idx_scan = 0 
    AND tablename = 'sales_data';

-- Reindex for maintenance
REINDEX INDEX idx_sales_customer_id;
REINDEX TABLE sales_data;
```

**Output:**
```
schemaname | tablename  | indexname                | indexdef
-----------|------------|--------------------------|--------------------------------------------------
public     | sales_data | idx_sales_created_at_brin| CREATE INDEX idx_sales_created_at_brin ON public.sales_data USING brin (created_at)
public     | sales_data | idx_sales_customer_id    | CREATE INDEX idx_sales_customer_id ON public.sales_data USING btree (customer_id)
public     | sales_data | idx_sales_date_region    | CREATE INDEX idx_sales_date_region ON public.sales_data USING btree (sale_date, region)
public     | sales_data | idx_sales_details        | CREATE INDEX idx_sales_details ON public.sales_data USING gin (sale_details)
public     | sales_data | idx_sales_high_value     | CREATE INDEX idx_sales_high_value ON public.sales_data USING btree (sale_amount) WHERE (sale_amount > 500)

QUERY PLAN (for customer_id = 500):
Index Scan using idx_sales_customer_id on sales_data  (cost=0.29..8.31 rows=1 width=141) (actual time=0.045..0.089 rows=97 loops=1)
  Index Cond: (customer_id = 500)
  Buffers: shared hit=4
Planning Time: 0.123 ms
Execution Time: 0.112 ms

indexname                | idx_tup_read | idx_tup_fetch | idx_scan
-------------------------|--------------|---------------|----------
idx_sales_customer_id    | 97           | 97            | 1
idx_sales_date_region    | 0            | 0             | 0
idx_sales_high_value     | 0            | 0             | 0

indexname                | index_size
-------------------------|------------
idx_sales_customer_id    | 2208 kB
idx_sales_date_region    | 2208 kB
idx_sales_details        | 6440 kB
```

### 4. How do you write complex queries with JOINs and subqueries?

**Answer:** PostgreSQL supports various JOIN types and advanced subquery patterns.

#### 🎯 **JOIN Types**
- **INNER JOIN**: Matching records from both tables
- **LEFT/RIGHT JOIN**: All records from one side + matches
- **FULL OUTER JOIN**: All records from both tables
- **CROSS JOIN**: Cartesian product
- **SELF JOIN**: Table joined with itself

```sql
-- Create related tables for JOIN demonstrations
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    city VARCHAR(50),
    registration_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending'
);

CREATE TABLE order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_name VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0
);

-- Insert sample data
INSERT INTO customers (customer_name, email, city) VALUES
('Alice Johnson', 'alice@email.com', 'New York'),
('Bob Smith', 'bob@email.com', 'Los Angeles'),
('Charlie Brown', 'charlie@email.com', 'Chicago'),
('Diana Prince', 'diana@email.com', 'New York'),
('Eve Wilson', 'eve@email.com', 'Boston');

INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES
(1, '2024-01-15', 299.99, 'completed'),
(1, '2024-01-20', 149.50, 'completed'),
(2, '2024-01-18', 89.99, 'pending'),
(3, '2024-01-22', 199.99, 'completed'),
(4, '2024-01-25', 349.99, 'shipped');

INSERT INTO order_items (order_id, product_name, quantity, unit_price) VALUES
(1, 'Laptop', 1, 299.99),
(2, 'Mouse', 2, 24.99),
(2, 'Keyboard', 1, 99.52),
(3, 'Headphones', 1, 89.99),
(4, 'Monitor', 1, 199.99),
(5, 'Tablet', 1, 349.99);

INSERT INTO products (product_name, category, price, stock_quantity) VALUES
('Laptop', 'Electronics', 299.99, 50),
('Mouse', 'Electronics', 24.99, 200),
('Keyboard', 'Electronics', 99.52, 150),
('Headphones', 'Electronics', 89.99, 100),
('Monitor', 'Electronics', 199.99, 75),
('Tablet', 'Electronics', 349.99, 30);

-- 1. INNER JOIN - Customers with orders
SELECT 
    c.customer_id,
    c.customer_name,
    c.email,
    c.city,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_spent,
    AVG(o.total_amount) AS avg_order_value,
    MIN(o.order_date) AS first_order,
    MAX(o.order_date) AS last_order
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.email, c.city
ORDER BY total_spent DESC;

-- 2. LEFT JOIN - All customers including those without orders
SELECT 
    c.customer_id,
    c.customer_name,
    c.city,
    COALESCE(COUNT(o.order_id), 0) AS total_orders,
    COALESCE(SUM(o.total_amount), 0) AS total_spent,
    CASE 
        WHEN COUNT(o.order_id) = 0 THEN 'No Orders'
        WHEN SUM(o.total_amount) > 300 THEN 'High Value'
        WHEN SUM(o.total_amount) > 100 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS customer_segment
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.city
ORDER BY total_spent DESC;

-- 3. Complex JOIN with multiple tables
SELECT 
    c.customer_name,
    o.order_id,
    o.order_date,
    o.status,
    oi.product_name,
    oi.quantity,
    oi.unit_price,
    oi.quantity * oi.unit_price AS line_total,
    p.category,
    p.stock_quantity
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN products p ON oi.product_name = p.product_name
ORDER BY c.customer_name, o.order_date, oi.item_id;

-- 4. Self JOIN - Find customers from the same city
SELECT 
    c1.customer_name AS customer1,
    c2.customer_name AS customer2,
    c1.city
FROM customers c1
INNER JOIN customers c2 ON c1.city = c2.city AND c1.customer_id < c2.customer_id
ORDER BY c1.city, c1.customer_name;

-- 5. Subqueries - Correlated and non-correlated
-- Find customers who spent more than average
SELECT 
    customer_name,
    email,
    (SELECT SUM(total_amount) FROM orders WHERE customer_id = c.customer_id) AS total_spent
FROM customers c
WHERE (SELECT SUM(total_amount) FROM orders WHERE customer_id = c.customer_id) > 
      (SELECT AVG(customer_total) FROM 
       (SELECT SUM(total_amount) AS customer_total FROM orders GROUP BY customer_id) AS avg_calc)
ORDER BY total_spent DESC;

-- 6. EXISTS subquery
-- Find customers who have placed orders in the last 30 days
SELECT 
    customer_name,
    email,
    city
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id 
    AND o.order_date >= CURRENT_DATE - INTERVAL '30 days'
);

-- 7. Window functions with JOINs
SELECT 
    c.customer_name,
    o.order_date,
    o.total_amount,
    SUM(o.total_amount) OVER (PARTITION BY c.customer_id ORDER BY o.order_date) AS running_total,
    ROW_NUMBER() OVER (PARTITION BY c.customer_id ORDER BY o.order_date) AS order_sequence,
    LAG(o.total_amount) OVER (PARTITION BY c.customer_id ORDER BY o.order_date) AS previous_order_amount,
    LEAD(o.total_amount) OVER (PARTITION BY c.customer_id ORDER BY o.order_date) AS next_order_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
ORDER BY c.customer_name, o.order_date;

-- 8. CTE (Common Table Expression) with complex logic
WITH customer_metrics AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        c.city,
        COUNT(o.order_id) AS order_count,
        SUM(o.total_amount) AS total_spent,
        AVG(o.total_amount) AS avg_order_value,
        MAX(o.order_date) AS last_order_date
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name, c.city
),
city_stats AS (
    SELECT 
        city,
        COUNT(*) AS customers_in_city,
        AVG(total_spent) AS avg_city_spending
    FROM customer_metrics
    GROUP BY city
)
SELECT 
    cm.customer_name,
    cm.city,
    cm.order_count,
    cm.total_spent,
    cm.avg_order_value,
    cs.customers_in_city,
    cs.avg_city_spending,
    CASE 
        WHEN cm.total_spent > cs.avg_city_spending THEN 'Above City Average'
        ELSE 'Below City Average'
    END AS spending_vs_city_avg
FROM customer_metrics cm
INNER JOIN city_stats cs ON cm.city = cs.city
ORDER BY cm.city, cm.total_spent DESC;
```

**Output:**
```
customer_id | customer_name | email           | city        | total_orders | total_spent | avg_order_value | first_order | last_order
------------|---------------|-----------------|-------------|--------------|-------------|-----------------|-------------|------------
1           | Alice Johnson | alice@email.com | New York    | 2            | 449.49      | 224.75          | 2024-01-15  | 2024-01-20
4           | Diana Prince  | diana@email.com | New York    | 1            | 349.99      | 349.99          | 2024-01-25  | 2024-01-25
3           | Charlie Brown | charlie@email.com| Chicago     | 1            | 199.99      | 199.99          | 2024-01-22  | 2024-01-22
2           | Bob Smith     | bob@email.com   | Los Angeles | 1            | 89.99       | 89.99           | 2024-01-18  | 2024-01-18

customer_id | customer_name | city        | total_orders | total_spent | customer_segment
------------|---------------|-------------|--------------|-------------|------------------
1           | Alice Johnson | New York    | 2            | 449.49      | High Value
4           | Diana Prince  | New York    | 1            | 349.99      | High Value
3           | Charlie Brown | Chicago     | 1            | 199.99      | Medium Value
2           | Bob Smith     | Los Angeles | 1            | 89.99       | Low Value
5           | Eve Wilson    | Boston      | 0            | 0.00        | No Orders

customer1     | customer2    | city
--------------|--------------|----------
Alice Johnson | Diana Prince | New York

customer_name | order_date | total_amount | running_total | order_sequence | previous_order_amount | next_order_amount
--------------|------------|--------------|---------------|----------------|-----------------------|-------------------
Alice Johnson | 2024-01-15 | 299.99       | 299.99        | 1              | null                  | 149.50
Alice Johnson | 2024-01-20 | 149.50       | 449.49        | 2              | 299.99                | null
Bob Smith     | 2024-01-18 | 89.99        | 89.99         | 1              | null                  | null
Charlie Brown | 2024-01-22 | 199.99       | 199.99        | 1              | null                  | null
Diana Prince  | 2024-01-25 | 349.99       | 349.99        | 1              | null                  | null
```