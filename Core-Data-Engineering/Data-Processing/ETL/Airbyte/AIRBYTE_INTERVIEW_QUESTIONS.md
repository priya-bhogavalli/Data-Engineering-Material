# 🎯 Airbyte Interview Questions & Answers

**Difficulty Levels**: 🟢 Beginner | 🟡 Intermediate | 🔴 Advanced  
**Total Questions**: 50+  
**Interview Frequency**: 45% of data engineering roles

---

## 🟢 Beginner Level Questions (1-2 years experience)

### **Q1: What is Airbyte and how does it differ from traditional ETL tools?**

**Answer:**
Airbyte is an open-source ELT (Extract, Load, Transform) platform that focuses on data replication and integration. Key differences from traditional ETL:

**Airbyte (ELT)**:
- Extracts and loads raw data first, transforms later
- Cloud-native, API-first architecture
- 300+ pre-built connectors
- Open source with community contributions
- Schema evolution handling

**Traditional ETL**:
- Transforms data before loading
- Often monolithic, on-premises solutions
- Limited connectors, expensive to extend
- Proprietary, vendor lock-in
- Manual schema management

**Example Use Case**:
```
Traditional ETL: Source → Transform → Load → Warehouse
Airbyte ELT: Source → Load → Warehouse → Transform (DBT)
```

---

### **Q2: Explain the main components of Airbyte architecture.**

**Answer:**
Airbyte consists of several key components:

1. **Airbyte Server**: Orchestrates data movement, manages configurations
2. **Airbyte Worker**: Executes actual data replication jobs
3. **Airbyte Scheduler**: Manages job scheduling and timing
4. **Connector Hub**: Repository of source and destination connectors
5. **Airbyte UI**: Web interface for configuration and monitoring
6. **Database**: Stores metadata, configurations, and job history

**Architecture Flow**:
```
UI → Server → Scheduler → Worker → Connectors → Destinations
```

---

### **Q3: What are the different sync modes available in Airbyte?**

**Answer:**
Airbyte supports three main sync modes:

| **Sync Mode** | **Description** | **Use Case** | **Performance** |
|---------------|-----------------|--------------|-----------------|
| **Full Refresh** | Replaces all destination data | Small datasets, complete refresh | Slow, high resource usage |
| **Incremental** | Only syncs new/changed records | Large datasets, append-only | Fast, efficient |
| **CDC (Change Data Capture)** | Real-time change tracking | Real-time requirements | Fastest, complex setup |

**Example Configuration**:
```json
{
  "sync_mode": "incremental",
  "cursor_field": ["updated_at"],
  "destination_sync_mode": "append"
}
```

---

### **Q4: How do you set up a basic connection in Airbyte?**

**Answer:**
Setting up an Airbyte connection involves these steps:

1. **Create Source Connection**:
```json
{
  "name": "MySQL Production DB",
  "source_definition_id": "mysql-source-id",
  "connection_configuration": {
    "host": "prod-db.company.com",
    "port": 3306,
    "database": "ecommerce",
    "username": "airbyte_user",
    "password": "secure_password"
  }
}
```

2. **Create Destination Connection**:
```json
{
  "name": "Snowflake Warehouse",
  "destination_definition_id": "snowflake-dest-id",
  "connection_configuration": {
    "host": "company.snowflakecomputing.com",
    "role": "AIRBYTE_ROLE",
    "warehouse": "COMPUTE_WH",
    "database": "ANALYTICS",
    "schema": "RAW_DATA"
  }
}
```

3. **Configure Connection**:
- Select streams (tables) to sync
- Choose sync mode for each stream
- Set sync frequency
- Configure field selection

---

### **Q5: What is a connector in Airbyte and how are they categorized?**

**Answer:**
A connector is a pre-built integration that handles data extraction from sources or loading to destinations.

**Categories**:

1. **Source Connectors** (Extract data):
   - Databases: MySQL, PostgreSQL, MongoDB
   - SaaS: Salesforce, HubSpot, Stripe
   - APIs: REST APIs, GraphQL
   - Files: CSV, JSON, Parquet

