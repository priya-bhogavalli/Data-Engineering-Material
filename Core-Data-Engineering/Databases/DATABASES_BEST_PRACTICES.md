# Database Best Practices for Data Engineering

## 1. Schema Design

### Normalization vs Denormalization
```sql
-- Normalized design (OLTP)
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date DATE,
    total_amount DECIMAL(10,2)
);

-- Denormalized design (OLAP)
CREATE TABLE order_summary (
    order_id SERIAL PRIMARY KEY,
    customer_id INT,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100),
    order_date DATE,
    total_amount DECIMAL(10,2)
);
```

### Data Types and Constraints
```sql
-- Use appropriate data types
CREATE TABLE products (
    product_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) CHECK (price > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Add constraints for data integrity
ALTER TABLE orders 
ADD CONSTRAINT chk_order_date 
CHECK (order_date <= CURRENT_DATE);
```

## 2. Indexing Strategy

### Index Types and Usage
```sql
-- B-tree index (default)
CREATE INDEX idx_customer_email ON customers(email);

-- Partial index
CREATE INDEX idx_active_products ON products(name) 
WHERE is_active = TRUE;

-- Composite index
CREATE INDEX idx_order_customer_date ON orders(customer_id, order_date);

-- Covering index
CREATE INDEX idx_order_summary ON orders(customer_id) 
INCLUDE (order_date, total_amount);

-- Hash index (for equality comparisons)
CREATE INDEX CONCURRENTLY idx_product_id_hash ON products 
USING HASH(product_id);
```

### Index Maintenance
```python
def monitor_index_usage():
    """Monitor and maintain database indexes."""
    
    # Query to find unused indexes
    unused_indexes_query = """
    SELECT schemaname, tablename, indexname, idx_tup_read, idx_tup_fetch
    FROM pg_stat_user_indexes 
    WHERE idx_tup_read = 0 AND idx_tup_fetch = 0
    """
    
    # Query to find duplicate indexes
    duplicate_indexes_query = """
    SELECT pg_size_pretty(SUM(pg_relation_size(indexrelid))) AS size,
           array_agg(indexname) AS indexes
    FROM pg_stat_user_indexes
    GROUP BY indrelid, indkey
    HAVING COUNT(*) > 1
    """
    
    # Rebuild fragmented indexes
    rebuild_query = """
    REINDEX INDEX CONCURRENTLY idx_name;
    """
```

## 3. Query Optimization

### Query Performance Analysis
```sql
-- Enable query execution analysis
EXPLAIN (ANALYZE, BUFFERS, VERBOSE) 
SELECT c.name, COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.created_date >= '2024-01-01'
GROUP BY c.name
ORDER BY order_count DESC;

-- Use query hints when necessary (SQL Server)
SELECT /*+ USE_INDEX(customers, idx_customer_email) */
    name, email
FROM customers
WHERE email LIKE '%@company.com';
```

### Efficient Query Patterns
```sql
-- Use EXISTS instead of IN for large subqueries
SELECT customer_id, name
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id 
    AND o.order_date >= '2024-01-01'
);

-- Use LIMIT with ORDER BY for pagination
SELECT customer_id, name, email
FROM customers
ORDER BY customer_id
LIMIT 50 OFFSET 100;

-- Use window functions instead of self-joins
SELECT customer_id, order_date, total_amount,
       LAG(total_amount) OVER (PARTITION BY customer_id ORDER BY order_date) as prev_amount
FROM orders;
```

## 4. Connection Management

### Connection Pooling
```python
import psycopg2.pool
from contextlib import contextmanager

class DatabaseConnectionPool:
    def __init__(self, min_conn=1, max_conn=20):
        self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
            min_conn, max_conn,
            host="localhost",
            database="mydb",
            user="user",
            password="password"
        )
    
    @contextmanager
    def get_connection(self):
        conn = self.connection_pool.getconn()
        try:
            yield conn
        finally:
            self.connection_pool.putconn(conn)
    
    def execute_query(self, query, params=None):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()

# Usage
db_pool = DatabaseConnectionPool()
results = db_pool.execute_query("SELECT * FROM customers WHERE id = %s", (123,))
```

### Transaction Management
```python
def safe_transaction_execution(connection, operations):
    """Execute multiple operations in a single transaction."""
    try:
        connection.autocommit = False
        cursor = connection.cursor()
        
        for operation in operations:
            cursor.execute(operation['query'], operation.get('params'))
        
        connection.commit()
        return True
        
    except Exception as e:
        connection.rollback()
        print(f"Transaction failed: {e}")
        return False
    finally:
        cursor.close()
        connection.autocommit = True
```

## 5. Data Security

### Access Control
```sql
-- Create roles with specific permissions
CREATE ROLE data_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO data_reader;

CREATE ROLE data_writer;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO data_writer;

-- Row-level security
CREATE POLICY customer_policy ON orders
    FOR ALL TO data_reader
    USING (customer_id = current_user_id());

ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
```

### Data Encryption
```sql
-- Column-level encryption
CREATE TABLE sensitive_data (
    id SERIAL PRIMARY KEY,
    customer_id INT,
    encrypted_ssn BYTEA,
    encrypted_credit_card BYTEA
);

-- Use pgcrypto extension
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Insert encrypted data
INSERT INTO sensitive_data (customer_id, encrypted_ssn)
VALUES (123, pgp_sym_encrypt('123-45-6789', 'encryption_key'));

-- Query encrypted data
SELECT customer_id, pgp_sym_decrypt(encrypted_ssn, 'encryption_key') as ssn
FROM sensitive_data
WHERE customer_id = 123;
```

