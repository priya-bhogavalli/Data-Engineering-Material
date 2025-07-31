# Informatica Key Concepts

## 1. Informatica Architecture
**Components**:
- **PowerCenter**: ETL development and execution platform
- **Repository**: Metadata storage
- **Integration Service**: Executes workflows and sessions
- **Designer**: Development tool for mappings
- **Workflow Manager**: Scheduling and monitoring
- **Monitor**: Runtime monitoring and debugging

## 2. Mappings and Transformations
```sql
-- Source Qualifier (SQ)
-- Extracts data from relational sources
SELECT 
    CUSTOMER_ID,
    FIRST_NAME,
    LAST_NAME,
    EMAIL,
    REGISTRATION_DATE
FROM CUSTOMERS
WHERE REGISTRATION_DATE >= SYSDATE - 30

-- Expression Transformation
-- Data transformation and calculations
FULL_NAME = FIRST_NAME || ' ' || LAST_NAME
AGE = TRUNC((SYSDATE - DATE_OF_BIRTH) / 365.25)
EMAIL_DOMAIN = SUBSTR(EMAIL, INSTR(EMAIL, '@') + 1)

-- Filter Transformation
-- Conditional row filtering
ACTIVE_CUSTOMERS = STATUS = 'ACTIVE' AND LAST_LOGIN_DATE >= SYSDATE - 90

-- Aggregator Transformation
-- Group by operations
GROUP BY: CUSTOMER_SEGMENT
SUM(ORDER_AMOUNT) as TOTAL_SALES
COUNT(*) as ORDER_COUNT
AVG(ORDER_AMOUNT) as AVG_ORDER_VALUE
```

## 3. Lookup Transformations
```sql
-- Connected Lookup
-- Join with reference table
Lookup Table: PRODUCT_MASTER
Lookup Condition: IN_PRODUCT_ID = LKP_PRODUCT_ID
Return Values: 
  - PRODUCT_NAME
  - CATEGORY
  - UNIT_PRICE

-- Unconnected Lookup
-- Function-based lookup
:LKP.LKP_GET_CUSTOMER_TIER(CUSTOMER_ID)

-- Dynamic Lookup
-- Updates lookup cache during session
-- Used for slowly changing dimensions

-- Persistent Lookup Cache
-- Reuse cache across sessions
$PMCacheDir/LKP_CUSTOMER_CACHE.dat
```

## 4. Slowly Changing Dimensions (SCD)
```sql
-- SCD Type 1 - Overwrite
UPDATE CUSTOMER_DIM 
SET 
    CUSTOMER_NAME = :NEW_NAME,
    EMAIL = :NEW_EMAIL,
    LAST_UPDATED = SYSDATE
WHERE CUSTOMER_KEY = :CUSTOMER_KEY

-- SCD Type 2 - Historical Tracking
-- Insert new record for changes
INSERT INTO CUSTOMER_DIM (
    CUSTOMER_KEY,
    CUSTOMER_ID,
    CUSTOMER_NAME,
    EMAIL,
    EFFECTIVE_DATE,
    EXPIRY_DATE,
    CURRENT_FLAG
) VALUES (
    CUSTOMER_DIM_SEQ.NEXTVAL,
    :CUSTOMER_ID,
    :NEW_NAME,
    :NEW_EMAIL,
    SYSDATE,
    TO_DATE('9999-12-31', 'YYYY-MM-DD'),
    'Y'
)

-- Update previous record
UPDATE CUSTOMER_DIM 
SET 
    EXPIRY_DATE = SYSDATE - 1,
    CURRENT_FLAG = 'N'
WHERE CUSTOMER_ID = :CUSTOMER_ID 
AND CURRENT_FLAG = 'Y'

-- SCD Type 3 - Previous Value Column
ALTER TABLE CUSTOMER_DIM ADD (
    PREVIOUS_EMAIL VARCHAR2(100),
    EMAIL_CHANGE_DATE DATE
)
```

