# Snowflake Interview Questions for Data Engineering

## Basic Level Questions (1-8)

### 1. What is Snowflake and how does it differ from traditional data warehouses?
**Answer:**
Snowflake is a cloud-native data warehouse built for the cloud with a unique multi-cluster, shared data architecture.

**Key Differences:**
- **Separation of Storage and Compute**: Scale independently
- **Multi-cluster Architecture**: Automatic scaling and concurrency
- **Zero Management**: No infrastructure to manage
- **Pay-per-use**: Only pay for what you use
- **Cross-cloud**: Available on AWS, Azure, and GCP

```sql
-- Snowflake's unique features
-- Virtual warehouses can be resized instantly
ALTER WAREHOUSE my_warehouse SET WAREHOUSE_SIZE = 'LARGE';

-- Time travel without additional storage cost
SELECT * FROM my_table AT (TIMESTAMP => '2024-01-01 10:00:00');

-- Zero-copy cloning
CREATE TABLE my_table_clone CLONE my_table;
```

### 2. Explain Snowflake's architecture components
**Answer:**
**Three-layer Architecture:**
- **Storage Layer**: Stores data in micro-partitions
- **Compute Layer**: Virtual warehouses process queries
- **Services Layer**: Manages metadata, security, optimization

```sql
-- Storage layer - automatic micro-partitioning
CREATE TABLE sales (
    id NUMBER,
    sale_date DATE,
    amount DECIMAL(10,2),
    region STRING
);

-- Compute layer - virtual warehouses
CREATE WAREHOUSE analytics_wh WITH
    WAREHOUSE_SIZE = 'MEDIUM'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE;

-- Services layer - automatic optimization
-- Snowflake automatically maintains statistics and optimizes queries
```

### 3. What are Virtual Warehouses and how do they work?
**Answer:**
Virtual Warehouses are compute clusters that execute queries and DML operations.

**Key Features:**
- **Independent Scaling**: Each warehouse scales independently
- **Auto-suspend/Resume**: Automatically pause when idle
- **Multi-cluster**: Scale out for concurrency
- **Instant Resize**: Change size without downtime

```sql
-- Create virtual warehouse
CREATE WAREHOUSE data_loading_wh WITH
    WAREHOUSE_SIZE = 'X-LARGE'
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 5
    SCALING_POLICY = 'STANDARD'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE;

-- Use specific warehouse
USE WAREHOUSE data_loading_wh;

-- Monitor warehouse usage
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE WAREHOUSE_NAME = 'DATA_LOADING_WH'
ORDER BY START_TIME DESC;
```

### 4. How does Snowflake handle data storage and micro-partitions?
**Answer:**
Snowflake automatically organizes data into micro-partitions (50-500MB compressed).

**Micro-partition Benefits:**
- **Automatic Clustering**: No manual partitioning needed
- **Pruning**: Skip irrelevant micro-partitions
- **Compression**: Automatic compression
- **Metadata**: Rich metadata for optimization

```sql
-- Snowflake automatically creates micro-partitions
INSERT INTO sales VALUES 
(1, '2024-01-01', 100.00, 'US'),
(2, '2024-01-02', 150.00, 'EU'),
(3, '2024-01-03', 200.00, 'APAC');

-- View clustering information
SELECT SYSTEM$CLUSTERING_INFORMATION('sales', '(sale_date)');

-- Manual clustering for better performance
ALTER TABLE sales CLUSTER BY (sale_date, region);
```

### 5. What is Time Travel in Snowflake?
**Answer:**
Time Travel allows querying historical data within a retention period (1-90 days).

**Use Cases:**
- **Data Recovery**: Restore accidentally deleted data
- **Historical Analysis**: Compare data at different points
- **Auditing**: Track data changes over time
- **Debugging**: Investigate data issues

```sql
-- Query data as of specific timestamp
SELECT * FROM customers AT (TIMESTAMP => '2024-01-01 10:00:00');

-- Query data as of specific offset
SELECT * FROM customers AT (OFFSET => -3600); -- 1 hour ago

-- Query data before statement execution
SELECT * FROM customers BEFORE (STATEMENT => '01a1b2c3-0000-0000-0000-000000000000');

-- Restore dropped table
UNDROP TABLE customers;

-- Set retention period
ALTER TABLE customers SET DATA_RETENTION_TIME_IN_DAYS = 7;
```

### 6. How do you load data into Snowflake?
**Answer:**
Multiple methods for data loading:

**Bulk Loading:**
```sql
-- Create file format
CREATE FILE FORMAT csv_format
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    NULL_IF = ('NULL', 'null', '')
    EMPTY_FIELD_AS_NULL = TRUE;

-- Create stage
CREATE STAGE my_s3_stage
    URL = 's3://my-bucket/data/'
    CREDENTIALS = (AWS_KEY_ID = 'xxx' AWS_SECRET_KEY = 'yyy')
    FILE_FORMAT = csv_format;

-- Load data using COPY command
COPY INTO customers
FROM @my_s3_stage/customers.csv
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE';

-- Monitor load status
SELECT * FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => 'CUSTOMERS',
    START_TIME => DATEADD(HOUR, -1, CURRENT_TIMESTAMP())
));
```

**Streaming:**
```sql
-- Snowpipe for continuous loading
CREATE PIPE customer_pipe AS
COPY INTO customers
FROM @my_s3_stage
FILE_FORMAT = csv_format;

-- Show pipe status
SELECT SYSTEM$PIPE_STATUS('customer_pipe');
```

