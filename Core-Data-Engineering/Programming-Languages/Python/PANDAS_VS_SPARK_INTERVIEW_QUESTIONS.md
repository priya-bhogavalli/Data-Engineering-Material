# Pandas vs Spark Interview Questions

## 🎯 **Core Comparison Questions**

### Q1: When would you choose Pandas over Spark and vice versa?

**Answer:**
- **Choose Pandas when:**
  - Dataset fits in memory (< 10GB typically)
  - Single machine processing is sufficient
  - Need rich data manipulation and analysis features
  - Working with structured data analysis and exploration
  - Need immediate results for small to medium datasets

- **Choose Spark when:**
  - Dataset is too large for single machine memory
  - Need distributed processing across multiple nodes
  - Working with big data (100GB+ datasets)
  - Need fault tolerance and scalability
  - Processing streaming data

### Q2: What are the key architectural differences?

**Answer:**
- **Pandas:**
  - Single-threaded, runs on one machine
  - In-memory processing
  - Eager evaluation
  - Rich API for data manipulation

- **Spark:**
  - Distributed computing framework
  - Lazy evaluation with optimized execution plans
  - Fault-tolerant with RDD lineage
  - Can process data larger than memory

### Q3: Compare performance characteristics

**Answer:**
- **Pandas:**
  - Faster for small datasets (< 1GB)
  - No network overhead
  - Direct memory access
  - Limited by single machine resources

- **Spark:**
  - Better for large datasets (> 10GB)
  - Parallel processing across nodes
  - Network overhead for data shuffling
  - Scales horizontally

## 🔄 **Data Processing Comparison**

### Q4: How do you handle missing data in both?

**Pandas:**
```python
# Drop missing values
df.dropna()

# Fill missing values
df.fillna(0)
df.fillna(method='forward')

# Check for missing values
df.isnull().sum()
```

**Spark:**
```python
# Drop missing values
df.na.drop()

# Fill missing values
df.na.fill(0)
df.na.fill({'column1': 0, 'column2': 'unknown'})

# Check for missing values
df.select([count(when(col(c).isNull(), c)).alias(c) for c in df.columns]).show()
```

### Q5: How do you perform group operations?

**Pandas:**
```python
# Group by and aggregate
df.groupby('category').agg({
    'sales': 'sum',
    'quantity': 'mean'
})

# Multiple aggregations
df.groupby('category')['sales'].agg(['sum', 'mean', 'count'])
```

**Spark:**
```python
from pyspark.sql.functions import sum, avg, count

# Group by and aggregate
df.groupBy('category').agg(
    sum('sales').alias('total_sales'),
    avg('quantity').alias('avg_quantity')
)

# Multiple aggregations
df.groupBy('category').agg(
    sum('sales'),
    avg('sales'),
    count('sales')
)
```

## 💾 **Memory Management**

### Q6: How does memory management differ?

**Answer:**
- **Pandas:**
  - Loads entire dataset into RAM
  - Memory usage = dataset size + overhead
  - Limited by single machine memory
  - Can use chunking for large files

- **Spark:**
  - Distributed memory across cluster
  - Lazy evaluation reduces memory pressure
  - Spills to disk when memory is full
  - Memory management handled by Spark engine

### Q7: How do you optimize memory usage?

**Pandas:**
```python
# Use appropriate data types
df['category'] = df['category'].astype('category')
df['id'] = df['id'].astype('int32')

# Process in chunks
for chunk in pd.read_csv('large_file.csv', chunksize=10000):
    process_chunk(chunk)

# Use memory-efficient operations
df.query('sales > 1000')  # Instead of df[df['sales'] > 1000]
```

**Spark:**
```python
# Cache frequently used DataFrames
df.cache()

# Partition data appropriately
df.repartition(200)

# Use broadcast for small lookup tables
broadcast_df = broadcast(small_df)
```

## 🚀 **Performance Optimization**

### Q8: What are the performance optimization techniques?

**Pandas:**
- Use vectorized operations instead of loops
- Leverage NumPy operations
- Use appropriate data types
- Process data in chunks for large datasets
- Use `query()` method for filtering

**Spark:**
- Optimize partitioning
- Cache intermediate results
- Use broadcast joins for small tables
- Avoid shuffling operations
- Use appropriate file formats (Parquet)

### Q9: How do you handle joins in both frameworks?

**Pandas:**
```python
# Inner join
result = df1.merge(df2, on='key', how='inner')

# Left join with different column names
result = df1.merge(df2, left_on='id', right_on='user_id', how='left')

# Multiple key join
result = df1.merge(df2, on=['key1', 'key2'])
```

