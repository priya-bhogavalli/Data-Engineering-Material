# Apache Impala - Comprehensive Interview Questions & Answers

## 📋 Table of Contents
1. [Core Concepts](#-core-concepts)
2. [Architecture & Components](#-architecture--components)
3. [SQL & Query Processing](#-sql--query-processing)
4. [Performance Optimization](#-performance-optimization)
5. [Data Formats & Storage](#-data-formats--storage)
6. [Security & Administration](#-security--administration)
7. [Integration & Use Cases](#-integration--use-cases)
8. [Real-world Scenarios](#-real-world-scenarios)

---

## 🎯 Core Concepts

### Q1: What is Apache Impala and what problems does it solve?
**Answer:**
Apache Impala is a modern, open-source, distributed SQL query engine for Apache Hadoop that provides low-latency queries and high concurrency for business intelligence and analytics workloads.

**Key Problems Solved:**
- **Low Latency**: Sub-second to few-second query response times
- **Interactive Analytics**: Real-time business intelligence on big data
- **SQL Compatibility**: Standard SQL interface for Hadoop data
- **High Concurrency**: Support for many concurrent users
- **No ETL Required**: Query data in place without movement

**Core Features:**
- Massively Parallel Processing (MPP) architecture
- In-memory processing with spill-to-disk
- Columnar storage optimization
- Cost-based query optimization
- Integration with Hadoop ecosystem

### Q2: How does Impala differ from Hive?
**Answer:**
**Impala vs Hive Comparison:**

| Aspect | Impala | Hive |
|--------|--------|------|
| **Processing Model** | MPP (native C++) | MapReduce/Tez/Spark |
| **Latency** | Sub-second to seconds | Minutes to hours |
| **Use Case** | Interactive analytics | Batch processing |
| **SQL Support** | ANSI SQL subset | HiveQL (SQL-like) |
| **Memory Usage** | In-memory processing | Disk-based processing |
| **Fault Tolerance** | Query-level restart | Task-level restart |
| **Concurrency** | High (100+ users) | Medium (10-50 users) |
| **Data Formats** | Parquet, ORC, Avro, Text | All Hadoop formats |

**When to Use Impala:**
- Interactive dashboards and BI tools
- Ad-hoc data exploration
- Real-time reporting
- Low-latency analytics

**When to Use Hive:**
- ETL and batch processing
- Complex data transformations
- Large-scale data processing
- Fault-tolerant long-running jobs

### Q3: What are the key architectural components of Impala?
**Answer:**
**Impala Architecture Components:**

```
Client → Impala Daemon → HDFS/HBase
   ↓         ↓              ↓
StateStore ← Catalog Service ← Hive Metastore
```

**1. Impala Daemon (impalad)**
- Query execution engine
- Runs on each DataNode
- Handles client connections
- Executes query fragments

**2. Statestore Daemon**
- Cluster membership service
- Monitors daemon health
- Distributes metadata updates
- Handles node failures

**3. Catalog Service**
- Metadata management
- Synchronizes with Hive Metastore
- Distributes schema changes
- Manages table statistics

**4. Query Coordinator**
- Plans query execution
- Distributes work to executors
- Aggregates results
- Returns data to client

---

## 🏗️ Architecture & Components

### Q4: Explain Impala's query execution architecture
**Answer:**
**Impala Query Execution Flow:**

**1. Query Planning Phase:**
```sql
-- Example query
SELECT c.customer_name, SUM(o.order_amount)
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2023-01-01'
GROUP BY c.customer_name
ORDER BY SUM(o.order_amount) DESC
LIMIT 10;
```

**2. Execution Steps:**

**a) Parse and Analyze:**
- SQL parsing and validation
- Semantic analysis
- Access control checks
- Metadata retrieval

**b) Query Planning:**
- Cost-based optimization
- Join order optimization
- Predicate pushdown
- Partition pruning

**c) Fragment Generation:**
- Break query into fragments
- Assign fragments to nodes
- Create execution tree

**d) Distributed Execution:**
- Parallel fragment execution
- Data exchange between nodes
- Intermediate result aggregation
- Final result collection

**3. Execution Tree Example:**
```
                    [Coordinator]
                         |
                    [TOP-N: 10]
                         |
                   [ORDER BY]
                         |
                   [AGGREGATE]
                         |
                   [HASH JOIN]
                    /        \
            [SCAN: customers] [SCAN: orders]
```

### Q5: How does Impala handle memory management?
**Answer:**
**Impala Memory Management:**

**1. Memory Pools:**
```bash
# Memory configuration
--mem_limit=8GB                    # Total memory limit per daemon
--buffer_pool_limit=6GB            # Buffer pool size
--min_buffer_size=64KB             # Minimum buffer size
--max_buffer_size=8MB              # Maximum buffer size
```

**2. Memory Usage Categories:**

**a) Query Memory:**
- Hash tables for joins
- Aggregation buffers
- Sort operations
- Exchange operators

**b) Buffer Pool:**
- I/O buffers for reading data
- Intermediate result storage
- Spill-to-disk buffers

**c) System Memory:**
- Metadata caching
- Connection handling
- Background processes

**3. Memory Management Strategies:**

**a) Admission Control:**
```sql
-- Set query memory limit
SET MEM_LIMIT=2GB;

-- Check memory usage
SELECT * FROM sys.impala_query_log 
WHERE memory_aggregate_peak > 1000000000; -- 1GB
```

**b) Spill-to-Disk:**
```bash
# Configure scratch directories
--scratch_dirs=/tmp/impala-scratch1,/tmp/impala-scratch2
```

**c) Memory Monitoring:**
```sql
-- Query memory usage
SHOW QUERY STATS;

-- Profile memory usage
PROFILE;
```

### Q6: Explain Impala's fault tolerance mechanisms
**Answer:**
**Impala Fault Tolerance:**

**1. Query-level Fault Tolerance:**
- Failed queries are retried from beginning
- No intermediate state recovery
- Client receives error for failed queries

