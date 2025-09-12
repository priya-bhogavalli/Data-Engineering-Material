# Amazon Athena Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-40)](#basic-level-questions-1-40)
2. [Intermediate Level Questions (41-80)](#intermediate-level-questions-41-80)
3. [Advanced Level Questions (81-120)](#advanced-level-questions-81-120)
4. [Architecture & Performance (121-160)](#architecture--performance-121-160)
5. [Streaming & Real-time Processing (161-180)](#streaming--real-time-processing-161-180)
6. [Production & Operations (181-220)](#production--operations-181-220)
7. [Scenario-Based Questions (221-250)](#scenario-based-questions-221-250)

---

## Basic Level Questions (1-40)

### 1. What is Amazon Athena and how does it differ from traditional databases?

**Answer:** Amazon Athena is a serverless, interactive query service that makes it easy to analyze data in S3 using standard SQL.

#### **Key Differences:**

| Aspect | Amazon Athena | Traditional Databases |
|--------|---------------|----------------------|
| **Infrastructure** | Serverless, no management | Requires server setup/maintenance |
| **Data Storage** | Data stays in S3 | Data stored in database files |
| **Pricing Model** | Pay per query (data scanned) | Pay for compute/storage resources |
| **Schema** | Schema-on-read | Schema-on-write |
| **Scalability** | Automatic scaling | Manual scaling required |
| **Use Case** | Analytics on data lake | OLTP and OLAP workloads |

### 2. What is the underlying engine that powers Athena?

**Answer:** Athena is built on **Presto**, a distributed SQL query engine originally developed by Facebook.

#### **Presto Features:**
- **Distributed Architecture**: Coordinator and worker nodes
- **In-Memory Processing**: Fast query execution
- **ANSI SQL Support**: Standard SQL with extensions
- **Connector Architecture**: Pluggable data source connectors

### 3. How does Athena pricing work?

**Answer:** Athena uses a pay-per-query pricing model based on data scanned.

#### **Pricing Details:**
- **Cost**: $5.00 per TB of data scanned
- **Minimum Charge**: 10MB per query
- **No Charge For**: DDL statements, failed queries, cancelled queries
- **Data Transfer**: No additional charges for data transfer from S3

```sql
-- Example: Query scanning 100GB of data
-- Cost = 0.1 TB × $5.00 = $0.50

SELECT customer_id, SUM(amount) as total
FROM sales_data
WHERE order_date >= '2023-01-01'
GROUP BY customer_id;
```

### 4. What data formats does Athena support?

**Answer:** Athena supports multiple structured and semi-structured data formats.

#### **Supported Formats:**
```sql
-- Parquet (recommended for performance)
CREATE EXTERNAL TABLE sales_parquet (
    order_id bigint,
    amount decimal(10,2)
)
STORED AS PARQUET
LOCATION 's3://bucket/parquet-data/';

-- JSON
CREATE EXTERNAL TABLE events_json (
    event_id string,
    user_id string,
    properties map<string,string>
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://bucket/json-data/';

-- CSV
CREATE EXTERNAL TABLE customers_csv (
    customer_id string,
    name string,
    email string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES ('field.delim' = ',')
LOCATION 's3://bucket/csv-data/';

-- ORC
CREATE EXTERNAL TABLE transactions_orc (
    transaction_id string,
    amount decimal(15,2)
)
STORED AS ORC
LOCATION 's3://bucket/orc-data/';
```

### 5. Explain the relationship between Athena and AWS Glue Data Catalog.

**Answer:** AWS Glue Data Catalog serves as Athena's metadata repository.

#### **Integration Benefits:**
- **Centralized Metadata**: Single source of truth for table schemas
- **Automatic Discovery**: Glue crawlers discover and catalog data
- **Cross-Service Sharing**: Multiple AWS services use same catalog
- **Schema Evolution**: Handles schema changes over time

```python
# Glue Crawler example
import boto3

glue = boto3.client('glue')

crawler_config = {
    'Name': 'sales-data-crawler',
    'Role': 'arn:aws:iam::account:role/GlueServiceRole',
    'DatabaseName': 'sales_db',
    'Targets': {
        'S3Targets': [{'Path': 's3://sales-bucket/data/'}]
    }
}

glue.create_crawler(**crawler_config)
```

### 6. How do you create a table in Athena?

**Answer:** Tables in Athena are created using CREATE EXTERNAL TABLE statements.

```sql
-- Basic table creation
CREATE EXTERNAL TABLE customer_orders (
    order_id bigint,
    customer_id string,
    order_date date,
    amount decimal(10,2),
    status string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES ('field.delim' = ',')
STORED AS TEXTFILE
LOCATION 's3://my-bucket/orders/'
TBLPROPERTIES ('has_encrypted_data'='false');

-- Partitioned table
CREATE EXTERNAL TABLE orders_partitioned (
    order_id bigint,
    customer_id string,
    amount decimal(10,2)
)
PARTITIONED BY (
    year int,
    month int
)
STORED AS PARQUET
LOCATION 's3://my-bucket/partitioned-orders/';
```

### 7. What is partitioning in Athena and why is it important?

**Answer:** Partitioning divides data into smaller, manageable chunks based on column values.

#### **Benefits:**
- **Performance**: Reduces data scanned by queries
- **Cost**: Lower costs due to less data processed
- **Query Speed**: Faster execution through partition pruning

```sql
-- Create partitioned table
CREATE EXTERNAL TABLE sales_by_date (
    order_id string,
    customer_id string,
    amount decimal(10,2)
)
PARTITIONED BY (
    year string,
    month string,
    day string
)
STORED AS PARQUET
LOCATION 's3://sales-bucket/partitioned/';

-- Add partition
ALTER TABLE sales_by_date ADD PARTITION (year='2023', month='01', day='15')
LOCATION 's3://sales-bucket/partitioned/year=2023/month=01/day=15/';

-- Query with partition pruning
SELECT customer_id, SUM(amount) as total
FROM sales_by_date
WHERE year = '2023' AND month = '01'  -- Only scans January 2023 data
GROUP BY customer_id;
```

### 8. How do you optimize Athena query performance?

**Answer:** Multiple strategies can improve Athena query performance.

#### **Optimization Techniques:**
```sql
-- 1. Use columnar formats
CREATE TABLE optimized_sales
WITH (
    format = 'PARQUET',
    parquet_compression = 'SNAPPY'
) AS
SELECT * FROM raw_sales;

-- 2. Partition data appropriately
CREATE EXTERNAL TABLE partitioned_logs (
    timestamp string,
    level string,
    message string
)
PARTITIONED BY (date_partition string)
STORED AS PARQUET
LOCATION 's3://logs-bucket/partitioned/';

-- 3. Use specific column selection
SELECT customer_id, amount  -- Instead of SELECT *
FROM orders
WHERE order_date >= '2023-01-01';

-- 4. Use LIMIT for exploratory queries
SELECT *
FROM large_table
LIMIT 100;

-- 5. Use approximate functions for large datasets
SELECT 
    region,
    APPROX_COUNT_DISTINCT(customer_id) as unique_customers
FROM sales
GROUP BY region;
```

### 9. What are Athena workgroups and their benefits?

**Answer:** Workgroups provide a way to separate users, teams, applications, or workloads.

#### **Workgroup Benefits:**
- **Resource Management**: Control query concurrency and data usage
- **Cost Control**: Set per-query and per-workgroup data usage limits
- **Security**: Isolate queries and results
- **Configuration**: Different settings per workgroup

```sql
-- Create workgroup
CREATE WORKGROUP analytics_team
WITH (
    result_configuration = (
        output_location = 's3://athena-results/analytics/',
        encryption_configuration = (
            encryption_option = 'SSE_S3'
        )
    ),
    enforce_workgroup_configuration = true,
    bytes_scanned_cutoff_per_query = 1073741824  -- 1GB limit
);
```

### 16. What are the limitations of Athena?

**Answer:** Athena has several limitations to consider when designing solutions.

#### **Query Limitations:**
- **Maximum query execution time**: 30 minutes
- **Maximum query string length**: 262,144 bytes
- **Maximum number of partitions per table**: 20,000
- **Maximum databases per account**: 10,000
- **Maximum tables per database**: 100,000

#### **Performance Limitations:**
```sql
-- Small files impact performance
-- Avoid: Many small files (< 128MB)
-- Prefer: Fewer large files (128MB - 1GB)

-- No indexing support
-- Relies on partitioning for performance
SELECT *
FROM large_table
WHERE partition_column = 'value'  -- Fast
AND non_partition_column = 'value';  -- Slow (full scan)
```

#### **Data Type Limitations:**
```sql
-- Supported data types
CREATE TABLE data_types_demo (
    string_col string,
    int_col int,
    bigint_col bigint,
    double_col double,
    decimal_col decimal(10,2),
    date_col date,
    timestamp_col timestamp,
    boolean_col boolean,
    array_col array<string>,
    map_col map<string,string>,
    struct_col struct<field1:string,field2:int>
);
```

### 17. How do you monitor Athena query performance?

**Answer:** Use CloudWatch metrics, query history, and EXPLAIN statements.

```sql
-- Use EXPLAIN to understand query execution
EXPLAIN (TYPE DISTRIBUTED)
SELECT customer_id, SUM(amount)
FROM orders
WHERE order_date >= '2023-01-01'
GROUP BY customer_id;

-- Query execution details
EXPLAIN (TYPE IO)
SELECT *
FROM partitioned_table
WHERE year = '2023' AND month = '01';
```

#### **CloudWatch Metrics:**
- **DataScannedInBytes**: Amount of data scanned
- **QueryExecutionTime**: Query execution duration
- **ProcessedBytes**: Data processed by engine
- **EngineExecutionTime**: Time spent in query engine

### 18. How do you implement security in Athena?

**Answer:** Implement multiple layers of security including IAM, encryption, and access controls.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "athena:StartQueryExecution",
                "athena:GetQueryExecution",
                "athena:GetQueryResults",
                "athena:StopQueryExecution"
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
        },
        {
            "Effect": "Allow",
            "Action": [
                "glue:GetTable",
                "glue:GetPartitions",
                "glue:GetDatabase"
            ],
            "Resource": "*"
        }
    ]
}
```

```sql
-- Encryption configuration
CREATE EXTERNAL TABLE encrypted_data (
    sensitive_id string,
    encrypted_field string
)
STORED AS PARQUET
LOCATION 's3://encrypted-bucket/data/'
TBLPROPERTIES (
    'has_encrypted_data'='true',
    'encryption_option'='SSE_S3'
);
```

### 19. How do you handle large result sets in Athena?

**Answer:** Use pagination, LIMIT clauses, and result caching strategies.

```sql
-- Use LIMIT for large result sets
SELECT customer_id, order_count
FROM (
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) as rn
    FROM orders
    GROUP BY customer_id
)
WHERE rn <= 1000;  -- Top 1000 customers

-- Pagination pattern
SELECT *
FROM (
    SELECT 
        *,
        ROW_NUMBER() OVER (ORDER BY order_date) as row_num
    FROM orders
)
WHERE row_num BETWEEN 1001 AND 2000;  -- Page 2 (1000 records per page)

-- Use CTAS for large transformations
CREATE TABLE customer_summary
WITH (
    format = 'PARQUET',
    external_location = 's3://results-bucket/summaries/'
) AS
SELECT 
    customer_id,
    COUNT(*) as total_orders,
    SUM(amount) as total_spent,
    AVG(amount) as avg_order_value
FROM orders
GROUP BY customer_id;
```

### 20. How do you integrate Athena with other AWS services?

**Answer:** Athena integrates with multiple AWS services for comprehensive analytics solutions.

#### **QuickSight Integration:**
```sql
-- Create view for QuickSight
CREATE VIEW sales_dashboard AS
SELECT 
    DATE_TRUNC('month', order_date) as month,
    region,
    product_category,
    SUM(amount) as total_sales,
    COUNT(*) as order_count
FROM sales_data
WHERE order_date >= DATE('2023-01-01')
GROUP BY 
    DATE_TRUNC('month', order_date),
    region,
    product_category;
```

#### **Lambda Integration:**
```python
import boto3
import json

def lambda_handler(event, context):
    athena = boto3.client('athena')
    
    query = """
    SELECT customer_id, COUNT(*) as recent_orders
    FROM orders
    WHERE order_date >= current_date - interval '7' day
    GROUP BY customer_id
    HAVING COUNT(*) > 5
    """
    
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': 'ecommerce'},
        ResultConfiguration={
            'OutputLocation': 's3://athena-results/lambda-queries/'
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'queryExecutionId': response['QueryExecutionId']
        })
    }

