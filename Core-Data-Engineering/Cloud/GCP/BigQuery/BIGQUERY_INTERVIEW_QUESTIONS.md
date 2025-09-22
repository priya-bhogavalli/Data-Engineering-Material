
### Q1: What is Google BigQuery and what makes it unique?
**Answer:**
BigQuery is Google's fully managed, serverless data warehouse that enables scalable analysis over petabytes of data.

**Key Features:**
- **Serverless**: No infrastructure management
- **Columnar Storage**: Optimized for analytics
- **Massively Parallel Processing**: Distributed query execution
- **Built-in ML**: BigQuery ML for machine learning
- **Real-time Analytics**: Streaming data support
- **Standard SQL**: ANSI SQL compliance

**Unique Advantages:**
- Separation of compute and storage
- Automatic scaling and optimization
- Pay-per-query pricing model
- Integration with Google Cloud ecosystem

### Q2: How does BigQuery's architecture work?
**Answer:**
**Core Components:**
- **Dremel**: Query execution engine
- **Colossus**: Distributed storage system
- **Jupiter**: High-speed network
- **Borg**: Container orchestration

**Architecture Flow:**
```
Client → BigQuery API → Dremel (Query Engine) → Colossus (Storage)
                           ↓
                    Massively Parallel Processing
```

**Storage Model:**
- Columnar format for fast analytics
- Automatic compression and encoding
- Distributed across multiple data centers
- Immutable storage with versioning

---

## Architecture & Storage

### Q3: What is BigQuery's storage model?
**Answer:**
**Capacitor Storage Format:**
- **Columnar**: Data stored by columns, not rows
- **Compressed**: Automatic compression algorithms
- **Encrypted**: Data encrypted at rest and in transit
- **Replicated**: Multiple copies across zones

**Benefits:**
```sql
-- Efficient for analytical queries
SELECT AVG(sales_amount), COUNT(*)
FROM transactions
WHERE date >= '2024-01-01';
-- Only reads sales_amount and date columns
```

### Q4: How does BigQuery handle partitioning and clustering?
**Answer:**
**Partitioning:**
- **Time-based**: By date/timestamp columns
- **Integer Range**: By integer columns
- **Ingestion Time**: By data load time

**Clustering:**
- **Co-location**: Related data stored together
- **Up to 4 columns**: Clustering key limitation
- **Automatic Optimization**: Google manages clustering

**Example:**
```sql
-- Create partitioned and clustered table
CREATE TABLE sales_data (
  transaction_date DATE,
  customer_id STRING,
  product_category STRING,
  sales_amount NUMERIC
)
PARTITION BY transaction_date
CLUSTER BY customer_id, product_category;
```

---

## SQL & Querying

### Q5: What are BigQuery's SQL extensions and unique features?
**Answer:**
**BigQuery SQL Extensions:**
- **Array and Struct Types**: Complex data types
- **Window Functions**: Advanced analytics
- **User-Defined Functions**: Custom logic
- **Scripting**: Multi-statement scripts
- **Approximate Functions**: Fast approximate results

**Examples:**
```sql
-- Array operations
SELECT customer_id, 
       ARRAY_AGG(product_name) as purchased_products
FROM transactions
GROUP BY customer_id;

-- Struct operations
SELECT customer.name, customer.email.address
FROM customers;

-- Approximate functions
SELECT APPROX_COUNT_DISTINCT(customer_id) as unique_customers
FROM transactions;
```

### Q6: How do you optimize BigQuery queries?
**Answer:**
**Optimization Techniques:**

1. **Avoid SELECT ***:
```sql
-- Bad
SELECT * FROM large_table;

-- Good
SELECT customer_id, sales_amount FROM large_table;
```

2. **Use Partitioning Filters**:
```sql
-- Efficient - uses partition pruning
SELECT * FROM sales_data 
WHERE transaction_date = '2024-01-15';
```

3. **Optimize JOINs**:
```sql
-- Use clustering for JOIN columns
SELECT s.*, c.customer_name
FROM sales_data s
JOIN customers c ON s.customer_id = c.customer_id;
```

4. **Use Approximate Functions**:
```sql
-- Faster for large datasets
SELECT APPROX_QUANTILES(sales_amount, 100) as percentiles
FROM sales_data;
```

---

## Data Loading & Export

### Q7: What are the different ways to load data into BigQuery?
**Answer:**
**Loading Methods:**

1. **Batch Loading**:
```bash
# Using bq command-line tool
bq load --source_format=CSV dataset.table gs://bucket/data.csv schema.json
```

2. **Streaming Inserts**:
```python
from google.cloud import bigquery

client = bigquery.Client()
table = client.get_table('project.dataset.table')

rows = [
    {"name": "John", "age": 30},
    {"name": "Jane", "age": 25}
]

errors = client.insert_rows_json(table, rows)
```

3. **Data Transfer Service**:
- Scheduled transfers from external sources
- Google Ads, YouTube, etc.

4. **Dataflow Integration**:
```python
# Apache Beam pipeline
import apache_beam as beam

(p | 'Read' >> beam.io.ReadFromText('gs://bucket/input.txt')
   | 'Transform' >> beam.Map(transform_function)
   | 'Write' >> beam.io.WriteToBigQuery('project:dataset.table'))
```

### Q8: How do you export data from BigQuery?
**Answer:**
**Export Methods:**

1. **Export to Cloud Storage**:
```sql
EXPORT DATA OPTIONS(
  uri='gs://bucket/export/*.csv',
  format='CSV',
  overwrite=true
) AS
SELECT * FROM dataset.table;
```

2. **Using Client Libraries**:
```python
from google.cloud import bigquery

client = bigquery.Client()
query = "SELECT * FROM dataset.table LIMIT 1000"
df = client.query(query).to_dataframe()
```

3. **Scheduled Exports**:
- Data Transfer Service for regular exports
- Cloud Functions for custom scheduling

---

## Performance & Optimization

### Q9: How does BigQuery pricing work?
**Answer:**
**Pricing Models:**

1. **On-Demand**: Pay per TB processed
```sql
-- Check query cost before running
SELECT 
  job_id,
  total_bytes_processed / 1024 / 1024 / 1024 / 1024 as tb_processed,
  total_bytes_processed / 1024 / 1024 / 1024 / 1024 * 5 as estimated_cost_usd
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE job_id = 'your_job_id';
```

2. **Flat-Rate**: Reserved capacity
- Predictable costs for consistent workloads
- Slot-based pricing model

**Cost Optimization:**
- Use partitioning and clustering
- Avoid SELECT *
- Use approximate functions
- Cache query results

### Q10: What are BigQuery slots and how do they work?
**Answer:**
**Slots Concept:**
- **Virtual CPU**: Unit of computational capacity
- **Dynamic Allocation**: Automatically assigned
- **Shared Pool**: On-demand queries share slots
- **Reserved Slots**: Guaranteed capacity

**Slot Usage:**
```sql
-- Monitor slot usage
SELECT
  job_id,
  user_email,
  total_slot_ms,
  total_slot_ms / (1000 * 60) as slot_minutes
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY);
```

---

## Security & Access Control

### Q11: How does BigQuery handle security and access control?
**Answer:**
**Security Features:**
- **IAM Integration**: Google Cloud IAM roles
- **Column-level Security**: Restrict access to specific columns
- **Row-level Security**: Filter data based on user context
- **VPC Service Controls**: Network-level security
- **Encryption**: Automatic encryption at rest and in transit

**IAM Roles:**
```yaml
# Common BigQuery roles
- roles/bigquery.dataViewer    # Read data
- roles/bigquery.dataEditor    # Read/write data
- roles/bigquery.user          # Run queries
- roles/bigquery.admin         # Full access
```

### Q12: How do you implement row-level security in BigQuery?
**Answer:**
**Row-Level Security Setup:**

1. **Create Row Access Policy**:
```sql
CREATE ROW ACCESS POLICY regional_filter
ON dataset.sales_table
GRANT TO ('user:analyst@company.com')
FILTER USING (region = SESSION_USER());
```

2. **Column-Level Security**:
```sql
-- Create policy tag taxonomy
CREATE SCHEMA `project.taxonomy`;

-- Apply policy tags to columns
ALTER TABLE dataset.customers
ALTER COLUMN ssn SET OPTIONS (policy_tags=['projects/project/locations/us/taxonomies/taxonomy_id/policyTags/tag_id']);
```

---

## Machine Learning

### Q13: What is BigQuery ML and how do you use it?
**Answer:**
BigQuery ML enables creating and executing machine learning models using SQL.

**Supported Models:**
- Linear/Logistic Regression
- K-means Clustering
- Time Series Forecasting
- Deep Neural Networks
- AutoML Integration

**Example - Linear Regression:**
```sql
-- Create model
CREATE MODEL `dataset.sales_model`
OPTIONS(model_type='linear_reg') AS
SELECT
  advertising_spend,
  season,
  sales_amount as label
FROM `dataset.sales_data`;

-- Make predictions
SELECT *
FROM ML.PREDICT(MODEL `dataset.sales_model`,
  (SELECT advertising_spend, season FROM `dataset.new_data`));
```

### Q14: How do you evaluate BigQuery ML models?
**Answer:**
**Model Evaluation:**
```sql
-- Evaluate model performance
SELECT *
FROM ML.EVALUATE(MODEL `dataset.sales_model`,
  (SELECT advertising_spend, season, sales_amount as label
   FROM `dataset.test_data`));

-- Get model information
SELECT *
FROM ML.TRAINING_INFO(MODEL `dataset.sales_model`);

-- Feature importance
SELECT *
FROM ML.FEATURE_INFO(MODEL `dataset.sales_model`);
```

---

## Streaming & Real-time

### Q15: How does BigQuery handle streaming data?
**Answer:**
**Streaming Features:**
- **Real-time Ingestion**: Sub-second latency
- **Automatic Schema Detection**: Dynamic schema updates
- **Exactly-Once Delivery**: Deduplication support
- **DML Operations**: Real-time updates and deletes

**Streaming Insert Example:**
```python
from google.cloud import bigquery

def stream_data():
    client = bigquery.Client()
    table_id = "project.dataset.table"
    
    rows_to_insert = [
        {"timestamp": datetime.utcnow(), "user_id": "123", "event": "click"},
        {"timestamp": datetime.utcnow(), "user_id": "456", "event": "view"}
    ]
    
    errors = client.insert_rows_json(table_id, rows_to_insert)
    return len(errors) == 0
```

### Q16: How do you handle late-arriving data in BigQuery?
**Answer:**
**Late Data Strategies:**

1. **DML Operations**:
```sql
-- Update existing records
MERGE `dataset.events` T
USING `dataset.late_events` S
ON T.event_id = S.event_id
WHEN MATCHED THEN
  UPDATE SET timestamp = S.timestamp, data = S.data
WHEN NOT MATCHED THEN
  INSERT (event_id, timestamp, data) VALUES (S.event_id, S.timestamp, S.data);
```

2. **Time-based Windows**:
```sql
-- Use event time vs processing time
SELECT
  event_timestamp,
  COUNT(*) as event_count
FROM events
WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
GROUP BY event_timestamp;
```

---

## Cost Management

### Q17: How do you monitor and control BigQuery costs?
**Answer:**
**Cost Monitoring:**

1. **Query Cost Estimation**:
```sql
-- Dry run to estimate cost
SELECT
  total_bytes_processed,
  total_bytes_processed / 1024 / 1024 / 1024 / 1024 * 5 as estimated_cost_usd
FROM (
  SELECT COUNT(*) FROM `dataset.large_table`  -- DRY RUN
);
```

2. **Cost Controls**:
```sql
-- Set maximum bytes billed
SELECT *
FROM `dataset.table`
WHERE date >= '2024-01-01'
OPTIONS (maximum_bytes_billed = 1000000000);  -- 1GB limit
```

3. **Monitoring Queries**:
```sql
-- Monitor expensive queries
SELECT
  job_id,
  user_email,
  query,
  total_bytes_processed / 1024 / 1024 / 1024 as gb_processed,
  creation_time
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE total_bytes_processed > 1000000000  -- > 1GB
ORDER BY total_bytes_processed DESC;
```

---

## Integration & APIs

### Q18: How do you integrate BigQuery with other Google Cloud services?
**Answer:**
**Common Integrations:**

1. **Cloud Storage**:
```sql
-- Query external data
CREATE OR REPLACE EXTERNAL TABLE dataset.external_table
OPTIONS (
  format = 'CSV',
  uris = ['gs://bucket/data/*.csv']
);
```

2. **Dataflow**:
```python
# Dataflow to BigQuery pipeline
import apache_beam as beam

(p | 'Read from Pub/Sub' >> beam.io.ReadFromPubSub(subscription=subscription)
   | 'Parse JSON' >> beam.Map(json.loads)
   | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
       table='project:dataset.table',
       schema=schema))
```

3. **Cloud Functions**:
```python
def bigquery_trigger(event, context):
    from google.cloud import bigquery
    
    client = bigquery.Client()
    query = """
        INSERT INTO dataset.processed_data
        SELECT * FROM dataset.raw_data
        WHERE processed = FALSE
    """
    client.query(query)
```

---

## Best Practices

### Q19: What are BigQuery best practices?
**Answer:**
**Performance Best Practices:**
- Use partitioning and clustering appropriately
- Avoid SELECT * in production queries
- Use approximate functions for large datasets
- Optimize JOIN operations
- Cache frequently used query results

**Cost Optimization:**
- Monitor query costs regularly
- Use query labels for cost attribution
- Implement query cost controls
- Use materialized views for repeated computations

**Security Best Practices:**
- Implement least privilege access
- Use row-level and column-level security
- Enable audit logging
- Encrypt sensitive data
- Use VPC Service Controls

---

## Scenario-Based Questions

### Q20: How would you design a real-time analytics pipeline using BigQuery?
**Answer:**
**Architecture Design:**
```
Data Sources → Pub/Sub → Dataflow → BigQuery → Dashboard
     ↓            ↓         ↓          ↓         ↓
  Web Apps    Message     Stream    Streaming   Looker/
  Mobile      Queue       Process   Tables      Data Studio
  IoT                     Transform
```

**Implementation:**
```python
# Dataflow pipeline for real-time processing
def run_pipeline():
    pipeline_options = PipelineOptions([
        '--project=my-project',
        '--runner=DataflowRunner',
        '--streaming=true'
    ])
    
    with beam.Pipeline(options=pipeline_options) as p:
        (p | 'Read from Pub/Sub' >> beam.io.ReadFromPubSub(subscription=subscription)
           | 'Parse and Transform' >> beam.Map(transform_message)
           | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
               table='project:dataset.real_time_data',
               write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND))
```

### Q21: How would you migrate from a traditional data warehouse to BigQuery?
**Answer:**
**Migration Strategy:**

1. **Assessment Phase**:
- Analyze current data volumes and query patterns
- Identify dependencies and integrations
- Estimate costs and performance improvements

2. **Data Migration**:
```bash
# Export from source system
mysqldump --single-transaction database > export.sql

# Transform and load to BigQuery
bq load --source_format=CSV dataset.table gs://bucket/transformed_data.csv
```

3. **Query Migration**:
```sql
-- Convert proprietary SQL to BigQuery SQL
-- Traditional SQL
SELECT TOP 10 * FROM table ORDER BY date DESC;

-- BigQuery SQL
SELECT * FROM table ORDER BY date DESC LIMIT 10;
```

4. **Validation and Testing**:
- Compare query results between systems
- Performance testing and optimization
- User acceptance testing

---

## Performance Optimization (Advanced)

### Q22: What are BigQuery partitioning strategies and when to use each?
**Answer:**
**Partitioning Types:**
- **Time-unit**: Daily, monthly, yearly partitions
- **Integer range**: Numeric column partitioning
- **Ingestion time**: Based on data load time

```sql
-- Time-unit partitioning
CREATE TABLE sales_partitioned (
  transaction_date DATE,
  amount NUMERIC
)
PARTITION BY transaction_date;

-- Integer range partitioning
CREATE TABLE user_data (
  user_id INT64,
  data STRING
)
PARTITION BY RANGE_BUCKET(user_id, GENERATE_ARRAY(0, 1000000, 10000));
```

### Q23: How does clustering improve query performance?
**Answer:**
**Clustering Benefits:**
- Co-locates related data
- Reduces data scanned
- Improves JOIN performance
- Automatic re-clustering

```sql
-- Optimal clustering example
CREATE TABLE events (
  event_date DATE,
  user_id STRING,
  event_type STRING,
  data JSON
)
PARTITION BY event_date
CLUSTER BY user_id, event_type;

-- Query benefits from clustering
SELECT COUNT(*) FROM events
WHERE user_id = '12345' AND event_type = 'purchase';
```

### Q24: What are materialized views and when should you use them?
**Answer:**
**Materialized Views:**
- Pre-computed query results
- Automatic refresh
- Cost-effective for repeated queries
- Support incremental updates

```sql
-- Create materialized view
CREATE MATERIALIZED VIEW dataset.daily_sales AS
SELECT 
  DATE(transaction_timestamp) as date,
  SUM(amount) as total_sales,
  COUNT(*) as transaction_count
FROM dataset.transactions
GROUP BY DATE(transaction_timestamp);

-- Automatic refresh options
CREATE MATERIALIZED VIEW dataset.hourly_metrics
OPTIONS (enable_refresh = true, refresh_interval_minutes = 60)
AS SELECT ...
```

### Q25: How do you optimize JOIN operations in BigQuery?
**Answer:**
**JOIN Optimization:**

```sql
-- Use clustering for JOIN keys
CREATE TABLE orders CLUSTER BY customer_id;
CREATE TABLE customers CLUSTER BY customer_id;

-- Efficient JOIN
SELECT o.order_id, c.customer_name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;

-- Use ARRAY_AGG for one-to-many relationships
SELECT 
  c.customer_id,
  c.customer_name,
  ARRAY_AGG(STRUCT(o.order_id, o.amount)) as orders
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name;
```

### Q26: What is slot management and how do you monitor it?
**Answer:**
**Slot Management:**
- Virtual CPUs for query processing
- Dynamic allocation for on-demand
- Reserved slots for predictable workloads

```sql
-- Monitor slot usage
SELECT
  job_id,
  user_email,
  total_slot_ms / 1000 as slot_seconds,
  total_bytes_processed / POW(1024, 4) as tb_processed
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
ORDER BY total_slot_ms DESC;

-- Slot utilization by project
SELECT
  project_id,
  AVG(total_slot_ms) as avg_slot_ms,
  MAX(total_slot_ms) as max_slot_ms
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
GROUP BY project_id;
```

### Q27: How do you handle query optimization for large datasets?
**Answer:**
**Large Dataset Strategies:**

```sql
-- Use LIMIT for exploration
SELECT * FROM large_table LIMIT 1000;

-- Sample data for analysis
SELECT * FROM large_table TABLESAMPLE SYSTEM (1 PERCENT);

-- Use approximate functions
SELECT 
  APPROX_COUNT_DISTINCT(user_id) as unique_users,
  APPROX_QUANTILES(amount, 100)[OFFSET(50)] as median_amount
FROM transactions;

-- Optimize with WHERE clauses early
SELECT customer_id, SUM(amount)
FROM (
  SELECT customer_id, amount
  FROM transactions
  WHERE date >= '2024-01-01'  -- Filter early
)
GROUP BY customer_id;
```

### Q28: What are BigQuery's caching mechanisms?
**Answer:**
**Caching Types:**
- **Query result cache**: 24-hour cache
- **Shuffle cache**: Intermediate results
- **Metadata cache**: Schema and statistics

```sql
-- Disable cache for testing
SELECT * FROM dataset.table
WHERE date = CURRENT_DATE()
OPTIONS (use_cache = false);

-- Check if query used cache
SELECT
  job_id,
  cache_hit,
  total_bytes_processed
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE job_id = 'your_job_id';
```

### Q29: How do you optimize window functions in BigQuery?
**Answer:**
**Window Function Optimization:**

```sql
-- Efficient window function with partitioning
SELECT
  customer_id,
  order_date,
  amount,
  SUM(amount) OVER (
    PARTITION BY customer_id 
    ORDER BY order_date 
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) as running_total
FROM orders
WHERE order_date >= '2024-01-01';  -- Filter before window

-- Use clustering for PARTITION BY columns
CREATE TABLE orders_clustered
CLUSTER BY customer_id
AS SELECT * FROM orders;
```

### Q30: What are BigQuery's query execution stages?
**Answer:**
**Execution Stages:**
1. **Parse**: SQL syntax validation
2. **Plan**: Query optimization
3. **Execute**: Distributed processing
4. **Return**: Result aggregation

```sql
-- View query execution plan
SELECT
  job_id,
  stage_id,
  name,
  status,
  slot_ms,
  shuffle_output_bytes
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT_STAGES
WHERE job_id = 'your_job_id'
ORDER BY stage_id;
```

### Q31: How do you handle skewed data in BigQuery?
**Answer:**
**Skew Mitigation:**

```sql
-- Identify skewed data
SELECT 
  partition_column,
  COUNT(*) as row_count
FROM dataset.table
GROUP BY partition_column
ORDER BY row_count DESC;

-- Use FARM_FINGERPRINT for better distribution
SELECT
  ABS(MOD(FARM_FINGERPRINT(skewed_column), 100)) as bucket,
  COUNT(*) as count
FROM dataset.skewed_table
GROUP BY bucket;

-- Redistribute skewed JOINs
WITH redistributed AS (
  SELECT 
    *,
    ABS(MOD(FARM_FINGERPRINT(CAST(customer_id AS STRING)), 10)) as shard
  FROM customers
)
SELECT * FROM redistributed;
```

### Q32: What are BigQuery's storage optimization techniques?
**Answer:**
**Storage Optimization:**

```sql
-- Check table storage details
SELECT
  table_name,
  row_count,
  size_bytes / POW(1024, 3) as size_gb,
  partitioning_type,
  clustering_fields
FROM `project.dataset.INFORMATION_SCHEMA.TABLES`;

-- Optimize with column pruning
SELECT customer_id, amount  -- Only needed columns
FROM transactions
WHERE date >= '2024-01-01';

-- Use nested/repeated fields efficiently
SELECT 
  order_id,
  items.product_id,
  items.quantity
FROM orders,
UNNEST(items) as items
WHERE items.quantity > 1;
```

### Q33: How do you optimize BigQuery for real-time analytics?
**Answer:**
**Real-time Optimization:**

```sql
-- Use streaming buffer efficiently
CREATE TABLE real_time_events (
  event_timestamp TIMESTAMP,
  user_id STRING,
  event_data JSON
)
PARTITION BY DATE(event_timestamp)
CLUSTER BY user_id;

-- Query recent data efficiently
SELECT 
  COUNT(*) as event_count,
  AVG(EXTRACT(EPOCH FROM event_timestamp)) as avg_timestamp
FROM real_time_events
WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR);

-- Use DML for updates
MERGE real_time_events T
USING new_events S
ON T.event_id = S.event_id
WHEN NOT MATCHED THEN INSERT ROW;
```

### Q34: What are BigQuery's performance monitoring best practices?
**Answer:**
**Monitoring Queries:**

