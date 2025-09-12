# Oracle Database Interview Questions for Data Engineers

## Basic Level Questions

### 1. What is Oracle Database and its key features for data engineering?
**Answer**: Oracle Database is an enterprise-grade RDBMS with advanced features:
- **Multi-model Database**: Supports relational, JSON, XML, spatial data
- **Advanced Analytics**: Built-in machine learning, statistical functions
- **Partitioning**: Advanced partitioning strategies for large datasets
- **Real Application Clusters (RAC)**: High availability clustering
- **Data Guard**: Disaster recovery and standby databases

```sql
-- Example: Creating a partitioned table for data engineering
CREATE TABLE sales_data (
    sale_id NUMBER,
    sale_date DATE,
    customer_id NUMBER,
    product_id NUMBER,
    amount NUMBER(10,2),
    region VARCHAR2(50)
)
PARTITION BY RANGE (sale_date) (
    PARTITION p2023_q1 VALUES LESS THAN (DATE '2023-04-01'),
    PARTITION p2023_q2 VALUES LESS THAN (DATE '2023-07-01'),
    PARTITION p2023_q3 VALUES LESS THAN (DATE '2023-10-01'),
    PARTITION p2023_q4 VALUES LESS THAN (DATE '2024-01-01')
);
```

### 2. Explain Oracle data types commonly used in data engineering
**Answer**: Key Oracle data types for data engineering:
- **NUMBER**: Precise numeric data with scale and precision
- **VARCHAR2**: Variable-length character data
- **DATE/TIMESTAMP**: Date and time data with timezone support
- **CLOB/BLOB**: Large objects for text and binary data
- **JSON**: Native JSON data type (Oracle 21c+)

```sql
CREATE TABLE customer_data (
    customer_id NUMBER(10) PRIMARY KEY,
    email VARCHAR2(255) NOT NULL,
    registration_date DATE,
    last_login TIMESTAMP WITH TIME ZONE,
    profile_data CLOB CHECK (profile_data IS JSON),
    total_spent NUMBER(12,2) DEFAULT 0
);

-- Working with JSON data
INSERT INTO customer_data (customer_id, email, profile_data)
VALUES (1, 'john@example.com', 
        '{"name": "John Doe", "preferences": {"theme": "dark"}}');
```

### 3. What are Oracle tablespaces and how are they used?
**Answer**: Tablespaces are logical storage units that group related data files:
- **System Tablespace**: Contains data dictionary
- **User Tablespaces**: Store application data
- **Temporary Tablespace**: For sorting and temporary operations
- **Undo Tablespace**: For transaction rollback

```sql
-- Create tablespace for data warehouse
CREATE TABLESPACE dwh_data
DATAFILE '/u01/app/oracle/oradata/dwh_data01.dbf' SIZE 1G
AUTOEXTEND ON NEXT 100M MAXSIZE 10G
EXTENT MANAGEMENT LOCAL
SEGMENT SPACE MANAGEMENT AUTO;

-- Create table in specific tablespace
CREATE TABLE fact_sales (
    sale_id NUMBER,
    date_key NUMBER,
    customer_key NUMBER,
    product_key NUMBER,
    quantity NUMBER,
    revenue NUMBER(10,2)
) TABLESPACE dwh_data;
```

### 4. How do you handle NULL values in Oracle?
**Answer**: Oracle NULL handling techniques:
- **NVL/NVL2**: Replace NULL with default values
- **COALESCE**: Return first non-NULL value
- **NULLIF**: Convert values to NULL
- **IS NULL/IS NOT NULL**: NULL comparisons

```sql
-- NULL handling examples
SELECT 
    customer_id,
    NVL(phone, 'No Phone') as contact_phone,
    NVL2(email, 'Has Email', 'No Email') as email_status,
    COALESCE(mobile, phone, email, 'No Contact') as best_contact,
    NULLIF(status, 'UNKNOWN') as clean_status
FROM customers
WHERE email IS NOT NULL;

-- Handle NULLs in aggregations
SELECT 
    region,
    COUNT(*) as total_customers,
    COUNT(phone) as customers_with_phone,
    AVG(NVL(age, 0)) as avg_age_with_default
FROM customers
GROUP BY region;
```

