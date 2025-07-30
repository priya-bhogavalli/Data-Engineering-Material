# Snowflake Key Concepts

## 1. Snowflake Architecture
**What is Snowflake**: A cloud-native data warehouse built for the cloud with a unique multi-cluster, shared data architecture.

**Three-Layer Architecture**:
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

**Key Benefits**:
- **Separation of Storage and Compute**: Scale independently
- **Multi-cluster**: Multiple compute clusters access same data
- **Zero-copy Cloning**: Instant database/table copies
- **Time Travel**: Query historical data
- **Automatic Scaling**: Elastic compute resources

## 2. Virtual Warehouses
**What they are**: Compute clusters that execute queries and DML operations.

**Warehouse Sizes**:
```sql
-- Create warehouses of different sizes
CREATE WAREHOUSE SMALL_WH WITH 
    WAREHOUSE_SIZE = 'SMALL'        -- 1 server, 8 cores
    AUTO_SUSPEND = 300              -- Suspend after 5 minutes
    AUTO_RESUME = TRUE              -- Auto-resume on query
    INITIALLY_SUSPENDED = TRUE;

CREATE WAREHOUSE LARGE_WH WITH 
    WAREHOUSE_SIZE = 'LARGE'        -- 8 servers, 64 cores
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE;

-- Warehouse sizes: X-SMALL, SMALL, MEDIUM, LARGE, X-LARGE, 2X-LARGE, 3X-LARGE, 4X-LARGE
```

**Multi-cluster Warehouses**:
```sql
-- Auto-scaling warehouse
CREATE WAREHOUSE ETL_WH WITH 
    WAREHOUSE_SIZE = 'MEDIUM'
    MIN_CLUSTER_COUNT = 1           -- Minimum clusters
    MAX_CLUSTER_COUNT = 5           -- Maximum clusters
    SCALING_POLICY = 'STANDARD'     -- STANDARD or ECONOMY
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE;

-- Monitor cluster usage
SHOW WAREHOUSES;
SELECT * FROM INFORMATION_SCHEMA.WAREHOUSE_LOAD_HISTORY;
```

**Warehouse Management**:
```sql
-- Resize warehouse
ALTER WAREHOUSE COMPUTE_WH SET WAREHOUSE_SIZE = 'LARGE';

-- Suspend/Resume
ALTER WAREHOUSE COMPUTE_WH SUSPEND;
ALTER WAREHOUSE COMPUTE_WH RESUME;

-- Set warehouse for session
USE WAREHOUSE COMPUTE_WH;

-- Query with specific warehouse
SELECT COUNT(*) FROM SALES USING WAREHOUSE LARGE_WH;
```

## 3. Database Objects
**Three-Level Namespace**: `DATABASE.SCHEMA.OBJECT`

### Databases and Schemas
```sql
-- Create database
CREATE DATABASE ANALYTICS_DB;
USE DATABASE ANALYTICS_DB;

-- Create schemas
CREATE SCHEMA RAW_DATA;
CREATE SCHEMA STAGING;
CREATE SCHEMA MARTS;

-- Fully qualified names
SELECT * FROM ANALYTICS_DB.MARTS.DIM_CUSTOMERS;
```

### Tables
```sql
-- Permanent table
CREATE TABLE CUSTOMERS (
    CUSTOMER_ID NUMBER(10,0) NOT NULL,
    FIRST_NAME VARCHAR(50),
    LAST_NAME VARCHAR(50),
    EMAIL VARCHAR(100),
    CREATED_DATE TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    CONSTRAINT PK_CUSTOMERS PRIMARY KEY (CUSTOMER_ID)
);

-- Temporary table (session-scoped)
CREATE TEMPORARY TABLE TEMP_ANALYSIS AS
SELECT CUSTOMER_ID, COUNT(*) AS ORDER_COUNT
FROM ORDERS
GROUP BY CUSTOMER_ID;

-- Transient table (no fail-safe, lower cost)
CREATE TRANSIENT TABLE STAGING_ORDERS (
    ORDER_ID NUMBER,
    CUSTOMER_ID NUMBER,
    ORDER_DATE DATE,
    AMOUNT DECIMAL(10,2)
);
```

### External Tables
```sql
-- Create file format
CREATE FILE FORMAT CSV_FORMAT
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    NULL_IF = ('NULL', 'null', '')
    EMPTY_FIELD_AS_NULL = TRUE;

-- Create stage
CREATE STAGE S3_STAGE
    URL = 's3://my-bucket/data/'
    CREDENTIALS = (AWS_KEY_ID = 'AKIAIOSFODNN7EXAMPLE' 
                   AWS_SECRET_KEY = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY');

-- Create external table
CREATE EXTERNAL TABLE EXT_CUSTOMERS (
    CUSTOMER_ID NUMBER,
    NAME VARCHAR(100),
    EMAIL VARCHAR(100)
)
WITH LOCATION = @S3_STAGE/customers/
FILE_FORMAT = CSV_FORMAT
AUTO_REFRESH = TRUE;
```

