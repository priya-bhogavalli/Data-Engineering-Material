# AWS Glue Interview Questions - Complete Guide (200+ Questions)

## 📋 Table of Contents

1. [Basic Level Questions (1-3 years experience)](#basic-level-questions-1-3-years-experience)
2. [Intermediate Level Questions (3-5 years experience)](#intermediate-level-questions-3-5-years-experience)
3. [Advanced Level Questions (5+ years experience)](#advanced-level-questions-5-years-experience)
4. [Architecture & Performance Questions](#architecture--performance-questions)
5. [Data Catalog & Crawlers Questions](#data-catalog--crawlers-questions)
6. [ETL Jobs & Transformations Questions](#etl-jobs--transformations-questions)
7. [Security & Governance Questions](#security--governance-questions)
8. [Cost Optimization Questions](#cost-optimization-questions)
9. [Integration Questions](#integration-questions)
10. [Troubleshooting & Monitoring Questions](#troubleshooting--monitoring-questions)
11. [Scenario-Based Questions](#scenario-based-questions)
12. [Production & Operations Questions](#production--operations-questions)

---

## Basic Level Questions (1-3 years experience)

### 1. What is AWS Glue and what are its main components?

**Answer**: AWS Glue is a fully managed ETL (Extract, Transform, Load) service that makes it easy to prepare and load data for analytics.

**Main Components**:
- **Data Catalog**: Centralized metadata repository
- **ETL Engine**: Apache Spark-based processing engine
- **Crawlers**: Automatic schema discovery and cataloging
- **Job Scheduler**: Workflow orchestration and triggers
- **Development Endpoints**: Interactive development environment

```python
# Basic Glue job structure
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Initialize Glue context
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# ETL logic here
job.commit()
```

### 2. How do you create a basic ETL job in AWS Glue?

**Answer**: Create ETL jobs using AWS Console, CLI, or SDK with these steps:

```python
# 1. Create job using boto3
import boto3

glue = boto3.client('glue')

response = glue.create_job(
    Name='basic-etl-job',
    Role='arn:aws:iam::account:role/GlueServiceRole',
    Command={
        'Name': 'glueetl',
        'ScriptLocation': 's3://my-bucket/scripts/etl-job.py',
        'PythonVersion': '3'
    },
    DefaultArguments={
        '--TempDir': 's3://my-bucket/temp/',
        '--job-bookmark-option': 'job-bookmark-enable'
    },
    MaxRetries=1,
    GlueVersion='4.0',
    NumberOfWorkers=2,
    WorkerType='G.1X'
)

# 2. Basic ETL script
def basic_etl():
    # Read from catalog
    datasource = glueContext.create_dynamic_frame.from_catalog(
        database="my_database",
        table_name="source_table"
    )
    
    # Transform
    transformed = ApplyMapping.apply(
        frame=datasource,
        mappings=[
            ("old_col", "string", "new_col", "string"),
            ("amount", "double", "amount", "double")
        ]
    )
    
    # Write to S3
    glueContext.write_dynamic_frame.from_options(
        frame=transformed,
        connection_type="s3",
        connection_options={"path": "s3://output-bucket/data/"},
        format="parquet"
    )
```

### 3. What is the difference between DynamicFrame and DataFrame in Glue?

**Answer**: DynamicFrame is Glue's extension of Spark DataFrame with additional ETL capabilities.

**Comparison**:
| Feature | DynamicFrame | DataFrame |
|---------|--------------|-----------|
| **Schema** | Self-describing, flexible | Fixed schema |
| **Error Handling** | Built-in error records | Manual handling |
| **Nested Data** | Native support | Requires flattening |
| **Transformations** | ETL-specific transforms | General Spark operations |
| **Performance** | Optimized for ETL | General purpose |

```python
# DynamicFrame example
dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
    database="db", table_name="table"
)

# Convert to DataFrame for Spark operations
df = dynamic_frame.toDF()

# Convert back to DynamicFrame
new_dynamic_frame = DynamicFrame.fromDF(df, glueContext, "new_frame")

# DynamicFrame transformations
mapped_frame = ApplyMapping.apply(
    frame=dynamic_frame,
    mappings=[("old_name", "string", "new_name", "string")]
)

# Error handling
error_frame = dynamic_frame.errorsAsList()
clean_frame = dynamic_frame.drop_fields(["error_field"])
```

### 4. How do you handle different data formats in AWS Glue?

**Answer**: Glue supports multiple data formats with built-in readers and writers.

```python
# Reading different formats
# JSON
json_frame = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://bucket/json-data/"]},
    format="json"
)

# CSV
csv_frame = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://bucket/csv-data/"]},
    format="csv",
    format_options={"withHeader": True, "separator": ","}
)

# Parquet
parquet_frame = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://bucket/parquet-data/"]},
    format="parquet"
)

# Avro
avro_frame = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://bucket/avro-data/"]},
    format="avro"
)

# Writing different formats
glueContext.write_dynamic_frame.from_options(
    frame=transformed_frame,
    connection_type="s3",
    connection_options={"path": "s3://output/"},
    format="parquet",
    format_options={"compression": "snappy"}
)
```

### 5. What are AWS Glue Crawlers and how do they work?

**Answer**: Crawlers automatically discover and catalog data schemas from various sources.

```python
# Create crawler
crawler_config = {
    'Name': 'sales-data-crawler',
    'Role': 'arn:aws:iam::account:role/GlueServiceRole',
    'DatabaseName': 'sales_db',
    'Targets': {
        'S3Targets': [
            {
                'Path': 's3://data-bucket/sales/',
                'Exclusions': ['*.tmp', '*.log', '_*']
            }
        ],
        'JdbcTargets': [
            {
                'ConnectionName': 'rds-connection',
                'Path': 'sales_db/customers'
            }
        ]
    },
    'Schedule': 'cron(0 12 * * ? *)',  # Daily at noon
    'SchemaChangePolicy': {
        'UpdateBehavior': 'UPDATE_IN_DATABASE',
        'DeleteBehavior': 'LOG'
    },
    'Configuration': json.dumps({
        "Version": 1.0,
        "CrawlerOutput": {
            "Partitions": {"AddOrUpdateBehavior": "InheritFromTable"}
        }
    })
}

glue.create_crawler(**crawler_config)

# Start crawler
glue.start_crawler(Name='sales-data-crawler')

# Monitor crawler
response = glue.get_crawler(Name='sales-data-crawler')
print(f"Crawler state: {response['Crawler']['State']}")
```

### 6. How do you schedule AWS Glue jobs?

**Answer**: Schedule jobs using triggers, workflows, or external orchestration tools.

```python
# 1. Time-based trigger
time_trigger = {
    'Name': 'daily-etl-trigger',
    'Type': 'SCHEDULED',
    'Schedule': 'cron(0 2 * * ? *)',  # Daily at 2 AM
    'Actions': [
        {
            'JobName': 'daily-etl-job',
            'Arguments': {
                '--date': '${date}'
            }
        }
    ],
    'StartOnCreation': True
}

glue.create_trigger(**time_trigger)

# 2. Event-based trigger
event_trigger = {
    'Name': 'crawler-completion-trigger',
    'Type': 'CONDITIONAL',
    'Predicate': {
        'Conditions': [
            {
                'LogicalOperator': 'EQUALS',
                'CrawlerName': 'source-crawler',
                'CrawlState': 'SUCCEEDED'
            }
        ]
    },
    'Actions': [
        {
            'JobName': 'process-crawled-data',
            'Arguments': {
                '--database': 'source_db'
            }
        }
    ]
}

glue.create_trigger(**event_trigger)

# 3. Workflow
workflow = {
    'Name': 'data-processing-workflow',
    'Description': 'Complete data processing pipeline'
}

glue.create_workflow(**workflow)
```

### 7. What is the AWS Glue Data Catalog?

**Answer**: The Data Catalog is a centralized metadata repository that stores table definitions, schema information, and other metadata.

```python
# Create database
glue.create_database(
    DatabaseInput={
        'Name': 'analytics_db',
        'Description': 'Analytics database for reporting'
    }
)

# Create table
table_input = {
    'Name': 'customer_orders',
    'StorageDescriptor': {
        'Columns': [
            {'Name': 'customer_id', 'Type': 'bigint'},
            {'Name': 'order_date', 'Type': 'date'},
            {'Name': 'total_amount', 'Type': 'decimal(10,2)'},
            {'Name': 'status', 'Type': 'string'}
        ],
        'Location': 's3://data-lake/customer-orders/',
        'InputFormat': 'org.apache.hadoop.mapred.TextInputFormat',
        'OutputFormat': 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat',
        'SerdeInfo': {
            'SerializationLibrary': 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe',
            'Parameters': {'field.delim': ','}
        }
    },
    'PartitionKeys': [
        {'Name': 'year', 'Type': 'string'},
        {'Name': 'month', 'Type': 'string'}
    ]
}

glue.create_table(
    DatabaseName='analytics_db',
    TableInput=table_input
)

# Query catalog
tables = glue.get_tables(DatabaseName='analytics_db')
for table in tables['TableList']:
    print(f"Table: {table['Name']}, Location: {table['StorageDescriptor']['Location']}")
```

### 8. How do you handle errors in AWS Glue jobs?

**Answer**: Implement error handling using try-catch blocks, error records, and monitoring.

```python
import logging
from awsglue.utils import getResolvedOptions

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handle_errors_in_glue():
    try:
        # Main ETL logic
        datasource = glueContext.create_dynamic_frame.from_catalog(
            database="source_db",
            table_name="raw_data"
        )
        
        # Check for errors in source data
        if datasource.count() == 0:
            raise ValueError("No data found in source table")
        
        # Transform with error handling
        transformed = ApplyMapping.apply(
            frame=datasource,
            mappings=[
                ("id", "string", "customer_id", "long"),
                ("amount", "string", "amount", "double")
            ]
        )
        
        # Separate error records
        error_records = transformed.errorsAsList()
        if error_records:
            logger.warning(f"Found {len(error_records)} error records")
            
            # Write error records to separate location
            error_frame = DynamicFrame.fromDF(
                spark.createDataFrame(error_records),
                glueContext,
                "error_frame"
            )
            
            glueContext.write_dynamic_frame.from_options(
                frame=error_frame,
                connection_type="s3",
                connection_options={"path": "s3://error-bucket/errors/"},
                format="json"
            )
        
        # Process clean records
        clean_frame = transformed.drop_fields(["error"])
        
        # Write output
        glueContext.write_dynamic_frame.from_options(
            frame=clean_frame,
            connection_type="s3",
            connection_options={"path": "s3://output-bucket/clean-data/"},
            format="parquet"
        )
        
        logger.info(f"Successfully processed {clean_frame.count()} records")
        
    except Exception as e:
        logger.error(f"Job failed with error: {str(e)}")
        
        # Send notification
        import boto3
        sns = boto3.client('sns')
        sns.publish(
            TopicArn='arn:aws:sns:region:account:glue-failures',
            Subject='Glue Job Failed',
            Message=f"Job {args['JOB_NAME']} failed: {str(e)}"
        )
        
        # Re-raise to fail the job
        raise
```

### 9. What are the different worker types in AWS Glue?

**Answer**: Glue offers different worker types optimized for various workloads.

**Worker Types**:
| Type | vCPU | Memory | Use Case | Cost |
|------|------|--------|----------|------|
| **G.1X** | 4 | 16 GB | General purpose | $0.44/DPU-hour |
| **G.2X** | 8 | 32 GB | Memory-intensive | $0.88/DPU-hour |
| **G.025X** | 2 | 4 GB | Light workloads | $0.44/DPU-hour |

```python
# Configure worker type in job
job_config = {
    'Name': 'memory-intensive-job',
    'Role': 'arn:aws:iam::account:role/GlueServiceRole',
    'Command': {
        'Name': 'glueetl',
        'ScriptLocation': 's3://scripts/heavy-processing.py'
    },
    'WorkerType': 'G.2X',  # For memory-intensive operations
    'NumberOfWorkers': 10,
    'GlueVersion': '4.0',
    'MaxRetries': 1,
    'Timeout': 2880  # 48 hours
}

# For streaming jobs
streaming_job_config = {
    'Name': 'streaming-job',
    'WorkerType': 'G.1X',
    'NumberOfWorkers': 5,
    'Command': {
        'Name': 'gluestreaming',
        'ScriptLocation': 's3://scripts/streaming-job.py'
    }
}
```

### 10. How do you optimize AWS Glue job performance?

**Answer**: Optimize through proper resource allocation, data partitioning, and efficient transformations.

```python
# 1. Optimize data reading
def optimize_data_reading():
    # Use pushdown predicates
    datasource = glueContext.create_dynamic_frame.from_catalog(
        database="db",
        table_name="large_table",
        push_down_predicate="date >= '2024-01-01'"
    )
    
    # Read only required columns
    selected_fields = SelectFields.apply(
        frame=datasource,
        paths=["customer_id", "amount", "date"]
    )
    
    return selected_fields

# 2. Optimize transformations
def optimize_transformations(df):
    # Use broadcast joins for small tables
    from pyspark.sql.functions import broadcast
    
    small_df = spark.read.table("small_lookup_table")
    result = df.join(broadcast(small_df), "key")
    
    # Partition data appropriately
    result.write \
        .partitionBy("year", "month") \
        .mode("overwrite") \
        .parquet("s3://output/partitioned-data/")
    
    return result

# 3. Optimize job configuration
optimal_config = {
    'WorkerType': 'G.1X',  # Start with G.1X, scale up if needed
    'NumberOfWorkers': 10,  # Based on data size
    'MaxConcurrentRuns': 1,  # Prevent resource conflicts
    'DefaultArguments': {
        '--enable-metrics': '',
        '--enable-continuous-cloudwatch-log': 'true',
        '--job-bookmark-option': 'job-bookmark-enable'
    }
}
```

---

## Intermediate Level Questions (3-5 years experience)

### 11. How do you implement incremental data processing in AWS Glue?

**Answer**: Use job bookmarks, timestamps, or custom logic to process only new/changed data.

```python
# 1. Using Job Bookmarks
def incremental_with_bookmarks():
    # Enable job bookmarks in job configuration
    datasource = glueContext.create_dynamic_frame.from_catalog(
        database="source_db",
        table_name="incremental_table",
        transformation_ctx="datasource"  # Required for bookmarks
    )
    
    # Glue automatically tracks processed data
    transformed = ApplyMapping.apply(
        frame=datasource,
        mappings=[("id", "long", "id", "long")],
        transformation_ctx="transformed"
    )
    
    # Write with bookmark context
    glueContext.write_dynamic_frame.from_options(
        frame=transformed,
        connection_type="s3",
        connection_options={"path": "s3://output/incremental/"},
        format="parquet",
        transformation_ctx="output"
    )

# 2. Using timestamp-based incremental processing
def timestamp_based_incremental():
    from datetime import datetime, timedelta
    
    # Get last processed timestamp
    last_run = get_last_run_timestamp()  # Custom function
    current_run = datetime.now()
    
    # Filter data based on timestamp
    df = spark.sql(f"""
        SELECT * FROM source_table 
        WHERE updated_timestamp > '{last_run}' 
        AND updated_timestamp <= '{current_run}'
    """)
    
    if df.count() > 0:
        # Process incremental data
        processed_df = transform_data(df)
        
        # Write to target
        processed_df.write \
            .mode("append") \
            .parquet("s3://output/incremental/")
        
        # Update last run timestamp
        update_last_run_timestamp(current_run)
    
    return df.count()

# 3. CDC (Change Data Capture) processing
def process_cdc_data():
    cdc_frame = glueContext.create_dynamic_frame.from_catalog(
        database="cdc_db",
        table_name="cdc_table"
    )
    
    # Convert to DataFrame for complex operations
    cdc_df = cdc_frame.toDF()
    
    # Separate operations
    inserts = cdc_df.filter(cdc_df.operation == 'I')
    updates = cdc_df.filter(cdc_df.operation == 'U')
    deletes = cdc_df.filter(cdc_df.operation == 'D')
    
    # Process each operation type
    process_inserts(inserts)
    process_updates(updates)
    process_deletes(deletes)
```

### 12. How do you handle schema evolution in AWS Glue?

**Answer**: Configure crawlers and jobs to handle schema changes automatically or with controlled updates.

```python
# 1. Crawler schema change policy
crawler_config = {
    'Name': 'schema-evolution-crawler',
    'SchemaChangePolicy': {
        'UpdateBehavior': 'UPDATE_IN_DATABASE',  # Update existing tables
        'DeleteBehavior': 'LOG'  # Log deleted columns
    },
    'Configuration': json.dumps({
        "Version": 1.0,
        "CrawlerOutput": {
            "Partitions": {"AddOrUpdateBehavior": "InheritFromTable"},
            "Tables": {"AddOrUpdateBehavior": "MergeNewColumns"}
        }
    })
}

# 2. Handle schema evolution in ETL jobs
def handle_schema_evolution():
    # Read with schema evolution support
    datasource = glueContext.create_dynamic_frame.from_catalog(
        database="evolving_db",
        table_name="evolving_table"
    )
    
    # Get current schema
    current_schema = datasource.schema()
    print(f"Current schema: {current_schema}")
    
    # Handle missing columns
    required_columns = ["id", "name", "email", "created_date"]
    
    for col in required_columns:
        if col not in [field.name for field in current_schema]:
            # Add missing column with default value
            datasource = datasource.resolveChoice(specs=[(col, "cast:string")])
    
    # Handle data type changes
    type_mappings = [
        ("id", "string", "id", "long"),
        ("amount", "string", "amount", "double"),
        ("date", "string", "date", "timestamp")
    ]
    
    transformed = ApplyMapping.apply(
        frame=datasource,
        mappings=type_mappings
    )
    
    return transformed

# 3. Version-aware schema handling
def version_aware_processing():
    # Detect schema version
    sample_record = datasource.toDF().first()
    
    if 'schema_version' in sample_record:
        version = sample_record['schema_version']
    else:
        version = "1.0"  # Default version
    
    # Apply version-specific transformations
    if version == "1.0":
        return transform_v1(datasource)
    elif version == "2.0":
        return transform_v2(datasource)
    else:
        raise ValueError(f"Unsupported schema version: {version}")
```

### 13. How do you implement data quality checks in AWS Glue?

**Answer**: Use AWS Glue Data Quality, custom validation functions, and error handling mechanisms.

```python
# 1. AWS Glue Data Quality (Native)
from awsglue.data_quality import *

def implement_data_quality():
    # Define data quality rules
    rules = """
    Rules = [
        Completeness "customer_id" > 0.95,
        Uniqueness "customer_id" > 0.99,
        ColumnValues "amount" > 0,
        ColumnDataType "email" = "string",
        ColumnLength "phone" between 10 and 15,
        CustomSql "SELECT COUNT(*) FROM primary WHERE date >= current_date - 7" > 1000
    ]
    """
    
    # Apply data quality evaluation
    quality_result = EvaluateDataQuality.apply(
        frame=datasource,
        ruleset=rules,
        publishing_options={
            "dataQualityEvaluationContext": "customer_data_quality",
            "enableDataQualityCloudWatchMetrics": True,
            "enableDataQualityResultsPublishing": True
        }
    )
    
    # Get quality results
    quality_df = quality_result["ruleOutcomes"]
    failed_rules = quality_df.filter(quality_df.Outcome == "Failed")
    
    if failed_rules.count() > 0:
        print("Data quality issues found:")
        failed_rules.show()
        
        # Send alert
        send_quality_alert(failed_rules)
    
    return quality_result

# 2. Custom data quality checks
def custom_data_quality_checks(df):
    from pyspark.sql.functions import col, count, when, isnan, isnull
    
    total_records = df.count()
    
    # Completeness checks
    completeness_results = {}
    for column in df.columns:
        null_count = df.filter(col(column).isNull() | isnan(col(column))).count()
        completeness_rate = (total_records - null_count) / total_records
        completeness_results[column] = completeness_rate
        
        if completeness_rate < 0.95:
            print(f"Warning: {column} completeness is {completeness_rate:.2%}")
    
    # Uniqueness checks
    unique_checks = {
        'customer_id': df.select('customer_id').distinct().count() / total_records,
        'email': df.select('email').distinct().count() / total_records
    }
    
    # Range checks
    amount_stats = df.select('amount').describe().collect()
    min_amount = float(amount_stats[3]['amount'])  # min
    max_amount = float(amount_stats[4]['amount'])  # max
    
    if min_amount < 0:
        print(f"Warning: Negative amounts found (min: {min_amount})")
    
    # Pattern checks
    invalid_emails = df.filter(~col('email').rlike(r'^[^@]+@[^@]+\.[^@]+$')).count()
    if invalid_emails > 0:
        print(f"Warning: {invalid_emails} invalid email formats found")
    
    return {
        'completeness': completeness_results,
        'uniqueness': unique_checks,
        'range_issues': min_amount < 0,
        'pattern_issues': invalid_emails
    }

# 3. Data profiling
def profile_data(df):
    from pyspark.sql.functions import mean, stddev, min, max, count
    
    # Statistical profiling
    numeric_columns = [field.name for field in df.schema.fields 
                      if field.dataType.typeName() in ['double', 'float', 'integer', 'long']]
    
    for col_name in numeric_columns:
        stats = df.select(
            mean(col(col_name)).alias('mean'),
            stddev(col(col_name)).alias('stddev'),
            min(col(col_name)).alias('min'),
            max(col(col_name)).alias('max'),
            count(col(col_name)).alias('count')
        ).collect()[0]
        
        print(f"{col_name}: mean={stats['mean']:.2f}, std={stats['stddev']:.2f}")
    
    # Categorical profiling
    categorical_columns = [field.name for field in df.schema.fields 
                          if field.dataType.typeName() == 'string']
    
    for col_name in categorical_columns:
        value_counts = df.groupBy(col_name).count().orderBy('count', ascending=False)
        print(f"{col_name} top values:")
        value_counts.show(5)
```

### 14. How do you optimize costs for AWS Glue jobs?

**Answer**: Implement cost optimization through right-sizing, scheduling, and efficient resource usage.

```python
# 1. Right-sizing workers
def optimize_worker_configuration():
    # Monitor job metrics to determine optimal configuration
    job_metrics = get_job_metrics()  # Custom function
    
    if job_metrics['memory_utilization'] < 50:
        # Reduce worker size
        return {
            'WorkerType': 'G.1X',
            'NumberOfWorkers': max(2, job_metrics['current_workers'] // 2)
        }
    elif job_metrics['memory_utilization'] > 80:
        # Increase worker size or count
        return {
            'WorkerType': 'G.2X',
            'NumberOfWorkers': job_metrics['current_workers']
        }
    
    return job_metrics['current_config']

# 2. Efficient data processing
def cost_efficient_processing():
    # Use columnar formats
    df.write \
        .option("compression", "snappy") \
        .mode("overwrite") \
        .parquet("s3://output/optimized-data/")
    
    # Partition data for better query performance
    df.write \
        .partitionBy("year", "month", "day") \
        .parquet("s3://output/partitioned-data/")
    
    # Use appropriate file sizes (128MB - 1GB)
    df.coalesce(optimal_partition_count) \
        .write \
        .parquet("s3://output/coalesced-data/")

# 3. Job scheduling optimization
def optimize_job_scheduling():
    # Schedule jobs during off-peak hours
    off_peak_trigger = {
        'Name': 'off-peak-etl',
        'Type': 'SCHEDULED',
        'Schedule': 'cron(0 2 * * ? *)',  # 2 AM
        'Actions': [{'JobName': 'cost-optimized-job'}]
    }
    
    # Use spot instances for development/testing
    dev_job_config = {
        'WorkerType': 'G.1X',
        'NumberOfWorkers': 2,
        'DefaultArguments': {
            '--enable-spark-ui': 'false',  # Disable for cost savings
            '--enable-metrics': 'false'
        }
    }
    
    return off_peak_trigger, dev_job_config

# 4. Resource monitoring and alerting
def setup_cost_monitoring():
    import boto3
    
    cloudwatch = boto3.client('cloudwatch')
    
    # Create cost alarm
    cloudwatch.put_metric_alarm(
        AlarmName='GlueJobCostAlert',
        ComparisonOperator='GreaterThanThreshold',
        EvaluationPeriods=1,
        MetricName='DPUHour',
        Namespace='AWS/Glue',
        Period=3600,
        Statistic='Sum',
        Threshold=100.0,  # Alert if DPU hours > 100
        ActionsEnabled=True,
        AlarmActions=[
            'arn:aws:sns:region:account:cost-alerts'
        ],
        AlarmDescription='Alert when Glue costs are high'
    )
```

### 15. How do you implement complex transformations in AWS Glue?

**Answer**: Use a combination of Glue transforms, Spark SQL, and custom functions for complex data processing.

```python
# 1. Complex data transformations
def complex_transformations():
    # Read multiple sources
    customers = glueContext.create_dynamic_frame.from_catalog(
        database="crm", table_name="customers"
    )
    orders = glueContext.create_dynamic_frame.from_catalog(
        database="sales", table_name="orders"
    )
    products = glueContext.create_dynamic_frame.from_catalog(
        database="inventory", table_name="products"
    )
    
    # Convert to DataFrames for complex operations
    customers_df = customers.toDF()
    orders_df = orders.toDF()
    products_df = products.toDF()
    
    # Complex join with aggregations
    result = customers_df.alias("c") \
        .join(orders_df.alias("o"), col("c.customer_id") == col("o.customer_id")) \
        .join(products_df.alias("p"), col("o.product_id") == col("p.product_id")) \
        .groupBy("c.customer_id", "c.customer_name", "c.segment") \
        .agg(
            count("o.order_id").alias("total_orders"),
            sum("o.amount").alias("total_spent"),
            avg("o.amount").alias("avg_order_value"),
            collect_list("p.category").alias("purchased_categories")
        )
    
    # Window functions for ranking
    from pyspark.sql.window import Window
    from pyspark.sql.functions import row_number, rank, dense_rank
    
    window_spec = Window.partitionBy("segment").orderBy(col("total_spent").desc())
    
    ranked_customers = result.withColumn(
        "rank_in_segment", 
        row_number().over(window_spec)
    )
    
    return DynamicFrame.fromDF(ranked_customers, glueContext, "complex_result")

# 2. Custom transformation functions
def custom_transformations():
    from pyspark.sql.functions import udf
    from pyspark.sql.types import StringType, DoubleType
    
    # Custom UDF for data cleansing
    @udf(returnType=StringType())
    def clean_phone_number(phone):
        if phone:
            # Remove non-numeric characters
            cleaned = ''.join(filter(str.isdigit, phone))
            # Format as (XXX) XXX-XXXX
            if len(cleaned) == 10:
                return f"({cleaned[:3]}) {cleaned[3:6]}-{cleaned[6:]}"
        return None
    
    # Custom UDF for business logic
    @udf(returnType=DoubleType())
    def calculate_discount(amount, customer_tier):
        if customer_tier == "GOLD":
            return amount * 0.15
        elif customer_tier == "SILVER":
            return amount * 0.10
        elif customer_tier == "BRONZE":
            return amount * 0.05
        return 0.0
    
    # Apply custom transformations
    df = datasource.toDF()
    transformed_df = df \
        .withColumn("clean_phone", clean_phone_number(col("phone"))) \
        .withColumn("discount_amount", calculate_discount(col("amount"), col("tier")))
    
    return DynamicFrame.fromDF(transformed_df, glueContext, "custom_transformed")

# 3. Nested data processing
def process_nested_data():
    # Handle JSON/nested structures
    from pyspark.sql.functions import explode, col, get_json_object
    
    # Flatten nested JSON
    nested_df = datasource.toDF()
    
    # Extract nested fields
    flattened_df = nested_df \
        .withColumn("address_street", get_json_object(col("address"), "$.street")) \
        .withColumn("address_city", get_json_object(col("address"), "$.city")) \
        .withColumn("address_state", get_json_object(col("address"), "$.state"))
    
    # Explode arrays
    if "orders" in nested_df.columns:
        exploded_df = flattened_df \
            .select("customer_id", "name", explode("orders").alias("order")) \
            .select("customer_id", "name", 
                   col("order.order_id").alias("order_id"),
                   col("order.amount").alias("order_amount"))
    
    return DynamicFrame.fromDF(exploded_df, glueContext, "flattened_data")
```

---

*[Continuing with more questions in the next batch to avoid file freezing...]*
# AWS Glue Interview Questions - Complete Guide (200+ Questions)

## 📋 Table of Contents

1. [Basic Level Questions (1-3 years experience)](#basic-level-questions-1-3-years-experience)
2. [Intermediate Level Questions (3-5 years experience)](#intermediate-level-questions-3-5-years-experience)
3. [Advanced Level Questions (5+ years experience)](#advanced-level-questions-5-years-experience)
4. [Architecture & Performance Questions](#architecture--performance-questions)
5. [Data Catalog & Crawlers Questions](#data-catalog--crawlers-questions)
6. [ETL Jobs & Transformations Questions](#etl-jobs--transformations-questions)
7. [Security & Governance Questions](#security--governance-questions)
8. [Cost Optimization Questions](#cost-optimization-questions)
9. [Integration Questions](#integration-questions)
10. [Troubleshooting & Monitoring Questions](#troubleshooting--monitoring-questions)
11. [Scenario-Based Questions](#scenario-based-questions)
12. [Production & Operations Questions](#production--operations-questions)

---

## Basic Level Questions (1-3 years experience)

### 1. What is AWS Glue and what are its main components?

**Answer**: AWS Glue is a fully managed ETL (Extract, Transform, Load) service that makes it easy to prepare and load data for analytics.

**Main Components**:
- **Data Catalog**: Centralized metadata repository
- **ETL Engine**: Apache Spark-based processing engine
- **Crawlers**: Automatic schema discovery and cataloging
- **Job Scheduler**: Workflow orchestration and triggers
- **Development Endpoints**: Interactive development environment

```python
# Basic Glue job structure
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Initialize Glue context
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# ETL logic here
job.commit()
```

### 2. How do you create a basic ETL job in AWS Glue?

**Answer**: Create ETL jobs using AWS Console, CLI, or SDK with these steps:

```python
# 1. Create job using boto3
import boto3

glue = boto3.client('glue')

response = glue.create_job(
    Name='basic-etl-job',
    Role='arn:aws:iam::account:role/GlueServiceRole',
    Command={
        'Name': 'glueetl',
        'ScriptLocation': 's3://my-bucket/scripts/etl-job.py',
        'PythonVersion': '3'
    },
    DefaultArguments={
        '--TempDir': 's3://my-bucket/temp/',
        '--job-bookmark-option': 'job-bookmark-enable'
    },
    MaxRetries=1,
    GlueVersion='4.0',
    NumberOfWorkers=2,
    WorkerType='G.1X'
)

# 2. Basic ETL script
def basic_etl():
    # Read from catalog
    datasource = glueContext.create_dynamic_frame.from_catalog(
        database="my_database",
        table_name="source_table"
    )
    
    # Transform
    transformed = ApplyMapping.apply(
        frame=datasource,
        mappings=[
            ("old_col", "string", "new_col", "string"),
            ("amount", "double", "amount", "double")
        ]
    )
    
    # Write to S3
    glueContext.write_dynamic_frame.from_options(
        frame=transformed,
        connection_type="s3",
        connection_options={"path": "s3://output-bucket/data/"},
        format="parquet"
    )
```

### 3. What is the difference between DynamicFrame and DataFrame in Glue?

**Answer**: DynamicFrame is Glue's extension of Spark DataFrame with additional ETL capabilities.

**Comparison**:
| Feature | DynamicFrame | DataFrame |
|---------|--------------|-----------|
| **Schema** | Self-describing, flexible | Fixed schema |
| **Error Handling** | Built-in error records | Manual handling |
| **Nested Data** | Native support | Requires flattening |
| **Transformations** | ETL-specific transforms | General Spark operations |
| **Performance** | Optimized for ETL | General purpose |

```python
# DynamicFrame example
dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
    database="db", table_name="table"
)

# Convert to DataFrame for Spark operations
df = dynamic_frame.toDF()

# Convert back to DynamicFrame
new_dynamic_frame = DynamicFrame.fromDF(df, glueContext, "new_frame")

# DynamicFrame transformations
mapped_frame = ApplyMapping.apply(
    frame=dynamic_frame,
    mappings=[("old_name", "string", "new_name", "string")]
)

# Error handling
error_frame = dynamic_frame.errorsAsList()
clean_frame = dynamic_frame.drop_fields(["error_field"])
```

### 4. How do you handle different data formats in AWS Glue?

**Answer**: Glue supports multiple data formats with built-in readers and writers.

```python
# Reading different formats
# JSON
json_frame = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://bucket/json-data/"]},
    format="json"
)

# CSV
csv_frame = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://bucket/csv-data/"]},
    format="csv",
    format_options={"withHeader": True, "separator": ","}
)

# Parquet
parquet_frame = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://bucket/parquet-data/"]},
    format="parquet"
)

# Avro
avro_frame = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://bucket/avro-data/"]},
    format="avro"
)

# Writing different formats
glueContext.write_dynamic_frame.from_options(
    frame=transformed_frame,
    connection_type="s3",
    connection_options={"path": "s3://output/"},
    format="parquet",
    format_options={"compression": "snappy"}
)
```

### 5. What are AWS Glue Crawlers and how do they work?

**Answer**: Crawlers automatically discover and catalog data schemas from various sources.

```python
# Create crawler
crawler_config = {
    'Name': 'sales-data-crawler',
    'Role': 'arn:aws:iam::account:role/GlueServiceRole',
    'DatabaseName': 'sales_db',
    'Targets': {
        'S3Targets': [
            {
                'Path': 's3://data-bucket/sales/',
                'Exclusions': ['*.tmp', '*.log', '_*']
            }
        ],
        'JdbcTargets': [
            {
                'ConnectionName': 'rds-connection',
                'Path': 'sales_db/customers'
            }
        ]
    },
    'Schedule': 'cron(0 12 * * ? *)',  # Daily at noon
    'SchemaChangePolicy': {
        'UpdateBehavior': 'UPDATE_IN_DATABASE',
        'DeleteBehavior': 'LOG'
    },
    'Configuration': json.dumps({
        "Version": 1.0,
        "CrawlerOutput": {
            "Partitions": {"AddOrUpdateBehavior": "InheritFromTable"}
        }
    })
}

glue.create_crawler(**crawler_config)

# Start crawler
glue.start_crawler(Name='sales-data-crawler')

# Monitor crawler
response = glue.get_crawler(Name='sales-data-crawler')
print(f"Crawler state: {response['Crawler']['State']}")
```

### 6. How do you schedule AWS Glue jobs?

**Answer**: Schedule jobs using triggers, workflows, or external orchestration tools.

```python
# 1. Time-based trigger
time_trigger = {
    'Name': 'daily-etl-trigger',
    'Type': 'SCHEDULED',
    'Schedule': 'cron(0 2 * * ? *)',  # Daily at 2 AM
    'Actions': [
        {
            'JobName': 'daily-etl-job',
            'Arguments': {
                '--date': '${date}'
            }
        }
    ],
    'StartOnCreation': True
}

glue.create_trigger(**time_trigger)

# 2. Event-based trigger
event_trigger = {
    'Name': 'crawler-completion-trigger',
    'Type': 'CONDITIONAL',
    'Predicate': {
        'Conditions': [
            {
                'LogicalOperator': 'EQUALS',
                'CrawlerName': 'source-crawler',
                'CrawlState': 'SUCCEEDED'
            }
        ]
    },
    'Actions': [
        {
            'JobName': 'process-crawled-data',
            'Arguments': {
                '--database': 'source_db'
            }
        }
    ]
}

glue.create_trigger(**event_trigger)

# 3. Workflow
workflow = {
    'Name': 'data-processing-workflow',
    'Description': 'Complete data processing pipeline'
}

glue.create_workflow(**workflow)
```

### 7. What is the AWS Glue Data Catalog?

**Answer**: The Data Catalog is a centralized metadata repository that stores table definitions, schema information, and other metadata.

```python
# Create database
glue.create_database(
    DatabaseInput={
        'Name': 'analytics_db',
        'Description': 'Analytics database for reporting'
    }
)

# Create table
table_input = {
    'Name': 'customer_orders',
    'StorageDescriptor': {
        'Columns': [
            {'Name': 'customer_id', 'Type': 'bigint'},
            {'Name': 'order_date', 'Type': 'date'},
            {'Name': 'total_amount', 'Type': 'decimal(10,2)'},
            {'Name': 'status', 'Type': 'string'}
        ],
        'Location': 's3://data-lake/customer-orders/',
        'InputFormat': 'org.apache.hadoop.mapred.TextInputFormat',
        'OutputFormat': 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat',
        'SerdeInfo': {
            'SerializationLibrary': 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe',
            'Parameters': {'field.delim': ','}
        }
    },
    'PartitionKeys': [
        {'Name': 'year', 'Type': 'string'},
        {'Name': 'month', 'Type': 'string'}
    ]
}

glue.create_table(
    DatabaseName='analytics_db',
    TableInput=table_input
)

# Query catalog
tables = glue.get_tables(DatabaseName='analytics_db')
for table in tables['TableList']:
    print(f"Table: {table['Name']}, Location: {table['StorageDescriptor']['Location']}")
```

### 8. How do you handle errors in AWS Glue jobs?

**Answer**: Implement error handling using try-catch blocks, error records, and monitoring.

```python
import logging
from awsglue.utils import getResolvedOptions

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handle_errors_in_glue():
    try:
        # Main ETL logic
        datasource = glueContext.create_dynamic_frame.from_catalog(
            database="source_db",
            table_name="raw_data"
        )
        
        # Check for errors in source data
        if datasource.count() == 0:
            raise ValueError("No data found in source table")
        
        # Transform with error handling
        transformed = ApplyMapping.apply(
            frame=datasource,
            mappings=[
                ("id", "string", "customer_id", "long"),
                ("amount", "string", "amount", "double")
            ]
        )
        
        # Separate error records
        error_records = transformed.errorsAsList()
        if error_records:
            logger.warning(f"Found {len(error_records)} error records")
            
            # Write error records to separate location
            error_frame = DynamicFrame.fromDF(
                spark.createDataFrame(error_records),
                glueContext,
                "error_frame"
            )
            
            glueContext.write_dynamic_frame.from_options(
                frame=error_frame,
                connection_type="s3",
                connection_options={"path": "s3://error-bucket/errors/"},
                format="json"
            )
        
        # Process clean records
        clean_frame = transformed.drop_fields(["error"])
        
        # Write output
        glueContext.write_dynamic_frame.from_options(
            frame=clean_frame,
            connection_type="s3",
            connection_options={"path": "s3://output-bucket/clean-data/"},
            format="parquet"
        )
        
        logger.info(f"Successfully processed {clean_frame.count()} records")
        
    except Exception as e:
        logger.error(f"Job failed with error: {str(e)}")
        
        # Send notification
        import boto3
        sns = boto3.client('sns')
        sns.publish(
            TopicArn='arn:aws:sns:region:account:glue-failures',
            Subject='Glue Job Failed',
            Message=f"Job {args['JOB_NAME']} failed: {str(e)}"
        )
        
        # Re-raise to fail the job
        raise
```

### 9. What are the different worker types in AWS Glue?

**Answer**: Glue offers different worker types optimized for various workloads.

**Worker Types**:
| Type | vCPU | Memory | Use Case | Cost |
|------|------|--------|----------|------|
| **G.1X** | 4 | 16 GB | General purpose | $0.44/DPU-hour |
| **G.2X** | 8 | 32 GB | Memory-intensive | $0.88/DPU-hour |
| **G.025X** | 2 | 4 GB | Light workloads | $0.44/DPU-hour |

```python
# Configure worker type in job
job_config = {
    'Name': 'memory-intensive-job',
    'Role': 'arn:aws:iam::account:role/GlueServiceRole',
    'Command': {
        'Name': 'glueetl',
        'ScriptLocation': 's3://scripts/heavy-processing.py'
    },
    'WorkerType': 'G.2X',  # For memory-intensive operations
    'NumberOfWorkers': 10,
    'GlueVersion': '4.0',
    'MaxRetries': 1,
    'Timeout': 2880  # 48 hours
}

# For streaming jobs
streaming_job_config = {
    'Name': 'streaming-job',
    'WorkerType': 'G.1X',
    'NumberOfWorkers': 5,
    'Command': {
        'Name': 'gluestreaming',
        'ScriptLocation': 's3://scripts/streaming-job.py'
    }
}
```

### 10. How do you optimize AWS Glue job performance?

**Answer**: Optimize through proper resource allocation, data partitioning, and efficient transformations.

```python
# 1. Optimize data reading
def optimize_data_reading():
    # Use pushdown predicates
    datasource = glueContext.create_dynamic_frame.from_catalog(
        database="db",
        table_name="large_table",
        push_down_predicate="date >= '2024-01-01'"
    )
    
    # Read only required columns
    selected_fields = SelectFields.apply(
        frame=datasource,
        paths=["customer_id", "amount", "date"]
    )
    
    return selected_fields

# 2. Optimize transformations
def optimize_transformations(df):
    # Use broadcast joins for small tables
    from pyspark.sql.functions import broadcast
    
    small_df = spark.read.table("small_lookup_table")
    result = df.join(broadcast(small_df), "key")
    
    # Partition data appropriately
    result.write \
        .partitionBy("year", "month") \
        .mode("overwrite") \
        .parquet("s3://output/partitioned-data/")
    
    return result

# 3. Optimize job configuration
optimal_config = {
    'WorkerType': 'G.1X',  # Start with G.1X, scale up if needed
    'NumberOfWorkers': 10,  # Based on data size
    'MaxConcurrentRuns': 1,  # Prevent resource conflicts
    'DefaultArguments': {
        '--enable-metrics': '',
        '--enable-continuous-cloudwatch-log': 'true',
        '--job-bookmark-option': 'job-bookmark-enable'
    }
}
```

---

## Intermediate Level Questions (3-5 years experience)

### 11. How do you implement incremental data processing in AWS Glue?

**Answer**: Use job bookmarks, timestamps, or custom logic to process only new/changed data.

```python
# 1. Using Job Bookmarks
def incremental_with_bookmarks():
    # Enable job bookmarks in job configuration
    datasource = glueContext.create_dynamic_frame.from_catalog(
        database="source_db",
        table_name="incremental_table",
        transformation_ctx="datasource"  # Required for bookmarks
    )
    
    # Glue automatically tracks processed data
    transformed = ApplyMapping.apply(
        frame=datasource,
        mappings=[("id", "long", "id", "long")],
        transformation_ctx="transformed"
    )
    
    # Write with bookmark context
    glueContext.write_dynamic_frame.from_options(
        frame=transformed,
        connection_type="s3",
        connection_options={"path": "s3://output/incremental/"},
        format="parquet",
        transformation_ctx="output"
    )

# 2. Using timestamp-based incremental processing
def timestamp_based_incremental():
    from datetime import datetime, timedelta
    
    # Get last processed timestamp
    last_run = get_last_run_timestamp()  # Custom function
    current_run = datetime.now()
    
    # Filter data based on timestamp
    df = spark.sql(f"""
        SELECT * FROM source_table 
        WHERE updated_timestamp > '{last_run}' 
        AND updated_timestamp <= '{current_run}'
    """)
    
    if df.count() > 0:
        # Process incremental data
        processed_df = transform_data(df)
        
        # Write to target
        processed_df.write \
            .mode("append") \
            .parquet("s3://output/incremental/")
        
        # Update last run timestamp
        update_last_run_timestamp(current_run)
    
    return df.count()

# 3. CDC (Change Data Capture) processing
def process_cdc_data():
    cdc_frame = glueContext.create_dynamic_frame.from_catalog(
        database="cdc_db",
        table_name="cdc_table"
    )
    
    # Convert to DataFrame for complex operations
    cdc_df = cdc_frame.toDF()
    
    # Separate operations
    inserts = cdc_df.filter(cdc_df.operation == 'I')
    updates = cdc_df.filter(cdc_df.operation == 'U')
    deletes = cdc_df.filter(cdc_df.operation == 'D')
    
    # Process each operation type
    process_inserts(inserts)
    process_updates(updates)
    process_deletes(deletes)
```

### 12. How do you handle schema evolution in AWS Glue?

**Answer**: Configure crawlers and jobs to handle schema changes automatically or with controlled updates.

```python
# 1. Crawler schema change policy
crawler_config = {
    'Name': 'schema-evolution-crawler',
    'SchemaChangePolicy': {
        'UpdateBehavior': 'UPDATE_IN_DATABASE',  # Update existing tables
        'DeleteBehavior': 'LOG'  # Log deleted columns
    },
    'Configuration': json.dumps({
        "Version": 1.0,
        "CrawlerOutput": {
            "Partitions": {"AddOrUpdateBehavior": "InheritFromTable"},
            "Tables": {"AddOrUpdateBehavior": "MergeNewColumns"}
        }
    })
}

# 2. Handle schema evolution in ETL jobs
def handle_schema_evolution():
    # Read with schema evolution support
    datasource = glueContext.create_dynamic_frame.from_catalog(
        database="evolving_db",
        table_name="evolving_table"
    )
    
    # Get current schema
    current_schema = datasource.schema()
    print(f"Current schema: {current_schema}")
    
    # Handle missing columns
    required_columns = ["id", "name", "email", "created_date"]
    
    for col in required_columns:
        if col not in [field.name for field in current_schema]:
            # Add missing column with default value
            datasource = datasource.resolveChoice(specs=[(col, "cast:string")])
    
    # Handle data type changes
    type_mappings = [
        ("id", "string", "id", "long"),
        ("amount", "string", "amount", "double"),
        ("date", "string", "date", "timestamp")
    ]
    
    transformed = ApplyMapping.apply(
        frame=datasource,
        mappings=type_mappings
    )
    
    return transformed

# 3. Version-aware schema handling
def version_aware_processing():
    # Detect schema version
    sample_record = datasource.toDF().first()
    
    if 'schema_version' in sample_record:
        version = sample_record['schema_version']
    else:
        version = "1.0"  # Default version
    
    # Apply version-specific transformations
    if version == "1.0":
        return transform_v1(datasource)
    elif version == "2.0":
        return transform_v2(datasource)
    else:
        raise ValueError(f"Unsupported schema version: {version}")
```

### 13. How do you implement data quality checks in AWS Glue?

**Answer**: Use AWS Glue Data Quality, custom validation functions, and error handling mechanisms.

```python
# 1. AWS Glue Data Quality (Native)
from awsglue.data_quality import *

def implement_data_quality():
    # Define data quality rules
    rules = """
    Rules = [
        Completeness "customer_id" > 0.95,
        Uniqueness "customer_id" > 0.99,
        ColumnValues "amount" > 0,
        ColumnDataType "email" = "string",
        ColumnLength "phone" between 10 and 15,
        CustomSql "SELECT COUNT(*) FROM primary WHERE date >= current_date - 7" > 1000
    ]
    """
    
    # Apply data quality evaluation
    quality_result = EvaluateDataQuality.apply(
        frame=datasource,
        ruleset=rules,
        publishing_options={
            "dataQualityEvaluationContext": "customer_data_quality",
            "enableDataQualityCloudWatchMetrics": True,
            "enableDataQualityResultsPublishing": True
        }
    )
    
    # Get quality results
    quality_df = quality_result["ruleOutcomes"]
    failed_rules = quality_df.filter(quality_df.Outcome == "Failed")
    
    if failed_rules.count() > 0:
        print("Data quality issues found:")
        failed_rules.show()
        
        # Send alert
        send_quality_alert(failed_rules)
    
    return quality_result

# 2. Custom data quality checks
def custom_data_quality_checks(df):
    from pyspark.sql.functions import col, count, when, isnan, isnull
    
    total_records = df.count()
    
    # Completeness checks
    completeness_results = {}
    for column in df.columns:
        null_count = df.filter(col(column).isNull() | isnan(col(column))).count()
        completeness_rate = (total_records - null_count) / total_records
        completeness_results[column] = completeness_rate
        
        if completeness_rate < 0.95:
            print(f"Warning: {column} completeness is {completeness_rate:.2%}")
    
    # Uniqueness checks
    unique_checks = {
        'customer_id': df.select('customer_id').distinct().count() / total_records,
        'email': df.select('email').distinct().count() / total_records
    }
    
    # Range checks
    amount_stats = df.select('amount').describe().collect()
    min_amount = float(amount_stats[3]['amount'])  # min
    max_amount = float(amount_stats[4]['amount'])  # max
    
    if min_amount < 0:
        print(f"Warning: Negative amounts found (min: {min_amount})")
    
    # Pattern checks
    invalid_emails = df.filter(~col('email').rlike(r'^[^@]+@[^@]+\.[^@]+$')).count()
    if invalid_emails > 0:
        print(f"Warning: {invalid_emails} invalid email formats found")
    
    return {
        'completeness': completeness_results,
        'uniqueness': unique_checks,
        'range_issues': min_amount < 0,
        'pattern_issues': invalid_emails
    }

# 3. Data profiling
def profile_data(df):
    from pyspark.sql.functions import mean, stddev, min, max, count
    
    # Statistical profiling
    numeric_columns = [field.name for field in df.schema.fields 
                      if field.dataType.typeName() in ['double', 'float', 'integer', 'long']]
    
    for col_name in numeric_columns:
        stats = df.select(
            mean(col(col_name)).alias('mean'),
            stddev(col(col_name)).alias('stddev'),
            min(col(col_name)).alias('min'),
            max(col(col_name)).alias('max'),
            count(col(col_name)).alias('count')
        ).collect()[0]
        
        print(f"{col_name}: mean={stats['mean']:.2f}, std={stats['stddev']:.2f}")
    
    # Categorical profiling
    categorical_columns = [field.name for field in df.schema.fields 
                          if field.dataType.typeName() == 'string']
    
    for col_name in categorical_columns:
        value_counts = df.groupBy(col_name).count().orderBy('count', ascending=False)
        print(f"{col_name} top values:")
        value_counts.show(5)
```

### 14. How do you optimize costs for AWS Glue jobs?

**Answer**: Implement cost optimization through right-sizing, scheduling, and efficient resource usage.

```python
# 1. Right-sizing workers
def optimize_worker_configuration():
    # Monitor job metrics to determine optimal configuration
    job_metrics = get_job_metrics()  # Custom function
    
    if job_metrics['memory_utilization'] < 50:
        # Reduce worker size
        return {
            'WorkerType': 'G.1X',
            'NumberOfWorkers': max(2, job_metrics['current_workers'] // 2)
        }
    elif job_metrics['memory_utilization'] > 80:
        # Increase worker size or count
        return {
            'WorkerType': 'G.2X',
            'NumberOfWorkers': job_metrics['current_workers']
        }
    
    return job_metrics['current_config']

# 2. Efficient data processing
def cost_efficient_processing():
    # Use columnar formats
    df.write \
        .option("compression", "snappy") \
        .mode("overwrite") \
        .parquet("s3://output/optimized-data/")
    
    # Partition data for better query performance
    df.write \
        .partitionBy("year", "month", "day") \
        .parquet("s3://output/partitioned-data/")
    
    # Use appropriate file sizes (128MB - 1GB)
    df.coalesce(optimal_partition_count) \
        .write \
        .parquet("s3://output/coalesced-data/")

# 3. Job scheduling optimization
def optimize_job_scheduling():
    # Schedule jobs during off-peak hours
    off_peak_trigger = {
        'Name': 'off-peak-etl',
        'Type': 'SCHEDULED',
        'Schedule': 'cron(0 2 * * ? *)',  # 2 AM
        'Actions': [{'JobName': 'cost-optimized-job'}]
    }
    
    # Use spot instances for development/testing
    dev_job_config = {
        'WorkerType': 'G.1X',
        'NumberOfWorkers': 2,
        'DefaultArguments': {
            '--enable-spark-ui': 'false',  # Disable for cost savings
            '--enable-metrics': 'false'
        }
    }
    
    return off_peak_trigger, dev_job_config

# 4. Resource monitoring and alerting
def setup_cost_monitoring():
    import boto3
    
    cloudwatch = boto3.client('cloudwatch')
    
    # Create cost alarm
    cloudwatch.put_metric_alarm(
        AlarmName='GlueJobCostAlert',
        ComparisonOperator='GreaterThanThreshold',
        EvaluationPeriods=1,
        MetricName='DPUHour',
        Namespace='AWS/Glue',
        Period=3600,
        Statistic='Sum',
        Threshold=100.0,  # Alert if DPU hours > 100
        ActionsEnabled=True,
        AlarmActions=[
            'arn:aws:sns:region:account:cost-alerts'
        ],
        AlarmDescription='Alert when Glue costs are high'
    )
```

### 15. How do you implement complex transformations in AWS Glue?

**Answer**: Use a combination of Glue transforms, Spark SQL, and custom functions for complex data processing.

```python
# 1. Complex data transformations
def complex_transformations():
    # Read multiple sources
    customers = glueContext.create_dynamic_frame.from_catalog(
        database="crm", table_name="customers"
    )
    orders = glueContext.create_dynamic_frame.from_catalog(
        database="sales", table_name="orders"
    )
    products = glueContext.create_dynamic_frame.from_catalog(
        database="inventory", table_name="products"
    )
    
    # Convert to DataFrames for complex operations
    customers_df = customers.toDF()
    orders_df = orders.toDF()
    products_df = products.toDF()
    
    # Complex join with aggregations
    result = customers_df.alias("c") \
        .join(orders_df.alias("o"), col("c.customer_id") == col("o.customer_id")) \
        .join(products_df.alias("p"), col("o.product_id") == col("p.product_id")) \
        .groupBy("c.customer_id", "c.customer_name", "c.segment") \
        .agg(
            count("o.order_id").alias("total_orders"),
            sum("o.amount").alias("total_spent"),
            avg("o.amount").alias("avg_order_value"),
            collect_list("p.category").alias("purchased_categories")
        )
    
    # Window functions for ranking
    from pyspark.sql.window import Window
    from pyspark.sql.functions import row_number, rank, dense_rank
    
    window_spec = Window.partitionBy("segment").orderBy(col("total_spent").desc())
    
    ranked_customers = result.withColumn(
        "rank_in_segment", 
        row_number().over(window_spec)
    )
    
    return DynamicFrame.fromDF(ranked_customers, glueContext, "complex_result")

# 2. Custom transformation functions
def custom_transformations():
    from pyspark.sql.functions import udf
    from pyspark.sql.types import StringType, DoubleType
    
    # Custom UDF for data cleansing
    @udf(returnType=StringType())
    def clean_phone_number(phone):
        if phone:
            # Remove non-numeric characters
            cleaned = ''.join(filter(str.isdigit, phone))
            # Format as (XXX) XXX-XXXX
            if len(cleaned) == 10:
                return f"({cleaned[:3]}) {cleaned[3:6]}-{cleaned[6:]}"
        return None
    
    # Custom UDF for business logic
    @udf(returnType=DoubleType())
    def calculate_discount(amount, customer_tier):
        if customer_tier == "GOLD":
            return amount * 0.15
        elif customer_tier == "SILVER":
            return amount * 0.10
        elif customer_tier == "BRONZE":
            return amount * 0.05
        return 0.0
    
    # Apply custom transformations
    df = datasource.toDF()
    transformed_df = df \
        .withColumn("clean_phone", clean_phone_number(col("phone"))) \
        .withColumn("discount_amount", calculate_discount(col("amount"), col("tier")))
    
    return DynamicFrame.fromDF(transformed_df, glueContext, "custom_transformed")

# 3. Nested data processing
def process_nested_data():
    # Handle JSON/nested structures
    from pyspark.sql.functions import explode, col, get_json_object
    
    # Flatten nested JSON
    nested_df = datasource.toDF()
    
    # Extract nested fields
    flattened_df = nested_df \
        .withColumn("address_street", get_json_object(col("address"), "$.street")) \
        .withColumn("address_city", get_json_object(col("address"), "$.city")) \
        .withColumn("address_state", get_json_object(col("address"), "$.state"))
    
    # Explode arrays
    if "orders" in nested_df.columns:
        exploded_df = flattened_df \
            .select("customer_id", "name", explode("orders").alias("order")) \
            .select("customer_id", "name", 
                   col("order.order_id").alias("order_id"),
                   col("order.amount").alias("order_amount"))
    
    return DynamicFrame.fromDF(exploded_df, glueContext, "flattened_data")
```

---

## Advanced Level Questions (5+ years experience)

### 16. How do you implement a data lake architecture using AWS Glue?

**Answer**: Design a comprehensive data lake with multiple layers, governance, and automated processing.

```python
# 1. Data Lake Architecture Implementation
def implement_data_lake_architecture():
    """
    Data Lake Layers:
    - Raw Layer: Unprocessed data from various sources
    - Processed Layer: Cleaned and standardized data
    - Curated Layer: Business-ready analytical datasets
    """
    
    # Raw Layer Processing
    def process_raw_layer():
        # Multiple source ingestion
        sources = [
            {"name": "sales_api", "format": "json", "path": "s3://raw/sales/"},
            {"name": "crm_db", "format": "jdbc", "connection": "crm-connection"},
            {"name": "web_logs", "format": "csv", "path": "s3://raw/logs/"}
        ]
        
        for source in sources:
            if source["format"] == "jdbc":
                raw_frame = glueContext.create_dynamic_frame.from_options(
                    connection_type="mysql",
                    connection_options={
                        "useConnectionProperties": "true",
                        "connectionName": source["connection"]
                    }
                )
            else:
                raw_frame = glueContext.create_dynamic_frame.from_options(
                    connection_type="s3",
                    connection_options={"paths": [source["path"]]},
                    format=source["format"]
                )
            
            # Add metadata columns
            enriched_frame = raw_frame.toDF() \
                .withColumn("ingestion_timestamp", current_timestamp()) \
                .withColumn("source_system", lit(source["name"])) \
                .withColumn("file_name", input_file_name())
            
            # Write to processed layer with partitioning
            DynamicFrame.fromDF(enriched_frame, glueContext, f"enriched_{source['name']}") \
                .write.partitionBy("year", "month", "day") \
                .mode("append") \
                .parquet(f"s3://processed/{source['name']}/")
    
    # Processed Layer - Data Quality and Standardization
    def process_standardized_layer():
        # Apply data quality rules
        quality_rules = """
        Rules = [
            Completeness "customer_id" > 0.98,
            Uniqueness "transaction_id" > 0.99,
            ColumnValues "amount" > 0,
            ColumnDataType "email" = "string",
            CustomSql "SELECT COUNT(*) FROM primary WHERE created_date >= current_date - 1" > 100
        ]
        """
        
        # Process each dataset
        datasets = ["sales", "customers", "products"]
        
        for dataset in datasets:
            source_frame = glueContext.create_dynamic_frame.from_catalog(
                database="processed_db",
                table_name=dataset
            )
            
            # Apply data quality
            quality_result = EvaluateDataQuality.apply(
                frame=source_frame,
                ruleset=quality_rules
            )
            
            # Separate good and bad records
            good_records = quality_result["rowLevelOutcomes"] \
                .filter(col("DataQualityEvaluationResult") == "Passed")
            
            bad_records = quality_result["rowLevelOutcomes"] \
                .filter(col("DataQualityEvaluationResult") == "Failed")
            
            # Write good records to curated layer
            good_records.write \
                .partitionBy("year", "month") \
                .mode("overwrite") \
                .parquet(f"s3://curated/{dataset}/")
            
            # Write bad records to quarantine
            bad_records.write \
                .partitionBy("year", "month", "day") \
                .mode("append") \
                .parquet(f"s3://quarantine/{dataset}/")
    
    # Curated Layer - Business Logic and Aggregations
    def process_curated_layer():
        # Create business-ready datasets
        customers_df = spark.read.parquet("s3://curated/customers/")
        orders_df = spark.read.parquet("s3://curated/orders/")
        products_df = spark.read.parquet("s3://curated/products/")
        
        # Customer 360 view
        customer_360 = customers_df.alias("c") \
            .join(orders_df.alias("o"), "customer_id") \
            .join(products_df.alias("p"), "product_id") \
            .groupBy("c.customer_id", "c.customer_name", "c.segment") \
            .agg(
                count("o.order_id").alias("total_orders"),
                sum("o.amount").alias("lifetime_value"),
                avg("o.amount").alias("avg_order_value"),
                max("o.order_date").alias("last_order_date"),
                collect_set("p.category").alias("purchased_categories")
            )
        
        # Write to analytics layer
        customer_360.write \
            .mode("overwrite") \
            .parquet("s3://analytics/customer_360/")
        
        # Update Data Catalog
        glue.create_table(
            DatabaseName='analytics_db',
            TableInput={
                'Name': 'customer_360',
                'StorageDescriptor': {
                    'Location': 's3://analytics/customer_360/',
                    'InputFormat': 'org.apache.hadoop.mapred.TextInputFormat',
                    'OutputFormat': 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat',
                    'SerdeInfo': {
                        'SerializationLibrary': 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
                    }
                }
            }
        )

# 2. Data Governance Implementation
def implement_data_governance():
    # Data lineage tracking
    lineage_metadata = {
        "job_name": args['JOB_NAME'],
        "source_tables": ["raw.sales", "raw.customers"],
        "target_tables": ["curated.customer_360"],
        "transformation_logic": "customer aggregation with lifetime value calculation",
        "execution_timestamp": datetime.now().isoformat()
    }
    
    # Store lineage in DynamoDB
    dynamodb = boto3.resource('dynamodb')
    lineage_table = dynamodb.Table('data_lineage')
    
    lineage_table.put_item(Item=lineage_metadata)
    
    # Data classification
    def classify_data(df, table_name):
        sensitive_columns = []
        
        for column in df.columns:
            if any(keyword in column.lower() for keyword in ['ssn', 'credit_card', 'phone', 'email']):
                sensitive_columns.append(column)
        
        # Tag sensitive data
        if sensitive_columns:
            glue.tag_resource(
                ResourceArn=f"arn:aws:glue:region:account:table/{table_name}",
                TagsToAdd={
                    'DataClassification': 'Sensitive',
                    'SensitiveColumns': ','.join(sensitive_columns)
                }
            )
```

### 17. How do you implement real-time streaming ETL with AWS Glue?

**Answer**: Use Glue Streaming to process real-time data from Kinesis, Kafka, or other streaming sources.

```python
# 1. Glue Streaming Job Implementation
def implement_streaming_etl():
    # Streaming job configuration
    streaming_job_config = {
        'Name': 'real-time-etl-job',
        'Role': 'arn:aws:iam::account:role/GlueStreamingRole',
        'Command': {
            'Name': 'gluestreaming',
            'ScriptLocation': 's3://scripts/streaming-etl.py',
            'PythonVersion': '3'
        },
        'DefaultArguments': {
            '--TempDir': 's3://temp-bucket/streaming/',
            '--enable-metrics': '',
            '--enable-continuous-cloudwatch-log': 'true',
            '--job-bookmark-option': 'job-bookmark-enable'
        },
        'WorkerType': 'G.1X',
        'NumberOfWorkers': 5,
        'GlueVersion': '4.0'
    }
    
    # Streaming ETL logic
    def streaming_etl_logic():
        # Read from Kinesis stream
        kinesis_stream = glueContext.create_data_frame.from_options(
            connection_type="kinesis",
            connection_options={
                "streamName": "transaction-stream",
                "startingPosition": "TRIM_HORIZON",
                "inferSchema": "true",
                "classification": "json"
            }
        )
        
        # Process streaming data
        def process_batch(batch_df, batch_id):
            if batch_df.count() > 0:
                # Data transformations
                transformed_df = batch_df \
                    .withColumn("processing_timestamp", current_timestamp()) \
                    .withColumn("batch_id", lit(batch_id))
                
                # Apply business logic
                enriched_df = enrich_transaction_data(transformed_df)
                
                # Write to multiple sinks
                # 1. Real-time analytics (DynamoDB)
                write_to_dynamodb(enriched_df)
                
                # 2. Data lake (S3)
                enriched_df.write \
                    .format("parquet") \
                    .mode("append") \
                    .option("path", "s3://streaming-data/transactions/") \
                    .save()
                
                # 3. Real-time dashboard (ElasticSearch)
                write_to_elasticsearch(enriched_df)
                
                print(f"Processed batch {batch_id} with {batch_df.count()} records")
        
        # Start streaming query
        streaming_query = kinesis_stream.writeStream \
            .foreachBatch(process_batch) \
            .outputMode("append") \
            .option("checkpointLocation", "s3://checkpoints/streaming-etl/") \
            .trigger(processingTime='30 seconds') \
            .start()
        
        streaming_query.awaitTermination()

# 2. Advanced streaming patterns
def advanced_streaming_patterns():
    # Windowed aggregations
    def windowed_aggregations():
        from pyspark.sql.functions import window, sum, count, avg
        
        # Read streaming data
        stream_df = spark.readStream \
            .format("kinesis") \
            .option("streamName", "user-events") \
            .option("region", "us-east-1") \
            .option("initialPosition", "TRIM_HORIZON") \
            .load()
        
        # Parse JSON data
        parsed_df = stream_df.select(
            from_json(col("data").cast("string"), event_schema).alias("event")
        ).select("event.*")
        
        # Windowed aggregations
        windowed_counts = parsed_df \
            .withWatermark("timestamp", "10 minutes") \
            .groupBy(
                window(col("timestamp"), "5 minutes", "1 minute"),
                col("user_id"),
                col("event_type")
            ) \
            .agg(
                count("*").alias("event_count"),
                sum("value").alias("total_value")
            )
        
        # Write aggregated results
        query = windowed_counts.writeStream \
            .outputMode("update") \
            .format("console") \
            .option("truncate", False) \
            .start()
        
        return query
    
    # Stream-to-stream joins
    def stream_joins():
        # User events stream
        user_events = spark.readStream \
            .format("kinesis") \
            .option("streamName", "user-events") \
            .load()
        
        # Transaction stream
        transactions = spark.readStream \
            .format("kinesis") \
            .option("streamName", "transactions") \
            .load()
        
        # Join streams with watermarks
        joined_stream = user_events \
            .withWatermark("event_timestamp", "10 minutes") \
            .join(
                transactions.withWatermark("transaction_timestamp", "5 minutes"),
                expr("""
                    user_id = transaction_user_id AND
                    event_timestamp >= transaction_timestamp AND
                    event_timestamp <= transaction_timestamp + interval 1 hour
                """)
            )
        
        return joined_stream

# 3. Error handling and monitoring in streaming
def streaming_error_handling():
    def robust_streaming_processor():
        try:
            # Main streaming logic
            stream_df = spark.readStream \
                .format("kinesis") \
                .option("streamName", "data-stream") \
                .load()
            
            # Process with error handling
            def process_with_error_handling(batch_df, batch_id):
                try:
                    # Separate valid and invalid records
                    valid_records = batch_df.filter(col("data").isNotNull())
                    invalid_records = batch_df.filter(col("data").isNull())
                    
                    # Process valid records
                    if valid_records.count() > 0:
                        processed_records = transform_data(valid_records)
                        write_to_target(processed_records)
                    
                    # Handle invalid records
                    if invalid_records.count() > 0:
                        write_to_dead_letter_queue(invalid_records, batch_id)
                    
                    # Update metrics
                    update_streaming_metrics(batch_id, valid_records.count(), invalid_records.count())
                    
                except Exception as e:
                    logger.error(f"Error processing batch {batch_id}: {str(e)}")
                    # Send alert
                    send_streaming_alert(batch_id, str(e))
                    # Continue processing (don't fail the entire stream)
            
            # Start streaming with error handling
            query = stream_df.writeStream \
                .foreachBatch(process_with_error_handling) \
                .option("checkpointLocation", "s3://checkpoints/error-handling/") \
                .start()
            
            return query
            
        except Exception as e:
            logger.error(f"Streaming job failed: {str(e)}")
            raise
    
    # Monitoring and alerting
    def setup_streaming_monitoring():
        # CloudWatch custom metrics
        def update_streaming_metrics(batch_id, valid_count, invalid_count):
            cloudwatch = boto3.client('cloudwatch')
            
            cloudwatch.put_metric_data(
                Namespace='Glue/Streaming',
                MetricData=[
                    {
                        'MetricName': 'RecordsProcessed',
                        'Value': valid_count,
                        'Unit': 'Count',
                        'Dimensions': [
                            {'Name': 'JobName', 'Value': args['JOB_NAME']},
                            {'Name': 'BatchId', 'Value': str(batch_id)}
                        ]
                    },
                    {
                        'MetricName': 'InvalidRecords',
                        'Value': invalid_count,
                        'Unit': 'Count',
                        'Dimensions': [
                            {'Name': 'JobName', 'Value': args['JOB_NAME']},
                            {'Name': 'BatchId', 'Value': str(batch_id)}
                        ]
                    }
                ]
            )
```

### 18. How do you implement advanced data partitioning strategies in AWS Glue?

**Answer**: Design optimal partitioning schemes for performance, cost optimization, and query patterns.

```python
# 1. Dynamic partitioning based on data characteristics
def implement_dynamic_partitioning():
    # Analyze data distribution
    def analyze_data_distribution(df):
        # Get data statistics
        total_records = df.count()
        
        # Analyze potential partition columns
        partition_analysis = {}
        
        for column in ['date', 'region', 'category', 'status']:
            if column in df.columns:
                distinct_values = df.select(column).distinct().count()
                avg_records_per_partition = total_records / distinct_values
                
                partition_analysis[column] = {
                    'distinct_values': distinct_values,
                    'avg_records_per_partition': avg_records_per_partition,
                    'recommended': 1000 <= avg_records_per_partition <= 100000
                }
        
        return partition_analysis
    
    # Dynamic partitioning strategy
    def apply_dynamic_partitioning(df, analysis):
        # Select optimal partition columns
        recommended_partitions = [
            col for col, stats in analysis.items() 
            if stats['recommended']
        ]
        
        if not recommended_partitions:
            # Use time-based partitioning as fallback
            if 'timestamp' in df.columns:
                df = df.withColumn('year', year(col('timestamp'))) \
                       .withColumn('month', month(col('timestamp'))) \
                       .withColumn('day', dayofmonth(col('timestamp')))
                recommended_partitions = ['year', 'month', 'day']
        
        # Write with optimal partitioning
        df.write \
            .partitionBy(*recommended_partitions) \
            .mode('overwrite') \
            .parquet('s3://optimized-data/partitioned/')
        
        return recommended_partitions

# 2. Multi-level partitioning with bucketing
def implement_advanced_partitioning():
    # Hierarchical partitioning
    def hierarchical_partitioning(df):
        # Level 1: Time-based (for time-series queries)
        df_with_time_partitions = df \
            .withColumn('year', year(col('order_date'))) \
            .withColumn('month', month(col('order_date'))) \
            .withColumn('day', dayofmonth(col('order_date')))
        
        # Level 2: Business logic partitioning
        df_with_business_partitions = df_with_time_partitions \
            .withColumn('customer_segment', 
                       when(col('total_spent') > 10000, 'premium')
                       .when(col('total_spent') > 1000, 'standard')
                       .otherwise('basic'))
        
        # Level 3: Geographic partitioning
        df_final = df_with_business_partitions \
            .withColumn('region', 
                       when(col('state').isin(['CA', 'OR', 'WA']), 'west')
                       .when(col('state').isin(['NY', 'NJ', 'CT']), 'east')
                       .otherwise('central'))
        
        # Write with multi-level partitioning
        df_final.write \
            .partitionBy('year', 'month', 'customer_segment', 'region') \
            .mode('overwrite') \
            .option('maxRecordsPerFile', 100000) \
            .parquet('s3://data-lake/hierarchical-partitioned/')
    
    # Bucketing for join optimization
    def implement_bucketing(df):
        # Bucket by frequently joined columns
        df.write \
            .bucketBy(10, 'customer_id') \
            .sortBy('order_date') \
            .mode('overwrite') \
            .saveAsTable('bucketed_orders')
        
        # Co-locate related data
        customers_df.write \
            .bucketBy(10, 'customer_id') \
            .mode('overwrite') \
            .saveAsTable('bucketed_customers')

# 3. Partition pruning optimization
def optimize_partition_pruning():
    # Partition elimination strategies
    def partition_aware_queries():
        # Good: Uses partition columns in WHERE clause
        efficient_query = spark.sql("""
            SELECT customer_id, total_amount
            FROM partitioned_orders
            WHERE year = 2024 
            AND month = 12 
            AND region = 'west'
        """)
        
        # Bad: Doesn't use partition columns
        inefficient_query = spark.sql("""
            SELECT customer_id, total_amount
            FROM partitioned_orders
            WHERE customer_name LIKE 'John%'
        """)
        
        return efficient_query
    
    # Dynamic partition pruning
    def dynamic_partition_pruning():
        # Enable dynamic partition pruning
        spark.conf.set("spark.sql.optimizer.dynamicPartitionPruning.enabled", "true")
        
        # Query that benefits from dynamic pruning
        result = spark.sql("""
            SELECT o.order_id, o.amount, c.customer_name
            FROM partitioned_orders o
            JOIN customers c ON o.customer_id = c.customer_id
            WHERE c.registration_date >= '2024-01-01'
            AND o.year = 2024
        """)
        
        return result

# 4. Partition maintenance and optimization
def partition_maintenance():
    # Partition compaction
    def compact_small_partitions():
        # Identify small partitions
        partition_stats = spark.sql("""
            SELECT year, month, day, COUNT(*) as record_count
            FROM partitioned_table
            GROUP BY year, month, day
            HAVING COUNT(*) < 1000
        """)
        
        small_partitions = partition_stats.collect()
        
        for partition in small_partitions:
            # Read small partition
            small_partition_df = spark.read.parquet(
                f"s3://data/year={partition.year}/month={partition.month}/day={partition.day}/"
            )
            
            # Combine with adjacent partitions or rewrite
            if small_partition_df.count() < 100:
                # Move to monthly partition
                small_partition_df.write \
                    .mode('append') \
                    .parquet(f"s3://data/year={partition.year}/month={partition.month}/")
                
                # Delete daily partition
                s3 = boto3.client('s3')
                s3.delete_object(
                    Bucket='data',
                    Key=f"year={partition.year}/month={partition.month}/day={partition.day}/"
                )
    
    # Partition lifecycle management
    def manage_partition_lifecycle():
        from datetime import datetime, timedelta
        
        # Archive old partitions
        cutoff_date = datetime.now() - timedelta(days=365)
        
        old_partitions = spark.sql(f"""
            SELECT DISTINCT year, month
            FROM partitioned_table
            WHERE CONCAT(year, '-', LPAD(month, 2, '0'), '-01') < '{cutoff_date.strftime('%Y-%m-%d')}'
        """)
        
        for partition in old_partitions.collect():
            # Move to archive storage class
            archive_partition(partition.year, partition.month)
            
            # Update catalog to point to archived location
            update_catalog_for_archived_partition(partition.year, partition.month)
    
    # Partition statistics update
    def update_partition_statistics():
        # Analyze table to update statistics
        spark.sql("ANALYZE TABLE partitioned_orders COMPUTE STATISTICS")
        
        # Update partition-level statistics
        spark.sql("""
            ANALYZE TABLE partitioned_orders 
            PARTITION (year=2024, month=12) 
            COMPUTE STATISTICS
        """)
        
        # Update column statistics for cost-based optimization
        spark.sql("""
            ANALYZE TABLE partitioned_orders 
            COMPUTE STATISTICS FOR COLUMNS customer_id, amount, order_date
        """)
```

---

*[Continuing with more advanced questions in the next batch...]*
## Architecture & Performance Questions

### 19. How do you design a scalable AWS Glue architecture for enterprise data processing?

**Answer**: Design a multi-layered architecture with proper resource management, monitoring, and governance.

```python
# Enterprise Glue Architecture
def design_enterprise_architecture():
    # 1. Multi-environment setup
    environments = {
        'dev': {
            'worker_type': 'G.1X',
            'max_workers': 5,
            'max_concurrent_runs': 2
        },
        'staging': {
            'worker_type': 'G.1X',
            'max_workers': 10,
            'max_concurrent_runs': 5
        },
        'prod': {
            'worker_type': 'G.2X',
            'max_workers': 50,
            'max_concurrent_runs': 10
        }
    }
    
    # 2. Job categorization and resource allocation
    job_categories = {
        'light_etl': {
            'worker_type': 'G.1X',
            'worker_count': 2,
            'timeout': 60,
            'max_retries': 1
        },
        'heavy_etl': {
            'worker_type': 'G.2X',
            'worker_count': 20,
            'timeout': 480,
            'max_retries': 2
        },
        'streaming': {
            'worker_type': 'G.1X',
            'worker_count': 10,
            'timeout': None,  # Continuous
            'max_retries': 0
        }
    }
    
    # 3. Centralized configuration management
    def create_job_with_standards(job_name, category, environment):
        env_config = environments[environment]
        job_config = job_categories[category]
        
        return {
            'Name': f"{environment}-{job_name}",
            'Role': f"arn:aws:iam::account:role/GlueRole-{environment}",
            'Command': {
                'Name': 'glueetl',
                'ScriptLocation': f's3://glue-scripts-{environment}/{job_name}.py'
            },
            'DefaultArguments': {
                '--TempDir': f's3://glue-temp-{environment}/',
                '--job-bookmark-option': 'job-bookmark-enable',
                '--enable-metrics': '',
                '--enable-continuous-cloudwatch-log': 'true',
                '--environment': environment,
                '--job-category': category
            },
            'WorkerType': job_config['worker_type'],
            'NumberOfWorkers': min(job_config['worker_count'], env_config['max_workers']),
            'MaxRetries': job_config['max_retries'],
            'Timeout': job_config['timeout'],
            'MaxConcurrentRuns': env_config['max_concurrent_runs'],
            'GlueVersion': '4.0'
        }

# 4. Performance monitoring and auto-scaling
def implement_performance_monitoring():
    # Custom metrics collection
    def collect_job_metrics():
        cloudwatch = boto3.client('cloudwatch')
        
        # Memory utilization tracking
        def track_memory_usage():
            memory_metrics = get_spark_memory_metrics()  # Custom function
            
            cloudwatch.put_metric_data(
                Namespace='Glue/Performance',
                MetricData=[
                    {
                        'MetricName': 'MemoryUtilization',
                        'Value': memory_metrics['used_percentage'],
                        'Unit': 'Percent',
                        'Dimensions': [
                            {'Name': 'JobName', 'Value': args['JOB_NAME']},
                            {'Name': 'WorkerType', 'Value': 'G.2X'}
                        ]
                    }
                ]
            )
        
        # Processing rate tracking
        def track_processing_rate(records_processed, time_taken):
            processing_rate = records_processed / time_taken
            
            cloudwatch.put_metric_data(
                Namespace='Glue/Performance',
                MetricData=[
                    {
                        'MetricName': 'RecordsPerSecond',
                        'Value': processing_rate,
                        'Unit': 'Count/Second',
                        'Dimensions': [
                            {'Name': 'JobName', 'Value': args['JOB_NAME']}
                        ]
                    }
                ]
            )
    
    # Auto-scaling based on metrics
    def implement_auto_scaling():
        # Lambda function for auto-scaling
        auto_scaling_lambda = """
        import boto3
        import json
        
        def lambda_handler(event, context):
            glue = boto3.client('glue')
            cloudwatch = boto3.client('cloudwatch')
            
            job_name = event['job_name']
            
            # Get current job configuration
            job_response = glue.get_job(JobName=job_name)
            current_workers = job_response['Job']['NumberOfWorkers']
            
            # Get memory utilization metrics
            metrics = cloudwatch.get_metric_statistics(
                Namespace='Glue/Performance',
                MetricName='MemoryUtilization',
                Dimensions=[{'Name': 'JobName', 'Value': job_name}],
                StartTime=datetime.utcnow() - timedelta(minutes=10),
                EndTime=datetime.utcnow(),
                Period=300,
                Statistics=['Average']
            )
            
            if metrics['Datapoints']:
                avg_memory = metrics['Datapoints'][-1]['Average']
                
                # Scale up if memory > 80%
                if avg_memory > 80 and current_workers < 50:
                    new_workers = min(current_workers * 2, 50)
                    update_job_workers(job_name, new_workers)
                
                # Scale down if memory < 30%
                elif avg_memory < 30 and current_workers > 2:
                    new_workers = max(current_workers // 2, 2)
                    update_job_workers(job_name, new_workers)
        """
```

### 20. How do you implement data lineage and impact analysis in AWS Glue?

**Answer**: Build comprehensive data lineage tracking using metadata, job dependencies, and automated documentation.

```python
# Data Lineage Implementation
def implement_data_lineage():
    # 1. Automated lineage extraction
    def extract_job_lineage():
        lineage_info = {
            'job_name': args['JOB_NAME'],
            'job_run_id': args.get('JOB_RUN_ID'),
            'start_time': datetime.now().isoformat(),
            'source_tables': [],
            'target_tables': [],
            'transformations': [],
            'dependencies': []
        }
        
        # Track data sources
        def track_data_source(database, table, transformation_ctx):
            source_info = {
                'database': database,
                'table': table,
                'transformation_context': transformation_ctx,
                'access_time': datetime.now().isoformat(),
                'schema': get_table_schema(database, table)
            }
            lineage_info['source_tables'].append(source_info)
        
        # Track data targets
        def track_data_target(path, format, transformation_ctx):
            target_info = {
                'path': path,
                'format': format,
                'transformation_context': transformation_ctx,
                'write_time': datetime.now().isoformat(),
                'record_count': get_record_count(path)
            }
            lineage_info['target_tables'].append(target_info)
        
        # Track transformations
        def track_transformation(transformation_type, input_ctx, output_ctx, logic):
            transform_info = {
                'type': transformation_type,
                'input_context': input_ctx,
                'output_context': output_ctx,
                'logic': logic,
                'timestamp': datetime.now().isoformat()
            }
            lineage_info['transformations'].append(transform_info)
        
        return lineage_info
    
    # 2. Lineage storage and querying
    def store_lineage_metadata(lineage_info):
        # Store in DynamoDB for fast querying
        dynamodb = boto3.resource('dynamodb')
        lineage_table = dynamodb.Table('data_lineage')
        
        # Main lineage record
        lineage_table.put_item(Item=lineage_info)
        
        # Create reverse lookup entries
        for source in lineage_info['source_tables']:
            lineage_table.put_item(Item={
                'pk': f"table#{source['database']}#{source['table']}",
                'sk': f"consumer#{lineage_info['job_name']}#{lineage_info['start_time']}",
                'type': 'consumer',
                'job_name': lineage_info['job_name'],
                'access_pattern': 'read'
            })
        
        for target in lineage_info['target_tables']:
            lineage_table.put_item(Item={
                'pk': f"path#{target['path']}",
                'sk': f"producer#{lineage_info['job_name']}#{lineage_info['start_time']}",
                'type': 'producer',
                'job_name': lineage_info['job_name'],
                'access_pattern': 'write'
            })
    
    # 3. Impact analysis
    def perform_impact_analysis(table_name):
        dynamodb = boto3.resource('dynamodb')
        lineage_table = dynamodb.Table('data_lineage')
        
        # Find all downstream consumers
        downstream_jobs = []
        response = lineage_table.query(
            KeyConditionExpression=Key('pk').eq(f"table#{table_name}")
        )
        
        for item in response['Items']:
            if item['type'] == 'consumer':
                downstream_jobs.append(item['job_name'])
        
        # Recursively find impact
        def find_recursive_impact(job_name, visited=None):
            if visited is None:
                visited = set()
            
            if job_name in visited:
                return []
            
            visited.add(job_name)
            impact_chain = [job_name]
            
            # Find what this job produces
            job_outputs = get_job_outputs(job_name)
            
            for output in job_outputs:
                # Find consumers of this output
                consumers = get_table_consumers(output)
                for consumer in consumers:
                    impact_chain.extend(find_recursive_impact(consumer, visited))
            
            return impact_chain
        
        # Build complete impact analysis
        impact_analysis = {
            'source_table': table_name,
            'direct_consumers': downstream_jobs,
            'impact_chains': []
        }
        
        for job in downstream_jobs:
            chain = find_recursive_impact(job)
            impact_analysis['impact_chains'].append(chain)
        
        return impact_analysis

# 4. Automated documentation generation
def generate_data_documentation():
    # Generate data dictionary
    def generate_data_dictionary():
        glue = boto3.client('glue')
        
        databases = glue.get_databases()['DatabaseList']
        data_dictionary = {}
        
        for db in databases:
            db_name = db['Name']
            tables = glue.get_tables(DatabaseName=db_name)['TableList']
            
            data_dictionary[db_name] = {}
            
            for table in tables:
                table_name = table['Name']
                columns = table['StorageDescriptor']['Columns']
                
                data_dictionary[db_name][table_name] = {
                    'description': table.get('Description', ''),
                    'location': table['StorageDescriptor']['Location'],
                    'format': table['StorageDescriptor']['InputFormat'],
                    'columns': [
                        {
                            'name': col['Name'],
                            'type': col['Type'],
                            'comment': col.get('Comment', '')
                        }
                        for col in columns
                    ],
                    'partitions': table.get('PartitionKeys', []),
                    'last_updated': table.get('UpdateTime', '').isoformat() if table.get('UpdateTime') else ''
                }
        
        # Store documentation
        s3 = boto3.client('s3')
        s3.put_object(
            Bucket='data-documentation',
            Key='data-dictionary.json',
            Body=json.dumps(data_dictionary, indent=2)
        )
    
    # Generate lineage visualization
    def generate_lineage_graph():
        # Create DOT graph for visualization
        dot_graph = """
        digraph data_lineage {
            rankdir=LR;
            node [shape=box];
        """
        
        # Add nodes and edges based on lineage data
        lineage_data = get_all_lineage_data()
        
        for job in lineage_data:
            # Add job node
            dot_graph += f'    "{job["job_name"]}" [shape=ellipse, color=blue];\n'
            
            # Add source nodes and edges
            for source in job['source_tables']:
                table_id = f"{source['database']}.{source['table']}"
                dot_graph += f'    "{table_id}" [color=green];\n'
                dot_graph += f'    "{table_id}" -> "{job["job_name"]}";\n'
            
            # Add target nodes and edges
            for target in job['target_tables']:
                target_id = target['path'].split('/')[-1]
                dot_graph += f'    "{target_id}" [color=red];\n'
                dot_graph += f'    "{job["job_name"]}" -> "{target_id}";\n'
        
        dot_graph += "}"
        
        # Save graph
        s3 = boto3.client('s3')
        s3.put_object(
            Bucket='data-documentation',
            Key='lineage-graph.dot',
            Body=dot_graph
        )
```

---

## Data Catalog & Crawlers Questions

### 21. How do you optimize AWS Glue Crawler performance and cost?

**Answer**: Implement crawler optimization strategies for better performance and cost control.

```python
# Crawler Optimization Strategies
def optimize_crawler_performance():
    # 1. Intelligent crawler configuration
    def configure_optimized_crawler():
        crawler_config = {
            'Name': 'optimized-data-crawler',
            'Role': 'arn:aws:iam::account:role/GlueServiceRole',
            'DatabaseName': 'optimized_db',
            'Targets': {
                'S3Targets': [
                    {
                        'Path': 's3://data-bucket/structured-data/',
                        'Exclusions': [
                            '*.tmp', '*.log', '_*', '*.crc',
                            '*/_temporary/*', '*/temp/*'
                        ],
                        'SampleSize': 1  # Sample only first file for schema
                    }
                ]
            },
            'SchemaChangePolicy': {
                'UpdateBehavior': 'UPDATE_IN_DATABASE',
                'DeleteBehavior': 'LOG'
            },
            'RecrawlPolicy': {
                'RecrawlBehavior': 'CRAWL_NEW_FOLDERS_ONLY'
            },
            'LineageConfiguration': {
                'CrawlerLineageSettings': 'DISABLE'  # Disable if not needed
            },
            'Configuration': json.dumps({
                "Version": 1.0,
                "CrawlerOutput": {
                    "Partitions": {"AddOrUpdateBehavior": "InheritFromTable"},
                    "Tables": {"AddOrUpdateBehavior": "MergeNewColumns"}
                },
                "Grouping": {
                    "TableGroupingPolicy": "CombineCompatibleSchemas"
                }
            })
        }
        
        return crawler_config
    
    # 2. Incremental crawling strategy
    def implement_incremental_crawling():
        # Custom logic to crawl only new partitions
        def crawl_new_partitions_only():
            s3 = boto3.client('s3')
            glue = boto3.client('glue')
            
            # Get last crawl time
            crawler_name = 'incremental-crawler'
            try:
                crawler_info = glue.get_crawler(Name=crawler_name)
                last_crawl = crawler_info['Crawler']['LastCrawl']['StartTime']
            except:
                last_crawl = datetime.min
            
            # List new objects since last crawl
            bucket = 'data-bucket'
            prefix = 'partitioned-data/'
            
            new_prefixes = set()
            paginator = s3.get_paginator('list_objects_v2')
            
            for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
                if 'Contents' in page:
                    for obj in page['Contents']:
                        if obj['LastModified'] > last_crawl:
                            # Extract partition path
                            partition_path = '/'.join(obj['Key'].split('/')[:-1])
                            new_prefixes.add(f"s3://{bucket}/{partition_path}/")
            
            # Update crawler targets with only new prefixes
            if new_prefixes:
                glue.update_crawler(
                    Name=crawler_name,
                    Targets={
                        'S3Targets': [
                            {'Path': path} for path in new_prefixes
                        ]
                    }
                )
                
                # Start crawler
                glue.start_crawler(Name=crawler_name)
                
                return len(new_prefixes)
            
            return 0
    
    # 3. Cost optimization techniques
    def optimize_crawler_costs():
        # Schedule crawlers during off-peak hours
        def schedule_cost_effective_crawling():
            # Create trigger for off-peak hours (2 AM)
            trigger_config = {
                'Name': 'cost-effective-crawler-trigger',
                'Type': 'SCHEDULED',
                'Schedule': 'cron(0 2 * * ? *)',  # 2 AM daily
                'Actions': [
                    {
                        'CrawlerName': 'main-data-crawler'
                    }
                ],
                'StartOnCreation': True
            }
            
            return trigger_config
        
        # Batch multiple small datasets
        def batch_small_datasets():
            # Group small datasets into single crawler
            small_datasets = [
                's3://data-bucket/small-dataset-1/',
                's3://data-bucket/small-dataset-2/',
                's3://data-bucket/small-dataset-3/'
            ]
            
            batched_crawler = {
                'Name': 'batched-small-datasets-crawler',
                'Targets': {
                    'S3Targets': [
                        {'Path': path} for path in small_datasets
                    ]
                },
                'Schedule': 'cron(0 3 ? * SUN *)'  # Weekly on Sunday
            }
            
            return batched_crawler

# 4. Advanced crawler patterns
def implement_advanced_crawler_patterns():
    # Schema evolution handling
    def handle_schema_evolution():
        # Custom classifier for complex formats
        custom_classifier = {
            'Name': 'custom-json-classifier',
            'JsonClassifier': {
                'JsonPath': '$.data[*]',  # Extract nested data
            }
        }
        
        glue.create_classifier(**custom_classifier)
        
        # Crawler with custom classifier
        evolution_crawler = {
            'Name': 'schema-evolution-crawler',
            'Classifiers': ['custom-json-classifier'],
            'SchemaChangePolicy': {
                'UpdateBehavior': 'UPDATE_IN_DATABASE',
                'DeleteBehavior': 'DEPRECATE_IN_DATABASE'
            },
            'Configuration': json.dumps({
                "Version": 1.0,
                "CrawlerOutput": {
                    "Tables": {
                        "AddOrUpdateBehavior": "MergeNewColumns"
                    }
                }
            })
        }
        
        return evolution_crawler
    
    # Multi-format data handling
    def handle_multi_format_data():
        # Separate crawlers for different formats
        format_crawlers = {
            'json_crawler': {
                'Name': 'json-data-crawler',
                'Targets': {
                    'S3Targets': [
                        {
                            'Path': 's3://data-bucket/json-data/',
                            'Exclusions': ['*.parquet', '*.csv']
                        }
                    ]
                },
                'Classifiers': ['json-classifier']
            },
            'parquet_crawler': {
                'Name': 'parquet-data-crawler',
                'Targets': {
                    'S3Targets': [
                        {
                            'Path': 's3://data-bucket/parquet-data/',
                            'Exclusions': ['*.json', '*.csv']
                        }
                    ]
                }
            }
        }
        
        return format_crawlers
```

### 22. How do you implement custom classifiers in AWS Glue?

**Answer**: Create custom classifiers to handle specialized data formats and improve schema detection.

```python
# Custom Classifier Implementation
def implement_custom_classifiers():
    # 1. Grok classifier for log files
    def create_grok_classifier():
        grok_pattern = '%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:message}'
        
        grok_classifier = {
            'Name': 'application-log-classifier',
            'GrokClassifier': {
                'Classification': 'application-logs',
                'GrokPattern': grok_pattern,
                'CustomPatterns': """
                    CUSTOM_TIMESTAMP %{YEAR}-%{MONTHNUM}-%{MONTHDAY} %{TIME}
                    ERROR_CODE E[0-9]{4}
                """
            }
        }
        
        glue.create_classifier(**grok_classifier)
        return grok_classifier
    
    # 2. JSON classifier for nested structures
    def create_json_classifier():
        json_classifier = {
            'Name': 'nested-json-classifier',
            'JsonClassifier': {
                'JsonPath': '$.events[*]',  # Extract array elements
            }
        }
        
        glue.create_classifier(**json_classifier)
        return json_classifier
    
    # 3. XML classifier for structured XML
    def create_xml_classifier():
        xml_classifier = {
            'Name': 'xml-data-classifier',
            'XMLClassifier': {
                'Classification': 'xml-data',
                'RowTag': 'record'  # XML element representing a row
            }
        }
        
        glue.create_classifier(**xml_classifier)
        return xml_classifier
    
    # 4. CSV classifier with custom delimiters
    def create_csv_classifier():
        csv_classifier = {
            'Name': 'pipe-delimited-classifier',
            'CsvClassifier': {
                'Delimiter': '|',
                'QuoteSymbol': '"',
                'ContainsHeader': 'PRESENT',
                'Header': ['id', 'name', 'email', 'created_date'],
                'DisableValueTrimming': False,
                'AllowSingleColumn': False
            }
        }
        
        glue.create_classifier(**csv_classifier)
        return csv_classifier

# 5. Testing and validation
def test_custom_classifiers():
    # Test classifier effectiveness
    def validate_classifier_performance():
        # Create test crawler with custom classifier
        test_crawler = {
            'Name': 'classifier-test-crawler',
            'Classifiers': ['application-log-classifier'],
            'Targets': {
                'S3Targets': [
                    {'Path': 's3://test-bucket/sample-logs/'}
                ]
            },
            'DatabaseName': 'test_db'
        }
        
        glue.create_crawler(**test_crawler)
        glue.start_crawler(Name='classifier-test-crawler')
        
        # Monitor crawler results
        def check_crawler_results():
            crawler_state = 'RUNNING'
            while crawler_state == 'RUNNING':
                time.sleep(30)
                response = glue.get_crawler(Name='classifier-test-crawler')
                crawler_state = response['Crawler']['State']
            
            if crawler_state == 'READY':
                # Check created tables
                tables = glue.get_tables(DatabaseName='test_db')
                for table in tables['TableList']:
                    print(f"Table: {table['Name']}")
                    print(f"Classification: {table.get('Parameters', {}).get('classification', 'Unknown')}")
                    print(f"Columns: {len(table['StorageDescriptor']['Columns'])}")
            
            return crawler_state
        
        return check_crawler_results()
```

---

## ETL Jobs & Transformations Questions

### 23. How do you implement complex data transformations using AWS Glue?

**Answer**: Use advanced Spark operations, custom functions, and Glue transforms for complex data processing.

```python
# Complex Data Transformations
def implement_complex_transformations():
    # 1. Advanced aggregations and window functions
    def advanced_aggregations():
        from pyspark.sql.window import Window
        from pyspark.sql.functions import *
        
        # Read source data
        sales_df = glueContext.create_dynamic_frame.from_catalog(
            database="sales_db", table_name="transactions"
        ).toDF()
        
        # Complex aggregations with multiple grouping sets
        monthly_aggregates = sales_df.groupBy(
            year("transaction_date").alias("year"),
            month("transaction_date").alias("month"),
            "product_category",
            "region"
        ).agg(
            sum("amount").alias("total_sales"),
            count("transaction_id").alias("transaction_count"),
            avg("amount").alias("avg_transaction_value"),
            stddev("amount").alias("sales_volatility"),
            collect_list("customer_id").alias("unique_customers")
        )
        
        # Window functions for ranking and running totals
        window_spec = Window.partitionBy("region", "product_category") \
                           .orderBy(col("total_sales").desc())
        
        ranked_sales = monthly_aggregates.withColumn(
            "sales_rank", 
            row_number().over(window_spec)
        ).withColumn(
            "running_total",
            sum("total_sales").over(
                window_spec.rowsBetween(Window.unboundedPreceding, Window.currentRow)
            )
        )
        
        return ranked_sales
    
    # 2. Complex joins and data enrichment
    def complex_joins_and_enrichment():
        # Multiple table joins
        customers_df = glueContext.create_dynamic_frame.from_catalog(
            database="crm_db", table_name="customers"
        ).toDF()
        
        orders_df = glueContext.create_dynamic_frame.from_catalog(
            database="sales_db", table_name="orders"
        ).toDF()
        
        products_df = glueContext.create_dynamic_frame.from_catalog(
            database="inventory_db", table_name="products"
        ).toDF()
        
        # Complex join with multiple conditions
        enriched_orders = orders_df.alias("o") \
            .join(customers_df.alias("c"), 
                  (col("o.customer_id") == col("c.customer_id")) & 
                  (col("o.order_date") >= col("c.registration_date"))) \
            .join(products_df.alias("p"), 
                  col("o.product_id") == col("p.product_id")) \
            .select(
                col("o.order_id"),
                col("o.order_date"),
                col("c.customer_name"),
                col("c.customer_segment"),
                col("p.product_name"),
                col("p.category"),
                col("o.quantity"),
                col("o.unit_price"),
                (col("o.quantity") * col("o.unit_price")).alias("total_amount")
            )
        
        # Add derived columns
        enriched_orders = enriched_orders \
            .withColumn("order_year", year("order_date")) \
            .withColumn("order_quarter", quarter("order_date")) \
            .withColumn("days_since_registration", 
                       datediff("order_date", "registration_date"))
        
        return enriched_orders
    
    # 3. Data quality and cleansing transformations
    def data_quality_transformations():
        # Custom data cleansing functions
        @udf(returnType=StringType())
        def standardize_phone(phone):
            if phone:
                # Remove all non-numeric characters
                digits = ''.join(filter(str.isdigit, phone))
                if len(digits) == 10:
                    return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
                elif len(digits) == 11 and digits[0] == '1':
                    return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
            return None
        
        @udf(returnType=StringType())
        def clean_email(email):
            if email and '@' in email:
                return email.lower().strip()
            return None
        
        @udf(returnType=DoubleType())
        def normalize_amount(amount, currency):
            # Convert to USD based on currency
            exchange_rates = {'EUR': 1.1, 'GBP': 1.3, 'USD': 1.0}
            return amount * exchange_rates.get(currency, 1.0)
        
        # Apply cleansing transformations
        raw_df = glueContext.create_dynamic_frame.from_catalog(
            database="raw_db", table_name="customer_data"
        ).toDF()
        
        cleaned_df = raw_df \
            .withColumn("clean_phone", standardize_phone("phone")) \
            .withColumn("clean_email", clean_email("email")) \
            .withColumn("normalized_amount", normalize_amount("amount", "currency")) \
            .filter(col("clean_email").isNotNull())  # Remove invalid emails
        
        return cleaned_df

# 4. Advanced data reshaping and pivoting
def advanced_data_reshaping():
    # Pivot operations
    def pivot_sales_data():
        sales_df = spark.read.table("monthly_sales")
        
        # Pivot by product category
        pivoted_sales = sales_df.groupBy("year", "month", "region") \
            .pivot("product_category") \
            .agg(sum("sales_amount"))
        
        return pivoted_sales
    
    # Unpivot operations (melt)
    def unpivot_data():
        wide_df = spark.read.table("quarterly_metrics")
        
        # Convert columns to rows
        unpivoted_df = wide_df.select(
            "company_id",
            "year",
            explode(array(
                struct(lit("Q1").alias("quarter"), col("q1_revenue").alias("revenue")),
                struct(lit("Q2").alias("quarter"), col("q2_revenue").alias("revenue")),
                struct(lit("Q3").alias("quarter"), col("q3_revenue").alias("revenue")),
                struct(lit("Q4").alias("quarter"), col("q4_revenue").alias("revenue"))
            )).alias("quarter_data")
        ).select(
            "company_id",
            "year",
            col("quarter_data.quarter"),
            col("quarter_data.revenue")
        )
        
        return unpivoted_df
```

---

*[Continuing with more sections in the next batch...]*