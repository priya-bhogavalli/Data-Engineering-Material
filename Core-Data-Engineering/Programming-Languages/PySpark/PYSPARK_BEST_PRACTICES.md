# PySpark Best Practices for Data Engineering

## 1. Performance Optimization

### DataFrame Operations
```python
# Use DataFrame API over RDD API
# Good: DataFrame operations are optimized by Catalyst
df.filter(col("age") > 25).select("name", "age")

# Avoid: RDD operations bypass Catalyst optimizer
rdd.filter(lambda x: x.age > 25).map(lambda x: (x.name, x.age))

# Cache frequently accessed DataFrames
df.cache()  # or df.persist(StorageLevel.MEMORY_AND_DISK)

# Use broadcast joins for small tables
broadcast_df = broadcast(small_df)
result = large_df.join(broadcast_df, "key")
```

### Column Operations
```python
from pyspark.sql.functions import col, when, lit

# Use column expressions instead of UDFs when possible
df.withColumn("category", 
    when(col("amount") > 1000, "high")
    .when(col("amount") > 100, "medium")
    .otherwise("low"))

# Avoid collecting large datasets
# Bad: df.collect()  # Brings all data to driver
# Good: df.limit(100).collect()  # Only collect what you need
```

### Partitioning Strategy
```python
# Partition by frequently filtered columns
df.write.partitionBy("year", "month").parquet("path")

# Optimal partition size: 128MB - 1GB per partition
# Check partition count
print(f"Number of partitions: {df.rdd.getNumPartitions()}")

# Repartition for better distribution
df = df.repartition(200, "customer_id")

# Use coalesce to reduce partitions without shuffle
df = df.coalesce(50)
```

## 2. Memory Management

### Storage Levels
```python
from pyspark import StorageLevel

# Choose appropriate storage level
df.persist(StorageLevel.MEMORY_ONLY)  # Fast access, memory only
df.persist(StorageLevel.MEMORY_AND_DISK)  # Spill to disk if needed
df.persist(StorageLevel.DISK_ONLY)  # Disk storage only

# Unpersist when no longer needed
df.unpersist()
```

### Memory Configuration
```python
# Spark configuration for memory optimization
spark = SparkSession.builder \
    .appName("DataProcessing") \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.cores", "4") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .getOrCreate()
```

## 3. Data Quality and Validation

### Schema Enforcement
```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Define explicit schemas
schema = StructType([
    StructField("id", IntegerType(), False),
    StructField("name", StringType(), False),
    StructField("email", StringType(), True)
])

# Read with schema enforcement
df = spark.read.schema(schema).csv("data.csv", header=True)

# Validate data quality
def validate_data_quality(df):
    total_rows = df.count()
    null_counts = df.select([
        sum(col(c).isNull().cast("int")).alias(c) 
        for c in df.columns
    ]).collect()[0].asDict()
    
    return {
        "total_rows": total_rows,
        "null_counts": null_counts,
        "completeness": {k: 1 - (v/total_rows) for k, v in null_counts.items()}
    }
```

### Data Profiling
```python
def profile_dataframe(df):
    """Generate comprehensive data profile"""
    profile = {}
    
    # Basic statistics
    profile['row_count'] = df.count()
    profile['column_count'] = len(df.columns)
    
    # Column statistics
    numeric_cols = [f.name for f in df.schema.fields 
                   if f.dataType.typeName() in ['integer', 'double', 'float']]
    
    if numeric_cols:
        profile['numeric_stats'] = df.select(numeric_cols).describe().collect()
    
    # Null analysis
    profile['null_counts'] = df.select([
        sum(col(c).isNull().cast("int")).alias(c) 
        for c in df.columns
    ]).collect()[0].asDict()
    
    return profile
```

## 4. Error Handling and Logging

