# Data Engineering Code Best Practices & Guidelines

## 🎯 Overview
This comprehensive guide covers coding best practices, do's and don'ts for data engineering across all major technologies, languages, and platforms. Following these practices ensures maintainable, scalable, and reliable data systems.

---

## 🐍 Python Best Practices

### ✅ **DO's**
- **Use type hints** for function parameters and return values
- **Follow PEP 8** style guidelines consistently
- **Use virtual environments** for dependency isolation
- **Write docstrings** for all functions and classes
- **Use list/dict comprehensions** for simple transformations
- **Handle exceptions explicitly** with specific exception types
- **Use logging** instead of print statements
- **Validate input data** before processing
- **Use context managers** for resource management

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

### ❌ **DON'Ts**
- **Don't use global variables** for data processing
- **Don't ignore exceptions** with bare except clauses
- **Don't use mutable default arguments**
- **Don't mix tabs and spaces**
- **Don't use `import *`**
- **Don't hardcode credentials** in source code
- **Don't use deprecated libraries**

```python
# ❌ BAD
def process_data(records, config={}):  # Mutable default
    try:
        # Processing logic
        pass
    except:  # Bare except
        pass
    
    global processed_count  # Global variable
    processed_count += len(records)
```

---

## 🗃️ SQL Best Practices

### ✅ **DO's**
- **Use consistent naming conventions** (snake_case)
- **Write readable queries** with proper indentation
- **Use explicit JOIN syntax** instead of implicit joins
- **Add comments** for complex business logic
- **Use CTEs** for complex queries instead of subqueries
- **Index frequently queried columns**
- **Use LIMIT** for testing queries
- **Validate data quality** with constraints

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

### ❌ **DON'Ts**
- **Don't use SELECT \*** in production queries
- **Don't use implicit joins** (comma-separated tables)
- **Don't ignore NULL handling**
- **Don't use functions in WHERE clauses** on indexed columns
- **Don't create queries without LIMIT** during development
- **Don't use reserved words** as column names

```sql
-- ❌ BAD
SELECT * FROM orders, customers 
WHERE orders.customer_id = customers.customer_id
AND YEAR(order_date) = 2024;  -- Function on indexed column
```

---

## ⚡ PySpark Best Practices

### ✅ **DO's**
- **Use DataFrame API** over RDD when possible
- **Cache/persist** frequently accessed DataFrames
- **Use broadcast variables** for small lookup tables
- **Partition data** appropriately for your use case
- **Use column functions** instead of UDFs when possible
- **Monitor Spark UI** for performance optimization
- **Use appropriate file formats** (Parquet, Delta)
- **Handle skewed data** with salting techniques

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

### ❌ **DON'Ts**
- **Don't use collect()** on large DataFrames
- **Don't create too many small partitions**
- **Don't use Python UDFs** unnecessarily
- **Don't ignore data skew**
- **Don't forget to unpersist** cached DataFrames

---

## ☁️ Cloud Platform Best Practices

### **AWS Best Practices**

#### ✅ **DO's**
- **Use IAM roles** instead of access keys
- **Enable CloudTrail** for audit logging
- **Use S3 lifecycle policies** for cost optimization
- **Implement proper VPC security**
- **Use AWS Secrets Manager** for credentials
- **Tag all resources** for cost tracking
- **Use CloudFormation/CDK** for infrastructure

```python
# ✅ GOOD - Using boto3 with proper error handling
import boto3
from botocore.exceptions import ClientError

def upload_to_s3(file_path: str, bucket: str, key: str) -> bool:
    """Upload file to S3 with proper error handling."""
    try:
        s3_client = boto3.client('s3')
        s3_client.upload_file(file_path, bucket, key)
        return True
    except ClientError as e:
        logging.error(f"S3 upload failed: {e}")
        return False
```

#### ❌ **DON'Ts**
- **Don't hardcode AWS credentials**
- **Don't use root account** for daily operations
- **Don't ignore cost monitoring**
- **Don't leave resources untagged**
- **Don't use overly permissive IAM policies**

### **Data Lake Best Practices**

#### ✅ **DO's**
- **Organize data by date partitions**
- **Use consistent naming conventions**
- **Implement data cataloging**
- **Use columnar formats** (Parquet, ORC)
- **Implement data lineage tracking**
- **Use compression** to reduce storage costs

```
# ✅ GOOD - Data Lake Structure
s3://data-lake/
├── raw/
│   ├── year=2024/month=01/day=15/
│   └── year=2024/month=01/day=16/
├── processed/
│   ├── customers/year=2024/month=01/
│   └── orders/year=2024/month=01/
└── curated/
    ├── customer_360/
    └── sales_metrics/
```

---

## 🔄 Data Pipeline Best Practices

