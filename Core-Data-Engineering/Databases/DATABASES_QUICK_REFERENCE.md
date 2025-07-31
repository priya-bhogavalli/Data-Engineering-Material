# Database Quick Reference

## SQL Basics

### DDL (Data Definition Language)
```sql
-- Create table
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Alter table
ALTER TABLE customers ADD COLUMN phone VARCHAR(20);
ALTER TABLE customers DROP COLUMN phone;
ALTER TABLE customers MODIFY COLUMN name VARCHAR(150);

-- Create index
CREATE INDEX idx_customer_email ON customers(email);
CREATE UNIQUE INDEX idx_customer_phone ON customers(phone);

-- Drop objects
DROP TABLE customers;
DROP INDEX idx_customer_email;
```

### DML (Data Manipulation Language)
```sql
-- Insert
INSERT INTO customers (name, email) VALUES ('John Doe', 'john@example.com');
INSERT INTO customers (name, email) VALUES 
    ('Jane Smith', 'jane@example.com'),
    ('Bob Johnson', 'bob@example.com');

-- Update
UPDATE customers SET email = 'newemail@example.com' WHERE id = 1;

-- Delete
DELETE FROM customers WHERE id = 1;

-- Select
SELECT * FROM customers;
SELECT name, email FROM customers WHERE created_at >= '2024-01-01';
```

### Joins
```sql
-- Inner Join
SELECT c.name, o.order_date
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id;

-- Left Join
SELECT c.name, o.order_date
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id;

-- Self Join
SELECT e1.name as employee, e2.name as manager
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.id;
```

### Aggregations
```sql
-- Basic aggregations
SELECT COUNT(*) FROM customers;
SELECT AVG(amount) FROM orders;
SELECT SUM(amount) FROM orders WHERE order_date >= '2024-01-01';

-- Group By
SELECT customer_id, COUNT(*) as order_count, SUM(amount) as total
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 5;

-- Window functions
SELECT name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC) as rank,
       AVG(salary) OVER () as avg_salary
FROM employees;
```

## Database-Specific Commands

### PostgreSQL
```sql
-- Show databases
\l

-- Connect to database
\c database_name

-- Show tables
\dt

-- Describe table
\d table_name

-- Show indexes
\di

-- Vacuum and analyze
VACUUM ANALYZE table_name;

-- Create extension
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

### MySQL
```sql
-- Show databases
SHOW DATABASES;

-- Use database
USE database_name;

-- Show tables
SHOW TABLES;

-- Describe table
DESCRIBE table_name;

-- Show indexes
SHOW INDEX FROM table_name;

-- Optimize table
OPTIMIZE TABLE table_name;
```

### SQL Server
```sql
-- Show databases
SELECT name FROM sys.databases;

-- Use database
USE database_name;

-- Show tables
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES;

-- Show columns
SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'table_name';

-- Update statistics
UPDATE STATISTICS table_name;
```

## NoSQL Commands

### MongoDB
```javascript
// Show databases
show dbs

// Use database
use mydb

// Show collections
show collections

// Insert document
db.customers.insertOne({name: "John", email: "john@example.com"})

// Find documents
db.customers.find({name: "John"})
db.customers.find({age: {$gt: 25}})

// Update document
db.customers.updateOne({name: "John"}, {$set: {age: 30}})

// Delete document
db.customers.deleteOne({name: "John"})

// Create index
db.customers.createIndex({email: 1})

// Aggregation
db.orders.aggregate([
    {$match: {status: "completed"}},
    {$group: {_id: "$customer_id", total: {$sum: "$amount"}}}
])
```

### Redis
```bash
# String operations
SET key "value"
GET key
INCR counter
EXPIRE key 3600

# Hash operations
HSET user:1 name "John" email "john@example.com"
HGET user:1 name
HGETALL user:1

# List operations
LPUSH mylist "item1"
RPUSH mylist "item2"
LRANGE mylist 0 -1

