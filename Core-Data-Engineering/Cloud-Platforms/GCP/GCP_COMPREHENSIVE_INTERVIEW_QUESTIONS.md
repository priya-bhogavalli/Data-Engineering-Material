# Google Cloud Platform (GCP) Interview Questions for Data Engineers

## Basic Level Questions

### 1. What are the core GCP services for data engineering and their use cases?
**Answer**: Essential GCP services for data engineering:

**Storage Services**:
- **Cloud Storage**: Object storage for data lakes, backups
- **Persistent Disk**: Block storage for Compute Engine instances
- **Filestore**: Managed NFS file system

**Compute Services**:
- **Compute Engine**: Virtual machines for custom applications
- **Cloud Functions**: Serverless compute for event-driven processing
- **Dataproc**: Managed Hadoop/Spark clusters
- **Cloud Run**: Containerized serverless applications

**Database Services**:
- **Cloud SQL**: Managed relational databases
- **Firestore**: NoSQL document database
- **BigQuery**: Data warehouse and analytics
- **Cloud Spanner**: Globally distributed database

**Analytics Services**:
- **BigQuery**: Serverless data warehouse
- **Dataflow**: Stream and batch processing
- **Pub/Sub**: Real-time messaging
- **Data Studio**: Business intelligence

```python
# Example: Basic GCP SDK usage
from google.cloud import storage, bigquery, pubsub_v1

# Cloud Storage operations
storage_client = storage.Client()
bucket = storage_client.bucket('my-bucket')
blob = bucket.blob('data/file.csv')
blob.upload_from_filename('local_file.csv')

# BigQuery operations
bq_client = bigquery.Client()
query = "SELECT * FROM `project.dataset.table` LIMIT 10"
results = bq_client.query(query)

# Pub/Sub operations
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('project-id', 'topic-name')
publisher.publish(topic_path, b'Hello World!')
```

### 2. How do you design a data lake architecture on GCP?
**Answer**: GCP data lake architecture components:

**Storage Layer (Cloud Storage)**:
```
gs://data-lake-bucket/
├── raw/                    # Raw ingested data
│   ├── year=2024/
│   ├── month=01/
│   └── day=15/
├── processed/              # Cleaned and transformed data
│   ├── bronze/            # Basic cleaning
│   ├── silver/            # Business logic applied
│   └── gold/              # Analytics-ready
├── curated/               # Final datasets
└── archive/               # Historical data
```

**Data Ingestion**:
```python
# Cloud Functions for data ingestion
import functions_framework
from google.cloud import storage, bigquery

@functions_framework.cloud_event
def process_gcs_file(cloud_event):
    data = cloud_event.data
    bucket_name = data['bucket']
    file_name = data['name']
    
    # Process file and load to BigQuery
    client = bigquery.Client()
    
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
    )
    
    uri = f"gs://{bucket_name}/{file_name}"
    table_id = "project.dataset.table"
    
    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )
    
    load_job.result()  # Wait for job to complete
    print(f"Loaded {load_job.output_rows} rows")

# Dataflow pipeline for ETL
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

def run_pipeline():
    options = PipelineOptions([
        '--project=my-project',
        '--region=us-central1',
        '--runner=DataflowRunner',
        '--temp_location=gs://temp-bucket/temp',
        '--staging_location=gs://temp-bucket/staging'
    ])
    
    with beam.Pipeline(options=options) as pipeline:
        (pipeline
         | 'Read from GCS' >> beam.io.ReadFromText('gs://input-bucket/*.csv')
         | 'Parse CSV' >> beam.Map(parse_csv)
         | 'Transform Data' >> beam.Map(transform_data)
         | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
             'project:dataset.table',
             schema='id:INTEGER,name:STRING,amount:FLOAT',
             write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
         ))
```

### 3. How do you implement data security and access control in GCP?
**Answer**: Multi-layered security approach:

**IAM Policies**:
```python
# IAM policy example
from google.cloud import resourcemanager

def set_iam_policy():
    client = resourcemanager.Client()
    project = client.project('my-project')
    
    policy = project.get_iam_policy()
    
    # Add data engineer role
    policy.bindings.append({
        'role': 'roles/bigquery.dataEditor',
        'members': ['user:engineer@company.com']
    })
    
    # Add viewer role for analysts
    policy.bindings.append({
        'role': 'roles/bigquery.dataViewer',
        'members': ['group:analysts@company.com']
    })
    
    project.set_iam_policy(policy)
```

