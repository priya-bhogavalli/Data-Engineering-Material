# Apache Impala Key Concepts for Data Engineering

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Architecture](#-architecture)
   - [Core Components](#core-components)
   - [Query Execution](#query-execution)
   - [Memory Management](#memory-management)
3. [Features](#-features)
   - [SQL Support](#sql-support)
   - [Data Formats](#data-formats)
   - [Performance Optimizations](#performance-optimizations)
4. [Use Cases](#-use-cases)
5. [Integrations](#-integrations)
6. [Best Practices](#-best-practices)
7. [Limitations](#-limitations)
8. [Version Highlights](#-version-highlights)
9. [Interview Focus Areas](#-interview-focus-areas)
10. [Quick References](#-quick-references)

---

## 🎯 Overview

Apache Impala is a modern, open-source, distributed SQL query engine for Apache Hadoop that provides low-latency queries and high concurrency for business intelligence and analytics workloads.

**Key Benefits:**
- **Low Latency**: Sub-second to few-second query response times
- **Interactive Analytics**: Real-time business intelligence on big data
- **SQL Compatibility**: Standard SQL interface for Hadoop data
- **High Concurrency**: Support for many concurrent users (100+)
- **No ETL Required**: Query data in place without movement

**Core Differentiators:**
- Massively Parallel Processing (MPP) architecture
- In-memory processing with spill-to-disk
- Columnar storage optimization
- Cost-based query optimization
- Native integration with Hadoop ecosystem

```sql
-- Example: Interactive analytics query
SELECT 
    customer_segment,
    COUNT(*) as customer_count,
    AVG(order_total) as avg_order_value,
    SUM(order_total) as total_revenue
FROM customer_orders 
WHERE order_date >= '2023-01-01'
GROUP BY customer_segment
ORDER BY total_revenue DESC;

-- Output (sub-second response):
-- +----------------+----------------+----------------+--------------+
-- |customer_segment|customer_count  |avg_order_value |total_revenue |
-- +----------------+----------------+----------------+--------------+
-- |Enterprise      |1250            |2847.50         |3559375.00    |
-- |Premium         |3420            |1245.75         |4260465.00    |
-- |Standard        |8750            |456.25          |3992187.50    |
-- +----------------+----------------+----------------+--------------+
```

## 🏗️ Architecture

### Core Components

**Impala Architecture Diagram:**
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              IMPALA CLUSTER                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐             │
│  │   CLIENT APPS   │    │   STATESTORE    │    │ CATALOG SERVICE │             │
│  │                 │    │                 │    │                 │             │
│  │ • JDBC/ODBC     │    │ • Cluster       │    │ • Metadata      │             │
│  │ • Impala Shell  │    │   Membership    │    │   Management    │             │
│  │ • BI Tools      │    │ • Health        │    │ • Schema        │             │
│  │ • Applications  │    │   Monitoring    │    │   Changes       │             │
│  └─────────────────┘    │ • Metadata      │    │ • Statistics    │             │
│           │              │   Distribution  │    │   Distribution  │             │
│           │              └─────────────────┘    └─────────────────┘             │
│           ▼                        │                       │                    │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           IMPALA DAEMONS                                   │ │
│  │                                                                             │ │
│  │ ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │ │
│  │ │   COORDINATOR   │  │   EXECUTOR 1    │  │   EXECUTOR N    │             │ │
│  │ │                 │  │                 │  │                 │             │ │
│  │ │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │             │ │
│  │ │ │Query Planner│ │  │ │Scan Operator│ │  │ │Scan Operator│ │             │ │
│  │ │ │Optimizer    │ │  │ │Join Operator│ │  │ │Join Operator│ │             │ │
│  │ │ │Scheduler    │ │  │ │Agg Operator │ │  │ │Agg Operator │ │             │ │
│  │ │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │             │ │
│  │ │                 │  │                 │  │                 │             │ │
│  │ │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │             │ │
│  │ │ │Result       │ │  │ │Memory Pool  │ │  │ │Memory Pool  │ │             │ │
│  │ │ │Aggregation  │ │  │ │Buffer Pool  │ │  │ │Buffer Pool  │ │             │ │
│  │ │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │             │ │
│  │ └─────────────────┘  └─────────────────┘  └─────────────────┘             │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                     │                                           │
│                                     ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                          STORAGE LAYER                                     │ │
│  │                                                                             │ │
│  │ ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │ │
│  │ │      HDFS       │  │      HBase      │  │   Hive Metastore│             │ │
│  │ │                 │  │                 │  │                 │             │ │
│  │ │ • Parquet       │  │ • Real-time     │  │ • Schema        │             │ │
│  │ │ • ORC           │  │   Updates       │  │   Metadata      │             │ │
│  │ │ • Avro          │  │ • Key-Value     │  │ • Table         │             │ │
│  │ │ • Text          │  │   Access        │  │   Definitions   │             │ │
│  │ └─────────────────┘  └─────────────────┘  └─────────────────┘             │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### 1. Impala Daemon (impalad)
**Definition**: Core execution engine that runs on each DataNode in the cluster.

**Key Responsibilities:**
- Query execution and coordination
- Client connection handling
- Local data scanning and processing
- Inter-node communication for distributed queries

```bash
# Impala daemon configuration
--mem_limit=8GB                    # Total memory limit per daemon
--num_scanner_threads=16           # Parallel scan threads
--be_port=22000                    # Backend communication port
--hs2_port=21000                   # HiveServer2 protocol port
--webserver_port=25000             # Web UI port
```

#### 2. Statestore Daemon
**Definition**: Cluster membership service that monitors daemon health and distributes metadata updates.

**Key Functions:**
- Node health monitoring and failure detection
- Cluster membership management
- Metadata change propagation
- Load balancing information distribution

```bash
# Statestore configuration
--statestore_port=24000
--statestore_subscriber_timeout_seconds=30
--statestore_heartbeat_frequency_ms=1000
```

#### 3. Catalog Service
**Definition**: Metadata management service that synchronizes with Hive Metastore and distributes schema information.

**Key Functions:**
- Metadata caching and distribution
- Schema change coordination
- Table statistics management
- DDL operation coordination

```bash
# Catalog service configuration
--catalog_service_port=26000
--load_catalog_in_background=true
--invalidate_tables_timeout_s=600
```

### Query Execution

**Impala Query Execution Flow:**
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           QUERY EXECUTION PIPELINE                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  1. CLIENT REQUEST                                                              │
│  ┌─────────────────┐                                                           │
│  │   SQL Query     │ ──────────────────────────────────────────────────────┐   │
│  │   from Client   │                                                       │   │
│  └─────────────────┘                                                       │   │
│                                                                             │   │
│  2. PARSING & ANALYSIS                                                      │   │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │   │
│  │   SQL Parser    │───►│  Semantic       │───►│   Access        │        │   │
│  │   • Syntax      │    │  Analysis       │    │   Control       │        │   │
│  │   • Validation  │    │  • Schema       │    │   • Permissions │        │   │
│  │   • AST Build   │    │  • Type Check   │    │   • Privileges  │        │   │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘        │   │
│                                                                             │   │
│  3. QUERY PLANNING                                                          │   │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │   │
│  │  Cost-Based     │───►│   Physical      │───►│   Fragment      │        │   │
│  │  Optimization   │    │   Plan          │    │   Generation    │        │   │
│  │  • Statistics   │    │   • Operators   │    │   • Parallelism │        │   │
│  │  • Join Order   │    │   • Algorithms  │    │   • Distribution│        │   │
│  │  • Predicate    │    │   • Memory Est. │    │   • Scheduling  │        │   │
│  │    Pushdown     │    │                 │    │                 │        │   │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘        │   │
│                                                                             │   │
│  4. DISTRIBUTED EXECUTION                                                   │   │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │   │
│  │   Coordinator   │───►│   Fragment      │───►│    Result       │        │   │
│  │   • Task Dist.  │    │   Execution     │    │   Aggregation   │        │   │
│  │   • Progress    │    │   • Parallel    │    │   • Final       │        │   │
│  │     Monitoring  │    │     Processing  │    │     Assembly    │        │   │
│  │   • Error       │    │   • Data        │    │   • Client      │        │   │
│  │     Handling    │    │     Exchange    │    │     Return      │        │   │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘        │   │
│                                                                             │   │
│  ◄──────────────────────────────────────────────────────────────────────────   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Example Query Execution:**
```sql
-- Complex analytical query
SELECT 
    c.customer_segment,
    p.product_category,
    DATE_TRUNC('month', o.order_date) as order_month,
    COUNT(*) as order_count,
    SUM(o.order_total) as total_revenue,
    AVG(o.order_total) as avg_order_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id
WHERE o.order_date >= '2023-01-01'
  AND c.customer_segment IN ('Premium', 'Enterprise')
GROUP BY 1, 2, 3
HAVING SUM(o.order_total) > 10000
ORDER BY total_revenue DESC
LIMIT 100;

-- Execution plan shows:
-- 1. Predicate pushdown (date and segment filters)
-- 2. Partition pruning (if tables are partitioned)
-- 3. Join order optimization (smallest table first)
-- 4. Parallel execution across nodes
-- 5. Distributed aggregation
-- 6. Final result collection
```

### Memory Management

**Impala Memory Architecture:**
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            IMPALA MEMORY LAYOUT                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                          PROCESS MEMORY LIMIT                              │ │
│  │                              (--mem_limit)                                 │ │
│  │                                                                             │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │ │
│  │  │   QUERY MEMORY  │  │  BUFFER POOL    │  │  SYSTEM MEMORY  │             │ │
│  │  │                 │  │                 │  │                 │             │ │
│  │  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │             │ │
│  │  │ │Hash Tables  │ │  │ │I/O Buffers  │ │  │ │Metadata     │ │             │ │
│  │  │ │for Joins    │ │  │ │             │ │  │ │Cache        │ │             │ │
│  │  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │             │ │
│  │  │                 │  │                 │  │                 │             │ │
│  │  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │             │ │
│  │  │ │Aggregation  │ │  │ │Scan Buffers │ │  │ │Connection   │ │             │ │
│  │  │ │Buffers      │ │  │ │             │ │  │ │Handling     │ │             │ │
│  │  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │             │ │
│  │  │                 │  │                 │  │                 │             │ │
│  │  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │             │ │
│  │  │ │Sort         │ │  │ │Exchange     │ │  │ │Background   │ │             │ │
│  │  │ │Operations   │ │  │ │Buffers      │ │  │ │Processes    │ │             │ │
│  │  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │             │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘             │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                     │                                           │
│                                     ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                          SPILL-TO-DISK                                     │ │
│  │                        (--scratch_dirs)                                    │ │
│  │                                                                             │ │
│  │  When memory is exhausted:                                                 │ │
│  │  • Hash tables spill to disk                                               │ │
│  │  • Sort operations use external sort                                       │ │
│  │  • Aggregations spill intermediate results                                 │ │
│  │  • Buffer pool manages disk I/O                                            │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Memory Configuration Example:**
```bash
# Production memory settings
--mem_limit=64GB                   # Total memory per daemon
--buffer_pool_limit=48GB           # Buffer pool (75% of total)
--min_buffer_size=64KB             # Minimum buffer size
--max_buffer_size=8MB              # Maximum buffer size
--scratch_dirs=/ssd1/impala-scratch,/ssd2/impala-scratch
```

## 🚀 Features

### SQL Support

**ANSI SQL Compliance:**
Impala supports a comprehensive subset of ANSI SQL with extensions for analytical workloads.

**Supported SQL Features:**
```sql
-- Complex SELECT with window functions
SELECT 
    customer_id,
    order_date,
    order_total,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as order_sequence,
    SUM(order_total) OVER (PARTITION BY customer_id ORDER BY order_date 
                          ROWS UNBOUNDED PRECEDING) as running_total,
    LAG(order_total, 1) OVER (PARTITION BY customer_id ORDER BY order_date) as prev_order,
    LEAD(order_total, 1) OVER (PARTITION BY customer_id ORDER BY order_date) as next_order
FROM orders
WHERE order_date >= '2023-01-01';

-- Advanced aggregations
SELECT 
    product_category,
    COUNT(*) as product_count,
    AVG(price) as avg_price,
    STDDEV(price) as price_stddev,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price) as median_price,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price) as q1_price,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) as q3_price
FROM products
GROUP BY product_category
HAVING COUNT(*) > 10;

-- Complex joins and subqueries
SELECT c.customer_name, recent_orders.order_count, recent_orders.total_spent
FROM customers c
JOIN (
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        SUM(order_total) as total_spent
    FROM orders
    WHERE order_date >= CURRENT_DATE - INTERVAL 30 DAYS
    GROUP BY customer_id
    HAVING COUNT(*) > 5
) recent_orders ON c.customer_id = recent_orders.customer_id
WHERE c.customer_segment = 'Premium';
```

### Data Formats

**Supported File Formats:**
```sql
-- Parquet (Recommended for analytics)
CREATE TABLE sales_parquet (
    sale_id BIGINT,
    customer_id INT,
    product_id INT,
    sale_amount DECIMAL(10,2),
    sale_date DATE
)
STORED AS PARQUET
TBLPROPERTIES (
    'parquet.compression'='SNAPPY',
    'parquet.block.size'='268435456'  -- 256MB
);

-- ORC format
CREATE TABLE sales_orc (
    sale_id BIGINT,
    customer_id INT,
    sale_amount DECIMAL(10,2)
)
STORED AS ORC
TBLPROPERTIES (
    'orc.compress'='SNAPPY',
    'orc.stripe.size'='268435456'
);

-- Avro with schema evolution
CREATE TABLE user_events (
    event_id STRING,
    user_id STRING,
    event_type STRING,
    event_data STRING
)
STORED AS AVRO
TBLPROPERTIES (
    'avro.schema.literal'='{
        "type": "record",
        "name": "UserEvent",
        "fields": [
            {"name": "event_id", "type": "string"},
            {"name": "user_id", "type": "string"},
            {"name": "event_type", "type": "string"},
            {"name": "event_data", "type": ["null", "string"], "default": null}
        ]
    }'
);
```

### Performance Optimizations

**Built-in Optimizations:**
```sql
-- Automatic optimizations
SET QUERY_TIMEOUT_S=300;
SET MEM_LIMIT=4GB;
SET DISABLE_CODEGEN=false;

-- Cost-based optimization with statistics
COMPUTE STATS sales_table;
COMPUTE INCREMENTAL STATS partitioned_sales;

-- Query hints for join optimization
SELECT /*+ BROADCAST(small_table) */
    l.large_column,
    s.small_column
FROM large_table l
JOIN small_table s ON l.id = s.id;

-- Partition pruning
SELECT * FROM sales_partitioned
WHERE year = 2023 AND month IN (1, 2, 3);
```

## 🎯 Use Cases

### 1. Interactive Business Intelligence
```sql
-- Real-time dashboard queries
SELECT 
    DATE_TRUNC('hour', event_timestamp) as hour,
    event_type,
    COUNT(*) as event_count,
    COUNT(DISTINCT user_id) as unique_users
FROM user_events
WHERE event_timestamp >= NOW() - INTERVAL 24 HOURS
GROUP BY 1, 2
ORDER BY 1 DESC, event_count DESC;
```

### 2. Ad-hoc Data Exploration
```sql
-- Exploratory data analysis
SELECT 
    customer_segment,
    AVG(DATEDIFF(last_order_date, first_order_date)) as avg_customer_lifespan,
    AVG(total_orders) as avg_orders_per_customer,
    AVG(total_spent) as avg_lifetime_value
FROM (
    SELECT 
        c.customer_segment,
        MIN(o.order_date) as first_order_date,
        MAX(o.order_date) as last_order_date,
        COUNT(*) as total_orders,
        SUM(o.order_total) as total_spent
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_segment
) customer_metrics
GROUP BY customer_segment;
```

### 3. Real-time Reporting
```sql
-- Near real-time metrics
CREATE VIEW real_time_sales_metrics AS
SELECT 
    DATE_TRUNC('minute', sale_timestamp) as minute,
    SUM(sale_amount) as total_sales,
    COUNT(*) as transaction_count,
    AVG(sale_amount) as avg_transaction_value,
    COUNT(DISTINCT customer_id) as unique_customers
FROM sales_stream
WHERE sale_timestamp >= NOW() - INTERVAL 1 HOUR
GROUP BY 1
ORDER BY 1 DESC;
```

## 🔗 Integrations

### BI Tool Integration
```python
# Python JDBC connection
import jaydebeapi

# Connection string
jdbc_url = "jdbc:impala://impala-server:21050/default;AuthMech=1"
driver = "com.cloudera.impala.jdbc41.Driver"

# Connect and query
conn = jaydebeapi.connect(driver, jdbc_url)
cursor = conn.cursor()

cursor.execute("""
    SELECT customer_segment, COUNT(*), AVG(order_total)
    FROM customer_orders 
    WHERE order_date >= '2023-01-01'
    GROUP BY customer_segment
""")

results = cursor.fetchall()
print("Query results:", results)
```

### Hadoop Ecosystem Integration
```sql
-- Access Hive tables
SELECT * FROM hive_database.hive_table LIMIT 10;

-- Query HBase tables
SELECT * FROM hbase_table 
WHERE rowkey LIKE 'user_%'
LIMIT 100;

-- Access HDFS files directly
CREATE EXTERNAL TABLE external_data (
    id INT,
    name STRING,
    value DOUBLE
)
LOCATION '/hdfs/path/to/data/'
STORED AS PARQUET;
```

## 📋 Best Practices

### 1. Table Design
```sql
-- Optimal partitioning strategy
CREATE TABLE sales_optimized (
    sale_id BIGINT,
    customer_id INT,
    product_id INT,
    sale_amount DECIMAL(10,2),
    sale_timestamp TIMESTAMP
)
PARTITIONED BY (year INT, month INT)
STORED AS PARQUET
TBLPROPERTIES (
    'parquet.compression'='SNAPPY',
    'parquet.block.size'='268435456'
);

-- Keep partitions reasonably sized (256MB - 1GB)
-- Avoid over-partitioning (too many small partitions)
```

### 2. Query Optimization
```sql
-- Use appropriate data types
CREATE TABLE optimized_schema (
    id BIGINT,                    -- Use BIGINT for large IDs
    status TINYINT,               -- Use TINYINT for small integers
    amount DECIMAL(10,2),         -- Use DECIMAL for currency
    created_date DATE,            -- Use DATE instead of TIMESTAMP when time not needed
    description STRING            -- Use STRING for variable-length text
);

-- Compute and maintain statistics
COMPUTE STATS sales_table;
COMPUTE INCREMENTAL STATS partitioned_table;

-- Use query hints when needed
SELECT /*+ STRAIGHT_JOIN */ * 
FROM large_table l
JOIN medium_table m ON l.id = m.id
JOIN small_table s ON m.id = s.id;
```

### 3. Performance Monitoring
```sql
-- Monitor query performance
PROFILE;  -- After running a query
SUMMARY;  -- Get execution summary

-- Check resource usage
SHOW QUERY STATS;

-- Monitor cluster health
SELECT * FROM sys.impala_query_log 
WHERE start_time > NOW() - INTERVAL 1 HOUR
ORDER BY memory_aggregate_peak DESC;
```

## ⚠️ Limitations

### 1. Fault Tolerance
- **Query-level recovery**: Failed queries restart from beginning
- **No intermediate checkpointing**: Unlike Spark, no mid-query recovery
- **Memory constraints**: Large queries may fail if memory insufficient

### 2. Data Modification
```sql
-- Limited DML support
-- INSERT is supported
INSERT INTO target_table SELECT * FROM source_table;

-- UPDATE and DELETE have limitations
-- Not supported on HDFS tables
-- Supported on Kudu tables only
UPDATE kudu_table SET status = 'active' WHERE id = 123;
DELETE FROM kudu_table WHERE created_date < '2022-01-01';
```

### 3. Complex Data Types
```sql
-- Limited support for nested data
-- Basic ARRAY and MAP support
SELECT 
    customer_id,
    orders[0].order_id as first_order_id,
    SIZE(orders) as order_count
FROM customers_with_orders;

-- Complex nested operations may require flattening
```

## 📈 Version Highlights

### Impala 4.x Features
- **Improved Kudu integration**: Better performance for real-time updates
- **Enhanced security**: Fine-grained access control
- **Query result caching**: Faster repeated queries
- **Admission control improvements**: Better resource management

### Impala 3.x Features
- **ACID transactions**: Support for transactional tables
- **Ranger integration**: Comprehensive security policies
- **Parquet improvements**: Better compression and encoding
- **Scalability enhancements**: Support for larger clusters

### Recent Improvements
```sql
-- Query result caching (4.x)
SET QUERY_CACHE_ENABLED=true;
SET QUERY_CACHE_TTL_SECONDS=3600;

-- Improved admission control
SET REQUEST_POOL='analytics_pool';
SET MEM_LIMIT=8GB;
SET QUERY_TIMEOUT_S=1800;
```

## 🎯 Interview Focus Areas

1. **Architecture**: Impala daemons, Statestore, Catalog Service
2. **vs Hive**: Performance differences, use case comparison
3. **Query Execution**: MPP architecture, distributed processing
4. **Memory Management**: Buffer pools, spill-to-disk
5. **Performance**: Optimization techniques, statistics
6. **Data Formats**: Parquet, ORC, Avro support
7. **SQL Features**: Window functions, complex joins
8. **Limitations**: Fault tolerance, DML restrictions
9. **Integration**: BI tools, Hadoop ecosystem
10. **Best Practices**: Table design, query optimization

## 📚 Quick References

- [Impala Documentation](https://impala.apache.org/docs/build/html/)
- [Cloudera Impala Guide](https://docs.cloudera.com/cdp-private-cloud-base/7.1.8/impala-overview/topics/impala.html)
- [Impala SQL Reference](https://impala.apache.org/docs/build/html/topics/impala_langref.html)
- [Performance Tuning Guide](https://impala.apache.org/docs/build/html/topics/impala_perf_tuning.html)