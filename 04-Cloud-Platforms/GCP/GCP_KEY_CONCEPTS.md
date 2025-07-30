# Google Cloud Platform (GCP) Key Concepts

## 1. GCP Data Services Overview
**Core Data Services**:
- **BigQuery**: Serverless data warehouse
- **Cloud Storage**: Object storage service
- **Dataflow**: Stream and batch processing
- **Cloud SQL**: Managed relational databases
- **Firestore**: NoSQL document database
- **Pub/Sub**: Messaging service
- **Dataproc**: Managed Spark and Hadoop

```python
from google.cloud import bigquery, storage
from google.oauth2 import service_account

# Authentication
credentials = service_account.Credentials.from_service_account_file(
    'path/to/service-account-key.json'
)

# Initialize clients
bq_client = bigquery.Client(credentials=credentials, project='my-project')
storage_client = storage.Client(credentials=credentials)
```

## 2. BigQuery
```python
from google.cloud import bigquery
import pandas as pd

# Create dataset
dataset_id = f"{project_id}.sales_data"
dataset = bigquery.Dataset(dataset_id)
dataset.location = "US"
dataset = bq_client.create_dataset(dataset, exists_ok=True)

# Create table with schema
schema = [
    bigquery.SchemaField("customer_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("product_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("amount", "FLOAT", mode="REQUIRED"),
    bigquery.SchemaField("sale_date", "DATE", mode="REQUIRED"),
    bigquery.SchemaField("metadata", "JSON", mode="NULLABLE")
]

table_id = f"{project_id}.sales_data.transactions"
table = bigquery.Table(table_id, schema=schema)
table = bq_client.create_table(table, exists_ok=True)

# Query data
query = """
    SELECT 
        customer_id,
        SUM(amount) as total_spent,
        COUNT(*) as transaction_count,
        AVG(amount) as avg_transaction
    FROM `my-project.sales_data.transactions`
    WHERE sale_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
    GROUP BY customer_id
    HAVING total_spent > 1000
    ORDER BY total_spent DESC
"""

query_job = bq_client.query(query)
results = query_job.result()

# Convert to DataFrame
df = results.to_dataframe()

# Parameterized queries
query_with_params = """
    SELECT *
    FROM `my-project.sales_data.transactions`
    WHERE sale_date BETWEEN @start_date AND @end_date
    AND amount > @min_amount
"""

job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("start_date", "DATE", "2024-01-01"),
        bigquery.ScalarQueryParameter("end_date", "DATE", "2024-01-31"),
        bigquery.ScalarQueryParameter("min_amount", "FLOAT", 100.0)
    ]
)

query_job = bq_client.query(query_with_params, job_config=job_config)
```

```sql
-- BigQuery SQL features
-- Window functions
SELECT 
    customer_id,
    sale_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id 
        ORDER BY sale_date 
        ROWS UNBOUNDED PRECEDING
    ) as running_total,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id 
        ORDER BY amount DESC
    ) as amount_rank
FROM `project.dataset.sales`;

-- Array and struct operations
SELECT 
    customer_id,
    ARRAY_AGG(
        STRUCT(product_id, amount, sale_date)
        ORDER BY sale_date DESC
        LIMIT 5
    ) as recent_purchases
FROM `project.dataset.sales`
GROUP BY customer_id;

-- JSON functions
SELECT 
    customer_id,
    JSON_EXTRACT_SCALAR(metadata, '$.source') as source,
    JSON_EXTRACT_ARRAY(metadata, '$.tags') as tags
FROM `project.dataset.sales`
WHERE JSON_EXTRACT_SCALAR(metadata, '$.verified') = 'true';

-- Machine Learning
CREATE OR REPLACE MODEL `project.dataset.customer_segmentation`
OPTIONS(
    model_type='kmeans',
    num_clusters=4
) AS
SELECT 
    total_spent,
    transaction_count,
    avg_amount,
    days_since_last_purchase
FROM `project.dataset.customer_features`;

-- Predict using ML model
SELECT 
    customer_id,
    predicted_cluster,
    CENTROID_ID(predicted_cluster) as cluster_id
FROM ML.PREDICT(
    MODEL `project.dataset.customer_segmentation`,
    (SELECT * FROM `project.dataset.new_customers`)
);
```

