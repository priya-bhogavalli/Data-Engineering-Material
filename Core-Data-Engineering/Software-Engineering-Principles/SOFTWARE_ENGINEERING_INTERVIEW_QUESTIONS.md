# Software Engineering Principles Interview Questions

## 🎯 **Testing Strategies**

### **Q1: How do you implement data quality testing in ETL pipelines?**

**Answer:**
Data quality testing involves multiple layers:

1. **Schema Validation**
```python
def test_schema_compliance(df):
    expected_schema = {
        'user_id': 'int64',
        'timestamp': 'datetime64[ns]',
        'amount': 'float64'
    }
    assert df.dtypes.to_dict() == expected_schema
```

2. **Data Completeness**
```python
def test_data_completeness(df):
    assert df.isnull().sum().sum() == 0
    assert len(df) > 0
```

3. **Business Rule Validation**
```python
def test_business_rules(df):
    assert (df['amount'] >= 0).all()
    assert df['user_id'].nunique() == len(df)
```

**Key Points:**
- Use Great Expectations for comprehensive data validation
- Implement data contracts between systems
- Monitor data drift and anomalies
- Test both positive and negative scenarios

### **Q2: What is the data testing pyramid and how do you apply it?**

**Answer:**
The data testing pyramid follows the traditional testing pyramid:

```
    /\
   /  \     Unit Tests (70%)
  /____\    - Schema validation
 /      \   - Data transformation logic
/________\  - Business rule validation

Integration Tests (20%)
- Pipeline end-to-end
- Database connections
- API integrations

System Tests (10%)
- Full workflow validation
- Performance testing
- Load testing
```

**Implementation:**
- **Unit Tests**: Test individual functions and transformations
- **Integration Tests**: Test component interactions
- **System Tests**: Test complete workflows under realistic conditions

### **Q3: How do you test data pipeline performance?**

**Answer:**
Performance testing involves multiple dimensions:

1. **Throughput Testing**
```python
@pytest.mark.performance
def test_pipeline_throughput():
    start_time = time.time()
    result = process_batch(large_dataset)
    execution_time = time.time() - start_time
    
    records_per_second = len(large_dataset) / execution_time
    assert records_per_second > 1000  # Minimum throughput
```

2. **Latency Testing**
```python
def test_query_latency():
    start_time = time.time()
    result = execute_query()
    latency = time.time() - start_time
    assert latency < 5.0  # Max 5 seconds
```

3. **Resource Usage Testing**
```python
def test_memory_usage():
    process = psutil.Process()
    initial_memory = process.memory_info().rss
    
    process_large_dataset()
    
    final_memory = process.memory_info().rss
    memory_increase = (final_memory - initial_memory) / 1024 / 1024
    assert memory_increase < 1000  # Max 1GB increase
```

---

## 🗂️ **Database Indexing & Optimization**

### **Q4: Explain different types of database indexes and their use cases.**

**Answer:**

1. **B-Tree Indexes (Default)**
   - Use case: Equality and range queries
   - Best for: Primary keys, foreign keys, ordered data

2. **Hash Indexes**
   - Use case: Equality queries only
   - Best for: Exact match lookups

3. **Bitmap Indexes**
   - Use case: Low cardinality columns
   - Best for: Data warehousing, OLAP queries

4. **Partial Indexes**
```sql
CREATE INDEX idx_active_users ON users(email) 
WHERE status = 'active';
```
   - Use case: Subset of data frequently queried
   - Best for: Reducing index size and maintenance

5. **Composite Indexes**
```sql
CREATE INDEX idx_orders_user_date ON orders(user_id, order_date);
```
   - Use case: Multi-column queries
   - Best for: Complex WHERE clauses

6. **Functional Indexes**
```sql
CREATE INDEX idx_users_lower_email ON users(LOWER(email));
```
   - Use case: Function-based queries
   - Best for: Case-insensitive searches

### **Q5: How do you optimize database queries for large datasets?**

**Answer:**

1. **Query Analysis**
```sql
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.created_at >= '2024-01-01';
```

2. **Index Optimization**
```sql
-- Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_tup_read DESC;
```

3. **Partitioning Strategy**
```sql
-- Range partitioning
CREATE TABLE sales (
    id SERIAL,
    sale_date DATE,
    amount DECIMAL
) PARTITION BY RANGE (sale_date);
```

4. **Materialized Views**
```sql
CREATE MATERIALIZED VIEW user_order_summary AS
SELECT 
    u.id,
    u.name,
    COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;
```

### **Q6: What are the trade-offs between different partitioning strategies?**

**Answer:**

| Strategy | Pros | Cons | Use Case |
|----------|------|------|----------|
| **Range Partitioning** | Easy to understand, good for time-series | Uneven distribution possible | Time-based data |
| **Hash Partitioning** | Even distribution | No range queries | High-volume OLTP |
| **List Partitioning** | Logical grouping | Manual maintenance | Geographic regions |
| **Composite Partitioning** | Combines benefits | Complex management | Large, complex datasets |