**Cloud Storage Security**:
```python
# Bucket-level security
from google.cloud import storage

def secure_bucket():
    client = storage.Client()
    bucket = client.bucket('secure-data-bucket')
    
    # Enable uniform bucket-level access
    bucket.iam_configuration.uniform_bucket_level_access_enabled = True
    bucket.patch()
    
    # Set lifecycle policy
    lifecycle_rule = {
        'action': {'type': 'SetStorageClass', 'storageClass': 'COLDLINE'},
        'condition': {'age': 30}
    }
    bucket.lifecycle_rules = [lifecycle_rule]
    bucket.patch()
```

**Data Encryption**:
```python
# Customer-managed encryption keys
from google.cloud import kms

def create_crypto_key():
    client = kms.KeyManagementServiceClient()
    
    # Create key ring
    location_name = f"projects/my-project/locations/global"
    key_ring_id = "data-encryption-ring"
    key_ring = {"name": key_ring_id}
    
    key_ring_name = client.create_key_ring(
        request={"parent": location_name, "key_ring_id": key_ring_id, "key_ring": key_ring}
    )
    
    # Create crypto key
    crypto_key = {
        "purpose": kms.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT,
        "version_template": {
            "algorithm": kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
        },
    }
    
    crypto_key_name = client.create_crypto_key(
        request={"parent": key_ring_name.name, "crypto_key_id": "data-key", "crypto_key": crypto_key}
    )
    
    return crypto_key_name.name
```

### 4. How do you monitor and optimize costs in GCP?
**Answer**: Cost optimization strategies:

**Cost Monitoring**:
```python
# Cloud Monitoring for cost alerts
from google.cloud import monitoring_v3

def create_cost_alert():
    client = monitoring_v3.AlertPolicyServiceClient()
    project_name = f"projects/my-project"
    
    alert_policy = monitoring_v3.AlertPolicy(
        display_name="High BigQuery Costs",
        conditions=[
            monitoring_v3.AlertPolicy.Condition(
                display_name="BigQuery cost condition",
                condition_threshold=monitoring_v3.AlertPolicy.Condition.MetricThreshold(
                    filter='resource.type="bigquery_dataset"',
                    comparison=monitoring_v3.ComparisonType.GREATER_THAN,
                    threshold_value=1000.0,
                    duration={"seconds": 300},
                    aggregations=[
                        monitoring_v3.Aggregation(
                            alignment_period={"seconds": 300},
                            per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_RATE,
                        )
                    ],
                ),
            )
        ],
        notification_channels=["projects/my-project/notificationChannels/123"],
    )
    
    created_policy = client.create_alert_policy(
        name=project_name, alert_policy=alert_policy
    )
    return created_policy
```

**Storage Optimization**:
```python
# Cloud Storage lifecycle management
def set_lifecycle_policy():
    client = storage.Client()
    bucket = client.bucket('data-lake-bucket')
    
    lifecycle_rules = [
        {
            'action': {'type': 'SetStorageClass', 'storageClass': 'NEARLINE'},
            'condition': {'age': 30}
        },
        {
            'action': {'type': 'SetStorageClass', 'storageClass': 'COLDLINE'},
            'condition': {'age': 90}
        },
        {
            'action': {'type': 'SetStorageClass', 'storageClass': 'ARCHIVE'},
            'condition': {'age': 365}
        },
        {
            'action': {'type': 'Delete'},
            'condition': {'age': 2555}  # 7 years
        }
    ]
    
    bucket.lifecycle_rules = lifecycle_rules
    bucket.patch()
```

### 5. How do you implement data backup and disaster recovery?
**Answer**: Comprehensive backup and DR strategy:

**Cross-Region Replication**:
```python
# Cloud Storage cross-region replication
def setup_replication():
    client = storage.Client()
    
    # Primary bucket
    primary_bucket = client.bucket('primary-data-bucket')
    primary_bucket.location = 'US-CENTRAL1'
    primary_bucket.create()
    
    # Replica bucket
    replica_bucket = client.bucket('replica-data-bucket')
    replica_bucket.location = 'US-WEST1'
    replica_bucket.create()
    
    # Set up transfer job
    from google.cloud import storage_transfer
    
    transfer_client = storage_transfer.StorageTransferServiceClient()
    
    transfer_job = {
        'description': 'Cross-region backup',
        'project_id': 'my-project',
        'transfer_spec': {
            'gcs_data_source': {
                'bucket_name': 'primary-data-bucket'
            },
            'gcs_data_sink': {
                'bucket_name': 'replica-data-bucket'
            }
        },
        'schedule': {
            'schedule_start_date': {'year': 2024, 'month': 1, 'day': 1},
            'repeat_interval': {'seconds': 86400}  # Daily
        }
    }
    
    response = transfer_client.create_transfer_job(
        parent=f"projects/my-project",
        transfer_job=transfer_job
    )
    return response
```