## 4. Data Loading
**COPY Command**:
```sql
-- Load from stage
COPY INTO CUSTOMERS
FROM @S3_STAGE/customers.csv
FILE_FORMAT = CSV_FORMAT
ON_ERROR = 'CONTINUE';

-- Load with transformations
COPY INTO CUSTOMERS (CUSTOMER_ID, FULL_NAME, EMAIL, CREATED_DATE)
FROM (
    SELECT 
        $1::NUMBER,
        CONCAT($2, ' ', $3),
        LOWER($4),
        CURRENT_TIMESTAMP()
    FROM @S3_STAGE/raw_customers.csv
)
FILE_FORMAT = CSV_FORMAT;

-- Load JSON data
COPY INTO JSON_TABLE
FROM @S3_STAGE/data.json
FILE_FORMAT = (TYPE = 'JSON');
```

**Snowpipe (Continuous Loading)**:
```sql
-- Create pipe for auto-loading
CREATE PIPE CUSTOMER_PIPE
AUTO_INGEST = TRUE
AS COPY INTO CUSTOMERS
FROM @S3_STAGE/customers/
FILE_FORMAT = CSV_FORMAT;

-- Show pipe status
SELECT SYSTEM$PIPE_STATUS('CUSTOMER_PIPE');

-- Refresh pipe manually
SELECT SYSTEM$PIPE_FORCE_RESUME('CUSTOMER_PIPE');
```

**Bulk Loading Best Practices**:
```sql
-- Use appropriate warehouse size
USE WAREHOUSE LARGE_WH;

-- Disable auto-commit for large loads
BEGIN;
COPY INTO LARGE_TABLE FROM @STAGE/data/ PATTERN = '.*\.csv';
COMMIT;

-- Parallel loading with multiple files
COPY INTO ORDERS
FROM @S3_STAGE/orders/
PATTERN = 'orders_[0-9]+\.csv'
FILE_FORMAT = CSV_FORMAT;
```

## 5. Cloning and Time Travel
**Zero-Copy Cloning**:
```sql
-- Clone database
CREATE DATABASE DEV_DB CLONE PROD_DB;

-- Clone table
CREATE TABLE CUSTOMERS_BACKUP CLONE CUSTOMERS;

-- Clone at specific time
CREATE TABLE CUSTOMERS_YESTERDAY CLONE CUSTOMERS 
AT (TIMESTAMP => '2024-01-14 23:59:59'::TIMESTAMP);

-- Clone from stream offset
CREATE TABLE ORDERS_CLONE CLONE ORDERS 
AT (STREAM => 'ORDER_STREAM');
```

**Time Travel**:
```sql
-- Query historical data (up to 90 days for Enterprise)
SELECT * FROM CUSTOMERS AT (TIMESTAMP => '2024-01-01 00:00:00'::TIMESTAMP);

-- Query by query ID
SELECT * FROM CUSTOMERS AT (STATEMENT => '01a2b3c4-5678-90ab-cdef-1234567890ab');

-- Query before statement
SELECT * FROM CUSTOMERS BEFORE (STATEMENT => '01a2b3c4-5678-90ab-cdef-1234567890ab');

-- Restore table
CREATE OR REPLACE TABLE CUSTOMERS AS 
SELECT * FROM CUSTOMERS AT (TIMESTAMP => '2024-01-14 12:00:00'::TIMESTAMP);
```

**Undrop Objects**:
```sql
-- Undrop table
UNDROP TABLE CUSTOMERS;

-- Undrop database
UNDROP DATABASE ANALYTICS_DB;

-- Show dropped objects
SHOW TABLES HISTORY;
```

## 6. Streams and Tasks
**Streams (Change Data Capture)**:
```sql
-- Create stream on table
CREATE STREAM CUSTOMER_STREAM ON TABLE CUSTOMERS;

-- Create stream on view
CREATE STREAM ORDER_CHANGES ON VIEW ORDER_SUMMARY;

-- Query stream data
SELECT 
    CUSTOMER_ID,
    FIRST_NAME,
    LAST_NAME,
    METADATA$ACTION,        -- INSERT, UPDATE, DELETE
    METADATA$ISUPDATE,      -- TRUE for UPDATE
    METADATA$ROW_ID
FROM CUSTOMER_STREAM;

-- Process stream data
INSERT INTO CUSTOMER_HISTORY
SELECT 
    CUSTOMER_ID,
    FIRST_NAME,
    LAST_NAME,
    METADATA$ACTION,
    CURRENT_TIMESTAMP()
FROM CUSTOMER_STREAM
WHERE METADATA$ACTION = 'INSERT';
```

