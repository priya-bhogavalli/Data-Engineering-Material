# 📊 InfluxDB Interview Questions & Answers

## 📋 Table of Contents
- [Basic Concepts](#basic-concepts)
- [Data Model](#data-model)
- [Query Language](#query-language)
- [Architecture](#architecture)
- [Performance](#performance)
- [Operations](#operations)
- [Advanced Topics](#advanced-topics)

---

## Basic Concepts

### 1. What is InfluxDB and what makes it suitable for time-series data?
**Answer:**
InfluxDB is a purpose-built time-series database optimized for handling time-stamped data.

**Key Features:**
- **Time-optimized storage**: Efficient compression for time-series data
- **High write throughput**: Handles millions of writes per second
- **Built-in retention policies**: Automatic data lifecycle management
- **Downsampling**: Automatic data aggregation over time
- **SQL-like query language**: Flux and InfluxQL
- **Schemaless**: No predefined schema required

**Use Cases:**
- IoT sensor data
- Application metrics
- System monitoring
- Financial market data

### 2. Explain InfluxDB's data model and key concepts.
**Answer:**
**Core Concepts:**

**Measurement**: Similar to a table in SQL
**Tags**: Indexed metadata (key-value pairs)
**Fields**: Actual data values (not indexed)
**Timestamp**: Time when data point was recorded
**Point**: Single data record

**Example:**
```
measurement: cpu_usage
tags: host=server1, region=us-west
fields: usage_idle=85.2, usage_system=10.1
timestamp: 2024-03-01T10:00:00Z
```

**Data Structure:**
```
cpu_usage,host=server1,region=us-west usage_idle=85.2,usage_system=10.1 1709287200000000000
```

### 3. What is the difference between tags and fields in InfluxDB?
**Answer:**
**Tags:**
- Indexed for fast queries
- Used for grouping and filtering
- Always stored as strings
- Should have limited cardinality
- Metadata about the measurement

**Fields:**
- Not indexed (except in InfluxDB 2.0+)
- Contain the actual measured values
- Can be various data types (float, integer, string, boolean)
- Used for calculations and aggregations

**Example:**
```influxql
-- Tags: host, region (indexed, filterable)
-- Fields: cpu_percent, memory_percent (values)
SELECT mean(cpu_percent) 
FROM system_metrics 
WHERE host = 'server1' AND time > now() - 1h
GROUP BY region
```

### 4. What are InfluxDB retention policies?
**Answer:**
Retention policies define how long data is kept and how it's stored.

**Components:**
- **Duration**: How long to keep data
- **Replication**: Number of copies (InfluxDB Enterprise)
- **Shard duration**: Time range covered by each shard

**Examples:**
```influxql
-- Create retention policy
CREATE RETENTION POLICY "one_week" ON "mydb" 
DURATION 7d REPLICATION 1 DEFAULT

-- Show retention policies
SHOW RETENTION POLICIES ON "mydb"

-- Use specific retention policy
SELECT * FROM "one_week"."cpu_usage"
```

### 5. What is continuous query in InfluxDB?
**Answer:**
Continuous queries automatically downsample data at regular intervals.

**Purpose:**
- Reduce storage requirements
- Pre-aggregate data for faster queries
- Implement data retention strategies

**Example:**
```influxql
-- Create continuous query for hourly averages
CREATE CONTINUOUS QUERY "hourly_avg" ON "mydb"
BEGIN
  SELECT mean(cpu_percent) AS mean_cpu
  INTO "average"."hourly_cpu"
  FROM "cpu_usage"
  GROUP BY time(1h), host
END

-- Resample every 30 minutes, look back 1 hour
CREATE CONTINUOUS QUERY "cq_basic" ON "mydb"
RESAMPLE EVERY 30m FOR 1h
BEGIN
  SELECT mean(temperature) 
  INTO "average"."temperature"
  FROM "sensors"
  GROUP BY time(10m), location
END
```

---

## Data Model

### 6. How do you design an efficient schema for InfluxDB?
**Answer:**
**Best Practices:**

**1. Tag Design:**
- Use tags for metadata you'll filter/group by
- Keep tag cardinality low (< 100K unique values)
- Avoid high-cardinality tags (UUIDs, timestamps)

**2. Field Design:**
- Store actual measurements as fields
- Use appropriate data types
- Avoid storing metadata as fields

**3. Measurement Design:**
- One measurement per data source/type
- Include context in measurement name

**Example Schema:**
```influxql
-- Good schema design
measurement: sensor_data
tags: sensor_id, location, sensor_type
fields: temperature, humidity, battery_level
timestamp: auto-generated

-- Bad schema (high cardinality tag)
measurement: sensor_data
tags: sensor_id, timestamp_string  -- BAD: high cardinality
fields: temperature, location       -- BAD: metadata as field
```

### 7. How do you handle high cardinality data in InfluxDB?
**Answer:**
**Strategies:**

**1. Reduce Tag Cardinality:**
```influxql
-- Instead of unique user IDs as tags
-- Use bucketed approach
tags: user_bucket=bucket_1, region=us-west
fields: user_id="user123", value=42.5

-- Or use fields for high cardinality data
tags: region=us-west, service=api
fields: user_id="user123", response_time=150
```

**2. Use Series Cardinality Monitoring:**
```bash
# Check series cardinality
influx -execute "SHOW SERIES CARDINALITY"

# Check tag cardinality
influx -execute "SHOW TAG KEY CARDINALITY"
```

**3. Implement Data Lifecycle:**
- Use retention policies
- Implement downsampling
- Archive old data

### 8. What are InfluxDB line protocol best practices?
**Answer:**
**Line Protocol Format:**
```
measurement,tag1=value1,tag2=value2 field1=value1,field2=value2 timestamp
```

**Best Practices:**

**1. Batch Writes:**
```python
# Good: Batch multiple points
points = [
    "cpu,host=server1 usage=80.1 1609459200000000000",
    "cpu,host=server2 usage=75.5 1609459200000000000",
    "memory,host=server1 usage=65.2 1609459200000000000"
]
client.write_points_from_dataframe(points)

# Bad: Individual writes
for point in points:
    client.write_points(point)  # Inefficient
```

**2. Proper Escaping:**
```
# Escape spaces and special characters
measurement\ name,tag\ key=tag\ value field\ key="field value" 1609459200000000000
```

**3. Consistent Timestamps:**
- Use nanosecond precision
- Ensure monotonic timestamps
- Handle clock skew

### 9. How do you model relationships in InfluxDB?
**Answer:**
**Approaches:**

**1. Denormalization (Recommended):**
```influxql
-- Include related data in same measurement
measurement: order_metrics
tags: customer_id, product_category, region
fields: order_value, quantity, customer_name, product_name
```

**2. Multiple Measurements with Common Tags:**
```influxql
-- Customer data
measurement: customers
tags: customer_id, region
fields: name, email, signup_date

-- Order data  
measurement: orders
tags: customer_id, product_id
fields: order_value, quantity
```

**3. Reference Fields:**
```influxql
-- Store references as fields
measurement: events
tags: event_type, region
fields: user_id, session_id, event_data
```

### 10. What are InfluxDB data types and their use cases?
**Answer:**
**Field Data Types:**

**Float (default):**
```influxql
cpu_usage=85.2
temperature=23.5
```

**Integer:**
```influxql
count=42i
user_id=12345i
```

**String:**
```influxql
status="active"
message="system started"
```

**Boolean:**
```influxql
is_active=true
error_occurred=false
```

**Usage Guidelines:**
- Use integers for counts, IDs
- Use floats for measurements, percentages
- Use strings for status, categories
- Use booleans for flags, states

---

## Query Language

### 11. Compare InfluxQL and Flux query languages.
**Answer:**
**InfluxQL (SQL-like):**
```influxql
SELECT mean(cpu_usage) 
FROM "system_metrics" 
WHERE time > now() - 1h 
GROUP BY time(5m), host
```

**Flux (Functional):**
```flux
from(bucket: "system_metrics")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "cpu_usage")
  |> aggregateWindow(every: 5m, fn: mean)
  |> group(columns: ["host"])
```

**Comparison:**
| Feature | InfluxQL | Flux |
|---------|----------|------|
| **Syntax** | SQL-like | Functional |
| **Flexibility** | Limited | High |
| **Performance** | Fast for simple queries | Optimized for complex operations |
| **Learning Curve** | Easy (SQL knowledge) | Steeper |
| **Future** | Maintenance mode | Active development |

### 12. How do you write efficient InfluxQL queries?
**Answer:**
**Optimization Techniques:**

**1. Use Time Bounds:**
```influxql
-- Good: Bounded time range
SELECT mean(cpu_usage) 
FROM system_metrics 
WHERE time > now() - 1h AND time < now()

-- Bad: Unbounded query
SELECT mean(cpu_usage) FROM system_metrics
```

**2. Filter by Tags First:**
```influxql
-- Good: Tag filter first
SELECT * FROM cpu_usage 
WHERE host = 'server1' AND time > now() - 1h

-- Less efficient: Field filter
SELECT * FROM cpu_usage 
WHERE cpu_percent > 80 AND time > now() - 1h
```

**3. Use Appropriate Aggregation:**
```influxql
-- Use GROUP BY time for downsampling
SELECT mean(cpu_usage) 
FROM system_metrics 
WHERE time > now() - 24h 
GROUP BY time(1h)
```

### 13. What are Flux functions and how to use them?
**Answer:**
**Common Flux Functions:**

**Data Selection:**
```flux
// Filter data
from(bucket: "sensors")
  |> range(start: -1h)
  |> filter(fn: (r) => r.sensor_type == "temperature")
  |> filter(fn: (r) => r._value > 25.0)
```

**Aggregation:**
```flux
// Time-based aggregation
from(bucket: "metrics")
  |> range(start: -24h)
  |> aggregateWindow(every: 1h, fn: mean)
  |> yield(name: "hourly_average")
```

**Transformation:**
```flux
// Mathematical operations
from(bucket: "sensors")
  |> range(start: -1h)
  |> map(fn: (r) => ({ r with _value: r._value * 1.8 + 32 }))  // C to F
```

**Joining Data:**
```flux
cpu = from(bucket: "system") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "cpu")
memory = from(bucket: "system") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "memory")

join(tables: {cpu: cpu, memory: memory}, on: ["_time", "host"])
```

### 14. How do you implement alerting with InfluxDB?
**Answer:**
**Kapacitor Integration (InfluxDB 1.x):**
```javascript
// TICKscript for CPU alerting
stream
  |from()
    .measurement('cpu_usage')
  |window()
    .period(5m)
    .every(1m)
  |mean('usage_idle')
  |alert()
    .crit(lambda: "mean" < 10)
    .message('High CPU usage detected')
    .email('admin@company.com')
```

**InfluxDB 2.0 Checks:**
```flux
// Threshold check
from(bucket: "system")
  |> range(start: -5m)
  |> filter(fn: (r) => r._measurement == "cpu")
  |> mean()
  |> map(fn: (r) => ({ r with _level: if r._value > 80.0 then "crit" else "ok" }))
```

**External Alerting:**
```python
# Python alerting script
def check_cpu_usage():
    query = '''
    SELECT mean(cpu_usage) 
    FROM system_metrics 
    WHERE time > now() - 5m
    '''
    result = client.query(query)
    
    if result.raw['series'][0]['values'][0][1] > 80:
        send_alert("High CPU usage detected")
```

### 15. How do you perform data transformations in InfluxDB?
**Answer:**
**Flux Transformations:**

**1. Mathematical Operations:**
```flux
from(bucket: "sensors")
  |> range(start: -1h)
  |> map(fn: (r) => ({ 
      r with 
      celsius: (r._value - 32.0) * 5.0 / 9.0,
      category: if r._value > 30.0 then "hot" else "normal"
  }))
```

**2. Data Reshaping:**
```flux
// Pivot data
from(bucket: "system")
  |> range(start: -1h)
  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
```

**3. Window Functions:**
```flux
// Moving average
from(bucket: "metrics")
  |> range(start: -24h)
  |> movingAverage(n: 5)
```

**4. Custom Functions:**
```flux
// Define custom function
normalize = (tables=<-) => tables
  |> map(fn: (r) => ({ r with _value: (r._value - r.min) / (r.max - r.min) }))

// Use custom function
from(bucket: "data") |> normalize()
```

---

## Architecture

### 16. Describe InfluxDB's storage engine and TSM files.
**Answer:**
**TSM (Time Structured Merge) Engine:**

**Components:**
- **WAL (Write-Ahead Log)**: Durability for writes
- **Cache**: In-memory storage for recent data
- **TSM Files**: Compressed, immutable files on disk
- **Index**: Fast lookups for series and tags

**Write Path:**
```
Write Request → WAL → Cache → TSM Files (when cache full)
```

**TSM File Structure:**
- **Header**: Metadata about the file
- **Blocks**: Compressed time-series data
- **Index**: Offset information for fast seeks
- **Footer**: Checksum and validation

**Compaction:**
- Merges multiple TSM files
- Removes deleted data
- Optimizes compression

### 17. How does InfluxDB handle clustering and high availability?
**Answer:**
**InfluxDB Enterprise Clustering:**

**Architecture:**
- **Data Nodes**: Store time-series data
- **Meta Nodes**: Store cluster metadata
- **Load Balancer**: Distributes client requests

**Replication:**
```bash
# Create database with replication
CREATE DATABASE "mydb" WITH REPLICATION 2

# Show shards and replication
SHOW SHARDS
```

**High Availability Setup:**
```yaml
# Meta node configuration
[meta]
  dir = "/var/lib/influxdb/meta"
  bind-address = ":8088"
  
# Data node configuration  
[data]
  dir = "/var/lib/influxdb/data"
  wal-dir = "/var/lib/influxdb/wal"
```

**InfluxDB 2.0 (OSS):**
- Single-node architecture
- Backup/restore for disaster recovery
- External replication solutions

### 18. What are InfluxDB shards and shard groups?
**Answer:**
**Sharding Concepts:**

**Shard**: Contains data for specific time range and retention policy
**Shard Group**: Collection of shards covering same time range
**Shard Duration**: Time range each shard covers

**Configuration:**
```influxql
-- Create retention policy with shard duration
CREATE RETENTION POLICY "policy_name" ON "database" 
DURATION 30d REPLICATION 1 SHARD DURATION 1d

-- Show shard information
SHOW SHARDS
```

**Shard Management:**
```bash
# Drop shard (data loss!)
DROP SHARD 123

# Copy shard to another server
influx_inspect copyshard -source /path/to/shard -dest server2:8088
```

**Best Practices:**
- Align shard duration with query patterns
- Consider retention policy duration
- Monitor shard distribution

### 19. How do you backup and restore InfluxDB?
**Answer:**
**Backup Methods:**

**1. Full Backup:**
```bash
# Backup entire database
influxd backup -portable -database mydb /backup/path/

# Backup all databases
influxd backup -portable /backup/path/
```

**2. Incremental Backup:**
```bash
# Backup changes since last backup
influxd backup -portable -database mydb -since 2024-03-01T00:00:00Z /backup/path/
```

**3. Online Backup (Enterprise):**
```bash
# Backup without stopping service
influxd backup -online -database mydb /backup/path/
```

**Restore Process:**
```bash
# Stop InfluxDB service
sudo systemctl stop influxdb

# Restore from backup
influxd restore -portable -database mydb /backup/path/

# Start InfluxDB service
sudo systemctl start influxdb
```

**Automated Backup Script:**
```bash
#!/bin/bash
BACKUP_DIR="/backups/influxdb/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

influxd backup -portable -database mydb $BACKUP_DIR

# Cleanup old backups (keep 7 days)
find /backups/influxdb/ -type d -mtime +7 -exec rm -rf {} \;
```

### 20. How do you monitor InfluxDB performance?
**Answer:**
**Key Metrics:**

**1. System Metrics:**
```influxql
-- Query performance
SHOW STATS FOR 'httpd'
SHOW STATS FOR 'queryExecutor'

-- Storage metrics
SHOW STATS FOR 'tsm1_engine'
SHOW STATS FOR 'tsm1_cache'
```

**2. Internal Monitoring:**
```bash
# Enable internal monitoring
[monitor]
  store-enabled = true
  store-database = "_internal"
  store-interval = "10s"
```

**3. Custom Monitoring:**
```python
# Monitor query performance
import time
from influxdb import InfluxDBClient

def monitor_query_performance():
    start_time = time.time()
    
    result = client.query("SELECT count(*) FROM my_measurement")
    
    execution_time = time.time() - start_time
    
    # Log slow queries
    if execution_time > 1.0:
        logger.warning(f"Slow query detected: {execution_time}s")
```

**Grafana Dashboard:**
```json
{
  "dashboard": {
    "title": "InfluxDB Monitoring",
    "panels": [
      {
        "title": "Query Rate",
        "targets": [
          {
            "query": "SELECT derivative(mean(queryReq), 1s) FROM _internal.monitor.httpd"
          }
        ]
      }
    ]
  }
}
```

---

## Performance

### 21. How do you optimize InfluxDB write performance?
**Answer:**
**Write Optimization Strategies:**

**1. Batch Writes:**
```python
# Good: Batch multiple points
points = []
for i in range(1000):
    point = {
        "measurement": "cpu_usage",
        "tags": {"host": f"server{i}"},
        "fields": {"usage": random.uniform(0, 100)},
        "time": datetime.utcnow()
    }
    points.append(point)

client.write_points(points, batch_size=5000)
```

**2. Configuration Tuning:**
```toml
[data]
  # Increase cache size
  cache-max-memory-size = "1g"
  
  # Tune WAL settings
  wal-fsync-delay = "100ms"
  
  # Optimize compaction
  compact-full-write-cold-duration = "4h"
```

**3. Hardware Optimization:**
- Use SSD for WAL directory
- Separate data and WAL on different disks
- Sufficient RAM for cache

### 22. How do you optimize InfluxDB query performance?
**Answer:**
**Query Optimization:**

**1. Index Usage:**
```influxql
-- Use indexed tags for filtering
SELECT * FROM cpu_usage 
WHERE host = 'server1'  -- Fast: uses tag index

-- Avoid field filters when possible
SELECT * FROM cpu_usage 
WHERE usage > 80  -- Slower: scans field values
```

**2. Time Range Optimization:**
```influxql
-- Always specify time bounds
SELECT mean(cpu_usage) 
FROM system_metrics 
WHERE time >= '2024-03-01T00:00:00Z' 
  AND time < '2024-03-02T00:00:00Z'
```

**3. Aggregation Strategies:**
```influxql
-- Use continuous queries for pre-aggregation
CREATE CONTINUOUS QUERY "hourly_avg" ON "mydb"
BEGIN
  SELECT mean(cpu_usage) AS avg_cpu
  INTO "downsampled"."cpu_hourly"
  FROM "cpu_usage"
  GROUP BY time(1h), host
END
```

### 23. What causes high cardinality issues and how to solve them?
**Answer:**
**High Cardinality Causes:**
- Using unique IDs as tags
- Timestamp strings as tags
- User-generated content as tags

**Detection:**
```bash
# Check series cardinality
influx -execute "SHOW SERIES CARDINALITY ON mydb"

# Check tag cardinality by key
influx -execute "SHOW TAG KEY CARDINALITY ON mydb"

# Find high cardinality measurements
influx -execute "SHOW SERIES CARDINALITY ON mydb GROUP BY measurement"
```

**Solutions:**

**1. Redesign Schema:**
```influxql
-- Bad: High cardinality tag
measurement: requests
tags: user_id=12345, endpoint=/api/users/12345
fields: response_time=150

-- Good: Use fields for high cardinality data
measurement: requests  
tags: endpoint_type=api, method=GET
fields: user_id=12345, response_time=150
```

**2. Use Bucketing:**
```influxql
-- Instead of exact user_id as tag
tags: user_bucket=bucket_001, region=us-west
fields: user_id=12345, value=42
```

### 24. How do you handle InfluxDB memory issues?
**Answer:**
**Memory Management:**

**1. Configuration Tuning:**
```toml
[data]
  # Limit cache memory
  cache-max-memory-size = "512m"
  
  # Tune snapshot settings
  cache-snapshot-memory-size = "25m"
  cache-snapshot-write-cold-duration = "10m"
```

**2. Query Optimization:**
```influxql
-- Avoid SELECT * on large datasets
SELECT cpu_usage FROM system_metrics 
WHERE time > now() - 1h
LIMIT 10000

-- Use aggregation to reduce data
SELECT mean(cpu_usage) FROM system_metrics 
WHERE time > now() - 24h 
GROUP BY time(1h)
```

**3. Monitoring Memory Usage:**
```bash
# Check memory stats
influx -execute "SHOW STATS FOR 'runtime'"

# Monitor heap size
influx -execute "SELECT * FROM _internal.monitor.runtime WHERE time > now() - 5m"
```

### 25. What are InfluxDB compaction strategies?
**Answer:**
**Compaction Types:**

**1. Level Compaction (Default):**
- Organizes TSM files in levels
- Merges files of similar size
- Good for mixed workloads

**2. Full Compaction:**
```toml
[data]
  # Force full compaction
  compact-full-write-cold-duration = "4h"
```

**Manual Compaction:**
```bash
# Compact specific shard
influx_inspect buildtsi -datadir /var/lib/influxdb/data -waldir /var/lib/influxdb/wal

# Compact all shards
influx_inspect compact-shard /var/lib/influxdb/data/mydb/autogen/123
```

**Monitoring Compaction:**
```influxql
-- Check compaction stats
SHOW STATS FOR 'tsm1_engine'

-- Monitor compaction queue
SELECT * FROM _internal.monitor.tsm1_engine 
WHERE time > now() - 5m
```

---

## Operations

### 26. How do you migrate data between InfluxDB instances?
**Answer:**
**Migration Methods:**

**1. Backup/Restore:**
```bash
# Source: Create backup
influxd backup -portable -database mydb /backup/

# Target: Restore backup
influxd restore -portable -database mydb /backup/
```

**2. Export/Import:**
```bash
# Export data
influx -database mydb -execute "SELECT * FROM measurement" -format csv > data.csv

# Import data (using line protocol)
influx -database mydb -import -path data.txt -precision ns
```

**3. Programmatic Migration:**
```python
def migrate_data(source_client, target_client, measurement):
    # Query source
    query = f"SELECT * FROM {measurement}"
    result = source_client.query(query)
    
    # Convert to line protocol
    points = []
    for point in result.get_points():
        line_protocol = format_line_protocol(point)
        points.append(line_protocol)
    
    # Write to target
    target_client.write_points_from_dataframe(points)
```

### 27. How do you upgrade InfluxDB versions?
**Answer:**
**Upgrade Process:**

**1. Pre-upgrade Steps:**
```bash
# Backup data
influxd backup -portable /backup/pre-upgrade/

# Check current version
influx -version

# Review release notes
# Test upgrade in staging environment
```

**2. Upgrade Steps:**
```bash
# Stop InfluxDB
sudo systemctl stop influxdb

# Install new version
sudo apt-get update
sudo apt-get install influxdb=1.8.10

# Start InfluxDB
sudo systemctl start influxdb

# Verify upgrade
influx -version
```

**3. Post-upgrade Verification:**
```bash
# Check database integrity
influx -execute "SHOW DATABASES"
influx -execute "SHOW MEASUREMENTS ON mydb"

# Run test queries
influx -execute "SELECT count(*) FROM my_measurement"
```

### 28. How do you implement InfluxDB security?
**Answer:**
**Security Configuration:**

**1. Authentication:**
```toml
[http]
  auth-enabled = true
  
[meta]
  auth-enabled = true
```

**2. User Management:**
```influxql
-- Create admin user
CREATE USER admin WITH PASSWORD 'password' WITH ALL PRIVILEGES

-- Create database user
CREATE USER dbuser WITH PASSWORD 'password'
GRANT ALL ON mydb TO dbuser

-- Create read-only user
CREATE USER readonly WITH PASSWORD 'password'
GRANT READ ON mydb TO readonly
```

**3. SSL/TLS:**
```toml
[http]
  https-enabled = true
  https-certificate = "/etc/ssl/influxdb.pem"
  https-private-key = "/etc/ssl/influxdb-key.pem"
```

**4. Network Security:**
```bash
# Firewall rules
sudo ufw allow from 192.168.1.0/24 to any port 8086
sudo ufw deny 8086
```

### 29. How do you troubleshoot InfluxDB performance issues?
**Answer:**
**Diagnostic Steps:**

**1. Check System Resources:**
```bash
# CPU and memory usage
top -p $(pgrep influxd)

# Disk I/O
iostat -x 1

# Network usage
netstat -i
```

**2. InfluxDB Diagnostics:**
```bash
# Generate diagnostic report
influx_inspect report

# Check query performance
influx -execute "SHOW QUERIES"

# Monitor internal stats
influx -execute "SELECT * FROM _internal.monitor.httpd WHERE time > now() - 5m"
```

**3. Query Analysis:**
```influxql
-- Identify slow queries
SHOW QUERIES

-- Kill long-running query
KILL QUERY 123
```

### 30. What are InfluxDB best practices for production?
**Answer:**
**Production Guidelines:**

**1. Hardware Sizing:**
- SSD storage for better I/O
- Sufficient RAM (8GB+ recommended)
- Separate WAL and data directories

**2. Configuration:**
```toml
[data]
  # Optimize for your workload
  cache-max-memory-size = "1g"
  wal-fsync-delay = "100ms"
  
[http]
  # Security settings
  auth-enabled = true
  max-connection-limit = 0
  
[logging]
  level = "info"
```

**3. Monitoring:**
- Set up alerting for key metrics
- Monitor disk usage and growth
- Track query performance
- Monitor cardinality growth

**4. Maintenance:**
- Regular backups
- Monitor and manage retention policies
- Plan for capacity growth
- Keep InfluxDB updated

---

## Advanced Topics

### 31. How do you implement custom functions in Flux?
**Answer:**
**Custom Function Definition:**
```flux
// Define reusable function
calculateSMA = (tables=<-, n) => tables
  |> movingAverage(n: n)
  |> map(fn: (r) => ({ r with _value: r._value }))

// Use custom function
from(bucket: "stock_prices")
  |> range(start: -30d)
  |> filter(fn: (r) => r._measurement == "price")
  |> calculateSMA(n: 10)
```

**Package Creation:**
```flux
// Create package file: sma.flux
package sma

// Export function
builtin movingAverage : (<-tables: stream[A], n: int) => stream[A] where A: Record

calculateSMA = (tables=<-, n) => tables |> movingAverage(n: n)
```

### 32. How do you integrate InfluxDB with other systems?
**Answer:**
**Integration Patterns:**

**1. Telegraf Integration:**
```toml
# telegraf.conf
[[outputs.influxdb_v2]]
  urls = ["http://localhost:8086"]
  token = "your-token"
  organization = "your-org"
  bucket = "your-bucket"

[[inputs.cpu]]
  percpu = true
  totalcpu = true
```

**2. Grafana Integration:**
```json
{
  "datasource": {
    "type": "influxdb",
    "url": "http://localhost:8086",
    "database": "mydb",
    "user": "grafana",
    "password": "password"
  }
}
```

**3. Application Integration:**
```python
# Python client
from influxdb_client import InfluxDBClient, Point

client = InfluxDBClient(url="http://localhost:8086", token="token", org="org")
write_api = client.write_api()

# Write data
point = Point("measurement").tag("host", "server1").field("cpu", 85.2)
write_api.write(bucket="bucket", record=point)
```

### 33. How do you implement real-time analytics with InfluxDB?
**Answer:**
**Real-time Architecture:**

**1. Streaming Ingestion:**
```python
# Kafka consumer to InfluxDB
from kafka import KafkaConsumer
from influxdb_client import InfluxDBClient

consumer = KafkaConsumer('sensor_data')
client = InfluxDBClient(url="http://localhost:8086", token="token")

for message in consumer:
    data = json.loads(message.value)
    
    point = Point("sensors") \
        .tag("sensor_id", data["sensor_id"]) \
        .field("temperature", data["temperature"]) \
        .time(data["timestamp"])
    
    client.write_api().write(bucket="sensors", record=point)
```

**2. Real-time Queries:**
```flux
// Continuous monitoring query
from(bucket: "sensors")
  |> range(start: -5m)
  |> filter(fn: (r) => r._measurement == "temperature")
  |> aggregateWindow(every: 30s, fn: mean)
  |> map(fn: (r) => ({ 
      r with 
      alert: if r._value > 30.0 then "HIGH" else "NORMAL" 
  }))
```

### 34. How do you handle InfluxDB in microservices architecture?
**Answer:**
**Microservices Patterns:**

**1. Service-per-Database:**
```yaml
# docker-compose.yml
version: '3'
services:
  user-service:
    image: user-service:latest
    environment:
      INFLUXDB_URL: http://user-influxdb:8086
      
  user-influxdb:
    image: influxdb:2.0
    environment:
      INFLUXDB_DB: user_metrics
      
  order-service:
    image: order-service:latest
    environment:
      INFLUXDB_URL: http://order-influxdb:8086
      
  order-influxdb:
    image: influxdb:2.0
    environment:
      INFLUXDB_DB: order_metrics
```

**2. Shared InfluxDB with Namespacing:**
```python
# Service-specific bucket/measurement naming
class MetricsService:
    def __init__(self, service_name):
        self.service_name = service_name
        self.bucket = f"{service_name}_metrics"
        
    def write_metric(self, metric_name, value, tags=None):
        measurement = f"{self.service_name}_{metric_name}"
        # Write to service-specific measurement
```

### 35. What are InfluxDB 3.0 new features and improvements?
**Answer:**
**InfluxDB 3.0 Features:**

**1. Apache Arrow Integration:**
- Columnar data format
- Better query performance
- Improved analytics capabilities

**2. Object Storage Support:**
- S3-compatible storage
- Separation of compute and storage
- Better scalability

**3. SQL Query Support:**
```sql
-- Native SQL queries
SELECT AVG(cpu_usage) as avg_cpu
FROM system_metrics 
WHERE time >= NOW() - INTERVAL '1 hour'
GROUP BY host
```

**4. Improved Performance:**
- Faster ingestion rates
- Better compression
- Optimized query execution

**5. Cloud-Native Architecture:**
- Kubernetes-native deployment
- Auto-scaling capabilities
- Multi-tenancy support

---

*This comprehensive guide covers 35+ essential InfluxDB interview questions with detailed answers and practical examples for data engineering interviews.*