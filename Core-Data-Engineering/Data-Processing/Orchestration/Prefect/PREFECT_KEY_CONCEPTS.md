# 🚀 Prefect - Key Concepts

**Category**: Modern Workflow Orchestration  
**Market Share**: 15% of workflow orchestration market  
**Interview Frequency**: 25% of data engineering roles  
**Learning Time**: 2-3 weeks

---

## 🎯 What is Prefect?

Prefect is a modern workflow orchestration platform that makes it easy to build, run, and monitor data pipelines at scale with Python-first approach.

### **Core Value Proposition**
- **Python-native** workflow definition
- **Hybrid execution** model (cloud + on-premises)
- **Dynamic workflows** with conditional logic
- **Modern UI** with rich observability
- **Failure handling** and automatic retries

---

## 🏗️ Architecture Overview

```
Flows → Tasks → Prefect Cloud/Server → Agents → Infrastructure
  ↓       ↓           ↓                    ↓         ↓
Python  Functions  Orchestration      Execution   Docker/K8s
```

### **Key Components**

1. **Flows**: Containerized workflows
2. **Tasks**: Individual units of work
3. **Prefect Server/Cloud**: Orchestration engine
4. **Agents**: Execute flows on infrastructure
5. **Deployments**: Scheduled flow runs

---

## 🔧 Core Concepts

### **1. Flows and Tasks**
```python
from prefect import flow, task
import requests

@task
def extract_data(url: str):
    """Extract data from API"""
    response = requests.get(url)
    return response.json()

@task  
def transform_data(raw_data: dict):
    """Transform the data"""
    return {
        'processed_at': datetime.now(),
        'record_count': len(raw_data.get('records', [])),
        'data': raw_data
    }

@task
def load_data(transformed_data: dict, destination: str):
    """Load data to destination"""
    print(f"Loading {transformed_data['record_count']} records to {destination}")
    return True

@flow(name="ETL Pipeline")
def etl_pipeline(api_url: str, destination: str):
    """Main ETL flow"""
    raw_data = extract_data(api_url)
    transformed_data = transform_data(raw_data)
    result = load_data(transformed_data, destination)
    return result

# Run the flow
if __name__ == "__main__":
    etl_pipeline(
        api_url="https://api.example.com/data",
        destination="warehouse"
    )
```

### **2. Flow Configuration**
```python
from prefect import flow
from prefect.task_runners import ConcurrentTaskRunner

@flow(
    name="Data Processing Pipeline",
    description="Process daily sales data",
    version="1.0.0",
    task_runner=ConcurrentTaskRunner(),
    retries=3,
    retry_delay_seconds=60
)
def data_pipeline():
    # Flow logic here
    pass
```

### **3. Task Dependencies**
```python
@flow
def complex_pipeline():
    # Sequential execution
    data = extract_data()
    cleaned_data = clean_data(data)
    result = load_data(cleaned_data)
    
    # Parallel execution
    report1 = generate_report(result, "summary")
    report2 = generate_report(result, "detailed")
    
    # Wait for both reports
    send_notification([report1, report2])
```

---

## 🚀 Implementation

### **1. Basic Setup**
```bash
# Install Prefect
pip install prefect

# Start Prefect server (local)
prefect server start

# Or use Prefect Cloud
prefect cloud login
```

### **2. Deployments**
```python
from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerContainer

# Create deployment
deployment = Deployment.build_from_flow(
    flow=etl_pipeline,
    name="daily-etl",
    schedule={"cron": "0 6 * * *"},  # Daily at 6 AM
    infrastructure=DockerContainer(
        image="my-etl-image:latest",
        env={"ENV": "production"}
    ),
    parameters={
        "api_url": "https://api.example.com/data",
        "destination": "snowflake"
    }
)

deployment.apply()
```

### **3. Error Handling**
```python
from prefect import task, flow
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(
    retries=3,
    retry_delay_seconds=60,
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(hours=1)
)
def unreliable_api_call(endpoint: str):
    """Task with retry logic and caching"""
    try:
        response = requests.get(endpoint, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"API call failed: {e}")
        raise

@flow
def robust_pipeline():
    try:
        data = unreliable_api_call("https://api.example.com/data")
        process_data(data)
    except Exception as e:
        # Handle flow-level errors
        send_alert(f"Pipeline failed: {e}")
        raise
```

---

## 📊 Monitoring & Observability

