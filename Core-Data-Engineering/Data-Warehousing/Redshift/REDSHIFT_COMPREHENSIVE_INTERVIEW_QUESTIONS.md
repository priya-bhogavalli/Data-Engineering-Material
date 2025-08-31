# 🔴 Amazon Redshift - Comprehensive Interview Questions & Answers

## 📋 Table of Contents
1. [Fundamentals (Questions 1-15)](#fundamentals)
2. [Architecture & Performance (Questions 16-30)](#architecture--performance)
3. [Data Loading & ETL (Questions 31-45)](#data-loading--etl)
4. [Query Optimization (Questions 46-60)](#query-optimization)
5. [Administration & Operations (Questions 61-75)](#administration--operations)

---

## 🔰 Fundamentals

### 1. What is Amazon Redshift and what problems does it solve?
**Answer:** Amazon Redshift is a fully managed, petabyte-scale data warehouse service in the cloud that solves:
- **Scalability**: Handle massive datasets (petabytes)
- **Performance**: Fast analytical queries using columnar storage
- **Cost-effectiveness**: Pay-as-you-use pricing model
- **Integration**: Native AWS ecosystem integration
- **Maintenance**: Fully managed service with automated backups

### 2. Explain Redshift's architecture components
**Answer:**
- **Leader Node**: Coordinates query execution and client connections
- **Compute Nodes**: Execute queries and store data
- **Node Slices**: Parallel processing units within compute nodes
- **Columnar Storage**: Data stored in columns for analytical workloads
- **Massively Parallel Processing (MPP)**: Distributed query execution

### 3. What are the different Redshift node types?
**Answer:**
| Node Type | Use Case | Storage | Memory | vCPUs |
|-----------|----------|---------|--------|-------|
| **ra3.xlplus** | Balanced workloads | Managed Storage | 32 GB | 4 |
| **ra3.4xlarge** | Heavy workloads | Managed Storage | 96 GB | 12 |
| **ra3.16xlarge** | Largest workloads | Managed Storage | 384 GB | 48 |
| **dc2.large** | Small datasets | 160 GB SSD | 15 GB | 2 |
| **dc2.8xlarge** | Large datasets | 2.56 TB SSD | 244 GB | 32 |

### 4. How does Redshift's columnar storage work?
**Answer:**
```sql
-- Traditional row storage
Row 1: [ID=1, Name='John', Age=25, Salary=50000]
Row 2: [ID=2, Name='Jane', Age=30, Salary=60000]

-- Columnar storage
ID Column: [1, 2, 3, ...]
Name Column: ['John', 'Jane', 'Bob', ...]
Age Column: [25, 30, 35, ...]
Salary Column: [50000, 60000, 70000, ...]
```
**Benefits:**
- Better compression ratios
- Faster analytical queries
- I/O reduction for column-specific queries
- Efficient aggregations

### 5. What are distribution keys and styles in Redshift?
**Answer:**
```sql
-- EVEN distribution (default)
CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    order_date DATE
) DISTSTYLE EVEN;

-- KEY distribution
CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    order_date DATE
) DISTKEY(customer_id);

-- ALL distribution
CREATE TABLE small_lookup (
    category_id INT,
    category_name VARCHAR(50)
) DISTSTYLE ALL;
```

### 6. Explain Redshift sort keys
**Answer:**
```sql
-- Compound sort key (default)
CREATE TABLE sales (
    sale_date DATE,
    product_id INT,
    customer_id INT,
    amount DECIMAL(10,2)
) SORTKEY(sale_date, product_id);

-- Interleaved sort key
CREATE TABLE sales (
    sale_date DATE,
    product_id INT,
    customer_id INT,
    amount DECIMAL(10,2)
) INTERLEAVED SORTKEY(sale_date, product_id, customer_id);
```

### 7. What is Redshift Spectrum?
**Answer:** Redshift Spectrum allows querying data in S3 without loading it into Redshift:
```sql
-- Create external schema
CREATE EXTERNAL SCHEMA spectrum_schema
FROM DATA CATALOG
DATABASE 'spectrum_db'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftSpectrumRole';

-- Query S3 data
SELECT *
FROM spectrum_schema.s3_table
WHERE year = 2023;
```

### 8. How does Redshift handle data compression?
**Answer:**
```sql
-- Automatic compression
CREATE TABLE test_table (
    id INT ENCODE DELTA,
    name VARCHAR(100) ENCODE LZO,
    date_col DATE ENCODE DELTA32K,
    amount DECIMAL(10,2) ENCODE AZ64
);

-- Analyze compression
ANALYZE COMPRESSION test_table;
```
**Compression types:**
- **AZ64**: General purpose
- **LZO**: Text data
- **DELTA**: Numeric sequences
- **RUNLENGTH**: Repeated values

### 9. What are Redshift workload management (WLM) queues?
**Answer:**
```json
{
  "query_group": "etl_queue",
  "memory_percent_to_use": 40,
  "max_execution_time": 3600,
  "user_group": ["etl_users"],
  "query_concurrency": 5
}
```
- **Automatic WLM**: Machine learning-based queue management
- **Manual WLM**: Custom queue configuration
- **Query monitoring rules**: Automatic query termination

### 10. Explain Redshift's VACUUM operation
**Answer:**
```sql
-- Full vacuum (reclaims space and sorts)
VACUUM table_name;

-- Delete only vacuum (reclaims space)
VACUUM DELETE ONLY table_name;

-- Sort only vacuum (sorts data)
VACUUM SORT ONLY table_name;

-- Reindex vacuum (rebuilds interleaved sort keys)
VACUUM REINDEX table_name;
```

### 11. What is Redshift's ANALYZE command?
**Answer:**
```sql
-- Analyze entire table
ANALYZE table_name;

-- Analyze specific columns
ANALYZE table_name (column1, column2);

-- Analyze with threshold
ANALYZE table_name PREDICATE COLUMNS;

-- Check table statistics
SELECT * FROM pg_stats WHERE tablename = 'table_name';
```

### 12. How does Redshift handle transactions?
**Answer:**
- **ACID compliance**: Atomic, Consistent, Isolated, Durable
- **Serializable isolation**: Highest isolation level
- **Automatic commit**: DDL statements auto-commit
- **Manual transactions**: BEGIN/COMMIT/ROLLBACK

```sql
BEGIN;
INSERT INTO orders VALUES (1, 'Product A', 100);
UPDATE inventory SET quantity = quantity - 1 WHERE product = 'Product A';
COMMIT;
```

### 13. What are Redshift system tables and views?
**Answer:**
```sql
-- Query performance monitoring
SELECT * FROM stl_query WHERE userid = 100;

-- Table information
SELECT * FROM pg_table_def WHERE tablename = 'orders';

-- Current running queries
SELECT * FROM stv_recents WHERE status = 'Running';

-- Disk usage
SELECT * FROM stv_tbl_perm WHERE name = 'orders';
```

### 14. Explain Redshift's backup and restore capabilities
**Answer:**
- **Automated snapshots**: Daily backups with 1-day retention (default)
- **Manual snapshots**: User-initiated backups
- **Cross-region snapshots**: Disaster recovery
- **Point-in-time recovery**: Restore to specific timestamp

```sql
-- Create manual snapshot
CREATE SNAPSHOT my_snapshot FROM CLUSTER my_cluster;

-- Restore from snapshot
RESTORE CLUSTER new_cluster FROM SNAPSHOT my_snapshot;
```

### 15. What is Redshift Serverless?
**Answer:**
- **No cluster management**: Automatic scaling
- **Pay-per-use**: Charged for actual usage
- **Automatic scaling**: Scales up/down based on workload
- **Namespace and workgroup**: Logical separation of resources

---

## 🏗️ Architecture & Performance

### 16. How does Redshift's MPP architecture work?
**Answer:**
```
Leader Node
├── SQL Endpoint
├── Query Planner
├── Query Coordinator
└── Result Aggregator

Compute Nodes (1-128)
├── Node 1
│   ├── Slice 1 (CPU + Memory + Disk)
│   └── Slice 2 (CPU + Memory + Disk)
├── Node 2
│   ├── Slice 1
│   └── Slice 2
└── ...
```

### 17. What factors affect Redshift query performance?
**Answer:**
- **Distribution key**: Minimizes data movement
- **Sort key**: Enables zone maps and efficient scans
- **Compression**: Reduces I/O
- **Statistics**: Enables optimal query plans
- **WLM configuration**: Manages resource allocation
- **Data skew**: Uneven data distribution

### 18. How do you optimize table design for performance?
**Answer:**
```sql
-- Optimal table design
CREATE TABLE fact_sales (
    sale_date DATE SORTKEY,           -- Most selective filter
    product_id INT,
    customer_id INT DISTKEY,          -- Join key for distribution
    store_id INT,
    quantity INT ENCODE DELTA,
    amount DECIMAL(10,2) ENCODE AZ64
) 
COMPOUND SORTKEY (sale_date, product_id)
DISTSTYLE KEY;

-- Avoid
CREATE TABLE bad_design (
    id INT IDENTITY(1,1),             -- IDENTITY as DISTKEY causes skew
    data VARCHAR(MAX)                 -- No compression
) DISTSTYLE EVEN;                     -- Poor for joins
```

### 19. Explain Redshift's query execution process
**Answer:**
1. **Parse**: SQL parsing and syntax validation
2. **Plan**: Query optimizer creates execution plan
3. **Compile**: Generate executable code
4. **Execute**: Distribute to compute nodes
5. **Aggregate**: Collect results at leader node
6. **Return**: Send results to client

### 20. How do you monitor Redshift performance?
**Answer:**
```sql
-- Query performance
SELECT 
    query,
    starttime,
    endtime,
    datediff(seconds, starttime, endtime) as duration,
    aborted
FROM stl_query 
WHERE starttime >= CURRENT_DATE - 1
ORDER BY duration DESC;

-- Table scan statistics
SELECT 
    schema,
    table,
    size,
    pct_used,
    empty,
    unsorted,
    stats_off
FROM svv_table_info
ORDER BY size DESC;

-- Disk usage by table
SELECT 
    name,
    sum(rows) as rows,
    sum(size) as size_mb
FROM stv_tbl_perm
GROUP BY name
ORDER BY size_mb DESC;
```

### 21. What causes data skew in Redshift?
**Answer:**
```sql
-- Check distribution skew
SELECT 
    slice,
    COUNT(*) as row_count
FROM stv_slices s
JOIN stv_tbl_perm t ON s.slice = t.slice
WHERE t.name = 'orders'
GROUP BY slice
ORDER BY row_count DESC;

-- Causes of skew:
-- 1. Poor distribution key choice
-- 2. NULL values in distribution key
-- 3. Hot keys (few values with many rows)
-- 4. IDENTITY columns as distribution keys
```

### 22. How do you handle large table joins efficiently?
**Answer:**
```sql
-- Co-located join (same distribution key)
CREATE TABLE orders (
    order_id INT,
    customer_id INT DISTKEY
) DISTSTYLE KEY;

CREATE TABLE customers (
    customer_id INT DISTKEY,
    customer_name VARCHAR(100)
) DISTSTYLE KEY;

-- Efficient join (no data movement)
SELECT o.order_id, c.customer_name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;

-- Broadcast join (small dimension table)
CREATE TABLE product_categories (
    category_id INT,
    category_name VARCHAR(50)
) DISTSTYLE ALL;
```

### 23. What are Redshift's concurrency and scaling limits?
**Answer:**
- **Query concurrency**: Up to 50 concurrent queries (WLM dependent)
- **Connections**: Up to 500 concurrent connections
- **Cluster size**: 1-128 compute nodes
- **Database size**: Petabyte scale
- **Table limit**: No hard limit
- **Column limit**: 1,600 columns per table

### 24. How does Redshift handle memory management?
**Answer:**
```sql
-- Memory allocation per query queue
-- Total cluster memory divided among:
-- 1. System processes (reserved)
-- 2. WLM queues (configurable)
-- 3. Each queue divided among concurrent queries

-- Check memory usage
SELECT 
    query,
    max_rows_in_memory,
    rows_pre_filter,
    rows_pre_user_filter
FROM stl_query_metrics
WHERE query = 12345;
```

### 25. What is Redshift's approach to high availability?
**Answer:**
- **Multi-AZ deployment**: Automatic failover
- **Node failure recovery**: Automatic node replacement
- **Snapshot backups**: Point-in-time recovery
- **Cross-region replication**: Disaster recovery
- **Cluster resize**: Online scaling operations

### 26. How do you optimize Redshift for mixed workloads?
**Answer:**
```sql
-- Separate WLM queues for different workloads
{
  "query_groups": [
    {
      "name": "etl_queue",
      "memory_percent": 50,
      "max_execution_time": 7200,
      "query_concurrency": 2
    },
    {
      "name": "reporting_queue", 
      "memory_percent": 30,
      "max_execution_time": 300,
      "query_concurrency": 10
    },
    {
      "name": "adhoc_queue",
      "memory_percent": 20,
      "max_execution_time": 600,
      "query_concurrency": 5
    }
  ]
}
```

### 27. What are Redshift's storage optimization features?
**Answer:**
- **Automatic compression**: Analyzes and applies optimal encoding
- **Zone maps**: Skip irrelevant data blocks
- **Columnar storage**: Store only needed columns
- **Data lifecycle management**: Automated archival to S3
- **Managed storage**: Automatic scaling (RA3 nodes)

### 28. How do you handle time-series data in Redshift?
**Answer:**
```sql
-- Optimal design for time-series
CREATE TABLE sensor_data (
    timestamp TIMESTAMP SORTKEY,     -- Primary filter
    sensor_id INT DISTKEY,           -- Even distribution
    location VARCHAR(50),
    temperature DECIMAL(5,2) ENCODE AZ64,
    humidity DECIMAL(5,2) ENCODE AZ64
)
COMPOUND SORTKEY (timestamp, sensor_id);

-- Partition-like queries using date ranges
SELECT sensor_id, AVG(temperature)
FROM sensor_data
WHERE timestamp BETWEEN '2023-01-01' AND '2023-01-31'
GROUP BY sensor_id;
```

### 29. What are Redshift's networking and security features?
**Answer:**
- **VPC deployment**: Private network isolation
- **Security groups**: Network-level access control
- **Encryption**: At-rest and in-transit encryption
- **IAM integration**: AWS identity management
- **Database users**: Internal user management
- **SSL connections**: Encrypted client connections

### 30. How do you implement disaster recovery for Redshift?
**Answer:**
```sql
-- Cross-region snapshot copy
COPY SNAPSHOT source_snapshot_id
TO REGION 'us-west-2'
WITH SNAPSHOT_COPY_GRANT 'my-grant';

-- Automated snapshot schedule
{
  "ScheduleIdentifier": "daily-backup",
  "ScheduleDefinition": "rate(24 hours)",
  "TargetAction": {
    "CreateClusterSnapshot": {
      "SnapshotIdentifier": "daily-snapshot-{timestamp}"
    }
  }
}
```

---

## 📥 Data Loading & ETL

### 31. What are the different ways to load data into Redshift?
**Answer:**
- **COPY command**: Bulk loading from S3, EMR, DynamoDB
- **INSERT statements**: Row-by-row insertion
- **AWS Data Pipeline**: Managed ETL service
- **AWS Glue**: Serverless ETL service
- **Third-party tools**: Informatica, Talend, etc.

### 32. How do you optimize COPY command performance?
**Answer:**
```sql
-- Optimal COPY command
COPY orders
FROM 's3://my-bucket/orders/'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftRole'
FORMAT AS PARQUET
COMPUPDATE ON
STATUPDATE ON
MAXERROR 100
PARALLEL ON;

-- Best practices:
-- 1. Use multiple files (1-125MB each)
-- 2. Compress files (GZIP, BZIP2)
-- 3. Use columnar formats (Parquet, ORC)
-- 4. Enable parallel loading
-- 5. Use appropriate file splitting
```

### 33. How do you handle data quality during loading?
**Answer:**
```sql
-- Data validation during COPY
COPY orders
FROM 's3://my-bucket/orders.csv'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftRole'
CSV
MAXERROR 10                    -- Allow up to 10 errors
ACCEPTINVCHARS AS '?'          -- Replace invalid chars
DATEFORMAT 'YYYY-MM-DD'       -- Specify date format
TIMEFORMAT 'HH:MI:SS'         -- Specify time format
TRUNCATECOLUMNS;               -- Truncate oversized strings

-- Check load errors
SELECT * FROM stl_load_errors WHERE query = pg_last_copy_id();
```

### 34. What are Redshift's data format support options?
**Answer:**
```sql
-- CSV format
COPY table_name FROM 's3://bucket/file.csv'
CSV DELIMITER ',' QUOTE '"' ESCAPE;

-- JSON format
COPY table_name FROM 's3://bucket/file.json'
JSON 'auto' GZIP;

-- Parquet format
COPY table_name FROM 's3://bucket/file.parquet'
FORMAT AS PARQUET;

-- Avro format
COPY table_name FROM 's3://bucket/file.avro'
FORMAT AS AVRO 's3://bucket/schema.avsc';

-- Fixed-width format
COPY table_name FROM 's3://bucket/file.txt'
FIXEDWIDTH 'column1:10,column2:20,column3:15';
```

### 35. How do you implement incremental data loading?
**Answer:**
```sql
-- Method 1: Merge using staging table
CREATE TEMP TABLE staging_orders (LIKE orders);

COPY staging_orders FROM 's3://bucket/new_orders.csv' CSV;

-- Upsert logic
DELETE FROM orders 
WHERE order_id IN (SELECT order_id FROM staging_orders);

INSERT INTO orders 
SELECT * FROM staging_orders;

-- Method 2: Using timestamps
COPY orders FROM 's3://bucket/orders_2023_01_15.csv'
CSV
WHERE last_modified > (SELECT MAX(last_modified) FROM orders);
```

### 36. How do you handle large file loading efficiently?
**Answer:**
```sql
-- Split large files into optimal sizes
-- Optimal: 1MB - 125MB per file
-- Use manifest file for multiple files

-- manifest.json
{
  "entries": [
    {"url": "s3://bucket/part1.csv", "mandatory": true},
    {"url": "s3://bucket/part2.csv", "mandatory": true},
    {"url": "s3://bucket/part3.csv", "mandatory": true}
  ]
}

COPY orders FROM 's3://bucket/manifest.json'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftRole'
CSV MANIFEST;
```

### 37. What are UNLOAD command best practices?
**Answer:**
```sql
-- Efficient UNLOAD
UNLOAD ('SELECT * FROM orders WHERE order_date >= ''2023-01-01''')
TO 's3://my-bucket/orders_export/'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftRole'
FORMAT AS PARQUET
PARTITION BY (order_date)
MAXFILESIZE 100 MB
PARALLEL ON
CLEANPATH;

-- Export with compression
UNLOAD ('SELECT * FROM large_table')
TO 's3://my-bucket/export/'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftRole'
GZIP
ALLOWOVERWRITE;
```

### 38. How do you implement CDC (Change Data Capture)?
**Answer:**
```sql
-- Using timestamps for CDC
CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    order_date DATE,
    created_at TIMESTAMP DEFAULT GETDATE(),
    updated_at TIMESTAMP DEFAULT GETDATE()
);

-- CDC query
SELECT * FROM orders 
WHERE updated_at > '2023-01-15 10:00:00'
AND updated_at <= '2023-01-15 11:00:00';

-- Using AWS DMS for CDC
-- Configure DMS task to capture changes from source
-- Load changes incrementally to Redshift
```

### 39. How do you handle data type conversions during loading?
**Answer:**
```sql
-- Automatic conversions
COPY orders (
    order_id,
    order_date,
    amount
) FROM 's3://bucket/orders.csv'
CSV
DATEFORMAT 'MM/DD/YYYY'        -- Convert date format
TIMEFORMAT 'HH12:MI:SS AM'     -- Convert time format
ACCEPTINVCHARS AS '?'          -- Handle invalid characters
BLANKSASNULL                   -- Convert blanks to NULL
EMPTYASNULL;                   -- Convert empty strings to NULL

-- Manual conversions in staging
CREATE TEMP TABLE staging AS
SELECT 
    order_id::INT,
    TO_DATE(order_date_str, 'MM/DD/YYYY') as order_date,
    amount::DECIMAL(10,2)
FROM raw_staging;
```

### 40. What are the limitations of COPY command?
**Answer:**
- **File size**: Individual files should be 1MB-125MB
- **Concurrent COPY**: Limited by WLM queue slots
- **Data types**: Some complex types not supported
- **Error handling**: Limited error recovery options
- **Transaction size**: Large transactions can cause issues
- **Network dependency**: Requires stable S3 connectivity

### 41. How do you implement data archival strategies?
**Answer:**
```sql
-- Time-based archival
-- 1. Create archive table
CREATE TABLE orders_archive (LIKE orders);

-- 2. Move old data
INSERT INTO orders_archive
SELECT * FROM orders 
WHERE order_date < CURRENT_DATE - INTERVAL '2 years';

-- 3. Delete from main table
DELETE FROM orders 
WHERE order_date < CURRENT_DATE - INTERVAL '2 years';

-- 4. UNLOAD to S3 for long-term storage
UNLOAD ('SELECT * FROM orders_archive')
TO 's3://archive-bucket/orders/year=2021/'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftRole'
FORMAT AS PARQUET
PARTITION BY (EXTRACT(year FROM order_date));
```

### 42. How do you handle schema evolution during ETL?
**Answer:**
```sql
-- Add columns safely
ALTER TABLE orders ADD COLUMN new_field VARCHAR(100) DEFAULT 'N/A';

-- Handle missing columns in COPY
COPY orders (order_id, customer_id, order_date)  -- Specify columns
FROM 's3://bucket/old_format.csv'
CSV;

-- Use staging table for complex transformations
CREATE TEMP TABLE staging_new_format AS
SELECT 
    order_id,
    customer_id,
    order_date,
    CASE 
        WHEN payment_method IS NULL THEN 'UNKNOWN'
        ELSE payment_method 
    END as payment_method
FROM staging_raw;
```

### 43. What are streaming data loading options for Redshift?
**Answer:**
- **Kinesis Data Firehose**: Direct streaming to Redshift
- **Kinesis Analytics**: Real-time processing before loading
- **AWS Lambda**: Micro-batch processing
- **Redshift Streaming Ingestion**: Direct from Kinesis (preview)

```sql
-- Kinesis Data Firehose configuration
{
  "DeliveryStreamName": "redshift-stream",
  "RedshiftDestinationConfiguration": {
    "ClusterJDBCURL": "jdbc:redshift://cluster.region.redshift.amazonaws.com:5439/db",
    "CopyCommand": {
      "DataTableName": "streaming_data",
      "CopyOptions": "CSV GZIP"
    },
    "S3Configuration": {
      "BucketARN": "arn:aws:s3:::my-bucket",
      "BufferingHints": {
        "SizeInMBs": 64,
        "IntervalInSeconds": 300
      }
    }
  }
}
```

### 44. How do you implement data lineage tracking?
**Answer:**
```sql
-- Create metadata tables
CREATE TABLE data_lineage (
    job_id VARCHAR(100),
    source_table VARCHAR(100),
    target_table VARCHAR(100),
    transformation_logic TEXT,
    execution_time TIMESTAMP,
    record_count BIGINT
);

-- Log ETL operations
INSERT INTO data_lineage VALUES (
    'daily_etl_001',
    'raw_orders',
    'fact_orders',
    'Aggregation and cleansing',
    GETDATE(),
    (SELECT COUNT(*) FROM fact_orders WHERE load_date = CURRENT_DATE)
);

-- Query lineage
SELECT * FROM data_lineage 
WHERE target_table = 'fact_orders'
ORDER BY execution_time DESC;
```

### 45. How do you handle data loading failures and recovery?
**Answer:**
```sql
-- Transaction-based loading
BEGIN;

-- Create checkpoint
CREATE TEMP TABLE load_checkpoint AS
SELECT MAX(order_id) as last_order_id FROM orders;

-- Attempt load
COPY orders FROM 's3://bucket/new_orders.csv' CSV;

-- Validate load
SELECT COUNT(*) FROM orders 
WHERE order_id > (SELECT last_order_id FROM load_checkpoint);

-- Commit or rollback based on validation
COMMIT; -- or ROLLBACK;

-- Error recovery
-- Check STL_LOAD_ERRORS for failure details
SELECT 
    starttime,
    filename,
    line_number,
    colname,
    err_reason
FROM stl_load_errors 
WHERE query = pg_last_copy_id();
```

---

## 🔍 Query Optimization

### 46. How do you analyze query performance in Redshift?
**Answer:**
```sql
-- Query execution details
SELECT 
    query,
    querytxt,
    starttime,
    endtime,
    datediff(seconds, starttime, endtime) as duration_seconds
FROM stl_query 
WHERE query = 12345;

-- Query steps breakdown
SELECT 
    query,
    step,
    operation,
    rows,
    bytes,
    workmem,
    is_diskbased
FROM stl_explain 
WHERE query = 12345
ORDER BY step;

-- I/O statistics
SELECT 
    query,
    step,
    rows,
    bytes,
    read_pct,
    write_pct
FROM stl_query_metrics 
WHERE query = 12345;
```

### 47. What are common query performance anti-patterns?
**Answer:**
```sql
-- Anti-pattern 1: SELECT *
-- Bad
SELECT * FROM large_table WHERE date_col = '2023-01-01';

-- Good
SELECT order_id, customer_id, amount 
FROM large_table WHERE date_col = '2023-01-01';

-- Anti-pattern 2: Functions in WHERE clause
-- Bad
SELECT * FROM orders WHERE EXTRACT(year FROM order_date) = 2023;

-- Good
SELECT * FROM orders 
WHERE order_date >= '2023-01-01' AND order_date < '2024-01-01';

-- Anti-pattern 3: Cartesian joins
-- Bad
SELECT * FROM table1, table2 WHERE condition;

-- Good
SELECT * FROM table1 JOIN table2 ON table1.id = table2.id WHERE condition;
```

### 48. How do you optimize JOIN operations?
**Answer:**
```sql
-- Co-located joins (same distribution key)
CREATE TABLE orders (order_id INT, customer_id INT DISTKEY);
CREATE TABLE customers (customer_id INT DISTKEY, name VARCHAR(100));

-- Efficient join - no data redistribution
SELECT o.order_id, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;

-- Broadcast join for small tables
CREATE TABLE product_types (type_id INT, type_name VARCHAR(50)) DISTSTYLE ALL;

-- Join optimization techniques:
-- 1. Use appropriate distribution keys
-- 2. Join on distribution keys when possible
-- 3. Use DISTSTYLE ALL for small dimension tables
-- 4. Order joins from largest to smallest tables
-- 5. Use EXISTS instead of IN for subqueries
```

### 49. How do you optimize GROUP BY and aggregation queries?
**Answer:**
```sql
-- Efficient aggregation with sort key
CREATE TABLE sales (
    sale_date DATE SORTKEY,
    product_id INT,
    amount DECIMAL(10,2)
) SORTKEY(sale_date, product_id);

-- Optimized query uses sort key
SELECT 
    sale_date,
    SUM(amount) as daily_total
FROM sales 
WHERE sale_date BETWEEN '2023-01-01' AND '2023-01-31'
GROUP BY sale_date
ORDER BY sale_date;

-- Use approximate functions for large datasets
SELECT 
    product_id,
    APPROXIMATE COUNT(DISTINCT customer_id) as unique_customers
FROM sales
GROUP BY product_id;
```

### 50. What are Redshift's query optimization techniques?
**Answer:**
- **Predicate pushdown**: Filter early in execution
- **Projection pushdown**: Select only needed columns
- **Join elimination**: Remove unnecessary joins
- **Aggregation pushdown**: Aggregate before joins
- **Sort merge joins**: Leverage sort keys
- **Hash joins**: For unsorted data
- **Nested loop joins**: For small datasets

### 51. How do you use EXPLAIN to optimize queries?
**Answer:**
```sql
-- Get query execution plan
EXPLAIN 
SELECT c.customer_name, SUM(o.amount)
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2023-01-01'
GROUP BY c.customer_name;

-- Analyze plan components:
-- XN Seq Scan: Sequential scan (potentially slow)
-- XN Hash Join: Hash join operation
-- XN Aggregate: Aggregation operation
-- XN Sort: Sorting operation
-- DS_DIST_*: Data redistribution (expensive)
-- DS_BCAST_*: Broadcast operation
```

### 52. How do you optimize window functions?
**Answer:**
```sql
-- Efficient window function with sort key
CREATE TABLE transactions (
    transaction_date DATE SORTKEY,
    customer_id INT DISTKEY,
    amount DECIMAL(10,2)
) SORTKEY(transaction_date, customer_id);

-- Optimized window function
SELECT 
    customer_id,
    transaction_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id 
        ORDER BY transaction_date 
        ROWS UNBOUNDED PRECEDING
    ) as running_total
FROM transactions
WHERE transaction_date >= '2023-01-01';

-- Tips:
-- 1. Use sort keys that match window function ORDER BY
-- 2. Partition by distribution key when possible
-- 3. Limit window frame size when appropriate
```

### 53. How do you handle large result sets efficiently?
**Answer:**
```sql
-- Use LIMIT for large result sets
SELECT * FROM large_table 
WHERE condition 
ORDER BY sort_column 
LIMIT 1000;

-- Use cursors for batch processing
DECLARE cursor_name CURSOR FOR 
SELECT * FROM large_table WHERE condition;

-- Pagination pattern
SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER (ORDER BY id) as rn
    FROM large_table
    WHERE condition
) WHERE rn BETWEEN 1001 AND 2000;

-- Use UNLOAD for large exports
UNLOAD ('SELECT * FROM large_table WHERE condition')
TO 's3://bucket/export/'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftRole';
```

### 54. What are query monitoring rules (QMR)?
**Answer:**
```sql
-- Create query monitoring rule
{
  "rule_name": "long_running_queries",
  "predicate": "query_execution_time > 3600",
  "action": "abort"
}

{
  "rule_name": "high_cpu_queries", 
  "predicate": "query_cpu_time > 300",
  "action": "log"
}

-- Monitor rule violations
SELECT 
    userid,
    query,
    rule,
    action,
    recordtime
FROM stl_wlm_rule_action
WHERE recordtime >= CURRENT_DATE - 1;
```

### 55. How do you optimize subqueries?
**Answer:**
```sql
-- Convert correlated subquery to join
-- Inefficient correlated subquery
SELECT customer_id, customer_name
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id 
    AND o.order_date >= '2023-01-01'
);

-- Efficient join
SELECT DISTINCT c.customer_id, c.customer_name
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2023-01-01';

-- Use IN instead of EXISTS when appropriate
SELECT customer_id FROM customers
WHERE customer_id IN (
    SELECT DISTINCT customer_id FROM orders 
    WHERE order_date >= '2023-01-01'
);
```

### 56. How do you handle data skew in queries?
**Answer:**
```sql
-- Identify skewed data
SELECT 
    customer_id,
    COUNT(*) as order_count
FROM orders
GROUP BY customer_id
ORDER BY order_count DESC
LIMIT 10;

-- Techniques to handle skew:
-- 1. Use different distribution key
-- 2. Add random suffix for hot keys
-- 3. Use DISTSTYLE EVEN for highly skewed data
-- 4. Pre-aggregate skewed data

-- Example: Handle hot customer
SELECT 
    CASE 
        WHEN customer_id = 'HOT_CUSTOMER' 
        THEN customer_id || '_' || (order_id % 10)
        ELSE customer_id 
    END as dist_key,
    *
FROM orders;
```

### 57. What are materialized views in Redshift?
**Answer:**
```sql
-- Create materialized view
CREATE MATERIALIZED VIEW mv_daily_sales AS
SELECT 
    DATE_TRUNC('day', order_date) as sale_date,
    product_category,
    SUM(amount) as total_sales,
    COUNT(*) as order_count
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE order_date >= '2023-01-01'
GROUP BY 1, 2;

-- Refresh materialized view
REFRESH MATERIALIZED VIEW mv_daily_sales;

-- Query materialized view
SELECT * FROM mv_daily_sales 
WHERE sale_date = '2023-01-15';
```

### 58. How do you optimize date and time queries?
**Answer:**
```sql
-- Use date literals instead of functions
-- Inefficient
SELECT * FROM orders 
WHERE EXTRACT(year FROM order_date) = 2023;

-- Efficient
SELECT * FROM orders 
WHERE order_date >= '2023-01-01' 
AND order_date < '2024-01-01';

-- Use date sort keys
CREATE TABLE time_series (
    timestamp TIMESTAMP SORTKEY,
    metric_value DECIMAL(10,2)
);

-- Efficient time range queries
SELECT * FROM time_series
WHERE timestamp BETWEEN '2023-01-01 00:00:00' 
AND '2023-01-01 23:59:59';
```

### 59. How do you use query result caching?
**Answer:**
```sql
-- Enable result caching (automatic in Redshift)
-- Cached when:
-- 1. Identical query text
-- 2. Same user or user with same permissions
-- 3. No underlying data changes
-- 4. Query completed successfully

-- Check if query used cache
SELECT 
    query,
    querytxt,
    source_query,
    cache_hit
FROM stl_query 
WHERE query = 12345;

-- Force cache bypass
SELECT /* NO_CACHE */ * FROM orders WHERE order_date = '2023-01-01';
```

### 60. What are late binding views and their benefits?
**Answer:**
```sql
-- Create late binding view
CREATE VIEW late_binding_view AS
SELECT 
    order_id,
    customer_id,
    order_date,
    amount
FROM orders
WITH NO SCHEMA BINDING;

-- Benefits:
-- 1. View remains valid when underlying table schema changes
-- 2. Can reference external tables (Spectrum)
-- 3. Better performance for complex views
-- 4. Supports cross-database queries

-- Regular view (early binding)
CREATE VIEW regular_view AS
SELECT * FROM orders;  -- Schema locked at creation time
```

---

## ⚙️ Administration & Operations

### 61. How do you monitor Redshift cluster health?
**Answer:**
```sql
-- Cluster performance metrics
SELECT 
    node,
    cpu_user,
    cpu_system,
    cpu_idle,
    memory_used_mb,
    memory_available_mb
FROM stv_node_storage_capacity;

-- Query queue wait times
SELECT 
    service_class,
    condition,
    count,
    avg_queue_time,
    max_queue_time
FROM stv_wlm_service_class_state;

-- Disk usage by table
SELECT 
    schema,
    "table",
    size,
    pct_used,
    unsorted,
    stats_off
FROM svv_table_info
WHERE size > 1000  -- Tables larger than 1GB
ORDER BY size DESC;
```

### 62. How do you implement Redshift security best practices?
**Answer:**
```sql
-- User and role management
CREATE USER analyst_user PASSWORD 'SecurePassword123!';
CREATE GROUP analysts;
ALTER GROUP analysts ADD USER analyst_user;

-- Grant permissions
GRANT SELECT ON ALL TABLES IN SCHEMA public TO GROUP analysts;
GRANT USAGE ON SCHEMA finance TO GROUP analysts;
GRANT SELECT ON finance.sensitive_table TO USER senior_analyst;

-- Row-level security (RLS)
CREATE RLS POLICY customer_policy ON orders
FOR SELECT TO analyst_user
USING (customer_region = current_user_region());

-- Column-level security
GRANT SELECT (order_id, customer_id, amount) ON orders TO analyst_user;
-- Exclude sensitive columns like SSN, credit_card_number

-- Audit logging
SELECT 
    userid,
    username,
    query,
    starttime
FROM stl_query
WHERE userid = 100  -- Specific user
AND starttime >= CURRENT_DATE - 1;
```

### 63. How do you implement backup and disaster recovery?
**Answer:**
```sql
-- Automated snapshots configuration
{
  "ClusterIdentifier": "my-redshift-cluster",
  "AutomatedSnapshotRetentionPeriod": 7,
  "PreferredMaintenanceWindow": "sun:03:00-sun:04:00"
}

-- Manual snapshot
aws redshift create-cluster-snapshot \
  --cluster-identifier my-cluster \
  --snapshot-identifier manual-snapshot-2023-01-15

-- Cross-region snapshot copy
aws redshift copy-cluster-snapshot \
  --source-snapshot-identifier manual-snapshot-2023-01-15 \
  --target-snapshot-identifier dr-snapshot-2023-01-15 \
  --destination-region us-west-2

-- Restore cluster
aws redshift restore-from-cluster-snapshot \
  --cluster-identifier restored-cluster \
  --snapshot-identifier manual-snapshot-2023-01-15
```

### 64. How do you handle Redshift maintenance and upgrades?
**Answer:**
```sql
-- Maintenance window configuration
{
  "PreferredMaintenanceWindow": "sun:03:00-sun:04:00",
  "AllowVersionUpgrade": true,
  "AutoMinorVersionUpgrade": true
}

-- Check maintenance status
SELECT 
    cluster_identifier,
    maintenance_track_name,
    current_version,
    next_maintenance_window_start_time
FROM stv_maintenance_window_state;

-- Defer maintenance (if needed)
aws redshift modify-cluster \
  --cluster-identifier my-cluster \
  --defer-maintenance \
  --defer-maintenance-duration 14  -- days
```

### 65. How do you optimize Redshift costs?
**Answer:**
```sql
-- Reserved instance planning
-- Analyze usage patterns
SELECT 
    DATE_TRUNC('hour', starttime) as hour,
    COUNT(*) as query_count,
    AVG(datediff(seconds, starttime, endtime)) as avg_duration
FROM stl_query
WHERE starttime >= CURRENT_DATE - 30
GROUP BY 1
ORDER BY 1;

-- Pause/resume cluster for dev environments
aws redshift pause-cluster --cluster-identifier dev-cluster
aws redshift resume-cluster --cluster-identifier dev-cluster

-- Use Redshift Serverless for variable workloads
{
  "workgroupName": "analytics-workgroup",
  "baseCapacity": 32,  -- RPUs (Redshift Processing Units)
  "maxCapacity": 512
}

-- Monitor costs with usage tracking
SELECT 
    service_class,
    slots,
    query_working_mem,
    query_cpu_time,
    query_blocks_read
FROM stl_wlm_query
WHERE service_class > 4  -- User-defined queues
AND starttime >= CURRENT_DATE - 1;
```

### 66. How do you implement data governance in Redshift?
**Answer:**
```sql
-- Data classification and tagging
CREATE TABLE customer_data (
    customer_id INT,
    customer_name VARCHAR(100),
    email VARCHAR(100),  -- PII
    ssn VARCHAR(11),     -- Sensitive PII
    phone VARCHAR(20)    -- PII
);

-- Implement data masking
CREATE VIEW masked_customers AS
SELECT 
    customer_id,
    customer_name,
    CASE 
        WHEN CURRENT_USER IN ('analyst1', 'analyst2') 
        THEN 'xxx@xxx.com'
        ELSE email 
    END as email,
    '***-**-****' as ssn,  -- Always masked
    phone
FROM customer_data;

-- Data lineage tracking
CREATE TABLE data_lineage_log (
    table_name VARCHAR(100),
    source_system VARCHAR(100),
    load_timestamp TIMESTAMP,
    record_count BIGINT,
    data_quality_score DECIMAL(3,2)
);
```

### 67. How do you troubleshoot common Redshift issues?
**Answer:**
```sql
-- Long-running queries
SELECT 
    query,
    pid,
    user_name,
    starttime,
    DATEDIFF(seconds, starttime, GETDATE()) as runtime_seconds,
    SUBSTRING(querytxt, 1, 100) as query_text
FROM stv_recents 
WHERE status = 'Running'
AND DATEDIFF(seconds, starttime, GETDATE()) > 300  -- > 5 minutes
ORDER BY runtime_seconds DESC;

-- Blocking queries
SELECT 
    blocked_pid,
    blocking_pid,
    blocked_query,
    blocking_query,
    lock_owner_table
FROM stv_locks
WHERE granted = 'f';  -- Not granted (blocked)

-- Disk space issues
SELECT 
    node,
    used,
    capacity,
    (used::float/capacity::float)*100 as pct_used
FROM stv_partitions
WHERE pct_used > 80;  -- > 80% full

-- Kill problematic query
CANCEL query_id;
```

### 68. How do you implement connection pooling?
**Answer:**
```python
# Using pgbouncer for connection pooling
# pgbouncer.ini configuration
[databases]
redshift_db = host=cluster.region.redshift.amazonaws.com port=5439 dbname=analytics

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
max_db_connections = 100

# Application connection
import psycopg2
from psycopg2 import pool

# Create connection pool
connection_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=1,
    maxconn=20,
    host='pgbouncer-host',
    port=6432,
    database='redshift_db',
    user='username',
    password='password'
)

# Use connection from pool
conn = connection_pool.getconn()
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM orders")
result = cursor.fetchone()
connection_pool.putconn(conn)
```

### 69. How do you implement automated monitoring and alerting?
**Answer:**
```python
# CloudWatch custom metrics
import boto3

def publish_redshift_metrics():
    redshift = boto3.client('redshift')
    cloudwatch = boto3.client('cloudwatch')
    
    # Get cluster metrics
    response = redshift.describe_clusters(
        ClusterIdentifier='my-cluster'
    )
    
    cluster = response['Clusters'][0]
    
    # Publish custom metrics
    cloudwatch.put_metric_data(
        Namespace='Redshift/Custom',
        MetricData=[
            {
                'MetricName': 'ClusterStatus',
                'Value': 1 if cluster['ClusterStatus'] == 'available' else 0,
                'Unit': 'Count'
            }
        ]
    )

# CloudWatch alarms
{
  "AlarmName": "RedshiftHighCPU",
  "MetricName": "CPUUtilization",
  "Namespace": "AWS/Redshift",
  "Statistic": "Average",
  "Period": 300,
  "EvaluationPeriods": 2,
  "Threshold": 80,
  "ComparisonOperator": "GreaterThanThreshold"
}
```

### 70. How do you implement multi-tenancy in Redshift?
**Answer:**
```sql
-- Schema-based multi-tenancy
CREATE SCHEMA tenant_a;
CREATE SCHEMA tenant_b;

-- Create tenant-specific users
CREATE USER tenant_a_user PASSWORD 'password';
CREATE USER tenant_b_user PASSWORD 'password';

-- Grant schema access
GRANT ALL ON SCHEMA tenant_a TO tenant_a_user;
GRANT ALL ON SCHEMA tenant_b TO tenant_b_user;

-- Row-level security for shared tables
CREATE TABLE shared_orders (
    order_id INT,
    tenant_id VARCHAR(50),
    customer_id INT,
    amount DECIMAL(10,2)
);

-- Create RLS policy
CREATE RLS POLICY tenant_isolation ON shared_orders
FOR ALL TO PUBLIC
USING (tenant_id = current_setting('app.current_tenant'));

-- Set tenant context in application
SET app.current_tenant = 'tenant_a';
SELECT * FROM shared_orders;  -- Only sees tenant_a data
```

### 71. How do you handle Redshift version upgrades?
**Answer:**
```sql
-- Check current version
SELECT version();

-- Plan upgrade strategy
-- 1. Test in development environment
-- 2. Review release notes for breaking changes
-- 3. Plan maintenance window
-- 4. Create snapshot before upgrade
-- 5. Monitor post-upgrade performance

-- Upgrade process
aws redshift modify-cluster \
  --cluster-identifier my-cluster \
  --cluster-version "1.0.47" \
  --allow-version-upgrade

-- Post-upgrade validation
-- Check query performance
SELECT 
    query,
    starttime,
    endtime,
    datediff(seconds, starttime, endtime) as duration
FROM stl_query
WHERE starttime >= '2023-01-15 10:00:00'  -- After upgrade
ORDER BY duration DESC
LIMIT 10;
```

### 72. How do you implement data retention policies?
**Answer:**
```sql
-- Time-based retention
CREATE OR REPLACE PROCEDURE cleanup_old_data()
AS $$
BEGIN
    -- Archive data older than 2 years
    INSERT INTO orders_archive
    SELECT * FROM orders 
    WHERE order_date < CURRENT_DATE - INTERVAL '2 years';
    
    -- Delete archived data from main table
    DELETE FROM orders 
    WHERE order_date < CURRENT_DATE - INTERVAL '2 years';
    
    -- Log cleanup activity
    INSERT INTO cleanup_log VALUES (
        'orders',
        CURRENT_DATE - INTERVAL '2 years',
        ROW_COUNT,
        GETDATE()
    );
END;
$$ LANGUAGE plpgsql;

-- Schedule cleanup (using external scheduler)
-- 0 2 * * 0 (Weekly on Sunday at 2 AM)
CALL cleanup_old_data();
```

### 73. How do you implement change management for Redshift?
**Answer:**
```sql
-- Version control for schema changes
-- migration_001_create_orders_table.sql
CREATE TABLE orders (
    order_id INT IDENTITY(1,1),
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL
) DISTKEY(customer_id) SORTKEY(order_date);

-- migration_002_add_status_column.sql
ALTER TABLE orders ADD COLUMN status VARCHAR(20) DEFAULT 'pending';

-- Track schema versions
CREATE TABLE schema_migrations (
    version VARCHAR(50) PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT GETDATE(),
    applied_by VARCHAR(100) DEFAULT CURRENT_USER
);

-- Deployment script
INSERT INTO schema_migrations (version) VALUES ('002_add_status_column');

-- Rollback plan
-- rollback_002.sql
ALTER TABLE orders DROP COLUMN status;
DELETE FROM schema_migrations WHERE version = '002_add_status_column';
```

### 74. How do you implement compliance and auditing?
**Answer:**
```sql
-- Enable audit logging
{
  "ClusterIdentifier": "my-cluster",
  "LoggingProperties": {
    "Enable": true,
    "BucketName": "my-audit-bucket",
    "S3KeyPrefix": "redshift-logs/"
  }
}

-- Query audit logs
SELECT 
    recordtime,
    username,
    database_name,
    query_text,
    query_id
FROM stl_query
WHERE username = 'sensitive_user'
AND recordtime >= CURRENT_DATE - 7
ORDER BY recordtime DESC;

-- Data access tracking
CREATE TABLE data_access_log (
    access_time TIMESTAMP DEFAULT GETDATE(),
    user_name VARCHAR(100) DEFAULT CURRENT_USER,
    table_name VARCHAR(100),
    operation VARCHAR(20),
    row_count BIGINT
);

-- Trigger for sensitive table access
CREATE OR REPLACE FUNCTION log_sensitive_access()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO data_access_log (table_name, operation, row_count)
    VALUES (TG_TABLE_NAME, TG_OP, 1);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### 75. How do you implement disaster recovery testing?
**Answer:**
```sql
-- DR testing procedure
-- 1. Create test snapshot
CREATE SNAPSHOT dr_test_snapshot_20230115 
FROM CLUSTER production_cluster;

-- 2. Restore in DR region
RESTORE CLUSTER dr_test_cluster 
FROM SNAPSHOT dr_test_snapshot_20230115
IN REGION us-west-2;

-- 3. Validate data integrity
SELECT 
    table_name,
    row_count,
    checksum
FROM (
    SELECT 
        'orders' as table_name,
        COUNT(*) as row_count,
        SUM(CHECKSUM(order_id, customer_id, amount)) as checksum
    FROM orders
    UNION ALL
    SELECT 
        'customers' as table_name,
        COUNT(*) as row_count,
        SUM(CHECKSUM(customer_id, customer_name)) as checksum
    FROM customers
) validation_results;

-- 4. Test application connectivity
-- 5. Measure RTO/RPO metrics
-- 6. Document lessons learned
-- 7. Clean up test resources

DROP CLUSTER dr_test_cluster;
```

---

## 🎯 **Quick Reference Commands**

```sql
-- Cluster management
CREATE CLUSTER my_cluster NODE_TYPE dc2.large MASTER_USERNAME admin;
RESIZE CLUSTER my_cluster NODE_TYPE ra3.xlplus NUMBER_OF_NODES 4;
PAUSE CLUSTER my_cluster;
RESUME CLUSTER my_cluster;

-- Data loading
COPY table_name FROM 's3://bucket/data.csv' IAM_ROLE 'role_arn' CSV;
UNLOAD ('SELECT * FROM table_name') TO 's3://bucket/export/' IAM_ROLE 'role_arn';

-- Performance monitoring
SELECT * FROM stl_query WHERE starttime >= CURRENT_DATE - 1;
SELECT * FROM svv_table_info ORDER BY size DESC;
ANALYZE table_name;
VACUUM table_name;

-- User management
CREATE USER username PASSWORD 'password';
GRANT SELECT ON table_name TO username;
REVOKE ALL ON table_name FROM username;
```

---

**Total Questions: 75** | **Difficulty: Beginner to Expert** | **Coverage: Complete Redshift Ecosystem**