**2. Node Failure Handling:**
```bash
# Statestore monitors node health
# Failed nodes removed from cluster
# Queries redistributed to healthy nodes
```

**3. Metadata Synchronization:**
```sql
-- Refresh metadata after external changes
REFRESH table_name;

-- Invalidate metadata cache
INVALIDATE METADATA table_name;

-- Compute table statistics
COMPUTE STATS table_name;
```

**4. High Availability Setup:**
```bash
# Multiple Catalog Service instances
# Load balancer for client connections
# Automatic failover configuration

# Example HA configuration
--catalog_service_host=catalog1.example.com:26000,catalog2.example.com:26000
--state_store_host=statestore1.example.com:24000,statestore2.example.com:24000
```

**5. Monitoring and Alerting:**
```sql
-- Check cluster health
SELECT * FROM sys.impala_nodes WHERE is_healthy = false;

-- Monitor query failures
SELECT query_id, error_message, start_time
FROM sys.impala_query_log
WHERE query_state = 'EXCEPTION'
AND start_time > NOW() - INTERVAL 1 HOUR;
```

---

## 📝 SQL & Query Processing

### Q7: What SQL features does Impala support?
**Answer:**
**Impala SQL Features:**

**1. Standard SQL Operations:**
```sql
-- SELECT with complex expressions
SELECT 
    customer_id,
    UPPER(customer_name) as name,
    CASE 
        WHEN age < 25 THEN 'Young'
        WHEN age < 50 THEN 'Middle'
        ELSE 'Senior'
    END as age_group,
    COALESCE(phone, 'N/A') as contact
FROM customers
WHERE registration_date >= '2023-01-01'
ORDER BY customer_name
LIMIT 100;
```

**2. Joins and Subqueries:**
```sql
-- Complex joins
SELECT c.customer_name, o.order_total, p.product_name
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date BETWEEN '2023-01-01' AND '2023-12-31';

-- Correlated subqueries
SELECT customer_name
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id 
    AND o.order_total > 1000
);
```

**3. Window Functions:**
```sql
-- Ranking and analytics
SELECT 
    customer_id,
    order_date,
    order_total,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as order_sequence,
    SUM(order_total) OVER (PARTITION BY customer_id ORDER BY order_date 
                          ROWS UNBOUNDED PRECEDING) as running_total,
    LAG(order_total, 1) OVER (PARTITION BY customer_id ORDER BY order_date) as prev_order
FROM orders;
```

**4. Aggregate Functions:**
```sql
-- Standard and advanced aggregations
SELECT 
    product_category,
    COUNT(*) as product_count,
    AVG(price) as avg_price,
    STDDEV(price) as price_stddev,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price) as median_price,
    STRING_AGG(product_name, ', ') as product_list
FROM products
GROUP BY product_category
HAVING COUNT(*) > 10;
```

**5. Data Types and Functions:**
```sql
-- Date/time functions
SELECT 
    order_date,
    EXTRACT(YEAR FROM order_date) as order_year,
    DATE_ADD(order_date, INTERVAL 30 DAY) as due_date,
    DATEDIFF(CURRENT_DATE(), order_date) as days_ago
FROM orders;

-- String functions
SELECT 
    CONCAT(first_name, ' ', last_name) as full_name,
    LENGTH(customer_name) as name_length,
    REGEXP_REPLACE(phone, '[^0-9]', '') as clean_phone
FROM customers;
```

### Q8: How do you optimize Impala queries?
**Answer:**
**Impala Query Optimization Techniques:**

**1. Table Statistics:**
```sql
-- Compute table statistics
COMPUTE STATS customers;
COMPUTE STATS orders;

-- Compute incremental statistics
COMPUTE INCREMENTAL STATS partitioned_table;

-- Show table statistics
SHOW TABLE STATS customers;
SHOW COLUMN STATS customers;
```

**2. Partitioning:**
```sql
-- Create partitioned table
CREATE TABLE sales_partitioned (
    sale_id BIGINT,
    customer_id INT,
    product_id INT,
    sale_amount DECIMAL(10,2),
    sale_date DATE
)
PARTITIONED BY (year INT, month INT)
STORED AS PARQUET;

-- Query with partition pruning
SELECT * FROM sales_partitioned
WHERE year = 2023 AND month IN (1, 2, 3);
```

**3. Join Optimization:**
```sql
-- Use broadcast joins for small tables
SELECT /*+ BROADCAST(small_table) */
    l.large_column,
    s.small_column
FROM large_table l
JOIN small_table s ON l.id = s.id;

-- Use shuffle joins for large tables
SELECT /*+ SHUFFLE(large_table1) */
    t1.column1,
    t2.column2
FROM large_table1 t1
JOIN large_table2 t2 ON t1.id = t2.id;
```

**4. Query Hints:**
```sql
-- Memory limit hint
SELECT /*+ MEM_LIMIT(2GB) */ * FROM large_table;

-- Straight join hint
SELECT /*+ STRAIGHT_JOIN */
    t1.col1, t2.col2, t3.col3
FROM table1 t1
JOIN table2 t2 ON t1.id = t2.id
JOIN table3 t3 ON t2.id = t3.id;
```

**5. Query Profiling:**
```sql
-- Enable query profiling
SET QUERY_TIMEOUT_S=300;
SET MEM_LIMIT=4GB;

-- Execute query
SELECT COUNT(*) FROM large_table WHERE condition = 'value';

-- View query profile
PROFILE;

-- Summary profile
SUMMARY;
```

### Q9: How do you handle complex analytical queries in Impala?
**Answer:**
**Complex Analytical Query Patterns:**

