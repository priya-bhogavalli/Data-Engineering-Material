# Cloud Quick Reference for Data Engineering

## AWS Services

### S3 (Simple Storage Service)
```bash
# AWS CLI commands
aws s3 ls s3://bucket-name/
aws s3 cp file.txt s3://bucket-name/
aws s3 sync ./local-folder s3://bucket-name/folder/
aws s3 rm s3://bucket-name/file.txt

# Python boto3
import boto3
s3 = boto3.client('s3')
s3.upload_file('local-file.txt', 'bucket-name', 'remote-file.txt')
s3.download_file('bucket-name', 'remote-file.txt', 'local-file.txt')
```

### EC2 (Elastic Compute Cloud)
```bash
# List instances
aws ec2 describe-instances

# Start/stop instances
aws ec2 start-instances --instance-ids i-1234567890abcdef0
aws ec2 stop-instances --instance-ids i-1234567890abcdef0

# Create instance
aws ec2 run-instances --image-id ami-12345678 --count 1 --instance-type t2.micro
```

### RDS (Relational Database Service)
```bash
# List DB instances
aws rds describe-db-instances

# Create DB instance
aws rds create-db-instance \
    --db-instance-identifier mydb \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username admin \
    --master-user-password mypassword
```

### Glue (ETL Service)
```python
# Glue job script
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

# Read from catalog
datasource0 = glueContext.create_dynamic_frame.from_catalog(
    database="my_database",
    table_name="my_table"
)

# Transform
applymapping1 = ApplyMapping.apply(
    frame=datasource0,
    mappings=[("col1", "string", "col1", "string")]
)

# Write to S3
glueContext.write_dynamic_frame.from_options(
    frame=applymapping1,
    connection_type="s3",
    connection_options={"path": "s3://my-bucket/output/"},
    format="parquet"
)

job.commit()
```

### Lambda (Serverless Functions)
```python
# Lambda function example
import json
import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    # Process S3 event
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        # Process file
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read()
        
        # Your processing logic here
        
    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete')
    }
```

## Azure Services

### Blob Storage
```bash
# Azure CLI
az storage blob list --container-name mycontainer --account-name mystorageaccount
az storage blob upload --file myfile.txt --container-name mycontainer --name myblob
az storage blob download --container-name mycontainer --name myblob --file downloaded.txt
```

```python
# Python SDK
from azure.storage.blob import BlobServiceClient

blob_service_client = BlobServiceClient(
    account_url="https://mystorageaccount.blob.core.windows.net",
    credential="account_key"
)

# Upload blob
with open("local-file.txt", "rb") as data:
    blob_service_client.get_blob_client(
        container="mycontainer", 
        blob="myblob"
    ).upload_blob(data)
```

### Azure Data Factory
```json
{
    "name": "CopyPipeline",
    "properties": {
        "activities": [
            {
                "name": "CopyFromBlobToSQL",
                "type": "Copy",
                "inputs": [
                    {
                        "referenceName": "BlobDataset",
                        "type": "DatasetReference"
                    }
                ],
                "outputs": [
                    {
                        "referenceName": "SQLDataset",
                        "type": "DatasetReference"
                    }
                ],
                "typeProperties": {
                    "source": {
                        "type": "BlobSource"
                    },
                    "sink": {
                        "type": "SqlSink"
                    }
                }
            }
        ]
    }
}
```

### Azure Databricks
```python
# Databricks notebook
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("DataProcessing").getOrCreate()

# Read from Azure Data Lake
df = spark.read.format("delta").load("/mnt/datalake/raw/data")

# Transform
transformed_df = df.filter(df.amount > 0).groupBy("category").sum("amount")

# Write to processed layer
transformed_df.write.format("delta").mode("overwrite").save("/mnt/datalake/processed/aggregated")
```

## Google Cloud Platform (GCP)

### Cloud Storage
```bash
# gsutil commands
gsutil ls gs://bucket-name/
gsutil cp file.txt gs://bucket-name/
gsutil rsync -r ./local-folder gs://bucket-name/folder/
gsutil rm gs://bucket-name/file.txt
```

