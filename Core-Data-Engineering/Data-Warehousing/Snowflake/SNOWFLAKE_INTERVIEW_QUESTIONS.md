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

**Answer:** Snowflake is a cloud-native data warehouse with unique multi-cluster, shared data architecture.

#### **Key Differences:**

| Aspect | Snowflake | Traditional DW |
|--------|-----------|----------------|
| **Architecture** | Multi-cluster, shared data | Shared-nothing MPP |
| **Scaling** | Independent compute/storage | Scale entire system |
| **Maintenance** | Zero maintenance | Manual tuning required |
| **Pricing** | Pay-per-use | Fixed licensing |
| **Deployment** | Cloud-native | On-premises/hybrid |

```sql
-- Snowflake's elastic scaling
CREATE WAREHOUSE analytics_wh WITH
    WAREHOUSE_SIZE = 'LARGE'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 10;

-- Monitor usage
SELECT 
    warehouse_name,
    credits_used,
    avg_running_time
FROM snowflake.account_usage.warehouse_metering_history
WHERE start_time >= DATEADD('day', -7, CURRENT_TIMESTAMP());
```

### 2. Explain Snowflake's three-layer architecture.

**Answer:** Snowflake separates storage, compute, and services into independent layers.

#### **Architecture Layers:**
- **Storage Layer**: Immutable micro-partitions in cloud storage
- **Compute Layer**: Virtual warehouses for query processing
- **Services Layer**: Metadata, security, and optimization

```sql
-- Storage layer - automatic micro-partitioning
CREATE TABLE sales_data (
    sale_id NUMBER,
    sale_date DATE,
    customer_id NUMBER,
    amount DECIMAL(10,2)
);

-- Compute layer - virtual warehouses
CREATE WAREHOUSE etl_warehouse WITH WAREHOUSE_SIZE = 'MEDIUM';
CREATE WAREHOUSE analytics_warehouse WITH WAREHOUSE_SIZE = 'LARGE';

-- Services layer handles metadata automatically
SHOW TABLES;
DESCRIBE TABLE sales_data;
```

### 3. What are virtual warehouses and how do they work?

**Answer:** Virtual warehouses are compute clusters that execute queries independently.

```sql
-- Create warehouse with auto-scaling
CREATE WAREHOUSE my_warehouse WITH
    WAREHOUSE_SIZE = 'MEDIUM'
    AUTO_SUSPEND = 60           -- Suspend after 1 minute
    AUTO_RESUME = TRUE          -- Resume automatically
    MIN_CLUSTER_COUNT = 1       -- Minimum clusters
    MAX_CLUSTER_COUNT = 5       -- Maximum for scaling
    SCALING_POLICY = 'STANDARD'; -- STANDARD or ECONOMY

-- Resize warehouse dynamically
ALTER WAREHOUSE my_warehouse SET WAREHOUSE_SIZE = 'LARGE';

-- Monitor warehouse performance
SELECT 
    query_id,
    warehouse_name,
    warehouse_size,
    execution_time,
    queued_provisioning_time
FROM snowflake.account_usage.query_history
WHERE start_time >= DATEADD('hour', -1, CURRENT_TIMESTAMP());
```

### 4. How do you load data into Snowflake?

**Answer:** Multiple methods including COPY command, Snowpipe, and external tables.

```sql
-- 1. COPY command for batch loading
CREATE FILE FORMAT csv_format
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    NULL_IF = ('NULL', 'null', '');

CREATE STAGE my_stage
    URL = 's3://my-bucket/data/'
    CREDENTIALS = (AWS_KEY_ID = 'key' AWS_SECRET_KEY = 'secret');

COPY INTO sales_data
FROM @my_stage/sales.csv
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE';

-- 2. Snowpipe for continuous loading
CREATE PIPE sales_pipe
    AUTO_INGEST = TRUE
AS
    COPY INTO sales_data
    FROM @my_stage/
    FILE_FORMAT = csv_format;

-- Monitor loading
SELECT * FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => 'SALES_DATA',
    START_TIME => DATEADD(hours, -1, CURRENT_TIMESTAMP())
));
```

