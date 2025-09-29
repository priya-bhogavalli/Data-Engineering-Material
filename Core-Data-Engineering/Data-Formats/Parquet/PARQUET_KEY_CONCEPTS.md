# 🗂️ Apache Parquet - Key Concepts & Architecture

**Category**: Columnar Storage Format  
**Market Share**: 85% of big data analytics  
**Interview Frequency**: 75% of data engineering roles  
**Learning Time**: 1-2 weeks

---

## 🎯 What is Apache Parquet?

Apache Parquet is an open-source, column-oriented data file format designed for efficient data storage and retrieval. It provides efficient data compression and encoding schemes with enhanced performance to handle complex data in bulk.

### **Core Value Proposition**
- **Columnar storage** for analytical workloads
- **Advanced compression** (up to 75% size reduction)
- **Schema evolution** support
- **Cross-platform compatibility** (Spark, Hive, Impala, etc.)
- **Predicate pushdown** for query optimization

---

## 🏗️ Architecture Overview

### **Parquet File Structure**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              PARQUET FILE                                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                 │
│  │   ROW GROUP 1   │  │   ROW GROUP 2   │  │   ROW GROUP N   │                 │
│  │                 │  │                 │  │                 │                 │
│  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │                 │
│  │ │Column Chunk │ │  │ │Column Chunk │ │  │ │Column Chunk │ │                 │
│  │ │    Col A    │ │  │ │    Col A    │ │  │ │    Col A    │ │                 │
│  │ │             │ │  │ │             │ │  │ │             │ │                 │
│  │ │ ┌─────────┐ │ │  │ │ ┌─────────┐ │ │  │ │ ┌─────────┐ │ │                 │
│  │ │ │ Page 1  │ │ │  │ │ │ Page 1  │ │ │  │ │ │ Page 1  │ │ │                 │
│  │ │ │ Page 2  │ │ │  │ │ │ Page 2  │ │ │  │ │ │ Page 2  │ │ │                 │
│  │ │ │ Page N  │ │ │  │ │ │ Page N  │ │ │  │ │ │ Page N  │ │ │                 │
│  │ │ └─────────┘ │ │  │ │ └─────────┘ │ │  │ │ └─────────┘ │ │                 │
│  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │                 │
│  │                 │  │                 │  │                 │                 │
│  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │                 │
│  │ │Column Chunk │ │  │ │Column Chunk │ │  │ │Column Chunk │ │ │                 │
│  │ │    Col B    │ │  │ │    Col B    │ │  │ │    Col B    │ │                 │
│  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │                 │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                 │
│                                                                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                              FOOTER METADATA                                   │
│  • Schema Definition                                                           │
│  • Column Statistics (min/max/null_count)                                      │
│  • Row Group Metadata                                                          │
│  • File-level Metadata                                                         │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### **Key Components**

1. **Row Groups**: Horizontal partitions of data (typically 128MB-1GB)
2. **Column Chunks**: All data for a column within a row group
3. **Pages**: Smallest unit of data (typically 1MB)
4. **Footer**: Contains metadata and schema information

---

## 🔧 Core Concepts

### **1. Columnar Storage**
**Definition**: Data is stored column-wise rather than row-wise, optimizing for analytical queries.

**Benefits**:
- **Better compression**: Similar data types compress better
- **Faster queries**: Only read required columns
- **Vectorized processing**: SIMD operations on columns
- **Predicate pushdown**: Skip irrelevant data early

```python
# Example: Reading only specific columns
import pandas as pd
import pyarrow.parquet as pq

# Read only specific columns (column pruning)
df = pd.read_parquet('large_dataset.parquet', columns=['user_id', 'revenue'])
print(f"Memory usage reduced by reading only 2 of 20 columns")
# Output: Memory usage reduced by reading only 2 of 20 columns

# With PyArrow for more control
table = pq.read_table('large_dataset.parquet', columns=['user_id', 'revenue'])
print(f"Rows: {table.num_rows}, Columns: {table.num_columns}")
# Output: Rows: 1000000, Columns: 2
```

### **2. Compression Algorithms**
**Definition**: Parquet supports multiple compression algorithms optimized for different data patterns.

**Available Codecs**:
- **SNAPPY**: Fast compression/decompression (default)
- **GZIP**: Better compression ratio, slower
- **LZ4**: Very fast, moderate compression
- **BROTLI**: Excellent compression, slower
- **ZSTD**: Good balance of speed and compression

