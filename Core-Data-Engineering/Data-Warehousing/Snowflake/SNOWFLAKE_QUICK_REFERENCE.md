# Snowflake Quick Reference for Data Engineering

## Account and Database Management

### Account Setup
```sql
-- Show current account information
SELECT CURRENT_ACCOUNT();
SELECT CURRENT_REGION();
SELECT CURRENT_VERSION();

-- Account usage views
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.DATABASES;
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSES;
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.USERS;
```

### Database Operations
```sql
-- Create database
CREATE DATABASE production;
CREATE DATABASE development CLONE production;  -- Zero-copy clone

-- Use database
USE DATABASE production;

-- Show databases
SHOW DATABASES;

-- Drop database
DROP DATABASE IF EXISTS old_database;

-- Database properties
ALTER DATABASE production SET DATA_RETENTION_TIME_IN_DAYS = 7;
```

### Schema Management
```sql
-- Create schema
CREATE SCHEMA production.sales;
CREATE TRANSIENT SCHEMA temp_data;  -- No fail-safe, lower cost

-- Use schema
USE SCHEMA production.sales;

-- Show schemas
SHOW SCHEMAS IN DATABASE production;

-- Grant permissions
GRANT USAGE ON SCHEMA production.sales TO ROLE analyst;
```

## Virtual Warehouses

### Warehouse Creation and Management
```sql
-- Create warehouse
CREATE WAREHOUSE analytics_wh WITH
    WAREHOUSE_SIZE = 'MEDIUM'
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 3
    SCALING_POLICY = 'STANDARD'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE
    COMMENT = 'Analytics workload warehouse';

-- Resize warehouse
ALTER WAREHOUSE analytics_wh SET WAREHOUSE_SIZE = 'LARGE';

-- Suspend/Resume warehouse
ALTER WAREHOUSE analytics_wh SUSPEND;
ALTER WAREHOUSE analytics_wh RESUME;

-- Use warehouse
USE WAREHOUSE analytics_wh;

-- Show warehouses
SHOW WAREHOUSES;

-- Monitor warehouse usage
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE WAREHOUSE_NAME = 'ANALYTICS_WH'
ORDER BY START_TIME DESC;
```

### Warehouse Sizing
```sql
-- Warehouse sizes and credits per hour
-- X-Small: 1 credit/hour
-- Small: 2 credits/hour  
-- Medium: 4 credits/hour
-- Large: 8 credits/hour
-- X-Large: 16 credits/hour
-- 2X-Large: 32 credits/hour
-- 3X-Large: 64 credits/hour
-- 4X-Large: 128 credits/hour
```

## Table Operations

### Table Creation
```sql
-- Standard table
CREATE TABLE customers (
    customer_id NUMBER(10,0) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    created_date DATE DEFAULT CURRENT_DATE(),
    updated_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Transient table (no fail-safe)
CREATE TRANSIENT TABLE temp_data (
    id NUMBER,
    data VARIANT
);

-- Temporary table (session-scoped)
CREATE TEMPORARY TABLE session_temp (
    temp_id NUMBER,
    temp_value STRING
);

-- External table
CREATE EXTERNAL TABLE external_sales (
    order_id NUMBER AS (value:c1::NUMBER),
    customer_id NUMBER AS (value:c2::NUMBER),
    amount DECIMAL(10,2) AS (value:c3::DECIMAL(10,2))
)
WITH LOCATION = @my_stage
FILE_FORMAT = (TYPE = 'CSV');
```

### Table Modifications
```sql
-- Add column
ALTER TABLE customers ADD COLUMN middle_name VARCHAR(50);

-- Drop column
ALTER TABLE customers DROP COLUMN middle_name;

-- Rename column
ALTER TABLE customers RENAME COLUMN phone TO phone_number;

-- Modify column
ALTER TABLE customers ALTER COLUMN email SET NOT NULL;

-- Add constraint
ALTER TABLE customers ADD CONSTRAINT chk_email CHECK (email LIKE '%@%');

-- Clustering
ALTER TABLE large_table CLUSTER BY (date_column, category);
```

