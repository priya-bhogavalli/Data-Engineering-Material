# 🌪️ Apache Airflow - Comprehensive Interview Questions & Answers

## 📋 Table of Contents
1. [Fundamentals (Questions 1-15)](#fundamentals)
2. [DAGs & Tasks (Questions 16-30)](#dags--tasks)
3. [Operators & Hooks (Questions 31-45)](#operators--hooks)
4. [Scheduling & Execution (Questions 46-60)](#scheduling--execution)
5. [Advanced Topics (Questions 61-75)](#advanced-topics)

---

## 🔰 Fundamentals

### 1. What is Apache Airflow and what problems does it solve?

### 🎯 **Theoretical Foundation**

#### **Core Concepts**
- **Workflow Orchestration**: Programmatic scheduling and monitoring of data workflows
- **Directed Acyclic Graph (DAG)**: Mathematical model ensuring no circular dependencies
- **Task Dependency Management**: Complex dependency resolution using topological sorting
- **Distributed Execution**: Horizontal scaling through pluggable executors
- **Idempotency**: Tasks designed to produce same result regardless of execution count

#### **Historical Context**
- **2014**: Created at Airbnb by Maxime Beauchemin to solve data pipeline challenges
- **2016**: Open-sourced and donated to Apache Software Foundation
- **2019**: Became Apache top-level project
- **2020**: Airflow 2.0 with major architectural improvements
- **2021**: TaskFlow API and improved UI introduction
- **2023**: Airflow 2.6+ with enhanced security and performance

#### **Architectural Principles**
- **Configuration as Code**: Workflows defined in Python for version control
- **Extensibility**: Plugin architecture for custom operators and hooks
- **Scalability**: Multi-node deployment with various executors
- **Observability**: Comprehensive logging, monitoring, and alerting
- **Fault Tolerance**: Automatic retry mechanisms and failure handling

### 📈 **Comparative Analysis**

#### **Workflow Orchestration Platform Comparison Matrix**
| Feature | Apache Airflow | Prefect | Dagster | Luigi |
|---------|----------------|---------|---------|-------|
| **Architecture** | Scheduler-based | Hybrid cloud | Data-aware | Batch-focused |
| **UI/Monitoring** | Rich web UI | Modern UI | GraphQL API | Basic UI |
| **Scalability** | High (multi-executor) | Cloud-native | Kubernetes | Limited |
| **Learning Curve** | Medium-High | Medium | High | Low |
| **Community** | Very Large | Growing | Growing | Moderate |
| **Enterprise Features** | Extensive | Commercial | Commercial | Limited |
| **Data Lineage** | Basic | Advanced | Native | None |
| **Testing** | Manual setup | Built-in | Native | Basic |
| **Deployment** | Complex | Managed/Self | Flexible | Simple |
| **Cost** | Open source | Freemium | Commercial | Open source |

#### **Performance Benchmarks**
```
Airflow Performance Characteristics:
┌─────────────────┬──────────────┬──────────────┬──────────────┐
| Deployment      | DAGs/Cluster | Tasks/Hour   | Resource Usage|
├─────────────────┼──────────────┼──────────────┼──────────────┤
| Single Node     | 100-500      | 10K-50K      | 2-8GB RAM     |
| Multi-Node      | 1000-5000    | 100K-500K    | 16-64GB RAM   |
| Kubernetes      | 5000+        | 1M+          | Auto-scaling  |
| Cloud Managed   | 10000+       | 5M+          | Fully managed |
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

#### **Use Case Decision Matrix**
```
Airflow Use Case Selection Guide:
┌────────────────────┬────────────────┬────────────────┐
| Use Case            | Airflow Fit        | Alternative       |
├────────────────────┼────────────────┼────────────────┤
| ETL/ELT Pipelines   | ✓ Excellent       | Prefect, Dagster  |
| Data Orchestration  | ✓ Perfect         | Luigi, Argo       |
| ML Pipeline Mgmt    | ✓ Great           | Kubeflow, MLflow  |
| Batch Processing    | ✓ Excellent       | Cron, Jenkins     |
| Complex Dependencies| ✓ Perfect         | Custom solutions  |
| Multi-system Coord  | ✓ Great           | Zapier, n8n       |
| Real-time Streaming | ✗ Limited         | Kafka, Flink      |
| Simple Scheduling   | ✗ Overkill        | Cron, systemd     |
└────────────────────┴────────────────┴────────────────┘
```

**Answer:** Apache Airflow is an open-source workflow orchestration platform that solves:
- **Complex dependencies**: Manages task dependencies in data pipelines
- **Scheduling**: Automated execution of workflows
- **Monitoring**: Visual tracking of pipeline execution
- **Retry logic**: Automatic failure handling and retries
- **Scalability**: Distributed task execution

### 2. Explain Airflow's core components

### 🎯 **Theoretical Foundation**

#### **Core Concepts**
- **Component Separation**: Microservices architecture with distinct responsibilities
- **Stateful Coordination**: Metadata database as single source of truth
- **Pluggable Execution**: Executor abstraction for different deployment models
- **Event-Driven Scheduling**: Reactive scheduling based on task state changes
- **Horizontal Scalability**: Components can be scaled independently

#### **Component Architecture**
```
Airflow Component Interaction Flow:
┌────────────────────┬────────────────┬────────────────┐
| Component           | Primary Role       | Resource Usage   |
├────────────────────┼────────────────┼────────────────┤
| Web Server          | UI & API           | 1-2GB RAM        |
| Scheduler           | Task orchestration | 2-4GB RAM        |
| Executor            | Task distribution  | Varies by type   |
| Metadata Database   | State persistence  | 4-16GB RAM       |
| Workers             | Task execution     | 1-8GB per worker |
| Triggerer (2.2+)    | Async sensors      | 512MB-1GB RAM    |
└────────────────────┴────────────────┴────────────────┘
```

#### **Executor Comparison**
```
Executor Performance & Use Cases:
┌────────────────┬──────────────┬──────────────┬──────────────┐
| Executor Type       | Concurrency    | Scalability    | Use Case       |
├────────────────┼──────────────┼──────────────┼──────────────┤
| Sequential          | 1 task         | None           | Development    |
| Local               | Multi-process  | Single machine | Small teams    |
| Celery              | Distributed    | Multi-machine  | Production     |
| Kubernetes          | Pod-based      | Auto-scaling   | Cloud-native   |
| CeleryKubernetes    | Hybrid         | Best of both   | Enterprise     |
└────────────────┴──────────────┴──────────────┴──────────────┘
```

**Answer:**
- **Web Server**: UI for monitoring and managing workflows
- **Scheduler**: Triggers tasks based on dependencies and schedules
- **Executor**: Runs tasks (LocalExecutor, CeleryExecutor, KubernetesExecutor)
- **Metadata Database**: Stores DAG definitions, task states, connections
- **Workers**: Execute tasks in distributed setups

### 3. What is a DAG in Airflow?
**Answer:** DAG (Directed Acyclic Graph) represents a workflow:
- **Directed**: Tasks have clear upstream/downstream relationships
- **Acyclic**: No circular dependencies
- **Graph**: Collection of tasks with dependencies

```python
from airflow import DAG
from datetime import datetime

dag = DAG(
    'example_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False
)
```

### 4. What are Tasks and Task Instances?
**Answer:**
- **Task**: Unit of work defined in DAG (static definition)
- **Task Instance**: Specific execution of a task for a particular date
- **State**: Task instances have states (success, failed, running, etc.)

### 5. Explain Airflow's execution model
**Answer:**
1. **Scheduler** reads DAG files and creates DAG runs
2. **Task instances** created based on schedule and dependencies
3. **Executor** picks up tasks and assigns to workers
4. **Workers** execute tasks and report back status
5. **Metadata database** tracks all states and logs

### 6. What are the different Airflow executors?
**Answer:**
- **SequentialExecutor**: Single-threaded, for development
- **LocalExecutor**: Multi-process on single machine
- **CeleryExecutor**: Distributed execution using Celery
- **KubernetesExecutor**: Dynamic pod creation in Kubernetes
- **CeleryKubernetesExecutor**: Hybrid approach

### 7. How does Airflow handle task dependencies?
**Answer:**
```python
# Method 1: Using >> operator
task1 >> task2 >> task3

# Method 2: Using set_upstream/set_downstream
task2.set_upstream(task1)
task3.set_downstream(task2)

# Method 3: Using depends_on_past
task = BashOperator(
    task_id='example',
    depends_on_past=True,
    dag=dag
)
```

### 8. What is XCom in Airflow?
**Answer:** XCom (Cross-Communication) enables task communication:
```python
# Push data
def push_function(**context):
    context['task_instance'].xcom_push(key='my_key', value='my_value')

# Pull data
def pull_function(**context):
    value = context['task_instance'].xcom_pull(key='my_key', task_ids='push_task')
```

### 9. Explain Airflow's connection management
**Answer:**
- **Connections**: Store credentials and connection details
- **Hooks**: Interface to external systems using connections
- **Security**: Encrypted storage of sensitive information
- **UI Management**: Create/edit connections via web interface

### 10. What are Airflow Variables?
**Answer:**
```python
from airflow.models import Variable

# Set variable
Variable.set("my_var", "my_value")

# Get variable
my_value = Variable.get("my_var")

# Use in templates
bash_command='echo {{ var.value.my_var }}'
```

### 11. How does Airflow handle timezones?
**Answer:**
- **UTC default**: All times stored in UTC
- **Timezone aware**: Support for timezone-aware scheduling
- **Configuration**: Set timezone in airflow.cfg
- **DAG timezone**: Can specify timezone per DAG

### 12. What is the Airflow metadata database?
**Answer:**
- **Purpose**: Stores DAG definitions, task states, connections, variables
- **Supported DBs**: PostgreSQL, MySQL, SQLite (dev only)
- **Schema**: Well-defined schema for all Airflow objects
- **Migrations**: Automatic schema migrations during upgrades

### 13. Explain Airflow's logging mechanism
**Answer:**
- **Task logs**: Individual logs per task instance
- **Remote logging**: Store logs in S3, GCS, Azure Blob
- **Log levels**: Configurable logging levels
- **Structured logging**: JSON format support

### 14. What are Airflow pools?
**Answer:**
```python
# Limit concurrent tasks
task = BashOperator(
    task_id='limited_task',
    pool='my_pool',  # Pool with limited slots
    dag=dag
)
```
- **Resource management**: Limit concurrent task execution
- **Slot allocation**: Tasks consume pool slots
- **Priority**: Tasks can have priority within pools

### 15. How does Airflow handle backfilling?
**Answer:**
```bash
# Backfill command
airflow dags backfill -s 2023-01-01 -e 2023-01-31 my_dag
```
- **Historical runs**: Execute DAG for past dates
- **Catchup**: Automatic backfilling when enabled
- **Performance**: Parallel execution of historical runs

---

## 📊 DAGs & Tasks

### 16. How do you create a basic DAG?
**Answer:**
```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'my_data_pipeline',
    default_args=default_args,
    description='Data processing pipeline',
    schedule_interval='@daily',
    catchup=False,
    tags=['data', 'etl']
)

extract_task = BashOperator(
    task_id='extract_data',
    bash_command='python /scripts/extract.py',
    dag=dag
)
```

### 17. What are DAG default_args?
**Answer:**
```python
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email': ['admin@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'queue': 'bash_queue',
    'pool': 'backfill',
    'priority_weight': 10,
    'end_date': datetime(2023, 12, 31),
    'wait_for_downstream': False,
    'sla': timedelta(hours=2),
    'execution_timeout': timedelta(seconds=300),
    'on_failure_callback': some_function,
    'on_success_callback': some_other_function,
    'on_retry_callback': another_function,
    'sla_miss_callback': sla_callback_function,
    'trigger_rule': 'all_success'
}
```

### 18. How do you implement conditional logic in DAGs?
**Answer:**
```python
from airflow.operators.python import BranchPythonOperator

def choose_branch(**context):
    if context['ds'] == '2023-01-01':
        return 'special_task'
    else:
        return 'normal_task'

branch_task = BranchPythonOperator(
    task_id='branch_decision',
    python_callable=choose_branch,
    dag=dag
)

special_task = BashOperator(
    task_id='special_task',
    bash_command='echo "Special processing"',
    dag=dag
)

normal_task = BashOperator(
    task_id='normal_task',
    bash_command='echo "Normal processing"',
    dag=dag
)

branch_task >> [special_task, normal_task]
```

### 19. What are trigger rules in Airflow?
**Answer:**
- **all_success**: All upstream tasks succeeded (default)
- **all_failed**: All upstream tasks failed
- **all_done**: All upstream tasks completed (success or failed)
- **one_failed**: At least one upstream task failed
- **one_success**: At least one upstream task succeeded
- **none_failed**: No upstream tasks failed
- **none_skipped**: No upstream tasks skipped
- **dummy**: No dependencies

### 20. How do you handle task failures and retries?
**Answer:**
```python
task = BashOperator(
    task_id='retry_task',
    bash_command='exit 1',  # Will fail
    retries=3,
    retry_delay=timedelta(minutes=5),
    retry_exponential_backoff=True,
    max_retry_delay=timedelta(hours=1),
    dag=dag
)
```

### 21. What are SubDAGs and TaskGroups?
**Answer:**
```python
# TaskGroup (recommended)
from airflow.utils.task_group import TaskGroup

with TaskGroup("processing_group", dag=dag) as tg1:
    task1 = BashOperator(task_id="task1", bash_command="echo 1")
    task2 = BashOperator(task_id="task2", bash_command="echo 2")
    task1 >> task2

# SubDAG (deprecated)
from airflow.operators.subdag import SubDagOperator

subdag_task = SubDagOperator(
    task_id='subdag_task',
    subdag=create_subdag('main_dag', 'subdag_task', default_args),
    dag=dag
)
```

### 22. How do you implement dynamic task generation?
**Answer:**
```python
def create_dynamic_tasks():
    tasks = []
    for i in range(5):
        task = BashOperator(
            task_id=f'dynamic_task_{i}',
            bash_command=f'echo "Processing batch {i}"',
            dag=dag
        )
        tasks.append(task)
    return tasks

dynamic_tasks = create_dynamic_tasks()

# Set dependencies
for i in range(len(dynamic_tasks) - 1):
    dynamic_tasks[i] >> dynamic_tasks[i + 1]
```

### 23. What are task sensors in Airflow?
**Answer:**
```python
from airflow.sensors.filesystem import FileSensor
from airflow.sensors.s3_key_sensor import S3KeySensor

# File sensor
file_sensor = FileSensor(
    task_id='wait_for_file',
    filepath='/data/input.csv',
    poke_interval=30,
    timeout=300,
    dag=dag
)

# S3 sensor
s3_sensor = S3KeySensor(
    task_id='wait_for_s3_file',
    bucket_key='data/{{ ds }}/input.csv',
    bucket_name='my-bucket',
    aws_conn_id='aws_default',
    dag=dag
)
```

### 24. How do you implement task parallelism?
**Answer:**
```python
# Parallel tasks
extract_task1 = BashOperator(task_id='extract1', bash_command='echo 1', dag=dag)
extract_task2 = BashOperator(task_id='extract2', bash_command='echo 2', dag=dag)
extract_task3 = BashOperator(task_id='extract3', bash_command='echo 3', dag=dag)

transform_task = BashOperator(task_id='transform', bash_command='echo transform', dag=dag)

# All extract tasks run in parallel, then transform
[extract_task1, extract_task2, extract_task3] >> transform_task
```

### 25. What is task context in Airflow?
**Answer:**
```python
def my_function(**context):
    # Access context variables
    ds = context['ds']  # Execution date
    dag_run = context['dag_run']
    task_instance = context['task_instance']
    params = context['params']
    
    print(f"Execution date: {ds}")
    return "Success"

python_task = PythonOperator(
    task_id='context_task',
    python_callable=my_function,
    dag=dag
)
```

### 26. How do you pass parameters to DAGs?
**Answer:**
```python
# DAG level parameters
dag = DAG(
    'parameterized_dag',
    params={'env': 'prod', 'batch_size': 1000},
    dag=dag
)

# Task level parameters
task = BashOperator(
    task_id='param_task',
    bash_command='echo {{ params.env }} {{ params.batch_size }}',
    params={'custom_param': 'value'},
    dag=dag
)

# Runtime parameters
airflow dags trigger my_dag --conf '{"key": "value"}'
```

### 27. What are DAG tags and how are they used?
**Answer:**
```python
dag = DAG(
    'tagged_dag',
    tags=['data-engineering', 'etl', 'production'],
    dag=dag
)
```
- **Organization**: Group related DAGs
- **Filtering**: Filter DAGs in UI by tags
- **Monitoring**: Track DAGs by category
- **Access control**: Role-based access by tags

### 28. How do you implement SLA monitoring?
**Answer:**
```python
def sla_miss_callback(dag, task_list, blocking_task_list, slas, blocking_tis):
    print(f"SLA missed for tasks: {task_list}")
    # Send alert, create ticket, etc.

dag = DAG(
    'sla_dag',
    sla_miss_callback=sla_miss_callback,
    dag=dag
)

task = BashOperator(
    task_id='sla_task',
    bash_command='sleep 10',
    sla=timedelta(seconds=5),  # Will trigger SLA miss
    dag=dag
)
```

### 29. What are DAG dependencies?
**Answer:**
```python
from airflow.sensors.external_task import ExternalTaskSensor

# Wait for another DAG's task
wait_for_dag = ExternalTaskSensor(
    task_id='wait_for_upstream_dag',
    external_dag_id='upstream_dag',
    external_task_id='final_task',
    dag=dag
)

# Cross-DAG dependencies
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

trigger_downstream = TriggerDagRunOperator(
    task_id='trigger_downstream_dag',
    trigger_dag_id='downstream_dag',
    dag=dag
)
```

### 30. How do you implement task cleanup and maintenance?
**Answer:**
```python
def cleanup_function(**context):
    # Cleanup temporary files
    import os
    temp_dir = f"/tmp/{context['dag_run'].run_id}"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

cleanup_task = PythonOperator(
    task_id='cleanup',
    python_callable=cleanup_function,
    trigger_rule='all_done',  # Run regardless of upstream success/failure
    dag=dag
)

# Set as final task
[task1, task2, task3] >> cleanup_task
```

---

## 🔧 Operators & Hooks

### 31. What are the main types of operators in Airflow?
**Answer:**
- **BashOperator**: Execute bash commands
- **PythonOperator**: Execute Python functions
- **SQLOperator**: Execute SQL queries
- **EmailOperator**: Send emails
- **HttpOperator**: Make HTTP requests
- **DockerOperator**: Run Docker containers
- **KubernetesPodOperator**: Run Kubernetes pods

### 32. How do you create custom operators?
**Answer:**
```python
from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

class CustomOperator(BaseOperator):
    @apply_defaults
    def __init__(self, my_param, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.my_param = my_param
    
    def execute(self, context):
        self.log.info(f"Executing with param: {self.my_param}")
        # Custom logic here
        return "Success"

# Usage
custom_task = CustomOperator(
    task_id='custom_task',
    my_param='test_value',
    dag=dag
)
```

### 33. What are hooks in Airflow?
**Answer:**
```python
from airflow.hooks.postgres_hook import PostgresHook

def query_database(**context):
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    
    # Execute query
    records = pg_hook.get_records("SELECT * FROM users LIMIT 10")
    
    # Insert data
    pg_hook.insert_rows(
        table='processed_data',
        rows=records,
        target_fields=['id', 'name', 'email']
    )

python_task = PythonOperator(
    task_id='db_task',
    python_callable=query_database,
    dag=dag
)
```

### 34. How do you use the DockerOperator?
**Answer:**
```python
from airflow.providers.docker.operators.docker import DockerOperator

docker_task = DockerOperator(
    task_id='docker_task',
    image='python:3.8',
    command='python -c "print(\'Hello from Docker\')"',
    docker_url='unix://var/run/docker.sock',
    network_mode='bridge',
    auto_remove=True,
    dag=dag
)
```

### 35. What is the KubernetesPodOperator?
**Answer:**
```python
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

k8s_task = KubernetesPodOperator(
    task_id='k8s_task',
    name='airflow-pod',
    namespace='default',
    image='python:3.8',
    cmds=['python'],
    arguments=['-c', 'print("Hello from Kubernetes")'],
    get_logs=True,
    dag=dag
)
```

### 36. How do you implement the EmailOperator?
**Answer:**
```python
from airflow.operators.email import EmailOperator

email_task = EmailOperator(
    task_id='send_email',
    to=['admin@company.com'],
    subject='DAG {{ dag.dag_id }} completed',
    html_content='''
    <h3>DAG Execution Summary</h3>
    <p>Execution Date: {{ ds }}</p>
    <p>Status: Success</p>
    ''',
    dag=dag
)
```

### 37. What are decorated operators (@task)?
**Answer:**
```python
from airflow.decorators import task

@task
def extract_data():
    # Extract logic
    return {'records': 100, 'status': 'success'}

@task
def transform_data(data):
    # Transform logic
    transformed = data['records'] * 2
    return {'transformed_records': transformed}

@task
def load_data(data):
    # Load logic
    print(f"Loading {data['transformed_records']} records")

# Usage
extracted = extract_data()
transformed = transform_data(extracted)
load_data(transformed)
```

### 38. How do you use the SQLOperator?
**Answer:**
```python
from airflow.providers.postgres.operators.postgres import PostgresOperator

sql_task = PostgresOperator(
    task_id='sql_task',
    postgres_conn_id='postgres_default',
    sql='''
    INSERT INTO summary_table
    SELECT 
        date_trunc('day', created_at) as date,
        count(*) as daily_count
    FROM transactions 
    WHERE created_at >= '{{ ds }}'
    GROUP BY date_trunc('day', created_at)
    ''',
    dag=dag
)
```

### 39. What is the HttpOperator?
**Answer:**
```python
from airflow.providers.http.operators.http import SimpleHttpOperator

http_task = SimpleHttpOperator(
    task_id='api_call',
    http_conn_id='api_default',
    endpoint='data/{{ ds }}',
    method='GET',
    headers={'Authorization': 'Bearer {{ var.value.api_token }}'},
    xcom_push=True,
    dag=dag
)
```

### 40. How do you create custom hooks?
**Answer:**
```python
from airflow.hooks.base import BaseHook
import requests

class CustomApiHook(BaseHook):
    def __init__(self, conn_id):
        self.conn_id = conn_id
        self.connection = self.get_connection(conn_id)
    
    def get_data(self, endpoint):
        url = f"{self.connection.host}/{endpoint}"
        headers = {'Authorization': f'Bearer {self.connection.password}'}
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def post_data(self, endpoint, data):
        url = f"{self.connection.host}/{endpoint}"
        headers = {'Authorization': f'Bearer {self.connection.password}'}
        
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
```

### 41. What are sensor operators?
**Answer:**
```python
from airflow.sensors.base import BaseSensorOperator

class CustomSensor(BaseSensorOperator):
    def __init__(self, condition_param, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.condition_param = condition_param
    
    def poke(self, context):
        # Check condition
        if self.check_condition():
            return True
        return False
    
    def check_condition(self):
        # Custom condition logic
        return True

sensor_task = CustomSensor(
    task_id='custom_sensor',
    condition_param='value',
    poke_interval=60,
    timeout=300,
    dag=dag
)
```

### 42. How do you use the BashOperator effectively?
**Answer:**
```python
bash_task = BashOperator(
    task_id='bash_task',
    bash_command='''
    set -e  # Exit on error
    
    # Environment setup
    export DATA_DATE={{ ds }}
    export OUTPUT_DIR=/data/processed/{{ ds }}
    
    # Create directory
    mkdir -p $OUTPUT_DIR
    
    # Process data
    python /scripts/process_data.py \
        --input-date $DATA_DATE \
        --output-dir $OUTPUT_DIR \
        --config {{ var.value.config_path }}
    
    # Validate output
    if [ ! -f "$OUTPUT_DIR/success.flag" ]; then
        echo "Processing failed - no success flag found"
        exit 1
    fi
    ''',
    dag=dag
)
```

### 43. What are operator relationships and dependencies?
**Answer:**
```python
# Linear dependency
task1 >> task2 >> task3

# Fan-out
task1 >> [task2, task3, task4]

# Fan-in
[task2, task3, task4] >> task5

# Complex dependencies
task1 >> task2
task1 >> task3
[task2, task3] >> task4
task4 >> task5

# Cross dependencies
task1.set_downstream([task2, task3])
task4.set_upstream([task2, task3])
```

### 44. How do you implement operator callbacks?
**Answer:**
```python
def success_callback(context):
    print(f"Task {context['task_instance'].task_id} succeeded")
    # Send success notification

def failure_callback(context):
    print(f"Task {context['task_instance'].task_id} failed")
    # Send failure alert

def retry_callback(context):
    print(f"Task {context['task_instance'].task_id} retrying")
    # Log retry attempt

task = BashOperator(
    task_id='callback_task',
    bash_command='echo "Hello"',
    on_success_callback=success_callback,
    on_failure_callback=failure_callback,
    on_retry_callback=retry_callback,
    dag=dag
)
```

### 45. What are provider packages in Airflow?
**Answer:**
Provider packages extend Airflow functionality:
```bash
# Install providers
pip install apache-airflow-providers-amazon
pip install apache-airflow-providers-google
pip install apache-airflow-providers-postgres

# Usage
from airflow.providers.amazon.aws.operators.s3 import S3CreateBucketOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
```

---

## ⏰ Scheduling & Execution

### 46. What are Airflow's scheduling options?
**Answer:**
```python
# Cron expressions
dag = DAG(schedule_interval='0 2 * * *')  # Daily at 2 AM

# Preset intervals
dag = DAG(schedule_interval='@daily')     # Daily at midnight
dag = DAG(schedule_interval='@hourly')    # Every hour
dag = DAG(schedule_interval='@weekly')    # Weekly on Sunday
dag = DAG(schedule_interval='@monthly')   # Monthly on 1st

# Timedelta
dag = DAG(schedule_interval=timedelta(hours=6))  # Every 6 hours

# No schedule
dag = DAG(schedule_interval=None)  # Manual trigger only
```

### 47. How does Airflow handle execution dates?
**Answer:**
- **Execution date**: Start of the data interval
- **Logical date**: Same as execution date (Airflow 2.2+)
- **Data interval**: Period of data being processed
- **Run date**: Actual execution time

```python
def print_dates(**context):
    print(f"Execution date: {context['ds']}")
    print(f"Next execution: {context['next_ds']}")
    print(f"Previous execution: {context['prev_ds']}")
```

### 48. What is catchup in Airflow?
**Answer:**
```python
dag = DAG(
    'catchup_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=True,  # Run all missed intervals
    max_active_runs=3  # Limit concurrent runs
)
```
- **catchup=True**: Backfill all missed runs
- **catchup=False**: Only run latest interval
- **max_active_runs**: Control concurrent executions

### 49. How do you implement custom scheduling logic?
**Answer:**
```python
from airflow.timetables.base import Timetable

class CustomTimetable(Timetable):
    def next_dagrun_info(self, last_automated_dagrun, restriction):
        # Custom scheduling logic
        if last_automated_dagrun is None:
            next_run = restriction.earliest
        else:
            # Business logic for next run
            next_run = last_automated_dagrun.data_interval_end + timedelta(days=1)
        
        return DagRunInfo.interval(next_run, next_run + timedelta(days=1))

dag = DAG(
    'custom_schedule_dag',
    timetable=CustomTimetable(),
    dag=dag
)
```

### 50. What are DAG runs and how are they managed?
**Answer:**
- **DAG run**: Single execution of a DAG for a specific date
- **Run ID**: Unique identifier for each run
- **State**: running, success, failed
- **Concurrency**: Control with max_active_runs

```bash
# Trigger manual run
airflow dags trigger my_dag

# List DAG runs
airflow dags list-runs -d my_dag

# Clear DAG run
airflow tasks clear my_dag -s 2023-01-01 -e 2023-01-01
```

### 51. How do you handle timezone-aware scheduling?
**Answer:**
```python
from pendulum import timezone

dag = DAG(
    'timezone_dag',
    start_date=datetime(2023, 1, 1, tzinfo=timezone('US/Eastern')),
    schedule_interval='0 9 * * *',  # 9 AM Eastern
    dag=dag
)
```

### 52. What are task priorities and pools?
**Answer:**
```python
# Create pool
from airflow.models import Pool

# Task with priority and pool
task = BashOperator(
    task_id='priority_task',
    bash_command='echo "High priority task"',
    pool='critical_pool',
    priority_weight=100,  # Higher number = higher priority
    dag=dag
)
```

### 53. How do you implement task timeouts?
**Answer:**
```python
task = BashOperator(
    task_id='timeout_task',
    bash_command='sleep 300',  # 5 minutes
    execution_timeout=timedelta(minutes=2),  # Timeout after 2 minutes
    dag=dag
)
```

### 54. What is task reschedule vs retry?
**Answer:**
- **Retry**: Re-execute failed task immediately (with delay)
- **Reschedule**: Sensor-specific, check condition again later

```python
# Retry configuration
task = BashOperator(
    task_id='retry_task',
    retries=3,
    retry_delay=timedelta(minutes=5),
    dag=dag
)

# Sensor reschedule
sensor = FileSensor(
    task_id='file_sensor',
    filepath='/data/file.txt',
    poke_interval=60,  # Check every minute
    mode='reschedule',  # Reschedule instead of blocking
    dag=dag
)
```

### 55. How do you handle DAG pausing and unpausing?
**Answer:**
```bash
# Pause DAG
airflow dags pause my_dag

# Unpause DAG
airflow dags unpause my_dag

# Check DAG state
airflow dags state my_dag 2023-01-01
```

### 56. What are task slots and parallelism?
**Answer:**
```python
# DAG level parallelism
dag = DAG(
    'parallel_dag',
    max_active_tasks=10,  # Max concurrent tasks
    max_active_runs=3,    # Max concurrent DAG runs
    dag=dag
)

# Global configuration in airflow.cfg
# parallelism = 32              # Max tasks across all DAGs
# dag_concurrency = 16          # Max tasks per DAG
# max_active_runs_per_dag = 16  # Max runs per DAG
```

### 57. How do you implement conditional scheduling?
**Answer:**
```python
def should_run(**context):
    # Business logic to determine if DAG should run
    execution_date = context['ds']
    if datetime.strptime(execution_date, '%Y-%m-%d').weekday() < 5:
        return True  # Run on weekdays only
    return False

conditional_task = ShortCircuitOperator(
    task_id='check_condition',
    python_callable=should_run,
    dag=dag
)

main_task = BashOperator(
    task_id='main_processing',
    bash_command='echo "Processing data"',
    dag=dag
)

conditional_task >> main_task
```

### 58. What are external triggers in Airflow?
**Answer:**
```python
# API trigger
curl -X POST \
  "http://localhost:8080/api/v1/dags/my_dag/dagRuns" \
  -H "Content-Type: application/json" \
  -d '{"conf": {"key": "value"}}'

# File-based trigger
from airflow.sensors.filesystem import FileSensor

trigger_sensor = FileSensor(
    task_id='wait_for_trigger_file',
    filepath='/triggers/run_dag.flag',
    dag=dag
)
```

### 59. How do you implement data-driven scheduling?
**Answer:**
```python
from airflow.sensors.sql import SqlSensor

# Wait for new data
data_sensor = SqlSensor(
    task_id='wait_for_new_data',
    conn_id='postgres_default',
    sql='''
    SELECT COUNT(*) 
    FROM raw_data 
    WHERE created_date = '{{ ds }}'
    AND processed = false
    ''',
    dag=dag
)

# Process when data available
process_task = BashOperator(
    task_id='process_new_data',
    bash_command='python /scripts/process.py {{ ds }}',
    dag=dag
)

data_sensor >> process_task
```

### 60. What are DAG serialization and parsing?
**Answer:**
- **Parsing**: Airflow reads Python files to create DAG objects
- **Serialization**: DAGs stored in database for scheduler
- **Performance**: Serialization improves scheduler performance
- **Validation**: Syntax errors caught during parsing

```python
# DAG parsing configuration
dag = DAG(
    'serialized_dag',
    is_paused_upon_creation=True,  # Start paused
    dag=dag
)
```

---

## 🚀 Advanced Topics

### 61. How do you implement Airflow security?
**Answer:**
```python
# RBAC configuration
from airflow.auth.managers.fab.security_manager import FabAirflowSecurityManager

# Custom security manager
class CustomSecurityManager(FabAirflowSecurityManager):
    def get_user_roles(self, user):
        # Custom role assignment logic
        return super().get_user_roles(user)

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'airflow.auth.backends.ldap_auth',
    'airflow.auth.backends.password_auth'
]
```

### 62. What are Airflow plugins?
**Answer:**
```python
from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint

# Custom view
custom_bp = Blueprint(
    "custom_view",
    __name__,
    template_folder='templates',
    static_folder='static'
)

class CustomPlugin(AirflowPlugin):
    name = "custom_plugin"
    operators = [CustomOperator]
    hooks = [CustomHook]
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = [custom_bp]
    menu_links = []
```

### 63. How do you implement custom executors?
**Answer:**
```python
from airflow.executors.base_executor import BaseExecutor

class CustomExecutor(BaseExecutor):
    def start(self):
        # Initialize executor
        pass
    
    def execute_async(self, key, command, queue=None, executor_config=None):
        # Submit task for execution
        pass
    
    def sync(self):
        # Check task status and update
        pass
    
    def end(self):
        # Cleanup executor
        pass
```

### 64. What are Airflow REST APIs?
**Answer:**
```python
import requests

# Get DAG information
response = requests.get(
    'http://localhost:8080/api/v1/dags/my_dag',
    auth=('admin', 'password')
)

# Trigger DAG run
response = requests.post(
    'http://localhost:8080/api/v1/dags/my_dag/dagRuns',
    json={'conf': {'param': 'value'}},
    auth=('admin', 'password')
)

# Get task instances
response = requests.get(
    'http://localhost:8080/api/v1/dags/my_dag/dagRuns/run_id/taskInstances',
    auth=('admin', 'password')
)
```

### 65. How do you implement Airflow monitoring?
**Answer:**
```python
# Custom metrics
from airflow.stats import Stats

def my_task(**context):
    # Increment counter
    Stats.incr('my_dag.task_executed')
    
    # Time operation
    with Stats.timer('my_dag.processing_time'):
        # Processing logic
        pass
    
    # Gauge metric
    Stats.gauge('my_dag.records_processed', 1000)

# Health check endpoint
from flask import Blueprint
health_bp = Blueprint('health', __name__)

@health_bp.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}
```

### 66. What are Airflow configuration best practices?
**Answer:**
```ini
# airflow.cfg optimizations
[core]
parallelism = 32
dag_concurrency = 16
max_active_runs_per_dag = 16
load_examples = False
dags_are_paused_at_creation = True

[scheduler]
dag_dir_list_interval = 300
catchup_by_default = False
max_threads = 2

[webserver]
expose_config = False
authenticate = True
rbac = True

[celery]
worker_concurrency = 16
task_soft_time_limit = 600
task_time_limit = 1200
```

### 67. How do you implement data lineage tracking?
**Answer:**
```python
from airflow.lineage import apply_lineage

@apply_lineage
def process_data(**context):
    # Processing logic with automatic lineage tracking
    input_data = read_from_source()
    processed_data = transform(input_data)
    write_to_destination(processed_data)

# Manual lineage
from airflow.lineage.entities import File

task = BashOperator(
    task_id='lineage_task',
    bash_command='process_data.py',
    inlets=[File('/input/data.csv')],
    outlets=[File('/output/processed.csv')],
    dag=dag
)
```

### 68. What are Airflow testing strategies?
**Answer:**
```python
import pytest
from airflow.models import DagBag

def test_dag_loaded():
    """Test that DAG is loaded without errors"""
    dag_bag = DagBag()
    dag = dag_bag.get_dag(dag_id='my_dag')
    assert dag is not None
    assert len(dag.tasks) > 0

def test_task_dependencies():
    """Test task dependencies are correct"""
    dag_bag = DagBag()
    dag = dag_bag.get_dag(dag_id='my_dag')
    
    extract_task = dag.get_task('extract')
    transform_task = dag.get_task('transform')
    
    assert extract_task in transform_task.upstream_list

def test_task_execution():
    """Test individual task execution"""
    from airflow.models import TaskInstance
    
    ti = TaskInstance(task=my_task, execution_date=datetime.now())
    result = my_task.execute(ti.get_template_context())
    assert result is not None
```

### 69. How do you implement Airflow disaster recovery?
**Answer:**
```python
# Backup strategy
import subprocess

def backup_metadata_db():
    """Backup Airflow metadata database"""
    subprocess.run([
        'pg_dump',
        '-h', 'localhost',
        '-U', 'airflow',
        '-d', 'airflow',
        '-f', f'/backups/airflow_backup_{datetime.now().strftime("%Y%m%d")}.sql'
    ])

# Multi-region setup
dag = DAG(
    'disaster_recovery_dag',
    default_args={
        'on_failure_callback': failover_callback,
        'retries': 3,
        'retry_delay': timedelta(minutes=5)
    },
    dag=dag
)
```

### 70. What are Airflow performance optimization techniques?
**Answer:**
```python
# DAG optimization
dag = DAG(
    'optimized_dag',
    max_active_tasks=20,           # Increase parallelism
    max_active_runs=1,             # Limit concurrent runs
    dagrun_timeout=timedelta(hours=2),  # Set timeout
    dag=dag
)

# Task optimization
task = PythonOperator(
    task_id='optimized_task',
    python_callable=my_function,
    pool='fast_pool',              # Use dedicated pool
    priority_weight=10,            # Set priority
    queue='high_memory',           # Use specific queue
    dag=dag
)

# Database optimization
# - Use connection pooling
# - Optimize SQL queries
# - Regular database maintenance
```

### 71. How do you implement custom authentication?
**Answer:**
```python
from airflow.auth.managers.base_auth_manager import BaseAuthManager

class CustomAuthManager(BaseAuthManager):
    def get_user(self, username):
        # Custom user lookup
        return User(username=username)
    
    def authenticate_user(self, username, password):
        # Custom authentication logic
        return self.validate_credentials(username, password)
    
    def is_authorized(self, user, resource, action):
        # Custom authorization logic
        return self.check_permissions(user, resource, action)

# Configuration
AUTH_MANAGER = 'path.to.CustomAuthManager'
```

### 72. What are Airflow deployment patterns?
**Answer:**
```yaml
# Docker Compose deployment
version: '3.8'
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: airflow
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
  
  redis:
    image: redis:6
  
  airflow-webserver:
    image: apache/airflow:2.5.0
    command: webserver
    environment:
      AIRFLOW__CORE__EXECUTOR: CeleryExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
      AIRFLOW__CELERY__RESULT_BACKEND: db+postgresql://airflow:airflow@postgres/airflow
      AIRFLOW__CELERY__BROKER_URL: redis://:@redis:6379/0
  
  airflow-scheduler:
    image: apache/airflow:2.5.0
    command: scheduler
  
  airflow-worker:
    image: apache/airflow:2.5.0
    command: celery worker
```

### 73. How do you implement Airflow scaling?
**Answer:**
```python
# Horizontal scaling with Celery
from airflow.executors.celery_executor import CeleryExecutor

# Configuration for scaling
CELERY_CONFIG = {
    'worker_concurrency': 16,
    'task_soft_time_limit': 600,
    'task_time_limit': 1200,
    'worker_prefetch_multiplier': 1,
    'task_acks_late': True,
}

# Auto-scaling with Kubernetes
from airflow.providers.cncf.kubernetes.executors.kubernetes_executor import KubernetesExecutor

k8s_task = KubernetesPodOperator(
    task_id='scalable_task',
    name='worker-pod',
    namespace='airflow',
    image='my-worker-image',
    resources={
        'request_memory': '1Gi',
        'request_cpu': '500m',
        'limit_memory': '2Gi',
        'limit_cpu': '1000m'
    },
    dag=dag
)
```

### 74. What are Airflow upgrade strategies?
**Answer:**
```bash
# Upgrade process
# 1. Backup metadata database
pg_dump airflow > airflow_backup.sql

# 2. Stop Airflow services
systemctl stop airflow-webserver
systemctl stop airflow-scheduler
systemctl stop airflow-worker

# 3. Upgrade Airflow
pip install --upgrade apache-airflow==2.5.0

# 4. Upgrade database schema
airflow db upgrade

# 5. Start services
systemctl start airflow-webserver
systemctl start airflow-scheduler
systemctl start airflow-worker

# 6. Verify upgrade
airflow version
```

### 75. How do you implement Airflow observability?
**Answer:**
```python
# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'airflow': {
            'format': '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'airflow',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'airflow',
            'filename': '/opt/airflow/logs/airflow.log',
            'maxBytes': 104857600,  # 100MB
            'backupCount': 5
        }
    },
    'loggers': {
        'airflow': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

# Metrics collection
from airflow.stats import Stats
from prometheus_client import Counter, Histogram

# Custom metrics
task_counter = Counter('airflow_tasks_total', 'Total tasks executed')
task_duration = Histogram('airflow_task_duration_seconds', 'Task execution time')

def instrumented_task(**context):
    task_counter.inc()
    with task_duration.time():
        # Task logic
        pass
```

---

## 🎯 **Quick Reference Commands**

```bash
# DAG operations
airflow dags list
airflow dags trigger my_dag
airflow dags pause my_dag
airflow dags unpause my_dag

# Task operations
airflow tasks list my_dag
airflow tasks run my_dag my_task 2023-01-01
airflow tasks clear my_dag -s 2023-01-01 -e 2023-01-01

# Database operations
airflow db init
airflow db upgrade
airflow db reset

# User management
airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com

# Configuration
airflow config list
airflow config get-value core sql_alchemy_conn
```

---

**Total Questions: 75** | **Difficulty: Beginner to Expert** | **Coverage: Complete Airflow Ecosystem**