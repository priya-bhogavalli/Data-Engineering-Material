# Great Expectations Comprehensive Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Core Concepts & Architecture (1-25)](#core-concepts--architecture-1-25)
2. [Expectations & Validation (26-50)](#expectations--validation-26-50)
3. [Data Sources & Connectors (51-75)](#data-sources--connectors-51-75)
4. [Checkpoints & Automation (76-100)](#checkpoints--automation-76-100)
5. [Data Documentation & Profiling (101-125)](#data-documentation--profiling-101-125)
6. [Production Integration (126-150)](#production-integration-126-150)

---

## Core Concepts & Architecture (1-25)

### 1. What is Great Expectations and how does it solve data quality challenges?
**Answer:**
Great Expectations is an open-source data validation, documentation, and profiling tool that helps teams maintain data quality and understand data better.

**Problems Solved:**
- **Data Quality Assurance**: Automated validation of data quality rules
- **Data Documentation**: Self-updating documentation from data
- **Data Profiling**: Understanding data characteristics and patterns
- **Pipeline Monitoring**: Continuous monitoring of data pipelines
- **Collaboration**: Shared understanding of data expectations

```python
# Basic Great Expectations setup
import great_expectations as gx
from great_expectations.core.batch import RuntimeBatchRequest

# Initialize Data Context
context = gx.get_context()

# Create expectation suite
suite = context.create_expectation_suite("my_suite", overwrite_existing=True)

# Add expectations
suite.expect_column_to_exist("customer_id")
suite.expect_column_values_to_not_be_null("customer_id")
suite.expect_column_values_to_be_unique("customer_id")
suite.expect_column_values_to_be_between("age", min_value=0, max_value=120)

# Save suite
context.save_expectation_suite(suite)
```

### 2. Explain Great Expectations architecture and core components
**Answer:**
**Core Components:**

- **Data Context**: Central configuration and coordination
- **Datasources**: Connections to data storage systems
- **Expectations**: Assertions about data properties
- **Expectation Suites**: Collections of related expectations
- **Validators**: Execute expectations against data
- **Checkpoints**: Automated validation workflows
- **Data Docs**: Generated documentation

```python
# Architecture overview
import great_expectations as gx

# 1. Data Context - Central hub
context = gx.get_context()

# 2. Datasource - Connection to data
datasource_config = {
    "name": "my_datasource",
    "class_name": "Datasource",
    "execution_engine": {
        "class_name": "PandasExecutionEngine"
    },
    "data_connectors": {
        "default_runtime_data_connector": {
            "class_name": "RuntimeDataConnector",
            "batch_identifiers": ["default_identifier_name"]
        }
    }
}

context.add_datasource(**datasource_config)

# 3. Expectation Suite - Collection of expectations
suite = context.create_expectation_suite("customer_data_suite")

# 4. Validator - Execute expectations
batch_request = RuntimeBatchRequest(
    datasource_name="my_datasource",
    data_connector_name="default_runtime_data_connector",
    data_asset_name="customer_data",
    runtime_parameters={"batch_data": df},
    batch_identifiers={"default_identifier_name": "customer_batch"}
)

validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name="customer_data_suite"
)
```

### 3. What are the different types of expectations in Great Expectations?
**Answer:**
**Expectation Categories:**

```python
# 1. Table-level expectations
validator.expect_table_row_count_to_be_between(min_value=1000, max_value=10000)
validator.expect_table_column_count_to_equal(15)
validator.expect_table_columns_to_match_ordered_list([
    "customer_id", "name", "email", "age", "signup_date"
])

# 2. Column existence expectations
validator.expect_column_to_exist("customer_id")
validator.expect_column_to_exist("email")

# 3. Column type expectations
validator.expect_column_values_to_be_of_type("customer_id", "int64")
validator.expect_column_values_to_be_of_type("email", "object")
validator.expect_column_values_to_be_of_type("signup_date", "datetime64[ns]")

# 4. Column value expectations
validator.expect_column_values_to_not_be_null("customer_id")
validator.expect_column_values_to_be_unique("customer_id")
validator.expect_column_values_to_be_between("age", min_value=13, max_value=120)

# 5. String pattern expectations
validator.expect_column_values_to_match_regex("email", r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
validator.expect_column_values_to_match_regex("phone", r'^\+?1?[0-9]{10,15}$')

# 6. Set membership expectations
validator.expect_column_values_to_be_in_set("status", ["active", "inactive", "pending"])
validator.expect_column_values_to_be_in_type_list("priority", ["high", "medium", "low"])

# 7. Statistical expectations
validator.expect_column_mean_to_be_between("order_amount", min_value=50, max_value=500)
validator.expect_column_stdev_to_be_between("order_amount", min_value=10, max_value=200)
validator.expect_column_quantile_values_to_be_between("age", quantile_ranges={
    "quantiles": [0.25, 0.5, 0.75],
    "value_ranges": [[20, 30], [30, 40], [40, 60]]
})

# 8. Multi-column expectations
validator.expect_multicolumn_values_to_be_unique(["customer_id", "order_date"])
validator.expect_column_pair_values_A_to_be_greater_than_B("end_date", "start_date")
```

### 4. How do you create custom expectations?
**Answer:**
**Custom Expectation Development:**

```python
# Method 1: Custom expectation class
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
from great_expectations.execution_engine.util import execute_pandas_df
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

# Method 2: Custom expectation using existing patterns
def expect_column_values_to_be_business_email(validator, column):
    """Custom expectation for business email validation"""
    
    # Business domains to exclude
    personal_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
    
    # Create regex pattern excluding personal domains
    business_email_pattern = r'^[a-zA-Z0-9._%+-]+@(?!' + '|'.join(personal_domains) + r')[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    return validator.expect_column_values_to_match_regex(
        column=column,
        regex=business_email_pattern,
        meta={"notes": "Validates business email addresses (excludes common personal domains)"}
    )

# Usage
expect_column_values_to_be_business_email(validator, "work_email")
```

### 5. How do you configure datasources in Great Expectations?
**Answer:**
**Datasource Configuration:**

```python
# 1. Pandas datasource (CSV, Excel, etc.)
pandas_datasource_config = {
    "name": "pandas_datasource",
    "class_name": "Datasource",
    "execution_engine": {
        "class_name": "PandasExecutionEngine"
    },
    "data_connectors": {
        "default_inferred_data_connector": {
            "class_name": "InferredAssetFilesystemDataConnector",
            "base_directory": "/path/to/data",
            "default_regex": {
                "group_names": ["data_asset_name"],
                "pattern": "(.*)\\.csv"
            }
        }
    }
}

# 2. Spark datasource
spark_datasource_config = {
    "name": "spark_datasource",
    "class_name": "Datasource",
    "execution_engine": {
        "class_name": "SparkDFExecutionEngine"
    },
    "data_connectors": {
        "default_runtime_data_connector": {
            "class_name": "RuntimeDataConnector",
            "batch_identifiers": ["run_id"]
        }
    }
}

# 3. SQL datasource (PostgreSQL)
sql_datasource_config = {
    "name": "postgres_datasource",
    "class_name": "Datasource",
    "execution_engine": {
        "class_name": "SqlAlchemyExecutionEngine",
        "connection_string": "postgresql://user:password@localhost:5432/database"
    },
    "data_connectors": {
        "default_runtime_data_connector": {
            "class_name": "RuntimeDataConnector",
            "batch_identifiers": ["default_identifier_name"]
        },
        "default_inferred_data_connector": {
            "class_name": "InferredAssetSqlDataConnector",
            "include_schema_name": True
        }
    }
}

# 4. Cloud storage datasource (S3)
s3_datasource_config = {
    "name": "s3_datasource",
    "class_name": "Datasource",
    "execution_engine": {
        "class_name": "PandasExecutionEngine"
    },
    "data_connectors": {
        "default_inferred_data_connector": {
            "class_name": "InferredAssetS3DataConnector",
            "bucket": "my-data-bucket",
            "prefix": "data/",
            "default_regex": {
                "group_names": ["data_asset_name", "year", "month", "day"],
                "pattern": r"data/(\w+)/(\d{4})/(\d{2})/(\d{2})/.*\.csv"
            }
        }
    }
}

# Add datasources to context
context.add_datasource(**pandas_datasource_config)
context.add_datasource(**spark_datasource_config)
context.add_datasource(**sql_datasource_config)
context.add_datasource(**s3_datasource_config)

# Test datasource connection
datasource = context.get_datasource("pandas_datasource")
available_data_asset_names = datasource.get_available_data_asset_names()
print("Available data assets:", available_data_asset_names)
```

---

## Expectations & Validation (26-50)

### 26. How do you create and manage expectation suites?
**Answer:**
**Expectation Suite Management:**

```python
# 1. Create expectation suite
suite_name = "customer_data_quality_suite"
suite = context.create_expectation_suite(suite_name, overwrite_existing=True)

# 2. Add expectations programmatically
def create_customer_expectations(suite):
    """Create comprehensive customer data expectations"""
    
    # Table-level expectations
    suite.expect_table_row_count_to_be_between(min_value=1000, max_value=1000000)
    suite.expect_table_column_count_to_equal(8)
    
    # Required columns
    required_columns = ["customer_id", "first_name", "last_name", "email", 
                       "phone", "signup_date", "status", "lifetime_value"]
    
    for column in required_columns:
        suite.expect_column_to_exist(column)
    
    # Customer ID expectations
    suite.expect_column_values_to_not_be_null("customer_id")
    suite.expect_column_values_to_be_unique("customer_id")
    suite.expect_column_values_to_be_of_type("customer_id", "int64")
    suite.expect_column_values_to_be_between("customer_id", min_value=1, max_value=999999999)
    
    # Name expectations
    suite.expect_column_values_to_not_be_null("first_name")
    suite.expect_column_values_to_not_be_null("last_name")
    suite.expect_column_value_lengths_to_be_between("first_name", min_value=1, max_value=50)
    suite.expect_column_value_lengths_to_be_between("last_name", min_value=1, max_value=50)
    
    # Email expectations
    suite.expect_column_values_to_not_be_null("email")
    suite.expect_column_values_to_be_unique("email")
    suite.expect_column_values_to_match_regex("email", 
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    # Phone expectations
    suite.expect_column_values_to_match_regex("phone", 
        r'^\+?1?[0-9]{10,15}$', mostly=0.95)  # Allow 5% invalid
    
    # Status expectations
    suite.expect_column_values_to_be_in_set("status", 
        ["active", "inactive", "suspended", "pending"])
    
    # Date expectations
    suite.expect_column_values_to_not_be_null("signup_date")
    suite.expect_column_values_to_be_of_type("signup_date", "datetime64[ns]")
    suite.expect_column_values_to_be_between("signup_date", 
        min_value="2020-01-01", max_value="2024-12-31")
    
    # Lifetime value expectations
    suite.expect_column_values_to_be_of_type("lifetime_value", "float64")
    suite.expect_column_values_to_be_between("lifetime_value", 
        min_value=0, max_value=100000)
    suite.expect_column_mean_to_be_between("lifetime_value", 
        min_value=100, max_value=5000)
    
    return suite

# Apply expectations
suite = create_customer_expectations(suite)

# 3. Save expectation suite
context.save_expectation_suite(suite)

# 4. Load existing suite
loaded_suite = context.get_expectation_suite("customer_data_quality_suite")

# 5. Update existing suite
def update_suite_with_new_expectations(suite_name):
    """Add new expectations to existing suite"""
    
    suite = context.get_expectation_suite(suite_name)
    
    # Add new expectations
    suite.expect_column_values_to_match_regex("customer_id", r'^[0-9]+$')
    suite.expect_column_distinct_values_to_be_in_set("status", 
        ["active", "inactive", "suspended", "pending", "churned"])
    
    # Save updated suite
    context.save_expectation_suite(suite)
    
    return suite

# 6. Suite validation and testing
def validate_suite_against_sample_data(suite_name, sample_data):
    """Test expectation suite against sample data"""
    
    batch_request = RuntimeBatchRequest(
        datasource_name="pandas_datasource",
        data_connector_name="default_runtime_data_connector",
        data_asset_name="sample_data",
        runtime_parameters={"batch_data": sample_data},
        batch_identifiers={"default_identifier_name": "sample_batch"}
    )
    
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=suite_name
    )
    
    # Run validation
    results = validator.validate()
    
    # Analyze results
    print(f"Validation success: {results.success}")
    print(f"Total expectations: {len(results.results)}")
    print(f"Successful expectations: {sum(1 for r in results.results if r.success)}")
    print(f"Failed expectations: {sum(1 for r in results.results if not r.success)}")
    
    # Show failed expectations
    for result in results.results:
        if not result.success:
            print(f"Failed: {result.expectation_config.expectation_type}")
            print(f"Details: {result.result}")
    
    return results
```

### 27. How do you implement data profiling with Great Expectations?
**Answer:**
**Data Profiling Implementation:**

```python
# 1. Automated profiling with UserConfigurableProfiler
from great_expectations.profile.user_configurable_profiler import UserConfigurableProfiler

def profile_dataset(context, datasource_name, data_asset_name):
    """Profile dataset and generate expectation suite"""
    
    # Create batch request
    batch_request = RuntimeBatchRequest(
        datasource_name=datasource_name,
        data_connector_name="default_runtime_data_connector",
        data_asset_name=data_asset_name,
        runtime_parameters={"batch_data": df},
        batch_identifiers={"default_identifier_name": "profiling_batch"}
    )
    
    # Configure profiler
    profiler = UserConfigurableProfiler(
        profile_dataset=context.get_validator(
            batch_request=batch_request,
            create_expectation_suite_with_name="profiled_suite"
        ),
        excluded_expectations=[
            "expect_column_values_to_be_unique",  # May be too strict
            "expect_column_values_to_not_be_null"  # May be too strict
        ],
        ignored_columns=["internal_id", "created_at"],  # Skip system columns
        not_null_only=False,
        primary_or_compound_key=["customer_id"],
        semantic_types_dict={
            "email": "email",
            "phone": "phone_number",
            "signup_date": "datetime"
        },
        table_expectations_only=False,
        value_set_threshold="few"  # Generate value sets for low-cardinality columns
    )
    
    # Build suite
    suite = profiler.build_suite()
    
    return suite

# 2. Custom profiling function
def custom_data_profiling(df, column_name):
    """Custom profiling for specific column"""
    
    profile = {
        "column_name": column_name,
        "data_type": str(df[column_name].dtype),
        "null_count": df[column_name].isnull().sum(),
        "null_percentage": (df[column_name].isnull().sum() / len(df)) * 100,
        "unique_count": df[column_name].nunique(),
        "unique_percentage": (df[column_name].nunique() / len(df)) * 100
    }
    
    # Numeric column profiling
    if df[column_name].dtype in ['int64', 'float64']:
        profile.update({
            "min_value": df[column_name].min(),
            "max_value": df[column_name].max(),
            "mean": df[column_name].mean(),
            "median": df[column_name].median(),
            "std_dev": df[column_name].std(),
            "quantiles": {
                "25%": df[column_name].quantile(0.25),
                "50%": df[column_name].quantile(0.50),
                "75%": df[column_name].quantile(0.75)
            }
        })
    
    # String column profiling
    elif df[column_name].dtype == 'object':
        profile.update({
            "min_length": df[column_name].str.len().min(),
            "max_length": df[column_name].str.len().max(),
            "avg_length": df[column_name].str.len().mean(),
            "most_common_values": df[column_name].value_counts().head(10).to_dict()
        })
    
    # DateTime column profiling
    elif 'datetime' in str(df[column_name].dtype):
        profile.update({
            "min_date": df[column_name].min(),
            "max_date": df[column_name].max(),
            "date_range_days": (df[column_name].max() - df[column_name].min()).days
        })
    
    return profile

# 3. Generate expectations from profiling
def generate_expectations_from_profile(validator, profile):
    """Generate expectations based on profiling results"""
    
    column_name = profile["column_name"]
    
    # Basic expectations
    if profile["null_percentage"] < 5:  # Less than 5% nulls
        validator.expect_column_values_to_not_be_null(column_name)
    
    if profile["unique_percentage"] > 95:  # More than 95% unique
        validator.expect_column_values_to_be_unique(column_name)
    
    # Numeric expectations
    if "min_value" in profile:
        validator.expect_column_values_to_be_between(
            column_name,
            min_value=profile["min_value"],
            max_value=profile["max_value"]
        )
        
        # Statistical expectations
        validator.expect_column_mean_to_be_between(
            column_name,
            min_value=profile["mean"] * 0.8,  # 20% tolerance
            max_value=profile["mean"] * 1.2
        )
    
    # String expectations
    if "min_length" in profile:
        validator.expect_column_value_lengths_to_be_between(
            column_name,
            min_value=profile["min_length"],
            max_value=profile["max_length"]
        )
        
        # Value set expectations for low cardinality
        if profile["unique_count"] <= 20:
            unique_values = list(profile["most_common_values"].keys())
            validator.expect_column_values_to_be_in_set(column_name, unique_values)
    
    # DateTime expectations
    if "min_date" in profile:
        validator.expect_column_values_to_be_between(
            column_name,
            min_value=profile["min_date"],
            max_value=profile["max_date"]
        )

# 4. Comprehensive dataset profiling
def comprehensive_dataset_profiling(df):
    """Comprehensive profiling of entire dataset"""
    
    dataset_profile = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "memory_usage_mb": df.memory_usage(deep=True).sum() / (1024 * 1024),
        "duplicate_rows": df.duplicated().sum(),
        "columns": {}
    }
    
    # Profile each column
    for column in df.columns:
        dataset_profile["columns"][column] = custom_data_profiling(df, column)
    
    # Data quality summary
    total_cells = len(df) * len(df.columns)
    null_cells = sum(profile["null_count"] for profile in dataset_profile["columns"].values())
    
    dataset_profile["data_quality"] = {
        "completeness_percentage": ((total_cells - null_cells) / total_cells) * 100,
        "duplicate_percentage": (dataset_profile["duplicate_rows"] / len(df)) * 100
    }
    
    return dataset_profile
```

---

## Data Sources & Connectors (51-75)

### 51. How do you integrate Great Expectations with different data sources?
**Answer:**
**Multi-Source Integration:**

```python
# 1. Database integration (PostgreSQL, MySQL, etc.)
def setup_database_datasource():
    """Setup database datasource with connection pooling"""
    
    database_config = {
        "name": "production_db",
        "class_name": "Datasource",
        "execution_engine": {
            "class_name": "SqlAlchemyExecutionEngine",
            "connection_string": "postgresql://user:password@localhost:5432/production",
            "pool_size": 10,
            "max_overflow": 20,
            "pool_pre_ping": True,
            "pool_recycle": 3600
        },
        "data_connectors": {
            "default_runtime_data_connector": {
                "class_name": "RuntimeDataConnector",
                "batch_identifiers": ["default_identifier_name"]
            },
            "default_inferred_data_connector": {
                "class_name": "InferredAssetSqlDataConnector",
                "include_schema_name": True,
                "introspection_directives": {
                    "schema_name": "public"
                }
            }
        }
    }
    
    context.add_datasource(**database_config)
    
    # Test connection
    datasource = context.get_datasource("production_db")
    available_tables = datasource.get_available_data_asset_names()
    print("Available tables:", available_tables)

# 2. Cloud storage integration (S3, GCS, Azure Blob)
def setup_cloud_storage_datasources():
    """Setup cloud storage datasources"""
    
    # S3 configuration
    s3_config = {
        "name": "s3_data_lake",
        "class_name": "Datasource",
        "execution_engine": {
            "class_name": "PandasExecutionEngine"
        },
        "data_connectors": {
            "s3_connector": {
                "class_name": "InferredAssetS3DataConnector",
                "bucket": "my-data-lake-bucket",
                "prefix": "raw-data/",
                "default_regex": {
                    "group_names": ["data_asset_name", "year", "month", "day"],
                    "pattern": r"raw-data/(\w+)/year=(\d{4})/month=(\d{2})/day=(\d{2})/.*\.parquet"
                },
                "sorters": [
                    {
                        "name": "datetime_sorter",
                        "class_name": "DateTimeSorter",
                        "orderby": "desc"
                    }
                ]
            }
        }
    }
    
    # Google Cloud Storage configuration
    gcs_config = {
        "name": "gcs_warehouse",
        "class_name": "Datasource",
        "execution_engine": {
            "class_name": "PandasExecutionEngine"
        },
        "data_connectors": {
            "gcs_connector": {
                "class_name": "InferredAssetGCSDataConnector",
                "bucket_or_name": "my-gcs-bucket",
                "prefix": "warehouse/",
                "default_regex": {
                    "group_names": ["table_name"],
                    "pattern": r"warehouse/(\w+)/.*\.csv"
                }
            }
        }
    }
    
    context.add_datasource(**s3_config)
    context.add_datasource(**gcs_config)

# 3. Spark integration
def setup_spark_datasource():
    """Setup Spark datasource for big data processing"""
    
    from pyspark.sql import SparkSession
    
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("GreatExpectations") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()
    
    spark_config = {
        "name": "spark_datasource",
        "class_name": "Datasource",
        "execution_engine": {
            "class_name": "SparkDFExecutionEngine",
            "spark_config": {
                "spark.sql.adaptive.enabled": "true",
                "spark.sql.adaptive.coalescePartitions.enabled": "true"
            }
        },
        "data_connectors": {
            "default_runtime_data_connector": {
                "class_name": "RuntimeDataConnector",
                "batch_identifiers": ["run_id"]
            },
            "configured_asset_filesystem_data_connector": {
                "class_name": "ConfiguredAssetFilesystemDataConnector",
                "base_directory": "/path/to/spark/data",
                "assets": {
                    "large_dataset": {
                        "group_names": ["year", "month"],
                        "pattern": r"large_dataset/year=(\d{4})/month=(\d{2})/.*\.parquet"
                    }
                }
            }
        }
    }
    
    context.add_datasource(**spark_config)

# 4. API integration
def setup_api_datasource():
    """Setup API datasource for real-time data validation"""
    
    import requests
    import pandas as pd
    
    class APIDataConnector:
        def __init__(self, api_endpoint, headers=None):
            self.api_endpoint = api_endpoint
            self.headers = headers or {}
        
        def fetch_data(self, params=None):
            """Fetch data from API"""
            response = requests.get(
                self.api_endpoint,
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            return pd.DataFrame(response.json())
    
    # Custom runtime data connector for API
    api_connector = APIDataConnector(
        api_endpoint="https://api.example.com/data",
        headers={"Authorization": "Bearer your-token"}
    )
    
    # Fetch and validate API data
    api_data = api_connector.fetch_data(params={"limit": 1000})
    
    batch_request = RuntimeBatchRequest(
        datasource_name="pandas_datasource",
        data_connector_name="default_runtime_data_connector",
        data_asset_name="api_data",
        runtime_parameters={"batch_data": api_data},
        batch_identifiers={"default_identifier_name": "api_batch"}
    )
    
    return batch_request

# 5. Streaming data integration
def setup_streaming_validation():
    """Setup streaming data validation"""
    
    import time
    from datetime import datetime
    
    def validate_streaming_batch(batch_data, batch_id):
        """Validate streaming batch"""
        
        batch_request = RuntimeBatchRequest(
            datasource_name="pandas_datasource",
            data_connector_name="default_runtime_data_connector",
            data_asset_name="streaming_data",
            runtime_parameters={"batch_data": batch_data},
            batch_identifiers={"default_identifier_name": f"stream_batch_{batch_id}"}
        )
        
        validator = context.get_validator(
            batch_request=batch_request,
            expectation_suite_name="streaming_data_suite"
        )
        
        results = validator.validate()
        
        # Log results
        print(f"Batch {batch_id} validation: {'PASSED' if results.success else 'FAILED'}")
        
        if not results.success:
            # Handle validation failures
            failed_expectations = [r for r in results.results if not r.success]
            print(f"Failed expectations: {len(failed_expectations)}")
            
            # Send alerts or take corrective action
            send_validation_alert(batch_id, failed_expectations)
        
        return results
    
    def send_validation_alert(batch_id, failed_expectations):
        """Send alert for validation failures"""
        alert_message = f"Data validation failed for batch {batch_id}\n"
        alert_message += f"Failed expectations: {len(failed_expectations)}\n"
        
        for expectation in failed_expectations:
            alert_message += f"- {expectation.expectation_config.expectation_type}\n"
        
        # Send to monitoring system
        print(f"ALERT: {alert_message}")
    
    return validate_streaming_batch
```

---

## Checkpoints & Automation (76-100)

### 76. How do you create and configure checkpoints for automated validation?
**Answer:**
**Checkpoint Configuration and Automation:**

```python
# 1. Basic checkpoint creation
def create_basic_checkpoint():
    """Create basic checkpoint for automated validation"""
    
    checkpoint_config = {
        "name": "customer_data_checkpoint",
        "config_version": 1.0,
        "template_name": None,
        "module_name": "great_expectations.checkpoint",
        "class_name": "Checkpoint",
        "run_name_template": "%Y%m%d-%H%M%S-customer-data-validation",
        "expectation_suite_name": "customer_data_quality_suite",
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
        ],
        "evaluation_parameters": {},
        "runtime_configuration": {},
        "validations": []
    }
    
    context.add_checkpoint(**checkpoint_config)
    return checkpoint_config

# 2. Advanced checkpoint with multiple validations
def create_advanced_checkpoint():
    """Create advanced checkpoint with multiple data sources"""
    
    checkpoint_config = {
        "name": "comprehensive_data_validation",
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
                "expectation_suite_name": "customer_data_quality_suite"
            },
            {
                "batch_request": {
                    "datasource_name": "production_db",
                    "data_connector_name": "default_inferred_data_connector",
                    "data_asset_name": "orders"
                },
                "expectation_suite_name": "order_data_quality_suite"
            },
            {
                "batch_request": {
                    "datasource_name": "s3_data_lake",
                    "data_connector_name": "s3_connector",
                    "data_asset_name": "user_events"
                },
                "expectation_suite_name": "event_data_quality_suite"
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
                "name": "send_slack_notification",
                "action": {
                    "class_name": "SlackNotificationAction",
                    "slack_webhook": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
                    "notify_on": "failure",
                    "renderer": {
                        "module_name": "great_expectations.render.renderer.slack_renderer",
                        "class_name": "SlackRenderer"
                    }
                }
            }
        ]
    }
    
    context.add_checkpoint(**checkpoint_config)
    return checkpoint_config

# 3. Custom checkpoint actions
class CustomEmailAction:
    """Custom action to send email notifications"""
    
    def __init__(self, smtp_server, smtp_port, username, password, recipients):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.recipients = recipients
    
    def run(self, validation_result_suite, checkpoint_identifier, **kwargs):
        """Send email notification based on validation results"""
        
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        # Analyze results
        total_expectations = len(validation_result_suite.results)
        failed_expectations = sum(1 for r in validation_result_suite.results if not r.success)
        success_rate = ((total_expectations - failed_expectations) / total_expectations) * 100
        
        # Create email content
        subject = f"Data Validation Report - {checkpoint_identifier}"
        
        body = f"""
        Data Validation Summary:
        
        Checkpoint: {checkpoint_identifier}
        Timestamp: {validation_result_suite.meta.get('run_id', {}).get('run_time', 'Unknown')}
        
        Results:
        - Total Expectations: {total_expectations}
        - Passed: {total_expectations - failed_expectations}
        - Failed: {failed_expectations}
        - Success Rate: {success_rate:.2f}%
        
        Status: {'PASSED' if validation_result_suite.success else 'FAILED'}
        """
        
        if failed_expectations > 0:
            body += "\n\nFailed Expectations:\n"
            for result in validation_result_suite.results:
                if not result.success:
                    body += f"- {result.expectation_config.expectation_type}\n"
        
        # Send email
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = ', '.join(self.recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
            server.quit()
            print(f"Email notification sent to {self.recipients}")
        except Exception as e:
            print(f"Failed to send email: {e}")

# 4. Scheduled checkpoint execution
def setup_scheduled_validation():
    """Setup scheduled validation using cron or task scheduler"""
    
    import schedule
    import time
    from datetime import datetime
    
    def run_daily_validation():
        """Run daily data validation"""
        
        print(f"Starting daily validation at {datetime.now()}")
        
        try:
            # Run checkpoint
            results = context.run_checkpoint(
                checkpoint_name="comprehensive_data_validation",
                run_name=f"daily_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            
            # Log results
            if results["success"]:
                print("Daily validation completed successfully")
            else:
                print("Daily validation failed - check data docs for details")
                
        except Exception as e:
            print(f"Daily validation error: {e}")
    
    # Schedule daily validation at 6 AM
    schedule.every().day.at("06:00").do(run_daily_validation)
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)

# 5. CI/CD integration
def create_cicd_checkpoint():
    """Create checkpoint for CI/CD pipeline integration"""
    
    cicd_checkpoint_config = {
        "name": "cicd_data_validation",
        "config_version": 1.0,
        "template_name": None,
        "module_name": "great_expectations.checkpoint",
        "class_name": "Checkpoint",
        "run_name_template": "cicd-validation-%Y%m%d-%H%M%S",
        "validations": [
            {
                "batch_request": {
                    "datasource_name": "test_datasource",
                    "data_connector_name": "default_runtime_data_connector",
                    "data_asset_name": "test_data",
                    "runtime_parameters": {
                        "batch_data": "{{ batch_data }}"  # Parameterized
                    },
                    "batch_identifiers": {
                        "default_identifier_name": "{{ run_id }}"
                    }
                },
                "expectation_suite_name": "{{ expectation_suite_name }}"
            }
        ],
        "action_list": [
            {
                "name": "store_validation_result",
                "action": {
                    "class_name": "StoreValidationResultAction"
                }
            }
        ],
        "runtime_configuration": {
            "result_format": "COMPLETE"
        }
    }
    
    context.add_checkpoint(**cicd_checkpoint_config)
    
    # Example usage in CI/CD script
    def validate_in_pipeline(test_data, suite_name, run_id):
        """Validate data in CI/CD pipeline"""
        
        results = context.run_checkpoint(
            checkpoint_name="cicd_data_validation",
            validations=[
                {
                    "batch_request": {
                        "datasource_name": "test_datasource",
                        "data_connector_name": "default_runtime_data_connector",
                        "data_asset_name": "test_data",
                        "runtime_parameters": {"batch_data": test_data},
                        "batch_identifiers": {"default_identifier_name": run_id}
                    },
                    "expectation_suite_name": suite_name
                }
            ]
        )
        
        # Exit with error code if validation fails
        if not results["success"]:
            print("Data validation failed in CI/CD pipeline")
            exit(1)
        else:
            print("Data validation passed in CI/CD pipeline")
            return results
    
    return validate_in_pipeline
```

This comprehensive Great Expectations interview guide covers essential concepts from basic setup to advanced production scenarios, providing practical examples for data engineering roles.