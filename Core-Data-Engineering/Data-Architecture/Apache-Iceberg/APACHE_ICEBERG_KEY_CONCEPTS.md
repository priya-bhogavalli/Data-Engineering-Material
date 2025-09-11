# Apache Iceberg Key Concepts for Data Engineering

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Core Architecture](#-core-architecture)
3. [Key Features](#-key-features)
4. [Use Cases](#-use-cases)
5. [Integrations](#-integrations)
6. [Best Practices](#-best-practices)
7. [Limitations](#-limitations)
8. [Version Highlights](#-version-highlights)
9. [Interview Focus Areas](#-interview-focus-areas)
10. [Quick References](#-quick-references)

---

## 🎯 Overview

Apache Iceberg is an open table format for huge analytic datasets that brings the reliability and simplicity of SQL tables to big data. It provides ACID transactions, schema evolution, and time travel capabilities for data lakes.

**Key Benefits:**
- **ACID Transactions**: Atomic, consistent, isolated, and durable operations
- **Schema Evolution**: Safe schema changes without breaking downstream consumers
- **Time Travel**: Query historical data versions and rollback changes
- **Hidden Partitioning**: Automatic partition management without user intervention
- **Performance**: Efficient query planning and execution optimization

## 🏗️ Core Architecture

### Metadata Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            ICEBERG TABLE ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐             │
│  │   METADATA      │    │   MANIFEST      │    │     DATA        │             │
│  │     LAYER       │    │     LAYER       │    │     LAYER       │             │
│  │                 │    │                 │    │                 │             │
│  │ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │             │
│  │ │Table        │ │    │ │Manifest     │ │    │ │Parquet/ORC  │ │             │
│  │ │Metadata     │ │───►│ │Lists        │ │───►│ │Data Files   │ │             │
│  │ │             │ │    │ │             │ │    │ │             │ │             │
│  │ │• Schema     │ │    │ │• Snapshots  │ │    │ │• Actual Data│ │             │
│  │ │• Partitions │ │    │ │• Manifests  │ │    │ │• Statistics │ │             │
│  │ │• Snapshots  │ │    │ │• Statistics │ │    │ │• Partitions │ │             │
│  │ │• Properties │ │    │ │             │ │    │ │             │ │             │
│  │ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │             │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘             │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           METADATA FLOW                                    │ │
│  │                                                                             │ │
│  │  1. Table Metadata points to current snapshot                              │ │
│  │  2. Snapshot points to manifest list                                       │ │
│  │  3. Manifest list points to manifest files                                 │ │
│  │  4. Manifest files track data files and statistics                         │ │
│  │  5. Data files contain actual table data                                   │ │
│  │                                                                             │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Component Details

**1. Table Metadata**
- Current schema and partition specification
- Snapshot history and current snapshot pointer
- Table properties and configuration
- Location of manifest lists

**2. Manifest Lists**
- List of manifest files for a snapshot
- Summary statistics for query planning
- Partition information for pruning

**3. Manifest Files**
- Track individual data files
- File-level statistics (min/max values, null counts)
- Partition values for each file

**4. Data Files**
- Actual table data in Parquet, ORC, or Avro format
- Immutable once written
- Include embedded statistics

## 🚀 Key Features

### 1. ACID Transactions

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("IcebergACID") \
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkSessionCatalog") \
    .config("spark.sql.catalog.spark_catalog.type", "hive") \
    .getOrCreate()

# Atomic operations
spark.sql("""
    CREATE TABLE iceberg.db.transactions (
        id BIGINT,
        amount DECIMAL(10,2),
        timestamp TIMESTAMP
    ) USING ICEBERG
""")

# Multiple operations in single transaction
spark.sql("""
    INSERT INTO iceberg.db.transactions 
    VALUES (1, 100.50, current_timestamp())
""")
```

### 2. Schema Evolution

```python
# Safe schema changes
spark.sql("""
    ALTER TABLE iceberg.db.transactions
    ADD COLUMN customer_id BIGINT
""")

# Rename columns
spark.sql("""
    ALTER TABLE iceberg.db.transactions
    RENAME COLUMN amount TO transaction_amount
""")

# Drop columns (data preserved)
spark.sql("""
    ALTER TABLE iceberg.db.transactions
    DROP COLUMN customer_id
""")
```

### 3. Time Travel

```python
# Query by snapshot ID
spark.sql("""
    SELECT * FROM iceberg.db.transactions
    VERSION AS OF 12345678901234567890
""").show()

# Query by timestamp
spark.sql("""
    SELECT * FROM iceberg.db.transactions
    TIMESTAMP AS OF '2024-01-01 10:00:00'
""").show()

# Rollback to previous version
spark.sql("""
    CALL iceberg.system.rollback_to_snapshot('db.transactions', 12345678901234567890)
""")
```

### 4. Hidden Partitioning

```python
# Partition transforms
spark.sql("""
    CREATE TABLE iceberg.db.events (
        event_id BIGINT,
        user_id BIGINT,
        event_time TIMESTAMP,
        event_type STRING
    ) USING ICEBERG
    PARTITIONED BY (
        days(event_time),
        bucket(16, user_id)
    )
""")

# Partition evolution
spark.sql("""
    ALTER TABLE iceberg.db.events
    REPLACE PARTITION FIELD days(event_time) WITH hours(event_time)
""")
```

### 5. Merge Operations

```python
# MERGE INTO for CDC
spark.sql("""
    MERGE INTO iceberg.db.customers AS target
    USING updates AS source
    ON target.customer_id = source.customer_id
    WHEN MATCHED THEN
        UPDATE SET *
    WHEN NOT MATCHED THEN
        INSERT *
""")
```

## 🎯 Use Cases

### 1. Data Lake Analytics
- **Large-scale analytics** on petabyte datasets
- **Interactive queries** with sub-second response times
- **Batch and streaming** data processing

### 2. Data Warehousing
- **ACID transactions** for consistent data updates
- **Schema evolution** for changing business requirements
- **Time travel** for auditing and compliance

### 3. Change Data Capture (CDC)
- **Real-time data synchronization** from operational systems
- **Incremental updates** with MERGE operations
- **Historical tracking** of data changes

### 4. Machine Learning
- **Feature stores** with versioned datasets
- **Model training** on historical data snapshots
- **A/B testing** with time travel capabilities

### 5. Compliance and Auditing
- **Data lineage** tracking through snapshots
- **Point-in-time recovery** for regulatory requirements
- **Immutable audit trails** of data changes

## 🔗 Integrations

### Compute Engines
- **Apache Spark** (3.0+)
- **Apache Flink** (1.11+)
- **Trino/Presto** (latest versions)
- **Apache Hive** (3.1+)
- **Dremio** (enterprise)

### Storage Systems
- **Amazon S3**
- **Azure Data Lake Storage**
- **Google Cloud Storage**
- **HDFS**
- **MinIO**

### Catalogs
- **Hive Metastore**
- **AWS Glue Catalog**
- **Nessie**
- **REST Catalog**
- **JDBC Catalog**

### Streaming Platforms
- **Apache Kafka**
- **Amazon Kinesis**
- **Apache Pulsar**
- **Azure Event Hubs**

## 📋 Best Practices

### 1. Table Design

```python
# Optimal partitioning strategy
spark.sql("""
    CREATE TABLE iceberg.db.sales (
        sale_id BIGINT,
        customer_id BIGINT,
        product_id BIGINT,
        sale_date DATE,
        amount DECIMAL(10,2)
    ) USING ICEBERG
    PARTITIONED BY (
        months(sale_date),
        bucket(32, customer_id)
    )
    TBLPROPERTIES (
        'write.target-file-size-bytes'='134217728',
        'write.parquet.compression-codec'='zstd'
    )
""")
```

### 2. Performance Optimization

```python
# Regular maintenance
spark.sql("""
    CALL iceberg.system.rewrite_data_files(
        table => 'db.sales',
        strategy => 'sort',
        sort_order => 'customer_id, sale_date'
    )
""")

# Expire old snapshots
spark.sql("""
    CALL iceberg.system.expire_snapshots(
        table => 'db.sales',
        older_than => TIMESTAMP '2024-01-01 00:00:00',
        retain_last => 100
    )
""")
```

### 3. Schema Management

```python
# Gradual schema evolution
# 1. Add optional columns first
spark.sql("ALTER TABLE iceberg.db.events ADD COLUMN session_id STRING")

# 2. Populate new column
spark.sql("""
    UPDATE iceberg.db.events 
    SET session_id = uuid() 
    WHERE session_id IS NULL
""")

# 3. Make column required in application logic
# 4. Eventually add NOT NULL constraint
```

### 4. Monitoring and Maintenance

```python
# Monitor table health
def monitor_table_health(table_name):
    # Check snapshot count
    snapshots = spark.sql(f"SELECT COUNT(*) FROM {table_name}.snapshots").collect()[0][0]
    
    # Check file count and sizes
    files_stats = spark.sql(f"""
        SELECT 
            COUNT(*) as file_count,
            AVG(file_size_in_bytes) as avg_file_size,
            MIN(file_size_in_bytes) as min_file_size,
            MAX(file_size_in_bytes) as max_file_size
        FROM {table_name}.files
    """).collect()[0]
    
    print(f"Snapshots: {snapshots}")
    print(f"Files: {files_stats['file_count']}")
    print(f"Avg file size: {files_stats['avg_file_size']} bytes")
    
    # Recommend maintenance if needed
    if files_stats['file_count'] > 1000:
        print("Consider running compaction")
    if snapshots > 500:
        print("Consider expiring old snapshots")
```

## ⚠️ Limitations

### 1. Storage Format Constraints
- **Immutable files**: Cannot update data in place
- **Small file problem**: Frequent writes create many small files
- **Storage overhead**: Metadata overhead for very small tables

### 2. Compute Engine Support
- **Limited engines**: Not all engines support all features
- **Version compatibility**: Engine versions must match Iceberg versions
- **Feature gaps**: Some advanced features only in specific engines

### 3. Operational Complexity
- **Maintenance overhead**: Regular compaction and cleanup required
- **Catalog dependencies**: Requires external catalog service
- **Learning curve**: New concepts and operations to learn

### 4. Performance Considerations
- **Cold start**: First query may be slower due to metadata reading
- **Metadata size**: Large tables have significant metadata overhead
- **Concurrent writes**: Limited concurrent write performance

## 📈 Version Highlights

### Iceberg 1.4.0 (Latest)
- **Multi-table transactions**
- **Branching and tagging**
- **Improved delete performance**
- **Enhanced statistics collection**

### Iceberg 1.3.0
- **Position delete files**
- **Row-level security**
- **Improved merge performance**
- **Z-ordering support**

### Iceberg 1.2.0
- **Flink integration improvements**
- **Trino compatibility enhancements**
- **Better partition pruning**

### Iceberg 1.1.0
- **Spark 3.3 support**
- **Improved schema evolution**
- **Better error handling**

### Iceberg 1.0.0
- **Production-ready release**
- **Stable API**
- **Full ACID compliance**
- **Time travel queries**

## 🎯 Interview Focus Areas

1. **Architecture**: Metadata layers, snapshot isolation, file organization
2. **ACID Properties**: Transaction guarantees, consistency models
3. **Schema Evolution**: Safe changes, backward compatibility
4. **Time Travel**: Snapshot management, historical queries
5. **Partitioning**: Hidden partitioning, partition evolution
6. **Performance**: Query optimization, file management, compaction
7. **Operations**: Maintenance procedures, monitoring, troubleshooting
8. **Integrations**: Compute engines, storage systems, catalogs
9. **Best Practices**: Table design, optimization strategies
10. **Limitations**: Known constraints, workarounds

## 📚 Quick References

### Essential Commands
```sql
-- Create table
CREATE TABLE catalog.db.table (...) USING ICEBERG

-- Time travel
SELECT * FROM table VERSION AS OF snapshot_id
SELECT * FROM table TIMESTAMP AS OF '2024-01-01'

-- Schema evolution
ALTER TABLE table ADD COLUMN col_name data_type
ALTER TABLE table RENAME COLUMN old_name TO new_name
ALTER TABLE table DROP COLUMN col_name

-- Maintenance
CALL system.expire_snapshots('table', older_than => timestamp)
CALL system.rewrite_data_files('table')
CALL system.remove_orphan_files('table')
```

### Key Properties
```python
# Table properties
'write.target-file-size-bytes': '134217728'  # 128MB
'write.parquet.compression-codec': 'zstd'
'commit.retry.num-retries': '4'
'commit.retry.min-wait-ms': '100'
```

### Useful Resources
- [Apache Iceberg Documentation](https://iceberg.apache.org/docs/latest/)
- [Iceberg Spark Integration](https://iceberg.apache.org/docs/latest/spark-configuration/)
- [Iceberg Best Practices](https://iceberg.apache.org/docs/latest/best-practices/)
- [Community Slack](https://apache-iceberg.slack.com/)