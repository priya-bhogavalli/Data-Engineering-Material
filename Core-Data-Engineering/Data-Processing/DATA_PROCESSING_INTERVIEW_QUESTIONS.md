# Data Processing Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-50)](#basic-level-questions-1-50)
2. [Intermediate Level Questions (51-100)](#intermediate-level-questions-51-100)
3. [Advanced Level Questions (101-150)](#advanced-level-questions-101-150)
4. [Architecture & Performance (151-200)](#architecture--performance-151-200)
5. [Streaming & Real-time Processing (201-250)](#streaming--real-time-processing-201-250)
6. [Production & Operations (251-300)](#production--operations-251-300)
7. [Scenario-Based Questions (301-350)](#scenario-based-questions-301-350)

---

## Basic Level Questions (1-50)

### 1. What is the difference between batch processing and stream processing?

**Answer:** Batch and stream processing are two fundamental data processing paradigms.

#### 🎯 **Key Differences**

| Aspect | Batch Processing | Stream Processing |
|--------|------------------|-------------------|
| **Data Processing** | Large volumes at scheduled intervals | Continuous, real-time processing |
| **Latency** | High (minutes to hours) | Low (milliseconds to seconds) |
| **Data Size** | Large datasets | Small, continuous data streams |
| **Use Cases** | ETL, reporting, analytics | Real-time alerts, monitoring |
| **Complexity** | Lower | Higher |
| **Resource Usage** | Periodic high usage | Consistent moderate usage |

#### **Batch Processing Example:**
```python
# Daily sales report processing
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, count, avg

spark = SparkSession.builder.appName("DailySalesReport").getOrCreate()

# Read yesterday's transactions
daily_transactions = spark.read.parquet("s3://data/transactions/2023/12/01/")

# Aggregate data
sales_summary = daily_transactions.groupBy("product_category", "region").agg(
    sum("amount").alias("total_sales"),
    count("*").alias("transaction_count"),
    avg("amount").alias("avg_transaction")
)

# Write results
sales_summary.write.mode("overwrite").parquet("s3://reports/daily_sales/2023/12/01/")
print("Daily sales report generated")
```

#### **Stream Processing Example:**
```python
# Real-time fraud detection
from pyspark.sql import SparkSession
from pyspark.sql.functions import window, count, sum

spark = SparkSession.builder.appName("FraudDetection").getOrCreate()

# Read streaming transactions
streaming_transactions = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "transactions") \
    .load()

# Detect suspicious patterns in 5-minute windows
fraud_alerts = streaming_transactions \
    .withWatermark("timestamp", "10 minutes") \
    .groupBy(
        window("timestamp", "5 minutes"),
        "user_id"
    ).agg(
        count("*").alias("transaction_count"),
        sum("amount").alias("total_amount")
    ).filter(
        (col("transaction_count") > 10) | (col("total_amount") > 5000)
    )

# Write alerts to Kafka
query = fraud_alerts.writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "fraud_alerts") \
    .start()

print("Real-time fraud detection started")
```

### 2. What are the main components of Apache Spark?

**Answer:** Apache Spark consists of several core components that work together.

#### 🎯 **Core Components**

**1. Spark Core**
- **RDDs**: Resilient Distributed Datasets
- **Task Scheduling**: Distributes work across cluster
- **Memory Management**: Caches data in memory
- **Fault Recovery**: Automatic failure handling

**2. Spark SQL**
- **DataFrames**: Structured data processing
- **Catalyst Optimizer**: Query optimization engine
- **Data Sources**: Connect to various formats
- **Hive Integration**: Compatible with Hive metastore

**3. Spark Streaming**
- **DStreams**: Discretized streams
- **Structured Streaming**: DataFrame-based streaming
- **Windowing**: Time-based aggregations
- **Checkpointing**: Fault tolerance for streams

**4. MLlib**
- **Machine Learning**: Distributed ML algorithms
- **Feature Engineering**: Data preparation tools
- **Model Selection**: Cross-validation and tuning
- **Pipelines**: End-to-end ML workflows

**5. GraphX**
- **Graph Processing**: Distributed graph analytics
- **Graph Algorithms**: PageRank, connected components
- **Graph Builders**: Create graphs from data
- **Pregel API**: Iterative graph computations

```python
# Example using multiple Spark components
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.sql.functions import col, when

spark = SparkSession.builder.appName("SparkComponents").getOrCreate()

# Spark SQL - Read and transform data
df = spark.read.csv("customer_data.csv", header=True, inferSchema=True)
processed_df = df.withColumn("age_group", 
    when(col("age") < 30, "Young")
    .when(col("age") < 50, "Middle")
    .otherwise("Senior")
)

# MLlib - Machine learning
assembler = VectorAssembler(inputCols=["age", "income"], outputCol="features")
ml_df = assembler.transform(processed_df)

lr = LogisticRegression(featuresCol="features", labelCol="churn")
model = lr.fit(ml_df)

print(f"Model accuracy: {model.summary.accuracy:.3f}")
```

### 3. What is Apache Kafka and what are its key features?

**Answer:** Apache Kafka is a distributed streaming platform for building real-time data pipelines.

#### 🎯 **Key Features**

**1. High Throughput**
- Handle millions of messages per second
- Horizontal scaling across multiple brokers
- Efficient binary protocol

**2. Durability**
- Messages persisted to disk
- Configurable replication factor
- Fault-tolerant design

**3. Scalability**
- Add brokers without downtime
- Partition topics for parallelism
- Consumer groups for load balancing

**4. Real-time Processing**
- Low-latency message delivery
- Stream processing capabilities
- Event-driven architecture

#### **Kafka Architecture Example:**
```python
# Kafka Producer
from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: k.encode('utf-8') if k else None
)

# Send messages
for i in range(100):
    message = {
        'user_id': f'user_{i}',
        'event_type': 'page_view',
        'timestamp': int(time.time()),
        'page': f'/page_{i % 10}'
    }
    
    producer.send('user_events', key=f'user_{i}', value=message)
    print(f"Sent message {i}")

producer.flush()
```

```python
# Kafka Consumer
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'user_events',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id='analytics_group',
    auto_offset_reset='earliest'
)

# Process messages
for message in consumer:
    event = message.value
    print(f"Processing event: {event['event_type']} for {event['user_id']}")
    
    # Process the event (e.g., update analytics)
    if event['event_type'] == 'page_view':
        # Update page view counters
        pass
```

### 4. What is the difference between ETL and ELT?

**Answer:** ETL and ELT are two different approaches to data integration.

#### 🎯 **Key Differences**

| Aspect | ETL (Extract, Transform, Load) | ELT (Extract, Load, Transform) |
|--------|--------------------------------|--------------------------------|
| **Process Order** | Transform before loading | Transform after loading |
| **Transformation Location** | Separate processing engine | Target data warehouse |
| **Data Storage** | Processed data only | Raw + processed data |
| **Flexibility** | Less flexible | More flexible |
| **Performance** | Good for complex transforms | Better for large volumes |
| **Cost** | Higher processing costs | Lower processing costs |

#### **ETL Example:**
```python
# Traditional ETL with Spark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, regexp_replace

spark = SparkSession.builder.appName("ETL_Pipeline").getOrCreate()

# Extract
raw_data = spark.read.csv("s3://raw-data/customer_data.csv", header=True)

# Transform
cleaned_data = raw_data \
    .filter(col("email").isNotNull()) \
    .withColumn("phone_clean", regexp_replace(col("phone"), "[^0-9]", "")) \
    .withColumn("age_group", 
        when(col("age") < 25, "Young")
        .when(col("age") < 45, "Adult")
        .otherwise("Senior")
    ) \
    .withColumn("email_domain", 
        regexp_extract(col("email"), "@(.+)", 1)
    )

# Load
cleaned_data.write \
    .mode("overwrite") \
    .parquet("s3://processed-data/customers/")

print("ETL pipeline completed")
```

#### **ELT Example:**
```sql
-- ELT with Snowflake/BigQuery
-- Extract & Load (raw data loaded first)
COPY INTO raw_customers
FROM 's3://raw-data/customer_data.csv'
FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1);

-- Transform (in the warehouse)
CREATE OR REPLACE TABLE processed_customers AS
SELECT 
    customer_id,
    email,
    REGEXP_REPLACE(phone, '[^0-9]', '') as phone_clean,
    CASE 
        WHEN age < 25 THEN 'Young'
        WHEN age < 45 THEN 'Adult'
        ELSE 'Senior'
    END as age_group,
    SPLIT_PART(email, '@', 2) as email_domain,
    current_timestamp() as processed_at
FROM raw_customers
WHERE email IS NOT NULL;
```

### 5. What is Apache Airflow and how does it work?

**Answer:** Apache Airflow is a platform to programmatically author, schedule, and monitor workflows.

#### 🎯 **Core Concepts**

**1. DAG (Directed Acyclic Graph)**
- Workflow definition
- Task dependencies
- Scheduling configuration

**2. Operators**
- Define what gets executed
- Built-in and custom operators
- Task templates

**3. Tasks**
- Instances of operators
- Execution units
- State management

**4. Scheduler**
- Triggers task execution
- Manages dependencies
- Handles retries

#### **Airflow DAG Example:**
```python
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

# Default arguments
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

# Create DAG
dag = DAG(
    'daily_etl_pipeline',
    default_args=default_args,
    description='Daily ETL pipeline for sales data',
    schedule_interval='@daily',
    catchup=False,
    tags=['etl', 'sales']
)

def extract_sales_data(**context):
    """Extract sales data from source systems"""
    execution_date = context['execution_date']
    print(f"Extracting sales data for {execution_date}")
    
    # Extract logic here
    return f"Extracted data for {execution_date}"

def transform_sales_data(**context):
    """Transform extracted sales data"""
    print("Transforming sales data")
    
    # Transformation logic here
    return "Data transformed successfully"

def validate_data_quality(**context):
    """Validate data quality"""
    print("Validating data quality")
    
    # Quality checks here
    return "Data quality validated"

# Define tasks
extract_task = PythonOperator(
    task_id='extract_sales_data',
    python_callable=extract_sales_data,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform_sales_data',
    python_callable=transform_sales_data,
    dag=dag
)

quality_check_task = PythonOperator(
    task_id='validate_data_quality',
    python_callable=validate_data_quality,
    dag=dag
)

load_task = PostgresOperator(
    task_id='load_to_warehouse',
    postgres_conn_id='warehouse_db',
    sql="""
        INSERT INTO sales_summary 
        SELECT * FROM staging_sales 
        WHERE date = '{{ ds }}'
    """,
    dag=dag
)

cleanup_task = BashOperator(
    task_id='cleanup_temp_files',
    bash_command='rm -rf /tmp/sales_{{ ds }}/*',
    dag=dag
)

# Set dependencies
extract_task >> transform_task >> quality_check_task >> load_task >> cleanup_task
```

### 6. What is Snowflake and what are its key advantages?

**Answer:** Snowflake is a cloud-native data warehouse with unique architecture separating compute and storage.

#### 🎯 **Key Advantages**

**1. Separation of Compute and Storage**
- Independent scaling
- Pay for what you use
- Multiple compute clusters

**2. Multi-Cloud Support**
- AWS, Azure, Google Cloud
- Cross-cloud data sharing
- Avoid vendor lock-in

**3. Zero Management**
- No infrastructure to manage
- Automatic scaling
- Built-in optimization

**4. Advanced Features**
- Time Travel (query historical data)
- Zero-copy cloning
- Data sharing
- Semi-structured data support

#### **Snowflake Examples:**
```sql
-- Create warehouse with auto-scaling
CREATE WAREHOUSE analytics_wh WITH
    WAREHOUSE_SIZE = 'MEDIUM'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 5
    SCALING_POLICY = 'STANDARD';

-- Create database and schema
CREATE DATABASE sales_analytics;
CREATE SCHEMA sales_analytics.reporting;

-- Create table with clustering
CREATE TABLE sales_analytics.reporting.daily_sales (
    sale_date DATE,
    product_id STRING,
    customer_id STRING,
    amount NUMBER(10,2),
    region STRING
) CLUSTER BY (sale_date, region);

-- Time Travel query (query data from 1 hour ago)
SELECT * FROM daily_sales 
AT (OFFSET => -3600);

-- Zero-copy clone
CREATE TABLE daily_sales_backup 
CLONE daily_sales;

-- Semi-structured data processing
SELECT 
    customer_id,
    profile:name::STRING as customer_name,
    profile:preferences[0]::STRING as top_preference
FROM customer_profiles;
```

### 7. What is DBT and how does it fit in the modern data stack?

**Answer:** DBT (Data Build Tool) is a transformation tool that enables data teams to transform data in their warehouse using SQL.

#### 🎯 **Key Features**

**1. SQL-Based Transformations**
- Write transformations in SQL
- Version control for analytics code
- Modular and reusable code

**2. Testing and Documentation**
- Built-in data quality tests
- Automatic documentation generation
- Data lineage visualization

**3. Incremental Processing**
- Process only new/changed data
- Efficient for large datasets
- Configurable strategies

#### **DBT Model Example:**
```sql
-- models/staging/stg_orders.sql
{{ config(materialized='view') }}

SELECT 
    order_id,
    customer_id,
    order_date,
    status,
    CAST(amount AS DECIMAL(10,2)) as amount,
    UPPER(TRIM(region)) as region,
    created_at,
    updated_at
FROM {{ source('raw_data', 'orders') }}
WHERE order_date >= '2023-01-01'
```

```sql
-- models/marts/customer_metrics.sql
{{ config(
    materialized='table',
    indexes=[
      {'columns': ['customer_id'], 'type': 'btree'},
    ]
) }}

WITH customer_orders AS (
    SELECT 
        customer_id,
        COUNT(*) as total_orders,
        SUM(amount) as total_spent,
        AVG(amount) as avg_order_value,
        MIN(order_date) as first_order_date,
        MAX(order_date) as last_order_date
    FROM {{ ref('stg_orders') }}
    WHERE status = 'completed'
    GROUP BY customer_id
),

customer_segments AS (
    SELECT 
        *,
        CASE 
            WHEN total_spent >= 1000 THEN 'High Value'
            WHEN total_spent >= 500 THEN 'Medium Value'
            ELSE 'Low Value'
        END as customer_segment,
        DATEDIFF('day', first_order_date, last_order_date) as customer_lifetime_days
    FROM customer_orders
)

SELECT * FROM customer_segments
```

```yaml
# models/schema.yml
version: 2

models:
  - name: customer_metrics
    description: "Customer metrics and segmentation"
    columns:
      - name: customer_id
        description: "Unique customer identifier"
        tests:
          - unique
          - not_null
      - name: total_spent
        description: "Total amount spent by customer"
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
      - name: customer_segment
        description: "Customer value segment"
        tests:
          - accepted_values:
              values: ['High Value', 'Medium Value', 'Low Value']
```

### 8. What are the different types of data processing architectures?

**Answer:** There are several architectural patterns for data processing systems.

#### 🎯 **Architecture Types**

**1. Lambda Architecture**
- **Batch Layer**: Historical data processing
- **Speed Layer**: Real-time processing
- **Serving Layer**: Query interface

**Benefits:**
- Fault tolerance
- Low latency + high throughput
- Handles both batch and stream

**Challenges:**
- Complex to maintain
- Code duplication
- Data synchronization

**2. Kappa Architecture**
- **Stream-only processing**
- **Reprocessing through replay**
- **Simplified architecture**

**Benefits:**
- Single codebase
- Simpler to maintain
- Real-time by default

**Challenges:**
- Stream processing complexity
- Reprocessing overhead
- Storage requirements

**3. Modern Data Stack**
- **Ingestion**: Fivetran, Airbyte
- **Storage**: Snowflake, BigQuery
- **Transformation**: DBT
- **Orchestration**: Airflow
- **Visualization**: Tableau, Looker

**Benefits:**
- Best-of-breed tools
- Cloud-native
- Easy to scale

**4. Data Mesh**
- **Domain-oriented**
- **Data as a product**
- **Self-serve infrastructure**
- **Federated governance**

### 9. What is the difference between OLTP and OLAP systems?

**Answer:** OLTP and OLAP serve different purposes in data processing.

#### 🎯 **Key Differences**

| Aspect | OLTP (Online Transaction Processing) | OLAP (Online Analytical Processing) |
|--------|--------------------------------------|-------------------------------------|
| **Purpose** | Day-to-day operations | Business intelligence and analytics |
| **Data** | Current, detailed | Historical, aggregated |
| **Queries** | Simple, frequent | Complex, ad-hoc |
| **Users** | Many concurrent users | Fewer analytical users |
| **Response Time** | Milliseconds | Seconds to minutes |
| **Data Model** | Normalized (3NF) | Denormalized (star/snowflake) |
| **Storage** | Row-oriented | Column-oriented |

#### **OLTP Example:**
```sql
-- E-commerce transaction processing
-- Insert new order
INSERT INTO orders (customer_id, product_id, quantity, amount, order_date)
VALUES (12345, 'PROD001', 2, 99.98, CURRENT_TIMESTAMP);

-- Update inventory
UPDATE products 
SET stock_quantity = stock_quantity - 2
WHERE product_id = 'PROD001';

-- Simple lookup queries
SELECT * FROM customers WHERE customer_id = 12345;
SELECT * FROM orders WHERE order_id = 'ORD789';
```

#### **OLAP Example:**
```sql
-- Business intelligence queries
-- Sales analysis by region and time
SELECT 
    r.region_name,
    DATE_TRUNC('month', o.order_date) as month,
    SUM(o.amount) as total_sales,
    COUNT(*) as order_count,
    AVG(o.amount) as avg_order_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN regions r ON c.region_id = r.region_id
WHERE o.order_date >= '2023-01-01'
GROUP BY r.region_name, DATE_TRUNC('month', o.order_date)
ORDER BY month, total_sales DESC;

-- Customer cohort analysis
WITH customer_cohorts AS (
    SELECT 
        customer_id,
        DATE_TRUNC('month', MIN(order_date)) as cohort_month
    FROM orders
    GROUP BY customer_id
),
cohort_data AS (
    SELECT 
        c.cohort_month,
        DATE_TRUNC('month', o.order_date) as order_month,
        COUNT(DISTINCT o.customer_id) as customers
    FROM customer_cohorts c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.cohort_month, DATE_TRUNC('month', o.order_date)
)
SELECT * FROM cohort_data
ORDER BY cohort_month, order_month;
```

### 10. What is data partitioning and why is it important?

**Answer:** Data partitioning divides large datasets into smaller, manageable chunks for better performance and scalability.

#### 🎯 **Types of Partitioning**

**1. Range Partitioning**
- Based on value ranges
- Common for dates/timestamps
- Easy to understand and maintain

**2. Hash Partitioning**
- Based on hash function
- Even distribution
- Good for parallel processing

**3. List Partitioning**
- Based on predefined lists
- Useful for categorical data
- Manual control over distribution

**4. Composite Partitioning**
- Combination of methods
- Multi-level partitioning
- Fine-grained control

#### **Partitioning Examples:**

**Spark Partitioning:**
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month

spark = SparkSession.builder.appName("PartitioningExample").getOrCreate()

# Read large dataset
df = spark.read.parquet("s3://data-lake/transactions/")

# Range partitioning by date
df_partitioned = df.repartition(
    year(col("transaction_date")),
    month(col("transaction_date"))
)

# Write with partitioning
df_partitioned.write \
    .partitionBy("year", "month") \
    .mode("overwrite") \
    .parquet("s3://data-lake/partitioned_transactions/")

# Hash partitioning for joins
df_hash_partitioned = df.repartition(200, col("customer_id"))

# Check partition distribution
partition_counts = df_hash_partitioned.rdd.mapPartitions(
    lambda iterator: [sum(1 for _ in iterator)]
).collect()

print(f"Partition distribution: {partition_counts}")
```

**Database Partitioning:**
```sql
-- PostgreSQL range partitioning
CREATE TABLE sales (
    id SERIAL,
    sale_date DATE,
    amount DECIMAL(10,2),
    customer_id INTEGER
) PARTITION BY RANGE (sale_date);

-- Create partitions for each quarter
CREATE TABLE sales_2023_q1 PARTITION OF sales
    FOR VALUES FROM ('2023-01-01') TO ('2023-04-01');

CREATE TABLE sales_2023_q2 PARTITION OF sales
    FOR VALUES FROM ('2023-04-01') TO ('2023-07-01');

-- Queries automatically use appropriate partitions
SELECT * FROM sales 
WHERE sale_date BETWEEN '2023-02-01' AND '2023-02-28';
```

**Benefits of Partitioning:**
- **Query Performance**: Partition pruning eliminates irrelevant data
- **Parallel Processing**: Multiple partitions processed simultaneously
- **Maintenance**: Easier to manage smaller chunks
- **Storage Optimization**: Compress/archive old partitions
- **Scalability**: Add new partitions as data grows

---

### 11. What is Apache Flink and how does it differ from Spark Streaming?

**Answer:** Apache Flink is a stream processing framework designed for low-latency, high-throughput data processing.

#### 🎯 **Key Differences**

| Aspect | Apache Flink | Spark Streaming |
|--------|--------------|------------------|
| **Processing Model** | True streaming | Micro-batching |
| **Latency** | Sub-second | Seconds |
| **State Management** | Native stateful | RDD-based |
| **Event Time** | Built-in support | Limited support |
| **Backpressure** | Automatic | Manual tuning |
| **Exactly-Once** | Native support | Requires configuration |

### 12. What are the key components of a data pipeline?

**Answer:** A data pipeline consists of several interconnected components that move and transform data.

#### 🎯 **Core Components**

**1. Data Sources**
- Databases (OLTP systems)
- APIs and web services
- File systems and object storage
- Streaming platforms (Kafka)
- IoT devices and sensors

**2. Data Ingestion**
- Batch ingestion (scheduled loads)
- Real-time ingestion (streaming)
- Change Data Capture (CDC)
- API polling and webhooks

**3. Data Processing**
- Data validation and cleansing
- Transformations and enrichment
- Aggregations and calculations
- Data quality checks

**4. Data Storage**
- Data lakes (S3, HDFS)
- Data warehouses (Snowflake, BigQuery)
- Operational databases
- Cache layers (Redis)

**5. Data Orchestration**
- Workflow scheduling
- Dependency management
- Error handling and retries
- Monitoring and alerting

### 13. What is Change Data Capture (CDC) and why is it important?

**Answer:** CDC is a method to identify and capture changes made to data in a database and deliver those changes to downstream systems.

#### 🎯 **CDC Methods**

**1. Log-based CDC**
- Reads database transaction logs
- Captures all changes (INSERT, UPDATE, DELETE)
- Low impact on source system
- Real-time change detection

**2. Trigger-based CDC**
- Database triggers capture changes
- Writes changes to audit tables
- Higher impact on source system
- Guaranteed capture of changes

**3. Timestamp-based CDC**
- Uses timestamp columns
- Periodic polling for changes
- Simple to implement
- May miss some changes

**4. Snapshot-based CDC**
- Compares full snapshots
- Resource intensive
- Good for small tables
- Captures all changes

### 14. What are the different data storage formats and when to use each?

**Answer:** Different storage formats optimize for different use cases and access patterns.

#### 🎯 **Storage Formats Comparison**

| Format | Type | Compression | Schema Evolution | Use Case |
|--------|------|-------------|------------------|----------|
| **CSV** | Text | Poor | None | Simple data exchange |
| **JSON** | Text | Poor | Flexible | Semi-structured data |
| **Avro** | Binary | Good | Excellent | Schema evolution |
| **Parquet** | Columnar | Excellent | Good | Analytics workloads |
| **ORC** | Columnar | Excellent | Good | Hive/Hadoop ecosystems |
| **Delta Lake** | Parquet+ | Excellent | Good | ACID transactions |

### 15. What is data lineage and why is it important?

**Answer:** Data lineage tracks the flow of data from its origin through various transformations to its final destination.

#### 🎯 **Components of Data Lineage**

**1. Data Sources**
- Origin systems and databases
- File locations and formats
- API endpoints and services

**2. Transformations**
- ETL/ELT processes
- Data quality rules
- Business logic applications

**3. Data Movement**
- Pipeline execution paths
- Scheduling and dependencies
- Error handling and retries

**4. Data Destinations**
- Target systems and warehouses
- Reports and dashboards
- ML models and applications

#### **Benefits:**
- **Impact Analysis**: Understand downstream effects of changes
- **Root Cause Analysis**: Trace data quality issues to source
- **Compliance**: Meet regulatory requirements (GDPR, SOX)


### 16. What is the difference between horizontal and vertical scaling?

**Answer:** Scaling strategies for handling increased data processing demands.

#### 🎯 **Scaling Approaches**

| Aspect | Horizontal Scaling (Scale Out) | Vertical Scaling (Scale Up) |
|--------|--------------------------------|------------------------------|
| **Method** | Add more machines | Increase machine resources |
| **Cost** | Lower per unit | Higher per unit |
| **Complexity** | Higher (distributed) | Lower (single machine) |
| **Fault Tolerance** | Better | Single point of failure |
| **Scalability Limit** | Nearly unlimited | Hardware limits |
| **Examples** | Spark clusters, Kafka brokers | Bigger EC2 instances |

```python
# Horizontal scaling example - Spark cluster
spark = SparkSession.builder \
    .appName("HorizontalScaling") \
    .config("spark.executor.instances", "20") \
    .config("spark.executor.cores", "4") \
    .config("spark.executor.memory", "8g") \
    .getOrCreate()

# Process large dataset across multiple executors
large_df = spark.read.parquet("s3://big-data/transactions/")
result = large_df.groupBy("category").agg(sum("amount"))
print(f"Processed {large_df.count()} records across {spark.sparkContext.defaultParallelism} cores")
```

### 17. What are the key considerations for data quality?

**Answer:** Data quality ensures data is fit for its intended use in operations and decision-making.

#### 🎯 **Data Quality Dimensions**

**1. Completeness**
- All required data is present
- No missing critical fields
- Measure: % of non-null values

**2. Accuracy**
- Data correctly represents reality
- Values are correct and precise
- Measure: % of correct values

**3. Consistency**
- Data is uniform across systems
- Same format and standards
- Measure: % of consistent records

**4. Timeliness**
- Data is up-to-date and available when needed
- Fresh and current information
- Measure: Data freshness metrics

**5. Validity**
- Data conforms to business rules
- Follows defined formats and constraints
- Measure: % of valid records

```python
# Data quality validation example
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, isnan, when, count, sum as spark_sum

def data_quality_report(df, table_name):
    """Generate comprehensive data quality report"""
    total_records = df.count()
    quality_metrics = []
    
    for column in df.columns:
        # Completeness check
        null_count = df.filter(col(column).isNull() | isnan(col(column))).count()
        completeness = (total_records - null_count) / total_records * 100
        
        # Uniqueness check (for ID columns)
        if 'id' in column.lower():
            distinct_count = df.select(column).distinct().count()
            uniqueness = distinct_count / total_records * 100
        else:
            uniqueness = None
        
        quality_metrics.append({
            'table': table_name,
            'column': column,
            'total_records': total_records,
            'null_count': null_count,
            'completeness_pct': round(completeness, 2),
            'uniqueness_pct': round(uniqueness, 2) if uniqueness else None
        })
    
    return quality_metrics

# Usage
df = spark.read.csv("customer_data.csv", header=True, inferSchema=True)
quality_report = data_quality_report(df, "customers")

for metric in quality_report:
    print(f"Column {metric['column']}: {metric['completeness_pct']}% complete")
```

### 18. What is idempotency and why is it important in data processing?

**Answer:** Idempotency ensures that running the same operation multiple times produces the same result.

#### 🎯 **Importance in Data Processing**

**Benefits:**
- **Reliability**: Safe to retry failed operations
- **Consistency**: Prevents duplicate data
- **Recovery**: Easy to reprocess data
- **Debugging**: Reproducible results

**Implementation Strategies:**
- **Upsert Operations**: INSERT or UPDATE based on key
- **Deduplication**: Remove duplicate records
- **Checkpointing**: Track processed data
- **Atomic Operations**: All-or-nothing processing

```python
# Idempotent data processing example
from delta.tables import DeltaTable
from pyspark.sql.functions import current_timestamp, lit

def idempotent_data_load(spark, source_path, target_path, date_partition):
    """Idempotent data loading with upsert"""
    
    # Read new data
    new_data = spark.read.parquet(source_path) \
        .withColumn("load_date", lit(date_partition)) \
        .withColumn("processed_at", current_timestamp())
    
    # Check if target exists
    if DeltaTable.isDeltaTable(spark, target_path):
        # Existing table - perform merge (upsert)
        target_table = DeltaTable.forPath(spark, target_path)
        
        target_table.alias("target").merge(
            new_data.alias("source"),
            "target.id = source.id AND target.load_date = source.load_date"
        ).whenMatchedUpdateAll() \
         .whenNotMatchedInsertAll() \
         .execute()
        
        print(f"Merged data for {date_partition}")
    else:
        # New table - initial load
        new_data.write.format("delta").save(target_path)
        print(f"Created new table with data for {date_partition}")
    
    return spark.read.format("delta").load(target_path)

# Usage - can run multiple times safely
result = idempotent_data_load(
    spark, 
    "s3://raw-data/2023/12/01/", 
    "s3://processed-data/daily_sales/", 
    "2023-12-01"
)
```

### 19. What are the different types of joins and their performance characteristics?

**Answer:** Joins combine data from multiple datasets based on common keys.

#### 🎯 **Join Types**

**1. Inner Join**
- Returns matching records from both datasets
- Most restrictive
- Best performance for filtered results

**2. Left/Right Outer Join**
- Returns all records from one side + matches
- Preserves data from one dataset
- Moderate performance impact

**3. Full Outer Join**
- Returns all records from both datasets
- Most comprehensive
- Highest performance cost

**4. Cross Join**
- Cartesian product of datasets
- Rarely used in practice
- Extremely expensive

#### 🎯 **Join Strategies**

**1. Broadcast Hash Join**
- Small table broadcasted to all nodes
- Best for small dimension tables (<200MB)
- No shuffle required

**2. Sort Merge Join**
- Both datasets sorted by join key
- Good for large datasets
- Requires shuffle

**3. Hash Join**
- Build hash table from smaller dataset
- Probe with larger dataset
- Memory intensive

```python
# Join optimization examples
from pyspark.sql.functions import broadcast

# Large fact table
orders = spark.read.parquet("s3://data/orders/")  # 100M records

# Small dimension table
customers = spark.read.parquet("s3://data/customers/")  # 1M records

# Broadcast join (automatic for small tables)
result1 = orders.join(broadcast(customers), "customer_id")

# Sort merge join (for large tables)
products = spark.read.parquet("s3://data/products/")  # 10M records
result2 = orders.join(products, "product_id")

# Bucketed join (pre-partitioned data)
# orders and products bucketed by join key
bucketed_orders = spark.table("bucketed_orders")
bucketed_products = spark.table("bucketed_products")
result3 = bucketed_orders.join(bucketed_products, "product_id")  # No shuffle

print("Join optimizations applied")
```

### 20. What is data partitioning and what are the different strategies?

**Answer:** Data partitioning divides large datasets into smaller, manageable chunks for better performance.

#### 🎯 **Partitioning Strategies**

**1. Range Partitioning**
- Based on value ranges (dates, numbers)
- Easy to understand and query
- May lead to uneven distribution

**2. Hash Partitioning**
- Based on hash function of key
- Even distribution
- Good for parallel processing

**3. List Partitioning**
- Based on predefined lists of values
- Manual control over distribution
- Good for categorical data

**4. Round-Robin Partitioning**
- Distributes records evenly
- No consideration of data values
- Good for load balancing

```python
# Partitioning examples in Spark
from pyspark.sql.functions import year, month, hash

# Range partitioning by date
df = spark.read.parquet("s3://data/transactions/")

# Write with date-based partitioning
df.withColumn("year", year("transaction_date")) \
  .withColumn("month", month("transaction_date")) \
  .write \
  .partitionBy("year", "month") \
  .parquet("s3://partitioned-data/transactions/")

# Hash partitioning for joins
df_hash_partitioned = df.repartition(200, "customer_id")

# Check partition distribution
partition_counts = df_hash_partitioned.rdd.mapPartitions(
    lambda iterator: [sum(1 for _ in iterator)]
).collect()

print(f"Partition distribution: min={min(partition_counts)}, max={max(partition_counts)}")

# Optimal partition size calculation
total_size_gb = 100  # Dataset size in GB
optimal_partition_size_mb = 128  # Target partition size
optimal_partitions = int((total_size_gb * 1024) / optimal_partition_size_mb)



### 21. What is the difference between DataFrames and RDDs in Spark?

**Answer:** DataFrames and RDDs are different abstractions for distributed data in Spark.

#### 🎯 **Key Differences**

| Aspect | RDD | DataFrame |
|--------|-----|----------|
| **Abstraction Level** | Low-level | High-level |
| **Schema** | No schema | Structured schema |
| **Optimization** | Manual | Automatic (Catalyst) |
| **API** | Functional programming | SQL-like operations |
| **Performance** | Slower | Faster (optimized) |
| **Type Safety** | Compile-time (Scala/Java) | Runtime |
| **Memory Usage** | Higher overhead | Optimized (Tungsten) |

```python
# RDD example
from pyspark import SparkContext

sc = SparkContext.getOrCreate()
rdd = sc.parallelize([("Alice", 25), ("Bob", 30), ("Charlie", 35)])

# RDD transformations
filtered_rdd = rdd.filter(lambda x: x[1] > 25)
mapped_rdd = filtered_rdd.map(lambda x: (x[0], x[1], "Adult"))
result_rdd = mapped_rdd.collect()

print(f"RDD result: {result_rdd}")

# DataFrame example
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

spark = SparkSession.builder.getOrCreate()
df = spark.createDataFrame([("Alice", 25), ("Bob", 30), ("Charlie", 35)], ["name", "age"])

# DataFrame transformations
result_df = df.filter(col("age") > 25) \
              .withColumn("category", when(col("age") > 25, "Adult").otherwise("Young"))

result_df.show()
```

### 22. What are the key features of Apache Kafka?

**Answer:** Kafka is a distributed streaming platform with several key capabilities.

#### 🎯 **Core Features**

**1. High Throughput**
- Handle millions of messages per second
- Efficient binary protocol
- Batch processing capabilities

**2. Scalability**
- Horizontal scaling by adding brokers
- Topic partitioning for parallelism
- Consumer groups for load balancing

**3. Durability**
- Messages persisted to disk
- Configurable replication
- Fault-tolerant design

**4. Real-time Processing**
- Low-latency message delivery
- Stream processing with Kafka Streams
- Connect ecosystem for integration

```python
# Kafka producer with advanced configuration
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: k.encode('utf-8'),
    # Performance tuning
    batch_size=16384,
    linger_ms=10,
    compression_type='snappy',
    # Reliability
    acks='all',
    retries=3,
    max_in_flight_requests_per_connection=1
)

# Send messages with callback
def on_send_success(record_metadata):
    print(f"Message sent to {record_metadata.topic} partition {record_metadata.partition}")

def on_send_error(excp):
    print(f"Message send failed: {excp}")

# Produce messages
for i in range(1000):
    future = producer.send(
        'user-events',
        key=f'user_{i}',
        value={'user_id': i, 'event': 'page_view', 'timestamp': time.time()}
    )
    future.add_callback(on_send_success)
    future.add_errback(on_send_error)

producer.flush()
```

### 23. What is the difference between batch and micro-batch processing?

**Answer:** Different approaches to processing streaming data with varying latency and complexity trade-offs.

#### 🎯 **Processing Models**

| Aspect | Batch Processing | Micro-batch Processing | True Streaming |
|--------|------------------|------------------------|----------------|
| **Latency** | Hours/Minutes | Seconds | Milliseconds |
| **Data Size** | Large volumes | Small batches | Individual records |
| **Complexity** | Low | Medium | High |
| **Fault Tolerance** | Restart jobs | Replay batches | Checkpointing |
| **Examples** | Spark batch | Spark Streaming | Flink, Storm |

```python
# Micro-batch processing with Spark Streaming
from pyspark.sql import SparkSession
from pyspark.sql.functions import window, count, avg

spark = SparkSession.builder.appName("MicroBatch").getOrCreate()

# Read streaming data in micro-batches
streaming_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sensor-data") \
    .load()

# Process in 10-second micro-batches
windowed_avg = streaming_df \
    .withWatermark("timestamp", "30 seconds") \
    .groupBy(window("timestamp", "10 seconds")) \
    .agg(avg("temperature").alias("avg_temp"))

# Write results
query = windowed_avg.writeStream \
    .outputMode("update") \
    .format("console") \
    .trigger(processingTime='10 seconds') \
    .start()

print("Micro-batch processing started")
```

### 24. What are the different types of data warehousing schemas?

**Answer:** Data warehouse schemas organize data for optimal query performance and business understanding.

#### 🎯 **Schema Types**

**1. Star Schema**
- Central fact table surrounded by dimension tables
- Simple and intuitive
- Fast query performance
- Some data redundancy

**2. Snowflake Schema**
- Normalized dimension tables
- Reduced data redundancy
- More complex joins
- Better for storage optimization

**3. Galaxy Schema**
- Multiple fact tables sharing dimensions
- Complex but flexible
- Good for multiple business processes

```sql
-- Star Schema example
-- Fact table
CREATE TABLE fact_sales (
    sale_id BIGINT PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    product_key INT REFERENCES dim_product(product_key),
    customer_key INT REFERENCES dim_customer(customer_key),
    store_key INT REFERENCES dim_store(store_key),
    quantity INT,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(12,2)
);

-- Dimension tables
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_id VARCHAR(50),
    product_name VARCHAR(200),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100)
);

CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY,
    customer_id VARCHAR(50),
    customer_name VARCHAR(200),
    age_group VARCHAR(50),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100)
);

-- Analytical query
SELECT 
    p.category,
    c.age_group,
    SUM(f.total_amount) as total_sales,
    COUNT(*) as transaction_count
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
JOIN dim_customer c ON f.customer_key = c.customer_key
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.year = 2023
GROUP BY p.category, c.age_group
ORDER BY total_sales DESC;
```

### 25. What is data serialization and what are the common formats?

**Answer:** Data serialization converts data structures into a format for storage or transmission.

#### 🎯 **Serialization Formats**

| Format | Type | Size | Speed | Schema Evolution | Use Case |
|--------|------|------|-------|------------------|----------|
| **JSON** | Text | Large | Slow | Flexible | APIs, configuration |
| **XML** | Text | Very Large | Slow | Flexible | Legacy systems |
| **Avro** | Binary | Small | Fast | Excellent | Schema evolution |
| **Protocol Buffers** | Binary | Very Small | Very Fast | Good | High-performance APIs |
| **Parquet** | Columnar | Small | Fast | Good | Analytics |
| **MessagePack** | Binary | Small | Fast | Limited | Real-time systems |

```python
# Serialization examples
import json
import avro.schema
import avro.io
import io

# JSON serialization
data = {'name': 'John', 'age': 30, 'city': 'New York'}
json_data = json.dumps(data)
print(f"JSON size: {len(json_data)} bytes")

# Avro serialization
avro_schema = avro.schema.parse("""
{
    "type": "record",
    "name": "Person",
    "fields": [
        {"name": "name", "type": "string"},
        {"name": "age", "type": "int"},
        {"name": "city", "type": "string"}
    ]
}
""")

writer = avro.io.DatumWriter(avro_schema)
bytes_writer = io.BytesIO()
encoder = avro.io.BinaryEncoder(bytes_writer)
writer.write(data, encoder)
avro_data = bytes_writer.getvalue()
print(f"Avro size: {len(avro_data)} bytes")

# Parquet with Spark
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()
df = spark.createDataFrame([data])

# Write in different formats
df.write.mode("overwrite").json("output.json")
df.write.mode("overwrite").parquet("output.parquet")
df.write.mode("overwrite").format("avro").save("output.avro")

print("Data serialized in multiple formats")
```

### 26. What are the key principles of data governance?

**Answer:** Data governance ensures data is managed as a valuable asset with proper policies and controls.

#### 🎯 **Core Principles**

**1. Data Quality**
- Accuracy, completeness, consistency
- Validation rules and monitoring
- Data profiling and cleansing

**2. Data Security**
- Access controls and permissions
- Encryption and privacy protection
- Audit trails and compliance

**3. Data Lineage**
- Track data flow and transformations
- Impact analysis and root cause
- Documentation and metadata

**4. Data Stewardship**
- Assign data ownership
- Define roles and responsibilities
- Business and technical stewards

**5. Data Standards**
- Naming conventions
- Data formats and types
- Business definitions

### 27. What is the difference between data lakes and data warehouses?

**Answer:** Data lakes and warehouses serve different purposes in data architecture.

#### 🎯 **Key Differences**

| Aspect | Data Lake | Data Warehouse |
|--------|-----------|----------------|
| **Data Structure** | Raw, unstructured | Processed, structured |
| **Schema** | Schema-on-read | Schema-on-write |
| **Storage Cost** | Low | Higher |
| **Processing** | ELT | ETL |
| **Flexibility** | High | Lower |
| **Query Performance** | Variable | Optimized |
| **Use Cases** | Exploration, ML | Reporting, BI |

```python
# Data Lake pattern - store raw data
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

# Store raw data in data lake
raw_data = spark.read.json("api_responses/")
raw_data.write.partitionBy("date").parquet("s3://data-lake/raw/api_data/")

# Process data when needed (Schema-on-read)
processed_data = spark.read.parquet("s3://data-lake/raw/api_data/") \
    .select("user_id", "event_type", "timestamp") \
    .filter(col("event_type") == "purchase")

# Data Warehouse pattern - structured data
warehouse_data = processed_data.groupBy("user_id").agg(
    count("*").alias("purchase_count"),
    sum("amount").alias("total_spent")
)

# Store in optimized format
warehouse_data.write.mode("overwrite").parquet("s3://data-warehouse/customer_metrics/")
```

### 28. What are the different types of data processing patterns?

**Answer:** Various patterns for organizing and executing data processing workflows.

#### 🎯 **Processing Patterns**

**1. Extract-Transform-Load (ETL)**
- Transform data before loading
- Processing outside target system
- Traditional approach

**2. Extract-Load-Transform (ELT)**
- Load raw data first, transform in target
- Leverage target system's compute power
- Modern cloud approach

**3. Change Data Capture (CDC)**
- Capture and process only changes
- Real-time data synchronization
- Efficient for large datasets

**4. Event-Driven Processing**
- Process data as events occur
- Reactive and real-time
- Good for streaming architectures

### 29. What is backpressure and how do you handle it?

**Answer:** Backpressure occurs when data producers generate data faster than consumers can process it.

#### 🎯 **Handling Strategies**

**1. Rate Limiting**
- Limit producer rate
- Control data flow
- Prevent system overload

**2. Buffering**
- Queue messages temporarily
- Smooth out traffic spikes
- Risk of memory overflow

**3. Load Balancing**
- Distribute load across consumers
- Scale horizontally
- Improve throughput

**4. Circuit Breakers**
- Stop processing when overwhelmed
- Prevent cascade failures
- Allow system recovery

```python
# Backpressure handling in Kafka Streams
from kafka import KafkaConsumer
import time

consumer = KafkaConsumer(
    'high-volume-topic',
    bootstrap_servers=['localhost:9092'],
    # Backpressure configuration
    max_poll_records=100,  # Limit batch size
    fetch_max_wait_ms=500,  # Control fetch timing
    enable_auto_commit=False,  # Manual commit for flow control
    group_id='backpressure-group'
)

processing_times = []

for message in consumer:
    start_time = time.time()
    
    # Process message
    process_message(message.value)
    
    processing_time = time.time() - start_time
    processing_times.append(processing_time)
    
    # Adaptive backpressure
    if len(processing_times) > 100:
        avg_processing_time = sum(processing_times[-100:]) / 100
        
        if avg_processing_time > 0.1:  # Too slow
            # Reduce batch size or add delay
            time.sleep(0.01)
        
        processing_times = processing_times[-100:]  # Keep recent history
    
    # Manual commit for flow control
    consumer.commit()
```

### 30. What are the key metrics for monitoring data pipelines?

**Answer:** Essential metrics to track data pipeline health and performance.

#### 🎯 **Key Metrics Categories**

**1. Throughput Metrics**
- Records processed per second
- Data volume processed
- Pipeline completion time

**2. Latency Metrics**
- End-to-end processing time
- Stage-wise processing time
- Queue waiting time

**3. Quality Metrics**
- Data completeness percentage
- Data accuracy scores
- Schema validation failures

**4. Reliability Metrics**
- Pipeline success rate
- Error rates by type
- Recovery time

**5. Resource Metrics**
- CPU and memory utilization
- Storage usage
- Network I/O

```python
# Pipeline monitoring example
import time
import logging
from datetime import datetime

class PipelineMonitor:
    def __init__(self):
        self.metrics = {
            'records_processed': 0,
            'errors': 0,
            'start_time': None,
            'stage_times': {}
        }
    
    def start_pipeline(self):
        self.metrics['start_time'] = time.time()
        logging.info("Pipeline started")
    
    def track_stage(self, stage_name, records_count):
        stage_start = time.time()
        
        # Simulate processing
        time.sleep(0.1)
        
        stage_duration = time.time() - stage_start
        self.metrics['stage_times'][stage_name] = stage_duration
        self.metrics['records_processed'] += records_count
        
        logging.info(f"Stage {stage_name}: {records_count} records in {stage_duration:.2f}s")
    
    def track_error(self, error_type, error_message):
        self.metrics['errors'] += 1
        logging.error(f"Error ({error_type}): {error_message}")
    
    def get_summary(self):
        total_time = time.time() - self.metrics['start_time']
        throughput = self.metrics['records_processed'] / total_time
        
        return {
            'total_records': self.metrics['records_processed'],
            'total_time': total_time,
            'throughput': throughput,
            'error_rate': self.metrics['errors'] / self.metrics['records_processed'],
            'stage_breakdown': self.metrics['stage_times']
        }

# Usage
monitor = PipelineMonitor()
monitor.start_pipeline()

monitor.track_stage('extract', 10000)
monitor.track_stage('transform', 9500)
monitor.track_stage('load', 9500)

summary = monitor.get_summary()
print(f"Pipeline completed: {summary['throughput']:.0f} records/sec")
```

---

## Intermediate Level Questions (51-100)

### 51. How do you implement data quality validation in a streaming pipeline?

**Answer:** Streaming data quality requires real-time validation and monitoring approaches.

#### 🎯 **Streaming Quality Strategies**

**1. Schema Validation**
- Validate incoming data against expected schema
- Reject or quarantine invalid records
- Track schema evolution

**2. Business Rule Validation**
- Apply business logic in real-time
- Range checks, format validation
- Cross-field validation

**3. Statistical Monitoring**
- Track data distribution changes
- Detect anomalies and outliers
- Alert on significant deviations

**4. Completeness Checks**
- Monitor for missing data
- Track late-arriving data
- Measure data freshness

```python
# Streaming data quality validation
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, isnan, isnull, count, sum as spark_sum
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

def streaming_quality_validation(spark):
    # Define expected schema
    expected_schema = StructType([
        StructField("user_id", StringType(), False),
        StructField("event_type", StringType(), False),
        StructField("timestamp", StringType(), False),
        StructField("amount", DoubleType(), True)
    ])
    
    # Read streaming data
    streaming_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "events") \
        .load()
    
    # Parse and validate schema
    parsed_df = streaming_df.select(
        from_json(col("value").cast("string"), expected_schema).alias("data")
    ).select("data.*")
    
    # Quality validation function
    def validate_batch(batch_df, batch_id):
        if batch_df.count() > 0:
            total_records = batch_df.count()
            
            # Schema validation
            valid_records = batch_df.filter(
                col("user_id").isNotNull() & 
                col("event_type").isNotNull() & 
                col("timestamp").isNotNull()
            )
            
            # Business rule validation
            business_valid = valid_records.filter(
                (col("amount") >= 0) | col("amount").isNull()
            )
            
            # Calculate quality metrics
            schema_validity = valid_records.count() / total_records
            business_validity = business_valid.count() / total_records
            
            # Store quality metrics
            quality_metrics = spark.createDataFrame([{
                'batch_id': batch_id,
                'timestamp': datetime.now().isoformat(),
                'total_records': total_records,
                'schema_validity': schema_validity,
                'business_validity': business_validity
            }])
            
            quality_metrics.write.format("delta").mode("append") \
                .save("/quality/streaming_metrics")
            
            # Alert if quality drops below threshold
            if schema_validity < 0.95 or business_validity < 0.90:
                send_quality_alert(batch_id, schema_validity, business_validity)
    
    # Apply validation
    query = parsed_df.writeStream \
        .foreachBatch(validate_batch) \
        .outputMode("append") \
        .option("checkpointLocation", "/checkpoints/quality_validation") \
        .start()
    
    return query
```
```