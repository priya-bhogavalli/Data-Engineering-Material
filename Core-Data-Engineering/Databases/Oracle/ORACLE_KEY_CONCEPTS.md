# Oracle Database Key Concepts

## 🏢 Real-World Analogy: Oracle as a Premium Enterprise Library System

> **Think of Oracle Database as a world-class enterprise library system with premium services, advanced security, and sophisticated management capabilities**

### 🎯 **The Analogy**
Oracle Database is like a premium enterprise library system that serves large corporations and government institutions. Just as a premium library offers advanced services, specialized collections, and enterprise-grade security, Oracle provides comprehensive database services with advanced features for mission-critical applications.

### 🔗 **Technical Mapping**
| Oracle Concept | Library Equivalent | Why This Works |
|----------------|-------------------|----------------|
| **Instance** | Library management system with staff | Active operations and memory management |
| **Database** | Physical library building and collections | Actual data storage and organization |
| **SGA (System Global Area)** | Shared library resources (reading rooms, catalogs) | Shared memory for all users |
| **PGA (Program Global Area)** | Personal study spaces for each visitor | Private memory for each session |
| **Tablespaces** | Different library wings (Science, History, Fiction) | Logical storage organization |
| **Data Files** | Physical book storage shelves | Actual file storage on disk |
| **PL/SQL** | Library automation system with custom procedures | Stored procedures and business logic |
| **Partitioning** | Organized sections by date/topic | Dividing large tables for performance |
| **RAC (Real Application Clusters)** | Multiple library branches sharing same catalog | Multiple instances accessing same database |

### 💼 **Business Value**
- **Enterprise-Grade**: Like a premium library system, Oracle handles the most demanding enterprise workloads
- **Advanced Features**: Sophisticated capabilities like a research library with specialized services
- **High Availability**: Multiple redundancy systems like backup library locations
- **Security**: Bank-level security features for protecting sensitive data
- **Scalability**: Can grow from departmental to global enterprise scale

---

## 1. Oracle Architecture
**Core Components**:
- **Instance**: Memory structures and background processes
- **Database**: Physical files storing data
- **SGA (System Global Area)**: Shared memory region
- **PGA (Program Global Area)**: Private memory for sessions
- **Tablespaces**: Logical storage units
- **Data Files**: Physical storage files

```sql
-- Check instance information
SELECT instance_name, status, database_status FROM v$instance;

-- View memory components
SELECT component, current_size/1024/1024 as size_mb 
FROM v$memory_dynamic_components;

-- Check tablespace usage
SELECT 
    tablespace_name,
    ROUND(bytes/1024/1024, 2) as size_mb,
    ROUND(maxbytes/1024/1024, 2) as max_size_mb
FROM dba_data_files
ORDER BY tablespace_name;
```

## 2. Data Types and Storage
```sql
-- Numeric types
CREATE TABLE products (
    id NUMBER(10) PRIMARY KEY,
    price NUMBER(10,2) NOT NULL,
    quantity NUMBER(8) DEFAULT 0,
    weight BINARY_FLOAT,
    is_active NUMBER(1) CHECK (is_active IN (0,1))
);

-- Character types
CREATE TABLE customers (
    id NUMBER(10) PRIMARY KEY,
    name VARCHAR2(100) NOT NULL,
    email VARCHAR2(255) UNIQUE,
    description CLOB,
    status CHAR(1) DEFAULT 'A'
);

-- Date and timestamp types
CREATE TABLE orders (
    id NUMBER(10) PRIMARY KEY,
    order_date DATE DEFAULT SYSDATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    delivery_window INTERVAL DAY(2) TO SECOND(6)
);

-- LOB types
CREATE TABLE documents (
    id NUMBER(10) PRIMARY KEY,
    document_name VARCHAR2(255),
    document_content BLOB,
    metadata CLOB,
    xml_data XMLTYPE
);

-- Collections (Nested Tables and VARRAYs)
CREATE TYPE phone_list AS VARRAY(5) OF VARCHAR2(20);
CREATE TYPE address_type AS OBJECT (
    street VARCHAR2(100),
    city VARCHAR2(50),
    postal_code VARCHAR2(10)
);

CREATE TABLE customers_extended (
    id NUMBER(10) PRIMARY KEY,
    name VARCHAR2(100),
    phones phone_list,
    address address_type
);
```

