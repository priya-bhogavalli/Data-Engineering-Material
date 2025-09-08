# Data Engineering Fundamentals - Interview Questions

## Table of Contents
1. [Core Concepts](#core-concepts)
2. [Data Pipeline Design](#data-pipeline-design)
3. [ETL vs ELT](#etl-vs-elt)
4. [Data Quality & Governance](#data-quality--governance)
5. [Scalability & Performance](#scalability--performance)
6. [Real-World Scenarios](#real-world-scenarios)

---

## Core Concepts

### 1. What is Data Engineering and how does it differ from Data Science?

**Answer:**
Data Engineering focuses on building and maintaining the infrastructure and systems that collect, store, and process data. Key differences:

**Data Engineering:**
- Builds data pipelines and infrastructure
- Focuses on data availability, reliability, and scalability
- Works with production systems and large-scale data processing
- Ensures data quality and governance

**Data Science:**
- Analyzes data to extract insights and build models
- Focuses on statistical analysis and machine learning
- Works with processed, clean datasets
- Generates business insights and predictions

**Example:**
```python
# Data Engineering - Building ETL Pipeline
def extract_transform_load():
    # Extract from multiple sources
    raw_data = extract_from_sources(['database', 'api', 'files'])
    
    # Transform and clean
    clean_data = transform_data(raw_data)
    
    # Load to data warehouse
    load_to_warehouse(clean_data)

# Data Science - Analyzing processed data
def analyze_customer_behavior():
    # Use clean data from warehouse
    data = query_warehouse("SELECT * FROM customer_events")
    
    # Build predictive model
    model = train_model(data)
    return model.predict(new_data)
```

### 2. Explain the concept of Data Lineage and why it's important.

**Answer:**
Data Lineage tracks the flow of data from source to destination, showing transformations and dependencies.

**Importance:**
- **Impact Analysis**: Understand downstream effects of changes
- **Debugging**: Trace data quality issues to source
- **Compliance**: Meet regulatory requirements (GDPR, SOX)
- **Documentation**: Maintain data governance

**Example:**
```
Source DB → ETL Process → Data Lake → Transformation → Data Warehouse → BI Dashboard
     ↓           ↓              ↓             ↓              ↓
  Schema A → Clean/Filter → Parquet → Aggregate → Star Schema → KPIs
```

### 3. What are the key principles of building reliable data systems?

**Answer:**
**1. Idempotency**: Same input produces same output
```python
# Idempotent operation
def process_daily_data(date):
    # Delete existing data for date first
    delete_data_for_date(date)
    # Then process new data
    process_and_insert(date)
```

**2. Fault Tolerance**: System continues operating despite failures
**3. Monitoring & Alerting**: Proactive issue detection
**4. Data Quality Checks**: Validate data at each stage
**5. Scalability**: Handle growing data volumes
**6. Security**: Protect sensitive data

---

## Data Pipeline Design

### 4. Design a data pipeline for processing e-commerce transaction data in real-time.

**Answer:**
```
[Web App] → [Kafka] → [Stream Processing] → [Data Lake] → [Batch Processing] → [Data Warehouse]
    ↓           ↓            ↓                ↓              ↓                    ↓
Transactions → Topics → Flink/Spark → Raw Storage → ETL Jobs → Analytics Tables
```

**Components:**
1. **Ingestion**: Kafka for real-time event streaming
2. **Stream Processing**: Apache Flink for real-time aggregations
3. **Storage**: Data Lake (S3/HDFS) for raw data
4. **Batch Processing**: Spark for complex transformations
5. **Serving**: Data Warehouse for analytics

**Code Example:**
```python
# Kafka Producer
def publish_transaction(transaction):
    producer.send('transactions', transaction)

# Flink Stream Processing
def process_stream():
    transactions = env.add_source(FlinkKafkaConsumer('transactions'))
    
    # Real-time aggregations
    revenue_by_hour = transactions \
        .window(TumblingEventTimeWindows.of(Time.hours(1))) \
        .aggregate(RevenueAggregator())
    
    revenue_by_hour.add_sink(ElasticsearchSink())
```

### 5. How would you handle late-arriving data in a streaming pipeline?

**Answer:**
**Strategies:**
1. **Watermarks**: Define acceptable lateness threshold
2. **Windowing**: Use event time windows with grace periods
3. **Reprocessing**: Handle late data in separate batch jobs

**Implementation:**
```python
# Apache Flink example
def handle_late_data():
    stream = env.add_source(kafka_source) \
        .assign_timestamps_and_watermarks(
            WatermarkStrategy
            .for_bounded_out_of_orderness(Duration.of_minutes(5))
        ) \
        .window_all(TumblingEventTimeWindows.of(Time.hours(1))) \
        .allowed_lateness(Time.minutes(10)) \
        .side_output_late_data(late_data_tag)
    
    # Process main stream
    main_result = stream.aggregate(aggregator)
    
    # Handle late data separately
    late_data = main_result.get_side_output(late_data_tag)
```

### 6. Explain different data ingestion patterns and when to use each.

**Answer:**
**1. Batch Ingestion**
- **Use Case**: Large volumes, non-time-sensitive data
- **Tools**: Sqoop, Spark, Airflow
- **Example**: Daily sales reports, historical data migration

**2. Real-time Streaming**
- **Use Case**: Time-sensitive, continuous data
- **Tools**: Kafka, Kinesis, Pulsar
- **Example**: IoT sensors, user clickstreams

**3. Micro-batch**
- **Use Case**: Near real-time with small latency tolerance
- **Tools**: Spark Streaming, Storm
- **Example**: Fraud detection, recommendation updates

**4. Change Data Capture (CDC)**
- **Use Case**: Database synchronization
- **Tools**: Debezium, AWS DMS
- **Example**: Replicating OLTP to OLAP systems

---

## ETL vs ELT

### 7. Compare ETL and ELT approaches. When would you choose each?

**Answer:**
**ETL (Extract, Transform, Load):**
```
Source → Transform → Target
```
- Transform data before loading
- Better for structured data
- Reduces storage costs
- Traditional approach

**ELT (Extract, Load, Transform):**
```
Source → Target → Transform
```
- Load raw data first, transform later
- Better for big data and cloud
- More flexible and scalable
- Modern approach

**When to use ETL:**
- Limited storage capacity
- Well-defined transformation requirements
- Sensitive data requiring pre-processing
- Legacy systems

**When to use ELT:**
- Cloud-based data warehouses (Snowflake, BigQuery)
- Big data scenarios
- Exploratory data analysis needs
- Scalable compute resources available

### 8. How do you ensure data consistency in distributed ETL processes?

**Answer:**
**Strategies:**
1. **Transactional Processing**: Use database transactions
2. **Idempotent Operations**: Same operation can be repeated safely
3. **Checkpointing**: Save progress at regular intervals
4. **Two-Phase Commit**: Ensure all-or-nothing operations

**Implementation:**
```python
def consistent_etl_process():
    try:
        # Start transaction
        with database.transaction():
            # Extract
            data = extract_data()
            
            # Transform
            transformed = transform_data(data)
            
            # Validate
            if not validate_data(transformed):
                raise DataQualityError()
            
            # Load
            load_data(transformed)
            
            # Update checkpoint
            update_checkpoint(current_batch_id)
            
    except Exception as e:
        # Rollback on failure
        rollback_transaction()
        raise e
```

---

## Data Quality & Governance

### 9. What are the key dimensions of data quality and how do you measure them?

**Answer:**
**Six Dimensions of Data Quality:**

1. **Accuracy**: Data correctly represents reality
2. **Completeness**: No missing values where expected
3. **Consistency**: Data follows defined formats and rules
4. **Timeliness**: Data is up-to-date and available when needed
5. **Validity**: Data conforms to defined formats and constraints
6. **Uniqueness**: No duplicate records where not expected

**Measurement Example:**
```python
def measure_data_quality(df):
    quality_metrics = {
        'completeness': 1 - (df.isnull().sum() / len(df)),
        'uniqueness': len(df.drop_duplicates()) / len(df),
        'validity': validate_formats(df),
        'accuracy': cross_validate_with_source(df),
        'consistency': check_business_rules(df),
        'timeliness': check_data_freshness(df)
    }
    return quality_metrics
```

### 10. How do you implement data governance in a data engineering pipeline?

**Answer:**
**Key Components:**
1. **Data Catalog**: Metadata management and discovery
2. **Data Lineage**: Track data flow and transformations
3. **Access Control**: Role-based permissions
4. **Data Classification**: Identify sensitive data
5. **Quality Monitoring**: Automated data quality checks

**Implementation:**
```python
# Data governance framework
class DataGovernance:
    def __init__(self):
        self.catalog = DataCatalog()
        self.lineage = LineageTracker()
        self.access_control = AccessManager()
    
    def process_data(self, data, user, pipeline_id):
        # Check permissions
        if not self.access_control.has_permission(user, data.source):
            raise UnauthorizedError()
        
        # Track lineage
        self.lineage.track_transformation(data.source, pipeline_id)
        
        # Apply data classification
        classified_data = self.classify_sensitive_data(data)
        
        # Quality checks
        if not self.validate_quality(classified_data):
            raise DataQualityError()
        
        return classified_data
```

---

## Scalability & Performance

### 11. How do you design data pipelines to handle growing data volumes?

**Answer:**
**Scalability Strategies:**

1. **Horizontal Partitioning**: Distribute data across multiple nodes
2. **Parallel Processing**: Process data in parallel
3. **Incremental Processing**: Process only new/changed data
4. **Caching**: Store frequently accessed data in memory
5. **Compression**: Reduce storage and I/O costs

**Example:**
```python
# Scalable pipeline design
def scalable_pipeline():
    # Partition data by date
    partitions = partition_data_by_date(source_data)
    
    # Process partitions in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for partition in partitions:
            future = executor.submit(process_partition, partition)
            futures.append(future)
        
        # Collect results
        results = [future.result() for future in futures]
    
    # Merge results
    return merge_results(results)

def process_partition(partition):
    # Use columnar format for better compression
    df = pd.read_parquet(partition)
    
    # Apply transformations
    transformed = apply_transformations(df)
    
    # Write back in compressed format
    transformed.to_parquet(output_path, compression='snappy')
```

### 12. Explain different data storage formats and their trade-offs.

**Answer:**
**Storage Formats:**

1. **CSV**: Human-readable, simple, but inefficient
2. **JSON**: Flexible schema, but verbose
3. **Parquet**: Columnar, compressed, optimized for analytics
4. **Avro**: Schema evolution, good for streaming
5. **ORC**: Optimized for Hive, good compression

**Comparison:**
```python
# Performance comparison example
formats = {
    'csv': {
        'compression': 'Low',
        'query_speed': 'Slow',
        'schema_evolution': 'Poor',
        'use_case': 'Simple data exchange'
    },
    'parquet': {
        'compression': 'High',
        'query_speed': 'Fast',
        'schema_evolution': 'Good',
        'use_case': 'Analytics workloads'
    },
    'avro': {
        'compression': 'Medium',
        'query_speed': 'Medium',
        'schema_evolution': 'Excellent',
        'use_case': 'Streaming data'
    }
}
```

---

## Real-World Scenarios

### 13. You notice data quality issues in production. How do you investigate and resolve them?

**Answer:**
**Investigation Process:**
1. **Identify Scope**: Which data is affected?
2. **Trace Lineage**: Follow data flow upstream
3. **Check Recent Changes**: Code deployments, schema changes
4. **Validate Sources**: Verify source data quality
5. **Review Transformations**: Check transformation logic

**Resolution Steps:**
```python
def investigate_data_quality_issue():
    # 1. Identify affected data
    affected_tables = identify_quality_issues()
    
    # 2. Trace data lineage
    for table in affected_tables:
        lineage = get_data_lineage(table)
        print(f"Data flow for {table}: {lineage}")
    
    # 3. Check source data quality
    source_quality = validate_source_data(lineage.source)
    
    # 4. Compare with historical patterns
    historical_metrics = get_historical_quality_metrics(table)
    current_metrics = calculate_current_metrics(table)
    
    # 5. Identify root cause
    root_cause = compare_metrics(historical_metrics, current_metrics)
    
    return root_cause

def resolve_quality_issue(root_cause):
    if root_cause == 'source_data_corruption':
        # Re-extract from backup
        reprocess_from_backup()
    elif root_cause == 'transformation_error':
        # Fix transformation logic and reprocess
        fix_transformation()
        reprocess_affected_data()
```

### 14. How would you migrate a legacy data warehouse to a modern cloud-based solution?

**Answer:**
**Migration Strategy:**
1. **Assessment**: Analyze current system and requirements
2. **Planning**: Design target architecture
3. **Pilot**: Start with non-critical workloads
4. **Parallel Run**: Run both systems simultaneously
5. **Cutover**: Switch to new system
6. **Optimization**: Fine-tune performance

**Implementation:**
```python
def migration_plan():
    phases = {
        'phase_1_assessment': {
            'duration': '2-4 weeks',
            'activities': [
                'Inventory existing data sources',
                'Analyze data volumes and growth',
                'Document current ETL processes',
                'Identify dependencies'
            ]
        },
        'phase_2_design': {
            'duration': '4-6 weeks',
            'activities': [
                'Design target architecture',
                'Select cloud platform and tools',
                'Plan data migration strategy',
                'Design security and governance'
            ]
        },
        'phase_3_pilot': {
            'duration': '6-8 weeks',
            'activities': [
                'Migrate sample datasets',
                'Build core ETL pipelines',
                'Test performance and functionality',
                'Train team on new tools'
            ]
        }
    }
    return phases
```

### 15. Design a disaster recovery strategy for a critical data pipeline.

**Answer:**
**DR Strategy Components:**
1. **Backup Strategy**: Regular data and metadata backups
2. **Replication**: Real-time data replication to DR site
3. **Monitoring**: Automated failure detection
4. **Failover**: Automated or manual failover procedures
5. **Recovery**: Data recovery and validation processes

**Implementation:**
```python
class DisasterRecoveryManager:
    def __init__(self):
        self.primary_site = PrimarySite()
        self.dr_site = DRSite()
        self.monitor = HealthMonitor()
    
    def setup_replication(self):
        # Set up real-time replication
        self.primary_site.enable_replication(self.dr_site)
        
        # Configure backup schedules
        self.schedule_backups()
    
    def monitor_health(self):
        while True:
            if not self.primary_site.is_healthy():
                self.initiate_failover()
            time.sleep(60)  # Check every minute
    
    def initiate_failover(self):
        # Stop primary site processing
        self.primary_site.stop_processing()
        
        # Activate DR site
        self.dr_site.activate()
        
        # Update DNS/load balancer
        self.update_routing_to_dr()
        
        # Notify stakeholders
        self.send_failover_notification()
    
    def recover_primary(self):
        # Sync data from DR to primary
        self.sync_data_to_primary()
        
        # Validate data consistency
        if self.validate_data_consistency():
            # Switch back to primary
            self.failback_to_primary()
```

---

## Advanced Topics

### 16. Explain the CAP theorem and its implications for data engineering.

**Answer:**
**CAP Theorem**: In a distributed system, you can only guarantee two of:
- **Consistency**: All nodes see the same data simultaneously
- **Availability**: System remains operational
- **Partition Tolerance**: System continues despite network failures

**Implications:**
- **CP Systems**: Consistent but may be unavailable (traditional RDBMS)
- **AP Systems**: Available but eventually consistent (NoSQL databases)
- **CA Systems**: Not realistic in distributed environments

**Data Engineering Decisions:**
```python
# Choose based on requirements
def select_database(requirements):
    if requirements.strict_consistency:
        return "PostgreSQL"  # CP system
    elif requirements.high_availability:
        return "Cassandra"   # AP system
    else:
        return "MongoDB"     # Balanced approach
```

### 17. How do you handle schema evolution in data pipelines?

**Answer:**
**Schema Evolution Strategies:**
1. **Backward Compatibility**: New schema can read old data
2. **Forward Compatibility**: Old schema can read new data
3. **Full Compatibility**: Both backward and forward compatible

**Implementation:**
```python
# Avro schema evolution example
def evolve_schema():
    # Original schema
    original_schema = {
        "type": "record",
        "name": "User",
        "fields": [
            {"name": "id", "type": "int"},
            {"name": "name", "type": "string"}
        ]
    }
    
    # Evolved schema (backward compatible)
    evolved_schema = {
        "type": "record",
        "name": "User",
        "fields": [
            {"name": "id", "type": "int"},
            {"name": "name", "type": "string"},
            {"name": "email", "type": ["null", "string"], "default": None}
        ]
    }
    
    return evolved_schema

# Handle schema changes in pipeline
def process_with_schema_evolution(data):
    try:
        # Try with latest schema
        return process_with_schema(data, latest_schema)
    except SchemaCompatibilityError:
        # Fallback to previous schema
        return process_with_schema(data, previous_schema)
```

### 18. What are the key considerations for building a data lake architecture?

**Answer:**
**Data Lake Architecture Considerations:**

1. **Storage Layer**: Scalable, cost-effective storage (S3, HDFS)
2. **Ingestion Layer**: Handle various data sources and formats
3. **Processing Layer**: Batch and stream processing capabilities
4. **Catalog Layer**: Metadata management and data discovery
5. **Security Layer**: Access control and data encryption
6. **Governance Layer**: Data quality and compliance

**Architecture Example:**
```python
class DataLakeArchitecture:
    def __init__(self):
        self.storage = S3Storage()
        self.ingestion = MultiSourceIngestion()
        self.processing = SparkProcessing()
        self.catalog = GlueCatalog()
        self.security = IAMSecurity()
    
    def ingest_data(self, source, format):
        # Raw data ingestion
        raw_path = f"s3://datalake/raw/{source}/"
        self.ingestion.ingest(source, raw_path, format)
        
        # Update catalog
        self.catalog.register_dataset(raw_path, format)
    
    def process_data(self, dataset):
        # Process raw data
        processed = self.processing.transform(dataset)
        
        # Store processed data
        processed_path = f"s3://datalake/processed/{dataset}/"
        processed.write.parquet(processed_path)
        
        return processed_path
```

This comprehensive set of interview questions covers the fundamental concepts that every data engineer should understand, from basic principles to advanced architectural considerations.