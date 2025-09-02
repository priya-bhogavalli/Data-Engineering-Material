# MongoDB All Features Reference

## 🎯 Overview
Comprehensive reference for MongoDB document database, including data modeling, querying, indexing, sharding, and performance optimization.

## 📍 Legend

### Feature Status
- 🟢 **GA** - Generally Available, production-ready
- 🟡 **Beta** - Available but may change
- 🔴 **Preview** - Early access, limited availability
- ⚫ **Deprecated** - Being phased out

### MongoDB Editions
- **Community** - Open source edition
- **Enterprise** - Commercial edition with advanced features
- **Atlas** - Managed cloud service
- **Mobile** - Embedded database for mobile apps

## 🏗️ Core Architecture

| Component | Purpose | Scalability | Consistency | Performance Impact |
|-----------|---------|-------------|-------------|-------------------|
| **mongod** | Database server | Vertical/Horizontal | Configurable | Direct |
| **mongos** | Query router | Horizontal | Transparent | Routing overhead |
| **Config Servers** | Metadata storage | Replica set | Strong | Metadata operations |
| **Replica Set** | High availability | Read scaling | Tunable | Replication lag |
| **Sharding** | Horizontal scaling | Linear | Eventual | Shard key dependent |

## 📊 Document Model & Data Types

### BSON Data Types
| Type | Description | Storage Size | Use Cases | Indexing |
|------|-------------|--------------|-----------|----------|
| **String** | UTF-8 text | Variable | Text data | B-tree, Text |
| **Integer** | 32/64-bit numbers | 4/8 bytes | Counters, IDs | B-tree |
| **Double** | 64-bit floating point | 8 bytes | Calculations | B-tree |
| **Boolean** | True/false | 1 byte | Flags | B-tree |
| **Date** | UTC datetime | 8 bytes | Timestamps | B-tree |
| **ObjectId** | 12-byte identifier | 12 bytes | Primary keys | B-tree |
| **Array** | Ordered list | Variable | Lists, sets | Multikey |
| **Object** | Embedded document | Variable | Nested data | Compound |
| **Binary** | Binary data | Variable | Files, images | Limited |
| **Decimal128** | High precision decimal | 16 bytes | Financial data | B-tree |

### Document Structure Best Practices
| Pattern | Use Cases | Advantages | Disadvantages | Performance |
|---------|-----------|------------|---------------|-------------|
| **Embedding** | Related data | Single query | Document size limits | Excellent read |
| **Referencing** | Large/shared data | Normalized | Multiple queries | Good with indexes |
| **Hybrid** | Mixed requirements | Flexible | Complex design | Variable |
| **Bucketing** | Time series | Efficient storage | Query complexity | Good aggregation |

## 🔍 Querying & Aggregation

### Query Operations
| Operation | Syntax | Complexity | Use Cases | Performance |
|-----------|--------|------------|-----------|-------------|
| **find()** | `db.collection.find({})` | O(n) without index | Basic queries | Index dependent |
| **findOne()** | `db.collection.findOne({})` | O(n) without index | Single document | Index dependent |
| **count()** | `db.collection.countDocuments({})` | O(n) | Document counting | Index dependent |
| **distinct()** | `db.collection.distinct("field")` | O(n) | Unique values | Index dependent |
| **aggregate()** | `db.collection.aggregate([])` | Variable | Complex analysis | Pipeline dependent |

### Query Operators
| Category | Operators | Use Cases | Examples | Performance |
|----------|-----------|-----------|----------|-------------|
| **Comparison** | `$eq, $ne, $gt, $gte, $lt, $lte` | Range queries | `{age: {$gte: 18}}` | Index friendly |
| **Logical** | `$and, $or, $not, $nor` | Complex conditions | `{$or: [{}, {}]}` | Variable |
| **Element** | `$exists, $type` | Field validation | `{email: {$exists: true}}` | Index dependent |
| **Array** | `$in, $nin, $all, $size` | Array operations | `{tags: {$in: ["red"]}}` | Index dependent |
| **Text** | `$text, $regex` | Text search | `{$text: {$search: "word"}}` | Text index required |
| **Geospatial** | `$near, $geoWithin` | Location queries | `{loc: {$near: [x, y]}}` | Geo index required |