## 3. Advanced SQL Features
```sql
-- Hierarchical queries
SELECT 
    employee_id,
    name,
    manager_id,
    LEVEL,
    SYS_CONNECT_BY_PATH(name, '/') as hierarchy_path
FROM employees
START WITH manager_id IS NULL
CONNECT BY PRIOR employee_id = manager_id
ORDER SIBLINGS BY name;

-- Analytic functions
SELECT 
    employee_id,
    department_id,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) as rank,
    DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank,
    LAG(salary, 1) OVER (PARTITION BY department_id ORDER BY salary) as prev_salary,
    SUM(salary) OVER (PARTITION BY department_id) as dept_total,
    RATIO_TO_REPORT(salary) OVER (PARTITION BY department_id) as salary_ratio
FROM employees;

-- Model clause for calculations
SELECT 
    year,
    sales,
    predicted_sales
FROM sales_data
MODEL
    PARTITION BY (region)
    DIMENSION BY (year)
    MEASURES (sales, 0 as predicted_sales)
    RULES (
        predicted_sales[2024] = sales[2023] * 1.1,
        predicted_sales[2025] = predicted_sales[2024] * 1.05
    )
ORDER BY region, year;

-- Pivot and unpivot
SELECT *
FROM (
    SELECT department, quarter, sales
    FROM quarterly_sales
)
PIVOT (
    SUM(sales)
    FOR quarter IN ('Q1' as q1, 'Q2' as q2, 'Q3' as q3, 'Q4' as q4)
);

-- Common Table Expressions (WITH clause)
WITH 
monthly_sales AS (
    SELECT 
        EXTRACT(YEAR FROM order_date) as year,
        EXTRACT(MONTH FROM order_date) as month,
        SUM(amount) as total_sales
    FROM orders
    GROUP BY EXTRACT(YEAR FROM order_date), EXTRACT(MONTH FROM order_date)
),
sales_with_growth AS (
    SELECT 
        year,
        month,
        total_sales,
        LAG(total_sales) OVER (ORDER BY year, month) as prev_month_sales,
        (total_sales - LAG(total_sales) OVER (ORDER BY year, month)) / 
        LAG(total_sales) OVER (ORDER BY year, month) * 100 as growth_rate
    FROM monthly_sales
)
SELECT * FROM sales_with_growth
WHERE growth_rate > 10;
```

