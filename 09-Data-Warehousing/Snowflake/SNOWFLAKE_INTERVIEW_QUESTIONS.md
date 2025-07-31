# Snowflake Interview Questions

## Basic Level Questions (1-3 years experience)

### 1. What is Snowflake and why is it popular for data engineering?
**Answer**: Snowflake is a cloud-native data warehouse that separates compute and storage, providing scalable, flexible, and cost-effective data analytics.

**Key Benefits for Data Engineering**:
- **Separation of Compute and Storage**: Scale independently based on needs
- **Multi-Cloud Support**: Available on AWS, Azure, and GCP
- **Zero Management**: No infrastructure maintenance required
- **Automatic Scaling**: Elastic compute resources
- **Data Sharing**: Secure data sharing across organizations

```sql
-- Basic Snowflake operations
-- Create database and schema
CREATE DATABASE data_warehouse;
CREATE SCHEMA data_warehouse.sales;

-- Create table with clustering
CREATE TABLE data_warehouse.sales.fact_sales (
    sale_id NUMBER AUTOINCREMENT,
    customer_id NUMBER,
    product_id NUMBER,
    sale_date DATE,
    quantity NUMBER,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(12,2),
    region VARCHAR(50),
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
) CLUSTER BY (sale_date, region);

-- Load data from S3
COPY INTO data_warehouse.sales.fact_sales
FROM @my_s3_stage/sales_data/
FILE_FORMAT = (TYPE = 'CSV' FIELD_DELIMITER = ',' SKIP_HEADER = 1)
PATTERN = '.*sales_.*\.csv';

-- Basic analytics query
SELECT 
    region,
    DATE_TRUNC('month', sale_date) AS month,
    COUNT(*) AS transaction_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_transaction_value
FROM data_warehouse.sales.fact_sales
WHERE sale_date >= DATEADD('year', -1, CURRENT_DATE())
GROUP BY region, DATE_TRUNC('month', sale_date)
ORDER BY region, month;
```

### 2. Explain Snowflake's architecture and key components
**Answer**: Snowflake uses a unique multi-cluster, shared data architecture with three main layers.

**Architecture Components**:

```sql
-- 1. STORAGE LAYER
-- Automatically managed, compressed, and optimized
-- Data stored in micro-partitions
-- Immutable and encrypted

-- 2. COMPUTE LAYER (Virtual Warehouses)
-- Create different sized warehouses
CREATE WAREHOUSE etl_warehouse WITH
    WAREHOUSE_SIZE = 'LARGE'
    AUTO_SUSPEND = 300  -- 5 minutes
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE;

CREATE WAREHOUSE analytics_warehouse WITH
    WAREHOUSE_SIZE = 'MEDIUM'
    AUTO_SUSPEND = 60   -- 1 minute
    AUTO_RESUME = TRUE
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 3
    SCALING_POLICY = 'STANDARD';

-- 3. SERVICES LAYER
-- Authentication, metadata management, query optimization
-- Infrastructure management, security

-- Warehouse management
USE WAREHOUSE etl_warehouse;

-- Resize warehouse dynamically
ALTER WAREHOUSE etl_warehouse SET WAREHOUSE_SIZE = 'X-LARGE';

-- Suspend/Resume warehouse
ALTER WAREHOUSE etl_warehouse SUSPEND;
ALTER WAREHOUSE etl_warehouse RESUME;

-- Monitor warehouse usage
SELECT 
    warehouse_name,
    start_time,
    end_time,
    credits_used,
    credits_used_compute,
    credits_used_cloud_services
FROM snowflake.account_usage.warehouse_metering_history
WHERE start_time >= DATEADD('day', -7, CURRENT_TIMESTAMP())
ORDER BY start_time DESC;
```

### 3. How do you load data into Snowflake?
**Answer**: Snowflake provides multiple methods for data loading, from batch to real-time streaming.

