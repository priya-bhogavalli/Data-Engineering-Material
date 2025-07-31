# Database Key Concepts for Data Engineering

## 1. ACID Properties
**What they are**: Fundamental properties that guarantee reliable database transactions.

**Why important**: Ensures data integrity and consistency in database operations, critical for data engineering pipelines.

**Atomicity**: All operations in a transaction succeed or fail together
**Consistency**: Database remains in valid state before and after transaction
**Isolation**: Concurrent transactions don't interfere with each other
**Durability**: Committed changes persist even after system failure

```sql
-- Example: Bank transfer transaction
BEGIN TRANSACTION;
    UPDATE accounts SET balance = balance - 100 WHERE account_id = 'A001';
    UPDATE accounts SET balance = balance + 100 WHERE account_id = 'A002';
    
    -- If any operation fails, entire transaction rolls back
    IF @@ERROR <> 0
        ROLLBACK TRANSACTION;
    ELSE
        COMMIT TRANSACTION;
```

## 2. Database Normalization
**What it is**: Process of organizing data to reduce redundancy and improve integrity.

**1NF (First Normal Form)**:
- Atomic values only
- No repeating groups

**2NF (Second Normal Form)**:
- Must be in 1NF
- No partial dependencies on composite keys

**3NF (Third Normal Form)**:
- Must be in 2NF
- No transitive dependencies

```sql
-- Unnormalized table
CREATE TABLE orders_bad (
    order_id INT,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100),
    product_names VARCHAR(500), -- Violates 1NF
    total_amount DECIMAL(10,2)
);

-- Normalized tables (3NF)
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date DATE,
    total_amount DECIMAL(10,2)
);

CREATE TABLE order_items (
    order_id INT REFERENCES orders(order_id),
    product_id INT,
    quantity INT,
    unit_price DECIMAL(8,2)
);
```

## 3. Indexing Strategies
**What they are**: Data structures that improve query performance by creating shortcuts to data.

**Types**:
- **Clustered**: Physical ordering of data
- **Non-clustered**: Separate structure pointing to data
- **Composite**: Multiple columns
- **Partial**: Subset of rows

```sql
-- Primary key (clustered index)
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    email VARCHAR(100),
    created_date DATE
);

-- Non-clustered indexes
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_date ON customers(created_date);

-- Composite index
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- Partial index
CREATE INDEX idx_active_customers ON customers(customer_id) 
WHERE status = 'active';

-- Analyze index usage
SELECT 
    schemaname, tablename, indexname, 
    idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes 
ORDER BY idx_scan DESC;
```

## 4. Query Optimization
**What it is**: Techniques to improve query performance and reduce resource usage.

```sql
-- Use EXPLAIN to analyze query plans
EXPLAIN ANALYZE
SELECT c.customer_name, COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.created_date >= '2024-01-01'
GROUP BY c.customer_id, c.customer_name;

-- Optimization techniques
-- 1. Use EXISTS instead of IN for subqueries
SELECT customer_name FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id 
    AND o.order_date >= '2024-01-01'
);

-- 2. Use LIMIT for large result sets
SELECT * FROM orders 
ORDER BY order_date DESC 
LIMIT 100;

-- 3. Use proper WHERE clause ordering
SELECT * FROM orders 
WHERE status = 'completed'  -- Most selective first
AND order_date >= '2024-01-01'
AND total_amount > 100;
```

## 5. Database Partitioning
**What it is**: Dividing large tables into smaller, manageable pieces.

**Types**:
- **Range**: Based on value ranges
- **Hash**: Based on hash function
- **List**: Based on specific values

```sql
-- Range partitioning by date
CREATE TABLE orders_partitioned (
    order_id BIGSERIAL,
    customer_id INTEGER,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2)
) PARTITION BY RANGE (order_date);

-- Create partitions
CREATE TABLE orders_2024_q1 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE orders_2024_q2 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- Hash partitioning
CREATE TABLE customers_partitioned (
    customer_id INTEGER,
    customer_name VARCHAR(100)
) PARTITION BY HASH (customer_id);

CREATE TABLE customers_part_0 PARTITION OF customers_partitioned
    FOR VALUES WITH (modulus 4, remainder 0);
```

## 6. Replication and High Availability
**What it is**: Techniques to ensure database availability and data redundancy.

**Types**:
- **Master-Slave**: One write, multiple read replicas
- **Master-Master**: Multiple write nodes
- **Synchronous**: Wait for replica confirmation
- **Asynchronous**: Don't wait for replica confirmation

```python
# PostgreSQL streaming replication setup
# Master configuration (postgresql.conf)
"""
wal_level = replica
max_wal_senders = 3
wal_keep_segments = 64
archive_mode = on
archive_command = 'cp %p /var/lib/postgresql/archive/%f'
"""

# Slave configuration
"""
standby_mode = 'on'
primary_conninfo = 'host=master_ip port=5432 user=replicator'
restore_command = 'cp /var/lib/postgresql/archive/%f %p'
"""

# Python connection with read/write splitting
import psycopg2

class DatabaseConnection:
    def __init__(self):
        self.write_conn = psycopg2.connect(
            host='master.db.com',
            database='mydb',
            user='app_user',
            password='password'
        )
        
        self.read_conn = psycopg2.connect(
            host='replica.db.com',
            database='mydb',
            user='app_user',
            password='password'
        )
    
    def execute_write(self, query, params=None):
        with self.write_conn.cursor() as cursor:
            cursor.execute(query, params)
            self.write_conn.commit()
    
    def execute_read(self, query, params=None):
        with self.read_conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
```

