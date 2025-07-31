# AWS Glue Key Concepts

## 1. Serverless ETL Service
**What it is**: Fully managed extract, transform, and load (ETL) service for preparing data for analytics.

**Core Components**:
- **Data Catalog**: Central metadata repository
- **ETL Jobs**: Data transformation scripts
- **Crawlers**: Automatic schema discovery
- **Triggers**: Job scheduling and orchestration

## 2. Data Catalog
**Purpose**: Centralized metadata store for all data assets across AWS.

**Catalog Structure**:
```python
# Create database
import boto3
glue = boto3.client('glue')

glue.create_database(
    DatabaseInput={
        'Name': 'sales_database',
        'Description': 'Sales data warehouse'
    }
)

# Create table
glue.create_table(
    DatabaseName='sales_database',
    TableInput={
        'Name': 'customer_orders',
        'StorageDescriptor': {
            'Columns': [
                {'Name': 'customer_id', 'Type': 'string'},
                {'Name': 'order_date', 'Type': 'date'},
                {'Name': 'amount', 'Type': 'decimal(10,2)'}
            ],
            'Location': 's3://my-bucket/orders/',
            'InputFormat': 'org.apache.hadoop.mapred.TextInputFormat',
            'OutputFormat': 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat',
            'SerdeInfo': {
                'SerializationLibrary': 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
            }
        }
    }
)
```

## 3. Crawlers
**Purpose**: Automatically discover and catalog data schemas from various sources.

**Crawler Configuration**:
```python
# Create crawler
glue.create_crawler(
    Name='sales-data-crawler',
    Role='arn:aws:iam::account:role/GlueServiceRole',
    DatabaseName='sales_database',
    Targets={
        'S3Targets': [
            {
                'Path': 's3://my-bucket/sales-data/',
                'Exclusions': ['*.tmp', '*.log']
            }
        ]
    },
    Schedule='cron(0 2 * * ? *)',  # Daily at 2 AM
    SchemaChangePolicy={
        'UpdateBehavior': 'UPDATE_IN_DATABASE',
        'DeleteBehavior': 'LOG'
    }
)
```

## 4. ETL Jobs
**Job Types**:
- **Spark Jobs**: For large-scale data processing
- **Python Shell Jobs**: For lightweight scripting
- **Ray Jobs**: For ML workloads

**Spark ETL Script**:
```python
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Initialize
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read from catalog
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="sales_database",
    table_name="raw_orders"
)

# Transform data
transformed = ApplyMapping.apply(
    frame=datasource,
    mappings=[
        ("order_id", "string", "order_id", "string"),
        ("customer_id", "string", "customer_id", "string"),
        ("order_date", "string", "order_date", "date"),
        ("amount", "string", "amount", "decimal(10,2)")
    ]
)

# Filter and clean
filtered = Filter.apply(
    frame=transformed,
    f=lambda x: x["amount"] > 0
)

# Write to S3
glueContext.write_dynamic_frame.from_options(
    frame=filtered,
    connection_type="s3",
    connection_options={
        "path": "s3://processed-bucket/orders/",
        "partitionKeys": ["year", "month"]
    },
    format="parquet"
)

job.commit()
```

## 5. Data Transformations
**Built-in Transforms**:
```python
# ApplyMapping - rename/cast columns
mapped = ApplyMapping.apply(
    frame=df,
    mappings=[
        ("old_name", "string", "new_name", "string"),
        ("price", "string", "price", "decimal(10,2)")
    ]
)

# Filter - remove unwanted records
filtered = Filter.apply(
    frame=df,
    f=lambda x: x["status"] == "ACTIVE"
)

# Join - combine datasets
joined = Join.apply(
    frame1=customers,
    frame2=orders,
    keys1=["customer_id"],
    keys2=["customer_id"]
)

# DropFields - remove columns
cleaned = DropFields.apply(
    frame=df,
    paths=["temp_column", "debug_info"]
)
```

## 6. Job Scheduling & Triggers
**Trigger Types**:
```python
# Schedule-based trigger
glue.create_trigger(
    Name='daily-etl-trigger',
    Type='SCHEDULED',
    Schedule='cron(0 2 * * ? *)',
    Actions=[
        {
            'JobName': 'process-sales-data',
            'Arguments': {
                '--date': '${date}'
            }
        }
    ]
)

# Event-based trigger
glue.create_trigger(
    Name='on-demand-trigger',
    Type='ON_DEMAND',
    Actions=[
        {'JobName': 'process-sales-data'}
    ]
)

# Conditional trigger
glue.create_trigger(
    Name='conditional-trigger',
    Type='CONDITIONAL',
    Predicate={
        'Conditions': [
            {
                'LogicalOperator': 'EQUALS',
                'JobName': 'extract-job',
                'State': 'SUCCEEDED'
            }
        ]
    },
    Actions=[
        {'JobName': 'transform-job'}
    ]
)
```

## 7. Data Quality & Monitoring
**Data Quality Rules**:
```python
# Data quality evaluation
from awsglue.data_quality import *

# Define rules
rules = """
    Rules = [
        ColumnCount > 5,
        IsComplete "customer_id",
        IsUnique "customer_id",
        Mean "amount" > 0,
        ColumnValues "status" in ["ACTIVE", "INACTIVE"]
    ]
"""

# Evaluate quality
quality_result = EvaluateDataQuality.apply(
    frame=datasource,
    ruleset=rules,
    publishing_options={
        "dataQualityEvaluationContext": "sales_data_quality",
        "enableDataQualityCloudWatchMetrics": True
    }
)
```

**Job Monitoring**:
```python
# CloudWatch metrics
import boto3
cloudwatch = boto3.client('cloudwatch')

# Custom metrics
cloudwatch.put_metric_data(
    Namespace='Glue/Jobs',
    MetricData=[
        {
            'MetricName': 'RecordsProcessed',
            'Value': record_count,
            'Unit': 'Count',
            'Dimensions': [
                {
                    'Name': 'JobName',
                    'Value': 'process-sales-data'
                }
            ]
        }
    ]
)
```

## 8. Cost Optimization
**Strategies**:
- **Right-sizing**: Choose appropriate worker types
- **Auto Scaling**: Enable dynamic worker allocation
- **Spot Instances**: Use for fault-tolerant workloads
- **Job Bookmarks**: Process only new data

**Configuration Example**:
```python
# Job configuration for cost optimization
job_config = {
    'Role': 'GlueServiceRole',
    'Command': {
        'Name': 'glueetl',
        'ScriptLocation': 's3://scripts/etl-job.py'
    },
    'DefaultArguments': {
        '--enable-metrics': '',
        '--enable-continuous-cloudwatch-log': 'true',
        '--job-bookmark-option': 'job-bookmark-enable',
        '--enable-auto-scaling': 'true'
    },
    'MaxCapacity': 10,
    'WorkerType': 'G.1X',
    'NumberOfWorkers': 2
}
```