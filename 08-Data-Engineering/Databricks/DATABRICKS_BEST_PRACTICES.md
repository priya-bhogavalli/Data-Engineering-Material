# Databricks Best Practices for Data Engineering

## Cluster Management

### Cluster Configuration
```python
# Optimal cluster settings
cluster_config = {
    "cluster_name": "production-etl-cluster",
    "spark_version": "11.3.x-scala2.12",  # Use LTS versions
    "node_type_id": "i3.xlarge",  # Memory-optimized for data processing
    "driver_node_type_id": "i3.xlarge",
    "num_workers": 2,
    "autoscale": {
        "min_workers": 1,
        "max_workers": 8
    },
    "auto_termination_minutes": 30,  # Prevent idle costs
    "enable_elastic_disk": True,
    "disk_spec": {
        "disk_type": {"azure_disk_type": "premium_lrs"},
        "disk_size": 100
    }
}

# Production Spark configurations
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.databricks.delta.optimizeWrite.enabled", "true")
spark.conf.set("spark.databricks.delta.autoCompact.enabled", "true")
```

### Cluster Policies
```json
{
  "cluster_type": {
    "type": "fixed",
    "value": "job"
  },
  "spark_version": {
    "type": "regex",
    "pattern": "11\\.3\\.x-scala2\\.12"
  },
  "node_type_id": {
    "type": "allowlist",
    "values": ["i3.xlarge", "i3.2xlarge", "r5.xlarge"]
  },
  "autoscale": {
    "type": "range",
    "min": 1,
    "max": 10
  },
  "auto_termination_minutes": {
    "type": "range",
    "min": 10,
    "max": 120
  }
}
```

### Resource Optimization
```python
def optimize_cluster_resources():
    """Best practices for cluster resource optimization"""
    
    # Monitor cluster utilization
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
    
    # Right-size recommendations
    recommendations = cluster_metrics.withColumn(
        "recommendation",
        when(col("avg_cpu") < 0.3, "Consider smaller instance type")
        .when(col("avg_cpu") > 0.8, "Consider larger instance type")
        .when(col("avg_memory") > 0.9, "Add more memory or workers")
        .otherwise("Current sizing is appropriate")
    )
    
    return recommendations
```

## Data Organization and Storage

### Delta Lake Best Practices
```python
# Table creation with optimal settings
def create_optimized_delta_table():
    """Create Delta table with best practices"""
    
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
            'delta.deletedFileRetentionDuration' = 'interval 7 days',
            'delta.logRetentionDuration' = 'interval 30 days'
        )
    """)

# Optimal partitioning strategy
def implement_partitioning_strategy(df, table_path):
    """Implement optimal partitioning for large tables"""
    
    # Analyze data distribution
    partition_stats = df.groupBy("order_date", "region").count()
    
    # Check partition sizes
    avg_partition_size = partition_stats.agg(avg("count")).collect()[0][0]
    
    if avg_partition_size > 1000000:  # > 1M records per partition
        # Add sub-partitioning
        df_partitioned = df.withColumn("year", year("order_date")) \
                          .withColumn("month", month("order_date"))
        
        df_partitioned.write.format("delta") \
            .partitionBy("year", "month", "region") \
            .save(table_path)
    else:
        df.write.format("delta") \
            .partitionBy("order_date", "region") \
            .save(table_path)
```

### File Organization
```python
def organize_data_files():
    """Best practices for file organization"""
    
    # Medallion architecture implementation
    data_layers = {
        "bronze": "/delta/bronze/",    # Raw data
        "silver": "/delta/silver/",    # Cleaned data
        "gold": "/delta/gold/"         # Business aggregations
    }
    
    # Naming conventions
    table_naming = {
        "bronze": "raw_{source_system}_{table_name}",
        "silver": "clean_{domain}_{table_name}",
        "gold": "agg_{business_area}_{metric_name}"
    }
    
    # File size optimization
    spark.conf.set("spark.sql.files.maxPartitionBytes", "134217728")  # 128MB
    spark.conf.set("spark.sql.files.openCostInBytes", "4194304")      # 4MB
    
    return data_layers, table_naming
```

## Performance Optimization

