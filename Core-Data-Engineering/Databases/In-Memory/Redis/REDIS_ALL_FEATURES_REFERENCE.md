# Redis All Features Reference

## 🎯 Overview
Comprehensive reference for Redis in-memory data structure store, including data types, persistence, clustering, and performance optimization.

## 📍 Legend

### Feature Status
- 🟢 **Stable** - Production-ready, fully supported
- 🟡 **Beta** - Available but may change
- 🔴 **Experimental** - Early development
- ⚫ **Deprecated** - Being phased out

### Redis Editions
- **Open Source** - Community edition
- **Redis Enterprise** - Commercial edition
- **Redis Cloud** - Managed service
- **Redis Stack** - Extended modules

## 🏗️ Core Architecture

| Component | Purpose | Scalability | Persistence | Performance Impact |
|-----------|---------|-------------|-------------|-------------------|
| **Single-threaded Core** | Command processing | Vertical | Memory-based | Excellent |
| **Event Loop** | I/O handling | Async | N/A | Minimal overhead |
| **Memory Allocator** | Memory management | Configuration | Snapshots | Direct |
| **Persistence Engine** | Data durability | Background | RDB/AOF | Configurable |
| **Replication** | Data redundancy | Master-slave | Async | Network dependent |

## 📊 Data Types & Operations

### String Operations
| Command | Complexity | Use Cases | Memory Efficiency | Performance |
|---------|------------|-----------|-------------------|-------------|
| **SET/GET** | O(1) | Caching, counters | Excellent | Excellent |
| **INCR/DECR** | O(1) | Counters, metrics | Excellent | Excellent |
| **MSET/MGET** | O(N) | Batch operations | Good | Very Good |
| **SETEX/PSETEX** | O(1) | TTL with set | Excellent | Excellent |
| **APPEND** | O(1) | String building | Good | Good |
| **GETRANGE/SETRANGE** | O(N) | Substring operations | Good | Good |

### Hash Operations
| Command | Complexity | Use Cases | Memory Efficiency | Performance |
|---------|------------|-----------|-------------------|-------------|
| **HSET/HGET** | O(1) | Object storage | Very Good | Excellent |
| **HMSET/HMGET** | O(N) | Batch field operations | Very Good | Very Good |
| **HGETALL** | O(N) | Full object retrieval | Good | Good |
| **HINCRBY** | O(1) | Field counters | Very Good | Excellent |
| **HKEYS/HVALS** | O(N) | Field/value enumeration | Good | Good |
| **HSCAN** | O(1) per call | Large hash iteration | Good | Good |

### List Operations
| Command | Complexity | Use Cases | Memory Efficiency | Performance |
|---------|------------|-----------|-------------------|-------------|
| **LPUSH/RPUSH** | O(1) | Queues, stacks | Good | Excellent |
| **LPOP/RPOP** | O(1) | Queue processing | Good | Excellent |
| **LRANGE** | O(S+N) | Range retrieval | Good | Good |
| **LINDEX** | O(N) | Random access | Good | Variable |
| **LSET** | O(N) | Element update | Good | Variable |
| **BLPOP/BRPOP** | O(1) | Blocking queues | Good | Excellent |

### Set Operations
| Command | Complexity | Use Cases | Memory Efficiency | Performance |
|---------|------------|-----------|-------------------|-------------|
| **SADD/SREM** | O(1) | Membership tracking | Good | Excellent |
| **SISMEMBER** | O(1) | Membership testing | Good | Excellent |
| **SMEMBERS** | O(N) | Set enumeration | Good | Good |
| **SINTER/SUNION** | O(N*M) | Set operations | Good | Variable |
| **SCARD** | O(1) | Set size | Good | Excellent |
| **SPOP/SRANDMEMBER** | O(1) | Random selection | Good | Excellent |

### Sorted Set Operations
| Command | Complexity | Use Cases | Memory Efficiency | Performance |
|---------|------------|-----------|-------------------|-------------|
| **ZADD/ZREM** | O(log(N)) | Leaderboards, rankings | Good | Very Good |
| **ZRANGE/ZREVRANGE** | O(log(N)+M) | Range queries | Good | Very Good |
| **ZRANK/ZREVRANK** | O(log(N)) | Position queries | Good | Very Good |
| **ZSCORE** | O(1) | Score retrieval | Good | Excellent |
| **ZINCRBY** | O(log(N)) | Score updates | Good | Very Good |
| **ZRANGEBYSCORE** | O(log(N)+M) | Score-based ranges | Good | Very Good |