```sql
-- Monitor query performance
SELECT
  job_id,
  user_email,
  query,
  total_bytes_processed / POW(1024, 4) as tb_processed,
  total_slot_ms / 1000 as slot_seconds,
  TIMESTAMP_DIFF(end_time, start_time, SECOND) as duration_seconds
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
ORDER BY total_bytes_processed DESC;

-- Identify expensive queries
SELECT
  REGEXP_EXTRACT(query, r'FROM `([^`]+)`') as table_name,
  COUNT(*) as query_count,
  AVG(total_bytes_processed) as avg_bytes
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
GROUP BY table_name
ORDER BY avg_bytes DESC;
```

### Q35: How do you implement query result caching strategies?
**Answer:**
**Caching Strategies:**

```sql
-- Leverage automatic caching
SELECT customer_id, SUM(amount) as total
FROM transactions
WHERE date = '2024-01-15'
GROUP BY customer_id;
-- Subsequent identical queries use cache

-- Create cached views
CREATE VIEW daily_summary AS
SELECT 
  DATE(transaction_timestamp) as date,
  COUNT(*) as transaction_count,
  SUM(amount) as total_amount
FROM transactions
GROUP BY DATE(transaction_timestamp);

-- Use table snapshots for point-in-time data
CREATE SNAPSHOT TABLE dataset.transactions_snapshot
CLONE dataset.transactions
FOR SYSTEM_TIME AS OF TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR);
```

### Q36: What are advanced partitioning patterns?
**Answer:**
**Advanced Partitioning:**

```sql
-- Multi-level partitioning simulation
CREATE TABLE events_partitioned (
  event_date DATE,
  region STRING,
  user_id STRING,
  event_data JSON
)
PARTITION BY event_date
CLUSTER BY region, user_id;

-- Partition pruning optimization
SELECT COUNT(*)
FROM events_partitioned
WHERE event_date BETWEEN '2024-01-01' AND '2024-01-31'
  AND region = 'US';

-- Dynamic partition filtering
DECLARE start_date DATE DEFAULT '2024-01-01';
DECLARE end_date DATE DEFAULT '2024-01-31';

SELECT *
FROM events_partitioned
WHERE event_date BETWEEN start_date AND end_date;
```

### Q37: How do you optimize cross-region queries?
**Answer:**
**Cross-region Optimization:**

```sql
-- Query data in different regions
SELECT 
  'US' as region,
  COUNT(*) as count
FROM `project.us_dataset.table`
UNION ALL
SELECT 
  'EU' as region,
  COUNT(*) as count
FROM `project.eu_dataset.table`;

-- Use regional datasets for better performance
CREATE DATASET us_analytics
OPTIONS (location = 'US');

CREATE DATASET eu_analytics
OPTIONS (location = 'EU');
```

### Q38: What are BigQuery's query optimization patterns?
**Answer:**
**Optimization Patterns:**

```sql
-- Pattern 1: Filter early and often
WITH filtered_data AS (
  SELECT customer_id, amount, date
  FROM transactions
  WHERE date >= '2024-01-01'
    AND amount > 0
)
SELECT customer_id, SUM(amount)
FROM filtered_data
GROUP BY customer_id;

-- Pattern 2: Use EXISTS instead of IN
SELECT *
FROM customers c
WHERE EXISTS (
  SELECT 1 FROM orders o
  WHERE o.customer_id = c.customer_id
);

-- Pattern 3: Optimize GROUP BY
SELECT 
  customer_id,
  COUNTIF(amount > 100) as high_value_orders,
  AVG(amount) as avg_amount
FROM orders
GROUP BY customer_id;
```

### Q39: How do you handle BigQuery query timeouts?
**Answer:**
**Timeout Management:**

```sql
-- Set query timeout
SELECT *
FROM large_table
WHERE complex_condition = true
OPTIONS (job_timeout_ms = 600000);  -- 10 minutes

-- Break large queries into chunks
CREATE TEMP TABLE temp_results AS
SELECT * FROM large_table
WHERE date = '2024-01-01';

SELECT COUNT(*) FROM temp_results;

-- Use query jobs for long-running queries
```

```python
from google.cloud import bigquery

client = bigquery.Client()
job_config = bigquery.QueryJobConfig(
    job_timeout_ms=1800000,  # 30 minutes
    use_query_cache=False
)

query_job = client.query(query, job_config=job_config)
results = query_job.result()  # Wait for completion
```

### Q40: What are BigQuery's advanced analytical functions?
**Answer:**
**Advanced Analytics:**

```sql
-- Statistical functions
SELECT
  STDDEV(amount) as std_deviation,
  VARIANCE(amount) as variance,
  CORR(amount, quantity) as correlation
FROM sales_data;

-- Percentile functions
SELECT
  PERCENTILE_CONT(amount, 0.5) OVER() as median,
  PERCENTILE_DISC(amount, 0.9) OVER() as p90
FROM transactions;

-- Advanced window functions
SELECT
  customer_id,
  order_date,
  amount,
  LAG(amount, 1) OVER (PARTITION BY customer_id ORDER BY order_date) as prev_amount,
  LEAD(amount, 1) OVER (PARTITION BY customer_id ORDER BY order_date) as next_amount
FROM orders;
```

### Q41: How do you optimize BigQuery for machine learning workloads?
**Answer:**
**ML Optimization:**

```sql
-- Prepare ML training data efficiently
CREATE OR REPLACE TABLE ml_training_data AS
SELECT
  customer_id,
  AVG(amount) as avg_purchase,
  COUNT(*) as purchase_count,
  MAX(date) as last_purchase_date,
  CASE WHEN SUM(amount) > 1000 THEN 1 ELSE 0 END as high_value_customer
FROM transactions
WHERE date >= '2023-01-01'
GROUP BY customer_id;

-- Feature engineering with SQL
SELECT
  *,
  DATE_DIFF(CURRENT_DATE(), last_purchase_date, DAY) as days_since_purchase,
  avg_purchase * purchase_count as total_value
FROM ml_training_data;
```

### Q42: What are BigQuery's data quality optimization techniques?
**Answer:**
**Data Quality Checks:**

```sql
-- Automated data quality checks
SELECT
  'null_check' as test_name,
  COUNT(*) as null_count
FROM dataset.table
WHERE important_column IS NULL

UNION ALL

SELECT
  'duplicate_check' as test_name,
  COUNT(*) - COUNT(DISTINCT id) as duplicate_count
FROM dataset.table

UNION ALL

SELECT
  'range_check' as test_name,
  COUNTIF(amount < 0 OR amount > 1000000) as out_of_range_count
FROM dataset.table;

-- Data profiling query
SELECT
  column_name,
  data_type,
  is_nullable,
  COUNT(*) as total_rows,
  COUNT(DISTINCT column_name) as distinct_values
FROM `project.dataset.INFORMATION_SCHEMA.COLUMNS`
CROSS JOIN dataset.table
GROUP BY column_name, data_type, is_nullable;
```

### Q43: How do you implement incremental data processing in BigQuery?
**Answer:**
**Incremental Processing:**

```sql
-- Incremental load pattern
CREATE OR REPLACE TABLE dataset.incremental_summary AS
SELECT
  date,
  customer_id,
  SUM(amount) as daily_total
FROM dataset.transactions
WHERE date >= (
  SELECT COALESCE(MAX(date), '1900-01-01')
  FROM dataset.incremental_summary
)
GROUP BY date, customer_id;

-- Merge pattern for updates
MERGE dataset.customer_summary T
USING (
  SELECT 
    customer_id,
    SUM(amount) as total_amount,
    COUNT(*) as transaction_count
  FROM dataset.new_transactions
  GROUP BY customer_id
) S
ON T.customer_id = S.customer_id
WHEN MATCHED THEN
  UPDATE SET 
    total_amount = T.total_amount + S.total_amount,
    transaction_count = T.transaction_count + S.transaction_count
WHEN NOT MATCHED THEN
  INSERT (customer_id, total_amount, transaction_count)
  VALUES (S.customer_id, S.total_amount, S.transaction_count);
```

### Q44: What are BigQuery's geographic and spatial optimization techniques?
**Answer:**
**Geospatial Optimization:**

```sql
-- Efficient geographic queries
SELECT
  store_id,
  ST_DISTANCE(store_location, ST_GEOGPOINT(-74.0060, 40.7128)) as distance_to_nyc
FROM stores
WHERE ST_DWITHIN(store_location, ST_GEOGPOINT(-74.0060, 40.7128), 50000)  -- 50km radius
ORDER BY distance_to_nyc;

-- Spatial clustering
CREATE TABLE stores_clustered (
  store_id STRING,
  store_location GEOGRAPHY,
  region STRING
)
CLUSTER BY region;  -- Cluster by geographic region

-- Geospatial aggregations
SELECT
  region,
  COUNT(*) as store_count,
  ST_CENTROID(ST_UNION_AGG(store_location)) as region_center
FROM stores
GROUP BY region;
```

### Q45: How do you optimize BigQuery for time-series analysis?
**Answer:**
**Time-series Optimization:**

```sql
-- Time-series partitioning
CREATE TABLE time_series_data (
  timestamp TIMESTAMP,
  metric_name STRING,
  value FLOAT64,
  tags ARRAY<STRUCT<key STRING, value STRING>>
)
PARTITION BY DATE(timestamp)
CLUSTER BY metric_name;

-- Efficient time-series queries
SELECT
  timestamp,
  value,
  AVG(value) OVER (
    ORDER BY timestamp
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) as moving_avg_7day
FROM time_series_data
WHERE metric_name = 'cpu_usage'
  AND DATE(timestamp) >= '2024-01-01'
ORDER BY timestamp;

-- Time-series aggregation
SELECT
  TIMESTAMP_TRUNC(timestamp, HOUR) as hour,
  metric_name,
  AVG(value) as avg_value,
  MIN(value) as min_value,
  MAX(value) as max_value
FROM time_series_data
WHERE DATE(timestamp) = '2024-01-15'
GROUP BY hour, metric_name
ORDER BY hour;
```

### Q46: What are BigQuery's advanced cost optimization strategies?
**Answer:**
**Advanced Cost Optimization:**

```sql
-- Cost monitoring by user
SELECT
  user_email,
  DATE(creation_time) as query_date,
  SUM(total_bytes_processed) / POW(1024, 4) as tb_processed,
  SUM(total_bytes_processed) / POW(1024, 4) * 5 as estimated_cost_usd
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY user_email, query_date
ORDER BY estimated_cost_usd DESC;

-- Query cost optimization
SELECT
  table_name,
  AVG(total_bytes_processed) as avg_bytes_per_query,
  COUNT(*) as query_count
FROM (
  SELECT
    REGEXP_EXTRACT(query, r'FROM `[^.]+\.([^.`]+)') as table_name,
    total_bytes_processed
  FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
  WHERE query LIKE '%FROM%'
)
WHERE table_name IS NOT NULL
GROUP BY table_name
ORDER BY avg_bytes_per_query DESC;
```

---

## BigQuery ML (Machine Learning)

### Q47: What are the different model types available in BigQuery ML?
**Answer:**
**Supervised Learning:**
- Linear/Logistic Regression
- Boosted Trees (XGBoost)
- Random Forest
- Deep Neural Networks (DNN)
- Wide & Deep Networks

**Unsupervised Learning:**
- K-means Clustering
- Principal Component Analysis (PCA)
- Autoencoder

**Time Series:**
- ARIMA Plus
- Time Series Forecasting

```sql
-- Classification model
CREATE MODEL `dataset.customer_churn_model`
OPTIONS(
  model_type='logistic_reg',
  input_label_cols=['churned']
) AS
SELECT
  tenure_months,
  monthly_charges,
  total_charges,
  churned
FROM `dataset.customer_data`;
```

### Q48: How do you perform feature engineering in BigQuery ML?
**Answer:**
**Feature Engineering Techniques:**

```sql
-- Feature transformation
CREATE MODEL `dataset.sales_model`
OPTIONS(
  model_type='linear_reg',
  input_label_cols=['sales_amount']
) AS
SELECT
  -- Numerical features
  advertising_spend,
  SQRT(advertising_spend) as sqrt_ad_spend,
  
  -- Categorical encoding
  season,
  
  -- Date features
  EXTRACT(MONTH FROM date) as month,
  EXTRACT(DAYOFWEEK FROM date) as day_of_week,
  
  -- Interaction features
  advertising_spend * EXTRACT(MONTH FROM date) as ad_spend_month_interaction,
  
  -- Target variable
  sales_amount
FROM `dataset.sales_data`
WHERE date >= '2023-01-01';
```

### Q49: How do you handle model evaluation and validation in BigQuery ML?
**Answer:**
**Model Evaluation:**

```sql
-- Evaluate model performance
SELECT *
FROM ML.EVALUATE(MODEL `dataset.customer_churn_model`,
  (
    SELECT
      tenure_months,
      monthly_charges,
      total_charges,
      churned
    FROM `dataset.test_data`
  )
);

-- Cross-validation
CREATE MODEL `dataset.cv_model`
OPTIONS(
  model_type='logistic_reg',
  data_split_method='seq',
  data_split_eval_fraction=0.2,
  data_split_col='date'
) AS
SELECT * FROM training_data;

-- Feature importance
SELECT *
FROM ML.FEATURE_IMPORTANCE(MODEL `dataset.customer_churn_model`);
```

### Q50: How do you implement hyperparameter tuning in BigQuery ML?
**Answer:**
**Hyperparameter Tuning:**

```sql
-- XGBoost with hyperparameter tuning
CREATE MODEL `dataset.tuned_model`
OPTIONS(
  model_type='boosted_tree_classifier',
  booster_type='gbtree',
  num_parallel_tree=1,
  max_iterations=50,
  tree_method='hist',
  early_stop=true,
  subsample=0.8,
  colsample_bytree=0.8,
  min_tree_child_weight=1,
  
  -- Hyperparameter tuning
  enable_global_explain=true,
  input_label_cols=['target']
) AS
SELECT * FROM training_data;

-- Grid search simulation
CREATE MODEL `dataset.model_v1`
OPTIONS(model_type='linear_reg', l1_reg=0.1, l2_reg=0.1) AS
SELECT * FROM training_data;

CREATE MODEL `dataset.model_v2`
OPTIONS(model_type='linear_reg', l1_reg=0.01, l2_reg=0.01) AS
SELECT * FROM training_data;
```

### Q51: How do you deploy and serve BigQuery ML models?
**Answer:**
**Model Deployment:**

```sql
-- Batch predictions
SELECT
  customer_id,
  predicted_churned,
  predicted_churned_probs[OFFSET(1)].prob as churn_probability
FROM ML.PREDICT(MODEL `dataset.customer_churn_model`,
  (
    SELECT
      customer_id,
      tenure_months,
      monthly_charges,
      total_charges
    FROM `dataset.new_customers`
  )
);

-- Export model for external serving
EXPORT MODEL `dataset.customer_churn_model`
OPTIONS(uri='gs://bucket/model_export/');

-- Model versioning
CREATE MODEL `dataset.churn_model_v2`
OPTIONS(
  model_type='boosted_tree_classifier',
  input_label_cols=['churned']
) AS
SELECT * FROM updated_training_data;
```

### Q52: How do you implement time series forecasting in BigQuery ML?
**Answer:**
**Time Series Models:**

```sql
-- ARIMA Plus model
CREATE MODEL `dataset.sales_forecast_model`
OPTIONS(
  model_type='arima_plus',
  time_series_timestamp_col='date',
  time_series_data_col='sales_amount',
  time_series_id_col='product_id',
  holiday_region='US'
) AS
SELECT
  date,
  product_id,
  sales_amount
FROM `dataset.daily_sales`
WHERE date >= '2022-01-01';

-- Generate forecasts
SELECT
  *
FROM ML.FORECAST(MODEL `dataset.sales_forecast_model`,
  STRUCT(30 AS horizon, 0.8 AS confidence_level)
);

-- Detect anomalies
SELECT
  *
FROM ML.DETECT_ANOMALIES(MODEL `dataset.sales_forecast_model`,
  STRUCT(0.8 AS anomaly_prob_threshold)
);
```

### Q53: How do you implement clustering with BigQuery ML?
**Answer:**
**K-means Clustering:**

```sql
-- Customer segmentation
CREATE MODEL `dataset.customer_segments`
OPTIONS(
  model_type='kmeans',
  num_clusters=5,
  standardize_features=true
) AS
SELECT
  customer_id,
  total_purchases,
  avg_order_value,
  days_since_last_purchase,
  total_returns
FROM `dataset.customer_features`;

-- Predict clusters
SELECT
  customer_id,
  CENTROID_ID as cluster_id
FROM ML.PREDICT(MODEL `dataset.customer_segments`,
  (
    SELECT * FROM `dataset.new_customers`
  )
);

-- Analyze clusters
SELECT
  centroid_id,
  feature,
  numerical_value
FROM ML.CENTROIDS(MODEL `dataset.customer_segments`);
```

### Q54: How do you implement recommendation systems in BigQuery ML?
**Answer:**
**Matrix Factorization:**

```sql
-- Collaborative filtering model
CREATE MODEL `dataset.product_recommendations`
OPTIONS(
  model_type='matrix_factorization',
  user_col='customer_id',
  item_col='product_id',
  rating_col='rating',
  l2_reg=0.1,
  num_factors=50
) AS
SELECT
  customer_id,
  product_id,
  rating
FROM `dataset.customer_ratings`;

-- Generate recommendations
SELECT
  customer_id,
  product_id,
  predicted_rating
FROM ML.RECOMMEND(MODEL `dataset.product_recommendations`,
  STRUCT(5 AS max_recommendations)
)
WHERE customer_id = '12345'
ORDER BY predicted_rating DESC;
```

### Q55: How do you implement deep learning models in BigQuery ML?
**Answer:**
**Deep Neural Networks:**

```sql
-- DNN for complex patterns
CREATE MODEL `dataset.dnn_model`
OPTIONS(
  model_type='dnn_classifier',
  hidden_units=[128, 64, 32],
  dropout=0.2,
  batch_size=1000,
  max_iterations=100,
  learn_rate=0.001,
  activation_fn='relu',
  optimizer='adam'
) AS
SELECT
  feature1,
  feature2,
  feature3,
  label
FROM `dataset.training_data`;

-- Wide & Deep model
CREATE MODEL `dataset.wide_deep_model`
OPTIONS(
  model_type='dnn_linear_combined_classifier',
  dnn_hidden_units=[100, 50],
  dnn_dropout=0.1,
  dnn_learning_rate=0.001
) AS
SELECT * FROM training_data;
```

### Q56: How do you handle model monitoring and drift detection?
**Answer:**
**Model Monitoring:**

```sql
-- Monitor model performance over time
WITH model_performance AS (
  SELECT
    DATE(prediction_timestamp) as prediction_date,
    AVG(ABS(actual_value - predicted_value)) as mae,
    CORR(actual_value, predicted_value) as correlation
  FROM `dataset.model_predictions`
  WHERE prediction_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  GROUP BY prediction_date
)
SELECT
  prediction_date,
  mae,
  correlation,
  LAG(mae) OVER (ORDER BY prediction_date) as prev_mae,
  (mae - LAG(mae) OVER (ORDER BY prediction_date)) / LAG(mae) OVER (ORDER BY prediction_date) as mae_change_pct
FROM model_performance
ORDER BY prediction_date;

-- Feature drift detection
SELECT
  feature_name,
  training_mean,
  current_mean,
  ABS(current_mean - training_mean) / training_std as drift_score
FROM (
  SELECT
    'feature1' as feature_name,
    AVG(feature1) as current_mean
  FROM `dataset.current_data`
) current
CROSS JOIN (
  SELECT
    AVG(feature1) as training_mean,
    STDDEV(feature1) as training_std
  FROM `dataset.training_data`
) training;
```

### Q57: How do you implement AutoML integration with BigQuery ML?
**Answer:**
**AutoML Integration:**

```sql
-- AutoML Tables model
CREATE MODEL `dataset.automl_model`
OPTIONS(
  model_type='automl_classifier',
  budget_hours=1.0,
  optimization_objective='maximize-au-prc'
) AS
SELECT * FROM `dataset.training_data`;

-- AutoML forecasting
CREATE MODEL `dataset.automl_forecast`
OPTIONS(
  model_type='automl_forecaster',
  time_series_timestamp_col='timestamp',
  time_series_data_col='value',
  budget_hours=2.0
) AS
SELECT * FROM `dataset.time_series_data`;
```

### Q58: How do you implement feature selection in BigQuery ML?
**Answer:**
**Feature Selection:**

```sql
-- Correlation analysis
SELECT
  CORR(feature1, target) as feature1_corr,
  CORR(feature2, target) as feature2_corr,
  CORR(feature3, target) as feature3_corr
FROM `dataset.training_data`;

-- Feature importance from trained model
SELECT
  feature,
  importance
FROM ML.FEATURE_IMPORTANCE(MODEL `dataset.trained_model`)
ORDER BY importance DESC;

-- Recursive feature elimination simulation
CREATE MODEL `dataset.model_all_features`
OPTIONS(model_type='linear_reg') AS
SELECT * FROM training_data;

CREATE MODEL `dataset.model_top_features`
OPTIONS(model_type='linear_reg') AS
SELECT
  top_feature1,
  top_feature2,
  top_feature3,
  target
FROM training_data;
```

### Q59: How do you implement ensemble methods in BigQuery ML?
**Answer:**
**Ensemble Approaches:**

```sql
-- Multiple model predictions
WITH model1_pred AS (
  SELECT
    customer_id,
    predicted_value as pred1
  FROM ML.PREDICT(MODEL `dataset.model1`, (SELECT * FROM test_data))
),
model2_pred AS (
  SELECT
    customer_id,
    predicted_value as pred2
  FROM ML.PREDICT(MODEL `dataset.model2`, (SELECT * FROM test_data))
)
SELECT
  customer_id,
  (pred1 + pred2) / 2 as ensemble_prediction
FROM model1_pred
JOIN model2_pred USING (customer_id);

-- Weighted ensemble
SELECT
  customer_id,
  (0.6 * pred1 + 0.4 * pred2) as weighted_ensemble
FROM model_predictions;
```

### Q60: How do you implement model explainability in BigQuery ML?
**Answer:**
**Model Explainability:**

```sql
-- Global explanations
SELECT *
FROM ML.GLOBAL_EXPLAIN(MODEL `dataset.customer_churn_model`);

-- Feature importance
SELECT
  feature,
  importance,
  RANK() OVER (ORDER BY importance DESC) as importance_rank
FROM ML.FEATURE_IMPORTANCE(MODEL `dataset.customer_churn_model`);

-- Training statistics
SELECT *
FROM ML.TRAINING_INFO(MODEL `dataset.customer_churn_model`);

-- Model weights (for linear models)
SELECT *
FROM ML.WEIGHTS(MODEL `dataset.linear_model`)
ORDER BY ABS(weight) DESC;
```

### Q61: How do you implement A/B testing for ML models in BigQuery?
**Answer:**
**A/B Testing Framework:**

```sql
-- Model comparison setup
WITH model_a_results AS (
  SELECT
    customer_id,
    'model_a' as model_version,
    predicted_value,
    actual_value
  FROM ML.PREDICT(MODEL `dataset.model_a`, (SELECT * FROM test_data))
  JOIN actual_results USING (customer_id)
),
model_b_results AS (
  SELECT
    customer_id,
    'model_b' as model_version,
    predicted_value,
    actual_value
  FROM ML.PREDICT(MODEL `dataset.model_b`, (SELECT * FROM test_data))
  JOIN actual_results USING (customer_id)
)
SELECT
  model_version,
  COUNT(*) as sample_size,
  AVG(ABS(predicted_value - actual_value)) as mae,
  SQRT(AVG(POW(predicted_value - actual_value, 2))) as rmse,
  CORR(predicted_value, actual_value) as correlation
FROM (
  SELECT * FROM model_a_results
  UNION ALL
  SELECT * FROM model_b_results
)
GROUP BY model_version;
```

### Q62: How do you implement transfer learning in BigQuery ML?
**Answer:**
**Transfer Learning:**

```sql
-- Pre-trained model fine-tuning
CREATE MODEL `dataset.fine_tuned_model`
OPTIONS(
  model_type='dnn_classifier',
  warm_start=true,
  warm_start_from='dataset.base_model'
) AS
SELECT * FROM `dataset.new_domain_data`;

-- Feature extraction from pre-trained model
CREATE MODEL `dataset.feature_extractor`
OPTIONS(
  model_type='autoencoder',
  hidden_units=[100, 50, 20]
) AS
SELECT * FROM `dataset.source_domain_data`;

-- Use extracted features
WITH extracted_features AS (
  SELECT
    customer_id,
    ML.PREDICT(MODEL `dataset.feature_extractor`, 
               STRUCT(features AS input)) as encoded_features
  FROM `dataset.target_domain_data`
)
CREATE MODEL `dataset.target_model`
OPTIONS(model_type='linear_reg') AS
SELECT * FROM extracted_features;
```

### Q63: How do you implement online learning patterns in BigQuery ML?
**Answer:**
**Incremental Learning:**

```sql
-- Incremental model updates
CREATE OR REPLACE MODEL `dataset.incremental_model`
OPTIONS(
  model_type='linear_reg',
  warm_start=true,
  warm_start_from='dataset.previous_model'
) AS
SELECT * FROM (
  SELECT * FROM `dataset.historical_data`
  UNION ALL
  SELECT * FROM `dataset.new_batch_data`
);

-- Sliding window training
CREATE OR REPLACE MODEL `dataset.sliding_window_model`
OPTIONS(model_type='linear_reg') AS
SELECT *
FROM `dataset.training_data`
WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY);

-- Model performance tracking
SELECT
  model_version,
  training_date,
  evaluation_metrics
FROM `dataset.model_performance_log`
ORDER BY training_date DESC;
```

### Q64: How do you implement multi-class and multi-label classification?
**Answer:**
**Multi-class/Multi-label:**

```sql
-- Multi-class classification
CREATE MODEL `dataset.multiclass_model`
OPTIONS(
  model_type='logistic_reg',
  input_label_cols=['category']
) AS
SELECT
  feature1,
  feature2,
  feature3,
  category  -- Categories: A, B, C, D
FROM `dataset.multiclass_data`;

-- Multi-label approach (binary classification per label)
CREATE MODEL `dataset.label1_model`
OPTIONS(model_type='logistic_reg') AS
SELECT
  features.*,
  has_label1 as label
FROM `dataset.multilabel_data`;

CREATE MODEL `dataset.label2_model`
OPTIONS(model_type='logistic_reg') AS
SELECT
  features.*,
  has_label2 as label
FROM `dataset.multilabel_data`;
```

### Q65: How do you implement model versioning and lifecycle management?
**Answer:**
**Model Lifecycle:**

```sql
-- Model versioning
CREATE TABLE `dataset.model_registry` (
  model_name STRING,
  version STRING,
  created_date TIMESTAMP,
  performance_metrics JSON,
  status STRING,  -- 'training', 'validation', 'production', 'archived'
  model_path STRING
);

-- Register new model version
INSERT INTO `dataset.model_registry`
VALUES (
  'customer_churn_model',
  'v2.1',
  CURRENT_TIMESTAMP(),
  JSON '{"accuracy": 0.85, "precision": 0.82, "recall": 0.88}',
  'validation',
  'dataset.customer_churn_model_v21'
);

-- Model comparison
SELECT
  version,
  JSON_EXTRACT_SCALAR(performance_metrics, '$.accuracy') as accuracy,
  JSON_EXTRACT_SCALAR(performance_metrics, '$.precision') as precision,
  created_date
FROM `dataset.model_registry`
WHERE model_name = 'customer_churn_model'
ORDER BY created_date DESC;

-- Promote model to production
UPDATE `dataset.model_registry`
SET status = 'production'
WHERE model_name = 'customer_churn_model' AND version = 'v2.1';
```

### Q66: How do you implement real-time ML inference in BigQuery?
**Answer:**
**Real-time Inference:**

```sql
-- Streaming predictions
CREATE OR REPLACE FUNCTION `dataset.predict_churn`(tenure INT64, charges FLOAT64)
RETURNS FLOAT64
LANGUAGE SQL AS (
  (
    SELECT predicted_churned_probs[OFFSET(1)].prob
    FROM ML.PREDICT(MODEL `dataset.customer_churn_model`,
      (SELECT tenure as tenure_months, charges as monthly_charges)
    )
  )
);

