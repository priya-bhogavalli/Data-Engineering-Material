# Amazon Neptune - Key Concepts

## Overview
Amazon Neptune is a fully managed graph database service that supports both property graph and RDF graph models with Apache TinkerPop Gremlin and SPARQL query languages.

## Core Concepts

### Graph Database Fundamentals
- **Vertices (Nodes)**: Entities in the graph
- **Edges (Relationships)**: Connections between vertices
- **Properties**: Key-value pairs attached to vertices and edges

### Neptune Architecture
- **Cluster**: Contains primary and read replica instances
- **Primary Instance**: Handles write operations
- **Read Replicas**: Handle read operations (up to 15 replicas)
- **Storage**: Automatically scales up to 128 TB

### Query Languages
- **Gremlin**: Apache TinkerPop graph traversal language
- **SPARQL**: W3C standard for RDF graphs
- **openCypher**: Property graph query language (read-only)

### Data Models
- **Property Graph**: Vertices and edges with properties
- **RDF**: Resource Description Framework for semantic data

### Security Features
- VPC isolation
- Encryption at rest and in transit
- IAM authentication
- Database activity streams

### Performance Features
- Multi-AZ deployment
- Automatic failover
- Point-in-time recovery
- Continuous backup to S3

## Use Cases
- Social networks
- Recommendation engines
- Fraud detection
- Knowledge graphs
- Network and IT operations