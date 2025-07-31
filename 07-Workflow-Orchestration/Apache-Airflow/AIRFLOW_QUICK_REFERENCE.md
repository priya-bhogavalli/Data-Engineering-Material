# Apache Airflow Quick Reference

## Core Concepts

### DAG (Directed Acyclic Graph)
```python
from airflow import DAG
from datetime import datetime, timedelta

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'my_dag',
    default_args=default_args,
    description='My first DAG',
    schedule_interval='@daily',
    catchup=False,
    max_active_runs=1
)
```

### Common Schedule Intervals
```python
# Cron expressions
'0 0 * * *'        # Daily at midnight
'0 */6 * * *'      # Every 6 hours
'0 0 * * 1'        # Weekly on Monday
'0 0 1 * *'        # Monthly on 1st

# Preset intervals
'@once'            # Run once
'@hourly'          # Every hour
'@daily'           # Every day at midnight
'@weekly'          # Every Sunday at midnight
'@monthly'         # First day of month at midnight
'@yearly'          # January 1st at midnight

# Timedelta
timedelta(hours=1)  # Every hour
timedelta(days=1)   # Every day
```

## Essential Operators

### PythonOperator
```python
from airflow.operators.python import PythonOperator

def my_function(**context):
    print(f"Execution date: {context['execution_date']}")
    return "Hello World"

python_task = PythonOperator(
    task_id='python_task',
    python_callable=my_function,
    dag=dag
)
```

### BashOperator
```python
from airflow.operators.bash import BashOperator

bash_task = BashOperator(
    task_id='bash_task',
    bash_command='echo "Hello from Bash"',
    dag=dag
)

# With templating
bash_task = BashOperator(
    task_id='templated_bash',
    bash_command='echo "Processing {{ ds }}"',
    dag=dag
)
```

### SQLOperator
```python
from airflow.providers.postgres.operators.postgres import PostgresOperator

sql_task = PostgresOperator(
    task_id='sql_task',
    postgres_conn_id='postgres_default',
    sql="""
        INSERT INTO processed_data 
        SELECT * FROM raw_data 
        WHERE date = '{{ ds }}';
    """,
    dag=dag
)
```

### EmailOperator
```python
from airflow.operators.email import EmailOperator

email_task = EmailOperator(
    task_id='send_email',
    to=['admin@company.com'],
    subject='DAG Completed',
    html_content='<p>DAG completed successfully</p>',
    dag=dag
)
```

## Task Dependencies

### Basic Dependencies
```python
# Sequential
task1 >> task2 >> task3

# Parallel
task1 >> [task2, task3] >> task4

# Mixed
[task1, task2] >> task3 >> [task4, task5]

# Alternative syntax
task1.set_downstream(task2)
task2.set_upstream(task1)
```

### Trigger Rules
```python
from airflow.utils.trigger_rule import TriggerRule

task = PythonOperator(
    task_id='conditional_task',
    python_callable=my_function,
    trigger_rule=TriggerRule.ONE_SUCCESS,  # Run if at least one upstream succeeds
    dag=dag
)

# Available trigger rules:
# ALL_SUCCESS (default) - All upstream tasks succeed
# ALL_FAILED - All upstream tasks fail
# ALL_DONE - All upstream tasks complete (success or fail)
# ONE_SUCCESS - At least one upstream task succeeds
# ONE_FAILED - At least one upstream task fails
# NONE_FAILED - No upstream tasks fail (success or skipped)
```

## XCom (Cross-Communication)

### Push and Pull Data
```python
def push_data(**context):
    # Push to XCom
    context['task_instance'].xcom_push(key='my_key', value='my_value')
    return 'return_value'  # Automatically pushed with key 'return_value'

def pull_data(**context):
    # Pull from XCom
    value = context['task_instance'].xcom_pull(task_ids='push_task', key='my_key')
    return_value = context['task_instance'].xcom_pull(task_ids='push_task')
    print(f"Pulled: {value}, Return: {return_value}")

push_task = PythonOperator(task_id='push_task', python_callable=push_data, dag=dag)
pull_task = PythonOperator(task_id='pull_task', python_callable=pull_data, dag=dag)

push_task >> pull_task
```

## Templating

