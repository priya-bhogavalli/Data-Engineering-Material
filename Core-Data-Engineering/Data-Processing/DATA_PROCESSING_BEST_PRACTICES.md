# Data Processing Best Practices for Data Engineering

## 1. Pipeline Design Principles

### Design for Reliability
```python
# Implement circuit breaker pattern
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
            raise e

# Usage in data pipeline
def robust_data_extraction():
    circuit_breaker = CircuitBreaker()
    
    try:
        data = circuit_breaker.call(extract_from_api)
        return data
    except Exception as e:
        # Fallback to cached data or alternative source
        return extract_from_backup_source()
```

### Implement Idempotency
```python
def idempotent_data_processing():
    """Ensure pipeline can be safely re-run without side effects."""
    
    # Use deterministic IDs
    def generate_record_id(record):
        import hashlib
        key_fields = f"{record['customer_id']}_{record['order_date']}_{record['amount']}"
        return hashlib.md5(key_fields.encode()).hexdigest()
    
    # Upsert instead of insert
    def upsert_records(df, target_table):
        df.createOrReplaceTempView("source_data")
        
        spark.sql(f"""
            MERGE INTO {target_table} target
            USING source_data source
            ON target.record_id = source.record_id
            WHEN MATCHED THEN
                UPDATE SET *
            WHEN NOT MATCHED THEN
                INSERT *
        """)
    
    # Use staging tables for atomic operations
    def atomic_table_update(df, target_table):
        staging_table = f"{target_table}_staging_{int(time.time())}"
        
        try:
            # Write to staging
            df.write.mode("overwrite").saveAsTable(staging_table)
            
            # Atomic swap
            spark.sql(f"ALTER TABLE {target_table} RENAME TO {target_table}_old")
            spark.sql(f"ALTER TABLE {staging_table} RENAME TO {target_table}")
            spark.sql(f"DROP TABLE {target_table}_old")
            
        except Exception as e:
            # Cleanup on failure
            spark.sql(f"DROP TABLE IF EXISTS {staging_table}")
            raise e
```

## 2. Performance Optimization

### Spark Optimization Strategies
```python
# Configure Spark for optimal performance
def configure_spark_session():
    return SparkSession.builder \
        .appName("OptimizedDataProcessing") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .config("spark.sql.adaptive.skewJoin.enabled", "true") \
        .config("spark.sql.adaptive.localShuffleReader.enabled", "true") \
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
        .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
        .getOrCreate()

# Optimize data layout
def optimize_data_layout(df, partition_cols, z_order_cols=None):
    """Optimize data layout for query performance."""
    
    # Partition by frequently filtered columns
    df.write \
        .partitionBy(*partition_cols) \
        .mode("overwrite") \
        .option("path", "s3://optimized-data/") \
        .saveAsTable("optimized_table")
    
    # Z-order for Delta tables (if using Delta Lake)
    if z_order_cols:
        spark.sql(f"""
            OPTIMIZE optimized_table
            ZORDER BY ({', '.join(z_order_cols)})
        """)

# Cache strategically
def strategic_caching():
    # Cache frequently accessed datasets
    lookup_data = spark.read.table("lookup_table").cache()
    
    # Use appropriate storage levels
    from pyspark import StorageLevel
    
    # Memory only for small, frequently accessed data
    small_df.persist(StorageLevel.MEMORY_ONLY)
    
    # Memory and disk for larger datasets
    large_df.persist(StorageLevel.MEMORY_AND_DISK_SER)
    
    # Disk only for infrequently accessed but needed data
    archive_df.persist(StorageLevel.DISK_ONLY)
```

### Join Optimization
```python
def optimize_joins():
    """Best practices for join optimization."""
    
    # 1. Broadcast small tables
    large_df = spark.read.table("large_table")
    small_df = spark.read.table("small_table")
    
    # Explicit broadcast
    from pyspark.sql.functions import broadcast
    result = large_df.join(broadcast(small_df), "key")
    
    # 2. Bucketing for repeated joins
    large_df.write \
        .bucketBy(10, "customer_id") \
        .sortBy("customer_id") \
        .saveAsTable("bucketed_large_table")
    
    small_df.write \
        .bucketBy(10, "customer_id") \
        .sortBy("customer_id") \
        .saveAsTable("bucketed_small_table")
    
    # Bucketed join (no shuffle needed)
    bucketed_result = spark.sql("""
        SELECT * FROM bucketed_large_table l
        JOIN bucketed_small_table s ON l.customer_id = s.customer_id
    """)
    
    # 3. Salting for skewed joins
    def salt_skewed_join(large_df, small_df, join_key, salt_factor=10):
        from pyspark.sql.functions import rand, floor, col
        
        # Add salt to both datasets
        salted_large = large_df.withColumn(
            "salt", floor(rand() * salt_factor)
        ).withColumn(
            "salted_key", concat(col(join_key), lit("_"), col("salt"))
        )
        
        # Replicate small dataset
        salt_values = spark.range(salt_factor).select(col("id").alias("salt"))
        salted_small = small_df.crossJoin(salt_values).withColumn(
            "salted_key", concat(col(join_key), lit("_"), col("salt"))
        )
        
        return salted_large.join(salted_small, "salted_key")
```

