# Snowflake Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-30)](#basic-level-questions-1-30)
2. [Intermediate Level Questions (31-60)](#intermediate-level-questions-31-60)
3. [Advanced Level Questions (61-90)](#advanced-level-questions-61-90)
4. [Architecture & Performance (91-120)](#architecture--performance-91-120)
5. [Data Loading & Integration (121-150)](#data-loading--integration-121-150)
6. [Security & Governance (151-180)](#security--governance-151-180)
7. [Scenario-Based Questions (181-200)](#scenario-based-questions-181-200)

---

## Basic Level Questions (1-30)

### 1. What is Snowflake and how does it differ from traditional data warehouses?

**Snowflake** is a cloud-native data warehouse that separates compute and storage, providing elastic scalability and pay-per-use pricing.

#### **Key Differences:**

| Aspect | Snowflake | Traditional Data Warehouse |
|--------|-----------|---------------------------|
| **Architecture** | Multi-cluster, shared data | Shared-nothing architecture |
| **Scalability** | Elastic, instant scaling | Manual scaling, downtime required |
| **Storage** | Unlimited, automatic compression | Fixed capacity, manual management |
| **Compute** | Independent virtual warehouses | Coupled compute and storage |
| **Pricing** | Pay-per-second usage | Fixed licensing costs |
| **Maintenance** | Fully managed, zero maintenance | Requires DBA management |
| **Data Sharing** | Native secure data sharing | Complex ETL processes |

```sql
-- Basic Snowflake operations
-- Create database and schema
CREATE DATABASE IF NOT EXISTS DEMO_DB;
CREATE SCHEMA IF NOT EXISTS DEMO_DB.SALES;

-- Create table with Snowflake-specific features
CREATE TABLE DEMO_DB.SALES.CUSTOMERS (
    CUSTOMER_ID NUMBER AUTOINCREMENT,
    NAME VARCHAR(100) NOT NULL,
    EMAIL VARCHAR(255),
    REGISTRATION_DATE DATE DEFAULT CURRENT_DATE(),
    LAST_LOGIN TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    METADATA VARIANT  -- JSON data type
);

-- Insert sample data
INSERT INTO DEMO_DB.SALES.CUSTOMERS (NAME, EMAIL, METADATA) VALUES
('Alice Johnson', 'alice@email.com', PARSE_JSON('{"age": 28, "city": "New York", "preferences": ["tech", "books"]}')),
('Bob Smith', 'bob@email.com', PARSE_JSON('{"age": 35, "city": "San Francisco", "preferences": ["sports", "music"]}')),
('Charlie Brown', 'charlie@email.com', PARSE_JSON('{"age": 42, "city": "Chicago", "preferences": ["travel", "food"]}'));

-- Query with JSON operations
SELECT 
    CUSTOMER_ID,
    NAME,
    EMAIL,
    METADATA:age::NUMBER AS AGE,
    METADATA:city::STRING AS CITY,
    ARRAY_SIZE(METADATA:preferences) AS PREFERENCE_COUNT
FROM DEMO_DB.SALES.CUSTOMERS;
```

**Output:**
```
CUSTOMER_ID | NAME          | EMAIL              | AGE | CITY          | PREFERENCE_COUNT
------------|---------------|--------------------|----|---------------|------------------
1           | Alice Johnson | alice@email.com    | 28  | New York      | 2
2           | Bob Smith     | bob@email.com      | 35  | San Francisco | 2
3           | Charlie Brown | charlie@email.com  | 42  | Chicago       | 2
```

### 2. What is Snowflake's unique architecture?

**Answer:** Snowflake uses a multi-cluster, shared data architecture with three distinct layers.

#### 🎯 **Architecture Layers**
- **Storage Layer**: Centralized, compressed, encrypted storage
- **Compute Layer**: Virtual warehouses for processing
- **Services Layer**: Metadata, security, optimization

```sql
-- Demonstrate architecture benefits
-- Create multiple virtual warehouses for different workloads
CREATE WAREHOUSE IF NOT EXISTS ETL_WH 
WITH WAREHOUSE_SIZE = 'LARGE'
     AUTO_SUSPEND = 300  -- 5 minutes
     AUTO_RESUME = TRUE
     COMMENT = 'Warehouse for ETL operations';

CREATE WAREHOUSE IF NOT EXISTS ANALYTICS_WH 
WITH WAREHOUSE_SIZE = 'MEDIUM'
     AUTO_SUSPEND = 60   -- 1 minute
     AUTO_RESUME = TRUE
     COMMENT = 'Warehouse for analytics queries';

-- Show warehouse information
SHOW WAREHOUSES;

-- Use different warehouses for different operations
USE WAREHOUSE ETL_WH;

-- ETL operation - data loading
CREATE TABLE DEMO_DB.SALES.ORDERS AS
SELECT 
    ROW_NUMBER() OVER (ORDER BY RANDOM()) AS ORDER_ID,
    UNIFORM(1, 1000, RANDOM()) AS CUSTOMER_ID,
    DATEADD(DAY, -UNIFORM(1, 365, RANDOM()), CURRENT_DATE()) AS ORDER_DATE,
    UNIFORM(10, 1000, RANDOM()) AS ORDER_AMOUNT,
    ARRAY_CONSTRUCT('pending', 'processing', 'shipped', 'delivered')[UNIFORM(1, 4, RANDOM())] AS STATUS
FROM TABLE(GENERATOR(ROWCOUNT => 10000));

-- Switch to analytics warehouse
USE WAREHOUSE ANALYTICS_WH;

-- Analytics query
SELECT 
    STATUS,
    COUNT(*) AS ORDER_COUNT,
    AVG(ORDER_AMOUNT) AS AVG_AMOUNT,
    SUM(ORDER_AMOUNT) AS TOTAL_AMOUNT
FROM DEMO_DB.SALES.ORDERS
GROUP BY STATUS
ORDER BY TOTAL_AMOUNT DESC;
```

**Output:**
```
STATUS      | ORDER_COUNT | AVG_AMOUNT | TOTAL_AMOUNT
------------|-------------|------------|-------------
shipped     | 2487        | 505.23     | 1,256,507
delivered   | 2501        | 498.76     | 1,247,234
processing  | 2534        | 492.18     | 1,246,984
pending     | 2478        | 503.91     | 1,248,691
```

### 3. What are Virtual Warehouses and how do they work?

**Answer:** Virtual Warehouses are compute clusters that execute queries independently of data storage.

#### 🎯 **Virtual Warehouse Features**
- **Independent Scaling**: Scale compute without affecting storage
- **Auto-suspend/Resume**: Automatic resource management
- **Multi-cluster**: Handle concurrent workloads
- **Different Sizes**: T-shirt sizing (XS to 6XL)

```sql
-- Create warehouses of different sizes
CREATE WAREHOUSE SMALL_WH WITH WAREHOUSE_SIZE = 'SMALL';
CREATE WAREHOUSE LARGE_WH WITH WAREHOUSE_SIZE = 'LARGE';

-- Demonstrate performance differences
-- Small warehouse query
USE WAREHOUSE SMALL_WH;
SET START_TIME = CURRENT_TIMESTAMP();

SELECT 
    EXTRACT(YEAR FROM ORDER_DATE) AS YEAR,
    EXTRACT(MONTH FROM ORDER_DATE) AS MONTH,
    COUNT(*) AS ORDERS,
    SUM(ORDER_AMOUNT) AS REVENUE
FROM DEMO_DB.SALES.ORDERS
GROUP BY YEAR, MONTH
ORDER BY YEAR, MONTH;

SET SMALL_WH_TIME = DATEDIFF(MILLISECOND, $START_TIME, CURRENT_TIMESTAMP());

-- Large warehouse query (same query)
USE WAREHOUSE LARGE_WH;
SET START_TIME = CURRENT_TIMESTAMP();

SELECT 
    EXTRACT(YEAR FROM ORDER_DATE) AS YEAR,
    EXTRACT(MONTH FROM ORDER_DATE) AS MONTH,
    COUNT(*) AS ORDERS,
    SUM(ORDER_AMOUNT) AS REVENUE
FROM DEMO_DB.SALES.ORDERS
GROUP BY YEAR, MONTH
ORDER BY YEAR, MONTH;

SET LARGE_WH_TIME = DATEDIFF(MILLISECOND, $START_TIME, CURRENT_TIMESTAMP());

-- Compare performance
SELECT 
    'Small Warehouse' AS WAREHOUSE_TYPE,
    $SMALL_WH_TIME AS EXECUTION_TIME_MS
UNION ALL
SELECT 
    'Large Warehouse' AS WAREHOUSE_TYPE,
    $LARGE_WH_TIME AS EXECUTION_TIME_MS;

-- Show warehouse usage
SELECT 
    WAREHOUSE_NAME,
    CREDITS_USED,
    CREDITS_USED_COMPUTE,
    CREDITS_USED_CLOUD_SERVICES
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE START_TIME >= DATEADD(HOUR, -1, CURRENT_TIMESTAMP())
ORDER BY START_TIME DESC;
```

**Output:**
```
YEAR | MONTH | ORDERS | REVENUE
-----|-------|--------|----------
2023 | 1     | 849    | 425,673
2023 | 2     | 765    | 383,291
2023 | 3     | 832    | 417,845
...

WAREHOUSE_TYPE   | EXECUTION_TIME_MS
-----------------|------------------
Small Warehouse  | 1,245
Large Warehouse  | 423

WAREHOUSE_NAME | CREDITS_USED | CREDITS_USED_COMPUTE | CREDITS_USED_CLOUD_SERVICES
---------------|--------------|---------------------|---------------------------
LARGE_WH       | 0.0028       | 0.0025              | 0.0003
SMALL_WH       | 0.0015       | 0.0013              | 0.0002
```

### 4. How does Snowflake handle data types and semi-structured data?

**Answer:** Snowflake supports standard SQL data types plus native JSON, XML, and ARRAY handling.

#### 🎯 **Data Type Categories**
- **Numeric**: NUMBER, DECIMAL, INT, FLOAT
- **String**: VARCHAR, CHAR, TEXT
- **Date/Time**: DATE, TIME, TIMESTAMP variants
- **Semi-structured**: VARIANT, OBJECT, ARRAY
- **Binary**: BINARY, VARBINARY

```sql
-- Create table with various data types
CREATE TABLE DEMO_DB.SALES.PRODUCT_CATALOG (
    PRODUCT_ID NUMBER,
    PRODUCT_NAME VARCHAR(255),
    PRICE NUMBER(10,2),
    LAUNCH_DATE DATE,
    LAST_UPDATED TIMESTAMP_LTZ,
    SPECIFICATIONS VARIANT,  -- JSON data
    TAGS ARRAY,             -- Array of strings
    METADATA OBJECT         -- Object type
);

-- Insert data with semi-structured content
INSERT INTO DEMO_DB.SALES.PRODUCT_CATALOG VALUES
(1, 'Laptop Pro', 1299.99, '2023-01-15', CURRENT_TIMESTAMP(),
 PARSE_JSON('{"cpu": "Intel i7", "ram": "16GB", "storage": "512GB SSD", "ports": ["USB-C", "HDMI", "Audio"]}'),
 ARRAY_CONSTRUCT('electronics', 'computers', 'portable'),
 OBJECT_CONSTRUCT('brand', 'TechCorp', 'warranty', '2 years', 'rating', 4.5)
),
(2, 'Smartphone X', 899.99, '2023-03-20', CURRENT_TIMESTAMP(),
 PARSE_JSON('{"cpu": "A15 Bionic", "ram": "8GB", "storage": "256GB", "cameras": [{"type": "main", "mp": 48}, {"type": "ultra-wide", "mp": 12}]}'),
 ARRAY_CONSTRUCT('electronics', 'mobile', 'communication'),
 OBJECT_CONSTRUCT('brand', 'MobileTech', 'warranty', '1 year', 'rating', 4.8)
);

-- Query semi-structured data
SELECT 
    PRODUCT_ID,
    PRODUCT_NAME,
    PRICE,
    
    -- Extract from VARIANT (JSON)
    SPECIFICATIONS:cpu::STRING AS CPU,
    SPECIFICATIONS:ram::STRING AS RAM,
    ARRAY_SIZE(SPECIFICATIONS:ports) AS PORT_COUNT,
    
    -- Work with ARRAY
    ARRAY_SIZE(TAGS) AS TAG_COUNT,
    TAGS[0]::STRING AS PRIMARY_TAG,
    
    -- Extract from OBJECT
    METADATA:brand::STRING AS BRAND,
    METADATA:rating::FLOAT AS RATING
FROM DEMO_DB.SALES.PRODUCT_CATALOG;

-- Flatten nested arrays
SELECT 
    p.PRODUCT_NAME,
    f.VALUE::STRING AS TAG
FROM DEMO_DB.SALES.PRODUCT_CATALOG p,
LATERAL FLATTEN(INPUT => p.TAGS) f;

-- Complex JSON path queries
SELECT 
    PRODUCT_NAME,
    SPECIFICATIONS:cameras[0].type::STRING AS MAIN_CAMERA_TYPE,
    SPECIFICATIONS:cameras[0].mp::NUMBER AS MAIN_CAMERA_MP
FROM DEMO_DB.SALES.PRODUCT_CATALOG
WHERE SPECIFICATIONS:cameras IS NOT NULL;
```

**Output:**
```
PRODUCT_ID | PRODUCT_NAME  | PRICE   | CPU        | RAM  | PORT_COUNT | TAG_COUNT | PRIMARY_TAG | BRAND     | RATING
-----------|---------------|---------|------------|------|------------|-----------|-------------|-----------|--------
1          | Laptop Pro    | 1299.99 | Intel i7   | 16GB | 3          | 3         | electronics | TechCorp  | 4.5
2          | Smartphone X  | 899.99  | A15 Bionic | 8GB  | null       | 3         | electronics | MobileTech| 4.8

PRODUCT_NAME  | TAG
--------------|-------------
Laptop Pro    | electronics
Laptop Pro    | computers
Laptop Pro    | portable
Smartphone X  | electronics
Smartphone X  | mobile
Smartphone X  | communication

PRODUCT_NAME | MAIN_CAMERA_TYPE | MAIN_CAMERA_MP
-------------|------------------|----------------
Smartphone X | main             | 48
```

### 5. What are Snowflake's data loading options?

**Answer:** Snowflake provides multiple methods for loading data efficiently.

#### 🎯 **Data Loading Methods**
- **COPY INTO**: Bulk loading from files
- **INSERT**: Direct SQL inserts
- **Snowpipe**: Continuous, automated loading
- **External Tables**: Query data without loading
- **Streams**: Change data capture

```sql
-- Create file format for CSV loading
CREATE FILE FORMAT DEMO_DB.SALES.CSV_FORMAT
TYPE = 'CSV'
FIELD_DELIMITER = ','
SKIP_HEADER = 1
NULL_IF = ('NULL', 'null', '')
EMPTY_FIELD_AS_NULL = TRUE
COMPRESSION = 'AUTO';

-- Create stage for file storage
CREATE STAGE DEMO_DB.SALES.DATA_STAGE
FILE_FORMAT = DEMO_DB.SALES.CSV_FORMAT
COMMENT = 'Stage for loading data files';

-- Simulate file upload (in practice, files would be uploaded to cloud storage)
-- Create sample data in a table to export
CREATE TABLE DEMO_DB.SALES.SAMPLE_SALES AS
SELECT 
    ROW_NUMBER() OVER (ORDER BY RANDOM()) AS SALE_ID,
    DATEADD(DAY, -UNIFORM(1, 30, RANDOM()), CURRENT_DATE()) AS SALE_DATE,
    UNIFORM(1, 1000, RANDOM()) AS CUSTOMER_ID,
    UNIFORM(10, 500, RANDOM()) AS AMOUNT,
    ARRAY_CONSTRUCT('online', 'store', 'phone')[UNIFORM(1, 3, RANDOM())] AS CHANNEL
FROM TABLE(GENERATOR(ROWCOUNT => 1000));

-- Create target table for loading
CREATE TABLE DEMO_DB.SALES.LOADED_SALES (
    SALE_ID NUMBER,
    SALE_DATE DATE,
    CUSTOMER_ID NUMBER,
    AMOUNT NUMBER,
    CHANNEL VARCHAR(20),
    LOAD_TIMESTAMP TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Demonstrate COPY INTO (simulated)
-- In practice: COPY INTO DEMO_DB.SALES.LOADED_SALES FROM @DEMO_DB.SALES.DATA_STAGE/sales_data.csv;

-- Alternative: Direct INSERT with transformation
INSERT INTO DEMO_DB.SALES.LOADED_SALES (SALE_ID, SALE_DATE, CUSTOMER_ID, AMOUNT, CHANNEL)
SELECT 
    SALE_ID,
    SALE_DATE,
    CUSTOMER_ID,
    AMOUNT,
    CHANNEL
FROM DEMO_DB.SALES.SAMPLE_SALES
WHERE SALE_DATE >= DATEADD(DAY, -7, CURRENT_DATE());

-- Check loaded data
SELECT 
    COUNT(*) AS TOTAL_RECORDS,
    MIN(SALE_DATE) AS EARLIEST_SALE,
    MAX(SALE_DATE) AS LATEST_SALE,
    SUM(AMOUNT) AS TOTAL_AMOUNT,
    COUNT(DISTINCT CHANNEL) AS UNIQUE_CHANNELS
FROM DEMO_DB.SALES.LOADED_SALES;

-- Show loading history
SELECT 
    FILE_NAME,
    STATUS,
    ROWS_PARSED,
    ROWS_LOADED,
    ERROR_COUNT,
    FIRST_ERROR_MESSAGE
FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => 'DEMO_DB.SALES.LOADED_SALES',
    START_TIME => DATEADD(HOUR, -1, CURRENT_TIMESTAMP())
));
```

**Output:**
```
TOTAL_RECORDS | EARLIEST_SALE | LATEST_SALE | TOTAL_AMOUNT | UNIQUE_CHANNELS
--------------|---------------|-------------|--------------|----------------
234           | 2024-01-09    | 2024-01-15  | 58,742       | 3

FILE_NAME | STATUS    | ROWS_PARSED | ROWS_LOADED | ERROR_COUNT | FIRST_ERROR_MESSAGE
----------|-----------|-------------|-------------|-------------|--------------------
(Direct)  | LOADED    | 234         | 234         | 0           | null
```

### 6. How do you implement slowly changing dimensions (SCD) in Snowflake?

**Answer:** Snowflake supports SCD patterns using MERGE statements and time-travel features.

#### 🎯 **SCD Implementation Types**
- **Type 1**: Overwrite existing data
- **Type 2**: Keep historical versions
- **Type 3**: Add columns for changes
- **Type 4**: Separate history table

```sql
-- Create dimension table for SCD Type 2
CREATE TABLE DEMO_DB.SALES.DIM_CUSTOMER (
    CUSTOMER_KEY NUMBER AUTOINCREMENT,
    CUSTOMER_ID NUMBER NOT NULL,
    NAME VARCHAR(100),
    EMAIL VARCHAR(255),
    CITY VARCHAR(100),
    EFFECTIVE_DATE DATE NOT NULL,
    EXPIRY_DATE DATE,
    IS_CURRENT BOOLEAN DEFAULT TRUE,
    CREATED_TIMESTAMP TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    UPDATED_TIMESTAMP TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Initial load
INSERT INTO DEMO_DB.SALES.DIM_CUSTOMER (CUSTOMER_ID, NAME, EMAIL, CITY, EFFECTIVE_DATE)
VALUES 
(101, 'John Doe', 'john@email.com', 'New York', '2024-01-01'),
(102, 'Jane Smith', 'jane@email.com', 'Los Angeles', '2024-01-01'),
(103, 'Bob Johnson', 'bob@email.com', 'Chicago', '2024-01-01');

-- Show initial data
SELECT * FROM DEMO_DB.SALES.DIM_CUSTOMER ORDER BY CUSTOMER_ID, EFFECTIVE_DATE;

-- Create staging table with changes
CREATE TABLE DEMO_DB.SALES.STG_CUSTOMER AS
SELECT * FROM (VALUES
    (101, 'John Doe', 'john.doe@newemail.com', 'Boston'),      -- Email and city change
    (102, 'Jane Smith', 'jane@email.com', 'Los Angeles'),      -- No change
    (103, 'Bob Johnson', 'bob@email.com', 'Miami'),            -- City change
    (104, 'Alice Brown', 'alice@email.com', 'Seattle')         -- New customer
) AS t(CUSTOMER_ID, NAME, EMAIL, CITY);

-- SCD Type 2 MERGE operation
MERGE INTO DEMO_DB.SALES.DIM_CUSTOMER AS target
USING (
    SELECT 
        s.CUSTOMER_ID,
        s.NAME,
        s.EMAIL,
        s.CITY,
        CURRENT_DATE() AS EFFECTIVE_DATE
    FROM DEMO_DB.SALES.STG_CUSTOMER s
) AS source
ON target.CUSTOMER_ID = source.CUSTOMER_ID AND target.IS_CURRENT = TRUE

-- Handle changes (expire old record, insert new)
WHEN MATCHED AND (
    target.NAME != source.NAME OR 
    target.EMAIL != source.EMAIL OR 
    target.CITY != source.CITY
) THEN UPDATE SET
    EXPIRY_DATE = DATEADD(DAY, -1, source.EFFECTIVE_DATE),
    IS_CURRENT = FALSE,
    UPDATED_TIMESTAMP = CURRENT_TIMESTAMP()

-- Handle new records
WHEN NOT MATCHED THEN INSERT (
    CUSTOMER_ID, NAME, EMAIL, CITY, EFFECTIVE_DATE
) VALUES (
    source.CUSTOMER_ID, source.NAME, source.EMAIL, source.CITY, source.EFFECTIVE_DATE
);

-- Insert new versions for changed records
INSERT INTO DEMO_DB.SALES.DIM_CUSTOMER (CUSTOMER_ID, NAME, EMAIL, CITY, EFFECTIVE_DATE)
SELECT 
    s.CUSTOMER_ID,
    s.NAME,
    s.EMAIL,
    s.CITY,
    CURRENT_DATE()
FROM DEMO_DB.SALES.STG_CUSTOMER s
JOIN DEMO_DB.SALES.DIM_CUSTOMER d 
    ON s.CUSTOMER_ID = d.CUSTOMER_ID 
    AND d.IS_CURRENT = FALSE 
    AND d.UPDATED_TIMESTAMP >= DATEADD(MINUTE, -5, CURRENT_TIMESTAMP())
WHERE (d.NAME != s.NAME OR d.EMAIL != s.EMAIL OR d.CITY != s.CITY);

-- Show SCD Type 2 results
SELECT 
    CUSTOMER_KEY,
    CUSTOMER_ID,
    NAME,
    EMAIL,
    CITY,
    EFFECTIVE_DATE,
    EXPIRY_DATE,
    IS_CURRENT
FROM DEMO_DB.SALES.DIM_CUSTOMER 
ORDER BY CUSTOMER_ID, EFFECTIVE_DATE;

-- Query current and historical data
SELECT 
    'Current View' AS VIEW_TYPE,
    COUNT(*) AS RECORD_COUNT
FROM DEMO_DB.SALES.DIM_CUSTOMER 
WHERE IS_CURRENT = TRUE

UNION ALL

SELECT 
    'Historical View' AS VIEW_TYPE,
    COUNT(*) AS RECORD_COUNT
FROM DEMO_DB.SALES.DIM_CUSTOMER 
WHERE IS_CURRENT = FALSE;
```

**Output:**
```
CUSTOMER_KEY | CUSTOMER_ID | NAME        | EMAIL              | CITY        | EFFECTIVE_DATE | EXPIRY_DATE | IS_CURRENT
-------------|-------------|-------------|--------------------|-----------  |----------------|-------------|------------
1            | 101         | John Doe    | john@email.com     | New York    | 2024-01-01     | 2024-01-14  | FALSE
2            | 102         | Jane Smith  | jane@email.com     | Los Angeles | 2024-01-01     | null        | TRUE
3            | 103         | Bob Johnson | bob@email.com      | Chicago     | 2024-01-01     | 2024-01-14  | FALSE
4            | 104         | Alice Brown | alice@email.com    | Seattle     | 2024-01-15     | null        | TRUE
5            | 101         | John Doe    | john.doe@newemail.com | Boston   | 2024-01-15     | null        | TRUE
6            | 103         | Bob Johnson | bob@email.com      | Miami       | 2024-01-15     | null        | TRUE

VIEW_TYPE      | RECORD_COUNT
---------------|-------------
Current View   | 4
Historical View| 2
```