**Spark:**
```python
# Inner join
result = df1.join(df2, df1.key == df2.key, 'inner')

# Left join
result = df1.join(df2, df1.id == df2.user_id, 'left')

# Multiple key join
result = df1.join(df2, (df1.key1 == df2.key1) & (df1.key2 == df2.key2))
```

## 📊 **Data Types and Schema**

### Q10: How do you handle schema differences?

**Answer:**
- **Pandas:**
  - Dynamic typing, infers types automatically
  - Can change types on the fly
  - Flexible schema evolution

- **Spark:**
  - Structured data with defined schema
  - Schema enforcement and evolution
  - Better for data quality and consistency

### Q11: How do you work with different file formats?

**Pandas:**
```python
# CSV
df = pd.read_csv('file.csv')
df.to_csv('output.csv')

# JSON
df = pd.read_json('file.json')
df.to_json('output.json')

# Parquet
df = pd.read_parquet('file.parquet')
df.to_parquet('output.parquet')
```

**Spark:**
```python
# CSV
df = spark.read.csv('file.csv', header=True, inferSchema=True)
df.write.csv('output.csv')

# JSON
df = spark.read.json('file.json')
df.write.json('output.json')

# Parquet
df = spark.read.parquet('file.parquet')
df.write.parquet('output.parquet')
```

## 🔧 **Integration and Ecosystem**

### Q12: How do they integrate with other tools?

**Answer:**
- **Pandas:**
  - Integrates well with scikit-learn, matplotlib, seaborn
  - Works with Jupyter notebooks
  - Good for data science workflows
  - Limited scalability

- **Spark:**
  - Integrates with Hadoop ecosystem
  - Works with MLlib for machine learning
  - Connects to various data sources
  - Better for production data pipelines

### Q13: When would you use both together?

**Answer:**
- Use Spark for large-scale data processing and aggregation
- Use Pandas for final analysis and visualization on smaller result sets
- Convert Spark DataFrame to Pandas for detailed analysis:
```python
# Spark processing
large_df = spark.read.parquet('large_dataset.parquet')
aggregated = large_df.groupBy('category').sum('sales')

# Convert to Pandas for analysis
pandas_df = aggregated.toPandas()
pandas_df.plot()
```

## 🎯 **Best Practices**

### Q14: What are the best practices for each?

**Pandas Best Practices:**
- Use vectorized operations
- Avoid loops when possible
- Use appropriate data types
- Process data in chunks for large files
- Use `query()` for complex filtering

**Spark Best Practices:**
- Design for immutability
- Cache intermediate results
- Optimize partitioning
- Use appropriate join strategies
- Monitor and tune Spark configurations

### Q15: How do you debug performance issues?

**Pandas:**
```python
# Profile memory usage
df.info(memory_usage='deep')

# Time operations
%timeit df.groupby('category').sum()

# Use profiling tools
import cProfile
cProfile.run('df.groupby("category").sum()')
```

**Spark:**
```python
# Check execution plan
df.explain()

# Monitor Spark UI
# Access at http://driver:4040

# Cache analysis
df.cache()
df.count()  # Trigger caching
```

## 🚀 **Advanced Scenarios**

### Q16: How do you handle streaming data?

**Answer:**
- **Pandas:** Not designed for streaming, use chunking or external tools
- **Spark:** Native streaming support with Structured Streaming

**Spark Streaming:**
```python
# Read streaming data
stream_df = spark.readStream.format('kafka').load()

# Process streaming data
result = stream_df.groupBy('key').count()

# Write streaming output
query = result.writeStream.outputMode('complete').format('console').start()
```

### Q17: How do you handle machine learning workflows?

**Pandas + Scikit-learn:**
```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

X_train, X_test, y_train, y_test = train_test_split(X, y)
model = RandomForestClassifier()
model.fit(X_train, y_train)
```

**Spark + MLlib:**
```python
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier

assembler = VectorAssembler(inputCols=features, outputCol='features')
rf = RandomForestClassifier(featuresCol='features', labelCol='label')
pipeline = Pipeline(stages=[assembler, rf])
model = pipeline.fit(train_df)
```

---

## 🎯 **Key Takeaways**

1. **Size Matters**: Use Pandas for small-medium data, Spark for big data
2. **Performance**: Pandas faster for small datasets, Spark scales better
3. **Memory**: Pandas requires data to fit in memory, Spark distributes across cluster
4. **Ecosystem**: Pandas better for data science, Spark better for production pipelines
5. **Learning Curve**: Pandas easier to learn, Spark requires distributed computing knowledge

Choose based on your specific use case, data size, and infrastructure requirements.