**1. Time Series Analysis:**
```sql
-- Daily sales trend with moving average
WITH daily_sales AS (
    SELECT 
        DATE(order_date) as sale_date,
        SUM(order_total) as daily_total
    FROM orders
    WHERE order_date >= '2023-01-01'
    GROUP BY DATE(order_date)
),
moving_avg AS (
    SELECT 
        sale_date,
        daily_total,
        AVG(daily_total) OVER (
            ORDER BY sale_date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) as moving_avg_7day
    FROM daily_sales
)
SELECT * FROM moving_avg ORDER BY sale_date;
```

**2. Customer Segmentation:**
```sql
-- RFM Analysis (Recency, Frequency, Monetary)
WITH customer_metrics AS (
    SELECT 
        customer_id,
        DATEDIFF(CURRENT_DATE(), MAX(order_date)) as recency,
        COUNT(*) as frequency,
        SUM(order_total) as monetary
    FROM orders
    WHERE order_date >= '2022-01-01'
    GROUP BY customer_id
),
rfm_scores AS (
    SELECT 
        customer_id,
        recency,
        frequency,
        monetary,
        NTILE(5) OVER (ORDER BY recency DESC) as r_score,
        NTILE(5) OVER (ORDER BY frequency) as f_score,
        NTILE(5) OVER (ORDER BY monetary) as m_score
    FROM customer_metrics
)
SELECT 
    customer_id,
    CASE 
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Loyal Customers'
        WHEN r_score >= 3 AND f_score <= 2 THEN 'Potential Loyalists'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk'
        ELSE 'Others'
    END as customer_segment
FROM rfm_scores;
```

**3. Cohort Analysis:**
```sql
-- Monthly cohort retention analysis
WITH first_purchase AS (
    SELECT 
        customer_id,
        DATE_TRUNC('month', MIN(order_date)) as cohort_month
    FROM orders
    GROUP BY customer_id
),
customer_activities AS (
    SELECT 
        fp.customer_id,
        fp.cohort_month,
        DATE_TRUNC('month', o.order_date) as activity_month,
        MONTHS_BETWEEN(DATE_TRUNC('month', o.order_date), fp.cohort_month) as period_number
    FROM first_purchase fp
    JOIN orders o ON fp.customer_id = o.customer_id
),
cohort_table AS (
    SELECT 
        cohort_month,
        period_number,
        COUNT(DISTINCT customer_id) as customers
    FROM customer_activities
    GROUP BY cohort_month, period_number
),
cohort_sizes AS (
    SELECT 
        cohort_month,
        customers as cohort_size
    FROM cohort_table
    WHERE period_number = 0
)
SELECT 
    ct.cohort_month,
    ct.period_number,
    ct.customers,
    ROUND(100.0 * ct.customers / cs.cohort_size, 2) as retention_rate
FROM cohort_table ct
JOIN cohort_sizes cs ON ct.cohort_month = cs.cohort_month
ORDER BY ct.cohort_month, ct.period_number;
```

---

## ⚡ Performance Optimization

### Q10: What are the key performance optimization strategies for Impala?
**Answer:**
**Impala Performance Optimization:**

**1. Data Format Optimization:**
```sql
-- Use Parquet for analytical workloads
CREATE TABLE optimized_table (
    id BIGINT,
    name STRING,
    amount DECIMAL(10,2),
    created_date TIMESTAMP
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- Convert existing table to Parquet
CREATE TABLE new_parquet_table
STORED AS PARQUET
AS SELECT * FROM old_text_table;
```

**2. Partitioning Strategy:**
```sql
-- Partition by commonly filtered columns
CREATE TABLE sales_optimized (
    sale_id BIGINT,
    customer_id INT,
    product_id INT,
    sale_amount DECIMAL(10,2)
)
PARTITIONED BY (year INT, month INT, day INT)
STORED AS PARQUET;

-- Avoid over-partitioning (keep partitions > 256MB)
-- Use partition pruning in queries
SELECT * FROM sales_optimized 
WHERE year = 2023 AND month = 12;
```

**3. Join Optimization:**
```sql
-- Broadcast join for small dimension tables
SELECT /*+ BROADCAST(d) */
    f.fact_column,
    d.dimension_column
FROM fact_table f
JOIN dimension_table d ON f.dim_id = d.dim_id;

-- Optimize join order (largest table last)
SELECT t1.col1, t2.col2, t3.col3
FROM small_table t1
JOIN medium_table t2 ON t1.id = t2.id
JOIN large_table t3 ON t2.id = t3.id;
```

**4. Memory and Resource Tuning:**
```bash
# Impala daemon configuration
--mem_limit=16GB
--num_scanner_threads=16
--be_port=22000
--krpc_port=27000

# Query-specific settings
SET MEM_LIMIT=4GB;
SET NUM_NODES=1;  # For single-node testing
SET DISABLE_CODEGEN=false;
```

**5. Statistics and Metadata:**
```sql
-- Keep statistics current
COMPUTE STATS fact_table;
COMPUTE INCREMENTAL STATS partitioned_table;

-- Refresh metadata after external changes
REFRESH fact_table;
INVALIDATE METADATA;

-- Monitor statistics freshness
SHOW TABLE STATS fact_table;
```

### Q11: How do you troubleshoot slow Impala queries?
**Answer:**
**Impala Query Troubleshooting:**

**1. Query Profiling:**
```sql
-- Execute query with profiling
SET QUERY_TIMEOUT_S=600;
SELECT COUNT(*) FROM large_table WHERE complex_condition;

-- View detailed profile
PROFILE;

-- View summary profile
SUMMARY;
```

**2. Profile Analysis:**
```bash
# Key metrics to check:
# - Total query time
# - Planning time
# - Execution time per fragment
# - Memory usage
# - Rows processed vs rows returned
# - Network time
# - Disk I/O time
```

**3. Common Performance Issues:**

**a) Missing Statistics:**
```sql
-- Check if statistics exist
SHOW TABLE STATS problematic_table;
SHOW COLUMN STATS problematic_table;

-- Compute missing statistics
COMPUTE STATS problematic_table;
```