**BigQuery Backup**:
```python
# BigQuery dataset backup
def backup_bigquery_dataset():
    client = bigquery.Client()
    
    # Export table to Cloud Storage
    dataset_ref = client.dataset('source_dataset')
    table_ref = dataset_ref.table('source_table')
    
    job_config = bigquery.ExtractJobConfig()
    job_config.destination_format = bigquery.DestinationFormat.PARQUET
    
    extract_job = client.extract_table(
        table_ref,
        'gs://backup-bucket/dataset_backup/*.parquet',
        job_config=job_config
    )
    
    extract_job.result()  # Wait for job to complete
    
    # Create backup dataset
    backup_dataset = bigquery.Dataset('my-project.backup_dataset')
    backup_dataset.location = 'US'
    client.create_dataset(backup_dataset)
    
    # Copy table to backup dataset
    copy_config = bigquery.CopyJobConfig()
    copy_job = client.copy_table(
        table_ref,
        'my-project.backup_dataset.source_table',
        job_config=copy_config
    )
    copy_job.result()
```

## Intermediate Level Questions

### 6. How do you implement real-time data processing with GCP Pub/Sub and Dataflow?
**Answer**: Real-time streaming architecture:

**Pub/Sub Setup**:
```python
# Publisher
from google.cloud import pubsub_v1
import json

def publish_messages():
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path('my-project', 'events-topic')
    
    for i in range(100):
        message_data = {
            'user_id': f'user_{i}',
            'event_type': 'click',
            'timestamp': time.time(),
            'value': random.uniform(1, 100)
        }
        
        data = json.dumps(message_data).encode('utf-8')
        future = publisher.publish(topic_path, data)
        print(f'Published message ID: {future.result()}')

# Subscriber
def receive_messages():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path('my-project', 'events-subscription')
    
    def callback(message):
        data = json.loads(message.data.decode('utf-8'))
        process_event(data)
        message.ack()
    
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
```

**Dataflow Streaming Pipeline**:
```python
# Apache Beam streaming pipeline
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

def run_streaming_pipeline():
    options = PipelineOptions([
        '--project=my-project',
        '--region=us-central1',
        '--runner=DataflowRunner',
        '--streaming',
        '--temp_location=gs://temp-bucket/temp'
    ])
    
    with beam.Pipeline(options=options) as pipeline:
        events = (pipeline
                 | 'Read from Pub/Sub' >> beam.io.ReadFromPubSub(
                     topic='projects/my-project/topics/events-topic')
                 | 'Parse JSON' >> beam.Map(json.loads)
                 | 'Add Timestamp' >> beam.Map(add_timestamp)
                 | 'Window' >> beam.WindowInto(
                     beam.window.FixedWindows(60))  # 1-minute windows
                 | 'Group by User' >> beam.GroupBy('user_id')
                 | 'Aggregate' >> beam.Map(aggregate_events)
                 | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
                     'my-project:dataset.aggregated_events',
                     schema='user_id:STRING,event_count:INTEGER,total_value:FLOAT,window_start:TIMESTAMP',
                     write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
                 ))

def add_timestamp(element):
    element['processing_time'] = time.time()
    return element

def aggregate_events(grouped_data):
    user_id, events = grouped_data
    return {
        'user_id': user_id,
        'event_count': len(events),
        'total_value': sum(e['value'] for e in events),
        'window_start': min(e['timestamp'] for e in events)
    }
```

### 7. How do you optimize BigQuery for performance and cost?
**Answer**: BigQuery optimization techniques:

**Query Optimization**:
```sql
-- Partitioned and clustered table
CREATE TABLE `project.dataset.sales_data`
(
  transaction_id STRING,
  customer_id STRING,
  product_id STRING,
  amount NUMERIC,
  transaction_date DATE,
  region STRING
)
PARTITION BY transaction_date
CLUSTER BY customer_id, region;

-- Optimized query with partition pruning
SELECT 
  customer_id,
  SUM(amount) as total_spent,
  COUNT(*) as transaction_count
FROM `project.dataset.sales_data`
WHERE transaction_date BETWEEN '2024-01-01' AND '2024-01-31'  -- Partition pruning
  AND region = 'US'  -- Cluster pruning
GROUP BY customer_id
HAVING total_spent > 1000;

-- Use approximate aggregation for large datasets
SELECT 
  region,
  APPROX_COUNT_DISTINCT(customer_id) as unique_customers,
  APPROX_QUANTILES(amount, 100)[OFFSET(50)] as median_amount
FROM `project.dataset.sales_data`
WHERE transaction_date >= '2024-01-01'
GROUP BY region;
```

**Cost Optimization**:
```python
# BigQuery cost monitoring
def monitor_query_costs():
    client = bigquery.Client()
    
    # Set maximum bytes billed
    job_config = bigquery.QueryJobConfig()
    job_config.maximum_bytes_billed = 1000000000  # 1GB limit
    
    query = """
    SELECT customer_id, SUM(amount) as total
    FROM `project.dataset.large_table`
    GROUP BY customer_id
    """
    
    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
        
        print(f"Query processed {query_job.total_bytes_processed} bytes")
        print(f"Query cost: ${query_job.total_bytes_processed / 1e12 * 5:.2f}")
        
    except Exception as e:
        print(f"Query would exceed cost limit: {e}")

# Materialized views for frequently accessed data
def create_materialized_view():
    client = bigquery.Client()
    
    view_sql = """
    CREATE MATERIALIZED VIEW `project.dataset.daily_sales_summary`
    PARTITION BY DATE(transaction_date)
    CLUSTER BY region
    AS
    SELECT 
      DATE(transaction_date) as date,
      region,
      SUM(amount) as daily_revenue,
      COUNT(*) as transaction_count,
      COUNT(DISTINCT customer_id) as unique_customers
    FROM `project.dataset.sales_data`
    GROUP BY DATE(transaction_date), region
    """
    
    query_job = client.query(view_sql)
    query_job.result()
```

### 8. How do you implement data quality checks in GCP?
**Answer**: Data quality framework using GCP services:

**Cloud Functions for Data Validation**:
```python
import functions_framework
from google.cloud import bigquery
import pandas as pd

@functions_framework.cloud_event
def validate_data_quality(cloud_event):
    data = cloud_event.data
    table_id = f"{data['project']}.{data['dataset']}.{data['table']}"
    
    client = bigquery.Client()
    
    quality_checks = [
        check_null_values,
        check_data_types,
        check_business_rules,
        check_data_freshness
    ]
    
    results = []
    for check in quality_checks:
        result = check(client, table_id)
        results.append(result)
    
    # Send results to monitoring
    send_quality_metrics(results)
    
    return {'status': 'completed', 'checks': len(results)}

def check_null_values(client, table_id):
    query = f"""
    SELECT 
      'null_check' as check_type,
      column_name,
      COUNT(*) as null_count,
      COUNT(*) / (SELECT COUNT(*) FROM `{table_id}`) as null_percentage
    FROM `{table_id}`,
    UNNEST([
      STRUCT('customer_id' as column_name, customer_id as value),
      STRUCT('amount' as column_name, CAST(amount AS STRING) as value)
    ])
    WHERE value IS NULL
    GROUP BY column_name
    """
    
    results = client.query(query).to_dataframe()
    return results

def check_business_rules(client, table_id):
    query = f"""
    SELECT 
      'business_rule' as check_type,
      'negative_amounts' as rule_name,
      COUNT(*) as violation_count
    FROM `{table_id}`
    WHERE amount < 0
    
    UNION ALL
    
    SELECT 
      'business_rule' as check_type,
      'future_dates' as rule_name,
      COUNT(*) as violation_count
    FROM `{table_id}`
    WHERE transaction_date > CURRENT_DATE()
    """
    
    results = client.query(query).to_dataframe()
    return results
```