### 5. Explain Oracle indexing strategies
**Answer**: Oracle index types and strategies:
- **B-tree Index**: Default index type for most queries
- **Bitmap Index**: For low-cardinality columns in data warehouses
- **Function-based Index**: Index on expressions or functions
- **Partitioned Index**: Indexes on partitioned tables

```sql
-- Create various index types
CREATE INDEX idx_customer_email ON customers(email);
CREATE BITMAP INDEX idx_product_category ON products(category);
CREATE INDEX idx_upper_lastname ON customers(UPPER(last_name));

-- Composite index for data warehouse queries
CREATE INDEX idx_sales_analysis ON sales_data(region, sale_date, product_id);

-- Analyze index usage
SELECT * FROM USER_INDEXES WHERE table_name = 'SALES_DATA';
```

## Intermediate Level Questions

### 6. How do you optimize Oracle queries for large datasets?
**Answer**: Oracle query optimization techniques:
- **Execution Plans**: Use EXPLAIN PLAN and AUTOTRACE
- **Hints**: Guide optimizer decisions
- **Statistics**: Keep table and index statistics current
- **Partitioning**: Partition pruning for large tables

```sql
-- Analyze execution plan
EXPLAIN PLAN FOR
SELECT /*+ USE_INDEX(s, idx_sales_analysis) */
    s.region,
    SUM(s.amount) as total_sales,
    COUNT(*) as order_count
FROM sales_data s
WHERE s.sale_date BETWEEN DATE '2023-01-01' AND DATE '2023-12-31'
GROUP BY s.region;

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);

-- Update statistics for better optimization
BEGIN
    DBMS_STATS.GATHER_TABLE_STATS(
        ownname => 'HR',
        tabname => 'SALES_DATA',
        estimate_percent => DBMS_STATS.AUTO_SAMPLE_SIZE,
        cascade => TRUE
    );
END;
/

-- Partitioned query with partition pruning
SELECT /*+ PARALLEL(4) */
    region,
    SUM(amount) as total_sales
FROM sales_data
WHERE sale_date >= DATE '2023-10-01'  -- This will prune partitions
GROUP BY region;
```

### 7. Explain Oracle partitioning strategies for data engineering
**Answer**: Oracle partitioning types and benefits:
- **Range Partitioning**: Based on value ranges (dates, numbers)
- **List Partitioning**: Based on discrete values
- **Hash Partitioning**: Even distribution across partitions
- **Composite Partitioning**: Combination of partitioning methods

```sql
-- Range partitioning by date
CREATE TABLE transaction_log (
    transaction_id NUMBER,
    transaction_date DATE,
    customer_id NUMBER,
    amount NUMBER(10,2),
    status VARCHAR2(20)
)
PARTITION BY RANGE (transaction_date) (
    PARTITION p_2023_01 VALUES LESS THAN (DATE '2023-02-01'),
    PARTITION p_2023_02 VALUES LESS THAN (DATE '2023-03-01'),
    PARTITION p_2023_03 VALUES LESS THAN (DATE '2023-04-01')
);

-- Hash partitioning for even distribution
CREATE TABLE user_sessions (
    session_id VARCHAR2(64),
    user_id NUMBER,
    created_at TIMESTAMP,
    session_data CLOB
)
PARTITION BY HASH (user_id) PARTITIONS 8;

-- Composite partitioning (Range-Hash)
CREATE TABLE sales_fact (
    sale_id NUMBER,
    sale_date DATE,
    customer_id NUMBER,
    product_id NUMBER,
    amount NUMBER(10,2)
)
PARTITION BY RANGE (sale_date)
SUBPARTITION BY HASH (customer_id) SUBPARTITIONS 4 (
    PARTITION p_2023_q1 VALUES LESS THAN (DATE '2023-04-01'),
    PARTITION p_2023_q2 VALUES LESS THAN (DATE '2023-07-01')
);
```

### 8. How do you implement data loading strategies in Oracle?
**Answer**: Oracle data loading methods:
- **SQL*Loader**: High-performance bulk loading
- **External Tables**: Query files as tables
- **Data Pump**: Export/import utilities
- **INSERT with APPEND hint**: Direct path inserts