### 21. What are the different join types supported in Athena?

**Answer:** Athena supports all standard SQL join types with optimization strategies.

```sql
-- Sample tables
CREATE EXTERNAL TABLE customers (
    customer_id string,
    name string,
    region string
) STORED AS PARQUET
LOCATION 's3://data-bucket/customers/';

CREATE EXTERNAL TABLE orders (
    order_id string,
    customer_id string,
    amount decimal(10,2),
    order_date date
) STORED AS PARQUET
LOCATION 's3://data-bucket/orders/';

-- Inner Join
SELECT 
    c.name,
    c.region,
    o.amount,
    o.order_date
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2023-01-01';

-- Left Outer Join
SELECT 
    c.customer_id,
    c.name,
    COALESCE(o.total_orders, 0) as total_orders
FROM customers c
LEFT JOIN (
    SELECT 
        customer_id,
        COUNT(*) as total_orders
    FROM orders
    GROUP BY customer_id
) o ON c.customer_id = o.customer_id;

-- Cross Join (Cartesian Product)
SELECT 
    p.product_name,
    r.region_name
FROM products p
CROSS JOIN regions r;
```

### 22. How do you handle duplicate data in Athena?

**Answer:** Use DISTINCT, window functions, and deduplication strategies.

```sql
-- Remove duplicates with DISTINCT
SELECT DISTINCT 
    customer_id,
    email,
    registration_date
FROM customer_registrations;

-- Deduplication using window functions
SELECT 
    customer_id,
    email,
    registration_date
FROM (
    SELECT 
        customer_id,
        email,
        registration_date,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id 
            ORDER BY registration_date DESC
        ) as rn
    FROM customer_registrations
)
WHERE rn = 1;  -- Keep latest registration per customer

-- Create deduplicated table
CREATE TABLE clean_customers
WITH (
    format = 'PARQUET',
    external_location = 's3://clean-data/customers/'
) AS
SELECT DISTINCT *
FROM raw_customers;
```

