# AWS Athena Key Concepts

## 1. Serverless Query Engine
**What it is**: Interactive query service that analyzes data in S3 using standard SQL without managing infrastructure.

**Core Features**:
- **No servers to manage**: Fully managed service
- **Pay per query**: Charged only for data scanned
- **Standard SQL**: ANSI SQL compliant with JDBC/ODBC drivers
- **Federated queries**: Query multiple data sources

```sql
-- Basic query structure
SELECT column1, column2, COUNT(*)
FROM "database"."table"
WHERE partition_date = '2024-01-15'
GROUP BY column1, column2
LIMIT 1000;
```

## 2. Data Catalog Integration
**AWS Glue Data Catalog**: Central metadata repository for all your data.

**Key Components**:
```sql
-- Database creation
CREATE DATABASE sales_data
COMMENT 'Sales analytics database'
LOCATION 's3://my-bucket/sales/';

-- Table creation with partitions
CREATE EXTERNAL TABLE sales_transactions (
    transaction_id string,
    customer_id string,
    amount decimal(10,2),
    product_category string
)
PARTITIONED BY (
    year int,
    month int,
    day int
)
STORED AS PARQUET
LOCATION 's3://my-bucket/sales/transactions/';
```

## 3. Data Formats and Storage
**Supported Formats**:
- **Parquet**: Columnar, best performance
- **ORC**: Optimized row columnar
- **JSON**: Semi-structured data
- **CSV**: Simple delimited files
- **Avro**: Schema evolution support

**Optimization Strategies**:
```sql
-- Columnar format for better performance
CREATE TABLE optimized_sales
WITH (
    format = 'PARQUET',
    parquet_compression = 'SNAPPY',
    partitioned_by = ARRAY['year', 'month']
) AS
SELECT * FROM raw_sales;
```

## 4. Partitioning
**What it is**: Dividing tables into smaller, more manageable pieces based on column values.

**Partition Types**:
```sql
-- Date-based partitioning (most common)
PARTITIONED BY (
    year int,
    month int,
    day int
)

-- Category-based partitioning
PARTITIONED BY (
    region string,
    product_type string
)

-- Adding partitions manually
ALTER TABLE sales_data ADD
PARTITION (year=2024, month=1, day=15)
LOCATION 's3://bucket/sales/2024/01/15/';
```

**Partition Projection**: Automatically generate partition metadata.
```sql
CREATE EXTERNAL TABLE projected_logs (
    timestamp string,
    level string,
    message string
)
PARTITIONED BY (
    year int,
    month int,
    day int,
    hour int
)
TBLPROPERTIES (
    'projection.enabled' = 'true',
    'projection.year.type' = 'integer',
    'projection.year.range' = '2020,2030',
    'projection.month.type' = 'integer',
    'projection.month.range' = '1,12',
    'projection.day.type' = 'integer',
    'projection.day.range' = '1,31',
    'projection.hour.type' = 'integer',
    'projection.hour.range' = '0,23',
    'storage.location.template' = 's3://logs/${year}/${month}/${day}/${hour}/'
);
```

## 5. Query Optimization
**Performance Best Practices**:

### Column Selection
```sql
-- Good: Select only needed columns
SELECT customer_id, amount, transaction_date
FROM sales
WHERE transaction_date >= '2024-01-01';

-- Bad: Select all columns
SELECT * FROM sales;
```

### Partition Pruning
```sql
-- Efficient: Uses partition filters
SELECT COUNT(*)
FROM sales
WHERE year = 2024 AND month = 1;

-- Inefficient: Scans all partitions
SELECT COUNT(*)
FROM sales
WHERE transaction_date >= '2024-01-01';
```

### Data Compression
```sql
-- Use compressed formats
CREATE TABLE compressed_data
WITH (
    format = 'PARQUET',
    parquet_compression = 'GZIP'
) AS SELECT * FROM raw_data;
```

## 6. Cost Optimization
**Pricing Model**: $5 per TB of data scanned.

**Cost Reduction Strategies**:
```sql
-- 1. Use columnar formats (90% cost reduction)
-- 2. Compress data (additional 70-90% reduction)
-- 3. Partition data effectively
-- 4. Use LIMIT for testing
SELECT * FROM large_table LIMIT 100;

-- 5. Use approximate functions
SELECT approx_distinct(customer_id) FROM sales;

-- 6. Filter early and often
WITH filtered_data AS (
    SELECT * FROM sales 
    WHERE date_col >= '2024-01-01'
)
SELECT COUNT(*) FROM filtered_data;
```

## 7. Security and Access Control
**IAM Integration**: Control access through AWS IAM policies.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "athena:StartQueryExecution",
                "athena:GetQueryResults",
                "athena:GetQueryExecution"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::my-data-bucket/*",
                "arn:aws:s3:::my-data-bucket"
            ]
        }
    ]
}
```

**Column-Level Security**:
```sql
-- Create view with restricted columns
CREATE VIEW customer_summary AS
SELECT 
    customer_id,
    total_purchases,
    -- Exclude sensitive PII
    'REDACTED' as email
FROM customer_data;
```

## 8. Advanced Features
**Federated Queries**: Query multiple data sources.
```sql
-- Query data from different sources
SELECT 
    a.customer_id,
    a.purchase_amount,
    b.customer_name
FROM "athena_catalog"."sales_db"."transactions" a
JOIN "mysql_connector"."crm_db"."customers" b
ON a.customer_id = b.id;
```

**Machine Learning Functions**:
```sql
-- Anomaly detection
SELECT 
    transaction_id,
    amount,
    ml_predict('anomaly_model', amount, customer_id) as anomaly_score
FROM transactions;
```

**User Defined Functions (UDFs)**:
```sql
-- Register UDF
USING EXTERNAL FUNCTION my_custom_function(x double)
RETURNS double
LANGUAGE JAVA
AS 'com.example.MyFunction';

-- Use UDF
SELECT my_custom_function(amount) FROM sales;
```

## 9. Integration Patterns
**With AWS Services**:
```python
# Python boto3 integration
import boto3

athena = boto3.client('athena')

response = athena.start_query_execution(
    QueryString='SELECT COUNT(*) FROM sales',
    QueryExecutionContext={'Database': 'sales_db'},
    ResultConfiguration={
        'OutputLocation': 's3://query-results-bucket/'
    }
)

query_execution_id = response['QueryExecutionId']
```

**With BI Tools**:
```python
# JDBC connection string
jdbc:awsathena://AwsRegion=us-east-1;
S3OutputLocation=s3://query-results-bucket/;
User=access_key;
Password=secret_key;
```

## 10. Monitoring and Troubleshooting
**CloudWatch Metrics**:
- **DataScannedInBytes**: Amount of data processed
- **QueryExecutionTime**: Query duration
- **ProcessedBytes**: Data processed per query

**Query Performance Insights**:
```sql
-- Check query history
SELECT 
    query_id,
    query,
    state,
    data_scanned_in_bytes,
    execution_time_in_millis
FROM information_schema.query_history
WHERE creation_time >= current_timestamp - interval '1' day;
```

**Common Issues**:
- **HIVE_PARTITION_SCHEMA_MISMATCH**: Partition schema conflicts
- **EXCEEDED_MEMORY_LIMIT**: Query too complex, add LIMIT
- **PERMISSION_DENIED**: Check IAM permissions for S3 access
- **TABLE_NOT_FOUND**: Verify Glue catalog registration