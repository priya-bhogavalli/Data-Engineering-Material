# Neo4j (NoSQL) - Key Concepts

## Overview
Neo4j is a native graph database that stores data as nodes and relationships, optimized for traversing connected data with the Cypher query language.

## Graph Data Model

### Core Components
- **Nodes**: Entities in the graph (people, places, things)
- **Relationships**: Connections between nodes with direction
- **Properties**: Key-value pairs on nodes and relationships
- **Labels**: Categories for grouping nodes
- **Types**: Categories for relationships

### Graph Structure
- **Property Graph**: Nodes and relationships with properties
- **Schema-optional**: Flexible data modeling
- **ACID Transactions**: Full transaction support
- **Index-free Adjacency**: Direct pointer navigation

## Cypher Query Language

### Basic Syntax
- **Nodes**: `(n:Label {property: 'value'})`
- **Relationships**: `-[:TYPE]->`
- **Patterns**: `(a)-[:KNOWS]->(b)`
- **Variables**: Bind graph elements to variables

### Common Operations
- **CREATE**: Add nodes and relationships
- **MATCH**: Find patterns in the graph
- **WHERE**: Filter results
- **RETURN**: Specify output
- **DELETE**: Remove nodes and relationships

## Performance Features

### Indexing
- **Node Indexes**: Speed up node lookups
- **Relationship Indexes**: Index relationship properties
- **Composite Indexes**: Multi-property indexes
- **Full-text Indexes**: Text search capabilities

### Query Optimization
- **Query Planner**: Cost-based query optimization
- **Query Cache**: Cache compiled queries
- **Statistics**: Maintain graph statistics
- **Hints**: Manual query optimization

## Scalability Options

### Clustering (Enterprise)
- **Causal Clustering**: Read replicas with eventual consistency
- **Core Servers**: Handle writes and maintain consensus
- **Read Replicas**: Scale read operations
- **Load Balancing**: Distribute read queries

### Fabric (Enterprise)
- **Sharding**: Distribute data across databases
- **Federation**: Query across multiple databases
- **Routing**: Intelligent query routing
- **Composite Databases**: Virtual database views

## Use Cases
- **Social Networks**: Friend connections and recommendations
- **Fraud Detection**: Pattern analysis in financial transactions
- **Recommendation Engines**: Product and content recommendations
- **Knowledge Graphs**: Semantic data relationships
- **Network Management**: IT infrastructure mapping