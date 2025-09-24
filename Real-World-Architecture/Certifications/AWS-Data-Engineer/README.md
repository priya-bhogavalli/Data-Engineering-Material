# 🎓 AWS Certified Data Engineer Study Guide

> **Complete preparation guide for the AWS Certified Data Engineer - Associate (DEA-C01) certification**

## 📋 **Certification Overview**

### **Exam Details**
- **Exam Code**: DEA-C01
- **Duration**: 170 minutes
- **Questions**: 85 questions (multiple choice & multiple response)
- **Passing Score**: 720/1000
- **Cost**: $150 USD
- **Validity**: 3 years
- **Prerequisites**: None (Associate level)

### **Target Audience**
- Data engineers with 2+ years AWS experience
- Professionals designing data pipelines
- Engineers implementing data solutions on AWS

---

## 🎯 **Exam Domains & Weightings**

| Domain | Weight | Key Topics |
|--------|--------|------------|
| **Domain 1: Data Ingestion & Transformation** | 34% | Kinesis, Glue, EMR, Lambda |
| **Domain 2: Data Store Management** | 26% | S3, RDS, DynamoDB, Redshift |
| **Domain 3: Data Operations & Support** | 22% | Monitoring, Security, Optimization |
| **Domain 4: Data Security & Governance** | 18% | IAM, Encryption, Compliance |

---

## 📚 **Domain 1: Data Ingestion & Transformation (34%)**

### **Key Services to Master**

#### **Amazon Kinesis Family**
```python
# Kinesis Data Streams - Real-time data ingestion
import boto3

kinesis = boto3.client('kinesis')

# Put record to stream
response = kinesis.put_record(
    StreamName='user-events',
    Data=json.dumps({
        'user_id': '12345',
        'event_type': 'page_view',
        'timestamp': datetime.utcnow().isoformat()
    }),
    PartitionKey='user_12345'
)

# Kinesis Analytics - Real-time processing
CREATE STREAM processed_events (
    user_id VARCHAR(32),
    event_count INTEGER,
    window_start TIMESTAMP
);

CREATE PUMP "STREAM_PUMP" AS INSERT INTO processed_events
SELECT user_id, COUNT(*) as event_count, ROWTIME_TO_TIMESTAMP(ROWTIME)
FROM SOURCE_SQL_STREAM_001
GROUP BY user_id, RANGE_INTERVAL '1' MINUTE;
```

#### **AWS Glue**
```python
# Glue ETL Job
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

# Read from S3
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="ecommerce_db",
    table_name="raw_orders"
)

# Transform data
transformed = ApplyMapping.apply(
    frame=datasource,
    mappings=[
        ("order_id", "string", "order_id", "string"),
        ("customer_id", "string", "customer_id", "string"),
        ("order_amount", "double", "order_amount", "decimal(10,2)"),
        ("order_date", "string", "order_date", "date")
    ]
)

# Write to Redshift
glueContext.write_dynamic_frame.from_jdbc_conf(
    frame=transformed,
    catalog_connection="redshift-connection",
    connection_options={"dbtable": "processed_orders", "database": "analytics"}
)

job.commit()
```

#### **Amazon EMR**
```python
# EMR Cluster Configuration
cluster_config = {
    'Name': 'DataProcessingCluster',
    'ReleaseLabel': 'emr-6.15.0',
    'Applications': [
        {'Name': 'Spark'},
        {'Name': 'Hadoop'},
        {'Name': 'Hive'}
    ],
    'Instances': {
        'InstanceGroups': [
            {
                'Name': 'Master',
                'Market': 'ON_DEMAND',
                'InstanceRole': 'MASTER',
                'InstanceType': 'm5.xlarge',
                'InstanceCount': 1
            },
            {
                'Name': 'Workers',
                'Market': 'SPOT',
                'InstanceRole': 'CORE',
                'InstanceType': 'm5.large',
                'InstanceCount': 3,
                'BidPrice': '0.10'
            }
        ]
    },
    'ServiceRole': 'EMR_DefaultRole',
    'JobFlowRole': 'EMR_EC2_DefaultRole'
}
```

### **Practice Questions**
1. **Which service provides the lowest latency for real-time data ingestion?**
   - A) Kinesis Data Firehose
   - B) Kinesis Data Streams ✅
   - C) SQS
   - D) SNS

2. **What is the maximum retention period for Kinesis Data Streams?**
   - A) 24 hours
   - B) 7 days
   - C) 365 days ✅
   - D) Unlimited

---

## 🗄️ **Domain 2: Data Store Management (26%)**

### **Key Services**