**Dataflow for Data Profiling**:
```python
# Data profiling pipeline
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

def run_data_profiling():
    options = PipelineOptions([
        '--project=my-project',
        '--region=us-central1',
        '--runner=DataflowRunner'
    ])
    
    with beam.Pipeline(options=options) as pipeline:
        (pipeline
         | 'Read from BigQuery' >> beam.io.ReadFromBigQuery(
             query='SELECT * FROM `project.dataset.table`',
             use_standard_sql=True)
         | 'Profile Data' >> beam.Map(profile_record)
         | 'Aggregate Profiles' >> beam.CombineGlobally(aggregate_profiles)
         | 'Write Results' >> beam.io.WriteToBigQuery(
             'project:dataset.data_profile',
             schema='column:STRING,data_type:STRING,null_count:INTEGER,unique_count:INTEGER',
             write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE
         ))

def profile_record(record):
    profile = {}
    for key, value in record.items():
        profile[key] = {
            'data_type': type(value).__name__,
            'is_null': value is None,
            'value': value
        }
    return profile
```

### 9. How do you implement data lineage and governance in GCP?
**Answer**: Data governance framework:

**Data Catalog Integration**:
```python
# Data Catalog for metadata management
from google.cloud import datacatalog_v1

def create_data_catalog_entry():
    client = datacatalog_v1.DataCatalogClient()
    
    # Create entry group
    location = "us-central1"
    entry_group_id = "data_engineering_group"
    entry_group = datacatalog_v1.EntryGroup()
    entry_group.display_name = "Data Engineering Assets"
    entry_group.description = "Data assets managed by data engineering team"
    
    parent = f"projects/my-project/locations/{location}"
    
    created_entry_group = client.create_entry_group(
        parent=parent,
        entry_group_id=entry_group_id,
        entry_group=entry_group
    )
    
    # Create entry for BigQuery table
    entry = datacatalog_v1.Entry()
    entry.display_name = "Customer Transactions"
    entry.description = "Daily customer transaction data"
    entry.type_ = datacatalog_v1.EntryType.TABLE
    entry.bigquery_table_spec.table_source_type = datacatalog_v1.TableSourceType.BIGQUERY_TABLE
    
    # Add custom metadata
    entry.user_specified_system = "data_pipeline"
    entry.user_specified_type = "fact_table"
    
    created_entry = client.create_entry(
        parent=created_entry_group.name,
        entry_id="customer_transactions",
        entry=entry
    )
    
    # Add tags
    tag_template = create_tag_template(client, location)
    create_tag(client, created_entry.name, tag_template.name)
    
    return created_entry

def create_tag_template(client, location):
    tag_template = datacatalog_v1.TagTemplate()
    tag_template.display_name = "Data Engineering Template"
    
    # Add fields
    tag_template.fields["data_owner"] = datacatalog_v1.TagTemplateField()
    tag_template.fields["data_owner"].display_name = "Data Owner"
    tag_template.fields["data_owner"].type_.primitive_type = datacatalog_v1.FieldType.PrimitiveType.STRING
    
    tag_template.fields["update_frequency"] = datacatalog_v1.TagTemplateField()
    tag_template.fields["update_frequency"].display_name = "Update Frequency"
    tag_template.fields["update_frequency"].type_.primitive_type = datacatalog_v1.FieldType.PrimitiveType.STRING
    
    parent = f"projects/my-project/locations/{location}"
    
    created_template = client.create_tag_template(
        parent=parent,
        tag_template_id="data_engineering_template",
        tag_template=tag_template
    )
    
    return created_template
```

**Lineage Tracking**:
```python
# Custom lineage tracking system
from google.cloud import firestore

class DataLineageTracker:
    def __init__(self):
        self.db = firestore.Client()
    
    def record_transformation(self, job_name, source_tables, target_tables, transformation_logic):
        lineage_doc = {
            'job_name': job_name,
            'timestamp': firestore.SERVER_TIMESTAMP,
            'source_tables': source_tables,
            'target_tables': target_tables,
            'transformation_logic': transformation_logic,
            'status': 'completed'
        }
        
        self.db.collection('data_lineage').add(lineage_doc)
    
    def get_lineage(self, table_name):
        # Get upstream lineage
        upstream_query = self.db.collection('data_lineage').where(
            'target_tables', 'array_contains', table_name
        )
        
        # Get downstream lineage
        downstream_query = self.db.collection('data_lineage').where(
            'source_tables', 'array_contains', table_name
        )
        
        upstream = [doc.to_dict() for doc in upstream_query.stream()]
        downstream = [doc.to_dict() for doc in downstream_query.stream()]
        
        return {
            'upstream': upstream,
            'downstream': downstream
        }

# Usage in Dataflow job
def track_lineage_in_pipeline():
    tracker = DataLineageTracker()
    
    # Record transformation
    tracker.record_transformation(
        job_name='customer-data-processing',
        source_tables=['raw.customers', 'raw.transactions'],
        target_tables=['processed.customer_metrics'],
        transformation_logic='Aggregate transactions by customer, calculate lifetime value'
    )
```

