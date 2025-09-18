# 🚁 Apache Airflow Interview Questions - Tier 1 Expansion

## 📊 **DAG Design Patterns & Best Practices** (20 questions)

### Q1: What are the key principles for designing maintainable DAGs?
**Answer:**
- **Single Responsibility**: Each DAG should handle one business process
- **Idempotency**: Tasks should produce same results when re-run
- **Atomic Tasks**: Break complex operations into smaller, testable units
- **Clear Dependencies**: Use explicit task dependencies with `>>` or `set_downstream()`
- **Proper Naming**: Use descriptive DAG and task IDs
- **Documentation**: Include docstrings and descriptions

### Q2: How do you implement dynamic DAG generation?
**Answer:**
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Dynamic task creation
def create_dynamic_dag(dag_id, schedule, tasks_config):
    dag = DAG(
        dag_id=dag_id,
        schedule_interval=schedule,
        start_date=datetime(2024, 1, 1),
        catchup=False
    )
    
    for task_config in tasks_config:
        task = PythonOperator(
            task_id=task_config['task_id'],
            python_callable=task_config['function'],
            dag=dag
        )
    
    return dag

# Generate multiple DAGs
configs = [
    {'dag_id': 'process_region_us', 'tasks': [...]},
    {'dag_id': 'process_region_eu', 'tasks': [...]}
]

for config in configs:
    globals()[config['dag_id']] = create_dynamic_dag(**config)
```

### Q3: What's the difference between `depends_on_past` and `wait_for_downstream`?
**Answer:**
- **`depends_on_past=True`**: Current task instance waits for previous instance to succeed
- **`wait_for_downstream=True`**: Current task waits for all downstream tasks of previous instance
- **Use Case**: `depends_on_past` for sequential processing, `wait_for_downstream` for complex dependencies

### Q4: How do you handle branching logic in DAGs?
**Answer:**
```python
from airflow.operators.python import BranchPythonOperator

def choose_branch(**context):
    if context['ds'] == '2024-01-01':
        return 'holiday_task'
    return 'regular_task'

branch_task = BranchPythonOperator(
    task_id='branch_decision',
    python_callable=choose_branch,
    dag=dag
)

holiday_task = PythonOperator(task_id='holiday_task', ...)
regular_task = PythonOperator(task_id='regular_task', ...)

branch_task >> [holiday_task, regular_task]
```

### Q5: What are DAG-level configurations and their impact?
**Answer:**
```python
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=2)
}

