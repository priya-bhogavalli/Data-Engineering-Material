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
    
    # 1. Optimize joins with broadcast
    customer_dim = spark.read.table("customer_dimension")
    if customer_dim.count() < 1000000:  # Small enough to broadcast
        df = df.join(broadcast(customer_dim), "customer_id")
    
    # 2. Partition pruning and column pruning
    df = df.select("customer_id", "transaction_date", "amount", "category") \
           .filter(col("transaction_date") >= "2023-01-01")
    
    # 3. Optimize aggregations with pre-aggregation
    daily_aggs = df.groupBy("customer_id", "transaction_date") \
                   .agg(sum("amount").alias("daily_amount"),
                        count("*").alias("daily_transactions"))
    
    # 4. Use window functions efficiently
    window_spec = Window.partitionBy("customer_id").orderBy("transaction_date")
    result = daily_aggs.withColumn("running_total",
        sum("daily_amount").over(window_spec.rowsBetween(Window.unboundedPreceding, 0))
    )
    
    # 5. Optimize storage format
    result.write.format("delta") \
          .option("optimizeWrite", "true") \
          .option("autoCompact", "true") \
          .partitionBy("transaction_date") \
          .save("optimized_customer_analytics")
    
    return result

# Advanced optimization techniques
def apply_advanced_optimizations(spark):
    # Dynamic partition pruning
    spark.conf.set("spark.sql.optimizer.dynamicPartitionPruning.enabled", "true")
    
    # Adaptive query execution
    spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
    spark.conf.set("spark.sql.adaptive.localShuffleReader.enabled", "true")
    
    # Z-ordering for Delta tables
    spark.sql("OPTIMIZE customer_analytics ZORDER BY (customer_id)")
```

**Step 3: Resource Optimization**
```python
def optimize_cluster_resources():
    """Optimize Spark cluster configuration"""
    
    optimal_config = {
        # Executor configuration
        "spark.executor.memory": "14g",
        "spark.executor.memoryFraction": "0.8",
        "spark.executor.cores": "5",
        "spark.executor.instances": "40",
        
        # Driver configuration
        "spark.driver.memory": "8g",
        "spark.driver.maxResultSize": "4g",
        
        # Shuffle optimization
        "spark.sql.shuffle.partitions": "400",
        "spark.shuffle.compress": "true",
        "spark.shuffle.spill.compress": "true",
        
        # Serialization
        "spark.serializer": "org.apache.spark.serializer.KryoSerializer",
        "spark.kryo.unsafe": "true"
    }
    
    return optimal_config
```

**Q4: Design a data quality framework using PySpark that can handle 100+ data sources with different quality requirements.**

**Answer**: Comprehensive data quality framework:

**Framework Architecture**:
```python
from abc import ABC, abstractmethod
from typing import Dict, List, Any
import json

class DataQualityRule(ABC):
    """Abstract base class for data quality rules"""
    
    @abstractmethod
    def validate(self, df: DataFrame) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_rule_name(self) -> str:
        pass

class CompletenessRule(DataQualityRule):
    def __init__(self, columns: List[str], threshold: float = 0.95):
        self.columns = columns
        self.threshold = threshold
    
    def validate(self, df: DataFrame) -> Dict[str, Any]:
        total_rows = df.count()
        results = {}
        
        for column in self.columns:
            non_null_count = df.filter(col(column).isNotNull()).count()
            completeness = non_null_count / total_rows if total_rows > 0 else 0
            
            results[column] = {
                "completeness_score": completeness,
                "passed": completeness >= self.threshold,
                "total_rows": total_rows,
                "non_null_rows": non_null_count
            }
        
        return results
    
    def get_rule_name(self) -> str:
        return "completeness_check"

class UniquenessRule(DataQualityRule):
    def __init__(self, columns: List[str]):
        self.columns = columns
    
    def validate(self, df: DataFrame) -> Dict[str, Any]:
        results = {}
        
        for column in self.columns:
            total_count = df.count()
            distinct_count = df.select(column).distinct().count()
            uniqueness = distinct_count / total_count if total_count > 0 else 0
            
            results[column] = {
                "uniqueness_score": uniqueness,
                "passed": uniqueness == 1.0,
                "total_rows": total_count,
                "distinct_rows": distinct_count,
                "duplicate_rows": total_count - distinct_count
            }
        
        return results
    
    def get_rule_name(self) -> str:
        return "uniqueness_check"

