# Apache Airflow Complete Guide for Data Engineering

## 🎯 What is Apache Airflow?

Apache Airflow is an **open-source workflow orchestration platform** that allows you to programmatically author, schedule, and monitor data pipelines. It's the de facto standard for orchestrating complex data engineering workflows.

### Key Characteristics
- **Programmatic**: Define workflows as code using Python
- **Scalable**: Distributed execution across multiple workers
- **Extensible**: Rich ecosystem of operators and hooks
- **Monitoring**: Web UI for pipeline visualization and monitoring
- **Flexible**: Support for complex dependencies and scheduling

## 💾 Core Concepts

### 1. DAGs (Directed Acyclic Graphs)
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default arguments for all tasks
default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

# Define the DAG
dag = DAG(
    'data_pipeline_example',
    default_args=default_args,
    description='Complete data pipeline example',
    schedule_interval='@daily',
    catchup=False,
    tags=['data-engineering', 'etl']
)

# Python function for data extraction
def extract_data(**context):
    """Extract data from source systems"""
    import pandas as pd
    import logging
    
    # Simulate data extraction
    data = {
        'user_id': range(1, 1001),
        'event_date': context['ds'],  # Execution date
        'event_type': ['login', 'purchase', 'logout'] * 334
    }
    
    df = pd.DataFrame(data)
    
    # Save to temporary location
    output_path = f"/tmp/extracted_data_{context['ds']}.csv"
    df.to_csv(output_path, index=False)
    
    logging.info(f"Extracted {len(df)} records to {output_path}")
    return output_path

# Define tasks
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag
)

transform_task = BashOperator(
    task_id='transform_data',
    bash_command='python /opt/airflow/scripts/transform.py {{ ds }}',
    dag=dag
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=lambda **context: print(f"Loading data for {context['ds']}"),
    dag=dag
)

# Set dependencies
extract_task >> transform_task >> load_task
```

### 2. Operators and Tasks
```python
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.operators.http import SimpleHttpOperator

# Database operations
create_table_task = PostgresOperator(
    task_id='create_staging_table',
    postgres_conn_id='postgres_default',
    sql="""
        CREATE TABLE IF NOT EXISTS staging.user_events (
            user_id INTEGER,
            event_date DATE,
            event_type VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """,
    dag=dag
)

# HTTP API calls
api_call_task = SimpleHttpOperator(
    task_id='call_external_api',
    http_conn_id='api_default',
    endpoint='data/users',
    method='GET',
    headers={'Authorization': 'Bearer {{ var.value.api_token }}'},
    xcom_push=True,
    dag=dag
)

# Email notifications
email_task = EmailOperator(
    task_id='send_completion_email',
    to=['data-team@company.com'],
    subject='Data Pipeline Completed - {{ ds }}',
    html_content="""
        <h3>Pipeline Status</h3>
        <p>The daily data pipeline has completed successfully.</p>
        <p>Execution Date: {{ ds }}</p>
        <p>Records Processed: {{ ti.xcom_pull(task_ids='extract_data') }}</p>
    """,
    dag=dag
)
```

### 3. Sensors and Triggers
```python
from airflow.sensors.filesystem import FileSensor
from airflow.sensors.sql import SqlSensor
from airflow.sensors.s3_key_sensor import S3KeySensor

# File sensor - wait for file to arrive
file_sensor = FileSensor(
    task_id='wait_for_input_file',
    filepath='/data/input/{{ ds }}/data.csv',
    fs_conn_id='fs_default',
    poke_interval=60,  # Check every 60 seconds
    timeout=3600,      # Timeout after 1 hour
    dag=dag
)

# SQL sensor - wait for data condition
sql_sensor = SqlSensor(
    task_id='wait_for_data_quality',
    conn_id='postgres_default',
    sql="""
        SELECT COUNT(*) FROM staging.user_events 
        WHERE event_date = '{{ ds }}' 
        AND quality_score > 0.8
    """,
    poke_interval=300,  # Check every 5 minutes
    dag=dag
)

