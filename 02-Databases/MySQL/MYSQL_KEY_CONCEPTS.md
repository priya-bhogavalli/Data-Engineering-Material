# MySQL Key Concepts

## 1. MySQL Architecture
**Storage Engines**:
- **InnoDB**: Default, ACID compliant, row-level locking
- **MyISAM**: Fast reads, table-level locking
- **Memory**: In-memory storage
- **Archive**: Compressed storage for archival

```sql
-- Check available engines
SHOW ENGINES;

-- Create table with specific engine
CREATE TABLE sales (
    id INT PRIMARY KEY AUTO_INCREMENT,
    amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;
```

## 2. Data Types and Schema Design
```sql
-- Numeric types
CREATE TABLE products (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    price DECIMAL(10,2) NOT NULL,
    quantity SMALLINT UNSIGNED DEFAULT 0,
    weight FLOAT(7,2),
    is_active BOOLEAN DEFAULT TRUE
);

-- String types
CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    description TEXT,
    status ENUM('active', 'inactive', 'pending') DEFAULT 'pending'
);

-- Date and time types
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    delivery_time TIME
);

-- JSON type (MySQL 5.7+)
CREATE TABLE user_preferences (
    user_id INT PRIMARY KEY,
    settings JSON,
    metadata JSON
);

-- Insert JSON data
INSERT INTO user_preferences VALUES 
(1, '{"theme": "dark", "notifications": true}', '{"last_login": "2024-01-15"}');

-- Query JSON data
SELECT user_id, JSON_EXTRACT(settings, '$.theme') as theme
FROM user_preferences
WHERE JSON_EXTRACT(settings, '$.notifications') = true;
```

## 3. Indexing and Performance
```sql
-- Primary key (clustered index)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(100)
);

-- Secondary indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_name ON users(name);

-- Composite index
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- Unique index
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);

-- Partial index (functional)
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';

-- Full-text index
CREATE TABLE articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    FULLTEXT(title, content)
);

-- Full-text search
SELECT * FROM articles 
WHERE MATCH(title, content) AGAINST('data engineering' IN NATURAL LANGUAGE MODE);

-- Check index usage
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';
SHOW INDEX FROM users;
```

## 4. Joins and Relationships
```sql
-- Inner join
SELECT u.name, o.order_date, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.order_date >= '2024-01-01';

-- Left join with aggregation
SELECT 
    u.name,
    COUNT(o.id) as order_count,
    COALESCE(SUM(o.total), 0) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name
HAVING total_spent > 1000;

-- Self join
SELECT 
    e1.name as employee,
    e2.name as manager
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.id;

-- Multiple joins
SELECT 
    u.name,
    o.order_date,
    p.product_name,
    oi.quantity,
    oi.price
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE o.order_date >= DATE_SUB(NOW(), INTERVAL 30 DAY);
```

## 5. Advanced Queries
```sql
-- Window functions (MySQL 8.0+)
SELECT 
    user_id,
    order_date,
    total,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_date) as order_sequence,
    SUM(total) OVER (PARTITION BY user_id ORDER BY order_date) as running_total,
    LAG(total) OVER (PARTITION BY user_id ORDER BY order_date) as previous_order
FROM orders;

-- Common Table Expressions (CTE)
WITH monthly_sales AS (
    SELECT 
        DATE_FORMAT(order_date, '%Y-%m') as month,
        SUM(total) as monthly_total
    FROM orders
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
),
growth_analysis AS (
    SELECT 
        month,
        monthly_total,
        LAG(monthly_total) OVER (ORDER BY month) as previous_month,
        (monthly_total - LAG(monthly_total) OVER (ORDER BY month)) / 
        LAG(monthly_total) OVER (ORDER BY month) * 100 as growth_rate
    FROM monthly_sales
)
SELECT * FROM growth_analysis WHERE growth_rate > 10;

-- Recursive CTE (MySQL 8.0+)
WITH RECURSIVE employee_hierarchy AS (
    SELECT id, name, manager_id, 1 as level
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    SELECT e.id, e.name, e.manager_id, eh.level + 1
    FROM employees e
    JOIN employee_hierarchy eh ON e.manager_id = eh.id
)
SELECT * FROM employee_hierarchy ORDER BY level, name;

-- Subqueries
SELECT name, email
FROM users
WHERE id IN (
    SELECT DISTINCT user_id
    FROM orders
    WHERE total > (SELECT AVG(total) FROM orders)
);
```

