# Google BigQuery Interview Questions

## 📋 Table of Contents
1. [Basic Concepts](#basic-concepts)
2. [Architecture & Storage](#architecture--storage)
3. [SQL & Querying](#sql--querying)
4. [Data Loading & Export](#data-loading--export)
5. [Performance & Optimization](#performance--optimization)
6. [Security & Access Control](#security--access-control)
7. [Machine Learning](#machine-learning)
8. [Streaming & Real-time](#streaming--real-time)
9. [Cost Management](#cost-management)
10. [Integration & APIs](#integration--apis)
11. [Best Practices](#best-practices)
12. [Scenario-Based Questions](#scenario-based-questions)

---

## Basic Concepts

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

## 🎯 Key Takeaways

- **Serverless**: No infrastructure management required
- **Scalable**: Handles petabyte-scale analytics automatically
- **Cost-Effective**: Pay-per-query pricing model
- **ML Integration**: Built-in machine learning capabilities
- **Real-time**: Streaming data support with low latency
- **Standard SQL**: ANSI SQL compliance with extensions
- **Google Ecosystem**: Seamless integration with GCP services

Remember: BigQuery excels at large-scale analytics with its serverless architecture and automatic optimization, making it ideal for organizations needing scalable data warehousing without operational overhead.