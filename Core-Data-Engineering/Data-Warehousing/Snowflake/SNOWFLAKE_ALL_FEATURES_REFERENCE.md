# Snowflake All Features Reference

## 🎯 Overview
Comprehensive reference for Snowflake features, architecture, performance optimization, security, and data engineering capabilities.

## 📍 Legend

### Feature Status
- 🟢 **GA** - Generally Available, production-ready
- 🟡 **Public Preview** - Available for testing
- 🔴 **Private Preview** - Limited availability
- ⚫ **Deprecated** - Being phased out

### Edition Support
- **Standard** - Basic features
- **Enterprise** - Advanced features
- **Business Critical** - Enhanced security
- **VPS** - Virtual Private Snowflake

## 🏗️ Core Architecture Components

| Component | Purpose | Scaling | Isolation | Performance Impact |
|-----------|---------|---------|-----------|-------------------|
| **Storage Layer** | Data persistence | Automatic | Complete | Transparent |
| **Compute Layer** | Query processing | Manual/Auto | Per warehouse | Direct |
| **Services Layer** | Metadata, security | Automatic | Shared | Minimal |
| **Cloud Services** | Authentication, optimization | Automatic | Shared | Background |

## 💾 Storage Features

| Feature | Edition | Description | Use Cases | Cost Impact |
|---------|---------|-------------|-----------|-------------|
| **Micro-partitions** | All | Automatic data partitioning | Query performance | None |
| **Clustering** | All | Data organization | Large table performance | Compute credits |
| **Time Travel** | All | Historical data access | Data recovery, auditing | Storage costs |
| **Fail-safe** | All | Data protection | Disaster recovery | Included |
| **Zero-copy Cloning** | All | Instant data copies | Development, testing | Metadata only |
| **Data Sharing** | All | Secure data sharing | Collaboration | None (reader pays) |
| **Secure Views** | Enterprise+ | Row-level security | Data governance | None |

### Time Travel & Fail-safe
| Data Retention | Standard | Enterprise | Business Critical | Use Cases |
|----------------|----------|------------|-------------------|-----------|
| **Time Travel** | 1 day | 90 days | 90 days | Accidental changes, auditing |
| **Fail-safe** | 7 days | 7 days | 7 days | Disaster recovery |
| **Total Protection** | 8 days | 97 days | 97 days | Complete data protection |

## 🖥️ Compute Resources (Warehouses)

### Warehouse Sizes
| Size | Credits/Hour | Nodes | Memory | Use Cases | Cost/Hour (On-Demand) |
|------|--------------|-------|--------|-----------|----------------------|
| **X-Small** | 1 | 1 | 8 GB | Development, small queries | $2-4 |
| **Small** | 2 | 2 | 16 GB | Regular workloads | $4-8 |
| **Medium** | 4 | 4 | 32 GB | Medium workloads | $8-16 |
| **Large** | 8 | 8 | 64 GB | Large datasets | $16-32 |
| **X-Large** | 16 | 16 | 128 GB | Heavy processing | $32-64 |
| **2X-Large** | 32 | 32 | 256 GB | Very large workloads | $64-128 |
| **3X-Large** | 64 | 64 | 512 GB | Massive processing | $128-256 |
| **4X-Large** | 128 | 128 | 1 TB | Extreme workloads | $256-512 |

### Warehouse Features
| Feature | Purpose | Configuration | Impact | Best Practices |
|---------|---------|---------------|--------|----------------|
| **Auto-suspend** | Cost optimization | Timeout setting | High cost savings | Set to 1-5 minutes |
| **Auto-resume** | Convenience | Automatic | User experience | Always enable |
| **Multi-cluster** | Concurrency | Min/max clusters | Performance, cost | Enterprise+ only |
| **Query queuing** | Resource management | Automatic | Performance | Monitor queue depth |
| **Resource monitors** | Cost control | Credit limits | Cost management | Set alerts at 80% |

## 🔒 Security & Governance

### Authentication Methods
| Method | Edition | Security Level | Use Cases | Setup Complexity |
|--------|---------|----------------|-----------|------------------|
| **Username/Password** | All | Basic | Development | Low |
| **MFA** | All | Medium | Production users | Low |
| **SSO (SAML)** | Enterprise+ | High | Enterprise integration | Medium |
| **OAuth** | All | High | Application integration | Medium |
| **Key Pair** | All | High | Service accounts | Medium |
| **External OAuth** | Enterprise+ | High | Third-party integration | High |

### Access Control
| Feature | Granularity | Edition | Use Cases | Management |
|---------|-------------|---------|-----------|------------|
| **RBAC** | Role-based | All | Standard access control | Manual |
| **ABAC** | Attribute-based | Enterprise+ | Dynamic access | Policy-driven |
| **Row Access Policies** | Row-level | Enterprise+ | Data privacy | Policy-based |
| **Column Masking** | Column-level | Enterprise+ | PII protection | Policy-based |
| **Tag-based Policies** | Tag-based | Enterprise+ | Automated governance | Tag-driven |

### Encryption
| Type | Scope | Key Management | Edition | Performance Impact |
|------|-------|----------------|---------|-------------------|
| **At Rest** | All data | Snowflake-managed | All | None |
| **In Transit** | Network | TLS 1.2+ | All | Minimal |
| **Client-side** | Application | Customer-managed | All | Application-dependent |
| **Tri-Secret Secure** | Enhanced | Customer + Snowflake | Business Critical | None |

## 📊 Data Types & Functions

### Native Data Types
| Category | Types | Max Size | Use Cases | Performance |
|----------|-------|----------|-----------|-------------|
| **Numeric** | NUMBER, INT, FLOAT | 38 digits | Calculations, IDs | Excellent |
| **String** | VARCHAR, CHAR, TEXT | 16 MB | Text data | Good |
| **Date/Time** | DATE, TIME, TIMESTAMP | N/A | Temporal data | Excellent |
| **Semi-structured** | VARIANT, OBJECT, ARRAY | 16 MB | JSON, XML | Good |
| **Binary** | BINARY, VARBINARY | 8 MB | Files, images | Good |
| **Boolean** | BOOLEAN | N/A | Flags | Excellent |
| **Geography** | GEOGRAPHY | 16 MB | Geospatial data | Good |

### Semi-structured Functions
| Function | Purpose | Performance | Use Cases | Example |
|----------|---------|-------------|-----------|---------|
| **PARSE_JSON()** | Parse JSON strings | Good | Data ingestion | `PARSE_JSON(json_string)` |
| **GET()** | Extract values | Excellent | Data extraction | `GET(variant_col, 'key')` |
| **FLATTEN()** | Unnest arrays | Good | Data normalization | `FLATTEN(array_col)` |
| **OBJECT_CONSTRUCT()** | Build objects | Good | Data transformation | `OBJECT_CONSTRUCT('key', value)` |
| **ARRAY_CONSTRUCT()** | Build arrays | Good | Data aggregation | `ARRAY_CONSTRUCT(val1, val2)` |

## 🔄 Data Loading & Unloading

### Loading Methods
| Method | Performance | Use Cases | Complexity | Cost |
|--------|-------------|-----------|------------|------|
| **COPY INTO** | Excellent | Batch loading | Low | Compute only |
| **Snowpipe** | Good | Continuous loading | Medium | Compute + serverless |
| **INSERT** | Poor | Small datasets | Low | Compute only |
| **Streams & Tasks** | Good | Change data capture | High | Compute + serverless |
| **External Tables** | Good | Query without loading | Medium | Compute only |

### File Formats
| Format | Compression | Performance | Schema Evolution | Use Cases |
|--------|-------------|-------------|------------------|-----------|
| **Parquet** | Built-in | Excellent | Yes | Analytics, data lakes |
| **JSON** | gzip, brotli | Good | Limited | Semi-structured data |
| **CSV** | gzip, brotli | Good | No | Legacy systems |
| **Avro** | Built-in | Good | Yes | Streaming data |
| **ORC** | Built-in | Excellent | Yes | Hadoop ecosystems |
| **XML** | gzip, brotli | Fair | No | Legacy systems |

### Stage Types
| Stage Type | Location | Security | Use Cases | Management |
|------------|----------|----------|-----------|------------|
| **Internal** | Snowflake storage | High | Temporary files | Automatic |
| **External (S3)** | AWS S3 | Medium-High | Data lakes | Customer |
| **External (Azure)** | Azure Blob | Medium-High | Azure integration | Customer |
| **External (GCS)** | Google Cloud | Medium-High | GCP integration | Customer |

## ⚡ Performance Optimization

### Query Optimization
| Technique | Impact | Complexity | Use Cases | Implementation |
|-----------|--------|------------|-----------|----------------|
| **Clustering Keys** | Very High | Medium | Large tables | `ALTER TABLE ... CLUSTER BY` |
| **Materialized Views** | High | Low | Repeated queries | `CREATE MATERIALIZED VIEW` |
| **Result Caching** | Very High | None | Identical queries | Automatic |
| **Warehouse Sizing** | High | Low | Resource allocation | Right-sizing |
| **Partition Pruning** | High | Low | Time-based queries | Proper WHERE clauses |
| **Projection Pushdown** | Medium | None | Column selection | SELECT specific columns |