## 3. Data Quality and Monitoring

### Implement Data Quality Checks
```python
import great_expectations as ge
from pyspark.sql.functions import col, count, when, isnan, isnull

class DataQualityValidator:
    def __init__(self, spark_session):
        self.spark = spark_session
        self.quality_metrics = {}
    
    def validate_completeness(self, df, required_columns):
        """Check for null values in required columns."""
        for column in required_columns:
            null_count = df.filter(col(column).isNull()).count()
            total_count = df.count()
            completeness_rate = (total_count - null_count) / total_count
            
            self.quality_metrics[f"{column}_completeness"] = completeness_rate
            
            if completeness_rate < 0.95:  # 95% threshold
                raise ValueError(f"Column {column} completeness below threshold: {completeness_rate}")
    
    def validate_uniqueness(self, df, unique_columns):
        """Check for duplicate values in unique columns."""
        for column in unique_columns:
            total_count = df.count()
            unique_count = df.select(column).distinct().count()
            uniqueness_rate = unique_count / total_count
            
            self.quality_metrics[f"{column}_uniqueness"] = uniqueness_rate
            
            if uniqueness_rate < 1.0:
                duplicate_count = total_count - unique_count
                raise ValueError(f"Column {column} has {duplicate_count} duplicates")
    
    def validate_data_freshness(self, df, timestamp_column, max_age_hours=24):
        """Check data freshness."""
        from pyspark.sql.functions import current_timestamp, hour
        
        stale_data_count = df.filter(
            hour(current_timestamp() - col(timestamp_column)) > max_age_hours
        ).count()
        
        if stale_data_count > 0:
            raise ValueError(f"Found {stale_data_count} stale records")
    
    def validate_schema_evolution(self, df, expected_schema):
        """Validate schema changes."""
        current_schema = df.schema
        
        # Check for missing columns
        expected_columns = set(field.name for field in expected_schema.fields)
        current_columns = set(field.name for field in current_schema.fields)
        
        missing_columns = expected_columns - current_columns
        if missing_columns:
            raise ValueError(f"Missing columns: {missing_columns}")
        
        # Check for data type changes
        for expected_field in expected_schema.fields:
            current_field = next(
                (f for f in current_schema.fields if f.name == expected_field.name), 
                None
            )
            if current_field and current_field.dataType != expected_field.dataType:
                raise ValueError(
                    f"Data type mismatch for {expected_field.name}: "
                    f"expected {expected_field.dataType}, got {current_field.dataType}"
                )

# Usage in pipeline
def data_pipeline_with_quality_checks():
    validator = DataQualityValidator(spark)
    
    # Extract data
    df = spark.read.table("source_table")
    
    # Validate data quality
    validator.validate_completeness(df, ["customer_id", "order_date", "amount"])
    validator.validate_uniqueness(df, ["order_id"])
    validator.validate_data_freshness(df, "order_date")
    
    # Process data
    processed_df = df.filter(col("amount") > 0) \
        .withColumn("processed_timestamp", current_timestamp())
    
    # Final validation
    validator.validate_completeness(processed_df, ["customer_id", "processed_timestamp"])
    
    return processed_df
```

