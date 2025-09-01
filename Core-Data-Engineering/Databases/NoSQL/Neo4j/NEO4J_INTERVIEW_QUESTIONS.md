# Neo4j (NoSQL) - Interview Questions

## Basic Questions

### 1. What is Neo4j and when would you use a graph database?
**Answer:** Neo4j is a native graph database that stores data as nodes and relationships. Use graph databases when:
- Data has complex relationships (social networks, fraud detection)
- Need to traverse connections efficiently
- Relationships are as important as the data itself
- Traditional joins become complex and slow
- Pattern matching is required (recommendation engines)

### 2. Explain the basic components of Neo4j's graph model.
**Answer:** Neo4j's graph model consists of:
- **Nodes**: Entities with labels and properties
- **Relationships**: Directed connections with types and properties
- **Properties**: Key-value pairs on nodes and relationships
- **Labels**: Categories for grouping nodes (e.g., :Person, :Company)
- **Types**: Categories for relationships (e.g., :WORKS_FOR, :KNOWS)

### 3. What is Cypher and how does it differ from SQL?
**Answer:** Cypher is Neo4j's declarative query language designed for graphs:
- **Pattern matching**: Uses ASCII art patterns `(a)-[:KNOWS]->(b)`
- **Graph-focused**: Optimized for traversing relationships
- **Visual**: Intuitive representation of graph patterns
- **Declarative**: Specify what you want, not how to get it

## Intermediate Questions

### 4. How do you model a social network in Neo4j?
**Answer:**
```cypher
// Create users
CREATE (alice:Person {name: 'Alice', age: 30})
CREATE (bob:Person {name: 'Bob', age: 25})

// Create friendship
CREATE (alice)-[:FRIENDS_WITH {since: '2020-01-01'}]->(bob)

// Find friends of friends
MATCH (person:Person {name: 'Alice'})-[:FRIENDS_WITH]->(friend)-[:FRIENDS_WITH]->(fof)
WHERE fof <> person
RETURN fof.name
```

### 5. What are the different types of indexes in Neo4j?
**Answer:** Neo4j supports several index types:
- **Node indexes**: Speed up node lookups by properties
- **Relationship indexes**: Index relationship properties
- **Composite indexes**: Multi-property indexes
- **Full-text indexes**: Text search with Lucene
- **Vector indexes**: Similarity search for embeddings

### 6. How does Neo4j handle ACID transactions?
**Answer:** Neo4j provides full ACID compliance:
- **Atomicity**: All operations in transaction succeed or fail together
- **Consistency**: Database remains in valid state
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed changes persist through failures

## Advanced Questions

### 7. How would you implement a recommendation engine using Neo4j?
**Answer:**
```cypher
// Collaborative filtering - find similar users
MATCH (user:Person {name: 'Alice'})-[:LIKES]->(item)<-[:LIKES]-(similar:Person)
WHERE user <> similar
WITH similar, COUNT(item) as commonLikes
ORDER BY commonLikes DESC
LIMIT 10

// Content-based recommendations
MATCH (user:Person {name: 'Alice'})-[:LIKES]->(liked:Product)-[:CATEGORY]->(cat:Category)
MATCH (cat)<-[:CATEGORY]-(recommended:Product)
WHERE NOT (user)-[:LIKES]->(recommended)
RETURN recommended.name, COUNT(cat) as score
ORDER BY score DESC
```

### 8. What are the performance considerations for Neo4j?
**Answer:** Key performance factors:
- **Query design**: Avoid Cartesian products, use specific patterns
- **Indexing**: Create indexes for frequently queried properties
- **Data modeling**: Design schema to match query patterns
- **Memory**: Sufficient heap and page cache
- **Query profiling**: Use PROFILE and EXPLAIN
- **Batch operations**: Use UNWIND for bulk operations

### 9. How does Neo4j clustering work?
**Answer:** Neo4j Enterprise clustering features:
- **Causal Clustering**: Core servers handle writes, read replicas scale reads
- **Raft Protocol**: Consensus algorithm for consistency
- **Leader Election**: Automatic failover for high availability
- **Read Routing**: Distribute read queries across replicas
- **Bookmarks**: Ensure read-after-write consistency

### 10. What are the limitations of Neo4j?
**Answer:** Neo4j limitations include:
- **Memory requirements**: Graph must fit in memory for optimal performance
- **Analytical queries**: Not optimized for complex aggregations
- **Bulk operations**: Slower than specialized bulk loading systems
- **Licensing**: Advanced features require Enterprise license
- **Learning curve**: Different paradigm from relational databases
- **Ecosystem**: Smaller ecosystem compared to relational databases