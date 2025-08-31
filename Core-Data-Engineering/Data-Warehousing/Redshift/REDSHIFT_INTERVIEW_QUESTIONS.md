# Amazon Redshift Interview Questions

## Table of Contents

1. [Basic Redshift Concepts](#basic-redshift-concepts)
2. [Architecture and Performance](#architecture-and-performance)
3. [Data Loading and ETL](#data-loading-and-etl)
4. [Query Optimization](#query-optimization)
5. [Security and Administration](#security-and-administration)
6. [Data Engineering Use Cases](#data-engineering-use-cases)

---

## Basic Redshift Concepts

### Q1: What is Amazon Redshift and how does it differ from traditional databases?

**Answer:**
Amazon Redshift is a fully managed, petabyte-scale data warehouse service designed for analytical workloads. It uses columnar storage, massively parallel processing (MPP), and compression to deliver fast query performance.

**Key Differences:**
- **Columnar Storage**: Optimized for analytical queries vs row-based OLTP
- **MPP Architecture**: Distributes queries across multiple nodes
- **Compression**: Automatic compression reduces storage and I/O
- **Managed Service**: AWS handles infrastructure, backups, and maintenance
- **Scalability**: Elastic scaling from gigabytes to petabytes

**Code Example:**
```sql
-- Create Redshift cluster and database objects
CREATE SCHEMA analytics;

-- Fact table with distribution and sort keys
CREATE TABLE analytics.fact_sales (
    sale_id BIGINT IDENTITY(1,1),
    product_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    store_id INTEGER NOT NULL,
    sale_date DATE NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT GETDATE()
)
DISTSTYLE KEY
DISTKEY (customer_id)
SORTKEY (sale_date, store_id);

-- Dimension table with ALL distribution
CREATE TABLE analytics.dim_products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    brand VARCHAR(100),
    unit_cost DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT GETDATE()
)
DISTSTYLE ALL;

-- Load sample data
INSERT INTO analytics.dim_products VALUES
(1, 'Laptop Pro 15"', 'Electronics', 'TechBrand', 800.00),
(2, 'Wireless Mouse', 'Electronics', 'TechBrand', 15.00),
(3, 'Office Chair', 'Furniture', 'ComfortCorp', 150.00);

-- Analytical query leveraging columnar storage
SELECT 
    p.category,
    DATE_TRUNC('month', s.sale_date) as month,
    SUM(s.total_amount) as monthly_revenue,
    COUNT(DISTINCT s.customer_id) as unique_customers,
    AVG(s.total_amount) as avg_order_value
FROM analytics.fact_sales s
JOIN analytics.dim_products p ON s.product_id = p.product_id
WHERE s.sale_date >= '2023-01-01'
GROUP BY p.category, DATE_TRUNC('month', s.sale_date)
ORDER BY category, month;
```

### Q2: Explain Redshift's architecture and node types.

**Answer:**
Redshift uses a leader-compute node architecture where the leader node coordinates query execution and compute nodes perform the actual data processing in parallel.

**Architecture Components:**
- **Leader Node**: Query planning, coordination, and client communication
- **Compute Nodes**: Data storage and query execution
- **Node Slices**: Parallel processing units within compute nodes
- **Cluster**: Collection of nodes working together

**Node Types:**
- **dc2.large**: Dense compute, SSD storage
- **dc2.8xlarge**: Dense compute, high performance
- **ds2.xlarge**: Dense storage, HDD-based
- **ra3.xlarge/4xlarge/16xlarge**: Managed storage, compute-storage separation

**Code Example:**
```sql
-- Query system tables to understand cluster architecture
SELECT 
    node,
    slice,
    tbl,
    rows,
    size,
    size_mb
FROM stv_tbl_perm 
WHERE schemaname = 'analytics'
ORDER BY node, slice, tbl;

-- Check cluster configuration
SELECT 
    node_type,
    node_count,
    cluster_version,
    cluster_status
FROM stv_cluster_info;

-- Monitor node performance
SELECT 
    node,
    slice,
    cpu_user,
    cpu_system,
    cpu_idle,
    bytes_read,
    bytes_written
FROM stv_slices
ORDER BY node, slice;

-- Distribution analysis
SELECT 
    schemaname,
    tablename,
    diststyle,
    distkey,
    sortkey1,
    size_mb,
    pct_used
FROM svv_table_info 
WHERE schemaname = 'analytics'
ORDER BY size_mb DESC;
```

### Q3: How do distribution styles and sort keys affect performance?

**Answer:**
Distribution styles determine how data is distributed across nodes, while sort keys determine physical data ordering. Proper selection minimizes data movement and enables zone maps for query pruning.

**Distribution Styles:**
- **KEY**: Distribute based on column values
- **ALL**: Copy entire table to all nodes
- **EVEN**: Round-robin distribution
- **AUTO**: Redshift chooses optimal distribution

**Code Example:**
```sql
-- Analyze distribution for optimization
SELECT 
    schemaname,
    tablename,
    diststyle,
    distkey,
    size_mb,
    skew_rows,
    skew_sortkey1
FROM svv_table_info 
WHERE schemaname = 'analytics';

-- Check data distribution skew
SELECT 
    slice,
    COUNT(*) as row_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() as pct_of_total
FROM analytics.fact_sales
GROUP BY slice
ORDER BY slice;

-- Optimal distribution key selection example
CREATE TABLE analytics.fact_orders_optimized (
    order_id BIGINT,
    customer_id INTEGER,
    product_id INTEGER,
    order_date DATE,
    quantity INTEGER,
    amount DECIMAL(10,2)
)
-- Choose distribution key based on join patterns
DISTSTYLE KEY
DISTKEY (customer_id)  -- Most frequent join column
-- Choose sort keys based on query patterns
SORTKEY (order_date, customer_id);  -- Filter and group by patterns

-- Compare query performance with different distributions
EXPLAIN (VERBOSE TRUE, COSTS TRUE)
SELECT 
    c.customer_name,
    SUM(o.amount) as total_spent
FROM analytics.fact_orders_optimized o
JOIN analytics.dim_customers c ON o.customer_id = c.customer_id
WHERE o.order_date >= '2023-01-01'
GROUP BY c.customer_name;

-- Sort key effectiveness analysis
SELECT 
    schemaname,
    tablename,
    sortkey1,
    sortkey1_enc,
    sortkey_num,
    size_mb,
    pct_used
FROM svv_table_info 
WHERE schemaname = 'analytics'
AND sortkey1 IS NOT NULL;
```

## Architecture and Performance

### Q4: How do you optimize Redshift performance for analytical workloads?

**Answer:**
Redshift performance optimization involves proper table design, query optimization, workload management, and monitoring. Key strategies include distribution keys, sort keys, compression, and query patterns.

**Code Example:**
```sql
-- Performance optimization strategies

-- 1. Table design optimization
CREATE TABLE analytics.fact_sales_optimized (
    sale_id BIGINT IDENTITY(1,1),
    customer_id INTEGER NOT NULL ENCODE DELTA,
    product_id INTEGER NOT NULL ENCODE DELTA32K,
    store_id INTEGER NOT NULL ENCODE DELTA32K,
    sale_date DATE NOT NULL ENCODE DELTA32K,
    quantity INTEGER NOT NULL ENCODE DELTA32K,
    unit_price DECIMAL(10,2) NOT NULL ENCODE DELTA32K,
    total_amount DECIMAL(12,2) NOT NULL ENCODE DELTA32K,
    created_at TIMESTAMP DEFAULT GETDATE() ENCODE DELTA32K
)
DISTSTYLE KEY
DISTKEY (customer_id)
COMPOUND SORTKEY (sale_date, store_id, customer_id);

-- 2. Compression analysis and optimization
SELECT 
    schemaname,
    tablename,
    column_name,
    type,
    encoding,
    distkey,
    sortkey
FROM pg_table_def 
WHERE schemaname = 'analytics'
ORDER BY tablename, ordinal_position;

-- Run compression analysis
ANALYZE COMPRESSION analytics.fact_sales;

-- 3. Query performance monitoring
SELECT 
    query,
    userid,
    starttime,
    endtime,
    DATEDIFF(seconds, starttime, endtime) as duration_seconds,
    aborted,
    insert_pristine,
    concurrency_scaling_status
FROM stl_query 
WHERE starttime >= DATEADD(hour, -1, GETDATE())
AND duration_seconds > 10
ORDER BY duration_seconds DESC;

-- 4. Workload Management (WLM) configuration
-- Check current WLM configuration
SELECT * FROM stv_wlm_service_class_config;

-- Monitor WLM queue performance
SELECT 
    service_class,
    num_query_tasks,
    num_executing_queries,
    num_executed_queries,
    num_queued_queries,
    total_queue_time,
    avg_queue_time
FROM stv_wlm_service_class_state;

-- 5. Vacuum and analyze operations
-- Check table statistics freshness
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    most_common_vals,
    histogram_bounds,
    last_analyze
FROM pg_stats 
WHERE schemaname = 'analytics';

-- Vacuum operations for maintenance
VACUUM REINDEX analytics.fact_sales;
ANALYZE analytics.fact_sales;

-- 6. Query optimization techniques
-- Use EXPLAIN to analyze query plans
EXPLAIN (VERBOSE TRUE, COSTS TRUE)
SELECT 
    p.category,
    s.store_name,
    DATE_TRUNC('month', f.sale_date) as month,
    SUM(f.total_amount) as revenue,
    COUNT(*) as transaction_count
FROM analytics.fact_sales f
JOIN analytics.dim_products p ON f.product_id = p.product_id
JOIN analytics.dim_stores s ON f.store_id = s.store_id
WHERE f.sale_date BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY p.category, s.store_name, DATE_TRUNC('month', f.sale_date)
ORDER BY revenue DESC;
```

### Q5: How do you implement and manage Redshift Spectrum for external data?

**Answer:**
Redshift Spectrum allows querying data in S3 without loading it into Redshift. It extends the cluster with virtually unlimited storage and enables data lake analytics.

**Code Example:**
```sql
-- 1. Create external schema for Spectrum
CREATE EXTERNAL SCHEMA spectrum_schema
FROM DATA CATALOG
DATABASE 'data_lake_db'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftSpectrumRole'
CREATE EXTERNAL DATABASE IF NOT EXISTS;

-- 2. Create external table for S3 data
CREATE EXTERNAL TABLE spectrum_schema.external_logs (
    timestamp TIMESTAMP,
    user_id INTEGER,
    session_id VARCHAR(50),
    event_type VARCHAR(50),
    page_url VARCHAR(500),
    user_agent VARCHAR(500),
    ip_address VARCHAR(15)
)
STORED AS PARQUET
LOCATION 's3://company-data-lake/logs/year=2023/'
TABLE PROPERTIES ('has_encrypted_data'='false');

-- 3. Partitioned external table for better performance
CREATE EXTERNAL TABLE spectrum_schema.external_sales_partitioned (
    sale_id BIGINT,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    amount DECIMAL(10,2),
    sale_timestamp TIMESTAMP
)
PARTITIONED BY (
    year INTEGER,
    month INTEGER,
    day INTEGER
)
STORED AS PARQUET
LOCATION 's3://company-data-lake/sales/'
TABLE PROPERTIES ('has_encrypted_data'='false');

-- Add partitions
ALTER TABLE spectrum_schema.external_sales_partitioned 
ADD PARTITION (year=2023, month=1, day=1) 
LOCATION 's3://company-data-lake/sales/year=2023/month=01/day=01/';

ALTER TABLE spectrum_schema.external_sales_partitioned 
ADD PARTITION (year=2023, month=1, day=2) 
LOCATION 's3://company-data-lake/sales/year=2023/month=01/day=02/';

-- 4. Query combining Redshift and Spectrum data
SELECT 
    c.customer_name,
    c.customer_segment,
    ext.total_external_sales,
    int.total_internal_sales,
    (ext.total_external_sales + int.total_internal_sales) as total_sales
FROM analytics.dim_customers c
LEFT JOIN (
    -- External data from S3 via Spectrum
    SELECT 
        customer_id,
        SUM(amount) as total_external_sales
    FROM spectrum_schema.external_sales_partitioned
    WHERE year = 2023 AND month = 1
    GROUP BY customer_id
) ext ON c.customer_id = ext.customer_id
LEFT JOIN (
    -- Internal Redshift data
    SELECT 
        customer_id,
        SUM(total_amount) as total_internal_sales
    FROM analytics.fact_sales
    WHERE sale_date >= '2023-01-01' AND sale_date < '2023-02-01'
    GROUP BY customer_id
) int ON c.customer_id = int.customer_id;

-- 5. Monitor Spectrum query performance
SELECT 
    query,
    segment,
    step,
    max_time,
    avg_time,
    rows,
    bytes,
    rate_row,
    rate_byte
FROM svl_s3query_summary 
WHERE query IN (
    SELECT query FROM stl_query 
    WHERE querytxt LIKE '%spectrum_schema%'
    AND starttime >= DATEADD(hour, -1, GETDATE())
)
ORDER BY query, segment, step;

-- 6. Optimize Spectrum queries
-- Use columnar formats (Parquet, ORC)
-- Partition data appropriately
-- Use compression
-- Predicate pushdown optimization

-- Example of predicate pushdown
SELECT 
    event_type,
    COUNT(*) as event_count,
    COUNT(DISTINCT user_id) as unique_users
FROM spectrum_schema.external_logs
WHERE timestamp >= '2023-01-01 00:00:00'
  AND timestamp < '2023-01-02 00:00:00'  -- Partition pruning
  AND event_type IN ('login', 'purchase')  -- Predicate pushdown
GROUP BY event_type;
```

## Data Loading and ETL

### Q6: How do you implement efficient data loading strategies in Redshift?

**Answer:**
Efficient data loading in Redshift involves using COPY command, proper file formats, compression, and parallel loading. Different strategies suit different use cases and data volumes.

**Code Example:**
```sql
-- 1. Basic COPY command from S3
COPY analytics.fact_sales 
FROM 's3://company-data/sales/2023/01/'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftLoadRole'
FORMAT AS CSV
DELIMITER ','
IGNOREHEADER 1
DATEFORMAT 'YYYY-MM-DD'
TIMEFORMAT 'YYYY-MM-DD HH:MI:SS'
COMPUPDATE ON
STATUPDATE ON;

-- 2. Optimized COPY with multiple files for parallel loading
COPY analytics.fact_sales_large
FROM 's3://company-data/sales/2023/01/manifest.json'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftLoadRole'
FORMAT AS CSV
DELIMITER ','
IGNOREHEADER 1
GZIP
MANIFEST
COMPUPDATE OFF  -- Disable if table already has compression
STATUPDATE OFF; -- Update statistics separately for better control

-- 3. COPY from Parquet format (most efficient)
COPY analytics.fact_sales_parquet
FROM 's3://company-data/sales-parquet/2023/01/'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftLoadRole'
FORMAT AS PARQUET;

-- 4. Incremental loading with UPSERT pattern
-- Create staging table
CREATE TEMP TABLE staging_sales (LIKE analytics.fact_sales);

-- Load new data into staging
COPY staging_sales
FROM 's3://company-data/incremental/sales_20230115.csv'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftLoadRole'
FORMAT AS CSV
DELIMITER ','
IGNOREHEADER 1;

-- Perform UPSERT operation
BEGIN TRANSACTION;

-- Delete existing records that will be updated
DELETE FROM analytics.fact_sales
WHERE sale_id IN (SELECT sale_id FROM staging_sales);

-- Insert new and updated records
INSERT INTO analytics.fact_sales
SELECT * FROM staging_sales;

END TRANSACTION;

-- 5. Error handling and monitoring
-- Check for load errors
SELECT 
    starttime,
    filename,
    line_number,
    colname,
    type,
    position,
    raw_line,
    err_reason
FROM stl_load_errors 
WHERE starttime >= DATEADD(hour, -1, GETDATE())
ORDER BY starttime DESC;

-- Monitor COPY performance
SELECT 
    query,
    slice,
    read_time,
    write_time,
    file_size,
    lines_scanned,
    lines_loaded
FROM stl_load_commits 
WHERE query IN (
    SELECT query FROM stl_query 
    WHERE querytxt LIKE 'COPY%'
    AND starttime >= DATEADD(hour, -1, GETDATE())
);

-- 6. Bulk loading best practices
-- Create optimized staging table for bulk loads
CREATE TABLE analytics.staging_fact_sales (
    sale_id BIGINT,
    customer_id INTEGER,
    product_id INTEGER,
    store_id INTEGER,
    sale_date DATE,
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(12,2)
)
DISTSTYLE KEY
DISTKEY (customer_id)
SORTKEY (sale_date);

-- Bulk load with transaction control
BEGIN TRANSACTION;

-- Load data
COPY analytics.staging_fact_sales
FROM 's3://company-data/bulk-load/sales_202301.csv.gz'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftLoadRole'
FORMAT AS CSV
DELIMITER ','
IGNOREHEADER 1
GZIP
COMPUPDATE OFF
STATUPDATE OFF;

-- Validate data quality
SELECT 
    COUNT(*) as total_rows,
    COUNT(DISTINCT sale_id) as unique_sales,
    MIN(sale_date) as min_date,
    MAX(sale_date) as max_date,
    SUM(CASE WHEN total_amount <= 0 THEN 1 ELSE 0 END) as invalid_amounts
FROM analytics.staging_fact_sales;

-- If validation passes, swap tables
ALTER TABLE analytics.fact_sales RENAME TO fact_sales_backup;
ALTER TABLE analytics.staging_fact_sales RENAME TO fact_sales;

-- Update statistics
ANALYZE analytics.fact_sales;

END TRANSACTION;

-- 7. Real-time streaming with Kinesis Data Firehose
-- Configure Firehose to deliver to S3 in Redshift-compatible format
-- Use Lambda to trigger COPY commands for micro-batches

-- Example Lambda-triggered incremental load
CREATE OR REPLACE PROCEDURE load_incremental_data(file_path VARCHAR(500))
AS $$
BEGIN
    -- Create temporary table for new data
    CREATE TEMP TABLE temp_incremental (LIKE analytics.fact_sales);
    
    -- Load new data
    EXECUTE 'COPY temp_incremental FROM ''' || file_path || ''' 
             IAM_ROLE ''arn:aws:iam::123456789012:role/RedshiftLoadRole''
             FORMAT AS CSV DELIMITER '','' IGNOREHEADER 1';
    
    -- Merge with existing data
    DELETE FROM analytics.fact_sales 
    WHERE sale_id IN (SELECT sale_id FROM temp_incremental);
    
    INSERT INTO analytics.fact_sales 
    SELECT * FROM temp_incremental;
    
    -- Log the load
    INSERT INTO analytics.load_log (load_time, file_path, rows_loaded)
    SELECT GETDATE(), file_path, COUNT(*) FROM temp_incremental;
    
END;
$$ LANGUAGE plpgsql;

-- Call procedure for incremental load
CALL load_incremental_data('s3://company-data/incremental/sales_20230115_1400.csv');
```

### Q7: How do you implement Change Data Capture (CDC) with Redshift?

**Answer:**
CDC in Redshift involves capturing changes from source systems and applying them to the data warehouse. Common patterns include timestamp-based, log-based, and trigger-based CDC.

**Code Example:**
```sql
-- 1. Timestamp-based CDC implementation
-- Source table structure (simulating operational database)
CREATE TABLE source_system.customers (
    customer_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    status VARCHAR(20),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- CDC tracking table in Redshift
CREATE TABLE analytics.cdc_customers (
    customer_id INTEGER,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    status VARCHAR(20),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    cdc_operation VARCHAR(10), -- INSERT, UPDATE, DELETE
    cdc_timestamp TIMESTAMP DEFAULT GETDATE(),
    is_current BOOLEAN DEFAULT TRUE
)
DISTSTYLE KEY
DISTKEY (customer_id)
SORTKEY (customer_id, cdc_timestamp);

-- 2. CDC processing procedure
CREATE OR REPLACE PROCEDURE process_customer_cdc()
AS $$
DECLARE
    last_processed_time TIMESTAMP;
    current_time TIMESTAMP := GETDATE();
BEGIN
    -- Get last processed timestamp
    SELECT COALESCE(MAX(cdc_timestamp), '1900-01-01'::TIMESTAMP)
    INTO last_processed_time
    FROM analytics.cdc_customers;
    
    -- Create staging table for changes
    CREATE TEMP TABLE staging_customer_changes AS
    SELECT 
        customer_id,
        first_name,
        last_name,
        email,
        status,
        created_at,
        updated_at,
        CASE 
            WHEN created_at > last_processed_time THEN 'INSERT'
            WHEN updated_at > last_processed_time THEN 'UPDATE'
        END as cdc_operation
    FROM source_system.customers
    WHERE created_at > last_processed_time 
       OR updated_at > last_processed_time;
    
    -- Handle deletes (requires additional logic or soft delete flags)
    INSERT INTO staging_customer_changes
    SELECT 
        customer_id,
        NULL, NULL, NULL, 'DELETED',
        NULL, NULL, 'DELETE'
    FROM analytics.cdc_customers c
    WHERE c.is_current = TRUE
    AND NOT EXISTS (
        SELECT 1 FROM source_system.customers s 
        WHERE s.customer_id = c.customer_id
    );
    
    -- Mark existing records as not current for updated/deleted records
    UPDATE analytics.cdc_customers 
    SET is_current = FALSE
    WHERE customer_id IN (
        SELECT customer_id FROM staging_customer_changes
        WHERE cdc_operation IN ('UPDATE', 'DELETE')
    )
    AND is_current = TRUE;
    
    -- Insert new CDC records
    INSERT INTO analytics.cdc_customers (
        customer_id, first_name, last_name, email, status,
        created_at, updated_at, cdc_operation, cdc_timestamp, is_current
    )
    SELECT 
        customer_id, first_name, last_name, email, status,
        created_at, updated_at, cdc_operation, current_time,
        CASE WHEN cdc_operation = 'DELETE' THEN FALSE ELSE TRUE END
    FROM staging_customer_changes;
    
    -- Log CDC processing
    INSERT INTO analytics.cdc_log (table_name, processed_time, records_processed)
    SELECT 'customers', current_time, COUNT(*) FROM staging_customer_changes;
    
END;
$$ LANGUAGE plpgsql;

-- 3. Create current view for easy querying
CREATE VIEW analytics.dim_customers_current AS
SELECT 
    customer_id,
    first_name,
    last_name,
    email,
    status,
    created_at,
    updated_at
FROM analytics.cdc_customers
WHERE is_current = TRUE
AND cdc_operation != 'DELETE';

-- 4. Historical analysis capabilities
-- Point-in-time query
CREATE OR REPLACE FUNCTION get_customers_at_time(query_time TIMESTAMP)
RETURNS TABLE (
    customer_id INTEGER,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    status VARCHAR(20)
) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT ON (c.customer_id)
        c.customer_id,
        c.first_name,
        c.last_name,
        c.email,
        c.status
    FROM analytics.cdc_customers c
    WHERE c.cdc_timestamp <= query_time
    AND c.cdc_operation != 'DELETE'
    ORDER BY c.customer_id, c.cdc_timestamp DESC;
END;
$$ LANGUAGE plpgsql;

-- Usage: Get customer state as of specific time
SELECT * FROM get_customers_at_time('2023-01-15 12:00:00');

-- 5. CDC with AWS DMS integration
-- Create target table for DMS replication
CREATE TABLE analytics.dms_customers (
    customer_id INTEGER,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    status VARCHAR(20),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    -- DMS metadata columns
    dms_operation VARCHAR(10),
    dms_timestamp TIMESTAMP,
    dms_batch_id VARCHAR(50)
)
DISTSTYLE KEY
DISTKEY (customer_id)
SORTKEY (customer_id, dms_timestamp);

-- Process DMS CDC data
CREATE OR REPLACE PROCEDURE process_dms_cdc()
AS $$
BEGIN
    -- Apply DMS changes to dimension table
    -- Handle INSERT operations
    INSERT INTO analytics.dim_customers_scd2 (
        customer_id, first_name, last_name, email, status,
        effective_date, expiry_date, is_current
    )
    SELECT 
        customer_id, first_name, last_name, email, status,
        dms_timestamp, '9999-12-31'::DATE, TRUE
    FROM analytics.dms_customers
    WHERE dms_operation = 'I'
    AND dms_timestamp > (SELECT COALESCE(MAX(last_processed), '1900-01-01') FROM analytics.cdc_control WHERE table_name = 'customers');
    
    -- Handle UPDATE operations (SCD Type 2)
    -- Close existing record
    UPDATE analytics.dim_customers_scd2 
    SET expiry_date = dms.dms_timestamp::DATE - 1,
        is_current = FALSE
    FROM analytics.dms_customers dms
    WHERE dms.dms_operation = 'U'
    AND analytics.dim_customers_scd2.customer_id = dms.customer_id
    AND analytics.dim_customers_scd2.is_current = TRUE;
    
    -- Insert new version
    INSERT INTO analytics.dim_customers_scd2 (
        customer_id, first_name, last_name, email, status,
        effective_date, expiry_date, is_current
    )
    SELECT 
        customer_id, first_name, last_name, email, status,
        dms_timestamp::DATE, '9999-12-31'::DATE, TRUE
    FROM analytics.dms_customers
    WHERE dms_operation = 'U';
    
    -- Handle DELETE operations
    UPDATE analytics.dim_customers_scd2 
    SET expiry_date = dms.dms_timestamp::DATE,
        is_current = FALSE
    FROM analytics.dms_customers dms
    WHERE dms.dms_operation = 'D'
    AND analytics.dim_customers_scd2.customer_id = dms.customer_id
    AND analytics.dim_customers_scd2.is_current = TRUE;
    
    -- Update control table
    UPDATE analytics.cdc_control 
    SET last_processed = (SELECT MAX(dms_timestamp) FROM analytics.dms_customers)
    WHERE table_name = 'customers';
    
END;
$$ LANGUAGE plpgsql;

-- 6. Monitor CDC performance and data quality
SELECT 
    table_name,
    cdc_operation,
    COUNT(*) as record_count,
    MIN(cdc_timestamp) as earliest_change,
    MAX(cdc_timestamp) as latest_change
FROM analytics.cdc_customers
WHERE cdc_timestamp >= DATEADD(day, -1, GETDATE())
GROUP BY table_name, cdc_operation
ORDER BY table_name, cdc_operation;

-- Data quality checks for CDC
SELECT 
    'Duplicate active records' as check_name,
    COUNT(*) as issue_count
FROM (
    SELECT customer_id, COUNT(*)
    FROM analytics.cdc_customers
    WHERE is_current = TRUE
    GROUP BY customer_id
    HAVING COUNT(*) > 1
) duplicates

UNION ALL

SELECT 
    'Records without operations' as check_name,
    COUNT(*) as issue_count
FROM analytics.cdc_customers
WHERE cdc_operation IS NULL;
```

## Query Optimization

### Q8: How do you optimize complex analytical queries in Redshift?

**Answer:**
Redshift query optimization involves understanding execution plans, using appropriate joins, leveraging distribution keys, and implementing proper indexing strategies through sort keys.

**Code Example:**
```sql
-- Query optimization techniques

-- 1. Analyze query execution plan
EXPLAIN (VERBOSE TRUE, COSTS TRUE)
SELECT 
    c.customer_segment,
    p.product_category,
    DATE_TRUNC('month', s.sale_date) as month,
    SUM(s.sale_amount) as total_revenue,
    COUNT(DISTINCT s.customer_id) as unique_customers,
    AVG(s.sale_amount) as avg_order_value
FROM fact_sales s
JOIN dim_customers c ON s.customer_id = c.customer_id
JOIN dim_products p ON s.product_id = p.product_id
WHERE s.sale_date >= '2023-01-01'
GROUP BY c.customer_segment, p.product_category, DATE_TRUNC('month', s.sale_date)
ORDER BY total_revenue DESC;

-- 2. Optimized version with proper filtering and joins
SELECT 
    c.customer_segment,
    p.product_category,
    DATE_TRUNC('month', s.sale_date) as month,
    SUM(s.sale_amount) as total_revenue,
    COUNT(DISTINCT s.customer_id) as unique_customers,
    AVG(s.sale_amount) as avg_order_value
FROM (
    -- Pre-filter fact table to reduce data volume
    SELECT customer_id, product_id, sale_date, sale_amount
    FROM fact_sales
    WHERE sale_date >= '2023-01-01'
    AND sale_date < '2024-01-01'  -- Explicit upper bound for better pruning
) s
JOIN (
    -- Pre-filter dimension tables if needed
    SELECT customer_id, customer_segment
    FROM dim_customers
    WHERE customer_segment IN ('Premium', 'Standard', 'Basic')
) c ON s.customer_id = c.customer_id
JOIN (
    SELECT product_id, product_category
    FROM dim_products
    WHERE product_category IS NOT NULL
) p ON s.product_id = p.product_id
GROUP BY c.customer_segment, p.product_category, DATE_TRUNC('month', s.sale_date)
ORDER BY total_revenue DESC
LIMIT 100;  -- Limit results if not all needed

-- 3. Window function optimization
-- Inefficient: Multiple passes over data
SELECT 
    customer_id,
    sale_date,
    sale_amount,
    (SELECT AVG(sale_amount) FROM fact_sales s2 WHERE s2.customer_id = s1.customer_id) as avg_customer_spend,
    (SELECT COUNT(*) FROM fact_sales s3 WHERE s3.customer_id = s1.customer_id) as customer_order_count
FROM fact_sales s1;

-- Optimized: Single pass with window functions
SELECT 
    customer_id,
    sale_date,
    sale_amount,
    AVG(sale_amount) OVER (PARTITION BY customer_id) as avg_customer_spend,
    COUNT(*) OVER (PARTITION BY customer_id) as customer_order_count,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY sale_date DESC) as recency_rank
FROM fact_sales;

-- 4. Efficient aggregation patterns
-- Create pre-aggregated tables for common queries
CREATE TABLE monthly_sales_summary AS
SELECT 
    DATE_TRUNC('month', sale_date) as month,
    customer_segment,
    product_category,
    SUM(sale_amount) as total_revenue,
    COUNT(*) as transaction_count,
    COUNT(DISTINCT customer_id) as unique_customers,
    AVG(sale_amount) as avg_transaction_value
FROM fact_sales s
JOIN dim_customers c USING (customer_id)
JOIN dim_products p USING (product_id)
GROUP BY 1, 2, 3;

-- 5. Query rewriting for better performance
-- Instead of EXISTS (can be slow)
SELECT DISTINCT customer_id
FROM dim_customers c
WHERE EXISTS (
    SELECT 1 FROM fact_sales s 
    WHERE s.customer_id = c.customer_id 
    AND s.sale_date >= '2023-01-01'
);

-- Use INNER JOIN (often faster)
SELECT DISTINCT c.customer_id
FROM dim_customers c
INNER JOIN (
    SELECT DISTINCT customer_id 
    FROM fact_sales 
    WHERE sale_date >= '2023-01-01'
) s ON c.customer_id = s.customer_id;
```

### Q9: How do you implement and tune Workload Management (WLM) in Redshift?

**Answer:**
WLM controls query execution by managing memory allocation, concurrency, and query prioritization. Proper WLM configuration ensures optimal resource utilization and query performance.

**Code Example:**
```sql
-- Monitor current WLM configuration
SELECT 
    service_class,
    service_class_name,
    num_query_tasks,
    query_working_mem,
    max_execution_time,
    user_group_wild_card,
    query_group_wild_card
FROM stv_wlm_service_class_config
ORDER BY service_class;

-- Monitor WLM queue performance
SELECT 
    service_class,
    service_class_name,
    num_executing_queries,
    num_executed_queries,
    num_queued_queries,
    total_queue_time,
    avg_queue_time,
    total_exec_time,
    avg_exec_time
FROM stv_wlm_service_class_state
WHERE service_class > 4  -- Exclude system queues
ORDER BY service_class;

-- Analyze query queue wait times
SELECT 
    w.query,
    w.service_class,
    w.slot_count,
    w.total_queue_time,
    w.total_exec_time,
    q.querytxt,
    q.starttime,
    q.endtime
FROM stl_wlm_query w
JOIN stl_query q ON w.query = q.query
WHERE w.queue_start_time >= DATEADD(hour, -1, GETDATE())
AND w.total_queue_time > 0
ORDER BY w.total_queue_time DESC;

-- WLM configuration example (JSON format for parameter group)
{
  "query_concurrency": 15,
  "max_concurrency_scaling_clusters": 10,
  "wlm_json_configuration": [
    {
      "query_concurrency": 5,
      "max_execution_time": 14400000,
      "memory_percent_to_use": 40,
      "name": "ETL_Queue",
      "query_group": ["etl"],
      "query_group_wild_card": 0,
      "user_group": ["etl_users"],
      "user_group_wild_card": 0
    },
    {
      "query_concurrency": 8,
      "max_execution_time": 3600000,
      "memory_percent_to_use": 35,
      "name": "Analytics_Queue",
      "query_group": ["analytics"],
      "query_group_wild_card": 0,
      "user_group": ["analysts"],
      "user_group_wild_card": 0
    },
    {
      "query_concurrency": 2,
      "max_execution_time": 7200000,
      "memory_percent_to_use": 25,
      "name": "Reporting_Queue",
      "query_group": ["reporting"],
      "query_group_wild_card": 0,
      "user_group": ["report_users"],
      "user_group_wild_card": 0
    }
  ]
}

-- Set query group for session
SET query_group TO 'etl';

-- Monitor concurrency scaling usage
SELECT 
    start_time,
    end_time,
    cluster_identifier,
    concurrency_scaling_cluster_identifier,
    usage_limit_breach
FROM stl_concurrency_scaling_usage
WHERE start_time >= DATEADD(day, -7, GETDATE())
ORDER BY start_time DESC;

-- Query performance by WLM queue
SELECT 
    w.service_class,
    sc.service_class_name,
    COUNT(*) as query_count,
    AVG(w.total_queue_time) as avg_queue_time,
    AVG(w.total_exec_time) as avg_exec_time,
    MAX(w.total_queue_time) as max_queue_time,
    MAX(w.total_exec_time) as max_exec_time
FROM stl_wlm_query w
JOIN stv_wlm_service_class_config sc ON w.service_class = sc.service_class
WHERE w.queue_start_time >= DATEADD(day, -1, GETDATE())
GROUP BY w.service_class, sc.service_class_name
ORDER BY w.service_class;
```

## Security and Administration

### Q10: How do you implement comprehensive security in Redshift?

**Answer:**
Redshift security involves encryption, access control, network security, and audit logging. Implementation includes IAM integration, VPC configuration, and fine-grained permissions.

**Code Example:**
```sql
-- User and role management
-- Create users with different access levels
CREATE USER analyst_user PASSWORD 'SecurePassword123!' 
CREATE_DB FALSE
CREATE_USER FALSE;

CREATE USER etl_service_user PASSWORD 'ETLServicePassword456!'
CREATE_DB FALSE
CREATE_USER FALSE;

CREATE USER admin_user PASSWORD 'AdminPassword789!'
CREATE_DB TRUE
CREATE_USER TRUE;

-- Create groups for role-based access
CREATE GROUP analysts;
CREATE GROUP etl_users;
CREATE GROUP data_engineers;

-- Add users to groups
ALTER GROUP analysts ADD USER analyst_user;
ALTER GROUP etl_users ADD USER etl_service_user;
ALTER GROUP data_engineers ADD USER admin_user;

-- Schema-level permissions
CREATE SCHEMA raw_data;
CREATE SCHEMA staging;
CREATE SCHEMA analytics;
CREATE SCHEMA sensitive_data;

-- Grant schema permissions
GRANT USAGE ON SCHEMA raw_data TO GROUP etl_users;
GRANT CREATE ON SCHEMA staging TO GROUP etl_users;
GRANT USAGE ON SCHEMA analytics TO GROUP analysts;
GRANT ALL ON SCHEMA sensitive_data TO GROUP data_engineers;

-- Table-level permissions
-- Grant read access to analysts
GRANT SELECT ON ALL TABLES IN SCHEMA analytics TO GROUP analysts;
GRANT SELECT ON ALL TABLES IN SCHEMA staging TO GROUP analysts;

-- Grant ETL permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA raw_data TO GROUP etl_users;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA staging TO GROUP etl_users;

-- Column-level security for sensitive data
CREATE TABLE sensitive_data.customer_pii (
    customer_id INTEGER,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    ssn VARCHAR(11),  -- Sensitive
    phone VARCHAR(15), -- Sensitive
    address VARCHAR(200) -- Sensitive
);

-- Create view with masked sensitive columns
CREATE VIEW analytics.customer_info AS
SELECT 
    customer_id,
    first_name,
    last_name,
    email,
    'XXX-XX-' || RIGHT(ssn, 4) as ssn_masked,
    'XXX-XXX-' || RIGHT(phone, 4) as phone_masked,
    LEFT(address, 20) || '...' as address_partial
FROM sensitive_data.customer_pii;

-- Grant access to masked view instead of raw table
GRANT SELECT ON analytics.customer_info TO GROUP analysts;

-- Row-level security implementation
CREATE TABLE sales_data (
    sale_id INTEGER,
    customer_id INTEGER,
    region VARCHAR(50),
    sale_amount DECIMAL(10,2),
    sale_date DATE
);

-- Create region-specific views
CREATE VIEW sales_data_east AS
SELECT * FROM sales_data WHERE region = 'East';

CREATE VIEW sales_data_west AS
SELECT * FROM sales_data WHERE region = 'West';

-- Create regional users and grant appropriate access
CREATE USER east_analyst PASSWORD 'EastPassword123!';
CREATE USER west_analyst PASSWORD 'WestPassword123!';

GRANT SELECT ON sales_data_east TO east_analyst;
GRANT SELECT ON sales_data_west TO west_analyst;

-- Audit and monitoring queries
-- Monitor user connections
SELECT 
    username,
    starttime,
    endtime,
    duration,
    remotehost,
    remoteport
FROM stl_connection_log
WHERE starttime >= DATEADD(day, -1, GETDATE())
ORDER BY starttime DESC;

-- Monitor user activity
SELECT 
    userid,
    username,
    query,
    starttime,
    endtime,
    aborted,
    substring(querytxt, 1, 100) as query_text
FROM stl_query
WHERE starttime >= DATEADD(hour, -1, GETDATE())
AND userid > 1  -- Exclude superuser
ORDER BY starttime DESC;

-- Monitor failed login attempts
SELECT 
    event,
    recordtime,
    username,
    remotehost,
    remoteport
FROM stl_userlog
WHERE event = 'authentication failure'
AND recordtime >= DATEADD(day, -1, GETDATE())
ORDER BY recordtime DESC;

-- Database encryption status
SELECT 
    cluster_identifier,
    encrypted,
    kms_key_id
FROM stv_cluster_info;

-- SSL connection monitoring
SELECT 
    username,
    ssl,
    starttime,
    remotehost
FROM stl_connection_log
WHERE starttime >= DATEADD(day, -1, GETDATE())
AND ssl = false  -- Monitor non-SSL connections
ORDER BY starttime DESC;
```

### Q11: How do you implement disaster recovery and backup strategies for Redshift?

**Answer:**
Redshift disaster recovery involves automated snapshots, cross-region replication, and recovery procedures. Strategies include point-in-time recovery and cluster restoration.

**Code Example:**
```sql
-- Snapshot management and monitoring
-- Check current snapshot configuration
SELECT 
    cluster_identifier,
    automated_snapshot_retention_period,
    preferred_maintenance_window,
    cluster_create_time
FROM stv_cluster_info;

-- Monitor snapshot status
SELECT 
    snapshot_id,
    cluster_identifier,
    snapshot_time,
    status,
    progress_in_mega_bytes,
    total_backup_size_in_mega_bytes,
    elapsed_time_in_seconds
FROM stv_snapshot
WHERE snapshot_time >= DATEADD(day, -7, GETDATE())
ORDER BY snapshot_time DESC;

-- Create manual snapshot
-- (This would be done via AWS CLI or API)
-- aws redshift create-cluster-snapshot \
--   --cluster-identifier my-cluster \
--   --snapshot-identifier manual-snapshot-2023-01-15

-- Backup validation queries
-- Check data consistency before backup
SELECT 
    schemaname,
    tablename,
    COUNT(*) as row_count,
    SUM(size) as total_size_mb
FROM svv_table_info
WHERE schemaname NOT IN ('information_schema', 'pg_catalog')
GROUP BY schemaname, tablename
ORDER BY total_size_mb DESC;

-- Create backup metadata table
CREATE TABLE backup_metadata (
    backup_id VARCHAR(100),
    backup_type VARCHAR(20), -- 'automated' or 'manual'
    backup_timestamp TIMESTAMP,
    cluster_identifier VARCHAR(100),
    database_name VARCHAR(100),
    total_size_mb BIGINT,
    table_count INTEGER,
    row_count BIGINT,
    backup_status VARCHAR(20),
    retention_days INTEGER
);

-- Log backup information
INSERT INTO backup_metadata
SELECT 
    'manual-snapshot-' || TO_CHAR(GETDATE(), 'YYYY-MM-DD-HH24-MI-SS') as backup_id,
    'manual' as backup_type,
    GETDATE() as backup_timestamp,
    'production-cluster' as cluster_identifier,
    'analytics_db' as database_name,
    SUM(size) as total_size_mb,
    COUNT(*) as table_count,
    SUM(tbl_rows) as row_count,
    'completed' as backup_status,
    30 as retention_days
FROM svv_table_info
WHERE schemaname NOT IN ('information_schema', 'pg_catalog');

-- Disaster recovery procedures
-- 1. Cross-region snapshot copy (via AWS CLI)
-- aws redshift copy-cluster-snapshot \
--   --source-snapshot-identifier manual-snapshot-2023-01-15 \
--   --target-snapshot-identifier dr-snapshot-2023-01-15 \
--   --source-region us-east-1 \
--   --target-region us-west-2

-- 2. Point-in-time recovery validation
SELECT 
    backup_timestamp,
    backup_id,
    total_size_mb,
    table_count,
    row_count
FROM backup_metadata
WHERE backup_timestamp BETWEEN '2023-01-15 00:00:00' AND '2023-01-15 23:59:59'
ORDER BY backup_timestamp;

-- 3. Recovery testing queries
-- Validate restored data integrity
WITH current_counts AS (
    SELECT 
        schemaname,
        tablename,
        tbl_rows as current_rows
    FROM svv_table_info
    WHERE schemaname = 'analytics'
),
backup_counts AS (
    -- This would come from backup metadata or restored cluster
    SELECT 
        'analytics' as schemaname,
        'fact_sales' as tablename,
        1000000 as backup_rows
    UNION ALL
    SELECT 'analytics', 'dim_customers', 50000
    UNION ALL
    SELECT 'analytics', 'dim_products', 10000
)
SELECT 
    c.schemaname,
    c.tablename,
    c.current_rows,
    b.backup_rows,
    c.current_rows - b.backup_rows as row_difference,
    CASE 
        WHEN c.current_rows = b.backup_rows THEN 'MATCH'
        WHEN ABS(c.current_rows - b.backup_rows) < (b.backup_rows * 0.01) THEN 'ACCEPTABLE'
        ELSE 'MISMATCH'
    END as validation_status
FROM current_counts c
JOIN backup_counts b ON c.schemaname = b.schemaname AND c.tablename = b.tablename;

-- 4. Recovery time objective (RTO) monitoring
CREATE TABLE recovery_metrics (
    recovery_id VARCHAR(100),
    recovery_start_time TIMESTAMP,
    recovery_end_time TIMESTAMP,
    recovery_duration_minutes INTEGER,
    data_size_gb DECIMAL(10,2),
    recovery_type VARCHAR(50), -- 'full_restore', 'point_in_time', 'table_restore'
    success_status BOOLEAN,
    notes TEXT
);

-- Log recovery operation
INSERT INTO recovery_metrics VALUES (
    'recovery-2023-01-15-001',
    '2023-01-15 10:00:00',
    '2023-01-15 10:45:00',
    45,
    500.5,
    'full_restore',
    true,
    'Successful restore from automated snapshot'
);

-- Recovery performance analysis
SELECT 
    recovery_type,
    COUNT(*) as recovery_count,
    AVG(recovery_duration_minutes) as avg_duration_minutes,
    AVG(data_size_gb) as avg_data_size_gb,
    AVG(data_size_gb / recovery_duration_minutes) as avg_gb_per_minute,
    SUM(CASE WHEN success_status THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as success_rate_pct
FROM recovery_metrics
GROUP BY recovery_type;
```

## Data Engineering Use Cases

### Q12: How do you implement a complete data warehouse solution using Redshift?

**Answer:**
A complete Redshift data warehouse involves dimensional modeling, ETL processes, data quality checks, and performance optimization. Implementation includes staging, transformation, and serving layers.

**Code Example:**
```sql
-- Complete data warehouse implementation

-- 1. Create schema structure
CREATE SCHEMA raw_data;
CREATE SCHEMA staging;
CREATE SCHEMA dimensions;
CREATE SCHEMA facts;
CREATE SCHEMA marts;
CREATE SCHEMA audit;

-- 2. Staging tables for raw data
CREATE TABLE staging.customers_staging (
    customer_id INTEGER,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    registration_date DATE,
    last_updated TIMESTAMP,
    source_system VARCHAR(20),
    batch_id VARCHAR(50)
)
DISTSTYLE EVEN;

CREATE TABLE staging.orders_staging (
    order_id INTEGER,
    customer_id INTEGER,
    product_id INTEGER,
    order_date DATE,
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(12,2),
    order_status VARCHAR(20),
    last_updated TIMESTAMP,
    source_system VARCHAR(20),
    batch_id VARCHAR(50)
)
DISTSTYLE KEY
DISTKEY (customer_id);

-- 3. Dimension tables (SCD Type 2)
CREATE TABLE dimensions.dim_customers (
    customer_key BIGINT IDENTITY(1,1) PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    registration_date DATE,
    effective_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    is_current BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP DEFAULT GETDATE(),
    updated_date TIMESTAMP DEFAULT GETDATE()
)
DISTSTYLE ALL
SORTKEY (customer_id, effective_date);

CREATE TABLE dimensions.dim_products (
    product_key BIGINT IDENTITY(1,1) PRIMARY KEY,
    product_id INTEGER NOT NULL,
    product_name VARCHAR(255),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    unit_cost DECIMAL(10,2),
    effective_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    is_current BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP DEFAULT GETDATE()
)
DISTSTYLE ALL
SORTKEY (product_id, effective_date);

-- 4. Fact table
CREATE TABLE facts.fact_sales (
    sale_key BIGINT IDENTITY(1,1) PRIMARY KEY,
    order_id INTEGER NOT NULL,
    customer_key BIGINT NOT NULL,
    product_key BIGINT NOT NULL,
    date_key INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    tax_amount DECIMAL(10,2) DEFAULT 0,
    created_date TIMESTAMP DEFAULT GETDATE()
)
DISTSTYLE KEY
DISTKEY (customer_key)
SORTKEY (date_key, customer_key);

-- 5. Date dimension
CREATE TABLE dimensions.dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL,
    day_of_week INTEGER,
    day_name VARCHAR(10),
    day_of_month INTEGER,
    day_of_year INTEGER,
    week_of_year INTEGER,
    month_number INTEGER,
    month_name VARCHAR(10),
    quarter_number INTEGER,
    quarter_name VARCHAR(2),
    year_number INTEGER,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN,
    fiscal_year INTEGER,
    fiscal_quarter INTEGER
)
DISTSTYLE ALL
SORTKEY (date_key);

-- 6. ETL procedures
CREATE OR REPLACE PROCEDURE load_customer_dimension()
AS $$
BEGIN
    -- Handle SCD Type 2 for customer dimension
    
    -- Step 1: Identify changed records
    CREATE TEMP TABLE customer_changes AS
    SELECT 
        s.customer_id,
        s.first_name,
        s.last_name,
        s.email,
        s.registration_date,
        CURRENT_DATE as effective_date,
        '9999-12-31'::DATE as expiry_date,
        TRUE as is_current
    FROM staging.customers_staging s
    LEFT JOIN dimensions.dim_customers d ON s.customer_id = d.customer_id AND d.is_current = TRUE
    WHERE d.customer_id IS NULL  -- New customers
       OR d.first_name != s.first_name
       OR d.last_name != s.last_name
       OR d.email != s.email;
    
    -- Step 2: Close existing records for changed customers
    UPDATE dimensions.dim_customers
    SET expiry_date = CURRENT_DATE - 1,
        is_current = FALSE,
        updated_date = GETDATE()
    WHERE customer_id IN (SELECT customer_id FROM customer_changes)
      AND is_current = TRUE;
    
    -- Step 3: Insert new/updated records
    INSERT INTO dimensions.dim_customers (
        customer_id, first_name, last_name, email, registration_date,
        effective_date, expiry_date, is_current
    )
    SELECT 
        customer_id, first_name, last_name, email, registration_date,
        effective_date, expiry_date, is_current
    FROM customer_changes;
    
    -- Log the operation
    INSERT INTO audit.etl_log (table_name, operation, record_count, execution_time)
    SELECT 'dim_customers', 'SCD_TYPE_2', COUNT(*), GETDATE()
    FROM customer_changes;
    
END;
$$ LANGUAGE plpgsql;

-- 7. Fact table loading procedure
CREATE OR REPLACE PROCEDURE load_sales_fact()
AS $$
BEGIN
    -- Load fact table with proper dimension key lookups
    INSERT INTO facts.fact_sales (
        order_id, customer_key, product_key, date_key,
        quantity, unit_price, total_amount
    )
    SELECT 
        s.order_id,
        c.customer_key,
        p.product_key,
        d.date_key,
        s.quantity,
        s.unit_price,
        s.total_amount
    FROM staging.orders_staging s
    JOIN dimensions.dim_customers c ON s.customer_id = c.customer_id 
        AND s.order_date BETWEEN c.effective_date AND c.expiry_date
    JOIN dimensions.dim_products p ON s.product_id = p.product_id 
        AND s.order_date BETWEEN p.effective_date AND p.expiry_date
    JOIN dimensions.dim_date d ON s.order_date = d.full_date
    WHERE NOT EXISTS (
        SELECT 1 FROM facts.fact_sales f WHERE f.order_id = s.order_id
    );
    
    -- Log the operation
    INSERT INTO audit.etl_log (table_name, operation, record_count, execution_time)
    SELECT 'fact_sales', 'INSERT', COUNT(*), GETDATE()
    FROM staging.orders_staging;
    
END;
$$ LANGUAGE plpgsql;

-- 8. Data mart creation
CREATE TABLE marts.customer_sales_summary AS
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    c.email,
    COUNT(DISTINCT f.order_id) as total_orders,
    SUM(f.total_amount) as total_spent,
    AVG(f.total_amount) as avg_order_value,
    MIN(d.full_date) as first_order_date,
    MAX(d.full_date) as last_order_date,
    DATEDIFF(day, MIN(d.full_date), MAX(d.full_date)) as customer_lifetime_days,
    CASE 
        WHEN SUM(f.total_amount) >= 1000 THEN 'High Value'
        WHEN SUM(f.total_amount) >= 500 THEN 'Medium Value'
        ELSE 'Low Value'
    END as customer_segment
FROM dimensions.dim_customers c
JOIN facts.fact_sales f ON c.customer_key = f.customer_key
JOIN dimensions.dim_date d ON f.date_key = d.date_key
WHERE c.is_current = TRUE
GROUP BY c.customer_id, c.first_name, c.last_name, c.email;

-- 9. Data quality checks
CREATE OR REPLACE PROCEDURE run_data_quality_checks()
AS $$
BEGIN
    -- Check for orphaned records
    INSERT INTO audit.data_quality_issues (issue_type, table_name, issue_count, check_date)
    SELECT 
        'ORPHANED_RECORDS' as issue_type,
        'fact_sales' as table_name,
        COUNT(*) as issue_count,
        CURRENT_DATE as check_date
    FROM facts.fact_sales f
    LEFT JOIN dimensions.dim_customers c ON f.customer_key = c.customer_key
    WHERE c.customer_key IS NULL;
    
    -- Check for duplicate records
    INSERT INTO audit.data_quality_issues (issue_type, table_name, issue_count, check_date)
    SELECT 
        'DUPLICATE_RECORDS' as issue_type,
        'fact_sales' as table_name,
        COUNT(*) - COUNT(DISTINCT order_id) as issue_count,
        CURRENT_DATE as check_date
    FROM facts.fact_sales;
    
    -- Check for null values in critical columns
    INSERT INTO audit.data_quality_issues (issue_type, table_name, issue_count, check_date)
    SELECT 
        'NULL_VALUES' as issue_type,
        'fact_sales' as table_name,
        SUM(CASE WHEN total_amount IS NULL THEN 1 ELSE 0 END) as issue_count,
        CURRENT_DATE as check_date
    FROM facts.fact_sales;
    
END;
$$ LANGUAGE plpgsql;

-- 10. Performance monitoring
CREATE VIEW audit.table_performance_summary AS
SELECT 
    schemaname,
    tablename,
    size as size_mb,
    tbl_rows,
    skew_sortkey1,
    skew_rows,
    pct_used,
    diststyle,
    sortkey1,
    CASE 
        WHEN skew_rows > 1.5 THEN 'HIGH_SKEW'
        WHEN pct_used < 80 THEN 'UNDER_UTILIZED'
        WHEN sortkey1 IS NULL THEN 'NO_SORT_KEY'
        ELSE 'OPTIMAL'
    END as performance_status
FROM svv_table_info
WHERE schemaname IN ('dimensions', 'facts', 'marts')
ORDER BY size DESC;
```

---

## Key Takeaways

1. **Columnar Storage**: Optimized for analytical queries with compression and encoding
2. **MPP Architecture**: Parallel processing across multiple compute nodes
3. **Distribution Strategy**: Proper DISTKEY and SORTKEY selection critical for performance
4. **Spectrum Integration**: Seamless querying of S3 data without loading
5. **COPY Command**: Efficient bulk loading with parallel processing
6. **Workload Management**: WLM queues for managing concurrent queries
7. **CDC Implementation**: Various patterns for capturing and applying data changes
8. **Monitoring**: Comprehensive system tables for performance analysis and optimization
9. **Query Optimization**: Advanced techniques for complex analytical workloads
10. **Security**: Comprehensive access control and encryption strategies
11. **Disaster Recovery**: Automated backups and cross-region replication
12. **Data Warehouse Design**: Complete dimensional modeling and ETL processes