### Aggregation Pipeline
| Stage | Purpose | Performance | Use Cases | Memory Usage |
|-------|---------|-------------|-----------|--------------|
| **$match** | Filter documents | Excellent (with index) | Data filtering | Low |
| **$group** | Group and aggregate | Variable | Summarization | High |
| **$sort** | Sort documents | Good (with index) | Ordering | High |
| **$project** | Shape output | Excellent | Field selection | Low |
| **$lookup** | Join collections | Poor | Data enrichment | Very High |
| **$unwind** | Deconstruct arrays | Good | Array processing | Medium |
| **$facet** | Multiple pipelines | Variable | Multi-dimensional analysis | High |
| **$bucket** | Group by ranges | Good | Histogram creation | Medium |

## 🗂️ Indexing Strategies

### Index Types
| Type | Structure | Use Cases | Performance | Storage Overhead |
|------|-----------|-----------|-------------|------------------|
| **Single Field** | B-tree | Simple queries | Excellent | Low |
| **Compound** | B-tree | Multi-field queries | Excellent | Medium |
| **Multikey** | B-tree | Array fields | Good | Medium |
| **Text** | Inverted index | Full-text search | Good | High |
| **Geospatial** | 2dsphere/2d | Location queries | Excellent | Medium |
| **Hashed** | Hash table | Sharding | Good | Low |
| **Partial** | Filtered B-tree | Conditional indexing | Excellent | Low |
| **Sparse** | Null-excluding | Optional fields | Good | Low |
| **TTL** | Time-based | Auto-expiration | Good | Low |

### Index Performance
| Scenario | Index Strategy | Query Performance | Write Performance | Storage Impact |
|----------|----------------|-------------------|-------------------|----------------|
| **Equality Queries** | Single field | O(log n) | Minimal impact | Low |
| **Range Queries** | Single field | O(log n + k) | Minimal impact | Low |
| **Multi-field Queries** | Compound index | O(log n) | Medium impact | Medium |
| **Text Search** | Text index | Variable | High impact | High |
| **Sorting** | Index on sort fields | O(log n) | Medium impact | Medium |
| **Aggregation** | Pipeline-specific | Variable | Variable | Variable |

### Index Optimization
| Technique | Impact | Complexity | Use Cases | Implementation |
|-----------|--------|------------|-----------|----------------|
| **Index Intersection** | Medium | Low | Multiple single indexes | Automatic |
| **Covered Queries** | Very High | Medium | Projection optimization | Include fields in index |
| **Index Prefixes** | High | Low | Compound index efficiency | Order fields by selectivity |
| **Partial Indexes** | High | Medium | Conditional data | Filter expression |

## 🔄 Replication & High Availability

### Replica Set Configuration
| Member Type | Purpose | Voting | Data | Use Cases |
|-------------|---------|--------|------|-----------|
| **Primary** | Read/write operations | Yes | Full | Main operations |
| **Secondary** | Read operations (optional) | Yes | Full | Read scaling |
| **Arbiter** | Election participation | Yes | None | Odd number voting |
| **Hidden** | Background operations | Yes | Full | Analytics, backups |
| **Delayed** | Historical data | Yes | Full | Point-in-time recovery |

### Read Preferences
| Preference | Behavior | Use Cases | Consistency | Performance |
|------------|----------|-----------|-------------|-------------|
| **primary** | Primary only | Default | Strong | Single point |
| **primaryPreferred** | Primary, then secondary | High consistency | Strong/eventual | Good availability |
| **secondary** | Secondary only | Read scaling | Eventual | Distributed reads |
| **secondaryPreferred** | Secondary, then primary | Analytics | Eventual | Load distribution |
| **nearest** | Lowest latency | Geographic distribution | Eventual | Best performance |