### Advanced Data Types
| Type | Use Cases | Memory Usage | Complexity | Redis Version |
|------|-----------|--------------|------------|---------------|
| **Bitmaps** | Analytics, flags | Very Efficient | O(1) | 2.2+ |
| **HyperLogLog** | Cardinality estimation | Fixed 12KB | O(1) | 2.8+ |
| **Geospatial** | Location services | Good | O(log(N)) | 3.2+ |
| **Streams** | Event sourcing | Good | Various | 5.0+ |
| **JSON** | Document storage | Variable | Various | RedisJSON module |
| **Time Series** | Metrics, monitoring | Compressed | O(1) | RedisTimeSeries module |

## 💾 Persistence Mechanisms

### RDB (Redis Database Backup)
| Aspect | Configuration | Performance Impact | Use Cases | Trade-offs |
|--------|---------------|-------------------|-----------|------------|
| **Snapshot Frequency** | save 900 1 | Low during operation | Point-in-time backup | Data loss window |
| **Compression** | rdbcompression yes | CPU vs storage | Storage optimization | CPU overhead |
| **Checksum** | rdbchecksum yes | Minimal | Data integrity | Slight overhead |
| **Background Save** | BGSAVE command | Fork overhead | Non-blocking backup | Memory usage spike |

### AOF (Append Only File)
| Setting | Options | Durability | Performance | Use Cases |
|---------|---------|------------|-------------|-----------|
| **appendonly** | yes/no | High | Medium impact | High durability needs |
| **appendfsync** | always/everysec/no | Variable | Variable | Durability vs performance |
| **auto-aof-rewrite** | Percentage/size | Background | Minimal | Log size management |
| **aof-use-rdb-preamble** | yes/no | Hybrid | Best of both | Fast startup + durability |

### Persistence Comparison
| Method | Startup Time | Durability | File Size | CPU Usage | Use Cases |
|--------|--------------|------------|-----------|-----------|-----------|
| **RDB Only** | Fast | Medium | Small | Low | Caching, acceptable data loss |
| **AOF Only** | Slow | High | Large | Medium | High durability requirements |
| **RDB + AOF** | Medium | Very High | Large | Medium | Production systems |
| **None** | Instant | None | None | Minimal | Pure cache, temporary data |

## 🔄 Replication & High Availability

### Replication Configuration
| Parameter | Default | Recommended | Impact | Use Cases |
|-----------|---------|-------------|--------|-----------|
| **replicaof** | None | Master IP:port | Enables replication | Read scaling |
| **replica-read-only** | yes | yes | Write protection | Read replicas |
| **repl-diskless-sync** | no | yes (fast networks) | Network vs disk | Cloud deployments |
| **repl-backlog-size** | 1mb | 64mb+ | Partial resync | Network instability |

### Redis Sentinel
| Feature | Purpose | Configuration | Monitoring | Use Cases |
|---------|---------|---------------|------------|-----------|
| **Master Monitoring** | Health checking | sentinel monitor | Continuous | Automatic failover |
| **Automatic Failover** | Master promotion | Quorum-based | Event-driven | High availability |
| **Configuration Provider** | Service discovery | Dynamic updates | Real-time | Client configuration |
| **Notification** | Event alerts | Pub/sub | Configurable | Operations monitoring |

### Redis Cluster
| Aspect | Specification | Scalability | Consistency | Complexity |
|--------|---------------|-------------|-------------|------------|
| **Sharding** | Hash slots (16384) | Horizontal | Eventual | High |
| **Replication** | Master-replica per shard | Read scaling | Async | Medium |
| **Resharding** | Online migration | Dynamic | Consistent hashing | High |
| **Multi-key Operations** | Hash tag required | Limited | Cross-slot restrictions | Medium |

## ⚡ Performance Optimization

### Memory Optimization
| Technique | Memory Savings | Complexity | Trade-offs | Implementation |
|-----------|----------------|------------|------------|----------------|
| **Hash Optimization** | 30-50% | Low | None | maxmemory-policy |
| **Compression** | 20-40% | Medium | CPU overhead | hash-max-ziplist-* |
| **Expiration** | Variable | Low | Data availability | TTL settings |
| **Data Structure Choice** | 10-90% | Medium | Feature limitations | Design decisions |

### Configuration Tuning
| Parameter | Default | Optimized | Impact | Workload |
|-----------|---------|-----------|--------|----------|
| **maxmemory** | 0 (unlimited) | 80% of RAM | Memory management | All |
| **maxmemory-policy** | noeviction | allkeys-lru | Eviction behavior | Cache workloads |
| **tcp-keepalive** | 300 | 60 | Connection health | Network issues |
| **timeout** | 0 | 300 | Idle connections | Resource management |
| **tcp-backlog** | 511 | 65535 | Connection queue | High concurrency |

### Pipelining & Batching
| Technique | Throughput Gain | Latency Impact | Complexity | Use Cases |
|-----------|-----------------|----------------|------------|-----------|
| **Pipelining** | 5-10x | Increased | Low | Batch operations |
| **Transactions** | Variable | Atomic | Medium | Consistency requirements |
| **Lua Scripts** | High | Reduced | High | Complex operations |
| **Mass Insertion** | Very High | N/A | Low | Data loading |

