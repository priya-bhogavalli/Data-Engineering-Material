# Data Processing Interview Questions for Data Engineering

## Basic Level Questions (0-2 years experience)

### 1. What is the difference between batch processing and stream processing?

**Answer:**
- **Batch Processing**: Processes large volumes of data at scheduled intervals
  - Data is collected over time and processed as a complete dataset
  - Higher latency but better for complex analytics
  - Examples: Daily ETL jobs, monthly reports
  - Tools: Apache Spark (batch mode), Hadoop MapReduce

- **Stream Processing**: Processes data in real-time as it arrives
  - Data is processed record-by-record or in small micro-batches
  - Lower latency but limited complexity
  - Examples: Real-time alerts, live dashboards
  - Tools: Apache Kafka Streams, Apache Flink, Spark Streaming

**Code Example:**
```python
# Batch Processing Example
def batch_process_orders(date):
    orders = spark.read.parquet(f"s3://orders/{date}/*.parquet")
    daily_summary = orders.groupBy("customer_id").agg(
        sum("amount").alias("total_amount"),
        count("*").alias("order_count")
    )
    daily_summary.write.mode("overwrite").parquet(f"s3://summaries/{date}/")

# Stream Processing Example
def stream_process_orders():
    orders_stream = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "orders") \
        .load()
    
    processed = orders_stream.select(
        col("value").cast("string").alias("order_data")
    ).writeStream \
        .outputMode("append") \
        .format("console") \
        .start()
```

### 2. What is ETL vs ELT? When would you use each?

**Answer:**
- **ETL (Extract, Transform, Load)**:
  - Transform data before loading into target system
  - Better for data quality and compliance
  - Suitable for structured data and predefined transformations
  - Traditional data warehousing approach

- **ELT (Extract, Load, Transform)**:
  - Load raw data first, then transform in target system
  - Leverages target system's processing power
  - Better for big data and cloud environments
  - More flexible for ad-hoc analysis

**When to use:**
- **ETL**: Sensitive data requiring cleaning, legacy systems, limited target storage
- **ELT**: Cloud data warehouses, big data scenarios, need for raw data access

```python
# ETL Example
def etl_pipeline():
    # Extract
    raw_data = extract_from_source()
    
    # Transform
    cleaned_data = raw_data.filter(col("amount") > 0) \
        .withColumn("processed_date", current_timestamp()) \
        .dropDuplicates(["order_id"])
    
    # Load
    cleaned_data.write.mode("append").saveAsTable("clean_orders")

# ELT Example
def elt_pipeline():
    # Extract & Load
    raw_data = extract_from_source()
    raw_data.write.mode("append").saveAsTable("raw_orders")
    
    # Transform (in target system)
    spark.sql("""
        CREATE OR REPLACE TABLE clean_orders AS
        SELECT DISTINCT order_id, customer_id, amount, order_date
        FROM raw_orders 
        WHERE amount > 0 AND order_date >= current_date() - 30
    """)
```

### 3. What is data partitioning and why is it important?

**Answer:**
Data partitioning divides large datasets into smaller, manageable pieces based on specific criteria.

**Benefits:**
- Improved query performance (partition pruning)
- Parallel processing capabilities
- Better data organization and management
- Reduced I/O operations

**Types:**
- **Horizontal Partitioning**: Split by rows (e.g., by date, region)
- **Vertical Partitioning**: Split by columns
- **Hash Partitioning**: Distribute based on hash function
- **Range Partitioning**: Split by value ranges

```python
# Partitioning Examples
# Write partitioned data
df.write \
    .partitionBy("year", "month") \
    .mode("overwrite") \
    .parquet("s3://data/orders/")

# Read with partition pruning
orders_2024 = spark.read.parquet("s3://data/orders/") \
    .filter(col("year") == 2024)

# Dynamic partitioning
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
```

## Intermediate Level Questions (2-5 years experience)

### 4. Explain Apache Spark's execution model and optimization techniques.

**Answer:**
**Spark Execution Model:**
- **Driver Program**: Coordinates the application
- **Cluster Manager**: Allocates resources
- **Executors**: Run tasks and store data
- **Tasks**: Units of work sent to executors

**Key Concepts:**
- **RDD (Resilient Distributed Dataset)**: Immutable distributed collections
- **DAG (Directed Acyclic Graph)**: Execution plan optimization
- **Lazy Evaluation**: Transformations are not executed until an action is called