### 7. What are Snowflake's data types and how do you work with semi-structured data?
**Answer:**
```sql
-- Standard data types
CREATE TABLE products (
    id NUMBER(10,0),
    name VARCHAR(100),
    price DECIMAL(10,2),
    created_date DATE,
    created_timestamp TIMESTAMP_NTZ,
    is_active BOOLEAN
);

-- Semi-structured data with VARIANT
CREATE TABLE events (
    id NUMBER,
    event_data VARIANT,
    event_timestamp TIMESTAMP
);

-- Insert JSON data
INSERT INTO events VALUES 
(1, PARSE_JSON('{"user_id": 123, "action": "login", "metadata": {"ip": "192.168.1.1"}}'), CURRENT_TIMESTAMP());

-- Query JSON data
SELECT 
    id,
    event_data:user_id::NUMBER as user_id,
    event_data:action::STRING as action,
    event_data:metadata.ip::STRING as ip_address
FROM events;

-- Flatten nested arrays
SELECT 
    id,
    f.value:name::STRING as product_name,
    f.value:price::NUMBER as product_price
FROM events,
LATERAL FLATTEN(input => event_data:products) f;
```

### 8. How do you manage security and access control in Snowflake?
**Answer:**
```sql
-- Role-based access control
CREATE ROLE data_engineer;
CREATE ROLE data_analyst;

-- Grant privileges to roles
GRANT USAGE ON WAREHOUSE analytics_wh TO ROLE data_analyst;
GRANT USAGE ON DATABASE production TO ROLE data_analyst;
GRANT USAGE ON SCHEMA production.sales TO ROLE data_analyst;
GRANT SELECT ON ALL TABLES IN SCHEMA production.sales TO ROLE data_analyst;

-- Create users and assign roles
CREATE USER john_doe PASSWORD = 'SecurePassword123' DEFAULT_ROLE = data_analyst;
GRANT ROLE data_analyst TO USER john_doe;

-- Row-level security
CREATE ROW ACCESS POLICY region_policy AS (region_column STRING) RETURNS BOOLEAN ->
    CURRENT_ROLE() = 'ADMIN' OR 
    (CURRENT_ROLE() = 'US_ANALYST' AND region_column = 'US') OR
    (CURRENT_ROLE() = 'EU_ANALYST' AND region_column = 'EU');

ALTER TABLE sales ADD ROW ACCESS POLICY region_policy ON (region);

-- Column-level security (masking)
CREATE MASKING POLICY email_mask AS (val STRING) RETURNS STRING ->
    CASE 
        WHEN CURRENT_ROLE() IN ('ADMIN', 'DATA_ENGINEER') THEN val
        ELSE REGEXP_REPLACE(val, '.+@', '*****@')
    END;

ALTER TABLE customers MODIFY COLUMN email SET MASKING POLICY email_mask;
```

## Intermediate Level Questions (9-16)

### 9. How do you optimize query performance in Snowflake?
**Answer:**
```sql
-- 1. Use clustering keys for large tables
ALTER TABLE large_table CLUSTER BY (date_column, category);

-- 2. Analyze query profile
-- Use Snowflake UI Query Profile or:
SELECT * FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())
WHERE QUERY_TEXT ILIKE '%your_query%'
ORDER BY START_TIME DESC;

-- 3. Use appropriate warehouse size
-- Start small and scale up if needed
ALTER WAREHOUSE my_wh SET WAREHOUSE_SIZE = 'LARGE';

-- 4. Optimize joins
-- Use broadcast joins for small tables
SELECT /*+ USE_BROADCAST_JOIN */ 
    l.*, s.category
FROM large_table l
JOIN small_table s ON l.id = s.id;

-- 5. Use result caching
-- Identical queries return cached results within 24 hours
SELECT COUNT(*) FROM sales WHERE date >= '2024-01-01';

-- 6. Partition pruning
-- Structure queries to eliminate micro-partitions
SELECT * FROM sales 
WHERE sale_date BETWEEN '2024-01-01' AND '2024-01-31'
  AND region = 'US';

-- 7. Use LIMIT for exploratory queries
SELECT * FROM large_table LIMIT 1000;

-- 8. Monitor warehouse utilization
SELECT 
    WAREHOUSE_NAME,
    AVG(AVG_RUNNING) as avg_queries_running,
    AVG(AVG_QUEUED_LOAD) as avg_queued_load
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_LOAD_HISTORY
WHERE START_TIME >= DATEADD(DAY, -7, CURRENT_TIMESTAMP())
GROUP BY WAREHOUSE_NAME;
```

### 10. How do you implement Change Data Capture (CDC) in Snowflake?
**Answer:**
```sql
-- Using Streams for CDC
CREATE STREAM customer_stream ON TABLE customers;

-- View stream contents
SELECT * FROM customer_stream;

-- Process changes
MERGE INTO customer_summary cs
USING customer_stream s ON cs.customer_id = s.customer_id
WHEN MATCHED AND s.METADATA$ACTION = 'DELETE' THEN DELETE
WHEN MATCHED AND s.METADATA$ACTION = 'INSERT' THEN 
    UPDATE SET 
        total_orders = cs.total_orders + 1,
        last_updated = CURRENT_TIMESTAMP()
WHEN NOT MATCHED AND s.METADATA$ACTION = 'INSERT' THEN
    INSERT (customer_id, total_orders, last_updated)
    VALUES (s.customer_id, 1, CURRENT_TIMESTAMP());

-- Create task to process stream automatically
CREATE TASK process_customer_changes
    WAREHOUSE = 'ETL_WH'
    SCHEDULE = '5 MINUTE'
AS
    MERGE INTO customer_summary cs
    USING customer_stream s ON cs.customer_id = s.customer_id
    WHEN MATCHED AND s.METADATA$ACTION = 'DELETE' THEN DELETE
    WHEN MATCHED THEN 
        UPDATE SET last_updated = CURRENT_TIMESTAMP()
    WHEN NOT MATCHED THEN
        INSERT (customer_id, last_updated)
        VALUES (s.customer_id, CURRENT_TIMESTAMP());

-- Enable task
ALTER TASK process_customer_changes RESUME;

-- Monitor task execution
SELECT * FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY())
WHERE NAME = 'PROCESS_CUSTOMER_CHANGES'
ORDER BY SCHEDULED_TIME DESC;
```

