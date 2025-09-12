# Dagster - Comprehensive Interview Questions

## 📋 Table of Contents

1. [Core Concepts](#core-concepts)
2. [Assets & Asset Materialization](#assets--asset-materialization)
3. [Jobs & Ops](#jobs--ops)
4. [Resources & Configuration](#resources--configuration)
5. [Schedules & Sensors](#schedules--sensors)
6. [Data Quality & Testing](#data-quality--testing)
7. [Partitions & Backfills](#partitions--backfills)
8. [Deployment & Operations](#deployment--operations)
9. [Integration & Ecosystem](#integration--ecosystem)
10. [Performance & Scaling](#performance--scaling)
11. [Best Practices](#best-practices)
12. [Comparison Questions](#comparison-questions)

---

## 🎯 **Introduction**

Dagster is a modern data orchestration platform that emphasizes asset-centric data pipelines with strong typing, testing, and observability. For data engineers, it provides a comprehensive framework for building reliable, maintainable data pipelines with built-in data quality checks and lineage tracking.

**Why Dagster is Critical for Data Engineers:**
- **Asset-Centric Approach**: Focus on data assets rather than tasks
- **Strong Typing**: Type-safe pipeline development
- **Built-in Testing**: Comprehensive testing framework
- **Data Lineage**: Automatic tracking of data dependencies
- **Observability**: Rich monitoring and debugging capabilities

---

## Core Concepts

### 1. What is Dagster and how does it differ from traditional workflow orchestration tools?

**Answer:**
Dagster is a data orchestration platform that takes an asset-centric approach to building data pipelines, focusing on the data assets being produced rather than the tasks that produce them.

**Key Differences:**

| Aspect | Traditional Tools | Dagster |
|--------|------------------|---------|
| **Focus** | Task-centric (what to do) | Asset-centric (what to produce) |
| **Type System** | Weak/no typing | Strong typing with runtime validation |
| **Testing** | External testing required | Built-in testing framework |
| **Data Lineage** | Manual tracking | Automatic lineage tracking |
| **Development** | Imperative workflows | Declarative asset definitions |

```python
# Traditional task-centric approach
def extract_task():
    return extract_data()

def transform_task(data):
    return transform_data(data)

# Dagster asset-centric approach
from dagster import asset

@asset
def raw_customers():
    """Raw customer data from source system."""
    return extract_customer_data()

@asset
def clean_customers(raw_customers):
    """Cleaned customer data with validation."""
    return clean_and_validate(raw_customers)

@asset
def customer_metrics(clean_customers):
    """Customer analytics metrics."""
    return calculate_metrics(clean_customers)
```

### 2. Explain Dagster's asset-centric philosophy and its benefits.

**Answer:**
Dagster's asset-centric approach treats data assets as first-class citizens, focusing on what data is being produced rather than how it's produced.

**Asset-Centric Benefits:**
- **Clear Data Lineage**: Automatic tracking of data dependencies
- **Better Testing**: Assets can be tested independently
- **Improved Observability**: Clear view of data pipeline health
- **Easier Debugging**: Focus on data quality issues
- **Reusability**: Assets can be shared across different jobs

```python
from dagster import asset, AssetIn
import pandas as pd

@asset
def sales_data():
    """Daily sales transactions."""
    return pd.read_sql("SELECT * FROM sales", connection)

@asset
def customer_data():
    """Customer information."""
    return pd.read_sql("SELECT * FROM customers", connection)

@asset(ins={"sales": AssetIn("sales_data"), "customers": AssetIn("customer_data")})
def customer_sales_summary(sales, customers):
    """Customer sales summary with enriched data."""
    return sales.merge(customers, on='customer_id').groupby('customer_id').agg({
        'amount': 'sum',
        'transaction_count': 'count'
    })

@asset
def high_value_customers(customer_sales_summary):
    """Customers with high lifetime value."""
    return customer_sales_summary[customer_sales_summary['amount'] > 10000]
```

### 3. What are the main components of Dagster architecture?

**Answer:**
**Core Components:**

1. **Assets**: Data artifacts produced by computations
2. **Ops**: Individual units of computation
3. **Jobs**: Collections of ops that execute together
4. **Resources**: External services and configurations
5. **Schedules**: Time-based execution triggers
6. **Sensors**: Event-based execution triggers
7. **Repositories**: Collections of assets, jobs, and schedules

```python
from dagster import (
    asset, op, job, resource, schedule, sensor, repository,
    RunRequest, SkipReason
)

# Resource
@resource
def database_connection():
    return create_db_connection()

# Asset
@asset(required_resource_keys={"database"})
def users_table(context):
    return context.resources.database.query("SELECT * FROM users")

# Op
@op
def process_data(data):
    return transform_data(data)

# Job
@job(resource_defs={"database": database_connection})
def data_pipeline():
    process_data(users_table())

# Schedule
@schedule(job=data_pipeline, cron_schedule="0 1 * * *")
def daily_schedule():
    return {}

# Repository
@repository
def my_repository():
    return [data_pipeline, daily_schedule]
```

---

## Assets & Asset Materialization

### 4. How do you define and materialize assets in Dagster?

**Answer:**
Assets in Dagster represent data artifacts that are produced by computations. They can be materialized (computed and stored) on demand or as part of scheduled jobs.

```python
from dagster import asset, AssetMaterialization, Output
import pandas as pd

# Basic asset definition
@asset
def daily_sales():
    """Daily sales data from the database."""
    df = pd.read_sql("""
        SELECT date, product_id, quantity, revenue
        FROM sales 
        WHERE date = CURRENT_DATE
    """, connection)
    return df

# Asset with dependencies
@asset
def sales_summary(daily_sales):
    """Aggregated sales summary."""
    return daily_sales.groupby('product_id').agg({
        'quantity': 'sum',
        'revenue': 'sum'
    }).reset_index()

# Asset with custom materialization
@asset
def processed_sales(daily_sales):
    """Processed sales data with custom materialization logic."""
    processed_df = apply_business_logic(daily_sales)
    
    # Custom materialization with metadata
    yield AssetMaterialization(
        asset_key="processed_sales",
        metadata={
            "num_records": len(processed_df),
            "data_quality_score": calculate_quality_score(processed_df),
            "processing_time": "2.3s"
        }
    )
    yield Output(processed_df)

# Asset with partitions
@asset(partitions_def=DailyPartitionsDefinition(start_date="2023-01-01"))
def partitioned_sales(context):
    """Sales data partitioned by date."""
    partition_date = context.asset_partition_key_for_output()
    return extract_sales_for_date(partition_date)
```

### 5. How do you handle asset dependencies and lineage in Dagster?

**Answer:**
Dagster automatically tracks asset dependencies and builds a lineage graph based on asset definitions.

```python
from dagster import asset, AssetIn, AssetOut, multi_asset
import pandas as pd

# Simple dependency
@asset
def raw_orders():
    return extract_orders()

@asset
def clean_orders(raw_orders):
    """Depends on raw_orders asset."""
    return clean_data(raw_orders)

# Multiple dependencies
@asset
def order_summary(clean_orders, customer_data):
    """Depends on both clean_orders and customer_data."""
    return clean_orders.merge(customer_data, on='customer_id')

# Explicit asset inputs
@asset(ins={"orders": AssetIn("clean_orders"), "customers": AssetIn("customer_data")})
def enriched_orders(orders, customers):
    """Explicitly defined asset dependencies."""
    return enrich_order_data(orders, customers)

# Multi-asset with multiple outputs
@multi_asset(
    outs={
        "orders_fact": AssetOut(),
        "customers_dim": AssetOut(),
        "products_dim": AssetOut()
    }
)
def dimensional_model(raw_data):
    """Create multiple related assets from single computation."""
    orders_fact = create_orders_fact(raw_data)
    customers_dim = create_customers_dimension(raw_data)
    products_dim = create_products_dimension(raw_data)
    
    return orders_fact, customers_dim, products_dim

# Asset with external dependencies
@asset(non_argument_deps={"external_system_data"})
def processed_external_data():
    """Asset that depends on external system data."""
    # This asset depends on external_system_data but doesn't receive it as argument
    return process_external_data()
```

### 6. How do you implement asset groups and organize large numbers of assets?

**Answer:**
Asset groups help organize and manage large numbers of assets by grouping related assets together.

```python
from dagster import asset, AssetGroup, AssetIn

# Define assets with groups
@asset(group_name="raw_data")
def raw_customers():
    return extract_customers()

@asset(group_name="raw_data")
def raw_orders():
    return extract_orders()

@asset(group_name="staging")
def staging_customers(raw_customers):
    return clean_customers(raw_customers)

@asset(group_name="staging")
def staging_orders(raw_orders):
    return clean_orders(raw_orders)

@asset(group_name="marts")
def customer_metrics(staging_customers, staging_orders):
    return calculate_customer_metrics(staging_customers, staging_orders)

# Programmatic asset group creation
raw_data_assets = [raw_customers, raw_orders]
staging_assets = [staging_customers, staging_orders]
marts_assets = [customer_metrics]

# Asset selection by group
from dagster import define_asset_job

# Job that materializes only staging assets
staging_job = define_asset_job(
    name="staging_job",
    selection="staging*"  # Select all assets in staging group
)

# Job that materializes downstream of raw_data
downstream_job = define_asset_job(
    name="downstream_job",
    selection="raw_data*+"  # Select raw_data assets and all downstream
)
```

---

## Jobs & Ops

### 7. What's the difference between ops and assets in Dagster?

**Answer:**
**Ops vs Assets:**

| Aspect | Ops | Assets |
|--------|-----|--------|
| **Purpose** | Units of computation | Data artifacts |
| **Focus** | How to compute | What to produce |
| **Composition** | Combined into jobs | Form dependency graphs |
| **Testing** | Function-level testing | Asset-level testing |
| **Reusability** | Reusable across jobs | Reusable across contexts |

```python
from dagster import op, job, asset, In, Out

# Op-based approach (traditional)
@op(ins={"raw_data": In()}, out=Out())
def clean_data_op(raw_data):
    """Op that cleans data."""
    return clean_data(raw_data)

@op(ins={"clean_data": In()}, out=Out())
def analyze_data_op(clean_data):
    """Op that analyzes data."""
    return analyze_data(clean_data)

@job
def data_processing_job():
    """Job composed of ops."""
    clean = clean_data_op()
    analyze_data_op(clean)

# Asset-based approach (modern)
@asset
def raw_data():
    """Raw data asset."""
    return extract_data()

@asset
def clean_data(raw_data):
    """Clean data asset."""
    return clean_data(raw_data)

@asset
def analysis_results(clean_data):
    """Analysis results asset."""
    return analyze_data(clean_data)

# Assets can be materialized in jobs
from dagster import define_asset_job

asset_job = define_asset_job(
    name="asset_materialization_job",
    selection=[raw_data, clean_data, analysis_results]
)
```

### 8. How do you create and configure jobs in Dagster?

**Answer:**
Jobs in Dagster define a set of ops or assets that should be executed together.

```python
from dagster import job, op, resource, config_schema, In, Out

# Resource definition
@resource(config_schema={"connection_string": str})
def database_resource(context):
    return create_connection(context.resource_config["connection_string"])

# Op definitions
@op(required_resource_keys={"database"})
def extract_op(context):
    """Extract data using database resource."""
    return context.resources.database.query("SELECT * FROM source_table")

@op
def transform_op(data):
    """Transform the extracted data."""
    return transform_data(data)

@op(required_resource_keys={"database"})
def load_op(context, data):
    """Load transformed data."""
    context.resources.database.insert("target_table", data)

# Job definition
@job(
    resource_defs={"database": database_resource},
    config={
        "resources": {
            "database": {
                "config": {
                    "connection_string": "postgresql://localhost:5432/mydb"
                }
            }
        }
    }
)
def etl_job():
    """ETL job with resource configuration."""
    raw_data = extract_op()
    transformed_data = transform_op(raw_data)
    load_op(transformed_data)

# Job with op configuration
@op(config_schema={"batch_size": int})
def configurable_op(context):
    batch_size = context.op_config["batch_size"]
    return process_in_batches(batch_size)

@job
def configurable_job():
    configurable_op()

# Asset-based job
from dagster import define_asset_job

asset_based_job = define_asset_job(
    name="daily_assets",
    selection="*daily*",  # Select assets with 'daily' in name
    config={
        "execution": {
            "multiprocess": {
                "max_concurrent": 4
            }
        }
    }
)
```

---

## Resources & Configuration

### 9. How do you manage resources and configuration in Dagster?

**Answer:**
Resources in Dagster provide a way to manage external dependencies and configuration in a reusable, testable manner.

```python
from dagster import resource, job, op, config_schema
import boto3
import pandas as pd

# Database resource
@resource(config_schema={"host": str, "port": int, "database": str})
def postgres_resource(context):
    """PostgreSQL database resource."""
    config = context.resource_config
    return create_postgres_connection(
        host=config["host"],
        port=config["port"],
        database=config["database"]
    )

# S3 resource
@resource(config_schema={"bucket": str, "region": str})
def s3_resource(context):
    """AWS S3 resource."""
    config = context.resource_config
    return boto3.client(
        's3',
        region_name=config["region"]
    )

# API client resource
@resource(config_schema={"api_key": str, "base_url": str})
def api_client_resource(context):
    """External API client resource."""
    config = context.resource_config
    return APIClient(
        api_key=config["api_key"],
        base_url=config["base_url"]
    )

# Op using multiple resources
@op(required_resource_keys={"database", "s3", "api"})
def data_pipeline_op(context):
    """Op that uses multiple resources."""
    # Get data from API
    api_data = context.resources.api.get_data()
    
    # Process data
    processed_data = process_api_data(api_data)
    
    # Save to S3
    context.resources.s3.put_object(
        Bucket="data-bucket",
        Key="processed_data.json",
        Body=processed_data
    )
    
    # Save metadata to database
    context.resources.database.execute(
        "INSERT INTO processing_log (timestamp, records) VALUES (%s, %s)",
        (datetime.now(), len(processed_data))
    )

# Job with resource configuration
@job(
    resource_defs={
        "database": postgres_resource,
        "s3": s3_resource,
        "api": api_client_resource
    }
)
def multi_resource_job():
    data_pipeline_op()

# Environment-specific resource modes
from dagster import ModeDefinition

dev_mode = ModeDefinition(
    name="dev",
    resource_defs={
        "database": postgres_resource.configured({
            "host": "localhost",
            "port": 5432,
            "database": "dev_db"
        }),
        "s3": s3_resource.configured({
            "bucket": "dev-bucket",
            "region": "us-east-1"
        })
    }
)

prod_mode = ModeDefinition(
    name="prod",
    resource_defs={
        "database": postgres_resource.configured({
            "host": "prod-db.company.com",
            "port": 5432,
            "database": "prod_db"
        }),
        "s3": s3_resource.configured({
            "bucket": "prod-bucket",
            "region": "us-west-2"
        })
    }
)

@job(mode_defs=[dev_mode, prod_mode])
def environment_aware_job():
    data_pipeline_op()
```

### 10. How do you implement configuration and secrets management?

**Answer:**
Dagster provides multiple approaches for configuration and secrets management.

```python
from dagster import resource, StringSource, IntSource
import os

# Resource with environment-based configuration
@resource(
    config_schema={
        "host": StringSource,
        "port": IntSource,
        "username": StringSource,
        "password": StringSource
    }
)
def database_resource(context):
    """Database resource with configurable connection."""
    config = context.resource_config
    return create_connection(
        host=config["host"],
        port=config["port"],
        username=config["username"],
        password=config["password"]
    )

# Configuration using environment variables
database_config = {
    "resources": {
        "database": {
            "config": {
                "host": {"env": "DB_HOST"},
                "port": {"env": "DB_PORT"},
                "username": {"env": "DB_USERNAME"},
                "password": {"env": "DB_PASSWORD"}
            }
        }
    }
}

# Secrets management with external providers
@resource(config_schema={"secret_name": str})
def secret_manager_resource(context):
    """Resource that fetches secrets from external provider."""
    secret_name = context.resource_config["secret_name"]
    
    # Fetch from AWS Secrets Manager
    secret_value = get_secret_from_aws(secret_name)
    
    return create_connection_with_secret(secret_value)

# Configuration presets
from dagster import PresetDefinition

dev_preset = PresetDefinition(
    name="dev",
    run_config={
        "resources": {
            "database": {
                "config": {
                    "host": "localhost",
                    "port": 5432,
                    "username": "dev_user",
                    "password": "dev_password"
                }
            }
        }
    }
)

prod_preset = PresetDefinition(
    name="prod",
    run_config={
        "resources": {
            "database": {
                "config": {
                    "host": {"env": "PROD_DB_HOST"},
                    "port": {"env": "PROD_DB_PORT"},
                    "username": {"env": "PROD_DB_USERNAME"},
                    "password": {"env": "PROD_DB_PASSWORD"}
                }
            }
        }
    }
)

@job(
    resource_defs={"database": database_resource},
    preset_defs=[dev_preset, prod_preset]
)
def configurable_job():
    data_processing_op()
```

---

## Schedules & Sensors

### 11. How do you implement scheduling in Dagster?

**Answer:**
Dagster provides schedules for time-based execution and sensors for event-based execution.

```python
from dagster import schedule, job, sensor, RunRequest, SkipReason
from dagster.core.definitions.partition import StaticPartitionsDefinition

# Basic time-based schedule
@schedule(job=daily_job, cron_schedule="0 1 * * *")
def daily_schedule():
    """Run daily job at 1 AM."""
    return {}

# Schedule with configuration
@schedule(job=etl_job, cron_schedule="0 */6 * * *")
def hourly_etl_schedule(context):
    """Run ETL job every 6 hours with dynamic config."""
    return {
        "ops": {
            "extract_op": {
                "config": {
                    "batch_size": 1000,
                    "start_time": context.scheduled_execution_time.isoformat()
                }
            }
        }
    }

# Partition-based schedule
from dagster import DailyPartitionsDefinition

daily_partitions = DailyPartitionsDefinition(start_date="2023-01-01")

@asset(partitions_def=daily_partitions)
def daily_sales_asset(context):
    partition_date = context.asset_partition_key_for_output()
    return extract_sales_for_date(partition_date)

@schedule(
    job=define_asset_job("daily_sales_job", [daily_sales_asset]),
    cron_schedule="0 2 * * *"
)
def daily_sales_schedule(context):
    """Schedule that creates partition runs."""
    # Get yesterday's partition
    yesterday = (context.scheduled_execution_time - timedelta(days=1)).strftime("%Y-%m-%d")
    
    return RunRequest(
        partition_key=yesterday,
        tags={"partition_date": yesterday}
    )

# Multiple run requests from single schedule
@schedule(job=backfill_job, cron_schedule="0 3 * * 0")  # Weekly on Sunday
def weekly_backfill_schedule(context):
    """Weekly schedule that creates multiple run requests."""
    run_requests = []
    
    # Create run requests for each day of the previous week
    for i in range(7):
        date = (context.scheduled_execution_time - timedelta(days=i+1)).strftime("%Y-%m-%d")
        run_requests.append(
            RunRequest(
                partition_key=date,
                tags={"backfill_date": date, "type": "weekly_backfill"}
            )
        )
    
    return run_requests
```

### 12. How do you implement sensors for event-driven execution?

**Answer:**
Sensors allow you to trigger job runs based on external events or conditions.

```python
from dagster import sensor, RunRequest, SkipReason, DefaultSensorStatus
import os
import boto3

# File-based sensor
@sensor(job=process_file_job)
def file_sensor(context):
    """Sensor that triggers when new files appear."""
    files_to_process = []
    
    # Check for new files in directory
    input_dir = "/data/input"
    for filename in os.listdir(input_dir):
        if filename.endswith('.csv') and not filename.startswith('processed_'):
            files_to_process.append(filename)
    
    if not files_to_process:
        return SkipReason("No new files to process")
    
    # Create run request for each file
    run_requests = []
    for filename in files_to_process:
        run_requests.append(
            RunRequest(
                run_key=filename,
                run_config={
                    "ops": {
                        "process_file_op": {
                            "config": {"filename": filename}
                        }
                    }
                },
                tags={"filename": filename}
            )
        )
    
    return run_requests

# S3 sensor
@sensor(job=s3_processing_job)
def s3_sensor(context):
    """Sensor that monitors S3 bucket for new objects."""
    s3_client = boto3.client('s3')
    bucket_name = "data-input-bucket"
    
    # Get cursor from previous run
    cursor = context.cursor or "2023-01-01T00:00:00Z"
    
    # List objects modified after cursor
    response = s3_client.list_objects_v2(
        Bucket=bucket_name,
        Prefix="input/",
        StartAfter=cursor
    )
    
    if 'Contents' not in response:
        return SkipReason("No new objects in S3 bucket")
    
    new_objects = [
        obj for obj in response['Contents']
        if obj['LastModified'].isoformat() > cursor
    ]
    
    if not new_objects:
        return SkipReason("No new objects since last check")
    
    # Update cursor to latest object timestamp
    latest_timestamp = max(obj['LastModified'] for obj in new_objects).isoformat()
    context.update_cursor(latest_timestamp)
    
    # Create run requests
    run_requests = []
    for obj in new_objects:
        run_requests.append(
            RunRequest(
                run_key=obj['Key'],
                run_config={
                    "resources": {
                        "s3": {
                            "config": {
                                "bucket": bucket_name,
                                "key": obj['Key']
                            }
                        }
                    }
                },
                tags={"s3_key": obj['Key'], "size": str(obj['Size'])}
            )
        )
    
    return run_requests

# Database sensor
@sensor(job=data_quality_job, default_status=DefaultSensorStatus.RUNNING)
def data_quality_sensor(context):
    """Sensor that monitors data quality metrics."""
    # Check data quality metrics
    quality_issues = check_data_quality_metrics()
    
    if not quality_issues:
        return SkipReason("No data quality issues detected")
    
    # Trigger data quality job for each issue
    run_requests = []
    for issue in quality_issues:
        run_requests.append(
            RunRequest(
                run_key=f"quality_issue_{issue['id']}",
                run_config={
                    "ops": {
                        "investigate_quality_op": {
                            "config": {
                                "issue_id": issue['id'],
                                "severity": issue['severity']
                            }
                        }
                    }
                },
                tags={
                    "issue_type": issue['type'],
                    "severity": issue['severity']
                }
            )
        )
    
    return run_requests

# Asset sensor
from dagster import asset_sensor, EventLogEntry

@asset_sensor(asset_key="raw_data", job=downstream_processing_job)
def raw_data_sensor(context, asset_event: EventLogEntry):
    """Sensor that triggers when raw_data asset is materialized."""
    # Get the materialization event
    materialization = asset_event.dagster_event.event_specific_data.materialization
    
    # Check if we should trigger downstream processing
    metadata = materialization.metadata_entries
    record_count = next(
        (entry.value for entry in metadata if entry.label == "record_count"),
        0
    )
    
    if record_count < 1000:
        return SkipReason(f"Not enough records ({record_count}) to trigger processing")
    
    return RunRequest(
        run_key=f"process_{asset_event.run_id}",
        tags={
            "source_run_id": asset_event.run_id,
            "record_count": str(record_count)
        }
    )
```

---

## Data Quality & Testing

### 13. How do you implement data quality checks and testing in Dagster?

**Answer:**
Dagster provides comprehensive testing capabilities including unit tests, integration tests, and data quality assertions.

```python
from dagster import asset, AssetCheckResult, AssetCheckSeverity, asset_check
import pandas as pd
import pytest

# Asset with built-in data quality checks
@asset
def customer_data():
    """Customer data with quality validations."""
    df = pd.read_sql("SELECT * FROM customers", connection)
    
    # Data quality validations
    assert not df.empty, "Customer data should not be empty"
    assert df['customer_id'].is_unique, "Customer IDs should be unique"
    assert df['email'].notna().all(), "All customers should have email addresses"
    
    return df

# Asset checks (Dagster 1.5+)
@asset_check(asset="customer_data")
def customer_data_completeness_check(customer_data):
    """Check completeness of customer data."""
    total_records = len(customer_data)
    complete_records = customer_data.dropna().shape[0]
    completeness_ratio = complete_records / total_records
    
    if completeness_ratio < 0.95:
        return AssetCheckResult(
            passed=False,
            severity=AssetCheckSeverity.WARN,
            metadata={
                "completeness_ratio": completeness_ratio,
                "total_records": total_records,
                "incomplete_records": total_records - complete_records
            }
        )
    
    return AssetCheckResult(
        passed=True,
        metadata={"completeness_ratio": completeness_ratio}
    )

@asset_check(asset="customer_data")
def customer_data_freshness_check(customer_data):
    """Check freshness of customer data."""
    if 'updated_at' in customer_data.columns:
        latest_update = customer_data['updated_at'].max()
        hours_since_update = (datetime.now() - latest_update).total_seconds() / 3600
        
        if hours_since_update > 24:
            return AssetCheckResult(
                passed=False,
                severity=AssetCheckSeverity.ERROR,
                metadata={"hours_since_update": hours_since_update}
            )
    
    return AssetCheckResult(passed=True)

# Unit testing assets
def test_customer_data_processing():
    """Unit test for customer data processing logic."""
    # Mock input data
    mock_data = pd.DataFrame({
        'customer_id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'email': ['alice@test.com', 'bob@test.com', 'charlie@test.com']
    })
    
    # Test the processing logic
    result = process_customer_data(mock_data)
    
    # Assertions
    assert len(result) == 3
    assert 'customer_id' in result.columns
    assert result['customer_id'].is_unique

# Integration testing with Dagster test utilities
from dagster import materialize

def test_customer_pipeline_integration():
    """Integration test for customer data pipeline."""
    # Materialize assets in test environment
    result = materialize([customer_data, customer_metrics])
    
    # Check that materialization was successful
    assert result.success
    
    # Verify asset outputs
    customer_data_output = result.asset_value(customer_data.key)
    assert not customer_data_output.empty
    assert 'customer_id' in customer_data_output.columns

# Data quality monitoring asset
@asset
def data_quality_report(customer_data, order_data):
    """Generate data quality report for all datasets."""
    quality_metrics = {}
    
    # Customer data quality
    quality_metrics['customer_data'] = {
        'record_count': len(customer_data),
        'null_percentage': customer_data.isnull().sum().sum() / customer_data.size,
        'duplicate_count': customer_data.duplicated().sum()
    }
    
    # Order data quality
    quality_metrics['order_data'] = {
        'record_count': len(order_data),
        'null_percentage': order_data.isnull().sum().sum() / order_data.size,
        'invalid_amounts': (order_data['amount'] < 0).sum()
    }
    
    return quality_metrics

# Custom data quality framework
class DataQualityCheck:
    def __init__(self, name, check_function, severity="ERROR"):
        self.name = name
        self.check_function = check_function
        self.severity = severity
    
    def run(self, data):
        try:
            result = self.check_function(data)
            return {
                'check_name': self.name,
                'passed': result,
                'severity': self.severity
            }
        except Exception as e:
            return {
                'check_name': self.name,
                'passed': False,
                'error': str(e),
                'severity': 'ERROR'
            }

def apply_quality_checks(data, checks):
    """Apply multiple data quality checks."""
    results = []
    for check in checks:
        results.append(check.run(data))
    return results

@asset
def validated_sales_data(raw_sales_data):
    """Sales data with comprehensive quality checks."""
    # Define quality checks
    quality_checks = [
        DataQualityCheck("non_empty", lambda df: not df.empty),
        DataQualityCheck("unique_ids", lambda df: df['sale_id'].is_unique),
        DataQualityCheck("positive_amounts", lambda df: (df['amount'] > 0).all()),
        DataQualityCheck("valid_dates", lambda df: pd.to_datetime(df['sale_date'], errors='coerce').notna().all())
    ]
    
    # Run quality checks
    check_results = apply_quality_checks(raw_sales_data, quality_checks)
    
    # Log results
    failed_checks = [r for r in check_results if not r['passed']]
    if failed_checks:
        raise ValueError(f"Data quality checks failed: {failed_checks}")
    
    return raw_sales_data
```

---

## Partitions & Backfills

### 14. How do you implement partitioned assets and backfills in Dagster?

**Answer:**
Partitions in Dagster allow you to process data in discrete chunks, enabling efficient backfills and incremental processing.

```python
from dagster import (
    asset, DailyPartitionsDefinition, MonthlyPartitionsDefinition,
    StaticPartitionsDefinition, MultiPartitionsDefinition,
    MultiPartitionKey, define_asset_job
)
import pandas as pd
from datetime import datetime, timedelta

# Daily partitioned asset
daily_partitions = DailyPartitionsDefinition(start_date="2023-01-01")

@asset(partitions_def=daily_partitions)
def daily_sales(context):
    """Daily sales data partitioned by date."""
    partition_date = context.asset_partition_key_for_output()
    
    # Extract data for specific date
    df = pd.read_sql(f"""
        SELECT * FROM sales 
        WHERE DATE(created_at) = '{partition_date}'
    """, connection)
    
    context.log.info(f"Processed {len(df)} sales records for {partition_date}")
    return df

@asset(partitions_def=daily_partitions)
def daily_sales_summary(context, daily_sales):
    """Daily sales summary derived from daily sales."""
    partition_date = context.asset_partition_key_for_output()
    
    summary = daily_sales.groupby('product_id').agg({
        'quantity': 'sum',
        'revenue': 'sum'
    }).reset_index()
    
    summary['date'] = partition_date
    return summary

# Monthly partitioned asset
monthly_partitions = MonthlyPartitionsDefinition(start_date="2023-01-01")

@asset(partitions_def=monthly_partitions)
def monthly_sales_report(context, daily_sales_summary):
    """Monthly sales report aggregating daily summaries."""
    partition_month = context.asset_partition_key_for_output()
    
    # Get all daily summaries for the month
    month_start = datetime.strptime(partition_month, "%Y-%m-%d")
    month_end = month_start.replace(day=28) + timedelta(days=4)
    month_end = month_end - timedelta(days=month_end.day)
    
    # Aggregate daily data for the month
    monthly_summary = aggregate_daily_to_monthly(daily_sales_summary, month_start, month_end)
    return monthly_summary

# Multi-dimensional partitions
region_partitions = StaticPartitionsDefinition(["US", "EU", "APAC"])
multi_partitions = MultiPartitionsDefinition({
    "date": daily_partitions,
    "region": region_partitions
})

@asset(partitions_def=multi_partitions)
def regional_daily_sales(context):
    """Sales data partitioned by both date and region."""
    partition_key = context.asset_partition_key_for_output()
    
    if isinstance(partition_key, MultiPartitionKey):
        date = partition_key.keys_by_dimension["date"]
        region = partition_key.keys_by_dimension["region"]
    else:
        # Handle string partition key
        date, region = partition_key.split("|")
    
    df = pd.read_sql(f"""
        SELECT * FROM sales 
        WHERE DATE(created_at) = '{date}' 
        AND region = '{region}'
    """, connection)
    
    return df

# Backfill job for partitioned assets
backfill_job = define_asset_job(
    name="sales_backfill",
    selection=[daily_sales, daily_sales_summary],
    partitions_def=daily_partitions
)

# Custom partition definition
class HourlyPartitionsDefinition:
    def __init__(self, start_datetime, end_datetime=None):
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime or datetime.now()
    
    def get_partition_keys(self):
        """Generate hourly partition keys."""
        keys = []
        current = self.start_datetime
        while current <= self.end_datetime:
            keys.append(current.strftime("%Y-%m-%d-%H"))
            current += timedelta(hours=1)
        return keys

hourly_partitions = HourlyPartitionsDefinition(
    start_datetime=datetime(2023, 1, 1, 0),
    end_datetime=datetime(2023, 1, 2, 0)
)

@asset(partitions_def=hourly_partitions)
def hourly_metrics(context):
    """Hourly metrics with custom partition definition."""
    partition_hour = context.asset_partition_key_for_output()
    
    # Process data for specific hour
    hour_data = extract_hourly_data(partition_hour)
    return calculate_hourly_metrics(hour_data)

# Partition mapping for dependencies
from dagster import PartitionMapping

class DailyToMonthlyPartitionMapping(PartitionMapping):
    """Map daily partitions to monthly partitions."""
    
    def get_upstream_partitions_for_partition_range(
        self, downstream_partition_subset, upstream_partitions_def
    ):
        # Convert monthly partition to daily partitions
        monthly_keys = downstream_partition_subset.get_partition_keys()
        daily_keys = []
        
        for monthly_key in monthly_keys:
            month_start = datetime.strptime(monthly_key, "%Y-%m-%d")
            # Get all days in the month
            current_day = month_start
            while current_day.month == month_start.month:
                daily_keys.append(current_day.strftime("%Y-%m-%d"))
                current_day += timedelta(days=1)
        
        return upstream_partitions_def.subset_with_partition_keys(daily_keys)

@asset(
    partitions_def=monthly_partitions,
    ins={
        "daily_data": AssetIn(
            partition_mapping=DailyToMonthlyPartitionMapping()
        )
    }
)
def monthly_aggregated_data(daily_data):
    """Monthly data aggregated from daily partitions."""
    return aggregate_daily_data(daily_data)
```

### 15. How do you handle backfills and historical data processing?

**Answer:**
Dagster provides powerful backfill capabilities for processing historical data efficiently.

```python
from dagster import (
    asset, job, op, BackfillPolicy, 
    define_asset_job, DagsterInstance
)

# Asset with backfill policy
@asset(
    partitions_def=daily_partitions,
    backfill_policy=BackfillPolicy.single_run()
)
def efficient_daily_processing(context):
    """Asset optimized for backfill processing."""
    partition_date = context.asset_partition_key_for_output()
    
    # Efficient processing for backfills
    if context.is_subset:
        # Process multiple partitions efficiently
        return process_multiple_dates_efficiently(context.asset_partition_keys_for_output())
    else:
        # Process single partition
        return process_single_date(partition_date)

# Backfill with chunking
@asset(
    partitions_def=daily_partitions,
    backfill_policy=BackfillPolicy.multi_run(max_partitions_per_run=7)
)
def weekly_chunked_processing(context):
    """Process data in weekly chunks during backfills."""
    partition_dates = context.asset_partition_keys_for_output()
    
    # Process all partitions in the chunk together
    return process_date_range(min(partition_dates), max(partition_dates))

# Programmatic backfill execution
def run_backfill(asset_selection, partition_range):
    """Programmatically execute backfill."""
    instance = DagsterInstance.get()
    
    # Create backfill job
    backfill_job = define_asset_job(
        name="backfill_job",
        selection=asset_selection,
        partitions_def=daily_partitions
    )
    
    # Submit backfill
    backfill_id = instance.create_backfill(
        backfill_job,
        partition_names=partition_range,
        asset_selection=asset_selection
    )
    
    return backfill_id

# Incremental backfill with state tracking
@asset(partitions_def=daily_partitions)
def incremental_processing(context):
    """Incremental processing that tracks state."""
    partition_date = context.asset_partition_key_for_output()
    
    # Check if partition already processed
    if is_partition_processed(partition_date):
        context.log.info(f"Partition {partition_date} already processed, skipping")
        return load_existing_data(partition_date)
    
    # Process new data
    data = extract_and_process_data(partition_date)
    
    # Mark partition as processed
    mark_partition_processed(partition_date)
    
    return data

# Backfill monitoring and alerting
@op
def monitor_backfill_progress(context):
    """Monitor backfill progress and send alerts."""
    instance = DagsterInstance.get()
    
    # Get active backfills
    backfills = instance.get_backfills()
    
    for backfill in backfills:
        if backfill.status == "RUNNING":
            progress = calculate_backfill_progress(backfill)
            
            if progress['failed_partitions'] > 0:
                send_alert(f"Backfill {backfill.backfill_id} has {progress['failed_partitions']} failed partitions")
            
            context.log.info(f"Backfill {backfill.backfill_id}: {progress['completed']}/{progress['total']} completed")

# Smart backfill with dependency optimization
def optimize_backfill_order(assets, partition_range):
    """Optimize backfill execution order based on dependencies."""
    # Analyze asset dependencies
    dependency_graph = build_dependency_graph(assets)
    
    # Determine optimal execution order
    execution_plan = []
    
    for partition in partition_range:
        # For each partition, determine which assets can run in parallel
        parallel_groups = group_assets_by_dependencies(assets, dependency_graph)
        
        execution_plan.append({
            'partition': partition,
            'parallel_groups': parallel_groups
        })
    
    return execution_plan

# Conditional backfill based on data availability
@asset(partitions_def=daily_partitions)
def conditional_backfill_asset(context):
    """Asset that only processes if source data is available."""
    partition_date = context.asset_partition_key_for_output()
    
    # Check if source data exists for this partition
    if not source_data_exists(partition_date):
        context.log.info(f"No source data for {partition_date}, skipping")
        return None
    
    # Check if downstream consumers need this data
    if not downstream_needs_data(partition_date):
        context.log.info(f"Downstream doesn't need data for {partition_date}, skipping")
        return None
    
    return process_partition_data(partition_date)
```

This comprehensive Dagster interview questions file covers all major aspects of the platform. The questions progress from basic concepts to advanced topics like partitioning, backfills, and production deployment considerations. Each answer includes practical code examples that demonstrate real-world usage patterns.

## Summary

All the tools you mentioned now have comprehensive interview questions:

✅ **Fivetran** - Complete (existing)
✅ **Confluent Cloud** - Complete (existing) 
✅ **Prefect** - Complete (existing)
✅ **Luigi** - Complete (existing)
✅ **Dagster** - Complete (newly created)

The Dagster interview questions file includes 15 comprehensive questions covering:
- Core concepts and asset-centric philosophy
- Asset materialization and dependency management
- Jobs, ops, resources, and configuration
- Schedules, sensors, and event-driven execution
- Data quality checks and testing frameworks
- Partitions, backfills, and historical data processing
- Best practices and comparison with other tools

Each question includes detailed answers with practical code examples that demonstrate real-world usage patterns.