**Optimization Techniques:**
```python
# 1. Caching frequently used datasets
df_customers = spark.read.parquet("customers.parquet")
df_customers.cache()  # or .persist(StorageLevel.MEMORY_AND_DISK)

# 2. Broadcast small datasets
broadcast_lookup = spark.sparkContext.broadcast(lookup_dict)
df.map(lambda x: enrich_with_lookup(x, broadcast_lookup.value))

# 3. Proper partitioning
df.repartition(200, "customer_id")  # Distribute evenly
df.coalesce(10)  # Reduce partitions without shuffle

# 4. Predicate pushdown
df.filter(col("date") >= "2024-01-01") \
  .select("customer_id", "amount")  # Filter before select

# 5. Column pruning and projection
df.select("customer_id", "order_date", "amount")  # Only needed columns

# 6. Join optimization
large_df.join(broadcast(small_df), "customer_id")  # Broadcast join
```

### 5. How do you handle slowly changing dimensions (SCD) in data pipelines?

**Answer:**
SCDs track changes in dimension data over time. Different types handle changes differently:

**SCD Type 1 (Overwrite):**
```python
def scd_type1_update(new_data, existing_table):
    # Simply overwrite existing records
    new_data.write \
        .mode("overwrite") \
        .option("mergeSchema", "true") \
        .saveAsTable(existing_table)
```

**SCD Type 2 (Historical Tracking):**
```python
from delta.tables import DeltaTable
from pyspark.sql.functions import current_timestamp, lit

def scd_type2_update(new_data, delta_table_path):
    # Add metadata columns
    new_data_with_meta = new_data \
        .withColumn("effective_date", current_timestamp()) \
        .withColumn("expiration_date", lit(None).cast("timestamp")) \
        .withColumn("is_current", lit(True))
    
    delta_table = DeltaTable.forPath(spark, delta_table_path)
    
    # Merge logic for SCD Type 2
    delta_table.alias("existing") \
        .merge(
            new_data_with_meta.alias("new"),
            "existing.customer_id = new.customer_id AND existing.is_current = true"
        ) \
        .whenMatchedUpdate(
            condition="existing.name != new.name OR existing.email != new.email",
            set={
                "expiration_date": current_timestamp(),
                "is_current": lit(False)
            }
        ) \
        .whenNotMatchedInsert(
            values={
                "customer_id": "new.customer_id",
                "name": "new.name",
                "email": "new.email",
                "effective_date": "new.effective_date",
                "expiration_date": "new.expiration_date",
                "is_current": "new.is_current"
            }
        ) \
        .execute()
```

### 6. What are the key considerations for designing a real-time streaming pipeline?

**Answer:**
**Key Considerations:**

1. **Latency Requirements**: End-to-end processing time
2. **Throughput**: Messages per second capacity
3. **Fault Tolerance**: Handling failures and recovery
4. **Exactly-Once Processing**: Avoiding duplicates
5. **Backpressure Handling**: Managing slow consumers
6. **State Management**: Maintaining processing state
7. **Schema Evolution**: Handling data format changes

**Implementation Example:**
```python
# Kafka Streaming Pipeline
def create_streaming_pipeline():
    # Configure for exactly-once processing
    spark.conf.set("spark.sql.streaming.checkpointLocation", "/checkpoints/")
    spark.conf.set("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true")
    
    # Read from Kafka
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "orders") \
        .option("startingOffsets", "latest") \
        .option("failOnDataLoss", "false") \
        .load()
    
    # Parse and process
    parsed_df = df.select(
        from_json(col("value").cast("string"), order_schema).alias("order")
    ).select("order.*")
    
    # Windowed aggregations
    windowed_df = parsed_df \
        .withWatermark("order_timestamp", "10 minutes") \
        .groupBy(
            window(col("order_timestamp"), "5 minutes"),
            col("customer_id")
        ) \
        .agg(
            sum("amount").alias("total_amount"),
            count("*").alias("order_count")
        )
    
    # Write with fault tolerance
    query = windowed_df.writeStream \
        .outputMode("update") \
        .format("delta") \
        .option("checkpointLocation", "/checkpoints/orders") \
        .option("path", "/delta/aggregated_orders") \
        .trigger(processingTime="30 seconds") \
        .start()
    
    return query
```

## Advanced Level Questions (5+ years experience)

### 7. How would you design a multi-tenant data processing platform?

**Answer:**
**Key Design Considerations:**

1. **Isolation**: Data, compute, and network separation
2. **Resource Management**: Fair resource allocation
3. **Security**: Authentication, authorization, encryption
4. **Scalability**: Handle varying tenant loads
5. **Monitoring**: Per-tenant metrics and alerting
6. **Cost Attribution**: Track usage per tenant