## 4. PL/SQL Programming
```sql
-- Basic PL/SQL block
DECLARE
    v_customer_count NUMBER;
    v_avg_order_value NUMBER(10,2);
    v_message VARCHAR2(200);
BEGIN
    SELECT COUNT(*), AVG(order_total)
    INTO v_customer_count, v_avg_order_value
    FROM customers c
    JOIN orders o ON c.id = o.customer_id
    WHERE o.order_date >= SYSDATE - 30;
    
    v_message := 'Processed ' || v_customer_count || ' customers with avg order: $' || v_avg_order_value;
    DBMS_OUTPUT.PUT_LINE(v_message);
    
    IF v_avg_order_value > 500 THEN
        DBMS_OUTPUT.PUT_LINE('High value customers detected');
    END IF;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('No data found for the specified period');
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
END;
/

-- Stored procedures
CREATE OR REPLACE PROCEDURE process_customer_orders(
    p_customer_id IN NUMBER,
    p_start_date IN DATE DEFAULT SYSDATE - 30,
    p_end_date IN DATE DEFAULT SYSDATE,
    p_total_amount OUT NUMBER,
    p_order_count OUT NUMBER
) IS
    v_debug_mode BOOLEAN := TRUE;
BEGIN
    IF v_debug_mode THEN
        DBMS_OUTPUT.PUT_LINE('Processing customer: ' || p_customer_id);
    END IF;
    
    SELECT 
        NVL(SUM(order_total), 0),
        COUNT(*)
    INTO p_total_amount, p_order_count
    FROM orders
    WHERE customer_id = p_customer_id
    AND order_date BETWEEN p_start_date AND p_end_date;
    
    -- Update customer statistics
    UPDATE customers
    SET last_order_total = p_total_amount,
        last_processed_date = SYSDATE
    WHERE id = p_customer_id;
    
    COMMIT;
    
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        p_total_amount := 0;
        p_order_count := 0;
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE_APPLICATION_ERROR(-20001, 'Error processing customer: ' || SQLERRM);
END;
/

-- Functions
CREATE OR REPLACE FUNCTION calculate_customer_tier(
    p_customer_id IN NUMBER
) RETURN VARCHAR2 IS
    v_total_spent NUMBER;
    v_tier VARCHAR2(20);
BEGIN
    SELECT NVL(SUM(order_total), 0)
    INTO v_total_spent
    FROM orders
    WHERE customer_id = p_customer_id
    AND order_date >= ADD_MONTHS(SYSDATE, -12);
    
    CASE
        WHEN v_total_spent >= 10000 THEN v_tier := 'PLATINUM';
        WHEN v_total_spent >= 5000 THEN v_tier := 'GOLD';
        WHEN v_total_spent >= 1000 THEN v_tier := 'SILVER';
        ELSE v_tier := 'BRONZE';
    END CASE;
    
    RETURN v_tier;
END;
/

-- Packages
CREATE OR REPLACE PACKAGE customer_management IS
    -- Public declarations
    TYPE customer_rec IS RECORD (
        id NUMBER,
        name VARCHAR2(100),
        tier VARCHAR2(20),
        total_spent NUMBER
    );
    
    TYPE customer_tab IS TABLE OF customer_rec;
    
    FUNCTION get_high_value_customers RETURN customer_tab PIPELINED;
    PROCEDURE update_customer_tiers;
    PROCEDURE send_tier_notifications(p_tier IN VARCHAR2);
END customer_management;
/

CREATE OR REPLACE PACKAGE BODY customer_management IS
    FUNCTION get_high_value_customers RETURN customer_tab PIPELINED IS
        v_customer customer_rec;
    BEGIN
        FOR rec IN (
            SELECT 
                c.id,
                c.name,
                calculate_customer_tier(c.id) as tier,
                NVL(SUM(o.order_total), 0) as total_spent
            FROM customers c
            LEFT JOIN orders o ON c.id = o.customer_id
            WHERE o.order_date >= ADD_MONTHS(SYSDATE, -12)
            GROUP BY c.id, c.name
            HAVING NVL(SUM(o.order_total), 0) > 5000
        ) LOOP
            v_customer.id := rec.id;
            v_customer.name := rec.name;
            v_customer.tier := rec.tier;
            v_customer.total_spent := rec.total_spent;
            
            PIPE ROW(v_customer);
        END LOOP;
        RETURN;
    END;
    
    PROCEDURE update_customer_tiers IS
    BEGIN
        UPDATE customers
        SET tier = calculate_customer_tier(id),
            tier_updated_date = SYSDATE;
        
        COMMIT;
        DBMS_OUTPUT.PUT_LINE('Updated ' || SQL%ROWCOUNT || ' customer tiers');
    END;
    
    PROCEDURE send_tier_notifications(p_tier IN VARCHAR2) IS
    BEGIN
        FOR rec IN (SELECT * FROM customers WHERE tier = p_tier) LOOP
            -- Send notification logic here
            DBMS_OUTPUT.PUT_LINE('Notification sent to: ' || rec.name);
        END LOOP;
    END;
END customer_management;
/
```

## 5. Indexing and Performance
```sql
-- B-tree indexes
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
CREATE INDEX idx_customers_email ON customers(email);

-- Function-based indexes
CREATE INDEX idx_customers_upper_name ON customers(UPPER(name));
CREATE INDEX idx_orders_year ON orders(EXTRACT(YEAR FROM order_date));

-- Bitmap indexes (for low cardinality columns)
CREATE BITMAP INDEX idx_products_category ON products(category);
CREATE BITMAP INDEX idx_orders_status ON orders(status);

-- Partitioned indexes
CREATE INDEX idx_sales_date_local ON sales_partitioned(sale_date) LOCAL;
CREATE INDEX idx_sales_customer_global ON sales_partitioned(customer_id) GLOBAL;

-- Index monitoring
ALTER INDEX idx_orders_customer_date MONITORING USAGE;

-- Check index usage
SELECT 
    index_name,
    table_name,
    monitoring,
    used,
    start_monitoring,
    end_monitoring
FROM v$object_usage
WHERE index_name = 'IDX_ORDERS_CUSTOMER_DATE';

-- Analyze execution plans
EXPLAIN PLAN FOR
SELECT c.name, COUNT(o.id) as order_count
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE o.order_date >= SYSDATE - 30
GROUP BY c.name;

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);

-- Optimizer hints
SELECT /*+ USE_INDEX(o, idx_orders_customer_date) */
    c.name, o.order_date, o.order_total
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE o.order_date >= SYSDATE - 7;

-- Gather statistics
EXEC DBMS_STATS.GATHER_TABLE_STATS('SCHEMA_NAME', 'ORDERS');
EXEC DBMS_STATS.GATHER_SCHEMA_STATS('SCHEMA_NAME');
```

