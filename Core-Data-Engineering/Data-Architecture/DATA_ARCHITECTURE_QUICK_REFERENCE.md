# Data Architecture Quick Reference

## Data Modeling Quick Commands

### Entity-Relationship Modeling
```sql
-- Basic table creation with relationships
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending'
);

-- Add foreign key constraint
ALTER TABLE orders 
ADD CONSTRAINT fk_orders_customer 
FOREIGN KEY (customer_id) REFERENCES customers(customer_id);

-- Add check constraint
ALTER TABLE orders 
ADD CONSTRAINT chk_positive_amount 
CHECK (total_amount > 0);
```

### Normalization Quick Reference
```sql
-- 1NF: Atomic values, unique column names
-- 2NF: 1NF + no partial dependencies
-- 3NF: 2NF + no transitive dependencies

-- Example: Normalize order items
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(8,2) NOT NULL
);
```

## Dimensional Modeling Quick Reference

### Star Schema Template
```sql
-- Fact Table (center of star)
CREATE TABLE fact_sales (
    sale_key BIGSERIAL PRIMARY KEY,
    date_key INTEGER NOT NULL,
    customer_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    store_key INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(8,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(8,2) DEFAULT 0
);

-- Dimension Table Template
CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    customer_segment VARCHAR(30)
);
```

### Date Dimension Quick Setup
```sql
-- Create comprehensive date dimension
CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL,
    day_of_month INTEGER,
    day_of_year INTEGER,
    day_of_week INTEGER,
    day_name VARCHAR(10),
    month_number INTEGER,
    month_name VARCHAR(10),
    quarter_number INTEGER,
    year_number INTEGER,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN
);

-- Populate date dimension (2020-2030)
INSERT INTO dim_date 
SELECT 
    TO_CHAR(date_series, 'YYYYMMDD')::INTEGER,
    date_series,
    EXTRACT(DAY FROM date_series),
    EXTRACT(DOY FROM date_series),
    EXTRACT(DOW FROM date_series),
    TO_CHAR(date_series, 'Day'),
    EXTRACT(MONTH FROM date_series),
    TO_CHAR(date_series, 'Month'),
    EXTRACT(QUARTER FROM date_series),
    EXTRACT(YEAR FROM date_series),
    EXTRACT(DOW FROM date_series) IN (0, 6),
    FALSE
FROM generate_series('2020-01-01'::DATE, '2030-12-31'::DATE, '1 day') AS date_series;
```

### Slowly Changing Dimensions (SCD)
```sql
-- SCD Type 1: Overwrite
UPDATE dim_customer 
SET city = 'New York', state = 'NY' 
WHERE customer_id = 'CUST001';

-- SCD Type 2: Add new record
CREATE TABLE dim_customer_scd2 (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(50),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    effective_date DATE NOT NULL,
    expiration_date DATE DEFAULT '9999-12-31',
    is_current BOOLEAN DEFAULT TRUE
);

-- SCD Type 2 Insert Process
INSERT INTO dim_customer_scd2 (customer_id, first_name, last_name, city, state, effective_date)
VALUES ('CUST001', 'John', 'Doe', 'New York', 'NY', CURRENT_DATE);

UPDATE dim_customer_scd2 
SET expiration_date = CURRENT_DATE - 1, is_current = FALSE
WHERE customer_id = 'CUST001' AND is_current = TRUE 
AND customer_key != (SELECT MAX(customer_key) FROM dim_customer_scd2 WHERE customer_id = 'CUST001');
```

## Data Vault 2.0 Quick Reference

### Core Components
```sql
-- Hub: Business Keys
CREATE TABLE hub_customer (
    customer_hk CHAR(32) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL
);

-- Satellite: Descriptive Data
CREATE TABLE sat_customer_details (
    customer_hk CHAR(32),
    load_date TIMESTAMP,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    hash_diff CHAR(32) NOT NULL,
    record_source VARCHAR(50) NOT NULL,
    PRIMARY KEY (customer_hk, load_date)
);

-- Link: Relationships
CREATE TABLE link_customer_order (
    customer_order_hk CHAR(32) PRIMARY KEY,
    customer_hk CHAR(32) NOT NULL,
    order_hk CHAR(32) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL
);
```