### 23. How do you perform window functions in Athena?

**Answer:** Athena supports comprehensive window function capabilities.

```sql
-- Ranking functions
SELECT 
    customer_id,
    order_date,
    amount,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as order_sequence,
    RANK() OVER (ORDER BY amount DESC) as amount_rank,
    DENSE_RANK() OVER (ORDER BY amount DESC) as dense_amount_rank
FROM orders;

-- Aggregate window functions
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
    ) as moving_avg_3_orders
FROM orders;

-- Lead and Lag functions
SELECT 
    customer_id,
    order_date,
    amount,
    LAG(amount, 1) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as previous_order_amount,
    LEAD(order_date, 1) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as next_order_date
FROM orders;
```

### 24. How do you handle array and map data types in Athena?

**Answer:** Athena provides functions to work with complex data types.

```sql
-- Working with arrays
CREATE EXTERNAL TABLE user_preferences (
    user_id string,
    preferences array<string>,
    scores array<double>
) STORED AS PARQUET
LOCATION 's3://data-bucket/preferences/';

-- Array operations
SELECT 
    user_id,
    preferences,
    CARDINALITY(preferences) as num_preferences,
    preferences[1] as first_preference,
    ARRAY_JOIN(preferences, ', ') as preferences_string
FROM user_preferences;

-- Unnest arrays
SELECT 
    user_id,
    preference
FROM user_preferences
CROSS JOIN UNNEST(preferences) AS t(preference);

-- Working with maps
CREATE EXTERNAL TABLE event_metadata (
    event_id string,
    properties map<string,string>
) STORED AS PARQUET
LOCATION 's3://data-bucket/events/';

-- Map operations
SELECT 
    event_id,
    properties,
    properties['source'] as event_source,
    properties['campaign_id'] as campaign_id,
    CARDINALITY(properties) as num_properties
FROM event_metadata;
```

### 25. How do you implement data aggregation patterns in Athena?

**Answer:** Use various aggregation functions and grouping strategies.

