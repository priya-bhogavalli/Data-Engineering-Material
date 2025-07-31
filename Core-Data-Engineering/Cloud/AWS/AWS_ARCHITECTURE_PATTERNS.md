# AWS Architecture Patterns for Data Engineering

## 1. Data Lake Architecture

### Basic Data Lake Pattern
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │───▶│   Amazon S3     │───▶│   Analytics     │
│ • Databases     │    │   Data Lake     │    │ • Athena        │
│ • APIs          │    │ • Raw           │    │ • QuickSight    │
│ • Files         │    │ • Processed     │    │ • EMR           │
│ • Streams       │    │ • Curated       │    │ • Redshift      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Implementation**:
```python
# S3 bucket structure for data lake
data_lake_structure = {
    "raw/": {
        "description": "Ingested data in original format",
        "retention": "7 years",
        "storage_class": "Standard → IA → Glacier"
    },
    "processed/": {
        "description": "Cleaned and transformed data",
        "retention": "3 years", 
        "storage_class": "Standard → IA"
    },
    "curated/": {
        "description": "Business-ready datasets",
        "retention": "1 year",
        "storage_class": "Standard"
    }
}

# CloudFormation template for data lake
data_lake_template = {
    "AWSTemplateFormatVersion": "2010-09-09",
    "Resources": {
        "DataLakeBucket": {
            "Type": "AWS::S3::Bucket",
            "Properties": {
                "BucketName": {"Fn::Sub": "data-lake-${AWS::AccountId}-${AWS::Region}"},
                "VersioningConfiguration": {"Status": "Enabled"},
                "LifecycleConfiguration": {
                    "Rules": [
                        {
                            "Id": "DataLakeLifecycle",
                            "Status": "Enabled",
                            "Transitions": [
                                {"Days": 30, "StorageClass": "STANDARD_IA"},
                                {"Days": 90, "StorageClass": "GLACIER"},
                                {"Days": 365, "StorageClass": "DEEP_ARCHIVE"}
                            ]
                        }
                    ]
                }
            }
        }
    }
}
```

### Advanced Data Lake with Lake Formation
```python
# Lake Formation setup
import boto3

lakeformation = boto3.client('lakeformation')

# Register S3 location
lakeformation.register_resource(
    ResourceArn='arn:aws:s3:::data-lake-bucket',
    UseServiceLinkedRole=True
)

# Grant permissions
lakeformation.grant_permissions(
    Principal={'DataLakePrincipalIdentifier': 'arn:aws:iam::account:role/DataAnalyst'},
    Resource={
        'Table': {
            'DatabaseName': 'sales_db',
            'Name': 'transactions'
        }
    },
    Permissions=['SELECT', 'DESCRIBE']
)
```

## 2. Real-Time Streaming Architecture

### Kinesis-Based Streaming Pattern
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Data Sources   │───▶│  Kinesis Data   │───▶│  Kinesis Data   │───▶│  Destinations   │
│ • Applications  │    │    Streams      │    │   Analytics     │    │ • S3            │
│ • IoT Devices   │    │ • Sharding      │    │ • SQL Queries   │    │ • Redshift      │
│ • Log Files     │    │ • Retention     │    │ • Windowing     │    │ • Elasticsearch │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Implementation**:
```python
# Kinesis Data Streams setup
kinesis = boto3.client('kinesis')

# Create stream
stream_config = {
    'StreamName': 'real-time-events',
    'ShardCount': 5,
    'StreamModeDetails': {
        'StreamMode': 'PROVISIONED'
    }
}

# Kinesis Analytics application
analytics_app = {
    'ApplicationName': 'real-time-analytics',
    'ApplicationDescription': 'Real-time event processing',
    'RuntimeEnvironment': 'SQL-1_0',
    'ServiceExecutionRole': 'arn:aws:iam::account:role/KinesisAnalyticsRole',
    'ApplicationConfiguration': {
        'SqlApplicationConfiguration': {
            'Inputs': [{
                'NamePrefix': 'SOURCE_SQL_STREAM',
                'KinesisStreamsInput': {
                    'ResourceARN': 'arn:aws:kinesis:region:account:stream/real-time-events'
                },
                'InputSchema': {
                    'RecordColumns': [
                        {'Name': 'event_time', 'SqlType': 'TIMESTAMP'},
                        {'Name': 'user_id', 'SqlType': 'VARCHAR(32)'},
                        {'Name': 'event_type', 'SqlType': 'VARCHAR(64)'},
                        {'Name': 'value', 'SqlType': 'DOUBLE'}
                    ]
                }
            }]
        }
    }
}

# Real-time SQL query
real_time_query = """
CREATE OR REPLACE STREAM "DESTINATION_SQL_STREAM" (
    user_id VARCHAR(32),
    event_count INTEGER,
    avg_value DOUBLE,
    window_start TIMESTAMP,
    window_end TIMESTAMP
);

CREATE OR REPLACE PUMP "STREAM_PUMP" AS INSERT INTO "DESTINATION_SQL_STREAM"
SELECT STREAM 
    user_id,
    COUNT(*) as event_count,
    AVG(value) as avg_value,
    ROWTIME_TO_TIMESTAMP(MIN(ROWTIME)) as window_start,
    ROWTIME_TO_TIMESTAMP(MAX(ROWTIME)) as window_end
FROM SOURCE_SQL_STREAM_001
GROUP BY user_id, 
         RANGE_INTERVAL '5' MINUTE;
"""
```

### Lambda-Based Event Processing
```python
# Lambda function for stream processing
import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('processed_events')
    
    processed_records = []
    
    for record in event['Records']:
        # Decode Kinesis data
        payload = json.loads(
            base64.b64decode(record['kinesis']['data']).decode('utf-8')
        )
        
        # Process the event
        processed_event = {
            'event_id': str(uuid.uuid4()),
            'user_id': payload['user_id'],
            'event_type': payload['event_type'],
            'processed_at': datetime.utcnow().isoformat(),
            'original_timestamp': payload['timestamp'],
            'enriched_data': enrich_event(payload)
        }
        
        # Store in DynamoDB
        table.put_item(Item=processed_event)
        processed_records.append(processed_event)
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Processed {len(processed_records)} records')
    }

def enrich_event(payload):
    # Add business logic for event enrichment
    return {
        'category': categorize_event(payload['event_type']),
        'priority': calculate_priority(payload),
        'metadata': extract_metadata(payload)
    }
```

## 3. Batch Processing Architecture

### EMR-Based Big Data Processing
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │───▶│   Amazon S3     │───▶│   Amazon EMR    │───▶│  Data Warehouse │
│ • HDFS          │    │ • Staging Area  │    │ • Spark Jobs    │    │ • Redshift      │
│ • Databases     │    │ • Raw Data      │    │ • Hive Queries  │    │ • RDS           │
│ • Files         │    │ • Partitioned   │    │ • Scala/Python  │    │ • S3 (Parquet)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Implementation**:
```python
# EMR cluster configuration
emr_config = {
    'Name': 'DataProcessing-Cluster',
    'ReleaseLabel': 'emr-6.4.0',
    'Instances': {
        'MasterInstanceType': 'm5.xlarge',
        'SlaveInstanceType': 'm5.large',
        'InstanceCount': 10,
        'Ec2KeyName': 'my-key-pair',
        'Ec2SubnetId': 'subnet-12345678',
        'EmrManagedMasterSecurityGroup': 'sg-master',
        'EmrManagedSlaveSecurityGroup': 'sg-slave'
    },
    'Applications': [
        {'Name': 'Spark'},
        {'Name': 'Hadoop'},
        {'Name': 'Hive'},
        {'Name': 'Livy'}
    ],
    'Configurations': [
        {
            'Classification': 'spark-defaults',
            'Properties': {
                'spark.sql.adaptive.enabled': 'true',
                'spark.sql.adaptive.coalescePartitions.enabled': 'true',
                'spark.dynamicAllocation.enabled': 'true',
                'spark.dynamicAllocation.minExecutors': '1',
                'spark.dynamicAllocation.maxExecutors': '20'
            }
        }
    ],
    'ServiceRole': 'EMR_DefaultRole',
    'JobFlowRole': 'EMR_EC2_DefaultRole',
    'LogUri': 's3://emr-logs-bucket/',
    'BootstrapActions': [
        {
            'Name': 'Install Additional Libraries',
            'ScriptBootstrapAction': {
                'Path': 's3://bootstrap-scripts/install-libs.sh'
            }
        }
    ]
}

# Spark job submission
spark_step = {
    'Name': 'DataProcessingJob',
    'ActionOnFailure': 'TERMINATE_CLUSTER',
    'HadoopJarStep': {
        'Jar': 'command-runner.jar',
        'Args': [
            'spark-submit',
            '--deploy-mode', 'cluster',
            '--class', 'com.company.DataProcessor',
            's3://spark-jobs/data-processor.jar',
            '--input', 's3://input-bucket/data/',
            '--output', 's3://output-bucket/processed/',
            '--date', '2024-01-01'
        ]
    }
}
```

