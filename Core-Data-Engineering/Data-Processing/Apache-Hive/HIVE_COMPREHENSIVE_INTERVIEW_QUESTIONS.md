# Apache Hive - Comprehensive Interview Questions & Answers

## 📋 Table of Contents
1. [Core Concepts](#-core-concepts)
2. [Hive Architecture](#-hive-architecture)
3. [HiveQL (Hive Query Language)](#-hiveql-hive-query-language)
4. [Data Types & File Formats](#-data-types--file-formats)
5. [Partitioning & Bucketing](#-partitioning--bucketing)
6. [Performance Optimization](#-performance-optimization)
7. [Hive Metastore](#-hive-metastore)
8. [User Defined Functions (UDFs)](#-user-defined-functions-udfs)
9. [Integration & Ecosystem](#-integration--ecosystem)
10. [Real-world Scenarios](#-real-world-scenarios)

---

## 🎯 Core Concepts

### Q1: What is Apache Hive and what problems does it solve?
**Answer:**
Apache Hive is a data warehouse software built on Hadoop that provides SQL-like query capabilities for large datasets stored in HDFS.

**Key Problems Solved:**
- **SQL Interface**: Provides familiar SQL syntax for Hadoop data
- **Schema-on-Read**: Flexible schema definition at query time
- **Large-scale Analytics**: Handles petabyte-scale data processing
- **Batch Processing**: Optimized for analytical workloads
- **Data Abstraction**: Hides MapReduce complexity from analysts

**Core Features:**
- HiveQL (SQL-like query language)
- Metastore for schema management
- Support for various file formats
- Extensible with UDFs
- Integration with Hadoop ecosystem

### Q2: Explain the difference between Hive and traditional RDBMS
**Answer:**
**Apache Hive vs Traditional RDBMS:**

| Aspect | Hive | Traditional RDBMS |
|--------|------|-------------------|
| **Schema** | Schema-on-Read | Schema-on-Write |
| **ACID** | Limited ACID support | Full ACID compliance |
| **Scalability** | Horizontal scaling | Vertical scaling |
| **Latency** | High latency (batch) | Low latency (real-time) |
| **Data Size** | Petabytes | Terabytes |
| **Updates** | Limited UPDATE/DELETE | Full DML support |
| **Indexes** | Limited indexing | Rich indexing |
| **Joins** | MapReduce-based joins | Optimized joins |

**Use Cases:**
- **Hive**: Data warehousing, ETL, batch analytics
- **RDBMS**: OLTP, real-time queries, transactional systems

### Q3: What are the advantages and limitations of Hive?
**Answer:**
**Advantages:**
- SQL-like interface for Hadoop data
- Handles large-scale data processing
- Cost-effective for big data analytics
- Extensible with custom functions
- Integration with BI tools
- Schema flexibility
- Fault tolerance through Hadoop

**Limitations:**
- High latency (not suitable for real-time)
- Limited ACID transactions
- No row-level updates/deletes (in older versions)
- Not optimized for OLTP workloads
- Dependency on Hadoop ecosystem
- Limited indexing capabilities
- No stored procedures

---

## 🏗️ Hive Architecture

### Q4: Explain Hive architecture and its components
**Answer:**
**Hive Architecture Components:**

```
Client (CLI/JDBC/ODBC) → Hive Driver → Query Compiler → Execution Engine → Metastore
                                                      ↓
                                               MapReduce/Tez/Spark
                                                      ↓
                                                    HDFS
```

**Key Components:**

1. **Hive Client**
   - CLI (Command Line Interface)
   - JDBC/ODBC drivers
   - Web UI (HUE)

2. **Hive Driver**
   - Receives queries from clients
   - Manages session handles
   - Provides API for query execution

3. **Query Compiler**
   - Parses HiveQL queries
   - Semantic analysis
   - Generates execution plan

4. **Execution Engine**
   - Executes compiled queries
   - Supports multiple engines (MapReduce, Tez, Spark)

5. **Metastore**
   - Stores metadata about tables and partitions
   - Schema information
   - Location of data files

### Q5: What is Hive Metastore and why is it important?
**Answer:**
**Hive Metastore:**
Central repository storing metadata about Hive tables, partitions, columns, and their data types.

**Components:**
- **Metastore Service**: Thrift service providing metadata access
- **Metastore Database**: Stores actual metadata (MySQL, PostgreSQL, etc.)
- **Metastore Client**: Libraries for accessing metadata

**Importance:**
- Schema management and validation
- Query optimization and planning
- Security and access control
- Data lineage and governance
- Integration with other tools

**Configuration:**
```xml
<property>
    <name>javax.jdo.option.ConnectionURL</name>
    <value>jdbc:mysql://localhost:3306/hive_metastore</value>
</property>

<property>
    <name>javax.jdo.option.ConnectionDriverName</name>
    <value>com.mysql.jdbc.Driver</value>
</property>
```

### Q6: Explain different modes of Hive Metastore
**Answer:**
**Hive Metastore Modes:**

1. **Embedded Mode**
   - Metastore runs in same JVM as Hive service
   - Uses embedded Derby database
   - Single user access only
   - Good for testing/development

2. **Local Mode**
   - Metastore runs in same JVM as Hive service
   - Uses external database (MySQL, PostgreSQL)
   - Multiple Hive sessions can connect
   - Better than embedded for development

3. **Remote Mode**
   - Metastore runs as separate service
   - Multiple Hive services can connect
   - Better scalability and security
   - Production recommended setup

**Remote Mode Configuration:**
```xml
<property>
    <name>hive.metastore.uris</name>
    <value>thrift://metastore-server:9083</value>
</property>
```

---

## 📝 HiveQL (Hive Query Language)

### Q7: Explain HiveQL syntax and key differences from standard SQL
**Answer:**
**HiveQL Features:**
- SQL-like syntax with Hadoop-specific extensions
- Support for complex data types (arrays, maps, structs)
- Built-in functions for data processing
- Custom serialization/deserialization

**Key Differences from SQL:**

1. **Data Types:**
```sql
-- Complex data types
CREATE TABLE users (
    id INT,
    name STRING,
    addresses ARRAY<STRING>,
    properties MAP<STRING, STRING>,
    contact STRUCT<email:STRING, phone:STRING>
);
```

2. **Table Creation:**
```sql
-- External table with custom format
CREATE EXTERNAL TABLE web_logs (
    ip STRING,
    timestamp STRING,
    url STRING
) ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe'
WITH SERDEPROPERTIES (
    "input.regex" = "([^ ]*) ([^ ]*) ([^ ]*)"
)
LOCATION '/data/weblogs/';
```

3. **Partitioning:**
```sql
-- Partitioned table
CREATE TABLE sales (
    product_id INT,
    amount DECIMAL(10,2)
) PARTITIONED BY (year INT, month INT);
```

### Q8: What are the different types of tables in Hive?
**Answer:**
**Hive Table Types:**

1. **Managed Tables (Internal Tables)**
   - Hive manages both metadata and data
   - Data stored in Hive warehouse directory
   - DROP TABLE deletes both metadata and data

```sql
CREATE TABLE employees (
    id INT,
    name STRING,
    salary DECIMAL(10,2)
) STORED AS PARQUET;
```

2. **External Tables**
   - Hive manages only metadata
   - Data stored in external location
   - DROP TABLE deletes only metadata

```sql
CREATE EXTERNAL TABLE external_logs (
    timestamp STRING,
    level STRING,
    message STRING
) LOCATION '/external/logs/';
```

3. **Temporary Tables**
   - Session-specific tables
   - Automatically dropped at session end
   - Not visible to other sessions

```sql
CREATE TEMPORARY TABLE temp_results AS
SELECT * FROM sales WHERE amount > 1000;
```

**Comparison:**
| Feature | Managed | External | Temporary |
|---------|---------|----------|-----------|
| Data Management | Hive | User | Session |
| DROP Behavior | Deletes data | Keeps data | Session end |
| Sharing | Global | Global | Session only |

### Q9: Explain Hive joins and their types
**Answer:**
**Hive Join Types:**

1. **Inner Join:**
```sql
SELECT c.name, o.amount
FROM customers c
JOIN orders o ON c.id = o.customer_id;
```

2. **Left/Right Outer Join:**
```sql
SELECT c.name, o.amount
FROM customers c
LEFT OUTER JOIN orders o ON c.id = o.customer_id;
```

3. **Full Outer Join:**
```sql
SELECT c.name, o.amount
FROM customers c
FULL OUTER JOIN orders o ON c.id = o.customer_id;
```

4. **Map-side Join (Broadcast Join):**
```sql
-- For small tables
SELECT /*+ MAPJOIN(small_table) */ *
FROM large_table l
JOIN small_table s ON l.id = s.id;
```

5. **Bucket Map Join:**
```sql
-- For bucketed tables
SET hive.auto.convert.join = true;
SET hive.optimize.bucketmapjoin = true;
```

**Join Optimization:**
- Use map-side joins for small tables
- Bucket tables for efficient joins
- Sort-merge bucket joins for large tables
- Proper join order (largest table last)

---

## 📊 Data Types & File Formats

### Q10: What are the data types supported by Hive?
**Answer:**
**Hive Data Types:**

**Primitive Types:**
```sql
-- Numeric types
TINYINT, SMALLINT, INT, BIGINT
FLOAT, DOUBLE, DECIMAL

-- String types
STRING, VARCHAR(n), CHAR(n)

-- Date/Time types
DATE, TIMESTAMP

-- Boolean
BOOLEAN

-- Binary
BINARY
```

**Complex Types:**
```sql
-- Array
ARRAY<data_type>

-- Map
MAP<key_type, value_type>

-- Struct
STRUCT<field_name:data_type, ...>

-- Union (deprecated)
UNIONTYPE<data_type, data_type, ...>
```

**Example Usage:**
```sql
CREATE TABLE complex_data (
    id INT,
    tags ARRAY<STRING>,
    properties MAP<STRING, STRING>,
    address STRUCT<street:STRING, city:STRING, zip:STRING>
);

-- Accessing complex data
SELECT 
    id,
    tags[0] as first_tag,
    properties['color'] as color,
    address.city as city
FROM complex_data;
```

### Q11: Explain different file formats supported by Hive
**Answer:**
**Hive File Formats:**

1. **Text File (Default)**
```sql
CREATE TABLE text_table (
    id INT,
    name STRING
) STORED AS TEXTFILE;
```

2. **Sequence File**
```sql
CREATE TABLE seq_table (
    id INT,
    name STRING
) STORED AS SEQUENCEFILE;
```

3. **RC File (Record Columnar)**
```sql
CREATE TABLE rc_table (
    id INT,
    name STRING
) STORED AS RCFILE;
```

4. **ORC (Optimized Row Columnar)**
```sql
CREATE TABLE orc_table (
    id INT,
    name STRING
) STORED AS ORC
TBLPROPERTIES ("orc.compress"="SNAPPY");
```

5. **Parquet**
```sql
CREATE TABLE parquet_table (
    id INT,
    name STRING
) STORED AS PARQUET;
```

6. **Avro**
```sql
CREATE TABLE avro_table
STORED AS AVRO
TBLPROPERTIES (
    'avro.schema.literal'='{
        "type":"record",
        "name":"User",
        "fields":[
            {"name":"id","type":"int"},
            {"name":"name","type":"string"}
        ]
    }'
);
```

**Format Comparison:**
| Format | Compression | Query Performance | Storage Efficiency |
|--------|-------------|-------------------|-------------------|
| TextFile | Good | Poor | Poor |
| SequenceFile | Good | Fair | Fair |
| RCFile | Good | Good | Good |
| ORC | Excellent | Excellent | Excellent |
| Parquet | Excellent | Excellent | Excellent |

---

## 🗂️ Partitioning & Bucketing

### Q12: Explain Hive partitioning and its benefits
**Answer:**
**Hive Partitioning:**
Dividing large tables into smaller, manageable parts based on column values.

**Benefits:**
- Faster query performance
- Reduced data scanning
- Parallel processing
- Better resource utilization
- Easier data management

**Static Partitioning:**
```sql
-- Create partitioned table
CREATE TABLE sales (
    product_id INT,
    amount DECIMAL(10,2),
    customer_id INT
) PARTITIONED BY (year INT, month INT);

-- Insert data into specific partition
INSERT INTO TABLE sales PARTITION (year=2023, month=12)
SELECT product_id, amount, customer_id
FROM raw_sales
WHERE sale_date >= '2023-12-01' AND sale_date < '2024-01-01';
```

**Dynamic Partitioning:**
```sql
-- Enable dynamic partitioning
SET hive.exec.dynamic.partition = true;
SET hive.exec.dynamic.partition.mode = nonstrict;

-- Insert with dynamic partitioning
INSERT INTO TABLE sales PARTITION (year, month)
SELECT product_id, amount, customer_id, 
       YEAR(sale_date), MONTH(sale_date)
FROM raw_sales;
```

**Best Practices:**
- Choose partition columns with low cardinality
- Avoid over-partitioning (too many small partitions)
- Use date-based partitioning for time-series data
- Regular partition maintenance

### Q13: What is bucketing in Hive and when to use it?
**Answer:**
**Hive Bucketing:**
Dividing data within partitions into fixed number of buckets based on hash function.

**Benefits:**
- Efficient sampling
- Faster joins on bucketed columns
- Better data distribution
- Improved query performance

**Creating Bucketed Table:**
```sql
CREATE TABLE bucketed_users (
    id INT,
    name STRING,
    email STRING
) CLUSTERED BY (id) INTO 10 BUCKETS
STORED AS ORC;

-- Enable bucketing
SET hive.enforce.bucketing = true;

INSERT INTO TABLE bucketed_users
SELECT id, name, email FROM users;
```

**Bucket Map Join:**
```sql
-- Optimize joins between bucketed tables
SET hive.auto.convert.join = true;
SET hive.optimize.bucketmapjoin = true;

SELECT u.name, o.amount
FROM bucketed_users u
JOIN bucketed_orders o ON u.id = o.user_id;
```

**When to Use Bucketing:**
- Frequent joins on specific columns
- Need for efficient sampling
- Large tables with skewed data
- Performance optimization for specific queries

**Bucketing vs Partitioning:**
| Aspect | Partitioning | Bucketing |
|--------|--------------|-----------|
| Purpose | Reduce data scanning | Improve joins/sampling |
| Directory Structure | Separate directories | Files within partition |
| Number of Parts | Variable | Fixed |
| Use Case | Time-based queries | Join optimization |

---

## ⚡ Performance Optimization

### Q14: What are the key performance optimization techniques in Hive?
**Answer:**
**Hive Performance Optimization Techniques:**

1. **File Format Optimization:**
```sql
-- Use columnar formats
CREATE TABLE optimized_table (
    id INT,
    name STRING,
    amount DECIMAL(10,2)
) STORED AS ORC
TBLPROPERTIES (
    "orc.compress"="SNAPPY",
    "orc.stripe.size"="268435456"
);
```

2. **Partitioning and Bucketing:**
```sql
-- Partition by frequently filtered columns
CREATE TABLE partitioned_sales (
    product_id INT,
    amount DECIMAL(10,2)
) PARTITIONED BY (year INT, month INT)
CLUSTERED BY (product_id) INTO 10 BUCKETS
STORED AS ORC;
```

3. **Query Optimization:**
```sql
-- Use appropriate execution engine
SET hive.execution.engine = tez;

-- Enable vectorization
SET hive.vectorized.execution.enabled = true;

-- Cost-based optimization
SET hive.cbo.enable = true;
SET hive.compute.query.using.stats = true;
```

4. **Join Optimization:**
```sql
-- Map-side join for small tables
SELECT /*+ MAPJOIN(small_table) */ *
FROM large_table l
JOIN small_table s ON l.id = s.id;

-- Sort-merge bucket join
SET hive.auto.convert.sortmerge.join = true;
SET hive.optimize.bucketmapjoin.sortedmerge = true;
```

5. **Compression:**
```sql
-- Enable compression
SET hive.exec.compress.output = true;
SET mapreduce.output.fileoutputformat.compress.codec = 
    org.apache.hadoop.io.compress.SnappyCodec;
```

### Q15: Explain Hive execution engines and their differences
**Answer:**
**Hive Execution Engines:**

1. **MapReduce (Default in older versions)**
   - Mature and stable
   - High latency due to disk I/O
   - Good for batch processing
   - Limited optimization capabilities

2. **Tez (Recommended)**
   - Directed Acyclic Graph (DAG) execution
   - In-memory processing
   - Better resource utilization
   - Faster than MapReduce

3. **Spark**
   - In-memory computing
   - Iterative algorithm support
   - Machine learning integration
   - Good for complex analytics

**Configuration:**
```sql
-- Set execution engine
SET hive.execution.engine = tez;

-- Tez-specific optimizations
SET hive.tez.container.size = 4096;
SET hive.tez.java.opts = -Xmx3276m;
```

**Performance Comparison:**
| Engine | Latency | Memory Usage | Complexity | Best For |
|--------|---------|--------------|------------|----------|
| MapReduce | High | Low | Simple | Batch ETL |
| Tez | Medium | Medium | Medium | Interactive queries |
| Spark | Low | High | High | Complex analytics |

### Q16: What is vectorization in Hive?
**Answer:**
**Hive Vectorization:**
Processing multiple rows together in batches instead of row-by-row processing.

**Benefits:**
- Improved CPU utilization
- Reduced function call overhead
- Better cache locality
- Significant performance improvement

**Enabling Vectorization:**
```sql
-- Enable vectorized execution
SET hive.vectorized.execution.enabled = true;
SET hive.vectorized.execution.reduce.enabled = true;

-- Vectorized aggregation
SET hive.vectorized.execution.reduce.groupby.enabled = true;

-- Vectorized map join
SET hive.vectorized.execution.mapjoin.native.enabled = true;
```

**Supported Operations:**
- Arithmetic operations
- Comparison operations
- Logical operations
- String functions
- Date functions
- Aggregations (SUM, COUNT, AVG, etc.)

**Requirements:**
- ORC file format
- Supported data types
- Compatible operations
- Tez execution engine (recommended)

---

## 🗄️ Hive Metastore

### Q17: How do you backup and restore Hive Metastore?
**Answer:**
**Hive Metastore Backup Strategies:**

1. **Database Backup:**
```bash
# MySQL backup
mysqldump -u hive -p hive_metastore > metastore_backup.sql

# PostgreSQL backup
pg_dump -U hive hive_metastore > metastore_backup.sql
```

2. **Schema Export:**
```bash
# Export schema using schematool
schematool -dbType mysql -info
schematool -dbType mysql -exportSchema schema_export.sql
```

3. **Automated Backup Script:**
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/metastore"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
mysqldump -u hive -p$HIVE_PASSWORD hive_metastore > \
    $BACKUP_DIR/metastore_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/metastore_$DATE.sql
```

**Restore Process:**
```bash
# Restore from backup
mysql -u hive -p hive_metastore < metastore_backup.sql

# Verify restoration
schematool -dbType mysql -info
```

### Q18: How do you handle Hive Metastore schema evolution?
**Answer:**
**Schema Evolution Strategies:**

1. **Schema Versioning:**
```bash
# Check current schema version
schematool -dbType mysql -info

# Upgrade schema
schematool -dbType mysql -upgradeSchema
```

2. **Backward Compatibility:**
```sql
-- Add new column with default value
ALTER TABLE table_name ADD COLUMNS (new_column STRING DEFAULT 'default_value');

-- Modify column type (limited support)
ALTER TABLE table_name CHANGE old_column new_column NEW_TYPE;
```

3. **Schema Evolution Best Practices:**
- Always backup before schema changes
- Test schema changes in development
- Use external tables for flexibility
- Document schema changes
- Plan for rollback scenarios

4. **Handling Data Type Changes:**
```sql
-- Create new table with updated schema
CREATE TABLE table_v2 (
    id INT,
    name STRING,
    new_field DECIMAL(10,2)  -- New field
) STORED AS PARQUET;

-- Migrate data
INSERT INTO table_v2
SELECT id, name, 0.0 as new_field
FROM table_v1;
```

---

## 🔧 User Defined Functions (UDFs)

### Q19: Explain different types of UDFs in Hive
**Answer:**
**Hive UDF Types:**

1. **UDF (User Defined Function)**
   - Takes single row as input
   - Returns single value
   - One-to-one mapping

```java
public class UpperCaseUDF extends UDF {
    public String evaluate(String input) {
        if (input == null) return null;
        return input.toUpperCase();
    }
}
```

2. **UDAF (User Defined Aggregate Function)**
   - Takes multiple rows as input
   - Returns single aggregated value
   - Many-to-one mapping

```java
public class SumUDAF extends AbstractGenericUDAFResolver {
    // Implementation for custom aggregation
}
```

3. **UDTF (User Defined Table Function)**
   - Takes single row as input
   - Returns multiple rows/columns
   - One-to-many mapping

```java
public class ExplodeUDTF extends GenericUDTF {
    public void process(Object[] args) throws HiveException {
        // Split input and forward multiple rows
    }
}
```

**Using UDFs:**
```sql
-- Register UDF
ADD JAR /path/to/udf.jar;
CREATE TEMPORARY FUNCTION upper_case AS 'com.example.UpperCaseUDF';

-- Use UDF in query
SELECT upper_case(name) FROM users;
```

### Q20: How do you create and deploy a custom UDF?
**Answer:**
**Creating Custom UDF:**

1. **Java Implementation:**
```java
package com.example.hive.udf;

import org.apache.hadoop.hive.ql.exec.UDF;
import org.apache.hadoop.io.Text;

public class StringLengthUDF extends UDF {
    public int evaluate(Text input) {
        if (input == null) {
            return 0;
        }
        return input.toString().length();
    }
}
```

2. **Build and Package:**
```xml
<!-- pom.xml -->
<dependencies>
    <dependency>
        <groupId>org.apache.hive</groupId>
        <artifactId>hive-exec</artifactId>
        <version>3.1.2</version>
    </dependency>
</dependencies>
```

```bash
# Build JAR
mvn clean package
```

3. **Deploy and Register:**
```sql
-- Add JAR to Hive classpath
ADD JAR /path/to/string-length-udf.jar;

-- Create temporary function
CREATE TEMPORARY FUNCTION string_length AS 'com.example.hive.udf.StringLengthUDF';

-- Use in query
SELECT name, string_length(name) as name_length FROM users;
```

4. **Permanent Function:**
```sql
-- Create permanent function
CREATE FUNCTION string_length AS 'com.example.hive.udf.StringLengthUDF'
USING JAR 'hdfs://path/to/string-length-udf.jar';
```

---

## 🔗 Integration & Ecosystem

### Q21: How does Hive integrate with other Hadoop ecosystem tools?
**Answer:**
**Hive Integration with Hadoop Ecosystem:**

1. **Spark Integration:**
```scala
// Spark SQL with Hive
val spark = SparkSession.builder()
    .appName("HiveIntegration")
    .enableHiveSupport()
    .getOrCreate()

// Query Hive tables
spark.sql("SELECT * FROM hive_table").show()
```

2. **HBase Integration:**
```sql
-- Create HBase-backed Hive table
CREATE TABLE hive_hbase_table (
    key STRING,
    value STRING
) STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
WITH SERDEPROPERTIES (
    "hbase.columns.mapping" = ":key,cf:value"
)
TBLPROPERTIES ("hbase.table.name" = "hbase_table");
```

3. **Kafka Integration:**
```sql
-- Create Kafka-backed table
CREATE TABLE kafka_table (
    key STRING,
    value STRING,
    topic STRING,
    partition INT,
    offset BIGINT
) STORED BY 'org.apache.hadoop.hive.kafka.KafkaStorageHandler'
TBLPROPERTIES (
    "kafka.topic" = "my_topic",
    "kafka.bootstrap.servers" = "localhost:9092"
);
```

4. **BI Tool Integration:**
```java
// JDBC connection
String url = "jdbc:hive2://hive-server:10000/default";
Connection conn = DriverManager.getConnection(url, "user", "password");
```

### Q22: Explain Hive security features
**Answer:**
**Hive Security Features:**

1. **Authentication:**
```xml
<!-- Kerberos authentication -->
<property>
    <name>hive.server2.authentication</name>
    <value>KERBEROS</value>
</property>

<property>
    <name>hive.server2.authentication.kerberos.principal</name>
    <value>hive/_HOST@REALM.COM</value>
</property>
```

2. **Authorization:**
```sql
-- SQL standard authorization
SET hive.security.authorization.enabled = true;
SET hive.security.authorization.manager = 
    org.apache.hadoop.hive.ql.security.authorization.plugin.sqlstd.SQLStdHiveAuthorizerFactory;

-- Grant permissions
GRANT SELECT ON TABLE sensitive_data TO USER analyst;
GRANT ALL ON DATABASE finance TO ROLE finance_team;
```

3. **Column-level Security:**
```sql
-- Create view with column masking
CREATE VIEW masked_users AS
SELECT 
    id,
    name,
    CASE 
        WHEN current_user() = 'admin' THEN email
        ELSE 'xxx@xxx.com'
    END as email
FROM users;
```

4. **Row-level Security:**
```sql
-- Row-level filtering
CREATE VIEW filtered_sales AS
SELECT * FROM sales
WHERE region = current_user_region();
```

5. **Encryption:**
```xml
<!-- Enable SSL -->
<property>
    <name>hive.server2.use.SSL</name>
    <value>true</value>
</property>

<!-- Transparent Data Encryption -->
<property>
    <name>hive.exec.orc.encryption.strategy</name>
    <value>PERFORMANCE</value>
</property>
```

---

## 🌟 Real-world Scenarios

### Q23: Design a data warehouse solution using Hive for e-commerce analytics
**Answer:**
**E-commerce Data Warehouse Design:**

**1. Data Architecture:**
```
Raw Data → Staging → ODS → Data Warehouse → Data Marts
```

**2. Table Design:**
```sql
-- Fact table - Sales
CREATE TABLE fact_sales (
    sale_id BIGINT,
    product_id INT,
    customer_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    discount_amount DECIMAL(10,2),
    sale_timestamp TIMESTAMP
) PARTITIONED BY (year INT, month INT, day INT)
CLUSTERED BY (product_id) INTO 10 BUCKETS
STORED AS ORC
TBLPROPERTIES ("orc.compress"="SNAPPY");

-- Dimension table - Products
CREATE TABLE dim_products (
    product_id INT,
    product_name STRING,
    category STRING,
    subcategory STRING,
    brand STRING,
    price DECIMAL(10,2),
    created_date DATE
) STORED AS ORC;

-- Dimension table - Customers
CREATE TABLE dim_customers (
    customer_id INT,
    customer_name STRING,
    email STRING,
    phone STRING,
    address STRUCT<street:STRING, city:STRING, state:STRING, zip:STRING>,
    registration_date DATE,
    customer_segment STRING
) STORED AS ORC;
```

**3. ETL Process:**
```sql
-- Daily ETL job
INSERT INTO TABLE fact_sales PARTITION (year, month, day)
SELECT 
    s.sale_id,
    s.product_id,
    s.customer_id,
    s.quantity,
    s.unit_price,
    s.total_amount,
    s.discount_amount,
    s.sale_timestamp,
    YEAR(s.sale_timestamp),
    MONTH(s.sale_timestamp),
    DAY(s.sale_timestamp)
FROM staging_sales s
WHERE s.sale_date = '${hiveconf:target_date}';
```

**4. Analytics Queries:**
```sql
-- Monthly sales report
SELECT 
    p.category,
    SUM(f.total_amount) as total_sales,
    COUNT(DISTINCT f.customer_id) as unique_customers,
    AVG(f.total_amount) as avg_order_value
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
WHERE f.year = 2023 AND f.month = 12
GROUP BY p.category
ORDER BY total_sales DESC;

-- Customer segmentation
SELECT 
    c.customer_segment,
    COUNT(*) as customer_count,
    SUM(f.total_amount) as total_spent,
    AVG(f.total_amount) as avg_spent
FROM fact_sales f
JOIN dim_customers c ON f.customer_id = c.customer_id
WHERE f.year = 2023
GROUP BY c.customer_segment;
```

### Q24: How would you optimize a slow-running Hive query?
**Answer:**
**Hive Query Optimization Process:**

**1. Query Analysis:**
```sql
-- Enable query execution plan
EXPLAIN EXTENDED
SELECT c.name, SUM(o.amount)
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE o.order_date >= '2023-01-01'
GROUP BY c.name;
```

**2. Identify Bottlenecks:**
- Large table scans
- Inefficient joins
- Data skew
- Poor partitioning
- Suboptimal file formats

**3. Optimization Techniques:**

**a) Partitioning:**
```sql
-- Partition pruning
SELECT * FROM orders
WHERE year = 2023 AND month = 12;  -- Uses partition pruning
```

**b) Join Optimization:**
```sql
-- Map-side join for small dimension tables
SELECT /*+ MAPJOIN(c) */ c.name, o.amount
FROM orders o
JOIN customers c ON o.customer_id = c.id;
```

**c) Bucketing:**
```sql
-- Create bucketed tables for efficient joins
CREATE TABLE bucketed_orders (
    order_id INT,
    customer_id INT,
    amount DECIMAL(10,2)
) CLUSTERED BY (customer_id) INTO 10 BUCKETS
STORED AS ORC;
```

**d) File Format:**
```sql
-- Convert to columnar format
CREATE TABLE optimized_orders
STORED AS ORC
TBLPROPERTIES ("orc.compress"="SNAPPY")
AS SELECT * FROM text_orders;
```

**e) Configuration Tuning:**
```sql
-- Execution engine
SET hive.execution.engine = tez;

-- Vectorization
SET hive.vectorized.execution.enabled = true;

-- Parallel execution
SET hive.exec.parallel = true;
SET hive.exec.parallel.thread.number = 8;

-- Memory optimization
SET hive.tez.container.size = 4096;
SET hive.tez.java.opts = -Xmx3276m;
```

**4. Monitoring and Validation:**
```sql
-- Compare execution times
SET hive.exec.perf.logger = org.apache.hadoop.hive.ql.log.PerfLogger;

-- Monitor resource usage
SET hive.exec.show.job.failure.debug.info = true;
```

---

## 📚 Additional Resources

### Best Practices Summary
1. **Table Design**: Use appropriate partitioning and bucketing
2. **File Formats**: Prefer ORC/Parquet for analytics
3. **Query Optimization**: Use proper join strategies and execution engines
4. **Security**: Implement authentication and authorization
5. **Monitoring**: Regular performance monitoring and optimization

### Recommended Reading
- "Programming Hive" by Edward Capriolo
- Apache Hive Official Documentation
- Hive Performance Tuning Guide

### Hands-on Practice
- Cloudera Quickstart VM
- Hortonworks Sandbox
- AWS EMR with Hive
- Azure HDInsight

---

*This comprehensive guide covers essential Hive interview questions for data engineering roles. Practice with real datasets and complex queries to master Hive concepts.*