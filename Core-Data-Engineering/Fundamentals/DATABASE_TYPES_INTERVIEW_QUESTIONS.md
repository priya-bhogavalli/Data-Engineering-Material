# Database Types Interview Questions

## 🎯 **Core Database Categories**

### Q1: What are the main types of databases and their use cases?

**Answer:**
1. **Relational Databases (RDBMS)**
   - Examples: PostgreSQL, MySQL, Oracle, SQL Server
   - Use Cases: Transactional systems, structured data, ACID compliance
   - Strengths: Data consistency, complex queries, mature ecosystem

2. **NoSQL Databases**
   - Document: MongoDB, CouchDB
   - Key-Value: Redis, DynamoDB
   - Column-Family: Cassandra, HBase
   - Graph: Neo4j, Amazon Neptune
   - Use Cases: Scalability, flexible schemas, specific data models

3. **NewSQL Databases**
   - Examples: CockroachDB, TiDB, VoltDB
   - Use Cases: ACID compliance with horizontal scalability

4. **Specialized Databases**
   - Time-Series: InfluxDB, TimescaleDB
   - Search: Elasticsearch, Solr
   - In-Memory: Redis, Memcached

### Q2: When would you choose a relational database over NoSQL?

**Answer:**
**Choose Relational when:**
- Strong consistency requirements (ACID properties)
- Complex relationships between entities
- Well-defined, stable schema
- Complex queries with joins
- Regulatory compliance requirements
- Mature tooling and expertise available

**Example Use Cases:**
- Financial transactions
- E-commerce order management
- HR management systems
- Inventory management

## 📊 **NoSQL Database Types**

### Q3: Explain the different types of NoSQL databases with examples

**Answer:**

**Document Databases:**
```javascript
// MongoDB example
{
  "_id": "user123",
  "name": "John Doe",
  "email": "john@example.com",
  "addresses": [
    {
      "type": "home",
      "street": "123 Main St",
      "city": "Anytown"
    }
  ],
  "preferences": {
    "theme": "dark",
    "notifications": true
  }
}
```
- **Best For**: Content management, catalogs, user profiles
- **Strengths**: Flexible schema, natural data representation
- **Examples**: MongoDB, CouchDB, Amazon DocumentDB

**Key-Value Stores:**
```python
# Redis example
SET user:123:name "John Doe"
SET user:123:email "john@example.com"
HSET user:123:preferences theme dark notifications true
```
- **Best For**: Caching, session storage, real-time recommendations
- **Strengths**: High performance, simple model
- **Examples**: Redis, DynamoDB, Riak

**Column-Family:**
```sql
-- Cassandra example
CREATE TABLE user_activity (
    user_id UUID,
    timestamp TIMESTAMP,
    activity_type TEXT,
    details MAP<TEXT, TEXT>,
    PRIMARY KEY (user_id, timestamp)
);
```
- **Best For**: Time-series data, IoT, analytics
- **Strengths**: High write throughput, compression
- **Examples**: Cassandra, HBase, Amazon SimpleDB

**Graph Databases:**
```cypher
// Neo4j example
CREATE (john:Person {name: 'John Doe', age: 30})
CREATE (jane:Person {name: 'Jane Smith', age: 28})
CREATE (company:Company {name: 'Tech Corp'})
CREATE (john)-[:WORKS_FOR]->(company)
CREATE (jane)-[:WORKS_FOR]->(company)
CREATE (john)-[:KNOWS]->(jane)
```
- **Best For**: Social networks, recommendations, fraud detection
- **Strengths**: Relationship queries, pattern matching
- **Examples**: Neo4j, Amazon Neptune, ArangoDB

### Q4: What is the CAP theorem and how does it affect database choice?

**Answer:**
**CAP Theorem states you can only guarantee 2 of 3:**
- **Consistency**: All nodes see the same data simultaneously
- **Availability**: System remains operational
- **Partition Tolerance**: System continues despite network failures