## 6. Stored Procedures and Functions
```sql
-- Stored procedure
DELIMITER //
CREATE PROCEDURE GetCustomerOrders(IN customer_id INT)
BEGIN
    SELECT 
        o.id,
        o.order_date,
        o.total,
        COUNT(oi.id) as item_count
    FROM orders o
    LEFT JOIN order_items oi ON o.id = oi.order_id
    WHERE o.user_id = customer_id
    GROUP BY o.id, o.order_date, o.total
    ORDER BY o.order_date DESC;
END //
DELIMITER ;

-- Call procedure
CALL GetCustomerOrders(123);

-- Function
DELIMITER //
CREATE FUNCTION CalculateDiscount(order_total DECIMAL(10,2))
RETURNS DECIMAL(10,2)
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE discount DECIMAL(10,2) DEFAULT 0;
    
    IF order_total >= 1000 THEN
        SET discount = order_total * 0.10;
    ELSEIF order_total >= 500 THEN
        SET discount = order_total * 0.05;
    END IF;
    
    RETURN discount;
END //
DELIMITER ;

-- Use function
SELECT 
    id,
    total,
    CalculateDiscount(total) as discount,
    total - CalculateDiscount(total) as final_amount
FROM orders;

-- Trigger
DELIMITER //
CREATE TRIGGER update_inventory
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    UPDATE products 
    SET quantity = quantity - NEW.quantity
    WHERE id = NEW.product_id;
END //
DELIMITER ;
```

## 7. Transactions and Locking
```sql
-- Transaction control
START TRANSACTION;

INSERT INTO orders (user_id, total) VALUES (1, 100.00);
SET @order_id = LAST_INSERT_ID();

INSERT INTO order_items (order_id, product_id, quantity, price) 
VALUES (@order_id, 1, 2, 50.00);

UPDATE products SET quantity = quantity - 2 WHERE id = 1;

COMMIT;

-- Rollback on error
START TRANSACTION;

INSERT INTO accounts (name, balance) VALUES ('Alice', 1000);
INSERT INTO accounts (name, balance) VALUES ('Bob', 500);

-- If error occurs
ROLLBACK;

-- Savepoints
START TRANSACTION;

INSERT INTO orders (user_id, total) VALUES (1, 100);
SAVEPOINT order_created;

INSERT INTO order_items (order_id, product_id, quantity) VALUES (1, 1, 2);
-- If this fails, rollback to savepoint
ROLLBACK TO order_created;

COMMIT;

-- Locking
-- Shared lock
SELECT * FROM products WHERE id = 1 LOCK IN SHARE MODE;

-- Exclusive lock
SELECT * FROM products WHERE id = 1 FOR UPDATE;

-- Check locks
SHOW ENGINE INNODB STATUS;
```