2. **Destination Connectors** (Load data):
   - Data Warehouses: Snowflake, BigQuery, Redshift
   - Data Lakes: S3, GCS, Azure Blob
   - Databases: PostgreSQL, MySQL
   - Analytics: Elasticsearch, ClickHouse

**Connector Certification Levels**:
- **Certified**: Production-ready, fully supported
- **Beta**: Feature-complete, limited support
- **Alpha**: Early development, community support

---

## 🟡 Intermediate Level Questions (2-4 years experience)

### **Q6: How would you handle schema evolution in Airbyte?**

**Answer:**
Schema evolution in Airbyte is handled through several mechanisms:

**1. Automatic Schema Detection**:
```json
{
  "stream": "users",
  "json_schema": {
    "type": "object",
    "properties": {
      "id": {"type": "integer"},
      "name": {"type": "string"},
      "email": {"type": "string"},
      "phone": {"type": "string"}  // New field added
    }
  }
}
```

**2. Schema Change Handling**:
- **Additive Changes**: New columns automatically detected and added
- **Breaking Changes**: Require manual intervention and connection reset
- **Data Type Changes**: May require full refresh

**3. Best Practices**:
```python
# Enable schema evolution in destination
{
  "destination_configuration": {
    "schema_evolution": "auto_add_columns",
    "handle_type_changes": "cast_when_possible"
  }
}
```

**4. Monitoring Schema Changes**:
- Set up alerts for schema drift
- Regular schema validation checks
- Version control for schema definitions

---

### **Q7: Explain how to optimize Airbyte performance for large datasets.**

**Answer:**
Performance optimization strategies for large datasets:

**1. Worker Scaling**:
```yaml
# Docker Compose scaling
services:
  worker:
    deploy:
      replicas: 5
    environment:
      - MAX_WORKERS=10
      - WORKER_ENVIRONMENT=docker
```

**2. Incremental Sync Configuration**:
```json
{
  "sync_mode": "incremental",
  "cursor_field": ["updated_at"],
  "chunk_size": 10000,
  "lookback_window": "P1D"
}
```

**3. Resource Allocation**:
```yaml
worker:
  resources:
    limits:
      memory: "16Gi"
      cpu: "4"
    requests:
      memory: "8Gi"
      cpu: "2"
```

**4. Network Optimization**:
- Use connection pooling
- Enable compression
- Optimize batch sizes
- Configure timeout settings

**5. Destination-Specific Optimizations**:
```json
// Snowflake optimization
{
  "loading_method": "Internal Staging",
  "purge_staging_data": true,
  "file_buffer_count": 10
}
```

---

### **Q8: How do you implement Change Data Capture (CDC) with Airbyte?**

**Answer:**
CDC implementation in Airbyte varies by source database:

**1. PostgreSQL CDC Setup**:
```sql
-- Enable logical replication
ALTER SYSTEM SET wal_level = logical;
ALTER SYSTEM SET max_replication_slots = 4;
ALTER SYSTEM SET max_wal_senders = 4;

-- Create replication slot
SELECT pg_create_logical_replication_slot('airbyte_slot', 'pgoutput');

-- Grant permissions
GRANT REPLICATION ON DATABASE mydb TO airbyte_user;
```

**2. MySQL CDC Configuration**:
```json
{
  "replication_method": {
    "method": "CDC",
    "initial_waiting_seconds": 300,
    "server_time_zone": "UTC"
  },
  "ssl_mode": {
    "mode": "preferred"
  }
}
```

**3. CDC Benefits**:
- Real-time data replication
- Minimal source system impact
- Captures all data changes (INSERT, UPDATE, DELETE)
- Maintains data lineage

**4. CDC Considerations**:
- Requires database configuration changes
- Higher complexity than incremental sync
- Network stability requirements
- Monitoring and alerting essential

---

### **Q9: How would you handle data quality issues in Airbyte pipelines?**

**Answer:**
Data quality management in Airbyte involves multiple layers:

**1. Source-Level Validation**:
```python
# Custom connector validation
def validate_record(record):
    if not record.get('id'):
        raise ValueError("Missing required field: id")
    if not isinstance(record.get('email'), str):
        raise TypeError("Email must be string")
    return record
```