### 11. How do you implement data sharing in Snowflake?
**Answer:**
```sql
-- Create share (as data provider)
CREATE SHARE sales_data_share;

-- Grant usage on database and schema
GRANT USAGE ON DATABASE production TO SHARE sales_data_share;
GRANT USAGE ON SCHEMA production.sales TO SHARE sales_data_share;

-- Grant select on specific tables
GRANT SELECT ON TABLE production.sales.orders TO SHARE sales_data_share;
GRANT SELECT ON TABLE production.sales.customers TO SHARE sales_data_share;

-- Add accounts to share
ALTER SHARE sales_data_share ADD ACCOUNTS = account1, account2;

-- Create secure view for sharing
CREATE SECURE VIEW shared_sales_summary AS
SELECT 
    DATE_TRUNC('MONTH', order_date) as month,
    region,
    SUM(amount) as total_sales,
    COUNT(*) as order_count
FROM production.sales.orders
WHERE order_date >= DATEADD(YEAR, -1, CURRENT_DATE())
GROUP BY 1, 2;

GRANT SELECT ON VIEW shared_sales_summary TO SHARE sales_data_share;

-- As data consumer, create database from share
CREATE DATABASE shared_sales_data FROM SHARE provider_account.sales_data_share;

-- Query shared data
SELECT * FROM shared_sales_data.sales.shared_sales_summary;

-- Monitor share usage
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.DATA_TRANSFER_HISTORY
WHERE SOURCE_CLOUD = 'AWS' AND TARGET_CLOUD = 'AWS'
ORDER BY START_TIME DESC;
```

### 12. How do you work with external data using External Tables?
**Answer:**
```sql
-- Create external stage
CREATE STAGE external_s3_stage
    URL = 's3://external-bucket/data/'
    CREDENTIALS = (AWS_KEY_ID = 'xxx' AWS_SECRET_KEY = 'yyy');

-- Create file format for external data
CREATE FILE FORMAT parquet_format TYPE = 'PARQUET';

-- Create external table
CREATE EXTERNAL TABLE external_sales (
    order_id NUMBER AS (value:c1::NUMBER),
    customer_id NUMBER AS (value:c2::NUMBER),
    order_date DATE AS (value:c3::DATE),
    amount DECIMAL(10,2) AS (value:c4::DECIMAL(10,2))
)
WITH LOCATION = @external_s3_stage
FILE_FORMAT = parquet_format
AUTO_REFRESH = TRUE;

-- Query external table
SELECT 
    DATE_TRUNC('MONTH', order_date) as month,
    COUNT(*) as order_count,
    SUM(amount) as total_sales
FROM external_sales
WHERE order_date >= '2024-01-01'
GROUP BY 1
ORDER BY 1;

-- Materialize external data for better performance
CREATE TABLE materialized_sales AS
SELECT * FROM external_sales
WHERE order_date >= DATEADD(YEAR, -1, CURRENT_DATE());

-- Set up automatic refresh
ALTER EXTERNAL TABLE external_sales REFRESH;

-- Monitor external table metadata
SELECT * FROM TABLE(INFORMATION_SCHEMA.EXTERNAL_TABLE_FILES(
    TABLE_NAME => 'EXTERNAL_SALES'
));
```

### 13. How do you implement data pipelines using Tasks and Stored Procedures?
**Answer:**
```sql
-- Create stored procedure for data transformation
CREATE OR REPLACE PROCEDURE transform_sales_data()
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    row_count NUMBER;
BEGIN
    -- Transform raw data
    CREATE OR REPLACE TRANSIENT TABLE sales_staging AS
    SELECT 
        order_id,
        customer_id,
        order_date,
        amount,
        CASE 
            WHEN amount > 1000 THEN 'High Value'
            WHEN amount > 100 THEN 'Medium Value'
            ELSE 'Low Value'
        END as value_category,
        CURRENT_TIMESTAMP() as processed_at
    FROM raw_sales
    WHERE order_date >= CURRENT_DATE - 1;
    
    -- Get row count
    SELECT COUNT(*) INTO row_count FROM sales_staging;
    
    -- Merge into target table
    MERGE INTO sales_fact sf
    USING sales_staging ss ON sf.order_id = ss.order_id
    WHEN MATCHED THEN 
        UPDATE SET 
            amount = ss.amount,
            value_category = ss.value_category,
            updated_at = ss.processed_at
    WHEN NOT MATCHED THEN
        INSERT (order_id, customer_id, order_date, amount, value_category, created_at)
        VALUES (ss.order_id, ss.customer_id, ss.order_date, ss.amount, ss.value_category, ss.processed_at);
    
    -- Clean up staging table
    DROP TABLE sales_staging;
    
    RETURN 'Processed ' || row_count || ' records successfully';
END;
$$;

-- Create task tree for data pipeline
CREATE TASK extract_task
    WAREHOUSE = 'ETL_WH'
    SCHEDULE = 'USING CRON 0 2 * * * UTC'  -- Daily at 2 AM
AS
    COPY INTO raw_sales FROM @data_stage;

CREATE TASK transform_task
    WAREHOUSE = 'ETL_WH'
    AFTER extract_task
AS
    CALL transform_sales_data();

CREATE TASK aggregate_task
    WAREHOUSE = 'ETL_WH'
    AFTER transform_task
AS
    CREATE OR REPLACE TABLE daily_sales_summary AS
    SELECT 
        order_date,
        value_category,
        COUNT(*) as order_count,
        SUM(amount) as total_amount,
        AVG(amount) as avg_amount
    FROM sales_fact
    WHERE order_date >= CURRENT_DATE - 1
    GROUP BY order_date, value_category;

-- Enable tasks (start from root)
ALTER TASK extract_task RESUME;
ALTER TASK transform_task RESUME;
ALTER TASK aggregate_task RESUME;

-- Monitor task execution
SELECT 
    name,
    state,
    scheduled_time,
    completed_time,
    return_value,
    error_code,
    error_message
FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY())
WHERE scheduled_time >= DATEADD(DAY, -1, CURRENT_TIMESTAMP())
ORDER BY scheduled_time DESC;
```