-- Use in streaming queries
SELECT
  customer_id,
  `dataset.predict_churn`(tenure_months, monthly_charges) as churn_probability,
  CASE 
    WHEN `dataset.predict_churn`(tenure_months, monthly_charges) > 0.7 
    THEN 'high_risk'
    ELSE 'low_risk'
  END as risk_category
FROM `dataset.streaming_customer_data`;

-- Batch scoring for real-time serving
CREATE OR REPLACE TABLE `dataset.customer_scores` AS
SELECT
  customer_id,
  predicted_churned_probs[OFFSET(1)].prob as churn_score,
  CURRENT_TIMESTAMP() as score_timestamp
FROM ML.PREDICT(MODEL `dataset.customer_churn_model`,
  (SELECT * FROM `dataset.active_customers`)
);
```

---

## Advanced Analytics

### Q67: How do you implement complex window functions in BigQuery?
**Answer:**
**Advanced Window Functions:**

```sql
-- Running calculations
SELECT
  customer_id,
  order_date,
  amount,
  SUM(amount) OVER (
    PARTITION BY customer_id 
    ORDER BY order_date 
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) as running_total,
  AVG(amount) OVER (
    PARTITION BY customer_id 
    ORDER BY order_date 
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
  ) as moving_avg_3
FROM orders;

-- Percentile functions
SELECT
  customer_id,
  amount,
  PERCENT_RANK() OVER (ORDER BY amount) as percentile_rank,
  NTILE(10) OVER (ORDER BY amount) as decile
FROM transactions;
```

### Q68: How do you perform cohort analysis in BigQuery?
**Answer:**
**Cohort Analysis:**

```sql
-- Customer cohort analysis
WITH customer_cohorts AS (
  SELECT
    customer_id,
    DATE_TRUNC(MIN(order_date), MONTH) as cohort_month
  FROM orders
  GROUP BY customer_id
),
cohort_data AS (
  SELECT
    c.cohort_month,
    DATE_DIFF(DATE_TRUNC(o.order_date, MONTH), c.cohort_month, MONTH) as period_number,
    COUNT(DISTINCT o.customer_id) as customers
  FROM customer_cohorts c
  JOIN orders o ON c.customer_id = o.customer_id
  GROUP BY c.cohort_month, period_number
),
cohort_sizes AS (
  SELECT
    cohort_month,
    COUNT(DISTINCT customer_id) as cohort_size
  FROM customer_cohorts
  GROUP BY cohort_month
)
SELECT
  cd.cohort_month,
  cd.period_number,
  cd.customers,
  cs.cohort_size,
  cd.customers / cs.cohort_size as retention_rate
FROM cohort_data cd
JOIN cohort_sizes cs ON cd.cohort_month = cs.cohort_month
ORDER BY cd.cohort_month, cd.period_number;
```

### Q69: How do you implement funnel analysis in BigQuery?
**Answer:**
**Funnel Analysis:**

```sql
-- E-commerce funnel
WITH funnel_events AS (
  SELECT
    user_id,
    event_timestamp,
    event_name,
    ROW_NUMBER() OVER (
      PARTITION BY user_id, event_name 
      ORDER BY event_timestamp
    ) as event_rank
  FROM events
  WHERE event_name IN ('page_view', 'add_to_cart', 'checkout', 'purchase')
    AND DATE(event_timestamp) = '2024-01-15'
),
first_events AS (
  SELECT *
  FROM funnel_events
  WHERE event_rank = 1
),
funnel_steps AS (
  SELECT
    user_id,
    MAX(CASE WHEN event_name = 'page_view' THEN 1 ELSE 0 END) as step1_page_view,
    MAX(CASE WHEN event_name = 'add_to_cart' THEN 1 ELSE 0 END) as step2_add_cart,
    MAX(CASE WHEN event_name = 'checkout' THEN 1 ELSE 0 END) as step3_checkout,
    MAX(CASE WHEN event_name = 'purchase' THEN 1 ELSE 0 END) as step4_purchase
  FROM first_events
  GROUP BY user_id
)
SELECT
  SUM(step1_page_view) as page_views,
  SUM(step2_add_cart) as add_to_carts,
  SUM(step3_checkout) as checkouts,
  SUM(step4_purchase) as purchases,
  
  SUM(step2_add_cart) / SUM(step1_page_view) as page_to_cart_rate,
  SUM(step3_checkout) / SUM(step2_add_cart) as cart_to_checkout_rate,
  SUM(step4_purchase) / SUM(step3_checkout) as checkout_to_purchase_rate
FROM funnel_steps;
```

### Q70: How do you perform RFM analysis in BigQuery?
**Answer:**
**RFM Analysis (Recency, Frequency, Monetary):**

```sql
-- Calculate RFM metrics
WITH rfm_metrics AS (
  SELECT
    customer_id,
    DATE_DIFF(CURRENT_DATE(), MAX(order_date), DAY) as recency,
    COUNT(DISTINCT order_id) as frequency,
    SUM(amount) as monetary
  FROM orders
  WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY)
  GROUP BY customer_id
),
rfm_scores AS (
  SELECT
    customer_id,
    recency,
    frequency,
    monetary,
    NTILE(5) OVER (ORDER BY recency DESC) as r_score,  -- Lower recency = higher score
    NTILE(5) OVER (ORDER BY frequency) as f_score,
    NTILE(5) OVER (ORDER BY monetary) as m_score
  FROM rfm_metrics
)
SELECT
  customer_id,
  CONCAT(CAST(r_score AS STRING), CAST(f_score AS STRING), CAST(m_score AS STRING)) as rfm_segment,
  CASE
    WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
    WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Loyal Customers'
    WHEN r_score >= 4 AND f_score <= 2 THEN 'New Customers'
    WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk'
    WHEN r_score <= 2 AND f_score <= 2 THEN 'Lost Customers'
    ELSE 'Others'
  END as customer_segment
FROM rfm_scores;
```

### Q71: How do you implement statistical analysis in BigQuery?
**Answer:**
**Statistical Functions:**

```sql
-- Descriptive statistics
SELECT
  product_category,
  COUNT(*) as sample_size,
  AVG(price) as mean_price,
  STDDEV(price) as std_dev,
  VARIANCE(price) as variance,
  MIN(price) as min_price,
  MAX(price) as max_price,
  
  -- Percentiles
  APPROX_QUANTILES(price, 100)[OFFSET(25)] as q1,
  APPROX_QUANTILES(price, 100)[OFFSET(50)] as median,
  APPROX_QUANTILES(price, 100)[OFFSET(75)] as q3,
  
  -- Skewness approximation
  (AVG(POW((price - AVG(price)) / STDDEV(price), 3))) as skewness_approx
FROM products
GROUP BY product_category;

-- Correlation analysis
SELECT
  CORR(advertising_spend, sales) as correlation,
  COVAR_POP(advertising_spend, sales) as covariance
FROM marketing_data;

-- Hypothesis testing (t-test simulation)
WITH group_stats AS (
  SELECT
    treatment_group,
    COUNT(*) as n,
    AVG(conversion_rate) as mean_conversion,
    STDDEV(conversion_rate) as std_conversion
  FROM ab_test_results
  GROUP BY treatment_group
)
SELECT
  ABS(a.mean_conversion - b.mean_conversion) / 
  SQRT((POW(a.std_conversion, 2) / a.n) + (POW(b.std_conversion, 2) / b.n)) as t_statistic
FROM group_stats a
CROSS JOIN group_stats b
WHERE a.treatment_group = 'A' AND b.treatment_group = 'B';
```

### Q72: How do you perform time series analysis in BigQuery?
**Answer:**
**Time Series Analysis:**

```sql
-- Trend analysis
WITH daily_metrics AS (
  SELECT
    DATE(timestamp) as date,
    SUM(revenue) as daily_revenue
  FROM transactions
  GROUP BY DATE(timestamp)
),
trend_analysis AS (
  SELECT
    date,
    daily_revenue,
    AVG(daily_revenue) OVER (
      ORDER BY date 
      ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as moving_avg_7day,
    
    -- Linear trend
    REGR_SLOPE(daily_revenue, UNIX_DATE(date)) OVER (
      ORDER BY date 
      ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as trend_slope_30day
  FROM daily_metrics
)
SELECT
  date,
  daily_revenue,
  moving_avg_7day,
  trend_slope_30day,
  CASE
    WHEN trend_slope_30day > 0 THEN 'Increasing'
    WHEN trend_slope_30day < 0 THEN 'Decreasing'
    ELSE 'Stable'
  END as trend_direction
FROM trend_analysis
ORDER BY date;

-- Seasonality detection
SELECT
  EXTRACT(MONTH FROM date) as month,
  EXTRACT(DAYOFWEEK FROM date) as day_of_week,
  AVG(daily_revenue) as avg_revenue,
  STDDEV(daily_revenue) as revenue_volatility
FROM daily_metrics
GROUP BY month, day_of_week
ORDER BY month, day_of_week;
```

### Q73: How do you implement geographic analysis in BigQuery?
**Answer:**
**Geospatial Analytics:**

```sql
-- Distance-based analysis
SELECT
  store_id,
  customer_id,
  ST_DISTANCE(store_location, customer_location) / 1000 as distance_km,
  CASE
    WHEN ST_DISTANCE(store_location, customer_location) <= 5000 THEN 'Local'
    WHEN ST_DISTANCE(store_location, customer_location) <= 25000 THEN 'Regional'
    ELSE 'Remote'
  END as customer_proximity
FROM store_customer_pairs;

-- Spatial clustering
WITH customer_clusters AS (
  SELECT
    customer_id,
    customer_location,
    ST_CLUSTERDBSCAN(customer_location, 1000, 5) OVER() as cluster_id
  FROM customers
  WHERE customer_location IS NOT NULL
)
SELECT
  cluster_id,
  COUNT(*) as customers_in_cluster,
  ST_CENTROID(ST_UNION_AGG(customer_location)) as cluster_center
FROM customer_clusters
WHERE cluster_id IS NOT NULL
GROUP BY cluster_id;

-- Market penetration by region
SELECT
  region,
  COUNT(DISTINCT customer_id) as customers,
  SUM(total_purchases) as total_revenue,
  AVG(total_purchases) as avg_customer_value,
  COUNT(DISTINCT customer_id) / population * 100 as penetration_rate
FROM customer_summary cs
JOIN region_demographics rd USING (region)
GROUP BY region, population;
```

### Q74: How do you perform text analytics in BigQuery?
**Answer:**
**Text Analytics:**

```sql
-- Text processing and analysis
WITH processed_reviews AS (
  SELECT
    review_id,
    customer_id,
    LOWER(TRIM(review_text)) as clean_text,
    ARRAY_LENGTH(SPLIT(review_text, ' ')) as word_count,
    REGEXP_CONTAINS(LOWER(review_text), r'excellent|great|amazing|love') as positive_keywords,
    REGEXP_CONTAINS(LOWER(review_text), r'terrible|awful|hate|worst') as negative_keywords
  FROM product_reviews
)
SELECT
  customer_id,
  COUNT(*) as total_reviews,
  AVG(word_count) as avg_words_per_review,
  COUNTIF(positive_keywords) / COUNT(*) as positive_sentiment_ratio,
  COUNTIF(negative_keywords) / COUNT(*) as negative_sentiment_ratio
FROM processed_reviews
GROUP BY customer_id;

-- N-gram analysis
WITH words AS (
  SELECT
    review_id,
    word
  FROM product_reviews,
  UNNEST(SPLIT(LOWER(REGEXP_REPLACE(review_text, r'[^a-zA-Z\s]', '')), ' ')) as word
  WHERE LENGTH(word) > 2
)
SELECT
  word,
  COUNT(*) as frequency
FROM words
GROUP BY word
ORDER BY frequency DESC
LIMIT 50;
```

### Q75: How do you implement anomaly detection in BigQuery?
**Answer:**
**Anomaly Detection:**

```sql
-- Statistical anomaly detection
WITH daily_metrics AS (
  SELECT
    DATE(timestamp) as date,
    SUM(revenue) as daily_revenue
  FROM transactions
  GROUP BY DATE(timestamp)
),
stats AS (
  SELECT
    date,
    daily_revenue,
    AVG(daily_revenue) OVER () as mean_revenue,
    STDDEV(daily_revenue) OVER () as std_revenue
  FROM daily_metrics
)
SELECT
  date,
  daily_revenue,
  mean_revenue,
  ABS(daily_revenue - mean_revenue) / std_revenue as z_score,
  CASE
    WHEN ABS(daily_revenue - mean_revenue) / std_revenue > 2 THEN 'Anomaly'
    ELSE 'Normal'
  END as anomaly_flag
FROM stats
ORDER BY z_score DESC;

-- Interquartile range (IQR) method
WITH quartiles AS (
  SELECT
    APPROX_QUANTILES(daily_revenue, 100)[OFFSET(25)] as q1,
    APPROX_QUANTILES(daily_revenue, 100)[OFFSET(75)] as q3
  FROM daily_metrics
)
SELECT
  dm.date,
  dm.daily_revenue,
  q.q1,
  q.q3,
  q.q3 - q.q1 as iqr,
  CASE
    WHEN dm.daily_revenue < (q.q1 - 1.5 * (q.q3 - q.q1)) OR 
         dm.daily_revenue > (q.q3 + 1.5 * (q.q3 - q.q1)) THEN 'Outlier'
    ELSE 'Normal'
  END as outlier_flag
FROM daily_metrics dm
CROSS JOIN quartiles q;
```

### Q76: How do you perform market basket analysis in BigQuery?
**Answer:**
**Market Basket Analysis:**

```sql
-- Association rules mining
WITH transaction_items AS (
  SELECT
    transaction_id,
    ARRAY_AGG(product_id) as items
  FROM order_items
  GROUP BY transaction_id
),
item_pairs AS (
  SELECT
    transaction_id,
    item1,
    item2
  FROM transaction_items,
  UNNEST(items) as item1,
  UNNEST(items) as item2
  WHERE item1 < item2  -- Avoid duplicates and self-pairs
),
association_metrics AS (
  SELECT
    item1,
    item2,
    COUNT(*) as pair_count,
    COUNT(*) / (SELECT COUNT(DISTINCT transaction_id) FROM transaction_items) as support,
    
    -- Calculate confidence: P(item2|item1)
    COUNT(*) / (
      SELECT COUNT(DISTINCT transaction_id)
      FROM transaction_items
      WHERE item1 IN UNNEST(items)
    ) as confidence_item1_to_item2
  FROM item_pairs
  GROUP BY item1, item2
  HAVING COUNT(*) >= 10  -- Minimum support threshold
)
SELECT
  p1.product_name as product1,
  p2.product_name as product2,
  am.pair_count,
  am.support,
  am.confidence_item1_to_item2,
  am.support / (
    (SELECT support FROM single_item_support WHERE item = am.item1) *
    (SELECT support FROM single_item_support WHERE item = am.item2)
  ) as lift
FROM association_metrics am
JOIN products p1 ON am.item1 = p1.product_id
JOIN products p2 ON am.item2 = p2.product_id
WHERE am.confidence_item1_to_item2 > 0.1  -- Minimum confidence threshold
ORDER BY lift DESC;
```

### Q77: How do you implement customer lifetime value (CLV) analysis?
**Answer:**
**CLV Analysis:**

```sql
-- Historical CLV calculation
WITH customer_metrics AS (
  SELECT
    customer_id,
    MIN(order_date) as first_purchase_date,
    MAX(order_date) as last_purchase_date,
    COUNT(DISTINCT order_id) as total_orders,
    SUM(amount) as total_revenue,
    AVG(amount) as avg_order_value,
    DATE_DIFF(MAX(order_date), MIN(order_date), DAY) + 1 as customer_lifespan_days
  FROM orders
  GROUP BY customer_id
),
clv_calculation AS (
  SELECT
    customer_id,
    total_revenue as historical_clv,
    
    -- Average order frequency (orders per day)
    total_orders / NULLIF(customer_lifespan_days, 0) as order_frequency_daily,
    
    -- Predicted CLV (simple model)
    avg_order_value * 
    (total_orders / NULLIF(customer_lifespan_days, 0)) * 
    365 as predicted_annual_clv,
    
    -- Customer segments based on CLV
    NTILE(5) OVER (ORDER BY total_revenue) as clv_quintile
  FROM customer_metrics
  WHERE customer_lifespan_days > 0
)
SELECT
  clv_quintile,
  COUNT(*) as customers,
  AVG(historical_clv) as avg_historical_clv,
  AVG(predicted_annual_clv) as avg_predicted_clv,
  SUM(historical_clv) as total_clv_contribution
FROM clv_calculation
GROUP BY clv_quintile
ORDER BY clv_quintile DESC;
```

### Q78: How do you perform churn prediction analysis in BigQuery?
**Answer:**
**Churn Analysis:**

```sql
-- Feature engineering for churn prediction
WITH customer_features AS (
  SELECT
    customer_id,
    
    -- Recency features
    DATE_DIFF(CURRENT_DATE(), MAX(order_date), DAY) as days_since_last_order,
    
    -- Frequency features
    COUNT(DISTINCT order_id) as total_orders,
    COUNT(DISTINCT order_id) / 
      NULLIF(DATE_DIFF(MAX(order_date), MIN(order_date), DAY), 0) as order_frequency,
    
    -- Monetary features
    SUM(amount) as total_spent,
    AVG(amount) as avg_order_value,
    
    -- Behavioral features
    COUNT(DISTINCT product_category) as categories_purchased,
    STDDEV(amount) as order_value_volatility,
    
    -- Trend features
    SUM(CASE WHEN order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY) 
             THEN amount ELSE 0 END) as recent_90d_spent,
    COUNT(CASE WHEN order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY) 
               THEN order_id END) as recent_90d_orders
  FROM orders
  GROUP BY customer_id
),
churn_labels AS (
  SELECT
    customer_id,
    CASE
      WHEN days_since_last_order > 180 THEN 1  -- Churned
      ELSE 0  -- Active
    END as churned,
    
    -- Risk scoring
    CASE
      WHEN days_since_last_order > 120 THEN 'High Risk'
      WHEN days_since_last_order > 60 THEN 'Medium Risk'
      ELSE 'Low Risk'
    END as churn_risk_category
  FROM customer_features
)
SELECT
  churn_risk_category,
  COUNT(*) as customers,
  AVG(cf.total_spent) as avg_total_spent,
  AVG(cf.days_since_last_order) as avg_days_since_last_order,
  SUM(cl.churned) / COUNT(*) as actual_churn_rate
FROM customer_features cf
JOIN churn_labels cl USING (customer_id)
GROUP BY churn_risk_category
ORDER BY 
  CASE churn_risk_category
    WHEN 'High Risk' THEN 1
    WHEN 'Medium Risk' THEN 2
    WHEN 'Low Risk' THEN 3
  END;
```

### Q79: How do you implement A/B testing analysis in BigQuery?
**Answer:**
**A/B Testing Analysis:**

```sql
-- A/B test results analysis
WITH test_results AS (
  SELECT
    user_id,
    test_group,  -- 'A' or 'B'
    converted,   -- 1 if converted, 0 if not
    revenue
  FROM ab_test_data
  WHERE test_start_date >= '2024-01-01'
    AND test_end_date <= '2024-01-31'
),
group_metrics AS (
  SELECT
    test_group,
    COUNT(*) as sample_size,
    SUM(converted) as conversions,
    SUM(converted) / COUNT(*) as conversion_rate,
    AVG(revenue) as avg_revenue_per_user,
    STDDEV(revenue) as revenue_std_dev,
    
    -- Confidence intervals for conversion rate
    SUM(converted) / COUNT(*) - 
    1.96 * SQRT((SUM(converted) / COUNT(*)) * (1 - SUM(converted) / COUNT(*)) / COUNT(*)) as ci_lower,
    SUM(converted) / COUNT(*) + 
    1.96 * SQRT((SUM(converted) / COUNT(*)) * (1 - SUM(converted) / COUNT(*)) / COUNT(*)) as ci_upper
  FROM test_results
  GROUP BY test_group
),
statistical_significance AS (
  SELECT
    a.conversion_rate as group_a_rate,
    b.conversion_rate as group_b_rate,
    ABS(a.conversion_rate - b.conversion_rate) as rate_difference,
    
    -- Z-test for proportions
    ABS(a.conversion_rate - b.conversion_rate) / 
    SQRT(
      ((a.conversions + b.conversions) / (a.sample_size + b.sample_size)) *
      (1 - (a.conversions + b.conversions) / (a.sample_size + b.sample_size)) *
      (1/a.sample_size + 1/b.sample_size)
    ) as z_score,
    
    -- Statistical significance (z > 1.96 for 95% confidence)
    CASE
      WHEN ABS(a.conversion_rate - b.conversion_rate) / 
           SQRT(
             ((a.conversions + b.conversions) / (a.sample_size + b.sample_size)) *
             (1 - (a.conversions + b.conversions) / (a.sample_size + b.sample_size)) *
             (1/a.sample_size + 1/b.sample_size)
           ) > 1.96 THEN 'Significant'
      ELSE 'Not Significant'
    END as significance
  FROM group_metrics a
  CROSS JOIN group_metrics b
  WHERE a.test_group = 'A' AND b.test_group = 'B'
)
SELECT
  'Group A' as group_name,
  sample_size,
  conversions,
  ROUND(conversion_rate * 100, 2) as conversion_rate_pct,
  ROUND(avg_revenue_per_user, 2) as avg_revenue,
  ROUND(ci_lower * 100, 2) as ci_lower_pct,
  ROUND(ci_upper * 100, 2) as ci_upper_pct
FROM group_metrics
WHERE test_group = 'A'

UNION ALL

SELECT
  'Group B' as group_name,
  sample_size,
  conversions,
  ROUND(conversion_rate * 100, 2) as conversion_rate_pct,
  ROUND(avg_revenue_per_user, 2) as avg_revenue,
  ROUND(ci_lower * 100, 2) as ci_lower_pct,
  ROUND(ci_upper * 100, 2) as ci_upper_pct
FROM group_metrics
WHERE test_group = 'B';
```

### Q80: How do you implement advanced segmentation analysis?
**Answer:**
**Advanced Segmentation:**

```sql
-- Multi-dimensional customer segmentation
WITH customer_behavior AS (
  SELECT
    customer_id,
    
    -- Purchase behavior
    COUNT(DISTINCT order_id) as order_frequency,
    AVG(amount) as avg_order_value,
    SUM(amount) as total_spent,
    
    -- Temporal behavior
    DATE_DIFF(CURRENT_DATE(), MAX(order_date), DAY) as recency,
    DATE_DIFF(MAX(order_date), MIN(order_date), DAY) as customer_tenure,
    
    -- Product diversity
    COUNT(DISTINCT product_category) as category_diversity,
    COUNT(DISTINCT brand) as brand_diversity,
    
    -- Channel behavior
    COUNT(DISTINCT channel) as channel_usage,
    COUNTIF(channel = 'online') / COUNT(*) as online_preference
  FROM orders o
  JOIN products p USING (product_id)
  GROUP BY customer_id
),
segmentation_scores AS (
  SELECT
    customer_id,
    
    -- Normalize metrics to 0-1 scale
    (order_frequency - MIN(order_frequency) OVER()) / 
    NULLIF(MAX(order_frequency) OVER() - MIN(order_frequency) OVER(), 0) as frequency_score,
    
    (total_spent - MIN(total_spent) OVER()) / 
    NULLIF(MAX(total_spent) OVER() - MIN(total_spent) OVER(), 0) as monetary_score,
    
    1 - (recency - MIN(recency) OVER()) / 
    NULLIF(MAX(recency) OVER() - MIN(recency) OVER(), 0) as recency_score,
    
    (category_diversity - MIN(category_diversity) OVER()) / 
    NULLIF(MAX(category_diversity) OVER() - MIN(category_diversity) OVER(), 0) as diversity_score
  FROM customer_behavior
),
customer_segments AS (
  SELECT
    customer_id,
    frequency_score,
    monetary_score,
    recency_score,
    diversity_score,
    
    -- Composite scoring
    (frequency_score + monetary_score + recency_score + diversity_score) / 4 as composite_score,
    
    -- Rule-based segmentation
    CASE
      WHEN frequency_score >= 0.8 AND monetary_score >= 0.8 AND recency_score >= 0.8 THEN 'VIP Champions'
      WHEN frequency_score >= 0.6 AND monetary_score >= 0.6 AND recency_score >= 0.6 THEN 'Loyal Customers'
      WHEN recency_score >= 0.7 AND frequency_score <= 0.3 THEN 'New Customers'
      WHEN recency_score <= 0.3 AND frequency_score >= 0.5 THEN 'At Risk'
      WHEN recency_score <= 0.3 AND frequency_score <= 0.3 THEN 'Lost Customers'
      ELSE 'Developing'
    END as segment
  FROM segmentation_scores
)
SELECT
  segment,
  COUNT(*) as customer_count,
  ROUND(AVG(composite_score), 3) as avg_composite_score,
  ROUND(AVG(frequency_score), 3) as avg_frequency_score,
  ROUND(AVG(monetary_score), 3) as avg_monetary_score,
  ROUND(AVG(recency_score), 3) as avg_recency_score,
  COUNT(*) / SUM(COUNT(*)) OVER() as segment_percentage
