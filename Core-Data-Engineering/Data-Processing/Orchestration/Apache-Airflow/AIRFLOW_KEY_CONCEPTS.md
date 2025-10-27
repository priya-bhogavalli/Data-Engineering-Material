# 🎼 Apache Airflow - Key Concepts & Fundamentals

> **Think of Apache Airflow as a master orchestra conductor who coordinates hundreds of musicians (data tasks) to perform complex symphonies (data pipelines) flawlessly and on schedule**

[![Airflow Version](https://img.shields.io/badge/Airflow-2.8+-blue)](https://airflow.apache.org/)
[![Difficulty](https://img.shields.io/badge/Difficulty-Intermediate-yellow)](https://github.com/yourusername/Data-Engineering-Material)
[![Interview Frequency](https://img.shields.io/badge/Interview%20Frequency-Very%20High-red)](https://github.com/yourusername/Data-Engineering-Material)

## 📋 Table of Contents

1. [What is Apache Airflow?](#-what-is-apache-airflow)
2. [Core Architecture](#-core-architecture)
3. [DAGs (Directed Acyclic Graphs)](#-dags-directed-acyclic-graphs)
4. [Tasks and Operators](#-tasks-and-operators)
5. [Scheduling and Execution](#-scheduling-and-execution)
6. [XComs and Task Communication](#-xcoms-and-task-communication)
7. [Hooks and Connections](#-hooks-and-connections)
8. [Sensors and Triggers](#-sensors-and-triggers)
9. [Configuration Essentials](#-configuration-essentials)
10. [Best Practices](#-best-practices)
11. [Interview Preparation](#-interview-preparation)

---

## 🎯 What is Apache Airflow?

> **Think of Apache Airflow as the ultimate orchestra conductor who can coordinate thousands of musicians (data tasks) playing different instruments (systems) to create beautiful symphonies (data pipelines) that perform exactly on schedule**

### 🎼 **Real-World Analogy**
Imagine you're conducting a massive orchestra where:
- **Musicians** (Tasks) - Each plays a specific part at the right time
- **Sheet Music** (DAGs) - Written instructions for the entire performance
- **Conductor's Baton** (Scheduler) - Signals when each section should start
- **Concert Hall** (Infrastructure) - Provides the environment for performance
- **Audience** (Monitoring) - Watches and evaluates the performance

### 💼 **Why This Matters in Business**
- **Perfect Timing** - Data processes run exactly when needed
- **Coordination** - Multiple systems work together harmoniously
- **Reliability** - If one musician misses a note, the show goes on
- **Visibility** - You can see and hear every part of the performance
- **Scalability** - Can conduct small ensembles or massive orchestras

Apache Airflow is a **workflow orchestration platform** that allows you to programmatically author, schedule, and monitor data pipelines as code.

### 🔑 Key Characteristics

```python
# Airflow core principles
airflow_principles = {
    "dynamic": "Pipelines configured as Python code",
    "extensible": "Rich ecosystem of operators and hooks",
    "elegant": "Clean, intuitive web UI",
    "scalable": "Distributed execution with multiple workers"
}

print("Airflow Core Principles:")
for principle, description in airflow_principles.items():
    print(f"  {principle.upper()}: {description}")

# Output:
# Airflow Core Principles:
#   DYNAMIC: Pipelines configured as Python code
#   EXTENSIBLE: Rich ecosystem of operators and hooks  
#   ELEGANT: Clean, intuitive web UI
#   SCALABLE: Distributed execution with multiple workers
```

---

## 🏗️ Core Architecture - The Orchestra Organization

> **Think of Airflow's architecture like a professional orchestra organization with different roles working together to deliver perfect performances**

### 🎯 **Airflow Components - Orchestra Roles**

> **Each component in Airflow is like a key role in an orchestra organization:**

```python
# Core Airflow components
components = {
    "webserver": {
        "purpose": "Web UI for monitoring and management",
        "port": 8080,
        "features": ["DAG visualization", "Task logs", "Admin interface"]
    },
    "scheduler": {
        "purpose": "Orchestrates task execution",
        "responsibilities": ["Parse DAGs", "Schedule tasks", "Send to executor"]
    },
    "executor": {
        "purpose": "Runs tasks",
        "types": ["SequentialExecutor", "LocalExecutor", "CeleryExecutor", "KubernetesExecutor"]
    },
    "metadata_database": {
        "purpose": "Stores DAG and task metadata",
        "supported": ["PostgreSQL", "MySQL", "SQLite (dev only)"]
    }
}

print("Airflow Architecture Components:")
for component, details in components.items():
    print(f"\n{component.upper()}:")
    print(f"  Purpose: {details['purpose']}")
```

---

## 📊 DAGs (Directed Acyclic Graphs) - Musical Compositions

> **Think of DAGs like sheet music for a symphony - they define exactly when each instrument should play, in what order, and how they coordinate together**

### 🎯 **Basic DAG Structure - Writing Sheet Music**

> **Creating a DAG is like composing sheet music - you define the tempo, instruments, and sequence of the performance**

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# DAG definition
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'example_dag',
    default_args=default_args,
    description='A simple example DAG',
    schedule_interval='@daily',
    catchup=False,
    tags=['example', 'tutorial']
)
```

### 📅 **Schedule Intervals - Concert Schedule**

> **Schedule intervals are like planning when concerts happen - daily matinees, weekly performances, or special one-time events**

```python
# Common schedule patterns
schedule_patterns = {
    "@once": "Run once",
    "@hourly": "0 * * * * (every hour)",
    "@daily": "0 0 * * * (every day at midnight)",
    "@weekly": "0 0 * * 0 (every Sunday)",
    "0 */6 * * *": "Every 6 hours",
    "30 2 * * 1-5": "2:30 AM on weekdays"
}

print("Schedule Patterns:")
for pattern, description in schedule_patterns.items():
    print(f"  {pattern}: {description}")
```

---

## 🔧 Tasks and Operators - Musicians and Instruments

> **Think of tasks as individual musicians and operators as the different types of instruments they can play**

### 🎯 **Core Operators - Orchestra Instruments**

> **Each operator type is like a different instrument section in the orchestra:**

- **PythonOperator** = 🎹 Piano (versatile, can play any melody)
- **BashOperator** = 🥁 Drums (executes commands with precision)
- **SQLOperator** = 🎻 Violin (elegant data queries)
- **EmailOperator** = 🎺 Trumpet (announces important events)

```python
# Essential operators
core_operators = {
    "PythonOperator": "Execute Python functions",
    "BashOperator": "Execute bash commands", 
    "SQLOperator": "Execute SQL queries",
    "EmailOperator": "Send email notifications"
}

# PythonOperator example
def process_data(**context):
    execution_date = context['execution_date']
    print(f"Processing data for {execution_date}")
    return {"processed_records": 1000}

task = PythonOperator(
    task_id='process_data',
    python_callable=process_data,
    dag=dag
)
```

---

## ⏰ Scheduling and Execution - Concert Timing

> **Think of scheduling like planning a concert series - each performance happens at the right time with perfect coordination**

### 📅 **Execution Date Concept - Concert Programs**

> **Execution date is like the date printed on concert programs - it represents which performance the music is for, not when the musicians actually rehearse**

```python
# Understanding execution_date
scheduling_example = {
    "start_date": "2024-01-01",
    "schedule_interval": "@daily",
    "first_run": "2024-01-02 00:00 (for execution_date 2024-01-01)",
    "second_run": "2024-01-03 00:00 (for execution_date 2024-01-02)"
}

print("Daily DAG Scheduling:")
for key, value in scheduling_example.items():
    print(f"  {key}: {value}")
```

---

## 📡 XComs and Task Communication

### 🔄 XCom Examples

```python
# Task communication via XComs
def push_data(**context):
    """Task that pushes data to XCom"""
    data = {"processed_records": 1000, "status": "success"}
    return data  # Automatically pushed to XCom

def pull_data(**context):
    """Task that pulls data from XCom"""
    data = context['task_instance'].xcom_pull(task_ids='push_data_task')
    print(f"Received data: {data}")
    return f"Processed {data['processed_records']} records"

# XCom limitations
xcom_guidelines = {
    "size_limit": "Small data only (< 48KB)",
    "serialization": "JSON serializable objects only",
    "alternatives": "Use external storage for large data"
}
```

---

## 🔌 Hooks and Connections

### 🎯 Connection Management

```python
# Common connection types
connection_types = {
    "postgres": {
        "conn_type": "Postgres",
        "example": "postgresql://user:pass@localhost:5432/mydb"
    },
    "aws": {
        "conn_type": "Amazon Web Services",
        "fields": ["aws_access_key_id", "aws_secret_access_key", "region"]
    },
    "http": {
        "conn_type": "HTTP", 
        "example": "https://api.example.com"
    }
}

# Using hooks
from airflow.providers.postgres.hooks.postgres import PostgresHook

def query_database(**context):
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    result = pg_hook.get_first("SELECT COUNT(*) FROM users")
    return result[0]
```

---

## 👁️ Sensors and Triggers

### 📡 Common Sensors

```python
# Sensor examples
sensor_types = {
    "FileSensor": "Wait for file to appear",
    "S3KeySensor": "Wait for S3 object to exist", 
    "SqlSensor": "Wait for SQL condition to be true",
    "TimeSensor": "Wait until specific time"
}

# FileSensor example
from airflow.sensors.filesystem import FileSensor

file_sensor = FileSensor(
    task_id='wait_for_file',
    filepath='/data/input.csv',
    poke_interval=30,
    timeout=300,
    dag=dag
)
```

---

## ⚙️ Configuration Essentials

### 🔧 Core Configuration

```python
# Essential settings
core_config = {
    "executor": "LocalExecutor",
    "sql_alchemy_conn": "postgresql://user:pass@localhost/airflow",
    "dags_folder": "/opt/airflow/dags",
    "load_examples": "False"
}

scheduler_config = {
    "catchup_by_default": "False",
    "max_active_runs_per_dag": "16",
    "parallelism": "32"
}
```

---

## 🎯 Best Practices

### 🏆 Development Guidelines

```python
best_practices = {
    "dag_design": [
        "Keep DAGs simple and focused",
        "Use meaningful task and DAG IDs",
        "Set catchup=False for most use cases",
        "Implement proper error handling"
    ],
    "task_design": [
        "Make tasks idempotent",
        "Keep tasks atomic",
        "Use XComs sparingly",
        "Avoid heavy computation in DAG definition"
    ]
}

print("Airflow Best Practices:")
for category, practices in best_practices.items():
    print(f"\n{category.upper()}:")
    for practice in practices:
        print(f"  • {practice}")
```

---

## 🎯 Interview Preparation

### 🔥 Key Interview Topics

```python
interview_topics = {
    "architecture": [
        "Explain Airflow's core components",
        "What is the role of the scheduler?",
        "How do different executors work?"
    ],
    "dag_concepts": [
        "What is a DAG and why directed acyclic?",
        "Explain execution_date vs actual run time",
        "How does catchup work?"
    ],
    "production": [
        "How do you monitor Airflow?",
        "What are scaling strategies?",
        "How do you handle secrets?"
    ]
}
```

### 💡 Sample Questions

**Q: Explain execution_date vs actual run time**

```python
def execution_date_explanation():
    explanation = {
        "execution_date": "Logical date/time the DAG run represents",
        "actual_run_time": "When DAG actually executes (usually later)",
        "example": {
            "execution_date": "2024-01-01 00:00:00",
            "actual_run_time": "2024-01-02 00:00:00",
            "reason": "Airflow waits for period to complete"
        }
    }
    return explanation
```

---

## 🎓 Next Steps

### 🚀 **Immediate Actions**
1. Set up local Airflow environment
2. Create simple DAGs with different operators
3. Practice with connections and hooks
4. Learn Airflow UI navigation

### 📚 **Advanced Topics**
- **[Airflow Advanced Patterns](./AIRFLOW_ADVANCED_ORCHESTRATION_PATTERNS.md)** - Production optimization
- Custom operators and sensors
- Airflow API usage
- Multi-cluster deployments

### 🛠️ **Build Projects**
1. **ETL Pipeline** - Database → Transform → Warehouse
2. **ML Pipeline** - Data prep → Training → Deployment
3. **API Integration** - Multiple APIs → Processing → Storage

Remember: **Airflow orchestrates the entire data ecosystem!** Master these concepts for robust pipeline management.

Happy orchestrating! 🎼✨