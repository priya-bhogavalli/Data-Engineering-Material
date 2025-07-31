# AWS Comprehensive Key Concepts for Data Engineering

## 1. AWS Core Services Overview
**AWS Global Infrastructure**:
- **Regions**: Geographic areas with multiple Availability Zones
- **Availability Zones**: Isolated data centers within regions
- **Edge Locations**: CDN endpoints for CloudFront

**Identity and Access Management (IAM)**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"AWS": "arn:aws:iam::123456789012:user/DataEngineer"},
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::data-lake/*"
    }
  ]
}
```

## 2. Storage Services

### S3 (Simple Storage Service)
```python
import boto3

s3 = boto3.client('s3')

# Data lake structure
s3.put_object(
    Bucket='data-lake',
    Key='raw/year=2024/month=01/day=15/data.parquet',
    Body=data,
    StorageClass='STANDARD_IA'
)

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
```python
# High-performance storage for databases
ec2 = boto3.client('ec2')
ec2.create_volume(
    Size=1000,
    VolumeType='gp3',
    Iops=3000,
    Throughput=125
)
```

### EFS (Elastic File System)
```python
# Shared file system for distributed processing
efs = boto3.client('efs')
efs.create_file_system(
    PerformanceMode='generalPurpose',
    ThroughputMode='provisioned',
    ProvisionedThroughputInMibps=500
)
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