### 10. How do you implement automated data pipeline orchestration?
**Answer**: Pipeline orchestration using GCP services:

**Cloud Composer (Apache Airflow)**:
```python
# Airflow DAG for data pipeline
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyTableOperator
from airflow.providers.google.cloud.operators.dataflow import DataflowTemplatedJobStartOperator
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'data_processing_pipeline',
    default_args=default_args,
    description='Daily data processing pipeline',
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    catchup=False
)

# Wait for input file
wait_for_file = GCSObjectExistenceSensor(
    task_id='wait_for_input_file',
    bucket='input-bucket',
    object='data/{{ ds }}/input.csv',
    timeout=3600,
    poke_interval=300,
    dag=dag
)

# Data validation
validate_data = DataflowTemplatedJobStartOperator(
    task_id='validate_data',
    template='gs://dataflow-templates/latest/Cloud_PubSub_to_BigQuery',
    parameters={
        'inputTopic': 'projects/my-project/topics/validation-topic',
        'outputTableSpec': 'my-project:dataset.validation_results'
    },
    location='us-central1',
    dag=dag
)

# ETL processing
etl_processing = DataflowTemplatedJobStartOperator(
    task_id='etl_processing',
    template='gs://my-templates/etl-template',
    parameters={
        'inputPath': 'gs://input-bucket/data/{{ ds }}/',
        'outputPath': 'gs://output-bucket/processed/{{ ds }}/'
    },
    location='us-central1',
    dag=dag
)

# Load to BigQuery
load_to_bq = BigQueryCreateEmptyTableOperator(
    task_id='load_to_bigquery',
    dataset_id='processed_data',
    table_id='daily_metrics_{{ ds_nodash }}',
    schema_fields=[
        {'name': 'date', 'type': 'DATE', 'mode': 'REQUIRED'},
        {'name': 'metric_value', 'type': 'FLOAT', 'mode': 'NULLABLE'}
    ],
    dag=dag
)

# Set dependencies
wait_for_file >> validate_data >> etl_processing >> load_to_bq
```

**Cloud Functions for Event-Driven Processing**:
```python
# Event-driven pipeline with Cloud Functions
import functions_framework
from google.cloud import workflows_v1

@functions_framework.cloud_event
def trigger_pipeline(cloud_event):
    data = cloud_event.data
    
    if data['eventType'] == 'google.storage.object.finalize':
        bucket_name = data['bucketId']
        file_name = data['objectId']
        
        # Trigger workflow
        client = workflows_v1.WorkflowsClient()
        
        execution = {
            'argument': json.dumps({
                'bucket': bucket_name,
                'file': file_name,
                'timestamp': data['timeCreated']
            })
        }
        
        parent = f"projects/my-project/locations/us-central1/workflows/data-pipeline"
        
        response = client.create_execution(
            parent=parent,
            execution=execution
        )
        
        return {'execution_id': response.name}

# Workflow definition (YAML)
workflow_definition = """
main:
  params: [args]
  steps:
    - validate_input:
        call: http.post
        args:
          url: https://us-central1-my-project.cloudfunctions.net/validate-data
          body: ${args}
        result: validation_result
    
    - check_validation:
        switch:
          - condition: ${validation_result.body.valid == true}
            next: process_data
        next: send_error_notification
    
    - process_data:
        call: http.post
        args:
          url: https://us-central1-my-project.cloudfunctions.net/process-data
          body: ${args}
        result: processing_result
    
    - load_to_warehouse:
        call: http.post
        args:
          url: https://us-central1-my-project.cloudfunctions.net/load-data
          body: ${processing_result.body}
    
    - send_success_notification:
        call: http.post
        args:
          url: https://us-central1-my-project.cloudfunctions.net/send-notification
          body:
            status: "success"
            message: "Pipeline completed successfully"
        next: end
    
    - send_error_notification:
        call: http.post
        args:
          url: https://us-central1-my-project.cloudfunctions.net/send-notification
          body:
            status: "error"
            message: "Pipeline failed validation"
"""
```

## Advanced Level Questions

### 11. How do you implement multi-region data replication and disaster recovery?
**Answer**: Enterprise-grade DR architecture:

**Multi-Region Setup**:
```python
# Deployment Manager template for multi-region infrastructure
deployment_config = {
    "resources": [
        {
            "name": "primary-dataset",
            "type": "bigquery.v2.dataset",
            "properties": {
                "datasetReference": {
                    "datasetId": "primary_dataset",
                    "projectId": "my-project"
                },
                "location": "US",
                "friendlyName": "Primary Dataset"
            }
        },
        {
            "name": "replica-dataset",
            "type": "bigquery.v2.dataset", 
            "properties": {
                "datasetReference": {
                    "datasetId": "replica_dataset",
                    "projectId": "my-project"
                },
                "location": "EU",
                "friendlyName": "Replica Dataset"
            }
        },
        {
            "name": "primary-bucket",
            "type": "storage.v1.bucket",
            "properties": {
                "name": "primary-data-bucket",
                "location": "US-CENTRAL1",
                "storageClass": "STANDARD"
            }
        },
        {
            "name": "replica-bucket",
            "type": "storage.v1.bucket",
            "properties": {
                "name": "replica-data-bucket", 
                "location": "EUROPE-WEST1",
                "storageClass": "STANDARD"
            }
        }
    ]
}

# Cross-region replication job
def setup_cross_region_replication():
    from google.cloud import storage_transfer
    
    client = storage_transfer.StorageTransferServiceClient()
    
    transfer_job = {
        'description': 'Cross-region data replication',
        'project_id': 'my-project',
        'transfer_spec': {
            'gcs_data_source': {
                'bucket_name': 'primary-data-bucket'
            },
            'gcs_data_sink': {
                'bucket_name': 'replica-data-bucket'
            },
            'transfer_options': {
                'overwrite_objects_already_existing_in_sink': False,
                'delete_objects_unique_in_sink': False
            }
        },
        'schedule': {
            'schedule_start_date': {'year': 2024, 'month': 1, 'day': 1},
            'repeat_interval': {'seconds': 3600}  # Hourly
        },
        'status': 'ENABLED'
    }
    
    response = client.create_transfer_job(
        parent=f"projects/my-project",
        transfer_job=transfer_job
    )
    
    return response
```

**Automated Failover**:
```python
# Health check and failover automation
from google.cloud import monitoring_v3
from google.cloud import dns

def setup_automated_failover():
    # Create health check
    monitoring_client = monitoring_v3.UptimeCheckServiceClient()
    
    uptime_check_config = monitoring_v3.UptimeCheckConfig(
        display_name="Primary Region Health Check",
        monitored_resource=monitoring_v3.MonitoredResource(
            type="uptime_url",
            labels={"host": "primary-api.company.com"}
        ),
        http_check=monitoring_v3.UptimeCheckConfig.HttpCheck(
            path="/health",
            port=443,
            use_ssl=True
        ),
        timeout={"seconds": 10},
        period={"seconds": 60}
    )
    
    project_name = f"projects/my-project"
    created_check = monitoring_client.create_uptime_check_config(
        parent=project_name,
        uptime_check_config=uptime_check_config
    )
    
    # Create alert policy for failover
    alert_client = monitoring_v3.AlertPolicyServiceClient()
    
    alert_policy = monitoring_v3.AlertPolicy(
        display_name="Primary Region Down - Trigger Failover",
        conditions=[
            monitoring_v3.AlertPolicy.Condition(
                display_name="Uptime check failure",
                condition_threshold=monitoring_v3.AlertPolicy.Condition.MetricThreshold(
                    filter=f'resource.type="uptime_url" AND metric.type="monitoring.googleapis.com/uptime_check/check_passed"',
                    comparison=monitoring_v3.ComparisonType.LESS_THAN,
                    threshold_value=1.0,
                    duration={"seconds": 300}
                )
            )
        ],
        notification_channels=[
            f"projects/my-project/notificationChannels/{webhook_channel_id}"
        ]
    )
    
    created_policy = alert_client.create_alert_policy(
        name=project_name,
        alert_policy=alert_policy
    )
    
    return created_policy

# Cloud Function for DNS failover
@functions_framework.http
def handle_failover(request):
    dns_client = dns.Client()
    zone = dns_client.zone('company-com')
    
    # Update DNS to point to secondary region
    changes = zone.changes()
    
    # Remove primary record
    primary_record = zone.resource_record_set(
        'api.company.com.', 'A', 300, ['1.2.3.4']
    )
    changes.delete_record_set(primary_record)
    
    # Add secondary record
    secondary_record = zone.resource_record_set(
        'api.company.com.', 'A', 60, ['5.6.7.8']  # Secondary region IP
    )
    changes.add_record_set(secondary_record)
    
    changes.create()
    
    return {'status': 'failover_completed', 'timestamp': time.time()}
```

