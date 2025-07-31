# Apache Airflow Key Concepts

## 1. DAG (Directed Acyclic Graph)
**What it is**: The fundamental building block of Airflow - a collection of tasks with defined dependencies that represents a complete workflow.

**Key Properties**:
- **Directed**: Tasks have a specific execution order (A → B → C)
- **Acyclic**: No circular dependencies (prevents infinite loops)
- **Graph**: Visual representation viewable in Airflow UI

**Essential DAG Parameters**:
```python
from datetime import datetime, timedelta
from airflow import DAG

dag = DAG(
    dag_id='my_data_pipeline',           # Unique identifier (required)
    description='Daily ETL pipeline',     # Human-readable description
    start_date=datetime(2024, 1, 1),     # When DAG becomes schedulable
    schedule='@daily',                   # Execution frequency
    catchup=False,                       # Skip historical runs
    tags=['etl', 'production', 'daily'], # Organization and filtering
    max_active_runs=1,                   # Prevent overlapping runs
    max_active_tasks=10,                 # Limit concurrent tasks
    default_view='graph',                # Default UI view
    is_paused_upon_creation=True,        # Start paused for safety
    dagrun_timeout=timedelta(hours=4),   # Maximum runtime
    doc_md="""# Data Pipeline
    This DAG processes daily sales data..."""
)
```

**DAG Lifecycle States**:
- **Active**: Currently scheduled and running
- **Paused**: Temporarily disabled
- **Success**: Last run completed successfully
- **Failed**: Last run encountered errors

## 2. Tasks and Operators
**What they are**: Individual units of work within a DAG that perform specific actions.

**Core Operator Types**:

### PythonOperator
Executes Python functions with full context access.
```python
from airflow.operators.python import PythonOperator

def process_data(**context):
    execution_date = context['ds']
    print(f"Processing data for {execution_date}")
    return {"processed_records": 1000}

task = PythonOperator(
    task_id='process_data',
    python_callable=process_data,
    provide_context=True
)
```

### BashOperator
Runs shell commands and scripts.
```python
from airflow.operators.bash import BashOperator

task = BashOperator(
    task_id='run_script',
    bash_command='python /path/to/script.py {{ ds }}',
    env={'ENV_VAR': 'production'}
)
```

### EmailOperator
Sends email notifications.
```python
from airflow.operators.email import EmailOperator

task = EmailOperator(
    task_id='send_report',
    to=['team@company.com'],
    subject='Daily Report - {{ ds }}',
    html_content='<h1>Report completed successfully</h1>'
)
```

**Task Lifecycle States**:
1. **None**: Not yet scheduled
2. **Scheduled**: Ready to be picked up by executor
3. **Queued**: Waiting for available worker
4. **Running**: Currently executing
5. **Success**: Completed successfully
6. **Failed**: Encountered an error
7. **Skipped**: Intentionally bypassed
8. **Up for retry**: Failed but will retry
9. **Up for reschedule**: Sensor waiting to check again
10. **Upstream failed**: Dependency failed
11. **Deferred**: Waiting for external trigger

## 3. Task Dependencies
**What they are**: Rules that define the execution order and relationships between tasks.

**Dependency Operators**:
```python
# Basic dependencies
task_a >> task_b >> task_c  # Sequential: A → B → C
task_a << task_b            # Reverse: B → A

# Multiple dependencies
task_a >> [task_b, task_c]  # Fan-out: A → [B, C]
[task_a, task_b] >> task_c  # Fan-in: [A, B] → C

# Complex patterns
start >> extract_tasks >> transform_task >> [load_db, send_email] >> cleanup
```

**Advanced Dependency Patterns**:
```python
# Conditional dependencies with trigger rules
task_c = PythonOperator(
    task_id='task_c',
    python_callable=my_function,
    trigger_rule='one_success'  # Run if ANY upstream succeeds
)

# Cross-DAG dependencies
from airflow.sensors.external_task import ExternalTaskSensor

wait_for_upstream = ExternalTaskSensor(
    task_id='wait_for_data_prep',
    external_dag_id='data_preparation_dag',
    external_task_id='final_task',
    timeout=3600
)
```

