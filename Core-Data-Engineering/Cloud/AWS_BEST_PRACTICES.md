# AWS Best Practices for Data Engineering

## S3 Optimization

### Bucket Configuration
```bash
# Create bucket with versioning and encryption
aws s3api create-bucket --bucket data-lake-prod --region us-east-1
aws s3api put-bucket-versioning --bucket data-lake-prod --versioning-configuration Status=Enabled
aws s3api put-bucket-encryption --bucket data-lake-prod --server-side-encryption-configuration '{
  "Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]
}'
```

### Data Partitioning
```python
import boto3
from datetime import datetime

def upload_partitioned_data(data, bucket, prefix):
    s3 = boto3.client('s3')
    today = datetime.now()
    
    # Partition by year/month/day
    key = f"{prefix}/year={today.year}/month={today.month:02d}/day={today.day:02d}/data.parquet"
    
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=data,
        StorageClass='STANDARD_IA'  # Cost optimization
    )
```

### Lifecycle Management
```json
{
  "Rules": [
    {
      "ID": "DataLakeLifecycle",
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        },
        {
          "Days": 365,
          "StorageClass": "DEEP_ARCHIVE"
        }
      ]
    }
  ]
}
```

## Glue ETL Optimization

### Job Configuration
```python
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

# Optimize Spark configuration
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")

# Read from catalog
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="data_lake",
    table_name="raw_events",
    transformation_ctx="datasource"
)

# Apply transformations
transformed = ApplyMapping.apply(
    frame=datasource,
    mappings=[
        ("event_id", "string", "event_id", "string"),
        ("timestamp", "string", "event_timestamp", "timestamp"),
        ("user_id", "string", "user_id", "string")
    ]
)

# Write to S3 with partitioning
glueContext.write_dynamic_frame.from_options(
    frame=transformed,
    connection_type="s3",
    connection_options={
        "path": "s3://data-lake-prod/processed/events/",
        "partitionKeys": ["year", "month", "day"]
    },
    format="parquet"
)

job.commit()
```

## Redshift Optimization

### Table Design
```sql
-- Fact table with distribution and sort keys
CREATE TABLE sales_fact (
    sale_id BIGINT IDENTITY(1,1),
    customer_id INT,
    product_id INT,
    sale_date DATE,
    amount DECIMAL(10,2)
)
DISTKEY(customer_id)
SORTKEY(sale_date);

-- Dimension table with ALL distribution
CREATE TABLE customer_dim (
    customer_id INT,
    customer_name VARCHAR(100),
    region VARCHAR(50)
)
DISTSTYLE ALL;
```

### COPY Command Optimization
```sql
-- Efficient bulk loading
COPY sales_fact
FROM 's3://data-lake-prod/sales/'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftRole'
FORMAT AS PARQUET
COMPUPDATE ON
STATUPDATE ON;

-- Parallel loading with manifest
COPY sales_fact
FROM 's3://data-lake-prod/manifest.json'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftRole'
MANIFEST
COMPUPDATE ON;
```

## Lambda for Data Processing

### Event-Driven Processing
```python
import json
import boto3
import pandas as pd
from io import StringIO

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    # Process S3 event
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        # Read CSV from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        df = pd.read_csv(StringIO(response['Body'].read().decode('utf-8')))
        
        # Transform data
        df['processed_date'] = pd.Timestamp.now()
        df = df.dropna()
        
        # Write back to S3
        output_key = key.replace('raw/', 'processed/')
        s3.put_object(
            Bucket=bucket,
            Key=output_key,
            Body=df.to_csv(index=False)
        )
    
    return {'statusCode': 200}
```

## IAM Security

### Least Privilege Policies
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
      "Resource": "arn:aws:s3:::data-lake-prod/processed/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "glue:GetTable",
        "glue:GetPartitions"
      ],
      "Resource": "*"
    }
  ]
}
```

### Cross-Account Access
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::ACCOUNT-B:role/DataProcessingRole"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::shared-data-bucket/*"
    }
  ]
}
```