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