### 5. What are micro-partitions in Snowflake?

**Answer:** Immutable, compressed data files (50-500MB) that store table data.

```sql
-- Micro-partitions are created automatically
INSERT INTO sales_data VALUES
    (1, '2024-01-01', 100, 1500.00),
    (2, '2024-01-02', 101, 2000.00);

-- Check partition information
SELECT 
    table_name,
    row_count,
    bytes,
    micropartition_count
FROM snowflake.account_usage.table_storage_metrics
WHERE table_name = 'SALES_DATA';

-- Clustering improves partition pruning
ALTER TABLE sales_data CLUSTER BY (sale_date);
```

### 6. How does Snowflake handle concurrency?

**Answer:** Multi-cluster warehouses provide automatic concurrency scaling.

```sql
-- Multi-cluster warehouse for concurrency
CREATE WAREHOUSE concurrent_wh WITH
    WAREHOUSE_SIZE = 'MEDIUM'
    MIN_CLUSTER_COUNT = 2
    MAX_CLUSTER_COUNT = 8
    SCALING_POLICY = 'STANDARD'
    AUTO_SUSPEND = 300;

-- Monitor concurrency
SELECT 
    warehouse_name,
    cluster_number,
    start_time,
    end_time,
    credits_used
FROM snowflake.account_usage.warehouse_load_history
WHERE start_time >= DATEADD('hour', -1, CURRENT_TIMESTAMP());
```

### 7. What is Time Travel in Snowflake?

**Answer:** Feature that allows querying historical data and recovering from changes.

```sql
-- Query data at specific time
SELECT * FROM sales_data AT (TIMESTAMP => '2024-01-01 12:00:00');

-- Query data before specific statement
SELECT * FROM sales_data BEFORE (STATEMENT => '01a2b3c4-5678-90de-f123-456789abcdef');

-- Restore table to previous state
CREATE OR REPLACE TABLE sales_data AS
SELECT * FROM sales_data AT (TIMESTAMP => '2024-01-01 10:00:00');

-- Set retention period
ALTER TABLE sales_data SET DATA_RETENTION_TIME_IN_DAYS = 7;

-- Undrop table
UNDROP TABLE accidentally_dropped_table;
```

### 8. How do you optimize query performance in Snowflake?

**Answer:** Use clustering keys, result caching, and proper warehouse sizing.

```sql
-- 1. Clustering keys
ALTER TABLE large_table CLUSTER BY (date_column, category);

-- Check clustering effectiveness
SELECT SYSTEM$CLUSTERING_DEPTH('large_table', '(date_column, category)');

-- 2. Result caching (automatic for 24 hours)
SELECT customer_id, SUM(amount) FROM sales_data GROUP BY customer_id;

-- 3. Warehouse sizing
ALTER WAREHOUSE analytics_wh SET WAREHOUSE_SIZE = 'X-LARGE';

-- 4. Query optimization
SELECT customer_id, amount
FROM sales_data
WHERE sale_date >= '2024-01-01'
  AND region = 'US'
LIMIT 1000;
```

### 9. What are the different Snowflake editions?

**Answer:** Standard, Enterprise, Business Critical, and Virtual Private Snowflake.

| Edition | Key Features | Time Travel | Multi-Cluster |
|---------|-------------|-------------|---------------|
| **Standard** | Basic features | 1 day | No |
| **Enterprise** | Advanced security | 90 days | Yes |
| **Business Critical** | Enhanced security, HIPAA | 90 days | Yes |
| **VPS** | Dedicated infrastructure | 90 days | Yes |

### 10. How do you monitor Snowflake usage and costs?

**Answer:** Use account usage views and resource monitors.

