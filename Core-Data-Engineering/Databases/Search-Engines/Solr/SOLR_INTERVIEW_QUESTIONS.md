# Apache Solr - Interview Questions

## Basic Questions

### 1. What is Apache Solr and how does it differ from Elasticsearch?
**Answer:** Apache Solr is an enterprise search platform built on Lucene. Key differences from Elasticsearch:
- **Architecture**: Solr uses SolrCloud with ZooKeeper; Elasticsearch has built-in clustering
- **Configuration**: Solr uses XML configuration; Elasticsearch uses JSON
- **Query Language**: Solr has more mature query parsers; Elasticsearch focuses on JSON DSL
- **Analytics**: Solr has stronger faceting capabilities; Elasticsearch excels in aggregations

### 2. Explain Solr's document model and schema.
**Answer:** Solr's document model consists of:
- **Documents**: Collections of fields representing data units
- **Fields**: Named data elements with specific types
- **Schema**: Defines field types, analysis chains, and constraints
- **Dynamic Fields**: Pattern-based field definitions for flexible schemas

### 3. What is SolrCloud and how does it provide scalability?
**Answer:** SolrCloud is Solr's distributed architecture that provides:
- **Sharding**: Horizontal data distribution across nodes
- **Replication**: Data redundancy for fault tolerance
- **Auto-discovery**: ZooKeeper-based node coordination
- **Load balancing**: Request distribution across replicas
- **Auto-failover**: Automatic handling of node failures

## Intermediate Questions

### 4. How does Solr handle indexing and what are the different update methods?
**Answer:** Solr indexing methods:
```xml
<!-- Full document update -->
<add>
  <doc>
    <field name="id">123</field>
    <field name="title">Updated Title</field>
  </doc>
</add>

<!-- Atomic update -->
<add>
  <doc>
    <field name="id">123</field>
    <field name="price" update="set">29.99</field>
  </doc>
</add>
```
- **Full updates**: Replace entire documents
- **Atomic updates**: Modify specific fields
- **Batch updates**: Process multiple documents together
- **Real-time updates**: Near real-time search availability

### 5. What are Solr facets and how do you implement faceted search?
**Answer:** Facets provide drill-down navigation and analytics:
```
# Simple faceting
facet=true&facet.field=category&facet.field=brand

# Range faceting
facet.range=price&facet.range.start=0&facet.range.end=1000&facet.range.gap=100

# Query faceting
facet.query=price:[0 TO 50]&facet.query=price:[50 TO 100]
```
Types include field facets, range facets, query facets, and pivot facets.

### 6. How do you optimize Solr performance?
**Answer:** Performance optimization strategies:
- **Schema design**: Proper field types and analysis
- **Indexing**: Batch updates and commit strategies
- **Caching**: Query result and filter caching
- **Memory**: JVM heap tuning and off-heap storage
- **Sharding**: Optimal shard size and distribution
- **Hardware**: SSD storage and adequate RAM

## Advanced Questions

### 7. Explain Solr's query processing pipeline.
**Answer:** Query processing steps:
1. **Query parsing**: Parse query syntax into internal representation
2. **Analysis**: Apply text analysis (tokenization, filtering)
3. **Query expansion**: Handle synonyms, spell correction
4. **Index search**: Search inverted index structures
5. **Scoring**: Calculate relevance scores
6. **Filtering**: Apply filter queries
7. **Faceting**: Calculate facet counts
8. **Response formatting**: Format results for client

### 8. How would you implement a recommendation system using Solr?
**Answer:**
```xml
<!-- More Like This query -->
<requestHandler name="/mlt" class="solr.MoreLikeThisHandler">
  <lst name="defaults">
    <str name="mlt.fl">title,description,tags</str>
    <int name="mlt.mindf">2</int>
    <int name="mlt.mintf">2</int>
  </lst>
</requestHandler>

<!-- Collaborative filtering with function queries -->
q=*:*&fq={!func}sum(product(user_rating,similarity_score))&sort=score desc
```
Approaches include More Like This, collaborative filtering, and content-based recommendations.

### 9. What are Solr's security features and how do you implement them?
**Answer:** Solr security features:
- **Authentication**: Basic, Kerberos, JWT authentication
- **Authorization**: Role-based access control
- **SSL/TLS**: Encrypted communication
- **Audit logging**: Security event tracking
```xml
<!-- Security configuration -->
<security>
  <authentication class="solr.BasicAuthPlugin">
    <str name="blockUnknown">true</str>
  </authentication>
  <authorization class="solr.RuleBasedAuthorizationPlugin">
    <str name="permissions">admin-paths:/admin/*</str>
  </authorization>
</security>
```

### 10. How do you handle data migration and backup in Solr?
**Answer:** Data management strategies:
- **Backup**: Collection-level snapshots to HDFS/S3
- **Restore**: Point-in-time collection recovery
- **Replication**: Master-slave data synchronization
- **Export/Import**: JSON/CSV data exchange
```bash
# Create backup
curl "http://localhost:8983/solr/admin/collections?action=BACKUP&name=backup1&collection=mycollection"

# Restore backup
curl "http://localhost:8983/solr/admin/collections?action=RESTORE&name=backup1&collection=restored_collection"
```