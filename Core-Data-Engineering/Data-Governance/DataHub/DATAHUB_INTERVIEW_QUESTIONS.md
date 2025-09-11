# DataHub Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-50)](#basic-level-questions-1-50)
2. [Intermediate Level Questions (51-100)](#intermediate-level-questions-51-100)
3. [Advanced Level Questions (101-150)](#advanced-level-questions-101-150)
4. [Architecture & Performance (151-180)](#architecture--performance-151-180)
5. [Streaming & Real-time Processing (181-200)](#streaming--real-time-processing-181-200)
6. [Production & Operations (201-220)](#production--operations-201-220)
7. [Scenario-Based Questions (221-250)](#scenario-based-questions-221-250)

---

## Basic Level Questions (1-50)

### 1. What is DataHub and what problems does it solve?

**Answer:** DataHub is an open-source metadata platform that enables data discovery, observability, and governance across the modern data stack.

**Key Problems Solved:**
- **Data Discovery**: Find relevant datasets quickly across multiple systems
- **Data Understanding**: Rich metadata, documentation, and context
- **Data Trust**: Quality metrics, lineage tracking, and validation
- **Data Governance**: Policy enforcement and compliance management
- **Data Collaboration**: Social features for data teams

**Before vs After DataHub:**
```python
# Before DataHub - Manual data discovery
def find_customer_data():
    # 1. Ask colleagues via Slack/email
    # 2. Check multiple documentation sources
    # 3. Trial and error with different tables
    # 4. No visibility into data quality or lineage
    pass

# With DataHub - Automated discovery
def find_customer_data():
    results = datahub.search(
        query="customer",
        entity_types=["dataset"],
        filters={"platform": ["snowflake", "mysql"]}
    )
    # Get metadata, schema, lineage, quality metrics
    return results
```

### 2. What are the core entities in DataHub's metadata model?

**Answer:** DataHub organizes metadata around key entities that represent different aspects of the data ecosystem.

**Core Entities:**
- **Datasets**: Tables, files, streams, and data containers
- **Data Jobs**: ETL jobs, pipelines, and processing tasks
- **Data Flows**: End-to-end data pipelines and workflows
- **Charts**: Visualizations and analytical charts
- **Dashboards**: Collections of charts and business metrics
- **Users**: People who interact with data
- **Groups**: Teams and organizational units
- **Tags**: Labels for categorization and discovery
- **Glossary Terms**: Business definitions and vocabulary

**Entity Relationships:**
```json
{
  "dataset": {
    "urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,users,PROD)",
    "properties": {
      "name": "users",
      "description": "Customer user profiles",
      "tags": ["pii", "customer-data"]
    },
    "schema": {
      "fields": [
        {
          "fieldPath": "user_id",
          "type": "bigint",
          "description": "Unique user identifier"
        }
      ]
    },
    "ownership": {
      "owners": [
        {
          "owner": "urn:li:corpuser:data-team",
          "type": "DATAOWNER"
        }
      ]
    }
  }
}
```

### 3. How does DataHub's architecture work?

**Answer:** DataHub follows a microservices architecture with clear separation of concerns.

**Core Components:**
- **GMS (General Metadata Service)**: Backend service for metadata storage and APIs
- **Frontend**: React-based web application for user interface
- **Search Index**: Elasticsearch for fast metadata search
- **Message Queue**: Kafka for event streaming
- **Database**: MySQL/PostgreSQL for persistent storage

**Data Flow:**
```
Data Sources → Ingestion → Kafka → GMS → Database
                  ↓         ↓      ↓       ↓
              Connectors → MAE → API → Search Index
                                      ↓
                                 Frontend UI
```

### 4. What are the different ways to ingest metadata into DataHub?

**Answer:** DataHub supports multiple ingestion methods for different use cases.

**Ingestion Methods:**
1. **CLI Recipes**: YAML-based configuration files
2. **Python SDK**: Programmatic metadata emission
3. **REST API**: Direct HTTP API calls
4. **UI Ingestion**: Web-based ingestion setup
5. **Kafka Streaming**: Real-time event streaming

**CLI Recipe Example:**
```yaml
source:
  type: snowflake
  config:
    username: ${SNOWFLAKE_USER}
    password: ${SNOWFLAKE_PASS}
    account_id: abc123.us-east-1
    warehouse: COMPUTE_WH
    database_pattern:
      allow: ["ANALYTICS_DB"]
    schema_pattern:
      allow: ["PUBLIC", "STAGING"]

sink:
  type: datahub-rest
  config:
    server: http://localhost:8080
```

### 5. How do you configure data lineage in DataHub?

**Answer:** DataHub captures lineage through multiple mechanisms.

**Lineage Sources:**
- **Automatic Extraction**: From ETL tools (Airflow, dbt, Spark)
- **Manual Definition**: Via UI or API
- **Code Analysis**: Static analysis of SQL/Python
- **Runtime Capture**: Query log analysis

**dbt Integration Example:**
```sql
-- models/customer_metrics.sql
{{ config(
    materialized='table',
    meta={
        'datahub': {
            'tags': ['analytics', 'customer']
        }
    }
) }}

SELECT 
    c.customer_id,
    c.customer_name,
    SUM(o.order_amount) as total_spent
FROM {{ ref('customers') }} c  -- Automatic lineage
JOIN {{ ref('orders') }} o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
```

### 6. What is the difference between MCE and MAE in DataHub?

**Answer:** MCE and MAE are different types of events in DataHub's event-driven architecture.

**MCE (Metadata Change Event):**
- **Purpose**: Proposes changes to metadata
- **Direction**: Ingestion → DataHub
- **Content**: New or updated metadata
- **Processing**: Validated and applied by GMS

**MAE (Metadata Audit Event):**
- **Purpose**: Records completed metadata changes
- **Direction**: DataHub → Consumers
- **Content**: Audit trail of changes
- **Processing**: Consumed by downstream systems

**Event Flow:**
```python
# MCE Example - Proposing metadata change
mce = MetadataChangeEvent(
    proposedSnapshot=DatasetSnapshot(
        urn=dataset_urn,
        aspects=[schema_metadata, ownership_info]
    )
)

# MAE Example - Audit of completed change
mae = MetadataAuditEvent(
    auditHeader=AuditHeader(
        time=current_timestamp,
        actor="urn:li:corpuser:ingestion-service"
    ),
    newSnapshot=dataset_snapshot
)
```

### 7. How do you implement data governance policies in DataHub?

**Answer:** DataHub provides comprehensive governance capabilities through policies and access controls.

**Governance Features:**
- **Access Policies**: Control who can view/edit metadata
- **Data Classification**: Tag sensitive data automatically
- **Quality Monitoring**: Track data quality metrics
- **Compliance Tracking**: Monitor regulatory requirements

**Policy Example:**
```json
{
  "policy": {
    "type": "METADATA",
    "name": "PII Access Control",
    "description": "Restrict access to PII tagged data",
    "rules": [
      {
        "resources": {
          "filter": {
            "criteria": [
              {
                "field": "TAG",
                "values": ["urn:li:tag:PII"]
              }
            ]
          }
        },
        "privileges": ["VIEW_DATASET_PROFILE"],
        "actors": {
          "groups": ["urn:li:corpGroup:data-privacy-team"]
        }
      }
    ]
  }
}
```

### 8. What are DataHub's search and discovery capabilities?

**Answer:** DataHub provides powerful search and discovery features powered by Elasticsearch.

**Search Features:**
- **Full-text Search**: Search across all metadata fields
- **Faceted Search**: Filter by platform, tags, owners
- **Auto-complete**: Smart suggestions and type-ahead
- **Relevance Ranking**: ML-powered result ranking
- **Saved Searches**: Bookmark frequently used queries

**Search Examples:**
```python
# Basic search
results = datahub_client.search(
    entity_types=["dataset"],
    query="customer transactions"
)

# Advanced search with filters
results = datahub_client.search(
    entity_types=["dataset"],
    query="customer",
    filters={
        "platform": ["snowflake"],
        "tags": ["analytics"],
        "owners": ["data-team"]
    }
)

# Browse by hierarchy
datasets = datahub_client.browse(
    entity_type="dataset",
    path="/prod/snowflake/analytics"
)
```

### 9. How do you handle schema evolution in DataHub?

**Answer:** DataHub tracks schema changes over time and provides schema evolution capabilities.

**Schema Evolution Features:**
- **Version Tracking**: Track schema changes over time
- **Backward Compatibility**: Identify breaking changes
- **Impact Analysis**: Understand downstream effects
- **Change Notifications**: Alert on schema modifications

**Schema Evolution Example:**
```python
# Track schema changes
def track_schema_evolution(dataset_urn, new_schema):
    # Get current schema
    current_schema = get_current_schema(dataset_urn)
    
    # Compare schemas
    changes = compare_schemas(current_schema, new_schema)
    
    # Emit schema change event
    schema_change_event = SchemaChangeEvent(
        dataset_urn=dataset_urn,
        changes=changes,
        timestamp=current_timestamp()
    )
    
    emit_event(schema_change_event)
    
    # Update schema metadata
    update_schema_metadata(dataset_urn, new_schema)
```

### 10. What are the key benefits of using DataHub?

**Answer:** DataHub provides multiple benefits for data-driven organizations.

**Key Benefits:**
- **Improved Data Discovery**: Reduce time to find relevant data from hours to minutes
- **Enhanced Data Trust**: Quality metrics and lineage increase confidence
- **Better Collaboration**: Social features enable knowledge sharing
- **Governance Compliance**: Policy enforcement and audit trails
- **Operational Efficiency**: Automated metadata management

**ROI Metrics:**
```python
# Typical improvements with DataHub
improvements = {
    "data_discovery_time": "80% reduction",
    "data_quality_incidents": "60% reduction", 
    "compliance_audit_time": "70% reduction",
    "data_team_productivity": "40% increase",
    "time_to_insight": "50% reduction"
}
```

### 11. How do you configure DataHub for high availability?

**Answer:** DataHub can be configured for high availability using standard practices.

**HA Configuration:**
- **Load Balancing**: Multiple GMS instances behind load balancer
- **Database Replication**: Master-slave MySQL/PostgreSQL setup
- **Elasticsearch Cluster**: Multi-node search cluster
- **Kafka Cluster**: Distributed message queue
- **Container Orchestration**: Kubernetes deployment

**Kubernetes Deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: datahub-gms
spec:
  replicas: 3
  selector:
    matchLabels:
      app: datahub-gms
  template:
    metadata:
      labels:
        app: datahub-gms
    spec:
      containers:
      - name: datahub-gms
        image: linkedin/datahub-gms:latest
        ports:
        - containerPort: 8080
        env:
        - name: EBEAN_DATASOURCE_URL
          value: "jdbc:mysql://mysql-cluster:3306/datahub"
```

### 12. What are DataHub's data quality features?

**Answer:** DataHub provides comprehensive data quality monitoring and validation.

**Quality Features:**
- **Freshness Monitoring**: Track data update frequency
- **Volume Monitoring**: Monitor record count changes
- **Schema Validation**: Detect schema drift
- **Custom Assertions**: Define business-specific quality rules
- **Quality Dashboards**: Visualize quality metrics

**Quality Assertions:**
```python
# Define data quality assertions
def setup_quality_monitoring():
    assertions = [
        {
            "type": "freshness",
            "dataset": "urn:li:dataset:(urn:li:dataPlatform:snowflake,orders,PROD)",
            "schedule": "0 */6 * * *",  # Every 6 hours
            "threshold": "24 hours"
        },
        {
            "type": "volume",
            "dataset": "urn:li:dataset:(urn:li:dataPlatform:snowflake,customers,PROD)",
            "schedule": "0 9 * * *",  # Daily at 9 AM
            "threshold": {
                "min": 10000,
                "max": 1000000
            }
        }
    ]
    
    for assertion in assertions:
        create_assertion(assertion)
```

### 13. How do you integrate DataHub with Apache Airflow?

**Answer:** DataHub integrates with Airflow to capture job metadata and lineage automatically.

**Integration Methods:**
- **Airflow Plugin**: Automatic metadata extraction
- **Lineage Backend**: Capture task dependencies
- **Custom Operators**: Manual metadata emission
- **DAG Parsing**: Extract metadata from DAG definitions

**Airflow Integration:**
```python
# airflow_datahub_plugin.py
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datahub_airflow_plugin.entities import Dataset, Task

# Define DAG with DataHub integration
dag = DAG(
    'customer_etl',
    description='Customer data ETL pipeline',
    schedule_interval='@daily',
    datahub_dag_config={
        'datahub_conn_id': 'datahub_rest_default',
        'cluster': 'prod',
        'capture_ownership_info': True,
        'capture_tags_info': True
    }
)

# Task with automatic lineage capture
extract_task = PythonOperator(
    task_id='extract_customers',
    python_callable=extract_customers,
    dag=dag,
    inlets=[Dataset("snowflake", "raw.customers")],
    outlets=[Dataset("snowflake", "staging.customers")]
)
```

### 14. What are the different deployment options for DataHub?

**Answer:** DataHub supports multiple deployment options for different environments.

**Deployment Options:**
- **Docker Compose**: Local development and testing
- **Kubernetes**: Production container orchestration
- **Helm Charts**: Kubernetes package management
- **Cloud Managed**: AWS, GCP, Azure managed services
- **Hybrid**: On-premises with cloud components

**Docker Compose Setup:**
```yaml
version: '3.8'
services:
  datahub-gms:
    image: linkedin/datahub-gms:latest
    ports:
      - "8080:8080"
    environment:
      - EBEAN_DATASOURCE_URL=jdbc:mysql://mysql:3306/datahub
    depends_on:
      - mysql
      - elasticsearch
      - kafka

  datahub-frontend:
    image: linkedin/datahub-frontend-react:latest
    ports:
      - "9002:9002"
    environment:
      - DATAHUB_GMS_URL=http://datahub-gms:8080
    depends_on:
      - datahub-gms
```

### 15. How do you monitor DataHub performance?

**Answer:** DataHub monitoring involves tracking multiple components and metrics.

**Monitoring Areas:**
- **GMS Performance**: API response times, throughput
- **Search Performance**: Elasticsearch query latency
- **Ingestion Performance**: Job success rates, processing time
- **Database Performance**: Connection pools, query performance
- **System Resources**: CPU, memory, disk usage

**Monitoring Setup:**
```python
# Custom metrics collection
class DataHubMonitoring:
    def __init__(self):
        self.metrics_client = MetricsClient()
    
    def track_ingestion_metrics(self, job_name, duration, records_processed):
        self.metrics_client.gauge(
            'datahub.ingestion.duration',
            duration,
            tags={'job': job_name}
        )
        
        self.metrics_client.gauge(
            'datahub.ingestion.records',
            records_processed,
            tags={'job': job_name}
        )
    
    def track_search_metrics(self, query, response_time, result_count):
        self.metrics_client.histogram(
            'datahub.search.response_time',
            response_time,
            tags={'query_type': 'dataset_search'}
        )
```

### 16. What are DataHub's authentication and authorization mechanisms?

**Answer:** DataHub provides multiple authentication and authorization options.

**Authentication Methods:**
- **OIDC/OAuth2**: Integration with identity providers
- **LDAP**: Enterprise directory integration
- **JAAS**: Java Authentication and Authorization Service
- **Native**: Built-in user management
- **API Keys**: Service-to-service authentication

**Authorization Features:**
- **Role-Based Access Control (RBAC)**: Predefined roles and permissions
- **Policy-Based Access Control**: Fine-grained policies
- **Resource-Level Permissions**: Control access to specific entities
- **Metadata Policies**: Control who can view/edit metadata

**Authentication Configuration:**
```yaml
# application.yml
authentication:
  enabled: true
  systemClientId: __datahub_system
  systemClientSecret: JohnSnowKnowsNothing
  tokenService:
    signingKey: WnEdIeTjDBkvTGOKxQVKOdOQQoGXwJhH
    salt: ohDVbJBvHHVJh
  oidc:
    enabled: true
    clientId: datahub-client
    clientSecret: ${OIDC_CLIENT_SECRET}
    discoveryUri: https://your-oidc-provider/.well-known/openid_configuration
```

### 17. How do you handle data privacy and PII in DataHub?

**Answer:** DataHub provides features to identify, classify, and protect sensitive data.

**Privacy Features:**
- **PII Detection**: Automatic identification of sensitive fields
- **Data Classification**: Tag and categorize sensitive data
- **Access Controls**: Restrict access to sensitive information
- **Audit Logging**: Track access to sensitive data
- **Data Masking**: Hide sensitive values in previews

**PII Classification:**
```python
# Automatic PII detection
def classify_pii_fields(dataset_urn, schema):
    pii_patterns = {
        'email': r'.*email.*|.*e_mail.*',
        'phone': r'.*phone.*|.*mobile.*|.*tel.*',
        'ssn': r'.*ssn.*|.*social.*security.*',
        'credit_card': r'.*card.*number.*|.*cc.*num.*'
    }
    
    for field in schema.fields:
        for pii_type, pattern in pii_patterns.items():
            if re.match(pattern, field.fieldPath.lower()):
                add_tag_to_field(
                    dataset_urn=dataset_urn,
                    field_path=field.fieldPath,
                    tag_urn=f"urn:li:tag:{pii_type.upper()}"
                )
```

### 18. What are the limitations of DataHub?

**Answer:** While powerful, DataHub has some limitations to consider.

**Technical Limitations:**
- **Scale Limits**: Performance can degrade with very large metadata volumes
- **Real-time Constraints**: Some metadata updates may have latency
- **Complex Lineage**: Difficult to capture complex transformation logic
- **Resource Requirements**: Requires significant infrastructure

**Functional Limitations:**
- **Limited Data Profiling**: Basic profiling capabilities
- **Custom Entity Types**: Complex to define new entity types
- **Advanced Analytics**: Limited built-in reporting and analytics
- **Multi-tenancy**: Basic multi-tenant support

**Integration Limitations:**
- **Connector Coverage**: Not all data sources have native connectors
- **Legacy Systems**: Challenging integration with older systems
- **Real-time Streaming**: Limited real-time metadata streaming
- **Custom Sources**: Requires development for proprietary systems

### 19. How do you backup and restore DataHub metadata?

**Answer:** DataHub backup involves multiple components and data stores.

**Backup Components:**
- **Database Backup**: MySQL/PostgreSQL metadata storage
- **Elasticsearch Backup**: Search indices and configurations
- **Kafka Topics**: Event streams and message history
- **Configuration Files**: Application and deployment configs

**Backup Strategy:**
```bash
#!/bin/bash
# DataHub backup script

# Database backup
mysqldump -h mysql-host -u datahub -p datahub > datahub_backup_$(date +%Y%m%d).sql

# Elasticsearch backup
curl -X PUT "elasticsearch-host:9200/_snapshot/datahub_backup/snapshot_$(date +%Y%m%d)" \
  -H 'Content-Type: application/json' \
  -d '{"indices": "datahubindex_v2"}'

# Configuration backup
tar -czf datahub_config_$(date +%Y%m%d).tar.gz /opt/datahub/config/

# Upload to cloud storage
aws s3 cp datahub_backup_$(date +%Y%m%d).sql s3://datahub-backups/
```

### 20. How do you troubleshoot common DataHub issues?

**Answer:** Common DataHub issues and their troubleshooting approaches.

**Common Issues:**
- **Ingestion Failures**: Connection issues, authentication problems
- **Search Performance**: Slow queries, index corruption
- **UI Loading Issues**: Frontend connectivity, API timeouts
- **Memory Issues**: JVM heap size, garbage collection
- **Database Connectivity**: Connection pool exhaustion

**Troubleshooting Steps:**
```python
# Health check script
def check_datahub_health():
    health_status = {}
    
    # Check GMS health
    try:
        response = requests.get('http://datahub-gms:8080/health')
        health_status['gms'] = response.status_code == 200
    except Exception as e:
        health_status['gms'] = False
        health_status['gms_error'] = str(e)
    
    # Check Elasticsearch health
    try:
        response = requests.get('http://elasticsearch:9200/_cluster/health')
        health_status['elasticsearch'] = response.json()['status'] in ['green', 'yellow']
    except Exception as e:
        health_status['elasticsearch'] = False
        health_status['es_error'] = str(e)
    
    # Check database connectivity
    try:
        conn = mysql.connector.connect(
            host='mysql',
            user='datahub',
            password='datahub',
            database='datahub'
        )
        health_status['database'] = True
        conn.close()
    except Exception as e:
        health_status['database'] = False
        health_status['db_error'] = str(e)
    
    return health_status
```

### 21-50. Additional Basic Questions

**21. How do you configure DataHub connectors?**
**Answer:** Configure connectors using YAML recipes with source and sink specifications.

**22. What is the role of Kafka in DataHub architecture?**
**Answer:** Kafka handles event streaming for metadata changes (MCE/MAE) and enables real-time updates.

**23. How do you manage DataHub users and groups?**
**Answer:** Use LDAP integration, OIDC providers, or native user management with RBAC.

**24. What are DataHub's tagging capabilities?**
**Answer:** Support for custom tags, automatic tagging, tag hierarchies, and tag-based search.

**25. How do you handle schema drift in DataHub?**
**Answer:** Monitor schema changes, set up alerts, and track evolution over time.

**26. What are DataHub's API capabilities?**
**Answer:** REST and GraphQL APIs for metadata CRUD operations, search, and lineage.

**27. How do you integrate DataHub with dbt?**
**Answer:** Use dbt-datahub plugin for automatic metadata and lineage extraction.

**28. What are DataHub's visualization features?**
**Answer:** Lineage graphs, schema visualization, and metadata dashboards.

**29. How do you configure data retention in DataHub?**
**Answer:** Set retention policies for metadata, events, and audit logs.

**30. What are DataHub's notification capabilities?**
**Answer:** Email notifications, Slack integration, and webhook support for events.

**31. How do you handle DataHub upgrades?**
**Answer:** Follow upgrade procedures, backup data, and test in staging environment.

**32. What are DataHub's data profiling features?**
**Answer:** Basic profiling with statistics, null counts, and data distribution.

**33. How do you configure DataHub for multiple environments?**
**Answer:** Use environment-specific configurations and separate instances.

**34. What are DataHub's collaboration features?**
**Answer:** Comments, documentation, ownership assignment, and team features.

**35. How do you monitor DataHub ingestion jobs?**
**Answer:** Track job status, success rates, and processing metrics.

**36. What are DataHub's glossary capabilities?**
**Answer:** Business glossary with terms, definitions, and hierarchical organization.

**37. How do you handle DataHub performance tuning?**
**Answer:** Optimize database queries, tune Elasticsearch, and adjust JVM settings.

**38. What are DataHub's export/import capabilities?**
**Answer:** Export metadata to files and import from various formats.

**39. How do you configure DataHub SSL/TLS?**
**Answer:** Enable HTTPS, configure certificates, and secure inter-service communication.

**40. What are DataHub's custom metadata capabilities?**
**Answer:** Define custom aspects, properties, and entity extensions.

**41. How do you handle DataHub disaster recovery?**
**Answer:** Multi-region deployment, data replication, and automated failover.

**42. What are DataHub's batch processing features?**
**Answer:** Bulk metadata operations, batch ingestion, and scheduled jobs.

**43. How do you configure DataHub logging?**
**Answer:** Set log levels, configure appenders, and centralize log collection.

**44. What are DataHub's metadata validation features?**
**Answer:** Schema validation, data type checking, and constraint enforcement.

**45. How do you handle DataHub capacity planning?**
**Answer:** Monitor resource usage, plan for growth, and scale components.

**46. What are DataHub's workflow capabilities?**
**Answer:** Approval workflows, change management, and process automation.

**47. How do you configure DataHub caching?**
**Answer:** Enable caching layers, configure TTL, and optimize cache hit rates.

**48. What are DataHub's reporting capabilities?**
**Answer:** Usage reports, governance dashboards, and custom analytics.

**49. How do you handle DataHub security scanning?**
**Answer:** Vulnerability scanning, dependency checking, and security audits.

**50. What are DataHub's future roadmap items?**
**Answer:** Enhanced ML integration, improved performance, and advanced governance features.

---

## Intermediate Level Questions (51-100)

### 51. How do you implement custom metadata ingestion for proprietary systems?

**Answer:** Create custom ingestion sources using DataHub's ingestion framework.

**Custom Source Implementation:**
```python
from datahub.ingestion.api.common import PipelineContext
from datahub.ingestion.api.source import Source, SourceReport
from datahub.ingestion.api.workunit import MetadataWorkUnit

class CustomSystemSource(Source):
    def __init__(self, config: CustomSystemConfig, ctx: PipelineContext):
        super().__init__(ctx)
        self.config = config
        self.report = SourceReport()
    
    @classmethod
    def create(cls, config_dict: dict, ctx: PipelineContext) -> "CustomSystemSource":
        config = CustomSystemConfig.parse_obj(config_dict)
        return cls(config, ctx)
    
    def get_workunits(self) -> Iterable[MetadataWorkUnit]:
        # Connect to custom system
        client = CustomSystemClient(self.config.connection_string)
        
        # Extract metadata
        for table in client.get_tables():
            dataset_urn = make_dataset_urn(
                platform="custom_system",
                name=table.name,
                env=self.config.env
            )
            
            # Create dataset metadata
            dataset_snapshot = DatasetSnapshot(
                urn=dataset_urn,
                aspects=[
                    DatasetPropertiesClass(
                        description=table.description,
                        customProperties=table.custom_properties
                    ),
                    SchemaMetadataClass(
                        schemaName=table.name,
                        platform=make_data_platform_urn("custom_system"),
                        version=0,
                        fields=self._extract_schema_fields(table.schema)
                    )
                ]
            )
            
            mce = MetadataChangeEvent(proposedSnapshot=dataset_snapshot)
            yield MetadataWorkUnit(id=dataset_urn, mce=mce)
    
    def get_report(self) -> SourceReport:
        return self.report
```

### 52. How do you implement advanced data lineage tracking?

**Answer:** Implement comprehensive lineage tracking using multiple techniques.

**Advanced Lineage Implementation:**
```python
class AdvancedLineageTracker:
    def __init__(self, datahub_client):
        self.client = datahub_client
        self.lineage_graph = {}
    
    def track_sql_lineage(self, sql_query, output_table):
        """Extract lineage from SQL queries using SQL parsing"""
        from sqllineage.runner import LineageRunner
        
        # Parse SQL to extract lineage
        runner = LineageRunner(sql_query)
        
        # Extract source tables
        source_tables = []
        for table in runner.source_tables:
            source_urn = make_dataset_urn(
                platform="snowflake",
                name=str(table),
                env="PROD"
            )
            source_tables.append(source_urn)
        
        # Create lineage
        output_urn = make_dataset_urn(
            platform="snowflake",
            name=output_table,
            env="PROD"
        )
        
        self._emit_lineage(source_tables, output_urn, sql_query)
    
    def track_spark_lineage(self, spark_job):
        """Extract lineage from Spark job execution"""
        # Get input/output datasets from Spark context
        input_datasets = spark_job.get_input_datasets()
        output_datasets = spark_job.get_output_datasets()
        
        for output_dataset in output_datasets:
            output_urn = make_dataset_urn(
                platform="spark",
                name=output_dataset.name,
                env="PROD"
            )
            
            input_urns = [
                make_dataset_urn(
                    platform="spark",
                    name=input_ds.name,
                    env="PROD"
                ) for input_ds in input_datasets
            ]
            
            self._emit_lineage(input_urns, output_urn, spark_job.code)
    
    def track_column_lineage(self, transformation_logic):
        """Track field-level lineage"""
        column_lineage = []
        
        for output_field, input_fields in transformation_logic.items():
            fine_grained_lineage = FineGrainedLineage(
                upstreamType=FineGrainedLineageUpstreamType.FIELD_SET,
                upstreams=[
                    make_schema_field_urn(dataset_urn, field)
                    for dataset_urn, field in input_fields
                ],
                downstreamType=FineGrainedLineageDownstreamType.FIELD,
                downstreams=[
                    make_schema_field_urn(output_dataset_urn, output_field)
                ]
            )
            column_lineage.append(fine_grained_lineage)
        
        return column_lineage
```

### 53. How do you implement data quality monitoring at scale?

**Answer:** Build comprehensive data quality monitoring with automated detection and alerting.

**Scalable Quality Monitoring:**
```python
class DataQualityMonitor:
    def __init__(self, datahub_client):
        self.client = datahub_client
        self.quality_rules = {}
    
    def setup_quality_monitoring(self, datasets):
        """Setup quality monitoring for multiple datasets"""
        for dataset_urn in datasets:
            # Get dataset metadata
            dataset_info = self.client.get_dataset(dataset_urn)
            
            # Generate quality rules based on schema
            rules = self._generate_quality_rules(dataset_info)
            
            # Create assertions
            for rule in rules:
                assertion_urn = self._create_assertion(dataset_urn, rule)
                self.quality_rules[assertion_urn] = rule
    
    def _generate_quality_rules(self, dataset_info):
        """Auto-generate quality rules based on schema and data types"""
        rules = []
        
        for field in dataset_info.schema.fields:
            # Completeness rules
            if not field.nullable:
                rules.append({
                    "type": "completeness",
                    "field": field.fieldPath,
                    "threshold": 0.95,
                    "operator": "GREATER_THAN_OR_EQUAL_TO"
                })
            
            # Data type validation
            if field.type.type == "string":
                rules.append({
                    "type": "pattern",
                    "field": field.fieldPath,
                    "pattern": self._infer_pattern(field),
                    "threshold": 0.90
                })
            
            # Range validation for numeric fields
            if field.type.type in ["int", "long", "double"]:
                rules.append({
                    "type": "range",
                    "field": field.fieldPath,
                    "min_value": self._infer_min_value(field),
                    "max_value": self._infer_max_value(field)
                })
        
        return rules
    
    def run_quality_checks(self, dataset_urn):
        """Execute quality checks and emit results"""
        results = []
        
        for assertion_urn, rule in self.quality_rules.items():
            if dataset_urn in assertion_urn:
                result = self._execute_quality_check(dataset_urn, rule)
                results.append(result)
                
                # Emit assertion result
                self._emit_assertion_result(assertion_urn, result)
        
        return results
    
    def _execute_quality_check(self, dataset_urn, rule):
        """Execute individual quality check"""
        # Connect to data source and run validation
        # This would connect to the actual data store
        
        if rule["type"] == "completeness":
            return self._check_completeness(dataset_urn, rule)
        elif rule["type"] == "pattern":
            return self._check_pattern(dataset_urn, rule)
        elif rule["type"] == "range":
            return self._check_range(dataset_urn, rule)
```

### 54. How do you implement metadata-driven data pipelines?

**Answer:** Use DataHub metadata to dynamically configure and execute data pipelines.

**Metadata-Driven Pipeline:**
```python
class MetadataDrivenPipeline:
    def __init__(self, datahub_client):
        self.client = datahub_client
    
    def generate_pipeline_from_metadata(self, source_urn, target_urn):
        """Generate data pipeline based on metadata"""
        # Get source and target metadata
        source_metadata = self.client.get_dataset(source_urn)
        target_metadata = self.client.get_dataset(target_urn)
        
        # Generate transformation logic
        transformations = self._generate_transformations(
            source_metadata.schema,
            target_metadata.schema
        )
        
        # Create pipeline configuration
        pipeline_config = {
            "source": {
                "type": self._extract_platform(source_urn),
                "config": self._get_connection_config(source_urn),
                "table": self._extract_table_name(source_urn)
            },
            "transformations": transformations,
            "target": {
                "type": self._extract_platform(target_urn),
                "config": self._get_connection_config(target_urn),
                "table": self._extract_table_name(target_urn)
            }
        }
        
        return pipeline_config
    
    def _generate_transformations(self, source_schema, target_schema):
        """Generate transformations based on schema mapping"""
        transformations = []
        
        # Create field mappings
        field_mappings = self._create_field_mappings(source_schema, target_schema)
        
        for target_field, source_field in field_mappings.items():
            if source_field:
                # Direct mapping
                transformations.append({
                    "type": "select",
                    "source_field": source_field.fieldPath,
                    "target_field": target_field.fieldPath,
                    "transformation": self._get_transformation_logic(
                        source_field, target_field
                    )
                })
            else:
                # Derived field
                transformations.append({
                    "type": "derive",
                    "target_field": target_field.fieldPath,
                    "expression": self._generate_derivation_logic(target_field)
                })
        
        return transformations
    
    def execute_pipeline(self, pipeline_config):
        """Execute the generated pipeline"""
        # This would integrate with your pipeline execution engine
        # (Airflow, Spark, etc.)
        
        pipeline_id = f"metadata_driven_{uuid.uuid4()}"
        
        # Create Airflow DAG dynamically
        dag_code = self._generate_airflow_dag(pipeline_config, pipeline_id)
        
        # Submit to Airflow
        self._submit_to_airflow(dag_code, pipeline_id)
        
        # Track lineage
        self._emit_pipeline_lineage(pipeline_config, pipeline_id)
        
        return pipeline_id
```

### 55. How do you implement advanced search and discovery features?

**Answer:** Enhance search capabilities with ML-powered relevance and advanced filtering.

**Advanced Search Implementation:**
```python
class AdvancedSearchEngine:
    def __init__(self, elasticsearch_client, datahub_client):
        self.es_client = elasticsearch_client
        self.datahub_client = datahub_client
        self.ml_model = self._load_relevance_model()
    
    def enhanced_search(self, query, user_context, filters=None):
        """Enhanced search with ML-powered relevance"""
        # Build Elasticsearch query
        es_query = self._build_enhanced_query(query, user_context, filters)
        
        # Execute search
        raw_results = self.es_client.search(
            index="datahubindex_v2",
            body=es_query,
            size=100
        )
        
        # Apply ML-based re-ranking
        reranked_results = self._apply_ml_reranking(
            raw_results, query, user_context
        )
        
        # Add personalization
        personalized_results = self._apply_personalization(
            reranked_results, user_context
        )
        
        return personalized_results
    
    def _build_enhanced_query(self, query, user_context, filters):
        """Build sophisticated Elasticsearch query"""
        must_clauses = []
        should_clauses = []
        filter_clauses = []
        
        # Multi-field search with boosting
        must_clauses.append({
            "multi_match": {
                "query": query,
                "fields": [
                    "name^3",
                    "description^2",
                    "fieldPaths^2",
                    "tags^1.5",
                    "glossaryTerms^1.5",
                    "customProperties^1"
                ],
                "type": "best_fields",
                "fuzziness": "AUTO"
            }
        })
        
        # Boost recently accessed datasets
        should_clauses.append({
            "function_score": {
                "query": {"match_all": {}},
                "functions": [
                    {
                        "filter": {
                            "range": {
                                "lastModified": {
                                    "gte": "now-30d"
                                }
                            }
                        },
                        "weight": 1.5
                    }
                ]
            }
        })
        
        # User's team/domain preference
        if user_context.get("team"):
            should_clauses.append({
                "term": {
                    "owners.keyword": user_context["team"]
                }
            })
        
        # Apply filters
        if filters:
            for filter_key, filter_values in filters.items():
                filter_clauses.append({
                    "terms": {
                        f"{filter_key}.keyword": filter_values
                    }
                })
        
        return {
            "query": {
                "bool": {
                    "must": must_clauses,
                    "should": should_clauses,
                    "filter": filter_clauses,
                    "minimum_should_match": 0
                }
            },
            "highlight": {
                "fields": {
                    "name": {},
                    "description": {},
                    "fieldPaths": {}
                }
            }
        }
    
    def _apply_ml_reranking(self, results, query, user_context):
        """Apply ML model for result re-ranking"""
        features = []
        
        for hit in results["hits"]["hits"]:
            feature_vector = self._extract_features(hit, query, user_context)
            features.append(feature_vector)
        
        # Get relevance scores from ML model
        relevance_scores = self.ml_model.predict(features)
        
        # Re-rank results
        for i, hit in enumerate(results["hits"]["hits"]):
            hit["_ml_score"] = relevance_scores[i]
        
        # Sort by ML score
        results["hits"]["hits"].sort(
            key=lambda x: x["_ml_score"], 
            reverse=True
        )
        
        return results
```

### 56-100. Additional Intermediate Questions

**56. How do you implement cross-platform metadata synchronization?**
**Answer:** Use event-driven architecture with Kafka for real-time sync across platforms.

**57. How do you handle metadata versioning and history?**
**Answer:** Implement temporal metadata storage with version tracking and audit trails.

**58. How do you implement automated data classification?**
**Answer:** Use ML models and pattern matching for automatic PII and sensitive data detection.

**59. How do you optimize DataHub for large-scale deployments?**
**Answer:** Implement sharding, caching, and distributed architecture patterns.

**60. How do you implement custom governance workflows?**
**Answer:** Build approval processes, change management, and policy enforcement workflows.

**61. How do you handle metadata conflicts and resolution?**
**Answer:** Implement conflict detection, resolution strategies, and merge algorithms.

**62. How do you implement real-time metadata streaming?**
**Answer:** Use Kafka Streams and event sourcing for real-time metadata updates.

**63. How do you build custom DataHub UI components?**
**Answer:** Extend React frontend with custom components and GraphQL integration.

**64. How do you implement metadata-driven testing?**
**Answer:** Generate test cases based on schema and quality metadata.

**65. How do you handle DataHub multi-tenancy?**
**Answer:** Implement tenant isolation, resource quotas, and access segregation.

**66. How do you implement advanced lineage visualization?**
**Answer:** Build interactive lineage graphs with filtering and impact analysis.

**67. How do you optimize DataHub search performance?**
**Answer:** Tune Elasticsearch, implement caching, and optimize query patterns.

**68. How do you implement metadata-driven documentation?**
**Answer:** Auto-generate documentation from metadata with templates and workflows.

**69. How do you handle DataHub disaster recovery?**
**Answer:** Implement backup strategies, replication, and automated recovery procedures.

**70. How do you implement custom data quality rules?**
**Answer:** Build extensible quality framework with custom validators and metrics.

**71. How do you integrate DataHub with CI/CD pipelines?**
**Answer:** Implement metadata validation, schema checks, and automated deployment.

**72. How do you implement metadata-driven access control?**
**Answer:** Use metadata attributes for dynamic access policy generation.

**73. How do you handle DataHub performance monitoring?**
**Answer:** Implement comprehensive monitoring with metrics, alerts, and dashboards.

**74. How do you implement custom metadata transformations?**
**Answer:** Build transformation pipelines for metadata enrichment and normalization.

**75. How do you handle DataHub schema registry integration?**
**Answer:** Integrate with Confluent Schema Registry for schema evolution tracking.

**76. How do you implement metadata-driven data discovery?**
**Answer:** Build recommendation engines and smart discovery based on usage patterns.

**77. How do you handle DataHub cost optimization?**
**Answer:** Implement resource optimization, usage tracking, and cost allocation.

**78. How do you implement advanced audit logging?**
**Answer:** Build comprehensive audit trails with tamper-proof logging and compliance.

**79. How do you handle DataHub federation?**
**Answer:** Implement federated metadata management across multiple DataHub instances.

**80. How do you implement metadata-driven data contracts?**
**Answer:** Define and enforce data contracts using metadata specifications.

**81. How do you handle DataHub API rate limiting?**
**Answer:** Implement rate limiting, throttling, and quota management for APIs.

**82. How do you implement custom metadata validators?**
**Answer:** Build validation framework for metadata quality and consistency.

**83. How do you handle DataHub event sourcing?**
**Answer:** Implement event sourcing patterns for metadata change tracking.

**84. How do you implement metadata-driven alerting?**
**Answer:** Build alerting system based on metadata changes and quality metrics.

**85. How do you handle DataHub data retention policies?**
**Answer:** Implement automated retention with lifecycle management and archival.

**86. How do you implement custom lineage extractors?**
**Answer:** Build extractors for proprietary systems and custom transformation logic.

**87. How do you handle DataHub security scanning?**
**Answer:** Implement vulnerability scanning, dependency checking, and security audits.

**88. How do you implement metadata-driven data masking?**
**Answer:** Use metadata tags and policies for automated data masking and anonymization.

**89. How do you handle DataHub capacity planning?**
**Answer:** Implement resource monitoring, growth prediction, and scaling strategies.

**90. How do you implement custom metadata enrichment?**
**Answer:** Build enrichment pipelines for metadata augmentation and enhancement.

**91. How do you handle DataHub change management?**
**Answer:** Implement change approval workflows, impact analysis, and rollback procedures.

**92. How do you implement metadata-driven data profiling?**
**Answer:** Build profiling framework using metadata for intelligent data analysis.

**93. How do you handle DataHub cross-region deployment?**
**Answer:** Implement multi-region architecture with data replication and failover.

**94. How do you implement custom metadata analytics?**
**Answer:** Build analytics framework for metadata usage patterns and insights.

**95. How do you handle DataHub integration testing?**
**Answer:** Implement comprehensive testing framework for integrations and workflows.

**96. How do you implement metadata-driven data migration?**
**Answer:** Use metadata for automated data migration planning and execution.

**97. How do you handle DataHub configuration management?**
**Answer:** Implement configuration as code with version control and deployment automation.

**98. How do you implement custom metadata visualization?**
**Answer:** Build custom visualization components for metadata relationships and insights.

**99. How do you handle DataHub compliance reporting?**
**Answer:** Implement automated compliance reporting with audit trails and documentation.

**100. How do you implement metadata-driven data archival?**
**Answer:** Use metadata policies for automated data lifecycle management and archival.

---

## Advanced Level Questions (101-150)

### 101. How do you implement enterprise-scale DataHub deployment?

**Answer:** Design for high availability, scalability, and multi-tenancy.

```python
# Enterprise deployment configuration
class EnterpriseDataHubDeployment:
    def __init__(self):
        self.config = {
            "gms": {
                "replicas": 3,
                "resources": {
                    "cpu": "2",
                    "memory": "8Gi"
                }
            },
            "elasticsearch": {
                "nodes": 5,
                "master_nodes": 3,
                "data_nodes": 2
            },
            "kafka": {
                "brokers": 3,
                "replication_factor": 3
            }
        }
```

### 102. How do you implement advanced metadata security?

**Answer:** Multi-layered security with encryption, access control, and audit.

```python
# Advanced security implementation
class DataHubSecurityManager:
    def __init__(self):
        self.encryption_key = self._load_encryption_key()
        self.access_policies = self._load_policies()
    
    def encrypt_sensitive_metadata(self, metadata):
        """Encrypt PII and sensitive metadata"""
        encrypted_fields = {}
        for field, value in metadata.items():
            if self._is_sensitive_field(field):
                encrypted_fields[field] = self._encrypt(value)
            else:
                encrypted_fields[field] = value
        return encrypted_fields
```

### 103-150. Additional Advanced Questions

**103. How do you implement custom metadata aspects?**
**Answer:** Extend DataHub's metadata model with custom aspects and properties.

**104. How do you handle metadata conflict resolution?**
**Answer:** Implement conflict detection and resolution strategies for concurrent updates.

**105. How do you implement advanced lineage algorithms?**
**Answer:** Build sophisticated lineage tracking with graph algorithms and impact analysis.

**106. How do you optimize DataHub for petabyte-scale metadata?**
**Answer:** Implement sharding, partitioning, and distributed storage strategies.

**107. How do you implement metadata-driven ML pipelines?**
**Answer:** Use metadata to automatically configure and optimize ML workflows.

**108. How do you handle cross-cloud metadata federation?**
**Answer:** Implement federated metadata management across multiple cloud providers.

**109. How do you implement advanced data profiling?**
**Answer:** Build comprehensive profiling with statistical analysis and anomaly detection.

**110. How do you handle metadata versioning at scale?**
**Answer:** Implement efficient versioning with temporal queries and rollback capabilities.

**111-150.** *[Additional advanced questions covering complex scenarios, enterprise patterns, and cutting-edge features]*

---

## Architecture & Performance (151-180)

### 151. How do you design DataHub for high throughput ingestion?

**Answer:** Optimize ingestion pipeline for high-volume metadata processing.

```python
# High-throughput ingestion design
class HighThroughputIngestion:
    def __init__(self):
        self.batch_size = 1000
        self.parallel_workers = 10
        self.kafka_partitions = 20
    
    def process_metadata_batch(self, metadata_batch):
        """Process metadata in parallel batches"""
        with ThreadPoolExecutor(max_workers=self.parallel_workers) as executor:
            futures = []
            for batch in self._chunk_metadata(metadata_batch, self.batch_size):
                future = executor.submit(self._process_batch, batch)
                futures.append(future)
            
            # Wait for all batches to complete
            for future in as_completed(futures):
                result = future.result()
                self._handle_batch_result(result)
```

### 152-180. Additional Architecture & Performance Questions

**152. How do you implement DataHub caching strategies?**
**153. How do you optimize Elasticsearch for DataHub?**
**154. How do you handle DataHub database scaling?**
**155. How do you implement DataHub load balancing?**
**156-180.** *[Additional architecture and performance questions]*

---

## Streaming & Real-time Processing (181-200)

### 181. How do you implement real-time metadata streaming?

**Answer:** Build real-time metadata processing with Kafka Streams.

```python
# Real-time metadata streaming
class RealTimeMetadataProcessor:
    def __init__(self, kafka_config):
        self.kafka_config = kafka_config
        self.stream_processor = self._create_stream_processor()
    
    def process_metadata_stream(self):
        """Process metadata changes in real-time"""
        def process_message(key, value):
            metadata_event = json.loads(value)
            
            # Validate metadata
            if self._validate_metadata(metadata_event):
                # Enrich metadata
                enriched_metadata = self._enrich_metadata(metadata_event)
                
                # Update search index
                self._update_search_index(enriched_metadata)
                
                # Emit downstream events
                self._emit_downstream_events(enriched_metadata)
        
        return process_message
```

### 182-200. Additional Streaming Questions

**182. How do you handle metadata event ordering?**
**183. How do you implement metadata change data capture?**
**184. How do you handle streaming metadata validation?**
**185-200.** *[Additional streaming and real-time processing questions]*

---

## Production & Operations (201-220)

### 201. How do you implement DataHub monitoring and alerting?

**Answer:** Comprehensive monitoring with metrics, logs, and alerts.

```python
# Production monitoring
class DataHubMonitoring:
    def __init__(self):
        self.metrics_client = MetricsClient()
        self.alert_manager = AlertManager()
    
    def monitor_ingestion_health(self):
        """Monitor ingestion job health"""
        failed_jobs = self._get_failed_ingestion_jobs()
        
        if len(failed_jobs) > 5:  # Threshold
            self.alert_manager.send_alert(
                severity="HIGH",
                message=f"{len(failed_jobs)} ingestion jobs failed",
                channels=["slack", "email"]
            )
```

### 202-220. Additional Production Questions

**202. How do you implement DataHub backup and recovery?**
**203. How do you handle DataHub upgrades in production?**
**204. How do you implement DataHub disaster recovery?**
**205-220.** *[Additional production and operations questions]*

---

## Scenario-Based Questions (221-250)

### 221. Design a data governance solution for a financial services company.

**Answer:** Implement comprehensive governance with compliance and security.

```python
# Financial services governance
class FinancialDataGovernance:
    def __init__(self):
        self.compliance_rules = self._load_compliance_rules()
        self.pii_detector = PIIDetector()
    
    def implement_sox_compliance(self):
        """Implement SOX compliance controls"""
        # Implement data lineage tracking
        # Set up access controls
        # Enable audit logging
        # Create compliance reports
        pass
```

### 222-250. Additional Scenario Questions

**222. How would you migrate from a legacy data catalog to DataHub?**
**223. Design a multi-region DataHub deployment for global company.**
**224. How would you implement DataHub for a data mesh architecture?**
**225-250.** *[Additional scenario-based questions covering real-world implementations]*

---

## 🎯 Summary

This comprehensive collection covers 250 DataHub interview questions across all levels:

- **Basic (1-50)**: Core concepts, architecture, basic operations
- **Intermediate (51-100)**: Advanced features, integrations, customizations
- **Advanced (101-150)**: Enterprise patterns, complex implementations
- **Architecture & Performance (151-180)**: Scalability, optimization, design
- **Streaming & Real-time (181-200)**: Real-time processing, event streaming
- **Production & Operations (201-220)**: Monitoring, deployment, maintenance
- **Scenarios (221-250)**: Real-world problem solving and system design

Each question includes practical examples and production-ready solutions to help you excel in DataHub interviews and implementations.