### Glue-Based ETL Pipeline
```python
# Glue job for ETL processing
glue_job_script = """
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'INPUT_PATH', 'OUTPUT_PATH'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read from S3
df = spark.read.option("header", "true").csv(args['INPUT_PATH'])

# Data transformations
df_cleaned = df.filter(F.col("amount").isNotNull()) \
               .withColumn("amount", F.col("amount").cast("double")) \
               .withColumn("processed_date", F.current_date()) \
               .withColumn("year", F.year(F.col("transaction_date"))) \
               .withColumn("month", F.month(F.col("transaction_date")))

# Write to S3 with partitioning
df_cleaned.write \
          .mode("overwrite") \
          .partitionBy("year", "month") \
          .parquet(args['OUTPUT_PATH'])

job.commit()
"""

# Glue job configuration
glue_job_config = {
    'Name': 'etl-processing-job',
    'Role': 'arn:aws:iam::account:role/GlueServiceRole',
    'Command': {
        'Name': 'glueetl',
        'ScriptLocation': 's3://glue-scripts/etl-script.py',
        'PythonVersion': '3'
    },
    'DefaultArguments': {
        '--job-language': 'python',
        '--job-bookmark-option': 'job-bookmark-enable',
        '--enable-metrics': '',
        '--enable-continuous-cloudwatch-log': 'true'
    },
    'MaxRetries': 1,
    'Timeout': 2880,
    'GlueVersion': '3.0',
    'NumberOfWorkers': 10,
    'WorkerType': 'G.1X'
}
```

## 4. Data Warehouse Architecture

### Redshift-Based Data Warehouse
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │───▶│   Staging       │───▶│   Amazon        │───▶│   BI Tools      │
│ • OLTP Systems  │    │ • S3 Staging    │    │   Redshift      │    │ • QuickSight    │
│ • Data Lake     │    │ • Data Prep     │    │ • Star Schema   │    │ • Tableau       │
│ • External APIs │    │ • Validation    │    │ • Materialized  │    │ • Power BI      │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Implementation**:
```sql
-- Redshift cluster setup
CREATE CLUSTER my_cluster
NODE TYPE dc2.large
NODES 3
MASTER USERNAME admin
MASTER PASSWORD 'SecurePassword123!'
DB NAME analytics
PORT 5439
PUBLICLY ACCESSIBLE false
ENCRYPTED true;

-- Star schema design
-- Dimension tables
CREATE TABLE dim_customer (
    customer_key INTEGER IDENTITY(1,1) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    customer_name VARCHAR(200),
    email VARCHAR(200),
    phone VARCHAR(50),
    address VARCHAR(500),
    city VARCHAR(100),
    state VARCHAR(50),
    country VARCHAR(50),
    created_date DATE,
    updated_date DATE,
    is_active BOOLEAN DEFAULT TRUE
) DISTSTYLE KEY DISTKEY(customer_key) SORTKEY(customer_id);

CREATE TABLE dim_product (
    product_key INTEGER IDENTITY(1,1) PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(200),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    price DECIMAL(10,2),
    cost DECIMAL(10,2),
    created_date DATE,
    updated_date DATE,
    is_active BOOLEAN DEFAULT TRUE
) DISTSTYLE ALL SORTKEY(product_id);

CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    date_value DATE NOT NULL,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    week INTEGER,
    day INTEGER,
    day_of_week INTEGER,
    day_name VARCHAR(20),
    month_name VARCHAR(20),
    is_weekend BOOLEAN,
    is_holiday BOOLEAN
) DISTSTYLE ALL SORTKEY(date_key);

-- Fact table
CREATE TABLE fact_sales (
    sales_key INTEGER IDENTITY(1,1) PRIMARY KEY,
    date_key INTEGER NOT NULL,
    customer_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    discount_amount DECIMAL(10,2),
    tax_amount DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    created_timestamp TIMESTAMP DEFAULT GETDATE()
) 
DISTSTYLE KEY 
DISTKEY(customer_key) 
SORTKEY(date_key, customer_key);

-- Foreign key constraints
ALTER TABLE fact_sales ADD CONSTRAINT fk_sales_date 
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key);
ALTER TABLE fact_sales ADD CONSTRAINT fk_sales_customer 
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key);
ALTER TABLE fact_sales ADD CONSTRAINT fk_sales_product 
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key);
```