# S3 sensor - wait for S3 object
s3_sensor = S3KeySensor(
    task_id='wait_for_s3_file',
    bucket_name='data-lake-bucket',
    bucket_key='raw-data/{{ ds }}/events.json',
    aws_conn_id='aws_default',
    timeout=1800,  # 30 minutes timeout
    dag=dag
)
```

## 🔧 Advanced Data Engineering Patterns

### 1. Dynamic DAG Generation
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import yaml

# Configuration for multiple data sources
DATA_SOURCES = [
    {'name': 'users', 'table': 'dim_users', 'schedule': '@daily'},
    {'name': 'orders', 'table': 'fact_orders', 'schedule': '@hourly'},
    {'name': 'products', 'table': 'dim_products', 'schedule': '@daily'}
]

def create_etl_dag(source_config):
    """Create ETL DAG for a specific data source"""
    
    dag_id = f"etl_{source_config['name']}"
    
    default_args = {
        'owner': 'data-engineering',
        'start_date': datetime(2024, 1, 1),
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
    }
    
    dag = DAG(
        dag_id,
        default_args=default_args,
        schedule_interval=source_config['schedule'],
        catchup=False,
        tags=['dynamic', 'etl', source_config['name']]
    )
    
    def extract_data(source_name, **context):
        """Generic extraction function"""
        print(f"Extracting data from {source_name}")
        # Implement source-specific extraction logic
        return f"extracted_{source_name}_{context['ds']}"
    
    def transform_data(source_name, **context):
        """Generic transformation function"""
        print(f"Transforming data for {source_name}")
        # Implement source-specific transformation logic
        return f"transformed_{source_name}_{context['ds']}"
    
    def load_data(table_name, **context):
        """Generic load function"""
        print(f"Loading data to {table_name}")
        # Implement loading logic
        return f"loaded_to_{table_name}"
    
    # Create tasks
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract_data,
        op_args=[source_config['name']],
        dag=dag
    )
    
    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform_data,
        op_args=[source_config['name']],
        dag=dag
    )
    
    load_task = PythonOperator(
        task_id='load',
        python_callable=load_data,
        op_args=[source_config['table']],
        dag=dag
    )
    
    # Set dependencies
    extract_task >> transform_task >> load_task
    
    return dag

# Generate DAGs for each data source
for source in DATA_SOURCES:
    globals()[f"etl_{source['name']}_dag"] = create_etl_dag(source)
```

