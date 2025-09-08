# Apache Iceberg Comprehensive Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Core Concepts (1-25)](#core-concepts-1-25)
2. [Schema Evolution (26-50)](#schema-evolution-26-50)
3. [Performance & Optimization (51-75)](#performance--optimization-51-75)
4. [Production Operations (76-100)](#production-operations-76-100)

---

## Core Concepts (1-25)

### 1. What is Apache Iceberg and how does it differ from traditional table formats?
**Answer:**
Apache Iceberg is an open table format for huge analytic datasets that provides ACID transactions, schema evolution, and time travel.

**Key Differences:**
- **ACID Transactions**: Atomic commits vs eventual consistency
- **Schema Evolution**: Safe schema changes vs breaking changes
- **Hidden Partitioning**: Automatic partition management
- **Time Travel**: Query historical data versions
- **Metadata Management**: Efficient metadata handling for large tables

```python
# Basic Iceberg table creation
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("IcebergExample") \
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkSessionCatalog") \
    .config("spark.sql.catalog.spark_catalog.type", "hive") \
    .getOrCreate()

# Create Iceberg table
spark.sql("""
    CREATE TABLE iceberg_catalog.db.events (
        event_id BIGINT,
        user_id BIGINT,
        event_type STRING,
        timestamp TIMESTAMP,
        properties MAP<STRING, STRING>
    ) USING ICEBERG
    PARTITIONED BY (days(timestamp))
""")
```

### 2. Explain Iceberg's metadata architecture
**Answer:**
Iceberg uses a three-level metadata structure for efficient operations:

**Metadata Layers:**
- **Metadata Files**: Track table schema, partitioning, snapshots
- **Manifest Lists**: Point to manifest files for each snapshot
- **Manifest Files**: Track data files and their statistics
- **Data Files**: Actual data in Parquet/ORC format

```python
# View table metadata
spark.sql("DESCRIBE EXTENDED iceberg_catalog.db.events").show()

# View snapshots
spark.sql("SELECT * FROM iceberg_catalog.db.events.snapshots").show()

# View manifests
spark.sql("SELECT * FROM iceberg_catalog.db.events.manifests").show()

# View files
spark.sql("SELECT * FROM iceberg_catalog.db.events.files").show()
```

### 3. How does Iceberg handle partitioning?
**Answer:**
Iceberg uses hidden partitioning with partition transforms:

```python
# Partition transforms
spark.sql("""
    CREATE TABLE iceberg_catalog.db.sales (
        sale_id BIGINT,
        customer_id BIGINT,
        sale_date DATE,
        amount DECIMAL(10,2)
    ) USING ICEBERG
    PARTITIONED BY (
        months(sale_date),
        bucket(16, customer_id)
    )
""")

# Partition evolution
spark.sql("""
    ALTER TABLE iceberg_catalog.db.sales
    REPLACE PARTITION FIELD months(sale_date) WITH days(sale_date)
""")
```

---

## Schema Evolution (26-50)

### 26. How do you perform schema evolution in Iceberg?
**Answer:**
Iceberg supports safe schema evolution operations:

```python
# Add column
spark.sql("""
    ALTER TABLE iceberg_catalog.db.events
    ADD COLUMN session_id STRING
""")

# Rename column
spark.sql("""
    ALTER TABLE iceberg_catalog.db.events
    RENAME COLUMN event_type TO action_type
""")

# Drop column
spark.sql("""
    ALTER TABLE iceberg_catalog.db.events
    DROP COLUMN properties
""")

# Change column type (widening only)
spark.sql("""
    ALTER TABLE iceberg_catalog.db.events
    ALTER COLUMN user_id TYPE BIGINT
""")
```

### 27. How do you implement time travel queries?
**Answer:**
Iceberg provides time travel capabilities:

```python
# Query by snapshot ID
spark.sql("""
    SELECT * FROM iceberg_catalog.db.events
    VERSION AS OF 12345678901234567890
""").show()

# Query by timestamp
spark.sql("""
    SELECT * FROM iceberg_catalog.db.events
    TIMESTAMP AS OF '2024-01-01 10:00:00'
""").show()

# Compare versions
current = spark.table("iceberg_catalog.db.events")
historical = spark.sql("""
    SELECT * FROM iceberg_catalog.db.events
    TIMESTAMP AS OF '2024-01-01 00:00:00'
""")

# Find differences
added = current.exceptAll(historical)
removed = historical.exceptAll(current)
```

---

## Performance & Optimization (51-75)

### 51. How do you optimize Iceberg table performance?
**Answer:**
Multiple optimization strategies:

```python
# Compaction
spark.sql("CALL iceberg_catalog.system.rewrite_data_files('db.events')")

# Z-ordering
spark.sql("""
    CALL iceberg_catalog.system.rewrite_data_files(
        table => 'db.events',
        strategy => 'sort',
        sort_order => 'user_id, timestamp'
    )
""")

# File size optimization
spark.sql("""
    CALL iceberg_catalog.system.rewrite_data_files(
        table => 'db.events',
        options => map('target-file-size-bytes', '134217728')
    )
""")
```

### 52. How do you manage table maintenance?
**Answer:**
Regular maintenance operations:

```python
# Expire old snapshots
spark.sql("""
    CALL iceberg_catalog.system.expire_snapshots(
        table => 'db.events',
        older_than => TIMESTAMP '2024-01-01 00:00:00'
    )
""")

# Remove orphan files
spark.sql("""
    CALL iceberg_catalog.system.remove_orphan_files(
        table => 'db.events'
    )
""")

# Rewrite manifests
spark.sql("""
    CALL iceberg_catalog.system.rewrite_manifests('db.events')
""")
```

---

## Production Operations (76-100)

### 76. How do you implement CDC with Iceberg?
**Answer:**
Change Data Capture implementation:

```python
# Merge CDC data
spark.sql("""
    MERGE INTO iceberg_catalog.db.customers AS target
    USING cdc_changes AS source
    ON target.customer_id = source.customer_id
    WHEN MATCHED AND source.operation = 'U' THEN
        UPDATE SET *
    WHEN MATCHED AND source.operation = 'D' THEN
        DELETE
    WHEN NOT MATCHED AND source.operation = 'I' THEN
        INSERT *
""")
```

### 77. How do you monitor Iceberg tables?
**Answer:**
Monitoring and observability:

```python
# Table statistics
spark.sql("SELECT * FROM iceberg_catalog.db.events.snapshots").show()

# File statistics
spark.sql("""
    SELECT 
        COUNT(*) as file_count,
        SUM(file_size_in_bytes) as total_size,
        AVG(file_size_in_bytes) as avg_file_size
    FROM iceberg_catalog.db.events.files
""").show()

# Partition statistics
spark.sql("""
    SELECT 
        partition,
        COUNT(*) as file_count,
        SUM(record_count) as total_records
    FROM iceberg_catalog.db.events.files
    GROUP BY partition
""").show()
```

This covers the essential Iceberg concepts for data engineering interviews with practical examples.