**Tasks (Scheduling)**:
```sql
-- Create task
CREATE TASK DAILY_ETL_TASK
    WAREHOUSE = ETL_WH
    SCHEDULE = 'USING CRON 0 2 * * * UTC'  -- Daily at 2 AM UTC
AS
    CALL ETL_PROCEDURE();

-- Task with stream dependency
CREATE TASK PROCESS_CUSTOMER_CHANGES
    WAREHOUSE = SMALL_WH
    AFTER CUSTOMER_STREAM
AS
    INSERT INTO CUSTOMER_AUDIT
    SELECT * FROM CUSTOMER_STREAM;

-- Enable task
ALTER TASK DAILY_ETL_TASK RESUME;

-- Monitor tasks
SELECT * FROM INFORMATION_SCHEMA.TASK_HISTORY;
```

## 7. Stored Procedures and UDFs
**Stored Procedures**:
```sql
-- JavaScript stored procedure
CREATE OR REPLACE PROCEDURE ETL_CUSTOMERS()
RETURNS STRING
LANGUAGE JAVASCRIPT
AS
$$
    var sql_command = "INSERT INTO CUSTOMERS_SUMMARY SELECT CUSTOMER_ID, COUNT(*) FROM ORDERS GROUP BY CUSTOMER_ID";
    var statement = snowflake.createStatement({sqlText: sql_command});
    var result = statement.execute();
    return "ETL completed successfully";
$$;

-- SQL stored procedure
CREATE OR REPLACE PROCEDURE UPDATE_CUSTOMER_TIER(CUSTOMER_ID NUMBER)
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    total_spent DECIMAL(10,2);
    new_tier VARCHAR(20);
BEGIN
    SELECT SUM(AMOUNT) INTO total_spent 
    FROM ORDERS 
    WHERE CUSTOMER_ID = :CUSTOMER_ID;
    
    IF (total_spent >= 10000) THEN
        new_tier := 'PLATINUM';
    ELSEIF (total_spent >= 5000) THEN
        new_tier := 'GOLD';
    ELSE
        new_tier := 'SILVER';
    END IF;
    
    UPDATE CUSTOMERS 
    SET TIER = new_tier 
    WHERE CUSTOMER_ID = :CUSTOMER_ID;
    
    RETURN 'Customer tier updated to ' || new_tier;
END;
$$;
```

**User-Defined Functions**:
```sql
-- SQL UDF
CREATE OR REPLACE FUNCTION CALCULATE_AGE(BIRTH_DATE DATE)
RETURNS NUMBER
AS
$$
    DATEDIFF('YEAR', BIRTH_DATE, CURRENT_DATE())
$$;

-- JavaScript UDF
CREATE OR REPLACE FUNCTION PARSE_EMAIL_DOMAIN(EMAIL STRING)
RETURNS STRING
LANGUAGE JAVASCRIPT
AS
$$
    if (EMAIL) {
        var parts = EMAIL.split('@');
        return parts.length > 1 ? parts[1] : null;
    }
    return null;
$$;

-- Use UDFs
SELECT 
    CUSTOMER_ID,
    FIRST_NAME,
    CALCULATE_AGE(BIRTH_DATE) AS AGE,
    PARSE_EMAIL_DOMAIN(EMAIL) AS EMAIL_DOMAIN
FROM CUSTOMERS;
```

## 8. Security and Access Control
**Role-Based Access Control**:
```sql
-- Create roles
CREATE ROLE DATA_ENGINEER;
CREATE ROLE DATA_ANALYST;
CREATE ROLE DATA_SCIENTIST;

-- Grant privileges to roles
GRANT USAGE ON DATABASE ANALYTICS_DB TO ROLE DATA_ANALYST;
GRANT USAGE ON SCHEMA ANALYTICS_DB.MARTS TO ROLE DATA_ANALYST;
GRANT SELECT ON ALL TABLES IN SCHEMA ANALYTICS_DB.MARTS TO ROLE DATA_ANALYST;

-- Grant roles to users
GRANT ROLE DATA_ANALYST TO USER john_doe;

-- Create custom role hierarchy
GRANT ROLE DATA_ANALYST TO ROLE DATA_SCIENTIST;
```

**Row-Level Security**:
```sql
-- Create row access policy
CREATE ROW ACCESS POLICY CUSTOMER_POLICY AS (REGION) RETURNS BOOLEAN ->
    CASE 
        WHEN CURRENT_ROLE() = 'ADMIN' THEN TRUE
        WHEN CURRENT_ROLE() = 'US_ANALYST' AND REGION = 'US' THEN TRUE
        WHEN CURRENT_ROLE() = 'EU_ANALYST' AND REGION = 'EU' THEN TRUE
        ELSE FALSE
    END;

-- Apply policy to table
ALTER TABLE CUSTOMERS ADD ROW ACCESS POLICY CUSTOMER_POLICY ON (REGION);
```