## 4. XCom (Cross-Communication)
**What it is**: Airflow's built-in mechanism for passing small amounts of data between tasks.

**How XCom Works**:
1. **Push**: Task returns data → Automatically stored in XCom table
2. **Pull**: Downstream task retrieves data using task_id
3. **Storage**: Data serialized as JSON in metadata database

**XCom Usage Patterns**:
```python
# Automatic push (return value)
def extract_data():
    data = {"records": 1000, "status": "success"}
    return data  # Automatically pushed to XCom

# Manual push
def manual_push(**context):
    context['ti'].xcom_push(key='custom_key', value={'data': 'value'})

# Pull data in downstream task
def process_data(**context):
    # Pull from specific task
    data = context['ti'].xcom_pull(task_ids='extract_data')
    
    # Pull with custom key
    custom_data = context['ti'].xcom_pull(key='custom_key', task_ids='manual_push')
    
    # Pull from multiple tasks
    all_data = context['ti'].xcom_pull(task_ids=['task1', 'task2'])
    
    return {"processed": len(data)}
```

**XCom Limitations & Best Practices**:
- **Size limit**: Keep data small (< 48KB recommended)
- **Serialization**: Must be JSON serializable
- **Not for files**: Use external storage (S3, GCS) for large data
- **Security**: Avoid sensitive data in XCom

## 5. Context and Templating
**Context**: Runtime information automatically provided to tasks.

**Essential Context Variables**:
```python
def my_task(**context):
    # Date/Time information
    execution_date = context['ds']           # '2024-01-15'
    timestamp = context['ts']                # '2024-01-15T10:00:00+00:00'
    yesterday = context['yesterday_ds']      # '2024-01-14'
    
    # DAG/Task information
    dag_id = context['dag'].dag_id
    task_id = context['task'].task_id
    run_id = context['run_id']
    
    # Task instance for XCom
    ti = context['ti']
    data = ti.xcom_pull(task_ids='upstream_task')
    
    # User parameters
    params = context['params']
    
    # Configuration
    conf = context['dag_run'].conf or {}
```

**Jinja2 Templating**:
```python
# Template fields in operators
BashOperator(
    task_id='process_file',
    bash_command='''
        echo "Processing file for {{ ds }}"
        python process.py --date {{ ds }} --run-id {{ run_id }}
        mv /tmp/{{ ds }}_data.csv /archive/
    '''
)

# Custom templates
SqlOperator(
    task_id='update_table',
    sql='''
        UPDATE sales_data 
        SET processed_date = '{{ ts }}'
        WHERE date = '{{ ds }}'
        AND batch_id = '{{ params.batch_id }}'
    ''',
    params={'batch_id': 'daily_batch'}
)
```

## 6. Scheduling
**Schedule Types and Patterns**:

### Cron Expressions
```python
# Standard cron format: minute hour day month day_of_week
'0 2 * * *'        # Daily at 2 AM
'0 */6 * * *'      # Every 6 hours
'0 9 * * 1-5'      # Weekdays at 9 AM
'0 0 1 * *'        # First day of month
'0 8 * * MON'      # Every Monday at 8 AM
```

### Preset Schedules
```python
'@once'            # Run once
'@hourly'          # Every hour
'@daily'           # Every day at midnight
'@weekly'          # Every Sunday at midnight
'@monthly'         # First day of month at midnight
'@yearly'          # January 1st at midnight
```

### Timedelta Scheduling
```python
from datetime import timedelta

schedule=timedelta(hours=6)     # Every 6 hours
schedule=timedelta(minutes=30)  # Every 30 minutes
```