## 5. Workflows and Sessions
```xml
<!-- Workflow Definition -->
<WORKFLOW NAME="DAILY_CUSTOMER_ETL" VERSION="1">
    <SESSION NAME="s_EXTRACT_CUSTOMERS" MAPPING="m_EXTRACT_CUSTOMERS"/>
    <SESSION NAME="s_TRANSFORM_CUSTOMERS" MAPPING="m_TRANSFORM_CUSTOMERS"/>
    <SESSION NAME="s_LOAD_CUSTOMER_DIM" MAPPING="m_LOAD_CUSTOMER_DIM"/>
    
    <!-- Dependencies -->
    <LINK FROM="s_EXTRACT_CUSTOMERS" TO="s_TRANSFORM_CUSTOMERS"/>
    <LINK FROM="s_TRANSFORM_CUSTOMERS" TO="s_LOAD_CUSTOMER_DIM"/>
    
    <!-- Scheduling -->
    <SCHEDULER TYPE="CRON" EXPRESSION="0 2 * * *"/>
</WORKFLOW>

<!-- Session Configuration -->
<SESSION NAME="s_LOAD_CUSTOMER_DIM">
    <CONFIG>
        <COMMIT_INTERVAL>10000</COMMIT_INTERVAL>
        <ERROR_THRESHOLD>100</ERROR_THRESHOLD>
        <RECOVERY_STRATEGY>RESTART_TASK</RECOVERY_STRATEGY>
    </CONFIG>
</SESSION>
```

## 6. Error Handling and Data Quality
```sql
-- Router Transformation
-- Multiple output groups based on conditions
GROUP1: VALID_RECORDS
  Condition: NOT ISNULL(CUSTOMER_ID) AND NOT ISNULL(EMAIL)
  
GROUP2: INVALID_EMAIL
  Condition: ISNULL(EMAIL) OR INSTR(EMAIL, '@') = 0
  
GROUP3: MISSING_CUSTOMER_ID
  Condition: ISNULL(CUSTOMER_ID)

-- Update Strategy Transformation
-- Define insert/update/delete operations
IIF(ISNULL(LKP_CUSTOMER_KEY), DD_INSERT, 
    IIF(CUSTOMER_NAME != LKP_CUSTOMER_NAME OR EMAIL != LKP_EMAIL, DD_UPDATE, DD_REJECT))

-- Data Quality Rules
-- Expression for validation
IS_VALID_EMAIL = IIF(
    INSTR(EMAIL, '@') > 0 AND 
    INSTR(EMAIL, '.') > INSTR(EMAIL, '@') AND
    LENGTH(EMAIL) > 5, 
    'VALID', 
    'INVALID'
)

-- Reject records to error table
CREATE TABLE CUSTOMER_ERRORS (
    ERROR_DATE DATE,
    SOURCE_ROW CLOB,
    ERROR_MESSAGE VARCHAR2(500),
    MAPPING_NAME VARCHAR2(100)
)
```

## 7. Performance Optimization
```sql
-- Partitioning
-- Partition large tables for parallel processing
PARTITION BY: REGISTRATION_DATE
RANGE: MONTHLY

-- Pushdown Optimization
-- Execute transformations in database
$DBConnectionName = SOURCE_DB
SELECT 
    CUSTOMER_ID,
    UPPER(FIRST_NAME) as FIRST_NAME,
    UPPER(LAST_NAME) as LAST_NAME,
    CASE 
        WHEN TOTAL_PURCHASES > 10000 THEN 'PREMIUM'
        WHEN TOTAL_PURCHASES > 5000 THEN 'GOLD'
        ELSE 'STANDARD'
    END as CUSTOMER_TIER
FROM CUSTOMERS

-- Caching Strategies
-- Static cache for reference data
CACHE_SIZE = 100000000  -- 100MB
CACHE_TYPE = STATIC

-- Dynamic cache for lookups
CACHE_TYPE = DYNAMIC
CACHE_PERSISTENCE = PERSISTENT

-- Bulk Loading
-- Use database-specific bulk load utilities
TARGET_LOAD_TYPE = BULK
BULK_LOAD_COMMAND = sqlldr userid=user/pass@db control=customer.ctl
```

