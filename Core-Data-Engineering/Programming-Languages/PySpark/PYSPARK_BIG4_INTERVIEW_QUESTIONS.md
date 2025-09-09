# Big 4 Consulting PySpark Interview Questions

## Architecture & Design Questions

**Q1: Design a real-time fraud detection system using PySpark for a major bank processing 1 million transactions per minute.**

**Answer**: I would design a multi-layered architecture:

**Streaming Architecture**:
```python
# Kafka consumer for real-time transactions
transaction_stream = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka-cluster:9092") \
    .option("subscribe", "transactions") \
    .option("maxOffsetsPerTrigger", 100000) \
    .load()

# Parse and enrich transactions
enriched_stream = transaction_stream \
    .select(from_json(col("value").cast("string"), transaction_schema).alias("txn")) \
    .select("txn.*") \
    .withColumn("processing_time", current_timestamp()) \
    .join(broadcast(customer_profiles), "customer_id", "left")
```

**Multi-Model Fraud Detection**:
```python
def fraud_detection_pipeline(df):
    # Rule-based detection (fast)
    rule_based_flags = df.withColumn("rule_fraud_score",
        when(col("amount") > 10000, 0.8)
        .when(col("merchant_category") == "high_risk", 0.6)
        .when(col("transaction_hour") < 6, 0.4)
        .otherwise(0.0)
    )
    
    # ML model scoring (batch every 5 minutes)
    ml_features = create_ml_features(rule_based_flags)
    ml_scored = ml_model.transform(ml_features)
    
    # Ensemble scoring
    final_scores = ml_scored.withColumn("final_fraud_score",
        (col("rule_fraud_score") * 0.3 + col("ml_fraud_score") * 0.7)
    )
    
    return final_scores.withColumn("fraud_flag",
        when(col("final_fraud_score") > 0.7, "HIGH")
        .when(col("final_fraud_score") > 0.4, "MEDIUM")
        .otherwise("LOW")
    )

# Real-time processing with watermarking
fraud_results = enriched_stream \
    .withWatermark("processing_time", "2 minutes") \
    .transform(fraud_detection_pipeline)
```

**Scalability Considerations**:
- Partition by customer_id for data locality
- Use Delta Lake for ACID transactions
- Implement circuit breakers for external service calls
- Auto-scaling based on Kafka lag metrics

**Q2: A Fortune 500 retail client wants to migrate their legacy ETL system (processing 50TB daily) to PySpark. How would you approach this migration?**

**Answer**: Systematic migration approach:

**Phase 1: Assessment and Planning**
```python
class LegacyETLAnalyzer:
    def __init__(self, legacy_jobs):
        self.jobs = legacy_jobs
        self.complexity_matrix = {}
    
    def analyze_complexity(self):
        for job in self.jobs:
            complexity = {
                "data_volume": self.assess_volume(job),
                "transformation_complexity": self.assess_transformations(job),
                "dependencies": self.map_dependencies(job),
                "business_criticality": self.assess_criticality(job)
            }
            self.complexity_matrix[job.name] = complexity
        return self.prioritize_migration()
    
    def prioritize_migration(self):
        # Prioritize by low complexity, high business value
        return sorted(self.complexity_matrix.items(), 
                     key=lambda x: (x[1]['complexity'], -x[1]['business_value']))
```

**Phase 2: Proof of Concept**
```python
def create_poc_pipeline(legacy_job):
    """Create PySpark equivalent of legacy job"""
    
    # Parallel processing strategy
    spark_config = {
        "spark.sql.adaptive.enabled": "true",
        "spark.sql.adaptive.coalescePartitions.enabled": "true",
        "spark.sql.adaptive.skewJoin.enabled": "true",
        "spark.executor.memory": "16g",
        "spark.executor.cores": "5",
        "spark.executor.instances": "100"
    }
    
    spark = create_spark_session("POC_Migration", spark_config)
    
    # Implement equivalent transformations
    source_df = spark.read.format("delta").load(legacy_job.source_path)
    
    # Optimize common patterns
    if legacy_job.has_complex_joins():
        result = optimize_complex_joins(source_df, legacy_job.join_logic)
    
    if legacy_job.has_aggregations():
        result = optimize_aggregations(result, legacy_job.agg_logic)
    
    # Performance comparison
    benchmark_results = compare_performance(legacy_job, result)
    return result, benchmark_results
```

**Phase 3: Production Migration**
```python
class ProductionMigrationFramework:
    def __init__(self):
        self.migration_tracker = MigrationTracker()
        self.rollback_manager = RollbackManager()
    
    def migrate_job(self, legacy_job, pyspark_job):
        try:
            # Parallel execution for validation
            legacy_result = self.run_legacy_job(legacy_job)
            pyspark_result = self.run_pyspark_job(pyspark_job)
            
            # Data validation
            validation_results = self.validate_results(legacy_result, pyspark_result)
            
            if validation_results.success_rate > 0.999:
                self.cutover_to_pyspark(pyspark_job)
                self.migration_tracker.mark_success(legacy_job.name)
            else:
                self.rollback_manager.rollback(legacy_job.name)
                raise MigrationValidationError(validation_results)
                
        except Exception as e:
            self.handle_migration_failure(legacy_job, e)
```

## Performance & Optimization Questions

**Q3: Your PySpark job processing customer analytics is taking 8 hours instead of the required 2 hours. Walk me through your optimization approach.**

**Answer**: Systematic performance optimization:

**Step 1: Profiling and Analysis**
```python
def profile_spark_job(spark):
    """Comprehensive job profiling"""
    
    # Enable detailed metrics
    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    spark.conf.set("spark.sql.adaptive.enabled", "true")
    spark.conf.set("spark.eventLog.enabled", "true")
    
    # Analyze query plans
    df.explain(mode="cost")  # Analyze execution plan
    
    # Check partition distribution
    partition_stats = df.rdd.mapPartitions(lambda x: [sum(1 for _ in x)]).collect()
    print(f"Partition sizes: {partition_stats}")
    
    # Memory usage analysis
    storage_level_info = spark.sparkContext.statusTracker().getExecutorInfos()
    return storage_level_info

def identify_bottlenecks(df, operations):
    """Identify performance bottlenecks"""
    bottlenecks = []
    
    # Check for data skew
    skew_analysis = df.groupBy("partition_key").count().orderBy(desc("count"))
    if skew_analysis.first()["count"] > skew_analysis.collect()[-1]["count"] * 10:
        bottlenecks.append("DATA_SKEW")
    
    # Check for small files
    file_stats = spark.sql("DESCRIBE DETAIL delta_table").select("numFiles", "sizeInBytes")
    avg_file_size = file_stats.first()["sizeInBytes"] / file_stats.first()["numFiles"]
    if avg_file_size < 128 * 1024 * 1024:  # Less than 128MB
        bottlenecks.append("SMALL_FILES")
    
    return bottlenecks
```

**Step 2: Targeted Optimizations**
```python
def optimize_customer_analytics(df):
    """Apply specific optimizations"""
    