### Write Concerns
| Level | Acknowledgment | Durability | Performance | Use Cases |
|-------|----------------|------------|-------------|-----------|
| **w: 1** | Primary only | Low | Excellent | High throughput |
| **w: majority** | Majority of members | High | Good | Production default |
| **w: "all"** | All members | Very High | Poor | Critical data |
| **j: true** | Journal sync | High | Medium | Durability required |

## 🌐 Sharding & Horizontal Scaling

### Shard Key Selection
| Pattern | Distribution | Query Performance | Limitations | Use Cases |
|---------|--------------|-------------------|-------------|-----------|
| **Ascending** | Poor (hotspots) | Good for ranges | Write hotspots | Time-based queries |
| **Random/Hashed** | Excellent | Poor for ranges | No range queries | Even distribution |
| **Compound** | Good | Excellent | Complex | Multi-dimensional queries |
| **Tag-aware** | Configurable | Good | Management overhead | Geographic distribution |

### Sharding Components
| Component | Role | Scalability | Fault Tolerance | Performance Impact |
|-----------|------|-------------|-----------------|-------------------|
| **mongos** | Query routing | Horizontal | Stateless | Routing overhead |
| **Config Servers** | Metadata storage | Replica set | High availability | Metadata queries |
| **Shards** | Data storage | Horizontal | Replica sets | Direct data access |
| **Balancer** | Chunk migration | Automatic | Background process | Migration overhead |

### Chunk Management
| Aspect | Configuration | Impact | Monitoring | Optimization |
|--------|---------------|--------|------------|--------------|
| **Chunk Size** | 64MB default | Migration frequency | Chunk distribution | Workload-dependent |
| **Splitting** | Automatic | Query performance | Split points | Shard key design |
| **Migration** | Background | Temporary performance impact | Migration status | Balancer windows |
| **Jumbo Chunks** | >chunk size | Performance degradation | Chunk sizes | Shard key cardinality |

## ⚡ Performance Optimization

### Query Optimization
| Technique | Impact | Complexity | Implementation | Monitoring |
|-----------|--------|------------|----------------|------------|
| **Proper Indexing** | Very High | Medium | Index design | Query plans |
| **Query Hints** | Medium | Low | Query modification | Performance metrics |
| **Projection** | Medium | Low | Field selection | Network usage |
| **Limit/Skip** | High | Low | Result limiting | Query efficiency |
| **Aggregation Optimization** | High | High | Pipeline design | Stage analysis |

### Configuration Tuning
| Parameter | Default | Recommended | Impact | Workload |
|-----------|---------|-------------|--------|----------|
| **wiredTigerCacheSizeGB** | 50% RAM | 60-70% RAM | Memory usage | All |
| **wiredTigerCollectionBlockCompressor** | snappy | zstd | Storage/CPU | Storage-sensitive |
| **operationProfiling** | off | slowms: 100 | Performance monitoring | Development |
| **maxIncomingConnections** | 65536 | Workload-dependent | Connection handling | High concurrency |

### Storage Engine Options
| Engine | Use Cases | Performance | Features | Availability |
|--------|-----------|-------------|----------|--------------|
| **WiredTiger** | General purpose | Excellent | Compression, encryption | Default (3.2+) |
| **In-Memory** | High performance | Excellent | No persistence | Enterprise |
| **Encrypted** | Security | Good | Encryption at rest | Enterprise |

## 🔒 Security Features

### Authentication Methods
| Method | Security Level | Complexity | Use Cases | Enterprise Only |
|--------|----------------|------------|-----------|-----------------|
| **SCRAM-SHA-1/256** | High | Low | Standard auth | No |
| **x.509 Certificates** | Very High | High | Certificate-based | No |
| **LDAP** | High | Medium | Enterprise integration | Yes |
| **Kerberos** | Very High | High | Enterprise SSO | Yes |