**b) Inefficient Joins:**
```sql
-- Check join strategy in profile
-- Look for:
-- - Cross joins (Cartesian products)
-- - Large shuffle operations
-- - Uneven data distribution

-- Fix with appropriate hints
SELECT /*+ BROADCAST(small_table) */
FROM large_table l JOIN small_table s ON l.id = s.id;
```

**c) Memory Issues:**
```sql
-- Check memory usage in profile
-- Increase memory limit if needed
SET MEM_LIMIT=8GB;

-- Enable spill to disk
SET SCRATCH_LIMIT=10GB;
```

**4. Query Optimization Checklist:**
```sql
-- 1. Check execution plan
EXPLAIN SELECT * FROM table WHERE condition;

-- 2. Verify partition pruning
EXPLAIN SELECT * FROM partitioned_table WHERE partition_col = 'value';

-- 3. Check predicate pushdown
EXPLAIN SELECT * FROM table WHERE filterable_column = 'value';

-- 4. Analyze join order and strategy
EXPLAIN SELECT * FROM t1 JOIN t2 ON t1.id = t2.id;
```

### Q12: How do you handle large-scale data processing in Impala?
**Answer:**
**Large-Scale Data Processing Strategies:**

**1. Cluster Sizing:**
```bash
# Recommended cluster configuration
# - 3-5 nodes minimum for production
# - 128GB+ RAM per node
# - SSD storage for scratch space
# - 10Gb+ network connectivity

# Node configuration
--mem_limit=64GB
--num_scanner_threads=32
--scratch_dirs=/ssd1/impala-scratch,/ssd2/impala-scratch
```

**2. Data Layout Optimization:**
```sql
-- Optimize file sizes (aim for 256MB - 1GB per file)
CREATE TABLE optimized_large_table (
    id BIGINT,
    data STRING,
    created_date DATE
)
PARTITIONED BY (year INT, month INT)
STORED AS PARQUET
TBLPROPERTIES (
    'parquet.block.size'='268435456',  -- 256MB
    'parquet.compression'='SNAPPY'
);

-- Compact small files
INSERT OVERWRITE TABLE optimized_large_table
SELECT * FROM fragmented_table;
```

**3. Query Patterns for Large Data:**
```sql
-- Use LIMIT for exploratory queries
SELECT * FROM huge_table LIMIT 1000;

-- Aggregate before joins
WITH aggregated_data AS (
    SELECT 
        customer_id,
        SUM(order_total) as total_spent,
        COUNT(*) as order_count
    FROM orders
    WHERE order_date >= '2023-01-01'
    GROUP BY customer_id
)
SELECT c.customer_name, a.total_spent, a.order_count
FROM customers c
JOIN aggregated_data a ON c.customer_id = a.customer_id;
```

**4. Batch Processing Patterns:**
```sql
-- Process data in chunks
WITH date_ranges AS (
    SELECT 
        '2023-01-01' as start_date, '2023-01-31' as end_date
    UNION ALL
    SELECT 
        '2023-02-01' as start_date, '2023-02-28' as end_date
    -- ... more ranges
)
SELECT 
    dr.start_date,
    dr.end_date,
    COUNT(*) as record_count,
    SUM(amount) as total_amount
FROM date_ranges dr
JOIN transactions t ON t.transaction_date BETWEEN dr.start_date AND dr.end_date
GROUP BY dr.start_date, dr.end_date;
```

---

## 💾 Data Formats & Storage

### Q13: How does Impala work with different data formats?
**Answer:**
**Impala Data Format Support:**

**1. Parquet (Recommended):**
```sql
-- Create Parquet table
CREATE TABLE parquet_table (
    id BIGINT,
    name STRING,
    amount DECIMAL(10,2),
    created_date TIMESTAMP
)
STORED AS PARQUET
TBLPROPERTIES (
    'parquet.compression'='SNAPPY',
    'parquet.block.size'='268435456'
);

-- Benefits:
-- - Columnar storage
-- - Excellent compression
-- - Predicate pushdown
-- - Schema evolution support
```

**2. ORC Format:**
```sql
-- Create ORC table
CREATE TABLE orc_table (
    id BIGINT,
    data STRING,
    amount DOUBLE
)
STORED AS ORC
TBLPROPERTIES (
    'orc.compress'='SNAPPY',
    'orc.stripe.size'='268435456'
);

-- Good for:
-- - ACID transactions (with Hive)
-- - Complex nested data
-- - High compression ratios
```

**3. Avro Format:**
```sql
-- Create Avro table
CREATE TABLE avro_table (
    id BIGINT,
    user_data STRING,
    metadata STRING
)
STORED AS AVRO
TBLPROPERTIES (
    'avro.schema.literal'='{
        "type": "record",
        "name": "User",
        "fields": [
            {"name": "id", "type": "long"},
            {"name": "user_data", "type": "string"},
            {"name": "metadata", "type": "string"}
        ]
    }'
);

-- Benefits:
-- - Schema evolution
-- - Cross-language support
-- - Rich data types
```

**4. Text/CSV Format:**
```sql
-- Create text table
CREATE TABLE text_table (
    id INT,
    name STRING,
    email STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE;

-- Use for:
-- - Data ingestion
-- - Human-readable formats
-- - Legacy system integration
```

**5. Format Conversion:**
```sql
-- Convert text to Parquet
CREATE TABLE parquet_converted
STORED AS PARQUET
AS SELECT * FROM text_table;

-- Bulk conversion with partitioning
CREATE TABLE partitioned_parquet (
    id BIGINT,
    data STRING,
    amount DECIMAL(10,2)
)
PARTITIONED BY (year INT, month INT)
STORED AS PARQUET;

INSERT INTO partitioned_parquet
PARTITION (year, month)
SELECT 
    id, data, amount,
    YEAR(created_date) as year,
    MONTH(created_date) as month
FROM source_table;
```

### Q14: How do you manage schema evolution in Impala?
**Answer:**
**Schema Evolution Strategies:**