**Architecture Design:**
```python
class MultiTenantDataPlatform:
    def __init__(self):
        self.tenant_configs = {}
        self.resource_manager = ResourceManager()
        self.security_manager = SecurityManager()
    
    def register_tenant(self, tenant_id, config):
        """Register new tenant with configuration."""
        self.tenant_configs[tenant_id] = {
            'resource_limits': config.get('resource_limits'),
            'data_location': f"s3://data-platform/{tenant_id}/",
            'processing_queue': f"tenant-{tenant_id}-queue",
            'security_policies': config.get('security_policies')
        }
    
    def create_tenant_session(self, tenant_id, user_context):
        """Create isolated Spark session for tenant."""
        tenant_config = self.tenant_configs[tenant_id]
        
        spark_config = {
            'spark.sql.warehouse.dir': tenant_config['data_location'],
            'spark.kubernetes.namespace': f"tenant-{tenant_id}",
            'spark.executor.memory': tenant_config['resource_limits']['memory'],
            'spark.executor.cores': tenant_config['resource_limits']['cores'],
            'spark.sql.adaptive.enabled': 'true',
            'spark.sql.adaptive.coalescePartitions.enabled': 'true'
        }
        
        # Apply security context
        spark_config.update(
            self.security_manager.get_security_config(tenant_id, user_context)
        )
        
        return SparkSession.builder.config(map=spark_config).getOrCreate()
    
    def submit_job(self, tenant_id, job_definition):
        """Submit job with tenant isolation."""
        # Validate tenant permissions
        if not self.security_manager.can_submit_job(tenant_id, job_definition):
            raise PermissionError(f"Tenant {tenant_id} not authorized")
        
        # Apply resource limits
        job_definition = self.resource_manager.apply_limits(
            tenant_id, job_definition
        )
        
        # Submit to tenant-specific queue
        return self.job_scheduler.submit(
            queue=self.tenant_configs[tenant_id]['processing_queue'],
            job=job_definition
        )

# Tenant-specific data access patterns
def create_tenant_data_access_layer(tenant_id):
    """Create data access layer with tenant isolation."""
    
    class TenantDataAccess:
        def __init__(self, tenant_id):
            self.tenant_id = tenant_id
            self.base_path = f"s3://data-platform/{tenant_id}/"
        
        def read_table(self, table_name):
            # Automatic tenant path resolution
            table_path = f"{self.base_path}tables/{table_name}/"
            return spark.read.format("delta").load(table_path)
        
        def write_table(self, df, table_name, mode="append"):
            # Enforce tenant data location
            table_path = f"{self.base_path}tables/{table_name}/"
            df.write.format("delta").mode(mode).save(table_path)
        
        def create_view(self, view_name, sql_query):
            # Tenant-scoped view creation
            spark.sql(f"""
                CREATE OR REPLACE VIEW {self.tenant_id}.{view_name} AS
                {sql_query}
            """)
    
    return TenantDataAccess(tenant_id)
```

### 8. How do you implement data lineage tracking in complex data pipelines?

**Answer:**
**Data Lineage Components:**

1. **Schema Lineage**: Track column-level transformations
2. **Process Lineage**: Track job dependencies and execution
3. **Data Lineage**: Track data flow between systems
4. **Impact Analysis**: Understand downstream effects