**2. Schema Validation**:
```json
{
  "json_schema": {
    "type": "object",
    "required": ["id", "email"],
    "properties": {
      "id": {"type": "integer", "minimum": 1},
      "email": {"type": "string", "format": "email"},
      "age": {"type": "integer", "minimum": 0, "maximum": 150}
    }
  }
}
```

**3. Destination-Level Checks**:
```sql
-- Post-load data quality checks
SELECT 
  COUNT(*) as total_records,
  COUNT(DISTINCT id) as unique_ids,
  COUNT(*) - COUNT(email) as missing_emails
FROM raw_users
WHERE _airbyte_emitted_at >= CURRENT_DATE;
```

**4. Integration with Data Quality Tools**:
```python
# Great Expectations integration
import great_expectations as ge

def validate_airbyte_data(df):
    ge_df = ge.from_pandas(df)
    
    # Expectations
    ge_df.expect_column_to_exist("id")
    ge_df.expect_column_values_to_be_unique("id")
    ge_df.expect_column_values_to_not_be_null("email")
    
    return ge_df.validate()
```

**5. Monitoring and Alerting**:
```yaml
# Data quality alerts
alerts:
  - name: "High null rate"
    condition: "null_percentage > 5"
    action: "pause_sync"
  - name: "Schema drift detected"
    condition: "new_columns_detected"
    action: "notify_team"
```

---

### **Q10: Describe how to implement custom transformations in Airbyte.**

**Answer:**
Airbyte supports transformations through several approaches:

**1. Basic Normalization (Built-in)**:
```json
{
  "operation_name": "normalization",
  "operator_configuration": {
    "normalization": {
      "option": "basic"
    }
  }
}
```

**2. Custom DBT Transformations**:
```sql
-- models/staging/stg_users.sql
{{ config(materialized='view') }}

SELECT 
    id,
    LOWER(TRIM(email)) as email,
    CASE 
        WHEN age < 18 THEN 'minor'
        WHEN age >= 65 THEN 'senior'
        ELSE 'adult'
    END as age_group,
    _airbyte_emitted_at
FROM {{ source('airbyte_raw', 'users') }}
WHERE _airbyte_emitted_at IS NOT NULL
```

**3. Custom Connector Transformations**:
```python
# In custom connector
def transform_record(record: Dict[str, Any]) -> Dict[str, Any]:
    # Clean email
    if 'email' in record:
        record['email'] = record['email'].lower().strip()
    
    # Parse JSON fields
    if 'metadata' in record and isinstance(record['metadata'], str):
        record['metadata'] = json.loads(record['metadata'])
    
    # Add derived fields
    record['full_name'] = f"{record.get('first_name', '')} {record.get('last_name', '')}"
    
    return record
```

**4. Post-Load Transformations**:
```python
# Airflow DAG for post-Airbyte transformations
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def transform_airbyte_data():
    # Connect to destination
    # Apply business logic transformations
    # Update processed tables
    pass

dag = DAG('airbyte_post_processing')
transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_airbyte_data
)
```

---

## 🔴 Advanced Level Questions (4+ years experience)

### **Q11: How would you design a multi-tenant Airbyte architecture?**

**Answer:**
Multi-tenant Airbyte architecture requires careful planning for isolation, security, and scalability:

**1. Deployment Architecture**:
```yaml
# Kubernetes multi-tenant setup
apiVersion: v1
kind: Namespace
metadata:
  name: airbyte-tenant-a
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: airbyte-server
  namespace: airbyte-tenant-a
spec:
  replicas: 1
  selector:
    matchLabels:
      app: airbyte-server
      tenant: tenant-a
```

**2. Database Isolation**:
```sql
-- Separate databases per tenant
CREATE DATABASE airbyte_tenant_a;
CREATE DATABASE airbyte_tenant_b;

-- Or schema-based isolation
CREATE SCHEMA tenant_a;
CREATE SCHEMA tenant_b;
```

**3. Resource Isolation**:
```yaml
# Resource quotas per tenant
apiVersion: v1
kind: ResourceQuota
metadata:
  name: tenant-a-quota
  namespace: airbyte-tenant-a
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
```

