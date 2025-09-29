# Apache NiFi All Features Reference

## 🎯 Overview
Comprehensive reference for Apache NiFi features, processors, deployment modes, performance tuning, and ecosystem integrations for data flow automation and management.

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Legend](#-legend)
3. [Core Components & Features](#️-core-components--features)
4. [Processor Categories](#-processor-categories)
5. [Deployment Modes Comparison](#-deployment-modes-comparison)
6. [Data Sources & Formats](#-data-sources--formats)
7. [Performance Optimization Features](#-performance-optimization-features)
8. [Configuration Categories](#-configuration-categories)
9. [Ecosystem Integrations](#-ecosystem-integrations)
10. [Performance Benchmarks & Limits](#-performance-benchmarks--limits)
11. [Monitoring & Debugging](#-monitoring--debugging)
12. [Common Issues & Solutions](#-common-issues--solutions)
13. [Version Compatibility](#-version-compatibility)
14. [Quick Reference Commands](#-quick-reference-commands)
15. [Related Resources](#-related-resources)

## 📍 Legend

### Component Status
- 🟢 **Stable** - Production-ready, fully supported
- 🟡 **Experimental** - Available but may change
- 🔴 **Alpha** - Early development, use with caution
- ⚫ **Deprecated** - Being phased out

### Processor Types
- **Source** - Data ingestion processors
- **Transform** - Data transformation processors
- **Route** - Data routing and filtering
- **Destination** - Data output processors
- **Control** - Flow control processors

## 🏗️ Core Components & Features

| Component | Status | Description | Primary Use Cases | Key Features | Performance Notes |
|-----------|--------|-------------|-------------------|--------------|-------------------|
| **Flow Controller** | 🟢 | Core orchestration engine | Task scheduling, resource management | Thread management, flow coordination | Central processing hub |
| **Web Server** | 🟢 | User interface and REST API | Flow design, monitoring, configuration | Drag-drop UI, real-time monitoring | Lightweight HTTP server |
| **FlowFile Repository** | 🟢 | FlowFile metadata storage | State tracking, recovery | Write-ahead logging, checkpointing | High-performance metadata store |
| **Content Repository** | 🟢 | FlowFile content storage | Data payload management | Pluggable storage, compression | Optimized for streaming I/O |
| **Provenance Repository** | 🟢 | Data lineage tracking | Audit trails, compliance | Event logging, searchable history | Configurable retention policies |
| **Processor Framework** | 🟢 | Extensible processing engine | Custom logic implementation | Plugin architecture, lifecycle management | Concurrent execution support |
| **Expression Language** | 🟢 | Dynamic attribute evaluation | Runtime configuration, routing | Function library, conditional logic | Compiled expressions |
| **Controller Services** | 🟢 | Shared service components | Connection pooling, configuration | Lifecycle management, dependency injection | Resource sharing optimization |

## 🔧 Processor Categories

### Data Ingestion Processors
| Processor | Status | Data Sources | Key Features | Performance Tips |
|-----------|--------|--------------|--------------|------------------|
| **GetFile** | 🟢 | Local filesystem | File monitoring, filtering | Use minimum file age, batch processing |
| **GetSFTP** | 🟢 | SFTP servers | Secure file transfer | Connection pooling, keep-alive |
| **GetHTTP** | 🟢 | HTTP/HTTPS endpoints | REST API consumption | Connection reuse, compression |
| **GetKafka** | 🟢 | Apache Kafka | Stream ingestion | Consumer group management, offset tracking |
| **GetJMS** | 🟢 | JMS message queues | Message consumption | Connection pooling, transaction management |
| **GetDatabase** | 🟢 | JDBC databases | Database polling | Connection pooling, incremental queries |
| **GetMongo** | 🟢 | MongoDB | Document retrieval | Aggregation pipeline, batch size tuning |
| **GetElasticsearch** | 🟢 | Elasticsearch | Search-based ingestion | Query optimization, scroll API |
| **ListenHTTP** | 🟢 | HTTP listeners | Webhook reception | Port management, SSL configuration |
| **ConsumeAMQP** | 🟢 | AMQP brokers | Message consumption | Queue management, acknowledgments |

### Data Transformation Processors
| Processor | Status | Transformation Type | Use Cases | Configuration Tips |
|-----------|--------|-------------------|-----------|-------------------|
| **JoltTransformJSON** | 🟢 | JSON transformation | Schema mapping, data restructuring | Optimize Jolt specs, cache transformations |
| **ConvertRecord** | 🟢 | Format conversion | CSV to JSON, Avro to Parquet | Use appropriate readers/writers |
| **ReplaceText** | 🟢 | Text manipulation | Pattern replacement, data cleansing | Compile regex patterns, use streaming |
| **SplitText** | 🟢 | Text splitting | File decomposition, batch processing | Optimize line counts, header handling |
| **MergeContent** | 🟢 | Content aggregation | File consolidation, batching | Configure merge strategies, size limits |
| **CompressContent** | 🟢 | Data compression | Storage optimization, transfer efficiency | Choose appropriate algorithms |
| **EncryptContent** | 🟢 | Data encryption | Security, compliance | Key management, algorithm selection |
| **ExecuteScript** | 🟢 | Custom scripting | Complex transformations | Script optimization, resource management |
| **UpdateAttribute** | 🟢 | Attribute modification | Metadata enrichment, routing preparation | Expression language optimization |
| **ValidateRecord** | 🟢 | Data validation | Quality assurance, schema enforcement | Schema caching, validation rules |

### Data Routing Processors
| Processor | Status | Routing Logic | Use Cases | Performance Considerations |
|-----------|--------|---------------|-----------|---------------------------|
| **RouteOnAttribute** | 🟢 | Attribute-based | Content routing, filtering | Expression evaluation efficiency |
| **RouteOnContent** | 🟢 | Content-based | Pattern matching, classification | Regex compilation, streaming |
| **DistributeLoad** | 🟢 | Load balancing | Traffic distribution, scaling | Round-robin efficiency |
| **ControlRate** | 🟢 | Rate limiting | Throttling, backpressure | Timer precision, queue management |
| **RouteText** | 🟢 | Text-based routing | Log processing, content filtering | Pattern optimization |
| **ScanContent** | 🟢 | Content scanning | Security, compliance | Scan rule efficiency |
| **DetectDuplicate** | 🟢 | Deduplication | Data quality, uniqueness | Cache management, hash algorithms |

### Data Output Processors
| Processor | Status | Destinations | Key Features | Optimization Tips |
|-----------|--------|--------------|--------------|-------------------|
| **PutFile** | 🟢 | Local filesystem | File output, archiving | Directory structure, conflict resolution |
| **PutSFTP** | 🟢 | SFTP servers | Secure file transfer | Connection reuse, batch transfers |
| **PutHTTP** | 🟢 | HTTP/HTTPS endpoints | REST API publishing | Connection pooling, retry logic |
| **PutKafka** | 🟢 | Apache Kafka | Stream publishing | Producer configuration, batching |
| **PutJMS** | 🟢 | JMS message queues | Message publishing | Transaction management, acknowledgments |
| **PutDatabaseRecord** | 🟢 | JDBC databases | Bulk database loading | Batch size, connection pooling |
| **PutMongo** | 🟢 | MongoDB | Document insertion | Bulk operations, write concerns |
| **PutElasticsearch** | 🟢 | Elasticsearch | Index management | Bulk indexing, refresh policies |
| **PutS3Object** | 🟢 | Amazon S3 | Cloud storage | Multipart uploads, server-side encryption |
| **PutAzureBlobStorage** | 🟢 | Azure Blob Storage | Cloud storage | Block size optimization |

## 🚀 Deployment Modes Comparison

| Mode | Best For | Resource Management | Fault Tolerance | Scaling | Setup Complexity |
|------|----------|-------------------|-----------------|---------|------------------|
| **Standalone** | Development, small deployments | Single node | Limited | Manual | Minimal |
| **Cluster** | Production, high availability | Distributed | High | Horizontal | Medium |
| **Docker** | Containerized environments | Container orchestration | Medium | Container-based | Medium |
| **Kubernetes** | Cloud-native, microservices | K8s scheduler | High | Auto-scaling | High |
| **Cloud Managed** | Fully managed service | Cloud provider | High | Auto-scaling | Low |

## 📊 Data Sources & Formats

| Data Source | Read Support | Write Support | Streaming | Schema Evolution | Performance Tips |
|-------------|--------------|---------------|-----------|------------------|------------------|
| **Files (CSV, JSON, XML)** | ✅ | ✅ | Yes | Limited | Use appropriate parsers, streaming |
| **Databases (JDBC)** | ✅ | ✅ | Polling | No | Connection pooling, incremental queries |
| **Apache Kafka** | ✅ | ✅ | Yes | Yes | Consumer group management, batching |
| **JMS Queues** | ✅ | ✅ | Yes | No | Connection pooling, transaction management |
| **HTTP/REST APIs** | ✅ | ✅ | Yes | No | Connection reuse, rate limiting |
| **SFTP/FTP** | ✅ | ✅ | Polling | No | Connection pooling, keep-alive |
| **Amazon S3** | ✅ | ✅ | Polling | No | Multipart operations, encryption |
| **Azure Blob Storage** | ✅ | ✅ | Polling | No | Block size optimization |
| **Google Cloud Storage** | ✅ | ✅ | Polling | No | Resumable uploads |
| **MongoDB** | ✅ | ✅ | Change streams | Yes | Aggregation pipeline, bulk operations |
| **Elasticsearch** | ✅ | ✅ | Yes | Yes | Bulk operations, scroll API |
| **Apache Cassandra** | ✅ | ✅ | No | Limited | Prepared statements, token awareness |
| **Redis** | ✅ | ✅ | Pub/Sub | No | Connection pooling, pipelining |
| **HDFS** | ✅ | ✅ | No | No | Block size optimization |

## ⚡ Performance Optimization Features

| Feature | Category | Impact | Configuration | Use Cases |
|---------|----------|--------|---------------|-----------|
| **Connection Pooling** | I/O | High | Controller Services | Database, HTTP connections |
| **Back Pressure** | Flow Control | High | Connection settings | Prevent memory overflow |
| **Load Balancing** | Distribution | Medium | Connection configuration | Multi-node processing |
| **Caching** | Memory | Medium | Processor settings | Lookup tables, transformations |
| **Compression** | I/O | Medium | Content processors | Network transfer, storage |
| **Streaming Processing** | Memory | High | Processor design | Large file handling |
| **Batch Processing** | Throughput | High | Processor configuration | High-volume data |
| **Parallel Processing** | CPU | High | Concurrent tasks | Multi-core utilization |
| **Expression Compilation** | CPU | Medium | Automatic | Attribute evaluation |
| **Content Claiming** | Memory | High | Repository configuration | Memory management |

## 🔧 Configuration Categories

### Memory Management
| Parameter | Default | Description | Tuning Guidelines |
|-----------|---------|-------------|-------------------|
| `nifi.jvm.heap.init` | 512m | Initial heap size | Set to same as max heap |
| `nifi.jvm.heap.max` | 512m | Maximum heap size | 50-75% of system memory |
| `nifi.content.claim.max.appendable.size` | 10 MB | Max content claim size | Adjust based on data size |
| `nifi.content.claim.max.flow.files` | 100 | Max FlowFiles per claim | Balance memory vs I/O |

### Threading & Concurrency
| Parameter | Default | Description | Tuning Guidelines |
|-----------|---------|-------------|-------------------|
| `nifi.flow.engine.threads` | 10 | Flow engine threads | 2x number of CPU cores |
| `nifi.administrative.yield.duration` | 30 sec | Administrative yield | Adjust for responsiveness |
| `nifi.bored.yield.duration` | 10 millis | Processor yield when no work | Balance CPU usage |
| `nifi.processor.scheduling.timeout` | 1 min | Processor scheduling timeout | Increase for slow processors |

### Repository Configuration
| Parameter | Default | Description | Tuning Guidelines |
|-----------|---------|-------------|-------------------|
| `nifi.flowfile.repository.partitions` | 256 | FlowFile repository partitions | Increase for high throughput |
| `nifi.flowfile.repository.checkpoint.interval` | 2 mins | Checkpoint interval | Balance recovery vs performance |
| `nifi.content.repository.archive.max.retention.period` | 12 hours | Content retention | Adjust based on storage |
| `nifi.provenance.repository.max.storage.time` | 24 hours | Provenance retention | Balance compliance vs storage |

### Network & Security
| Parameter | Default | Description | Tuning Guidelines |
|-----------|---------|-------------|-------------------|
| `nifi.web.http.port` | 8080 | HTTP port | Use HTTPS in production |
| `nifi.web.https.port` | 8443 | HTTPS port | Configure SSL certificates |
| `nifi.cluster.node.protocol.port` | 11443 | Cluster communication port | Ensure firewall access |
| `nifi.zookeeper.connect.string` | localhost:2181 | ZooKeeper connection | Use ensemble for HA |

## 🌐 Ecosystem Integrations

| Tool/Platform | Integration Type | NiFi Component | Key Features | Setup Complexity |
|---------------|------------------|----------------|--------------|------------------|
| **Apache Kafka** | Stream Processing | Kafka processors | Real-time ingestion, publishing | Medium |
| **Elasticsearch** | Search & Analytics | Elasticsearch processors | Full-text search, log analytics | Medium |
| **Apache Hadoop** | Big Data Storage | HDFS processors | Distributed storage, batch processing | High |
| **Apache Spark** | Data Processing | Custom processors | Large-scale analytics | High |
| **MongoDB** | Document Database | MongoDB processors | Document storage, aggregation | Medium |
| **PostgreSQL/MySQL** | Relational Database | JDBC processors | Structured data, transactions | Low |
| **Amazon S3** | Cloud Storage | S3 processors | Scalable storage, data lakes | Medium |
| **Azure Data Lake** | Cloud Storage | Azure processors | Enterprise data lakes | Medium |
| **Google Cloud Storage** | Cloud Storage | GCS processors | Multi-region storage | Medium |
| **Apache Cassandra** | NoSQL Database | Cassandra processors | Distributed database | High |
| **Redis** | In-Memory Cache | Redis processors | Caching, session storage | Low |
| **Apache Solr** | Search Platform | Solr processors | Enterprise search | Medium |
| **InfluxDB** | Time Series DB | InfluxDB processors | Metrics, monitoring data | Medium |
| **Prometheus** | Monitoring | Metrics reporting | System monitoring | Medium |
| **Grafana** | Visualization | Metrics integration | Dashboard creation | Low |

## 📈 Performance Benchmarks & Limits

| Metric | Small Deployment | Medium Deployment | Large Deployment | Notes |
|--------|------------------|-------------------|------------------|-------|
| **Max Nodes** | 1 | 3-10 | 50+ | Limited by network and coordination |
| **Max Processors per Flow** | 100 | 500 | 2000+ | UI performance may degrade |
| **Max Concurrent Tasks** | 50 | 200 | 1000+ | Limited by CPU and memory |
| **Max FlowFiles in Queue** | 10K | 100K | 1M+ | Limited by memory and disk |
| **Max Throughput (records/sec)** | 1K | 10K | 100K+ | Depends on data size and complexity |
| **Max Data Rate (MB/sec)** | 10 | 100 | 1000+ | Network and I/O dependent |
| **Max Flow Complexity** | Simple | Medium | Complex | Affects maintainability |
| **Recommended Heap Size** | 2-4GB | 8-16GB | 32GB+ | Balance with system memory |

## 🔍 Monitoring & Debugging

| Tool/Feature | Purpose | Access Method | Key Metrics | Best Practices |
|--------------|---------|---------------|-------------|----------------|
| **NiFi UI** | Real-time monitoring | Web interface | Processor status, queue depth | Monitor during development |
| **System Diagnostics** | Resource monitoring | UI diagnostics page | CPU, memory, disk usage | Regular health checks |
| **Data Provenance** | Lineage tracking | Provenance UI | Event history, data flow | Enable for compliance |
| **Bulletins** | Error tracking | UI bulletins | Error messages, warnings | Configure appropriate levels |
| **Logs** | Detailed debugging | Log files | Application logs, audit logs | Centralized log management |
| **JMX Metrics** | System monitoring | JMX endpoints | JVM metrics, custom metrics | Integrate with monitoring tools |
| **REST API** | Programmatic access | HTTP endpoints | All UI functionality | Automation and integration |
| **Cluster Status** | Multi-node monitoring | Cluster page | Node health, coordination | Monitor cluster stability |

## 🚨 Common Issues & Solutions

| Issue | Symptoms | Root Cause | Solution | Prevention |
|-------|----------|------------|----------|-----------|
| **OutOfMemoryError** | JVM crashes, slow performance | Insufficient heap, memory leaks | Increase heap size, optimize flows | Monitor memory usage, tune GC |
| **Back Pressure** | Queues filling up, slow processing | Downstream bottlenecks | Increase concurrent tasks, optimize processors | Monitor queue depths |
| **Connection Timeouts** | Processor failures, network errors | Network issues, firewall blocks | Increase timeouts, check connectivity | Network monitoring, proper configuration |
| **Disk Space Issues** | Repository errors, performance degradation | Insufficient disk space | Clean repositories, increase storage | Monitor disk usage, configure retention |
| **Cluster Coordination Issues** | Node disconnections, split brain | ZooKeeper problems, network partitions | Fix ZooKeeper, network issues | Proper ZooKeeper setup, network stability |
| **Slow UI Performance** | Unresponsive interface | Complex flows, many processors | Simplify flows, use process groups | Design modular flows |
| **Data Loss** | Missing FlowFiles | Repository corruption, improper shutdown | Restore from backup, fix repositories | Regular backups, graceful shutdowns |
| **Security Issues** | Unauthorized access | Misconfigured security | Proper authentication, authorization | Security best practices, regular audits |

## 🔄 Version Compatibility

| NiFi Version | Release Date | Key Features | End of Support | Recommended For |
|--------------|--------------|--------------|----------------|-----------------|
| **1.25.x** | 2024 | Python processors, enhanced security | Active | Latest features, new deployments |
| **1.24.x** | 2023 | Improved clustering, performance | Active | Production workloads |
| **1.23.x** | 2023 | Enhanced monitoring, bug fixes | Active | Stable production |
| **1.22.x** | 2023 | Security improvements, new processors | Extended | Migration path |
| **1.21.x** | 2022 | Kubernetes support, cloud integrations | Extended | Cloud deployments |
| **1.20.x** | 2022 | Performance improvements | EOL | Legacy compatibility |
| **1.19.x** | 2022 | Enhanced UI, new processors | EOL | Legacy systems only |

## ⚡ Quick Reference Commands

### NiFi Toolkit Commands
```bash
# Start NiFi
./bin/nifi.sh start

# Stop NiFi
./bin/nifi.sh stop

# Check status
./bin/nifi.sh status

# Install processor
./bin/nifi.sh install-processor /path/to/processor.nar

# Encrypt sensitive properties
./bin/encrypt-config.sh -n nifi.properties -b bootstrap.conf
```

### REST API Examples
```bash
# Get cluster summary
curl -X GET http://localhost:8080/nifi-api/controller/cluster

# Get process groups
curl -X GET http://localhost:8080/nifi-api/flow/process-groups/root

# Start processor
curl -X PUT http://localhost:8080/nifi-api/processors/{id}/run-status \
  -H "Content-Type: application/json" \
  -d '{"revision":{"version":1},"state":"RUNNING"}'
```

### Performance Tuning Quick Wins
```properties
# Increase heap size
nifi.jvm.heap.init=8g
nifi.jvm.heap.max=8g

# Optimize repositories
nifi.flowfile.repository.partitions=512
nifi.content.claim.max.appendable.size=50MB

# Enable compression
nifi.content.repository.archive.enabled=true
```

### Expression Language Examples
```
# File operations
${filename:substringBeforeLast('.')}
${now():format('yyyy-MM-dd HH:mm:ss')}

# Conditional logic
${fileSize:toNumber():gt(1000):ifElse('large', 'small')}

# String manipulation
${data:replace('old', 'new'):toUpper()}
```

## 📚 Related Resources

### Internal Links
- [NiFi Interview Questions](./APACHE_NIFI_INTERVIEW_QUESTIONS.md)
- [NiFi Key Concepts](./APACHE_NIFI_KEY_CONCEPTS.md)
- [NiFi Best Practices](./APACHE_NIFI_BEST_PRACTICES.md)
- [ETL Tools Comparison](../ETL_COMPREHENSIVE_INTERVIEW_QUESTIONS.md)

### External Resources
- [Apache NiFi Documentation](https://nifi.apache.org/docs.html)
- [NiFi Expression Language Guide](https://nifi.apache.org/docs/nifi-docs/html/expression-language-guide.html)
- [NiFi Processor Documentation](https://nifi.apache.org/docs/nifi-docs/components/)
- [NiFi Community](https://nifi.apache.org/mailing_lists.html)

## 🎓 Learning Path & Certification

| Level | Topics | Hands-on Projects | Skills Developed | Time Investment |
|-------|--------|-------------------|------------------|-----------------|
| **Beginner** | Basic concepts, UI navigation | Simple file processing | Flow design, basic processors | 2-4 weeks |
| **Intermediate** | Advanced processors, clustering | ETL pipelines, error handling | Performance tuning, monitoring | 2-3 months |
| **Advanced** | Custom processors, security | Enterprise integration, automation | Architecture design, optimization | 4-6 months |
| **Expert** | Internals, extensions | Custom components, contributions | Framework development | 6+ months |

## 🆚 NiFi vs Alternatives

| Tool | Best For | NiFi Advantage | Alternative Advantage | When to Choose NiFi |
|------|---------|----------------|----------------------|---------------------|
| **Apache Airflow** | Workflow orchestration | Visual flow design, real-time | Better for complex DAGs | Data flow automation, real-time processing |
| **Apache Kafka Connect** | Kafka integration | General-purpose flows | Native Kafka integration | Beyond Kafka ecosystems |
| **Talend** | Enterprise ETL | Open source, flexibility | Commercial support, GUI | Cost-conscious, customization needed |
| **Informatica** | Enterprise data integration | Lower cost, open source | Mature enterprise features | Budget constraints, open source preference |
| **StreamSets** | DataOps pipelines | Broader ecosystem | Modern UI, cloud-native | On-premises or hybrid deployments |
| **AWS Glue** | Cloud ETL | On-premises capability | Serverless, managed | Multi-cloud or on-premises requirements |

---

**Last Updated**: 2024  
**NiFi Version Coverage**: 1.20 - 1.25.x