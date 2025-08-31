# 🔥 Emergency Interview Prep (2-4 hours)

## ⚡ **Immediate Actions (30 mins)**
1. Review [Python basics](./python-cheat-sheet.md)
2. Refresh [SQL commands](./sql-cheat-sheet.md)
3. Scan [AWS services overview](./aws-quick-reference.md)
4. Quick read [Data Engineering Fundamentals](./fundamentals-review.md)

## 🎯 **Top 10 Must-Know Questions with Answers (90 mins)**

### 1. **"Explain the difference between OLTP and OLAP"**
**Answer:**
- **OLTP (Online Transaction Processing)**:
  - Real-time operational data processing
  - Normalized database design (3NF)
  - High volume of short transactions
  - ACID compliance critical
  - Examples: Banking systems, e-commerce

- **OLAP (Online Analytical Processing)**:
  - Historical data analysis
  - Denormalized design (star/snowflake schema)
  - Complex queries, aggregations
  - Read-heavy workloads
  - Examples: Data warehouses, reporting

### 2. **"How would you handle duplicate data in a pipeline?"**
**Answer:**
- **Prevention**: Use unique constraints, proper data modeling
- **Detection**: Data profiling, duplicate checks in ETL
- **Removal**: 
  ```sql
  -- SQL approach
  DELETE FROM table WHERE id NOT IN (
    SELECT MIN(id) FROM table GROUP BY unique_columns
  );
  ```
  ```python
  # Pandas approach
  df.drop_duplicates(subset=['key_columns'], keep='first')
  ```
- **Idempotency**: Design pipelines to handle re-runs safely

### 3. **"What's the difference between batch and stream processing?"**
**Answer:**
- **Batch Processing**:
  - Process large volumes at scheduled intervals
  - Higher latency, higher throughput
  - Tools: Spark, Hadoop, Airflow
  - Use cases: ETL jobs, reporting, ML training

- **Stream Processing**:
  - Process data in real-time as it arrives
  - Lower latency, continuous processing
  - Tools: Kafka, Flink, Kinesis
  - Use cases: Fraud detection, monitoring, real-time analytics

### 4. **"Explain database normalization vs denormalization"**
**Answer:**
- **Normalization**:
  - Reduces data redundancy
  - Multiple related tables
  - Better for OLTP (insert/update heavy)
  - 1NF → 2NF → 3NF progression

- **Denormalization**:
  - Optimizes for read performance
  - Fewer JOINs required
  - Better for OLAP (read-heavy)
  - Trade storage for query speed

### 5. **"How do you optimize a slow SQL query?"**
**Answer:**
1. **Analyze execution plan**: Use EXPLAIN
2. **Add indexes**: On WHERE, JOIN, ORDER BY columns
3. **Rewrite query**: 
   - Avoid SELECT *
   - Use appropriate JOINs
   - Filter early with WHERE
4. **Partitioning**: For large tables
5. **Statistics**: Update table statistics
6. **Query hints**: As last resort

### 6. **"What's the CAP theorem?"**
**Answer:**
In distributed systems, you can only guarantee 2 out of 3:
- **Consistency**: All nodes see same data simultaneously
- **Availability**: System remains operational
- **Partition tolerance**: System continues despite network failures

Examples:
- **CP**: Traditional RDBMS (PostgreSQL)
- **AP**: NoSQL databases (Cassandra)
- **CA**: Single-node systems (not distributed)

### 7. **"Explain eventual consistency"**
**Answer:**
- System will become consistent over time
- Immediate consistency not guaranteed
- Trade-off for availability and partition tolerance
- Common in distributed NoSQL systems
- Example: DNS propagation, social media feeds

### 8. **"How would you design a data pipeline for real-time analytics?"**
**Answer:**
```
Data Sources → Kafka → Stream Processing → Storage → Visualization
     ↓           ↓           ↓              ↓           ↓
  Web logs    Message     Spark         ClickHouse   Grafana
  APIs        Queue      Streaming      TimescaleDB  Tableau
  Databases   Buffer     Flink          Elasticsearch Kibana
```

Key considerations:
- **Scalability**: Horizontal scaling
- **Fault tolerance**: Replication, checkpointing
- **Monitoring**: Metrics, alerting
- **Schema evolution**: Handle data changes