### Monitoring and Alerting
```python
import logging
from datetime import datetime
import json

class PipelineMonitor:
    def __init__(self, pipeline_name):
        self.pipeline_name = pipeline_name
        self.metrics = {}
        self.logger = self._setup_logging()
    
    def _setup_logging(self):
        logger = logging.getLogger(self.pipeline_name)
        logger.setLevel(logging.INFO)
        
        # JSON formatter for structured logging
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
            '"pipeline": "%(name)s", "message": "%(message)s"}'
        )
        
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def track_execution_time(self, stage_name):
        """Decorator to track execution time."""
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    
                    self.metrics[f"{stage_name}_execution_time"] = execution_time
                    self.logger.info(f"Stage {stage_name} completed in {execution_time:.2f}s")
                    
                    return result
                except Exception as e:
                    execution_time = time.time() - start_time
                    self.logger.error(f"Stage {stage_name} failed after {execution_time:.2f}s: {str(e)}")
                    raise
            return wrapper
        return decorator
    
    def track_data_volume(self, df, stage_name):
        """Track data volume at each stage."""
        row_count = df.count()
        column_count = len(df.columns)
        
        self.metrics[f"{stage_name}_row_count"] = row_count
        self.metrics[f"{stage_name}_column_count"] = column_count
        
        self.logger.info(f"Stage {stage_name}: {row_count} rows, {column_count} columns")
        
        return df
    
    def check_sla_compliance(self, start_time, sla_minutes):
        """Check if pipeline meets SLA."""
        elapsed_minutes = (time.time() - start_time) / 60
        
        if elapsed_minutes > sla_minutes:
            self.logger.warning(f"SLA breach: {elapsed_minutes:.2f}min > {sla_minutes}min")
            self._send_alert("SLA_BREACH", f"Pipeline exceeded SLA by {elapsed_minutes - sla_minutes:.2f} minutes")
        
        return elapsed_minutes <= sla_minutes
    
    def _send_alert(self, alert_type, message):
        """Send alert to monitoring system."""
        alert_payload = {
            "pipeline": self.pipeline_name,
            "alert_type": alert_type,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "metrics": self.metrics
        }
        
        # Send to monitoring system (SNS, Slack, etc.)
        self.logger.error(f"ALERT: {json.dumps(alert_payload)}")

# Usage example
def monitored_pipeline():
    monitor = PipelineMonitor("customer_analytics_pipeline")
    start_time = time.time()
    
    @monitor.track_execution_time("data_extraction")
    def extract_data():
        return spark.read.table("source_table")
    
    @monitor.track_execution_time("data_transformation")
    def transform_data(df):
        return df.filter(col("amount") > 0) \
            .groupBy("customer_id") \
            .agg(sum("amount").alias("total_amount"))
    
    @monitor.track_execution_time("data_loading")
    def load_data(df):
        df.write.mode("overwrite").saveAsTable("customer_summary")
    
    try:
        # Execute pipeline with monitoring
        raw_data = extract_data()
        monitor.track_data_volume(raw_data, "extraction")
        
        processed_data = transform_data(raw_data)
        monitor.track_data_volume(processed_data, "transformation")
        
        load_data(processed_data)
        
        # Check SLA compliance (e.g., 30 minutes)
        monitor.check_sla_compliance(start_time, 30)
        
    except Exception as e:
        monitor._send_alert("PIPELINE_FAILURE", str(e))
        raise
```

## 4. Error Handling and Recovery

### Implement Robust Error Handling
```python
class PipelineErrorHandler:
    def __init__(self, max_retries=3, backoff_factor=2):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
    
    def retry_with_backoff(self, func, *args, **kwargs):
        """Retry function with exponential backoff."""
        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries:
                    raise e
                
                wait_time = self.backoff_factor ** attempt
                time.sleep(wait_time)
                print(f"Attempt {attempt + 1} failed, retrying in {wait_time}s: {str(e)}")
    
    def handle_partial_failures(self, df, processing_func):
        """Handle partial failures in data processing."""
        try:
            return processing_func(df)
        except Exception as e:
            # Log failed records for later reprocessing
            failed_records = df.filter(col("processing_status") == "failed")
            failed_records.write.mode("append").saveAsTable("failed_records_queue")
            
            # Continue with successful records
            successful_records = df.filter(col("processing_status") == "success")
            return processing_func(successful_records)
    
    def implement_dead_letter_queue(self, failed_df, error_info):
        """Store failed records for manual investigation."""
        failed_with_error = failed_df.withColumn(
            "error_info", lit(json.dumps(error_info))
        ).withColumn(
            "failed_timestamp", current_timestamp()
        )
        
        failed_with_error.write \
            .mode("append") \
            .saveAsTable("dead_letter_queue")

# Graceful degradation
def pipeline_with_graceful_degradation():
    """Pipeline that degrades gracefully on failures."""
    
    try:
        # Primary data source
        df = spark.read.table("primary_source")
    except Exception as e:
        print(f"Primary source failed: {e}")
        try:
            # Fallback to secondary source
            df = spark.read.table("secondary_source")
        except Exception as e2:
            print(f"Secondary source failed: {e2}")
            # Use cached data as last resort
            df = spark.read.table("cached_data") \
                .filter(col("cache_date") >= date_sub(current_date(), 1))
    
    return df
```

## 5. Security and Compliance

