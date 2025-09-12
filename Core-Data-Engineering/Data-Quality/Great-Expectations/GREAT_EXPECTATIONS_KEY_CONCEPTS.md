# Great Expectations Key Concepts for Data Engineers

## 📋 Table of Contents

1. [Introduction to Great Expectations](#introduction-to-great-expectations)
2. [Core Architecture](#core-architecture)
3. [Data Context](#data-context)
4. [Datasources and Data Connectors](#datasources-and-data-connectors)
5. [Expectations Framework](#expectations-framework)
6. [Expectation Suites](#expectation-suites)
7. [Validators](#validators)
8. [Checkpoints](#checkpoints)
9. [Data Documentation](#data-documentation)
10. [Integration Patterns](#integration-patterns)
11. [Best Practices](#best-practices)
12. [Advanced Features](#advanced-features)

---

## Introduction to Great Expectations

### What is Great Expectations?
Great Expectations is an open-source Python library that helps data teams eliminate pipeline debt through data testing, documentation, and profiling. It enables teams to:

- **Validate data** at every stage of the pipeline
- **Generate documentation** automatically from data
- **Profile data** to understand its characteristics
- **Monitor data quality** continuously
- **Collaborate** effectively around data expectations

### Core Philosophy
Great Expectations follows the principle of "expectations as code" - treating data quality rules as first-class citizens in the codebase, version-controlled and testable like any other code.

### Key Benefits
```python
# Example: Business impact of Great Expectations
data_quality_benefits = {
    'reduced_pipeline_failures': '85%',
    'faster_issue_detection': '10x faster',
    'improved_data_trust': '95% stakeholder confidence',
    'documentation_automation': '100% up-to-date docs',
    'collaboration_improvement': '3x faster onboarding'
}
```

---

## Core Architecture

### Architecture Overview
```
┌─────────────────────────────────────────────────────────────┐
│                    Great Expectations                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Data Docs   │  │ Checkpoints │  │   Validation        │  │
│  │ (HTML/JSON) │  │ (Workflows) │  │   Results           │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Expectation │  │ Validators  │  │   Batch Requests    │  │
│  │ Suites      │  │             │  │                     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Datasources │  │ Data        │  │   Execution         │  │
│  │             │  │ Connectors  │  │   Engines           │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                    Data Context                             │
│              (Central Configuration Hub)                    │
└─────────────────────────────────────────────────────────────┘
```

### Component Relationships
```python
import great_expectations as gx

# 1. Data Context - Central hub
context = gx.get_context()

# 2. Datasource - Connection to data
datasource = context.get_datasource("my_datasource")

# 3. Batch Request - Specify data to validate
batch_request = RuntimeBatchRequest(
    datasource_name="my_datasource",
    data_connector_name="default_runtime_data_connector",
    data_asset_name="customer_data",
    runtime_parameters={"batch_data": df},
    batch_identifiers={"default_identifier_name": "batch_1"}
)

# 4. Expectation Suite - Collection of data quality rules
suite = context.get_expectation_suite("customer_suite")

# 5. Validator - Combines data and expectations
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name="customer_suite"
)

# 6. Validation Results - Outcome of validation
results = validator.validate()

# 7. Checkpoint - Automated workflow
checkpoint_result = context.run_checkpoint("customer_checkpoint")
```

---

## Data Context

### What is Data Context?
The Data Context is the primary entry point for Great Expectations. It manages configuration, coordinates components, and provides the main API for interacting with the framework.

### Data Context Configuration
```python
# Initialize Data Context
import great_expectations as gx

# Method 1: Default context (looks for great_expectations.yml)
context = gx.get_context()

# Method 2: Specify context root directory
context = gx.get_context(context_root_dir="/path/to/ge/config")

# Method 3: In-memory context (for testing)
context = gx.get_context(mode="memory")

# Method 4: Cloud-based context
context = gx.get_context(
    cloud_mode=True,
    cloud_access_token="your_token",
    cloud_organization_id="your_org_id"
)
```

### Context Directory Structure
```
great_expectations/
├── great_expectations.yml          # Main configuration file
├── expectations/                   # Expectation suites
│   ├── customer_suite.json
│   └── order_suite.json
├── checkpoints/                    # Checkpoint configurations
│   ├── customer_checkpoint.yml
│   └── daily_validation.yml
├── plugins/                        # Custom expectations and actions
│   ├── custom_expectations/
│   └── custom_actions/
├── uncommitted/                    # Local development files
│   ├── config_variables.yml       # Environment-specific variables
│   ├── data_docs/                 # Generated documentation
│   └── validations/               # Validation results
└── .gitignore                     # Git ignore patterns
```

### Context Configuration File
```yaml
# great_expectations.yml
config_version: 3.0

datasources:
  production_db:
    class_name: Datasource
    execution_engine:
      class_name: SqlAlchemyExecutionEngine
      connection_string: ${DATABASE_URL}
    data_connectors:
      default_runtime_data_connector:
        class_name: RuntimeDataConnector
        batch_identifiers:
          - default_identifier_name

stores:
  expectations_store:
    class_name: ExpectationsStore
    store_backend:
      class_name: TupleFilesystemStoreBackend
      base_directory: expectations/

  validations_store:
    class_name: ValidationsStore
    store_backend:
      class_name: TupleFilesystemStoreBackend
      base_directory: uncommitted/validations/

  evaluation_parameter_store:
    class_name: EvaluationParameterStore

  checkpoint_store:
    class_name: CheckpointStore
    store_backend:
      class_name: TupleFilesystemStoreBackend
      base_directory: checkpoints/

expectations_store_name: expectations_store
validations_store_name: validations_store
evaluation_parameter_store_name: evaluation_parameter_store
checkpoint_store_name: checkpoint_store

data_docs_sites:
  local_site:
    class_name: SiteBuilder
    show_how_to_buttons: true
    store_backend:
      class_name: TupleFilesystemStoreBackend
      base_directory: uncommitted/data_docs/local_site/
    site_index_builder:
      class_name: DefaultSiteIndexBuilder

anonymous_usage_statistics:
  enabled: false
```

---

## Datasources and Data Connectors

### Datasource Types
Great Expectations supports multiple datasource types for different data storage systems:

```python
# 1. Pandas Datasource (Files: CSV, Excel, JSON, Parquet)
pandas_datasource = {
    "name": "file_datasource",
    "class_name": "Datasource",
    "execution_engine": {
        "class_name": "PandasExecutionEngine"
    },
    "data_connectors": {
        "inferred_connector": {
            "class_name": "InferredAssetFilesystemDataConnector",
            "base_directory": "/data/files/",
            "default_regex": {
                "group_names": ["data_asset_name"],
                "pattern": "(.*)\\.csv"
            }
        }
    }
}

# 2. SQL Datasource (PostgreSQL, MySQL, SQLite, etc.)
sql_datasource = {
    "name": "database_datasource",
    "class_name": "Datasource",
    "execution_engine": {
        "class_name": "SqlAlchemyExecutionEngine",
        "connection_string": "postgresql://user:pass@host:port/db"
    },
    "data_connectors": {
        "table_connector": {
            "class_name": "InferredAssetSqlDataConnector",
            "include_schema_name": True
        }
    }
}

# 3. Spark Datasource (Big Data Processing)
spark_datasource = {
    "name": "spark_datasource",
    "class_name": "Datasource",
    "execution_engine": {
        "class_name": "SparkDFExecutionEngine"
    },
    "data_connectors": {
        "runtime_connector": {
            "class_name": "RuntimeDataConnector",
            "batch_identifiers": ["run_id"]
        }
    }
}

# 4. Cloud Storage Datasource (S3, GCS, Azure Blob)
s3_datasource = {
    "name": "s3_datasource",
    "class_name": "Datasource",
    "execution_engine": {
        "class_name": "PandasExecutionEngine"
    },
    "data_connectors": {
        "s3_connector": {
            "class_name": "InferredAssetS3DataConnector",
            "bucket": "my-data-bucket",
            "prefix": "data/",
            "default_regex": {
                "group_names": ["data_asset_name", "year", "month"],
                "pattern": r"data/(\w+)/(\d{4})/(\d{2})/.*\.parquet"
            }
        }
    }
}
```

### Data Connector Types
```python
# 1. RuntimeDataConnector - For programmatic data passing
runtime_connector = {
    "class_name": "RuntimeDataConnector",
    "batch_identifiers": ["default_identifier_name"]
}

# 2. InferredAssetFilesystemDataConnector - Auto-discover files
inferred_filesystem_connector = {
    "class_name": "InferredAssetFilesystemDataConnector",
    "base_directory": "/path/to/data/",
    "default_regex": {
        "group_names": ["data_asset_name"],
        "pattern": "(.*)\\.csv"
    }
}

# 3. ConfiguredAssetFilesystemDataConnector - Explicitly configured files
configured_filesystem_connector = {
    "class_name": "ConfiguredAssetFilesystemDataConnector",
    "base_directory": "/path/to/data/",
    "assets": {
        "customer_data": {
            "group_names": ["year", "month"],
            "pattern": "customers_(\d{4})_(\d{2})\\.csv"
        }
    }
}

# 4. InferredAssetSqlDataConnector - Auto-discover database tables
inferred_sql_connector = {
    "class_name": "InferredAssetSqlDataConnector",
    "include_schema_name": True,
    "introspection_directives": {
        "schema_name": "public"
    }
}
```

### Batch Requests
```python
from great_expectations.core.batch import RuntimeBatchRequest, BatchRequest

# 1. Runtime Batch Request (for DataFrames, in-memory data)
runtime_batch_request = RuntimeBatchRequest(
    datasource_name="pandas_datasource",
    data_connector_name="default_runtime_data_connector",
    data_asset_name="customer_data",
    runtime_parameters={"batch_data": df},
    batch_identifiers={"default_identifier_name": "customer_batch_001"}
)

# 2. File-based Batch Request
file_batch_request = BatchRequest(
    datasource_name="file_datasource",
    data_connector_name="inferred_connector",
    data_asset_name="customer_data",
    data_connector_query={
        "batch_filter_parameters": {
            "year": "2023",
            "month": "12"
        }
    }
)

# 3. SQL Batch Request
sql_batch_request = BatchRequest(
    datasource_name="database_datasource",
    data_connector_name="table_connector",
    data_asset_name="public.customers",
    data_connector_query={
        "custom_sql": "SELECT * FROM customers WHERE created_date >= '2023-01-01'"
    }
)
```

---

## Expectations Framework

### Expectation Categories
Great Expectations provides a comprehensive library of built-in expectations:

```python
# 1. Table-level Expectations
validator.expect_table_row_count_to_be_between(min_value=1000, max_value=10000)
validator.expect_table_column_count_to_equal(15)
validator.expect_table_columns_to_match_ordered_list([
    "id", "name", "email", "created_date"
])

# 2. Column Existence Expectations
validator.expect_column_to_exist("customer_id")
validator.expect_column_to_exist("email")

# 3. Data Type Expectations
validator.expect_column_values_to_be_of_type("customer_id", "int64")
validator.expect_column_values_to_be_of_type("email", "object")
validator.expect_column_values_to_be_of_type("created_date", "datetime64[ns]")

# 4. Null Value Expectations
validator.expect_column_values_to_not_be_null("customer_id")
validator.expect_column_values_to_not_be_null("email", mostly=0.95)  # Allow 5% nulls

# 5. Uniqueness Expectations
validator.expect_column_values_to_be_unique("customer_id")
validator.expect_column_values_to_be_unique("email")

# 6. Range Expectations
validator.expect_column_values_to_be_between("age", min_value=0, max_value=120)
validator.expect_column_values_to_be_between("order_amount", min_value=0.01)

# 7. Set Membership Expectations
validator.expect_column_values_to_be_in_set("status", ["active", "inactive", "pending"])
validator.expect_column_distinct_values_to_be_in_set("country", ["US", "CA", "UK"])

# 8. String Pattern Expectations
validator.expect_column_values_to_match_regex(
    "email", r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)
validator.expect_column_values_to_match_regex(
    "phone", r'^\+?1?[0-9]{10,15}$'
)

# 9. String Length Expectations
validator.expect_column_value_lengths_to_be_between("name", min_value=1, max_value=100)
validator.expect_column_value_lengths_to_equal("country_code", 2)

# 10. Statistical Expectations
validator.expect_column_mean_to_be_between("order_amount", min_value=50, max_value=500)
validator.expect_column_stdev_to_be_between("order_amount", min_value=10, max_value=200)
validator.expect_column_quantile_values_to_be_between(
    "age",
    quantile_ranges={
        "quantiles": [0.25, 0.5, 0.75],
        "value_ranges": [[20, 30], [35, 45], [50, 65]]
    }
)

# 11. Multi-column Expectations
validator.expect_multicolumn_values_to_be_unique(["customer_id", "order_date"])
validator.expect_column_pair_values_A_to_be_greater_than_B("end_date", "start_date")
validator.expect_column_pair_values_to_be_equal("calculated_total", "order_total")

# 12. Date/Time Expectations
validator.expect_column_values_to_be_dateutil_parseable("created_date")
validator.expect_column_values_to_match_strftime_format("created_date", "%Y-%m-%d")
validator.expect_column_values_to_be_between(
    "created_date",
    min_value="2020-01-01",
    max_value="2024-12-31"
)
```

### Custom Expectations
```python
from great_expectations.expectations import ColumnMapExpectation
from great_expectations.execution_engine import PandasExecutionEngine
from great_expectations.metrics import ColumnMetricProvider, column_condition_partial

# 1. Custom Column Map Expectation
class ExpectColumnValuesToBeValidEmail(ColumnMapExpectation):
    """Expect column values to be valid email addresses"""
    
    map_metric = "column_values.valid_email"
    success_keys = ("mostly",)
    
    @classmethod
    def _prescriptive_template(cls, renderer_type):
        return {
            "content_block_type": "string_template",
            "string_template": {
                "template": "Values in column $column must be valid email addresses.",
                "params": {"column": "$column"},
            },
        }

# 2. Custom Metric Provider
class ColumnValuesValidEmail(ColumnMetricProvider):
    metric_name = "column_values.valid_email"
    
    @column_condition_partial(engine=PandasExecutionEngine)
    def _pandas(cls, column, **kwargs):
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return column.str.match(email_pattern, na=False)

# 3. Business-specific Custom Expectation
class ExpectColumnValuesToBeValidCreditCard(ColumnMapExpectation):
    """Expect column values to be valid credit card numbers using Luhn algorithm"""
    
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

class ColumnValuesValidCreditCard(ColumnMetricProvider):
    metric_name = "column_values.valid_credit_card"
    
    @column_condition_partial(engine=PandasExecutionEngine)
    def _pandas(cls, column, **kwargs):
        def luhn_check(card_number):
            if not isinstance(card_number, str):
                return False
            
            # Remove spaces and dashes
            card_number = card_number.replace(" ", "").replace("-", "")
            
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
        
        return column.apply(luhn_check)

# Usage of custom expectations
validator.expect_column_values_to_be_valid_email("email_address")
validator.expect_column_values_to_be_valid_credit_card("credit_card_number")
```

---

## Expectation Suites

### Creating and Managing Suites
```python
# 1. Create new expectation suite
suite_name = "customer_data_quality_suite"
suite = context.create_expectation_suite(suite_name, overwrite_existing=True)

# 2. Add expectations to suite
suite.expect_column_to_exist("customer_id")
suite.expect_column_values_to_not_be_null("customer_id")
suite.expect_column_values_to_be_unique("customer_id")

# 3. Add metadata to expectations
suite.expect_column_values_to_be_between(
    "age", 
    min_value=0, 
    max_value=120,
    meta={
        "notes": "Age must be realistic for human customers",
        "owner": "data-quality-team",
        "criticality": "high"
    }
)

# 4. Save suite
context.save_expectation_suite(suite)

# 5. Load existing suite
loaded_suite = context.get_expectation_suite(suite_name)

# 6. Update existing suite
def update_suite_with_business_rules(suite_name):
    """Add business-specific expectations to existing suite"""
    
    suite = context.get_expectation_suite(suite_name)
    
    # Add new business rules
    suite.expect_column_values_to_match_regex(
        "customer_id", 
        r'^CUST[0-9]{6}$',
        meta={"notes": "Customer ID must follow CUST######ß format"}
    )
    
    suite.expect_column_values_to_be_in_set(
        "subscription_tier",
        ["basic", "premium", "enterprise"],
        meta={"notes": "Only valid subscription tiers allowed"}
    )
    
    # Save updated suite
    context.save_expectation_suite(suite)
    
    return suite
```

### Suite Organization Patterns
```python
# 1. Domain-based Suite Organization
def create_domain_suites():
    """Create suites organized by business domain"""
    
    # Customer domain suite
    customer_suite = context.create_expectation_suite("customer_domain_suite")
    customer_suite.expect_column_to_exist("customer_id")
    customer_suite.expect_column_values_to_be_unique("customer_id")
    customer_suite.expect_column_values_to_match_regex("email", r'^[^@]+@[^@]+\.[^@]+$')
    
    # Order domain suite
    order_suite = context.create_expectation_suite("order_domain_suite")
    order_suite.expect_column_to_exist("order_id")
    order_suite.expect_column_values_to_be_unique("order_id")
    order_suite.expect_column_values_to_be_between("order_amount", 0.01, 10000)
    
    # Product domain suite
    product_suite = context.create_expectation_suite("product_domain_suite")
    product_suite.expect_column_to_exist("product_id")
    product_suite.expect_column_values_to_be_unique("product_id")
    product_suite.expect_column_values_to_be_in_set("category", ["electronics", "clothing", "books"])
    
    # Save all suites
    context.save_expectation_suite(customer_suite)
    context.save_expectation_suite(order_suite)
    context.save_expectation_suite(product_suite)

# 2. Layer-based Suite Organization
def create_layer_suites():
    """Create suites organized by data pipeline layer"""
    
    # Raw data layer suite (basic structure validation)
    raw_suite = context.create_expectation_suite("raw_data_suite")
    raw_suite.expect_table_row_count_to_be_between(min_value=1)
    raw_suite.expect_column_to_exist("id")
    raw_suite.expect_column_values_to_not_be_null("id")
    
    # Bronze layer suite (data type validation)
    bronze_suite = context.create_expectation_suite("bronze_data_suite")
    bronze_suite.expect_column_values_to_be_of_type("id", "int64")
    bronze_suite.expect_column_values_to_be_of_type("created_date", "datetime64[ns]")
    bronze_suite.expect_column_values_to_be_unique("id")
    
    # Silver layer suite (business rule validation)
    silver_suite = context.create_expectation_suite("silver_data_suite")
    silver_suite.expect_column_values_to_be_between("age", 0, 120)
    silver_suite.expect_column_values_to_match_regex("email", r'^[^@]+@[^@]+\.[^@]+$')
    silver_suite.expect_column_values_to_be_in_set("status", ["active", "inactive"])
    
    # Gold layer suite (statistical validation)
    gold_suite = context.create_expectation_suite("gold_data_suite")
    gold_suite.expect_column_mean_to_be_between("order_amount", 50, 500)
    gold_suite.expect_column_stdev_to_be_between("order_amount", 10, 200)
    
    # Save all suites
    for suite in [raw_suite, bronze_suite, silver_suite, gold_suite]:
        context.save_expectation_suite(suite)

# 3. Criticality-based Suite Organization
def create_criticality_suites():
    """Create suites organized by expectation criticality"""
    
    # Critical expectations (must pass for pipeline to continue)
    critical_suite = context.create_expectation_suite("critical_expectations")
    critical_suite.expect_column_to_exist("customer_id")
    critical_suite.expect_column_values_to_not_be_null("customer_id")
    critical_suite.expect_column_values_to_be_unique("customer_id")
    
    # Warning expectations (log warnings but don't fail pipeline)
    warning_suite = context.create_expectation_suite("warning_expectations")
    warning_suite.expect_column_values_to_not_be_null("phone", mostly=0.8)
    warning_suite.expect_column_mean_to_be_between("order_amount", 40, 600)
    
    # Monitoring expectations (for trend analysis)
    monitoring_suite = context.create_expectation_suite("monitoring_expectations")
    monitoring_suite.expect_table_row_count_to_be_between(min_value=900, max_value=1100)
    monitoring_suite.expect_column_distinct_values_to_be_in_set("country", ["US", "CA", "UK", "DE"])
    
    # Save all suites
    for suite in [critical_suite, warning_suite, monitoring_suite]:
        context.save_expectation_suite(suite)
```

---

## Validators

### Creating and Using Validators
```python
# 1. Basic Validator Creation
def create_basic_validator():
    """Create basic validator for data validation"""
    
    # Create batch request
    batch_request = RuntimeBatchRequest(
        datasource_name="pandas_datasource",
        data_connector_name="default_runtime_data_connector",
        data_asset_name="customer_data",
        runtime_parameters={"batch_data": df},
        batch_identifiers={"default_identifier_name": "validation_batch"}
    )
    
    # Get validator
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name="customer_data_quality_suite"
    )
    
    return validator

# 2. Interactive Expectation Development
def develop_expectations_interactively(validator):
    """Develop expectations interactively using validator"""
    
    # Explore data structure
    print("Column names:", validator.active_batch.data.columns.tolist())
    print("Data types:", validator.active_batch.data.dtypes.to_dict())
    print("Shape:", validator.active_batch.data.shape)
    
    # Add expectations interactively
    validator.expect_column_to_exist("customer_id")
    validator.expect_column_values_to_not_be_null("customer_id")
    validator.expect_column_values_to_be_unique("customer_id")
    
    # Test expectations immediately
    result = validator.expect_column_values_to_be_between("age", 0, 120)
    print("Age range validation:", result.success)
    
    # Save expectations to suite
    validator.save_expectation_suite()
    
    return validator

# 3. Batch Validation
def validate_multiple_batches():
    """Validate multiple batches of data"""
    
    validation_results = []
    
    # List of data batches to validate
    data_batches = [
        {"data": df1, "batch_id": "batch_001"},
        {"data": df2, "batch_id": "batch_002"},
        {"data": df3, "batch_id": "batch_003"}
    ]
    
    for batch_info in data_batches:
        # Create batch request
        batch_request = RuntimeBatchRequest(
            datasource_name="pandas_datasource",
            data_connector_name="default_runtime_data_connector",
            data_asset_name="customer_data",
            runtime_parameters={"batch_data": batch_info["data"]},
            batch_identifiers={"default_identifier_name": batch_info["batch_id"]}
        )
        
        # Get validator
        validator = context.get_validator(
            batch_request=batch_request,
            expectation_suite_name="customer_data_quality_suite"
        )
        
        # Validate
        result = validator.validate()
        validation_results.append({
            "batch_id": batch_info["batch_id"],
            "success": result.success,
            "statistics": result.statistics
        })
        
        print(f"Batch {batch_info['batch_id']}: {'PASSED' if result.success else 'FAILED'}")
    
    return validation_results
```

### Validation Results Analysis
```python
def analyze_validation_results(validation_result):
    """Analyze and process validation results"""
    
    analysis = {
        "overall_success": validation_result.success,
        "run_id": validation_result.meta.get("run_id"),
        "statistics": validation_result.statistics,
        "expectation_results": []
    }
    
    # Analyze individual expectation results
    for result in validation_result.results:
        expectation_analysis = {
            "expectation_type": result.expectation_config.expectation_type,
            "success": result.success,
            "column": result.expectation_config.kwargs.get("column"),
            "result_details": result.result
        }
        
        # Add failure details for failed expectations
        if not result.success:
            expectation_analysis["failure_reason"] = result.result.get("partial_unexpected_list", [])
            expectation_analysis["unexpected_count"] = result.result.get("unexpected_count", 0)
            expectation_analysis["unexpected_percent"] = result.result.get("unexpected_percent", 0)
        
        analysis["expectation_results"].append(expectation_analysis)
    
    # Generate summary statistics
    total_expectations = len(validation_result.results)
    failed_expectations = sum(1 for r in validation_result.results if not r.success)
    success_rate = ((total_expectations - failed_expectations) / total_expectations) * 100
    
    analysis["summary"] = {
        "total_expectations": total_expectations,
        "passed_expectations": total_expectations - failed_expectations,
        "failed_expectations": failed_expectations,
        "success_rate": success_rate
    }
    
    return analysis

# Usage example
def validation_workflow_example():
    """Complete validation workflow example"""
    
    # Create validator
    validator = create_basic_validator()
    
    # Run validation
    validation_result = validator.validate()
    
    # Analyze results
    analysis = analyze_validation_results(validation_result)
    
    # Print summary
    print(f"Validation Summary:")
    print(f"Overall Success: {analysis['overall_success']}")
    print(f"Success Rate: {analysis['summary']['success_rate']:.2f}%")
    print(f"Failed Expectations: {analysis['summary']['failed_expectations']}")
    
    # Handle failures
    if not analysis['overall_success']:
        print("\nFailed Expectations:")
        for result in analysis['expectation_results']:
            if not result['success']:
                print(f"- {result['expectation_type']} on column '{result['column']}'")
                print(f"  Unexpected count: {result.get('unexpected_count', 'N/A')}")
    
    return analysis
```

This comprehensive guide covers the essential concepts of Great Expectations, providing practical examples and patterns for implementing robust data quality validation in data engineering workflows.