### Authorization Model
| Feature | Granularity | Scope | Management | Use Cases |
|---------|-------------|-------|------------|-----------|
| **Role-Based Access Control** | Action-level | Database/collection | Built-in roles | Standard access control |
| **Custom Roles** | Fine-grained | Configurable | Manual | Specific requirements |
| **Field-Level Security** | Field-level | Document | Views/aggregation | Sensitive data |
| **Auditing** | Operation-level | System-wide | Enterprise feature | Compliance |

### Encryption
| Type | Scope | Performance Impact | Configuration | Enterprise Only |
|------|-------|-------------------|---------------|-----------------|
| **Encryption at Rest** | Storage | 5-10% | Key management | Yes |
| **Encryption in Transit** | Network | Minimal | TLS configuration | No |
| **Client-Side Field Level** | Application | Variable | Driver support | No |

## 📊 Monitoring & Diagnostics

### Built-in Monitoring
| Tool | Information | Granularity | Real-time | Use Cases |
|------|-------------|-------------|-----------|-----------|
| **db.stats()** | Database statistics | Database-level | Snapshot | Capacity planning |
| **db.collection.stats()** | Collection statistics | Collection-level | Snapshot | Performance analysis |
| **db.serverStatus()** | Server metrics | Server-level | Snapshot | Health monitoring |
| **db.currentOp()** | Active operations | Operation-level | Real-time | Performance debugging |
| **Profiler** | Slow operations | Query-level | Configurable | Query optimization |

### Key Performance Metrics
| Metric | Importance | Threshold | Action | Collection Method |
|--------|------------|-----------|--------|------------------|
| **Query Performance** | High | >100ms | Optimize queries/indexes | Profiler |
| **Replication Lag** | High | <10s | Investigate network/load | rs.status() |
| **Connection Count** | Medium | <80% of max | Connection pooling | serverStatus |
| **Memory Usage** | High | <80% of cache | Tune cache size | serverStatus |
| **Disk Usage** | Medium | <80% capacity | Archive/compress data | File system |

### External Monitoring Tools
| Tool | Integration | Features | Cost | Complexity |
|------|-------------|----------|------|------------|
| **MongoDB Compass** | Native | GUI, query analysis | Free | Low |
| **MongoDB Cloud Manager** | Agent | Comprehensive monitoring | Paid | Medium |
| **Prometheus + Grafana** | Exporter | Custom dashboards | Free | High |
| **Datadog** | Agent | Full observability | Paid | Low |
| **New Relic** | Agent | APM integration | Paid | Low |

## 🌍 Multi-Cloud & Deployment

### Deployment Options
| Option | Management | Scalability | Cost | Control |
|--------|------------|-------------|------|---------|
| **Self-Managed** | Manual | Manual | Infrastructure only | Full |
| **MongoDB Atlas** | Fully managed | Auto-scaling | Service + infrastructure | Limited |
| **Cloud Provider Managed** | Partially managed | Manual | Service + infrastructure | Medium |
| **Kubernetes** | Container orchestration | Auto-scaling | Infrastructure + orchestration | High |

### Atlas Features
| Feature | Capability | Availability | Use Cases | Cost Impact |
|---------|------------|--------------|-----------|-------------|
| **Auto-scaling** | Vertical/horizontal | All tiers | Variable workloads | Usage-based |
| **Global Clusters** | Multi-region | M30+ | Global applications | Higher cost |
| **Serverless** | Pay-per-operation | Limited regions | Sporadic workloads | Operation-based |
| **Data Lake** | Analytics | All tiers | Historical analysis | Storage-based |

## 🚨 Troubleshooting Guide

