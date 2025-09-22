
### Q1: What is Prefect and how does it differ from traditional workflow orchestration tools?
**Answer:**
Prefect is a modern workflow orchestration platform that emphasizes:
- **Hybrid execution model**: Flows can run anywhere while being orchestrated centrally
- **Positive engineering**: Focuses on what should happen rather than what could go wrong
- **Dynamic workflows**: Supports runtime flow generation and modification
- **Native Python**: Workflows are written in pure Python with decorators
- **Observability-first**: Built-in monitoring, logging, and debugging capabilities

Key differences from traditional tools:
- No need for complex DAG definitions
- Dynamic task generation at runtime
- Better error handling and recovery
- Modern UI with real-time updates
- Cloud-native architecture

### Q2: Explain the core components of Prefect architecture.
**Answer:**
**Core Components:**
1. **Prefect Server/Cloud**: Central orchestration and monitoring
2. **Agents**: Execute flows in various environments
3. **Flows**: Top-level containers for workflow logic
4. **Tasks**: Individual units of work within flows
5. **Storage**: Where flow code is stored (Git, S3, etc.)
6. **Run Config**: Defines execution environment
7. **Executor**: Handles task execution (local, distributed)

**Architecture Flow:**
```
Flow Registration → Storage → Agent Polling → Execution → Results → Server
```

### Q3: What are Flows and Tasks in Prefect? How do they relate?
**Answer:**
**Flows:**
- Top-level containers that define workflow logic
- Can contain multiple tasks and sub-flows
- Define dependencies and execution order
- Handle state management and scheduling

**Tasks:**
- Individual units of work within flows
- Atomic operations that can be retried independently
- Can have inputs, outputs, and dependencies
- Support caching and result persistence

**Relationship:**
```python
from prefect import flow, task

@task
def extract_data():
    return "data"

@task
def transform_data(data):
    return f"transformed_{data}"

@flow
def etl_pipeline():
    raw_data = extract_data()
    processed_data = transform_data(raw_data)
    return processed_data
```

---

## Architecture & Components

### Q4: Explain Prefect's hybrid execution model.
**Answer:**
**Hybrid Execution Model:**
- **Orchestration**: Centralized in Prefect Cloud/Server
- **Execution**: Distributed across various environments
- **Communication**: Agents poll for work and report back

**Benefits:**
- Flows run in their native environments
- No need to move code to orchestration platform
- Better security (no inbound connections required)
- Flexible deployment options

**Components:**
1. **Prefect Server**: Manages flow state and scheduling
2. **Agents**: Run in execution environments, poll for work
3. **Storage**: Code repository (Git, S3, Docker)
4. **Infrastructure**: Where flows actually execute

### Q5: What are Prefect Agents and how do they work?
**Answer:**
**Prefect Agents:**
- Lightweight processes that poll for scheduled flow runs
- Execute flows in their local environment
- Report results back to Prefect Server/Cloud

**Types of Agents:**
1. **Local Agent**: Runs flows as local processes
2. **Docker Agent**: Executes flows in Docker containers
3. **Kubernetes Agent**: Deploys flows as Kubernetes jobs
4. **ECS Agent**: Runs flows on AWS ECS
5. **Vertex Agent**: Executes on Google Cloud Vertex AI

**Agent Workflow:**
```python
# Agent polling cycle
while True:
    flow_runs = query_for_scheduled_runs()
    for run in flow_runs:
        submit_flow_run(run)
    sleep(polling_interval)
```

### Q6: How does Prefect handle state management?
**Answer:**
**State Management:**
Prefect uses a comprehensive state system to track flow and task execution:

**Flow States:**
- `Scheduled`: Waiting to run
- `Running`: Currently executing
- `Completed`: Finished successfully
- `Failed`: Encountered an error
- `Cancelled`: Manually stopped
- `Crashed`: Unexpected termination

**Task States:**
- `Pending`: Waiting for dependencies
- `Running`: Currently executing
- `Success`: Completed successfully
- `Failed`: Encountered an error
- `Skipped`: Conditionally bypassed
- `Cached`: Using cached result

**State Transitions:**
```python
from prefect import get_run_logger

@task
def monitored_task():
    logger = get_run_logger()
    logger.info("Task starting")
    # Task logic
    logger.info("Task completed")
```

---

## Flow Development

### Q7: How do you create and structure a Prefect flow?
**Answer:**
**Basic Flow Structure:**
```python
from prefect import flow, task
from typing import List

@task
def extract_data(source: str) -> List[dict]:
    # Extract logic
    return data

@task
def transform_data(data: List[dict]) -> List[dict]:
    # Transform logic
    return transformed_data

@task
def load_data(data: List[dict], destination: str):
    # Load logic
    pass

@flow(name="ETL Pipeline")
def etl_flow(source: str, destination: str):
    raw_data = extract_data(source)
    clean_data = transform_data(raw_data)
    load_data(clean_data, destination)
    return "Pipeline completed"

# Run the flow
if __name__ == "__main__":
    etl_flow("source_db", "target_db")
```

**Flow Features:**
- Automatic dependency resolution
- Parameter passing
- Return value handling
- Built-in logging

### Q8: How do you handle dynamic task generation in Prefect?
**Answer:**
**Dynamic Task Generation:**
```python
from prefect import flow, task

@task
def process_file(filename: str):
    # Process individual file
    return f"processed_{filename}"

@flow
def dynamic_processing_flow(file_list: List[str]):
    results = []
    for filename in file_list:
        # Dynamic task creation
        result = process_file(filename)
        results.append(result)
    return results

# Alternative using map
@flow
def mapped_processing_flow(file_list: List[str]):
    return process_file.map(file_list)
```

**Use Cases:**
- Processing variable number of files
- Dynamic API calls based on data
- Conditional workflow branches

### Q9: How do you implement conditional logic in Prefect flows?
**Answer:**
**Conditional Execution:**
```python
from prefect import flow, task

@task
def check_condition() -> bool:
    return True  # Some condition logic

@task
def task_a():
    return "Task A executed"

@task
def task_b():
    return "Task B executed"

@flow
def conditional_flow():
    condition = check_condition()
    
    if condition:
        result = task_a()
    else:
        result = task_b()
    
    return result

# Using task results for conditions
@flow
def data_driven_flow():
    data_size = get_data_size()
    
    if data_size > 1000:
        return process_large_dataset()
    else:
        return process_small_dataset()
```

---

## Task Management

### Q10: How do you configure task retries and timeouts in Prefect?
**Answer:**
**Task Configuration:**
```python
from prefect import task
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(
    retries=3,
    retry_delay_seconds=60,
    timeout_seconds=300,
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(hours=1)
)
def robust_task(data: str):
    # Task logic that might fail
    return processed_data

# Flow-level configuration
@flow(
    timeout_seconds=3600,
    retries=2
)
def robust_flow():
    return robust_task("input_data")
```

**Configuration Options:**
- `retries`: Number of retry attempts
- `retry_delay_seconds`: Delay between retries
- `timeout_seconds`: Maximum execution time
- `cache_key_fn`: Caching strategy
- `cache_expiration`: Cache validity period

### Q11: Explain task caching in Prefect.
**Answer:**
**Task Caching:**
Prefect provides intelligent caching to avoid re-running expensive tasks:

```python
from prefect import task
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(hours=24)
)
def expensive_computation(input_data):
    # Expensive operation
    return result

# Custom cache key
def custom_cache_key(context, parameters):
    return f"{parameters['data_date']}_{parameters['version']}"

@task(cache_key_fn=custom_cache_key)
def date_based_task(data_date, version):
    return processed_data
```

**Cache Key Functions:**
- `task_input_hash`: Based on input parameters
- `flow_run_name`: Based on flow run name
- Custom functions for specific logic

### Q12: How do you handle task dependencies in Prefect?
**Answer:**
**Dependency Management:**
```python
from prefect import flow, task

@task
def task_a():
    return "A"

@task
def task_b():
    return "B"

@task
def task_c(a_result, b_result):
    return f"{a_result}_{b_result}"

@flow
def dependency_flow():
    # Implicit dependencies through data flow
    a = task_a()
    b = task_b()
    c = task_c(a, b)  # Depends on both a and b
    return c

# Explicit dependencies
@flow
def explicit_dependency_flow():
    a = task_a()
    b = task_b()
    
    # Wait for both tasks before proceeding
    c = task_c.with_options(wait_for=[a, b])("manual_a", "manual_b")
    return c
```

---

## Deployment & Execution

### Q13: How do you deploy Prefect flows to production?
**Answer:**
**Deployment Process:**

1. **Create Deployment:**
```python
from prefect.deployments import Deployment
from prefect.infrastructure import DockerContainer

deployment = Deployment.build_from_flow(
    flow=etl_flow,
    name="production-etl",
    infrastructure=DockerContainer(
        image="my-etl-image:latest",
        env={"ENV": "production"}
    ),
    schedule=CronSchedule(cron="0 2 * * *"),  # Daily at 2 AM
    work_queue_name="production"
)

deployment.apply()
```

2. **Infrastructure Options:**
- Docker containers
- Kubernetes jobs
- AWS ECS tasks
- Local processes

3. **Storage Options:**
- Git repositories
- S3 buckets
- Docker images
- Local file system

### Q14: Explain Prefect's scheduling capabilities.
**Answer:**
**Scheduling Options:**

1. **Cron Schedules:**
```python
from prefect.schedules import CronSchedule

schedule = CronSchedule(
    cron="0 8 * * 1-5",  # Weekdays at 8 AM
    timezone="America/New_York"
)
```

2. **Interval Schedules:**
```python
from prefect.schedules import IntervalSchedule
from datetime import timedelta

schedule = IntervalSchedule(
    interval=timedelta(hours=6),
    anchor_date="2023-01-01T00:00:00"
)
```

3. **RRule Schedules:**
```python
from prefect.schedules import RRuleSchedule

schedule = RRuleSchedule(
    rrule="FREQ=WEEKLY;BYDAY=MO,WE,FR;BYHOUR=9"
)
```

### Q15: How do you manage different environments (dev, staging, prod) in Prefect?
**Answer:**
**Environment Management:**

1. **Work Queues:**
```python
# Different queues for different environments
deployment_dev = Deployment.build_from_flow(
    flow=my_flow,
    name="dev-deployment",
    work_queue_name="development"
)

deployment_prod = Deployment.build_from_flow(
    flow=my_flow,
    name="prod-deployment",
    work_queue_name="production"
)
```

2. **Environment Variables:**
```python
import os
from prefect import flow

@flow
def environment_aware_flow():
    env = os.getenv("ENVIRONMENT", "dev")
    
    if env == "production":
        return production_logic()
    else:
        return development_logic()
```

3. **Configuration Management:**
```python
from prefect.blocks.system import Secret

@flow
def secure_flow():
    db_password = Secret.load("db-password")
    # Use password for database connection
```

---

## Monitoring & Observability

### Q16: How does Prefect provide observability into workflow execution?
**Answer:**
**Observability Features:**

1. **Real-time Dashboard:**
- Flow run status and progress
- Task-level execution details
- Resource utilization metrics
- Error tracking and logs

2. **Logging:**
```python
from prefect import get_run_logger

@task
def logged_task():
    logger = get_run_logger()
    logger.info("Starting task execution")
    logger.warning("Potential issue detected")
    logger.error("Error occurred", extra={"error_code": 500})
```

3. **Metrics and Alerts:**
- Custom metrics collection
- Webhook notifications
- Email alerts for failures
- Slack/Teams integrations

4. **Flow Run Artifacts:**
```python
from prefect.artifacts import create_table_artifact

@task
def create_report():
    data = [["Name", "Value"], ["Metric1", 100], ["Metric2", 200]]
    create_table_artifact(
        key="daily-report",
        table=data,
        description="Daily metrics report"
    )
```

### Q17: How do you implement custom logging and monitoring in Prefect?
**Answer:**
**Custom Monitoring:**

1. **Custom Logging:**
```python
import logging
from prefect import get_run_logger

@task
def monitored_task():
    logger = get_run_logger()
    
    # Custom log formatting
    logger.info(
        "Processing batch",
        extra={
            "batch_id": "batch_123",
            "record_count": 1000,
            "processing_time": 45.2
        }
    )
```

2. **Metrics Collection:**
```python
from prefect import task
import time

@task
def timed_task():
    start_time = time.time()
    
    # Task logic
    result = process_data()
    
    execution_time = time.time() - start_time
    
    # Log metrics
    logger = get_run_logger()
    logger.info(f"Execution time: {execution_time}s")
    
    return result
```

3. **External Monitoring Integration:**
```python
import requests
from prefect import task

@task
def notify_external_system():
    # Send metrics to external monitoring system
    requests.post(
        "https://monitoring-system.com/metrics",
        json={"flow_status": "completed", "timestamp": time.time()}
    )
```

---

## Error Handling & Retries

### Q18: How do you implement comprehensive error handling in Prefect?
**Answer:**
**Error Handling Strategies:**