**4. Security Considerations**:
```python
# Tenant-aware authentication
class TenantAwareAuth:
    def authenticate(self, token: str) -> Tenant:
        payload = jwt.decode(token, SECRET_KEY)
        tenant_id = payload.get('tenant_id')
        return self.get_tenant(tenant_id)
    
    def authorize_connection(self, user: User, connection_id: str):
        connection = self.get_connection(connection_id)
        if connection.tenant_id != user.tenant_id:
            raise UnauthorizedError()
```

**5. Monitoring and Observability**:
```python
# Tenant-specific metrics
airbyte_sync_duration_seconds{tenant="tenant-a", connection="mysql-to-snowflake"}
airbyte_records_synced_total{tenant="tenant-b", source="salesforce"}
```

---

### **Q12: Explain how to implement disaster recovery for Airbyte.**

**Answer:**
Disaster recovery for Airbyte involves multiple components and strategies:

**1. Data Backup Strategy**:
```bash
# Database backup
pg_dump airbyte_db > airbyte_backup_$(date +%Y%m%d).sql

# Configuration backup
kubectl get configmaps -o yaml > airbyte_configs_backup.yaml
kubectl get secrets -o yaml > airbyte_secrets_backup.yaml
```

**2. Multi-Region Deployment**:
```yaml
# Primary region (us-east-1)
primary_cluster:
  region: us-east-1
  airbyte_server: active
  database: primary
  
# Secondary region (us-west-2)  
secondary_cluster:
  region: us-west-2
  airbyte_server: standby
  database: replica
```

**3. Database Replication**:
```sql
-- PostgreSQL streaming replication
-- Primary server
archive_mode = on
archive_command = 'cp %p /archive/%f'
wal_level = replica
max_wal_senders = 3

-- Standby server
standby_mode = on
primary_conninfo = 'host=primary-db port=5432 user=replicator'
```

**4. Automated Failover**:
```python
# Health check and failover logic
class DisasterRecoveryManager:
    def check_primary_health(self):
        try:
            response = requests.get(f"{PRIMARY_URL}/health")
            return response.status_code == 200
        except:
            return False
    
    def failover_to_secondary(self):
        # Update DNS to point to secondary
        # Promote standby database
        # Start secondary Airbyte instance
        # Notify operations team
        pass
```

**5. Recovery Testing**:
```bash
# Regular DR drills
#!/bin/bash
# 1. Simulate primary failure
# 2. Execute failover procedures
# 3. Validate data integrity
# 4. Test sync resumption
# 5. Document recovery time
```

---

### **Q13: How would you implement custom metrics and monitoring for Airbyte?**

**Answer:**
Custom monitoring implementation for Airbyte production environments:

**1. Custom Metrics Collection**:
```python
# Custom metrics exporter
from prometheus_client import Counter, Histogram, Gauge
import psycopg2

class AirbyteMetricsCollector:
    def __init__(self):
        self.sync_duration = Histogram('airbyte_sync_duration_seconds')
        self.records_processed = Counter('airbyte_records_processed_total')
        self.active_connections = Gauge('airbyte_active_connections')
    
    def collect_metrics(self):
        conn = psycopg2.connect(DATABASE_URL)
        
        # Sync performance metrics
        cursor.execute("""
            SELECT 
                connection_id,
                AVG(EXTRACT(EPOCH FROM (ended_at - started_at))) as avg_duration,
                SUM(records_emitted) as total_records
            FROM jobs 
            WHERE created_at >= NOW() - INTERVAL '1 hour'
            GROUP BY connection_id
        """)
        
        for row in cursor.fetchall():
            self.sync_duration.observe(row[1])
            self.records_processed.inc(row[2])
```

**2. Grafana Dashboard Configuration**:
```json
{
  "dashboard": {
    "title": "Airbyte Operations Dashboard",
    "panels": [
      {
        "title": "Sync Success Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(airbyte_job_succeeded_total[5m]) / rate(airbyte_job_total[5m]) * 100"
          }
        ]
      },
      {
        "title": "Data Freshness",
        "type": "graph",
        "targets": [
          {
            "expr": "time() - airbyte_last_successful_sync_timestamp"
          }
        ]
      }
    ]
  }
}
```

