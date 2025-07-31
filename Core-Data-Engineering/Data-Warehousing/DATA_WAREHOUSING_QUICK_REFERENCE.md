# Data Warehousing Quick Reference

## Schema Design Patterns

### Star Schema
```sql
-- Fact table (center)
CREATE TABLE fact_sales (
    sale_id BIGINT PRIMARY KEY,
    date_key INT,
    customer_key INT,
    product_key INT,
    quantity INT,
    amount DECIMAL(12,2)
);

-- Dimension tables (points)
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    year INT,
    month INT,
    day INT
);
```

### Snowflake Schema
```sql
-- Normalized dimensions
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_name VARCHAR(100),
    category_key INT
);

CREATE TABLE dim_category (
    category_key INT PRIMARY KEY,
    category_name VARCHAR(50),
    department_key INT
);
```

## SCD Implementation

### Type 1 (Overwrite)
```sql
UPDATE dim_customer 
SET city = 'New York', updated_date = CURRENT_DATE
WHERE customer_id = 'C001';
```

### Type 2 (Historical)
```sql
-- Expire current record
UPDATE dim_customer 
SET end_date = CURRENT_DATE, is_current = FALSE
WHERE customer_id = 'C001' AND is_current = TRUE;

-- Insert new record
INSERT INTO dim_customer (customer_id, name, city, start_date, is_current)
VALUES ('C001', 'John Doe', 'New York', CURRENT_DATE, TRUE);
```

## Common Queries

### Time-based Analysis
```sql
SELECT 
    d.year,
    d.month,
    SUM(f.amount) as total_sales
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.year = 2024
GROUP BY d.year, d.month
ORDER BY d.month;
```

### Customer Analytics
```sql
SELECT 
    c.customer_name,
    COUNT(f.sale_id) as order_count,
    SUM(f.amount) as total_spent,
    AVG(f.amount) as avg_order_value
FROM fact_sales f
JOIN dim_customer c ON f.customer_key = c.customer_key
WHERE c.is_current = TRUE
GROUP BY c.customer_name
HAVING SUM(f.amount) > 1000;
```

## Performance Optimization

### Indexing
```sql
-- Clustered index on date
CREATE CLUSTERED INDEX idx_sales_date ON fact_sales(date_key);

-- Non-clustered indexes
CREATE INDEX idx_customer ON fact_sales(customer_key);
CREATE INDEX idx_product ON fact_sales(product_key);
```

### Partitioning
```sql
-- Range partitioning
CREATE TABLE fact_sales_partitioned (
    sale_id BIGINT,
    sale_date DATE,
    amount DECIMAL(12,2)
) PARTITION BY RANGE (sale_date);
```

## Data Loading

### Bulk Insert
```sql
-- PostgreSQL COPY
COPY fact_sales FROM '/data/sales.csv' 
WITH (FORMAT csv, HEADER true);

-- SQL Server BULK INSERT
BULK INSERT fact_sales
FROM '/data/sales.csv'
WITH (FIELDTERMINATOR = ',', ROWTERMINATOR = '\n');
```

### Incremental Load
```sql
-- Merge/Upsert pattern
MERGE fact_sales AS target
USING staging_sales AS source
ON target.sale_id = source.sale_id
WHEN MATCHED THEN
    UPDATE SET amount = source.amount
WHEN NOT MATCHED THEN
    INSERT VALUES (source.sale_id, source.date_key, source.amount);
```

## Snowflake Specific

### Virtual Warehouses
```sql
-- Create warehouse
CREATE WAREHOUSE analytics_wh 
WITH WAREHOUSE_SIZE = 'MEDIUM'
AUTO_SUSPEND = 300
AUTO_RESUME = TRUE;

-- Use warehouse
USE WAREHOUSE analytics_wh;
```

### Time Travel
```sql
-- Query historical data
SELECT * FROM fact_sales AT (TIMESTAMP => '2024-01-01 00:00:00');

-- Restore table
CREATE TABLE fact_sales_restored AS
SELECT * FROM fact_sales AT (TIMESTAMP => '2024-01-01 00:00:00');
```

### Clustering
```sql
-- Cluster table by date
ALTER TABLE fact_sales CLUSTER BY (sale_date);

-- Check clustering information
SELECT SYSTEM$CLUSTERING_INFORMATION('fact_sales');
```

## Redshift Specific

### Distribution Styles
```sql
-- EVEN distribution
CREATE TABLE fact_sales (
    sale_id BIGINT,
    amount DECIMAL(12,2)
) DISTSTYLE EVEN;

-- KEY distribution
CREATE TABLE fact_sales (
    sale_id BIGINT,
    customer_id INT,
    amount DECIMAL(12,2)
) DISTKEY(customer_id);
```

### Sort Keys
```sql
-- Compound sort key
CREATE TABLE fact_sales (
    sale_id BIGINT,
    sale_date DATE,
    customer_id INT
) COMPOUND SORTKEY(sale_date, customer_id);

-- Interleaved sort key
CREATE TABLE fact_sales (
    sale_id BIGINT,
    sale_date DATE,
    customer_id INT
) INTERLEAVED SORTKEY(sale_date, customer_id);
```

## Monitoring Queries

### Table Statistics
```sql
-- PostgreSQL
SELECT 
    schemaname,
    tablename,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes
FROM pg_stat_user_tables;

-- Snowflake
SELECT 
    table_name,
    row_count,
    bytes,
    last_altered
FROM information_schema.tables
WHERE table_schema = 'PUBLIC';
```

### Query Performance
```sql
-- Long running queries
SELECT 
    query_id,
    query_text,
    execution_time,
    rows_produced
FROM query_history
WHERE execution_time > 30000
ORDER BY execution_time DESC;
```