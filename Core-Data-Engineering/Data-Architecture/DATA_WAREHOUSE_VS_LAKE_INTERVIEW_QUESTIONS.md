# Data Warehouse vs Data Lake vs Lakehouse - Interview Questions

## 1. What is the difference between Data Warehouse and Data Lake?

**Answer:**
Data Warehouses and Data Lakes represent different approaches to storing and processing data.

**Data Warehouse:**
- **Structure**: Highly structured, schema-on-write
- **Data Types**: Processed, cleaned, structured data
- **Purpose**: Business intelligence, reporting, analytics
- **Performance**: Optimized for fast queries
- **Cost**: Higher storage and processing costs
- **Governance**: Strong data governance and quality

**Data Lake:**
- **Structure**: Raw, unstructured, schema-on-read
- **Data Types**: All data types (structured, semi-structured, unstructured)
- **Purpose**: Data exploration, machine learning, big data analytics
- **Performance**: Flexible but potentially slower queries
- **Cost**: Lower storage costs, pay-as-you-go processing
- **Governance**: Requires additional governance tools

**Comparison Table:**
```
Aspect          | Data Warehouse    | Data Lake
----------------|-------------------|------------------
Schema          | Schema-on-write   | Schema-on-read
Data Types      | Structured only   | All types
Processing      | ETL before load   | ELT after load
Query Speed     | Fast              | Variable
Storage Cost    | High              | Low
Flexibility     | Low               | High
Data Quality    | High              | Variable
Time to Insight | Longer setup      | Faster ingestion
```

**Use Cases:**
- **Data Warehouse**: Financial reporting, compliance, executive dashboards
- **Data Lake**: Data science, machine learning, IoT analytics, data exploration

## 2. What is a Data Lakehouse and how does it differ from Data Lake?

**Answer:**
A Data Lakehouse combines the flexibility of data lakes with the performance and reliability of data warehouses.

**Data Lakehouse Features:**
- **ACID Transactions**: Ensures data consistency
- **Schema Enforcement**: Optional schema validation
- **Time Travel**: Version control for data
- **Unified Batch and Streaming**: Single platform for all workloads
- **Open Formats**: Uses open standards (Delta Lake, Iceberg, Hudi)

**Key Technologies:**
- **Delta Lake**: ACID transactions on data lakes
- **Apache Iceberg**: Table format for analytics
- **Apache Hudi**: Incremental data processing

**Architecture Comparison:**
```
Data Lake:
Raw Data → Storage → Processing → Analytics

Data Warehouse:
Raw Data → ETL → Structured Storage → Analytics

Data Lakehouse:
Raw Data → Lakehouse Storage (with ACID) → Analytics
```

**Benefits of Lakehouse:**
- Eliminates data silos
- Reduces data duplication
- Supports all data types and workloads
- Lower total cost of ownership
- Simplified architecture

**Implementation Example:**
```python
# Delta Lake (Lakehouse) example
from delta.tables import DeltaTable

# Create Delta table with ACID properties
df.write.format("delta").save("/path/to/delta-table")

# Time travel - query historical versions
df_historical = spark.read.format("delta").option("versionAsOf", 0).load("/path/to/delta-table")

# ACID transactions - merge operations
deltaTable = DeltaTable.forPath(spark, "/path/to/delta-table")
deltaTable.alias("target").merge(
    source.alias("source"),
    "target.id = source.id"
).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
```

**When to Choose Each:**
- **Data Warehouse**: Traditional BI, regulatory compliance, well-defined requirements
- **Data Lake**: Exploratory analytics, diverse data types, cost-sensitive projects
- **Data Lakehouse**: Modern analytics, need for both flexibility and performance, unified platform requirements