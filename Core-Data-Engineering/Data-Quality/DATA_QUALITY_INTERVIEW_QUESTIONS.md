# Data Quality Comprehensive Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-50)](#basic-level-questions-1-50)
2. [Intermediate Level Questions (51-100)](#intermediate-level-questions-51-100)
3. [Advanced Level Questions (101-150)](#advanced-level-questions-101-150)
4. [Architecture & Performance (151-200)](#architecture--performance-151-200)
5. [Streaming & Real-time Processing (201-230)](#streaming--real-time-processing-201-230)
6. [Production & Operations (231-260)](#production--operations-231-260)
7. [Scenario-Based Questions (261-300)](#scenario-based-questions-261-300)

---

## Basic Level Questions (1-50)

### 1. What is data quality and why is it important?
**Answer:**
Data quality refers to the condition of data based on factors like accuracy, completeness, consistency, reliability, and timeliness. It's important because:

- **Business Impact**: Poor data quality costs organizations millions annually
- **Decision Making**: Quality data enables accurate analytics and informed decisions
- **Compliance**: Regulatory requirements demand high data quality standards
- **Automation**: ML/AI systems require high-quality training data
- **Trust**: Stakeholder confidence depends on reliable data

```python
# Example: Data quality impact on business metrics
def calculate_revenue_impact(data_quality_score, total_revenue):
    """
    Poor data quality typically reduces business value by 15-25%
    """
    quality_multiplier = data_quality_score / 100
    actual_revenue = total_revenue * quality_multiplier
    lost_revenue = total_revenue - actual_revenue
    
    return {
        'actual_revenue': actual_revenue,
        'lost_revenue': lost_revenue,
        'impact_percentage': (lost_revenue / total_revenue) * 100
    }

# Example calculation
impact = calculate_revenue_impact(75, 1000000)  # 75% quality score, $1M revenue
print(f"Lost revenue due to poor data quality: ${impact['lost_revenue']:,.2f}")
```

### 2. What are the main dimensions of data quality?
**Answer:**
The six main dimensions of data quality are:

1. **Accuracy**: Data correctly represents real-world entities
2. **Completeness**: All required data is present
3. **Consistency**: Data is uniform across systems
4. **Validity**: Data conforms to defined formats and rules
5. **Timeliness**: Data is available when needed and up-to-date
6. **Uniqueness**: No duplicate records exist where they shouldn't

```python
# Data quality dimensions assessment
def assess_data_quality_dimensions(df):
    """Assess all six dimensions of data quality"""
    
    assessment = {}
    
    # 1. Completeness
    assessment['completeness'] = {
        'score': ((df.count().sum()) / (len(df) * len(df.columns))) * 100,
        'null_counts': df.isnull().sum().to_dict()
    }
    
    # 2. Uniqueness
    assessment['uniqueness'] = {
        'duplicate_rows': len(df) - len(df.drop_duplicates()),
        'duplicate_percentage': ((len(df) - len(df.drop_duplicates())) / len(df)) * 100
    }
    
    # 3. Validity (example for numeric columns)
    numeric_cols = df.select_dtypes(include=['number']).columns
    assessment['validity'] = {}
    for col in numeric_cols:
        assessment['validity'][col] = {
            'negative_values': (df[col] < 0).sum(),
            'outliers': len(df[df[col] > df[col].quantile(0.95)])
        }
    
    return assessment
```

### 3. What is Great Expectations and how does it work?
**Answer:**
Great Expectations is an open-source data validation, documentation, and profiling tool that helps teams maintain data quality.

**Core Components:**
- **Data Context**: Central configuration hub
- **Datasources**: Connections to data systems
- **Expectations**: Assertions about data properties
- **Expectation Suites**: Collections of related expectations
- **Validators**: Execute expectations against data
- **Checkpoints**: Automated validation workflows

```python
import great_expectations as gx

# 1. Initialize Data Context
context = gx.get_context()

# 2. Create Expectation Suite
suite = context.create_expectation_suite("customer_data_suite", overwrite_existing=True)

# 3. Add Expectations
suite.expect_column_to_exist("customer_id")
suite.expect_column_values_to_not_be_null("customer_id")
suite.expect_column_values_to_be_unique("customer_id")
suite.expect_column_values_to_be_between("age", min_value=0, max_value=120)

# 4. Save Suite
context.save_expectation_suite(suite)

# 5. Create Validator
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name="customer_data_suite"
)

# 6. Validate Data
validation_result = validator.validate()
```

### 4. How do you handle missing data in data quality processes?
**Answer:**
Missing data handling strategies depend on the context and business requirements:

```python
import pandas as pd
import numpy as np

def handle_missing_data(df, strategy='context_aware'):
    """Comprehensive missing data handling"""
    
    if strategy == 'context_aware':
        # Different strategies for different column types
        for column in df.columns:
            missing_pct = (df[column].isnull().sum() / len(df)) * 100
            
            if missing_pct > 50:
                print(f"Warning: {column} has {missing_pct:.1f}% missing values")
            
            # Numeric columns
            if df[column].dtype in ['int64', 'float64']:
                if missing_pct < 5:
                    # Low missing: use median
                    df[column].fillna(df[column].median(), inplace=True)
                elif missing_pct < 20:
                    # Medium missing: use interpolation
                    df[column].interpolate(inplace=True)
                else:
                    # High missing: create indicator variable
                    df[f'{column}_missing'] = df[column].isnull()
                    df[column].fillna(df[column].median(), inplace=True)
            
            # Categorical columns
            elif df[column].dtype == 'object':
                if missing_pct < 10:
                    # Use mode for low missing
                    df[column].fillna(df[column].mode()[0], inplace=True)
                else:
                    # Create 'Unknown' category for high missing
                    df[column].fillna('Unknown', inplace=True)
    
    return df

# Great Expectations validation for missing data
def validate_missing_data_handling(validator):
    """Validate missing data handling results"""
    
    # Ensure critical columns have no nulls
    validator.expect_column_values_to_not_be_null("customer_id")
    validator.expect_column_values_to_not_be_null("email")
    
    # Allow controlled nulls in optional fields
    validator.expect_column_values_to_not_be_null(
        "phone_number",
        mostly=0.8  # Allow 20% nulls
    )
    
    # Validate imputation results
    validator.expect_column_values_to_be_between("age", 0, 120)
    validator.expect_column_mean_to_be_between("income", 20000, 200000)
```

### 5. What are the different types of data validation?
**Answer:**
Data validation can be categorized into several types:

```python
# 1. Schema Validation
def validate_schema(df, expected_schema):
    """Validate data schema against expected structure"""
    
    schema_issues = []
    
    # Check column existence
    expected_columns = set(expected_schema.keys())
    actual_columns = set(df.columns)
    
    missing_columns = expected_columns - actual_columns
    extra_columns = actual_columns - expected_columns
    
    if missing_columns:
        schema_issues.append(f"Missing columns: {missing_columns}")
    
    if extra_columns:
        schema_issues.append(f"Unexpected columns: {extra_columns}")
    
    # Check data types
    for column, expected_type in expected_schema.items():
        if column in df.columns:
            actual_type = str(df[column].dtype)
            if actual_type != expected_type:
                schema_issues.append(f"Column {column}: expected {expected_type}, got {actual_type}")
    
    return schema_issues

# 2. Business Rule Validation
def validate_business_rules(validator):
    """Validate business-specific rules"""
    
    # Age must be reasonable
    validator.expect_column_values_to_be_between("age", 0, 120)
    
    # Email format validation
    validator.expect_column_values_to_match_regex(
        "email", r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    
    # Order amount must be positive
    validator.expect_column_values_to_be_between("order_amount", 0.01, None)
    
    # Status must be from valid set
    validator.expect_column_values_to_be_in_set(
        "status", ["active", "inactive", "pending", "cancelled"]
    )

# 3. Statistical Validation
def validate_statistical_properties(validator):
    """Validate statistical properties of data"""
    
    # Mean within expected range
    validator.expect_column_mean_to_be_between("order_amount", 50, 500)
    
    # Standard deviation within expected range
    validator.expect_column_stdev_to_be_between("order_amount", 10, 200)
    
    # Quantile validation
    validator.expect_column_quantile_values_to_be_between(
        "age",
        quantile_ranges={
            "quantiles": [0.25, 0.5, 0.75],
            "value_ranges": [[20, 30], [30, 40], [40, 60]]
        }
    )

# 4. Referential Integrity Validation
def validate_referential_integrity(validator, reference_data):
    """Validate referential integrity"""
    
    # Customer IDs must exist in customer table
    valid_customer_ids = reference_data['customers']['customer_id'].tolist()
    validator.expect_column_values_to_be_in_set("customer_id", valid_customer_ids)
    
    # Product codes must exist in product catalog
    valid_product_codes = reference_data['products']['product_code'].tolist()
    validator.expect_column_values_to_be_in_set("product_code", valid_product_codes)
```

### 6. How do you create expectations in Great Expectations?
**Answer:**
Expectations in Great Expectations can be created through multiple methods:

```python
import great_expectations as gx

# Method 1: Programmatic creation
def create_expectations_programmatically(context):
    """Create expectations using code"""
    
    # Create expectation suite
    suite = context.create_expectation_suite("programmatic_suite", overwrite_existing=True)
    
    # Add table-level expectations
    suite.expect_table_row_count_to_be_between(min_value=1000, max_value=10000)
    suite.expect_table_column_count_to_equal(10)
    
    # Add column-level expectations
    suite.expect_column_to_exist("customer_id")
    suite.expect_column_values_to_not_be_null("customer_id")
    suite.expect_column_values_to_be_unique("customer_id")
    suite.expect_column_values_to_be_of_type("customer_id", "int64")
    
    # Add pattern-based expectations
    suite.expect_column_values_to_match_regex(
        "email", 
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        meta={"notes": "Email format validation"}
    )
    
    # Add range-based expectations
    suite.expect_column_values_to_be_between(
        "age", 
        min_value=0, 
        max_value=120,
        meta={"critical": True}
    )
    
    context.save_expectation_suite(suite)
    return suite

# Method 2: Interactive creation using validator
def create_expectations_interactively(validator):
    """Create expectations interactively"""
    
    # Basic existence and null checks
    validator.expect_column_to_exist("customer_id")
    validator.expect_column_values_to_not_be_null("customer_id")
    
    # Uniqueness validation
    validator.expect_column_values_to_be_unique("email")
    
    # Set membership validation
    validator.expect_column_values_to_be_in_set(
        "country", ["US", "CA", "UK", "DE", "FR"]
    )
    
    # Statistical expectations
    validator.expect_column_mean_to_be_between("order_value", 10, 1000)
    validator.expect_column_stdev_to_be_between("order_value", 5, 500)
    
    # Multi-column expectations
    validator.expect_multicolumn_values_to_be_unique(["customer_id", "order_date"])
    validator.expect_column_pair_values_A_to_be_greater_than_B("end_date", "start_date")
    
    # Save expectations to suite
    validator.save_expectation_suite()

# Method 3: Profiler-based creation
def create_expectations_with_profiler(context, validator):
    """Create expectations using automated profiler"""
    
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
    context.save_expectation_suite(suite)
    return suite
```

### 7. What is data profiling and how is it different from data validation?
**Answer:**
**Data Profiling** is the process of examining and analyzing data to understand its structure, content, quality, and relationships.

**Data Validation** is the process of checking data against predefined rules and expectations.

```python
import pandas as pd
import numpy as np

# Data Profiling Example
def comprehensive_data_profile(df):
    """Generate comprehensive data profile"""
    
    profile = {
        'dataset_info': {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'memory_usage': df.memory_usage(deep=True).sum(),
            'duplicate_rows': len(df) - len(df.drop_duplicates())
        },
        'column_profiles': {}
    }
    
    for column in df.columns:
        col_profile = {
            'data_type': str(df[column].dtype),
            'null_count': df[column].isnull().sum(),
            'null_percentage': (df[column].isnull().sum() / len(df)) * 100,
            'unique_count': df[column].nunique(),
            'unique_percentage': (df[column].nunique() / len(df)) * 100
        }
        
        # Numeric column profiling
        if df[column].dtype in ['int64', 'float64']:
            col_profile.update({
                'min': df[column].min(),
                'max': df[column].max(),
                'mean': df[column].mean(),
                'median': df[column].median(),
                'std': df[column].std(),
                'q25': df[column].quantile(0.25),
                'q75': df[column].quantile(0.75),
                'skewness': df[column].skew(),
                'kurtosis': df[column].kurtosis()
            })
        
        # String column profiling
        elif df[column].dtype == 'object':
            col_profile.update({
                'avg_length': df[column].str.len().mean(),
                'min_length': df[column].str.len().min(),
                'max_length': df[column].str.len().max(),
                'most_common': df[column].value_counts().head(5).to_dict()
            })
        
        profile['column_profiles'][column] = col_profile
    
    return profile

# Data Validation Example
def validate_profiled_data(validator, profile_results):
    """Validate data based on profiling results"""
    
    # Use profiling results to create dynamic expectations
    for column, col_profile in profile_results['column_profiles'].items():
        
        # Null validation based on profiling
        if col_profile['null_percentage'] < 5:
            validator.expect_column_values_to_not_be_null(column)
        else:
            validator.expect_column_values_to_not_be_null(
                column, 
                mostly=(100 - col_profile['null_percentage']) / 100
            )
        
        # Uniqueness validation
        if col_profile['unique_percentage'] > 95:
            validator.expect_column_values_to_be_unique(column)
        
        # Range validation for numeric columns
        if column in ['age', 'price', 'quantity']:
            if 'min' in col_profile and 'max' in col_profile:
                validator.expect_column_values_to_be_between(
                    column,
                    min_value=col_profile['min'],
                    max_value=col_profile['max']
                )

# Great Expectations Profiling
def profile_with_great_expectations(context, batch_request):
    """Profile data using Great Expectations"""
    
    from great_expectations.profile.user_configurable_profiler import UserConfigurableProfiler
    
    # Get validator
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name="profiling_suite"
    )
    
    # Create profiler
    profiler = UserConfigurableProfiler(
        profile_dataset=validator,
        excluded_expectations=None,
        ignored_columns=None,
        not_null_only=False,
        primary_or_compound_key=None,
        semantic_types_dict=None,
        table_expectations_only=False,
        value_set_threshold="MANY"
    )
    
    # Generate suite from profiling
    suite = profiler.build_suite()
    
    return suite
```

### 8. How do you handle data quality issues in streaming data?
**Answer:**
Streaming data quality requires real-time validation and handling strategies:

```python
from kafka import KafkaConsumer, KafkaProducer
import json
import great_expectations as gx
from datetime import datetime

class StreamingDataQualityProcessor:
    def __init__(self, context, suite_name):
        self.context = context
        self.suite_name = suite_name
        self.producer = KafkaProducer(
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        self.quality_metrics = {
            'total_records': 0,
            'valid_records': 0,
            'invalid_records': 0,
            'error_types': {}
        }
    
    def process_stream(self, input_topic, output_topic, error_topic):
        """Process streaming data with quality validation"""
        
        consumer = KafkaConsumer(
            input_topic,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        
        for message in consumer:
            record = message.value
            self.quality_metrics['total_records'] += 1
            
            # Validate record
            validation_result = self.validate_record(record)
            
            if validation_result['is_valid']:
                # Send valid record to output topic
                self.producer.send(output_topic, record)
                self.quality_metrics['valid_records'] += 1
            else:
                # Handle invalid record
                self.handle_invalid_record(record, validation_result, error_topic)
                self.quality_metrics['invalid_records'] += 1
            
            # Update quality metrics
            self.update_quality_metrics(validation_result)
    
    def validate_record(self, record):
        """Validate individual record"""
        
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Basic structure validation
        required_fields = ['customer_id', 'timestamp', 'event_type']
        for field in required_fields:
            if field not in record:
                validation_result['is_valid'] = False
                validation_result['errors'].append(f"Missing required field: {field}")
        
        # Data type validation
        if 'customer_id' in record:
            if not isinstance(record['customer_id'], (int, str)):
                validation_result['is_valid'] = False
                validation_result['errors'].append("customer_id must be int or string")
        
        # Business rule validation
        if 'amount' in record:
            if record['amount'] < 0:
                validation_result['is_valid'] = False
                validation_result['errors'].append("Amount cannot be negative")
            elif record['amount'] > 10000:
                validation_result['warnings'].append("High amount detected")
        
        # Timestamp validation
        if 'timestamp' in record:
            try:
                timestamp = datetime.fromisoformat(record['timestamp'])
                if timestamp > datetime.now():
                    validation_result['warnings'].append("Future timestamp detected")
            except ValueError:
                validation_result['is_valid'] = False
                validation_result['errors'].append("Invalid timestamp format")
        
        return validation_result
    
    def handle_invalid_record(self, record, validation_result, error_topic):
        """Handle invalid records"""
        
        error_record = {
            'original_record': record,
            'validation_errors': validation_result['errors'],
            'validation_warnings': validation_result['warnings'],
            'timestamp': datetime.now().isoformat(),
            'processor': 'streaming_quality_processor'
        }
        
        # Send to error topic for further analysis
        self.producer.send(error_topic, error_record)
        
        # Log error for monitoring
        print(f"Invalid record detected: {validation_result['errors']}")
    
    def update_quality_metrics(self, validation_result):
        """Update quality metrics"""
        
        for error in validation_result['errors']:
            error_type = error.split(':')[0] if ':' in error else error
            self.quality_metrics['error_types'][error_type] = \
                self.quality_metrics['error_types'].get(error_type, 0) + 1
    
    def get_quality_report(self):
        """Generate quality report"""
        
        total = self.quality_metrics['total_records']
        if total == 0:
            return "No records processed"
        
        quality_score = (self.quality_metrics['valid_records'] / total) * 100
        
        return {
            'quality_score': quality_score,
            'total_records': total,
            'valid_records': self.quality_metrics['valid_records'],
            'invalid_records': self.quality_metrics['invalid_records'],
            'error_breakdown': self.quality_metrics['error_types']
        }

# Usage example
processor = StreamingDataQualityProcessor(context, "streaming_quality_suite")
processor.process_stream("input_topic", "clean_data_topic", "error_topic")
```

### 9. What are checkpoints in Great Expectations?
**Answer:**
Checkpoints in Great Expectations are automated validation workflows that combine data batches, expectation suites, and actions into a single, executable unit.

```python
import great_expectations as gx

# Basic Checkpoint Configuration
def create_basic_checkpoint(context):
    """Create a basic checkpoint"""
    
    checkpoint_config = {
        "name": "customer_data_checkpoint",
        "config_version": 1.0,
        "template_name": None,
        "module_name": "great_expectations.checkpoint",
        "class_name": "Checkpoint",
        "run_name_template": "%Y%m%d-%H%M%S-customer-validation",
        "expectation_suite_name": "customer_data_suite",
        "batch_request": {
            "datasource_name": "production_db",
            "data_connector_name": "default_inferred_data_connector",
            "data_asset_name": "customers"
        },
        "action_list": [
            {
                "name": "store_validation_result",
                "action": {
                    "class_name": "StoreValidationResultAction"
                }
            },
            {
                "name": "update_data_docs",
                "action": {
                    "class_name": "UpdateDataDocsAction"
                }
            },
            {
                "name": "send_slack_notification",
                "action": {
                    "class_name": "SlackNotificationAction",
                    "slack_webhook": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
                    "notify_on": "failure"
                }
            }
        ]
    }
    
    context.add_checkpoint(**checkpoint_config)
    return checkpoint_config

# Advanced Checkpoint with Multiple Suites
def create_advanced_checkpoint(context):
    """Create checkpoint with multiple validation suites"""
    
    checkpoint_config = {
        "name": "comprehensive_data_checkpoint",
        "config_version": 1.0,
        "template_name": None,
        "module_name": "great_expectations.checkpoint",
        "class_name": "Checkpoint",
        "run_name_template": "%Y%m%d-%H%M%S-comprehensive-validation",
        "validations": [
            {
                "batch_request": {
                    "datasource_name": "production_db",
                    "data_connector_name": "default_inferred_data_connector",
                    "data_asset_name": "customers"
                },
                "expectation_suite_name": "customer_data_suite"
            },
            {
                "batch_request": {
                    "datasource_name": "production_db",
                    "data_connector_name": "default_inferred_data_connector",
                    "data_asset_name": "orders"
                },
                "expectation_suite_name": "order_data_suite"
            },
            {
                "batch_request": {
                    "datasource_name": "production_db",
                    "data_connector_name": "default_inferred_data_connector",
                    "data_asset_name": "products"
                },
                "expectation_suite_name": "product_data_suite"
            }
        ],
        "action_list": [
            {
                "name": "store_validation_result",
                "action": {
                    "class_name": "StoreValidationResultAction"
                }
            },
            {
                "name": "update_data_docs",
                "action": {
                    "class_name": "UpdateDataDocsAction"
                }
            },
            {
                "name": "email_notification",
                "action": {
                    "class_name": "EmailAction",
                    "smtp_address": "smtp.company.com",
                    "smtp_port": 587,
                    "sender_login": "data-quality@company.com",
                    "sender_password": "${EMAIL_PASSWORD}",
                    "receiver_emails": ["data-team@company.com"],
                    "notify_on": "failure"
                }
            }
        ]
    }
    
    context.add_checkpoint(**checkpoint_config)
    return checkpoint_config

# Running Checkpoints
def run_checkpoint_examples(context):
    """Examples of running checkpoints"""
    
    # Simple checkpoint run
    result = context.run_checkpoint(checkpoint_name="customer_data_checkpoint")
    
    # Checkpoint run with runtime parameters
    result = context.run_checkpoint(
        checkpoint_name="customer_data_checkpoint",
        batch_request={
            "datasource_name": "production_db",
            "data_connector_name": "default_inferred_data_connector",
            "data_asset_name": "customers",
            "data_connector_query": {
                "batch_filter_parameters": {
                    "date": "2023-12-01"
                }
            }
        }
    )
    
    # Process checkpoint results
    if result.success:
        print("All validations passed!")
        for validation_result in result.run_results.values():
            print(f"Suite: {validation_result.meta['expectation_suite_name']}")
            print(f"Success: {validation_result.success}")
            print(f"Statistics: {validation_result.statistics}")
    else:
        print("Some validations failed!")
        for validation_result in result.run_results.values():
            if not validation_result.success:
                print(f"Failed suite: {validation_result.meta['expectation_suite_name']}")
                for expectation_result in validation_result.results:
                    if not expectation_result.success:
                        print(f"Failed expectation: {expectation_result.expectation_config}")

# Scheduled Checkpoint Execution
def schedule_checkpoint_execution(context):
    """Schedule checkpoint execution"""
    
    import schedule
    import time
    
    def run_daily_validation():
        """Daily validation job"""
        try:
            result = context.run_checkpoint(checkpoint_name="daily_quality_checkpoint")
            
            if not result.success:
                # Handle validation failures
                send_alert("Daily data quality validation failed")
                log_validation_failures(result)
            
            # Update quality dashboard
            update_quality_dashboard(result)
            
        except Exception as e:
            send_critical_alert(f"Checkpoint execution failed: {str(e)}")
    
    # Schedule daily at 6 AM
    schedule.every().day.at("06:00").do(run_daily_validation)
    
    # Schedule hourly for critical data
    schedule.every().hour.do(lambda: context.run_checkpoint("hourly_critical_checkpoint"))
    
    # Keep scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)
```

### 10. How do you integrate data quality checks into CI/CD pipelines?
**Answer:**
Integrating data quality into CI/CD ensures that data issues are caught early in the development process:

```yaml
# .github/workflows/data-quality-ci.yml
name: Data Quality CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
    paths:
      - 'data/**'
      - 'expectations/**'
      - 'pipelines/**'
  pull_request:
    branches: [ main ]

jobs:
  data-quality-validation:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install great-expectations pandas sqlalchemy psycopg2-binary
        pip install -r requirements.txt
    
    - name: Set up test data
      run: |
        python scripts/setup_test_data.py
    
    - name: Run data quality tests
      run: |
        python scripts/run_data_quality_tests.py
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
    
    - name: Generate data quality report
      run: |
        great_expectations docs build
    
    - name: Upload data quality results
      uses: actions/upload-artifact@v3
      with:
        name: data-quality-results
        path: |
          great_expectations/uncommitted/data_docs/
          great_expectations/uncommitted/validations/
    
    - name: Comment PR with results
      if: github.event_name == 'pull_request'
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          const path = './great_expectations/uncommitted/validations/';
          
          // Read validation results
          const files = fs.readdirSync(path);
          const latestResult = files[files.length - 1];
          const result = JSON.parse(fs.readFileSync(path + latestResult));
          
          // Create comment
          const success = result.success;
          const statistics = result.statistics;
          
          const comment = `
          ## Data Quality Validation Results
          
          **Status**: ${success ? '✅ PASSED' : '❌ FAILED'}
          
          **Statistics**:
          - Evaluated Expectations: ${statistics.evaluated_expectations}
          - Successful Expectations: ${statistics.successful_expectations}
          - Success Percentage: ${statistics.success_percent}%
          
          ${success ? '' : '⚠️ Please review and fix data quality issues before merging.'}
          `;
          
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: comment
          });

  deploy-to-staging:
    needs: data-quality-validation
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    
    steps:
    - name: Deploy to staging
      run: |
        echo "Deploying to staging environment"
        # Add deployment steps here

  deploy-to-production:
    needs: data-quality-validation
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Run production data quality gate
      run: |
        python scripts/production_quality_gate.py
    
    - name: Deploy to production
      run: |
        echo "Deploying to production environment"
        # Add deployment steps here
```

```python
# scripts/run_data_quality_tests.py
import great_expectations as gx
import sys
import os

def run_data_quality_tests():
    """Run data quality tests in CI/CD pipeline"""
    
    # Initialize context
    context = gx.get_context()
    
    # Define test checkpoints
    test_checkpoints = [
        "customer_data_test_checkpoint",
        "order_data_test_checkpoint",
        "product_data_test_checkpoint"
    ]
    
    all_passed = True
    results_summary = []
    
    for checkpoint_name in test_checkpoints:
        try:
            print(f"Running checkpoint: {checkpoint_name}")
            result = context.run_checkpoint(checkpoint_name=checkpoint_name)
            
            success = result.success
            statistics = result.statistics
            
            results_summary.append({
                'checkpoint': checkpoint_name,
                'success': success,
                'statistics': statistics
            })
            
            if not success:
                all_passed = False
                print(f"❌ {checkpoint_name} FAILED")
                
                # Log detailed failures
                for validation_result in result.run_results.values():
                    if not validation_result.success:
                        for expectation_result in validation_result.results:
                            if not expectation_result.success:
                                print(f"  Failed: {expectation_result.expectation_config}")
            else:
                print(f"✅ {checkpoint_name} PASSED")
        
        except Exception as e:
            print(f"❌ Error running {checkpoint_name}: {str(e)}")
            all_passed = False
    
    # Generate summary report
    print("\n" + "="*50)
    print("DATA QUALITY TEST SUMMARY")
    print("="*50)
    
    for result in results_summary:
        status = "PASSED" if result['success'] else "FAILED"
        stats = result['statistics']
        print(f"{result['checkpoint']}: {status}")
        print(f"  Success Rate: {stats['success_percent']}%")
        print(f"  Expectations: {stats['successful_expectations']}/{stats['evaluated_expectations']}")
    
    # Exit with appropriate code
    if all_passed:
        print("\n🎉 All data quality tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Some data quality tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    run_data_quality_tests()
```

```python
# scripts/production_quality_gate.py
import great_expectations as gx
import sys
from datetime import datetime, timedelta

def production_quality_gate():
    """Production quality gate with strict validation"""
    
    context = gx.get_context()
    
    # Critical production checkpoints
    critical_checkpoints = [
        "production_customer_checkpoint",
        "production_transaction_checkpoint",
        "production_inventory_checkpoint"
    ]
    
    # Quality thresholds for production
    quality_thresholds = {
        'min_success_rate': 95.0,  # Minimum 95% success rate
        'max_critical_failures': 0,  # No critical failures allowed
        'max_data_age_hours': 2  # Data must be fresh (within 2 hours)
    }
    
    gate_passed = True
    
    for checkpoint_name in critical_checkpoints:
        print(f"Validating production checkpoint: {checkpoint_name}")
        
        result = context.run_checkpoint(checkpoint_name=checkpoint_name)
        
        # Check success rate
        success_rate = result.statistics['success_percent']
        if success_rate < quality_thresholds['min_success_rate']:
            print(f"❌ Success rate {success_rate}% below threshold {quality_thresholds['min_success_rate']}%")
            gate_passed = False
        
        # Check for critical failures
        critical_failures = 0
        for validation_result in result.run_results.values():
            for expectation_result in validation_result.results:
                if not expectation_result.success:
                    if expectation_result.expectation_config.meta.get('critical', False):
                        critical_failures += 1
        
        if critical_failures > quality_thresholds['max_critical_failures']:
            print(f"❌ {critical_failures} critical failures detected")
            gate_passed = False
        
        # Check data freshness (if applicable)
        # This would be implemented based on your specific data sources
        
        if gate_passed:
            print(f"✅ {checkpoint_name} passed production quality gate")
        else:
            print(f"❌ {checkpoint_name} failed production quality gate")
    
    if gate_passed:
        print("\n🚀 Production quality gate PASSED - Safe to deploy!")
        sys.exit(0)
    else:
        print("\n🛑 Production quality gate FAILED - Deployment blocked!")
        sys.exit(1)

if __name__ == "__main__":
    production_quality_gate()
```

### 11. What are the common data quality issues you encounter in production?
**Answer:**
Common data quality issues in production environments include:

```python
# Common Data Quality Issues and Detection

def detect_common_quality_issues(df):
    """Detect common data quality issues"""
    
    issues = {
        'missing_data': {},
        'duplicates': {},
        'outliers': {},
        'inconsistencies': {},
        'format_issues': {},
        'referential_integrity': {}
    }
    
    # 1. Missing Data Issues
    for column in df.columns:
        null_count = df[column].isnull().sum()
        null_percentage = (null_count / len(df)) * 100
        
        if null_percentage > 0:
            issues['missing_data'][column] = {
                'null_count': null_count,
                'null_percentage': null_percentage,
                'severity': 'high' if null_percentage > 20 else 'medium' if null_percentage > 5 else 'low'
            }
    
    # 2. Duplicate Issues
    duplicate_rows = len(df) - len(df.drop_duplicates())
    if duplicate_rows > 0:
        issues['duplicates']['total_duplicates'] = duplicate_rows
        issues['duplicates']['duplicate_percentage'] = (duplicate_rows / len(df)) * 100
    
    # Check for duplicate keys
    key_columns = ['id', 'customer_id', 'order_id', 'email']
    for col in key_columns:
        if col in df.columns:
            duplicates = df[col].duplicated().sum()
            if duplicates > 0:
                issues['duplicates'][f'{col}_duplicates'] = duplicates
    
    # 3. Outlier Detection
    numeric_columns = df.select_dtypes(include=['number']).columns
    for col in numeric_columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        if len(outliers) > 0:
            issues['outliers'][col] = {
                'outlier_count': len(outliers),
                'outlier_percentage': (len(outliers) / len(df)) * 100,
                'bounds': {'lower': lower_bound, 'upper': upper_bound}
            }
    
    # 4. Format Inconsistencies
    text_columns = df.select_dtypes(include=['object']).columns
    for col in text_columns:
        if col in ['email', 'phone', 'date']:
            # Email format issues
            if 'email' in col.lower():
                invalid_emails = df[~df[col].str.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', na=False)]
                if len(invalid_emails) > 0:
                    issues['format_issues'][f'{col}_invalid_format'] = len(invalid_emails)
            
            # Phone format issues
            if 'phone' in col.lower():
                invalid_phones = df[~df[col].str.match(r'^\+?1?[0-9]{10,15}$', na=False)]
                if len(invalid_phones) > 0:
                    issues['format_issues'][f'{col}_invalid_format'] = len(invalid_phones)
    
    return issues

# Great Expectations implementation for common issues
def create_common_issue_expectations(validator):
    """Create expectations to catch common data quality issues"""
    
    # 1. Missing Data Expectations
    validator.expect_column_values_to_not_be_null("customer_id")
    validator.expect_column_values_to_not_be_null("email")
    validator.expect_column_values_to_not_be_null("order_date", mostly=0.95)  # Allow 5% nulls
    
    # 2. Duplicate Prevention
    validator.expect_column_values_to_be_unique("customer_id")
    validator.expect_column_values_to_be_unique("email")
    validator.expect_compound_columns_to_be_unique(["customer_id", "order_date"])
    
    # 3. Outlier Detection
    validator.expect_column_values_to_be_between("age", 0, 120)
    validator.expect_column_values_to_be_between("order_amount", 0.01, 10000)
    validator.expect_column_quantile_values_to_be_between(
        "income",
        quantile_ranges={
            "quantiles": [0.05, 0.95],
            "value_ranges": [[10000, 20000], [200000, 500000]]
        }
    )
    
    # 4. Format Validation
    validator.expect_column_values_to_match_regex(
        "email", r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    validator.expect_column_values_to_match_regex(
        "phone", r'^\+?1?[0-9]{10,15}$'
    )
    validator.expect_column_values_to_match_strftime_format(
        "order_date", "%Y-%m-%d"
    )
    
    # 5. Referential Integrity
    valid_statuses = ["active", "inactive", "pending", "cancelled"]
    validator.expect_column_values_to_be_in_set("status", valid_statuses)
    
    valid_countries = ["US", "CA", "UK", "DE", "FR", "AU"]
    validator.expect_column_values_to_be_in_set("country", valid_countries)
```

### 12. How do you measure data quality?
**Answer:**
Data quality can be measured using various metrics and KPIs:

```python
import pandas as pd
import numpy as np
from datetime import datetime

class DataQualityMetrics:
    def __init__(self, df):
        self.df = df
        self.metrics = {}
    
    def calculate_completeness_score(self):
        """Calculate completeness score (0-100)"""
        total_cells = len(self.df) * len(self.df.columns)
        non_null_cells = self.df.count().sum()
        completeness = (non_null_cells / total_cells) * 100
        
        self.metrics['completeness'] = {
            'score': completeness,
            'total_cells': total_cells,
            'non_null_cells': non_null_cells,
            'null_cells': total_cells - non_null_cells
        }
        return completeness
    
    def calculate_uniqueness_score(self, key_columns):
        """Calculate uniqueness score for key columns"""
        uniqueness_scores = {}
        
        for column in key_columns:
            if column in self.df.columns:
                total_records = len(self.df)
                unique_records = self.df[column].nunique()
                uniqueness = (unique_records / total_records) * 100
                
                uniqueness_scores[column] = {
                    'score': uniqueness,
                    'total_records': total_records,
                    'unique_records': unique_records,
                    'duplicate_records': total_records - unique_records
                }
        
        self.metrics['uniqueness'] = uniqueness_scores
        return uniqueness_scores
    
    def calculate_validity_score(self, validation_rules):
        """Calculate validity score based on business rules"""
        validity_results = {}
        total_validations = 0
        passed_validations = 0
        
        for column, rules in validation_rules.items():
            if column not in self.df.columns:
                continue
            
            column_results = {}
            
            for rule_name, rule_func in rules.items():
                try:
                    valid_mask = rule_func(self.df[column])
                    valid_count = valid_mask.sum()
                    total_count = len(self.df)
                    
                    validity_percentage = (valid_count / total_count) * 100
                    
                    column_results[rule_name] = {
                        'score': validity_percentage,
                        'valid_records': valid_count,
                        'invalid_records': total_count - valid_count,
                        'total_records': total_count
                    }
                    
                    total_validations += 1
                    if validity_percentage >= 95:  # 95% threshold
                        passed_validations += 1
                
                except Exception as e:
                    column_results[rule_name] = {'error': str(e)}
            
            validity_results[column] = column_results
        
        overall_validity = (passed_validations / total_validations) * 100 if total_validations > 0 else 0
        
        self.metrics['validity'] = {
            'overall_score': overall_validity,
            'passed_validations': passed_validations,
            'total_validations': total_validations,
            'column_results': validity_results
        }
        
        return validity_results
    
    def calculate_overall_quality_score(self, weights=None):
        """Calculate weighted overall quality score"""
        if weights is None:
            weights = {
                'completeness': 0.25,
                'uniqueness': 0.20,
                'validity': 0.25,
                'consistency': 0.15,
                'timeliness': 0.15
            }
        
        overall_score = 0
        total_weight = 0
        
        # Completeness
        if 'completeness' in self.metrics:
            overall_score += self.metrics['completeness']['score'] * weights['completeness']
            total_weight += weights['completeness']
        
        # Uniqueness (average across key columns)
        if 'uniqueness' in self.metrics:
            uniqueness_scores = [v['score'] for v in self.metrics['uniqueness'].values()]
            avg_uniqueness = np.mean(uniqueness_scores) if uniqueness_scores else 0
            overall_score += avg_uniqueness * weights['uniqueness']
            total_weight += weights['uniqueness']
        
        # Validity
        if 'validity' in self.metrics:
            overall_score += self.metrics['validity']['overall_score'] * weights['validity']
            total_weight += weights['validity']
        
        final_score = overall_score / total_weight if total_weight > 0 else 0
        
        self.metrics['overall_quality'] = {
            'score': final_score,
            'weights_used': weights,
            'total_weight': total_weight
        }
        
        return final_score
```

### 13. What is the difference between data validation and data verification?
**Answer:**
**Data Validation** checks if data conforms to predefined rules and constraints.
**Data Verification** confirms that data accurately represents the real-world entity or event.

```python
# Data Validation Example
def data_validation_example(validator):
    """Data validation checks format and rules compliance"""
    
    # Format validation
    validator.expect_column_values_to_match_regex(
        "email", r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    
    # Range validation
    validator.expect_column_values_to_be_between("age", 0, 120)
    
    # Type validation
    validator.expect_column_values_to_be_of_type("customer_id", "int64")
    
    # Null validation
    validator.expect_column_values_to_not_be_null("customer_id")
    
    # Set membership validation
    validator.expect_column_values_to_be_in_set(
        "status", ["active", "inactive", "pending"]
    )

# Data Verification Example
def data_verification_example():
    """Data verification checks accuracy against source systems"""
    
    import requests
    import pandas as pd
    
    def verify_customer_data(df):
        """Verify customer data against external systems"""
        
        verification_results = []
        
        for _, row in df.iterrows():
            customer_id = row['customer_id']
            email = row['email']
            phone = row['phone']
            
            # Verify email exists and is deliverable
            email_verification = verify_email_deliverability(email)
            
            # Verify phone number is valid and active
            phone_verification = verify_phone_number(phone)
            
            # Verify customer exists in CRM system
            crm_verification = verify_customer_in_crm(customer_id)
            
            verification_results.append({
                'customer_id': customer_id,
                'email_verified': email_verification['is_valid'],
                'phone_verified': phone_verification['is_active'],
                'crm_verified': crm_verification['exists']
            })
        
        return pd.DataFrame(verification_results)
```

### 14. How do you handle data quality in streaming data?
**Answer:**
Streaming data quality requires real-time validation and handling strategies:

```python
from kafka import KafkaConsumer, KafkaProducer
import json
import great_expectations as gx
from datetime import datetime

class StreamingDataQualityProcessor:
    def __init__(self, context, suite_name):
        self.context = context
        self.suite_name = suite_name
        self.producer = KafkaProducer(
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        self.quality_metrics = {
            'total_records': 0,
            'valid_records': 0,
            'invalid_records': 0,
            'error_types': {}
        }
    
    def process_stream(self, input_topic, output_topic, error_topic):
        """Process streaming data with quality validation"""
        
        consumer = KafkaConsumer(
            input_topic,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        
        for message in consumer:
            record = message.value
            self.quality_metrics['total_records'] += 1
            
            # Validate record
            validation_result = self.validate_record(record)
            
            if validation_result['is_valid']:
                # Send valid record to output topic
                self.producer.send(output_topic, record)
                self.quality_metrics['valid_records'] += 1
            else:
                # Handle invalid record
                self.handle_invalid_record(record, validation_result, error_topic)
                self.quality_metrics['invalid_records'] += 1
    
    def validate_record(self, record):
        """Validate individual record"""
        
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Basic structure validation
        required_fields = ['customer_id', 'timestamp', 'event_type']
        for field in required_fields:
            if field not in record:
                validation_result['is_valid'] = False
                validation_result['errors'].append(f"Missing required field: {field}")
        
        # Business rule validation
        if 'amount' in record:
            if record['amount'] < 0:
                validation_result['is_valid'] = False
                validation_result['errors'].append("Amount cannot be negative")
        
        return validation_result
```

### 15. What are checkpoints in Great Expectations?
**Answer:**
Checkpoints in Great Expectations are automated validation workflows that combine data batches, expectation suites, and actions into a single, executable unit.

```python
import great_expectations as gx

# Basic Checkpoint Configuration
def create_basic_checkpoint(context):
    """Create a basic checkpoint"""
    
    checkpoint_config = {
        "name": "customer_data_checkpoint",
        "config_version": 1.0,
        "template_name": None,
        "module_name": "great_expectations.checkpoint",
        "class_name": "Checkpoint",
        "run_name_template": "%Y%m%d-%H%M%S-customer-validation",
        "expectation_suite_name": "customer_data_suite",
        "batch_request": {
            "datasource_name": "production_db",
            "data_connector_name": "default_inferred_data_connector",
            "data_asset_name": "customers"
        },
        "action_list": [
            {
                "name": "store_validation_result",
                "action": {
                    "class_name": "StoreValidationResultAction"
                }
            },
            {
                "name": "update_data_docs",
                "action": {
                    "class_name": "UpdateDataDocsAction"
                }
            }
        ]
    }
    
    context.add_checkpoint(**checkpoint_config)
    return checkpoint_config

# Running Checkpoints
def run_checkpoint_examples(context):
    """Examples of running checkpoints"""
    
    # Simple checkpoint run
    result = context.run_checkpoint(checkpoint_name="customer_data_checkpoint")
    
    # Process checkpoint results
    if result.success:
        print("All validations passed!")
    else:
        print("Some validations failed!")
        for validation_result in result.run_results.values():
            if not validation_result.success:
                print(f"Failed suite: {validation_result.meta['expectation_suite_name']}")
```

### 16. How do you integrate data quality checks into CI/CD pipelines?
**Answer:**
Integrating data quality into CI/CD ensures that data issues are caught early in the development process:

```yaml
# .github/workflows/data-quality-ci.yml
name: Data Quality CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
    paths:
      - 'data/**'
      - 'expectations/**'
      - 'pipelines/**'
  pull_request:
    branches: [ main ]

jobs:
  data-quality-validation:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install great-expectations pandas sqlalchemy
        pip install -r requirements.txt
    
    - name: Run data quality tests
      run: |
        python scripts/run_data_quality_tests.py
    
    - name: Generate data quality report
      run: |
        great_expectations docs build
    
    - name: Upload data quality results
      uses: actions/upload-artifact@v3
      with:
        name: data-quality-results
        path: |
          great_expectations/uncommitted/data_docs/
          great_expectations/uncommitted/validations/
```

### 17. What is data profiling and how is it different from data validation?
**Answer:**
**Data Profiling** is the process of examining and analyzing data to understand its structure, content, quality, and relationships.
**Data Validation** is the process of checking data against predefined rules and expectations.

```python
import pandas as pd
import numpy as np

# Data Profiling Example
def comprehensive_data_profile(df):
    """Generate comprehensive data profile"""
    
    profile = {
        'dataset_info': {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'memory_usage': df.memory_usage(deep=True).sum(),
            'duplicate_rows': len(df) - len(df.drop_duplicates())
        },
        'column_profiles': {}
    }
    
    for column in df.columns:
        col_profile = {
            'data_type': str(df[column].dtype),
            'null_count': df[column].isnull().sum(),
            'null_percentage': (df[column].isnull().sum() / len(df)) * 100,
            'unique_count': df[column].nunique(),
            'unique_percentage': (df[column].nunique() / len(df)) * 100
        }
        
        # Numeric column profiling
        if df[column].dtype in ['int64', 'float64']:
            col_profile.update({
                'min': df[column].min(),
                'max': df[column].max(),
                'mean': df[column].mean(),
                'median': df[column].median(),
                'std': df[column].std()
            })
        
        # String column profiling
        elif df[column].dtype == 'object':
            col_profile.update({
                'avg_length': df[column].str.len().mean(),
                'min_length': df[column].str.len().min(),
                'max_length': df[column].str.len().max()
            })
        
        profile['column_profiles'][column] = col_profile
    
    return profile

# Great Expectations Profiling
def profile_with_great_expectations(context, batch_request):
    """Profile data using Great Expectations"""
    
    from great_expectations.profile.user_configurable_profiler import UserConfigurableProfiler
    
    # Get validator
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name="profiling_suite"
    )
    
    # Create profiler
    profiler = UserConfigurableProfiler(
        profile_dataset=validator,
        excluded_expectations=None,
        ignored_columns=None,
        not_null_only=False,
        primary_or_compound_key=None,
        semantic_types_dict=None,
        table_expectations_only=False,
        value_set_threshold="MANY"
    )
    
    # Generate suite from profiling
    suite = profiler.build_suite()
    
    return suite
```

### 18. How do you create custom expectations in Great Expectations?
**Answer:**
Custom expectations allow you to implement business-specific validation rules:

```python
from great_expectations.expectations import ExpectationConfiguration
from great_expectations.execution_engine import PandasExecutionEngine
from great_expectations.expectations import ColumnMapExpectation

class ExpectColumnValuesToBeValidCreditCard(ColumnMapExpectation):
    """Expect column values to be valid credit card numbers"""
    
    map_metric = "column_values.valid_credit_card"
    success_keys = ("mostly",)
    
    @classmethod
    def _prescriptive_template(cls, renderer_type):
        return {
            "content_block_type": "string_template",
            "string_template": {
                "template": "Values in column $column must be valid credit card numbers.",
                "params": {"column": "$column"},
            },
        }

# Register custom metric
from great_expectations.metrics import ColumnMetricProvider, column_condition_partial

class ColumnValuesValidCreditCard(ColumnMetricProvider):
    metric_name = "column_values.valid_credit_card"
    
    @column_condition_partial(engine=PandasExecutionEngine)
    def _pandas(cls, column, **kwargs):
        def is_valid_credit_card(card_number):
            # Luhn algorithm implementation
            if not isinstance(card_number, str):
                return False
            
            # Remove spaces and dashes
            card_number = card_number.replace(" ", "").replace("-", "")
            
            # Check if all digits
            if not card_number.isdigit():
                return False
            
            # Luhn algorithm
            total = 0
            reverse_digits = card_number[::-1]
            
            for i, digit in enumerate(reverse_digits):
                n = int(digit)
                if i % 2 == 1:
                    n *= 2
                    if n > 9:
                        n = (n // 10) + (n % 10)
                total += n
            
            return total % 10 == 0
        
        return column.apply(is_valid_credit_card)

# Usage of custom expectation
validator.expect_column_values_to_be_valid_credit_card("credit_card_number")
```

### 19. How do you monitor data quality in production?
**Answer:**
Production data quality monitoring requires continuous assessment and alerting:

```python
import schedule
import time
from datetime import datetime, timedelta

class ProductionDataQualityMonitor:
    def __init__(self, context, alert_config):
        self.context = context
        self.alert_config = alert_config
        self.quality_history = []
    
    def run_continuous_monitoring(self):
        """Run continuous data quality monitoring"""
        
        # Schedule different monitoring frequencies
        schedule.every(5).minutes.do(self.monitor_critical_data)
        schedule.every().hour.do(self.monitor_standard_data)
        schedule.every().day.at("06:00").do(self.generate_daily_report)
        
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    def monitor_critical_data(self):
        """Monitor critical data every 5 minutes"""
        
        critical_checkpoints = [
            "payment_data_checkpoint",
            "user_authentication_checkpoint",
            "transaction_checkpoint"
        ]
        
        for checkpoint_name in critical_checkpoints:
            try:
                result = self.context.run_checkpoint(checkpoint_name=checkpoint_name)
                
                if not result.success:
                    self.handle_critical_failure(checkpoint_name, result)
                
                self.record_quality_metrics(checkpoint_name, result)
                
            except Exception as e:
                self.handle_monitoring_error(checkpoint_name, str(e))
    
    def handle_critical_failure(self, checkpoint_name, result):
        """Handle critical data quality failures"""
        
        # Send immediate alert
        alert_message = f"CRITICAL: Data quality failure in {checkpoint_name}"
        self.send_alert(alert_message, severity="critical")
        
        # Log detailed failure information
        failure_details = self.extract_failure_details(result)
        self.log_failure(checkpoint_name, failure_details)
        
        # Trigger automated remediation if configured
        if self.alert_config.get('auto_remediation', False):
            self.trigger_remediation(checkpoint_name, failure_details)
    
    def send_alert(self, message, severity="warning"):
        """Send alert through configured channels"""
        
        # Email alert
        if 'email' in self.alert_config:
            self.send_email_alert(message, severity)
        
        # Slack alert
        if 'slack' in self.alert_config:
            self.send_slack_alert(message, severity)
        
        # PagerDuty for critical issues
        if severity == "critical" and 'pagerduty' in self.alert_config:
            self.send_pagerduty_alert(message)
    
    def generate_daily_report(self):
        """Generate daily data quality report"""
        
        # Calculate quality trends
        quality_trends = self.calculate_quality_trends()
        
        # Generate report
        report = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'overall_quality_score': quality_trends['overall_score'],
            'quality_trend': quality_trends['trend'],
            'top_issues': quality_trends['top_issues'],
            'recommendations': quality_trends['recommendations']
        }
        
        # Send report
        self.send_daily_report(report)
```

### 20. What are the best practices for implementing data quality frameworks?
**Answer:**
Best practices for implementing robust data quality frameworks:

```python
# 1. Layered Quality Architecture
class DataQualityFramework:
    def __init__(self):
        self.layers = {
            'ingestion': IngestionQualityLayer(),
            'processing': ProcessingQualityLayer(),
            'storage': StorageQualityLayer(),
            'consumption': ConsumptionQualityLayer()
        }
    
    def validate_at_all_layers(self, data, metadata):
        """Validate data quality at all layers"""
        
        results = {}
        
        for layer_name, layer in self.layers.items():
            try:
                layer_result = layer.validate(data, metadata)
                results[layer_name] = layer_result
                
                # Stop if critical failure
                if not layer_result.success and layer_result.is_critical:
                    break
                    
            except Exception as e:
                results[layer_name] = {'error': str(e), 'success': False}
        
        return results

# 2. Quality Rules Management
class QualityRulesManager:
    def __init__(self):
        self.rules = {
            'global': [],      # Apply to all datasets
            'domain': {},      # Apply to specific domains
            'dataset': {}      # Apply to specific datasets
        }
    
    def add_global_rule(self, rule):
        """Add rule that applies to all datasets"""
        self.rules['global'].append(rule)
    
    def add_domain_rule(self, domain, rule):
        """Add rule for specific domain (e.g., finance, marketing)"""
        if domain not in self.rules['domain']:
            self.rules['domain'][domain] = []
        self.rules['domain'][domain].append(rule)
    
    def get_applicable_rules(self, dataset_metadata):
        """Get all rules applicable to a dataset"""
        
        applicable_rules = []
        
        # Global rules
        applicable_rules.extend(self.rules['global'])
        
        # Domain rules
        domain = dataset_metadata.get('domain')
        if domain and domain in self.rules['domain']:
            applicable_rules.extend(self.rules['domain'][domain])
        
        # Dataset-specific rules
        dataset_name = dataset_metadata.get('name')
        if dataset_name and dataset_name in self.rules['dataset']:
            applicable_rules.extend(self.rules['dataset'][dataset_name])
        
        return applicable_rules

# 3. Quality Metrics and SLAs
class QualityMetricsManager:
    def __init__(self):
        self.slas = {
            'completeness': {'min': 95.0, 'target': 99.0},
            'accuracy': {'min': 98.0, 'target': 99.5},
            'timeliness': {'max_delay_hours': 2, 'target_delay_hours': 0.5},
            'consistency': {'min': 95.0, 'target': 99.0}
        }
    
    def evaluate_sla_compliance(self, quality_metrics):
        """Evaluate SLA compliance"""
        
        compliance_results = {}
        
        for metric_name, sla in self.slas.items():
            if metric_name in quality_metrics:
                actual_value = quality_metrics[metric_name]
                
                if 'min' in sla:
                    compliance_results[metric_name] = {
                        'compliant': actual_value >= sla['min'],
                        'actual': actual_value,
                        'threshold': sla['min'],
                        'target': sla.get('target'),
                        'gap': max(0, sla['min'] - actual_value)
                    }
                elif 'max' in sla:
                    compliance_results[metric_name] = {
                        'compliant': actual_value <= sla['max'],
                        'actual': actual_value,
                        'threshold': sla['max'],
                        'target': sla.get('target'),
                        'gap': max(0, actual_value - sla['max'])
                    }
        
        return compliance_results

# 4. Quality Governance
class DataQualityGovernance:
    def __init__(self):
        self.stakeholders = {
            'data_owners': [],
            'data_stewards': [],
            'data_consumers': [],
            'quality_team': []
        }
        self.approval_workflows = {}
    
    def define_approval_workflow(self, rule_type, workflow):
        """Define approval workflow for quality rules"""
        self.approval_workflows[rule_type] = workflow
    
    def request_rule_approval(self, rule, requester):
        """Request approval for new quality rule"""
        
        rule_type = rule.get('type', 'standard')
        workflow = self.approval_workflows.get(rule_type, 'default')
        
        approval_request = {
            'rule': rule,
            'requester': requester,
            'workflow': workflow,
            'status': 'pending',
            'created_at': datetime.now(),
            'approvers': self.get_required_approvers(rule_type)
        }
        


### 21. How do you handle data quality in data lakes?
**Answer:**
Data lakes present unique challenges for data quality due to their schema-on-read nature and diverse data formats:

```python
import great_expectations as gx
import boto3
import pandas as pd
from datetime import datetime

class DataLakeQualityManager:
    def __init__(self, s3_bucket, ge_context):
        self.s3_bucket = s3_bucket
        self.s3_client = boto3.client('s3')
        self.context = ge_context
        self.quality_zones = {
            'raw': 'raw-data/',
            'bronze': 'bronze-data/',
            'silver': 'silver-data/',
            'gold': 'gold-data/'
        }
    
    def validate_raw_data_ingestion(self, file_path, data_source):
        """Validate data as it enters the raw zone"""
        
        validation_results = {
            'file_path': file_path,
            'data_source': data_source,
            'ingestion_timestamp': datetime.now(),
            'validations': {}
        }
        
        # 1. File-level validations
        file_validation = self.validate_file_properties(file_path)
        validation_results['validations']['file_properties'] = file_validation
        
        # 2. Schema detection and validation
        schema_validation = self.detect_and_validate_schema(file_path)
        validation_results['validations']['schema'] = schema_validation
        
        # 3. Basic data quality checks
        if schema_validation['is_readable']:
            data_validation = self.validate_raw_data_content(file_path)
            validation_results['validations']['content'] = data_validation
        
        # 4. Metadata validation
        metadata_validation = self.validate_metadata(file_path, data_source)
        validation_results['validations']['metadata'] = metadata_validation
        
        # Determine overall success
        validation_results['overall_success'] = all(
            v.get('success', False) for v in validation_results['validations'].values()
        )
        
        # Route data based on validation results
        if validation_results['overall_success']:
            self.move_to_bronze_zone(file_path)
        else:
            self.quarantine_data(file_path, validation_results)
        
        return validation_results
    
    def validate_file_properties(self, file_path):
        """Validate file-level properties"""
        
        try:
            # Get file metadata from S3
            response = self.s3_client.head_object(
                Bucket=self.s3_bucket,
                Key=file_path
            )
            
            file_size = response['ContentLength']
            last_modified = response['LastModified']
            
            validation = {
                'success': True,
                'file_size_bytes': file_size,
                'last_modified': last_modified,
                'checks': {}
            }
            
            # File size validation
            if file_size == 0:
                validation['success'] = False
                validation['checks']['empty_file'] = 'File is empty'
            elif file_size > 10 * 1024 * 1024 * 1024:  # 10GB limit
                validation['success'] = False
                validation['checks']['file_too_large'] = f'File size {file_size} exceeds limit'
            
            # File age validation
            age_hours = (datetime.now(last_modified.tzinfo) - last_modified).total_seconds() / 3600
            if age_hours > 24:  # Files older than 24 hours
                validation['checks']['stale_file'] = f'File is {age_hours:.1f} hours old'
            
            return validation
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def detect_and_validate_schema(self, file_path):
        """Detect and validate data schema"""
        
        try:
            # Read sample of data to detect schema
            if file_path.endswith('.csv'):
                df_sample = pd.read_csv(f's3://{self.s3_bucket}/{file_path}', nrows=1000)
            elif file_path.endswith('.parquet'):
                df_sample = pd.read_parquet(f's3://{self.s3_bucket}/{file_path}')
            elif file_path.endswith('.json'):
                df_sample = pd.read_json(f's3://{self.s3_bucket}/{file_path}', lines=True, nrows=1000)
            else:
                return {
                    'success': False,
                    'error': 'Unsupported file format'
                }
            
            detected_schema = {
                'columns': list(df_sample.columns),
                'dtypes': df_sample.dtypes.to_dict(),
                'row_count_sample': len(df_sample)
            }
            
            # Validate against expected schema if available
            expected_schema = self.get_expected_schema(file_path)
            if expected_schema:
                schema_compliance = self.validate_schema_compliance(detected_schema, expected_schema)
            else:
                schema_compliance = {'compliant': True, 'message': 'No expected schema defined'}
            
            return {
                'success': True,
                'is_readable': True,
                'detected_schema': detected_schema,
                'schema_compliance': schema_compliance
            }
            
        except Exception as e:
            return {
                'success': False,
                'is_readable': False,
                'error': str(e)
            }
    
    def validate_bronze_to_silver_promotion(self, dataset_path):
        """Validate data for promotion from bronze to silver zone"""
        
        # Create Great Expectations validator
        batch_request = self.create_batch_request(dataset_path, 'bronze')
        validator = self.context.get_validator(
            batch_request=batch_request,
            expectation_suite_name='bronze_to_silver_suite'
        )
        
        # Apply bronze-to-silver quality rules
        self.apply_bronze_to_silver_expectations(validator)
        
        # Run validation
        validation_result = validator.validate()
        
        if validation_result.success:
            # Promote to silver zone
            self.promote_to_silver_zone(dataset_path)
            
            # Apply silver zone transformations
            self.apply_silver_zone_transformations(dataset_path)
        
        return validation_result
    
    def apply_bronze_to_silver_expectations(self, validator):
        """Apply quality expectations for bronze to silver promotion"""
        
        # Data completeness requirements
        validator.expect_table_row_count_to_be_between(min_value=1)
        
        # Key column requirements
        validator.expect_column_to_exist('id')
        validator.expect_column_values_to_not_be_null('id')
        validator.expect_column_values_to_be_unique('id')
        
        # Timestamp requirements
        validator.expect_column_to_exist('created_timestamp')
        validator.expect_column_values_to_be_dateutil_parseable('created_timestamp')
        
        # Data freshness requirements
        validator.expect_column_values_to_be_between(
            'created_timestamp',
            min_value=datetime.now() - pd.Timedelta(days=7),  # Data not older than 7 days
            max_value=datetime.now() + pd.Timedelta(hours=1)   # Data not from future
        )
        
        # Business rule validations
        validator.expect_column_values_to_be_in_set(
            'status',
            ['active', 'inactive', 'pending', 'archived']
        )
    
    def validate_silver_to_gold_promotion(self, dataset_path):
        """Validate data for promotion from silver to gold zone"""
        
        batch_request = self.create_batch_request(dataset_path, 'silver')
        validator = self.context.get_validator(
            batch_request=batch_request,
            expectation_suite_name='silver_to_gold_suite'
        )
        
        # Apply gold zone quality requirements (highest standards)
        self.apply_silver_to_gold_expectations(validator)
        
        validation_result = validator.validate()
        
        if validation_result.success:
            self.promote_to_gold_zone(dataset_path)
        
        return validation_result
    
    def apply_silver_to_gold_expectations(self, validator):
        """Apply highest quality expectations for gold zone"""
        
        # Perfect data completeness
        validator.expect_column_values_to_not_be_null('customer_id')
        validator.expect_column_values_to_not_be_null('transaction_amount')
        validator.expect_column_values_to_not_be_null('transaction_date')
        
        # Data accuracy requirements
        validator.expect_column_values_to_be_between('transaction_amount', 0.01, 1000000)
        validator.expect_column_values_to_match_regex(
            'email',
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        
        # Statistical quality requirements
        validator.expect_column_mean_to_be_between('transaction_amount', 10, 10000)
        validator.expect_column_stdev_to_be_between('transaction_amount', 5, 5000)
        
        # Referential integrity
        validator.expect_column_values_to_be_in_set(
            'currency_code',
            ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD']
        )
```

### 22. How do you implement data quality testing in Apache Spark?
**Answer:**
Implementing data quality testing in Spark requires leveraging Spark's distributed computing capabilities:

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when, isnan, isnull, regexp_extract
from pyspark.sql.types import *
import great_expectations as gx
from great_expectations.dataset import SparkDFDataset

class SparkDataQualityTester:
    def __init__(self, spark_session):
        self.spark = spark_session
        self.quality_results = {}
    
    def validate_dataframe_quality(self, df, dataset_name):
        """Comprehensive data quality validation for Spark DataFrame"""
        
        print(f"Starting quality validation for {dataset_name}")
        
        validation_results = {
            'dataset_name': dataset_name,
            'total_rows': df.count(),
            'total_columns': len(df.columns),
            'validations': {}
        }
        
        # 1. Schema validation
        schema_validation = self.validate_schema(df, dataset_name)
        validation_results['validations']['schema'] = schema_validation
        
        # 2. Completeness validation
        completeness_validation = self.validate_completeness(df)
        validation_results['validations']['completeness'] = completeness_validation
        
        # 3. Uniqueness validation
        uniqueness_validation = self.validate_uniqueness(df)
        validation_results['validations']['uniqueness'] = uniqueness_validation
        
        # 4. Data type validation
        datatype_validation = self.validate_data_types(df)
        validation_results['validations']['data_types'] = datatype_validation
        
        # 5. Business rule validation
        business_rule_validation = self.validate_business_rules(df)
        validation_results['validations']['business_rules'] = business_rule_validation
        
        # 6. Statistical validation
        statistical_validation = self.validate_statistical_properties(df)
        validation_results['validations']['statistical'] = statistical_validation
        
        # Calculate overall quality score
        validation_results['overall_quality_score'] = self.calculate_quality_score(validation_results)
        
        return validation_results
    
    def validate_completeness(self, df):
        """Validate data completeness"""
        
        total_rows = df.count()
        completeness_results = {}
        
        for column in df.columns:
            # Count null and empty values
            null_count = df.filter(
                col(column).isNull() | 
                isnan(col(column)) | 
                (col(column) == '')
            ).count()
            
            completeness_percentage = ((total_rows - null_count) / total_rows) * 100
            
            completeness_results[column] = {
                'null_count': null_count,
                'completeness_percentage': completeness_percentage,
                'meets_threshold': completeness_percentage >= 95.0  # 95% threshold
            }
        
        return completeness_results
    
    def validate_uniqueness(self, df):
        """Validate data uniqueness for key columns"""
        
        uniqueness_results = {}
        key_columns = ['id', 'customer_id', 'order_id', 'email']  # Define key columns
        
        for column in key_columns:
            if column in df.columns:
                total_count = df.count()
                distinct_count = df.select(column).distinct().count()
                
                uniqueness_percentage = (distinct_count / total_count) * 100
                duplicate_count = total_count - distinct_count
                
                uniqueness_results[column] = {
                    'total_count': total_count,
                    'distinct_count': distinct_count,
                    'duplicate_count': duplicate_count,
                    'uniqueness_percentage': uniqueness_percentage,
                    'is_unique': duplicate_count == 0
                }
        
        return uniqueness_results
    
    def validate_business_rules(self, df):
        """Validate business-specific rules"""
        
        business_rule_results = {}
        
        # Rule 1: Age must be between 0 and 120
        if 'age' in df.columns:
            invalid_age_count = df.filter(
                (col('age') < 0) | (col('age') > 120)
            ).count()
            
            business_rule_results['valid_age_range'] = {
                'invalid_count': invalid_age_count,
                'rule_passed': invalid_age_count == 0
            }
        
        # Rule 2: Email format validation
        if 'email' in df.columns:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            invalid_email_count = df.filter(
                ~col('email').rlike(email_pattern)
            ).count()
            
            business_rule_results['valid_email_format'] = {
                'invalid_count': invalid_email_count,
                'rule_passed': invalid_email_count == 0
            }
        
        # Rule 3: Transaction amount must be positive
        if 'transaction_amount' in df.columns:
            negative_amount_count = df.filter(
                col('transaction_amount') <= 0
            ).count()
            
            business_rule_results['positive_transaction_amount'] = {
                'invalid_count': negative_amount_count,
                'rule_passed': negative_amount_count == 0
            }
        
        # Rule 4: Status must be from valid set
        if 'status' in df.columns:
            valid_statuses = ['active', 'inactive', 'pending', 'cancelled']
            invalid_status_count = df.filter(
                ~col('status').isin(valid_statuses)
            ).count()
            
            business_rule_results['valid_status_values'] = {
                'invalid_count': invalid_status_count,
                'rule_passed': invalid_status_count == 0
            }
        
        return business_rule_results
    
    def validate_statistical_properties(self, df):
        """Validate statistical properties of numeric columns"""
        
        statistical_results = {}
        numeric_columns = [field.name for field in df.schema.fields 
                          if isinstance(field.dataType, (IntegerType, LongType, FloatType, DoubleType))]
        
        for column in numeric_columns:
            # Calculate statistics
            stats = df.select(
                col(column)
            ).describe().collect()
            
            # Convert to dictionary
            stats_dict = {}
            for row in stats:
                stats_dict[row['summary']] = float(row[column]) if row[column] else None
            
            # Validate against expected ranges
            statistical_results[column] = {
                'statistics': stats_dict,
                'validations': {}
            }
            
            # Example validations
            if column == 'age':
                mean_age = stats_dict.get('mean', 0)
                statistical_results[column]['validations']['reasonable_mean'] = {
                    'expected_range': [18, 65],
                    'actual_value': mean_age,
                    'passed': 18 <= mean_age <= 65
                }
            
            if column == 'transaction_amount':
                mean_amount = stats_dict.get('mean', 0)
                statistical_results[column]['validations']['reasonable_mean'] = {
                    'expected_range': [10, 10000],
                    'actual_value': mean_amount,
                    'passed': 10 <= mean_amount <= 10000
                }
        
        return statistical_results
    
    def integrate_with_great_expectations(self, df, suite_name):
        """Integrate Spark DataFrame with Great Expectations"""
        
        # Convert Spark DataFrame to Great Expectations dataset
        ge_df = SparkDFDataset(df)
        
        # Add expectations
        ge_df.expect_table_row_count_to_be_between(min_value=1000)
        ge_df.expect_column_to_exist('customer_id')
        ge_df.expect_column_values_to_not_be_null('customer_id')
        ge_df.expect_column_values_to_be_unique('customer_id')
        
        # Validate
        validation_result = ge_df.validate()
        
        return validation_result
    
    def create_quality_report_table(self, validation_results):
        """Create a Spark DataFrame with quality report"""
        
        report_data = []
        
        for dataset_name, results in validation_results.items():
            for validation_type, validation_data in results.get('validations', {}).items():
                if isinstance(validation_data, dict):
                    for check_name, check_result in validation_data.items():
                        if isinstance(check_result, dict):
                            report_data.append((
                                dataset_name,
                                validation_type,
                                check_name,
                                check_result.get('rule_passed', check_result.get('meets_threshold', None)),
                                str(check_result)
                            ))
        
        # Create DataFrame
        schema = StructType([
            StructField('dataset_name', StringType(), True),
            StructField('validation_type', StringType(), True),
            StructField('check_name', StringType(), True),
            StructField('passed', BooleanType(), True),
            StructField('details', StringType(), True)
        ])
        
        report_df = self.spark.createDataFrame(report_data, schema)
        
        return report_df

# Usage example
def spark_quality_testing_example():
    """Example of using Spark for data quality testing"""
    
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("DataQualityTesting") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()
    
    # Initialize quality tester
    quality_tester = SparkDataQualityTester(spark)
    
    # Load data
    df = spark.read.parquet("s3://data-lake/customer-data/")
    
    # Run quality validation
    validation_results = quality_tester.validate_dataframe_quality(df, "customer_data")
    
    # Create quality report
    quality_report_df = quality_tester.create_quality_report_table({"customer_data": validation_results})
    
    # Save quality report
    quality_report_df.write \
        .mode("overwrite") \
        .parquet("s3://data-lake/quality-reports/customer-data-quality/")
    
    # Show summary
    print(f"Overall Quality Score: {validation_results['overall_quality_score']:.2f}%")
    
    return validation_results
```

### 23. What are data quality dimensions and how do you measure them?
**Answer:**
Data quality dimensions are the key characteristics used to assess data quality. Here's how to measure each dimension:

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re

class DataQualityDimensionsMeasurement:
    def __init__(self, df):
        self.df = df
        self.measurements = {}
    
    def measure_accuracy(self, reference_data=None, validation_rules=None):
        """Measure data accuracy - correctness of data values"""
        
        accuracy_results = {
            'dimension': 'accuracy',
            'score': 0,
            'measurements': {}
        }
        
        if validation_rules:
            # Rule-based accuracy measurement
            total_rules = len(validation_rules)
            passed_rules = 0
            
            for rule_name, rule_func in validation_rules.items():
                try:
                    rule_result = rule_func(self.df)
                    accuracy_results['measurements'][rule_name] = {
                        'passed': rule_result,
                        'accuracy_contribution': 1.0 if rule_result else 0.0
                    }
                    if rule_result:
                        passed_rules += 1
                except Exception as e:
                    accuracy_results['measurements'][rule_name] = {
                        'error': str(e),
                        'accuracy_contribution': 0.0
                    }
            
            accuracy_results['score'] = (passed_rules / total_rules) * 100
        
        if reference_data is not None:
            # Reference-based accuracy measurement
            matching_records = 0
            total_records = len(self.df)
            
            # Compare with reference data (simplified example)
            for index, row in self.df.iterrows():
                if index < len(reference_data):
                    reference_row = reference_data.iloc[index]
                    if row.equals(reference_row):
                        matching_records += 1
            
            reference_accuracy = (matching_records / total_records) * 100
            accuracy_results['measurements']['reference_match'] = {
                'matching_records': matching_records,
                'total_records': total_records,
                'accuracy_percentage': reference_accuracy
            }
        
        self.measurements['accuracy'] = accuracy_results
        return accuracy_results
    
    def measure_completeness(self):
        """Measure data completeness - presence of required data"""
        
        completeness_results = {
            'dimension': 'completeness',
            'score': 0,
            'measurements': {}
        }
        
        total_cells = len(self.df) * len(self.df.columns)
        non_null_cells = 0
        
        for column in self.df.columns:
            null_count = self.df[column].isnull().sum()
            empty_string_count = (self.df[column] == '').sum() if self.df[column].dtype == 'object' else 0
            
            missing_count = null_count + empty_string_count
            present_count = len(self.df) - missing_count
            completeness_percentage = (present_count / len(self.df)) * 100
            
            completeness_results['measurements'][column] = {
                'total_records': len(self.df),
                'missing_records': missing_count,
                'present_records': present_count,
                'completeness_percentage': completeness_percentage
            }
            
            non_null_cells += present_count
        
        # Overall completeness score
        completeness_results['score'] = (non_null_cells / total_cells) * 100
        
        self.measurements['completeness'] = completeness_results
        return completeness_results
    
    def measure_consistency(self, consistency_rules=None):
        """Measure data consistency - uniformity across datasets/systems"""
        
        consistency_results = {
            'dimension': 'consistency',
            'score': 0,
            'measurements': {}
        }
        
        # Format consistency
        format_consistency = self._measure_format_consistency()
        consistency_results['measurements']['format_consistency'] = format_consistency
        
        # Value consistency
        value_consistency = self._measure_value_consistency()
        consistency_results['measurements']['value_consistency'] = value_consistency
        
        # Cross-column consistency
        cross_column_consistency = self._measure_cross_column_consistency()
        consistency_results['measurements']['cross_column_consistency'] = cross_column_consistency
        
        # Calculate overall consistency score
        consistency_scores = [
            format_consistency.get('score', 0),
            value_consistency.get('score', 0),
            cross_column_consistency.get('score', 0)
        ]
        consistency_results['score'] = np.mean([s for s in consistency_scores if s > 0])
        
        self.measurements['consistency'] = consistency_results
        return consistency_results
    
    def _measure_format_consistency(self):
        """Measure format consistency within columns"""
        
        format_results = {'score': 0, 'column_scores': {}}
        
        text_columns = self.df.select_dtypes(include=['object']).columns
        total_score = 0
        scored_columns = 0
        
        for column in text_columns:
            if 'email' in column.lower():
                # Email format consistency
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                valid_format_count = self.df[column].str.match(email_pattern, na=False).sum()
                total_count = self.df[column].notna().sum()
                
                if total_count > 0:
                    format_score = (valid_format_count / total_count) * 100
                    format_results['column_scores'][column] = format_score
                    total_score += format_score
                    scored_columns += 1
            
            elif 'phone' in column.lower():
                # Phone format consistency
                phone_pattern = r'^\+?1?[0-9]{10,15}$'
                valid_format_count = self.df[column].str.match(phone_pattern, na=False).sum()
                total_count = self.df[column].notna().sum()
                
                if total_count > 0:
                    format_score = (valid_format_count / total_count) * 100
                    format_results['column_scores'][column] = format_score
                    total_score += format_score
                    scored_columns += 1
        
        if scored_columns > 0:
            format_results['score'] = total_score / scored_columns
        
        return format_results
    
    def measure_validity(self, business_rules):
        """Measure data validity - conformance to business rules"""
        
        validity_results = {
            'dimension': 'validity',
            'score': 0,
            'measurements': {}
        }
        
        total_rules = len(business_rules)
        passed_rules = 0
        
        for rule_name, rule_config in business_rules.items():
            column = rule_config['column']
            rule_type = rule_config['type']
            rule_params = rule_config.get('params', {})
            
            if column not in self.df.columns:
                validity_results['measurements'][rule_name] = {
                    'error': f'Column {column} not found',
                    'validity_score': 0
                }
                continue
            
            try:
                if rule_type == 'range':
                    min_val = rule_params.get('min')
                    max_val = rule_params.get('max')
                    valid_mask = (self.df[column] >= min_val) & (self.df[column] <= max_val)
                    
                elif rule_type == 'set_membership':
                    valid_values = rule_params.get('valid_values', [])
                    valid_mask = self.df[column].isin(valid_values)
                    
                elif rule_type == 'regex':
                    pattern = rule_params.get('pattern')
                    valid_mask = self.df[column].str.match(pattern, na=False)
                    
                else:
                    validity_results['measurements'][rule_name] = {
                        'error': f'Unknown rule type: {rule_type}',
                        'validity_score': 0
                    }
                    continue
                
                valid_count = valid_mask.sum()
                total_count = self.df[column].notna().sum()
                validity_score = (valid_count / total_count) * 100 if total_count > 0 else 0
                
                validity_results['measurements'][rule_name] = {
                    'valid_count': valid_count,
                    'total_count': total_count,
                    'validity_score': validity_score,
                    'rule_passed': validity_score >= 95  # 95% threshold
                }
                
                if validity_score >= 95:
                    passed_rules += 1
                    
            except Exception as e:
                validity_results['measurements'][rule_name] = {
                    'error': str(e),
                    'validity_score': 0
                }
        
        validity_results['score'] = (passed_rules / total_rules) * 100 if total_rules > 0 else 0
        
        self.measurements['validity'] = validity_results
        return validity_results
    
    def measure_timeliness(self, timestamp_column, max_age_hours=24):
        """Measure data timeliness - how current the data is"""
        
        timeliness_results = {
            'dimension': 'timeliness',
            'score': 0,
            'measurements': {}
        }
        
        if timestamp_column not in self.df.columns:
            timeliness_results['measurements']['error'] = f'Timestamp column {timestamp_column} not found'
            return timeliness_results
        
        try:
            # Convert to datetime if not already
            timestamps = pd.to_datetime(self.df[timestamp_column])
            current_time = datetime.now()
            
            # Calculate age in hours
            age_hours = (current_time - timestamps).dt.total_seconds() / 3600
            
            # Count fresh records
            fresh_records = (age_hours <= max_age_hours).sum()
            total_records = len(self.df)
            
            timeliness_score = (fresh_records / total_records) * 100
            
            timeliness_results['measurements'] = {
                'total_records': total_records,
                'fresh_records': fresh_records,
                'stale_records': total_records - fresh_records,
                'max_age_hours': max_age_hours,
                'avg_age_hours': age_hours.mean(),
                'min_age_hours': age_hours.min(),
                'max_age_hours_actual': age_hours.max()
            }
            
            timeliness_results['score'] = timeliness_score
            
        except Exception as e:
            timeliness_results['measurements']['error'] = str(e)
        
        self.measurements['timeliness'] = timeliness_results
        return timeliness_results
    
    def measure_uniqueness(self, key_columns):
        """Measure data uniqueness - absence of duplicates"""
        
        uniqueness_results = {
            'dimension': 'uniqueness',
            'score': 0,
            'measurements': {}
        }
        
        total_score = 0
        scored_columns = 0
        
        for column in key_columns:
            if column in self.df.columns:
                total_records = len(self.df)
                unique_records = self.df[column].nunique()
                duplicate_records = total_records - unique_records
                
                uniqueness_score = (unique_records / total_records) * 100
                
                uniqueness_results['measurements'][column] = {
                    'total_records': total_records,
                    'unique_records': unique_records,
                    'duplicate_records': duplicate_records,
                    'uniqueness_score': uniqueness_score,
                    'is_unique': duplicate_records == 0
                }
                
                total_score += uniqueness_score
                scored_columns += 1
        
        if scored_columns > 0:
            uniqueness_results['score'] = total_score / scored_columns
        
        self.measurements['uniqueness'] = uniqueness_results
        return uniqueness_results
    
    def calculate_overall_quality_score(self, weights=None):
        """Calculate weighted overall quality score across all dimensions"""
        
        if weights is None:
            weights = {
                'accuracy': 0.25,
                'completeness': 0.20,
                'consistency': 0.15,
                'validity': 0.20,
                'timeliness': 0.10,
                'uniqueness': 0.10
            }
        
        overall_score = 0
        total_weight = 0
        
        for dimension, weight in weights.items():
            if dimension in self.measurements:
                dimension_score = self.measurements[dimension].get('score', 0)
                overall_score += dimension_score * weight
                total_weight += weight
        
        final_score = overall_score / total_weight if total_weight > 0 else 0
        
        return {
            'overall_quality_score': final_score,
            'dimension_scores': {dim: self.measurements[dim].get('score', 0) 
                               for dim in self.measurements},
            'weights_used': weights
        }

# Usage example
def measure_quality_dimensions_example():
    """Example of measuring all data quality dimensions"""
    
    # Sample data
    df = pd.DataFrame({
        'customer_id': [1, 2, 3, 4, 5, 1],  # Duplicate
        'email': ['john@email.com', 'jane@email.com', 'invalid-email', 'bob@email.com', None, 'john@email.com'],
        'age': [25, 30, 150, 35, 28, 25],  # Outlier
        'order_amount': [100.50, 250.00, -50.00, 300.00, 150.00, 100.50],  # Negative value
        'created_date': ['2023-12-01', '2023-12-02', '2023-12-03', '2023-12-04', '2023-12-05', '2023-12-01']
    })
    
    # Initialize measurement class
    quality_measurer = DataQualityDimensionsMeasurement(df)
    
    # Measure completeness
    completeness = quality_measurer.measure_completeness()
    print(f"Completeness Score: {completeness['score']:.2f}%")
    
    # Measure uniqueness
    uniqueness = quality_measurer.measure_uniqueness(['customer_id', 'email'])
    print(f"Uniqueness Score: {uniqueness['score']:.2f}%")
    
    # Measure validity
    business_rules = {
        'valid_age': {
            'column': 'age',
            'type': 'range',
            'params': {'min': 0, 'max': 120}
        },
        'positive_amount': {
            'column': 'order_amount',
            'type': 'range',
            'params': {'min': 0.01, 'max': 10000}
        },
        'valid_email': {
            'column': 'email',
            'type': 'regex',
            'params': {'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'}
        }
    }
    
    validity = quality_measurer.measure_validity(business_rules)
    print(f"Validity Score: {validity['score']:.2f}%")
    
    # Calculate overall quality score
    overall_quality = quality_measurer.calculate_overall_quality_score()
    print(f"Overall Quality Score: {overall_quality['overall_quality_score']:.2f}%")
    


### 24. How do you implement data quality gates in data pipelines?
**Answer:**
Data quality gates are checkpoints that prevent poor-quality data from progressing through the pipeline:

```python
class DataQualityGate:
    def __init__(self, context, gate_config):
        self.context = context
        self.gate_config = gate_config
        self.gate_results = {}
    
    def execute_gate(self, data, gate_name):
        """Execute data quality gate"""
        
        gate_definition = self.gate_config[gate_name]
        
        # Run quality checks
        checkpoint_result = self.context.run_checkpoint(
            checkpoint_name=gate_definition['checkpoint_name']
        )
        
        # Evaluate gate criteria
        gate_passed = self.evaluate_gate_criteria(
            checkpoint_result, 
            gate_definition['criteria']
        )
        
        # Record gate result
        self.gate_results[gate_name] = {
            'passed': gate_passed,
            'timestamp': datetime.now(),
            'checkpoint_result': checkpoint_result,
            'data_volume': len(data) if hasattr(data, '__len__') else 'unknown'
        }
        
        # Handle gate failure
        if not gate_passed:
            self.handle_gate_failure(gate_name, checkpoint_result)
        
        return gate_passed
    
    def evaluate_gate_criteria(self, checkpoint_result, criteria):
        """Evaluate if gate criteria are met"""
        
        # Extract metrics from checkpoint result
        success_rate = checkpoint_result.statistics['success_percent']
        
        # Check minimum success rate
        if success_rate < criteria.get('min_success_rate', 95.0):
            return False
        
        # Check for critical failures
        critical_failures = 0
        for validation_result in checkpoint_result.run_results.values():
            for expectation_result in validation_result.results:
                if not expectation_result.success:
                    if expectation_result.expectation_config.meta.get('critical', False):
                        critical_failures += 1
        
        if critical_failures > criteria.get('max_critical_failures', 0):
            return False
        
        return True
    
    def handle_gate_failure(self, gate_name, checkpoint_result):
        """Handle gate failure"""
        
        failure_action = self.gate_config[gate_name].get('failure_action', 'stop')
        
        if failure_action == 'stop':
            raise DataQualityGateException(f"Data quality gate '{gate_name}' failed")
        elif failure_action == 'quarantine':
            self.quarantine_data(gate_name, checkpoint_result)
        elif failure_action == 'alert':
            self.send_alert(gate_name, checkpoint_result)

# Usage in pipeline
def pipeline_with_quality_gates():
    """Data pipeline with quality gates"""
    
    gate_config = {
        'ingestion_gate': {
            'checkpoint_name': 'raw_data_checkpoint',
            'criteria': {
                'min_success_rate': 90.0,
                'max_critical_failures': 0
            },
            'failure_action': 'stop'
        },
        'transformation_gate': {
            'checkpoint_name': 'transformed_data_checkpoint',
            'criteria': {
                'min_success_rate': 95.0,
                'max_critical_failures': 0
            },
            'failure_action': 'quarantine'
        },
        'publication_gate': {
            'checkpoint_name': 'final_data_checkpoint',
            'criteria': {
                'min_success_rate': 99.0,
                'max_critical_failures': 0
            },
            'failure_action': 'stop'
        }
    }
    
    quality_gate = DataQualityGate(context, gate_config)
    
    # Pipeline stages with gates
    try:
        # Stage 1: Data Ingestion
        raw_data = ingest_data()
        
        # Gate 1: Validate raw data
        if not quality_gate.execute_gate(raw_data, 'ingestion_gate'):
            return {'status': 'failed', 'stage': 'ingestion'}
        
        # Stage 2: Data Transformation
        transformed_data = transform_data(raw_data)
        
        # Gate 2: Validate transformed data
        if not quality_gate.execute_gate(transformed_data, 'transformation_gate'):
            return {'status': 'failed', 'stage': 'transformation'}
        
        # Stage 3: Data Publication
        final_data = prepare_for_publication(transformed_data)
        
        # Gate 3: Final validation
        if not quality_gate.execute_gate(final_data, 'publication_gate'):
            return {'status': 'failed', 'stage': 'publication'}
        
        # Publish data
        publish_data(final_data)
        
        return {'status': 'success', 'gates_passed': list(quality_gate.gate_results.keys())}
        
    except DataQualityGateException as e:
        return {'status': 'failed', 'error': str(e)}
```

### 25. What are the challenges of implementing data quality at scale?
**Answer:**
Scaling data quality presents several technical and organizational challenges:

```python
# 1. Performance Challenges
class ScalableDataQualityProcessor:
    def __init__(self, spark_session, ge_context):
        self.spark = spark_session
        self.context = ge_context
        self.performance_metrics = {}
    
    def validate_large_dataset(self, df, suite_name, sampling_strategy='adaptive'):
        """Validate large datasets efficiently"""
        
        dataset_size = df.count()
        
        # Adaptive sampling based on dataset size
        if sampling_strategy == 'adaptive':
            if dataset_size > 100_000_000:  # 100M+ rows
                sample_fraction = 0.001  # 0.1% sample
            elif dataset_size > 10_000_000:  # 10M+ rows
                sample_fraction = 0.01   # 1% sample
            elif dataset_size > 1_000_000:   # 1M+ rows
                sample_fraction = 0.1    # 10% sample
            else:
                sample_fraction = 1.0    # Full validation
        
        # Create stratified sample if needed
        if sample_fraction < 1.0:
            sampled_df = df.sample(fraction=sample_fraction, seed=42)
            print(f"Validating {sample_fraction*100}% sample ({sampled_df.count():,} rows)")
        else:
            sampled_df = df
        
        # Convert to Great Expectations dataset
        from great_expectations.dataset import SparkDFDataset
        ge_df = SparkDFDataset(sampled_df)
        
        # Apply expectations
        validation_result = self.apply_scalable_expectations(ge_df, suite_name)
        
        return validation_result
    
    def apply_scalable_expectations(self, ge_df, suite_name):
        """Apply expectations optimized for large datasets"""
        
        # Use approximate algorithms for statistical expectations
        ge_df.expect_column_values_to_not_be_null('customer_id')
        ge_df.expect_column_values_to_be_unique('customer_id')
        
        # Use sampling for expensive operations
        ge_df.expect_column_mean_to_be_between(
            'order_amount', 
            min_value=10, 
            max_value=1000,
            mostly=0.95  # Allow some tolerance
        )
        
        # Validate and return results
        return ge_df.validate()

# 2. Resource Management
class ResourceAwareQualityManager:
    def __init__(self, max_concurrent_validations=5):
        self.max_concurrent = max_concurrent_validations
        self.active_validations = 0
        self.validation_queue = []
    
    def queue_validation(self, validation_task):
        """Queue validation task with resource management"""
        
        if self.active_validations < self.max_concurrent:
            self.execute_validation(validation_task)
        else:
            self.validation_queue.append(validation_task)
    
    def execute_validation(self, validation_task):
        """Execute validation with resource monitoring"""
        
        self.active_validations += 1
        
        try:
            # Monitor resource usage
            start_memory = self.get_memory_usage()
            start_time = time.time()
            
            # Execute validation
            result = validation_task.execute()
            
            # Record metrics
            end_time = time.time()
            end_memory = self.get_memory_usage()
            
            self.record_performance_metrics({
                'task_id': validation_task.id,
                'execution_time': end_time - start_time,
                'memory_used': end_memory - start_memory,
                'success': result.success
            })
            
        finally:
            self.active_validations -= 1
            
            # Process next queued validation
            if self.validation_queue:
                next_task = self.validation_queue.pop(0)
                self.execute_validation(next_task)

# 3. Distributed Validation
class DistributedQualityValidator:
    def __init__(self, cluster_config):
        self.cluster_config = cluster_config
        self.worker_nodes = cluster_config['worker_nodes']
    
    def distribute_validation_tasks(self, datasets, expectations):
        """Distribute validation across cluster nodes"""
        
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        # Partition datasets across workers
        dataset_partitions = self.partition_datasets(datasets)
        
        validation_results = []
        
        with ThreadPoolExecutor(max_workers=len(self.worker_nodes)) as executor:
            # Submit validation tasks to workers
            future_to_partition = {
                executor.submit(
                    self.validate_partition, 
                    partition, 
                    expectations,
                    worker_node
                ): partition 
                for partition, worker_node in zip(dataset_partitions, self.worker_nodes)
            }
            
            # Collect results
            for future in as_completed(future_to_partition):
                partition = future_to_partition[future]
                try:
                    result = future.result()
                    validation_results.append(result)
                except Exception as e:
                    print(f"Validation failed for partition {partition}: {e}")
        
        # Aggregate results
        return self.aggregate_distributed_results(validation_results)
    
    def aggregate_distributed_results(self, results):
        """Aggregate validation results from distributed execution"""
        
        aggregated = {
            'overall_success': all(r['success'] for r in results),
            'total_records_validated': sum(r['records_validated'] for r in results),
            'total_expectations_run': sum(r['expectations_run'] for r in results),
            'failed_expectations': sum(r['failed_expectations'] for r in results),
            'execution_time': max(r['execution_time'] for r in results),
            'worker_results': results
        }
        
        return aggregated

# 4. Organizational Challenges
class DataQualityGovernance:
    def __init__(self):
        self.quality_standards = {}
        self.stakeholder_agreements = {}
        self.escalation_procedures = {}
    
    def establish_quality_standards(self, domain, standards):
        """Establish domain-specific quality standards"""
        
        self.quality_standards[domain] = {
            'completeness_threshold': standards.get('completeness', 95.0),
            'accuracy_threshold': standards.get('accuracy', 98.0),
            'timeliness_threshold': standards.get('timeliness_hours', 24),
            'consistency_threshold': standards.get('consistency', 95.0),
            'uniqueness_threshold': standards.get('uniqueness', 99.0)
        }
    
    def create_stakeholder_agreement(self, dataset, stakeholders, sla):
        """Create data quality SLA with stakeholders"""
        
        self.stakeholder_agreements[dataset] = {
            'data_owners': stakeholders.get('owners', []),
            'data_consumers': stakeholders.get('consumers', []),
            'quality_team': stakeholders.get('quality_team', []),
            'sla': {
                'availability': sla.get('availability', 99.9),
                'quality_score': sla.get('quality_score', 95.0),
                'resolution_time': sla.get('resolution_time_hours', 4)
            }
        }
    
    def handle_quality_incident(self, incident):
        """Handle data quality incidents with proper escalation"""
        
        severity = self.assess_incident_severity(incident)
        
        if severity == 'critical':
            # Immediate escalation to senior stakeholders
            self.escalate_to_senior_management(incident)
            # Stop downstream processes
            self.halt_dependent_processes(incident['affected_datasets'])
        elif severity == 'high':
            # Escalate to data owners and quality team
            self.notify_data_owners(incident)
            # Quarantine affected data
            self.quarantine_data(incident['affected_datasets'])
        else:
            # Standard notification and tracking
            self.log_incident(incident)
            self.notify_quality_team(incident)
```

### 26. How do you ensure data quality in real-time streaming scenarios?
**Answer:**
Real-time data quality requires specialized approaches for low-latency validation:

```python
from kafka import KafkaConsumer, KafkaProducer
import json
from datetime import datetime
import asyncio

class StreamingDataQualityProcessor:
    def __init__(self, kafka_config, quality_rules):
        self.kafka_config = kafka_config
        self.quality_rules = quality_rules
        self.consumer = KafkaConsumer(
            kafka_config['input_topic'],
            bootstrap_servers=kafka_config['bootstrap_servers'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_config['bootstrap_servers'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        self.quality_metrics = {
            'total_messages': 0,
            'valid_messages': 0,
            'invalid_messages': 0,
            'processing_time_ms': []
        }
    
    async def process_stream(self):
        """Process streaming data with quality validation"""
        
        for message in self.consumer:
            start_time = datetime.now()
            
            try:
                # Extract record
                record = message.value
                
                # Validate record
                validation_result = await self.validate_record_async(record)
                
                # Route based on quality
                if validation_result['is_valid']:
                    await self.route_valid_record(record, message.partition)
                else:
                    await self.handle_invalid_record(record, validation_result)
                
                # Update metrics
                self.update_metrics(validation_result, start_time)
                
            except Exception as e:
                await self.handle_processing_error(message, str(e))
    
    async def validate_record_async(self, record):
        """Asynchronous record validation for low latency"""
        
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'validation_timestamp': datetime.now().isoformat()
        }
        
        # Fast validation checks (microsecond level)
        validation_tasks = [
            self.validate_schema(record),
            self.validate_required_fields(record),
            self.validate_data_types(record),
            self.validate_business_rules(record)
        ]
        
        # Execute validations concurrently
        validation_results = await asyncio.gather(*validation_tasks)
        
        # Aggregate results
        for result in validation_results:
            if not result['valid']:
                validation_result['is_valid'] = False
                validation_result['errors'].extend(result.get('errors', []))
            validation_result['warnings'].extend(result.get('warnings', []))
        
        return validation_result
    
    async def validate_schema(self, record):
        """Fast schema validation"""
        
        required_fields = self.quality_rules.get('required_fields', [])
        
        missing_fields = [field for field in required_fields if field not in record]
        
        return {
            'valid': len(missing_fields) == 0,
            'errors': [f'Missing required field: {field}' for field in missing_fields]
        }
    
    async def validate_business_rules(self, record):
        """Fast business rule validation"""
        
        errors = []
        warnings = []
        
        # Example business rules
        if 'amount' in record:
            if record['amount'] < 0:
                errors.append('Amount cannot be negative')
            elif record['amount'] > 10000:
                warnings.append('High amount detected')
        
        if 'email' in record:
            if '@' not in record['email']:
                errors.append('Invalid email format')
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    async def route_valid_record(self, record, partition):
        """Route valid records to appropriate topics"""
        
        # Add quality metadata
        enriched_record = {
            **record,
            'quality_metadata': {
                'validated_at': datetime.now().isoformat(),
                'quality_score': 100,
                'validation_version': '1.0'
            }
        }
        
        # Send to clean data topic
        self.producer.send(
            self.kafka_config['clean_topic'],
            value=enriched_record,
            partition=partition
        )
    
    async def handle_invalid_record(self, record, validation_result):
        """Handle invalid records"""
        
        # Create error record
        error_record = {
            'original_record': record,
            'validation_errors': validation_result['errors'],
            'validation_warnings': validation_result['warnings'],
            'error_timestamp': datetime.now().isoformat(),
            'processor_id': 'streaming_quality_processor'
        }
        
        # Send to error topic
        self.producer.send(
            self.kafka_config['error_topic'],
            value=error_record
        )
        
        # Update invalid message count
        self.quality_metrics['invalid_messages'] += 1
    
    def get_quality_metrics(self):
        """Get real-time quality metrics"""
        
        total = self.quality_metrics['total_messages']
        if total == 0:
            return {'quality_score': 0, 'message': 'No messages processed'}
        
        quality_score = (self.quality_metrics['valid_messages'] / total) * 100
        avg_processing_time = sum(self.quality_metrics['processing_time_ms']) / len(self.quality_metrics['processing_time_ms'])
        
        return {
            'quality_score': quality_score,
            'total_messages': total,
            'valid_messages': self.quality_metrics['valid_messages'],
            'invalid_messages': self.quality_metrics['invalid_messages'],
            'avg_processing_time_ms': avg_processing_time
        }

# Real-time Quality Dashboard
class RealTimeQualityDashboard:
    def __init__(self, processors):
        self.processors = processors
        self.dashboard_data = {}
    
    async def update_dashboard(self):
        """Update dashboard with real-time metrics"""
        
        while True:
            dashboard_update = {
                'timestamp': datetime.now().isoformat(),
                'processors': {}
            }
            
            for processor_name, processor in self.processors.items():
                metrics = processor.get_quality_metrics()
                dashboard_update['processors'][processor_name] = metrics
            
            # Calculate overall metrics
            total_messages = sum(p['total_messages'] for p in dashboard_update['processors'].values())
            total_valid = sum(p['valid_messages'] for p in dashboard_update['processors'].values())
            
            dashboard_update['overall'] = {
                'quality_score': (total_valid / total_messages * 100) if total_messages > 0 else 0,
                'total_messages': total_messages,
                'processors_count': len(self.processors)
            }
            
            self.dashboard_data = dashboard_update
            
            # Wait before next update
            await asyncio.sleep(5)  # Update every 5 seconds
    
    def get_dashboard_data(self):
        """Get current dashboard data"""
        return self.dashboard_data
```

### 27. How do you handle data quality for different data types (structured, semi-structured, unstructured)?
**Answer:**
Different data types require specialized validation approaches:

```python
import json
import pandas as pd
from jsonschema import validate, ValidationError
import great_expectations as gx

class MultiFormatDataQualityValidator:
    def __init__(self, context):
        self.context = context
        self.validation_strategies = {
            'structured': self.validate_structured_data,
            'semi_structured': self.validate_semi_structured_data,
            'unstructured': self.validate_unstructured_data
        }
    
    def validate_data_by_type(self, data, data_type, validation_config):
        """Route validation based on data type"""
        
        if data_type not in self.validation_strategies:
            raise ValueError(f"Unsupported data type: {data_type}")
        
        return self.validation_strategies[data_type](data, validation_config)
    
    def validate_structured_data(self, df, config):
        """Validate structured data (CSV, database tables, etc.)"""
        
        # Use Great Expectations for structured data
        batch_request = RuntimeBatchRequest(
            datasource_name="pandas_datasource",
            data_connector_name="default_runtime_data_connector",
            data_asset_name="structured_data",
            runtime_parameters={"batch_data": df},
            batch_identifiers={"default_identifier_name": "structured_batch"}
        )
        
        validator = self.context.get_validator(
            batch_request=batch_request,
            expectation_suite_name=config['expectation_suite']
        )
        
        # Standard structured data validations
        validation_result = validator.validate()
        
        return {
            'data_type': 'structured',
            'validation_framework': 'great_expectations',
            'result': validation_result,
            'quality_score': validation_result.statistics['success_percent']
        }
    
    def validate_semi_structured_data(self, data, config):
        """Validate semi-structured data (JSON, XML, etc.)"""
        
        validation_results = {
            'data_type': 'semi_structured',
            'total_records': len(data) if isinstance(data, list) else 1,
            'valid_records': 0,
            'validation_errors': [],
            'schema_violations': [],
            'business_rule_violations': []
        }
        
        # Convert to list if single record
        records = data if isinstance(data, list) else [data]
        
        for i, record in enumerate(records):
            record_validation = self.validate_json_record(record, config, i)
            
            if record_validation['is_valid']:
                validation_results['valid_records'] += 1
            else:
                validation_results['validation_errors'].extend(record_validation['errors'])
                validation_results['schema_violations'].extend(record_validation['schema_errors'])
                validation_results['business_rule_violations'].extend(record_validation['business_errors'])
        
        # Calculate quality score
        validation_results['quality_score'] = (
            validation_results['valid_records'] / validation_results['total_records']
        ) * 100
        
        return validation_results
    
    def validate_json_record(self, record, config, record_index):
        """Validate individual JSON record"""
        
        validation_result = {
            'is_valid': True,
            'errors': [],
            'schema_errors': [],
            'business_errors': []
        }
        
        # 1. Schema validation
        if 'json_schema' in config:
            try:
                validate(instance=record, schema=config['json_schema'])
            except ValidationError as e:
                validation_result['is_valid'] = False
                validation_result['schema_errors'].append({
                    'record_index': record_index,
                    'error': str(e),
                    'path': list(e.path) if e.path else []
                })
        
        # 2. Required fields validation
        required_fields = config.get('required_fields', [])
        for field in required_fields:
            if field not in record:
                validation_result['is_valid'] = False
                validation_result['errors'].append({
                    'record_index': record_index,
                    'error': f'Missing required field: {field}'
                })
        
        # 3. Data type validation
        field_types = config.get('field_types', {})
        for field, expected_type in field_types.items():
            if field in record:
                if not isinstance(record[field], expected_type):
                    validation_result['is_valid'] = False
                    validation_result['errors'].append({
                        'record_index': record_index,
                        'error': f'Field {field} has wrong type. Expected {expected_type.__name__}, got {type(record[field]).__name__}'
                    })
        
        # 4. Business rules validation
        business_rules = config.get('business_rules', [])
        for rule in business_rules:
            if not self.evaluate_business_rule(record, rule):
                validation_result['is_valid'] = False
                validation_result['business_errors'].append({
                    'record_index': record_index,
                    'rule': rule['name'],
                    'error': rule['error_message']
                })
        
        return validation_result
    
    def validate_unstructured_data(self, data, config):
        """Validate unstructured data (text, images, etc.)"""
        
        validation_results = {
            'data_type': 'unstructured',
            'validation_framework': 'custom',
            'total_items': len(data) if isinstance(data, list) else 1,
            'valid_items': 0,
            'validation_errors': [],
            'quality_metrics': {}
        }
        
        # Convert to list if single item
        items = data if isinstance(data, list) else [data]
        
        for i, item in enumerate(items):
            item_validation = self.validate_unstructured_item(item, config, i)
            
            if item_validation['is_valid']:
                validation_results['valid_items'] += 1
            else:
                validation_results['validation_errors'].extend(item_validation['errors'])
        
        # Calculate quality metrics
        validation_results['quality_score'] = (
            validation_results['valid_items'] / validation_results['total_items']
        ) * 100
        
        # Add content-specific metrics
        if config.get('content_type') == 'text':
            validation_results['quality_metrics'] = self.calculate_text_quality_metrics(items)
        
        return validation_results
    
    def validate_unstructured_item(self, item, config, item_index):
        """Validate individual unstructured item"""
        
        validation_result = {
            'is_valid': True,
            'errors': []
        }
        
        content_type = config.get('content_type', 'text')
        
        if content_type == 'text':
            # Text-specific validations
            if not isinstance(item, str):
                validation_result['is_valid'] = False
                validation_result['errors'].append({
                    'item_index': item_index,
                    'error': 'Item is not a string'
                })
            else:
                # Length validation
                min_length = config.get('min_length', 0)
                max_length = config.get('max_length', float('inf'))
                
                if len(item) < min_length:
                    validation_result['is_valid'] = False
                    validation_result['errors'].append({
                        'item_index': item_index,
                        'error': f'Text too short. Minimum length: {min_length}'
                    })
                
                if len(item) > max_length:
                    validation_result['is_valid'] = False
                    validation_result['errors'].append({
                        'item_index': item_index,
                        'error': f'Text too long. Maximum length: {max_length}'
                    })
                
                # Language detection (if required)
                if 'expected_language' in config:
                    detected_language = self.detect_language(item)
                    if detected_language != config['expected_language']:
                        validation_result['is_valid'] = False
                        validation_result['errors'].append({
                            'item_index': item_index,
                            'error': f'Unexpected language. Expected: {config["expected_language"]}, Detected: {detected_language}'
                        })
        
        return validation_result
    
    def calculate_text_quality_metrics(self, text_items):
        """Calculate quality metrics for text data"""
        
        if not text_items:
            return {}
        
        # Basic text metrics
        lengths = [len(item) for item in text_items if isinstance(item, str)]
        
        metrics = {
            'avg_length': sum(lengths) / len(lengths) if lengths else 0,
            'min_length': min(lengths) if lengths else 0,
            'max_length': max(lengths) if lengths else 0,
            'total_characters': sum(lengths),
            'empty_items': sum(1 for item in text_items if not item or not item.strip()),
            'non_ascii_items': sum(1 for item in text_items if isinstance(item, str) and not item.isascii())
        }
        
        return metrics

# Usage example
def multi_format_validation_example():
    """Example of validating different data formats"""
    
    validator = MultiFormatDataQualityValidator(context)
    
    # 1. Structured data validation
    structured_data = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'email': ['alice@email.com', 'bob@email.com', 'charlie@email.com']
    })
    
    structured_config = {
        'expectation_suite': 'structured_data_suite'
    }
    
    structured_result = validator.validate_data_by_type(
        structured_data, 'structured', structured_config
    )
    
    # 2. Semi-structured data validation
    semi_structured_data = [
        {'id': 1, 'name': 'Alice', 'metadata': {'age': 30, 'city': 'NYC'}},
        {'id': 2, 'name': 'Bob', 'metadata': {'age': 25, 'city': 'LA'}}
    ]
    
    json_schema = {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer'},
            'name': {'type': 'string'},
            'metadata': {
                'type': 'object',
                'properties': {
                    'age': {'type': 'integer'},
                    'city': {'type': 'string'}
                }
            }
        },
        'required': ['id', 'name']
    }
    
    semi_structured_config = {
        'json_schema': json_schema,
        'required_fields': ['id', 'name'],
        'field_types': {'id': int, 'name': str}
    }
    
    semi_structured_result = validator.validate_data_by_type(
        semi_structured_data, 'semi_structured', semi_structured_config
    )
    
    # 3. Unstructured data validation
    unstructured_data = [
        "This is a valid text document with sufficient content.",
        "Short",
        "This is another valid document with good length and content quality."
    ]
    
    unstructured_config = {
        'content_type': 'text',
        'min_length': 10,
        'max_length': 1000,
        'expected_language': 'en'
    }
    
    unstructured_result = validator.validate_data_by_type(
        unstructured_data, 'unstructured', unstructured_config
    )
    
    # Print results
    print(f"Structured data quality score: {structured_result['quality_score']:.2f}%")
    print(f"Semi-structured data quality score: {semi_structured_result['quality_score']:.2f}%")
    print(f"Unstructured data quality score: {unstructured_result['quality_score']:.2f}%")
    
    return {
        'structured': structured_result,
        'semi_structured': semi_structured_result,
        'unstructured': unstructured_result
    }
```