### Dataset-Driven Scheduling (Airflow 2.4+)
```python
from airflow.datasets import Dataset

# Define datasets
sales_data = Dataset("s3://bucket/sales/")
processed_data = Dataset("s3://bucket/processed/")

# Producer DAG
dag1 = DAG(
    'data_producer',
    schedule='@daily',
    outlets=[sales_data]  # This DAG produces sales_data
)

# Consumer DAG
dag2 = DAG(
    'data_consumer',
    schedule=[sales_data],  # Triggered when sales_data is updated
    outlets=[processed_data]
)
```

**Critical Scheduling Concepts**:
- **start_date**: When DAG becomes active (not first execution)
- **execution_date**: Logical date for data processing
- **data_interval**: Time period the run represents
- **catchup**: Whether to run missed historical intervals

## 7. Error Handling and Retries
**Comprehensive Error Handling**:

### Retry Configuration
```python
from datetime import timedelta

default_args = {
    'retries': 3,                              # Number of retry attempts
    'retry_delay': timedelta(minutes=5),       # Initial delay
    'retry_exponential_backoff': True,         # Increase delay each retry
    'max_retry_delay': timedelta(hours=1),     # Maximum delay cap
    'on_failure_callback': notify_failure,     # Custom failure handler
    'on_retry_callback': log_retry,            # Custom retry handler
    'on_success_callback': log_success         # Custom success handler
}
```

### Trigger Rules
Control when tasks execute based on upstream task states:
```python
# Default: all upstream tasks must succeed
trigger_rule='all_success'

# At least one upstream task succeeded
trigger_rule='one_success'

# All upstream tasks failed
trigger_rule='all_failed'

# No upstream tasks failed (success or skipped)
trigger_rule='none_failed'

# Always run regardless of upstream status
trigger_rule='always'

# No upstream tasks were skipped
trigger_rule='none_skipped'

# Combination: no failures AND at least one success
trigger_rule='none_failed_min_one_success'
```

### Custom Callbacks
```python
def failure_callback(context):
    """Called when task fails after all retries"""
    task_id = context['task_instance'].task_id
    dag_id = context['task_instance'].dag_id
    execution_date = context['execution_date']
    
    # Send alert to monitoring system
    send_slack_alert(f"Task {task_id} in {dag_id} failed on {execution_date}")

def retry_callback(context):
    """Called on each retry attempt"""
    attempt = context['task_instance'].try_number
    print(f"Retry attempt {attempt}")
```

## 8. Branching and Conditional Logic
**Creating Dynamic Workflows**:

### BranchPythonOperator
```python
from airflow.operators.python import BranchPythonOperator

def decide_branch(**context):
    """Decide which path to take based on conditions"""
    execution_date = context['ds']
    
    # Example: different processing for weekends
    if datetime.strptime(execution_date, '%Y-%m-%d').weekday() >= 5:
        return 'weekend_processing'
    else:
        return 'weekday_processing'

branch_task = BranchPythonOperator(
    task_id='decide_processing_type',
    python_callable=decide_branch
)

# Branch paths
weekend_task = PythonOperator(task_id='weekend_processing', ...)
weekday_task = PythonOperator(task_id='weekday_processing', ...)

# Convergence point (use trigger_rule to handle skipped branches)
final_task = PythonOperator(
    task_id='final_processing',
    trigger_rule='none_failed_min_one_success'
)

# Dependencies
branch_task >> [weekend_task, weekday_task] >> final_task
```

### ShortCircuitOperator
```python
from airflow.operators.python import ShortCircuitOperator

def check_condition(**context):
    """Return True to continue, False to skip downstream tasks"""
    data_available = check_data_exists(context['ds'])
    return data_available

gate = ShortCircuitOperator(
    task_id='check_data_available',
    python_callable=check_condition
)
```

## 9. TaskFlow API (Modern Airflow)
**Python-First Approach with Decorators**:

### Basic TaskFlow Pattern
```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['taskflow', 'modern']
)
def modern_pipeline():
    
    @task
    def extract() -> dict:
        """Extract data and return as dictionary"""
        return {"records": 1000, "source": "api"}
    
    @task
    def transform(data: dict) -> dict:
        """Transform the extracted data"""
        return {
            "processed_records": data["records"] * 2,
            "source": data["source"]
        }
    
    @task
    def load(data: dict) -> str:
        """Load processed data"""
        print(f"Loading {data['processed_records']} records")
        return "success"
    
    # Create dependencies through function calls
    extracted_data = extract()
    transformed_data = transform(extracted_data)
    load(transformed_data)

# Instantiate the DAG
dag_instance = modern_pipeline()
```

### Advanced TaskFlow Features
```python
@dag(schedule='@daily', start_date=datetime(2024, 1, 1))
def advanced_taskflow():
    
    @task.branch
    def decide_path(data_size: int) -> str:
        """Branching with TaskFlow"""
        return 'large_data_processing' if data_size > 1000 else 'small_data_processing'
    
    @task
    def get_data_size() -> int:
        return 1500
    
    @task
    def large_data_processing():
        print("Processing large dataset")
    
    @task
    def small_data_processing():
        print("Processing small dataset")
    
    @task(trigger_rule='none_failed_min_one_success')
    def final_step():
        print("Pipeline completed")
    
    # Flow
    size = get_data_size()
    branch = decide_path(size)
    branch >> [large_data_processing(), small_data_processing()] >> final_step()

dag_instance = advanced_taskflow()
```

## 10. Sensors
**Waiting for External Conditions**:

### Common Sensor Types
```python
from airflow.sensors.filesystem import FileSensor
from airflow.sensors.time_delta import TimeDeltaSensor
from airflow.sensors.http import HttpSensor
from airflow.sensors.sql import SqlSensor

# Wait for file to appear
file_sensor = FileSensor(
    task_id='wait_for_file',
    filepath='/data/input/{{ ds }}_data.csv',
    poke_interval=60,        # Check every 60 seconds
    timeout=3600,            # Give up after 1 hour
    mode='poke'              # 'poke' or 'reschedule'
)

# Wait for API endpoint
api_sensor = HttpSensor(
    task_id='wait_for_api',
    http_conn_id='api_connection',
    endpoint='health',
    poke_interval=30,
    timeout=600
)

# Wait for database condition
sql_sensor = SqlSensor(
    task_id='wait_for_data',
    conn_id='postgres_default',
    sql="SELECT COUNT(*) FROM orders WHERE date = '{{ ds }}'",
    poke_interval=120,
    timeout=1800
)
```

### Custom Sensors
```python
from airflow.sensors.base import BaseSensorOperator

class CustomApiSensor(BaseSensorOperator):
    def __init__(self, api_endpoint, **kwargs):
        super().__init__(**kwargs)
        self.api_endpoint = api_endpoint
    
    def poke(self, context):
        """Return True when condition is met"""
        response = requests.get(self.api_endpoint)
        return response.status_code == 200 and response.json().get('ready', False)

custom_sensor = CustomApiSensor(
    task_id='wait_for_custom_condition',
    api_endpoint='https://api.example.com/status'
)
```

## 11. Task Groups
**Organizing Related Tasks**:

```python
from airflow.utils.task_group import TaskGroup

with DAG('grouped_pipeline', ...) as dag:
    
    start = EmptyOperator(task_id='start')
    
    # Group related extraction tasks
    with TaskGroup('extraction_group') as extract_group:
        extract_sales = PythonOperator(task_id='extract_sales', ...)
        extract_customers = PythonOperator(task_id='extract_customers', ...)
        extract_products = PythonOperator(task_id='extract_products', ...)
    
    # Group transformation tasks
    with TaskGroup('transformation_group') as transform_group:
        transform_sales = PythonOperator(task_id='transform_sales', ...)
        transform_customers = PythonOperator(task_id='transform_customers', ...)
        
        # Nested task groups
        with TaskGroup('validation_subgroup') as validation:
            validate_data = PythonOperator(task_id='validate', ...)
            clean_data = PythonOperator(task_id='clean', ...)
    
    end = EmptyOperator(task_id='end')
    
    # Dependencies between groups
    start >> extract_group >> transform_group >> end
```

