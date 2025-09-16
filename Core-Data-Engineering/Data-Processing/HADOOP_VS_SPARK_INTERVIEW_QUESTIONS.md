# Hadoop vs Spark Interview Questions

## 🎯 **Core Architecture Comparison**

### Q1: What are the fundamental differences between Hadoop and Spark?

**Answer:**
- **Hadoop:**
  - Disk-based processing (MapReduce)
  - Batch processing framework
  - Two-stage processing (Map and Reduce)
  - Data stored in HDFS between operations
  - Higher latency due to disk I/O

- **Spark:**
  - In-memory processing
  - Supports batch, streaming, and interactive processing
  - Multi-stage processing with DAG execution
  - Data cached in memory between operations
  - Lower latency for iterative algorithms

### Q2: How do their processing models differ?

**Answer:**
- **Hadoop MapReduce:**
  - Linear data flow: Input → Map → Shuffle → Reduce → Output
  - Each job writes intermediate results to disk
  - Limited to map and reduce operations
  - Good for simple, one-pass algorithms

- **Spark:**
  - Directed Acyclic Graph (DAG) execution
  - Lazy evaluation with query optimization
  - Rich set of transformations and actions
  - In-memory caching reduces I/O overhead

### Q3: Compare their performance characteristics

**Answer:**
- **Hadoop:**
  - Better for large-scale batch processing
  - Disk-based storage provides durability
  - Slower for iterative algorithms
  - Lower memory requirements

- **Spark:**
  - 10-100x faster for iterative algorithms
  - Better for machine learning workloads
  - Requires more memory
  - Faster for interactive queries

## 💾 **Storage and Memory Management**

### Q4: How do they handle data storage?

**Answer:**
- **Hadoop:**
  - Relies heavily on HDFS for storage
  - Intermediate data written to disk
  - Fault tolerance through data replication
  - Better for write-once, read-many scenarios

- **Spark:**
  - Can work with various storage systems (HDFS, S3, etc.)
  - In-memory storage with configurable persistence levels
  - Fault tolerance through RDD lineage
  - Better for iterative processing

### Q5: What are the memory management differences?

**Hadoop MapReduce:**
```java
// Memory configuration in mapred-site.xml
<property>
    <name>mapreduce.map.memory.mb</name>
    <value>2048</value>
</property>
<property>
    <name>mapreduce.reduce.memory.mb</name>
    <value>4096</value>
</property>
```

**Spark:**
```python
# Memory configuration
spark.conf.set("spark.executor.memory", "4g")
spark.conf.set("spark.executor.memoryFraction", "0.8")
spark.conf.set("spark.storage.memoryFraction", "0.6")

# Caching strategies
df.cache()  # Memory only
df.persist(StorageLevel.MEMORY_AND_DISK)  # Memory + disk fallback
```

## 🔄 **Programming Models**

### Q6: How do you implement word count in both?

**Hadoop MapReduce (Java):**
```java
// Mapper
public class WordCountMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
    public void map(LongWritable key, Text value, Context context) {
        String[] words = value.toString().split("\\s+");
        for (String word : words) {
            context.write(new Text(word), new IntWritable(1));
        }
    }
}

// Reducer
public class WordCountReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
    public void reduce(Text key, Iterable<IntWritable> values, Context context) {
        int sum = 0;
        for (IntWritable value : values) {
            sum += value.get();
        }
        context.write(key, new IntWritable(sum));
    }
}
```

**Spark (Python):**
```python
# Word count in Spark
text_file = spark.textFile("hdfs://...")
word_counts = text_file.flatMap(lambda line: line.split(" ")) \
                      .map(lambda word: (word, 1)) \
                      .reduceByKey(lambda a, b: a + b)
word_counts.collect()
```

### Q7: How do you handle complex data transformations?

**Hadoop MapReduce:**
- Requires multiple MapReduce jobs chained together
- Each job writes intermediate results to disk
- Complex to implement multi-stage algorithms
- Limited built-in operations

**Spark:**
```python
# Complex transformations in single pipeline
result = df.filter(df.age > 18) \
          .groupBy("department") \
          .agg(avg("salary").alias("avg_salary")) \
          .orderBy("avg_salary", ascending=False) \
          .limit(10)
```

## 🚀 **Performance and Optimization**

### Q8: What are the optimization techniques for each?

**Hadoop Optimization:**
- Combiner functions to reduce network traffic
- Appropriate input/output formats
- Optimal number of mappers and reducers
- Data locality optimization
- Compression techniques

**Spark Optimization:**
```python
# Partitioning optimization
df.repartition(200, "key_column")

# Caching frequently used data
df.cache()

# Broadcast small lookup tables
broadcast_var = spark.sparkContext.broadcast(small_dict)

# Avoid shuffling operations
df.mapPartitions(process_partition)
```

### Q9: How do they handle fault tolerance?

**Answer:**
- **Hadoop:**
  - Task-level fault tolerance
  - Automatic task restart on failure
  - Data replication in HDFS (default 3x)
  - JobTracker monitors TaskTrackers

