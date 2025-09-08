# Hadoop MapReduce vs Spark - Interview Questions

## 1. What are the differences between Hadoop MapReduce and Spark?

**Answer:**
Both are big data processing frameworks but with different architectures and performance characteristics.

**Key Differences:**

**Processing Model:**
- **MapReduce**: Batch processing only, disk-based
- **Spark**: Batch + streaming + ML, memory-based

**Performance:**
- **MapReduce**: Slower due to disk I/O between stages
- **Spark**: 10-100x faster with in-memory processing

**Ease of Use:**
- **MapReduce**: Complex Java/Python code required
- **Spark**: High-level APIs in multiple languages

**Fault Tolerance:**
- **MapReduce**: Replication-based, slower recovery
- **Spark**: RDD lineage, faster recovery

**Resource Management:**
- **MapReduce**: Static resource allocation
- **Spark**: Dynamic resource allocation

**Comparison Table:**
```
Aspect          | MapReduce    | Spark
----------------|--------------|-------------
Speed           | Slower       | 10-100x faster
Memory Usage    | Disk-based   | Memory-based
APIs            | Low-level    | High-level
Real-time       | No           | Yes
Machine Learning| Limited      | MLlib included
Complexity      | High         | Lower
```

**Code Example:**
```python
# MapReduce (conceptual)
def mapper(line):
    for word in line.split():
        yield (word, 1)

def reducer(word, counts):
    yield (word, sum(counts))

# Spark
from pyspark import SparkContext
sc = SparkContext()
text = sc.textFile("file.txt")
counts = text.flatMap(lambda line: line.split()) \
             .map(lambda word: (word, 1)) \
             .reduceByKey(lambda a, b: a + b)
```

## 2. When would you choose MapReduce over Spark?

**Answer:**
Choose MapReduce when:
- Very large datasets that don't fit in cluster memory
- Simple batch processing jobs
- Existing Hadoop infrastructure
- Cost is primary concern (can use cheaper hardware)
- Long-running jobs where fault tolerance is critical

Choose Spark when:
- Interactive data analysis needed
- Real-time processing required
- Machine learning workloads
- Complex multi-stage pipelines
- Development speed is important