#### **Amazon S3**
```python
# S3 Storage Classes and Lifecycle
lifecycle_config = {
    'Rules': [
        {
            'ID': 'DataLakeLifecycle',
            'Status': 'Enabled',
            'Filter': {'Prefix': 'data/'},
            'Transitions': [
                {
                    'Days': 30,
                    'StorageClass': 'STANDARD_IA'
                },
                {
                    'Days': 90,
                    'StorageClass': 'GLACIER'
                },
                {
                    'Days': 365,
                    'StorageClass': 'DEEP_ARCHIVE'
                }
            ]
        }
    ]
}

# S3 Event Notifications
event_config = {
    'LambdaConfigurations': [
        {
            'Id': 'ProcessNewData',
            'LambdaFunctionArn': 'arn:aws:lambda:us-east-1:123456789012:function:ProcessData',
            'Events': ['s3:ObjectCreated:*'],
            'Filter': {
                'Key': {
                    'FilterRules': [
                        {
                            'Name': 'prefix',
                            'Value': 'incoming/'
                        },
                        {
                            'Name': 'suffix',
                            'Value': '.json'
                        }
                    ]
                }
            }
        }
    ]
}
```

#### **Amazon Redshift**
```sql
-- Redshift Distribution and Sort Keys
CREATE TABLE sales_fact (
    sale_id BIGINT IDENTITY(1,1),
    customer_id INTEGER,
    product_id INTEGER,
    sale_date DATE,
    amount DECIMAL(10,2)
)
DISTKEY(customer_id)  -- Distribute by customer_id
SORTKEY(sale_date);   -- Sort by date for time-series queries

-- Redshift Spectrum for S3 querying
CREATE EXTERNAL SCHEMA spectrum_schema
FROM DATA CATALOG
DATABASE 'external_db'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftSpectrumRole';

-- Query S3 data directly
SELECT customer_id, SUM(amount) as total_sales
FROM spectrum_schema.external_sales
WHERE sale_date >= '2024-01-01'
GROUP BY customer_id;
```

#### **Amazon DynamoDB**
```python
# DynamoDB Design Patterns
import boto3

dynamodb = boto3.resource('dynamodb')

# Single Table Design
table = dynamodb.Table('EcommerceData')

# Put item with GSI
table.put_item(
    Item={
        'PK': 'USER#12345',
        'SK': 'PROFILE',
        'GSI1PK': 'EMAIL#user@example.com',
        'GSI1SK': 'USER#12345',
        'user_name': 'John Doe',
        'email': 'user@example.com',
        'created_at': '2024-01-01T00:00:00Z'
    }
)

# Query with GSI
response = table.query(
    IndexName='GSI1',
    KeyConditionExpression=Key('GSI1PK').eq('EMAIL#user@example.com')
)
```

### **Practice Questions**
1. **Which Redshift feature allows querying S3 data without loading it?**
   - A) Redshift ML
   - B) Redshift Spectrum ✅
   - C) Redshift Serverless
   - D) Redshift Concurrency Scaling

---

## 🔧 **Domain 3: Data Operations & Support (22%)**

### **Monitoring & Optimization**

#### **CloudWatch Metrics**
```python
# Custom CloudWatch Metrics
import boto3

cloudwatch = boto3.client('cloudwatch')

def publish_pipeline_metrics(pipeline_name, records_processed, processing_time):
    cloudwatch.put_metric_data(
        Namespace='DataPipeline',
        MetricData=[
            {
                'MetricName': 'RecordsProcessed',
                'Dimensions': [
                    {
                        'Name': 'PipelineName',
                        'Value': pipeline_name
                    }
                ],
                'Value': records_processed,
                'Unit': 'Count'
            },
            {
                'MetricName': 'ProcessingTime',
                'Dimensions': [
                    {
                        'Name': 'PipelineName',
                        'Value': pipeline_name
                    }
                ],
                'Value': processing_time,
                'Unit': 'Seconds'
            }
        ]
    )

# CloudWatch Alarms
alarm_config = {
    'AlarmName': 'HighDataProcessingLatency',
    'ComparisonOperator': 'GreaterThanThreshold',
    'EvaluationPeriods': 2,
    'MetricName': 'ProcessingTime',
    'Namespace': 'DataPipeline',
    'Period': 300,
    'Statistic': 'Average',
    'Threshold': 600.0,
    'ActionsEnabled': True,
    'AlarmActions': [
        'arn:aws:sns:us-east-1:123456789012:data-alerts'
    ]
}
```

#### **Cost Optimization**
```python
# S3 Storage Class Analysis
def analyze_s3_storage_costs():
    s3 = boto3.client('s3')
    
    # Get storage metrics
    response = s3.get_bucket_analytics_configuration(
        Bucket='data-lake-bucket',
        Id='StorageAnalytics'
    )
    
    # Recommend storage class transitions
    recommendations = []
    
    for obj in s3.list_objects_v2(Bucket='data-lake-bucket')['Contents']:
        last_modified = obj['LastModified']
        age_days = (datetime.now(timezone.utc) - last_modified).days
        
        if age_days > 30 and obj['StorageClass'] == 'STANDARD':
            recommendations.append({
                'key': obj['Key'],
                'current_class': 'STANDARD',
                'recommended_class': 'STANDARD_IA',
                'potential_savings': calculate_savings(obj['Size'], 'STANDARD_IA')
            })
    
    return recommendations
```