**1. Parquet Schema Evolution:**
```sql
-- Original table schema
CREATE TABLE evolving_table (
    id BIGINT,
    name STRING,
    created_date TIMESTAMP
)
STORED AS PARQUET;

-- Add new column (safe operation)
ALTER TABLE evolving_table ADD COLUMNS (
    email STRING,
    phone STRING
);

-- Refresh metadata
REFRESH evolving_table;
```

**2. Backward Compatibility:**
```sql
-- Handle missing columns with defaults
SELECT 
    id,
    name,
    COALESCE(email, 'unknown@example.com') as email,
    COALESCE(phone, 'N/A') as phone,
    created_date
FROM evolving_table;
```

**3. Schema Versioning:**
```sql
-- Create versioned tables
CREATE TABLE customer_v1 (
    id BIGINT,
    name STRING
) STORED AS PARQUET;

CREATE TABLE customer_v2 (
    id BIGINT,
    first_name STRING,
    last_name STRING,
    email STRING
) STORED AS PARQUET;

-- Migration view
CREATE VIEW customers AS
SELECT 
    id,
    COALESCE(first_name, SPLIT_PART(name, ' ', 1)) as first_name,
    COALESCE(last_name, SPLIT_PART(name, ' ', 2)) as last_name,
    email
FROM customer_v2
UNION ALL
SELECT 
    id,
    SPLIT_PART(name, ' ', 1) as first_name,
    SPLIT_PART(name, ' ', 2) as last_name,
    CAST(NULL AS STRING) as email
FROM customer_v1
WHERE id NOT IN (SELECT id FROM customer_v2);
```

**4. Complex Type Evolution:**
```sql
-- Avro schema evolution
CREATE TABLE avro_evolving
STORED AS AVRO
TBLPROPERTIES (
    'avro.schema.literal'='{
        "type": "record",
        "name": "UserEvent",
        "fields": [
            {"name": "user_id", "type": "long"},
            {"name": "event_type", "type": "string"},
            {"name": "properties", "type": ["null", "string"], "default": null}
        ]
    }'
);

-- Update schema with new field
ALTER TABLE avro_evolving
SET TBLPROPERTIES (
    'avro.schema.literal'='{
        "type": "record",
        "name": "UserEvent",
        "fields": [
            {"name": "user_id", "type": "long"},
            {"name": "event_type", "type": "string"},
            {"name": "properties", "type": ["null", "string"], "default": null},
            {"name": "timestamp", "type": ["null", "long"], "default": null}
        ]
    }'
);
```

---

## 🔒 Security & Administration

### Q15: How do you implement security in Impala?
**Answer:**
**Impala Security Implementation:**

**1. Authentication:**
```bash
# Kerberos authentication
--principal=impala/_HOST@REALM.COM
--keytab_file=/etc/security/keytabs/impala.keytab
--be_principal=impala/_HOST@REALM.COM

# LDAP authentication
--enable_ldap_auth=true
--ldap_uri=ldap://ldap.company.com:389
--ldap_bind_dn=cn=impala,ou=services,dc=company,dc=com
--ldap_bind_password_cmd="cat /etc/impala/ldap_password"
```

**2. Authorization with Apache Ranger:**
```sql
-- Create policies in Ranger UI or via API
-- Database-level access
GRANT SELECT ON DATABASE sales_db TO ROLE analyst_role;

-- Table-level access
GRANT SELECT, INSERT ON TABLE sales_db.transactions TO ROLE data_engineer_role;

-- Column-level access
GRANT SELECT(customer_id, order_date, amount) ON TABLE sales_db.orders TO ROLE report_role;
```

**3. Row-Level Security:**
```sql
-- Create security view
CREATE VIEW secure_customer_view AS
SELECT 
    customer_id,
    customer_name,
    CASE 
        WHEN USER() IN ('admin@company.com', 'manager@company.com') 
        THEN email 
        ELSE 'REDACTED' 
    END as email,
    CASE 
        WHEN USER() IN ('admin@company.com') 
        THEN ssn 
        ELSE 'XXX-XX-XXXX' 
    END as ssn
FROM customers;

-- Grant access to view instead of table
GRANT SELECT ON secure_customer_view TO ROLE analyst_role;
```

**4. Data Masking:**
```sql
-- Create masked view for sensitive data
CREATE VIEW masked_transactions AS
SELECT 
    transaction_id,
    customer_id,
    CASE 
        WHEN USER() LIKE '%@finance.company.com' THEN amount
        ELSE ROUND(amount, -2)  -- Round to nearest hundred
    END as amount,
    transaction_date,
    CASE 
        WHEN USER() IN ('admin@company.com') THEN credit_card_number
        ELSE CONCAT('****-****-****-', RIGHT(credit_card_number, 4))
    END as credit_card_number
FROM transactions;
```

**5. Audit Logging:**
```bash
# Enable audit logging
--audit_event_log_dir=/var/log/impala/audit
--max_audit_event_log_file_size=5000
--abort_on_failed_audit_event=false

# Log query execution
--log_query_to_file=true
--query_log_dir=/var/log/impala/queries
```

### Q16: How do you monitor and manage Impala clusters?
**Answer:**
**Impala Monitoring and Management:**

**1. Web UI Monitoring:**
```bash
# Impala daemon web UI
http://impala-node:25000

# Key metrics:
# - Active queries
# - Query history
# - Memory usage
# - Admission control status
# - Backend health
```

**2. System Metrics:**
```sql
-- Query system tables
SELECT * FROM sys.impala_query_log 
WHERE start_time > NOW() - INTERVAL 1 HOUR;

-- Check resource usage
SELECT 
    query_id,
    user,
    memory_aggregate_peak,
    hdfs_bytes_read,
    query_state
FROM sys.impala_query_log
WHERE memory_aggregate_peak > 1000000000  -- > 1GB
ORDER BY start_time DESC;
```

