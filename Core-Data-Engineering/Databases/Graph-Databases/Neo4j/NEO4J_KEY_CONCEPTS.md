# Neo4j Key Concepts

## 🎯 What is Neo4j?
Native graph database that stores data as nodes and relationships, optimized for traversing connected data.

## 🏗️ Graph Data Model

### Core Components
- **Node** - Entity (person, product, location)
- **Relationship** - Connection between nodes
- **Property** - Key-value pairs on nodes/relationships
- **Label** - Groups nodes by type

### Graph Structure
```cypher
// Nodes with labels and properties
(person:Person {name: "Alice", age: 30})
(company:Company {name: "TechCorp", founded: 2010})

// Relationships with types and properties
(person)-[:WORKS_FOR {since: 2020, role: "Engineer"}]->(company)
```

## 🔧 Cypher Query Language

### Basic Operations
```cypher
// Create nodes
CREATE (alice:Person {name: "Alice", age: 30})
CREATE (bob:Person {name: "Bob", age: 25})

// Create relationships
MATCH (a:Person {name: "Alice"}), (b:Person {name: "Bob"})
CREATE (a)-[:FRIENDS_WITH {since: 2020}]->(b)

// Read data
MATCH (p:Person)
RETURN p.name, p.age

// Update properties
MATCH (p:Person {name: "Alice"})
SET p.age = 31

// Delete nodes/relationships
MATCH (p:Person {name: "Alice"})-[r:FRIENDS_WITH]->()
DELETE r, p
```

### Pattern Matching
```cypher
// Find friends of friends
MATCH (person:Person {name: "Alice"})-[:FRIENDS_WITH]->(friend)-[:FRIENDS_WITH]->(fof)
RETURN fof.name

// Variable length paths
MATCH (start:Person {name: "Alice"})-[:FRIENDS_WITH*1..3]->(connected)
RETURN connected.name

// Shortest path
MATCH path = shortestPath((a:Person {name: "Alice"})-[*]-(b:Person {name: "Bob"}))
RETURN path
```

## 📊 Advanced Queries

### Aggregation
```cypher
// Count relationships
MATCH (p:Person)-[:WORKS_FOR]->(c:Company)
RETURN c.name, count(p) as employee_count
ORDER BY employee_count DESC

// Collect related data
MATCH (p:Person)-[:LIKES]->(product:Product)
RETURN p.name, collect(product.name) as liked_products
```

### Conditional Logic
```cypher
// CASE statements
MATCH (p:Person)
RETURN p.name,
  CASE
    WHEN p.age < 18 THEN "Minor"
    WHEN p.age < 65 THEN "Adult"
    ELSE "Senior"
  END as age_group
```

## 🚀 Performance Features

### Indexing
```cypher
// Create index
CREATE INDEX person_name FOR (p:Person) ON (p.name)

// Composite index
CREATE INDEX person_name_age FOR (p:Person) ON (p.name, p.age)

// Full-text index
CREATE FULLTEXT INDEX product_search FOR (p:Product) ON EACH [p.name, p.description]
```

### Query Optimization
```cypher
// Use PROFILE to analyze query performance
PROFILE MATCH (p:Person {name: "Alice"})-[:FRIENDS_WITH]->(friend)
RETURN friend.name

// Use EXPLAIN to see execution plan
EXPLAIN MATCH (p:Person)-[:WORKS_FOR]->(c:Company)
WHERE c.name = "TechCorp"
RETURN p.name
```

## 🔧 Python Integration

### Basic Operations
```python
from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def create_person(self, name, age):
        with self.driver.session() as session:
            session.run(
                "CREATE (p:Person {name: $name, age: $age})",
                name=name, age=age
            )
    
    def find_friends(self, name):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (p:Person {name: $name})-[:FRIENDS_WITH]->(friend) "
                "RETURN friend.name as name",
                name=name
            )
            return [record["name"] for record in result]

# Usage
conn = Neo4jConnection("bolt://localhost:7687", "neo4j", "password")
conn.create_person("Alice", 30)
friends = conn.find_friends("Alice")
```

### Batch Operations
```python
def create_social_network(conn, users, relationships):
    with conn.driver.session() as session:
        # Create users in batch
        session.run(
            "UNWIND $users as user "
            "CREATE (p:Person {name: user.name, age: user.age})",
            users=users
        )
        
        # Create relationships in batch
        session.run(
            "UNWIND $relationships as rel "
            "MATCH (a:Person {name: rel.from}), (b:Person {name: rel.to}) "
            "CREATE (a)-[:FRIENDS_WITH {since: rel.since}]->(b)",
            relationships=relationships
        )
```

## 🎯 Use Cases & Patterns

### Social Network Analysis
```cypher
// Find mutual friends
MATCH (person1:Person {name: "Alice"})-[:FRIENDS_WITH]->(mutual)<-[:FRIENDS_WITH]-(person2:Person {name: "Bob"})
RETURN mutual.name

// Recommend friends (friends of friends who aren't already friends)
MATCH (person:Person {name: "Alice"})-[:FRIENDS_WITH]->(friend)-[:FRIENDS_WITH]->(fof)
WHERE NOT (person)-[:FRIENDS_WITH]->(fof) AND person <> fof
RETURN fof.name, count(*) as mutual_friends
ORDER BY mutual_friends DESC
```

### Recommendation Engine
```cypher
// Product recommendations based on similar users
MATCH (user:Person {name: "Alice"})-[:PURCHASED]->(product)<-[:PURCHASED]-(similar)
MATCH (similar)-[:PURCHASED]->(recommendation)
WHERE NOT (user)-[:PURCHASED]->(recommendation)
RETURN recommendation.name, count(*) as score
ORDER BY score DESC
LIMIT 5
```

### Fraud Detection
```cypher
// Detect suspicious patterns
MATCH (account1:Account)-[:TRANSFER]->(account2:Account)-[:TRANSFER]->(account3:Account)
WHERE account1 <> account3
AND duration.between(account1.created, account3.created).days < 1
RETURN account1.id, account2.id, account3.id
```

## 🔒 Best Practices

### Data Modeling
- Use meaningful labels and relationship types
- Store frequently queried properties on nodes
- Avoid deep hierarchies
- Use appropriate data types

### Performance
- Create indexes for frequently queried properties
- Use parameters in queries to enable query caching
- Limit result sets with LIMIT clause
- Profile and optimize slow queries

### Operations
- Regular backups and monitoring
- Implement proper security measures
- Use connection pooling
- Monitor memory usage and garbage collection

## 🎯 Common Use Cases
- Social networks and recommendations
- Fraud detection and risk analysis
- Knowledge graphs and semantic search
- Network and IT operations
- Supply chain and logistics
- Master data management

## ⚠️ Considerations
- Memory requirements for large graphs
- Complex query optimization needed
- Learning curve for Cypher language
- Scaling limitations for write-heavy workloads