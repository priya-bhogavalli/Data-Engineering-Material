# GCP Services Quick Reference for Data Engineers

## Storage Services

### Cloud Storage
**Use Case**: Data lake, backup, static websites
```bash
# CLI Commands
gsutil cp file.csv gs://bucket/path/
gsutil -m rsync -r ./data/ gs://bucket/data/
gsutil ls gs://bucket/ -r
gsutil rm gs://bucket/file.csv
```

### Persistent Disk
**Use Case**: Block storage for Compute Engine
```bash
# Create disk
gcloud compute disks create my-disk --size=100GB --zone=us-central1-a
# Attach disk
gcloud compute instances attach-disk my-instance --disk=my-disk --zone=us-central1-a
```

## Compute Services

### Compute Engine
**Use Case**: Virtual machines
```bash
# Create instance
gcloud compute instances create my-instance --machine-type=n1-standard-4 --zone=us-central1-a
# SSH to instance
gcloud compute ssh my-instance --zone=us-central1-a
```

### Cloud Functions
**Use Case**: Serverless compute
```python
import functions_framework
@functions_framework.http
def hello_world(request):
    return 'Hello World!'
```

### Dataproc
**Use Case**: Managed Hadoop/Spark
```bash
# Create cluster
gcloud dataproc clusters create my-cluster --zone=us-central1-a --num-workers=3
# Submit job
gcloud dataproc jobs submit spark --cluster=my-cluster --jar=gs://bucket/job.jar
```

## Database Services

### BigQuery
**Use Case**: Data warehouse
```sql
-- Create dataset
CREATE SCHEMA my_dataset;

-- Create table
CREATE TABLE my_dataset.sales (
    id INT64,
    amount NUMERIC,
    date DATE
);

-- Load data
LOAD DATA INTO my_dataset.sales
FROM FILES (
    format = 'CSV',
    uris = ['gs://bucket/data.csv']
);
```

### Cloud SQL
**Use Case**: Managed relational database
```bash
# Create instance
gcloud sql instances create my-instance --database-version=MYSQL_8_0 --tier=db-n1-standard-2
# Create database
gcloud sql databases create my-db --instance=my-instance
```

### Firestore
**Use Case**: NoSQL document database
```python
from google.cloud import firestore
db = firestore.Client()
doc_ref = db.collection('users').document('user1')
doc_ref.set({'name': 'John', 'age': 30})
```

## Analytics Services

### BigQuery
**Use Case**: Analytics and ML
```python
from google.cloud import bigquery
client = bigquery.Client()
query = "SELECT * FROM `project.dataset.table` LIMIT 10"
results = client.query(query)
for row in results:
    print(row)
```

### Dataflow
**Use Case**: Stream and batch processing
```python
import apache_beam as beam
with beam.Pipeline() as pipeline:
    (pipeline
     | 'Read' >> beam.io.ReadFromText('gs://bucket/input.txt')
     | 'Transform' >> beam.Map(lambda x: x.upper())
     | 'Write' >> beam.io.WriteToText('gs://bucket/output.txt'))
```

### Pub/Sub
**Use Case**: Real-time messaging
```python
from google.cloud import pubsub_v1
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('project', 'topic')
publisher.publish(topic_path, b'Hello World!')
```

## Machine Learning Services

### Vertex AI
**Use Case**: ML platform
```python
from google.cloud import aiplatform
aiplatform.init(project='my-project', location='us-central1')

job = aiplatform.CustomTrainingJob(
    display_name='training-job',
    script_path='train.py',
    container_uri='gcr.io/cloud-aiplatform/training/tf-cpu.2-8:latest'
)
job.run()
```

### AutoML
**Use Case**: Automated ML
```python
from google.cloud import automl
client = automl.AutoMlClient()
dataset = client.create_dataset(
    parent='projects/my-project/locations/us-central1',
    dataset={'display_name': 'my_dataset', 'tables_dataset_metadata': {}}
)
```

## Security Services

### IAM
**Use Case**: Access control
```bash
# Grant role
gcloud projects add-iam-policy-binding my-project --member="user:email@company.com" --role="roles/bigquery.dataEditor"
# Create service account
gcloud iam service-accounts create my-service-account
```

### Cloud KMS
**Use Case**: Key management
```python
from google.cloud import kms
client = kms.KeyManagementServiceClient()
key_ring = client.create_key_ring(
    request={'parent': 'projects/my-project/locations/global', 'key_ring_id': 'my-ring'}
)
```

### Secret Manager
**Use Case**: Store secrets
```python
from google.cloud import secretmanager
client = secretmanager.SecretManagerServiceClient()
secret = client.create_secret(
    request={'parent': 'projects/my-project', 'secret_id': 'my-secret', 'secret': {}}
)
```

## Monitoring Services

### Cloud Monitoring
**Use Case**: Metrics and alerting
```python
from google.cloud import monitoring_v3
client = monitoring_v3.MetricServiceClient()
series = monitoring_v3.TimeSeries()
series.metric.type = 'custom.googleapis.com/my_metric'
series.resource.type = 'global'
client.create_time_series(name='projects/my-project', time_series=[series])
```

### Cloud Logging
**Use Case**: Log management
```python
from google.cloud import logging
client = logging.Client()
logger = client.logger('my-log')
logger.log_text('Hello World!')
```

## Networking Services

### VPC
**Use Case**: Virtual private cloud
```bash
# Create VPC
gcloud compute networks create my-vpc --subnet-mode=custom
# Create subnet
gcloud compute networks subnets create my-subnet --network=my-vpc --range=10.0.1.0/24 --region=us-central1
```

## Management Services

### Deployment Manager
**Use Case**: Infrastructure as code
```yaml
# config.yaml
resources:
- name: my-instance
  type: compute.v1.instance
  properties:
    zone: us-central1-a
    machineType: zones/us-central1-a/machineTypes/n1-standard-1
```

### Cloud Build
**Use Case**: CI/CD
```yaml
# cloudbuild.yaml
steps:
- name: 'gcr.io/cloud-builders/docker'
  args: ['build', '-t', 'gcr.io/$PROJECT_ID/my-app', '.']
- name: 'gcr.io/cloud-builders/docker'
  args: ['push', 'gcr.io/$PROJECT_ID/my-app']
```

## Cost Management

### Billing
**Use Case**: Cost monitoring
```python
from google.cloud import billing
client = billing.CloudBillingClient()
accounts = client.list_billing_accounts()
for account in accounts:
    print(f"Account: {account.name}")
```

## Common CLI Commands

### Project Management
```bash
# Set project
gcloud config set project my-project
# List projects
gcloud projects list
# Create project
gcloud projects create my-new-project
```

### Authentication
```bash
# Login
gcloud auth login
# Set service account
gcloud auth activate-service-account --key-file=key.json
# Application default credentials
gcloud auth application-default login
```

### Resource Management
```bash
# List resources
gcloud compute instances list
gcloud sql instances list
gcloud container clusters list

# Describe resource
gcloud compute instances describe my-instance --zone=us-central1-a
```

## Best Practices

### Security
- Use IAM roles instead of service account keys
- Enable audit logging
- Use VPC for network isolation
- Encrypt data with Cloud KMS

### Cost Optimization
- Use preemptible instances for fault-tolerant workloads
- Set up billing alerts
- Use committed use discounts
- Implement lifecycle policies for Cloud Storage

### Performance
- Choose appropriate machine types
- Use regional persistent disks for high availability
- Implement caching strategies
- Monitor with Cloud Monitoring

### Reliability
- Design for failure with multi-zone deployments
- Implement backup strategies
- Use health checks
- Test disaster recovery procedures