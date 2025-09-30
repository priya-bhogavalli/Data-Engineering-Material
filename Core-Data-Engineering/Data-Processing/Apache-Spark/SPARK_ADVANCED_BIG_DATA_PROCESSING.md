# Spark Advanced Big Data Processing

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Performance Optimization](#-performance-optimization)
3. [Memory Tuning](#-memory-tuning)
4. [Cluster Management](#-cluster-management)
5. [Streaming Applications](#-streaming-applications)
6. [ML Pipeline Integration](#-ml-pipeline-integration)
7. [Security Configuration](#-security-configuration)
8. [Monitoring & Debugging](#-monitoring--debugging)
9. [Production Deployment](#-production-deployment)
10. [Enterprise Patterns](#-enterprise-patterns)

---

## 🎯 Overview

This document covers advanced Apache Spark concepts for production big data processing, including optimization, tuning, and enterprise deployment patterns essential for data engineering at scale.

**Prerequisites:** Complete [Spark Key Concepts](./SPARK_KEY_CONCEPTS.md) for foundational knowledge.

## 📚 Related Documents

- **[Spark Key Concepts](./SPARK_KEY_CONCEPTS.md)** - Fundamental Spark concepts and theory
- **[Spark Quick Reference](./SPARK_QUICK_REFERENCE.md)** - Essential operations and patterns
- **[Spark Interview Questions](./SPARK_INTERVIEW_QUESTIONS_COMPLETE.md)** - Interview preparation

## ⚡ Performance Optimization

### Catalyst Optimizer Deep Dive

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Create optimized SparkSession
spark = SparkSession.builder \
    .appName("AdvancedOptimization") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.sql.adaptive.skewJoin.enabled", "true") \
    .config("spark.sql.cbo.enabled", "true") \
    .config("spark.sql.statistics.histogram.enabled", "true") \
    .getOrCreate()

# Sample large datasets
customers = spark.range(1000000).select(
    col("id").alias("customer_id"),
    (rand() * 100).cast("int").alias("age"),
    when(rand() > 0.5, "Premium").otherwise("Standard").alias("tier"),
    (rand() * 50 + 18).cast("int").alias("years_active")
)

orders = spark.range(5000000).select(
    col("id").alias("order_id"),
    (rand() * 1000000).cast("int").alias("customer_id"),
    (rand() * 1000 + 10).cast("decimal(10,2)").alias("amount"),
    date_sub(current_date(), (rand() * 365).cast("int")).alias("order_date")
)

# Optimize joins with broadcast hints
small_lookup = spark.range(100).select(
    col("id").alias("category_id"),
    concat(lit("Category_"), col("id")).alias("category_name")
)

# Broadcast join for small tables
optimized_query = customers.join(
    broadcast(small_lookup.filter(col("category_id") < 50)),
    customers.customer_id % 50 == small_lookup.category_id,
    "left"
).select("customer_id", "tier", "category_name")

print("Broadcast join execution plan:")
optimized_query.explain(mode="cost")

# Bucketing for large table joins
customers.write \
    .bucketBy(10, "customer_id") \
    .sortBy("customer_id") \
    .mode("overwrite") \
    .saveAsTable("customers_bucketed")

orders.write \
    .bucketBy(10, "customer_id") \
    .sortBy("customer_id", "order_date") \
    .mode("overwrite") \
    .saveAsTable("orders_bucketed")

# Bucketed join (no shuffle required)
bucketed_join = spark.sql("""
    SELECT c.customer_id, c.tier, COUNT(o.order_id) as order_count
    FROM customers_bucketed c
    JOIN orders_bucketed o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.tier
""")

print("Bucketed join execution plan:")
bucketed_join.explain(mode="formatted")
```

### Advanced Join Optimization

```python
# Join strategies demonstration
def analyze_join_strategy(df1, df2, join_condition, join_type="inner"):
    """Analyze and optimize join strategy"""
    
    # Get table statistics
    df1_count = df1.count()
    df2_count = df2.count()
    
    print(f"Table 1 size: {df1_count:,} rows")
    print(f"Table 2 size: {df2_count:,} rows")
    
    # Determine optimal join strategy
    if min(df1_count, df2_count) < 10000:  # Broadcast threshold
        print("Recommendation: Use broadcast join")
        if df1_count < df2_count:
            result = df2.join(broadcast(df1), join_condition, join_type)
        else:
            result = df1.join(broadcast(df2), join_condition, join_type)
    else:
        print("Recommendation: Use sort-merge join with bucketing")
        result = df1.join(df2, join_condition, join_type)
    
    return result

# Skewed join handling
def handle_skewed_join(large_df, small_df, join_key):
    """Handle data skew in joins"""
    
    # Identify skewed keys
    key_distribution = large_df.groupBy(join_key).count()
    skewed_keys = key_distribution.filter(col("count") > 1000).select(join_key)
    
    # Split data into skewed and non-skewed
    skewed_data = large_df.join(skewed_keys, join_key, "inner")
    non_skewed_data = large_df.join(skewed_keys, join_key, "left_anti")
    
    # Process non-skewed data normally
    non_skewed_result = non_skewed_data.join(small_df, join_key, "inner")
    
    # Process skewed data with salting
    salted_large = skewed_data.withColumn(
        "salt", (rand() * 10).cast("int")
    ).withColumn(
        "salted_key", concat(col(join_key), lit("_"), col("salt"))
    )
    
    salted_small = small_df.withColumn("salt", explode(array([lit(i) for i in range(10)]))) \
        .withColumn("salted_key", concat(col(join_key), lit("_"), col("salt")))
    
    skewed_result = salted_large.join(salted_small, "salted_key", "inner") \
        .drop("salt", "salted_key")
    
    # Union results
    final_result = non_skewed_result.union(skewed_result)
    
    return final_result

# Example usage
large_table = spark.range(1000000).select(
    col("id").alias("user_id"),
    when(col("id") % 100 == 0, 1).otherwise((rand() * 1000).cast("int")).alias("category_id")
)

small_table = spark.range(1000).select(
    col("id").alias("category_id"),
    concat(lit("Category_"), col("id")).alias("name")
)

# Handle skewed join
optimized_result = handle_skewed_join(large_table, small_table, "category_id")
print(f"Optimized join result count: {optimized_result.count()}")
```

### Predicate Pushdown and Projection Pruning

```python
# Demonstrate predicate pushdown
def demonstrate_pushdown_optimization():
    """Show how Spark optimizes queries with predicate pushdown"""
    
    # Create partitioned data
    sales_data = spark.range(1000000).select(
        col("id").alias("sale_id"),
        (col("id") % 12 + 1).alias("month"),
        (col("id") % 4 + 2020).alias("year"),
        (rand() * 1000).cast("decimal(10,2)").alias("amount"),
        (rand() * 100).cast("int").alias("product_id")
    )
    
    # Write partitioned data
    sales_data.write \
        .partitionBy("year", "month") \
        .mode("overwrite") \
        .parquet("sales_partitioned")
    
    # Read with predicate pushdown
    filtered_sales = spark.read.parquet("sales_partitioned") \
        .filter((col("year") == 2023) & (col("month").isin([6, 7, 8]))) \
        .select("sale_id", "amount", "product_id")  # Projection pruning
    
    print("Query with predicate pushdown and projection pruning:")
    filtered_sales.explain(True)
    
    # Compare with non-optimized query
    non_optimized = spark.read.parquet("sales_partitioned") \
        .select("*") \
        .filter((col("year") == 2023) & (col("month").isin([6, 7, 8])))
    
    print("\nNon-optimized query plan:")
    non_optimized.explain(True)

# demonstrate_pushdown_optimization()
```

## 🧠 Memory Tuning

### Memory Management Configuration

```python
# Memory configuration for different workloads
def configure_spark_memory(workload_type="general"):
    """Configure Spark memory settings for different workloads"""
    
    configs = {
        "general": {
            "spark.executor.memory": "4g",
            "spark.executor.memoryFraction": "0.8",
            "spark.sql.execution.arrow.pyspark.enabled": "true",
            "spark.sql.adaptive.coalescePartitions.enabled": "true"
        },
        "memory_intensive": {
            "spark.executor.memory": "8g",
            "spark.executor.memoryFraction": "0.9",
            "spark.sql.execution.arrow.maxRecordsPerBatch": "20000",
            "spark.sql.inMemoryColumnarStorage.compressed": "true"
        },
        "streaming": {
            "spark.executor.memory": "2g",
            "spark.streaming.backpressure.enabled": "true",
            "spark.sql.streaming.metricsEnabled": "true",
            "spark.sql.adaptive.enabled": "false"  # Not recommended for streaming
        }
    }
    
    return configs.get(workload_type, configs["general"])

# Dynamic memory allocation
def optimize_memory_usage(df, operation_type="transform"):
    """Optimize memory usage based on operation type"""
    
    # Estimate memory requirements
    row_count = df.count()
    column_count = len(df.columns)
    estimated_size_mb = (row_count * column_count * 8) / (1024 * 1024)  # Rough estimate
    
    print(f"Estimated DataFrame size: {estimated_size_mb:.2f} MB")
    
    if operation_type == "join" and estimated_size_mb > 1000:
        # Use disk-based operations for large joins
        df = df.persist(StorageLevel.MEMORY_AND_DISK_SER)
        print("Using MEMORY_AND_DISK_SER storage level")
    elif operation_type == "aggregation" and estimated_size_mb < 500:
        # Cache in memory for aggregations on smaller datasets
        df = df.cache()
        print("Caching in memory for aggregation")
    elif operation_type == "transform":
        # No caching for simple transformations
        print("No caching for simple transformations")
    
    return df

# Memory monitoring
def monitor_memory_usage(spark_context):
    """Monitor current memory usage"""
    
    status = spark_context.statusTracker()
    
    print("Executor Memory Status:")
    for executor in status.getExecutorInfos():
        print(f"Executor {executor.executorId}:")
        print(f"  Host: {executor.host}")
        print(f"  Active Tasks: {executor.activeTasks}")
        print(f"  Max Memory: {executor.maxMemory / (1024**3):.2f} GB")
        print(f"  Memory Used: {executor.memoryUsed / (1024**3):.2f} GB")
        print(f"  Disk Used: {executor.diskUsed / (1024**3):.2f} GB")

# Example usage
sample_df = spark.range(100000).select(
    col("id"),
    (rand() * 1000).alias("value1"),
    (rand() * 1000).alias("value2")
)

optimized_df = optimize_memory_usage(sample_df, "aggregation")
result = optimized_df.groupBy().agg(
    avg("value1").alias("avg_value1"),
    sum("value2").alias("sum_value2")
).collect()

print(f"Aggregation result: {result}")
```

### Garbage Collection Tuning

```python
# GC tuning configurations
gc_configs = {
    "g1gc_optimized": {
        "spark.executor.extraJavaOptions": 
            "-XX:+UseG1GC "
            "-XX:MaxGCPauseMillis=200 "
            "-XX:G1HeapRegionSize=16m "
            "-XX:+G1UseAdaptiveIHOP "
            "-XX:G1MixedGCCountTarget=8 "
            "-XX:InitiatingHeapOccupancyPercent=35"
    },
    "parallel_gc": {
        "spark.executor.extraJavaOptions":
            "-XX:+UseParallelGC "
            "-XX:ParallelGCThreads=4 "
            "-XX:+UseParallelOldGC"
    },
    "cms_gc": {
        "spark.executor.extraJavaOptions":
            "-XX:+UseConcMarkSweepGC "
            "-XX:+CMSIncrementalMode "
            "-XX:CMSInitiatingOccupancyFraction=70"
    }
}

def create_gc_optimized_session(gc_type="g1gc_optimized"):
    """Create Spark session with GC optimization"""
    
    builder = SparkSession.builder.appName("GC_Optimized")
    
    # Apply GC configurations
    for key, value in gc_configs[gc_type].items():
        builder = builder.config(key, value)
    
    # Additional memory configurations
    builder = builder.config("spark.executor.memory", "4g") \
                    .config("spark.driver.memory", "2g") \
                    .config("spark.sql.execution.arrow.pyspark.enabled", "true")
    
    return builder.getOrCreate()

# Memory leak detection
def detect_memory_leaks(df_operations):
    """Detect potential memory leaks in DataFrame operations"""
    
    initial_memory = spark.sparkContext.statusTracker().getExecutorInfos()[0].memoryUsed
    
    for i, operation in enumerate(df_operations):
        # Execute operation
        result = operation()
        
        # Force garbage collection
        spark.sparkContext._jvm.System.gc()
        
        # Check memory usage
        current_memory = spark.sparkContext.statusTracker().getExecutorInfos()[0].memoryUsed
        memory_increase = current_memory - initial_memory
        
        print(f"Operation {i+1}: Memory increase = {memory_increase / (1024**2):.2f} MB")
        
        # Clean up intermediate results
        if hasattr(result, 'unpersist'):
            result.unpersist()

# Example memory leak detection
def create_test_operations():
    """Create test operations for memory leak detection"""
    
    base_df = spark.range(10000)
    
    operations = [
        lambda: base_df.select("*").cache(),
        lambda: base_df.filter(col("id") > 5000).cache(),
        lambda: base_df.groupBy().count(),
        lambda: base_df.repartition(10).cache()
    ]
    
    return operations

# test_ops = create_test_operations()
# detect_memory_leaks(test_ops)
```

## 🏗️ Cluster Management

### Dynamic Resource Allocation

```python
# Dynamic allocation configuration
dynamic_allocation_config = {
    "spark.dynamicAllocation.enabled": "true",
    "spark.dynamicAllocation.minExecutors": "1",
    "spark.dynamicAllocation.maxExecutors": "20",
    "spark.dynamicAllocation.initialExecutors": "3",
    "spark.dynamicAllocation.executorIdleTimeout": "60s",
    "spark.dynamicAllocation.cachedExecutorIdleTimeout": "300s",
    "spark.dynamicAllocation.schedulerBacklogTimeout": "1s",
    "spark.shuffle.service.enabled": "true"
}

def create_dynamic_spark_session():
    """Create Spark session with dynamic allocation"""
    
    builder = SparkSession.builder.appName("DynamicAllocation")
    
    for key, value in dynamic_allocation_config.items():
        builder = builder.config(key, value)
    
    return builder.getOrCreate()

# Resource monitoring
class ResourceMonitor:
    def __init__(self, spark_context):
        self.sc = spark_context
        self.metrics_history = []
    
    def collect_metrics(self):
        """Collect current resource metrics"""
        status = self.sc.statusTracker()
        
        metrics = {
            "timestamp": datetime.now(),
            "active_jobs": len(status.getActiveJobIds()),
            "active_stages": len(status.getActiveStageIds()),
            "executor_count": len(status.getExecutorInfos()),
            "total_cores": sum(e.totalCores for e in status.getExecutorInfos()),
            "total_memory_gb": sum(e.maxMemory for e in status.getExecutorInfos()) / (1024**3)
        }
        
        self.metrics_history.append(metrics)
        return metrics
    
    def get_resource_utilization(self):
        """Calculate resource utilization over time"""
        if len(self.metrics_history) < 2:
            return "Insufficient data"
        
        recent_metrics = self.metrics_history[-10:]  # Last 10 measurements
        
        avg_executors = sum(m["executor_count"] for m in recent_metrics) / len(recent_metrics)
        avg_cores = sum(m["total_cores"] for m in recent_metrics) / len(recent_metrics)
        
        return {
            "avg_executors": avg_executors,
            "avg_cores": avg_cores,
            "utilization_trend": "stable"  # Would implement trend analysis
        }

# Cluster health monitoring
def monitor_cluster_health(spark_session):
    """Monitor cluster health and performance"""
    
    sc = spark_session.sparkContext
    
    # Check executor health
    executors = sc.statusTracker().getExecutorInfos()
    healthy_executors = [e for e in executors if e.activeTasks >= 0]
    
    print(f"Healthy executors: {len(healthy_executors)}/{len(executors)}")
    
    # Check for failed tasks
    app_status = sc.statusTracker().getApplicationInfo()
    print(f"Application attempt: {app_status.attemptId}")
    
    # Resource utilization
    total_cores = sum(e.totalCores for e in executors)
    active_tasks = sum(e.activeTasks for e in executors)
    
    utilization = (active_tasks / total_cores * 100) if total_cores > 0 else 0
    print(f"CPU utilization: {utilization:.1f}%")
    
    return {
        "healthy_executors": len(healthy_executors),
        "total_executors": len(executors),
        "cpu_utilization": utilization
    }

# Example usage
# monitor = ResourceMonitor(spark.sparkContext)
# health_status = monitor_cluster_health(spark)
# print(f"Cluster health: {health_status}")
```

### Multi-Cluster Management

```python
# Multi-cluster configuration
class MultiClusterManager:
    def __init__(self):
        self.clusters = {}
    
    def register_cluster(self, name, config):
        """Register a new cluster configuration"""
        self.clusters[name] = config
    
    def get_optimal_cluster(self, workload_type, data_size_gb):
        """Select optimal cluster based on workload characteristics"""
        
        if workload_type == "streaming" and data_size_gb < 10:
            return "streaming_cluster"
        elif workload_type == "batch" and data_size_gb > 100:
            return "large_batch_cluster"
        elif workload_type == "interactive":
            return "interactive_cluster"
        else:
            return "general_cluster"
    
    def create_session_for_cluster(self, cluster_name):
        """Create Spark session for specific cluster"""
        
        if cluster_name not in self.clusters:
            raise ValueError(f"Unknown cluster: {cluster_name}")
        
        config = self.clusters[cluster_name]
        builder = SparkSession.builder.appName(f"App_{cluster_name}")
        
        for key, value in config.items():
            builder = builder.config(key, value)
        
        return builder.getOrCreate()

# Register different cluster configurations
cluster_manager = MultiClusterManager()

cluster_manager.register_cluster("streaming_cluster", {
    "spark.master": "yarn",
    "spark.executor.instances": "5",
    "spark.executor.cores": "2",
    "spark.executor.memory": "2g",
    "spark.streaming.backpressure.enabled": "true"
})

cluster_manager.register_cluster("large_batch_cluster", {
    "spark.master": "yarn",
    "spark.executor.instances": "50",
    "spark.executor.cores": "4",
    "spark.executor.memory": "8g",
    "spark.sql.adaptive.enabled": "true"
})

cluster_manager.register_cluster("interactive_cluster", {
    "spark.master": "yarn",
    "spark.executor.instances": "10",
    "spark.executor.cores": "2",
    "spark.executor.memory": "4g",
    "spark.sql.execution.arrow.pyspark.enabled": "true"
})

# Usage example
optimal_cluster = cluster_manager.get_optimal_cluster("batch", 150)
print(f"Optimal cluster for large batch job: {optimal_cluster}")
```

## 🌊 Streaming Applications

### Structured Streaming Patterns

```python
from pyspark.sql.streaming import StreamingQuery
from pyspark.sql.functions import window, current_timestamp

# Advanced streaming patterns
def create_streaming_pipeline():
    """Create advanced streaming data pipeline"""
    
    # Read from Kafka (simulated with rate source)
    streaming_df = spark.readStream \
        .format("rate") \
        .option("rowsPerSecond", 1000) \
        .option("numPartitions", 4) \
        .load()
    
    # Add processing timestamp
    enriched_df = streaming_df.select(
        col("timestamp").alias("event_time"),
        col("value").alias("sensor_id"),
        current_timestamp().alias("processing_time"),
        (rand() * 100).alias("temperature"),
        (rand() * 50 + 20).alias("humidity")
    )
    
    # Windowed aggregations
    windowed_stats = enriched_df \
        .withWatermark("event_time", "10 minutes") \
        .groupBy(
            window(col("event_time"), "5 minutes", "1 minute"),
            col("sensor_id")
        ) \
        .agg(
            avg("temperature").alias("avg_temp"),
            max("temperature").alias("max_temp"),
            min("temperature").alias("min_temp"),
            count("*").alias("reading_count")
        )
    
    return windowed_stats

# Stream monitoring and alerting
class StreamMonitor:
    def __init__(self):
        self.alert_thresholds = {
            "input_rate_min": 100,
            "processing_delay_max": 30000,  # milliseconds
            "batch_duration_max": 10000
        }
    
    def check_stream_health(self, query: StreamingQuery):
        """Monitor streaming query health"""
        
        progress = query.lastProgress
        if not progress:
            return {"status": "no_progress", "alerts": []}
        
        alerts = []
        
        # Check input rate
        input_rate = progress.get("inputRowsPerSecond", 0)
        if input_rate < self.alert_thresholds["input_rate_min"]:
            alerts.append(f"Low input rate: {input_rate}")
        
        # Check processing delay
        batch_duration = progress.get("batchDuration", 0)
        if batch_duration > self.alert_thresholds["batch_duration_max"]:
            alerts.append(f"High batch duration: {batch_duration}ms")
        
        # Check for errors
        if "exception" in progress:
            alerts.append(f"Stream error: {progress['exception']}")
        
        return {
            "status": "healthy" if not alerts else "unhealthy",
            "alerts": alerts,
            "metrics": {
                "input_rate": input_rate,
                "batch_duration": batch_duration,
                "processed_rows": progress.get("numInputRows", 0)
            }
        }

# Exactly-once processing with checkpointing
def create_exactly_once_stream():
    """Create streaming query with exactly-once semantics"""
    
    streaming_data = spark.readStream \
        .format("rate") \
        .option("rowsPerSecond", 100) \
        .load()
    
    processed_data = streaming_data.select(
        col("timestamp"),
        col("value"),
        (col("value") * 2).alias("doubled_value")
    )
    
    # Write with checkpointing for exactly-once processing
    query = processed_data.writeStream \
        .outputMode("append") \
        .format("console") \
        .option("checkpointLocation", "/tmp/checkpoint") \
        .option("truncate", "false") \
        .trigger(processingTime="10 seconds") \
        .start()
    
    return query

# Example usage
# streaming_pipeline = create_streaming_pipeline()
# monitor = StreamMonitor()

# Start streaming query (commented to avoid actual streaming)
# query = streaming_pipeline.writeStream \
#     .outputMode("update") \
#     .format("console") \
#     .start()

# Monitor stream health
# health_status = monitor.check_stream_health(query)
# print(f"Stream health: {health_status}")
```

### Stream Processing Patterns

```python
# Complex event processing
def complex_event_processing():
    """Implement complex event processing patterns"""
    
    # Simulate event stream
    events_df = spark.readStream \
        .format("rate") \
        .option("rowsPerSecond", 500) \
        .load() \
        .select(
            col("timestamp").alias("event_time"),
            (col("value") % 1000).alias("user_id"),
            when(col("value") % 4 == 0, "login")
            .when(col("value") % 4 == 1, "purchase")
            .when(col("value") % 4 == 2, "view")
            .otherwise("logout").alias("event_type"),
            (rand() * 1000).alias("amount")
        )
    
    # Pattern detection: Find users with purchase after login within 5 minutes
    user_sessions = events_df \
        .withWatermark("event_time", "10 minutes") \
        .groupBy(
            col("user_id"),
            window(col("event_time"), "5 minutes")
        ) \
        .agg(
            collect_list("event_type").alias("events"),
            sum(when(col("event_type") == "purchase", col("amount")).otherwise(0)).alias("total_spent")
        ) \
        .filter(
            array_contains(col("events"), "login") & 
            array_contains(col("events"), "purchase")
        )
    
    return user_sessions

# State management in streaming
def stateful_streaming_processing():
    """Implement stateful processing with mapGroupsWithState"""
    
    # This would require Scala/Java implementation for full functionality
    # In PySpark, we use groupBy with window functions for similar results
    
    events_df = spark.readStream \
        .format("rate") \
        .option("rowsPerSecond", 100) \
        .load() \
        .select(
            col("timestamp").alias("event_time"),
            (col("value") % 100).alias("session_id"),
            (rand() * 10).cast("int").alias("action_type")
        )
    
    # Session aggregation with state
    session_stats = events_df \
        .withWatermark("event_time", "30 minutes") \
        .groupBy(
            col("session_id"),
            window(col("event_time"), "30 minutes", "5 minutes")
        ) \
        .agg(
            count("*").alias("event_count"),
            countDistinct("action_type").alias("unique_actions"),
            min("event_time").alias("session_start"),
            max("event_time").alias("session_end")
        )
    
    return session_stats

# Stream-to-stream joins
def stream_to_stream_join():
    """Implement stream-to-stream joins with watermarks"""
    
    # Stream 1: User actions
    actions_stream = spark.readStream \
        .format("rate") \
        .option("rowsPerSecond", 200) \
        .load() \
        .select(
            col("timestamp").alias("action_time"),
            (col("value") % 1000).alias("user_id"),
            lit("click").alias("action_type")
        )
    
    # Stream 2: User purchases
    purchases_stream = spark.readStream \
        .format("rate") \
        .option("rowsPerSecond", 50) \
        .load() \
        .select(
            col("timestamp").alias("purchase_time"),
            (col("value") % 1000).alias("user_id"),
            (rand() * 100 + 10).alias("amount")
        )
    
    # Join streams with watermarks
    joined_stream = actions_stream \
        .withWatermark("action_time", "10 minutes") \
        .join(
            purchases_stream.withWatermark("purchase_time", "10 minutes"),
            expr("""
                user_id = user_id AND
                purchase_time >= action_time AND
                purchase_time <= action_time + interval 5 minutes
            """),
            "inner"
        )
    
    return joined_stream

# Example usage
# cep_stream = complex_event_processing()
# stateful_stream = stateful_streaming_processing()
# joined_stream = stream_to_stream_join()

print("Advanced streaming patterns configured")
```

This advanced Spark documentation provides production-ready patterns for performance optimization, memory tuning, cluster management, and streaming applications essential for enterprise big data processing.