```sql
-- External table for CSV data loading
CREATE TABLE ext_sales_data (
    sale_id NUMBER,
    sale_date DATE,
    customer_id NUMBER,
    amount NUMBER(10,2)
)
ORGANIZATION EXTERNAL (
    TYPE ORACLE_LOADER
    DEFAULT DIRECTORY data_dir
    ACCESS PARAMETERS (
        RECORDS DELIMITED BY NEWLINE
        FIELDS TERMINATED BY ','
        MISSING FIELD VALUES ARE NULL
        (sale_id, sale_date DATE "YYYY-MM-DD", customer_id, amount)
    )
    LOCATION ('sales_data.csv')
);

-- Load data using external table
INSERT /*+ APPEND */ INTO sales_data
SELECT * FROM ext_sales_data;
COMMIT;

-- SQL*Loader control file example
-- sales_data.ctl
LOAD DATA
INFILE 'sales_data.csv'
INTO TABLE sales_data
FIELDS TERMINATED BY ','
TRAILING NULLCOLS
(
    sale_id,
    sale_date DATE "YYYY-MM-DD",
    customer_id,
    amount
);
```

### 9. How do you handle Oracle PL/SQL for data processing?
**Answer**: PL/SQL for data engineering tasks:
- **Stored Procedures**: Encapsulate business logic
- **Functions**: Reusable calculations
- **Packages**: Group related procedures and functions
- **Bulk Operations**: Process large datasets efficiently

```sql
-- Data processing procedure
CREATE OR REPLACE PROCEDURE process_daily_sales(p_date DATE)
IS
    v_total_sales NUMBER;
    v_record_count NUMBER;
BEGIN
    -- Process sales data for specific date
    INSERT INTO daily_sales_summary (
        summary_date,
        total_revenue,
        order_count,
        avg_order_value,
        created_at
    )
    SELECT 
        p_date,
        SUM(amount),
        COUNT(*),
        AVG(amount),
        SYSDATE
    FROM sales_data
    WHERE TRUNC(sale_date) = p_date;
    
    v_record_count := SQL%ROWCOUNT;
    
    -- Log processing results
    INSERT INTO process_log (
        process_name,
        process_date,
        records_processed,
        status,
        log_timestamp
    ) VALUES (
        'DAILY_SALES_PROCESSING',
        p_date,
        v_record_count,
        'SUCCESS',
        SYSDATE
    );
    
    COMMIT;
    
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        INSERT INTO process_log (
            process_name,
            process_date,
            status,
            error_message,
            log_timestamp
        ) VALUES (
            'DAILY_SALES_PROCESSING',
            p_date,
            'ERROR',
            SQLERRM,
            SYSDATE
        );
        COMMIT;
        RAISE;
END;
/

-- Bulk processing with FORALL
CREATE OR REPLACE PROCEDURE bulk_update_customer_status
IS
    TYPE customer_array IS TABLE OF customers.customer_id%TYPE;
    TYPE status_array IS TABLE OF customers.status%TYPE;
    
    l_customer_ids customer_array;
    l_new_status status_array;
BEGIN
    -- Collect data to process
    SELECT customer_id, 
           CASE WHEN last_order_date < SYSDATE - 365 THEN 'INACTIVE'
                ELSE 'ACTIVE' END
    BULK COLLECT INTO l_customer_ids, l_new_status
    FROM customers;
    
    -- Bulk update
    FORALL i IN 1..l_customer_ids.COUNT
        UPDATE customers
        SET status = l_new_status(i),
            last_updated = SYSDATE
        WHERE customer_id = l_customer_ids(i);
    
    COMMIT;
END;
/
```

### 10. How do you implement Oracle materialized views for data warehousing?
**Answer**: Materialized views for performance optimization:
- **Complete Refresh**: Full rebuild of materialized view
- **Fast Refresh**: Incremental updates using logs
- **On Demand/On Commit**: Refresh timing strategies
- **Query Rewrite**: Automatic use of materialized views

