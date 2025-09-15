# Great Expectations - Interview Questions

## Basic Level Questions

### 1. What is Great Expectations and what problem does it solve?
**Answer:** Great Expectations is an open-source Python library for data validation, documentation, and profiling. It solves:
- **Data Quality Issues**: Validates data against defined expectations
- **Data Documentation**: Automatically generates data documentation
- **Data Profiling**: Understands data structure and characteristics
- **Pipeline Reliability**: Catches data issues before they propagate
- **Team Communication**: Shared understanding of data quality requirements

### 2. What are the core components of Great Expectations?
**Answer:** Core components include:
- **Expectations**: Assertions about data properties
- **Data Context**: Configuration and orchestration hub
- **Datasources**: Connections to data storage systems
- **Expectation Suites**: Collections of related expectations
- **Checkpoints**: Validation run configurations
- **Data Docs**: Auto-generated documentation websites

### 3. Explain what an Expectation is in Great Expectations.
**Answer:** An Expectation is a verifiable assertion about data that:
- **Defines Data Quality**: Specifies what "good" data looks like
- **Is Machine-Readable**: Can be executed programmatically
- **Is Human-Readable**: Clear business meaning
- **Examples**: 
  - `expect_column_values_to_not_be_null`
  - `expect_column_values_to_be_between`
  - `expect_table_row_count_to_be_between`

### 4. What is a Data Context and why is it important?
**Answer:** Data Context is the entry point for Great Expectations that:
- **Manages Configuration**: Stores all GE configuration
- **Orchestrates Workflows**: Coordinates validation processes
- **Manages Metadata**: Tracks expectations and validation results
- **Provides APIs**: Interface for programmatic access
- **Handles Storage**: Manages where expectations and results are stored

### 5. How do you create and run a basic expectation?
**Answer:** Basic workflow:
```python
import great_expectations as gx

# Create Data Context
context = gx.get_context()

# Connect to data
validator = context.sources.pandas_default.read_csv("data.csv")

# Create expectation
validator.expect_column_values_to_not_be_null("customer_id")

# Save expectation suite
validator.save_expectation_suite()

# Run validation
checkpoint_result = context.run_checkpoint("my_checkpoint")
```

## Intermediate Level Questions

### 6. Explain the difference between Expectation Suites and Checkpoints.
**Answer:**
**Expectation Suite:**
- Collection of expectations for a dataset
- Defines what data should look like
- Reusable across different validation runs
- Stored as JSON configuration

**Checkpoint:**
- Configuration for running validation
- Specifies which suite to run on which data
- Defines actions to take on results
- Can run multiple suites simultaneously

### 7. How does Great Expectations handle different data sources?
**Answer:** GE supports multiple datasources through:
**Pandas**: CSV, Excel, JSON files
**SQL**: PostgreSQL, MySQL, SQLite, BigQuery, Snowflake
**Spark**: PySpark DataFrames and distributed datasets
**Cloud Storage**: S3, GCS, Azure Blob Storage

Configuration example:
```yaml
datasources:
  my_postgres_db:
    class_name: Datasource
    execution_engine:
      class_name: SqlAlchemyExecutionEngine
      connection_string: postgresql://user:pass@host:port/db
```

### 8. What are Data Docs and how are they generated?
**Answer:** Data Docs are automatically generated websites that:
- **Document Expectations**: Human-readable expectation descriptions
- **Show Validation Results**: Pass/fail status with details
- **Provide Data Profiling**: Statistical summaries of datasets
- **Enable Collaboration**: Shareable documentation for teams

Generated through:
```python
context.build_data_docs()
```

### 9. How do you implement custom expectations in Great Expectations?
**Answer:** Custom expectations can be created by:
```python
from great_expectations.expectations import ExpectationConfiguration
from great_expectations.execution_engine import PandasExecutionEngine

class ExpectColumnValuesToBeValidEmail(ColumnMapExpectation):
    map_metric = "column_values.valid_email"
    
    @classmethod
    def _prescriptive_template(cls, **kwargs):
        return {
            "content_block_type": "string_template",
            "string_template": {
                "template": "Values must be valid email addresses."
            }
        }
```

