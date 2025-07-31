# AWS Services Quick Reference for Data Engineers

## Storage Services

### Amazon S3 (Simple Storage Service)
**Use Case**: Data lake, backup, static websites, content distribution
```bash
# CLI Commands
aws s3 cp file.csv s3://bucket/path/
aws s3 sync ./data/ s3://bucket/data/
aws s3 ls s3://bucket/ --recursive
aws s3 rm s3://bucket/file.csv
```

### Amazon EBS (Elastic Block Store)
**Use Case**: Persistent block storage for EC2 instances
```bash
# Create volume
aws ec2 create-volume --size 100 --volume-type gp3 --availability-zone us-east-1a
# Attach volume
aws ec2 attach-volume --volume-id vol-12345 --instance-id i-12345 --device /dev/sdf
```

### Amazon EFS (Elastic File System)
**Use Case**: Shared file system for multiple EC2 instances
```bash
# Create file system
aws efs create-file-system --creation-token mytoken
# Create mount target
aws efs create-mount-target --file-system-id fs-12345 --subnet-id subnet-12345
```

## Compute Services

### Amazon EC2 (Elastic Compute Cloud)
**Use Case**: Virtual servers for custom applications
```bash
# Launch instance
aws ec2 run-instances --image-id ami-12345 --count 1 --instance-type t3.medium
# Stop instance
aws ec2 stop-instances --instance-ids i-12345
# Terminate instance
aws ec2 terminate-instances --instance-ids i-12345
```

### AWS Lambda
**Use Case**: Serverless compute for event-driven processing
```python
# Basic Lambda function
import json
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
```

### Amazon EMR (Elastic MapReduce)
**Use Case**: Managed Hadoop/Spark clusters
```bash
# Create cluster
aws emr create-cluster --name "MyCluster" --release-label emr-6.4.0 \
  --applications Name=Spark Name=Hadoop \
  --instance-type m5.xlarge --instance-count 3
```

### AWS Batch
**Use Case**: Managed batch computing
```bash
# Submit job
aws batch submit-job --job-name myjob --job-queue myqueue \
  --job-definition myjobdef
```

## Database Services

### Amazon RDS (Relational Database Service)
**Use Case**: Managed relational databases (MySQL, PostgreSQL, Oracle, SQL Server)
```bash
# Create DB instance
aws rds create-db-instance --db-instance-identifier mydb \
  --db-instance-class db.t3.micro --engine mysql \
  --master-username admin --master-user-password password
```

### Amazon DynamoDB
**Use Case**: NoSQL database for high-performance applications
```python
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MyTable')
table.put_item(Item={'id': '123', 'name': 'John'})
```

### Amazon Redshift
**Use Case**: Data warehouse for analytics
```sql
-- Create table
CREATE TABLE sales (
    id INT,
    amount DECIMAL(10,2),
    date DATE
);
-- Copy data from S3
COPY sales FROM 's3://bucket/data/' IAM_ROLE 'arn:aws:iam::account:role/RedshiftRole';
```

### Amazon DocumentDB
**Use Case**: MongoDB-compatible document database
```javascript
// Connect to DocumentDB
const MongoClient = require('mongodb').MongoClient;
const client = new MongoClient('mongodb://username:password@docdb-cluster.cluster-xyz.us-east-1.docdb.amazonaws.com:27017');
```

## Analytics Services

### Amazon Athena
**Use Case**: Serverless SQL queries on S3 data
```sql
-- Create external table
CREATE EXTERNAL TABLE sales (
    id int,
    amount double,
    date string
)
STORED AS PARQUET
LOCATION 's3://bucket/sales-data/';

-- Query data
SELECT date, SUM(amount) as total_sales
FROM sales
WHERE date >= '2024-01-01'
GROUP BY date;
```

### AWS Glue
**Use Case**: ETL service and data catalog
```python
# Glue ETL script
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)

# Read from catalog
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="mydb", table_name="mytable"
)

# Transform data
mapped_data = ApplyMapping.apply(
    frame=datasource,
    mappings=[("old_name", "string", "new_name", "string")]
)

# Write to S3
glueContext.write_dynamic_frame.from_options(
    frame=mapped_data,
    connection_type="s3",
    connection_options={"path": "s3://bucket/output/"},
    format="parquet"
)
```