### Hash Key Generation
```python
import hashlib

def generate_hash_key(*args):
    """Generate Data Vault hash key"""
    concatenated = '||'.join(str(arg).upper().strip() for arg in args if arg)
    return hashlib.md5(concatenated.encode()).hexdigest().upper()

# Usage
customer_hk = generate_hash_key('CUST001')
link_hk = generate_hash_key('CUST001', 'ORD001')
```

## Performance Optimization Quick Reference

### Indexing Strategies
```sql
-- Single column index
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- Composite index (order matters)
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- Partial index
CREATE INDEX idx_orders_pending ON orders(order_date) WHERE status = 'pending';

-- Functional index
CREATE INDEX idx_orders_month ON orders(DATE_TRUNC('month', order_date));

-- Unique index
CREATE UNIQUE INDEX idx_customers_email ON customers(email);

-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes 
ORDER BY idx_scan DESC;
```

### Query Optimization
```sql
-- Use EXISTS instead of IN
SELECT * FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);

-- Use LIMIT for large result sets
SELECT * FROM orders ORDER BY order_date DESC LIMIT 100;

-- Use window functions for analytics
SELECT 
    customer_id,
    order_date,
    total_amount,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as order_number
FROM orders;

-- Use CTEs for complex queries
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        SUM(total_amount) as total_sales
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT * FROM monthly_sales WHERE total_sales > 10000;
```

### Partitioning
```sql
-- Range partitioning by date
CREATE TABLE orders_partitioned (
    order_id BIGSERIAL,
    customer_id INTEGER,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2)
) PARTITION BY RANGE (order_date);

-- Create partitions
CREATE TABLE orders_2024_q1 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE orders_2024_q2 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');
```

## Data Quality Quick Reference

### Basic Data Quality Checks
```sql
-- Completeness check
SELECT 
    COUNT(*) as total_records,
    COUNT(customer_id) as non_null_customer_id,
    COUNT(email) as non_null_email,
    (COUNT(email) * 100.0 / COUNT(*)) as email_completeness_pct
FROM customers;

-- Uniqueness check
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT email) as unique_emails,
    COUNT(*) - COUNT(DISTINCT email) as duplicate_count
FROM customers;

-- Range validation
SELECT 
    COUNT(*) as total_orders,
    COUNT(CASE WHEN total_amount < 0 THEN 1 END) as negative_amounts,
    COUNT(CASE WHEN total_amount > 100000 THEN 1 END) as excessive_amounts
FROM orders;

-- Pattern validation
SELECT 
    COUNT(*) as total_customers,
    COUNT(CASE WHEN email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN 1 END) as valid_emails
FROM customers;
```

### Data Profiling Queries
```sql
-- Column profiling
SELECT 
    'customer_id' as column_name,
    COUNT(*) as total_count,
    COUNT(DISTINCT customer_id) as distinct_count,
    COUNT(customer_id) as non_null_count,
    MIN(customer_id) as min_value,
    MAX(customer_id) as max_value
FROM customers
UNION ALL
SELECT 
    'total_amount',
    COUNT(*),
    COUNT(DISTINCT total_amount),
    COUNT(total_amount),
    MIN(total_amount)::TEXT,
    MAX(total_amount)::TEXT
FROM orders;

-- Distribution analysis
SELECT 
    CASE 
        WHEN total_amount < 100 THEN '0-99'
        WHEN total_amount < 500 THEN '100-499'
        WHEN total_amount < 1000 THEN '500-999'
        ELSE '1000+'
    END as amount_range,
    COUNT(*) as order_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM orders
GROUP BY 1
ORDER BY 1;
```

## Data Governance Quick Reference

### Data Catalog Schema
```sql
-- Data catalog tables
CREATE TABLE data_catalog (
    asset_id VARCHAR(100) PRIMARY KEY,
    asset_name VARCHAR(200) NOT NULL,
    asset_type VARCHAR(50) NOT NULL,
    description TEXT,
    owner VARCHAR(100),
    steward VARCHAR(100),
    classification VARCHAR(20),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE data_lineage (
    lineage_id SERIAL PRIMARY KEY,
    source_asset_id VARCHAR(100) REFERENCES data_catalog(asset_id),
    target_asset_id VARCHAR(100) REFERENCES data_catalog(asset_id),
    transformation_type VARCHAR(50),
    transformation_logic TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Data Classification
```sql
-- Add classification to existing tables
ALTER TABLE customers ADD COLUMN data_classification VARCHAR(20) DEFAULT 'internal';
ALTER TABLE customers ADD COLUMN contains_pii BOOLEAN DEFAULT FALSE;