1. **Task-level Error Handling:**
```python
from prefect import task, flow
from prefect.exceptions import FAIL

@task(retries=3, retry_delay_seconds=60)
def resilient_task():
    try:
        # Risky operation
        result = risky_operation()
        return result
    except SpecificError as e:
        logger = get_run_logger()
        logger.error(f"Specific error: {e}")
        raise FAIL("Task failed due to specific error")
    except Exception as e:
        logger = get_run_logger()
        logger.warning(f"Unexpected error: {e}")
        # Let Prefect handle retry
        raise
```

2. **Flow-level Error Handling:**
```python
@flow
def error_handling_flow():
    try:
        result = risky_task()
        return result
    except Exception as e:
        # Cleanup or notification logic
        cleanup_task()
        send_alert(f"Flow failed: {e}")
        raise
```

3. **Custom Retry Logic:**
```python
from prefect.tasks import exponential_backoff

@task(
    retries=5,
    retry_delay_seconds=exponential_backoff(backoff_factor=2)
)
def task_with_backoff():
    # Task logic
    pass
```

### Q19: How do you handle partial failures in Prefect workflows?
**Answer:**
**Partial Failure Handling:**

1. **Continue on Failure:**
```python
@flow
def partial_failure_flow():
    results = []
    
    for item in items:
        try:
            result = process_item(item)
            results.append(result)
        except Exception as e:
            logger = get_run_logger()
            logger.warning(f"Failed to process {item}: {e}")
            # Continue with other items
            continue
    
    return results
```

2. **Conditional Execution:**
```python
@flow
def conditional_recovery_flow():
    try:
        primary_result = primary_task()
        return primary_result
    except Exception:
        logger = get_run_logger()
        logger.info("Primary task failed, using fallback")
        return fallback_task()
```

3. **State-based Recovery:**
```python
from prefect.states import Failed

@flow
def recovery_flow():
    task_state = risky_task(return_state=True)
    
    if isinstance(task_state, Failed):
        return recovery_task()
    else:
        return task_state.result()
```

---

## Scaling & Performance

### Q20: How do you scale Prefect workflows for high-volume data processing?
**Answer:**
**Scaling Strategies:**

1. **Parallel Task Execution:**
```python
from prefect import flow, task

@task
def process_chunk(chunk):
    return processed_chunk

@flow
def parallel_processing_flow(data_chunks):
    # Process chunks in parallel
    results = process_chunk.map(data_chunks)
    return combine_results(results)
```

2. **Distributed Execution:**
```python
from prefect.executors import DaskExecutor

@flow(executor=DaskExecutor(cluster_address="dask-cluster:8786"))
def distributed_flow():
    # Tasks will be distributed across Dask cluster
    return parallel_tasks()
```

3. **Resource Management:**
```python
from prefect.infrastructure import KubernetesJob

deployment = Deployment.build_from_flow(
    flow=heavy_computation_flow,
    infrastructure=KubernetesJob(
        cpu_request="2",
        cpu_limit="4",
        memory_request="4Gi",
        memory_limit="8Gi"
    )
)
```

### Q21: How do you optimize Prefect workflow performance?
**Answer:**
**Performance Optimization:**

1. **Task Granularity:**
```python
# Good: Appropriate task size
@task
def process_batch(batch_data):
    return [process_item(item) for item in batch_data]

# Avoid: Too fine-grained
@task
def process_single_item(item):
    return process_item(item)
```

2. **Caching Strategy:**
```python
@task(
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(hours=24)
)
def expensive_computation(params):
    # Cache expensive operations
    return compute_result(params)
```

3. **Resource Optimization:**
```python
@task(
    task_run_name="optimized-{batch_id}",
    tags=["high-memory", "cpu-intensive"]
)
def resource_intensive_task(batch_id, data):
    # Optimize resource usage
    return process_with_optimization(data)
```

---

## Integration & Ecosystem

### Q22: How do you integrate Prefect with external systems and databases?
**Answer:**
**Integration Patterns:**

1. **Database Integration:**
```python
from prefect import task
from prefect.blocks.sql import DatabaseCredentials
import pandas as pd

@task
def query_database():
    db_creds = DatabaseCredentials.load("production-db")
    
    with db_creds.get_connection() as conn:
        df = pd.read_sql("SELECT * FROM users", conn)
        return df

@task
def write_to_database(data):
    db_creds = DatabaseCredentials.load("warehouse-db")
    
    with db_creds.get_connection() as conn:
        data.to_sql("processed_users", conn, if_exists="replace")
```

2. **Cloud Service Integration:**
```python
from prefect_aws import S3Bucket
from prefect_gcp import GcsBucket

@task
def cloud_data_transfer():
    # AWS S3
    s3_bucket = S3Bucket.load("data-bucket")
    data = s3_bucket.read_path("input/data.csv")
    
    # Process data
    processed_data = transform_data(data)
    
    # Google Cloud Storage
    gcs_bucket = GcsBucket.load("output-bucket")
    gcs_bucket.write_path("output/processed.csv", processed_data)
```

3. **API Integration:**
```python
@task
def api_integration():
    import requests
    
    response = requests.get("https://api.example.com/data")
    data = response.json()
    
    # Process API data
    return process_api_data(data)
```

### Q23: How do you use Prefect Blocks for configuration management?
**Answer:**
**Prefect Blocks:**

1. **Creating Blocks:**
```python
from prefect.blocks.system import Secret
from prefect_aws import S3Bucket

# Create secret block
secret = Secret(value="my-secret-key")
secret.save("api-key")

# Create S3 bucket block
s3_bucket = S3Bucket(
    bucket_name="my-data-bucket",
    aws_access_key_id="access_key",
    aws_secret_access_key="secret_key"
)
s3_bucket.save("data-bucket")
```

2. **Using Blocks in Flows:**
```python
@task
def secure_task():
    api_key = Secret.load("api-key")
    bucket = S3Bucket.load("data-bucket")
    
    # Use blocks in task logic
    data = fetch_data_with_key(api_key.get())
    bucket.upload_from_dataframe(data, "output.csv")
```

3. **Block Types:**
- **Secret**: Secure credential storage
- **S3Bucket**: AWS S3 integration
- **GcsBucket**: Google Cloud Storage
- **DatabaseCredentials**: Database connections
- **DockerContainer**: Container configuration

---

## Best Practices

### Q24: What are the best practices for developing Prefect workflows?
**Answer:**
**Development Best Practices:**

1. **Flow Design:**
```python
# Good: Clear, focused flows
@flow(name="ETL Pipeline", description="Daily data processing")
def etl_pipeline(source: str, target: str, date: str):
    """
    Extract, transform, and load daily data.
    
    Args:
        source: Source database connection
        target: Target warehouse connection
        date: Processing date (YYYY-MM-DD)
    """
    data = extract_data(source, date)
    clean_data = transform_data(data)
    load_data(clean_data, target)
    return {"status": "success", "records": len(clean_data)}
```

2. **Task Organization:**
```python
# Good: Atomic, reusable tasks
@task(name="Extract Customer Data")
def extract_customers(db_conn: str, date: str) -> pd.DataFrame:
    """Extract customer data for specific date."""
    return pd.read_sql(query, db_conn)

@task(name="Validate Data Quality")
def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate data quality and completeness."""
    # Validation logic
    return validated_df
```

3. **Error Handling:**
```python
@task(retries=3, retry_delay_seconds=60)
def robust_api_call(endpoint: str):
    """Make API call with proper error handling."""
    try:
        response = requests.get(endpoint, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger = get_run_logger()
        logger.error(f"API call failed: {e}")
        raise
```

### Q25: How do you implement testing for Prefect workflows?
**Answer:**
**Testing Strategies:**

1. **Unit Testing Tasks:**
```python
import pytest
from prefect import flow, task

@task
def add_numbers(a: int, b: int) -> int:
    return a + b

def test_add_numbers():
    result = add_numbers(2, 3)
    assert result == 5

# Testing with Prefect context
def test_task_with_context():
    with flow("test-flow"):
        result = add_numbers(2, 3)
        assert result == 5
```

2. **Integration Testing:**
```python
@pytest.fixture
def test_database():
    # Setup test database
    yield test_db_connection
    # Cleanup

def test_etl_flow(test_database):
    # Test complete flow with test data
    result = etl_flow("test_source", "test_target", "2023-01-01")
    assert result["status"] == "success"
```

3. **Mock External Dependencies:**
```python
from unittest.mock import patch

@patch('requests.get')
def test_api_task(mock_get):
    mock_get.return_value.json.return_value = {"data": "test"}
    
    result = api_task("http://test.com")
    assert result["data"] == "test"
```

---

## Troubleshooting

### Q26: How do you debug failed Prefect workflows?
**Answer:**
**Debugging Strategies:**

1. **Log Analysis:**
```python
from prefect import get_run_logger

@task
def debug_task():
    logger = get_run_logger()
    
    logger.info("Task started", extra={"step": "initialization"})
    
    try:
        result = complex_operation()
        logger.info("Operation completed", extra={"result_size": len(result)})
        return result
    except Exception as e:
        logger.error("Operation failed", extra={"error": str(e), "step": "processing"})
        raise
```

2. **State Inspection:**
```python
# Check task states programmatically
@flow
def diagnostic_flow():
    task_state = problematic_task(return_state=True)
    
    if task_state.is_failed():
        logger = get_run_logger()
        logger.error(f"Task failed: {task_state.message}")
        # Implement recovery logic
```

3. **Local Testing:**
```python
# Run flows locally for debugging
if __name__ == "__main__":
    # Set up local environment
    os.environ["PREFECT_API_URL"] = "http://localhost:4200/api"
    
    # Run flow with debug parameters
    result = debug_flow(debug_mode=True)
    print(f"Debug result: {result}")
```

### Q27: What are common Prefect performance issues and how do you resolve them?
**Answer:**
**Common Issues and Solutions:**

1. **Task Overhead:**
```python
# Problem: Too many small tasks
@task
def process_item(item):
    return item * 2

# Solution: Batch processing
@task
def process_batch(items):
    return [item * 2 for item in items]
```

2. **Memory Issues:**
```python
# Problem: Large data in memory
@task
def memory_intensive_task():
    large_data = load_huge_dataset()  # Memory issue
    return process_data(large_data)

# Solution: Streaming/chunking
@task
def streaming_task():
    for chunk in stream_data():
        yield process_chunk(chunk)
```

3. **Agent Performance:**
```python
# Configure agent for better performance
prefect agent start \
    --work-queue "production" \
    --limit 10 \
    --prefetch-seconds 30
```

---

## Comparison Questions

### Q28: How does Prefect compare to Apache Airflow?
**Answer:**
**Prefect vs Airflow:**

| Aspect | Prefect | Airflow |
|--------|---------|---------|
| **Architecture** | Hybrid execution model | Centralized execution |
| **Code Style** | Pure Python with decorators | DAG-based Python |
| **Dynamic Workflows** | Native support | Limited support |
| **Error Handling** | Positive engineering approach | Traditional try/catch |
| **UI/UX** | Modern, real-time | Traditional web interface |
| **Deployment** | Flexible, cloud-native | Requires infrastructure setup |
| **Learning Curve** | Gentler, Python-native | Steeper, DAG concepts |
| **Scalability** | Built for cloud-scale | Requires configuration |

**When to Choose Prefect:**
- Modern Python-first approach
- Dynamic workflow requirements
- Cloud-native deployment
- Better developer experience

**When to Choose Airflow:**
- Established ecosystem
- Complex scheduling needs
- Large existing Airflow investment
- Extensive plugin ecosystem

### Q29: How does Prefect compare to other modern orchestration tools like Dagster?
**Answer:**
**Prefect vs Dagster:**

| Feature | Prefect | Dagster |
|---------|---------|---------|
| **Focus** | General workflow orchestration | Data-centric pipelines |
| **Type System** | Optional typing | Strong type system |
| **Testing** | Standard Python testing | Built-in testing framework |
| **Data Lineage** | Basic tracking | Advanced lineage tracking |
| **Asset Management** | Flow-based | Asset-centric |
| **Learning Curve** | Moderate | Steeper (data concepts) |
| **Use Cases** | General automation | Data engineering focused |

**Choose Prefect for:**
- General workflow automation
- Simpler learning curve
- Flexible deployment options
- Broader use case coverage

**Choose Dagster for:**
- Data-heavy pipelines
- Strong typing requirements
- Advanced data lineage needs
- Asset-centric thinking

### Q30: What factors should influence the choice of Prefect for a project?
**Answer:**
**Decision Factors:**

**Choose Prefect When:**
1. **Team Expertise**: Strong Python background
2. **Workflow Complexity**: Dynamic, data-driven workflows
3. **Deployment Flexibility**: Need for hybrid execution
4. **Development Speed**: Rapid prototyping requirements
5. **Modern Stack**: Cloud-native architecture preference
6. **Observability**: Need for real-time monitoring

