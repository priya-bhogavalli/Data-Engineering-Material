# Apache Cassandra Key Concepts

## 🎯 What is Cassandra?
Distributed wide-column NoSQL database designed for handling large amounts of data across commodity servers.

## 🏗️ Core Architecture

### Data Model
```cql
-- Keyspace (like database)
CREATE KEYSPACE ecommerce 
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3};

-- Table with partition and clustering keys
CREATE TABLE orders (
    customer_id UUID,
    order_date timestamp,
    order_id UUID,
    amount decimal,
    PRIMARY KEY (customer_id, order_date, order_id)
);
```

### Key Components
- **Keyspace** - Top-level namespace
- **Table** - Collection of rows
- **Partition Key** - Determines data distribution
- **Clustering Key** - Sorts data within partition
- **Column** - Name-value pair

## 🔧 CQL Operations

### Basic CRUD
```cql
-- Insert
INSERT INTO orders (customer_id, order_date, order_id, amount)
VALUES (uuid(), '2024-01-15', uuid(), 99.99);

-- Select
SELECT * FROM orders 
WHERE customer_id = 123e4567-e89b-12d3-a456-426614174000;

-- Update
UPDATE orders SET amount = 89.99 
WHERE customer_id = 123e4567-e89b-12d3-a456-426614174000 
AND order_date = '2024-01-15';

-- Delete
DELETE FROM orders 
WHERE customer_id = 123e4567-e89b-12d3-a456-426614174000;
```

## 📊 Data Distribution

### Partitioning Strategy
```cql
-- Time-series partitioning
CREATE TABLE metrics (
    sensor_id text,
    date text,
    timestamp timestamp,
    value double,
    PRIMARY KEY ((sensor_id, date), timestamp)
);
```

### Replication
- **SimpleStrategy** - Single datacenter
- **NetworkTopologyStrategy** - Multiple datacenters
- Configurable replication factor

## 🚀 Performance Features

### Consistency Levels
```cql
-- Strong consistency
CONSISTENCY QUORUM;

-- Eventual consistency
CONSISTENCY ONE;

-- Read/write consistency
CONSISTENCY LOCAL_QUORUM;
```

### Materialized Views
```cql
CREATE MATERIALIZED VIEW orders_by_date AS
SELECT customer_id, order_date, order_id, amount
FROM orders
WHERE order_date IS NOT NULL
PRIMARY KEY (order_date, customer_id, order_id);
```

## 🔧 Tuning & Optimization

### Compaction Strategies
- **SizeTieredCompactionStrategy** - General purpose
- **LeveledCompactionStrategy** - Read-heavy workloads
- **TimeWindowCompactionStrategy** - Time-series data

### Best Practices
- Design tables for specific queries
- Avoid large partitions (>100MB)
- Use appropriate consistency levels
- Monitor compaction and repair operations
- Implement proper data modeling patterns

## 🎯 Use Cases
- Time-series data (IoT, metrics)
- Real-time recommendations
- Fraud detection
- Content management
- High-velocity data ingestion

## ⚠️ Limitations
- No JOINs between tables
- Limited secondary index support
- Eventually consistent by default
- Complex data modeling requirements