**ETL Process for Data Warehouse**:
```python
# Python script for Redshift ETL
import psycopg2
import boto3
from datetime import datetime

class RedshiftETL:
    def __init__(self, cluster_endpoint, database, username, password):
        self.conn = psycopg2.connect(
            host=cluster_endpoint,
            database=database,
            user=username,
            password=password,
            port=5439
        )
        self.s3 = boto3.client('s3')
    
    def load_dimension_table(self, table_name, s3_path, iam_role):
        """Load dimension table using COPY command"""
        copy_sql = f"""
        COPY {table_name}
        FROM '{s3_path}'
        IAM_ROLE '{iam_role}'
        CSV
        IGNOREHEADER 1
        DATEFORMAT 'YYYY-MM-DD'
        TIMEFORMAT 'YYYY-MM-DD HH:MI:SS'
        TRUNCATECOLUMNS
        COMPUPDATE ON;
        """
        
        with self.conn.cursor() as cursor:
            cursor.execute(copy_sql)
            self.conn.commit()
    
    def load_fact_table_incremental(self, s3_path, iam_role, load_date):
        """Incremental load for fact table"""
        staging_sql = f"""
        CREATE TEMP TABLE staging_sales (LIKE fact_sales);
        
        COPY staging_sales
        FROM '{s3_path}'
        IAM_ROLE '{iam_role}'
        CSV
        IGNOREHEADER 1
        DATEFORMAT 'YYYY-MM-DD';
        
        -- Delete existing records for the load date
        DELETE FROM fact_sales 
        WHERE date_key IN (
            SELECT date_key FROM dim_date 
            WHERE date_value = '{load_date}'
        );
        
        -- Insert new records
        INSERT INTO fact_sales
        SELECT * FROM staging_sales;
        
        DROP TABLE staging_sales;
        """
        
        with self.conn.cursor() as cursor:
            cursor.execute(staging_sql)
            self.conn.commit()
    
    def create_materialized_views(self):
        """Create materialized views for common queries"""
        mv_sql = """
        CREATE MATERIALIZED VIEW mv_monthly_sales AS
        SELECT 
            d.year,
            d.month,
            d.month_name,
            c.customer_name,
            p.category,
            SUM(f.quantity) as total_quantity,
            SUM(f.total_amount) as total_revenue,
            COUNT(DISTINCT f.sales_key) as transaction_count
        FROM fact_sales f
        JOIN dim_date d ON f.date_key = d.date_key
        JOIN dim_customer c ON f.customer_key = c.customer_key
        JOIN dim_product p ON f.product_key = p.product_key
        GROUP BY d.year, d.month, d.month_name, c.customer_name, p.category;
        """
        
        with self.conn.cursor() as cursor:
            cursor.execute(mv_sql)
            self.conn.commit()
```

## 5. Serverless Architecture