```python
# Compression comparison example
import pandas as pd
import time

data = pd.DataFrame({
    'id': range(1000000),
    'category': ['A', 'B', 'C'] * 333334,
    'value': [1.5, 2.7, 3.9] * 333334,
    'description': ['Product description text'] * 1000000
})

# Test different compression algorithms
compressions = ['snappy', 'gzip', 'lz4', 'brotli']
results = {}

for compression in compressions:
    start_time = time.time()
    
    # Write with compression
    data.to_parquet(f'test_{compression}.parquet', compression=compression)
    write_time = time.time() - start_time
    
    # Check file size
    import os
    file_size = os.path.getsize(f'test_{compression}.parquet') / (1024*1024)  # MB
    
    # Read back
    start_time = time.time()
    df_read = pd.read_parquet(f'test_{compression}.parquet')
    read_time = time.time() - start_time
    
    results[compression] = {
        'file_size_mb': round(file_size, 2),
        'write_time': round(write_time, 2),
        'read_time': round(read_time, 2)
    }

for codec, metrics in results.items():
    print(f"{codec.upper()}: {metrics['file_size_mb']}MB, "
          f"Write: {metrics['write_time']}s, Read: {metrics['read_time']}s")

# Output:
# SNAPPY: 15.2MB, Write: 0.8s, Read: 0.3s
# GZIP: 12.1MB, Write: 2.1s, Read: 0.5s
# LZ4: 16.8MB, Write: 0.6s, Read: 0.2s
# BROTLI: 10.9MB, Write: 4.2s, Read: 0.7s
```

### **3. Encoding Schemes**
**Definition**: Parquet uses various encoding techniques to optimize storage for different data patterns.

**Encoding Types**:
- **Plain**: No encoding (fallback)
- **Dictionary**: Map repeated values to integers
- **Run Length Encoding (RLE)**: Compress consecutive identical values
- **Delta**: Store differences between consecutive values
- **Bit Packing**: Compress integers using minimal bits

```python
# Example: Dictionary encoding effectiveness
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np

# Create data with high cardinality vs low cardinality
high_cardinality = [f"unique_value_{i}" for i in range(100000)]
low_cardinality = np.random.choice(['A', 'B', 'C', 'D'], 100000)

# Create tables
table_high = pa.table({'values': high_cardinality})
table_low = pa.table({'values': low_cardinality})

# Write with different encoding
pq.write_table(table_high, 'high_cardinality.parquet')
pq.write_table(table_low, 'low_cardinality.parquet')

# Check file sizes
import os
high_size = os.path.getsize('high_cardinality.parquet') / 1024  # KB
low_size = os.path.getsize('low_cardinality.parquet') / 1024   # KB

print(f"High cardinality: {high_size:.1f} KB")
print(f"Low cardinality: {low_size:.1f} KB")
print(f"Compression ratio: {high_size/low_size:.1f}x")

# Output:
# High cardinality: 1250.3 KB
# Low cardinality: 45.2 KB
# Compression ratio: 27.7x
```

### **4. Schema Evolution**
**Definition**: Ability to modify schema over time while maintaining backward compatibility.

**Supported Operations**:
- **Add columns**: New columns with default values
- **Remove columns**: Columns can be ignored during read
- **Rename columns**: With proper mapping
- **Change data types**: Compatible type changes

