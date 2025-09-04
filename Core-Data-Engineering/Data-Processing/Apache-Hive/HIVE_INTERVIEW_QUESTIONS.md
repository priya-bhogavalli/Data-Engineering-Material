# Apache Hive Interview Questions & Answers

## 📋 Table of Contents
1. [Core Concepts](#core-concepts)
2. [HiveQL and Data Types](#hiveql-and-data-types)
3. [Partitioning and Bucketing](#partitioning-and-bucketing)
4. [Performance Optimization](#performance-optimization)
5. [Integration and Use Cases](#integration-and-use-cases)

---

## Core Concepts

### 1. What is Apache Hive and how does it work with Hadoop?

**Answer:**
Apache Hive is a data warehouse software that provides SQL-like interface for querying and managing large datasets stored in Hadoop's distributed storage.

**Key Features:**
- **SQL-like Interface**: HiveQL for familiar SQL operations
- **Schema on Read**: Apply schema when reading data
- **Extensibility**: Custom functions and data formats
- **Integration**: Works with Hadoop ecosystem tools

**Architecture:**
```
Hive Components:
├── Hive CLI/Beeline (Client Interface)
├── Hive Driver (Query Processing)
├── Compiler (HiveQL to MapReduce/Tez/Spark)
├── Metastore (Schema and Metadata)
└── Execution Engine (MapReduce/Tez/Spark)

Data Flow:
HiveQL Query → Parser → Compiler → Optimizer → Execution Engine → HDFS
```

### 2. Explain Hive's architecture and key components.

**Answer:**
Hive architecture consists of several components that work together to process SQL-like queries on big data.

**Component Details:**

**Metastore:**
```sql
-- Stores table schemas, partitions, and statistics
CREATE TABLE customers (
    id INT,
    name STRING,
    email STRING,
    created_date DATE
)
STORED AS PARQUET
LOCATION '/data/customers/';

-- Metastore stores:
-- - Table schema (columns, data types)
-- - Storage location
-- - File format
-- - Partition information
```

**Query Processing:**
```
Query Execution Flow:
1. HiveQL Query → Hive Driver
2. Driver → Compiler (Parse, Analyze, Optimize)
3. Compiler → Execution Plan (DAG of tasks)
4. Execution Engine → MapReduce/Tez/Spark jobs
5. Results → Client
```

**Configuration:**
```xml
<!-- hive-site.xml -->
<configuration>
    <property>
        <name>javax.jdo.option.ConnectionURL</name>
        <value>jdbc:mysql://localhost:3306/hive_metastore</value>
    </property>
    <property>
        <name>hive.execution.engine</name>
        <value>tez</value>
    </property>
</configuration>
```

---

## HiveQL and Data Types

### 3. What are Hive's data types and how do you work with complex data?

**Answer:**
Hive supports primitive and complex data types for handling various data structures.

**Primitive Data Types:**
```sql
CREATE TABLE sales_data (
    transaction_id BIGINT,
    customer_id INT,
    product_name STRING,
    price DECIMAL(10,2),
    quantity SMALLINT,
    sale_date DATE,
    sale_timestamp TIMESTAMP,
    is_online BOOLEAN
);
```

**Complex Data Types:**
```sql
CREATE TABLE customer_orders (
    customer_id INT,
    customer_info STRUCT<name:STRING, email:STRING, phone:STRING>,
    order_items ARRAY<STRUCT<product_id:INT, quantity:INT, price:DECIMAL(10,2)>>,
    preferences MAP<STRING, STRING>
)
STORED AS PARQUET;

-- Working with complex types
SELECT 
    customer_id,
    customer_info.name,
    customer_info.email,
    order_items[0].product_id as first_product,
    preferences['newsletter'] as newsletter_pref
FROM customer_orders;

-- Array operations
SELECT 
    customer_id,
    size(order_items) as item_count,
    explode(order_items) as item
FROM customer_orders;

-- Map operations
SELECT 
    customer_id,
    map_keys(preferences) as pref_keys,
    map_values(preferences) as pref_values
FROM customer_orders;
```

### 4. How do you perform advanced HiveQL operations for data analysis?

**Answer:**
HiveQL supports advanced SQL operations for complex data analysis tasks.

**Window Functions:**
```sql
-- Ranking and analytics
SELECT 
    customer_id,
    order_date,
    order_amount,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as order_sequence,
    RANK() OVER (ORDER BY order_amount DESC) as amount_rank,
    LAG(order_amount, 1) OVER (PARTITION BY customer_id ORDER BY order_date) as prev_order,
    SUM(order_amount) OVER (PARTITION BY customer_id ORDER BY order_date 
                           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_total
FROM orders;
```

**Common Table Expressions (CTEs):**
```sql
WITH customer_metrics AS (
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        SUM(order_amount) as total_spent,
        AVG(order_amount) as avg_order_value
    FROM orders
    WHERE order_date >= '2023-01-01'
    GROUP BY customer_id
),
customer_segments AS (
    SELECT 
        customer_id,
        CASE 
            WHEN total_spent > 1000 THEN 'High Value'
            WHEN total_spent > 500 THEN 'Medium Value'
            ELSE 'Low Value'
        END as segment
    FROM customer_metrics
)
SELECT 
    segment,
    COUNT(*) as customer_count,
    AVG(total_spent) as avg_spent_per_segment
FROM customer_segments
GROUP BY segment;
```

**User Defined Functions (UDFs):**
```java
// Custom UDF for data processing
public class EmailDomainUDF extends UDF {
    public String evaluate(String email) {
        if (email == null || !email.contains("@")) {
            return null;
        }
        return email.substring(email.indexOf("@") + 1);
    }
}
```

```sql
-- Register and use UDF
ADD JAR /path/to/email-udf.jar;
CREATE TEMPORARY FUNCTION extract_domain AS 'com.company.EmailDomainUDF';

SELECT 
    customer_id,
    email,
    extract_domain(email) as email_domain
FROM customers;
```

---

## Partitioning and Bucketing

### 5. How do you implement partitioning in Hive for performance optimization?

**Answer:**
Partitioning divides tables into smaller, manageable pieces based on column values, improving query performance.

**Static Partitioning:**
```sql
-- Create partitioned table
CREATE TABLE sales_partitioned (
    transaction_id BIGINT,
    customer_id INT,
    product_id INT,
    amount DECIMAL(10,2)
)
PARTITIONED BY (year INT, month INT)
STORED AS PARQUET;

-- Insert data into specific partition
INSERT INTO sales_partitioned PARTITION (year=2023, month=12)
SELECT transaction_id, customer_id, product_id, amount
FROM sales_raw
WHERE year(sale_date) = 2023 AND month(sale_date) = 12;
```

**Dynamic Partitioning:**
```sql
-- Enable dynamic partitioning
SET hive.exec.dynamic.partition = true;
SET hive.exec.dynamic.partition.mode = nonstrict;
SET hive.exec.max.dynamic.partitions = 1000;

-- Dynamic partition insert
INSERT INTO sales_partitioned PARTITION (year, month)
SELECT 
    transaction_id,
    customer_id, 
    product_id,
    amount,
    year(sale_date) as year,
    month(sale_date) as month
FROM sales_raw;
```

**Partition Management:**
```sql
-- Show partitions
SHOW PARTITIONS sales_partitioned;

-- Add partition manually
ALTER TABLE sales_partitioned ADD PARTITION (year=2024, month=1);

-- Drop partition
ALTER TABLE sales_partitioned DROP PARTITION (year=2022, month=1);

-- Repair partitions (after external data addition)
MSCK REPAIR TABLE sales_partitioned;
```

### 6. What is bucketing in Hive and when should you use it?

**Answer:**
Bucketing divides data into fixed number of buckets based on hash function, enabling efficient joins and sampling.

**Bucketing Implementation:**
```sql
-- Create bucketed table
CREATE TABLE customer_bucketed (
    customer_id INT,
    name STRING,
    email STRING,
    registration_date DATE
)
CLUSTERED BY (customer_id) INTO 32 BUCKETS
STORED AS PARQUET;

-- Enable bucketing
SET hive.enforce.bucketing = true;

-- Insert data (Hive handles bucketing automatically)
INSERT INTO customer_bucketed
SELECT customer_id, name, email, registration_date
FROM customers_raw;
```

**Benefits and Use Cases:**
```sql
-- Efficient map-side joins (when both tables bucketed on join key)
SELECT /*+ MAPJOIN(o) */ 
    c.customer_id,
    c.name,
    o.order_id,
    o.order_amount
FROM customer_bucketed c
JOIN orders_bucketed o ON c.customer_id = o.customer_id;

-- Efficient sampling
SELECT * FROM customer_bucketed TABLESAMPLE(BUCKET 1 OUT OF 32);

-- Better performance for GROUP BY on bucketed column
SELECT 
    customer_id,
    COUNT(*) as order_count
FROM orders_bucketed
GROUP BY customer_id;
```

**Bucketing vs Partitioning:**
| Aspect | Partitioning | Bucketing |
|--------|--------------|-----------|
| **Purpose** | Reduce data scan | Improve joins/sampling |
| **Number of divisions** | Variable (based on data) | Fixed |
| **Query pruning** | Automatic | Manual (sampling) |
| **Join optimization** | Limited | Map-side joins |

---

## Performance Optimization

### 7. How do you optimize Hive query performance?

**Answer:**
Multiple optimization techniques can significantly improve Hive query performance.

**Execution Engine Optimization:**
```sql
-- Use Tez instead of MapReduce
SET hive.execution.engine = tez;

-- Enable vectorization
SET hive.vectorized.execution.enabled = true;
SET hive.vectorized.execution.reduce.enabled = true;

-- Cost-based optimization
SET hive.cbo.enable = true;
SET hive.compute.query.using.stats = true;
SET hive.stats.fetch.column.stats = true;
```

**Join Optimization:**
```sql
-- Map-side join for small tables
SELECT /*+ MAPJOIN(small_table) */
    l.customer_id,
    l.order_amount,
    s.customer_name
FROM large_orders_table l
JOIN small_customers_table s ON l.customer_id = s.customer_id;

-- Bucket map join
SET hive.auto.convert.join = true;
SET hive.auto.convert.join.noconditionaltask = true;
SET hive.auto.convert.join.noconditionaltask.size = 268435456; -- 256MB
```

**Storage Optimization:**
```sql
-- Use columnar formats
CREATE TABLE sales_optimized (
    transaction_id BIGINT,
    customer_id INT,
    product_id INT,
    amount DECIMAL(10,2),
    sale_date DATE
)
STORED AS ORC
TBLPROPERTIES (
    "orc.compress"="SNAPPY",
    "orc.stripe.size"="268435456"
);

-- Enable compression
SET hive.exec.compress.output = true;
SET mapreduce.output.fileoutputformat.compress.codec = org.apache.hadoop.io.compress.SnappyCodec;
```

### 8. How do you use Hive statistics for query optimization?

**Answer:**
Hive statistics help the optimizer make better decisions about query execution plans.

**Collecting Statistics:**
```sql
-- Analyze table for basic statistics
ANALYZE TABLE sales_data COMPUTE STATISTICS;

-- Analyze table with column statistics
ANALYZE TABLE sales_data COMPUTE STATISTICS FOR COLUMNS customer_id, amount, sale_date;

-- Analyze partitioned table
ANALYZE TABLE sales_partitioned PARTITION(year=2023, month=12) COMPUTE STATISTICS;

-- Analyze all partitions
ANALYZE TABLE sales_partitioned COMPUTE STATISTICS;
```

**Viewing Statistics:**
```sql
-- Show table statistics
DESCRIBE FORMATTED sales_data;

-- Show column statistics
DESCRIBE FORMATTED sales_data customer_id;

-- Show partition statistics
SHOW TABLE EXTENDED LIKE sales_partitioned PARTITION(year=2023, month=12);
```

**Using Statistics for Optimization:**
```sql
-- Enable cost-based optimization
SET hive.cbo.enable = true;
SET hive.stats.fetch.column.stats = true;
SET hive.stats.fetch.partition.stats = true;

-- Query with statistics-based optimization
EXPLAIN CBO
SELECT 
    customer_id,
    COUNT(*) as order_count,
    SUM(amount) as total_amount
FROM sales_data
WHERE sale_date >= '2023-01-01'
GROUP BY customer_id
HAVING COUNT(*) > 5;
```

---

## Integration and Use Cases

### 9. How do you integrate Hive with other big data tools?

**Answer:**
Hive integrates seamlessly with various tools in the Hadoop ecosystem and beyond.

**Spark Integration:**
```python
# PySpark with Hive
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("HiveIntegration") \
    .enableHiveSupport() \
    .getOrCreate()

# Query Hive tables from Spark
df = spark.sql("SELECT * FROM sales_data WHERE sale_date >= '2023-01-01'")

# Write Spark DataFrame to Hive
df.write \
  .mode("overwrite") \
  .option("path", "/data/processed_sales") \
  .saveAsTable("processed_sales")
```

**Kafka Integration:**
```sql
-- Create external table for Kafka data
CREATE TABLE kafka_events (
    event_id STRING,
    user_id STRING,
    event_type STRING,
    timestamp BIGINT,
    properties MAP<STRING, STRING>
)
STORED BY 'org.apache.hadoop.hive.kafka.KafkaStorageHandler'
TBLPROPERTIES (
    "kafka.topic" = "user_events",
    "kafka.bootstrap.servers" = "localhost:9092"
);
```

**HBase Integration:**
```sql
-- Create HBase-backed Hive table
CREATE TABLE customer_hbase (
    customer_id STRING,
    name STRING,
    email STRING,
    phone STRING
)
STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
WITH SERDEPROPERTIES (
    "hbase.columns.mapping" = ":key,info:name,info:email,info:phone"
)
TBLPROPERTIES (
    "hbase.table.name" = "customers"
);
```

### 10. What are common Hive use cases in data engineering pipelines?

**Answer:**
Hive serves multiple purposes in modern data engineering workflows.

**ETL Processing:**
```sql
-- Data transformation pipeline
CREATE TABLE customer_summary AS
SELECT 
    c.customer_id,
    c.name,
    c.email,
    c.registration_date,
    COUNT(o.order_id) as total_orders,
    SUM(o.amount) as total_spent,
    AVG(o.amount) as avg_order_value,
    MAX(o.order_date) as last_order_date,
    DATEDIFF(CURRENT_DATE, MAX(o.order_date)) as days_since_last_order
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.email, c.registration_date;
```

**Data Quality Checks:**
```sql
-- Data quality validation
CREATE TABLE data_quality_report AS
SELECT 
    'customers' as table_name,
    COUNT(*) as total_records,
    COUNT(CASE WHEN customer_id IS NULL THEN 1 END) as null_customer_ids,
    COUNT(CASE WHEN email NOT RLIKE '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$' THEN 1 END) as invalid_emails,
    COUNT(DISTINCT customer_id) as unique_customers,
    COUNT(*) - COUNT(DISTINCT customer_id) as duplicate_records
FROM customers

UNION ALL

SELECT 
    'orders' as table_name,
    COUNT(*) as total_records,
    COUNT(CASE WHEN order_id IS NULL THEN 1 END) as null_order_ids,
    COUNT(CASE WHEN amount <= 0 THEN 1 END) as invalid_amounts,
    COUNT(DISTINCT order_id) as unique_orders,
    COUNT(*) - COUNT(DISTINCT order_id) as duplicate_records
FROM orders;
```

**Reporting and Analytics:**
```sql
-- Business intelligence queries
CREATE VIEW monthly_sales_report AS
SELECT 
    year(order_date) as year,
    month(order_date) as month,
    COUNT(DISTINCT customer_id) as unique_customers,
    COUNT(*) as total_orders,
    SUM(amount) as total_revenue,
    AVG(amount) as avg_order_value,
    PERCENTILE_APPROX(amount, 0.5) as median_order_value
FROM orders
GROUP BY year(order_date), month(order_date);

-- Customer segmentation
CREATE TABLE customer_segments AS
SELECT 
    customer_id,
    total_spent,
    order_count,
    CASE 
        WHEN total_spent >= 1000 AND order_count >= 10 THEN 'VIP'
        WHEN total_spent >= 500 AND order_count >= 5 THEN 'Premium'
        WHEN total_spent >= 100 AND order_count >= 2 THEN 'Regular'
        ELSE 'New'
    END as segment
FROM customer_summary;
```

---

## Summary

Apache Hive provides SQL-like interface for big data processing with:

1. **SQL Familiarity**: HiveQL for easy adoption by SQL users
2. **Schema Management**: Flexible schema-on-read approach
3. **Performance Optimization**: Partitioning, bucketing, and statistics
4. **Ecosystem Integration**: Works with Spark, Kafka, HBase, and other tools
5. **Scalability**: Handles petabyte-scale data processing on Hadoop clusters