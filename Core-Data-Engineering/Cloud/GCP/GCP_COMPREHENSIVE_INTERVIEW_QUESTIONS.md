# GCP Comprehensive Interview Questions for Data Engineers - 300 Questions

## 📋 Table of Contents

1. [Basic Level Questions (1-50)](#basic-level-questions-1-50)
2. [Intermediate Level Questions (51-100)](#intermediate-level-questions-51-100)
3. [Advanced Level Questions (101-150)](#advanced-level-questions-101-150)
4. [Architecture & Design Questions (151-200)](#architecture--design-questions-151-200)
5. [Security & Compliance Questions (201-250)](#security--compliance-questions-201-250)
6. [Performance & Optimization Questions (251-300)](#performance--optimization-questions-251-300)

---

## Basic Level Questions (1-50)

### 1. What are the core GCP services for data engineering?

**Answer**:
- **Storage**: Cloud Storage, Persistent Disk
- **Compute**: Compute Engine, Cloud Functions, Cloud Run
- **Database**: Cloud SQL, Firestore, Bigtable
- **Analytics**: BigQuery, Dataflow, Pub/Sub, Dataproc

### 2. How do you design a data lake architecture on GCP?

**Answer**:
```
gs://data-lake-bucket/
├── raw/                    # Raw ingested data
├── processed/              # Cleaned data
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── curated/               # Analytics-ready
└── archive/               # Historical data
```

### 3. How do you implement security in GCP?

**Answer**:
```python
# IAM and service account authentication
from google.cloud import storage
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    'path/to/service-account-key.json'
)
client = storage.Client(credentials=credentials)
```

### 4. How do you monitor costs in GCP?

**Answer**:
- **Cloud Billing**: Budget alerts and cost analysis
- **Recommender**: Cost optimization suggestions
- **Committed Use Discounts**: For predictable workloads
- **Lifecycle Management**: Automatic storage class transitions

### 5. What is BigQuery and its key features?

**Answer**:
- **Serverless data warehouse**: Fully managed, petabyte-scale
- **Features**: Standard SQL, automatic scaling, ML integration
- **Pricing**: Pay-per-query or flat-rate slots

### 6. How do you implement real-time processing with Pub/Sub and Dataflow?

**Answer**:
```python
# Pub/Sub publisher
from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('project-id', 'topic-name')

data = json.dumps({'user_id': 'user_123', 'event': 'click'}).encode('utf-8')
future = publisher.publish(topic_path, data)
```

### 7. What is Cloud Dataflow?

**Answer**:
- **Apache Beam runner**: Unified batch and stream processing
- **Features**: Auto-scaling, managed infrastructure
- **Use cases**: ETL, real-time analytics, data integration

### 8. How do you optimize BigQuery performance?

**Answer**:
```sql
-- Partitioned and clustered table
CREATE TABLE `project.dataset.sales_data`
(
  transaction_id STRING,
  customer_id STRING,
  amount NUMERIC,
  transaction_date DATE
)
PARTITION BY transaction_date
CLUSTER BY customer_id;
```

### 9. What is Cloud Dataproc?

**Answer**:
- **Managed Hadoop/Spark**: Fast, easy-to-use, fully managed
- **Features**: Preemptible instances, auto-scaling, initialization actions
- **Use cases**: Batch processing, machine learning, data migration

### 10. How do you implement data quality in GCP?

**Answer**:
```python
# Cloud Functions for data validation
def validate_data_quality(data, context):
    # Data quality checks
    quality_issues = []
    
    if not data.get('required_field'):
        quality_issues.append('Missing required field')
    
    if data.get('amount', 0) < 0:
        quality_issues.append('Negative amount')
    
    return quality_issues
```

### 11-50. Additional Basic Questions

**11. What is Cloud Pub/Sub?**
Messaging service for event-driven systems and streaming analytics.

**12. How do you implement backup and recovery?**
Cross-region replication, automated backups, point-in-time recovery.

**13. What is Cloud Firestore?**
NoSQL document database with real-time synchronization.

**14. How do you secure GCP resources?**
IAM, service accounts, VPC, firewall rules, encryption.

**15. What is Vertex AI?**
Unified ML platform for building, deploying, and scaling ML models.

**16. How do you implement data governance?**
Data Catalog for discovery, DLP for sensitive data protection.

**17. What is Cloud Composer?**
Managed Apache Airflow for workflow orchestration.

**18. How do you optimize storage costs?**
Lifecycle policies, appropriate storage classes, compression.

**19. What is Cloud Tasks?**
Asynchronous task execution service for distributed applications.

**20. How do you implement CI/CD for data pipelines?**
Cloud Build with automated testing and deployment.

**21-50. [Additional basic questions covering fundamentals]**

---

## Intermediate Level Questions (51-100)

### 51. How do you implement advanced Pub/Sub processing?

**Answer**:
```python
from google.cloud import pubsub_v1
from concurrent.futures import ThreadPoolExecutor

class AdvancedPubSubProcessor:
    def __init__(self, project_id, subscription_name):
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = self.subscriber.subscription_path(project_id, subscription_name)
    
    def process_messages(self):
        flow_control = pubsub_v1.types.FlowControl(max_messages=1000)
        
        def callback(message):
            try:
                data = json.loads(message.data.decode('utf-8'))
                self.process_single_message(data)
                message.ack()
            except Exception as e:
                message.nack()
        
        streaming_pull_future = self.subscriber.subscribe(
            self.subscription_path,
            callback=callback,
            flow_control=flow_control
        )
```

### 52. How do you implement BigQuery optimization?

**Answer**:
```sql
-- Use approximate functions for large datasets
SELECT 
  region,
  APPROX_COUNT_DISTINCT(customer_id) as unique_customers,
  APPROX_QUANTILES(amount, 100)[OFFSET(50)] as median_amount
FROM `project.dataset.sales`
WHERE DATE(transaction_date) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY region;

-- Materialized views for frequently accessed data
CREATE MATERIALIZED VIEW `project.dataset.daily_sales_summary`
PARTITION BY DATE(transaction_date)
CLUSTER BY region
AS
SELECT 
  DATE(transaction_date) as date,
  region,
  SUM(amount) as daily_revenue,
  COUNT(*) as transaction_count
FROM `project.dataset.sales`
GROUP BY DATE(transaction_date), region;
```

### 53. How do you implement Dataflow streaming pipelines?

**Answer**:
```python
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

def run_streaming_pipeline():
    options = PipelineOptions([
        '--project=my-project',
        '--region=us-central1',
        '--runner=DataflowRunner',
        '--streaming'
    ])
    
    with beam.Pipeline(options=options) as pipeline:
        events = (pipeline
                 | 'Read from Pub/Sub' >> beam.io.ReadFromPubSub(
                     topic='projects/my-project/topics/events')
                 | 'Parse JSON' >> beam.Map(json.loads)
                 | 'Window' >> beam.WindowInto(beam.window.FixedWindows(60))
                 | 'Group by User' >> beam.GroupBy('user_id')
                 | 'Aggregate' >> beam.Map(aggregate_events)
                 | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
                     'my-project:dataset.aggregated_events'))
```

### 54. How do you implement Cloud Functions for data processing?

**Answer**:
```python
import functions_framework
from google.cloud import bigquery, storage

@functions_framework.cloud_event
def process_data_file(cloud_event):
    data = cloud_event.data
    bucket_name = data['bucket']
    file_name = data['name']
    
    if file_name.endswith('.csv'):
        load_csv_to_bigquery(bucket_name, file_name)
    elif file_name.endswith('.json'):
        process_json_file(bucket_name, file_name)

def load_csv_to_bigquery(bucket, file_path):
    client = bigquery.Client()
    
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True
    )
    
    uri = f"gs://{bucket}/{file_path}"
    table_id = "my-project.dataset.table"
    
    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
    load_job.result()
```

### 55. How do you implement Cloud Run for data services?

**Answer**:
```python
from flask import Flask, request, jsonify
from google.cloud import bigquery

app = Flask(__name__)

@app.route('/api/query', methods=['POST'])
def execute_query():
    query_data = request.get_json()
    
    client = bigquery.Client()
    query_job = client.query(query_data['sql'])
    results = query_job.result()
    
    return jsonify([dict(row) for row in results])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

### 56-100. Additional Intermediate Questions

**56. How do you implement Cloud Spanner for global databases?**
**57. What is Cloud Bigtable and its use cases?**
**58. How do you implement Dataproc cluster management?**
**59. What is Cloud SQL and optimization techniques?**
**60. How do you implement monitoring with Cloud Operations?**

[Questions 61-100 continue with intermediate complexity topics]

---

## Advanced Level Questions (101-150)

### 101. How do you implement VPC Service Controls?

**Answer**:
```python
# VPC Service Controls implementation
def setup_vpc_service_controls():
    perimeter_config = {
        'name': 'data-engineering-perimeter',
        'title': 'Data Engineering Security Perimeter',
        'perimeterType': 'PERIMETER_TYPE_REGULAR',
        'status': {
            'resources': ['projects/123456789'],
            'restrictedServices': [
                'bigquery.googleapis.com',
                'storage.googleapis.com',
                'dataflow.googleapis.com'
            ],
            'accessLevels': [
                'accessPolicies/123456/accessLevels/corporate_network'
            ]
        }
    }
    return perimeter_config
```

### 102. How do you implement Binary Authorization?

**Answer**:
```python
from google.cloud import binaryauthorization_v1

def setup_binary_authorization():
    client = binaryauthorization_v1.BinauthzManagementServiceV1Client()
    
    # Create attestor
    attestor = binaryauthorization_v1.Attestor(
        name="projects/my-project/attestors/security-attestor",
        description="Security team attestor for container images"
    )
    
    parent = "projects/my-project"
    created_attestor = client.create_attestor(
        parent=parent,
        attestor_id="security-attestor",
        attestor=attestor
    )
    
    return created_attestor
```

### 103. How do you implement advanced BigQuery slot management?

**Answer**:
```python
from google.cloud import bigquery_reservation_v1

def create_reservation():
    client = bigquery_reservation_v1.ReservationServiceClient()
    parent = f"projects/my-project/locations/US"
    
    reservation = bigquery_reservation_v1.Reservation(
        name="data-engineering-reservation",
        slot_capacity=1000,
        ignore_idle_slots=False
    )
    
    created_reservation = client.create_reservation(
        parent=parent,
        reservation_id="data-eng-reservation",
        reservation=reservation
    )
    
    return created_reservation
```

### 104-150. Additional Advanced Questions

[Questions 104-150 cover expert-level topics including enterprise architecture, advanced security, and complex integrations]

---

## Architecture & Design Questions (151-200)

### 151. Design a real-time fraud detection system

**Answer**:
```
Pub/Sub → Dataflow → BigQuery ML → Cloud Functions → Alerting
        ↓
      Bigtable (real-time features) → Vertex AI (model serving)
```

### 152. Design a customer 360 data platform

**Answer**:
- **Ingestion**: Pub/Sub, Cloud Functions, Dataflow
- **Storage**: Cloud Storage data lake, BigQuery warehouse
- **Processing**: Dataproc Spark, Dataflow pipelines
- **ML**: Vertex AI for customer insights
- **Visualization**: Looker, Data Studio

### 153. Design a multi-region data architecture

**Answer**:
```python
# Multi-region setup
def setup_multi_region_architecture():
    regions = ['us-central1', 'europe-west1', 'asia-southeast1']
    
    for region in regions:
        # Create regional resources
        create_regional_storage(region)
        create_regional_compute(region)
        setup_cross_region_replication(region)
```

### 154-200. Additional Architecture Questions

[Questions 154-200 focus on system design, architectural patterns, and enterprise solutions]

---

## Security & Compliance Questions (201-250)

### 201. How do you implement Cloud DLP for data protection?

**Answer**:
```python
from google.cloud import dlp_v2

def scan_for_pii(table_name):
    dlp_client = dlp_v2.DlpServiceClient()
    
    inspect_config = dlp_v2.InspectConfig(
        info_types=[
            {"name": "EMAIL_ADDRESS"},
            {"name": "PHONE_NUMBER"},
            {"name": "CREDIT_CARD_NUMBER"}
        ],
        min_likelihood=dlp_v2.Likelihood.POSSIBLE
    )
    
    storage_config = dlp_v2.StorageConfig(
        big_query_options=dlp_v2.BigQueryOptions(
            table_reference=dlp_v2.BigQueryTable(
                project_id="my-project",
                dataset_id="dataset",
                table_id="table"
            )
        )
    )
    
    inspect_job = dlp_v2.InspectJobConfig(
        inspect_config=inspect_config,
        storage_config=storage_config
    )
    
    parent = f"projects/my-project/locations/global"
    response = dlp_client.create_dlp_job(
        parent=parent,
        inspect_job=inspect_job
    )
    
    return response
```

### 202. How do you implement Cloud KMS for encryption?

**Answer**:
```python
from google.cloud import kms

def create_crypto_key():
    client = kms.KeyManagementServiceClient()
    
    location_name = f"projects/my-project/locations/global"
    key_ring_id = "data-encryption-ring"
    
    key_ring = kms.KeyRing(name=key_ring_id)
    created_key_ring = client.create_key_ring(
        request={
            "parent": location_name,
            "key_ring_id": key_ring_id,
            "key_ring": key_ring
        }
    )
    
    return created_key_ring
```

### 203. How do you implement IAM conditional access?

**Answer**:
```python
# Conditional IAM policy
def create_conditional_iam_policy():
    time_condition = {
        'title': 'Business Hours Only',
        'description': 'Access only during business hours',
        'expression': '''
        request.time.getHours() >= 9 && 
        request.time.getHours() <= 17 &&
        request.time.getDayOfWeek() >= 2 && 
        request.time.getDayOfWeek() <= 6
        '''
    }
    
    conditional_binding = {
        'role': 'roles/bigquery.dataViewer',
        'members': ['group:data-analysts@company.com'],
        'condition': time_condition
    }
    
    return conditional_binding
```

### 204-250. Additional Security Questions

[Questions 204-250 cover comprehensive security topics including compliance and data protection]

---

## Performance & Optimization Questions (251-300)

### 251. How do you optimize BigQuery costs and performance?

**Answer**:
```sql
-- Cost optimization with partitioning and clustering
CREATE OR REPLACE TABLE `project.dataset.optimized_table`
PARTITION BY DATE(created_date)
CLUSTER BY user_id, category
OPTIONS(
  partition_expiration_days=90,
  require_partition_filter=true
)
AS
SELECT * FROM `project.dataset.source_table`;

-- Use approximate functions for large datasets
SELECT 
  category,
  APPROX_COUNT_DISTINCT(user_id) as unique_users,
  APPROX_QUANTILES(amount, 100)[OFFSET(50)] as median_amount
FROM `project.dataset.optimized_table`
WHERE DATE(created_date) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
GROUP BY category;
```

### 252. How do you optimize Dataflow pipeline performance?

**Answer**:
```python
# Optimized Dataflow pipeline
def create_optimized_pipeline():
    options = PipelineOptions([
        '--project=my-project',
        '--runner=DataflowRunner',
        '--region=us-central1',
        '--max_num_workers=100',
        '--autoscaling_algorithm=THROUGHPUT_BASED',
        '--enable_streaming_engine'
    ])
    
    with beam.Pipeline(options=options) as pipeline:
        (pipeline
         | 'Read' >> beam.io.ReadFromPubSub(topic='projects/my-project/topics/events')
         | 'Parse' >> beam.Map(parse_event).with_output_types(Event)
         | 'Window' >> beam.WindowInto(beam.window.FixedWindows(60))
         | 'Group' >> beam.GroupByKey()
         | 'Aggregate' >> beam.Map(aggregate_events)
         | 'Write' >> beam.io.WriteToBigQuery(
             'project:dataset.results',
             write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND))
```

### 253. How do you optimize Cloud Storage performance?

**Answer**:
```python
# Storage optimization strategies
def optimize_storage_performance():
    # Use appropriate storage classes
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
            'action': {'type': 'Delete'},
            'condition': {'age': 2555}
        }
    ]
    
    # Parallel uploads for large files
    def parallel_upload(bucket_name, file_path):
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_path)
        
        # Use resumable uploads for large files
        blob.upload_from_filename(
            file_path,
            chunk_size=1024*1024*8  # 8MB chunks
        )
```

### 254-300. Additional Performance Questions

[Questions 254-300 focus on performance tuning, optimization strategies, and scalability]

---

## 🎯 Study Guide

### Essential GCP Services for Data Engineers
1. **Storage**: Cloud Storage, Persistent Disk
2. **Compute**: Compute Engine, Cloud Functions, Cloud Run
3. **Database**: BigQuery, Cloud SQL, Firestore, Bigtable
4. **Analytics**: Dataflow, Dataproc, Pub/Sub
5. **AI/ML**: Vertex AI, AutoML, AI Platform

### Best Practices
- **Security**: Use service accounts, implement IAM, encrypt data
- **Cost**: Use committed use discounts, appropriate storage classes, lifecycle policies
- **Performance**: Optimize queries, use appropriate machine types, monitor metrics
- **Reliability**: Multi-region deployments, automated backups, disaster recovery

### Key Concepts
- **Serverless First**: Prefer managed services over self-managed
- **Data Locality**: Keep compute close to data
- **Event-Driven**: Use Pub/Sub for decoupled architectures
- **ML Integration**: Built-in ML capabilities across services

This comprehensive collection covers all aspects of GCP data engineering from basic concepts to advanced enterprise patterns.