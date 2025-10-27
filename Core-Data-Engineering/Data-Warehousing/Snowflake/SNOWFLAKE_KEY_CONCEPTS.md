# ❄️ Snowflake Key Concepts for Data Engineering

> **Think of Snowflake as the ultimate smart shopping mall for data - it has separate floors for different activities (compute and storage), automatic escalators that appear when needed (auto-scaling), and a central management system that handles everything from security to billing, all while multiple shoppers can browse simultaneously without interfering with each other**

[![Snowflake](https://img.shields.io/badge/Snowflake-Latest-blue)](https://snowflake.com/)
[![Difficulty](https://img.shields.io/badge/Difficulty-Intermediate-yellow)](https://github.com/yourusername/Data-Engineering-Material)
[![Interview Frequency](https://img.shields.io/badge/Interview-Very%20High-red)](https://github.com/yourusername/Data-Engineering-Material)

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Architecture](#-architecture)
3. [Core Features](#-core-features)
4. [Data Loading & ETL](#-data-loading--etl)
5. [Performance Optimization](#-performance-optimization)
6. [Security & Governance](#-security--governance)
7. [Time Travel & Data Recovery](#-time-travel--data-recovery)
8. [Streams & Tasks](#-streams--tasks)
9. [Data Sharing & Marketplace](#-data-sharing--marketplace)
10. [Cost Optimization](#-cost-optimization)
11. [Integration Capabilities](#-integration-capabilities)
12. [Version Highlights](#-version-highlights)
13. [When to Use Snowflake](#-when-to-use-snowflake)
14. [Interview Focus Areas](#-interview-focus-areas)
15. [Quick References](#-quick-references)

---

## 🎯 Overview - The Smart Data Mall

> **Think of Snowflake as the world's most advanced shopping mall where the storage areas (warehouses) are completely separate from the shopping floors (compute), allowing unlimited shoppers to browse simultaneously while the mall automatically adjusts its size based on crowd levels**

### 🏬 **Smart Mall Analogy**
Snowflake is like a revolutionary shopping mall where:
- **🏪 Storage Basement** - Unlimited warehouse space that never runs out
- **🛍️ Shopping Floors** - Separate floors that can be added or removed instantly based on shopper traffic
- **🎫 Central Management** - One system handles security, billing, and coordination
- **🚶‍♂️ Independent Shoppers** - Multiple groups can shop simultaneously without affecting each other
- **⚡ Smart Escalators** - Transportation appears automatically when needed, disappears when not
- **🔄 Instant Copies** - Create duplicate stores instantly without copying inventory

### 💼 **Why This Smart Mall Approach Works**
- **Unlimited Capacity** - Storage grows automatically as your data collection expands
- **Flexible Shopping Experience** - Add more floors during busy periods, reduce during quiet times
- **Cost Efficiency** - Pay only for the shopping floors you use, storage is incredibly cheap
- **No Maintenance** - Mall management handles all infrastructure, security, and updates
- **Perfect Coordination** - Multiple departments can work simultaneously without conflicts

Snowflake is a cloud-native data warehouse built for the cloud, offering a unique multi-cluster, shared data architecture that separates compute from storage. It provides ANSI SQL support, automatic scaling, and zero-maintenance operations.

**🏆 Key Smart Mall Benefits:**
- **🏪➕🛍️ Separation of Storage and Compute** = **Warehouse + Shopping Floors** - Scale independently based on workload needs (add more floors without expanding storage)
- **🏬 Multi-Cluster Architecture** = **Multiple Shopping Floors** - Concurrent workloads without resource contention (different departments shop simultaneously)
- **📋 Zero-Copy Cloning** = **Instant Store Replicas** - Instant data copies without storage duplication (duplicate stores share the same inventory)
- **⏰ Time Travel** = **Security Camera Playback** - Query historical data and recover from changes (see what the store looked like yesterday)
- **⚡ Automatic Scaling** = **Smart Escalators** - Elastic compute resources that scale up/down automatically (more floors appear during rush hour)
- **🤝 Data Sharing** = **Mall Partnerships** - Secure, real-time data sharing across organizations (partner stores share customer insights)

## 🏗️ Architecture

### Multi-Cluster, Shared Data Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            SNOWFLAKE ARCHITECTURE                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           SERVICES LAYER                                    │ │
│  │                                                                             │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │ │
│  │  │  Authentication │  │    Metadata     │  │ Query Optimizer │             │ │
│  │  │   & Security    │  │   Management    │  │   & Planner     │             │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘             │ │
│  │                                                                             │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │ │
│  │  │ Infrastructure  │  │ Transaction Mgmt│  │ Access Control  │             │ │
│  │  │   Management    │  │ & Concurrency   │  │  & Governance   │             │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘             │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                       │                                         │
│                                       ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                          COMPUTE LAYER                                      │ │
│  │                      (Virtual Warehouses)                                   │ │
│  │                                                                             │ │
│  │ ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │ │
│  │ │   WAREHOUSE 1   │  │   WAREHOUSE 2   │  │   WAREHOUSE N   │             │ │
│  │ │                 │  │                 │  │                 │             │ │
│  │ │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │             │ │
│  │ │ │  Cluster 1  │ │  │ │  Cluster 1  │ │  │ │  Cluster 1  │ │             │ │
│  │ │ │  Cluster 2  │ │  │ │  Cluster 2  │ │  │ │  Cluster 2  │ │             │ │
│  │ │ │  Cluster N  │ │  │ │  Cluster N  │ │  │ │  Cluster N  │ │             │ │
│  │ │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │             │ │
│  │ │                 │  │                 │  │                 │             │ │
│  │ │ Auto-Suspend    │  │ Auto-Resume     │  │ Multi-Cluster   │             │ │
│  │ │ Auto-Resume     │  │ Auto-Scale      │  │ Auto-Scale      │             │ │
│  │ └─────────────────┘  └─────────────────┘  └─────────────────┘             │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                       │                                         │
│                                       ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                          STORAGE LAYER                                      │ │
│  │                      (Cloud Storage)                                        │ │
│  │                                                                             │ │
│  │ ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │ │
│  │ │ Micro-Partitions│  │   Compression   │  │   Encryption    │             │ │
│  │ │   (50-500MB)    │  │   & Columnar    │  │   (AES-256)     │             │ │
│  │ └─────────────────┘  └─────────────────┘  └─────────────────┘             │ │
│  │                                                                             │ │
│  │ ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │ │
│  │ │   Metadata      │  │ Time Travel     │  │ Zero-Copy Clone │             │ │
│  │ │   Statistics    │  │   History       │  │   References    │             │ │
│  │ │ └─────────────────┘  └─────────────────┘  └─────────────────┘             │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘

                                DATA FLOW
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  1. Client connects through Services Layer (authentication, authorization)     │
│  2. Query submitted to Services Layer for parsing and optimization             │
│  3. Services Layer creates execution plan and allocates Virtual Warehouse      │
│  4. Virtual Warehouse executes query against Storage Layer                     │
│  5. Storage Layer returns data through micro-partitions                        │
│  6. Results processed and returned to client                                   │
│  7. Virtual Warehouse can auto-suspend when idle                               │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Architecture Components

**1. Services Layer (Cloud Services)**
- **Authentication & Authorization**: User management and access control
- **Metadata Management**: Schema, statistics, and query history
- **Query Optimization**: Cost-based optimizer and execution planning
- **Infrastructure Management**: Resource allocation and monitoring
- **Transaction Management**: ACID compliance and concurrency control

**2. Compute Layer (Virtual Warehouses)**
- **Independent Scaling**: Each warehouse scales independently
- **Multi-Cluster**: Automatic scaling with multiple clusters
- **Auto-Suspend/Resume**: Automatic resource management
- **Workload Isolation**: Separate warehouses for different workloads

**3. Storage Layer**
- **Micro-Partitions**: Immutable, compressed data files (50-500MB)
- **Columnar Storage**: Optimized for analytical queries
- **Automatic Compression**: Built-in compression algorithms
- **Encryption**: AES-256 encryption at rest and in transit

## 📦 Core Features

### 1. Virtual Warehouses

**Definition**: Compute clusters that execute queries and DML operations. They can be created, resized, suspended, and resumed independently.

```sql
-- Create virtual warehouse
CREATE WAREHOUSE analytics_warehouse WITH
    WAREHOUSE_SIZE = 'LARGE'
    AUTO_SUSPEND = 300          -- Suspend after 5 minutes of inactivity
    AUTO_RESUME = TRUE          -- Resume automatically when queries submitted
    MIN_CLUSTER_COUNT = 1       -- Minimum clusters for multi-cluster warehouse
    MAX_CLUSTER_COUNT = 3       -- Maximum clusters for auto-scaling
    SCALING_POLICY = 'STANDARD' -- STANDARD or ECONOMY scaling
    INITIALLY_SUSPENDED = TRUE; -- Start in suspended state

-- Use warehouse
USE WAREHOUSE analytics_warehouse;

-- Resize warehouse dynamically
ALTER WAREHOUSE analytics_warehouse SET WAREHOUSE_SIZE = 'X-LARGE';

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

### 2. Micro-Partitions

**Definition**: Snowflake automatically partitions data into immutable micro-partitions (50-500MB each) with built-in compression and statistics.

```sql
-- Clustering keys for better micro-partition pruning
ALTER TABLE sales_data CLUSTER BY (sale_date, region);

-- Check clustering information
SELECT SYSTEM$CLUSTERING_INFORMATION('sales_data', '(sale_date, region)');

-- Monitor clustering depth
SELECT SYSTEM$CLUSTERING_DEPTH('sales_data', '(sale_date, region)');

-- Automatic clustering (Enterprise edition)
ALTER TABLE sales_data RESUME RECLUSTER;
```

### 3. Zero-Copy Cloning

**Definition**: Create instant copies of databases, schemas, or tables without duplicating underlying data.

```sql
-- Clone database
CREATE DATABASE dev_database CLONE prod_database;

-- Clone table
CREATE TABLE sales_backup CLONE sales_data;

-- Clone with time travel
CREATE TABLE sales_yesterday CLONE sales_data AT (TIMESTAMP => '2024-01-01 00:00:00');

-- Clone from stream
CREATE TABLE sales_stream_clone CLONE sales_stream;
```

## 🔄 Data Loading & ETL

### Loading Methods Comparison

| Method | Use Case | Latency | Throughput | Complexity |
|--------|----------|---------|------------|------------|
| **COPY Command** | Batch loading | Minutes | Very High | Low |
| **Snowpipe** | Near real-time | Seconds | High | Medium |
| **Kafka Connector** | Streaming | Sub-second | Medium | High |
| **External Tables** | Query without loading | Real-time | Variable | Low |

### 1. COPY Command (Batch Loading)

```sql
-- Create file format
CREATE FILE FORMAT csv_format
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    NULL_IF = ('NULL', 'null', '')
    EMPTY_FIELD_AS_NULL = TRUE
    COMPRESSION = 'GZIP';

-- Create stage
CREATE STAGE my_s3_stage
    URL = 's3://my-bucket/data/'
    CREDENTIALS = (AWS_KEY_ID = 'your_key' AWS_SECRET_KEY = 'your_secret')
    FILE_FORMAT = csv_format;

-- Load data with COPY
COPY INTO sales_data
FROM @my_s3_stage/sales/
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE'
PURGE = TRUE;

-- Monitor load history
SELECT 
    file_name,
    status,
    rows_parsed,
    rows_loaded,
    error_count,
    first_error_message
FROM table(information_schema.copy_history(
    table_name => 'SALES_DATA',
    start_time => dateadd(hours, -1, current_timestamp())
));
```

### 2. Snowpipe (Continuous Loading)

```sql
-- Create pipe for automatic loading
CREATE PIPE sales_pipe
    AUTO_INGEST = TRUE
    AWS_SNS_TOPIC = 'arn:aws:sns:us-east-1:123456789012:snowpipe-topic'
AS
    COPY INTO sales_data
    FROM @my_s3_stage/sales/
    FILE_FORMAT = csv_format;

-- Show pipe status
SELECT SYSTEM$PIPE_STATUS('sales_pipe');

-- Monitor pipe history
SELECT 
    pipe_name,
    file_name,
    status,
    rows_inserted,
    errors_seen
FROM table(information_schema.pipe_usage_history(
    date_range_start => dateadd(hours, -24, current_timestamp()),
    date_range_end => current_timestamp(),
    pipe_name => 'SALES_PIPE'
));
```

### 3. External Tables

```sql
-- Create external table
CREATE EXTERNAL TABLE sales_external (
    sale_id NUMBER AS (value:c1::NUMBER),
    customer_id NUMBER AS (value:c2::NUMBER),
    sale_date DATE AS (value:c3::DATE),
    amount DECIMAL(10,2) AS (value:c4::DECIMAL(10,2))
)
LOCATION = @my_s3_stage/sales/
FILE_FORMAT = csv_format
AUTO_REFRESH = TRUE;

-- Query external table
SELECT * FROM sales_external WHERE sale_date >= '2024-01-01';
```

## ⚡ Performance Optimization

### 1. Clustering Keys

**Definition**: Organize data within micro-partitions to improve query performance by reducing data scanning.

```sql
-- Add clustering key
ALTER TABLE fact_sales CLUSTER BY (sale_date, region);

-- Multi-column clustering
ALTER TABLE customer_data CLUSTER BY (customer_segment, registration_date);

-- Check clustering effectiveness
SELECT 
    table_name,
    clustering_key,
    total_partition_count,
    total_constant_partition_count,
    average_overlaps,
    average_depth,
    partition_depth_histogram
FROM snowflake.information_schema.automatic_clustering_history
WHERE table_name = 'FACT_SALES'
ORDER BY start_time DESC;

-- Manual reclustering
ALTER TABLE fact_sales RECLUSTER;
```

### 2. Result Caching

**Definition**: Snowflake caches query results for 24 hours, providing instant responses for identical queries.

```sql
-- Query result caching (automatic)
SELECT customer_segment, COUNT(*) 
FROM customers 
GROUP BY customer_segment;

-- Use cached results from previous query
SELECT * FROM TABLE(RESULT_SCAN('01234567-89ab-cdef-0123-456789abcdef'));

-- Disable result caching for specific query
SELECT customer_segment, COUNT(*) 
FROM customers 
GROUP BY customer_segment
OPTION (DISABLE_QUERY_RESULT_CACHE = TRUE);
```

### 3. Materialized Views

```sql
-- Create materialized view for common aggregations
CREATE MATERIALIZED VIEW sales_summary AS
SELECT 
    DATE_TRUNC('month', sale_date) AS month,
    region,
    product_category,
    SUM(amount) AS total_sales,
    COUNT(*) AS transaction_count,
    AVG(amount) AS avg_transaction
FROM fact_sales
GROUP BY 1, 2, 3;

-- Query uses materialized view automatically
SELECT month, region, total_sales
FROM sales_summary
WHERE month >= '2024-01-01';

-- Monitor materialized view usage
SHOW MATERIALIZED VIEWS;
```

## 🔒 Security & Governance

### 1. Role-Based Access Control (RBAC)

```sql
-- Create roles
CREATE ROLE data_analyst;
CREATE ROLE data_engineer;
CREATE ROLE data_admin;

-- Grant privileges to roles
GRANT USAGE ON WAREHOUSE analytics_warehouse TO ROLE data_analyst;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO ROLE data_analyst;
GRANT ALL PRIVILEGES ON SCHEMA etl TO ROLE data_engineer;

-- Create role hierarchy
GRANT ROLE data_analyst TO ROLE data_engineer;
GRANT ROLE data_engineer TO ROLE data_admin;

-- Assign roles to users
GRANT ROLE data_analyst TO USER john_doe;
```

### 2. Row-Level Security

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
SELECT * FROM customers; -- Only shows rows based on current role
```

### 3. Column-Level Security

```sql
-- Create masking policy
CREATE MASKING POLICY ssn_mask AS (val STRING) RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() IN ('ADMIN', 'HR_MANAGER') THEN val
        ELSE '***-**-' || RIGHT(val, 4)
    END;

-- Apply masking policy
ALTER TABLE employees MODIFY COLUMN ssn SET MASKING POLICY ssn_mask;

-- Query shows masked data based on role
SELECT employee_id, name, ssn FROM employees;
```

## ⏰ Time Travel & Data Recovery

### Time Travel Capabilities

```sql
-- Query data as of specific timestamp
SELECT * FROM sales_data AT (TIMESTAMP => '2024-01-01 12:00:00');

-- Query data as of specific offset
SELECT * FROM sales_data AT (OFFSET => -3600); -- 1 hour ago

-- Query data before specific statement
SELECT * FROM sales_data BEFORE (STATEMENT => '01234567-89ab-cdef-0123-456789abcdef');

-- Compare current vs historical data
SELECT 
    current.customer_id,
    current.status AS current_status,
    historical.status AS previous_status
FROM customers current
JOIN customers AT (TIMESTAMP => '2024-01-01 00:00:00') historical
    ON current.customer_id = historical.customer_id
WHERE current.status != historical.status;

-- Restore table to previous state
CREATE OR REPLACE TABLE sales_data AS
SELECT * FROM sales_data AT (TIMESTAMP => '2024-01-01 12:00:00');

-- Undrop table
UNDROP TABLE accidentally_dropped_table;

-- Set retention period (1-90 days)
ALTER TABLE important_data SET DATA_RETENTION_TIME_IN_DAYS = 30;
```

## 🌊 Streams & Tasks

### 1. Streams (Change Data Capture)

```sql
-- Create stream on table
CREATE STREAM sales_stream ON TABLE sales_data;

-- Create stream on view
CREATE STREAM sales_view_stream ON VIEW sales_summary;

-- Query stream to see changes
SELECT 
    customer_id,
    amount,
    METADATA$ACTION,
    METADATA$ISUPDATE,
    METADATA$ROW_ID
FROM sales_stream;

-- Process stream data
INSERT INTO sales_audit
SELECT 
    customer_id,
    amount,
    METADATA$ACTION AS change_type,
    CURRENT_TIMESTAMP() AS processed_at
FROM sales_stream
WHERE METADATA$ACTION = 'INSERT';

-- Check stream status
SHOW STREAMS;
```

### 2. Tasks (Scheduling)

```sql
-- Create task for data processing
CREATE TASK daily_sales_summary
    WAREHOUSE = analytics_warehouse
    SCHEDULE = 'USING CRON 0 2 * * * UTC' -- Daily at 2 AM UTC
AS
    INSERT INTO daily_sales_summary
    SELECT 
        DATE(sale_date) AS sale_date,
        region,
        SUM(amount) AS total_sales,
        COUNT(*) AS transaction_count
    FROM sales_data
    WHERE DATE(sale_date) = CURRENT_DATE() - 1
    GROUP BY 1, 2;

-- Create task with stream dependency
CREATE TASK process_sales_changes
    WAREHOUSE = analytics_warehouse
    SCHEDULE = '5 MINUTE'
    WHEN SYSTEM$STREAM_HAS_DATA('sales_stream')
AS
    CALL process_sales_stream_procedure();

-- Start task
ALTER TASK daily_sales_summary RESUME;

-- Monitor task history
SELECT 
    name,
    state,
    scheduled_time,
    completed_time,
    return_value
FROM table(information_schema.task_history())
WHERE name = 'DAILY_SALES_SUMMARY'
ORDER BY scheduled_time DESC;
```

## 🤝 Data Sharing & Marketplace

### 1. Secure Data Sharing

```sql
-- Create share
CREATE SHARE customer_data_share;

-- Grant access to database/schema
GRANT USAGE ON DATABASE customer_db TO SHARE customer_data_share;
GRANT USAGE ON SCHEMA customer_db.public TO SHARE customer_data_share;

-- Grant access to specific tables
GRANT SELECT ON TABLE customer_db.public.customers TO SHARE customer_data_share;
GRANT SELECT ON TABLE customer_db.public.orders TO SHARE customer_data_share;

-- Add accounts to share
ALTER SHARE customer_data_share ADD ACCOUNTS = ('PARTNER_ACCOUNT_1', 'PARTNER_ACCOUNT_2');

-- Create database from share (consumer side)
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

### 2. Snowflake Marketplace

```sql
-- List available data products
SHOW SHARES IN ACCOUNT;

-- Create database from marketplace listing
CREATE DATABASE weather_data FROM SHARE SFC_SAMPLES.SAMPLE_DATA;

-- Query marketplace data
SELECT * FROM weather_data.weather.daily_14_total LIMIT 10;
```

## 💰 Cost Optimization

### 1. Warehouse Management

```sql
-- Right-size warehouses based on workload
CREATE WAREHOUSE small_etl WITH WAREHOUSE_SIZE = 'SMALL' AUTO_SUSPEND = 60;
CREATE WAREHOUSE large_analytics WITH WAREHOUSE_SIZE = 'LARGE' AUTO_SUSPEND = 300;

-- Use multi-cluster for concurrent workloads
CREATE WAREHOUSE concurrent_warehouse WITH
    WAREHOUSE_SIZE = 'MEDIUM'
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 5
    SCALING_POLICY = 'ECONOMY'; -- Favor cost over performance

-- Monitor credit usage
SELECT 
    warehouse_name,
    SUM(credits_used) AS total_credits,
    AVG(credits_used_compute) AS avg_compute_credits,
    AVG(credits_used_cloud_services) AS avg_cloud_services_credits
FROM snowflake.account_usage.warehouse_metering_history
WHERE start_time >= DATEADD('month', -1, CURRENT_TIMESTAMP())
GROUP BY warehouse_name
ORDER BY total_credits DESC;
```

### 2. Storage Optimization

```sql
-- Monitor storage usage
SELECT 
    table_name,
    active_bytes / (1024*1024*1024) AS active_gb,
    time_travel_bytes / (1024*1024*1024) AS time_travel_gb,
    failsafe_bytes / (1024*1024*1024) AS failsafe_gb,
    retained_for_clone_bytes / (1024*1024*1024) AS clone_gb
FROM snowflake.account_usage.table_storage_metrics
WHERE deleted = FALSE
ORDER BY active_bytes DESC;

-- Optimize data retention
ALTER TABLE temp_data SET DATA_RETENTION_TIME_IN_DAYS = 1;
ALTER TABLE archive_data SET DATA_RETENTION_TIME_IN_DAYS = 7;

-- Drop unused objects
DROP TABLE IF EXISTS old_temp_table;
DROP VIEW IF EXISTS unused_view;
```

## 🔗 Integration Capabilities

### 1. Native Connectors

```sql
-- Kafka connector configuration
CREATE PIPE kafka_sales_pipe
    AUTO_INGEST = TRUE
AS
    COPY INTO sales_data
    FROM @kafka_stage
    FILE_FORMAT = (TYPE = 'JSON');

-- Spark connector (via external tools)
-- Configure Spark to write to Snowflake
-- spark.write.format("snowflake")
--   .options(sfOptions)
--   .option("dbtable", "sales_data")
--   .mode("append")
--   .save()
```

### 2. REST API Integration

```sql
-- Create API integration
CREATE API INTEGRATION my_api_integration
    API_PROVIDER = 'aws_api_gateway'
    API_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/snowflake-api-role'
    ENABLED = TRUE;

-- Create external function
CREATE EXTERNAL FUNCTION enrich_customer_data(customer_id NUMBER)
RETURNS VARIANT
LANGUAGE PYTHON
API_INTEGRATION = my_api_integration
HEADERS = ('content-type' = 'application/json')
AS 'https://api.example.com/enrich';

-- Use external function
SELECT 
    customer_id,
    enrich_customer_data(customer_id) AS enriched_data
FROM customers;
```

## 📈 Version Highlights

### Recent Version Features

**Snowflake 7.x (2024)**
- **Iceberg Tables**: Native support for Apache Iceberg format
- **Hybrid Tables**: OLTP capabilities with ACID transactions
- **Cortex AI**: Built-in AI/ML functions and LLM integration
- **Dynamic Tables**: Materialized views with automatic refresh
- **Native Apps**: Custom applications within Snowflake

**Snowflake 6.x (2023)**
- **Snowpark**: Native support for Python, Java, and Scala
- **Streamlit Integration**: Build and deploy apps directly in Snowflake
- **External Functions**: Call external APIs from SQL
- **Search Optimization**: Improved performance for point lookups

**Key Capabilities by Edition**
- **Standard**: Basic features, time travel (1 day)
- **Enterprise**: Advanced security, time travel (90 days), multi-cluster
- **Business Critical**: Enhanced security, customer-managed keys, tri-secret secure
- **Virtual Private Snowflake**: Dedicated infrastructure, complete isolation

## 🎯 When to Use Snowflake

**Ideal Use Cases:**
- **Data Warehousing**: OLAP workloads, business intelligence, reporting
- **Data Lake Analytics**: Query structured and semi-structured data
- **Real-time Analytics**: Stream processing with Snowpipe and streams
- **Data Sharing**: Secure data exchange between organizations
- **Machine Learning**: Feature engineering and model training with Snowpark
- **Multi-cloud Strategy**: Consistent experience across AWS, Azure, GCP

**Not Ideal For:**
- **OLTP Workloads**: High-frequency transactional systems
- **Real-time Streaming**: Sub-second latency requirements
- **Small Datasets**: Cost may not justify benefits for small data volumes
- **Complex ETL**: Heavy transformation workloads (better suited for Spark/Databricks)

## 🎯 Interview Focus Areas

1. **Architecture**: Multi-cluster, shared data architecture
2. **Virtual Warehouses**: Sizing, scaling, and cost optimization
3. **Data Loading**: COPY, Snowpipe, and external tables
4. **Performance**: Clustering, caching, and query optimization
5. **Security**: RBAC, row-level security, and data masking
6. **Time Travel**: Data recovery and historical analysis
7. **Streams & Tasks**: Change data capture and automation
8. **Cost Management**: Credit usage and optimization strategies
9. **Data Sharing**: Secure sharing and marketplace
10. **Integration**: Connectors and external functions

## 📚 Quick References

- [Snowflake Documentation](https://docs.snowflake.com/)
- [SQL Reference](https://docs.snowflake.com/en/sql-reference)
- [Snowpark Developer Guide](https://docs.snowflake.com/en/developer-guide/snowpark/index)
- [Data Loading Guide](https://docs.snowflake.com/en/user-guide/data-load-overview)
- [Security Guide](https://docs.snowflake.com/en/user-guide/security)
- [Cost Optimization](https://docs.snowflake.com/en/user-guide/cost-understanding)