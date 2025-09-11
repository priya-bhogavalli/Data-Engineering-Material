# DataHub Key Concepts for Data Engineering

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Core Components](#-core-components)
   - [Metadata Model](#metadata-model)
   - [GMS (General Metadata Service)](#gms-general-metadata-service)
   - [Frontend](#frontend)
   - [Search & Discovery](#search--discovery)
3. [Architecture](#-architecture)
4. [Key Features](#-key-features)
   - [Data Discovery](#data-discovery)
   - [Data Lineage](#data-lineage)
   - [Data Governance](#data-governance)
   - [Data Quality](#data-quality)
5. [Metadata Ingestion](#-metadata-ingestion)
6. [Integration Patterns](#-integration-patterns)
7. [Best Practices](#-best-practices)
8. [Limitations](#-limitations)
9. [Version Highlights](#-version-highlights)
10. [Use Cases](#-use-cases)
11. [When to Use DataHub](#-when-to-use-datahub)
12. [Quick References](#-quick-references)

---

## 🎯 Overview

DataHub is an open-source metadata platform that enables data discovery, observability, and governance across the modern data stack. It provides a unified view of your organization's data assets, making it easier for data teams to find, understand, and trust their data.

**Key Benefits:**
- **Unified Data Discovery**: Single pane of glass for all data assets
- **Rich Metadata Management**: Comprehensive metadata capture and enrichment
- **Data Lineage Tracking**: End-to-end data flow visualization
- **Governance & Compliance**: Policy enforcement and audit capabilities
- **Collaboration**: Social features for data teams

## 📦 Core Components

### Metadata Model

**Definition**: DataHub's metadata model is built around entities and aspects, providing a flexible and extensible way to represent data assets.

**Core Entities:**
- **Datasets**: Tables, files, streams, and other data containers
- **Data Jobs**: ETL jobs, pipelines, and data processing tasks
- **Data Flows**: End-to-end data pipelines and workflows
- **Charts**: Visualizations and analytical charts
- **Dashboards**: Collections of charts and metrics
- **Users**: People who interact with data
- **Groups**: Teams and organizational units
- **Tags**: Labels for categorization and discovery
- **Glossary Terms**: Business definitions and vocabulary

**Entity Relationships:**
```
Dataset → Schema → Fields
   ↓        ↓        ↓
Owners → Tags → Glossary Terms
   ↓        ↓        ↓
Lineage → Quality → Usage Stats
```

**Metadata Aspects:**
```json
{
  "dataset": {
    "urn": "urn:li:dataset:(urn:li:dataPlatform:mysql,users,PROD)",
    "aspects": {
      "datasetProperties": {
        "name": "users",
        "description": "User profile information",
        "tags": ["pii", "customer-data"]
      },
      "schemaMetadata": {
        "fields": [
          {
            "fieldPath": "user_id",
            "type": "int",
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
}
```

### GMS (General Metadata Service)

**Definition**: The core service that stores and serves metadata, providing REST APIs for metadata operations.

**Key Responsibilities:**
- **Metadata Storage**: Persistent storage of all metadata
- **API Gateway**: REST and GraphQL APIs for metadata access
- **Event Processing**: Handles metadata change events
- **Search Indexing**: Maintains search indices for fast discovery
- **Authentication**: User authentication and authorization

**API Examples:**
```python
# Python SDK example
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
    entityUrn="urn:li:dataset:(urn:li:dataPlatform:snowflake,transactions,PROD)",
    aspectName="datasetProperties",
    aspect=dataset_properties
)

emitter.emit_mcp(mcp)
```

### Frontend

**Definition**: React-based web application providing the user interface for data discovery and governance.

**Key Features:**
- **Search Interface**: Powerful search with filters and facets
- **Entity Pages**: Detailed views of datasets, jobs, and other entities
- **Lineage Visualization**: Interactive data lineage graphs
- **Governance Tools**: Policy management and compliance dashboards
- **Social Features**: Comments, documentation, and collaboration

### Search & Discovery

**Definition**: Elasticsearch-powered search engine enabling fast and relevant data discovery.

**Search Capabilities:**
- **Full-text Search**: Search across all metadata fields
- **Faceted Search**: Filter by entity type, platform, tags, etc.
- **Relevance Ranking**: ML-powered relevance scoring
- **Auto-complete**: Smart suggestions and type-ahead
- **Saved Searches**: Bookmark and share search queries

## 🏗️ Architecture

**High-Level Architecture:**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                DATAHUB ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐             │
│  │   DATA SOURCES  │    │   INGESTION     │    │   DATAHUB CORE  │             │
│  │                 │    │                 │    │                 │             │
│  │ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │             │
│  │ │   MySQL     │ │───►│ │ CLI Recipes │ │───►│ │     GMS     │ │             │
│  │ │ PostgreSQL  │ │    │ │ Python SDK  │ │    │ │  (Backend)  │ │             │
│  │ │ Snowflake   │ │    │ │ REST API    │ │    │ │             │ │             │
│  │ │ BigQuery    │ │    │ │ Kafka       │ │    │ │ ┌─────────┐ │ │             │
│  │ │ Airflow     │ │    │ └─────────────┘ │    │ │ │ MySQL/  │ │ │             │
│  │ │ dbt         │ │    │                 │    │ │ │Postgres │ │ │             │
│  │ │ Tableau     │ │    │                 │    │ │ └─────────┘ │ │             │
│  │ └─────────────┘ │    │                 │    │ └─────────────┘ │             │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘             │
│                                                          │                      │
│                                                          ▼                      │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           SERVING LAYER                                     │ │
│  │                                                                             │ │
│  │ ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │ │
│  │ │   FRONTEND      │  │ ELASTICSEARCH   │  │   KAFKA         │             │ │
│  │ │                 │  │                 │  │                 │             │ │
│  │ │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │             │ │
│  │ │ │ React UI    │ │  │ │Search Index │ │  │ │ MAE Stream  │ │             │ │
│  │ │ │ GraphQL API │ │  │ │Faceted      │ │  │ │ MCE Stream  │ │             │ │
│  │ │ │ Discovery   │ │  │ │Search       │ │  │ │ Events      │ │             │ │
│  │ │ │ Lineage     │ │  │ │Auto-complete│ │  │ └─────────────┘ │             │ │
│  │ │ │ Governance  │ │  │ └─────────────┘ │  └─────────────────┘             │ │
│  │ │ └─────────────┘ │  └─────────────────┘                                  │ │
│  │ └─────────────────┘                                                        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘

                                DATA FLOW
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  1. Data Sources generate metadata (schema, lineage, usage)                    │
│  2. Ingestion layer extracts and transforms metadata                           │
│  3. Metadata Change Events (MCE) sent to Kafka                                 │
│  4. GMS processes events and stores in database                                │
│  5. Search index updated for fast discovery                                    │
│  6. Frontend serves metadata to users                                          │
│  7. Metadata Audit Events (MAE) track all changes                              │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Component Interaction:**
- **Ingestion → Kafka → GMS**: Metadata flows through event streams
- **GMS → Elasticsearch**: Search indices updated automatically
- **Frontend → GMS**: UI queries metadata via GraphQL/REST
- **MAE Stream**: Audit trail of all metadata changes

## 🔧 Key Features

### Data Discovery

**Definition**: Comprehensive search and discovery capabilities across all data assets.

**Core Capabilities:**
- **Universal Search**: Search across datasets, jobs, dashboards, and users
- **Smart Filters**: Filter by platform, environment, tags, and ownership
- **Relevance Ranking**: ML-powered search result ranking
- **Browse by Category**: Navigate data assets by domain or platform

**Search Examples:**
```python
# Search for customer data
search_results = datahub_client.search(
    entity_types=["dataset"],
    query="customer",
    filters={
        "platform": ["snowflake", "bigquery"],
        "tags": ["pii"]
    }
)

# Browse datasets by platform
datasets = datahub_client.browse(
    entity_type="dataset",
    path="/prod/snowflake/analytics"
)
```

### Data Lineage

**Definition**: End-to-end tracking of data flow from source to consumption.

**Lineage Types:**
- **Dataset Lineage**: Table-to-table relationships
- **Column Lineage**: Field-level transformations
- **Job Lineage**: ETL job dependencies
- **Dashboard Lineage**: Report data sources

**Lineage Sources:**
- **Automatic Extraction**: From ETL tools (Airflow, dbt, Spark)
- **Manual Definition**: Via UI or API
- **Code Analysis**: Static analysis of SQL/Python code
- **Runtime Capture**: Dynamic lineage from query logs

**Lineage Example:**
```python
# Define lineage programmatically
from datahub.metadata.schema_classes import UpstreamLineage, Upstream

upstream_urns = [
    "urn:li:dataset:(urn:li:dataPlatform:mysql,orders,PROD)",
    "urn:li:dataset:(urn:li:dataPlatform:mysql,customers,PROD)"
]

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

### Data Governance

**Definition**: Policy enforcement, access control, and compliance management.

**Governance Features:**
- **Data Classification**: Automatic and manual data tagging
- **Access Policies**: Fine-grained access control
- **Data Quality**: Monitoring and alerting on quality issues
- **Compliance**: Regulatory compliance tracking
- **Ownership**: Data stewardship and responsibility

**Policy Example:**
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

### Data Quality

**Definition**: Monitoring and validation of data quality across the organization.

**Quality Dimensions:**
- **Completeness**: Missing or null values
- **Accuracy**: Data correctness and validity
- **Consistency**: Data uniformity across systems
- **Timeliness**: Data freshness and currency
- **Uniqueness**: Duplicate detection and handling

**Quality Monitoring:**
```python
# Define data quality assertions
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

## 📥 Metadata Ingestion

**Definition**: Process of extracting metadata from various data sources and loading it into DataHub.

**Ingestion Methods:**

### 1. CLI Ingestion
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

### 2. Python SDK Ingestion
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

### 3. Kafka Ingestion
```python
# Stream metadata changes via Kafka
from datahub.emitter.kafka_emitter import DatahubKafkaEmitter

kafka_emitter = DatahubKafkaEmitter(
    config={
        'bootstrap.servers': 'localhost:9092',
        'schema.registry.url': 'http://localhost:8081'
    }
)

kafka_emitter.emit_mcp(mcp)
```

## 🔗 Integration Patterns

**Supported Integrations:**

### Data Platforms
- **Databases**: MySQL, PostgreSQL, Oracle, SQL Server, MongoDB
- **Data Warehouses**: Snowflake, BigQuery, Redshift, Databricks
- **Data Lakes**: S3, HDFS, Azure Data Lake, Google Cloud Storage
- **Streaming**: Kafka, Pulsar, Kinesis

### ETL/ELT Tools
- **Orchestration**: Apache Airflow, Prefect, Dagster
- **Transformation**: dbt, Apache Spark, Databricks
- **Integration**: Fivetran, Stitch, Airbyte

### BI/Analytics Tools
- **Visualization**: Tableau, Power BI, Looker, Superset
- **Notebooks**: Jupyter, Databricks Notebooks, Hex

### Data Quality Tools
- **Profiling**: Great Expectations, Deequ, Monte Carlo
- **Monitoring**: Datadog, New Relic, custom solutions

## 💡 Best Practices

### 1. Metadata Management
- **Consistent Naming**: Use standardized naming conventions
- **Rich Descriptions**: Provide comprehensive documentation
- **Tag Strategy**: Implement consistent tagging taxonomy
- **Ownership Assignment**: Assign clear data ownership

### 2. Ingestion Strategy
- **Incremental Updates**: Use incremental ingestion for large datasets
- **Scheduling**: Set appropriate ingestion frequencies
- **Error Handling**: Implement robust error handling and retry logic
- **Monitoring**: Monitor ingestion jobs and data quality

### 3. Governance Implementation
- **Policy Definition**: Define clear data governance policies
- **Access Control**: Implement role-based access control
- **Compliance Tracking**: Monitor regulatory compliance
- **Audit Logging**: Maintain comprehensive audit trails

### 4. Performance Optimization
- **Search Tuning**: Optimize Elasticsearch configuration
- **Caching**: Implement appropriate caching strategies
- **Resource Allocation**: Right-size infrastructure components
- **Monitoring**: Monitor system performance and usage

## ⚠️ Limitations

### Technical Limitations
- **Scale Limits**: Performance degrades with very large metadata volumes
- **Real-time Updates**: Some metadata updates may have latency
- **Complex Lineage**: Challenging to capture complex transformation logic
- **Resource Requirements**: Requires significant infrastructure resources

### Functional Limitations
- **Data Profiling**: Limited built-in data profiling capabilities
- **Custom Entities**: Complex to define custom entity types
- **Advanced Analytics**: Limited built-in analytics and reporting
- **Multi-tenancy**: Limited native multi-tenant support

### Integration Limitations
- **Connector Coverage**: Not all data sources have native connectors
- **Custom Sources**: Requires development for custom data sources
- **Real-time Streaming**: Limited real-time metadata streaming
- **Legacy Systems**: Challenging integration with legacy systems

## 🚀 Version Highlights

### DataHub 0.12.x (Latest)
- **Improved UI/UX**: Enhanced user interface and experience
- **Advanced Search**: Better search relevance and performance
- **Data Contracts**: Support for data contracts and SLAs
- **Enhanced Lineage**: Improved lineage visualization and accuracy
- **Better Performance**: Optimized backend performance

### DataHub 0.11.x
- **Column-level Lineage**: Fine-grained lineage tracking
- **Data Quality**: Built-in data quality monitoring
- **Advanced Governance**: Enhanced policy management
- **API Improvements**: Better REST and GraphQL APIs

### DataHub 0.10.x
- **Kubernetes Support**: Native Kubernetes deployment
- **Improved Ingestion**: Better ingestion framework
- **Enhanced Security**: Improved authentication and authorization
- **Performance Optimizations**: Better scalability and performance

## 🎯 Use Cases

### 1. Data Discovery & Cataloging
- **Problem**: Data scientists spend 80% of time finding and understanding data
- **Solution**: Centralized catalog with rich metadata and search capabilities
- **Benefits**: Reduced time to insight, improved data reuse

### 2. Data Governance & Compliance
- **Problem**: Difficulty tracking data usage and ensuring compliance
- **Solution**: Policy enforcement, access control, and audit trails
- **Benefits**: Regulatory compliance, risk reduction, data security

### 3. Data Lineage & Impact Analysis
- **Problem**: Unknown data dependencies and impact of changes
- **Solution**: End-to-end lineage tracking and impact analysis
- **Benefits**: Reduced downtime, better change management

### 4. Data Quality Management
- **Problem**: Poor data quality affecting business decisions
- **Solution**: Automated quality monitoring and alerting
- **Benefits**: Improved data trust, better decision making

### 5. Data Collaboration
- **Problem**: Siloed data teams and poor communication
- **Solution**: Social features, documentation, and knowledge sharing
- **Benefits**: Improved collaboration, knowledge retention

## 📊 When to Use DataHub

### ✅ Use DataHub When:
- **Large Data Estate**: Managing hundreds or thousands of data assets
- **Multiple Data Platforms**: Diverse technology stack requiring unified view
- **Governance Requirements**: Need for data governance and compliance
- **Data Discovery Challenges**: Users struggle to find relevant data
- **Lineage Tracking**: Need to understand data flow and dependencies
- **Collaboration Needs**: Multiple teams working with shared data

### ❌ Consider Alternatives When:
- **Small Data Estate**: Few data sources and simple requirements
- **Single Platform**: All data in one system with built-in catalog
- **Limited Resources**: Insufficient infrastructure or maintenance capacity
- **Simple Use Cases**: Basic cataloging needs without governance requirements

## 📚 Quick References

### Essential Commands
```bash
# Install DataHub CLI
pip install acryl-datahub

# Run ingestion recipe
datahub ingest -c recipe.yml

# Check ingestion status
datahub check

# Delete metadata
datahub delete --urn "urn:li:dataset:..."
```

### Key APIs
```python
# REST API endpoints
GET /entities/{urn}                    # Get entity metadata
POST /entities                         # Create/update entity
DELETE /entities/{urn}                 # Delete entity
GET /search                           # Search entities
POST /lineage                         # Get lineage information
```

### Configuration Files
```yaml
# docker-compose.yml for local setup
version: '3.8'
services:
  datahub-gms:
    image: linkedin/datahub-gms:latest
    ports:
      - "8080:8080"
  
  datahub-frontend:
    image: linkedin/datahub-frontend-react:latest
    ports:
      - "9002:9002"
```

### Useful Links
- **Documentation**: [https://datahubproject.io/docs/](https://datahubproject.io/docs/)
- **GitHub Repository**: [https://github.com/datahub-project/datahub](https://github.com/datahub-project/datahub)
- **Community Slack**: [https://datahubspace.slack.com/](https://datahubspace.slack.com/)
- **Demo Environment**: [https://demo.datahubproject.io/](https://demo.datahubproject.io/)
- **API Documentation**: [https://datahubproject.io/docs/api/](https://datahubproject.io/docs/api/)