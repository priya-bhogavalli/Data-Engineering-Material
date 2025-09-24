# 🚀 Trino - Key Concepts

**Category**: Distributed SQL Query Engine  
**Market Share**: 35% of federated query workloads  
**Interview Frequency**: 35% of data engineering roles  
**Learning Time**: 3-4 weeks

---

## 🎯 What is Trino?

Trino (formerly PrestoSQL) is a distributed SQL query engine designed to query large datasets across multiple data sources. It enables federated queries without moving data.

### **Core Value Proposition**
- **Query multiple data sources** with single SQL
- **Sub-second query latency** for interactive analytics
- **Petabyte-scale** data processing
- **No data movement** required
- **ANSI SQL compliance**

---

## 🏗️ Architecture Overview

```
Client → Coordinator → Workers → Data Sources
                ↓
        Query Planning & Execution
```

### **Key Components**

1. **Coordinator**: Query planning and metadata management
2. **Workers**: Execute query fragments in parallel
3. **Connectors**: Interface to data sources
4. **Catalog**: Metadata about data sources
5. **Discovery Service**: Node coordination

---

## 🔧 Core Concepts

### **1. Connectors**
```sql
-- Query different data sources
SELECT h.customer_id, h.order_total, c.customer_name
FROM hive.sales.orders h
JOIN mysql.crm.customers c ON h.customer_id = c.id
WHERE h.order_date >= DATE '2024-01-01'
```

**Popular Connectors**:
- Hive, Delta Lake, Iceberg
- MySQL, PostgreSQL, Oracle
- Elasticsearch, MongoDB
- S3, HDFS, Kafka

### **2. Query Execution Model**
```
Query → Parse → Plan → Schedule → Execute → Results
```

**Execution Features**:
- Vectorized execution
- Code generation
- Adaptive query optimization
- Dynamic filtering

### **3. Memory Management**
```properties
# Memory configuration
query.max-memory=50GB
query.max-memory-per-node=8GB
query.max-total-memory-per-node=10GB
memory.heap-headroom-per-node=1GB
```

---

## 🚀 Implementation

### **1. Basic Setup**
```bash
# Download and start Trino
wget https://repo1.maven.org/maven2/io/trino/trino-server/435/trino-server-435.tar.gz
tar -xzf trino-server-435.tar.gz
cd trino-server-435

# Start server
bin/launcher start
```

### **2. Catalog Configuration**
```properties
# catalog/hive.properties
connector.name=hive-hadoop2
hive.metastore.uri=thrift://localhost:9083
hive.s3.endpoint=s3.amazonaws.com
hive.s3.aws-access-key=YOUR_ACCESS_KEY
hive.s3.aws-secret-key=YOUR_SECRET_KEY

# catalog/mysql.properties  
connector.name=mysql
connection-url=jdbc:mysql://localhost:3306
connection-user=trino
connection-password=password
```

### **3. Query Examples**
```sql
-- Cross-source analytics
WITH sales_summary AS (
  SELECT 
    customer_id,
    SUM(amount) as total_sales,
    COUNT(*) as order_count
  FROM hive.warehouse.sales
  WHERE order_date >= DATE '2024-01-01'
  GROUP BY customer_id
),
customer_segments AS (
  SELECT 
    customer_id,
    segment,
    lifetime_value
  FROM mysql.crm.customers
)
SELECT 
  cs.segment,
  AVG(ss.total_sales) as avg_sales,
  COUNT(*) as customer_count
FROM sales_summary ss
JOIN customer_segments cs ON ss.customer_id = cs.customer_id
GROUP BY cs.segment
ORDER BY avg_sales DESC
```

---

## 📊 Performance Optimization

### **1. Query Optimization**
```sql
-- Use partition pruning
SELECT * FROM hive.sales.orders
WHERE year = 2024 AND month = 1  -- Partition columns

-- Predicate pushdown
SELECT customer_id, amount 
FROM hive.sales.orders
WHERE amount > 1000  -- Pushed to source

-- Join optimization
SELECT /*+ BROADCAST(small_table) */ *
FROM large_table l
JOIN small_table s ON l.id = s.id
```

### **2. Resource Management**
```properties
# Resource groups
resource-groups.configuration-manager=file
resource-groups.config-file=etc/resource-groups.json
```

```json
{
  "rootGroups": [
    {
      "name": "global",
      "softMemoryLimit": "80%",
      "maxQueued": 1000,
      "subGroups": [
        {
          "name": "adhoc",
          "softMemoryLimit": "50%",
          "maxQueued": 50
        },
        {
          "name": "pipeline", 
          "softMemoryLimit": "30%",
          "maxQueued": 10
        }
      ]
    }
  ]
}
```

---

## 🛠️ Common Use Cases

### **1. Data Lake Analytics**
```sql
-- Query across multiple formats
SELECT 
  p.product_name,
  SUM(s.quantity) as total_sold
FROM iceberg.warehouse.sales s
JOIN delta.catalog.products p ON s.product_id = p.id
WHERE s.sale_date >= DATE '2024-01-01'
GROUP BY p.product_name
```

### **2. Real-time Dashboards**
```sql
-- Fast aggregations for dashboards
SELECT 
  DATE(order_timestamp) as order_date,
  COUNT(*) as order_count,
  SUM(amount) as revenue
FROM hive.realtime.orders
WHERE order_timestamp >= NOW() - INTERVAL '7' DAY
GROUP BY DATE(order_timestamp)
ORDER BY order_date
```

### **3. Data Migration**
```sql
-- Cross-system data movement
CREATE TABLE hive.warehouse.migrated_customers AS
SELECT 
  customer_id,
  customer_name,
  email,
  registration_date
FROM mysql.legacy.customers
WHERE registration_date >= DATE '2020-01-01'
```

---

## 💡 Best Practices

### **1. Query Design**
- Use **partition pruning** when possible
- Apply **filters early** in queries
- Choose appropriate **join strategies**
- Limit **result set sizes**

### **2. Connector Configuration**
- Configure **connection pooling**
- Set appropriate **timeouts**
- Use **predicate pushdown**
- Enable **statistics collection**

### **3. Performance Tuning**
```properties
# Tuning parameters
join-distribution-type=AUTOMATIC
optimizer.join-reordering-strategy=AUTOMATIC
optimizer.use-mark-distinct=true
experimental.optimizer.enable-stats-calculator=true
```

---

## 🎯 When to Choose Trino

### **✅ Choose Trino When:**
- Need **federated queries** across multiple sources
- Require **interactive query performance**
- Have **diverse data sources** to unify
- Want **ANSI SQL** compatibility
- Need **elastic scaling**

### **❌ Consider Alternatives When:**
- Need **batch processing** (use Spark)
- Require **streaming** (use Flink)
- Have **single data source** (use native tools)
- Need **complex transformations** (use Spark)

---

## 🔗 Integration Ecosystem

### **Data Sources**
- **Data Lakes**: S3, HDFS, ADLS
- **Databases**: MySQL, PostgreSQL, Oracle
- **NoSQL**: MongoDB, Cassandra, Elasticsearch
- **Cloud**: BigQuery, Redshift, Snowflake

### **BI Tools**
- **Tableau**, **Power BI**, **Looker**
- **Superset**, **Metabase**
- **Jupyter**, **Zeppelin**

---

**🎯 Next Steps**: Check out [Interview Questions](./TRINO_INTERVIEW_QUESTIONS.md)