# Set operations
SADD myset "member1"
SMEMBERS myset

# Sorted set operations
ZADD leaderboard 100 "player1"
ZRANGE leaderboard 0 -1 WITHSCORES
```

### Cassandra
```sql
-- Create keyspace
CREATE KEYSPACE mykeyspace 
WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 3};

-- Use keyspace
USE mykeyspace;

-- Create table
CREATE TABLE customers (
    id UUID PRIMARY KEY,
    name TEXT,
    email TEXT,
    created_at TIMESTAMP
);

-- Insert data
INSERT INTO customers (id, name, email, created_at) 
VALUES (uuid(), 'John Doe', 'john@example.com', toTimestamp(now()));

-- Select data
SELECT * FROM customers WHERE id = 123e4567-e89b-12d3-a456-426614174000;
```

## Performance Optimization

### Index Management
```sql
-- Check index usage (PostgreSQL)
SELECT schemaname, tablename, indexname, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_tup_read DESC;

-- Find missing indexes
SELECT schemaname, tablename, seq_tup_read
FROM pg_stat_user_tables
WHERE seq_tup_read > 1000
ORDER BY seq_tup_read DESC;

-- Create partial index
CREATE INDEX idx_active_customers ON customers(name) WHERE active = true;
```

### Query Analysis
```sql
-- Explain query plan
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM customers WHERE email = 'john@example.com';

-- Show slow queries (PostgreSQL)
SELECT query, mean_time, calls
FROM pg_stat_statements
WHERE mean_time > 1000
ORDER BY mean_time DESC;
```

## Backup and Recovery

### PostgreSQL
```bash
# Full backup
pg_dump -h localhost -U username -d database_name > backup.sql

# Restore
psql -h localhost -U username -d database_name < backup.sql

# Backup with compression
pg_dump -h localhost -U username -d database_name | gzip > backup.sql.gz

# Point-in-time recovery
pg_basebackup -D /backup/location -Ft -z -P
```

### MySQL
```bash
# Full backup
mysqldump -u username -p database_name > backup.sql

# Restore
mysql -u username -p database_name < backup.sql

# Backup specific tables
mysqldump -u username -p database_name table1 table2 > backup.sql
```

## Connection Strings

### PostgreSQL
```python
# psycopg2
import psycopg2
conn = psycopg2.connect(
    host="localhost",
    database="mydb",
    user="username",
    password="password",
    port="5432"
)

# SQLAlchemy
from sqlalchemy import create_engine
engine = create_engine('postgresql://username:password@localhost:5432/mydb')
```

### MySQL
```python
# PyMySQL
import pymysql
conn = pymysql.connect(
    host='localhost',
    user='username',
    password='password',
    database='mydb',
    port=3306
)

# SQLAlchemy
engine = create_engine('mysql+pymysql://username:password@localhost:3306/mydb')
```

### MongoDB
```python
# PyMongo
from pymongo import MongoClient
client = MongoClient('mongodb://username:password@localhost:27017/')
db = client.mydb
```

### Redis
```python
# redis-py
import redis
r = redis.Redis(host='localhost', port=6379, db=0, password='password')
```

## Common Data Types

### SQL Data Types
```sql
-- Numeric
INT, BIGINT, DECIMAL(10,2), FLOAT, DOUBLE

-- String
VARCHAR(255), TEXT, CHAR(10)

-- Date/Time
DATE, TIME, TIMESTAMP, DATETIME

-- Boolean
BOOLEAN

-- JSON (PostgreSQL, MySQL 5.7+)
JSON, JSONB
```

### MongoDB Data Types
```javascript
// String
"text"

// Number
123, 123.45

// Boolean
true, false

// Date
new Date()

// Array
[1, 2, 3]

// Object
{name: "John", age: 30}

// ObjectId
ObjectId("507f1f77bcf86cd799439011")
```