### 2. Data Quality Framework
```python
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
import pandas as pd
import logging

def run_data_quality_checks(**context):
    """Run comprehensive data quality checks"""
    
    # Get data from previous task
    data_path = context['ti'].xcom_pull(task_ids='extract_data')
    df = pd.read_csv(data_path)
    
    quality_results = {
        'total_records': len(df),
        'null_checks': {},
        'duplicate_checks': {},
        'range_checks': {},
        'overall_score': 0
    }
    
    # Null value checks
    for column in df.columns:
        null_percentage = (df[column].isnull().sum() / len(df)) * 100
        quality_results['null_checks'][column] = {
            'null_percentage': null_percentage,
            'passed': null_percentage < 5  # Less than 5% nulls
        }
    
    # Duplicate checks
    duplicate_count = df.duplicated().sum()
    quality_results['duplicate_checks'] = {
        'duplicate_count': duplicate_count,
        'duplicate_percentage': (duplicate_count / len(df)) * 100,
        'passed': duplicate_count == 0
    }
    
    # Range checks (example for numeric columns)
    numeric_columns = df.select_dtypes(include=['number']).columns
    for column in numeric_columns:
        if column in df.columns:
            min_val, max_val = df[column].min(), df[column].max()
            quality_results['range_checks'][column] = {
                'min_value': min_val,
                'max_value': max_val,
                'passed': min_val >= 0  # Example: values should be non-negative
            }
    
    # Calculate overall quality score
    passed_checks = sum([
        sum([check['passed'] for check in quality_results['null_checks'].values()]),
        quality_results['duplicate_checks']['passed'],
        sum([check['passed'] for check in quality_results['range_checks'].values()])
    ])
    
    total_checks = (
        len(quality_results['null_checks']) + 
        1 + 
        len(quality_results['range_checks'])
    )
    
    quality_results['overall_score'] = (passed_checks / total_checks) * 100
    
    # Log results
    logging.info(f"Data Quality Results: {quality_results}")
    
    # Store results in XCom
    context['ti'].xcom_push(key='quality_results', value=quality_results)
    
    return quality_results['overall_score']

def decide_pipeline_path(**context):
    """Decide whether to continue or fail based on data quality"""
    
    quality_score = context['ti'].xcom_pull(task_ids='data_quality_check')
    
    if quality_score >= 80:  # 80% quality threshold
        return 'continue_pipeline'
    else:
        return 'data_quality_failed'

# Data quality tasks
quality_check_task = PythonOperator(
    task_id='data_quality_check',
    python_callable=run_data_quality_checks,
    dag=dag
)

quality_gate_task = BranchPythonOperator(
    task_id='quality_gate',
    python_callable=decide_pipeline_path,
    dag=dag
)

continue_task = DummyOperator(
    task_id='continue_pipeline',
    dag=dag
)

quality_failed_task = PythonOperator(
    task_id='data_quality_failed',
    python_callable=lambda: logging.error("Data quality check failed!"),
    dag=dag
)

# Set dependencies
extract_task >> quality_check_task >> quality_gate_task
quality_gate_task >> [continue_task, quality_failed_task]
continue_task >> transform_task
```

### 3. Error Handling and Monitoring
```python
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.models import Variable
import logging

def robust_data_processing(**context):
    """Data processing with comprehensive error handling"""
    
    try:
        # Main processing logic
        data_path = context['ti'].xcom_pull(task_ids='extract_data')
        
        # Simulate processing
        import time
        import random
        
        # Random failure for demonstration
        if random.random() < 0.1:  # 10% chance of failure
            raise Exception("Simulated processing error")
        
        time.sleep(2)  # Simulate processing time
        
        result = {
            'status': 'success',
            'records_processed': 1000,
            'processing_time': 2.0
        }
        
        logging.info(f"Processing completed: {result}")
        return result
        
    except Exception as e:
        # Log error details
        error_info = {
            'error_type': type(e).__name__,
            'error_message': str(e),
            'task_id': context['task'].task_id,
            'dag_id': context['dag'].dag_id,
            'execution_date': str(context['execution_date'])
        }
        
        logging.error(f"Processing failed: {error_info}")
        
        # Store error info for downstream tasks
        context['ti'].xcom_push(key='error_info', value=error_info)
        
        # Re-raise to trigger task failure
        raise

def send_failure_notification(**context):
    """Send detailed failure notification"""
    
    error_info = context['ti'].xcom_pull(key='error_info')
    
    # Send to monitoring system
    # send_to_slack(error_info)
    # send_to_pagerduty(error_info)
    
    logging.info(f"Failure notification sent: {error_info}")

# Task with error handling
processing_task = PythonOperator(
    task_id='robust_processing',
    python_callable=robust_data_processing,
    dag=dag
)

# Failure notification task
failure_notification_task = PythonOperator(
    task_id='failure_notification',
    python_callable=send_failure_notification,
    trigger_rule='one_failed',  # Run when upstream task fails
    dag=dag
)

# Set up failure handling
processing_task >> failure_notification_task
```

## ⚡ Performance and Scaling

### 1. Executor Configuration
```python
# airflow.cfg configuration for different executors

# Local Executor (single machine)
[core]
executor = LocalExecutor
sql_alchemy_conn = postgresql+psycopg2://airflow:password@localhost/airflow

# Celery Executor (distributed)
[core]
executor = CeleryExecutor

[celery]
broker_url = redis://localhost:6379/0
result_backend = db+postgresql://airflow:password@localhost/airflow
worker_concurrency = 16

# Kubernetes Executor (cloud-native)
[core]
executor = KubernetesExecutor

[kubernetes]
namespace = airflow
worker_container_repository = apache/airflow
worker_container_tag = 2.7.0
```