### Amazon Kinesis
**Use Case**: Real-time data streaming
```python
# Kinesis producer
import boto3
kinesis = boto3.client('kinesis')
kinesis.put_record(
    StreamName='mystream',
    Data='{"event": "user_click"}',
    PartitionKey='user123'
)

# Kinesis consumer
response = kinesis.get_records(ShardIterator=shard_iterator)
for record in response['Records']:
    data = record['Data']
    # Process data
```

### Amazon QuickSight
**Use Case**: Business intelligence and visualization
```python
# Create QuickSight dataset
import boto3
quicksight = boto3.client('quicksight')

quicksight.create_data_set(
    AwsAccountId='123456789012',
    DataSetId='mydataset',
    Name='My Dataset',
    PhysicalTableMap={
        'table1': {
            'S3Source': {
                'DataSourceArn': 'arn:aws:quicksight:region:account:datasource/datasource-id',
                'InputColumns': [
                    {'Name': 'column1', 'Type': 'STRING'},
                    {'Name': 'column2', 'Type': 'INTEGER'}
                ]
            }
        }
    }
)
```

## Machine Learning Services

### Amazon SageMaker
**Use Case**: Machine learning platform
```python
import sagemaker
from sagemaker.sklearn.estimator import SKLearn

# Create estimator
sklearn_estimator = SKLearn(
    entry_point='train.py',
    framework_version='0.23-1',
    instance_type='ml.m5.large',
    role='arn:aws:iam::account:role/SageMakerRole'
)

# Train model
sklearn_estimator.fit({'train': 's3://bucket/train-data/'})

# Deploy model
predictor = sklearn_estimator.deploy(
    initial_instance_count=1,
    instance_type='ml.t2.medium'
)
```

### Amazon Comprehend
**Use Case**: Natural language processing
```python
import boto3
comprehend = boto3.client('comprehend')

# Detect sentiment
response = comprehend.detect_sentiment(
    Text='I love this product!',
    LanguageCode='en'
)
print(response['Sentiment'])  # POSITIVE
```

### Amazon Rekognition
**Use Case**: Image and video analysis
```python
import boto3
rekognition = boto3.client('rekognition')

# Detect labels in image
response = rekognition.detect_labels(
    Image={'S3Object': {'Bucket': 'mybucket', 'Name': 'image.jpg'}},
    MaxLabels=10
)
```

## Security Services

### AWS IAM (Identity and Access Management)
**Use Case**: Access control and permissions
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["s3:GetObject", "s3:PutObject"],
            "Resource": "arn:aws:s3:::mybucket/*"
        }
    ]
}
```

### AWS KMS (Key Management Service)
**Use Case**: Encryption key management
```python
import boto3
kms = boto3.client('kms')

# Create key
key = kms.create_key(Description='Data encryption key')

# Encrypt data
encrypted = kms.encrypt(
    KeyId=key['KeyMetadata']['KeyId'],
    Plaintext=b'sensitive data'
)
```

### AWS Secrets Manager
**Use Case**: Store and manage secrets
```python
import boto3
secrets = boto3.client('secretsmanager')

# Store secret
secrets.create_secret(
    Name='database-credentials',
    SecretString='{"username":"admin","password":"secret123"}'
)

# Retrieve secret
response = secrets.get_secret_value(SecretId='database-credentials')
secret = response['SecretString']
```

## Monitoring Services

### Amazon CloudWatch
**Use Case**: Monitoring and logging
```python
import boto3
cloudwatch = boto3.client('cloudwatch')

# Put custom metric
cloudwatch.put_metric_data(
    Namespace='MyApp',
    MetricData=[
        {
            'MetricName': 'ProcessingTime',
            'Value': 123.45,
            'Unit': 'Seconds'
        }
    ]
)

# Create alarm
cloudwatch.put_metric_alarm(
    AlarmName='HighCPU',
    ComparisonOperator='GreaterThanThreshold',
    EvaluationPeriods=2,
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Period=300,
    Statistic='Average',
    Threshold=80.0
)
```

### AWS X-Ray
**Use Case**: Distributed tracing
```python
from aws_xray_sdk.core import xray_recorder

@xray_recorder.capture('process_data')
def process_data():
    # Your code here
    pass