```sql
-- Basic aggregations
SELECT 
    region,
    COUNT(*) as total_customers,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(total_spent) as total_revenue,
    AVG(total_spent) as avg_customer_value,
    MIN(registration_date) as first_registration,
    MAX(registration_date) as latest_registration
FROM customers
GROUP BY region;

-- Conditional aggregations
SELECT 
    product_category,
    COUNT(*) as total_orders,
    COUNT(*) FILTER (WHERE amount > 100) as high_value_orders,
    SUM(amount) as total_sales,
    SUM(amount) FILTER (WHERE order_date >= '2023-01-01') as ytd_sales
FROM orders
GROUP BY product_category;

-- Multiple grouping sets
SELECT 
    region,
    product_category,
    SUM(amount) as total_sales
FROM sales
GROUP BY GROUPING SETS (
    (region),
    (product_category),
    (region, product_category),
    ()
);

-- Percentile calculations
SELECT 
    region,
    APPROX_PERCENTILE(amount, 0.5) as median_amount,
    APPROX_PERCENTILE(amount, 0.95) as p95_amount,
    APPROX_PERCENTILE(amount, 0.99) as p99_amount
FROM orders
GROUP BY region;
```

### 26. How do you handle date and time operations in Athena?

**Answer:** Athena provides comprehensive date/time functions.

```sql
-- Date extraction and formatting
SELECT 
    order_id,
    order_timestamp,
    DATE(order_timestamp) as order_date,
    EXTRACT(YEAR FROM order_timestamp) as order_year,
    EXTRACT(MONTH FROM order_timestamp) as order_month,
    EXTRACT(DAY FROM order_timestamp) as order_day,
    EXTRACT(HOUR FROM order_timestamp) as order_hour,
    DATE_FORMAT(order_timestamp, '%Y-%m-%d %H:%i:%s') as formatted_timestamp
FROM orders;

-- Date arithmetic
SELECT 
    customer_id,
    registration_date,
    current_date as today,
    DATE_DIFF('day', registration_date, current_date) as days_since_registration,
    DATE_ADD('month', 1, registration_date) as one_month_later,
    DATE_SUB('week', 2, current_date) as two_weeks_ago
FROM customers;

-- Date truncation for grouping
SELECT 
    DATE_TRUNC('month', order_date) as month,
    COUNT(*) as orders_count,
    SUM(amount) as monthly_revenue
FROM orders
WHERE order_date >= DATE('2023-01-01')
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;

-- Working with time intervals
SELECT 
    customer_id,
    COUNT(*) as order_count
FROM orders
WHERE order_date >= current_date - INTERVAL '30' DAY
GROUP BY customer_id
HAVING COUNT(*) > 5;
```

### 27. How do you implement conditional logic in Athena?

**Answer:** Use CASE statements, COALESCE, and conditional functions.

```sql
-- CASE statements
SELECT 
    customer_id,
    total_spent,
    CASE 
        WHEN total_spent >= 10000 THEN 'VIP'
        WHEN total_spent >= 5000 THEN 'Premium'
        WHEN total_spent >= 1000 THEN 'Standard'
        ELSE 'Basic'
    END as customer_tier,
    CASE 
        WHEN registration_date >= DATE('2023-01-01') THEN 'New'
        ELSE 'Existing'
    END as customer_type
FROM customers;

-- Conditional aggregations
SELECT 
    region,
    SUM(CASE WHEN order_date >= '2023-01-01' THEN amount ELSE 0 END) as ytd_sales,
    SUM(CASE WHEN order_date >= '2022-01-01' AND order_date < '2023-01-01' THEN amount ELSE 0 END) as last_year_sales,
    COUNT(CASE WHEN amount > 1000 THEN 1 END) as high_value_orders
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY region;

-- COALESCE for null handling
SELECT 
    customer_id,
    COALESCE(email, 'no-email@company.com') as email,
    COALESCE(phone, 'Not Provided') as phone,
    COALESCE(last_login_date, registration_date) as last_activity_date
FROM customers;

-- IF function
SELECT 
    order_id,
    amount,
    IF(amount > 100, 'High Value', 'Standard') as order_category,
    IF(discount_percent > 0, amount * (1 - discount_percent/100), amount) as final_amount
FROM orders;
```

### 28. How do you handle string operations in Athena?

**Answer:** Athena provides extensive string manipulation functions.

```sql
-- String functions
SELECT 
    customer_id,
    name,
    UPPER(name) as name_upper,
    LOWER(name) as name_lower,
    LENGTH(name) as name_length,
    SUBSTR(name, 1, 3) as name_prefix,
    TRIM(name) as name_trimmed,
    REPLACE(email, '@gmail.com', '@company.com') as corporate_email
FROM customers;

-- String splitting and concatenation
SELECT 
    customer_id,
    full_name,
    SPLIT(full_name, ' ')[1] as first_name,
    SPLIT(full_name, ' ')[2] as last_name,
    CONCAT(first_name, ' ', last_name) as reconstructed_name,
    CONCAT_WS(' | ', customer_id, email, phone) as customer_info
FROM customers;

-- Pattern matching
SELECT 
    customer_id,
    email,
    REGEXP_LIKE(email, '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$') as is_valid_email,
    REGEXP_EXTRACT(email, '([^@]+)@(.+)', 1) as username,
    REGEXP_EXTRACT(email, '([^@]+)@(.+)', 2) as domain
FROM customers;

-- String position and search
SELECT 
    product_name,
    POSITION('Pro' IN product_name) as pro_position,
    STRPOS(product_name, 'Premium') as premium_position,
    STARTS_WITH(product_name, 'iPhone') as is_iphone,
    ENDS_WITH(product_name, 'Plus') as is_plus_model
FROM products;
```

### 29. How do you implement data type conversions in Athena?

**Answer:** Use CAST and TRY_CAST functions for safe type conversions.