**3. Admission Control:**
```bash
# Configure admission control
--admission_control_slots=16
--admission_control_pool_max_requests=200
--admission_control_pool_queue_timeout_ms=60000

# Pool configuration
--fair_scheduler_allocation_path=/etc/impala/fair-scheduler.xml
```

**4. Performance Monitoring:**
```sql
-- Monitor slow queries
SELECT 
    query_id,
    user,
    query_type,
    start_time,
    end_time,
    DATEDIFF(end_time, start_time) as duration_seconds,
    query_state
FROM sys.impala_query_log
WHERE DATEDIFF(end_time, start_time) > 300  -- > 5 minutes
ORDER BY duration_seconds DESC;

-- Check resource utilization
SELECT 
    AVG(memory_aggregate_peak) as avg_memory_mb,
    MAX(memory_aggregate_peak) as max_memory_mb,
    AVG(hdfs_bytes_read) as avg_bytes_read
FROM sys.impala_query_log
WHERE start_time > NOW() - INTERVAL 1 DAY;
```

**5. Health Check Script:**
```bash
#!/bin/bash
# impala-health-check.sh

IMPALA_NODES="node1:25000 node2:25000 node3:25000"
ALERT_EMAIL="admin@company.com"

for node in $IMPALA_NODES; do
    # Check if daemon is responding
    response=$(curl -s -o /dev/null -w "%{http_code}" http://$node/healthz)
    
    if [ "$response" != "200" ]; then
        echo "ALERT: Impala daemon on $node is not responding" | \
        mail -s "Impala Health Alert" $ALERT_EMAIL
    fi
    
    # Check memory usage
    memory_usage=$(curl -s http://$node/memz | grep -o 'Total: [0-9.]*' | cut -d' ' -f2)
    if (( $(echo "$memory_usage > 0.9" | bc -l) )); then
        echo "WARNING: High memory usage on $node: ${memory_usage}%" | \
        mail -s "Impala Memory Alert" $ALERT_EMAIL
    fi
done
```

---

## 🔗 Integration & Use Cases

### Q17: How do you integrate Impala with BI tools?
**Answer:**
**Impala BI Tool Integration:**

**1. JDBC/ODBC Connectivity:**
```java
// Java JDBC connection
String jdbcUrl = "jdbc:impala://impala-server:21050/default;AuthMech=1;KrbRealm=COMPANY.COM;KrbHostFQDN=impala-server.company.com;KrbServiceName=impala";

Connection conn = DriverManager.getConnection(jdbcUrl);
PreparedStatement stmt = conn.prepareStatement(
    "SELECT customer_segment, COUNT(*), AVG(order_total) " +
    "FROM customer_orders WHERE order_date >= ? GROUP BY customer_segment"
);
stmt.setDate(1, Date.valueOf("2023-01-01"));
ResultSet rs = stmt.executeQuery();
```

**2. Tableau Integration:**
```sql
-- Optimize queries for Tableau
CREATE VIEW tableau_sales_summary AS
SELECT 
    DATE_TRUNC('month', order_date) as order_month,
    customer_segment,
    product_category,
    SUM(order_total) as total_sales,
    COUNT(DISTINCT customer_id) as unique_customers,
    AVG(order_total) as avg_order_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id
GROUP BY 1, 2, 3;

-- Create extract-friendly tables
CREATE TABLE tableau_extract_ready
STORED AS PARQUET
AS SELECT * FROM complex_analytical_view;
```

**3. Power BI Integration:**
```sql
-- Create optimized views for Power BI
CREATE VIEW powerbi_dashboard_data AS
SELECT 
    order_date,
    customer_name,
    product_name,
    order_total,
    CASE 
        WHEN order_total < 100 THEN 'Small'
        WHEN order_total < 500 THEN 'Medium'
        ELSE 'Large'
    END as order_size_category
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id
WHERE order_date >= '2023-01-01';
```

**4. Custom Dashboard Integration:**
```python
# Python integration example
import impala.dbapi

conn = impala.dbapi.connect(
    host='impala-server',
    port=21050,
    auth_mechanism='GSSAPI',
    kerberos_service_name='impala'
)

cursor = conn.cursor()
cursor.execute("""
    SELECT 
        DATE_TRUNC('day', order_date) as day,
        SUM(order_total) as daily_sales
    FROM orders 
    WHERE order_date >= CURRENT_DATE - INTERVAL 30 DAYS
    GROUP BY 1
    ORDER BY 1
""")

results = cursor.fetchall()
# Process results for dashboard
```

### Q18: How do you implement real-time analytics with Impala?
**Answer:**
**Real-time Analytics Implementation:**

**1. Near Real-time Data Pipeline:**
```
Kafka → Flume/Spark Streaming → HDFS/Kudu → Impala
```

**2. Kudu Integration for Real-time Updates:**
```sql
-- Create Kudu table for real-time data
CREATE TABLE real_time_metrics (
    metric_id BIGINT,
    metric_name STRING,
    metric_value DOUBLE,
    timestamp_col TIMESTAMP,
    PRIMARY KEY (metric_id, timestamp_col)
)
PARTITION BY HASH(metric_id) PARTITIONS 16
STORED AS KUDU;

-- Real-time upserts
UPSERT INTO real_time_metrics VALUES
(1, 'page_views', 1500.0, NOW()),
(2, 'active_users', 250.0, NOW()),
(3, 'conversion_rate', 0.045, NOW());
```

**3. Streaming Data Processing:**
```sql
-- Create external table for streaming data
CREATE TABLE streaming_events (
    event_id STRING,
    user_id STRING,
    event_type STRING,
    event_data STRING,
    event_timestamp TIMESTAMP
)
PARTITIONED BY (year INT, month INT, day INT, hour INT)
STORED AS PARQUET
LOCATION '/streaming/events/';

-- Real-time aggregation view
CREATE VIEW real_time_dashboard AS
SELECT 
    event_type,
    COUNT(*) as event_count,
    COUNT(DISTINCT user_id) as unique_users,
    MAX(event_timestamp) as last_event_time
FROM streaming_events
WHERE event_timestamp >= NOW() - INTERVAL 1 HOUR
GROUP BY event_type;
```