FROM customer_segments
GROUP BY segment
ORDER BY avg_composite_score DESC;
```

### Q81: How do you implement predictive analytics for demand forecasting?
**Answer:**
**Demand Forecasting:**

```sql
-- Historical demand patterns
WITH daily_demand AS (
  SELECT
    product_id,
    DATE(order_date) as date,
    SUM(quantity) as daily_quantity,
    SUM(amount) as daily_revenue
  FROM orders
  GROUP BY product_id, DATE(order_date)
),
demand_features AS (
  SELECT
    product_id,
    date,
    daily_quantity,
    
    -- Temporal features
    EXTRACT(MONTH FROM date) as month,
    EXTRACT(DAYOFWEEK FROM date) as day_of_week,
    EXTRACT(DAY FROM date) as day_of_month,
    
    -- Lag features
    LAG(daily_quantity, 1) OVER (PARTITION BY product_id ORDER BY date) as lag_1_day,
    LAG(daily_quantity, 7) OVER (PARTITION BY product_id ORDER BY date) as lag_7_day,
    LAG(daily_quantity, 30) OVER (PARTITION BY product_id ORDER BY date) as lag_30_day,
    
    -- Moving averages
    AVG(daily_quantity) OVER (
      PARTITION BY product_id 
      ORDER BY date 
      ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as ma_7_day,
    
    AVG(daily_quantity) OVER (
      PARTITION BY product_id 
      ORDER BY date 
      ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as ma_30_day,
    
    -- Trend features
    REGR_SLOPE(daily_quantity, UNIX_DATE(date)) OVER (
      PARTITION BY product_id 
      ORDER BY date 
      ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as trend_30_day
  FROM daily_demand
),
seasonality_analysis AS (
  SELECT
    product_id,
    month,
    day_of_week,
    AVG(daily_quantity) as avg_demand,
    STDDEV(daily_quantity) as demand_volatility,
    
    -- Seasonality index
    AVG(daily_quantity) / AVG(AVG(daily_quantity)) OVER (PARTITION BY product_id) as seasonality_index
  FROM demand_features
  WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY)
  GROUP BY product_id, month, day_of_week
)
SELECT
  df.product_id,
  df.date,
  df.daily_quantity as actual_demand,
  
  -- Simple forecast based on seasonality and trend
  sa.avg_demand * sa.seasonality_index + 
  COALESCE(df.trend_30_day * 30, 0) as forecasted_demand,
  
  -- Forecast accuracy metrics
  ABS(df.daily_quantity - (sa.avg_demand * sa.seasonality_index)) as forecast_error,
  ABS(df.daily_quantity - (sa.avg_demand * sa.seasonality_index)) / 
  NULLIF(df.daily_quantity, 0) as mape
FROM demand_features df
JOIN seasonality_analysis sa ON 
  df.product_id = sa.product_id AND 
  df.month = sa.month AND 
  df.day_of_week = sa.day_of_week
WHERE df.date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
ORDER BY df.product_id, df.date;
```

### Q82: How do you implement real-time analytics dashboards with BigQuery?
**Answer:**
**Real-time Dashboard Queries:**

```sql
-- Real-time KPI dashboard
WITH real_time_metrics AS (
  SELECT
    -- Current hour metrics
    COUNT(*) as current_hour_orders,
    SUM(amount) as current_hour_revenue,
    COUNT(DISTINCT customer_id) as current_hour_customers,
    AVG(amount) as current_hour_aov
  FROM orders
  WHERE timestamp >= TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), HOUR)
),
comparison_metrics AS (
  SELECT
    -- Same hour yesterday
    COUNT(*) as yesterday_same_hour_orders,
    SUM(amount) as yesterday_same_hour_revenue
  FROM orders
  WHERE timestamp >= TIMESTAMP_SUB(TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), HOUR), INTERVAL 24 HOUR)
    AND timestamp < TIMESTAMP_SUB(TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), HOUR), INTERVAL 23 HOUR)
),
trending_data AS (
  SELECT
    TIMESTAMP_TRUNC(timestamp, MINUTE) as minute,
    COUNT(*) as orders_per_minute,
    SUM(amount) as revenue_per_minute
  FROM orders
  WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
  GROUP BY TIMESTAMP_TRUNC(timestamp, MINUTE)
  ORDER BY minute DESC
  LIMIT 60
)
SELECT
  -- Current performance
  rm.current_hour_orders,
  rm.current_hour_revenue,
  rm.current_hour_customers,
  rm.current_hour_aov,
  
  -- Growth rates
  SAFE_DIVIDE(rm.current_hour_orders - cm.yesterday_same_hour_orders, 
              cm.yesterday_same_hour_orders) * 100 as order_growth_pct,
  SAFE_DIVIDE(rm.current_hour_revenue - cm.yesterday_same_hour_revenue, 
              cm.yesterday_same_hour_revenue) * 100 as revenue_growth_pct,
  
  -- Trending data for charts
  ARRAY_AGG(STRUCT(td.minute, td.orders_per_minute, td.revenue_per_minute) 
            ORDER BY td.minute DESC LIMIT 60) as minute_by_minute_data
FROM real_time_metrics rm
CROSS JOIN comparison_metrics cm
CROSS JOIN trending_data td
GROUP BY rm.current_hour_orders, rm.current_hour_revenue, rm.current_hour_customers, 
         rm.current_hour_aov, cm.yesterday_same_hour_orders, cm.yesterday_same_hour_revenue;
```

### Q83: How do you implement data quality monitoring in BigQuery?
**Answer:**
**Data Quality Monitoring:**

```sql
-- Comprehensive data quality checks
WITH data_quality_checks AS (
  SELECT
    'orders' as table_name,
    CURRENT_TIMESTAMP() as check_timestamp,
    
    -- Completeness checks
    COUNT(*) as total_rows,
    COUNTIF(order_id IS NULL) as null_order_ids,
    COUNTIF(customer_id IS NULL) as null_customer_ids,
    COUNTIF(amount IS NULL) as null_amounts,
    
    -- Validity checks
    COUNTIF(amount < 0) as negative_amounts,
    COUNTIF(amount > 10000) as suspiciously_high_amounts,
    COUNTIF(order_date > CURRENT_DATE()) as future_dates,
    COUNTIF(order_date < '2020-01-01') as very_old_dates,
    
    -- Uniqueness checks
    COUNT(DISTINCT order_id) as unique_order_ids,
    COUNT(*) - COUNT(DISTINCT order_id) as duplicate_order_ids,
    
    -- Consistency checks
    COUNTIF(order_date != DATE(timestamp)) as date_timestamp_mismatches,
    
    -- Freshness checks
    MAX(timestamp) as latest_record,
    TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), MAX(timestamp), HOUR) as hours_since_latest
  FROM orders
  WHERE DATE(order_date) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
),
quality_scores AS (
  SELECT
    *,
    -- Calculate quality scores (0-100)
    100 * (1 - SAFE_DIVIDE(null_order_ids + null_customer_ids + null_amounts, total_rows * 3)) as completeness_score,
    100 * (1 - SAFE_DIVIDE(negative_amounts + suspiciously_high_amounts + future_dates + very_old_dates, total_rows * 4)) as validity_score,
    100 * (1 - SAFE_DIVIDE(duplicate_order_ids, total_rows)) as uniqueness_score,
    100 * (1 - SAFE_DIVIDE(date_timestamp_mismatches, total_rows)) as consistency_score,
    CASE
      WHEN hours_since_latest <= 1 THEN 100
      WHEN hours_since_latest <= 6 THEN 80
      WHEN hours_since_latest <= 24 THEN 60
      ELSE 0
    END as freshness_score
  FROM data_quality_checks
)
SELECT
  table_name,
  check_timestamp,
  total_rows,
  
  -- Quality scores
  ROUND(completeness_score, 1) as completeness_score,
  ROUND(validity_score, 1) as validity_score,
  ROUND(uniqueness_score, 1) as uniqueness_score,
  ROUND(consistency_score, 1) as consistency_score,
  freshness_score,
  
  -- Overall quality score
  ROUND((completeness_score + validity_score + uniqueness_score + consistency_score + freshness_score) / 5, 1) as overall_quality_score,
  
  -- Issue details
  STRUCT(
    null_order_ids,
    null_customer_ids,
    null_amounts,
    negative_amounts,
    suspiciously_high_amounts,
    duplicate_order_ids,
    hours_since_latest
  ) as quality_issues
FROM quality_scores;
```

### Q84: How do you implement advanced data profiling in BigQuery?
**Answer:**
**Data Profiling:**

```sql
-- Comprehensive data profiling
WITH column_profiles AS (
  SELECT
    'customer_id' as column_name,
    'STRING' as data_type,
    COUNT(*) as total_count,
    COUNT(customer_id) as non_null_count,
    COUNT(DISTINCT customer_id) as distinct_count,
    MIN(LENGTH(customer_id)) as min_length,
    MAX(LENGTH(customer_id)) as max_length,
    AVG(LENGTH(customer_id)) as avg_length,
    NULL as min_value,
    NULL as max_value,
    NULL as mean_value,
    NULL as std_dev
  FROM orders
  
  UNION ALL
  
  SELECT
    'amount' as column_name,
    'NUMERIC' as data_type,
    COUNT(*) as total_count,
    COUNT(amount) as non_null_count,
    COUNT(DISTINCT amount) as distinct_count,
    NULL as min_length,
    NULL as max_length,
    NULL as avg_length,
    CAST(MIN(amount) AS STRING) as min_value,
    CAST(MAX(amount) AS STRING) as max_value,
    CAST(AVG(amount) AS STRING) as mean_value,
    CAST(STDDEV(amount) AS STRING) as std_dev
  FROM orders
  
  UNION ALL
  
  SELECT
    'order_date' as column_name,
    'DATE' as data_type,
    COUNT(*) as total_count,
    COUNT(order_date) as non_null_count,
    COUNT(DISTINCT order_date) as distinct_count,
    NULL as min_length,
    NULL as max_length,
    NULL as avg_length,
    CAST(MIN(order_date) AS STRING) as min_value,
    CAST(MAX(order_date) AS STRING) as max_value,
    NULL as mean_value,
    NULL as std_dev
  FROM orders
),
pattern_analysis AS (
  SELECT
    'customer_id' as column_name,
    'Pattern Analysis' as analysis_type,
    ARRAY_AGG(
      STRUCT(
        pattern,
        count,
        ROUND(count / SUM(count) OVER() * 100, 2) as percentage
      ) ORDER BY count DESC LIMIT 10
    ) as top_patterns
  FROM (
    SELECT
      REGEXP_REPLACE(customer_id, r'\d', 'N') as pattern,
      COUNT(*) as count
    FROM orders
    WHERE customer_id IS NOT NULL
    GROUP BY pattern
  )
)
SELECT
  cp.column_name,
  cp.data_type,
  cp.total_count,
  cp.non_null_count,
  ROUND(cp.non_null_count / cp.total_count * 100, 2) as completeness_pct,
  cp.distinct_count,
  ROUND(cp.distinct_count / cp.non_null_count * 100, 2) as uniqueness_pct,
  cp.min_length,
  cp.max_length,
  ROUND(cp.avg_length, 1) as avg_length,
  cp.min_value,
  cp.max_value,
  cp.mean_value,
  cp.std_dev,
  pa.top_patterns
FROM column_profiles cp
LEFT JOIN pattern_analysis pa ON cp.column_name = pa.column_name
ORDER BY cp.column_name;
```

### Q85: How do you implement cross-platform analytics integration?
**Answer:**
**Cross-platform Integration:**

```sql
-- Unified analytics across platforms
WITH web_analytics AS (
  SELECT
    user_id,
    'web' as platform,
    session_id,
    page_views,
    session_duration,
    conversion_events,
    DATE(session_start) as date
  FROM web_sessions
),
mobile_analytics AS (
  SELECT
    user_id,
    'mobile' as platform,
    session_id,
    screen_views as page_views,
    session_duration,
    conversion_events,
    DATE(session_start) as date
  FROM mobile_sessions
),
email_analytics AS (
  SELECT
    user_id,
    'email' as platform,
    campaign_id as session_id,
    clicks as page_views,
    NULL as session_duration,
    conversions as conversion_events,
    DATE(sent_date) as date
  FROM email_campaigns
),
unified_analytics AS (
  SELECT * FROM web_analytics
  UNION ALL
  SELECT * FROM mobile_analytics
  UNION ALL
  SELECT * FROM email_analytics
),
cross_platform_metrics AS (
  SELECT
    user_id,
    date,
    COUNT(DISTINCT platform) as platforms_used,
    SUM(page_views) as total_page_views,
    AVG(session_duration) as avg_session_duration,
    SUM(conversion_events) as total_conversions,
    
    -- Platform preference
    ARRAY_AGG(
      STRUCT(platform, SUM(page_views) as views) 
      ORDER BY SUM(page_views) DESC
    )[OFFSET(0)].platform as primary_platform
  FROM unified_analytics
  GROUP BY user_id, date
)
SELECT
  date,
  platforms_used,
  COUNT(DISTINCT user_id) as users,
  AVG(total_page_views) as avg_page_views,
  AVG(total_conversions) as avg_conversions,
  
  -- Cross-platform behavior analysis
  COUNTIF(platforms_used = 1) / COUNT(*) as single_platform_users_pct,
  COUNTIF(platforms_used >= 2) / COUNT(*) as multi_platform_users_pct,
  
  -- Platform distribution
  COUNTIF(primary_platform = 'web') / COUNT(*) as web_primary_pct,
  COUNTIF(primary_platform = 'mobile') / COUNT(*) as mobile_primary_pct,
  COUNTIF(primary_platform = 'email') / COUNT(*) as email_primary_pct
FROM cross_platform_metrics
GROUP BY date, platforms_used
ORDER BY date DESC, platforms_used;
```

### Q86: How do you implement advanced attribution modeling?
**Answer:**
**Attribution Modeling:**

```sql
-- Multi-touch attribution analysis
WITH customer_journey AS (
  SELECT
    customer_id,
    conversion_id,
    touchpoint_timestamp,
    channel,
    campaign,
    conversion_value,
    ROW_NUMBER() OVER (
      PARTITION BY customer_id, conversion_id 
      ORDER BY touchpoint_timestamp
    ) as touchpoint_position,
    COUNT(*) OVER (
      PARTITION BY customer_id, conversion_id
    ) as total_touchpoints
  FROM customer_touchpoints
  WHERE conversion_id IS NOT NULL
),
attribution_models AS (
  SELECT
    customer_id,
    conversion_id,
    channel,
    campaign,
    conversion_value,
    touchpoint_position,
    total_touchpoints,
    
    -- First-touch attribution
    CASE WHEN touchpoint_position = 1 THEN conversion_value ELSE 0 END as first_touch_value,
    
    -- Last-touch attribution
    CASE WHEN touchpoint_position = total_touchpoints THEN conversion_value ELSE 0 END as last_touch_value,
    
    -- Linear attribution
    conversion_value / total_touchpoints as linear_attribution_value,
    
    -- Time-decay attribution (more recent touchpoints get more credit)
    conversion_value * POW(2, -(total_touchpoints - touchpoint_position)) / 
    SUM(POW(2, -(total_touchpoints - touchpoint_position))) OVER (
      PARTITION BY customer_id, conversion_id
    ) as time_decay_value,
    
    -- Position-based attribution (40% first, 40% last, 20% middle)
    CASE
      WHEN total_touchpoints = 1 THEN conversion_value
      WHEN touchpoint_position = 1 THEN conversion_value * 0.4
      WHEN touchpoint_position = total_touchpoints THEN conversion_value * 0.4
      ELSE conversion_value * 0.2 / (total_touchpoints - 2)
    END as position_based_value
  FROM customer_journey
)
SELECT
  channel,
  campaign,
  COUNT(DISTINCT conversion_id) as conversions,
  
  -- Attribution model results
  SUM(first_touch_value) as first_touch_revenue,
  SUM(last_touch_value) as last_touch_revenue,
  SUM(linear_attribution_value) as linear_attribution_revenue,
  SUM(time_decay_value) as time_decay_revenue,
  SUM(position_based_value) as position_based_revenue,
  
  -- Model comparison
  SUM(linear_attribution_value) / SUM(last_touch_value) as linear_vs_last_touch_ratio
FROM attribution_models
GROUP BY channel, campaign
ORDER BY linear_attribution_revenue DESC;
```

---

## Cost Management & Optimization

### Q87: How do you implement comprehensive cost monitoring in BigQuery?
**Answer:**
**Cost Monitoring Setup:**

```sql
-- Daily cost analysis
WITH daily_costs AS (
  SELECT
    DATE(creation_time) as query_date,
    user_email,
    project_id,
    job_type,
    SUM(total_bytes_processed) / POW(1024, 4) as tb_processed,
    SUM(total_bytes_processed) / POW(1024, 4) * 5 as estimated_cost_usd,
    COUNT(*) as query_count,
    SUM(total_slot_ms) / 1000 / 60 as slot_minutes
  FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
  WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  GROUP BY query_date, user_email, project_id, job_type
)
SELECT
  query_date,
  user_email,
  SUM(estimated_cost_usd) as daily_cost,
  SUM(tb_processed) as daily_tb_processed,
  SUM(query_count) as daily_queries,
  AVG(estimated_cost_usd / query_count) as avg_cost_per_query
FROM daily_costs
GROUP BY query_date, user_email
ORDER BY query_date DESC, daily_cost DESC;
```

### Q88: How do you set up cost controls and budgets?
**Answer:**
**Cost Control Implementation:**

```sql
-- Query cost estimation before execution
SELECT
  'Cost Estimation' as check_type,
  total_bytes_processed / POW(1024, 4) as estimated_tb,
  total_bytes_processed / POW(1024, 4) * 5 as estimated_cost_usd
FROM (
  SELECT COUNT(*) FROM `dataset.large_table`  -- DRY RUN
);

-- Set maximum bytes billed
SELECT *
FROM `dataset.expensive_table`
WHERE date >= '2024-01-01'
OPTIONS (maximum_bytes_billed = 10737418240);  -- 10GB limit

-- Cost-aware query patterns
CREATE OR REPLACE VIEW `dataset.cost_efficient_summary` AS
SELECT
  DATE(order_date) as date,
  customer_segment,
  SUM(amount) as total_revenue,
  COUNT(*) as order_count
FROM `dataset.orders`
WHERE DATE(order_date) >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
GROUP BY DATE(order_date), customer_segment;
```

### Q89: How do you optimize storage costs in BigQuery?
**Answer:**
**Storage Cost Optimization:**

```sql
-- Analyze table storage costs
SELECT
  table_schema,
  table_name,
  row_count,
  size_bytes / POW(1024, 3) as size_gb,
  size_bytes / POW(1024, 3) * 0.02 as monthly_storage_cost_usd,  -- $0.02 per GB
  partitioning_type,
  clustering_fields,
  
  -- Storage efficiency metrics
  CASE
    WHEN partitioning_type IS NOT NULL THEN 'Partitioned'
    ELSE 'Not Partitioned'
  END as partition_status,
  
  CASE
    WHEN clustering_fields IS NOT NULL THEN 'Clustered'
    ELSE 'Not Clustered'
  END as cluster_status
FROM `project.dataset.INFORMATION_SCHEMA.TABLES`
WHERE table_type = 'BASE TABLE'
ORDER BY size_gb DESC;

-- Identify unused tables
WITH table_usage AS (
  SELECT
    REGEXP_EXTRACT(query, r'FROM `([^`]+)`') as table_reference,
    MAX(creation_time) as last_queried
  FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
  WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
    AND query LIKE '%FROM%'
  GROUP BY table_reference
)
SELECT
  t.table_schema,
  t.table_name,
  t.size_bytes / POW(1024, 3) as size_gb,
  tu.last_queried,
  TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), tu.last_queried, DAY) as days_since_last_query,
  CASE
    WHEN tu.last_queried IS NULL THEN 'Never Queried'
    WHEN TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), tu.last_queried, DAY) > 90 THEN 'Unused (90+ days)'
    WHEN TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), tu.last_queried, DAY) > 30 THEN 'Rarely Used (30+ days)'
    ELSE 'Active'
  END as usage_status
FROM `project.dataset.INFORMATION_SCHEMA.TABLES` t
LEFT JOIN table_usage tu ON CONCAT('`', t.table_catalog, '.', t.table_schema, '.', t.table_name, '`') = tu.table_reference
WHERE t.table_type = 'BASE TABLE'
ORDER BY size_gb DESC;
```

### Q90: How do you implement slot-based cost optimization?
**Answer:**
**Slot Optimization:**

```sql
-- Analyze slot usage patterns
WITH hourly_slot_usage AS (
  SELECT
    TIMESTAMP_TRUNC(creation_time, HOUR) as hour,
    SUM(total_slot_ms) / 1000 / 60 as total_slot_minutes,
    COUNT(*) as query_count,
    AVG(total_slot_ms / 1000) as avg_slot_seconds_per_query
  FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
  WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
  GROUP BY hour
)
SELECT
  EXTRACT(HOUR FROM hour) as hour_of_day,
  AVG(total_slot_minutes) as avg_slot_minutes,
  MAX(total_slot_minutes) as peak_slot_minutes,
  AVG(query_count) as avg_queries_per_hour,
  
  -- Slot efficiency
  AVG(avg_slot_seconds_per_query) as avg_slot_seconds_per_query
FROM hourly_slot_usage
GROUP BY EXTRACT(HOUR FROM hour)
ORDER BY hour_of_day;

-- Reservation vs on-demand cost analysis
WITH slot_analysis AS (
  SELECT
    DATE(creation_time) as date,
    SUM(total_slot_ms) / 1000 / 60 / 60 as total_slot_hours,
    
    -- On-demand cost (based on bytes processed)
    SUM(total_bytes_processed) / POW(1024, 4) * 5 as on_demand_cost,
    
    -- Estimated flat-rate cost (100 slots = $2000/month)
    100 * 24 * 30 * (2000 / (100 * 24 * 30)) as flat_rate_daily_cost
  FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
  WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  GROUP BY date
)
SELECT
  date,
  total_slot_hours,
  on_demand_cost,
  flat_rate_daily_cost,
  on_demand_cost - flat_rate_daily_cost as cost_difference,
  CASE
    WHEN on_demand_cost > flat_rate_daily_cost THEN 'Flat-rate Better'
    ELSE 'On-demand Better'
  END as recommendation
FROM slot_analysis
ORDER BY date DESC;
```

### Q91: How do you optimize query costs through better SQL practices?
**Answer:**
**Query Cost Optimization:**

```sql
-- Cost-efficient query patterns

-- 1. Avoid SELECT *
-- Expensive:
SELECT * FROM large_table WHERE date = '2024-01-01';

-- Cost-efficient:
SELECT customer_id, amount, order_date 
FROM large_table 
WHERE date = '2024-01-01';

-- 2. Use partition pruning
-- Expensive (scans all partitions):
SELECT SUM(amount) FROM partitioned_table;

-- Cost-efficient (scans only needed partitions):
SELECT SUM(amount) 
FROM partitioned_table 
WHERE date BETWEEN '2024-01-01' AND '2024-01-31';

-- 3. Use clustering for JOINs
-- Create clustered tables for frequent JOIN keys
CREATE TABLE orders_clustered
CLUSTER BY customer_id
AS SELECT * FROM orders;

-- 4. Use approximate functions for large datasets
-- Expensive:
SELECT COUNT(DISTINCT customer_id) FROM large_table;

-- Cost-efficient:
SELECT APPROX_COUNT_DISTINCT(customer_id) FROM large_table;

-- 5. Optimize subqueries
-- Expensive (correlated subquery):
SELECT *
FROM customers c
WHERE (
  SELECT SUM(amount) 
  FROM orders o 
  WHERE o.customer_id = c.customer_id
) > 1000;

-- Cost-efficient (JOIN):
SELECT c.*
FROM customers c
JOIN (
  SELECT customer_id, SUM(amount) as total_amount
  FROM orders
  GROUP BY customer_id
  HAVING SUM(amount) > 1000
) o ON c.customer_id = o.customer_id;
```

### Q92: How do you implement cost allocation and chargeback?
**Answer:**
**Cost Allocation System:**

```sql
-- Cost allocation by department/team
WITH cost_allocation AS (
  SELECT
    user_email,
    DATE(creation_time) as date,
    
    -- Extract department from email or use lookup table
    CASE
      WHEN user_email LIKE '%marketing%' THEN 'Marketing'
      WHEN user_email LIKE '%finance%' THEN 'Finance'
      WHEN user_email LIKE '%engineering%' THEN 'Engineering'
      ELSE 'Other'
    END as department,
    
    -- Cost calculations
    SUM(total_bytes_processed) / POW(1024, 4) * 5 as query_cost,
    COUNT(*) as query_count,
    SUM(total_slot_ms) / 1000 / 60 as slot_minutes
  FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
  WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  GROUP BY user_email, date, department
),
department_summary AS (
  SELECT
    department,
    date,
    SUM(query_cost) as daily_cost,
    SUM(query_count) as daily_queries,
    COUNT(DISTINCT user_email) as active_users,
    AVG(query_cost / query_count) as avg_cost_per_query
  FROM cost_allocation
  GROUP BY department, date
)
SELECT
  department,
  SUM(daily_cost) as total_monthly_cost,
  AVG(daily_cost) as avg_daily_cost,
  SUM(daily_queries) as total_queries,
  AVG(active_users) as avg_daily_users,
  SUM(daily_cost) / SUM(SUM(daily_cost)) OVER() * 100 as cost_percentage
FROM department_summary
GROUP BY department
ORDER BY total_monthly_cost DESC;

-- Project-level cost tracking
CREATE TABLE `dataset.cost_tracking` (
  date DATE,
  project_id STRING,
  department STRING,
  cost_center STRING,
  query_cost NUMERIC,
  storage_cost NUMERIC,
  total_cost NUMERIC
);

-- Daily cost insertion
INSERT INTO `dataset.cost_tracking`
SELECT
  CURRENT_DATE() as date,
  project_id,
  department,
  cost_center,
  SUM(query_cost) as query_cost,
  SUM(storage_cost) as storage_cost,
  SUM(query_cost + storage_cost) as total_cost
