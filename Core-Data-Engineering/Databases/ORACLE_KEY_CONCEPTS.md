# Oracle Database Key Concepts

## 1. Database Architecture
**What it is**: Enterprise-grade relational database with advanced features for high-performance applications.

**Core Components**:
- **Instance**: Memory structures and background processes
- **Database**: Physical files storing data
- **SGA (System Global Area)**: Shared memory region
- **PGA (Program Global Area)**: Private memory for each process

```sql
-- Database creation
CREATE DATABASE SALESDB
CONTROLFILE REUSE
DATAFILE '/u01/oradata/salesdb/system01.dbf' SIZE 500M AUTOEXTEND ON
SYSAUX DATAFILE '/u01/oradata/salesdb/sysaux01.dbf' SIZE 300M AUTOEXTEND ON
UNDO TABLESPACE UNDOTBS1 
DATAFILE '/u01/oradata/salesdb/undotbs01.dbf' SIZE 200M AUTOEXTEND ON
DEFAULT TEMPORARY TABLESPACE TEMP 
TEMPFILE '/u01/oradata/salesdb/temp01.dbf' SIZE 100M;
```

## 2. PL/SQL Programming
**What it is**: Oracle's procedural extension to SQL with advanced programming features.

**Core Constructs**:
```sql
-- PL/SQL block structure
DECLARE
    v_customer_count NUMBER;
    v_message VARCHAR2(100);
BEGIN
    SELECT COUNT(*) INTO v_customer_count FROM customers;
    
    IF v_customer_count > 1000 THEN
        v_message := 'Large customer base: ' || v_customer_count;
    ELSE
        v_message := 'Growing customer base: ' || v_customer_count;
    END IF;
    
    DBMS_OUTPUT.PUT_LINE(v_message);
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('No customers found');
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
END;
/

-- Stored procedure with parameters
CREATE OR REPLACE PROCEDURE get_customer_orders(
    p_customer_id IN NUMBER,
    p_start_date IN DATE DEFAULT NULL,
    p_end_date IN DATE DEFAULT NULL,
    p_cursor OUT SYS_REFCURSOR
) IS
BEGIN
    OPEN p_cursor FOR
        SELECT order_id, order_date, total_amount
        FROM orders
        WHERE customer_id = p_customer_id
          AND (p_start_date IS NULL OR order_date >= p_start_date)
          AND (p_end_date IS NULL OR order_date <= p_end_date)
        ORDER BY order_date DESC;
END;
/

-- Function with return value
CREATE OR REPLACE FUNCTION calculate_discount(
    p_amount IN NUMBER,
    p_customer_type IN VARCHAR2
) RETURN NUMBER IS
    v_discount NUMBER := 0;
BEGIN
    CASE p_customer_type
        WHEN 'PREMIUM' THEN v_discount := p_amount * 0.15;
        WHEN 'STANDARD' THEN v_discount := p_amount * 0.10;
        ELSE v_discount := 0;
    END CASE;
    
    RETURN v_discount;
END;
/
```

## 3. Advanced SQL Features
**Analytical Functions and CTEs**:

```sql
-- Common Table Expressions (WITH clause)
WITH sales_ranking AS (
    SELECT 
        customer_id,
        total_sales,
        ROW_NUMBER() OVER (ORDER BY total_sales DESC) as rank,
        DENSE_RANK() OVER (ORDER BY total_sales DESC) as dense_rank
    FROM customer_sales
),
top_customers AS (
    SELECT * FROM sales_ranking WHERE rank <= 10
)
SELECT * FROM top_customers;

-- Window functions
SELECT 
    customer_id,
    order_date,
    amount,
    SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date 
                      ROWS UNBOUNDED PRECEDING) as running_total,
    LAG(amount, 1) OVER (PARTITION BY customer_id ORDER BY order_date) as prev_amount,
    LEAD(amount, 1) OVER (PARTITION BY customer_id ORDER BY order_date) as next_amount,
    NTILE(4) OVER (ORDER BY amount) as quartile
FROM orders;

-- PIVOT and UNPIVOT
SELECT *
FROM (
    SELECT customer_id, product_category, amount
    FROM sales
)
PIVOT (
    SUM(amount)
    FOR product_category IN ('Electronics', 'Clothing', 'Books')
);
```

## 4. Indexing and Performance
**Index Types and Strategies**:

```sql
-- B-tree index (default)
CREATE INDEX idx_orders_customer_date 
ON orders (customer_id, order_date);

-- Bitmap index (for low cardinality)
CREATE BITMAP INDEX idx_orders_status 
ON orders (status);

-- Function-based index
CREATE INDEX idx_customers_upper_name 
ON customers (UPPER(last_name));

-- Partial index with WHERE clause
CREATE INDEX idx_orders_active 
ON orders (order_date) 
WHERE status = 'ACTIVE';

-- Reverse key index (for sequences)
CREATE INDEX idx_orders_id_reverse 
ON orders (order_id) REVERSE;

-- Index monitoring
ALTER INDEX idx_orders_customer_date MONITORING USAGE;

-- Check index usage
SELECT * FROM v$object_usage WHERE index_name = 'IDX_ORDERS_CUSTOMER_DATE';
```

## 5. Partitioning
**Table Partitioning for Large Tables**:

```sql
-- Range partitioning by date
CREATE TABLE sales_data (
    sale_id NUMBER,
    sale_date DATE,
    customer_id NUMBER,
    amount NUMBER(10,2)
)
PARTITION BY RANGE (sale_date) (
    PARTITION p_2023_q1 VALUES LESS THAN (DATE '2023-04-01'),
    PARTITION p_2023_q2 VALUES LESS THAN (DATE '2023-07-01'),
    PARTITION p_2023_q3 VALUES LESS THAN (DATE '2023-10-01'),
    PARTITION p_2023_q4 VALUES LESS THAN (DATE '2024-01-01'),
    PARTITION p_2024_q1 VALUES LESS THAN (DATE '2024-04-01')
);

-- Hash partitioning for even distribution
CREATE TABLE customer_data (
    customer_id NUMBER,
    customer_name VARCHAR2(100),
    region VARCHAR2(50)
)
PARTITION BY HASH (customer_id) PARTITIONS 8;

-- List partitioning by discrete values
CREATE TABLE regional_sales (
    sale_id NUMBER,
    region VARCHAR2(20),
    amount NUMBER(10,2)
)
PARTITION BY LIST (region) (
    PARTITION p_north VALUES ('NORTH', 'NORTHEAST'),
    PARTITION p_south VALUES ('SOUTH', 'SOUTHEAST'),
    PARTITION p_west VALUES ('WEST', 'SOUTHWEST'),
    PARTITION p_east VALUES ('EAST')
);

-- Composite partitioning
CREATE TABLE sales_composite (
    sale_id NUMBER,
    sale_date DATE,
    region VARCHAR2(20),
    amount NUMBER(10,2)
)
PARTITION BY RANGE (sale_date)
SUBPARTITION BY LIST (region) (
    PARTITION p_2024_q1 VALUES LESS THAN (DATE '2024-04-01') (
        SUBPARTITION p_2024_q1_north VALUES ('NORTH'),
        SUBPARTITION p_2024_q1_south VALUES ('SOUTH')
    ),
    PARTITION p_2024_q2 VALUES LESS THAN (DATE '2024-07-01') (
        SUBPARTITION p_2024_q2_north VALUES ('NORTH'),
        SUBPARTITION p_2024_q2_south VALUES ('SOUTH')
    )
);
```

## 6. Transaction Management and Concurrency
**ACID Properties and Isolation Levels**:

```sql
-- Explicit transaction control
BEGIN
    UPDATE accounts SET balance = balance - 1000 WHERE account_id = 1;
    UPDATE accounts SET balance = balance + 1000 WHERE account_id = 2;
    
    INSERT INTO transaction_log (from_account, to_account, amount, trans_date)
    VALUES (1, 2, 1000, SYSDATE);
    
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/

-- Savepoints for partial rollback
BEGIN
    INSERT INTO customers VALUES (1, 'John Doe');
    SAVEPOINT sp1;
    
    INSERT INTO orders VALUES (1, 1, SYSDATE, 100);
    SAVEPOINT sp2;
    
    -- If this fails, rollback to sp2
    INSERT INTO order_items VALUES (1, 1, 'Invalid Product');
    
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK TO sp2;  -- Keep customer and order, remove items
        COMMIT;
END;
/

-- Lock management
SELECT 
    s.sid,
    s.serial#,
    s.username,
    o.object_name,
    l.locked_mode
FROM v$locked_object l
JOIN dba_objects o ON l.object_id = o.object_id
JOIN v$session s ON l.session_id = s.sid;
```

## 7. Security and User Management
**Authentication and Authorization**:

```sql
-- Create user with profile
CREATE PROFILE analyst_profile LIMIT
    SESSIONS_PER_USER 2
    CPU_PER_SESSION 10000
    CONNECT_TIME 480
    IDLE_TIME 30;

CREATE USER data_analyst 
IDENTIFIED BY SecurePassword123
DEFAULT TABLESPACE users
TEMPORARY TABLESPACE temp
PROFILE analyst_profile;

-- Grant system and object privileges
GRANT CREATE SESSION TO data_analyst;
GRANT SELECT ON sales TO data_analyst;
GRANT EXECUTE ON get_customer_orders TO data_analyst;

-- Role-based security
CREATE ROLE sales_readers;
GRANT SELECT ON sales TO sales_readers;
GRANT SELECT ON customers TO sales_readers;
GRANT sales_readers TO data_analyst;

-- Virtual Private Database (VPD) for row-level security
CREATE OR REPLACE FUNCTION sales_security_policy(
    schema_var IN VARCHAR2,
    table_var IN VARCHAR2
) RETURN VARCHAR2 IS
    predicate VARCHAR2(400);
BEGIN
    predicate := 'region = SYS_CONTEXT(''USERENV'', ''CLIENT_IDENTIFIER'')';
    RETURN predicate;
END;
/

BEGIN
    DBMS_RLS.ADD_POLICY(
        object_schema => 'SALES',
        object_name => 'SALES_DATA',
        policy_name => 'REGION_POLICY',
        function_schema => 'SALES',
        policy_function => 'SALES_SECURITY_POLICY',
        statement_types => 'SELECT, INSERT, UPDATE, DELETE'
    );
END;
/
```

## 8. High Availability and Recovery
**Oracle Real Application Clusters (RAC)**:

```sql
-- Check cluster status
SELECT inst_id, instance_name, status FROM gv$instance;

-- Data Guard configuration
ALTER DATABASE ADD STANDBY LOGFILE GROUP 4 
('/u01/oradata/standby/redo04a.log', '/u02/oradata/standby/redo04b.log') 
SIZE 100M;

-- RMAN backup strategy
RMAN> CONFIGURE RETENTION POLICY TO RECOVERY WINDOW OF 7 DAYS;
RMAN> CONFIGURE DEFAULT DEVICE TYPE TO DISK;
RMAN> BACKUP DATABASE PLUS ARCHIVELOG;

-- Flashback database
ALTER DATABASE FLASHBACK ON;
FLASHBACK DATABASE TO TIMESTAMP (SYSTIMESTAMP - INTERVAL '2' HOUR);
```

## 9. Performance Monitoring and Tuning
**Automatic Workload Repository (AWR)**:

```sql
-- Generate AWR report
@$ORACLE_HOME/rdbms/admin/awrrpt.sql

-- Top SQL by elapsed time
SELECT 
    sql_id,
    elapsed_time_delta / executions_delta as avg_elapsed,
    executions_delta,
    SUBSTR(sql_text, 1, 100) as sql_text
FROM dba_hist_sqlstat s
JOIN dba_hist_sqltext t ON s.sql_id = t.sql_id
WHERE snap_id BETWEEN 100 AND 110
ORDER BY avg_elapsed DESC
FETCH FIRST 10 ROWS ONLY;

-- Session wait events
SELECT 
    event,
    total_waits,
    total_timeouts,
    time_waited,
    average_wait
FROM v$session_event
WHERE sid = 123
ORDER BY time_waited DESC;

-- SQL execution plan
EXPLAIN PLAN FOR
SELECT * FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.region = 'NORTH';

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

## 10. Advanced Features
**Oracle Advanced Analytics**:

```sql
-- Data mining with Oracle ML
SELECT 
    customer_id,
    PREDICTION(churn_model USING *) as churn_prediction,
    PREDICTION_PROBABILITY(churn_model, 'YES' USING *) as churn_probability
FROM customer_features;

-- JSON support
CREATE TABLE json_data (
    id NUMBER,
    data CLOB CHECK (data IS JSON)
);

SELECT j.data.customer.name, j.data.orders[0].amount
FROM json_data j
WHERE JSON_VALUE(j.data, '$.customer.region') = 'NORTH';

-- Spatial data
SELECT 
    store_name,
    SDO_GEOM.SDO_DISTANCE(store_location, 
        SDO_GEOMETRY(2001, 8307, SDO_POINT_TYPE(-122.4194, 37.7749, NULL), NULL, NULL),
        0.005, 'unit=MILE') as distance_miles
FROM stores
WHERE SDO_WITHIN_DISTANCE(store_location,
    SDO_GEOMETRY(2001, 8307, SDO_POINT_TYPE(-122.4194, 37.7749, NULL), NULL, NULL),
    'distance=10 unit=MILE') = 'TRUE';
```