### Query Optimization
```python
def optimize_queries():
    """Query optimization best practices"""
    
    # Use broadcast joins for small tables
    small_table = spark.table("dim_products").filter(col("is_active") == True)
    large_table = spark.table("fact_sales")
    
    # Explicit broadcast hint
    result = large_table.join(
        broadcast(small_table),
        "product_id"
    )
    
    # Predicate pushdown
    optimized_query = spark.sql("""
        SELECT s.*, p.product_name
        FROM fact_sales s
        JOIN dim_products p ON s.product_id = p.product_id
        WHERE s.order_date >= '2024-01-01'  -- Filter early
          AND p.is_active = true
    """)
    
    # Use column pruning
    selected_columns = large_table.select("order_id", "customer_id", "order_amount")
    
    return result, optimized_query, selected_columns

# Cache frequently accessed data
def implement_caching_strategy():
    """Strategic caching for performance"""
    
    # Cache dimension tables
    dim_customers = spark.table("dim_customers").cache()
    dim_products = spark.table("dim_products").cache()
    
    # Cache intermediate results
    daily_aggregates = spark.sql("""
        SELECT 
            order_date,
            region,
            SUM(order_amount) as daily_sales,
            COUNT(*) as order_count
        FROM fact_sales
        WHERE order_date >= current_date() - 30
        GROUP BY order_date, region
    """).cache()
    
    # Monitor cache usage
    cache_stats = spark.sql("SHOW TABLES").filter(col("isTemporary") == True)
    
    return dim_customers, dim_products, daily_aggregates
```

### Delta Lake Optimization
```python
def optimize_delta_tables():
    """Delta Lake optimization strategies"""
    
    # Regular optimization schedule
    def optimize_table(table_name):
        # Compact small files
        spark.sql(f"OPTIMIZE {table_name}")
        
        # Z-order for better data skipping
        spark.sql(f"OPTIMIZE {table_name} ZORDER BY (customer_id, order_date)")
        
        # Vacuum old files
        spark.sql(f"VACUUM {table_name} RETAIN 168 HOURS")  # 7 days
    
    # Analyze table statistics
    def analyze_table_stats(table_name):
        stats = spark.sql(f"DESCRIBE DETAIL {table_name}").collect()[0]
        
        file_count = stats['numFiles']
        avg_file_size = stats['sizeInBytes'] / file_count if file_count > 0 else 0
        
        if file_count > 1000 or avg_file_size < 10 * 1024 * 1024:  # < 10MB
            print(f"Table {table_name} needs optimization")
            optimize_table(table_name)
    
    # Automated optimization
    tables_to_optimize = ["fact_sales", "fact_orders", "dim_customers"]
    for table in tables_to_optimize:
        analyze_table_stats(table)
```

## Data Quality and Validation

### Data Quality Framework
```python
from pyspark.sql.functions import *

def implement_data_quality_checks():
    """Comprehensive data quality framework"""
    
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
                        "passed": null_percentage < 5,  # < 5% nulls allowed
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
            
            elif rule_name == "range_check":
                for column, (min_val, max_val) in rule_condition.items():
                    out_of_range = df.filter(
                        (col(column) < min_val) | (col(column) > max_val)
                    ).count()
                    
                    results.append({
                        "table": table_name,
                        "rule": f"range_check_{column}",
                        "passed": out_of_range == 0,
                        "value": out_of_range,
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
    
    # Apply to tables
    df = spark.table("fact_sales")
    quality_results = validate_data_quality(df, "fact_sales", quality_rules)
    
    # Store results
    results_df = spark.createDataFrame(quality_results)
    results_df.write.format("delta").mode("append").save("/delta/monitoring/data_quality")
    
    return quality_results
```

### Schema Evolution
```python
def handle_schema_evolution():
    """Best practices for schema evolution"""
    
    # Enable schema evolution
    spark.conf.set("spark.databricks.delta.schema.autoMerge.enabled", "true")
    
    def safe_schema_evolution(source_df, target_path, expected_schema):
        """Safely evolve schema with validation"""
        
        current_schema = source_df.schema
        
        # Add missing columns with defaults
        for field in expected_schema.fields:
            if field.name not in [f.name for f in current_schema.fields]:
                source_df = source_df.withColumn(
                    field.name, 
                    lit(None).cast(field.dataType)
                )
        
        # Handle type changes safely
        for field in current_schema.fields:
            expected_field = next(
                (f for f in expected_schema.fields if f.name == field.name), 
                None
            )
            
            if expected_field and field.dataType != expected_field.dataType:
                try:
                    source_df = source_df.withColumn(
                        field.name,
                        col(field.name).cast(expected_field.dataType)
                    )
                except Exception as e:
                    print(f"Cannot cast {field.name}: {e}")
        
        # Write with schema merge
        source_df.write.format("delta") \
            .option("mergeSchema", "true") \
            .mode("append") \
            .save(target_path)
        
        return source_df
    
    return safe_schema_evolution
```

## Security and Governance

