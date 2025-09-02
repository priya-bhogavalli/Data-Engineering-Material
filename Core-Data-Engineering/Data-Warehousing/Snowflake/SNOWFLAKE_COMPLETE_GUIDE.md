# Snowflake Complete Guide for Data Engineering

## 🎯 What is Snowflake?

Snowflake is a **cloud-native data warehouse** built from the ground up for the cloud. Think of it as a modern, intelligent storage and computing system that can instantly scale to handle any amount of data while keeping your costs under control.

### Key Characteristics
- **Cloud-Native**: Built specifically for cloud environments
- **Elastic Scaling**: Instantly scale compute up or down
- **Zero Management**: No infrastructure to maintain
- **Multi-Cloud**: Runs on AWS, Azure, and Google Cloud
- **Concurrent Workloads**: Multiple teams can work simultaneously without interference

## 🏗️ Architecture Overview

### Three-Layer Architecture
```
┌─────────────────────────────────────────────────────────┐
│                    Services Layer                        │
│  (Authentication, Metadata, Query Optimization)         │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                   Compute Layer                         │
│        (Virtual Warehouses - Elastic Compute)          │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                   Storage Layer                         │
│           (Compressed, Columnar Storage)                │
└─────────────────────────────────────────────────────────┘
```

**Services Layer**: Authentication, metadata management, query optimization
**Compute Layer**: Independent virtual warehouses for processing
**Storage Layer**: Automatically managed, compressed data storage

## 💾 Core Concepts

### 1. Virtual Warehouses
Virtual warehouses are compute clusters that execute your queries. Think of them as powerful, on-demand computers.

```sql
-- Create warehouse
CREATE WAREHOUSE analytics_wh WITH
    WAREHOUSE_SIZE = 'MEDIUM'
    AUTO_SUSPEND = 300              -- Suspend after 5 minutes
    AUTO_RESUME = TRUE              -- Auto-resume on query
    INITIALLY_SUSPENDED = TRUE;

-- Warehouse sizes: X-SMALL, SMALL, MEDIUM, LARGE, X-LARGE, 2X-LARGE, 3X-LARGE, 4X-LARGE
-- Credits per hour: 1, 2, 4, 8, 16, 32, 64, 128

-- Multi-cluster for concurrency
CREATE WAREHOUSE etl_wh WITH
    WAREHOUSE_SIZE = 'LARGE'
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 5
    SCALING_POLICY = 'STANDARD';

-- Resize warehouse dynamically
ALTER WAREHOUSE analytics_wh SET WAREHOUSE_SIZE = 'LARGE';

-- Monitor warehouse usage
SELECT 
    warehouse_name,
    start_time,
    credits_used,
    credits_used_compute
FROM snowflake.account_usage.warehouse_metering_history
WHERE start_time >= DATEADD('day', -7, CURRENT_TIMESTAMP())
ORDER BY start_time DESC;
```

### 2. Database Objects
```sql
-- Three-level namespace: DATABASE.SCHEMA.OBJECT
CREATE DATABASE analytics_db;
CREATE SCHEMA analytics_db.sales;
CREATE SCHEMA analytics_db.marketing;

-- Table types
CREATE TABLE customers (                    -- Permanent table
    customer_id NUMBER(10,0) PRIMARY KEY,
    first_name VARCHAR(50),
    email VARCHAR(100),
    created_date DATE DEFAULT CURRENT_DATE()
);

CREATE TRANSIENT TABLE staging_data (      -- No fail-safe, lower cost
    id NUMBER,
    data VARIANT
);

CREATE TEMPORARY TABLE session_temp (      -- Session-scoped
    temp_id NUMBER,
    temp_value STRING
);
```

### 3. Data Loading
```sql
-- File formats
CREATE FILE FORMAT csv_format
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    NULL_IF = ('NULL', 'null', '')
    FIELD_OPTIONALLY_ENCLOSED_BY = '"';

-- Stages
CREATE STAGE s3_stage
    URL = 's3://my-bucket/data/'
    CREDENTIALS = (AWS_KEY_ID = 'xxx' AWS_SECRET_KEY = 'yyy')
    FILE_FORMAT = csv_format;

-- COPY command
COPY INTO customers
FROM @s3_stage/customers.csv
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE';

-- Snowpipe for continuous loading
CREATE PIPE customer_pipe AS
COPY INTO customers
FROM @s3_stage/customers/
FILE_FORMAT = csv_format;
```

