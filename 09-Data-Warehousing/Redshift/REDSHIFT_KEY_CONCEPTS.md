# Amazon Redshift Key Concepts

## 1. Redshift Architecture
**Components**:
- **Leader Node**: Coordinates query execution and client connections
- **Compute Nodes**: Store data and execute queries
- **Node Slices**: Parallel processing units within compute nodes

**Cluster Types**:
```sql
-- Dense Compute (DC2) - SSD storage
CREATE CLUSTER my-cluster
NODE TYPE dc2.large
NUMBER OF NODES 3;

-- Dense Storage (DS2) - HDD storage  
CREATE CLUSTER data-warehouse
NODE TYPE ds2.xlarge
NUMBER OF NODES 6;

-- RA3 - Managed storage with compute scaling
CREATE CLUSTER modern-dw
NODE TYPE ra3.xlarge
NUMBER OF NODES 2;
```

## 2. Data Distribution
```sql
-- Distribution styles
CREATE TABLE sales (
    sale_id INTEGER,
    customer_id INTEGER,
    product_id INTEGER,
    sale_date DATE,
    amount DECIMAL(10,2)
)
DISTSTYLE KEY
DISTKEY (customer_id);  -- Distribute by customer_id

-- EVEN distribution
CREATE TABLE products (
    product_id INTEGER,
    product_name VARCHAR(100),
    category VARCHAR(50)
)
DISTSTYLE EVEN;

-- ALL distribution (small tables)
CREATE TABLE categories (
    category_id INTEGER,
    category_name VARCHAR(50)
)
DISTSTYLE ALL;

-- Check distribution
SELECT 
    slice,
    COUNT(*) as row_count
FROM stv_blocklist 
WHERE tbl = (SELECT oid FROM pg_class WHERE relname = 'sales')
GROUP BY slice
ORDER BY slice;
```

## 3. Sort Keys and Compression
```sql
-- Compound sort key (multiple columns)
CREATE TABLE orders (
    order_id INTEGER,
    customer_id INTEGER,
    order_date DATE,
    status VARCHAR(20)
)
SORTKEY (order_date, customer_id);

-- Interleaved sort key (better for multiple query patterns)
CREATE TABLE events (
    event_id BIGINT,
    user_id INTEGER,
    event_date DATE,
    event_type VARCHAR(50)
)
INTERLEAVED SORTKEY (event_date, user_id, event_type);

-- Compression encoding
CREATE TABLE compressed_sales (
    sale_id INTEGER ENCODE DELTA,
    customer_id INTEGER ENCODE DELTA32K,
    product_name VARCHAR(100) ENCODE LZO,
    sale_date DATE ENCODE DELTA32K,
    amount DECIMAL(10,2) ENCODE DELTA32K
);

-- Analyze compression
ANALYZE COMPRESSION sales;
```

## 4. Data Loading
```sql
-- COPY from S3
COPY sales
FROM 's3://my-bucket/sales-data/'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftRole'
FORMAT AS CSV
DELIMITER ','
IGNOREHEADER 1
DATEFORMAT 'YYYY-MM-DD'
TIMEFORMAT 'YYYY-MM-DD HH:MI:SS'
REGION 'us-west-2';

-- COPY with manifest
COPY sales
FROM 's3://my-bucket/manifest.json'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftRole'
FORMAT AS CSV
MANIFEST;

-- COPY from multiple files
COPY sales
FROM 's3://my-bucket/sales-data/sales'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftRole'
FORMAT AS CSV
DELIMITER '|'
GZIP;

-- UPSERT pattern
BEGIN;

CREATE TEMP TABLE sales_staging (LIKE sales);

COPY sales_staging
FROM 's3://my-bucket/incremental-data/'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftRole'
FORMAT AS CSV;

DELETE FROM sales
USING sales_staging
WHERE sales.sale_id = sales_staging.sale_id;

INSERT INTO sales
SELECT * FROM sales_staging;

DROP TABLE sales_staging;

COMMIT;
```

## 5. Query Optimization
```sql
-- Use EXPLAIN to analyze query plans
EXPLAIN
SELECT 
    c.customer_name,
    SUM(s.amount) as total_sales
FROM customers c
JOIN sales s ON c.customer_id = s.customer_id
WHERE s.sale_date >= '2024-01-01'
GROUP BY c.customer_name
ORDER BY total_sales DESC;

-- Efficient joins with distribution keys
-- Good: Join on distribution key
SELECT *
FROM sales s
JOIN customers c ON s.customer_id = c.customer_id;

-- Avoid: Cross-joins and Cartesian products
-- Use WHERE clauses to filter early

-- Window functions for analytics
SELECT 
    customer_id,
    sale_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id 
        ORDER BY sale_date 
        ROWS UNBOUNDED PRECEDING
    ) as running_total,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id 
        ORDER BY amount DESC
    ) as sales_rank
FROM sales;

-- Use LIMIT for large result sets
SELECT *
FROM large_table
ORDER BY created_date DESC
LIMIT 1000;
```

## 6. Workload Management (WLM)
```sql
-- Create parameter group with WLM configuration
{
  "query_group": "etl",
  "query_slot_count": 3,
  "memory_percent_to_use": 40,
  "max_execution_time": 3600000
}

-- Set query group
SET query_group TO 'etl';

-- Monitor WLM queues
SELECT 
    query,
    queue,
    slot_count,
    total_queue_time,
    total_exec_time,
    service_class
FROM stl_wlm_query
WHERE userid > 1
ORDER BY total_queue_time DESC;

-- Short Query Acceleration (SQA)
-- Automatically routes short queries to dedicated queue

-- Concurrency Scaling
-- Automatically adds capacity during peak usage
```