## 3. Cloud Storage
```python
from google.cloud import storage
import json

# Create bucket
bucket_name = "my-data-lake-bucket"
bucket = storage_client.bucket(bucket_name)
bucket.location = "US"
bucket = storage_client.create_bucket(bucket, location="US")

# Upload file
blob = bucket.blob("raw-data/sales/2024/01/sales.csv")
blob.upload_from_filename("local_sales.csv")

# Set metadata
blob.metadata = {
    "source": "sales_system",
    "processed": "false",
    "upload_date": "2024-01-15"
}
blob.patch()

# Download file
blob = bucket.blob("processed-data/sales_summary.json")
content = blob.download_as_text()
data = json.loads(content)

# List objects with prefix
blobs = storage_client.list_blobs(bucket_name, prefix="raw-data/sales/")
for blob in blobs:
    print(f"File: {blob.name}, Size: {blob.size}, Created: {blob.time_created}")

# Lifecycle management
from google.cloud.storage import LifecycleRuleConditions, LifecycleRuleAction

rule = {
    "action": {"type": "SetStorageClass", "storageClass": "NEARLINE"},
    "condition": {"age": 30}
}

bucket.lifecycle_rules = [rule]
bucket.patch()

# Signed URLs for temporary access
from datetime import datetime, timedelta

url = blob.generate_signed_url(
    version="v4",
    expiration=datetime.utcnow() + timedelta(hours=1),
    method="GET"
)
```

## 4. Dataflow (Apache Beam)
```python
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromText, WriteToText

# Pipeline options
options = PipelineOptions([
    '--project=my-project',
    '--region=us-central1',
    '--runner=DataflowRunner',
    '--temp_location=gs://my-bucket/temp',
    '--staging_location=gs://my-bucket/staging'
])

# Batch processing pipeline
def run_batch_pipeline():
    with beam.Pipeline(options=options) as pipeline:
        (pipeline
         | 'Read CSV' >> ReadFromText('gs://my-bucket/input/*.csv')
         | 'Parse CSV' >> beam.Map(parse_csv_line)
         | 'Filter Valid' >> beam.Filter(lambda x: x['amount'] > 0)
         | 'Add Timestamp' >> beam.Map(add_processing_timestamp)
         | 'Group by Customer' >> beam.GroupBy(lambda x: x['customer_id'])
         | 'Calculate Totals' >> beam.Map(calculate_customer_totals)
         | 'Format Output' >> beam.Map(format_json_output)
         | 'Write Results' >> WriteToText('gs://my-bucket/output/results'))

def parse_csv_line(line):
    fields = line.split(',')
    return {
        'customer_id': fields[0],
        'product_id': fields[1],
        'amount': float(fields[2]),
        'sale_date': fields[3]
    }

# Streaming pipeline
def run_streaming_pipeline():
    with beam.Pipeline(options=options) as pipeline:
        (pipeline
         | 'Read from Pub/Sub' >> beam.io.ReadFromPubSub(
             subscription='projects/my-project/subscriptions/sales-events'
         )
         | 'Parse JSON' >> beam.Map(json.loads)
         | 'Window into Fixed Intervals' >> beam.WindowInto(
             beam.window.FixedWindows(60)  # 1-minute windows
         )
         | 'Group by Product' >> beam.GroupBy(lambda x: x['product_id'])
         | 'Count Sales' >> beam.Map(lambda x: {
             'product_id': x[0],
             'count': len(x[1]),
             'total_amount': sum(item['amount'] for item in x[1])
         })
         | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
             'my-project:dataset.streaming_results',
             schema='product_id:STRING,count:INTEGER,total_amount:FLOAT',
             write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
         ))

# Custom transforms
class CalculateMetrics(beam.DoFn):
    def process(self, element):
        # Complex processing logic
        metrics = {
            'customer_id': element['customer_id'],
            'total_spent': sum(t['amount'] for t in element['transactions']),
            'avg_amount': sum(t['amount'] for t in element['transactions']) / len(element['transactions']),
            'transaction_count': len(element['transactions'])
        }
        yield metrics
```