```sql
-- Monitor credit usage
SELECT 
    warehouse_name,
    SUM(credits_used) as total_credits,
    AVG(credits_used_compute) as avg_compute_credits
FROM snowflake.account_usage.warehouse_metering_history
WHERE start_time >= DATEADD('month', -1, CURRENT_TIMESTAMP())
GROUP BY warehouse_name;

-- Create resource monitor
CREATE RESOURCE MONITOR monthly_limit WITH
    CREDIT_QUOTA = 1000
    FREQUENCY = MONTHLY
    START_TIMESTAMP = IMMEDIATELY
    TRIGGERS 
        ON 75 PERCENT DO NOTIFY
        ON 100 PERCENT DO SUSPEND;

-- Apply to warehouse
ALTER WAREHOUSE analytics_wh SET RESOURCE_MONITOR = monthly_limit;

### 11. What is zero-copy cloning in Snowflake?

**Answer:** Create instant copies of databases, schemas, or tables without duplicating data.

```sql
-- Clone database
CREATE DATABASE dev_db CLONE prod_db;

-- Clone table
CREATE TABLE sales_backup CLONE sales_data;

-- Clone with time travel
CREATE TABLE sales_yesterday CLONE sales_data 
AT (TIMESTAMP => '2024-01-01 00:00:00');

-- Clone from stream
CREATE TABLE sales_stream_clone CLONE sales_stream;

-- Monitor clone storage
SELECT 
    table_name,
    clone_group_id,
    bytes,
    retained_for_clone_bytes
FROM snowflake.account_usage.table_storage_metrics
WHERE clone_group_id IS NOT NULL;
```

### 12. How do you handle semi-structured data in Snowflake?

**Answer:** Use VARIANT data type and built-in functions for JSON, XML, Avro, Parquet.

```sql
-- Create table with VARIANT column
CREATE TABLE user_events (
    event_id NUMBER,
    event_timestamp TIMESTAMP,
    event_data VARIANT
);

-- Insert JSON data
INSERT INTO user_events VALUES
    (1, CURRENT_TIMESTAMP(), PARSE_JSON('{"user_id": 123, "action": "click", "page": "home"}')),
    (2, CURRENT_TIMESTAMP(), PARSE_JSON('{"user_id": 456, "action": "view", "product": "laptop"}'));

-- Query semi-structured data
SELECT 
    event_id,
    event_data:user_id::NUMBER as user_id,
    event_data:action::STRING as action,
    event_data:page::STRING as page
FROM user_events;

-- Flatten nested arrays
SELECT 
    event_id,
    f.value:name::STRING as item_name,
    f.value:price::NUMBER as item_price
FROM user_events,
LATERAL FLATTEN(input => event_data:items) f;
```

### 13. What are Snowflake stages and how do you use them?

**Answer:** Stages are locations where data files are stored for loading into tables.

```sql
-- Internal stage (Snowflake-managed)
CREATE STAGE internal_stage;

-- External stage (cloud storage)
CREATE STAGE s3_stage
    URL = 's3://my-bucket/data/'
    CREDENTIALS = (
        AWS_KEY_ID = 'AKIAIOSFODNN7EXAMPLE'
        AWS_SECRET_KEY = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
    )
    FILE_FORMAT = (TYPE = 'CSV' FIELD_DELIMITER = ',');

-- List files in stage
LIST @s3_stage;

-- Load data from stage
COPY INTO sales_data FROM @s3_stage/sales.csv;

-- Remove files from stage
REMOVE @s3_stage/processed/;
```

### 14. How do you implement role-based access control (RBAC) in Snowflake?

**Answer:** Create roles, grant privileges, and assign roles to users.

```sql
-- Create roles
CREATE ROLE data_analyst;
CREATE ROLE data_engineer;
CREATE ROLE data_admin;

-- Grant privileges to roles
GRANT USAGE ON WAREHOUSE analytics_wh TO ROLE data_analyst;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO ROLE data_analyst;
GRANT ALL PRIVILEGES ON SCHEMA etl TO ROLE data_engineer;

-- Create role hierarchy
GRANT ROLE data_analyst TO ROLE data_engineer;
GRANT ROLE data_engineer TO ROLE data_admin;

-- Assign roles to users
GRANT ROLE data_analyst TO USER john_doe;

-- Switch roles
USE ROLE data_engineer;