FROM daily_cost_calculations
GROUP BY project_id, department, cost_center;
```

### Q93: How do you optimize costs for streaming data?
**Answer:**
**Streaming Cost Optimization:**

```sql
-- Streaming insert cost analysis
WITH streaming_costs AS (
  SELECT
    DATE(timestamp) as date,
    table_name,
    COUNT(*) as insert_count,
    SUM(JSON_EXTRACT_SCALAR(payload, '$.bytes')) as total_bytes,
    
    -- Streaming insert pricing: $0.01 per 200MB
    SUM(JSON_EXTRACT_SCALAR(payload, '$.bytes')) / (200 * 1024 * 1024) * 0.01 as streaming_cost
  FROM `dataset.streaming_inserts_log`
  WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  GROUP BY date, table_name
)
SELECT
  table_name,
  SUM(streaming_cost) as monthly_streaming_cost,
  AVG(insert_count) as avg_daily_inserts,
  SUM(total_bytes) / POW(1024, 3) as total_gb_streamed
FROM streaming_costs
GROUP BY table_name
ORDER BY monthly_streaming_cost DESC;

-- Batch vs streaming cost comparison
WITH cost_comparison AS (
  SELECT
    'streaming' as method,
    SUM(streaming_cost) as total_cost,
    'Real-time availability' as benefit
  FROM streaming_costs
  
  UNION ALL
  
  SELECT
    'batch' as method,
    SUM(batch_load_cost) as total_cost,
    'Lower cost, delayed availability' as benefit
  FROM batch_load_costs
)
SELECT * FROM cost_comparison;
```

### Q94: How do you implement automated cost alerting?
**Answer:**
**Cost Alerting System:**

```sql
-- Daily cost monitoring with thresholds
WITH daily_costs AS (
  SELECT
    DATE(creation_time) as date,
    SUM(total_bytes_processed) / POW(1024, 4) * 5 as daily_cost,
    COUNT(*) as query_count
  FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
  WHERE DATE(creation_time) = CURRENT_DATE()
  GROUP BY date
),
cost_alerts AS (
  SELECT
    date,
    daily_cost,
    query_count,
    
    -- Define thresholds
    CASE
      WHEN daily_cost > 1000 THEN 'CRITICAL'
      WHEN daily_cost > 500 THEN 'WARNING'
      WHEN daily_cost > 200 THEN 'CAUTION'
      ELSE 'NORMAL'
    END as alert_level,
    
    -- Compare to historical average
    daily_cost / (
      SELECT AVG(daily_cost)
      FROM (
        SELECT
          DATE(creation_time) as hist_date,
          SUM(total_bytes_processed) / POW(1024, 4) * 5 as daily_cost
        FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
        WHERE DATE(creation_time) BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) 
                                      AND DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
        GROUP BY hist_date
      )
    ) as cost_ratio_to_avg
  FROM daily_costs
)
SELECT
  date,
  daily_cost,
  alert_level,
  cost_ratio_to_avg,
  CASE
    WHEN alert_level IN ('CRITICAL', 'WARNING') THEN 
      CONCAT('Alert: Daily BigQuery cost is $', CAST(ROUND(daily_cost, 2) AS STRING), 
             ' (', CAST(ROUND(cost_ratio_to_avg * 100, 1) AS STRING), '% of average)')
    ELSE 'Normal operations'
  END as alert_message
FROM cost_alerts;

-- User-specific cost alerts
WITH user_cost_analysis AS (
  SELECT
    user_email,
    DATE(creation_time) as date,
    SUM(total_bytes_processed) / POW(1024, 4) * 5 as user_daily_cost,
    COUNT(*) as user_query_count
  FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
  WHERE DATE(creation_time) = CURRENT_DATE()
  GROUP BY user_email, date
)
SELECT
  user_email,
  user_daily_cost,
  user_query_count,
  CASE
    WHEN user_daily_cost > 100 THEN 'High cost user - review queries'
    WHEN user_query_count > 100 THEN 'High volume user - optimize queries'
    ELSE 'Normal usage'
  END as user_alert
FROM user_cost_analysis
WHERE user_daily_cost > 50 OR user_query_count > 50
ORDER BY user_daily_cost DESC;
```

### Q95: How do you optimize costs for data exports?
**Answer:**
**Export Cost Optimization:**

```sql
-- Export cost analysis
WITH export_analysis AS (
  SELECT
    DATE(creation_time) as date,
    destination_uri,
    total_bytes_processed / POW(1024, 3) as gb_exported,
    
    -- Export pricing varies by destination
    CASE
      WHEN destination_uri LIKE 'gs://%' THEN 
        total_bytes_processed / POW(1024, 3) * 0.01  -- Cloud Storage export
      ELSE 0
    END as export_cost
  FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
  WHERE job_type = 'EXTRACT'
    AND creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
)
SELECT
  date,
  COUNT(*) as export_jobs,
  SUM(gb_exported) as total_gb_exported,
  SUM(export_cost) as total_export_cost,
  AVG(gb_exported) as avg_gb_per_export
FROM export_analysis
GROUP BY date
ORDER BY date DESC;

-- Optimize export queries
-- Instead of exporting entire table:
EXPORT DATA OPTIONS(
  uri='gs://bucket/export/*.csv',
  format='CSV',
  overwrite=true
) AS
SELECT * FROM large_table;  -- Expensive

-- Export only needed data:
EXPORT DATA OPTIONS(
  uri='gs://bucket/export/*.csv',
  format='CSV',
  overwrite=true
) AS
SELECT 
  customer_id,
  order_date,
  amount
FROM large_table
WHERE order_date >= '2024-01-01'
  AND amount > 0;  -- Cost-efficient
```

### Q96: How do you implement cost-aware data retention policies?
**Answer:**
**Data Retention Cost Management:**

```sql
-- Analyze storage costs by table age
WITH table_age_analysis AS (
  SELECT
    table_schema,
    table_name,
    creation_time,
    TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), creation_time, DAY) as table_age_days,
    size_bytes / POW(1024, 3) as size_gb,
    size_bytes / POW(1024, 3) * 0.02 as monthly_storage_cost,
    
    -- Categorize by age
    CASE
      WHEN TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), creation_time, DAY) > 365 THEN 'Archive Candidate'
      WHEN TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), creation_time, DAY) > 90 THEN 'Long-term Storage'
      ELSE 'Active Storage'
    END as retention_category
  FROM `project.dataset.INFORMATION_SCHEMA.TABLES`
  WHERE table_type = 'BASE TABLE'
)
SELECT
  retention_category,
  COUNT(*) as table_count,
  SUM(size_gb) as total_size_gb,
  SUM(monthly_storage_cost) as total_monthly_cost,
  AVG(table_age_days) as avg_age_days
FROM table_age_analysis
GROUP BY retention_category
ORDER BY total_monthly_cost DESC;

-- Implement automated archival
CREATE OR REPLACE PROCEDURE `dataset.archive_old_data`()
BEGIN
  -- Archive tables older than 1 year to cheaper storage
  FOR record IN (
    SELECT table_name
    FROM `project.dataset.INFORMATION_SCHEMA.TABLES`
    WHERE table_type = 'BASE TABLE'
      AND TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), creation_time, DAY) > 365
  ) DO
    -- Export to Cloud Storage (cheaper long-term storage)
    EXECUTE IMMEDIATE FORMAT(
      "EXPORT DATA OPTIONS(uri='gs://archive-bucket/%s/*.parquet', format='PARQUET') AS SELECT * FROM `dataset.%s`",
      record.table_name, record.table_name
    );
    
    -- Drop original table after successful export
    EXECUTE IMMEDIATE FORMAT("DROP TABLE `dataset.%s`", record.table_name);
  END FOR;
END;
```

### Q97: How do you optimize costs for machine learning workloads?
**Answer:**
**ML Cost Optimization:**

```sql
-- ML model training cost analysis
WITH ml_costs AS (
  SELECT
    DATE(creation_time) as date,
    REGEXP_EXTRACT(query, r'CREATE MODEL `([^`]+)`') as model_name,
    total_bytes_processed / POW(1024, 4) as tb_processed,
    total_bytes_processed / POW(1024, 4) * 5 as training_cost,
    total_slot_ms / 1000 / 60 / 60 as training_hours
  FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
  WHERE query LIKE '%CREATE MODEL%'
    AND creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
)
SELECT
  model_name,
  COUNT(*) as training_runs,
  SUM(training_cost) as total_training_cost,
  AVG(training_cost) as avg_cost_per_run,
  SUM(training_hours) as total_training_hours
FROM ml_costs
WHERE model_name IS NOT NULL
GROUP BY model_name
ORDER BY total_training_cost DESC;

-- Cost-efficient ML practices
-- 1. Use sampling for model development
CREATE MODEL `dataset.prototype_model`
OPTIONS(model_type='linear_reg') AS
SELECT *
FROM `dataset.training_data`
TABLESAMPLE SYSTEM (10 PERCENT);  -- Use 10% sample for prototyping

-- 2. Optimize feature selection
CREATE MODEL `dataset.optimized_model`
OPTIONS(model_type='linear_reg') AS
SELECT
  -- Only include high-importance features
  feature1,
  feature2,
  feature3,  -- Exclude low-importance features
  target
FROM `dataset.training_data`;

-- 3. Use incremental training
CREATE OR REPLACE MODEL `dataset.incremental_model`
OPTIONS(
  model_type='linear_reg',
  warm_start=true,
  warm_start_from='dataset.previous_model'
) AS
SELECT * FROM `dataset.new_training_data`;  -- Only new data
```

### Q98: How do you implement cross-project cost optimization?
**Answer:**
**Cross-project Cost Management:**

```sql
-- Multi-project cost analysis
WITH project_costs AS (
  SELECT
    project_id,
    DATE(creation_time) as date,
    SUM(total_bytes_processed) / POW(1024, 4) * 5 as daily_cost,
    COUNT(*) as query_count,
    COUNT(DISTINCT user_email) as active_users
  FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
  WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  GROUP BY project_id, date
)
SELECT
  project_id,
  SUM(daily_cost) as total_monthly_cost,
  AVG(daily_cost) as avg_daily_cost,
  SUM(query_count) as total_queries,
  AVG(active_users) as avg_daily_users,
  SUM(daily_cost) / SUM(query_count) as cost_per_query
FROM project_costs
GROUP BY project_id
ORDER BY total_monthly_cost DESC;

-- Shared dataset cost allocation
WITH shared_dataset_usage AS (
  SELECT
    project_id as consuming_project,
    REGEXP_EXTRACT(query, r'FROM `([^.]+)\.') as source_project,
    COUNT(*) as query_count,
    SUM(total_bytes_processed) / POW(1024, 4) * 5 as usage_cost
  FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
  WHERE query LIKE '%FROM `%'
    AND REGEXP_EXTRACT(query, r'FROM `([^.]+)\.') != project_id  -- Cross-project queries
  GROUP BY consuming_project, source_project
)
SELECT
  source_project,
  consuming_project,
  query_count,
  usage_cost,
  usage_cost / SUM(usage_cost) OVER (PARTITION BY source_project) * 100 as usage_percentage
FROM shared_dataset_usage
ORDER BY source_project, usage_cost DESC;
```

### Q99: How do you optimize costs for real-time analytics?
**Answer:**
**Real-time Analytics Cost Optimization:**

```sql
-- Real-time query cost analysis
WITH realtime_costs AS (
  SELECT
    TIMESTAMP_TRUNC(creation_time, HOUR) as hour,
    COUNT(*) as query_count,
    SUM(total_bytes_processed) / POW(1024, 4) * 5 as hourly_cost,
    AVG(total_bytes_processed) as avg_bytes_per_query,
    
    -- Identify real-time queries (frequent, small queries)
    COUNTIF(total_bytes_processed < 1024*1024*100) as small_queries,  -- < 100MB
    COUNTIF(TIMESTAMP_DIFF(end_time, start_time, SECOND) < 10) as fast_queries  -- < 10 seconds
  FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
  WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
  GROUP BY hour
)
SELECT
  EXTRACT(HOUR FROM hour) as hour_of_day,
  AVG(query_count) as avg_queries_per_hour,
  AVG(hourly_cost) as avg_cost_per_hour,
  AVG(small_queries) / AVG(query_count) * 100 as small_query_percentage,
  AVG(fast_queries) / AVG(query_count) * 100 as fast_query_percentage
FROM realtime_costs
GROUP BY EXTRACT(HOUR FROM hour)
ORDER BY hour_of_day;

-- Optimize with materialized views for real-time dashboards
CREATE MATERIALIZED VIEW `dataset.realtime_dashboard_mv`
OPTIONS (enable_refresh = true, refresh_interval_minutes = 5)
AS
SELECT
  TIMESTAMP_TRUNC(timestamp, MINUTE) as minute,
  COUNT(*) as events_per_minute,
  SUM(revenue) as revenue_per_minute,
  COUNT(DISTINCT user_id) as unique_users_per_minute
FROM `dataset.events`
WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR)
GROUP BY TIMESTAMP_TRUNC(timestamp, MINUTE);

-- Use the materialized view instead of raw data
SELECT *
FROM `dataset.realtime_dashboard_mv`
WHERE minute >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
ORDER BY minute DESC;
```

### Q100: How do you implement cost optimization governance?
**Answer:**
**Cost Governance Framework:**

```sql
-- Cost governance dashboard
CREATE OR REPLACE VIEW `dataset.cost_governance_dashboard` AS
WITH cost_metrics AS (
  SELECT
    DATE(creation_time) as date,
    user_email,
    project_id,
    SUM(total_bytes_processed) / POW(1024, 4) * 5 as daily_cost,
    COUNT(*) as query_count,
    SUM(total_slot_ms) / 1000 / 60 as slot_minutes,
    
    -- Cost efficiency metrics
    AVG(total_bytes_processed / GREATEST(TIMESTAMP_DIFF(end_time, start_time, SECOND), 1)) as bytes_per_second,
    COUNT(DISTINCT REGEXP_EXTRACT(query, r'FROM `([^`]+)`')) as tables_accessed
  FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
  WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  GROUP BY date, user_email, project_id
),
governance_metrics AS (
  SELECT
    date,
    user_email,
    project_id,
    daily_cost,
    query_count,
    
    -- Governance flags
    CASE WHEN daily_cost > 100 THEN 'High Cost User' ELSE 'Normal' END as cost_flag,
    CASE WHEN query_count > 100 THEN 'High Volume User' ELSE 'Normal' END as volume_flag,
    CASE WHEN daily_cost / query_count > 10 THEN 'Inefficient Queries' ELSE 'Efficient' END as efficiency_flag,
    
    -- Compliance scoring
    CASE
      WHEN daily_cost <= 50 AND query_count <= 50 THEN 100
      WHEN daily_cost <= 100 AND query_count <= 100 THEN 80
      WHEN daily_cost <= 200 AND query_count <= 200 THEN 60
      ELSE 40
    END as compliance_score
  FROM cost_metrics
)
SELECT
  date,
  user_email,
  project_id,
  daily_cost,
  query_count,
  cost_flag,
  volume_flag,
  efficiency_flag,
  compliance_score,
  
  -- Recommendations
  CASE
    WHEN cost_flag = 'High Cost User' AND efficiency_flag = 'Inefficient Queries' 
      THEN 'Review query optimization and partitioning strategies'
    WHEN volume_flag = 'High Volume User' 
      THEN 'Consider query caching and result reuse'
    WHEN compliance_score < 60 
      THEN 'Requires cost optimization review'
    ELSE 'Good cost management practices'
  END as recommendation
FROM governance_metrics;

-- Automated cost governance alerts
CREATE OR REPLACE PROCEDURE `dataset.cost_governance_check`()
BEGIN
  DECLARE alert_count INT64;
  
  -- Check for cost violations
  SET alert_count = (
    SELECT COUNT(*)
    FROM `dataset.cost_governance_dashboard`
    WHERE date = CURRENT_DATE()
      AND (cost_flag = 'High Cost User' OR compliance_score < 60)
  );
  
  -- Log alerts if violations found
  IF alert_count > 0 THEN
    INSERT INTO `dataset.cost_governance_alerts`
    SELECT
      CURRENT_TIMESTAMP() as alert_timestamp,
      'Cost Governance Violation' as alert_type,
      user_email,
      project_id,
      daily_cost,
      compliance_score,
      recommendation
    FROM `dataset.cost_governance_dashboard`
    WHERE date = CURRENT_DATE()
      AND (cost_flag = 'High Cost User' OR compliance_score < 60);
  END IF;