**3. Alerting Rules**:
```yaml
# Prometheus alerting rules
groups:
  - name: airbyte_alerts
    rules:
      - alert: AirbyteSyncFailure
        expr: increase(airbyte_job_failed_total[5m]) > 0
        for: 0m
        labels:
          severity: critical
        annotations:
          summary: "Airbyte sync failed"
          
      - alert: AirbyteHighLatency
        expr: airbyte_sync_duration_seconds > 3600
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Airbyte sync taking too long"
```

**4. Custom Health Checks**:
```python
# Advanced health monitoring
class AirbyteHealthMonitor:
    def check_connector_health(self, connector_id: str):
        # Test connector connectivity
        # Validate schema discovery
        # Check resource utilization
        pass
    
    def check_data_quality(self, connection_id: str):
        # Row count validation
        # Schema drift detection
        # Data freshness checks
        pass
    
    def generate_health_report(self):
        return {
            "overall_health": "healthy",
            "active_syncs": 15,
            "failed_syncs_24h": 2,
            "avg_sync_duration": "45 minutes",
            "data_freshness": "< 1 hour"
        }
```

---

### **Q14: How would you handle Airbyte at scale with thousands of connections?**

**Answer:**
Scaling Airbyte for thousands of connections requires architectural considerations:

**1. Horizontal Scaling Architecture**:
```yaml
# Kubernetes scaling configuration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: airbyte-worker
spec:
  replicas: 50  # Scale based on connection count
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
```

**2. Database Optimization**:
```sql
-- Connection pooling and indexing
CREATE INDEX CONCURRENTLY idx_jobs_connection_status 
ON jobs(connection_id, status, created_at);

CREATE INDEX CONCURRENTLY idx_sync_stats_connection_time
ON sync_stats(connection_id, sync_start_time);

-- Partitioning for large tables
CREATE TABLE jobs_2024_01 PARTITION OF jobs
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

**3. Resource Management**:
```python
# Dynamic resource allocation
class ResourceManager:
    def calculate_worker_resources(self, connection_config):
        data_volume = self.estimate_data_volume(connection_config)
        
        if data_volume < 1_000_000:  # < 1M records
            return {"cpu": "0.5", "memory": "1Gi"}
        elif data_volume < 10_000_000:  # < 10M records
            return {"cpu": "2", "memory": "4Gi"}
        else:  # > 10M records
            return {"cpu": "4", "memory": "8Gi"}
    
    def schedule_sync(self, connection_id):
        # Implement intelligent scheduling
        # Consider resource availability
        # Avoid peak hours for large syncs
        pass
```

**4. Connection Prioritization**:
```python
# Priority-based scheduling
class ConnectionScheduler:
    def prioritize_connections(self, connections):
        return sorted(connections, key=lambda c: (
            c.business_criticality,  # High priority first
            -c.data_volume,          # Smaller jobs first
            c.last_sync_time         # Oldest syncs first
        ))
```

**5. Monitoring at Scale**:
```python
# Aggregated monitoring
class ScaleMonitoring:
    def get_cluster_health(self):
        return {
            "total_connections": 5000,
            "active_syncs": 150,
            "queued_syncs": 25,
            "worker_utilization": 0.75,
            "avg_queue_time": "2 minutes",
            "success_rate_24h": 0.98
        }
```

---

### **Q15: Explain how to implement a custom Airbyte connector from scratch.**

**Answer:**
Building a custom Airbyte connector involves several steps:

**1. Connector Specification**:
```python
# connector_spec.py
from airbyte_cdk.sources.declarative.yaml_declarative_source import YamlDeclarativeSource

class CustomAPISource(YamlDeclarativeSource):
    def __init__(self):
        super().__init__(**{"path_to_yaml": "custom_api.yaml"})
```

**2. Configuration Schema**:
```json
{
  "documentationUrl": "https://docs.company.com/api",
  "connectionSpecification": {
    "type": "object",
    "required": ["api_key", "base_url"],
    "properties": {
      "api_key": {
        "type": "string",
        "title": "API Key",
        "description": "API key for authentication",
        "airbyte_secret": true
      },
      "base_url": {
        "type": "string",
        "title": "Base URL",
        "default": "https://api.company.com/v1"
      },
      "start_date": {
        "type": "string",
        "title": "Start Date",
        "format": "date-time"
      }
    }
  }
}
```

**3. Stream Implementation**:
```python
# streams.py
from airbyte_cdk.sources.streams.http import HttpStream
from typing import Any, Iterable, Mapping, Optional

