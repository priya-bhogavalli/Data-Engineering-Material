# Apache Airflow - Conceptual Overview

## 🎯 What is Apache Airflow?

Apache Airflow is a **workflow orchestration platform** that allows you to programmatically author, schedule, and monitor data pipelines. Think of it as a sophisticated project manager that coordinates complex sequences of tasks, ensuring they run in the right order, at the right time, and handles failures gracefully.

### Key Characteristics:
- **Code-Based**: Workflows defined as Python code (DAGs)
- **Scalable**: Handles thousands of tasks across multiple machines
- **Extensible**: Rich ecosystem of operators and hooks
- **Monitoring**: Comprehensive web UI for pipeline visibility
- **Fault Tolerant**: Automatic retries and failure handling

## 🏗️ Core Architecture Concepts

### 1. Airflow Components Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    Airflow Architecture                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐                                       │
│  │   Web Server    │ ←── Users access UI here              │
│  │   (Flask App)   │                                       │
│  └─────────────────┘                                       │
│           │                                                 │
│           ▼                                                 │
│  ┌─────────────────┐     ┌─────────────────┐              │
│  │   Scheduler     │────▶│   Executor      │              │
│  │ (Task Manager)  │     │ (Task Runner)   │              │
│  └─────────────────┘     └─────────────────┘              │
│           │                       │                        │
│           ▼                       ▼                        │
│  ┌─────────────────┐     ┌─────────────────┐              │
│  │   Metadata DB   │     │   Worker Nodes  │              │
│  │  (PostgreSQL/   │     │                 │              │
│  │   MySQL)        │     │ ┌─────────────┐ │              │
│  └─────────────────┘     │ │   Task 1    │ │              │
│                          │ │   Task 2    │ │              │
│                          │ │   Task 3    │ │              │
│                          │ └─────────────┘ │              │
│                          └─────────────────┘              │
└─────────────────────────────────────────────────────────────┘
```

### Component Explanations:

**Web Server**: 
- Provides the Airflow UI for monitoring and management
- Shows DAG status, task logs, and execution history
- Allows manual triggering and configuration

**Scheduler**: 
- Heart of Airflow - decides when and what to run
- Monitors DAG files for changes
- Creates task instances and sends them to executor
- Handles dependencies and scheduling logic

**Executor**: 
- Determines how and where tasks are executed
- Types: Sequential, Local, Celery, Kubernetes, etc.
- Manages worker processes and task distribution

**Metadata Database**: 
- Stores all Airflow state information
- DAG definitions, task instances, connections, variables
- Critical for Airflow operation and recovery

**Worker Nodes**: 
- Execute the actual tasks
- Can be local processes or distributed across machines
- Run your business logic (Python functions, bash commands, etc.)

## 📊 DAG (Directed Acyclic Graph) Concepts

### 1. What is a DAG?

A **DAG** represents your workflow as a collection of tasks with dependencies. It's "directed" because tasks flow in one direction, and "acyclic" because there are no loops.

**Visual DAG Example**:
```
┌─────────────────────────────────────────────────────────────┐
│                    E-commerce ETL DAG                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐                                           │
│  │   Extract   │                                           │
│  │ Customer    │                                           │
│  │   Data      │                                           │
│  └─────────────┘                                           │
│         │                                                  │
│         ▼                                                  │
│  ┌─────────────┐     ┌─────────────┐                      │
│  │ Transform   │     │   Extract   │                      │
│  │ Customer    │     │   Orders    │                      │
│  │   Data      │     │    Data     │                      │
│  └─────────────┘     └─────────────┘                      │
│         │                     │                           │
│         └─────────┬───────────┘                           │
│                   ▼                                       │
│            ┌─────────────┐                                │
│            │   Join &    │                                │
│            │ Aggregate   │                                │
│            │    Data     │                                │
│            └─────────────┘                                │
│                   │                                       │
│                   ▼                                       │
│            ┌─────────────┐                                │
│            │    Load     │                                │
│            │   to DW     │                                │
│            └─────────────┘                                │
│                   │                                       │
│                   ▼                                       │
│            ┌─────────────┐                                │
│            │   Send      │                                │
│            │ Notification│                                │
│            └─────────────┘                                │
└─────────────────────────────────────────────────────────────┘
```

### 2. DAG Structure and Properties

**Basic DAG Definition**:
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# DAG configuration
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

# Create DAG
dag = DAG(
    'customer_analytics_pipeline',
    default_args=default_args,
    description='Daily customer analytics processing',
    schedule_interval='@daily',  # Run once per day
    catchup=False,  # Don't run historical instances
    max_active_runs=1,  # Only one instance at a time
    tags=['analytics', 'customer', 'daily']
)
```

