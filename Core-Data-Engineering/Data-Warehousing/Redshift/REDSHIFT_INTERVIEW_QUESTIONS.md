# Amazon Redshift Interview Questions - Complete Guide (150+ Questions)

## 📋 Table of Contents

1. [Basic Level Questions (1-3 years experience)](#basic-level-questions-1-3-years-experience) - Q1-Q10
2. [Intermediate Level Questions (3-5 years experience)](#intermediate-level-questions-3-5-years-experience) - Q11-Q15
3. [Advanced Level Questions (5+ years experience)](#advanced-level-questions-5-years-experience) - Q16-Q20
4. [Architecture & Performance](#architecture--performance) - Q21-Q23
5. [Streaming & Real-time Processing](#streaming--real-time-processing) - Q24-Q25
6. [Production & Operations](#production--operations) - Q26-Q27
7. [Scenario-Based Questions](#scenario-based-questions) - Q28-Q30
8. [Performance Tuning & Optimization](#performance-tuning--optimization) - Q31-Q35
9. [Data Modeling & Architecture](#data-modeling--architecture) - Q36-Q40
10. [Security & Compliance](#security--compliance) - Q41-Q45
11. [Cost Optimization](#cost-optimization) - Q46-Q50
12. [Troubleshooting & Operations](#troubleshooting--operations) - Q51-Q55
13. [Advanced Integration](#advanced-integration) - Q56-Q60

---

## Basic Level Questions (1-3 years experience)

### Q1: What is Amazon Redshift and how does it differ from traditional databases?

**Answer:**
Amazon Redshift is a fully managed, petabyte-scale data warehouse service designed for analytical workloads. It uses columnar storage, massively parallel processing (MPP), and compression to deliver fast query performance.

**Key Differences:**
- **Columnar Storage**: Optimized for analytical queries vs row-based OLTP
- **MPP Architecture**: Distributes queries across multiple nodes
- **Compression**: Automatic compression reduces storage and I/O
- **Managed Service**: AWS handles infrastructure, backups, and maintenance
- **Scalability**: Elastic scaling from gigabytes to petabytes

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
```

### Q3: How do distribution styles and sort keys affect performance?

**Answer:**
Distribution styles determine how data is distributed across nodes, while sort keys determine physical data ordering. Proper selection minimizes data movement and enables zone maps for query pruning.

**Distribution Styles:**
- **KEY**: Distribute based on column values
- **ALL**: Copy entire table to all nodes
- **EVEN**: Round-robin distribution
- **AUTO**: Redshift chooses optimal distribution

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

-- Optimal distribution key selection example
CREATE TABLE analytics.fact_orders_optimized (
    order_id BIGINT,
    customer_id INTEGER,
    product_id INTEGER,
    order_date DATE,
    quantity INTEGER,
    amount DECIMAL(10,2)
)
DISTSTYLE KEY
DISTKEY (customer_id)  -- Most frequent join column
SORTKEY (order_date, customer_id);  -- Filter and group by patterns
```

### Q4: What is the COPY command and why is it preferred for data loading?

**Answer:**
COPY is Redshift's primary data loading command that provides parallel loading, automatic compression, and error handling. It's optimized for bulk data loading from S3, DynamoDB, or remote hosts.

**Key Benefits:**
- **Parallel Processing**: Loads multiple files simultaneously
- **Automatic Compression**: Analyzes and applies optimal compression
- **Error Handling**: Detailed error reporting and recovery
- **Performance**: Much faster than INSERT statements

```sql
-- Basic COPY from S3
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

-- COPY from Parquet (most efficient)
COPY analytics.fact_sales_parquet
FROM 's3://company-data/sales-parquet/2023/01/'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftLoadRole'
FORMAT AS PARQUET;

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
```

### Q5: How do you monitor query performance in Redshift?

**Answer:**
Redshift provides comprehensive system tables and views for monitoring query performance, resource utilization, and identifying bottlenecks.

```sql
-- Monitor recent query performance
SELECT 
    query,
    userid,
    starttime,
    endtime,
    DATEDIFF(seconds, starttime, endtime) as duration_seconds,
    aborted,
    substring(querytxt, 1, 100) as query_text
FROM stl_query 
WHERE starttime >= DATEADD(hour, -1, GETDATE())
AND duration_seconds > 10
ORDER BY duration_seconds DESC;

-- Check query execution details
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
FROM svl_query_summary 
WHERE query = pg_last_query_id()
ORDER BY segment, step;

-- Monitor table scan performance
SELECT 
    schemaname,
    tablename,
    size_mb,
    pct_used,
    skew_rows,
    skew_sortkey1
FROM svv_table_info 
WHERE schemaname = 'analytics'
ORDER BY size_mb DESC;
```

### Q6: What are the different compression encodings available in Redshift?

**Answer:**
Redshift supports various compression encodings optimized for different data types and patterns to reduce storage and improve I/O performance.

**Encoding Types:**
- **RAW**: No compression
- **BYTEDICT**: Dictionary encoding for low-cardinality strings
- **DELTA**: Stores differences between consecutive values
- **DELTA32K**: Delta encoding for larger ranges
- **LZO**: General-purpose compression
- **RUNLENGTH**: For columns with many repeated values
- **TEXT255/TEXT32K**: Optimized text compression
- **ZSTD**: High compression ratio encoding

```sql
-- Create table with explicit encoding
CREATE TABLE optimized_sales (
    sale_id BIGINT IDENTITY(1,1),
    customer_id INTEGER ENCODE DELTA,
    product_id INTEGER ENCODE DELTA32K,
    sale_date DATE ENCODE DELTA32K,
    quantity INTEGER ENCODE DELTA32K,
    unit_price DECIMAL(10,2) ENCODE DELTA32K,
    total_amount DECIMAL(12,2) ENCODE DELTA32K,
    status VARCHAR(20) ENCODE BYTEDICT,
    created_at TIMESTAMP ENCODE DELTA32K
)
DISTSTYLE KEY
DISTKEY (customer_id)
SORTKEY (sale_date, customer_id);

-- Analyze compression recommendations
ANALYZE COMPRESSION analytics.fact_sales;

-- Check current compression ratios
SELECT 
    schemaname,
    tablename,
    column_name,
    type,
    encoding,
    size,
    size_raw,
    compression_ratio
FROM pg_table_def 
WHERE schemaname = 'analytics'
AND compression_ratio > 1
ORDER BY compression_ratio DESC;
```

### Q7: How do you handle data types in Redshift?

**Answer:**
Redshift supports standard SQL data types with some specific considerations for optimal performance and storage efficiency.

**Key Data Types:**
- **SMALLINT**: 2 bytes, -32,768 to 32,767
- **INTEGER**: 4 bytes, -2,147,483,648 to 2,147,483,647
- **BIGINT**: 8 bytes, large integers
- **DECIMAL(p,s)**: Exact numeric with precision and scale
- **REAL**: 4-byte floating point
- **DOUBLE PRECISION**: 8-byte floating point
- **BOOLEAN**: True/false values
- **CHAR(n)**: Fixed-length character string
- **VARCHAR(n)**: Variable-length character string
- **DATE**: Date values
- **TIMESTAMP**: Date and time values
- **TIMESTAMPTZ**: Timestamp with timezone

```sql
-- Optimal data type selection
CREATE TABLE customer_data (
    customer_id INTEGER,                    -- Use INTEGER instead of BIGINT if range sufficient
    first_name VARCHAR(50),                 -- Specify length instead of generic VARCHAR
    last_name VARCHAR(50),
    email VARCHAR(100),
    birth_date DATE,                        -- Use DATE instead of TIMESTAMP if time not needed
    registration_timestamp TIMESTAMP,       -- Use TIMESTAMP for date/time
    is_active BOOLEAN,                      -- Use BOOLEAN for true/false
    credit_score SMALLINT,                  -- Use SMALLINT for small ranges
    account_balance DECIMAL(12,2),          -- Use DECIMAL for exact monetary values
    last_login TIMESTAMPTZ                  -- Use TIMESTAMPTZ when timezone matters
);

-- Data type conversion examples
SELECT 
    customer_id::VARCHAR as customer_id_str,
    birth_date::TIMESTAMP as birth_timestamp,
    account_balance::REAL as balance_float,
    CAST(credit_score AS VARCHAR) as score_str
FROM customer_data;

-- Check data type information
SELECT 
    column_name,
    data_type,
    character_maximum_length,
    numeric_precision,
    numeric_scale
FROM information_schema.columns
WHERE table_name = 'customer_data'
ORDER BY ordinal_position;
```

### Q8: What is Redshift Spectrum and when would you use it?

**Answer:**
Redshift Spectrum allows querying data directly in S3 without loading it into Redshift, extending the cluster with virtually unlimited storage for data lake analytics.

**Use Cases:**
- **Data Lake Queries**: Query data stored in S3 data lakes
- **Cost Optimization**: Avoid loading infrequently accessed data
- **Data Archival**: Query historical data stored in S3
- **Mixed Workloads**: Combine Redshift and S3 data in single queries

```sql
-- Create external schema for Spectrum
CREATE EXTERNAL SCHEMA spectrum_schema
FROM DATA CATALOG
DATABASE 'data_lake_db'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftSpectrumRole'
CREATE EXTERNAL DATABASE IF NOT EXISTS;

-- Create external table for S3 data
CREATE EXTERNAL TABLE spectrum_schema.external_logs (
    timestamp TIMESTAMP,
    user_id INTEGER,
    session_id VARCHAR(50),
    event_type VARCHAR(50),
    page_url VARCHAR(500)
)
STORED AS PARQUET
LOCATION 's3://company-data-lake/logs/year=2023/'
TABLE PROPERTIES ('has_encrypted_data'='false');

-- Query combining Redshift and Spectrum data
SELECT 
    c.customer_name,
    ext.total_external_events,
    int.total_internal_sales
FROM analytics.dim_customers c
LEFT JOIN (
    SELECT 
        user_id,
        COUNT(*) as total_external_events
    FROM spectrum_schema.external_logs
    WHERE timestamp >= '2023-01-01'
    GROUP BY user_id
) ext ON c.customer_id = ext.user_id
LEFT JOIN (
    SELECT 
        customer_id,
        SUM(total_amount) as total_internal_sales
    FROM analytics.fact_sales
    WHERE sale_date >= '2023-01-01'
    GROUP BY customer_id
) int ON c.customer_id = int.customer_id;
```

### Q9: How do you implement basic security in Redshift?

**Answer:**
Redshift provides multiple layers of security including encryption, access control, network security, and audit logging.

```sql
-- User management
CREATE USER analyst_user PASSWORD 'SecurePassword123!' 
CREATE_DB FALSE
CREATE_USER FALSE;

CREATE USER etl_service_user PASSWORD 'ETLServicePassword456!';

-- Group management
CREATE GROUP analysts;
CREATE GROUP etl_users;

ALTER GROUP analysts ADD USER analyst_user;
ALTER GROUP etl_users ADD USER etl_service_user;

-- Schema permissions
GRANT USAGE ON SCHEMA analytics TO GROUP analysts;
GRANT SELECT ON ALL TABLES IN SCHEMA analytics TO GROUP analysts;

-- Table-level permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON analytics.fact_sales TO GROUP etl_users;

-- Monitor user activity
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

-- Check failed login attempts
SELECT 
    event,
    recordtime,
    username,
    remotehost
FROM stl_userlog
WHERE event = 'authentication failure'
AND recordtime >= DATEADD(day, -1, GETDATE());
```

### Q10: What are the maintenance operations required for Redshift?

**Answer:**
Regular maintenance operations are essential for optimal Redshift performance, including VACUUM, ANALYZE, and monitoring table statistics.

```sql
-- VACUUM operations
VACUUM REINDEX analytics.fact_sales;  -- Full vacuum with reindex
VACUUM DELETE ONLY analytics.fact_sales;  -- Reclaim deleted space only
VACUUM SORT ONLY analytics.fact_sales;  -- Sort data only

-- ANALYZE operations
ANALYZE analytics.fact_sales;  -- Update statistics for one table
ANALYZE;  -- Update statistics for all tables

-- Check tables needing maintenance
SELECT 
    schemaname,
    tablename,
    size_mb,
    pct_used,
    empty,
    unsorted,
    vacuum_sort_benefit
FROM svv_table_info
WHERE vacuum_sort_benefit > 5  -- Tables that would benefit from VACUUM
ORDER BY vacuum_sort_benefit DESC;

-- Monitor table statistics freshness
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    most_common_vals,
    histogram_bounds,
    last_analyze
FROM pg_stats 
WHERE schemaname = 'analytics'
AND last_analyze < DATEADD(day, -7, GETDATE());  -- Statistics older than 7 days
```
## Intermediate Level Questions (3-5 years experience)

### Q11: How do you implement and optimize Workload Management (WLM) in Redshift?

**Answer:**
WLM controls query execution by managing memory allocation, concurrency, and query prioritization. Proper WLM configuration ensures optimal resource utilization and query performance.

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

-- Set query group for session
SET query_group TO 'etl';

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
```

### Q12: How do you implement Change Data Capture (CDC) patterns in Redshift?

**Answer:**
CDC captures and applies incremental changes from source systems. Common patterns include timestamp-based, log-based, and snapshot comparison approaches.

```sql
-- Timestamp-based CDC implementation
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

-- CDC processing procedure
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
    
    -- Mark existing records as not current for updated records
    UPDATE analytics.cdc_customers 
    SET is_current = FALSE
    WHERE customer_id IN (
        SELECT customer_id FROM staging_customer_changes
        WHERE cdc_operation = 'UPDATE'
    )
    AND is_current = TRUE;
    
    -- Insert new CDC records
    INSERT INTO analytics.cdc_customers (
        customer_id, first_name, last_name, email, status,
        created_at, updated_at, cdc_operation, cdc_timestamp, is_current
    )
    SELECT 
        customer_id, first_name, last_name, email, status,
        created_at, updated_at, cdc_operation, current_time, TRUE
    FROM staging_customer_changes;
    
END;
$$ LANGUAGE plpgsql;
```

### Q13: How do you optimize complex analytical queries in Redshift?

**Answer:**
Query optimization involves understanding execution plans, using appropriate joins, leveraging distribution keys, and implementing proper indexing strategies through sort keys.

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
SELECT 
    customer_id,
    sale_date,
    sale_amount,
    AVG(sale_amount) OVER (PARTITION BY customer_id) as avg_customer_spend,
    COUNT(*) OVER (PARTITION BY customer_id) as customer_order_count,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY sale_date DESC) as recency_rank
FROM fact_sales;
```

### Q14: How do you implement data quality checks and validation in Redshift?

**Answer:**
Data quality checks ensure data integrity and consistency through validation rules, constraint checking, and automated monitoring.

```sql
-- Data quality framework
CREATE TABLE audit.data_quality_issues (
    check_id BIGINT IDENTITY(1,1),
    issue_type VARCHAR(50),
    table_name VARCHAR(100),
    column_name VARCHAR(100),
    issue_count INTEGER,
    issue_description TEXT,
    check_date TIMESTAMP DEFAULT GETDATE(),
    severity VARCHAR(20)
);

-- Data quality checks procedure
CREATE OR REPLACE PROCEDURE run_data_quality_checks()
AS $$
BEGIN
    -- Check for null values in critical columns
    INSERT INTO audit.data_quality_issues (issue_type, table_name, column_name, issue_count, issue_description, severity)
    SELECT 
        'NULL_VALUES' as issue_type,
        'fact_sales' as table_name,
        'customer_id' as column_name,
        SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) as issue_count,
        'Critical column contains null values' as issue_description,
        'HIGH' as severity
    FROM fact_sales
    HAVING SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) > 0;
    
    -- Check for duplicate records
    INSERT INTO audit.data_quality_issues (issue_type, table_name, issue_count, issue_description, severity)
    SELECT 
        'DUPLICATE_RECORDS' as issue_type,
        'fact_sales' as table_name,
        COUNT(*) - COUNT(DISTINCT sale_id) as issue_count,
        'Duplicate sale_id values found' as issue_description,
        'MEDIUM' as severity
    FROM fact_sales
    HAVING COUNT(*) - COUNT(DISTINCT sale_id) > 0;
    
    -- Check for orphaned records
    INSERT INTO audit.data_quality_issues (issue_type, table_name, issue_count, issue_description, severity)
    SELECT 
        'ORPHANED_RECORDS' as issue_type,
        'fact_sales' as table_name,
        COUNT(*) as issue_count,
        'Sales records without corresponding customer' as issue_description,
        'HIGH' as severity
    FROM fact_sales f
    LEFT JOIN dim_customers c ON f.customer_id = c.customer_id
    WHERE c.customer_id IS NULL
    HAVING COUNT(*) > 0;
    
    -- Check data freshness
    INSERT INTO audit.data_quality_issues (issue_type, table_name, issue_count, issue_description, severity)
    SELECT 
        'DATA_FRESHNESS' as issue_type,
        'fact_sales' as table_name,
        DATEDIFF(day, MAX(sale_date), CURRENT_DATE) as issue_count,
        'Data is older than expected' as issue_description,
        'MEDIUM' as severity
    FROM fact_sales
    HAVING DATEDIFF(day, MAX(sale_date), CURRENT_DATE) > 2;
    
    -- Check value ranges
    INSERT INTO audit.data_quality_issues (issue_type, table_name, column_name, issue_count, issue_description, severity)
    SELECT 
        'INVALID_RANGE' as issue_type,
        'fact_sales' as table_name,
        'total_amount' as column_name,
        SUM(CASE WHEN total_amount <= 0 OR total_amount > 100000 THEN 1 ELSE 0 END) as issue_count,
        'Total amount outside expected range' as issue_description,
        'MEDIUM' as severity
    FROM fact_sales
    HAVING SUM(CASE WHEN total_amount <= 0 OR total_amount > 100000 THEN 1 ELSE 0 END) > 0;
    
END;
$$ LANGUAGE plpgsql;

-- Run data quality checks
CALL run_data_quality_checks();

-- View data quality issues
SELECT 
    issue_type,
    table_name,
    column_name,
    issue_count,
    issue_description,
    severity,
    check_date
FROM audit.data_quality_issues
WHERE check_date >= DATEADD(day, -1, GETDATE())
ORDER BY severity DESC, issue_count DESC;
```

### Q15: How do you implement disaster recovery and backup strategies for Redshift?

**Answer:**
Redshift disaster recovery involves automated snapshots, cross-region replication, and recovery procedures. Strategies include point-in-time recovery and cluster restoration.

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

-- Recovery testing queries
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
```
## Advanced Level Questions (5+ years experience)

### Q16: How do you implement a complete data warehouse solution using Redshift?

**Answer:**
A complete Redshift data warehouse involves dimensional modeling, ETL processes, data quality checks, and performance optimization. Implementation includes staging, transformation, and serving layers.

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

-- 5. ETL procedures
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
```

### Q17: How do you implement advanced performance tuning and optimization?

**Answer:**
Advanced performance tuning involves deep analysis of query patterns, workload characteristics, and system resource utilization to optimize for specific use cases.

```sql
-- Advanced performance optimization strategies

-- 1. Workload-specific table design
CREATE TABLE fact_sales_optimized (
    sale_id BIGINT IDENTITY(1,1),
    customer_id INTEGER NOT NULL ENCODE DELTA,
    product_id INTEGER NOT NULL ENCODE DELTA32K,
    store_id INTEGER NOT NULL ENCODE DELTA32K,
    sale_date DATE NOT NULL ENCODE DELTA32K,
    quantity INTEGER NOT NULL ENCODE DELTA32K,
    unit_price DECIMAL(10,2) NOT NULL ENCODE DELTA32K,
    total_amount DECIMAL(12,2) NOT NULL ENCODE DELTA32K,
    created_at TIMESTAMP ENCODE DELTA32K
)
DISTSTYLE KEY
DISTKEY (customer_id)
COMPOUND SORTKEY (sale_date, store_id, customer_id);

-- 2. Advanced query optimization patterns
-- Materialized view for common aggregations
CREATE MATERIALIZED VIEW mv_monthly_sales AS
SELECT 
    DATE_TRUNC('month', sale_date) as month,
    store_id,
    product_category,
    SUM(total_amount) as total_revenue,
    COUNT(*) as transaction_count,
    COUNT(DISTINCT customer_id) as unique_customers
FROM fact_sales s
JOIN dim_products p ON s.product_id = p.product_id
GROUP BY DATE_TRUNC('month', sale_date), store_id, product_category;

-- 3. Advanced concurrency scaling configuration
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

-- 4. Query result caching optimization
-- Analyze cache hit rates
SELECT 
    DATE_TRUNC('hour', starttime) as hour,
    COUNT(*) as total_queries,
    SUM(CASE WHEN from_cache = 't' THEN 1 ELSE 0 END) as cached_queries,
    (SUM(CASE WHEN from_cache = 't' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as cache_hit_rate
FROM stl_query
WHERE starttime >= DATEADD(day, -1, GETDATE())
AND userid > 1
GROUP BY DATE_TRUNC('hour', starttime)
ORDER BY hour;

-- 5. Advanced monitoring and alerting
CREATE OR REPLACE PROCEDURE monitor_cluster_performance()
AS $$
BEGIN
    -- Check for long-running queries
    INSERT INTO audit.performance_alerts (alert_type, message, severity, alert_time)
    SELECT 
        'LONG_RUNNING_QUERY',
        'Query ' || query || ' has been running for ' || 
        DATEDIFF(minutes, starttime, GETDATE()) || ' minutes',
        'HIGH',
        GETDATE()
    FROM stl_query
    WHERE endtime IS NULL
    AND starttime < DATEADD(minutes, -30, GETDATE())
    AND userid > 1;
    
    -- Check for high queue wait times
    INSERT INTO audit.performance_alerts (alert_type, message, severity, alert_time)
    SELECT 
        'HIGH_QUEUE_WAIT',
        'Service class ' || service_class || ' has average queue time of ' || 
        avg_queue_time || ' seconds',
        'MEDIUM',
        GETDATE()
    FROM stv_wlm_service_class_state
    WHERE avg_queue_time > 60000  -- 1 minute in microseconds
    AND service_class > 4;
    
    -- Check for storage utilization
    INSERT INTO audit.performance_alerts (alert_type, message, severity, alert_time)
    SELECT 
        'HIGH_STORAGE_USAGE',
        'Schema ' || schemaname || ' is using ' || 
        ROUND(SUM(size) / 1024.0, 2) || ' GB of storage',
        'LOW',
        GETDATE()
    FROM svv_table_info
    WHERE schemaname NOT IN ('information_schema', 'pg_catalog')
    GROUP BY schemaname
    HAVING SUM(size) > 1024 * 100;  -- > 100 GB
    
END;
$$ LANGUAGE plpgsql;
```

### Q18: How do you implement complex data integration patterns with external systems?

**Answer:**
Complex data integration involves multiple data sources, transformation patterns, and real-time/batch processing combinations using various AWS services and third-party tools.

```sql
-- Complex data integration architecture

-- 1. Multi-source data integration
-- External table for S3 data lake
CREATE EXTERNAL SCHEMA data_lake
FROM DATA CATALOG
DATABASE 'enterprise_data_lake'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftSpectrumRole';

-- Federated query to RDS
CREATE EXTERNAL SCHEMA operational_db
FROM POSTGRES
DATABASE 'production_db'
URI 'prod-db.cluster-xyz.us-east-1.rds.amazonaws.com'
PORT 5432
USER 'redshift_user'
PASSWORD 'secure_password'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftFederatedRole';

-- 2. Complex transformation pipeline
CREATE OR REPLACE PROCEDURE process_multi_source_data()
AS $$
BEGIN
    -- Stage 1: Load from multiple sources
    CREATE TEMP TABLE staging_combined AS
    SELECT 
        'S3' as source,
        customer_id,
        event_timestamp,
        event_type,
        event_value
    FROM data_lake.customer_events
    WHERE event_timestamp >= DATEADD(hour, -1, GETDATE())
    
    UNION ALL
    
    SELECT 
        'RDS' as source,
        customer_id,
        transaction_timestamp as event_timestamp,
        'TRANSACTION' as event_type,
        transaction_amount as event_value
    FROM operational_db.transactions
    WHERE transaction_timestamp >= DATEADD(hour, -1, GETDATE())
    
    UNION ALL
    
    SELECT 
        'REDSHIFT' as source,
        customer_id,
        created_at as event_timestamp,
        'INTERNAL_EVENT' as event_type,
        metric_value as event_value
    FROM analytics.customer_metrics
    WHERE created_at >= DATEADD(hour, -1, GETDATE());
    
    -- Stage 2: Data quality and enrichment
    CREATE TEMP TABLE enriched_data AS
    SELECT 
        sc.source,
        sc.customer_id,
        sc.event_timestamp,
        sc.event_type,
        sc.event_value,
        c.customer_segment,
        c.customer_tier,
        CASE 
            WHEN sc.event_value > 1000 THEN 'HIGH_VALUE'
            WHEN sc.event_value > 100 THEN 'MEDIUM_VALUE'
            ELSE 'LOW_VALUE'
        END as value_category
    FROM staging_combined sc
    JOIN dimensions.dim_customers c ON sc.customer_id = c.customer_id
    WHERE c.is_current = TRUE
    AND sc.event_value IS NOT NULL
    AND sc.customer_id IS NOT NULL;
    
    -- Stage 3: Load to target tables
    INSERT INTO facts.fact_customer_events (
        customer_key, event_date_key, event_type, event_value, 
        value_category, source_system, created_date
    )
    SELECT 
        c.customer_key,
        d.date_key,
        ed.event_type,
        ed.event_value,
        ed.value_category,
        ed.source,
        GETDATE()
    FROM enriched_data ed
    JOIN dimensions.dim_customers c ON ed.customer_id = c.customer_id AND c.is_current = TRUE
    JOIN dimensions.dim_date d ON ed.event_timestamp::DATE = d.date_value;
    
    -- Stage 4: Update aggregated metrics
    DELETE FROM marts.customer_daily_summary
    WHERE summary_date = CURRENT_DATE;
    
    INSERT INTO marts.customer_daily_summary (
        customer_id, summary_date, total_events, total_value, 
        high_value_events, data_sources, last_updated
    )
    SELECT 
        customer_id,
        event_timestamp::DATE as summary_date,
        COUNT(*) as total_events,
        SUM(event_value) as total_value,
        SUM(CASE WHEN value_category = 'HIGH_VALUE' THEN 1 ELSE 0 END) as high_value_events,
        LISTAGG(DISTINCT source, ',') as data_sources,
        GETDATE()
    FROM enriched_data
    WHERE event_timestamp::DATE = CURRENT_DATE
    GROUP BY customer_id, event_timestamp::DATE;
    
    -- Log processing results
    INSERT INTO audit.integration_log (
        process_name, records_processed, sources_processed, 
        execution_time, status
    )
    SELECT 
        'MULTI_SOURCE_INTEGRATION',
        COUNT(*),
        COUNT(DISTINCT source),
        GETDATE(),
        'SUCCESS'
    FROM enriched_data;
    
END;
$$ LANGUAGE plpgsql;
```

### Q19: How do you implement advanced security and compliance patterns?

**Answer:**
Advanced security involves comprehensive access control, data encryption, audit logging, and compliance with regulations like GDPR, HIPAA, and SOX.

```sql
-- Advanced security implementation

-- 1. Role-based access control with hierarchy
CREATE ROLE data_analyst;
CREATE ROLE senior_analyst;
CREATE ROLE data_engineer;
CREATE ROLE data_architect;

-- Grant role hierarchy
GRANT data_analyst TO senior_analyst;
GRANT senior_analyst TO data_engineer;
GRANT data_engineer TO data_architect;

-- Schema-level security
GRANT USAGE ON SCHEMA analytics TO ROLE data_analyst;
GRANT USAGE ON SCHEMA staging TO ROLE data_engineer;
GRANT ALL ON SCHEMA raw_data TO ROLE data_architect;

-- 2. Row-level security implementation
CREATE TABLE customer_data_secure (
    customer_id INTEGER,
    customer_name VARCHAR(100),
    region VARCHAR(50),
    sensitive_data VARCHAR(500),
    data_classification VARCHAR(20)
);

-- Create security policy views
CREATE VIEW customer_data_analyst_view AS
SELECT 
    customer_id,
    customer_name,
    region,
    'REDACTED' as sensitive_data,
    data_classification
FROM customer_data_secure
WHERE region IN (
    SELECT region FROM user_region_access 
    WHERE username = CURRENT_USER
);

-- 3. Data masking for PII
CREATE OR REPLACE FUNCTION mask_pii(input_value VARCHAR, mask_type VARCHAR)
RETURNS VARCHAR
IMMUTABLE
AS $$
BEGIN
    RETURN CASE mask_type
        WHEN 'EMAIL' THEN 
            SUBSTRING(input_value, 1, 2) || '***@' || 
            SPLIT_PART(input_value, '@', 2)
        WHEN 'PHONE' THEN 
            'XXX-XXX-' || RIGHT(input_value, 4)
        WHEN 'SSN' THEN 
            'XXX-XX-' || RIGHT(input_value, 4)
        WHEN 'CREDIT_CARD' THEN 
            'XXXX-XXXX-XXXX-' || RIGHT(input_value, 4)
        ELSE 'REDACTED'
    END;
END;
$$ LANGUAGE plpgsql;

-- Apply masking in views
CREATE VIEW customer_pii_masked AS
SELECT 
    customer_id,
    first_name,
    last_name,
    mask_pii(email, 'EMAIL') as email,
    mask_pii(phone, 'PHONE') as phone,
    mask_pii(ssn, 'SSN') as ssn
FROM customer_pii_raw;

-- 4. Comprehensive audit logging
CREATE TABLE audit.access_log (
    log_id BIGINT IDENTITY(1,1),
    username VARCHAR(50),
    table_accessed VARCHAR(100),
    action_type VARCHAR(20),
    row_count INTEGER,
    access_timestamp TIMESTAMP DEFAULT GETDATE(),
    session_id VARCHAR(100),
    client_ip VARCHAR(15),
    query_hash VARCHAR(64)
);

-- Audit trigger function
CREATE OR REPLACE FUNCTION log_table_access()
RETURNS TRIGGER
AS $$
BEGIN
    INSERT INTO audit.access_log (
        username, table_accessed, action_type, row_count, 
        session_id, client_ip, query_hash
    )
    VALUES (
        CURRENT_USER,
        TG_TABLE_NAME,
        TG_OP,
        CASE TG_OP 
            WHEN 'INSERT' THEN 1
            WHEN 'UPDATE' THEN 1
            WHEN 'DELETE' THEN 1
            ELSE 0
        END,
        PG_BACKEND_PID()::VARCHAR,
        INET_CLIENT_ADDR()::VARCHAR,
        MD5(CURRENT_QUERY())
    );
    
    RETURN CASE TG_OP
        WHEN 'DELETE' THEN OLD
        ELSE NEW
    END;
END;
$$ LANGUAGE plpgsql;

-- 5. Compliance reporting
CREATE OR REPLACE PROCEDURE generate_compliance_report(report_type VARCHAR)
AS $$
BEGIN
    IF report_type = 'GDPR_ACCESS' THEN
        -- GDPR Article 15 - Right of access
        CREATE TEMP TABLE gdpr_access_report AS
        SELECT 
            'CUSTOMER_DATA' as data_category,
            customer_id,
            'Personal identification' as data_type,
            first_name || ' ' || last_name as data_value,
            created_date as collection_date,
            'Legitimate interest' as legal_basis
        FROM dim_customers
        WHERE customer_id = :customer_id
        
        UNION ALL
        
        SELECT 
            'TRANSACTION_DATA',
            customer_id,
            'Financial transaction',
            'Transaction amount: ' || total_amount::VARCHAR,
            sale_date,
            'Contract performance'
        FROM fact_sales
        WHERE customer_id = :customer_id;
        
    ELSIF report_type = 'DATA_LINEAGE' THEN
        -- Track data lineage for compliance
        CREATE TEMP TABLE data_lineage_report AS
        SELECT 
            table_name,
            source_system,
            transformation_applied,
            data_quality_checks,
            last_updated,
            retention_period
        FROM audit.data_lineage
        WHERE table_name LIKE '%customer%';
        
    END IF;
END;
$$ LANGUAGE plpgsql;
```

### Q20: How do you implement real-time analytics and streaming integration?

**Answer:**
Real-time analytics in Redshift involves integration with streaming services like Kinesis, implementing micro-batch processing, and optimizing for low-latency queries.

```sql
-- Real-time analytics implementation

-- 1. Streaming data ingestion setup
-- Create staging table for streaming data
CREATE TABLE streaming.kinesis_events (
    event_id VARCHAR(50),
    customer_id INTEGER,
    event_type VARCHAR(50),
    event_timestamp TIMESTAMP,
    event_data VARCHAR(65535),
    partition_key VARCHAR(50),
    shard_id VARCHAR(50),
    sequence_number VARCHAR(50),
    ingestion_time TIMESTAMP DEFAULT GETDATE()
)
DISTSTYLE KEY
DISTKEY (customer_id)
SORTKEY (event_timestamp, ingestion_time);

-- 2. Micro-batch processing procedure
CREATE OR REPLACE PROCEDURE process_streaming_batch()
AS $$
DECLARE
    batch_start_time TIMESTAMP;
    batch_end_time TIMESTAMP;
    processed_count INTEGER;
BEGIN
    -- Define batch window (last 5 minutes)
    batch_end_time := GETDATE();
    batch_start_time := batch_end_time - INTERVAL '5 minutes';
    
    -- Process events in micro-batch
    CREATE TEMP TABLE current_batch AS
    SELECT 
        event_id,
        customer_id,
        event_type,
        event_timestamp,
        JSON_EXTRACT_PATH_TEXT(event_data, 'value') as event_value,
        JSON_EXTRACT_PATH_TEXT(event_data, 'category') as event_category
    FROM streaming.kinesis_events
    WHERE ingestion_time >= batch_start_time
    AND ingestion_time < batch_end_time
    AND event_id NOT IN (
        SELECT event_id FROM analytics.processed_events 
        WHERE processed_date >= batch_start_time - INTERVAL '1 hour'
    );
    
    -- Real-time aggregations
    INSERT INTO analytics.real_time_metrics (
        metric_timestamp, customer_id, event_type, 
        event_count, total_value, avg_value, max_value
    )
    SELECT 
        DATE_TRUNC('minute', event_timestamp) as metric_timestamp,
        customer_id,
        event_type,
        COUNT(*) as event_count,
        SUM(event_value::DECIMAL) as total_value,
        AVG(event_value::DECIMAL) as avg_value,
        MAX(event_value::DECIMAL) as max_value
    FROM current_batch
    WHERE event_value IS NOT NULL
    GROUP BY DATE_TRUNC('minute', event_timestamp), customer_id, event_type;
    
    -- Update customer real-time profile
    INSERT INTO analytics.customer_real_time_profile (
        customer_id, last_activity, activity_score, 
        recent_events, profile_updated
    )
    SELECT 
        customer_id,
        MAX(event_timestamp) as last_activity,
        COUNT(*) * 10 + SUM(CASE WHEN event_type = 'HIGH_VALUE' THEN 5 ELSE 1 END) as activity_score,
        COUNT(*) as recent_events,
        GETDATE()
    FROM current_batch
    GROUP BY customer_id
    ON CONFLICT (customer_id) DO UPDATE SET
        last_activity = EXCLUDED.last_activity,
        activity_score = customer_real_time_profile.activity_score + EXCLUDED.activity_score,
        recent_events = customer_real_time_profile.recent_events + EXCLUDED.recent_events,
        profile_updated = EXCLUDED.profile_updated;
    
    -- Mark events as processed
    INSERT INTO analytics.processed_events (event_id, processed_date)
    SELECT event_id, GETDATE()
    FROM current_batch;
    
    GET DIAGNOSTICS processed_count = ROW_COUNT;
    
    -- Log batch processing
    INSERT INTO audit.streaming_batch_log (
        batch_start, batch_end, events_processed, 
        processing_duration, status
    )
    VALUES (
        batch_start_time,
        batch_end_time,
        processed_count,
        DATEDIFF(seconds, batch_start_time, GETDATE()),
        'SUCCESS'
    );
    
END;
$$ LANGUAGE plpgsql;

-- 3. Real-time dashboard queries
-- Low-latency customer activity view
CREATE MATERIALIZED VIEW mv_customer_activity_realtime AS
SELECT 
    customer_id,
    last_activity,
    activity_score,
    recent_events,
    CASE 
        WHEN last_activity >= GETDATE() - INTERVAL '5 minutes' THEN 'ACTIVE'
        WHEN last_activity >= GETDATE() - INTERVAL '1 hour' THEN 'RECENT'
        ELSE 'INACTIVE'
    END as activity_status
FROM analytics.customer_real_time_profile;

-- Real-time alerting
CREATE OR REPLACE PROCEDURE check_real_time_alerts()
AS $$
BEGIN
    -- High-value transaction alert
    INSERT INTO alerts.real_time_alerts (alert_type, customer_id, alert_message, severity)
    SELECT 
        'HIGH_VALUE_TRANSACTION',
        customer_id,
        'Customer ' || customer_id || ' has ' || event_count || ' high-value events in last minute',
        'HIGH'
    FROM analytics.real_time_metrics
    WHERE metric_timestamp >= GETDATE() - INTERVAL '1 minute'
    AND event_type = 'HIGH_VALUE'
    AND event_count >= 5;
    
    -- Unusual activity pattern
    INSERT INTO alerts.real_time_alerts (alert_type, customer_id, alert_message, severity)
    SELECT 
        'UNUSUAL_ACTIVITY',
        customer_id,
        'Customer activity score increased by ' || (activity_score - prev_score) || ' in last 5 minutes',
        'MEDIUM'
    FROM (
        SELECT 
            customer_id,
            activity_score,
            LAG(activity_score) OVER (PARTITION BY customer_id ORDER BY profile_updated) as prev_score
        FROM analytics.customer_real_time_profile
        WHERE profile_updated >= GETDATE() - INTERVAL '5 minutes'
    ) activity_changes
    WHERE (activity_score - prev_score) > 100;
    
END;
$$ LANGUAGE plpgsql;
```
## Architecture & Performance

### Q21: How do you design optimal table structures for different query patterns?

**Answer:**
Table design should align with query patterns, considering distribution keys, sort keys, and compression based on access patterns and join requirements.

```sql
-- Query pattern analysis
SELECT 
    schemaname,
    tablename,
    diststyle,
    distkey,
    sortkey1,
    size_mb,
    skew_rows,
    pct_used
FROM svv_table_info 
WHERE schemaname = 'analytics'
ORDER BY size_mb DESC;

-- Design patterns for different use cases

-- 1. OLAP Star Schema - Fact table
CREATE TABLE facts.fact_sales_optimized (
    sale_id BIGINT IDENTITY(1,1),
    customer_key BIGINT NOT NULL,
    product_key BIGINT NOT NULL,
    date_key INTEGER NOT NULL,
    store_key INTEGER NOT NULL,
    quantity INTEGER ENCODE DELTA32K,
    unit_price DECIMAL(10,2) ENCODE DELTA32K,
    total_amount DECIMAL(12,2) ENCODE DELTA32K,
    discount_amount DECIMAL(10,2) ENCODE DELTA32K
)
DISTSTYLE KEY
DISTKEY (customer_key)  -- Most common join dimension
COMPOUND SORTKEY (date_key, store_key, customer_key);  -- Query filter order

-- 2. Dimension table - small, replicated
CREATE TABLE dimensions.dim_products_optimized (
    product_key BIGINT IDENTITY(1,1) PRIMARY KEY,
    product_id INTEGER NOT NULL,
    product_name VARCHAR(255) ENCODE BYTEDICT,
    category VARCHAR(100) ENCODE BYTEDICT,
    subcategory VARCHAR(100) ENCODE BYTEDICT,
    brand VARCHAR(100) ENCODE BYTEDICT,
    unit_cost DECIMAL(10,2) ENCODE DELTA32K
)
DISTSTYLE ALL  -- Replicate to all nodes for fast joins
SORTKEY (product_id);

-- 3. Event/Log table - time-series pattern
CREATE TABLE events.user_events_optimized (
    event_id BIGINT IDENTITY(1,1),
    user_id INTEGER ENCODE DELTA,
    event_timestamp TIMESTAMP ENCODE DELTA32K,
    event_type VARCHAR(50) ENCODE BYTEDICT,
    session_id VARCHAR(50) ENCODE LZO,
    page_url VARCHAR(500) ENCODE LZO,
    user_agent VARCHAR(500) ENCODE LZO
)
DISTSTYLE KEY
DISTKEY (user_id)
SORTKEY (event_timestamp, user_id);  -- Time-based queries

-- Performance monitoring
SELECT 
    query,
    segment,
    step,
    max_time,
    avg_time,
    rows,
    bytes
FROM svl_query_summary 
WHERE query = pg_last_query_id()
ORDER BY segment, step;
```

### Q22: How do you implement and tune concurrency scaling?

**Answer:**
Concurrency scaling automatically adds cluster capacity during peak demand. Proper configuration and monitoring ensure cost-effective scaling.

```sql
-- Monitor concurrency scaling usage
SELECT 
    start_time,
    end_time,
    cluster_identifier,
    concurrency_scaling_cluster_identifier,
    usage_limit_breach,
    DATEDIFF(seconds, start_time, end_time) as duration_seconds
FROM stl_concurrency_scaling_usage
WHERE start_time >= DATEADD(day, -7, GETDATE())
ORDER BY start_time DESC;

-- Analyze scaling triggers
SELECT 
    DATE_TRUNC('hour', start_time) as hour,
    COUNT(*) as scaling_events,
    AVG(DATEDIFF(seconds, start_time, end_time)) as avg_duration_sec,
    SUM(CASE WHEN usage_limit_breach THEN 1 ELSE 0 END) as limit_breaches
FROM stl_concurrency_scaling_usage
WHERE start_time >= DATEADD(day, -30, GETDATE())
GROUP BY DATE_TRUNC('hour', start_time)
ORDER BY hour;

-- Query performance during scaling
SELECT 
    w.service_class,
    w.concurrency_scaling_status,
    COUNT(*) as query_count,
    AVG(w.total_exec_time) as avg_exec_time,
    AVG(w.total_queue_time) as avg_queue_time
FROM stl_wlm_query w
WHERE w.queue_start_time >= DATEADD(day, -1, GETDATE())
GROUP BY w.service_class, w.concurrency_scaling_status
ORDER BY w.service_class, w.concurrency_scaling_status;

-- Cost analysis for concurrency scaling
SELECT 
    DATE_TRUNC('day', start_time) as day,
    COUNT(*) as scaling_events,
    SUM(DATEDIFF(seconds, start_time, end_time)) / 3600.0 as total_hours,
    SUM(DATEDIFF(seconds, start_time, end_time)) / 3600.0 * 0.045 as estimated_cost_usd
FROM stl_concurrency_scaling_usage
WHERE start_time >= DATEADD(day, -30, GETDATE())
GROUP BY DATE_TRUNC('day', start_time)
ORDER BY day;
```

### Q23: How do you optimize join performance in complex queries?

**Answer:**
Join optimization involves proper distribution key selection, join order optimization, and understanding Redshift's join algorithms.

```sql
-- Join performance analysis
EXPLAIN (VERBOSE TRUE, COSTS TRUE)
SELECT 
    c.customer_name,
    p.product_name,
    s.store_name,
    SUM(f.total_amount) as total_sales
FROM fact_sales f
JOIN dim_customers c ON f.customer_key = c.customer_key
JOIN dim_products p ON f.product_key = p.product_key
JOIN dim_stores s ON f.store_key = s.store_key
WHERE f.date_key BETWEEN 20230101 AND 20231231
GROUP BY c.customer_name, p.product_name, s.store_name;

-- Optimized join patterns

-- 1. Co-located joins (same distribution key)
SELECT 
    c.customer_name,
    SUM(f.total_amount) as total_sales
FROM fact_sales f
JOIN dim_customers c ON f.customer_key = c.customer_key  -- Co-located join
WHERE f.date_key >= 20230101
GROUP BY c.customer_name;

-- 2. Broadcast joins (small dimension tables)
SELECT 
    p.product_name,
    COUNT(*) as sale_count
FROM fact_sales f
JOIN dim_products p ON f.product_key = p.product_key  -- Broadcast join (ALL distribution)
WHERE f.date_key >= 20230101
GROUP BY p.product_name;

-- 3. Join order optimization
-- Filter early, join late
SELECT 
    customer_summary.customer_name,
    product_summary.product_name,
    customer_summary.customer_sales,
    product_summary.product_sales
FROM (
    SELECT 
        c.customer_name,
        c.customer_key,
        SUM(f.total_amount) as customer_sales
    FROM fact_sales f
    JOIN dim_customers c ON f.customer_key = c.customer_key
    WHERE f.date_key >= 20230101
    AND c.customer_segment = 'Premium'
    GROUP BY c.customer_name, c.customer_key
) customer_summary
JOIN (
    SELECT 
        p.product_name,
        p.product_key,
        SUM(f.total_amount) as product_sales
    FROM fact_sales f
    JOIN dim_products p ON f.product_key = p.product_key
    WHERE f.date_key >= 20230101
    AND p.product_category = 'Electronics'
    GROUP BY p.product_name, p.product_key
) product_summary ON customer_summary.customer_key = product_summary.product_key;

-- Monitor join performance
SELECT 
    query,
    segment,
    step,
    label,
    max_time,
    avg_time,
    rows,
    bytes
FROM svl_query_summary 
WHERE query = pg_last_query_id()
AND label LIKE '%Join%'
ORDER BY segment, step;
```

## Streaming & Real-time Processing

### Q24: How do you implement near real-time data ingestion with Kinesis and Redshift?

**Answer:**
Near real-time ingestion combines Kinesis Data Firehose for streaming delivery and Lambda functions for micro-batch processing.

```sql
-- Real-time ingestion architecture

-- 1. Staging table for Kinesis data
CREATE TABLE streaming.kinesis_raw_events (
    record_id VARCHAR(100),
    event_timestamp TIMESTAMP,
    event_data VARCHAR(65535),
    kinesis_timestamp TIMESTAMP,
    shard_id VARCHAR(50),
    sequence_number VARCHAR(50),
    ingestion_time TIMESTAMP DEFAULT GETDATE()
)
DISTSTYLE EVEN
SORTKEY (event_timestamp, ingestion_time);

-- 2. Processed events table
CREATE TABLE streaming.processed_events (
    event_id BIGINT IDENTITY(1,1),
    customer_id INTEGER,
    event_type VARCHAR(50),
    event_timestamp TIMESTAMP,
    event_value DECIMAL(10,2),
    session_id VARCHAR(50),
    processed_time TIMESTAMP DEFAULT GETDATE()
)
DISTSTYLE KEY
DISTKEY (customer_id)
SORTKEY (event_timestamp, processed_time);

-- 3. Real-time processing procedure
CREATE OR REPLACE PROCEDURE process_kinesis_batch()
AS $$
DECLARE
    batch_size INTEGER := 10000;
    processed_count INTEGER;
BEGIN
    -- Process oldest unprocessed records
    CREATE TEMP TABLE current_batch AS
    SELECT 
        record_id,
        event_timestamp,
        event_data,
        ingestion_time
    FROM streaming.kinesis_raw_events
    WHERE record_id NOT IN (
        SELECT record_id FROM streaming.processing_log 
        WHERE status = 'PROCESSED'
    )
    ORDER BY ingestion_time
    LIMIT batch_size;
    
    -- Parse and transform JSON data
    INSERT INTO streaming.processed_events (
        customer_id, event_type, event_timestamp, event_value, session_id
    )
    SELECT 
        JSON_EXTRACT_PATH_TEXT(event_data, 'customer_id')::INTEGER,
        JSON_EXTRACT_PATH_TEXT(event_data, 'event_type'),
        JSON_EXTRACT_PATH_TEXT(event_data, 'timestamp')::TIMESTAMP,
        JSON_EXTRACT_PATH_TEXT(event_data, 'value')::DECIMAL(10,2),
        JSON_EXTRACT_PATH_TEXT(event_data, 'session_id')
    FROM current_batch
    WHERE JSON_EXTRACT_PATH_TEXT(event_data, 'customer_id') IS NOT NULL;
    
    GET DIAGNOSTICS processed_count = ROW_COUNT;
    
    -- Mark records as processed
    INSERT INTO streaming.processing_log (record_id, status, processed_time)
    SELECT record_id, 'PROCESSED', GETDATE()
    FROM current_batch;
    
    -- Update real-time aggregates
    INSERT INTO streaming.customer_metrics_realtime (
        customer_id, metric_timestamp, event_count, total_value
    )
    SELECT 
        customer_id,
        DATE_TRUNC('minute', event_timestamp) as metric_timestamp,
        COUNT(*) as event_count,
        SUM(event_value) as total_value
    FROM streaming.processed_events
    WHERE processed_time >= DATEADD(minutes, -5, GETDATE())
    GROUP BY customer_id, DATE_TRUNC('minute', event_timestamp)
    ON CONFLICT (customer_id, metric_timestamp) DO UPDATE SET
        event_count = customer_metrics_realtime.event_count + EXCLUDED.event_count,
        total_value = customer_metrics_realtime.total_value + EXCLUDED.total_value;
    
    -- Log processing results
    INSERT INTO streaming.batch_processing_log (
        batch_start, records_processed, processing_duration, status
    )
    VALUES (
        GETDATE() - INTERVAL '1 minute',
        processed_count,
        DATEDIFF(seconds, GETDATE() - INTERVAL '1 minute', GETDATE()),
        'SUCCESS'
    );
    
END;
$$ LANGUAGE plpgsql;

-- 4. Real-time monitoring queries
-- Stream processing lag
SELECT 
    MAX(ingestion_time) as latest_ingestion,
    MAX(processed_time) as latest_processing,
    DATEDIFF(seconds, MAX(processed_time), MAX(ingestion_time)) as processing_lag_sec
FROM streaming.kinesis_raw_events k
LEFT JOIN streaming.processing_log p ON k.record_id = p.record_id;

-- Throughput monitoring
SELECT 
    DATE_TRUNC('minute', processed_time) as minute,
    COUNT(*) as events_processed,
    COUNT(*) / 60.0 as events_per_second
FROM streaming.processed_events
WHERE processed_time >= DATEADD(hour, -1, GETDATE())
GROUP BY DATE_TRUNC('minute', processed_time)
ORDER BY minute;
```

### Q25: How do you handle late-arriving data and out-of-order events?

**Answer:**
Late-arriving data requires windowing strategies, watermarks, and reprocessing mechanisms to maintain data accuracy.

```sql
-- Late-arriving data handling

-- 1. Event tracking with watermarks
CREATE TABLE streaming.event_watermarks (
    partition_key VARCHAR(50),
    event_timestamp TIMESTAMP,
    watermark_timestamp TIMESTAMP,
    late_arrival_window_minutes INTEGER DEFAULT 60,
    updated_time TIMESTAMP DEFAULT GETDATE()
);

-- 2. Late event detection and handling
CREATE OR REPLACE PROCEDURE handle_late_events()
AS $$
BEGIN
    -- Identify late-arriving events
    CREATE TEMP TABLE late_events AS
    SELECT 
        pe.event_id,
        pe.customer_id,
        pe.event_timestamp,
        pe.processed_time,
        ew.watermark_timestamp,
        DATEDIFF(minutes, pe.event_timestamp, pe.processed_time) as arrival_delay_minutes
    FROM streaming.processed_events pe
    JOIN streaming.event_watermarks ew ON pe.customer_id::VARCHAR = ew.partition_key
    WHERE pe.processed_time >= DATEADD(hour, -1, GETDATE())
    AND pe.event_timestamp < ew.watermark_timestamp
    AND DATEDIFF(minutes, pe.event_timestamp, pe.processed_time) > ew.late_arrival_window_minutes;
    
    -- Reprocess affected aggregations
    DELETE FROM streaming.customer_metrics_realtime
    WHERE customer_id IN (SELECT customer_id FROM late_events)
    AND metric_timestamp >= (
        SELECT MIN(DATE_TRUNC('minute', event_timestamp)) 
        FROM late_events
    );
    
    -- Recalculate aggregations including late events
    INSERT INTO streaming.customer_metrics_realtime (
        customer_id, metric_timestamp, event_count, total_value, 
        contains_late_events, last_updated
    )
    SELECT 
        customer_id,
        DATE_TRUNC('minute', event_timestamp) as metric_timestamp,
        COUNT(*) as event_count,
        SUM(event_value) as total_value,
        TRUE as contains_late_events,
        GETDATE()
    FROM streaming.processed_events
    WHERE customer_id IN (SELECT customer_id FROM late_events)
    AND event_timestamp >= (
        SELECT MIN(DATE_TRUNC('minute', event_timestamp)) 
        FROM late_events
    )
    GROUP BY customer_id, DATE_TRUNC('minute', event_timestamp);
    
    -- Update watermarks
    UPDATE streaming.event_watermarks
    SET watermark_timestamp = GETDATE() - INTERVAL '60 minutes',
        updated_time = GETDATE()
    WHERE partition_key IN (
        SELECT customer_id::VARCHAR FROM late_events
    );
    
    -- Log late event handling
    INSERT INTO streaming.late_event_log (
        event_count, max_delay_minutes, reprocessed_windows, processing_time
    )
    SELECT 
        COUNT(*),
        MAX(arrival_delay_minutes),
        COUNT(DISTINCT DATE_TRUNC('minute', event_timestamp)),
        GETDATE()
    FROM late_events;
    
END;
$$ LANGUAGE plpgsql;

-- 3. Out-of-order event handling with session windows
CREATE OR REPLACE PROCEDURE process_session_windows()
AS $$
BEGIN
    -- Define session windows (30-minute inactivity gap)
    CREATE TEMP TABLE session_windows AS
    WITH ordered_events AS (
        SELECT 
            customer_id,
            event_timestamp,
            event_value,
            LAG(event_timestamp) OVER (
                PARTITION BY customer_id 
                ORDER BY event_timestamp
            ) as prev_event_time
        FROM streaming.processed_events
        WHERE processed_time >= DATEADD(hour, -2, GETDATE())
    ),
    session_boundaries AS (
        SELECT 
            customer_id,
            event_timestamp,
            event_value,
            CASE 
                WHEN prev_event_time IS NULL 
                     OR DATEDIFF(minutes, prev_event_time, event_timestamp) > 30 
                THEN 1 
                ELSE 0 
            END as is_session_start
        FROM ordered_events
    ),
    session_groups AS (
        SELECT 
            customer_id,
            event_timestamp,
            event_value,
            SUM(is_session_start) OVER (
                PARTITION BY customer_id 
                ORDER BY event_timestamp 
                ROWS UNBOUNDED PRECEDING
            ) as session_id
        FROM session_boundaries
    )
    SELECT 
        customer_id,
        session_id,
        MIN(event_timestamp) as session_start,
        MAX(event_timestamp) as session_end,
        COUNT(*) as event_count,
        SUM(event_value) as session_value
    FROM session_groups
    GROUP BY customer_id, session_id;
    
    -- Update session aggregates
    INSERT INTO streaming.customer_sessions (
        customer_id, session_start, session_end, event_count, 
        session_value, session_duration_minutes
    )
    SELECT 
        customer_id,
        session_start,
        session_end,
        event_count,
        session_value,
        DATEDIFF(minutes, session_start, session_end) as session_duration_minutes
    FROM session_windows
    ON CONFLICT (customer_id, session_start) DO UPDATE SET
        session_end = EXCLUDED.session_end,
        event_count = EXCLUDED.event_count,
        session_value = EXCLUDED.session_value,
        session_duration_minutes = EXCLUDED.session_duration_minutes;
    
END;
$$ LANGUAGE plpgsql;
```

## Production & Operations

### Q26: How do you implement comprehensive monitoring and alerting for Redshift?

**Answer:**
Production monitoring requires tracking cluster health, query performance, resource utilization, and automated alerting for issues.

```sql
-- Comprehensive monitoring framework

-- 1. Cluster health monitoring
CREATE TABLE monitoring.cluster_health_metrics (
    metric_timestamp TIMESTAMP DEFAULT GETDATE(),
    cluster_identifier VARCHAR(100),
    node_count INTEGER,
    cluster_status VARCHAR(50),
    cpu_utilization DECIMAL(5,2),
    storage_utilization DECIMAL(5,2),
    connection_count INTEGER,
    active_queries INTEGER,
    queued_queries INTEGER
);

-- Health check procedure
CREATE OR REPLACE PROCEDURE collect_cluster_metrics()
AS $$
BEGIN
    INSERT INTO monitoring.cluster_health_metrics (
        cluster_identifier, node_count, cluster_status,
        connection_count, active_queries, queued_queries
    )
    SELECT 
        'production-cluster',
        (SELECT COUNT(*) FROM stv_slices) / 2 as node_count,
        'available' as cluster_status,
        (SELECT COUNT(*) FROM stv_sessions WHERE user_name != 'rdsdb'),
        (SELECT COUNT(*) FROM stv_recents WHERE status = 'Running'),
        (SELECT SUM(num_queued_queries) FROM stv_wlm_service_class_state WHERE service_class > 4);
    
    -- Storage utilization by schema
    INSERT INTO monitoring.storage_metrics (
        schema_name, table_count, total_size_mb, 
        largest_table_mb, avg_table_size_mb
    )
    SELECT 
        schemaname,
        COUNT(*) as table_count,
        SUM(size) as total_size_mb,
        MAX(size) as largest_table_mb,
        AVG(size) as avg_table_size_mb
    FROM svv_table_info
    WHERE schemaname NOT IN ('information_schema', 'pg_catalog')
    GROUP BY schemaname;
    
END;
$$ LANGUAGE plpgsql;

-- 2. Query performance monitoring
CREATE TABLE monitoring.query_performance_metrics (
    metric_timestamp TIMESTAMP DEFAULT GETDATE(),
    query_type VARCHAR(50),
    avg_execution_time_sec DECIMAL(10,2),
    max_execution_time_sec DECIMAL(10,2),
    query_count INTEGER,
    failed_queries INTEGER,
    avg_queue_time_sec DECIMAL(10,2)
);

CREATE OR REPLACE PROCEDURE collect_query_metrics()
AS $$
BEGIN
    INSERT INTO monitoring.query_performance_metrics (
        query_type, avg_execution_time_sec, max_execution_time_sec,
        query_count, failed_queries, avg_queue_time_sec
    )
    SELECT 
        CASE 
            WHEN querytxt LIKE 'SELECT%' THEN 'SELECT'
            WHEN querytxt LIKE 'INSERT%' THEN 'INSERT'
            WHEN querytxt LIKE 'COPY%' THEN 'COPY'
            WHEN querytxt LIKE 'DELETE%' THEN 'DELETE'
            WHEN querytxt LIKE 'UPDATE%' THEN 'UPDATE'
            ELSE 'OTHER'
        END as query_type,
        AVG(DATEDIFF(seconds, starttime, endtime)) as avg_execution_time_sec,
        MAX(DATEDIFF(seconds, starttime, endtime)) as max_execution_time_sec,
        COUNT(*) as query_count,
        SUM(CASE WHEN aborted = 1 THEN 1 ELSE 0 END) as failed_queries,
        AVG(COALESCE(w.total_queue_time, 0) / 1000000.0) as avg_queue_time_sec
    FROM stl_query q
    LEFT JOIN stl_wlm_query w ON q.query = w.query
    WHERE q.starttime >= DATEADD(hour, -1, GETDATE())
    AND q.userid > 1
    GROUP BY CASE 
        WHEN querytxt LIKE 'SELECT%' THEN 'SELECT'
        WHEN querytxt LIKE 'INSERT%' THEN 'INSERT'
        WHEN querytxt LIKE 'COPY%' THEN 'COPY'
        WHEN querytxt LIKE 'DELETE%' THEN 'DELETE'
        WHEN querytxt LIKE 'UPDATE%' THEN 'UPDATE'
        ELSE 'OTHER'
    END;
END;
$$ LANGUAGE plpgsql;

-- 3. Automated alerting system
CREATE TABLE monitoring.alert_rules (
    rule_id INTEGER IDENTITY(1,1),
    rule_name VARCHAR(100),
    metric_type VARCHAR(50),
    threshold_value DECIMAL(10,2),
    comparison_operator VARCHAR(10),
    severity VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE
);

-- Insert alert rules
INSERT INTO monitoring.alert_rules (rule_name, metric_type, threshold_value, comparison_operator, severity)
VALUES 
('Long Running Query', 'query_duration_sec', 1800, '>', 'HIGH'),
('High Queue Wait Time', 'avg_queue_time_sec', 300, '>', 'MEDIUM'),
('Storage Utilization High', 'storage_utilization_pct', 85, '>', 'HIGH'),
('Failed Query Rate High', 'failed_query_rate_pct', 5, '>', 'MEDIUM'),
('Connection Count High', 'connection_count', 450, '>', 'LOW');

CREATE OR REPLACE PROCEDURE check_alert_conditions()
AS $$
BEGIN
    -- Check for long-running queries
    INSERT INTO monitoring.active_alerts (alert_type, message, severity, alert_time)
    SELECT 
        'LONG_RUNNING_QUERY',
        'Query ' || query || ' has been running for ' || 
        DATEDIFF(minutes, starttime, GETDATE()) || ' minutes',
        'HIGH',
        GETDATE()
    FROM stl_query
    WHERE endtime IS NULL
    AND starttime < DATEADD(minutes, -30, GETDATE())
    AND userid > 1;
    
    -- Check storage utilization
    INSERT INTO monitoring.active_alerts (alert_type, message, severity, alert_time)
    SELECT 
        'HIGH_STORAGE_USAGE',
        'Schema ' || schemaname || ' is using ' || 
        ROUND(SUM(size) / 1024.0, 2) || ' GB of storage',
        'MEDIUM',
        GETDATE()
    FROM svv_table_info
    WHERE schemaname NOT IN ('information_schema', 'pg_catalog')
    GROUP BY schemaname
    HAVING SUM(size) > 100 * 1024;  -- > 100 GB
    
    -- Check failed query rate
    INSERT INTO monitoring.active_alerts (alert_type, message, severity, alert_time)
    SELECT 
        'HIGH_FAILURE_RATE',
        'Failed query rate is ' || 
        ROUND((failed_queries * 100.0 / query_count), 2) || '%',
        'HIGH',
        GETDATE()
    FROM (
        SELECT 
            COUNT(*) as query_count,
            SUM(CASE WHEN aborted = 1 THEN 1 ELSE 0 END) as failed_queries
        FROM stl_query
        WHERE starttime >= DATEADD(hour, -1, GETDATE())
        AND userid > 1
    ) query_stats
    WHERE (failed_queries * 100.0 / query_count) > 5;
    
END;
$$ LANGUAGE plpgsql;
```

### Q27: How do you implement automated backup and recovery procedures?

**Answer:**
Automated backup and recovery involves scheduled snapshots, cross-region replication, and automated recovery testing.

```sql
-- Automated backup and recovery framework

-- 1. Backup scheduling and management
CREATE TABLE backup.backup_schedule (
    schedule_id INTEGER IDENTITY(1,1),
    backup_type VARCHAR(20), -- 'FULL', 'INCREMENTAL'
    schedule_expression VARCHAR(50), -- Cron expression
    retention_days INTEGER,
    cross_region_copy BOOLEAN DEFAULT FALSE,
    target_region VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE
);

-- Backup execution log
CREATE TABLE backup.backup_execution_log (
    execution_id BIGINT IDENTITY(1,1),
    backup_type VARCHAR(20),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    snapshot_id VARCHAR(100),
    status VARCHAR(20),
    error_message TEXT,
    data_size_gb DECIMAL(10,2),
    backup_duration_minutes INTEGER
);

-- Backup procedure
CREATE OR REPLACE PROCEDURE execute_backup(backup_type VARCHAR)
AS $$
DECLARE
    execution_id BIGINT;
    start_time TIMESTAMP := GETDATE();
    snapshot_identifier VARCHAR(100);
    total_size_gb DECIMAL(10,2);
BEGIN
    -- Generate unique snapshot identifier
    snapshot_identifier := 'auto-backup-' || backup_type || '-' || 
                           TO_CHAR(start_time, 'YYYY-MM-DD-HH24-MI-SS');
    
    -- Log backup start
    INSERT INTO backup.backup_execution_log (
        backup_type, start_time, status
    )
    VALUES (backup_type, start_time, 'STARTED')
    RETURNING execution_id INTO execution_id;
    
    -- Calculate total data size
    SELECT SUM(size) / 1024.0 INTO total_size_gb
    FROM svv_table_info
    WHERE schemaname NOT IN ('information_schema', 'pg_catalog');
    
    -- Pre-backup validation
    PERFORM run_backup_validation();
    
    -- Create snapshot (this would be done via AWS API in practice)
    -- aws redshift create-cluster-snapshot 
    --   --cluster-identifier production-cluster
    --   --snapshot-identifier snapshot_identifier
    
    -- Update execution log
    UPDATE backup.backup_execution_log
    SET end_time = GETDATE(),
        snapshot_id = snapshot_identifier,
        status = 'COMPLETED',
        data_size_gb = total_size_gb,
        backup_duration_minutes = DATEDIFF(minutes, start_time, GETDATE())
    WHERE execution_id = execution_id;
    
    -- Cross-region copy if configured
    IF EXISTS (SELECT 1 FROM backup.backup_schedule 
               WHERE backup_type = backup_type AND cross_region_copy = TRUE) THEN
        PERFORM copy_snapshot_cross_region(snapshot_identifier);
    END IF;
    
    -- Cleanup old snapshots
    PERFORM cleanup_old_snapshots(backup_type);
    
EXCEPTION
    WHEN OTHERS THEN
        UPDATE backup.backup_execution_log
        SET end_time = GETDATE(),
            status = 'FAILED',
            error_message = SQLERRM
        WHERE execution_id = execution_id;
        RAISE;
END;
$$ LANGUAGE plpgsql;

-- 2. Recovery procedures
CREATE TABLE backup.recovery_procedures (
    procedure_id INTEGER IDENTITY(1,1),
    procedure_name VARCHAR(100),
    recovery_type VARCHAR(50), -- 'FULL_RESTORE', 'POINT_IN_TIME', 'TABLE_RESTORE'
    estimated_duration_minutes INTEGER,
    prerequisites TEXT,
    procedure_steps TEXT
);

-- Recovery execution
CREATE OR REPLACE PROCEDURE execute_recovery(
    recovery_type VARCHAR,
    snapshot_id VARCHAR DEFAULT NULL,
    target_timestamp TIMESTAMP DEFAULT NULL
)
AS $$
DECLARE
    recovery_start_time TIMESTAMP := GETDATE();
    validation_results TEXT;
BEGIN
    -- Log recovery start
    INSERT INTO backup.recovery_execution_log (
        recovery_type, snapshot_id, target_timestamp, 
        start_time, status
    )
    VALUES (
        recovery_type, snapshot_id, target_timestamp,
        recovery_start_time, 'STARTED'
    );
    
    -- Pre-recovery validation
    IF recovery_type = 'FULL_RESTORE' THEN
        -- Validate snapshot exists and is complete
        PERFORM validate_snapshot_integrity(snapshot_id);
        
    ELSIF recovery_type = 'POINT_IN_TIME' THEN
        -- Validate target timestamp is within retention period
        IF target_timestamp < DATEADD(day, -35, GETDATE()) THEN
            RAISE EXCEPTION 'Target timestamp is outside retention period';
        END IF;
        
    END IF;
    
    -- Execute recovery based on type
    CASE recovery_type
        WHEN 'FULL_RESTORE' THEN
            PERFORM restore_from_snapshot(snapshot_id);
            
        WHEN 'POINT_IN_TIME' THEN
            PERFORM restore_to_point_in_time(target_timestamp);
            
        WHEN 'TABLE_RESTORE' THEN
            PERFORM restore_specific_tables(snapshot_id);
            
    END CASE;
    
    -- Post-recovery validation
    PERFORM validate_recovery_integrity();
    
    -- Update recovery log
    UPDATE backup.recovery_execution_log
    SET end_time = GETDATE(),
        status = 'COMPLETED',
        recovery_duration_minutes = DATEDIFF(minutes, recovery_start_time, GETDATE())
    WHERE start_time = recovery_start_time;
    
EXCEPTION
    WHEN OTHERS THEN
        UPDATE backup.recovery_execution_log
        SET end_time = GETDATE(),
            status = 'FAILED',
            error_message = SQLERRM
        WHERE start_time = recovery_start_time;
        RAISE;
END;
$$ LANGUAGE plpgsql;

-- 3. Recovery testing automation
CREATE OR REPLACE PROCEDURE test_recovery_procedures()
AS $$
BEGIN
    -- Test snapshot integrity
    PERFORM validate_all_snapshots();
    
    -- Test recovery time objectives (RTO)
    PERFORM measure_recovery_times();
    
    -- Test data integrity after recovery
    PERFORM validate_data_consistency();
    
    -- Generate recovery test report
    INSERT INTO backup.recovery_test_results (
        test_date, test_type, success_rate, avg_recovery_time_minutes,
        issues_found, recommendations
    )
    SELECT 
        CURRENT_DATE,
        'AUTOMATED_RECOVERY_TEST',
        (successful_tests * 100.0 / total_tests) as success_rate,
        AVG(recovery_duration_minutes),
        COUNT(CASE WHEN status = 'FAILED' THEN 1 END),
        'Review failed recovery attempts and optimize procedures'
    FROM backup.recovery_execution_log
    WHERE start_time >= DATEADD(day, -1, GETDATE());
    
END;
$$ LANGUAGE plpgsql;
```

## Scenario-Based Questions

### Q28: Design a solution for a retail company with 100TB of sales data requiring real-time analytics

**Answer:**
A comprehensive solution combining batch processing for historical data and streaming for real-time insights, with proper data modeling and performance optimization.

```sql
-- Retail analytics solution architecture

-- 1. Data model design
-- Fact table for sales transactions
CREATE TABLE retail.fact_sales (
    transaction_id BIGINT IDENTITY(1,1),
    store_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    customer_key INTEGER,
    date_key INTEGER NOT NULL,
    time_key INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    tax_amount DECIMAL(10,2) DEFAULT 0,
    payment_method VARCHAR(20),
    transaction_timestamp TIMESTAMP NOT NULL
)
DISTSTYLE KEY
DISTKEY (store_key)  -- Distribute by store for regional analytics
COMPOUND SORTKEY (date_key, time_key, store_key);

-- Real-time aggregation tables
CREATE TABLE retail.sales_realtime_hourly (
    store_key INTEGER,
    product_category VARCHAR(50),
    hour_timestamp TIMESTAMP,
    transaction_count INTEGER,
    total_revenue DECIMAL(15,2),
    avg_transaction_value DECIMAL(10,2),
    unique_customers INTEGER,
    last_updated TIMESTAMP DEFAULT GETDATE()
)
DISTSTYLE KEY
DISTKEY (store_key)
SORTKEY (hour_timestamp, store_key);

-- 2. Real-time processing pipeline
CREATE OR REPLACE PROCEDURE process_realtime_sales()
AS $$
BEGIN
    -- Process last hour of transactions
    CREATE TEMP TABLE hourly_aggregates AS
    SELECT 
        s.store_key,
        p.product_category,
        DATE_TRUNC('hour', s.transaction_timestamp) as hour_timestamp,
        COUNT(*) as transaction_count,
        SUM(s.total_amount) as total_revenue,
        AVG(s.total_amount) as avg_transaction_value,
        COUNT(DISTINCT s.customer_key) as unique_customers
    FROM retail.fact_sales s
    JOIN retail.dim_products p ON s.product_key = p.product_key
    WHERE s.transaction_timestamp >= DATE_TRUNC('hour', GETDATE() - INTERVAL '1 hour')
    AND s.transaction_timestamp < DATE_TRUNC('hour', GETDATE())
    GROUP BY s.store_key, p.product_category, DATE_TRUNC('hour', s.transaction_timestamp);
    
    -- Update real-time aggregates
    DELETE FROM retail.sales_realtime_hourly
    WHERE hour_timestamp = (SELECT MIN(hour_timestamp) FROM hourly_aggregates);
    
    INSERT INTO retail.sales_realtime_hourly (
        store_key, product_category, hour_timestamp, transaction_count,
        total_revenue, avg_transaction_value, unique_customers
    )
    SELECT * FROM hourly_aggregates;
    
    -- Update store performance dashboard
    INSERT INTO retail.store_performance_realtime (
        store_key, current_hour_revenue, daily_revenue_to_date,
        hourly_transaction_rate, performance_vs_target, last_updated
    )
    SELECT 
        s.store_key,
        COALESCE(rt.total_revenue, 0) as current_hour_revenue,
        COALESCE(daily.daily_revenue, 0) as daily_revenue_to_date,
        COALESCE(rt.transaction_count, 0) as hourly_transaction_rate,
        CASE 
            WHEN COALESCE(daily.daily_revenue, 0) >= t.daily_target THEN 'ABOVE_TARGET'
            WHEN COALESCE(daily.daily_revenue, 0) >= t.daily_target * 0.8 THEN 'ON_TARGET'
            ELSE 'BELOW_TARGET'
        END as performance_vs_target,
        GETDATE()
    FROM retail.dim_stores s
    LEFT JOIN (
        SELECT store_key, SUM(total_revenue) as total_revenue, SUM(transaction_count) as transaction_count
        FROM hourly_aggregates
        GROUP BY store_key
    ) rt ON s.store_key = rt.store_key
    LEFT JOIN (
        SELECT store_key, SUM(total_amount) as daily_revenue
        FROM retail.fact_sales
        WHERE DATE(transaction_timestamp) = CURRENT_DATE
        GROUP BY store_key
    ) daily ON s.store_key = daily.store_key
    LEFT JOIN retail.store_targets t ON s.store_key = t.store_key
    ON CONFLICT (store_key) DO UPDATE SET
        current_hour_revenue = EXCLUDED.current_hour_revenue,
        daily_revenue_to_date = EXCLUDED.daily_revenue_to_date,
        hourly_transaction_rate = EXCLUDED.hourly_transaction_rate,
        performance_vs_target = EXCLUDED.performance_vs_target,
        last_updated = EXCLUDED.last_updated;
    
END;
$$ LANGUAGE plpgsql;

-- 3. Analytics queries for business insights
-- Top performing products by region
CREATE VIEW retail.top_products_by_region AS
SELECT 
    r.region_name,
    p.product_name,
    p.product_category,
    SUM(f.total_amount) as total_revenue,
    SUM(f.quantity) as total_quantity,
    COUNT(DISTINCT f.customer_key) as unique_customers,
    AVG(f.total_amount) as avg_transaction_value
FROM retail.fact_sales f
JOIN retail.dim_products p ON f.product_key = p.product_key
JOIN retail.dim_stores s ON f.store_key = s.store_key
JOIN retail.dim_regions r ON s.region_key = r.region_key
WHERE f.date_key >= (SELECT date_key FROM retail.dim_date WHERE date_value = CURRENT_DATE - 30)
GROUP BY r.region_name, p.product_name, p.product_category;

-- Customer segmentation analysis
CREATE MATERIALIZED VIEW retail.customer_segments AS
SELECT 
    c.customer_key,
    c.customer_name,
    COUNT(DISTINCT f.transaction_id) as total_transactions,
    SUM(f.total_amount) as total_spent,
    AVG(f.total_amount) as avg_transaction_value,
    MAX(d.date_value) as last_purchase_date,
    DATEDIFF(day, MAX(d.date_value), CURRENT_DATE) as days_since_last_purchase,
    CASE 
        WHEN SUM(f.total_amount) >= 10000 AND COUNT(DISTINCT f.transaction_id) >= 50 THEN 'VIP'
        WHEN SUM(f.total_amount) >= 5000 AND COUNT(DISTINCT f.transaction_id) >= 20 THEN 'HIGH_VALUE'
        WHEN SUM(f.total_amount) >= 1000 AND COUNT(DISTINCT f.transaction_id) >= 10 THEN 'REGULAR'
        ELSE 'OCCASIONAL'
    END as customer_segment
FROM retail.fact_sales f
JOIN retail.dim_customers c ON f.customer_key = c.customer_key
JOIN retail.dim_date d ON f.date_key = d.date_key
WHERE d.date_value >= CURRENT_DATE - 365  -- Last year
GROUP BY c.customer_key, c.customer_name;

-- 4. Performance monitoring and optimization
CREATE OR REPLACE PROCEDURE monitor_retail_performance()
AS $$
BEGIN
    -- Monitor query performance for dashboard queries
    INSERT INTO retail.performance_metrics (
        metric_name, metric_value, metric_timestamp
    )
    SELECT 
        'avg_dashboard_query_time_sec',
        AVG(DATEDIFF(seconds, starttime, endtime)),
        GETDATE()
    FROM stl_query
    WHERE querytxt LIKE '%retail.%'
    AND starttime >= DATEADD(hour, -1, GETDATE())
    AND endtime IS NOT NULL;
    
    -- Monitor data freshness
    INSERT INTO retail.performance_metrics (
        metric_name, metric_value, metric_timestamp
    )
    SELECT 
        'data_freshness_minutes',
        DATEDIFF(minutes, MAX(transaction_timestamp), GETDATE()),
        GETDATE()
    FROM retail.fact_sales;
    
    -- Monitor storage growth
    INSERT INTO retail.performance_metrics (
        metric_name, metric_value, metric_timestamp
    )
    SELECT 
        'storage_size_gb',
        SUM(size) / 1024.0,
        GETDATE()
    FROM svv_table_info
    WHERE schemaname = 'retail';
    
END;
$$ LANGUAGE plpgsql;
```

### Q29: How would you migrate a 500TB Oracle data warehouse to Redshift with minimal downtime?

**Answer:**
A phased migration approach using AWS DMS, parallel processing, and careful cutover planning to minimize business impact.

```sql
-- Large-scale migration strategy

-- 1. Migration planning and assessment
CREATE TABLE migration.source_assessment (
    table_name VARCHAR(100),
    schema_name VARCHAR(50),
    row_count BIGINT,
    size_gb DECIMAL(10,2),
    complexity_score INTEGER, -- 1-10 based on features used
    migration_priority VARCHAR(20), -- HIGH, MEDIUM, LOW
    estimated_migration_hours DECIMAL(5,2),
    dependencies TEXT
);

-- Migration phases
CREATE TABLE migration.migration_phases (
    phase_id INTEGER,
    phase_name VARCHAR(50),
    start_date DATE,
    end_date DATE,
    tables_included TEXT,
    success_criteria TEXT,
    rollback_plan TEXT
);

-- 2. Schema conversion and optimization
CREATE OR REPLACE PROCEDURE convert_oracle_schema()
AS $$
BEGIN
    -- Phase 1: Create optimized Redshift schema
    
    -- Convert Oracle partitioned table to Redshift distributed table
    CREATE TABLE migration.fact_sales_migrated (
        sale_id BIGINT,
        customer_id INTEGER ENCODE DELTA,
        product_id INTEGER ENCODE DELTA32K,
        sale_date DATE ENCODE DELTA32K,
        amount DECIMAL(12,2) ENCODE DELTA32K,
        -- Oracle CLOB to VARCHAR(MAX)
        notes VARCHAR(65535) ENCODE LZO,
        -- Oracle NUMBER to appropriate Redshift type
        quantity INTEGER ENCODE DELTA32K,
        created_timestamp TIMESTAMP ENCODE DELTA32K
    )
    DISTSTYLE KEY
    DISTKEY (customer_id)
    SORTKEY (sale_date, customer_id);
    
    -- Convert Oracle materialized views to Redshift materialized views
    CREATE MATERIALIZED VIEW migration.mv_monthly_sales AS
    SELECT 
        DATE_TRUNC('month', sale_date) as month,
        customer_id,
        SUM(amount) as total_amount,
        COUNT(*) as transaction_count
    FROM migration.fact_sales_migrated
    GROUP BY DATE_TRUNC('month', sale_date), customer_id;
    
    -- Log schema conversion
    INSERT INTO migration.conversion_log (
        object_type, object_name, conversion_status, notes
    )
    VALUES 
    ('TABLE', 'fact_sales', 'CONVERTED', 'Added distribution and sort keys'),
    ('MATERIALIZED_VIEW', 'mv_monthly_sales', 'CONVERTED', 'Converted from Oracle MV');
    
END;
$$ LANGUAGE plpgsql;

-- 3. Data migration with DMS
CREATE TABLE migration.dms_tasks (
    task_id VARCHAR(100),
    task_name VARCHAR(100),
    source_table VARCHAR(100),
    target_table VARCHAR(100),
    migration_type VARCHAR(20), -- FULL_LOAD, CDC, FULL_LOAD_AND_CDC
    task_status VARCHAR(20),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    rows_migrated BIGINT,
    errors_count INTEGER
);

-- Monitor DMS migration progress
CREATE OR REPLACE PROCEDURE monitor_dms_migration()
AS $$
BEGIN
    -- Check migration progress
    INSERT INTO migration.progress_log (
        log_timestamp, total_tables, completed_tables, 
        in_progress_tables, failed_tables, overall_progress_pct
    )
    SELECT 
        GETDATE(),
        COUNT(*) as total_tables,
        SUM(CASE WHEN task_status = 'COMPLETED' THEN 1 ELSE 0 END) as completed_tables,
        SUM(CASE WHEN task_status = 'RUNNING' THEN 1 ELSE 0 END) as in_progress_tables,
        SUM(CASE WHEN task_status = 'FAILED' THEN 1 ELSE 0 END) as failed_tables,
        (SUM(CASE WHEN task_status = 'COMPLETED' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as overall_progress_pct
    FROM migration.dms_tasks;
    
    -- Identify bottlenecks
    INSERT INTO migration.bottleneck_analysis (
        analysis_timestamp, bottleneck_type, affected_tables, 
        recommended_action
    )
    SELECT 
        GETDATE(),
        'SLOW_MIGRATION',
        STRING_AGG(task_name, ', '),
        'Consider increasing DMS instance size or parallelizing large tables'
    FROM migration.dms_tasks
    WHERE task_status = 'RUNNING'
    AND DATEDIFF(hours, start_time, GETDATE()) > 24
    HAVING COUNT(*) > 0;
    
END;
$$ LANGUAGE plpgsql;

-- 4. Data validation and reconciliation
CREATE OR REPLACE PROCEDURE validate_migrated_data()
AS $$
BEGIN
    -- Row count validation
    CREATE TEMP TABLE validation_results AS
    SELECT 
        t.table_name,
        t.oracle_row_count,
        r.redshift_row_count,
        ABS(t.oracle_row_count - r.redshift_row_count) as row_difference,
        CASE 
            WHEN t.oracle_row_count = r.redshift_row_count THEN 'PASS'
            WHEN ABS(t.oracle_row_count - r.redshift_row_count) < (t.oracle_row_count * 0.001) THEN 'ACCEPTABLE'
            ELSE 'FAIL'
        END as validation_status
    FROM migration.oracle_table_counts t
    JOIN migration.redshift_table_counts r ON t.table_name = r.table_name;
    
    -- Data type validation
    INSERT INTO migration.validation_log (
        validation_type, table_name, validation_status, 
        details, validation_timestamp
    )
    SELECT 
        'ROW_COUNT',
        table_name,
        validation_status,
        'Oracle: ' || oracle_row_count || ', Redshift: ' || redshift_row_count,
        GETDATE()
    FROM validation_results;
    
    -- Sample data comparison
    PERFORM compare_sample_data();
    
    -- Aggregate validation
    PERFORM validate_aggregates();
    
END;
$$ LANGUAGE plpgsql;

-- 5. Cutover planning and execution
CREATE OR REPLACE PROCEDURE execute_cutover()
AS $$
DECLARE
    cutover_start_time TIMESTAMP := GETDATE();
BEGIN
    -- Pre-cutover validation
    PERFORM validate_all_data();
    PERFORM test_application_connectivity();
    
    -- Stop Oracle applications (coordinated with application teams)
    INSERT INTO migration.cutover_log (step_name, start_time, status)
    VALUES ('STOP_APPLICATIONS', cutover_start_time, 'STARTED');
    
    -- Final CDC sync
    PERFORM sync_final_changes();
    
    -- Switch DNS/connection strings to Redshift
    PERFORM update_connection_strings();
    
    -- Start applications with Redshift
    PERFORM start_applications();
    
    -- Post-cutover validation
    PERFORM validate_application_functionality();
    
    -- Update cutover status
    UPDATE migration.cutover_log 
    SET end_time = GETDATE(), status = 'COMPLETED'
    WHERE step_name = 'STOP_APPLICATIONS' 
    AND start_time = cutover_start_time;
    
    -- Generate cutover report
    INSERT INTO migration.cutover_report (
        cutover_date, total_downtime_minutes, 
        validation_results, issues_encountered
    )
    SELECT 
        CURRENT_DATE,
        DATEDIFF(minutes, cutover_start_time, GETDATE()),
        'All validations passed',
        'None'
    WHERE NOT EXISTS (
        SELECT 1 FROM migration.validation_log 
        WHERE validation_status = 'FAIL' 
        AND validation_timestamp >= cutover_start_time
    );
    
END;
$$ LANGUAGE plpgsql;

-- 6. Post-migration optimization
CREATE OR REPLACE PROCEDURE optimize_post_migration()
AS $$
BEGIN
    -- Analyze all migrated tables
    ANALYZE;
    
    -- Vacuum tables that had heavy loading
    VACUUM REINDEX migration.fact_sales_migrated;
    
    -- Update table statistics
    PERFORM update_table_statistics();
    
    -- Optimize queries based on new execution plans
    PERFORM analyze_query_performance();
    
    -- Set up monitoring for production workload
    PERFORM setup_production_monitoring();
    
END;
$$ LANGUAGE plpgsql;
```

### Q30: Design a multi-tenant SaaS analytics platform using Redshift

**Answer:**
A secure, scalable multi-tenant architecture with proper data isolation, resource management, and tenant-specific analytics capabilities.

```sql
-- Multi-tenant SaaS analytics platform

-- 1. Tenant management and isolation
CREATE SCHEMA tenant_management;

CREATE TABLE tenant_management.tenants (
    tenant_id INTEGER IDENTITY(1,1) PRIMARY KEY,
    tenant_uuid VARCHAR(36) UNIQUE NOT NULL,
    tenant_name VARCHAR(100) NOT NULL,
    subscription_tier VARCHAR(20), -- BASIC, PREMIUM, ENTERPRISE
    data_retention_days INTEGER DEFAULT 365,
    max_storage_gb INTEGER,
    max_queries_per_hour INTEGER,
    created_date TIMESTAMP DEFAULT GETDATE(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Tenant data isolation using row-level security
CREATE TABLE saas.customer_data (
    tenant_id INTEGER NOT NULL,
    customer_id BIGINT,
    customer_name VARCHAR(100),
    email VARCHAR(100),
    created_date TIMESTAMP,
    -- Tenant isolation enforced at application level and views
    FOREIGN KEY (tenant_id) REFERENCES tenant_management.tenants(tenant_id)
)
DISTSTYLE KEY
DISTKEY (tenant_id)
SORTKEY (tenant_id, created_date);

-- 2. Tenant-specific schemas and views
CREATE OR REPLACE PROCEDURE create_tenant_schema(tenant_uuid VARCHAR)
AS $$
DECLARE
    tenant_id_val INTEGER;
    schema_name VARCHAR(50);
BEGIN
    -- Get tenant ID
    SELECT tenant_id INTO tenant_id_val
    FROM tenant_management.tenants
    WHERE tenant_uuid = tenant_uuid;
    
    schema_name := 'tenant_' || tenant_id_val;
    
    -- Create tenant-specific schema
    EXECUTE 'CREATE SCHEMA IF NOT EXISTS ' || schema_name;
    
    -- Create tenant-specific views with data isolation
    EXECUTE 'CREATE VIEW ' || schema_name || '.customers AS 
             SELECT customer_id, customer_name, email, created_date
             FROM saas.customer_data 
             WHERE tenant_id = ' || tenant_id_val;
    
    EXECUTE 'CREATE VIEW ' || schema_name || '.analytics_summary AS
             SELECT 
                 DATE_TRUNC(''month'', created_date) as month,
                 COUNT(*) as customer_count,
                 COUNT(DISTINCT email) as unique_emails
             FROM saas.customer_data 
             WHERE tenant_id = ' || tenant_id_val || '
             GROUP BY DATE_TRUNC(''month'', created_date)';
    
    -- Create tenant user and grant permissions
    EXECUTE 'CREATE USER tenant_user_' || tenant_id_val || 
            ' PASSWORD ''TempPassword123!'' CREATE_DB FALSE';
    
    EXECUTE 'GRANT USAGE ON SCHEMA ' || schema_name || 
            ' TO tenant_user_' || tenant_id_val;
    
    EXECUTE 'GRANT SELECT ON ALL TABLES IN SCHEMA ' || schema_name || 
            ' TO tenant_user_' || tenant_id_val;
    
    -- Log tenant setup
    INSERT INTO tenant_management.tenant_setup_log (
        tenant_id, schema_name, setup_date, status
    )
    VALUES (tenant_id_val, schema_name, GETDATE(), 'COMPLETED');
    
END;
$$ LANGUAGE plpgsql;

-- 3. Resource management and quotas
CREATE TABLE tenant_management.resource_usage (
    tenant_id INTEGER,
    usage_date DATE,
    storage_used_gb DECIMAL(10,2),
    queries_executed INTEGER,
    compute_hours DECIMAL(8,2),
    data_scanned_gb DECIMAL(12,2),
    PRIMARY KEY (tenant_id, usage_date)
);

CREATE OR REPLACE PROCEDURE monitor_tenant_usage()
AS $$
BEGIN
    -- Calculate daily usage per tenant
    INSERT INTO tenant_management.resource_usage (
        tenant_id, usage_date, storage_used_gb, 
        queries_executed, compute_hours, data_scanned_gb
    )
    SELECT 
        t.tenant_id,
        CURRENT_DATE,
        -- Storage usage
        COALESCE(storage.size_gb, 0),
        -- Query count
        COALESCE(queries.query_count, 0),
        -- Compute hours (estimated)
        COALESCE(queries.total_execution_seconds, 0) / 3600.0,
        -- Data scanned
        COALESCE(queries.total_bytes_scanned, 0) / (1024.0 * 1024.0 * 1024.0)
    FROM tenant_management.tenants t
    LEFT JOIN (
        -- Calculate storage per tenant
        SELECT 
            tenant_id,
            SUM(size) / 1024.0 as size_gb
        FROM svv_table_info sti
        JOIN saas.tenant_table_mapping ttm ON sti.tablename = ttm.table_name
        GROUP BY tenant_id
    ) storage ON t.tenant_id = storage.tenant_id
    LEFT JOIN (
        -- Calculate query metrics per tenant
        SELECT 
            tm.tenant_id,
            COUNT(*) as query_count,
            SUM(DATEDIFF(seconds, q.starttime, q.endtime)) as total_execution_seconds,
            SUM(qs.bytes) as total_bytes_scanned
        FROM stl_query q
        JOIN tenant_management.tenant_user_mapping tm ON q.userid = tm.user_id
        LEFT JOIN svl_query_summary qs ON q.query = qs.query
        WHERE q.starttime >= CURRENT_DATE
        AND q.starttime < CURRENT_DATE + 1
        GROUP BY tm.tenant_id
    ) queries ON t.tenant_id = queries.tenant_id
    ON CONFLICT (tenant_id, usage_date) DO UPDATE SET
        storage_used_gb = EXCLUDED.storage_used_gb,
        queries_executed = EXCLUDED.queries_executed,
        compute_hours = EXCLUDED.compute_hours,
        data_scanned_gb = EXCLUDED.data_scanned_gb;
    
    -- Check quota violations
    INSERT INTO tenant_management.quota_violations (
        tenant_id, violation_type, current_usage, 
        quota_limit, violation_date
    )
    SELECT 
        ru.tenant_id,
        'STORAGE_QUOTA_EXCEEDED',
        ru.storage_used_gb,
        t.max_storage_gb,
        CURRENT_DATE
    FROM tenant_management.resource_usage ru
    JOIN tenant_management.tenants t ON ru.tenant_id = t.tenant_id
    WHERE ru.usage_date = CURRENT_DATE
    AND ru.storage_used_gb > t.max_storage_gb;
    
END;
$$ LANGUAGE plpgsql;

-- 4. Tenant-specific analytics and reporting
CREATE OR REPLACE FUNCTION get_tenant_analytics(
    tenant_uuid VARCHAR,
    start_date DATE,
    end_date DATE
)
RETURNS TABLE (
    metric_name VARCHAR(50),
    metric_value DECIMAL(15,2),
    metric_date DATE
)
AS $$
DECLARE
    tenant_id_val INTEGER;
BEGIN
    -- Get tenant ID
    SELECT tenant_id INTO tenant_id_val
    FROM tenant_management.tenants
    WHERE tenant_uuid = tenant_uuid;
    
    -- Return analytics data
    RETURN QUERY
    SELECT 
        'total_customers'::VARCHAR(50),
        COUNT(*)::DECIMAL(15,2),
        CURRENT_DATE
    FROM saas.customer_data
    WHERE tenant_id = tenant_id_val
    AND created_date BETWEEN start_date AND end_date
    
    UNION ALL
    
    SELECT 
        'daily_signups'::VARCHAR(50),
        COUNT(*)::DECIMAL(15,2),
        created_date::DATE
    FROM saas.customer_data
    WHERE tenant_id = tenant_id_val
    AND created_date BETWEEN start_date AND end_date
    GROUP BY created_date::DATE
    
    UNION ALL
    
    SELECT 
        'storage_usage_gb'::VARCHAR(50),
        storage_used_gb,
        usage_date
    FROM tenant_management.resource_usage
    WHERE tenant_id = tenant_id_val
    AND usage_date BETWEEN start_date AND end_date;
    
END;
$$ LANGUAGE plpgsql;

-- 5. Multi-tenant data pipeline
CREATE OR REPLACE PROCEDURE process_tenant_data_pipeline()
AS $$
BEGIN
    -- Process data for each active tenant
    FOR tenant_rec IN 
        SELECT tenant_id, tenant_uuid, subscription_tier
        FROM tenant_management.tenants
        WHERE is_active = TRUE
    LOOP
        -- Tenant-specific ETL processing
        PERFORM process_tenant_etl(tenant_rec.tenant_id);
        
        -- Update tenant metrics
        PERFORM update_tenant_metrics(tenant_rec.tenant_id);
        
        -- Generate tenant reports based on subscription tier
        IF tenant_rec.subscription_tier IN ('PREMIUM', 'ENTERPRISE') THEN
            PERFORM generate_advanced_reports(tenant_rec.tenant_id);
        END IF;
        
        -- Data retention cleanup
        PERFORM cleanup_tenant_data(
            tenant_rec.tenant_id, 
            (SELECT data_retention_days FROM tenant_management.tenants 
             WHERE tenant_id = tenant_rec.tenant_id)
        );
        
    END LOOP;
    
    -- Log pipeline completion
    INSERT INTO tenant_management.pipeline_log (
        pipeline_date, tenants_processed, status, duration_minutes
    )
    SELECT 
        CURRENT_DATE,
        COUNT(*),
        'COMPLETED',
        DATEDIFF(minutes, MIN(start_time), MAX(end_time))
    FROM tenant_management.tenant_processing_log
    WHERE processing_date = CURRENT_DATE;
    
END;
$$ LANGUAGE plpgsql;

-- 6. Tenant billing and usage reporting
CREATE VIEW tenant_management.billing_summary AS
SELECT 
    t.tenant_id,
    t.tenant_name,
    t.subscription_tier,
    ru.usage_date,
    ru.storage_used_gb,
    ru.queries_executed,
    ru.compute_hours,
    -- Calculate costs based on subscription tier
    CASE t.subscription_tier
        WHEN 'BASIC' THEN 
            (ru.storage_used_gb * 0.10) + (ru.compute_hours * 1.00)
        WHEN 'PREMIUM' THEN 
            (ru.storage_used_gb * 0.08) + (ru.compute_hours * 0.80)
        WHEN 'ENTERPRISE' THEN 
            (ru.storage_used_gb * 0.06) + (ru.compute_hours * 0.60)
    END as daily_cost
FROM tenant_management.tenants t
JOIN tenant_management.resource_usage ru ON t.tenant_id = ru.tenant_id
WHERE t.is_active = TRUE;
```

## Performance Tuning & Optimization

### Q31: How do you implement advanced compression strategies?

**Answer:**
Optimal compression reduces storage costs and improves I/O performance through proper encoding selection.

```sql
-- Analyze compression effectiveness
SELECT 
    schemaname,
    tablename,
    column_name,
    type,
    encoding,
    size,
    size_raw,
    compression_ratio
FROM pg_table_def 
WHERE schemaname = 'analytics'
AND compression_ratio > 1
ORDER BY compression_ratio DESC;

-- Test compression on sample data
ANALYZE COMPRESSION staging.large_table;
```

### Q32: How do you optimize COPY operations for maximum throughput?

**Answer:**
COPY optimization involves file sizing, parallelization, and format selection.

```sql
-- Optimized COPY with multiple files
COPY fact_sales 
FROM 's3://bucket/data/'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftRole'
FORMAT AS PARQUET
MANIFEST
COMPUPDATE ON
STATUPDATE ON;

-- Monitor COPY performance
SELECT 
    query,
    slice,
    read_time,
    write_time,
    file_size
FROM stl_load_commits 
WHERE query = pg_last_query_id();
```

### Q33: How do you handle large DELETE operations efficiently?

**Answer:**
Large deletes should use staging tables and CTAS patterns to avoid performance issues.

```sql
-- Efficient delete using CTAS
CREATE TABLE fact_sales_new AS
SELECT * FROM fact_sales
WHERE sale_date >= '2023-01-01';

DROP TABLE fact_sales;
ALTER TABLE fact_sales_new RENAME TO fact_sales;
```

### Q34: How do you implement table maintenance automation?

**Answer:**
Automated maintenance ensures optimal performance through scheduled VACUUM and ANALYZE operations.

```sql
-- Maintenance scheduling procedure
CREATE OR REPLACE PROCEDURE automated_maintenance()
AS $$
BEGIN
    -- Check tables needing VACUUM
    FOR table_rec IN 
        SELECT schemaname, tablename
        FROM svv_table_info
        WHERE vacuum_sort_benefit > 5
    LOOP
        EXECUTE 'VACUUM ' || table_rec.schemaname || '.' || table_rec.tablename;
    END LOOP;
    
    -- Update statistics
    ANALYZE;
END;
$$ LANGUAGE plpgsql;
```

### Q35: How do you optimize window functions in Redshift?

**Answer:**
Window function optimization involves proper partitioning and sort key alignment.

```sql
-- Optimized window function
SELECT 
    customer_id,
    sale_date,
    total_amount,
    SUM(total_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY sale_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_total
FROM fact_sales
WHERE sale_date >= '2023-01-01'
ORDER BY customer_id, sale_date;
```

## Data Modeling & Architecture

### Q36: How do you design star schema vs snowflake schema in Redshift?

**Answer:**
Star schema is preferred in Redshift for better join performance and simpler queries.

```sql
-- Star schema design
CREATE TABLE dim_customer (
    customer_key BIGINT IDENTITY(1,1) PRIMARY KEY,
    customer_id INTEGER,
    customer_name VARCHAR(100),
    segment VARCHAR(50),
    region VARCHAR(50)
) DISTSTYLE ALL;

CREATE TABLE fact_orders (
    order_key BIGINT IDENTITY(1,1),
    customer_key BIGINT,
    product_key BIGINT,
    date_key INTEGER,
    order_amount DECIMAL(12,2)
) DISTSTYLE KEY DISTKEY (customer_key);
```

### Q37: How do you implement slowly changing dimensions (SCD)?

**Answer:**
SCD Type 2 tracks historical changes with effective dates and current flags.

```sql
-- SCD Type 2 implementation
CREATE TABLE dim_customer_scd (
    customer_key BIGINT IDENTITY(1,1),
    customer_id INTEGER,
    customer_name VARCHAR(100),
    effective_date DATE,
    expiry_date DATE,
    is_current BOOLEAN
) DISTSTYLE ALL;

-- SCD update procedure
CREATE OR REPLACE PROCEDURE update_customer_scd()
AS $$
BEGIN
    -- Close existing records
    UPDATE dim_customer_scd 
    SET expiry_date = CURRENT_DATE - 1,
        is_current = FALSE
    WHERE customer_id IN (SELECT customer_id FROM staging_customers)
    AND is_current = TRUE;
    
    -- Insert new records
    INSERT INTO dim_customer_scd (
        customer_id, customer_name, effective_date, expiry_date, is_current
    )
    SELECT customer_id, customer_name, CURRENT_DATE, '9999-12-31', TRUE
    FROM staging_customers;
END;
$$ LANGUAGE plpgsql;
```

### Q38: How do you handle large fact table partitioning strategies?

**Answer:**
Redshift uses distribution and sort keys instead of traditional partitioning.

```sql
-- Time-based partitioning using sort keys
CREATE TABLE fact_sales_partitioned (
    sale_id BIGINT,
    sale_date DATE,
    customer_id INTEGER,
    amount DECIMAL(12,2)
)
DISTSTYLE KEY
DISTKEY (customer_id)
SORTKEY (sale_date);  -- Enables zone maps for date filtering

-- Query with partition pruning
SELECT customer_id, SUM(amount)
FROM fact_sales_partitioned
WHERE sale_date BETWEEN '2023-01-01' AND '2023-01-31'
GROUP BY customer_id;
```

### Q39: How do you implement data vault modeling in Redshift?

**Answer:**
Data Vault uses hubs, links, and satellites for flexible data warehousing.

```sql
-- Hub table
CREATE TABLE hub_customer (
    customer_hash_key VARCHAR(32) PRIMARY KEY,
    customer_id INTEGER,
    load_date TIMESTAMP,
    record_source VARCHAR(50)
) DISTSTYLE ALL;

-- Satellite table
CREATE TABLE sat_customer (
    customer_hash_key VARCHAR(32),
    load_date TIMESTAMP,
    customer_name VARCHAR(100),
    email VARCHAR(100),
    hash_diff VARCHAR(32)
) DISTSTYLE ALL;

-- Link table
CREATE TABLE link_customer_order (
    link_hash_key VARCHAR(32) PRIMARY KEY,
    customer_hash_key VARCHAR(32),
    order_hash_key VARCHAR(32),
    load_date TIMESTAMP
) DISTSTYLE KEY DISTKEY (customer_hash_key);
```

### Q40: How do you optimize aggregation tables and materialized views?

**Answer:**
Pre-aggregated tables and materialized views improve query performance for common patterns.

```sql
-- Aggregation table
CREATE TABLE agg_monthly_sales AS
SELECT 
    DATE_TRUNC('month', sale_date) as month,
    customer_id,
    product_category,
    SUM(amount) as total_sales,
    COUNT(*) as transaction_count
FROM fact_sales
GROUP BY DATE_TRUNC('month', sale_date), customer_id, product_category;

-- Materialized view
CREATE MATERIALIZED VIEW mv_customer_summary AS
SELECT 
    customer_id,
    COUNT(*) as order_count,
    SUM(amount) as total_spent,
    MAX(sale_date) as last_order_date
FROM fact_sales
GROUP BY customer_id;

-- Refresh materialized view
REFRESH MATERIALIZED VIEW mv_customer_summary;
```

## Security & Compliance

### Q41: How do you implement column-level security in Redshift?

**Answer:**
Column-level security uses views and grants to restrict access to sensitive data.

```sql
-- Secure view with column masking
CREATE VIEW secure_customer_view AS
SELECT 
    customer_id,
    first_name,
    CASE 
        WHEN CURRENT_USER IN ('analyst', 'manager') THEN email
        ELSE 'REDACTED'
    END as email,
    registration_date
FROM customers;

-- Grant access to secure view
GRANT SELECT ON secure_customer_view TO analyst_role;
```

### Q42: How do you implement audit logging for compliance?

**Answer:**
Comprehensive audit logging tracks all data access and modifications.

```sql
-- Audit log table
CREATE TABLE audit_log (
    log_id BIGINT IDENTITY(1,1),
    username VARCHAR(50),
    table_name VARCHAR(100),
    action VARCHAR(20),
    timestamp TIMESTAMP DEFAULT GETDATE(),
    query_text TEXT
);

-- Monitor user activity
SELECT 
    username,
    COUNT(*) as query_count,
    MIN(starttime) as first_query,
    MAX(starttime) as last_query
FROM stl_query
WHERE starttime >= CURRENT_DATE - 7
GROUP BY username;
```

### Q43: How do you implement data encryption at rest and in transit?

**Answer:**
Redshift provides encryption options for data protection.

```sql
-- Check encryption status
SELECT 
    cluster_identifier,
    encrypted,
    kms_key_id
FROM stv_cluster_info;

-- SSL connection verification
SELECT 
    pid,
    user_name,
    ssl,
    ssl_version
FROM stv_sessions
WHERE user_name != 'rdsdb';
```

### Q44: How do you implement GDPR compliance in Redshift?

**Answer:**
GDPR compliance requires data subject rights implementation and audit trails.

```sql
-- Data subject access request
CREATE OR REPLACE PROCEDURE gdpr_data_export(subject_email VARCHAR)
AS $$
BEGIN
    CREATE TEMP TABLE subject_data AS
    SELECT 
        'CUSTOMER' as data_type,
        customer_id::VARCHAR as identifier,
        first_name || ' ' || last_name as data_value,
        'Personal identification' as category
    FROM customers
    WHERE email = subject_email
    
    UNION ALL
    
    SELECT 
        'ORDERS',
        order_id::VARCHAR,
        'Order amount: ' || total_amount::VARCHAR,
        'Transaction data'
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE c.email = subject_email;
END;
$$ LANGUAGE plpgsql;

-- Right to be forgotten
CREATE OR REPLACE PROCEDURE gdpr_delete_subject(subject_email VARCHAR)
AS $$
BEGIN
    DELETE FROM customers WHERE email = subject_email;
    DELETE FROM orders WHERE customer_id IN (
        SELECT customer_id FROM customers WHERE email = subject_email
    );
END;
$$ LANGUAGE plpgsql;
```

### Q45: How do you implement role-based access control (RBAC)?

**Answer:**
RBAC provides granular permissions through roles and groups.

```sql
-- Create roles hierarchy
CREATE ROLE data_viewer;
CREATE ROLE data_analyst;
CREATE ROLE data_engineer;
CREATE ROLE data_admin;

-- Grant role hierarchy
GRANT data_viewer TO data_analyst;
GRANT data_analyst TO data_engineer;
GRANT data_engineer TO data_admin;

-- Schema permissions
GRANT USAGE ON SCHEMA analytics TO ROLE data_viewer;
GRANT SELECT ON ALL TABLES IN SCHEMA analytics TO ROLE data_viewer;
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA staging TO ROLE data_engineer;

-- User assignment
CREATE USER john_analyst PASSWORD 'SecurePass123!';
GRANT data_analyst TO john_analyst;
```

## Cost Optimization

### Q46: How do you optimize Redshift costs?

**Answer:**
Cost optimization involves right-sizing, reserved instances, and efficient resource usage.

```sql
-- Monitor cluster utilization
SELECT 
    DATE_TRUNC('hour', starttime) as hour,
    COUNT(*) as query_count,
    AVG(DATEDIFF(seconds, starttime, endtime)) as avg_duration
FROM stl_query
WHERE starttime >= CURRENT_DATE - 7
GROUP BY DATE_TRUNC('hour', starttime)
ORDER BY hour;

-- Storage cost analysis
SELECT 
    schemaname,
    SUM(size) / 1024.0 as size_gb,
    SUM(size) / 1024.0 * 0.025 as monthly_cost_usd
FROM svv_table_info
WHERE schemaname NOT IN ('information_schema', 'pg_catalog')
GROUP BY schemaname
ORDER BY size_gb DESC;
```

### Q47: How do you implement elastic resize and pause/resume?

**Answer:**
Elastic resize and pause/resume optimize costs for variable workloads.

```sql
-- Monitor resize operations
SELECT 
    resize_id,
    cluster_identifier,
    resize_type,
    start_time,
    end_time,
    status
FROM stl_resize
WHERE start_time >= CURRENT_DATE - 30
ORDER BY start_time DESC;

-- Check cluster status for pause/resume
SELECT 
    cluster_identifier,
    cluster_status,
    cluster_create_time,
    automated_snapshot_retention_period
FROM stv_cluster_info;
```

### Q48: How do you optimize storage with data lifecycle management?

**Answer:**
Data lifecycle management archives old data to reduce storage costs.

```sql
-- Identify old data for archival
SELECT 
    schemaname,
    tablename,
    size,
    tbl_rows,
    CASE 
        WHEN MAX(last_accessed) < CURRENT_DATE - 90 THEN 'ARCHIVE_CANDIDATE'
        WHEN MAX(last_accessed) < CURRENT_DATE - 30 THEN 'REVIEW'
        ELSE 'ACTIVE'
    END as lifecycle_status
FROM svv_table_info sti
LEFT JOIN (
    SELECT 
        schemaname,
        tablename,
        MAX(starttime) as last_accessed
    FROM stl_scan
    GROUP BY schemaname, tablename
) access ON sti.schemaname = access.schemaname 
    AND sti.tablename = access.tablename
GROUP BY sti.schemaname, sti.tablename, sti.size, sti.tbl_rows;

-- Archive old data to S3
UNLOAD ('SELECT * FROM old_transactions WHERE transaction_date < ''2022-01-01''')
TO 's3://archive-bucket/old_transactions/'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftUnloadRole'
PARQUET;
```

### Q49: How do you implement workload isolation for cost control?

**Answer:**
Workload isolation prevents resource contention and controls costs.

```sql
-- WLM queue configuration monitoring
SELECT 
    service_class,
    service_class_name,
    num_query_tasks,
    query_working_mem,
    max_execution_time
FROM stv_wlm_service_class_config
ORDER BY service_class;

-- Query queue analysis
SELECT 
    w.service_class,
    w.service_class_name,
    COUNT(*) as query_count,
    AVG(w.total_queue_time) as avg_queue_time,
    AVG(w.total_exec_time) as avg_exec_time
FROM stl_wlm_query w
WHERE w.queue_start_time >= CURRENT_DATE - 1
GROUP BY w.service_class, w.service_class_name
ORDER BY w.service_class;
```

### Q50: How do you monitor and optimize concurrency scaling costs?

**Answer:**
Concurrency scaling monitoring helps control automatic scaling costs.

```sql
-- Concurrency scaling usage analysis
SELECT 
    DATE_TRUNC('day', start_time) as day,
    COUNT(*) as scaling_events,
    SUM(DATEDIFF(seconds, start_time, end_time)) / 3600.0 as total_hours,
    SUM(DATEDIFF(seconds, start_time, end_time)) / 3600.0 * 0.045 as estimated_cost
FROM stl_concurrency_scaling_usage
WHERE start_time >= CURRENT_DATE - 30
GROUP BY DATE_TRUNC('day', start_time)
ORDER BY day;

-- Identify queries using concurrency scaling
SELECT 
    w.query,
    w.concurrency_scaling_status,
    q.querytxt,
    w.total_exec_time
FROM stl_wlm_query w
JOIN stl_query q ON w.query = q.query
WHERE w.concurrency_scaling_status = 'concurrency_scaling'
AND w.queue_start_time >= CURRENT_DATE - 1;
```

## Troubleshooting & Operations

### Q51: How do you troubleshoot slow query performance?

**Answer:**
Query troubleshooting involves analyzing execution plans and system bottlenecks.

```sql
-- Identify slow queries
SELECT 
    query,
    userid,
    DATEDIFF(seconds, starttime, endtime) as duration_sec,
    substring(querytxt, 1, 100) as query_text
FROM stl_query
WHERE endtime IS NOT NULL
AND DATEDIFF(seconds, starttime, endtime) > 300
AND starttime >= CURRENT_DATE - 1
ORDER BY duration_sec DESC;

-- Analyze query execution steps
SELECT 
    query,
    segment,
    step,
    label,
    max_time,
    avg_time,
    rows
FROM svl_query_summary
WHERE query = 12345  -- Replace with actual query ID
ORDER BY segment, step;
```

### Q52: How do you diagnose and resolve disk space issues?

**Answer:**
Disk space monitoring prevents cluster failures and performance degradation.

```sql
-- Check disk space usage
SELECT 
    node,
    slice,
    used,
    capacity,
    (used::FLOAT / capacity::FLOAT) * 100 as usage_percent
FROM stv_partitions
WHERE (used::FLOAT / capacity::FLOAT) > 0.8
ORDER BY usage_percent DESC;

-- Identify large tables
SELECT 
    schemaname,
    tablename,
    size as size_mb,
    tbl_rows,
    size / NULLIF(tbl_rows, 0) as mb_per_row
FROM svv_table_info
WHERE schemaname NOT IN ('information_schema', 'pg_catalog')
ORDER BY size DESC
LIMIT 20;
```

### Q53: How do you handle connection and timeout issues?

**Answer:**
Connection management involves monitoring sessions and configuring timeouts.

```sql
-- Monitor active connections
SELECT 
    user_name,
    db_name,
    pid,
    starttime,
    status
FROM stv_sessions
WHERE user_name != 'rdsdb'
ORDER BY starttime;

-- Check for blocked queries
SELECT 
    blocked.pid as blocked_pid,
    blocked.user_name as blocked_user,
    blocking.pid as blocking_pid,
    blocking.user_name as blocking_user,
    blocked.query as blocked_query
FROM stv_locks blocked
JOIN stv_locks blocking ON blocked.table_id = blocking.table_id
WHERE blocked.granted = 'f' AND blocking.granted = 't';
```

### Q54: How do you resolve data loading errors?

**Answer:**
Data loading troubleshooting involves error analysis and data validation.

```sql
-- Check COPY errors
SELECT 
    query,
    filename,
    line_number,
    colname,
    type,
    position,
    raw_line,
    err_reason
FROM stl_load_errors
WHERE query = pg_last_query_id()
ORDER BY starttime DESC;

-- Validate data before loading
SELECT 
    COUNT(*) as total_rows,
    COUNT(CASE WHEN customer_id IS NULL THEN 1 END) as null_customer_ids,
    COUNT(CASE WHEN sale_date IS NULL THEN 1 END) as null_dates
FROM staging_table;
```

### Q55: How do you handle cluster maintenance and upgrades?

**Answer:**
Maintenance planning minimizes downtime and ensures system health.

```sql
-- Check maintenance window
SELECT 
    cluster_identifier,
    preferred_maintenance_window,
    cluster_version,
    next_maintenance_window_start_time
FROM stv_cluster_info;

-- Monitor upgrade progress
SELECT 
    upgrade_id,
    cluster_identifier,
    upgrade_type,
    start_time,
    end_time,
    status
FROM stl_upgrade
WHERE start_time >= CURRENT_DATE - 30
ORDER BY start_time DESC;

-- Pre-upgrade validation
CREATE OR REPLACE PROCEDURE pre_upgrade_check()
AS $$
BEGIN
    -- Check for long-running queries
    IF EXISTS (SELECT 1 FROM stl_query WHERE endtime IS NULL AND starttime < GETDATE() - INTERVAL '1 hour') THEN
        RAISE EXCEPTION 'Long-running queries detected';
    END IF;
    
    -- Validate data integrity
    PERFORM validate_critical_tables();
END;
$$ LANGUAGE plpgsql;
```

## Advanced Integration

### Q56: How do you integrate Redshift with AWS services?

**Answer:**
Redshift integrates with multiple AWS services for comprehensive data solutions.

```sql
-- S3 integration with Spectrum
CREATE EXTERNAL SCHEMA s3_data
FROM DATA CATALOG
DATABASE 'data_lake'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftSpectrumRole';

-- Query S3 data
SELECT COUNT(*) FROM s3_data.external_logs
WHERE log_date >= '2023-01-01';

-- Lambda integration for automation
SELECT aws_lambda_invoke(
    'arn:aws:lambda:us-east-1:123456789012:function:ProcessRedshiftData',
    '{
        "cluster": "production",
        "database": "analytics",
        "action": "refresh_materialized_views"
    }'
);
```

### Q57: How do you implement automated data quality monitoring?

**Answer:**
Automated monitoring ensures data quality through continuous validation.

```sql
-- Data quality framework
CREATE TABLE data_quality_rules (
    rule_id INTEGER IDENTITY(1,1),
    table_name VARCHAR(100),
    column_name VARCHAR(100),
    rule_type VARCHAR(50),
    rule_definition TEXT,
    threshold_value DECIMAL(10,2)
);

-- Automated quality checks
CREATE OR REPLACE PROCEDURE run_quality_checks()
AS $$
BEGIN
    -- Null value checks
    INSERT INTO quality_violations
    SELECT 
        'NULL_CHECK',
        'customers',
        'email',
        COUNT(*)
    FROM customers
    WHERE email IS NULL
    HAVING COUNT(*) > 0;
    
    -- Duplicate checks
    INSERT INTO quality_violations
    SELECT 
        'DUPLICATE_CHECK',
        'customers',
        'customer_id',
        COUNT(*) - COUNT(DISTINCT customer_id)
    FROM customers
    HAVING COUNT(*) - COUNT(DISTINCT customer_id) > 0;
END;
$$ LANGUAGE plpgsql;
```

### Q58: How do you implement cross-region disaster recovery?

**Answer:**
Cross-region DR ensures business continuity through automated replication.

```sql
-- Monitor cross-region snapshots
SELECT 
    snapshot_id,
    cluster_identifier,
    snapshot_time,
    status,
    source_region,
    destination_region
FROM stv_snapshot_copy
WHERE snapshot_time >= CURRENT_DATE - 7
ORDER BY snapshot_time DESC;

-- DR failover procedure
CREATE OR REPLACE PROCEDURE execute_dr_failover()
AS $$
BEGIN
    -- Validate DR cluster readiness
    PERFORM validate_dr_cluster();
    
    -- Update DNS records
    PERFORM update_dns_to_dr();
    
    -- Notify applications
    PERFORM notify_application_teams();
END;
$$ LANGUAGE plpgsql;
```

### Q59: How do you implement automated ETL orchestration?

**Answer:**
ETL orchestration coordinates complex data workflows.

```sql
-- ETL job metadata
CREATE TABLE etl_jobs (
    job_id INTEGER IDENTITY(1,1),
    job_name VARCHAR(100),
    job_type VARCHAR(50),
    schedule_expression VARCHAR(50),
    dependencies TEXT,
    last_run_time TIMESTAMP,
    status VARCHAR(20)
);

-- ETL orchestration procedure
CREATE OR REPLACE PROCEDURE orchestrate_etl()
AS $$
BEGIN
    -- Stage 1: Extract
    PERFORM extract_source_data();
    
    -- Stage 2: Transform
    PERFORM transform_staging_data();
    
    -- Stage 3: Load
    PERFORM load_target_tables();
    
    -- Stage 4: Validate
    PERFORM validate_etl_results();
END;
$$ LANGUAGE plpgsql;
```

### Q60: How do you implement machine learning integration?

**Answer:**
ML integration enables advanced analytics directly in Redshift.

```sql
-- Create ML model
CREATE MODEL customer_churn_model
FROM (
    SELECT 
        customer_id,
        total_orders,
        avg_order_value,
        days_since_last_order,
        churned
    FROM customer_features
)
TARGET churned
FUNCTION ml_fn_customer_churn
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftMLRole'
SETTINGS (
    S3_BUCKET 'ml-models-bucket'
);

-- Use model for predictions
SELECT 
    customer_id,
    ml_fn_customer_churn(
        total_orders,
        avg_order_value,
        days_since_last_order
    ) as churn_probability
FROM customer_features
WHERE churn_probability > 0.7;
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
13. **Real-time Analytics**: Integration with streaming services for near real-time insights
14. **Multi-tenant Architecture**: Secure data isolation and resource management
15. **Migration Strategies**: Comprehensive approaches for large-scale data warehouse migrations