END;
```

### Q101: How do you implement predictive cost modeling?
**Answer:**
**Predictive Cost Modeling:**

```sql
-- Historical cost trend analysis for prediction
WITH daily_costs AS (
  SELECT
    DATE(creation_time) as date,
    SUM(total_bytes_processed) / POW(1024, 4) * 5 as daily_cost,
    COUNT(*) as query_count,
    COUNT(DISTINCT user_email) as active_users
  FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
  WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
  GROUP BY date
),
cost_trends AS (
  SELECT
    date,
    daily_cost,
    query_count,
    active_users,
    
    -- Moving averages for trend analysis
    AVG(daily_cost) OVER (
      ORDER BY date 
      ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as cost_7day_avg,
    
    AVG(daily_cost) OVER (
      ORDER BY date 
      ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as cost_30day_avg,
    
    -- Linear trend calculation
    REGR_SLOPE(daily_cost, UNIX_DATE(date)) OVER (
      ORDER BY date 
      ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as cost_trend_slope,
    
    -- Seasonality detection
    AVG(daily_cost) OVER (
      PARTITION BY EXTRACT(DAYOFWEEK FROM date)
      ORDER BY date
      ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as day_of_week_avg
  FROM daily_costs
),
cost_predictions AS (
  SELECT
    date,
    daily_cost,
    cost_7day_avg,
    cost_30day_avg,
    cost_trend_slope,
    
    -- Simple linear prediction for next 30 days
    cost_30day_avg + (cost_trend_slope * 30) as predicted_30day_cost,
    
    -- Seasonal adjustment
    (cost_30day_avg + (cost_trend_slope * 30)) * 
    (day_of_week_avg / cost_30day_avg) as seasonally_adjusted_prediction,
    
    -- Confidence intervals (simplified)
    STDDEV(daily_cost) OVER (
      ORDER BY date 
      ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as cost_volatility
  FROM cost_trends
)
SELECT
  date,
  daily_cost,
  predicted_30day_cost,
  seasonally_adjusted_prediction,
  cost_volatility,
  
  -- Prediction confidence
  CASE
    WHEN cost_volatility < 50 THEN 'High Confidence'
    WHEN cost_volatility < 100 THEN 'Medium Confidence'
    ELSE 'Low Confidence'
  END as prediction_confidence,
  
  -- Budget alerts
  CASE
    WHEN predicted_30day_cost > 1000 THEN 'Budget Alert: Projected monthly cost exceeds $1000'
    WHEN predicted_30day_cost > 500 THEN 'Budget Warning: Projected monthly cost exceeds $500'
    ELSE 'Within Budget'
  END as budget_alert
FROM cost_predictions
WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
ORDER BY date DESC;
```

---

## Data Integration

### Q102: How do you integrate BigQuery with external data sources?
**Answer:**
**External Data Integration:**

```sql
-- External table from Cloud Storage
CREATE OR REPLACE EXTERNAL TABLE `dataset.external_csv`
OPTIONS (
  format = 'CSV',
  uris = ['gs://bucket/data/*.csv'],
  skip_leading_rows = 1
);

-- External table from Google Sheets
CREATE OR REPLACE EXTERNAL TABLE `dataset.sheets_data`
OPTIONS (
  format = 'GOOGLE_SHEETS',
  uris = ['https://docs.google.com/spreadsheets/d/SHEET_ID'],
  skip_leading_rows = 1
);

-- Federated queries to Cloud SQL
SELECT *
FROM EXTERNAL_QUERY(
  'projects/PROJECT_ID/locations/LOCATION/connections/CONNECTION_ID',
  'SELECT customer_id, name FROM customers WHERE active = true'
);
```

### Q103: How do you implement real-time data ingestion?
**Answer:**
**Real-time Ingestion Methods:**

```python
# Streaming inserts
from google.cloud import bigquery

def stream_data_to_bigquery(rows):
    client = bigquery.Client()
    table_id = "project.dataset.table"
    
    errors = client.insert_rows_json(table_id, rows)
    if errors:
        print(f"Errors: {errors}")
    return len(errors) == 0

# Pub/Sub to BigQuery via Dataflow
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

def run_streaming_pipeline():
    options = PipelineOptions([
        '--project=PROJECT_ID',
        '--runner=DataflowRunner',
        '--streaming=true'
    ])
    
    with beam.Pipeline(options=options) as p:
        (p | 'Read from Pub/Sub' >> beam.io.ReadFromPubSub(subscription=subscription)
           | 'Parse JSON' >> beam.Map(json.loads)
           | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
               table='project:dataset.table',
               write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND))
```

### Q104: How do you handle schema evolution in BigQuery?
**Answer:**
**Schema Evolution Strategies:**

```sql
-- Add new columns (backward compatible)
ALTER TABLE `dataset.table`
ADD COLUMN new_field STRING;

-- Modify column descriptions
ALTER TABLE `dataset.table`
ALTER COLUMN existing_field SET OPTIONS (description = 'Updated description');

-- Handle schema changes in streaming
CREATE TABLE `dataset.flexible_table` (
  id STRING,
  data JSON,  -- Store flexible schema as JSON
  created_at TIMESTAMP
);

-- Extract structured data from JSON
SELECT
  id,
  JSON_EXTRACT_SCALAR(data, '$.customer_id') as customer_id,
  JSON_EXTRACT_SCALAR(data, '$.amount') as amount,
  created_at
FROM `dataset.flexible_table`;
```

### Q105: How do you implement data validation during ingestion?
**Answer:**
**Data Validation Patterns:**

```sql
-- Create staging table with validation
CREATE OR REPLACE TABLE `dataset.staging_orders` AS
SELECT
  order_id,
  customer_id,
  amount,
  order_date,
  
  -- Validation flags
  CASE
    WHEN order_id IS NULL THEN 'Missing order_id'
    WHEN amount < 0 THEN 'Negative amount'
    WHEN order_date > CURRENT_DATE() THEN 'Future date'
    ELSE 'Valid'
  END as validation_status
FROM `dataset.raw_orders`;

-- Insert only valid records
INSERT INTO `dataset.orders`
SELECT order_id, customer_id, amount, order_date
FROM `dataset.staging_orders`
WHERE validation_status = 'Valid';

-- Log validation errors
INSERT INTO `dataset.validation_errors`
SELECT
  CURRENT_TIMESTAMP() as error_timestamp,
  'orders' as table_name,
  order_id,
  validation_status as error_message
FROM `dataset.staging_orders`
WHERE validation_status != 'Valid';
```

### Q106: How do you implement CDC (Change Data Capture) with BigQuery?
**Answer:**
**CDC Implementation:**

```sql
-- CDC using merge operations
MERGE `dataset.target_table` T
USING (
  SELECT
    id,
    name,
    email,
    updated_at,
    operation  -- 'INSERT', 'UPDATE', 'DELETE'
  FROM `dataset.cdc_stream`
  WHERE DATE(updated_at) = CURRENT_DATE()
) S
ON T.id = S.id
WHEN MATCHED AND S.operation = 'UPDATE' THEN
  UPDATE SET name = S.name, email = S.email, updated_at = S.updated_at
WHEN MATCHED AND S.operation = 'DELETE' THEN
  DELETE
WHEN NOT MATCHED AND S.operation = 'INSERT' THEN
  INSERT (id, name, email, updated_at) VALUES (S.id, S.name, S.email, S.updated_at);

-- Track changes with versioning
CREATE TABLE `dataset.customer_history` (
  id STRING,
  name STRING,
  email STRING,
  valid_from TIMESTAMP,
  valid_to TIMESTAMP,
  is_current BOOLEAN
);

-- Insert new version and close previous
INSERT INTO `dataset.customer_history`
SELECT
  id,
  name,
  email,
  CURRENT_TIMESTAMP() as valid_from,
  TIMESTAMP('2999-12-31') as valid_to,
  true as is_current
FROM `dataset.updated_customers`;

UPDATE `dataset.customer_history`
SET valid_to = CURRENT_TIMESTAMP(), is_current = false
WHERE id IN (SELECT id FROM `dataset.updated_customers`)
  AND is_current = true;
```

### Q107: How do you implement data lineage tracking?
**Answer:**
**Data Lineage Implementation:**

```sql
-- Create lineage tracking table
CREATE TABLE `dataset.data_lineage` (
  job_id STRING,
  source_table STRING,
  target_table STRING,
  transformation_type STRING,
  created_timestamp TIMESTAMP,
  created_by STRING
);

-- Track lineage in ETL processes
INSERT INTO `dataset.data_lineage`
VALUES (
  GENERATE_UUID(),
  'dataset.raw_orders',
  'dataset.processed_orders',
  'aggregation',
  CURRENT_TIMESTAMP(),
  SESSION_USER()
);

-- Query lineage information
WITH RECURSIVE lineage_tree AS (
  SELECT
    source_table,
    target_table,
    transformation_type,
    1 as level
  FROM `dataset.data_lineage`
  WHERE target_table = 'dataset.final_report'
  
  UNION ALL
  
  SELECT
    dl.source_table,
    dl.target_table,
    dl.transformation_type,
    lt.level + 1
  FROM `dataset.data_lineage` dl
  JOIN lineage_tree lt ON dl.target_table = lt.source_table
  WHERE lt.level < 10  -- Prevent infinite recursion
)
SELECT * FROM lineage_tree
ORDER BY level, source_table;
```

### Q108: How do you handle large-scale data migrations to BigQuery?
**Answer:**
**Migration Strategies:**

```sql
-- Parallel data transfer
CREATE TABLE `dataset.migrated_data`
PARTITION BY DATE(created_date)
CLUSTER BY customer_id
AS
SELECT *
FROM `source_project.source_dataset.source_table`
WHERE DATE(created_date) BETWEEN '2024-01-01' AND '2024-01-31';

-- Incremental migration
CREATE OR REPLACE PROCEDURE `dataset.incremental_migration`(start_date DATE, end_date DATE)
BEGIN
  DECLARE current_date DATE DEFAULT start_date;
  
  WHILE current_date <= end_date DO
    INSERT INTO `dataset.target_table`
    SELECT *
    FROM `source_project.source_dataset.source_table`
    WHERE DATE(created_date) = current_date;
    
    SET current_date = DATE_ADD(current_date, INTERVAL 1 DAY);
  END WHILE;
END;

-- Data validation post-migration
WITH source_counts AS (
  SELECT
    DATE(created_date) as date,
    COUNT(*) as source_count,
    SUM(amount) as source_sum
  FROM `source_project.source_dataset.source_table`
  GROUP BY DATE(created_date)
),
target_counts AS (
  SELECT
    DATE(created_date) as date,
    COUNT(*) as target_count,
    SUM(amount) as target_sum
  FROM `dataset.target_table`
  GROUP BY DATE(created_date)
)
SELECT
  s.date,
  s.source_count,
  t.target_count,
  s.source_count - t.target_count as count_diff,
  s.source_sum - t.target_sum as sum_diff
FROM source_counts s
FULL OUTER JOIN target_counts t ON s.date = t.date
WHERE s.source_count != t.target_count OR ABS(s.source_sum - t.target_sum) > 0.01;
```

### Q109: How do you implement data quality monitoring during integration?
**Answer:**
**Integration Quality Monitoring:**

```sql
-- Real-time data quality checks
CREATE OR REPLACE VIEW `dataset.integration_quality_monitor` AS
WITH quality_metrics AS (
  SELECT
    'orders' as table_name,
    CURRENT_TIMESTAMP() as check_time,
    COUNT(*) as total_records,
    COUNTIF(order_id IS NULL) as null_ids,
    COUNTIF(amount < 0) as negative_amounts,
    COUNTIF(order_date > CURRENT_DATE()) as future_dates,
    MAX(created_at) as latest_record,
    TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), MAX(created_at), MINUTE) as minutes_since_latest
  FROM `dataset.orders`
  WHERE DATE(created_at) = CURRENT_DATE()
)
SELECT
  *,
  CASE
    WHEN minutes_since_latest > 60 THEN 'Data Freshness Issue'
    WHEN null_ids > 0 THEN 'Data Completeness Issue'
    WHEN negative_amounts > 0 THEN 'Data Validity Issue'
    ELSE 'Healthy'
  END as quality_status
FROM quality_metrics;

-- Automated quality alerts
CREATE OR REPLACE PROCEDURE `dataset.check_integration_quality`()
BEGIN
  DECLARE quality_issues INT64;
  
  SET quality_issues = (
    SELECT COUNT(*)
    FROM `dataset.integration_quality_monitor`
    WHERE quality_status != 'Healthy'
  );
  
  IF quality_issues > 0 THEN
    INSERT INTO `dataset.quality_alerts`
    SELECT
      CURRENT_TIMESTAMP() as alert_time,
      table_name,
      quality_status,
      'Integration quality issue detected' as message
    FROM `dataset.integration_quality_monitor`
    WHERE quality_status != 'Healthy';
  END IF;
END;
```

### Q110: How do you implement multi-cloud data integration?
**Answer:**
**Multi-cloud Integration:**

```sql
-- Connect to AWS S3 data
CREATE OR REPLACE EXTERNAL TABLE `dataset.aws_data`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://transfer-bucket/aws-data/*.parquet']  -- Data transferred via Storage Transfer Service
);

-- Connect to Azure data via external connection
SELECT *
FROM EXTERNAL_QUERY(
  'projects/PROJECT_ID/locations/US/connections/azure-connection',
  'SELECT * FROM azure_table WHERE date >= \'2024-01-01\''
);

-- Unified view across clouds
CREATE OR REPLACE VIEW `dataset.unified_customer_data` AS
SELECT
  'gcp' as source_cloud,
  customer_id,
  name,
  email
FROM `dataset.gcp_customers`

UNION ALL

SELECT
  'aws' as source_cloud,
  customer_id,
  name,
  email
FROM `dataset.aws_data`

UNION ALL

SELECT
  'azure' as source_cloud,
  customer_id,
  name,
  email
FROM EXTERNAL_QUERY(
  'projects/PROJECT_ID/locations/US/connections/azure-connection',
  'SELECT customer_id, name, email FROM customers'
);
```

### Q111: How do you handle API data integration?
**Answer:**
**API Integration Patterns:**

```python
# Cloud Function for API data ingestion
import functions_framework
from google.cloud import bigquery
import requests

@functions_framework.http
def ingest_api_data(request):
    client = bigquery.Client()
    table_id = "project.dataset.api_data"
    
    # Fetch data from API
    response = requests.get('https://api.example.com/data')
    data = response.json()
    
    # Transform and insert
    rows = []
    for item in data:
        rows.append({
            'id': item['id'],
            'value': item['value'],
            'timestamp': item['timestamp'],
            'ingested_at': datetime.utcnow().isoformat()
        })
    
    errors = client.insert_rows_json(table_id, rows)
    return {'status': 'success', 'rows_inserted': len(rows), 'errors': errors}

# Scheduled API ingestion
CREATE OR REPLACE PROCEDURE `dataset.scheduled_api_ingestion`()
BEGIN
  -- Call external API via Cloud Function
  CALL `dataset.call_api_function`();
  
  -- Process and validate data
  INSERT INTO `dataset.processed_api_data`
  SELECT
    id,
    value,
    PARSE_TIMESTAMP('%Y-%m-%dT%H:%M:%E*S', timestamp) as parsed_timestamp,
    ingested_at
  FROM `dataset.raw_api_data`
  WHERE DATE(ingested_at) = CURRENT_DATE()
    AND value IS NOT NULL;
END;
```

### Q112: How do you implement event-driven data integration?
**Answer:**
**Event-driven Integration:**

```sql
-- Event-driven processing with Pub/Sub triggers
CREATE OR REPLACE FUNCTION `dataset.process_event`(event_data JSON)
RETURNS STRING
LANGUAGE SQL AS (
  CASE JSON_EXTRACT_SCALAR(event_data, '$.event_type')
    WHEN 'order_created' THEN 'INSERT'
    WHEN 'order_updated' THEN 'UPDATE'
    WHEN 'order_deleted' THEN 'DELETE'
    ELSE 'UNKNOWN'
  END
);

-- Process events in real-time
WITH event_stream AS (
  SELECT
    JSON_EXTRACT_SCALAR(data, '$.order_id') as order_id,
    JSON_EXTRACT_SCALAR(data, '$.customer_id') as customer_id,
    CAST(JSON_EXTRACT_SCALAR(data, '$.amount') AS NUMERIC) as amount,
    `dataset.process_event`(data) as operation,
    CURRENT_TIMESTAMP() as processed_at
  FROM `dataset.pubsub_events`
  WHERE DATE(timestamp) = CURRENT_DATE()
)
SELECT
  operation,
  COUNT(*) as event_count,
  SUM(amount) as total_amount
FROM event_stream
GROUP BY operation;

-- Event sourcing pattern
CREATE TABLE `dataset.event_store` (
  event_id STRING,
  aggregate_id STRING,
  event_type STRING,
  event_data JSON,
  event_timestamp TIMESTAMP,
  version INT64
);

-- Rebuild state from events
WITH ordered_events AS (
  SELECT *
  FROM `dataset.event_store`
  WHERE aggregate_id = 'customer_123'
  ORDER BY version
)
SELECT
  aggregate_id,
  LAST_VALUE(JSON_EXTRACT_SCALAR(event_data, '$.name')) OVER (
    ORDER BY version ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) as current_name,
  LAST_VALUE(JSON_EXTRACT_SCALAR(event_data, '$.email')) OVER (
    ORDER BY version ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) as current_email
FROM ordered_events;
```

### Q113: How do you handle data format conversions during integration?
**Answer:**
**Format Conversion Strategies:**

```sql
-- JSON to structured data
SELECT
  JSON_EXTRACT_SCALAR(json_data, '$.customer.id') as customer_id,
  JSON_EXTRACT_SCALAR(json_data, '$.customer.name') as customer_name,
  CAST(JSON_EXTRACT_SCALAR(json_data, '$.order.amount') AS NUMERIC) as amount,
  PARSE_TIMESTAMP('%Y-%m-%dT%H:%M:%E*S', JSON_EXTRACT_SCALAR(json_data, '$.order.timestamp')) as order_timestamp
FROM `dataset.json_source`;

-- CSV parsing with error handling
SELECT
  SPLIT(csv_line, ',')[OFFSET(0)] as id,
  SPLIT(csv_line, ',')[OFFSET(1)] as name,
  SAFE_CAST(SPLIT(csv_line, ',')[OFFSET(2)] AS NUMERIC) as amount,
  CASE
    WHEN ARRAY_LENGTH(SPLIT(csv_line, ',')) != 3 THEN 'Invalid column count'
    WHEN SAFE_CAST(SPLIT(csv_line, ',')[OFFSET(2)] AS NUMERIC) IS NULL THEN 'Invalid amount'
    ELSE 'Valid'
  END as validation_status
FROM `dataset.csv_source`;

-- XML to JSON conversion (using external UDF)
CREATE TEMP FUNCTION xml_to_json(xml_string STRING)
RETURNS JSON
LANGUAGE js AS """
  // XML parsing logic here
  return JSON.parse(convertedJson);
""";

SELECT
  xml_to_json(xml_data) as json_data
FROM `dataset.xml_source`;
```

### Q114: How do you implement data deduplication during integration?
**Answer:**
**Deduplication Strategies:**

```sql
-- Remove exact duplicates
CREATE OR REPLACE TABLE `dataset.deduplicated_orders` AS
SELECT DISTINCT *
FROM `dataset.raw_orders`;

-- Remove duplicates based on business key
CREATE OR REPLACE TABLE `dataset.unique_customers` AS
SELECT
  customer_id,
  name,
  email,
  ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) as rn
FROM `dataset.raw_customers`
QUALIFY rn = 1;

-- Fuzzy deduplication for similar records
WITH similarity_scores AS (
  SELECT
    a.id as id_a,
    b.id as id_b,
    a.name as name_a,
    b.name as name_b,
    EDIT_DISTANCE(LOWER(a.name), LOWER(b.name)) as name_distance,
    EDIT_DISTANCE(a.email, b.email) as email_distance
  FROM `dataset.customers` a
  CROSS JOIN `dataset.customers` b
  WHERE a.id < b.id  -- Avoid comparing same record twice
)
SELECT
  id_a,
  id_b,
  name_a,
  name_b,
  name_distance,
  email_distance,
  CASE
    WHEN name_distance <= 2 AND email_distance <= 1 THEN 'Likely Duplicate'
    WHEN name_distance <= 5 AND email_distance <= 3 THEN 'Possible Duplicate'
    ELSE 'Different'
  END as duplicate_status
FROM similarity_scores
WHERE name_distance <= 5 OR email_distance <= 3
ORDER BY name_distance, email_distance;
```

### Q115: How do you implement data synchronization across systems?
**Answer:**
**Data Synchronization Patterns:**

```sql
-- Timestamp-based synchronization
CREATE OR REPLACE PROCEDURE `dataset.sync_customer_data`()
BEGIN
  DECLARE last_sync_time TIMESTAMP;
  
  -- Get last synchronization timestamp
  SET last_sync_time = (
    SELECT MAX(sync_timestamp)
    FROM `dataset.sync_log`
    WHERE table_name = 'customers'
  );
  
  -- Sync new/updated records
  MERGE `dataset.customers` T
  USING (
    SELECT *
    FROM EXTERNAL_QUERY(
      'projects/PROJECT_ID/locations/US/connections/source-db',
      CONCAT('SELECT * FROM customers WHERE updated_at > \'', 
             FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%E*S', last_sync_time), '\'')
    )
  ) S
  ON T.customer_id = S.customer_id
  WHEN MATCHED THEN
    UPDATE SET name = S.name, email = S.email, updated_at = S.updated_at
  WHEN NOT MATCHED THEN
    INSERT (customer_id, name, email, updated_at) 
    VALUES (S.customer_id, S.name, S.email, S.updated_at);
  
  -- Log synchronization
  INSERT INTO `dataset.sync_log`
  VALUES ('customers', CURRENT_TIMESTAMP(), @@row_count.last_modified_count);
END;

-- Checksum-based synchronization
WITH source_checksums AS (
  SELECT
    customer_id,
    FARM_FINGERPRINT(CONCAT(name, email, CAST(updated_at AS STRING))) as checksum
  FROM EXTERNAL_QUERY(
    'projects/PROJECT_ID/locations/US/connections/source-db',
    'SELECT customer_id, name, email, updated_at FROM customers'
  )
),
target_checksums AS (
  SELECT
    customer_id,
    FARM_FINGERPRINT(CONCAT(name, email, CAST(updated_at AS STRING))) as checksum
  FROM `dataset.customers`
)
SELECT
  COALESCE(s.customer_id, t.customer_id) as customer_id,
  CASE
    WHEN s.customer_id IS NULL THEN 'DELETE_FROM_TARGET'
    WHEN t.customer_id IS NULL THEN 'INSERT_TO_TARGET'
    WHEN s.checksum != t.checksum THEN 'UPDATE_TARGET'
    ELSE 'IN_SYNC'
  END as sync_action
FROM source_checksums s
FULL OUTER JOIN target_checksums t ON s.customer_id = t.customer_id
WHERE COALESCE(s.checksum, 0) != COALESCE(t.checksum, 0);
```

### Q116: How do you handle data transformation during integration?
**Answer:**
**Transformation Patterns:**

```sql
-- Complex data transformations
WITH transformed_data AS (
  SELECT
    customer_id,
    
    -- String transformations
    UPPER(TRIM(name)) as normalized_name,
    REGEXP_REPLACE(phone, r'[^0-9]', '') as clean_phone,
    
    -- Date transformations
    PARSE_DATE('%m/%d/%Y', date_string) as parsed_date,
    DATE_DIFF(CURRENT_DATE(), birth_date, YEAR) as age,
    
    -- Numeric transformations
    ROUND(amount * exchange_rate, 2) as amount_usd,
    CASE
      WHEN amount < 100 THEN 'Small'
      WHEN amount < 1000 THEN 'Medium'
      ELSE 'Large'
    END as amount_category,
    
    -- Array transformations
    ARRAY(
      SELECT TRIM(tag)
      FROM UNNEST(SPLIT(tags_string, ',')) as tag
      WHERE LENGTH(TRIM(tag)) > 0
    ) as tags_array,
    
    -- JSON transformations
    STRUCT(
      JSON_EXTRACT_SCALAR(metadata, '$.source') as source,
      CAST(JSON_EXTRACT_SCALAR(metadata, '$.priority') AS INT64) as priority
    ) as parsed_metadata
  FROM `dataset.raw_data`
)
SELECT * FROM transformed_data
WHERE normalized_name IS NOT NULL
  AND parsed_date IS NOT NULL;

-- Lookup enrichment
SELECT
  o.*,
  c.customer_name,
  c.customer_segment,
  p.product_name,
  p.category,
  CASE
    WHEN c.customer_segment = 'Premium' THEN o.amount * 0.95
    ELSE o.amount
  END as discounted_amount
FROM `dataset.orders` o
LEFT JOIN `dataset.customers` c ON o.customer_id = c.customer_id
LEFT JOIN `dataset.products` p ON o.product_id = p.product_id;
```

### Q117: How do you implement data archival strategies?
**Answer:**
**Archival Implementation:**

```sql
-- Time-based archival
CREATE OR REPLACE PROCEDURE `dataset.archive_old_data`(archive_date DATE)
BEGIN
  -- Move old data to archive table
  INSERT INTO `dataset.orders_archive`
  SELECT *, CURRENT_TIMESTAMP() as archived_at
  FROM `dataset.orders`
  WHERE order_date < archive_date;
  
  -- Delete archived data from main table
  DELETE FROM `dataset.orders`
  WHERE order_date < archive_date;
  
  -- Log archival operation
  INSERT INTO `dataset.archival_log`
  VALUES (
    'orders',
    archive_date,
    CURRENT_TIMESTAMP(),
    @@row_count.last_modified_count
  );
END;

-- Export to cheaper storage
EXPORT DATA OPTIONS(
  uri='gs://archive-bucket/orders/year=2023/*.parquet',
  format='PARQUET',
  overwrite=true
) AS
SELECT *
FROM `dataset.orders`
WHERE EXTRACT(YEAR FROM order_date) = 2023;

-- Create external table for archived data
CREATE OR REPLACE EXTERNAL TABLE `dataset.orders_2023_archive`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://archive-bucket/orders/year=2023/*.parquet']
);

-- Unified view of current and archived data
CREATE OR REPLACE VIEW `dataset.orders_complete` AS
SELECT *, 'current' as data_location
FROM `dataset.orders`

UNION ALL

SELECT *, 'archived' as data_location
FROM `dataset.orders_2023_archive`;
```

### Q118: How do you implement data quality rules during integration?
**Answer:**
**Quality Rules Implementation:**

```sql
-- Define data quality rules
CREATE TABLE `dataset.quality_rules` (
  rule_id STRING,
  table_name STRING,
  column_name STRING,
  rule_type STRING,
  rule_definition STRING,
  severity STRING
);

INSERT INTO `dataset.quality_rules` VALUES
('R001', 'orders', 'order_id', 'NOT_NULL', 'order_id IS NOT NULL', 'CRITICAL'),
('R002', 'orders', 'amount', 'RANGE', 'amount > 0 AND amount < 100000', 'HIGH'),
('R003', 'orders', 'email', 'FORMAT', 'REGEXP_CONTAINS(email, r\'@\')', 'MEDIUM');

-- Execute quality checks
CREATE OR REPLACE PROCEDURE `dataset.run_quality_checks`(target_table STRING)
BEGIN
  DECLARE rule_cursor CURSOR FOR
    SELECT rule_id, column_name, rule_definition, severity
    FROM `dataset.quality_rules`
    WHERE table_name = target_table;
  
  FOR rule IN rule_cursor DO
    EXECUTE IMMEDIATE FORMAT(
      "INSERT INTO `dataset.quality_violations` 
       SELECT '%s' as rule_id, '%s' as column_name, '%s' as severity, 
              COUNT(*) as violation_count, CURRENT_TIMESTAMP() as check_time
       FROM `dataset.%s` WHERE NOT (%s)",
      rule.rule_id, rule.column_name, rule.severity, target_table, rule.rule_definition
    );
  END FOR;
END;

-- Quality score calculation
WITH quality_metrics AS (
  SELECT
    table_name,
    SUM(CASE WHEN severity = 'CRITICAL' THEN violation_count * 10 ELSE 0 END) as critical_score,
    SUM(CASE WHEN severity = 'HIGH' THEN violation_count * 5 ELSE 0 END) as high_score,
    SUM(CASE WHEN severity = 'MEDIUM' THEN violation_count * 2 ELSE 0 END) as medium_score,
    SUM(violation_count) as total_violations
  FROM `dataset.quality_violations`
  WHERE DATE(check_time) = CURRENT_DATE()
  GROUP BY table_name
)
SELECT
  table_name,
  total_violations,
  critical_score + high_score + medium_score as weighted_score,
  CASE
    WHEN critical_score > 0 THEN 'FAIL'
    WHEN high_score > 10 THEN 'WARNING'
    WHEN medium_score > 20 THEN 'CAUTION'
    ELSE 'PASS'
  END as quality_status
FROM quality_metrics;
```

### Q119: How do you implement cross-region data replication?
**Answer:**
**Cross-region Replication:**

```sql
-- Set up cross-region dataset replication
CREATE DATASET `us_dataset`
OPTIONS (location = 'US');

CREATE DATASET `eu_dataset`
OPTIONS (location = 'EU');

-- Replicate data across regions
CREATE OR REPLACE PROCEDURE `dataset.replicate_to_eu`()
BEGIN
  -- Copy US data to EU region
  CREATE OR REPLACE TABLE `eu_dataset.orders`
  CLUSTER BY customer_id
  AS SELECT * FROM `us_dataset.orders`;
  
  -- Log replication
  INSERT INTO `us_dataset.replication_log`
  VALUES (
    'orders',
    'US',
    'EU',
    CURRENT_TIMESTAMP(),
    @@row_count.last_modified_count
  );
END;

-- Bi-directional sync with conflict resolution
CREATE OR REPLACE PROCEDURE `dataset.bidirectional_sync`()
BEGIN
  -- Sync US to EU (newer records win)
  MERGE `eu_dataset.orders` T
  USING (
    SELECT *
    FROM `us_dataset.orders`
    WHERE updated_at > (
      SELECT COALESCE(MAX(last_sync_time), TIMESTAMP('1900-01-01'))
      FROM `us_dataset.sync_metadata`
      WHERE source_region = 'US' AND target_region = 'EU'
    )
  ) S
  ON T.order_id = S.order_id
  WHEN MATCHED AND S.updated_at > T.updated_at THEN
    UPDATE SET amount = S.amount, status = S.status, updated_at = S.updated_at
  WHEN NOT MATCHED THEN
    INSERT (order_id, customer_id, amount, status, updated_at)
    VALUES (S.order_id, S.customer_id, S.amount, S.status, S.updated_at);
  
  -- Update sync metadata
  MERGE `us_dataset.sync_metadata` T
  USING (SELECT 'US' as source_region, 'EU' as target_region, CURRENT_TIMESTAMP() as sync_time) S
  ON T.source_region = S.source_region AND T.target_region = S.target_region
  WHEN MATCHED THEN
    UPDATE SET last_sync_time = S.sync_time
  WHEN NOT MATCHED THEN
    INSERT (source_region, target_region, last_sync_time)
    VALUES (S.source_region, S.target_region, S.sync_time);
END;
```

### Q120: How do you implement data pipeline monitoring and alerting?
**Answer:**
**Pipeline Monitoring:**

```sql
-- Pipeline health monitoring
CREATE OR REPLACE VIEW `dataset.pipeline_health` AS
WITH pipeline_metrics AS (
  SELECT
    'orders_pipeline' as pipeline_name,
    COUNT(*) as records_processed,
    MAX(processed_at) as last_run_time,
    TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), MAX(processed_at), MINUTE) as minutes_since_last_run,
    COUNTIF(status = 'ERROR') as error_count,
    AVG(processing_duration_seconds) as avg_processing_time
  FROM `dataset.pipeline_log`
  WHERE DATE(processed_at) = CURRENT_DATE()
  
  UNION ALL
  
  SELECT
    'customers_pipeline' as pipeline_name,
    COUNT(*) as records_processed,
    MAX(processed_at) as last_run_time,
    TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), MAX(processed_at), MINUTE) as minutes_since_last_run,
    COUNTIF(status = 'ERROR') as error_count,
    AVG(processing_duration_seconds) as avg_processing_time
  FROM `dataset.customer_pipeline_log`
  WHERE DATE(processed_at) = CURRENT_DATE()
)
SELECT
  pipeline_name,
  records_processed,
  last_run_time,
  minutes_since_last_run,
  error_count,
  avg_processing_time,
  CASE
    WHEN minutes_since_last_run > 120 THEN 'STALE'
    WHEN error_count > 0 THEN 'ERRORS'
    WHEN avg_processing_time > 300 THEN 'SLOW'
    ELSE 'HEALTHY'
  END as health_status
FROM pipeline_metrics;

-- Automated alerting
CREATE OR REPLACE PROCEDURE `dataset.check_pipeline_health`()
BEGIN
  DECLARE alert_count INT64;
  
  SET alert_count = (
    SELECT COUNT(*)
    FROM `dataset.pipeline_health`
    WHERE health_status != 'HEALTHY'
  );
  
  IF alert_count > 0 THEN
    INSERT INTO `dataset.pipeline_alerts`
    SELECT
      CURRENT_TIMESTAMP() as alert_time,
      pipeline_name,
      health_status,
      CASE health_status
        WHEN 'STALE' THEN CONCAT('Pipeline has not run for ', CAST(minutes_since_last_run AS STRING), ' minutes')
        WHEN 'ERRORS' THEN CONCAT('Pipeline has ', CAST(error_count AS STRING), ' errors')
        WHEN 'SLOW' THEN CONCAT('Pipeline average processing time is ', CAST(ROUND(avg_processing_time, 2) AS STRING), ' seconds')
      END as alert_message
    FROM `dataset.pipeline_health`
    WHERE health_status != 'HEALTHY';
  END IF;
END;

-- SLA monitoring
WITH sla_metrics AS (
  SELECT
    pipeline_name,
    DATE(processed_at) as date,
    COUNT(*) as total_runs,
    COUNTIF(processing_duration_seconds <= 300) as runs_within_sla,  -- 5 minute SLA
    AVG(processing_duration_seconds) as avg_duration,
    MAX(processing_duration_seconds) as max_duration
  FROM `dataset.pipeline_log`
  WHERE DATE(processed_at) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
  GROUP BY pipeline_name, DATE(processed_at)
)
SELECT
  pipeline_name,
  AVG(runs_within_sla / total_runs * 100) as sla_compliance_pct,
  AVG(avg_duration) as avg_processing_time,
  MAX(max_duration) as worst_processing_time
FROM sla_metrics
GROUP BY pipeline_name
ORDER BY sla_compliance_pct DESC;
```

### Q121: How do you implement data versioning and rollback capabilities?
**Answer:**
**Data Versioning System:**

```sql
-- Create versioned table structure
CREATE TABLE `dataset.orders_versioned` (
  order_id STRING,
  customer_id STRING,
  amount NUMERIC,
  status STRING,
  version_id STRING,
  version_timestamp TIMESTAMP,
  operation_type STRING,  -- INSERT, UPDATE, DELETE
  is_current BOOLEAN
);