class DataQualityFramework:
    def __init__(self, spark: SparkSession):
        self.spark = spark
        self.rules_registry = {}
        self.source_configs = {}
    
    def register_rule(self, rule: DataQualityRule):
        """Register a data quality rule"""
        self.rules_registry[rule.get_rule_name()] = rule
    
    def configure_source(self, source_name: str, config: Dict[str, Any]):
        """Configure quality requirements for a data source"""
        self.source_configs[source_name] = config
    
    def validate_data_source(self, source_name: str, df: DataFrame) -> Dict[str, Any]:
        """Validate a data source against its configured rules"""
        
        if source_name not in self.source_configs:
            raise ValueError(f"No configuration found for source: {source_name}")
        
        config = self.source_configs[source_name]
        results = {
            "source_name": source_name,
            "validation_timestamp": datetime.now().isoformat(),
            "rule_results": {},
            "overall_status": "PASSED"
        }
        
        # Apply configured rules
        for rule_config in config.get("rules", []):
            rule_name = rule_config["rule_name"]
            rule_params = rule_config.get("parameters", {})
            
            if rule_name in self.rules_registry:
                rule = self.rules_registry[rule_name]
                rule_result = rule.validate(df)
                results["rule_results"][rule_name] = rule_result
                
                # Check if any rule failed
                if not all(r.get("passed", True) for r in rule_result.values()):
                    results["overall_status"] = "FAILED"
        
        # Store results for monitoring
        self.store_validation_results(results)
        
        return results
    
    def store_validation_results(self, results: Dict[str, Any]):
        """Store validation results for monitoring and alerting"""
        results_df = self.spark.createDataFrame([results])
        
        results_df.write \
            .format("delta") \
            .mode("append") \
            .option("mergeSchema", "true") \
            .save("data_quality_results")
```

**Configuration Management**:
```python
def setup_data_quality_configs():
    """Setup configurations for different data sources"""
    
    # Customer data configuration
    customer_config = {
        "rules": [
            {
                "rule_name": "completeness_check",
                "parameters": {
                    "columns": ["customer_id", "email", "registration_date"],
                    "threshold": 0.98
                }
            },
            {
                "rule_name": "uniqueness_check",
                "parameters": {
                    "columns": ["customer_id", "email"]
                }
            },
            {
                "rule_name": "validity_check",
                "parameters": {
                    "email_pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                    "date_range": {"min": "2020-01-01", "max": "2024-12-31"}
                }
            }
        ],
        "alert_thresholds": {
            "critical": 0.95,
            "warning": 0.98
        }
    }
    
    # Transaction data configuration
    transaction_config = {
        "rules": [
            {
                "rule_name": "completeness_check",
                "parameters": {
                    "columns": ["transaction_id", "customer_id", "amount", "timestamp"],
                    "threshold": 0.999
                }
            },
            {
                "rule_name": "range_check",
                "parameters": {
                    "amount": {"min": 0, "max": 1000000},
                    "timestamp": {"min": "2023-01-01", "max": "2024-12-31"}
                }
            }
        ]
    }
    
    return {
        "customer_data": customer_config,
        "transaction_data": transaction_config
    }

# Automated quality monitoring
class DataQualityMonitor:
    def __init__(self, framework: DataQualityFramework):
        self.framework = framework
        self.alert_manager = AlertManager()
    
    def run_scheduled_validation(self, source_name: str, schedule: str):
        """Run validation on schedule"""
        
        # Read latest data
        df = self.framework.spark.read.format("delta").load(f"sources/{source_name}")
        
        # Run validation
        results = self.framework.validate_data_source(source_name, df)
        
        # Check for alerts
        if results["overall_status"] == "FAILED":
            self.alert_manager.send_alert(
                severity="CRITICAL",
                message=f"Data quality validation failed for {source_name}",
                details=results
            )
        
        return results
    
    def generate_quality_dashboard(self):
        """Generate data quality dashboard"""
        
        quality_trends = self.framework.spark.sql("""
            SELECT 
                source_name,
                DATE(validation_timestamp) as validation_date,
                overall_status,
                COUNT(*) as validation_count
            FROM data_quality_results
            WHERE validation_timestamp >= current_date() - INTERVAL 30 DAYS
            GROUP BY source_name, DATE(validation_timestamp), overall_status
            ORDER BY validation_date DESC
        """)
        
        return quality_trends
