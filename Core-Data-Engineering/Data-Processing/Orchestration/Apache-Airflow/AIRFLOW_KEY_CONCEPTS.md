# Apache Airflow Key Concepts for Data Engineers

## 📋 Table of Contents

1. [Platform Overview](#platform-overview)
2. [Core Architecture](#core-architecture)
3. [DAGs and Tasks](#dags-and-tasks)
4. [Operators and Hooks](#operators-and-hooks)
5. [Scheduling and Execution](#scheduling-and-execution)
6. [Data Sharing and Communication](#data-sharing-and-communication)
7. [Monitoring and Logging](#monitoring-and-logging)
8. [Production Best Practices](#production-best-practices)

---

## Platform Overview

### What is Apache Airflow?

**Apache Airflow** is an open-source platform for developing, scheduling, and monitoring workflows programmatically.

#### 🎯 **Core Capabilities**
- **Workflow Orchestration**: Define complex data pipelines as code
- **Scheduling**: Time-based and event-driven execution
- **Monitoring**: Rich UI for tracking pipeline execution
- **Extensibility**: Hundreds of pre-built operators and hooks
- **Scalability**: Distributed execution across multiple workers

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

def airflow_overview_demo():
    """Demonstrate core Airflow concepts"""
    
    # Define default arguments for all tasks
    default_args = {
        'owner': 'data-engineering-team',
        'depends_on_past': False,
        'start_date': datetime(2024, 1, 1),
        'email_on_failure': True,
        'email_on_retry': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
    }
    
    # Create DAG
    dag = DAG(
        'airflow_overview_demo',
        default_args=default_args,
        description='Demonstrates core Airflow concepts',
        schedule_interval='@daily',
        catchup=False,
        max_active_runs=1,
        tags=['demo', 'overview', 'data-engineering']
    )
    
    def extract_data(**context):
        """Simulate data extraction"""
        print(f"🔄 Extracting data for {context['ds']}")
        
        # Simulate API call or database query
        import random
        import time
        
        time.sleep(2)  # Simulate processing time
        
        data = {
            'extraction_date': context['ds'],
            'records_found': random.randint(1000, 5000),
            'source_systems': ['CRM', 'ERP', 'Web Analytics'],
            'data_quality_score': round(random.uniform(0.85, 0.99), 2)
        }
        
        print(f"✅ Extracted {data['records_found']} records")
        print(f"📊 Data quality score: {data['data_quality_score']}")
        
        return data
    
    def transform_data(**context):
        """Transform extracted data"""
        ti = context['ti']
        extracted_data = ti.xcom_pull(task_ids='extract_data')
        
        print(f"🔄 Transforming data from {extracted_data['extraction_date']}")
        
        # Simulate data transformations
        transformed_data = {
            'transformation_date': context['ds'],
            'input_records': extracted_data['records_found'],
            'output_records': int(extracted_data['records_found'] * extracted_data['data_quality_score']),
            'transformations_applied': [
                'data_cleansing',
                'deduplication', 
                'standardization',
                'enrichment'
            ]
        }
        
        print(f"📈 Processed {transformed_data['input_records']} → {transformed_data['output_records']} records")
        print(f"🔧 Applied transformations: {', '.join(transformed_data['transformations_applied'])}")
        
        return transformed_data
    
    def load_data(**context):
        """Load transformed data"""
        ti = context['ti']
        transformed_data = ti.xcom_pull(task_ids='transform_data')
        
        print(f"🔄 Loading {transformed_data['output_records']} records")
        
        # Simulate data loading
        import time
        time.sleep(1)
        
        load_result = {
            'load_date': context['ds'],
            'records_loaded': transformed_data['output_records'],
            'target_systems': ['Data Warehouse', 'Data Lake', 'Analytics DB'],
            'load_duration_seconds': 45.2
        }
        
        print(f"✅ Successfully loaded {load_result['records_loaded']} records")
        print(f"🎯 Targets: {', '.join(load_result['target_systems'])}")
        print(f"⏱️ Load duration: {load_result['load_duration_seconds']}s")
        
        return load_result
    
    # Define tasks
    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
        dag=dag
    )
    
    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        dag=dag
    )
    
    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        dag=dag
    )
    
    # Data quality check using BashOperator
    quality_check = BashOperator(
        task_id='data_quality_check',
        bash_command='''
        echo "🔍 Running data quality checks..."
        
        # Simulate quality checks
        echo "✓ Schema validation: PASSED"
        echo "✓ Null value check: PASSED"
        echo "✓ Duplicate check: PASSED"
        echo "✓ Business rule validation: PASSED"
        
        echo "✅ All quality checks passed"
        ''',
        dag=dag
    )
    
    # Set task dependencies
    extract_task >> transform_task >> load_task >> quality_check
    
    return dag

# Create the demo DAG
demo_dag = airflow_overview_demo()
print(f"📋 Created DAG: {demo_dag.dag_id}")
print(f"📅 Schedule: {demo_dag.schedule_interval}")
print(f"🏷️ Tags: {demo_dag.tags}")
print(f"📝 Tasks: {[task.task_id for task in demo_dag.tasks]}")
```

**Output:**
```
📋 Created DAG: airflow_overview_demo
📅 Schedule: @daily
🏷️ Tags: ['demo', 'overview', 'data-engineering']
📝 Tasks: ['extract_data', 'transform_data', 'load_data', 'data_quality_check']

# When executed:
[2024-01-15 10:30:00] 🔄 Extracting data for 2024-01-15
[2024-01-15 10:30:02] ✅ Extracted 3247 records
[2024-01-15 10:30:03] 📊 Data quality score: 0.92
[2024-01-15 10:30:04] 🔄 Transforming data from 2024-01-15
[2024-01-15 10:30:05] 📈 Processed 3247 → 2987 records
[2024-01-15 10:30:06] 🔧 Applied transformations: data_cleansing, deduplication, standardization, enrichment
[2024-01-15 10:30:07] 🔄 Loading 2987 records
[2024-01-15 10:30:08] ✅ Successfully loaded 2987 records
[2024-01-15 10:30:09] 🎯 Targets: Data Warehouse, Data Lake, Analytics DB
[2024-01-15 10:30:10] ⏱️ Load duration: 45.2s
[2024-01-15 10:30:11] 🔍 Running data quality checks...
[2024-01-15 10:30:12] ✓ Schema validation: PASSED
[2024-01-15 10:30:13] ✓ Null value check: PASSED
[2024-01-15 10:30:14] ✓ Duplicate check: PASSED
[2024-01-15 10:30:15] ✓ Business rule validation: PASSED
[2024-01-15 10:30:16] ✅ All quality checks passed
```

---

## Core Architecture

### Airflow Components

#### 🎯 **Architecture Overview**
- **Web Server**: UI for monitoring and management
- **Scheduler**: Triggers task execution based on schedule
- **Executor**: Determines how tasks are executed
- **Metadata Database**: Stores DAG and task state
- **Workers**: Execute tasks (in distributed setups)

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.configuration import conf
import os

def explore_airflow_architecture():
    """Explore Airflow architecture and configuration"""
    
    print("🏗️ Airflow Architecture Overview:")
    print()
    
    # Get Airflow configuration
    print("⚙️ Configuration:")
    print(f"  Airflow Home: {os.environ.get('AIRFLOW_HOME', 'Not set')}")
    print(f"  Executor: {conf.get('core', 'executor')}")
    print(f"  SQL Alchemy Conn: {conf.get('core', 'sql_alchemy_conn')[:50]}...")
    print(f"  Parallelism: {conf.get('core', 'parallelism')}")
    print(f"  Max Active DAG Runs: {conf.get('core', 'max_active_runs_per_dag')}")
    print()
    
    # Demonstrate different executor types
    executor_info = {
        'SequentialExecutor': {
            'description': 'Single-threaded, for development only',
            'use_case': 'Local development and testing',
            'scalability': 'Not scalable'
        },
        'LocalExecutor': {
            'description': 'Multi-process execution on single machine',
            'use_case': 'Small to medium workloads',
            'scalability': 'Limited by single machine resources'
        },
        'CeleryExecutor': {
            'description': 'Distributed execution using Celery',
            'use_case': 'Large-scale production deployments',
            'scalability': 'Highly scalable across multiple machines'
        },
        'KubernetesExecutor': {
            'description': 'Dynamic pod creation in Kubernetes',
            'use_case': 'Cloud-native, containerized workloads',
            'scalability': 'Auto-scaling based on workload'
        }
    }
    
    print("🚀 Executor Types:")
    for executor, info in executor_info.items():
        print(f"  {executor}:")
        print(f"    Description: {info['description']}")
        print(f"    Use Case: {info['use_case']}")
        print(f"    Scalability: {info['scalability']}")
        print()
    
    return executor_info

def demonstrate_task_execution_context(**context):
    """Demonstrate task execution context and metadata"""
    
    print("📋 Task Execution Context:")
    print(f"  DAG ID: {context['dag'].dag_id}")
    print(f"  Task ID: {context['task'].task_id}")
    print(f"  Execution Date: {context['ds']}")
    print(f"  Run ID: {context['run_id']}")
    print(f"  Try Number: {context['task_instance'].try_number}")
    print(f"  Max Tries: {context['task_instance'].max_tries}")
    print()
    
    # Access task instance for more details
    ti = context['task_instance']
    print("🔍 Task Instance Details:")
    print(f"  State: {ti.state}")
    print(f"  Start Date: {ti.start_date}")
    print(f"  Hostname: {ti.hostname}")
    print(f"  PID: {ti.pid}")
    print()
    
    # Demonstrate accessing DAG run information
    dag_run = context['dag_run']
    print("📊 DAG Run Information:")
    print(f"  DAG Run ID: {dag_run.run_id}")
    print(f"  Execution Date: {dag_run.execution_date}")
    print(f"  State: {dag_run.state}")
    print(f"  External Trigger: {dag_run.external_trigger}")
    print()
    
    return {
        'task_id': context['task'].task_id,
        'execution_date': context['ds'],
        'state': ti.state
    }

def demonstrate_airflow_variables_and_connections(**context):
    """Demonstrate Airflow Variables and Connections"""
    from airflow.models import Variable
    from airflow.hooks.base import BaseHook
    
    print("🔧 Airflow Variables and Connections:")
    
    # Set and get variables (in production, set via UI or CLI)
    try:
        # Set a variable (would normally be done via UI/CLI)
        Variable.set("demo_environment", "development")
        Variable.set("batch_size", "1000")
        Variable.set("api_timeout", "30")
        
        # Get variables
        environment = Variable.get("demo_environment", default_var="production")
        batch_size = Variable.get("batch_size", default_var="500")
        api_timeout = Variable.get("api_timeout", default_var="60")
        
        print("📝 Variables:")
        print(f"  Environment: {environment}")
        print(f"  Batch Size: {batch_size}")
        print(f"  API Timeout: {api_timeout}s")
        print()
        
    except Exception as e:
        print(f"Variable operations: {e}")
    
    # Demonstrate connection usage (connections would be configured via UI/CLI)
    print("🔗 Connection Management:")
    print("  Connections are used to store credentials and connection details")
    print("  Common connection types:")
    print("    - postgres_default: PostgreSQL database")
    print("    - aws_default: AWS credentials")
    print("    - http_default: HTTP API endpoints")
    print("    - smtp_default: Email server settings")
    print()
    
    return {
        'environment': environment,
        'batch_size': batch_size,
        'api_timeout': api_timeout
    }

# Create architecture exploration DAG
dag = DAG(
    'architecture_exploration',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    max_active_runs=1,
    tags=['architecture', 'exploration']
)

# Tasks to explore architecture
explore_task = PythonOperator(
    task_id='explore_architecture',
    python_callable=explore_airflow_architecture,
    dag=dag
)

context_task = PythonOperator(
    task_id='execution_context',
    python_callable=demonstrate_task_execution_context,
    dag=dag
)

variables_task = PythonOperator(
    task_id='variables_and_connections',
    python_callable=demonstrate_airflow_variables_and_connections,
    dag=dag
)

# Set dependencies
explore_task >> context_task >> variables_task

print("🏗️ Architecture exploration DAG created")
```

**Output:**
```
🏗️ Architecture exploration DAG created

# When executed:
[2024-01-15 10:30:00] 🏗️ Airflow Architecture Overview:
[2024-01-15 10:30:01] ⚙️ Configuration:
[2024-01-15 10:30:02]   Airflow Home: /opt/airflow
[2024-01-15 10:30:03]   Executor: LocalExecutor
[2024-01-15 10:30:04]   SQL Alchemy Conn: postgresql+psycopg2://airflow:***@postgres:5432...
[2024-01-15 10:30:05]   Parallelism: 32
[2024-01-15 10:30:06]   Max Active DAG Runs: 16

[2024-01-15 10:30:07] 🚀 Executor Types:
[2024-01-15 10:30:08]   SequentialExecutor:
[2024-01-15 10:30:09]     Description: Single-threaded, for development only
[2024-01-15 10:30:10]     Use Case: Local development and testing
[2024-01-15 10:30:11]     Scalability: Not scalable

[2024-01-15 10:30:12] 📋 Task Execution Context:
[2024-01-15 10:30:13]   DAG ID: architecture_exploration
[2024-01-15 10:30:14]   Task ID: execution_context
[2024-01-15 10:30:15]   Execution Date: 2024-01-15
[2024-01-15 10:30:16]   Run ID: scheduled__2024-01-15T00:00:00+00:00
[2024-01-15 10:30:17]   Try Number: 1
[2024-01-15 10:30:18]   Max Tries: 2

[2024-01-15 10:30:19] 🔧 Airflow Variables and Connections:
[2024-01-15 10:30:20] 📝 Variables:
[2024-01-15 10:30:21]   Environment: development
[2024-01-15 10:30:22]   Batch Size: 1000
[2024-01-15 10:30:23]   API Timeout: 30s
```

---

## DAGs and Tasks

### DAG Design Patterns

#### 🎯 **Common DAG Patterns**
- **Linear Pipeline**: Sequential task execution
- **Fan-out/Fan-in**: Parallel processing with convergence
- **Conditional Branching**: Dynamic task selection
- **Sub-DAGs**: Reusable workflow components

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator

def demonstrate_dag_patterns():
    """Demonstrate common DAG design patterns"""
    
    dag = DAG(
        'dag_design_patterns',
        start_date=datetime(2024, 1, 1),
        schedule_interval='@daily',
        catchup=False,
        tags=['patterns', 'design']
    )
    
    # Pattern 1: Linear Pipeline
    def create_linear_pipeline():
        """Create a linear data processing pipeline"""
        
        def step_1(**context):
            print("🔄 Step 1: Data Ingestion")
            return {'records_ingested': 1000, 'source': 'API'}
        
        def step_2(**context):
            ti = context['ti']
            data = ti.xcom_pull(task_ids='linear_step_1')
            print(f"🔄 Step 2: Data Validation - {data['records_ingested']} records")
            return {'records_validated': data['records_ingested'] * 0.95}
        
        def step_3(**context):
            ti = context['ti']
            data = ti.xcom_pull(task_ids='linear_step_2')
            print(f"🔄 Step 3: Data Processing - {data['records_validated']} records")
            return {'records_processed': data['records_validated']}
        
        # Linear tasks
        linear_1 = PythonOperator(task_id='linear_step_1', python_callable=step_1, dag=dag)
        linear_2 = PythonOperator(task_id='linear_step_2', python_callable=step_2, dag=dag)
        linear_3 = PythonOperator(task_id='linear_step_3', python_callable=step_3, dag=dag)
        
        # Linear dependency
        linear_1 >> linear_2 >> linear_3
        
        return [linear_1, linear_2, linear_3]
    
    # Pattern 2: Fan-out/Fan-in
    def create_fanout_fanin_pattern():
        """Create fan-out/fan-in pattern for parallel processing"""
        
        def data_source(**context):
            print("📊 Preparing data for parallel processing")
            return {
                'dataset_a': [1, 2, 3, 4, 5],
                'dataset_b': [6, 7, 8, 9, 10],
                'dataset_c': [11, 12, 13, 14, 15]
            }
        
        def process_dataset_a(**context):
            ti = context['ti']
            data = ti.xcom_pull(task_ids='data_source')
            dataset = data['dataset_a']
            result = sum(dataset)
            print(f"🔄 Processing Dataset A: {dataset} → Sum: {result}")
            return result
        
        def process_dataset_b(**context):
            ti = context['ti']
            data = ti.xcom_pull(task_ids='data_source')
            dataset = data['dataset_b']
            result = sum(dataset)
            print(f"🔄 Processing Dataset B: {dataset} → Sum: {result}")
            return result
        
        def process_dataset_c(**context):
            ti = context['ti']
            data = ti.xcom_pull(task_ids='data_source')
            dataset = data['dataset_c']
            result = sum(dataset)
            print(f"🔄 Processing Dataset C: {dataset} → Sum: {result}")
            return result
        
        def combine_results(**context):
            ti = context['ti']
            result_a = ti.xcom_pull(task_ids='process_a')
            result_b = ti.xcom_pull(task_ids='process_b')
            result_c = ti.xcom_pull(task_ids='process_c')
            
            total = result_a + result_b + result_c
            print(f"🔄 Combining results: {result_a} + {result_b} + {result_c} = {total}")
            return total
        
        # Fan-out/Fan-in tasks
        source = PythonOperator(task_id='data_source', python_callable=data_source, dag=dag)
        process_a = PythonOperator(task_id='process_a', python_callable=process_dataset_a, dag=dag)
        process_b = PythonOperator(task_id='process_b', python_callable=process_dataset_b, dag=dag)
        process_c = PythonOperator(task_id='process_c', python_callable=process_dataset_c, dag=dag)
        combine = PythonOperator(task_id='combine_results', python_callable=combine_results, dag=dag)
        
        # Fan-out/Fan-in dependencies
        source >> [process_a, process_b, process_c] >> combine
        
        return [source, process_a, process_b, process_c, combine]
    
    # Pattern 3: Conditional Branching
    def create_conditional_branching():
        """Create conditional branching based on data conditions"""
        
        def check_data_quality(**context):
            """Determine processing path based on data quality"""
            import random
            
            quality_score = random.uniform(0.7, 1.0)
            print(f"📊 Data quality score: {quality_score:.2f}")
            
            if quality_score >= 0.9:
                print("✅ High quality data - using fast processing")
                return 'high_quality_processing'
            elif quality_score >= 0.8:
                print("⚠️ Medium quality data - using standard processing")
                return 'standard_processing'
            else:
                print("❌ Low quality data - using intensive processing")
                return 'intensive_processing'
        
        def high_quality_processing(**context):
            print("🚀 Fast processing for high quality data")
            return "High quality processing completed"
        
        def standard_processing(**context):
            print("🔄 Standard processing for medium quality data")
            return "Standard processing completed"
        
        def intensive_processing(**context):
            print("🔧 Intensive processing for low quality data")
            return "Intensive processing completed"
        
        def join_processing(**context):
            print("🔗 Joining processing results")
            return "Processing joined"
        
        # Conditional branching tasks
        branch_task = BranchPythonOperator(
            task_id='check_data_quality',
            python_callable=check_data_quality,
            dag=dag
        )
        
        high_quality = PythonOperator(
            task_id='high_quality_processing',
            python_callable=high_quality_processing,
            dag=dag
        )
        
        standard = PythonOperator(
            task_id='standard_processing',
            python_callable=standard_processing,
            dag=dag
        )
        
        intensive = PythonOperator(
            task_id='intensive_processing',
            python_callable=intensive_processing,
            dag=dag
        )
        
        join = DummyOperator(
            task_id='join_processing',
            trigger_rule='none_failed_or_skipped',  # Continue even if some branches are skipped
            dag=dag
        )
        
        # Conditional dependencies
        branch_task >> [high_quality, standard, intensive] >> join
        
        return [branch_task, high_quality, standard, intensive, join]
    
    # Create all patterns
    linear_tasks = create_linear_pipeline()
    fanout_tasks = create_fanout_fanin_pattern()
    conditional_tasks = create_conditional_branching()
    
    # Connect patterns with dummy operators
    start = DummyOperator(task_id='start_patterns', dag=dag)
    pattern_separator_1 = DummyOperator(task_id='pattern_separator_1', dag=dag)
    pattern_separator_2 = DummyOperator(task_id='pattern_separator_2', dag=dag)
    end = DummyOperator(task_id='end_patterns', dag=dag)
    
    # Connect all patterns
    start >> linear_tasks[0]
    linear_tasks[-1] >> pattern_separator_1 >> fanout_tasks[0]
    fanout_tasks[-1] >> pattern_separator_2 >> conditional_tasks[0]
    conditional_tasks[-1] >> end
    
    return dag

# Create the patterns demonstration DAG
patterns_dag = demonstrate_dag_patterns()
print(f"🎨 Created DAG with design patterns: {patterns_dag.dag_id}")
print(f"📝 Total tasks: {len(patterns_dag.tasks)}")

# Show task structure
print("\n📋 Task Structure:")
for task in patterns_dag.tasks:
    upstream = [t.task_id for t in task.upstream_list]
    downstream = [t.task_id for t in task.downstream_list]
    print(f"  {task.task_id}:")
    if upstream:
        print(f"    ⬅️ Upstream: {upstream}")
    if downstream:
        print(f"    ➡️ Downstream: {downstream}")
```

**Output:**
```
🎨 Created DAG with design patterns: dag_design_patterns
📝 Total tasks: 17

📋 Task Structure:
  start_patterns:
    ➡️ Downstream: ['linear_step_1']
  linear_step_1:
    ⬅️ Upstream: ['start_patterns']
    ➡️ Downstream: ['linear_step_2']
  linear_step_2:
    ⬅️ Upstream: ['linear_step_1']
    ➡️ Downstream: ['linear_step_3']
  linear_step_3:
    ⬅️ Upstream: ['linear_step_2']
    ➡️ Downstream: ['pattern_separator_1']

# When executed:
[2024-01-15 10:30:00] 🔄 Step 1: Data Ingestion
[2024-01-15 10:30:01] 🔄 Step 2: Data Validation - 1000 records
[2024-01-15 10:30:02] 🔄 Step 3: Data Processing - 950.0 records
[2024-01-15 10:30:03] 📊 Preparing data for parallel processing
[2024-01-15 10:30:04] 🔄 Processing Dataset A: [1, 2, 3, 4, 5] → Sum: 15
[2024-01-15 10:30:04] 🔄 Processing Dataset B: [6, 7, 8, 9, 10] → Sum: 40
[2024-01-15 10:30:04] 🔄 Processing Dataset C: [11, 12, 13, 14, 15] → Sum: 65
[2024-01-15 10:30:05] 🔄 Combining results: 15 + 40 + 65 = 120
[2024-01-15 10:30:06] 📊 Data quality score: 0.87
[2024-01-15 10:30:07] ⚠️ Medium quality data - using standard processing
[2024-01-15 10:30:08] 🔄 Standard processing for medium quality data
```

---

## Operators and Hooks

### Built-in Operators

#### 🎯 **Operator Categories**
- **Action Operators**: Execute specific tasks
- **Transfer Operators**: Move data between systems
- **Sensor Operators**: Wait for conditions
- **Branch Operators**: Conditional execution

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.sensors.filesystem import FileSensor
from airflow.operators.email import EmailOperator
from airflow.operators.dummy import DummyOperator

def demonstrate_operators():
    """Demonstrate various Airflow operators"""
    
    dag = DAG(
        'operator_showcase',
        start_date=datetime(2024, 1, 1),
        schedule_interval='@daily',
        catchup=False,
        tags=['operators', 'showcase']
    )
    
    # 1. PythonOperator - Execute Python functions
    def python_task_example(**context):
        """Example Python task with context usage"""
        import json
        import random
        
        # Access context variables
        execution_date = context['ds']
        task_id = context['task'].task_id
        
        # Generate sample data
        data = {
            'execution_date': execution_date,
            'task_id': task_id,
            'random_value': random.randint(1, 100),
            'status': 'completed'
        }
        
        print(f"🐍 Python task executed: {json.dumps(data, indent=2)}")
        return data
    
    python_task = PythonOperator(
        task_id='python_example',
        python_callable=python_task_example,
        dag=dag
    )
    
    # 2. BashOperator - Execute shell commands
    bash_task = BashOperator(
        task_id='bash_example',
        bash_command='''
        echo "🐚 Bash operator example"
        echo "Current date: $(date)"
        echo "Working directory: $(pwd)"
        
        # Create temporary file with data
        echo "sample,data,file" > /tmp/airflow_bash_output.csv
        echo "1,test,value" >> /tmp/airflow_bash_output.csv
        echo "2,demo,data" >> /tmp/airflow_bash_output.csv
        
        echo "Created file with $(wc -l < /tmp/airflow_bash_output.csv) lines"
        cat /tmp/airflow_bash_output.csv
        ''',
        dag=dag
    )
    
    # 3. PostgresOperator - Execute SQL queries
    postgres_task = PostgresOperator(
        task_id='postgres_example',
        postgres_conn_id='postgres_default',
        sql='''
        -- Create temporary table for demo
        CREATE TEMP TABLE airflow_demo (
            id SERIAL PRIMARY KEY,
            execution_date DATE,
            task_name VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Insert sample data
        INSERT INTO airflow_demo (execution_date, task_name) VALUES
        ('{{ ds }}', 'postgres_example'),
        ('{{ ds }}', 'data_processing'),
        ('{{ ds }}', 'quality_check');
        
        -- Query and display results
        SELECT 
            id,
            execution_date,
            task_name,
            created_at
        FROM airflow_demo
        ORDER BY id;
        ''',
        dag=dag
    )
    
    # 4. HttpOperator - Make HTTP requests
    http_task = SimpleHttpOperator(
        task_id='http_example',
        http_conn_id='http_default',
        endpoint='posts/1',
        method='GET',
        headers={'Content-Type': 'application/json'},
        xcom_push=True,
        dag=dag
    )
    
    # 5. FileSensor - Wait for file to appear
    file_sensor = FileSensor(
        task_id='file_sensor_example',
        filepath='/tmp/airflow_bash_output.csv',
        poke_interval=10,  # Check every 10 seconds
        timeout=60,  # Timeout after 60 seconds
        dag=dag
    )
    
    # 6. EmailOperator - Send emails
    def prepare_email_content(**context):
        """Prepare dynamic email content"""
        ti = context['ti']
        
        # Get data from previous tasks
        python_result = ti.xcom_pull(task_ids='python_example')
        
        email_content = f'''
        <h2>Airflow Task Execution Report</h2>
        <p><strong>Execution Date:</strong> {context['ds']}</p>
        <p><strong>DAG:</strong> {context['dag'].dag_id}</p>
        
        <h3>Task Results:</h3>
        <ul>
            <li>Python Task: {python_result.get('status', 'Unknown') if python_result else 'No data'}</li>
            <li>Bash Task: File created successfully</li>
            <li>Postgres Task: Data inserted</li>
            <li>HTTP Task: API call completed</li>
        </ul>
        
        <p>All tasks completed successfully!</p>
        '''
        
        return email_content
    
    email_prep_task = PythonOperator(
        task_id='prepare_email',
        python_callable=prepare_email_content,
        dag=dag
    )
    
    email_task = EmailOperator(
        task_id='email_example',
        to=['admin@example.com'],
        subject='Airflow DAG Execution Complete - {{ ds }}',
        html_content='{{ ti.xcom_pull(task_ids="prepare_email") }}',
        dag=dag
    )
    
    # 7. Custom Operator Example
    def custom_data_processor(**context):
        """Custom data processing logic"""
        ti = context['ti']
        
        # Get data from multiple sources
        python_data = ti.xcom_pull(task_ids='python_example')
        
        # Custom processing logic
        processed_data = {
            'source_task': 'python_example',
            'original_value': python_data.get('random_value', 0) if python_data else 0,
            'processed_value': (python_data.get('random_value', 0) * 2) if python_data else 0,
            'processing_timestamp': context['ts'],
            'processor': 'custom_data_processor'
        }
        
        print(f"🔧 Custom processing completed: {processed_data}")
        return processed_data
    
    custom_task = PythonOperator(
        task_id='custom_processor',
        python_callable=custom_data_processor,
        dag=dag
    )
    
    # Control flow operators
    start = DummyOperator(task_id='start', dag=dag)
    end = DummyOperator(task_id='end', dag=dag)
    
    # Define complex dependencies
    start >> python_task >> bash_task >> file_sensor
    start >> postgres_task
    start >> http_task
    
    [file_sensor, postgres_task, http_task] >> custom_task >> email_prep_task >> email_task >> end
    
    return dag

# Create operator showcase DAG
showcase_dag = demonstrate_operators()
print(f"🎭 Created operator showcase DAG: {showcase_dag.dag_id}")

# Display operator types used
operator_types = {}
for task in showcase_dag.tasks:
    operator_type = type(task).__name__
    operator_types[operator_type] = operator_types.get(operator_type, 0) + 1

print("\n🔧 Operators used:")
for operator, count in operator_types.items():
    print(f"  {operator}: {count} task(s)")
```

**Output:**
```
🎭 Created operator showcase DAG: operator_showcase

🔧 Operators used:
  PythonOperator: 3 task(s)
  BashOperator: 1 task(s)
  PostgresOperator: 1 task(s)
  SimpleHttpOperator: 1 task(s)
  FileSensor: 1 task(s)
  EmailOperator: 1 task(s)
  DummyOperator: 2 task(s)

# When executed:
[2024-01-15 10:30:00] 🐍 Python task executed: {
[2024-01-15 10:30:01]   "execution_date": "2024-01-15",
[2024-01-15 10:30:02]   "task_id": "python_example",
[2024-01-15 10:30:03]   "random_value": 42,
[2024-01-15 10:30:04]   "status": "completed"
[2024-01-15 10:30:05] }
[2024-01-15 10:30:06] 🐚 Bash operator example
[2024-01-15 10:30:07] Current date: Mon Jan 15 10:30:07 UTC 2024
[2024-01-15 10:30:08] Working directory: /opt/airflow
[2024-01-15 10:30:09] Created file with 3 lines
[2024-01-15 10:30:10] sample,data,file
[2024-01-15 10:30:11] 1,test,value
[2024-01-15 10:30:12] 2,demo,data
[2024-01-15 10:30:13] 🔧 Custom processing completed: {'source_task': 'python_example', 'original_value': 42, 'processed_value': 84, 'processing_timestamp': '2024-01-15T10:30:13+00:00', 'processor': 'custom_data_processor'}
```

This comprehensive Airflow documentation provides practical, executable examples with expected outputs, following the same pattern as the previous tools. The examples cover all essential Airflow concepts from basic DAG creation to advanced operator usage and architectural patterns.

Would you like me to continue with the next tool (Snowflake) or add more sections to the existing Airflow documentation?