## 5. Cloud Pub/Sub
```python
from google.cloud import pubsub_v1
import json

# Publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, 'sales-events')

# Create topic
try:
    topic = publisher.create_topic(request={"name": topic_path})
    print(f"Created topic: {topic.name}")
except Exception as e:
    print(f"Topic may already exist: {e}")

# Publish messages
def publish_sales_event(customer_id, product_id, amount):
    message_data = {
        'customer_id': customer_id,
        'product_id': product_id,
        'amount': amount,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    # Convert to bytes
    data = json.dumps(message_data).encode('utf-8')
    
    # Publish with attributes
    future = publisher.publish(
        topic_path, 
        data,
        source='sales_system',
        event_type='purchase'
    )
    
    message_id = future.result()
    print(f"Published message ID: {message_id}")

# Batch publishing
def publish_batch(messages):
    futures = []
    
    for message in messages:
        data = json.dumps(message).encode('utf-8')
        future = publisher.publish(topic_path, data)
        futures.append(future)
    
    # Wait for all messages to be published
    for future in futures:
        message_id = future.result()
        print(f"Published: {message_id}")

# Subscriber
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, 'sales-events-sub')

# Create subscription
try:
    subscription = subscriber.create_subscription(
        request={
            "name": subscription_path,
            "topic": topic_path,
            "ack_deadline_seconds": 60
        }
    )
except Exception as e:
    print(f"Subscription may already exist: {e}")

# Message handler
def callback(message):
    try:
        # Process message
        data = json.loads(message.data.decode('utf-8'))
        print(f"Received: {data}")
        
        # Process the sales event
        process_sales_event(data)
        
        # Acknowledge message
        message.ack()
        
    except Exception as e:
        print(f"Error processing message: {e}")
        message.nack()

# Pull messages
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
```

## 6. Cloud SQL and Firestore
```python
# Cloud SQL (PostgreSQL)
import sqlalchemy
from google.cloud.sql.connector import Connector

def create_connection_pool():
    connector = Connector()
    
    def getconn():
        conn = connector.connect(
            "my-project:us-central1:my-instance",
            "pg8000",
            user="postgres",
            password="password",
            db="sales_db"
        )
        return conn
    
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        pool_size=5,
        max_overflow=2,
        pool_pre_ping=True,
        pool_recycle=300,
    )
    return pool

# Firestore (NoSQL)
from google.cloud import firestore

db = firestore.Client()

# Add document
doc_ref = db.collection('customers').document('customer_123')
doc_ref.set({
    'name': 'John Doe',
    'email': 'john@example.com',
    'total_spent': 1250.50,
    'last_purchase': firestore.SERVER_TIMESTAMP,
    'preferences': {
        'newsletter': True,
        'category': 'electronics'
    }
})

# Query documents
customers_ref = db.collection('customers')
query = customers_ref.where('total_spent', '>', 1000).order_by('total_spent', direction=firestore.Query.DESCENDING)

for doc in query.stream():
    print(f'{doc.id} => {doc.to_dict()}')

# Real-time listener
def on_snapshot(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == 'ADDED':
            print(f'New customer: {change.document.id}')
        elif change.type.name == 'MODIFIED':
            print(f'Modified customer: {change.document.id}')
        elif change.type.name == 'REMOVED':
            print(f'Removed customer: {change.document.id}')

col_query = db.collection('customers')
query_watch = col_query.on_snapshot(on_snapshot)
```