```sql
-- Create materialized view log for fast refresh
CREATE MATERIALIZED VIEW LOG ON sales_data
WITH ROWID, SEQUENCE (sale_date, region, product_id, amount)
INCLUDING NEW VALUES;

-- Create materialized view with fast refresh
CREATE MATERIALIZED VIEW mv_monthly_sales
BUILD IMMEDIATE
REFRESH FAST ON DEMAND
ENABLE QUERY REWRITE
AS
SELECT 
    TRUNC(sale_date, 'MM') as month_year,
    region,
    product_id,
    SUM(amount) as total_sales,
    COUNT(*) as order_count,
    COUNT(DISTINCT customer_id) as unique_customers
FROM sales_data
GROUP BY TRUNC(sale_date, 'MM'), region, product_id;

-- Refresh materialized view
BEGIN
    DBMS_MVIEW.REFRESH('MV_MONTHLY_SALES', 'F');
END;
/

-- Check materialized view refresh status
SELECT 
    mview_name,
    last_refresh_date,
    refresh_method,
    fast_refreshable
FROM user_mviews;
```

## Advanced Level Questions

### 11. How do you implement Oracle Advanced Analytics for data engineering?
**Answer**: Oracle Advanced Analytics features:
- **SQL Model Clause**: Advanced analytical calculations
- **Analytic Functions**: Window functions for complex analysis
- **Oracle Machine Learning**: Built-in ML algorithms
- **Statistical Functions**: Advanced statistical analysis

```sql
-- Advanced analytics with MODEL clause
SELECT 
    region,
    month_year,
    actual_sales,
    predicted_sales
FROM (
    SELECT region, month_year, SUM(amount) as sales
    FROM sales_data
    GROUP BY region, TRUNC(sale_date, 'MM')
)
MODEL
    PARTITION BY (region)
    DIMENSION BY (month_year)
    MEASURES (sales as actual_sales, 0 as predicted_sales)
    RULES (
        predicted_sales[ANY] = AVG(actual_sales)[month_year BETWEEN 
                               PRESENTV(month_year, 1, month_year[CV()-3]) 
                               AND month_year[CV()-1]]
    );

-- Window functions for advanced analysis
SELECT 
    customer_id,
    order_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_total,
    LAG(amount, 1) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as previous_order_amount,
    PERCENT_RANK() OVER (
        PARTITION BY TRUNC(order_date, 'MM')
        ORDER BY amount
    ) as percentile_rank
FROM orders;

-- Oracle Machine Learning example
BEGIN
    -- Create and train a regression model
    DBMS_DATA_MINING.CREATE_MODEL(
        model_name => 'SALES_PREDICTION_MODEL',
        mining_function => DBMS_DATA_MINING.REGRESSION,
        data_table_name => 'SALES_TRAINING_DATA',
        case_id_column_name => 'CUSTOMER_ID',
        target_column_name => 'SALES_AMOUNT'
    );
END;
/
```

### 12. How do you implement Oracle Data Guard for disaster recovery?
**Answer**: Oracle Data Guard configuration:
- **Physical Standby**: Exact copy of primary database
- **Logical Standby**: Logical replica with SQL apply
- **Snapshot Standby**: Read-write standby for testing
- **Fast-Start Failover**: Automatic failover capability

```sql
-- Configure Data Guard on primary database
ALTER DATABASE FORCE LOGGING;
ALTER DATABASE ADD STANDBY LOGFILE GROUP 4 SIZE 100M;
ALTER DATABASE ADD STANDBY LOGFILE GROUP 5 SIZE 100M;

-- Set Data Guard parameters
ALTER SYSTEM SET LOG_ARCHIVE_CONFIG='DG_CONFIG=(primary,standby)';
ALTER SYSTEM SET LOG_ARCHIVE_DEST_1='LOCATION=/u01/app/oracle/archive VALID_FOR=(ALL_LOGFILES,ALL_ROLES) DB_UNIQUE_NAME=primary';
ALTER SYSTEM SET LOG_ARCHIVE_DEST_2='SERVICE=standby ASYNC VALID_FOR=(ONLINE_LOGFILES,PRIMARY_ROLE) DB_UNIQUE_NAME=standby';
ALTER SYSTEM SET LOG_ARCHIVE_DEST_STATE_2=ENABLE;
ALTER SYSTEM SET REMOTE_LOGIN_PASSWORDFILE=EXCLUSIVE;
ALTER SYSTEM SET LOG_ARCHIVE_FORMAT='%t_%s_%r.arc';
ALTER SYSTEM SET LOG_ARCHIVE_MAX_PROCESSES=30;
ALTER SYSTEM SET FAL_SERVER=standby;
ALTER SYSTEM SET FAL_CLIENT=primary;

-- Monitor Data Guard status
SELECT 
    dest_id,
    status,
    destination,
    error
FROM v$archive_dest
WHERE dest_id <= 2;

-- Check log apply status on standby
SELECT 
    sequence#,
    applied,
    completion_time
FROM v$archived_log
WHERE dest_id = 1
ORDER BY sequence# DESC;
```