### ✅ **DO's**
- **Implement idempotent operations**
- **Use checkpointing** for long-running processes
- **Implement proper error handling and retries**
- **Monitor pipeline health** with alerts
- **Use configuration files** for environment-specific settings
- **Implement data quality checks**
- **Use incremental processing** when possible
- **Document data lineage**

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

### ❌ **DON'Ts**
- **Don't process all data** every time
- **Don't ignore failed records** without logging
- **Don't skip data validation**
- **Don't hardcode file paths**
- **Don't run pipelines without monitoring**

---

## 🗄️ Database Best Practices

### **General Database DO's**
- **Use connection pooling**
- **Implement proper indexing strategy**
- **Use transactions** for data consistency
- **Implement backup and recovery procedures**
- **Monitor query performance**
- **Use parameterized queries** to prevent SQL injection
- **Implement proper schema versioning**

```python
# ✅ GOOD - Database connection with pooling
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
import pandas as pd

class DatabaseManager:
    def __init__(self, connection_string: str):
        self.engine = create_engine(
            connection_string,
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True
        )
    
    def execute_query(self, query: str, params: dict = None) -> pd.DataFrame:
        """Execute query with proper error handling."""
        try:
            return pd.read_sql(query, self.engine, params=params)
        except Exception as e:
            logging.error(f"Query execution failed: {e}")
            raise
```

### **NoSQL Best Practices**

#### ✅ **DO's**
- **Design for your query patterns**
- **Use appropriate data models** for your NoSQL type
- **Implement proper sharding strategies**
- **Monitor performance metrics**
- **Use bulk operations** for better performance

#### ❌ **DON'Ts**
- **Don't treat NoSQL like relational databases**
- **Don't ignore consistency models**
- **Don't over-normalize** data structures

---

## 🔧 DevOps & Infrastructure Best Practices

### **Docker Best Practices**

#### ✅ **DO's**
- **Use multi-stage builds** to reduce image size
- **Use specific base image tags**
- **Run containers as non-root users**
- **Use .dockerignore** to exclude unnecessary files
- **Keep images small** and focused

```dockerfile
# ✅ GOOD
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

### **Kubernetes Best Practices**

#### ✅ **DO's**
- **Set resource limits and requests**
- **Use health checks** (liveness/readiness probes)
- **Use ConfigMaps and Secrets** for configuration
- **Implement proper RBAC**
- **Use namespaces** for isolation

---

## 📊 Monitoring & Logging Best Practices

### ✅ **DO's**
- **Use structured logging** (JSON format)
- **Include correlation IDs** for request tracing
- **Set up proper log levels**
- **Monitor key metrics** (latency, throughput, errors)
- **Implement alerting** for critical issues
- **Use centralized logging**

```python
# ✅ GOOD - Structured logging
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

---

## 🔒 Security Best Practices

### ✅ **DO's**
- **Use encryption** for data at rest and in transit
- **Implement proper authentication and authorization**
- **Use secrets management** systems
- **Regularly update dependencies**
- **Implement network security** (VPCs, security groups)
- **Audit access logs** regularly
- **Use least privilege principle**

### ❌ **DON'Ts**
- **Don't store credentials** in code or config files
- **Don't use default passwords**
- **Don't ignore security updates**
- **Don't expose sensitive data** in logs
- **Don't use unencrypted connections**

---

## 🧪 Testing Best Practices

### ✅ **DO's**
- **Write unit tests** for all functions
- **Use integration tests** for data pipelines
- **Test with realistic data volumes**
- **Mock external dependencies**
- **Use data quality tests**
- **Implement CI/CD pipelines**

```python
# ✅ GOOD - Unit test example
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

---

## 📈 Performance Optimization Best Practices

### ✅ **DO's**
- **Profile your code** to identify bottlenecks
- **Use appropriate data structures**
- **Implement caching** for frequently accessed data
- **Optimize database queries**
- **Use parallel processing** when appropriate
- **Monitor resource usage**

### **Memory Management**
```python
# ✅ GOOD - Memory-efficient processing
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

---

## 📋 Code Review Best Practices

### ✅ **DO's**
- **Review for logic correctness**
- **Check error handling**
- **Verify security practices**
- **Ensure code readability**
- **Check performance implications**
- **Validate test coverage**

### **Code Review Checklist**
- [ ] Code follows style guidelines
- [ ] Functions have appropriate documentation
- [ ] Error handling is implemented
- [ ] Security best practices are followed
- [ ] Performance considerations are addressed
- [ ] Tests are included and comprehensive
- [ ] No hardcoded values or credentials
- [ ] Logging is appropriate and structured

---

## 🎯 Summary Guidelines

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

*Following these best practices ensures robust, maintainable, and scalable data engineering solutions that can handle enterprise-level requirements while maintaining code quality and security standards.*