# Apache Airflow Interview Questions

## Basic Level Questions (1-3 years experience)

### 1. What is Apache Airflow and why is it used?
**Answer**: Apache Airflow is an open-source platform for developing, scheduling, and monitoring workflows. It allows you to programmatically author, schedule, and monitor data pipelines.

**Key Features**:
- **DAG-based**: Workflows are defined as Directed Acyclic Graphs
- **Scalable**: Can handle complex workflows with dependencies
- **Extensible**: Rich ecosystem of operators and hooks
- **Monitoring**: Web UI for monitoring and troubleshooting
- **Scheduling**: Cron-based and interval-based scheduling

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def extract_data():
    print("Extracting data...")
    return "extracted_data"

def transform_data(**context):
    data = context['task_instance'].xcom_pull(task_ids='extract')
    print(f"Transforming {data}")
    return "transformed_data"

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'simple_etl',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
)

extract_task = PythonOperator(
    task_id='extract',
    python_callable=extract_data,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform',
    python_callable=transform_data,
    dag=dag
)

extract_task >> transform_task
```

### 2. Explain the concept of DAG in Airflow
**Answer**: A DAG (Directed Acyclic Graph) represents a workflow where tasks have dependencies but no cycles. Each node is a task, and edges represent dependencies.

**Key Properties**:
- **Directed**: Dependencies flow in one direction
- **Acyclic**: No circular dependencies
- **Tasks**: Individual units of work
- **Dependencies**: Define execution order

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# DAG with multiple dependencies
dag = DAG('complex_workflow', schedule_interval='@daily')

# Tasks
start = BashOperator(task_id='start', bash_command='echo "Starting"', dag=dag)
task_a = BashOperator(task_id='task_a', bash_command='echo "Task A"', dag=dag)
task_b = BashOperator(task_id='task_b', bash_command='echo "Task B"', dag=dag)
task_c = BashOperator(task_id='task_c', bash_command='echo "Task C"', dag=dag)
end = BashOperator(task_id='end', bash_command='echo "Ending"', dag=dag)

# Dependencies
start >> [task_a, task_b]  # Parallel execution
[task_a, task_b] >> task_c  # Wait for both
task_c >> end
```

### 3. What are Operators in Airflow?
**Answer**: Operators define what actually gets executed in a task. They are the building blocks of DAGs.

**Common Operators**:
- **BashOperator**: Execute bash commands
- **PythonOperator**: Execute Python functions
- **SQLOperator**: Execute SQL queries
- **EmailOperator**: Send emails
- **S3Operator**: Interact with AWS S3

```python
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

# Bash Operator
bash_task = BashOperator(
    task_id='run_script',
    bash_command='python /path/to/script.py',
    dag=dag
)

# Python Operator
def my_function(**context):
    return "Hello from Python"

python_task = PythonOperator(
    task_id='python_task',
    python_callable=my_function,
    dag=dag
)

# SQL Operator
sql_task = PostgresOperator(
    task_id='sql_task',
    postgres_conn_id='postgres_default',
    sql="SELECT COUNT(*) FROM users;",
    dag=dag
)
```

### 4. How do you handle task dependencies in Airflow?
**Answer**: Task dependencies are defined using bitshift operators (`>>`, `<<`) or the `set_upstream`/`set_downstream` methods.

```python
# Method 1: Bitshift operators
task1 >> task2 >> task3  # Sequential
task1 >> [task2, task3]  # Parallel after task1
[task1, task2] >> task3  # task3 waits for both

# Method 2: Explicit methods
task1.set_downstream(task2)
task2.set_upstream(task1)

# Method 3: Using lists for complex dependencies
from airflow.models import Variable

def create_parallel_tasks():
    tasks = []
    for i in range(3):
        task = PythonOperator(
            task_id=f'parallel_task_{i}',
            python_callable=lambda: print(f"Task {i}"),
            dag=dag
        )
        tasks.append(task)
    return tasks

start_task = PythonOperator(task_id='start', python_callable=lambda: None, dag=dag)
parallel_tasks = create_parallel_tasks()
end_task = PythonOperator(task_id='end', python_callable=lambda: None, dag=dag)

start_task >> parallel_tasks >> end_task
```

### 5. What is XCom and how is it used?
**Answer**: XCom (Cross-Communication) allows tasks to exchange small amounts of data. Tasks can push data to XCom and other tasks can pull it.

```python
def push_data(**context):
    data = {"key": "value", "count": 100}
    # Push to XCom
    context['task_instance'].xcom_push(key='my_data', value=data)
    return data  # Also automatically pushed with return_value key

def pull_data(**context):
    # Pull from XCom
    data = context['task_instance'].xcom_pull(
        task_ids='push_task', 
        key='my_data'
    )
    print(f"Received data: {data}")
    
    # Pull return value
    return_value = context['task_instance'].xcom_pull(task_ids='push_task')
    print(f"Return value: {return_value}")

push_task = PythonOperator(
    task_id='push_task',
    python_callable=push_data,
    dag=dag
)

pull_task = PythonOperator(
    task_id='pull_task',
    python_callable=pull_data,
    dag=dag
)

push_task >> pull_task
```

## Intermediate Level Questions (3-5 years experience)

### 6. How do you handle failures and retries in Airflow?
**Answer**: Airflow provides multiple mechanisms for handling failures including retries, retry delays, and failure callbacks.

```python
from airflow.operators.email import EmailOperator

def failure_callback(context):
    """Called when task fails after all retries."""
    print(f"Task {context['task_instance'].task_id} failed!")
    # Send notification, log to external system, etc.

def retry_callback(context):
    """Called on each retry."""
    print(f"Retrying task {context['task_instance'].task_id}")

default_args = {
    'owner': 'data_engineer',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
    'max_retry_delay': timedelta(hours=1),
    'on_failure_callback': failure_callback,
    'on_retry_callback': retry_callback
}

# Task-specific retry configuration
risky_task = PythonOperator(
    task_id='risky_task',
    python_callable=lambda: 1/0,  # Will fail
    retries=5,
    retry_delay=timedelta(seconds=30),
    dag=dag
)

# Email on failure
email_on_failure = EmailOperator(
    task_id='failure_email',
    to=['admin@company.com'],
    subject='DAG Failed',
    html_content='The DAG has failed. Please check logs.',
    trigger_rule='one_failed',  # Runs if any upstream task fails
    dag=dag
)
```

### 7. Explain Airflow Connections and Hooks
**Answer**: Connections store credentials and connection information. Hooks provide interfaces to external systems using these connections.

```python
from airflow.hooks.postgres_hook import PostgresHook
from airflow.hooks.S3_hook import S3Hook
from airflow.models import Connection

# Using PostgresHook
def query_database(**context):
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    
    # Execute query
    records = pg_hook.get_records("SELECT * FROM users LIMIT 10")
    print(f"Found {len(records)} records")
    
    # Execute with parameters
    result = pg_hook.get_first(
        "SELECT COUNT(*) FROM users WHERE created_date > %s",
        parameters=['2024-01-01']
    )
    return result[0]

# Using S3Hook
def upload_to_s3(**context):
    s3_hook = S3Hook(aws_conn_id='aws_default')
    
    # Upload file
    s3_hook.load_file(
        filename='/tmp/data.csv',
        key='data/processed/data.csv',
        bucket_name='my-bucket',
        replace=True
    )
    
    # Check if file exists
    if s3_hook.check_for_key('data/processed/data.csv', 'my-bucket'):
        print("File uploaded successfully")

# Custom Hook
class CustomAPIHook(BaseHook):
    def __init__(self, conn_id):
        self.conn_id = conn_id
        self.connection = self.get_connection(conn_id)
    
    def get_data(self):
        import requests
        response = requests.get(
            f"{self.connection.host}/api/data",
            headers={'Authorization': f'Bearer {self.connection.password}'}
        )
        return response.json()
```

### 8. How do you implement branching in Airflow?
**Answer**: Branching allows conditional execution of tasks based on runtime conditions using BranchPythonOperator.

```python
from airflow.operators.python import BranchPythonOperator
from airflow.operators.dummy import DummyOperator

def decide_branch(**context):
    """Decide which branch to take based on conditions."""
    # Get current hour
    from datetime import datetime
    current_hour = datetime.now().hour
    
    if current_hour < 12:
        return 'morning_task'
    else:
        return 'afternoon_task'

def check_data_quality(**context):
    """Branch based on data quality check."""
    # Simulate data quality check
    data_quality_score = 0.85
    
    if data_quality_score > 0.8:
        return 'high_quality_processing'
    else:
        return 'data_cleaning_required'

# Branching DAG
branch_task = BranchPythonOperator(
    task_id='branch_decision',
    python_callable=decide_branch,
    dag=dag
)

morning_task = DummyOperator(task_id='morning_task', dag=dag)
afternoon_task = DummyOperator(task_id='afternoon_task', dag=dag)

# Quality-based branching
quality_check = BranchPythonOperator(
    task_id='quality_check',
    python_callable=check_data_quality,
    dag=dag
)

high_quality = DummyOperator(task_id='high_quality_processing', dag=dag)
data_cleaning = DummyOperator(task_id='data_cleaning_required', dag=dag)

# Dependencies
branch_task >> [morning_task, afternoon_task]
quality_check >> [high_quality, data_cleaning]
```

### 9. How do you monitor and troubleshoot Airflow DAGs?
**Answer**: Airflow provides multiple monitoring and troubleshooting tools including the web UI, logs, and metrics.

```python
import logging
from airflow.models import Variable
from airflow.configuration import conf

def monitored_task(**context):
    """Task with comprehensive monitoring."""
    logger = logging.getLogger(__name__)
    
    try:
        # Log task start
        logger.info(f"Starting task {context['task_instance'].task_id}")
        
        # Get task metadata
        dag_run = context['dag_run']
        logger.info(f"DAG Run ID: {dag_run.run_id}")
        logger.info(f"Execution Date: {context['execution_date']}")
        
        # Simulate work with progress logging
        import time
        for i in range(5):
            logger.info(f"Processing step {i+1}/5")
            time.sleep(1)
        
        # Log success metrics
        Variable.set("last_successful_run", str(datetime.now()))
        logger.info("Task completed successfully")
        
    except Exception as e:
        logger.error(f"Task failed with error: {str(e)}")
        # Push error details to XCom for downstream handling
        context['task_instance'].xcom_push(
            key='error_details',
            value={'error': str(e), 'timestamp': str(datetime.now())}
        )
        raise

# Health check task
def health_check(**context):
    """Monitor system health."""
    import psutil
    
    # Check system resources
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    
    logger = logging.getLogger(__name__)
    logger.info(f"CPU Usage: {cpu_percent}%")
    logger.info(f"Memory Usage: {memory_percent}%")
    
    # Alert if resources are high
    if cpu_percent > 80 or memory_percent > 80:
        logger.warning("High resource usage detected!")
        return "resource_alert"
    
    return "healthy"

# SLA monitoring
sla_task = PythonOperator(
    task_id='sla_monitored_task',
    python_callable=monitored_task,
    sla=timedelta(minutes=30),  # Task should complete within 30 minutes
    dag=dag
)
```

### 10. How do you implement dynamic DAGs in Airflow?
**Answer**: Dynamic DAGs are created programmatically based on external configuration, allowing for flexible and scalable workflows.

```python
import os
import yaml
from airflow import DAG
from airflow.operators.python import PythonOperator

# Load configuration
def load_dag_config():
    config_path = '/opt/airflow/config/dag_config.yaml'
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

# Dynamic task creation
def create_processing_task(table_name, dag):
    def process_table(**context):
        print(f"Processing table: {table_name}")
        # Add actual processing logic here
        return f"Processed {table_name}"
    
    return PythonOperator(
        task_id=f'process_{table_name}',
        python_callable=process_table,
        dag=dag
    )

# Create DAGs dynamically
config = load_dag_config()

for dag_config in config.get('dags', []):
    dag_id = dag_config['dag_id']
    tables = dag_config['tables']
    
    # Create DAG
    dag = DAG(
        dag_id=dag_id,
        schedule_interval=dag_config.get('schedule', '@daily'),
        start_date=datetime(2024, 1, 1),
        catchup=False
    )
    
    # Create tasks dynamically
    tasks = []
    for table in tables:
        task = create_processing_task(table, dag)
        tasks.append(task)
    
    # Set up dependencies
    if len(tasks) > 1:
        for i in range(len(tasks) - 1):
            tasks[i] >> tasks[i + 1]
    
    # Make DAG available globally
    globals()[dag_id] = dag

# Example config file (dag_config.yaml):
"""
dags:
  - dag_id: "process_sales_data"
    schedule: "@daily"
    tables:
      - "sales_raw"
      - "sales_processed"
      - "sales_aggregated"
  - dag_id: "process_user_data"
    schedule: "@hourly"
    tables:
      - "users_raw"
      - "users_cleaned"
"""
```

## Advanced Level Questions (5+ years experience)

### 11. How do you implement custom operators in Airflow?
**Answer**: Custom operators extend BaseOperator to encapsulate specific business logic and make DAGs more readable and reusable.

```python
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.postgres_hook import PostgresHook

class DataQualityOperator(BaseOperator):
    """Custom operator for data quality checks."""
    
    template_fields = ['sql', 'table_name']
    
    @apply_defaults
    def __init__(self,
                 postgres_conn_id='postgres_default',
                 table_name='',
                 sql='',
                 min_rows=1,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.postgres_conn_id = postgres_conn_id
        self.table_name = table_name
        self.sql = sql
        self.min_rows = min_rows
    
    def execute(self, context):
        hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        
        # Check row count
        count_sql = f"SELECT COUNT(*) FROM {self.table_name}"
        row_count = hook.get_first(count_sql)[0]
        
        if row_count < self.min_rows:
            raise ValueError(f"Data quality check failed: {row_count} rows < {self.min_rows}")
        
        # Run custom SQL check
        if self.sql:
            result = hook.get_first(self.sql)
            if not result[0]:
                raise ValueError("Custom data quality check failed")
        
        self.log.info(f"Data quality check passed: {row_count} rows")
        return row_count

# Usage
quality_check = DataQualityOperator(
    task_id='check_data_quality',
    table_name='sales_data',
    sql="SELECT COUNT(*) > 0 FROM sales_data WHERE date = '{{ ds }}'",
    min_rows=100,
    dag=dag
)
```

### 12. How do you handle large-scale data processing with Airflow?
**Answer**: For large-scale processing, use external compute engines and implement proper resource management and monitoring.

```python
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

# Spark processing for large datasets
spark_task = SparkSubmitOperator(
    task_id='process_large_dataset',
    application='/opt/spark/apps/data_processing.py',
    conn_id='spark_default',
    conf={
        'spark.executor.memory': '4g',
        'spark.executor.cores': '2',
        'spark.executor.instances': '10',
        'spark.sql.adaptive.enabled': 'true',
        'spark.sql.adaptive.coalescePartitions.enabled': 'true'
    },
    application_args=['--input', 's3://bucket/input/', '--output', 's3://bucket/output/'],
    dag=dag
)

# Kubernetes for scalable processing
k8s_task = KubernetesPodOperator(
    task_id='k8s_data_processing',
    image='my-data-processing:latest',
    cmds=['python'],
    arguments=['process_data.py'],
    env_vars={
        'INPUT_PATH': 's3://bucket/input/',
        'OUTPUT_PATH': 's3://bucket/output/'
    },
    resources={
        'request_memory': '2Gi',
        'request_cpu': '1',
        'limit_memory': '4Gi',
        'limit_cpu': '2'
    },
    dag=dag
)

# Chunked processing for very large datasets
def create_chunk_tasks(total_chunks):
    tasks = []
    for i in range(total_chunks):
        task = PythonOperator(
            task_id=f'process_chunk_{i}',
            python_callable=process_chunk,
            op_args=[i],
            dag=dag
        )
        tasks.append(task)
    return tasks

def process_chunk(chunk_id, **context):
    """Process a specific chunk of data."""
    print(f"Processing chunk {chunk_id}")
    # Implement chunk processing logic
    return f"Chunk {chunk_id} processed"

# Create parallel chunk processing
chunk_tasks = create_chunk_tasks(10)

# Aggregate results
def aggregate_results(**context):
    """Aggregate results from all chunks."""
    results = []
    for i in range(10):
        result = context['task_instance'].xcom_pull(task_ids=f'process_chunk_{i}')
        results.append(result)
    
    print(f"Aggregated {len(results)} chunk results")
    return results

aggregate_task = PythonOperator(
    task_id='aggregate_results',
    python_callable=aggregate_results,
    dag=dag
)

# Set up dependencies
chunk_tasks >> aggregate_task
```

This comprehensive set covers Airflow fundamentals through advanced concepts with practical data engineering examples.