### Robust Error Handling
```python
import logging
from pyspark.sql.utils import AnalysisException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_read_data(spark, file_path, file_format="parquet"):
    """Safely read data with error handling"""
    try:
        if file_format == "parquet":
            df = spark.read.parquet(file_path)
        elif file_format == "csv":
            df = spark.read.option("header", "true").csv(file_path)
        else:
            raise ValueError(f"Unsupported format: {file_format}")
        
        logger.info(f"Successfully read {df.count()} rows from {file_path}")
        return df
        
    except AnalysisException as e:
        logger.error(f"Analysis error reading {file_path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error reading {file_path}: {e}")
        raise

def safe_write_data(df, output_path, mode="overwrite"):
    """Safely write data with validation"""
    try:
        # Validate DataFrame before writing
        if df.count() == 0:
            logger.warning("DataFrame is empty, skipping write")
            return False
        
        df.write.mode(mode).parquet(output_path)
        logger.info(f"Successfully wrote data to {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error writing to {output_path}: {e}")
        raise
```

### Data Validation Functions
```python
def validate_required_columns(df, required_columns):
    """Validate that required columns exist"""
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

def validate_data_types(df, expected_types):
    """Validate column data types"""
    for col_name, expected_type in expected_types.items():
        actual_type = dict(df.dtypes)[col_name]
        if actual_type != expected_type:
            raise ValueError(f"Column {col_name}: expected {expected_type}, got {actual_type}")
```

## 5. Code Organization and Modularity

### Reusable Transformation Functions
```python
from pyspark.sql.functions import col, when, regexp_replace, trim, upper

def clean_string_columns(df, columns):
    """Clean string columns by trimming and standardizing case"""
    for column in columns:
        df = df.withColumn(column, trim(upper(col(column))))
    return df

def standardize_phone_numbers(df, phone_column):
    """Standardize phone number format"""
    return df.withColumn(
        phone_column,
        regexp_replace(col(phone_column), r'[^\d]', '')
    )

def add_derived_columns(df):
    """Add commonly used derived columns"""
    return df.withColumn(
        "age_group",
        when(col("age") < 18, "minor")
        .when(col("age") < 65, "adult")
        .otherwise("senior")
    ).withColumn(
        "is_weekend",
        col("day_of_week").isin([1, 7])  # Sunday=1, Saturday=7
    )
```

### Configuration Management
```python
class SparkConfig:
    """Centralized Spark configuration management"""
    
    @staticmethod
    def get_spark_session(app_name, config_overrides=None):
        builder = SparkSession.builder.appName(app_name)
        
        # Default configurations
        default_configs = {
            "spark.sql.adaptive.enabled": "true",
            "spark.sql.adaptive.coalescePartitions.enabled": "true",
            "spark.sql.execution.arrow.pyspark.enabled": "true",
            "spark.serializer": "org.apache.spark.serializer.KryoSerializer"
        }
        
        # Apply configurations
        configs = {**default_configs, **(config_overrides or {})}
        for key, value in configs.items():
            builder = builder.config(key, value)
        
        return builder.getOrCreate()
```

## 6. Testing Strategies

### Unit Testing DataFrames
```python
import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder \
        .appName("test") \
        .master("local[2]") \
        .getOrCreate()

def test_data_transformation(spark):
    # Create test data
    schema = StructType([
        StructField("name", StringType(), True),
        StructField("age", IntegerType(), True)
    ])
    
    test_data = [("John", 25), ("Jane", 30), ("Bob", 35)]
    df = spark.createDataFrame(test_data, schema)
    
    # Apply transformation
    result = add_age_group(df)
    
    # Verify results
    assert result.count() == 3
    assert "age_group" in result.columns
    
    age_groups = result.select("age_group").distinct().collect()
    assert len(age_groups) == 1  # All should be "adult"

def assert_dataframes_equal(df1, df2):
    """Compare two DataFrames for equality"""
    assert df1.count() == df2.count()
    assert df1.columns == df2.columns
    assert df1.subtract(df2).count() == 0
    assert df2.subtract(df1).count() == 0
```

### Integration Testing
```python
def test_end_to_end_pipeline(spark, tmp_path):
    # Setup test data
    input_path = str(tmp_path / "input")
    output_path = str(tmp_path / "output")
    
    # Create test input
    test_df = spark.createDataFrame([
        ("John", 25, "john@email.com"),
        ("Jane", 30, "jane@email.com")
    ], ["name", "age", "email"])
    
    test_df.write.parquet(input_path)
    
    # Run pipeline
    result = run_data_pipeline(spark, input_path, output_path)
    
    # Verify output
    output_df = spark.read.parquet(output_path)
    assert output_df.count() == 2
    assert "processed_date" in output_df.columns
```