### **1. Flow Run States**
```python
from prefect import get_run_logger

@task
def monitored_task():
    logger = get_run_logger()
    
    logger.info("Starting data processing")
    # Process data
    logger.info("Data processing completed")
    
    return {"status": "success", "records_processed": 1000}

@flow
def monitored_flow():
    result = monitored_task()
    
    # Log flow-level metrics
    logger = get_run_logger()
    logger.info(f"Flow completed: {result}")
```

### **2. Custom Metrics**
```python
from prefect.blocks.notifications import SlackWebhook

@task
def send_metrics(metrics: dict):
    """Send custom metrics to monitoring system"""
    
    # Send to Slack
    slack_webhook = SlackWebhook.load("data-team-alerts")
    slack_webhook.notify(
        subject="Pipeline Metrics",
        body=f"Processed {metrics['record_count']} records in {metrics['duration']} seconds"
    )
    
    # Send to custom monitoring
    send_to_datadog(metrics)
```

### **3. Flow Run Tracking**
```python
@flow
def tracked_pipeline():
    start_time = time.time()
    
    try:
        # Pipeline logic
        result = process_data()
        
        # Track success metrics
        duration = time.time() - start_time
        track_success_metrics(duration, result)
        
    except Exception as e:
        # Track failure metrics
        track_failure_metrics(str(e))
        raise
```

---

## 🛠️ Common Use Cases

### **1. ETL Pipelines**
```python
@flow(name="Daily ETL")
def daily_etl():
    # Extract from multiple sources
    sales_data = extract_from_database("sales")
    customer_data = extract_from_api("customers") 
    
    # Transform data
    cleaned_sales = clean_sales_data(sales_data)
    enriched_data = enrich_with_customer_data(cleaned_sales, customer_data)
    
    # Load to warehouse
    load_to_snowflake(enriched_data)
    
    # Generate reports
    create_daily_report(enriched_data)
```

### **2. ML Pipeline**
```python
@flow(name="ML Training Pipeline")
def ml_training_pipeline():
    # Data preparation
    raw_data = extract_training_data()
    features = engineer_features(raw_data)
    train_data, test_data = split_data(features)
    
    # Model training
    model = train_model(train_data)
    metrics = evaluate_model(model, test_data)
    
    # Model deployment
    if metrics['accuracy'] > 0.85:
        deploy_model(model)
        notify_success(metrics)
    else:
        notify_failure(metrics)
```

### **3. Data Quality Monitoring**
```python
@flow(name="Data Quality Checks")
def data_quality_pipeline():
    tables = ["users", "orders", "products"]
    
    quality_results = []
    for table in tables:
        result = check_data_quality(table)
        quality_results.append(result)
        
        if result['quality_score'] < 0.9:
            send_quality_alert(table, result)
    
    generate_quality_report(quality_results)
```

---

## 💡 Best Practices

### **1. Flow Design**
- Keep **tasks atomic** and focused
- Use **meaningful names** for flows and tasks
- Implement **proper error handling**
- Design for **idempotency**

### **2. Resource Management**
```python
from prefect.infrastructure import Process, DockerContainer

# For lightweight tasks
@flow(infrastructure=Process())
def simple_flow():
    pass

# For resource-intensive tasks  
@flow(infrastructure=DockerContainer(
    image="python:3.9",
    cpu_request="2",
    memory_request="4Gi"
))
def heavy_flow():
    pass
```

### **3. Configuration Management**
```python
from prefect.blocks.system import Secret

@task
def connect_to_database():
    # Use Prefect blocks for secrets
    db_password = Secret.load("database-password")
    
    connection = create_connection(
        host="localhost",
        password=db_password.get()
    )
    return connection
```

---

## 🎯 When to Choose Prefect

### **✅ Choose Prefect When:**
- Want **Python-native** workflows
- Need **modern UI** and observability
- Require **hybrid execution** (cloud + on-prem)
- Want **dynamic workflows**
- Need **easy deployment** and scaling

### **❌ Consider Alternatives When:**
- Need **mature ecosystem** (use Airflow)
- Require **complex scheduling** (use Airflow)
- Want **language agnostic** (use Temporal)
- Have **simple workflows** (use cron jobs)

---

## 🔗 Integration Ecosystem

### **Infrastructure**
- **Docker** containers
- **Kubernetes** deployments  
- **AWS ECS/Fargate**
- **Local processes**

### **Notifications**
- **Slack**, **Microsoft Teams**
- **Email**, **PagerDuty**
- **Custom webhooks**

### **Storage**
- **S3**, **GCS**, **Azure Blob**
- **Local filesystem**
- **Database connections**

---

**🎯 Next Steps**: Check out [Interview Questions](./PREFECT_INTERVIEW_QUESTIONS.md)