**Database Classifications:**
- **CP Systems**: MongoDB, HBase, Redis (prioritize consistency)
- **AP Systems**: Cassandra, DynamoDB, CouchDB (prioritize availability)
- **CA Systems**: Traditional RDBMS in single-node scenarios

**Practical Implications:**
```python
# Example: Choosing based on CAP requirements

# High consistency requirement (financial transactions)
# Choose CP system like MongoDB with strong consistency
client = MongoClient()
db = client.banking
collection = db.transactions

# High availability requirement (social media feed)
# Choose AP system like Cassandra
from cassandra.cluster import Cluster
cluster = Cluster(['127.0.0.1'])
session = cluster.connect('social_media')
```

## 🔍 **Specialized Database Types**

### Q5: When would you use a time-series database?

**Answer:**
**Use Time-Series DB when:**
- Data points are timestamped
- High write volume with time-ordered data
- Need time-based aggregations and analytics
- Retention policies based on time

**Examples:**
```sql
-- InfluxDB example
SELECT MEAN(cpu_usage) 
FROM system_metrics 
WHERE time >= now() - 1h 
GROUP BY time(5m), host
```

**Use Cases:**
- IoT sensor data
- Application performance monitoring
- Financial market data
- System metrics and logs

**Popular Options:**
- **InfluxDB**: Purpose-built time-series database
- **TimescaleDB**: PostgreSQL extension for time-series
- **Prometheus**: Monitoring-focused time-series DB

### Q6: What are the advantages of in-memory databases?

**Answer:**
**Advantages:**
- Ultra-low latency (microseconds vs milliseconds)
- High throughput for read/write operations
- Real-time analytics capabilities
- Simplified data structures

**Use Cases:**
```python
# Redis for caching
import redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Cache frequently accessed data
r.setex('user:123:profile', 3600, json.dumps(user_data))

# Real-time counters
r.incr('page_views:today')

# Session storage
r.hset('session:abc123', mapping={
    'user_id': '123',
    'login_time': '2023-01-01T10:00:00Z'
})
```

**Limitations:**
- Data volatility (lost on restart without persistence)
- Memory cost higher than disk storage
- Limited by available RAM

### Q7: How do search databases differ from traditional databases?

**Answer:**
**Search Databases (Elasticsearch, Solr):**
- Optimized for full-text search and analytics
- Inverted index data structures
- Relevance scoring and ranking
- Faceted search capabilities

**Example:**
```python
# Elasticsearch query
from elasticsearch import Elasticsearch

es = Elasticsearch()

# Full-text search with filters
query = {
    "query": {
        "bool": {
            "must": [
                {"match": {"title": "data engineering"}},
                {"range": {"publish_date": {"gte": "2023-01-01"}}}
            ],
            "filter": [
                {"term": {"category": "technology"}}
            ]
        }
    },
    "aggs": {
        "authors": {
            "terms": {"field": "author.keyword"}
        }
    }
}

result = es.search(index="articles", body=query)
```

**Use Cases:**
- E-commerce product search
- Log analysis and monitoring
- Content management systems
- Business intelligence dashboards

## 🏗️ **Database Selection Criteria**

### Q8: What factors should you consider when choosing a database?

**Answer:**
**Technical Factors:**
1. **Data Model**: Structured vs unstructured
2. **Scalability**: Vertical vs horizontal scaling needs
3. **Consistency**: ACID vs eventual consistency
4. **Performance**: Read vs write heavy workloads
5. **Query Complexity**: Simple lookups vs complex analytics

**Business Factors:**
1. **Team Expertise**: Available skills and training needs
2. **Cost**: Licensing, infrastructure, operational costs
3. **Vendor Lock-in**: Open source vs proprietary solutions
4. **Compliance**: Regulatory and security requirements
5. **Ecosystem**: Tool integration and community support

