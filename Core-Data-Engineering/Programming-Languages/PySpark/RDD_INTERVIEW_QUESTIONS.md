# RDD (Resilient Distributed Datasets) - Interview Questions

## 1. What are RDDs and how do you use them?

**Answer:**
RDDs (Resilient Distributed Datasets) are the fundamental data structure in Apache Spark, representing immutable distributed collections of objects.

**Key Characteristics:**
- **Resilient**: Fault-tolerant through lineage
- **Distributed**: Partitioned across cluster nodes
- **Dataset**: Collection of objects

**RDD Operations:**

**Transformations (Lazy):**
```python
from pyspark import SparkContext
sc = SparkContext()

# Create RDD
data = [1, 2, 3, 4, 5]
rdd = sc.parallelize(data)

# Transformations
mapped_rdd = rdd.map(lambda x: x * 2)
filtered_rdd = rdd.filter(lambda x: x > 2)
flat_mapped_rdd = rdd.flatMap(lambda x: [x, x * 2])

# Key-value transformations
pairs_rdd = rdd.map(lambda x: (x, x * 2))
reduced_rdd = pairs_rdd.reduceByKey(lambda a, b: a + b)
```

**Actions (Eager):**
```python
# Actions trigger computation
result = mapped_rdd.collect()  # Return all elements
count = rdd.count()            # Count elements
first = rdd.first()            # Get first element
sample = rdd.take(3)           # Take first 3 elements
reduced = rdd.reduce(lambda a, b: a + b)  # Reduce to single value
```

**RDD Lineage:**
```python
# RDD maintains lineage for fault tolerance
print(rdd.toDebugString())
# Shows the DAG of transformations
```

## 2. What are DataFrames and how do you use them?

**Answer:**
DataFrames are higher-level abstractions built on RDDs with schema information and optimizations.

**Key Features:**
- **Schema**: Structured data with column names and types
- **Catalyst Optimizer**: Query optimization
- **Code Generation**: Improved performance
- **Language Integration**: SQL, Python, Scala, R

**DataFrame Operations:**
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg

spark = SparkSession.builder.appName("DataFrames").getOrCreate()

# Create DataFrame
data = [(1, "Alice", 25), (2, "Bob", 30), (3, "Charlie", 35)]
columns = ["id", "name", "age"]
df = spark.createDataFrame(data, columns)

# Transformations
filtered_df = df.filter(col("age") > 25)
selected_df = df.select("name", "age")
grouped_df = df.groupBy("age").count()

# SQL operations
df.createOrReplaceTempView("people")
result = spark.sql("SELECT name, age FROM people WHERE age > 25")
```

## 3. What are the differences between RDDs and DataFrames?

**Answer:**
RDDs and DataFrames serve different purposes with distinct advantages:

**Performance:**
- **RDD**: No optimization, manual tuning required
- **DataFrame**: Catalyst optimizer, automatic optimization

**Ease of Use:**
- **RDD**: Low-level API, more complex
- **DataFrame**: High-level API, SQL-like operations

**Type Safety:**
- **RDD**: Compile-time type safety (Scala/Java)
- **DataFrame**: Runtime type checking

**Memory Usage:**
- **RDD**: Higher memory overhead
- **DataFrame**: Optimized memory usage with Tungsten

**Schema:**
- **RDD**: No schema information
- **DataFrame**: Rich schema with metadata

**Comparison Table:**
```
Aspect          | RDD           | DataFrame
----------------|---------------|-------------
Abstraction     | Low-level     | High-level
Optimization    | Manual        | Automatic
Schema          | None          | Rich schema
Performance     | Slower        | Faster
API             | Functional    | SQL + Functional
Type Safety     | Compile-time  | Runtime
Memory          | Higher        | Optimized
```

**When to Use Each:**
- **Use RDD when**: Low-level control needed, unstructured data, complex operations
- **Use DataFrame when**: Structured data, SQL operations, performance critical