**Column-Level Security**:
```sql
-- Create masking policy
CREATE MASKING POLICY EMAIL_MASK AS (VAL STRING) RETURNS STRING ->
    CASE 
        WHEN CURRENT_ROLE() IN ('ADMIN', 'DATA_ENGINEER') THEN VAL
        ELSE REGEXP_REPLACE(VAL, '.+@', '*****@')
    END;

-- Apply masking policy
ALTER TABLE CUSTOMERS MODIFY COLUMN EMAIL SET MASKING POLICY EMAIL_MASK;
```

## 9. Performance Optimization
**Clustering**:
```sql
-- Create clustered table
CREATE TABLE ORDERS (
    ORDER_ID NUMBER,
    CUSTOMER_ID NUMBER,
    ORDER_DATE DATE,
    AMOUNT DECIMAL(10,2)
) CLUSTER BY (ORDER_DATE, CUSTOMER_ID);

-- Add clustering to existing table
ALTER TABLE ORDERS CLUSTER BY (ORDER_DATE);

-- Monitor clustering
SELECT SYSTEM$CLUSTERING_INFORMATION('ORDERS', '(ORDER_DATE)');

-- Automatic clustering
ALTER TABLE ORDERS RESUME RECLUSTER;
```

**Search Optimization**:
```sql
-- Enable search optimization
ALTER TABLE CUSTOMERS ADD SEARCH OPTIMIZATION;

-- Optimize specific columns
ALTER TABLE CUSTOMERS ADD SEARCH OPTIMIZATION ON (FIRST_NAME, LAST_NAME, EMAIL);

-- Monitor search optimization
SELECT * FROM INFORMATION_SCHEMA.SEARCH_OPTIMIZATION_HISTORY;
```

**Query Optimization**:
```sql
-- Use appropriate data types
CREATE TABLE OPTIMIZED_ORDERS (
    ORDER_ID NUMBER(10,0),          -- Specify precision
    CUSTOMER_ID NUMBER(10,0),
    ORDER_DATE DATE,                -- Use DATE instead of TIMESTAMP when possible
    AMOUNT NUMBER(10,2),            -- Specify scale for decimals
    STATUS VARCHAR(20)              -- Specify length for strings
);

-- Partition pruning with clustering
SELECT * FROM ORDERS 
WHERE ORDER_DATE BETWEEN '2024-01-01' AND '2024-01-31'  -- Uses clustering
AND CUSTOMER_ID = 12345;

-- Use LIMIT for large result sets
SELECT * FROM LARGE_TABLE 
ORDER BY CREATED_DATE DESC 
LIMIT 1000;
```

## 10. Data Sharing and Marketplace
**Secure Data Sharing**:
```sql
-- Create share
CREATE SHARE CUSTOMER_SHARE;

-- Grant database to share
GRANT USAGE ON DATABASE ANALYTICS_DB TO SHARE CUSTOMER_SHARE;
GRANT USAGE ON SCHEMA ANALYTICS_DB.MARTS TO SHARE CUSTOMER_SHARE;
GRANT SELECT ON TABLE ANALYTICS_DB.MARTS.DIM_CUSTOMERS TO SHARE CUSTOMER_SHARE;

-- Add accounts to share
ALTER SHARE CUSTOMER_SHARE ADD ACCOUNTS = ABC12345, DEF67890;

-- Create database from share (consumer side)
CREATE DATABASE SHARED_CUSTOMER_DATA FROM SHARE PROVIDER_ACCOUNT.CUSTOMER_SHARE;
```

**Reader Accounts**:
```sql
-- Create reader account
CREATE MANAGED ACCOUNT CUSTOMER_READER
    ADMIN_NAME = 'reader_admin'
    ADMIN_PASSWORD = 'SecurePassword123!'
    TYPE = READER;

-- Share data with reader account
ALTER SHARE CUSTOMER_SHARE ADD ACCOUNTS = READER_ACCOUNT_LOCATOR;
```

**Snowflake Marketplace**:
```sql
-- List available data products
SHOW SHARES IN APPLICATION PACKAGE SNOWFLAKE_MARKETPLACE;

-- Create database from marketplace listing
CREATE DATABASE WEATHER_DATA FROM SHARE SFC_SAMPLES.SAMPLE_DATA;

-- Query marketplace data
SELECT * FROM WEATHER_DATA.WEATHER.DAILY_14_TOTAL LIMIT 10;
```