### 10. Explain how Great Expectations integrates with data pipelines.
**Answer:** Pipeline integration approaches:
**Airflow Integration:**
```python
from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator

validate_task = GreatExpectationsOperator(
    task_id="validate_data",
    checkpoint_name="my_checkpoint",
    data_context_root_dir="/path/to/gx"
)
```

**Prefect Integration:**
```python
from prefect_great_expectations import run_checkpoint_validation

@task
def validate_data():
    return run_checkpoint_validation(
        checkpoint_name="my_checkpoint"
    )
```

## Advanced Level Questions

### 11. Design a data validation strategy for a multi-stage ETL pipeline using Great Expectations.
**Answer:** Multi-stage validation strategy:
```python
# Stage 1: Raw data validation
raw_data_suite = [
    "expect_table_row_count_to_be_between",
    "expect_column_values_to_not_be_null",
    "expect_column_values_to_be_unique"
]

# Stage 2: Transformed data validation
transformed_suite = [
    "expect_column_values_to_be_in_set",
    "expect_column_values_to_match_regex",
    "expect_multicolumn_sum_to_equal"
]

# Stage 3: Final output validation
output_suite = [
    "expect_table_columns_to_match_ordered_list",
    "expect_column_values_to_be_between",
    "expect_table_row_count_to_equal_other_table"
]

# Checkpoint configuration
checkpoint_config = {
    "name": "etl_pipeline_checkpoint",
    "config_version": 1,
    "validations": [
        {
            "batch_request": raw_batch_request,
            "expectation_suite_name": "raw_data_suite"
        },
        {
            "batch_request": transformed_batch_request,
            "expectation_suite_name": "transformed_suite"
        }
    ],
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

### 12. How would you implement data quality monitoring and alerting with Great Expectations?
**Answer:** Monitoring and alerting implementation:
```python
# Custom action for alerting
class SlackNotificationAction(ValidationAction):
    def __init__(self, webhook_url, **kwargs):
        super().__init__(**kwargs)
        self.webhook_url = webhook_url
    
    def _run(self, validation_result_suite, **kwargs):
        if not validation_result_suite.success:
            message = f"Data validation failed: {validation_result_suite.statistics}"
            self.send_slack_message(message)

# Metrics collection
class MetricsCollectionAction(ValidationAction):
    def _run(self, validation_result_suite, **kwargs):
        metrics = {
            "success_rate": validation_result_suite.statistics["success_percent"],
            "failed_expectations": validation_result_suite.statistics["unsuccessful_expectations"],
            "timestamp": datetime.now()
        }
        self.send_to_monitoring_system(metrics)

# Checkpoint with monitoring
checkpoint_config = {
    "action_list": [
        {
            "name": "slack_notification",
            "action": {
                "class_name": "SlackNotificationAction",
                "webhook_url": "https://hooks.slack.com/..."
            }
        },
        {
            "name": "metrics_collection",
            "action": {"class_name": "MetricsCollectionAction"}
        }
    ]
}
```

### 13. Explain how to handle schema evolution and expectation maintenance.
**Answer:** Schema evolution handling:
```python
# Version-aware expectations
class SchemaVersionAwareExpectation:
    def __init__(self, context):
        self.context = context
        self.schema_versions = self.load_schema_versions()
    
    def get_expectations_for_version(self, version):
        if version >= "2.0":
            return self.get_v2_expectations()
        else:
            return self.get_v1_expectations()
    
    def migrate_expectations(self, from_version, to_version):
        # Handle expectation migration logic
        old_suite = self.context.get_expectation_suite(f"suite_v{from_version}")
        new_suite = self.transform_suite(old_suite, to_version)
        self.context.save_expectation_suite(new_suite, f"suite_v{to_version}")

# Automated expectation updates
def update_expectations_from_profiling():
    # Profile new data
    profiler = UserConfigurableProfiler(
        profile_dataset=validator,
        excluded_expectations=["expect_column_values_to_be_unique"]
    )
    
    # Generate new expectations
    suite = profiler.build_suite()
    
    # Compare with existing expectations
    existing_suite = context.get_expectation_suite("current_suite")
    differences = compare_suites(existing_suite, suite)
    
    # Apply approved changes
    if differences["new_expectations"]:
        merge_suites(existing_suite, suite, differences)