```

### AWS CloudTrail
**Use Case**: API call logging and auditing
```bash
# Create trail
aws cloudtrail create-trail --name mytrail --s3-bucket-name mybucket
# Start logging
aws cloudtrail start-logging --name mytrail
```

## Networking Services

### Amazon VPC (Virtual Private Cloud)
**Use Case**: Isolated network environment
```bash
# Create VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16
# Create subnet
aws ec2 create-subnet --vpc-id vpc-12345 --cidr-block 10.0.1.0/24
# Create internet gateway
aws ec2 create-internet-gateway
```

### AWS Direct Connect
**Use Case**: Dedicated network connection to AWS
```bash
# Create virtual interface
aws directconnect create-private-virtual-interface \
  --connection-id dxcon-12345 \
  --new-private-virtual-interface vlan=100,bgpAsn=65000,virtualInterfaceName=MyVIF
```

## Management Services

### AWS CloudFormation
**Use Case**: Infrastructure as code
```yaml
# CloudFormation template
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  MyBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-data-bucket
  MyTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: MyTable
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
      KeySchema:
        - AttributeName: id
          KeyType: HASH
```

### AWS Systems Manager
**Use Case**: Operational insights and automation
```bash
# Run command on instances
aws ssm send-command --document-name "AWS-RunShellScript" \
  --parameters 'commands=["echo hello"]' \
  --targets "Key=tag:Environment,Values=Production"
```

### AWS Config
**Use Case**: Configuration compliance monitoring
```bash
# Put configuration recorder
aws configservice put-configuration-recorder \
  --configuration-recorder name=default,roleARN=arn:aws:iam::account:role/ConfigRole
```

## Cost Management

### AWS Cost Explorer
**Use Case**: Cost analysis and optimization
```python
import boto3
ce = boto3.client('ce')

# Get cost and usage
response = ce.get_cost_and_usage(
    TimePeriod={
        'Start': '2024-01-01',
        'End': '2024-01-31'
    },
    Granularity='MONTHLY',
    Metrics=['BlendedCost']
)
```

### AWS Budgets
**Use Case**: Cost budgets and alerts
```python
import boto3
budgets = boto3.client('budgets')

# Create budget
budgets.create_budget(
    AccountId='123456789012',
    Budget={
        'BudgetName': 'DataEngineering',
        'BudgetLimit': {
            'Amount': '1000',
            'Unit': 'USD'
        },
        'TimeUnit': 'MONTHLY',
        'BudgetType': 'COST'
    }
)
```

## Common CLI Commands

### S3 Operations
```bash
# Sync directories
aws s3 sync ./local-folder s3://bucket/folder/

# Copy with metadata
aws s3 cp file.txt s3://bucket/ --metadata key1=value1,key2=value2

# List objects with details
aws s3api list-objects-v2 --bucket mybucket --query 'Contents[?Size > `1000000`]'
```

### EC2 Operations
```bash
# Describe instances
aws ec2 describe-instances --query 'Reservations[].Instances[?State.Name==`running`].[InstanceId,InstanceType,PublicIpAddress]'

# Create AMI
aws ec2 create-image --instance-id i-12345 --name "MyAMI" --description "My custom AMI"

# Modify instance attribute
aws ec2 modify-instance-attribute --instance-id i-12345 --instance-type Value=t3.large
```

### RDS Operations
```bash
# Create snapshot
aws rds create-db-snapshot --db-instance-identifier mydb --db-snapshot-identifier mydb-snapshot

# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot --db-instance-identifier restored-db --db-snapshot-identifier mydb-snapshot
```

### Lambda Operations
```bash
# Create function
aws lambda create-function --function-name myfunction --runtime python3.9 --role arn:aws:iam::account:role/LambdaRole --handler lambda_function.lambda_handler --zip-file fileb://function.zip

# Invoke function
aws lambda invoke --function-name myfunction --payload '{"key":"value"}' response.json
```

## Best Practices Quick Tips

### Security
- Use IAM roles instead of access keys
- Enable MFA for root account
- Encrypt data at rest and in transit
- Use VPC for network isolation
- Regular security audits with AWS Config

### Cost Optimization
- Use Reserved Instances for predictable workloads
- Implement lifecycle policies for S3
- Monitor with CloudWatch and set up billing alerts
- Use Spot Instances for fault-tolerant workloads
- Regular cost reviews with Cost Explorer

### Performance
- Use CloudFront for content delivery
- Implement caching strategies
- Choose appropriate instance types
- Use Auto Scaling for variable workloads
- Monitor performance with CloudWatch

### Reliability
- Design for failure with multi-AZ deployments
- Implement backup and disaster recovery
- Use health checks and auto-recovery
- Monitor with CloudWatch alarms
- Test disaster recovery procedures

This quick reference provides essential commands and code snippets for the most commonly used AWS services in data engineering workflows.