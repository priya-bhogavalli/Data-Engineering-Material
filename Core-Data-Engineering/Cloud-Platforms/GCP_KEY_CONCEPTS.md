# Google Cloud Platform (GCP) Key Concepts

## 1. Cloud Computing Platform
**What it is**: Google's suite of cloud computing services running on the same infrastructure as Google's products.

**Core Services**:
- **Compute**: Virtual machines, containers, serverless
- **Storage**: Object, block, file storage solutions
- **Databases**: SQL, NoSQL, analytics databases
- **Networking**: VPC, load balancing, CDN
- **Big Data**: Analytics, ML, data processing

## 2. Project Organization
**Resource Hierarchy**:
```bash
Organization
└── Folders
    └── Projects
        └── Resources (VMs, databases, etc.)

# Create project
gcloud projects create my-data-project \
    --name="Data Engineering Project" \
    --labels=environment=dev,team=data

# Set active project
gcloud config set project my-data-project
```

## 3. Compute Services
**Compute Engine (VMs)**:
```bash
# Create VM instance
gcloud compute instances create data-processing-vm \
    --zone=us-central1-a \
    --machine-type=n1-standard-4 \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=100GB \
    --boot-disk-type=pd-ssd

# SSH to instance
gcloud compute ssh data-processing-vm --zone=us-central1-a
```

**Cloud Run (Serverless)**:
```bash
# Deploy container
gcloud run deploy data-api \
    --image=gcr.io/my-project/data-api:latest \
    --platform=managed \
    --region=us-central1 \
    --allow-unauthenticated \
    --memory=2Gi \
    --cpu=2
```

## 4. Storage Services
**Cloud Storage**:
```bash
# Create bucket
gsutil mb -p my-project -c STANDARD -l us-central1 gs://my-data-bucket

# Upload files
gsutil cp local-file.csv gs://my-data-bucket/data/
gsutil -m cp -r local-directory gs://my-data-bucket/

# Set lifecycle policy
gsutil lifecycle set lifecycle.json gs://my-data-bucket
```

**Lifecycle Policy Example**:
```json
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "SetStorageClass", "storageClass": "NEARLINE"},
        "condition": {"age": 30}
      },
      {
        "action": {"type": "SetStorageClass", "storageClass": "COLDLINE"},
        "condition": {"age": 90}
      },
      {
        "action": {"type": "Delete"},
        "condition": {"age": 365}
      }
    ]
  }
}
```

## 5. Database Services
**Cloud SQL**:
```bash
# Create MySQL instance
gcloud sql instances create mysql-instance \
    --database-version=MYSQL_8_0 \
    --tier=db-n1-standard-2 \
    --region=us-central1 \
    --storage-size=100GB \
    --storage-type=SSD \
    --backup-start-time=03:00

# Create database
gcloud sql databases create sales_db --instance=mysql-instance

# Create user
gcloud sql users create datauser \
    --instance=mysql-instance \
    --password=SecurePassword123!
```

**BigQuery**:
```bash
# Create dataset
bq mk --dataset --location=US my-project:sales_data

# Create table
bq mk --table my-project:sales_data.orders \
    order_id:STRING,customer_id:STRING,amount:FLOAT,order_date:DATE

# Load data
bq load --source_format=CSV \
    my-project:sales_data.orders \
    gs://my-data-bucket/orders.csv \
    order_id:STRING,customer_id:STRING,amount:FLOAT,order_date:DATE
```

## 6. Big Data and Analytics
**Dataflow (Apache Beam)**:
```python
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

def run_pipeline():
    pipeline_options = PipelineOptions([
        '--project=my-project',
        '--region=us-central1',
        '--runner=DataflowRunner',
        '--temp_location=gs://my-bucket/temp',
        '--staging_location=gs://my-bucket/staging'
    ])
    
    with beam.Pipeline(options=pipeline_options) as pipeline:
        (pipeline
         | 'Read from GCS' >> beam.io.ReadFromText('gs://input-bucket/data.txt')
         | 'Transform' >> beam.Map(lambda x: x.upper())
         | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
             'my-project:dataset.table',
             schema='field1:STRING,field2:INTEGER'
         ))
```

**Dataproc (Managed Spark/Hadoop)**:
```bash
# Create cluster
gcloud dataproc clusters create spark-cluster \
    --zone=us-central1-a \
    --num-masters=1 \
    --num-workers=2 \
    --worker-machine-type=n1-standard-4 \
    --image-version=2.0-debian10

# Submit Spark job
gcloud dataproc jobs submit spark \
    --cluster=spark-cluster \
    --region=us-central1 \
    --class=com.example.SparkJob \
    --jars=gs://my-bucket/spark-job.jar \
    --properties=spark.executor.memory=4g
```

