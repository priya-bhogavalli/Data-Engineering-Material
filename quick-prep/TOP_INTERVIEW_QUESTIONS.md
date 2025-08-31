# 💡 Top 50 Data Engineering Interview Questions

## 🏗️ **Data Architecture & Design (10 questions)**

### 1. **Explain the difference between Data Lake, Data Warehouse, and Data Mart**
- **Data Lake**: Raw data storage, schema-on-read, supports all data types
- **Data Warehouse**: Structured, schema-on-write, optimized for analytics
- **Data Mart**: Subset of data warehouse, department-specific

### 2. **What is the difference between OLTP and OLAP?**
- **OLTP**: Online Transaction Processing, normalized, real-time operations
- **OLAP**: Online Analytical Processing, denormalized, historical analysis

### 3. **Explain ETL vs ELT**
- **ETL**: Extract-Transform-Load, transform before loading
- **ELT**: Extract-Load-Transform, leverage target system's processing power

### 4. **What is data partitioning and why is it important?**
- Divides large datasets into smaller, manageable pieces
- Improves query performance and enables parallel processing

### 5. **Describe the CAP theorem**
- **Consistency**: All nodes see the same data simultaneously
- **Availability**: System remains operational
- **Partition tolerance**: System continues despite network failures
- Can only guarantee 2 out of 3

## 🔄 **Data Processing & Pipelines (15 questions)**

### 6. **What's the difference between batch and stream processing?**
- **Batch**: Process large volumes at scheduled intervals
- **Stream**: Process data in real-time as it arrives

### 7. **How do you handle duplicate data in a pipeline?**
- Use unique constraints, deduplication logic, or upsert operations
- Implement idempotency in pipeline design

### 8. **Explain data lineage and why it's important**
- Tracks data flow from source to destination
- Essential for debugging, compliance, and impact analysis

### 9. **What is backpressure in streaming systems?**
- When downstream systems can't keep up with data flow
- Handle with buffering, throttling, or dropping data

### 10. **How do you ensure data quality?**
- Data validation, profiling, monitoring, and automated testing
- Implement data contracts and SLAs

## 🗄️ **Databases & Storage (10 questions)**

### 11. **Explain database normalization vs denormalization**
- **Normalization**: Reduce redundancy, multiple tables
- **Denormalization**: Optimize for read performance, fewer joins

### 12. **What are the different types of NoSQL databases?**
- **Document**: MongoDB, CouchDB
- **Key-Value**: Redis, DynamoDB
- **Column-family**: Cassandra, HBase
- **Graph**: Neo4j, Amazon Neptune

### 13. **Explain ACID properties**
- **Atomicity**: All or nothing transactions
- **Consistency**: Data integrity maintained
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed data persists

### 14. **What is eventual consistency?**
- System will become consistent over time
- Trade-off for availability and partition tolerance

### 15. **Explain different file formats (Parquet, Avro, JSON)**
- **Parquet**: Columnar, compressed, analytics-optimized
- **Avro**: Row-based, schema evolution support
- **JSON**: Human-readable, flexible schema

## ☁️ **Cloud & Infrastructure (8 questions)**

### 16. **Compare AWS S3 storage classes**
- **Standard**: Frequent access
- **IA**: Infrequent access, lower cost
- **Glacier**: Archive, very low cost, longer retrieval

### 17. **What is serverless computing?**
- No server management, pay-per-use, auto-scaling
- Examples: AWS Lambda, Glue, Athena

### 18. **Explain Infrastructure as Code (IaC)**
- Manage infrastructure through code
- Tools: Terraform, CloudFormation, Ansible

### 19. **What is containerization?**
- Package applications with dependencies
- Benefits: portability, consistency, scalability

## 🐍 **Programming & Tools (7 questions)**

### 20. **Explain Python list comprehensions**
```python
squares = [x**2 for x in range(10) if x % 2 == 0]
```

### 21. **What are Python generators?**
- Memory-efficient iterators using yield
- Process large datasets without loading everything into memory