### 4. Time Travel & Cloning
```sql
-- Time Travel (access historical data)
SELECT * FROM customers AT (TIMESTAMP => '2024-01-01 10:00:00');
SELECT * FROM customers AT (OFFSET => -3600);  -- 1 hour ago

-- Zero-copy cloning
CREATE TABLE customers_backup CLONE customers;
CREATE DATABASE dev_db CLONE prod_db;

-- Undrop objects
UNDROP TABLE customers;
SHOW TABLES HISTORY;
```

### 5. Streams & Tasks
```sql
-- Streams for change data capture
CREATE STREAM customer_stream ON TABLE customers;

-- Query stream data
SELECT 
    customer_id,
    first_name,
    METADATA$ACTION,        -- INSERT, UPDATE, DELETE
    METADATA$ISUPDATE       -- TRUE for UPDATE
FROM customer_stream;

-- Tasks for scheduling
CREATE TASK daily_summary
    WAREHOUSE = 'ETL_WH'
    SCHEDULE = 'USING CRON 0 2 * * * UTC'  -- Daily at 2 AM
AS
    INSERT INTO daily_summary
    SELECT DATE(created_date), COUNT(*)
    FROM customers
    WHERE DATE(created_date) = CURRENT_DATE - 1
    GROUP BY DATE(created_date);

-- Enable task
ALTER TASK daily_summary RESUME;
```

## 🔒 Security & Access Control

### Role-Based Access Control
```sql
-- Create roles
CREATE ROLE data_engineer;
CREATE ROLE data_analyst;

-- Grant privileges
GRANT USAGE ON DATABASE analytics_db TO ROLE data_analyst;
GRANT SELECT ON ALL TABLES IN SCHEMA analytics_db.sales TO ROLE data_analyst;

-- Grant roles to users
GRANT ROLE data_analyst TO USER john_doe;

-- Row-level security
CREATE ROW ACCESS POLICY region_policy AS (region STRING) RETURNS BOOLEAN ->
    CURRENT_ROLE() = 'ADMIN' OR 
    (CURRENT_ROLE() = 'US_ANALYST' AND region = 'US');

ALTER TABLE sales ADD ROW ACCESS POLICY region_policy ON (region);

-- Column masking
CREATE MASKING POLICY email_mask AS (val STRING) RETURNS STRING ->
    CASE 
        WHEN CURRENT_ROLE() IN ('ADMIN', 'DATA_ENGINEER') THEN val
        ELSE REGEXP_REPLACE(val, '.+@', '*****@')
    END;

ALTER TABLE customers MODIFY COLUMN email SET MASKING POLICY email_mask;
```

## ⚡ Performance Optimization

### 1. Clustering
```sql
-- Add clustering key for large tables
ALTER TABLE large_sales_table CLUSTER BY (sale_date, region);

-- Monitor clustering
SELECT SYSTEM$CLUSTERING_DEPTH('large_sales_table', '(sale_date, region)');

-- Automatic clustering
ALTER TABLE large_sales_table RESUME RECLUSTER;
```

### 2. Query Optimization
```sql
-- Use appropriate data types
CREATE TABLE optimized_table (
    id NUMBER(10,0),                    -- Specify precision
    amount NUMBER(10,2),                -- Specify scale
    status VARCHAR(20),                 -- Size appropriately
    created_date DATE,                  -- Use DATE vs TIMESTAMP when possible
    metadata VARIANT                    -- For JSON data
);

-- Efficient queries
SELECT customer_id, SUM(amount)
FROM orders 
WHERE order_date >= '2024-01-01'      -- Use partition pruning
  AND status = 'COMPLETED'
GROUP BY customer_id
LIMIT 1000;                           -- Use LIMIT for large results

-- Window functions with QUALIFY
SELECT 
    customer_id,
    order_date,
    amount,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) as rn
FROM orders
QUALIFY rn <= 5;  -- Get top 5 orders per customer
```

### 3. Result Caching
```sql
-- Automatic result caching (24 hours)
-- Identical queries return cached results instantly
SELECT region, SUM(sales) FROM orders GROUP BY region;  -- First run: scans data
SELECT region, SUM(sales) FROM orders GROUP BY region;  -- Second run: cached result
```

## 🌐 Data Sharing