```

## Streaming & Real-time Questions

**Q5: Design a real-time recommendation engine using PySpark Streaming that can handle 50,000 user interactions per second.**

**Answer**: High-throughput streaming recommendation system:

**Streaming Architecture**:
```python
class RealTimeRecommendationEngine:
    def __init__(self, spark: SparkSession):
        self.spark = spark
        self.model_store = ModelStore()
        self.feature_store = FeatureStore()
        
    def setup_streaming_pipeline(self):
        """Setup high-throughput streaming pipeline"""
        
        # Configure for high throughput
        stream_config = {
            "maxOffsetsPerTrigger": 50000,
            "kafka.max.poll.records": 10000,
            "kafka.fetch.max.bytes": 52428800,  # 50MB
            "kafka.max.partition.fetch.bytes": 10485760  # 10MB
        }
        
        # Read user interactions
        user_interactions = self.spark \
            .readStream \
            .format("kafka") \
            .options(**stream_config) \
            .option("kafka.bootstrap.servers", "kafka-cluster:9092") \
            .option("subscribe", "user-interactions") \
            .load()
        
        # Parse and enrich interactions
        parsed_interactions = user_interactions \
            .select(from_json(col("value").cast("string"), interaction_schema).alias("interaction")) \
            .select("interaction.*") \
            .withColumn("processing_timestamp", current_timestamp())
        
        return parsed_interactions
    
    def real_time_feature_engineering(self, interactions_df):
        """Generate real-time features for recommendations"""
        
        # Session-based features (5-minute windows)
        session_features = interactions_df \
            .withWatermark("processing_timestamp", "1 minute") \
            .groupBy(
                col("user_id"),
                window(col("processing_timestamp"), "5 minutes")
            ) \
            .agg(
                count("*").alias("session_interactions"),
                collect_list("item_id").alias("session_items"),
                collect_list("action_type").alias("session_actions"),
                avg("rating").alias("avg_session_rating")
            )
        
        # Real-time user preferences
        user_preferences = interactions_df \
            .filter(col("action_type").isin(["like", "purchase", "add_to_cart"])) \
            .groupBy("user_id") \
            .agg(
                collect_list("category").alias("preferred_categories"),
                avg("price").alias("avg_price_preference"),
                count("*").alias("positive_interactions")
            )
        
        return session_features, user_preferences
    
    def generate_recommendations(self, user_features_df):
        """Generate real-time recommendations"""
        
        # Load pre-trained models
        collaborative_model = self.model_store.load_model("collaborative_filtering")
        content_model = self.model_store.load_model("content_based")
        
        # Collaborative filtering recommendations
        cf_recommendations = collaborative_model.recommendForUserSubset(
            user_features_df.select("user_id"), 10
        )
        
        # Content-based recommendations
        content_recommendations = content_model.transform(user_features_df)
        
        # Ensemble recommendations
        final_recommendations = self.ensemble_recommendations(
            cf_recommendations, content_recommendations
        )
        
        return final_recommendations
    
    def ensemble_recommendations(self, cf_recs, content_recs):
        """Combine multiple recommendation approaches"""
        
        # Weight-based ensemble
        ensemble_recs = cf_recs.alias("cf").join(
            content_recs.alias("content"), 
            "user_id", "outer"
        ).select(
            col("user_id"),
            # Combine recommendation scores
            when(col("cf.recommendations").isNotNull() & col("content.recommendations").isNotNull(),
                 # Both models have recommendations - weighted average
                 expr("transform(cf.recommendations, x -> struct(x.item_id, x.rating * 0.6 + content.score * 0.4 as rating))")
            ).when(col("cf.recommendations").isNotNull(),
                 # Only collaborative filtering
                 col("cf.recommendations")
            ).otherwise(
                 # Only content-based
                 col("content.recommendations")
            ).alias("final_recommendations")
        )
        
        return ensemble_recs
```

**High-Performance Serving**:
```python
def setup_high_performance_serving(recommendations_stream):
    """Setup high-performance recommendation serving"""
    
    # Write to multiple sinks for different use cases
    
    # 1. Real-time cache (Redis) for immediate serving
    redis_sink = recommendations_stream \
        .selectExpr("user_id as key", "to_json(final_recommendations) as value") \
        .writeStream \
        .format("redis") \
        .option("host", "redis-cluster") \
        .option("port", "6379") \
        .option("ttl", "3600") \
        .outputMode("update") \
        .trigger(processingTime="10 seconds")
    
    # 2. Feature store for model training
    feature_store_sink = recommendations_stream \
        .writeStream \
        .format("delta") \
        .option("checkpointLocation", "checkpoints/recommendations") \
        .outputMode("append") \
        .trigger(processingTime="30 seconds") \
        .start("feature_store/recommendations")
    
    # 3. Analytics sink for monitoring
    analytics_sink = recommendations_stream \
        .select("user_id", "processing_timestamp", 
                size("final_recommendations").alias("num_recommendations")) \
        .writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka-cluster:9092") \
        .option("topic", "recommendation-analytics") \
        .outputMode("append") \
        .trigger(processingTime="5 seconds")
    
    return [redis_sink, feature_store_sink, analytics_sink]