## 🔒 Security Features

### Authentication & Authorization
| Feature | Security Level | Complexity | Use Cases | Redis Version |
|---------|----------------|------------|-----------|---------------|
| **AUTH Command** | Basic | Low | Simple authentication | All |
| **ACL (Access Control Lists)** | Advanced | Medium | Fine-grained access | 6.0+ |
| **TLS/SSL** | High | Medium | Encrypted connections | 6.0+ |
| **Protected Mode** | Basic | None | Default security | 3.2+ |

### ACL Configuration
| ACL Rule | Purpose | Granularity | Examples | Use Cases |
|----------|---------|-------------|----------|-----------|
| **User Management** | Identity | User-level | `ACL SETUSER alice` | Multi-tenant |
| **Command Restrictions** | Operations | Command-level | `+get -set` | Read-only users |
| **Key Patterns** | Data access | Key-level | `~cache:*` | Namespace isolation |
| **Channel Patterns** | Pub/sub access | Channel-level | `&news:*` | Topic-based access |

### Network Security
| Feature | Protection Level | Implementation | Performance Impact | Use Cases |
|---------|------------------|----------------|-------------------|-----------|
| **Bind Interface** | Medium | Configuration | None | Network isolation |
| **Firewall Rules** | High | External | None | Access control |
| **VPN/Private Networks** | Very High | Infrastructure | Minimal | Secure communication |
| **TLS Encryption** | Very High | Configuration | 10-20% | Data protection |

## 🌐 Clustering & Scaling

### Scaling Patterns
| Pattern | Scalability | Complexity | Consistency | Use Cases |
|---------|-------------|------------|-------------|-----------|
| **Master-Replica** | Read scaling | Low | Strong | Read-heavy workloads |
| **Redis Cluster** | Horizontal | High | Eventual | Large datasets |
| **Client-side Sharding** | Horizontal | Medium | Application-managed | Custom requirements |
| **Proxy-based Sharding** | Horizontal | Medium | Proxy-managed | Transparent sharding |

### Redis Cluster Features
| Feature | Capability | Limitations | Configuration | Monitoring |
|---------|------------|-------------|---------------|------------|
| **Automatic Sharding** | 16384 hash slots | Multi-key operations | cluster-enabled yes | CLUSTER INFO |
| **Online Resharding** | Live migration | Temporary performance impact | Manual/automated | CLUSTER NODES |
| **Failover** | Automatic promotion | Split-brain scenarios | cluster-node-timeout | Sentinel integration |
| **Cross-slot Operations** | Hash tags | Limited functionality | Application design | Client libraries |

## 🔌 Modules & Extensions

### Redis Stack Modules
| Module | Purpose | Use Cases | Performance | Maturity |
|--------|---------|-----------|-------------|----------|
| **RedisJSON** | JSON document store | Document databases | Good | Stable |
| **RedisSearch** | Full-text search | Search engines | Excellent | Stable |
| **RedisTimeSeries** | Time series data | Metrics, monitoring | Excellent | Stable |
| **RedisGraph** | Graph database | Social networks | Good | Stable |
| **RedisBloom** | Probabilistic data | Bloom filters, counting | Excellent | Stable |
| **RedisGears** | Serverless functions | Data processing | Good | Stable |

### Third-party Modules
| Module | Provider | Purpose | License | Popularity |
|--------|----------|---------|---------|------------|
| **neural-redis** | RedisLabs | Machine learning | Commercial | Medium |
| **redis-cell** | Community | Rate limiting | BSD | High |
| **rejson** | Community | JSON (legacy) | AGPL | Medium |
| **redis-ml** | Community | Machine learning | BSD | Low |

## 📊 Monitoring & Observability

### Built-in Monitoring
| Command | Information | Frequency | Use Cases | Performance Impact |
|---------|-------------|-----------|-----------|-------------------|
| **INFO** | Server statistics | On-demand | Health monitoring | Minimal |
| **MONITOR** | Real-time commands | Continuous | Debugging | High |
| **SLOWLOG** | Slow queries | Automatic | Performance tuning | Minimal |
| **CLIENT LIST** | Connection info | On-demand | Connection monitoring | Low |
| **MEMORY USAGE** | Memory analysis | On-demand | Memory optimization | Low |

### Key Metrics
| Metric | Importance | Threshold | Action | Collection Method |
|--------|------------|-----------|--------|------------------|
| **Memory Usage** | Critical | 80% of maxmemory | Scale/optimize | INFO memory |
| **Hit Ratio** | High | >90% | Optimize caching | INFO stats |
| **Connected Clients** | Medium | Monitor trends | Connection pooling | INFO clients |
| **Operations/sec** | Medium | Baseline comparison | Performance tuning | INFO stats |
| **Keyspace Hits/Misses** | High | Application dependent | Cache optimization | INFO stats |