### Access Control
```python
def implement_security_best_practices():
    """Security and governance implementation"""
    
    # Unity Catalog setup
    spark.sql("""
        CREATE CATALOG IF NOT EXISTS production
        COMMENT 'Production data catalog'
    """)
    
    spark.sql("""
        CREATE SCHEMA IF NOT EXISTS production.sales
        COMMENT 'Sales domain data'
    """)
    
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
    
    # Column-level security
    spark.sql("""
        CREATE VIEW secure_customers AS
        SELECT 
            customer_id,
            customer_name,
            mask_sensitive_data(current_user(), email) as email,
            mask_sensitive_data(current_user(), phone) as phone,
            registration_date
        FROM customers
        WHERE 
            CASE 
                WHEN is_member('data_engineers') THEN TRUE
                WHEN is_member('analysts') AND region = 'US' THEN TRUE
                ELSE FALSE
            END
    """)

def setup_data_lineage():
    """Implement data lineage tracking"""
    
    lineage_info = {
        "job_id": dbutils.widgets.get("job_id") if dbutils.widgets.get("job_id") else "manual",
        "notebook_path": dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get(),
        "user": dbutils.notebook.entry_point.getDbutils().notebook().getContext().userName().get(),
        "timestamp": current_timestamp()
    }
    
    def track_transformation(source_tables, target_table, transformation_logic):
        """Track data transformation lineage"""
        
        lineage_record = {
            **lineage_info,
            "source_tables": source_tables,
            "target_table": target_table,
            "transformation_logic": transformation_logic
        }
        
        lineage_df = spark.createDataFrame([lineage_record])
        lineage_df.write.format("delta").mode("append").save("/delta/governance/lineage")
    
    return track_transformation
```

### Secrets Management
```python
def manage_secrets_securely():
    """Best practices for secrets management"""
    
    # Use secret scopes instead of hardcoding
    def get_database_connection():
        """Secure database connection"""
        
        connection_params = {
            "url": "jdbc:postgresql://hostname:5432/database",
            "user": dbutils.secrets.get("database", "username"),
            "password": dbutils.secrets.get("database", "password"),
            "driver": "org.postgresql.Driver"
        }
        
        return connection_params
    
    # Rotate secrets regularly
    def validate_secret_freshness():
        """Check if secrets need rotation"""
        
        secret_metadata = spark.sql("""
            SELECT 
                scope_name,
                key_name,
                last_updated,
                DATEDIFF(current_date(), last_updated) as days_old
            FROM system.secrets.secret_metadata
            WHERE days_old > 90  -- Rotate every 90 days
        """)
        
        return secret_metadata
    
    return get_database_connection, validate_secret_freshness
```

## Workflow and Job Management

### Job Design Patterns
```python
def design_robust_workflows():
    """Best practices for workflow design"""
    
    # Idempotent job design
    def idempotent_etl_job(source_path, target_path, date_partition):
        """Design jobs to be safely re-runnable"""
        
        # Check if already processed
        try:
            existing_data = spark.read.format("delta").load(target_path) \
                .filter(col("partition_date") == date_partition)
            
            if existing_data.count() > 0:
                print(f"Data for {date_partition} already exists. Skipping.")
                return
        except:
            pass  # Table doesn't exist yet
        
        # Process data
        source_df = spark.read.format("delta").load(source_path) \
            .filter(col("date") == date_partition)
        
        processed_df = source_df.withColumn("partition_date", lit(date_partition)) \
                                .withColumn("processed_at", current_timestamp())
        
        # Atomic write
        processed_df.write.format("delta") \
            .mode("append") \
            .save(target_path)
    
    # Error handling and retry logic
    def robust_job_execution(job_function, max_retries=3):
        """Implement retry logic with exponential backoff"""
        
        import time
        
        for attempt in range(max_retries):
            try:
                result = job_function()
                return result
            except Exception as e:
                if attempt == max_retries - 1:
                    # Log error and fail
                    error_info = {
                        "job_name": "etl_pipeline",
                        "error_message": str(e),
                        "attempt": attempt + 1,
                        "timestamp": current_timestamp()
                    }
                    
                    error_df = spark.createDataFrame([error_info])
                    error_df.write.format("delta").mode("append").save("/delta/monitoring/job_errors")
                    
                    raise e
                else:
                    # Wait before retry (exponential backoff)
                    wait_time = 2 ** attempt
                    print(f"Attempt {attempt + 1} failed. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
    
    return idempotent_etl_job, robust_job_execution
```