### Data Security Best Practices
```python
# Encryption at rest and in transit
def secure_data_processing():
    # Configure encryption
    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    spark.conf.set("spark.hadoop.fs.s3a.server-side-encryption-algorithm", "AES256")
    spark.conf.set("spark.hadoop.fs.s3a.encryption.key", "your-kms-key-id")
    
    # Use SSL for data transfer
    spark.conf.set("spark.hadoop.fs.s3a.connection.ssl.enabled", "true")

# Data masking for sensitive information
def mask_sensitive_data(df):
    """Mask PII data for non-production environments."""
    from pyspark.sql.functions import regexp_replace, sha2
    
    masked_df = df \
        .withColumn("email", 
            regexp_replace(col("email"), r"(.{2}).*(@.*)", r"$1***$2")) \
        .withColumn("phone", 
            regexp_replace(col("phone"), r"(\d{3})\d{3}(\d{4})", r"$1***$2")) \
        .withColumn("ssn_hash", 
            sha2(col("ssn"), 256)) \
        .drop("ssn")
    
    return masked_df

# Access control and audit logging
class DataAccessController:
    def __init__(self):
        self.access_log = []
    
    def check_access_permissions(self, user, table_name, operation):
        """Check if user has permission for operation."""
        # Implement role-based access control
        user_roles = self.get_user_roles(user)
        table_permissions = self.get_table_permissions(table_name)
        
        has_permission = any(
            role in table_permissions.get(operation, [])
            for role in user_roles
        )
        
        # Log access attempt
        self.access_log.append({
            "user": user,
            "table": table_name,
            "operation": operation,
            "granted": has_permission,
            "timestamp": datetime.now().isoformat()
        })
        
        return has_permission
    
    def audit_data_access(self, df, user, operation):
        """Audit data access for compliance."""
        row_count = df.count()
        
        audit_record = {
            "user": user,
            "operation": operation,
            "row_count": row_count,
            "timestamp": datetime.now().isoformat(),
            "data_classification": self.classify_data_sensitivity(df)
        }
        
        # Store audit record
        spark.createDataFrame([audit_record]).write \
            .mode("append") \
            .saveAsTable("data_access_audit")
```

## 6. Testing and Validation

### Unit Testing for Data Pipelines
```python
import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

class TestDataPipeline:
    @pytest.fixture(scope="class")
    def spark(self):
        return SparkSession.builder \
            .appName("TestDataPipeline") \
            .master("local[2]") \
            .getOrCreate()
    
    def test_data_transformation(self, spark):
        # Create test data
        schema = StructType([
            StructField("customer_id", StringType(), True),
            StructField("amount", IntegerType(), True),
            StructField("status", StringType(), True)
        ])
        
        test_data = [
            ("C001", 100, "active"),
            ("C002", -50, "inactive"),
            ("C003", 200, "active")
        ]
        
        df = spark.createDataFrame(test_data, schema)
        
        # Apply transformation
        result = df.filter(col("amount") > 0) \
            .filter(col("status") == "active")
        
        # Assertions
        assert result.count() == 2
        assert result.filter(col("customer_id") == "C001").count() == 1
        assert result.filter(col("customer_id") == "C002").count() == 0
    
    def test_data_quality_validation(self, spark):
        # Test data quality checks
        validator = DataQualityValidator(spark)
        
        # Create test data with quality issues
        bad_data = spark.createDataFrame([
            ("C001", None, "active"),  # Missing amount
            ("C002", 100, "active"),
            ("C002", 150, "active")    # Duplicate customer_id
        ], ["customer_id", "amount", "status"])
        
        # Test completeness validation
        with pytest.raises(ValueError, match="completeness below threshold"):
            validator.validate_completeness(bad_data, ["amount"])
        
        # Test uniqueness validation
        with pytest.raises(ValueError, match="duplicates"):
            validator.validate_uniqueness(bad_data, ["customer_id"])

# Integration testing
def test_end_to_end_pipeline():
    """Test complete pipeline with sample data."""
    
    # Setup test environment
    test_spark = SparkSession.builder.appName("IntegrationTest").getOrCreate()
    
    # Create test input data
    test_input = test_spark.createDataFrame([
        ("C001", "2024-01-01", 100),
        ("C002", "2024-01-02", 200),
        ("C003", "2024-01-03", 150)
    ], ["customer_id", "order_date", "amount"])
    
    # Run pipeline
    result = run_customer_analytics_pipeline(test_input)
    
    # Validate results
    assert result.count() > 0
    assert "total_amount" in result.columns
    assert result.filter(col("total_amount") < 0).count() == 0
    
    # Cleanup
    test_spark.stop()
```

These best practices ensure robust, performant, and maintainable data processing pipelines that can handle enterprise-scale requirements while maintaining data quality and security standards.