```sql
-- Basic type casting
SELECT 
    order_id,
    CAST(order_id AS bigint) as order_id_int,
    CAST(amount_string AS decimal(10,2)) as amount_decimal,
    CAST(order_date_string AS date) as order_date,
    CAST(created_timestamp AS timestamp) as created_ts
FROM raw_orders;

-- Safe casting with TRY_CAST
SELECT 
    customer_id,
    age_string,
    TRY_CAST(age_string AS integer) as age_int,
    CASE 
        WHEN TRY_CAST(age_string AS integer) IS NULL 
        THEN 'Invalid Age' 
        ELSE 'Valid Age' 
    END as age_validation
FROM customer_data;

-- Date parsing
SELECT 
    event_id,
    date_string,
    DATE_PARSE(date_string, '%Y-%m-%d %H:%i:%s') as parsed_timestamp,
    DATE_PARSE(date_string, '%m/%d/%Y') as parsed_date
FROM events;

-- JSON parsing
SELECT 
    event_id,
    json_data,
    JSON_EXTRACT_SCALAR(json_data, '$.user_id') as user_id,
    CAST(JSON_EXTRACT_SCALAR(json_data, '$.amount') AS decimal(10,2)) as amount
FROM event_logs;
```

### 30. How do you create and use views in Athena?

**Answer:** Views provide reusable query abstractions and security layers.

```sql
-- Create a simple view
CREATE VIEW customer_summary AS
SELECT 
    c.customer_id,
    c.name,
    c.region,
    COUNT(o.order_id) as total_orders,
    SUM(o.amount) as total_spent,
    AVG(o.amount) as avg_order_value,
    MAX(o.order_date) as last_order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.region;

-- Create a parameterized view (using WITH clause)
CREATE VIEW monthly_sales AS
WITH monthly_data AS (
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        region,
        product_category,
        SUM(amount) as total_sales,
        COUNT(*) as order_count
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE order_date >= DATE('2023-01-01')
    GROUP BY 
        DATE_TRUNC('month', order_date),
        region,
        product_category
)
SELECT 
    month,
    region,
    product_category,
    total_sales,
    order_count,
    total_sales / order_count as avg_order_value
FROM monthly_data;

-- Security view (column masking)
CREATE VIEW customer_public AS
SELECT 
    customer_id,
    name,
    region,
    SUBSTR(email, 1, 3) || '***@' || SPLIT(email, '@')[2] as masked_email,
    registration_date
FROM customers;

-- Use views in queries
SELECT 
    region,
    COUNT(*) as customer_count,
    AVG(total_spent) as avg_customer_value
FROM customer_summary
WHERE total_orders > 5
GROUP BY region
ORDER BY avg_customer_value DESC;
```
```

### 31. How do you implement data sampling in Athena?

**Answer:** Use TABLESAMPLE and random sampling techniques for large datasets.

```sql
-- System sampling (percentage of data blocks)
SELECT *
FROM large_table TABLESAMPLE SYSTEM (10);  -- ~10% of data blocks

-- Bernoulli sampling (row-level sampling)
SELECT *
FROM large_table TABLESAMPLE BERNOULLI (5);  -- ~5% of rows

-- Random sampling with RANDOM()
SELECT *
FROM large_table
WHERE RANDOM() < 0.01  -- 1% sample
LIMIT 10000;

-- Stratified sampling
SELECT *
FROM (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY region 
            ORDER BY RANDOM()
        ) as rn
    FROM customers
)
WHERE rn <= 100;  -- 100 samples per region

-- Systematic sampling
SELECT *
FROM (
    SELECT 
        *,
        ROW_NUMBER() OVER (ORDER BY customer_id) as row_num
    FROM customers
)
WHERE row_num % 100 = 1;  -- Every 100th record
```

### 32. How do you handle NULL values in Athena?

**Answer:** Use various NULL handling functions and strategies.

```sql
-- NULL checking functions
SELECT 
    customer_id,
    email,
    phone,
    email IS NULL as email_is_null,
    email IS NOT NULL as email_is_not_null,
    COALESCE(email, phone, 'No Contact') as primary_contact
FROM customers;

-- NULL replacement
SELECT 
    customer_id,
    COALESCE(middle_name, '') as middle_name,
    NULLIF(phone, '') as phone_cleaned,  -- Convert empty string to NULL
    NVL(last_login, registration_date) as last_activity
FROM customers;

-- Conditional NULL handling
SELECT 
    order_id,
    amount,
    discount_amount,
    CASE 
        WHEN discount_amount IS NULL THEN amount
        ELSE amount - discount_amount
    END as final_amount
FROM orders;

-- Aggregations with NULL handling
SELECT 
    region,
    COUNT(*) as total_customers,
    COUNT(email) as customers_with_email,
    COUNT(phone) as customers_with_phone,
    AVG(age) as avg_age,  -- Ignores NULLs
    SUM(COALESCE(lifetime_value, 0)) as total_ltv
FROM customers
GROUP BY region;
```

### 33. How do you perform data validation in Athena?

**Answer:** Implement comprehensive validation checks using SQL.

```sql
-- Data validation query
WITH validation_results AS (
    SELECT 
        'row_count' as check_name,
        COUNT(*) as result_value,
        CASE WHEN COUNT(*) > 0 THEN 'PASS' ELSE 'FAIL' END as status
    FROM orders
    
    UNION ALL
    
    SELECT 
        'null_customer_id' as check_name,
        COUNT(*) as result_value,
        CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as status
    FROM orders
    WHERE customer_id IS NULL
    
    UNION ALL
    
    SELECT 
        'negative_amounts' as check_name,
        COUNT(*) as result_value,
        CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as status
    FROM orders
    WHERE amount < 0
    
    UNION ALL
    
    SELECT 
        'future_dates' as check_name,
        COUNT(*) as result_value,
        CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as status
    FROM orders
    WHERE order_date > current_date
    
    UNION ALL
    
    SELECT 
        'duplicate_order_ids' as check_name,
        COUNT(*) - COUNT(DISTINCT order_id) as result_value,
        CASE WHEN COUNT(*) = COUNT(DISTINCT order_id) THEN 'PASS' ELSE 'FAIL' END as status
    FROM orders
)
SELECT 
    check_name,
    result_value,
    status,
    current_timestamp as check_timestamp
