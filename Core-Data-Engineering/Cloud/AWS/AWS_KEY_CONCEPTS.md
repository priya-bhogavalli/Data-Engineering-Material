# AWS for Data Engineering - Key Concepts

## 🎯 What is AWS in Data Engineering?
Amazon Web Services provides cloud infrastructure and managed services for building scalable data pipelines, storage, and analytics solutions.

## 🔑 Core Data Services

### 1. Storage Services

#### S3 (Simple Storage Service)
```python
import boto3

# Basic S3 operations
s3 = boto3.client('s3')

# Upload file
s3.upload_file('local_file.csv', 'my-bucket', 'data/file.csv')

# Download file
s3.download_file('my-bucket', 'data/file.csv', 'local_file.csv')

# List objects
response = s3.list_objects_v2(Bucket='my-bucket', Prefix='data/')
```

**Use Cases**: Data lake storage, backup, static website hosting
**Key Features**: Unlimited storage, multiple storage classes, lifecycle policies

### 2. Compute Services

#### EC2 (Elastic Compute Cloud)
- **Purpose**: Virtual servers for custom data processing
- **Use Cases**: Self-managed Spark clusters, custom applications
- **Key Features**: Multiple instance types, auto-scaling, spot instances

#### Lambda
```python
import json

def lambda_handler(event, context):
    """Process S3 events"""
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        # Process file
        process_file(bucket, key)
    
    return {'statusCode': 200}
```

**Use Cases**: Event-driven processing, ETL triggers, data validation
**Key Features**: Serverless, automatic scaling, pay-per-execution

### 3. Database Services

#### RDS (Relational Database Service)
```python
import sqlalchemy as sa

# Connect to RDS
engine = sa.create_engine(
    'postgresql://username:password@rds-endpoint:5432/database'
)

# Query data
df = pd.read_sql('SELECT * FROM sales', engine)
```

**Use Cases**: Transactional databases, OLTP systems
**Supported Engines**: PostgreSQL, MySQL, Oracle, SQL Server, MariaDB

#### DynamoDB
```python
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('user-data')

# Put item
table.put_item(Item={'user_id': '123', 'name': 'John', 'email': 'john@example.com'})

# Get item
response = table.get_item(Key={'user_id': '123'})
```

**Use Cases**: NoSQL applications, high-throughput workloads
**Key Features**: Serverless, auto-scaling, single-digit millisecond latency

### 4. Analytics Services

#### Athena
```sql
-- Query S3 data directly with SQL
CREATE EXTERNAL TABLE sales (
    order_id string,
    customer_id string,
    amount double,
    order_date date
)
STORED AS PARQUET
LOCATION 's3://my-bucket/sales-data/';

SELECT customer_id, SUM(amount) as total
FROM sales
WHERE order_date >= '2023-01-01'
GROUP BY customer_id;
```

**Use Cases**: Ad-hoc queries on S3 data, serverless analytics
**Key Features**: No infrastructure, pay-per-query, standard SQL

#### Redshift
```python
import psycopg2

# Connect to Redshift
conn = psycopg2.connect(
    host='redshift-cluster.amazonaws.com',
    port=5439,
    database='dev',
    user='username',
    password='password'
)

# Execute query
cursor = conn.cursor()
cursor.execute("SELECT * FROM sales LIMIT 10")
results = cursor.fetchall()
```

**Use Cases**: Data warehousing, OLAP, business intelligence
**Key Features**: Columnar storage, massively parallel processing

## 🔄 Data Pipeline Services

### 1. AWS Glue
```python
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Initialize Glue context
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# Read from catalog
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="my_database",
    table_name="my_table"
)

# Transform data
transformed = ApplyMapping.apply(
    frame=datasource,
    mappings=[
        ("old_column", "string", "new_column", "string"),
        ("amount", "double", "amount", "double")
    ]
)

# Write to S3
glueContext.write_dynamic_frame.from_options(
    frame=transformed,
    connection_type="s3",
    connection_options={"path": "s3://my-bucket/output/"},
    format="parquet"
)
```