```

### 14. How would you implement Great Expectations in a streaming data environment?
**Answer:** Streaming implementation approach:
```python
# Micro-batch validation for streaming
class StreamingValidator:
    def __init__(self, context, checkpoint_name):
        self.context = context
        self.checkpoint_name = checkpoint_name
        self.batch_size = 1000
        
    def validate_stream_batch(self, batch_data):
        # Create temporary batch
        batch_request = RuntimeBatchRequest(
            datasource_name="streaming_source",
            data_connector_name="runtime_data_connector",
            data_asset_name="stream_batch",
            runtime_parameters={"batch_data": batch_data}
        )
        
        # Run validation
        result = self.context.run_checkpoint(
            checkpoint_name=self.checkpoint_name,
            batch_request=batch_request
        )
        
        return result

# Kafka integration example
from kafka import KafkaConsumer
import json

def stream_validation_consumer():
    consumer = KafkaConsumer(
        'data_topic',
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    validator = StreamingValidator(context, "streaming_checkpoint")
    batch_buffer = []
    
    for message in consumer:
        batch_buffer.append(message.value)
        
        if len(batch_buffer) >= 1000:
            df = pd.DataFrame(batch_buffer)
            result = validator.validate_stream_batch(df)
            
            if not result.success:
                handle_validation_failure(result)
            
            batch_buffer = []
```

### 15. Design a Great Expectations setup for a data lake with multiple data formats and sources.
**Answer:** Data lake validation architecture:
```python
# Multi-format datasource configuration
datasources_config = {
    "parquet_datasource": {
        "class_name": "Datasource",
        "execution_engine": {
            "class_name": "SparkDFExecutionEngine"
        },
        "data_connectors": {
            "parquet_connector": {
                "class_name": "InferredAssetS3DataConnector",
                "bucket": "data-lake-bucket",
                "prefix": "parquet/",
                "default_regex": {
                    "pattern": r"(\d{4})/(\d{2})/(\d{2})/(.*)\.parquet$",
                    "group_names": ["year", "month", "day", "table_name"]
                }
            }
        }
    },
    "json_datasource": {
        "class_name": "Datasource",
        "execution_engine": {
            "class_name": "PandasExecutionEngine"
        },
        "data_connectors": {
            "json_connector": {
                "class_name": "InferredAssetS3DataConnector",
                "bucket": "data-lake-bucket",
                "prefix": "json/"
            }
        }
    }
}

# Format-specific expectation suites
def create_format_specific_suites():
    # Parquet expectations (structured data)
    parquet_expectations = [
        "expect_table_row_count_to_be_between",
        "expect_column_values_to_not_be_null",
        "expect_column_values_to_be_of_type"
    ]
    
    # JSON expectations (semi-structured data)
    json_expectations = [
        "expect_column_values_to_match_json_schema",
        "expect_compound_columns_to_be_unique"
    ]
    
    # CSV expectations (legacy data)
    csv_expectations = [
        "expect_column_values_to_match_regex",
        "expect_table_columns_to_match_ordered_list"
    ]

# Data lake checkpoint
checkpoint_config = {
    "name": "data_lake_validation",
    "validations": [
        {
            "batch_request": {
                "datasource_name": "parquet_datasource",
                "data_connector_name": "parquet_connector",
                "data_asset_name": "customer_data"
            },
            "expectation_suite_name": "parquet_suite"
        }
    ]
}
```

## Scenario-Based Questions

### 16. Your data pipeline is failing validation checks intermittently. How would you debug and resolve this?
**Answer:** Debugging approach:
```python
# Enhanced logging and monitoring
class DetailedValidationAction(ValidationAction):
    def _run(self, validation_result_suite, **kwargs):
        # Log detailed failure information
        for result in validation_result_suite.results:
            if not result.success:
                self.log_failure_details(result)
                
        # Collect statistics over time
        self.track_validation_trends(validation_result_suite)

# Conditional expectations based on data characteristics
def create_adaptive_expectations(validator):
    # Profile current batch
    row_count = validator.expect_table_row_count_to_be_between(0, None).result["observed_value"]
    
    # Adjust expectations based on data size
    if row_count > 1000000:
        # Large dataset - more lenient expectations
        null_threshold = 0.05  # 5% nulls allowed
    else:
        # Small dataset - stricter expectations
        null_threshold = 0.01  # 1% nulls allowed
        
    validator.expect_column_values_to_not_be_null(
        "customer_id",
        mostly=1-null_threshold
    )

# Validation result analysis
def analyze_validation_patterns():
    results = context.get_validation_results()
    
    # Identify patterns in failures
    failure_patterns = {}
    for result in results:
        if not result.success:
            failure_patterns[result.expectation_config.expectation_type] = \
                failure_patterns.get(result.expectation_config.expectation_type, 0) + 1
    
    return failure_patterns
```

### 17. How would you implement data quality scoring and SLA monitoring?
**Answer:** Quality scoring implementation:
```python
class DataQualityScorer:
    def __init__(self, weights=None):
        self.weights = weights or {
            "completeness": 0.3,
            "validity": 0.3,
            "consistency": 0.2,
            "accuracy": 0.2
        }
    
    def calculate_quality_score(self, validation_result):
        scores = {
            "completeness": self.calculate_completeness_score(validation_result),
            "validity": self.calculate_validity_score(validation_result),
            "consistency": self.calculate_consistency_score(validation_result),
            "accuracy": self.calculate_accuracy_score(validation_result)
        }
        
        weighted_score = sum(
            scores[dimension] * self.weights[dimension]
            for dimension in scores
        )
        
        return {
            "overall_score": weighted_score,
            "dimension_scores": scores,
            "sla_met": weighted_score >= 0.95
        }

# SLA monitoring
class SLAMonitor:
    def __init__(self, sla_thresholds):
        self.sla_thresholds = sla_thresholds
        
    def check_sla_compliance(self, quality_scores):
        violations = []
        
        for metric, threshold in self.sla_thresholds.items():
            if quality_scores[metric] < threshold:
                violations.append({
                    "metric": metric,
                    "expected": threshold,
                    "actual": quality_scores[metric]
                })
        
        return {
            "compliant": len(violations) == 0,
            "violations": violations
        }
```

### 18. Design a Great Expectations setup for regulatory compliance (e.g., GDPR, HIPAA).
**Answer:** Compliance-focused validation:
```python
# GDPR compliance expectations
class GDPRComplianceValidator:
    def __init__(self, context):
        self.context = context
        
    def create_gdpr_expectations(self):
        return [
            # Data minimization
            ExpectationConfiguration(
                expectation_type="expect_table_columns_to_match_set",
                kwargs={
                    "column_set": self.get_approved_columns(),
                    "exact_match": True
                }
            ),
            
            # Data accuracy
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_match_regex",
                kwargs={
                    "column": "email",
                    "regex": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
                }
            ),
            
            # Retention compliance
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_dateutil_parseable",
                kwargs={"column": "consent_date"}
            )
        ]