## 8. Real-time Processing
```xml
<!-- PowerExchange Real-time -->
<REAL_TIME_SESSION NAME="RT_CUSTOMER_CHANGES">
    <SOURCE TYPE="POWEREXCHANGE_REALTIME">
        <CONNECTION>PWX_ORACLE_CDC</CONNECTION>
        <CAPTURE_MODE>CHANGE_DATA_CAPTURE</CAPTURE_MODE>
    </SOURCE>
    
    <TARGET TYPE="JMS_QUEUE">
        <CONNECTION>CUSTOMER_CHANGES_QUEUE</CONNECTION>
        <MESSAGE_FORMAT>XML</MESSAGE_FORMAT>
    </TARGET>
</REAL_TIME_SESSION>

<!-- Streaming Transformations -->
<MAPPING NAME="m_RT_CUSTOMER_PROCESSING" TYPE="STREAMING">
    <TRANSFORMATION TYPE="EXPRESSION">
        <LOGIC>
            CHANGE_TYPE = IIF(OPCOD = 'I', 'INSERT',
                         IIF(OPCOD = 'U', 'UPDATE', 'DELETE'))
            PROCESSING_TIME = SYSTIMESTAMP()
        </LOGIC>
    </TRANSFORMATION>
</MAPPING>
```

## 9. Data Integration Patterns
```sql
-- Full Load Pattern
TRUNCATE TABLE CUSTOMER_STAGING;

INSERT INTO CUSTOMER_STAGING
SELECT * FROM SOURCE_CUSTOMERS;

MERGE INTO CUSTOMER_DIM cd
USING CUSTOMER_STAGING cs ON (cd.CUSTOMER_ID = cs.CUSTOMER_ID)
WHEN MATCHED THEN
    UPDATE SET 
        cd.CUSTOMER_NAME = cs.CUSTOMER_NAME,
        cd.EMAIL = cs.EMAIL,
        cd.LAST_UPDATED = SYSDATE
WHEN NOT MATCHED THEN
    INSERT (CUSTOMER_KEY, CUSTOMER_ID, CUSTOMER_NAME, EMAIL, CREATED_DATE)
    VALUES (CUSTOMER_DIM_SEQ.NEXTVAL, cs.CUSTOMER_ID, cs.CUSTOMER_NAME, cs.EMAIL, SYSDATE);

-- Incremental Load Pattern
-- Delta detection using timestamps
SELECT *
FROM SOURCE_CUSTOMERS
WHERE LAST_MODIFIED_DATE > $$LAST_EXTRACT_DATE

-- Change Data Capture (CDC)
-- Track changes using database logs
SELECT 
    CUSTOMER_ID,
    CUSTOMER_NAME,
    EMAIL,
    OPERATION_TYPE,  -- I/U/D
    CHANGE_TIMESTAMP
FROM CDC_CUSTOMER_CHANGES
WHERE CHANGE_TIMESTAMP > $$LAST_CDC_TIMESTAMP
```

## 10. Monitoring and Administration
```sql
-- Session Statistics
SELECT 
    WORKFLOW_NAME,
    SESSION_NAME,
    START_TIME,
    END_TIME,
    (END_TIME - START_TIME) * 24 * 60 as DURATION_MINUTES,
    ROWS_SUCCESS,
    ROWS_FAILED,
    STATUS
FROM REP_SESS_LOG
WHERE START_TIME >= SYSDATE - 7
ORDER BY START_TIME DESC;

-- Performance Monitoring
SELECT 
    MAPPING_NAME,
    TRANSFORMATION_NAME,
    PARTITION_NAME,
    ROWS_IN,
    ROWS_OUT,
    THROUGHPUT_ROWS_PER_SEC
FROM REP_SESS_TFM_INST
WHERE SESSION_LOG_ID = :SESSION_LOG_ID;

-- Repository Queries
-- Find mappings using specific source
SELECT DISTINCT
    FOLDER_NAME,
    MAPPING_NAME
FROM REP_ALL_MAPPINGS m
JOIN REP_ALL_SOURCES s ON m.MAPPING_ID = s.MAPPING_ID
WHERE s.SOURCE_NAME = 'CUSTOMERS';

-- Lineage Analysis
SELECT 
    SOURCE_TABLE,
    TARGET_TABLE,
    MAPPING_NAME,
    TRANSFORMATION_PATH
FROM REP_LINEAGE_VIEW
WHERE SOURCE_TABLE = 'CUSTOMERS'
   OR TARGET_TABLE = 'CUSTOMER_DIM';

-- Workflow Dependencies
SELECT 
    PARENT_WORKFLOW,
    CHILD_WORKFLOW,
    DEPENDENCY_TYPE
FROM REP_WORKFLOW_DEPENDENCIES
WHERE PARENT_WORKFLOW = 'DAILY_CUSTOMER_ETL';
```