## 7. Maintenance Operations
```sql
-- VACUUM to reclaim space and sort data
VACUUM FULL sales;
VACUUM DELETE ONLY sales;  -- Only reclaim deleted space
VACUUM SORT ONLY sales;    -- Only sort data

-- ANALYZE to update table statistics
ANALYZE sales;
ANALYZE;  -- All tables

-- Check table statistics
SELECT 
    schemaname,
    tablename,
    n_tup_ins,
    n_tup_upd,
    n_tup_del,
    last_vacuum,
    last_analyze
FROM svv_table_info
WHERE schemaname = 'public'
ORDER BY n_tup_ins DESC;

-- Deep copy for major restructuring
CREATE TABLE sales_new (LIKE sales);
INSERT INTO sales_new SELECT * FROM sales;
DROP TABLE sales;
ALTER TABLE sales_new RENAME TO sales;

-- Automatic table optimization
ALTER TABLE sales SET TABLE PROPERTIES ('auto_mv' = 'true');
```

## 8. Security and Access Control
```sql
-- Create users and groups
CREATE USER analyst PASSWORD 'SecurePassword123!';
CREATE GROUP analysts;
ALTER GROUP analysts ADD USER analyst;

-- Grant permissions
GRANT SELECT ON TABLE sales TO GROUP analysts;
GRANT ALL ON SCHEMA analytics TO GROUP analysts;

-- Row-level security
CREATE OR REPLACE VIEW sales_filtered AS
SELECT *
FROM sales
WHERE region = (
    SELECT region 
    FROM user_regions 
    WHERE username = current_user
);

GRANT SELECT ON sales_filtered TO GROUP regional_analysts;

-- Column-level security
GRANT SELECT (customer_id, amount, sale_date) ON sales TO analyst;

-- Encryption
-- Cluster encryption (at rest)
CREATE CLUSTER encrypted-cluster
ENCRYPTED
KMS KEY ID 'arn:aws:kms:us-west-2:123456789012:key/12345678-1234-1234-1234-123456789012';

-- SSL/TLS (in transit)
-- Configure in connection string: sslmode=require
```

## 9. Monitoring and Performance
```sql
-- Query performance monitoring
SELECT 
    query,
    userid,
    starttime,
    endtime,
    DATEDIFF(seconds, starttime, endtime) as duration,
    aborted
FROM stl_query
WHERE starttime >= DATEADD(hour, -1, GETDATE())
ORDER BY duration DESC;

-- Table scan information
SELECT 
    schemaname,
    tablename,
    size,
    tbl_rows,
    skew_sortkey1,
    skew_rows
FROM svv_table_info
WHERE schemaname = 'public'
ORDER BY size DESC;

-- Disk usage
SELECT 
    schemaname,
    tablename,
    size_in_mb,
    pct_used
FROM (
    SELECT 
        schemaname,
        tablename,
        (size/1024/1024) as size_in_mb,
        CASE 
            WHEN tbl_rows = 0 THEN 0
            ELSE ((size/1024/1024)/tbl_rows)
        END as pct_used
    FROM svv_table_info
) t
ORDER BY size_in_mb DESC;

-- Connection monitoring
SELECT 
    process,
    user_name,
    db_name,
    start_time,
    status
FROM stv_sessions
WHERE user_name != 'rdsdb';
```

## 10. Advanced Features
```sql
-- Materialized Views
CREATE MATERIALIZED VIEW sales_summary AS
SELECT 
    DATE_TRUNC('month', sale_date) as month,
    customer_id,
    SUM(amount) as total_sales,
    COUNT(*) as transaction_count
FROM sales
GROUP BY DATE_TRUNC('month', sale_date), customer_id;

REFRESH MATERIALIZED VIEW sales_summary;

-- External Tables (Spectrum)
CREATE EXTERNAL SCHEMA spectrum_schema
FROM DATA CATALOG
DATABASE 'spectrum_db'
IAM_ROLE 'arn:aws:iam::123456789012:role/SpectrumRole';

CREATE EXTERNAL TABLE spectrum_schema.external_sales (
    sale_id INTEGER,
    customer_id INTEGER,
    amount DECIMAL(10,2),
    sale_date DATE
)
STORED AS PARQUET
LOCATION 's3://data-lake/sales/';

-- Query external data
SELECT 
    local.customer_name,
    SUM(external.amount) as total_sales
FROM customers local
JOIN spectrum_schema.external_sales external
    ON local.customer_id = external.customer_id
GROUP BY local.customer_name;

-- Stored Procedures
CREATE OR REPLACE PROCEDURE update_sales_summary()
AS $$
BEGIN
    DELETE FROM sales_summary WHERE month = DATE_TRUNC('month', CURRENT_DATE);
    
    INSERT INTO sales_summary
    SELECT 
        DATE_TRUNC('month', sale_date) as month,
        customer_id,
        SUM(amount) as total_sales,
        COUNT(*) as transaction_count
    FROM sales
    WHERE DATE_TRUNC('month', sale_date) = DATE_TRUNC('month', CURRENT_DATE)
    GROUP BY DATE_TRUNC('month', sale_date), customer_id;
END;
$$ LANGUAGE plpgsql;

CALL update_sales_summary();
```