**Implementation Considerations:**
- Partition pruning effectiveness
- Maintenance overhead
- Query patterns
- Data distribution

---

## 📈 **Scaling Strategies**

### **Q7: Compare horizontal vs vertical scaling for data systems.**

**Answer:**

**Vertical Scaling (Scale Up):**
- **Pros**: Simple, no application changes, strong consistency
- **Cons**: Hardware limits, single point of failure, expensive
- **Use Case**: OLTP systems, small to medium datasets

**Horizontal Scaling (Scale Out):**
- **Pros**: Unlimited scaling, fault tolerance, cost-effective
- **Cons**: Complex architecture, eventual consistency, data distribution challenges
- **Use Case**: Big data, high-volume systems, distributed applications

**Implementation Example:**
```python
# Read replica routing
class DatabaseRouter:
    def __init__(self):
        self.master = create_engine('postgresql://master:5432/db')
        self.replicas = [
            create_engine('postgresql://replica1:5432/db'),
            create_engine('postgresql://replica2:5432/db')
        ]
    
    def get_read_connection(self):
        return random.choice(self.replicas)
    
    def get_write_connection(self):
        return self.master
```

### **Q8: How do you implement caching strategies in data systems?**

**Answer:**

1. **Cache-Aside Pattern**
```python
def get_user(user_id):
    cache_key = f"user:{user_id}"
    
    # Try cache first
    user_data = redis_client.get(cache_key)
    if user_data:
        return json.loads(user_data)
    
    # Fetch from database
    user_data = db.fetch_user(user_id)
    
    # Populate cache
    redis_client.setex(cache_key, 3600, json.dumps(user_data))
    
    return user_data
```

2. **Write-Through Cache**
```python
def update_user(user_id, data):
    # Update database
    db.execute("UPDATE users SET ... WHERE id = %s", user_id)
    
    # Update cache
    cache_key = f"user:{user_id}"
    redis_client.setex(cache_key, 3600, json.dumps(data))
```

3. **Multi-Level Caching**
```python
@cached(expiration=1800)
def get_user_analytics(user_id):
    # Expensive database query
    return execute_complex_analytics_query(user_id)
```

**Cache Invalidation Strategies:**
- TTL (Time To Live)
- Event-based invalidation
- Manual invalidation
- Cache warming

### **Q9: Explain the Circuit Breaker pattern and its implementation.**

**Answer:**

The Circuit Breaker pattern prevents cascading failures by monitoring service health and failing fast when issues are detected.

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self.reset()
            return result
        except Exception as e:
            self.record_failure()
            raise e
```

**States:**
- **CLOSED**: Normal operation
- **OPEN**: Failing fast, not calling service
- **HALF_OPEN**: Testing if service recovered

---

## 💻 **Development Best Practices**

### **Q10: How do you structure a data engineering project for maintainability?**

**Answer:**

**Layered Architecture:**
```
data-pipeline/
├── src/
│   ├── domain/          # Business logic
│   │   ├── models/
│   │   └── services/
│   ├── infrastructure/  # External dependencies
│   │   ├── database/
│   │   ├── messaging/
│   │   └── storage/
│   ├── application/     # Use cases
│   │   ├── etl/
│   │   └── api/
│   └── interfaces/      # Controllers/adapters
├── tests/
├── config/
└── docs/
```

**Key Principles:**
- Separation of concerns
- Dependency inversion
- Single responsibility
- Configuration externalization

### **Q11: How do you handle configuration management in data systems?**

**Answer:**

**Environment-Based Configuration:**
```python
@dataclass
class DatabaseConfig:
    host: str
    port: int
    database: str
    username: str
    password: str
    
    @classmethod
    def from_env(cls):
        return cls(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 5432)),
            database=os.getenv('DB_NAME'),
            username=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
```

**Best Practices:**
- Use environment variables for secrets
- Validate configuration at startup
- Provide sensible defaults
- Document all configuration options
- Use configuration schemas

### **Q12: Explain error handling strategies for data pipelines.**

**Answer:**

1. **Retry with Exponential Backoff**
```python
def retry_with_backoff(max_retries=3, base_delay=1, max_delay=60):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    jitter = random.uniform(0, delay * 0.1)
                    time.sleep(delay + jitter)
        return wrapper
    return decorator
```

2. **Graceful Degradation**
```python
class DataService:
    def get_data(self, query):
        try:
            return self.primary_source.execute(query)
        except Exception as e:
            logger.warning(f"Primary source failed: {e}")
            return self.fallback_source.execute(query)
```

3. **Dead Letter Queues**
- Route failed messages to separate queue
- Implement retry logic with backoff
- Monitor and alert on failures
- Manual intervention for persistent failures

---

## ⚡ **Performance Engineering**

### **Q13: How do you profile and optimize Python code for data processing?**

**Answer:**

1. **Profiling with cProfile**
```python
def profile_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        
        result = func(*args, **kwargs)
        
        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(10)
        
        return result
    return wrapper