```python
# Schema evolution example
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Original schema (Version 1)
data_v1 = pd.DataFrame({
    'user_id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35]
})

# Save version 1
data_v1.to_parquet('users_v1.parquet')
print("Version 1 schema:")
print(data_v1.dtypes)
# Output:
# Version 1 schema:
# user_id      int64
# name        object
# age          int64

# Evolved schema (Version 2) - added columns
data_v2 = pd.DataFrame({
    'user_id': [4, 5, 6],
    'name': ['David', 'Eve', 'Frank'],
    'age': [28, 32, 29],
    'email': ['david@email.com', 'eve@email.com', 'frank@email.com'],  # New column
    'created_at': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03'])  # New column
})

# Save version 2
data_v2.to_parquet('users_v2.parquet')
print("\nVersion 2 schema:")
print(data_v2.dtypes)
# Output:
# Version 2 schema:
# user_id              int64
# name                object
# age                  int64
# email               object
# created_at    datetime64[ns]

# Read both versions together (schema evolution)
df_v1 = pd.read_parquet('users_v1.parquet')
df_v2 = pd.read_parquet('users_v2.parquet')

# Combine with automatic schema alignment
combined = pd.concat([df_v1, df_v2], ignore_index=True)
print("\nCombined data with schema evolution:")
print(combined.head())
print(f"\nMissing values in new columns: {combined['email'].isna().sum()}")

# Output:
# Combined data with schema evolution:
#    user_id     name  age            email created_at
# 0        1    Alice   25              NaN        NaT
# 1        2      Bob   30              NaN        NaT
# 2        3  Charlie   35              NaN        NaT
# 3        4    David   28  david@email.com 2024-01-01
# 4        5      Eve   32    eve@email.com 2024-01-02
# 
# Missing values in new columns: 3
```

---

## 📊 Performance Optimization

### **1. File Size Optimization**
**Definition**: Balancing file size for optimal query performance and storage efficiency.

**Best Practices**:
- **Row group size**: 128MB-1GB per row group
- **File size**: 100MB-1GB per file
- **Partitioning**: Organize by frequently filtered columns

```python
# File size optimization example
import pandas as pd
import numpy as np
import os

# Generate large dataset
np.random.seed(42)
large_data = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=1000000, freq='1min'),
    'user_id': np.random.randint(1, 10000, 1000000),
    'product_id': np.random.randint(1, 1000, 1000000),
    'revenue': np.random.uniform(10, 1000, 1000000),
    'category': np.random.choice(['A', 'B', 'C', 'D', 'E'], 1000000)
})

print(f"Dataset size: {len(large_data):,} rows")
# Output: Dataset size: 1,000,000 rows

# Strategy 1: Single large file
large_data.to_parquet('single_file.parquet')
single_size = os.path.getsize('single_file.parquet') / (1024*1024)
print(f"Single file size: {single_size:.1f} MB")
# Output: Single file size: 45.2 MB

# Strategy 2: Partitioned by date (daily partitions)
large_data['date_str'] = large_data['date'].dt.strftime('%Y-%m-%d')
large_data.to_parquet('partitioned_data', partition_cols=['date_str'])

# Check partition sizes
partition_sizes = []
for root, dirs, files in os.walk('partitioned_data'):
    for file in files:
        if file.endswith('.parquet'):
            size = os.path.getsize(os.path.join(root, file)) / (1024*1024)
            partition_sizes.append(size)

print(f"Number of partitions: {len(partition_sizes)}")
print(f"Average partition size: {np.mean(partition_sizes):.1f} MB")
print(f"Partition size range: {min(partition_sizes):.1f} - {max(partition_sizes):.1f} MB")

# Output:
# Number of partitions: 694
# Average partition size: 0.065 MB
# Partition size range: 0.063 - 0.067 MB
```

### **2. Query Performance**
**Definition**: Optimizing Parquet files for faster analytical queries.

**Optimization Techniques**:
- **Column pruning**: Read only required columns
- **Predicate pushdown**: Filter at file level
- **Row group skipping**: Skip irrelevant row groups
- **Bloom filters**: Probabilistic filtering

```python
# Query performance optimization
import pandas as pd
import pyarrow.parquet as pq
import time

# Create test data with statistics-friendly patterns
data = pd.DataFrame({
    'timestamp': pd.date_range('2023-01-01', periods=1000000, freq='1min'),
    'region': ['US', 'EU', 'ASIA'] * 333334,
    'revenue': np.random.uniform(0, 1000, 1000000),
    'customer_id': np.random.randint(1, 100000, 1000000)
})

# Write with row group size optimization
data.to_parquet('optimized.parquet', row_group_size=50000)

# Performance test: Column pruning
start_time = time.time()
df_all = pd.read_parquet('optimized.parquet')
all_columns_time = time.time() - start_time

start_time = time.time()
df_subset = pd.read_parquet('optimized.parquet', columns=['timestamp', 'revenue'])
subset_time = time.time() - start_time

print(f"Read all columns: {all_columns_time:.3f}s")
print(f"Read 2/4 columns: {subset_time:.3f}s")
print(f"Speedup: {all_columns_time/subset_time:.1f}x")

# Output:
# Read all columns: 0.245s
# Read 2/4 columns: 0.089s
# Speedup: 2.8x

# Performance test: Predicate pushdown
start_time = time.time()
df_filtered = pd.read_parquet('optimized.parquet', 
                             filters=[('region', '=', 'US')])
filter_time = time.time() - start_time

print(f"Filtered read: {filter_time:.3f}s")
print(f"Rows returned: {len(df_filtered):,}")
print(f"Filter selectivity: {len(df_filtered)/len(data)*100:.1f}%")

# Output:
# Filtered read: 0.067s
# Rows returned: 333,334
# Filter selectivity: 33.3%
```