## Data Loading

### File Formats
```sql
-- CSV format
CREATE FILE FORMAT csv_format
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    NULL_IF = ('NULL', 'null', '')
    EMPTY_FIELD_AS_NULL = TRUE
    FIELD_OPTIONALLY_ENCLOSED_BY = '"';

-- JSON format
CREATE FILE FORMAT json_format
    TYPE = 'JSON'
    STRIP_OUTER_ARRAY = TRUE;

-- Parquet format
CREATE FILE FORMAT parquet_format
    TYPE = 'PARQUET';
```

### Stages
```sql
-- Internal stage
CREATE STAGE my_internal_stage;

-- External stage (S3)
CREATE STAGE my_s3_stage
    URL = 's3://my-bucket/data/'
    CREDENTIALS = (AWS_KEY_ID = 'xxx' AWS_SECRET_KEY = 'yyy')
    FILE_FORMAT = csv_format;

-- External stage (Azure)
CREATE STAGE my_azure_stage
    URL = 'azure://myaccount.blob.core.windows.net/mycontainer/data/'
    CREDENTIALS = (AZURE_SAS_TOKEN = 'xxx')
    FILE_FORMAT = csv_format;

-- List files in stage
LIST @my_s3_stage;

-- Upload to internal stage
PUT file:///path/to/local/file.csv @my_internal_stage;
```

### COPY Command
```sql
-- Basic copy
COPY INTO customers
FROM @my_s3_stage/customers.csv
FILE_FORMAT = csv_format;

-- Copy with options
COPY INTO customers
FROM @my_s3_stage
PATTERN = '.*customers.*\.csv'
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE'
PURGE = TRUE
FORCE = TRUE;

-- Copy with transformation
COPY INTO customers (customer_id, full_name, email)
FROM (
    SELECT 
        $1,
        CONCAT($2, ' ', $3),
        LOWER($4)
    FROM @my_s3_stage/customers.csv
)
FILE_FORMAT = csv_format;

-- Monitor copy history
SELECT * FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => 'CUSTOMERS',
    START_TIME => DATEADD(HOUR, -1, CURRENT_TIMESTAMP())
));
```

### Snowpipe (Continuous Loading)
```sql
-- Create pipe
CREATE PIPE customer_pipe AS
COPY INTO customers
FROM @my_s3_stage
FILE_FORMAT = csv_format;

-- Show pipe status
SELECT SYSTEM$PIPE_STATUS('customer_pipe');

-- Refresh pipe
SELECT SYSTEM$PIPE_FORCE_RESUME('customer_pipe');

-- Monitor pipe
SELECT * FROM TABLE(INFORMATION_SCHEMA.PIPE_USAGE_HISTORY(
    DATE_RANGE_START => DATEADD(DAY, -1, CURRENT_DATE())
));
```

## Querying Data

### Basic Queries
```sql
-- Select with conditions
SELECT customer_id, first_name, last_name
FROM customers
WHERE created_date >= '2024-01-01'
ORDER BY last_name
LIMIT 100;

-- Joins
SELECT 
    c.customer_id,
    c.first_name,
    o.order_date,
    o.amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= CURRENT_DATE - 30;

-- Window functions
SELECT 
    customer_id,
    order_date,
    amount,
    SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date) as running_total,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) as order_rank
FROM orders;
```

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
    f.value:product_name::STRING as product_name,
    f.value:price::NUMBER as price
FROM json_table,
LATERAL FLATTEN(input => json_data:products) f;

-- Parse JSON
SELECT PARSE_JSON('{"name": "John", "age": 30}') as parsed_json;

-- Extract from VARIANT
SELECT 
    GET(json_column, 'key') as value,
    GET_PATH(json_column, 'nested.key') as nested_value
FROM table_with_json;
```

## Time Travel and Cloning

### Time Travel
```sql
-- Query at specific timestamp
SELECT * FROM customers AT (TIMESTAMP => '2024-01-01 10:00:00');

-- Query at offset (seconds ago)
SELECT * FROM customers AT (OFFSET => -3600);