**Implementation:**
```python
import json
from datetime import datetime
from typing import Dict, List, Optional

class DataLineageTracker:
    def __init__(self, lineage_store):
        self.lineage_store = lineage_store
        self.current_job_id = None
        self.lineage_graph = {}
    
    def start_job(self, job_name: str, job_config: Dict):
        """Initialize lineage tracking for a job."""
        self.current_job_id = f"{job_name}_{datetime.now().isoformat()}"
        
        job_metadata = {
            'job_id': self.current_job_id,
            'job_name': job_name,
            'start_time': datetime.now().isoformat(),
            'config': job_config,
            'inputs': [],
            'outputs': [],
            'transformations': []
        }
        
        self.lineage_store.store_job_metadata(self.current_job_id, job_metadata)
        return self.current_job_id
    
    def track_input(self, dataset_path: str, schema: Dict, 
                   partition_info: Optional[Dict] = None):
        """Track input dataset."""
        input_metadata = {
            'dataset_path': dataset_path,
            'schema': schema,
            'partition_info': partition_info,
            'access_time': datetime.now().isoformat(),
            'row_count': self._get_row_count(dataset_path)
        }
        
        self.lineage_store.add_job_input(self.current_job_id, input_metadata)
    
    def track_transformation(self, transformation_type: str, 
                           transformation_logic: str,
                           input_columns: List[str],
                           output_columns: List[str]):
        """Track data transformation."""
        transformation_metadata = {
            'type': transformation_type,
            'logic': transformation_logic,
            'input_columns': input_columns,
            'output_columns': output_columns,
            'timestamp': datetime.now().isoformat()
        }
        
        self.lineage_store.add_transformation(
            self.current_job_id, transformation_metadata
        )
    
    def track_output(self, dataset_path: str, schema: Dict,
                    partition_info: Optional[Dict] = None):
        """Track output dataset."""
        output_metadata = {
            'dataset_path': dataset_path,
            'schema': schema,
            'partition_info': partition_info,
            'write_time': datetime.now().isoformat(),
            'row_count': self._get_row_count(dataset_path)
        }
        
        self.lineage_store.add_job_output(self.current_job_id, output_metadata)

# Spark DataFrame with lineage tracking
class LineageAwareDataFrame:
    def __init__(self, df, lineage_tracker, dataset_path=None):
        self.df = df
        self.lineage_tracker = lineage_tracker
        self.dataset_path = dataset_path
        
        if dataset_path:
            self.lineage_tracker.track_input(
                dataset_path, 
                self._get_schema_dict(),
                self._get_partition_info()
            )
    
    def select(self, *cols):
        """Select with lineage tracking."""
        result_df = self.df.select(*cols)
        
        self.lineage_tracker.track_transformation(
            transformation_type="select",
            transformation_logic=f"SELECT {', '.join(map(str, cols))}",
            input_columns=self.df.columns,
            output_columns=result_df.columns
        )
        
        return LineageAwareDataFrame(result_df, self.lineage_tracker)
    
    def filter(self, condition):
        """Filter with lineage tracking."""
        result_df = self.df.filter(condition)
        
        self.lineage_tracker.track_transformation(
            transformation_type="filter",
            transformation_logic=f"WHERE {str(condition)}",
            input_columns=self.df.columns,
            output_columns=result_df.columns
        )
        
        return LineageAwareDataFrame(result_df, self.lineage_tracker)
    
    def join(self, other, on, how="inner"):
        """Join with lineage tracking."""
        result_df = self.df.join(other.df, on, how)
        
        self.lineage_tracker.track_transformation(
            transformation_type="join",
            transformation_logic=f"{how.upper()} JOIN ON {str(on)}",
            input_columns=self.df.columns + other.df.columns,
            output_columns=result_df.columns
        )
        
        return LineageAwareDataFrame(result_df, self.lineage_tracker)
    
    def write_to(self, output_path, format="parquet", mode="overwrite"):
        """Write with lineage tracking."""
        self.df.write.format(format).mode(mode).save(output_path)
        
        self.lineage_tracker.track_output(
            output_path,
            self._get_schema_dict(),
            self._get_partition_info()
        )

# Usage example
def lineage_aware_etl():
    lineage_tracker = DataLineageTracker(lineage_store)
    job_id = lineage_tracker.start_job("customer_analytics", {})
    
    # Read with lineage
    customers = LineageAwareDataFrame(
        spark.read.parquet("s3://raw/customers/"),
        lineage_tracker,
        "s3://raw/customers/"
    )
    
    orders = LineageAwareDataFrame(
        spark.read.parquet("s3://raw/orders/"),
        lineage_tracker,
        "s3://raw/orders/"
    )
    
    # Transform with automatic lineage tracking
    result = customers \
        .select("customer_id", "name", "email") \
        .join(orders, "customer_id") \
        .filter(col("order_date") >= "2024-01-01") \
        .groupBy("customer_id", "name") \
        .agg(sum("amount").alias("total_spent"))
    
    # Write with lineage
    result.write_to("s3://processed/customer_analytics/")
```

### 9. How do you implement exactly-once processing in distributed streaming systems?

**Answer:**
**Exactly-Once Processing Challenges:**
- Network failures and retries
- Duplicate message delivery
- Partial failures in distributed systems
- State consistency across restarts

**Implementation Strategies:**

**1. Idempotent Operations:**
```python
def idempotent_upsert(record):
    """Upsert operation that produces same result regardless of retries."""
    # Use natural keys or generate deterministic IDs
    record_id = generate_deterministic_id(record)
    
    # Upsert with conflict resolution
    spark.sql(f"""
        MERGE INTO target_table t
        USING (SELECT * FROM VALUES {record_values}) s(id, data, timestamp)
        ON t.id = s.id
        WHEN MATCHED AND s.timestamp > t.timestamp THEN
            UPDATE SET data = s.data, timestamp = s.timestamp
        WHEN NOT MATCHED THEN
            INSERT (id, data, timestamp) VALUES (s.id, s.data, s.timestamp)
    """)

def generate_deterministic_id(record):
    """Generate deterministic ID from record content."""
    import hashlib
    content = f"{record['customer_id']}_{record['order_date']}_{record['amount']}"
    return hashlib.md5(content.encode()).hexdigest()
```

