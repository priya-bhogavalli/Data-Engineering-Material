# MySQL Interview Questions for Data Engineers

## Basic Level Questions

### 1. What is MySQL and how does it differ from other databases?
**Answer**: MySQL is an open-source relational database management system (RDBMS) that uses SQL. Key differences:
- **Open Source**: Free to use with community support
- **Performance**: Optimized for read-heavy workloads
- **Storage Engines**: Multiple storage engines (InnoDB, MyISAM)
- **Replication**: Built-in master-slave replication
- **ACID Compliance**: Full ACID compliance with InnoDB

```sql
-- Example: Creating a database with specific character set
CREATE DATABASE sales_data 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
```

### 2. Explain MySQL storage engines and their use cases
**Answer**: MySQL supports multiple storage engines:
- **InnoDB**: Default, ACID compliant, supports foreign keys, row-level locking
- **MyISAM**: Fast for read-heavy workloads, table-level locking
- **Memory**: Stores data in RAM, fast but volatile
- **Archive**: For compressed, archival data

```sql
-- Creating tables with different storage engines
CREATE TABLE transactions (
    id INT PRIMARY KEY,
    amount DECIMAL(10,2),
    created_at TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE logs (
    id INT PRIMARY KEY,
    message TEXT,
    log_date DATE
) ENGINE=MyISAM;
```

### 3. What are MySQL data types commonly used in data engineering?
**Answer**: Key data types for data engineering:
- **Numeric**: INT, BIGINT, DECIMAL, FLOAT, DOUBLE
- **String**: VARCHAR, TEXT, CHAR
- **Date/Time**: DATE, DATETIME, TIMESTAMP
- **JSON**: JSON (MySQL 5.7+)
- **Binary**: BLOB, VARBINARY

```sql
CREATE TABLE customer_data (
    customer_id BIGINT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    registration_date DATE,
    last_login TIMESTAMP,
    profile_data JSON,
    total_spent DECIMAL(12,2) DEFAULT 0.00
);
```

### 4. How do you handle NULL values in MySQL?
**Answer**: NULL handling strategies:
- Use `IS NULL` and `IS NOT NULL` for comparisons
- `COALESCE()` for default values
- `IFNULL()` for simple null replacement
- `NULLIF()` to convert values to NULL

```sql
-- NULL handling examples
SELECT 
    customer_id,
    COALESCE(phone, email, 'No Contact') as contact_method,
    IFNULL(last_purchase_date, '1900-01-01') as last_purchase,
    NULLIF(status, '') as clean_status
FROM customers
WHERE email IS NOT NULL;
```

### 5. Explain MySQL indexing basics
**Answer**: Indexes improve query performance by creating sorted data structures:
- **Primary Index**: Automatically created for PRIMARY KEY
- **Secondary Index**: Created on non-primary columns
- **Composite Index**: Multiple columns in single index
- **Unique Index**: Ensures uniqueness

```sql
-- Creating indexes
CREATE INDEX idx_customer_email ON customers(email);
CREATE INDEX idx_order_date_status ON orders(order_date, status);
CREATE UNIQUE INDEX idx_product_sku ON products(sku);

-- Analyzing index usage
EXPLAIN SELECT * FROM orders WHERE order_date = '2024-01-01';
```

## Intermediate Level Questions

### 6. How do you optimize MySQL queries for large datasets?
**Answer**: Query optimization strategies:
- **Proper Indexing**: Create indexes on WHERE, JOIN, ORDER BY columns
- **Query Structure**: Avoid SELECT *, use LIMIT
- **Join Optimization**: Use appropriate join types
- **Partitioning**: Split large tables
- **Query Cache**: Enable for repeated queries

```sql
-- Before optimization
SELECT * FROM orders o 
JOIN customers c ON o.customer_id = c.id 
WHERE o.order_date > '2024-01-01';

-- After optimization
SELECT o.id, o.total, c.name 
FROM orders o 
INNER JOIN customers c ON o.customer_id = c.id 
WHERE o.order_date > '2024-01-01'
AND o.status = 'completed'
LIMIT 1000;

-- Add supporting indexes
CREATE INDEX idx_orders_date_status ON orders(order_date, status);
```

### 7. Explain MySQL replication and its types
**Answer**: MySQL replication types:
- **Master-Slave**: One master, multiple read-only slaves
- **Master-Master**: Bidirectional replication
- **Group Replication**: Multi-master with conflict resolution
- **Binary Log**: Records all changes for replication

