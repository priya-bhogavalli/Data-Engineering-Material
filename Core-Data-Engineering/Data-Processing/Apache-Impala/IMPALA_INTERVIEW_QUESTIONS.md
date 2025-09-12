# Apache Impala Interview Questions for Data Engineering

## 📋 Table of Contents

1. [Basic Level Questions](#-basic-level-questions)
2. [Intermediate Level Questions](#-intermediate-level-questions)
3. [Advanced Level Questions](#-advanced-level-questions)
4. [Architecture & Performance](#-architecture--performance)
5. [Streaming & Real-time Processing](#-streaming--real-time-processing)
6. [Production & Operations](#-production--operations)
7. [Scenario-Based Questions](#-scenario-based-questions)

---

## 🟢 Basic Level Questions

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

### Q4: What data formats does Impala support?
**Answer:**
**Supported Data Formats:**

**1. Parquet (Recommended)**
```sql
CREATE TABLE parquet_table (
    id BIGINT,
    name STRING,
    amount DECIMAL(10,2)
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');
```
- Columnar storage format
- Excellent compression ratios
- Predicate pushdown support
- Schema evolution capabilities

**2. ORC (Optimized Row Columnar)**
```sql
CREATE TABLE orc_table (
    id BIGINT,
    data STRING
)
STORED AS ORC
TBLPROPERTIES ('orc.compress'='SNAPPY');
```
- Good for ACID transactions
- High compression ratios
- Built-in indexing

**3. Avro**
```sql
CREATE TABLE avro_table (
    id BIGINT,
    user_data STRING
)
STORED AS AVRO;
```
- Schema evolution support
- Cross-language compatibility
- Rich data types

**4. Text/CSV**
```sql
CREATE TABLE text_table (
    id INT,
    name STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```
- Human-readable format
- Easy data ingestion
- Legacy system compatibility

### Q5: How do you create and manage tables in Impala?
**Answer:**
**Table Creation Examples:**

**1. Basic Table Creation:**
```sql
CREATE TABLE employees (
    emp_id INT,
    name STRING,
    department STRING,
    salary DECIMAL(10,2),
    hire_date DATE
)
STORED AS PARQUET;
```

**2. Partitioned Table:**
```sql
CREATE TABLE sales (
    sale_id BIGINT,
    customer_id INT,
    product_id INT,
    sale_amount DECIMAL(10,2),
    sale_date DATE
)
PARTITIONED BY (year INT, month INT)
STORED AS PARQUET;
```

**3. External Table:**
```sql
CREATE EXTERNAL TABLE external_data (
    id INT,
    value STRING
)
LOCATION '/hdfs/path/to/data/'
STORED AS PARQUET;
```

**4. Table Management:**
```sql
-- Add partition
ALTER TABLE sales ADD PARTITION (year=2023, month=12);

-- Drop partition
ALTER TABLE sales DROP PARTITION (year=2022, month=1);

-- Add column
ALTER TABLE employees ADD COLUMNS (email STRING);

-- Compute statistics
COMPUTE STATS employees;
COMPUTE INCREMENTAL STATS sales;
```

### Q6: What are the basic SQL operations supported by Impala?
**Answer:**
**Core SQL Operations:**

**1. SELECT Operations:**
```sql
-- Basic SELECT
SELECT emp_id, name, salary
FROM employees
WHERE department = 'Engineering'
ORDER BY salary DESC
LIMIT 10;

-- Aggregations
SELECT 
    department,
    COUNT(*) as emp_count,
    AVG(salary) as avg_salary,
    MAX(salary) as max_salary
FROM employees
GROUP BY department
HAVING COUNT(*) > 5;
```

**2. JOIN Operations:**
```sql
-- Inner join
SELECT e.name, d.dept_name, e.salary
FROM employees e
JOIN departments d ON e.department_id = d.dept_id;

-- Left outer join
SELECT c.customer_name, o.order_total
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
```

**3. Window Functions:**
```sql
SELECT 
    emp_id,
    name,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rank,
    AVG(salary) OVER (PARTITION BY department) as dept_avg_salary
FROM employees;
```

**4. Subqueries:**
```sql
-- Correlated subquery
SELECT name, salary
FROM employees e1
WHERE salary > (
    SELECT AVG(salary)
    FROM employees e2
    WHERE e2.department = e1.department
);
```

### Q7: How do you connect to Impala from different clients?
**Answer:**
**Connection Methods:**

**1. Impala Shell:**
```bash
# Connect to Impala shell
impala-shell -i impala-server:21000

# Connect with specific database
impala-shell -i impala-server:21000 -d my_database

# Execute query from command line
impala-shell -i impala-server:21000 -q "SELECT COUNT(*) FROM employees;"
```

**2. JDBC Connection:**
```java
// Java JDBC connection
String jdbcUrl = "jdbc:impala://impala-server:21050/default";
Connection conn = DriverManager.getConnection(jdbcUrl);
PreparedStatement stmt = conn.prepareStatement("SELECT * FROM employees WHERE dept = ?");
stmt.setString(1, "Engineering");
ResultSet rs = stmt.executeQuery();
```

**3. Python Connection:**
```python
# Using impyla library
from impala.dbapi import connect

conn = connect(host='impala-server', port=21050)
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM employees')
result = cursor.fetchone()
print(f"Employee count: {result[0]}")
```

**4. ODBC Connection:**
```python
# Using pyodbc
import pyodbc

conn_str = "DRIVER={Cloudera ODBC Driver for Impala};HOST=impala-server;PORT=21050"
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
cursor.execute("SELECT * FROM employees LIMIT 10")
rows = cursor.fetchall()
```

### Q8: What is the role of the Hive Metastore in Impala?
**Answer:**
**Hive Metastore Integration:**

**1. Metadata Storage:**
- Table schemas and definitions
- Partition information
- Column metadata and types
- Storage location details
- Table properties and statistics

**2. Shared Metadata:**
```sql
-- Tables created in Hive are accessible in Impala
-- (after REFRESH or INVALIDATE METADATA)

-- In Hive:
CREATE TABLE hive_table (id INT, name STRING) STORED AS PARQUET;

-- In Impala (after refresh):
REFRESH hive_table;
SELECT * FROM hive_table;
```

**3. Metadata Synchronization:**
```sql
-- Refresh specific table metadata
REFRESH table_name;

-- Invalidate all metadata (forces reload)
INVALIDATE METADATA;

-- Invalidate specific table
INVALIDATE METADATA table_name;
```

**4. Benefits:**
- Consistent metadata across Hadoop ecosystem
- Shared table definitions between Hive and Impala
- Centralized schema management
- Support for external tools and applications

### Q9: How do you handle data types in Impala?
**Answer:**
**Impala Data Types:**

**1. Numeric Types:**
```sql
CREATE TABLE numeric_example (
    tiny_col TINYINT,      -- 1 byte: -128 to 127
    small_col SMALLINT,    -- 2 bytes: -32,768 to 32,767
    int_col INT,           -- 4 bytes: -2^31 to 2^31-1
    big_col BIGINT,        -- 8 bytes: -2^63 to 2^63-1
    float_col FLOAT,       -- 4 bytes: single precision
    double_col DOUBLE,     -- 8 bytes: double precision
    decimal_col DECIMAL(10,2)  -- Exact decimal: precision, scale
);
```

**2. String Types:**
```sql
CREATE TABLE string_example (
    char_col CHAR(10),     -- Fixed-length string
    varchar_col VARCHAR(50), -- Variable-length string with limit
    string_col STRING      -- Variable-length string (unlimited)
);
```

**3. Date/Time Types:**
```sql
CREATE TABLE datetime_example (
    date_col DATE,         -- Date only: YYYY-MM-DD
    timestamp_col TIMESTAMP -- Date and time: YYYY-MM-DD HH:MM:SS
);

-- Date/time functions
SELECT 
    CURRENT_DATE() as today,
    CURRENT_TIMESTAMP() as now,
    YEAR(date_col) as year,
    MONTH(date_col) as month,
    DAY(date_col) as day
FROM datetime_example;
```

**4. Boolean Type:**
```sql
CREATE TABLE boolean_example (
    is_active BOOLEAN      -- TRUE or FALSE
);

SELECT * FROM boolean_example WHERE is_active = TRUE;
```

### Q10: What are the basic performance considerations in Impala?
**Answer:**
**Key Performance Factors:**

**1. Data Format Selection:**
```sql
-- Use Parquet for analytical workloads
CREATE TABLE optimized_table (
    id BIGINT,
    data STRING,
    amount DECIMAL(10,2)
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');
```

**2. Partitioning Strategy:**
```sql
-- Partition by commonly filtered columns
CREATE TABLE sales_partitioned (
    sale_id BIGINT,
    customer_id INT,
    sale_amount DECIMAL(10,2)
)
PARTITIONED BY (year INT, month INT)
STORED AS PARQUET;

-- Query with partition pruning
SELECT * FROM sales_partitioned 
WHERE year = 2023 AND month = 12;
```

**3. Statistics Management:**
```sql
-- Compute table statistics for optimization
COMPUTE STATS sales_table;

-- Compute incremental statistics for partitioned tables
COMPUTE INCREMENTAL STATS partitioned_table;

-- Check statistics
SHOW TABLE STATS sales_table;
SHOW COLUMN STATS sales_table;
```

**4. Memory Configuration:**
```bash
# Configure memory limits
--mem_limit=8GB
--buffer_pool_limit=6GB
--scratch_dirs=/tmp/impala-scratch
```

**5. Query Optimization:**
```sql
-- Use appropriate query hints
SELECT /*+ BROADCAST(small_table) */
    l.large_column,
    s.small_column
FROM large_table l
JOIN small_table s ON l.id = s.id;

-- Set query-specific limits
SET MEM_LIMIT=2GB;
SET QUERY_TIMEOUT_S=300;
```

---

## 🟡 Intermediate Level Questions

### Q11: Explain Impala's query execution architecture in detail
**Answer:**
**Impala Query Execution Flow:**

**1. Query Planning Phase:**
```sql
-- Example complex query
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
- Metadata retrieval from Catalog Service

**b) Query Planning:**
- Cost-based optimization using table statistics
- Join order optimization
- Predicate pushdown to storage layer
- Partition pruning for partitioned tables

**c) Fragment Generation:**
- Break query into executable fragments
- Assign fragments to appropriate nodes
- Create distributed execution tree
- Determine data exchange requirements

**d) Distributed Execution:**
- Parallel fragment execution across nodes
- Data exchange between nodes using network
- Intermediate result aggregation
- Final result collection at coordinator

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

### Q12: How does Impala handle memory management and what happens when memory is exhausted?
**Answer:**
**Impala Memory Management:**

**1. Memory Architecture:**
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

# When memory is exhausted:
# - Hash joins spill to disk
# - Sort operations use external sort
# - Aggregations spill intermediate results
```

**c) Memory Monitoring:**
```sql
-- Query memory usage
SHOW QUERY STATS;

-- Profile memory usage
PROFILE;

-- Check current memory usage
SELECT 
    query_id,
    memory_aggregate_peak,
    memory_per_node_peak
FROM sys.impala_query_log
WHERE start_time > NOW() - INTERVAL 1 HOUR;
```

### Q13: What are the different types of joins in Impala and how are they optimized?
**Answer:**
**Impala Join Types and Optimization:**

**1. Join Algorithms:**

**a) Broadcast Join:**
```sql
-- Small table broadcasted to all nodes
SELECT /*+ BROADCAST(d) */
    f.fact_column,
    d.dimension_column
FROM fact_table f
JOIN dimension_table d ON f.dim_id = d.dim_id;

-- Automatic broadcast for small tables (< broadcast_bytes_limit)
-- Default: 34MB
```

**b) Partitioned Hash Join:**
```sql
-- Large tables partitioned and shuffled
SELECT /*+ SHUFFLE(t1) */
    t1.column1,
    t2.column2
FROM large_table1 t1
JOIN large_table2 t2 ON t1.id = t2.id;

-- Used when both tables are large
-- Data shuffled across network based on join keys
```

**2. Join Types:**
```sql
-- Inner join
SELECT c.name, o.total
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id;

-- Left outer join
SELECT c.name, COALESCE(o.total, 0) as total
FROM customers c
LEFT OUTER JOIN orders o ON c.id = o.customer_id;

-- Right outer join
SELECT c.name, o.total
FROM customers c
RIGHT OUTER JOIN orders o ON c.id = o.customer_id;

-- Full outer join
SELECT COALESCE(c.name, 'Unknown') as name, o.total
FROM customers c
FULL OUTER JOIN orders o ON c.id = o.customer_id;

-- Semi join (EXISTS equivalent)
SELECT c.name
FROM customers c
LEFT SEMI JOIN orders o ON c.id = o.customer_id;

-- Anti join (NOT EXISTS equivalent)
SELECT c.name
FROM customers c
LEFT ANTI JOIN orders o ON c.id = o.customer_id;
```

**3. Join Optimization Techniques:**
```sql
-- Join order optimization
SELECT /*+ STRAIGHT_JOIN */
    t1.col1, t2.col2, t3.col3
FROM small_table t1
JOIN medium_table t2 ON t1.id = t2.id
JOIN large_table t3 ON t2.id = t3.id;

-- Runtime filter optimization
-- Automatically applied to reduce data scanned
SELECT f.*, d.category
FROM fact_sales f
JOIN dim_product d ON f.product_id = d.product_id
WHERE d.category = 'Electronics';
```

### Q14: How do you optimize Impala queries for better performance?
**Answer:**
**Impala Query Optimization Techniques:**

**1. Table Statistics:**
```sql
-- Compute table statistics
COMPUTE STATS customers;
COMPUTE STATS orders;

-- Compute incremental statistics for partitioned tables
COMPUTE INCREMENTAL STATS partitioned_table;

-- Show table statistics
SHOW TABLE STATS customers;
SHOW COLUMN STATS customers;

-- Statistics help with:
-- - Join order optimization
-- - Memory estimation
-- - Cardinality estimation
-- - Cost-based optimization
```

**2. Partitioning Optimization:**
```sql
-- Create well-partitioned table
CREATE TABLE sales_optimized (
    sale_id BIGINT,
    customer_id INT,
    product_id INT,
    sale_amount DECIMAL(10,2),
    sale_date DATE
)
PARTITIONED BY (year INT, month INT, day INT)
STORED AS PARQUET;

-- Query with partition pruning
SELECT * FROM sales_optimized 
WHERE year = 2023 AND month = 12;

-- Avoid over-partitioning (keep partitions > 256MB)
-- Typical partition sizes: 256MB - 1GB
```

**3. Join Optimization:**
```sql
-- Use broadcast joins for small dimension tables
SELECT /*+ BROADCAST(d) */
    f.fact_column,
    d.dimension_column
FROM fact_table f
JOIN dimension_table d ON f.dim_id = d.dim_id;

-- Use shuffle joins for large tables
SELECT /*+ SHUFFLE(large_table1) */
    t1.column1,
    t2.column2
FROM large_table1 t1
JOIN large_table2 t2 ON t1.id = t2.id;

-- Optimize join order (smallest table first)
SELECT t1.col1, t2.col2, t3.col3
FROM small_table t1
JOIN medium_table t2 ON t1.id = t2.id
JOIN large_table t3 ON t2.id = t3.id;
```

**4. Query Hints and Settings:**
```sql
-- Memory limit hint
SELECT /*+ MEM_LIMIT(2GB) */ * FROM large_table;

-- Straight join hint (preserve join order)
SELECT /*+ STRAIGHT_JOIN */
    t1.col1, t2.col2, t3.col3
FROM table1 t1
JOIN table2 t2 ON t1.id = t2.id
JOIN table3 t3 ON t2.id = t3.id;

-- Query-specific settings
SET QUERY_TIMEOUT_S=300;
SET MEM_LIMIT=4GB;
SET DISABLE_CODEGEN=false;
SET BATCH_SIZE=1024;
```

**5. Data Format Optimization:**
```sql
-- Use Parquet with appropriate compression
CREATE TABLE optimized_parquet (
    id BIGINT,
    data STRING,
    amount DECIMAL(10,2)
)
STORED AS PARQUET
TBLPROPERTIES (
    'parquet.compression'='SNAPPY',
    'parquet.block.size'='268435456'  -- 256MB
);

-- Convert existing tables to Parquet
CREATE TABLE new_parquet_table
STORED AS PARQUET
AS SELECT * FROM old_text_table;
```

### Q15: How do you handle complex analytical queries in Impala?
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

**4. Advanced Window Functions:**
```sql
-- Sales performance analysis with multiple window functions
SELECT 
    sales_rep,
    sale_date,
    sale_amount,
    -- Running total
    SUM(sale_amount) OVER (
        PARTITION BY sales_rep 
        ORDER BY sale_date 
        ROWS UNBOUNDED PRECEDING
    ) as running_total,
    -- Moving average (30 days)
    AVG(sale_amount) OVER (
        PARTITION BY sales_rep 
        ORDER BY sale_date 
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as moving_avg_30d,
    -- Rank within month
    RANK() OVER (
        PARTITION BY sales_rep, YEAR(sale_date), MONTH(sale_date)
        ORDER BY sale_amount DESC
    ) as monthly_rank,
    -- Percentage of total
    ROUND(100.0 * sale_amount / SUM(sale_amount) OVER (
        PARTITION BY YEAR(sale_date), MONTH(sale_date)
    ), 2) as pct_of_monthly_total
FROM sales
WHERE sale_date >= '2023-01-01'
ORDER BY sales_rep, sale_date;
```

---

*This is the first batch of questions. I'll continue with more batches to complete the comprehensive interview questions file.*

---

## 📚 Additional Comprehensive Content

*(Merged from comprehensive interview questions file)*

