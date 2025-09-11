# Apache Iceberg Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-30)](#basic-level-questions-1-30)
2. [Intermediate Level Questions (31-60)](#intermediate-level-questions-31-60)
3. [Advanced Level Questions (61-90)](#advanced-level-questions-61-90)
4. [Architecture & Performance (91-120)](#architecture--performance-91-120)
5. [Streaming & Real-time Processing (121-150)](#streaming--real-time-processing-121-150)
6. [Production & Operations (151-180)](#production--operations-151-180)
7. [Scenario-Based Questions (181-200)](#scenario-based-questions-181-200)

---

## Basic Level Questions (1-30)

### 1. What is Apache Iceberg and how does it differ from traditional table formats?

**Answer:**
Apache Iceberg is an open table format for huge analytic datasets that provides ACID transactions, schema evolution, and time travel capabilities.

#### 🎯 **Key Differences from Traditional Formats**

| Aspect | Traditional Formats | Apache Iceberg |
|--------|-------------------|----------------|
| **ACID Transactions** | No guarantees | Full ACID compliance |
| **Schema Evolution** | Breaking changes | Safe, backward compatible |
| **Partitioning** | Manual management | Hidden, automatic |
| **Time Travel** | Not supported | Query historical versions |
| **Metadata** | Limited | Rich metadata with statistics |
| **Concurrent Writes** | Conflicts possible | Optimistic concurrency |

```python
from pyspark.sql import SparkSession

# Configure Spark for Iceberg
spark = SparkSession.builder \
    .appName("IcebergBasics") \
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

print("Iceberg table created with ACID guarantees and hidden partitioning")
```

**Output:**
```
Iceberg table created with ACID guarantees and hidden partitioning
```

### 2. Explain Iceberg's metadata architecture and its three-layer structure.

**Answer:**
Iceberg uses a hierarchical metadata structure for efficient operations and ACID guarantees.

#### 🎯 **Three-Layer Metadata Architecture**

```python
# View table metadata layers
def explore_iceberg_metadata():
    # 1. Table Metadata (top level)
    table_metadata = spark.sql("DESCRIBE EXTENDED iceberg_catalog.db.events")
    print("=== TABLE METADATA ===")
    table_metadata.show(truncate=False)
    
    # 2. Snapshots (version history)
    snapshots = spark.sql("SELECT * FROM iceberg_catalog.db.events.snapshots")
    print("=== SNAPSHOTS ===")
    snapshots.show()
    
    # 3. Manifest Lists (snapshot contents)
    manifests = spark.sql("SELECT * FROM iceberg_catalog.db.events.manifests")
    print("=== MANIFESTS ===")
    manifests.show()
    
    # 4. Data Files (actual data)
    files = spark.sql("SELECT * FROM iceberg_catalog.db.events.files")
    print("=== DATA FILES ===")
    files.show()

explore_iceberg_metadata()
```

**Metadata Flow:**
1. **Table Metadata** → Points to current snapshot
2. **Snapshot** → Points to manifest list
3. **Manifest List** → Points to manifest files
4. **Manifest Files** → Track data files and statistics

### 3. How does Iceberg implement ACID transactions?

**Answer:**
Iceberg provides ACID guarantees through atomic metadata updates and optimistic concurrency control.

```python
# ACID transaction example
def demonstrate_acid_transactions():
    # Atomicity - All operations succeed or fail together
    try:
        spark.sql("BEGIN")
        
        # Multiple operations in single transaction
        spark.sql("""
            INSERT INTO iceberg_catalog.db.events 
            VALUES (1, 100, 'click', current_timestamp(), map('page', 'home'))
        """)
        
        spark.sql("""
            INSERT INTO iceberg_catalog.db.events 
            VALUES (2, 101, 'view', current_timestamp(), map('page', 'product'))
        """)
        
        spark.sql("COMMIT")
        print("Transaction committed atomically")
        
    except Exception as e:
        spark.sql("ROLLBACK")
        print(f"Transaction rolled back: {e}")
    
    # Isolation - Concurrent reads see consistent snapshots
    snapshot_id = spark.sql("SELECT snapshot_id FROM iceberg_catalog.db.events.snapshots ORDER BY committed_at DESC LIMIT 1").collect()[0][0]
    
    # Read from specific snapshot (isolation)
    consistent_read = spark.sql(f"""
        SELECT COUNT(*) as record_count 
        FROM iceberg_catalog.db.events 
        VERSION AS OF {snapshot_id}
    """)
    
    print("Isolated read from snapshot:")
    consistent_read.show()

demonstrate_acid_transactions()
```

### 4. What are the different types of partitioning in Iceberg?

**Answer:**
Iceberg supports hidden partitioning with various partition transforms.

```python
# Partition transform examples
def demonstrate_partitioning():
    # Identity partitioning
    spark.sql("""
        CREATE TABLE iceberg_catalog.db.sales_identity (
            sale_id BIGINT,
            region STRING,
            amount DECIMAL(10,2),
            sale_date DATE
        ) USING ICEBERG
        PARTITIONED BY (region)
    """)
    
    # Date-based partitioning
    spark.sql("""
        CREATE TABLE iceberg_catalog.db.sales_date (
            sale_id BIGINT,
            amount DECIMAL(10,2),
            sale_date DATE
        ) USING ICEBERG
        PARTITIONED BY (
            years(sale_date),
            months(sale_date),
            days(sale_date)
        )
    """)
    
    # Bucketing
    spark.sql("""
        CREATE TABLE iceberg_catalog.db.sales_bucket (
            sale_id BIGINT,
            customer_id BIGINT,
            amount DECIMAL(10,2)
        ) USING ICEBERG
        PARTITIONED BY (bucket(16, customer_id))
    """)
    
    # Truncate partitioning
    spark.sql("""
        CREATE TABLE iceberg_catalog.db.sales_truncate (
            sale_id BIGINT,
            customer_name STRING,
            amount DECIMAL(10,2)
        ) USING ICEBERG
        PARTITIONED BY (truncate(4, customer_name))
    """)
    
    print("Created tables with different partition transforms")

demonstrate_partitioning()
```

### 5. How do you perform time travel queries in Iceberg?

**Answer:**
Iceberg supports time travel through snapshot IDs and timestamps.

```python
def demonstrate_time_travel():
    # Insert initial data
    spark.sql("""
        INSERT INTO iceberg_catalog.db.events 
        VALUES 
        (1, 100, 'login', current_timestamp(), map('device', 'mobile')),
        (2, 101, 'click', current_timestamp(), map('page', 'home'))
    """)
    
    # Get current snapshot
    current_snapshot = spark.sql("""
        SELECT snapshot_id, committed_at 
        FROM iceberg_catalog.db.events.snapshots 
        ORDER BY committed_at DESC LIMIT 1
    """).collect()[0]
    
    print(f"Current snapshot: {current_snapshot['snapshot_id']}")
    
    # Insert more data
    spark.sql("""
        INSERT INTO iceberg_catalog.db.events 
        VALUES (3, 102, 'purchase', current_timestamp(), map('amount', '99.99'))
    """)
    
    # Time travel by snapshot ID
    historical_data = spark.sql(f"""
        SELECT COUNT(*) as count_at_snapshot
        FROM iceberg_catalog.db.events 
        VERSION AS OF {current_snapshot['snapshot_id']}
    """)
    
    print("Historical data count:")
    historical_data.show()
    
    # Time travel by timestamp
    timestamp_query = spark.sql(f"""
        SELECT COUNT(*) as count_at_timestamp
        FROM iceberg_catalog.db.events 
        TIMESTAMP AS OF '{current_snapshot['committed_at']}'
    """)
    
    print("Data count at specific timestamp:")
    timestamp_query.show()
    
    # Current data count
    current_data = spark.sql("SELECT COUNT(*) as current_count FROM iceberg_catalog.db.events")
    print("Current data count:")
    current_data.show()

demonstrate_time_travel()
```

### 6. What is schema evolution in Iceberg and how does it work?

**Answer:**
Schema evolution allows safe changes to table structure without breaking existing queries.

```python
def demonstrate_schema_evolution():
    # Create initial table
    spark.sql("""
        CREATE TABLE iceberg_catalog.db.customers (
            customer_id BIGINT,
            name STRING,
            email STRING
        ) USING ICEBERG
    """)
    
    # Insert initial data
    spark.sql("""
        INSERT INTO iceberg_catalog.db.customers 
        VALUES (1, 'John Doe', 'john@email.com')
    """)
    
    print("=== INITIAL SCHEMA ===")
    spark.sql("DESCRIBE iceberg_catalog.db.customers").show()
    
    # Add new column (safe operation)
    spark.sql("""
        ALTER TABLE iceberg_catalog.db.customers 
        ADD COLUMN phone STRING
    """)
    
    print("=== AFTER ADDING COLUMN ===")
    spark.sql("DESCRIBE iceberg_catalog.db.customers").show()
    
    # Rename column (safe operation)
    spark.sql("""
        ALTER TABLE iceberg_catalog.db.customers 
        RENAME COLUMN email TO email_address
    """)
    
    print("=== AFTER RENAMING COLUMN ===")
    spark.sql("DESCRIBE iceberg_catalog.db.customers").show()
    
    # Drop column (safe - data preserved in old snapshots)
    spark.sql("""
        ALTER TABLE iceberg_catalog.db.customers 
        DROP COLUMN phone
    """)
    
    print("=== AFTER DROPPING COLUMN ===")
    spark.sql("DESCRIBE iceberg_catalog.db.customers").show()
    
    # Verify data integrity
    current_data = spark.sql("SELECT * FROM iceberg_catalog.db.customers")
    print("=== CURRENT DATA ===")
    current_data.show()

demonstrate_schema_evolution()
```

### 7. How do you create and configure an Iceberg table?

**Answer:**
Iceberg tables can be created with various configurations and properties.

```python
def create_configured_iceberg_table():
    # Basic table creation
    spark.sql("""
        CREATE TABLE iceberg_catalog.db.orders (
            order_id BIGINT,
            customer_id BIGINT,
            product_id BIGINT,
            quantity INT,
            price DECIMAL(10,2),
            order_date DATE,
            status STRING
        ) USING ICEBERG
        PARTITIONED BY (months(order_date), bucket(8, customer_id))
        TBLPROPERTIES (
            'write.target-file-size-bytes'='134217728',
            'write.parquet.compression-codec'='zstd',
            'write.metadata.compression-codec'='gzip',
            'commit.retry.num-retries'='4',
            'commit.retry.min-wait-ms'='100'
        )
    """)
    
    # View table properties
    properties = spark.sql("SHOW TBLPROPERTIES iceberg_catalog.db.orders")
    print("=== TABLE PROPERTIES ===")
    properties.show(truncate=False)
    
    # Create table from existing data
    sample_data = spark.createDataFrame([
        (1, 100, 1001, 2, 29.99, "2024-01-15", "completed"),
        (2, 101, 1002, 1, 49.99, "2024-01-16", "pending")
    ], ["order_id", "customer_id", "product_id", "quantity", "price", "order_date", "status"])
    
    # Write as Iceberg table
    sample_data.writeTo("iceberg_catalog.db.orders_from_df").using("iceberg").create()
    
    print("Tables created successfully")

create_configured_iceberg_table()
```

### 8. What are the benefits of hidden partitioning in Iceberg?

**Answer:**
Hidden partitioning eliminates partition management overhead and prevents user errors.

```python
def demonstrate_hidden_partitioning():
    # Traditional partitioning problems (what Iceberg solves)
    print("=== TRADITIONAL PARTITIONING ISSUES ===")
    print("1. Users must specify partition values in queries")
    print("2. Partition evolution requires data migration")
    print("3. Wrong partition predicates cause full scans")
    print("4. Partition layout exposed to users")
    
    # Iceberg hidden partitioning benefits
    spark.sql("""
        CREATE TABLE iceberg_catalog.db.user_events (
            event_id BIGINT,
            user_id BIGINT,
            event_timestamp TIMESTAMP,
            event_type STRING
        ) USING ICEBERG
        PARTITIONED BY (
            days(event_timestamp),
            bucket(16, user_id)
        )
    """)
    
    # Insert test data
    spark.sql("""
        INSERT INTO iceberg_catalog.db.user_events VALUES
        (1, 100, TIMESTAMP '2024-01-15 10:00:00', 'login'),
        (2, 101, TIMESTAMP '2024-01-15 11:00:00', 'click'),
        (3, 100, TIMESTAMP '2024-01-16 09:00:00', 'logout')
    """)
    
    # Query without partition awareness (Iceberg handles automatically)
    result = spark.sql("""
        SELECT event_type, COUNT(*) as count
        FROM iceberg_catalog.db.user_events
        WHERE event_timestamp >= TIMESTAMP '2024-01-15 10:30:00'
        GROUP BY event_type
    """)
    
    print("=== QUERY RESULTS (Automatic Partition Pruning) ===")
    result.show()
    
    # Show partition information
    partitions = spark.sql("""
        SELECT partition, record_count, file_count
        FROM iceberg_catalog.db.user_events.files
        GROUP BY partition
    """)
    
    print("=== PARTITION INFORMATION ===")
    partitions.show(truncate=False)

demonstrate_hidden_partitioning()
```

### 9. How do you perform MERGE operations in Iceberg?

**Answer:**
Iceberg supports MERGE operations for Change Data Capture (CDC) and upsert scenarios.

```python
def demonstrate_merge_operations():
    # Create target table
    spark.sql("""
        CREATE TABLE iceberg_catalog.db.customer_profiles (
            customer_id BIGINT,
            name STRING,
            email STRING,
            last_updated TIMESTAMP
        ) USING ICEBERG
    """)
    
    # Insert initial data
    spark.sql("""
        INSERT INTO iceberg_catalog.db.customer_profiles VALUES
        (1, 'John Doe', 'john@old.com', TIMESTAMP '2024-01-01 10:00:00'),
        (2, 'Jane Smith', 'jane@email.com', TIMESTAMP '2024-01-01 10:00:00')
    """)
    
    # Create source data (updates and new records)
    updates_df = spark.createDataFrame([
        (1, 'John Doe', 'john@new.com', '2024-01-15 12:00:00'),  # Update
        (3, 'Bob Wilson', 'bob@email.com', '2024-01-15 12:00:00')  # Insert
    ], ["customer_id", "name", "email", "last_updated"])
    
    updates_df.createOrReplaceTempView("customer_updates")
    
    # Perform MERGE operation
    spark.sql("""
        MERGE INTO iceberg_catalog.db.customer_profiles AS target
        USING customer_updates AS source
        ON target.customer_id = source.customer_id
        WHEN MATCHED THEN
            UPDATE SET 
                name = source.name,
                email = source.email,
                last_updated = source.last_updated
        WHEN NOT MATCHED THEN
            INSERT (customer_id, name, email, last_updated)
            VALUES (source.customer_id, source.name, source.email, source.last_updated)
    """)
    
    print("=== AFTER MERGE OPERATION ===")
    result = spark.sql("SELECT * FROM iceberg_catalog.db.customer_profiles ORDER BY customer_id")
    result.show()
    
    # MERGE with DELETE
    spark.sql("""
        MERGE INTO iceberg_catalog.db.customer_profiles AS target
        USING (SELECT 2 as customer_id, 'DELETE' as operation) AS source
        ON target.customer_id = source.customer_id
        WHEN MATCHED AND source.operation = 'DELETE' THEN DELETE
    """)
    
    print("=== AFTER MERGE WITH DELETE ===")
    final_result = spark.sql("SELECT * FROM iceberg_catalog.db.customer_profiles ORDER BY customer_id")
    final_result.show()

demonstrate_merge_operations()
```

### 10. What are Iceberg snapshots and how do they work?

**Answer:**
Snapshots represent immutable table states at specific points in time, enabling ACID transactions and time travel.

```python
def explore_iceberg_snapshots():
    # Create table and insert data in multiple operations
    spark.sql("""
        CREATE TABLE iceberg_catalog.db.transaction_log (
            transaction_id BIGINT,
            amount DECIMAL(10,2),
            timestamp TIMESTAMP
        ) USING ICEBERG
    """)
    
    # Operation 1: Initial insert
    spark.sql("""
        INSERT INTO iceberg_catalog.db.transaction_log VALUES
        (1, 100.00, TIMESTAMP '2024-01-01 10:00:00'),
        (2, 250.50, TIMESTAMP '2024-01-01 11:00:00')
    """)
    
    # Operation 2: More inserts
    spark.sql("""
        INSERT INTO iceberg_catalog.db.transaction_log VALUES
        (3, 75.25, TIMESTAMP '2024-01-01 12:00:00')
    """)
    
    # Operation 3: Update
    spark.sql("""
        UPDATE iceberg_catalog.db.transaction_log 
        SET amount = 300.00 
        WHERE transaction_id = 2
    """)
    
    # View all snapshots
    snapshots = spark.sql("""
        SELECT 
            snapshot_id,
            committed_at,
            operation,
            summary
        FROM iceberg_catalog.db.transaction_log.snapshots
        ORDER BY committed_at
    """)
    
    print("=== SNAPSHOT HISTORY ===")
    snapshots.show(truncate=False)
    
    # Query different snapshots
    snapshot_ids = [row['snapshot_id'] for row in snapshots.collect()]
    
    for i, snapshot_id in enumerate(snapshot_ids):
        print(f"=== DATA AT SNAPSHOT {i+1} ===")
        data = spark.sql(f"""
            SELECT COUNT(*) as record_count, SUM(amount) as total_amount
            FROM iceberg_catalog.db.transaction_log
            VERSION AS OF {snapshot_id}
        """)
        data.show()

explore_iceberg_snapshots()
```

**Output:**
```
=== SNAPSHOT HISTORY ===
+-------------------+-------------------+---------+-------+
|        snapshot_id|       committed_at|operation|summary|
+-------------------+-------------------+---------+-------+
|1234567890123456789|2024-01-01 10:00:00|   append|   {...}|
|1234567890123456790|2024-01-01 11:00:00|   append|   {...}|
|1234567890123456791|2024-01-01 12:00:00|   update|   {...}|
+-------------------+-------------------+---------+-------+

=== DATA AT SNAPSHOT 1 ===
+------------+------------+
|record_count|total_amount|
+------------+------------+
|           2|      350.50|
+------------+------------+
```

I'll continue with the next batch of questions (11-20):

### 21. How do you implement Write-Audit-Publish (WAP) pattern in Iceberg?

**Answer:**
WAP pattern allows data validation before making changes visible to readers.

```python
def demonstrate_wap_pattern():
    # Enable WAP for table
    spark.sql("""
        ALTER TABLE iceberg_catalog.db.wap_demo
        SET TBLPROPERTIES ('write.wap.enabled'='true')
    """)
    
    # Write to audit branch
    spark.conf.set("spark.wap.branch", "audit")
    
    spark.sql("""
        INSERT INTO iceberg_catalog.db.wap_demo VALUES
        (1, 'audit data', current_timestamp())
    """)
    
    # Publish to main branch if validation passes
    spark.sql("""
        CALL iceberg_catalog.system.fast_forward(
            table => 'db.wap_demo',
            branch => 'main',
            to => 'audit'
        )
    """)
    
    print("WAP pattern completed")

demonstrate_wap_pattern()
```

### 22. How do you handle large-scale data migration to Iceberg?

**Answer:**
Migrating large datasets to Iceberg requires careful planning and incremental approaches.

```python
def demonstrate_large_scale_migration():
    # Migrate data in chunks by partition
    partitions_to_migrate = ["2024-01-01", "2024-01-02", "2024-01-03"]
    
    for partition_date in partitions_to_migrate:
        # Read partition from source
        source_partition = spark.sql(f"""
            SELECT * FROM source_table 
            WHERE partition_date = '{partition_date}'
        """)
        
        # Write to Iceberg table
        source_partition.writeTo("iceberg_catalog.db.migrated_table").append()
        
        print(f"Migrated partition: {partition_date}")
    
    print("Large-scale migration completed")

demonstrate_large_scale_migration()
```

### 23. How do you implement data quality checks in Iceberg?

**Answer:**
Data quality checks can be implemented using Iceberg's metadata and custom validation logic.

```python
def implement_data_quality_checks():
    def check_data_completeness(table_name, required_columns):
        for column in required_columns:
            null_count = spark.sql(f"""
                SELECT COUNT(*) as null_count
                FROM {table_name}
                WHERE {column} IS NULL
            """).collect()[0][0]
            
            if null_count > 0:
                print(f"⚠️  Quality issue: {null_count} null values in {column}")
                return False
        return True
    
    # Run quality checks
    table_name = "iceberg_catalog.db.quality_demo"
    completeness_ok = check_data_completeness(table_name, ["id", "name", "email"])
    
    print(f"Overall data quality: {'PASS' if completeness_ok else 'FAIL'}")

implement_data_quality_checks()
```

### 24. How do you optimize query performance in Iceberg?

**Answer:**
Iceberg provides several optimization techniques for better query performance.

```python
def optimize_query_performance():
    # Z-ordering for better data clustering
    spark.sql("""
        CALL iceberg_catalog.system.rewrite_data_files(
            table => 'db.performance_demo',
            strategy => 'sort',
            sort_order => 'customer_id, order_date'
        )
    """)
    
    # Bloom filters for selective queries
    spark.sql("""
        ALTER TABLE iceberg_catalog.db.performance_demo
        SET TBLPROPERTIES (
            'write.metadata.bloom-filter-columns'='customer_id,product_id'
        )
    """)
    
    print("Query performance optimizations applied")

optimize_query_performance()
```

### 25. How do you implement disaster recovery for Iceberg tables?

**Answer:**
Disaster recovery involves backup strategies, cross-region replication, and recovery procedures.

```python
def implement_disaster_recovery():
    # Point-in-time recovery
    def point_in_time_recovery(table_name, recovery_timestamp):
        recovery_snapshot = spark.sql(f"""
            SELECT snapshot_id
            FROM {table_name}.snapshots
            WHERE committed_at <= '{recovery_timestamp}'
            ORDER BY committed_at DESC
            LIMIT 1
        """).collect()[0][0]
        
        recovery_table = f"{table_name}_recovery_{recovery_snapshot}"
        
        spark.sql(f"""
            CREATE TABLE {recovery_table}
            USING ICEBERG
            AS SELECT * FROM {table_name}
            VERSION AS OF {recovery_snapshot}
        """)
        
        print(f"Recovery table created: {recovery_table}")
        return recovery_table
    
    print("Disaster recovery procedures implemented")

implement_disaster_recovery()
```

### 26. How do you handle schema compatibility and evolution strategies?

**Answer:**
Schema evolution in Iceberg requires careful planning to maintain backward and forward compatibility.

```python
def handle_schema_compatibility():
    def evolve_schema_safely(table_name):
        # Add new optional column
        spark.sql(f"""
            ALTER TABLE {table_name}
            ADD COLUMN new_field STRING
        """)
        
        # Populate new column with default values
        spark.sql(f"""
            UPDATE {table_name}
            SET new_field = 'default_value'
            WHERE new_field IS NULL
        """)
        
        print(f"Schema evolved safely for {table_name}")
    
    def test_schema_compatibility(table_name):
        try:
            old_schema_data = spark.sql(f"""
                SELECT id, name, email
                FROM {table_name}
                LIMIT 1
            """)
            print("✅ Backward compatibility: OK")
        except Exception as e:
            print(f"❌ Backward compatibility: FAILED - {e}")
    
    print("Schema compatibility handling completed")

handle_schema_compatibility()
```

### 27. How do you implement multi-table transactions in Iceberg?

**Answer:**
Iceberg supports multi-table transactions for maintaining consistency across related tables.

```python
def implement_multi_table_transactions():
    def process_order_transaction(order_data, items_data):
        try:
            # Start transaction
            spark.sql("BEGIN")
            
            # Insert order
            order_df = spark.createDataFrame([order_data], 
                ["order_id", "customer_id", "total_amount", "order_date"])
            order_df.writeTo("iceberg_catalog.db.orders").append()
            
            # Insert order items
            items_df = spark.createDataFrame(items_data,
                ["item_id", "order_id", "product_id", "quantity", "price"])
            items_df.writeTo("iceberg_catalog.db.order_items").append()
            
            # Commit transaction
            spark.sql("COMMIT")
            print(f"Order {order_data[0]} processed successfully")
            
        except Exception as e:
            spark.sql("ROLLBACK")
            print(f"Order {order_data[0]} failed: {e}")
            raise
    
    print("Multi-table transaction completed")

implement_multi_table_transactions()
```

### 28. How do you implement data lineage tracking in Iceberg?

**Answer:**
Data lineage tracking helps understand data flow and transformations across Iceberg tables.

```python
def implement_data_lineage_tracking():
    def track_lineage(source_table, target_table, transformation_type, sql_query, user):
        import uuid
        from datetime import datetime
        
        # Get source snapshot
        source_snapshot = spark.sql(f"""
            SELECT snapshot_id FROM {source_table}.snapshots
            ORDER BY committed_at DESC LIMIT 1
        """).collect()[0][0]
        
        # Execute transformation
        spark.sql(sql_query)
        
        # Record lineage
        lineage_record = [
            (str(uuid.uuid4()), source_table, target_table, transformation_type,
             sql_query, user, datetime.now(), source_snapshot, None)
        ]
        
        lineage_df = spark.createDataFrame(lineage_record, [
            "lineage_id", "source_table", "target_table", "transformation_type",
            "transformation_sql", "created_by", "created_at", 
            "source_snapshot_id", "target_snapshot_id"
        ])
        
        lineage_df.writeTo("iceberg_catalog.db.data_lineage").append()
        
        print(f"Lineage tracked: {source_table} -> {target_table}")
    
    print("Data lineage tracking implemented")

implement_data_lineage_tracking()
```

### 29. How do you implement cost optimization strategies for Iceberg?

**Answer:**
Cost optimization involves storage efficiency, compute optimization, and lifecycle management.

```python
def implement_cost_optimization():
    def optimize_storage_costs(table_name):
        # Compress data with efficient codec
        spark.sql(f"""
            ALTER TABLE {table_name}
            SET TBLPROPERTIES (
                'write.parquet.compression-codec'='zstd',
                'write.parquet.compression-level'='3'
            )
        """)
        
        print(f"Storage optimized for {table_name}")
    
    def monitor_costs(table_name):
        storage_stats = spark.sql(f"""
            SELECT 
                SUM(file_size_in_bytes) / (1024*1024*1024) as size_gb,
                COUNT(*) as file_count
            FROM {table_name}.files
        """).collect()[0]
        
        estimated_monthly_cost = storage_stats['size_gb'] * 0.023
        
        print(f"Storage size: {storage_stats['size_gb']:.2f} GB")
        print(f"Estimated monthly cost: ${estimated_monthly_cost:.2f}")
    
    print("Cost optimization strategies implemented")

implement_cost_optimization()
```

### 30. How do you implement security and access control in Iceberg?

**Answer:**
Security in Iceberg involves encryption, access control, and audit logging.

```python
def implement_security_and_access_control():
    def configure_encryption():
        spark.sql("""
            CREATE TABLE iceberg_catalog.db.secure_table (
                id BIGINT,
                sensitive_data STRING,
                created_at TIMESTAMP
            ) USING ICEBERG
            TBLPROPERTIES (
                'encryption.key-id'='arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012',
                'encryption.type'='SSE_KMS'
            )
        """)
        
        print("Encryption configured")
    
    def implement_audit_logging():
        def log_table_access(user_id, table_name, operation, query_text, rows_affected):
            import uuid
            from datetime import datetime
            
            audit_record = [(
                str(uuid.uuid4()),
                user_id,
                table_name,
                operation,
                datetime.now(),
                query_text,
                rows_affected
            )]
            
            audit_df = spark.createDataFrame(audit_record, [
                "audit_id", "user_id", "table_name", "operation",
                "timestamp", "query_text", "rows_affected"
            ])
            
            audit_df.writeTo("iceberg_catalog.db.audit_log").append()
        
        print("Audit logging implemented")
    
    print("Security and access control implemented")

implement_security_and_access_control()
```

---

## Intermediate Level Questions (31-60)

### 31. How do you implement streaming ingestion with Iceberg?

**Answer:**
Iceberg supports streaming data ingestion with exactly-once semantics and automatic compaction.

```python
def implement_streaming_ingestion():
    # Configure streaming write
    streaming_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "events") \
        .load()
    
    # Parse and transform streaming data
    from pyspark.sql.functions import from_json, col
    from pyspark.sql.types import StructType, StructField, StringType, TimestampType
    
    schema = StructType([
        StructField("event_id", StringType(), True),
        StructField("user_id", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("timestamp", TimestampType(), True)
    ])
    
    parsed_df = streaming_df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")
    
    # Write to Iceberg table with streaming
    query = parsed_df.writeStream \
        .format("iceberg") \
        .outputMode("append") \
        .option("path", "iceberg_catalog.db.streaming_events") \
        .option("checkpointLocation", "/tmp/checkpoint") \
        .trigger(processingTime="30 seconds") \
        .start()
    
    print("Streaming ingestion configured")
    return query

implement_streaming_ingestion()
```

### 32. How do you implement table evolution with backward compatibility?

**Answer:**
Table evolution ensures new schema changes don't break existing applications.

```python
def implement_table_evolution():
    # Create initial table version
    spark.sql("""
        CREATE TABLE iceberg_catalog.db.evolving_schema (
            id BIGINT,
            name STRING,
            created_at TIMESTAMP
        ) USING ICEBERG
    """)
    
    # Evolution 1: Add optional column
    spark.sql("""
        ALTER TABLE iceberg_catalog.db.evolving_schema
        ADD COLUMN email STRING
    """)
    
    # Evolution 2: Add column with default value
    spark.sql("""
        ALTER TABLE iceberg_catalog.db.evolving_schema
        ADD COLUMN status STRING
    """)
    
    # Populate default values for existing records
    spark.sql("""
        UPDATE iceberg_catalog.db.evolving_schema
        SET status = 'active'
        WHERE status IS NULL
    """)
    
    # Evolution 3: Widen column type (safe)
    spark.sql("""
        ALTER TABLE iceberg_catalog.db.evolving_schema
        ALTER COLUMN id TYPE BIGINT
    """)
    
    # Test backward compatibility
    def test_compatibility():
        # Old application code (only knows about original columns)
        old_app_query = spark.sql("""
            SELECT id, name, created_at
            FROM iceberg_catalog.db.evolving_schema
        """)
        
        # New application code (knows about all columns)
        new_app_query = spark.sql("""
            SELECT id, name, created_at, email, status
            FROM iceberg_catalog.db.evolving_schema
        """)
        
        print("Both old and new applications can read the table")
    
    test_compatibility()
    print("Table evolution with backward compatibility completed")

implement_table_evolution()
```

### 33. How do you implement advanced partitioning strategies?

**Answer:**
Advanced partitioning combines multiple partition transforms for optimal query performance.

```python
def implement_advanced_partitioning():
    # Multi-level partitioning strategy
    spark.sql("""
        CREATE TABLE iceberg_catalog.db.advanced_partitioned (
            transaction_id BIGINT,
            user_id BIGINT,
            merchant_id BIGINT,
            amount DECIMAL(10,2),
            transaction_time TIMESTAMP,
            region STRING
        ) USING ICEBERG
        PARTITIONED BY (
            days(transaction_time),
            bucket(16, user_id),
            truncate(2, region)
        )
    """)
    
    # Dynamic partition pruning example
    def demonstrate_partition_pruning():
        # Query with partition filters
        result = spark.sql("""
            SELECT COUNT(*), AVG(amount)
            FROM iceberg_catalog.db.advanced_partitioned
            WHERE transaction_time >= '2024-01-01'
              AND transaction_time < '2024-01-02'
              AND region LIKE 'US%'
        """)
        
        # Show query plan to verify partition pruning
        result.explain(True)
        
        print("Partition pruning demonstrated")
    
    # Partition evolution without data rewrite
    def evolve_partitioning():
        # Add new partition field
        spark.sql("""
            ALTER TABLE iceberg_catalog.db.advanced_partitioned
            ADD PARTITION FIELD bucket(8, merchant_id)
        """)
        
        # Replace existing partition field
        spark.sql("""
            ALTER TABLE iceberg_catalog.db.advanced_partitioned
            REPLACE PARTITION FIELD days(transaction_time) 
            WITH hours(transaction_time)
        """)
        
        print("Partition evolution completed")
    
    demonstrate_partition_pruning()
    evolve_partitioning()
    
    print("Advanced partitioning strategies implemented")

implement_advanced_partitioning()
```

### 34. How do you implement custom metadata and table properties?

**Answer:**
Custom metadata helps track table lineage, ownership, and business context.

```python
def implement_custom_metadata():
    # Create table with custom properties
    spark.sql("""
        CREATE TABLE iceberg_catalog.db.metadata_demo (
            id BIGINT,
            data STRING,
            created_at TIMESTAMP
        ) USING ICEBERG
        TBLPROPERTIES (
            'owner'='data_team',
            'business_domain'='customer_analytics',
            'data_classification'='confidential',
            'retention_days'='2555',
            'contact_email'='data-team@company.com',
            'last_quality_check'='2024-01-01',
            'sla_tier'='gold'
        )
    """)
    
    # Function to update metadata
    def update_table_metadata(table_name, properties):
        for key, value in properties.items():
            spark.sql(f"""
                ALTER TABLE {table_name}
                SET TBLPROPERTIES ('{key}'='{value}')
            """)
        
        print(f"Updated metadata for {table_name}")
    
    # Function to read metadata
    def get_table_metadata(table_name):
        properties = spark.sql(f"SHOW TBLPROPERTIES {table_name}")
        
        print(f"=== METADATA FOR {table_name} ===")
        properties.show(truncate=False)
        
        return properties
    
    # Update metadata
    new_properties = {
        'last_quality_check': '2024-01-15',
        'data_freshness': 'daily',
        'compliance_status': 'gdpr_compliant'
    }
    
    update_table_metadata("iceberg_catalog.db.metadata_demo", new_properties)
    
    # Read current metadata
    metadata = get_table_metadata("iceberg_catalog.db.metadata_demo")
    
    # Metadata-driven operations
    def metadata_driven_operations(table_name):
        # Get retention policy from metadata
        retention_days = spark.sql(f"""
            SHOW TBLPROPERTIES {table_name}
        """).filter("key = 'retention_days'").collect()
        
        if retention_days:
            days = int(retention_days[0]['value'])
            
            # Apply retention policy
            spark.sql(f"""
                DELETE FROM {table_name}
                WHERE created_at < current_date() - INTERVAL {days} DAYS
            """)
            
            print(f"Applied retention policy: {days} days")
    
    metadata_driven_operations("iceberg_catalog.db.metadata_demo")
    
    print("Custom metadata implementation completed")

implement_custom_metadata()
```

### 35. How do you implement advanced merge strategies?

**Answer:**
Advanced merge operations handle complex CDC scenarios and data synchronization.

```python
def implement_advanced_merge_strategies():
    # Create target and source tables
    spark.sql("""
        CREATE TABLE iceberg_catalog.db.customer_master (
            customer_id BIGINT,
            name STRING,
            email STRING,
            phone STRING,
            address STRING,
            status STRING,
            created_at TIMESTAMP,
            updated_at TIMESTAMP,
            version BIGINT
        ) USING ICEBERG
    """)
    
    # Complex merge with versioning
    def merge_with_versioning():
        # Source data with CDC operations
        source_data = spark.createDataFrame([
            (1, "John Doe", "john@new.com", "555-0001", "123 Main St", "active", "2024-01-01 10:00:00", "2024-01-15 12:00:00", 2),
            (2, "Jane Smith", "jane@email.com", "555-0002", "456 Oak Ave", "inactive", "2024-01-01 11:00:00", "2024-01-15 13:00:00", 1),
            (3, "Bob Wilson", "bob@email.com", "555-0003", "789 Pine St", "active", "2024-01-15 14:00:00", "2024-01-15 14:00:00", 1)
        ], ["customer_id", "name", "email", "phone", "address", "status", "created_at", "updated_at", "version"])
        
        source_data.createOrReplaceTempView("customer_updates")
        
        # Advanced merge with conflict resolution
        spark.sql("""
            MERGE INTO iceberg_catalog.db.customer_master AS target
            USING customer_updates AS source
            ON target.customer_id = source.customer_id
            WHEN MATCHED AND source.version > target.version THEN
                UPDATE SET 
                    name = source.name,
                    email = source.email,
                    phone = source.phone,
                    address = source.address,
                    status = source.status,
                    updated_at = source.updated_at,
                    version = source.version
            WHEN MATCHED AND source.version <= target.version THEN
                UPDATE SET updated_at = current_timestamp()  -- Log the attempt
            WHEN NOT MATCHED THEN
                INSERT (customer_id, name, email, phone, address, status, created_at, updated_at, version)
                VALUES (source.customer_id, source.name, source.email, source.phone, 
                       source.address, source.status, source.created_at, source.updated_at, source.version)
        """)
        
        print("Merge with versioning completed")
    
    # Conditional merge based on business rules
    def conditional_merge():
        spark.sql("""
            MERGE INTO iceberg_catalog.db.customer_master AS target
            USING customer_updates AS source
            ON target.customer_id = source.customer_id
            WHEN MATCHED AND source.status = 'deleted' THEN
                DELETE
            WHEN MATCHED AND target.status != 'locked' THEN
                UPDATE SET *
            WHEN NOT MATCHED AND source.status != 'deleted' THEN
                INSERT *
        """)
        
        print("Conditional merge completed")
    
    # Merge with audit trail
    def merge_with_audit():
        # Create audit table
        spark.sql("""
            CREATE TABLE iceberg_catalog.db.customer_audit (
                audit_id STRING,
                customer_id BIGINT,
                operation STRING,
                old_values MAP<STRING, STRING>,
                new_values MAP<STRING, STRING>,
                changed_by STRING,
                changed_at TIMESTAMP
            ) USING ICEBERG
        """)
        
        # Merge with audit logging (simplified)
        spark.sql("""
            MERGE INTO iceberg_catalog.db.customer_master AS target
            USING customer_updates AS source
            ON target.customer_id = source.customer_id
            WHEN MATCHED THEN
                UPDATE SET *
            WHEN NOT MATCHED THEN
                INSERT *
        """)
        
        # Log changes to audit table (would be done via triggers in real implementation)
        print("Merge with audit trail completed")
    
    merge_with_versioning()
    conditional_merge()
    merge_with_audit()
    
    print("Advanced merge strategies implemented")

implement_advanced_merge_strategies()
```

I'll continue with more intermediate questions. Let me add the next batch: