# Apache Airflow Interview Questions

## Table of Contents

1. [Basic Airflow Concepts](#basic-airflow-concepts)
2. [DAGs and Task Management](#dags-and-task-management)
3. [Operators and Hooks](#operators-and-hooks)
4. [Scheduling and Dependencies](#scheduling-and-dependencies)
5. [Monitoring and Troubleshooting](#monitoring-and-troubleshooting)
6. [Data Engineering Use Cases](#data-engineering-use-cases)

---

## Basic Airflow Concepts

### Q1: What is Apache Airflow and what problems does it solve?

**Answer:**
Apache Airflow is an open-source workflow orchestration platform for developing, scheduling, and monitoring batch-oriented workflows. It solves complex data pipeline management challenges.

**Key Problems Solved:**
- **Workflow Orchestration**: Manage complex dependencies between tasks
- **Scheduling**: Reliable, cron-like scheduling with backfill capabilities
- **Monitoring**: Visual monitoring and alerting for pipeline failures
- **Scalability**: Distributed execution across multiple workers
- **Maintainability**: Code-based workflow definition with version control

**Code Example:**
```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# Define default arguments
default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

# Create DAG
dag = DAG(
    'data_pipeline_example',
    default_args=default_args,
    description='A simple data pipeline',
    schedule_interval='@daily',
    catchup=False,
    tags=['data_engineering', 'etl']
)

def extract_data(**context):
    """Extract data from source"""
    print(f"Extracting data for {context['ds']}")
    # Simulate data extraction
    return "extracted_data.csv"

def transform_data(**context):
    """Transform extracted data"""
    ti = context['ti']
    filename = ti.xcom_pull(task_ids='extract_task')
    print(f"Transforming {filename}")
    return "transformed_data.csv"

def load_data(**context):
    """Load transformed data"""
    ti = context['ti']
    filename = ti.xcom_pull(task_ids='transform_task')
    print(f"Loading {filename} to warehouse")
    return "success"

# Define tasks
extract_task = PythonOperator(
    task_id='extract_task',
    python_callable=extract_data,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform_task',
    python_callable=transform_data,
    dag=dag
)

load_task = PythonOperator(
    task_id='load_task',
    python_callable=load_data,
    dag=dag
)

# Set dependencies
extract_task >> transform_task >> load_task
```

### Q2: Explain Airflow's architecture and core components.

**Answer:**
Airflow follows a distributed architecture with multiple components working together to execute and monitor workflows.

**Core Components:**
- **Web Server**: UI for monitoring and managing DAGs
- **Scheduler**: Orchestrates task execution based on dependencies
- **Executor**: Determines how tasks are executed (Local, Celery, Kubernetes)
- **Metadata Database**: Stores DAG definitions, task states, and logs
- **Workers**: Execute tasks (in distributed setups)

**Code Example:**
```python
# airflow.cfg configuration example
[core]
dags_folder = /opt/airflow/dags
base_log_folder = /opt/airflow/logs
executor = CeleryExecutor
sql_alchemy_conn = postgresql://airflow:password@postgres:5432/airflow

[celery]
broker_url = redis://redis:6379/0
result_backend = db+postgresql://airflow:password@postgres:5432/airflow

[webserver]
web_server_port = 8080
base_url = http://localhost:8080

[scheduler]
dag_dir_list_interval = 300
catchup_by_default = False
max_active_runs_per_dag = 1
```

```python
# Custom executor example
from airflow.executors.base_executor import BaseExecutor
from airflow.utils.state import State
import subprocess

class CustomExecutor(BaseExecutor):
    """Custom executor for specific requirements"""
    
    def start(self):
        """Initialize executor"""
        self.log.info("Starting Custom Executor")
    
    def execute_async(self, key, command, queue=None, executor_config=None):
        """Execute task asynchronously"""
        self.log.info(f"Executing task {key}")
        
        # Custom execution logic
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Track running tasks
        self.running[key] = process
    
    def sync(self):
        """Sync task states"""
        for key, process in list(self.running.items()):
            if process.poll() is not None:
                if process.returncode == 0:
                    self.change_state(key, State.SUCCESS)
                else:
                    self.change_state(key, State.FAILED)
                del self.running[key]
    
    def end(self):
        """Cleanup executor"""
        self.log.info("Shutting down Custom Executor")
```

### Q3: What are the different types of Airflow executors and when to use each?

**Answer:**
Airflow executors determine how and where tasks are executed, each suited for different deployment scenarios and scalability requirements.

**Executor Types:**
- **SequentialExecutor**: Single-threaded, development only
- **LocalExecutor**: Multi-threaded, single machine
- **CeleryExecutor**: Distributed across multiple workers
- **KubernetesExecutor**: Dynamic pod creation in Kubernetes
- **CeleryKubernetesExecutor**: Hybrid approach

**Code Example:**
```python
# LocalExecutor configuration
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import time
import concurrent.futures

def cpu_intensive_task(task_id):
    """Simulate CPU-intensive work"""
    start_time = time.time()
    # Simulate work
    sum(i * i for i in range(1000000))
    duration = time.time() - start_time
    print(f"Task {task_id} completed in {duration:.2f} seconds")
    return f"Task {task_id} result"

# DAG for testing executor performance
dag = DAG(
    'executor_performance_test',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    max_active_runs=1,
    concurrency=4  # LocalExecutor can run 4 tasks in parallel
)

# Create multiple parallel tasks
for i in range(8):
    task = PythonOperator(
        task_id=f'parallel_task_{i}',
        python_callable=cpu_intensive_task,
        op_args=[f'task_{i}'],
        dag=dag
    )

# CeleryExecutor configuration example
celery_dag = DAG(
    'celery_distributed_processing',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@hourly',
    max_active_runs=1
)

def distributed_task(worker_id, data_chunk):
    """Task designed for distributed execution"""
    import socket
    hostname = socket.gethostname()
    
    print(f"Processing chunk {data_chunk} on worker {worker_id} at {hostname}")
    
    # Simulate distributed processing
    time.sleep(2)
    
    return {
        'worker_id': worker_id,
        'hostname': hostname,
        'processed_items': len(data_chunk),
        'status': 'completed'
    }

# Create tasks for different workers
for worker_id in range(5):
    task = PythonOperator(
        task_id=f'distributed_worker_{worker_id}',
        python_callable=distributed_task,
        op_args=[worker_id, list(range(worker_id * 100, (worker_id + 1) * 100))],
        dag=celery_dag,
        # Celery-specific configuration
        queue='data_processing',  # Route to specific worker queue
        pool='cpu_intensive_pool'  # Use specific resource pool
    )

# KubernetesExecutor example
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

k8s_dag = DAG(
    'kubernetes_data_processing',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily'
)

# Task that runs in Kubernetes pod
k8s_task = KubernetesPodOperator(
    task_id='data_processing_pod',
    name='data-processor',
    namespace='airflow',
    image='python:3.9-slim',
    cmds=['python'],
    arguments=['-c', '''
import pandas as pd
import time

print("Starting data processing in Kubernetes pod...")
# Simulate data processing
data = pd.DataFrame({'values': range(1000)})
result = data['values'].sum()
print(f"Processed {len(data)} records, sum: {result}")
time.sleep(5)
print("Processing completed")
    '''],
    # Resource specifications
    resources={
        'request_memory': '512Mi',
        'request_cpu': '500m',
        'limit_memory': '1Gi',
        'limit_cpu': '1000m'
    },
    dag=k8s_dag
)
```

## DAGs and Task Management

### Q4: How do you design efficient DAGs with proper task dependencies?

**Answer:**
Efficient DAG design involves proper task granularity, dependency management, resource allocation, and error handling strategies.

**Design Principles:**
- **Atomic Tasks**: Each task should do one thing well
- **Idempotency**: Tasks should produce same result when re-run
- **Dependency Management**: Clear, minimal dependencies
- **Resource Efficiency**: Appropriate resource allocation
- **Error Handling**: Proper retry and failure strategies

**Code Example:**
```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.email import EmailOperator
from airflow.sensors.filesystem import FileSensor
from airflow.utils.trigger_rule import TriggerRule
import pandas as pd
import os

default_args = {
    'owner': 'data_engineering',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
    'max_retry_delay': timedelta(hours=1)
}

dag = DAG(
    'efficient_data_pipeline',
    default_args=default_args,
    description='Efficiently designed data pipeline',
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    catchup=False,
    max_active_runs=1,
    tags=['production', 'data_pipeline']
)

# Data validation functions
def validate_source_data(**context):
    """Validate source data quality"""
    execution_date = context['ds']
    file_path = f"/data/source/data_{execution_date}.csv"
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Source file not found: {file_path}")
    
    # Load and validate data
    df = pd.read_csv(file_path)
    
    # Data quality checks
    if df.empty:
        raise ValueError("Source data is empty")
    
    if df.isnull().sum().sum() > len(df) * 0.1:  # More than 10% nulls
        raise ValueError("Too many null values in source data")
    
    print(f"Validation passed: {len(df)} records, {df.columns.tolist()}")
    return file_path

def determine_processing_strategy(**context):
    """Branch based on data size"""
    ti = context['ti']
    file_path = ti.xcom_pull(task_ids='validate_data')
    
    df = pd.read_csv(file_path)
    
    if len(df) > 100000:
        return 'large_data_processing'
    else:
        return 'small_data_processing'

def process_small_dataset(**context):
    """Process small datasets efficiently"""
    ti = context['ti']
    file_path = ti.xcom_pull(task_ids='validate_data')
    
    df = pd.read_csv(file_path)
    
    # Simple processing for small data
    processed_df = df.groupby('category').agg({
        'amount': ['sum', 'mean', 'count']
    }).round(2)
    
    output_path = f"/data/processed/small_batch_{context['ds']}.csv"
    processed_df.to_csv(output_path)
    
    print(f"Small dataset processed: {len(processed_df)} categories")
    return output_path

def process_large_dataset(**context):
    """Process large datasets with chunking"""
    ti = context['ti']
    file_path = ti.xcom_pull(task_ids='validate_data')
    
    # Process in chunks for memory efficiency
    chunk_size = 10000
    processed_chunks = []
    
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        # Process each chunk
        chunk_result = chunk.groupby('category').agg({
            'amount': ['sum', 'mean', 'count']
        })
        processed_chunks.append(chunk_result)
    
    # Combine results
    final_result = pd.concat(processed_chunks).groupby(level=0).sum()
    
    output_path = f"/data/processed/large_batch_{context['ds']}.csv"
    final_result.to_csv(output_path)
    
    print(f"Large dataset processed: {len(final_result)} categories")
    return output_path

def quality_check_results(**context):
    """Validate processed results"""
    ti = context['ti']
    
    # Get output from either processing branch
    small_output = ti.xcom_pull(task_ids='small_data_processing')
    large_output = ti.xcom_pull(task_ids='large_data_processing')
    
    output_path = small_output or large_output
    
    if not output_path or not os.path.exists(output_path):
        raise ValueError("Processed output not found")
    
    df = pd.read_csv(output_path)
    
    # Quality checks
    if df.empty:
        raise ValueError("Processed data is empty")
    
    if (df < 0).any().any():  # Check for negative values where inappropriate
        raise ValueError("Invalid negative values found")
    
    print(f"Quality check passed: {len(df)} processed records")
    return output_path

def load_to_warehouse(**context):
    """Load processed data to warehouse"""
    ti = context['ti']
    file_path = ti.xcom_pull(task_ids='quality_check')
    
    # Simulate warehouse loading
    df = pd.read_csv(file_path)
    
    # In real scenario, this would connect to actual warehouse
    print(f"Loading {len(df)} records to data warehouse")
    
    # Simulate loading time
    import time
    time.sleep(2)
    
    print("Data successfully loaded to warehouse")
    return len(df)

# Define tasks with proper dependencies

# 1. Wait for source file
wait_for_file = FileSensor(
    task_id='wait_for_source_file',
    filepath='/data/source/data_{{ ds }}.csv',
    fs_conn_id='fs_default',
    poke_interval=60,
    timeout=300,
    dag=dag
)

# 2. Validate source data
validate_data = PythonOperator(
    task_id='validate_data',
    python_callable=validate_source_data,
    dag=dag
)

# 3. Determine processing strategy
branch_task = BranchPythonOperator(
    task_id='determine_strategy',
    python_callable=determine_processing_strategy,
    dag=dag
)

# 4a. Small data processing
small_data_processing = PythonOperator(
    task_id='small_data_processing',
    python_callable=process_small_dataset,
    dag=dag
)

# 4b. Large data processing
large_data_processing = PythonOperator(
    task_id='large_data_processing',
    python_callable=process_large_dataset,
    dag=dag
)

# 5. Join branches
join_branches = DummyOperator(
    task_id='join_processing_branches',
    trigger_rule=TriggerRule.NONE_FAILED_OR_SKIPPED,
    dag=dag
)

# 6. Quality check
quality_check = PythonOperator(
    task_id='quality_check',
    python_callable=quality_check_results,
    trigger_rule=TriggerRule.NONE_FAILED_OR_SKIPPED,
    dag=dag
)

# 7. Load to warehouse
load_warehouse = PythonOperator(
    task_id='load_warehouse',
    python_callable=load_to_warehouse,
    dag=dag
)

# 8. Success notification
success_email = EmailOperator(
    task_id='success_notification',
    to=['data-team@company.com'],
    subject='Data Pipeline Success - {{ ds }}',
    html_content='''
    <h3>Data Pipeline Completed Successfully</h3>
    <p>Date: {{ ds }}</p>
    <p>Records processed: {{ ti.xcom_pull(task_ids='load_warehouse') }}</p>
    <p>Pipeline duration: {{ (ti.end_date - ti.start_date).total_seconds() }} seconds</p>
    ''',
    dag=dag
)

# Set up dependencies
wait_for_file >> validate_data >> branch_task
branch_task >> [small_data_processing, large_data_processing]
[small_data_processing, large_data_processing] >> join_branches
join_branches >> quality_check >> load_warehouse >> success_email
```

### Q5: How do you handle dynamic task generation in Airflow?

**Answer:**
Dynamic task generation allows creating tasks at runtime based on external data or conditions, enabling flexible and scalable workflows.

**Code Example:**
```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
import json

default_args = {
    'owner': 'data_team',
    'start_date': datetime(2023, 1, 1),
    'retries': 1
}

dag = DAG(
    'dynamic_task_generation',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
)

def get_processing_config(**context):
    """Get dynamic configuration for task generation"""
    # This could come from database, API, or file
    config = {
        'data_sources': [
            {'name': 'customers', 'table': 'customer_data', 'priority': 'high'},
            {'name': 'orders', 'table': 'order_data', 'priority': 'medium'},
            {'name': 'products', 'table': 'product_data', 'priority': 'low'},
            {'name': 'inventory', 'table': 'inventory_data', 'priority': 'high'}
        ],
        'processing_date': context['ds']
    }
    
    # Store config in XCom for other tasks
    return config

def process_data_source(source_name, table_name, priority, processing_date):
    """Process individual data source"""
    print(f"Processing {source_name} from {table_name}")
    print(f"Priority: {priority}, Date: {processing_date}")
    
    # Simulate different processing times based on priority
    import time
    if priority == 'high':
        time.sleep(1)
    elif priority == 'medium':
        time.sleep(2)
    else:
        time.sleep(3)
    
    # Simulate processing result
    processed_records = hash(source_name) % 1000
    print(f"Processed {processed_records} records for {source_name}")
    
    return {
        'source': source_name,
        'records_processed': processed_records,
        'status': 'completed'
    }

def aggregate_results(**context):
    """Aggregate results from all dynamic tasks"""
    ti = context['ti']
    config = ti.xcom_pull(task_ids='get_config')
    
    total_records = 0
    results = []
    
    # Pull results from all dynamic tasks
    for source in config['data_sources']:
        task_id = f"process_{source['name']}"
        result = ti.xcom_pull(task_ids=task_id)
        if result:
            total_records += result['records_processed']
            results.append(result)
    
    print(f"Total records processed: {total_records}")
    print(f"Sources processed: {len(results)}")
    
    return {
        'total_records': total_records,
        'sources_count': len(results),
        'details': results
    }

# Static task to get configuration
get_config_task = PythonOperator(
    task_id='get_config',
    python_callable=get_processing_config,
    dag=dag
)

# Generate dynamic tasks based on configuration
def create_dynamic_tasks():
    """Create tasks dynamically based on configuration"""
    # This would typically read from Variable or external source
    # For demo, using static config
    sample_config = {
        'data_sources': [
            {'name': 'customers', 'table': 'customer_data', 'priority': 'high'},
            {'name': 'orders', 'table': 'order_data', 'priority': 'medium'},
            {'name': 'products', 'table': 'product_data', 'priority': 'low'}
        ]
    }
    
    dynamic_tasks = []
    
    for source in sample_config['data_sources']:
        task = PythonOperator(
            task_id=f"process_{source['name']}",
            python_callable=process_data_source,
            op_args=[
                source['name'],
                source['table'],
                source['priority'],
                '{{ ds }}'
            ],
            dag=dag
        )
        dynamic_tasks.append(task)
        
        # Set dependency from config task
        get_config_task >> task
    
    return dynamic_tasks

# Create dynamic tasks
dynamic_processing_tasks = create_dynamic_tasks()

# Aggregation task
aggregate_task = PythonOperator(
    task_id='aggregate_results',
    python_callable=aggregate_results,
    dag=dag
)

# Set dependencies: all dynamic tasks must complete before aggregation
for task in dynamic_processing_tasks:
    task >> aggregate_task

# Alternative approach using TaskGroup for better organization
from airflow.utils.task_group import TaskGroup

def create_task_group_approach():
    """Alternative approach using TaskGroup"""
    
    dag_v2 = DAG(
        'dynamic_with_task_groups',
        default_args=default_args,
        schedule_interval='@daily',
        catchup=False
    )
    
    with TaskGroup('data_processing_group', dag=dag_v2) as processing_group:
        
        # Dynamic task creation within task group
        sources = ['customers', 'orders', 'products', 'inventory']
        
        for source in sources:
            PythonOperator(
                task_id=f'process_{source}',
                python_callable=lambda source=source: print(f"Processing {source}"),
                dag=dag_v2
            )
    
    # Tasks outside the group
    start_task = PythonOperator(
        task_id='start_processing',
        python_callable=lambda: print("Starting dynamic processing"),
        dag=dag_v2
    )
    
    end_task = PythonOperator(
        task_id='end_processing',
        python_callable=lambda: print("Completed dynamic processing"),
        dag=dag_v2
    )
    
    # Set dependencies
    start_task >> processing_group >> end_task
    
    return dag_v2

# Example of runtime dynamic task generation
def runtime_dynamic_generation(**context):
    """Generate tasks at runtime based on external data"""
    from airflow.models import DagBag
    from airflow.operators.python import PythonOperator
    
    # Get current DAG
    dag_bag = DagBag()
    current_dag = dag_bag.get_dag('dynamic_task_generation')
    
    # Simulate getting dynamic data (could be from API, database, etc.)
    external_data = [
        {'region': 'us-east', 'priority': 1},
        {'region': 'us-west', 'priority': 2},
        {'region': 'europe', 'priority': 1},
        {'region': 'asia', 'priority': 3}
    ]
    
    # Create tasks for each region
    for data in external_data:
        task_id = f"process_region_{data['region']}"
        
        # Check if task already exists
        if task_id not in current_dag.task_dict:
            new_task = PythonOperator(
                task_id=task_id,
                python_callable=lambda region=data['region'], priority=data['priority']: 
                    print(f"Processing region {region} with priority {priority}"),
                dag=current_dag
            )
            
            # Add to DAG
            current_dag.add_task(new_task)
    
    return f"Created tasks for {len(external_data)} regions"

# Runtime generation task
runtime_task = PythonOperator(
    task_id='runtime_generation',
    python_callable=runtime_dynamic_generation,
    dag=dag
)
```

## Operators and Hooks

### Q6: Explain different types of Airflow operators and when to use each.

**Answer:**
Airflow operators define what actually gets executed in each task. Different operators are optimized for specific types of work and integrations.

**Operator Categories:**
- **Action Operators**: Execute specific actions (PythonOperator, BashOperator)
- **Transfer Operators**: Move data between systems
- **Sensor Operators**: Wait for conditions or external events
- **Branch Operators**: Implement conditional logic

**Code Example:**
```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.sensors.filesystem import FileSensor
from airflow.sensors.sql import SqlSensor
from airflow.operators.dummy import DummyOperator
import pandas as pd
import requests

default_args = {
    'owner': 'data_team',
    'start_date': datetime(2023, 1, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'operator_examples',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
)

# 1. PythonOperator - Execute Python functions
def extract_api_data(**context):
    """Extract data from API"""
    import requests
    import json
    
    api_url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Extracted {len(data)} records from API")
        
        # Save to file for next task
        filename = f"/tmp/api_data_{context['ds']}.json"
        with open(filename, 'w') as f:
            json.dump(data, f)
        
        return filename
    else:
        raise Exception(f"API request failed: {response.status_code}")

extract_data = PythonOperator(
    task_id='extract_api_data',
    python_callable=extract_api_data,
    dag=dag
)

# 2. BashOperator - Execute shell commands
process_with_bash = BashOperator(
    task_id='process_with_bash',
    bash_command='''
    echo "Processing data for {{ ds }}"
    
    # Create processing directory
    mkdir -p /tmp/processed/{{ ds }}
    
    # Simulate data processing with shell tools
    if [ -f "/tmp/api_data_{{ ds }}.json" ]; then
        echo "File found, processing..."
        # Count records using jq
        record_count=$(cat /tmp/api_data_{{ ds }}.json | jq '. | length')
        echo "Record count: $record_count"
        
        # Create summary file
        echo "Processing completed on $(date)" > /tmp/processed/{{ ds }}/summary.txt
        echo "Records processed: $record_count" >> /tmp/processed/{{ ds }}/summary.txt
    else
        echo "Input file not found!"
        exit 1
    fi
    ''',
    dag=dag
)

# 3. PostgresOperator - Execute SQL commands
create_table = PostgresOperator(
    task_id='create_staging_table',
    postgres_conn_id='postgres_default',
    sql='''
    CREATE TABLE IF NOT EXISTS staging_posts (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        title TEXT,
        body TEXT,
        created_date DATE DEFAULT CURRENT_DATE
    );
    
    -- Clear existing data for this date
    DELETE FROM staging_posts WHERE created_date = '{{ ds }}';
    ''',
    dag=dag
)

# 4. Custom operator for data loading
def load_json_to_postgres(**context):
    """Load JSON data to PostgreSQL"""
    from airflow.providers.postgres.hooks.postgres import PostgresHook
    import json
    
    # Get filename from previous task
    ti = context['ti']
    filename = ti.xcom_pull(task_ids='extract_api_data')
    
    # Load JSON data
    with open(filename, 'r') as f:
        data = json.load(f)
    
    # Connect to PostgreSQL
    postgres_hook = PostgresHook(postgres_conn_id='postgres_default')
    
    # Insert data
    insert_sql = '''
    INSERT INTO staging_posts (id, user_id, title, body, created_date)
    VALUES (%s, %s, %s, %s, %s)
    '''
    
    for record in data:
        postgres_hook.run(insert_sql, parameters=(
            record['id'],
            record['userId'],
            record['title'],
            record['body'],
            context['ds']
        ))
    
    print(f"Loaded {len(data)} records to PostgreSQL")
    return len(data)

load_to_postgres = PythonOperator(
    task_id='load_to_postgres',
    python_callable=load_json_to_postgres,
    dag=dag
)

# 5. SqlSensor - Wait for data condition
wait_for_data = SqlSensor(
    task_id='wait_for_sufficient_data',
    conn_id='postgres_default',
    sql='''
    SELECT COUNT(*) FROM staging_posts 
    WHERE created_date = '{{ ds }}'
    ''',
    success_criteria=lambda x: x[0][0] > 50,  # Wait for at least 50 records
    poke_interval=30,
    timeout=300,
    dag=dag
)

# 6. SimpleHttpOperator - Make HTTP requests
api_health_check = SimpleHttpOperator(
    task_id='api_health_check',
    http_conn_id='http_default',
    endpoint='posts/1',
    method='GET',
    headers={'Content-Type': 'application/json'},
    xcom_push=True,
    dag=dag
)

# 7. Custom transfer operator
class JsonToPostgresOperator(PythonOperator):
    """Custom operator for JSON to PostgreSQL transfer"""
    
    def __init__(self, source_file, target_table, postgres_conn_id, *args, **kwargs):
        self.source_file = source_file
        self.target_table = target_table
        self.postgres_conn_id = postgres_conn_id
        
        super().__init__(
            python_callable=self._transfer_data,
            *args, **kwargs
        )
    
    def _transfer_data(self, **context):
        """Transfer data from JSON to PostgreSQL"""
        from airflow.providers.postgres.hooks.postgres import PostgresHook
        import json
        
        # Load source data
        with open(self.source_file.format(**context), 'r') as f:
            data = json.load(f)
        
        # Connect to target database
        postgres_hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        
        # Dynamic insert based on data structure
        if data:
            columns = list(data[0].keys())
            placeholders = ', '.join(['%s'] * len(columns))
            
            insert_sql = f'''
            INSERT INTO {self.target_table} ({', '.join(columns)})
            VALUES ({placeholders})
            '''
            
            for record in data:
                values = [record[col] for col in columns]
                postgres_hook.run(insert_sql, parameters=values)
        
        return len(data)

# Use custom operator
custom_transfer = JsonToPostgresOperator(
    task_id='custom_json_transfer',
    source_file='/tmp/api_data_{ds}.json',
    target_table='custom_staging',
    postgres_conn_id='postgres_default',
    dag=dag
)

# 8. EmailOperator - Send notifications
send_report = EmailOperator(
    task_id='send_completion_report',
    to=['data-team@company.com'],
    subject='Data Pipeline Completed - {{ ds }}',
    html_content='''
    <h2>Daily Data Pipeline Report</h2>
    <p><strong>Date:</strong> {{ ds }}</p>
    <p><strong>Records Processed:</strong> {{ ti.xcom_pull(task_ids='load_to_postgres') }}</p>
    <p><strong>Status:</strong> Completed Successfully</p>
    
    <h3>Task Summary:</h3>
    <ul>
        <li>API Data Extraction: ✓</li>
        <li>Bash Processing: ✓</li>
        <li>Database Loading: ✓</li>
        <li>Data Validation: ✓</li>
    </ul>
    
    <p>Pipeline completed at {{ ts }}</p>
    ''',
    dag=dag
)

# 9. FileSensor - Wait for file availability
wait_for_config = FileSensor(
    task_id='wait_for_config_file',
    filepath='/tmp/config_{{ ds }}.json',
    fs_conn_id='fs_default',
    poke_interval=60,
    timeout=300,
    dag=dag
)

# Set up dependencies
extract_data >> process_with_bash
extract_data >> create_table >> load_to_postgres
load_to_postgres >> wait_for_data >> send_report
api_health_check >> extract_data
wait_for_config >> extract_data
```

### Q7: How do you create custom operators and hooks in Airflow?

**Answer:**
Custom operators and hooks extend Airflow's functionality for specific business requirements or integrations not covered by existing operators.

**Code Example:**
```python
from airflow.models import BaseOperator
from airflow.hooks.base import BaseHook
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException
import requests
import pandas as pd
import boto3
from typing import Any, Dict, Optional

# Custom Hook for external API
class CustomAPIHook(BaseHook):
    """Custom hook for interacting with external API"""
    
    def __init__(self, api_conn_id: str = 'api_default'):
        super().__init__()
        self.api_conn_id = api_conn_id
        self._base_url = None
        self._session = None
    
    def get_conn(self):
        """Get API connection"""
        if self._session is None:
            connection = self.get_connection(self.api_conn_id)
            
            self._base_url = f"{connection.schema}://{connection.host}"
            if connection.port:
                self._base_url += f":{connection.port}"
            
            self._session = requests.Session()
            
            # Add authentication if provided
            if connection.login and connection.password:
                self._session.auth = (connection.login, connection.password)
            
            # Add custom headers
            if connection.extra:
                import json
                extra = json.loads(connection.extra)
                if 'headers' in extra:
                    self._session.headers.update(extra['headers'])
        
        return self._session
    
    def make_request(self, endpoint: str, method: str = 'GET', **kwargs) -> Dict[str, Any]:
        """Make API request"""
        session = self.get_conn()
        url = f"{self._base_url}/{endpoint.lstrip('/')}"
        
        response = session.request(method, url, **kwargs)
        
        if response.status_code >= 400:
            raise AirflowException(f"API request failed: {response.status_code} - {response.text}")
        
        return response.json()
    
    def get_data(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get data from API endpoint"""
        return self.make_request(endpoint, method='GET', params=params)
    
    def post_data(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Post data to API endpoint"""
        return self.make_request(endpoint, method='POST', json=data)

# Custom Operator using the hook
class APIToS3Operator(BaseOperator):
    """Custom operator to extract data from API and load to S3"""
    
    template_fields = ['api_endpoint', 's3_key', 'api_params']
    
    @apply_defaults
    def __init__(
        self,
        api_endpoint: str,
        s3_bucket: str,
        s3_key: str,
        api_conn_id: str = 'api_default',
        aws_conn_id: str = 'aws_default',
        api_params: Optional[Dict] = None,
        data_format: str = 'json',
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.api_endpoint = api_endpoint
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.api_conn_id = api_conn_id
        self.aws_conn_id = aws_conn_id
        self.api_params = api_params or {}
        self.data_format = data_format
    
    def execute(self, context):
        """Execute the operator"""
        # Initialize hooks
        api_hook = CustomAPIHook(api_conn_id=self.api_conn_id)
        
        # Extract data from API
        self.log.info(f"Extracting data from {self.api_endpoint}")
        data = api_hook.get_data(self.api_endpoint, params=self.api_params)
        
        # Process data based on format
        if self.data_format == 'csv':
            # Convert to CSV
            df = pd.DataFrame(data)
            content = df.to_csv(index=False)
            content_type = 'text/csv'
        else:
            # Keep as JSON
            import json
            content = json.dumps(data, indent=2)
            content_type = 'application/json'
        
        # Upload to S3
        from airflow.providers.amazon.aws.hooks.s3 import S3Hook
        s3_hook = S3Hook(aws_conn_id=self.aws_conn_id)
        
        self.log.info(f"Uploading data to s3://{self.s3_bucket}/{self.s3_key}")
        s3_hook.load_string(
            string_data=content,
            key=self.s3_key,
            bucket_name=self.s3_bucket,
            content_type=content_type
        )
        
        # Return metadata
        return {
            'records_extracted': len(data) if isinstance(data, list) else 1,
            's3_location': f"s3://{self.s3_bucket}/{self.s3_key}",
            'data_format': self.data_format
        }

# Advanced custom operator with multiple data sources
class MultiSourceDataOperator(BaseOperator):
    """Operator that can handle multiple data sources"""
    
    template_fields = ['sources', 'output_path']
    
    @apply_defaults
    def __init__(
        self,
        sources: Dict[str, Dict],
        output_path: str,
        merge_strategy: str = 'concat',
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.sources = sources
        self.output_path = output_path
        self.merge_strategy = merge_strategy
    
    def execute(self, context):
        """Execute multi-source data extraction"""
        dataframes = {}
        
        for source_name, source_config in self.sources.items():
            self.log.info(f"Processing source: {source_name}")
            
            source_type = source_config['type']
            
            if source_type == 'api':
                # Use custom API hook
                api_hook = CustomAPIHook(source_config.get('conn_id', 'api_default'))
                data = api_hook.get_data(source_config['endpoint'])
                df = pd.DataFrame(data)
                
            elif source_type == 'postgres':
                # Use PostgreSQL hook
                from airflow.providers.postgres.hooks.postgres import PostgresHook
                pg_hook = PostgresHook(source_config.get('conn_id', 'postgres_default'))
                df = pg_hook.get_pandas_df(source_config['sql'])
                
            elif source_type == 's3':
                # Use S3 hook
                from airflow.providers.amazon.aws.hooks.s3 import S3Hook
                s3_hook = S3Hook(source_config.get('conn_id', 'aws_default'))
                
                # Download and read file
                file_content = s3_hook.read_key(
                    key=source_config['key'],
                    bucket_name=source_config['bucket']
                )
                
                if source_config.get('format') == 'csv':
                    from io import StringIO
                    df = pd.read_csv(StringIO(file_content))
                else:
                    import json
                    data = json.loads(file_content)
                    df = pd.DataFrame(data)
            
            else:
                raise AirflowException(f"Unsupported source type: {source_type}")
            
            # Add source identifier
            df['source'] = source_name
            dataframes[source_name] = df
            
            self.log.info(f"Loaded {len(df)} records from {source_name}")
        
        # Merge dataframes based on strategy
        if self.merge_strategy == 'concat':
            merged_df = pd.concat(dataframes.values(), ignore_index=True)
        elif self.merge_strategy == 'join':
            # Assume first source is base, join others
            source_names = list(dataframes.keys())
            merged_df = dataframes[source_names[0]]
            
            for source_name in source_names[1:]:
                join_key = self.sources[source_name].get('join_key', 'id')
                merged_df = merged_df.merge(
                    dataframes[source_name],
                    on=join_key,
                    how='left',
                    suffixes=('', f'_{source_name}')
                )
        
        # Save merged data
        merged_df.to_csv(self.output_path, index=False)
        
        self.log.info(f"Merged data saved to {self.output_path}")
        
        return {
            'total_records': len(merged_df),
            'sources_processed': len(dataframes),
            'output_path': self.output_path
        }

# Usage example in DAG
from datetime import datetime
from airflow import DAG

dag = DAG(
    'custom_operators_example',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False
)

# Use custom API to S3 operator
api_to_s3_task = APIToS3Operator(
    task_id='extract_api_to_s3',
    api_endpoint='posts',
    s3_bucket='my-data-bucket',
    s3_key='raw_data/posts_{{ ds }}.json',
    api_params={'userId': 1},
    dag=dag
)

# Use multi-source operator
multi_source_task = MultiSourceDataOperator(
    task_id='merge_multiple_sources',
    sources={
        'api_data': {
            'type': 'api',
            'endpoint': 'users',
            'conn_id': 'jsonplaceholder_api'
        },
        'db_data': {
            'type': 'postgres',
            'sql': 'SELECT * FROM user_metrics WHERE date = {{ ds }}',
            'conn_id': 'postgres_default'
        },
        's3_data': {
            'type': 's3',
            'bucket': 'my-data-bucket',
            'key': 'external_data/user_segments_{{ ds }}.csv',
            'format': 'csv'
        }
    },
    output_path='/tmp/merged_user_data_{{ ds }}.csv',
    merge_strategy='join',
    dag=dag
)

# Set dependencies
api_to_s3_task >> multi_source_task
```

## Scheduling and Dependencies

### Q8: How do you implement complex scheduling patterns and handle time zones in Airflow?

**Answer:**
Airflow supports complex scheduling through cron expressions, timedelta objects, and custom timetables. Time zone handling requires careful consideration of execution_date vs actual time.

**Code Example:**
```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.timetables.interval import CronDataIntervalTimetable
from airflow.utils.dates import days_ago
import pendulum

# Complex scheduling examples

# 1. Business hours only (9 AM - 5 PM, weekdays)
business_hours_dag = DAG(
    'business_hours_processing',
    start_date=datetime(2023, 1, 1, tzinfo=pendulum.timezone('America/New_York')),
    schedule_interval='0 9-17 * * 1-5',  # Every hour from 9-17, Mon-Fri
    catchup=False,
    max_active_runs=1
)

# 2. Custom timetable for complex business logic
class BusinessDayTimetable(CronDataIntervalTimetable):
    """Custom timetable that skips holidays"""
    
    def __init__(self):
        super().__init__('0 2 * * 1-5', pendulum.timezone('UTC'))
        # Define holidays (simplified)
        self.holidays = [
            datetime(2023, 1, 1),  # New Year
            datetime(2023, 7, 4),  # Independence Day
            datetime(2023, 12, 25) # Christmas
        ]
    
    def next_dagrun_info(self, last_automated_data_interval, restriction):
        """Calculate next DAG run, skipping holidays"""
        next_info = super().next_dagrun_info(last_automated_data_interval, restriction)
        
        if next_info and next_info.run_after.date() in [h.date() for h in self.holidays]:
            # Skip to next business day
            next_date = next_info.run_after + timedelta(days=1)
            while next_date.weekday() >= 5 or next_date.date() in [h.date() for h in self.holidays]:
                next_date += timedelta(days=1)
            
            return next_info._replace(run_after=next_date)
        
        return next_info

# DAG with custom timetable
custom_schedule_dag = DAG(
    'custom_business_schedule',
    start_date=datetime(2023, 1, 1),
    timetable=BusinessDayTimetable(),
    catchup=False
)

# 3. Time zone aware processing
def process_timezone_data(**context):
    """Process data with timezone awareness"""
    execution_date = context['execution_date']
    
    # Convert to different timezones
    utc_time = execution_date
    ny_time = utc_time.in_timezone('America/New_York')
    tokyo_time = utc_time.in_timezone('Asia/Tokyo')
    
    print(f"UTC: {utc_time}")
    print(f"New York: {ny_time}")
    print(f"Tokyo: {tokyo_time}")
    
    # Process data based on business timezone
    if ny_time.hour >= 9 and ny_time.hour <= 17:
        print("Processing during NY business hours")
        return "business_hours_processing"
    else:
        print("Processing during off hours")
        return "off_hours_processing"

# 4. Conditional scheduling based on external factors
def check_data_availability(**context):
    """Check if data is available for processing"""
    import os
    from datetime import datetime
    
    execution_date = context['execution_date']
    expected_file = f"/data/input/data_{execution_date.strftime('%Y%m%d')}.csv"
    
    if os.path.exists(expected_file):
        file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(expected_file))
        if file_age.total_seconds() < 3600:  # File less than 1 hour old
            return "process_data"
    
    return "skip_processing"

# Branch operator for conditional execution
from airflow.operators.python import BranchPythonOperator
from airflow.operators.dummy import DummyOperator

conditional_dag = DAG(
    'conditional_processing',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@hourly',
    catchup=False
)

check_data = BranchPythonOperator(
    task_id='check_data_availability',
    python_callable=check_data_availability,
    dag=conditional_dag
)

process_data = PythonOperator(
    task_id='process_data',
    python_callable=lambda: print("Processing data..."),
    dag=conditional_dag
)

skip_processing = DummyOperator(
    task_id='skip_processing',
    dag=conditional_dag
)

check_data >> [process_data, skip_processing]
```

### Q9: How do you handle cross-DAG dependencies and communication?

**Answer:**
Cross-DAG dependencies can be managed through sensors, external task sensors, and XCom. Proper design prevents tight coupling while enabling workflow coordination.

**Code Example:**
```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sensors.filesystem import FileSensor
from airflow.models import Variable

# Producer DAG - generates data
producer_dag = DAG(
    'data_producer',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False
)

def extract_and_prepare_data(**context):
    """Extract data and prepare for downstream processing"""
    import json
    
    # Simulate data extraction
    data_summary = {
        'records_extracted': 10000,
        'extraction_time': context['execution_date'].isoformat(),
        'data_quality_score': 0.95,
        'output_path': f"/data/extracted/data_{context['ds']}.json"
    }
    
    # Store metadata in XCom for cross-DAG communication
    context['ti'].xcom_push(key='data_summary', value=data_summary)
    
    # Also store in Airflow Variable for global access
    Variable.set(f"data_summary_{context['ds']}", json.dumps(data_summary))
    
    print(f"Data extracted: {data_summary}")
    return data_summary

producer_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_and_prepare_data,
    dag=producer_dag
)

# Consumer DAG - processes data from producer
consumer_dag = DAG(
    'data_consumer',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False
)

# Wait for producer DAG to complete
wait_for_producer = ExternalTaskSensor(
    task_id='wait_for_data_extraction',
    external_dag_id='data_producer',
    external_task_id='extract_data',
    execution_delta=timedelta(hours=0),  # Same execution date
    timeout=3600,  # 1 hour timeout
    poke_interval=60,  # Check every minute
    dag=consumer_dag
)

def process_extracted_data(**context):
    """Process data from producer DAG"""
    import json
    
    # Get data summary from producer
    data_summary_json = Variable.get(f"data_summary_{context['ds']}")
    data_summary = json.loads(data_summary_json)
    
    print(f"Processing data: {data_summary}")
    
    # Validate data quality
    if data_summary['data_quality_score'] < 0.9:
        raise ValueError(f"Data quality too low: {data_summary['data_quality_score']}")
    
    # Process the data
    processed_records = data_summary['records_extracted'] * 0.8  # Simulate processing
    
    result = {
        'processed_records': processed_records,
        'processing_time': context['execution_date'].isoformat(),
        'source_summary': data_summary
    }
    
    return result

process_task = PythonOperator(
    task_id='process_data',
    python_callable=process_extracted_data,
    dag=consumer_dag
)

wait_for_producer >> process_task

# Orchestrator DAG - coordinates multiple DAGs
orchestrator_dag = DAG(
    'workflow_orchestrator',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False
)

# Trigger multiple DAGs in sequence
trigger_producer = TriggerDagRunOperator(
    task_id='trigger_data_producer',
    trigger_dag_id='data_producer',
    wait_for_completion=True,
    poke_interval=60,
    dag=orchestrator_dag
)

trigger_consumer = TriggerDagRunOperator(
    task_id='trigger_data_consumer',
    trigger_dag_id='data_consumer',
    wait_for_completion=True,
    poke_interval=60,
    dag=orchestrator_dag
)

# Parallel processing DAGs
trigger_analytics = TriggerDagRunOperator(
    task_id='trigger_analytics',
    trigger_dag_id='analytics_pipeline',
    wait_for_completion=False,  # Don't wait, run in parallel
    dag=orchestrator_dag
)

trigger_reporting = TriggerDagRunOperator(
    task_id='trigger_reporting',
    trigger_dag_id='reporting_pipeline',
    wait_for_completion=False,
    dag=orchestrator_dag
)

# Set dependencies
trigger_producer >> trigger_consumer
trigger_consumer >> [trigger_analytics, trigger_reporting]

# Advanced cross-DAG communication using custom XCom backend
class CrossDAGXComManager:
    """Utility class for cross-DAG XCom communication"""
    
    @staticmethod
    def push_cross_dag_data(dag_id, task_id, execution_date, key, value):
        """Push data that can be accessed by other DAGs"""
        from airflow.models import XCom
        
        XCom.set(
            key=f"cross_dag_{key}",
            value=value,
            dag_id=dag_id,
            task_id=task_id,
            execution_date=execution_date
        )
    
    @staticmethod
    def pull_cross_dag_data(source_dag_id, source_task_id, execution_date, key):
        """Pull data from another DAG"""
        from airflow.models import XCom
        
        return XCom.get_one(
            key=f"cross_dag_{key}",
            dag_id=source_dag_id,
            task_id=source_task_id,
            execution_date=execution_date
        )

# Usage in tasks
def advanced_cross_dag_communication(**context):
    """Example of advanced cross-DAG communication"""
    xcom_manager = CrossDAGXComManager()
    
    # Push data for other DAGs
    xcom_manager.push_cross_dag_data(
        dag_id=context['dag'].dag_id,
        task_id=context['task'].task_id,
        execution_date=context['execution_date'],
        key='processing_metadata',
        value={
            'status': 'completed',
            'records_processed': 5000,
            'processing_duration': 120
        }
    )
    
    # Pull data from another DAG
    try:
        upstream_data = xcom_manager.pull_cross_dag_data(
            source_dag_id='data_producer',
            source_task_id='extract_data',
            execution_date=context['execution_date'],
            key='data_summary'
        )
        print(f"Received upstream data: {upstream_data}")
    except Exception as e:
        print(f"Could not retrieve upstream data: {e}")
```

## Monitoring and Troubleshooting

### Q10: How do you implement comprehensive monitoring and alerting in Airflow?

**Answer:**
Airflow monitoring involves tracking DAG performance, task failures, resource usage, and SLA violations. Integration with external monitoring systems provides comprehensive observability.

**Code Example:**
```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.models import Variable
from airflow.utils.email import send_email
from airflow.hooks.base import BaseHook
import logging
import json

# Custom monitoring functions
def monitor_dag_performance(**context):
    """Monitor DAG performance metrics"""
    from airflow.models import DagRun, TaskInstance
    from sqlalchemy import func
    
    dag_id = context['dag'].dag_id
    execution_date = context['execution_date']
    
    # Get DAG run statistics
    session = context['session']
    
    # Recent DAG runs performance
    recent_runs = session.query(DagRun).filter(
        DagRun.dag_id == dag_id,
        DagRun.execution_date >= execution_date - timedelta(days=7)
    ).all()
    
    performance_metrics = {
        'dag_id': dag_id,
        'execution_date': execution_date.isoformat(),
        'recent_runs_count': len(recent_runs),
        'success_rate': len([r for r in recent_runs if r.state == 'success']) / len(recent_runs) if recent_runs else 0,
        'avg_duration': sum([(r.end_date - r.start_date).total_seconds() for r in recent_runs if r.end_date]) / len(recent_runs) if recent_runs else 0
    }
    
    # Task-level metrics
    task_stats = session.query(
        TaskInstance.task_id,
        func.avg(TaskInstance.duration).label('avg_duration'),
        func.count(TaskInstance.task_id).label('run_count'),
        func.sum(func.case([(TaskInstance.state == 'success', 1)], else_=0)).label('success_count')
    ).filter(
        TaskInstance.dag_id == dag_id,
        TaskInstance.execution_date >= execution_date - timedelta(days=7)
    ).group_by(TaskInstance.task_id).all()
    
    performance_metrics['task_metrics'] = [
        {
            'task_id': stat.task_id,
            'avg_duration': stat.avg_duration,
            'success_rate': stat.success_count / stat.run_count if stat.run_count > 0 else 0
        }
        for stat in task_stats
    ]
    
    # Store metrics for alerting
    Variable.set(f"performance_metrics_{dag_id}", json.dumps(performance_metrics))
    
    return performance_metrics

def check_sla_violations(**context):
    """Check for SLA violations and alert"""
    from airflow.models import SlaMiss
    
    # Check recent SLA misses
    session = context['session']
    recent_sla_misses = session.query(SlaMiss).filter(
        SlaMiss.timestamp >= datetime.now() - timedelta(hours=24)
    ).all()
    
    if recent_sla_misses:
        sla_report = {
            'total_violations': len(recent_sla_misses),
            'violations': [
                {
                    'dag_id': miss.dag_id,
                    'task_id': miss.task_id,
                    'execution_date': miss.execution_date.isoformat(),
                    'timestamp': miss.timestamp.isoformat()
                }
                for miss in recent_sla_misses
            ]
        }
        
        # Send alert
        send_sla_alert(sla_report)
        return sla_report
    
    return {'total_violations': 0}

def send_sla_alert(sla_report):
    """Send SLA violation alert"""
    subject = f"Airflow SLA Violations - {sla_report['total_violations']} violations"
    
    html_content = f"""
    <h2>SLA Violations Report</h2>
    <p>Total violations in last 24 hours: {sla_report['total_violations']}</p>
    
    <table border="1">
        <tr><th>DAG ID</th><th>Task ID</th><th>Execution Date</th><th>Violation Time</th></tr>
    """
    
    for violation in sla_report['violations']:
        html_content += f"""
        <tr>
            <td>{violation['dag_id']}</td>
            <td>{violation['task_id']}</td>
            <td>{violation['execution_date']}</td>
            <td>{violation['timestamp']}</td>
        </tr>
        """
    
    html_content += "</table>"
    
    send_email(
        to=['data-team@company.com'],
        subject=subject,
        html_content=html_content
    )

# Resource monitoring
def monitor_resource_usage(**context):
    """Monitor Airflow resource usage"""
    import psutil
    from airflow.models import TaskInstance
    
    # System resources
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Airflow-specific metrics
    session = context['session']
    
    # Running tasks count
    running_tasks = session.query(TaskInstance).filter(
        TaskInstance.state == 'running'
    ).count()
    
    # Queued tasks count
    queued_tasks = session.query(TaskInstance).filter(
        TaskInstance.state == 'queued'
    ).count()
    
    resource_metrics = {
        'timestamp': datetime.now().isoformat(),
        'cpu_percent': cpu_percent,
        'memory_percent': memory.percent,
        'memory_available_gb': memory.available / (1024**3),
        'disk_percent': disk.percent,
        'disk_free_gb': disk.free / (1024**3),
        'running_tasks': running_tasks,
        'queued_tasks': queued_tasks
    }
    
    # Alert if resources are high
    if cpu_percent > 80 or memory.percent > 85 or disk.percent > 90:
        send_resource_alert(resource_metrics)
    
    return resource_metrics

def send_resource_alert(metrics):
    """Send resource usage alert"""
    subject = "Airflow High Resource Usage Alert"
    
    html_content = f"""
    <h2>High Resource Usage Detected</h2>
    <ul>
        <li>CPU Usage: {metrics['cpu_percent']:.1f}%</li>
        <li>Memory Usage: {metrics['memory_percent']:.1f}%</li>
        <li>Disk Usage: {metrics['disk_percent']:.1f}%</li>
        <li>Running Tasks: {metrics['running_tasks']}</li>
        <li>Queued Tasks: {metrics['queued_tasks']}</li>
    </ul>
    
    <p>Please check the Airflow cluster and consider scaling if necessary.</p>
    """
    
    send_email(
        to=['ops-team@company.com'],
        subject=subject,
        html_content=html_content
    )

# Integration with external monitoring systems
def send_metrics_to_datadog(**context):
    """Send Airflow metrics to Datadog"""
    try:
        from datadog import initialize, statsd
        
        # Initialize Datadog
        options = {
            'api_key': Variable.get('datadog_api_key'),
            'app_key': Variable.get('datadog_app_key')
        }
        initialize(**options)
        
        # Get performance metrics
        dag_id = context['dag'].dag_id
        metrics_json = Variable.get(f"performance_metrics_{dag_id}")
        metrics = json.loads(metrics_json)
        
        # Send metrics to Datadog
        statsd.gauge('airflow.dag.success_rate', metrics['success_rate'], tags=[f'dag_id:{dag_id}'])
        statsd.gauge('airflow.dag.avg_duration', metrics['avg_duration'], tags=[f'dag_id:{dag_id}'])
        
        for task_metric in metrics['task_metrics']:
            task_id = task_metric['task_id']
            statsd.gauge('airflow.task.avg_duration', task_metric['avg_duration'], 
                        tags=[f'dag_id:{dag_id}', f'task_id:{task_id}'])
            statsd.gauge('airflow.task.success_rate', task_metric['success_rate'], 
                        tags=[f'dag_id:{dag_id}', f'task_id:{task_id}'])
        
        print("Metrics sent to Datadog successfully")
        
    except Exception as e:
        print(f"Failed to send metrics to Datadog: {e}")

# Monitoring DAG
monitoring_dag = DAG(
    'airflow_monitoring',
    start_date=datetime(2023, 1, 1),
    schedule_interval='*/15 * * * *',  # Every 15 minutes
    catchup=False,
    max_active_runs=1
)

# Monitoring tasks
performance_monitor = PythonOperator(
    task_id='monitor_performance',
    python_callable=monitor_dag_performance,
    dag=monitoring_dag
)

sla_monitor = PythonOperator(
    task_id='check_sla_violations',
    python_callable=check_sla_violations,
    dag=monitoring_dag
)

resource_monitor = PythonOperator(
    task_id='monitor_resources',
    python_callable=monitor_resource_usage,
    dag=monitoring_dag
)

datadog_metrics = PythonOperator(
    task_id='send_datadog_metrics',
    python_callable=send_metrics_to_datadog,
    dag=monitoring_dag
)

# Set up monitoring pipeline
[performance_monitor, sla_monitor, resource_monitor] >> datadog_metrics

# Custom failure callback
def task_failure_alert(context):
    """Custom callback for task failures"""
    task_instance = context['task_instance']
    dag_id = task_instance.dag_id
    task_id = task_instance.task_id
    execution_date = context['execution_date']
    
    subject = f"Airflow Task Failure: {dag_id}.{task_id}"
    
    html_content = f"""
    <h2>Task Failure Alert</h2>
    <ul>
        <li>DAG: {dag_id}</li>
        <li>Task: {task_id}</li>
        <li>Execution Date: {execution_date}</li>
        <li>Log URL: {task_instance.log_url}</li>
    </ul>
    
    <p>Please check the logs and take appropriate action.</p>
    """
    
    send_email(
        to=['data-team@company.com'],
        subject=subject,
        html_content=html_content
    )

# Apply failure callback to DAG
monitoring_dag.default_args['on_failure_callback'] = task_failure_alert
```

---

## Key Takeaways

1. **Workflow Orchestration**: Airflow manages complex data pipeline dependencies and scheduling
2. **DAG Design**: Proper task granularity and dependency management for maintainable workflows
3. **Executor Selection**: Choose appropriate executor based on scalability and infrastructure needs
4. **Dynamic Tasks**: Generate tasks at runtime for flexible, data-driven workflows
5. **Custom Operators**: Extend functionality for specific business requirements and integrations
6. **Error Handling**: Implement proper retry strategies and failure notifications
7. **Monitoring**: Use Airflow UI and logging for pipeline observability
8. **Best Practices**: Idempotent tasks, proper resource allocation, and code organization
9. **Complex Scheduling**: Advanced scheduling patterns with timezone awareness
10. **Cross-DAG Dependencies**: Coordinate workflows across multiple DAGs
11. **Comprehensive Monitoring**: Track performance, SLAs, and resource usage
12. **External Integration**: Connect with monitoring systems like Datadog