```sql
-- 1. BULK LOADING WITH COPY COMMAND

-- Create file format
CREATE FILE FORMAT csv_format
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    RECORD_DELIMITER = '\n'
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    TRIM_SPACE = TRUE
    ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE
    REPLACE_INVALID_CHARACTERS = TRUE
    DATE_FORMAT = 'YYYY-MM-DD'
    TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS';

-- Create external stage
CREATE STAGE s3_data_stage
    URL = 's3://my-data-bucket/raw-data/'
    CREDENTIALS = (AWS_KEY_ID = 'your_key' AWS_SECRET_KEY = 'your_secret')
    FILE_FORMAT = csv_format;

-- Load data with error handling
COPY INTO customer_data
FROM @s3_data_stage/customers/
ON_ERROR = 'CONTINUE'
RETURN_FAILED_ONLY = TRUE;

-- Check load status
SELECT * FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => 'CUSTOMER_DATA',
    START_TIME => DATEADD('hour', -1, CURRENT_TIMESTAMP())
));

-- 2. STREAMING DATA WITH SNOWPIPE

-- Create pipe for automatic loading
CREATE PIPE customer_pipe
    AUTO_INGEST = TRUE
    AS COPY INTO customer_data
    FROM @s3_data_stage/customers/
    FILE_FORMAT = csv_format;

-- Show pipe status
SELECT SYSTEM$PIPE_STATUS('customer_pipe');

-- 3. REAL-TIME STREAMING WITH KAFKA
-- Create stream for change data capture
CREATE STREAM customer_stream ON TABLE customer_data;

-- Process stream data
MERGE INTO customer_summary s
USING (
    SELECT 
        customer_id,
        SUM(CASE WHEN metadata$action = 'INSERT' THEN 1 ELSE -1 END) AS net_change,
        MAX(metadata$isupdate) AS is_update
    FROM customer_stream
    GROUP BY customer_id
) t ON s.customer_id = t.customer_id
WHEN MATCHED AND t.is_update THEN
    UPDATE SET last_updated = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN
    INSERT (customer_id, created_at) VALUES (t.customer_id, CURRENT_TIMESTAMP());

-- 4. LOADING WITH PYTHON CONNECTOR
```

```python
import snowflake.connector
import pandas as pd

# Snowflake connection
def connect_to_snowflake():
    """Establish connection to Snowflake."""
    
    conn = snowflake.connector.connect(
        user='your_username',
        password='your_password',
        account='your_account',
        warehouse='etl_warehouse',
        database='data_warehouse',
        schema='sales'
    )
    
    return conn

# Load DataFrame to Snowflake
def load_dataframe_to_snowflake(df, table_name):
    """Load pandas DataFrame to Snowflake table."""
    
    conn = connect_to_snowflake()
    
    # Write DataFrame to Snowflake
    success, nchunks, nrows, _ = write_pandas(
        conn, 
        df, 
        table_name,
        auto_create_table=True,
        overwrite=True
    )
    
    print(f"Loaded {nrows} rows in {nchunks} chunks")
    conn.close()

# Bulk insert with staging
def bulk_insert_with_staging(data_file, table_name):
    """Bulk insert using internal staging."""
    
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    
    try:
        # Create internal stage
        cursor.execute("CREATE OR REPLACE STAGE temp_stage")
        
        # Upload file to stage
        cursor.execute(f"PUT file://{data_file} @temp_stage")
        
        # Copy from stage to table
        cursor.execute(f"""
            COPY INTO {table_name}
            FROM @temp_stage
            FILE_FORMAT = (TYPE = 'CSV' FIELD_DELIMITER = ',' SKIP_HEADER = 1)
            ON_ERROR = 'CONTINUE'
        """)
        
        # Get load results
        cursor.execute("SELECT * FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))")
        results = cursor.fetchall()
        
        print(f"Load completed: {results}")
        
    finally:
        cursor.close()
        conn.close()
```

### 4. How do you optimize query performance in Snowflake?
**Answer**: Use clustering, partitioning, caching, and query optimization techniques.

