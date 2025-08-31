# Amazon DynamoDB Interview Questions

## Table of Contents

1. [Basic DynamoDB Questions](#basic-dynamodb-questions)
2. [Data Modeling](#data-modeling)
3. [Performance & Scaling](#performance--scaling)
4. [Indexes & Queries](#indexes--queries)
5. [Consistency & Transactions](#consistency--transactions)
6. [Security & Backup](#security--backup)
7. [Advanced Features](#advanced-features)
8. [Scenario-Based Questions](#scenario-based-questions)

---

## Basic DynamoDB Questions

### 1. What is Amazon DynamoDB and what are its key characteristics?
**Answer:**
Amazon DynamoDB is a fully managed NoSQL database service that provides fast and predictable performance with seamless scalability.

**Key Characteristics:**
- **Serverless**: Fully managed with no servers to provision
- **Performance**: Single-digit millisecond latency at any scale
- **Scalability**: Automatic scaling based on demand
- **Durability**: Multi-AZ replication with 99.999999999% (11 9's) durability
- **Security**: Encryption at rest and in transit, fine-grained access control

### 2. How does DynamoDB differ from relational databases?
**Answer:**
- **Schema**: Schema-less vs. fixed schema
- **Scaling**: Horizontal scaling vs. vertical scaling
- **Queries**: Key-based access vs. complex SQL queries
- **ACID**: Eventually consistent vs. ACID compliant
- **Joins**: No joins vs. complex join operations
- **Flexibility**: Flexible data structure vs. rigid table structure

### 3. What are the core components of DynamoDB?
**Answer:**
- **Tables**: Collection of items (similar to tables in RDBMS)
- **Items**: Individual records (similar to rows)
- **Attributes**: Key-value pairs within items (similar to columns)
- **Primary Key**: Uniquely identifies each item
- **Indexes**: Secondary access patterns for queries

### 4. Explain DynamoDB's primary key types.
**Answer:**
- **Partition Key (Hash Key)**: Single attribute that determines partition
- **Composite Key**: Partition key + Sort key (Range key)
  - Partition key determines partition
  - Sort key orders items within partition
  - Combination must be unique

### 5. What data types does DynamoDB support?
**Answer:**
**Scalar Types:**
- String (S), Number (N), Binary (B), Boolean (BOOL), Null (NULL)

**Collection Types:**
- String Set (SS), Number Set (NS), Binary Set (BS)
- List (L), Map (M)

**Special Considerations:**
- No native date type (use String or Number)
- Maximum item size: 400KB

## Data Modeling

### 6. What are the principles of DynamoDB data modeling?
**Answer:**
1. **Understand Access Patterns**: Design based on how data will be queried
2. **Denormalization**: Store related data together to avoid joins
3. **Single Table Design**: Use one table for entire application when possible
4. **Hierarchical Data**: Use sort keys for hierarchical relationships
5. **Avoid Hot Partitions**: Distribute data evenly across partitions

### 7. Explain the single table design pattern.
**Answer:**
Single table design stores different entity types in one table:
- **Benefits**: Reduced complexity, better performance, cost efficiency
- **Implementation**: Use generic attribute names (PK, SK, GSI1PK, GSI1SK)
- **Entity Types**: Differentiate using type attributes or key patterns
- **Relationships**: Model relationships using sort key patterns

### 8. How do you handle one-to-many relationships in DynamoDB?
**Answer:**
```
PK (Partition Key) | SK (Sort Key) | Attributes
USER#123          | PROFILE       | name, email, created_date
USER#123          | ORDER#001     | order_date, total, status
USER#123          | ORDER#002     | order_date, total, status
```
- Use same partition key for related items
- Use sort key to differentiate item types
- Query with partition key to get all related items

### 9. What are the best practices for choosing partition keys?
**Answer:**
- **High Cardinality**: Many distinct values to distribute load
- **Uniform Access**: Avoid hot partitions with uneven access
- **Predictable Patterns**: Enable efficient query patterns
- **Avoid Sequential**: Don't use timestamps or incrementing IDs
- **Examples**: User ID, Product ID, Device ID

### 10. How do you model hierarchical data in DynamoDB?
**Answer:**
Use sort key patterns for hierarchy:
```
PK: ORG#123
SK: DEPT#ENGINEERING
SK: DEPT#ENGINEERING#TEAM#BACKEND
SK: DEPT#ENGINEERING#TEAM#BACKEND#EMP#456
```
- Query with begins_with() for different hierarchy levels
- Use consistent delimiter patterns
- Enable range queries for hierarchical access

## Performance & Scaling

### 11. Explain DynamoDB's capacity modes.
**Answer:**
**Provisioned Mode:**
- Pre-allocated read/write capacity units
- Predictable performance and costs
- Auto-scaling available
- Best for predictable workloads

**On-Demand Mode:**
- Pay-per-request pricing
- Automatic scaling
- No capacity planning required
- Best for unpredictable workloads

### 12. What are Read Capacity Units (RCU) and Write Capacity Units (WCU)?
**Answer:**
**RCU (Read Capacity Units):**
- 1 RCU = 1 strongly consistent read per second for items up to 4KB
- 1 RCU = 2 eventually consistent reads per second for items up to 4KB

**WCU (Write Capacity Units):**
- 1 WCU = 1 write per second for items up to 1KB

**Calculation Examples:**
- 10KB item with strong consistency = 3 RCUs
- 2KB item write = 2 WCUs

### 13. How does DynamoDB handle hot partitions?
**Answer:**
- **Adaptive Capacity**: Automatically redistributes capacity to hot partitions
- **Burst Capacity**: Provides temporary additional capacity
- **Partition Splitting**: Splits hot partitions automatically
- **Best Practices**: Design keys to avoid hot partitions
- **Monitoring**: Use CloudWatch metrics to identify hot partitions

### 14. What is DynamoDB Accelerator (DAX) and when should you use it?
**Answer:**
DAX is an in-memory cache for DynamoDB:
- **Performance**: Microsecond latency for cached data
- **Compatibility**: Drop-in replacement for DynamoDB API
- **Use Cases**: Read-heavy workloads, gaming leaderboards, real-time bidding
- **Considerations**: Additional cost, eventual consistency for writes

### 15. How do you optimize DynamoDB performance?
**Answer:**
- **Efficient Keys**: Design partition keys for even distribution
- **Batch Operations**: Use BatchGetItem and BatchWriteItem
- **Projection**: Only retrieve needed attributes
- **Caching**: Implement application-level caching or use DAX
- **Connection Pooling**: Reuse connections in applications
- **Parallel Scans**: Use parallel scans for large table operations

## Indexes & Queries

### 16. What are Global Secondary Indexes (GSI) and Local Secondary Indexes (LSI)?
**Answer:**
**Global Secondary Index (GSI):**
- Different partition key and/or sort key from base table
- Can be created/deleted after table creation
- Has its own provisioned capacity
- Eventually consistent reads only

**Local Secondary Index (LSI):**
- Same partition key as base table, different sort key
- Must be created at table creation time
- Shares capacity with base table
- Supports both strong and eventual consistency

### 17. When should you use GSI vs LSI?
**Answer:**
**Use GSI when:**
- Need different partition key for access patterns
- Want to query across all partitions
- Need to add indexes after table creation

**Use LSI when:**
- Same partition key but different sort key needed
- Need strong consistency for secondary index queries
- Want to avoid additional capacity costs

### 18. What are the limitations of DynamoDB queries?
**Answer:**
- **Key Conditions**: Must specify partition key in queries
- **Sort Key**: Can only use one sort key condition per query
- **Filter Expressions**: Applied after data retrieval (affects performance)
- **Result Size**: Maximum 1MB per query operation
- **No Joins**: Cannot join data across tables
- **Limited Operators**: Restricted comparison operators

### 19. Explain the difference between Query and Scan operations.
**Answer:**
**Query:**
- Requires partition key specification
- Optionally filters on sort key
- Efficient, only reads relevant partitions
- Returns items in sort key order

**Scan:**
- Examines every item in table
- Can filter on any attribute
- Expensive, reads entire table
- Use parallel scans for better performance

### 20. How do you implement pagination in DynamoDB?
**Answer:**
```python
response = table.query(
    KeyConditionExpression=Key('pk').eq('USER#123'),
    Limit=10,
    ExclusiveStartKey=last_evaluated_key  # From previous response
)

last_evaluated_key = response.get('LastEvaluatedKey')
```
- Use `LastEvaluatedKey` from previous response
- Set `Limit` to control page size
- Continue until `LastEvaluatedKey` is not returned

## Consistency & Transactions

### 21. Explain DynamoDB's consistency models.
**Answer:**
**Eventually Consistent Reads (Default):**
- May not reflect recent write operations
- Higher throughput and lower latency
- Default for all read operations

**Strongly Consistent Reads:**
- Always returns most up-to-date data
- Higher latency and lower throughput
- Must be explicitly requested
- Not available for GSI queries

### 22. What are DynamoDB transactions and their limitations?
**Answer:**
DynamoDB supports ACID transactions across multiple items:
- **TransactWriteItems**: Up to 25 write operations
- **TransactGetItems**: Up to 25 read operations
- **Limitations**: Same region, 4MB total size, higher latency
- **Use Cases**: Financial transactions, inventory management

### 23. How do you implement optimistic locking in DynamoDB?
**Answer:**
```python
# Use version attribute for optimistic locking
response = table.update_item(
    Key={'id': 'item123'},
    UpdateExpression='SET #data = :new_data, #version = #version + :inc',
    ConditionExpression='#version = :current_version',
    ExpressionAttributeNames={
        '#data': 'data',
        '#version': 'version'
    },
    ExpressionAttributeValues={
        ':new_data': 'updated_value',
        ':current_version': 5,
        ':inc': 1
    }
)
```

### 24. What are conditional writes and when to use them?
**Answer:**
Conditional writes only execute if specified conditions are met:
- **Use Cases**: Prevent overwrites, implement business logic
- **Condition Types**: attribute_exists, attribute_not_exists, comparisons
- **Failure Handling**: ConditionalCheckFailedException when condition fails
- **Atomic Operations**: Ensure data integrity

## Security & Backup

### 25. How do you secure DynamoDB tables?
**Answer:**
- **IAM Policies**: Fine-grained access control using IAM
- **VPC Endpoints**: Private connectivity within VPC
- **Encryption**: Encryption at rest using AWS KMS
- **Encryption in Transit**: TLS for all API calls
- **Audit Logging**: AWS CloudTrail for API call logging

### 26. What backup and restore options does DynamoDB provide?
**Answer:**
**On-Demand Backup:**
- Manual backup creation
- Full table backup with consistent state
- Restore to new table in same or different region

**Point-in-Time Recovery (PITR):**
- Continuous backups for up to 35 days
- Restore to any point within retention period
- Automatic incremental backups

**Cross-Region Replication:**
- Global Tables for multi-region replication
- Automatic failover capabilities

### 27. How do you implement fine-grained access control?
**Answer:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:Query"
      ],
      "Resource": "arn:aws:dynamodb:region:account:table/MyTable",
      "Condition": {
        "ForAllValues:StringEquals": {
          "dynamodb:LeadingKeys": ["${aws:userid}"]
        }
      }
    }
  ]
}
```

## Advanced Features

### 28. What is DynamoDB Streams and its use cases?
**Answer:**
DynamoDB Streams captures data modification events:
- **Event Types**: INSERT, MODIFY, REMOVE
- **Retention**: 24-hour retention period
- **Processing**: Lambda triggers, Kinesis integration
- **Use Cases**: Real-time analytics, replication, audit logging

### 29. How do you implement change data capture with DynamoDB?
**Answer:**
1. **Enable Streams**: Configure DynamoDB Streams on table
2. **Lambda Function**: Create Lambda to process stream records
3. **Event Processing**: Handle INSERT, MODIFY, REMOVE events
4. **Downstream Systems**: Send changes to analytics, search, or other systems
5. **Error Handling**: Implement retry logic and dead letter queues

### 30. What are DynamoDB Global Tables?
**Answer:**
Global Tables provide multi-region, multi-master replication:
- **Active-Active**: Write to any region
- **Automatic Replication**: Changes replicated across regions
- **Conflict Resolution**: Last writer wins conflict resolution
- **Use Cases**: Global applications, disaster recovery, low latency access

### 31. How do you monitor DynamoDB performance?
**Answer:**
- **CloudWatch Metrics**: Capacity utilization, throttling, latency
- **X-Ray Tracing**: End-to-end request tracing
- **CloudTrail**: API call logging and auditing
- **Custom Metrics**: Application-level performance metrics
- **Alarms**: Automated alerting for threshold breaches

## Scenario-Based Questions

### 32. You're building a social media application. How would you model user posts and comments in DynamoDB?
**Answer:**
```
PK: USER#123
SK: POST#2023-01-15#001    (timestamp + unique ID)
SK: POST#2023-01-15#001#COMMENT#001
SK: POST#2023-01-15#001#COMMENT#002

GSI1PK: POST#2023-01-15#001
GSI1SK: COMMENT#001
```
- Use hierarchical sort keys for posts and comments
- GSI for querying comments by post
- Include timestamp in sort key for chronological ordering

### 33. Your application is experiencing throttling. How do you troubleshoot and resolve it?
**Answer:**
1. **Identify Hot Partitions**: Check CloudWatch metrics for throttling
2. **Analyze Access Patterns**: Review partition key distribution
3. **Increase Capacity**: Scale up provisioned capacity temporarily
4. **Redesign Keys**: Modify partition key for better distribution
5. **Implement Backoff**: Add exponential backoff in application
6. **Use Batch Operations**: Reduce API call frequency

### 34. How would you migrate data from a relational database to DynamoDB?
**Answer:**
1. **Analyze Schema**: Understand current data model and relationships
2. **Design DynamoDB Model**: Create single table design for access patterns
3. **Data Transformation**: Write ETL scripts to transform relational data
4. **Migration Strategy**: Choose between full migration or gradual approach
5. **Validation**: Verify data integrity and completeness
6. **Application Updates**: Modify application to use DynamoDB APIs
7. **Performance Testing**: Validate performance meets requirements

### 35. You need to implement a leaderboard for a gaming application. How would you design it?
**Answer:**
```
Table: GameLeaderboard
PK: GAME#chess
SK: SCORE#999999999999-{actual_score}#{user_id}

GSI1PK: USER#{user_id}
GSI1SK: GAME#chess
```
- Use inverted score in sort key for descending order
- Query top N players using Query with Limit
- GSI for user's rank lookup
- Consider using DAX for ultra-low latency

### 36. How would you implement a shopping cart with DynamoDB?
**Answer:**
```
PK: USER#{user_id}
SK: CART#ITEM#{product_id}
Attributes: quantity, price, added_date

PK: USER#{user_id}
SK: CART#METADATA
Attributes: total_items, total_price, last_updated
```
- Use transactions for cart operations
- Implement TTL for cart expiration
- Use conditional writes to prevent race conditions
- Consider using DynamoDB Streams for analytics

---

## Key Takeaways for Interviews

1. **Data Modeling**: Master single table design and access pattern-driven modeling
2. **Performance**: Understand capacity modes, scaling, and optimization techniques
3. **Indexes**: Know when to use GSI vs LSI and their limitations
4. **Consistency**: Understand eventual vs strong consistency trade-offs
5. **Security**: Be familiar with IAM, encryption, and access control patterns
6. **Monitoring**: Know key metrics and troubleshooting approaches
7. **Advanced Features**: Understand Streams, Global Tables, and transactions
8. **Real-world Scenarios**: Practice designing solutions for common use cases