### 13. How do you implement Oracle Real Application Clusters (RAC)?
**Answer**: Oracle RAC for high availability and scalability:
- **Shared Storage**: All nodes access same database files
- **Cache Fusion**: Inter-node data block transfers
- **Load Balancing**: Distribute connections across nodes
- **Failover**: Automatic failover to surviving nodes

```sql
-- RAC-specific monitoring queries
SELECT 
    inst_id,
    instance_name,
    status,
    startup_time
FROM gv$instance
ORDER BY inst_id;

-- Check cluster interconnect performance
SELECT 
    name,
    value
FROM gv$sysstat
WHERE name LIKE '%gc%'
AND inst_id = 1;

-- RAC-aware connection string
-- tnsnames.ora entry
RACDB =
  (DESCRIPTION =
    (ADDRESS_LIST =
      (ADDRESS = (PROTOCOL = TCP)(HOST = rac1-vip)(PORT = 1521))
      (ADDRESS = (PROTOCOL = TCP)(HOST = rac2-vip)(PORT = 1521))
    )
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = racdb.example.com)
      (FAILOVER_MODE =
        (TYPE = SELECT)
        (METHOD = BASIC)
        (RETRIES = 180)
        (DELAY = 5)
      )
    )
  )

-- Application-level load balancing
ALTER SYSTEM SET REMOTE_LISTENER='rac-scan:1521';
```

### 14. How do you implement Oracle Automatic Workload Management?
**Answer**: Oracle Resource Manager and workload management:
- **Resource Plans**: Define resource allocation policies
- **Consumer Groups**: Group sessions with similar requirements
- **Automatic Workload Repository (AWR)**: Performance monitoring
- **SQL Plan Management**: Stable execution plans

```sql
-- Create resource plan for data warehouse
BEGIN
    DBMS_RESOURCE_MANAGER.CREATE_PLAN(
        plan => 'DWH_PLAN',
        comment => 'Data Warehouse Resource Plan'
    );
    
    -- Create consumer groups
    DBMS_RESOURCE_MANAGER.CREATE_CONSUMER_GROUP(
        consumer_group => 'ETL_GROUP',
        comment => 'ETL Processing Group'
    );
    
    DBMS_RESOURCE_MANAGER.CREATE_CONSUMER_GROUP(
        consumer_group => 'REPORTING_GROUP',
        comment => 'Reporting and Analytics Group'
    );
    
    -- Create plan directives
    DBMS_RESOURCE_MANAGER.CREATE_PLAN_DIRECTIVE(
        plan => 'DWH_PLAN',
        group_or_subplan => 'ETL_GROUP',
        comment => 'ETL Resource Allocation',
        cpu_p1 => 70,
        parallel_degree_limit_p1 => 8
    );
    
    DBMS_RESOURCE_MANAGER.CREATE_PLAN_DIRECTIVE(
        plan => 'DWH_PLAN',
        group_or_subplan => 'REPORTING_GROUP',
        comment => 'Reporting Resource Allocation',
        cpu_p1 => 30,
        parallel_degree_limit_p1 => 4
    );
    
    -- Activate the plan
    DBMS_RESOURCE_MANAGER.VALIDATE_PLAN('DWH_PLAN');
END;
/

-- Set resource plan
ALTER SYSTEM SET RESOURCE_MANAGER_PLAN = 'DWH_PLAN';

-- Assign users to consumer groups
BEGIN
    DBMS_RESOURCE_MANAGER_PRIVS.GRANT_SWITCH_CONSUMER_GROUP(
        grantee_name => 'ETL_USER',
        consumer_group => 'ETL_GROUP',
        grant_option => FALSE
    );
END;
/
```

