# Debezium - Interview Questions

## Basic Concepts

### 1. What is Debezium and how does it implement Change Data Capture?
**Answer:** Debezium is an open-source CDC platform that captures database changes in real-time:
- **Log-based CDC**: Reads database transaction logs (binlog, WAL, oplog)
- **Kafka integration**: Streams changes to Apache Kafka
- **Real-time**: Near real-time change capture with low latency
- **Complete history**: Captures all insert, update, delete operations
- **Minimal impact**: Low overhead on source databases
- **Event sourcing**: Maintains complete change history

### 2. What databases does Debezium support and how does it connect to them?
**Answer:** Debezium supports multiple databases:
- **MySQL**: Uses binlog for change capture
- **PostgreSQL**: Uses logical replication slots
- **SQL Server**: Uses Change Data Capture feature
- **Oracle**: Uses LogMiner and XStream
- **MongoDB**: Uses oplog (operations log)
- **Db2**: Uses SQL replication
- **Cassandra**: Uses commit log

### 3. Explain the structure of a Debezium change event.
**Answer:** Debezium change events contain:
- **before**: Record state before the change (null for inserts)
- **after**: Record state after the change (null for deletes)
- **source**: Metadata about the change (timestamp, position, table)
- **op**: Operation type (c=create, u=update, d=delete, r=read)
- **ts_ms**: Event timestamp in milliseconds
- **transaction**: Transaction metadata (if available)

### 4. What is the difference between snapshot and streaming modes in Debezium?
**Answer:**
- **Snapshot mode**: Captures existing data at startup (initial state)
- **Streaming mode**: Captures ongoing changes from transaction logs
- **Combined approach**: Typically starts with snapshot, then switches to streaming
- **Incremental snapshots**: Capture large tables without blocking
- **Resumable**: Can resume interrupted snapshots

### 5. How does Debezium handle schema evolution?
**Answer:** Schema evolution handling:
- **Automatic detection**: Detects DDL changes automatically
- **Schema registry**: Integrates with Confluent Schema Registry
- **Backward compatibility**: Maintains compatibility with consumers
- **Schema history**: Tracks schema changes over time
- **Avro schemas**: Generates Avro schemas for events
- **Validation**: Validates schema changes before applying

## Intermediate Concepts

### 6. How do you configure filtering in Debezium connectors?
**Answer:** Debezium filtering options:
- **Database filtering**: `database.include.list`, `database.exclude.list`
- **Table filtering**: `table.include.list`, `table.exclude.list`
- **Column filtering**: `column.include.list`, `column.exclude.list`
- **Content filtering**: Custom predicates for record content
- **Regex patterns**: Use regular expressions for flexible filtering
- **Transformations**: Apply Kafka Connect transformations

### 7. Explain Debezium's approach to handling large transactions.
**Answer:** Large transaction handling:
- **Incremental processing**: Process large transactions incrementally
- **Memory management**: Avoid memory overflow with large transactions
- **Buffering**: Buffer transaction events until commit
- **Timeout handling**: Handle long-running transactions
- **Monitoring**: Track transaction size and duration
- **Configuration**: Tune buffer sizes and timeouts

### 8. How does Debezium ensure exactly-once delivery?
**Answer:** Exactly-once delivery mechanisms:
- **Kafka transactions**: Use Kafka's transactional capabilities
- **Idempotent producers**: Ensure idempotent message production
- **Offset management**: Careful offset tracking and commits
- **Connector restarts**: Handle restarts without duplicates
- **Source position tracking**: Track database log positions
- **Consumer idempotency**: Design consumers to handle duplicates

### 9. What are the different deployment options for Debezium?
**Answer:** Deployment options:
- **Kafka Connect Distributed**: Scalable, fault-tolerant deployment
- **Kafka Connect Standalone**: Single-node deployment for testing
- **Debezium Engine**: Embedded in custom applications
- **Kubernetes**: Container-based deployment with operators
- **Cloud services**: Managed Kafka Connect services
- **Docker**: Containerized deployment

### 10. How do you monitor Debezium connector performance?
**Answer:** Monitoring approaches:
- **JMX metrics**: Connector-specific performance metrics
- **Kafka metrics**: Topic lag, throughput, error rates
- **Database metrics**: Source database performance impact
- **Custom dashboards**: Grafana, Kibana visualizations
- **Alerting**: Set up alerts for lag, errors, failures
- **Health checks**: Regular connector health monitoring

## Advanced Concepts

### 11. Design a real-time data synchronization system using Debezium.
**Answer:** Real-time sync architecture:
```
Source DB → Debezium → Kafka → Stream Processor → Target Systems
```
- **Multi-source**: Capture from multiple databases
- **Transformation**: Apply business logic transformations
- **Routing**: Route changes to appropriate targets
- **Conflict resolution**: Handle concurrent updates
- **Monitoring**: Track sync lag and data quality
- **Recovery**: Handle failures and catch-up scenarios