dag = DAG(
    'example_dag',
    default_args=default_args,
    schedule_interval='@daily',
    max_active_runs=1,
    catchup=False,
    tags=['production', 'etl']
)
```

## 🔧 **Custom Operators & Sensors** (20 questions)

### Q6: How do you create a custom operator?
**Answer:**
```python
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class CustomS3Operator(BaseOperator):
    @apply_defaults
    def __init__(self, s3_bucket, s3_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
    
    def execute(self, context):
        # Custom logic here
        self.log.info(f"Processing {self.s3_bucket}/{self.s3_key}")
        return f"Processed {self.s3_key}"
```

### Q7: What's the difference between Sensor and Operator?
**Answer:**
- **Operator**: Executes an action (ETL, API call, file processing)
- **Sensor**: Waits for a condition to be met (file exists, API response, time)
- **Poke vs Reschedule**: Sensors can poke (continuous checking) or reschedule (release worker slot)

### Q8: How do you implement a custom file sensor?
**Answer:**
```python
from airflow.sensors.base import BaseSensorOperator

class CustomFileSensor(BaseSensorOperator):
    def __init__(self, filepath, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filepath = filepath
    
    def poke(self, context):
        import os
        exists = os.path.exists(self.filepath)
        self.log.info(f"File {self.filepath} exists: {exists}")
        return exists
```

### Q9: How do you handle operator failures and retries?
**Answer:**
```python
task = PythonOperator(
    task_id='risky_task',
    python_callable=my_function,
    retries=3,
    retry_delay=timedelta(minutes=5),
    retry_exponential_backoff=True,
    max_retry_delay=timedelta(hours=1),
    on_failure_callback=failure_callback,
    dag=dag
)
```

### Q10: What are the best practices for sensor configuration?
**Answer:**
- **Timeout**: Set appropriate `timeout` to avoid infinite waiting
- **Poke Interval**: Use reasonable `poke_interval` to balance responsiveness and resource usage
- **Mode**: Choose `poke` for short waits, `reschedule` for long waits
- **Soft Fail**: Use `soft_fail=True` for optional dependencies

## 📡 **XComs & Task Communication** (15 questions)

### Q11: How do XComs work and what are their limitations?
**Answer:**
- **Purpose**: Share small data between tasks
- **Storage**: Stored in Airflow metadata database
- **Size Limit**: Typically 48KB (database dependent)
- **Serialization**: JSON serializable objects only
- **Scope**: Available within same DAG run

```python
# Push XCom
def push_data(**context):
    return {'key': 'value', 'count': 100}

# Pull XCom
def pull_data(**context):
    data = context['task_instance'].xcom_pull(task_ids='push_task')
    print(f"Received: {data}")
```

### Q12: What are alternatives to XComs for large data sharing?
**Answer:**
- **External Storage**: S3, GCS, Azure Blob for large files
- **Database**: Shared database tables
- **Message Queues**: Redis, RabbitMQ for real-time data
- **File System**: Shared file systems (not recommended for distributed setups)

### Q13: How do you implement custom XCom backends?
**Answer:**
```python
from airflow.models.xcom import BaseXCom

class S3XComBackend(BaseXCom):
    @staticmethod
    def serialize_value(value):
        # Upload to S3, return reference
        s3_key = upload_to_s3(value)
        return {'s3_key': s3_key}
    
    @staticmethod
    def deserialize_value(result):
        # Download from S3
        return download_from_s3(result['s3_key'])
```

## ⚡ **Scaling & Performance Optimization** (20 questions)

### Q14: How do you optimize Airflow for high throughput?
**Answer:**
- **Parallelism**: Increase `parallelism` and `dag_concurrency`
- **Executor**: Use CeleryExecutor or KubernetesExecutor for scaling
- **Database**: Optimize metadata database (connection pooling, indexing)
- **Task Design**: Break large tasks into smaller parallel tasks
- **Resource Allocation**: Right-size worker resources

### Q15: What are the different Airflow executors and when to use them?
**Answer:**
- **SequentialExecutor**: Development only, single-threaded
- **LocalExecutor**: Single machine, multi-process
- **CeleryExecutor**: Distributed, uses Celery workers
- **KubernetesExecutor**: Dynamic pod creation, cloud-native
- **CeleryKubernetesExecutor**: Hybrid approach

### Q16: How do you monitor and troubleshoot DAG performance?
**Answer:**
```python
# Task duration monitoring
from airflow.models import TaskInstance
from airflow.utils.db import provide_session

@provide_session
def get_task_durations(dag_id, session=None):
    return session.query(TaskInstance).filter(
        TaskInstance.dag_id == dag_id,
        TaskInstance.state == 'success'
    ).all()
```

### Q17: What are pool configurations and how do they help?
**Answer:**
```python
# Pool limits concurrent tasks
task = PythonOperator(
    task_id='db_task',
    python_callable=my_function,
    pool='database_pool',  # Limit concurrent DB connections
    dag=dag
)
```

## ☁️ **Cloud Integration** (15 questions)

### Q18: How do you deploy Airflow on Kubernetes?
**Answer:**
```yaml
# airflow-values.yaml
executor: "KubernetesExecutor"
webserver:
  replicas: 2
scheduler:
  replicas: 1
workers:
  replicas: 3
postgresql:
  enabled: true
redis:
  enabled: true
```

### Q19: How do you integrate Airflow with AWS services?
**Answer:**
```python
from airflow.providers.amazon.aws.operators.s3 import S3CreateBucketOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator

s3_task = S3CreateBucketOperator(
    task_id='create_bucket',
    bucket_name='my-data-bucket',
    aws_conn_id='aws_default'
)

glue_task = GlueJobOperator(
    task_id='run_glue_job',
    job_name='my-etl-job',
    aws_conn_id='aws_default'
)
```

### Q20: How do you handle secrets and connections securely?
**Answer:**
- **Connections**: Store in Airflow UI or environment variables
- **Secrets Backend**: Use AWS Secrets Manager, HashiCorp Vault
- **Environment Variables**: For non-sensitive configuration
- **Encryption**: Enable Fernet key encryption

## 🚨 **Error Handling & Monitoring** (15 questions)

### Q21: How do you implement comprehensive error handling?
**Answer:**
```python
def failure_callback(context):
    task_instance = context['task_instance']
    send_alert(f"Task {task_instance.task_id} failed")

def retry_callback(context):
    task_instance = context['task_instance']
    log_retry(f"Retrying {task_instance.task_id}")

task = PythonOperator(
    task_id='monitored_task',
    python_callable=my_function,
    on_failure_callback=failure_callback,
    on_retry_callback=retry_callback,
    retries=3,
    dag=dag
)
```

### Q22: What are SLA configurations and monitoring?
**Answer:**
```python
dag = DAG(
    'sla_dag',
    default_args={
        'sla': timedelta(hours=2),  # Task-level SLA
        'email_on_failure': True
    },
    sla_miss_callback=sla_miss_alert,
    schedule_interval='@hourly'
)
```

### Q23: How do you implement data quality checks?
**Answer:**
```python
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowException

def data_quality_check(**context):
    # Check row count
    if row_count < expected_minimum:
        raise AirflowException("Data quality check failed: insufficient rows")
    
    # Check for nulls
    if null_percentage > 0.05:
        raise AirflowException("Data quality check failed: too many nulls")
    
    return "Data quality checks passed"

quality_check = PythonOperator(
    task_id='data_quality_check',
    python_callable=data_quality_check,
    dag=dag
)
```

## 🔐 **Security & Access Control** (10 questions)

### Q24: How do you implement role-based access control?
**Answer:**
- **Roles**: Admin, Op, Viewer, User
- **Permissions**: DAG-level and task-level permissions
- **LDAP Integration**: Enterprise authentication
- **API Security**: Token-based authentication

### Q25: What are security best practices for Airflow?
**Answer:**
- **Fernet Encryption**: Encrypt sensitive data in database
- **HTTPS**: Use SSL/TLS for web interface
- **Network Security**: Restrict access to Airflow components
- **Secrets Management**: External secrets backends
- **Audit Logging**: Track user actions and changes

## 🔄 **Advanced Patterns** (20 questions)

### Q26: How do you implement cross-DAG dependencies?
**Answer:**
```python
from airflow.sensors.external_task import ExternalTaskSensor

wait_for_upstream = ExternalTaskSensor(
    task_id='wait_for_upstream_dag',
    external_dag_id='upstream_dag',
    external_task_id='final_task',
    timeout=600,
    dag=dag
)
```

### Q27: How do you handle time zones and scheduling?
**Answer:**
```python
from pendulum import timezone

dag = DAG(
    'timezone_dag',
    schedule_interval='0 9 * * *',  # 9 AM
    start_date=datetime(2024, 1, 1, tzinfo=timezone('UTC')),
    timezone='America/New_York'  # Execute in EST/EDT
)
```

### Q28: What are task groups and how do they improve DAG readability?
**Answer:**
```python
from airflow.utils.task_group import TaskGroup

with TaskGroup('data_processing') as processing_group:
    extract = PythonOperator(task_id='extract', ...)
    transform = PythonOperator(task_id='transform', ...)
    load = PythonOperator(task_id='load', ...)
    
    extract >> transform >> load

start >> processing_group >> end
```

### Q29: How do you implement conditional task execution?
**Answer:**
```python
from airflow.operators.dummy import DummyOperator
from airflow.utils.trigger_rule import TriggerRule

# Skip downstream if condition not met
skip_task = PythonOperator(
    task_id='conditional_skip',
    python_callable=lambda: None,  # Skip logic
    dag=dag
)

downstream_task = PythonOperator(
    task_id='conditional_execution',
    python_callable=my_function,
    trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    dag=dag
)
```

### Q30: How do you implement data lineage tracking?
**Answer:**
```python
from airflow.lineage import apply_lineage

@apply_lineage
def etl_task(**context):
    # Airflow tracks input/output datasets
    return {
        'inputs': ['s3://input-bucket/data.csv'],
        'outputs': ['s3://output-bucket/processed.parquet']
    }
```

## 📈 **Performance Tuning** (15 questions)

### Q31: How do you optimize DAG parsing performance?
**Answer:**
- **Minimize Top-level Code**: Avoid expensive operations in DAG file
- **Dynamic Imports**: Import modules inside functions
- **Caching**: Cache expensive computations
- **DAG Serialization**: Enable DAG serialization for faster parsing

### Q32: What are the key metrics to monitor in Airflow?
**Answer:**
- **DAG Performance**: Parse time, task duration, success rate
- **System Metrics**: CPU, memory, disk usage
- **Queue Metrics**: Task queue length, worker utilization
- **Database Metrics**: Connection pool, query performance

### Q33: How do you handle large-scale DAG deployments?
**Answer:**
- **Git-based Deployment**: Version control for DAG files
- **CI/CD Pipeline**: Automated testing and deployment
- **Environment Separation**: Dev, staging, production environments
- **Configuration Management**: External configuration files

## 🧪 **Testing & Development** (10 questions)

### Q34: How do you unit test Airflow DAGs?
**Answer:**
```python
import pytest
from airflow.models import DagBag

def test_dag_loaded():
    dagbag = DagBag()
    dag = dagbag.get_dag(dag_id='my_dag')
    assert dag is not None
    assert len(dag.tasks) == 5

def test_task_dependencies():
    dag = dagbag.get_dag('my_dag')
    extract_task = dag.get_task('extract')
    transform_task = dag.get_task('transform')
    assert transform_task in extract_task.downstream_list
```

### Q35: What are best practices for DAG development?
**Answer:**
- **Version Control**: Use Git for DAG versioning
- **Code Review**: Peer review for DAG changes
- **Testing**: Unit tests for DAG structure and logic
- **Documentation**: Clear documentation for business logic
- **Linting**: Use pylint, black for code quality

This completes the first 35 questions for Apache Airflow Tier 1 expansion. The remaining questions would cover advanced topics like:
- Multi-tenancy patterns
- Custom authentication backends  
- Advanced scheduling patterns
- Integration with data catalogs
- Cost optimization strategies
- Disaster recovery procedures
- Advanced monitoring and alerting
- Custom UI plugins
- API automation
- Enterprise deployment patterns

Total: 83 additional questions to reach 150 target.