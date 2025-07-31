# Snowflake Best Practices for Data Engineering

## Warehouse Management

### Warehouse Sizing
```sql
-- Create appropriately sized warehouses
CREATE WAREHOUSE ETL_WH WITH
  WAREHOUSE_SIZE = 'LARGE'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE;

-- Separate warehouses by workload
CREATE WAREHOUSE ANALYTICS_WH WITH WAREHOUSE_SIZE = 'MEDIUM';
CREATE WAREHOUSE LOADING_WH WITH WAREHOUSE_SIZE = 'X-LARGE';

-- Multi-cluster for concurrency
CREATE WAREHOUSE REPORTING_WH WITH
  WAREHOUSE_SIZE = 'LARGE'
  MIN_CLUSTER_COUNT = 1
  MAX_CLUSTER_COUNT = 5
  SCALING_POLICY = 'STANDARD';
```

### Resource Monitoring
```sql
-- Monitor warehouse usage
SELECT 
  warehouse_name,
  SUM(credits_used) as total_credits,
  AVG(avg_running) as avg_concurrent_queries
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE start_time >= DATEADD(day, -7, CURRENT_TIMESTAMP())
GROUP BY warehouse_name
ORDER BY total_credits DESC;

-- Query performance analysis
SELECT 
  query_id,
  query_text,
  warehouse_name,
  execution_time,
  compilation_time,
  bytes_scanned
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE start_time >= DATEADD(hour, -24, CURRENT_TIMESTAMP())
ORDER BY execution_time DESC
LIMIT 10;
```

## Table Design and Optimization

### Clustering Keys
```sql
-- Define clustering keys for large tables
ALTER TABLE sales_fact CLUSTER BY (sale_date, region_id);

-- Multi-column clustering
ALTER TABLE customer_transactions 
CLUSTER BY (customer_id, transaction_date);

-- Monitor clustering effectiveness
SELECT 
  table_name,
  clustering_key,
  total_partition_count,
  average_overlaps,
  average_depth
FROM SNOWFLAKE.ACCOUNT_USAGE.AUTOMATIC_CLUSTERING_HISTORY
WHERE start_time >= DATEADD(day, -7, CURRENT_TIMESTAMP());
```

### Data Types and Compression
```sql
-- Use appropriate data types
CREATE TABLE optimized_table (
  id NUMBER(38,0),                    -- Use NUMBER for integers
  amount NUMBER(10,2),                -- Specify precision for decimals
  status VARCHAR(20),                 -- Size VARCHAR appropriately
  created_date TIMESTAMP_NTZ,         -- Use TIMESTAMP_NTZ for UTC dates
  metadata VARIANT                    -- Use VARIANT for JSON data
);

-- Enable automatic clustering
ALTER TABLE large_table RESUME RECLUSTER;
```

## Data Loading Best Practices

### Bulk Loading with COPY
```sql
-- Efficient bulk loading
COPY INTO customer_data
FROM @my_stage/customer_files/
FILE_FORMAT = (TYPE = 'CSV' FIELD_DELIMITER = ',' SKIP_HEADER = 1)
ON_ERROR = 'SKIP_FILE'
PURGE = TRUE;

-- Parallel loading with pattern matching
COPY INTO sales_data
FROM @my_stage/sales/
PATTERN = '.*sales_[0-9]{4}_[0-9]{2}_[0-9]{2}\.csv'
FILE_FORMAT = my_csv_format;
```

### Streaming with Snowpipe
```sql
-- Create Snowpipe for continuous loading
CREATE PIPE customer_pipe AS
COPY INTO customer_data
FROM @my_stage/streaming/
FILE_FORMAT = (TYPE = 'JSON');

-- Monitor Snowpipe status
SELECT 
  pipe_name,
  files_in_ingestion_queue,
  avg_file_load_time,
  last_received_message_timestamp
FROM SNOWFLAKE.ACCOUNT_USAGE.PIPE_USAGE_HISTORY
WHERE pipe_name = 'CUSTOMER_PIPE';
```

## Query Optimization

### Efficient Joins
```sql
-- Use appropriate join types
SELECT c.customer_name, SUM(o.amount)
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE c.status = 'ACTIVE'
GROUP BY c.customer_id, c.customer_name;

-- Optimize large table joins with clustering
SELECT /*+ USE_CACHED_RESULT(FALSE) */ 
  f.*, d.dimension_name
FROM fact_table f
JOIN dimension_table d ON f.dimension_key = d.dimension_key
WHERE f.date_key BETWEEN 20230101 AND 20231231;
```

### Window Functions
```sql
-- Efficient window function usage
SELECT 
  customer_id,
  order_date,
  amount,
  SUM(amount) OVER (
    PARTITION BY customer_id 
    ORDER BY order_date 
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) as running_total
FROM orders
QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) <= 10;
```

## Security and Governance

### Role-Based Access Control
```sql
-- Create hierarchical roles
CREATE ROLE DATA_ENGINEER;
CREATE ROLE DATA_ANALYST;
CREATE ROLE DATA_SCIENTIST;

-- Grant privileges
GRANT USAGE ON WAREHOUSE ETL_WH TO ROLE DATA_ENGINEER;
GRANT SELECT ON ALL TABLES IN SCHEMA RAW_DATA TO ROLE DATA_ANALYST;

-- Create secure views
CREATE SECURE VIEW customer_summary AS
SELECT 
  customer_id,
  CASE WHEN CURRENT_ROLE() = 'ADMIN' 
       THEN email 
       ELSE 'REDACTED' 
  END as email,
  total_orders
FROM customers;
```

### Data Masking
```sql
-- Dynamic data masking
CREATE MASKING POLICY email_mask AS (val string) RETURNS string ->
  CASE 
    WHEN CURRENT_ROLE() IN ('ADMIN', 'DATA_ENGINEER') THEN val
    ELSE REGEXP_REPLACE(val, '.+@', '*****@')
  END;

-- Apply masking policy
ALTER TABLE customers MODIFY COLUMN email 
SET MASKING POLICY email_mask;
```