**Decision Matrix Example:**
```python
# Database selection scoring
criteria = {
    'consistency': {'weight': 0.3, 'postgresql': 9, 'mongodb': 7, 'cassandra': 5},
    'scalability': {'weight': 0.25, 'postgresql': 6, 'mongodb': 8, 'cassandra': 9},
    'performance': {'weight': 0.2, 'postgresql': 7, 'mongodb': 8, 'cassandra': 9},
    'complexity': {'weight': 0.15, 'postgresql': 8, 'mongodb': 7, 'cassandra': 5},
    'cost': {'weight': 0.1, 'postgresql': 9, 'mongodb': 7, 'cassandra': 8}
}

def calculate_score(db_name):
    total_score = 0
    for criterion, data in criteria.items():
        total_score += data['weight'] * data[db_name]
    return total_score

# Calculate scores
scores = {db: calculate_score(db) for db in ['postgresql', 'mongodb', 'cassandra']}
print(scores)  # {'postgresql': 7.65, 'mongodb': 7.4, 'cassandra': 7.1}
```

### Q9: How do you handle polyglot persistence?

**Answer:**
**Polyglot Persistence**: Using different databases for different parts of an application based on data characteristics and access patterns.

**Example Architecture:**
```python
# E-commerce platform with polyglot persistence

# User profiles and orders (RDBMS for consistency)
class UserService:
    def __init__(self):
        self.db = PostgreSQLConnection()
    
    def create_order(self, user_id, items):
        # ACID transaction for financial data
        with self.db.transaction():
            order = self.db.create_order(user_id, items)
            self.db.update_inventory(items)
            return order

# Product catalog (Document DB for flexibility)
class CatalogService:
    def __init__(self):
        self.db = MongoDBConnection()
    
    def search_products(self, query):
        return self.db.products.find({
            "$text": {"$search": query}
        })

# Session data (Key-Value for speed)
class SessionService:
    def __init__(self):
        self.cache = RedisConnection()
    
    def store_session(self, session_id, data):
        self.cache.setex(session_id, 3600, json.dumps(data))

# Analytics (Column store for aggregations)
class AnalyticsService:
    def __init__(self):
        self.db = CassandraConnection()
    
    def track_event(self, user_id, event_type, timestamp):
        self.db.execute("""
            INSERT INTO user_events (user_id, event_type, timestamp)
            VALUES (?, ?, ?)
        """, (user_id, event_type, timestamp))
```

**Benefits:**
- Optimal performance for each use case
- Technology flexibility
- Reduced vendor lock-in

**Challenges:**
- Increased complexity
- Data consistency across systems
- Operational overhead

## 📈 **Performance and Scaling**

### Q10: How do different database types handle scaling?

**Answer:**

**Vertical Scaling (Scale Up):**
- Add more CPU, RAM, or storage to existing server
- Suitable for: RDBMS, single-node systems
- Limitations: Hardware limits, single point of failure

**Horizontal Scaling (Scale Out):**
- Add more servers to distribute load
- Suitable for: NoSQL databases, distributed systems

**Scaling Strategies by Database Type:**

**RDBMS Scaling:**
```sql
-- Read replicas for read scaling
-- Master-slave replication
CREATE REPLICA replica1 FROM master_db;

-- Sharding for write scaling
-- Partition data across multiple databases
SELECT * FROM users_shard_1 WHERE user_id BETWEEN 1 AND 1000000;
SELECT * FROM users_shard_2 WHERE user_id BETWEEN 1000001 AND 2000000;
```

**NoSQL Scaling:**
```python
# Cassandra automatic sharding
# Data automatically distributed across nodes
CREATE KEYSPACE ecommerce 
WITH REPLICATION = {
    'class': 'SimpleStrategy',
    'replication_factor': 3
};

# MongoDB sharding
# Shard key determines data distribution
sh.shardCollection("ecommerce.products", {"category": 1})
```

### Q11: What are the trade-offs between consistency models?

**Answer:**

**Strong Consistency:**
- All reads receive the most recent write
- Higher latency, lower availability
- Examples: RDBMS, MongoDB (default)

**Eventual Consistency:**
- System will become consistent over time
- Higher availability, lower latency
- Examples: Cassandra, DynamoDB

**Weak Consistency:**
- No guarantees about when data will be consistent
- Highest performance
- Examples: Memcached, some caching systems

