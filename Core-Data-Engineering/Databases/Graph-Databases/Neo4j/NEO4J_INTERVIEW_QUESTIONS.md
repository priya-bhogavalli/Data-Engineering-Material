# Neo4j Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions](#-basic-level-questions)
2. [Intermediate Level Questions](#-intermediate-level-questions)
3. [Advanced Level Questions](#-advanced-level-questions)
4. [Architecture & Performance](#-architecture--performance)
5. [Streaming & Real-time Processing](#-streaming--real-time-processing)
6. [Production & Operations](#-production--operations)
7. [Scenario-Based Questions](#-scenario-based-questions)

---

## 🟢 Basic Level Questions

### 1. What is Neo4j and when should you use a graph database?
**Answer**: Neo4j is a native graph database that stores data as nodes and relationships, optimized for traversing connected data.

**Use Cases:**
- Social networks and friend recommendations
- Fraud detection through pattern analysis
- Knowledge graphs and semantic search
- Supply chain and dependency analysis

```cypher
CREATE (alice:Person {name: 'Alice', age: 30})
CREATE (bob:Person {name: 'Bob', age: 25})
CREATE (alice)-[:KNOWS {since: 2019}]->(bob)
```

### 2. Explain Neo4j's property graph model
**Answer**: Property graph model consists of nodes, relationships, labels, and properties.

**Components:**
- **Nodes**: Entities with labels and properties
- **Relationships**: Directed connections with types and properties
- **Labels**: Group nodes by type (Person, Company)
- **Properties**: Key-value pairs on nodes/relationships

```cypher
CREATE (p:Person:Employee {
  name: 'John Doe',
  email: 'john@company.com',
  department: 'Engineering'
})
```

### 3. What is Cypher and how does it differ from SQL?
**Answer**: Cypher is Neo4j's declarative graph query language, designed for pattern matching.

**Key Differences:**
- **Pattern-based**: Uses ASCII art for relationships
- **Graph-focused**: Native support for traversals
- **Relationship-centric**: Joins are implicit through relationships

```cypher
MATCH (person:Person {name: 'Alice'})-[:FRIENDS_WITH]->(friend)-[:FRIENDS_WITH]->(fof)
WHERE person <> fof
RETURN fof.name
```

### 4. How do you create nodes and relationships in Neo4j?
**Answer**: Use CREATE statement for new data, MERGE for upsert operations.

```cypher
CREATE (alice:Person {name: 'Alice', age: 30})
CREATE (bob:Person {name: 'Bob', age: 25})

MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
CREATE (a)-[:FRIENDS_WITH {since: date('2020-01-01')}]->(b)

MERGE (c:Company {name: 'TechCorp'})
MERGE (alice:Person {name: 'Alice'})
MERGE (alice)-[:WORKS_FOR]->(c)
```

### 5. What are the basic Cypher clauses?
**Answer**: Core Cypher clauses for data manipulation and querying.

```cypher
-- MATCH: Pattern matching
MATCH (p:Person)-[:WORKS_FOR]->(c:Company)
WHERE p.age > 25
RETURN p.name, c.name

-- CREATE: Create new data
CREATE (p:Person {name: 'John', age: 35})

-- SET: Update properties
MATCH (p:Person {name: 'John'})
SET p.email = 'john@example.com'

-- DELETE: Remove nodes/relationships
MATCH (p:Person {name: 'John'})-[r:WORKS_FOR]->()
DELETE r, p

-- MERGE: Create or match
MERGE (p:Person {name: 'Jane'})
ON CREATE SET p.created = timestamp()
ON MATCH SET p.accessed = timestamp()
```

### 6. How do you handle variable-length paths in Neo4j?
**Answer**: Use variable-length path patterns with * notation.

```cypher
-- Find connections within 1-3 hops
MATCH path = (start:Person {name: 'Alice'})-[:KNOWS*1..3]-(connected:Person)
RETURN connected.name, length(path) as degrees_of_separation
ORDER BY degrees_of_separation

-- Shortest path between two nodes
MATCH (start:Person {name: 'Alice'}), (end:Person {name: 'Bob'})
MATCH path = shortestPath((start)-[:KNOWS*]-(end))
RETURN path, length(path) as path_length
```

### 7. What are indexes in Neo4j and why are they important?
**Answer**: Indexes improve query performance by creating fast lookup structures.

```cypher
-- Single property index
CREATE INDEX person_name FOR (p:Person) ON (p.name)

-- Composite index
CREATE INDEX person_name_age FOR (p:Person) ON (p.name, p.age)

-- Full-text index
CREATE FULLTEXT INDEX person_search FOR (p:Person) ON EACH [p.name, p.email]

-- Check index usage
EXPLAIN MATCH (p:Person {name: 'Alice'}) RETURN p
```

### 8. How do you implement constraints in Neo4j?
**Answer**: Constraints ensure data integrity and uniqueness.

```cypher
-- Uniqueness constraint
CREATE CONSTRAINT person_email FOR (p:Person) REQUIRE p.email IS UNIQUE

-- Node existence constraint
CREATE CONSTRAINT person_name FOR (p:Person) REQUIRE p.name IS NOT NULL

-- Node key constraint (composite uniqueness)
CREATE CONSTRAINT person_key FOR (p:Person) REQUIRE (p.name, p.email) IS NODE KEY

-- Property type constraint
CREATE CONSTRAINT person_age FOR (p:Person) REQUIRE p.age IS :: INTEGER
```

### 9. What is the difference between CREATE and MERGE?
**Answer**: CREATE always creates new data, MERGE creates only if pattern doesn't exist.

```cypher
-- CREATE: Always creates new nodes (can create duplicates)
CREATE (p:Person {name: 'Alice'})
CREATE (p:Person {name: 'Alice'}) -- Creates duplicate

-- MERGE: Creates only if doesn't exist
MERGE (p:Person {name: 'Alice'})
MERGE (p:Person {name: 'Alice'}) -- No duplicate created

-- MERGE with ON CREATE/ON MATCH
MERGE (p:Person {name: 'Alice'})
ON CREATE SET p.created = timestamp(), p.status = 'new'
ON MATCH SET p.accessed = timestamp(), p.status = 'existing'
```

### 10. How do you delete data in Neo4j?
**Answer**: Use DELETE clause, ensuring relationships are deleted before nodes.

```cypher
-- Delete relationships first, then nodes
MATCH (p:Person {name: 'Alice'})-[r]-()
DELETE r, p

-- DETACH DELETE removes node and all its relationships
MATCH (p:Person {name: 'Alice'})
DETACH DELETE p

-- Conditional deletion
MATCH (p:Person)
WHERE p.age < 18
DETACH DELETE p
```

## 🟡 Intermediate Level Questions

### 11. How do you implement aggregation in Cypher?
**Answer**: Use aggregation functions with GROUP BY behavior.

```cypher
-- Count relationships
MATCH (p:Person)-[:WORKS_FOR]->(c:Company)
RETURN c.name, count(p) as employee_count
ORDER BY employee_count DESC

-- Collect related data
MATCH (p:Person)-[:KNOWS]->(friend:Person)
RETURN p.name, collect(friend.name) as friends

-- Statistical aggregations
MATCH (p:Person)
RETURN avg(p.age) as avg_age, 
       min(p.age) as min_age, 
       max(p.age) as max_age,
       count(*) as total_people
```

### 12. How do you handle conditional logic in Cypher?
**Answer**: Use CASE expressions and conditional functions.

```cypher
-- CASE statements
MATCH (p:Person)
RETURN p.name,
  CASE
    WHEN p.age < 18 THEN 'Minor'
    WHEN p.age < 65 THEN 'Adult'
    ELSE 'Senior'
  END as age_group

-- COALESCE for null handling
MATCH (p:Person)
RETURN p.name, coalesce(p.email, 'No email provided') as email
```

### 13. What are the different types of joins in Neo4j?
**Answer**: Neo4j uses pattern matching instead of explicit joins.

```cypher
-- Inner join equivalent (both nodes must exist)
MATCH (p:Person)-[:WORKS_FOR]->(c:Company)
RETURN p.name, c.name

-- Left outer join equivalent (OPTIONAL MATCH)
MATCH (p:Person)
OPTIONAL MATCH (p)-[:WORKS_FOR]->(c:Company)
RETURN p.name, coalesce(c.name, 'Unemployed') as company

-- Multiple optional matches
MATCH (p:Person)
OPTIONAL MATCH (p)-[:WORKS_FOR]->(c:Company)
OPTIONAL MATCH (p)-[:LIVES_IN]->(city:City)
RETURN p.name, c.name, city.name
```

### 14. How do you implement graph algorithms in Neo4j?
**Answer**: Use Graph Data Science (GDS) library or write custom traversals.

```cypher
-- Create graph projection
CALL gds.graph.project(
  'social-network',
  'Person',
  'KNOWS',
  {
    nodeProperties: ['age'],
    relationshipProperties: ['strength']
  }
)

-- PageRank algorithm
CALL gds.pageRank.stream('social-network')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS person, score
ORDER BY score DESC
LIMIT 10

-- Community detection
CALL gds.louvain.stream('social-network')
YIELD nodeId, communityId
RETURN gds.util.asNode(nodeId).name AS person, communityId
ORDER BY communityId
```

### 15. How do you handle large data imports in Neo4j?
**Answer**: Use batch processing and optimized import strategies.

```cypher
-- LOAD CSV with periodic commit
USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM 'file:///large_dataset.csv' AS row
CREATE (p:Person {name: row.name, email: row.email})

-- UNWIND for batch operations
UNWIND $batch as row
MERGE (p:Person {id: row.id})
SET p.name = row.name, p.email = row.email

-- APOC batch processing
CALL apoc.periodic.iterate(
  "LOAD CSV FROM 'file:///data.csv' AS row RETURN row",
  "CREATE (p:Person {name: row[0], email: row[1]})",
  {batchSize: 1000, parallel: true}
)
```

### 16. What is APOC and how do you use it?
**Answer**: APOC (Awesome Procedures on Cypher) provides additional functionality.

```cypher
-- Load JSON data
CALL apoc.load.json('https://api.example.com/users') 
YIELD value
CREATE (p:Person {
  name: value.name,
  email: value.email,
  created: datetime(value.created_at)
})

-- Export data
CALL apoc.export.csv.query(
  "MATCH (p:Person)-[:WORKS_FOR]->(c:Company) RETURN p.name, c.name",
  "employees.csv",
  {}
)

-- Path expansion
MATCH (start:Person {name: 'Alice'})
CALL apoc.path.expandConfig(start, {
  relationshipFilter: 'KNOWS>',
  labelFilter: 'Person',
  maxLevel: 3
}) YIELD path
RETURN path
```

### 17. How do you implement full-text search in Neo4j?
**Answer**: Use full-text indexes with Lucene query syntax.

```cypher
-- Create full-text index
CREATE FULLTEXT INDEX person_search FOR (p:Person) ON EACH [p.name, p.bio, p.skills]

-- Basic full-text search
CALL db.index.fulltext.queryNodes('person_search', 'java developer')
YIELD node, score
RETURN node.name, node.skills, score
ORDER BY score DESC

-- Advanced search with Lucene syntax
CALL db.index.fulltext.queryNodes('person_search', 'name:john AND skills:python')
YIELD node, score
RETURN node.name, score
```

### 18. How do you handle transactions in Neo4j?
**Answer**: Neo4j provides ACID transactions with automatic and explicit control.

```python
# Python driver transaction example
from neo4j import GraphDatabase

def transfer_relationship(driver, from_person, to_person):
    with driver.session() as session:
        return session.write_transaction(
            _transfer_relationship, from_person, to_person
        )

def _transfer_relationship(tx, from_person, to_person):
    # Remove old relationship
    tx.run(
        "MATCH (from:Person {name: $from_name})-[r:MANAGES]->(to:Person {name: $to_name}) "
        "DELETE r",
        from_name=from_person, to_name=to_person
    )
    
    # Create new relationship
    result = tx.run(
        "MATCH (from:Person {name: $from_name}), (to:Person {name: $to_name}) "
        "CREATE (from)-[r:REPORTS_TO]->(to) "
        "RETURN r",
        from_name=from_person, to_name=to_person
    )
    
    return result.single()[0]
```

### 19. How do you optimize Cypher queries?
**Answer**: Use profiling, indexing, and query optimization techniques.

```cypher
-- Profile query performance
PROFILE MATCH (p:Person {name: 'Alice'})-[:KNOWS*1..3]-(connected)
RETURN connected.name

-- Explain query execution plan
EXPLAIN MATCH (p:Person)-[:WORKS_FOR]->(c:Company)
WHERE c.name = 'TechCorp'
RETURN p.name

-- Use parameters for query caching
MATCH (p:Person {name: $person_name})-[:WORKS_FOR]->(c:Company)
RETURN p.name, c.name

-- Filter early in the query
MATCH (p:Person)
WHERE p.department = 'Engineering'  -- Filter before relationship traversal
MATCH (p)-[:WORKS_FOR]->(c:Company)
RETURN p.name, c.name
```

### 20. How do you implement data validation in Neo4j?
**Answer**: Use constraints, property type checking, and validation procedures.

```cypher
-- Property type constraints
CREATE CONSTRAINT person_age FOR (p:Person) REQUIRE p.age IS :: INTEGER
CREATE CONSTRAINT person_email FOR (p:Person) REQUIRE p.email IS :: STRING

-- Custom validation with APOC
CALL apoc.when(
  $email =~ '.*@.*\..*',
  "MERGE (p:Person {email: $email})",
  "CREATE (e:ValidationError {message: 'Invalid email format', value: $email})",
  {email: $email}
)
```

## 🔴 Advanced Level Questions

### 21. How do you implement complex recommendation algorithms?
**Answer**: Combine collaborative filtering with graph traversals.

```cypher
-- Collaborative filtering recommendation
MATCH (target:Customer {id: 'C001'})-[:PURCHASED]->(p1:Product)<-[:PURCHASED]-(similar:Customer)
WHERE target <> similar
WITH target, similar, count(p1) as shared_products
WHERE shared_products >= 2
MATCH (similar)-[:PURCHASED]->(p2:Product)
WHERE NOT (target)-[:PURCHASED]->(p2)
RETURN p2.name, count(*) as recommendation_score
ORDER BY recommendation_score DESC
LIMIT 10
```

### 22. How do you handle graph versioning and temporal data?
**Answer**: Implement time-based relationships and versioned nodes.

```cypher
-- Temporal relationships with validity periods
CREATE (alice:Person {name: 'Alice'})
CREATE (company1:Company {name: 'StartupCorp'})
CREATE (company2:Company {name: 'BigCorp'})

-- Historical employment with time ranges
CREATE (alice)-[:WORKED_FOR {
  from: date('2018-01-01'),
  to: date('2020-12-31'),
  role: 'Developer'
}]->(company1)

CREATE (alice)-[:WORKS_FOR {
  from: date('2021-01-01'),
  to: null,
  role: 'Senior Developer'
}]->(company2)

-- Query current relationships
MATCH (p:Person)-[r:WORKS_FOR]->(c:Company)
WHERE r.to IS NULL OR r.to >= date()
RETURN p.name, c.name, r.role
```

### 23. How do you implement fraud detection patterns?
**Answer**: Use graph patterns to detect suspicious activities.

```cypher
-- Circular money transfer detection
MATCH path = (start:Account)-[:TRANSFER*3..6]->(start)
WHERE all(rel in relationships(path) WHERE rel.amount > 10000)
  AND all(node in nodes(path)[1..-1] WHERE node.created > datetime() - duration('P30D'))
RETURN path, 
       reduce(total = 0, rel in relationships(path) | total + rel.amount) as total_amount
ORDER BY total_amount DESC

-- Velocity fraud detection
MATCH (account:Account)-[t:TRANSFER]->()
WHERE t.timestamp > datetime() - duration('PT1H')
WITH account, count(t) as transfers_per_hour, sum(t.amount) as total_amount
WHERE transfers_per_hour > 50 OR total_amount > 100000
RETURN account.id, transfers_per_hour, total_amount
```

### 24. How do you implement graph-based machine learning pipelines?
**Answer**: Use GDS library for feature engineering and ML workflows.

```cypher
-- Create graph projection with features
CALL gds.graph.project(
  'ml-graph',
  ['Person', 'Company', 'Product'],
  ['KNOWS', 'WORKS_FOR', 'PURCHASED'],
  {
    nodeProperties: ['age', 'salary', 'price'],
    relationshipProperties: ['strength', 'duration', 'quantity']
  }
)

-- Feature engineering with graph algorithms
CALL gds.degree.mutate('ml-graph', {mutateProperty: 'degree'})
CALL gds.pageRank.mutate('ml-graph', {mutateProperty: 'pagerank'})
CALL gds.betweenness.mutate('ml-graph', {mutateProperty: 'betweenness'})

-- Node classification pipeline
CALL gds.beta.pipeline.nodeClassification.create('person-classifier')
CALL gds.beta.pipeline.nodeClassification.addNodeProperty('person-classifier', 'degree')
CALL gds.beta.pipeline.nodeClassification.addLogisticRegression('person-classifier')
```

### 25. How do you handle multi-tenancy in Neo4j?
**Answer**: Use multiple databases or tenant-aware data modeling.

```cypher
-- Database-level multi-tenancy (Neo4j 4.0+)
CREATE DATABASE tenant_a
CREATE DATABASE tenant_b

-- Switch to tenant database
:use tenant_a
CREATE (p:Person {name: 'Alice', tenant_id: 'tenant_a'})

-- Node-level multi-tenancy with filtering
MATCH (p:Person {tenant_id: $tenant_id})
RETURN p.name
```

### 26. How do you implement graph data lineage tracking?
**Answer**: Model data transformations as graph relationships.

```cypher
-- Data lineage model
CREATE (source:Dataset {name: 'customer_raw', type: 'source'})
CREATE (transform:Process {name: 'data_cleaning', type: 'transformation'})
CREATE (target:Dataset {name: 'customer_clean', type: 'target'})

CREATE (source)-[:INPUT_TO {timestamp: datetime()}]->(transform)
CREATE (transform)-[:OUTPUT_TO {timestamp: datetime()}]->(target)

-- Impact analysis query
MATCH path = (source:Dataset {name: 'customer_raw'})-[:INPUT_TO*]->(downstream:Dataset)
RETURN downstream.name, length(path) as impact_distance
ORDER BY impact_distance
```

### 27. How do you implement real-time graph updates with streaming?
**Answer**: Use change data capture and streaming processors.

```python
# Kafka consumer for real-time graph updates
from kafka import KafkaConsumer
from neo4j import GraphDatabase
import json

class RealTimeGraphUpdater:
    def __init__(self, neo4j_uri, kafka_topic):
        self.driver = GraphDatabase.driver(neo4j_uri)
        self.consumer = KafkaConsumer(
            kafka_topic,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
    
    def process_events(self):
        for message in self.consumer:
            event = message.value
            self.handle_event(event)
```

### 28. How do you implement graph-based access control?
**Answer**: Model permissions as graph relationships.

```cypher
-- Access control model
CREATE (user:User {name: 'alice', role: 'analyst'})
CREATE (resource:Resource {name: 'customer_data', type: 'dataset'})
CREATE (permission:Permission {action: 'read', granted_by: 'admin'})

CREATE (user)-[:HAS_PERMISSION]->(permission)
CREATE (permission)-[:APPLIES_TO]->(resource)

-- Check user permissions
MATCH (user:User {name: $username})-[:HAS_ROLE|HAS_PERMISSION*1..2]->(perm:Permission)-[:APPLIES_TO]->(resource:Resource)
WHERE resource.name = $resource_name AND perm.action = $action
RETURN count(perm) > 0 as has_access
```

### 29. How do you implement graph-based caching strategies?
**Answer**: Use graph patterns for intelligent cache invalidation.

```cypher
-- Cache dependency model
CREATE (cache1:Cache {key: 'user_profile_123', ttl: 3600})
CREATE (data:Data {id: 'user_123', last_modified: datetime()})
CREATE (cache1)-[:DEPENDS_ON]->(data)

-- Invalidate dependent caches
MATCH (data:Data {id: $data_id})<-[:DEPENDS_ON]-(cache:Cache)
SET data.last_modified = datetime()
DETACH DELETE cache
```

### 30. How do you implement distributed graph processing?
**Answer**: Use graph partitioning and distributed algorithms.

```cypher
-- Graph partitioning by community
CALL gds.louvain.write('large-graph', {
  writeProperty: 'partition'
})

-- Process partitions separately
MATCH (n:Node {partition: $partition_id})
WITH collect(n) as partition_nodes
CALL apoc.periodic.iterate(
  "UNWIND $nodes as node RETURN node",
  "MATCH (node)-[r]->(connected) SET r.processed = true",
  {batchSize: 1000, params: {nodes: partition_nodes}}
)
```

## 🏢 Architecture & Performance

### 31. How do you design Neo4j clustering for high availability?
**Answer**: Implement Causal Clustering with core and read replica servers.

```bash
# Core server configuration (neo4j.conf)
dbms.mode=CORE
causal_clustering.minimum_core_cluster_size_at_formation=3
causal_clustering.initial_discovery_members=server1:5000,server2:5000,server3:5000
```

```cypher
-- Check cluster status
CALL dbms.cluster.overview() YIELD id, addresses, role, groups
RETURN id, addresses, role, groups
```

### 32. How do you optimize Neo4j memory configuration?
**Answer**: Configure heap, page cache, and off-heap memory appropriately.

```bash
# Memory configuration in neo4j.conf
dbms.memory.heap.initial_size=8G
dbms.memory.heap.max_size=8G
dbms.memory.pagecache.size=16G
dbms.memory.transaction.global_max_size=1G
```

### 33. How do you implement backup and disaster recovery?
**Answer**: Use neo4j-admin backup and implement recovery procedures.

```bash
# Full backup
neo4j-admin backup --backup-dir=/backups --name=graph.db-backup

# Restore from backup
neo4j-admin restore --from=/backups/graph.db-backup --database=graph.db --force

# Consistency check
neo4j-admin check-consistency --database=graph.db
```

### 34. How do you monitor Neo4j performance?
**Answer**: Use built-in monitoring and custom metrics collection.

```cypher
-- Monitor running queries
CALL dbms.listQueries() 
YIELD queryId, query, elapsedTimeMillis, status
WHERE elapsedTimeMillis > 5000
RETURN queryId, query, elapsedTimeMillis, status

-- Kill long-running queries
CALL dbms.killQuery($queryId)

-- Database statistics
CALL db.stats.retrieve('GRAPH COUNTS') YIELD section, data
RETURN section, data
```

### 35. How do you implement security in Neo4j?
**Answer**: Configure authentication, authorization, and encryption.

```cypher
-- User and role management
CREATE USER alice SET PASSWORD 'secure_password'
CREATE ROLE data_analyst
GRANT ROLE data_analyst TO alice

-- Fine-grained permissions
GRANT MATCH {name, email} ON GRAPH * NODES Person TO data_analyst
DENY MATCH {salary} ON GRAPH * NODES Person TO data_analyst
```

```bash
# Enable encryption at rest
dbms.security.encryption.enabled=true

# Enable SSL/TLS
dbms.connector.bolt.tls_level=REQUIRED
dbms.ssl.policy.bolt.enabled=true
```

### 36. How do you optimize write performance?
**Answer**: Use batch operations and optimize transactions.

```cypher
-- Batch insert optimization
UNWIND $batch as row
CREATE (p:Person {id: row.id, name: row.name, email: row.email})

-- Use MERGE carefully (can be slow)
WITH $data as data
MATCH (existing:Person {id: data.id})
WITH data, existing
WHERE existing IS NULL
CREATE (p:Person {id: data.id, name: data.name})
```

### 37. How do you implement read scaling?
**Answer**: Use read replicas and query routing.

```python
# Python driver with read/write routing
from neo4j import GraphDatabase, WRITE_ACCESS, READ_ACCESS

class Neo4jService:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def write_data(self, query, parameters):
        with self.driver.session(default_access_mode=WRITE_ACCESS) as session:
            return session.run(query, parameters)
    
    def read_data(self, query, parameters):
        with self.driver.session(default_access_mode=READ_ACCESS) as session:
            return session.run(query, parameters)
```

### 38. How do you handle capacity planning?
**Answer**: Analyze growth patterns and resource requirements.

```cypher
-- Growth analysis
MATCH (n)
WITH labels(n) as nodeLabels, count(n) as nodeCount
UNWIND nodeLabels as label
RETURN label, sum(nodeCount) as total_nodes
ORDER BY total_nodes DESC

-- Relationship distribution
MATCH ()-[r]->()
RETURN type(r) as relationship_type, count(r) as count
ORDER BY count DESC

-- Storage size analysis
CALL db.stats.retrieve('STORE SIZES') YIELD section, data
RETURN section, data
```

### 39. How do you troubleshoot performance issues?
**Answer**: Use profiling and diagnostic tools.

```cypher
-- Query plan analysis
PROFILE MATCH (p:Person)-[:WORKS_FOR*1..3]->(c:Company)
WHERE c.industry = 'Technology'
RETURN p.name, c.name

-- Index usage analysis
CALL db.indexes() YIELD name, state, populationPercent, type
WHERE populationPercent < 100
RETURN name, state, populationPercent, type

-- Transaction monitoring
CALL dbms.queryJmx('org.neo4j:instance=kernel#0,name=Transactions')
YIELD attributes
RETURN attributes.NumberOfOpenTransactions
```

### 40. How do you implement data partitioning?
**Answer**: Use Fabric for query federation and logical partitioning.

```cypher
-- Fabric query across shards
USE fabric.graphAt('neo4j://server1:7687', 'shard1')
MATCH (p:Person) WHERE p.region = 'US'
RETURN p.name
UNION
USE fabric.graphAt('neo4j://server2:7687', 'shard2')
MATCH (p:Person) WHERE p.region = 'EU'
RETURN p.name

-- Horizontal partitioning strategy
MATCH (p:Person)
WHERE p.created_date >= date('2023-01-01')
SET p:RecentPerson
```

## 🔄 Streaming & Real-time Processing

### 41. How do you implement real-time graph updates?
**Answer**: Use change data capture and streaming processors.

```python
# Kafka consumer for real-time updates
from kafka import KafkaConsumer
from neo4j import GraphDatabase
import json

class RealTimeGraphUpdater:
    def __init__(self, neo4j_uri, kafka_topic):
        self.driver = GraphDatabase.driver(neo4j_uri)
        self.consumer = KafkaConsumer(
            kafka_topic,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
    
    def process_events(self):
        for message in self.consumer:
            event = message.value
            self.update_graph(event)
    
    def update_graph(self, event):
        query = """
        MERGE (u:User {id: $user_id})
        CREATE (a:Activity {
            type: $activity_type,
            timestamp: datetime($timestamp)
        })
        CREATE (u)-[:PERFORMED]->(a)
        """
        
        with self.driver.session() as session:
            session.run(query, event)
```

### 42. How do you handle event sourcing with Neo4j?
**Answer**: Model events as nodes with temporal relationships.

```cypher
-- Event sourcing model
CREATE (user:User {id: 'U001', name: 'Alice'})
CREATE (event1:Event {id: 'E001', type: 'UserCreated', timestamp: datetime()})
CREATE (event2:Event {id: 'E002', type: 'ProfileUpdated', timestamp: datetime()})

CREATE (event1)-[:APPLIES_TO]->(user)
CREATE (event2)-[:APPLIES_TO]->(user)
CREATE (event1)-[:NEXT]->(event2)

-- Replay events to rebuild state
MATCH (user:User {id: 'U001'})<-[:APPLIES_TO]-(event:Event)
WITH user, event
ORDER BY event.timestamp
RETURN user, collect(event) as event_history
```

### 43. How do you implement graph streaming analytics?
**Answer**: Use windowed aggregations and pattern detection.

```cypher
-- Sliding window analysis
MATCH (user:User)-[:PERFORMED]->(event:Event)
WHERE event.timestamp > datetime() - duration('PT1H')
WITH user, count(event) as events_per_hour
WHERE events_per_hour > 100
RETURN user.id, events_per_hour
ORDER BY events_per_hour DESC

-- Real-time anomaly detection
MATCH (account:Account)-[t:TRANSACTION]->()
WHERE t.timestamp > datetime() - duration('PT5M')
WITH account, 
     count(t) as recent_transactions,
     sum(t.amount) as total_amount,
     avg(t.amount) as avg_amount
WHERE recent_transactions > 20 OR total_amount > 50000
RETURN account.id, recent_transactions, total_amount, avg_amount
```

### 44. How do you handle high-velocity data ingestion?
**Answer**: Use batching and asynchronous processing.

```python
# Async batch processor
import asyncio
from neo4j import AsyncGraphDatabase

class AsyncBatchProcessor:
    def __init__(self, uri, user, password, batch_size=1000):
        self.driver = AsyncGraphDatabase.driver(uri, auth=(user, password))
        self.batch_size = batch_size
        self.batch = []
    
    async def add_event(self, event):
        self.batch.append(event)
        if len(self.batch) >= self.batch_size:
            await self.flush_batch()
    
    async def flush_batch(self):
        if not self.batch:
            return
        
        query = """
        UNWIND $events as event
        MERGE (u:User {id: event.user_id})
        CREATE (a:Activity {
            type: event.type,
            timestamp: datetime(event.timestamp)
        })
        CREATE (u)-[:PERFORMED]->(a)
        """
        
        async with self.driver.session() as session:
            await session.run(query, events=self.batch)
        
        self.batch.clear()
```

### 45. How do you implement change data capture (CDC)?
**Answer**: Track changes using triggers or log-based CDC.

```cypher
-- Change tracking model
CREATE (person:Person {id: 'P001', name: 'Alice', version: 1})
CREATE (change:Change {
  entity_id: 'P001',
  entity_type: 'Person',
  operation: 'CREATE',
  timestamp: datetime(),
  changes: {name: 'Alice'}
})

-- Update with change tracking
MATCH (p:Person {id: 'P001'})
SET p.name = 'Alice Johnson', p.version = p.version + 1
CREATE (change:Change {
  entity_id: 'P001',
  entity_type: 'Person',
  operation: 'UPDATE',
  timestamp: datetime(),
  old_values: {name: 'Alice'},
  new_values: {name: 'Alice Johnson'}
})
```

### 46. How do you implement real-time recommendations?
**Answer**: Combine streaming events with graph algorithms.

```cypher
-- Real-time recommendation based on current session
MATCH (user:User {id: $user_id})-[:VIEWED]->(product:Product)
WHERE product.viewed_at > datetime() - duration('PT30M')
WITH user, collect(product) as recent_views

-- Find similar products viewed by others
UNWIND recent_views as viewed_product
MATCH (viewed_product)<-[:VIEWED]-(other_user:User)-[:VIEWED]->(similar:Product)
WHERE other_user <> user AND NOT (user)-[:VIEWED]->(similar)
WITH similar, count(*) as similarity_score
ORDER BY similarity_score DESC
LIMIT 5
RETURN similar.name, similarity_score
```

### 47. How do you handle streaming data deduplication?
**Answer**: Use MERGE operations and temporal windows.

```cypher
-- Deduplication with time windows
WITH $events as events
UNWIND events as event
WITH event, 
     datetime(event.timestamp) as event_time,
     event.user_id + '_' + event.type + '_' + toString(duration.between(datetime('1970-01-01T00:00:00Z'), datetime(event.timestamp)).minutes / 5) as dedup_key

MERGE (de:DedupEvent {key: dedup_key})
ON CREATE SET 
  de.user_id = event.user_id,
  de.type = event.type,
  de.first_seen = event_time,
  de.count = 1
ON MATCH SET 
  de.count = de.count + 1,
  de.last_seen = event_time
```

### 48. How do you implement streaming graph pattern matching?
**Answer**: Use incremental pattern detection on streaming data.

```cypher
-- Detect suspicious patterns in real-time
MATCH (account:Account)-[t1:TRANSFER]->(intermediate:Account)-[t2:TRANSFER]->(destination:Account)
WHERE t1.timestamp > datetime() - duration('PT10M')
  AND t2.timestamp > t1.timestamp
  AND t2.timestamp < t1.timestamp + duration('PT5M')
  AND t1.amount > 10000
  AND abs(t1.amount - t2.amount) < 100
RETURN account.id as source, 
       intermediate.id as intermediate, 
       destination.id as destination,
       t1.amount, t2.amount,
       duration.between(t1.timestamp, t2.timestamp) as time_diff
```

### 49. How do you handle streaming data schema evolution?
**Answer**: Use flexible property models and versioning.

```cypher
-- Schema evolution handling
WITH $event as event
CALL {
  WITH event
  WHERE event.schema_version = '1.0'
  MERGE (u:User {id: event.user_id})
  SET u.name = event.name
  RETURN u
  UNION
  WITH event
  WHERE event.schema_version = '2.0'
  MERGE (u:User {id: event.user_id})
  SET u.name = event.full_name, u.email = event.email
  RETURN u
} IN TRANSACTIONS
RETURN count(*) as processed
```

### 50. How do you implement streaming graph aggregations?
**Answer**: Use time-based bucketing and incremental updates.

```cypher
-- Streaming aggregation with time buckets
WITH $events as events
UNWIND events as event
WITH event,
     datetime(event.timestamp) as event_time,
     duration.between(datetime('1970-01-01T00:00:00Z'), datetime(event.timestamp)).minutes / 15 as bucket_id

MERGE (bucket:TimeBucket {id: toString(bucket_id), type: event.type})
ON CREATE SET 
  bucket.start_time = datetime({epochMinutes: bucket_id * 15}),
  bucket.count = 1,
  bucket.sum = event.value
ON MATCH SET 
  bucket.count = bucket.count + 1,
  bucket.sum = bucket.sum + event.value,
  bucket.avg = bucket.sum / bucket.count
```

## 🛠️ Production & Operations

### 51. How do you implement Neo4j monitoring in production?
**Answer**: Use comprehensive monitoring stack with metrics collection.

```bash
# Prometheus metrics configuration
metrics.prometheus.enabled=true
metrics.prometheus.endpoint=localhost:2004

# JMX monitoring
dbms.jvm.additional=-Dcom.sun.management.jmxremote
dbms.jvm.additional=-Dcom.sun.management.jmxremote.port=3637
```

```cypher
-- Health check queries
CALL dbms.components() YIELD name, versions, edition
RETURN name, versions, edition

-- Performance metrics
CALL dbms.queryJmx('org.neo4j:instance=kernel#0,name=Transactions')
YIELD attributes
RETURN attributes.NumberOfOpenTransactions

-- Memory usage
CALL dbms.queryJmx('java.lang:type=Memory')
YIELD attributes
RETURN attributes.HeapMemoryUsage, attributes.NonHeapMemoryUsage
```

### 52. How do you handle Neo4j upgrades?
**Answer**: Plan and execute rolling upgrades with minimal downtime.

```bash
# Pre-upgrade checklist
# 1. Backup database
neo4j-admin backup --backup-dir=/backups --name=pre-upgrade-backup

# 2. Check compatibility
neo4j-admin check-consistency --database=graph.db

# 3. Test upgrade on staging
# 4. Rolling upgrade for cluster
# Stop read replicas first, then core servers one by one
```

### 53. How do you implement disaster recovery procedures?
**Answer**: Establish RTO/RPO targets and recovery procedures.

```bash
# Disaster recovery setup
# 1. Cross-region backup replication
rsync -av /backups/ backup-server:/remote-backups/

# 2. Recovery procedure
neo4j stop
neo4j-admin restore --from=/backups/disaster-recovery --database=graph.db --force
neo4j start

# 3. Verify recovery
neo4j-admin check-consistency --database=graph.db
```

### 54. How do you handle Neo4j configuration management?
**Answer**: Use configuration management tools and version control.

```yaml
# Ansible playbook for Neo4j configuration
- name: Configure Neo4j
  template:
    src: neo4j.conf.j2
    dest: /etc/neo4j/neo4j.conf
  vars:
    heap_size: "{{ neo4j_heap_size }}"
    page_cache_size: "{{ neo4j_page_cache_size }}"
  notify: restart neo4j

- name: Configure cluster settings
  lineinfile:
    path: /etc/neo4j/neo4j.conf
    regexp: '^causal_clustering.initial_discovery_members='
    line: 'causal_clustering.initial_discovery_members={{ cluster_members }}'
```

### 55. How do you implement Neo4j log management?
**Answer**: Configure structured logging and log aggregation.

```bash
# Logging configuration in neo4j.conf
dbms.logs.query.enabled=true
dbms.logs.query.threshold=1s
dbms.logs.query.parameter_logging_enabled=true
dbms.logs.security.level=INFO

# Log rotation
dbms.logs.query.rotation.keep_number=7
dbms.logs.query.rotation.size=20M
```

```yaml
# Filebeat configuration for log shipping
filebeat.inputs:
- type: log
  paths:
    - /var/log/neo4j/query.log
  fields:
    service: neo4j
    log_type: query
  multiline.pattern: '^\d{4}-\d{2}-\d{2}'
  multiline.negate: true
  multiline.match: after
```

### 56. How do you implement Neo4j security hardening?
**Answer**: Apply security best practices and compliance measures.

```bash
# Security configuration
dbms.security.auth_enabled=true
dbms.security.procedures.unrestricted=apoc.*
dbms.security.procedures.allowlist=apoc.*,gds.*

# Network security
dbms.default_listen_address=127.0.0.1
dbms.connector.bolt.listen_address=:7687
dbms.connector.http.listen_address=:7474

# SSL/TLS configuration
dbms.ssl.policy.bolt.enabled=true
dbms.ssl.policy.bolt.base_directory=certificates/bolt
dbms.ssl.policy.bolt.private_key=private.key
dbms.ssl.policy.bolt.public_certificate=public.crt
```

### 57. How do you handle Neo4j capacity planning?
**Answer**: Monitor usage patterns and plan for growth.

```cypher
-- Storage analysis
CALL db.stats.retrieve('STORE SIZES') YIELD section, data
UNWIND data as item
RETURN section, item.label as component, item.size as size_bytes
ORDER BY size_bytes DESC

-- Query performance analysis
CALL db.stats.retrieve('QUERY STATS') YIELD section, data
RETURN section, data

-- Growth trend analysis
MATCH (n)
WHERE exists(n.created_date)
WITH date(n.created_date) as creation_date, count(n) as daily_count
RETURN creation_date, daily_count
ORDER BY creation_date DESC
LIMIT 30
```

### 58. How do you implement Neo4j performance tuning?
**Answer**: Optimize configuration, queries, and hardware resources.

```bash
# Performance tuning configuration
# Memory settings
dbms.memory.heap.initial_size=16G
dbms.memory.heap.max_size=16G
dbms.memory.pagecache.size=32G

# Transaction settings
dbms.memory.transaction.global_max_size=2G
dbms.memory.transaction.max_size=1G

# Query settings
cypher.default_language_version=4
cypher.forbid_exhaustive_shortestpath=true
cypher.hints_error=true
```

```cypher
-- Query optimization
-- Before: Slow query
MATCH (p:Person)-[:KNOWS*1..3]-(connected:Person)
WHERE p.name = 'Alice'
RETURN connected.name

-- After: Optimized with index and limits
MATCH (p:Person {name: 'Alice'})-[:KNOWS*1..3]-(connected:Person)
RETURN connected.name
LIMIT 100
```

### 59. How do you handle Neo4j data migration?
**Answer**: Plan and execute data migration with minimal downtime.

```bash
# Migration strategy
# 1. Export data from source
neo4j-admin dump --database=source_db --to=/exports/source_dump.dump

# 2. Transform data if needed
# Custom scripts or APOC procedures

# 3. Import to target
neo4j-admin load --from=/exports/source_dump.dump --database=target_db --force

# 4. Verify migration
neo4j-admin check-consistency --database=target_db
```

```cypher
-- Data validation after migration
MATCH (n)
RETURN labels(n) as node_labels, count(n) as count
ORDER BY count DESC

MATCH ()-[r]->()
RETURN type(r) as relationship_type, count(r) as count
ORDER BY count DESC
```

### 60. How do you implement Neo4j alerting and incident response?
**Answer**: Set up proactive monitoring and automated responses.

```yaml
# Prometheus alerting rules
groups:
- name: neo4j
  rules:
  - alert: Neo4jDown
    expr: up{job="neo4j"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Neo4j instance is down"
      
  - alert: Neo4jHighQueryLatency
    expr: neo4j_cypher_query_duration_seconds{quantile="0.95"} > 5
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: "Neo4j query latency is high"
      
  - alert: Neo4jHighMemoryUsage
    expr: neo4j_memory_heap_used_bytes / neo4j_memory_heap_max_bytes > 0.9
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Neo4j memory usage is high"

## 🎯 Scenario-Based Questions

### 61. Design a social media recommendation system
**Answer**: Implement collaborative filtering with graph algorithms.

```cypher
-- Data model
CREATE (alice:User {id: 'U001', name: 'Alice'})
CREATE (bob:User {id: 'U002', name: 'Bob'})
CREATE (post1:Post {id: 'P001', content: 'Hello World'})

CREATE (alice)-[:FOLLOWS]->(bob)
CREATE (alice)-[:LIKES]->(post1)
CREATE (bob)-[:LIKES]->(post1)

-- Friend recommendations
MATCH (user:User {id: 'U001'})-[:FOLLOWS]->(friend)-[:FOLLOWS]->(fof:User)
WHERE NOT (user)-[:FOLLOWS]->(fof) AND user <> fof
WITH fof, count(*) as mutual_connections
ORDER BY mutual_connections DESC
LIMIT 5
RETURN fof.name, mutual_connections
```

### 62. Implement a fraud detection system
**Answer**: Use pattern matching to detect suspicious activities.

```cypher
-- Circular money transfers
MATCH path = (start:Account)-[:TRANSFER*3..5]->(start)
WHERE all(rel in relationships(path) WHERE rel.amount > 1000)
RETURN path, reduce(total = 0, rel in relationships(path) | total + rel.amount) as total

-- Shared device fraud
MATCH (account1:Account)-[:USED_DEVICE]->(device:Device)<-[:USED_DEVICE]-(account2:Account)
WHERE account1 <> account2 AND account1.created > datetime() - duration('P7D')
WITH device, collect(DISTINCT account1) + collect(DISTINCT account2) as suspicious_accounts
WHERE size(suspicious_accounts) > 5
RETURN device.id, suspicious_accounts
```

### 63. Design a knowledge graph for enterprise search
**Answer**: Model entities, relationships, and implement semantic search.

```cypher
-- Knowledge graph model
CREATE (person:Person {name: 'John Doe', role: 'Data Engineer'})
CREATE (company:Company {name: 'TechCorp', industry: 'Technology'})
CREATE (project:Project {name: 'Data Pipeline', status: 'Active'})
CREATE (skill:Skill {name: 'Neo4j', category: 'Database'})

CREATE (person)-[:WORKS_FOR]->(company)
CREATE (person)-[:WORKS_ON]->(project)
CREATE (person)-[:HAS_SKILL]->(skill)

-- Expert finding
MATCH (person:Person)-[:HAS_SKILL]->(skill:Skill {name: 'Neo4j'})
MATCH (person)-[:WORKS_ON]->(project:Project {status: 'Active'})
RETURN person.name, collect(project.name) as active_projects
```

### 64. Implement supply chain risk analysis
**Answer**: Model dependencies and analyze impact propagation.

```cypher
-- Supply chain model
CREATE (supplier:Supplier {name: 'Critical Supplier', risk_level: 'High'})
CREATE (component:Component {name: 'Microchip', criticality: 'High'})
CREATE (product:Product {name: 'Smartphone', revenue_impact: 1000000})

CREATE (supplier)-[:SUPPLIES {lead_time: 30, reliability: 0.95}]->(component)
CREATE (component)-[:USED_IN {quantity: 2}]->(product)

-- Risk impact analysis
MATCH path = (supplier:Supplier {risk_level: 'High'})-[:SUPPLIES*1..5]->(product:Product)
WITH product, length(path) as supply_chain_depth, supplier
RETURN product.name, product.revenue_impact, supply_chain_depth
ORDER BY product.revenue_impact DESC
```

### 65. Design a real-time recommendation engine
**Answer**: Combine real-time events with historical patterns.

```cypher
-- Real-time recommendation model
MATCH (user:User {id: 'U001'})-[:VIEWED]->(product:Product)
WHERE product.viewed_at > datetime() - duration('PT1H')
WITH user, collect(product) as recent_views

-- Find similar products
UNWIND recent_views as viewed_product
MATCH (viewed_product)-[:BELONGS_TO]->(category:Category)<-[:BELONGS_TO]-(similar:Product)
WHERE NOT (user)-[:PURCHASED]->(similar)
WITH similar, count(*) as similarity_score
ORDER BY similarity_score DESC
LIMIT 5
RETURN similar.name, similarity_score
```

### 66. Build a network security monitoring system
**Answer**: Model network topology and detect security threats.

```cypher
-- Network topology model
CREATE (server1:Server {ip: '192.168.1.10', role: 'web'})
CREATE (firewall:Firewall {ip: '192.168.1.1'})
CREATE (user:User {ip: '192.168.1.100'})

CREATE (user)-[:CONNECTS_TO {port: 80, protocol: 'HTTP'}]->(firewall)
CREATE (firewall)-[:FORWARDS_TO {port: 8080}]->(server1)

-- Port scanning detection
MATCH (source)-[conn:CONNECTS_TO]->(target)
WHERE conn.timestamp > datetime() - duration('PT5M')
WITH source, target, count(DISTINCT conn.port) as unique_ports
WHERE unique_ports > 10
RETURN source.ip, target.ip, unique_ports
```

### 67. Create a content management workflow system
**Answer**: Model content lifecycle and approval workflows.

```cypher
-- Content workflow model
CREATE (author:User {name: 'Alice', role: 'Author'})
CREATE (article:Content {id: 'A001', title: 'Neo4j Guide', status: 'Draft'})
CREATE (step1:WorkflowStep {name: 'Draft', order: 1})
CREATE (step2:WorkflowStep {name: 'Review', order: 2})
CREATE (step3:WorkflowStep {name: 'Published', order: 3})

CREATE (step1)-[:NEXT_STEP]->(step2)
CREATE (step2)-[:NEXT_STEP]->(step3)
CREATE (author)-[:CREATED]->(article)
CREATE (article)-[:IN_STEP]->(step1)
```

### 68. Design a financial portfolio risk analysis system
**Answer**: Model financial instruments and calculate risk exposure.

```cypher
-- Portfolio model
CREATE (portfolio:Portfolio {id: 'P001', name: 'Growth Portfolio'})
CREATE (stock1:Stock {symbol: 'AAPL', sector: 'Technology', price: 150.00})
CREATE (bond1:Bond {symbol: 'US10Y', rating: 'AAA', yield: 0.025})

CREATE (portfolio)-[:HOLDS {quantity: 100, weight: 0.4}]->(stock1)
CREATE (portfolio)-[:HOLDS {quantity: 1000, weight: 0.2}]->(bond1)

-- Sector concentration risk
MATCH (portfolio:Portfolio {id: 'P001'})-[h:HOLDS]->(asset)
WHERE exists(asset.sector)
WITH portfolio, asset.sector as sector, sum(h.weight) as sector_weight
WHERE sector_weight > 0.3
RETURN portfolio.name, sector, sector_weight
```

### 69. Build a logistics optimization system
**Answer**: Model transportation networks and optimize routes.

```cypher
-- Logistics network model
CREATE (warehouse:Warehouse {id: 'W001', city: 'New York', capacity: 10000})
CREATE (store1:Store {id: 'S001', city: 'Boston', demand: 500})
CREATE (truck:Vehicle {id: 'T001', capacity: 1000, cost_per_mile: 2.5})

CREATE (warehouse)-[:ROUTE {distance: 200, time: 4}]->(store1)

-- Optimal delivery route
MATCH path = (start:Warehouse)-[:ROUTE*1..3]->(end:Store)
WITH path, 
     reduce(total_distance = 0, rel in relationships(path) | total_distance + rel.distance) as total_distance
RETURN path, total_distance
ORDER BY total_distance
LIMIT 5
```

### 70. Create a healthcare patient journey system
**Answer**: Model patient interactions and treatment pathways.

```cypher
-- Healthcare model
CREATE (patient:Patient {id: 'P001', age: 45, gender: 'M'})
CREATE (doctor1:Doctor {id: 'D001', specialty: 'Cardiology'})
CREATE (visit1:Visit {date: date('2023-01-15'), type: 'Consultation'})
CREATE (treatment:Treatment {name: 'Medication', duration: 30})

CREATE (patient)-[:HAD_VISIT]->(visit1)
CREATE (visit1)-[:WITH_DOCTOR]->(doctor1)
CREATE (visit1)-[:RESULTED_IN]->(treatment)

-- Patient journey analysis
MATCH path = (patient:Patient)-[:HAD_VISIT*1..5]->(visit:Visit)
WITH patient, path, length(path) as journey_length
RETURN patient.id, journey_length
ORDER BY journey_length DESC
```

### 71. How do you implement graph-based machine learning feature engineering?
**Answer**: Extract graph features for ML models using centrality and community metrics.

```cypher
-- Create graph projection for ML
CALL gds.graph.project(
  'ml-features',
  ['Person', 'Company', 'Product'],
  ['KNOWS', 'WORKS_FOR', 'PURCHASED']
)

-- Calculate multiple centrality measures
CALL gds.degree.mutate('ml-features', {mutateProperty: 'degree'})
CALL gds.pageRank.mutate('ml-features', {mutateProperty: 'pagerank'})
CALL gds.betweenness.mutate('ml-features', {mutateProperty: 'betweenness'})
CALL gds.closeness.mutate('ml-features', {mutateProperty: 'closeness'})

-- Community detection
CALL gds.louvain.mutate('ml-features', {mutateProperty: 'community'})

-- Export features for ML
CALL gds.graph.nodeProperties.stream('ml-features', ['degree', 'pagerank', 'betweenness', 'closeness', 'community'])
YIELD nodeId, propertyName, propertyValue
RETURN gds.util.asNode(nodeId).id as node_id, propertyName, propertyValue
```

### 72. How do you implement graph-based recommendation systems?
**Answer**: Build collaborative filtering using graph traversals and similarity metrics.

```cypher
-- Content-based recommendations
MATCH (user:User {id: 'U001'})-[:PURCHASED]->(item:Product)-[:BELONGS_TO]->(category:Category)
WITH user, collect(DISTINCT category) as user_categories
MATCH (similar_item:Product)-[:BELONGS_TO]->(cat:Category)
WHERE cat IN user_categories AND NOT (user)-[:PURCHASED]->(similar_item)
WITH similar_item, count(cat) as category_overlap
RETURN similar_item.name, category_overlap
ORDER BY category_overlap DESC
LIMIT 10

-- Collaborative filtering
MATCH (target:User {id: 'U001'})-[:PURCHASED]->(item:Product)<-[:PURCHASED]-(similar:User)
WHERE target <> similar
WITH target, similar, count(item) as shared_items
WHERE shared_items >= 3
MATCH (similar)-[:PURCHASED]->(rec:Product)
WHERE NOT (target)-[:PURCHASED]->(rec)
RETURN rec.name, count(*) as recommendation_score
ORDER BY recommendation_score DESC
LIMIT 10
```

### 73. How do you implement graph-based anomaly detection?
**Answer**: Detect unusual patterns and outliers in graph structures.

```cypher
-- Detect unusual connection patterns
MATCH (account:Account)-[t:TRANSFER]->(other:Account)
WITH account, count(t) as transfer_count, collect(other) as connected_accounts
WHERE transfer_count > 100
WITH account, transfer_count, 
     size([acc IN connected_accounts WHERE size((acc)-[:TRANSFER]->()) < 5]) as suspicious_targets
WHERE suspicious_targets > transfer_count * 0.8
RETURN account.id, transfer_count, suspicious_targets

-- Detect circular transaction patterns
MATCH path = (start:Account)-[:TRANSFER*3..6]->(start)
WHERE all(rel IN relationships(path) WHERE rel.amount > 10000)
  AND all(rel IN relationships(path) WHERE rel.timestamp > datetime() - duration('P7D'))
RETURN path, 
       reduce(total = 0, rel IN relationships(path) | total + rel.amount) as total_amount
ORDER BY total_amount DESC
```

### 74. How do you implement graph-based data lineage tracking?
**Answer**: Model and track data flow through systems and transformations.

```cypher
-- Data lineage model
CREATE (source:Dataset {name: 'raw_sales', type: 'source'})
CREATE (etl1:Process {name: 'clean_sales', type: 'transformation'})
CREATE (etl2:Process {name: 'aggregate_sales', type: 'transformation'})
CREATE (target:Dataset {name: 'sales_summary', type: 'target'})

CREATE (source)-[:FEEDS_INTO {timestamp: datetime()}]->(etl1)
CREATE (etl1)-[:PRODUCES {timestamp: datetime()}]->(target)
CREATE (etl1)-[:FEEDS_INTO {timestamp: datetime()}]->(etl2)
CREATE (etl2)-[:PRODUCES {timestamp: datetime()}]->(target)

-- Impact analysis
MATCH path = (source:Dataset {name: 'raw_sales'})-[:FEEDS_INTO|PRODUCES*]->(downstream)
RETURN downstream.name, length(path) as impact_distance
ORDER BY impact_distance

-- Root cause analysis
MATCH path = (upstream)-[:FEEDS_INTO|PRODUCES*]->(target:Dataset {name: 'sales_summary'})
RETURN upstream.name, length(path) as dependency_distance
ORDER BY dependency_distance DESC
```

### 75. How do you implement graph-based access control and permissions?
**Answer**: Model complex permission hierarchies and inheritance.

```cypher
-- Permission model
CREATE (user:User {name: 'alice', department: 'finance'})
CREATE (role:Role {name: 'analyst', level: 'standard'})
CREATE (resource:Resource {name: 'financial_reports', classification: 'confidential'})
CREATE (permission:Permission {action: 'read', granted_by: 'admin'})

CREATE (user)-[:HAS_ROLE]->(role)
CREATE (role)-[:HAS_PERMISSION]->(permission)
CREATE (permission)-[:APPLIES_TO]->(resource)

-- Check user permissions
MATCH (user:User {name: 'alice'})-[:HAS_ROLE*1..3]->(role:Role)-[:HAS_PERMISSION]->(perm:Permission)-[:APPLIES_TO]->(resource:Resource)
WHERE resource.name = 'financial_reports' AND perm.action = 'read'
RETURN count(perm) > 0 as has_access

-- Permission inheritance
MATCH (parent_role:Role)-[:INHERITS_FROM]->(child_role:Role)
MATCH (child_role)-[:HAS_PERMISSION]->(perm:Permission)
CREATE (parent_role)-[:HAS_PERMISSION]->(perm)
```

### 76-100. Additional Advanced Topics:

**76. Graph-based event sourcing patterns**
**77. Temporal graph analysis and time-based queries**
**78. Graph-based microservices architecture**
**79. Multi-dimensional graph modeling**
**80. Graph-based configuration management**
**81. Dynamic graph schema evolution**
**82. Graph-based workflow orchestration**
**83. Distributed graph processing patterns**
**84. Graph-based caching strategies**
**85. Real-time graph stream processing**
**86. Graph-based A/B testing frameworks**
**87. Multi-tenant graph architectures**
**88. Graph-based feature flags and toggles**
**89. Cross-platform graph synchronization**
**90. Graph-based audit and compliance tracking**
**91. Performance optimization for large graphs**
**92. Graph-based machine learning pipelines**
**93. Advanced graph visualization techniques**
**94. Graph-based natural language processing**
**95. Blockchain and cryptocurrency analysis**
**96. Graph-based IoT device management**
**97. Social network influence analysis**
**98. Graph-based recommendation engines**
**99. Advanced graph algorithms implementation**
**100. Future trends in graph database technology**

---

**Total Questions: 100** | **Coverage: Complete Neo4j Ecosystem for Data Engineering**
```