-- Query before statement
SELECT * FROM customers BEFORE (STATEMENT => '01a1b2c3-0000-0000-0000-000000000000');

-- Show changes
SELECT * FROM customers CHANGES(INFORMATION => DEFAULT)
AT (TIMESTAMP => '2024-01-01 10:00:00');
```

### Cloning
```sql
-- Clone table
CREATE TABLE customers_backup CLONE customers;

-- Clone at specific time
CREATE TABLE customers_jan1 CLONE customers AT (TIMESTAMP => '2024-01-01 00:00:00');

-- Clone database
CREATE DATABASE prod_backup CLONE production;

-- Clone schema
CREATE SCHEMA sales_backup CLONE production.sales;
```

### Undrop
```sql
-- Undrop table
UNDROP TABLE customers;

-- Undrop database
UNDROP DATABASE production;

-- Show dropped objects
SHOW TABLES HISTORY;
```

## Streams and Tasks

### Streams
```sql
-- Create stream on table
CREATE STREAM customer_stream ON TABLE customers;

-- Create stream on view
CREATE STREAM customer_view_stream ON VIEW customer_summary;

-- Query stream
SELECT * FROM customer_stream;

-- Check if stream has data
SELECT SYSTEM$STREAM_HAS_DATA('customer_stream');

-- Show streams
SHOW STREAMS;
```

### Tasks
```sql
-- Create simple task
CREATE TASK daily_summary
    WAREHOUSE = 'ETL_WH'
    SCHEDULE = 'USING CRON 0 2 * * * UTC'
AS
    INSERT INTO daily_summary
    SELECT DATE(order_date), COUNT(*), SUM(amount)
    FROM orders
    WHERE DATE(order_date) = CURRENT_DATE - 1
    GROUP BY DATE(order_date);

-- Create task with condition
CREATE TASK process_changes
    WAREHOUSE = 'ETL_WH'
    SCHEDULE = '5 MINUTE'
    WHEN SYSTEM$STREAM_HAS_DATA('customer_stream')
AS
    MERGE INTO customer_summary cs
    USING customer_stream s ON cs.customer_id = s.customer_id
    WHEN MATCHED THEN UPDATE SET last_updated = CURRENT_TIMESTAMP()
    WHEN NOT MATCHED THEN INSERT VALUES (s.customer_id, CURRENT_TIMESTAMP());

-- Task dependencies
CREATE TASK child_task
    WAREHOUSE = 'ETL_WH'
    AFTER parent_task
AS
    SELECT 'Child task executed';

-- Resume/Suspend tasks
ALTER TASK daily_summary RESUME;
ALTER TASK daily_summary SUSPEND;

-- Show tasks
SHOW TASKS;

-- Task history
SELECT * FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY())
WHERE NAME = 'DAILY_SUMMARY'
ORDER BY SCHEDULED_TIME DESC;
```

## Security and Access Control

### Roles and Users
```sql
-- Create role
CREATE ROLE data_engineer;
CREATE ROLE data_analyst;

-- Create user
CREATE USER john_doe 
    PASSWORD = 'SecurePassword123'
    DEFAULT_ROLE = data_analyst
    DEFAULT_WAREHOUSE = analytics_wh;

-- Grant role to user
GRANT ROLE data_analyst TO USER john_doe;

-- Grant role to role (role hierarchy)
GRANT ROLE data_analyst TO ROLE data_engineer;

-- Switch role
USE ROLE data_engineer;

-- Show current role
SELECT CURRENT_ROLE();
```

### Privileges
```sql
-- Database privileges
GRANT USAGE ON DATABASE production TO ROLE data_analyst;
GRANT CREATE SCHEMA ON DATABASE production TO ROLE data_engineer;

-- Schema privileges
GRANT USAGE ON SCHEMA production.sales TO ROLE data_analyst;
GRANT CREATE TABLE ON SCHEMA production.sales TO ROLE data_engineer;