-- Version management procedure
CREATE OR REPLACE PROCEDURE `dataset.create_data_version`(version_name STRING)
BEGIN
  DECLARE version_id STRING;
  SET version_id = CONCAT(version_name, '_', FORMAT_TIMESTAMP('%Y%m%d_%H%M%S', CURRENT_TIMESTAMP()));
  
  -- Create snapshot of current data
  INSERT INTO `dataset.orders_versioned`
  SELECT
    order_id,
    customer_id,
    amount,
    status,
    version_id,
    CURRENT_TIMESTAMP() as version_timestamp,
    'SNAPSHOT' as operation_type,
    true as is_current
  FROM `dataset.orders`;
  
  -- Mark previous versions as not current
  UPDATE `dataset.orders_versioned`
  SET is_current = false
  WHERE version_id != version_id AND is_current = true;
  
  -- Log version creation
  INSERT INTO `dataset.version_log`
  VALUES (version_id, version_name, CURRENT_TIMESTAMP(), @@row_count.last_modified_count);
END;

-- Rollback to specific version
CREATE OR REPLACE PROCEDURE `dataset.rollback_to_version`(target_version_id STRING)
BEGIN
  -- Backup current state
  CALL `dataset.create_data_version`('pre_rollback_backup');
  
  -- Replace current data with target version
  CREATE OR REPLACE TABLE `dataset.orders` AS
  SELECT order_id, customer_id, amount, status
  FROM `dataset.orders_versioned`
  WHERE version_id = target_version_id;
  
  -- Log rollback operation
  INSERT INTO `dataset.rollback_log`
  VALUES (target_version_id, CURRENT_TIMESTAMP(), SESSION_USER());
END;

-- Compare versions
WITH version_comparison AS (
  SELECT
    order_id,
    'v1' as version,
    amount as v1_amount,
    status as v1_status
  FROM `dataset.orders_versioned`
  WHERE version_id = 'version_1'
  
  UNION ALL
  
  SELECT
    order_id,
    'v2' as version,
    amount as v2_amount,
    status as v2_status
  FROM `dataset.orders_versioned`
  WHERE version_id = 'version_2'
)
SELECT
  order_id,
  v1_amount,
  v2_amount,
  v1_status,
  v2_status,
  CASE
    WHEN v1_amount != v2_amount OR v1_status != v2_status THEN 'CHANGED'
    ELSE 'UNCHANGED'
  END as change_status
FROM (
  SELECT
    order_id,
    MAX(CASE WHEN version = 'v1' THEN v1_amount END) as v1_amount,
    MAX(CASE WHEN version = 'v2' THEN v2_amount END) as v2_amount,
    MAX(CASE WHEN version = 'v1' THEN v1_status END) as v1_status,
    MAX(CASE WHEN version = 'v2' THEN v2_status END) as v2_status
  FROM version_comparison
  GROUP BY order_id
)
WHERE v1_amount IS NOT NULL AND v2_amount IS NOT NULL;
```

---

## Security & Governance

### Q122: How do you implement row-level security in BigQuery?
**Answer:**
**Row-Level Security Implementation:**

```sql
-- Create row access policy
CREATE ROW ACCESS POLICY regional_access_policy
ON `dataset.sales_data`
GRANT TO ('user:analyst@company.com', 'group:regional-analysts@company.com')
FILTER USING (region = SESSION_USER());

-- Dynamic row filtering based on user attributes
CREATE ROW ACCESS POLICY department_filter
ON `dataset.employee_data`
GRANT TO ('group:hr-team@company.com')
FILTER USING (
  department IN (
    SELECT department 
    FROM `dataset.user_permissions` 
    WHERE user_email = SESSION_USER()
  )
);

-- Time-based access control
CREATE ROW ACCESS POLICY time_based_access
ON `dataset.financial_data`
GRANT TO ('group:finance-team@company.com')
FILTER USING (
  report_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
  OR SESSION_USER() IN ('cfo@company.com', 'finance-director@company.com')
);
```

### Q123: How do you implement column-level security?
**Answer:**
**Column-Level Security:**

```sql
-- Create policy taxonomy
CREATE SCHEMA `project.data_governance`;

-- Create policy tags
CREATE TAXONOMY `project.locations.us.taxonomies.data_classification`
DISPLAY_NAME = 'Data Classification';

CREATE POLICY_TAG `project.locations.us.taxonomies.data_classification.policyTags.pii`
DISPLAY_NAME = 'Personally Identifiable Information';

-- Apply policy tags to columns
ALTER TABLE `dataset.customers`
ALTER COLUMN ssn SET OPTIONS (
  policy_tags = ['projects/project/locations/us/taxonomies/data_classification/policyTags/pii']
);

ALTER TABLE `dataset.customers`
ALTER COLUMN email SET OPTIONS (
  policy_tags = ['projects/project/locations/us/taxonomies/data_classification/policyTags/pii']
);

-- Create data policy for PII access
CREATE DATA_POLICY `project.locations.us.dataPolicies.pii_masking_policy`
DATA_POLICY_TYPE = COLUMN_LEVEL_SECURITY_POLICY
POLICY_TAG = 'projects/project/locations/us/taxonomies/data_classification/policyTags/pii'
DATA_MASKING_POLICY = (
  predefined_expression = 'SHA256'
);
```

### Q124: How do you implement data encryption and key management?
**Answer:**
**Encryption Implementation:**

```sql
-- Customer-managed encryption keys (CMEK)
CREATE TABLE `dataset.encrypted_table`
(
  customer_id STRING,
  sensitive_data STRING,
  created_at TIMESTAMP
)
OPTIONS (
  kms_key_name = 'projects/project/locations/us/keyRings/bigquery-ring/cryptoKeys/table-key'
);

-- Application-level encryption
CREATE TEMP FUNCTION encrypt_data(plaintext STRING, key_id STRING)
RETURNS STRING
LANGUAGE SQL AS (
  -- Use AEAD encryption functions
  KEYS.KEYSET_TO_JSON(
    KEYS.KEYSET_FROM_JSON(
      KEYS.NEW_KEYSET('AEAD_AES_GCM_256')
    )
  )
);

-- Decrypt data for authorized users
CREATE OR REPLACE FUNCTION decrypt_for_user(encrypted_data STRING, user_email STRING)
RETURNS STRING
LANGUAGE SQL AS (
  CASE
    WHEN user_email IN (
      SELECT authorized_user 
      FROM `dataset.encryption_permissions`
    ) THEN 
      -- Decrypt logic here
      encrypted_data  -- Simplified
    ELSE 
      '***ENCRYPTED***'
  END
);
```

### Q125: How do you implement audit logging and compliance monitoring?
**Answer:**
**Audit and Compliance:**

```sql
-- Query audit log analysis
SELECT
  timestamp,
  principal_email,
  method_name,
  resource_name,
  JSON_EXTRACT_SCALAR(metadata, '$.jobChange.job.jobConfig.query.query') as query_text,
  JSON_EXTRACT_SCALAR(metadata, '$.jobChange.job.jobStats.totalBilledBytes') as bytes_billed
FROM `project.dataset.cloudaudit_googleapis_com_data_access`
WHERE DATE(timestamp) = CURRENT_DATE()
  AND method_name = 'jobservice.insert'
  AND JSON_EXTRACT_SCALAR(metadata, '$.jobChange.job.jobConfig.type') = 'QUERY'
ORDER BY timestamp DESC;

-- Access pattern monitoring
WITH access_patterns AS (
  SELECT
    principal_email,
    DATE(timestamp) as access_date,
    COUNT(*) as query_count,
    COUNT(DISTINCT JSON_EXTRACT_SCALAR(metadata, '$.jobChange.job.jobConfig.query.destinationTable.tableId')) as tables_accessed,
    SUM(CAST(JSON_EXTRACT_SCALAR(metadata, '$.jobChange.job.jobStats.totalBilledBytes') AS INT64)) as total_bytes_processed
  FROM `project.dataset.cloudaudit_googleapis_com_data_access`
  WHERE DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
    AND method_name = 'jobservice.insert'
  GROUP BY principal_email, DATE(timestamp)
)
SELECT
  principal_email,
  AVG(query_count) as avg_daily_queries,
  AVG(tables_accessed) as avg_tables_per_day,
  SUM(total_bytes_processed) / POW(1024, 4) as total_tb_processed,
  CASE
    WHEN AVG(query_count) > 100 THEN 'High Usage'
    WHEN AVG(tables_accessed) > 20 THEN 'Broad Access'
    ELSE 'Normal'
  END as usage_pattern
FROM access_patterns
GROUP BY principal_email
ORDER BY total_tb_processed DESC;
```

### Q126: How do you implement data lineage and impact analysis?
**Answer:**
**Data Lineage Tracking:**

```sql
-- Create lineage metadata table
CREATE TABLE `dataset.data_lineage_metadata` (
  job_id STRING,
  source_tables ARRAY<STRING>,
  target_tables ARRAY<STRING>,
  transformation_type STRING,
  user_email STRING,
  execution_timestamp TIMESTAMP,
  query_text STRING
);

-- Extract lineage from audit logs
INSERT INTO `dataset.data_lineage_metadata`
SELECT
  JSON_EXTRACT_SCALAR(metadata, '$.jobChange.job.jobName') as job_id,
  ARRAY(
    SELECT table_ref
    FROM UNNEST(JSON_EXTRACT_ARRAY(metadata, '$.jobChange.job.jobStats.referencedTables')) as table_ref
  ) as source_tables,
  ARRAY[
    CONCAT(
      JSON_EXTRACT_SCALAR(metadata, '$.jobChange.job.jobConfig.query.destinationTable.projectId'),
      '.',
      JSON_EXTRACT_SCALAR(metadata, '$.jobChange.job.jobConfig.query.destinationTable.datasetId'),
      '.',
      JSON_EXTRACT_SCALAR(metadata, '$.jobChange.job.jobConfig.query.destinationTable.tableId')
    )
  ] as target_tables,
  'QUERY' as transformation_type,
  principal_email as user_email,
  timestamp as execution_timestamp,
  JSON_EXTRACT_SCALAR(metadata, '$.jobChange.job.jobConfig.query.query') as query_text
FROM `project.dataset.cloudaudit_googleapis_com_data_access`
WHERE DATE(timestamp) = CURRENT_DATE()
  AND method_name = 'jobservice.insert'
  AND JSON_EXTRACT_SCALAR(metadata, '$.jobChange.job.jobConfig.query.destinationTable.tableId') IS NOT NULL;

-- Impact analysis query
WITH RECURSIVE impact_analysis AS (
  SELECT
    target_table,
    source_table,
    transformation_type,
    1 as level
  FROM (
    SELECT
      target_tables[OFFSET(0)] as target_table,
      source_table,
      transformation_type
    FROM `dataset.data_lineage_metadata`,
    UNNEST(source_tables) as source_table
  )
  WHERE source_table = 'project.dataset.source_table'  -- Starting point
  
  UNION ALL
  
  SELECT
    lineage.target_table,
    lineage.source_table,
    lineage.transformation_type,
    impact.level + 1
  FROM (
    SELECT
      target_tables[OFFSET(0)] as target_table,
      source_table,
      transformation_type
    FROM `dataset.data_lineage_metadata`,
    UNNEST(source_tables) as source_table
  ) lineage
  JOIN impact_analysis impact ON lineage.source_table = impact.target_table
  WHERE impact.level < 5  -- Prevent infinite recursion
)
SELECT
  level,
  target_table,
  transformation_type,
  COUNT(*) as dependency_count
FROM impact_analysis
GROUP BY level, target_table, transformation_type
ORDER BY level, target_table;
```

### Q127: How do you implement data classification and tagging?
**Answer:**
**Data Classification System:**

```sql
-- Create classification metadata
CREATE TABLE `dataset.data_classification` (
  table_name STRING,
  column_name STRING,
  classification_level STRING,  -- PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED
  data_category STRING,         -- PII, FINANCIAL, HEALTH, etc.
  retention_period_days INT64,
  classification_date TIMESTAMP,
  classified_by STRING
);

-- Automated PII detection
WITH column_analysis AS (
  SELECT
    table_name,
    column_name,
    data_type,
    -- Pattern-based PII detection
    CASE
      WHEN LOWER(column_name) LIKE '%ssn%' OR LOWER(column_name) LIKE '%social%' THEN 'SSN'
      WHEN LOWER(column_name) LIKE '%email%' THEN 'EMAIL'
      WHEN LOWER(column_name) LIKE '%phone%' OR LOWER(column_name) LIKE '%mobile%' THEN 'PHONE'
      WHEN LOWER(column_name) LIKE '%credit%' OR LOWER(column_name) LIKE '%card%' THEN 'PAYMENT'
      WHEN LOWER(column_name) LIKE '%address%' THEN 'ADDRESS'
      ELSE 'UNKNOWN'
    END as detected_pii_type
  FROM `project.dataset.INFORMATION_SCHEMA.COLUMNS`
  WHERE table_schema = 'dataset'
)
INSERT INTO `dataset.data_classification`
SELECT
  table_name,
  column_name,
  CASE detected_pii_type
    WHEN 'SSN' THEN 'RESTRICTED'
    WHEN 'EMAIL' THEN 'CONFIDENTIAL'
    WHEN 'PHONE' THEN 'CONFIDENTIAL'
    WHEN 'PAYMENT' THEN 'RESTRICTED'
    WHEN 'ADDRESS' THEN 'CONFIDENTIAL'
    ELSE 'INTERNAL'
  END as classification_level,
  detected_pii_type as data_category,
  CASE detected_pii_type
    WHEN 'SSN' THEN 2555  -- 7 years
    WHEN 'PAYMENT' THEN 2555  -- 7 years
    ELSE 1095  -- 3 years
  END as retention_period_days,
  CURRENT_TIMESTAMP() as classification_date,
  'automated_classifier' as classified_by
FROM column_analysis
WHERE detected_pii_type != 'UNKNOWN';
```

### Q128: How do you implement data retention and deletion policies?
**Answer:**
**Data Retention Management:**

```sql
-- Create retention policy table
CREATE TABLE `dataset.retention_policies` (
  table_name STRING,
  retention_period_days INT64,
  deletion_method STRING,  -- DELETE, ARCHIVE, ANONYMIZE
  policy_effective_date DATE,
  created_by STRING
);

-- Automated retention enforcement
CREATE OR REPLACE PROCEDURE `dataset.enforce_retention_policies`()
BEGIN
  DECLARE policy_cursor CURSOR FOR
    SELECT table_name, retention_period_days, deletion_method
    FROM `dataset.retention_policies`
    WHERE policy_effective_date <= CURRENT_DATE();
  
  FOR policy IN policy_cursor DO
    CASE policy.deletion_method
      WHEN 'DELETE' THEN
        EXECUTE IMMEDIATE FORMAT(
          "DELETE FROM `dataset.%s` WHERE DATE(created_at) < DATE_SUB(CURRENT_DATE(), INTERVAL %d DAY)",
          policy.table_name, policy.retention_period_days
        );
      
      WHEN 'ARCHIVE' THEN
        EXECUTE IMMEDIATE FORMAT(
          "EXPORT DATA OPTIONS(uri='gs://archive-bucket/%s/*.parquet', format='PARQUET') AS SELECT * FROM `dataset.%s` WHERE DATE(created_at) < DATE_SUB(CURRENT_DATE(), INTERVAL %d DAY)",
          policy.table_name, policy.table_name, policy.retention_period_days
        );
        
        EXECUTE IMMEDIATE FORMAT(
          "DELETE FROM `dataset.%s` WHERE DATE(created_at) < DATE_SUB(CURRENT_DATE(), INTERVAL %d DAY)",
          policy.table_name, policy.retention_period_days
        );
      
      WHEN 'ANONYMIZE' THEN
        EXECUTE IMMEDIATE FORMAT(
          "UPDATE `dataset.%s` SET email = 'anonymized@example.com', phone = '000-000-0000' WHERE DATE(created_at) < DATE_SUB(CURRENT_DATE(), INTERVAL %d DAY)",
          policy.table_name, policy.retention_period_days
        );
    END CASE;
    
    -- Log retention action
    INSERT INTO `dataset.retention_log`
    VALUES (
      policy.table_name,
      policy.deletion_method,
      CURRENT_TIMESTAMP(),
      @@row_count.last_modified_count
    );
  END FOR;
END;
```

### Q129: How do you implement access control and permission management?
**Answer:**
**Access Control Framework:**

```sql
-- Create role-based access control
CREATE TABLE `dataset.rbac_roles` (
  role_name STRING,
  permissions ARRAY<STRING>,
  description STRING
);

CREATE TABLE `dataset.rbac_user_roles` (
  user_email STRING,
  role_name STRING,
  granted_by STRING,
  granted_at TIMESTAMP,
  expires_at TIMESTAMP
);