```sql
-- Configure master server
SET GLOBAL server_id = 1;
SET GLOBAL log_bin = 'mysql-bin';
SET GLOBAL binlog_format = 'ROW';

-- Create replication user
CREATE USER 'repl_user'@'%' IDENTIFIED BY 'password';
GRANT REPLICATION SLAVE ON *.* TO 'repl_user'@'%';

-- On slave server
CHANGE MASTER TO
    MASTER_HOST='master_host',
    MASTER_USER='repl_user',
    MASTER_PASSWORD='password',
    MASTER_LOG_FILE='mysql-bin.000001',
    MASTER_LOG_POS=154;
```

### 8. How do you handle transactions in MySQL?
**Answer**: Transaction management ensures data consistency:
- **ACID Properties**: Atomicity, Consistency, Isolation, Durability
- **Transaction Isolation Levels**: READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE
- **Locking**: Row-level vs table-level locking

```sql
-- Transaction example
START TRANSACTION;

UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;

-- Check if both updates succeeded
IF @@ERROR_COUNT = 0 THEN
    COMMIT;
ELSE
    ROLLBACK;
END IF;

-- Set isolation level
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

### 9. What are MySQL partitioning strategies?
**Answer**: Partitioning divides large tables into smaller, manageable pieces:
- **Range Partitioning**: Based on column value ranges
- **List Partitioning**: Based on predefined value lists
- **Hash Partitioning**: Based on hash function
- **Key Partitioning**: Based on primary key

```sql
-- Range partitioning by date
CREATE TABLE sales_data (
    id INT,
    sale_date DATE,
    amount DECIMAL(10,2),
    region VARCHAR(50)
) PARTITION BY RANGE (YEAR(sale_date)) (
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- Hash partitioning
CREATE TABLE user_sessions (
    session_id VARCHAR(64),
    user_id INT,
    created_at TIMESTAMP
) PARTITION BY HASH(user_id) PARTITIONS 4;
```

### 10. How do you monitor MySQL performance?
**Answer**: Performance monitoring techniques:
- **SHOW STATUS**: Server status variables
- **PERFORMANCE_SCHEMA**: Detailed performance metrics
- **EXPLAIN**: Query execution plans
- **Slow Query Log**: Identify slow queries

```sql
-- Check server status
SHOW STATUS LIKE 'Threads_connected';
SHOW STATUS LIKE 'Slow_queries';

-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;

-- Performance schema queries
SELECT * FROM performance_schema.events_statements_summary_by_digest
ORDER BY sum_timer_wait DESC LIMIT 10;

-- Check table sizes
SELECT 
    table_schema,
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.tables
ORDER BY (data_length + index_length) DESC;
```

## Advanced Level Questions

### 11. How do you implement data archiving strategies in MySQL?
**Answer**: Data archiving strategies for managing large datasets:
- **Partitioning**: Archive old partitions
- **Separate Archive Tables**: Move old data to archive tables
- **External Storage**: Export to files or data lakes
- **Automated Scripts**: Schedule archiving jobs

```sql
-- Create archive table structure
CREATE TABLE orders_archive LIKE orders;

-- Archive old data
INSERT INTO orders_archive 
SELECT * FROM orders 
WHERE order_date < DATE_SUB(NOW(), INTERVAL 2 YEAR);

-- Remove archived data
DELETE FROM orders 
WHERE order_date < DATE_SUB(NOW(), INTERVAL 2 YEAR);

-- Partition-based archiving
ALTER TABLE sales_data DROP PARTITION p2022;

-- Create stored procedure for automated archiving
DELIMITER //
CREATE PROCEDURE ArchiveOldOrders()
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    INSERT INTO orders_archive 
    SELECT * FROM orders 
    WHERE order_date < DATE_SUB(NOW(), INTERVAL 1 YEAR);
    
    DELETE FROM orders 
    WHERE order_date < DATE_SUB(NOW(), INTERVAL 1 YEAR);
    
    COMMIT;
END //
DELIMITER ;
```

### 12. Explain MySQL JSON data handling for modern data engineering
**Answer**: MySQL JSON features for semi-structured data:
- **JSON Data Type**: Native JSON storage and validation
- **JSON Functions**: Extract, modify, search JSON data
- **JSON Indexing**: Virtual columns and functional indexes
- **JSON Path Expressions**: Query nested data

```sql
-- Create table with JSON column
CREATE TABLE user_profiles (
    user_id INT PRIMARY KEY,
    profile JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert JSON data
INSERT INTO user_profiles (user_id, profile) VALUES
(1, '{"name": "John", "age": 30, "preferences": {"theme": "dark", "notifications": true}}'),
(2, '{"name": "Jane", "age": 25, "skills": ["Python", "SQL", "Spark"]}');

-- Query JSON data
SELECT 
    user_id,
    JSON_EXTRACT(profile, '$.name') as name,
    JSON_EXTRACT(profile, '$.age') as age,
    JSON_EXTRACT(profile, '$.skills[0]') as first_skill
FROM user_profiles;

-- Create virtual column for indexing
ALTER TABLE user_profiles 
ADD COLUMN name VARCHAR(100) AS (JSON_UNQUOTE(JSON_EXTRACT(profile, '$.name')));

CREATE INDEX idx_profile_name ON user_profiles(name);

-- JSON aggregation
SELECT 
    JSON_ARRAYAGG(JSON_EXTRACT(profile, '$.name')) as all_names,
    JSON_OBJECTAGG(user_id, JSON_EXTRACT(profile, '$.age')) as user_ages
FROM user_profiles;
```

### 13. How do you implement change data capture (CDC) in MySQL?
**Answer**: CDC implementation strategies:
- **Binary Log**: Parse binlog for changes
- **Triggers**: Capture changes with database triggers
- **Timestamp Columns**: Track last modified time
- **Tools**: Debezium, Maxwell, Canal

```sql
-- Trigger-based CDC
CREATE TABLE customer_changes (
    change_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    operation ENUM('INSERT', 'UPDATE', 'DELETE'),
    old_data JSON,
    new_data JSON,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create trigger for updates
DELIMITER //
CREATE TRIGGER customer_update_trigger
AFTER UPDATE ON customers
FOR EACH ROW
BEGIN
    INSERT INTO customer_changes (customer_id, operation, old_data, new_data)
    VALUES (
        NEW.id,
        'UPDATE',
        JSON_OBJECT('name', OLD.name, 'email', OLD.email, 'status', OLD.status),
        JSON_OBJECT('name', NEW.name, 'email', NEW.email, 'status', NEW.status)
    );
END //
DELIMITER ;

-- Timestamp-based CDC
ALTER TABLE customers 
ADD COLUMN last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- Query for changes since last sync
SELECT * FROM customers 
WHERE last_modified > '2024-01-01 10:00:00';
```

### 14. How do you handle MySQL high availability and disaster recovery?
**Answer**: HA and DR strategies:
- **MySQL Cluster**: Shared-nothing clustering
- **Group Replication**: Multi-master setup
- **ProxySQL**: Connection routing and failover
- **Backup Strategies**: Point-in-time recovery

```sql
-- Group Replication setup
SET GLOBAL group_replication_group_name = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa";
SET GLOBAL group_replication_start_on_boot = OFF;
SET GLOBAL group_replication_local_address = "server1:33061";
SET GLOBAL group_replication_group_seeds = "server1:33061,server2:33061,server3:33061";

-- Start group replication
START GROUP_REPLICATION;

-- Backup strategies
-- Full backup
mysqldump --single-transaction --routines --triggers --all-databases > full_backup.sql

-- Point-in-time recovery
mysqlbinlog --start-datetime="2024-01-01 10:00:00" \
           --stop-datetime="2024-01-01 11:00:00" \
           mysql-bin.000001 | mysql

-- Automated backup script
#!/bin/bash
BACKUP_DIR="/backups/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump --single-transaction --all-databases | gzip > "$BACKUP_DIR/backup_$DATE.sql.gz"
```

### 15. How do you optimize MySQL for data warehouse workloads?
**Answer**: Data warehouse optimization techniques:
- **Columnar Storage**: Use TokuDB or external solutions
- **Partitioning**: Partition by time or other dimensions
- **Indexing Strategy**: Covering indexes for analytical queries
- **Query Optimization**: Materialized views, summary tables

```sql
-- Create summary tables for faster analytics
CREATE TABLE daily_sales_summary (
    sale_date DATE PRIMARY KEY,
    total_revenue DECIMAL(15,2),
    total_orders INT,
    avg_order_value DECIMAL(10,2),
    unique_customers INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Populate summary table
INSERT INTO daily_sales_summary (sale_date, total_revenue, total_orders, avg_order_value, unique_customers)
SELECT 
    DATE(order_date) as sale_date,
    SUM(total_amount) as total_revenue,
    COUNT(*) as total_orders,
    AVG(total_amount) as avg_order_value,
    COUNT(DISTINCT customer_id) as unique_customers
FROM orders 
WHERE order_date >= CURDATE() - INTERVAL 1 DAY
GROUP BY DATE(order_date);

-- Create covering index for analytical queries
CREATE INDEX idx_orders_analytics ON orders(order_date, status, customer_id, total_amount);

-- Partitioned fact table
CREATE TABLE fact_sales (
    sale_id BIGINT,
    date_key INT,
    customer_key INT,
    product_key INT,
    quantity INT,
    revenue DECIMAL(10,2)
) PARTITION BY RANGE (date_key) (
    PARTITION p202401 VALUES LESS THAN (20240201),
    PARTITION p202402 VALUES LESS THAN (20240301),
    PARTITION p202403 VALUES LESS THAN (20240401)
);
```

## Data Engineering Specific Questions

### 16. How do you implement slowly changing dimensions (SCD) in MySQL?
**Answer**: SCD implementation patterns:

```sql
-- SCD Type 1: Overwrite
UPDATE dim_customer 
SET city = 'New York', last_updated = NOW()
WHERE customer_id = 123;

-- SCD Type 2: Historical tracking
CREATE TABLE dim_customer_scd2 (
    surrogate_key INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    name VARCHAR(100),
    city VARCHAR(50),
    effective_date DATE,
    expiry_date DATE,
    is_current BOOLEAN DEFAULT TRUE
);

-- Insert new version
INSERT INTO dim_customer_scd2 (customer_id, name, city, effective_date)
VALUES (123, 'John Doe', 'New York', CURDATE());

-- Update previous version
UPDATE dim_customer_scd2 
SET expiry_date = CURDATE() - INTERVAL 1 DAY, is_current = FALSE
WHERE customer_id = 123 AND is_current = TRUE AND surrogate_key != LAST_INSERT_ID();
```

### 17. How do you handle data quality checks in MySQL?
**Answer**: Data quality implementation:

```sql
-- Create data quality rules table
CREATE TABLE data_quality_rules (
    rule_id INT PRIMARY KEY,
    table_name VARCHAR(100),
    column_name VARCHAR(100),
    rule_type ENUM('NOT_NULL', 'UNIQUE', 'RANGE', 'PATTERN', 'REFERENCE'),
    rule_definition JSON,
    is_active BOOLEAN DEFAULT TRUE
);

-- Data quality check procedure
DELIMITER //
CREATE PROCEDURE CheckDataQuality(IN table_name VARCHAR(100))
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE rule_type VARCHAR(50);
    DECLARE column_name VARCHAR(100);
    DECLARE rule_def JSON;
    
    DECLARE rule_cursor CURSOR FOR
        SELECT rule_type, column_name, rule_definition
        FROM data_quality_rules
        WHERE table_name = table_name AND is_active = TRUE;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN rule_cursor;
    
    rule_loop: LOOP
        FETCH rule_cursor INTO rule_type, column_name, rule_def;
        IF done THEN
            LEAVE rule_loop;
        END IF;
        
        -- Execute quality checks based on rule_type
        CASE rule_type
            WHEN 'NOT_NULL' THEN
                SET @sql = CONCAT('SELECT COUNT(*) FROM ', table_name, ' WHERE ', column_name, ' IS NULL');
            WHEN 'UNIQUE' THEN
                SET @sql = CONCAT('SELECT COUNT(*) - COUNT(DISTINCT ', column_name, ') FROM ', table_name);
        END CASE;
        
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        
    END LOOP;
    
    CLOSE rule_cursor;
END //
DELIMITER ;
```

### 18. How do you implement data lineage tracking in MySQL?
**Answer**: Data lineage implementation:

```sql
-- Data lineage metadata tables
CREATE TABLE data_lineage (
    lineage_id INT AUTO_INCREMENT PRIMARY KEY,
    source_table VARCHAR(100),
    source_column VARCHAR(100),
    target_table VARCHAR(100),
    target_column VARCHAR(100),
    transformation_logic TEXT,
    created_by VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ETL job tracking
CREATE TABLE etl_job_runs (
    run_id INT AUTO_INCREMENT PRIMARY KEY,
    job_name VARCHAR(100),
    source_tables JSON,
    target_tables JSON,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status ENUM('RUNNING', 'SUCCESS', 'FAILED'),
    records_processed INT,
    error_message TEXT
);

-- Track data transformations
INSERT INTO data_lineage (source_table, source_column, target_table, target_column, transformation_logic)
VALUES 
('raw_orders', 'order_total', 'fact_sales', 'revenue', 'Direct mapping'),
('raw_orders', 'order_date', 'fact_sales', 'date_key', 'DATE_FORMAT(order_date, "%Y%m%d")');
```

This comprehensive set of MySQL interview questions covers the essential knowledge areas for data engineers, from basic database concepts to advanced data engineering patterns and practices.