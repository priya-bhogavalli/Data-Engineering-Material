# Amazon Kinesis - Interview Questions

## Basic Concepts

### 1. What is Amazon Kinesis and what are its main components?
**Answer:** Amazon Kinesis is a platform for streaming data on AWS that makes it easy to collect, process, and analyze real-time, streaming data. Main components:
- **Kinesis Data Streams**: Real-time data streaming service
- **Kinesis Data Firehose**: Fully managed delivery service
- **Kinesis Data Analytics**: Real-time analytics using SQL
- **Kinesis Video Streams**: Video streaming service

### 2. What is a shard in Kinesis Data Streams?
**Answer:** A shard is the base throughput unit of a Kinesis data stream. Each shard can:
- Support up to 1,000 records per second for writes
- Support up to 1 MB per second for writes
- Support up to 2 MB per second for reads
- Support up to 5 transactions per second for reads

### 3. How does Kinesis ensure data durability?
**Answer:** Kinesis ensures durability through:
- **Multi-AZ replication**: Data is replicated across multiple availability zones
- **Configurable retention**: Data retained from 24 hours to 365 days
- **Automatic backup**: Built-in data persistence
- **Checkpointing**: Track processing progress for recovery

### 4. What is the difference between Kinesis Data Streams and Kinesis Data Firehose?
**Answer:**
- **Data Streams**: Real-time processing, custom applications, manual scaling, pay per shard
- **Data Firehose**: Near real-time delivery, managed service, auto-scaling, pay per data volume

### 5. How do you handle scaling in Kinesis Data Streams?
**Answer:** Scaling options include:
- **Resharding**: Split shards to increase capacity or merge to reduce costs
- **Auto Scaling**: Use Application Auto Scaling for automatic adjustment
- **Partition key design**: Ensure even distribution across shards
- **Monitoring**: Use CloudWatch metrics to track utilization

## Intermediate Concepts

### 6. Explain partition keys and their importance in Kinesis.
**Answer:** Partition keys determine which shard a record goes to:
- **Hash function**: Kinesis uses MD5 hash of partition key
- **Even distribution**: Good partition key design prevents hot shards
- **Ordering**: Records with same partition key maintain order within shard
- **Best practices**: Use high-cardinality keys, avoid sequential patterns

### 7. What are the different types of windowing in Kinesis Data Analytics?
**Answer:**
- **Tumbling windows**: Fixed-size, non-overlapping time intervals
- **Sliding windows**: Fixed-size, overlapping time intervals
- **Session windows**: Variable-size based on activity gaps
- **Custom windows**: User-defined window logic

### 8. How do you implement exactly-once processing in Kinesis?
**Answer:** Strategies include:
- **Checkpointing**: Use KCL checkpointing mechanism
- **Idempotent operations**: Design operations to be safely retried
- **Deduplication**: Implement application-level deduplication
- **Sequence numbers**: Use for ordering and duplicate detection

### 9. What is the Kinesis Client Library (KCL)?
**Answer:** KCL is a library that helps build applications that process data from Kinesis Data Streams:
- **Load balancing**: Automatically distributes shards across workers
- **Fault tolerance**: Handles worker failures and recovery
- **Checkpointing**: Tracks processing progress
- **Scaling**: Automatically adjusts to shard count changes

### 10. How do you monitor Kinesis performance?
**Answer:** Monitoring approaches:
- **CloudWatch metrics**: IncomingRecords, OutgoingRecords, IteratorAge
- **Custom metrics**: Application-specific performance indicators
- **Alarms**: Set up proactive alerting for threshold breaches
- **Dashboards**: Visualize key performance metrics

## Advanced Concepts

### 11. Describe a real-time analytics architecture using Kinesis.
**Answer:**
```
Data Sources → Kinesis Data Streams → Kinesis Analytics → 
Lambda/Kinesis Firehose → S3/Redshift → QuickSight
```
- **Ingestion**: Multiple producers send data to streams
- **Processing**: Real-time SQL queries in Analytics
- **Storage**: Results stored in data lake/warehouse
- **Visualization**: Dashboards for business insights

### 12. How do you handle backpressure in Kinesis applications?
**Answer:** Backpressure handling strategies:
- **Buffering**: Implement local buffering in producers
- **Throttling**: Reduce producer rate when limits hit
- **Scaling**: Add more shards to increase capacity
- **Circuit breakers**: Prevent cascade failures
- **Dead letter queues**: Handle failed records

### 13. What are the security features available in Kinesis?
**Answer:** Security features include:
- **Encryption at rest**: Server-side encryption with KMS
- **Encryption in transit**: TLS for data transmission
- **IAM integration**: Fine-grained access control
- **VPC endpoints**: Private network access
- **CloudTrail**: API call logging and auditing

### 14. How do you optimize costs in Kinesis?
**Answer:** Cost optimization strategies:
- **Right-sizing**: Monitor shard utilization and adjust
- **Reserved capacity**: For predictable workloads
- **Data retention**: Set appropriate retention periods
- **Compression**: Use in Firehose to reduce storage costs
- **Lifecycle policies**: Archive old data to cheaper storage

### 15. Explain error handling in Kinesis Data Firehose.
**Answer:** Error handling mechanisms:
- **Retry logic**: Automatic retries with exponential backoff
- **Error records**: Failed records sent to error bucket
- **Processing errors**: Transformation failures handled separately
- **Monitoring**: CloudWatch metrics for error tracking
- **Alerting**: Set up notifications for error thresholds

## Real-world Scenarios

### 16. Design a fraud detection system using Kinesis.
**Answer:**
```
Transactions → Kinesis Data Streams → Lambda (ML Model) → 
DynamoDB (Results) → SNS (Alerts)
```
- **Real-time ingestion**: Transaction data streamed continuously
- **ML processing**: Lambda functions run fraud detection models
- **Low latency**: Sub-second fraud detection
- **Alerting**: Immediate notifications for suspicious activity

### 17. How would you migrate from batch processing to stream processing with Kinesis?
**Answer:** Migration strategy:
1. **Parallel processing**: Run both batch and stream initially
2. **Data validation**: Compare results between systems
3. **Gradual cutover**: Migrate workloads incrementally
4. **Monitoring**: Ensure performance and accuracy
5. **Rollback plan**: Maintain ability to revert if needed

### 18. Describe handling seasonal traffic spikes with Kinesis.
**Answer:** Spike handling approaches:
- **Predictive scaling**: Scale proactively based on patterns
- **Auto Scaling**: Configure automatic shard adjustment
- **Buffering**: Use SQS as buffer during extreme spikes
- **Load testing**: Validate capacity before peak periods
- **Monitoring**: Real-time alerting for capacity issues

### 19. How do you implement cross-region replication with Kinesis?
**Answer:** Cross-region replication strategies:
- **Kinesis Analytics**: Process and forward to another region
- **Lambda functions**: Cross-region data replication
- **Kinesis Agent**: Multi-region data shipping
- **Application-level**: Custom replication logic
- **Disaster recovery**: Maintain secondary region for failover

### 20. What are the limitations of Kinesis and how do you work around them?
**Answer:** Common limitations and workarounds:
- **1 MB record limit**: Split large records or use S3 references
- **Shard limits**: Request limit increases or use multiple streams
- **Ordering**: Only within shard, design partition keys carefully
- **Latency**: Near real-time, not true real-time processing
- **Cost**: Can be expensive at scale, optimize shard usage