### 14. How do you handle large-scale data loading and optimization?
**Answer:**
```sql
-- Optimize file sizes (100-250MB compressed recommended)
-- Use multiple files instead of single large file

-- Create optimized file format
CREATE FILE FORMAT optimized_csv
    TYPE = 'CSV'
    COMPRESSION = 'GZIP'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    NULL_IF = ('NULL', 'null', '', '\\N')
    EMPTY_FIELD_AS_NULL = TRUE
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    ESCAPE_UNENCLOSED_FIELD = NONE;

-- Use appropriate warehouse size for loading
CREATE WAREHOUSE loading_wh WITH
    WAREHOUSE_SIZE = 'X-LARGE'
    AUTO_SUSPEND = 60;

-- Parallel loading with pattern matching
COPY INTO large_table
FROM @my_stage
PATTERN = '.*sales_2024.*\.csv\.gz'
FILE_FORMAT = optimized_csv
ON_ERROR = 'SKIP_FILE_5%'  -- Skip file if >5% errors
PARALLEL = 16;  -- Use 16 parallel threads

-- Monitor loading performance
SELECT 
    file_name,
    file_size,
    row_count,
    row_parsed,
    first_error_message,
    first_error_line_number,
    first_error_character_position
FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => 'LARGE_TABLE',
    START_TIME => DATEADD(HOUR, -2, CURRENT_TIMESTAMP())
));

-- Use multi-table insert for denormalization
INSERT ALL
    INTO fact_sales (order_id, customer_id, amount, order_date)
        VALUES (order_id, customer_id, amount, order_date)
    INTO customer_summary (customer_id, last_order_date, total_spent)
        VALUES (customer_id, order_date, amount)
SELECT order_id, customer_id, amount, order_date
FROM staging_orders;

-- Optimize clustering for query performance
ALTER TABLE large_table CLUSTER BY (date_column, category_column);

-- Monitor clustering effectiveness
SELECT SYSTEM$CLUSTERING_INFORMATION('large_table', '(date_column, category_column)');

-- Use transient tables for temporary data
CREATE TRANSIENT TABLE temp_processing AS
SELECT * FROM large_table WHERE processing_flag = 'PENDING';
```

### 15. How do you implement data governance and compliance in Snowflake?
**Answer:**
```sql
-- Data classification using tags
CREATE TAG pii_tag ALLOWED_VALUES 'sensitive', 'highly_sensitive', 'public';
CREATE TAG data_domain ALLOWED_VALUES 'finance', 'marketing', 'operations';

-- Apply tags to objects
ALTER TABLE customers SET TAG (pii_tag = 'sensitive', data_domain = 'marketing');
ALTER TABLE customers MODIFY COLUMN ssn SET TAG (pii_tag = 'highly_sensitive');

-- Create governance policies
CREATE MASKING POLICY ssn_mask AS (val STRING) RETURNS STRING ->
    CASE 
        WHEN CURRENT_ROLE() IN ('COMPLIANCE_OFFICER', 'DBA') THEN val
        WHEN CURRENT_ROLE() IN ('ANALYST') THEN 'XXX-XX-' || RIGHT(val, 4)
        ELSE 'XXX-XX-XXXX'
    END;

-- Apply masking policy
ALTER TABLE customers MODIFY COLUMN ssn SET MASKING POLICY ssn_mask;

-- Row access policy for regional data
CREATE ROW ACCESS POLICY regional_access AS (region STRING) RETURNS BOOLEAN ->
    CASE 
        WHEN CURRENT_ROLE() = 'GLOBAL_ADMIN' THEN TRUE
        WHEN CURRENT_ROLE() = 'US_ANALYST' AND region = 'US' THEN TRUE
        WHEN CURRENT_ROLE() = 'EU_ANALYST' AND region = 'EU' THEN TRUE
        ELSE FALSE
    END;

ALTER TABLE sales ADD ROW ACCESS POLICY regional_access ON (region);

-- Audit and monitoring
SELECT 
    user_name,
    role_name,
    query_text,
    start_time,
    end_time,
    warehouse_name,
    database_name,
    schema_name
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE start_time >= DATEADD(DAY, -1, CURRENT_TIMESTAMP())
  AND query_text ILIKE '%sensitive_table%'
ORDER BY start_time DESC;

-- Data lineage tracking
SELECT 
    query_id,
    query_text,
    objects_modified,
    objects_accessed
FROM SNOWFLAKE.ACCOUNT_USAGE.ACCESS_HISTORY
WHERE query_start_time >= DATEADD(DAY, -7, CURRENT_TIMESTAMP())
ORDER BY query_start_time DESC;

-- Create compliance report
CREATE VIEW compliance_report AS
SELECT 
    table_name,
    column_name,
    tag_name,
    tag_value,
    policy_name
FROM SNOWFLAKE.ACCOUNT_USAGE.TAG_REFERENCES tr
JOIN SNOWFLAKE.ACCOUNT_USAGE.POLICY_REFERENCES pr 
    ON tr.object_name = pr.ref_entity_name
WHERE tag_name IN ('pii_tag', 'data_domain');
```