-- Check current role and privileges
SELECT CURRENT_ROLE();
SHOW GRANTS TO ROLE data_analyst;
```

### 15. What is Snowpipe and when would you use it?

**Answer:** Snowpipe enables continuous, automatic data loading as files arrive.

```sql
-- Create pipe with auto-ingest
CREATE PIPE sales_pipe
    AUTO_INGEST = TRUE
    AWS_SNS_TOPIC = 'arn:aws:sns:us-east-1:123456789012:snowpipe-topic'
AS
    COPY INTO sales_data
    FROM @s3_stage/sales/
    FILE_FORMAT = csv_format
    ON_ERROR = 'CONTINUE';

-- Check pipe status
SELECT SYSTEM$PIPE_STATUS('sales_pipe');

-- Monitor pipe history
SELECT 
    pipe_name,
    file_name,
    status,
    rows_inserted,
    errors_seen,
    last_received_time
FROM TABLE(INFORMATION_SCHEMA.PIPE_USAGE_HISTORY(
    DATE_RANGE_START => DATEADD('hour', -24, CURRENT_TIMESTAMP()),
    PIPE_NAME => 'SALES_PIPE'
));

-- Refresh pipe manually
ALTER PIPE sales_pipe REFRESH;
```

### 16. How do you handle data types and constraints in Snowflake?

**Answer:** Snowflake supports standard SQL data types with some unique features.

```sql
-- Create table with various data types
CREATE TABLE customer_data (
    customer_id NUMBER(10,0) NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    registration_date DATE,
    last_login TIMESTAMP_NTZ,
    profile_data VARIANT,
    is_active BOOLEAN DEFAULT TRUE,
    credit_limit NUMBER(12,2),
    tags ARRAY,
    metadata OBJECT
);

-- Add constraints
ALTER TABLE customer_data ADD CONSTRAINT pk_customer PRIMARY KEY (customer_id);
ALTER TABLE customer_data ADD CONSTRAINT chk_email CHECK (email LIKE '%@%.%');

-- Create sequence for auto-increment
CREATE SEQUENCE customer_seq START = 1 INCREMENT = 1;

-- Use sequence in insert
INSERT INTO customer_data (customer_id, customer_name, email)
VALUES (customer_seq.NEXTVAL, 'John Doe', 'john@example.com');
```

### 17. What are materialized views in Snowflake?

**Answer:** Pre-computed views that store query results for faster access.

```sql
-- Create materialized view
CREATE MATERIALIZED VIEW sales_summary AS
SELECT 
    DATE_TRUNC('month', sale_date) as month,
    region,
    product_category,
    SUM(amount) as total_sales,
    COUNT(*) as transaction_count,
    AVG(amount) as avg_transaction
FROM sales_data
GROUP BY 1, 2, 3;

-- Query uses materialized view automatically
SELECT month, region, total_sales
FROM sales_summary
WHERE month >= '2024-01-01';

-- Monitor materialized view usage
SHOW MATERIALIZED VIEWS;

-- Refresh materialized view
ALTER MATERIALIZED VIEW sales_summary REFRESH;
```

### 18. How do you work with external tables in Snowflake?

**Answer:** External tables allow querying data in external storage without loading.

```sql
-- Create external table
CREATE EXTERNAL TABLE sales_external (
    sale_id NUMBER AS (value:c1::NUMBER),
    customer_id NUMBER AS (value:c2::NUMBER),
    sale_date DATE AS (value:c3::DATE),
    amount DECIMAL(10,2) AS (value:c4::DECIMAL(10,2))
)
LOCATION = @s3_stage/sales/
FILE_FORMAT = csv_format
AUTO_REFRESH = TRUE;

-- Query external table
SELECT * FROM sales_external 
WHERE sale_date >= '2024-01-01';

-- Monitor external table metadata
SELECT 
    file_name,
    file_size,
    last_modified,
    etag
FROM TABLE(INFORMATION_SCHEMA.EXTERNAL_TABLE_FILES(
    TABLE_NAME => 'SALES_EXTERNAL'
));
```

### 19. What is the difference between transient and temporary tables?

**Answer:** Different table types with varying persistence and Time Travel capabilities.

```sql
-- Permanent table (default)
CREATE TABLE permanent_sales (
    sale_id NUMBER,
    amount DECIMAL(10,2)
);
-- Has full Time Travel (1-90 days based on edition)

