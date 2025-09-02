# Databricks Complete Guide for Data Engineering

## 🎯 What is Databricks?

Databricks is a **unified analytics platform** built on Apache Spark that combines data engineering, data science, and machine learning in a collaborative environment. It provides a managed Spark service with optimizations for cloud environments.

### Key Characteristics
- **Unified Platform**: Data engineering, ML, and analytics in one place
- **Collaborative**: Shared notebooks and workspaces
- **Optimized Spark**: Enhanced performance with Delta Lake
- **Multi-Cloud**: Available on AWS, Azure, and GCP
- **Serverless**: Managed infrastructure and auto-scaling

## 🏗️ Architecture Overview

### Databricks Architecture
```
┌─────────────────────────────────────────────────────────┐
│                 Databricks Workspace                    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│  │  Notebooks  │ │    Jobs     │ │   ML Flow   │       │
│  └─────────────┘ └─────────────┘ └─────────────┘       │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                   Compute Layer                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│  │All-Purpose  │ │Job Clusters │ │SQL Warehouse│       │
│  │ Clusters    │ │             │ │             │       │
│  └─────────────┘ └─────────────┘ └─────────────┘       │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                   Storage Layer                         │
│           Delta Lake + Cloud Storage                    │
└─────────────────────────────────────────────────────────┘
```

**Workspace**: Collaborative environment for notebooks, jobs, and ML
**Compute**: Managed Spark clusters with auto-scaling
**Storage**: Delta Lake for ACID transactions and data versioning

## 💾 Core Concepts

### 1. Clusters
```python
# Cluster configuration best practices
cluster_config = {
    "cluster_name": "production-etl-cluster",
    "spark_version": "11.3.x-scala2.12",  # Use LTS versions
    "node_type_id": "i3.xlarge",
    "driver_node_type_id": "i3.xlarge",
    "num_workers": 2,
    "autoscale": {
        "min_workers": 1,
        "max_workers": 8
    },
    "auto_termination_minutes": 30,
    "enable_elastic_disk": True
}

# Optimal Spark configurations
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.databricks.delta.optimizeWrite.enabled", "true")
spark.conf.set("spark.databricks.delta.autoCompact.enabled", "true")
```

### 2. Delta Lake
```python
# Create optimized Delta table
spark.sql("""
    CREATE TABLE IF NOT EXISTS production.sales.orders (
        order_id BIGINT,
        customer_id BIGINT,
        order_date DATE,
        order_amount DECIMAL(10,2),
        product_category STRING,
        region STRING,
        created_at TIMESTAMP
    ) USING DELTA
    PARTITIONED BY (order_date, region)
    TBLPROPERTIES (
        'delta.autoOptimize.optimizeWrite' = 'true',
        'delta.autoOptimize.autoCompact' = 'true',
        'delta.deletedFileRetentionDuration' = 'interval 7 days'
    )
""")

# ACID transactions with Delta Lake
from delta.tables import DeltaTable

# Merge operation (UPSERT)
delta_table = DeltaTable.forPath(spark, "/delta/customers")

delta_table.alias("target").merge(
    source_df.alias("source"),
    "target.customer_id = source.customer_id"
).whenMatchedUpdate(set={
    "customer_name": "source.customer_name",
    "updated_at": "current_timestamp()"
}).whenNotMatchedInsert(values={
    "customer_id": "source.customer_id",
    "customer_name": "source.customer_name",
    "created_at": "current_timestamp()"
}).execute()

# Time travel with Delta Lake
# Query historical data
historical_df = spark.read.format("delta").option("timestampAsOf", "2024-01-01").load("/delta/sales")

# Query by version
version_df = spark.read.format("delta").option("versionAsOf", 5).load("/delta/sales")
```

### 3. Medallion Architecture
```python
# Bronze Layer - Raw data ingestion
def bronze_layer_processing(source_path, bronze_path):
    """Ingest raw data with minimal transformation"""
    
    raw_df = spark.read.format("json").load(source_path)
    
    # Add metadata columns
    bronze_df = raw_df.withColumn("ingestion_timestamp", current_timestamp()) \
                     .withColumn("source_file", input_file_name())
    
    # Write to Bronze layer
    bronze_df.write.format("delta").mode("append").save(bronze_path)
    
    return bronze_df

# Silver Layer - Cleaned and validated data
def silver_layer_processing(bronze_path, silver_path):
    """Clean and validate data"""
    
    bronze_df = spark.read.format("delta").load(bronze_path)
    
    # Data cleaning and validation
    silver_df = bronze_df.filter(col("order_amount") > 0) \
                         .filter(col("customer_id").isNotNull()) \
                         .withColumn("order_date", to_date(col("order_timestamp"))) \
                         .dropDuplicates(["order_id"])
    
    # Write to Silver layer
    silver_df.write.format("delta").mode("overwrite").save(silver_path)
    
    return silver_df

# Gold Layer - Business aggregations
def gold_layer_processing(silver_path, gold_path):
    """Create business-ready aggregations"""
    
    silver_df = spark.read.format("delta").load(silver_path)
    
    # Business aggregations
    gold_df = silver_df.groupBy("customer_id", "order_date") \
                      .agg(
                          sum("order_amount").alias("daily_total"),
                          count("order_id").alias("order_count"),
                          avg("order_amount").alias("avg_order_value")
                      )
    
    # Write to Gold layer
    gold_df.write.format("delta").mode("overwrite").save(gold_path)
    
    return gold_df
```