### Jinja Templates
```python
# Available variables
'{{ ds }}'                    # Execution date (YYYY-MM-DD)
'{{ ds_nodash }}'            # Execution date (YYYYMMDD)
'{{ ts }}'                   # Timestamp (YYYY-MM-DDTHH:MM:SS+00:00)
'{{ execution_date }}'       # Execution date object
'{{ dag }}'                  # DAG object
'{{ task }}'                 # Task object
'{{ task_instance }}'        # Task instance object
'{{ run_id }}'               # DAG run ID
'{{ dag_run }}'              # DAG run object

# Date arithmetic
'{{ ds | ds_add(7) }}'       # Add 7 days
'{{ ds | ds_add(-1) }}'      # Subtract 1 day

# Custom macros
def custom_macro():
    return "custom_value"

dag.user_defined_macros = {
    'custom_macro': custom_macro
}

# Use in task
templated_task = BashOperator(
    task_id='templated',
    bash_command='echo "{{ custom_macro() }}"',
    dag=dag
)
```

## Sensors

### FileSensor
```python
from airflow.sensors.filesystem import FileSensor

file_sensor = FileSensor(
    task_id='wait_for_file',
    filepath='/path/to/file.txt',
    poke_interval=30,  # Check every 30 seconds
    timeout=300,       # Timeout after 5 minutes
    dag=dag
)
```

### S3KeySensor
```python
from airflow.providers.amazon.aws.sensors.s3_key import S3KeySensor

s3_sensor = S3KeySensor(
    task_id='wait_for_s3_file',
    bucket_name='my-bucket',
    bucket_key='data/{{ ds }}/file.csv',
    aws_conn_id='aws_default',
    poke_interval=60,
    dag=dag
)
```

### Custom Sensor
```python
from airflow.sensors.base import BaseSensorOperator

class CustomSensor(BaseSensorOperator):
    def poke(self, context):
        # Custom logic to check condition
        return check_condition()

custom_sensor = CustomSensor(
    task_id='custom_wait',
    poke_interval=30,
    dag=dag
)
```

## Hooks and Connections

### Using Hooks
```python
from airflow.hooks.postgres_hook import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

def database_operation(**context):
    # PostgreSQL Hook
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    records = pg_hook.get_records("SELECT * FROM users LIMIT 10")
    
    # S3 Hook
    s3_hook = S3Hook(aws_conn_id='aws_default')
    s3_hook.load_string(
        string_data="Hello World",
        key="data/hello.txt",
        bucket_name="my-bucket"
    )
    
    return len(records)
```

### Connection Management
```bash
# CLI commands
airflow connections add 'my_conn' \
    --conn-type 'postgres' \
    --conn-host 'localhost' \
    --conn-login 'user' \
    --conn-password 'password' \
    --conn-schema 'mydb'

airflow connections list
airflow connections delete my_conn
```

## Variables and Configuration

### Variables
```python
from airflow.models import Variable

# Set variable
Variable.set("my_var", "my_value")
Variable.set("config", {"key": "value"}, serialize_json=True)

# Get variable
value = Variable.get("my_var")
config = Variable.get("config", deserialize_json=True)
default_value = Variable.get("missing_var", default_var="default")

# Use in task
def task_with_variable(**context):
    batch_size = Variable.get("batch_size", default_var=1000)
    process_data(batch_size=int(batch_size))
```

### CLI Commands
```bash
# Variables
airflow variables set my_var "my_value"
airflow variables get my_var
airflow variables list
airflow variables delete my_var

# Import/Export
airflow variables export variables.json
airflow variables import variables.json
```

## Branching

### BranchPythonOperator
```python
from airflow.operators.python import BranchPythonOperator
from airflow.operators.dummy import DummyOperator

def choose_branch(**context):
    if context['execution_date'].weekday() < 5:  # Monday = 0, Sunday = 6
        return 'weekday_task'
    else:
        return 'weekend_task'

branch = BranchPythonOperator(
    task_id='branch_decision',
    python_callable=choose_branch,
    dag=dag
)

weekday_task = DummyOperator(task_id='weekday_task', dag=dag)
weekend_task = DummyOperator(task_id='weekend_task', dag=dag)

branch >> [weekday_task, weekend_task]
```

## Error Handling

### Retries and Callbacks
```python
def failure_callback(context):
    print(f"Task {context['task_instance'].task_id} failed!")

def retry_callback(context):
    print(f"Retrying task {context['task_instance'].task_id}")

task = PythonOperator(
    task_id='risky_task',
    python_callable=risky_function,
    retries=3,
    retry_delay=timedelta(minutes=5),
    retry_exponential_backoff=True,
    on_failure_callback=failure_callback,
    on_retry_callback=retry_callback,
    dag=dag
)
```

