# Apache Airflow - Core Concepts

## Overview
Apache Airflow is an open-source platform for developing, scheduling, and monitoring workflows. It allows you to programmatically author, schedule, and monitor data pipelines.

## Key Concepts

### 1. Directed Acyclic Graph (DAG)
- Collection of tasks with dependencies
- Defines the workflow structure
- No cycles allowed (acyclic)
- Tasks flow in one direction (directed)

### 2. Tasks and Operators
- **Task**: Unit of work in a DAG
- **Operator**: Template for creating tasks

#### Common Operators
- **BashOperator**: Execute bash commands
- **PythonOperator**: Execute Python functions
- **SQLOperator**: Execute SQL queries
- **EmailOperator**: Send emails

### 3. Scheduling
- **schedule_interval**: How often DAG runs
- **start_date**: When DAG becomes active
- **catchup**: Whether to run missed intervals

### 4. XComs (Cross-Communication)
- Mechanism for tasks to exchange data
- Store small amounts of data
- Stored in Airflow's metadata database

## Architecture Components

### 1. Web Server
- Provides web UI for monitoring workflows
- Shows DAG status and task logs

### 2. Scheduler
- Monitors DAGs and triggers tasks
- Handles dependencies and scheduling

### 3. Executor
- Determines how tasks are executed
- Types: Sequential, Local, Celery, Kubernetes

### 4. Metadata Database
- Stores DAG definitions and execution history
- Supports PostgreSQL, MySQL, SQLite

## Best Practices

### 1. DAG Design
- Keep DAGs simple and focused
- Use meaningful names
- Implement proper error handling

### 2. Resource Management
- Don't store large data in XComs
- Use external storage for data exchange
- Monitor resource usage

### 3. Testing
- Test DAGs before deployment
- Use unit tests for Python functions
- Validate DAG structure

### 4. Security
- Use connections for credentials
- Implement proper access controls
- Encrypt sensitive data