```python
# Python client
from google.cloud import storage

client = storage.Client()
bucket = client.bucket('bucket-name')

# Upload file
blob = bucket.blob('remote-file.txt')
blob.upload_from_filename('local-file.txt')

# Download file
blob.download_to_filename('downloaded-file.txt')
```

### BigQuery
```sql
-- BigQuery SQL
SELECT 
    customer_id,
    SUM(amount) as total_amount,
    COUNT(*) as order_count
FROM `project.dataset.orders`
WHERE order_date >= '2024-01-01'
GROUP BY customer_id
ORDER BY total_amount DESC;
```

```python
# Python client
from google.cloud import bigquery

client = bigquery.Client()

query = """
    SELECT customer_id, SUM(amount) as total
    FROM `project.dataset.orders`
    GROUP BY customer_id
"""

query_job = client.query(query)
results = query_job.result()

for row in results:
    print(f"Customer: {row.customer_id}, Total: {row.total}")
```

### Dataflow (Apache Beam)
```python
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

def run_pipeline():
    pipeline_options = PipelineOptions([
        '--project=my-project',
        '--region=us-central1',
        '--runner=DataflowRunner',
        '--temp_location=gs://my-bucket/temp'
    ])
    
    with beam.Pipeline(options=pipeline_options) as pipeline:
        (pipeline
         | 'Read from BigQuery' >> beam.io.ReadFromBigQuery(
             query='SELECT * FROM `project.dataset.table`')
         | 'Transform' >> beam.Map(lambda x: transform_function(x))
         | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
             'project:dataset.output_table'))
```

## Common Patterns

### Data Pipeline Orchestration
```python
# Apache Airflow DAG
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'data_pipeline',
    default_args=default_args,
    description='Daily data processing pipeline',
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    catchup=False
)

def extract_data():
    # Extraction logic
    pass

def transform_data():
    # Transformation logic
    pass

def load_data():
    # Loading logic
    pass

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag
)

extract_task >> transform_task >> load_task
```

### Infrastructure as Code
```yaml
# CloudFormation template
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Data Lake Infrastructure'

Resources:
  DataLakeBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${AWS::StackName}-data-lake'
      VersioningConfiguration:
        Status: Enabled
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256

  GlueDatabase:
    Type: AWS::Glue::Database
    Properties:
      CatalogId: !Ref AWS::AccountId
      DatabaseInput:
        Name: !Sub '${AWS::StackName}_database'
        Description: 'Data lake database'

  GlueRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: glue.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole
```

### Monitoring and Alerting
```python
# CloudWatch custom metrics
import boto3
from datetime import datetime

def send_custom_metric(metric_name, value, unit='Count'):
    cloudwatch = boto3.client('cloudwatch')
    
    cloudwatch.put_metric_data(
        Namespace='DataPipeline',
        MetricData=[
            {
                'MetricName': metric_name,
                'Value': value,
                'Unit': unit,
                'Timestamp': datetime.utcnow()
            }
        ]
    )

# Usage
send_custom_metric('RecordsProcessed', 1000)
send_custom_metric('ProcessingTime', 45.2, 'Seconds')
```

### Error Handling and Retry Logic
```python
import time
import random
from functools import wraps

def retry_with_backoff(max_retries=3, base_delay=1, max_delay=60):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    
                    delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.2f}s")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3)
def upload_to_s3(file_path, bucket, key):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket, key)
```

### Data Quality Checks
```python
def validate_data_quality(df):
    """Perform data quality checks."""
    
    quality_checks = {
        'row_count': len(df),
        'null_percentage': df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100,
        'duplicate_count': df.duplicated().sum(),
        'schema_validation': validate_schema(df)
    }
    
    # Alert if quality thresholds are breached
    if quality_checks['null_percentage'] > 10:
        send_alert("High null percentage detected")
    
    if quality_checks['duplicate_count'] > 100:
        send_alert("High duplicate count detected")
    
    return quality_checks

def send_alert(message):
    # Send to SNS, Slack, or email
    sns = boto3.client('sns')
    sns.publish(
        TopicArn='arn:aws:sns:us-east-1:123456789012:data-quality-alerts',
        Message=message,
        Subject='Data Quality Alert'
    )
```

This quick reference provides essential commands and patterns for working with major cloud platforms in data engineering contexts.