### 9. **"What's the difference between Data Lake and Data Warehouse?"**
**Answer:**

| Aspect | Data Lake | Data Warehouse |
|--------|-----------|----------------|
| **Data** | Raw, unprocessed | Processed, structured |
| **Schema** | Schema-on-read | Schema-on-write |
| **Cost** | Lower storage cost | Higher storage cost |
| **Flexibility** | High | Lower |
| **Query Performance** | Variable | Optimized |
| **Use Cases** | Exploration, ML | Reporting, BI |

### 10. **"How do you ensure data quality?"**
**Answer:**
- **Data Profiling**: Understand data characteristics
- **Validation Rules**: 
  ```python
  # Example validation
  assert df['age'].between(0, 120).all()
  assert df['email'].str.contains('@').all()
  ```
- **Monitoring**: Track data quality metrics
- **Data Lineage**: Understand data flow
- **Testing**: Unit tests for transformations
- **Alerts**: Notify on quality issues

## 💻 **Quick Coding Review (60 mins)**

### **Python Essentials**
```python
# List comprehensions
squares = [x**2 for x in range(10) if x % 2 == 0]

# Pandas basics
df.groupby('category').agg({'sales': 'sum', 'quantity': 'mean'})
df.merge(df2, on='key', how='left')
df.drop_duplicates(subset=['id'])

# Error handling
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    result = default_value
```

### **SQL Must-Know**
```sql
-- Window functions
SELECT name, salary,
       RANK() OVER (PARTITION BY dept ORDER BY salary DESC) as rank
FROM employees;

-- CTEs
WITH monthly_sales AS (
    SELECT DATE_TRUNC('month', date) as month, SUM(amount) as total
    FROM sales GROUP BY 1
)
SELECT month, total, LAG(total) OVER (ORDER BY month) as prev_month
FROM monthly_sales;

-- JOINs
SELECT a.*, b.name
FROM orders a
LEFT JOIN customers b ON a.customer_id = b.id;
```

### **Data Structures**
- **List**: Ordered, mutable, allows duplicates
- **Dict**: Key-value pairs, O(1) lookup
- **Set**: Unique values, fast membership testing
- **Tuple**: Immutable, hashable

## 🗣️ **Behavioral Prep (30 mins)**

### **"Tell me about a challenging data project"**
**Structure your answer:**
1. **Situation**: Context and challenge
2. **Task**: Your responsibility
3. **Action**: What you did (be specific)
4. **Result**: Outcome and impact

**Example topics:**
- Performance optimization
- Data quality issues
- System migration
- Scaling challenges

### **"How do you handle conflicting requirements?"**
**Key points:**
- Understand all stakeholder needs
- Communicate trade-offs clearly
- Propose alternative solutions
- Document decisions and rationale
- Follow up on outcomes

### **"Describe a time you optimized performance"**
**Include:**
- Specific metrics (before/after)
- Root cause analysis approach
- Technical solution implemented
- Monitoring and validation
- Lessons learned

## 🚨 **Last-Minute Checklist (15 mins)**

### **Technical Concepts to Memorize**
- ACID properties: Atomicity, Consistency, Isolation, Durability
- Data modeling: Star schema, snowflake schema, data vault
- Big data 4 Vs: Volume, Velocity, Variety, Veracity
- Lambda architecture: Batch + Speed + Serving layers

### **Common Metrics**
- **Latency**: Time to process single record
- **Throughput**: Records processed per second
- **Availability**: Uptime percentage (99.9% = 8.76 hours downtime/year)
- **RPO/RTO**: Recovery Point/Time Objectives

### **Quick Mental Math**
- 1 TB = 1,000 GB = 1,000,000 MB
- 1 million records ≈ 100MB (depending on schema)
- Network: 1 Gbps = 125 MB/s
- SSD: ~500 MB/s, HDD: ~100 MB/s

## 🎯 **Final Tips**
1. **Ask clarifying questions** - Shows analytical thinking
2. **Think out loud** - Demonstrate problem-solving process
3. **Start simple, then optimize** - Show iterative approach
4. **Mention trade-offs** - Shows understanding of real-world constraints
5. **Be honest about unknowns** - Better than guessing