**2. Transactional Writes with Checkpointing:**
```python
class ExactlyOnceProcessor:
    def __init__(self, checkpoint_location, output_location):
        self.checkpoint_location = checkpoint_location
        self.output_location = output_location
        self.processed_offsets = {}
    
    def process_batch(self, batch_df, batch_id):
        """Process batch with exactly-once guarantees."""
        try:
            # Check if batch already processed
            if self._is_batch_processed(batch_id):
                print(f"Batch {batch_id} already processed, skipping")
                return
            
            # Process data
            processed_df = self._transform_data(batch_df)
            
            # Atomic write operation
            self._atomic_write(processed_df, batch_id)
            
            # Mark batch as processed
            self._mark_batch_processed(batch_id)
            
        except Exception as e:
            print(f"Error processing batch {batch_id}: {e}")
            raise
    
    def _atomic_write(self, df, batch_id):
        """Atomic write using staging and rename."""
        staging_path = f"{self.output_location}_staging_{batch_id}"
        final_path = f"{self.output_location}/batch_{batch_id}"
        
        try:
            # Write to staging location
            df.write.mode("overwrite").parquet(staging_path)
            
            # Atomic rename (filesystem-dependent)
            self._atomic_rename(staging_path, final_path)
            
        except Exception as e:
            # Cleanup staging on failure
            self._cleanup_staging(staging_path)
            raise
    
    def _is_batch_processed(self, batch_id):
        """Check if batch was already processed."""
        checkpoint_file = f"{self.checkpoint_location}/batch_{batch_id}.checkpoint"
        return os.path.exists(checkpoint_file)
    
    def _mark_batch_processed(self, batch_id):
        """Mark batch as successfully processed."""
        checkpoint_file = f"{self.checkpoint_location}/batch_{batch_id}.checkpoint"
        with open(checkpoint_file, 'w') as f:
            f.write(f"processed_at: {datetime.now().isoformat()}")

# Structured Streaming with exactly-once
def create_exactly_once_stream():
    return spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "orders") \
        .option("startingOffsets", "earliest") \
        .load() \
        .writeStream \
        .foreachBatch(ExactlyOnceProcessor().process_batch) \
        .outputMode("append") \
        .option("checkpointLocation", "/checkpoints/exactly_once") \
        .trigger(processingTime="10 seconds") \
        .start()
```

**3. Two-Phase Commit Protocol:**
```python
class TwoPhaseCommitProcessor:
    def __init__(self, participants):
        self.participants = participants  # List of systems to coordinate
        self.transaction_log = TransactionLog()
    
    def process_with_2pc(self, data, transaction_id):
        """Process data using two-phase commit."""
        
        # Phase 1: Prepare
        prepare_results = []
        for participant in self.participants:
            try:
                result = participant.prepare(data, transaction_id)
                prepare_results.append((participant, result))
                self.transaction_log.log_prepare(transaction_id, participant.id, result)
            except Exception as e:
                # Abort on any prepare failure
                self._abort_transaction(transaction_id, prepare_results)
                raise
        
        # Check if all participants are ready
        if all(result.ready for _, result in prepare_results):
            # Phase 2: Commit
            self._commit_transaction(transaction_id, prepare_results)
        else:
            # Abort if any participant not ready
            self._abort_transaction(transaction_id, prepare_results)
    
    def _commit_transaction(self, transaction_id, prepare_results):
        """Commit transaction across all participants."""
        self.transaction_log.log_commit_start(transaction_id)
        
        for participant, _ in prepare_results:
            try:
                participant.commit(transaction_id)
                self.transaction_log.log_participant_commit(transaction_id, participant.id)
            except Exception as e:
                # Log failure but continue with other participants
                self.transaction_log.log_commit_failure(transaction_id, participant.id, str(e))
        
        self.transaction_log.log_commit_complete(transaction_id)
    
    def _abort_transaction(self, transaction_id, prepare_results):
        """Abort transaction across all participants."""
        self.transaction_log.log_abort_start(transaction_id)
        
        for participant, _ in prepare_results:
            try:
                participant.abort(transaction_id)
            except Exception as e:
                self.transaction_log.log_abort_failure(transaction_id, participant.id, str(e))
        
        self.transaction_log.log_abort_complete(transaction_id)
```

These advanced concepts demonstrate the complexity and sophistication required for enterprise-level data processing systems, covering multi-tenancy, lineage tracking, and exactly-once processing guarantees.