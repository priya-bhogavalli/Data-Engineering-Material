# Apache Hive Key Concepts for Data Engineering

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Core Components](#-core-components)
   - [Hive Architecture](#hive-architecture)
   - [Metastore](#metastore)
   - [Query Engine](#query-engine)
3. [Hive Architecture](#-hive-architecture)
4. [HiveQL (Hive Query Language)](#-hiveql-hive-query-language)
5. [Data Storage & File Formats](#-data-storage--file-formats)
6. [Performance Optimization](#-performance-optimization)
   - [Partitioning](#1-partitioning)
   - [Bucketing](#2-bucketing)
   - [Indexing](#3-indexing)
7. [Configuration](#️-configuration)
8. [ACID Transactions](#-acid-transactions)
9. [When to Use Hive](#-when-to-use-hive)
10. [Interview Focus Areas](#-interview-focus-areas)
11. [Quick References](#-quick-references)

---

## 🎯 Overview

Apache Hive is a data warehouse software built on top of Apache Hadoop for providing data query and analysis. It provides a SQL-like interface to query data stored in various databases and file systems that integrate with Hadoop.

**Key Benefits:**
- **SQL-like Interface**: HiveQL provides familiar SQL syntax for Hadoop data
- **Schema on Read**: Flexible schema definition at query time
- **Scalability**: Handles petabyte-scale data processing
- **Integration**: Works seamlessly with Hadoop ecosystem tools

## 📦 Core Components

### Hive Architecture

**Definition**: Hive follows a layered architecture with multiple components working together to process queries.

**Core Components**:
- **Hive CLI/Beeline**: Command-line interfaces for executing queries
- **Hive Driver**: Manages query lifecycle and session handling
- **Compiler**: Parses HiveQL and creates execution plans
- **Optimizer**: Optimizes query execution plans
- **Execution Engine**: Executes queries using MapReduce, Tez, or Spark
- **Metastore**: Stores metadata about tables, partitions, and schemas

### Metastore

**Definition**: Central repository that stores metadata information about Hive tables, partitions, columns, and their data types.

**Key Features**:
- **Schema Storage**: Table definitions and column information
- **Partition Metadata**: Partition locations and properties
- **Statistics**: Table and column statistics for optimization
- **Security**: Access control and authorization information

```sql
-- View metastore information
SHOW DATABASES;
SHOW TABLES IN database_name;
DESCRIBE FORMATTED table_name;
SHOW PARTITIONS table_name;
```

### Query Engine

**Definition**: Component responsible for executing HiveQL queries by translating them into MapReduce, Tez, or Spark jobs.

**Execution Engines**:
- **MapReduce**: Traditional batch processing (slower)
- **Tez**: Directed Acyclic Graph (DAG) execution (faster)
- **Spark**: In-memory processing (fastest for iterative queries)

```sql
-- Set execution engine
SET hive.execution.engine=tez;  -- or mapreduce, spark
```

## 🏧 Hive Architecture

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                HIVE ARCHITECTURE                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐             │
│  │   HIVE CLI      │    │    BEELINE      │    │   JDBC/ODBC     │             │
│  │                 │    │                 │    │   DRIVERS       │             │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘             │
│           │                       │                       │                     │
│           └───────────────────────┼───────────────────────┘                     │
│                                   │                                             │
│  ┌─────────────────────────────────▼─────────────────────────────────────────┐   │
│  │                           HIVE DRIVER                                     │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │   Parser    │  │  Compiler   │  │  Optimizer  │  │  Executor   │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                   │                                             │
│  ┌─────────────────────────────────▼─────────────────────────────────────────┐   │
│  │                           METASTORE                                       │   │
│  │  ┌─────────────────────────────────────────────────────────────────────┐ │   │
│  │  │ • Table Schemas        • Partition Information                      │ │   │
│  │  │ • Column Metadata      • Storage Location                           │ │   │
│  │  │ • Data Types          • File Formats                               │ │   │
│  │  │ • Statistics          • Access Control                             │ │   │
│  │  └─────────────────────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                   │                                             │
│  ┌─────────────────────────────────▼─────────────────────────────────────────┐   │
│  │                        EXECUTION ENGINES                                  │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                       │   │
│  │  │ MapReduce   │  │     Tez     │  │    Spark    │                       │   │
│  │  │ (Batch)     │  │   (DAG)     │  │ (In-Memory) │                       │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                       │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                   │                                             │
│  ┌─────────────────────────────────▼─────────────────────────────────────────┐   │
│  │                           HADOOP HDFS                                     │   │
│  │  ┌─────────────────────────────────────────────────────────────────────┐ │   │
│  │  │ • Data Files (Parquet, ORC, Avro, Text)                            │ │   │
│  │  │ • Partitioned Data                                                  │ │   │
│  │  │ • Bucketed Tables                                                   │ │   │
│  │  │ • External Data Sources                                             │ │   │
│  │  └─────────────────────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🚀 HiveQL (Hive Query Language)

**Definition**: SQL-like query language for Hive that provides familiar syntax for data analysis and manipulation.

### Data Definition Language (DDL)

```sql
-- Create database
CREATE DATABASE IF NOT EXISTS sales_db
COMMENT 'Sales data warehouse'
LOCATION '/user/hive/warehouse/sales_db.db';

-- Create table
CREATE TABLE IF NOT EXISTS sales (
    transaction_id STRING,
    customer_id INT,
    product_id INT,
    amount DECIMAL(10,2),
    transaction_date DATE
)
PARTITIONED BY (year INT, month INT)
CLUSTERED BY (customer_id) INTO 32 BUCKETS
STORED AS PARQUET
LOCATION '/user/data/sales'
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- Create external table
CREATE EXTERNAL TABLE web_logs (
    ip_address STRING,
    timestamp STRING,
    request STRING,
    status_code INT,
    response_size INT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe'
WITH SERDEPROPERTIES (
    'input.regex' = '([^ ]*) [^ ]* [^ ]* \\[([^\\]]*)\\] "([^"]*)" ([0-9]*) ([0-9]*)'
)
STORED AS TEXTFILE
LOCATION '/user/logs/web';
```

### Data Manipulation Language (DML)

```sql
-- Insert data
INSERT INTO TABLE sales PARTITION(year=2024, month=1)
VALUES 
    ('TXN001', 1001, 2001, 299.99, '2024-01-15'),
    ('TXN002', 1002, 2002, 149.50, '2024-01-16');

-- Insert from select
INSERT OVERWRITE TABLE sales PARTITION(year=2024, month=2)
SELECT transaction_id, customer_id, product_id, amount, transaction_date
FROM raw_sales
WHERE YEAR(transaction_date) = 2024 AND MONTH(transaction_date) = 2;

-- Update (requires ACID)
UPDATE sales 
SET amount = amount * 1.1 
WHERE year = 2024 AND customer_id = 1001;

-- Delete (requires ACID)
DELETE FROM sales 
WHERE year = 2024 AND amount < 10;
```

### Data Query Language (DQL)

```sql
-- Basic queries
SELECT customer_id, SUM(amount) as total_spent
FROM sales
WHERE year = 2024
GROUP BY customer_id
HAVING SUM(amount) > 1000
ORDER BY total_spent DESC
LIMIT 10;

-- Window functions
SELECT 
    customer_id,
    amount,
    transaction_date,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY transaction_date) as txn_sequence,
    SUM(amount) OVER (PARTITION BY customer_id ORDER BY transaction_date 
                     ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_total
FROM sales
WHERE year = 2024;

-- Complex joins
SELECT 
    c.customer_name,
    p.product_name,
    s.amount,
    s.transaction_date
FROM sales s
JOIN customers c ON s.customer_id = c.customer_id
JOIN products p ON s.product_id = p.product_id
WHERE s.year = 2024 AND s.month = 1;
```

## 💾 Data Storage & File Formats

**Definition**: Hive supports various file formats and storage options for optimal performance and compression.

### File Formats

```sql
-- Text format (default)
CREATE TABLE text_table (
    id INT,
    name STRING
) STORED AS TEXTFILE;

-- Parquet format (columnar, good for analytics)
CREATE TABLE parquet_table (
    id INT,
    name STRING,
    amount DECIMAL(10,2)
) STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- ORC format (optimized for Hive)
CREATE TABLE orc_table (
    id INT,
    name STRING,
    amount DECIMAL(10,2)
) STORED AS ORC
TBLPROPERTIES (
    'orc.compress'='ZLIB',
    'orc.create.index'='true'
);

-- Avro format (schema evolution)
CREATE TABLE avro_table
STORED AS AVRO
LOCATION '/user/data/avro_data'
TBLPROPERTIES (
    'avro.schema.url'='hdfs://namenode:port/path/to/schema.avsc'
);
```

### SerDe (Serializer/Deserializer)

```sql
-- JSON SerDe
CREATE TABLE json_table (
    id INT,
    data STRING
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
STORED AS TEXTFILE;

-- CSV SerDe
CREATE TABLE csv_table (
    id INT,
    name STRING,
    amount DOUBLE
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    'separatorChar' = ',',
    'quoteChar' = '"',
    'escapeChar' = '\\'
)
STORED AS TEXTFILE;
```

## ⚡ Performance Optimization

### 1. Partitioning

**Definition**: Dividing tables into partitions based on column values to improve query performance by partition pruning.

```sql
-- Create partitioned table
CREATE TABLE sales_partitioned (
    transaction_id STRING,
    customer_id INT,
    amount DECIMAL(10,2)
)
PARTITIONED BY (year INT, month INT, day INT)
STORED AS PARQUET;

-- Dynamic partitioning
SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;
SET hive.exec.max.dynamic.partitions=1000;

INSERT OVERWRITE TABLE sales_partitioned PARTITION(year, month, day)
SELECT 
    transaction_id,
    customer_id,
    amount,
    YEAR(transaction_date) as year,
    MONTH(transaction_date) as month,
    DAY(transaction_date) as day
FROM raw_sales;

-- Query with partition pruning
SELECT customer_id, SUM(amount)
FROM sales_partitioned
WHERE year = 2024 AND month = 1  -- Only scans specific partitions
GROUP BY customer_id;
```

### 2. Bucketing

**Definition**: Distributing data into fixed number of buckets based on hash of bucketing columns for efficient joins and sampling.

```sql
-- Create bucketed table
CREATE TABLE customers_bucketed (
    customer_id INT,
    name STRING,
    email STRING,
    region STRING
)
CLUSTERED BY (customer_id) INTO 32 BUCKETS
STORED AS ORC;

-- Enable bucketed map joins
SET hive.optimize.bucketmapjoin=true;
SET hive.optimize.bucketmapjoin.sortedmerge=true;

-- Efficient join on bucketed tables
SELECT c.name, s.amount
FROM customers_bucketed c
JOIN sales_bucketed s ON c.customer_id = s.customer_id;
```

### 3. Indexing

**Definition**: Creating indexes on frequently queried columns to speed up data retrieval.

```sql
-- Create index (deprecated in newer versions)
CREATE INDEX customer_idx ON TABLE sales (customer_id)
AS 'COMPACT'
WITH DEFERRED REBUILD;

-- Rebuild index
ALTER INDEX customer_idx ON sales REBUILD;

-- Show indexes
SHOW INDEXES ON sales;
```

## 🛠️ Configuration

**Definition**: Hive configuration parameters that control behavior, performance, and resource allocation.

### Performance Tuning

```sql
-- Enable Cost-Based Optimizer
SET hive.cbo.enable=true;
SET hive.compute.query.using.stats=true;
SET hive.stats.fetch.column.stats=true;

-- Vectorization for better performance
SET hive.vectorized.execution.enabled=true;
SET hive.vectorized.execution.reduce.enabled=true;

-- Parallel execution
SET hive.exec.parallel=true;
SET hive.exec.parallel.thread.number=8;

-- Join optimization
SET hive.auto.convert.join=true;
SET hive.mapjoin.smalltable.filesize=25000000;  -- 25MB

-- Compression
SET hive.exec.compress.output=true;
SET mapred.output.compression.codec=org.apache.hadoop.io.compress.SnappyCodec;
```

### Memory Management

```sql
-- Map-side join memory
SET hive.mapjoin.localtask.max.memory.usage=0.90;
SET hive.mapjoin.followby.gby.localtask.max.memory.usage=0.55;

-- Reduce memory
SET hive.exec.reducers.bytes.per.reducer=256000000;  -- 256MB
SET hive.exec.reducers.max=1009;
```

## 🔄 ACID Transactions

**Definition**: Hive supports ACID (Atomicity, Consistency, Isolation, Durability) transactions for INSERT, UPDATE, DELETE operations.

### ACID Configuration

```sql
-- Enable ACID transactions
SET hive.support.concurrency=true;
SET hive.enforce.bucketing=true;
SET hive.exec.dynamic.partition.mode=nonstrict;
SET hive.txn.manager=org.apache.hadoop.hive.ql.lockmgr.DbTxnManager;
SET hive.compactor.initiator.on=true;
SET hive.compactor.worker.threads=1;

-- Create ACID table
CREATE TABLE customer_updates (
    customer_id INT,
    name STRING,
    email STRING,
    last_updated TIMESTAMP
)
CLUSTERED BY (customer_id) INTO 4 BUCKETS
STORED AS ORC
TBLPROPERTIES ('transactional'='true');
```

### ACID Operations

```sql
-- Insert data
INSERT INTO customer_updates VALUES 
    (1, 'John Doe', 'john@example.com', current_timestamp()),
    (2, 'Jane Smith', 'jane@example.com', current_timestamp());

-- Update records
UPDATE customer_updates 
SET email = 'john.doe@newdomain.com', last_updated = current_timestamp()
WHERE customer_id = 1;

-- Delete records
DELETE FROM customer_updates WHERE customer_id = 2;

-- Merge operation (UPSERT)
MERGE INTO customer_updates AS target
USING (
    SELECT 3 as customer_id, 'Bob Johnson' as name, 'bob@example.com' as email
) AS source
ON target.customer_id = source.customer_id
WHEN MATCHED THEN 
    UPDATE SET name = source.name, email = source.email, last_updated = current_timestamp()
WHEN NOT MATCHED THEN 
    INSERT VALUES (source.customer_id, source.name, source.email, current_timestamp());
```

## 📊 When to Use Hive

- **Data Warehousing**: Large-scale data analysis and reporting
- **Batch Processing**: ETL operations on big data
- **SQL Familiarity**: Teams comfortable with SQL syntax
- **Hadoop Integration**: Existing Hadoop ecosystem
- **Cost-Effective**: Processing large datasets on commodity hardware

## 🎯 Interview Focus Areas

1. **Architecture**: Metastore, query execution, storage layers
2. **HiveQL**: SQL syntax, DDL/DML operations, functions
3. **Performance**: Partitioning, bucketing, file formats
4. **Optimization**: CBO, vectorization, join strategies
5. **ACID**: Transactional operations, limitations
6. **File Formats**: Parquet, ORC, Avro comparison
7. **Integration**: Hadoop ecosystem, Spark, external systems
8. **Troubleshooting**: Common issues, performance tuning
9. **Security**: Authentication, authorization, data masking
10. **Best Practices**: Schema design, query optimization

## 📚 Quick References

- [Hive Documentation](https://hive.apache.org/documentation.html)
- [HiveQL Language Manual](https://cwiki.apache.org/confluence/display/Hive/LanguageManual)
- [Hive Performance Tuning](https://cwiki.apache.org/confluence/display/Hive/Configuration+Properties)
- [Hive ACID Transactions](https://cwiki.apache.org/confluence/display/Hive/Hive+Transactions)