### Monitoring & Optimization
| Tool/Feature | Purpose | Granularity | Cost | Access |
|--------------|---------|-------------|------|--------|
| **Query History** | Performance analysis | Query-level | Free | Web UI, SQL |
| **Query Profile** | Execution details | Operator-level | Free | Web UI |
| **Account Usage** | Resource monitoring | Account-level | Free | Information Schema |
| **Resource Monitors** | Cost control | Warehouse-level | Free | Web UI, SQL |
| **Query Acceleration** | Automatic optimization | Query-level | Additional credits | Enterprise+ |

## 🌐 Data Sharing & Collaboration

### Sharing Types
| Type | Direction | Security | Use Cases | Pricing |
|------|-----------|----------|-----------|---------|
| **Direct Share** | One-to-one | High | Partner collaboration | Reader pays compute |
| **Data Exchange** | Many-to-many | High | Marketplace | Revenue sharing |
| **Reader Accounts** | One-to-many | Medium | Customer distribution | Provider pays |
| **Replication** | Cross-region | High | Global distribution | Storage + compute |

### Marketplace
| Category | Examples | Pricing Model | Quality | Use Cases |
|----------|----------|---------------|---------|-----------|
| **Business** | Financial, marketing data | Subscription, usage | High | Analytics, ML |
| **Weather** | Weather APIs, historical | Usage-based | High | Logistics, agriculture |
| **Demographics** | Population, economic | Subscription | High | Market research |
| **Geospatial** | Maps, location data | Usage-based | High | Location analytics |
| **Free** | Sample datasets | Free | Variable | Testing, learning |

## 🔧 Development & Integration

### Connectors & Drivers
| Type | Language/Tool | Performance | Features | Maintenance |
|------|---------------|-------------|----------|-------------|
| **JDBC** | Java, Scala | Excellent | Full SQL support | Snowflake |
| **ODBC** | Python, R, C++ | Excellent | Full SQL support | Snowflake |
| **Python** | Python | Excellent | Native integration | Snowflake |
| **Node.js** | JavaScript | Good | Async support | Snowflake |
| **Go** | Go | Good | Concurrent queries | Snowflake |
| **Spark** | Scala, Python | Excellent | Pushdown optimization | Snowflake |
| **Kafka** | Streaming | Good | Real-time ingestion | Snowflake |

### SQL Extensions
| Feature | Standard SQL | Snowflake Enhancement | Use Cases |
|---------|--------------|----------------------|-----------|
| **QUALIFY** | No | Row filtering after window functions | Analytics |
| **FLATTEN** | No | Semi-structured data processing | JSON/XML |
| **LATERAL** | Yes | Enhanced correlated queries | Complex joins |
| **PIVOT/UNPIVOT** | Limited | Full implementation | Data transformation |
| **MATCH_RECOGNIZE** | No | Pattern matching | Time series analysis |

## 🚀 Advanced Features

### Streams & Tasks
| Feature | Purpose | Trigger | Use Cases | Limitations |
|---------|---------|---------|-----------|-------------|
| **Streams** | Change tracking | DML operations | CDC, auditing | 14-day retention |
| **Tasks** | Scheduling | Time/stream-based | ETL automation | Single SQL statement |
| **Task Trees** | Dependencies | Predecessor completion | Complex workflows | Manual management |
| **Stored Procedures** | Logic encapsulation | Manual/scheduled | Complex processing | JavaScript/SQL |

### Machine Learning
| Feature | Edition | Capability | Use Cases | Integration |
|---------|---------|------------|-----------|-------------|
| **Snowpark** | All | Python in Snowflake | ML pipelines | Native |
| **UDFs** | All | Custom functions | Feature engineering | Multiple languages |
| **External Functions** | All | Cloud ML services | Model inference | AWS, Azure, GCP |
| **Cortex** | 🟡 Preview | Built-in ML | Text analysis, forecasting | Native |

## 💰 Pricing & Cost Optimization

### Credit Consumption
| Service | Credit Rate | Billing | Optimization Tips |
|---------|-------------|---------|-------------------|
| **Compute** | Warehouse size | Per-second | Auto-suspend, right-sizing |
| **Snowpipe** | 0.06 credits/hour | Minimum 1 minute | Batch files, optimize frequency |
| **Cloud Services** | Variable | Usage-based | Efficient queries, caching |
| **Data Transfer** | Variable | Per-byte | Regional optimization |
| **Replication** | Storage + compute | Usage-based | Selective replication |

