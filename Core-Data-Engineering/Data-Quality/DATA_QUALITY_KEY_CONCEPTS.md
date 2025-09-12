# Data Quality Key Concepts for Data Engineers

## 📋 Table of Contents

1. [Introduction to Data Quality](#introduction-to-data-quality)
2. [Data Quality Dimensions](#data-quality-dimensions)
3. [Data Quality Architecture](#data-quality-architecture)
4. [Great Expectations Framework](#great-expectations-framework)
5. [Data Profiling & Discovery](#data-profiling--discovery)
6. [Data Validation Strategies](#data-validation-strategies)
7. [Data Quality Monitoring](#data-quality-monitoring)
8. [Integration Patterns](#integration-patterns)
9. [Best Practices](#best-practices)
10. [Common Challenges](#common-challenges)

---

## Introduction to Data Quality

### What is Data Quality?
Data quality refers to the condition of data based on factors such as accuracy, completeness, consistency, reliability, and whether it's up-to-date and relevant for its intended use.

### Why Data Quality Matters
- **Business Impact**: Poor data quality costs organizations an average of $15 million annually
- **Decision Making**: Quality data enables accurate analytics and informed decisions
- **Compliance**: Regulatory requirements demand high data quality standards
- **Automation**: ML/AI systems require high-quality training data
- **Trust**: Stakeholder confidence depends on reliable data

### Data Quality vs Data Governance
```
Data Quality (Tactical):
├── Data validation and testing
├── Error detection and correction
├── Data profiling and monitoring
└── Quality metrics and reporting

Data Governance (Strategic):
├── Data policies and standards
├── Data stewardship roles
├── Data lifecycle management
└── Compliance and security
```

---

## Data Quality Dimensions

### 1. Accuracy
**Definition**: Data correctly represents the real-world entity or event
```python
# Example: Email validation
def validate_email_accuracy(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Great Expectations implementation
validator.expect_column_values_to_match_regex(
    column="email",
    regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)
```

### 2. Completeness
**Definition**: All required data is present
```python
# Completeness checks
validator.expect_column_values_to_not_be_null("customer_id")
validator.expect_table_row_count_to_be_between(min_value=1000)

# Completeness ratio calculation
completeness_ratio = (total_records - null_records) / total_records
```

### 3. Consistency
**Definition**: Data is uniform across systems and datasets
```python
# Cross-system consistency
validator.expect_column_values_to_be_in_set(
    column="status",
    value_set=["active", "inactive", "pending"]
)

# Format consistency
validator.expect_column_values_to_match_strftime_format(
    column="date_created",
    strftime_format="%Y-%m-%d"
)
```

### 4. Validity
**Definition**: Data conforms to defined formats and business rules
```python
# Business rule validation
validator.expect_column_values_to_be_between(
    column="age",
    min_value=0,
    max_value=120
)

# Referential integrity
validator.expect_column_values_to_be_in_set(
    column="country_code",
    value_set=valid_country_codes
)
```

### 5. Timeliness
**Definition**: Data is available when needed and up-to-date
```python
# Freshness validation
from datetime import datetime, timedelta

max_age = datetime.now() - timedelta(hours=24)
validator.expect_column_values_to_be_dateutil_parseable("last_updated")
validator.expect_column_values_to_be_between(
    column="last_updated",
    min_value=max_age
)
```

### 6. Uniqueness
**Definition**: No duplicate records exist where they shouldn't
```python
# Uniqueness validation
validator.expect_column_values_to_be_unique("customer_id")
validator.expect_compound_columns_to_be_unique(
    column_list=["customer_id", "order_date", "product_id"]
)
```

---

## Data Quality Architecture

### Layered Architecture
```
┌─────────────────────────────────────────┐
│           Data Quality Layer            │
├─────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────────┐   │
│  │ Monitoring  │  │   Alerting      │   │
│  │ & Reporting │  │   & Notification│   │
│  └─────────────┘  └─────────────────┘   │
├─────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────────┐   │
│  │ Validation  │  │   Profiling     │   │
│  │ & Testing   │  │   & Discovery   │   │
│  └─────────────┘  └─────────────────┘   │
├─────────────────────────────────────────┤
│           Data Processing Layer         │
├─────────────────────────────────────────┤
│             Data Storage Layer          │
└─────────────────────────────────────────┘
```

### Components
1. **Data Profiling**: Analyze data characteristics and patterns
2. **Data Validation**: Apply business rules and constraints
3. **Data Monitoring**: Continuous quality assessment
4. **Data Cleansing**: Correct identified quality issues
5. **Data Lineage**: Track data flow and transformations

---

## Great Expectations Framework

### Core Architecture
```python
import great_expectations as gx

# 1. Data Context - Central configuration hub
context = gx.get_context()

# 2. Datasource - Connection to data systems
datasource_config = {
    "name": "production_db",
    "class_name": "Datasource",
    "execution_engine": {
        "class_name": "SqlAlchemyExecutionEngine",
        "connection_string": "postgresql://user:pass@host:port/db"
    }
}

# 3. Expectation Suite - Collection of data quality rules
suite = context.create_expectation_suite("customer_data_quality")

# 4. Validator - Execute expectations against data
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name="customer_data_quality"
)

# 5. Checkpoint - Automated validation workflow
checkpoint_config = {
    "name": "customer_data_checkpoint",
    "config_version": 1.0,
    "template_name": None,
    "module_name": "great_expectations.checkpoint",
    "class_name": "Checkpoint",
    "run_name_template": "%Y%m%d-%H%M%S-customer-data",
    "expectation_suite_name": "customer_data_quality",
    "batch_request": batch_request,
    "action_list": [
        {
            "name": "store_validation_result",
            "action": {"class_name": "StoreValidationResultAction"}
        },
        {
            "name": "update_data_docs",
            "action": {"class_name": "UpdateDataDocsAction"}
        }
    ]
}
```

### Expectation Types
```python
# Table-level expectations
validator.expect_table_row_count_to_be_between(min_value=1000, max_value=10000)
validator.expect_table_column_count_to_equal(15)

# Column existence
validator.expect_column_to_exist("customer_id")

# Data type validation
validator.expect_column_values_to_be_of_type("age", "int64")

# Null value checks
validator.expect_column_values_to_not_be_null("customer_id")

# Uniqueness validation
validator.expect_column_values_to_be_unique("email")

# Range validation
validator.expect_column_values_to_be_between("age", min_value=0, max_value=120)

# Pattern matching
validator.expect_column_values_to_match_regex(
    "phone", r'^\+?1?[0-9]{10,15}$'
)

# Set membership
validator.expect_column_values_to_be_in_set(
    "status", ["active", "inactive", "pending"]
)

# Statistical expectations
validator.expect_column_mean_to_be_between("order_amount", 50, 500)
validator.expect_column_stdev_to_be_between("order_amount", 10, 200)

# Multi-column expectations
validator.expect_multicolumn_values_to_be_unique(["customer_id", "order_date"])
validator.expect_column_pair_values_A_to_be_greater_than_B("end_date", "start_date")
```

---

## Data Profiling & Discovery

### Automated Profiling
```python
# Great Expectations profiling
from great_expectations.profile.user_configurable_profiler import UserConfigurableProfiler

profiler = UserConfigurableProfiler(
    profile_dataset=validator,
    excluded_expectations=[
        "expect_column_values_to_be_in_type_list"
    ],
    ignored_columns=["internal_id", "created_by"],
    not_null_only=False,
    primary_or_compound_key=[{"customer_id": "primary"}],
    semantic_types_dict={
        "customer_id": "primary_key",
        "email": "email",
        "phone": "phone_number",
        "created_date": "datetime"
    },
    table_expectations_only=False,
    value_set_threshold="MANY"
)

suite = profiler.build_suite()
```

### Statistical Profiling
```python
import pandas as pd
import numpy as np

def comprehensive_profile(df):
    """Generate comprehensive data profile"""
    profile = {}
    
    for column in df.columns:
        col_profile = {
            'dtype': str(df[column].dtype),
            'count': len(df[column]),
            'null_count': df[column].isnull().sum(),
            'null_percentage': (df[column].isnull().sum() / len(df)) * 100,
            'unique_count': df[column].nunique(),
            'unique_percentage': (df[column].nunique() / len(df)) * 100
        }
        
        if df[column].dtype in ['int64', 'float64']:
            col_profile.update({
                'mean': df[column].mean(),
                'median': df[column].median(),
                'std': df[column].std(),
                'min': df[column].min(),
                'max': df[column].max(),
                'q25': df[column].quantile(0.25),
                'q75': df[column].quantile(0.75)
            })
        
        if df[column].dtype == 'object':
            col_profile.update({
                'avg_length': df[column].str.len().mean(),
                'max_length': df[column].str.len().max(),
                'min_length': df[column].str.len().min()
            })
        
        profile[column] = col_profile
    
    return profile
```

---

## Data Validation Strategies

### 1. Schema Validation
```python
# Schema enforcement
expected_schema = {
    'customer_id': 'int64',
    'name': 'object',
    'email': 'object',
    'age': 'int64',
    'signup_date': 'datetime64[ns]'
}

for column, expected_type in expected_schema.items():
    validator.expect_column_to_exist(column)
    validator.expect_column_values_to_be_of_type(column, expected_type)
```

### 2. Business Rule Validation
```python
# Complex business rules
def validate_customer_business_rules(validator):
    # Age must be reasonable for service
    validator.expect_column_values_to_be_between("age", 13, 120)
    
    # Email must be unique and valid
    validator.expect_column_values_to_be_unique("email")
    validator.expect_column_values_to_match_regex(
        "email", r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    
    # Signup date cannot be in the future
    from datetime import datetime
    validator.expect_column_values_to_be_between(
        "signup_date",
        min_value=datetime(2020, 1, 1),
        max_value=datetime.now()
    )
    
    # Premium customers must have valid payment method
    validator.expect_conditional_column_values_to_not_be_null(
        column="payment_method",
        condition_column="customer_type",
        condition_value="premium"
    )
```

### 3. Cross-System Validation
```python
# Reference data validation
def validate_reference_data(validator, reference_systems):
    # Country codes must exist in reference system
    valid_countries = reference_systems['countries'].get_valid_codes()
    validator.expect_column_values_to_be_in_set("country_code", valid_countries)
    
    # Product IDs must exist in product catalog
    valid_products = reference_systems['products'].get_active_products()
    validator.expect_column_values_to_be_in_set("product_id", valid_products)
    
    # Currency codes must be ISO compliant
    iso_currencies = reference_systems['currencies'].get_iso_codes()
    validator.expect_column_values_to_be_in_set("currency", iso_currencies)
```

---

## Data Quality Monitoring

### Real-time Monitoring
```python
# Streaming data quality monitoring
from kafka import KafkaConsumer
import json

class DataQualityMonitor:
    def __init__(self, context, suite_name):
        self.context = context
        self.suite_name = suite_name
        self.quality_metrics = {}
    
    def monitor_stream(self, topic_name):
        consumer = KafkaConsumer(
            topic_name,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        
        for message in consumer:
            data = message.value
            
            # Validate each record
            validation_result = self.validate_record(data)
            
            # Update quality metrics
            self.update_metrics(validation_result)
            
            # Alert on quality issues
            if not validation_result.success:
                self.send_alert(validation_result)
    
    def validate_record(self, record):
        # Convert to DataFrame for validation
        df = pd.DataFrame([record])
        
        # Create batch request
        batch_request = RuntimeBatchRequest(
            datasource_name="streaming_datasource",
            data_connector_name="default_runtime_data_connector",
            data_asset_name="streaming_data",
            runtime_parameters={"batch_data": df},
            batch_identifiers={"default_identifier_name": "streaming_batch"}
        )
        
        # Get validator and run expectations
        validator = self.context.get_validator(
            batch_request=batch_request,
            expectation_suite_name=self.suite_name
        )
        
        return validator.validate()
```

### Batch Monitoring
```python
# Scheduled batch validation
import schedule
import time

def run_daily_quality_check():
    """Daily data quality validation"""
    
    # Get today's data
    batch_request = BatchRequest(
        datasource_name="production_db",
        data_connector_name="daily_data_connector",
        data_asset_name="customer_transactions",
        data_connector_query={
            "batch_filter_parameters": {
                "date": datetime.now().strftime("%Y-%m-%d")
            }
        }
    )
    
    # Run checkpoint
    checkpoint_result = context.run_checkpoint(
        checkpoint_name="daily_quality_checkpoint",
        batch_request=batch_request
    )
    
    # Process results
    if not checkpoint_result.success:
        send_quality_alert(checkpoint_result)
        trigger_data_investigation(checkpoint_result)
    
    # Update quality dashboard
    update_quality_dashboard(checkpoint_result)

# Schedule daily runs
schedule.every().day.at("06:00").do(run_daily_quality_check)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## Integration Patterns

### 1. CI/CD Integration
```yaml
# .github/workflows/data-quality.yml
name: Data Quality Validation

on:
  push:
    paths:
      - 'data/**'
      - 'expectations/**'

jobs:
  validate-data-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      
      - name: Install dependencies
        run: |
          pip install great-expectations pandas
      
      - name: Run data quality tests
        run: |
          great_expectations checkpoint run customer_data_checkpoint
      
      - name: Upload results
        uses: actions/upload-artifact@v2
        with:
          name: data-quality-results
          path: great_expectations/uncommitted/data_docs/
```

### 2. Airflow Integration
```python
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator

def run_data_quality_check(**context):
    """Run Great Expectations validation in Airflow"""
    
    checkpoint_config = {
        "name": "airflow_checkpoint",
        "config_version": 1.0,
        "expectation_suite_name": "customer_data_suite",
        "batch_request": {
            "datasource_name": "production_db",
            "data_connector_name": "default_inferred_data_connector",
            "data_asset_name": "customer_table"
        }
    }
    
    return checkpoint_config

dag = DAG(
    'data_quality_pipeline',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1)
)

# Data quality validation task
quality_check = GreatExpectationsOperator(
    task_id='validate_customer_data',
    expectation_suite_name='customer_data_suite',
    batch_kwargs={
        'table': 'customers',
        'datasource': 'production_db'
    },
    dag=dag
)
```

### 3. Spark Integration
```python
from pyspark.sql import SparkSession
from great_expectations.dataset import SparkDFDataset

# Initialize Spark
spark = SparkSession.builder.appName("DataQuality").getOrCreate()

# Load data
df = spark.read.table("production.customers")

# Create Great Expectations dataset
ge_df = SparkDFDataset(df)

# Add expectations
ge_df.expect_column_to_exist("customer_id")
ge_df.expect_column_values_to_not_be_null("customer_id")
ge_df.expect_column_values_to_be_unique("customer_id")

# Validate
validation_result = ge_df.validate()

# Handle results
if not validation_result.success:
    # Log failures
    for result in validation_result.results:
        if not result.success:
            print(f"Validation failed: {result.expectation_config}")
    
    # Stop pipeline on critical failures
    critical_failures = [r for r in validation_result.results 
                        if not r.success and r.expectation_config.meta.get('critical', False)]
    
    if critical_failures:
        raise Exception("Critical data quality issues detected")
```

---

## Best Practices

### 1. Expectation Design
```python
# Good: Specific and actionable expectations
validator.expect_column_values_to_be_between(
    column="age",
    min_value=0,
    max_value=120,
    meta={
        "notes": "Age must be realistic for human customers",
        "critical": True,
        "owner": "data-team@company.com"
    }
)

# Bad: Vague expectations
validator.expect_column_values_to_not_be_null("some_column")
```

### 2. Expectation Organization
```python
# Organize expectations by domain
def create_customer_expectations(validator):
    """Customer-specific data quality rules"""
    
    # Identity validation
    validator.expect_column_to_exist("customer_id")
    validator.expect_column_values_to_be_unique("customer_id")
    validator.expect_column_values_to_not_be_null("customer_id")
    
    # Contact information validation
    validator.expect_column_values_to_match_regex(
        "email", r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    validator.expect_column_values_to_match_regex(
        "phone", r'^\+?1?[0-9]{10,15}$'
    )
    
    # Demographic validation
    validator.expect_column_values_to_be_between("age", 13, 120)
    validator.expect_column_values_to_be_in_set(
        "country", ["US", "CA", "UK", "DE", "FR", "AU"]
    )

def create_transaction_expectations(validator):
    """Transaction-specific data quality rules"""
    
    # Transaction identity
    validator.expect_column_values_to_be_unique("transaction_id")
    validator.expect_column_values_to_not_be_null("transaction_id")
    
    # Financial validation
    validator.expect_column_values_to_be_between("amount", 0.01, 10000.00)
    validator.expect_column_values_to_be_in_set(
        "currency", ["USD", "EUR", "GBP", "CAD", "AUD"]
    )
    
    # Temporal validation
    validator.expect_column_values_to_be_dateutil_parseable("transaction_date")
    validator.expect_column_values_to_be_between(
        "transaction_date",
        min_value=datetime(2020, 1, 1),
        max_value=datetime.now() + timedelta(days=1)
    )
```

### 3. Performance Optimization
```python
# Sampling for large datasets
def create_sampled_validator(context, table_name, sample_size=10000):
    """Create validator with sampled data for performance"""
    
    batch_request = BatchRequest(
        datasource_name="production_db",
        data_connector_name="default_inferred_data_connector",
        data_asset_name=table_name,
        data_connector_query={
            "limit": sample_size,
            "random_sample": True
        }
    )
    
    return context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=f"{table_name}_quality_suite"
    )

# Parallel validation
from concurrent.futures import ThreadPoolExecutor

def parallel_validation(context, table_configs):
    """Run validations in parallel"""
    
    def validate_table(config):
        validator = context.get_validator(**config)
        return validator.validate()
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(validate_table, table_configs))
    
    return results
```

### 4. Error Handling
```python
def robust_validation(context, checkpoint_name):
    """Robust validation with error handling"""
    
    try:
        # Run checkpoint
        result = context.run_checkpoint(checkpoint_name=checkpoint_name)
        
        # Process successful validation
        if result.success:
            log_success(result)
            update_quality_metrics(result)
        else:
            # Handle validation failures
            handle_validation_failures(result)
            
    except Exception as e:
        # Handle system errors
        log_error(f"Validation system error: {str(e)}")
        send_alert(f"Data quality system failure: {str(e)}")
        
        # Fallback validation
        try:
            run_fallback_validation(checkpoint_name)
        except Exception as fallback_error:
            log_critical_error(f"Fallback validation failed: {str(fallback_error)}")

def handle_validation_failures(result):
    """Handle specific validation failures"""
    
    critical_failures = []
    warning_failures = []
    
    for validation_result in result.run_results.values():
        for expectation_result in validation_result.results:
            if not expectation_result.success:
                if expectation_result.expectation_config.meta.get('critical', False):
                    critical_failures.append(expectation_result)
                else:
                    warning_failures.append(expectation_result)
    
    # Handle critical failures
    if critical_failures:
        send_critical_alert(critical_failures)
        trigger_data_quarantine()
    
    # Log warnings
    if warning_failures:
        log_warnings(warning_failures)
        update_quality_dashboard(warning_failures)
```

---

## Common Challenges

### 1. Scale and Performance
**Challenge**: Validating large datasets efficiently
**Solutions**:
- Sampling strategies for statistical validation
- Incremental validation for streaming data
- Parallel processing for multiple datasets
- Caching of validation results

### 2. False Positives
**Challenge**: Expectations failing due to legitimate data variations
**Solutions**:
- Statistical thresholds instead of absolute rules
- Time-based expectations that account for seasonality
- Contextual validation based on business cycles

### 3. Expectation Maintenance
**Challenge**: Keeping expectations current with evolving data
**Solutions**:
- Automated expectation generation and updates
- Version control for expectation suites
- Regular review and validation of expectations
- Data drift detection and alerting

### 4. Integration Complexity
**Challenge**: Integrating data quality into existing pipelines
**Solutions**:
- Gradual rollout with non-blocking validations
- API-first approach for easy integration
- Standardized checkpoint configurations
- Clear escalation procedures for failures

---

This comprehensive guide covers the essential concepts of data quality management with a focus on Great Expectations as the primary framework. The concepts and patterns shown here provide a solid foundation for implementing robust data quality practices in any data engineering environment.