## 🔧 Data Engineering Workflows

### 1. ETL Pipeline Design
```python
from pyspark.sql.functions import *
from pyspark.sql.types import *

def create_robust_etl_pipeline():
    """Production-ready ETL pipeline with error handling"""
    
    def extract_data(source_config):
        """Extract data from various sources"""
        
        if source_config["type"] == "jdbc":
            df = spark.read.format("jdbc") \
                .option("url", source_config["url"]) \
                .option("dbtable", source_config["table"]) \
                .option("user", dbutils.secrets.get("db", "username")) \
                .option("password", dbutils.secrets.get("db", "password")) \
                .load()
        
        elif source_config["type"] == "kafka":
            df = spark.readStream.format("kafka") \
                .option("kafka.bootstrap.servers", source_config["servers"]) \
                .option("subscribe", source_config["topic"]) \
                .load()
        
        elif source_config["type"] == "files":
            df = spark.read.format(source_config["format"]) \
                .load(source_config["path"])
        
        return df
    
    def transform_data(df, transformations):
        """Apply business transformations"""
        
        for transform in transformations:
            if transform["type"] == "filter":
                df = df.filter(transform["condition"])
            
            elif transform["type"] == "aggregate":
                df = df.groupBy(*transform["group_by"]) \
                      .agg(*[eval(agg) for agg in transform["aggregations"]])
            
            elif transform["type"] == "join":
                right_df = spark.table(transform["right_table"])
                df = df.join(right_df, transform["join_condition"], transform["join_type"])
        
        return df
    
    def load_data(df, target_config):
        """Load data to target with proper error handling"""
        
        try:
            if target_config["mode"] == "streaming":
                query = df.writeStream \
                    .format("delta") \
                    .outputMode("append") \
                    .option("checkpointLocation", target_config["checkpoint"]) \
                    .start(target_config["path"])
                
                return query
            
            else:
                df.write.format("delta") \
                    .mode(target_config["mode"]) \
                    .save(target_config["path"])
                
                return True
                
        except Exception as e:
            # Log error and handle gracefully
            error_df = spark.createDataFrame([{
                "pipeline": "etl_pipeline",
                "error": str(e),
                "timestamp": current_timestamp()
            }])
            
            error_df.write.format("delta").mode("append").save("/delta/monitoring/errors")
            raise e
    
    return extract_data, transform_data, load_data
```

### 2. Streaming Data Processing
```python
def create_streaming_pipeline():
    """Real-time streaming data processing"""
    
    # Read from Kafka
    streaming_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "orders") \
        .option("startingOffsets", "latest") \
        .load()
    
    # Parse JSON data
    schema = StructType([
        StructField("order_id", StringType(), True),
        StructField("customer_id", StringType(), True),
        StructField("order_amount", DoubleType(), True),
        StructField("order_timestamp", TimestampType(), True)
    ])
    
    parsed_df = streaming_df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")
    
    # Apply transformations
    enriched_df = parsed_df.withColumn("processing_time", current_timestamp()) \
                          .withColumn("order_date", to_date(col("order_timestamp")))
    
    # Write to Delta Lake with streaming
    query = enriched_df.writeStream \
        .format("delta") \
        .outputMode("append") \
        .option("checkpointLocation", "/delta/checkpoints/orders") \
        .trigger(processingTime="30 seconds") \
        .start("/delta/streaming/orders")
    
    return query

# Monitor streaming queries
def monitor_streaming_queries():
    """Monitor active streaming queries"""
    
    active_streams = spark.streams.active
    
    for stream in active_streams:
        print(f"Stream ID: {stream.id}")
        print(f"Status: {stream.status}")
        print(f"Progress: {stream.lastProgress}")
    
    return active_streams
```

## ⚡ Performance Optimization