### 15. How do you implement Oracle In-Memory for analytical workloads?
**Answer**: Oracle Database In-Memory features:
- **Columnar Storage**: Optimized for analytical queries
- **Vector Processing**: SIMD operations for fast scans
- **In-Memory Aggregation**: Fast GROUP BY operations
- **Automatic Data Optimization**: Intelligent data placement

```sql
-- Enable In-Memory column store
ALTER SYSTEM SET INMEMORY_SIZE = 2G;

-- Configure table for In-Memory
ALTER TABLE sales_data INMEMORY;
ALTER TABLE customers INMEMORY PRIORITY HIGH;

-- Configure specific columns
ALTER TABLE products INMEMORY (product_name, category, price) NO INMEMORY (description);

-- Monitor In-Memory usage
SELECT 
    segment_name,
    bytes,
    inmemory_size,
    inmemory_compression
FROM v$im_segments;

-- In-Memory advisor recommendations
SELECT 
    sql_id,
    parsing_schema_name,
    sql_text,
    benefit_ratio
FROM dba_advisor_recommendations
WHERE advisor_name = 'INMEMORY_ADVISOR'
ORDER BY benefit_ratio DESC;

-- Force In-Memory population
ALTER TABLE sales_data INMEMORY PRIORITY CRITICAL;

-- Query with In-Memory optimization
SELECT /*+ INMEMORY */
    region,
    product_category,
    SUM(sales_amount) as total_sales,
    COUNT(*) as transaction_count
FROM sales_data s
JOIN products p ON s.product_id = p.product_id
WHERE s.sale_date >= DATE '2023-01-01'
GROUP BY region, product_category;
```

## Data Engineering Specific Questions

### 16. How do you implement slowly changing dimensions (SCD) in Oracle?
**Answer**: SCD implementation using Oracle features:

```sql
-- SCD Type 2 with Oracle features
CREATE TABLE dim_customer (
    customer_key NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id NUMBER NOT NULL,
    customer_name VARCHAR2(100),
    email VARCHAR2(255),
    city VARCHAR2(50),
    effective_date DATE DEFAULT SYSDATE,
    expiry_date DATE DEFAULT DATE '9999-12-31',
    is_current CHAR(1) DEFAULT 'Y',
    version_number NUMBER DEFAULT 1
);

-- SCD Type 2 merge procedure
CREATE OR REPLACE PROCEDURE update_customer_scd(
    p_customer_id NUMBER,
    p_customer_name VARCHAR2,
    p_email VARCHAR2,
    p_city VARCHAR2
)
IS
BEGIN
    -- Update existing current record
    UPDATE dim_customer
    SET expiry_date = SYSDATE - 1,
        is_current = 'N'
    WHERE customer_id = p_customer_id
    AND is_current = 'Y';
    
    -- Insert new current record
    INSERT INTO dim_customer (
        customer_id, customer_name, email, city,
        effective_date, version_number
    )
    SELECT 
        p_customer_id, p_customer_name, p_email, p_city,
        SYSDATE,
        NVL(MAX(version_number), 0) + 1
    FROM dim_customer
    WHERE customer_id = p_customer_id;
    
    COMMIT;
END;
/
```

### 17. How do you implement data quality frameworks in Oracle?
**Answer**: Comprehensive data quality implementation:

