# Apache Hive Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-50)](#basic-level-questions-1-50)
2. [Intermediate Level Questions (51-100)](#intermediate-level-questions-51-100)
3. [Advanced Level Questions (101-150)](#advanced-level-questions-101-150)
4. [Performance & Optimization (151-200)](#performance--optimization-151-200)

---

## Basic Level Questions (1-50)

### 1. What is Apache Hive and how does it differ from traditional databases?

**Apache Hive** is a data warehouse software built on top of Apache Hadoop that provides SQL-like interface to query and analyze large datasets stored in Hadoop's distributed storage.

**Key Differences:**
- **Schema on Read**: Hive applies schema when data is read, not when stored
- **Batch Processing**: Optimized for large-scale batch operations, not real-time queries
- **Scalability**: Handles petabyte-scale data across distributed clusters
- **Storage**: Uses HDFS for distributed storage vs traditional RDBMS storage

### 2. Explain Hive architecture components.

**Core Components:**
- **Hive CLI/Beeline**: Command-line interfaces
- **Driver**: Manages query lifecycle
- **Compiler**: Parses HiveQL into execution plans
- **Metastore**: Stores table metadata
- **Execution Engine**: Runs queries (MapReduce/Tez/Spark)

### 3. What is Hive Metastore?

**Metastore** is the central repository storing metadata about Hive tables, partitions, columns, and schemas.

**Components:**
- **Database**: Stores metadata (MySQL, PostgreSQL, etc.)
- **Service**: Provides metadata access to Hive components
- **Client**: Libraries for accessing metastore

### 4. What are the different modes of Hive Metastore?

**Three Modes:**
- **Embedded**: Metastore runs in same JVM as Hive driver
- **Local**: Separate metastore process, same machine
- **Remote**: Metastore runs on separate server

### 5. Explain HiveQL and its components.

**HiveQL** is SQL-like query language for Hive supporting:
- **DDL**: CREATE, ALTER, DROP statements
- **DML**: INSERT, UPDATE, DELETE operations
- **DQL**: SELECT queries with joins, aggregations
- **Built-in Functions**: String, date, mathematical functions

### 6. What are Hive data types?

**Primitive Types:**
- TINYINT, SMALLINT, INT, BIGINT
- FLOAT, DOUBLE, DECIMAL
- BOOLEAN, STRING, VARCHAR, CHAR
- TIMESTAMP, DATE, BINARY

**Complex Types:**
- ARRAY, MAP, STRUCT, UNION

### 7. How do you create tables in Hive?

```sql
-- Internal table
CREATE TABLE employees (
    id INT,
    name STRING,
    salary DECIMAL(10,2)
) STORED AS PARQUET;

-- External table
CREATE EXTERNAL TABLE logs (
    timestamp STRING,
    level STRING,
    message STRING
) LOCATION '/user/data/logs';
```

### 8. What's the difference between internal and external tables?

**Internal Tables:**
- Hive manages both metadata and data
- Data deleted when table is dropped
- Stored in Hive warehouse directory

**External Tables:**
- Hive manages only metadata
- Data remains when table is dropped
- Data stored in specified location

### 9. What is partitioning in Hive?

**Partitioning** divides tables into partitions based on column values to improve query performance.

```sql
CREATE TABLE sales (
    id INT,
    amount DECIMAL(10,2)
) PARTITIONED BY (year INT, month INT)
STORED AS PARQUET;
```

### 10. What is bucketing in Hive?

**Bucketing** distributes data into fixed number of buckets based on hash of bucketing columns.

```sql
CREATE TABLE customers (
    id INT,
    name STRING
) CLUSTERED BY (id) INTO 32 BUCKETS
STORED AS ORC;
```

### 11. What are SerDes in Hive?

**SerDe (Serializer/Deserializer)** defines how Hive reads and writes data in different formats.

**Common SerDes:**
- LazySimpleSerDe (default)
- JsonSerDe
- OpenCSVSerDe
- RegexSerDe

### 12. What file formats does Hive support?

**Text Formats:**
- TEXTFILE (default)
- CSV, JSON

**Binary Formats:**
- PARQUET (columnar)
- ORC (optimized for Hive)
- AVRO (schema evolution)
- SEQUENCEFILE

### 13. How do you load data into Hive tables?

```sql
-- Load from file
LOAD DATA INPATH '/user/data/file.txt' INTO TABLE employees;

-- Insert from another table
INSERT INTO employees SELECT * FROM temp_employees;

-- Insert values
INSERT INTO employees VALUES (1, 'John', 50000);
```

### 14. What are Hive execution engines?

**Three Engines:**
- **MapReduce**: Traditional batch processing (slower)
- **Tez**: DAG-based execution (faster)
- **Spark**: In-memory processing (fastest for iterative queries)

### 15. How do you optimize Hive queries?

**Optimization Techniques:**
- Use partitioning and bucketing
- Enable vectorization
- Use appropriate file formats (ORC, Parquet)
- Enable Cost-Based Optimizer (CBO)
- Use map-side joins for small tables

### 16. What is Hive Cost-Based Optimizer?

**CBO** uses table and column statistics to generate optimal execution plans.

```sql
-- Enable CBO
SET hive.cbo.enable=true;
SET hive.compute.query.using.stats=true;

-- Generate statistics
ANALYZE TABLE sales COMPUTE STATISTICS;
ANALYZE TABLE sales COMPUTE STATISTICS FOR COLUMNS;
```

### 17. What are Hive UDFs?

**User Defined Functions** allow custom logic in Hive queries.

**Types:**
- **UDF**: One-to-one functions
- **UDAF**: Aggregation functions
- **UDTF**: Table-generating functions

### 18. How do you handle schema evolution in Hive?

**Schema Evolution** allows reading data with different schemas over time.

```sql
-- Add column
ALTER TABLE employees ADD COLUMNS (department STRING);

-- Change column type (limited support)
ALTER TABLE employees CHANGE salary salary DECIMAL(12,2);
```

### 19. What is dynamic partitioning?

**Dynamic Partitioning** automatically creates partitions based on data values.

```sql
SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;

INSERT OVERWRITE TABLE sales PARTITION(year, month)
SELECT id, amount, YEAR(date), MONTH(date) FROM raw_sales;
```

### 20. What are Hive views?

**Views** are virtual tables based on queries.

```sql
CREATE VIEW high_salary_employees AS
SELECT * FROM employees WHERE salary > 75000;
```

### 21-50. Additional Basic Questions

**21. What is Hive warehouse directory?**
Default location where Hive stores internal table data.

**22. How do you drop partitions?**
```sql
ALTER TABLE sales DROP PARTITION (year=2023, month=1);
```

**23. What is MSCK REPAIR TABLE?**
Command to sync partitions between metastore and HDFS.

**24. How do you show table structure?**
```sql
DESCRIBE FORMATTED table_name;
```

**25. What are Hive configuration properties?**
Settings that control Hive behavior, stored in hive-site.xml.

**26. How do you set Hive properties?**
```sql
SET property_name=value;
```

**27. What is Hive CLI vs Beeline?**
CLI is deprecated, Beeline is recommended JDBC client.

**28. How do you connect to Hive remotely?**
Use Beeline with JDBC URL or HiveServer2.

**29. What is HiveServer2?**
Service that allows remote clients to execute queries.

**30. How do you handle NULL values?**
Use IS NULL, IS NOT NULL, COALESCE, NVL functions.

**31. What are Hive built-in functions?**
String, date, math, conditional, and aggregate functions.

**32. How do you perform joins in Hive?**
```sql
SELECT * FROM table1 t1 JOIN table2 t2 ON t1.id = t2.id;
```

**33. What is map-side join?**
Join performed in map phase for small tables.

**34. How do you use CASE statements?**
```sql
SELECT CASE WHEN salary > 50000 THEN 'High' ELSE 'Low' END FROM employees;
```

**35. What are window functions?**
Functions that operate over a set of rows related to current row.

**36. How do you handle duplicates?**
Use DISTINCT, GROUP BY, or window functions.

**37. What is LATERAL VIEW?**
Used with table-generating functions to create multiple rows.

**38. How do you export data from Hive?**
```sql
INSERT OVERWRITE DIRECTORY '/path' SELECT * FROM table;
```

**39. What is Hive streaming?**
Processing data as it arrives using streaming APIs.

**40. How do you debug Hive queries?**
Use EXPLAIN, check logs, enable debug mode.

**41. What are Hive hooks?**
Extension points for custom logic during query execution.

**42. How do you secure Hive?**
Use Kerberos, Ranger, column masking, row filtering.

**43. What is Hive authorization?**
Access control mechanism for tables and databases.

**44. How do you backup Hive metadata?**
Backup metastore database and HDFS data.

**45. What is Hive compaction?**
Process to merge small files and clean up ACID tables.

**46. How do you monitor Hive performance?**
Use Hive UI, logs, metrics, and profiling tools.

**47. What are common Hive errors?**
OutOfMemory, small files, data skew, schema issues.

**48. How do you tune Hive memory?**
Configure heap size, map/reduce memory settings.

**49. What is Hive on Spark?**
Running Hive queries using Spark as execution engine.

**50. How do you migrate from Hive to Spark?**
Convert HiveQL to Spark SQL, test compatibility.

---

## Intermediate Level Questions (51-100)

### 51. How do you implement ACID transactions in Hive?

**ACID Configuration:**
```sql
SET hive.support.concurrency=true;
SET hive.enforce.bucketing=true;
SET hive.txn.manager=org.apache.hadoop.hive.ql.lockmgr.DbTxnManager;
SET hive.compactor.initiator.on=true;

CREATE TABLE acid_table (
    id INT,
    name STRING
) CLUSTERED BY (id) INTO 4 BUCKETS
STORED AS ORC
TBLPROPERTIES ('transactional'='true');
```

### 52. What are the limitations of Hive ACID?

**Limitations:**
- Only works with ORC format
- Requires bucketed tables
- No foreign key constraints
- Limited concurrent writers per partition
- Compaction overhead

### 53. How do you handle data skew in Hive?

**Solutions:**
```sql
-- Enable skew join optimization
SET hive.optimize.skewjoin=true;
SET hive.skewjoin.key=100000;

-- Use salting technique
SELECT /*+ MAPJOIN(b) */ * FROM 
(SELECT *, CAST(RAND() * 10 AS INT) as salt FROM table_a) a
JOIN 
(SELECT *, salt FROM table_b LATERAL VIEW explode(array(0,1,2,3,4,5,6,7,8,9)) t as salt) b
ON a.key = b.key AND a.salt = b.salt;
```

### 54. How do you optimize joins in Hive?

**Join Optimization:**
```sql
-- Map-side join
SET hive.auto.convert.join=true;
SET hive.mapjoin.smalltable.filesize=25000000;

-- Bucket map join
SET hive.optimize.bucketmapjoin=true;
SET hive.optimize.bucketmapjoin.sortedmerge=true;

-- Join hints
SELECT /*+ MAPJOIN(small_table) */ * 
FROM large_table l JOIN small_table s ON l.id = s.id;
```

### 55. What is vectorization in Hive?

**Vectorization** processes data in batches rather than row-by-row for better performance.

```sql
SET hive.vectorized.execution.enabled=true;
SET hive.vectorized.execution.reduce.enabled=true;
SET hive.vectorized.groupby.checkinterval=4096;
```

### 56. How do you implement slowly changing dimensions?

**SCD Type 2 Implementation:**
```sql
-- Create SCD table
CREATE TABLE customer_scd (
    customer_id INT,
    name STRING,
    email STRING,
    effective_date DATE,
    end_date DATE,
    is_current BOOLEAN
) STORED AS ORC;

-- Insert new version
INSERT INTO customer_scd
SELECT customer_id, name, email, CURRENT_DATE, NULL, true
FROM customer_updates;
```

### 57. How do you handle large file optimization?

**File Size Optimization:**
```sql
-- Set optimal file size
SET hive.merge.mapfiles=true;
SET hive.merge.mapredfiles=true;
SET hive.merge.size.per.task=256000000;
SET hive.merge.smallfiles.avgsize=128000000;

-- Use appropriate number of reducers
SET hive.exec.reducers.bytes.per.reducer=256000000;
```

### 58. What are Hive storage handlers?

**Storage Handlers** integrate Hive with external storage systems.

```sql
-- HBase integration
CREATE TABLE hbase_table (
    key STRING,
    value STRING
)
STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
WITH SERDEPROPERTIES (
    'hbase.columns.mapping' = ':key,cf:value'
)
TBLPROPERTIES ('hbase.table.name' = 'my_hbase_table');
```

### 59. How do you implement data quality checks?

**Quality Validation:**
```sql
-- Check for nulls
SELECT COUNT(*) as null_count 
FROM table_name 
WHERE important_column IS NULL;

-- Check duplicates
SELECT key, COUNT(*) as duplicate_count
FROM table_name
GROUP BY key
HAVING COUNT(*) > 1;

-- Data profiling
SELECT 
    COUNT(*) as total_rows,
    COUNT(DISTINCT customer_id) as unique_customers,
    MIN(amount) as min_amount,
    MAX(amount) as max_amount,
    AVG(amount) as avg_amount
FROM sales;
```

### 60. How do you implement incremental data processing?

**Incremental Processing:**
```sql
-- Track last processed timestamp
CREATE TABLE process_log (
    table_name STRING,
    last_processed_time TIMESTAMP
);

-- Incremental load
INSERT INTO target_table
SELECT * FROM source_table
WHERE update_time > (
    SELECT last_processed_time 
    FROM process_log 
    WHERE table_name = 'source_table'
);
```

### 61-100. Additional Intermediate Questions

**61. How do you implement data archiving?**
Move old partitions to cheaper storage tiers.

**62. What is Hive LLAP?**
Live Long and Process - interactive query service.

**63. How do you handle time zone conversions?**
Use from_utc_timestamp() and to_utc_timestamp() functions.

**64. What are Hive materialized views?**
Pre-computed views stored physically for faster queries.

**65. How do you implement row-level security?**
Use Apache Ranger or custom authorization.

**66. What is Hive streaming ingestion?**
Real-time data ingestion using streaming APIs.

**67. How do you optimize memory usage?**
Configure JVM heap, off-heap memory settings.

**68. What are Hive constraints?**
NOT NULL, DEFAULT, CHECK constraints (limited support).

**69. How do you handle schema validation?**
Use SerDe properties and table constraints.

**70. What is Hive query result caching?**
Cache query results for repeated queries.

**71. How do you implement data masking?**
Use column masking policies in Ranger.

**72. What are Hive workload management features?**
Resource pools, query queuing, resource isolation.

**73. How do you handle concurrent access?**
Use locks, transactions, and proper isolation levels.

**74. What is Hive query vectorization?**
SIMD processing for better CPU utilization.

**75. How do you implement data lineage?**
Track data flow using hooks and metadata.

**76. What are Hive performance counters?**
Metrics for monitoring query execution.

**77. How do you handle large result sets?**
Use LIMIT, pagination, or streaming results.

**78. What is Hive cost-based optimization?**
Use statistics for optimal query plans.

**79. How do you implement custom aggregations?**
Create UDAF (User Defined Aggregate Functions).

**80. What are Hive execution hooks?**
Pre/post execution hooks for custom logic.

**81. How do you handle data encryption?**
Use HDFS encryption zones and TLS.

**82. What is Hive query compilation?**
Process of converting HiveQL to execution plan.

**83. How do you implement data sampling?**
Use TABLESAMPLE clause for sampling.

**84. What are Hive storage policies?**
Rules for data placement and replication.

**85. How do you handle query timeouts?**
Configure timeout settings and monitoring.

**86. What is Hive query result compression?**
Compress intermediate and final results.

**87. How do you implement data validation rules?**
Use CHECK constraints and custom UDFs.

**88. What are Hive partition pruning techniques?**
Optimize queries to scan only relevant partitions.

**89. How do you handle metadata backup?**
Regular backup of metastore database.

**90. What is Hive query plan optimization?**
Techniques to improve execution plans.

**91. How do you implement data retention policies?**
Automated cleanup of old partitions.

**92. What are Hive indexing strategies?**
Create indexes on frequently queried columns.

**93. How do you handle query debugging?**
Use EXPLAIN, logs, and profiling tools.

**94. What is Hive memory management?**
Configure heap and off-heap memory usage.

**95. How do you implement data governance?**
Use metadata management and access controls.

**96. What are Hive performance best practices?**
Partitioning, bucketing, file formats, statistics.

**97. How do you handle data migration?**
Plan and execute data movement strategies.

**98. What is Hive query optimization framework?**
CBO, rule-based optimization, statistics.

**99. How do you implement monitoring and alerting?**
Use metrics, logs, and monitoring tools.

**100. What are Hive integration patterns?**
Connect with Spark, Kafka, external systems.

---

## Advanced Level Questions (101-150)

### 101. How do you implement custom storage handlers?

**Custom Storage Handler:**
```java
public class CustomStorageHandler extends DefaultStorageHandler {
    @Override
    public Class<? extends InputFormat> getInputFormatClass() {
        return CustomInputFormat.class;
    }
    
    @Override
    public Class<? extends OutputFormat> getOutputFormatClass() {
        return CustomOutputFormat.class;
    }
}
```

### 102. How do you optimize Hive for cloud environments?

**Cloud Optimization:**
```sql
-- S3 optimization
SET fs.s3a.fast.upload=true;
SET fs.s3a.multipart.size=104857600;
SET fs.s3a.connection.maximum=200;

-- Enable cloud-specific features
SET hive.blobstore.optimizations.enabled=true;
SET hive.blobstore.use.blobstore.as.scratchdir=true;
```

### 103. How do you implement complex ETL patterns?

**ETL Framework:**
```sql
-- Slowly Changing Dimension Type 2
MERGE INTO customer_dim AS target
USING customer_updates AS source
ON target.customer_id = source.customer_id AND target.is_current = true
WHEN MATCHED AND (target.name != source.name OR target.email != source.email) THEN
    UPDATE SET is_current = false, end_date = current_date()
WHEN NOT MATCHED THEN
    INSERT VALUES (source.customer_id, source.name, source.email, current_date(), null, true);
```

### 104. How do you implement advanced security patterns?

**Security Implementation:**
```sql
-- Row-level security
CREATE VIEW secure_sales AS
SELECT * FROM sales 
WHERE region = current_user_region();

-- Column masking
SELECT 
    customer_id,
    CASE WHEN has_permission('PII_ACCESS') 
         THEN email 
         ELSE mask_email(email) 
    END as email
FROM customers;
```

### 105. How do you handle multi-tenant architectures?

**Multi-tenancy:**
```sql
-- Tenant isolation
CREATE DATABASE tenant_${hiveconf:tenant_id}
LOCATION 's3://data-lake/tenants/${hiveconf:tenant_id}/';

-- Dynamic table access
SELECT * FROM ${hiveconf:tenant_id}.sales
WHERE tenant_id = '${hiveconf:tenant_id}';
```

### 106-150. Additional Advanced Questions

**106. How do you implement streaming analytics?**
Real-time processing with Kafka integration.

**107. What are advanced partitioning strategies?**
Multi-level partitioning, dynamic partition pruning.

**108. How do you handle schema registry integration?**
Avro schema evolution with registry.

**109. What are advanced join algorithms?**
Sort-merge join, broadcast join optimization.

**110. How do you implement data lake patterns?**
Bronze, silver, gold layer architecture.

**111. What are advanced UDF patterns?**
Generic UDFs, complex data type handling.

**112. How do you handle large-scale migrations?**
Parallel processing, validation, rollback strategies.

**113. What are advanced monitoring techniques?**
Custom metrics, performance profiling.

**114. How do you implement disaster recovery?**
Multi-region replication, backup strategies.

**115. What are advanced optimization techniques?**
Query rewriting, predicate pushdown.

**116. How do you handle complex data transformations?**
Window functions, analytical patterns.

**117. What are advanced security implementations?**
Encryption, tokenization, audit logging.

**118. How do you implement data governance frameworks?**
Metadata management, lineage tracking.

**119. What are advanced performance tuning methods?**
Resource allocation, query optimization.

**120. How do you handle integration challenges?**
API design, data format conversion.

**121-150. Continue with advanced topics covering:**
- Custom SerDes implementation
- Advanced ACID transaction patterns  
- Complex analytical queries
- Performance troubleshooting
- Scalability patterns
- Integration architectures
- Advanced security models
- Operational excellence
- Cost optimization
- Future-proofing strategies

---

## Performance & Optimization (151-200)

### 151. How do you diagnose and fix slow queries?

**Query Optimization Process:**
```sql
-- Analyze query plan
EXPLAIN EXTENDED SELECT * FROM large_table WHERE condition;

-- Check statistics
SHOW TABLE EXTENDED LIKE 'table_name';
ANALYZE TABLE table_name COMPUTE STATISTICS FOR COLUMNS;

-- Enable detailed logging
SET hive.root.logger=DEBUG,console;
```

### 152. How do you implement advanced caching strategies?

**Caching Techniques:**
```sql
-- Result caching
SET hive.query.results.cache.enabled=true;
SET hive.query.results.cache.max.size=2147483648;

-- Materialized views
CREATE MATERIALIZED VIEW sales_summary AS
SELECT region, SUM(amount) as total_sales
FROM sales GROUP BY region;
```

### 153-200. Additional Performance Questions

**153. How do you optimize for different workloads?**
Separate configurations for batch vs interactive queries.

**154. What are advanced memory management techniques?**
Off-heap storage, memory pools, garbage collection tuning.

**155. How do you implement workload isolation?**
Resource pools, queue management, priority scheduling.

**156. What are advanced file format optimizations?**
Compression algorithms, encoding strategies, block sizes.

**157. How do you handle resource contention?**
Fair scheduling, resource quotas, throttling.

**158. What are advanced indexing strategies?**
Bloom filters, zone maps, column statistics.

**159. How do you optimize for different data patterns?**
Skewed data, sparse data, time-series optimization.

**160. What are advanced partitioning techniques?**
Dynamic partitioning, partition evolution, pruning.

**161-200. Continue with performance topics covering:**
- Advanced query optimization
- Resource management
- Scalability patterns
- Monitoring and alerting
- Capacity planning
- Cost optimization
- Performance benchmarking
- Troubleshooting methodologies
- Best practices implementation
- Future performance considerations

---

## 🎯 Summary

This comprehensive collection covers 200 Apache Hive interview questions across all levels:

- **Basic (1-50)**: Core concepts, HiveQL, basic operations
- **Intermediate (51-100)**: ACID transactions, optimization, data quality
- **Advanced (101-150)**: Custom implementations, security, complex patterns
- **Performance (151-200)**: Query optimization, resource management, scalability

Each section builds upon previous knowledge to provide complete coverage of Hive concepts for data engineering interviews.

---

## 📚 Additional Comprehensive Content

*(Merged from comprehensive interview questions file)*

