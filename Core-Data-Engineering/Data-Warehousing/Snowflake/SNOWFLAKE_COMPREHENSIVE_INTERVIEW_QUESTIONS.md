# Snowflake Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-30)](#basic-level-questions-1-30)
2. [Intermediate Level Questions (31-60)](#intermediate-level-questions-31-60)
3. [Advanced Level Questions (61-90)](#advanced-level-questions-61-90)
4. [Architecture & Performance (91-120)](#architecture--performance-91-120)
5. [Streaming & Real-time Processing (121-150)](#streaming--real-time-processing-121-150)
6. [Production & Operations (151-180)](#production--operations-151-180)
7. [Scenario-Based Questions (181-200)](#scenario-based-questions-181-200)

---

## Basic Level Questions (1-30)

### 1. What is Snowflake and how does it differ from traditional data warehouses?

**Snowflake** is a cloud-native data warehouse with a unique multi-cluster, shared data architecture that separates compute and storage.

#### **Key Differences:**

| Aspect | Snowflake | Traditional DW |
|--------|-----------|----------------|
| **Architecture** | Multi-cluster, shared data | Shared-nothing MPP |
| **Scaling** | Independent compute/storage | Scale entire system |
| **Maintenance** | Zero maintenance | Manual tuning required |
| **Pricing** | Pay-per-use | Fixed licensing |
| **Deployment** | Cloud-native | On-premises/hybrid |

```sql
-- Snowflake's elastic scaling example
CREATE WAREHOUSE analytics_wh WITH
    WAREHOUSE_SIZE = 'LARGE'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 10
    SCALING_POLICY = 'STANDARD';

-- Monitor warehouse usage
SELECT 
    warehouse_name,
    credits_used,
    avg_running_time,
    avg_queued_load
FROM snowflake.account_usage.warehouse_metering_history
WHERE start_time >= DATEADD('day', -7, CURRENT_TIMESTAMP())
ORDER BY credits_used DESC;

-- Dynamic warehouse resizing
ALTER WAREHOUSE analytics_wh SET WAREHOUSE_SIZE = 'X-LARGE';
```

**Output:**
```
WAREHOUSE_NAME    CREDITS_USED    AVG_RUNNING_TIME    AVG_QUEUED_LOAD
ANALYTICS_WH      45.2           120.5               0.02
ETL_WH           23.8           89.3                0.15
```

### 2. Explain Snowflake's three-layer architecture in detail.

**Answer:** Snowflake's architecture separates storage, compute, and services into independent, scalable layers.

#### 🎯 **Architecture Components**

```sql
-- 1. STORAGE LAYER - Micro-partitions
CREATE TABLE sales_data (
    sale_id NUMBER AUTOINCREMENT,
    sale_date DATE,
    customer_id NUMBER,
    product_id NUMBER,
    amount DECIMAL(10,2),
    region VARCHAR(50)
);

-- Data is automatically partitioned into micro-partitions (50-500MB)
INSERT INTO sales_data (sale_date, customer_id, product_id, amount, region)
SELECT 
    DATEADD('day', UNIFORM(1, 365, RANDOM()), '2023-01-01'),
    UNIFORM(1, 10000, RANDOM()),
    UNIFORM(1, 1000, RANDOM()),
    UNIFORM(10, 1000, RANDOM()),
    CASE UNIFORM(1, 4, RANDOM())
        WHEN 1 THEN 'North'
        WHEN 2 THEN 'South'
        WHEN 3 THEN 'East'
        ELSE 'West'
    END
FROM TABLE(GENERATOR(ROWCOUNT => 100000));

-- 2. COMPUTE LAYER - Virtual Warehouses
CREATE WAREHOUSE etl_warehouse WITH 
    WAREHOUSE_SIZE = 'MEDIUM'
    AUTO_SUSPEND = 60;

CREATE WAREHOUSE analytics_warehouse WITH 
    WAREHOUSE_SIZE = 'LARGE'
    AUTO_SUSPEND = 300;

-- 3. SERVICES LAYER - Metadata and optimization
SHOW TABLES;
DESCRIBE TABLE sales_data;

-- Check micro-partition information
SELECT 
    table_name,
    row_count,
    bytes,
    micropartition_count,
    clustering_depth
FROM snowflake.account_usage.table_storage_metrics
WHERE table_name = 'SALES_DATA';
```

**Output:**
```
TABLE_NAME    ROW_COUNT    BYTES        MICROPARTITION_COUNT    CLUSTERING_DEPTH
SALES_DATA    100000       8456789      12                      2.3
```

### 3. What are virtual warehouses and how do they provide compute elasticity?

**Answer:** Virtual warehouses are compute clusters that can scale independently and automatically based on workload demands.

```sql
-- Create warehouse with multi-cluster auto-scaling
CREATE WAREHOUSE scalable_wh WITH
    WAREHOUSE_SIZE = 'MEDIUM'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 8
    SCALING_POLICY = 'STANDARD'
    COMMENT = 'Auto-scaling warehouse for variable workloads';

-- Monitor scaling behavior
SELECT 
    warehouse_name,
    cluster_number,
    start_time,
    end_time,
    credits_used,
    avg_running_time
FROM snowflake.account_usage.warehouse_load_history
WHERE warehouse_name = 'SCALABLE_WH'
  AND start_time >= DATEADD('hour', -24, CURRENT_TIMESTAMP())
ORDER BY start_time;

-- Resize warehouse for different workloads
-- Small for development
ALTER WAREHOUSE dev_wh SET WAREHOUSE_SIZE = 'X-SMALL';

-- Large for heavy analytics
ALTER WAREHOUSE analytics_wh SET WAREHOUSE_SIZE = 'X-LARGE';

-- Check current warehouse configuration
SHOW WAREHOUSES LIKE 'SCALABLE_WH';

-- Suspend/resume warehouses manually
ALTER WAREHOUSE scalable_wh SUSPEND;
ALTER WAREHOUSE scalable_wh RESUME;
```

**Output:**
```
WAREHOUSE_NAME    CLUSTER_NUMBER    CREDITS_USED    AVG_RUNNING_TIME
SCALABLE_WH      1                 2.5             45.2
SCALABLE_WH      2                 1.8             38.7
SCALABLE_WH      3                 0.9             22.1
```

### 4. How do you load data into Snowflake using different methods?

**Answer:** Snowflake provides multiple data loading methods optimized for different use cases and data volumes.

```sql
-- 1. COPY Command for Batch Loading
CREATE FILE FORMAT csv_format
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    NULL_IF = ('NULL', 'null', '')
    EMPTY_FIELD_AS_NULL = TRUE
    COMPRESSION = 'AUTO';

CREATE STAGE s3_stage
    URL = 's3://my-data-bucket/sales/'
    CREDENTIALS = (
        AWS_KEY_ID = 'AKIAIOSFODNN7EXAMPLE'
        AWS_SECRET_KEY = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
    )
    FILE_FORMAT = csv_format;

-- Load data with error handling
COPY INTO sales_data
FROM @s3_stage/sales_2024.csv
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE'
PURGE = TRUE
RETURN_FAILED_ONLY = TRUE;

-- 2. Snowpipe for Continuous Loading
CREATE PIPE sales_pipe
    AUTO_INGEST = TRUE
    AWS_SNS_TOPIC = 'arn:aws:sns:us-east-1:123456789012:snowpipe-topic'
AS
    COPY INTO sales_data
    FROM @s3_stage/
    FILE_FORMAT = csv_format
    ON_ERROR = 'CONTINUE';

-- Check pipe status and history
SELECT SYSTEM$PIPE_STATUS('sales_pipe');

SELECT 
    pipe_name,
    file_name,
    status,
    rows_inserted,
    errors_seen,
    last_received_time
FROM TABLE(INFORMATION_SCHEMA.PIPE_USAGE_HISTORY(
    DATE_RANGE_START => DATEADD('day', -1, CURRENT_TIMESTAMP()),
    PIPE_NAME => 'SALES_PIPE'
));

-- 3. Bulk Loading with PUT command (SnowSQL)
-- PUT file://local_file.csv @my_stage AUTO_COMPRESS=TRUE;

-- 4. INSERT statements for small datasets
INSERT INTO sales_data (sale_date, customer_id, amount, region)
VALUES 
    ('2024-01-15', 1001, 1500.00, 'North'),
    ('2024-01-15', 1002, 2300.50, 'South'),
    ('2024-01-15', 1003, 890.25, 'East');

-- Monitor loading performance
SELECT 
    table_name,
    file_name,
    status,
    rows_loaded,
    rows_parsed,
    execution_time,
    first_error_message
FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => 'SALES_DATA',
    START_TIME => DATEADD('hour', -1, CURRENT_TIMESTAMP())
));
```

**Output:**
```
PIPE_NAME     FILE_NAME        STATUS      ROWS_INSERTED    ERRORS_SEEN
SALES_PIPE    sales_001.csv    LOADED      15000           0
SALES_PIPE    sales_002.csv    LOADED      12500           3
SALES_PIPE    sales_003.csv    PARTIALLY   8900            15
```

### 5. What are micro-partitions and how do they optimize query performance?

**Answer:** Micro-partitions are immutable, compressed data files (50-500MB) that enable efficient query pruning and parallel processing.

```sql
-- Micro-partitions are created automatically
CREATE TABLE transaction_data (
    transaction_id NUMBER,
    transaction_date DATE,
    customer_id NUMBER,
    amount DECIMAL(12,2),
    product_category VARCHAR(50),
    store_location VARCHAR(100)
);

-- Insert sample data to create micro-partitions
INSERT INTO transaction_data
SELECT 
    ROW_NUMBER() OVER (ORDER BY RANDOM()),
    DATEADD('day', UNIFORM(-365, 0, RANDOM()), CURRENT_DATE()),
    UNIFORM(1, 50000, RANDOM()),
    UNIFORM(10, 5000, RANDOM()) / 100.0,
    ARRAY_CONSTRUCT('Electronics', 'Clothing', 'Food', 'Books', 'Sports')[UNIFORM(1, 5, RANDOM())],
    ARRAY_CONSTRUCT('New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix')[UNIFORM(1, 5, RANDOM())]
FROM TABLE(GENERATOR(ROWCOUNT => 1000000));

-- Check micro-partition statistics
SELECT 
    table_name,
    row_count,
    bytes,
    micropartition_count,
    average_overlaps
FROM snowflake.account_usage.table_storage_metrics
WHERE table_name = 'TRANSACTION_DATA';

-- Query with partition pruning
SELECT 
    product_category,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount
FROM transaction_data
WHERE transaction_date >= '2024-01-01'
  AND store_location = 'New York'
GROUP BY product_category;

-- Check query profile for partition pruning
SELECT 
    query_id,
    query_text,
    partitions_scanned,
    partitions_total,
    bytes_scanned
FROM snowflake.account_usage.query_history
WHERE query_text LIKE '%transaction_data%'
  AND start_time >= DATEADD('hour', -1, CURRENT_TIMESTAMP())
ORDER BY start_time DESC
LIMIT 1;

-- Clustering improves micro-partition effectiveness
ALTER TABLE transaction_data CLUSTER BY (transaction_date, store_location);

-- Check clustering effectiveness
SELECT SYSTEM$CLUSTERING_DEPTH('transaction_data', '(transaction_date, store_location)');
```

**Output:**
```
TABLE_NAME          ROW_COUNT    BYTES      MICROPARTITION_COUNT    AVERAGE_OVERLAPS
TRANSACTION_DATA    1000000      45678912   89                      1.2

QUERY_ID                              PARTITIONS_SCANNED    PARTITIONS_TOTAL    BYTES_SCANNED
01a2b3c4-5678-90de-f123-456789abcdef  12                   89                  6789123
```

### 6. How does Snowflake handle concurrency and multi-user access?

**Answer:** Snowflake uses multi-cluster warehouses and automatic scaling to handle concurrent workloads without performance degradation.

```sql
-- Create multi-cluster warehouse for concurrency
CREATE WAREHOUSE concurrent_wh WITH
    WAREHOUSE_SIZE = 'LARGE'
    MIN_CLUSTER_COUNT = 2
    MAX_CLUSTER_COUNT = 10
    SCALING_POLICY = 'STANDARD'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE
    COMMENT = 'Multi-cluster warehouse for concurrent users';

-- Monitor concurrency and queuing
SELECT 
    warehouse_name,
    avg_running,
    avg_queued_load,
    avg_queued_provisioning,
    avg_blocked
FROM snowflake.account_usage.warehouse_load_history
WHERE warehouse_name = 'CONCURRENT_WH'
  AND start_time >= DATEADD('hour', -24, CURRENT_TIMESTAMP());

-- Check active queries and sessions
SELECT 
    session_id,
    user_name,
    role_name,
    warehouse_name,
    query_text,
    start_time,
    execution_status
FROM snowflake.account_usage.query_history
WHERE warehouse_name = 'CONCURRENT_WH'
  AND execution_status = 'RUNNING'
ORDER BY start_time;

-- Resource monitor for cost control
CREATE RESOURCE MONITOR concurrent_monitor WITH
    CREDIT_QUOTA = 500
    FREQUENCY = MONTHLY
    START_TIMESTAMP = IMMEDIATELY
    TRIGGERS 
        ON 75 PERCENT DO NOTIFY
        ON 90 PERCENT DO SUSPEND_IMMEDIATE
        ON 100 PERCENT DO SUSPEND_IMMEDIATE;

ALTER WAREHOUSE concurrent_wh SET RESOURCE_MONITOR = concurrent_monitor;

-- Check cluster scaling history
SELECT 
    warehouse_name,
    cluster_number,
    start_time,
    end_time,
    credits_used
FROM snowflake.account_usage.warehouse_load_history
WHERE warehouse_name = 'CONCURRENT_WH'
  AND start_time >= DATEADD('day', -1, CURRENT_TIMESTAMP())
ORDER BY start_time;
```

**Output:**
```
WAREHOUSE_NAME    AVG_RUNNING    AVG_QUEUED_LOAD    AVG_QUEUED_PROVISIONING    AVG_BLOCKED
CONCURRENT_WH     8.5           0.2                0.1                        0.0

SESSION_ID    USER_NAME    ROLE_NAME    WAREHOUSE_NAME    EXECUTION_STATUS
12345        ANALYST1     DATA_ANALYST  CONCURRENT_WH     RUNNING
12346        ANALYST2     DATA_ANALYST  CONCURRENT_WH     RUNNING
```

### 7. What is Time Travel in Snowflake and how do you use it effectively?

**Answer:** Time Travel allows querying historical data and recovering from accidental changes using automatic data versioning.

```sql
-- Set retention period for Time Travel
ALTER TABLE customer_data SET DATA_RETENTION_TIME_IN_DAYS = 7;

-- Query data at specific timestamp
SELECT * FROM customer_data 
AT (TIMESTAMP => '2024-01-15 10:30:00'::TIMESTAMP);

-- Query data before specific statement
SELECT * FROM customer_data 
BEFORE (STATEMENT => '01a2b3c4-5678-90de-f123-456789abcdef');

-- Query data at offset (1 hour ago)
SELECT * FROM customer_data 
AT (OFFSET => -3600);

-- Compare current vs historical data
WITH current_data AS (
    SELECT customer_id, email, status FROM customer_data
),
historical_data AS (
    SELECT customer_id, email, status 
    FROM customer_data AT (TIMESTAMP => '2024-01-14 00:00:00')
)
SELECT 
    c.customer_id,
    c.email as current_email,
    h.email as previous_email,
    c.status as current_status,
    h.status as previous_status
FROM current_data c
JOIN historical_data h ON c.customer_id = h.customer_id
WHERE c.email != h.email OR c.status != h.status;

-- Restore table to previous state
CREATE OR REPLACE TABLE customer_data AS
SELECT * FROM customer_data AT (TIMESTAMP => '2024-01-14 23:59:59');

-- Undrop accidentally dropped objects
DROP TABLE test_table;
UNDROP TABLE test_table;

-- Check Time Travel storage costs
SELECT 
    table_name,
    active_bytes,
    time_travel_bytes,
    failsafe_bytes,
    retained_for_clone_bytes
FROM snowflake.account_usage.table_storage_metrics
WHERE table_name = 'CUSTOMER_DATA';

-- Clone table from specific point in time
CREATE TABLE customer_backup CLONE customer_data 
AT (TIMESTAMP => '2024-01-14 12:00:00');
```

**Output:**
```
CUSTOMER_ID    CURRENT_EMAIL         PREVIOUS_EMAIL        CURRENT_STATUS    PREVIOUS_STATUS
1001          john.new@email.com    john@email.com        ACTIVE           INACTIVE
1002          jane@company.org      jane@company.com      ACTIVE           ACTIVE

TABLE_NAME      ACTIVE_BYTES    TIME_TRAVEL_BYTES    FAILSAFE_BYTES    RETAINED_FOR_CLONE_BYTES
CUSTOMER_DATA   15678234       3456789              7890123           0
```

### 8. How do you optimize query performance in Snowflake?

**Answer:** Use clustering keys, result caching, proper warehouse sizing, and query optimization techniques.

```sql
-- 1. Clustering Keys for large tables
ALTER TABLE large_sales_table CLUSTER BY (sale_date, region);

-- Check clustering effectiveness
SELECT SYSTEM$CLUSTERING_DEPTH('large_sales_table', '(sale_date, region)');

-- Monitor clustering information
SELECT SYSTEM$CLUSTERING_INFORMATION('large_sales_table', '(sale_date, region)');

-- 2. Result Caching (automatic for 24 hours)
-- First execution - no cache
SELECT 
    region,
    product_category,
    SUM(amount) as total_sales,
    COUNT(*) as transaction_count
FROM large_sales_table
WHERE sale_date >= '2024-01-01'
GROUP BY region, product_category;

-- Second execution - uses result cache
SELECT 
    region,
    product_category,
    SUM(amount) as total_sales,
    COUNT(*) as transaction_count
FROM large_sales_table
WHERE sale_date >= '2024-01-01'
GROUP BY region, product_category;

-- 3. Warehouse sizing optimization
-- Start with smaller warehouse
USE WAREHOUSE small_wh;
SELECT COUNT(*) FROM large_sales_table; -- Baseline performance

-- Scale up for complex queries
USE WAREHOUSE large_wh;
SELECT 
    customer_id,
    SUM(amount) as total_spent,
    COUNT(DISTINCT product_id) as unique_products,
    AVG(amount) as avg_transaction
FROM large_sales_table
WHERE sale_date >= '2023-01-01'
GROUP BY customer_id
HAVING total_spent > 10000
ORDER BY total_spent DESC;

-- 4. Query optimization techniques
-- Use LIMIT for exploratory queries
SELECT * FROM large_sales_table LIMIT 1000;

-- Avoid SELECT * in production
SELECT sale_id, customer_id, amount, sale_date 
FROM large_sales_table
WHERE region = 'North America';

-- Use appropriate WHERE clauses for partition pruning
SELECT customer_id, SUM(amount)
FROM large_sales_table
WHERE sale_date BETWEEN '2024-01-01' AND '2024-01-31'
  AND region IN ('North', 'South')
GROUP BY customer_id;

-- 5. Monitor query performance
SELECT 
    query_id,
    query_text,
    warehouse_name,
    warehouse_size,
    execution_time,
    compilation_time,
    bytes_scanned,
    partitions_scanned,
    partitions_total
FROM snowflake.account_usage.query_history
WHERE user_name = CURRENT_USER()
  AND start_time >= DATEADD('hour', -1, CURRENT_TIMESTAMP())
ORDER BY execution_time DESC;
```

**Output:**
```
CLUSTERING_DEPTH: 1.8 (Good clustering - closer to 1 is better)

QUERY_ID                              EXECUTION_TIME    BYTES_SCANNED    PARTITIONS_SCANNED
01a2b3c4-5678-90de-f123-456789abcdef  2.5s             45MB             12/89
01b3c4d5-6789-01ef-g234-567890bcdefg  0.1s             0MB              0/89 (cached)
```

### 9. What are the different Snowflake editions and their capabilities?

**Answer:** Snowflake offers four editions with increasing features and security capabilities.

#### 🎯 **Edition Comparison**

| Feature | Standard | Enterprise | Business Critical | VPS |
|---------|----------|------------|-------------------|-----|
| **Time Travel** | 1 day | 90 days | 90 days | 90 days |
| **Multi-Cluster** | No | Yes | Yes | Yes |
| **Column-Level Security** | No | Yes | Yes | Yes |
| **Row-Level Security** | No | Yes | Yes | Yes |
| **HIPAA/PCI Compliance** | No | No | Yes | Yes |
| **Customer-Managed Keys** | No | No | Yes | Yes |
| **Dedicated Infrastructure** | No | No | No | Yes |

```sql
-- Check current account edition
SELECT CURRENT_ACCOUNT(), CURRENT_REGION();

-- Features available in Enterprise+
-- Multi-cluster warehouses
CREATE WAREHOUSE enterprise_wh WITH
    WAREHOUSE_SIZE = 'LARGE'
    MIN_CLUSTER_COUNT = 2
    MAX_CLUSTER_COUNT = 10;

-- Materialized views (Enterprise+)
CREATE MATERIALIZED VIEW sales_summary AS
SELECT 
    DATE_TRUNC('month', sale_date) as month,
    region,
    SUM(amount) as total_sales,
    COUNT(*) as transaction_count
FROM sales_data
GROUP BY 1, 2;

-- Search optimization (Enterprise+)
ALTER TABLE large_table ADD SEARCH OPTIMIZATION;

-- Features available in Business Critical+
-- Column-level security with masking policies
CREATE MASKING POLICY ssn_mask AS (val STRING) RETURNS STRING ->
    CASE 
        WHEN CURRENT_ROLE() IN ('ADMIN', 'HR') THEN val
        ELSE '***-**-' || RIGHT(val, 4)
    END;

-- Row-level security
CREATE ROW ACCESS POLICY region_policy AS (region STRING) RETURNS BOOLEAN ->
    CASE 
        WHEN CURRENT_ROLE() = 'ADMIN' THEN TRUE
        WHEN CURRENT_ROLE() = 'REGIONAL_MANAGER' AND region = 'North' THEN TRUE
        ELSE FALSE
    END;

-- Check account usage and billing
SELECT 
    service_type,
    usage_date,
    credits_used,
    credits_billed
FROM snowflake.account_usage.metering_daily_history
WHERE usage_date >= DATEADD('month', -1, CURRENT_DATE())
ORDER BY usage_date DESC;
```

### 10. How do you monitor Snowflake usage, performance, and costs?

**Answer:** Use account usage views, resource monitors, and performance monitoring tools.

```sql
-- 1. Credit Usage Monitoring
SELECT 
    warehouse_name,
    DATE_TRUNC('day', start_time) as usage_date,
    SUM(credits_used) as daily_credits,
    SUM(credits_used_compute) as compute_credits,
    SUM(credits_used_cloud_services) as cloud_service_credits
FROM snowflake.account_usage.warehouse_metering_history
WHERE start_time >= DATEADD('month', -1, CURRENT_TIMESTAMP())
GROUP BY warehouse_name, usage_date
ORDER BY usage_date DESC, daily_credits DESC;

-- 2. Storage Usage and Costs
SELECT 
    usage_date,
    storage_bytes / (1024*1024*1024) as storage_gb,
    stage_bytes / (1024*1024*1024) as stage_gb,
    failsafe_bytes / (1024*1024*1024) as failsafe_gb
FROM snowflake.account_usage.storage_usage
WHERE usage_date >= DATEADD('month', -1, CURRENT_DATE())
ORDER BY usage_date DESC;

-- 3. Query Performance Monitoring
SELECT 
    query_id,
    user_name,
    warehouse_name,
    query_type,
    execution_time / 1000 as execution_seconds,
    queued_provisioning_time / 1000 as queue_seconds,
    bytes_scanned / (1024*1024) as mb_scanned,
    rows_produced
FROM snowflake.account_usage.query_history
WHERE start_time >= DATEADD('day', -1, CURRENT_TIMESTAMP())
  AND execution_time > 30000  -- Queries > 30 seconds
ORDER BY execution_time DESC
LIMIT 20;

-- 4. Resource Monitor Setup
CREATE RESOURCE MONITOR monthly_budget WITH
    CREDIT_QUOTA = 1000
    FREQUENCY = MONTHLY
    START_TIMESTAMP = IMMEDIATELY
    TRIGGERS 
        ON 50 PERCENT DO NOTIFY
        ON 75 PERCENT DO NOTIFY
        ON 90 PERCENT DO SUSPEND
        ON 100 PERCENT DO SUSPEND_IMMEDIATE;

-- Apply to warehouses
ALTER WAREHOUSE analytics_wh SET RESOURCE_MONITOR = monthly_budget;
ALTER WAREHOUSE etl_wh SET RESOURCE_MONITOR = monthly_budget;

-- 5. User Activity Monitoring
SELECT 
    user_name,
    client_ip,
    reported_client_type,
    first_authentication_factor,
    second_authentication_factor,
    is_success,
    error_code,
    error_message
FROM snowflake.account_usage.login_history
WHERE event_timestamp >= DATEADD('day', -7, CURRENT_TIMESTAMP())
  AND is_success = 'NO'
ORDER BY event_timestamp DESC;

-- 6. Data Transfer Monitoring
SELECT 
    source_cloud,
    source_region,
    target_cloud,
    target_region,
    bytes_transferred / (1024*1024*1024) as gb_transferred,
    transfer_type
FROM snowflake.account_usage.data_transfer_history
WHERE start_time >= DATEADD('month', -1, CURRENT_TIMESTAMP())
ORDER BY bytes_transferred DESC;

-- 7. Automatic Clustering Costs
SELECT 
    table_name,
    schema_name,
    database_name,
    credits_used,
    num_bytes_reclustered / (1024*1024*1024) as gb_reclustered,
    num_rows_reclustered
FROM snowflake.account_usage.automatic_clustering_history
WHERE start_time >= DATEADD('day', -7, CURRENT_TIMESTAMP())
ORDER BY credits_used DESC;
```

**Output:**
```
WAREHOUSE_NAME    USAGE_DATE    DAILY_CREDITS    COMPUTE_CREDITS    CLOUD_SERVICE_CREDITS
ANALYTICS_WH      2024-01-15    45.2            42.8               2.4
ETL_WH           2024-01-15    23.7            22.1               1.6

QUERY_ID                              EXECUTION_SECONDS    MB_SCANNED    ROWS_PRODUCED
01a2b3c4-5678-90de-f123-456789abcdef  125.4               1250.8        2500000
01b3c4d5-6789-01ef-g234-567890bcdefg  89.2                890.5         1800000
```
### 11. What is zero-copy cloning and how does it work in Snowflake?

**Answer:** Zero-copy cloning creates instant copies of databases, schemas, or tables without duplicating underlying data, using metadata pointers.

```sql
-- Database cloning
CREATE DATABASE dev_environment CLONE production_db;

-- Schema cloning
CREATE SCHEMA analytics_dev CLONE analytics_prod;

-- Table cloning
CREATE TABLE customer_backup CLONE customer_data;

-- Clone with Time Travel
CREATE TABLE sales_yesterday CLONE sales_data 
AT (TIMESTAMP => '2024-01-14 23:59:59');

-- Clone from specific statement
CREATE TABLE sales_before_update CLONE sales_data 
BEFORE (STATEMENT => '01a2b3c4-5678-90de-f123-456789abcdef');

-- Monitor clone storage usage
SELECT 
    table_name,
    clone_group_id,
    active_bytes / (1024*1024*1024) as active_gb,
    time_travel_bytes / (1024*1024*1024) as time_travel_gb,
    retained_for_clone_bytes / (1024*1024*1024) as clone_gb
FROM snowflake.account_usage.table_storage_metrics
WHERE clone_group_id IS NOT NULL
ORDER BY retained_for_clone_bytes DESC;

-- Clone entire account (Enterprise+)
-- CREATE ACCOUNT dev_account CLONE production_account;
```

**Output:**
```
TABLE_NAME        CLONE_GROUP_ID    ACTIVE_GB    TIME_TRAVEL_GB    CLONE_GB
CUSTOMER_BACKUP   12345            5.2          1.8               0.0
SALES_YESTERDAY   12346            15.7         3.2               2.1
```

### 12. How do you handle semi-structured data (JSON, XML, Avro) in Snowflake?

**Answer:** Use VARIANT data type with built-in functions for parsing and querying semi-structured data.

```sql
-- Create table with VARIANT column
CREATE TABLE user_events (
    event_id NUMBER AUTOINCREMENT,
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    user_id NUMBER,
    event_data VARIANT
);

-- Insert JSON data
INSERT INTO user_events (user_id, event_data) VALUES
    (1001, PARSE_JSON('{"action": "login", "device": "mobile", "location": {"city": "New York", "country": "US"}}')),
    (1002, PARSE_JSON('{"action": "purchase", "items": [{"id": 123, "name": "laptop", "price": 999.99}, {"id": 456, "name": "mouse", "price": 29.99}]}')),
    (1003, PARSE_JSON('{"action": "view", "page": "product", "product_id": 789, "duration": 45}'));

-- Query semi-structured data
SELECT 
    event_id,
    user_id,
    event_data:action::STRING as action,
    event_data:device::STRING as device,
    event_data:location.city::STRING as city,
    event_data:location.country::STRING as country
FROM user_events
WHERE event_data:action::STRING = 'login';

-- Flatten nested arrays
SELECT 
    event_id,
    user_id,
    f.value:id::NUMBER as item_id,
    f.value:name::STRING as item_name,
    f.value:price::NUMBER as item_price
FROM user_events,
LATERAL FLATTEN(input => event_data:items) f
WHERE event_data:action::STRING = 'purchase';

-- Create view for easier querying
CREATE VIEW user_purchases AS
SELECT 
    event_id,
    user_id,
    event_timestamp,
    f.value:id::NUMBER as product_id,
    f.value:name::STRING as product_name,
    f.value:price::NUMBER as price
FROM user_events,
LATERAL FLATTEN(input => event_data:items) f
WHERE event_data:action::STRING = 'purchase';

-- Advanced JSON functions
SELECT 
    event_id,
    ARRAY_SIZE(event_data:items) as item_count,
    OBJECT_KEYS(event_data) as available_keys,
    TYPEOF(event_data:duration) as duration_type
FROM user_events;

-- Load semi-structured data from files
CREATE FILE FORMAT json_format TYPE = 'JSON';

COPY INTO user_events (user_id, event_data)
FROM (
    SELECT 
        $1:user_id::NUMBER,
        $1
    FROM @json_stage/events.json
)
FILE_FORMAT = json_format;
```

**Output:**
```
EVENT_ID    USER_ID    ACTION    DEVICE    CITY        COUNTRY
1          1001       login     mobile    New York    US

EVENT_ID    USER_ID    ITEM_ID    ITEM_NAME    ITEM_PRICE
2          1002       123        laptop       999.99
2          1002       456        mouse        29.99
```

### 13. What are Snowflake stages and how do you use them for data loading?

**Answer:** Stages are named locations for storing data files, supporting both internal (Snowflake-managed) and external (cloud storage) options.

```sql
-- 1. Internal Named Stage
CREATE STAGE internal_stage
    FILE_FORMAT = (TYPE = 'CSV' FIELD_DELIMITER = ',' SKIP_HEADER = 1);

-- 2. External Stage - AWS S3
CREATE STAGE s3_stage
    URL = 's3://my-data-bucket/sales-data/'
    CREDENTIALS = (
        AWS_KEY_ID = 'AKIAIOSFODNN7EXAMPLE'
        AWS_SECRET_KEY = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
    )
    FILE_FORMAT = (
        TYPE = 'CSV'
        FIELD_DELIMITER = ','
        SKIP_HEADER = 1
        NULL_IF = ('NULL', 'null', '')
        COMPRESSION = 'GZIP'
    );

-- 3. External Stage - Azure Blob Storage
CREATE STAGE azure_stage
    URL = 'azure://myaccount.blob.core.windows.net/mycontainer/path/'
    CREDENTIALS = (
        AZURE_SAS_TOKEN = 'sv=2018-03-28&ss=bfqt&srt=sco&sp=rwdlacup&se=2019-04-05T22:15:49Z&st=2019-04-05T14:15:49Z&spr=https&sig=example'
    )
    FILE_FORMAT = (TYPE = 'PARQUET');

-- 4. External Stage - Google Cloud Storage
CREATE STAGE gcs_stage
    URL = 'gcs://my-gcs-bucket/data/'
    STORAGE_INTEGRATION = gcs_integration
    FILE_FORMAT = (TYPE = 'JSON');

-- List files in stage
LIST @s3_stage;
LIST @s3_stage/2024/01/;

-- Load data from stage
COPY INTO sales_data
FROM @s3_stage/sales_2024_01.csv.gz
FILE_FORMAT = (TYPE = 'CSV' COMPRESSION = 'GZIP')
ON_ERROR = 'CONTINUE'
PURGE = TRUE;

-- Load with pattern matching
COPY INTO sales_data
FROM @s3_stage/
PATTERN = '.*sales_2024.*\.csv\.gz'
FILE_FORMAT = (TYPE = 'CSV' COMPRESSION = 'GZIP');

-- Load with file transformation
COPY INTO sales_data (sale_id, customer_id, amount, sale_date)
FROM (
    SELECT 
        $1::NUMBER,
        $2::NUMBER,
        $3::DECIMAL(10,2),
        TO_DATE($4, 'YYYY-MM-DD')
    FROM @s3_stage/sales.csv
)
FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1);

-- Monitor stage usage
SELECT 
    stage_name,
    stage_schema,
    stage_type,
    stage_region,
    created
FROM snowflake.account_usage.stages
WHERE stage_name LIKE '%STAGE%';

-- Remove files from stage
REMOVE @s3_stage/processed/sales_2024_01.csv.gz;
REMOVE @s3_stage PATTERN = '.*processed.*';

-- Stage with directory table
SELECT 
    relative_path,
    size,
    last_modified,
    etag
FROM DIRECTORY(@s3_stage)
WHERE relative_path LIKE '%.csv%';
```

**Output:**
```
name                           size      last_modified              etag
sales_2024_01_01.csv.gz       1048576   Mon, 15 Jan 2024 10:30:00  "abc123def456"
sales_2024_01_02.csv.gz       987654    Tue, 16 Jan 2024 10:30:00  "def456ghi789"
```

### 14. How do you implement role-based access control (RBAC) in Snowflake?

**Answer:** Create hierarchical roles, grant appropriate privileges, and assign roles to users for secure data access.

```sql
-- 1. Create Role Hierarchy
CREATE ROLE data_analyst;
CREATE ROLE data_engineer;
CREATE ROLE data_scientist;
CREATE ROLE team_lead;
CREATE ROLE data_admin;

-- Create role hierarchy (inheritance)
GRANT ROLE data_analyst TO ROLE team_lead;
GRANT ROLE data_engineer TO ROLE team_lead;
GRANT ROLE data_scientist TO ROLE team_lead;
GRANT ROLE team_lead TO ROLE data_admin;

-- 2. Grant Warehouse Privileges
GRANT USAGE ON WAREHOUSE small_wh TO ROLE data_analyst;
GRANT USAGE ON WAREHOUSE medium_wh TO ROLE data_engineer;
GRANT USAGE ON WAREHOUSE large_wh TO ROLE data_scientist;
GRANT ALL PRIVILEGES ON WAREHOUSE large_wh TO ROLE data_admin;

-- 3. Grant Database and Schema Privileges
GRANT USAGE ON DATABASE analytics_db TO ROLE data_analyst;
GRANT USAGE ON SCHEMA analytics_db.public TO ROLE data_analyst;
GRANT SELECT ON ALL TABLES IN SCHEMA analytics_db.public TO ROLE data_analyst;

-- Grant more privileges to engineers
GRANT CREATE TABLE ON SCHEMA analytics_db.staging TO ROLE data_engineer;
GRANT CREATE VIEW ON SCHEMA analytics_db.public TO ROLE data_engineer;
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA analytics_db.staging TO ROLE data_engineer;

-- 4. Future Grants (automatic privileges on new objects)
GRANT SELECT ON FUTURE TABLES IN SCHEMA analytics_db.public TO ROLE data_analyst;
GRANT ALL PRIVILEGES ON FUTURE TABLES IN SCHEMA analytics_db.staging TO ROLE data_engineer;

-- 5. Create and Assign Users
CREATE USER john_analyst 
    PASSWORD = 'SecurePassword123!'
    DEFAULT_ROLE = data_analyst
    DEFAULT_WAREHOUSE = small_wh
    MUST_CHANGE_PASSWORD = TRUE;

CREATE USER jane_engineer
    PASSWORD = 'SecurePassword456!'
    DEFAULT_ROLE = data_engineer
    DEFAULT_WAREHOUSE = medium_wh;

-- Assign roles to users
GRANT ROLE data_analyst TO USER john_analyst;
GRANT ROLE data_engineer TO USER jane_engineer;
GRANT ROLE data_scientist TO USER jane_engineer; -- Multiple roles

-- 6. Custom Roles for Specific Access Patterns
CREATE ROLE finance_analyst;
GRANT USAGE ON DATABASE finance_db TO ROLE finance_analyst;
GRANT SELECT ON ALL TABLES IN SCHEMA finance_db.reports TO ROLE finance_analyst;

-- Row-level security role
CREATE ROLE regional_manager;
CREATE ROW ACCESS POLICY region_access AS (region STRING) RETURNS BOOLEAN ->
    CASE 
        WHEN CURRENT_ROLE() = 'DATA_ADMIN' THEN TRUE
        WHEN CURRENT_ROLE() = 'REGIONAL_MANAGER' AND region = 'NORTH' THEN TRUE
        ELSE FALSE
    END;

-- 7. Monitor Role Usage and Permissions
SHOW GRANTS TO ROLE data_analyst;
SHOW GRANTS TO USER john_analyst;
SHOW ROLES;

-- Check current role and switch roles
SELECT CURRENT_ROLE();
USE ROLE data_engineer;

-- Audit role usage
SELECT 
    user_name,
    role_name,
    granted_on,
    granted_by,
    created_on
FROM snowflake.account_usage.grants_to_users
WHERE user_name = 'JOHN_ANALYST';

-- Monitor privilege usage
SELECT 
    user_name,
    role_name,
    query_text,
    execution_status
FROM snowflake.account_usage.query_history
WHERE user_name = 'JOHN_ANALYST'
  AND start_time >= DATEADD('day', -1, CURRENT_TIMESTAMP())
ORDER BY start_time DESC;
```

**Output:**
```
privilege    granted_on    name              granted_to    granted_by
USAGE       WAREHOUSE     SMALL_WH          DATA_ANALYST  ACCOUNTADMIN
SELECT      TABLE         CUSTOMERS         DATA_ANALYST  ACCOUNTADMIN
SELECT      TABLE         ORDERS           DATA_ANALYST  ACCOUNTADMIN
```

### 15. What is Snowpipe and how do you implement continuous data loading?

**Answer:** Snowpipe enables automatic, continuous data loading as files arrive in cloud storage using event notifications.

```sql
-- 1. Create Snowpipe with Auto-Ingest
CREATE PIPE sales_pipe
    AUTO_INGEST = TRUE
    AWS_SNS_TOPIC = 'arn:aws:sns:us-east-1:123456789012:snowpipe-notifications'
AS
    COPY INTO sales_data
    FROM @s3_stage/sales/
    FILE_FORMAT = (
        TYPE = 'CSV'
        FIELD_DELIMITER = ','
        SKIP_HEADER = 1
        NULL_IF = ('NULL', 'null', '')
    )
    ON_ERROR = 'CONTINUE';

-- 2. Snowpipe for JSON data
CREATE PIPE events_pipe
    AUTO_INGEST = TRUE
AS
    COPY INTO user_events (user_id, event_data)
    FROM (
        SELECT 
            $1:user_id::NUMBER,
            $1
        FROM @json_stage/events/
    )
    FILE_FORMAT = (TYPE = 'JSON')
    ON_ERROR = 'CONTINUE';

-- 3. Check Pipe Status
SELECT SYSTEM$PIPE_STATUS('sales_pipe');

-- 4. Monitor Pipe History and Performance
SELECT 
    pipe_name,
    file_name,
    status,
    rows_inserted,
    rows_parsed,
    errors_seen,
    first_error_message,
    last_received_time,
    last_inserted_time
FROM TABLE(INFORMATION_SCHEMA.PIPE_USAGE_HISTORY(
    DATE_RANGE_START => DATEADD('day', -7, CURRENT_TIMESTAMP()),
    PIPE_NAME => 'SALES_PIPE'
))
ORDER BY last_received_time DESC;

-- 5. Manual Pipe Refresh (for testing)
ALTER PIPE sales_pipe REFRESH;

-- 6. Pipe with Error Handling
CREATE PIPE robust_sales_pipe
    AUTO_INGEST = TRUE
    ERROR_INTEGRATION = 'MY_ERROR_INTEGRATION'
AS
    COPY INTO sales_data
    FROM @s3_stage/sales/
    FILE_FORMAT = csv_format
    ON_ERROR = 'SKIP_FILE_3'  -- Skip file after 3 errors
    SIZE_LIMIT = 1000000;    -- 1MB file size limit

-- 7. Monitor Pipe Credits Usage
SELECT 
    pipe_name,
    credits_used,
    bytes_inserted,
    files_inserted
FROM snowflake.account_usage.pipe_usage_history
WHERE start_time >= DATEADD('day', -30, CURRENT_TIMESTAMP())
GROUP BY pipe_name, DATE_TRUNC('day', start_time)
ORDER BY credits_used DESC;

-- 8. Pause and Resume Pipes
ALTER PIPE sales_pipe SET PIPE_EXECUTION_PAUSED = TRUE;
ALTER PIPE sales_pipe SET PIPE_EXECUTION_PAUSED = FALSE;

-- 9. Drop Pipe
DROP PIPE sales_pipe;

-- 10. Snowpipe REST API Usage (Python example)
/*
import requests
import json

# Get pipe status via REST API
url = "https://account.snowflakecomputing.com/v1/data/pipes/SALES_PIPE/insertReport"
headers = {
    "Authorization": "Bearer <token>",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
pipe_status = response.json()
*/
```

**Output:**
```
PIPE_NAME     FILE_NAME           STATUS    ROWS_INSERTED    ERRORS_SEEN    LAST_RECEIVED_TIME
SALES_PIPE    sales_001.csv       LOADED    15000           0              2024-01-15 10:30:15
SALES_PIPE    sales_002.csv       LOADED    12500           0              2024-01-15 10:31:22
SALES_PIPE    sales_003.csv       PARTIALLY 8900            5              2024-01-15 10:32:18

SYSTEM$PIPE_STATUS('SALES_PIPE'): {"executionState":"RUNNING","pendingFileCount":0}
```

### 16. How do you work with different data types and constraints in Snowflake?

**Answer:** Snowflake supports standard SQL data types plus specialized types like VARIANT, with flexible constraint options.

```sql
-- 1. Comprehensive Data Types Example
CREATE TABLE comprehensive_data (
    -- Numeric types
    id NUMBER(10,0) NOT NULL,
    price DECIMAL(12,2),
    quantity INTEGER,
    rate FLOAT,
    score DOUBLE PRECISION,
    
    -- String types
    product_name VARCHAR(255) NOT NULL,
    description TEXT,
    category CHAR(10),
    
    -- Date and time types
    created_date DATE,
    updated_timestamp TIMESTAMP_NTZ,
    event_time TIMESTAMP_LTZ,
    duration TIME,
    
    -- Boolean type
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Semi-structured types
    metadata VARIANT,
    tags ARRAY,
    attributes OBJECT,
    
    -- Binary type
    file_content BINARY,
    
    -- Geography type (if enabled)
    location GEOGRAPHY
);

-- 2. Add Constraints
ALTER TABLE comprehensive_data ADD CONSTRAINT pk_id PRIMARY KEY (id);
ALTER TABLE comprehensive_data ADD CONSTRAINT chk_price CHECK (price >= 0);
ALTER TABLE comprehensive_data ADD CONSTRAINT chk_quantity CHECK (quantity > 0);
ALTER TABLE comprehensive_data ADD CONSTRAINT uk_product_name UNIQUE (product_name);

-- 3. Create Sequences for Auto-increment
CREATE SEQUENCE product_seq START = 1 INCREMENT = 1;

-- 4. Insert Data with Various Types
INSERT INTO comprehensive_data VALUES (
    product_seq.NEXTVAL,                    -- Auto-increment ID
    999.99,                                 -- DECIMAL
    100,                                    -- INTEGER
    0.15,                                   -- FLOAT
    95.5,                                   -- DOUBLE
    'Premium Laptop',                       -- VARCHAR
    'High-performance laptop with SSD',     -- TEXT
    'TECH',                                -- CHAR
    CURRENT_DATE(),                        -- DATE
    CURRENT_TIMESTAMP(),                   -- TIMESTAMP_NTZ
    CURRENT_TIMESTAMP(),                   -- TIMESTAMP_LTZ
    '02:30:00',                           -- TIME
    TRUE,                                  -- BOOLEAN
    PARSE_JSON('{"brand": "TechCorp", "model": "X1", "specs": {"ram": "16GB", "storage": "512GB"}}'), -- VARIANT
    ARRAY_CONSTRUCT('electronics', 'computers', 'laptops'), -- ARRAY
    OBJECT_CONSTRUCT('warranty', '2 years', 'support', '24/7'), -- OBJECT
    TO_BINARY('sample file content'),      -- BINARY
    TO_GEOGRAPHY('POINT(-122.35 37.55)')  -- GEOGRAPHY
);

-- 5. Query Different Data Types
SELECT 
    id,
    product_name,
    price,
    metadata:brand::STRING as brand,
    metadata:specs.ram::STRING as ram,
    tags[0]::STRING as first_tag,
    ARRAY_SIZE(tags) as tag_count,
    attributes:warranty::STRING as warranty_period,
    ST_X(location) as longitude,
    ST_Y(location) as latitude
FROM comprehensive_data;

-- 6. Data Type Conversions
SELECT 
    id,
    price::STRING as price_string,
    TRY_CAST(product_name AS NUMBER) as name_as_number, -- Returns NULL if conversion fails
    created_date::TIMESTAMP as date_as_timestamp,
    is_active::STRING as active_string
FROM comprehensive_data;

-- 7. Working with VARIANT Data
SELECT 
    id,
    TYPEOF(metadata) as metadata_type,
    OBJECT_KEYS(metadata) as available_keys,
    metadata:specs as specs_object,
    FLATTEN(metadata:specs) as flattened_specs
FROM comprehensive_data;

-- 8. Array and Object Operations
SELECT 
    id,
    ARRAY_APPEND(tags, 'new-tag') as updated_tags,
    ARRAY_SLICE(tags, 0, 2) as first_two_tags,
    OBJECT_INSERT(attributes, 'color', 'silver') as updated_attributes,
    OBJECT_DELETE(attributes, 'support') as attributes_without_support
FROM comprehensive_data;

-- 9. Check Data Types and Constraints
DESCRIBE TABLE comprehensive_data;
SHOW PRIMARY KEYS IN TABLE comprehensive_data;
SHOW UNIQUE KEYS IN TABLE comprehensive_data;

-- 10. Constraint Validation
-- This will fail due to CHECK constraint
-- INSERT INTO comprehensive_data (id, price, quantity) VALUES (2, -100, 5);

-- This will fail due to UNIQUE constraint
-- INSERT INTO comprehensive_data (id, product_name) VALUES (3, 'Premium Laptop');
```

**Output:**
```
ID    PRODUCT_NAME     PRICE    BRAND      RAM     FIRST_TAG      TAG_COUNT    WARRANTY_PERIOD
1     Premium Laptop   999.99   TechCorp   16GB    electronics    3            2 years

Column Name       Data Type        Nullable    Default    Primary Key    Unique Key
ID               NUMBER(10,0)      N          NULL       Y              N
PRICE            NUMBER(12,2)      Y          NULL       N              N
PRODUCT_NAME     VARCHAR(255)      N          NULL       N              Y
METADATA         VARIANT           Y          NULL       N              N
```

### 17. What are materialized views and how do you use them for performance optimization?

**Answer:** Materialized views store pre-computed query results that automatically refresh when underlying data changes.

```sql
-- 1. Create Materialized View for Aggregations
CREATE MATERIALIZED VIEW sales_summary AS
SELECT 
    DATE_TRUNC('month', sale_date) as month,
    region,
    product_category,
    SUM(amount) as total_sales,
    COUNT(*) as transaction_count,
    AVG(amount) as avg_transaction_amount,
    COUNT(DISTINCT customer_id) as unique_customers
FROM sales_data
WHERE sale_date >= '2023-01-01'
GROUP BY 1, 2, 3;

-- 2. Materialized View with Joins
CREATE MATERIALIZED VIEW customer_sales_summary AS
SELECT 
    c.customer_id,
    c.customer_name,
    c.region,
    c.customer_segment,
    COUNT(s.sale_id) as total_orders,
    SUM(s.amount) as total_spent,
    AVG(s.amount) as avg_order_value,
    MAX(s.sale_date) as last_purchase_date,
    DATEDIFF('day', MAX(s.sale_date), CURRENT_DATE()) as days_since_last_purchase
FROM customers c
JOIN sales_data s ON c.customer_id = s.customer_id
WHERE s.sale_date >= '2023-01-01'
GROUP BY c.customer_id, c.customer_name, c.region, c.customer_segment;

-- 3. Query Materialized Views (automatic optimization)
-- Snowflake automatically uses materialized view when possible
SELECT 
    month,
    region,
    total_sales,
    unique_customers
FROM sales_summary
WHERE month >= '2024-01-01'
  AND region = 'North America'
ORDER BY total_sales DESC;

-- 4. Check Materialized View Status
SHOW MATERIALIZED VIEWS;

SELECT 
    name,
    database_name,
    schema_name,
    owner,
    created_on,
    is_secure,
    automatic_clustering
FROM snowflake.account_usage.materialized_views
WHERE name = 'SALES_SUMMARY';

-- 5. Monitor Materialized View Refresh
SELECT 
    materialized_view_name,
    refresh_start_time,
    refresh_end_time,
    credits_used,
    bytes_scanned,
    rows_inserted,
    rows_updated,
    rows_deleted
FROM snowflake.account_usage.materialized_view_refresh_history
WHERE materialized_view_name = 'SALES_SUMMARY'
ORDER BY refresh_start_time DESC;

-- 6. Manual Refresh (if needed)
ALTER MATERIALIZED VIEW sales_summary REFRESH;

-- 7. Suspend/Resume Materialized View
ALTER MATERIALIZED VIEW sales_summary SUSPEND;
ALTER MATERIALIZED VIEW sales_summary RESUME;

-- 8. Materialized View with Clustering
CREATE MATERIALIZED VIEW clustered_sales_summary
CLUSTER BY (month, region) AS
SELECT 
    DATE_TRUNC('month', sale_date) as month,
    region,
    product_category,
    SUM(amount) as total_sales,
    COUNT(*) as transaction_count
FROM sales_data
GROUP BY 1, 2, 3;

-- 9. Secure Materialized View
CREATE SECURE MATERIALIZED VIEW secure_financial_summary AS
SELECT 
    DATE_TRUNC('quarter', transaction_date) as quarter,
    account_type,
    SUM(transaction_amount) as total_amount,
    COUNT(*) as transaction_count
FROM financial_transactions
WHERE transaction_date >= '2023-01-01'
GROUP BY 1, 2;

-- 10. Drop Materialized View
DROP MATERIALIZED VIEW sales_summary;

-- 11. Check Query Optimization with Materialized Views
-- Use EXPLAIN to see if materialized view is used
EXPLAIN 
SELECT 
    region,
    SUM(total_sales) as region_total
FROM sales_summary
WHERE month >= '2024-01-01'
GROUP BY region;
```

**Output:**
```
MONTH       REGION          TOTAL_SALES    UNIQUE_CUSTOMERS
2024-01     North America   1250000.00     8500
2024-01     Europe          890000.00      6200
2024-01     Asia Pacific    1100000.00     7800

MATERIALIZED_VIEW_NAME    REFRESH_START_TIME       CREDITS_USED    ROWS_INSERTED
SALES_SUMMARY            2024-01-15 10:30:00      0.25           1250
SALES_SUMMARY            2024-01-15 11:30:00      0.18           89
```

### 18. How do you work with external tables for querying data without loading?

**Answer:** External tables provide a way to query data stored in external cloud storage without loading it into Snowflake.

```sql
-- 1. Create External Table for CSV Files
CREATE EXTERNAL TABLE sales_external (
    sale_id NUMBER AS (value:c1::NUMBER),
    customer_id NUMBER AS (value:c2::NUMBER),
    product_id NUMBER AS (value:c3::NUMBER),
    sale_date DATE AS (value:c4::DATE),
    amount DECIMAL(10,2) AS (value:c5::DECIMAL(10,2)),
    region STRING AS (value:c6::STRING)
)
LOCATION = @s3_stage/sales/
FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1)
AUTO_REFRESH = TRUE
PATTERN = '.*sales.*\.csv';

-- 2. External Table for Parquet Files
CREATE EXTERNAL TABLE events_external (
    event_id NUMBER AS (value:event_id::NUMBER),
    user_id NUMBER AS (value:user_id::NUMBER),
    event_type STRING AS (value:event_type::STRING),
    event_timestamp TIMESTAMP AS (value:event_timestamp::TIMESTAMP),
    properties VARIANT AS (value:properties::VARIANT)
)
LOCATION = @s3_stage/events/
FILE_FORMAT = (TYPE = 'PARQUET')
AUTO_REFRESH = TRUE;

-- 3. External Table for JSON Files
CREATE EXTERNAL TABLE logs_external (
    log_timestamp TIMESTAMP AS (value:timestamp::TIMESTAMP),
    log_level STRING AS (value:level::STRING),
    message STRING AS (value:message::STRING),
    source_ip STRING AS (value:source_ip::STRING),
    user_agent STRING AS (value:user_agent::STRING)
)
LOCATION = @s3_stage/logs/
FILE_FORMAT = (TYPE = 'JSON')
AUTO_REFRESH = FALSE;

-- 4. Query External Tables
SELECT 
    region,
    COUNT(*) as transaction_count,
    SUM(amount) as total_sales,
    AVG(amount) as avg_transaction
FROM sales_external
WHERE sale_date >= '2024-01-01'
GROUP BY region
ORDER BY total_sales DESC;

-- 5. Join External and Internal Tables
SELECT 
    c.customer_name,
    c.customer_segment,
    se.region,
    SUM(se.amount) as total_spent
FROM sales_external se
JOIN customers c ON se.customer_id = c.customer_id
WHERE se.sale_date >= '2024-01-01'
GROUP BY c.customer_name, c.customer_segment, se.region
HAVING total_spent > 10000;

-- 6. Monitor External Table Metadata
SELECT 
    file_name,
    file_size,
    last_modified,
    etag,
    md5
FROM TABLE(INFORMATION_SCHEMA.EXTERNAL_TABLE_FILES(
    TABLE_NAME => 'SALES_EXTERNAL'
))
ORDER BY last_modified DESC;

-- 7. Refresh External Table Metadata
ALTER EXTERNAL TABLE sales_external REFRESH;

-- 8. External Table with Partitioning
CREATE EXTERNAL TABLE partitioned_sales_external (
    sale_id NUMBER AS (value:c1::NUMBER),
    customer_id NUMBER AS (value:c2::NUMBER),
    amount DECIMAL(10,2) AS (value:c3::DECIMAL(10,2)),
    year NUMBER AS (SUBSTR(METADATA$FILENAME, 7, 4)::NUMBER),
    month NUMBER AS (SUBSTR(METADATA$FILENAME, 12, 2)::NUMBER)
)
PARTITION BY (year, month)
LOCATION = @s3_stage/partitioned_sales/
FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1)
PATTERN = '.*sales_[0-9]{4}_[0-9]{2}.*\.csv';

-- 9. Query with Partition Pruning
SELECT 
    COUNT(*) as transaction_count,
    SUM(amount) as total_sales
FROM partitioned_sales_external
WHERE year = 2024 AND month = 1;

-- 10. Create Materialized View on External Table
CREATE MATERIALIZED VIEW external_sales_summary AS
SELECT 
    region,
    DATE_TRUNC('month', sale_date) as month,
    SUM(amount) as total_sales,
    COUNT(*) as transaction_count
FROM sales_external
GROUP BY region, month;

-- 11. Monitor External Table Usage
SELECT 
    table_name,
    credits_used,
    bytes_scanned,
    files_scanned
FROM snowflake.account_usage.external_table_usage_history
WHERE table_name = 'SALES_EXTERNAL'
  AND start_time >= DATEADD('day', -7, CURRENT_TIMESTAMP())
ORDER BY start_time DESC;
```

**Output:**
```
REGION          TRANSACTION_COUNT    TOTAL_SALES    AVG_TRANSACTION
North America   15000               2500000.00     166.67
Europe          12000               1800000.00     150.00
Asia Pacific    18000               2200000.00     122.22

FILE_NAME              FILE_SIZE    LAST_MODIFIED              ETAG
sales_2024_01_15.csv   1048576     2024-01-15T10:30:00Z      "abc123"
sales_2024_01_14.csv   987654      2024-01-14T10:30:00Z      "def456"
```

### 19. What's the difference between transient, temporary, and permanent tables?

**Answer:** Different table types offer varying levels of data persistence, Time Travel capabilities, and storage costs.

```sql
-- 1. Permanent Table (Default)
CREATE TABLE permanent_customers (
    customer_id NUMBER,
    customer_name VARCHAR(255),
    email VARCHAR(255),
    registration_date DATE
);
-- Features: Full Time Travel (1-90 days), Fail-safe (7 days), highest storage cost

-- 2. Transient Table
CREATE TRANSIENT TABLE transient_staging (
    load_id NUMBER,
    raw_data VARIANT,
    processed_timestamp TIMESTAMP,
    status VARCHAR(50)
);
-- Features: Limited Time Travel (1 day max), no Fail-safe, lower storage cost

-- 3. Temporary Table
CREATE TEMPORARY TABLE temp_calculations (
    calculation_id NUMBER,
    input_value DECIMAL(10,2),
    result DECIMAL(15,4),
    calculation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
-- Features: Session-specific, no Time Travel, no Fail-safe, lowest cost

-- 4. Compare Table Types
INSERT INTO permanent_customers VALUES 
    (1, 'John Doe', 'john@email.com', '2024-01-01');

INSERT INTO transient_staging VALUES 
    (1, PARSE_JSON('{"source": "api", "records": 100}'), CURRENT_TIMESTAMP(), 'LOADED');

INSERT INTO temp_calculations VALUES 
    (1, 100.50, 150.75, CURRENT_TIMESTAMP());

-- 5. Time Travel Capabilities
-- Permanent table - full Time Travel
SELECT * FROM permanent_customers AT (TIMESTAMP => '2024-01-14 10:00:00');

-- Transient table - limited Time Travel (1 day)
SELECT * FROM transient_staging AT (OFFSET => -3600); -- 1 hour ago

-- Temporary table - no Time Travel (will fail)
-- SELECT * FROM temp_calculations AT (OFFSET => -3600); -- ERROR

-- 6. Set Retention Periods
ALTER TABLE permanent_customers SET DATA_RETENTION_TIME_IN_DAYS = 30;
ALTER TABLE transient_staging SET DATA_RETENTION_TIME_IN_DAYS = 1; -- Max for transient

-- 7. Check Table Information
SELECT 
    table_name,
    table_type,
    is_transient,
    retention_time,
    created
FROM snowflake.account_usage.tables
WHERE table_schema = CURRENT_SCHEMA()
  AND table_name IN ('PERMANENT_CUSTOMERS', 'TRANSIENT_STAGING');

-- 8. Storage Usage Comparison
SELECT 
    table_name,
    active_bytes / (1024*1024) as active_mb,
    time_travel_bytes / (1024*1024) as time_travel_mb,
    failsafe_bytes / (1024*1024) as failsafe_mb
FROM snowflake.account_usage.table_storage_metrics
WHERE table_name IN ('PERMANENT_CUSTOMERS', 'TRANSIENT_STAGING');

-- 9. Create Transient Database/Schema
CREATE TRANSIENT DATABASE staging_db;
CREATE TRANSIENT SCHEMA temp_schema;

-- All tables in transient database/schema are transient by default
USE DATABASE staging_db;
CREATE TABLE auto_transient_table (id NUMBER, data VARCHAR(100));

-- 10. Temporary Table Session Behavior
-- Temporary tables are automatically dropped when session ends
SHOW TABLES LIKE 'TEMP_%';

-- Create another session's temporary table (won't conflict)
CREATE TEMPORARY TABLE temp_calculations (
    different_id NUMBER,
    different_data VARCHAR(100)
);

-- 11. Use Cases for Each Type
/*
PERMANENT TABLES:
- Production data requiring full recovery capabilities
- Master data and dimension tables
- Critical business data with compliance requirements

TRANSIENT TABLES:
- ETL staging and intermediate processing
- Data that can be easily recreated
- Development and testing environments

TEMPORARY TABLES:
- Session-specific calculations
- Temporary result sets for complex queries
- Data that doesn't need persistence
*/

-- 12. Cost Optimization Strategy
-- Use transient for staging
CREATE TRANSIENT TABLE staging_sales AS
SELECT * FROM permanent_sales WHERE load_date = CURRENT_DATE();

-- Process data
INSERT INTO permanent_sales_summary
SELECT 
    region,
    SUM(amount) as total_sales
FROM staging_sales
GROUP BY region;

-- Clean up staging (or let it expire)
DROP TABLE staging_sales;
```

**Output:**
```
TABLE_NAME            TABLE_TYPE    IS_TRANSIENT    RETENTION_TIME    CREATED
PERMANENT_CUSTOMERS   BASE TABLE    NO             30                2024-01-15
TRANSIENT_STAGING     BASE TABLE    YES            1                 2024-01-15

TABLE_NAME            ACTIVE_MB    TIME_TRAVEL_MB    FAILSAFE_MB
PERMANENT_CUSTOMERS   5.2         1.8               2.1
TRANSIENT_STAGING     3.1         0.5               0.0
```

### 20. How do you implement data masking and column-level security?

**Answer:** Use masking policies to dynamically protect sensitive data based on user roles and context.

```sql
-- 1. Create Masking Policy for SSN
CREATE MASKING POLICY ssn_mask AS (val STRING) RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() IN ('ADMIN', 'HR_MANAGER', 'COMPLIANCE_OFFICER') THEN val
        WHEN CURRENT_ROLE() IN ('ANALYST', 'MANAGER') THEN '***-**-' || RIGHT(val, 4)
        WHEN CURRENT_ROLE() = 'INTERN' THEN '***-**-****'
        ELSE '***-**-****'
    END;

-- 2. Create Email Masking Policy
CREATE MASKING POLICY email_mask AS (val STRING) RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() IN ('ADMIN', 'CUSTOMER_SERVICE') THEN val
        WHEN CURRENT_ROLE() IN ('ANALYST', 'MANAGER') THEN 
            REGEXP_REPLACE(val, '(.{2})(.*)(@.*)', '\\1****\\3')
        ELSE '****@****.***'
    END;

-- 3. Create Credit Card Masking Policy
CREATE MASKING POLICY credit_card_mask AS (val STRING) RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() IN ('ADMIN', 'FINANCE_MANAGER') THEN val
        WHEN CURRENT_ROLE() = 'CUSTOMER_SERVICE' THEN 
            '****-****-****-' || RIGHT(val, 4)
        ELSE '****-****-****-****'
    END;

-- 4. Create Salary Masking Policy with Ranges
CREATE MASKING POLICY salary_mask AS (val NUMBER) RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() IN ('ADMIN', 'HR_MANAGER', 'PAYROLL') THEN val::STRING
        WHEN CURRENT_ROLE() = 'MANAGER' THEN 
            CASE 
                WHEN val < 50000 THEN '< $50K'
                WHEN val < 100000 THEN '$50K - $100K'
                WHEN val < 150000 THEN '$100K - $150K'
                ELSE '> $150K'
            END
        ELSE 'CONFIDENTIAL'
    END;

-- 5. Apply Masking Policies to Table Columns
CREATE TABLE employees (
    employee_id NUMBER,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    ssn VARCHAR(11),
    email VARCHAR(255),
    salary NUMBER(10,2),
    credit_card VARCHAR(19),
    hire_date DATE,
    department VARCHAR(50)
);

-- Apply masking policies
ALTER TABLE employees MODIFY COLUMN ssn SET MASKING POLICY ssn_mask;
ALTER TABLE employees MODIFY COLUMN email SET MASKING POLICY email_mask;
ALTER TABLE employees MODIFY COLUMN salary SET MASKING POLICY salary_mask;
ALTER TABLE employees MODIFY COLUMN credit_card SET MASKING POLICY credit_card_mask;

-- 6. Insert Sample Data
INSERT INTO employees VALUES
    (1, 'John', 'Doe', '123-45-6789', 'john.doe@company.com', 75000, '1234-5678-9012-3456', '2023-01-15', 'Engineering'),
    (2, 'Jane', 'Smith', '987-65-4321', 'jane.smith@company.com', 85000, '9876-5432-1098-7654', '2023-02-01', 'Marketing'),
    (3, 'Bob', 'Johnson', '555-44-3333', 'bob.johnson@company.com', 120000, '5555-4444-3333-2222', '2022-06-10', 'Management');

-- 7. Test Masking with Different Roles
USE ROLE admin;
SELECT employee_id, first_name, last_name, ssn, email, salary, credit_card 
FROM employees;
-- Shows: Full data visible

USE ROLE analyst;
SELECT employee_id, first_name, last_name, ssn, email, salary, credit_card 
FROM employees;
-- Shows: Masked SSN (***-**-6789), masked email (jo****@company.com), salary ranges

USE ROLE intern;
SELECT employee_id, first_name, last_name, ssn, email, salary, credit_card 
FROM employees;
-- Shows: Fully masked sensitive data

-- 8. Conditional Masking Based on Data Values
CREATE MASKING POLICY department_salary_mask AS (val NUMBER, dept STRING) RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() = 'ADMIN' THEN val::STRING
        WHEN CURRENT_ROLE() = 'HR_MANAGER' THEN val::STRING
        WHEN CURRENT_ROLE() = 'DEPT_MANAGER' AND dept = 'Engineering' THEN val::STRING
        WHEN CURRENT_ROLE() = 'ANALYST' AND val < 100000 THEN val::STRING
        ELSE 'CONFIDENTIAL'
    END;

-- Apply conditional masking
ALTER TABLE employees MODIFY COLUMN salary SET MASKING POLICY department_salary_mask USING (salary, department);

-- 9. Create Dynamic Masking Based on User Context
CREATE MASKING POLICY user_context_mask AS (val STRING, emp_id NUMBER) RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() = 'ADMIN' THEN val
        WHEN CURRENT_USER() = 'JOHN_DOE' AND emp_id = 1 THEN val  -- Users can see their own data
        WHEN CURRENT_ROLE() = 'MANAGER' THEN '***-**-' || RIGHT(val, 4)
        ELSE '***-**-****'
    END;

-- 10. Monitor Masking Policy Usage
SELECT 
    policy_name,
    policy_kind,
    policy_body,
    created_on,
    owner
FROM snowflake.account_usage.masking_policies
WHERE policy_name LIKE '%MASK%';

-- 11. Show Applied Masking Policies
DESCRIBE TABLE employees;

-- 12. Remove Masking Policy
ALTER TABLE employees MODIFY COLUMN ssn UNSET MASKING POLICY;

-- 13. Create Masking Policy with External Functions
CREATE MASKING POLICY advanced_mask AS (val STRING) RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() = 'ADMIN' THEN val
        WHEN IS_ROLE_IN_SESSION('ANALYST') THEN 
            -- Could call external function for complex masking
            REGEXP_REPLACE(val, '(.{2})(.*)(@.*)', '\\1****\\3')
        ELSE 'MASKED'
    END;
```

**Output (as different roles):**
```
-- As ADMIN role:
EMPLOYEE_ID    FIRST_NAME    SSN           EMAIL                    SALARY    CREDIT_CARD
1             John          123-45-6789   john.doe@company.com     75000     1234-5678-9012-3456

-- As ANALYST role:
EMPLOYEE_ID    FIRST_NAME    SSN           EMAIL                    SALARY         CREDIT_CARD
1             John          ***-**-6789   jo****@company.com       $50K - $100K   ****-****-****-3456

-- As INTERN role:
EMPLOYEE_ID    FIRST_NAME    SSN           EMAIL              SALARY         CREDIT_CARD
1             John          ***-**-****   ****@****.***      CONFIDENTIAL   ****-****-****-****
```