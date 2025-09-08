# Pandas vs Spark DataFrames - Interview Questions

## 1. Is Python pandas DataFrames and Spark DataFrames the same? What are the differences?

**Answer:**
No, pandas and Spark DataFrames are fundamentally different despite similar APIs.

**Key Differences:**

**Execution Model:**
- **Pandas**: Single-machine, eager evaluation
- **Spark**: Distributed, lazy evaluation

**Memory Usage:**
- **Pandas**: Loads entire dataset in memory
- **Spark**: Processes data in partitions across cluster

**Scalability:**
- **Pandas**: Limited by single machine memory
- **Spark**: Scales horizontally across cluster

**Performance:**
- **Pandas**: Faster for small datasets (<1GB)
- **Spark**: Better for large datasets (>10GB)

**API Differences:**
```python
# Pandas
import pandas as pd
df = pd.read_csv('file.csv')
result = df.groupby('column').sum()

# Spark
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
df = spark.read.csv('file.csv', header=True)
result = df.groupBy('column').sum()
```

**When to Use Each:**
- **Pandas**: Data analysis, prototyping, small datasets
- **Spark**: Big data processing, ETL pipelines, distributed computing

## 2. How do you convert between pandas and Spark DataFrames?

**Answer:**
```python
# Pandas to Spark
pandas_df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
spark_df = spark.createDataFrame(pandas_df)

# Spark to Pandas
spark_df = spark.range(1000).toDF("number")
pandas_df = spark_df.toPandas()
```

**Considerations:**
- Memory limitations when converting large Spark DataFrames
- Data type compatibility issues
- Performance impact of data transfer