### 12. How would you implement event sourcing with Debezium?
**Answer:** Event sourcing implementation:
- **Event store**: Use Kafka as the event store
- **Event capture**: Debezium captures all database changes
- **Event replay**: Rebuild state from event history
- **Snapshots**: Periodic snapshots for performance
- **Projections**: Create read models from events
- **Versioning**: Handle event schema evolution
- **Retention**: Configure appropriate event retention

### 13. Describe implementing a data lake ingestion pipeline with Debezium.
**Answer:** Data lake ingestion:
```
Databases → Debezium → Kafka → Kafka Connect → Data Lake
```
- **Change capture**: Real-time database change capture
- **Format conversion**: Convert to Parquet, Avro, or Delta
- **Partitioning**: Partition data by date, source, or other keys
- **Schema management**: Handle schema evolution in data lake
- **Compaction**: Implement log compaction for efficiency
- **Metadata**: Maintain data catalog and lineage

### 14. How do you handle Debezium connector failures and recovery?
**Answer:** Failure handling and recovery:
- **Automatic restart**: Configure automatic connector restart
- **Offset tracking**: Maintain accurate offset positions
- **State recovery**: Recover from last known good state
- **Error handling**: Handle transient vs. permanent errors
- **Dead letter queues**: Route problematic records
- **Monitoring**: Proactive failure detection
- **Runbooks**: Document recovery procedures

### 15. Explain how to implement cross-region replication with Debezium.
**Answer:** Cross-region replication:
- **Multi-region Kafka**: Deploy Kafka across regions
- **Network optimization**: Optimize cross-region connectivity
- **Conflict resolution**: Handle concurrent updates across regions
- **Disaster recovery**: Implement failover mechanisms
- **Data consistency**: Ensure eventual consistency
- **Monitoring**: Track cross-region lag and performance
- **Cost optimization**: Optimize data transfer costs

## Real-world Scenarios

### 16. How would you migrate from batch ETL to real-time CDC with Debezium?
**Answer:** Migration strategy:
1. **Assessment**: Analyze current ETL processes and dependencies
2. **Pilot**: Start with non-critical tables and processes
3. **Parallel processing**: Run both batch and CDC initially
4. **Data validation**: Compare results between systems
5. **Performance testing**: Ensure adequate performance
6. **Gradual migration**: Move workloads incrementally
7. **Consumer migration**: Update downstream consumers
8. **Monitoring**: Implement comprehensive monitoring
9. **Decommission**: Remove batch processes after validation

### 17. Design a microservices data integration strategy using Debezium.
**Answer:** Microservices integration:
- **Database per service**: Each service owns its data
- **Event publishing**: Debezium publishes domain events
- **Event consumption**: Services consume relevant events
- **Saga patterns**: Implement distributed transactions
- **CQRS**: Separate command and query models
- **Event sourcing**: Maintain complete event history
- **Service boundaries**: Respect service boundaries
- **Schema evolution**: Handle schema changes gracefully

### 18. How do you implement data compliance and privacy with Debezium?
**Answer:** Compliance implementation:
- **Data classification**: Identify sensitive data types
- **Field masking**: Mask PII fields in change events
- **Encryption**: Encrypt sensitive data in transit
- **Access controls**: Implement role-based access
- **Audit trails**: Maintain complete audit logs
- **Data retention**: Implement data lifecycle policies
- **Right to be forgotten**: Handle data deletion requests
- **Compliance reporting**: Generate compliance reports

### 19. What monitoring and alerting would you set up for Debezium?
**Answer:** Comprehensive monitoring:
- **Connector health**: Monitor connector status and uptime
- **Replication lag**: Track lag between source and Kafka
- **Throughput metrics**: Monitor events per second
- **Error rates**: Track connector and processing errors
- **Resource usage**: Monitor CPU, memory, network usage
- **Database impact**: Monitor source database performance
- **Schema changes**: Alert on schema evolution events
- **SLA monitoring**: Track data freshness SLAs

### 20. How would you troubleshoot a Debezium connector that stopped processing changes?
**Answer:** Troubleshooting process:
1. **Status check**: Verify connector status and error messages
2. **Log analysis**: Examine connector and Kafka Connect logs
3. **Database connectivity**: Check database connection and permissions
4. **Log position**: Verify database log position and availability
5. **Resource check**: Check CPU, memory, disk space
6. **Configuration validation**: Verify connector configuration
7. **Network issues**: Check network connectivity and firewall
8. **Recovery actions**: Restart connector, reset offsets if needed
9. **Root cause analysis**: Identify and fix underlying issues
10. **Prevention**: Update monitoring and error handling