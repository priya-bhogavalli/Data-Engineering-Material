# PostgreSQL Best Practices for Data Engineering

## Performance Optimization

### Index Strategy
```sql
-- B-tree indexes for equality and range queries
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_date_range ON orders(order_date);

-- Composite indexes for multi-column queries
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- Partial indexes for filtered queries
CREATE INDEX idx_active_customers ON customers(customer_id) 
WHERE status = 'active';

-- Expression indexes for computed values
CREATE INDEX idx_customer_email_lower ON customers(lower(email));
```

### Query Optimization
```sql
-- Use EXPLAIN ANALYZE for query planning
EXPLAIN (ANALYZE, BUFFERS) 
SELECT c.name, COUNT(o.order_id)
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.created_date >= '2023-01-01'
GROUP BY c.customer_id, c.name;

-- Optimize with CTEs
WITH recent_customers AS (
    SELECT customer_id, name
    FROM customers
    WHERE created_date >= '2023-01-01'
)
SELECT rc.name, COUNT(o.order_id)
FROM recent_customers rc
LEFT JOIN orders o ON rc.customer_id = o.customer_id
GROUP BY rc.customer_id, rc.name;
```

## Connection Management

### Connection Pooling
```python
import psycopg2
from psycopg2 import pool

# Create connection pool
connection_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=1,
    maxconn=20,
    host='localhost',
    database='datawarehouse',
    user='postgres',
    password='password'
)

def execute_query(query, params=None):
    conn = None
    try:
        conn = connection_pool.getconn()
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    finally:
        if conn:
            connection_pool.putconn(conn)
```

### Configuration Tuning
```sql
-- Memory settings
shared_buffers = '256MB'
effective_cache_size = '1GB'
work_mem = '4MB'
maintenance_work_mem = '64MB'

-- Checkpoint settings
checkpoint_completion_target = 0.9
wal_buffers = '16MB'
checkpoint_segments = 32

-- Query planner settings
random_page_cost = 1.1
effective_io_concurrency = 200
```

## Data Modeling

### Table Design
```sql
-- Fact table with proper data types
CREATE TABLE sales_fact (
    sale_id BIGSERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    sale_date DATE NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price > 0),
    total_amount DECIMAL(12,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Dimension table with constraints
CREATE TABLE customer_dim (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Partitioning
```sql
-- Range partitioning by date
CREATE TABLE sales_fact_partitioned (
    sale_id BIGSERIAL,
    customer_id INTEGER NOT NULL,
    sale_date DATE NOT NULL,
    amount DECIMAL(10,2)
) PARTITION BY RANGE (sale_date);

-- Create partitions
CREATE TABLE sales_2023_q1 PARTITION OF sales_fact_partitioned
FOR VALUES FROM ('2023-01-01') TO ('2023-04-01');

CREATE TABLE sales_2023_q2 PARTITION OF sales_fact_partitioned
FOR VALUES FROM ('2023-04-01') TO ('2023-07-01');
```

## ETL Operations

### Bulk Loading
```sql
-- COPY for bulk inserts
COPY customers(name, email, phone)
FROM '/path/to/customers.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',');

-- INSERT with ON CONFLICT for upserts
INSERT INTO customers (customer_id, name, email, updated_at)
VALUES (1, 'John Doe', 'john@example.com', CURRENT_TIMESTAMP)
ON CONFLICT (customer_id)
DO UPDATE SET
    name = EXCLUDED.name,
    email = EXCLUDED.email,
    updated_at = EXCLUDED.updated_at;
```

### Transaction Management
```python
import psycopg2

def bulk_upsert_customers(customers_data):
    conn = psycopg2.connect(
        host='localhost',
        database='datawarehouse',
        user='postgres',
        password='password'
    )
    
    try:
        with conn:
            with conn.cursor() as cursor:
                # Use COPY for bulk operations
                cursor.copy_from(
                    customers_data,
                    'temp_customers',
                    columns=('name', 'email', 'phone')
                )
                
                # Merge with main table
                cursor.execute("""
                    INSERT INTO customers (name, email, phone)
                    SELECT name, email, phone FROM temp_customers
                    ON CONFLICT (email)
                    DO UPDATE SET
                        name = EXCLUDED.name,
                        phone = EXCLUDED.phone,
                        updated_at = CURRENT_TIMESTAMP
                """)
                
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()
```

## Monitoring and Maintenance

### Performance Monitoring
```sql
-- Monitor slow queries
SELECT query, mean_time, calls, total_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Monitor table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Maintenance Tasks
```sql
-- Vacuum and analyze
VACUUM ANALYZE customers;

-- Reindex for maintenance
REINDEX INDEX idx_customers_email;

-- Update table statistics
ANALYZE customers;
```