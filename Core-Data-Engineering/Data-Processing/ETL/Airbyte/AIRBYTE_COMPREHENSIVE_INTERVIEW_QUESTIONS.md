# Airbyte - Comprehensive Interview Questions

## Table of Contents
1. [Core Concepts](#core-concepts)
2. [Architecture & Components](#architecture--components)
3. [Connectors & Sources](#connectors--sources)
4. [Configuration & Setup](#configuration--setup)
5. [Data Synchronization](#data-synchronization)
6. [Monitoring & Troubleshooting](#monitoring--troubleshooting)
7. [Deployment & Scaling](#deployment--scaling)
8. [Real-World Scenarios](#real-world-scenarios)

---

## Core Concepts

### 1. What is Airbyte and how does it differ from other ELT tools?

**Answer:**
Airbyte is an open-source data integration platform that moves data from sources to destinations using ELT approach.

**Key Differentiators:**
- **Open Source**: Full source code access and community-driven
- **Connector Development**: Easy custom connector creation
- **Self-Hosted**: Full control over infrastructure and data
- **API-First**: Everything accessible via REST API
- **Docker-Based**: Containerized architecture

**Airbyte vs Competitors:**
```
Airbyte (Open Source):
- Free to use and modify
- Self-hosted deployment
- Custom connector development
- Community support

Fivetran (Commercial):
- Fully managed service
- Pre-built connectors only
- Subscription pricing
- Enterprise support
```

### 2. Explain Airbyte's architecture and core components.

**Answer:**
**Core Components:**

1. **Airbyte Server**: Orchestrates data synchronization
2. **Airbyte Worker**: Executes sync jobs
3. **Airbyte Webapp**: User interface for configuration
4. **Airbyte Scheduler**: Manages job scheduling
5. **Database**: Stores metadata and configurations
6. **Temporal**: Workflow orchestration engine

**Architecture Diagram:**
```
[Web UI] → [Server] → [Scheduler] → [Worker] → [Source/Destination]
    ↓         ↓           ↓           ↓              ↓
  Config → API → Temporal → Docker → Connectors
```

**Component Interaction:**
```python
# Simplified workflow
def airbyte_sync_workflow():
    # 1. Scheduler triggers sync
    job = scheduler.create_sync_job(connection_id)
    
    # 2. Worker picks up job
    worker = get_available_worker()
    
    # 3. Worker runs source and destination connectors
    source_data = source_connector.read()
    destination_connector.write(source_data)
    
    # 4. Update job status
    job.update_status('completed')
```

### 3. What are Airbyte connectors and how do they work?

**Answer:**
**Airbyte Connectors** are Docker containers that implement the Airbyte Protocol for data extraction and loading.

**Connector Types:**
1. **Source Connectors**: Extract data from systems
2. **Destination Connectors**: Load data to warehouses
3. **Custom Connectors**: User-built connectors

**Airbyte Protocol:**
```json
{
  "type": "RECORD",
  "record": {
    "stream": "users",
    "data": {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com"
    },
    "emitted_at": 1640995200000
  }
}
```

**Connector Structure:**
```python
# Source connector implementation
class MySourceConnector:
    def check(self, config):
        # Test connection to source
        return {"status": "SUCCEEDED"}
    
    def discover(self, config):
        # Return available streams/tables
        return catalog
    
    def read(self, config, catalog, state):
        # Extract data and yield records
        for record in extract_data():
            yield AirbyteMessage(
                type=Type.RECORD,
                record=AirbyteRecordMessage(
                    stream=record.stream,
                    data=record.data,
                    emitted_at=int(time.time() * 1000)
                )
            )
```

### 4. How do you set up a basic Airbyte deployment?

**Answer:**
**Docker Compose Deployment:**

```yaml
# docker-compose.yml
version: "3.8"
services:
  db:
    image: postgres:13-alpine
    environment:
      POSTGRES_USER: docker
      POSTGRES_PASSWORD: docker
      POSTGRES_DB: airbyte
    volumes:
      - db:/var/lib/postgresql/data

  worker:
    image: airbyte/worker:latest
    environment:
      DATABASE_URL: postgresql://docker:docker@db:5432/airbyte
      WORKSPACE_ROOT: /tmp/workspace
    volumes:
      - workspace:/tmp/workspace
      - /var/run/docker.sock:/var/run/docker.sock

  server:
    image: airbyte/server:latest
    environment:
      DATABASE_URL: postgresql://docker:docker@db:5432/airbyte
    ports:
      - "8001:8001"

  webapp:
    image: airbyte/webapp:latest
    ports:
      - "8000:80"
    environment:
      AIRBYTE_API_URL: http://server:8001/api/v1/

volumes:
  db:
  workspace:
```

**Setup Commands:**
```bash
# Clone Airbyte repository
git clone https://github.com/airbytehq/airbyte.git
cd airbyte

# Start Airbyte
docker-compose up -d

# Access web interface
open http://localhost:8000
```

### 5. How do you configure a source and destination in Airbyte?

**Answer:**
**Source Configuration (PostgreSQL):**
```json
{
  "sourceDefinitionId": "decd338e-5647-4c0b-adf4-da0e75f5a750",
  "connectionConfiguration": {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
    "username": "postgres",
    "password": "password",
    "ssl": false,
    "replication_method": "Standard"
  },
  "name": "PostgreSQL Source"
}
```

**Destination Configuration (Snowflake):**
```json
{
  "destinationDefinitionId": "424892c4-daac-4491-b35d-c6688ba547ba",
  "connectionConfiguration": {
    "host": "account.snowflakecomputing.com",
    "role": "AIRBYTE_ROLE",
    "warehouse": "AIRBYTE_WAREHOUSE",
    "database": "AIRBYTE_DATABASE",
    "schema": "AIRBYTE_SCHEMA",
    "username": "airbyte_user",
    "password": "password"
  },
  "name": "Snowflake Destination"
}
```

**Connection Setup:**
```python
# Using Airbyte API
def create_connection():
    connection_config = {
        "sourceId": source_id,
        "destinationId": destination_id,
        "syncCatalog": {
            "streams": [
                {
                    "stream": {"name": "users", "jsonSchema": {...}},
                    "config": {
                        "syncMode": "incremental",
                        "destinationSyncMode": "append"
                    }
                }
            ]
        },
        "schedule": {
            "units": 24,
            "timeUnit": "hours"
        }
    }
    
    response = requests.post(
        f"{AIRBYTE_API_URL}/connections",
        json=connection_config
    )
    return response.json()
```

### 6. Explain different sync modes in Airbyte.

**Answer:**
**Sync Modes:**

1. **Full Refresh - Overwrite**: Replace all destination data
2. **Full Refresh - Append**: Add all source data to destination
3. **Incremental - Append**: Add only new/changed records
4. **Incremental - Deduped History**: Maintain change history with deduplication

**Sync Mode Configuration:**
```json
{
  "streams": [
    {
      "stream": {"name": "orders"},
      "config": {
        "syncMode": "incremental",
        "cursorField": ["updated_at"],
        "destinationSyncMode": "append_dedup",
        "primaryKey": [["id"]]
      }
    }
  ]
}
```

**Use Cases:**
```python
sync_mode_use_cases = {
    "full_refresh_overwrite": [
        "Small reference tables",
        "Daily snapshots",
        "Configuration data"
    ],
    "incremental_append": [
        "Event logs",
        "Time-series data",
        "Immutable records"
    ],
    "incremental_dedup": [
        "User profiles",
        "Product catalogs",
        "Transactional data"
    ]
}
```

### 7. How do you monitor Airbyte sync jobs and troubleshoot issues?

**Answer:**
**Monitoring Methods:**

1. **Web UI**: Built-in job monitoring dashboard
2. **API Monitoring**: Programmatic job status checks
3. **Logs**: Container and application logs
4. **Metrics**: Custom metrics collection

**API Monitoring:**
```python
def monitor_sync_jobs():
    # Get all connections
    connections = get_connections()
    
    for connection in connections:
        # Check latest job status
        jobs = get_jobs(connection['connectionId'])
        latest_job = jobs[0]
        
        if latest_job['status'] == 'failed':
            # Get job logs
            logs = get_job_logs(latest_job['id'])
            
            # Send alert
            send_alert(f"Sync failed: {connection['name']}", logs)
        
        # Check data freshness
        last_sync = latest_job['createdAt']
        if is_data_stale(last_sync):
            send_freshness_alert(connection['name'])
```

**Common Issues and Solutions:**
```python
troubleshooting_guide = {
    "connection_timeout": {
        "cause": "Network connectivity issues",
        "solution": "Check firewall rules, increase timeout"
    },
    "schema_mismatch": {
        "cause": "Source schema changed",
        "solution": "Refresh source schema, update connection"
    },
    "out_of_memory": {
        "cause": "Large dataset processing",
        "solution": "Increase worker memory, use incremental sync"
    },
    "authentication_failed": {
        "cause": "Invalid credentials",
        "solution": "Update source/destination credentials"
    }
}
```

### 8. How do you create a custom Airbyte connector?

**Answer:**
**Connector Development Process:**

1. **Use Connector Development Kit (CDK)**
2. **Implement Required Methods**
3. **Test Connector**
4. **Build Docker Image**
5. **Deploy to Airbyte**

**Custom Source Connector:**
```python
# source.py
from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream

class MyCustomSource(AbstractSource):
    def check_connection(self, logger, config):
        try:
            # Test connection to your API/database
            api_client = MyAPIClient(config)
            api_client.test_connection()
            return True, None
        except Exception as e:
            return False, str(e)
    
    def streams(self, config):
        return [
            UsersStream(config),
            OrdersStream(config)
        ]

class UsersStream(Stream):
    primary_key = "id"
    cursor_field = "updated_at"
    
    def read_records(self, sync_mode, cursor_field=None, stream_slice=None, stream_state=None):
        # Extract data from your source
        for user in self.api_client.get_users():
            yield {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "updated_at": user.updated_at
            }
```

**Connector Configuration:**
```yaml
# connector specification
spec:
  type: object
  properties:
    api_key:
      type: string
      description: API key for authentication
      airbyte_secret: true
    base_url:
      type: string
      description: Base URL for API
      default: "https://api.example.com"
```

**Build and Deploy:**
```bash
# Build connector image
docker build -t my-custom-source .

# Test connector
python main.py check --config config.json
python main.py discover --config config.json
python main.py read --config config.json --catalog catalog.json

# Add to Airbyte
# Upload connector definition via UI or API
```

### 9. How do you scale Airbyte for high-volume data processing?

**Answer:**
**Scaling Strategies:**

1. **Horizontal Scaling**: Multiple worker nodes
2. **Resource Optimization**: CPU/memory allocation
3. **Parallel Processing**: Concurrent sync jobs
4. **Infrastructure Scaling**: Kubernetes deployment

**Kubernetes Deployment:**
```yaml
# airbyte-worker-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: airbyte-worker
spec:
  replicas: 5  # Scale workers
  selector:
    matchLabels:
      app: airbyte-worker
  template:
    metadata:
      labels:
        app: airbyte-worker
    spec:
      containers:
      - name: worker
        image: airbyte/worker:latest
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        env:
        - name: MAX_SYNC_WORKERS
          value: "10"
```

**Performance Optimization:**
```python
# Optimize sync performance
def optimize_sync_performance():
    optimizations = {
        "batch_size": 10000,  # Records per batch
        "parallel_streams": 4,  # Concurrent streams
        "memory_limit": "4GB",  # Worker memory
        "timeout": 3600,  # Sync timeout
        "retry_attempts": 3  # Failed job retries
    }
    
    return optimizations
```

### 10. Design a complete data pipeline using Airbyte for an e-commerce company.

**Answer:**
**Architecture:**
```
Sources → Airbyte → Data Lake → Processing → Data Warehouse → BI
   ↓         ↓         ↓           ↓            ↓           ↓
MySQL → Connectors → S3 → Spark → Snowflake → Tableau
Shopify                                        
Stripe                                         
Google Ads                                     
```

**Implementation:**
```yaml
# Data pipeline configuration
sources:
  - name: mysql_orders
    type: mysql
    config:
      host: mysql.company.com
      database: ecommerce
      tables: [orders, order_items, customers]
      sync_mode: incremental
      cursor_field: updated_at
    
  - name: shopify_store
    type: shopify
    config:
      shop: company-store
      api_password: ${SHOPIFY_API_PASSWORD}
      sync_mode: incremental
    
  - name: stripe_payments
    type: stripe
    config:
      account_id: acct_123456789
      client_secret: ${STRIPE_SECRET}
      sync_mode: incremental

destinations:
  - name: s3_data_lake
    type: s3
    config:
      bucket: company-data-lake
      prefix: raw/
      format: parquet
  
  - name: snowflake_warehouse
    type: snowflake
    config:
      host: company.snowflakecomputing.com
      database: ANALYTICS
      schema: RAW_DATA
```

**Monitoring and Alerting:**
```python
def setup_monitoring():
    # Monitor sync health
    monitor_configs = [
        {
            "connection": "mysql_orders",
            "max_delay": "2 hours",
            "alert_channel": "slack"
        },
        {
            "connection": "shopify_store", 
            "max_delay": "1 hour",
            "alert_channel": "email"
        }
    ]
    
    for config in monitor_configs:
        setup_sync_monitoring(config)
    
    # Data quality checks
    setup_data_quality_monitoring()
    
    # Performance monitoring
    setup_performance_monitoring()
```

This comprehensive set of Airbyte interview questions covers the essential aspects of this open-source ELT platform, from basic concepts to advanced deployment and scaling scenarios.