### 16. How do you monitor and optimize costs in Snowflake?
**Answer:**
```sql
-- Monitor warehouse usage and costs
SELECT 
    warehouse_name,
    DATE(start_time) as usage_date,
    SUM(credits_used) as daily_credits,
    SUM(credits_used) * 2.5 as estimated_cost_usd  -- Assuming $2.5 per credit
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE start_time >= DATEADD(DAY, -30, CURRENT_TIMESTAMP())
GROUP BY warehouse_name, DATE(start_time)
ORDER BY daily_credits DESC;

-- Identify expensive queries
SELECT 
    query_id,
    user_name,
    warehouse_name,
    total_elapsed_time / 1000 as execution_seconds,
    credits_used_cloud_services,
    bytes_scanned,
    query_text
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE start_time >= DATEADD(DAY, -7, CURRENT_TIMESTAMP())
  AND total_elapsed_time > 60000  -- Queries longer than 1 minute
ORDER BY credits_used_cloud_services DESC
LIMIT 20;

-- Storage costs analysis
SELECT 
    table_name,
    active_bytes / (1024*1024*1024) as active_gb,
    time_travel_bytes / (1024*1024*1024) as time_travel_gb,
    failsafe_bytes / (1024*1024*1024) as failsafe_gb,
    (active_bytes + time_travel_bytes + failsafe_bytes) / (1024*1024*1024) as total_gb
FROM SNOWFLAKE.ACCOUNT_USAGE.TABLE_STORAGE_METRICS
WHERE deleted = FALSE
ORDER BY total_gb DESC
LIMIT 20;

-- Cost optimization strategies
-- 1. Right-size warehouses
ALTER WAREHOUSE analytics_wh SET 
    WAREHOUSE_SIZE = 'MEDIUM'  -- Downsize if underutilized
    AUTO_SUSPEND = 60;         -- Suspend after 1 minute

-- 2. Use resource monitors
CREATE RESOURCE MONITOR monthly_limit WITH 
    CREDIT_QUOTA = 1000
    FREQUENCY = MONTHLY
    START_TIMESTAMP = IMMEDIATELY
    TRIGGERS 
        ON 75 PERCENT DO NOTIFY
        ON 90 PERCENT DO SUSPEND
        ON 100 PERCENT DO SUSPEND_IMMEDIATE;

ALTER WAREHOUSE analytics_wh SET RESOURCE_MONITOR = monthly_limit;

-- 3. Optimize data retention
ALTER TABLE large_table SET DATA_RETENTION_TIME_IN_DAYS = 1;

-- 4. Use clustering efficiently
-- Only cluster tables > 1TB with predictable query patterns
SELECT 
    table_name,
    active_bytes / (1024*1024*1024*1024) as size_tb,
    clustering_key
FROM SNOWFLAKE.ACCOUNT_USAGE.TABLES
WHERE active_bytes > 1024*1024*1024*1024  -- > 1TB
  AND clustering_key IS NOT NULL;

-- 5. Monitor and optimize Snowpipe
SELECT 
    pipe_name,
    credits_used,
    bytes_inserted,
    files_inserted
FROM SNOWFLAKE.ACCOUNT_USAGE.PIPE_USAGE_HISTORY
WHERE start_time >= DATEADD(DAY, -7, CURRENT_TIMESTAMP())
ORDER BY credits_used DESC;

-- Cost allocation by department
SELECT 
    COALESCE(warehouse_name, 'Unknown') as warehouse,
    COALESCE(user_name, 'System') as user_name,
    DATE_TRUNC('MONTH', start_time) as month,
    SUM(credits_used) as total_credits,
    SUM(credits_used) * 2.5 as estimated_cost
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE start_time >= DATEADD(MONTH, -3, CURRENT_TIMESTAMP())
GROUP BY warehouse, user_name, month
ORDER BY total_credits DESC;
```

## Advanced Level Questions (17-20)

### 17. How do you implement a data lakehouse architecture with Snowflake?
**Answer:**
```sql
-- External stages for data lake integration
CREATE STAGE data_lake_stage
    URL = 's3://data-lake-bucket/'
    CREDENTIALS = (AWS_KEY_ID = 'xxx' AWS_SECRET_KEY = 'yyy')
    DIRECTORY = (ENABLE = TRUE AUTO_REFRESH = TRUE);

-- External tables for different data formats
CREATE EXTERNAL TABLE raw_events (
    event_id STRING AS (value:event_id::STRING),
    timestamp TIMESTAMP AS (value:timestamp::TIMESTAMP),
    user_id STRING AS (value:user_id::STRING),
    event_data VARIANT AS (value:event_data::VARIANT)
)
WITH LOCATION = @data_lake_stage/events/
FILE_FORMAT = (TYPE = 'JSON')
AUTO_REFRESH = TRUE;

-- Materialized views for performance
CREATE MATERIALIZED VIEW user_event_summary AS
SELECT 
    user_id,
    DATE(timestamp) as event_date,
    COUNT(*) as event_count,
    COUNT(DISTINCT event_data:event_type::STRING) as unique_event_types
FROM raw_events
GROUP BY user_id, DATE(timestamp);

-- Hybrid approach: External + Internal tables
CREATE TASK materialize_hot_data
    WAREHOUSE = 'ETL_WH'
    SCHEDULE = '60 MINUTE'
AS
    CREATE OR REPLACE TRANSIENT TABLE hot_events AS
    SELECT * FROM raw_events
    WHERE timestamp >= DATEADD(DAY, -7, CURRENT_TIMESTAMP());

-- Data lake to warehouse ETL
CREATE OR REPLACE PROCEDURE lakehouse_etl()
RETURNS STRING
LANGUAGE SQL
AS
$$
BEGIN
    -- Extract from data lake
    CREATE OR REPLACE TEMPORARY TABLE staging_data AS
    SELECT 
        event_id,
        timestamp,
        user_id,
        event_data:event_type::STRING as event_type,
        event_data:properties::VARIANT as properties
    FROM raw_events
    WHERE timestamp >= DATEADD(HOUR, -1, CURRENT_TIMESTAMP());
    
    -- Transform and load to warehouse
    MERGE INTO fact_events fe
    USING staging_data sd ON fe.event_id = sd.event_id
    WHEN NOT MATCHED THEN
        INSERT (event_id, timestamp, user_id, event_type, properties, created_at)
        VALUES (sd.event_id, sd.timestamp, sd.user_id, sd.event_type, sd.properties, CURRENT_TIMESTAMP());
    
    RETURN 'Lakehouse ETL completed successfully';
END;
$$;

-- Schema evolution handling
CREATE OR REPLACE PROCEDURE handle_schema_evolution()
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    new_columns ARRAY;
    col VARIANT;
BEGIN
    -- Detect new columns in external data
    SELECT ARRAY_AGG(DISTINCT key) INTO new_columns
    FROM raw_events,
    LATERAL FLATTEN(input => event_data)
    WHERE key NOT IN (
        SELECT column_name 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE table_name = 'FACT_EVENTS'
    );
    
    -- Add new columns dynamically
    FOR i IN 0 TO ARRAY_SIZE(new_columns) - 1 DO
        col := new_columns[i];
        EXECUTE IMMEDIATE 'ALTER TABLE fact_events ADD COLUMN ' || col::STRING || ' VARIANT';
    END FOR;
    
    RETURN 'Schema evolution completed';
END;
$$;
```