---

## 🔒 **Domain 4: Data Security & Governance (18%)**

### **Security Best Practices**

#### **IAM Policies for Data Access**
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
            "Resource": "arn:aws:s3:::data-lake-bucket/department/${aws:PrincipalTag/Department}/*",
            "Condition": {
                "StringEquals": {
                    "s3:x-amz-server-side-encryption": "AES256"
                }
            }
        }
    ]
}
```

#### **Data Encryption**
```python
# S3 Encryption Configuration
encryption_config = {
    'Rules': [
        {
            'ApplyServerSideEncryptionByDefault': {
                'SSEAlgorithm': 'aws:kms',
                'KMSMasterKeyID': 'arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012'
            },
            'BucketKeyEnabled': True
        }
    ]
}

# RDS Encryption
rds_config = {
    'DBInstanceIdentifier': 'analytics-db',
    'StorageEncrypted': True,
    'KmsKeyId': 'arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012'
}
```

---

## 📖 **Study Plan (8-12 Weeks)**

### **Week 1-2: Foundation**
- AWS Data Services Overview
- S3 Deep Dive
- IAM for Data Services

### **Week 3-4: Data Ingestion**
- Kinesis Family
- AWS Glue
- Lambda for Data Processing

### **Week 5-6: Data Storage**
- Redshift
- DynamoDB
- RDS

### **Week 7-8: Big Data Processing**
- EMR
- Athena
- QuickSight

### **Week 9-10: Operations & Security**
- CloudWatch
- CloudTrail
- Data Encryption

### **Week 11-12: Practice & Review**
- Practice Exams
- Hands-on Labs
- Review Weak Areas

---

## 🛠️ **Hands-on Labs**

### **Lab 1: Build a Data Lake**
```bash
# Create S3 bucket with proper configuration
aws s3 mb s3://my-data-lake-bucket
aws s3api put-bucket-encryption \
    --bucket my-data-lake-bucket \
    --server-side-encryption-configuration file://encryption.json

# Set up Glue Crawler
aws glue create-crawler \
    --name data-lake-crawler \
    --role GlueServiceRole \
    --database-name data_lake_db \
    --targets S3Targets=[{Path=s3://my-data-lake-bucket/}]
```

### **Lab 2: Real-time Analytics Pipeline**
```python
# Create Kinesis stream
kinesis = boto3.client('kinesis')
kinesis.create_stream(
    StreamName='analytics-stream',
    ShardCount=2
)

# Lambda function for processing
def lambda_handler(event, context):
    for record in event['Records']:
        # Decode Kinesis data
        payload = base64.b64decode(record['kinesis']['data'])
        data = json.loads(payload)
        
        # Process and store in DynamoDB
        dynamodb.put_item(
            TableName='processed-events',
            Item={
                'event_id': {'S': data['event_id']},
                'timestamp': {'S': data['timestamp']},
                'processed_at': {'S': datetime.utcnow().isoformat()}
            }
        )
```

---

## 📝 **Practice Exam Questions**

### **Sample Questions**

1. **A company needs to process streaming data with sub-second latency. Which service should they use?**
   - A) Kinesis Data Firehose
   - B) Kinesis Data Streams ✅
   - C) SQS
   - D) Step Functions

2. **What is the most cost-effective way to store infrequently accessed data in S3?**
   - A) S3 Standard
   - B) S3 Standard-IA ✅
   - C) S3 One Zone-IA
   - D) S3 Glacier

3. **Which Glue component automatically discovers schema from data sources?**
   - A) Glue Jobs
   - B) Glue Crawlers ✅
   - C) Glue Triggers
   - D) Glue Workflows

---

## 📚 **Recommended Resources**

### **Official AWS Resources**
- [AWS Data Engineer Learning Path](https://aws.amazon.com/training/learning-paths/data-engineer/)
- [AWS Whitepapers](https://aws.amazon.com/whitepapers/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

### **Practice Exams**
- AWS Official Practice Exam
- Whizlabs AWS Data Engineer Practice Tests
- Tutorials Dojo Practice Exams

### **Hands-on Experience**
- AWS Free Tier Account
- AWS Workshops
- AWS Samples GitHub Repository

---

## 🎯 **Exam Tips**

### **Day Before Exam**
- Review key service limits and quotas
- Practice CLI commands
- Review security best practices
- Get good rest

### **During Exam**
- Read questions carefully
- Eliminate obviously wrong answers
- Flag difficult questions for review
- Manage time effectively (2 minutes per question)

### **Common Pitfalls**
- Confusing Kinesis Data Streams vs Firehose
- Not understanding Redshift distribution keys
- Missing security requirements in scenarios
- Overlooking cost optimization opportunities

---

**🎓 With proper preparation and hands-on practice, you'll be ready to pass the AWS Certified Data Engineer exam and advance your cloud data engineering career!**