```sql
-- Data quality rules framework
CREATE TABLE dq_rules (
    rule_id NUMBER PRIMARY KEY,
    table_name VARCHAR2(128),
    column_name VARCHAR2(128),
    rule_type VARCHAR2(50),
    rule_expression CLOB,
    severity VARCHAR2(20),
    is_active CHAR(1) DEFAULT 'Y'
);

-- Data quality results tracking
CREATE TABLE dq_results (
    result_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    rule_id NUMBER,
    execution_date DATE,
    records_checked NUMBER,
    records_failed NUMBER,
    failure_rate NUMBER(5,2),
    status VARCHAR2(20),
    error_details CLOB
);

-- Data quality execution procedure
CREATE OR REPLACE PROCEDURE execute_data_quality_checks(
    p_table_name VARCHAR2 DEFAULT NULL
)
IS
    CURSOR rule_cursor IS
        SELECT rule_id, table_name, column_name, rule_type, rule_expression
        FROM dq_rules
        WHERE is_active = 'Y'
        AND (p_table_name IS NULL OR table_name = p_table_name);
    
    v_sql CLOB;
    v_count NUMBER;
    v_total_records NUMBER;
    v_failure_rate NUMBER;
BEGIN
    FOR rule_rec IN rule_cursor LOOP
        -- Build dynamic SQL based on rule type
        CASE rule_rec.rule_type
            WHEN 'NOT_NULL' THEN
                v_sql := 'SELECT COUNT(*) FROM ' || rule_rec.table_name || 
                        ' WHERE ' || rule_rec.column_name || ' IS NULL';
            WHEN 'UNIQUE' THEN
                v_sql := 'SELECT COUNT(*) - COUNT(DISTINCT ' || rule_rec.column_name || 
                        ') FROM ' || rule_rec.table_name;
            WHEN 'CUSTOM' THEN
                v_sql := rule_rec.rule_expression;
        END CASE;
        
        -- Execute quality check
        EXECUTE IMMEDIATE v_sql INTO v_count;
        
        -- Get total record count
        EXECUTE IMMEDIATE 'SELECT COUNT(*) FROM ' || rule_rec.table_name INTO v_total_records;
        
        -- Calculate failure rate
        v_failure_rate := CASE WHEN v_total_records > 0 THEN (v_count / v_total_records) * 100 ELSE 0 END;
        
        -- Log results
        INSERT INTO dq_results (
            rule_id, execution_date, records_checked, 
            records_failed, failure_rate, status
        ) VALUES (
            rule_rec.rule_id, SYSDATE, v_total_records,
            v_count, v_failure_rate,
            CASE WHEN v_count = 0 THEN 'PASS' ELSE 'FAIL' END
        );
    END LOOP;
    
    COMMIT;
END;
/
```

### 18. How do you implement Oracle GoldenGate for real-time data integration?
**Answer**: GoldenGate configuration for CDC and replication:

```sql
-- Enable supplemental logging for GoldenGate
ALTER DATABASE ADD SUPPLEMENTAL LOG DATA;
ALTER DATABASE ADD SUPPLEMENTAL LOG DATA (PRIMARY KEY, UNIQUE) COLUMNS;

-- Table-level supplemental logging
ALTER TABLE sales_data ADD SUPPLEMENTAL LOG DATA (ALL) COLUMNS;

-- GoldenGate extract configuration
-- extract.prm
EXTRACT ext_sales
USERID gg_user, PASSWORD gg_password
EXTTRAIL ./dirdat/es
TABLE hr.sales_data;
TABLE hr.customers;

-- GoldenGate replicat configuration  
-- replicat.prm
REPLICAT rep_sales
USERID gg_user, PASSWORD gg_password
ASSUMETARGETDEFS
MAP hr.sales_data, TARGET dwh.fact_sales,
COLMAP (USEDEFAULTS,
        sale_date = @DATENOW(),
        load_timestamp = @DATENOW());

-- Monitor GoldenGate processes
SELECT 
    extract_name,
    status,
    lag_time,
    checkpoint_time
FROM dba_goldengate_extracts;

-- GoldenGate conflict resolution
MAP hr.customers, TARGET dwh.dim_customers,
RESOLVECONFLICT (UPDATEROWEXISTS, (DEFAULT, USEMAX (last_updated)));
```

This comprehensive Oracle interview question set covers essential knowledge for data engineers working with Oracle Database, from basic concepts to advanced enterprise features and data engineering patterns.

---

## 📚 Additional Comprehensive Content

*(Merged from comprehensive interview questions file)*