- **Spark:**
  - RDD lineage for fault recovery
  - Automatic recomputation of lost partitions
  - Checkpointing for long lineage chains
  - Driver and executor failure handling

## 📊 **Use Cases and Scenarios**

### Q10: When should you choose Hadoop over Spark?

**Choose Hadoop when:**
- Processing very large datasets (PB scale)
- Simple batch processing requirements
- Limited memory resources
- Need proven stability for production workloads
- Cost is a primary concern
- Linear data processing workflows

### Q11: When should you choose Spark over Hadoop?

**Choose Spark when:**
- Need low-latency processing
- Iterative algorithms (ML, graph processing)
- Interactive data analysis
- Stream processing requirements
- Complex multi-stage pipelines
- Rich API requirements (SQL, ML, GraphX)

### Q12: How do they compare for different workloads?

**Batch Processing:**
- Hadoop: Better for simple, large-scale batch jobs
- Spark: Better for complex batch processing with multiple stages

**Stream Processing:**
- Hadoop: Limited streaming capabilities (requires additional tools)
- Spark: Native streaming support with Spark Streaming/Structured Streaming

**Machine Learning:**
- Hadoop: Requires external ML libraries (Mahout)
- Spark: Built-in MLlib with rich algorithms

**Interactive Analytics:**
- Hadoop: Not suitable for interactive queries
- Spark: Excellent for interactive analysis with Spark SQL

## 🔧 **Integration and Ecosystem**

### Q13: How do they integrate with other tools?

**Hadoop Ecosystem:**
- HDFS for storage
- YARN for resource management
- Hive for SQL-like queries
- HBase for NoSQL storage
- Oozie for workflow management
- Flume/Sqoop for data ingestion

**Spark Ecosystem:**
- Spark SQL for structured data processing
- Spark Streaming for real-time processing
- MLlib for machine learning
- GraphX for graph processing
- Can run on YARN, Mesos, or standalone

### Q14: Can Hadoop and Spark work together?

**Answer:**
Yes, they complement each other:
- Use HDFS as storage layer for Spark
- Run Spark on YARN cluster manager
- Use Hadoop for data ingestion, Spark for processing
- Leverage existing Hadoop infrastructure with Spark applications

```python
# Spark reading from HDFS
df = spark.read.parquet("hdfs://namenode:port/path/to/data")

# Spark writing to HDFS
df.write.mode("overwrite").parquet("hdfs://namenode:port/output/path")
```

## 💰 **Cost and Resource Considerations**

### Q15: How do their resource requirements compare?

**Answer:**
- **Hadoop:**
  - Lower memory requirements
  - Higher disk I/O requirements
  - More network bandwidth for shuffling
  - Better for commodity hardware

- **Spark:**
  - Higher memory requirements
  - Lower disk I/O (when data fits in memory)
  - Reduced network traffic with in-memory caching
  - Benefits from high-memory machines

### Q16: What are the operational considerations?

**Hadoop:**
- Mature ecosystem with extensive tooling
- Well-established operational practices
- Easier to debug with detailed logs
- Predictable resource usage

**Spark:**
- Newer technology with evolving best practices
- More complex memory management
- Dynamic resource allocation capabilities
- Requires Spark-specific monitoring tools

## 🎯 **Advanced Topics**

### Q17: How do they handle data skew?

**Hadoop:**
```java
// Custom partitioner to handle skew
public class CustomPartitioner extends Partitioner<Text, IntWritable> {
    @Override
    public int getPartition(Text key, IntWritable value, int numPartitions) {
        // Custom logic to distribute skewed keys
        return (key.hashCode() & Integer.MAX_VALUE) % numPartitions;
    }
}
```

**Spark:**
```python
# Salting technique for skewed keys
def add_salt(key, num_salts=10):
    salt = random.randint(0, num_salts - 1)
    return f"{key}_{salt}"

# Repartition to handle skew
df.repartition(col("key"))
```

### Q18: How do you monitor and tune performance?

**Hadoop Monitoring:**
- JobTracker web UI
- Hadoop metrics system
- Ganglia/Nagios integration
- Log analysis tools

**Spark Monitoring:**
```python
# Spark UI and metrics
spark.sparkContext.statusTracker()

# Custom metrics
spark.sparkContext.accumulator(0)

# Performance tuning
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
```

---

## 🎯 **Key Decision Factors**

| Factor | Hadoop | Spark |
|--------|--------|-------|
| **Processing Speed** | Slower (disk-based) | Faster (in-memory) |
| **Memory Usage** | Lower | Higher |
| **Fault Tolerance** | Data replication | RDD lineage |
| **Learning Curve** | Steeper (Java-heavy) | Easier (multiple languages) |
| **Use Cases** | Batch processing | Batch + Streaming + ML |
| **Maturity** | Very mature | Mature and growing |
| **Cost** | Lower hardware requirements | Higher memory costs |

Choose based on your specific requirements for performance, complexity, resources, and use cases.