### External Monitoring Tools
| Tool | Integration | Features | Cost | Complexity |
|------|-------------|----------|------|------------|
| **Redis Insight** | Native | GUI, profiling | Free | Low |
| **Prometheus + Grafana** | Exporter | Metrics, alerting | Free | Medium |
| **Datadog** | Agent | Full observability | Paid | Low |
| **New Relic** | Agent | APM integration | Paid | Low |
| **ElasticSearch** | Logstash | Log analysis | Free/Paid | Medium |

## 🚨 Troubleshooting Guide

### Common Issues
| Issue | Symptoms | Causes | Solutions | Prevention |
|-------|----------|--------|-----------|-----------|
| **High Memory Usage** | Slow performance, evictions | Large datasets, memory leaks | Optimize data structures, set TTL | Memory monitoring |
| **Slow Queries** | High latency | Complex operations, large data | Optimize commands, use pipelining | Query analysis |
| **Connection Issues** | Timeouts, refused connections | Network problems, limits | Check network, increase limits | Connection monitoring |
| **Replication Lag** | Stale data on replicas | Network latency, load | Optimize network, reduce load | Replication monitoring |
| **Cluster Split-brain** | Inconsistent data | Network partitions | Fix network, adjust timeouts | Network reliability |

### Diagnostic Commands
| Command | Purpose | Output | Use Cases |
|---------|---------|--------|-----------|
| **LATENCY DOCTOR** | Latency analysis | Recommendations | Performance issues |
| **MEMORY DOCTOR** | Memory analysis | Optimization tips | Memory problems |
| **DEBUG OBJECT** | Object inspection | Internal details | Data structure analysis |
| **CLIENT TRACKING** | Connection tracking | Client behavior | Connection debugging |

## 💰 Cost Optimization

### Memory Optimization Strategies
| Strategy | Memory Savings | Complexity | Trade-offs |
|----------|----------------|------------|------------|
| **Expire Keys** | 20-80% | Low | Data availability |
| **Compress Values** | 30-70% | Medium | CPU overhead |
| **Optimize Data Structures** | 10-50% | Medium | Feature limitations |
| **Use Appropriate Types** | 20-90% | Low | Design constraints |

### Managed Service Costs
| Provider | Pricing Model | Cost Factors | Optimization |
|----------|---------------|--------------|--------------|
| **Redis Cloud** | Memory + throughput | Memory size, operations | Right-sizing |
| **AWS ElastiCache** | Instance-based | Instance type, multi-AZ | Reserved instances |
| **Azure Cache** | Tier-based | Performance tier | Appropriate sizing |
| **GCP Memorystore** | Memory-based | Memory allocation | Usage monitoring |

## 📚 Learning Resources & Best Practices

### Official Resources
| Resource | Type | Focus | Level | Cost |
|----------|------|-------|-------|------|
| **Redis Documentation** | Reference | Complete features | All | Free |
| **Redis University** | Courses | Structured learning | Beginner-Advanced | Free |
| **Redis Labs Blog** | Articles | Best practices | Intermediate | Free |

### Best Practices
| Category | Recommendation | Impact | Implementation |
|----------|----------------|--------|----------------|
| **Key Naming** | Use consistent patterns | High | Naming conventions |
| **Memory Management** | Set appropriate TTLs | High | Application design |
| **Connection Pooling** | Use connection pools | Medium | Client configuration |
| **Monitoring** | Implement comprehensive monitoring | High | Monitoring setup |
| **Security** | Enable authentication and encryption | High | Security configuration |

### Performance Guidelines
| Guideline | Rationale | Implementation | Monitoring |
|-----------|-----------|----------------|------------|
| **Avoid KEYS command** | O(N) complexity | Use SCAN instead | Command monitoring |
| **Use Pipelining** | Reduce round trips | Client implementation | Latency metrics |
| **Optimize Data Structures** | Memory efficiency | Design choices | Memory usage |
| **Set Memory Limits** | Prevent OOM | Configuration | Memory monitoring |

## 🆚 Redis vs Alternatives

| Alternative | Redis Advantage | Alternative Advantage | Best Choice When |
|-------------|-----------------|----------------------|------------------|
| **Memcached** | Rich data types, persistence | Simplicity, multi-threading | Need complex data structures |
| **Hazelcast** | Simplicity, performance | Distributed computing | Need simple caching |
| **Apache Ignite** | Ease of use | SQL support, ACID | Need in-memory database |
| **Aerospike** | Cost, ecosystem | High performance, SSD optimization | Need general-purpose solution |
| **DynamoDB** | Open source, control | Serverless, AWS integration | Need flexibility, cost control |