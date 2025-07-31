# Database Technologies Overview

## 🗄️ Database Categories

### 1. Relational Databases (RDBMS)
**ACID compliant, structured data with relationships**
- [PostgreSQL](./PostgreSQL/) - Advanced open-source RDBMS
- [MySQL](./MySQL/) - Popular open-source database
- [Oracle](./Oracle/) - Enterprise-grade commercial database
- [MS SQL Server](./MS-SQL-Server/) - Microsoft's relational database
- [Athena](./Athena/) - AWS serverless query service

### 2. NoSQL Databases
**Flexible schema, horizontal scaling**

#### Document Stores
- [MongoDB](./NoSQL/MongoDB/) - JSON-like document database
- [CouchDB](./NoSQL/CouchDB/) - Multi-master document database

#### Key-Value Stores
- [Redis](./NoSQL/Redis/) - In-memory data structure store
- [DynamoDB](./NoSQL/DynamoDB/) - AWS managed NoSQL database

#### Column-Family
- [Cassandra](./NoSQL/Cassandra/) - Distributed wide-column database
- [HBase](./NoSQL/HBase/) - Hadoop-based column database

#### Graph Databases
- [Neo4j](./Graph-Databases/Neo4j/) - Native graph database
- [Amazon Neptune](./Graph-Databases/Amazon-Neptune/) - AWS managed graph database

### 3. Time-Series Databases
**Optimized for time-stamped data**
- [InfluxDB](./Time-Series/InfluxDB/) - Purpose-built time-series database
- [TimescaleDB](./Time-Series/TimescaleDB/) - PostgreSQL extension for time-series

### 4. Search Engines
**Full-text search and analytics**
- [Elasticsearch](./Search-Engines/Elasticsearch/) - Distributed search and analytics
- [Apache Solr](./Search-Engines/Solr/) - Enterprise search platform

### 5. In-Memory Databases
**High-performance data processing**
- [Redis](./In-Memory/Redis/) - In-memory data structure store
- [Memcached](./In-Memory/Memcached/) - Distributed memory caching

### 6. NewSQL Databases
**ACID compliance with NoSQL scalability**
- [CockroachDB](./NewSQL/CockroachDB/) - Distributed SQL database
- [TiDB](./NewSQL/TiDB/) - Hybrid transactional/analytical processing

## 🎯 Database Selection Guide

### Use Relational Databases When:
- ACID compliance is critical
- Complex relationships between data
- Well-defined schema
- Strong consistency requirements

### Use NoSQL Databases When:
- Rapid scaling requirements
- Flexible/evolving schema
- Big data applications
- High availability needs

### Use Time-Series Databases When:
- IoT data collection
- Monitoring and metrics
- Financial data analysis
- Real-time analytics

### Use Graph Databases When:
- Social networks
- Recommendation engines
- Fraud detection
- Network analysis

## 📊 Comparison Matrix

| Database Type | ACID | Scalability | Schema | Use Cases |
|---------------|------|-------------|--------|-----------|
| RDBMS | ✅ | Vertical | Fixed | Traditional apps, ERP |
| Document | ⚠️ | Horizontal | Flexible | Content management, catalogs |
| Key-Value | ⚠️ | Horizontal | None | Caching, session storage |
| Column-Family | ⚠️ | Horizontal | Semi-structured | Analytics, IoT |
| Graph | ⚠️ | Horizontal | Graph | Social networks, recommendations |
| Time-Series | ⚠️ | Horizontal | Time-based | Monitoring, IoT |
| In-Memory | ⚠️ | Horizontal | Flexible | Real-time processing |
| NewSQL | ✅ | Horizontal | Fixed | Modern distributed apps |

## 🚀 Getting Started

1. **Identify your use case** - Determine data patterns and requirements
2. **Consider scalability** - Current and future data volume
3. **Evaluate consistency needs** - ACID vs eventual consistency
4. **Assess team expertise** - Available skills and learning curve
5. **Review operational requirements** - Backup, monitoring, maintenance