# Performance monitoring and auto-scaling
class StreamingPerformanceMonitor:
    def __init__(self, streaming_query):
        self.query = streaming_query
        self.metrics_collector = MetricsCollector()
    
    def monitor_performance(self):
        """Monitor streaming performance metrics"""
        
        progress = self.query.lastProgress
        
        metrics = {
            "input_rows_per_second": progress.get("inputRowsPerSecond", 0),
            "processed_rows_per_second": progress.get("processedRowsPerSecond", 0),
            "batch_duration": progress.get("batchDuration", 0),
            "trigger_execution_time": progress.get("durationMs", {}).get("triggerExecution", 0)
        }
        
        # Auto-scaling logic
        if metrics["input_rows_per_second"] > 45000:  # Approaching limit
            self.scale_up_resources()
        elif metrics["input_rows_per_second"] < 10000:  # Under-utilized
            self.scale_down_resources()
        
        return metrics
    
    def scale_up_resources(self):
        """Scale up streaming resources"""
        # Increase Kafka partitions
        # Add more Spark executors
        # Increase memory allocation
        pass
    
    def scale_down_resources(self):
        """Scale down streaming resources"""
        # Reduce executor count
        # Decrease memory allocation
        pass
```

## Machine Learning & Advanced Analytics Questions

**Q6: Implement a distributed machine learning pipeline using PySpark MLlib for customer churn prediction with feature engineering, model training, and deployment.**

**Answer**: End-to-end ML pipeline implementation:

**Feature Engineering Pipeline**:
```python
from pyspark.ml import Pipeline
from pyspark.ml.feature import *
from pyspark.ml.classification import *
from pyspark.ml.evaluation import *
from pyspark.ml.tuning import *