## 7. Database Security
**What it is**: Protecting database from unauthorized access and ensuring data privacy.

```sql
-- User management and permissions
CREATE USER data_engineer WITH PASSWORD 'secure_password';
CREATE USER analyst WITH PASSWORD 'analyst_password';

-- Grant specific permissions
GRANT SELECT, INSERT, UPDATE ON customers TO data_engineer;
GRANT SELECT ON customers TO analyst;

-- Row-level security
CREATE POLICY customer_policy ON customers
    FOR ALL TO data_engineer
    USING (created_by = current_user);

-- Column-level security
GRANT SELECT (customer_id, customer_name) ON customers TO analyst;

-- Encryption at rest
CREATE TABLE sensitive_data (
    id SERIAL PRIMARY KEY,
    ssn VARCHAR(11) ENCRYPTED,
    credit_card VARCHAR(16) ENCRYPTED
);

-- Audit logging
CREATE TABLE audit_log (
    log_id SERIAL PRIMARY KEY,
    table_name VARCHAR(50),
    operation VARCHAR(10),
    user_name VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    old_values JSONB,
    new_values JSONB
);
```

## 8. Connection Pooling
**What it is**: Managing database connections efficiently to improve performance and resource utilization.

```python
# Connection pooling with psycopg2
from psycopg2 import pool
import threading

class DatabasePool:
    def __init__(self, minconn=1, maxconn=20):
        self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
            minconn, maxconn,
            host='localhost',
            database='mydb',
            user='user',
            password='password'
        )
        self.lock = threading.Lock()
    
    def get_connection(self):
        return self.connection_pool.getconn()
    
    def put_connection(self, conn):
        self.connection_pool.putconn(conn)
    
    def execute_query(self, query, params=None):
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if query.strip().upper().startswith('SELECT'):
                    return cursor.fetchall()
                else:
                    conn.commit()
        finally:
            if conn:
                self.put_connection(conn)

# Usage
db_pool = DatabasePool(minconn=5, maxconn=50)
results = db_pool.execute_query("SELECT * FROM customers WHERE status = %s", ('active',))
```

## 9. Database Monitoring and Performance Tuning
**What it is**: Continuously monitoring database performance and optimizing for better efficiency.

```sql
-- PostgreSQL performance monitoring queries
-- 1. Slow queries
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;

-- 2. Index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes 
WHERE idx_scan = 0;  -- Unused indexes

-- 3. Table statistics
SELECT 
    schemaname,
    tablename,
    n_tup_ins,
    n_tup_upd,
    n_tup_del,
    n_live_tup,
    n_dead_tup
FROM pg_stat_user_tables;

-- 4. Lock monitoring
SELECT 
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS blocking_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity 
    ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks 
    ON blocking_locks.locktype = blocked_locks.locktype
WHERE NOT blocked_locks.granted;
```

## 10. Database Backup and Recovery
**What it is**: Strategies to protect data and ensure business continuity.

```bash
# PostgreSQL backup strategies
# 1. Logical backup (pg_dump)
pg_dump -h localhost -U postgres -d mydb > backup_$(date +%Y%m%d).sql

# 2. Physical backup (pg_basebackup)
pg_basebackup -h localhost -D /backup/base -U postgres -v -P -W

# 3. Point-in-time recovery setup
# postgresql.conf
wal_level = replica
archive_mode = on
archive_command = 'cp %p /backup/archive/%f'
```

```python
# Automated backup script
import subprocess
import datetime
import boto3
import os

class DatabaseBackup:
    def __init__(self, db_config, s3_bucket):
        self.db_config = db_config
        self.s3_bucket = s3_bucket
        self.s3_client = boto3.client('s3')
    
    def create_backup(self):
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f"backup_{timestamp}.sql"
        
        # Create backup
        cmd = [
            'pg_dump',
            '-h', self.db_config['host'],
            '-U', self.db_config['user'],
            '-d', self.db_config['database'],
            '-f', backup_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Upload to S3
            self.s3_client.upload_file(
                backup_file, 
                self.s3_bucket, 
                f"database-backups/{backup_file}"
            )
            
            # Clean up local file
            os.remove(backup_file)
            
            print(f"Backup {backup_file} uploaded successfully")
        else:
            print(f"Backup failed: {result.stderr}")
    
    def restore_backup(self, backup_file):
        # Download from S3
        self.s3_client.download_file(
            self.s3_bucket, 
            f"database-backups/{backup_file}", 
            backup_file
        )
        
        # Restore database
        cmd = [
            'psql',
            '-h', self.db_config['host'],
            '-U', self.db_config['user'],
            '-d', self.db_config['database'],
            '-f', backup_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Database restored from {backup_file}")
        else:
            print(f"Restore failed: {result.stderr}")

# Usage
backup_manager = DatabaseBackup(
    db_config={
        'host': 'localhost',
        'user': 'postgres',
        'database': 'mydb'
    },
    s3_bucket='my-db-backups'
)

backup_manager.create_backup()
```

These database concepts form the foundation for effective data engineering, ensuring data integrity, performance, and reliability in data systems.