### 18. How do you implement real-time analytics with Snowflake?
**Answer:**
```sql
-- Snowpipe for real-time ingestion
CREATE PIPE real_time_events_pipe
    AUTO_INGEST = TRUE
    AWS_SNS_TOPIC = 'arn:aws:sns:us-east-1:123456789:snowpipe-topic'
AS
    COPY INTO raw_events
    FROM @event_stage
    FILE_FORMAT = (TYPE = 'JSON')
    MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

-- Streams for change tracking
CREATE STREAM events_stream ON TABLE raw_events;

-- Real-time aggregation task
CREATE TASK real_time_aggregation
    WAREHOUSE = 'STREAMING_WH'
    SCHEDULE = '1 MINUTE'
    WHEN SYSTEM$STREAM_HAS_DATA('events_stream')
AS
    MERGE INTO real_time_metrics rtm
    USING (
        SELECT 
            DATE_TRUNC('MINUTE', timestamp) as minute_window,
            event_type,
            COUNT(*) as event_count,
            COUNT(DISTINCT user_id) as unique_users
        FROM events_stream
        WHERE METADATA$ACTION = 'INSERT'
        GROUP BY DATE_TRUNC('MINUTE', timestamp), event_type
    ) es ON rtm.minute_window = es.minute_window AND rtm.event_type = es.event_type
    WHEN MATCHED THEN
        UPDATE SET 
            event_count = rtm.event_count + es.event_count,
            unique_users = rtm.unique_users + es.unique_users,
            updated_at = CURRENT_TIMESTAMP()
    WHEN NOT MATCHED THEN
        INSERT (minute_window, event_type, event_count, unique_users, created_at)
        VALUES (es.minute_window, es.event_type, es.event_count, es.unique_users, CURRENT_TIMESTAMP());

-- Real-time alerting
CREATE TASK anomaly_detection
    WAREHOUSE = 'STREAMING_WH'
    SCHEDULE = '5 MINUTE'
AS
    INSERT INTO alerts (alert_type, message, severity, created_at)
    SELECT 
        'HIGH_ERROR_RATE' as alert_type,
        'Error rate exceeded threshold: ' || error_rate || '%' as message,
        'HIGH' as severity,
        CURRENT_TIMESTAMP() as created_at
    FROM (
        SELECT 
            (SUM(CASE WHEN event_type = 'error' THEN event_count ELSE 0 END) * 100.0 / 
             SUM(event_count)) as error_rate
        FROM real_time_metrics
        WHERE minute_window >= DATEADD(MINUTE, -5, CURRENT_TIMESTAMP())
    )
    WHERE error_rate > 5.0;  -- Alert if error rate > 5%

-- Real-time dashboard views
CREATE VIEW real_time_dashboard AS
SELECT 
    minute_window,
    SUM(event_count) as total_events,
    SUM(unique_users) as total_users,
    SUM(CASE WHEN event_type = 'error' THEN event_count ELSE 0 END) as error_count,
    (SUM(CASE WHEN event_type = 'error' THEN event_count ELSE 0 END) * 100.0 / 
     SUM(event_count)) as error_rate
FROM real_time_metrics
WHERE minute_window >= DATEADD(HOUR, -1, CURRENT_TIMESTAMP())
GROUP BY minute_window
ORDER BY minute_window DESC;

-- Enable real-time processing
ALTER PIPE real_time_events_pipe REFRESH;
ALTER TASK real_time_aggregation RESUME;
ALTER TASK anomaly_detection RESUME;
```