## 7. Monitoring and Observability

### Performance Monitoring
```python
import time
from functools import wraps

def monitor_performance(func):
    """Decorator to monitor function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.info(f"Starting {func.__name__}")
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} completed in {execution_time:.2f} seconds")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.2f} seconds: {e}")
            raise
    
    return wrapper

@monitor_performance
def process_large_dataset(df):
    return df.groupBy("category").agg(
        count("*").alias("count"),
        avg("amount").alias("avg_amount")
    )
```

### Data Lineage Tracking
```python
class DataLineageTracker:
    """Track data transformations for lineage"""
    
    def __init__(self):
        self.transformations = []
    
    def log_transformation(self, operation, input_count, output_count, columns_added=None, columns_removed=None):
        self.transformations.append({
            "operation": operation,
            "timestamp": time.time(),
            "input_count": input_count,
            "output_count": output_count,
            "columns_added": columns_added or [],
            "columns_removed": columns_removed or []
        })
    
    def get_lineage_summary(self):
        return {
            "total_transformations": len(self.transformations),
            "transformations": self.transformations
        }
```

## 8. Security Best Practices

### Data Masking and Encryption
```python
from pyspark.sql.functions import sha2, regexp_replace

def mask_sensitive_data(df, sensitive_columns):
    """Mask sensitive data columns"""
    for column in sensitive_columns:
        if column in df.columns:
            df = df.withColumn(
                column,
                sha2(col(column).cast("string"), 256)
            )
    return df

def mask_pii_data(df):
    """Mask personally identifiable information"""
    return df.withColumn(
        "email",
        regexp_replace(col("email"), r"(.{2}).*(@.*)", r"$1***$2")
    ).withColumn(
        "phone",
        regexp_replace(col("phone"), r"(\d{3})\d{3}(\d{4})", r"$1***$2")
    )
```

### Access Control
```python
def validate_user_permissions(user_id, required_permissions):
    """Validate user has required permissions"""
    # Implementation would check against permission system
    pass

def audit_data_access(user_id, table_name, operation):
    """Log data access for audit purposes"""
    logger.info(f"User {user_id} performed {operation} on {table_name}")
```

## 9. Resource Management

### Dynamic Resource Allocation
```python
# Configure dynamic allocation
spark_config = {
    "spark.dynamicAllocation.enabled": "true",
    "spark.dynamicAllocation.minExecutors": "1",
    "spark.dynamicAllocation.maxExecutors": "20",
    "spark.dynamicAllocation.initialExecutors": "5"
}

def optimize_for_workload(df, workload_type):
    """Optimize Spark configuration based on workload"""
    if workload_type == "cpu_intensive":
        return df.repartition(spark.sparkContext.defaultParallelism * 2)
    elif workload_type == "io_intensive":
        return df.coalesce(spark.sparkContext.defaultParallelism // 2)
    else:
        return df
```

### Memory Optimization
```python
def optimize_memory_usage(spark):
    """Configure Spark for optimal memory usage"""
    spark.conf.set("spark.sql.adaptive.enabled", "true")
    spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
    spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
    spark.conf.set("spark.sql.execution.arrow.maxRecordsPerBatch", "10000")
```

## 10. Deployment and CI/CD

### Environment Configuration
```python
import os
from enum import Enum

class Environment(Enum):
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"

def get_environment_config(env: Environment):
    """Get environment-specific configuration"""
    configs = {
        Environment.DEV: {
            "spark.executor.instances": "2",
            "spark.executor.memory": "2g",
            "spark.executor.cores": "2"
        },
        Environment.STAGING: {
            "spark.executor.instances": "5",
            "spark.executor.memory": "4g",
            "spark.executor.cores": "4"
        },
        Environment.PROD: {
            "spark.executor.instances": "10",
            "spark.executor.memory": "8g",
            "spark.executor.cores": "4"
        }
    }
    return configs[env]
```

### Application Packaging
```python
# setup.py for PySpark application
from setuptools import setup, find_packages

setup(
    name="data-pipeline",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pyspark>=3.0.0",
        "pytest>=6.0.0",
        "pyyaml>=5.4.0"
    ],
    entry_points={
        "console_scripts": [
            "run-pipeline=pipeline.main:main"
        ]
    }
)
```