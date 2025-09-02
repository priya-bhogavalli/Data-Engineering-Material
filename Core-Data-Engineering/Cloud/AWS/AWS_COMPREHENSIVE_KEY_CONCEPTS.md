# AWS Comprehensive Key Concepts for Data Engineering

## 🎯 **Overview**
This comprehensive guide covers all essential AWS services and concepts for data engineering, from basic storage and compute services to advanced analytics and machine learning platforms. Each section includes practical examples, best practices, and real-world implementation patterns.

**What You'll Learn:**
- Core AWS services for data engineering workflows
- Storage strategies for data lakes and warehouses
- Compute options for batch and real-time processing
- Database services for different data models
- Analytics and ML services for insights
- Security, monitoring, and cost optimization
- Integration patterns and architecture designs

**Target Audience:**
- Data Engineers (1-10+ years experience)
- Cloud Architects working with data
- DevOps Engineers supporting data platforms
- Data Scientists needing infrastructure knowledge
- Solution Architects designing data systems

## 📋 Table of Contents

1. [AWS Core Services Overview](#1-aws-core-services-overview)
2. [Storage Services](#2-storage-services)
   - [S3 (Simple Storage Service)](#s3-simple-storage-service)
   - [EBS (Elastic Block Store)](#ebs-elastic-block-store)
   - [EFS (Elastic File System)](#efs-elastic-file-system)
3. [Compute Services](#3-compute-services)
   - [EC2 (Elastic Compute Cloud)](#ec2-elastic-compute-cloud)
   - [Lambda (Serverless Computing)](#lambda-serverless-computing)
   - [ECS/Fargate (Container Services)](#ecsfargate-container-services)
4. [Database Services](#4-database-services)
   - [RDS (Relational Database Service)](#rds-relational-database-service)
   - [DynamoDB (NoSQL Database)](#dynamodb-nosql-database)
   - [Redshift (Data Warehouse)](#redshift-data-warehouse)
5. [Analytics and Big Data Services](#5-analytics-and-big-data-services)
   - [EMR (Elastic MapReduce)](#emr-elastic-mapreduce)
   - [Glue (ETL Service)](#glue-etl-service)
   - [Athena (Serverless Query Service)](#athena-serverless-query-service)
6. [Streaming and Real-time Services](#6-streaming-and-real-time-services)
   - [Kinesis Data Streams](#kinesis-data-streams)
   - [Kinesis Data Firehose](#kinesis-data-firehose)
   - [MSK (Managed Streaming for Kafka)](#msk-managed-streaming-for-kafka)
7. [Machine Learning Services](#7-machine-learning-services)
   - [SageMaker](#sagemaker)
8. [Orchestration and Workflow](#8-orchestration-and-workflow)
   - [Step Functions](#step-functions)
   - [EventBridge (CloudWatch Events)](#eventbridge-cloudwatch-events)
9. [Monitoring and Security](#9-monitoring-and-security)
   - [CloudWatch](#cloudwatch)
   - [KMS (Key Management Service)](#kms-key-management-service)
10. [Cost Optimization and Best Practices](#10-cost-optimization-and-best-practices)
    - [Resource Tagging Strategy](#resource-tagging-strategy)
    - [Auto Scaling](#auto-scaling)
    - [Spot Instances for Cost Savings](#spot-instances-for-cost-savings)

---

## 1. AWS Core Services Overview

### AWS Global Infrastructure
**Understanding AWS's global reach and reliability:**

**Regions (25+ worldwide)**:
- **Definition**: Geographically separated areas containing multiple data centers
- **Purpose**: Data sovereignty, latency reduction, disaster recovery
- **Key Regions for Data Engineering**: us-east-1 (N. Virginia), us-west-2 (Oregon), eu-west-1 (Ireland)
- **Selection Criteria**: Data residency requirements, service availability, cost, latency

**Availability Zones (80+ globally)**:
- **Definition**: Isolated data centers within a region (typically 3-6 per region)
- **Purpose**: High availability, fault tolerance, load distribution
- **Data Engineering Impact**: Multi-AZ deployments for RDS, Redshift, EMR clusters
- **Best Practice**: Distribute workloads across multiple AZs for resilience

**Edge Locations (400+ worldwide)**:
- **Definition**: CDN endpoints for CloudFront content delivery
- **Purpose**: Reduce latency for global data access
- **Data Engineering Use**: Accelerate S3 transfers, cache query results, global data distribution

**Local Zones & Wavelength**:
- **Local Zones**: Extensions of regions for ultra-low latency (single-digit milliseconds)
- **Wavelength**: 5G edge computing for mobile applications
- **Use Cases**: Real-time analytics, IoT data processing, edge ML inference

### Identity and Access Management (IAM)
**The foundation of AWS security for data engineering:**

**Core Components:**
- **Users**: Individual identities with long-term credentials
- **Groups**: Collections of users with shared permissions
- **Roles**: Temporary credentials for services and cross-account access
- **Policies**: JSON documents defining permissions

**Data Engineering IAM Strategy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DataLakeReadWrite",
      "Effect": "Allow",
      "Principal": {"AWS": "arn:aws:iam::123456789012:user/DataEngineer"},
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::data-lake",
        "arn:aws:s3:::data-lake/*"
      ],
      "Condition": {
        "StringEquals": {
          "s3:x-amz-server-side-encryption": "AES256"
        },
        "IpAddress": {
          "aws:SourceIp": "203.0.113.0/24"
        }
      }
    },
    {
      "Sid": "GlueJobExecution",
      "Effect": "Allow",
      "Action": [
        "glue:StartJobRun",
        "glue:GetJobRun",
        "glue:GetJobRuns",
        "glue:BatchStopJobRun"
      ],
      "Resource": "arn:aws:glue:*:*:job/data-processing-*"
    }
  ]
}
```

**Best Practices for Data Teams:**
- Use roles instead of users for service access
- Implement least privilege principle
- Enable MFA for sensitive operations
- Regular access reviews and rotation
- Use AWS Organizations for multi-account governance
```

## 2. Storage Services

### S3 (Simple Storage Service)
**The backbone of modern data lakes and analytics platforms**

**Why S3 is Essential for Data Engineering:**
- **Unlimited Scale**: Store petabytes of data without capacity planning
- **11 9's Durability**: 99.999999999% durability across multiple facilities
- **Cost Effective**: Multiple storage classes for different access patterns
- **Integration Hub**: Native integration with 100+ AWS services
- **Global Access**: Access data from anywhere with proper permissions

**Data Lake Architecture with S3:**
```python
import boto3
import pandas as pd
from datetime import datetime

s3 = boto3.client('s3')

# Recommended data lake structure
data_lake_structure = {
    'raw/': {
        'description': 'Unprocessed data in original format',
        'retention': '7 years for compliance',
        'storage_class': 'STANDARD → IA → Glacier → Deep Archive',
        'access_pattern': 'Write once, read occasionally',
        'examples': [
            'raw/source=salesforce/year=2024/month=01/day=15/contacts.json',
            'raw/source=database/year=2024/month=01/day=15/transactions.parquet'
        ]
    },
    'processed/': {
        'description': 'Cleaned and validated data',
        'retention': '3 years',
        'storage_class': 'STANDARD → IA',
        'access_pattern': 'Regular access for analytics',
        'examples': [
            'processed/dataset=customer_360/year=2024/month=01/customers.parquet',
            'processed/dataset=sales_metrics/year=2024/month=01/daily_sales.parquet'
        ]
    },
    'curated/': {
        'description': 'Business-ready datasets for analytics',
        'retention': '1 year active access',
        'storage_class': 'STANDARD',
        'access_pattern': 'Frequent access by analysts and BI tools',
        'examples': [
            'curated/domain=finance/monthly_revenue_summary.parquet',
            'curated/domain=marketing/customer_segments.parquet'
        ]
    },
    'temp/': {
        'description': 'Temporary processing files',
        'retention': '7 days auto-delete',
        'storage_class': 'STANDARD',
        'access_pattern': 'Short-term processing',
        'examples': [
            'temp/spark-jobs/job-12345/intermediate_results.parquet',
            'temp/glue-jobs/etl-run-67890/staging_data.csv'
        ]
    }
}

# Upload with intelligent partitioning
def upload_partitioned_data(df, bucket, dataset_name, partition_cols=['year', 'month', 'day']):
    """Upload DataFrame with automatic partitioning for optimal query performance."""
    
    # Add partition columns if not present
    if 'date' in df.columns:
        df['year'] = pd.to_datetime(df['date']).dt.year
        df['month'] = pd.to_datetime(df['date']).dt.month
        df['day'] = pd.to_datetime(df['date']).dt.day
    
    # Group by partition columns
    for partition_values, group_df in df.groupby(partition_cols):
        # Create partition path
        partition_path = '/'.join([f"{col}={val}" for col, val in zip(partition_cols, partition_values)])
        key = f"processed/dataset={dataset_name}/{partition_path}/data.parquet"
        
        # Upload partition
        parquet_buffer = group_df.to_parquet(index=False)
        s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=parquet_buffer,
            StorageClass='STANDARD',
            ServerSideEncryption='AES256',
            Metadata={
                'dataset': dataset_name,
                'partition_date': str(partition_values[0]) if partition_cols[0] == 'year' else '',
                'record_count': str(len(group_df)),
                'upload_timestamp': datetime.utcnow().isoformat()
            }
        )
        print(f"Uploaded partition: {key} ({len(group_df)} records)")

# Advanced S3 operations for data engineering
def setup_data_lake_bucket(bucket_name, region='us-east-1'):
    """Create and configure S3 bucket for data lake with best practices."""
    
    # Create bucket
    if region == 'us-east-1':
        s3.create_bucket(Bucket=bucket_name)
    else:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )
    
    # Enable versioning for data protection
    s3.put_bucket_versioning(
        Bucket=bucket_name,
        VersioningConfiguration={'Status': 'Enabled'}
    )
    
    # Configure lifecycle management
    lifecycle_config = {
        'Rules': [
            {
                'ID': 'DataLakeLifecycle',
                'Status': 'Enabled',
                'Filter': {'Prefix': 'raw/'},
                'Transitions': [
                    {'Days': 30, 'StorageClass': 'STANDARD_IA'},
                    {'Days': 90, 'StorageClass': 'GLACIER'},
                    {'Days': 365, 'StorageClass': 'DEEP_ARCHIVE'}
                ],
                'NoncurrentVersionTransitions': [
                    {'NoncurrentDays': 30, 'StorageClass': 'STANDARD_IA'},
                    {'NoncurrentDays': 90, 'StorageClass': 'GLACIER'}
                ],
                'NoncurrentVersionExpiration': {'NoncurrentDays': 2555}  # 7 years
            },
            {
                'ID': 'TempDataCleanup',
                'Status': 'Enabled',
                'Filter': {'Prefix': 'temp/'},
                'Expiration': {'Days': 7}
            }
        ]
    }
    
    s3.put_bucket_lifecycle_configuration(
        Bucket=bucket_name,
        LifecycleConfiguration=lifecycle_config
    )
    
    # Enable default encryption
    s3.put_bucket_encryption(
        Bucket=bucket_name,
        ServerSideEncryptionConfiguration={
            'Rules': [{
                'ApplyServerSideEncryptionByDefault': {
                    'SSEAlgorithm': 'AES256'
                },
                'BucketKeyEnabled': True
            }]
        }
    )
    
    print(f"Data lake bucket '{bucket_name}' configured successfully")
    return bucket_name

# Lifecycle management
lifecycle_config = {
    'Rules': [{
        'Status': 'Enabled',
        'Transitions': [
            {'Days': 30, 'StorageClass': 'STANDARD_IA'},
            {'Days': 90, 'StorageClass': 'GLACIER'}
        ]
    }]
}
```

### EBS (Elastic Block Store)
**High-performance block storage for data-intensive applications**

**Why EBS Matters for Data Engineering:**
- **Persistent Storage**: Data survives instance termination
- **High Performance**: Up to 64,000 IOPS and 1,000 MB/s throughput
- **Scalable**: Resize volumes without downtime
- **Backup & Recovery**: Point-in-time snapshots
- **Encryption**: At-rest and in-transit encryption

**EBS Volume Types for Data Workloads:**
```python
ec2 = boto3.client('ec2')

# Volume type selection guide
volume_types = {
    'gp3': {
        'description': 'General Purpose SSD (latest generation)',
        'use_cases': ['Boot volumes', 'Development environments', 'Small to medium databases'],
        'performance': 'Baseline 3,000 IOPS, up to 16,000 IOPS',
        'throughput': 'Up to 1,000 MB/s',
        'cost': 'Most cost-effective for general workloads'
    },
    'io2': {
        'description': 'Provisioned IOPS SSD (latest)',
        'use_cases': ['Critical databases', 'High-performance analytics', 'NoSQL databases'],
        'performance': 'Up to 64,000 IOPS per volume',
        'throughput': 'Up to 1,000 MB/s',
        'durability': '99.999% durability (10x better than io1)'
    },
    'st1': {
        'description': 'Throughput Optimized HDD',
        'use_cases': ['Big data processing', 'Data warehouses', 'Log processing'],
        'performance': 'Up to 500 IOPS',
        'throughput': 'Up to 500 MB/s',
        'cost': 'Lowest cost for high-throughput workloads'
    }
}

# Create optimized volumes for different data workloads
def create_data_processing_volume(availability_zone, workload_type='analytics'):
    """Create EBS volume optimized for specific data workloads."""
    
    if workload_type == 'analytics':
        volume = ec2.create_volume(
            Size=1000,
            VolumeType='gp3',
            Iops=4000,
            Throughput=250,
            AvailabilityZone=availability_zone,
            Encrypted=True
        )
    elif workload_type == 'database':
        volume = ec2.create_volume(
            Size=500,
            VolumeType='io2',
            Iops=10000,
            AvailabilityZone=availability_zone,
            Encrypted=True
        )
    
    return volume
```

### EFS (Elastic File System)
**Fully managed NFS for distributed data processing**

**Why EFS is Valuable for Data Engineering:**
- **Shared Access**: Multiple EC2 instances can access simultaneously
- **Elastic Scaling**: Automatically grows and shrinks with usage
- **POSIX Compliance**: Standard file system semantics
- **High Availability**: Replicated across multiple AZs
- **Performance Modes**: Optimized for different workload patterns

**EFS Configuration for Data Workloads:**
```python
efs = boto3.client('efs')

# Create EFS for distributed data processing
def create_data_processing_efs(vpc_id, subnet_ids, performance_mode='maxIO'):
    """Create EFS optimized for distributed data processing workloads."""
    
    file_system = efs.create_file_system(
        PerformanceMode=performance_mode,
        ThroughputMode='provisioned',
        ProvisionedThroughputInMibps=500,
        Encrypted=True,
        Tags=[
            {'Key': 'Name', 'Value': 'DataProcessing-EFS'},
            {'Key': 'Purpose', 'Value': 'DistributedComputing'}
        ]
    )
    
    return file_system['FileSystemId']
```

## 3. Compute Services

### EC2 (Elastic Compute Cloud)
```python
# Launch data processing instance
ec2 = boto3.client('ec2')
response = ec2.run_instances(
    ImageId='ami-0c02fb55956c7d316',
    MinCount=1,
    MaxCount=1,
    InstanceType='r5.2xlarge',  # Memory optimized for data processing
    KeyName='data-key',
    SecurityGroupIds=['sg-12345678'],
    UserData='''#!/bin/bash
    yum update -y
    yum install -y python3 python3-pip
    pip3 install pandas numpy boto3
    '''
)
```

### Lambda (Serverless Computing)
```python
import json
import boto3

def lambda_handler(event, context):
    """Process S3 events for data pipeline"""
    s3 = boto3.client('s3')
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        # Trigger data processing
        if key.endswith('.csv'):
            process_csv_file(bucket, key)
    
    return {'statusCode': 200}
```

### ECS/Fargate (Container Services)
```yaml
# Task definition for data processing
{
  "family": "data-processor",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "2048",
  "memory": "4096",
  "containerDefinitions": [{
    "name": "processor",
    "image": "my-data-processor:latest",
    "environment": [
      {"name": "S3_BUCKET", "value": "data-lake"},
      {"name": "DB_HOST", "value": "rds-endpoint"}
    ]
  }]
}
```

## 4. Database Services

### RDS (Relational Database Service)
```python
rds = boto3.client('rds')

# Create PostgreSQL instance
rds.create_db_instance(
    DBInstanceIdentifier='data-warehouse',
    DBInstanceClass='db.r5.2xlarge',
    Engine='postgres',
    EngineVersion='13.7',
    AllocatedStorage=1000,
    StorageType='gp2',
    StorageEncrypted=True,
    MultiAZ=True,
    BackupRetentionPeriod=7
)
```

### DynamoDB (NoSQL Database)
```python
dynamodb = boto3.resource('dynamodb')

# Create table for real-time data
table = dynamodb.create_table(
    TableName='user-events',
    KeySchema=[
        {'AttributeName': 'user_id', 'KeyType': 'HASH'},
        {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
    ],
    AttributeDefinitions=[
        {'AttributeName': 'user_id', 'AttributeType': 'S'},
        {'AttributeName': 'timestamp', 'AttributeType': 'N'}
    ],
    BillingMode='PAY_PER_REQUEST'
)
```

### Redshift (Data Warehouse)
```python
redshift = boto3.client('redshift')

# Create cluster
redshift.create_cluster(
    ClusterIdentifier='data-warehouse',
    NodeType='dc2.large',
    NumberOfNodes=3,
    DBName='analytics',
    MasterUsername='admin',
    MasterUserPassword='SecurePassword123!'
)

# COPY command for bulk loading
copy_command = """
COPY sales_data FROM 's3://data-lake/processed/sales/'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftRole'
FORMAT AS PARQUET;
"""
```

## 5. Analytics and Big Data Services

### EMR (Elastic MapReduce)
```python
emr = boto3.client('emr')

# Create Spark cluster
cluster_id = emr.run_job_flow(
    Name='data-processing-cluster',
    ReleaseLabel='emr-6.15.0',
    Applications=[
        {'Name': 'Spark'},
        {'Name': 'Hadoop'},
        {'Name': 'Hive'}
    ],
    Instances={
        'MasterInstanceType': 'm5.xlarge',
        'SlaveInstanceType': 'm5.2xlarge',
        'InstanceCount': 4,
        'Ec2KeyName': 'emr-key'
    },
    ServiceRole='EMR_DefaultRole',
    JobFlowRole='EMR_EC2_DefaultRole'
)
```

### Glue (ETL Service)
```python
glue = boto3.client('glue')

# Create ETL job
glue.create_job(
    Name='sales-etl-job',
    Role='arn:aws:iam::123456789012:role/GlueRole',
    Command={
        'Name': 'glueetl',
        'ScriptLocation': 's3://scripts/etl_script.py'
    },
    DefaultArguments={
        '--job-language': 'python',
        '--source-bucket': 'raw-data',
        '--target-bucket': 'processed-data'
    }
)

# Glue ETL script example
script = """
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
    database="sales_db",
    table_name="raw_sales"
)

# Transform data
transformed = ApplyMapping.apply(
    frame=datasource,
    mappings=[
        ("customer_id", "string", "customer_id", "long"),
        ("amount", "string", "amount", "double"),
        ("date", "string", "order_date", "date")
    ]
)

# Write to S3
glueContext.write_dynamic_frame.from_options(
    frame=transformed,
    connection_type="s3",
    connection_options={"path": "s3://processed-data/sales/"},
    format="parquet"
)

job.commit()
"""
```

### Athena (Serverless Query Service)
```python
athena = boto3.client('athena')

# Create external table
create_table_query = """
CREATE EXTERNAL TABLE sales_data (
    customer_id bigint,
    product_id bigint,
    amount double,
    order_date date
)
PARTITIONED BY (year int, month int)
STORED AS PARQUET
LOCATION 's3://data-lake/sales/'
"""

# Execute query
response = athena.start_query_execution(
    QueryString=create_table_query,
    ResultConfiguration={
        'OutputLocation': 's3://athena-results/'
    },
    WorkGroup='primary'
)
```

## 6. Streaming and Real-time Services

### Kinesis Data Streams
```python
kinesis = boto3.client('kinesis')

# Create stream
kinesis.create_stream(
    StreamName='user-events',
    ShardCount=5
)

# Put record
kinesis.put_record(
    StreamName='user-events',
    Data=json.dumps({
        'user_id': '12345',
        'event_type': 'purchase',
        'timestamp': '2024-01-15T10:00:00Z'
    }),
    PartitionKey='12345'
)
```

### Kinesis Data Firehose
```python
firehose = boto3.client('firehose')

# Create delivery stream to S3
firehose.create_delivery_stream(
    DeliveryStreamName='events-to-s3',
    S3DestinationConfiguration={
        'RoleARN': 'arn:aws:iam::123456789012:role/FirehoseRole',
        'BucketARN': 'arn:aws:s3:::event-data',
        'Prefix': 'year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/',
        'BufferingHints': {
            'SizeInMBs': 128,
            'IntervalInSeconds': 60
        },
        'CompressionFormat': 'GZIP'
    }
)
```

### MSK (Managed Streaming for Kafka)
```python
kafka = boto3.client('kafka')

# Create Kafka cluster
kafka.create_cluster(
    BrokerNodeGroupInfo={
        'InstanceType': 'kafka.m5.large',
        'ClientSubnets': ['subnet-12345', 'subnet-67890'],
        'SecurityGroups': ['sg-kafka']
    },
    ClusterName='data-streaming-cluster',
    KafkaVersion='2.8.1',
    NumberOfBrokerNodes=3
)
```

## 7. Machine Learning Services

### SageMaker
```python
sagemaker = boto3.client('sagemaker')

# Create training job
sagemaker.create_training_job(
    TrainingJobName='customer-churn-model',
    AlgorithmSpecification={
        'TrainingImage': '382416733822.dkr.ecr.us-east-1.amazonaws.com/xgboost:latest',
        'TrainingInputMode': 'File'
    },
    RoleArn='arn:aws:iam::123456789012:role/SageMakerRole',
    InputDataConfig=[{
        'ChannelName': 'training',
        'DataSource': {
            'S3DataSource': {
                'S3DataType': 'S3Prefix',
                'S3Uri': 's3://ml-data/training/',
                'S3DataDistributionType': 'FullyReplicated'
            }
        }
    }],
    OutputDataConfig={
        'S3OutputPath': 's3://ml-models/output/'
    },
    ResourceConfig={
        'InstanceType': 'ml.m5.xlarge',
        'InstanceCount': 1,
        'VolumeSizeInGB': 30
    }
)
```

## 8. Orchestration and Workflow

### Step Functions
```json
{
  "Comment": "Data processing pipeline",
  "StartAt": "ExtractData",
  "States": {
    "ExtractData": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:extract-data",
      "Next": "TransformData"
    },
    "TransformData": {
      "Type": "Task",
      "Resource": "arn:aws:states:::glue:startJobRun.sync",
      "Parameters": {
        "JobName": "transform-job"
      },
      "Next": "LoadData"
    },
    "LoadData": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:load-data",
      "End": true
    }
  }
}
```

### EventBridge (CloudWatch Events)
```python
events = boto3.client('events')

# Create rule for S3 events
events.put_rule(
    Name='ProcessNewFiles',
    EventPattern=json.dumps({
        "source": ["aws.s3"],
        "detail-type": ["Object Created"],
        "detail": {
            "bucket": {"name": ["data-lake"]},
            "object": {"key": [{"prefix": "raw/"}]}
        }
    }),
    State='ENABLED'
)

# Add Lambda target
events.put_targets(
    Rule='ProcessNewFiles',
    Targets=[{
        'Id': '1',
        'Arn': 'arn:aws:lambda:us-east-1:123456789012:function:process-file'
    }]
)
```

## 9. Monitoring and Security

### CloudWatch
```python
cloudwatch = boto3.client('cloudwatch')

# Custom metric for data pipeline
cloudwatch.put_metric_data(
    Namespace='DataPipeline',
    MetricData=[{
        'MetricName': 'RecordsProcessed',
        'Value': 10000,
        'Unit': 'Count',
        'Dimensions': [
            {'Name': 'Pipeline', 'Value': 'sales-etl'},
            {'Name': 'Environment', 'Value': 'production'}
        ]
    }]
)

# Create alarm
cloudwatch.put_metric_alarm(
    AlarmName='HighErrorRate',
    ComparisonOperator='GreaterThanThreshold',
    EvaluationPeriods=2,
    MetricName='Errors',
    Namespace='AWS/Lambda',
    Period=300,
    Statistic='Sum',
    Threshold=10.0,
    ActionsEnabled=True,
    AlarmActions=['arn:aws:sns:us-east-1:123456789012:alerts']
)
```

### KMS (Key Management Service)
```python
kms = boto3.client('kms')

# Create encryption key
key = kms.create_key(
    Description='Data encryption key',
    Usage='ENCRYPT_DECRYPT',
    KeySpec='SYMMETRIC_DEFAULT'
)

# Encrypt data
encrypted = kms.encrypt(
    KeyId=key['KeyMetadata']['KeyId'],
    Plaintext=b'sensitive data'
)
```

## 10. Cost Optimization and Best Practices

### Resource Tagging Strategy
```python
# Consistent tagging for cost allocation
tags = [
    {'Key': 'Project', 'Value': 'DataPlatform'},
    {'Key': 'Environment', 'Value': 'Production'},
    {'Key': 'Owner', 'Value': 'DataEngineering'},
    {'Key': 'CostCenter', 'Value': 'Analytics'},
    {'Key': 'AutoShutdown', 'Value': 'true'}
]

# Apply to resources
ec2.create_tags(Resources=[instance_id], Tags=tags)
```

### Auto Scaling
```python
autoscaling = boto3.client('autoscaling')

# Create auto scaling group for EMR
autoscaling.create_auto_scaling_group(
    AutoScalingGroupName='emr-workers',
    MinSize=2,
    MaxSize=10,
    DesiredCapacity=4,
    DefaultCooldown=300,
    HealthCheckType='EC2',
    Tags=[{
        'Key': 'Name',
        'Value': 'EMR-Worker',
        'PropagateAtLaunch': True
    }]
)
```

### Spot Instances for Cost Savings
```python
# Use spot instances for batch processing
ec2.request_spot_instances(
    SpotPrice='0.10',
    InstanceCount=5,
    LaunchSpecification={
        'ImageId': 'ami-12345678',
        'InstanceType': 'm5.large',
        'KeyName': 'my-key',
        'SecurityGroups': ['batch-processing']
    }
)
```