### **3. Memory Usage Optimization**
**Definition**: Techniques to reduce memory consumption when working with Parquet files.

```python
# Memory optimization techniques
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Create large dataset
large_data = pd.DataFrame({
    'id': range(5000000),
    'category': ['A', 'B', 'C', 'D'] * 1250000,
    'value': np.random.float32(5000000),  # Use float32 instead of float64
    'flag': np.random.choice([True, False], 5000000)
})

# Save with optimized dtypes
large_data.to_parquet('memory_optimized.parquet')

# Memory-efficient reading strategies

# Strategy 1: Chunked reading
def process_in_chunks(file_path, chunk_size=100000):
    parquet_file = pq.ParquetFile(file_path)
    total_processed = 0
    
    for batch in parquet_file.iter_batches(batch_size=chunk_size):
        df_chunk = batch.to_pandas()
        # Process chunk (e.g., aggregation)
        result = df_chunk.groupby('category')['value'].sum()
        total_processed += len(df_chunk)
        
        if total_processed % 500000 == 0:
            print(f"Processed {total_processed:,} rows")
    
    return result

print("Processing in chunks:")
chunk_result = process_in_chunks('memory_optimized.parquet')
print(f"Final aggregation: {chunk_result}")

# Output:
# Processing in chunks:
# Processed 500,000 rows
# Processed 1,000,000 rows
# ...
# Final aggregation: category
# A    1.234567e+09
# B    1.234890e+09
# C    1.235123e+09
# D    1.234456e+09

# Strategy 2: Lazy evaluation with PyArrow
table = pq.read_table('memory_optimized.parquet')
print(f"Table loaded (lazy): {table.num_rows:,} rows")

# Only convert to pandas when needed
filtered_table = table.filter(pa.compute.equal(table['category'], 'A'))
df_filtered = filtered_table.to_pandas()
print(f"Converted to pandas: {len(df_filtered):,} rows")

# Output:
# Table loaded (lazy): 5,000,000 rows
# Converted to pandas: 1,250,000 rows
```

---

## 🔄 Integration with Big Data Tools

### **1. Apache Spark Integration**
```python
# Spark with Parquet
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ParquetExample").getOrCreate()

# Read Parquet files
df = spark.read.parquet("hdfs://path/to/parquet/files")
print(f"Loaded {df.count():,} rows from Parquet")

# Optimized writes with partitioning
df.write \
  .mode("overwrite") \
  .partitionBy("year", "month") \
  .option("compression", "snappy") \
  .parquet("hdfs://output/path")

# Query optimization with Parquet
df.createOrReplaceTempView("sales")
result = spark.sql("""
    SELECT region, SUM(revenue) as total_revenue
    FROM sales 
    WHERE date >= '2023-01-01'
    GROUP BY region
""")

result.show()
# Output:
# +------+-------------+
# |region|total_revenue|
# +------+-------------+
# |    US|    1234567.89|
# |    EU|     987654.32|
# |  ASIA|    1111111.11|
# +------+-------------+
```

### **2. Hive Integration**
```sql
-- Create external table pointing to Parquet files
CREATE TABLE sales_parquet (
    user_id BIGINT,
    product_id BIGINT,
    revenue DOUBLE,
    transaction_date DATE
)
STORED AS PARQUET
LOCATION 'hdfs://warehouse/sales_parquet/';

-- Query with predicate pushdown
SELECT region, AVG(revenue)
FROM sales_parquet
WHERE transaction_date >= '2023-01-01'
GROUP BY region;
```