**Consider Alternatives When:**
1. **Legacy Systems**: Heavy integration with existing tools
2. **Specific Domains**: Specialized requirements (e.g., ML pipelines)
3. **Enterprise Features**: Need for advanced governance
4. **Team Preferences**: Existing expertise in other tools
5. **Compliance**: Specific regulatory requirements

**Evaluation Criteria:**
- Development productivity
- Operational complexity
- Scalability requirements
- Integration needs
- Team skills and preferences
- Long-term maintenance considerations

---

## Advanced Configuration & Customization

### Q31: How do you implement custom task runners in Prefect?
**Answer:**
**Custom Task Runners:**

```python
from prefect.task_runners import BaseTaskRunner
from prefect import flow, task
import asyncio

class CustomTaskRunner(BaseTaskRunner):
    def __init__(self, max_workers: int = 4):
        super().__init__()
        self.max_workers = max_workers
    
    async def submit(self, key, call):
        # Custom submission logic
        return await asyncio.create_task(call())

@flow(task_runner=CustomTaskRunner(max_workers=8))
def custom_runner_flow():
    return parallel_tasks()
```

**Use Cases:**
- Custom resource management
- Specialized execution environments
- Integration with external schedulers
- Performance optimization

### Q32: How do you create custom Prefect blocks for reusable configurations?
**Answer:**
**Custom Block Development:**

```python
from prefect.blocks.core import Block
from pydantic import Field
from typing import Optional

class DatabaseConfig(Block):
    _block_type_name = "Database Config"
    _logo_url = "https://example.com/logo.png"
    
    host: str = Field(description="Database host")
    port: int = Field(default=5432, description="Database port")
    database: str = Field(description="Database name")
    username: str = Field(description="Username")
    password: str = Field(description="Password")
    
    def get_connection_string(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
    
    async def get_connection(self):
        import asyncpg
        return await asyncpg.connect(self.get_connection_string())

# Usage
db_config = DatabaseConfig(
    host="localhost",
    database="mydb",
    username="user",
    password="pass"
)
db_config.save("production-db")
```

### Q33: How do you implement custom result serializers in Prefect?
**Answer:**
**Custom Serializers:**

```python
from prefect.serializers import Serializer
from typing import Any
import pickle
import gzip

class CompressedPickleSerializer(Serializer):
    type: str = "compressed-pickle"
    
    def dumps(self, obj: Any) -> bytes:
        pickled = pickle.dumps(obj)
        return gzip.compress(pickled)
    
    def loads(self, data: bytes) -> Any:
        decompressed = gzip.decompress(data)
        return pickle.loads(decompressed)

# Register and use
from prefect.settings import PREFECT_RESULTS_DEFAULT_SERIALIZER

@task(result_serializer=CompressedPickleSerializer())
def large_data_task():
    return generate_large_dataset()
```

### Q34: How do you implement custom state handlers in Prefect?
**Answer:**
**Custom State Handlers:**

```python
from prefect import flow, task
from prefect.states import State, Failed, Completed
from prefect.context import get_run_context

def custom_state_handler(flow, flow_run, state):
    """Custom logic for state transitions."""
    if isinstance(state, Failed):
        # Send alert on failure
        send_failure_alert(flow_run.name, state.message)
        # Attempt recovery
        return trigger_recovery_flow(flow_run)
    
    elif isinstance(state, Completed):
        # Log success metrics
        log_success_metrics(flow_run.name, state.result())
    
    return state

@flow(on_completion=[custom_state_handler], on_failure=[custom_state_handler])
def monitored_flow():
    return process_data()
```

---

## Advanced Deployment Patterns

### Q35: How do you implement blue-green deployments with Prefect?
**Answer:**
**Blue-Green Deployment Strategy:**

```python
from prefect.deployments import Deployment
from prefect.infrastructure import DockerContainer

# Blue deployment (current production)
blue_deployment = Deployment.build_from_flow(
    flow=production_flow,
    name="production-blue",
    infrastructure=DockerContainer(
        image="myapp:v1.0",
        env={"ENVIRONMENT": "production", "VERSION": "blue"}
    ),
    work_queue_name="production-blue",
    is_schedule_active=True
)

# Green deployment (new version)
green_deployment = Deployment.build_from_flow(
    flow=production_flow,
    name="production-green",
    infrastructure=DockerContainer(
        image="myapp:v2.0",
        env={"ENVIRONMENT": "production", "VERSION": "green"}
    ),
    work_queue_name="production-green",
    is_schedule_active=False  # Initially inactive
)

# Deployment switching logic
@flow
def switch_deployment():
    # Validate green deployment
    if validate_green_deployment():
        # Activate green, deactivate blue
        activate_deployment("production-green")
        deactivate_deployment("production-blue")
    else:
        raise Exception("Green deployment validation failed")
```

### Q36: How do you implement canary deployments in Prefect?
**Answer:**
**Canary Deployment Pattern:**

```python
@flow
def canary_deployment_flow():
    # Route small percentage to canary
    canary_percentage = 10
    
    if random.randint(1, 100) <= canary_percentage:
        return canary_version_flow()
    else:
        return stable_version_flow()

# Gradual rollout
@flow
def gradual_rollout_flow():
    current_time = datetime.now().hour
    
    # Increase canary traffic over time
    if current_time < 6:  # Early morning
        canary_percentage = 5
    elif current_time < 12:  # Morning
        canary_percentage = 25
    elif current_time < 18:  # Afternoon
        canary_percentage = 50
    else:  # Evening
        canary_percentage = 100
    
    if random.randint(1, 100) <= canary_percentage:
        return new_version_flow()
    else:
        return current_version_flow()
```

### Q37: How do you implement multi-region deployments with Prefect?
**Answer:**
**Multi-Region Architecture:**

```python
from prefect.deployments import Deployment
from prefect.infrastructure import KubernetesJob

# US East deployment
us_east_deployment = Deployment.build_from_flow(
    flow=regional_flow,
    name="us-east-deployment",
    infrastructure=KubernetesJob(
        cluster_config="us-east-cluster",
        namespace="prefect-us-east"
    ),
    work_queue_name="us-east",
    parameters={"region": "us-east-1"}
)

# EU West deployment
eu_west_deployment = Deployment.build_from_flow(
    flow=regional_flow,
    name="eu-west-deployment",
    infrastructure=KubernetesJob(
        cluster_config="eu-west-cluster",
        namespace="prefect-eu-west"
    ),
    work_queue_name="eu-west",
    parameters={"region": "eu-west-1"}
)

# Cross-region coordination
@flow
def global_coordination_flow():
    # Trigger regional flows
    us_result = trigger_regional_flow.with_options(
        task_runner=KubernetesTaskRunner(cluster="us-east")
    )("us-east-1")
    
    eu_result = trigger_regional_flow.with_options(
        task_runner=KubernetesTaskRunner(cluster="eu-west")
    )("eu-west-1")
    
    # Aggregate results
    return aggregate_regional_results([us_result, eu_result])
```

---

## Data Pipeline Patterns

### Q38: How do you implement data validation pipelines in Prefect?
**Answer:**
**Data Validation Pipeline:**

```python
from prefect import flow, task
from great_expectations.core import ExpectationSuite
import pandas as pd

@task
def validate_data_quality(df: pd.DataFrame) -> dict:
    """Validate data quality using Great Expectations."""
    import great_expectations as ge
    
    # Convert to GE DataFrame
    ge_df = ge.from_pandas(df)
    
    # Define expectations
    results = {
        'null_check': ge_df.expect_column_values_to_not_be_null('id').success,
        'range_check': ge_df.expect_column_values_to_be_between('amount', 0, 10000).success,
        'format_check': ge_df.expect_column_values_to_match_regex('email', r'^[\w\.-]+@[\w\.-]+\.\w+$').success
    }
    
    return results

@task
def data_profiling(df: pd.DataFrame) -> dict:
    """Generate data profiling report."""
    profile = {
        'row_count': len(df),
        'column_count': len(df.columns),
        'null_percentage': df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100,
        'duplicate_rows': df.duplicated().sum(),
        'memory_usage': df.memory_usage(deep=True).sum()
    }
    return profile

@flow
def data_validation_pipeline(source: str):
    # Extract data
    raw_data = extract_data(source)
    
    # Profile data
    profile = data_profiling(raw_data)
    
    # Validate quality
    validation_results = validate_data_quality(raw_data)
    
    # Check if validation passed
    if all(validation_results.values()):
        # Proceed with processing
        processed_data = transform_data(raw_data)
        load_data(processed_data)
        return {"status": "success", "profile": profile}
    else:
        # Handle validation failure
        send_data_quality_alert(validation_results)
        raise ValueError(f"Data validation failed: {validation_results}")
```

### Q39: How do you implement incremental data processing in Prefect?
**Answer:**
**Incremental Processing Pattern:**

```python
from prefect import flow, task
from datetime import datetime, timedelta

@task
def get_last_processed_timestamp(table: str) -> datetime:
    """Get the last processed timestamp from metadata table."""
    query = f"SELECT MAX(processed_at) FROM {table}_metadata"
    result = execute_query(query)
    return result or datetime(2020, 1, 1)

@task
def extract_incremental_data(source: str, since: datetime) -> pd.DataFrame:
    """Extract data modified since last run."""
    query = f"""
    SELECT * FROM {source} 
    WHERE updated_at > '{since}'
    ORDER BY updated_at
    """
    return pd.read_sql(query, connection)

@task
def update_metadata(table: str, processed_at: datetime, record_count: int):
    """Update processing metadata."""
    query = f"""
    INSERT INTO {table}_metadata (processed_at, record_count, created_at)
    VALUES ('{processed_at}', {record_count}, NOW())
    """
    execute_query(query)

@flow
def incremental_etl_flow(source_table: str, target_table: str):
    # Get last processed timestamp
    last_processed = get_last_processed_timestamp(target_table)
    
    # Extract incremental data
    incremental_data = extract_incremental_data(source_table, last_processed)
    
    if len(incremental_data) > 0:
        # Transform data
        transformed_data = transform_data(incremental_data)
        
        # Load data (upsert)
        upsert_data(transformed_data, target_table)
        
        # Update metadata
        current_time = datetime.now()
        update_metadata(target_table, current_time, len(transformed_data))
        
        return {"status": "success", "records_processed": len(transformed_data)}
    else:
        return {"status": "no_new_data", "records_processed": 0}
```

### Q40: How do you implement data lineage tracking in Prefect?
**Answer:**
**Data Lineage Implementation:**

```python
from prefect import flow, task
from prefect.context import get_run_context
from typing import List, Dict

class DataLineageTracker:
    def __init__(self):
        self.lineage_graph = {}
    
    def track_input(self, task_name: str, input_sources: List[str]):
        """Track input data sources for a task."""
        if task_name not in self.lineage_graph:
            self.lineage_graph[task_name] = {"inputs": [], "outputs": []}
        self.lineage_graph[task_name]["inputs"].extend(input_sources)
    
    def track_output(self, task_name: str, output_targets: List[str]):
        """Track output data targets for a task."""
        if task_name not in self.lineage_graph:
            self.lineage_graph[task_name] = {"inputs": [], "outputs": []}
        self.lineage_graph[task_name]["outputs"].extend(output_targets)
    
    def get_lineage(self) -> Dict:
        return self.lineage_graph

# Global lineage tracker
lineage_tracker = DataLineageTracker()

@task
def extract_with_lineage(source_table: str) -> pd.DataFrame:
    """Extract data with lineage tracking."""
    context = get_run_context()
    task_name = context.task_run.name
    
    # Track input source
    lineage_tracker.track_input(task_name, [source_table])
    
    # Extract data
    data = pd.read_sql(f"SELECT * FROM {source_table}", connection)
    
    return data

@task
def transform_with_lineage(data: pd.DataFrame, transformation_name: str) -> pd.DataFrame:
    """Transform data with lineage tracking."""
    context = get_run_context()
    task_name = context.task_run.name
    
    # Track transformation
    lineage_tracker.track_input(task_name, [f"transformation:{transformation_name}"])
    
    # Apply transformation
    transformed_data = apply_transformation(data, transformation_name)
    
    return transformed_data

@task
def load_with_lineage(data: pd.DataFrame, target_table: str):
    """Load data with lineage tracking."""
    context = get_run_context()
    task_name = context.task_run.name
    
    # Track output target
    lineage_tracker.track_output(task_name, [target_table])
    
    # Load data
    data.to_sql(target_table, connection, if_exists='replace')

@flow
def lineage_aware_etl():
    # ETL with lineage tracking
    raw_data = extract_with_lineage("source_customers")
    clean_data = transform_with_lineage(raw_data, "data_cleaning")
    enriched_data = transform_with_lineage(clean_data, "data_enrichment")
    load_with_lineage(enriched_data, "target_customers")
    
    # Store lineage information
    lineage = lineage_tracker.get_lineage()
    store_lineage_metadata(lineage)
    
    return lineage
```

---

## Performance Optimization

### Q41: How do you optimize memory usage in Prefect workflows?
**Answer:**
**Memory Optimization Strategies:**