## 8. Replication and High Availability
```sql
-- Master configuration (my.cnf)
[mysqld]
server-id = 1
log-bin = mysql-bin
binlog-format = ROW
gtid-mode = ON
enforce-gtid-consistency = ON

-- Slave configuration
[mysqld]
server-id = 2
relay-log = relay-bin
read-only = 1
gtid-mode = ON
enforce-gtid-consistency = ON

-- Setup replication
-- On master
CREATE USER 'replication'@'%' IDENTIFIED BY 'password';
GRANT REPLICATION SLAVE ON *.* TO 'replication'@'%';

-- On slave
CHANGE MASTER TO
    MASTER_HOST='master-server',
    MASTER_USER='replication',
    MASTER_PASSWORD='password',
    MASTER_AUTO_POSITION=1;

START SLAVE;

-- Check replication status
SHOW SLAVE STATUS\G
SHOW MASTER STATUS;

-- Group Replication (MySQL 5.7+)
SET GLOBAL group_replication_group_name="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa";
SET GLOBAL group_replication_start_on_boot=off;
SET GLOBAL group_replication_local_address="node1:33061";
SET GLOBAL group_replication_group_seeds="node1:33061,node2:33061,node3:33061";
SET GLOBAL group_replication_bootstrap_group=on;
START GROUP_REPLICATION;
```

## 9. Performance Optimization
```sql
-- Query optimization
-- Use EXPLAIN to analyze queries
EXPLAIN FORMAT=JSON 
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

-- Optimize with covering index
CREATE INDEX idx_orders_user_covering ON orders(user_id, id);

-- Partition tables for large datasets
CREATE TABLE sales_partitioned (
    id INT AUTO_INCREMENT,
    sale_date DATE NOT NULL,
    amount DECIMAL(10,2),
    PRIMARY KEY (id, sale_date)
) PARTITION BY RANGE (YEAR(sale_date)) (
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- Configuration optimization
-- my.cnf settings
[mysqld]
innodb_buffer_pool_size = 2G
innodb_log_file_size = 256M
innodb_flush_log_at_trx_commit = 2
query_cache_size = 128M
max_connections = 200
tmp_table_size = 64M
max_heap_table_size = 64M

-- Monitor performance
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_read%';
SHOW GLOBAL STATUS LIKE 'Slow_queries';
SHOW PROCESSLIST;

-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;
```

## 10. Backup and Recovery
```bash
# Full backup with mysqldump
mysqldump -u root -p --single-transaction --routines --triggers \
  --all-databases > full_backup.sql

# Backup specific database
mysqldump -u root -p --single-transaction database_name > db_backup.sql

# Backup with compression
mysqldump -u root -p --single-transaction --all-databases | gzip > backup.sql.gz

# Point-in-time recovery
mysqldump -u root -p --single-transaction --flush-logs --master-data=2 \
  --all-databases > backup_with_binlog.sql

# Binary log backup
mysqlbinlog mysql-bin.000001 > binlog_backup.sql

# Restore from backup
mysql -u root -p < full_backup.sql

# Incremental restore using binary logs
mysql -u root -p -e "STOP SLAVE;"
mysql -u root -p < full_backup.sql
mysqlbinlog --start-datetime="2024-01-15 10:00:00" \
  --stop-datetime="2024-01-15 11:00:00" \
  mysql-bin.000001 | mysql -u root -p

# Physical backup with Percona XtraBackup
xtrabackup --backup --target-dir=/backup/full/
xtrabackup --prepare --target-dir=/backup/full/
xtrabackup --copy-back --target-dir=/backup/full/
```

```sql
-- Monitoring and maintenance
-- Check table status
SHOW TABLE STATUS LIKE 'orders';

-- Analyze table statistics
ANALYZE TABLE orders;

-- Optimize table
OPTIMIZE TABLE orders;

-- Check and repair tables
CHECK TABLE orders;
REPAIR TABLE orders;

-- Monitor replication lag
SELECT 
    TIMESTAMPDIFF(SECOND, 
        STR_TO_DATE(SUBSTRING_INDEX(SUBSTRING_INDEX(@@global.gtid_executed, ':', -1), '-', 1), '%Y%m%d%H%i%s'),
        NOW()
    ) as replication_lag_seconds;

-- Database size monitoring
SELECT 
    table_schema as database_name,
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as size_mb
FROM information_schema.tables
GROUP BY table_schema
ORDER BY size_mb DESC;
```