**Use Cases**: ETL jobs, data catalog, schema discovery
**Key Features**: Serverless, auto-scaling, integrated with other AWS services

### 2. Kinesis (Streaming)
```python
import boto3
import json

kinesis = boto3.client('kinesis')

# Put record to stream
kinesis.put_record(
    StreamName='my-stream',
    Data=json.dumps({'user_id': '123', 'action': 'click'}),
    PartitionKey='user_123'
)

# Process with Lambda
def lambda_handler(event, context):
    for record in event['Records']:
        # Decode data
        data = json.loads(record['kinesis']['data'])
        # Process record
        process_event(data)
```

**Use Cases**: Real-time data streaming, event processing
**Key Features**: Real-time processing, automatic scaling, integration with analytics

### 3. Step Functions
```json
{
  "Comment": "Data processing workflow",
  "StartAt": "ExtractData",
  "States": {
    "ExtractData": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:region:account:function:extract-data",
      "Next": "TransformData"
    },
    "TransformData": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:region:account:function:transform-data",
      "Next": "LoadData"
    },
    "LoadData": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:region:account:function:load-data",
      "End": true
    }
  }
}
```

**Use Cases**: Workflow orchestration, complex data pipelines
**Key Features**: Visual workflows, error handling, parallel execution

## 🛠️ Infrastructure as Code

### CloudFormation
```yaml
Resources:
  DataBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-data-bucket
      VersioningConfiguration:
        Status: Enabled
  
  GlueJob:
    Type: AWS::Glue::Job
    Properties:
      Name: data-processing-job
      Role: !Ref GlueRole
      Command:
        Name: glueetl
        ScriptLocation: s3://my-scripts/etl-job.py
```

### Terraform
```hcl
resource "aws_s3_bucket" "data_bucket" {
  bucket = "my-data-bucket"
}

resource "aws_glue_job" "etl_job" {
  name     = "data-processing-job"
  role_arn = aws_iam_role.glue_role.arn
  
  command {
    name            = "glueetl"
    script_location = "s3://my-scripts/etl-job.py"
  }
}
```

## 🔐 Security and Access

### IAM (Identity and Access Management)
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-data-bucket/*"
    },
    {
      "Effect": "Allow",
      "Action": "glue:StartJobRun",
      "Resource": "*"
    }
  ]
}
```

## 📊 Common Architecture Patterns

### 1. Data Lake Architecture
```
S3 (Raw Data) → Glue (ETL) → S3 (Processed) → Athena (Query) → QuickSight (Visualization)
```

### 2. Real-time Analytics
```
Kinesis (Streaming) → Lambda (Processing) → DynamoDB (Storage) → API Gateway (Access)
```

### 3. Data Warehouse
```
S3 (Staging) → Glue (ETL) → Redshift (Warehouse) → BI Tools (Analysis)
```

## 🎯 Cost Optimization
- **S3**: Use appropriate storage classes (IA, Glacier)
- **EC2**: Use spot instances for batch processing
- **Lambda**: Optimize memory allocation and execution time
- **Redshift**: Use reserved instances, pause clusters when not in use
- **Glue**: Use job bookmarks to avoid reprocessing data

## 📊 When to Use AWS Services
- **S3**: All data storage needs, data lake foundation
- **Lambda**: Event-driven processing, lightweight ETL
- **Glue**: Managed ETL, data catalog
- **Athena**: Ad-hoc queries on S3 data
- **Redshift**: Data warehousing, complex analytics
- **Kinesis**: Real-time streaming data

## 🎯 Interview Focus Areas
1. **Storage**: S3 features, storage classes, lifecycle policies
2. **Compute**: EC2 vs Lambda use cases
3. **Databases**: RDS vs DynamoDB comparison
4. **Analytics**: Athena vs Redshift vs EMR
5. **ETL**: Glue capabilities and limitations
6. **Streaming**: Kinesis vs SQS vs SNS
7. **Security**: IAM roles, policies, encryption

## 📚 Quick References
- [AWS Documentation](https://docs.aws.amazon.com/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Pricing Calculator](https://calculator.aws/)
- [AWS CLI Reference](https://docs.aws.amazon.com/cli/)