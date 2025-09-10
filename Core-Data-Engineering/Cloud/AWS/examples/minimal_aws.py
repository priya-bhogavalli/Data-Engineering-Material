"""
Minimal AWS Examples with Outputs
Essential AWS operations for data engineering
"""

import boto3
import json
from datetime import datetime

# 1. S3 Operations
s3 = boto3.client('s3')

# List buckets
response = s3.list_buckets()
print(f"Found {len(response['Buckets'])} buckets")
# Output: Found 3 buckets

# Upload file
s3.upload_file('local_file.txt', 'my-bucket', 'data/file.txt')
print("File uploaded to S3")
# Output: File uploaded to S3

# Download file
s3.download_file('my-bucket', 'data/file.txt', 'downloaded_file.txt')
print("File downloaded from S3")
# Output: File downloaded from S3

# 2. DynamoDB Operations
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

# Put item
table.put_item(Item={'id': '123', 'name': 'Alice', 'age': 25})
print("Item added to DynamoDB")
# Output: Item added to DynamoDB

# Get item
response = table.get_item(Key={'id': '123'})
print(f"Retrieved: {response['Item']['name']}")
# Output: Retrieved: Alice

# 3. Lambda Function
lambda_client = boto3.client('lambda')

# Invoke function
response = lambda_client.invoke(
    FunctionName='my-function',
    Payload=json.dumps({'key': 'value'})
)
result = json.loads(response['Payload'].read())
print(f"Lambda result: {result}")
# Output: Lambda result: {'statusCode': 200, 'body': 'Success'}

# 4. SQS Operations
sqs = boto3.client('sqs')

# Send message
sqs.send_message(
    QueueUrl='https://sqs.us-east-1.amazonaws.com/123456789/my-queue',
    MessageBody='Hello from SQS'
)
print("Message sent to SQS")
# Output: Message sent to SQS

# Receive message
response = sqs.receive_message(
    QueueUrl='https://sqs.us-east-1.amazonaws.com/123456789/my-queue'
)
if 'Messages' in response:
    print(f"Received: {response['Messages'][0]['Body']}")
# Output: Received: Hello from SQS

# 5. RDS Operations
rds = boto3.client('rds')

# List databases
response = rds.describe_db_instances()
print(f"Found {len(response['DBInstances'])} RDS instances")
# Output: Found 2 RDS instances

# 6. Glue Operations
glue = boto3.client('glue')

# Start crawler
glue.start_crawler(Name='my-crawler')
print("Glue crawler started")
# Output: Glue crawler started

# Get crawler status
response = glue.get_crawler(Name='my-crawler')
print(f"Crawler state: {response['Crawler']['State']}")
# Output: Crawler state: RUNNING

# 7. Athena Operations
athena = boto3.client('athena')

# Execute query
response = athena.start_query_execution(
    QueryString='SELECT COUNT(*) FROM my_table',
    ResultConfiguration={'OutputLocation': 's3://my-bucket/results/'}
)
query_id = response['QueryExecutionId']
print(f"Query started: {query_id}")
# Output: Query started: 12345678-1234-1234-1234-123456789012

# 8. Redshift Operations
redshift = boto3.client('redshift')

# List clusters
response = redshift.describe_clusters()
print(f"Found {len(response['Clusters'])} Redshift clusters")
# Output: Found 1 Redshift clusters

# 9. Kinesis Operations
kinesis = boto3.client('kinesis')

# Put record
kinesis.put_record(
    StreamName='my-stream',
    Data=json.dumps({'timestamp': str(datetime.now()), 'value': 42}),
    PartitionKey='partition-1'
)
print("Record sent to Kinesis")
# Output: Record sent to Kinesis

# 10. CloudWatch Logs
logs = boto3.client('logs')

# Create log group
logs.create_log_group(logGroupName='/aws/lambda/my-function')
print("Log group created")
# Output: Log group created

# Put log events
logs.put_log_events(
    logGroupName='/aws/lambda/my-function',
    logStreamName='stream-1',
    logEvents=[
        {
            'timestamp': int(datetime.now().timestamp() * 1000),
            'message': 'Application started'
        }
    ]
)
print("Log event sent")
# Output: Log event sent

# 11. IAM Operations
iam = boto3.client('iam')

# List users
response = iam.list_users()
print(f"Found {len(response['Users'])} IAM users")
# Output: Found 5 IAM users

# 12. EC2 Operations
ec2 = boto3.client('ec2')

# List instances
response = ec2.describe_instances()
instance_count = sum(len(r['Instances']) for r in response['Reservations'])
print(f"Found {instance_count} EC2 instances")
# Output: Found 3 EC2 instances

# 13. SNS Operations
sns = boto3.client('sns')

# Publish message
sns.publish(
    TopicArn='arn:aws:sns:us-east-1:123456789:my-topic',
    Message='Hello from SNS',
    Subject='Test Message'
)
print("Message published to SNS")
# Output: Message published to SNS

# 14. Step Functions
stepfunctions = boto3.client('stepfunctions')

# Start execution
response = stepfunctions.start_execution(
    stateMachineArn='arn:aws:states:us-east-1:123456789:stateMachine:MyStateMachine',
    input=json.dumps({'key': 'value'})
)
print(f"Execution started: {response['executionArn']}")
# Output: Execution started: arn:aws:states:us-east-1:123456789:execution:MyStateMachine:12345

# 15. Error Handling
try:
    s3.head_object(Bucket='nonexistent-bucket', Key='file.txt')
except Exception as e:
    print(f"Error handled: {e.__class__.__name__}")
# Output: Error handled: NoSuchBucket