FROM validation_results;

-- Email validation
SELECT 
    customer_id,
    email,
    CASE 
        WHEN email IS NULL THEN 'Missing'
        WHEN NOT REGEXP_LIKE(email, '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$') THEN 'Invalid Format'
        ELSE 'Valid'
    END as email_status
FROM customers;
```

### 34. How do you implement data profiling in Athena?

**Answer:** Generate comprehensive data statistics and profiles.

```sql
-- Column profiling
SELECT 
    'customer_id' as column_name,
    COUNT(*) as total_count,
    COUNT(customer_id) as non_null_count,
    COUNT(DISTINCT customer_id) as distinct_count,
    COUNT(*) - COUNT(customer_id) as null_count,
    (COUNT(customer_id) * 100.0 / COUNT(*)) as completeness_pct,
    (COUNT(DISTINCT customer_id) * 100.0 / COUNT(customer_id)) as uniqueness_pct
FROM customers

UNION ALL

SELECT 
    'email' as column_name,
    COUNT(*) as total_count,
    COUNT(email) as non_null_count,
    COUNT(DISTINCT email) as distinct_count,
    COUNT(*) - COUNT(email) as null_count,
    (COUNT(email) * 100.0 / COUNT(*)) as completeness_pct,
    (COUNT(DISTINCT email) * 100.0 / COUNT(email)) as uniqueness_pct
FROM customers;

-- Numeric column profiling
SELECT 
    'amount' as column_name,
    COUNT(*) as total_count,
    COUNT(amount) as non_null_count,
    MIN(amount) as min_value,
    MAX(amount) as max_value,
    AVG(amount) as mean_value,
    APPROX_PERCENTILE(amount, 0.5) as median_value,
    STDDEV(amount) as std_deviation
FROM orders;

-- Data distribution analysis
SELECT 
    region,
    COUNT(*) as customer_count,
    (COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()) as percentage
FROM customers
GROUP BY region
ORDER BY customer_count DESC;
```

### 35. How do you handle large file processing in Athena?

**Answer:** Optimize file sizes and use appropriate strategies for large datasets.

```sql
-- Check file sizes and counts
SELECT 
    '$path' as file_path,
    COUNT(*) as record_count
FROM large_table
GROUP BY '$path'
ORDER BY record_count;

-- Optimize file sizes using CTAS
CREATE TABLE optimized_large_table
WITH (
    format = 'PARQUET',
    parquet_compression = 'SNAPPY',
    external_location = 's3://optimized-bucket/large-table/',
    partitioned_by = ARRAY['year', 'month']
) AS
SELECT 
    *,
    EXTRACT(YEAR FROM order_date) as year,
    EXTRACT(MONTH FROM order_date) as month
FROM large_table
WHERE order_date >= DATE('2023-01-01');

-- Process large tables in chunks
WITH chunked_processing AS (
    SELECT 
        *,
        NTILE(10) OVER (ORDER BY order_id) as chunk_number
    FROM large_table
)
SELECT 
    chunk_number,
    COUNT(*) as records_in_chunk,
    SUM(amount) as chunk_total
FROM chunked_processing
WHERE chunk_number = 1  -- Process one chunk at a time
GROUP BY chunk_number;
```

### 36. How do you implement incremental data processing in Athena?

**Answer:** Use partition-based and timestamp-based incremental strategies.

```sql
-- Partition-based incremental processing
CREATE EXTERNAL TABLE incremental_orders (
    order_id string,
    customer_id string,
    amount decimal(10,2),
    order_timestamp timestamp
)
PARTITIONED BY (
    process_date string
)
STORED AS PARQUET
LOCATION 's3://data-bucket/incremental-orders/';

-- Process only new partitions
SELECT 
    customer_id,
    COUNT(*) as new_orders,
    SUM(amount) as new_revenue
FROM incremental_orders
WHERE process_date = '2023-12-01'  -- Only today's data
GROUP BY customer_id;

-- Timestamp-based incremental processing
CREATE TABLE daily_customer_summary
WITH (
    format = 'PARQUET',
    external_location = 's3://summaries/daily-customer/'
) AS
SELECT 
    DATE(order_timestamp) as summary_date,
    customer_id,
    COUNT(*) as daily_orders,
    SUM(amount) as daily_revenue
FROM orders
WHERE DATE(order_timestamp) = current_date - INTERVAL '1' DAY
GROUP BY DATE(order_timestamp), customer_id;

-- Merge incremental updates
WITH existing_summary AS (
    SELECT customer_id, total_orders, total_revenue
    FROM customer_lifetime_summary
),
new_orders AS (
    SELECT 
        customer_id,
        COUNT(*) as new_order_count,
        SUM(amount) as new_revenue
    FROM orders
    WHERE order_date = current_date
    GROUP BY customer_id
)
SELECT 
    COALESCE(e.customer_id, n.customer_id) as customer_id,
    COALESCE(e.total_orders, 0) + COALESCE(n.new_order_count, 0) as updated_total_orders,
    COALESCE(e.total_revenue, 0) + COALESCE(n.new_revenue, 0) as updated_total_revenue
FROM existing_summary e
FULL OUTER JOIN new_orders n ON e.customer_id = n.customer_id;
```

### 37. How do you handle cross-region data access in Athena?

**Answer:** Configure cross-region access with appropriate permissions and considerations.

```sql
-- Cross-region table definition
CREATE EXTERNAL TABLE cross_region_data (
    event_id string,
    user_id string,
    event_timestamp timestamp,
    region string
)
STORED AS PARQUET
LOCATION 's3://eu-west-1-bucket/events/'  -- Different region
TBLPROPERTIES (
    'projection.enabled' = 'true',
    'projection.region.type' = 'enum',
    'projection.region.values' = 'us-east-1,eu-west-1,ap-southeast-1'
);