-- Transient table
CREATE TRANSIENT TABLE transient_sales (
    sale_id NUMBER,
    amount DECIMAL(10,2)
);
-- Has limited Time Travel (1 day max)
-- Lower storage costs

-- Temporary table
CREATE TEMPORARY TABLE temp_sales (
    sale_id NUMBER,
    amount DECIMAL(10,2)
);
-- Session-specific, no Time Travel
-- Automatically dropped when session ends

-- Check table types
SHOW TABLES;
```

### 20. How do you implement data masking in Snowflake?

**Answer:** Use masking policies to protect sensitive data based on user roles.

```sql
-- Create masking policy for SSN
CREATE MASKING POLICY ssn_mask AS (val STRING) RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() IN ('ADMIN', 'HR_MANAGER') THEN val
        WHEN CURRENT_ROLE() = 'ANALYST' THEN '***-**-' || RIGHT(val, 4)
        ELSE '***-**-****'
    END;

-- Apply masking policy to column
ALTER TABLE employees MODIFY COLUMN ssn SET MASKING POLICY ssn_mask;

-- Create email masking policy
CREATE MASKING POLICY email_mask AS (val STRING) RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() IN ('ADMIN', 'MANAGER') THEN val
        ELSE REGEXP_REPLACE(val, '(.{2})(.*)(@.*)', '\\1****\\3')
    END;

-- Apply to email column
ALTER TABLE customers MODIFY COLUMN email SET MASKING POLICY email_mask;

-- Query shows masked data based on current role
SELECT employee_id, name, ssn FROM employees;
SELECT customer_id, name, email FROM customers;

### 21. How do you handle errors during data loading?

**Answer:** Use error handling options in COPY command and monitor load history.

```sql
-- Error handling options
COPY INTO sales_data
FROM @s3_stage/sales.csv
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE'          -- Skip errors and continue
-- ON_ERROR = 'SKIP_FILE'      -- Skip entire file on error
-- ON_ERROR = 'ABORT_STATEMENT' -- Stop on first error (default)
ERROR_LIMIT = 100;             -- Maximum errors allowed

-- Validate data before loading
SELECT 
    $1 as col1,
    $2 as col2,
    METADATA$FILENAME,
    METADATA$FILE_ROW_NUMBER
FROM @s3_stage/sales.csv
(FILE_FORMAT => csv_format)
WHERE $1 IS NULL OR $2 IS NULL;

-- Check load errors
SELECT 
    file_name,
    status,
    error_count,
    first_error_message,
    first_error_line_number
FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => 'SALES_DATA',
    START_TIME => DATEADD('hour', -1, CURRENT_TIMESTAMP())
));
```

### 22. What are Snowflake's data sharing capabilities?

**Answer:** Secure, real-time data sharing without copying data.

```sql
-- Create share (provider)
CREATE SHARE customer_data_share;

-- Grant database access to share
GRANT USAGE ON DATABASE customer_db TO SHARE customer_data_share;
GRANT USAGE ON SCHEMA customer_db.public TO SHARE customer_data_share;

-- Grant table access
GRANT SELECT ON TABLE customer_db.public.customers TO SHARE customer_data_share;
GRANT SELECT ON TABLE customer_db.public.orders TO SHARE customer_data_share;

-- Add consumer accounts
ALTER SHARE customer_data_share ADD ACCOUNTS = ('CONSUMER_ACCOUNT_1', 'CONSUMER_ACCOUNT_2');

-- Create database from share (consumer)
CREATE DATABASE shared_customer_data FROM SHARE provider_account.customer_data_share;

-- Monitor share usage
SELECT 
    share_name,
    consumer_account,
    credits_used,
    bytes_transferred
FROM snowflake.account_usage.data_transfer_history
WHERE start_time >= DATEADD('day', -7, CURRENT_TIMESTAMP());
```

### 23. How do you work with streams in Snowflake?

**Answer:** Streams capture data changes (CDC) for incremental processing.