### Common Issues
| Issue | Symptoms | Causes | Solutions | Prevention |
|-------|----------|--------|-----------|-----------|
| **Slow Queries** | High response times | Missing indexes | Add appropriate indexes | Query analysis |
| **High Memory Usage** | Performance degradation | Large working set | Increase cache size | Capacity planning |
| **Replication Lag** | Stale reads | Network/load issues | Optimize network/queries | Monitoring |
| **Shard Imbalance** | Uneven performance | Poor shard key | Reshard or rebalance | Shard key design |
| **Connection Exhaustion** | Connection errors | Too many connections | Connection pooling | Connection management |

### Diagnostic Commands
| Command | Purpose | Output | Use Cases |
|---------|---------|--------|-----------|
| **explain()** | Query analysis | Execution plan | Query optimization |
| **getShardDistribution()** | Shard analysis | Data distribution | Sharding issues |
| **validate()** | Data integrity | Validation results | Corruption detection |
| **collStats()** | Collection analysis | Storage statistics | Performance tuning |

## 💰 Cost Optimization

### Storage Optimization
| Strategy | Savings | Complexity | Trade-offs | Implementation |
|----------|---------|------------|------------|----------------|
| **Compression** | 30-80% | Low | CPU overhead | Storage engine config |
| **Data Archiving** | Variable | Medium | Data availability | Application logic |
| **Index Optimization** | 10-30% | Medium | Query performance | Index analysis |
| **Document Design** | 20-50% | High | Query patterns | Schema redesign |

### Atlas Cost Management
| Feature | Cost Impact | Configuration | Monitoring | Use Cases |
|---------|-------------|---------------|------------|-----------|
| **Auto-scaling** | Variable | Automatic | Usage metrics | Variable workloads |
| **Scheduled Scaling** | Predictable | Manual | Time-based | Known patterns |
| **Serverless** | Usage-based | Automatic | Operation count | Sporadic usage |
| **Reserved Capacity** | 20-40% savings | Commitment | Usage planning | Predictable workloads |

## 📚 Learning Resources & Best Practices

### Official Resources
| Resource | Type | Focus | Level | Cost |
|----------|------|-------|-------|------|
| **MongoDB Documentation** | Reference | Complete features | All | Free |
| **MongoDB University** | Courses | Structured learning | All | Free |
| **MongoDB Blog** | Articles | Best practices | Intermediate | Free |
| **MongoDB Community** | Forums | Support | All | Free |

### Best Practices
| Category | Recommendation | Impact | Implementation |
|----------|----------------|--------|----------------|
| **Schema Design** | Model for your queries | Very High | Application design |
| **Indexing** | Index your queries | Very High | Performance analysis |
| **Sharding** | Choose shard keys carefully | High | Architecture design |
| **Security** | Enable authentication | High | Security configuration |
| **Monitoring** | Monitor key metrics | High | Monitoring setup |

### Performance Guidelines
| Guideline | Rationale | Implementation | Monitoring |
|-----------|-----------|----------------|------------|
| **Avoid large documents** | Memory efficiency | Document design | Document size tracking |
| **Use projections** | Network efficiency | Query optimization | Network usage |
| **Limit result sets** | Performance | Query limits | Query analysis |
| **Design for growth** | Scalability | Architecture planning | Growth metrics |

## 🆚 MongoDB vs Alternatives

| Alternative | MongoDB Advantage | Alternative Advantage | Best Choice When |
|-------------|------------------|----------------------|------------------|
| **PostgreSQL** | Document model, horizontal scaling | ACID compliance, SQL | Need flexible schema |
| **Cassandra** | Easier operations, richer queries | Linear scalability | Need operational simplicity |
| **DynamoDB** | Open source, query flexibility | Serverless, AWS integration | Need control and flexibility |
| **CouchDB** | Better consistency, aggregation | Multi-master replication | Need strong consistency |
| **Elasticsearch** | General purpose, ACID | Full-text search focus | Need document database |