## 6. Backup and Recovery

### Backup Strategy
```python
import subprocess
from datetime import datetime

class DatabaseBackupManager:
    def __init__(self, db_config):
        self.db_config = db_config
    
    def full_backup(self):
        """Perform full database backup."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"full_backup_{timestamp}.sql"
        
        cmd = [
            "pg_dump",
            "-h", self.db_config['host'],
            "-U", self.db_config['user'],
            "-d", self.db_config['database'],
            "-f", backup_file,
            "--verbose"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Backup completed: {backup_file}")
            return backup_file
        else:
            print(f"Backup failed: {result.stderr}")
            return None
    
    def incremental_backup(self, base_backup_lsn):
        """Perform incremental backup using WAL files."""
        cmd = [
            "pg_basebackup",
            "-h", self.db_config['host'],
            "-U", self.db_config['user'],
            "-D", f"incremental_backup_{datetime.now().strftime('%Y%m%d')}",
            "-Ft", "-z", "-P"
        ]
        
        subprocess.run(cmd)
    
    def point_in_time_recovery(self, backup_file, target_time):
        """Restore database to specific point in time."""
        # Stop database service
        subprocess.run(["sudo", "systemctl", "stop", "postgresql"])
        
        # Restore base backup
        subprocess.run(["tar", "-xzf", backup_file, "-C", "/var/lib/postgresql/data"])
        
        # Create recovery configuration
        recovery_conf = f"""
        restore_command = 'cp /path/to/wal_archive/%f %p'
        recovery_target_time = '{target_time}'
        recovery_target_action = 'promote'
        """
        
        with open("/var/lib/postgresql/data/recovery.conf", "w") as f:
            f.write(recovery_conf)
        
        # Start database service
        subprocess.run(["sudo", "systemctl", "start", "postgresql"])
```

## 7. Monitoring and Maintenance

### Performance Monitoring
```sql
-- Monitor slow queries
SELECT query, mean_time, calls, total_time
FROM pg_stat_statements
WHERE mean_time > 1000  -- queries taking more than 1 second
ORDER BY mean_time DESC;

-- Monitor table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Monitor index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_tup_read DESC;
```

### Automated Maintenance
```python
class DatabaseMaintenance:
    def __init__(self, connection):
        self.connection = connection
    
    def update_statistics(self):
        """Update table statistics for query optimizer."""
        cursor = self.connection.cursor()
        cursor.execute("ANALYZE;")
        self.connection.commit()
    
    def vacuum_tables(self, table_names=None):
        """Vacuum tables to reclaim space and update statistics."""
        cursor = self.connection.cursor()
        
        if table_names:
            for table in table_names:
                cursor.execute(f"VACUUM ANALYZE {table};")
        else:
            cursor.execute("VACUUM ANALYZE;")
        
        self.connection.commit()
    
    def reindex_tables(self, table_names):
        """Rebuild indexes for better performance."""
        cursor = self.connection.cursor()
        
        for table in table_names:
            cursor.execute(f"REINDEX TABLE {table};")
        
        self.connection.commit()
    
    def check_database_health(self):
        """Perform comprehensive database health check."""
        health_checks = {
            'connection_count': self._check_connections(),
            'disk_usage': self._check_disk_usage(),
            'slow_queries': self._check_slow_queries(),
            'index_usage': self._check_index_usage(),
            'table_bloat': self._check_table_bloat()
        }
        
        return health_checks
```

## 8. NoSQL Best Practices

### MongoDB Optimization
```python
from pymongo import MongoClient, ASCENDING, DESCENDING

# Connection with proper configuration
client = MongoClient(
    'mongodb://localhost:27017/',
    maxPoolSize=50,
    wtimeoutMS=2500,
    readPreference='secondaryPreferred'
)

db = client.mydb
collection = db.mycollection

# Create compound indexes
collection.create_index([
    ("customer_id", ASCENDING),
    ("order_date", DESCENDING)
])

# Use aggregation pipeline for complex queries
pipeline = [
    {"$match": {"order_date": {"$gte": "2024-01-01"}}},
    {"$group": {
        "_id": "$customer_id",
        "total_amount": {"$sum": "$amount"},
        "order_count": {"$sum": 1}
    }},
    {"$sort": {"total_amount": -1}},
    {"$limit": 100}
]

results = list(collection.aggregate(pipeline))
```

### Redis Best Practices
```python
import redis
import json

# Connection pooling
redis_pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    db=0,
    max_connections=20
)

redis_client = redis.Redis(connection_pool=redis_pool)

# Use appropriate data structures
def cache_user_session(user_id, session_data, ttl=3600):
    """Cache user session with expiration."""
    key = f"session:{user_id}"
    redis_client.setex(key, ttl, json.dumps(session_data))

def get_user_session(user_id):
    """Retrieve user session from cache."""
    key = f"session:{user_id}"
    data = redis_client.get(key)
    return json.loads(data) if data else None

# Use Redis for rate limiting
def rate_limit(user_id, limit=100, window=3600):
    """Implement rate limiting using Redis."""
    key = f"rate_limit:{user_id}"
    current = redis_client.get(key)
    
    if current is None:
        redis_client.setex(key, window, 1)
        return True
    elif int(current) < limit:
        redis_client.incr(key)
        return True
    else:
        return False
```

These best practices ensure optimal database performance, security, and maintainability in data engineering environments.