```sql
-- Create stream on table
CREATE STREAM sales_stream ON TABLE sales_data;

-- Create stream on view
CREATE STREAM sales_view_stream ON VIEW sales_summary;

-- Query stream to see changes
SELECT 
    sale_id,
    customer_id,
    amount,
    METADATA$ACTION,
    METADATA$ISUPDATE,
    METADATA$ROW_ID
FROM sales_stream;

-- Process stream data
INSERT INTO sales_audit
SELECT 
    sale_id,
    customer_id,
    amount,
    METADATA$ACTION as change_type,
    CURRENT_TIMESTAMP() as processed_at
FROM sales_stream
WHERE METADATA$ACTION IN ('INSERT', 'UPDATE');

-- Check if stream has data
SELECT SYSTEM$STREAM_HAS_DATA('sales_stream');

### 24. What are tasks in Snowflake and how do you use them?

**Answer:** Tasks enable scheduling and automation of SQL statements.

```sql
-- Create simple scheduled task
CREATE TASK daily_sales_summary
    WAREHOUSE = analytics_wh
    SCHEDULE = 'USING CRON 0 2 * * * UTC'  -- Daily at 2 AM UTC
AS
    INSERT INTO daily_sales_summary
    SELECT 
        DATE(sale_date) as sale_date,
        region,
        SUM(amount) as total_sales,
        COUNT(*) as transaction_count
    FROM sales_data
    WHERE DATE(sale_date) = CURRENT_DATE() - 1
    GROUP BY 1, 2;

-- Start task
ALTER TASK daily_sales_summary RESUME;
```

### 25-30. Additional Basic Questions

**25. How do you optimize storage costs in Snowflake?**
**Answer:** Use transient tables, appropriate retention periods, and monitor storage usage.

**26. What is the difference between COPY and INSERT?**
**Answer:** COPY is optimized for bulk loading, INSERT for individual records.

**27. How do you handle schema changes?**
**Answer:** Use ALTER statements and consider impact on dependent objects.

**28. What are the different ways to connect to Snowflake?**
**Answer:** Web UI, SnowSQL, JDBC/ODBC, Python connector, REST API.

**29. How do you implement data validation?**
**Answer:** Use constraints, data quality checks, and validation procedures.

**30. What are Snowflake's security features?**
**Answer:** Encryption, authentication, RBAC, network security, data masking.

---

## Intermediate Level Questions (31-60)

### 31. How do you implement advanced clustering strategies?

**Answer:** Use multi-column clustering and automatic clustering for optimal performance.

```sql
-- Multi-column clustering
ALTER TABLE large_fact_table CLUSTER BY (date_column, region, product_category);

-- Check clustering effectiveness
SELECT SYSTEM$CLUSTERING_INFORMATION('large_fact_table', '(date_column, region)');

-- Automatic clustering (Enterprise+)
ALTER TABLE large_fact_table RESUME RECLUSTER;

-- Monitor clustering costs
SELECT 
    table_name,
    credits_used,
    num_bytes_reclustered,
    num_rows_reclustered
FROM snowflake.account_usage.automatic_clustering_history
WHERE start_time >= DATEADD('day', -7, CURRENT_TIMESTAMP());
```

### 32. How do you implement row-level security?

**Answer:** Create row access policies based on user context.

```sql
-- Create row access policy
CREATE ROW ACCESS POLICY customer_policy AS (region VARCHAR) RETURNS BOOLEAN ->
    CASE 
        WHEN CURRENT_ROLE() = 'ADMIN' THEN TRUE
        WHEN CURRENT_ROLE() = 'SALES_MANAGER' AND region = 'NORTH_AMERICA' THEN TRUE
        WHEN CURRENT_ROLE() = 'ANALYST' AND region IN ('EUROPE', 'ASIA') THEN TRUE
        ELSE FALSE
    END;

-- Apply policy to table
ALTER TABLE customers ADD ROW ACCESS POLICY customer_policy ON (region);

-- Query respects row-level security
SELECT * FROM customers; -- Only shows allowed rows
```

### 33. How do you optimize complex joins?

**Answer:** Use appropriate join strategies, clustering, and query hints.

```sql
-- Optimize large table joins with clustering
ALTER TABLE fact_sales CLUSTER BY (customer_id, product_id);
ALTER TABLE dim_customer CLUSTER BY (customer_id);

