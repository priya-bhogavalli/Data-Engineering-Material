# Amazon Athena Interview Questions

## Table of Contents

1. [Basic Athena Questions](#basic-athena-questions)
2. [Architecture & Performance](#architecture--performance)
3. [Data Formats & Partitioning](#data-formats--partitioning)
4. [Query Optimization](#query-optimization)
5. [Security & Access Control](#security--access-control)
6. [Integration & Advanced Topics](#integration--advanced-topics)
7. [Scenario-Based Questions](#scenario-based-questions)

---

## Basic Athena Questions

### 1. What is Amazon Athena and what are its key benefits?
**Answer:**
Amazon Athena is a serverless, interactive query service that makes it easy to analyze data in S3 using standard SQL.

**Key Benefits:**
- **Serverless**: No infrastructure to manage or provision
- **Pay-per-query**: Only pay for queries you run
- **Standard SQL**: Uses Presto engine with ANSI SQL support
- **Fast**: Parallel execution across multiple nodes
- **Integrated**: Works seamlessly with AWS Glue Data Catalog

### 2. How does Athena differ from traditional databases?
**Answer:**
- **Storage**: Data remains in S3, not moved to database storage
- **Schema-on-Read**: Schema applied when querying, not when storing
- **Serverless**: No servers to manage or maintain
- **Cost Model**: Pay per TB of data scanned, not for compute time
- **Use Case**: Optimized for analytics, not transactional workloads

### 3. What is the underlying engine that powers Athena?
**Answer:**
- **Presto**: Distributed SQL query engine originally developed by Facebook
- **Version**: Athena uses a managed version of Presto
- **Architecture**: Coordinator and worker nodes for distributed processing
- **SQL Compatibility**: Supports ANSI SQL with extensions

### 4. Explain the relationship between Athena and AWS Glue Data Catalog.
**Answer:**
- **Metadata Store**: Glue Data Catalog stores table schemas and metadata
- **Automatic Discovery**: Glue crawlers can automatically discover schema
- **Shared Catalog**: Multiple services can use the same catalog
- **Table Definitions**: Athena uses catalog to understand data structure

### 5. What data formats does Athena support?
**Answer:**
- **Structured**: CSV, TSV, JSON, Apache Parquet, Apache ORC
- **Semi-structured**: JSON, Apache Avro
- **Compressed**: GZIP, LZO, Snappy, BZIP2
- **Columnar**: Parquet and ORC (recommended for performance)

## Architecture & Performance

### 6. How does Athena execute queries?
**Answer:**
1. **Query Parsing**: SQL parsed and validated
2. **Planning**: Query execution plan created
3. **Resource Allocation**: Compute resources allocated dynamically
4. **Parallel Execution**: Query executed across multiple nodes
5. **Result Assembly**: Results collected and returned to user

### 7. What factors affect Athena query performance?
**Answer:**
- **Data Format**: Columnar formats (Parquet, ORC) perform better
- **Compression**: Reduces data transfer and I/O
- **Partitioning**: Limits data scanned by queries
- **File Size**: Optimal file sizes (128MB - 1GB)
- **Query Structure**: Efficient WHERE clauses and JOINs

### 8. Explain Athena's pricing model.
**Answer:**
- **Per Query**: $5.00 per TB of data scanned
- **Minimum Charge**: 10MB per query
- **Data Transfer**: No charge for data transfer from S3
- **Metadata**: No charge for DDL operations
- **Failed Queries**: No charge for cancelled queries

### 9. How can you reduce Athena costs?
**Answer:**
- **Columnar Formats**: Use Parquet or ORC to reduce data scanned
- **Compression**: Compress data to reduce scan volume
- **Partitioning**: Partition data to limit scan scope
- **Query Optimization**: Use specific columns instead of SELECT *
- **Result Caching**: Leverage query result caching

### 10. What are Athena workgroups and their benefits?
**Answer:**
**Workgroups** separate users, teams, or applications:
- **Resource Management**: Control query concurrency and data usage
- **Cost Control**: Set per-query and per-workgroup data usage limits
- **Security**: Isolate queries and results
- **Configuration**: Different settings per workgroup

## Data Formats & Partitioning

### 11. Why is partitioning important in Athena?
**Answer:**
- **Performance**: Reduces amount of data scanned
- **Cost**: Lower costs due to less data processed
- **Query Speed**: Faster query execution
- **Partition Pruning**: Athena automatically excludes irrelevant partitions

### 12. What are the best practices for partitioning in Athena?
**Answer:**
- **Partition Keys**: Use commonly filtered columns (date, region, etc.)
- **Cardinality**: Avoid high cardinality partition keys
- **Size**: Each partition should contain substantial data (>128MB)
- **Hierarchy**: Use hierarchical partitioning (year/month/day)
- **Limit**: Maximum 20,000 partitions per table

### 13. How do you handle schema evolution in Athena?
**Answer:**
- **Schema-on-Read**: New columns automatically detected
- **ALTER TABLE**: Add new columns or partitions
- **SerDe Properties**: Configure serialization/deserialization
- **Data Types**: Handle type changes carefully
- **Backward Compatibility**: Ensure new schema works with old data

### 14. What is the difference between Hive-style and non-Hive partitioning?
**Answer:**
**Hive-style**: `s3://bucket/year=2023/month=01/day=15/`
- Partition keys in directory names
- Automatic partition discovery

**Non-Hive**: `s3://bucket/2023/01/15/`
- Manual partition registration required
- More flexible directory structure

### 15. How do you optimize file sizes for Athena?
**Answer:**
- **Optimal Size**: 128MB to 1GB per file
- **Avoid Small Files**: Many small files increase query overhead
- **Compaction**: Regularly compact small files
- **Parallel Processing**: Larger files enable better parallelization

## Query Optimization

### 16. What are common Athena query optimization techniques?
**Answer:**
- **Column Selection**: Use specific columns instead of SELECT *
- **WHERE Clauses**: Filter early and on partition keys
- **JOIN Optimization**: Put smaller tables on the right side
- **Data Types**: Use appropriate data types for better performance
- **LIMIT**: Use LIMIT for exploratory queries

### 17. How do you troubleshoot slow Athena queries?
**Answer:**
1. **Query History**: Check query execution details
2. **Data Scanned**: Analyze amount of data processed
3. **Execution Plan**: Review query execution plan
4. **Partitioning**: Ensure proper partition pruning
5. **File Format**: Consider converting to columnar format

### 18. Explain the EXPLAIN statement in Athena.
**Answer:**
```sql
EXPLAIN SELECT * FROM table WHERE date = '2023-01-01';
```
Shows query execution plan:
- **Logical Plan**: High-level query structure
- **Physical Plan**: Actual execution steps
- **Cost Estimates**: Relative costs of operations
- **Data Sources**: Tables and partitions accessed

### 19. How do you handle large JOIN operations in Athena?
**Answer:**
- **Broadcast JOIN**: For small tables (< 100MB)
- **Partitioned JOIN**: Join on partition keys when possible
- **Bucketing**: Pre-sort and bucket large tables
- **Query Structure**: Filter before joining
- **Memory Limits**: Be aware of query memory constraints

### 20. What are Athena query result caching benefits?
**Answer:**
- **Performance**: Instant results for repeated queries
- **Cost Savings**: No re-scanning of data
- **Duration**: Results cached for 24 hours
- **Automatic**: Enabled by default for identical queries

## Security & Access Control

### 21. How do you secure data access in Athena?
**Answer:**
- **IAM Policies**: Control access to Athena and S3 resources
- **S3 Bucket Policies**: Restrict access to underlying data
- **Workgroups**: Isolate users and control resource usage
- **Encryption**: Encrypt data at rest and in transit
- **VPC Endpoints**: Private connectivity to Athena

### 22. What encryption options are available in Athena?
**Answer:**
- **S3 Encryption**: SSE-S3, SSE-KMS, SSE-C for source data
- **Query Results**: Encrypt results stored in S3
- **In Transit**: TLS encryption for API calls
- **Client-side**: Application-level encryption

### 23. How do you implement fine-grained access control?
**Answer:**
- **Column-level Security**: Use views to restrict column access
- **Row-level Security**: Filter data based on user attributes
- **Lake Formation**: Use AWS Lake Formation for advanced permissions
- **IAM Conditions**: Use condition keys for dynamic access control

## Integration & Advanced Topics

### 24. How does Athena integrate with other AWS services?
**Answer:**
- **S3**: Primary data source and result storage
- **Glue**: Data catalog and ETL integration
- **QuickSight**: Business intelligence and visualization
- **Lambda**: Serverless query execution triggers
- **CloudFormation**: Infrastructure as code deployment

### 25. What is Athena Federated Query?
**Answer:**
Allows querying data sources beyond S3:
- **Data Sources**: RDS, DynamoDB, ElastiCache, on-premises databases
- **Lambda Connectors**: Custom connectors for various data sources
- **JOIN Operations**: Join data across different sources
- **Real-time**: Query live data without ETL

### 26. How do you use Athena with streaming data?
**Answer:**
- **Kinesis Data Firehose**: Stream data to S3 for Athena queries
- **Partitioning**: Partition by time for efficient querying
- **Near Real-time**: Query data with minimal delay
- **Compaction**: Regular compaction of small streaming files

### 27. What are Athena prepared statements?
**Answer:**
```sql
PREPARE my_query FROM 'SELECT * FROM table WHERE id = ?';
EXECUTE my_query USING 123;
```
- **Performance**: Avoid query parsing overhead
- **Security**: Prevent SQL injection
- **Reusability**: Execute same query with different parameters

## Scenario-Based Questions

### 28. You need to analyze 5 years of web logs stored in S3. How do you optimize for Athena?
**Answer:**
1. **Partitioning**: Partition by year/month/day
2. **File Format**: Convert to Parquet with compression
3. **Schema Design**: Define appropriate data types
4. **Glue Crawler**: Set up crawler for automatic schema discovery
5. **Workgroups**: Create workgroup with appropriate limits
6. **Query Patterns**: Optimize for common query patterns

### 29. Your Athena queries are expensive. How do you reduce costs?
**Answer:**
1. **Analyze Usage**: Review query history and data scanned
2. **Optimize Format**: Convert to columnar format (Parquet/ORC)
3. **Improve Partitioning**: Better partition strategy
4. **Query Optimization**: Use specific columns, add WHERE clauses
5. **Compression**: Implement data compression
6. **Lifecycle Policies**: Archive old data to cheaper storage classes

### 30. How would you migrate from a traditional data warehouse to Athena?
**Answer:**
1. **Assessment**: Analyze current queries and data patterns
2. **Data Migration**: Export data to S3 in optimized format
3. **Schema Mapping**: Map existing schema to Athena tables
4. **Query Translation**: Convert proprietary SQL to standard SQL
5. **Performance Testing**: Validate query performance
6. **Gradual Migration**: Phase migration to minimize risk

### 31. You need to join data from Athena with real-time data from RDS. What's your approach?
**Answer:**
1. **Federated Query**: Use Athena federated query connectors
2. **Lambda Connector**: Deploy RDS connector for Athena
3. **Data Freshness**: Consider data latency requirements
4. **Performance**: Optimize JOIN operations
5. **Alternative**: ETL real-time data to S3 for better performance

### 32. How do you handle PII data in Athena queries?
**Answer:**
1. **Data Masking**: Mask sensitive data at source
2. **Column-level Security**: Use views to restrict PII access
3. **Encryption**: Encrypt PII data in S3
4. **Access Control**: Strict IAM policies for PII access
5. **Audit Logging**: Enable CloudTrail for query auditing
6. **Data Classification**: Use Macie for automatic PII detection

---

## Key Takeaways for Interviews

1. **Serverless Nature**: Understand the benefits and limitations of serverless architecture
2. **Cost Optimization**: Focus on techniques to reduce data scanning costs
3. **Performance**: Know how partitioning and file formats affect performance
4. **Integration**: Understand how Athena fits in the AWS ecosystem
5. **Security**: Be familiar with access control and encryption options
6. **Query Optimization**: Practice writing efficient SQL for large datasets
7. **Troubleshooting**: Know how to identify and resolve performance issues
8. **Real-world Scenarios**: Prepare for practical implementation questions