**Key DAG Properties Explained**:

- **schedule_interval**: When the DAG should run
  - `@daily`, `@hourly`, `@weekly`
  - Cron expressions: `0 2 * * *` (2 AM daily)
  - `None` for manual triggering only

- **start_date**: When the DAG becomes active
- **catchup**: Whether to run missed historical runs
- **max_active_runs**: Concurrent DAG instances allowed
- **retries**: How many times to retry failed tasks

## 🔧 Task and Operator Concepts

### 1. What are Tasks and Operators?

**Tasks** are individual units of work in your DAG. **Operators** define what type of work a task performs.

### 2. Common Operator Types

**PythonOperator**: Execute Python functions
```python
def extract_customer_data():
    # Your data extraction logic
    customers = fetch_from_database("SELECT * FROM customers")
    return customers

extract_task = PythonOperator(
    task_id='extract_customers',
    python_callable=extract_customer_data,
    dag=dag
)
```

**BashOperator**: Execute shell commands
```python
from airflow.operators.bash import BashOperator

cleanup_task = BashOperator(
    task_id='cleanup_temp_files',
    bash_command='rm -rf /tmp/processing/*',
    dag=dag
)
```

**SQLOperator**: Execute SQL queries
```python
from airflow.providers.postgres.operators.postgres import PostgresOperator

create_summary_table = PostgresOperator(
    task_id='create_customer_summary',
    postgres_conn_id='postgres_default',
    sql="""
        CREATE TABLE IF NOT EXISTS customer_summary AS
        SELECT 
            customer_id,
            COUNT(*) as order_count,
            SUM(amount) as total_spent
        FROM orders 
        GROUP BY customer_id
    """,
    dag=dag
)
```

### 3. Task Dependencies

**Setting Dependencies**:
```python
# Method 1: Using >> and << operators
extract_task >> transform_task >> load_task

# Method 2: Using set_upstream/set_downstream
transform_task.set_upstream(extract_task)
load_task.set_upstream(transform_task)

# Method 3: Complex dependencies
extract_customers >> [transform_customers, validate_customers] >> load_customers
```

## 🔄 Execution and Scheduling Concepts

### 1. Task Lifecycle

**Task States Flow**:
```
┌─────────────────────────────────────────────────────────────┐
│                    Task Lifecycle                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐                                           │
│  │   Queued    │ ←── Task is waiting to be picked up       │
│  └─────────────┘                                           │
│         │                                                  │
│         ▼                                                  │
│  ┌─────────────┐                                           │
│  │   Running   │ ←── Task is currently executing           │
│  └─────────────┘                                           │
│         │                                                  │
│    ┌────┴────┐                                             │
│    ▼         ▼                                             │
│ ┌─────────┐ ┌─────────┐                                    │
│ │Success  │ │ Failed  │                                    │
│ └─────────┘ └─────────┘                                    │
│                 │                                          │
│                 ▼                                          │
│          ┌─────────────┐                                   │
│          │   Retry     │ ←── If retries configured         │
│          └─────────────┘                                   │
│                 │                                          │
│                 └─────────────┐                            │
│                               ▼                            │
│                        ┌─────────────┐                     │
│                        │ Up for Retry│                     │
│                        └─────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

### 2. Scheduling Concepts

**Execution Date vs Run Date**:
- **Execution Date**: The logical date the DAG is processing data for
- **Run Date**: When the DAG actually runs

**Example**: A daily DAG with execution_date 2024-01-01 might run on 2024-01-02 at 2 AM

**Backfilling**: Running historical DAG instances
```bash
# Run DAG for specific date range
airflow dags backfill -s 2024-01-01 -e 2024-01-31 customer_analytics_pipeline
```

## 🎯 Advanced Concepts

### 1. XComs (Cross-Communication)

**Sharing data between tasks**:
```python
def extract_data():
    data = {"customer_count": 1000, "total_revenue": 50000}
    return data  # Automatically pushed to XCom