## 7. Dataproc (Managed Spark)
```python
from google.cloud import dataproc_v1

# Create Dataproc client
client = dataproc_v1.ClusterControllerClient(
    client_options={"api_endpoint": f"{region}-dataproc.googleapis.com:443"}
)

# Cluster configuration
cluster_config = {
    "project_id": project_id,
    "cluster_name": "spark-cluster",
    "config": {
        "master_config": {
            "num_instances": 1,
            "machine_type_uri": "n1-standard-2",
            "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 100}
        },
        "worker_config": {
            "num_instances": 2,
            "machine_type_uri": "n1-standard-2",
            "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 100}
        },
        "software_config": {
            "image_version": "2.0-debian10",
            "properties": {
                "spark:spark.sql.adaptive.enabled": "true",
                "spark:spark.sql.adaptive.coalescePartitions.enabled": "true"
            }
        }
    }
}

# Create cluster
operation = client.create_cluster(
    request={
        "project_id": project_id,
        "region": region,
        "cluster": cluster_config
    }
)

result = operation.result()
print(f"Cluster created: {result.cluster_name}")

# Submit Spark job
job_client = dataproc_v1.JobControllerClient(
    client_options={"api_endpoint": f"{region}-dataproc.googleapis.com:443"}
)

job = {
    "placement": {"cluster_name": "spark-cluster"},
    "pyspark_job": {
        "main_python_file_uri": "gs://my-bucket/spark-jobs/data_processing.py",
        "args": ["--input", "gs://my-bucket/input/", "--output", "gs://my-bucket/output/"],
        "python_file_uris": ["gs://my-bucket/spark-jobs/utils.py"]
    }
}

operation = job_client.submit_job(
    request={"project_id": project_id, "region": region, "job": job}
)

response = operation.result()
print(f"Job submitted: {response.reference.job_id}")
```

## 8. AI/ML Services
```python
# Vertex AI
from google.cloud import aiplatform

aiplatform.init(project=project_id, location="us-central1")

# AutoML Tables
dataset = aiplatform.TabularDataset.create(
    display_name="sales_prediction_dataset",
    gcs_source="gs://my-bucket/training_data.csv"
)

# Training job
job = aiplatform.AutoMLTabularTrainingJob(
    display_name="sales_prediction_model",
    optimization_prediction_type="regression",
    optimization_objective="minimize-rmse"
)

model = job.run(
    dataset=dataset,
    target_column="sales_amount",
    training_fraction_split=0.8,
    validation_fraction_split=0.1,
    test_fraction_split=0.1
)

# Batch prediction
batch_prediction_job = model.batch_predict(
    job_display_name="sales_batch_prediction",
    gcs_source="gs://my-bucket/prediction_input.csv",
    gcs_destination_prefix="gs://my-bucket/predictions/"
)

# BigQuery ML integration
bq_ml_query = """
CREATE OR REPLACE MODEL `project.dataset.sales_forecast`
OPTIONS(
    model_type='ARIMA_PLUS',
    time_series_timestamp_col='date',
    time_series_data_col='sales_amount',
    auto_arima=TRUE,
    data_frequency='DAILY'
) AS
SELECT date, sales_amount
FROM `project.dataset.daily_sales`
WHERE date >= '2023-01-01';
"""

query_job = bq_client.query(bq_ml_query)
```

## 9. Data Catalog and Governance
```python
# Data Catalog
from google.cloud import datacatalog_v1

catalog_client = datacatalog_v1.DataCatalogClient()

# Create entry group
entry_group = datacatalog_v1.EntryGroup()
entry_group.display_name = "Sales Data"
entry_group.description = "Sales and customer data assets"

entry_group_path = catalog_client.location_path(project_id, "us-central1")
created_entry_group = catalog_client.create_entry_group(
    parent=entry_group_path,
    entry_group_id="sales_data_group",
    entry_group=entry_group
)

# Create entry
entry = datacatalog_v1.Entry()
entry.display_name = "Customer Transactions"
entry.description = "Daily customer transaction data"
entry.type_ = datacatalog_v1.EntryType.TABLE

# BigQuery table reference
entry.bigquery_table_spec.table_spec.resource_name = (
    f"//bigquery.googleapis.com/projects/{project_id}/datasets/sales/tables/transactions"
)

created_entry = catalog_client.create_entry(
    parent=created_entry_group.name,
    entry_id="customer_transactions",
    entry=entry
)

# Add tags
tag_template = datacatalog_v1.TagTemplate()
tag_template.display_name = "Data Classification"

# Create tag template field
field = datacatalog_v1.TagTemplateField()
field.display_name = "Sensitivity Level"
field.type_.enum_type.allowed_values.append(
    datacatalog_v1.FieldType.EnumType.EnumValue(display_name="Public")
)
field.type_.enum_type.allowed_values.append(
    datacatalog_v1.FieldType.EnumType.EnumValue(display_name="Internal")
)
field.type_.enum_type.allowed_values.append(
    datacatalog_v1.FieldType.EnumType.EnumValue(display_name="Confidential")
)

tag_template.fields["sensitivity_level"] = field

# Data Loss Prevention (DLP)
from google.cloud import dlp_v2

dlp_client = dlp_v2.DlpServiceClient()

# Inspect data for PII
inspect_config = {
    "info_types": [
        {"name": "EMAIL_ADDRESS"},
        {"name": "PHONE_NUMBER"},
        {"name": "CREDIT_CARD_NUMBER"}
    ],
    "min_likelihood": dlp_v2.Likelihood.POSSIBLE,
    "include_quote": True
}

item = {"value": "Customer email: john.doe@example.com, Phone: 555-123-4567"}

parent = f"projects/{project_id}/locations/global"
response = dlp_client.inspect_content(
    request={
        "parent": parent,
        "inspect_config": inspect_config,
        "item": item
    }
)

for finding in response.result.findings:
    print(f"Info type: {finding.info_type.name}")
    print(f"Likelihood: {finding.likelihood}")
    print(f"Quote: {finding.quote}")
```