### Monitoring and Alerting
```python
def implement_monitoring():
    """Comprehensive monitoring and alerting"""
    
    def monitor_job_performance():
        """Monitor job execution metrics"""
        
        job_metrics = spark.sql("""
            SELECT 
                job_id,
                job_name,
                start_time,
                end_time,
                status,
                TIMESTAMPDIFF(MINUTE, start_time, end_time) as duration_minutes,
                cluster_id,
                total_task_time,
                input_size_bytes,
                output_size_bytes
            FROM system.workflow.job_runs
            WHERE start_time >= current_timestamp() - INTERVAL 24 HOURS
        """)
        
        # Identify performance issues
        performance_issues = job_metrics.filter(
            (col("duration_minutes") > 60) |  # Long-running jobs
            (col("status") == "FAILED") |     # Failed jobs
            (col("total_task_time") / col("duration_minutes") < 0.5)  # Low utilization
        )
        
        return performance_issues
    
    def setup_alerts():
        """Configure alerting for critical issues"""
        
        # Data freshness alerts
        freshness_check = spark.sql("""
            SELECT 
                table_name,
                MAX(last_updated) as last_update,
                TIMESTAMPDIFF(HOUR, MAX(last_updated), current_timestamp()) as hours_stale
            FROM information_schema.tables
            WHERE table_schema = 'production'
            GROUP BY table_name
            HAVING hours_stale > 24  -- Alert if data is > 24 hours old
        """)
        
        # Job failure alerts
        failed_jobs = spark.sql("""
            SELECT 
                job_name,
                COUNT(*) as failure_count,
                MAX(end_time) as last_failure
            FROM system.workflow.job_runs
            WHERE status = 'FAILED'
              AND start_time >= current_timestamp() - INTERVAL 1 HOUR
            GROUP BY job_name
            HAVING failure_count > 0
        """)
        
        return freshness_check, failed_jobs
    
    return monitor_job_performance, setup_alerts
```

## Cost Optimization

### Resource Management
```python
def optimize_costs():
    """Cost optimization strategies"""
    
    # Cluster auto-termination
    def configure_auto_termination():
        """Optimal auto-termination settings"""
        
        cluster_configs = {
            "interactive_clusters": {
                "auto_termination_minutes": 30,  # Short for development
                "enable_elastic_disk": True
            },
            "job_clusters": {
                "auto_termination_minutes": 0,   # Terminate immediately after job
                "spot_instances": True           # Use spot instances for cost savings
            },
            "sql_warehouses": {
                "auto_stop_mins": 10,           # Quick stop for SQL warehouses
                "min_num_clusters": 1,
                "max_num_clusters": 3
            }
        }
        
        return cluster_configs
    
    # Storage optimization
    def optimize_storage_costs():
        """Storage cost optimization"""
        
        # Implement data lifecycle policies
        lifecycle_policies = {
            "bronze_layer": {
                "retention_days": 90,
                "storage_class": "standard"
            },
            "silver_layer": {
                "retention_days": 365,
                "storage_class": "standard"
            },
            "gold_layer": {
                "retention_days": 2555,  # 7 years
                "storage_class": "cold"
            }
        }
        
        # Archive old data
        def archive_old_data(table_path, retention_days):
            """Archive data older than retention period"""
            
            cutoff_date = current_date() - retention_days
            
            old_data = spark.read.format("delta").load(table_path) \
                .filter(col("created_date") < cutoff_date)
            
            if old_data.count() > 0:
                # Move to archive storage
                old_data.write.format("delta") \
                    .mode("append") \
                    .save(f"{table_path}_archive")
                
                # Delete from main table
                from delta.tables import DeltaTable
                delta_table = DeltaTable.forPath(spark, table_path)
                delta_table.delete(col("created_date") < cutoff_date)
        
        return lifecycle_policies, archive_old_data
    
    return configure_auto_termination, optimize_storage_costs
```

### Usage Monitoring
```python
def monitor_usage_and_costs():
    """Monitor resource usage and costs"""
    
    # Cluster utilization analysis
    utilization_report = spark.sql("""
        SELECT 
            cluster_id,
            cluster_name,
            DATE(start_time) as usage_date,
            SUM(TIMESTAMPDIFF(MINUTE, start_time, end_time)) as total_runtime_minutes,
            AVG(cpu_utilization) as avg_cpu_utilization,
            AVG(memory_utilization) as avg_memory_utilization,
            COUNT(DISTINCT user_name) as unique_users
        FROM system.compute.cluster_usage
        WHERE start_time >= current_date() - 30
        GROUP BY cluster_id, cluster_name, DATE(start_time)
        ORDER BY usage_date DESC, total_runtime_minutes DESC
    """)
    
    # Cost allocation by team/project
    cost_allocation = spark.sql("""
        SELECT 
            cluster_tags.team as team_name,
            cluster_tags.project as project_name,
            SUM(dbu_hours * dbu_rate) as estimated_cost,
            SUM(dbu_hours) as total_dbu_hours
        FROM system.billing.usage
        WHERE usage_date >= current_date() - 30
        GROUP BY cluster_tags.team, cluster_tags.project
        ORDER BY estimated_cost DESC
    """)
    
    return utilization_report, cost_allocation
```

Remember to regularly review and update these best practices as Databricks continues to evolve with new features and improvements. Always test configurations in development environments before applying to production workloads.