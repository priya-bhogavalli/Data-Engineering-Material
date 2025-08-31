# 🛠️ Comprehensive Data Engineering Tools & Services Cheat Sheet

## 🎯 **Quick Navigation**
- [Core Programming](#-core-programming)
- [Cloud Platforms](#-cloud-platforms)
- [Databases](#-databases)
- [Data Processing](#-data-processing)
- [Data Warehousing](#-data-warehousing)
- [Data Architecture](#-data-architecture)
- [DevOps & Automation](#-devops--automation)
- [Monitoring & Visualization](#-monitoring--visualization)
- [AI & Machine Learning](#-ai--machine-learning)
- [Supporting Tools](#-supporting-tools)

---

## 🐍 **Core Programming**

### **Python**
- **Purpose**: Primary data engineering language
- **Key Libraries**: pandas, numpy, requests, boto3, psycopg2
- **Use Cases**: ETL scripts, data processing, API integration
- **Quick Commands**:
  ```python
  # Data manipulation
  df = pd.read_csv('file.csv')
  df.groupby('column').agg({'value': 'sum'})
  
  # AWS integration
  import boto3
  s3 = boto3.client('s3')
  ```

### **SQL**
- **Purpose**: Data querying and manipulation
- **Key Concepts**: JOINs, CTEs, Window Functions, Indexing
- **Use Cases**: Data analysis, ETL, reporting
- **Quick Commands**:
  ```sql
  -- Window functions
  SELECT *, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) as rank
  FROM employees;
  
  -- CTEs
  WITH sales_summary AS (SELECT dept, SUM(amount) as total FROM sales GROUP BY dept)
  SELECT * FROM sales_summary WHERE total > 10000;
  ```

### **PySpark**
- **Purpose**: Big data processing with Python
- **Key Concepts**: RDDs, DataFrames, Transformations, Actions
- **Use Cases**: Large-scale ETL, distributed computing
- **Quick Commands**:
  ```python
  # DataFrame operations
  df = spark.read.parquet("path/to/file")
  df.filter(col("age") > 21).groupBy("department").count().show()
  
  # Write data
  df.write.mode("overwrite").parquet("output/path")
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
- **Purpose**: Unified analytics engine for big data
- **Components**: Spark Core, SQL, Streaming, MLlib, GraphX
- **Key Concepts**: RDDs, DataFrames, Catalyst Optimizer
- **Quick Commands**:
  ```python
  # Read data
  df = spark.read.option("header", "true").csv("data.csv")
  
  # Transformations
  result = df.filter(col("age") > 25).groupBy("department").agg(avg("salary"))
  
  # Write results
  result.write.mode("overwrite").parquet("output")
  ```

### **Databricks**
- **Purpose**: Unified analytics platform built on Spark
- **Key Features**: Collaborative notebooks, Delta Lake, MLflow
- **Architecture**: Medallion (Bronze/Silver/Gold)
- **Use Cases**: Data engineering, ML, collaborative analytics

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
- **Architecture**: Multi-cluster, shared data
- **Key Features**: Auto-scaling, time travel, zero-copy cloning
- **SQL Extensions**: VARIANT data type, streams, tasks
- **Quick Commands**:
  ```sql
  -- Create warehouse
  CREATE WAREHOUSE my_wh WITH WAREHOUSE_SIZE = 'MEDIUM';
  
  -- Time travel
  SELECT * FROM table_name AT (TIMESTAMP => '2023-01-01 00:00:00');
  
  -- Clone table
  CREATE TABLE new_table CLONE existing_table;
  ```

### **Amazon Redshift**
- **Architecture**: Columnar storage, MPP
- **Key Features**: Spectrum (query S3), Concurrency Scaling
- **Optimization**: Distribution keys, sort keys, compression
- **Quick Commands**:
  ```sql
  -- Create table with distribution
  CREATE TABLE sales (id INT, amount DECIMAL) DISTKEY(id) SORTKEY(date);
  
  -- COPY from S3
  COPY table_name FROM 's3://bucket/path' IAM_ROLE 'role_arn';
  ```

---

## 🏗️ **Data Architecture**

### **Design Patterns**
| Pattern | Purpose | Key Concepts |
|---------|---------|--------------|
| **Data Vault 2.0** | Scalable data warehouse | Hubs, Links, Satellites |
| **Data Mesh** | Decentralized data architecture | Domain ownership, data products |
| **Dimensional Modeling** | Analytics-focused design | Facts, dimensions, star schema |
| **DataOps** | Agile data management | CI/CD for data, monitoring |

### **Storage Formats**
| Format | Use Case | Advantages |
|--------|----------|------------|
| **Parquet** | Analytics | Columnar, compression, schema evolution |
| **Avro** | Streaming | Schema evolution, compact binary |
| **Delta Lake** | Data lakes | ACID transactions, time travel |
| **Iceberg** | Data lakes | Schema evolution, partition evolution |

---

## 🔧 **DevOps & Automation**

### **Containerization**
| Tool | Purpose | Key Commands |
|------|---------|--------------|
| **Docker** | Containerization | `docker build`, `docker run`, `docker-compose` |
| **Kubernetes** | Container orchestration | `kubectl apply`, `kubectl get pods` |

### **Infrastructure as Code**
| Tool | Purpose | Key Features |
|------|---------|---------------|
| **Terraform** | Infrastructure provisioning | HCL syntax, state management |
| **Ansible** | Configuration management | Playbooks, idempotent |

### **CI/CD**
| Tool | Purpose | Key Features |
|------|---------|---------------|
| **Jenkins** | Build automation | Pipelines, plugins |
| **CircleCI** | Cloud CI/CD | Docker support, parallelism |

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

## 🤖 **AI & Machine Learning**

### **ML Platforms**
| Platform | Purpose | Key Features |
|----------|---------|---------------|
| **MLflow** | ML lifecycle management | Tracking, models, deployment |
| **Kubeflow** | ML on Kubernetes | Pipelines, notebooks |

### **GenAI & LLMs**
| Technology | Purpose | Key Concepts |
|------------|---------|---------------|
| **LangChain** | LLM applications | Chains, agents, memory |
| **Vector Databases** | Similarity search | Embeddings, RAG |
| **OpenAI APIs** | AI services | GPT models, embeddings |

---

## 🛠️ **Supporting Tools**

### **Version Control**
| Tool | Purpose | Key Commands |
|------|---------|--------------|
| **Git** | Source control | `git add`, `git commit`, `git push` |
| **GitLab** | DevOps platform | CI/CD, issue tracking |
| **Bitbucket** | Atlassian Git | Jira integration |

### **Project Management**
| Tool | Purpose | Key Features |
|------|---------|---------------|
| **Jira** | Issue tracking | Agile boards, workflows |
| **Confluence** | Documentation | Wiki, collaboration |
| **ServiceNow** | IT service management | Ticketing, workflows |

### **Programming Languages**
| Language | Use Cases | Key Features |
|----------|-----------|---------------|
| **JavaScript** | Web development | Node.js, React |
| **C/C++** | System programming | Performance, memory control |
| **C#** | .NET applications | Enterprise, Windows |
| **MATLAB** | Scientific computing | Matrix operations, toolboxes |

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