## 7. Machine Learning Services
**Vertex AI**:
```python
from google.cloud import aiplatform

# Initialize Vertex AI
aiplatform.init(project='my-project', location='us-central1')

# Create custom training job
job = aiplatform.CustomTrainingJob(
    display_name='sales-prediction-training',
    script_path='train.py',
    container_uri='gcr.io/cloud-aiplatform/training/tf-cpu.2-8:latest',
    requirements=['pandas', 'scikit-learn'],
    model_serving_container_image_uri='gcr.io/cloud-aiplatform/prediction/tf2-cpu.2-8:latest'
)

# Run training
model = job.run(
    dataset=dataset,
    replica_count=1,
    machine_type='n1-standard-4',
    sync=True
)
```

**AutoML**:
```bash
# Create AutoML dataset
gcloud ai datasets create \
    --display-name=sales-prediction-dataset \
    --metadata-schema-uri=gs://google-cloud-aiplatform/schema/dataset/metadata/tabular_1.0.0.yaml \
    --region=us-central1
```

## 8. Networking and Security
**VPC Networks**:
```bash
# Create VPC
gcloud compute networks create data-vpc --subnet-mode=custom

# Create subnet
gcloud compute networks subnets create data-subnet \
    --network=data-vpc \
    --range=10.1.0.0/24 \
    --region=us-central1

# Create firewall rule
gcloud compute firewall-rules create allow-ssh \
    --network=data-vpc \
    --allow=tcp:22 \
    --source-ranges=0.0.0.0/0
```

**Identity and Access Management (IAM)**:
```bash
# Grant role to user
gcloud projects add-iam-policy-binding my-project \
    --member=user:analyst@company.com \
    --role=roles/bigquery.dataViewer

# Create service account
gcloud iam service-accounts create data-pipeline-sa \
    --display-name="Data Pipeline Service Account"

# Generate key
gcloud iam service-accounts keys create key.json \
    --iam-account=data-pipeline-sa@my-project.iam.gserviceaccount.com
```

## 9. Monitoring and Logging
**Cloud Monitoring**:
```python
from google.cloud import monitoring_v3

client = monitoring_v3.MetricServiceClient()
project_name = f"projects/{project_id}"

# Create custom metric
descriptor = monitoring_v3.MetricDescriptor()
descriptor.type = "custom.googleapis.com/data_pipeline/records_processed"
descriptor.metric_kind = monitoring_v3.MetricDescriptor.MetricKind.GAUGE
descriptor.value_type = monitoring_v3.MetricDescriptor.ValueType.INT64

client.create_metric_descriptor(name=project_name, metric_descriptor=descriptor)
```

**Cloud Logging**:
```python
from google.cloud import logging

# Initialize client
client = logging.Client()
logger = client.logger('data-pipeline')

# Write log entry
logger.log_struct({
    'message': 'Data processing completed',
    'records_processed': 10000,
    'processing_time': 120.5
}, severity='INFO')
```

## 10. Cost Management
**Billing and Budgets**:
```bash
# Set up budget alert
gcloud billing budgets create \
    --billing-account=BILLING_ACCOUNT_ID \
    --display-name="Data Project Budget" \
    --budget-amount=1000USD \
    --threshold-rule=percent=0.8,basis=CURRENT_SPEND \
    --threshold-rule=percent=1.0,basis=CURRENT_SPEND
```

**Resource Optimization**:
```bash
# Use preemptible instances
gcloud compute instances create preemptible-vm \
    --preemptible \
    --machine-type=n1-standard-4 \
    --zone=us-central1-a

# Committed use discounts
gcloud compute commitments create cpu-commitment \
    --plan=12-month \
    --region=us-central1 \
    --type=GENERAL_PURPOSE_N1 \
    --cores=100
```

## 11. Data Pipeline Orchestration
**Cloud Composer (Managed Airflow)**:
```bash
# Create Composer environment
gcloud composer environments create data-pipeline-env \
    --location=us-central1 \
    --python-version=3 \
    --node-count=3 \
    --machine-type=n1-standard-2 \
    --disk-size=100GB
```

**Workflow DAG Example**:
```python
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyTableOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'gcp_data_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
)

load_data = GCSToBigQueryOperator(
    task_id='load_sales_data',
    bucket='my-data-bucket',
    source_objects=['sales/{{ ds }}/sales_data.csv'],
    destination_project_dataset_table='my-project.sales.daily_sales',
    schema_fields=[
        {'name': 'date', 'type': 'DATE'},
        {'name': 'amount', 'type': 'FLOAT'},
        {'name': 'customer_id', 'type': 'STRING'}
    ],
    write_disposition='WRITE_TRUNCATE',
    dag=dag
)
```