### 19. How do you implement advanced data modeling patterns in Snowflake?
**Answer:**
```sql
-- Data Vault 2.0 implementation
-- Hubs (business keys)
CREATE TABLE hub_customer (
    customer_hk STRING PRIMARY KEY,  -- Hash key
    customer_bk STRING NOT NULL,     -- Business key
    load_date TIMESTAMP NOT NULL,
    record_source STRING NOT NULL
);

-- Satellites (descriptive data)
CREATE TABLE sat_customer_details (
    customer_hk STRING,
    load_date TIMESTAMP,
    load_end_date TIMESTAMP,
    hash_diff STRING,
    customer_name STRING,
    email STRING,
    phone STRING,
    address STRING,
    record_source STRING,
    PRIMARY KEY (customer_hk, load_date),
    FOREIGN KEY (customer_hk) REFERENCES hub_customer(customer_hk)
);

-- Links (relationships)
CREATE TABLE link_customer_order (
    customer_order_hk STRING PRIMARY KEY,
    customer_hk STRING NOT NULL,
    order_hk STRING NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source STRING NOT NULL,
    FOREIGN KEY (customer_hk) REFERENCES hub_customer(customer_hk)
);

-- Data Vault loading procedures
CREATE OR REPLACE PROCEDURE load_data_vault()
RETURNS STRING
LANGUAGE SQL
AS
$$
BEGIN
    -- Load Hubs
    INSERT INTO hub_customer (customer_hk, customer_bk, load_date, record_source)
    SELECT DISTINCT
        SHA2(UPPER(TRIM(customer_id))) as customer_hk,
        customer_id as customer_bk,
        CURRENT_TIMESTAMP() as load_date,
        'CRM_SYSTEM' as record_source
    FROM staging_customers s
    WHERE NOT EXISTS (
        SELECT 1 FROM hub_customer h 
        WHERE h.customer_hk = SHA2(UPPER(TRIM(s.customer_id)))
    );
    
    -- Load Satellites
    INSERT INTO sat_customer_details (
        customer_hk, load_date, hash_diff, customer_name, 
        email, phone, address, record_source
    )
    SELECT 
        SHA2(UPPER(TRIM(customer_id))) as customer_hk,
        CURRENT_TIMESTAMP() as load_date,
        SHA2(CONCAT(customer_name, email, phone, address)) as hash_diff,
        customer_name,
        email,
        phone,
        address,
        'CRM_SYSTEM' as record_source
    FROM staging_customers s
    WHERE NOT EXISTS (
        SELECT 1 FROM sat_customer_details sat
        WHERE sat.customer_hk = SHA2(UPPER(TRIM(s.customer_id)))
          AND sat.hash_diff = SHA2(CONCAT(s.customer_name, s.email, s.phone, s.address))
          AND sat.load_end_date IS NULL
    );
    
    -- Close previous satellite records
    UPDATE sat_customer_details 
    SET load_end_date = CURRENT_TIMESTAMP()
    WHERE load_end_date IS NULL
      AND customer_hk IN (
          SELECT DISTINCT SHA2(UPPER(TRIM(customer_id)))
          FROM staging_customers
      );
    
    RETURN 'Data Vault loading completed';
END;
$$;

-- Dimensional modeling with SCD Type 2
CREATE TABLE dim_customer (
    customer_sk NUMBER AUTOINCREMENT PRIMARY KEY,  -- Surrogate key
    customer_bk STRING NOT NULL,                   -- Business key
    customer_name STRING,
    email STRING,
    phone STRING,
    address STRING,
    effective_date DATE NOT NULL,
    expiry_date DATE,
    is_current BOOLEAN DEFAULT TRUE,
    version NUMBER DEFAULT 1
);

-- SCD Type 2 implementation
CREATE OR REPLACE PROCEDURE update_customer_dimension()
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    updated_count NUMBER := 0;
BEGIN
    -- Close current records that have changed
    UPDATE dim_customer dc
    SET 
        expiry_date = CURRENT_DATE - 1,
        is_current = FALSE
    FROM staging_customers sc
    WHERE dc.customer_bk = sc.customer_id
      AND dc.is_current = TRUE
      AND (dc.customer_name != sc.customer_name 
           OR dc.email != sc.email 
           OR dc.phone != sc.phone 
           OR dc.address != sc.address);
    
    -- Insert new versions
    INSERT INTO dim_customer (
        customer_bk, customer_name, email, phone, address,
        effective_date, expiry_date, is_current, version
    )
    SELECT 
        sc.customer_id,
        sc.customer_name,
        sc.email,
        sc.phone,
        sc.address,
        CURRENT_DATE,
        '9999-12-31',
        TRUE,
        COALESCE(MAX(dc.version), 0) + 1
    FROM staging_customers sc
    LEFT JOIN dim_customer dc ON sc.customer_id = dc.customer_bk
    WHERE NOT EXISTS (
        SELECT 1 FROM dim_customer dc2
        WHERE dc2.customer_bk = sc.customer_id
          AND dc2.is_current = TRUE
          AND dc2.customer_name = sc.customer_name
          AND dc2.email = sc.email
          AND dc2.phone = sc.phone
          AND dc2.address = sc.address
    )
    GROUP BY sc.customer_id, sc.customer_name, sc.email, sc.phone, sc.address;
    
    GET DIAGNOSTICS updated_count = ROW_COUNT;
    RETURN 'Updated ' || updated_count || ' customer dimension records';
END;
$$;

-- Bridge tables for many-to-many relationships
CREATE TABLE bridge_customer_product (
    customer_sk NUMBER,
    product_sk NUMBER,
    relationship_type STRING,
    effective_date DATE,
    expiry_date DATE,
    weight_factor DECIMAL(5,4) DEFAULT 1.0000,
    PRIMARY KEY (customer_sk, product_sk, effective_date)
);
```