-- Query with region awareness
SELECT 
    region,
    DATE(event_timestamp) as event_date,
    COUNT(*) as event_count
FROM cross_region_data
WHERE DATE(event_timestamp) >= current_date - INTERVAL '7' DAY
GROUP BY region, DATE(event_timestamp)
ORDER BY region, event_date;
```

### 38. How do you implement data masking in Athena?

**Answer:** Use SQL functions to mask sensitive data for privacy protection.

```sql
-- Create masked view for sensitive data
CREATE VIEW customers_masked AS
SELECT 
    customer_id,
    -- Mask name (show first letter + asterisks)
    CONCAT(SUBSTR(name, 1, 1), REPEAT('*', LENGTH(name) - 1)) as masked_name,
    
    -- Mask email (show first 3 chars + domain)
    CONCAT(
        SUBSTR(email, 1, 3), 
        '***@', 
        SPLIT(email, '@')[2]
    ) as masked_email,
    
    -- Mask phone (show last 4 digits)
    CONCAT('***-***-', SUBSTR(phone, -4)) as masked_phone,
    
    -- Hash SSN
    TO_HEX(SHA256(TO_UTF8(ssn))) as hashed_ssn,
    
    -- Keep non-sensitive fields
    registration_date,
    region,
    customer_tier
FROM customers;

-- Dynamic masking based on user role
SELECT 
    customer_id,
    CASE 
        WHEN '${aws:userid}' LIKE '%admin%' THEN name
        ELSE CONCAT(SUBSTR(name, 1, 1), REPEAT('*', LENGTH(name) - 1))
    END as name,
    CASE 
        WHEN '${aws:userid}' LIKE '%admin%' THEN email
        ELSE CONCAT(SUBSTR(email, 1, 3), '***@', SPLIT(email, '@')[2])
    END as email
FROM customers;
```

### 39. How do you handle data lineage tracking in Athena?

**Answer:** Implement metadata tracking and documentation strategies.

```sql
-- Create lineage tracking table
CREATE EXTERNAL TABLE data_lineage (
    table_name string,
    source_tables array<string>,
    transformation_type string,
    created_by string,
    created_timestamp timestamp,
    query_text string
)
STORED AS PARQUET
LOCATION 's3://metadata-bucket/lineage/';

-- Track table creation lineage
INSERT INTO data_lineage VALUES (
    'customer_summary',
    ARRAY['customers', 'orders'],
    'aggregation',
    'data_engineer',
    current_timestamp,
    'CREATE TABLE customer_summary AS SELECT c.customer_id, COUNT(o.order_id) FROM customers c LEFT JOIN orders o...'
);

-- Query lineage information
SELECT 
    table_name,
    ARRAY_JOIN(source_tables, ', ') as source_tables,
    transformation_type,
    created_by,
    created_timestamp
FROM data_lineage
WHERE table_name = 'customer_summary';

-- Add comments to tables for documentation
COMMENT ON TABLE customer_summary IS 'Aggregated customer metrics including order count and total spend. Updated daily from customers and orders tables.';
```

### 40. How do you implement cost optimization strategies in Athena?

**Answer:** Use multiple techniques to minimize query costs and data scanned.

```sql
-- 1. Use columnar formats and compression
CREATE TABLE cost_optimized_sales
WITH (
    format = 'PARQUET',
    parquet_compression = 'SNAPPY',
    external_location = 's3://optimized-bucket/sales/'
) AS
SELECT *
FROM raw_sales;

-- 2. Implement proper partitioning
CREATE EXTERNAL TABLE partitioned_events (
    event_id string,
    user_id string,
    event_data string
)
PARTITIONED BY (
    year string,
    month string,
    day string
)
STORED AS PARQUET
LOCATION 's3://events-bucket/partitioned/';

-- 3. Use projection to avoid partition scanning
CREATE EXTERNAL TABLE projected_logs (
    timestamp string,
    level string,
    message string
)
PARTITIONED BY (
    year string,
    month string,
    day string
)
STORED AS PARQUET
LOCATION 's3://logs-bucket/projected/'
TBLPROPERTIES (
    'projection.enabled' = 'true',
    'projection.year.type' = 'integer',
    'projection.year.range' = '2020,2030',
    'projection.month.type' = 'integer',
    'projection.month.range' = '1,12',
    'projection.day.type' = 'integer',
    'projection.day.range' = '1,31',
    'storage.location.template' = 's3://logs-bucket/projected/year=${year}/month=${month}/day=${day}/'
);

-- 4. Use LIMIT for exploratory queries
SELECT *
FROM large_table
WHERE complex_condition = 'value'
LIMIT 1000;  -- Limit data scanned for exploration

-- 5. Use approximate functions for large aggregations
SELECT 
    region,
    APPROX_COUNT_DISTINCT(customer_id) as approx_unique_customers,
    APPROX_PERCENTILE(amount, 0.5) as approx_median_amount
FROM large_sales_table
GROUP BY region;

-- 6. Set workgroup query limits
-- This is done via AWS Console or CLI, not SQL
-- aws athena create-work-group --name cost-controlled \
--   --configuration 'BytesScannedCutoffPerQuery=1073741824'  -- 1GB limit
```

### 10. How do you handle schema evolution in Athena?

**Answer:** Athena supports schema evolution through various mechanisms.

```sql
-- Enable schema merging for Parquet
CREATE EXTERNAL TABLE evolving_data (
    id bigint,
    name string,
    -- New columns will be automatically detected
    email string,
    created_date date
)
STORED AS PARQUET
LOCATION 's3://data-bucket/evolving/'
TBLPROPERTIES (
    'projection.enabled' = 'true',
    'storage.location.template' = 's3://data-bucket/evolving/${year}/${month}/'
);