-- Table privileges
GRANT SELECT ON TABLE customers TO ROLE data_analyst;
GRANT INSERT, UPDATE, DELETE ON TABLE customers TO ROLE data_engineer;

-- Warehouse privileges
GRANT USAGE ON WAREHOUSE analytics_wh TO ROLE data_analyst;
GRANT MODIFY ON WAREHOUSE analytics_wh TO ROLE data_engineer;

-- Show grants
SHOW GRANTS TO ROLE data_analyst;
SHOW GRANTS ON TABLE customers;
```

### Row-Level Security
```sql
-- Create row access policy
CREATE ROW ACCESS POLICY region_policy AS (region_column STRING) RETURNS BOOLEAN ->
    CURRENT_ROLE() = 'ADMIN' OR 
    (CURRENT_ROLE() = 'US_ANALYST' AND region_column = 'US') OR
    (CURRENT_ROLE() = 'EU_ANALYST' AND region_column = 'EU');

-- Apply policy to table
ALTER TABLE sales ADD ROW ACCESS POLICY region_policy ON (region);

-- Remove policy
ALTER TABLE sales DROP ROW ACCESS POLICY region_policy;
```

### Column-Level Security
```sql
-- Create masking policy
CREATE MASKING POLICY email_mask AS (val STRING) RETURNS STRING ->
    CASE 
        WHEN CURRENT_ROLE() IN ('ADMIN', 'DATA_ENGINEER') THEN val
        ELSE REGEXP_REPLACE(val, '.+@', '*****@')
    END;

-- Apply masking policy
ALTER TABLE customers MODIFY COLUMN email SET MASKING POLICY email_mask;

-- Remove masking policy
ALTER TABLE customers MODIFY COLUMN email UNSET MASKING POLICY;
```

## Data Sharing

### Creating Shares
```sql
-- Create share
CREATE SHARE sales_data_share;

-- Grant database to share
GRANT USAGE ON DATABASE production TO SHARE sales_data_share;
GRANT USAGE ON SCHEMA production.sales TO SHARE sales_data_share;

-- Grant tables to share
GRANT SELECT ON TABLE production.sales.orders TO SHARE sales_data_share;
GRANT SELECT ON TABLE production.sales.customers TO SHARE sales_data_share;

-- Add accounts to share
ALTER SHARE sales_data_share ADD ACCOUNTS = account1, account2;

-- Show shares
SHOW SHARES;
```

### Consuming Shares
```sql
-- Show available shares
SHOW SHARES IN ACCOUNT;

-- Create database from share
CREATE DATABASE shared_sales_data FROM SHARE provider_account.sales_data_share;

-- Query shared data
SELECT * FROM shared_sales_data.sales.orders;
```

## Monitoring and Optimization

### Query Performance
```sql
-- Query history
SELECT 
    query_id,
    query_text,
    user_name,
    warehouse_name,
    start_time,
    end_time,
    total_elapsed_time,
    bytes_scanned,
    credits_used_cloud_services
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE start_time >= DATEADD(DAY, -1, CURRENT_TIMESTAMP())
ORDER BY total_elapsed_time DESC
LIMIT 10;

-- Explain query plan
EXPLAIN SELECT * FROM large_table WHERE date_col >= '2024-01-01';

-- Query profile (use Snowflake UI)
-- Get query ID from query history, then view in UI
```

### Storage Usage
```sql
-- Database storage
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.DATABASE_STORAGE_USAGE_HISTORY
ORDER BY USAGE_DATE DESC;

-- Table storage
SELECT 
    table_name,
    active_bytes / (1024*1024*1024) as active_gb,
    time_travel_bytes / (1024*1024*1024) as time_travel_gb,
    failsafe_bytes / (1024*1024*1024) as failsafe_gb
FROM SNOWFLAKE.ACCOUNT_USAGE.TABLE_STORAGE_METRICS
WHERE table_schema = 'SALES'
ORDER BY active_bytes DESC;
```

### Credit Usage
```sql
-- Warehouse credit usage
SELECT 
    warehouse_name,
    DATE(start_time) as usage_date,
    SUM(credits_used) as daily_credits
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE start_time >= DATEADD(DAY, -30, CURRENT_TIMESTAMP())
GROUP BY warehouse_name, DATE(start_time)
ORDER BY daily_credits DESC;