### 1. Query Optimization
```python
def optimize_queries():
    """Query optimization techniques"""
    
    # Use broadcast joins for small tables
    small_table = spark.table("dim_products").filter(col("is_active") == True)
    large_table = spark.table("fact_sales")
    
    # Explicit broadcast hint
    result = large_table.join(broadcast(small_table), "product_id")
    
    # Predicate pushdown
    optimized_query = spark.sql("""
        SELECT s.*, p.product_name
        FROM fact_sales s
        JOIN dim_products p ON s.product_id = p.product_id
        WHERE s.order_date >= '2024-01-01'  -- Filter early
          AND p.is_active = true
    """)
    
    # Cache frequently accessed data
    dim_customers = spark.table("dim_customers").cache()
    
    return result, optimized_query, dim_customers

# Delta Lake optimization
def optimize_delta_tables():
    """Optimize Delta tables for better performance"""
    
    # Compact small files
    spark.sql("OPTIMIZE sales_table")
    
    # Z-order for better data skipping
    spark.sql("OPTIMIZE sales_table ZORDER BY (customer_id, order_date)")
    
    # Vacuum old files (7 days retention)
    spark.sql("VACUUM sales_table RETAIN 168 HOURS")
    
    # Analyze table statistics
    spark.sql("ANALYZE TABLE sales_table COMPUTE STATISTICS FOR ALL COLUMNS")
```

### 2. Resource Management
```python
def manage_cluster_resources():
    """Optimize cluster resource utilization"""
    
    # Monitor cluster metrics
    cluster_metrics = spark.sql("""
        SELECT 
            cluster_id,
            avg(cpu_utilization) as avg_cpu,
            avg(memory_utilization) as avg_memory,
            max(disk_utilization) as max_disk
        FROM system.compute.cluster_metrics
        WHERE timestamp >= current_timestamp() - INTERVAL 1 HOUR
        GROUP BY cluster_id
    """)
    
    # Auto-scaling recommendations
    def get_scaling_recommendations(metrics_df):
        recommendations = metrics_df.withColumn(
            "recommendation",
            when(col("avg_cpu") < 0.3, "Consider smaller instance type")
            .when(col("avg_cpu") > 0.8, "Consider larger instance type")
            .when(col("avg_memory") > 0.9, "Add more memory or workers")
            .otherwise("Current sizing is appropriate")
        )
        
        return recommendations
    
    return cluster_metrics, get_scaling_recommendations
```

## 🔒 Security & Governance

### 1. Unity Catalog
```python
def setup_unity_catalog():
    """Implement Unity Catalog for governance"""
    
    # Create catalog and schema
    spark.sql("CREATE CATALOG IF NOT EXISTS production")
    spark.sql("CREATE SCHEMA IF NOT EXISTS production.sales")
    
    # Row-level security
    spark.sql("""
        CREATE FUNCTION mask_sensitive_data(user_role STRING, data STRING)
        RETURNS STRING
        LANGUAGE SQL
        RETURN CASE 
            WHEN user_role IN ('admin', 'data_engineer') THEN data
            WHEN user_role = 'analyst' THEN CONCAT(LEFT(data, 3), '***')
            ELSE '***'
        END
    """)
    
    # Secure view with row-level security
    spark.sql("""
        CREATE VIEW secure_customers AS
        SELECT 
            customer_id,
            customer_name,
            mask_sensitive_data(current_user(), email) as email,
            registration_date
        FROM customers
        WHERE 
            CASE 
                WHEN is_member('data_engineers') THEN TRUE
                WHEN is_member('analysts') AND region = 'US' THEN TRUE
                ELSE FALSE
            END
    """)

def manage_secrets():
    """Secure secrets management"""
    
    # Use secret scopes instead of hardcoding
    def get_database_connection():
        connection_params = {
            "url": "jdbc:postgresql://hostname:5432/database",
            "user": dbutils.secrets.get("database", "username"),
            "password": dbutils.secrets.get("database", "password"),
            "driver": "org.postgresql.Driver"
        }
        return connection_params
    
    return get_database_connection
```

### 2. Data Quality Framework
```python
def implement_data_quality():
    """Comprehensive data quality validation"""
    
    def validate_data_quality(df, table_name, rules):
        """Generic data quality validation"""
        
        results = []
        total_records = df.count()
        
        for rule_name, rule_condition in rules.items():
            if rule_name == "null_check":
                for column in rule_condition:
                    null_count = df.filter(col(column).isNull()).count()
                    null_percentage = (null_count / total_records) * 100
                    
                    results.append({
                        "table": table_name,
                        "rule": f"null_check_{column}",
                        "passed": null_percentage < 5,
                        "value": null_percentage,
                        "threshold": 5
                    })
            
            elif rule_name == "duplicate_check":
                duplicate_count = total_records - df.dropDuplicates(rule_condition).count()
                results.append({
                    "table": table_name,
                    "rule": "duplicate_check",
                    "passed": duplicate_count == 0,
                    "value": duplicate_count,
                    "threshold": 0
                })
        
        return results
    
    # Define quality rules
    quality_rules = {
        "null_check": ["customer_id", "order_date", "order_amount"],
        "duplicate_check": ["order_id"],
        "range_check": {
            "order_amount": (0, 100000),
            "customer_id": (1, 999999999)
        }
    }
    
    return validate_data_quality, quality_rules
```