### 2. Task Optimization
```python
from airflow.operators.python import PythonOperator
from airflow.models import TaskInstance
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

def parallel_processing(**context):
    """Process data in parallel using multiple threads"""
    
    def process_chunk(chunk_data):
        # Process individual chunk
        import time
        time.sleep(1)  # Simulate processing
        return len(chunk_data)
    
    # Get data and split into chunks
    data = list(range(1000))  # Simulate large dataset
    chunk_size = 100
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    
    # Process chunks in parallel
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(process_chunk, chunks))
    
    total_processed = sum(results)
    logging.info(f"Processed {total_processed} records in parallel")
    
    return total_processed

# Optimized task configuration
parallel_task = PythonOperator(
    task_id='parallel_processing',
    python_callable=parallel_processing,
    pool='cpu_intensive_pool',  # Use resource pool
    dag=dag
)
```

## 🔒 Security and Best Practices

### 1. Connection and Variable Management
```python
from airflow.models import Connection, Variable
from airflow.hooks.base import BaseHook

# Using connections securely
def get_database_connection():
    """Get database connection securely"""
    
    # Connection stored in Airflow UI or environment
    conn = BaseHook.get_connection('postgres_prod')
    
    connection_string = f"postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}"
    
    return connection_string

# Using variables for configuration
def get_config_value(key, default_value=None):
    """Get configuration value from Airflow Variables"""
    
    try:
        return Variable.get(key)
    except KeyError:
        if default_value is not None:
            return default_value
        raise

# Example usage in task
def secure_data_processing(**context):
    """Data processing with secure configuration"""
    
    # Get configuration
    batch_size = int(get_config_value('batch_size', '1000'))
    api_endpoint = get_config_value('api_endpoint')
    
    # Get database connection
    db_conn = get_database_connection()
    
    # Process data securely
    logging.info(f"Processing with batch size: {batch_size}")
```

### 2. DAG Security Best Practices
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Secure DAG configuration
default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'max_active_runs': 1,  # Prevent concurrent runs
    'catchup': False       # Don't backfill automatically
}

dag = DAG(
    'secure_data_pipeline',
    default_args=default_args,
    description='Secure data pipeline with best practices',
    schedule_interval='@daily',
    tags=['production', 'secure'],
    doc_md="""
    # Secure Data Pipeline
    
    This DAG implements security best practices:
    - Uses Airflow Connections for credentials
    - Implements proper error handling
    - Includes data quality checks
    - Has monitoring and alerting
    """
)
```

## 🎯 Best Practices Summary

### 1. DAG Design Best Practices
- **Idempotent Tasks**: Design tasks to be safely re-runnable
- **Atomic Operations**: Keep tasks focused on single responsibilities
- **Proper Dependencies**: Use clear task dependencies and avoid complex branching
- **Resource Management**: Use pools and queues for resource allocation

### 2. Performance Best Practices
- **Right Executor**: Choose appropriate executor for your scale
- **Task Parallelization**: Use parallel processing within tasks when possible
- **Resource Pools**: Limit concurrent resource-intensive tasks
- **Monitoring**: Monitor DAG performance and optimize bottlenecks

### 3. Operational Best Practices
- **Error Handling**: Implement comprehensive error handling and notifications
- **Data Quality**: Include data quality checks in pipelines
- **Documentation**: Document DAGs and tasks thoroughly
- **Testing**: Test DAGs in development environments

### 4. Security Best Practices
- **Secure Connections**: Use Airflow Connections for credentials
- **Variable Management**: Store configuration in Airflow Variables
- **Access Control**: Implement proper RBAC for Airflow UI
- **Audit Logging**: Enable audit logging for compliance

This guide provides essential Airflow knowledge for data engineering. Focus on understanding DAG design patterns, task orchestration, and operational best practices for building robust data pipelines.