**Implementation Examples:**
```python
# Strong consistency (MongoDB)
client = MongoClient()
db = client.ecommerce
collection = db.products

# Write with majority acknowledgment
result = collection.insert_one(
    {"name": "Product A", "price": 100},
    write_concern=WriteConcern(w="majority")
)

# Read from primary
product = collection.find_one(
    {"_id": result.inserted_id},
    read_preference=ReadPreference.PRIMARY
)

# Eventual consistency (Cassandra)
from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy

cluster = Cluster(
    load_balancing_policy=DCAwareRoundRobinPolicy()
)
session = cluster.connect('ecommerce')

# Write with eventual consistency
session.execute("""
    INSERT INTO products (id, name, price)
    VALUES (uuid(), 'Product A', 100)
    USING CONSISTENCY QUORUM
""")
```

## 🔧 **Integration Patterns**

### Q12: How do you integrate multiple database types in a data pipeline?

**Answer:**

**Common Integration Patterns:**

**1. Change Data Capture (CDC):**
```python
# Debezium CDC example
# Capture changes from PostgreSQL and stream to Kafka
{
    "name": "postgres-connector",
    "config": {
        "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
        "database.hostname": "localhost",
        "database.port": "5432",
        "database.user": "debezium",
        "database.password": "dbz",
        "database.dbname": "inventory",
        "database.server.name": "fulfillment",
        "table.whitelist": "public.orders,public.products"
    }
}
```

**2. ETL/ELT Pipelines:**
```python
# Apache Airflow DAG for multi-database ETL
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def extract_from_postgres():
    # Extract from RDBMS
    conn = psycopg2.connect(...)
    df = pd.read_sql("SELECT * FROM orders", conn)
    return df

def transform_data(df):
    # Transform data
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df.groupby('customer_id').agg({'amount': 'sum'})

def load_to_mongodb(df):
    # Load to document database
    client = MongoClient()
    db = client.analytics
    collection = db.customer_summary
    collection.insert_many(df.to_dict('records'))

dag = DAG('multi_db_etl', schedule_interval='@daily')

extract_task = PythonOperator(
    task_id='extract',
    python_callable=extract_from_postgres,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform',
    python_callable=transform_data,
    dag=dag
)

load_task = PythonOperator(
    task_id='load',
    python_callable=load_to_mongodb,
    dag=dag
)

extract_task >> transform_task >> load_task
```

**3. API-based Integration:**
```python
# Microservices with different databases
class OrderService:
    def __init__(self):
        self.db = PostgreSQLConnection()  # ACID for transactions
    
    def create_order(self, order_data):
        return self.db.orders.create(order_data)

class RecommendationService:
    def __init__(self):
        self.db = Neo4jConnection()  # Graph for relationships
    
    def get_recommendations(self, user_id):
        query = """
        MATCH (u:User {id: $user_id})-[:PURCHASED]->(p:Product)
        MATCH (p)<-[:PURCHASED]-(other:User)-[:PURCHASED]->(rec:Product)
        WHERE NOT (u)-[:PURCHASED]->(rec)
        RETURN rec.name, COUNT(*) as score
        ORDER BY score DESC LIMIT 10
        """
        return self.db.run(query, user_id=user_id)
```

---

## 🎯 **Key Decision Framework**

### Database Selection Checklist:

1. **Data Characteristics**
   - Structure: Structured/Semi-structured/Unstructured
   - Volume: Small/Medium/Large/Very Large
   - Velocity: Batch/Real-time/Streaming
   - Relationships: Simple/Complex/Graph-like

2. **Access Patterns**
   - Read/Write ratio
   - Query complexity
   - Consistency requirements
   - Latency requirements

3. **Operational Requirements**
   - Scalability needs
   - Availability requirements
   - Backup and recovery
   - Security and compliance

4. **Team and Organization**
   - Existing expertise
   - Learning curve
   - Operational complexity
   - Budget constraints

Choose the right database type based on your specific requirements rather than following trends or preferences.