### 12. How do you implement advanced security and compliance?
**Answer**: Enterprise security framework:

**VPC Security**:
```python
# VPC and firewall configuration
vpc_config = {
    "resources": [
        {
            "name": "data-vpc",
            "type": "compute.v1.network",
            "properties": {
                "name": "data-engineering-vpc",
                "autoCreateSubnetworks": False
            }
        },
        {
            "name": "private-subnet",
            "type": "compute.v1.subnetwork",
            "properties": {
                "name": "private-data-subnet",
                "network": "$(ref.data-vpc.selfLink)",
                "ipCidrRange": "10.0.1.0/24",
                "region": "us-central1",
                "privateIpGoogleAccess": True
            }
        },
        {
            "name": "data-firewall",
            "type": "compute.v1.firewall",
            "properties": {
                "name": "allow-data-processing",
                "network": "$(ref.data-vpc.selfLink)",
                "allowed": [
                    {
                        "IPProtocol": "tcp",
                        "ports": ["443", "8080"]
                    }
                ],
                "sourceRanges": ["10.0.0.0/8"],
                "targetTags": ["data-processing"]
            }
        }
    ]
}

# Private Google Access for secure API calls
def setup_private_google_access():
    from google.cloud import compute_v1
    
    client = compute_v1.SubnetworksClient()
    
    # Enable private Google access
    request = compute_v1.SetPrivateIpGoogleAccessSubnetworkRequest(
        project="my-project",
        region="us-central1",
        subnetwork="private-data-subnet",
        subnetworks_set_private_ip_google_access_request_resource=compute_v1.SubnetworksSetPrivateIpGoogleAccessRequest(
            private_ip_google_access=True
        )
    )
    
    operation = client.set_private_ip_google_access(request=request)
    return operation
```

**Data Loss Prevention (DLP)**:
```python
# Cloud DLP for sensitive data detection
from google.cloud import dlp_v2

def setup_dlp_inspection():
    dlp_client = dlp_v2.DlpServiceClient()
    project = f"projects/my-project"
    
    # Create inspection template
    info_types = [
        {"name": "EMAIL_ADDRESS"},
        {"name": "PHONE_NUMBER"},
        {"name": "CREDIT_CARD_NUMBER"},
        {"name": "US_SOCIAL_SECURITY_NUMBER"}
    ]
    
    inspect_config = {
        "info_types": info_types,
        "min_likelihood": dlp_v2.Likelihood.POSSIBLE,
        "limits": {"max_findings_per_request": 100}
    }
    
    inspect_template = {
        "inspect_config": inspect_config,
        "display_name": "PII Detection Template"
    }
    
    response = dlp_client.create_inspect_template(
        parent=project,
        inspect_template=inspect_template
    )
    
    return response

# DLP job for BigQuery scanning
def scan_bigquery_table():
    dlp_client = dlp_v2.DlpServiceClient()
    
    # Configure BigQuery storage
    storage_config = {
        "big_query_options": {
            "table_reference": {
                "project_id": "my-project",
                "dataset_id": "sensitive_data",
                "table_id": "customer_info"
            }
        }
    }
    
    # Configure inspection
    inspect_config = {
        "info_types": [{"name": "EMAIL_ADDRESS"}, {"name": "PHONE_NUMBER"}],
        "min_likelihood": dlp_v2.Likelihood.LIKELY
    }
    
    # Configure actions
    actions = [
        {
            "save_findings": {
                "output_config": {
                    "table": {
                        "project_id": "my-project",
                        "dataset_id": "dlp_results",
                        "table_id": "findings"
                    }
                }
            }
        }
    ]
    
    inspect_job = {
        "inspect_config": inspect_config,
        "storage_config": storage_config,
        "actions": actions
    }
    
    parent = f"projects/my-project/locations/global"
    
    response = dlp_client.create_dlp_job(
        parent=parent,
        inspect_job=inspect_job
    )
    
    return response
```

This comprehensive GCP documentation covers all major services and advanced patterns used in data engineering, providing practical examples and real-world implementation strategies for building robust, scalable, and cost-effective data platforms on Google Cloud Platform.