```sql
-- 1. CLUSTERING KEYS
-- Analyze clustering depth
SELECT SYSTEM$CLUSTERING_DEPTH('fact_sales', '(sale_date, region)');

-- Add clustering key to existing table
ALTER TABLE fact_sales CLUSTER BY (sale_date, region);

-- Monitor clustering information
SELECT 
    table_name,
    clustering_key,
    total_partition_count,
    total_constant_partition_count,
    average_overlaps,
    average_depth
FROM snowflake.information_schema.automatic_clustering_history
WHERE table_name = 'FACT_SALES'
ORDER BY start_time DESC;

-- 2. QUERY OPTIMIZATION TECHNIQUES

-- Use appropriate data types
CREATE TABLE optimized_sales (
    sale_id NUMBER(18,0),           -- Instead of generic NUMBER
    customer_id NUMBER(10,0),       -- Smaller precision when possible
    sale_date DATE,                 -- Not TIMESTAMP if time not needed
    amount DECIMAL(12,2),           -- Exact precision for money
    status VARCHAR(20),             -- Specific length instead of VARCHAR
    metadata VARIANT                -- For semi-structured data
);

-- Efficient filtering with clustering
SELECT *
FROM fact_sales
WHERE sale_date BETWEEN '2024-01-01' AND '2024-01-31'  -- Clustered column first
  AND region = 'North America'                          -- Then other filters
  AND total_amount > 1000;

-- Use appropriate JOIN strategies
-- Small dimension tables - use broadcast join
SELECT /*+ USE_CACHED_RESULT(FALSE) */
    f.sale_id,
    d.product_name,
    c.customer_name,
    f.total_amount
FROM fact_sales f
JOIN dim_product d ON f.product_id = d.product_id      -- Small table
JOIN dim_customer c ON f.customer_id = c.customer_id   -- Small table
WHERE f.sale_date >= CURRENT_DATE() - 30;

-- 3. RESULT CACHING
-- Enable result caching (default)
ALTER SESSION SET USE_CACHED_RESULT = TRUE;

-- Check if query used cache
SELECT 
    query_id,
    query_text,
    execution_status,
    total_elapsed_time,
    bytes_scanned,
    result_cache_hit
FROM snowflake.information_schema.query_history
WHERE query_text ILIKE '%fact_sales%'
ORDER BY start_time DESC
LIMIT 10;

-- 4. WAREHOUSE SIZING AND SCALING
-- Monitor warehouse performance
SELECT 
    warehouse_name,
    avg_running,
    avg_queued_load,
    avg_queued_provisioning,
    avg_blocked
FROM snowflake.information_schema.warehouse_load_history
WHERE start_time >= DATEADD('hour', -24, CURRENT_TIMESTAMP())
ORDER BY start_time DESC;

-- Auto-scaling configuration
ALTER WAREHOUSE analytics_warehouse SET
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 5
    SCALING_POLICY = 'STANDARD'
    AUTO_SUSPEND = 300;

-- 5. QUERY PROFILING
-- Analyze query profile
SELECT 
    query_id,
    query_text,
    database_name,
    schema_name,
    query_type,
    warehouse_name,
    warehouse_size,
    execution_status,
    error_code,
    error_message,
    start_time,
    end_time,
    total_elapsed_time,
    bytes_scanned,
    percentage_scanned_from_cache,
    bytes_written,
    bytes_written_to_result,
    rows_produced,
    compilation_time,
    execution_time,
    queued_provisioning_time,
    queued_repair_time,
    queued_overload_time,
    transaction_blocked_time
FROM snowflake.information_schema.query_history
WHERE query_text ILIKE '%your_query_pattern%'
ORDER BY start_time DESC;
```

### 5. How do you implement data security in Snowflake?
**Answer**: Use role-based access control, data masking, encryption, and network policies.

