# DataHub - Comprehensive Interview Questions

## Table of Contents
1. [Core Concepts](#core-concepts)
2. [Architecture & Components](#architecture--components)
3. [Metadata Management](#metadata-management)
4. [Data Discovery & Search](#data-discovery--search)
5. [Data Lineage](#data-lineage)
6. [Data Governance](#data-governance)
7. [Integration & APIs](#integration--apis)
8. [Real-World Scenarios](#real-world-scenarios)

---

## Core Concepts

### 1. What is DataHub and how does it solve data discovery challenges?

**Answer:**
DataHub is an open-source metadata platform that enables data discovery, observability, and governance across the modern data stack.

**Key Problems Solved:**
- **Data Discovery**: Find relevant datasets quickly
- **Data Understanding**: Rich metadata and documentation
- **Data Trust**: Quality metrics and lineage tracking
- **Data Governance**: Policies and compliance management
- **Data Collaboration**: Social features for data teams

**DataHub Benefits:**
```python
# Before DataHub
def find_customer_data():
    # Manual search across multiple systems
    # Ask colleagues via Slack
    # Check documentation (if exists)
    # Trial and error with different tables
    pass

# With DataHub
def find_customer_data():
    # Search "customer" in DataHub
    # View metadata, schema, and lineage
    # Check data quality metrics
    # Read documentation and tags
    # Contact dataset owners directly
    return datahub.search("customer", entity_types=["dataset"])
```

### 2. Explain DataHub's metadata model and core entities.

**Answer:**
**Core Entities:**

1. **Datasets**: Tables, files, streams
2. **Data Jobs**: ETL jobs, pipelines
3. **Data Flows**: End-to-end data pipelines
4. **Charts**: Visualizations and dashboards
5. **Dashboards**: Collections of charts
6. **Users**: People who interact with data
7. **Groups**: Teams and organizations

**Metadata Model:**
```json
{
  "dataset": {
    "urn": "urn:li:dataset:(urn:li:dataPlatform:mysql,users,PROD)",
    "properties": {
      "name": "users",
      "description": "User profile information",
      "tags": ["pii", "customer-data"],
      "owner": "data-team@company.com"
    },
    "schema": {
      "fields": [
        {
          "fieldPath": "user_id",
          "type": "int",
          "description": "Unique user identifier"
        },
        {
          "fieldPath": "email",
          "type": "string", 
          "tags": ["pii"]
        }
      ]
    }
  }
}
```

**Entity Relationships:**
```
Dataset → Schema → Fields
   ↓        ↓        ↓
Owners → Tags → Glossary Terms
   ↓        ↓        ↓
Lineage → Quality → Usage Stats
```

### 3. How does DataHub's architecture work?

**Answer:**
**Architecture Components:**

1. **GMS (General Metadata Service)**: Core metadata storage and APIs
2. **MAE (Metadata Audit Event)**: Event stream for metadata changes
3. **MCE (Metadata Change Event)**: Proposals for metadata updates
4. **Frontend**: React-based web interface
5. **Search Index**: Elasticsearch for fast search
6. **Graph Database**: Neo4j for lineage relationships

**Architecture Flow:**
```
Ingestion → Kafka → GMS → Storage (MySQL/PostgreSQL)
    ↓         ↓      ↓         ↓
Connectors → MAE → API → Search Index (Elasticsearch)
                         ↓
                    Frontend (React)
```

**Component Interaction:**
```python
# Metadata ingestion flow
def ingest_metadata():
    # 1. Extract metadata from source
    metadata = extract_from_mysql()
    
    # 2. Create MCE (Metadata Change Event)
    mce = MetadataChangeEvent(
        proposedSnapshot=DatasetSnapshot(
            urn=dataset_urn,
            aspects=[schema_metadata, ownership_info]
        )
    )
    
    # 3. Send to Kafka
    kafka_producer.send('MetadataChangeEvent_v4', mce)
    
    # 4. GMS processes and stores
    # 5. Search index updated
    # 6. Frontend displays updated metadata
```

### 4. What are the different ways to ingest metadata into DataHub?

**Answer:**
**Ingestion Methods:**

1. **CLI Ingestion**: Command-line recipes
2. **UI Ingestion**: Web-based configuration
3. **API Ingestion**: Direct REST API calls
4. **SDK Ingestion**: Python/Java SDKs
5. **Kafka Ingestion**: Direct event streaming

**CLI Recipe Example:**
```yaml
# mysql_recipe.yml
source:
  type: mysql
  config:
    host_port: localhost:3306
    database: ecommerce
    username: datahub
    password: ${MYSQL_PASSWORD}
    include_tables: true
    include_views: true
    profiling:
      enabled: true
      profile_table_level_only: false

sink:
  type: datahub-rest
  config:
    server: http://localhost:8080
```

**Python SDK Ingestion:**
```python
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.rest_emitter import DatahubRestEmitter

# Create emitter
emitter = DatahubRestEmitter(gms_server="http://localhost:8080")

# Create dataset metadata
dataset_properties = DatasetPropertiesClass(
    description="Customer transaction data",
    tags=["finance", "customer-data"]
)

# Emit metadata
mcp = MetadataChangeProposalWrapper(
    entityType="dataset",
    entityUrn=dataset_urn,
    aspectName="datasetProperties",
    aspect=dataset_properties
)

emitter.emit_mcp(mcp)
```

### 5. How do you configure data lineage in DataHub?

**Answer:**
**Lineage Sources:**

1. **Automatic Extraction**: From ETL tools (Airflow, dbt, Spark)
2. **Manual Definition**: Via UI or API
3. **Code Analysis**: Static analysis of SQL/Python code
4. **Runtime Capture**: Dynamic lineage from query logs

**dbt Lineage Integration:**
```yaml
# dbt profile for DataHub
datahub:
  type: datahub-rest
  config:
    server: http://localhost:8080
    token: ${DATAHUB_TOKEN}
    
# dbt model with lineage
{{ config(
    materialized='table',
    meta={
        'datahub': {
            'tags': ['analytics', 'customer-metrics']
        }
    }
) }}

SELECT 
    customer_id,
    SUM(order_amount) as total_spent
FROM {{ ref('orders') }}  -- Automatic lineage to orders table
GROUP BY customer_id
```

**Manual Lineage Definition:**
```python
# Define lineage via API
def create_lineage():
    upstream_urns = [
        "urn:li:dataset:(urn:li:dataPlatform:mysql,orders,PROD)",
        "urn:li:dataset:(urn:li:dataPlatform:mysql,customers,PROD)"
    ]
    
    downstream_urn = "urn:li:dataset:(urn:li:dataPlatform:snowflake,customer_metrics,PROD)"
    
    lineage = UpstreamLineage(
        upstreams=[
            Upstream(
                dataset=upstream_urn,
                type=DatasetLineageType.TRANSFORMED
            ) for upstream_urn in upstream_urns
        ]
    )
    
    # Emit lineage
    emit_lineage(downstream_urn, lineage)
```

### 6. How do you implement data governance policies in DataHub?

**Answer:**
**Governance Features:**

1. **Data Classification**: Tag sensitive data
2. **Access Policies**: Control who can access what
3. **Data Quality**: Monitor and alert on quality issues
4. **Compliance**: Track regulatory requirements
5. **Ownership**: Assign data stewards

**Data Classification:**
```python
# Tag PII data
def classify_pii_data():
    pii_fields = [
        "email", "phone", "ssn", "credit_card",
        "first_name", "last_name", "address"
    ]
    
    for field in pii_fields:
        add_tag_to_field(
            dataset_urn=dataset_urn,
            field_path=field,
            tag_urn="urn:li:tag:PII"
        )
```

**Access Policies:**
```json
{
  "policy": {
    "type": "METADATA",
    "name": "PII Data Access Policy",
    "description": "Restrict access to PII data",
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
          "users": ["urn:li:corpuser:data-steward"],
          "groups": ["urn:li:corpGroup:privacy-team"]
        }
      }
    ]
  }
}
```

**Data Quality Monitoring:**
```python
# Define data quality assertions
def setup_data_quality():
    assertions = [
        {
            "type": "freshness",
            "dataset": customer_dataset_urn,
            "schedule": "0 */6 * * *",  # Every 6 hours
            "threshold": "24 hours"
        },
        {
            "type": "volume",
            "dataset": orders_dataset_urn,
            "schedule": "0 9 * * *",  # Daily at 9 AM
            "threshold": {
                "min": 1000,
                "max": 100000
            }
        }
    ]
    
    for assertion in assertions:
        create_assertion(assertion)
```

### 7. How do you search and discover data in DataHub?

**Answer:**
**Search Capabilities:**

1. **Full-text Search**: Search across all metadata
2. **Faceted Search**: Filter by entity type, platform, tags
3. **Advanced Filters**: Complex search criteria
4. **Saved Searches**: Bookmark common searches
5. **Recommendations**: ML-powered suggestions

**Search Examples:**
```python
# Basic search
results = datahub.search(
    query="customer",
    entity_types=["dataset"],
    start=0,
    count=10
)

# Advanced search with filters
results = datahub.search(
    query="revenue",
    entity_types=["dataset", "chart"],
    filters=[
        {
            "field": "platform",
            "values": ["snowflake", "bigquery"]
        },
        {
            "field": "tags",
            "values": ["finance", "analytics"]
        }
    ]
)

# Search by schema
schema_results = datahub.search_by_schema(
    field_name="customer_id",
    field_type="bigint"
)
```

**Search Configuration:**
```yaml
# Elasticsearch configuration for search
search:
  elasticsearch:
    host: elasticsearch:9200
    index_prefix: datahub
    settings:
      analysis:
        analyzer:
          default:
            type: standard
            stopwords: _english_
        normalizer:
          lowercase_normalizer:
            type: custom
            filter: [lowercase]
```

### 8. How do you monitor DataHub performance and health?

**Answer:**
**Monitoring Areas:**

1. **System Health**: Service availability and performance
2. **Ingestion Health**: Metadata ingestion success rates
3. **Search Performance**: Query response times
4. **User Activity**: Usage patterns and adoption
5. **Data Quality**: Assertion pass/fail rates

**Health Monitoring:**
```python
def monitor_datahub_health():
    health_checks = {
        'gms_health': check_gms_health(),
        'kafka_health': check_kafka_health(),
        'elasticsearch_health': check_elasticsearch_health(),
        'mysql_health': check_mysql_health(),
        'frontend_health': check_frontend_health()
    }
    
    for service, status in health_checks.items():
        if not status.healthy:
            send_alert(f"{service} is unhealthy: {status.message}")
    
    return health_checks

def check_gms_health():
    try:
        response = requests.get(f"{GMS_URL}/health")
        return HealthStatus(
            healthy=response.status_code == 200,
            message=response.text
        )
    except Exception as e:
        return HealthStatus(healthy=False, message=str(e))
```

**Performance Metrics:**
```python
# Key metrics to monitor
metrics = {
    'ingestion_metrics': {
        'recipes_run': 'Number of ingestion recipes executed',
        'entities_ingested': 'Total entities processed',
        'ingestion_errors': 'Failed ingestion attempts',
        'ingestion_duration': 'Time taken for ingestion'
    },
    'search_metrics': {
        'search_queries': 'Number of search requests',
        'search_latency': 'Average search response time',
        'search_success_rate': 'Percentage of successful searches'
    },
    'user_metrics': {
        'active_users': 'Daily/monthly active users',
        'page_views': 'Frontend page views',
        'api_calls': 'API request volume'
    }
}
```

### 9. How do you integrate DataHub with existing data tools?

**Answer:**
**Integration Patterns:**

1. **Metadata Ingestion**: Extract metadata from tools
2. **Lineage Integration**: Capture data flow information
3. **Quality Integration**: Import data quality metrics
4. **Notification Integration**: Send alerts to external systems
5. **Authentication Integration**: SSO and RBAC

**Airflow Integration:**
```python
# Airflow DAG with DataHub lineage
from datahub_airflow_plugin.entities import Dataset, Task

dag = DAG('customer_pipeline')

# Define datasets
source_dataset = Dataset(
    platform="mysql",
    name="customers",
    env="PROD"
)

target_dataset = Dataset(
    platform="snowflake", 
    name="customer_metrics",
    env="PROD"
)

# Task with lineage
@task(inlets=[source_dataset], outlets=[target_dataset])
def transform_customer_data():
    # ETL logic here
    pass
```

**dbt Integration:**
```yaml
# dbt_project.yml with DataHub
vars:
  datahub:
    server: http://localhost:8080
    token: ${DATAHUB_TOKEN}

models:
  my_project:
    +meta:
      datahub:
        tags: ['analytics']
        owners: ['data-team@company.com']
```

**Slack Integration:**
```python
# Send DataHub notifications to Slack
def setup_slack_notifications():
    webhook_config = {
        'type': 'slack',
        'webhook_url': os.getenv('SLACK_WEBHOOK_URL'),
        'events': [
            'ENTITY_CHANGE_EVENT',
            'DATA_QUALITY_ASSERTION_FAILURE'
        ]
    }
    
    datahub.configure_webhook(webhook_config)
```

### 10. Design a complete data governance solution using DataHub for a financial services company.

**Answer:**
**Architecture:**
```
Data Sources → DataHub → Governance Layer → Compliance Reporting
     ↓            ↓            ↓                    ↓
Databases → Metadata → Policies → Audit Reports
APIs      → Lineage  → Controls → Risk Assessment
Files     → Quality  → Monitoring → Regulatory Compliance
```

**Implementation:**
```python
# Complete governance setup
def setup_financial_governance():
    # 1. Data Classification
    setup_data_classification()
    
    # 2. Access Controls
    setup_access_policies()
    
    # 3. Data Quality Monitoring
    setup_quality_monitoring()
    
    # 4. Compliance Tracking
    setup_compliance_monitoring()
    
    # 5. Audit Logging
    setup_audit_logging()

def setup_data_classification():
    # Classify sensitive financial data
    classifications = {
        'PII': ['customer_id', 'ssn', 'email', 'phone'],
        'PCI': ['credit_card', 'account_number'],
        'CONFIDENTIAL': ['salary', 'credit_score', 'transaction_amount'],
        'PUBLIC': ['product_name', 'branch_location']
    }
    
    for classification, fields in classifications.items():
        for field in fields:
            apply_classification(field, classification)

def setup_access_policies():
    # Role-based access control
    policies = [
        {
            'name': 'PII Access Policy',
            'resources': {'tags': ['PII']},
            'privileges': ['VIEW_DATASET_PROFILE'],
            'actors': ['privacy-officers', 'compliance-team']
        },
        {
            'name': 'Financial Data Policy',
            'resources': {'platforms': ['trading-db', 'risk-warehouse']},
            'privileges': ['VIEW_DATASET_USAGE'],
            'actors': ['risk-analysts', 'traders']
        }
    ]
    
    for policy in policies:
        create_access_policy(policy)

def setup_quality_monitoring():
    # Financial data quality rules
    quality_rules = [
        {
            'dataset': 'trading_transactions',
            'rules': [
                {'type': 'not_null', 'column': 'transaction_id'},
                {'type': 'positive', 'column': 'amount'},
                {'type': 'freshness', 'threshold': '15 minutes'}
            ]
        },
        {
            'dataset': 'customer_accounts',
            'rules': [
                {'type': 'unique', 'column': 'account_number'},
                {'type': 'format', 'column': 'ssn', 'pattern': r'^\d{3}-\d{2}-\d{4}$'}
            ]
        }
    ]
    
    for rule_set in quality_rules:
        setup_quality_assertions(rule_set)

def setup_compliance_monitoring():
    # Regulatory compliance tracking
    compliance_requirements = {
        'SOX': {
            'datasets': ['financial_statements', 'audit_trail'],
            'controls': ['access_logging', 'change_tracking']
        },
        'GDPR': {
            'datasets': ['customer_pii', 'marketing_data'],
            'controls': ['data_retention', 'consent_tracking']
        },
        'PCI_DSS': {
            'datasets': ['payment_data', 'card_transactions'],
            'controls': ['encryption', 'access_restriction']
        }
    }
    
    for regulation, requirements in compliance_requirements.items():
        setup_compliance_controls(regulation, requirements)
```

**Monitoring Dashboard:**
```python
def create_governance_dashboard():
    dashboard_metrics = {
        'data_coverage': calculate_metadata_coverage(),
        'policy_compliance': check_policy_compliance(),
        'quality_score': calculate_data_quality_score(),
        'lineage_completeness': measure_lineage_coverage(),
        'user_adoption': track_user_engagement()
    }
    
    # Generate compliance reports
    generate_compliance_report(dashboard_metrics)
    
    return dashboard_metrics
```

This comprehensive set of DataHub interview questions covers all essential aspects of metadata management, data discovery, and governance, providing practical examples for implementing a complete data governance solution.