```

2. **Memory Monitoring**
```python
@contextmanager
def memory_monitor(operation_name):
    process = psutil.Process()
    initial_memory = process.memory_info().rss / 1024 / 1024
    
    yield
    
    gc.collect()
    final_memory = process.memory_info().rss / 1024 / 1024
    
    print(f"{operation_name}: {final_memory - initial_memory:.2f} MB")
```

3. **Optimization Techniques**
- Use vectorized operations (NumPy, Pandas)
- Implement lazy evaluation
- Optimize data types
- Use multiprocessing for CPU-bound tasks
- Use asyncio for I/O-bound tasks

### **Q14: What are the key metrics for monitoring data system performance?**

**Answer:**

1. **Throughput Metrics**
   - Records processed per second
   - Bytes processed per second
   - Transactions per second

2. **Latency Metrics**
   - Query response time (p50, p95, p99)
   - End-to-end pipeline latency
   - API response time

3. **Resource Utilization**
   - CPU usage
   - Memory consumption
   - Disk I/O
   - Network bandwidth

4. **Error Metrics**
   - Error rate
   - Failed job count
   - Data quality violations

5. **Business Metrics**
   - Data freshness
   - SLA compliance
   - Cost per processed record

**Implementation:**
```python
# Prometheus metrics
REQUEST_COUNT = Counter('requests_total', 'Total requests')
REQUEST_DURATION = Histogram('request_duration_seconds', 'Request duration')
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Active connections')
```

---

## 📊 **Monitoring & Observability**

### **Q15: How do you implement comprehensive logging for data systems?**

**Answer:**

**Structured Logging:**
```python
class StructuredLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        handler = logging.StreamHandler()
        handler.setFormatter(self.JsonFormatter())
        self.logger.addHandler(handler)
    
    class JsonFormatter(logging.Formatter):
        def format(self, record):
            return json.dumps({
                'timestamp': datetime.utcnow().isoformat(),
                'level': record.levelname,
                'message': record.getMessage(),
                'module': record.module,
                'function': record.funcName,
                'line': record.lineno
            })
```

**Best Practices:**
- Use correlation IDs for request tracing
- Log at appropriate levels (DEBUG, INFO, WARN, ERROR)
- Include contextual information
- Avoid logging sensitive data
- Use centralized logging (ELK stack, Splunk)

### **Q16: Design a health check system for a data pipeline.**

**Answer:**

```python
@app.route('/health')
def health_check():
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'checks': {}
    }
    
    # Database connectivity
    try:
        db.execute('SELECT 1')
        health_status['checks']['database'] = 'healthy'
    except Exception as e:
        health_status['checks']['database'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    # Memory usage
    memory_percent = psutil.virtual_memory().percent
    health_status['checks']['memory'] = {
        'status': 'healthy' if memory_percent < 80 else 'warning',
        'usage_percent': memory_percent
    }
    
    return jsonify(health_status)
```

**Health Check Categories:**
- **Liveness**: Is the service running?
- **Readiness**: Can the service handle requests?
- **Dependency**: Are external services available?
- **Resource**: Are system resources adequate?

---

## 🎯 **Best Practices & Architecture**

### **Q17: How do you ensure data consistency in distributed systems?**

**Answer:**

1. **ACID Properties**
   - Atomicity: All or nothing transactions
   - Consistency: Data integrity constraints
   - Isolation: Concurrent transaction isolation
   - Durability: Committed data persistence

2. **CAP Theorem Trade-offs**
   - Consistency vs Availability vs Partition Tolerance
   - Choose based on business requirements

3. **Consistency Patterns**
   - **Strong Consistency**: All nodes see same data simultaneously
   - **Eventual Consistency**: Nodes will converge over time
   - **Weak Consistency**: No guarantees about when data will be consistent

4. **Implementation Strategies**
```python
# Two-phase commit
def distributed_transaction():
    try:
        # Phase 1: Prepare
        for db in databases:
            db.prepare_transaction()
        
        # Phase 2: Commit
        for db in databases:
            db.commit_transaction()
    except Exception:
        # Rollback all
        for db in databases:
            db.rollback_transaction()
```

### **Q18: What are the key considerations for data pipeline security?**

**Answer:**

1. **Data Encryption**
   - Encryption at rest
   - Encryption in transit
   - Key management

2. **Access Control**
   - Authentication (who you are)
   - Authorization (what you can do)
   - Role-based access control (RBAC)

3. **Data Privacy**
   - PII identification and protection
   - Data masking and anonymization
   - GDPR/CCPA compliance

4. **Audit and Compliance**
   - Access logging
   - Data lineage tracking
   - Compliance reporting

5. **Network Security**
   - VPC/subnet isolation
   - Firewall rules
   - VPN connections

**Implementation Example:**
```python
# Data masking
def mask_sensitive_data(df):
    df['email'] = df['email'].apply(lambda x: x[:3] + '***@' + x.split('@')[1])
    df['phone'] = df['phone'].apply(lambda x: '***-***-' + x[-4:])
    return df
```

This comprehensive interview guide covers essential software engineering principles for data systems, providing both theoretical knowledge and practical implementation examples.