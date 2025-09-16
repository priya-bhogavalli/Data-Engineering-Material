# 🏅 ETL Medallion Architecture: Bronze, Silver, Gold

## 📋 Table of Contents

1. [Overview](#overview)
2. [Bronze Layer (Raw Data)](#bronze-layer-raw-data)
3. [Silver Layer (Cleaned Data)](#silver-layer-cleaned-data)
4. [Gold Layer (Business Data)](#gold-layer-business-data)
5. [Implementation Examples](#implementation-examples)
6. [Best Practices](#best-practices)
7. [Tools and Technologies](#tools-and-technologies)

---

## Overview

The **Medallion Architecture** is a data design pattern used to logically organize data in a lakehouse, with each layer representing a different level of data quality and transformation.

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   BRONZE    │───▶│   SILVER    │───▶│    GOLD     │
│  Raw Data   │    │Cleaned Data │    │Business Data│
└─────────────┘    └─────────────┘    └─────────────┘
```

### Key Benefits
- **Incremental ETL**: Process only changed data
- **Data Quality**: Progressive improvement through layers
- **Flexibility**: Multiple consumption patterns
- **Auditability**: Full data lineage
- **Cost Efficiency**: Optimized storage and compute

---

## Bronze Layer (Raw Data)

### Purpose
- **Ingestion**: Raw data from source systems
- **Preservation**: Maintain original data format
- **Append-Only**: Historical data preservation

### Characteristics
```python
# Bronze Layer Example - PySpark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from delta.tables import DeltaTable

spark = SparkSession.builder.appName("BronzeLayer").getOrCreate()

def ingest_to_bronze(source_path, bronze_path):
    """Ingest raw data to Bronze layer"""
    
    # Read raw data (any format)
    raw_df = spark.read \
        .option("multiline", "true") \
        .json(source_path)
    
    # Add metadata columns
    bronze_df = raw_df \
        .withColumn("ingestion_timestamp", current_timestamp()) \
        .withColumn("source_file", input_file_name()) \
        .withColumn("bronze_id", monotonically_increasing_id())
    
    # Write to Bronze (append mode)
    bronze_df.write \
        .format("delta") \
        .mode("append") \
        .option("mergeSchema", "true") \
        .save(bronze_path)
    
    print(f"Ingested {bronze_df.count()} records to Bronze layer")
    return bronze_df

# Example usage
bronze_df = ingest_to_bronze(
    source_path="s3://raw-data/transactions/",
    bronze_path="s3://datalake/bronze/transactions/"
)
```

### Bronze Layer Schema
```sql
-- Bronze table structure
CREATE TABLE bronze_transactions (
    -- Original data (schema-on-read)
    transaction_data STRING,  -- Raw JSON/XML
    
    -- Metadata columns
    ingestion_timestamp TIMESTAMP,
    source_file STRING,
    bronze_id BIGINT,
    
    -- Partitioning
    ingestion_date DATE GENERATED ALWAYS AS (DATE(ingestion_timestamp))
) 
USING DELTA
PARTITIONED BY (ingestion_date)
LOCATION 's3://datalake/bronze/transactions/'
```

---

## Silver Layer (Cleaned Data)

### Purpose
- **Cleansing**: Data quality improvements
- **Standardization**: Consistent formats
- **Deduplication**: Remove duplicates
- **Validation**: Business rule enforcement

### Implementation
```python
def bronze_to_silver(bronze_path, silver_path):
    """Transform Bronze to Silver layer"""
    
    # Read from Bronze
    bronze_df = spark.read.format("delta").load(bronze_path)
    
    # Parse JSON and clean data
    silver_df = bronze_df \
        .select(
            get_json_object(col("transaction_data"), "$.transaction_id").alias("transaction_id"),
            get_json_object(col("transaction_data"), "$.user_id").alias("user_id"),
            get_json_object(col("transaction_data"), "$.amount").cast("decimal(10,2)").alias("amount"),
            get_json_object(col("transaction_data"), "$.currency").alias("currency"),
            to_timestamp(get_json_object(col("transaction_data"), "$.timestamp")).alias("transaction_timestamp"),
            col("ingestion_timestamp")
        ) \
        .filter(col("transaction_id").isNotNull()) \
        .filter(col("amount") > 0) \
        .dropDuplicates(["transaction_id"]) \
        .withColumn("amount_usd", 
            when(col("currency") == "EUR", col("amount") * 1.1)
            .when(col("currency") == "GBP", col("amount") * 1.3)
            .otherwise(col("amount"))
        ) \
        .withColumn("processed_timestamp", current_timestamp())
    
    # Upsert to Silver using Delta merge
    if DeltaTable.isDeltaTable(spark, silver_path):
        silver_table = DeltaTable.forPath(spark, silver_path)
        
        silver_table.alias("target").merge(
            silver_df.alias("source"),
            "target.transaction_id = source.transaction_id"
        ).whenMatchedUpdateAll() \
         .whenNotMatchedInsertAll() \
         .execute()
    else:
        silver_df.write.format("delta").save(silver_path)
    
    return silver_df

# Data Quality Checks
def validate_silver_data(silver_df):
    """Validate Silver layer data quality"""
    
    total_records = silver_df.count()
    
    # Check for nulls in critical fields
    null_checks = {
        "transaction_id": silver_df.filter(col("transaction_id").isNull()).count(),
        "user_id": silver_df.filter(col("user_id").isNull()).count(),
        "amount": silver_df.filter(col("amount").isNull()).count()
    }
    
    # Check for duplicates
    duplicate_count = silver_df.count() - silver_df.dropDuplicates(["transaction_id"]).count()
    
    # Data quality report
    quality_report = {
        "total_records": total_records,
        "null_checks": null_checks,
        "duplicate_count": duplicate_count,
        "quality_score": 1 - (sum(null_checks.values()) + duplicate_count) / total_records
    }
    
    print(f"Silver Layer Quality Report: {quality_report}")
    return quality_report
```

### Silver Layer Schema
```sql
-- Silver table structure
CREATE TABLE silver_transactions (
    transaction_id STRING NOT NULL,
    user_id STRING NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency STRING,
    amount_usd DECIMAL(10,2),
    transaction_timestamp TIMESTAMP,
    processed_timestamp TIMESTAMP,
    ingestion_timestamp TIMESTAMP,
    
    -- Constraints
    CONSTRAINT positive_amount CHECK (amount > 0),
    CONSTRAINT valid_currency CHECK (currency IN ('USD', 'EUR', 'GBP'))
) 
USING DELTA
PARTITIONED BY (DATE(transaction_timestamp))
LOCATION 's3://datalake/silver/transactions/'
```

---

## Gold Layer (Business Data)

### Purpose
- **Aggregation**: Business metrics and KPIs
- **Enrichment**: Join with reference data
- **Optimization**: Query performance
- **Business Logic**: Domain-specific transformations

### Implementation
```python
def silver_to_gold(silver_path, gold_path):
    """Transform Silver to Gold layer - Business aggregations"""
    
    silver_df = spark.read.format("delta").load(silver_path)
    
    # Daily user transaction summary
    daily_summary = silver_df \
        .groupBy(
            col("user_id"),
            date_trunc("day", col("transaction_timestamp")).alias("transaction_date")
        ) \
        .agg(
            count("*").alias("transaction_count"),
            sum("amount_usd").alias("total_amount_usd"),
            avg("amount_usd").alias("avg_amount_usd"),
            max("amount_usd").alias("max_amount_usd"),
            countDistinct("currency").alias("currency_diversity")
        ) \
        .withColumn("user_segment", 
            when(col("total_amount_usd") > 10000, "VIP")
            .when(col("total_amount_usd") > 1000, "Premium")
            .otherwise("Standard")
        ) \
        .withColumn("created_timestamp", current_timestamp())
    
    # Write to Gold layer
    daily_summary.write \
        .format("delta") \
        .mode("overwrite") \
        .option("overwriteSchema", "true") \
        .partitionBy("transaction_date") \
        .save(gold_path)
    
    return daily_summary

# Business Intelligence Views
def create_gold_views():
    """Create business-ready views in Gold layer"""
    
    # Monthly revenue by segment
    spark.sql("""
        CREATE OR REPLACE VIEW gold_monthly_revenue AS
        SELECT 
            DATE_TRUNC('month', transaction_date) as month,
            user_segment,
            COUNT(DISTINCT user_id) as active_users,
            SUM(total_amount_usd) as monthly_revenue,
            AVG(total_amount_usd) as avg_user_spend
        FROM gold_daily_user_summary
        GROUP BY DATE_TRUNC('month', transaction_date), user_segment
        ORDER BY month DESC, monthly_revenue DESC
    """)
    
    # User cohort analysis
    spark.sql("""
        CREATE OR REPLACE VIEW gold_user_cohorts AS
        WITH first_transaction AS (
            SELECT user_id, MIN(transaction_date) as cohort_month
            FROM gold_daily_user_summary
            GROUP BY user_id
        )
        SELECT 
            DATE_TRUNC('month', f.cohort_month) as cohort_month,
            DATE_TRUNC('month', g.transaction_date) as activity_month,
            COUNT(DISTINCT g.user_id) as active_users,
            SUM(g.total_amount_usd) as cohort_revenue
        FROM first_transaction f
        JOIN gold_daily_user_summary g ON f.user_id = g.user_id
        GROUP BY cohort_month, activity_month
        ORDER BY cohort_month, activity_month
    """)
```

### Gold Layer Schema
```sql
-- Gold table structure
CREATE TABLE gold_daily_user_summary (
    user_id STRING NOT NULL,
    transaction_date DATE NOT NULL,
    transaction_count BIGINT,
    total_amount_usd DECIMAL(15,2),
    avg_amount_usd DECIMAL(10,2),
    max_amount_usd DECIMAL(10,2),
    currency_diversity INT,
    user_segment STRING,
    created_timestamp TIMESTAMP,
    
    PRIMARY KEY (user_id, transaction_date)
) 
USING DELTA
PARTITIONED BY (transaction_date)
LOCATION 's3://datalake/gold/daily_user_summary/'
```

---

## Implementation Examples

### Complete ETL Pipeline
```python
class MedallionETLPipeline:
    def __init__(self, spark_session):
        self.spark = spark_session
        
    def run_full_pipeline(self, config):
        """Execute complete Bronze -> Silver -> Gold pipeline"""
        
        try:
            # Step 1: Ingest to Bronze
            print("🥉 Starting Bronze layer ingestion...")
            bronze_df = self.ingest_to_bronze(
                config["source_path"], 
                config["bronze_path"]
            )
            
            # Step 2: Process to Silver
            print("🥈 Processing Silver layer...")
            silver_df = self.bronze_to_silver(
                config["bronze_path"], 
                config["silver_path"]
            )
            
            # Step 3: Validate Silver data
            quality_report = self.validate_silver_data(silver_df)
            
            if quality_report["quality_score"] < 0.95:
                raise Exception(f"Data quality below threshold: {quality_report['quality_score']}")
            
            # Step 4: Create Gold layer
            print("🥇 Creating Gold layer...")
            gold_df = self.silver_to_gold(
                config["silver_path"], 
                config["gold_path"]
            )
            
            # Step 5: Update business views
            self.create_gold_views()
            
            print("✅ Pipeline completed successfully!")
            
            return {
                "status": "success",
                "bronze_records": bronze_df.count(),
                "silver_records": silver_df.count(),
                "gold_records": gold_df.count(),
                "quality_score": quality_report["quality_score"]
            }
            
        except Exception as e:
            print(f"❌ Pipeline failed: {str(e)}")
            return {"status": "failed", "error": str(e)}

# Configuration
pipeline_config = {
    "source_path": "s3://raw-data/transactions/2024/",
    "bronze_path": "s3://datalake/bronze/transactions/",
    "silver_path": "s3://datalake/silver/transactions/",
    "gold_path": "s3://datalake/gold/daily_user_summary/"
}

# Execute pipeline
pipeline = MedallionETLPipeline(spark)
result = pipeline.run_full_pipeline(pipeline_config)
print(f"Pipeline result: {result}")
```

### Incremental Processing
```python
def incremental_medallion_processing():
    """Process only new/changed data"""
    
    # Get last processed timestamp
    last_processed = spark.sql("""
        SELECT MAX(ingestion_timestamp) as last_timestamp
        FROM silver_transactions
    """).collect()[0]["last_timestamp"]
    
    # Process only new Bronze records
    new_bronze = spark.read.format("delta").load("s3://datalake/bronze/transactions/") \
        .filter(col("ingestion_timestamp") > last_processed)
    
    if new_bronze.count() > 0:
        print(f"Processing {new_bronze.count()} new records...")
        
        # Process through Silver and Gold layers
        silver_df = process_bronze_to_silver(new_bronze)
        gold_df = process_silver_to_gold(silver_df)
        
        print("✅ Incremental processing completed")
    else:
        print("ℹ️ No new data to process")
```

---

## Best Practices

### 1. Data Governance
```python
# Add data lineage tracking
def add_lineage_metadata(df, layer, source_layer=None):
    """Add data lineage and governance metadata"""
    
    lineage_df = df.withColumn("data_layer", lit(layer)) \
                   .withColumn("source_layer", lit(source_layer)) \
                   .withColumn("processing_timestamp", current_timestamp()) \
                   .withColumn("data_version", lit("v1.0")) \
                   .withColumn("quality_checks_passed", lit(True))
    
    return lineage_df
```

### 2. Error Handling
```python
def robust_layer_processing(source_df, target_path, transformation_func):
    """Robust processing with error handling"""
    
    try:
        # Apply transformation
        transformed_df = transformation_func(source_df)
        
        # Validate results
        if transformed_df.count() == 0:
            raise Exception("Transformation resulted in empty dataset")
        
        # Write to target
        transformed_df.write.format("delta").mode("append").save(target_path)
        
        return {"status": "success", "records": transformed_df.count()}
        
    except Exception as e:
        # Log error and write to error table
        error_record = spark.createDataFrame([{
            "error_timestamp": datetime.now(),
            "error_message": str(e),
            "source_count": source_df.count(),
            "target_path": target_path
        }])
        
        error_record.write.format("delta").mode("append").save("s3://datalake/errors/")
        
        return {"status": "failed", "error": str(e)}
```

### 3. Performance Optimization
```python
# Optimize Delta tables
def optimize_medallion_tables():
    """Optimize Delta tables for better performance"""
    
    tables = [
        "s3://datalake/bronze/transactions/",
        "s3://datalake/silver/transactions/",
        "s3://datalake/gold/daily_user_summary/"
    ]
    
    for table_path in tables:
        # Optimize file sizes
        spark.sql(f"OPTIMIZE delta.`{table_path}`")
        
        # Z-order for better query performance
        if "gold" in table_path:
            spark.sql(f"OPTIMIZE delta.`{table_path}` ZORDER BY (user_id, transaction_date)")
        
        # Vacuum old files (retain 7 days)
        spark.sql(f"VACUUM delta.`{table_path}` RETAIN 168 HOURS")
```

---

## Tools and Technologies

### Popular Implementations

| Tool | Bronze | Silver | Gold | Best For |
|------|--------|--------|------|----------|
| **Databricks** | Auto Loader | Delta Live Tables | SQL Analytics | Complete lakehouse |
| **AWS** | Kinesis/Glue | Glue ETL | Redshift/Athena | Cloud-native |
| **Snowflake** | Snowpipe | Streams/Tasks | Data Warehouse | SQL-heavy workloads |
| **Apache Spark** | Structured Streaming | DataFrame API | Spark SQL | Open source |

### Example with Databricks Delta Live Tables
```sql
-- Bronze table (DLT)
CREATE OR REFRESH STREAMING LIVE TABLE bronze_transactions
AS SELECT 
    *,
    current_timestamp() as ingestion_timestamp,
    input_file_name() as source_file
FROM cloud_files("s3://raw-data/transactions/", "json")

-- Silver table (DLT)
CREATE OR REFRESH STREAMING LIVE TABLE silver_transactions (
    CONSTRAINT valid_transaction_id EXPECT (transaction_id IS NOT NULL),
    CONSTRAINT positive_amount EXPECT (amount > 0) ON VIOLATION DROP ROW
)
AS SELECT 
    transaction_id,
    user_id,
    CAST(amount AS DECIMAL(10,2)) as amount,
    currency,
    CAST(timestamp AS TIMESTAMP) as transaction_timestamp,
    ingestion_timestamp
FROM STREAM(LIVE.bronze_transactions)
WHERE transaction_id IS NOT NULL

-- Gold table (DLT)
CREATE OR REFRESH LIVE TABLE gold_daily_summary
AS SELECT 
    user_id,
    DATE(transaction_timestamp) as transaction_date,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount
FROM LIVE.silver_transactions
GROUP BY user_id, DATE(transaction_timestamp)
```

---

## 🎯 Summary

The **Medallion Architecture** provides a structured approach to data processing:

- **🥉 Bronze**: Raw data preservation with minimal processing
- **🥈 Silver**: Cleaned, validated, and deduplicated data
- **🥇 Gold**: Business-ready aggregated data and metrics

**Key Benefits:**
- ✅ **Incremental Processing**: Only process changed data
- ✅ **Data Quality**: Progressive improvement through layers  
- ✅ **Flexibility**: Support multiple use cases
- ✅ **Auditability**: Complete data lineage
- ✅ **Cost Efficiency**: Optimized storage and compute

This architecture is ideal for modern data lakehouses and supports both batch and streaming data processing patterns.