-- Add new column to existing table
ALTER TABLE customer_data ADD COLUMNS (
    phone_number string,
    last_login timestamp
);

-- Handle missing columns with COALESCE
SELECT 
    customer_id,
    name,
    COALESCE(email, 'unknown') as email,
    COALESCE(phone_number, 'not_provided') as phone
FROM customer_data;

### 11. What compression formats does Athena support?

**Answer:** Athena supports multiple compression formats to reduce storage costs and improve performance.

#### **Supported Compression:**
```sql
-- Gzip compression
CREATE EXTERNAL TABLE logs_gzip (
    timestamp string,
    level string,
    message string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
LOCATION 's3://logs-bucket/gzip/'
TBLPROPERTIES ('compression_type'='gzip');

-- Snappy compression (Parquet)
CREATE EXTERNAL TABLE events_snappy (
    event_id string,
    user_id string,
    event_data string
)
STORED AS PARQUET
LOCATION 's3://events-bucket/snappy/'
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- LZO compression
CREATE EXTERNAL TABLE access_logs (
    ip_address string,
    timestamp string,
    request string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
LOCATION 's3://logs-bucket/lzo/'
TBLPROPERTIES ('compression_type'='lzo');
```

### 12. How do you handle nested JSON data in Athena?

**Answer:** Athena provides functions to extract and query nested JSON structures.

```sql
-- Create table for nested JSON
CREATE EXTERNAL TABLE user_events (
    event_id string,
    user_profile struct<
        name: string,
        age: int,
        preferences: array<string>
    >,
    metadata map<string,string>,
    raw_json string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://events-bucket/nested-json/';

-- Query nested data
SELECT 
    event_id,
    user_profile.name as user_name,
    user_profile.age as user_age,
    user_profile.preferences[1] as first_preference,
    metadata['source'] as event_source
FROM user_events
WHERE user_profile.age > 25;

-- Extract from raw JSON string
SELECT 
    event_id,
    JSON_EXTRACT_SCALAR(raw_json, '$.user.name') as user_name,
    JSON_EXTRACT_SCALAR(raw_json, '$.user.age') as user_age
FROM user_events;
```

### 13. What are the different ways to load data into Athena?

**Answer:** Athena doesn't store data itself but queries data directly from S3.

#### **Data Loading Methods:**
```sql
-- 1. Direct S3 upload and table creation
CREATE EXTERNAL TABLE uploaded_data (
    id bigint,
    name string,
    value decimal(10,2)
)
STORED AS PARQUET
LOCATION 's3://my-bucket/uploaded-data/';

-- 2. CTAS (Create Table As Select)
CREATE TABLE processed_data
WITH (
    format = 'PARQUET',
    external_location = 's3://my-bucket/processed/'
) AS
SELECT 
    customer_id,
    SUM(amount) as total_amount,
    COUNT(*) as order_count
FROM raw_orders
GROUP BY customer_id;

-- 3. INSERT INTO (for existing tables)
INSERT INTO target_table
SELECT *
FROM source_table
WHERE created_date = current_date;
```

### 14. How do you implement data quality checks in Athena?

**Answer:** Use SQL queries to validate data quality and identify issues.

```sql
-- Completeness check
SELECT 
    'completeness_check' as check_type,
    COUNT(*) as total_records,
    COUNT(customer_id) as non_null_customer_id,
    COUNT(email) as non_null_email,
    (COUNT(customer_id) * 100.0 / COUNT(*)) as customer_id_completeness,
    (COUNT(email) * 100.0 / COUNT(*)) as email_completeness
FROM customers;

-- Uniqueness check
SELECT 
    'uniqueness_check' as check_type,
    COUNT(*) as total_records,
    COUNT(DISTINCT customer_id) as unique_customer_ids,
    CASE 
        WHEN COUNT(*) = COUNT(DISTINCT customer_id) 
        THEN 'PASS' 
        ELSE 'FAIL' 
    END as uniqueness_status
FROM customers;

-- Data range validation
SELECT 
    'range_validation' as check_type,
    MIN(order_date) as min_date,
    MAX(order_date) as max_date,
    COUNT(*) FILTER (WHERE amount < 0) as negative_amounts,
    COUNT(*) FILTER (WHERE amount > 10000) as high_amounts
FROM orders;

-- Pattern validation
SELECT 
    'pattern_validation' as check_type,
    COUNT(*) as total_emails,
    COUNT(*) FILTER (
        WHERE regexp_like(email, '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    ) as valid_emails
FROM customers;
```

### 15. How do you handle time zones in Athena?

**Answer:** Athena provides functions for time zone conversion and handling.

```sql
-- Convert timestamps between time zones
SELECT 
    event_id,
    event_timestamp,
    -- Convert UTC to specific timezone
    AT_TIMEZONE(event_timestamp, 'America/New_York') as ny_time,
    AT_TIMEZONE(event_timestamp, 'Europe/London') as london_time,
    AT_TIMEZONE(event_timestamp, 'Asia/Tokyo') as tokyo_time
FROM events
WHERE event_timestamp >= TIMESTAMP '2023-01-01 00:00:00';

-- Extract timezone information
SELECT 
    event_id,
    event_timestamp,
    EXTRACT(TIMEZONE_HOUR FROM event_timestamp) as tz_hour,
    EXTRACT(TIMEZONE_MINUTE FROM event_timestamp) as tz_minute
FROM events;

-- Current time in different zones
SELECT 
    current_timestamp as utc_time,
    AT_TIMEZONE(current_timestamp, 'America/Los_Angeles') as pst_time,
    AT_TIMEZONE(current_timestamp, 'Europe/Paris') as cet_time;
```
```