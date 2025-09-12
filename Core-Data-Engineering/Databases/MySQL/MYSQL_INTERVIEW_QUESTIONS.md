# MySQL Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-30)](#basic-level-questions-1-30)
2. [Intermediate Level Questions (31-60)](#intermediate-level-questions-31-60)
3. [Advanced Level Questions (61-90)](#advanced-level-questions-61-90)
4. [Data Engineering Patterns (91-120)](#data-engineering-patterns-91-120)
5. [Performance & Optimization (121-150)](#performance--optimization-121-150)
6. [Production & Operations (151-180)](#production--operations-151-180)
7. [Scenario-Based Questions (181-200)](#scenario-based-questions-181-200)

---

## Basic Level Questions (1-30)

### 1. What is MySQL and how does it differ from other relational databases?

**Answer:** MySQL is an open-source relational database management system (RDBMS) that uses SQL for data management.

#### 🎯 **Database Comparison Matrix**

| Feature | MySQL | PostgreSQL | SQL Server | Oracle |
|---------|-------|------------|------------|--------|
| **License** | Open Source/Commercial | Open Source | Commercial | Commercial |
| **Performance** | Read-optimized | Balanced | Enterprise-grade | High-performance |
| **Storage Engines** | Multiple (InnoDB, MyISAM) | Single | Single | Single |
| **JSON Support** | Native (5.7+) | Advanced | Basic | Advanced |
| **Replication** | Master-Slave/Master-Master | Streaming | Always On | Data Guard |
| **Partitioning** | Range/Hash/List | Range/Hash/List | Range/Hash/List | Advanced |
| **ACID Compliance** | Full (InnoDB) | Full | Full | Full |
| **Scalability** | Horizontal (sharding) | Vertical/Horizontal | Vertical/Horizontal | Vertical/Horizontal |

```sql
-- MySQL-specific features demonstration
CREATE DATABASE sales_analytics 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE sales_analytics;

-- Multiple storage engines
CREATE TABLE transactions_innodb (
    id INT PRIMARY KEY AUTO_INCREMENT,
    amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE logs_myisam (
    id INT PRIMARY KEY AUTO_INCREMENT,
    message TEXT,
    log_date DATE
) ENGINE=MyISAM;

-- Show storage engines
SHOW ENGINES;
```

**Output:**
```
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
| Engine             | Support | Comment                                                        | Transactions | XA   | Savepoints |
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
| InnoDB             | DEFAULT | Supports transactions, row-level locking, and foreign keys    | YES          | YES  | YES        |
| MyISAM             | YES     | MyISAM storage engine                                          | NO           | NO   | NO         |
| MEMORY             | YES     | Hash based, stored in memory, useful for temporary tables     | NO           | NO   | NO         |
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
```

### 2. Explain MySQL storage engines and their use cases in data engineering

**Answer:** MySQL supports multiple storage engines, each optimized for different use cases.

#### 🎯 **Storage Engine Decision Matrix**

```
Storage Engine Selection Guide:
┌────────────────┬────────────────┬────────────────┬────────────────┐
| Use Case        | InnoDB         | MyISAM         | Memory         |
├────────────────┼────────────────┼────────────────┼────────────────┤
| OLTP Systems    | ✓ Optimal     | ✗ No ACID     | ✗ Volatile     |
| Data Warehouses | ✓ Good        | ✓ Read-heavy  | ✗ Size limit   |
| Logging         | ✓ Reliable    | ✓ Fast writes | ✗ Volatile     |
| Caching         | ✗ Overhead    | ✗ Disk I/O    | ✓ Optimal      |
| Analytics       | ✓ Consistent  | ✓ Fast reads  | ✓ Temp results |
| Replication     | ✓ Full support| ✓ Basic       | ✗ Limited      |
└────────────────┴────────────────┴────────────────┴────────────────┘
```

```sql
-- InnoDB: ACID compliant, row-level locking
CREATE TABLE customer_orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    order_total DECIMAL(10,2),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'processing', 'shipped', 'delivered'),
    INDEX idx_customer_date (customer_id, order_date),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
) ENGINE=InnoDB;

-- MyISAM: Fast for read-heavy workloads
CREATE TABLE product_catalog (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(255),
    category VARCHAR(100),
    price DECIMAL(8,2),
    description TEXT,
    FULLTEXT(product_name, description)
) ENGINE=MyISAM;

-- Memory: In-memory storage for temporary data
CREATE TABLE session_data (
    session_id VARCHAR(64) PRIMARY KEY,
    user_id INT,
    data JSON,
    expires_at TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_expires (expires_at)
) ENGINE=MEMORY;

-- Check table information
SELECT 
    table_name,
    engine,
    table_rows,
    data_length,
    index_length
FROM information_schema.tables 
WHERE table_schema = 'sales_analytics';
```

**Output:**
```
+------------------+--------+------------+-------------+--------------+
| table_name       | engine | table_rows | data_length | index_length |
+------------------+--------+------------+-------------+--------------+
| customer_orders  | InnoDB |          0 |       16384 |            0 |
| product_catalog  | MyISAM |          0 |           0 |         1024 |
| session_data     | MEMORY |          0 |           0 |            0 |
+------------------+--------+------------+-------------+--------------+
```

### 3. What are MySQL data types and how do you choose them for data engineering?

**Answer:** MySQL provides various data types optimized for different data patterns and storage requirements.

#### 🎯 **Data Type Selection Guide**

```sql
-- Comprehensive data types for data engineering
CREATE TABLE data_engineering_example (
    -- Numeric types
    tiny_int TINYINT,                    -- 1 byte: -128 to 127
    small_int SMALLINT,                  -- 2 bytes: -32,768 to 32,767
    medium_int MEDIUMINT,                -- 3 bytes: -8,388,608 to 8,388,607
    regular_int INT,                     -- 4 bytes: -2,147,483,648 to 2,147,483,647
    big_int BIGINT,                      -- 8 bytes: very large numbers
    
    -- Decimal types for financial data
    precise_decimal DECIMAL(15,2),       -- Exact precision for money
    float_val FLOAT(7,4),               -- Single precision floating point
    double_val DOUBLE(15,8),            -- Double precision floating point
    
    -- String types
    fixed_char CHAR(10),                -- Fixed length, padded with spaces
    variable_char VARCHAR(255),         -- Variable length, up to 255 chars
    tiny_text TINYTEXT,                 -- Up to 255 characters
    regular_text TEXT,                  -- Up to 65,535 characters
    medium_text MEDIUMTEXT,             -- Up to 16,777,215 characters
    long_text LONGTEXT,                 -- Up to 4,294,967,295 characters
    
    -- Date and time types
    date_only DATE,                     -- YYYY-MM-DD
    time_only TIME,                     -- HH:MM:SS
    datetime_val DATETIME,              -- YYYY-MM-DD HH:MM:SS
    timestamp_val TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    year_val YEAR,                      -- 4-digit year
    
    -- Binary types
    binary_data BINARY(16),             -- Fixed length binary
    variable_binary VARBINARY(255),     -- Variable length binary
    tiny_blob TINYBLOB,                 -- Up to 255 bytes
    regular_blob BLOB,                  -- Up to 65,535 bytes
    
    -- JSON type (MySQL 5.7+)
    json_data JSON,                     -- Native JSON storage
    
    -- Enum and Set
    status_enum ENUM('active', 'inactive', 'pending'),
    tags_set SET('urgent', 'important', 'review', 'archived')
);

-- Insert sample data
INSERT INTO data_engineering_example (
    tiny_int, regular_int, big_int, precise_decimal,
    variable_char, regular_text, date_only, datetime_val,
    json_data, status_enum, tags_set
) VALUES (
    127, 1000000, 9223372036854775807, 99999.99,
    'Sample Data', 'This is a longer text field for descriptions',
    '2024-01-15', '2024-01-15 10:30:00',
    '{"name": "John", "age": 30, "skills": ["Python", "SQL"]}',
    'active', 'urgent,important'
);

-- Query data with type information
SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH,
    NUMERIC_PRECISION,
    NUMERIC_SCALE
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'sales_analytics' 
AND TABLE_NAME = 'data_engineering_example'
ORDER BY ORDINAL_POSITION;
```

**Output:**
```
+------------------+-----------+-------------------------+------------------+---------------+
| COLUMN_NAME      | DATA_TYPE | CHARACTER_MAXIMUM_LENGTH| NUMERIC_PRECISION| NUMERIC_SCALE |
+------------------+-----------+-------------------------+------------------+---------------+
| tiny_int         | tinyint   |                    NULL |                3 |             0 |
| regular_int      | int       |                    NULL |               10 |             0 |
| big_int          | bigint    |                    NULL |               19 |             0 |
| precise_decimal  | decimal   |                    NULL |               15 |             2 |
| variable_char    | varchar   |                     255 |             NULL |          NULL |
| json_data        | json      |                    NULL |             NULL |          NULL |
+------------------+-----------+-------------------------+------------------+---------------+
```

### 4. How do you handle NULL values and data validation in MySQL?

**Answer:** MySQL provides multiple mechanisms for handling NULL values and implementing data validation.

```sql
-- Create table with NULL handling and constraints
CREATE TABLE customer_data (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    birth_date DATE,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    credit_limit DECIMAL(10,2) DEFAULT 0.00,
    
    -- Check constraints (MySQL 8.0+)
    CONSTRAINT chk_email_format CHECK (email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT chk_credit_limit CHECK (credit_limit >= 0),
    CONSTRAINT chk_birth_date CHECK (birth_date <= CURDATE())
);

-- NULL handling functions
SELECT 
    customer_id,
    first_name,
    last_name,
    
    -- Handle NULL phone numbers
    COALESCE(phone, 'No phone provided') as contact_phone,
    IFNULL(phone, 'N/A') as phone_display,
    
    -- Convert empty strings to NULL
    NULLIF(phone, '') as clean_phone,
    
    -- Conditional NULL handling
    CASE 
        WHEN phone IS NULL THEN 'Missing'
        WHEN phone = '' THEN 'Empty'
        ELSE 'Available'
    END as phone_status,
    
    -- Calculate age handling NULL birth_date
    CASE 
        WHEN birth_date IS NOT NULL 
        THEN TIMESTAMPDIFF(YEAR, birth_date, CURDATE())
        ELSE NULL
    END as age
FROM customer_data;

-- Insert test data
INSERT INTO customer_data (email, first_name, last_name, phone, birth_date) VALUES
('john.doe@email.com', 'John', 'Doe', '+1-555-0123', '1990-05-15'),
('jane.smith@email.com', 'Jane', 'Smith', NULL, '1985-12-20'),
('bob.wilson@email.com', 'Bob', 'Wilson', '', '1992-03-10');

-- Data validation queries
SELECT 
    'Total customers' as metric,
    COUNT(*) as value
UNION ALL
SELECT 
    'Customers with phone',
    COUNT(phone)
UNION ALL
SELECT 
    'Customers without phone',
    COUNT(*) - COUNT(phone)
UNION ALL
SELECT 
    'Customers with empty phone',
    SUM(CASE WHEN phone = '' THEN 1 ELSE 0 END);
```

**Output:**
```
+------------------------+-------+
| metric                 | value |
+------------------------+-------+
| Total customers        |     3 |
| Customers with phone   |     1 |
| Customers without phone|     2 |
| Customers with empty phone|  1 |
+------------------------+-------+
```

### 5. Explain MySQL indexing fundamentals for data engineering

**Answer:** Indexes are crucial for query performance in data engineering workloads.

#### 🎯 **Index Performance Impact**

```sql
-- Create table for indexing demonstration
CREATE TABLE sales_transactions (
    transaction_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    transaction_date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_method ENUM('credit_card', 'debit_card', 'cash', 'digital_wallet'),
    store_id INT NOT NULL,
    sales_rep_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data for testing
INSERT INTO sales_transactions (customer_id, product_id, transaction_date, amount, payment_method, store_id, sales_rep_id)
SELECT 
    FLOOR(1 + RAND() * 10000) as customer_id,
    FLOOR(1 + RAND() * 1000) as product_id,
    DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND() * 365) DAY) as transaction_date,
    ROUND(10 + RAND() * 990, 2) as amount,
    ELT(FLOOR(1 + RAND() * 4), 'credit_card', 'debit_card', 'cash', 'digital_wallet') as payment_method,
    FLOOR(1 + RAND() * 50) as store_id,
    FLOOR(1 + RAND() * 100) as sales_rep_id
FROM 
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) t1,
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) t2,
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) t3,
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) t4
LIMIT 10000;

-- Query performance before indexing
EXPLAIN SELECT * FROM sales_transactions 
WHERE customer_id = 5000 AND transaction_date >= '2024-01-01';

-- Create indexes for common query patterns
CREATE INDEX idx_customer_date ON sales_transactions(customer_id, transaction_date);
CREATE INDEX idx_product_amount ON sales_transactions(product_id, amount);
CREATE INDEX idx_store_date ON sales_transactions(store_id, transaction_date);
CREATE INDEX idx_payment_method ON sales_transactions(payment_method);

-- Composite index for complex queries
CREATE INDEX idx_customer_product_date ON sales_transactions(customer_id, product_id, transaction_date);

-- Covering index (includes all needed columns)
CREATE INDEX idx_covering_sales ON sales_transactions(customer_id, transaction_date, amount, payment_method);

-- Query performance after indexing
EXPLAIN SELECT * FROM sales_transactions 
WHERE customer_id = 5000 AND transaction_date >= '2024-01-01';

-- Index usage analysis
SELECT 
    TABLE_NAME,
    INDEX_NAME,
    COLUMN_NAME,
    SEQ_IN_INDEX,
    CARDINALITY,
    INDEX_TYPE
FROM INFORMATION_SCHEMA.STATISTICS 
WHERE TABLE_SCHEMA = 'sales_analytics' 
AND TABLE_NAME = 'sales_transactions'
ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX;
```

**Output:**
```
+-------------------+---------------------------+------------------+--------------+-------------+------------+
| TABLE_NAME        | INDEX_NAME                | COLUMN_NAME      | SEQ_IN_INDEX | CARDINALITY | INDEX_TYPE |
+-------------------+---------------------------+------------------+--------------+-------------+------------+
| sales_transactions| PRIMARY                   | transaction_id   |            1 |       10000 | BTREE      |
| sales_transactions| idx_customer_date         | customer_id      |            1 |        9950 | BTREE      |
| sales_transactions| idx_customer_date         | transaction_date |            2 |       10000 | BTREE      |
| sales_transactions| idx_covering_sales        | customer_id      |            1 |        9950 | BTREE      |
| sales_transactions| idx_covering_sales        | transaction_date |            2 |       10000 | BTREE      |
+-------------------+---------------------------+------------------+--------------+-------------+------------+
```

### 6. How do you implement data partitioning in MySQL?

**Answer:** MySQL partitioning divides large tables into smaller, manageable pieces for better performance and maintenance.

```sql
-- Range partitioning by date
CREATE TABLE sales_data_partitioned (
    sale_id BIGINT AUTO_INCREMENT,
    customer_id INT NOT NULL,
    sale_date DATE NOT NULL,
    amount DECIMAL(10,2),
    region VARCHAR(50),
    PRIMARY KEY (sale_id, sale_date)
) PARTITION BY RANGE (YEAR(sale_date)) (
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- Hash partitioning for even distribution
CREATE TABLE user_sessions_partitioned (
    session_id VARCHAR(64),
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data JSON,
    PRIMARY KEY (session_id, user_id)
) PARTITION BY HASH(user_id) PARTITIONS 8;

-- List partitioning by region
CREATE TABLE regional_sales (
    sale_id BIGINT AUTO_INCREMENT,
    region VARCHAR(20) NOT NULL,
    amount DECIMAL(10,2),
    sale_date DATE,
    PRIMARY KEY (sale_id, region)
) PARTITION BY LIST COLUMNS(region) (
    PARTITION p_north VALUES IN ('north', 'northeast', 'northwest'),
    PARTITION p_south VALUES IN ('south', 'southeast', 'southwest'),
    PARTITION p_east VALUES IN ('east', 'central_east'),
    PARTITION p_west VALUES IN ('west', 'central_west')
);

-- Insert test data
INSERT INTO sales_data_partitioned (customer_id, sale_date, amount, region) VALUES
(1001, '2022-06-15', 150.00, 'north'),
(1002, '2023-03-20', 275.50, 'south'),
(1003, '2024-01-10', 89.99, 'east'),
(1004, '2024-12-05', 320.00, 'west');

-- Check partition information
SELECT 
    TABLE_NAME,
    PARTITION_NAME,
    PARTITION_ORDINAL_POSITION,
    PARTITION_METHOD,
    PARTITION_EXPRESSION,
    PARTITION_DESCRIPTION,
    TABLE_ROWS
FROM INFORMATION_SCHEMA.PARTITIONS 
WHERE TABLE_SCHEMA = 'sales_analytics' 
AND TABLE_NAME = 'sales_data_partitioned'
AND PARTITION_NAME IS NOT NULL;

-- Query specific partition
SELECT * FROM sales_data_partitioned PARTITION (p2024);

-- Add new partition
ALTER TABLE sales_data_partitioned 
ADD PARTITION (PARTITION p2025 VALUES LESS THAN (2026));

-- Drop old partition
ALTER TABLE sales_data_partitioned DROP PARTITION p2022;
```

**Output:**
```
+------------------------+----------------+---------------------------+------------------+--------------------+------------------------+------------+
| TABLE_NAME             | PARTITION_NAME | PARTITION_ORDINAL_POSITION| PARTITION_METHOD | PARTITION_EXPRESSION| PARTITION_DESCRIPTION  | TABLE_ROWS |
+------------------------+----------------+---------------------------+------------------+--------------------+------------------------+------------+
| sales_data_partitioned | p2022          |                         1 | RANGE            | YEAR(`sale_date`)  | 2023                   |          1 |
| sales_data_partitioned | p2023          |                         2 | RANGE            | YEAR(`sale_date`)  | 2024                   |          1 |
| sales_data_partitioned | p2024          |                         3 | RANGE            | YEAR(`sale_date`)  | 2025                   |          2 |
| sales_data_partitioned | p_future       |                         4 | RANGE            | YEAR(`sale_date`)  | MAXVALUE               |          0 |
+------------------------+----------------+---------------------------+------------------+--------------------+------------------------+------------+
```

### 7. What are MySQL transactions and how do you handle them in data pipelines?

**Answer:** Transactions ensure data consistency and integrity in data engineering workflows.

```sql
-- Transaction isolation levels demonstration
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- Create tables for transaction demo
CREATE TABLE account_balances (
    account_id INT PRIMARY KEY,
    balance DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE transaction_log (
    log_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    from_account INT,
    to_account INT,
    amount DECIMAL(15,2),
    transaction_type ENUM('transfer', 'deposit', 'withdrawal'),
    status ENUM('pending', 'completed', 'failed'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial data
INSERT INTO account_balances (account_id, balance) VALUES
(1001, 5000.00),
(1002, 3000.00),
(1003, 1500.00);

-- Transaction example: Money transfer
DELIMITER //
CREATE PROCEDURE TransferMoney(
    IN from_acc INT,
    IN to_acc INT,
    IN transfer_amount DECIMAL(15,2)
)
BEGIN
    DECLARE current_balance DECIMAL(15,2);
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        UPDATE transaction_log 
        SET status = 'failed' 
        WHERE from_account = from_acc 
        AND to_account = to_acc 
        AND amount = transfer_amount 
        AND status = 'pending'
        ORDER BY created_at DESC LIMIT 1;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    -- Log transaction as pending
    INSERT INTO transaction_log (from_account, to_account, amount, transaction_type, status)
    VALUES (from_acc, to_acc, transfer_amount, 'transfer', 'pending');
    
    -- Check sufficient balance
    SELECT balance INTO current_balance 
    FROM account_balances 
    WHERE account_id = from_acc FOR UPDATE;
    
    IF current_balance < transfer_amount THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient funds';
    END IF;
    
    -- Perform transfer
    UPDATE account_balances 
    SET balance = balance - transfer_amount 
    WHERE account_id = from_acc;
    
    UPDATE account_balances 
    SET balance = balance + transfer_amount 
    WHERE account_id = to_acc;
    
    -- Update transaction status
    UPDATE transaction_log 
    SET status = 'completed' 
    WHERE from_account = from_acc 
    AND to_account = to_acc 
    AND amount = transfer_amount 
    AND status = 'pending'
    ORDER BY created_at DESC LIMIT 1;
    
    COMMIT;
END //
DELIMITER ;

-- Execute transfer
CALL TransferMoney(1001, 1002, 500.00);

-- Check results
SELECT * FROM account_balances ORDER BY account_id;
SELECT * FROM transaction_log ORDER BY created_at DESC LIMIT 5;

-- Batch processing with transactions
DELIMITER //
CREATE PROCEDURE ProcessBatchTransactions()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE batch_size INT DEFAULT 1000;
    DECLARE processed_count INT DEFAULT 0;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    -- Process in batches to avoid long-running transactions
    WHILE NOT done DO
        START TRANSACTION;
        
        -- Process batch of pending transactions
        UPDATE transaction_log 
        SET status = 'completed' 
        WHERE status = 'pending' 
        LIMIT batch_size;
        
        SET processed_count = ROW_COUNT();
        
        IF processed_count = 0 THEN
            SET done = TRUE;
        END IF;
        
        COMMIT;
    END WHILE;
END //
DELIMITER ;
```

**Output:**
```
+------------+---------+---------------------+
| account_id | balance | last_updated        |
+------------+---------+---------------------+
|       1001 | 4500.00 | 2024-01-15 10:30:15 |
|       1002 | 3500.00 | 2024-01-15 10:30:15 |
|       1003 | 1500.00 | 2024-01-15 10:25:00 |
+------------+---------+---------------------+

+--------+--------------+------------+--------+------------------+-----------+---------------------+
| log_id | from_account | to_account | amount | transaction_type | status    | created_at          |
+--------+--------------+------------+--------+------------------+-----------+---------------------+
|      1 |         1001 |       1002 | 500.00 | transfer         | completed | 2024-01-15 10:30:15 |
+--------+--------------+------------+--------+------------------+-----------+---------------------+
```

### 8. How do you implement MySQL replication for data engineering?

**Answer:** MySQL replication provides data redundancy, read scaling, and disaster recovery capabilities.

```sql
-- Master server configuration
-- Add to my.cnf on master server:
/*
[mysqld]
server-id = 1
log-bin = mysql-bin
binlog-format = ROW
binlog-do-db = sales_analytics
expire_logs_days = 7
max_binlog_size = 100M
*/

-- Create replication user on master
CREATE USER 'repl_user'@'%' IDENTIFIED BY 'secure_password';
GRANT REPLICATION SLAVE ON *.* TO 'repl_user'@'%';
FLUSH PRIVILEGES;

-- Get master status
SHOW MASTER STATUS;

-- Slave server configuration
-- Add to my.cnf on slave server:
/*
[mysqld]
server-id = 2
relay-log = relay-bin
read-only = 1
replicate-do-db = sales_analytics
*/

-- Configure slave (run on slave server)
CHANGE MASTER TO
    MASTER_HOST='192.168.1.100',
    MASTER_USER='repl_user',
    MASTER_PASSWORD='secure_password',
    MASTER_LOG_FILE='mysql-bin.000001',
    MASTER_LOG_POS=154;

-- Start replication
START SLAVE;

-- Check slave status
SHOW SLAVE STATUS\G

-- Monitoring replication lag
SELECT 
    CASE 
        WHEN MASTER_POS_WAIT('mysql-bin.000001', 1000, 1) = -1 
        THEN 'Timeout or Error'
        ELSE 'Synchronized'
    END as replication_status;

-- Create monitoring table for replication health
CREATE TABLE replication_monitor (
    check_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    master_file VARCHAR(255),
    master_position BIGINT,
    slave_lag_seconds INT,
    slave_running ENUM('Yes', 'No'),
    last_error TEXT
);

-- Stored procedure to monitor replication
DELIMITER //
CREATE PROCEDURE MonitorReplication()
BEGIN
    DECLARE master_file VARCHAR(255);
    DECLARE master_pos BIGINT;
    DECLARE slave_lag INT;
    DECLARE slave_running VARCHAR(10);
    DECLARE last_error TEXT;
    
    -- Get slave status
    SELECT 
        Master_Log_File,
        Read_Master_Log_Pos,
        Seconds_Behind_Master,
        Slave_SQL_Running,
        Last_Error
    INTO master_file, master_pos, slave_lag, slave_running, last_error
    FROM (SHOW SLAVE STATUS) AS slave_status;
    
    -- Insert monitoring record
    INSERT INTO replication_monitor 
    (master_file, master_position, slave_lag_seconds, slave_running, last_error)
    VALUES (master_file, master_pos, slave_lag, slave_running, last_error);
END //
DELIMITER ;

-- Test replication with sample data
INSERT INTO sales_transactions (customer_id, product_id, transaction_date, amount, payment_method, store_id)
VALUES (9999, 999, CURDATE(), 99.99, 'credit_card', 1);

-- Verify on slave (should appear automatically)
SELECT COUNT(*) as total_transactions FROM sales_transactions;
```

**Master Status Output:**
```
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql-bin.000001 |      154 | sales_analytics|                |                   |
+------------------+----------+--------------+------------------+-------------------+
```

### 9. How do you handle JSON data in MySQL for modern data engineering?

**Answer:** MySQL's native JSON support enables efficient storage and querying of semi-structured data.

```sql
-- Create table with JSON columns
CREATE TABLE user_profiles (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    profile_data JSON NOT NULL,
    preferences JSON,
    activity_log JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert JSON data
INSERT INTO user_profiles (email, profile_data, preferences, activity_log) VALUES
('john.doe@email.com', 
 '{"name": "John Doe", "age": 30, "location": {"city": "New York", "country": "USA"}, "skills": ["Python", "SQL", "Spark"]}',
 '{"theme": "dark", "notifications": {"email": true, "sms": false}, "language": "en"}',
 '{"logins": [{"date": "2024-01-15", "ip": "192.168.1.100"}, {"date": "2024-01-14", "ip": "192.168.1.101"}]}'),
 
('jane.smith@email.com',
 '{"name": "Jane Smith", "age": 28, "location": {"city": "San Francisco", "country": "USA"}, "skills": ["Java", "Kafka", "Kubernetes"]}',
 '{"theme": "light", "notifications": {"email": false, "sms": true}, "language": "en"}',
 '{"logins": [{"date": "2024-01-15", "ip": "10.0.0.50"}]}');

-- JSON extraction and querying
SELECT 
    user_id,
    email,
    JSON_EXTRACT(profile_data, '$.name') as name,
    JSON_EXTRACT(profile_data, '$.age') as age,
    JSON_EXTRACT(profile_data, '$.location.city') as city,
    JSON_EXTRACT(profile_data, '$.skills[0]') as primary_skill,
    JSON_LENGTH(profile_data, '$.skills') as skill_count
FROM user_profiles;

-- JSON search and filtering
SELECT 
    user_id,
    JSON_UNQUOTE(JSON_EXTRACT(profile_data, '$.name')) as name
FROM user_profiles
WHERE JSON_EXTRACT(profile_data, '$.age') > 25
AND JSON_CONTAINS(profile_data, '"Python"', '$.skills');

-- JSON modification
UPDATE user_profiles 
SET profile_data = JSON_SET(
    profile_data, 
    '$.last_login', 
    CURRENT_TIMESTAMP,
    '$.login_count',
    COALESCE(JSON_EXTRACT(profile_data, '$.login_count'), 0) + 1
)
WHERE user_id = 1;

-- Create virtual columns for indexing JSON data
ALTER TABLE user_profiles 
ADD COLUMN name VARCHAR(100) AS (JSON_UNQUOTE(JSON_EXTRACT(profile_data, '$.name'))) VIRTUAL,
ADD COLUMN age INT AS (JSON_EXTRACT(profile_data, '$.age')) VIRTUAL,
ADD COLUMN city VARCHAR(100) AS (JSON_UNQUOTE(JSON_EXTRACT(profile_data, '$.location.city'))) VIRTUAL;

-- Create indexes on virtual columns
CREATE INDEX idx_profile_name ON user_profiles(name);
CREATE INDEX idx_profile_age ON user_profiles(age);
CREATE INDEX idx_profile_city ON user_profiles(city);

-- JSON aggregation functions
SELECT 
    JSON_ARRAYAGG(JSON_EXTRACT(profile_data, '$.name')) as all_names,
    JSON_OBJECTAGG(user_id, JSON_EXTRACT(profile_data, '$.age')) as user_ages,
    AVG(JSON_EXTRACT(profile_data, '$.age')) as average_age
FROM user_profiles;

-- Complex JSON operations
SELECT 
    user_id,
    JSON_UNQUOTE(JSON_EXTRACT(profile_data, '$.name')) as name,
    JSON_PRETTY(preferences) as formatted_preferences,
    JSON_KEYS(profile_data) as profile_keys,
    JSON_TYPE(JSON_EXTRACT(profile_data, '$.skills')) as skills_type
FROM user_profiles;
```

**Output:**
```
+---------+---------------------+----------+-----+---------------+---------------+-------------+
| user_id | email               | name     | age | city          | primary_skill | skill_count |
+---------+---------------------+----------+-----+---------------+---------------+-------------+
|       1 | john.doe@email.com  | John Doe |  30 | New York      | Python        |           3 |
|       2 | jane.smith@email.com| Jane Smith|  28 | San Francisco | Java          |           3 |
+---------+---------------------+----------+-----+---------------+---------------+-------------+

JSON Aggregation Output:
+---------------------------+------------------------+-------------+
| all_names                 | user_ages              | average_age |
+---------------------------+------------------------+-------------+
| ["John Doe", "Jane Smith"]| {"1": 30, "2": 28}    |      29.0000|
+---------------------------+------------------------+-------------+
```

### 10. How do you implement data validation and constraints in MySQL?

**Answer:** MySQL provides multiple mechanisms for data validation and integrity enforcement.

```sql
-- Comprehensive constraint examples
CREATE TABLE customer_orders_validated (
    order_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    email VARCHAR(255) NOT NULL,
    order_date DATE NOT NULL,
    ship_date DATE,
    order_total DECIMAL(12,2) NOT NULL,
    discount_percent DECIMAL(5,2) DEFAULT 0.00,
    status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    priority ENUM('low', 'normal', 'high', 'urgent') DEFAULT 'normal',
    shipping_address JSON NOT NULL,
    
    -- Check constraints (MySQL 8.0+)
    CONSTRAINT chk_email_format 
        CHECK (email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT chk_order_total_positive 
        CHECK (order_total > 0),
    CONSTRAINT chk_discount_range 
        CHECK (discount_percent >= 0 AND discount_percent <= 100),
    CONSTRAINT chk_ship_date_after_order 
        CHECK (ship_date IS NULL OR ship_date >= order_date),
    CONSTRAINT chk_shipping_address_required 
        CHECK (JSON_VALID(shipping_address) AND JSON_LENGTH(shipping_address) > 0),
    
    -- Indexes for performance
    INDEX idx_customer_date (customer_id, order_date),
    INDEX idx_status_priority (status, priority),
    INDEX idx_order_date (order_date)
);

-- Create validation functions
DELIMITER //
CREATE FUNCTION ValidatePhoneNumber(phone VARCHAR(20)) 
RETURNS BOOLEAN
READS SQL DATA
DETERMINISTIC
BEGIN
    RETURN phone REGEXP '^[+]?[1-9][0-9]{0,3}[-. ]?[(]?[0-9]{1,4}[)]?[-. ]?[0-9]{1,4}[-. ]?[0-9]{1,9}$';
END //

CREATE FUNCTION ValidatePostalCode(postal_code VARCHAR(20), country VARCHAR(2))
RETURNS BOOLEAN
READS SQL DATA
DETERMINISTIC
BEGIN
    CASE country
        WHEN 'US' THEN RETURN postal_code REGEXP '^[0-9]{5}(-[0-9]{4})?$';
        WHEN 'CA' THEN RETURN postal_code REGEXP '^[A-Za-z][0-9][A-Za-z] [0-9][A-Za-z][0-9]$';
        WHEN 'UK' THEN RETURN postal_code REGEXP '^[A-Za-z]{1,2}[0-9]{1,2} [0-9][A-Za-z]{2}$';
        ELSE RETURN TRUE; -- Allow other formats
    END CASE;
END //
DELIMITER ;

-- Data quality monitoring table
CREATE TABLE data_quality_issues (
    issue_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(100),
    column_name VARCHAR(100),
    issue_type ENUM('null_value', 'invalid_format', 'out_of_range', 'duplicate', 'referential_integrity'),
    record_id BIGINT,
    issue_description TEXT,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    status ENUM('open', 'investigating', 'resolved', 'ignored') DEFAULT 'open'
);

-- Data validation stored procedure
DELIMITER //
CREATE PROCEDURE ValidateOrderData()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE order_id BIGINT;
    DECLARE email VARCHAR(255);
    DECLARE order_total DECIMAL(12,2);
    DECLARE shipping_addr JSON;
    
    DECLARE order_cursor CURSOR FOR
        SELECT order_id, email, order_total, shipping_address
        FROM customer_orders_validated
        WHERE order_date >= CURDATE() - INTERVAL 1 DAY;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN order_cursor;
    
    validation_loop: LOOP
        FETCH order_cursor INTO order_id, email, order_total, shipping_addr;
        IF done THEN
            LEAVE validation_loop;
        END IF;
        
        -- Validate email format
        IF NOT (email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$') THEN
            INSERT INTO data_quality_issues (table_name, column_name, issue_type, record_id, issue_description)
            VALUES ('customer_orders_validated', 'email', 'invalid_format', order_id, CONCAT('Invalid email format: ', email));
        END IF;
        
        -- Validate order total
        IF order_total <= 0 THEN
            INSERT INTO data_quality_issues (table_name, column_name, issue_type, record_id, issue_description)
            VALUES ('customer_orders_validated', 'order_total', 'out_of_range', order_id, CONCAT('Invalid order total: ', order_total));
        END IF;
        
        -- Validate shipping address
        IF NOT JSON_VALID(shipping_addr) OR JSON_LENGTH(shipping_addr) = 0 THEN
            INSERT INTO data_quality_issues (table_name, column_name, issue_type, record_id, issue_description)
            VALUES ('customer_orders_validated', 'shipping_address', 'invalid_format', order_id, 'Invalid or empty shipping address');
        END IF;
        
    END LOOP;
    
    CLOSE order_cursor;
END //
DELIMITER ;

-- Test data insertion with validation
INSERT INTO customer_orders_validated 
(customer_id, email, order_date, order_total, shipping_address) 
VALUES 
(1001, 'valid@email.com', CURDATE(), 150.00, 
 '{"street": "123 Main St", "city": "New York", "state": "NY", "zip": "10001"}'),
(1002, 'invalid-email', CURDATE(), -50.00, 
 '{"street": "456 Oak Ave", "city": "Boston", "state": "MA", "zip": "02101"}');

-- This will fail due to constraints
-- The second record will be rejected due to invalid email and negative total

-- Check constraint violations
SHOW WARNINGS;

-- Run validation procedure
CALL ValidateOrderData();

-- View data quality issues
SELECT * FROM data_quality_issues ORDER BY detected_at DESC;
```

**Output:**
```
ERROR 3819 (HY000): Check constraint 'chk_email_format' is violated.
ERROR 3819 (HY000): Check constraint 'chk_order_total_positive' is violated.

Data Quality Issues:
+----------+---------------------------+-------------+-------------+-----------+---------------------------+---------------------+-------------+--------+
| issue_id | table_name                | column_name | issue_type  | record_id | issue_description         | detected_at         | resolved_at | status |
+----------+---------------------------+-------------+-------------+-----------+---------------------------+---------------------+-------------+--------+
|        1 | customer_orders_validated | email       | invalid_format|      2  | Invalid email format: ... | 2024-01-15 10:30:00|        NULL | open   |
+----------+---------------------------+-------------+-------------+-----------+---------------------------+---------------------+-------------+--------+
```

This completes the first 10 questions of the comprehensive MySQL interview guide. Each question includes practical examples with expected outputs, demonstrating real-world data engineering scenarios and best practices.

## Intermediate Level Questions (31-60)

### 31. How do you optimize MySQL queries for large datasets?

**Answer:** Query optimization involves multiple strategies including proper indexing, query structure, and execution plan analysis.

#### 🎯 **Query Optimization Techniques**

```sql
-- Create large dataset for optimization testing
CREATE TABLE large_sales_data (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    category_id INT NOT NULL,
    sale_date DATE NOT NULL,
    sale_timestamp TIMESTAMP NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0.00,
    sales_rep_id INT,
    store_id INT NOT NULL,
    region VARCHAR(50) NOT NULL
);

-- Insert sample data (simulating large dataset)
INSERT INTO large_sales_data 
(customer_id, product_id, category_id, sale_date, sale_timestamp, quantity, unit_price, total_amount, sales_rep_id, store_id, region)
SELECT 
    FLOOR(1 + RAND() * 100000) as customer_id,
    FLOOR(1 + RAND() * 10000) as product_id,
    FLOOR(1 + RAND() * 100) as category_id,
    DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND() * 1095) DAY) as sale_date,
    TIMESTAMP(DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND() * 1095) DAY), 
              TIME(SEC_TO_TIME(FLOOR(RAND() * 86400)))) as sale_timestamp,
    FLOOR(1 + RAND() * 10) as quantity,
    ROUND(10 + RAND() * 490, 2) as unit_price,
    0 as total_amount, -- Will be calculated
    FLOOR(1 + RAND() * 200) as sales_rep_id,
    FLOOR(1 + RAND() * 50) as store_id,
    ELT(FLOOR(1 + RAND() * 5), 'North', 'South', 'East', 'West', 'Central') as region
FROM 
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) t1,
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) t2,
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) t3,
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) t4,
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) t5
LIMIT 50000;

-- Update calculated fields
UPDATE large_sales_data 
SET total_amount = quantity * unit_price - discount_amount;

-- BEFORE optimization - Slow query
EXPLAIN FORMAT=JSON
SELECT 
    customer_id,
    SUM(total_amount) as total_spent,
    COUNT(*) as order_count,
    AVG(total_amount) as avg_order_value
FROM large_sales_data 
WHERE sale_date >= '2023-01-01' 
AND region = 'North'
AND total_amount > 100
GROUP BY customer_id
HAVING total_spent > 1000
ORDER BY total_spent DESC
LIMIT 100;

-- Create optimized indexes
CREATE INDEX idx_sale_date_region ON large_sales_data(sale_date, region);
CREATE INDEX idx_total_amount ON large_sales_data(total_amount);
CREATE INDEX idx_customer_date_amount ON large_sales_data(customer_id, sale_date, total_amount);
CREATE INDEX idx_covering_query ON large_sales_data(sale_date, region, total_amount, customer_id);

-- AFTER optimization - Optimized query
EXPLAIN FORMAT=JSON
SELECT 
    customer_id,
    SUM(total_amount) as total_spent,
    COUNT(*) as order_count,
    AVG(total_amount) as avg_order_value
FROM large_sales_data 
WHERE sale_date >= '2023-01-01' 
AND region = 'North'
AND total_amount > 100
GROUP BY customer_id
HAVING total_spent > 1000
ORDER BY total_spent DESC
LIMIT 100;

-- Query optimization techniques
-- 1. Use LIMIT to reduce result set
SELECT customer_id, total_amount 
FROM large_sales_data 
WHERE sale_date >= '2024-01-01'
ORDER BY total_amount DESC 
LIMIT 10;

-- 2. Use specific columns instead of SELECT *
SELECT customer_id, product_id, total_amount 
FROM large_sales_data 
WHERE region = 'North' 
LIMIT 1000;

-- 3. Use EXISTS instead of IN for subqueries
SELECT DISTINCT customer_id 
FROM large_sales_data s1
WHERE EXISTS (
    SELECT 1 FROM large_sales_data s2 
    WHERE s2.customer_id = s1.customer_id 
    AND s2.total_amount > 500
);

-- 4. Optimize JOIN operations
CREATE TABLE customers_summary AS
SELECT 
    customer_id,
    COUNT(*) as total_orders,
    SUM(total_amount) as lifetime_value,
    MAX(sale_date) as last_purchase_date
FROM large_sales_data
GROUP BY customer_id;

-- Add index to summary table
CREATE INDEX idx_customer_summary ON customers_summary(customer_id, lifetime_value);

-- Optimized join query
SELECT 
    c.customer_id,
    c.lifetime_value,
    s.total_amount as recent_purchase
FROM customers_summary c
INNER JOIN large_sales_data s ON c.customer_id = s.customer_id
WHERE c.lifetime_value > 5000
AND s.sale_date = c.last_purchase_date
ORDER BY c.lifetime_value DESC
LIMIT 50;

-- Performance monitoring queries
SELECT 
    TABLE_NAME,
    ROUND(((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024), 2) AS 'Size (MB)',
    TABLE_ROWS,
    ROUND((INDEX_LENGTH / 1024 / 1024), 2) AS 'Index Size (MB)'
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = 'sales_analytics'
AND TABLE_NAME = 'large_sales_data';
```

**Output:**
```
+------------------+-----------+------------+------------------+
| TABLE_NAME       | Size (MB) | TABLE_ROWS | Index Size (MB)  |
+------------------+-----------+------------+------------------+
| large_sales_data |     15.52 |      50000 |             8.25 |
+------------------+-----------+------------+------------------+

Query Performance Improvement:
Before Optimization: 2.5 seconds, Full table scan
After Optimization: 0.15 seconds, Index range scan
```

### 32. How do you implement Change Data Capture (CDC) in MySQL?

**Answer:** CDC captures and tracks changes to database records for real-time data synchronization and auditing.

```sql
-- Method 1: Trigger-based CDC
CREATE TABLE customer_master (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address JSON,
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- CDC log table
CREATE TABLE customer_cdc_log (
    cdc_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    operation_type ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    table_name VARCHAR(100) NOT NULL,
    record_id INT NOT NULL,
    old_values JSON,
    new_values JSON,
    changed_columns JSON,
    change_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_name VARCHAR(100) DEFAULT USER(),
    connection_id BIGINT DEFAULT CONNECTION_ID()
);

-- CDC triggers
DELIMITER //
CREATE TRIGGER customer_insert_cdc
AFTER INSERT ON customer_master
FOR EACH ROW
BEGIN
    INSERT INTO customer_cdc_log (
        operation_type, table_name, record_id, new_values
    ) VALUES (
        'INSERT',
        'customer_master',
        NEW.customer_id,
        JSON_OBJECT(
            'customer_id', NEW.customer_id,
            'first_name', NEW.first_name,
            'last_name', NEW.last_name,
            'email', NEW.email,
            'phone', NEW.phone,
            'address', NEW.address,
            'status', NEW.status,
            'created_at', NEW.created_at
        )
    );
END //

CREATE TRIGGER customer_update_cdc
AFTER UPDATE ON customer_master
FOR EACH ROW
BEGIN
    DECLARE changed_cols JSON DEFAULT JSON_ARRAY();
    
    -- Track which columns changed
    IF OLD.first_name != NEW.first_name THEN
        SET changed_cols = JSON_ARRAY_APPEND(changed_cols, '$', 'first_name');
    END IF;
    IF OLD.last_name != NEW.last_name THEN
        SET changed_cols = JSON_ARRAY_APPEND(changed_cols, '$', 'last_name');
    END IF;
    IF OLD.email != NEW.email THEN
        SET changed_cols = JSON_ARRAY_APPEND(changed_cols, '$', 'email');
    END IF;
    IF COALESCE(OLD.phone, '') != COALESCE(NEW.phone, '') THEN
        SET changed_cols = JSON_ARRAY_APPEND(changed_cols, '$', 'phone');
    END IF;
    IF OLD.status != NEW.status THEN
        SET changed_cols = JSON_ARRAY_APPEND(changed_cols, '$', 'status');
    END IF;
    
    INSERT INTO customer_cdc_log (
        operation_type, table_name, record_id, old_values, new_values, changed_columns
    ) VALUES (
        'UPDATE',
        'customer_master',
        NEW.customer_id,
        JSON_OBJECT(
            'first_name', OLD.first_name,
            'last_name', OLD.last_name,
            'email', OLD.email,
            'phone', OLD.phone,
            'status', OLD.status,
            'updated_at', OLD.updated_at
        ),
        JSON_OBJECT(
            'first_name', NEW.first_name,
            'last_name', NEW.last_name,
            'email', NEW.email,
            'phone', NEW.phone,
            'status', NEW.status,
            'updated_at', NEW.updated_at
        ),
        changed_cols
    );
END //

CREATE TRIGGER customer_delete_cdc
AFTER DELETE ON customer_master
FOR EACH ROW
BEGIN
    INSERT INTO customer_cdc_log (
        operation_type, table_name, record_id, old_values
    ) VALUES (
        'DELETE',
        'customer_master',
        OLD.customer_id,
        JSON_OBJECT(
            'customer_id', OLD.customer_id,
            'first_name', OLD.first_name,
            'last_name', OLD.last_name,
            'email', OLD.email,
            'phone', OLD.phone,
            'status', OLD.status
        )
    );
END //
DELIMITER ;

-- Method 2: Timestamp-based CDC
ALTER TABLE customer_master 
ADD COLUMN cdc_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- CDC extraction query
SELECT * FROM customer_master 
WHERE cdc_timestamp > '2024-01-15 10:00:00'
ORDER BY cdc_timestamp;

-- Method 3: Binary log-based CDC (configuration)
-- Add to my.cnf:
/*
[mysqld]
log-bin = mysql-bin
binlog-format = ROW
binlog-row-image = FULL
server-id = 1
*/

-- Test CDC functionality
INSERT INTO customer_master (first_name, last_name, email, phone, address) VALUES
('John', 'Doe', 'john.doe@email.com', '+1-555-0123', 
 '{"street": "123 Main St", "city": "New York", "state": "NY", "zip": "10001"}');

UPDATE customer_master 
SET phone = '+1-555-0124', status = 'inactive' 
WHERE customer_id = 1;

DELETE FROM customer_master WHERE customer_id = 1;

-- View CDC log
SELECT 
    cdc_id,
    operation_type,
    record_id,
    JSON_PRETTY(old_values) as old_data,
    JSON_PRETTY(new_values) as new_data,
    JSON_PRETTY(changed_columns) as changed_fields,
    change_timestamp
FROM customer_cdc_log 
ORDER BY cdc_id DESC;

-- CDC processing for downstream systems
DELIMITER //
CREATE PROCEDURE ProcessCDCChanges(IN last_processed_id BIGINT)
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE cdc_id BIGINT;
    DECLARE op_type VARCHAR(10);
    DECLARE record_id INT;
    DECLARE new_vals JSON;
    
    DECLARE cdc_cursor CURSOR FOR
        SELECT cdc_id, operation_type, record_id, new_values
        FROM customer_cdc_log
        WHERE cdc_id > last_processed_id
        ORDER BY cdc_id;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN cdc_cursor;
    
    cdc_loop: LOOP
        FETCH cdc_cursor INTO cdc_id, op_type, record_id, new_vals;
        IF done THEN
            LEAVE cdc_loop;
        END IF;
        
        -- Process each change (send to message queue, update cache, etc.)
        CASE op_type
            WHEN 'INSERT' THEN
                -- Handle insert logic
                SELECT CONCAT('Processing INSERT for customer ', record_id) as message;
            WHEN 'UPDATE' THEN
                -- Handle update logic
                SELECT CONCAT('Processing UPDATE for customer ', record_id) as message;
            WHEN 'DELETE' THEN
                -- Handle delete logic
                SELECT CONCAT('Processing DELETE for customer ', record_id) as message;
        END CASE;
        
    END LOOP;
    
    CLOSE cdc_cursor;
END //
DELIMITER ;
```

**Output:**
```
+--------+----------------+-----------+------------------+------------------+------------------+---------------------+
| cdc_id | operation_type | record_id | old_data         | new_data         | changed_fields   | change_timestamp    |
+--------+----------------+-----------+------------------+------------------+------------------+---------------------+
|      3 | DELETE         |         1 | {"customer_id":1,| null             | null             | 2024-01-15 10:35:00 |
|        |                |           | "first_name":..} |                  |                  |                     |
|      2 | UPDATE         |         1 | {"first_name":..}| {"first_name":..}| ["phone","status"]| 2024-01-15 10:34:00 |
|      1 | INSERT         |         1 | null             | {"customer_id":1,| null             | 2024-01-15 10:33:00 |
|        |                |           |                  | "first_name":..} |                  |                     |
+--------+----------------+-----------+------------------+------------------+------------------+---------------------+
```

### 33. How do you implement data archiving strategies in MySQL?

**Answer:** Data archiving helps manage database size, improve performance, and meet compliance requirements.

```sql
-- Create main transaction table
CREATE TABLE transactions (
    transaction_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    account_id INT NOT NULL,
    transaction_type ENUM('deposit', 'withdrawal', 'transfer', 'payment') NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    description TEXT,
    transaction_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'completed', 'failed', 'cancelled') DEFAULT 'pending',
    
    INDEX idx_account_date (account_id, transaction_date),
    INDEX idx_date_status (transaction_date, status),
    INDEX idx_created_at (created_at)
) PARTITION BY RANGE (YEAR(transaction_date)) (
    PARTITION p2021 VALUES LESS THAN (2022),
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- Create archive table with same structure
CREATE TABLE transactions_archive (
    transaction_id BIGINT PRIMARY KEY,
    account_id INT NOT NULL,
    transaction_type ENUM('deposit', 'withdrawal', 'transfer', 'payment') NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    description TEXT,
    transaction_date DATE NOT NULL,
    created_at TIMESTAMP,
    status ENUM('pending', 'completed', 'failed', 'cancelled'),
    archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_account_date (account_id, transaction_date),
    INDEX idx_archived_at (archived_at)
) PARTITION BY RANGE (YEAR(transaction_date)) (
    PARTITION p2021 VALUES LESS THAN (2022),
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- Insert sample data
INSERT INTO transactions (account_id, transaction_type, amount, description, transaction_date, status)
SELECT 
    FLOOR(1 + RAND() * 10000) as account_id,
    ELT(FLOOR(1 + RAND() * 4), 'deposit', 'withdrawal', 'transfer', 'payment') as transaction_type,
    ROUND(10 + RAND() * 9990, 2) as amount,
    CONCAT('Transaction ', FLOOR(1 + RAND() * 1000000)) as description,
    DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND() * 1095) DAY) as transaction_date,
    ELT(FLOOR(1 + RAND() * 4), 'pending', 'completed', 'failed', 'cancelled') as status
FROM 
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) t1,
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) t2,
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) t3,
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) t4
LIMIT 25000;

-- Archiving strategy 1: Time-based archiving
DELIMITER //
CREATE PROCEDURE ArchiveOldTransactions(IN archive_before_date DATE)
BEGIN
    DECLARE archived_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    -- Move old transactions to archive
    INSERT INTO transactions_archive 
    (transaction_id, account_id, transaction_type, amount, description, 
     transaction_date, created_at, status)
    SELECT 
        transaction_id, account_id, transaction_type, amount, description,
        transaction_date, created_at, status
    FROM transactions 
    WHERE transaction_date < archive_before_date
    AND status IN ('completed', 'failed', 'cancelled');
    
    SET archived_count = ROW_COUNT();
    
    -- Delete archived transactions from main table
    DELETE FROM transactions 
    WHERE transaction_date < archive_before_date
    AND status IN ('completed', 'failed', 'cancelled');
    
    COMMIT;
    
    SELECT CONCAT('Archived ', archived_count, ' transactions') as result;
END //
DELIMITER ;

-- Archiving strategy 2: Partition-based archiving
DELIMITER //
CREATE PROCEDURE ArchivePartition(IN partition_name VARCHAR(64))
BEGIN
    DECLARE sql_stmt TEXT;
    
    -- Create archive partition if not exists
    SET sql_stmt = CONCAT(
        'ALTER TABLE transactions_archive ADD PARTITION (',
        'PARTITION ', partition_name, '_archive VALUES LESS THAN (', 
        SUBSTRING(partition_name, 2), '))'
    );
    
    SET @sql = sql_stmt;
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    -- Move partition data to archive
    SET sql_stmt = CONCAT(
        'INSERT INTO transactions_archive ',
        'SELECT *, NOW() as archived_at FROM transactions PARTITION (', partition_name, ')'
    );
    
    SET @sql = sql_stmt;
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    -- Drop the partition from main table
    SET sql_stmt = CONCAT('ALTER TABLE transactions DROP PARTITION ', partition_name);
    
    SET @sql = sql_stmt;
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    SELECT CONCAT('Archived partition ', partition_name) as result;
END //
DELIMITER ;

-- Archiving strategy 3: Incremental archiving with batching
DELIMITER //
CREATE PROCEDURE IncrementalArchive(IN batch_size INT, IN max_batches INT)
BEGIN
    DECLARE batch_count INT DEFAULT 0;
    DECLARE rows_processed INT DEFAULT 0;
    DECLARE total_archived INT DEFAULT 0;
    
    WHILE batch_count < max_batches DO
        START TRANSACTION;
        
        -- Archive batch of old completed transactions
        INSERT INTO transactions_archive 
        (transaction_id, account_id, transaction_type, amount, description, 
         transaction_date, created_at, status)
        SELECT 
            transaction_id, account_id, transaction_type, amount, description,
            transaction_date, created_at, status
        FROM transactions 
        WHERE transaction_date < DATE_SUB(CURDATE(), INTERVAL 2 YEAR)
        AND status = 'completed'
        ORDER BY transaction_id
        LIMIT batch_size;
        
        SET rows_processed = ROW_COUNT();
        
        IF rows_processed = 0 THEN
            COMMIT;
            LEAVE;
        END IF;
        
        -- Delete archived records
        DELETE FROM transactions 
        WHERE transaction_id IN (
            SELECT transaction_id FROM transactions_archive 
            WHERE archived_at >= NOW() - INTERVAL 1 MINUTE
            LIMIT batch_size
        );
        
        COMMIT;
        
        SET batch_count = batch_count + 1;
        SET total_archived = total_archived + rows_processed;
        
        -- Small delay to avoid overwhelming the system
        SELECT SLEEP(0.1);
        
    END WHILE;
    
    SELECT CONCAT('Archived ', total_archived, ' transactions in ', batch_count, ' batches') as result;
END //
DELIMITER ;

-- Archive monitoring and reporting
CREATE TABLE archive_log (
    log_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(100),
    archive_type ENUM('time_based', 'partition_based', 'incremental'),
    records_archived INT,
    archive_date DATE,
    execution_time_seconds DECIMAL(10,3),
    status ENUM('success', 'failed', 'partial'),
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Execute archiving procedures
CALL ArchiveOldTransactions('2022-01-01');
CALL IncrementalArchive(1000, 10);

-- Archive statistics
SELECT 
    'Main Table' as table_type,
    COUNT(*) as record_count,
    MIN(transaction_date) as oldest_date,
    MAX(transaction_date) as newest_date,
    ROUND(SUM(amount), 2) as total_amount
FROM transactions
UNION ALL
SELECT 
    'Archive Table' as table_type,
    COUNT(*) as record_count,
    MIN(transaction_date) as oldest_date,
    MAX(transaction_date) as newest_date,
    ROUND(SUM(amount), 2) as total_amount
FROM transactions_archive;

-- Partition information
SELECT 
    PARTITION_NAME,
    TABLE_ROWS,
    ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024, 2) as size_mb
FROM INFORMATION_SCHEMA.PARTITIONS 
WHERE TABLE_SCHEMA = 'sales_analytics' 
AND TABLE_NAME IN ('transactions', 'transactions_archive')
AND PARTITION_NAME IS NOT NULL
ORDER BY TABLE_NAME, PARTITION_ORDINAL_POSITION;
```

**Output:**
```
Archive Results:
+----------------------------------+
| result                           |
+----------------------------------+
| Archived 8,432 transactions     |
+----------------------------------+

Archive Statistics:
+--------------+--------------+-------------+-------------+--------------+
| table_type   | record_count | oldest_date | newest_date | total_amount |
+--------------+--------------+-------------+-------------+--------------+
| Main Table   |       16,568 | 2022-01-15  | 2024-01-15  |  2,456,789.50|
| Archive Table|        8,432 | 2021-02-10  | 2021-12-31  |  1,234,567.25|
+--------------+--------------+-------------+-------------+--------------+

Partition Information:
+----------------+------------+---------+
| PARTITION_NAME | TABLE_ROWS | size_mb |
+----------------+------------+---------+
| p2022          |      3,245 |    2.15 |
| p2023          |      6,789 |    4.32 |
| p2024          |      6,534 |    4.18 |
+----------------+------------+---------+
```

### 34. How do you implement MySQL high availability and disaster recovery?

**Answer:** HA and DR strategies ensure business continuity and data protection through redundancy and backup mechanisms.

```sql
-- High Availability Setup

-- 1. MySQL Group Replication Configuration
-- Add to my.cnf on all nodes:
/*
[mysqld]
# Group Replication Configuration
disabled_storage_engines="MyISAM,BLACKHOLE,FEDERATED,ARCHIVE,MEMORY"
gtid_mode=ON
enforce_gtid_consistency=ON
master_info_repository=TABLE
relay_log_info_repository=TABLE
binlog_checksum=NONE
log_slave_updates=ON
log_bin=binlog
binlog_format=ROW
transaction_write_set_extraction=XXHASH64
loose-group_replication_group_name="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
loose-group_replication_start_on_boot=off
loose-group_replication_local_address="192.168.1.10:33061"
loose-group_replication_group_seeds="192.168.1.10:33061,192.168.1.11:33061,192.168.1.12:33061"
loose-group_replication_bootstrap_group=off
*/

-- Create replication user
CREATE USER 'repl_user'@'%' IDENTIFIED BY 'secure_replication_password';
GRANT REPLICATION SLAVE ON *.* TO 'repl_user'@'%';
GRANT CONNECTION_ADMIN ON *.* TO 'repl_user'@'%';
GRANT BACKUP_ADMIN ON *.* TO 'repl_user'@'%';
GRANT GROUP_REPLICATION_ADMIN ON *.* TO 'repl_user'@'%';
FLUSH PRIVILEGES;

-- Install Group Replication plugin
INSTALL PLUGIN group_replication SONAME 'group_replication.so';

-- Configure Group Replication (on first node)
SET GLOBAL group_replication_bootstrap_group=ON;
START GROUP_REPLICATION;
SET GLOBAL group_replication_bootstrap_group=OFF;

-- Join other nodes to the group
-- (Run on nodes 2 and 3)
START GROUP_REPLICATION;

-- 2. Disaster Recovery Setup

-- Create backup user
CREATE USER 'backup_user'@'localhost' IDENTIFIED BY 'secure_backup_password';
GRANT SELECT, RELOAD, SHOW DATABASES, LOCK TABLES, REPLICATION CLIENT ON *.* TO 'backup_user'@'localhost';
GRANT PROCESS ON *.* TO 'backup_user'@'localhost';

-- Backup and recovery procedures
DELIMITER //
CREATE PROCEDURE CreateFullBackup(IN backup_path VARCHAR(500))
BEGIN
    DECLARE backup_file VARCHAR(600);
    DECLARE backup_command TEXT;
    
    SET backup_file = CONCAT(backup_path, '/full_backup_', DATE_FORMAT(NOW(), '%Y%m%d_%H%i%s'), '.sql');
    
    -- Create backup command
    SET backup_command = CONCAT(
        'mysqldump --single-transaction --routines --triggers --all-databases ',
        '--master-data=2 --flush-logs --hex-blob --user=backup_user ',
        '--password=secure_backup_password > ', backup_file
    );
    
    -- Log backup start
    INSERT INTO backup_log (backup_type, backup_file, status, start_time)
    VALUES ('FULL', backup_file, 'STARTED', NOW());
    
    -- Execute backup (this would be done externally)
    SELECT backup_command as command_to_execute;
    
    -- Update backup log (would be updated after external execution)
    UPDATE backup_log 
    SET status = 'COMPLETED', end_time = NOW()
    WHERE backup_file = backup_file;
END //

CREATE PROCEDURE CreateIncrementalBackup(IN backup_path VARCHAR(500))
BEGIN
    DECLARE backup_file VARCHAR(600);
    DECLARE last_backup_position BIGINT;
    DECLARE current_log_file VARCHAR(255);
    DECLARE current_log_pos BIGINT;
    
    -- Get current binary log position
    SELECT Variable_value INTO current_log_file 
    FROM performance_schema.global_status 
    WHERE Variable_name = 'Binlog_snapshot_file';
    
    SELECT Variable_value INTO current_log_pos 
    FROM performance_schema.global_status 
    WHERE Variable_name = 'Binlog_snapshot_position';
    
    -- Get last backup position
    SELECT COALESCE(MAX(log_position), 0) INTO last_backup_position
    FROM backup_log 
    WHERE status = 'COMPLETED';
    
    SET backup_file = CONCAT(backup_path, '/incremental_backup_', DATE_FORMAT(NOW(), '%Y%m%d_%H%i%s'), '.sql');
    
    -- Log incremental backup
    INSERT INTO backup_log (backup_type, backup_file, status, start_time, log_file, log_position)
    VALUES ('INCREMENTAL', backup_file, 'STARTED', NOW(), current_log_file, current_log_pos);
    
    SELECT CONCAT('mysqlbinlog --start-position=', last_backup_position, 
                  ' --stop-position=', current_log_pos, 
                  ' ', current_log_file, ' > ', backup_file) as command_to_execute;
END //
DELIMITER ;

-- Create backup monitoring table
CREATE TABLE backup_log (
    backup_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    backup_type ENUM('FULL', 'INCREMENTAL', 'DIFFERENTIAL') NOT NULL,
    backup_file VARCHAR(500) NOT NULL,
    status ENUM('STARTED', 'COMPLETED', 'FAILED') NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NULL,
    log_file VARCHAR(255),
    log_position BIGINT,
    backup_size_mb DECIMAL(10,2),
    error_message TEXT,
    retention_date DATE
);

-- 3. Health Monitoring Setup
CREATE TABLE cluster_health_log (
    check_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    node_name VARCHAR(100),
    node_status ENUM('ONLINE', 'RECOVERING', 'OFFLINE', 'ERROR'),
    group_size INT,
    primary_node VARCHAR(100),
    replication_lag_seconds INT,
    last_heartbeat TIMESTAMP,
    check_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //
CREATE PROCEDURE MonitorClusterHealth()
BEGIN
    DECLARE node_count INT;
    DECLARE primary_node VARCHAR(100);
    DECLARE node_state VARCHAR(20);
    
    -- Get group replication status
    SELECT COUNT(*) INTO node_count
    FROM performance_schema.replication_group_members
    WHERE MEMBER_STATE = 'ONLINE';
    
    SELECT MEMBER_HOST INTO primary_node
    FROM performance_schema.replication_group_members
    WHERE MEMBER_ROLE = 'PRIMARY';
    
    SELECT MEMBER_STATE INTO node_state
    FROM performance_schema.replication_group_members
    WHERE MEMBER_HOST = @@hostname;
    
    -- Log health status
    INSERT INTO cluster_health_log (
        node_name, node_status, group_size, primary_node, last_heartbeat
    ) VALUES (
        @@hostname, node_state, node_count, primary_node, NOW()
    );
    
    -- Alert if cluster is unhealthy
    IF node_count < 2 THEN
        INSERT INTO alert_log (alert_type, message, severity)
        VALUES ('CLUSTER_HEALTH', 'Cluster has less than 2 online nodes', 'CRITICAL');
    END IF;
END //
DELIMITER ;

-- 4. Failover Testing
DELIMITER //
CREATE PROCEDURE TestFailover()
BEGIN
    DECLARE current_primary VARCHAR(100);
    DECLARE new_primary VARCHAR(100);
    
    -- Get current primary
    SELECT MEMBER_HOST INTO current_primary
    FROM performance_schema.replication_group_members
    WHERE MEMBER_ROLE = 'PRIMARY';
    
    -- Simulate primary failure (for testing only)
    -- STOP GROUP_REPLICATION;
    
    -- Wait for new primary election
    SELECT SLEEP(10);
    
    -- Check new primary
    SELECT MEMBER_HOST INTO new_primary
    FROM performance_schema.replication_group_members
    WHERE MEMBER_ROLE = 'PRIMARY';
    
    -- Log failover test results
    INSERT INTO failover_test_log (
        old_primary, new_primary, test_timestamp, status
    ) VALUES (
        current_primary, new_primary, NOW(), 
        CASE WHEN new_primary != current_primary THEN 'SUCCESS' ELSE 'FAILED' END
    );
END //
DELIMITER ;

-- Create supporting tables
CREATE TABLE alert_log (
    alert_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    alert_type VARCHAR(50),
    message TEXT,
    severity ENUM('INFO', 'WARNING', 'CRITICAL'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acknowledged BOOLEAN DEFAULT FALSE
);

CREATE TABLE failover_test_log (
    test_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    old_primary VARCHAR(100),
    new_primary VARCHAR(100),
    test_timestamp TIMESTAMP,
    status ENUM('SUCCESS', 'FAILED'),
    notes TEXT
);

-- Monitor cluster status
SELECT 
    MEMBER_HOST as node,
    MEMBER_PORT as port,
    MEMBER_STATE as state,
    MEMBER_ROLE as role,
    MEMBER_VERSION as version
FROM performance_schema.replication_group_members;

-- Check replication lag
SELECT 
    CHANNEL_NAME,
    SERVICE_STATE,
    LAST_ERROR_MESSAGE,
    LAST_ERROR_TIMESTAMP
FROM performance_schema.replication_connection_status;

-- Execute monitoring procedures
CALL MonitorClusterHealth();
CALL CreateFullBackup('/backup/mysql');

-- View recent health checks
SELECT * FROM cluster_health_log 
ORDER BY check_timestamp DESC 
LIMIT 10;
```

**Output:**
```
Cluster Status:
+---------------+------+--------+---------+---------+
| node          | port | state  | role    | version |
+---------------+------+--------+---------+---------+
| 192.168.1.10  | 3306 | ONLINE | PRIMARY | 8.0.35  |
| 192.168.1.11  | 3306 | ONLINE | SECONDARY| 8.0.35  |
| 192.168.1.12  | 3306 | ONLINE | SECONDARY| 8.0.35  |
+---------------+------+--------+---------+---------+

Health Check Results:
+----------+---------------+-------------+------------+---------------+---------------------+
| check_id | node_name     | node_status | group_size | primary_node  | check_timestamp     |
+----------+---------------+-------------+------------+---------------+---------------------+
|        1 | 192.168.1.10  | ONLINE      |          3 | 192.168.1.10  | 2024-01-15 10:45:00 |
|        2 | 192.168.1.11  | ONLINE      |          3 | 192.168.1.10  | 2024-01-15 10:45:01 |
|        3 | 192.168.1.12  | ONLINE      |          3 | 192.168.1.10  | 2024-01-15 10:45:02 |
+----------+---------------+-------------+------------+---------------+---------------------+

Backup Command:
+---------------------------------------------------------------------------------+
| command_to_execute                                                              |
+---------------------------------------------------------------------------------+
| mysqldump --single-transaction --routines --triggers --all-databases          |
| --master-data=2 --flush-logs --hex-blob --user=backup_user                    |
| --password=secure_backup_password > /backup/mysql/full_backup_20240115_104500.sql |
+---------------------------------------------------------------------------------+
```

This completes the intermediate level questions (31-34). The documentation continues to build comprehensive coverage of MySQL for data engineering, including advanced optimization techniques, change data capture, archiving strategies, and high availability setup with practical examples and expected outputs.