## 6. Partitioning
```sql
-- Range partitioning by date
CREATE TABLE sales_range_partitioned (
    id NUMBER,
    sale_date DATE,
    customer_id NUMBER,
    amount NUMBER(10,2)
)
PARTITION BY RANGE (sale_date) (
    PARTITION sales_2023 VALUES LESS THAN (DATE '2024-01-01'),
    PARTITION sales_2024_q1 VALUES LESS THAN (DATE '2024-04-01'),
    PARTITION sales_2024_q2 VALUES LESS THAN (DATE '2024-07-01'),
    PARTITION sales_2024_q3 VALUES LESS THAN (DATE '2024-10-01'),
    PARTITION sales_2024_q4 VALUES LESS THAN (DATE '2025-01-01')
);

-- Hash partitioning
CREATE TABLE customers_hash_partitioned (
    id NUMBER PRIMARY KEY,
    name VARCHAR2(100),
    region VARCHAR2(50)
)
PARTITION BY HASH (id)
PARTITIONS 8;

-- List partitioning
CREATE TABLE orders_list_partitioned (
    id NUMBER,
    region VARCHAR2(20),
    order_date DATE,
    amount NUMBER(10,2)
)
PARTITION BY LIST (region) (
    PARTITION north_america VALUES ('US', 'CA', 'MX'),
    PARTITION europe VALUES ('UK', 'DE', 'FR', 'IT'),
    PARTITION asia_pacific VALUES ('JP', 'AU', 'SG', 'IN'),
    PARTITION others VALUES (DEFAULT)
);

-- Composite partitioning (Range-Hash)
CREATE TABLE sales_composite (
    id NUMBER,
    sale_date DATE,
    customer_id NUMBER,
    amount NUMBER(10,2)
)
PARTITION BY RANGE (sale_date)
SUBPARTITION BY HASH (customer_id)
SUBPARTITIONS 4 (
    PARTITION sales_2024_q1 VALUES LESS THAN (DATE '2024-04-01'),
    PARTITION sales_2024_q2 VALUES LESS THAN (DATE '2024-07-01'),
    PARTITION sales_2024_q3 VALUES LESS THAN (DATE '2024-10-01'),
    PARTITION sales_2024_q4 VALUES LESS THAN (DATE '2025-01-01')
);

-- Partition maintenance
-- Add new partition
ALTER TABLE sales_range_partitioned 
ADD PARTITION sales_2025_q1 VALUES LESS THAN (DATE '2025-04-01');

-- Drop old partition
ALTER TABLE sales_range_partitioned DROP PARTITION sales_2023;

-- Split partition
ALTER TABLE sales_range_partitioned 
SPLIT PARTITION sales_2024_q4 AT (DATE '2024-11-01')
INTO (PARTITION sales_2024_oct, PARTITION sales_2024_nov_dec);

-- Partition pruning example
SELECT COUNT(*)
FROM sales_range_partitioned
WHERE sale_date BETWEEN DATE '2024-01-01' AND DATE '2024-03-31';
```

