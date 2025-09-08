# Amundsen Interview Questions

## 📋 Table of Contents
1. [Basic Concepts](#basic-concepts)
2. [Architecture & Components](#architecture--components)
3. [Data Discovery](#data-discovery)
4. [Metadata Management](#metadata-management)
5. [Search & Navigation](#search--navigation)
6. [Integration & Setup](#integration--setup)
7. [Administration & Security](#administration--security)
8. [Best Practices](#best-practices)
9. [Scenario-Based Questions](#scenario-based-questions)

---

## Basic Concepts

### Q1: What is Amundsen and what problems does it solve?
**Answer:**
Amundsen is an open-source data discovery and metadata platform developed by Lyft to improve data discovery and trust.

**Key Problems Solved:**
- **Data Discovery**: Find relevant datasets in large organizations
- **Metadata Management**: Centralized data documentation
- **Data Trust**: Understanding data quality and usage
- **Knowledge Sharing**: Collaborative data insights
- **Productivity**: Faster data exploration and analysis

**Core Features:**
- Search-driven data discovery
- Rich metadata management
- Data lineage visualization
- Usage analytics
- Collaborative features
- Open-source and extensible

### Q2: What are the main components of Amundsen architecture?
**Answer:**
**Core Components:**

1. **Frontend Service**: React-based web UI
2. **Search Service**: Elasticsearch-powered search
3. **Metadata Service**: Neo4j graph database for metadata
4. **Databuilder**: ETL framework for metadata ingestion

**Supporting Components:**
- **Proxy Services**: API gateway layer
- **Authentication**: SSO integration
- **Notification Service**: User alerts and updates

---

## Architecture & Components

### Q3: Explain Amundsen's microservices architecture.
**Answer:**
**Service Architecture:**

```
Frontend (React) → Proxy → Backend Services
                           ├── Search Service (Elasticsearch)
                           ├── Metadata Service (Neo4j)
                           └── Databuilder (ETL)
```

**Service Responsibilities:**
- **Frontend**: User interface and experience
- **Search**: Query processing and ranking
- **Metadata**: Graph-based metadata storage
- **Databuilder**: Extract, transform, load metadata

### Q4: How does Amundsen use Neo4j for metadata storage?
**Answer:**
**Graph Model Benefits:**
- **Relationships**: Natural representation of data connections
- **Traversal**: Efficient relationship queries
- **Flexibility**: Schema-less metadata storage
- **Scalability**: Handle complex data relationships

**Node Types:**
```cypher
// Example Neo4j nodes
(:Table {name: 'users', database: 'prod'})
(:Column {name: 'user_id', type: 'integer'})
(:User {email: 'analyst@company.com'})
(:Dashboard {name: 'Sales Dashboard'})

// Relationships
(:Table)-[:COLUMN]->(:Column)
(:User)-[:READ]->(:Table)
(:Dashboard)-[:USES]->(:Table)
```

### Q5: What is Databuilder and how does it work?
**Answer:**
**Databuilder Framework:**
- **ETL Pipeline**: Extract metadata from various sources
- **Pluggable Architecture**: Support multiple data sources
- **Transformation**: Normalize metadata formats
- **Loading**: Populate Neo4j and Elasticsearch

**Example Configuration:**
```python
# Databuilder job configuration
job_config = ConfigFactory.from_dict({
    'extractor.postgres_metadata.{}'.format(PostgresMetadataExtractor.CONNECTION_CONFIG_KEY): connection_string,
    'extractor.postgres_metadata.{}'.format(PostgresMetadataExtractor.WHERE_CLAUSE_SUFFIX_KEY): where_clause,
    'loader.filesystem_csv_neo4j.{}'.format(FsNeo4jCSVLoader.NODE_DIR_PATH): node_files_folder,
    'loader.filesystem_csv_neo4j.{}'.format(FsNeo4jCSVLoader.RELATION_DIR_PATH): relationship_files_folder,
    'publisher.neo4j.{}'.format(neo4j_csv_publisher.NODE_FILES_DIR): node_files_folder,
    'publisher.neo4j.{}'.format(neo4j_csv_publisher.RELATION_FILES_DIR): relationship_files_folder
})
```

---

## Data Discovery

### Q6: How does Amundsen's search functionality work?
**Answer:**
**Search Architecture:**
- **Elasticsearch Backend**: Full-text search capabilities
- **Ranking Algorithm**: Relevance scoring
- **Faceted Search**: Filter by database, schema, tags
- **Auto-complete**: Suggest as you type

**Search Features:**
```
Search Capabilities:
- Table and column names
- Descriptions and documentation
- Tags and categories
- Owner information
- Usage statistics
```

### Q7: What types of metadata does Amundsen collect and display?
**Answer:**
**Metadata Categories:**

**Technical Metadata:**
- Schema information (tables, columns, types)
- Database and cluster details
- Partition information
- Statistics (row counts, data sizes)

**Business Metadata:**
- Descriptions and documentation
- Tags and categories
- Owner information
- Business glossary terms

**Operational Metadata:**
- Usage statistics
- Query patterns
- Performance metrics
- Data freshness

**Social Metadata:**
- User interactions
- Bookmarks and favorites
- Comments and ratings

---

## Search & Navigation

### Q8: How does Amundsen rank search results?
**Answer:**
**Ranking Factors:**
- **Usage Frequency**: How often tables are queried
- **Recency**: When tables were last accessed
- **User Behavior**: Bookmarks and interactions
- **Text Relevance**: Match quality with search terms
- **Data Quality**: Completeness of metadata

**Scoring Algorithm:**
```python
# Simplified ranking calculation
score = (
    usage_score * 0.4 +
    recency_score * 0.2 +
    text_relevance * 0.3 +
    quality_score * 0.1
)
```

### Q9: What navigation features does Amundsen provide?
**Answer:**
**Navigation Features:**
- **Browse by Database**: Hierarchical exploration
- **Tag-based Navigation**: Category filtering
- **Related Tables**: Discover connected datasets
- **Popular Tables**: Most-used datasets
- **Recent Activity**: Recently accessed data

**User Experience:**
- Breadcrumb navigation
- Faceted filtering
- Infinite scroll results
- Mobile-responsive design

---

## Integration & Setup

### Q10: How do you set up Amundsen in a production environment?
**Answer:**
**Production Setup:**

1. **Infrastructure Requirements:**
```yaml
# Docker Compose example
version: '3'
services:
  neo4j:
    image: neo4j:3.5.6
    environment:
      NEO4J_AUTH: neo4j/test
  
  elasticsearch:
    image: elasticsearch:6.7.0
    environment:
      discovery.type: single-node
  
  amundsen-metadata:
    image: amundsendev/amundsen-metadata:latest
    depends_on:
      - neo4j
  
  amundsen-search:
    image: amundsendev/amundsen-search:latest
    depends_on:
      - elasticsearch
  
  amundsen-frontend:
    image: amundsendev/amundsen-frontend:latest
    depends_on:
      - amundsen-metadata
      - amundsen-search
```

2. **Configuration:**
- Database connections
- Authentication setup
- Resource allocation
- Monitoring configuration

### Q11: How do you integrate Amundsen with different data sources?
**Answer:**
**Supported Data Sources:**
- **Databases**: PostgreSQL, MySQL, Redshift, Snowflake
- **Big Data**: Hive, Presto, Druid
- **Cloud**: BigQuery, Athena
- **BI Tools**: Tableau, Mode, Superset

**Integration Example:**
```python
# Hive metadata extraction
job = DefaultJob(
    conf=job_config,
    task=DefaultTask(
        extractor=HiveTableMetadataExtractor(),
        transformer=NoopTransformer(),
        loader=FsNeo4jCSVLoader()
    ),
    publisher=Neo4jCsvPublisher()
)
job.launch()
```

### Q12: How do you handle metadata updates and synchronization?
**Answer:**
**Update Strategies:**
- **Scheduled Jobs**: Regular metadata refresh
- **Incremental Updates**: Only changed metadata
- **Event-Driven**: Real-time updates via webhooks
- **Manual Triggers**: On-demand synchronization

**Implementation:**
```python
# Scheduled metadata update
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def run_metadata_extraction():
    # Databuilder job execution
    job.launch()

dag = DAG('amundsen_metadata_sync', schedule_interval='@daily')
sync_task = PythonOperator(
    task_id='sync_metadata',
    python_callable=run_metadata_extraction,
    dag=dag
)
```

---

## Administration & Security

### Q13: How do you implement authentication and authorization in Amundsen?
**Answer:**
**Authentication Options:**
- **OIDC/OAuth2**: Integration with identity providers
- **LDAP**: Enterprise directory services
- **SAML**: Single sign-on
- **Custom**: Proprietary authentication systems

**Authorization Levels:**
```python
# Example authorization configuration
AUTHORIZATION_ENABLED = True
AUTHORIZATION_USER_GROUP_HEADER = 'X-User-Groups'

# Role-based access
ADMIN_USERS = ['admin@company.com']
POWER_USERS = ['analyst@company.com']
```

### Q14: What monitoring and observability features does Amundsen provide?
**Answer:**
**Monitoring Capabilities:**
- **Application Metrics**: Response times, error rates
- **Usage Analytics**: Search patterns, popular tables
- **System Health**: Service availability, resource usage
- **User Behavior**: Feature adoption, engagement

**Implementation:**
```python
# Metrics collection
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Custom metrics
search_counter = Counter('amundsen_searches_total', 'Total searches')
table_views = Counter('amundsen_table_views_total', 'Table detail views')
```

---

## Best Practices

### Q15: What are the best practices for Amundsen implementation?
**Answer:**
**Implementation Best Practices:**

1. **Data Quality**: Ensure clean, accurate metadata
2. **Documentation**: Encourage rich descriptions
3. **Tagging Strategy**: Consistent categorization
4. **User Training**: Educate on search techniques
5. **Governance**: Establish ownership and processes

**Technical Best Practices:**
- Regular metadata synchronization
- Performance monitoring
- Backup and disaster recovery
- Security hardening
- Scalability planning

### Q16: How do you encourage user adoption of Amundsen?
**Answer:**
**Adoption Strategies:**
- **Training Sessions**: Hands-on workshops
- **Success Stories**: Share use cases and wins
- **Integration**: Embed in existing workflows
- **Gamification**: Encourage contributions
- **Feedback Loop**: Continuous improvement

**User Engagement:**
```
Engagement Tactics:
- Lunch and learn sessions
- Data discovery challenges
- Recognition for contributors
- Regular feature updates
- Community building
```

---

## Scenario-Based Questions

### Q17: How would you scale Amundsen for a large enterprise?
**Answer:**
**Scaling Strategy:**

1. **Infrastructure Scaling:**
```yaml
# Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: amundsen-frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: amundsen-frontend
  template:
    spec:
      containers:
      - name: frontend
        image: amundsendev/amundsen-frontend:latest
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

2. **Data Partitioning**: Separate metadata by business units
3. **Caching**: Implement Redis for frequently accessed data
4. **Load Balancing**: Distribute traffic across instances

### Q18: How would you implement data lineage in Amundsen?
**Answer:**
**Lineage Implementation:**

1. **Graph Relationships**: Model data flow in Neo4j
```cypher
// Lineage relationships
(:Table {name: 'raw_events'})-[:UPSTREAM_OF]->(:Table {name: 'processed_events'})
(:Table {name: 'processed_events'})-[:UPSTREAM_OF]->(:Dashboard {name: 'Analytics Dashboard'})
```

2. **ETL Integration**: Extract lineage from workflow tools
```python
# Airflow lineage extraction
class AirflowLineageExtractor(Extractor):
    def extract(self):
        # Parse DAG files for task dependencies
        # Create lineage relationships
        pass
```

3. **Visualization**: Display lineage graphs in UI

### Q19: How would you handle data privacy and compliance in Amundsen?
**Answer:**
**Privacy Measures:**
- **Data Classification**: Tag sensitive data types
- **Access Controls**: Restrict metadata visibility
- **Audit Logging**: Track all user activities
- **Data Masking**: Hide sensitive column details
- **Retention Policies**: Manage metadata lifecycle

**Implementation:**
```python
# Privacy configuration
PRIVACY_ENABLED = True
SENSITIVE_DATA_TAGS = ['PII', 'PHI', 'Financial']
RESTRICTED_COLUMNS = ['ssn', 'credit_card', 'phone']

# Access control
def check_column_access(user, column):
    if column.has_tag('PII') and not user.has_permission('view_pii'):
        return False
    return True
```

### Q20: How would you integrate Amundsen with a modern data stack?
**Answer:**
**Integration Architecture:**
```
Modern Data Stack Integration:
1. Data Sources (Snowflake, BigQuery) → Databuilder
2. dbt → Amundsen (model metadata)
3. Airflow → Amundsen (pipeline lineage)
4. Looker/Tableau → Amundsen (dashboard usage)
5. Slack → Amundsen (notifications)
```

**Technical Implementation:**
```python
# dbt integration
class DbtMetadataExtractor(Extractor):
    def extract(self):
        # Parse dbt manifest.json
        # Extract model metadata
        # Create table and column nodes
        pass

# Slack integration
@app.route('/slack/search', methods=['POST'])
def slack_search():
    query = request.form['text']
    results = search_service.search(query)
    return format_slack_response(results)
```

---

## 🎯 Key Takeaways

- **Open Source**: Community-driven, extensible platform
- **Graph-Based**: Neo4j enables rich metadata relationships
- **Microservices**: Scalable, maintainable architecture
- **Search-Driven**: Elasticsearch powers discovery experience
- **Extensible**: Pluggable architecture for customization
- **Production-Ready**: Battle-tested at scale (Lyft, ING, etc.)
- **Community**: Active open-source ecosystem

Remember: Amundsen's strength lies in its open-source nature and proven scalability, making it ideal for organizations wanting full control over their data discovery platform.