```sql
-- 1. ROLE-BASED ACCESS CONTROL (RBAC)

-- Create custom roles
CREATE ROLE data_engineer;
CREATE ROLE data_analyst;
CREATE ROLE data_scientist;

-- Grant privileges to roles
GRANT USAGE ON DATABASE data_warehouse TO ROLE data_engineer;
GRANT USAGE ON SCHEMA data_warehouse.sales TO ROLE data_engineer;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA data_warehouse.sales TO ROLE data_engineer;

GRANT USAGE ON DATABASE data_warehouse TO ROLE data_analyst;
GRANT USAGE ON SCHEMA data_warehouse.sales TO ROLE data_analyst;
GRANT SELECT ON ALL TABLES IN SCHEMA data_warehouse.sales TO ROLE data_analyst;

-- Create role hierarchy
GRANT ROLE data_analyst TO ROLE data_engineer;
GRANT ROLE data_engineer TO ROLE sysadmin;

-- Grant roles to users
GRANT ROLE data_analyst TO USER john_analyst;
GRANT ROLE data_engineer TO USER jane_engineer;

-- 2. DYNAMIC DATA MASKING

-- Create masking policy
CREATE MASKING POLICY email_mask AS (val STRING) RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() IN ('DATA_ENGINEER', 'SYSADMIN') THEN val
        ELSE REGEXP_REPLACE(val, '.+@', '*****@')
    END;

-- Apply masking policy to column
ALTER TABLE customer_data MODIFY COLUMN email 
SET MASKING POLICY email_mask;

-- Create conditional masking policy
CREATE MASKING POLICY ssn_mask AS (val STRING) RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() IN ('COMPLIANCE_OFFICER', 'SYSADMIN') THEN val
        WHEN CURRENT_ROLE() IN ('DATA_ANALYST') THEN 'XXX-XX-' || RIGHT(val, 4)
        ELSE 'XXX-XX-XXXX'
    END;

-- 3. ROW ACCESS POLICIES

-- Create row access policy
CREATE ROW ACCESS POLICY region_policy AS (region_column STRING) RETURNS BOOLEAN ->
    CASE
        WHEN CURRENT_ROLE() = 'GLOBAL_ADMIN' THEN TRUE
        WHEN CURRENT_ROLE() = 'NA_ANALYST' AND region_column = 'North America' THEN TRUE
        WHEN CURRENT_ROLE() = 'EU_ANALYST' AND region_column = 'Europe' THEN TRUE
        ELSE FALSE
    END;

-- Apply row access policy
ALTER TABLE sales_data ADD ROW ACCESS POLICY region_policy ON (region);

-- 4. NETWORK POLICIES

-- Create network policy
CREATE NETWORK POLICY corporate_network
    ALLOWED_IP_LIST = ('192.168.1.0/24', '10.0.0.0/8')
    BLOCKED_IP_LIST = ('192.168.1.99');

-- Apply to account
ALTER ACCOUNT SET NETWORK_POLICY = corporate_network;

-- Apply to specific user
ALTER USER sensitive_user SET NETWORK_POLICY = corporate_network;

-- 5. ENCRYPTION AND KEY MANAGEMENT

-- Customer-managed keys (CMK)
CREATE STAGE encrypted_stage
    URL = 's3://my-encrypted-bucket/'
    ENCRYPTION = (TYPE = 'AWS_CSE' MASTER_KEY = 'your-kms-key-id');

-- Column-level encryption
CREATE TABLE sensitive_data (
    id NUMBER,
    name VARCHAR(100),
    ssn VARCHAR(11) ENCRYPT,  -- Column-level encryption
    salary NUMBER ENCRYPT
);

-- 6. AUDIT AND MONITORING

-- Monitor login attempts
SELECT 
    user_name,
    client_ip,
    reported_client_type,
    reported_client_version,
    first_authentication_factor,
    second_authentication_factor,
    is_success,
    error_code,
    error_message,
    event_timestamp
FROM snowflake.information_schema.login_history
WHERE event_timestamp >= DATEADD('day', -7, CURRENT_TIMESTAMP())
ORDER BY event_timestamp DESC;

-- Monitor data access
SELECT 
    user_name,
    role_name,
    query_text,
    database_name,
    schema_name,
    execution_status,
    start_time,
    end_time,
    rows_produced,
    bytes_scanned
FROM snowflake.information_schema.query_history
WHERE query_text ILIKE '%sensitive_table%'
  AND start_time >= DATEADD('day', -1, CURRENT_TIMESTAMP())
ORDER BY start_time DESC;

-- Create alerts for suspicious activity
CREATE ALERT suspicious_access
    WAREHOUSE = monitoring_warehouse
    SCHEDULE = '5 MINUTE'
    IF (EXISTS (
        SELECT 1 
        FROM snowflake.information_schema.query_history 
        WHERE start_time >= DATEADD('minute', -5, CURRENT_TIMESTAMP())
          AND user_name NOT IN ('ETL_USER', 'SERVICE_ACCOUNT')
          AND query_text ILIKE '%DROP%'
          AND execution_status = 'SUCCESS'
    ))
    THEN CALL send_notification('Suspicious DROP operation detected');
```

## Intermediate Level Questions (3-5 years experience)

### 6. How do you implement Change Data Capture (CDC) in Snowflake?
**Answer**: Use Snowflake Streams and Tasks for automated change data capture and processing.