## 7. Advanced Features
```sql
-- Materialized Views
CREATE MATERIALIZED VIEW mv_customer_summary
BUILD IMMEDIATE
REFRESH FAST ON COMMIT
AS
SELECT 
    c.id,
    c.name,
    c.region,
    COUNT(o.id) as order_count,
    SUM(o.order_total) as total_spent,
    AVG(o.order_total) as avg_order_value,
    MAX(o.order_date) as last_order_date
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name, c.region;

-- Create materialized view log for fast refresh
CREATE MATERIALIZED VIEW LOG ON customers
WITH ROWID, SEQUENCE (id, name, region)
INCLUDING NEW VALUES;

CREATE MATERIALIZED VIEW LOG ON orders
WITH ROWID, SEQUENCE (id, customer_id, order_total, order_date)
INCLUDING NEW VALUES;

-- Refresh materialized view
EXEC DBMS_MVIEW.REFRESH('MV_CUSTOMER_SUMMARY', 'F');

-- Flashback features
-- Flashback query
SELECT * FROM customers
AS OF TIMESTAMP (SYSTIMESTAMP - INTERVAL '1' HOUR)
WHERE id = 12345;

-- Flashback table
FLASHBACK TABLE customers TO TIMESTAMP (SYSTIMESTAMP - INTERVAL '30' MINUTE);

-- Virtual Private Database (VPD)
CREATE OR REPLACE FUNCTION customer_security_policy(
    schema_var IN VARCHAR2,
    table_var IN VARCHAR2
) RETURN VARCHAR2 IS
    v_predicate VARCHAR2(400);
BEGIN
    -- Only show customers from user's region
    v_predicate := 'region = SYS_CONTEXT(''USERENV'', ''CLIENT_IDENTIFIER'')';
    RETURN v_predicate;
END;
/

-- Apply VPD policy
BEGIN
    DBMS_RLS.ADD_POLICY(
        object_schema => 'SALES_SCHEMA',
        object_name => 'CUSTOMERS',
        policy_name => 'CUSTOMER_REGION_POLICY',
        function_schema => 'SALES_SCHEMA',
        policy_function => 'CUSTOMER_SECURITY_POLICY',
        statement_types => 'SELECT, INSERT, UPDATE, DELETE'
    );
END;
/

-- Result Cache
SELECT /*+ RESULT_CACHE */
    region,
    COUNT(*) as customer_count,
    AVG(total_spent) as avg_spent
FROM mv_customer_summary
GROUP BY region;
```

## 8. Data Movement and Integration
```sql
-- External Tables
CREATE DIRECTORY ext_data_dir AS '/opt/oracle/external_data';

CREATE TABLE ext_sales_data (
    customer_id NUMBER,
    product_id NUMBER,
    sale_date DATE,
    amount NUMBER(10,2)
)
ORGANIZATION EXTERNAL (
    TYPE ORACLE_LOADER
    DEFAULT DIRECTORY ext_data_dir
    ACCESS PARAMETERS (
        RECORDS DELIMITED BY NEWLINE
        FIELDS TERMINATED BY ','
        OPTIONALLY ENCLOSED BY '"'
        MISSING FIELD VALUES ARE NULL
        (customer_id, product_id, sale_date DATE 'YYYY-MM-DD', amount)
    )
    LOCATION ('sales_data.csv')
)
REJECT LIMIT UNLIMITED;

-- Database Links
CREATE DATABASE LINK remote_db
CONNECT TO remote_user IDENTIFIED BY password
USING '(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=remote-host)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=remote_service)))';

-- Query remote data
SELECT * FROM customers@remote_db WHERE region = 'US';

-- Data Pump Export/Import
-- Export
EXPDP system/password DIRECTORY=data_pump_dir DUMPFILE=sales_export.dmp SCHEMAS=sales_schema

-- Import
IMPDP system/password DIRECTORY=data_pump_dir DUMPFILE=sales_export.dmp SCHEMAS=sales_schema REMAP_SCHEMA=sales_schema:new_sales_schema

-- SQL*Loader
-- Control file (sales_data.ctl)
/*
LOAD DATA
INFILE 'sales_data.csv'
INTO TABLE sales
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
    customer_id,
    product_id,
    sale_date DATE 'YYYY-MM-DD',
    amount
)
*/

-- Load data
-- sqlldr userid=username/password control=sales_data.ctl log=sales_load.log
```

## 9. Backup and Recovery
```sql
-- RMAN (Recovery Manager) commands
-- Connect to RMAN
-- rman target /

-- Full database backup
-- BACKUP DATABASE PLUS ARCHIVELOG;

-- Incremental backup
-- BACKUP INCREMENTAL LEVEL 1 DATABASE;

-- Tablespace backup
-- BACKUP TABLESPACE users;

-- Point-in-time recovery
-- RESTORE DATABASE UNTIL TIME "TO_DATE('2024-01-15 14:00:00', 'YYYY-MM-DD HH24:MI:SS')";
-- RECOVER DATABASE UNTIL TIME "TO_DATE('2024-01-15 14:00:00', 'YYYY-MM-DD HH24:MI:SS')";

-- Flashback Database
ALTER DATABASE FLASHBACK ON;

-- Flashback to specific time
FLASHBACK DATABASE TO TIMESTAMP TO_TIMESTAMP('2024-01-15 12:00:00', 'YYYY-MM-DD HH24:MI:SS');

-- User-managed backup
ALTER TABLESPACE users BEGIN BACKUP;
-- Copy datafiles using OS commands
ALTER TABLESPACE users END BACKUP;

-- Archive log management
ALTER SYSTEM ARCHIVE LOG CURRENT;
ALTER SYSTEM SWITCH LOGFILE;

-- Check backup status
SELECT 
    session_key,
    input_type,
    status,
    start_time,
    end_time,
    input_bytes/1024/1024 as input_mb,
    output_bytes/1024/1024 as output_mb
FROM v$rman_backup_job_details
WHERE start_time >= SYSDATE - 7
ORDER BY start_time DESC;
```

