# Apache Airflow Best Practices for Data Engineering

## DAG Design Principles

### DAG Structure
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'data_pipeline',
    default_args=default_args,
    description='Daily data processing pipeline',
    schedule_interval='@daily',
    catchup=False,
    max_active_runs=1
)
```

### Task Dependencies
```python
# Linear dependencies
extract_task >> transform_task >> load_task

# Parallel execution
extract_task >> [transform_task_1, transform_task_2] >> load_task

# Complex dependencies
with dag:
    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')
    
    extract_customers = PythonOperator(task_id='extract_customers')
    extract_orders = PythonOperator(task_id='extract_orders')
    
    transform = PythonOperator(task_id='transform')
    load = PythonOperator(task_id='load')
    
    start >> [extract_customers, extract_orders] >> transform >> load >> end
```

## Error Handling and Monitoring

### Retry Logic
```python
def reliable_task(**context):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Your task logic here
            return process_data()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff

task = PythonOperator(
    task_id='reliable_task',
    python_callable=reliable_task,
    retries=3,
    retry_delay=timedelta(minutes=5)
)
```

### Alerting and Notifications
```python
def task_fail_slack_alert(context):
    slack_msg = f"""
    Task Failed: {context.get('task_instance').task_id}
    DAG: {context.get('task_instance').dag_id}
    Execution Time: {context.get('execution_date')}
    Log Url: {context.get('task_instance').log_url}
    """
    send_slack_message(slack_msg)

dag = DAG(
    'monitored_pipeline',
    default_args={
        'on_failure_callback': task_fail_slack_alert
    }
)
```

## Resource Management

### Connection Management
```python
from airflow.hooks.postgres_hook import PostgresHook
from airflow.hooks.s3_hook import S3Hook

def extract_from_postgres(**context):
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    sql = "SELECT * FROM customers WHERE updated_date >= %s"
    df = pg_hook.get_pandas_df(sql, parameters=[context['ds']])
    return df

def upload_to_s3(**context):
    s3_hook = S3Hook(aws_conn_id='aws_default')
    s3_hook.load_file(
        filename='/tmp/data.csv',
        key=f"data/{context['ds']}/customers.csv",
        bucket_name='data-lake'
    )
```

### Memory Optimization
```python
# Use XCom for small data only
def small_data_task(**context):
    result = {"count": 1000, "status": "success"}
    return result  # This goes to XCom

# Use external storage for large data
def large_data_task(**context):
    df = process_large_dataset()
    file_path = f"/tmp/large_data_{context['ds']}.parquet"
    df.to_parquet(file_path)
    return file_path  # Return path, not data
```

## Testing and Development

### Unit Testing
```python
import pytest
from airflow.models import DagBag

def test_dag_loaded():
    dag_bag = DagBag()
    dag = dag_bag.get_dag(dag_id='data_pipeline')
    assert dag is not None
    assert len(dag.tasks) == 4

def test_task_dependencies():
    dag_bag = DagBag()
    dag = dag_bag.get_dag(dag_id='data_pipeline')
    
    extract_task = dag.get_task('extract')
    transform_task = dag.get_task('transform')
    
    assert transform_task in extract_task.downstream_list
```

### Environment Management
```python
import os
from airflow.models import Variable

# Environment-specific configuration
ENVIRONMENT = Variable.get("environment", default_var="dev")

if ENVIRONMENT == "prod":
    DATABASE_CONN = "postgres_prod"
    S3_BUCKET = "prod-data-lake"
else:
    DATABASE_CONN = "postgres_dev"
    S3_BUCKET = "dev-data-lake"
```