class ChurnPredictionPipeline:
    def __init__(self, spark: SparkSession):
        self.spark = spark
        self.feature_pipeline = None
        self.model_pipeline = None
    
    def create_feature_engineering_pipeline(self):
        """Create comprehensive feature engineering pipeline"""
        
        # Categorical encoding
        string_indexers = [
            StringIndexer(inputCol=col, outputCol=f"{col}_indexed", handleInvalid="keep")
            for col in ["subscription_type", "payment_method", "region", "device_type"]
        ]
        
        # One-hot encoding
        one_hot_encoders = [
            OneHotEncoder(inputCol=f"{col}_indexed", outputCol=f"{col}_encoded")
            for col in ["subscription_type", "payment_method", "region", "device_type"]
        ]
        
        # Numerical feature scaling
        numerical_cols = ["monthly_charges", "total_charges", "tenure_months", 
                         "support_tickets", "login_frequency", "data_usage"]
        
        vector_assembler_num = VectorAssembler(
            inputCols=numerical_cols,
            outputCol="numerical_features"
        )
        
        scaler = StandardScaler(
            inputCol="numerical_features",
            outputCol="scaled_numerical_features",
            withStd=True,
            withMean=True
        )
        
        # Advanced feature engineering
        # Interaction features
        interaction_features = SQLTransformer(sql="""
            SELECT *, 
                   monthly_charges * tenure_months as lifetime_value,
                   support_tickets / tenure_months as support_rate,
                   data_usage / monthly_charges as usage_efficiency,
                   CASE WHEN login_frequency > 20 THEN 1 ELSE 0 END as high_engagement
            FROM __THIS__
        """)
        
        # Temporal features
        temporal_features = SQLTransformer(sql="""
            SELECT *,
                   MONTH(last_login_date) as last_login_month,
                   DATEDIFF(current_date(), last_login_date) as days_since_login,
                   CASE WHEN DAYOFWEEK(registration_date) IN (1,7) THEN 1 ELSE 0 END as weekend_registration
            FROM __THIS__
        """)
        
        # Final feature assembly
        feature_cols = (
            [f"{col}_encoded" for col in ["subscription_type", "payment_method", "region", "device_type"]] +
            ["scaled_numerical_features", "lifetime_value", "support_rate", "usage_efficiency", 
             "high_engagement", "last_login_month", "days_since_login", "weekend_registration"]
        )
        
        final_assembler = VectorAssembler(
            inputCols=feature_cols,
            outputCol="features"
        )
        
        # Create pipeline
        self.feature_pipeline = Pipeline(stages=(
            string_indexers + one_hot_encoders + 
            [vector_assembler_num, scaler, interaction_features, temporal_features, final_assembler]
        ))
        
        return self.feature_pipeline
    
    def create_model_pipeline(self):
        """Create model training pipeline with hyperparameter tuning"""
        
        # Label encoding
        label_indexer = StringIndexer(inputCol="churn", outputCol="label")
        
        # Multiple algorithms for ensemble
        rf = RandomForestClassifier(
            featuresCol="features",
            labelCol="label",
            numTrees=100,
            maxDepth=10,
            seed=42
        )
        
        gbt = GBTClassifier(
            featuresCol="features",
            labelCol="label",
            maxIter=100,
            maxDepth=6,
            seed=42
        )
        
        lr = LogisticRegression(
            featuresCol="features",
            labelCol="label",
            maxIter=100,
            regParam=0.01
        )
        
        # Ensemble using VotingClassifier (custom implementation)
        ensemble_model = self.create_ensemble_classifier([rf, gbt, lr])
        
        # Create pipeline
        self.model_pipeline = Pipeline(stages=[label_indexer, ensemble_model])
        
        return self.model_pipeline
    
    def create_ensemble_classifier(self, base_models):
        """Create ensemble classifier"""
        # Custom ensemble implementation
        class EnsembleClassifier:
            def __init__(self, models):
                self.models = models
                self.fitted_models = []
            
            def fit(self, df):
                self.fitted_models = []
                for model in self.models:
                    fitted_model = model.fit(df)
                    self.fitted_models.append(fitted_model)
                return self
            
            def transform(self, df):
                predictions = []
                for model in self.fitted_models:
                    pred_df = model.transform(df)
                    predictions.append(pred_df.select("probability"))
                
                # Average probabilities
                ensemble_df = df
                for i, pred_df in enumerate(predictions):
                    ensemble_df = ensemble_df.join(
                        pred_df.withColumnRenamed("probability", f"prob_{i}"),
                        on=df.columns
                    )
                
                # Calculate ensemble prediction
                ensemble_df = ensemble_df.withColumn(
                    "ensemble_probability",
                    (col("prob_0") + col("prob_1") + col("prob_2")) / 3
                ).withColumn(
                    "prediction",
                    when(col("ensemble_probability")[1] > 0.5, 1.0).otherwise(0.0)
                )
                
                return ensemble_df
        
        return EnsembleClassifier(base_models)
    
    def hyperparameter_tuning(self, train_df):
        """Perform hyperparameter tuning"""
        
        # Parameter grid for Random Forest
        rf_param_grid = ParamGridBuilder() \
            .addGrid(RandomForestClassifier.numTrees, [50, 100, 200]) \
            .addGrid(RandomForestClassifier.maxDepth, [5, 10, 15]) \
            .addGrid(RandomForestClassifier.minInstancesPerNode, [1, 5, 10]) \
            .build()
        
        # Cross-validation
        evaluator = BinaryClassificationEvaluator(
            labelCol="label",
            rawPredictionCol="rawPrediction",
            metricName="areaUnderROC"
        )
        
        cv = CrossValidator(
            estimator=self.model_pipeline,
            estimatorParamMaps=rf_param_grid,
            evaluator=evaluator,
            numFolds=5,
            seed=42
        )
        
        # Fit cross-validator
        cv_model = cv.fit(train_df)
        
        return cv_model
    
    def evaluate_model(self, model, test_df):
        """Comprehensive model evaluation"""
        
        predictions = model.transform(test_df)
        
        # Multiple evaluation metrics
        evaluators = {
            "auc": BinaryClassificationEvaluator(
                labelCol="label", rawPredictionCol="rawPrediction", metricName="areaUnderROC"
            ),
            "precision": MulticlassClassificationEvaluator(
                labelCol="label", predictionCol="prediction", metricName="weightedPrecision"
            ),
            "recall": MulticlassClassificationEvaluator(
                labelCol="label", predictionCol="prediction", metricName="weightedRecall"
            ),
            "f1": MulticlassClassificationEvaluator(
                labelCol="label", predictionCol="prediction", metricName="f1"
            )
        }
        
        metrics = {}
        for metric_name, evaluator in evaluators.items():
            metrics[metric_name] = evaluator.evaluate(predictions)
        
        # Confusion matrix
        confusion_matrix = predictions.groupBy("label", "prediction").count().collect()
        
        # Feature importance (for tree-based models)
        if hasattr(model.stages[-1], 'featureImportances'):
            feature_importance = model.stages[-1].featureImportances.toArray()
            metrics["feature_importance"] = feature_importance
        
        return metrics, confusion_matrix
    
    def deploy_model(self, model, model_name: str, version: str):
        """Deploy model for production use"""
        
        # Save model
        model_path = f"models/{model_name}/v{version}"
        model.write().overwrite().save(model_path)
        
        # Create model serving endpoint
        serving_pipeline = self.create_serving_pipeline(model)
        
        # Register model in model registry
        self.register_model(model_name, version, model_path, metrics)
        
        return serving_pipeline
    
    def create_serving_pipeline(self, model):
        """Create real-time serving pipeline"""
        
        def predict_churn(customer_data):
            """Real-time churn prediction"""
            
            # Convert to DataFrame
            df = self.spark.createDataFrame([customer_data])
            
            # Apply transformations
            predictions = model.transform(df)
            
            # Extract prediction and probability
            result = predictions.select("prediction", "probability").collect()[0]
            
            return {
                "churn_prediction": int(result.prediction),
                "churn_probability": float(result.probability[1]),
                "confidence": float(max(result.probability))
            }
        
        return predict_churn
    
    def batch_scoring(self, model, input_path: str, output_path: str):
        """Batch scoring for large datasets"""
        
        # Read data
        df = self.spark.read.parquet(input_path)
        
        # Apply model
        predictions = model.transform(df)
        
        # Select relevant columns
        results = predictions.select(
            "customer_id",
            "prediction",
            "probability",
            col("probability")[1].alias("churn_probability")
        )
        
        # Write results
        results.write.mode("overwrite").parquet(output_path)
        
        return results