class UsersStream(HttpStream):
    url_base = "https://api.company.com/v1/"
    primary_key = "id"
    
    def __init__(self, api_key: str, start_date: str, **kwargs):
        super().__init__(**kwargs)
        self.api_key = api_key
        self.start_date = start_date
    
    def path(self, **kwargs) -> str:
        return "users"
    
    def request_headers(self, **kwargs) -> Mapping[str, Any]:
        return {"Authorization": f"Bearer {self.api_key}"}
    
    def request_params(self, **kwargs) -> Mapping[str, Any]:
        return {
            "limit": 100,
            "created_after": self.start_date
        }
    
    def parse_response(self, response, **kwargs) -> Iterable[Mapping]:
        data = response.json()
        for record in data.get("users", []):
            yield record
    
    def get_json_schema(self) -> Mapping[str, Any]:
        return {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": "string"},
                "created_at": {"type": "string", "format": "date-time"}
            }
        }
```

**4. Incremental Sync Support**:
```python
from airbyte_cdk.sources.streams.http import HttpStream
from airbyte_cdk.sources.streams import IncrementalMixin

class IncrementalUsersStream(HttpStream, IncrementalMixin):
    cursor_field = "updated_at"
    
    def get_updated_state(self, current_stream_state, latest_record):
        current_state = current_stream_state.get(self.cursor_field, self.start_date)
        latest_state = latest_record.get(self.cursor_field, current_state)
        return {self.cursor_field: max(current_state, latest_state)}
    
    def request_params(self, stream_state=None, **kwargs):
        params = super().request_params(**kwargs)
        if stream_state:
            params["updated_after"] = stream_state.get(self.cursor_field, self.start_date)
        return params
```

**5. Testing Framework**:
```python
# test_custom_connector.py
import pytest
from source_custom_api import SourceCustomApi

def test_connection():
    config = {
        "api_key": "test_key",
        "base_url": "https://api.company.com/v1",
        "start_date": "2024-01-01T00:00:00Z"
    }
    
    source = SourceCustomApi()
    status, error = source.check_connection(logger=None, config=config)
    assert status is True

def test_streams():
    source = SourceCustomApi()
    streams = source.streams(config)
    assert len(streams) > 0
    assert "users" in [s.name for s in streams]
```

**6. Deployment Configuration**:
```dockerfile
# Dockerfile
FROM airbyte/integration-base-python:1.0.0

COPY source_custom_api ./source_custom_api
COPY main.py ./
COPY setup.py ./

RUN pip install .

ENTRYPOINT ["python", "/airbyte/integration_code/main.py"]
```

This comprehensive approach covers the essential aspects of building production-ready custom Airbyte connectors with proper error handling, testing, and deployment considerations.

---

## 🎯 Interview Tips

### **Preparation Strategy**
1. **Hands-on Experience**: Set up Airbyte locally and create sample connections
2. **Architecture Understanding**: Know the components and how they interact
3. **Performance Optimization**: Understand scaling and optimization techniques
4. **Integration Patterns**: Learn how Airbyte fits in modern data stacks
5. **Troubleshooting**: Practice debugging common issues

### **Common Follow-up Questions**
- How does Airbyte compare to Fivetran/Stitch?
- When would you choose Airbyte over cloud-native ETL tools?
- How do you handle data quality in Airbyte pipelines?
- What are the security considerations for Airbyte?
- How do you monitor and alert on Airbyte performance?

### **Key Points to Emphasize**
- Open source with enterprise features
- 300+ pre-built connectors
- ELT approach vs traditional ETL
- Schema evolution handling
- Scalability and performance optimization
- Integration with modern data stack (DBT, Snowflake, etc.)

---

**🎯 Ready for your interview?** Practice these questions and explore our [Best Practices Guide](./AIRBYTE_BEST_PRACTICES.md) for additional insights!