## 🚀 MLOps Integration

### 1. ML Pipeline
```python
def create_ml_pipeline():
    """Integrate ML workflows with data engineering"""
    
    import mlflow
    import mlflow.spark
    from pyspark.ml import Pipeline
    from pyspark.ml.feature import VectorAssembler, StandardScaler
    from pyspark.ml.regression import LinearRegression
    
    # Feature engineering
    def prepare_features(df):
        feature_cols = ["customer_age", "order_history", "avg_order_value"]
        
        assembler = VectorAssembler(
            inputCols=feature_cols,
            outputCol="features"
        )
        
        scaler = StandardScaler(
            inputCol="features",
            outputCol="scaled_features"
        )
        
        return assembler, scaler
    
    # Model training
    def train_model(df):
        with mlflow.start_run():
            assembler, scaler = prepare_features(df)
            lr = LinearRegression(
                featuresCol="scaled_features",
                labelCol="customer_lifetime_value"
            )
            
            pipeline = Pipeline(stages=[assembler, scaler, lr])
            model = pipeline.fit(df)
            
            # Log model
            mlflow.spark.log_model(model, "customer_ltv_model")
            
            return model
    
    return prepare_features, train_model

# Model serving
def serve_ml_model():
    """Serve ML models for batch and real-time inference"""
    
    # Load model
    model = mlflow.spark.load_model("models:/customer_ltv_model/production")
    
    # Batch inference
    def batch_inference(input_df):
        predictions = model.transform(input_df)
        return predictions.select("customer_id", "prediction")
    
    # Real-time inference with streaming
    def streaming_inference(streaming_df):
        predictions = model.transform(streaming_df)
        
        query = predictions.writeStream \
            .format("delta") \
            .outputMode("append") \
            .option("checkpointLocation", "/delta/checkpoints/predictions") \
            .start("/delta/ml/predictions")
        
        return query
    
    return batch_inference, streaming_inference
```

## 💰 Cost Optimization

### 1. Resource Management
```python
def optimize_costs():
    """Cost optimization strategies"""
    
    # Cluster auto-termination settings
    cluster_configs = {
        "interactive_clusters": {
            "auto_termination_minutes": 30,
            "enable_elastic_disk": True
        },
        "job_clusters": {
            "auto_termination_minutes": 0,  # Terminate after job
            "spot_instances": True
        }
    }
    
    # Storage lifecycle management
    def implement_data_lifecycle():
        lifecycle_policies = {
            "bronze_layer": {"retention_days": 90},
            "silver_layer": {"retention_days": 365},
            "gold_layer": {"retention_days": 2555}  # 7 years
        }
        
        return lifecycle_policies
    
    # Monitor usage and costs
    def monitor_costs():
        cost_report = spark.sql("""
            SELECT 
                cluster_tags.team as team_name,
                SUM(dbu_hours * dbu_rate) as estimated_cost,
                SUM(dbu_hours) as total_dbu_hours
            FROM system.billing.usage
            WHERE usage_date >= current_date() - 30
            GROUP BY cluster_tags.team
            ORDER BY estimated_cost DESC
        """)
        
        return cost_report
    
    return cluster_configs, implement_data_lifecycle, monitor_costs
```

## 🎯 Best Practices Summary

### 1. Development Best Practices
- **Use version control** for notebooks and code
- **Implement proper error handling** and logging
- **Design idempotent jobs** that can be safely re-run
- **Use Delta Lake** for ACID transactions and data versioning
- **Implement data quality checks** at each layer

### 2. Performance Best Practices
- **Right-size clusters** based on workload requirements
- **Use auto-scaling** and auto-termination
- **Optimize Delta tables** with OPTIMIZE and ZORDER
- **Cache frequently accessed data**
- **Use broadcast joins** for small tables

### 3. Security Best Practices
- **Use Unity Catalog** for centralized governance
- **Implement row and column-level security**
- **Store secrets securely** using secret scopes
- **Enable audit logging** and monitoring
- **Follow principle of least privilege**

### 4. Cost Optimization Best Practices
- **Use job clusters** for production workloads
- **Enable auto-termination** for interactive clusters
- **Implement data lifecycle policies**
- **Monitor resource utilization** regularly
- **Use spot instances** where appropriate

This guide provides a comprehensive foundation for working with Databricks effectively in data engineering scenarios. Focus on implementing the medallion architecture, optimizing performance, and following security best practices for successful production deployments.