```python
from prefect import flow, task
import pandas as pd
from typing import Iterator

@task
def memory_efficient_processing(file_path: str, chunk_size: int = 10000) -> Iterator[pd.DataFrame]:
    """Process large files in chunks to manage memory."""
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        # Process chunk
        processed_chunk = transform_chunk(chunk)
        yield processed_chunk
        # Chunk goes out of scope and gets garbage collected

@task
def streaming_aggregation(chunks: Iterator[pd.DataFrame]) -> dict:
    """Aggregate data from chunks without loading all into memory."""
    total_records = 0
    sum_amount = 0
    
    for chunk in chunks:
        total_records += len(chunk)
        sum_amount += chunk['amount'].sum()
        # Process and discard chunk
    
    return {"total_records": total_records, "total_amount": sum_amount}

@task(cache_key_fn=None)  # Disable caching for memory-intensive tasks
def large_data_task():
    """Task that processes large data without caching."""
    # Process large dataset
    result = process_large_dataset()
    
    # Return only summary, not full data
    return {"status": "completed", "record_count": len(result)}

@flow
def memory_optimized_flow(file_path: str):
    # Process in chunks
    chunks = memory_efficient_processing(file_path)
    
    # Aggregate without loading all data
    summary = streaming_aggregation(chunks)
    
    return summary
```

### Q42: How do you implement parallel processing optimization in Prefect?
**Answer:**
**Parallel Processing Patterns:**

```python
from prefect import flow, task
from prefect.task_runners import ConcurrentTaskRunner
from concurrent.futures import ThreadPoolExecutor
import asyncio

@task
def cpu_intensive_task(data_chunk: list) -> list:
    """CPU-intensive task that benefits from process-based parallelism."""
    return [complex_computation(item) for item in data_chunk]

@task
def io_intensive_task(url: str) -> dict:
    """I/O-intensive task that benefits from thread-based parallelism."""
    import requests
    response = requests.get(url)
    return response.json()

@flow(task_runner=ConcurrentTaskRunner())
def optimized_parallel_flow(data_chunks: list, urls: list):
    # CPU-intensive tasks - use process pool
    cpu_results = cpu_intensive_task.map(data_chunks)
    
    # I/O-intensive tasks - use thread pool
    io_results = io_intensive_task.map(urls)
    
    # Combine results
    return combine_results(cpu_results, io_results)

# Custom task runner for specific optimization
class OptimizedTaskRunner(ConcurrentTaskRunner):
    def __init__(self):
        super().__init__()
        self.cpu_executor = ProcessPoolExecutor(max_workers=4)
        self.io_executor = ThreadPoolExecutor(max_workers=20)
    
    async def submit(self, key, call):
        # Route tasks to appropriate executor based on task type
        if "cpu_intensive" in key:
            return await asyncio.get_event_loop().run_in_executor(
                self.cpu_executor, call
            )
        else:
            return await asyncio.get_event_loop().run_in_executor(
                self.io_executor, call
            )
```

### Q43: How do you implement caching strategies for expensive operations?
**Answer:**
**Advanced Caching Strategies:**

```python
from prefect import task, flow
from prefect.tasks import task_input_hash
from datetime import timedelta
import hashlib
import json

def smart_cache_key(context, parameters):
    """Generate cache key based on data freshness requirements."""
    # Include date for daily refresh
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Hash parameters for uniqueness
    param_hash = hashlib.md5(
        json.dumps(parameters, sort_keys=True).encode()
    ).hexdigest()[:8]
    
    return f"{date_str}_{param_hash}"

def conditional_cache_key(context, parameters):
    """Cache key that considers data size for selective caching."""
    data_size = parameters.get('data_size', 0)
    
    # Only cache for large datasets
    if data_size > 100000:
        return task_input_hash(context, parameters)
    else:
        # No caching for small datasets
        return None

@task(
    cache_key_fn=smart_cache_key,
    cache_expiration=timedelta(hours=24),
    refresh_cache=False
)
def expensive_ml_training(dataset_path: str, model_params: dict):
    """Expensive ML training with smart caching."""
    # Load and train model
    model = train_model(dataset_path, model_params)
    return model

@task(
    cache_key_fn=conditional_cache_key,
    cache_expiration=timedelta(hours=6)
)
def adaptive_data_processing(data: list, data_size: int):
    """Processing with conditional caching based on data size."""
    return process_data(data)

# Cache warming strategy
@flow
def cache_warming_flow():
    """Pre-populate cache with commonly used results."""
    common_parameters = [
        {"dataset": "daily", "model": "regression"},
        {"dataset": "weekly", "model": "classification"},
        {"dataset": "monthly", "model": "clustering"}
    ]
    
    # Warm cache with common parameter combinations
    for params in common_parameters:
        expensive_ml_training(params["dataset"], {"type": params["model"]})
```

---

## Security & Compliance

### Q44: How do you implement secure credential management in Prefect?
**Answer:**
**Secure Credential Management:**

```python
from prefect.blocks.system import Secret
from prefect import flow, task
import os
from cryptography.fernet import Fernet

class SecureCredentialManager:
    def __init__(self):
        self.encryption_key = os.getenv("PREFECT_ENCRYPTION_KEY")
        self.cipher = Fernet(self.encryption_key) if self.encryption_key else None
    
    def encrypt_credential(self, credential: str) -> str:
        """Encrypt credential before storage."""
        if self.cipher:
            return self.cipher.encrypt(credential.encode()).decode()
        return credential
    
    def decrypt_credential(self, encrypted_credential: str) -> str:
        """Decrypt credential for use."""
        if self.cipher:
            return self.cipher.decrypt(encrypted_credential.encode()).decode()
        return encrypted_credential

@task
def secure_database_connection():
    """Establish database connection with secure credentials."""
    # Load encrypted credentials
    db_password = Secret.load("db-password-encrypted")
    
    # Decrypt for use
    credential_manager = SecureCredentialManager()
    decrypted_password = credential_manager.decrypt_credential(db_password.get())
    
    # Use credentials (never log them)
    connection = create_connection(
        host=os.getenv("DB_HOST"),
        username=os.getenv("DB_USER"),
        password=decrypted_password
    )
    
    return connection

@task
def audit_trail_task(operation: str, user: str, data_accessed: str):
    """Create audit trail for compliance."""
    audit_entry = {
        "timestamp": datetime.now().isoformat(),
        "operation": operation,
        "user": user,
        "data_accessed": data_accessed,
        "flow_run_id": get_run_context().flow_run.id
    }
    
    # Store in secure audit log
    store_audit_entry(audit_entry)

@flow
def compliant_data_flow(user_id: str):
    # Audit data access
    audit_trail_task("data_access", user_id, "customer_data")
    
    # Secure data processing
    connection = secure_database_connection()
    data = extract_data(connection)
    
    # Process with data masking
    masked_data = mask_sensitive_data(data)
    
    # Audit processing completion
    audit_trail_task("data_processing", user_id, "customer_data_processed")
    
    return masked_data
```

### Q45: How do you implement data privacy and GDPR compliance in Prefect?
**Answer:**
**GDPR Compliance Implementation:**

```python
from prefect import flow, task
from typing import List, Dict
import hashlib

@task
def anonymize_personal_data(data: pd.DataFrame, pii_columns: List[str]) -> pd.DataFrame:
    """Anonymize personally identifiable information."""
    anonymized_data = data.copy()
    
    for column in pii_columns:
        if column in anonymized_data.columns:
            # Hash PII data
            anonymized_data[column] = anonymized_data[column].apply(
                lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:16] if pd.notna(x) else x
            )
    
    return anonymized_data

@task
def data_retention_check(data: pd.DataFrame, retention_days: int) -> pd.DataFrame:
    """Filter data based on retention policy."""
    cutoff_date = datetime.now() - timedelta(days=retention_days)
    
    # Filter data within retention period
    if 'created_at' in data.columns:
        data['created_at'] = pd.to_datetime(data['created_at'])
        filtered_data = data[data['created_at'] >= cutoff_date]
        return filtered_data
    
    return data

@task
def consent_verification(user_ids: List[str]) -> List[str]:
    """Verify user consent for data processing."""
    consented_users = []
    
    for user_id in user_ids:
        # Check consent status
        consent_status = check_user_consent(user_id)
        if consent_status and consent_status.get('data_processing', False):
            consented_users.append(user_id)
    
    return consented_users

@task
def data_deletion_request(user_id: str) -> Dict:
    """Handle GDPR data deletion request."""
    deletion_results = {}
    
    # Delete from all relevant tables
    tables_to_clean = ['users', 'user_activities', 'user_preferences']
    
    for table in tables_to_clean:
        deleted_count = delete_user_data(table, user_id)
        deletion_results[table] = deleted_count
    
    # Log deletion for audit
    log_data_deletion(user_id, deletion_results)
    
    return deletion_results

@flow
def gdpr_compliant_processing_flow(user_ids: List[str]):
    # Verify consent
    consented_users = consent_verification(user_ids)
    
    if not consented_users:
        return {"status": "no_consent", "processed_users": 0}
    
    # Extract data for consented users only
    user_data = extract_user_data(consented_users)
    
    # Apply retention policy
    retained_data = data_retention_check(user_data, retention_days=365)
    
    # Anonymize PII
    pii_columns = ['email', 'phone', 'address']
    anonymized_data = anonymize_personal_data(retained_data, pii_columns)
    
    # Process anonymized data
    processed_data = process_data(anonymized_data)
    
    return {
        "status": "success",
        "processed_users": len(consented_users),
        "records_processed": len(processed_data)
    }
```

---

## Real-World Scenarios

### Q46: How do you handle data pipeline failures and implement circuit breakers?
**Answer:**
**Circuit Breaker Pattern:**

```python
from prefect import flow, task
from enum import Enum
from datetime import datetime, timedelta

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open" # Testing if service recovered

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _should_attempt_reset(self):
        return (datetime.now() - self.last_failure_time).seconds >= self.timeout
    
    def _on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# Global circuit breakers
api_circuit_breaker = CircuitBreaker(failure_threshold=3, timeout=300)
db_circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=120)

@task(retries=0)  # Let circuit breaker handle retries
def resilient_api_call(endpoint: str):
    """API call with circuit breaker protection."""
    def make_api_call():
        import requests
        response = requests.get(endpoint, timeout=30)
        response.raise_for_status()
        return response.json()
    
    return api_circuit_breaker.call(make_api_call)

@task(retries=0)
def resilient_db_query(query: str):
    """Database query with circuit breaker protection."""
    def execute_query():
        connection = get_db_connection()
        return pd.read_sql(query, connection)
    
    return db_circuit_breaker.call(execute_query)

@flow
def resilient_data_pipeline():
    try:
        # Protected API call
        api_data = resilient_api_call("https://api.example.com/data")
        
        # Protected database query
        db_data = resilient_db_query("SELECT * FROM source_table")
        
        # Process data
        processed_data = process_data(api_data, db_data)
        
        return {"status": "success", "records": len(processed_data)}
        
    except Exception as e:
        # Fallback to cached data or alternative source
        logger = get_run_logger()
        logger.warning(f"Primary pipeline failed: {e}")
        
        fallback_data = get_cached_data()
        return {"status": "fallback", "records": len(fallback_data)}
```

### Q47: How do you implement data quality monitoring and alerting?
**Answer:**
**Data Quality Monitoring:**