## 10. Monitoring and Operations
```python
# Cloud Monitoring
from google.cloud import monitoring_v3

monitoring_client = monitoring_v3.MetricServiceClient()
project_name = f"projects/{project_id}"

# Create custom metric
descriptor = monitoring_v3.MetricDescriptor()
descriptor.type = "custom.googleapis.com/pipeline/records_processed"
descriptor.metric_kind = monitoring_v3.MetricDescriptor.MetricKind.GAUGE
descriptor.value_type = monitoring_v3.MetricDescriptor.ValueType.INT64
descriptor.description = "Number of records processed by data pipeline"

descriptor = monitoring_client.create_metric_descriptor(
    name=project_name, metric_descriptor=descriptor
)

# Write time series data
series = monitoring_v3.TimeSeries()
series.metric.type = "custom.googleapis.com/pipeline/records_processed"
series.resource.type = "global"

now = time.time()
seconds = int(now)
nanos = int((now - seconds) * 10 ** 9)
interval = monitoring_v3.TimeInterval(
    {"end_time": {"seconds": seconds, "nanos": nanos}}
)

point = monitoring_v3.Point(
    {"interval": interval, "value": {"int64_value": 1000}}
)
series.points = [point]

monitoring_client.create_time_series(
    name=project_name, time_series=[series]
)

# Cloud Logging
from google.cloud import logging

logging_client = logging.Client()
logger = logging_client.logger("data-pipeline")

# Structured logging
logger.log_struct({
    "message": "Data processing completed",
    "severity": "INFO",
    "pipeline_id": "sales_etl_001",
    "records_processed": 10000,
    "duration_seconds": 120,
    "status": "success"
})

# Error tracking
try:
    # Data processing code
    process_data()
except Exception as e:
    logger.log_struct({
        "message": "Data processing failed",
        "severity": "ERROR",
        "pipeline_id": "sales_etl_001",
        "error_type": type(e).__name__,
        "error_message": str(e),
        "stack_trace": traceback.format_exc()
    })

# Cloud Functions for serverless processing
def process_gcs_file(event, context):
    """Triggered by Cloud Storage object creation."""
    
    file_name = event['name']
    bucket_name = event['bucket']
    
    logger.log_struct({
        "message": "Processing new file",
        "file_name": file_name,
        "bucket": bucket_name,
        "event_type": event['eventType']
    })
    
    # Process the file
    try:
        # Download and process
        blob = storage_client.bucket(bucket_name).blob(file_name)
        content = blob.download_as_text()
        
        # Process content
        processed_data = process_csv_content(content)
        
        # Upload results
        result_blob = storage_client.bucket(bucket_name).blob(f"processed/{file_name}")
        result_blob.upload_from_string(json.dumps(processed_data))
        
        logger.log_struct({
            "message": "File processed successfully",
            "file_name": file_name,
            "records_processed": len(processed_data)
        })
        
    except Exception as e:
        logger.log_struct({
            "message": "File processing failed",
            "severity": "ERROR",
            "file_name": file_name,
            "error": str(e)
        })
        raise
```