**4. Incremental Processing:**
```sql
-- Incremental aggregation pattern
CREATE TABLE hourly_aggregates (
    hour_timestamp TIMESTAMP,
    metric_name STRING,
    metric_value DOUBLE,
    PRIMARY KEY (hour_timestamp, metric_name)
)
STORED AS KUDU;

-- Incremental update procedure
INSERT INTO hourly_aggregates
SELECT 
    DATE_TRUNC('hour', event_timestamp) as hour_timestamp,
    'page_views' as metric_name,
    COUNT(*) as metric_value
FROM streaming_events
WHERE event_timestamp >= '${last_processed_hour}'
  AND event_timestamp < '${current_hour}'
  AND event_type = 'page_view'
GROUP BY 1, 2;
```

---

## 🌟 Real-world Scenarios

### Q19: Design a data warehouse solution using Impala
**Answer:**
**Impala Data Warehouse Design:**

**1. Architecture Overview:**
```
Source Systems → ETL Pipeline → Data Lake → Impala → BI Tools
                                    ↓
                              Data Warehouse
                            (Dimensional Model)
```

**2. Dimensional Model Implementation:**
```sql
-- Fact table design
CREATE TABLE fact_sales (
    sale_id BIGINT,
    customer_key INT,
    product_key INT,
    date_key INT,
    store_key INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(12,2),
    discount_amount DECIMAL(10,2),
    tax_amount DECIMAL(10,2)
)
PARTITIONED BY (year INT, month INT)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- Customer dimension
CREATE TABLE dim_customer (
    customer_key INT,
    customer_id STRING,
    customer_name STRING,
    customer_segment STRING,
    customer_category STRING,
    registration_date DATE,
    address STRING,
    city STRING,
    state STRING,
    country STRING,
    effective_date DATE,
    expiry_date DATE,
    is_current BOOLEAN
)
STORED AS PARQUET;

-- Product dimension
CREATE TABLE dim_product (
    product_key INT,
    product_id STRING,
    product_name STRING,
    product_category STRING,
    product_subcategory STRING,
    brand STRING,
    supplier STRING,
    unit_cost DECIMAL(10,2),
    list_price DECIMAL(10,2)
)
STORED AS PARQUET;

-- Date dimension
CREATE TABLE dim_date (
    date_key INT,
    full_date DATE,
    day_of_week STRING,
    day_of_month INT,
    day_of_year INT,
    week_of_year INT,
    month_name STRING,
    month_number INT,
    quarter STRING,
    year INT,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN
)
STORED AS PARQUET;
```

**3. ETL Process:**
```sql
-- Daily ETL for fact table
INSERT INTO fact_sales PARTITION (year, month)
SELECT 
    s.sale_id,
    dc.customer_key,
    dp.product_key,
    dd.date_key,
    ds.store_key,
    s.quantity,
    s.unit_price,
    s.total_amount,
    s.discount_amount,
    s.tax_amount,
    YEAR(s.sale_date) as year,
    MONTH(s.sale_date) as month
FROM staging_sales s
JOIN dim_customer dc ON s.customer_id = dc.customer_id AND dc.is_current = true
JOIN dim_product dp ON s.product_id = dp.product_id
JOIN dim_date dd ON s.sale_date = dd.full_date
JOIN dim_store ds ON s.store_id = ds.store_id
WHERE s.sale_date = '${process_date}';
```

**4. Analytical Views:**
```sql
-- Sales performance view
CREATE VIEW sales_performance AS
SELECT 
    dd.year,
    dd.month_name,
    dc.customer_segment,
    dp.product_category,
    SUM(fs.total_amount) as total_sales,
    SUM(fs.quantity) as total_quantity,
    COUNT(DISTINCT fs.customer_key) as unique_customers,
    AVG(fs.total_amount) as avg_order_value
FROM fact_sales fs
JOIN dim_date dd ON fs.date_key = dd.date_key
JOIN dim_customer dc ON fs.customer_key = dc.customer_key
JOIN dim_product dp ON fs.product_key = dp.product_key
GROUP BY 1, 2, 3, 4;

-- Customer lifetime value
CREATE VIEW customer_ltv AS
SELECT 
    dc.customer_id,
    dc.customer_name,
    dc.customer_segment,
    MIN(dd.full_date) as first_purchase_date,
    MAX(dd.full_date) as last_purchase_date,
    COUNT(DISTINCT fs.sale_id) as total_orders,
    SUM(fs.total_amount) as lifetime_value,
    AVG(fs.total_amount) as avg_order_value,
    DATEDIFF(MAX(dd.full_date), MIN(dd.full_date)) as customer_lifespan_days
FROM fact_sales fs
JOIN dim_customer dc ON fs.customer_key = dc.customer_key
JOIN dim_date dd ON fs.date_key = dd.date_key
GROUP BY 1, 2, 3;
```

### Q20: Implement a real-time fraud detection system using Impala
**Answer:**
**Real-time Fraud Detection System:**

**1. System Architecture:**
```
Transaction Stream → Kafka → Spark Streaming → Kudu → Impala → Alert System
```

**2. Transaction Data Model:**
```sql
-- Real-time transaction table
CREATE TABLE transactions (
    transaction_id STRING,
    user_id STRING,
    merchant_id STRING,
    amount DECIMAL(12,2),
    currency STRING,
    transaction_type STRING,
    payment_method STRING,
    location_lat DOUBLE,
    location_lon DOUBLE,
    device_id STRING,
    ip_address STRING,
    transaction_timestamp TIMESTAMP,
    is_fraud BOOLEAN,
    fraud_score DOUBLE,
    PRIMARY KEY (transaction_id)
)
STORED AS KUDU;

-- User profile table
CREATE TABLE user_profiles (
    user_id STRING,
    avg_transaction_amount DECIMAL(12,2),
    transaction_count_30d INT,
    unique_merchants_30d INT,
    home_lat DOUBLE,
    home_lon DOUBLE,
    typical_transaction_hours STRING,
    risk_score DOUBLE,
    last_updated TIMESTAMP,
    PRIMARY KEY (user_id)
)
STORED AS KUDU;
```

