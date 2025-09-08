# Database Types - Interview Questions

## 1. What are the different types of databases and when would you use each?

**Answer:**
Database types serve different use cases based on data structure, scalability, and consistency requirements.

**Relational Databases (RDBMS):**
- **Use cases**: ACID transactions, complex relationships, structured data
- **Examples**: PostgreSQL, MySQL, Oracle
- **When to use**: Financial systems, ERP, traditional applications

**Key-Value Stores:**
- **Use cases**: Caching, session storage, simple lookups
- **Examples**: Redis, DynamoDB, Riak
- **When to use**: High-performance caching, user sessions

**Document Databases:**
- **Use cases**: Flexible schema, JSON-like data, content management
- **Examples**: MongoDB, CouchDB, Amazon DocumentDB
- **When to use**: Content management, catalogs, user profiles

**Column-Family:**
- **Use cases**: Time-series data, analytics, wide tables
- **Examples**: Cassandra, HBase, Amazon Timestream
- **When to use**: IoT data, analytics, logging

**Graph Databases:**
- **Use cases**: Relationships, social networks, recommendations
- **Examples**: Neo4j, Amazon Neptune, ArangoDB
- **When to use**: Social networks, fraud detection, recommendations

**Time-Series Databases:**
- **Use cases**: Time-stamped data, monitoring, IoT
- **Examples**: InfluxDB, TimescaleDB, Prometheus
- **When to use**: Monitoring systems, IoT applications, financial data

## 2. How do you choose between SQL and NoSQL databases?

**Answer:**
Choose based on data structure, scalability needs, and consistency requirements.

**Choose SQL when:**
- ACID compliance is critical
- Complex relationships exist
- Data structure is well-defined
- Strong consistency required

**Choose NoSQL when:**
- Horizontal scaling needed
- Flexible schema required
- High availability prioritized
- Eventual consistency acceptable

**Decision Matrix:**
```
Requirement          | SQL    | NoSQL
---------------------|--------|-------
ACID Transactions    | ✓      | Limited
Horizontal Scaling   | Limited| ✓
Schema Flexibility   | Limited| ✓
Complex Queries      | ✓      | Limited
Consistency          | Strong | Eventual
```