### Secure Data Sharing
```sql
-- Create share
CREATE SHARE customer_share;

-- Grant objects to share
GRANT USAGE ON DATABASE analytics_db TO SHARE customer_share;
GRANT SELECT ON TABLE analytics_db.sales.customers TO SHARE customer_share;

-- Add accounts to share
ALTER SHARE customer_share ADD ACCOUNTS = ('partner_account_123');

-- Consumer side: create database from share
CREATE DATABASE shared_data FROM SHARE provider_account.customer_share;
```

## 🔧 Advanced Features

### Semi-Structured Data
```sql
-- Query JSON data
SELECT 
    id,
    json_data:name::STRING as name,
    json_data:age::NUMBER as age,
    json_data:address.city::STRING as city
FROM json_table;

-- Flatten arrays
SELECT 
    id,
    f.value:product_name::STRING as product_name
FROM json_table,
LATERAL FLATTEN(input => json_data:products) f;
```

### Stored Procedures & UDFs
```sql
-- JavaScript stored procedure
CREATE OR REPLACE PROCEDURE process_data()
RETURNS STRING
LANGUAGE JAVASCRIPT
AS
$$
    var sql_command = "INSERT INTO summary SELECT customer_id, COUNT(*) FROM orders GROUP BY customer_id";
    var statement = snowflake.createStatement({sqlText: sql_command});
    var result = statement.execute();
    return "Processing completed";
$$;

-- SQL UDF
CREATE OR REPLACE FUNCTION calculate_tax(amount DECIMAL(10,2), rate DECIMAL(5,4))
RETURNS DECIMAL(10,2)
AS
$$
    amount * rate
$$;
```

## 💰 Cost Optimization Best Practices

### 1. Warehouse Management
- Use auto-suspend (1-5 minutes) and auto-resume
- Right-size warehouses based on workload
- Use separate warehouses for different workloads
- Monitor credit usage regularly

### 2. Storage Optimization
- Use transient tables for temporary data
- Implement proper data retention policies
- Leverage clustering for large tables
- Use appropriate data types

### 3. Query Optimization
- Use result caching effectively
- Implement proper WHERE clauses for partition pruning
- Avoid SELECT * queries
- Use LIMIT for large result sets

## 🚨 Monitoring & Troubleshooting

### Key Monitoring Queries
```sql
-- Query performance
SELECT 
    query_id,
    query_text,
    execution_time,
    warehouse_name,
    bytes_scanned
FROM snowflake.account_usage.query_history
WHERE start_time >= DATEADD(hour, -24, CURRENT_TIMESTAMP())
ORDER BY execution_time DESC
LIMIT 10;

-- Storage usage
SELECT 
    table_name,
    active_bytes / (1024*1024*1024) as active_gb,
    time_travel_bytes / (1024*1024*1024) as time_travel_gb
FROM snowflake.account_usage.table_storage_metrics
ORDER BY active_bytes DESC;

-- Credit usage
SELECT 
    warehouse_name,
    DATE(start_time) as usage_date,
    SUM(credits_used) as daily_credits
FROM snowflake.account_usage.warehouse_metering_history
WHERE start_time >= DATEADD(day, -7, CURRENT_TIMESTAMP())
GROUP BY warehouse_name, DATE(start_time)
ORDER BY daily_credits DESC;
```

## 🎯 When to Use Snowflake

### ✅ Ideal Use Cases
- **Data Warehousing**: Central repository for analytical data
- **Multi-Team Analytics**: Different teams with varying compute needs
- **Variable Workloads**: Seasonal patterns, ad-hoc requests
- **Data Lake Modernization**: Replace complex Hadoop ecosystems
- **Cross-Cloud Strategy**: Multi-cloud data platform

### ❌ Not Ideal For
- **OLTP Systems**: Use operational databases instead
- **Real-time Processing**: Use streaming platforms
- **Small Data**: May be overkill for simple use cases
- **Cost-Sensitive Small Workloads**: Consider alternatives

## 🚀 Getting Started Checklist

1. **Setup Account**: Choose cloud provider and region
2. **Create Warehouses**: Start with SMALL, enable auto-suspend
3. **Design Schema**: Plan database and schema structure
4. **Load Data**: Use COPY command or Snowpipe
5. **Implement Security**: Set up roles and access control
6. **Monitor Usage**: Set up resource monitors and alerts
7. **Optimize Performance**: Add clustering keys for large tables
8. **Enable Sharing**: Set up data sharing if needed

This guide provides the foundation for working with Snowflake effectively. Focus on understanding the separation of compute and storage, proper warehouse management, and security best practices for successful implementation.