### 22. **Explain SQL window functions**
```sql
SELECT name, salary, 
       RANK() OVER (PARTITION BY dept ORDER BY salary DESC) as rank
FROM employees;
```

### 23. **What is Apache Spark and its advantages?**
- Unified analytics engine for big data processing
- In-memory computing, fault tolerance, ease of use

## 🔧 **Performance & Optimization (5 questions)**

### 24. **How do you optimize a slow SQL query?**
- Add indexes, analyze execution plan, rewrite joins
- Avoid SELECT *, use appropriate WHERE clauses

### 25. **What causes data skew and how to handle it?**
- Uneven data distribution across partitions
- Solutions: salting, custom partitioning, broadcast joins

### 26. **Explain caching strategies**
- **Cache-aside**: Application manages cache
- **Write-through**: Write to cache and database
- **Write-behind**: Write to cache first, database later

## 🚨 **Monitoring & Troubleshooting (5 questions)**

### 27. **How do you monitor data pipelines?**
- Metrics: latency, throughput, error rates
- Tools: CloudWatch, Datadog, custom dashboards

### 28. **What is circuit breaker pattern?**
- Prevents cascading failures in distributed systems
- States: Closed, Open, Half-Open

### 29. **How do you handle pipeline failures?**
- Retry mechanisms, dead letter queues, alerting
- Implement graceful degradation

## 🔐 **Security & Compliance (5 questions)**

### 30. **Explain data encryption at rest vs in transit**
- **At rest**: Stored data encryption (AES-256)
- **In transit**: Network communication encryption (TLS/SSL)

### 31. **What is data masking?**
- Hide sensitive data in non-production environments
- Techniques: substitution, shuffling, nulling

### 32. **Explain GDPR compliance in data engineering**
- Right to be forgotten, data minimization, consent
- Implement data retention policies and audit trails

## 🎯 **Scenario-Based Questions (5 questions)**

### 33. **Design a real-time analytics system**
- Kafka for ingestion → Spark Streaming → Database/Dashboard
- Consider scalability, fault tolerance, monitoring

### 34. **How would you migrate from on-premise to cloud?**
- Assessment, pilot migration, gradual transition
- Consider data transfer, security, cost optimization

### 35. **Handle a sudden 10x increase in data volume**
- Auto-scaling, partitioning, caching
- Monitor performance and optimize bottlenecks

## 🔄 **Advanced Topics (5 questions)**

### 36. **Explain Change Data Capture (CDC)**
- Track and capture database changes
- Tools: Debezium, AWS DMS, Kafka Connect

### 37. **What is data mesh architecture?**
- Decentralized data ownership by domain
- Self-serve data infrastructure, federated governance

### 38. **Explain Apache Kafka architecture**
- Topics, partitions, producers, consumers
- Distributed, fault-tolerant, high-throughput

### 39. **What is Apache Airflow?**
- Workflow orchestration platform
- DAGs, operators, schedulers, executors

### 40. **Explain data versioning**
- Track changes to datasets over time
- Tools: DVC, lakeFS, Delta Lake time travel

## 🎪 **Behavioral & Soft Skills (10 questions)**

### 41. **Describe a challenging data project you worked on**
- Focus on problem-solving, technical decisions, outcomes

### 42. **How do you handle conflicting requirements?**
- Stakeholder communication, trade-off analysis, documentation

### 43. **How do you stay updated with new technologies?**
- Continuous learning, conferences, online courses, experimentation

### 44. **Describe a time you optimized system performance**
- Specific metrics, approach, results achieved

### 45. **How do you ensure code quality?**
- Code reviews, testing, documentation, standards

### 46. **Explain a complex technical concept to a non-technical person**
- Use analogies, avoid jargon, focus on business value

### 47. **How do you prioritize tasks in a project?**
- Business impact, dependencies, effort estimation

### 48. **Describe a time you had to learn a new technology quickly**
- Learning approach, resources used, application

### 49. **How do you handle production incidents?**
- Incident response process, communication, post-mortem

### 50. **What questions do you have for us?**
- Ask about team structure, technology stack, challenges, growth opportunities