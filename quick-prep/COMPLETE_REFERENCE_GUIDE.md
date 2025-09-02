# 🛠️ Complete Data Engineering Reference Guide

## 🎯 **Quick Navigation**
- [Core Programming](#-core-programming)
- [Cloud Platforms](#-cloud-platforms)
- [Databases](#-databases)
- [Data Processing](#-data-processing)
- [Data Warehousing](#-data-warehousing)
- [DevOps & Automation](#-devops--automation)
- [Monitoring & Visualization](#-monitoring--visualization)
- [Quick Commands](#-quick-reference-commands)

---

## 🐍 **Core Programming**

### **Python Essentials**
```python
# Data Structures
data = [1, 2, 3]                    # Lists - ordered, mutable
config = {'host': 'localhost'}      # Dicts - key-value pairs
unique_ids = {1, 2, 3}              # Sets - unique values

# List comprehensions
squares = [x**2 for x in range(10) if x % 2 == 0]

# File Operations
import pandas as pd
df = pd.read_csv('data.csv')
df.head()                           # First 5 rows
df.info()                           # Data types & null counts
df.describe()                       # Summary statistics
df.groupby('column').sum()          # Group and aggregate
df.merge(df2, on='key')             # Join dataframes
df.drop_duplicates()                # Remove duplicates

# Database Connections
import psycopg2
conn = psycopg2.connect(
    host="localhost",
    database="mydb",
    user="user",
    password="password"
)
df = pd.read_sql("SELECT * FROM table", conn)

# Error Handling
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    result = default_value

# Performance Tips
# - Use iterrows() sparingly - vectorized operations are faster
# - Use pd.read_csv(chunksize=1000) for large files
# - Use df.query() instead of boolean indexing for readability
```

### **SQL Essentials**
```sql
-- Basic Queries
SELECT column1, column2 
FROM table_name 
WHERE condition 
ORDER BY column1 DESC;

-- Aggregations
SELECT department, COUNT(*), AVG(salary)
FROM employees 
GROUP BY department 
HAVING COUNT(*) > 5;

-- JOINs
-- Inner Join
SELECT a.*, b.name
FROM orders a
INNER JOIN customers b ON a.customer_id = b.id;

-- Left Join (keep all from left table)
SELECT a.*, b.name
FROM orders a
LEFT JOIN customers b ON a.customer_id = b.id;

-- Window Functions
-- Running total
SELECT date, amount,
       SUM(amount) OVER (ORDER BY date) as running_total
FROM transactions;

-- Rank within groups
SELECT name, department, salary,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC) as rank
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

-- Performance Tips
-- - Use LIMIT when testing queries
-- - Index frequently queried columns
-- - Use EXPLAIN to analyze query plans
-- - Avoid SELECT * in production
-- - Use WHERE before GROUP BY
```

### **PySpark Essentials**
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count, avg

# Initialize Spark
spark = SparkSession.builder.appName("DataEngineering").getOrCreate()

# Read data
df = spark.read.csv("path/to/file.csv", header=True, inferSchema=True)
df = spark.read.parquet("path/to/file.parquet")
df = spark.read.json("path/to/file.json")

# Basic operations
df.show(10)                         # Display first 10 rows
df.printSchema()                    # Show schema
df.count()                          # Count rows
df.select("col1", "col2")           # Select columns
df.filter(col("age") > 25)          # Filter rows
df.groupBy("department").agg(avg("salary"))  # Group and aggregate

# Transformations vs Actions
# Transformations (lazy evaluation)
df.select()
df.filter()
df.groupBy()
df.join()
df.withColumn()

# Actions (trigger execution)
df.show()
df.collect()
df.count()
df.write.parquet()

# Joins
df1.join(df2, "common_column")                    # Inner join (default)
df1.join(df2, df1.id == df2.user_id)
df1.join(df2, "key", "left")                      # Left outer
df1.join(df2, "key", "right")                     # Right outer
df1.join(df2, "key", "outer")                     # Full outer

# Window Functions
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, rank, lag

window = Window.partitionBy("department").orderBy("salary")
df.withColumn("rank", rank().over(window)) \
  .withColumn("prev_salary", lag("salary").over(window))

# Performance Optimization
df.cache()                          # Cache for reused DataFrames
df.repartition(200)                 # Increase partitions
df.coalesce(10)                     # Decrease partitions (no shuffle)

# Configuration Tuning
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")

# Common Pitfalls
# - Small files problem: Use coalesce() before writing
# - Data skew: Use salting or custom partitioning
# - Memory issues: Increase driver/executor memory
# - Collect() on large data: Use show() or write() instead
```

---

## ☁️ **Cloud Platforms**

### **AWS Services**
| Service | Purpose | Key Use Cases |
|---------|---------|---------------|
| **S3** | Object storage | Data lake, backup, static hosting |
| **EC2** | Virtual servers | Compute instances, applications |
| **Glue** | ETL service | Data cataloging, serverless ETL |
| **Athena** | Query service | SQL queries on S3 data |
| **Redshift** | Data warehouse | Analytics, OLAP queries |
| **RDS** | Managed databases | PostgreSQL, MySQL, Oracle |
| **Lambda** | Serverless compute | Event-driven processing |
| **Kinesis** | Streaming data | Real-time data ingestion |
| **EMR** | Big data platform | Spark, Hadoop clusters |
| **IAM** | Identity management | Access control, permissions |

### **Azure Services**
| Service | Purpose | AWS Equivalent |
|---------|---------|----------------|
| **Blob Storage** | Object storage | S3 |
| **Data Factory** | ETL/ELT | Glue |
| **Synapse Analytics** | Data warehouse | Redshift |
| **Databricks** | Analytics platform | EMR |
| **Event Hubs** | Streaming | Kinesis |
| **SQL Database** | Managed SQL | RDS |

### **GCP Services**
| Service | Purpose | AWS Equivalent |
|---------|---------|----------------|
| **Cloud Storage** | Object storage | S3 |
| **BigQuery** | Data warehouse | Redshift |
| **Dataflow** | Stream/batch processing | Kinesis Analytics |
| **Dataproc** | Managed Spark/Hadoop | EMR |
| **Cloud SQL** | Managed databases | RDS |
| **Pub/Sub** | Messaging | SNS/SQS |

---

## 🗄️ **Databases**

### **Relational Databases (RDBMS)**
| Database | Strengths | Use Cases |
|----------|-----------|-----------| 
| **PostgreSQL** | Advanced features, JSON support | OLTP, analytics, geospatial |
| **MySQL** | Performance, simplicity | Web apps, read-heavy workloads |
| **Oracle** | Enterprise features | Large enterprises, complex transactions |
| **SQL Server** | Microsoft ecosystem | .NET applications, BI |

### **NoSQL Databases**
| Type | Database | Use Cases | Key Features |
|------|----------|-----------|--------------| 
| **Document** | MongoDB | Content management, catalogs | Flexible schema, JSON-like |
| **Document** | CouchDB | Mobile sync, offline-first | Multi-master replication |
| **Key-Value** | Redis | Caching, sessions | In-memory, pub/sub |
| **Key-Value** | DynamoDB | Serverless apps, gaming | Auto-scaling, managed |
| **Column** | Cassandra | Time-series, IoT | High availability, linear scale |
| **Column** | HBase | Real-time analytics | Hadoop ecosystem |

### **Specialized Databases**
| Type | Database | Use Cases |
|------|----------|-----------| 
| **Time-Series** | InfluxDB | Metrics, monitoring |
| **Time-Series** | TimescaleDB | PostgreSQL + time-series |
| **Search** | Elasticsearch | Full-text search, logging |
| **Search** | Solr | Enterprise search |
| **Graph** | Neo4j | Social networks, recommendations |
| **Graph** | Neptune | AWS managed graph database |

---

## ⚡ **Data Processing**

### **Apache Spark**
```python
# Core Architecture
# Spark Application
# ├── Driver Program (SparkContext)
# ├── Cluster Manager (YARN/Mesos/Standalone)
# └── Executors (Worker nodes)

# Read data with schema
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
    StructField("customer_id", StringType(), True),
    StructField("order_amount", IntegerType(), True)
])

df = spark.read.schema(schema).parquet("s3://bucket/orders/")

# Cache frequently used DataFrame
df.cache()

# Use column functions instead of UDFs
from pyspark.sql.functions import when, col

result = df.withColumn(
    "amount_category",
    when(col("order_amount") > 1000, "high")
    .when(col("order_amount") > 100, "medium")
    .otherwise("low")
)

# Write with partitioning
result.write.partitionBy("amount_category").parquet("s3://bucket/processed/")

# Broadcast small tables
from pyspark.sql.functions import broadcast
large_df.join(broadcast(small_df), "key")
```

### **Streaming Platforms**
| Platform | Strengths | Use Cases |
|----------|-----------|-----------| 
| **Apache Kafka** | High throughput, durability | Event streaming, log aggregation |
| **Apache Flink** | Low latency, stateful processing | Real-time analytics, CEP |
| **Confluent Kafka** | Enterprise Kafka + tools | Managed Kafka, Schema Registry |

### **ETL Tools**
| Tool | Type | Strengths |
|------|------|-----------| 
| **Informatica** | Enterprise ETL | Data quality, governance |
| **SnapLogic** | iPaaS | API integration, cloud-native |

### **Orchestration**
| Tool | Purpose | Key Features |
|------|---------|---------------| 
| **Apache Airflow** | Workflow orchestration | DAGs, scheduling, monitoring |
| **DBT** | Data transformation | SQL-based, version control, testing |

---

## 🏢 **Data Warehousing**

### **Snowflake**
```sql
-- Architecture: Multi-cluster, shared data
-- Key Features: Auto-scaling, time travel, zero-copy cloning

-- Create warehouse
CREATE WAREHOUSE my_wh WITH WAREHOUSE_SIZE = 'MEDIUM';

-- Time travel
SELECT * FROM table_name AT (TIMESTAMP => '2023-01-01 00:00:00');

-- Clone table
CREATE TABLE new_table CLONE existing_table;

-- Warehouse management
USE WAREHOUSE etl_warehouse;
ALTER WAREHOUSE etl_warehouse SET WAREHOUSE_SIZE = 'X-LARGE';
ALTER WAREHOUSE etl_warehouse SUSPEND;
ALTER WAREHOUSE etl_warehouse RESUME;
```

### **Amazon Redshift**
```sql
-- Architecture: Columnar storage, MPP
-- Key Features: Spectrum (query S3), Concurrency Scaling

-- Create table with distribution
CREATE TABLE sales (
    id INT, 
    amount DECIMAL
) DISTKEY(id) SORTKEY(date);

-- COPY from S3
COPY table_name FROM 's3://bucket/path' 
IAM_ROLE 'role_arn';
```

---

## 🔧 **DevOps & Automation**

### **Docker**
```dockerfile
# Multi-stage builds to reduce image size
FROM python:3.9-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.9-slim
RUN groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY . .
USER appuser
CMD ["python", "app.py"]
```

### **Kubernetes**
```yaml
# Set resource limits and requests
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
    metadata:
      labels:
        app: data-processor
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
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
```

### **Terraform**
```hcl
# AWS S3 bucket for data lake
resource "aws_s3_bucket" "data_lake" {
  bucket = "company-data-lake-${var.environment}"
  
  versioning {
    enabled = true
  }
  
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

# IAM role for data processing
resource "aws_iam_role" "data_processor" {
  name = "data-processor-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}
```

---

## 📊 **Monitoring & Visualization**

### **Monitoring**
| Tool | Purpose | Key Features |
|------|---------|---------------| 
| **Datadog** | Infrastructure monitoring | Metrics, logs, traces |
| **Grafana** | Visualization | Dashboards, alerting |

### **Visualization**
| Tool | Strengths | Use Cases |
|------|-----------|-----------| 
| **Tableau** | Advanced analytics | Executive dashboards, self-service BI |
| **Power BI** | Microsoft integration | Office 365, cost-effective |
| **Kibana** | Log analysis | Elasticsearch integration |

---

## 🚀 **Quick Reference Commands**

### **AWS CLI**
```bash
# S3 operations
aws s3 cp file.txt s3://bucket/
aws s3 sync ./folder s3://bucket/folder/

# Glue
aws glue start-job-run --job-name my-job

# Athena
aws athena start-query-execution --query-string "SELECT * FROM table"
```

### **Docker**
```bash
# Build and run
docker build -t my-app .
docker run -p 8080:80 my-app

# Compose
docker-compose up -d
docker-compose logs -f
```

### **Kubernetes**
```bash
# Deploy
kubectl apply -f deployment.yaml
kubectl get pods
kubectl logs pod-name
```

### **Terraform**
```bash
# Infrastructure
terraform init
terraform plan
terraform apply
terraform destroy
```

### **Git**
```bash
# Basic workflow
git add .
git commit -m "Add new feature"
git push origin main

# Branching
git checkout -b feature-branch
git merge feature-branch
git branch -d feature-branch
```

---

## 📊 **Data Storage Formats Comparison**

| Format | Type | Schema | Compression | Analytics | Human Readable | Use Case |
|--------|------|--------|-------------|-----------|----------------|----------|
| **CSV** | Text | No | Poor | Poor | Yes | Simple data exchange |
| **JSON** | Text | Flexible | Poor | Poor | Yes | APIs, configuration |
| **Parquet** | Binary | Yes | Excellent | Excellent | No | Analytics, warehousing |
| **Avro** | Binary | Yes | Good | Good | No | Streaming, schema evolution |
| **ORC** | Binary | Yes | Excellent | Excellent | No | Hive, analytics |
| **Delta** | Binary | Yes | Excellent | Excellent | No | ACID transactions |

### **Format Selection Guidelines**
- **Analytics/OLAP**: Parquet or ORC
- **Streaming/Real-time**: Avro
- **APIs/Web**: JSON
- **Data Exchange**: CSV (simple) or Avro (complex)
- **Archive/Compression**: Parquet with Snappy/GZIP

---

## 🔄 **ETL vs ELT Quick Comparison**

| Aspect | ETL | ELT |
|--------|-----|-----|
| **Process** | Extract → Transform → Load | Extract → Load → Transform |
| **Transform Location** | Separate processing engine | Target system |
| **Data Storage** | Processed data only | Raw + processed data |
| **Flexibility** | Less flexible | More flexible |
| **Time to Insights** | Longer (pre-processing) | Faster (load first) |
| **Storage Cost** | Lower | Higher |
| **Processing Power** | External tools | Target system |

### **When to Use**
- **ETL**: Structured data, compliance requirements, limited storage, batch processing
- **ELT**: Big data, cloud environments, real-time analytics, exploratory analysis

---

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