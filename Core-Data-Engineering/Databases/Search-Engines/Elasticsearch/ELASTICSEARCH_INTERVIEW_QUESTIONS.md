# Elasticsearch Interview Questions

## Table of Contents

1. [Basic Elasticsearch Questions](#basic-elasticsearch-questions)
2. [Architecture & Concepts](#architecture--concepts)
3. [Indexing & Data Management](#indexing--data-management)
4. [Search & Query DSL](#search--query-dsl)
5. [Performance & Optimization](#performance--optimization)
6. [Cluster Management](#cluster-management)
7. [Security & Monitoring](#security--monitoring)
8. [Scenario-Based Questions](#scenario-based-questions)

---

## Basic Elasticsearch Questions

### 1. What is Elasticsearch and what are its primary use cases?
**Answer:**
Elasticsearch is a distributed, RESTful search and analytics engine built on Apache Lucene.

**Primary Use Cases:**
- **Full-text Search**: Website search, document search
- **Log Analytics**: Centralized logging with ELK stack
- **Real-time Analytics**: Business metrics and KPIs
- **Application Performance Monitoring**: APM and observability
- **Security Analytics**: SIEM and threat detection

### 2. Explain the ELK Stack and its components.
**Answer:**
- **Elasticsearch**: Search and analytics engine (storage and search)
- **Logstash**: Data processing pipeline (ingestion and transformation)
- **Kibana**: Visualization and management interface
- **Beats**: Lightweight data shippers (Filebeat, Metricbeat, etc.)

### 3. What are the key differences between Elasticsearch and traditional databases?
**Answer:**
- **Schema**: Schema-less vs. rigid schema
- **Search**: Full-text search capabilities vs. exact matches
- **Scaling**: Horizontal scaling vs. vertical scaling
- **ACID**: Eventually consistent vs. ACID compliant
- **Use Case**: Analytics and search vs. transactional operations

### 4. What is an inverted index and why is it important?
**Answer:**
An inverted index maps each unique word to a list of documents containing that word:
- **Fast Search**: Enables quick full-text search
- **Term Frequency**: Tracks how often terms appear
- **Relevance Scoring**: Supports relevance-based ranking
- **Memory Efficient**: Compressed storage of term mappings

### 5. Explain the basic Elasticsearch data structure hierarchy.
**Answer:**
```
Cluster → Nodes → Indices → Shards → Documents → Fields
```
- **Cluster**: Collection of nodes
- **Node**: Single Elasticsearch instance
- **Index**: Collection of documents with similar characteristics
- **Shard**: Subset of an index for horizontal scaling
- **Document**: JSON object stored in Elasticsearch
- **Field**: Key-value pair within a document

## Architecture & Concepts

### 6. What are shards and replicas in Elasticsearch?
**Answer:**
- **Primary Shard**: Original shard containing data
- **Replica Shard**: Copy of primary shard for redundancy
- **Benefits**: High availability, load distribution, fault tolerance
- **Configuration**: Set at index creation time (primary shards cannot be changed)

### 7. Explain the different types of Elasticsearch nodes.
**Answer:**
- **Master Node**: Cluster management, index creation/deletion
- **Data Node**: Stores data and executes search queries
- **Ingest Node**: Pre-processes documents before indexing
- **Coordinating Node**: Routes requests and aggregates results
- **Machine Learning Node**: Runs ML jobs and analytics

### 8. What is the master election process in Elasticsearch?
**Answer:**
- **Quorum**: Requires majority of master-eligible nodes
- **Split-brain Prevention**: Minimum master nodes setting
- **Election**: Nodes vote for master based on node ID and cluster state
- **Failover**: Automatic election when master fails

### 9. How does Elasticsearch handle distributed search?
**Answer:**
1. **Query Phase**: Coordinating node sends query to all shards
2. **Fetch Phase**: Retrieve actual documents from relevant shards
3. **Merge**: Combine and sort results from all shards
4. **Return**: Send final results to client

### 10. What is the difference between near real-time and real-time in Elasticsearch?
**Answer:**
- **Near Real-time**: Default refresh interval of 1 second
- **Real-time**: Immediate availability via GET API (bypasses refresh)
- **Refresh**: Makes indexed documents searchable
- **Performance**: Real-time has performance implications

## Indexing & Data Management

### 11. Explain the Elasticsearch indexing process.
**Answer:**
1. **Document Submission**: JSON document sent to Elasticsearch
2. **Routing**: Determine which shard to store document
3. **Primary Shard**: Document indexed on primary shard
4. **Replication**: Document replicated to replica shards
5. **Refresh**: Document becomes searchable after refresh

### 12. What are mappings in Elasticsearch?
**Answer:**
Mappings define how documents and fields are stored and indexed:
- **Dynamic Mapping**: Automatic field type detection
- **Explicit Mapping**: Manually defined field types and properties
- **Field Types**: text, keyword, date, numeric, boolean, etc.
- **Analyzers**: Define how text fields are processed

### 13. What is the difference between text and keyword field types?
**Answer:**
- **Text**: Analyzed, full-text search, not suitable for aggregations
- **Keyword**: Not analyzed, exact matches, suitable for filtering and aggregations
- **Use Cases**: Text for search content, keyword for IDs and categories

### 14. Explain analyzers in Elasticsearch.
**Answer:**
Analyzers process text during indexing and searching:
- **Character Filters**: Remove or replace characters
- **Tokenizer**: Split text into tokens
- **Token Filters**: Modify, add, or remove tokens
- **Built-in**: Standard, simple, whitespace, language-specific

### 15. What are index templates and when to use them?
**Answer:**
Index templates automatically apply settings and mappings to new indices:
- **Pattern Matching**: Apply to indices matching name patterns
- **Settings**: Index configuration (shards, replicas, analyzers)
- **Mappings**: Field definitions and types
- **Use Cases**: Log indices, time-series data

## Search & Query DSL

### 16. What are the main types of queries in Elasticsearch?
**Answer:**
- **Match Queries**: Full-text search with analysis
- **Term Queries**: Exact term matching
- **Range Queries**: Numeric or date ranges
- **Bool Queries**: Combine multiple queries with boolean logic
- **Wildcard/Regex**: Pattern matching queries

### 17. Explain the difference between query and filter context.
**Answer:**
- **Query Context**: Calculates relevance scores, affects ranking
- **Filter Context**: Yes/no matching, cached, no scoring
- **Performance**: Filters are faster and cacheable
- **Use Cases**: Query for search relevance, filter for exact matches

### 18. What is the bool query and its clauses?
**Answer:**
```json
{
  "bool": {
    "must": [],     // Documents must match (scored)
    "filter": [],   // Documents must match (not scored)
    "should": [],   // Documents should match (boost score)
    "must_not": []  // Documents must not match
  }
}
```

### 19. How does scoring work in Elasticsearch?
**Answer:**
- **TF-IDF**: Term frequency × Inverse document frequency
- **BM25**: Default scoring algorithm (improved TF-IDF)
- **Boost**: Increase/decrease field or query importance
- **Function Score**: Custom scoring with functions

### 20. What are aggregations and their types?
**Answer:**
Aggregations provide analytics on search results:
- **Bucket Aggregations**: Group documents (terms, date histogram)
- **Metric Aggregations**: Calculate metrics (avg, sum, max, min)
- **Pipeline Aggregations**: Process output of other aggregations
- **Matrix Aggregations**: Operate on multiple fields

## Performance & Optimization

### 21. How do you optimize Elasticsearch indexing performance?
**Answer:**
- **Bulk API**: Index multiple documents in single request
- **Refresh Interval**: Increase refresh interval during bulk loading
- **Replica Count**: Set replicas to 0 during initial loading
- **Memory**: Allocate sufficient heap memory (50% of RAM, max 32GB)
- **Disk I/O**: Use SSDs for better performance

### 22. What are the best practices for Elasticsearch search performance?
**Answer:**
- **Filter First**: Use filters before queries when possible
- **Field Data**: Avoid loading large field data into memory
- **Pagination**: Use scroll API for large result sets
- **Caching**: Leverage query and filter caching
- **Shard Size**: Keep shards between 10-50GB

### 23. How do you handle large datasets in Elasticsearch?
**Answer:**
- **Index Lifecycle Management**: Automate index rollover and deletion
- **Hot-Warm Architecture**: Separate recent and historical data
- **Shard Allocation**: Distribute shards across nodes efficiently
- **Compression**: Use best_compression codec for cold data
- **Frozen Indices**: Store rarely accessed data

### 24. What is index lifecycle management (ILM)?
**Answer:**
ILM automates index management through lifecycle phases:
- **Hot Phase**: Actively written and queried data
- **Warm Phase**: Read-only, less frequently queried
- **Cold Phase**: Rarely queried, compressed storage
- **Delete Phase**: Automatic deletion after retention period

### 25. How do you monitor Elasticsearch performance?
**Answer:**
- **Cluster Health API**: Overall cluster status
- **Node Stats API**: Node-level metrics
- **Index Stats API**: Index-level performance data
- **Monitoring Tools**: Kibana monitoring, Elastic APM
- **Key Metrics**: Indexing rate, search latency, memory usage

## Cluster Management

### 26. How do you scale an Elasticsearch cluster?
**Answer:**
- **Horizontal Scaling**: Add more nodes to cluster
- **Vertical Scaling**: Increase resources per node
- **Shard Strategy**: Plan shard count for future growth
- **Rebalancing**: Automatic shard redistribution
- **Rolling Upgrades**: Upgrade without downtime

### 27. What is shard allocation and how do you control it?
**Answer:**
- **Allocation Awareness**: Distribute shards across zones/racks
- **Allocation Filtering**: Control shard placement with attributes
- **Watermarks**: Disk usage thresholds for allocation decisions
- **Rebalancing**: Automatic redistribution for even load

### 28. How do you handle Elasticsearch cluster failures?
**Answer:**
- **Master Election**: Automatic master failover
- **Replica Promotion**: Promote replicas when primaries fail
- **Split-brain Prevention**: Minimum master nodes configuration
- **Backup Strategy**: Regular snapshots to external storage
- **Monitoring**: Proactive monitoring and alerting

### 29. What are Elasticsearch snapshots and how do you use them?
**Answer:**
Snapshots are backups of cluster data and state:
- **Repository**: S3, filesystem, or other storage backends
- **Incremental**: Only changed data since last snapshot
- **Restore**: Full or partial cluster restoration
- **Automation**: Schedule regular snapshots via SLM

## Security & Monitoring

### 30. How do you secure an Elasticsearch cluster?
**Answer:**
- **Authentication**: Built-in users, LDAP, SAML, PKI
- **Authorization**: Role-based access control (RBAC)
- **Encryption**: TLS for transport and HTTP layers
- **Network Security**: Firewall rules and VPN access
- **Audit Logging**: Track access and changes

### 31. What is X-Pack and its features?
**Answer:**
X-Pack provides enterprise features:
- **Security**: Authentication, authorization, encryption
- **Monitoring**: Cluster and application monitoring
- **Alerting**: Automated notifications and actions
- **Machine Learning**: Anomaly detection and forecasting
- **Graph**: Relationship analysis and visualization

## Scenario-Based Questions

### 32. You need to implement search for an e-commerce site. How do you design the Elasticsearch solution?
**Answer:**
1. **Index Design**: Product index with appropriate mappings
2. **Search Features**: Auto-complete, faceted search, fuzzy matching
3. **Performance**: Optimize for read-heavy workload
4. **Relevance**: Custom scoring for business rules
5. **Analytics**: Track search metrics and user behavior

### 33. Your Elasticsearch cluster is running slowly. How do you troubleshoot?
**Answer:**
1. **Check Cluster Health**: Identify red/yellow status
2. **Monitor Resources**: CPU, memory, disk usage
3. **Analyze Queries**: Slow query logs and performance
4. **Review Mappings**: Check for inefficient field types
5. **Optimize Indices**: Reindex with better settings if needed

### 34. How would you implement log aggregation for a microservices architecture?
**Answer:**
1. **Data Collection**: Deploy Filebeat on each service
2. **Processing**: Use Logstash for parsing and enrichment
3. **Storage**: Design time-based indices with ILM
4. **Visualization**: Create Kibana dashboards for monitoring
5. **Alerting**: Set up alerts for error patterns

### 35. You need to migrate from a relational database to Elasticsearch. What's your approach?
**Answer:**
1. **Data Analysis**: Understand current data structure and queries
2. **Mapping Design**: Design appropriate Elasticsearch mappings
3. **ETL Process**: Extract, transform, and load data
4. **Query Translation**: Convert SQL queries to Elasticsearch DSL
5. **Performance Testing**: Validate search performance
6. **Gradual Migration**: Phase migration to minimize risk

---

## Key Takeaways for Interviews

1. **Core Concepts**: Understand indices, shards, replicas, and documents
2. **Search Capabilities**: Know query DSL, analyzers, and scoring
3. **Performance**: Focus on indexing and search optimization techniques
4. **Cluster Management**: Understand scaling, failover, and maintenance
5. **Real-world Applications**: Be familiar with ELK stack and common use cases
6. **Troubleshooting**: Practice identifying and resolving performance issues
7. **Security**: Know authentication, authorization, and encryption options
8. **Monitoring**: Understand key metrics and monitoring tools