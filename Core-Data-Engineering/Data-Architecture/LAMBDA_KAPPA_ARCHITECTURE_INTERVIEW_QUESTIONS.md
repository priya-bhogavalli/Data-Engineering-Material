# Lambda and Kappa Architecture - Interview Questions

## 1. What are Lambda and Kappa architectures?

**Answer:**
Lambda and Kappa are architectural patterns for processing big data with different approaches to handling batch and stream processing.

**Lambda Architecture:**
- **Components**: Batch layer, speed layer, serving layer
- **Principle**: Process data through both batch and stream processing
- **Goal**: Provide comprehensive and accurate views of data

**Architecture Diagram:**
```
Data Sources → Batch Layer (Hadoop/Spark) → Serving Layer → Query Interface
            → Speed Layer (Storm/Kafka) ↗
```

**Layers:**
1. **Batch Layer**: Processes complete datasets, high latency but accurate
2. **Speed Layer**: Processes real-time data, low latency but approximate
3. **Serving Layer**: Merges batch and speed layer results

**Kappa Architecture:**
- **Components**: Stream processing only
- **Principle**: Everything is a stream, including batch data
- **Goal**: Simplify architecture by using only stream processing

**Architecture Diagram:**
```
Data Sources → Stream Processing (Kafka/Spark Streaming) → Serving Layer → Query Interface
```

**Key Differences:**
```
Aspect           | Lambda        | Kappa
-----------------|---------------|-------------
Complexity       | High          | Low
Data Processing  | Batch + Stream| Stream Only
Latency          | Mixed         | Low
Consistency      | Eventually    | Eventually
Maintenance      | Complex       | Simple
Use Cases        | Mixed Workload| Stream-First
```

## 2. When would you choose Lambda vs Kappa architecture?

**Answer:**
Choose based on requirements and organizational capabilities:

**Choose Lambda When:**
- Need both real-time and batch processing
- Historical data reprocessing is critical
- Different SLAs for real-time vs batch
- Complex analytics requiring full dataset
- Existing batch infrastructure

**Choose Kappa When:**
- Stream-first organization
- Simpler architecture preferred
- Real-time processing is primary need
- Team expertise in stream processing
- Event-driven applications

**Implementation Examples:**
```python
# Lambda Architecture - Batch Layer
def batch_processing():
    df = spark.read.parquet("hdfs://data/")
    result = df.groupBy("category").sum("amount")
    result.write.mode("overwrite").parquet("hdfs://batch_views/")

# Lambda Architecture - Speed Layer  
def speed_processing():
    stream = spark.readStream.kafka("topic")
    result = stream.groupBy("category").sum("amount")
    result.writeStream.outputMode("update").start()

# Kappa Architecture - Stream Only
def kappa_processing():
    stream = spark.readStream.kafka("topic")
    # Process both real-time and historical data as streams
    result = stream.groupBy(window("timestamp", "1 hour"), "category").sum("amount")
    result.writeStream.outputMode("append").start()
```