# Apache Airflow Key Concepts for Data Engineering

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Core Components](#-core-components)
   - [DAGs (Directed Acyclic Graphs)](#dags-directed-acyclic-graphs)
   - [Tasks and Operators](#tasks-and-operators)
   - [Executors](#executors)
3. [Airflow Architecture](#-airflow-architecture)
4. [Scheduling & Execution](#-scheduling--execution)
5. [Data Passing & Communication](#-data-passing--communication)
   - [XCom](#1-xcom)
   - [Variables](#2-variables)
   - [Connections](#3-connections)
6. [Performance Optimization](#-performance-optimization)
   - [Parallelism](#1-parallelism)
   - [Resource Management](#2-resource-management)
   - [Task Dependencies](#3-task-dependencies)
7. [Configuration](#️-configuration)
8. [Monitoring & Logging](#-monitoring--logging)
9. [When to Use Airflow](#-when-to-use-airflow)
10. [Interview Focus Areas](#-interview-focus-areas)
11. [Quick References](#-quick-references)

---

## 🎯 Overview

Apache Airflow is an open-source workflow orchestration platform for developing, scheduling, and monitoring batch-oriented workflows. It allows you to programmatically author, schedule, and monitor data pipelines using Python.

**Key Benefits:**
- **Dynamic Pipeline Generation**: Pipelines configured as code (Python)
- **Extensible**: Rich ecosystem of operators and hooks
- **Elegant UI**: Monitor, schedule, and troubleshoot pipelines
- **Scalable**: Modular architecture with message queues
- **Rich Scheduling**: Cron-based scheduling with backfill capabilities

## 📦 Core Components

### DAGs (Directed Acyclic Graphs)

**Definition**: A DAG is a collection of tasks organized to reflect their relationships and dependencies, with no cycles.

**Key Properties**:
- **Directed**: Clear upstream/downstream relationships
- **Acyclic**: No circular dependencies preventing infinite loops
- **Graph**: Collection of interconnected tasks

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# DAG definition
default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'data_pipeline_example',
    default_args=default_args,
    description='Sample data processing pipeline',
    schedule_interval='@daily',
    catchup=False,
    tags=['data', 'etl', 'production']
)

# Task definition
extract_task = BashOperator(
    task_id='extract_data',
    bash_command='python /scripts/extract.py',
    dag=dag
)

def transform_data(**context):
    print(f"Transforming data for {context['ds']}")
    return "transformation_complete"

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag
)

load_task = BashOperator(
    task_id='load_data',
    bash_command='python /scripts/load.py',
    dag=dag
)

# Define dependencies
extract_task >> transform_task >> load_task
```

### Tasks and Operators

**Definition**: Tasks are the basic unit of execution in Airflow. Operators define what actually gets executed.

#### 🔧 **Common Operator Types**

**1. Action Operators**
```python
# BashOperator - Execute bash commands
bash_task = BashOperator(
    task_id='run_script',
    bash_command='echo "Processing data for {{ ds }}"',
    dag=dag
)

# PythonOperator - Execute Python functions
def process_data(**context):
    execution_date = context['execution_date']
    print(f"Processing data for {execution_date}")
    return {"status": "success", "records": 1000}

python_task = PythonOperator(
    task_id='process_data',
    python_callable=process_data,
    dag=dag
)

# EmailOperator - Send emails
from airflow.operators.email import EmailOperator

email_task = EmailOperator(
    task_id='send_notification',
    to=['team@company.com'],
    subject='Pipeline Completed - {{ ds }}',
    html_content='<p>Data pipeline completed successfully</p>',
    dag=dag
)
```

**2. Transfer Operators**
```python
# S3ToRedshiftOperator - Transfer data between systems
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator

transfer_task = S3ToRedshiftOperator(
    task_id='s3_to_redshift',
    schema='public',
    table='user_data',
    s3_bucket='data-bucket',
    s3_key='processed/user_data.csv',
    copy_options=['CSV', 'IGNOREHEADER 1'],
    dag=dag
)
```

**3. Sensor Operators**
```python
# FileSensor - Wait for file to appear
from airflow.sensors.filesystem import FileSensor

file_sensor = FileSensor(
    task_id='wait_for_file',
    filepath='/data/input/daily_data.csv',
    fs_conn_id='fs_default',
    poke_interval=30,  # Check every 30 seconds
    timeout=300,       # Timeout after 5 minutes
    dag=dag
)

# S3KeySensor - Wait for S3 object
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

s3_sensor = S3KeySensor(
    task_id='wait_for_s3_file',
    bucket_name='data-bucket',
    bucket_key='input/{{ ds }}/data.parquet',
    aws_conn_id='aws_default',
    timeout=600,
    poke_interval=60,
    dag=dag
)
```

### Executors

**Definition**: Executors determine how and where tasks are executed.

#### 🚀 **Executor Types**

**1. SequentialExecutor**
- Single-threaded execution
- Development/testing only
- No parallelism

**2. LocalExecutor**
- Multi-process execution on single machine
- Good for small to medium workloads
- Limited by single machine resources

**3. CeleryExecutor**
- Distributed execution using Celery
- Scales across multiple worker machines
- Requires message broker (Redis/RabbitMQ)

```python
# Celery configuration
AIRFLOW__CORE__EXECUTOR = CeleryExecutor
AIRFLOW__CELERY__BROKER_URL = redis://localhost:6379/0
AIRFLOW__CELERY__RESULT_BACKEND = db+postgresql://user:pass@localhost/airflow
```

**4. KubernetesExecutor**
- Dynamic pod creation in Kubernetes
- Excellent resource isolation
- Auto-scaling capabilities

```python
# Kubernetes configuration
AIRFLOW__CORE__EXECUTOR = KubernetesExecutor
AIRFLOW__KUBERNETES__NAMESPACE = airflow
AIRFLOW__KUBERNETES__WORKER_CONTAINER_REPOSITORY = apache/airflow
AIRFLOW__KUBERNETES__WORKER_CONTAINER_TAG = 2.7.0
```

## 🏗️ Airflow Architecture

**Definition**: Airflow follows a distributed architecture with multiple components working together.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              AIRFLOW ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────────┐  │
│  │   WEB SERVER    │    │    SCHEDULER    │    │      METADATA DATABASE     │  │
│  │                 │    │                 │    │                             │  │
│  │ ┌─────────────┐ │    │ ┌─────────────┐ │    │  ┌─────────────────────────┐ │  │
│  │ │   Flask     │ │    │ │DAG Processor│ │    │  │ • DAG Definitions       │ │  │
│  │ │   Web UI    │ │◄──►│ │Task Scheduler│ │◄──►│  │ • Task Instances        │ │  │
│  │ │   REST API  │ │    │ │Executor Mgmt│ │    │  │ • Task Logs             │ │  │
│  │ └─────────────┘ │    │ └─────────────┘ │    │  │ • Variables & Connections│ │  │
│  └─────────────────┘    └─────────────────┘    │  │ • User Management       │ │  │
│           │                       │             │  └─────────────────────────┘ │  │
│           │                       │             └─────────────────────────────┘  │
│           │                       │                                              │
│           │                       ▼                                              │
│           │              ┌─────────────────┐                                     │
│           │              │    EXECUTOR     │                                     │
│           │              │                 │                                     │
│           │              │ ┌─────────────┐ │                                     │
│           │              │ │LocalExecutor│ │                                     │
│           │              │ │CeleryExecutor│ │                                     │
│           │              │ │K8sExecutor  │ │                                     │
│           │              │ └─────────────┘ │                                     │
│           │              └─────────────────┘                                     │
│           │                       │                                              │
│           │                       ▼                                              │
│           │              ┌─────────────────────────────────────────────────────┐ │
│           │              │                 WORKERS                             │ │
│           │              │                                                     │ │
│           │              │ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │ │
│           │              │ │  WORKER 1   │  │  WORKER 2   │  │  WORKER N   │ │ │
│           │              │ │             │  │             │  │             │ │ │
│           │              │ │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │ │ │
│           │              │ │ │ Task A  │ │  │ │ Task B  │ │  │ │ Task C  │ │ │ │
│           │              │ │ │ Task D  │ │  │ │ Task E  │ │  │ │ Task F  │ │ │ │
│           │              │ │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │ │ │
│           │              │ └─────────────┘  └─────────────┘  └─────────────┘ │ │
│           │              └─────────────────────────────────────────────────────┘ │
│           │                                                                      │
│           ▼                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                            MESSAGE BROKER                                   │ │
│  │                         (Redis / RabbitMQ)                                 │ │
│  │                                                                             │ │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐ │ │
│  │  │   Task Queue    │    │  Result Backend │    │    Celery Flower       │ │ │
│  │  │                 │    │                 │    │    (Monitoring)         │ │ │
│  │  │ • Pending Tasks │    │ • Task Results  │    │                         │ │ │
│  │  │ • Task Routing  │    │ • Task States   │    │ • Worker Status         │ │ │
│  │  │ • Priority Queue│    │ • Metadata      │    │ • Queue Monitoring      │ │ │
│  │  └─────────────────┘    └─────────────────┘    └─────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘

                                DATA FLOW
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  1. Scheduler reads DAG files and creates DagRun instances                     │
│  2. Scheduler creates TaskInstance objects for ready tasks                     │
│  3. Executor receives tasks and distributes to Workers                         │
│  4. Workers execute tasks and report status back                               │
│  5. Web Server provides UI for monitoring and management                       │
│  6. All metadata stored in Database for persistence                            │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Core Components**:
- **Web Server**: Flask-based UI and REST API
- **Scheduler**: Orchestrates task execution and manages DAG runs
- **Executor**: Determines how tasks are executed
- **Workers**: Execute individual tasks
- **Metadata Database**: Stores all Airflow metadata
- **Message Broker**: Queues tasks for distributed execution (Celery only)

## ⏰ Scheduling & Execution

**Definition**: Airflow's scheduling system determines when and how DAGs and tasks are executed.

### Scheduling Concepts

```python
from airflow import DAG
from datetime import datetime, timedelta

# Different scheduling intervals
dag_daily = DAG(
    'daily_pipeline',
    schedule_interval='@daily',  # Run once per day at midnight
    start_date=datetime(2024, 1, 1),
    catchup=True  # Backfill historical runs
)

dag_hourly = DAG(
    'hourly_pipeline',
    schedule_interval='@hourly',  # Run every hour
    start_date=datetime(2024, 1, 1),
    catchup=False  # Don't backfill
)

dag_cron = DAG(
    'custom_schedule',
    schedule_interval='0 8 * * 1-5',  # 8 AM on weekdays
    start_date=datetime(2024, 1, 1)
)

dag_manual = DAG(
    'manual_pipeline',
    schedule_interval=None,  # Manual trigger only
    start_date=datetime(2024, 1, 1)
)

# Dynamic scheduling
dag_conditional = DAG(
    'conditional_pipeline',
    schedule_interval=timedelta(hours=6),  # Every 6 hours
    start_date=datetime(2024, 1, 1),
    max_active_runs=1  # Only one run at a time
)
```

### Task Dependencies and Trigger Rules

```python
from airflow.utils.trigger_rule import TriggerRule

# Basic dependencies
task_a >> task_b >> task_c  # Sequential
task_a >> [task_b, task_c] >> task_d  # Parallel then join

# Advanced trigger rules
cleanup_task = BashOperator(
    task_id='cleanup',
    bash_command='rm -rf /tmp/processing/*',
    trigger_rule=TriggerRule.ALL_DONE,  # Run regardless of upstream success/failure
    dag=dag
)

notification_task = EmailOperator(
    task_id='failure_notification',
    to=['admin@company.com'],
    subject='Pipeline Failed',
    html_content='Pipeline failed, please investigate',
    trigger_rule=TriggerRule.ONE_FAILED,  # Run only if upstream task failed
    dag=dag
)
```

## 📡 Data Passing & Communication

### 1. XCom

**Definition**: XCom (Cross-Communication) enables tasks to exchange small amounts of data.

```python
from airflow.operators.python import PythonOperator

def extract_data(**context):
    # Simulate data extraction
    data = {
        'records_processed': 1000,
        'file_path': '/data/processed/output.csv',
        'status': 'success'
    }
    
    # Push to XCom (automatic return)
    return data

def process_data(**context):
    # Pull from XCom
    ti = context['task_instance']
    extracted_data = ti.xcom_pull(task_ids='extract_data')
    
    print(f"Processing {extracted_data['records_processed']} records")
    print(f"Input file: {extracted_data['file_path']}")
    
    # Process and return new data
    return {
        'processed_records': extracted_data['records_processed'],
        'output_file': '/data/final/processed_output.csv'
    }

def load_data(**context):
    # Pull from multiple tasks
    ti = context['task_instance']
    processed_data = ti.xcom_pull(task_ids='process_data')
    
    print(f"Loading {processed_data['processed_records']} records")
    print(f"From file: {processed_data['output_file']}")

# Define tasks
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag
)

process_task = PythonOperator(
    task_id='process_data',
    python_callable=process_data,
    dag=dag
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag
)

extract_task >> process_task >> load_task
```

### 2. Variables

**Definition**: Airflow Variables store global configuration values accessible across DAGs.

```python
from airflow.models import Variable

# Set variables (via UI or programmatically)
Variable.set("data_source_path", "/data/input")
Variable.set("batch_size", "1000")
Variable.set("notification_email", "team@company.com")

# Use variables in tasks
def process_with_config(**context):
    data_path = Variable.get("data_source_path")
    batch_size = int(Variable.get("batch_size"))
    email = Variable.get("notification_email")
    
    print(f"Processing data from {data_path} in batches of {batch_size}")
    return f"Processed data, notification sent to {email}"

# Use in templates
bash_task = BashOperator(
    task_id='process_files',
    bash_command='python process.py --path {{ var.value.data_source_path }} --batch {{ var.value.batch_size }}',
    dag=dag
)
```

### 3. Connections

**Definition**: Connections store credentials and connection information for external systems.

```python
from airflow.hooks.postgres_hook import PostgresHook
from airflow.hooks.S3_hook import S3Hook

def database_operation(**context):
    # Use connection defined in Airflow UI
    postgres_hook = PostgresHook(postgres_conn_id='postgres_default')
    
    # Execute query
    records = postgres_hook.get_records("""
        SELECT COUNT(*) FROM users 
        WHERE created_date = '{{ ds }}'
    """)
    
    print(f"Found {records[0][0]} new users")
    return records[0][0]

def s3_operation(**context):
    # Use S3 connection
    s3_hook = S3Hook(aws_conn_id='aws_default')
    
    # Upload file
    s3_hook.load_file(
        filename='/tmp/processed_data.csv',
        key='processed/{{ ds }}/data.csv',
        bucket_name='data-bucket',
        replace=True
    )
    
    print("File uploaded to S3")
```

## ⚡ Performance Optimization

### 1. Parallelism

**Definition**: Configure parallelism at different levels to optimize resource utilization.

```python
# DAG-level parallelism
dag = DAG(
    'parallel_pipeline',
    max_active_runs=3,  # Max concurrent DAG runs
    max_active_tasks=10,  # Max concurrent tasks per DAG run
    schedule_interval='@hourly'
)

# Task-level parallelism
from airflow.operators.subdag import SubDagOperator

def create_parallel_tasks(parent_dag_id, child_dag_id, start_date, schedule_interval):
    subdag = DAG(
        f"{parent_dag_id}.{child_dag_id}",
        start_date=start_date,
        schedule_interval=schedule_interval
    )
    
    # Create multiple parallel tasks
    for i in range(5):
        task = BashOperator(
            task_id=f'parallel_task_{i}',
            bash_command=f'echo "Processing partition {i}"',
            dag=subdag
        )
    
    return subdag

# Use SubDAG for parallel execution
parallel_subdag = SubDagOperator(
    task_id='parallel_processing',
    subdag=create_parallel_tasks('main_dag', 'parallel_processing', 
                                datetime(2024, 1, 1), '@daily'),
    dag=dag
)
```

### 2. Resource Management

```python
# Configure resource requirements
resource_intensive_task = BashOperator(
    task_id='heavy_computation',
    bash_command='python heavy_processing.py',
    pool='cpu_intensive_pool',  # Use specific resource pool
    priority_weight=10,  # Higher priority
    queue='high_memory',  # Specific queue for high-memory tasks
    dag=dag
)

# Pool configuration (via UI or programmatically)
from airflow.models import Pool

# Create resource pools
Pool.create_or_update_pool(
    name='cpu_intensive_pool',
    slots=4,  # Max 4 concurrent tasks
    description='Pool for CPU-intensive tasks'
)

Pool.create_or_update_pool(
    name='io_intensive_pool',
    slots=10,  # Max 10 concurrent I/O tasks
    description='Pool for I/O-intensive tasks'
)
```

### 3. Task Dependencies

```python
# Optimize dependencies for better parallelism
from airflow.utils.task_group import TaskGroup

with TaskGroup("data_processing", dag=dag) as processing_group:
    # Parallel data processing tasks
    process_users = PythonOperator(
        task_id='process_users',
        python_callable=process_user_data
    )
    
    process_orders = PythonOperator(
        task_id='process_orders',
        python_callable=process_order_data
    )
    
    process_products = PythonOperator(
        task_id='process_products',
        python_callable=process_product_data
    )

# Sequential tasks
extract_task >> processing_group >> load_task
```

## 🛠️ Configuration

**Definition**: Airflow configuration controls behavior, performance, and integration settings.

### Key Configuration Areas

```python
# airflow.cfg or environment variables

# Core settings
AIRFLOW__CORE__EXECUTOR = CeleryExecutor
AIRFLOW__CORE__SQL_ALCHEMY_CONN = postgresql://user:pass@localhost/airflow
AIRFLOW__CORE__DAGS_FOLDER = /opt/airflow/dags
AIRFLOW__CORE__PARALLELISM = 32
AIRFLOW__CORE__DAG_CONCURRENCY = 16
AIRFLOW__CORE__MAX_ACTIVE_RUNS_PER_DAG = 16

# Scheduler settings
AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL = 300
AIRFLOW__SCHEDULER__CATCHUP_BY_DEFAULT = False
AIRFLOW__SCHEDULER__MAX_THREADS = 2

# Webserver settings
AIRFLOW__WEBSERVER__WEB_SERVER_PORT = 8080
AIRFLOW__WEBSERVER__WORKERS = 4
AIRFLOW__WEBSERVER__WORKER_TIMEOUT = 120

# Email settings
AIRFLOW__EMAIL__EMAIL_BACKEND = airflow.utils.email.send_email_smtp
AIRFLOW__SMTP__SMTP_HOST = smtp.gmail.com
AIRFLOW__SMTP__SMTP_PORT = 587
AIRFLOW__SMTP__SMTP_USER = your-email@gmail.com
AIRFLOW__SMTP__SMTP_PASSWORD = your-password
AIRFLOW__SMTP__SMTP_MAIL_FROM = airflow@company.com

# Celery settings (if using CeleryExecutor)
AIRFLOW__CELERY__BROKER_URL = redis://localhost:6379/0
AIRFLOW__CELERY__RESULT_BACKEND = db+postgresql://user:pass@localhost/airflow
AIRFLOW__CELERY__WORKER_CONCURRENCY = 16
```

### Dynamic Configuration

```python
from airflow.configuration import conf

def get_dynamic_config(**context):
    # Read configuration values
    parallelism = conf.getint('core', 'parallelism')
    dag_concurrency = conf.getint('core', 'dag_concurrency')
    
    print(f"Current parallelism: {parallelism}")
    print(f"DAG concurrency: {dag_concurrency}")
    
    # Adjust processing based on configuration
    if parallelism > 16:
        return "high_performance_processing"
    else:
        return "standard_processing"
```

## 📊 Monitoring & Logging

**Definition**: Comprehensive monitoring and logging capabilities for pipeline observability.

### Built-in Monitoring

```python
# Task-level monitoring
def monitored_task(**context):
    import logging
    
    # Get task logger
    logger = logging.getLogger(__name__)
    
    try:
        # Simulate processing
        logger.info("Starting data processing")
        
        # Process data
        records_processed = 1000
        logger.info(f"Processed {records_processed} records")
        
        # Log metrics
        context['task_instance'].log.info(f"METRIC: records_processed={records_processed}")
        
        return {"status": "success", "records": records_processed}
        
    except Exception as e:
        logger.error(f"Task failed: {str(e)}")
        raise

# Custom metrics
def send_custom_metrics(**context):
    from airflow.providers.http.hooks.http import HttpHook
    
    # Send metrics to external system
    http_hook = HttpHook(http_conn_id='metrics_api')
    
    metrics = {
        'dag_id': context['dag'].dag_id,
        'task_id': context['task'].task_id,
        'execution_date': context['execution_date'].isoformat(),
        'duration': context['task_instance'].duration,
        'state': context['task_instance'].state
    }
    
    response = http_hook.run(
        endpoint='/metrics',
        data=metrics,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Metrics sent: {response.status_code}")
```

### Health Checks and Alerting

```python
# Health check task
def health_check(**context):
    from airflow.hooks.postgres_hook import PostgresHook
    
    try:
        # Check database connectivity
        postgres_hook = PostgresHook(postgres_conn_id='postgres_default')
        result = postgres_hook.get_first("SELECT 1")
        
        if result[0] == 1:
            print("Database health check passed")
        else:
            raise Exception("Database health check failed")
            
        # Check external API
        http_hook = HttpHook(http_conn_id='external_api')
        response = http_hook.run(endpoint='/health')
        
        if response.status_code == 200:
            print("External API health check passed")
        else:
            raise Exception(f"External API health check failed: {response.status_code}")
            
        return "healthy"
        
    except Exception as e:
        # Send alert
        send_alert(f"Health check failed: {str(e)}")
        raise

def send_alert(message):
    # Send to Slack, email, or monitoring system
    print(f"ALERT: {message}")
```

## 🚀 When to Use Airflow

**Use Airflow When:**
- **Batch Processing**: ETL/ELT pipelines, data warehousing
- **Complex Dependencies**: Multi-step workflows with conditional logic
- **Scheduling**: Time-based or event-driven pipeline execution
- **Monitoring**: Need visibility into pipeline execution and failures
- **Scalability**: Distributed execution across multiple machines
- **Integration**: Connecting multiple data systems and tools

**Don't Use Airflow For:**
- **Real-time Streaming**: Use Kafka, Spark Streaming, or Flink instead
- **Simple Scripts**: Cron jobs might be sufficient
- **Interactive Workflows**: Jupyter notebooks or similar tools
- **Low-latency Requirements**: Airflow has inherent scheduling overhead

## 🎯 Interview Focus Areas

1. **Architecture**: Components, executors, scaling strategies
2. **DAG Design**: Best practices, dependencies, trigger rules
3. **Task Management**: Operators, XCom, error handling
4. **Scheduling**: Cron expressions, backfill, catchup
5. **Performance**: Parallelism, resource management, optimization
6. **Monitoring**: Logging, alerting, troubleshooting
7. **Integration**: Hooks, connections, external systems
8. **Production**: Deployment, configuration, maintenance
9. **Security**: Authentication, authorization, secrets management
10. **Troubleshooting**: Common issues, debugging techniques

## 📚 Quick References

- [Airflow Documentation](https://airflow.apache.org/docs/)
- [Airflow Operators](https://airflow.apache.org/docs/apache-airflow/stable/operators-and-hooks-ref.html)
- [Airflow Configuration](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html)
- [Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [Airflow Providers](https://airflow.apache.org/docs/apache-airflow-providers/)