-- Use query hints for join optimization
SELECT /*+ USE_CACHED_RESULT(FALSE) */ 
    c.customer_name,
    SUM(s.amount) as total_sales
FROM fact_sales s
JOIN dim_customer c ON s.customer_id = c.customer_id
WHERE s.sale_date >= '2024-01-01'
GROUP BY c.customer_name;

-- Monitor join performance
SELECT 
    query_id,
    query_text,
    execution_time,
    bytes_scanned,
    partitions_scanned
FROM snowflake.account_usage.query_history
WHERE query_text ILIKE '%JOIN%'
ORDER BY execution_time DESC;
```

### 34-60. Additional Intermediate Questions

**34. How do you implement incremental data loading?**
**Answer:** Use streams, merge statements, and change data capture.

**35. What are stored procedures and how do you use them?**
**Answer:** Server-side code execution for complex business logic.

**36. How do you handle large-scale data transformations?**
**Answer:** Use appropriate warehouse sizing and parallel processing.

**37. What is the Snowflake Data Marketplace?**
**Answer:** Platform for discovering and accessing third-party data.

**38. How do you implement data lineage tracking?**
**Answer:** Use account usage views and custom metadata tracking.

**39. What are external functions and when to use them?**
**Answer:** Call external APIs and services from SQL queries.

**40. How do you optimize warehouse usage?**
**Answer:** Right-size warehouses and use auto-suspend/resume.

**41-60. [Additional intermediate questions covering advanced SQL, performance tuning, data modeling, integration patterns, monitoring, troubleshooting, and best practices]**

---

## Advanced Level Questions (61-90)

### 61. How do you design a multi-tenant data architecture in Snowflake?

**Answer:** Implement tenant isolation using schemas, databases, or row-level security.

```sql
-- Database-level isolation
CREATE DATABASE tenant_1_db;
CREATE DATABASE tenant_2_db;

-- Schema-level isolation
CREATE SCHEMA tenant_1_schema;
CREATE SCHEMA tenant_2_schema;

-- Row-level isolation with policy
CREATE ROW ACCESS POLICY tenant_isolation AS (tenant_id VARCHAR) RETURNS BOOLEAN ->
    tenant_id = CURRENT_USER() OR CURRENT_ROLE() = 'ADMIN';

ALTER TABLE multi_tenant_data ADD ROW ACCESS POLICY tenant_isolation ON (tenant_id);
```

### 62-90. Additional Advanced Questions

**62. How do you implement disaster recovery strategies?**
**Answer:** Use replication, failover, and backup strategies.

**63. What are hybrid tables and when to use them?**
**Answer:** OLTP capabilities with ACID transactions for operational workloads.

**64. How do you optimize for mixed workloads?**
**Answer:** Use multiple warehouses and workload management.

**65-90. [Additional advanced questions covering enterprise architecture, advanced security, compliance, performance at scale, custom solutions, and expert-level troubleshooting]**

---

## Architecture & Performance (91-120)

### 91. How do you design Snowflake architecture for high availability?

**Answer:** Implement multi-region deployment and failover strategies.

### 92-120. [Architecture and performance questions covering scaling, optimization, monitoring, and enterprise patterns]**

---

## Streaming & Real-time Processing (121-150)

### 121. How do you implement near real-time data processing?

**Answer:** Use Snowpipe, streams, and tasks for continuous processing.

### 122-150. [Streaming questions covering Snowpipe, change data capture, real-time analytics, and integration patterns]**

---

## Production & Operations (151-180)

### 151. How do you deploy Snowflake solutions in production?

**Answer:** Use CI/CD pipelines, version control, and automated testing.

### 152-180. [Production questions covering deployment, monitoring, maintenance, troubleshooting, and operational excellence]**

---

## Scenario-Based Questions (181-200)

### 181. Design a data warehouse solution for a retail company.

**Answer:** Implement dimensional modeling with fact and dimension tables.

### 182-200. [Scenario questions covering real-world implementations, problem-solving, and system design]**
```
```
```