## 12. Pools and Priority
**Resource Management**:

### Pools
Limit concurrent execution of tasks across all DAGs:
```python
# Create pool via UI or CLI:
# airflow pools set limited_resource 5 "Database connection pool"

task = PythonOperator(
    task_id='database_task',
    python_callable=db_operation,
    pool='limited_resource',    # Pool name
    pool_slots=2               # Slots required (default: 1)
)
```

### Priority Weights
Control execution order within pools:
```python
high_priority_task = PythonOperator(
    task_id='urgent_task',
    python_callable=urgent_function,
    pool='shared_pool',
    priority_weight=100        # Higher = higher priority
)

low_priority_task = PythonOperator(
    task_id='background_task',
    python_callable=background_function,
    pool='shared_pool',
    priority_weight=1
)
```

## 13. Variables and Connections
**Configuration Management**:

### Airflow Variables
Store configuration values accessible across DAGs:
```python
from airflow.models import Variable

# Set via UI, CLI, or code
# airflow variables set api_key "your-secret-key"

def my_task():
    # Get simple variable
    api_key = Variable.get("api_key")
    
    # Get with default value
    batch_size = Variable.get("batch_size", default_var=100)
    
    # Get JSON variable
    config = Variable.get("app_config", deserialize_json=True)
    
    # Use in templates
    return f"Processing with key: {api_key}"

# Template usage
BashOperator(
    task_id='use_variable',
    bash_command='echo "API Key: {{ var.value.api_key }}"'
)
```

### Connections
Store connection information for external systems:
```python
from airflow.hooks.base import BaseHook

def connect_to_database():
    # Get connection details
    conn = BaseHook.get_connection("postgres_prod")
    
    host = conn.host
    port = conn.port
    username = conn.login
    password = conn.password
    database = conn.schema
    
    # Use connection
    connection_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"
```

## 14. SLA and Monitoring
**Service Level Agreements and Observability**:

### SLA Configuration
```python
from datetime import timedelta

task = PythonOperator(
    task_id='time_critical_task',
    python_callable=critical_function,
    sla=timedelta(hours=2),           # Task should complete within 2 hours
    email_on_failure=True,
    email_on_retry=False,
    email=['admin@company.com']
)

# DAG-level SLA
dag = DAG(
    'sla_monitored_dag',
    sla_miss_callback=handle_sla_miss,  # Custom SLA handler
    default_args={
        'sla': timedelta(hours=4)       # Default SLA for all tasks
    }
)
```

### Monitoring and Alerting
```python
def sla_miss_callback(dag, task_list, blocking_task_list, slas, blocking_tis):
    """Handle SLA misses"""
    message = f"SLA missed for tasks: {[t.task_id for t in task_list]}"
    send_alert_to_slack(message)

def failure_callback(context):
    """Handle task failures"""
    task = context['task_instance']
    dag_run = context['dag_run']
    
    alert_message = {
        'dag_id': task.dag_id,
        'task_id': task.task_id,
        'execution_date': str(dag_run.execution_date),
        'log_url': task.log_url
    }
    
    send_to_monitoring_system(alert_message)
```

## 15. Executors
**Task Execution Backends**:

### Sequential Executor (Development)
- Single-threaded execution
- Good for testing and development
- Default for SQLite backend

### Local Executor
- Multi-process execution on single machine
- Good for small to medium workloads
- Uses PostgreSQL or MySQL

### Celery Executor
- Distributed execution across multiple workers
- Horizontal scaling capability
- Requires message broker (Redis/RabbitMQ)

### Kubernetes Executor
- Each task runs in separate Kubernetes pod
- Dynamic resource allocation
- Good for containerized environments

