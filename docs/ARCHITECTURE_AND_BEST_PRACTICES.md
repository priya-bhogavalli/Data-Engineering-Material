# 🏗️ Data Engineering Architecture & Best Practices Guide

## 📋 Table of Contents

1. [Solution Architecture Patterns](#-solution-architecture-patterns)
2. [Code Best Practices](#-code-best-practices)
3. [Performance Optimization](#-performance-optimization)
4. [Security & Compliance](#-security--compliance)
5. [Implementation Guidelines](#-implementation-guidelines)

---

## 🏛️ Solution Architecture Patterns

### **1. Modern Data Lake Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA SOURCES                              │
├─────────────────────────────────────────────────────────────────┤
│ Databases │ APIs │ Files │ Streams │ SaaS Apps │ IoT Devices    │
└─────────────┬───────────────────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────────────────┐
│                     INGESTION LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│ Batch: Airbyte, Fivetran, Custom ETL                           │
│ Stream: Kafka, Kinesis, Pub/Sub                                │
│ API: REST/GraphQL connectors                                    │
└─────────────┬───────────────────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────────────────┐
│                      STORAGE LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│ Raw Zone:       S3/ADLS/GCS (JSON, CSV, Avro)                 │
│ Processed Zone: S3/ADLS/GCS (Parquet, Delta, Iceberg)         │
│ Curated Zone:   S3/ADLS/GCS (Optimized for Analytics)         │
└─────────────┬───────────────────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────────────────┐
│                    PROCESSING LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│ Batch: Spark, Databricks, EMR, Dataflow                       │
│ Stream: Flink, Kafka Streams, Spark Streaming                 │
│ Orchestration: Airflow, Prefect, Step Functions               │
└─────────────┬───────────────────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────────────────┐
│                     SERVING LAYER                               │
├─────────────────────────────────────────────────────────────────┤
│ Data Warehouse: Snowflake, Redshift, BigQuery, Synapse        │
│ OLAP: ClickHouse, Druid, Pinot                                │
│ Search: Elasticsearch, Solr                                    │
│ Cache: Redis, Memcached                                        │
└─────────────┬───────────────────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────────────────┐
│                   CONSUMPTION LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│ BI Tools: Tableau, Power BI, Looker                           │
│ ML Platforms: SageMaker, Vertex AI, Azure ML                  │
│ APIs: REST/GraphQL endpoints                                   │
│ Applications: Custom dashboards, reports                       │
└─────────────────────────────────────────────────────────────────┘
```

### **2. Lambda Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA SOURCES                              │
└─────────────┬───────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MESSAGE QUEUE                                │
│              Kafka / Kinesis / Pub/Sub                         │
└─────────────┬───────────────────┬───────────────────────────────┘
              │                   │
              ▼                   ▼
┌─────────────────────┐ ┌─────────────────────┐
│    BATCH LAYER      │ │   SPEED LAYER       │
│                     │ │                     │
│ • Hadoop/Spark      │ │ • Storm/Flink       │
│ • Immutable data    │ │ • Low latency       │
│ • High accuracy     │ │ • Approximate       │
│ • High latency      │ │ • Real-time views   │
└─────────────┬───────┘ └─────────┬───────────┘
              │                   │
              ▼                   ▼
┌─────────────────────┐ ┌─────────────────────┐
│   BATCH VIEWS       │ │  REAL-TIME VIEWS    │
│                     │ │                     │
│ • Pre-computed      │ │ • Incremental       │
│ • Complete data     │ │ • Fast updates      │
└─────────────┬───────┘ └─────────┬───────────┘
              │                   │
              └─────────┬─────────┘
                        ▼
              ┌─────────────────────┐
              │   SERVING LAYER     │
              │                     │
              │ • Query merging     │
              │ • Unified interface │
              └─────────────────────┘
```

### **3. Medallion Architecture (Bronze-Silver-Gold)**

```
┌─────────────────────────────────────────────────────────────────┐
│                      BRONZE LAYER                               │
├─────────────────────────────────────────────────────────────────┤
│ • Raw data ingestion                                            │
│ • Minimal processing                                            │
│ • Schema-on-read                                                │
│ • Data lineage tracking                                         │
│                                                                 │
│ Format: JSON, CSV, Avro, Parquet                               │
│ Storage: S3, ADLS, GCS                                         │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SILVER LAYER                               │
├─────────────────────────────────────────────────────────────────┤
│ • Cleaned and validated data                                    │
│ • Standardized formats                                          │
│ • Deduplication                                                 │
│ • Basic transformations                                         │
│                                                                 │
│ Format: Delta Lake, Iceberg, Hudi                              │
│ Features: ACID transactions, time travel                       │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                       GOLD LAYER                                │
├─────────────────────────────────────────────────────────────────┤
│ • Business-ready datasets                                       │
│ • Aggregated metrics                                            │
│ • Feature engineering                                           │
│ • Optimized for consumption                                     │
│                                                                 │
│ Consumers: BI tools, ML models, APIs                           │
│ SLA: High availability, low latency                            │
└─────────────────────────────────────────────────────────────────┘
```

### **4. Event-Driven Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                        EVENT SOURCES                            │
├─────────────────────────────────────────────────────────────────┤
│ User Actions │ System Events │ External APIs │ Sensors         │
└─────────────┬───────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       EVENT BUS                                 │
├─────────────────────────────────────────────────────────────────┤
│                    Kafka / EventBridge                         │
│                                                                 │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐               │
│ │user.created │ │order.placed │ │payment.done │               │
│ └─────────────┘ └─────────────┘ └─────────────┘               │
└─────────────┬───────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EVENT PROCESSORS                             │
├─────────────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐               │
│ │Analytics    │ │Notifications│ │Data         │               │
│ │Service      │ │Service      │ │Warehouse    │               │
│ └─────────────┘ └─────────────┘ └─────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

### **5. Cloud-Native Architecture (AWS)**

```yaml
# Infrastructure as Code (Terraform)
architecture:
  ingestion:
    - service: AWS Kinesis Data Streams
      purpose: Real-time data ingestion
      scaling: Auto-scaling based on throughput
    
    - service: AWS Glue
      purpose: Batch ETL processing
      scheduling: EventBridge triggers
  
  storage:
    - service: Amazon S3
      structure:
        - raw/: Landing zone for all data
        - processed/: Cleaned and validated data
        - curated/: Business-ready datasets
      lifecycle: Intelligent tiering
    
    - service: AWS Lake Formation
      purpose: Data lake governance and security
  
  processing:
    - service: Amazon EMR
      purpose: Big data processing with Spark
      scaling: Spot instances for cost optimization
    
    - service: AWS Lambda
      purpose: Serverless data processing
      triggers: S3 events, Kinesis records
  
  serving:
    - service: Amazon Redshift
      purpose: Data warehousing
      scaling: Concurrency scaling
    
    - service: Amazon Athena
      purpose: Serverless analytics
      optimization: Partition projection
  
  orchestration:
    - service: AWS Step Functions
      purpose: Workflow orchestration
      integration: Native AWS service integration
  
  monitoring:
    - service: Amazon CloudWatch
      metrics: Custom application metrics
      alarms: Automated incident response
```

---

## 💻 Code Best Practices

### **Python Best Practices**

#### ✅ **DO's**
- **Use type hints** for function parameters and return values
- **Follow PEP 8** style guidelines consistently
- **Use virtual environments** for dependency isolation
- **Write docstrings** for all functions and classes
- **Handle exceptions explicitly** with specific exception types
- **Use logging** instead of print statements
- **Validate input data** before processing

```python
# ✅ GOOD
from typing import List, Dict, Optional
import logging

def process_data(records: List[Dict], batch_size: int = 1000) -> Optional[List[Dict]]:
    """
    Process data records in batches.
    
    Args:
        records: List of data records to process
        batch_size: Number of records per batch
        
    Returns:
        Processed records or None if error
    """
    try:
        processed = []
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            processed.extend([transform_record(r) for r in batch])
        return processed
    except ValueError as e:
        logging.error(f"Data processing failed: {e}")
        return None
```

#### ❌ **DON'Ts**
- **Don't use global variables** for data processing
- **Don't ignore exceptions** with bare except clauses
- **Don't use mutable default arguments**
- **Don't hardcode credentials** in source code

### **SQL Best Practices**

#### ✅ **DO's**
- **Use consistent naming conventions** (snake_case)
- **Write readable queries** with proper indentation
- **Use explicit JOIN syntax** instead of implicit joins
- **Add comments** for complex business logic
- **Use CTEs** for complex queries instead of subqueries
- **Index frequently queried columns**

```sql
-- ✅ GOOD
WITH monthly_sales AS (
    SELECT 
        customer_id,
        DATE_TRUNC('month', order_date) AS month,
        SUM(total_amount) AS monthly_total
    FROM orders 
    WHERE order_date >= '2024-01-01'
    GROUP BY customer_id, DATE_TRUNC('month', order_date)
),
customer_metrics AS (
    SELECT 
        customer_id,
        AVG(monthly_total) AS avg_monthly_spend,
        COUNT(*) AS active_months
    FROM monthly_sales
    GROUP BY customer_id
)
SELECT 
    c.customer_name,
    cm.avg_monthly_spend,
    cm.active_months
FROM customer_metrics cm
INNER JOIN customers c ON cm.customer_id = c.customer_id
WHERE cm.avg_monthly_spend > 1000
ORDER BY cm.avg_monthly_spend DESC;
```

#### ❌ **DON'Ts**
- **Don't use SELECT \*** in production queries
- **Don't use implicit joins** (comma-separated tables)
- **Don't ignore NULL handling**
- **Don't use functions in WHERE clauses** on indexed columns

### **PySpark Best Practices**

#### ✅ **DO's**
- **Use DataFrame API** over RDD when possible
- **Cache/persist** frequently accessed DataFrames
- **Use broadcast variables** for small lookup tables
- **Partition data** appropriately for your use case
- **Use column functions** instead of UDFs when possible

```python
# ✅ GOOD
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Define schema explicitly
schema = StructType([
    StructField("customer_id", StringType(), True),
    StructField("order_amount", IntegerType(), True)
])

# Read with schema
df = spark.read.schema(schema).parquet("s3://bucket/orders/")

# Cache frequently used DataFrame
df.cache()

# Use column functions instead of UDFs
result = df.withColumn(
    "amount_category",
    F.when(F.col("order_amount") > 1000, "high")
     .when(F.col("order_amount") > 100, "medium")
     .otherwise("low")
)

# Write with partitioning
result.write.partitionBy("amount_category").parquet("s3://bucket/processed/")
```

#### ❌ **DON'Ts**
- **Don't use collect()** on large DataFrames
- **Don't create too many small partitions**
- **Don't use Python UDFs** unnecessarily
- **Don't ignore data skew**

### **Data Pipeline Best Practices**

#### ✅ **DO's**
- **Implement idempotent operations**
- **Use checkpointing** for long-running processes
- **Implement proper error handling and retries**
- **Monitor pipeline health** with alerts
- **Use configuration files** for environment-specific settings
- **Implement data quality checks**

```python
# ✅ GOOD - Idempotent pipeline with checkpointing
import json
from pathlib import Path

class DataPipeline:
    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = json.load(f)
        self.checkpoint_path = Path(self.config['checkpoint_path'])
    
    def get_last_processed_timestamp(self) -> str:
        """Get last successfully processed timestamp."""
        if self.checkpoint_path.exists():
            return self.checkpoint_path.read_text().strip()
        return self.config['default_start_time']
    
    def update_checkpoint(self, timestamp: str):
        """Update checkpoint after successful processing."""
        self.checkpoint_path.write_text(timestamp)
    
    def process_incremental_data(self):
        """Process only new data since last checkpoint."""
        last_processed = self.get_last_processed_timestamp()
        
        try:
            # Process data newer than last_processed
            new_data = self.extract_data(since=last_processed)
            processed_data = self.transform_data(new_data)
            self.load_data(processed_data)
            
            # Update checkpoint only after successful processing
            self.update_checkpoint(self.get_current_timestamp())
            
        except Exception as e:
            logging.error(f"Pipeline failed: {e}")
            raise
```

#### ❌ **DON'Ts**
- **Don't process all data** every time
- **Don't ignore failed records** without logging
- **Don't skip data validation**
- **Don't hardcode file paths**
- **Don't run pipelines without monitoring**

---

## 📈 Performance Optimization

### **Database Optimization**

#### **Indexing Strategy**
```sql
-- Create appropriate indexes
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
CREATE INDEX idx_products_category ON products(category) WHERE active = true;

-- Monitor index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

#### **Query Optimization**
```sql
-- Use EXPLAIN to analyze query plans
EXPLAIN (ANALYZE, BUFFERS) 
SELECT c.name, SUM(o.total_amount)
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE o.order_date >= '2024-01-01'
GROUP BY c.name;

-- Optimize with proper WHERE clause placement
SELECT *
FROM large_table lt
JOIN small_table st ON lt.id = st.id
WHERE lt.status = 'active'  -- Filter early
  AND st.category = 'premium';
```

### **Big Data Optimization**

#### **Spark Optimization**
```python
# Configure Spark for optimal performance
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")

# Optimize data skew with salting
from pyspark.sql.functions import rand, floor

# Add salt to skewed keys
df_salted = df.withColumn("salted_key", 
                         concat(col("skewed_key"), 
                               lit("_"), 
                               floor(rand() * 10).cast("string")))

# Process with salted key
result = df_salted.groupBy("salted_key").agg(sum("value"))

# Remove salt from final result
final_result = result.withColumn("original_key", 
                                split(col("salted_key"), "_")[0])
```

#### **Memory Management**
```python
# Memory-efficient processing
def process_large_file(file_path: str, chunk_size: int = 10000):
    """Process large file in chunks to manage memory."""
    with open(file_path, 'r') as file:
        while True:
            chunk = file.readlines(chunk_size)
            if not chunk:
                break
            
            # Process chunk
            processed_chunk = [process_line(line) for line in chunk]
            yield processed_chunk
```

### **Caching Strategies**

#### **Application-Level Caching**
```python
import redis
from functools import wraps

# Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(expiration=3600):
    """Decorator to cache function results."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            redis_client.setex(cache_key, expiration, json.dumps(result))
            return result
        return wrapper
    return decorator

@cache_result(expiration=1800)
def expensive_computation(data):
    """Expensive computation that benefits from caching."""
    # Complex processing logic
    return processed_result
```

---

## 🔒 Security & Compliance

### **Data Encryption**

#### **Encryption at Rest**
```python
from cryptography.fernet import Fernet
import base64

class DataEncryption:
    def __init__(self, key: bytes = None):
        if key is None:
            key = Fernet.generate_key()
        self.cipher_suite = Fernet(key)
        self.key = key
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data."""
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        return base64.b64encode(encrypted_data).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data."""
        encrypted_bytes = base64.b64decode(encrypted_data.encode())
        decrypted_data = self.cipher_suite.decrypt(encrypted_bytes)
        return decrypted_data.decode()

# Usage
encryptor = DataEncryption()
encrypted_pii = encryptor.encrypt_data("sensitive_user_data")
```

#### **Encryption in Transit**
```python
import ssl
import requests

# Configure SSL/TLS for secure connections
session = requests.Session()
session.verify = True  # Verify SSL certificates
session.headers.update({
    'User-Agent': 'DataPipeline/1.0',
    'Content-Type': 'application/json'
})

# Use TLS 1.2 minimum
context = ssl.create_default_context()
context.minimum_version = ssl.TLSVersion.TLSv1_2
```

### **Access Control**

#### **Role-Based Access Control (RBAC)**
```sql
-- Create roles with specific permissions
CREATE ROLE data_analyst;
CREATE ROLE data_engineer;
CREATE ROLE data_scientist;

-- Grant appropriate permissions
GRANT SELECT ON analytics_schema.* TO data_analyst;
GRANT SELECT, INSERT, UPDATE ON etl_schema.* TO data_engineer;
GRANT SELECT ON ml_schema.* TO data_scientist;

-- Create users and assign roles
CREATE USER 'john.doe'@'%' IDENTIFIED BY 'secure_password';
GRANT data_analyst TO 'john.doe'@'%';
```

#### **Data Masking**
```python
import hashlib
import re

class DataMasking:
    @staticmethod
    def mask_email(email: str) -> str:
        """Mask email addresses."""
        if '@' not in email:
            return email
        
        local, domain = email.split('@', 1)
        masked_local = local[0] + '*' * (len(local) - 2) + local[-1] if len(local) > 2 else '*' * len(local)
        return f"{masked_local}@{domain}"
    
    @staticmethod
    def mask_phone(phone: str) -> str:
        """Mask phone numbers."""
        digits_only = re.sub(r'\D', '', phone)
        if len(digits_only) >= 10:
            return f"***-***-{digits_only[-4:]}"
        return '*' * len(phone)
    
    @staticmethod
    def hash_pii(data: str, salt: str = "default_salt") -> str:
        """Hash PII data for anonymization."""
        return hashlib.sha256((data + salt).encode()).hexdigest()
```

### **Compliance Framework**

#### **GDPR Compliance**
```python
class GDPRCompliance:
    def __init__(self, data_store):
        self.data_store = data_store
    
    def right_to_be_forgotten(self, user_id: str):
        """Implement right to be forgotten."""
        try:
            # Remove from all systems
            self.data_store.delete_user_data(user_id)
            self.audit_log.log_deletion(user_id, "GDPR_REQUEST")
            return True
        except Exception as e:
            logging.error(f"GDPR deletion failed for {user_id}: {e}")
            return False
    
    def data_portability(self, user_id: str) -> dict:
        """Export user data for portability."""
        user_data = self.data_store.get_user_data(user_id)
        return {
            'user_id': user_id,
            'data': user_data,
            'export_date': datetime.utcnow().isoformat(),
            'format': 'JSON'
        }
```

---

## 🛠️ Implementation Guidelines

### **Infrastructure as Code**

#### **Terraform Example**
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
  
  lifecycle_configuration {
    rule {
      id     = "transition_to_ia"
      status = "Enabled"
      
      transition {
        days          = 30
        storage_class = "STANDARD_IA"
      }
      
      transition {
        days          = 90
        storage_class = "GLACIER"
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

### **Monitoring & Observability**

#### **Structured Logging**
```python
import logging
import json
from datetime import datetime

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log(self, level: str, message: str, **kwargs):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': level,
            'message': message,
            **kwargs
        }
        self.logger.info(json.dumps(log_entry))

# Usage
logger = StructuredLogger('data_pipeline')
logger.log('INFO', 'Processing batch', batch_id='batch_123', record_count=1000)
```

#### **Metrics Collection**
```python
import time
from functools import wraps

class MetricsCollector:
    def __init__(self):
        self.metrics = {}
    
    def timing(self, metric_name: str):
        """Decorator to measure execution time."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    self.record_metric(f"{metric_name}.success", 1)
                    return result
                except Exception as e:
                    self.record_metric(f"{metric_name}.error", 1)
                    raise
                finally:
                    execution_time = time.time() - start_time
                    self.record_metric(f"{metric_name}.duration", execution_time)
            return wrapper
        return decorator
    
    def record_metric(self, name: str, value: float):
        """Record a metric value."""
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append({
            'value': value,
            'timestamp': time.time()
        })

# Usage
metrics = MetricsCollector()

@metrics.timing('data_processing')
def process_data(data):
    # Processing logic
    return processed_data
```

### **Testing Strategy**

#### **Unit Testing**
```python
import pytest
from unittest.mock import Mock, patch
from your_module import DataProcessor

class TestDataProcessor:
    def setup_method(self):
        self.processor = DataProcessor()
    
    def test_process_valid_data(self):
        # Arrange
        input_data = [{'id': 1, 'value': 100}]
        expected = [{'id': 1, 'value': 100, 'processed': True}]
        
        # Act
        result = self.processor.process(input_data)
        
        # Assert
        assert result == expected
    
    @patch('your_module.external_api_call')
    def test_process_with_external_dependency(self, mock_api):
        # Arrange
        mock_api.return_value = {'status': 'success'}
        
        # Act & Assert
        result = self.processor.process_with_api([])
        assert result is not None
```

#### **Integration Testing**
```python
import pytest
from testcontainers import DockerContainer

class TestDataPipelineIntegration:
    @pytest.fixture(scope="class")
    def postgres_container(self):
        with DockerContainer("postgres:13") \
            .with_env("POSTGRES_PASSWORD", "test") \
            .with_env("POSTGRES_DB", "testdb") \
            .with_exposed_ports(5432) as container:
            yield container
    
    def test_end_to_end_pipeline(self, postgres_container):
        # Setup test database connection
        connection_string = f"postgresql://postgres:test@{postgres_container.get_container_host_ip()}:{postgres_container.get_exposed_port(5432)}/testdb"
        
        # Run pipeline
        pipeline = DataPipeline(connection_string)
        result = pipeline.run()
        
        # Verify results
        assert result.success is True
        assert result.records_processed > 0
```

---

## 📚 Summary Guidelines

### **Universal Principles**
1. **Write self-documenting code** with clear variable names
2. **Follow DRY principle** (Don't Repeat Yourself)
3. **Implement proper error handling** at all levels
4. **Use version control** effectively with meaningful commits
5. **Document your code** and architectural decisions
6. **Test thoroughly** with unit, integration, and end-to-end tests
7. **Monitor and log** everything in production
8. **Secure by design** - never compromise on security
9. **Optimize for maintainability** over premature optimization
10. **Stay updated** with best practices and security patches

### **Data Engineering Specific**
1. **Design for scale** from the beginning
2. **Implement data quality checks** at every stage
3. **Use appropriate data formats** for your use case
4. **Plan for data governance** and compliance
5. **Implement proper data lineage** tracking
6. **Design fault-tolerant systems** with proper recovery mechanisms
7. **Optimize for both batch and streaming** processing patterns
8. **Use infrastructure as code** for reproducible deployments

---

*Following these architecture patterns and best practices ensures robust, maintainable, and scalable data engineering solutions that can handle enterprise-level requirements while maintaining code quality and security standards.*