```python
from prefect import flow, task
from dataclasses import dataclass
from typing import List, Dict, Any
import pandas as pd

@dataclass
class DataQualityRule:
    name: str
    description: str
    severity: str  # 'critical', 'warning', 'info'
    threshold: float
    
class DataQualityMonitor:
    def __init__(self):
        self.rules = []
        self.results = []
    
    def add_rule(self, rule: DataQualityRule):
        self.rules.append(rule)
    
    def check_completeness(self, df: pd.DataFrame, column: str, threshold: float) -> Dict:
        """Check data completeness."""
        null_percentage = df[column].isnull().sum() / len(df) * 100
        passed = null_percentage <= threshold
        
        return {
            'rule': 'completeness',
            'column': column,
            'value': null_percentage,
            'threshold': threshold,
            'passed': passed,
            'severity': 'critical' if not passed else 'info'
        }
    
    def check_uniqueness(self, df: pd.DataFrame, column: str, threshold: float) -> Dict:
        """Check data uniqueness."""
        duplicate_percentage = df[column].duplicated().sum() / len(df) * 100
        passed = duplicate_percentage <= threshold
        
        return {
            'rule': 'uniqueness',
            'column': column,
            'value': duplicate_percentage,
            'threshold': threshold,
            'passed': passed,
            'severity': 'warning' if not passed else 'info'
        }
    
    def check_range(self, df: pd.DataFrame, column: str, min_val: float, max_val: float) -> Dict:
        """Check value ranges."""
        out_of_range = ((df[column] < min_val) | (df[column] > max_val)).sum()
        out_of_range_percentage = out_of_range / len(df) * 100
        passed = out_of_range_percentage == 0
        
        return {
            'rule': 'range',
            'column': column,
            'value': out_of_range_percentage,
            'min_val': min_val,
            'max_val': max_val,
            'passed': passed,
            'severity': 'critical' if not passed else 'info'
        }

@task
def run_data_quality_checks(df: pd.DataFrame, table_name: str) -> List[Dict]:
    """Run comprehensive data quality checks."""
    monitor = DataQualityMonitor()
    results = []
    
    # Completeness checks
    for column in df.columns:
        if df[column].dtype in ['object', 'string']:
            result = monitor.check_completeness(df, column, threshold=5.0)
            results.append(result)
    
    # Uniqueness checks for ID columns
    id_columns = [col for col in df.columns if 'id' in col.lower()]
    for column in id_columns:
        result = monitor.check_uniqueness(df, column, threshold=0.0)
        results.append(result)
    
    # Range checks for numeric columns
    numeric_columns = df.select_dtypes(include=['number']).columns
    for column in numeric_columns:
        if 'amount' in column.lower() or 'price' in column.lower():
            result = monitor.check_range(df, column, min_val=0, max_val=1000000)
            results.append(result)
    
    return results

@task
def send_quality_alerts(quality_results: List[Dict], table_name: str):
    """Send alerts for data quality issues."""
    critical_issues = [r for r in quality_results if r['severity'] == 'critical' and not r['passed']]
    warning_issues = [r for r in quality_results if r['severity'] == 'warning' and not r['passed']]
    
    if critical_issues:
        # Send immediate alert
        alert_message = f"CRITICAL: Data quality issues in {table_name}:\n"
        for issue in critical_issues:
            alert_message += f"- {issue['rule']} check failed for {issue['column']}\n"
        
        send_slack_alert(alert_message, channel="#data-alerts")
        send_email_alert(alert_message, recipients=["data-team@company.com"])
    
    if warning_issues:
        # Log warnings
        logger = get_run_logger()
        for issue in warning_issues:
            logger.warning(f"Data quality warning: {issue['rule']} issue in {issue['column']}")

@flow
def data_quality_monitoring_flow(table_name: str):
    # Extract data
    data = extract_table_data(table_name)
    
    # Run quality checks
    quality_results = run_data_quality_checks(data, table_name)
    
    # Send alerts if needed
    send_quality_alerts(quality_results, table_name)
    
    # Store quality metrics
    store_quality_metrics(table_name, quality_results)
    
    # Calculate overall quality score
    passed_checks = sum(1 for r in quality_results if r['passed'])
    total_checks = len(quality_results)
    quality_score = (passed_checks / total_checks) * 100 if total_checks > 0 else 100
    
    return {
        "table": table_name,
        "quality_score": quality_score,
        "total_checks": total_checks,
        "passed_checks": passed_checks,
        "critical_issues": len([r for r in quality_results if r['severity'] == 'critical' and not r['passed']])
    }
```

### Q48: How do you implement disaster recovery for Prefect workflows?
**Answer:**
**Disaster Recovery Strategy:**

```python
from prefect import flow, task
from prefect.deployments import Deployment
from prefect.infrastructure import DockerContainer
import boto3
from datetime import datetime

class DisasterRecoveryManager:
    def __init__(self):
        self.primary_region = "us-east-1"
        self.backup_region = "us-west-2"
        self.s3_client = boto3.client('s3')
    
    def backup_flow_state(self, flow_run_id: str, state_data: dict):
        """Backup flow state to multiple regions."""
        backup_key = f"flow-states/{flow_run_id}/{datetime.now().isoformat()}.json"
        
        # Backup to primary region
        self.s3_client.put_object(
            Bucket=f"prefect-backup-{self.primary_region}",
            Key=backup_key,
            Body=json.dumps(state_data)
        )
        
        # Backup to secondary region
        backup_s3 = boto3.client('s3', region_name=self.backup_region)
        backup_s3.put_object(
            Bucket=f"prefect-backup-{self.backup_region}",
            Key=backup_key,
            Body=json.dumps(state_data)
        )
    
    def restore_flow_state(self, flow_run_id: str) -> dict:
        """Restore flow state from backup."""
        try:
            # Try primary region first
            response = self.s3_client.list_objects_v2(
                Bucket=f"prefect-backup-{self.primary_region}",
                Prefix=f"flow-states/{flow_run_id}/"
            )
        except Exception:
            # Fallback to backup region
            backup_s3 = boto3.client('s3', region_name=self.backup_region)
            response = backup_s3.list_objects_v2(
                Bucket=f"prefect-backup-{self.backup_region}",
                Prefix=f"flow-states/{flow_run_id}/"
            )
        
        # Get latest backup
        if 'Contents' in response:
            latest_backup = sorted(response['Contents'], key=lambda x: x['LastModified'])[-1]
            backup_data = self.s3_client.get_object(
                Bucket=f"prefect-backup-{self.primary_region}",
                Key=latest_backup['Key']
            )
            return json.loads(backup_data['Body'].read())
        
        return None

@task
def create_checkpoint(flow_run_id: str, checkpoint_data: dict):
    """Create recovery checkpoint."""
    dr_manager = DisasterRecoveryManager()
    dr_manager.backup_flow_state(flow_run_id, checkpoint_data)
    
    logger = get_run_logger()
    logger.info(f"Checkpoint created for flow run {flow_run_id}")

@task
def health_check() -> dict:
    """Check system health for disaster recovery."""
    health_status = {
        "database": check_database_health(),
        "api_services": check_api_health(),
        "storage": check_storage_health(),
        "timestamp": datetime.now().isoformat()
    }
    
    return health_status

@flow
def disaster_recovery_flow(original_flow_run_id: str = None):
    """Disaster recovery workflow."""
    if original_flow_run_id:
        # Recovery mode
        logger = get_run_logger()
        logger.info(f"Starting disaster recovery for flow {original_flow_run_id}")
        
        # Restore state
        dr_manager = DisasterRecoveryManager()
        restored_state = dr_manager.restore_flow_state(original_flow_run_id)
        
        if restored_state:
            # Resume from checkpoint
            return resume_from_checkpoint(restored_state)
        else:
            # Full restart
            logger.warning("No checkpoint found, starting from beginning")
            return full_restart_flow()
    else:
        # Normal operation with checkpointing
        context = get_run_context()
        flow_run_id = context.flow_run.id
        
        # Step 1: Initial processing
        step1_result = initial_processing_step()
        create_checkpoint(flow_run_id, {"step": 1, "result": step1_result})
        
        # Step 2: Data transformation
        step2_result = data_transformation_step(step1_result)
        create_checkpoint(flow_run_id, {"step": 2, "result": step2_result})
        
        # Step 3: Final processing
        final_result = final_processing_step(step2_result)
        create_checkpoint(flow_run_id, {"step": 3, "result": final_result})
        
        return final_result

# Multi-region deployment for disaster recovery
primary_deployment = Deployment.build_from_flow(
    flow=disaster_recovery_flow,
    name="primary-deployment",
    infrastructure=DockerContainer(
        image="myapp:latest",
        env={"REGION": "us-east-1", "MODE": "primary"}
    ),
    work_queue_name="primary-queue"
)

backup_deployment = Deployment.build_from_flow(
    flow=disaster_recovery_flow,
    name="backup-deployment",
    infrastructure=DockerContainer(
        image="myapp:latest",
        env={"REGION": "us-west-2", "MODE": "backup"}
    ),
    work_queue_name="backup-queue",
    is_schedule_active=False  # Activated only during disaster
)
```

### Q49: How do you implement cost optimization strategies for Prefect workflows?
**Answer:**
**Cost Optimization Strategies:**

```python
from prefect import flow, task
from prefect.infrastructure import DockerContainer, KubernetesJob
from datetime import datetime, time

@task
def cost_aware_processing(data_size: int, priority: str = "normal"):
    """Process data with cost-aware resource allocation."""
    if priority == "low" and data_size < 10000:
        # Use spot instances for low-priority, small jobs
        return process_on_spot_instance(data_size)
    elif data_size > 100000:
        # Use reserved instances for large, predictable workloads
        return process_on_reserved_instance(data_size)
    else:
        # Use on-demand for standard processing
        return process_on_demand(data_size)

@flow
def cost_optimized_flow(data_batches: list):
    # Schedule expensive operations during off-peak hours
    current_hour = datetime.now().hour
    
    if 2 <= current_hour <= 6:  # Off-peak hours
        # Use larger, more cost-effective instances
        infrastructure = KubernetesJob(
            cpu_request="4",
            memory_request="8Gi",
            node_selector={"instance-type": "spot"}
        )
    else:
        # Use smaller instances during peak hours
        infrastructure = KubernetesJob(
            cpu_request="1",
            memory_request="2Gi",
            node_selector={"instance-type": "on-demand"}
        )
    
    # Process batches with appropriate resources
    results = []
    for batch in data_batches:
        result = cost_aware_processing.with_options(
            infrastructure=infrastructure
        )(len(batch), priority="normal")
        results.append(result)
    
    return results
```

### Q50: How do you implement A/B testing workflows in Prefect?
**Answer:**
**A/B Testing Implementation:**

```python
from prefect import flow, task
import random
from typing import Dict, Any

class ABTestManager:
    def __init__(self):
        self.experiments = {}
    
    def create_experiment(self, name: str, variants: Dict[str, float]):
        """Create A/B test experiment with traffic allocation."""
        total_weight = sum(variants.values())
        normalized_variants = {k: v/total_weight for k, v in variants.items()}
        
        self.experiments[name] = {
            "variants": normalized_variants,
            "results": {variant: [] for variant in variants.keys()}
        }
    
    def assign_variant(self, experiment_name: str, user_id: str) -> str:
        """Assign user to experiment variant."""
        if experiment_name not in self.experiments:
            return "control"
        
        # Deterministic assignment based on user_id
        random.seed(hash(user_id) % 2**32)
        rand_val = random.random()
        
        cumulative_weight = 0
        variants = self.experiments[experiment_name]["variants"]
        
        for variant, weight in variants.items():
            cumulative_weight += weight
            if rand_val <= cumulative_weight:
                return variant
        
        return list(variants.keys())[0]  # Fallback

@flow
def ab_testing_flow(user_id: str, data: list):
    # Initialize A/B test
    ab_manager = ABTestManager()
    ab_manager.create_experiment(
        "algorithm_comparison",
        {"control": 0.5, "treatment": 0.5}
    )
    
    # Assign user to variant
    variant = ab_manager.assign_variant("algorithm_comparison", user_id)
    
    # Execute appropriate algorithm
    if variant == "treatment":
        result = algorithm_b_processing(data)
    else:
        result = algorithm_a_processing(data)
    
    return {**result, "variant": variant, "user_id": user_id}
```

---

## Summary

Prefect represents a modern approach to workflow orchestration with its hybrid execution model, Python-native development experience, and cloud-first architecture. Key strengths include dynamic workflow generation, excellent observability, and flexible deployment options. When evaluating Prefect, consider your team's Python expertise, workflow complexity requirements, and preference for modern development practices.

## Advanced Integration & Ecosystem

### Q51: How do you integrate Prefect with Apache Kafka for real-time data processing?
**Answer:**
**Kafka Integration Pattern:**

```python
from prefect import flow, task
from kafka import KafkaConsumer, KafkaProducer
import json

@task
def consume_kafka_messages(topic: str, batch_size: int = 100) -> list:
    """Consume messages from Kafka topic."""
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        consumer_timeout_ms=10000
    )
    
    messages = []
    for message in consumer:
        messages.append(message.value)
        if len(messages) >= batch_size:
            break
    
    consumer.close()
    return messages

@task
def process_streaming_data(messages: list) -> list:
    """Process streaming data batch."""
    processed = []
    for message in messages:
        # Apply transformations
        transformed = {
            'id': message['id'],
            'processed_at': datetime.now().isoformat(),
            'value': message['value'] * 1.1,
            'category': classify_data(message)
        }
        processed.append(transformed)
    return processed

@task
def publish_results(processed_data: list, output_topic: str):
    """Publish processed results to output topic."""
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    
    for record in processed_data:
        producer.send(output_topic, record)
    
    producer.flush()
    producer.close()

@flow
def kafka_streaming_flow():
    # Consume from input topic
    raw_messages = consume_kafka_messages('input-topic')
    
    if raw_messages:
        # Process data
        processed_data = process_streaming_data(raw_messages)
        
        # Publish to output topic
        publish_results(processed_data, 'output-topic')
        
        return {"processed_count": len(processed_data)}
    
    return {"processed_count": 0}
```

### Q52: How do you implement Prefect workflows with Apache Spark integration?
**Answer:**
**Spark Integration:**

