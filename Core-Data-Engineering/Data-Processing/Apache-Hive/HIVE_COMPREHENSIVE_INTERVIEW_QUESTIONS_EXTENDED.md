# Apache Hive Extended Interview Questions & Answers

## 📋 Table of Contents
1. [Advanced Architecture](#advanced-architecture)
2. [Performance Optimization](#performance-optimization)
3. [Data Formats & Storage](#data-formats--storage)
4. [Security & Governance](#security--governance)
5. [Integration & Ecosystem](#integration--ecosystem)
6. [Troubleshooting & Operations](#troubleshooting--operations)
7. [Real-World Scenarios](#real-world-scenarios)

---

## Advanced Architecture

### 1. Explain Hive's Cost-Based Optimizer (CBO) and how it improves query performance.

**Answer:**
Hive's Cost-Based Optimizer uses statistics to generate optimal execution plans:

**CBO Components:**
```sql
-- Enable CBO
SET hive.cbo.enable=true;
SET hive.compute.query.using.stats=true;
SET hive.stats.fetch.column.stats=true;

-- Generate table statistics
ANALYZE TABLE sales COMPUTE STATISTICS;
ANALYZE TABLE sales COMPUTE STATISTICS FOR COLUMNS customer_id, amount, date;

-- View statistics
DESCRIBE FORMATTED sales;
SHOW TABLE EXTENDED LIKE 'sales';
```

**Statistics Collection:**
```sql
-- Automatic statistics collection
SET hive.stats.autogather=true;
SET hive.stats.column.autogather=true;

-- Manual statistics for partitioned tables
ANALYZE TABLE sales PARTITION(year=2024, month=1) COMPUTE STATISTICS;
ANALYZE TABLE sales PARTITION(year=2024, month=1) COMPUTE STATISTICS FOR COLUMNS;

-- Column statistics
ANALYZE TABLE sales COMPUTE STATISTICS FOR COLUMNS 
    customer_id, product_id, amount, order_date;
```

**CBO Benefits:**
- **Join Optimization**: Chooses optimal join order and algorithms
- **Predicate Pushdown**: Moves filters closer to data sources
- **Projection Pushdown**: Reduces columns read from storage
- **Partition Pruning**: Eliminates unnecessary partitions

### 2. How does Hive handle ACID transactions and what are the limitations?

**Answer:**
Hive supports ACID transactions for INSERT, UPDATE, DELETE operations:

**ACID Configuration:**
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

**ACID Operations:**
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

**ACID Limitations:**
- Only works with ORC file format
- Requires bucketed tables
- No support for foreign keys
- Limited concurrent writers per partition
- Compaction overhead for small frequent updates

### 3. Explain Hive's vectorization and how it improves performance.

**Answer:**
Vectorization processes data in batches rather than row-by-row:

**Enable Vectorization:**
```sql
-- Enable vectorized execution
SET hive.vectorized.execution.enabled=true;
SET hive.vectorized.execution.reduce.enabled=true;
SET hive.vectorized.execution.reduce.groupby.enabled=true;

-- Vectorized aggregation
SET hive.vectorized.groupby.checkinterval=4096;
SET hive.vectorized.groupby.flush.percent=0.1;

-- Check if query uses vectorization
EXPLAIN VECTORIZATION DETAIL
SELECT customer_id, SUM(amount), COUNT(*)
FROM sales
WHERE amount > 100
GROUP BY customer_id;
```

**Vectorization Benefits:**
```sql
-- Example: Vectorized vs Non-vectorized performance
-- Non-vectorized (row-by-row processing)
SET hive.vectorized.execution.enabled=false;
SELECT COUNT(*) FROM large_table WHERE amount > 1000; -- Slower

-- Vectorized (batch processing)
SET hive.vectorized.execution.enabled=true;
SELECT COUNT(*) FROM large_table WHERE amount > 1000; -- Faster
```

**Supported Operations:**
- Arithmetic operations (+, -, *, /)
- Comparison operations (=, <, >, <=, >=, <>)
- Logical operations (AND, OR, NOT)
- String functions (SUBSTR, CONCAT, LENGTH)
- Date functions (YEAR, MONTH, DAY)
- Aggregations (SUM, COUNT, AVG, MIN, MAX)

---

## Performance Optimization

### 4. How do you optimize Hive queries for large datasets?

**Answer:**
Multiple optimization strategies for large-scale data processing:

**Partitioning Strategy:**
```sql
-- Time-based partitioning
CREATE TABLE sales_partitioned (
    transaction_id STRING,
    customer_id INT,
    product_id INT,
    amount DECIMAL(10,2),
    transaction_time TIMESTAMP
)
PARTITIONED BY (year INT, month INT, day INT)
STORED AS PARQUET;

-- Dynamic partitioning
SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;
SET hive.exec.max.dynamic.partitions=1000;

INSERT OVERWRITE TABLE sales_partitioned PARTITION(year, month, day)
SELECT 
    transaction_id, customer_id, product_id, amount, transaction_time,
    YEAR(transaction_time) as year,
    MONTH(transaction_time) as month,
    DAY(transaction_time) as day
FROM sales_raw;
```

**Bucketing for Join Optimization:**
```sql
-- Create bucketed tables for efficient joins
CREATE TABLE customers_bucketed (
    customer_id INT,
    name STRING,
    email STRING,
    region STRING
)
CLUSTERED BY (customer_id) INTO 32 BUCKETS
STORED AS ORC;

CREATE TABLE orders_bucketed (
    order_id STRING,
    customer_id INT,
    order_date DATE,
    amount DECIMAL(10,2)
)
CLUSTERED BY (customer_id) INTO 32 BUCKETS
STORED AS ORC;

-- Efficient bucket join
SET hive.optimize.bucketmapjoin=true;
SET hive.optimize.bucketmapjoin.sortedmerge=true;

SELECT c.name, o.order_date, o.amount
FROM customers_bucketed c
JOIN orders_bucketed o ON c.customer_id = o.customer_id;
```

**Query Optimization Techniques:**
```sql
-- Use appropriate file formats
-- Parquet for analytical workloads
CREATE TABLE analytics_data (...) STORED AS PARQUET;

-- ORC for transactional workloads
CREATE TABLE transactional_data (...) 
STORED AS ORC
TBLPROPERTIES ('transactional'='true');

-- Compression
SET hive.exec.compress.output=true;
SET mapred.output.compression.codec=org.apache.hadoop.io.compress.SnappyCodec;

-- Predicate pushdown
SELECT customer_id, SUM(amount)
FROM sales
WHERE year = 2024 AND month = 1  -- Partition pruning
  AND amount > 100               -- Predicate pushdown
GROUP BY customer_id;

-- Column pruning
SELECT customer_id, amount  -- Only select needed columns
FROM sales
WHERE year = 2024;
```

### 5. Explain different join strategies in Hive and when to use each.

**Answer:**
Hive supports multiple join algorithms optimized for different scenarios:

**Map-Side Join (Broadcast Join):**
```sql
-- For small tables (< 25MB by default)
SET hive.auto.convert.join=true;
SET hive.mapjoin.smalltable.filesize=25000000;

-- Explicit map join hint
SELECT /*+ MAPJOIN(d) */ 
    s.customer_id, s.amount, d.customer_name
FROM sales s
JOIN customer_dim d ON s.customer_id = d.customer_id;

-- Check execution plan
EXPLAIN
SELECT s.customer_id, s.amount, d.customer_name
FROM sales s
JOIN customer_dim d ON s.customer_id = d.customer_id;
```

**Bucket Map Join:**
```sql
-- For bucketed tables with same bucketing column
SET hive.optimize.bucketmapjoin=true;
SET hive.optimize.bucketmapjoin.sortedmerge=true;

-- Both tables must be bucketed on join key
SELECT c.name, o.amount
FROM customers_bucketed c
JOIN orders_bucketed o ON c.customer_id = o.customer_id;
```

**Sort-Merge-Bucket Join:**
```sql
-- For large sorted bucketed tables
SET hive.optimize.bucketmapjoin=true;
SET hive.optimize.bucketmapjoin.sortedmerge=true;
SET hive.enforce.sortmergebucketmapjoin=false;

-- Tables must be sorted on join key
CREATE TABLE customers_sorted (...)
CLUSTERED BY (customer_id) SORTED BY (customer_id) INTO 32 BUCKETS;
```

**Skew Join:**
```sql
-- Handle data skew in joins
SET hive.optimize.skewjoin=true;
SET hive.skewjoin.key=100000;  -- Threshold for skewed keys

-- Hive will automatically detect and handle skewed keys
SELECT c.name, COUNT(o.order_id)
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.name;
```

### 6. How do you handle data skew in Hive queries?

**Answer:**
Data skew occurs when data is unevenly distributed, causing performance bottlenecks:

**Identify Data Skew:**
```sql
-- Check data distribution
SELECT customer_id, COUNT(*) as order_count
FROM orders
GROUP BY customer_id
ORDER BY order_count DESC
LIMIT 20;

-- Identify skewed partitions
SELECT year, month, COUNT(*) as record_count
FROM sales
GROUP BY year, month
ORDER BY record_count DESC;
```

**Skew Join Optimization:**
```sql
-- Enable skew join optimization
SET hive.optimize.skewjoin=true;
SET hive.skewjoin.key=100000;
SET hive.skewjoin.mapjoin.map.tasks=10000;

-- Hive will split skewed keys into separate tasks
SELECT c.customer_name, SUM(o.amount)
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_name;
```

**Manual Skew Handling:**
```sql
-- Two-stage aggregation for skewed GROUP BY
-- Stage 1: Add random salt
WITH salted_data AS (
    SELECT 
        customer_id,
        amount,
        CAST(RAND() * 10 AS INT) as salt
    FROM orders
),
-- Stage 2: Partial aggregation with salt
partial_agg AS (
    SELECT 
        customer_id,
        salt,
        SUM(amount) as partial_sum,
        COUNT(*) as partial_count
    FROM salted_data
    GROUP BY customer_id, salt
)
-- Stage 3: Final aggregation
SELECT 
    customer_id,
    SUM(partial_sum) as total_amount,
    SUM(partial_count) as total_orders
FROM partial_agg
GROUP BY customer_id;
```

**Bucketing for Skew Mitigation:**
```sql
-- Use more buckets for skewed data
CREATE TABLE orders_many_buckets (
    order_id STRING,
    customer_id INT,
    amount DECIMAL(10,2)
)
CLUSTERED BY (customer_id) INTO 256 BUCKETS  -- More buckets
STORED AS ORC;

-- Custom bucketing function
CREATE TABLE orders_custom_bucket (
    order_id STRING,
    customer_id INT,
    amount DECIMAL(10,2)
)
CLUSTERED BY (HASH(customer_id, order_id)) INTO 128 BUCKETS
STORED AS ORC;
```

---

## Data Formats & Storage

### 7. Compare different file formats in Hive and their use cases.

**Answer:**
Different file formats optimized for various use cases:

**Text Format:**
```sql
-- Simple text format (default)
CREATE TABLE sales_text (
    id INT,
    customer_id INT,
    amount DECIMAL(10,2)
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- Pros: Human readable, simple
-- Cons: No compression, slow queries, no schema evolution
```

**Parquet Format:**
```sql
-- Columnar format optimized for analytics
CREATE TABLE sales_parquet (
    id INT,
    customer_id INT,
    amount DECIMAL(10,2),
    order_date DATE
)
STORED AS PARQUET
TBLPROPERTIES (
    'parquet.compression'='SNAPPY',
    'parquet.block.size'='134217728'  -- 128MB
);

-- Benefits: Column pruning, predicate pushdown, compression
-- Use case: Analytical queries, data warehousing
```

**ORC Format:**
```sql
-- Optimized Row Columnar format
CREATE TABLE sales_orc (
    id INT,
    customer_id INT,
    amount DECIMAL(10,2),
    order_date DATE
)
STORED AS ORC
TBLPROPERTIES (
    'orc.compress'='ZLIB',
    'orc.stripe.size'='67108864',  -- 64MB
    'transactional'='true'
);

-- Benefits: ACID support, vectorization, bloom filters
-- Use case: Transactional workloads, frequent updates
```

**Avro Format:**
```sql
-- Schema evolution support
CREATE TABLE sales_avro (
    id INT,
    customer_id INT,
    amount DECIMAL(10,2)
)
STORED AS AVRO
TBLPROPERTIES (
    'avro.schema.literal'='{
        "type":"record",
        "name":"sales",
        "fields":[
            {"name":"id","type":"int"},
            {"name":"customer_id","type":"int"},
            {"name":"amount","type":"double"}
        ]
    }'
);

-- Benefits: Schema evolution, cross-language support
-- Use case: Data exchange, streaming ingestion
```

**Performance Comparison:**
```sql
-- Query performance test
SET hive.exec.compress.output=true;

-- Test query on different formats
SELECT customer_id, SUM(amount), COUNT(*)
FROM sales_text     -- Slowest
GROUP BY customer_id;

SELECT customer_id, SUM(amount), COUNT(*)
FROM sales_parquet  -- Fast for analytics
GROUP BY customer_id;

SELECT customer_id, SUM(amount), COUNT(*)
FROM sales_orc      -- Fast with vectorization
GROUP BY customer_id;
```

### 8. How do you implement data compression strategies in Hive?

**Answer:**
Compression reduces storage costs and improves I/O performance:

**Compression Configuration:**
```sql
-- Enable compression
SET hive.exec.compress.output=true;
SET hive.exec.compress.intermediate=true;

-- Map output compression
SET mapred.compress.map.output=true;
SET mapred.map.output.compression.codec=org.apache.hadoop.io.compress.SnappyCodec;

-- Final output compression
SET mapred.output.compression.codec=org.apache.hadoop.io.compress.GzipCodec;
```

**Format-Specific Compression:**
```sql
-- Parquet with different compression
CREATE TABLE sales_parquet_snappy (...) 
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

CREATE TABLE sales_parquet_gzip (...) 
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='GZIP');

-- ORC with compression
CREATE TABLE sales_orc_zlib (...) 
STORED AS ORC
TBLPROPERTIES ('orc.compress'='ZLIB');

CREATE TABLE sales_orc_snappy (...) 
STORED AS ORC
TBLPROPERTIES ('orc.compress'='SNAPPY');
```

**Compression Comparison:**
```sql
-- Test different compression ratios and performance
-- GZIP: High compression ratio, slower decompression
-- SNAPPY: Moderate compression, fast decompression  
-- LZO: Low compression, very fast decompression
-- ZSTD: Good balance of compression and speed

-- Benchmark query
EXPLAIN ANALYZE
SELECT COUNT(*), AVG(amount)
FROM sales_compressed
WHERE order_date >= '2024-01-01';
```

---

## Security & Governance

### 9. How do you implement row-level and column-level security in Hive?

**Answer:**
Hive provides multiple security mechanisms for fine-grained access control:

**Column-Level Security:**
```sql
-- Create view with column masking
CREATE VIEW customer_masked AS
SELECT 
    customer_id,
    name,
    CASE 
        WHEN current_user() IN ('admin', 'manager') THEN email
        ELSE CONCAT(SUBSTR(email, 1, 3), '***@***.com')
    END as email,
    CASE 
        WHEN current_user() IN ('admin', 'manager') THEN phone
        ELSE 'XXX-XXX-XXXX'
    END as phone,
    region
FROM customers;

-- Grant access to masked view
GRANT SELECT ON customer_masked TO ROLE analyst;
```

**Row-Level Security:**
```sql
-- Create security policy view
CREATE VIEW sales_filtered AS
SELECT *
FROM sales s
JOIN user_region_mapping urm ON s.region = urm.region
WHERE urm.username = current_user();

-- Users only see data from their assigned regions
GRANT SELECT ON sales_filtered TO ROLE regional_analyst;
```

**Apache Ranger Integration:**
```sql
-- Ranger policies for dynamic masking
-- Policy: Mask email column for non-admin users
-- Mask Type: Partial mask (show first 3 characters)
-- Condition: User not in admin group

-- Ranger policies for row filtering
-- Policy: Filter sales data by user region
-- Filter Expression: region IN (${USER_REGIONS})
```

**Attribute-Based Access Control:**
```sql
-- Create table with security labels
CREATE TABLE sensitive_data (
    id INT,
    customer_id INT,
    data STRING,
    classification STRING  -- 'public', 'internal', 'confidential'
)
STORED AS ORC;

-- Security view based on user clearance
CREATE VIEW data_by_clearance AS
SELECT id, customer_id, data
FROM sensitive_data
WHERE classification IN (
    CASE current_user()
        WHEN 'admin' THEN ('public', 'internal', 'confidential')
        WHEN 'analyst' THEN ('public', 'internal')
        ELSE ('public')
    END
);
```

### 10. How do you implement data lineage and auditing in Hive?

**Answer:**
Data lineage tracks data flow and transformations for compliance and debugging:

**Query-Level Lineage:**
```sql
-- Enable lineage logging
SET hive.exec.post.hooks=org.apache.hadoop.hive.ql.hooks.LineageLogger;
SET hive.querylog.enable.plan.progress=true;

-- Lineage information is captured in:
-- 1. Hive query logs
-- 2. YARN application logs  
-- 3. Custom lineage hooks
```

**Custom Lineage Hook:**
```java
public class CustomLineageHook implements ExecuteWithHookContext {
    @Override
    public void run(HookContext hookContext) throws Exception {
        QueryPlan plan = hookContext.getQueryPlan();
        
        // Extract input tables
        Set<ReadEntity> inputs = plan.getInputs();
        for (ReadEntity input : inputs) {
            if (input.getType() == Entity.Type.TABLE) {
                logLineage("INPUT", input.getTable().getDbName(), 
                          input.getTable().getTableName());
            }
        }
        
        // Extract output tables
        Set<WriteEntity> outputs = plan.getOutputs();
        for (WriteEntity output : outputs) {
            if (output.getType() == Entity.Type.TABLE) {
                logLineage("OUTPUT", output.getTable().getDbName(), 
                          output.getTable().getTableName());
            }
        }
    }
}
```

**Audit Configuration:**
```sql
-- Enable audit logging
SET hive.server2.logging.operation.enabled=true;
SET hive.server2.logging.operation.log.location=/var/log/hive/audit;

-- Audit information includes:
-- - User who executed query
-- - Query text and execution time
-- - Tables accessed
-- - Success/failure status
```

**Apache Atlas Integration:**
```properties
# Atlas configuration for metadata management
atlas.cluster.name=production
atlas.kafka.bootstrap.servers=kafka1:9092,kafka2:9092
atlas.notification.embedded=false

# Hive Atlas hook
hive.exec.post.hooks=org.apache.atlas.hive.hook.HiveHook
atlas.hook.hive.synchronous=false
atlas.hook.hive.numRetries=3
```

---

## Integration & Ecosystem

### 11. How do you integrate Hive with Apache Spark for better performance?

**Answer:**
Spark can read Hive tables and provide better performance for certain workloads:

**Spark-Hive Integration:**
```python
from pyspark.sql import SparkSession

# Create Spark session with Hive support
spark = SparkSession.builder \
    .appName("Spark-Hive Integration") \
    .config("spark.sql.warehouse.dir", "/user/hive/warehouse") \
    .config("spark.sql.catalogImplementation", "hive") \
    .enableHiveSupport() \
    .getOrCreate()

# Read Hive table
df = spark.sql("SELECT * FROM sales WHERE year = 2024")

# Use Spark DataFrame API for complex transformations
result = df.groupBy("customer_id") \
    .agg({"amount": "sum", "order_id": "count"}) \
    .withColumnRenamed("sum(amount)", "total_amount") \
    .withColumnRenamed("count(order_id)", "order_count")

# Write back to Hive
result.write \
    .mode("overwrite") \
    .saveAsTable("customer_summary")
```

**Performance Comparison:**
```sql
-- Hive query (MapReduce engine)
SET hive.execution.engine=mr;
SELECT customer_id, SUM(amount), COUNT(*)
FROM large_sales_table
GROUP BY customer_id;

-- Hive query (Tez engine)
SET hive.execution.engine=tez;
SELECT customer_id, SUM(amount), COUNT(*)
FROM large_sales_table
GROUP BY customer_id;

-- Spark SQL (in-memory processing)
-- Generally faster for iterative algorithms and complex transformations
```

**Hybrid Architecture:**
```python
# Use Hive for data storage and cataloging
# Use Spark for complex analytics and ML

# ETL with Spark
raw_data = spark.read.table("raw_sales")
cleaned_data = raw_data.filter(col("amount") > 0) \
    .withColumn("processed_date", current_date())

# Save to Hive for reporting
cleaned_data.write.mode("append").saveAsTable("processed_sales")

# Complex analytics with Spark
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans

# Customer segmentation
features = VectorAssembler(
    inputCols=["total_amount", "order_count", "avg_order_value"],
    outputCol="features"
)

customer_features = features.transform(customer_summary)
kmeans = KMeans(k=5, seed=1)
model = kmeans.fit(customer_features)
predictions = model.transform(customer_features)

# Save results back to Hive
predictions.write.mode("overwrite").saveAsTable("customer_segments")
```

### 12. How do you implement real-time data ingestion into Hive?

**Answer:**
Real-time ingestion requires streaming technologies integrated with Hive:

**Kafka + Flume + Hive:**
```properties
# Flume configuration for Kafka to Hive
agent.sources = kafka-source
agent.sinks = hive-sink
agent.channels = memory-channel

# Kafka source
agent.sources.kafka-source.type = org.apache.flume.sink.solr.morphline.MorphlineHandlerImpl$Builder
agent.sources.kafka-source.kafka.bootstrap.servers = kafka1:9092,kafka2:9092
agent.sources.kafka-source.kafka.topics = sales-events
agent.sources.kafka-source.channels = memory-channel

# Hive sink
agent.sinks.hive-sink.type = hive
agent.sinks.hive-sink.hive.metastore = thrift://metastore:9083
agent.sinks.hive-sink.hive.database = streaming
agent.sinks.hive-sink.hive.table = sales_stream
agent.sinks.hive-sink.channel = memory-channel
```

**Spark Streaming + Hive:**
```python
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession

spark = SparkSession.builder.enableHiveSupport().getOrCreate()
ssc = StreamingContext(spark.sparkContext, 10)  # 10 second batches

# Read from Kafka
kafka_stream = KafkaUtils.createDirectStream(
    ssc,
    ['sales-topic'],
    {'metadata.broker.list': 'kafka1:9092,kafka2:9092'}
)

def process_batch(time, rdd):
    if not rdd.isEmpty():
        # Convert to DataFrame
        df = spark.read.json(rdd)
        
        # Data transformations
        processed_df = df.withColumn("processed_time", current_timestamp()) \
            .withColumn("year", year(col("order_date"))) \
            .withColumn("month", month(col("order_date")))
        
        # Append to Hive table
        processed_df.write \
            .mode("append") \
            .partitionBy("year", "month") \
            .saveAsTable("sales_streaming")

kafka_stream.foreachRDD(process_batch)
ssc.start()
ssc.awaitTermination()
```

**Delta Lake + Hive Integration:**
```python
# Use Delta Lake for ACID streaming writes
from delta.tables import DeltaTable

# Create Delta table
spark.sql("""
    CREATE TABLE sales_delta (
        order_id STRING,
        customer_id INT,
        amount DECIMAL(10,2),
        order_date DATE
    )
    USING DELTA
    PARTITIONED BY (order_date)
""")

# Streaming write to Delta
streaming_df.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/delta/checkpoints/sales") \
    .table("sales_delta") \
    .start()

# Register Delta table in Hive metastore
spark.sql("CREATE TABLE hive_sales USING DELTA LOCATION '/delta/sales'")
```

---

## Troubleshooting & Operations

### 13. How do you troubleshoot slow Hive queries?

**Answer:**
Systematic approach to identify and resolve performance issues:

**Query Analysis:**
```sql
-- Enable detailed execution plans
SET hive.explain.user=true;
SET hive.log.explain.output=true;

-- Analyze query execution plan
EXPLAIN EXTENDED
SELECT c.customer_name, SUM(o.amount)
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2024-01-01'
GROUP BY c.customer_name;

-- Check if CBO is being used
EXPLAIN CBO
SELECT customer_id, SUM(amount)
FROM orders
GROUP BY customer_id;
```

**Performance Monitoring:**
```sql
-- Enable query performance logging
SET hive.server2.logging.operation.enabled=true;
SET hive.server2.metrics.enabled=true;

-- Check query execution metrics
SET hive.exec.perf.logger=org.apache.hadoop.hive.ql.log.PerfLogger;

-- Monitor resource usage
SET hive.exec.counters.pull.interval=1000;
```

**Common Performance Issues:**
```sql
-- 1. Missing statistics
ANALYZE TABLE orders COMPUTE STATISTICS;
ANALYZE TABLE orders COMPUTE STATISTICS FOR COLUMNS;

-- 2. Inefficient joins
-- Problem: Large table joined with small table
SELECT * FROM large_table l JOIN small_table s ON l.id = s.id;

-- Solution: Use map join
SELECT /*+ MAPJOIN(s) */ * FROM large_table l JOIN small_table s ON l.id = s.id;

-- 3. Data skew
-- Problem: Uneven data distribution
SELECT customer_id, COUNT(*) FROM orders GROUP BY customer_id;

-- Solution: Use skew join
SET hive.optimize.skewjoin=true;
SET hive.skewjoin.key=100000;

-- 4. Inefficient file formats
-- Problem: Using text files for large datasets
-- Solution: Convert to ORC or Parquet
INSERT OVERWRITE TABLE orders_orc SELECT * FROM orders_text;
```

**Resource Optimization:**
```sql
-- Tune memory settings
SET hive.auto.convert.join.noconditionaltask.size=268435456;  -- 256MB
SET hive.exec.reducers.bytes.per.reducer=1073741824;         -- 1GB
SET hive.exec.reducers.max=999;

-- Optimize for specific workloads
-- For aggregation-heavy queries
SET hive.map.aggr=true;
SET hive.groupby.skewindata=true;

-- For join-heavy queries
SET hive.auto.convert.join=true;
SET hive.optimize.bucketmapjoin=true;
```

### 14. How do you manage Hive metastore and handle metadata corruption?

**Answer:**
Metastore management is critical for Hive operations:

**Metastore Backup:**
```bash
#!/bin/bash
# Backup Hive metastore database

# MySQL backup
mysqldump -u hive -p hive_metastore > metastore_backup_$(date +%Y%m%d).sql

# PostgreSQL backup
pg_dump -U hive -h localhost hive_metastore > metastore_backup_$(date +%Y%m%d).sql

# Backup metastore schema
schematool -dbType mysql -info > schema_info_$(date +%Y%m%d).txt
```

**Metastore Validation:**
```bash
# Validate metastore schema
schematool -dbType mysql -validate

# Check for inconsistencies
hive --service metatool -listFSRoot
hive --service metatool -executeJDOQL "SELECT * FROM TBLS WHERE TBL_NAME LIKE 'temp%'"

# Repair metadata inconsistencies
MSCK REPAIR TABLE sales_partitioned;

# Add missing partitions
ALTER TABLE sales_partitioned ADD PARTITION (year=2024, month=1);
```

**Metastore Recovery:**
```sql
-- Recover from backup
-- 1. Stop Hive services
-- 2. Restore database from backup
mysql -u hive -p hive_metastore < metastore_backup_20240115.sql

-- 3. Validate schema version
schematool -dbType mysql -validate

-- 4. Upgrade schema if needed
schematool -dbType mysql -upgradeSchema

-- 5. Restart Hive services
```

**Metastore Monitoring:**
```sql
-- Monitor metastore health
SELECT 
    DB_NAME,
    COUNT(*) as table_count
FROM DBS d
JOIN TBLS t ON d.DB_ID = t.DB_ID
GROUP BY DB_NAME;

-- Check for orphaned partitions
SELECT 
    t.TBL_NAME,
    COUNT(p.PART_ID) as partition_count
FROM TBLS t
LEFT JOIN PARTITIONS p ON t.TBL_ID = p.TBL_ID
GROUP BY t.TBL_NAME
HAVING COUNT(p.PART_ID) = 0;

-- Monitor metastore performance
SELECT 
    NOTIFICATION_ID,
    EVENT_TIME,
    EVENT_TYPE,
    DB_NAME,
    TBL_NAME
FROM NOTIFICATION_LOG
ORDER BY EVENT_TIME DESC
LIMIT 100;
```

---

## Real-World Scenarios

### 15. Design a complete data pipeline using Hive for a retail analytics use case.

**Answer:**
End-to-end retail analytics pipeline with Hive:

**1. Data Ingestion Layer:**
```sql
-- Raw data tables
CREATE TABLE raw_transactions (
    transaction_id STRING,
    customer_id STRING,
    product_id STRING,
    quantity INT,
    unit_price DECIMAL(10,2),
    transaction_timestamp STRING,
    store_id STRING,
    payment_method STRING
)
PARTITIONED BY (ingestion_date STRING)
STORED AS TEXTFILE
LOCATION '/data/raw/transactions/';

-- Product catalog
CREATE TABLE raw_products (
    product_id STRING,
    product_name STRING,
    category STRING,
    subcategory STRING,
    brand STRING,
    cost DECIMAL(10,2)
)
STORED AS TEXTFILE;

-- Customer data
CREATE TABLE raw_customers (
    customer_id STRING,
    first_name STRING,
    last_name STRING,
    email STRING,
    phone STRING,
    address STRING,
    city STRING,
    state STRING,
    zip_code STRING,
    registration_date STRING
)
STORED AS TEXTFILE;
```

**2. Data Cleaning and Transformation:**
```sql
-- Cleaned transactions table
CREATE TABLE clean_transactions (
    transaction_id STRING,
    customer_id STRING,
    product_id STRING,
    quantity INT,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    transaction_date DATE,
    transaction_hour INT,
    store_id STRING,
    payment_method STRING
)
PARTITIONED BY (year INT, month INT)
STORED AS ORC
TBLPROPERTIES ('transactional'='true');

-- ETL process
INSERT OVERWRITE TABLE clean_transactions PARTITION(year, month)
SELECT 
    transaction_id,
    customer_id,
    product_id,
    quantity,
    unit_price,
    quantity * unit_price as total_amount,
    CAST(SUBSTR(transaction_timestamp, 1, 10) AS DATE) as transaction_date,
    HOUR(transaction_timestamp) as transaction_hour,
    store_id,
    payment_method,
    YEAR(CAST(SUBSTR(transaction_timestamp, 1, 10) AS DATE)) as year,
    MONTH(CAST(SUBSTR(transaction_timestamp, 1, 10) AS DATE)) as month
FROM raw_transactions
WHERE transaction_id IS NOT NULL
  AND customer_id IS NOT NULL
  AND product_id IS NOT NULL
  AND quantity > 0
  AND unit_price > 0;
```

**3. Dimensional Modeling:**
```sql
-- Customer dimension (SCD Type 2)
CREATE TABLE dim_customer (
    customer_key BIGINT,
    customer_id STRING,
    first_name STRING,
    last_name STRING,
    full_name STRING,
    email STRING,
    phone STRING,
    address STRING,
    city STRING,
    state STRING,
    zip_code STRING,
    registration_date DATE,
    effective_date DATE,
    expiration_date DATE,
    is_current BOOLEAN
)
STORED AS ORC;

-- Product dimension
CREATE TABLE dim_product (
    product_key BIGINT,
    product_id STRING,
    product_name STRING,
    category STRING,
    subcategory STRING,
    brand STRING,
    cost DECIMAL(10,2),
    effective_date DATE
)
STORED AS ORC;

-- Date dimension
CREATE TABLE dim_date (
    date_key INT,
    date_value DATE,
    year INT,
    quarter INT,
    month INT,
    month_name STRING,
    day INT,
    day_of_week INT,
    day_name STRING,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN
)
STORED AS ORC;

-- Sales fact table
CREATE TABLE fact_sales (
    transaction_id STRING,
    customer_key BIGINT,
    product_key BIGINT,
    date_key INT,
    store_id STRING,
    quantity INT,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    cost_amount DECIMAL(10,2),
    profit_amount DECIMAL(10,2),
    payment_method STRING
)
PARTITIONED BY (year INT, month INT)
CLUSTERED BY (customer_key) INTO 32 BUCKETS
STORED AS ORC;
```

**4. Analytics and Reporting:**
```sql
-- Customer segmentation analysis
CREATE TABLE customer_segments AS
SELECT 
    c.customer_key,
    c.full_name,
    SUM(f.total_amount) as total_spent,
    COUNT(DISTINCT f.transaction_id) as transaction_count,
    AVG(f.total_amount) as avg_transaction_value,
    MAX(d.date_value) as last_purchase_date,
    DATEDIFF(CURRENT_DATE, MAX(d.date_value)) as days_since_last_purchase,
    CASE 
        WHEN SUM(f.total_amount) >= 10000 THEN 'VIP'
        WHEN SUM(f.total_amount) >= 5000 THEN 'Premium'
        WHEN SUM(f.total_amount) >= 1000 THEN 'Regular'
        ELSE 'Basic'
    END as customer_segment
FROM dim_customer c
JOIN fact_sales f ON c.customer_key = f.customer_key
JOIN dim_date d ON f.date_key = d.date_key
WHERE c.is_current = true
  AND d.date_value >= DATE_SUB(CURRENT_DATE, 365)
GROUP BY c.customer_key, c.full_name;

-- Product performance analysis
CREATE TABLE product_performance AS
SELECT 
    p.category,
    p.subcategory,
    p.brand,
    p.product_name,
    SUM(f.quantity) as total_quantity_sold,
    SUM(f.total_amount) as total_revenue,
    SUM(f.profit_amount) as total_profit,
    AVG(f.profit_amount / f.total_amount) as profit_margin,
    COUNT(DISTINCT f.customer_key) as unique_customers,
    RANK() OVER (PARTITION BY p.category ORDER BY SUM(f.total_amount) DESC) as revenue_rank
FROM dim_product p
JOIN fact_sales f ON p.product_key = f.product_key
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.date_value >= DATE_SUB(CURRENT_DATE, 90)
GROUP BY p.category, p.subcategory, p.brand, p.product_name;

-- Time-based sales trends
CREATE TABLE sales_trends AS
SELECT 
    d.year,
    d.month,
    d.month_name,
    SUM(f.total_amount) as monthly_revenue,
    COUNT(DISTINCT f.transaction_id) as monthly_transactions,
    COUNT(DISTINCT f.customer_key) as monthly_customers,
    AVG(f.total_amount) as avg_transaction_value,
    LAG(SUM(f.total_amount)) OVER (ORDER BY d.year, d.month) as prev_month_revenue,
    (SUM(f.total_amount) - LAG(SUM(f.total_amount)) OVER (ORDER BY d.year, d.month)) / 
    LAG(SUM(f.total_amount)) OVER (ORDER BY d.year, d.month) * 100 as revenue_growth_pct
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;
```

**5. Data Quality and Monitoring:**
```sql
-- Data quality checks
CREATE TABLE data_quality_metrics AS
SELECT 
    'transactions' as table_name,
    COUNT(*) as total_records,
    COUNT(DISTINCT transaction_id) as unique_transactions,
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) as null_customers,
    SUM(CASE WHEN product_id IS NULL THEN 1 ELSE 0 END) as null_products,
    SUM(CASE WHEN total_amount <= 0 THEN 1 ELSE 0 END) as invalid_amounts,
    MIN(transaction_date) as earliest_date,
    MAX(transaction_date) as latest_date,
    CURRENT_TIMESTAMP as check_timestamp
FROM clean_transactions
WHERE year = YEAR(CURRENT_DATE) AND month = MONTH(CURRENT_DATE);

-- Performance monitoring
CREATE TABLE query_performance_log (
    query_name STRING,
    execution_time_seconds BIGINT,
    rows_processed BIGINT,
    execution_date TIMESTAMP
)
STORED AS ORC;
```

This comprehensive retail analytics pipeline demonstrates:
- **Data ingestion** from multiple sources
- **Data cleaning** and validation
- **Dimensional modeling** for analytics
- **Customer segmentation** and behavior analysis
- **Product performance** tracking
- **Time-based trend** analysis
- **Data quality** monitoring
- **Performance** optimization techniques

---

## 🎯 Key Takeaways

1. **Performance Optimization**: Use appropriate file formats, partitioning, and bucketing
2. **Security**: Implement row-level and column-level security with proper governance
3. **Data Quality**: Establish comprehensive data validation and monitoring
4. **Integration**: Leverage Spark and other tools for enhanced capabilities
5. **Operations**: Maintain metastore health and implement proper backup strategies
6. **Real-time Processing**: Combine streaming technologies with Hive for near real-time analytics
7. **Cost Management**: Optimize storage formats and compression for cost efficiency

---

*This extended guide covers advanced Hive concepts essential for senior data engineering roles. Focus on understanding the architectural decisions, performance optimization techniques, and real-world implementation patterns.*