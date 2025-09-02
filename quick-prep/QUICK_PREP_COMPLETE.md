# 🚀 Complete Data Engineering Quick Prep Guide

> **Ultimate preparation resource for data engineering interviews and rapid skill review**

## 🎯 **Navigation**
- [🔥 Emergency Prep (2-4 hours)](#-emergency-prep-2-4-hours)
- [📚 Core Technologies Reference](#-core-technologies-reference)
- [🏗️ Architecture & Concepts](#️-architecture--concepts)
- [💻 Essential Code Snippets](#-essential-code-snippets)
- [🎯 Top Interview Questions](#-top-interview-questions)

---

# 🔥 Emergency Prep (2-4 hours)

## ⚡ **Immediate Actions (30 mins)**
1. Review Python basics & SQL commands
2. Scan AWS services overview
3. Quick read Data Engineering fundamentals
4. Practice top 10 interview questions

## 🎯 **Top 10 Must-Know Questions with Answers**

### 1. **"Explain the difference between OLTP and OLAP"**
**Answer:**
- **OLTP (Online Transaction Processing)**:
  - Real-time operational data processing
  - Normalized database design (3NF)
  - High volume of short transactions
  - ACID compliance critical
  - Examples: Banking systems, e-commerce

- **OLAP (Online Analytical Processing)**:
  - Historical data analysis
  - Denormalized design (star/snowflake schema)
  - Complex queries, aggregations
  - Read-heavy workloads
  - Examples: Data warehouses, reporting

### 2. **"How would you handle duplicate data in a pipeline?"**
**Answer:**
- **Prevention**: Use unique constraints, proper data modeling
- **Detection**: Data profiling, duplicate checks in ETL
- **Removal**: 
  ```sql
  DELETE FROM table WHERE id NOT IN (
    SELECT MIN(id) FROM table GROUP BY unique_columns
  );
  ```
  ```python
  df.drop_duplicates(subset=['key_columns'], keep='first')
  ```
- **Idempotency**: Design pipelines to handle re-runs safely

### 3. **"What's the difference between batch and stream processing?"**
**Answer:**
- **Batch Processing**:
  - Process large volumes at scheduled intervals
  - Higher latency, higher throughput
  - Tools: Spark, Hadoop, Airflow
  - Use cases: ETL jobs, reporting, ML training

- **Stream Processing**:
  - Process data in real-time as it arrives
  - Lower latency, continuous processing
  - Tools: Kafka, Flink, Kinesis
  - Use cases: Fraud detection, monitoring, real-time analytics

### 4. **"Explain database normalization vs denormalization"**
**Answer:**
- **Normalization**:
  - Reduces data redundancy
  - Multiple related tables
  - Better for OLTP (insert/update heavy)
  - 1NF → 2NF → 3NF progression

- **Denormalization**:
  - Optimizes for read performance
  - Fewer JOINs required
  - Better for OLAP (read-heavy)
  - Trade storage for query speed

### 5. **"How do you optimize a slow SQL query?"**
**Answer:**
1. **Analyze execution plan**: Use EXPLAIN
2. **Add indexes**: On WHERE, JOIN, ORDER BY columns
3. **Rewrite query**: 
   - Avoid SELECT *
   - Use appropriate JOINs
   - Filter early with WHERE
4. **Partitioning**: For large tables
5. **Statistics**: Update table statistics
6. **Query hints**: As last resort

### 6. **"What's the CAP theorem?"**
**Answer:**
In distributed systems, you can only guarantee 2 out of 3:
- **Consistency**: All nodes see same data simultaneously
- **Availability**: System remains operational
- **Partition tolerance**: System continues despite network failures

Examples:
- **CP**: Traditional RDBMS (PostgreSQL)
- **AP**: NoSQL databases (Cassandra)
- **CA**: Single-node systems (not distributed)

### 7. **"Explain eventual consistency"**
**Answer:**
- System will become consistent over time
- Immediate consistency not guaranteed
- Trade-off for availability and partition tolerance
- Common in distributed NoSQL systems
- Example: DNS propagation, social media feeds

### 8. **"How would you design a data pipeline for real-time analytics?"**
**Answer:**
```
Data Sources → Kafka → Stream Processing → Storage → Visualization
     ↓           ↓           ↓              ↓           ↓
  Web logs    Message     Spark         ClickHouse   Grafana
  APIs        Queue      Streaming      TimescaleDB  Tableau
  Databases   Buffer     Flink          Elasticsearch Kibana
```

Key considerations:
- **Scalability**: Horizontal scaling
- **Fault tolerance**: Replication, checkpointing
- **Monitoring**: Metrics, alerting
- **Schema evolution**: Handle data changes

### 9. **"What's the difference between Data Lake and Data Warehouse?"**
**Answer:**

| Aspect | Data Lake | Data Warehouse |
|--------|-----------|----------------|
| **Data** | Raw, unprocessed | Processed, structured |
| **Schema** | Schema-on-read | Schema-on-write |
| **Cost** | Lower storage cost | Higher storage cost |
| **Flexibility** | High | Lower |
| **Query Performance** | Variable | Optimized |
| **Use Cases** | Exploration, ML | Reporting, BI |

### 10. **"How do you ensure data quality?"**
**Answer:**
- **Data Profiling**: Understand data characteristics
- **Validation Rules**: 
  ```python
  assert df['age'].between(0, 120).all()
  assert df['email'].str.contains('@').all()
  ```
- **Monitoring**: Track data quality metrics
- **Data Lineage**: Understand data flow
- **Testing**: Unit tests for transformations
- **Alerts**: Notify on quality issues

## 🗣️ **Behavioral Prep (30 mins)**

### **"Tell me about a challenging data project"**
**Structure your answer:**
1. **Situation**: Context and challenge
2. **Task**: Your responsibility
3. **Action**: What you did (be specific)
4. **Result**: Outcome and impact

### **"How do you handle conflicting requirements?"**
**Key points:**
- Understand all stakeholder needs
- Communicate trade-offs clearly
- Propose alternative solutions
- Document decisions and rationale

## 🚨 **Last-Minute Checklist**

### **Technical Concepts to Memorize**
- ACID properties: Atomicity, Consistency, Isolation, Durability
- Data modeling: Star schema, snowflake schema, data vault
- Big data 4 Vs: Volume, Velocity, Variety, Veracity
- Lambda architecture: Batch + Speed + Serving layers

### **Common Metrics**
- **Latency**: Time to process single record
- **Throughput**: Records processed per second
- **Availability**: Uptime percentage (99.9% = 8.76 hours downtime/year)
- **RPO/RTO**: Recovery Point/Time Objectives

### **Quick Mental Math**
- 1 TB = 1,000 GB = 1,000,000 MB
- 1 million records ≈ 100MB (depending on schema)
- Network: 1 Gbps = 125 MB/s
- SSD: ~500 MB/s, HDD: ~100 MB/s

---

# 📚 Core Technologies Reference

## 🐍 **Python Essentials**
```python
# Data Structures
data = [1, 2, 3]                    # Lists - ordered, mutable
config = {'host': 'localhost'}      # Dicts - key-value pairs
unique_ids = {1, 2, 3}              # Sets - unique values

# List comprehensions
squares = [x**2 for x in range(10) if x % 2 == 0]

# Pandas Operations
df = pd.read_csv('data.csv')
df.head()                           # First 5 rows
df.info()                           # Data types & null counts
df.describe()                       # Summary statistics
df.groupby('column').sum()          # Group and aggregate
df.merge(df2, on='key')             # Join dataframes
df.drop_duplicates()                # Remove duplicates

# Error Handling
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    result = default_value
```

## 🗄️ **SQL Essentials**
```sql
-- Window Functions
SELECT name, salary,
       RANK() OVER (PARTITION BY dept ORDER BY salary DESC) as rank
FROM employees;

-- CTEs (Common Table Expressions)
WITH monthly_sales AS (
    SELECT DATE_TRUNC('month', order_date) as month,
           SUM(amount) as total_sales
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT month, total_sales,
       LAG(total_sales) OVER (ORDER BY month) as prev_month
FROM monthly_sales;

-- JOINs
SELECT a.*, b.name
FROM orders a
LEFT JOIN customers b ON a.customer_id = b.id;
```

## ⚡ **PySpark Essentials**
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count, avg

# Initialize Spark
spark = SparkSession.builder.appName("DataEngineering").getOrCreate()

# Basic operations
df.show(10)                         # Display first 10 rows
df.printSchema()                    # Show schema
df.count()                          # Count rows
df.select("col1", "col2")           # Select columns
df.filter(col("age") > 25)          # Filter rows
df.groupBy("department").agg(avg("salary"))  # Group and aggregate

# Joins
df1.join(df2, "common_column")                    # Inner join (default)
df1.join(df2, "key", "left")                      # Left outer

# Performance Optimization
df.cache()                          # Cache for reused DataFrames
df.repartition(200)                 # Increase partitions
df.coalesce(10)                     # Decrease partitions (no shuffle)
```

## ☁️ **Cloud Platforms**

### **AWS Services**
| Service | Purpose | Key Use Cases |
|---------|---------|---------------|
| **S3** | Object storage | Data lake, backup, static hosting |
| **Glue** | ETL service | Data cataloging, serverless ETL |
| **Athena** | Query service | SQL queries on S3 data |
| **Redshift** | Data warehouse | Analytics, OLAP queries |
| **Kinesis** | Streaming data | Real-time data ingestion |
| **EMR** | Big data platform | Spark, Hadoop clusters |

### **Azure Services**
| Service | Purpose | AWS Equivalent |
|---------|---------|----------------|
| **Blob Storage** | Object storage | S3 |
| **Data Factory** | ETL/ELT | Glue |
| **Synapse Analytics** | Data warehouse | Redshift |
| **Databricks** | Analytics platform | EMR |

### **GCP Services**
| Service | Purpose | AWS Equivalent |
|---------|---------|----------------|
| **Cloud Storage** | Object storage | S3 |
| **BigQuery** | Data warehouse | Redshift |
| **Dataflow** | Stream/batch processing | Kinesis Analytics |
| **Dataproc** | Managed Spark/Hadoop | EMR |

## 🗄️ **Databases**

### **Relational Databases**
| Database | Strengths | Use Cases |
|----------|-----------|-----------|
| **PostgreSQL** | Advanced features, JSON support | OLTP, analytics, geospatial |
| **MySQL** | Performance, simplicity | Web apps, read-heavy workloads |
| **Oracle** | Enterprise features | Large enterprises, complex transactions |

### **NoSQL Databases**
| Type | Database | Use Cases | Key Features |
|------|----------|-----------|--------------|
| **Document** | MongoDB | Content management, catalogs | Flexible schema, JSON-like |
| **Key-Value** | Redis | Caching, sessions | In-memory, pub/sub |
| **Key-Value** | DynamoDB | Serverless apps, gaming | Auto-scaling, managed |
| **Column** | Cassandra | Time-series, IoT | High availability, linear scale |

### **Specialized Databases**
| Type | Database | Use Cases |
|------|----------|-----------|
| **Time-Series** | InfluxDB | Metrics, monitoring |
| **Search** | Elasticsearch | Full-text search, logging |
| **Graph** | Neo4j | Social networks, recommendations |

## 🔧 **DevOps Tools**

### **Docker**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### **Kubernetes**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-processor
spec:
  replicas: 3
  selector:
    matchLabels:
      app: data-processor
  template:
    spec:
      containers:
      - name: processor
        image: data-processor:latest
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

---

# 🏗️ Architecture & Concepts

## 🔄 **ETL vs ELT**

| Aspect | ETL | ELT |
|--------|-----|-----|
| **Process** | Extract → Transform → Load | Extract → Load → Transform |
| **Transform Location** | Separate processing engine | Target system |
| **Data Storage** | Processed data only | Raw + processed data |
| **Flexibility** | Less flexible | More flexible |
| **Time to Insights** | Longer (pre-processing) | Faster (load first) |
| **Storage Cost** | Lower | Higher |

### **When to Use ETL**
- Structured data with stable schema
- Strict data quality requirements
- Limited storage budget
- Compliance is critical
- Traditional data warehouse

### **When to Use ELT**
- Large data volumes
- Schema changes frequently
- Need fast data availability
- Have powerful target system
- Exploratory analytics required

## 🏛️ **Architecture Patterns**

### **Lambda Architecture**
```
Batch Layer → Master Dataset → Batch Views
Speed Layer → Real-time Views
Serving Layer → Merge batch + real-time views
```

### **Kappa Architecture**
```
Stream Processing Only
All data treated as streams
Simpler than Lambda, but requires reprocessing for changes
```

### **Medallion Architecture (Bronze-Silver-Gold)**
```
Bronze Layer (Raw Data)
    ↓
Silver Layer (Cleaned & Validated)
    ↓
Gold Layer (Business-Ready)
```

## 📦 **Data Storage Formats**

| Format | Type | Schema | Compression | Analytics | Use Case |
|--------|------|--------|-------------|-----------|----------|
| **CSV** | Text | No | Poor | Poor | Simple data exchange |
| **JSON** | Text | Flexible | Poor | Poor | APIs, configuration |
| **Parquet** | Binary | Yes | Excellent | Excellent | Analytics, warehousing |
| **Avro** | Binary | Yes | Good | Good | Streaming, schema evolution |
| **ORC** | Binary | Yes | Excellent | Excellent | Hive, analytics |
| **Delta** | Binary | Yes | Excellent | Excellent | ACID transactions |

### **Format Selection Guidelines**
- **Analytics/OLAP**: Parquet or ORC
- **Streaming/Real-time**: Avro
- **APIs/Web**: JSON
- **Data Exchange**: CSV (simple) or Avro (complex)
- **Archive/Compression**: Parquet with Snappy/GZIP

## 🎯 **Data Quality Dimensions**
1. **Accuracy**: Correct values
2. **Completeness**: No missing data
3. **Consistency**: Same format across systems
4. **Timeliness**: Data available when needed
5. **Validity**: Conforms to business rules
6. **Uniqueness**: No duplicates

## 🚀 **Performance & Scalability**

### **Scalability Patterns**
- **Horizontal Scaling**: Add more machines
- **Vertical Scaling**: Increase machine resources
- **Auto-scaling**: Dynamic resource allocation

### **Key Metrics to Track**
- **Latency**: Time to process data
- **Throughput**: Volume processed per unit time
- **Error Rate**: Failed vs successful runs
- **Data Freshness**: How current is the data

---

# 💻 Essential Code Snippets

## 🐍 **Python Data Processing**
```python
# Database Connections
import psycopg2
conn = psycopg2.connect(
    host="localhost",
    database="mydb",
    user="user",
    password="password"
)
df = pd.read_sql("SELECT * FROM table", conn)

# Performance Tips
# - Use iterrows() sparingly - vectorized operations are faster
# - Use pd.read_csv(chunksize=1000) for large files
# - Use df.query() instead of boolean indexing for readability
```

## ⚡ **Spark Optimization**
```python
# Configuration Tuning
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")

# Window Functions
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, rank, lag

window = Window.partitionBy("department").orderBy("salary")
df.withColumn("rank", rank().over(window)) \
  .withColumn("prev_salary", lag("salary").over(window))

# Broadcast small tables
from pyspark.sql.functions import broadcast
large_df.join(broadcast(small_df), "key")
```

## 🗄️ **SQL Performance**
```sql
-- Performance Tips
-- - Use LIMIT when testing queries
-- - Index frequently queried columns
-- - Use EXPLAIN to analyze query plans
-- - Avoid SELECT * in production
-- - Use WHERE before GROUP BY

-- Aggregations with HAVING
SELECT department, COUNT(*), AVG(salary)
FROM employees 
GROUP BY department 
HAVING COUNT(*) > 5;
```

## ☁️ **AWS CLI Commands**
```bash
# S3 operations
aws s3 cp file.txt s3://bucket/
aws s3 sync ./folder s3://bucket/folder/

# Glue
aws glue start-job-run --job-name my-job

# Athena
aws athena start-query-execution --query-string "SELECT * FROM table"
```

## 🔧 **Docker & Kubernetes**
```bash
# Docker
docker build -t my-app .
docker run -p 8080:80 my-app
docker-compose up -d

# Kubernetes
kubectl apply -f deployment.yaml
kubectl get pods
kubectl logs pod-name
```

---

# 🎯 Final Tips

1. **Ask clarifying questions** - Shows analytical thinking
2. **Think out loud** - Demonstrate problem-solving process
3. **Start simple, then optimize** - Show iterative approach
4. **Mention trade-offs** - Shows understanding of real-world constraints
5. **Be honest about unknowns** - Better than guessing

## 📚 **Learning Priority**

### **🥇 Essential (Start Here)**
1. Python + SQL + PySpark
2. AWS (S3, Glue, Athena, Redshift)
3. Apache Spark + Databricks
4. Apache Airflow + DBT

### **🥈 Advanced**
1. Kafka + Streaming
2. Docker + Kubernetes
3. Snowflake + Data Architecture
4. Terraform + CI/CD

### **🥉 Specialized**
1. NoSQL Databases
2. ML/AI Tools
3. Monitoring + Visualization
4. Advanced Programming

---

*💡 **Pro Tip**: Focus on mastering the essential tools first, then gradually expand to advanced and specialized tools based on your career goals and project requirements.*