```python
from prefect import flow, task
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, sum as spark_sum

@task
def create_spark_session(app_name: str) -> SparkSession:
    """Create Spark session with optimized configuration."""
    spark = SparkSession.builder \
        .appName(app_name) \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
        .getOrCreate()
    
    return spark

@task
def spark_etl_processing(spark: SparkSession, input_path: str, output_path: str):
    """Perform ETL processing using Spark."""
    # Read data
    df = spark.read.parquet(input_path)
    
    # Data transformations
    processed_df = df \
        .filter(col("status") == "active") \
        .withColumn("processed_amount", 
                   when(col("amount") > 1000, col("amount") * 0.9)
                   .otherwise(col("amount"))) \
        .groupBy("category") \
        .agg(spark_sum("processed_amount").alias("total_amount"))
    
    # Write results
    processed_df.write \
        .mode("overwrite") \
        .parquet(output_path)
    
    return processed_df.count()

@task
def cleanup_spark_session(spark: SparkSession):
    """Clean up Spark session."""
    spark.stop()

@flow
def spark_integration_flow(input_path: str, output_path: str):
    # Create Spark session
    spark = create_spark_session("Prefect-Spark-ETL")
    
    try:
        # Process data
        record_count = spark_etl_processing(spark, input_path, output_path)
        
        return {"status": "success", "records_processed": record_count}
    
    finally:
        # Always cleanup
        cleanup_spark_session(spark)
```

### Q53: How do you integrate Prefect with dbt for data transformation workflows?
**Answer:**
**dbt Integration:**

```python
from prefect import flow, task
import subprocess

@task
def run_dbt_command(command: str, project_dir: str) -> dict:
    """Execute dbt command and return results."""
    try:
        result = subprocess.run(
            f"dbt {command}",
            cwd=project_dir,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        
        return {
            "status": "success",
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except subprocess.CalledProcessError as e:
        return {
            "status": "failed",
            "stdout": e.stdout,
            "stderr": e.stderr,
            "return_code": e.returncode
        }

@task
def dbt_test_models(project_dir: str) -> dict:
    """Run dbt tests on models."""
    return run_dbt_command("test", project_dir)

@task
def dbt_run_models(project_dir: str, models: str = None) -> dict:
    """Run dbt models."""
    command = "run"
    if models:
        command += f" --models {models}"
    
    return run_dbt_command(command, project_dir)

@flow
def dbt_workflow(project_dir: str, target_models: str = None):
    """Complete dbt workflow with testing and documentation."""
    
    # Run dbt models
    run_result = dbt_run_models(project_dir, target_models)
    
    if run_result["status"] != "success":
        raise Exception(f"dbt run failed: {run_result['stderr']}")
    
    # Run tests
    test_result = dbt_test_models(project_dir)
    
    return {
        "models_run": run_result["status"] == "success",
        "tests_passed": test_result["status"] == "success"
    }
```

---

## Cloud Platform Integration

### Q54: How do you deploy Prefect workflows on AWS with ECS?
**Answer:**
**AWS ECS Deployment:**

```python
from prefect.deployments import Deployment
from prefect_aws.ecs import ECSTask
from prefect_aws.credentials import AwsCredentials

# Configure AWS credentials
aws_credentials = AwsCredentials(
    aws_access_key_id="your-access-key",
    aws_secret_access_key="your-secret-key",
    region_name="us-east-1"
)
aws_credentials.save("aws-creds")

# Configure ECS task
ecs_task = ECSTask(
    aws_credentials=aws_credentials,
    image="your-account.dkr.ecr.us-east-1.amazonaws.com/prefect-flows:latest",
    cluster="prefect-cluster",
    family="prefect-task-family",
    cpu=1024,
    memory=2048,
    execution_role_arn="arn:aws:iam::account:role/ecsTaskExecutionRole",
    task_role_arn="arn:aws:iam::account:role/ecsTaskRole",
    vpc_id="vpc-12345678",
    subnets=["subnet-12345678", "subnet-87654321"],
    security_groups=["sg-12345678"]
)
ecs_task.save("ecs-infrastructure")

# Create deployment
deployment = Deployment.build_from_flow(
    flow=my_production_flow,
    name="production-ecs-deployment",
    infrastructure=ecs_task,
    schedule=CronSchedule(cron="0 2 * * *"),
    work_queue_name="ecs-queue"
)

deployment.apply()
```

### Q55: How do you implement cost optimization strategies for Prefect workflows?
**Answer:**
**Cost Optimization Strategies:**

```python
from prefect import flow, task
from prefect.infrastructure import KubernetesJob
from datetime import datetime

@task
def cost_aware_processing(data_size: int, priority: str = "normal"):
    """Process data with cost-aware resource allocation."""
    if priority == "low" and data_size < 10000:
        # Use spot instances for low-priority, small jobs
        return process_on_spot_instance(data_size)
    elif data_size > 100000:
        # Use reserved instances for large, predictable workloads
        return process_on_reserved_instance(data_size)
    else:
        # Use on-demand for standard processing
        return process_on_demand(data_size)

@flow
def cost_optimized_flow(data_batches: list):
    # Schedule expensive operations during off-peak hours
    current_hour = datetime.now().hour
    
    if 2 <= current_hour <= 6:  # Off-peak hours
        # Use larger, more cost-effective instances
        infrastructure = KubernetesJob(
            cpu_request="4",
            memory_request="8Gi",
            node_selector={"instance-type": "spot"}
        )
    else:
        # Use smaller instances during peak hours
        infrastructure = KubernetesJob(
            cpu_request="1",
            memory_request="2Gi",
            node_selector={"instance-type": "on-demand"}
        )
    
    # Process batches with appropriate resources
    results = []
    for batch in data_batches:
        result = cost_aware_processing.with_options(
            infrastructure=infrastructure
        )(len(batch), priority="normal")
        results.append(result)
    
    return results
```

---

## Advanced Monitoring & Observability

### Q56: How do you implement custom metrics and monitoring in Prefect?
**Answer:**
**Custom Metrics Implementation:**

```python
from prefect import flow, task
from prefect.context import get_run_context
import time
import psutil

class PrefectMetricsCollector:
    def __init__(self):
        self.start_time = None
        self.metrics = {}
    
    def start_timer(self, metric_name: str):
        """Start timing a metric."""
        self.metrics[metric_name] = time.time()
    
    def end_timer(self, metric_name: str):
        """End timing and send metric."""
        if metric_name in self.metrics:
            duration = time.time() - self.metrics[metric_name]
            # Send to monitoring system
            send_metric(f'prefect.{metric_name}', duration)
            del self.metrics[metric_name]
    
    def gauge(self, metric_name: str, value: float):
        """Send gauge metric."""
        send_metric(f'prefect.{metric_name}', value)

# Global metrics collector
metrics = PrefectMetricsCollector()

@task
def monitored_data_processing(data: list) -> dict:
    """Data processing with comprehensive monitoring."""
    context = get_run_context()
    task_name = context.task_run.name
    
    # Start monitoring
    metrics.start_timer('task.execution_time')
    
    # Monitor system resources
    initial_memory = psutil.virtual_memory().percent
    
    try:
        # Process data
        processed_data = []
        for i, item in enumerate(data):
            processed_item = complex_processing(item)
            processed_data.append(processed_item)
            
            # Monitor progress
            if i % 1000 == 0:
                progress = (i / len(data)) * 100
                metrics.gauge('task.progress_percent', progress)
        
        # Success metrics
        metrics.gauge('task.records_processed', len(processed_data))
        
        return {
            'status': 'success',
            'records_processed': len(processed_data),
            'memory_delta': psutil.virtual_memory().percent - initial_memory
        }
    
    finally:
        # End monitoring
        metrics.end_timer('task.execution_time')

@flow
def comprehensive_monitoring_flow(data_batches: list):
    """Flow with comprehensive monitoring."""
    results = []
    for batch in data_batches:
        result = monitored_data_processing(batch)
        results.append(result)
    
    total_records = sum(r['records_processed'] for r in results)
    return {'status': 'success', 'total_records': total_records}
```

### Q57: How do you implement distributed tracing in Prefect workflows?
**Answer:**
**Distributed Tracing Implementation:**

```python
from prefect import flow, task
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
import uuid

# Configure OpenTelemetry
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure Jaeger exporter
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

@task
def traced_data_extraction(source: str, trace_id: str = None) -> dict:
    """Data extraction with distributed tracing."""
    with tracer.start_as_current_span("data_extraction") as span:
        # Add trace context
        span.set_attribute("source", source)
        span.set_attribute("trace_id", trace_id or str(uuid.uuid4()))
        
        try:
            # Simulate data extraction
            data = extract_data_from_source(source)
            
            # Add span attributes
            span.set_attribute("records_extracted", len(data))
            span.set_attribute("extraction_status", "success")
            
            return {
                'data': data,
                'trace_id': trace_id,
                'span_id': format(span.get_span_context().span_id, '016x')
            }
        
        except Exception as e:
            span.set_attribute("error", True)
            span.set_attribute("error_message", str(e))
            raise

@task
def traced_data_transformation(data_result: dict) -> dict:
    """Data transformation with trace propagation."""
    trace_id = data_result.get('trace_id')
    
    with tracer.start_as_current_span("data_transformation") as span:
        # Propagate trace context
        span.set_attribute("trace_id", trace_id)
        span.set_attribute("parent_span_id", data_result.get('span_id'))
        
        data = data_result['data']
        
        # Perform transformation
        transformed_data = [transform_record(record) for record in data]
        
        span.set_attribute("output_records", len(transformed_data))
        span.set_attribute("transformation_status", "success")
        
        return {
            'data': transformed_data,
            'trace_id': trace_id,
            'span_id': format(span.get_span_context().span_id, '016x')
        }

@flow
def distributed_tracing_flow(source: str, target: str):
    """Flow with distributed tracing."""
    # Generate trace ID for the entire flow
    flow_trace_id = str(uuid.uuid4())
    
    with tracer.start_as_current_span("etl_flow") as flow_span:
        flow_span.set_attribute("flow_trace_id", flow_trace_id)
        flow_span.set_attribute("source", source)
        flow_span.set_attribute("target", target)
        
        # Execute traced tasks
        extracted_data = traced_data_extraction(source, flow_trace_id)
        transformed_data = traced_data_transformation(extracted_data)
        
        flow_span.set_attribute("flow_status", "completed")
        
        return {
            'status': 'success',
            'flow_trace_id': flow_trace_id
        }
```

---

## Enterprise Features & Governance

### Q58: How do you implement role-based access control (RBAC) in Prefect?
**Answer:**
**RBAC Implementation:**

```python
from prefect import flow, task
from functools import wraps
from typing import List

class RoleManager:
    def __init__(self):
        self.roles = {
            'admin': ['read', 'write', 'execute', 'deploy', 'delete'],
            'developer': ['read', 'write', 'execute'],
            'analyst': ['read', 'execute'],
            'viewer': ['read']
        }
        
        self.user_roles = {
            'john.doe@company.com': ['admin'],
            'jane.smith@company.com': ['developer'],
            'analyst@company.com': ['analyst'],
            'viewer@company.com': ['viewer']
        }
    
    def get_user_permissions(self, user_email: str) -> List[str]:
        """Get all permissions for a user."""
        user_roles = self.user_roles.get(user_email, [])
        permissions = set()
        
        for role in user_roles:
            if role in self.roles:
                permissions.update(self.roles[role])
        
        return list(permissions)
    
    def has_permission(self, user_email: str, permission: str) -> bool:
        """Check if user has specific permission."""
        user_permissions = self.get_user_permissions(user_email)
        return permission in user_permissions

# Global role manager
role_manager = RoleManager()

def require_permission(permission: str):
    """Decorator to enforce permission requirements."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get user from context (in real implementation, from auth token)
            user_email = get_current_user_email()  # Custom function
            
            if not role_manager.has_permission(user_email, permission):
                raise PermissionError(f"User {user_email} lacks {permission} permission")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@task
@require_permission('read')
def read_sensitive_data(source: str) -> dict:
    """Read data - requires read permission."""
    return extract_data(source)

@task
@require_permission('write')
def write_processed_data(data: dict, target: str):
    """Write data - requires write permission."""
    load_data(data, target)

@flow
@require_permission('execute')
def rbac_protected_flow(source: str, target: str):
    """Flow with RBAC protection."""
    # Log access attempt
    user_email = get_current_user_email()
    logger = get_run_logger()
    logger.info(f"Flow executed by user: {user_email}")
    
    # Execute with permission checks
    data = read_sensitive_data(source)
    write_processed_data(data, target)
    
    return {"status": "success", "executed_by": user_email}
```

### Q59: How do you implement data lineage and governance in Prefect workflows?
**Answer:**
**Data Lineage and Governance:**