-- Define roles and permissions
INSERT INTO `dataset.rbac_roles` VALUES
('data_analyst', ['SELECT'], 'Read-only access to analytical data'),
('data_scientist', ['SELECT', 'CREATE_MODEL'], 'ML model development access'),
('data_engineer', ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE_TABLE'], 'Full data pipeline access'),
('data_admin', ['ALL'], 'Administrative access to all data');

-- Permission checking function
CREATE OR REPLACE FUNCTION `dataset.check_user_permission`(user_email STRING, required_permission STRING)
RETURNS BOOLEAN
LANGUAGE SQL AS (
  EXISTS (
    SELECT 1
    FROM `dataset.rbac_user_roles` ur
    JOIN `dataset.rbac_roles` r ON ur.role_name = r.role_name
    WHERE ur.user_email = user_email
      AND (required_permission IN UNNEST(r.permissions) OR 'ALL' IN UNNEST(r.permissions))
      AND (ur.expires_at IS NULL OR ur.expires_at > CURRENT_TIMESTAMP())
  )
);

-- Dynamic access control view
CREATE OR REPLACE VIEW `dataset.secure_customer_data` AS
SELECT
  customer_id,
  name,
  CASE
    WHEN `dataset.check_user_permission`(SESSION_USER(), 'VIEW_PII') THEN email
    ELSE 'REDACTED'
  END as email,
  CASE
    WHEN `dataset.check_user_permission`(SESSION_USER(), 'VIEW_PII') THEN phone
    ELSE 'REDACTED'
  END as phone,
  created_at
FROM `dataset.customers`;
```

### Q130: How do you implement data masking and anonymization?
**Answer:**
**Data Masking Techniques:**

```sql
-- Static data masking
CREATE OR REPLACE TABLE `dataset.masked_customers` AS
SELECT
  customer_id,
  name,
  -- Email masking
  CONCAT(
    SUBSTR(email, 1, 2),
    REPEAT('*', LENGTH(email) - STRPOS(email, '@') - 2),
    SUBSTR(email, STRPOS(email, '@'))
  ) as masked_email,
  
  -- Phone masking
  CONCAT(
    SUBSTR(phone, 1, 3),
    '-***-',
    SUBSTR(phone, -4)
  ) as masked_phone,
  
  -- SSN masking
  CONCAT('***-**-', SUBSTR(ssn, -4)) as masked_ssn,
  
  -- Date shifting (maintain relative relationships)
  DATE_ADD(birth_date, INTERVAL CAST(RAND() * 365 - 182 AS INT64) DAY) as shifted_birth_date,
  
  created_at
FROM `dataset.customers`;

-- Dynamic data masking based on user role
CREATE OR REPLACE FUNCTION `dataset.mask_sensitive_data`(data STRING, data_type STRING, user_role STRING)
RETURNS STRING
LANGUAGE SQL AS (
  CASE
    WHEN user_role IN ('admin', 'compliance_officer') THEN data  -- Full access
    WHEN data_type = 'EMAIL' THEN
      CONCAT(
        SUBSTR(data, 1, 2),
        REPEAT('*', LENGTH(data) - STRPOS(data, '@') - 2),
        SUBSTR(data, STRPOS(data, '@'))
      )
    WHEN data_type = 'SSN' THEN CONCAT('***-**-', SUBSTR(data, -4))
    WHEN data_type = 'PHONE' THEN CONCAT(SUBSTR(data, 1, 3), '-***-', SUBSTR(data, -4))
    WHEN data_type = 'CREDIT_CARD' THEN CONCAT('****-****-****-', SUBSTR(data, -4))
    ELSE 'REDACTED'
  END
);

-- K-anonymity implementation
WITH anonymized_data AS (
  SELECT
    -- Generalize age to ranges
    CASE
      WHEN age BETWEEN 18 AND 25 THEN '18-25'
      WHEN age BETWEEN 26 AND 35 THEN '26-35'
      WHEN age BETWEEN 36 AND 45 THEN '36-45'
      WHEN age BETWEEN 46 AND 55 THEN '46-55'
      ELSE '55+'
    END as age_range,
    
    -- Generalize location to region
    CASE
      WHEN state IN ('CA', 'OR', 'WA') THEN 'West Coast'
      WHEN state IN ('NY', 'NJ', 'CT') THEN 'Northeast'
      WHEN state IN ('TX', 'OK', 'AR') THEN 'South Central'
      ELSE 'Other'
    END as region,
    
    -- Keep non-identifying attributes
    purchase_amount,
    product_category
  FROM `dataset.customer_purchases`
)
SELECT
  age_range,
  region,
  COUNT(*) as group_size,
  AVG(purchase_amount) as avg_purchase,
  ARRAY_AGG(DISTINCT product_category) as categories
FROM anonymized_data
GROUP BY age_range, region
HAVING COUNT(*) >= 5;  -- Ensure k-anonymity with k=5
```

### Q131: How do you implement compliance monitoring for regulations like GDPR?
**Answer:**
**GDPR Compliance Implementation:**

```sql
-- GDPR data subject registry
CREATE TABLE `dataset.gdpr_data_subjects` (
  subject_id STRING,
  email STRING,
  consent_status STRING,  -- GIVEN, WITHDRAWN, PENDING
  consent_date TIMESTAMP,
  consent_purpose ARRAY<STRING>,
  data_retention_period INT64,
  created_at TIMESTAMP
);

-- Right to be forgotten implementation
CREATE OR REPLACE PROCEDURE `dataset.process_deletion_request`(subject_email STRING)
BEGIN
  DECLARE tables_cursor CURSOR FOR
    SELECT table_name
    FROM `dataset.INFORMATION_SCHEMA.TABLES`
    WHERE table_type = 'BASE TABLE';
  
  -- Log deletion request
  INSERT INTO `dataset.gdpr_deletion_log`
  VALUES (subject_email, CURRENT_TIMESTAMP(), 'INITIATED', SESSION_USER());
  
  -- Delete from all relevant tables
  FOR table_record IN tables_cursor DO
    EXECUTE IMMEDIATE FORMAT(
      "DELETE FROM `dataset.%s` WHERE email = '%s'",
      table_record.table_name, subject_email
    );
  END FOR;
  
  -- Update deletion log
  UPDATE `dataset.gdpr_deletion_log`
  SET status = 'COMPLETED', completed_at = CURRENT_TIMESTAMP()
  WHERE subject_email = subject_email AND status = 'INITIATED';
END;

-- Data portability (Right to data portability)
CREATE OR REPLACE PROCEDURE `dataset.export_subject_data`(subject_email STRING)
BEGIN
  -- Export all data related to the subject
  EXPORT DATA OPTIONS(
    uri = CONCAT('gs://gdpr-exports/', subject_email, '/*.json'),
    format = 'JSON'
  ) AS
  SELECT
    'customers' as table_name,
    TO_JSON_STRING(STRUCT(*)) as data
  FROM `dataset.customers`
  WHERE email = subject_email
  
  UNION ALL
  
  SELECT
    'orders' as table_name,
    TO_JSON_STRING(STRUCT(*)) as data
  FROM `dataset.orders`
  WHERE customer_email = subject_email;
  
  -- Log export request
  INSERT INTO `dataset.gdpr_export_log`
  VALUES (subject_email, CURRENT_TIMESTAMP(), 'COMPLETED', SESSION_USER());
END;

-- Consent management
CREATE OR REPLACE VIEW `dataset.gdpr_compliance_status` AS
WITH consent_analysis AS (
  SELECT
    subject_id,
    email,
    consent_status,
    consent_date,
    DATE_DIFF(CURRENT_DATE(), DATE(consent_date), DAY) as days_since_consent,
    data_retention_period,
    CASE
      WHEN consent_status = 'WITHDRAWN' THEN 'REQUIRES_DELETION'
      WHEN DATE_DIFF(CURRENT_DATE(), DATE(consent_date), DAY) > data_retention_period THEN 'RETENTION_EXPIRED'
      WHEN consent_status = 'PENDING' AND DATE_DIFF(CURRENT_DATE(), DATE(consent_date), DAY) > 30 THEN 'CONSENT_EXPIRED'
      ELSE 'COMPLIANT'
    END as compliance_status
  FROM `dataset.gdpr_data_subjects`
)
SELECT
  compliance_status,
  COUNT(*) as subject_count,
  ARRAY_AGG(email LIMIT 10) as sample_subjects
FROM consent_analysis
GROUP BY compliance_status;
```

### Q132: How do you implement data quality governance?
**Answer:**
**Data Quality Governance Framework:**

```sql
-- Data quality rules registry
CREATE TABLE `dataset.dq_rules` (
  rule_id STRING,
  rule_name STRING,
  table_name STRING,
  column_name STRING,
  rule_type STRING,  -- COMPLETENESS, VALIDITY, CONSISTENCY, ACCURACY
  rule_sql STRING,
  severity STRING,   -- CRITICAL, HIGH, MEDIUM, LOW
  owner_email STRING,
  created_at TIMESTAMP
);

-- Data quality execution engine
CREATE OR REPLACE PROCEDURE `dataset.execute_dq_rules`(target_table STRING)
BEGIN
  DECLARE rule_cursor CURSOR FOR
    SELECT rule_id, rule_name, rule_sql, severity, owner_email
    FROM `dataset.dq_rules`
    WHERE table_name = target_table;
  
  FOR rule IN rule_cursor DO
    BEGIN
      EXECUTE IMMEDIATE FORMAT(
        "INSERT INTO `dataset.dq_results` 
         SELECT '%s' as rule_id, '%s' as rule_name, '%s' as severity, 
                COUNT(*) as violation_count, CURRENT_TIMESTAMP() as check_time
         FROM `dataset.%s` WHERE NOT (%s)",
        rule.rule_id, rule.rule_name, rule.severity, target_table, rule.rule_sql
      );
    EXCEPTION WHEN ERROR THEN
      INSERT INTO `dataset.dq_execution_errors`
      VALUES (rule.rule_id, ERROR_MESSAGE(), CURRENT_TIMESTAMP());
    END;
  END FOR;
END;

-- Data quality dashboard
CREATE OR REPLACE VIEW `dataset.dq_dashboard` AS
WITH quality_metrics AS (
  SELECT
    DATE(check_time) as check_date,
    rule_name,
    severity,
    SUM(violation_count) as total_violations,
    COUNT(*) as rule_executions
  FROM `dataset.dq_results`
  WHERE DATE(check_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
  GROUP BY DATE(check_time), rule_name, severity
),
quality_scores AS (
  SELECT
    check_date,
    SUM(CASE WHEN severity = 'CRITICAL' THEN total_violations * 10 ELSE 0 END) as critical_score,
    SUM(CASE WHEN severity = 'HIGH' THEN total_violations * 5 ELSE 0 END) as high_score,
    SUM(CASE WHEN severity = 'MEDIUM' THEN total_violations * 2 ELSE 0 END) as medium_score,
    SUM(CASE WHEN severity = 'LOW' THEN total_violations * 1 ELSE 0 END) as low_score
  FROM quality_metrics
  GROUP BY check_date
)
SELECT
  check_date,
  critical_score + high_score + medium_score + low_score as total_quality_score,
  CASE
    WHEN critical_score > 0 THEN 'CRITICAL'
    WHEN high_score > 50 THEN 'HIGH_RISK'
    WHEN medium_score > 100 THEN 'MEDIUM_RISK'
    ELSE 'ACCEPTABLE'
  END as quality_status
FROM quality_scores
ORDER BY check_date DESC;
```

### Q133: How do you implement data stewardship and ownership tracking?
**Answer:**
**Data Stewardship Framework:**

```sql
-- Data asset registry
CREATE TABLE `dataset.data_assets` (
  asset_id STRING,
  asset_name STRING,
  asset_type STRING,  -- TABLE, VIEW, DATASET, COLUMN
  business_owner STRING,
  technical_owner STRING,
  data_steward STRING,
  description STRING,
  business_glossary_terms ARRAY<STRING>,
  criticality_level STRING,  -- CRITICAL, HIGH, MEDIUM, LOW
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Stewardship responsibilities
CREATE TABLE `dataset.stewardship_responsibilities` (
  steward_email STRING,
  responsibility_type STRING,  -- QUALITY, SECURITY, COMPLIANCE, LIFECYCLE
  asset_pattern STRING,       -- Pattern to match assets
  assigned_date DATE,
  assigned_by STRING
);

-- Data lineage with ownership
CREATE OR REPLACE VIEW `dataset.data_ownership_lineage` AS
WITH lineage_with_owners AS (
  SELECT
    dl.source_table,
    dl.target_table,
    dl.transformation_type,
    so.business_owner as source_owner,
    so.data_steward as source_steward,
    to.business_owner as target_owner,
    to.data_steward as target_steward
  FROM `dataset.data_lineage_metadata` dl
  LEFT JOIN `dataset.data_assets` so ON dl.source_table = so.asset_name
  LEFT JOIN `dataset.data_assets` to ON dl.target_table = to.asset_name
)
SELECT
  *,
  CASE
    WHEN source_owner != target_owner THEN 'OWNERSHIP_CHANGE'
    WHEN source_steward != target_steward THEN 'STEWARD_CHANGE'
    ELSE 'CONSISTENT_OWNERSHIP'
  END as ownership_status
FROM lineage_with_owners;

-- Stewardship metrics
SELECT
  data_steward,
  COUNT(*) as assets_managed,
  COUNTIF(criticality_level = 'CRITICAL') as critical_assets,
  COUNTIF(DATE_DIFF(CURRENT_DATE(), DATE(updated_at), DAY) > 90) as stale_assets,
  AVG(DATE_DIFF(CURRENT_DATE(), DATE(updated_at), DAY)) as avg_days_since_update
FROM `dataset.data_assets`
WHERE data_steward IS NOT NULL
GROUP BY data_steward
ORDER BY critical_assets DESC, stale_assets DESC;
```

### Q134: How do you implement security incident response?
**Answer:**
**Security Incident Response:**

```sql
-- Security incident detection
CREATE OR REPLACE VIEW `dataset.security_incidents` AS
WITH suspicious_activities AS (
  -- Unusual access patterns
  SELECT
    'UNUSUAL_ACCESS' as incident_type,
    principal_email,
    COUNT(*) as activity_count,
    ARRAY_AGG(DISTINCT resource_name) as accessed_resources,
    MIN(timestamp) as first_activity,
    MAX(timestamp) as last_activity
  FROM `project.dataset.cloudaudit_googleapis_com_data_access`
  WHERE DATE(timestamp) = CURRENT_DATE()
    AND method_name = 'jobservice.insert'
  GROUP BY principal_email
  HAVING COUNT(*) > 100  -- Threshold for unusual activity
  
  UNION ALL
  
  -- After-hours access
  SELECT
    'AFTER_HOURS_ACCESS' as incident_type,
    principal_email,
    COUNT(*) as activity_count,
    ARRAY_AGG(DISTINCT resource_name) as accessed_resources,
    MIN(timestamp) as first_activity,
    MAX(timestamp) as last_activity
  FROM `project.dataset.cloudaudit_googleapis_com_data_access`
  WHERE DATE(timestamp) = CURRENT_DATE()
    AND (EXTRACT(HOUR FROM timestamp) < 6 OR EXTRACT(HOUR FROM timestamp) > 22)
    AND method_name = 'jobservice.insert'
  GROUP BY principal_email
  HAVING COUNT(*) > 5
  
  UNION ALL
  
  -- Large data exports
  SELECT
    'LARGE_DATA_EXPORT' as incident_type,
    principal_email,
    COUNT(*) as activity_count,
    ARRAY_AGG(DISTINCT resource_name) as accessed_resources,
    MIN(timestamp) as first_activity,
    MAX(timestamp) as last_activity
  FROM `project.dataset.cloudaudit_googleapis_com_data_access`
  WHERE DATE(timestamp) = CURRENT_DATE()
    AND method_name = 'jobservice.insert'
    AND CAST(JSON_EXTRACT_SCALAR(metadata, '$.jobChange.job.jobStats.totalBilledBytes') AS INT64) > 1099511627776  -- > 1TB
  GROUP BY principal_email
)
SELECT
  incident_type,
  principal_email,
  activity_count,
  accessed_resources,
  first_activity,
  last_activity,
  CURRENT_TIMESTAMP() as detected_at,
  CASE incident_type
    WHEN 'LARGE_DATA_EXPORT' THEN 'HIGH'
    WHEN 'AFTER_HOURS_ACCESS' THEN 'MEDIUM'
    ELSE 'LOW'
  END as severity
FROM suspicious_activities;

-- Incident response automation
CREATE OR REPLACE PROCEDURE `dataset.respond_to_security_incident`(incident_type STRING, user_email STRING)
BEGIN
  CASE incident_type
    WHEN 'LARGE_DATA_EXPORT' THEN
      -- Temporarily revoke access
      INSERT INTO `dataset.access_revocations`
      VALUES (user_email, 'TEMPORARY_SUSPENSION', CURRENT_TIMESTAMP(), 'SECURITY_INCIDENT');
      
      -- Alert security team
      INSERT INTO `dataset.security_alerts`
      VALUES (
        GENERATE_UUID(),
        'Large data export detected',
        CONCAT('User ', user_email, ' exported large amount of data'),
        'HIGH',
        CURRENT_TIMESTAMP()
      );
    
    WHEN 'AFTER_HOURS_ACCESS' THEN
      -- Log for review
      INSERT INTO `dataset.security_reviews`
      VALUES (user_email, incident_type, CURRENT_TIMESTAMP(), 'PENDING_REVIEW');
  END CASE;
END;
```

### Q135: How do you implement data privacy impact assessments?
**Answer:**
**Privacy Impact Assessment Framework:**

```sql
-- Privacy impact assessment registry
CREATE TABLE `dataset.privacy_impact_assessments` (
  pia_id STRING,
  project_name STRING,
  data_sources ARRAY<STRING>,
  personal_data_types ARRAY<STRING>,
  processing_purposes ARRAY<STRING>,
  risk_level STRING,  -- LOW, MEDIUM, HIGH, VERY_HIGH
  mitigation_measures ARRAY<STRING>,
  assessment_date DATE,
  assessor_email STRING,
  approval_status STRING,
  approved_by STRING,
  approved_date DATE
);

-- Automated privacy risk scoring
CREATE OR REPLACE FUNCTION `dataset.calculate_privacy_risk`(
  data_types ARRAY<STRING>,
  data_volume INT64,
  external_sharing BOOLEAN,
  retention_period INT64
)
RETURNS STRING
LANGUAGE SQL AS (
  CASE
    WHEN 'SSN' IN UNNEST(data_types) OR 'HEALTH_DATA' IN UNNEST(data_types) THEN 'VERY_HIGH'
    WHEN ('EMAIL' IN UNNEST(data_types) OR 'PHONE' IN UNNEST(data_types)) 
         AND (data_volume > 1000000 OR external_sharing) THEN 'HIGH'
    WHEN ARRAY_LENGTH(data_types) > 3 AND retention_period > 2555 THEN 'MEDIUM'
    ELSE 'LOW'
  END
);

-- Privacy compliance monitoring
WITH privacy_metrics AS (
  SELECT
    table_name,
    COUNT(*) as total_records,
    COUNTIF(email IS NOT NULL) as records_with_email,
    COUNTIF(phone IS NOT NULL) as records_with_phone,
    COUNTIF(ssn IS NOT NULL) as records_with_ssn,
    MAX(created_at) as latest_record,
    MIN(created_at) as oldest_record
  FROM `dataset.customer_data`
  GROUP BY table_name
)
SELECT
  table_name,
  total_records,
  records_with_email / total_records * 100 as email_percentage,
  records_with_phone / total_records * 100 as phone_percentage,
  records_with_ssn / total_records * 100 as ssn_percentage,
  DATE_DIFF(CURRENT_DATE(), DATE(oldest_record), DAY) as data_age_days,
  `dataset.calculate_privacy_risk`(
    ARRAY['EMAIL', 'PHONE', 'SSN'],
    total_records,
    false,
    DATE_DIFF(CURRENT_DATE(), DATE(oldest_record), DAY)
  ) as privacy_risk_level
FROM privacy_metrics;
```

### Q136: How do you implement continuous compliance monitoring?
**Answer:**
**Continuous Compliance Monitoring:**

```sql
-- Compliance monitoring dashboard
CREATE OR REPLACE VIEW `dataset.compliance_dashboard` AS
WITH compliance_checks AS (
  -- Data retention compliance
  SELECT
    'DATA_RETENTION' as compliance_area,
    COUNT(*) as total_items,
    COUNTIF(DATE_DIFF(CURRENT_DATE(), DATE(created_at), DAY) > retention_period_days) as non_compliant_items,
    'Records exceeding retention period' as description
  FROM `dataset.customer_data` cd
  JOIN `dataset.retention_policies` rp ON cd.table_name = rp.table_name
  
  UNION ALL
  
  -- Access control compliance
  SELECT
    'ACCESS_CONTROL' as compliance_area,
    COUNT(*) as total_items,
    COUNTIF(expires_at < CURRENT_TIMESTAMP()) as non_compliant_items,
    'Expired user access permissions' as description
  FROM `dataset.rbac_user_roles`
  
  UNION ALL
  
  -- Data classification compliance
  SELECT
    'DATA_CLASSIFICATION' as compliance_area,
    COUNT(*) as total_items,
    COUNTIF(classification_level IS NULL) as non_compliant_items,
    'Unclassified sensitive data' as description
  FROM `dataset.data_classification`
  WHERE data_category IN ('PII', 'FINANCIAL', 'HEALTH')
)
SELECT
  compliance_area,
  total_items,
  non_compliant_items,
  ROUND((total_items - non_compliant_items) / total_items * 100, 2) as compliance_percentage,
  description,
  CASE
    WHEN non_compliant_items = 0 THEN 'COMPLIANT'
    WHEN non_compliant_items / total_items < 0.05 THEN 'MOSTLY_COMPLIANT'
    WHEN non_compliant_items / total_items < 0.20 THEN 'PARTIALLY_COMPLIANT'
    ELSE 'NON_COMPLIANT'
  END as compliance_status
FROM compliance_checks;

-- Automated compliance reporting
CREATE OR REPLACE PROCEDURE `dataset.generate_compliance_report`(report_date DATE)
BEGIN
  -- Generate comprehensive compliance report
  CREATE OR REPLACE TABLE `dataset.compliance_report_` || FORMAT_DATE('%Y%m%d', report_date) AS
  SELECT
    report_date,
    compliance_area,
    compliance_status,
    compliance_percentage,
    non_compliant_items,
    description,
    CURRENT_TIMESTAMP() as report_generated_at
  FROM `dataset.compliance_dashboard`;
  
  -- Send alerts for non-compliance
  INSERT INTO `dataset.compliance_alerts`
  SELECT
    GENERATE_UUID() as alert_id,
    compliance_area,
    CONCAT('Compliance issue: ', description) as alert_message,
    'HIGH' as severity,
    CURRENT_TIMESTAMP() as alert_time
  FROM `dataset.compliance_dashboard`
  WHERE compliance_status IN ('NON_COMPLIANT', 'PARTIALLY_COMPLIANT');
END;
```

### Q137: How do you implement data breach detection and response?
**Answer:**
**Data Breach Detection System:**

```sql
-- Breach detection rules
CREATE TABLE `dataset.breach_detection_rules` (
  rule_id STRING,
  rule_name STRING,
  rule_description STRING,
  detection_query STRING,
  severity STRING,
  notification_emails ARRAY<STRING>
);

-- Real-time breach monitoring
CREATE OR REPLACE VIEW `dataset.potential_breaches` AS
WITH breach_indicators AS (
  -- Unusual data access patterns
  SELECT
    'MASS_DATA_ACCESS' as breach_type,
    principal_email,
    COUNT(*) as access_count,
    ARRAY_AGG(DISTINCT resource_name) as accessed_resources,
    'HIGH' as severity
  FROM `project.dataset.cloudaudit_googleapis_com_data_access`
  WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
    AND method_name = 'jobservice.insert'
  GROUP BY principal_email
  HAVING COUNT(*) > 50
  
  UNION ALL
  
  -- Unauthorized external data sharing
  SELECT
    'EXTERNAL_SHARING' as breach_type,
    principal_email,
    COUNT(*) as access_count,
    ARRAY_AGG(DISTINCT resource_name) as accessed_resources,
    'CRITICAL' as severity
  FROM `project.dataset.cloudaudit_googleapis_com_data_access`
  WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
    AND method_name = 'jobservice.insert'
    AND JSON_EXTRACT_SCALAR(metadata, '$.jobChange.job.jobConfig.extract.destinationUris[0]') LIKE '%external%'
  GROUP BY principal_email
)
SELECT
  breach_type,
  principal_email,
  access_count,
  accessed_resources,
  severity,
  CURRENT_TIMESTAMP() as detected_at
FROM breach_indicators;

-- Breach response automation
CREATE OR REPLACE PROCEDURE `dataset.respond_to_breach`(breach_type STRING, user_email STRING)
BEGIN
  -- Immediate containment
  CASE breach_type
    WHEN 'EXTERNAL_SHARING' THEN
      -- Immediately revoke access
      INSERT INTO `dataset.emergency_access_revocations`
      VALUES (user_email, 'IMMEDIATE_REVOCATION', CURRENT_TIMESTAMP(), 'DATA_BREACH');
      
      -- Alert security team
      INSERT INTO `dataset.security_incidents`
      VALUES (
        GENERATE_UUID(),
        'POTENTIAL_DATA_BREACH',
        CONCAT('External data sharing detected for user: ', user_email),
        'CRITICAL',
        CURRENT_TIMESTAMP(),
        'ACTIVE'
      );
    
    WHEN 'MASS_DATA_ACCESS' THEN
      -- Flag for investigation
      INSERT INTO `dataset.security_investigations`
      VALUES (
        GENERATE_UUID(),
        user_email,
        'Mass data access pattern detected',
        'INVESTIGATING',
        CURRENT_TIMESTAMP()
      );
  END CASE;
  
  -- Log breach response action
  INSERT INTO `dataset.breach_response_log`
  VALUES (
    breach_type,
    user_email,
    'AUTOMATED_RESPONSE',
    CURRENT_TIMESTAMP(),
    'system'
  );
END;
```

### Q138: How do you implement regulatory reporting automation?
**Answer:**
**Regulatory Reporting System:**

```sql
-- Regulatory reporting templates
CREATE TABLE `dataset.regulatory_reports` (
  report_id STRING,
  regulation_name STRING,  -- GDPR, CCPA, SOX, etc.
  report_type STRING,
  report_frequency STRING,  -- MONTHLY, QUARTERLY, ANNUAL
  report_query STRING,
  last_generated TIMESTAMP,
  next_due_date DATE
);

-- GDPR Article 30 - Records of Processing Activities
CREATE OR REPLACE VIEW `dataset.gdpr_article30_report` AS
SELECT
  'Customer Data Processing' as processing_activity,
  'Marketing and Customer Service' as purpose,
  ARRAY['Customers', 'Prospects'] as data_subject_categories,
  ARRAY['Name', 'Email', 'Phone', 'Address'] as personal_data_categories,
  ARRAY['Marketing Partners'] as recipients,
  'No third country transfers' as third_country_transfers,
  '7 years for customers, 3 years for prospects' as retention_periods,
  'Encryption at rest and in transit, access controls, audit logging' as security_measures,
  CURRENT_DATE() as report_date

UNION ALL

SELECT
  'Employee Data Processing' as processing_activity,
  'HR Management and Payroll' as purpose,
  ARRAY['Employees', 'Former Employees'] as data_subject_categories,
  ARRAY['Name', 'SSN', 'Salary', 'Performance Data'] as personal_data_categories,
  ARRAY['Payroll Provider', 'Benefits Administrator'] as recipients,
  'No third country transfers' as third_country_transfers,
  '7 years after employment termination' as retention_periods,
  'Role-based access, encryption, regular audits' as security_measures,
  CURRENT_DATE() as report_date;

-- SOX compliance reporting
CREATE OR REPLACE PROCEDURE `dataset.generate_sox_report`(report_quarter STRING)
BEGIN
  CREATE OR REPLACE TABLE `dataset.sox_compliance_report_` || report_quarter AS
  WITH financial_data_access AS (
    SELECT
      principal_email,
      COUNT(*) as access_count,
      ARRAY_AGG(DISTINCT resource_name) as accessed_tables
    FROM `project.dataset.cloudaudit_googleapis_com_data_access`
    WHERE DATE(timestamp) BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY) AND CURRENT_DATE()
      AND resource_name LIKE '%financial%'
    GROUP BY principal_email
  ),
  control_effectiveness AS (
    SELECT
      'Access Control' as control_name,
      COUNT(*) as total_users,
      COUNTIF(expires_at > CURRENT_TIMESTAMP() OR expires_at IS NULL) as compliant_users,
      'Effective' as control_status
    FROM `dataset.rbac_user_roles`
    WHERE role_name LIKE '%financial%'
  )
  SELECT
    report_quarter,
    'Financial Data Access Summary' as section,
    TO_JSON_STRING(STRUCT(
      (SELECT COUNT(*) FROM financial_data_access) as total_users_with_access,
      (SELECT AVG(access_count) FROM financial_data_access) as avg_access_per_user
    )) as metrics,
    CURRENT_TIMESTAMP() as generated_at
  
  UNION ALL
  
  SELECT
    report_quarter,
    'Control Effectiveness' as section,
    TO_JSON_STRING(control_effectiveness) as metrics,
    CURRENT_TIMESTAMP() as generated_at
  FROM control_effectiveness;
END;

-- Automated report generation
CREATE OR REPLACE PROCEDURE `dataset.generate_scheduled_reports`()
BEGIN
  DECLARE report_cursor CURSOR FOR
    SELECT report_id, regulation_name, report_type, report_query
    FROM `dataset.regulatory_reports`
    WHERE next_due_date <= CURRENT_DATE();
  
  FOR report IN report_cursor DO
    BEGIN
      -- Execute report query
      EXECUTE IMMEDIATE FORMAT(
        "CREATE OR REPLACE TABLE `dataset.%s_%s_%s` AS %s",
        report.regulation_name,
        report.report_type,
        FORMAT_DATE('%Y%m%d', CURRENT_DATE()),
        report.report_query
      );
      
      -- Update last generated timestamp
      UPDATE `dataset.regulatory_reports`
      SET 
        last_generated = CURRENT_TIMESTAMP(),
        next_due_date = CASE report_frequency
          WHEN 'MONTHLY' THEN DATE_ADD(CURRENT_DATE(), INTERVAL 1 MONTH)
          WHEN 'QUARTERLY' THEN DATE_ADD(CURRENT_DATE(), INTERVAL 3 MONTH)
          WHEN 'ANNUAL' THEN DATE_ADD(CURRENT_DATE(), INTERVAL 1 YEAR)
        END
      WHERE report_id = report.report_id;
      
    EXCEPTION WHEN ERROR THEN
      INSERT INTO `dataset.report_generation_errors`
      VALUES (report.report_id, ERROR_MESSAGE(), CURRENT_TIMESTAMP());
    END;
  END FOR;
END;
```

---

## 🎯 Key Takeaways

### **Core Capabilities**
- **Serverless Architecture**: No infrastructure management, automatic scaling
- **Petabyte-Scale Analytics**: Handles massive datasets with columnar storage
- **Standard SQL**: ANSI SQL compliance with powerful extensions
- **Real-time Processing**: Streaming ingestion with sub-second latency
- **Built-in ML**: BigQuery ML for in-database machine learning

### **Performance & Optimization**
- **Partitioning & Clustering**: Essential for query performance and cost control
- **Materialized Views**: Pre-computed results for faster analytics
- **Slot Management**: Understanding compute allocation and optimization
- **Query Optimization**: Partition pruning, column selection, and caching strategies
- **Storage Optimization**: Compression, encoding, and archival strategies

### **Advanced Analytics**
- **Window Functions**: Complex analytical computations
- **Array & Struct Operations**: Handling nested and repeated data
- **Geospatial Analytics**: Location-based analysis and clustering
- **Time Series Analysis**: Trend detection and forecasting
- **Statistical Functions**: Comprehensive statistical analysis capabilities

### **Machine Learning Integration**
- **Model Types**: Classification, regression, clustering, time series, deep learning
- **Feature Engineering**: SQL-based data preparation and transformation
- **Model Evaluation**: Built-in metrics and validation techniques
- **AutoML Integration**: Automated model selection and hyperparameter tuning
- **Model Deployment**: Batch and real-time inference capabilities

### **Cost Management**
- **Pricing Models**: On-demand vs. flat-rate pricing strategies
- **Cost Monitoring**: Query cost analysis and budget controls
- **Storage Optimization**: Lifecycle management and archival policies
- **Slot Optimization**: Efficient resource utilization
- **Cost Allocation**: Department and project-level cost tracking

### **Data Integration**
- **Multi-source Ingestion**: Batch, streaming, and real-time data loading
- **External Data Sources**: Cloud Storage, databases, APIs, and SaaS platforms
- **Schema Evolution**: Handling changing data structures
- **Data Quality**: Validation, monitoring, and error handling
- **CDC Implementation**: Change data capture and synchronization

### **Security & Governance**
- **Access Control**: IAM, row-level, and column-level security
- **Data Encryption**: At-rest and in-transit encryption with CMEK support
- **Audit Logging**: Comprehensive activity monitoring and compliance
- **Data Classification**: Automated PII detection and policy enforcement
- **Compliance**: GDPR, CCPA, SOX, and other regulatory requirements

### **Enterprise Features**
- **Data Lineage**: End-to-end data flow tracking and impact analysis
- **Data Stewardship**: Ownership, responsibility, and governance frameworks
- **Disaster Recovery**: Cross-region replication and backup strategies
- **Monitoring & Alerting**: Proactive issue detection and response
- **Performance Tuning**: Advanced optimization techniques and best practices

### **Best Practices Summary**
1. **Design for Performance**: Use partitioning, clustering, and appropriate data types
2. **Optimize Costs**: Monitor usage, implement controls, and use efficient query patterns
3. **Ensure Security**: Implement least-privilege access and comprehensive audit logging
4. **Plan for Scale**: Design schemas and queries that scale with data growth
5. **Automate Operations**: Use scheduled queries, monitoring, and alerting for operational efficiency
6. **Govern Data**: Implement classification, lineage tracking, and compliance monitoring
7. **Monitor Quality**: Establish data quality rules and continuous validation
8. **Document Everything**: Maintain clear documentation for schemas, processes, and governance

**Remember**: BigQuery's true power lies in its combination of serverless simplicity, massive scalability, and comprehensive analytics capabilities. Success requires understanding not just the technical features, but also the operational, cost, and governance considerations for enterprise-scale deployments.