### Lambda-Based Data Processing
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Event Sources │───▶│   AWS Lambda    │───▶│   Processing    │───▶│  Destinations   │
│ • S3 Events     │    │ • Auto Scaling  │    │ • Transform     │    │ • DynamoDB      │
│ • API Gateway   │    │ • Pay per Use   │    │ • Validate      │    │ • S3            │
│ • EventBridge   │    │ • No Servers    │    │ • Enrich        │    │ • SQS/SNS       │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Implementation**:
```python
# Serverless data processing pipeline
import json
import boto3
import pandas as pd
from io import StringIO

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb')
    
    # Process S3 event
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        # Read CSV from S3
        obj = s3.get_object(Bucket=bucket, Key=key)
        df = pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))
        
        # Data processing
        df_processed = process_data(df)
        
        # Write to DynamoDB
        table = dynamodb.Table('processed_data')
        
        with table.batch_writer() as batch:
            for _, row in df_processed.iterrows():
                batch.put_item(Item=row.to_dict())
        
        # Send notification
        sns = boto3.client('sns')
        sns.publish(
            TopicArn='arn:aws:sns:region:account:data-processed',
            Message=f'Processed {len(df_processed)} records from {key}',
            Subject='Data Processing Complete'
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete')
    }

def process_data(df):
    """Data processing logic"""
    # Clean data
    df = df.dropna()
    
    # Transform data
    df['processed_at'] = pd.Timestamp.now()
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    
    # Add business logic
    df['category'] = df['amount'].apply(categorize_amount)
    
    return df

def categorize_amount(amount):
    if amount < 100:
        return 'small'
    elif amount < 1000:
        return 'medium'
    else:
        return 'large'

# SAM template for serverless deployment
sam_template = """
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  DataProcessingFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: lambda_function.lambda_handler
      Runtime: python3.9
      Timeout: 300
      MemorySize: 512
      Environment:
        Variables:
          TABLE_NAME: !Ref ProcessedDataTable
      Events:
        S3Event:
          Type: S3
          Properties:
            Bucket: !Ref DataBucket
            Events: s3:ObjectCreated:*
            Filter:
              S3Key:
                Rules:
                  - Name: prefix
                    Value: incoming/
                  - Name: suffix
                    Value: .csv
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref ProcessedDataTable
        - S3ReadPolicy:
            BucketName: !Ref DataBucket

  ProcessedDataTable:
    Type: AWS::DynamoDB::Table
    Properties:
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
      KeySchema:
        - AttributeName: id
          KeyType: HASH

  DataBucket:
    Type: AWS::S3::Bucket
    Properties:
      NotificationConfiguration:
        LambdaConfigurations:
          - Event: s3:ObjectCreated:*
            Function: !GetAtt DataProcessingFunction.Arn
"""
```

## 6. Multi-Region Architecture

### Cross-Region Data Replication
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Primary       │───▶│   Replication   │───▶│   Secondary     │
│   Region        │    │   Services      │    │   Region        │
│ • RDS Master    │    │ • S3 CRR        │    │ • RDS Replica   │
│ • S3 Primary    │    │ • RDS Replica   │    │ • S3 Replica    │
│ • DynamoDB      │    │ • DDB Global    │    │ • DynamoDB      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Implementation**:
```python
# Multi-region setup with CloudFormation
multi_region_template = {
    "AWSTemplateFormatVersion": "2010-09-09",
    "Parameters": {
        "PrimaryRegion": {"Type": "String", "Default": "us-east-1"},
        "SecondaryRegion": {"Type": "String", "Default": "us-west-2"}
    },
    "Resources": {
        # S3 Cross-Region Replication
        "PrimaryBucket": {
            "Type": "AWS::S3::Bucket",
            "Properties": {
                "BucketName": {"Fn::Sub": "primary-data-${AWS::AccountId}"},
                "VersioningConfiguration": {"Status": "Enabled"},
                "ReplicationConfiguration": {
                    "Role": {"Fn::GetAtt": ["ReplicationRole", "Arn"]},
                    "Rules": [{
                        "Id": "ReplicateAll",
                        "Status": "Enabled",
                        "Prefix": "",
                        "Destination": {
                            "Bucket": {"Fn::Sub": "arn:aws:s3:::secondary-data-${AWS::AccountId}"},
                            "StorageClass": "STANDARD_IA"
                        }
                    }]
                }
            }
        },
        
        # DynamoDB Global Tables
        "GlobalTable": {
            "Type": "AWS::DynamoDB::GlobalTable",
            "Properties": {
                "BillingMode": "PAY_PER_REQUEST",
                "Replicas": [
                    {
                        "Region": {"Ref": "PrimaryRegion"},
                        "GlobalSecondaryIndexes": [{
                            "IndexName": "GSI1",
                            "KeySchema": [
                                {"AttributeName": "GSI1PK", "KeyType": "HASH"}
                            ],
                            "Projection": {"ProjectionType": "ALL"}
                        }]
                    },
                    {
                        "Region": {"Ref": "SecondaryRegion"},
                        "GlobalSecondaryIndexes": [{
                            "IndexName": "GSI1",
                            "KeySchema": [
                                {"AttributeName": "GSI1PK", "KeyType": "HASH"}
                            ],
                            "Projection": {"ProjectionType": "ALL"}
                        }]
                    }
                ],
                "AttributeDefinitions": [
                    {"AttributeName": "PK", "AttributeType": "S"},
                    {"AttributeName": "SK", "AttributeType": "S"},
                    {"AttributeName": "GSI1PK", "AttributeType": "S"}
                ]
            }
        }
    }
}

# Route 53 health checks and failover
route53_config = {
    "HealthCheck": {
        "Type": "AWS::Route53::HealthCheck",
        "Properties": {
            "Type": "HTTPS",
            "ResourcePath": "/health",
            "FullyQualifiedDomainName": "api.primary-region.company.com",
            "Port": 443,
            "RequestInterval": 30,
            "FailureThreshold": 3
        }
    },
    "PrimaryRecord": {
        "Type": "AWS::Route53::RecordSet",
        "Properties": {
            "HostedZoneId": "Z123456789",
            "Name": "api.company.com",
            "Type": "CNAME",
            "SetIdentifier": "primary",
            "Failover": "PRIMARY",
            "TTL": 60,
            "ResourceRecords": ["api.primary-region.company.com"],
            "HealthCheckId": {"Ref": "HealthCheck"}
        }
    },
    "SecondaryRecord": {
        "Type": "AWS::Route53::RecordSet",
        "Properties": {
            "HostedZoneId": "Z123456789",
            "Name": "api.company.com",
            "Type": "CNAME",
            "SetIdentifier": "secondary",
            "Failover": "SECONDARY",
            "TTL": 60,
            "ResourceRecords": ["api.secondary-region.company.com"]
        }
    }
}
```