-- Update classifications
UPDATE customers SET data_classification = 'confidential', contains_pii = TRUE;

-- Create view for sensitive data
CREATE VIEW customers_public AS
SELECT 
    customer_id,
    first_name,
    CASE WHEN contains_pii THEN 'REDACTED' ELSE last_name END as last_name,
    city,
    state
FROM customers
WHERE data_classification IN ('public', 'internal');
```

## Modern Data Stack Quick Reference

### dbt Model Template
```sql
-- models/staging/stg_customers.sql
{{ config(materialized='view') }}

SELECT 
    customer_id,
    TRIM(UPPER(first_name)) as first_name,
    TRIM(UPPER(last_name)) as last_name,
    LOWER(email) as email,
    created_at
FROM {{ source('raw', 'customers') }}
WHERE customer_id IS NOT NULL

-- models/marts/dim_customers.sql
{{ config(materialized='table') }}

SELECT 
    {{ dbt_utils.surrogate_key(['customer_id']) }} as customer_key,
    customer_id,
    first_name,
    last_name,
    email,
    created_at
FROM {{ ref('stg_customers') }}
```

### Great Expectations Data Tests
```python
# great_expectations/expectations/customer_data_suite.py
import great_expectations as ge

# Load data
df = ge.read_csv('customers.csv')

# Add expectations
df.expect_column_to_exist('customer_id')
df.expect_column_values_to_not_be_null('customer_id')
df.expect_column_values_to_be_unique('customer_id')
df.expect_column_values_to_match_regex('email', r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')

# Save expectation suite
df.save_expectation_suite('customer_data_suite.json')
```

### Airflow DAG Template
```python
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'customer_data_pipeline',
    default_args=default_args,
    description='Customer data processing pipeline',
    schedule_interval='@daily',
    catchup=False
)

def extract_data():
    # Extract logic here
    pass

def transform_data():
    # Transform logic here
    pass

def load_data():
    # Load logic here
    pass

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag
)

extract_task >> transform_task >> load_task
```

## Common SQL Patterns

### Analytical Queries
```sql
-- Running totals
SELECT 
    order_date,
    total_amount,
    SUM(total_amount) OVER (ORDER BY order_date) as running_total
FROM orders;

-- Ranking
SELECT 
    customer_id,
    total_amount,
    RANK() OVER (ORDER BY total_amount DESC) as amount_rank,
    DENSE_RANK() OVER (ORDER BY total_amount DESC) as dense_rank
FROM orders;

-- Percentiles
SELECT 
    customer_id,
    total_amount,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total_amount) as median_amount,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY total_amount) as p95_amount
FROM orders
GROUP BY customer_id;

-- Time series analysis
SELECT 
    DATE_TRUNC('month', order_date) as month,
    COUNT(*) as order_count,
    SUM(total_amount) as total_revenue,
    LAG(SUM(total_amount)) OVER (ORDER BY DATE_TRUNC('month', order_date)) as prev_month_revenue
FROM orders
GROUP BY DATE_TRUNC('month', order_date);
```

### Data Cleaning Patterns
```sql
-- Remove duplicates
WITH ranked_customers AS (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY email ORDER BY created_at DESC) as rn
    FROM customers
)
SELECT * FROM ranked_customers WHERE rn = 1;

-- Handle nulls
SELECT 
    customer_id,
    COALESCE(first_name, 'Unknown') as first_name,
    COALESCE(last_name, 'Unknown') as last_name,
    COALESCE(city, 'Not Specified') as city
FROM customers;

-- Standardize data
SELECT 
    customer_id,
    TRIM(UPPER(first_name)) as first_name,
    TRIM(UPPER(last_name)) as last_name,
    LOWER(TRIM(email)) as email
FROM customers;
```

This quick reference provides essential commands and patterns for common data architecture tasks. Keep it handy for rapid implementation and troubleshooting.