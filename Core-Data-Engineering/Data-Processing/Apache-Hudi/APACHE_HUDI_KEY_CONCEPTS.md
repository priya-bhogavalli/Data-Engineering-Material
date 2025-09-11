# Apache Hudi Key Concepts for Data Engineering

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Core Components](#-core-components)
   - [Table Types](#table-types)
   - [Timeline](#timeline)
   - [File Groups](#file-groups)
3. [Hudi Architecture](#-hudi-architecture)
4. [ACID Operations](#-acid-operations)
5. [Time Travel & Incremental Processing](#-time-travel--incremental-processing)
6. [Performance Optimization](#-performance-optimization)
   - [Compaction](#1-compaction)
   - [Clustering](#2-clustering)
   - [Indexing](#3-indexing)
7. [Configuration](#️-configuration)
8. [Integration](#-integration)
9. [When to Use Hudi](#-when-to-use-hudi)
10. [Interview Focus Areas](#-interview-focus-areas)
11. [Quick References](#-quick-references)

---

## 🎯 Overview

Apache Hudi (Hadoop Upserts Deletes and Incrementals) is an open-source data management framework that brings database-like capabilities to data lakes, enabling efficient upserts, deletes, and incremental data processing on large analytical datasets.

**Key Benefits:**
- **ACID Transactions**: Atomicity, Consistency, Isolation, Durability on data lakes
- **Upserts & Deletes**: Efficient record-level updates and deletions
- **Incremental Processing**: Process only changed data since last run
- **Time Travel**: Query data at different points in time
- **Schema Evolution**: Handle schema changes gracefully

## 📦 Core Components

### Table Types

#### Copy on Write (COW)
**Definition**: Stores data in columnar format (Parquet) and rewrites entire files during updates.

**Key Characteristics**:
- **Write Performance**: Slower due to file rewrites
- **Read Performance**: Faster as no merge required
- **Storage Overhead**: Lower storage requirements
- **Use Cases**: Read-heavy workloads, analytical queries

```python
# COW table creation
cow_options = {
    'hoodie.table.name': 'customers_cow',
    'hoodie.datasource.write.table.type': 'COPY_ON_WRITE',
    'hoodie.datasource.write.recordkey.field': 'customer_id',
    'hoodie.datasource.write.partitionpath.field': 'region',
    'hoodie.datasource.write.precombine.field': 'updated_at'
}

df.write.format("hudi").options(**cow_options).save("/path/to/cow_table")
print("COW table created successfully")
# Output: COW table created successfully
```

#### Merge on Read (MOR)
**Definition**: Stores data using combination of columnar (Parquet) and row-based (Avro) formats.

**Key Characteristics**:
- **Write Performance**: Faster with append-only delta logs
- **Read Performance**: Slower due to merge-on-read
- **Storage Overhead**: Higher due to base + delta files
- **Use Cases**: Write-heavy workloads, real-time ingestion

```python
# MOR table creation
mor_options = {
    'hoodie.table.name': 'transactions_mor',
    'hoodie.datasource.write.table.type': 'MERGE_ON_READ',
    'hoodie.datasource.write.recordkey.field': 'transaction_id',
    'hoodie.datasource.write.partitionpath.field': 'date',
    'hoodie.datasource.write.precombine.field': 'timestamp',
    'hoodie.compact.inline': 'false',
    'hoodie.compact.inline.max.delta.commits': '5'
}

df.write.format("hudi").options(**mor_options).save("/path/to/mor_table")
print("MOR table created successfully")
# Output: MOR table created successfully
```

### Timeline

**Definition**: Maintains an ordered log of all actions performed on the table, enabling time travel and incremental processing.

**Timeline Actions**:
- **COMMIT**: Successful write operation
- **DELTA_COMMIT**: Successful write to MOR table
- **CLEAN**: Cleanup of old file versions
- **COMPACTION**: Merge delta files with base files
- **ROLLBACK**: Revert failed operations

```python
# Query timeline information
timeline_df = spark.sql("SHOW COMMITS ON hudi_table")
timeline_df.show()
# Output:
# +-------------------+------+----------+
# |         timestamp |action|    state |
# +-------------------+------+----------+
# |20240101120000000  |commit|COMPLETED |
# |20240101110000000  |commit|COMPLETED |
# +-------------------+------+----------+
```

### File Groups

**Definition**: Logical grouping of files that contain records with the same record key within a partition.

**Components**:
- **Base Files**: Columnar files (Parquet) containing records
- **Log Files**: Row-based files (Avro) containing updates
- **File Slices**: Combination of base file + log files at a point in time

## 🏧 Hudi Architecture

**Definition**: Multi-layered architecture supporting ACID transactions and incremental processing.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                HUDI ARCHITECTURE                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           CLIENT LAYER                                     │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │ │
│  │  │   Spark     │  │    Flink    │  │    Presto   │  │    Hive     │       │ │
│  │  │ DataSource  │  │ DataSource  │  │ Connector   │  │ Connector   │       │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘       │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                       │                                         │
│                                       ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           HUDI CORE                                        │ │
│  │                                                                             │ │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │ │
│  │  │   WRITE CLIENT  │    │   READ CLIENT   │    │   TIMELINE      │         │ │
│  │  │                 │    │                 │    │   SERVICE       │         │ │
│  │  │ • Upsert        │    │ • Snapshot      │    │                 │         │ │
│  │  │ • Insert        │    │ • Incremental   │    │ • Commit        │         │ │
│  │  │ • Delete        │    │ • Time Travel   │    │ • Rollback      │         │ │
│  │  │ • Bulk Insert   │    │ • Read Optimized│    │ • Clean         │         │ │
│  │  └─────────────────┘    └─────────────────┘    └─────────────────┘         │ │
│  │                                                                             │ │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │ │
│  │  │     INDEX       │    │   COMPACTION    │    │   CLUSTERING    │         │ │
│  │  │                 │    │                 │    │                 │         │ │
│  │  │ • Bloom Filter  │    │ • Async         │    │ • Data Layout   │         │ │
│  │  │ • Simple        │    │ • Inline        │    │ • Optimization  │         │ │
│  │  │ • HBase         │    │ • Scheduling    │    │ • Sorting       │         │ │
│  │  │ • Global Simple │    │ • Strategy      │    │ • Bucketing     │         │ │
│  │  └─────────────────┘    └─────────────────┘    └─────────────────┘         │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                       │                                         │
│                                       ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                         STORAGE LAYER                                      │ │
│  │                                                                             │ │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │ │
│  │  │      HDFS       │    │       S3        │    │   Azure Blob    │         │ │
│  │  │                 │    │                 │    │                 │         │ │
│  │  │ • Base Files    │    │ • Base Files    │    │ • Base Files    │         │ │
│  │  │ • Log Files     │    │ • Log Files     │    │ • Log Files     │         │ │
│  │  │ • Timeline      │    │ • Timeline      │    │ • Timeline      │         │ │
│  │  │ • Metadata      │    │ • Metadata      │    │ • Metadata      │         │ │
│  │  └─────────────────┘    └─────────────────┘    └─────────────────┘         │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘

                                DATA FLOW
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  1. Client submits write/read operation                                        │
│  2. Write Client processes upserts/deletes with indexing                       │
│  3. Timeline Service manages commit coordination                                │
│  4. Data written to storage with ACID guarantees                               │
│  5. Read Client provides snapshot/incremental/time-travel queries              │
│  6. Background services handle compaction and clustering                       │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Core Components**:
- **Write Client**: Handles upserts, inserts, deletes with ACID guarantees
- **Read Client**: Provides different query types (snapshot, incremental, time travel)
- **Timeline Service**: Manages commit coordination and metadata
- **Index**: Enables efficient record lookups and updates

```python
# Check Hudi table metadata
table_path = "/path/to/hudi_table"
hudi_df = spark.read.format("hudi").load(table_path)

print(f"Table schema: {hudi_df.schema}")
print(f"Record count: {hudi_df.count()}")
print(f"Partitions: {hudi_df.rdd.getNumPartitions()}")

# Output:
# Table schema: StructType([StructField('_hoodie_commit_time', StringType(), True), ...])
# Record count: 1000000
# Partitions: 10
```

## 🔄 ACID Operations

**Definition**: Hudi provides ACID (Atomicity, Consistency, Isolation, Durability) guarantees for data lake operations.

### Upsert Operations
```python
# Upsert operation example
def perform_upsert():
    # New and updated records
    upsert_data = [
        (1, "John Updated", "john.new@email.com", "2024-01-15 11:00:00"),
        (4, "Alice Brown", "alice@email.com", "2024-01-15 11:00:00"),
        (5, "Charlie Wilson", "charlie@email.com", "2024-01-15 11:00:00")
    ]
    
    upsert_df = spark.createDataFrame(upsert_data, ["id", "name", "email", "timestamp"])
    
    # Upsert configuration
    upsert_options = {
        'hoodie.table.name': 'users',
        'hoodie.datasource.write.recordkey.field': 'id',
        'hoodie.datasource.write.partitionpath.field': '',
        'hoodie.datasource.write.operation': 'upsert',
        'hoodie.datasource.write.precombine.field': 'timestamp'
    }
    
    # Perform upsert
    upsert_df.write.format("hudi").options(**upsert_options).mode("append").save("/path/to/users")
    print("Upsert operation completed")
    # Output: Upsert operation completed

perform_upsert()
```

### Delete Operations
```python
# Delete operation example
def perform_delete():
    # Records to delete (only record keys needed)
    delete_data = [(2,), (3,)]
    delete_df = spark.createDataFrame(delete_data, ["id"])
    
    # Delete configuration
    delete_options = {
        'hoodie.table.name': 'users',
        'hoodie.datasource.write.recordkey.field': 'id',
        'hoodie.datasource.write.partitionpath.field': '',
        'hoodie.datasource.write.operation': 'delete',
        'hoodie.datasource.write.precombine.field': 'timestamp'
    }
    
    # Perform delete
    delete_df.write.format("hudi").options(**delete_options).mode("append").save("/path/to/users")
    print("Delete operation completed")
    # Output: Delete operation completed

perform_delete()
```

## ⏰ Time Travel & Incremental Processing

**Definition**: Query data at different points in time and process only changed records.

### Time Travel Queries
```python
# Time travel example
def time_travel_queries():
    table_path = "/path/to/hudi_table"
    
    # Current snapshot (default)
    current_df = spark.read.format("hudi").load(table_path)
    print(f"Current records: {current_df.count()}")
    
    # Query at specific timestamp
    timestamp_df = spark.read.format("hudi") \
        .option("as.of.instant", "20240115100000") \
        .load(table_path)
    print(f"Records at timestamp: {timestamp_df.count()}")
    
    # Query specific version
    version_df = spark.read.format("hudi") \
        .option("hoodie.datasource.read.begin.instanttime", "20240115100000") \
        .option("hoodie.datasource.read.end.instanttime", "20240115110000") \
        .load(table_path)
    print(f"Records in time range: {version_df.count()}")
    
    # Output:
    # Current records: 1000
    # Records at timestamp: 800
    # Records in time range: 200

time_travel_queries()
```

### Incremental Processing
```python
# Incremental processing example
def incremental_processing():
    table_path = "/path/to/hudi_table"
    
    # Read incremental changes since last checkpoint
    incremental_df = spark.read.format("hudi") \
        .option("hoodie.datasource.query.type", "incremental") \
        .option("hoodie.datasource.read.begin.instanttime", "20240115100000") \
        .load(table_path)
    
    # Process only changed records
    processed_df = incremental_df.filter(col("status") == "active") \
        .groupBy("category").agg(sum("amount").alias("total_amount"))
    
    print("Incremental processing completed")
    processed_df.show()
    
    # Output:
    # Incremental processing completed
    # +--------+------------+
    # |category|total_amount|
    # +--------+------------+
    # |       A|        1500|
    # |       B|        2300|
    # +--------+------------+

incremental_processing()
```

## ⚡ Performance Optimization

**Definition**: Techniques to improve Hudi table performance through compaction, clustering, and indexing.

### 1. Compaction
**Definition**: Merges delta files with base files to optimize read performance in MOR tables.

```python
# Compaction configuration
compaction_options = {
    'hoodie.compact.inline': 'false',  # Disable inline compaction
    'hoodie.compact.inline.max.delta.commits': '5',  # Trigger after 5 commits
    'hoodie.compaction.strategy': 'org.apache.hudi.table.action.compact.strategy.LogFileSizeBasedCompactionStrategy',
    'hoodie.compaction.target.io': '512000000',  # 512MB target
    'hoodie.compaction.small.file.limit': '104857600'  # 100MB small file limit
}

# Manual compaction trigger
def trigger_compaction():
    from pyspark.sql import SparkSession
    
    spark.sql(f"""
        CALL run_compaction(
            table => 'hudi_table',
            path => '/path/to/hudi_table'
        )
    """)
    print("Compaction completed")
    # Output: Compaction completed

trigger_compaction()
```

### 2. Clustering
**Definition**: Reorganizes data layout to improve query performance by co-locating related records.

```python
# Clustering configuration
clustering_options = {
    'hoodie.clustering.inline': 'true',
    'hoodie.clustering.inline.max.commits': '4',
    'hoodie.clustering.plan.strategy.target.file.max.bytes': '1073741824',  # 1GB
    'hoodie.clustering.plan.strategy.small.file.limit': '629145600',  # 600MB
    'hoodie.clustering.execution.strategy.class': 'org.apache.hudi.client.clustering.run.strategy.SparkSortAndSizeExecutionStrategy'
}

# Manual clustering trigger
def trigger_clustering():
    spark.sql(f"""
        CALL run_clustering(
            table => 'hudi_table',
            path => '/path/to/hudi_table'
        )
    """)
    print("Clustering completed")
    # Output: Clustering completed

trigger_clustering()
```

### 3. Indexing
**Definition**: Enables efficient record lookups during upsert operations.

```python
# Index configuration options
index_options = {
    # Bloom Filter Index (default)
    'hoodie.index.type': 'BLOOM',
    'hoodie.index.bloom.num_entries': '60000',
    'hoodie.index.bloom.fpp': '0.000000001',
    
    # Simple Index
    # 'hoodie.index.type': 'SIMPLE',
    
    # Global Simple Index
    # 'hoodie.index.type': 'GLOBAL_SIMPLE',
    
    # HBase Index
    # 'hoodie.index.type': 'HBASE',
    # 'hoodie.index.hbase.zkquorum': 'localhost:2181',
    # 'hoodie.index.hbase.table': 'hudi_index'
}

print("Index configuration applied")
# Output: Index configuration applied
```

## 🛠️ Configuration

**Definition**: Settings that control Hudi table behavior, performance, and functionality.

### Essential Configurations
```python
# Complete Hudi configuration example
hudi_config = {
    # Table identification
    'hoodie.table.name': 'my_hudi_table',
    'hoodie.datasource.write.table.name': 'my_hudi_table',
    
    # Table type
    'hoodie.datasource.write.table.type': 'COPY_ON_WRITE',  # or MERGE_ON_READ
    
    # Key fields
    'hoodie.datasource.write.recordkey.field': 'id',
    'hoodie.datasource.write.partitionpath.field': 'date',
    'hoodie.datasource.write.precombine.field': 'timestamp',
    
    # Write operation
    'hoodie.datasource.write.operation': 'upsert',  # insert, upsert, delete, bulk_insert
    
    # Parallelism
    'hoodie.upsert.shuffle.parallelism': '200',
    'hoodie.insert.shuffle.parallelism': '200',
    'hoodie.delete.shuffle.parallelism': '200',
    
    # File sizing
    'hoodie.parquet.max.file.size': '134217728',  # 128MB
    'hoodie.parquet.small.file.limit': '104857600',  # 100MB
    
    # Compaction (for MOR)
    'hoodie.compact.inline': 'false',
    'hoodie.compact.inline.max.delta.commits': '5',
    
    # Clustering
    'hoodie.clustering.inline': 'true',
    'hoodie.clustering.inline.max.commits': '4',
    
    # Index
    'hoodie.index.type': 'BLOOM',
    'hoodie.bloom.index.parallelism': '200',
    
    # Hive sync
    'hoodie.datasource.hive_sync.enable': 'true',
    'hoodie.datasource.hive_sync.database': 'default',
    'hoodie.datasource.hive_sync.table': 'my_hudi_table',
    'hoodie.datasource.hive_sync.partition_fields': 'date'
}

# Apply configuration
df.write.format("hudi").options(**hudi_config).save("/path/to/hudi_table")
print("Hudi table created with optimized configuration")
# Output: Hudi table created with optimized configuration
```

## 🔗 Integration

**Definition**: Hudi integrates with various data processing engines and storage systems.

### Spark Integration
```python
# Spark with Hudi
spark = SparkSession.builder \
    .appName("HudiSparkApp") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.hudi.catalog.HoodieCatalog") \
    .config("spark.sql.extensions", "org.apache.spark.sql.hudi.HoodieSparkSessionExtension") \
    .getOrCreate()

# SQL operations
spark.sql("CREATE TABLE hudi_table USING HUDI LOCATION '/path/to/hudi_table'")
spark.sql("SELECT * FROM hudi_table WHERE date = '2024-01-15'").show()
```

### Flink Integration
```python
# Flink configuration (conceptual)
flink_config = {
    'connector': 'hudi',
    'path': '/path/to/hudi_table',
    'table.type': 'MERGE_ON_READ',
    'write.operation': 'upsert',
    'hoodie.table.name': 'flink_hudi_table'
}
```

### Presto/Trino Integration
```sql
-- Query Hudi table from Presto/Trino
SELECT * FROM hudi.default.my_hudi_table 
WHERE date >= '2024-01-01'
ORDER BY timestamp DESC
LIMIT 100;
```

## 📊 When to Use Hudi

**Use Hudi When:**
- Need ACID transactions on data lakes
- Require efficient upserts and deletes
- Want incremental data processing
- Need time travel capabilities
- Have CDC (Change Data Capture) requirements
- Building real-time analytics pipelines
- Managing slowly changing dimensions

**Don't Use Hudi When:**
- Only append-only workloads (consider Delta Lake or Iceberg)
- Simple batch processing without updates
- Very small datasets (overhead not justified)
- Read-only analytical workloads

## 🎯 Interview Focus Areas

1. **Table Types**: COW vs MOR comparison and use cases
2. **ACID Operations**: Upserts, deletes, and transaction guarantees
3. **Timeline**: Understanding commit history and metadata
4. **Indexing**: Different index types and performance implications
5. **Compaction**: When and how to optimize MOR tables
6. **Incremental Processing**: CDC and time travel capabilities
7. **Performance Tuning**: File sizing, parallelism, clustering
8. **Integration**: Spark, Flink, Presto connectivity
9. **Configuration**: Key settings and optimization parameters
10. **Use Cases**: When to choose Hudi over alternatives

## 📚 Quick References

- [Hudi Documentation](https://hudi.apache.org/docs/overview)
- [Hudi Spark Guide](https://hudi.apache.org/docs/quick-start-guide)
- [Hudi Configuration](https://hudi.apache.org/docs/configurations)
- [Hudi SQL Guide](https://hudi.apache.org/docs/sql_ddl)