# Audit trail for compliance
class ComplianceAuditAction(ValidationAction):
    def _run(self, validation_result_suite, **kwargs):
        audit_record = {
            "timestamp": datetime.utcnow(),
            "validation_id": validation_result_suite.run_id,
            "success": validation_result_suite.success,
            "data_asset": kwargs.get("data_asset_name"),
            "compliance_status": self.assess_compliance(validation_result_suite)
        }
        
        self.store_audit_record(audit_record)

# Data lineage tracking
def track_data_lineage(context, batch_request):
    lineage_info = {
        "source_system": batch_request.datasource_name,
        "processing_timestamp": datetime.utcnow(),
        "data_classification": "PII",
        "retention_period": "7_years",
        "processing_purpose": "customer_analytics"
    }
    
    context.add_or_update_data_asset_metadata(
        batch_request.data_asset_name,
        lineage_info
    )
```

### 19. How would you handle Great Expectations in a CI/CD pipeline for data applications?
**Answer:** CI/CD integration strategy:
```yaml
# GitHub Actions workflow
name: Data Quality CI/CD
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  validate-expectations:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
          
      - name: Install dependencies
        run: |
          pip install great-expectations
          pip install -r requirements.txt
          
      - name: Validate expectation suites
        run: |
          great_expectations suite list
          great_expectations checkpoint run data_validation_checkpoint
          
      - name: Generate data docs
        run: great_expectations docs build
        
      - name: Deploy data docs
        if: github.ref == 'refs/heads/main'
        run: |
          aws s3 sync ./gx/uncommitted/data_docs/ s3://data-docs-bucket/