## 7. Security Architecture Patterns

### Data Encryption and Key Management
```python
# Comprehensive encryption setup
kms_config = {
    "DataEncryptionKey": {
        "Type": "AWS::KMS::Key",
        "Properties": {
            "Description": "Data encryption key for sensitive data",
            "KeyPolicy": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "Enable IAM User Permissions",
                        "Effect": "Allow",
                        "Principal": {"AWS": {"Fn::Sub": "arn:aws:iam::${AWS::AccountId}:root"}},
                        "Action": "kms:*",
                        "Resource": "*"
                    },
                    {
                        "Sid": "Allow use of the key",
                        "Effect": "Allow",
                        "Principal": {"AWS": {"Fn::GetAtt": ["DataProcessingRole", "Arn"]}},
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
        }
    },
    
    "EncryptedBucket": {
        "Type": "AWS::S3::Bucket",
        "Properties": {
            "BucketEncryption": {
                "ServerSideEncryptionConfiguration": [{
                    "ServerSideEncryptionByDefault": {
                        "SSEAlgorithm": "aws:kms",
                        "KMSMasterKeyID": {"Ref": "DataEncryptionKey"}
                    },
                    "BucketKeyEnabled": True
                }]
            },
            "PublicAccessBlockConfiguration": {
                "BlockPublicAcls": True,
                "BlockPublicPolicy": True,
                "IgnorePublicAcls": True,
                "RestrictPublicBuckets": True
            }
        }
    }
}

# VPC with private subnets
vpc_config = {
    "VPC": {
        "Type": "AWS::EC2::VPC",
        "Properties": {
            "CidrBlock": "10.0.0.0/16",
            "EnableDnsHostnames": True,
            "EnableDnsSupport": True
        }
    },
    
    "PrivateSubnet1": {
        "Type": "AWS::EC2::Subnet",
        "Properties": {
            "VpcId": {"Ref": "VPC"},
            "CidrBlock": "10.0.1.0/24",
            "AvailabilityZone": {"Fn::Select": [0, {"Fn::GetAZs": ""}]}
        }
    },
    
    "PrivateSubnet2": {
        "Type": "AWS::EC2::Subnet",
        "Properties": {
            "VpcId": {"Ref": "VPC"},
            "CidrBlock": "10.0.2.0/24",
            "AvailabilityZone": {"Fn::Select": [1, {"Fn::GetAZs": ""}]}
        }
    },
    
    "VPCEndpointS3": {
        "Type": "AWS::EC2::VPCEndpoint",
        "Properties": {
            "VpcId": {"Ref": "VPC"},
            "ServiceName": {"Fn::Sub": "com.amazonaws.${AWS::Region}.s3"},
            "VpcEndpointType": "Gateway",
            "RouteTableIds": [{"Ref": "PrivateRouteTable"}]
        }
    }
}
```

These architecture patterns provide proven blueprints for building scalable, reliable, and secure data engineering solutions on AWS. Each pattern can be customized based on specific requirements and combined to create comprehensive data platforms.