```sql
-- 1. CREATE STREAMS FOR CDC

-- Create stream on source table
CREATE STREAM customer_changes ON TABLE customer_data;

-- Create stream with specific options
CREATE STREAM order_changes ON TABLE orders
    APPEND_ONLY = FALSE  -- Capture all DML operations
    SHOW_INITIAL_ROWS = FALSE;  -- Don't show existing rows

-- 2. PROCESS STREAM DATA

-- View stream contents
SELECT 
    customer_id,
    customer_name,
    email,
    METADATA$ACTION,
    METADATA$ISUPDATE,
    METADATA$ROW_ID
FROM customer_changes;

-- Process incremental changes
MERGE INTO customer_summary cs
USING (
    SELECT 
        customer_id,
        customer_name,
        email,
        region,
        METADATA$ACTION as action,
        METADATA$ISUPDATE as is_update
    FROM customer_changes
) cc ON cs.customer_id = cc.customer_id
WHEN MATCHED AND cc.action = 'DELETE' THEN
    DELETE
WHEN MATCHED AND cc.action = 'INSERT' AND cc.is_update = TRUE THEN
    UPDATE SET 
        customer_name = cc.customer_name,
        email = cc.email,
        region = cc.region,
        last_updated = CURRENT_TIMESTAMP()
WHEN NOT MATCHED AND cc.action = 'INSERT' THEN
    INSERT (customer_id, customer_name, email, region, created_at)
    VALUES (cc.customer_id, cc.customer_name, cc.email, cc.region, CURRENT_TIMESTAMP());

-- 3. AUTOMATE WITH TASKS

-- Create task to process stream
CREATE TASK process_customer_changes
    WAREHOUSE = etl_warehouse
    SCHEDULE = '5 MINUTE'
    WHEN SYSTEM$STREAM_HAS_DATA('customer_changes')
    AS
    MERGE INTO customer_summary cs
    USING (
        SELECT 
            customer_id,
            customer_name,
            email,
            region,
            METADATA$ACTION as action,
            METADATA$ISUPDATE as is_update
        FROM customer_changes
    ) cc ON cs.customer_id = cc.customer_id
    WHEN MATCHED AND cc.action = 'DELETE' THEN DELETE
    WHEN MATCHED AND cc.action = 'INSERT' AND cc.is_update = TRUE THEN
        UPDATE SET 
            customer_name = cc.customer_name,
            email = cc.email,
            region = cc.region,
            last_updated = CURRENT_TIMESTAMP()
    WHEN NOT MATCHED AND cc.action = 'INSERT' THEN
        INSERT (customer_id, customer_name, email, region, created_at)
        VALUES (cc.customer_id, cc.customer_name, cc.email, cc.region, CURRENT_TIMESTAMP());

-- Start the task
ALTER TASK process_customer_changes RESUME;

-- 4. TASK DEPENDENCIES

-- Create parent task
CREATE TASK extract_data
    WAREHOUSE = etl_warehouse
    SCHEDULE = '1 HOUR'
    AS
    COPY INTO staging_table FROM @external_stage;

-- Create dependent task
CREATE TASK transform_data
    WAREHOUSE = etl_warehouse
    AFTER extract_data
    AS
    INSERT INTO processed_table
    SELECT * FROM staging_table WHERE status = 'valid';

-- Create final task
CREATE TASK load_data
    WAREHOUSE = etl_warehouse
    AFTER transform_data
    AS
    MERGE INTO target_table USING processed_table ON ...;

-- Resume all tasks in dependency order
ALTER TASK extract_data RESUME;
ALTER TASK transform_data RESUME;
ALTER TASK load_data RESUME;

-- 5. MONITOR TASKS AND STREAMS

-- Monitor task execution
SELECT 
    name,
    database_name,
    schema_name,
    state,
    scheduled_time,
    query_start_time,
    next_scheduled_time,
    completed_time,
    return_value,
    error_code,
    error_message
FROM snowflake.information_schema.task_history
WHERE scheduled_time >= DATEADD('day', -1, CURRENT_TIMESTAMP())
ORDER BY scheduled_time DESC;

-- Monitor stream consumption
SELECT 
    table_name,
    stream_name,
    bytes,
    rows,
    stale_after,
    created_on
FROM snowflake.information_schema.streams
WHERE table_schema = 'SALES';

-- Check stream lag
SELECT 
    SYSTEM$STREAM_GET_TABLE_TIMESTAMP('customer_changes') as stream_timestamp,
    CURRENT_TIMESTAMP() as current_timestamp,
    DATEDIFF('second', stream_timestamp, CURRENT_TIMESTAMP()) as lag_seconds;
```