-- Overall credit usage
SELECT 
    DATE(start_time) as usage_date,
    service_type,
    SUM(credits_used) as credits
FROM SNOWFLAKE.ACCOUNT_USAGE.METERING_HISTORY
WHERE start_time >= DATEADD(DAY, -7, CURRENT_TIMESTAMP())
GROUP BY DATE(start_time), service_type
ORDER BY usage_date DESC, credits DESC;
```

## Stored Procedures and UDFs

### Stored Procedures
```sql
-- JavaScript stored procedure
CREATE OR REPLACE PROCEDURE get_customer_summary(customer_id NUMBER)
RETURNS STRING
LANGUAGE JAVASCRIPT
AS
$$
    var sql_command = "SELECT COUNT(*) as order_count FROM orders WHERE customer_id = " + CUSTOMER_ID;
    var statement = snowflake.createStatement({sqlText: sql_command});
    var result_set = statement.execute();
    result_set.next();
    return "Customer has " + result_set.getColumnValue(1) + " orders";
$$;

-- SQL stored procedure
CREATE OR REPLACE PROCEDURE update_customer_stats()
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    row_count NUMBER;
BEGIN
    UPDATE customer_summary 
    SET last_order_date = (
        SELECT MAX(order_date) 
        FROM orders 
        WHERE orders.customer_id = customer_summary.customer_id
    );
    
    SELECT COUNT(*) INTO row_count FROM customer_summary;
    RETURN 'Updated ' || row_count || ' customer records';
END;
$$;

-- Call procedure
CALL get_customer_summary(123);
CALL update_customer_stats();
```

### User-Defined Functions
```sql
-- SQL UDF
CREATE OR REPLACE FUNCTION calculate_tax(amount DECIMAL(10,2), rate DECIMAL(5,4))
RETURNS DECIMAL(10,2)
AS
$$
    amount * rate
$$;

-- JavaScript UDF
CREATE OR REPLACE FUNCTION format_phone(phone STRING)
RETURNS STRING
LANGUAGE JAVASCRIPT
AS
$$
    if (PHONE && PHONE.length === 10) {
        return PHONE.substring(0,3) + '-' + PHONE.substring(3,6) + '-' + PHONE.substring(6,10);
    }
    return PHONE;
$$;

-- Use UDF
SELECT 
    customer_id,
    format_phone(phone) as formatted_phone,
    calculate_tax(order_amount, 0.0825) as tax_amount
FROM customers;
```

## Common Patterns

### Merge (Upsert)
```sql
MERGE INTO target_table t
USING source_table s ON t.id = s.id
WHEN MATCHED THEN
    UPDATE SET 
        t.name = s.name,
        t.updated_date = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN
    INSERT (id, name, created_date)
    VALUES (s.id, s.name, CURRENT_TIMESTAMP());
```

### Pivot/Unpivot
```sql
-- Pivot
SELECT *
FROM (
    SELECT customer_id, product_category, sales_amount
    FROM sales_data
) PIVOT (
    SUM(sales_amount)
    FOR product_category IN ('Electronics', 'Clothing', 'Books')
);

-- Unpivot
SELECT *
FROM monthly_sales UNPIVOT (
    sales_amount FOR month IN (jan, feb, mar, apr)
);
```

### Common Table Expressions
```sql
WITH customer_totals AS (
    SELECT 
        customer_id,
        SUM(amount) as total_spent,
        COUNT(*) as order_count
    FROM orders
    GROUP BY customer_id
),
high_value_customers AS (
    SELECT customer_id
    FROM customer_totals
    WHERE total_spent > 10000
)
SELECT 
    c.customer_name,
    ct.total_spent,
    ct.order_count
FROM customers c
JOIN customer_totals ct ON c.customer_id = ct.customer_id
JOIN high_value_customers hvc ON c.customer_id = hvc.customer_id;
```