### Cost Optimization Strategies
| Strategy | Impact | Complexity | Implementation |
|----------|--------|------------|----------------|
| **Warehouse Auto-suspend** | Very High | Low | Set timeout to 1-5 minutes |
| **Right-sizing Warehouses** | High | Medium | Monitor query performance |
| **Result Caching** | High | None | Automatic feature |
| **Clustering Optimization** | Medium | High | Analyze query patterns |
| **Resource Monitors** | High | Low | Set credit limits and alerts |
| **Query Optimization** | Medium | Medium | Analyze query profiles |

## 🌍 Multi-Cloud & Regions

### Cloud Providers
| Provider | Regions | Features | Integration | Availability |
|----------|---------|----------|-------------|--------------|
| **AWS** | 25+ regions | Full feature set | Native services | Global |
| **Azure** | 15+ regions | Full feature set | Native services | Global |
| **GCP** | 10+ regions | Full feature set | Native services | Growing |

### Cross-Cloud Features
| Feature | Capability | Use Cases | Limitations |
|---------|------------|-----------|-------------|
| **Cross-Cloud Auto-Fulfillment** | Automatic failover | Disaster recovery | Same provider |
| **Replication** | Cross-region/cloud | Global distribution | Additional costs |
| **Data Sharing** | Cross-account | Collaboration | Same cloud |
| **Private Connectivity** | VPC/VNet integration | Security | Cloud-specific |

## 🚨 Troubleshooting & Best Practices

### Common Issues
| Issue | Symptoms | Causes | Solutions |
|-------|----------|--------|-----------|
| **Slow Queries** | Long execution time | Poor clustering, large scans | Optimize clustering, add filters |
| **High Costs** | Unexpected bills | Large warehouses, no auto-suspend | Right-size, enable auto-suspend |
| **Load Failures** | COPY errors | File format issues | Validate format, check permissions |
| **Concurrency Issues** | Query queuing | Insufficient compute | Scale warehouse, use multi-cluster |
| **Data Skew** | Uneven performance | Poor clustering key | Reconsider clustering strategy |

### Best Practices
| Area | Recommendation | Impact | Implementation |
|------|----------------|--------|----------------|
| **Warehouse Management** | Use auto-suspend/resume | High cost savings | Configure timeouts |
| **Data Loading** | Use COPY INTO with stages | Better performance | Implement proper staging |
| **Security** | Implement RBAC and MFA | Risk reduction | Define roles and policies |
| **Monitoring** | Set up resource monitors | Cost control | Configure alerts |
| **Query Design** | Use clustering and filtering | Performance improvement | Analyze query patterns |

## 📚 Learning Resources & Certification

### Certification Paths
| Certification | Level | Focus | Duration | Validity |
|---------------|-------|-------|---------|----------|
| **SnowPro Core** | Associate | Fundamentals | 2 hours | 2 years |
| **SnowPro Advanced: Architect** | Professional | Architecture | 2 hours | 2 years |
| **SnowPro Advanced: Data Engineer** | Professional | Data Engineering | 2 hours | 2 years |
| **SnowPro Advanced: Data Analyst** | Professional | Analytics | 2 hours | 2 years |

### Learning Resources
| Resource | Type | Focus | Level | Cost |
|----------|------|-------|-------|------|
| **Snowflake University** | Online courses | Comprehensive | All | Free |
| **Hands-on Labs** | Interactive | Practical skills | Beginner-Intermediate | Free |
| **Documentation** | Reference | Complete feature set | All | Free |
| **Community** | Forums, Slack | Support | All | Free |
| **Partner Training** | Instructor-led | Specialized topics | Intermediate-Advanced | Paid |

## 🆚 Snowflake vs Competitors

| Competitor | Snowflake Advantage | Competitor Advantage | Best Choice When |
|------------|-------------------|---------------------|------------------|
| **Redshift** | Separation of compute/storage, multi-cloud | AWS integration, lower entry cost | Need flexibility, multi-cloud |
| **BigQuery** | More SQL features, data sharing | Serverless, Google ecosystem | Need advanced SQL, data collaboration |
| **Databricks** | Pure data warehouse, SQL focus | Unified analytics, ML focus | Primary use is data warehousing |
| **Synapse** | Multi-cloud, easier scaling | Azure integration, hybrid analytics | Need Azure independence |
| **Teradata** | Cloud-native, modern architecture | On-premises expertise | Cloud-first strategy |