### 7. How do you implement data sharing in Snowflake?
**Answer**: Use Snowflake's native data sharing capabilities for secure, real-time data collaboration.

```sql
-- 1. CREATE SHARE (Data Provider)

-- Create share
CREATE SHARE sales_data_share;

-- Grant database access to share
GRANT USAGE ON DATABASE data_warehouse TO SHARE sales_data_share;
GRANT USAGE ON SCHEMA data_warehouse.sales TO SHARE sales_data_share;

-- Grant table access
GRANT SELECT ON TABLE data_warehouse.sales.fact_sales TO SHARE sales_data_share;
GRANT SELECT ON TABLE data_warehouse.sales.dim_product TO SHARE sales_data_share;

-- Create secure view for sharing
CREATE SECURE VIEW data_warehouse.sales.shared_sales_summary AS
SELECT 
    DATE_TRUNC('month', sale_date) as month,
    product_category,
    region,
    COUNT(*) as transaction_count,
    SUM(total_amount) as total_revenue
FROM data_warehouse.sales.fact_sales f
JOIN data_warehouse.sales.dim_product p ON f.product_id = p.product_id
WHERE sale_date >= DATEADD('year', -2, CURRENT_DATE())
GROUP BY 1, 2, 3;

-- Grant view access to share
GRANT SELECT ON VIEW data_warehouse.sales.shared_sales_summary TO SHARE sales_data_share;

-- Add consumer account to share
ALTER SHARE sales_data_share ADD ACCOUNTS = ('consumer_account_1', 'consumer_account_2');

-- 2. CONSUME SHARED DATA (Data Consumer)

-- Show available shares
SHOW SHARES;

-- Create database from share
CREATE DATABASE shared_sales_data FROM SHARE provider_account.sales_data_share;

-- Query shared data
SELECT * FROM shared_sales_data.sales.shared_sales_summary
WHERE month >= '2024-01-01';

-- 3. SECURE DATA SHARING WITH ROW-LEVEL SECURITY

-- Create mapping table for consumer access
CREATE TABLE consumer_access_mapping (
    consumer_account VARCHAR(100),
    allowed_regions ARRAY
);

INSERT INTO consumer_access_mapping VALUES
('consumer_account_1', ARRAY_CONSTRUCT('North America', 'Europe')),
('consumer_account_2', ARRAY_CONSTRUCT('Asia Pacific'));

-- Create secure view with row-level filtering
CREATE SECURE VIEW shared_regional_sales AS
SELECT 
    s.sale_date,
    s.product_id,
    s.total_amount,
    s.region
FROM data_warehouse.sales.fact_sales s
JOIN consumer_access_mapping cam ON ARRAY_CONTAINS(s.region::VARIANT, cam.allowed_regions)
WHERE cam.consumer_account = CURRENT_ACCOUNT();

-- 4. MONITOR DATA SHARING

-- Monitor share usage (Provider)
SELECT 
    share_name,
    consumer_account_name,
    consumer_account_locator,
    is_share_restricted,
    created_on,
    kind
FROM snowflake.information_schema.shares;

-- Monitor shared object access
SELECT 
    share_name,
    consumer_account_name,
    object_name,
    object_type,
    granted_on,
    granted_by
FROM snowflake.information_schema.grants_to_shares
WHERE share_name = 'SALES_DATA_SHARE';

-- 5. DATA MARKETPLACE INTEGRATION

-- Create listing for Snowflake Marketplace
CREATE DATA EXCHANGE my_company_exchange;

-- Add share to exchange
ALTER DATA EXCHANGE my_company_exchange ADD SHARE sales_data_share;

-- Create listing
CREATE LISTING sales_analytics_listing
    FOR SHARE sales_data_share
    IN DATA EXCHANGE my_company_exchange;
```

This comprehensive Snowflake documentation covers fundamental concepts through advanced data sharing and CDC implementations essential for modern data engineering.