## 10. Monitoring and Tuning
```sql
-- AWR (Automatic Workload Repository)
-- Generate AWR report
SELECT output FROM TABLE(DBMS_WORKLOAD_REPOSITORY.AWR_REPORT_TEXT('HTML', 1, 1, 100, 101));

-- Create AWR snapshot
EXEC DBMS_WORKLOAD_REPOSITORY.CREATE_SNAPSHOT();

-- ASH (Active Session History)
SELECT 
    session_id,
    sql_id,
    event,
    wait_class,
    COUNT(*) as sample_count
FROM v$active_session_history
WHERE sample_time >= SYSDATE - 1/24  -- Last hour
GROUP BY session_id, sql_id, event, wait_class
ORDER BY sample_count DESC;

-- SQL Tuning Advisor
DECLARE
    task_name VARCHAR2(30);
    sql_text CLOB;
BEGIN
    sql_text := 'SELECT c.name, COUNT(o.id) FROM customers c JOIN orders o ON c.id = o.customer_id GROUP BY c.name';
    
    task_name := DBMS_SQLTUNE.CREATE_TUNING_TASK(
        sql_text => sql_text,
        task_name => 'tune_customer_orders'
    );
    
    DBMS_SQLTUNE.EXECUTE_TUNING_TASK(task_name);
END;
/

-- View tuning recommendations
SELECT DBMS_SQLTUNE.REPORT_TUNING_TASK('tune_customer_orders') FROM DUAL;

-- SQL Plan Management
-- Create SQL Plan Baseline
DECLARE
    plans_loaded PLS_INTEGER;
BEGIN
    plans_loaded := DBMS_SPM.LOAD_PLANS_FROM_CURSOR_CACHE(
        sql_id => 'abc123def456'
    );
    DBMS_OUTPUT.PUT_LINE('Plans loaded: ' || plans_loaded);
END;
/

-- Performance monitoring queries
-- Top SQL by CPU time
SELECT 
    sql_id,
    child_number,
    cpu_time/1000000 as cpu_seconds,
    executions,
    (cpu_time/1000000)/NULLIF(executions,0) as cpu_per_exec,
    SUBSTR(sql_text, 1, 100) as sql_text
FROM v$sql
WHERE cpu_time > 1000000  -- More than 1 second CPU time
ORDER BY cpu_time DESC;

-- Wait events
SELECT 
    event,
    total_waits,
    total_timeouts,
    time_waited/100 as time_waited_seconds,
    average_wait/100 as avg_wait_seconds
FROM v$system_event
WHERE wait_class != 'Idle'
ORDER BY time_waited DESC;

-- Session information
SELECT 
    s.sid,
    s.serial#,
    s.username,
    s.program,
    s.status,
    s.logon_time,
    p.spid as os_process_id
FROM v$session s
JOIN v$process p ON s.paddr = p.addr
WHERE s.username IS NOT NULL
ORDER BY s.logon_time DESC;

-- Tablespace usage
SELECT 
    tablespace_name,
    ROUND(used_mb, 2) as used_mb,
    ROUND(free_mb, 2) as free_mb,
    ROUND(total_mb, 2) as total_mb,
    ROUND((used_mb/total_mb)*100, 2) as pct_used
FROM (
    SELECT 
        tablespace_name,
        SUM(bytes)/1024/1024 as total_mb,
        SUM(CASE WHEN autoextensible = 'YES' THEN maxbytes ELSE bytes END)/1024/1024 as max_mb
    FROM dba_data_files
    GROUP BY tablespace_name
) df
JOIN (
    SELECT 
        tablespace_name,
        SUM(bytes)/1024/1024 as free_mb
    FROM dba_free_space
    GROUP BY tablespace_name
) fs ON df.tablespace_name = fs.tablespace_name
CROSS APPLY (
    SELECT df.total_mb - fs.free_mb as used_mb FROM dual
)
ORDER BY pct_used DESC;
```