### SLA (Service Level Agreement)
```python
task = PythonOperator(
    task_id='sla_task',
    python_callable=my_function,
    sla=timedelta(minutes=30),  # Task should complete within 30 minutes
    dag=dag
)

# DAG-level SLA callback
def sla_miss_callback(dag, task_list, blocking_task_list, slas, blocking_tis):
    print(f"SLA missed for tasks: {[t.task_id for t in task_list]}")

dag.sla_miss_callback = sla_miss_callback
```

## Testing

### Unit Testing
```python
import unittest
from airflow.models import DagBag

class TestDAG(unittest.TestCase):
    def setUp(self):
        self.dagbag = DagBag()
    
    def test_dag_loaded(self):
        dag = self.dagbag.get_dag('my_dag')
        self.assertIsNotNone(dag)
        self.assertEqual(len(dag.tasks), 3)
    
    def test_task_dependencies(self):
        dag = self.dagbag.get_dag('my_dag')
        task1 = dag.get_task('task1')
        task2 = dag.get_task('task2')
        self.assertIn(task2, task1.downstream_list)
```

### Task Testing
```python
from airflow.models import TaskInstance
from airflow.utils.state import State

def test_task_execution():
    dag = dagbag.get_dag('my_dag')
    task = dag.get_task('my_task')
    ti = TaskInstance(task, execution_date=datetime(2024, 1, 1))
    
    # Run task
    ti.run(ignore_dependencies=True)
    
    # Check result
    assert ti.state == State.SUCCESS
```

## CLI Commands

### DAG Management
```bash
# List DAGs
airflow dags list

# Trigger DAG
airflow dags trigger my_dag

# Pause/Unpause DAG
airflow dags pause my_dag
airflow dags unpause my_dag

# Test DAG
airflow dags test my_dag 2024-01-01
```

### Task Management
```bash
# List tasks
airflow tasks list my_dag

# Test task
airflow tasks test my_dag my_task 2024-01-01

# Task state
airflow tasks state my_dag my_task 2024-01-01

# Clear task
airflow tasks clear my_dag --task-regex "my_task.*"
```

### Monitoring
```bash
# List DAG runs
airflow dags list-runs -d my_dag

# List task instances
airflow tasks list-instances -d my_dag

# Show logs
airflow tasks logs my_dag my_task 2024-01-01
```

## Configuration

### airflow.cfg Key Settings
```ini
[core]
dags_folder = /opt/airflow/dags
base_log_folder = /opt/airflow/logs
executor = LocalExecutor
sql_alchemy_conn = postgresql://user:pass@localhost/airflow
parallelism = 32
dag_concurrency = 16
max_active_runs_per_dag = 16

[webserver]
web_server_port = 8080
base_url = http://localhost:8080

[scheduler]
dag_dir_list_interval = 300
catchup_by_default = False
max_threads = 2

[email]
email_backend = airflow.utils.email.send_email_smtp
```

### Environment Variables
```bash
export AIRFLOW_HOME=/opt/airflow
export AIRFLOW__CORE__EXECUTOR=LocalExecutor
export AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql://user:pass@localhost/airflow
export AIRFLOW__WEBSERVER__SECRET_KEY=your-secret-key
```

## Common Patterns

### ETL Pipeline
```python
def create_etl_dag():
    dag = DAG('etl_pipeline', schedule_interval='@daily')
    
    extract = PythonOperator(task_id='extract', python_callable=extract_data, dag=dag)
    transform = PythonOperator(task_id='transform', python_callable=transform_data, dag=dag)
    load = PythonOperator(task_id='load', python_callable=load_data, dag=dag)
    validate = PythonOperator(task_id='validate', python_callable=validate_data, dag=dag)
    
    extract >> transform >> load >> validate
    return dag
```

### Dynamic Task Generation
```python
def create_dynamic_tasks():
    dag = DAG('dynamic_tasks', schedule_interval='@daily')
    
    tables = ['users', 'orders', 'products']
    
    for table in tables:
        task = PythonOperator(
            task_id=f'process_{table}',
            python_callable=process_table,
            op_args=[table],
            dag=dag
        )
    
    return dag
```

### Conditional Execution
```python
def conditional_dag():
    dag = DAG('conditional_execution', schedule_interval='@daily')
    
    check = BranchPythonOperator(
        task_id='check_condition',
        python_callable=lambda: 'process_data' if check_condition() else 'skip_processing',
        dag=dag
    )
    
    process = PythonOperator(task_id='process_data', python_callable=process_data, dag=dag)
    skip = DummyOperator(task_id='skip_processing', dag=dag)
    
    check >> [process, skip]
    return dag
```

This quick reference covers the most commonly used Airflow features and patterns for data engineering workflows.