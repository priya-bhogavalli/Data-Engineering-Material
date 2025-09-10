# RDD Interview Questions for Data Engineering

## 📋 Table of Contents

1. [RDD Fundamentals (1-15)](#rdd-fundamentals-1-15)
2. [RDD Operations & Transformations (16-30)](#rdd-operations--transformations-16-30)
3. [RDD vs DataFrame Comparison (31-45)](#rdd-vs-dataframe-comparison-31-45)
4. [Performance & Optimization (46-60)](#performance--optimization-46-60)

---

## RDD Fundamentals (1-15)

### 1. What is an RDD and what are its key characteristics?

**Answer**: RDD (Resilient Distributed Dataset) is the fundamental data structure in Apache Spark.

**Key Characteristics:**
- **Immutable**: Once created, cannot be changed
- **Distributed**: Data spread across cluster nodes
- **Fault-tolerant**: Can recover from node failures
- **Lazy evaluation**: Transformations computed only when actions called
- **In-memory**: Can cache data in memory for faster access

```python
# Create RDD from collection
rdd = spark.sparkContext.parallelize([1, 2, 3, 4, 5])

# Create RDD from file
text_rdd = spark.sparkContext.textFile("hdfs://path/to/file.txt")
```

### 2. How do RDDs achieve fault tolerance?

**Answer**: RDDs use **lineage** - they remember the sequence of transformations used to build them.

```python
# Lineage example
rdd1 = spark.sparkContext.parallelize([1, 2, 3, 4])
rdd2 = rdd1.map(lambda x: x * 2)
rdd3 = rdd2.filter(lambda x: x > 4)

# If partition lost, Spark can recompute using lineage
print(rdd3.toDebugString())  # Shows lineage graph
```

### 3. What are the different ways to create RDDs?

**Answer**: Multiple RDD creation methods:

```python
# From Python collection
rdd1 = sc.parallelize([1, 2, 3, 4, 5])

# From external file
rdd2 = sc.textFile("file.txt")

# From existing RDD
rdd3 = rdd1.map(lambda x: x * 2)

# From DataFrame
df = spark.createDataFrame([(1, "a"), (2, "b")])
rdd4 = df.rdd
```

## RDD Operations & Transformations (16-30)

### 4. Explain the difference between transformations and actions in RDDs.

**Answer**: 
- **Transformations**: Lazy operations that create new RDDs
- **Actions**: Trigger computation and return results

```python
# Transformations (lazy)
rdd = sc.parallelize([1, 2, 3, 4, 5])
mapped_rdd = rdd.map(lambda x: x * 2)      # Lazy
filtered_rdd = mapped_rdd.filter(lambda x: x > 4)  # Lazy

# Actions (trigger execution)
result = filtered_rdd.collect()  # Action - executes pipeline
count = filtered_rdd.count()     # Action
first = filtered_rdd.first()     # Action
```

### 5. What are the most common RDD transformations?

**Answer**: Essential RDD transformations:

```python
rdd = sc.parallelize([1, 2, 3, 4, 5])

# map - transform each element
mapped = rdd.map(lambda x: x * 2)

# filter - select elements
filtered = rdd.filter(lambda x: x > 2)

# flatMap - flatten results
text_rdd = sc.parallelize(["hello world", "spark rdd"])
words = text_rdd.flatMap(lambda line: line.split(" "))

# distinct - remove duplicates
unique = sc.parallelize([1, 1, 2, 2, 3]).distinct()

# union - combine RDDs
rdd2 = sc.parallelize([6, 7, 8])
combined = rdd.union(rdd2)

# join - join paired RDDs
pairs1 = sc.parallelize([("a", 1), ("b", 2)])
pairs2 = sc.parallelize([("a", 3), ("c", 4)])
joined = pairs1.join(pairs2)
```

### 6. How do you work with key-value pair RDDs?

**Answer**: Paired RDDs enable key-based operations:

```python
# Create paired RDD
pairs = sc.parallelize([("apple", 1), ("banana", 2), ("apple", 3)])

# reduceByKey - aggregate by key
totals = pairs.reduceByKey(lambda a, b: a + b)

# groupByKey - group values by key
grouped = pairs.groupByKey()

# mapValues - transform only values
doubled = pairs.mapValues(lambda x: x * 2)

# keys and values
keys_only = pairs.keys()
values_only = pairs.values()

# sortByKey
sorted_pairs = pairs.sortByKey()
```

## RDD vs DataFrame Comparison (31-45)

### 7. When should you use RDDs instead of DataFrames?

**Answer**: Use RDDs when:

```python
# 1. Working with unstructured data
log_rdd = sc.textFile("logs.txt")
parsed_logs = log_rdd.map(parse_log_line)  # Custom parsing

# 2. Need low-level transformations
complex_rdd = rdd.mapPartitions(complex_partition_logic)

# 3. Working with non-tabular data
graph_rdd = sc.parallelize([(1, [2, 3]), (2, [3, 4])])

# 4. Performance-critical operations with known data patterns
optimized_rdd = rdd.mapPartitionsWithIndex(partition_aware_logic)
```

**Use DataFrames for:**
- Structured/semi-structured data
- SQL operations
- Catalyst optimizer benefits
- Better performance in most cases

### 8. How do you convert between RDDs and DataFrames?

**Answer**: Conversion methods:

```python
# RDD to DataFrame
rdd = sc.parallelize([(1, "John", 25), (2, "Jane", 30)])

# Method 1: With schema
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
schema = StructType([
    StructField("id", IntegerType()),
    StructField("name", StringType()),
    StructField("age", IntegerType())
])
df = spark.createDataFrame(rdd, schema)

# Method 2: Infer schema
df = rdd.toDF(["id", "name", "age"])

# DataFrame to RDD
rdd_from_df = df.rdd
```

## Performance & Optimization (46-60)

### 9. How do you optimize RDD performance?

**Answer**: Key optimization strategies:

```python
# 1. Persistence/Caching
from pyspark import StorageLevel
rdd.persist(StorageLevel.MEMORY_AND_DISK)
rdd.cache()  # Same as MEMORY_ONLY

# 2. Avoid groupByKey, use reduceByKey
# Bad
grouped = pairs.groupByKey().mapValues(sum)
# Good
reduced = pairs.reduceByKey(lambda a, b: a + b)

# 3. Use mapPartitions for expensive operations
def expensive_operation(iterator):
    # Setup expensive resources once per partition
    connection = create_connection()
    for record in iterator:
        yield process_with_connection(record, connection)

result = rdd.mapPartitions(expensive_operation)

# 4. Broadcast variables for lookup tables
broadcast_dict = sc.broadcast({"key1": "value1", "key2": "value2"})
enriched = rdd.map(lambda x: (x, broadcast_dict.value.get(x)))
```

### 10. What are the different persistence levels in RDDs?

**Answer**: Storage levels for caching:

```python
from pyspark import StorageLevel

# Memory only (default for cache())
rdd.persist(StorageLevel.MEMORY_ONLY)

# Memory and disk spillover
rdd.persist(StorageLevel.MEMORY_AND_DISK)

# Serialized in memory (more compact)
rdd.persist(StorageLevel.MEMORY_ONLY_SER)

# Disk only
rdd.persist(StorageLevel.DISK_ONLY)

# With replication
rdd.persist(StorageLevel.MEMORY_AND_DISK_2)

# Check if cached
print(rdd.is_cached)

# Unpersist when done
rdd.unpersist()
```

### 11. How do you handle partitioning in RDDs?

**Answer**: Partitioning strategies:

```python
# Check partitions
print(f"Partitions: {rdd.getNumPartitions()}")

# Repartition (causes shuffle)
repartitioned = rdd.repartition(10)

# Coalesce (reduce partitions, minimal shuffle)
coalesced = rdd.coalesce(5)

# Custom partitioner for key-value RDDs
from pyspark import HashPartitioner
partitioned = pairs.partitionBy(4, HashPartitioner(4))

# mapPartitionsWithIndex - partition-aware processing
def process_partition(index, iterator):
    return [f"Partition {index}: {list(iterator)}"]

result = rdd.mapPartitionsWithIndex(process_partition)
```

### 12. What are accumulators and broadcast variables?

**Answer**: Shared variables for distributed computing:

```python
# Accumulators - write-only variables for aggregation
counter = sc.accumulator(0)
error_lines = sc.accumulator(0)

def process_line(line):
    counter.add(1)
    if "ERROR" in line:
        error_lines.add(1)
    return line.upper()

processed = text_rdd.map(process_line)
processed.collect()  # Trigger action to update accumulators

print(f"Total lines: {counter.value}")
print(f"Error lines: {error_lines.value}")

# Broadcast variables - read-only shared data
lookup_table = {"A": 1, "B": 2, "C": 3}
broadcast_lookup = sc.broadcast(lookup_table)

def enrich_data(record):
    return (record, broadcast_lookup.value.get(record, 0))

enriched = rdd.map(enrich_data)
```

### 13. How do you debug RDD operations?

**Answer**: Debugging techniques:

```python
# 1. Check lineage
print(rdd.toDebugString())

# 2. Sample data
sample_data = rdd.sample(False, 0.1).collect()

# 3. Take first few elements
first_elements = rdd.take(10)

# 4. Count elements
total_count = rdd.count()

# 5. Glom - see partition contents
partition_contents = rdd.glom().collect()

# 6. Use foreach for side effects (debugging)
def debug_print(x):
    print(f"Processing: {x}")

rdd.foreach(debug_print)  # Use sparingly in production
```

### 14. What are the limitations of RDDs?

**Answer**: RDD limitations:

1. **No automatic optimization**: No Catalyst optimizer
2. **No schema**: Type safety issues, runtime errors
3. **Serialization overhead**: Python objects serialization cost
4. **Limited SQL support**: No native SQL operations
5. **Memory management**: Manual cache management required

```python
# Example showing DataFrame advantage
# RDD approach - no optimization
rdd_result = rdd.filter(lambda x: x.age > 25).map(lambda x: x.salary).reduce(lambda a, b: a + b)

# DataFrame approach - optimized by Catalyst
df_result = df.filter(col("age") > 25).agg(sum("salary")).collect()[0][0]
```

### 15. How do you handle large datasets with RDDs?

**Answer**: Strategies for large datasets:

```python
# 1. Partition appropriately
large_rdd = sc.textFile("large_file.txt", minPartitions=100)

# 2. Use efficient transformations
# Avoid collect() on large datasets
# Use take() or sample() instead
sample = large_rdd.sample(False, 0.01).collect()

# 3. Persist strategically
frequently_used = large_rdd.filter(important_filter).persist()

# 4. Use mapPartitions for batch processing
def batch_process(iterator):
    batch = list(iterator)
    # Process entire partition at once
    return process_batch(batch)

result = large_rdd.mapPartitions(batch_process)

# 5. Write to distributed storage
large_rdd.saveAsTextFile("hdfs://output/path")
```