def process_data(**context):
    # Pull data from previous task
    data = context['task_instance'].xcom_pull(task_ids='extract_data')
    customer_count = data['customer_count']
    # Process the data...

extract = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag
)

process = PythonOperator(
    task_id='process_data',
    python_callable=process_data,
    dag=dag
)

extract >> process
```

### 2. Sensors

**Waiting for external conditions**:
```python
from airflow.sensors.filesystem import FileSensor

# Wait for file to appear
file_sensor = FileSensor(
    task_id='wait_for_file',
    filepath='/data/input/customers.csv',
    poke_interval=60,  # Check every 60 seconds
    timeout=3600,  # Give up after 1 hour
    dag=dag
)
```

### 3. Branching

**Conditional task execution**:
```python
from airflow.operators.python import BranchPythonOperator

def choose_branch(**context):
    # Business logic to decide which path to take
    if context['ds'] == '2024-01-01':  # execution_date
        return 'special_processing'
    else:
        return 'normal_processing'

branch_task = BranchPythonOperator(
    task_id='choose_processing_type',
    python_callable=choose_branch,
    dag=dag
)

normal_task = PythonOperator(
    task_id='normal_processing',
    python_callable=normal_processing_function,
    dag=dag
)

special_task = PythonOperator(
    task_id='special_processing',
    python_callable=special_processing_function,
    dag=dag
)

branch_task >> [normal_task, special_task]
```

## 🚀 When to Use Airflow

### ✅ Ideal Use Cases:

**1. Complex ETL Pipelines**:
- Multi-step data transformations
- Dependencies between different data sources
- Need for retry logic and error handling

**2. Batch Processing Workflows**:
- Daily/weekly/monthly data processing
- Report generation pipelines
- Data warehouse loading

**3. Machine Learning Pipelines**:
- Model training workflows
- Feature engineering pipelines
- Model deployment automation

**4. Data Quality Monitoring**:
- Automated data validation
- Anomaly detection workflows
- Data lineage tracking

### ❌ Not Ideal For:

**1. Real-time Processing**: Use streaming platforms like Kafka
**2. Simple Cron Jobs**: Basic scheduling might be overkill
**3. Event-driven Workflows**: Better suited for event-based systems
**4. High-frequency Tasks**: Sub-minute scheduling not recommended

## 🎯 Real-World Analogy

Think of Airflow like a **smart factory assembly line manager**:

- **DAG**: The blueprint showing how products move through stations
- **Tasks**: Individual workstations (welding, painting, assembly)
- **Dependencies**: "Painting can't start until welding is complete"
- **Scheduler**: Factory supervisor deciding when to start each station
- **Workers**: The actual people/machines doing the work
- **Monitoring**: Quality control checking each step
- **Retries**: "If painting fails, clean and try again"

Just like a factory manager ensures products flow smoothly through the assembly line, Airflow ensures your data flows smoothly through your processing pipeline, handling failures and dependencies automatically.

## 📊 Performance and Scaling

### Scaling Patterns:
- **Vertical**: Increase resources on single machine
- **Horizontal**: Add more worker nodes
- **Executor Choice**: Local → Celery → Kubernetes

### Resource Considerations:
- **Scheduler**: CPU-intensive for large numbers of DAGs
- **Database**: I/O intensive, needs good storage
- **Workers**: Memory and CPU based on task requirements

### Best Practices:
- Keep DAGs simple and focused
- Use appropriate task granularity
- Monitor resource usage and bottlenecks
- Implement proper logging and alerting

This conceptual understanding helps you design robust, maintainable data pipelines using Airflow effectively.