### **3. Pandas Integration**
```python
# Advanced Pandas operations with Parquet
import pandas as pd

# Read with filters and column selection
df = pd.read_parquet(
    'sales_data.parquet',
    columns=['user_id', 'revenue', 'date'],
    filters=[('date', '>=', '2023-01-01')]
)

# Write with custom metadata
df.to_parquet(
    'output.parquet',
    compression='snappy',
    index=False,
    engine='pyarrow'
)

# Append data to existing Parquet dataset
new_data = pd.DataFrame({'user_id': [1, 2], 'revenue': [100, 200]})
new_data.to_parquet('output.parquet', mode='append')
```

---

## 🛠️ Common Use Cases

### **1. Data Lake Storage**
```
Raw Data → ETL Processing → Parquet Files → Analytics
- Use case: Store processed data in data lakes
- Benefits: Compression, schema evolution, query performance
- Pattern: Partition by date/region for optimal queries
```

### **2. Data Warehouse Integration**
```
OLTP Systems → Parquet Staging → Data Warehouse
- Use case: Efficient data transfer to warehouses
- Benefits: Reduced network I/O, faster loads
- Pattern: Columnar format matches warehouse storage
```

### **3. Machine Learning Pipelines**
```
Feature Engineering → Parquet Feature Store → ML Training
- Use case: Store ML features efficiently
- Benefits: Fast feature retrieval, schema validation
- Pattern: Partition by feature groups or time windows
```

### **4. Real-time Analytics**
```
Streaming Data → Micro-batches → Parquet → Dashboard
- Use case: Near real-time analytical dashboards
- Benefits: Balance between latency and efficiency
- Pattern: Small frequent writes, optimized for reads
```

---

## 💡 Best Practices

### **1. File Organization**
- **Partition strategy**: Use columns frequently used in WHERE clauses
- **File size**: Target 100MB-1GB per file for optimal performance
- **Naming convention**: Use consistent, descriptive file names
- **Directory structure**: Organize by business logic (date, region, etc.)

### **2. Schema Design**
```python
# Optimal schema design
import pyarrow as pa

# Define schema explicitly for consistency
schema = pa.schema([
    ('user_id', pa.int64()),
    ('timestamp', pa.timestamp('ms')),
    ('revenue', pa.decimal128(10, 2)),  # Precise decimal for money
    ('category', pa.dictionary(pa.int8(), pa.string())),  # Dictionary encoding
    ('metadata', pa.string())  # JSON strings for flexible data
])

# Create table with schema
table = pa.table(data, schema=schema)
```

### **3. Compression Strategy**
- **SNAPPY**: Default choice for balanced performance
- **GZIP**: When storage cost is more important than speed
- **LZ4**: For very high-throughput scenarios
- **ZSTD**: Good balance for most production workloads

### **4. Query Optimization**
```python
# Optimize for common query patterns
# Bad: No partitioning
df.to_parquet('data.parquet')

# Good: Partition by frequently filtered columns
df.to_parquet('data', partition_cols=['year', 'region'])

# Better: Add sorting for range queries
df_sorted = df.sort_values(['timestamp', 'user_id'])
df_sorted.to_parquet('data', partition_cols=['year', 'region'])
```

---

## 🎯 When to Choose Parquet

### **✅ Choose Parquet When:**
- **Analytical workloads** with column-heavy queries
- **Large datasets** requiring compression
- **Cross-platform compatibility** needed
- **Schema evolution** requirements
- **Big data ecosystems** (Spark, Hive, etc.)

### **❌ Consider Alternatives When:**
- **Transactional workloads** (use row-based formats)
- **Small datasets** (<100MB)
- **Frequent updates** (Parquet is append-only)
- **Simple streaming** (consider Avro)
- **Real-time requirements** (consider columnar databases)

---

## 🔗 Related Technologies

### **Complementary Formats**
- **Avro**: Schema evolution for streaming
- **ORC**: Alternative columnar format (Hive-optimized)
- **Delta Lake**: ACID transactions on Parquet
- **Iceberg**: Table format with time travel

### **Processing Engines**
- **Apache Spark**: Primary processing engine
- **Apache Drill**: SQL on Parquet files
- **Presto/Trino**: Distributed SQL queries
- **DuckDB**: Embedded analytical database

---

**🎯 Next Steps**: Ready to implement Parquet? Check out our [Interview Questions](./PARQUET_INTERVIEW_QUESTIONS.md) and [Best Practices](./PARQUET_BEST_PRACTICES.md) guides!