```

**Model Monitoring and Retraining**:
```python
class ModelMonitoringFramework:
    def __init__(self, spark: SparkSession):
        self.spark = spark
        self.model_registry = ModelRegistry()
    
    def monitor_model_performance(self, model_name: str, version: str):
        """Monitor model performance in production"""
        
        # Get recent predictions
        recent_predictions = self.spark.read.parquet(
            f"predictions/{model_name}/recent"
        ).filter(col("prediction_date") >= date_sub(current_date(), 7))
        
        # Calculate performance metrics
        if "actual_churn" in recent_predictions.columns:
            # Calculate accuracy metrics
            accuracy = recent_predictions.filter(
                col("prediction") == col("actual_churn")
            ).count() / recent_predictions.count()
            
            # Data drift detection
            drift_score = self.detect_data_drift(recent_predictions)
            
            # Model degradation check
            if accuracy < 0.85 or drift_score > 0.1:
                self.trigger_model_retraining(model_name)
        
        return {
            "accuracy": accuracy,
            "drift_score": drift_score,
            "prediction_volume": recent_predictions.count()
        }
    
    def detect_data_drift(self, current_data):
        """Detect data drift using statistical tests"""
        
        # Load reference data (training data statistics)
        reference_stats = self.spark.read.parquet("model_artifacts/reference_stats")
        
        # Calculate current data statistics
        current_stats = current_data.describe()
        
        # Compare distributions (simplified KS test)
        drift_scores = []
        for column in current_data.columns:
            if column in reference_stats.columns:
                # Calculate drift score (simplified)
                drift_score = self.calculate_drift_score(
                    reference_stats, current_stats, column
                )
                drift_scores.append(drift_score)
        
        return sum(drift_scores) / len(drift_scores) if drift_scores else 0
    
    def trigger_model_retraining(self, model_name: str):
        """Trigger automated model retraining"""
        
        # Get fresh training data
        training_data = self.spark.read.parquet("training_data/latest")
        
        # Retrain model
        pipeline = ChurnPredictionPipeline(self.spark)
        feature_pipeline = pipeline.create_feature_engineering_pipeline()
        model_pipeline = pipeline.create_model_pipeline()
        
        # Train new model
        new_model = model_pipeline.fit(training_data)
        
        # Evaluate new model
        test_data = self.spark.read.parquet("test_data/latest")
        metrics, _ = pipeline.evaluate_model(new_model, test_data)
        
        # Deploy if better than current model
        if metrics["auc"] > self.get_current_model_auc(model_name):
            new_version = self.get_next_version(model_name)
            pipeline.deploy_model(new_model, model_name, new_version)
```