```python
from prefect import flow, task
from prefect.context import get_run_context
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class DataAsset:
    name: str
    type: str  # 'table', 'file', 'api', 'stream'
    location: str
    schema: Optional[Dict] = None
    tags: Optional[List[str]] = None
    sensitivity: str = 'public'  # 'public', 'internal', 'confidential', 'restricted'

@dataclass
class LineageRecord:
    source_assets: List[DataAsset]
    target_assets: List[DataAsset]
    transformation: str
    flow_run_id: str
    task_run_id: str
    timestamp: datetime
    user: str
    metadata: Optional[Dict] = None

class DataGovernanceManager:
    def __init__(self):
        self.lineage_records = []
        self.data_catalog = {}
        self.governance_rules = {
            'pii_detection': True,
            'data_retention': 365,  # days
            'encryption_required': ['confidential', 'restricted'],
            'audit_required': ['confidential', 'restricted']
        }
    
    def register_asset(self, asset: DataAsset):
        """Register data asset in catalog."""
        self.data_catalog[asset.name] = asset
    
    def record_lineage(self, lineage: LineageRecord):
        """Record data lineage."""
        self.lineage_records.append(lineage)
        # Store in persistent storage
        self.store_lineage_record(lineage)
    
    def check_governance_compliance(self, asset: DataAsset) -> Dict[str, bool]:
        """Check governance compliance for data asset."""
        compliance = {
            'encryption_compliant': True,
            'retention_compliant': True,
            'access_compliant': True,
            'audit_compliant': True
        }
        
        # Check encryption requirements
        if asset.sensitivity in self.governance_rules['encryption_required']:
            compliance['encryption_compliant'] = self.check_encryption(asset)
        
        return compliance
    
    def store_lineage_record(self, lineage: LineageRecord):
        """Store lineage record in persistent storage."""
        # Implementation would store in database/data catalog
        pass
    
    def check_encryption(self, asset: DataAsset) -> bool:
        """Check if asset is properly encrypted."""
        # Implementation would check encryption status
        return True

# Global governance manager
governance = DataGovernanceManager()

@task
def governed_data_extraction(source_config: dict) -> dict:
    """Data extraction with governance tracking."""
    context = get_run_context()
    
    # Register source asset
    source_asset = DataAsset(
        name=source_config['name'],
        type=source_config['type'],
        location=source_config['location'],
        sensitivity=source_config.get('sensitivity', 'internal'),
        tags=source_config.get('tags', [])
    )
    governance.register_asset(source_asset)
    
    # Check compliance
    compliance = governance.check_governance_compliance(source_asset)
    if not all(compliance.values()):
        raise Exception(f"Governance compliance failed: {compliance}")
    
    # Extract data
    data = extract_data(source_config['location'])
    
    # Record lineage
    lineage = LineageRecord(
        source_assets=[source_asset],
        target_assets=[],
        transformation="data_extraction",
        flow_run_id=context.flow_run.id,
        task_run_id=context.task_run.id,
        timestamp=datetime.now(),
        user=get_current_user_email(),
        metadata={"records_extracted": len(data)}
    )
    
    return {
        'data': data,
        'source_asset': source_asset,
        'lineage': lineage
    }

@flow
def data_governance_flow(source_config: dict, target_config: dict):
    """Flow with comprehensive data governance."""
    
    # Extract with governance
    extraction_result = governed_data_extraction(source_config)
    
    # Generate governance report
    governance_report = {
        'compliance_status': 'passed',
        'lineage_records': len(governance.lineage_records),
        'assets_registered': len(governance.data_catalog)
    }
    
    return {
        'status': 'success',
        'governance_report': governance_report
    }
```

---

## Real-World Scenarios

### Q60: How do you handle data pipeline failures and implement circuit breakers?
**Answer:**
**Circuit Breaker Pattern:**

```python
from prefect import flow, task
from enum import Enum
from datetime import datetime, timedelta

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open" # Testing if service recovered

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _should_attempt_reset(self):
        return (datetime.now() - self.last_failure_time).seconds >= self.timeout
    
    def _on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# Global circuit breakers
api_circuit_breaker = CircuitBreaker(failure_threshold=3, timeout=300)
db_circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=120)

@task(retries=0)  # Let circuit breaker handle retries
def resilient_api_call(endpoint: str):
    """API call with circuit breaker protection."""
    def make_api_call():
        import requests
        response = requests.get(endpoint, timeout=30)
        response.raise_for_status()
        return response.json()
    
    return api_circuit_breaker.call(make_api_call)

@task(retries=0)
def resilient_db_query(query: str):
    """Database query with circuit breaker protection."""
    def execute_query():
        connection = get_db_connection()
        return pd.read_sql(query, connection)
    
    return db_circuit_breaker.call(execute_query)

@flow
def resilient_data_pipeline():
    try:
        # Protected API call
        api_data = resilient_api_call("https://api.example.com/data")
        
        # Protected database query
        db_data = resilient_db_query("SELECT * FROM source_table")
        
        # Process data
        processed_data = process_data(api_data, db_data)
        
        return {"status": "success", "records": len(processed_data)}
        
    except Exception as e:
        # Fallback to cached data or alternative source
        logger = get_run_logger()
        logger.warning(f"Primary pipeline failed: {e}")
        
        fallback_data = get_cached_data()
        return {"status": "fallback", "records": len(fallback_data)}
```

### Q61: How do you implement data quality monitoring and alerting?
**Answer:**
**Data Quality Monitoring:**

```python
from prefect import flow, task
from dataclasses import dataclass
from typing import List, Dict
import pandas as pd

@dataclass
class DataQualityRule:
    name: str
    description: str
    severity: str  # 'critical', 'warning', 'info'
    threshold: float

class DataQualityMonitor:
    def __init__(self):
        self.rules = []
        self.results = []
    
    def check_completeness(self, df: pd.DataFrame, column: str, threshold: float) -> Dict:
        """Check data completeness."""
        null_percentage = df[column].isnull().sum() / len(df) * 100
        passed = null_percentage <= threshold
        
        return {
            'rule': 'completeness',
            'column': column,
            'value': null_percentage,
            'threshold': threshold,
            'passed': passed,
            'severity': 'critical' if not passed else 'info'
        }
    
    def check_uniqueness(self, df: pd.DataFrame, column: str, threshold: float) -> Dict:
        """Check data uniqueness."""
        duplicate_percentage = df[column].duplicated().sum() / len(df) * 100
        passed = duplicate_percentage <= threshold
        
        return {
            'rule': 'uniqueness',
            'column': column,
            'value': duplicate_percentage,
            'threshold': threshold,
            'passed': passed,
            'severity': 'warning' if not passed else 'info'
        }

@task
def run_data_quality_checks(df: pd.DataFrame, table_name: str) -> List[Dict]:
    """Run comprehensive data quality checks."""
    monitor = DataQualityMonitor()
    results = []
    
    # Completeness checks
    for column in df.columns:
        if df[column].dtype in ['object', 'string']:
            result = monitor.check_completeness(df, column, threshold=5.0)
            results.append(result)
    
    # Uniqueness checks for ID columns
    id_columns = [col for col in df.columns if 'id' in col.lower()]
    for column in id_columns:
        result = monitor.check_uniqueness(df, column, threshold=0.0)
        results.append(result)
    
    return results

@task
def send_quality_alerts(quality_results: List[Dict], table_name: str):
    """Send alerts for data quality issues."""
    critical_issues = [r for r in quality_results if r['severity'] == 'critical' and not r['passed']]
    warning_issues = [r for r in quality_results if r['severity'] == 'warning' and not r['passed']]
    
    if critical_issues:
        # Send immediate alert
        alert_message = f"CRITICAL: Data quality issues in {table_name}:\n"
        for issue in critical_issues:
            alert_message += f"- {issue['rule']} check failed for {issue['column']}\n"
        
        send_slack_alert(alert_message, channel="#data-alerts")
    
    if warning_issues:
        # Log warnings
        logger = get_run_logger()
        for issue in warning_issues:
            logger.warning(f"Data quality warning: {issue['rule']} issue in {issue['column']}")

@flow
def data_quality_monitoring_flow(table_name: str):
    # Extract data
    data = extract_table_data(table_name)
    
    # Run quality checks
    quality_results = run_data_quality_checks(data, table_name)
    
    # Send alerts if needed
    send_quality_alerts(quality_results, table_name)
    
    # Calculate overall quality score
    passed_checks = sum(1 for r in quality_results if r['passed'])
    total_checks = len(quality_results)
    quality_score = (passed_checks / total_checks) * 100 if total_checks > 0 else 100
    
    return {
        "table": table_name,
        "quality_score": quality_score,
        "total_checks": total_checks,
        "passed_checks": passed_checks
    }
```

### Q62: How do you implement disaster recovery for Prefect workflows?
**Answer:**
**Disaster Recovery Strategy:**

```python
from prefect import flow, task
from prefect.deployments import Deployment
from prefect.infrastructure import DockerContainer
import boto3
from datetime import datetime

class DisasterRecoveryManager:
    def __init__(self):
        self.primary_region = "us-east-1"
        self.backup_region = "us-west-2"
        self.s3_client = boto3.client('s3')
    
    def backup_flow_state(self, flow_run_id: str, state_data: dict):
        """Backup flow state to multiple regions."""
        backup_key = f"flow-states/{flow_run_id}/{datetime.now().isoformat()}.json"
        
        # Backup to primary region
        self.s3_client.put_object(
            Bucket=f"prefect-backup-{self.primary_region}",
            Key=backup_key,
            Body=json.dumps(state_data)
        )
        
        # Backup to secondary region
        backup_s3 = boto3.client('s3', region_name=self.backup_region)
        backup_s3.put_object(
            Bucket=f"prefect-backup-{self.backup_region}",
            Key=backup_key,
            Body=json.dumps(state_data)
        )
    
    def restore_flow_state(self, flow_run_id: str) -> dict:
        """Restore flow state from backup."""
        try:
            # Try primary region first
            response = self.s3_client.list_objects_v2(
                Bucket=f"prefect-backup-{self.primary_region}",
                Prefix=f"flow-states/{flow_run_id}/"
            )
        except Exception:
            # Fallback to backup region
            backup_s3 = boto3.client('s3', region_name=self.backup_region)
            response = backup_s3.list_objects_v2(
                Bucket=f"prefect-backup-{self.backup_region}",
                Prefix=f"flow-states/{flow_run_id}/"
            )
        
        # Get latest backup
        if 'Contents' in response:
            latest_backup = sorted(response['Contents'], key=lambda x: x['LastModified'])[-1]
            backup_data = self.s3_client.get_object(
                Bucket=f"prefect-backup-{self.primary_region}",
                Key=latest_backup['Key']
            )
            return json.loads(backup_data['Body'].read())
        
        return None

@task
def create_checkpoint(flow_run_id: str, checkpoint_data: dict):
    """Create recovery checkpoint."""
    dr_manager = DisasterRecoveryManager()
    dr_manager.backup_flow_state(flow_run_id, checkpoint_data)
    
    logger = get_run_logger()
    logger.info(f"Checkpoint created for flow run {flow_run_id}")

@flow
def disaster_recovery_flow(original_flow_run_id: str = None):
    """Disaster recovery workflow."""
    if original_flow_run_id:
        # Recovery mode
        logger = get_run_logger()
        logger.info(f"Starting disaster recovery for flow {original_flow_run_id}")
        
        # Restore state
        dr_manager = DisasterRecoveryManager()
        restored_state = dr_manager.restore_flow_state(original_flow_run_id)
        
        if restored_state:
            # Resume from checkpoint
            return resume_from_checkpoint(restored_state)
        else:
            # Full restart
            logger.warning("No checkpoint found, starting from beginning")
            return full_restart_flow()
    else:
        # Normal operation with checkpointing
        context = get_run_context()
        flow_run_id = context.flow_run.id
        
        # Step 1: Initial processing
        step1_result = initial_processing_step()
        create_checkpoint(flow_run_id, {"step": 1, "result": step1_result})
        
        # Step 2: Data transformation
        step2_result = data_transformation_step(step1_result)
        create_checkpoint(flow_run_id, {"step": 2, "result": step2_result})
        
        # Step 3: Final processing
        final_result = final_processing_step(step2_result)
        create_checkpoint(flow_run_id, {"step": 3, "result": final_result})
        
        return final_result
```

### Q63: How do you implement A/B testing workflows in Prefect?
**Answer:**
**A/B Testing Implementation:**

```python
from prefect import flow, task
import random
from typing import Dict, Any

class ABTestManager:
    def __init__(self):
        self.experiments = {}
    
    def create_experiment(self, name: str, variants: Dict[str, float]):
        """Create A/B test experiment with traffic allocation."""
        total_weight = sum(variants.values())
        normalized_variants = {k: v/total_weight for k, v in variants.items()}
        
        self.experiments[name] = {
            "variants": normalized_variants,
            "results": {variant: [] for variant in variants.keys()}
        }
    
    def assign_variant(self, experiment_name: str, user_id: str) -> str:
        """Assign user to experiment variant."""
        if experiment_name not in self.experiments:
            return "control"
        
        # Deterministic assignment based on user_id
        random.seed(hash(user_id) % 2**32)
        rand_val = random.random()
        
        cumulative_weight = 0
        variants = self.experiments[experiment_name]["variants"]
        
        for variant, weight in variants.items():
            cumulative_weight += weight
            if rand_val <= cumulative_weight:
                return variant
        
        return list(variants.keys())[0]  # Fallback

@flow
def ab_testing_flow(user_id: str, data: list):
    # Initialize A/B test
    ab_manager = ABTestManager()
    ab_manager.create_experiment(
        "algorithm_comparison",
        {"control": 0.5, "treatment": 0.5}
    )
    
    # Assign user to variant
    variant = ab_manager.assign_variant("algorithm_comparison", user_id)
    
    # Execute appropriate algorithm
    if variant == "treatment":
        result = algorithm_b_processing(data)
    else:
        result = algorithm_a_processing(data)
    
    return {**result, "variant": variant, "user_id": user_id}
```

