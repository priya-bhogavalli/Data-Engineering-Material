# Apache Airflow Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-30)](#basic-level-questions-1-30)
2. [Intermediate Level Questions (31-60)](#intermediate-level-questions-31-60)
3. [Advanced Level Questions (61-90)](#advanced-level-questions-61-90)
4. [DAG Design & Best Practices (91-120)](#dag-design--best-practices-91-120)
5. [Operators & Hooks (121-150)](#operators--hooks-121-150)
6. [Production & Monitoring (151-180)](#production--monitoring-151-180)
7. [Scenario-Based Questions (181-200)](#scenario-based-questions-181-200)

---

## Basic Level Questions (1-30)

### 1. What is Apache Airflow and how does it work?

**Apache Airflow** is an open-source platform for developing, scheduling, and monitoring workflows as Directed Acyclic Graphs (DAGs).

#### **Key Components:**

| Component | Description | Purpose |
|-----------|-------------|---------|
| **DAG** | Directed Acyclic Graph | Workflow definition |
| **Task** | Unit of work in DAG | Individual operation |
| **Operator** | Template for tasks | Defines what to execute |
| **Scheduler** | Triggers task execution | Workflow orchestration |
| **Executor** | Runs tasks | Task execution engine |
| **Web UI** | Visual interface | Monitoring and management |

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# Define default arguments
default_args = {
    'owner': 'data-engineer',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Create DAG
dag = DAG(
    'basic_data_pipeline',
    default_args=default_args,
    description='A basic data pipeline example',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['example', 'data-engineering']
)

def extract_data(**context):
    """Extract data from source"""
    print(f"Extracting data on {context['ds']}")
    # Simulate data extraction
    data = [
        {'id': 1, 'name': 'Alice', 'value': 100},
        {'id': 2, 'name': 'Bob', 'value': 200},
        {'id': 3, 'name': 'Charlie', 'value': 300}
    ]
    print(f"Extracted {len(data)} records")
    return data

def transform_data(**context):
    """Transform extracted data"""
    # Get data from previous task
    ti = context['ti']
    data = ti.xcom_pull(task_ids='extract_task')
    
    print(f"Transforming {len(data)} records")
    # Apply transformations
    transformed_data = []
    for record in data:
        transformed_record = {
            'id': record['id'],
            'name': record['name'].upper(),
            'value': record['value'] * 1.1,  # Apply 10% increase
            'processed_date': context['ds']
        }
        transformed_data.append(transformed_record)
    
    print(f"Transformed data: {transformed_data}")
    return transformed_data

def load_data(**context):
    """Load transformed data to destination"""
    ti = context['ti']
    data = ti.xcom_pull(task_ids='transform_task')
    
    print(f"Loading {len(data)} records to destination")
    # Simulate loading to database/file
    for record in data:
        print(f"  Loaded: {record}")
    
    print("Data loading completed successfully")

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

# Set task dependencies
extract_task >> transform_task >> load_task

print("DAG 'basic_data_pipeline' defined successfully")
```

**Output:**
```
DAG 'basic_data_pipeline' defined successfully

# When executed:
[2024-01-15 10:30:00] Extracting data on 2024-01-15
[2024-01-15 10:30:01] Extracted 3 records
[2024-01-15 10:30:02] Transforming 3 records
[2024-01-15 10:30:03] Transformed data: [{'id': 1, 'name': 'ALICE', 'value': 110.0, 'processed_date': '2024-01-15'}, ...]
[2024-01-15 10:30:04] Loading 3 records to destination
[2024-01-15 10:30:05] Data loading completed successfully
```

### 2. What are DAGs and their key properties?

**Answer:** DAGs (Directed Acyclic Graphs) represent workflows with tasks and dependencies.

#### 🎯 **DAG Properties**
- **Directed**: Tasks have specific execution order
- **Acyclic**: No circular dependencies
- **Graph**: Network of connected tasks
- **Idempotent**: Same result when run multiple times

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator

def demonstrate_dag_properties():
    """Demonstrate key DAG properties"""
    
    # DAG with comprehensive configuration
    dag = DAG(
        'dag_properties_demo',
        description='Demonstrates DAG properties and features',
        schedule_interval='@daily',  # Run daily
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 12, 31),  # Optional end date
        catchup=False,  # Don't run historical instances
        max_active_runs=1,  # Only one instance at a time
        max_active_tasks=3,  # Limit concurrent tasks
        default_view='graph',  # Default UI view
        orientation='LR',  # Left-to-right layout
        tags=['demo', 'properties', 'data-engineering'],
        params={  # DAG-level parameters
            'environment': 'development',
            'batch_size': 1000
        }
    )
    
    # Task functions
    def start_pipeline(**context):
        print(f"Starting pipeline for date: {context['ds']}")
        print(f"Environment: {context['params']['environment']}")
        print(f"Batch size: {context['params']['batch_size']}")
        return "Pipeline started"
    
    def parallel_task_1(**context):
        print("Executing parallel task 1")
        # Simulate work
        import time
        time.sleep(2)
        return "Task 1 completed"
    
    def parallel_task_2(**context):
        print("Executing parallel task 2")
        # Simulate work
        import time
        time.sleep(2)
        return "Task 2 completed"
    
    def parallel_task_3(**context):
        print("Executing parallel task 3")
        # Simulate work
        import time
        time.sleep(2)
        return "Task 3 completed"
    
    def join_results(**context):
        ti = context['ti']
        result1 = ti.xcom_pull(task_ids='parallel_1')
        result2 = ti.xcom_pull(task_ids='parallel_2')
        result3 = ti.xcom_pull(task_ids='parallel_3')
        
        print(f"Joining results: {result1}, {result2}, {result3}")
        return "All parallel tasks completed"
    
    def end_pipeline(**context):
        ti = context['ti']
        join_result = ti.xcom_pull(task_ids='join_task')
        print(f"Pipeline completed: {join_result}")
        return "Pipeline finished"
    
    # Define tasks
    start = PythonOperator(
        task_id='start_task',
        python_callable=start_pipeline,
        dag=dag
    )
    
    # Parallel tasks
    parallel_1 = PythonOperator(
        task_id='parallel_1',
        python_callable=parallel_task_1,
        dag=dag
    )
    
    parallel_2 = PythonOperator(
        task_id='parallel_2',
        python_callable=parallel_task_2,
        dag=dag
    )
    
    parallel_3 = PythonOperator(
        task_id='parallel_3',
        python_callable=parallel_task_3,
        dag=dag
    )
    
    # Join task
    join_task = PythonOperator(
        task_id='join_task',
        python_callable=join_results,
        dag=dag
    )
    
    # End task
    end = PythonOperator(
        task_id='end_task',
        python_callable=end_pipeline,
        dag=dag
    )
    
    # Define dependencies (demonstrates DAG structure)
    start >> [parallel_1, parallel_2, parallel_3] >> join_task >> end
    
    return dag

# Create the DAG
demo_dag = demonstrate_dag_properties()
print(f"Created DAG: {demo_dag.dag_id}")
print(f"Schedule: {demo_dag.schedule_interval}")
print(f"Tasks: {[task.task_id for task in demo_dag.tasks]}")
```

**Output:**
```
Created DAG: dag_properties_demo
Schedule: @daily
Tasks: ['start_task', 'parallel_1', 'parallel_2', 'parallel_3', 'join_task', 'end_task']

# When executed:
[2024-01-15 10:30:00] Starting pipeline for date: 2024-01-15
[2024-01-15 10:30:01] Environment: development
[2024-01-15 10:30:02] Batch size: 1000
[2024-01-15 10:30:03] Executing parallel task 1
[2024-01-15 10:30:03] Executing parallel task 2
[2024-01-15 10:30:03] Executing parallel task 3
[2024-01-15 10:30:05] Joining results: Task 1 completed, Task 2 completed, Task 3 completed
[2024-01-15 10:30:06] Pipeline completed: All parallel tasks completed
```

### 3. What are the different types of Airflow operators?

**Answer:** Operators define what gets executed in each task.

#### 🎯 **Common Operator Types**
- **PythonOperator**: Execute Python functions
- **BashOperator**: Run bash commands
- **SQLOperator**: Execute SQL queries
- **EmailOperator**: Send emails
- **SensorOperator**: Wait for conditions

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.operators.email import EmailOperator
from airflow.operators.dummy import DummyOperator

# DAG definition
dag = DAG(
    'operator_examples',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['operators', 'examples']
)

# 1. PythonOperator Example
def process_data(**context):
    """Python function to process data"""
    import json
    import random
    
    # Generate sample data
    data = {
        'date': context['ds'],
        'records_processed': random.randint(100, 1000),
        'success_rate': round(random.uniform(0.85, 0.99), 2),
        'processing_time': round(random.uniform(10, 60), 1)
    }
    
    print(f"Processing data for {data['date']}")
    print(f"Records processed: {data['records_processed']}")
    print(f"Success rate: {data['success_rate']}%")
    print(f"Processing time: {data['processing_time']} seconds")
    
    return data

python_task = PythonOperator(
    task_id='python_data_processing',
    python_callable=process_data,
    dag=dag
)

# 2. BashOperator Example
bash_task = BashOperator(
    task_id='bash_file_operations',
    bash_command='''
    echo "Starting file operations..."
    mkdir -p /tmp/airflow_demo
    echo "Created directory: /tmp/airflow_demo"
    
    # Create sample data file
    echo "id,name,value" > /tmp/airflow_demo/sample_data.csv
    echo "1,Alice,100" >> /tmp/airflow_demo/sample_data.csv
    echo "2,Bob,200" >> /tmp/airflow_demo/sample_data.csv
    echo "3,Charlie,300" >> /tmp/airflow_demo/sample_data.csv
    
    echo "Sample data file created:"
    cat /tmp/airflow_demo/sample_data.csv
    
    # Count lines
    line_count=$(wc -l < /tmp/airflow_demo/sample_data.csv)
    echo "File contains $line_count lines"
    ''',
    dag=dag
)

# 3. SQL Operator Example (PostgreSQL)
sql_task = PostgresOperator(
    task_id='sql_data_operations',
    postgres_conn_id='postgres_default',  # Connection ID in Airflow
    sql='''
    -- Create temporary table
    CREATE TEMP TABLE daily_metrics (
        date DATE,
        metric_name VARCHAR(50),
        metric_value NUMERIC
    );
    
    -- Insert sample data
    INSERT INTO daily_metrics VALUES
    ('{{ ds }}', 'users_active', 1250),
    ('{{ ds }}', 'orders_processed', 89),
    ('{{ ds }}', 'revenue_generated', 15420.50);
    
    -- Query results
    SELECT 
        date,
        metric_name,
        metric_value,
        CASE 
            WHEN metric_name = 'revenue_generated' THEN metric_value * 1.1
            ELSE metric_value
        END as adjusted_value
    FROM daily_metrics
    ORDER BY metric_name;
    ''',
    dag=dag
)

# 4. HTTP Sensor Example
http_sensor = HttpSensor(
    task_id='wait_for_api_endpoint',
    http_conn_id='http_default',
    endpoint='api/health',
    poke_interval=30,  # Check every 30 seconds
    timeout=300,  # Timeout after 5 minutes
    dag=dag
)

# 5. Email Operator Example
def generate_report(**context):
    """Generate report data for email"""
    ti = context['ti']
    processing_data = ti.xcom_pull(task_ids='python_data_processing')
    
    report = f"""
    Daily Data Processing Report - {context['ds']}
    
    Summary:
    - Records Processed: {processing_data.get('records_processed', 'N/A')}
    - Success Rate: {processing_data.get('success_rate', 'N/A')}%
    - Processing Time: {processing_data.get('processing_time', 'N/A')} seconds
    
    Status: Pipeline completed successfully
    """
    
    return report

report_task = PythonOperator(
    task_id='generate_report',
    python_callable=generate_report,
    dag=dag
)

email_task = EmailOperator(
    task_id='send_completion_email',
    to=['data-team@company.com'],
    subject='Daily Pipeline Completion - {{ ds }}',
    html_content='''
    <h3>Pipeline Execution Summary</h3>
    <p>The daily data pipeline has completed successfully.</p>
    <p><strong>Execution Date:</strong> {{ ds }}</p>
    <p><strong>DAG:</strong> {{ dag.dag_id }}</p>
    <p>Please check the Airflow UI for detailed logs.</p>
    ''',
    dag=dag
)

# 6. Dummy Operators for workflow control
start_task = DummyOperator(
    task_id='start_pipeline',
    dag=dag
)

end_task = DummyOperator(
    task_id='end_pipeline',
    dag=dag
)

# Define task dependencies
start_task >> [python_task, bash_task] >> sql_task
sql_task >> http_sensor >> report_task >> email_task >> end_task

print("Operator examples DAG created with the following tasks:")
for task in dag.tasks:
    print(f"  - {task.task_id} ({type(task).__name__})")
```

**Output:**
```
Operator examples DAG created with the following tasks:
  - start_pipeline (DummyOperator)
  - python_data_processing (PythonOperator)
  - bash_file_operations (BashOperator)
  - sql_data_operations (PostgresOperator)
  - wait_for_api_endpoint (HttpSensor)
  - generate_report (PythonOperator)
  - send_completion_email (EmailOperator)
  - end_pipeline (DummyOperator)

# When executed:
[2024-01-15 10:30:00] Processing data for 2024-01-15
[2024-01-15 10:30:01] Records processed: 456
[2024-01-15 10:30:02] Success rate: 0.92%
[2024-01-15 10:30:03] Processing time: 23.4 seconds
[2024-01-15 10:30:04] Starting file operations...
[2024-01-15 10:30:05] Created directory: /tmp/airflow_demo
[2024-01-15 10:30:06] Sample data file created:
[2024-01-15 10:30:07] id,name,value
[2024-01-15 10:30:08] 1,Alice,100
[2024-01-15 10:30:09] 2,Bob,200
[2024-01-15 10:30:10] 3,Charlie,300
[2024-01-15 10:30:11] File contains 4 lines
```

### 4. How do you handle task dependencies in Airflow?

**Answer:** Dependencies define execution order and can be set using various methods.

#### 🎯 **Dependency Methods**
- **Bitshift operators**: `>>` and `<<`
- **set_upstream/set_downstream**: Explicit methods
- **depends_on_past**: Task depends on previous run
- **wait_for_downstream**: Wait for downstream tasks

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator

dag = DAG(
    'dependency_examples',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False
)

# Task functions
def task_a(**context):
    print(f"Executing Task A on {context['ds']}")
    return "Task A completed"

def task_b(**context):
    print(f"Executing Task B on {context['ds']}")
    return "Task B completed"

def task_c(**context):
    print(f"Executing Task C on {context['ds']}")
    return "Task C completed"

def task_d(**context):
    ti = context['ti']
    result_a = ti.xcom_pull(task_ids='task_a')
    result_b = ti.xcom_pull(task_ids='task_b')
    print(f"Task D received: {result_a}, {result_b}")
    return "Task D completed"

def task_e(**context):
    ti = context['ti']
    result_c = ti.xcom_pull(task_ids='task_c')
    result_d = ti.xcom_pull(task_ids='task_d')
    print(f"Task E received: {result_c}, {result_d}")
    return "Task E completed"

# Create tasks
start = DummyOperator(task_id='start', dag=dag)

task_a = PythonOperator(
    task_id='task_a',
    python_callable=task_a,
    dag=dag
)

task_b = PythonOperator(
    task_id='task_b',
    python_callable=task_b,
    dag=dag
)

task_c = PythonOperator(
    task_id='task_c',
    python_callable=task_c,
    dag=dag
)

task_d = PythonOperator(
    task_id='task_d',
    python_callable=task_d,
    dag=dag
)

task_e = PythonOperator(
    task_id='task_e',
    python_callable=task_e,
    dag=dag
)

end = DummyOperator(task_id='end', dag=dag)

# Method 1: Bitshift operators (most common)
start >> [task_a, task_b]  # Parallel execution
task_a >> task_d
task_b >> task_d
[task_c, task_d] >> task_e  # Multiple upstream dependencies
task_e >> end

# Method 2: Using set_upstream/set_downstream (alternative)
# task_a.set_downstream(task_d)
# task_b.set_downstream(task_d)
# task_d.set_upstream([task_a, task_b])

# Method 3: Chain for linear dependencies
# from airflow.models.baseoperator import chain
# chain(start, task_a, task_d, task_e, end)

print("Dependency structure:")
print("start >> [task_a, task_b]")
print("task_a >> task_d")
print("task_b >> task_d") 
print("[task_c, task_d] >> task_e")
print("task_e >> end")

# Demonstrate dependency properties
def demonstrate_dependency_features():
    """Show advanced dependency features"""
    
    # Task with depends_on_past
    depends_on_past_task = PythonOperator(
        task_id='depends_on_past_example',
        python_callable=lambda **context: print(f"This task depends on past success: {context['ds']}"),
        depends_on_past=True,  # Must wait for previous run to succeed
        dag=dag
    )
    
    # Task with wait_for_downstream
    wait_downstream_task = PythonOperator(
        task_id='wait_downstream_example',
        python_callable=lambda **context: print(f"Waiting for downstream: {context['ds']}"),
        wait_for_downstream=True,  # Wait for downstream tasks in previous run
        dag=dag
    )
    
    return depends_on_past_task, wait_downstream_task

# Add advanced dependency examples
advanced_tasks = demonstrate_dependency_features()
print(f"Added advanced dependency tasks: {[task.task_id for task in advanced_tasks]}")
```

**Output:**
```
Dependency structure:
start >> [task_a, task_b]
task_a >> task_d
task_b >> task_d
[task_c, task_d] >> task_e
task_e >> end
Added advanced dependency tasks: ['depends_on_past_example', 'wait_downstream_example']

# When executed:
[2024-01-15 10:30:00] Executing Task A on 2024-01-15
[2024-01-15 10:30:00] Executing Task B on 2024-01-15
[2024-01-15 10:30:01] Executing Task C on 2024-01-15
[2024-01-15 10:30:02] Task D received: Task A completed, Task B completed
[2024-01-15 10:30:03] Task E received: Task C completed, Task D completed
```

### 5. What is XCom and how is it used for task communication?

**Answer:** XCom (cross-communication) enables data sharing between tasks.

#### 🎯 **XCom Features**
- **Push/Pull**: Send and receive data between tasks
- **Automatic**: Return values automatically pushed
- **Serialization**: JSON serializable data only
- **Size Limits**: Limited by backend database

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import json

dag = DAG(
    'xcom_examples',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False
)

def extract_customer_data(**context):
    """Extract customer data and push to XCom"""
    import random
    
    # Simulate data extraction
    customers = []
    for i in range(5):
        customer = {
            'id': i + 1,
            'name': f'Customer_{i + 1}',
            'email': f'customer{i + 1}@example.com',
            'orders': random.randint(1, 10),
            'total_spent': round(random.uniform(100, 1000), 2)
        }
        customers.append(customer)
    
    print(f"Extracted {len(customers)} customers")
    for customer in customers:
        print(f"  {customer['name']}: {customer['orders']} orders, ${customer['total_spent']}")
    
    # Automatic XCom push (return value)
    return customers

def calculate_metrics(**context):
    """Calculate metrics from customer data"""
    ti = context['ti']
    
    # Pull data from previous task
    customers = ti.xcom_pull(task_ids='extract_customers')
    
    if not customers:
        print("No customer data received")
        return None
    
    # Calculate metrics
    total_customers = len(customers)
    total_orders = sum(c['orders'] for c in customers)
    total_revenue = sum(c['total_spent'] for c in customers)
    avg_orders_per_customer = total_orders / total_customers
    avg_revenue_per_customer = total_revenue / total_customers
    
    metrics = {
        'date': context['ds'],
        'total_customers': total_customers,
        'total_orders': total_orders,
        'total_revenue': round(total_revenue, 2),
        'avg_orders_per_customer': round(avg_orders_per_customer, 2),
        'avg_revenue_per_customer': round(avg_revenue_per_customer, 2)
    }
    
    print("Calculated metrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    
    # Manual XCom push with custom key
    ti.xcom_push(key='daily_metrics', value=metrics)
    
    # Also return for automatic push
    return metrics

def generate_segments(**context):
    """Generate customer segments"""
    ti = context['ti']
    
    # Pull original customer data
    customers = ti.xcom_pull(task_ids='extract_customers')
    
    if not customers:
        return None
    
    # Segment customers based on spending
    segments = {'high_value': [], 'medium_value': [], 'low_value': []}
    
    for customer in customers:
        if customer['total_spent'] > 500:
            segments['high_value'].append(customer)
        elif customer['total_spent'] > 200:
            segments['medium_value'].append(customer)
        else:
            segments['low_value'].append(customer)
    
    segment_summary = {
        'high_value_count': len(segments['high_value']),
        'medium_value_count': len(segments['medium_value']),
        'low_value_count': len(segments['low_value'])
    }
    
    print("Customer segments:")
    for segment, count in segment_summary.items():
        print(f"  {segment}: {count} customers")
    
    # Push segments with custom key
    ti.xcom_push(key='customer_segments', value=segments)
    
    return segment_summary

def create_report(**context):
    """Create final report using all XCom data"""
    ti = context['ti']
    
    # Pull data from multiple tasks
    customers = ti.xcom_pull(task_ids='extract_customers')
    metrics = ti.xcom_pull(task_ids='calculate_metrics', key='daily_metrics')
    segments = ti.xcom_pull(task_ids='generate_segments', key='customer_segments')
    segment_summary = ti.xcom_pull(task_ids='generate_segments')
    
    print("=== Daily Customer Report ===")
    print(f"Date: {context['ds']}")
    print()
    
    if metrics:
        print("📊 Key Metrics:")
        print(f"  Total Customers: {metrics['total_customers']}")
        print(f"  Total Orders: {metrics['total_orders']}")
        print(f"  Total Revenue: ${metrics['total_revenue']}")
        print(f"  Avg Orders/Customer: {metrics['avg_orders_per_customer']}")
        print(f"  Avg Revenue/Customer: ${metrics['avg_revenue_per_customer']}")
        print()
    
    if segment_summary:
        print("🎯 Customer Segments:")
        print(f"  High Value: {segment_summary['high_value_count']} customers")
        print(f"  Medium Value: {segment_summary['medium_value_count']} customers")
        print(f"  Low Value: {segment_summary['low_value_count']} customers")
        print()
    
    # Create comprehensive report
    report = {
        'date': context['ds'],
        'metrics': metrics,
        'segments': segment_summary,
        'total_customers': len(customers) if customers else 0
    }
    
    print("📋 Report generated successfully")
    return report

def demonstrate_xcom_operations(**context):
    """Demonstrate various XCom operations"""
    ti = context['ti']
    
    print("🔍 XCom Operations Demo:")
    
    # List all XCom entries for this DAG run
    dag_run = context['dag_run']
    xcom_entries = ti.get_dagrun().get_task_instances()
    
    print("Available XCom entries:")
    for task_instance in xcom_entries:
        if task_instance.xcom_pull():
            print(f"  Task: {task_instance.task_id}")
            xcom_data = task_instance.xcom_pull()
            if isinstance(xcom_data, dict):
                print(f"    Keys: {list(xcom_data.keys())}")
            else:
                print(f"    Type: {type(xcom_data).__name__}")

# Define tasks
extract_task = PythonOperator(
    task_id='extract_customers',
    python_callable=extract_customer_data,
    dag=dag
)

metrics_task = PythonOperator(
    task_id='calculate_metrics',
    python_callable=calculate_metrics,
    dag=dag
)

segments_task = PythonOperator(
    task_id='generate_segments',
    python_callable=generate_segments,
    dag=dag
)

report_task = PythonOperator(
    task_id='create_report',
    python_callable=create_report,
    dag=dag
)

xcom_demo_task = PythonOperator(
    task_id='xcom_operations_demo',
    python_callable=demonstrate_xcom_operations,
    dag=dag
)

# Set dependencies
extract_task >> [metrics_task, segments_task] >> report_task >> xcom_demo_task

print("XCom example DAG created with task communication flow")
```

**Output:**
```
XCom example DAG created with task communication flow

# When executed:
[2024-01-15 10:30:00] Extracted 5 customers
[2024-01-15 10:30:01]   Customer_1: 3 orders, $245.67
[2024-01-15 10:30:02]   Customer_2: 7 orders, $678.90
[2024-01-15 10:30:03]   Customer_3: 2 orders, $123.45
[2024-01-15 10:30:04]   Customer_4: 9 orders, $890.12
[2024-01-15 10:30:05]   Customer_5: 4 orders, $456.78

[2024-01-15 10:30:06] Calculated metrics:
[2024-01-15 10:30:07]   date: 2024-01-15
[2024-01-15 10:30:08]   total_customers: 5
[2024-01-15 10:30:09]   total_orders: 25
[2024-01-15 10:30:10]   total_revenue: 2394.92
[2024-01-15 10:30:11]   avg_orders_per_customer: 5.0
[2024-01-15 10:30:12]   avg_revenue_per_customer: 478.98

[2024-01-15 10:30:13] Customer segments:
[2024-01-15 10:30:14]   high_value_count: 2 customers
[2024-01-15 10:30:15]   medium_value_count: 2 customers
[2024-01-15 10:30:16]   low_value_count: 1 customers

[2024-01-15 10:30:17] === Daily Customer Report ===
[2024-01-15 10:30:18] Date: 2024-01-15
[2024-01-15 10:30:19] 📊 Key Metrics:
[2024-01-15 10:30:20]   Total Customers: 5
[2024-01-15 10:30:21]   Total Orders: 25
[2024-01-15 10:30:22]   Total Revenue: $2394.92
[2024-01-15 10:30:23]   Avg Orders/Customer: 5.0
[2024-01-15 10:30:24]   Avg Revenue/Customer: $478.98
[2024-01-15 10:30:25] 🎯 Customer Segments:
[2024-01-15 10:30:26]   High Value: 2 customers
[2024-01-15 10:30:27]   Medium Value: 2 customers
[2024-01-15 10:30:28]   Low Value: 1 customers
[2024-01-15 10:30:29] 📋 Report generated successfully
```