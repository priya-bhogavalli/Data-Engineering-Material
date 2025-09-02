# AWS Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-30)](#basic-level-questions-1-30)
2. [Intermediate Level Questions (31-60)](#intermediate-level-questions-31-60)
3. [Advanced Level Questions (61-90)](#advanced-level-questions-61-90)
4. [Conceptual Questions (91-120)](#conceptual-questions-91-120)
5. [Architecture & Design Questions (121-150)](#architecture--design-questions-121-150)
6. [Security & Compliance Questions (151-180)](#security--compliance-questions-151-180)
7. [Performance & Optimization Questions (181-210)](#performance--optimization-questions-181-210)
8. [Scenario-Based Questions (211-240)](#scenario-based-questions-211-240)

---

## Basic Level Questions (1-30)

### 1. What are the core AWS services for data engineering and how do you choose between them?
**Answer**: 
AWS provides a comprehensive suite of services for data engineering. The key is understanding when to use each service based on your specific requirements.

**Storage Services Decision Matrix**:
- **S3**: Choose for scalable object storage, data lakes, and archival. Best for unstructured data and when you need virtually unlimited storage.
- **EBS**: Choose for high-performance block storage attached to EC2. Best for databases requiring consistent IOPS.
- **EFS**: Choose when multiple EC2 instances need shared file access. Best for distributed applications.
- **Redshift**: Choose for structured data warehousing with complex analytical queries.

**Compute Services Decision Factors**:
- **Lambda**: Choose for event-driven, short-duration tasks (< 15 minutes). Best for serverless ETL and real-time processing.
- **EC2**: Choose when you need full control over the computing environment. Best for custom applications and long-running processes.
- **EMR**: Choose for big data processing with Hadoop/Spark. Best for large-scale data transformations.
- **Glue**: Choose for managed ETL with minimal infrastructure management. Best for standard data transformations.

### 2. How do you design a data lake architecture on AWS?
**Answer**: Data lake architecture components:

**Storage Layer (S3)**:
```
s3://data-lake-bucket/
├── raw/                    # Raw ingested data
│   ├── year=2024/
│   ├── month=01/
│   └── day=15/
├── processed/              # Cleaned and transformed data
│   ├── bronze/            # Basic cleaning
│   ├── silver/            # Business logic applied
│   └── gold/              # Analytics-ready
├── curated/               # Final datasets
└── archive/               # Historical data
```

**Data Ingestion**:
```python
# Kinesis Data Firehose for streaming data
import boto3

firehose = boto3.client('firehose')

# Configure delivery stream
delivery_stream_config = {
    'DeliveryStreamName': 'data-lake-stream',
    'DeliveryStreamType': 'DirectPut',
    'S3DestinationConfiguration': {
        'RoleARN': 'arn:aws:iam::account:role/firehose-role',
        'BucketARN': 'arn:aws:s3:::data-lake-bucket',
        'Prefix': 'raw/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/',
        'BufferingHints': {
            'SizeInMBs': 5,
            'IntervalInSeconds': 300
        },
        'CompressionFormat': 'GZIP'
    }
}
```

### 3. What is the fundamental difference between S3 storage classes and when would you use each?
**Answer**: 
S3 offers multiple storage classes optimized for different access patterns and cost requirements:

- **Standard**: Frequently accessed data, millisecond access, 99.999999999% durability
- **Standard-IA**: Infrequently accessed but requires rapid access when needed, lower storage cost but retrieval fees
- **One Zone-IA**: Lower cost than Standard-IA, stored in single AZ, good for reproducible data
- **Glacier Instant Retrieval**: Archive data with millisecond retrieval, 68% cost savings vs Standard
- **Glacier Flexible Retrieval**: Archive data with retrieval in minutes to hours, 10% cost of Standard
- **Glacier Deep Archive**: Lowest cost, retrieval in 12+ hours, for long-term retention

**Use Cases**: Standard for active data lakes, IA for backup data, Glacier for compliance archives.

### 4. Explain the concept of eventual consistency in AWS services and its implications for data engineering
**Answer**:
Eventual consistency means that after a write operation, reads will eventually return the updated value, but not necessarily immediately.

**AWS Services with Eventual Consistency**:
- **S3**: Eventually consistent for overwrite PUTs and DELETEs (though now strong consistency for new objects)
- **DynamoDB**: Eventually consistent reads by default, strongly consistent reads available
- **Route 53**: DNS propagation is eventually consistent

**Data Engineering Implications**:
- **Pipeline Design**: Must handle scenarios where recently written data might not be immediately available
- **Retry Logic**: Implement exponential backoff for read operations after writes
- **Data Validation**: Include checks to ensure data completeness before processing
- **Idempotency**: Design operations to be safely retryable

### 5. What are the key differences between Amazon RDS and Amazon Redshift, and how do you choose between them?
**Answer**:

**Amazon RDS**:
- **Purpose**: Transactional workloads (OLTP)
- **Query Pattern**: High-frequency, low-latency queries
- **Scaling**: Vertical scaling, read replicas
- **Data Size**: Typically smaller datasets (TBs)
- **Use Case**: Application databases, operational reporting

**Amazon Redshift**:
- **Purpose**: Analytical workloads (OLAP)
- **Query Pattern**: Complex analytical queries, aggregations
- **Scaling**: Horizontal scaling with clusters
- **Data Size**: Large datasets (PBs)
- **Use Case**: Data warehousing, business intelligence

**Decision Factors**:
- **Query Complexity**: Simple CRUD → RDS, Complex analytics → Redshift
- **Data Volume**: < 1TB → RDS, > 1TB → Redshift
- **Concurrency**: High concurrent users → RDS, Analytical users → Redshift
- **Performance**: Sub-second response → RDS, Minutes acceptable → Redshift

### 6. How does AWS Lambda's execution model impact data processing pipeline design?
**Answer**:

**Lambda Execution Model**:
- **Stateless**: No persistent storage between invocations
- **Event-driven**: Triggered by events from other AWS services
- **Time-limited**: Maximum 15-minute execution time
- **Concurrent**: Automatic scaling up to account limits
- **Cold starts**: Initial latency for new container initialization

**Pipeline Design Implications**:
- **Micro-batch Processing**: Break large jobs into smaller, Lambda-sized chunks
- **State Management**: Use external storage (S3, DynamoDB) for state persistence
- **Error Handling**: Implement retry logic and dead letter queues
- **Cost Optimization**: Pay-per-use model favors sporadic workloads
- **Orchestration**: Use Step Functions for complex workflows

### 7. What is the difference between Amazon Kinesis Data Streams and Kinesis Data Firehose?
**Answer**:

**Kinesis Data Streams**:
- **Purpose**: Real-time data streaming with custom processing
- **Retention**: 1-365 days configurable
- **Processing**: Requires custom consumers (applications, Lambda)
- **Scaling**: Manual shard management
- **Use Case**: Real-time analytics, complex event processing

**Kinesis Data Firehose**:
- **Purpose**: Data delivery to destinations with minimal setup
- **Retention**: No long-term storage, immediate delivery
- **Processing**: Built-in transformations, no custom consumers needed
- **Scaling**: Automatic scaling
- **Use Case**: ETL to data lakes, simple data ingestion

**When to Choose**:
- **Data Streams**: Need real-time processing, multiple consumers, custom logic
- **Firehose**: Simple data delivery, batch loading to S3/Redshift, minimal management

### 8. Explain the concept of data partitioning in AWS and its benefits
**Answer**:

**Partitioning Concept**:
Data partitioning divides large datasets into smaller, manageable segments based on specific criteria (date, region, category).

**AWS Services Supporting Partitioning**:
- **S3**: Prefix-based partitioning (year/month/day structure)
- **Athena**: Partition projection for query optimization
- **Glue**: Partition discovery and management
- **Redshift**: Distribution and sort keys

**Benefits**:
- **Query Performance**: Partition pruning reduces data scanned
- **Cost Optimization**: Pay only for data processed
- **Parallel Processing**: Multiple partitions processed simultaneously
- **Data Management**: Easier to manage lifecycle policies

### 9. What are the key considerations when designing a data lake architecture on AWS?
**Answer**:

**Core Components**:
- **Storage Layer**: S3 with appropriate storage classes
- **Catalog Layer**: AWS Glue Data Catalog for metadata
- **Processing Layer**: EMR, Glue ETL, Lambda for transformations
- **Analytics Layer**: Athena, Redshift, QuickSight for insights

**Design Considerations**:

**Data Organization**:
- Implement medallion architecture (Bronze/Silver/Gold)
- Use consistent naming conventions
- Plan partition strategy upfront

**Security & Governance**:
- Implement least privilege access
- Use Lake Formation for fine-grained permissions
- Enable CloudTrail for audit logging
- Encrypt data at rest and in transit

### 10. How does AWS Glue's serverless nature affect ETL job design and execution?
**Answer**:

**Serverless Characteristics**:
- **No Infrastructure Management**: AWS handles provisioning and scaling
- **Pay-per-use**: Charged only for DPU-hours consumed
- **Automatic Scaling**: Resources scale based on job requirements
- **Managed Environment**: Pre-configured Spark environment

**ETL Design Implications**:

**Job Structure**:
- Design jobs to be modular and reusable
- Implement proper error handling and retry logic
- Use job bookmarks for incremental processing
- Optimize for parallel execution

**Resource Management**:
- Choose appropriate worker types (G.1X, G.2X, G.025X)
- Set maximum capacity to control costs
- Use timeout settings to prevent runaway jobs

---

## Intermediate Level Questions (31-60)

### 31. How do you implement real-time data processing with AWS Kinesis?
**Answer**: Kinesis streaming architecture:

**Kinesis Data Streams**:
```python
# Create Kinesis stream
kinesis = boto3.client('kinesis')

kinesis.create_stream(
    StreamName='real-time-events',
    ShardCount=5
)

# Producer - sending data
import json
import uuid

def send_event(event_data):
    response = kinesis.put_record(
        StreamName='real-time-events',
        Data=json.dumps(event_data),
        PartitionKey=str(uuid.uuid4())
    )
    return response

# Consumer - processing data
def process_kinesis_records():
    response = kinesis.describe_stream(StreamName='real-time-events')
    shard_id = response['StreamDescription']['Shards'][0]['ShardId']
    
    # Get shard iterator
    shard_iterator_response = kinesis.get_shard_iterator(
        StreamName='real-time-events',
        ShardId=shard_id,
        ShardIteratorType='LATEST'
    )
    
    shard_iterator = shard_iterator_response['ShardIterator']
    
    while True:
        records_response = kinesis.get_records(ShardIterator=shard_iterator)
        
        for record in records_response['Records']:
            data = json.loads(record['Data'])
            process_event(data)
        
        shard_iterator = records_response['NextShardIterator']
        time.sleep(1)
```

### 32. How do you optimize AWS Glue ETL jobs for performance?
**Answer**: Glue optimization techniques:

**Job Configuration**:
```python
# Optimized Glue job script
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read from catalog with partitioning
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="data_catalog",
    table_name="sales_data",
    push_down_predicate="year >= '2024'"  # Partition pruning
)

# Optimize transformations
# Use repartition for better parallelism
datasource = datasource.repartition(10)

# Apply transformations
mapped_data = ApplyMapping.apply(
    frame=datasource,
    mappings=[
        ("customer_id", "string", "customer_id", "string"),
        ("order_date", "string", "order_date", "timestamp"),
        ("amount", "double", "amount", "decimal(10,2)")
    ]
)

# Write with partitioning
glueContext.write_dynamic_frame.from_options(
    frame=mapped_data,
    connection_type="s3",
    connection_options={
        "path": "s3://processed-data/sales/",
        "partitionKeys": ["year", "month"]
    },
    format="parquet",
    format_options={
        "compression": "snappy"
    }
)

job.commit()
```

### 33. How do you implement data quality checks in AWS?
**Answer**: Data quality framework using AWS services:

**Glue Data Quality**:
```python
# Glue Data Quality rules
import boto3

glue = boto3.client('glue')

# Create data quality ruleset
ruleset = {
    'Name': 'sales-data-quality',
    'Description': 'Data quality rules for sales data',
    'Ruleset': '''
        Rules = [
            ColumnCount = 10,
            IsComplete "customer_id",
            IsUnique "order_id",
            ColumnValues "amount" > 0,
            ColumnDataType "order_date" = "timestamp",
            ColumnValues "status" in ["pending", "completed", "cancelled"]
        ]
    ''',
    'TargetTable': {
        'TableName': 'sales_data',
        'DatabaseName': 'data_catalog'
    }
}

response = glue.create_data_quality_ruleset(**ruleset)
```

### 34. How do you implement data lineage and governance in AWS?
**Answer**: Data governance framework:

**AWS Glue Data Catalog**:
```python
# Create comprehensive data catalog
glue = boto3.client('glue')

# Create database
glue.create_database(
    DatabaseInput={
        'Name': 'enterprise_data_catalog',
        'Description': 'Central data catalog for enterprise data',
        'Parameters': {
            'owner': 'data-engineering-team',
            'environment': 'production'
        }
    }
)

# Create table with detailed metadata
table_input = {
    'Name': 'customer_transactions',
    'Description': 'Customer transaction data from payment system',
    'Owner': 'data-engineering-team',
    'Parameters': {
        'classification': 'csv',
        'delimiter': ',',
        'skip.header.line.count': '1',
        'data_source': 'payment_system',
        'update_frequency': 'daily',
        'data_classification': 'confidential'
    },
    'StorageDescriptor': {
        'Columns': [
            {
                'Name': 'transaction_id',
                'Type': 'string',
                'Comment': 'Unique transaction identifier'
            },
            {
                'Name': 'customer_id',
                'Type': 'string',
                'Comment': 'Customer identifier (PII)'
            },
            {
                'Name': 'amount',
                'Type': 'decimal(10,2)',
                'Comment': 'Transaction amount in USD'
            }
        ],
        'Location': 's3://data-lake/transactions/',
        'InputFormat': 'org.apache.hadoop.mapred.TextInputFormat',
        'OutputFormat': 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
    },
    'PartitionKeys': [
        {'Name': 'year', 'Type': 'string'},
        {'Name': 'month', 'Type': 'string'}
    ]
}

glue.create_table(
    DatabaseName='enterprise_data_catalog',
    TableInput=table_input
)
```

### 35. How do you implement automated data pipeline orchestration?
**Answer**: Pipeline orchestration using AWS services:

**Step Functions for Workflow**:
```json
{
  "Comment": "Data processing pipeline",
  "StartAt": "DataValidation",
  "States": {
    "DataValidation": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Parameters": {
        "FunctionName": "data-validation-function",
        "Payload.$": "$"
      },
      "Next": "CheckValidationResult"
    },
    "CheckValidationResult": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.validation_passed",
          "BooleanEquals": true,
          "Next": "StartGlueJob"
        }
      ],
      "Default": "ValidationFailed"
    },
    "StartGlueJob": {
      "Type": "Task",
      "Resource": "arn:aws:states:::glue:startJobRun.sync",
      "Parameters": {
        "JobName": "data-processing-job"
      },
      "Next": "SendNotification"
    },
    "SendNotification": {
      "Type": "Task",
      "Resource": "arn:aws:states:::sns:publish",
      "Parameters": {
        "TopicArn": "arn:aws:sns:region:account:pipeline-notifications",
        "Message": "Data pipeline completed successfully"
      },
      "End": true
    }
  }
}
```

---

## Advanced Level Questions (61-90)

### 61. How do you implement multi-region data replication and disaster recovery?
**Answer**: Enterprise-grade DR architecture:

**Cross-Region Infrastructure**:
```python
# CloudFormation template for multi-region setup
import boto3
import json

def deploy_multi_region_infrastructure():
    cloudformation = boto3.client('cloudformation')
    
    template = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Parameters": {
            "PrimaryRegion": {"Type": "String", "Default": "us-east-1"},
            "SecondaryRegion": {"Type": "String", "Default": "us-west-2"}
        },
        "Resources": {
            "PrimaryDataBucket": {
                "Type": "AWS::S3::Bucket",
                "Properties": {
                    "BucketName": {"Fn::Sub": "primary-data-${AWS::AccountId}-${PrimaryRegion}"},
                    "VersioningConfiguration": {"Status": "Enabled"},
                    "ReplicationConfiguration": {
                        "Role": {"Fn::GetAtt": ["ReplicationRole", "Arn"]},
                        "Rules": [{
                            "Id": "ReplicateToSecondary",
                            "Status": "Enabled",
                            "Prefix": "",
                            "Destination": {
                                "Bucket": {"Fn::Sub": "arn:aws:s3:::secondary-data-${AWS::AccountId}-${SecondaryRegion}"},
                                "StorageClass": "STANDARD_IA"
                            }
                        }]
                    }
                }
            }
        }
    }
    
    # Deploy to primary region
    cloudformation.create_stack(
        StackName='data-infrastructure-primary',
        TemplateBody=json.dumps(template)
    )
```

### 62. How do you implement advanced security and compliance?
**Answer**: Enterprise security framework:

**Data Encryption and Key Management**:
```python
# KMS key management
kms = boto3.client('kms')

# Create customer-managed key
key_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Enable IAM User Permissions",
            "Effect": "Allow",
            "Principal": {"AWS": f"arn:aws:iam::{account_id}:root"},
            "Action": "kms:*",
            "Resource": "*"
        },
        {
            "Sid": "Allow use of the key for data engineering",
            "Effect": "Allow",
            "Principal": {"AWS": f"arn:aws:iam::{account_id}:role/DataEngineeringRole"},
            "Action": [
                "kms:Encrypt",
                "kms:Decrypt",
                "kms:ReEncrypt*",
                "kms:GenerateDataKey*",
                "kms:DescribeKey"
            ],
            "Resource": "*"
        }
    ]
}

key_response = kms.create_key(
    Policy=json.dumps(key_policy),
    Description='Data Engineering Encryption Key',
    Usage='ENCRYPT_DECRYPT',
    KeySpec='SYMMETRIC_DEFAULT'
)
```

### 63. How do you implement advanced analytics and machine learning pipelines?
**Answer**: ML pipeline architecture:

**SageMaker Integration**:
```python
# SageMaker pipeline for ML workflows
import sagemaker
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep

# Data preprocessing step
sklearn_processor = SKLearnProcessor(
    framework_version='0.23-1',
    role='arn:aws:iam::account:role/SageMakerRole',
    instance_type='ml.m5.xlarge',
    instance_count=1
)

processing_step = ProcessingStep(
    name='DataPreprocessing',
    processor=sklearn_processor,
    code='preprocessing.py',
    inputs=[
        ProcessingInput(
            source='s3://data-bucket/raw/',
            destination='/opt/ml/processing/input'
        )
    ],
    outputs=[
        ProcessingOutput(
            output_name='train',
            source='/opt/ml/processing/train'
        )
    ]
)

# Create pipeline
pipeline = Pipeline(
    name='MLPipeline',
    steps=[processing_step]
)

pipeline.create(role_arn='arn:aws:iam::account:role/SageMakerRole')
```

---

## Conceptual Questions (91-120)

### 91. What is AWS Well-Architected Framework and its pillars?
**Answer:**
**Five Pillars of Well-Architected Framework:**
- **Operational Excellence**: Run and monitor systems
- **Security**: Protect information and systems
- **Reliability**: Recover from failures and meet demand
- **Performance Efficiency**: Use resources efficiently
- **Cost Optimization**: Avoid unnecessary costs

### 92. How do you implement Infrastructure as Code (IaC) in AWS?
**Answer:**
```yaml
# CloudFormation template example
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Data Engineering Infrastructure'

Parameters:
  Environment:
    Type: String
    Default: 'dev'
    AllowedValues: ['dev', 'staging', 'prod']

Resources:
  DataLakeS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub 'data-lake-${Environment}-${AWS::AccountId}'
      VersioningConfiguration:
        Status: Enabled
      LifecycleConfiguration:
        Rules:
          - Id: TransitionToIA
            Status: Enabled
            Transitions:
              - TransitionInDays: 30
                StorageClass: STANDARD_IA

  GlueDatabase:
    Type: AWS::Glue::Database
    Properties:
      CatalogId: !Ref AWS::AccountId
      DatabaseInput:
        Name: !Sub '${Environment}_data_catalog'
        Description: 'Data catalog for analytics'
```

### 93. What are AWS service limits and how do you handle them?
**Answer:**
**Common Service Limits:**
- S3: 5TB per object, 100 buckets per account
- Lambda: 15 minutes execution time, 10GB memory
- Glue: 100 concurrent jobs per account
- Kinesis: 1000 records per second per shard

**Handling Strategies:**
```python
# Request limit increases
support = boto3.client('support')

# Create support case for limit increase
support.create_case(
    subject='Increase Glue Job Limit',
    serviceCode='amazon-glue',
    severityCode='low',
    categoryCode='service-limit-increase',
    communicationBody='Request to increase concurrent Glue jobs from 100 to 500'
)
```

---

## Architecture & Design Questions (121-150)

### 121. Design a real-time analytics platform for e-commerce
**Answer:**
**Architecture Components:**
1. **Data Ingestion**: Kinesis Data Streams for clickstream data
2. **Real-time Processing**: Kinesis Analytics for windowed aggregations
3. **Storage**: S3 for raw data, DynamoDB for real-time metrics
4. **Analytics**: Athena for ad-hoc queries, QuickSight for dashboards
5. **Alerting**: CloudWatch alarms with SNS notifications

**Implementation:**
```python
# Kinesis Analytics SQL for real-time metrics
analytics_sql = """
CREATE OR REPLACE STREAM "DESTINATION_SQL_STREAM" (
    product_id VARCHAR(32),
    view_count INTEGER,
    purchase_count INTEGER,
    conversion_rate DOUBLE,
    window_start TIMESTAMP,
    window_end TIMESTAMP
);

CREATE OR REPLACE PUMP "STREAM_PUMP" AS INSERT INTO "DESTINATION_SQL_STREAM"
SELECT STREAM 
    product_id,
    COUNT(CASE WHEN event_type = 'view' THEN 1 END) as view_count,
    COUNT(CASE WHEN event_type = 'purchase' THEN 1 END) as purchase_count,
    CAST(COUNT(CASE WHEN event_type = 'purchase' THEN 1 END) AS DOUBLE) / 
    CAST(COUNT(CASE WHEN event_type = 'view' THEN 1 END) AS DOUBLE) as conversion_rate,
    ROWTIME_TO_TIMESTAMP(MIN(ROWTIME)) as window_start,
    ROWTIME_TO_TIMESTAMP(MAX(ROWTIME)) as window_end
FROM SOURCE_SQL_STREAM_001
GROUP BY product_id, 
         RANGE_INTERVAL '5' MINUTE;
"""
```

### 122. Design a data warehouse solution for financial reporting
**Answer:**
**Architecture:**
1. **Source Systems**: Multiple databases, APIs, files
2. **Staging**: S3 with raw data partitioned by date
3. **ETL**: Glue jobs for data transformation and validation
4. **Data Warehouse**: Redshift with star schema design
5. **Reporting**: QuickSight with pre-built dashboards

**Redshift Schema Design:**
```sql
-- Fact table
CREATE TABLE fact_transactions (
    transaction_id BIGINT PRIMARY KEY,
    account_id BIGINT,
    product_id BIGINT,
    date_id INTEGER,
    amount DECIMAL(15,2),
    transaction_type VARCHAR(20),
    created_at TIMESTAMP
)
DISTKEY(account_id)
SORTKEY(date_id, created_at);

-- Dimension tables
CREATE TABLE dim_accounts (
    account_id BIGINT PRIMARY KEY,
    account_number VARCHAR(20),
    account_type VARCHAR(50),
    customer_id BIGINT,
    created_date DATE
)
DISTSTYLE ALL;

CREATE TABLE dim_products (
    product_id BIGINT PRIMARY KEY,
    product_name VARCHAR(100),
    product_category VARCHAR(50),
    product_type VARCHAR(50)
)
DISTSTYLE ALL;
```

---

## Security & Compliance Questions (151-180)

### 151. How do you implement data encryption at rest and in transit?
**Answer:**
**Encryption at Rest:**
```python
# S3 with KMS encryption
s3.put_object(
    Bucket='sensitive-data',
    Key='customer-data.csv',
    Body=data,
    ServerSideEncryption='aws:kms',
    SSEKMSKeyId='arn:aws:kms:region:account:key/key-id'
)

# RDS with encryption
rds.create_db_instance(
    DBInstanceIdentifier='encrypted-db',
    StorageEncrypted=True,
    KmsKeyId='arn:aws:kms:region:account:key/key-id'
)
```

**Encryption in Transit:**
```python
# Force HTTPS for S3
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Sid": "DenyInsecureConnections",
        "Effect": "Deny",
        "Principal": "*",
        "Action": "s3:*",
        "Resource": [
            "arn:aws:s3:::secure-bucket",
            "arn:aws:s3:::secure-bucket/*"
        ],
        "Condition": {
            "Bool": {"aws:SecureTransport": "false"}
        }
    }]
}
```

### 152. How do you implement data masking and anonymization?
**Answer:**
**Glue Data Masking:**
```python
# Custom transformation for data masking
def mask_pii_data(glue_context, ddf):
    """Mask personally identifiable information"""
    
    # Convert to Spark DataFrame
    df = ddf.toDF()
    
    # Mask email addresses
    df = df.withColumn("email", 
        regexp_replace(col("email"), "(.{3}).*(@.*)", "$1***$2"))
    
    # Mask phone numbers
    df = df.withColumn("phone", 
        regexp_replace(col("phone"), "(\\d{3})(\\d{3})(\\d{4})", "XXX-XXX-$3"))
    
    # Hash sensitive IDs
    df = df.withColumn("ssn", sha2(col("ssn"), 256))
    
    # Convert back to DynamicFrame
    return DynamicFrame.fromDF(df, glue_context, "masked_data")
```

---

## Performance & Optimization Questions (181-210)

### 181. How do you optimize Redshift query performance?
**Answer:**
**Query Optimization Techniques:**

```sql
-- Use appropriate distribution keys
CREATE TABLE sales (
    sale_id BIGINT,
    customer_id BIGINT,
    product_id BIGINT,
    sale_date DATE,
    amount DECIMAL(10,2)
)
DISTKEY(customer_id)  -- Distribute by frequently joined column
SORTKEY(sale_date);   -- Sort by frequently filtered column

-- Use column compression
CREATE TABLE compressed_sales (
    sale_id BIGINT ENCODE DELTA,
    customer_id BIGINT ENCODE DELTA32K,
    product_name VARCHAR(100) ENCODE LZO,
    sale_date DATE ENCODE DELTA32K,
    amount DECIMAL(10,2) ENCODE DELTA32K
);

-- Optimize joins
SELECT s.customer_id, SUM(s.amount) as total_sales
FROM sales s
INNER JOIN customers c ON s.customer_id = c.customer_id
WHERE s.sale_date >= '2024-01-01'
GROUP BY s.customer_id;
```

### 182. How do you optimize S3 performance for big data workloads?
**Answer:**
**S3 Performance Optimization:**

```python
# Use multipart upload for large files
def multipart_upload_large_file(bucket, key, file_path):
    """Optimize upload of large files using multipart upload"""
    
    s3 = boto3.client('s3')
    
    # Configure multipart upload
    config = TransferConfig(
        multipart_threshold=1024 * 25,  # 25MB
        max_concurrency=10,
        multipart_chunksize=1024 * 25,
        use_threads=True
    )
    
    # Upload with progress callback
    def progress_callback(bytes_transferred):
        print(f"Transferred: {bytes_transferred} bytes")
    
    s3.upload_file(
        file_path, bucket, key,
        Config=config,
        Callback=progress_callback
    )

# Optimize request patterns
def optimize_s3_requests():
    """Use request patterns that avoid hotspotting"""
    
    # Use random prefixes for high-throughput scenarios
    import uuid
    
    # Instead of: data/2024/01/15/file.json
    # Use: abc123/data/2024/01/15/file.json
    random_prefix = str(uuid.uuid4())[:6]
    key = f"{random_prefix}/data/2024/01/15/file.json"
    
    return key
```

---

## Scenario-Based Questions (211-240)

### 211. You have a data pipeline that processes 1TB of data daily, but it's taking 8 hours to complete. How would you optimize it?
**Answer:**
**Optimization Strategy:**

1. **Analyze Current Bottlenecks:**
```python
# CloudWatch metrics analysis
cloudwatch = boto3.client('cloudwatch')

# Check Glue job metrics
metrics = cloudwatch.get_metric_statistics(
    Namespace='Glue',
    MetricName='glue.driver.aggregate.numCompletedTasks',
    Dimensions=[{'Name': 'JobName', 'Value': 'data-processing-job'}],
    StartTime=datetime.utcnow() - timedelta(days=7),
    EndTime=datetime.utcnow(),
    Period=3600,
    Statistics=['Average', 'Maximum']
)
```

2. **Optimization Techniques:**
```python
# Increase parallelism
job_config = {
    'MaxCapacity': 20,  # Increase from default 10
    'WorkerType': 'G.2X',  # Use larger workers
    'NumberOfWorkers': 10,
    'DefaultArguments': {
        '--enable-spark-ui': 'true',
        '--spark-event-logs-path': 's3://spark-logs/',
        '--conf': 'spark.sql.adaptive.enabled=true',
        '--conf': 'spark.sql.adaptive.coalescePartitions.enabled=true',
        '--conf': 'spark.sql.adaptive.skewJoin.enabled=true'
    }
}

# Optimize data format and partitioning
# Convert CSV to Parquet with optimal partitioning
glue_script = """
# Read data
df = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://raw-data/"]},
    format="csv"
)

# Repartition for optimal processing
df = df.repartition(100)  # Adjust based on data size

# Write as Parquet with partitioning
glueContext.write_dynamic_frame.from_options(
    frame=df,
    connection_type="s3",
    connection_options={
        "path": "s3://processed-data/",
        "partitionKeys": ["year", "month", "day"]
    },
    format="parquet",
    format_options={"compression": "snappy"}
)
"""
```

### 212. Your Redshift cluster is running out of storage and queries are getting slower. What's your approach?
**Answer:**
**Comprehensive Redshift Optimization:**

1. **Immediate Actions:**
```sql
-- Identify large tables
SELECT 
    schemaname,
    tablename,
    size_in_mb
FROM (
    SELECT 
        schemaname,
        tablename,
        ROUND(SUM(size)/1024/1024, 2) as size_in_mb
    FROM (
        SELECT 
            schemaname,
            tablename,
            COUNT(*) * 1024 as size
        FROM stv_blocklist
        GROUP BY schemaname, tablename
    )
    GROUP BY schemaname, tablename
)
ORDER BY size_in_mb DESC;

-- Check table statistics
SELECT 
    schemaname,
    tablename,
    max_varchar,
    sortkey1,
    max_varchar,
    skew_sortkey1,
    skew_rows
FROM svv_table_info
WHERE schemaname = 'public'
ORDER BY size DESC;
```

2. **Storage Optimization:**
```sql
-- Implement table compression
CREATE TABLE optimized_sales (
    sale_id BIGINT ENCODE DELTA,
    customer_id BIGINT ENCODE DELTA32K,
    product_name VARCHAR(100) ENCODE LZO,
    sale_date DATE ENCODE DELTA32K,
    amount DECIMAL(10,2) ENCODE DELTA32K
)
DISTKEY(customer_id)
SORTKEY(sale_date);

-- Archive old data
CREATE TABLE sales_archive AS
SELECT * FROM sales 
WHERE sale_date < '2023-01-01';

DELETE FROM sales 
WHERE sale_date < '2023-01-01';

VACUUM sales;
```

This comprehensive collection of AWS interview questions covers all aspects of data engineering on AWS, from basic concepts to advanced architectural patterns, providing practical examples and real-world scenarios that demonstrate deep understanding of AWS services and best practices.