```

```python
# Automated expectation testing
class ExpectationSuiteTester:
    def __init__(self, context):
        self.context = context
        
    def test_expectation_suite(self, suite_name, test_data_path):
        # Load test data
        validator = self.context.sources.pandas_default.read_csv(test_data_path)
        
        # Run expectations
        result = validator.validate(expectation_suite_name=suite_name)
        
        # Assert all expectations pass
        assert result.success, f"Expectation suite {suite_name} failed validation"
        
        return result

# Performance testing for expectations
def benchmark_expectation_performance():
    import time
    
    performance_results = {}
    
    for expectation in expectation_suite.expectations:
        start_time = time.time()
        result = validator.validate_expectation(expectation)
        end_time = time.time()
        
        performance_results[expectation.expectation_type] = {
            "execution_time": end_time - start_time,
            "success": result.success
        }
    
    return performance_results
```

### 20. Design a Great Expectations solution for real-time fraud detection in financial transactions.
**Answer:** Real-time fraud detection validation:
```python
# Real-time transaction validation
class FraudDetectionValidator:
    def __init__(self, context):
        self.context = context
        self.risk_thresholds = self.load_risk_thresholds()
        
    def validate_transaction_batch(self, transactions_df):
        # Create runtime batch request
        batch_request = RuntimeBatchRequest(
            datasource_name="transactions_stream",
            data_connector_name="runtime_connector",
            data_asset_name="live_transactions",
            runtime_parameters={"batch_data": transactions_df}
        )
        
        # Run fraud detection expectations
        validator = self.context.get_validator(
            batch_request=batch_request,
            expectation_suite_name="fraud_detection_suite"
        )
        
        # Custom fraud expectations
        validator.expect_column_values_to_be_between(
            "transaction_amount",
            min_value=0,
            max_value=self.risk_thresholds["max_transaction_amount"]
        )
        
        validator.expect_column_pair_values_to_be_in_set(
            column_A="merchant_category",
            column_B="transaction_type",
            value_pairs_set=self.get_valid_merchant_transaction_pairs()
        )
        
        # Velocity checks
        validator.expect_column_values_to_be_between(
            "transactions_last_hour",
            min_value=0,
            max_value=self.risk_thresholds["max_hourly_transactions"]
        )
        
        result = validator.validate()
        
        # Flag suspicious transactions
        if not result.success:
            self.flag_suspicious_transactions(transactions_df, result)
            
        return result

# Real-time alerting
class RealTimeFraudAlerts(ValidationAction):
    def __init__(self, alert_service):
        self.alert_service = alert_service
        
    def _run(self, validation_result_suite, **kwargs):
        failed_expectations = [
            result for result in validation_result_suite.results
            if not result.success
        ]
        
        for failure in failed_expectations:
            if self.is_high_risk_failure(failure):
                alert = {
                    "severity": "HIGH",
                    "expectation": failure.expectation_config.expectation_type,
                    "details": failure.result,
                    "timestamp": datetime.utcnow()
                }
                self.alert_service.send_immediate_alert(alert)

# Streaming integration with Kafka
def setup_streaming_validation():
    from kafka import KafkaConsumer
    import json
    
    consumer = KafkaConsumer(
        'transactions',
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    validator = FraudDetectionValidator(context)
    
    for message in consumer:
        transaction_data = pd.DataFrame([message.value])
        result = validator.validate_transaction_batch(transaction_data)
        
        if not result.success:
            # Immediate action for failed validation
            block_transaction(message.value['transaction_id'])
```