**3. Real-time Fraud Detection Rules:**
```sql
-- High-risk transaction detection
CREATE VIEW high_risk_transactions AS
SELECT 
    t.transaction_id,
    t.user_id,
    t.amount,
    t.transaction_timestamp,
    CASE 
        WHEN t.amount > 5000 THEN 'HIGH_AMOUNT'
        WHEN t.amount > up.avg_transaction_amount * 10 THEN 'UNUSUAL_AMOUNT'
        WHEN SQRT(POW(t.location_lat - up.home_lat, 2) + POW(t.location_lon - up.home_lon, 2)) > 1.0 THEN 'DISTANT_LOCATION'
        WHEN HOUR(t.transaction_timestamp) NOT IN (9,10,11,12,13,14,15,16,17,18) THEN 'UNUSUAL_TIME'
        ELSE 'NORMAL'
    END as risk_factor,
    CASE 
        WHEN t.amount > 5000 THEN 0.8
        WHEN t.amount > up.avg_transaction_amount * 10 THEN 0.7
        WHEN SQRT(POW(t.location_lat - up.home_lat, 2) + POW(t.location_lon - up.home_lon, 2)) > 1.0 THEN 0.6
        WHEN HOUR(t.transaction_timestamp) NOT IN (9,10,11,12,13,14,15,16,17,18) THEN 0.4
        ELSE 0.1
    END as risk_score
FROM transactions t
JOIN user_profiles up ON t.user_id = up.user_id
WHERE t.transaction_timestamp >= NOW() - INTERVAL 1 HOUR;

-- Velocity-based fraud detection
CREATE VIEW velocity_fraud_check AS
SELECT 
    user_id,
    COUNT(*) as transaction_count_1h,
    SUM(amount) as total_amount_1h,
    COUNT(DISTINCT merchant_id) as unique_merchants_1h,
    COUNT(DISTINCT ip_address) as unique_ips_1h,
    MAX(amount) as max_amount_1h
FROM transactions
WHERE transaction_timestamp >= NOW() - INTERVAL 1 HOUR
GROUP BY user_id
HAVING COUNT(*) > 10 
    OR SUM(amount) > 10000 
    OR COUNT(DISTINCT ip_address) > 3;
```

**4. Real-time Alerting:**
```sql
-- Fraud alert view
CREATE VIEW fraud_alerts AS
SELECT 
    t.transaction_id,
    t.user_id,
    t.merchant_id,
    t.amount,
    t.transaction_timestamp,
    hrt.risk_factor,
    hrt.risk_score,
    vfc.transaction_count_1h,
    vfc.total_amount_1h,
    CASE 
        WHEN hrt.risk_score > 0.7 OR vfc.transaction_count_1h > 15 THEN 'CRITICAL'
        WHEN hrt.risk_score > 0.5 OR vfc.transaction_count_1h > 10 THEN 'HIGH'
        WHEN hrt.risk_score > 0.3 OR vfc.transaction_count_1h > 5 THEN 'MEDIUM'
        ELSE 'LOW'
    END as alert_level
FROM transactions t
JOIN high_risk_transactions hrt ON t.transaction_id = hrt.transaction_id
LEFT JOIN velocity_fraud_check vfc ON t.user_id = vfc.user_id
WHERE hrt.risk_score > 0.3 OR vfc.transaction_count_1h > 5;
```

**5. Fraud Analytics Dashboard:**
```sql
-- Fraud metrics dashboard
CREATE VIEW fraud_dashboard AS
SELECT 
    DATE_TRUNC('hour', transaction_timestamp) as hour,
    COUNT(*) as total_transactions,
    COUNT(CASE WHEN is_fraud = true THEN 1 END) as fraud_transactions,
    ROUND(100.0 * COUNT(CASE WHEN is_fraud = true THEN 1 END) / COUNT(*), 2) as fraud_rate,
    SUM(amount) as total_amount,
    SUM(CASE WHEN is_fraud = true THEN amount ELSE 0 END) as fraud_amount,
    AVG(fraud_score) as avg_fraud_score,
    COUNT(DISTINCT user_id) as unique_users
FROM transactions
WHERE transaction_timestamp >= NOW() - INTERVAL 24 HOURS
GROUP BY 1
ORDER BY 1 DESC;

-- Top fraud patterns
CREATE VIEW fraud_patterns AS
SELECT 
    payment_method,
    transaction_type,
    COUNT(*) as fraud_count,
    AVG(amount) as avg_fraud_amount,
    COUNT(DISTINCT user_id) as affected_users
FROM transactions
WHERE is_fraud = true
  AND transaction_timestamp >= NOW() - INTERVAL 7 DAYS
GROUP BY 1, 2
ORDER BY fraud_count DESC;
```

---

## 📚 Additional Resources

### Best Practices Summary
1. **Data Format**: Use Parquet for analytical workloads
2. **Partitioning**: Partition by commonly filtered columns
3. **Statistics**: Keep table and column statistics current
4. **Memory**: Configure appropriate memory limits and admission control
5. **Security**: Implement proper authentication and authorization

### Recommended Reading
- Apache Impala Official Documentation
- "Getting Started with Impala" by John Russell
- Cloudera Impala performance tuning guides

### Hands-on Practice
- Local Impala cluster setup
- BI tool integration
- Performance optimization exercises
- Real-time analytics implementations

---

*This comprehensive guide covers essential Apache Impala concepts for interactive SQL analytics and data engineering roles. Practice with large datasets and complex analytical queries to master Impala usage.*