### 20. How do you implement disaster recovery and high availability in Snowflake?
**Answer:**
```sql
-- Database replication for disaster recovery
-- Primary account setup
CREATE DATABASE production_db;
CREATE SCHEMA production_db.sales;

-- Enable replication
ALTER DATABASE production_db ENABLE REPLICATION TO ACCOUNTS ('backup-account');

-- Secondary account setup (in backup account)
CREATE DATABASE production_db_replica AS REPLICA OF primary-account.production_db;

-- Failover procedure
CREATE OR REPLACE PROCEDURE failover_to_replica()
RETURNS STRING
LANGUAGE SQL
AS
$$
BEGIN
    -- Promote replica to primary
    ALTER DATABASE production_db_replica PROMOTE;
    
    -- Update application connection strings
    -- (This would typically be done externally)
    
    RETURN 'Failover completed successfully';
END;
$$;

-- Backup and recovery strategies
-- 1. Time Travel for point-in-time recovery
CREATE OR REPLACE PROCEDURE restore_table_to_timestamp(
    table_name STRING,
    restore_timestamp TIMESTAMP
)
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    backup_table_name STRING;
BEGIN
    backup_table_name := table_name || '_backup_' || TO_VARCHAR(CURRENT_TIMESTAMP(), 'YYYYMMDDHH24MISS');
    
    -- Create backup of current table
    EXECUTE IMMEDIATE 'CREATE TABLE ' || backup_table_name || ' AS SELECT * FROM ' || table_name;
    
    -- Restore from Time Travel
    EXECUTE IMMEDIATE 'CREATE OR REPLACE TABLE ' || table_name || 
                     ' AS SELECT * FROM ' || table_name || 
                     ' AT (TIMESTAMP => ''' || restore_timestamp || ''')';
    
    RETURN 'Table ' || table_name || ' restored to ' || restore_timestamp || 
           '. Backup created as ' || backup_table_name;
END;
$$;

-- 2. Zero-copy cloning for backups
CREATE OR REPLACE PROCEDURE create_database_backup()
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    backup_name STRING;
BEGIN
    backup_name := 'production_db_backup_' || TO_VARCHAR(CURRENT_DATE(), 'YYYYMMDD');
    
    -- Create zero-copy clone
    EXECUTE IMMEDIATE 'CREATE DATABASE ' || backup_name || ' CLONE production_db';
    
    -- Set retention period for backup
    EXECUTE IMMEDIATE 'ALTER DATABASE ' || backup_name || ' SET DATA_RETENTION_TIME_IN_DAYS = 90';
    
    RETURN 'Database backup created: ' || backup_name;
END;
$$;

-- 3. Cross-region replication monitoring
CREATE VIEW replication_status AS
SELECT 
    database_name,
    replication_group,
    region,
    is_primary,
    replication_lag_seconds,
    last_refresh_time
FROM SNOWFLAKE.ACCOUNT_USAGE.REPLICATION_DATABASES
ORDER BY database_name, region;

-- 4. Automated backup scheduling
CREATE TASK daily_backup
    WAREHOUSE = 'BACKUP_WH'
    SCHEDULE = 'USING CRON 0 2 * * * UTC'  -- Daily at 2 AM UTC
AS
    CALL create_database_backup();

-- 5. Health monitoring and alerting
CREATE OR REPLACE PROCEDURE monitor_system_health()
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    failed_tasks NUMBER;
    replication_lag NUMBER;
    storage_usage_pct NUMBER;
BEGIN
    -- Check for failed tasks
    SELECT COUNT(*) INTO failed_tasks
    FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY())
    WHERE scheduled_time >= DATEADD(HOUR, -1, CURRENT_TIMESTAMP())
      AND state = 'FAILED';
    
    -- Check replication lag
    SELECT MAX(replication_lag_seconds) INTO replication_lag
    FROM SNOWFLAKE.ACCOUNT_USAGE.REPLICATION_DATABASES
    WHERE is_primary = FALSE;
    
    -- Check storage usage
    SELECT (SUM(active_bytes) / (1024*1024*1024*1024)) INTO storage_usage_pct
    FROM SNOWFLAKE.ACCOUNT_USAGE.STORAGE_USAGE;
    
    -- Generate alerts
    IF failed_tasks > 0 THEN
        INSERT INTO system_alerts (alert_type, message, severity, created_at)
        VALUES ('TASK_FAILURE', failed_tasks || ' tasks failed in the last hour', 'HIGH', CURRENT_TIMESTAMP());
    END IF;
    
    IF replication_lag > 300 THEN  -- 5 minutes
        INSERT INTO system_alerts (alert_type, message, severity, created_at)
        VALUES ('REPLICATION_LAG', 'Replication lag is ' || replication_lag || ' seconds', 'MEDIUM', CURRENT_TIMESTAMP());
    END IF;
    
    IF storage_usage_pct > 0.8 THEN  -- 80% of quota
        INSERT INTO system_alerts (alert_type, message, severity, created_at)
        VALUES ('STORAGE_USAGE', 'Storage usage is at ' || (storage_usage_pct * 100) || '%', 'MEDIUM', CURRENT_TIMESTAMP());
    END IF;
    
    RETURN 'Health monitoring completed';
END;
$$;

-- 6. Recovery testing procedure
CREATE OR REPLACE PROCEDURE test_disaster_recovery()
RETURNS STRING
LANGUAGE SQL
AS
$$
BEGIN
    -- Create test environment
    CREATE DATABASE dr_test_db CLONE production_db;
    
    -- Simulate disaster scenario
    DROP TABLE dr_test_db.sales.orders;
    
    -- Test recovery
    CREATE TABLE dr_test_db.sales.orders AS 
    SELECT * FROM production_db.sales.orders AT (OFFSET => -3600);  -- 1 hour ago
    
    -- Validate recovery
    IF (SELECT COUNT(*) FROM dr_test_db.sales.orders) > 0 THEN
        DROP DATABASE dr_test_db;
        RETURN 'Disaster recovery test PASSED';
    ELSE
        DROP DATABASE dr_test_db;
        RETURN 'Disaster recovery test FAILED';
    END IF;
END;
$$;

-- Enable monitoring tasks
ALTER TASK daily_backup RESUME;

-- Schedule health monitoring
CREATE TASK health_monitoring
    WAREHOUSE = 'MONITORING_WH'
    SCHEDULE = '15 MINUTE'
AS
    CALL monitor_system_health();

ALTER TASK health_monitoring RESUME;
```