### Configuration Example
```python
# In airflow.cfg
[core]
executor = CeleryExecutor

[celery]
broker_url = redis://localhost:6379/0
result_backend = db+postgresql://user:pass@localhost/airflow
```

## 16. Data Lineage and Datasets
**Tracking Data Dependencies**:

### Dataset Definitions
```python
from airflow.datasets import Dataset

# Define datasets
raw_sales = Dataset("s3://data-lake/raw/sales/")
processed_sales = Dataset("s3://data-lake/processed/sales/")
sales_report = Dataset("s3://reports/sales/daily/")

# Producer DAG
@dag(schedule='@daily', outlets=[raw_sales])
def extract_sales_data():
    @task(outlets=[raw_sales])
    def extract():
        # Extract data logic
        pass

# Consumer DAG
@dag(schedule=[raw_sales], outlets=[processed_sales])
def process_sales_data():
    @task(outlets=[processed_sales])
    def transform():
        # Transform data logic
        pass

# Final consumer
@dag(schedule=[processed_sales], outlets=[sales_report])
def generate_sales_report():
    @task(outlets=[sales_report])
    def create_report():
        # Report generation logic
        pass
```

## 17. Security Best Practices
**Securing Airflow Deployments**:

### Secrets Backend
```python
# Use external secrets management
from airflow.configuration import conf

# Configure in airflow.cfg
[secrets]
backend = airflow.providers.hashicorp.secrets.vault.VaultBackend
backend_kwargs = {"connections_path": "connections", "variables_path": "variables"}
```

### RBAC and Authentication
```python
# Role-based access control
from airflow.security import permissions
from airflow.www.security import AirflowSecurityManager

class CustomSecurityManager(AirflowSecurityManager):
    def get_user_roles(self, user):
        # Custom role assignment logic
        return ['Admin'] if user.email.endswith('@company.com') else ['Viewer']
```

### Secure Connections
```python
# Use encrypted connections
from airflow.models.connection import Connection

conn = Connection(
    conn_id='secure_db',
    conn_type='postgres',
    host='db.company.com',
    login='{{ var.value.db_user }}',      # Use variables for credentials
    password='{{ var.value.db_password }}',
    port=5432,
    extra='{"sslmode": "require"}'        # Enable SSL
)
```

## 18. Performance Optimization
**Scaling and Tuning**:

### DAG Performance
```python
# Optimize DAG parsing
dag = DAG(
    'optimized_dag',
    max_active_runs=3,              # Limit concurrent DAG runs
    max_active_tasks=10,            # Limit concurrent tasks
    dagrun_timeout=timedelta(hours=2),  # Prevent hanging runs
    default_args={
        'pool': 'default_pool',     # Use resource pools
        'queue': 'high_priority'    # Use specific queues
    }
)

# Efficient task design
@task
def batch_process(batch_size: int = 1000):
    """Process data in batches for better performance"""
    for batch in get_data_batches(batch_size):
        process_batch(batch)
```

### Database Optimization
```python
# Configure connection pooling
[core]
sql_alchemy_pool_size = 10
sql_alchemy_pool_recycle = 3600
sql_alchemy_max_overflow = 20

# Optimize metadata database
[scheduler]
dag_dir_list_interval = 300      # Scan DAGs less frequently
min_file_process_interval = 30   # Process files less frequently
```

## Key Takeaways

1. **Start Simple**: Begin with basic DAGs and gradually add complexity
2. **Use TaskFlow API**: Modern approach for cleaner, more maintainable code
3. **Handle Errors Gracefully**: Implement proper retry logic and monitoring
4. **Optimize Performance**: Use pools, appropriate executors, and efficient task design
5. **Secure Your Deployment**: Use secrets backends and proper authentication
6. **Monitor Everything**: Set up comprehensive logging and alerting
7. **Test Thoroughly**: Test individual tasks before deploying full workflows
8. **Document Well**: Use clear naming and documentation for maintainability

This comprehensive guide covers the essential concepts needed to build robust, scalable, and maintainable Airflow workflows.