---

## Performance Optimization & Scaling

### Q64: How do you optimize memory usage in Prefect workflows?
**Answer:**
**Memory Optimization Strategies:**

```python
from prefect import flow, task
import pandas as pd
from typing import Iterator

@task
def memory_efficient_processing(file_path: str, chunk_size: int = 10000) -> Iterator[pd.DataFrame]:
    """Process large files in chunks to manage memory."""
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        # Process chunk
        processed_chunk = transform_chunk(chunk)
        yield processed_chunk
        # Chunk goes out of scope and gets garbage collected

@task
def streaming_aggregation(chunks: Iterator[pd.DataFrame]) -> dict:
    """Aggregate data from chunks without loading all into memory."""
    total_records = 0
    sum_amount = 0
    
    for chunk in chunks:
        total_records += len(chunk)
        sum_amount += chunk['amount'].sum()
        # Process and discard chunk
    
    return {"total_records": total_records, "total_amount": sum_amount}

@task(cache_key_fn=None)  # Disable caching for memory-intensive tasks
def large_data_task():
    """Task that processes large data without caching."""
    # Process large dataset
    result = process_large_dataset()
    
    # Return only summary, not full data
    return {"status": "completed", "record_count": len(result)}

@flow
def memory_optimized_flow(file_path: str):
    # Process in chunks
    chunks = memory_efficient_processing(file_path)
    
    # Aggregate without loading all data
    summary = streaming_aggregation(chunks)
    
    return summary
```

### Q65: How do you implement parallel processing optimization in Prefect?
**Answer:**
**Parallel Processing Patterns:**

```python
from prefect import flow, task
from prefect.task_runners import ConcurrentTaskRunner
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import asyncio

@task
def cpu_intensive_task(data_chunk: list) -> list:
    """CPU-intensive task that benefits from process-based parallelism."""
    return [complex_computation(item) for item in data_chunk]

@task
def io_intensive_task(url: str) -> dict:
    """I/O-intensive task that benefits from thread-based parallelism."""
    import requests
    response = requests.get(url)
    return response.json()

@flow(task_runner=ConcurrentTaskRunner())
def optimized_parallel_flow(data_chunks: list, urls: list):
    # CPU-intensive tasks - use process pool
    cpu_results = cpu_intensive_task.map(data_chunks)
    
    # I/O-intensive tasks - use thread pool
    io_results = io_intensive_task.map(urls)
    
    # Combine results
    return combine_results(cpu_results, io_results)

# Custom task runner for specific optimization
class OptimizedTaskRunner(ConcurrentTaskRunner):
    def __init__(self):
        super().__init__()
        self.cpu_executor = ProcessPoolExecutor(max_workers=4)
        self.io_executor = ThreadPoolExecutor(max_workers=20)
    
    async def submit(self, key, call):
        # Route tasks to appropriate executor based on task type
        if "cpu_intensive" in key:
            return await asyncio.get_event_loop().run_in_executor(
                self.cpu_executor, call
            )
        else:
            return await asyncio.get_event_loop().run_in_executor(
                self.io_executor, call
            )
```

### Q66: How do you implement caching strategies for expensive operations?
**Answer:**
**Advanced Caching Strategies:**

```python
from prefect import task, flow
from prefect.tasks import task_input_hash
from datetime import timedelta
import hashlib
import json

def smart_cache_key(context, parameters):
    """Generate cache key based on data freshness requirements."""
    # Include date for daily refresh
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Hash parameters for uniqueness
    param_hash = hashlib.md5(
        json.dumps(parameters, sort_keys=True).encode()
    ).hexdigest()[:8]
    
    return f"{date_str}_{param_hash}"

def conditional_cache_key(context, parameters):
    """Cache key that considers data size for selective caching."""
    data_size = parameters.get('data_size', 0)
    
    # Only cache for large datasets
    if data_size > 100000:
        return task_input_hash(context, parameters)
    else:
        # No caching for small datasets
        return None

@task(
    cache_key_fn=smart_cache_key,
    cache_expiration=timedelta(hours=24),
    refresh_cache=False
)
def expensive_ml_training(dataset_path: str, model_params: dict):
    """Expensive ML training with smart caching."""
    # Load and train model
    model = train_model(dataset_path, model_params)
    return model

@task(
    cache_key_fn=conditional_cache_key,
    cache_expiration=timedelta(hours=6)
)
def adaptive_data_processing(data: list, data_size: int):
    """Processing with conditional caching based on data size."""
    return process_data(data)

# Cache warming strategy
@flow
def cache_warming_flow():
    """Pre-populate cache with commonly used results."""
    common_parameters = [
        {"dataset": "daily", "model": "regression"},
        {"dataset": "weekly", "model": "classification"},
        {"dataset": "monthly", "model": "clustering"}
    ]
    
    # Warm cache with common parameter combinations
    for params in common_parameters:
        expensive_ml_training(params["dataset"], {"type": params["model"]})
```

---

## Security & Compliance

### Q67: How do you implement secure credential management in Prefect?
**Answer:**
**Secure Credential Management:**

```python
from prefect.blocks.system import Secret
from prefect import flow, task
import os
from cryptography.fernet import Fernet

class SecureCredentialManager:
    def __init__(self):
        self.encryption_key = os.getenv("PREFECT_ENCRYPTION_KEY")
        self.cipher = Fernet(self.encryption_key) if self.encryption_key else None
    
    def encrypt_credential(self, credential: str) -> str:
        """Encrypt credential before storage."""
        if self.cipher:
            return self.cipher.encrypt(credential.encode()).decode()
        return credential
    
    def decrypt_credential(self, encrypted_credential: str) -> str:
        """Decrypt credential for use."""
        if self.cipher:
            return self.cipher.decrypt(encrypted_credential.encode()).decode()
        return encrypted_credential

@task
def secure_database_connection():
    """Establish database connection with secure credentials."""
    # Load encrypted credentials
    db_password = Secret.load("db-password-encrypted")
    
    # Decrypt for use
    credential_manager = SecureCredentialManager()
    decrypted_password = credential_manager.decrypt_credential(db_password.get())
    
    # Use credentials (never log them)
    connection = create_connection(
        host=os.getenv("DB_HOST"),
        username=os.getenv("DB_USER"),
        password=decrypted_password
    )
    
    return connection

@task
def audit_trail_task(operation: str, user: str, data_accessed: str):
    """Create audit trail for compliance."""
    audit_entry = {
        "timestamp": datetime.now().isoformat(),
        "operation": operation,
        "user": user,
        "data_accessed": data_accessed,
        "flow_run_id": get_run_context().flow_run.id
    }
    
    # Store in secure audit log
    store_audit_entry(audit_entry)

@flow
def compliant_data_flow(user_id: str):
    # Audit data access
    audit_trail_task("data_access", user_id, "customer_data")
    
    # Secure data processing
    connection = secure_database_connection()
    data = extract_data(connection)
    
    # Process with data masking
    masked_data = mask_sensitive_data(data)
    
    # Audit processing completion
    audit_trail_task("data_processing", user_id, "customer_data_processed")
    
    return masked_data
```

### Q68: How do you implement data privacy and GDPR compliance in Prefect?
**Answer:**
**GDPR Compliance Implementation:**

```python
from prefect import flow, task
from typing import List, Dict
import hashlib

@task
def anonymize_personal_data(data: pd.DataFrame, pii_columns: List[str]) -> pd.DataFrame:
    """Anonymize personally identifiable information."""
    anonymized_data = data.copy()
    
    for column in pii_columns:
        if column in anonymized_data.columns:
            # Hash PII data
            anonymized_data[column] = anonymized_data[column].apply(
                lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:16] if pd.notna(x) else x
            )
    
    return anonymized_data

@task
def data_retention_check(data: pd.DataFrame, retention_days: int) -> pd.DataFrame:
    """Filter data based on retention policy."""
    cutoff_date = datetime.now() - timedelta(days=retention_days)
    
    # Filter data within retention period
    if 'created_at' in data.columns:
        data['created_at'] = pd.to_datetime(data['created_at'])
        filtered_data = data[data['created_at'] >= cutoff_date]
        return filtered_data
    
    return data

@task
def consent_verification(user_ids: List[str]) -> List[str]:
    """Verify user consent for data processing."""
    consented_users = []
    
    for user_id in user_ids:
        # Check consent status
        consent_status = check_user_consent(user_id)
        if consent_status and consent_status.get('data_processing', False):
            consented_users.append(user_id)
    
    return consented_users

@task
def data_deletion_request(user_id: str) -> Dict:
    """Handle GDPR data deletion request."""
    deletion_results = {}
    
    # Delete from all relevant tables
    tables_to_clean = ['users', 'user_activities', 'user_preferences']
    
    for table in tables_to_clean:
        deleted_count = delete_user_data(table, user_id)
        deletion_results[table] = deleted_count
    
    # Log deletion for audit
    log_data_deletion(user_id, deletion_results)
    
    return deletion_results

@flow
def gdpr_compliant_processing_flow(user_ids: List[str]):
    # Verify consent
    consented_users = consent_verification(user_ids)
    
    if not consented_users:
        return {"status": "no_consent", "processed_users": 0}
    
    # Extract data for consented users only
    user_data = extract_user_data(consented_users)
    
    # Apply retention policy
    retained_data = data_retention_check(user_data, retention_days=365)
    
    # Anonymize PII
    pii_columns = ['email', 'phone', 'address']
    anonymized_data = anonymize_personal_data(retained_data, pii_columns)
    
    # Process anonymized data
    processed_data = process_data(anonymized_data)
    
    return {
        "status": "success",
        "processed_users": len(consented_users),
        "records_processed": len(processed_data)
    }
```

---

## Advanced Deployment Patterns

### Q69: How do you implement blue-green deployments with Prefect?
**Answer:**
**Blue-Green Deployment Strategy:**

```python
from prefect.deployments import Deployment
from prefect.infrastructure import DockerContainer

# Blue deployment (current production)
blue_deployment = Deployment.build_from_flow(
    flow=production_flow,
    name="production-blue",
    infrastructure=DockerContainer(
        image="myapp:v1.0",
        env={"ENVIRONMENT": "production", "VERSION": "blue"}
    ),
    work_queue_name="production-blue",
    is_schedule_active=True
)

# Green deployment (new version)
green_deployment = Deployment.build_from_flow(
    flow=production_flow,
    name="production-green",
    infrastructure=DockerContainer(
        image="myapp:v2.0",
        env={"ENVIRONMENT": "production", "VERSION": "green"}
    ),
    work_queue_name="production-green",
    is_schedule_active=False  # Initially inactive
)

# Deployment switching logic
@flow
def switch_deployment():
    # Validate green deployment
    if validate_green_deployment():
        # Activate green, deactivate blue
        activate_deployment("production-green")
        deactivate_deployment("production-blue")
    else:
        raise Exception("Green deployment validation failed")
```

### Q70: How do you implement canary deployments in Prefect?
**Answer:**
**Canary Deployment Pattern:**

```python
@flow
def canary_deployment_flow():
    # Route small percentage to canary
    canary_percentage = 10
    
    if random.randint(1, 100) <= canary_percentage:
        return canary_version_flow()
    else:
        return stable_version_flow()

# Gradual rollout
@flow
def gradual_rollout_flow():
    current_time = datetime.now().hour
    
    # Increase canary traffic over time
    if current_time < 6:  # Early morning
        canary_percentage = 5
    elif current_time < 12:  # Morning
        canary_percentage = 25
    elif current_time < 18:  # Afternoon
        canary_percentage = 50
    else:  # Evening
        canary_percentage = 100
    
    if random.randint(1, 100) <= canary_percentage:
        return new_version_flow()
    else:
        return current_version_flow()
```

---

## Summary

Prefect represents a modern approach to workflow orchestration with its hybrid execution model, Python-native development experience, and cloud-first architecture. Key strengths include dynamic workflow generation, excellent observability, and flexible deployment options. When evaluating Prefect, consider your team's Python expertise, workflow complexity requirements, and preference for modern development practices.

**Key Interview Topics Covered:**
- Core architecture and components (Q1-Q30)
- Advanced integration with Kafka, Spark, dbt (Q51-Q53)
- Cloud platform deployments (Q54-Q55)
- Custom monitoring and distributed tracing (Q56-Q57)
- Enterprise RBAC and data governance (Q58-Q59)
- Real-world scenarios and failure handling (Q60-Q63)
- Performance optimization and scaling (Q64-Q66)
- Security and compliance (Q67-Q68)
- Advanced deployment patterns (Q69-Q70)

This comprehensive set of 70 questions covers everything from basic concepts to advanced enterprise implementations, providing thorough preparation for Prefect-focused interviews.