# InfluxDB Interview Questions

## Table of Contents

1. [Basic InfluxDB Questions](#basic-influxdb-questions)
2. [Data Model & Schema](#data-model--schema)
3. [InfluxQL & Flux Queries](#influxql--flux-queries)
4. [Performance & Optimization](#performance--optimization)
5. [Retention & Storage](#retention--storage)
6. [Clustering & High Availability](#clustering--high-availability)
7. [Integration & Monitoring](#integration--monitoring)
8. [Scenario-Based Questions](#scenario-based-questions)

---

## Basic InfluxDB Questions

### 1. What is InfluxDB and what makes it suitable for time-series data?
**Answer:**
InfluxDB is a purpose-built time-series database optimized for handling time-stamped data.

**Key Features:**
- **Time-Optimized Storage**: Columnar storage optimized for time-series
- **High Write Throughput**: Handles millions of writes per second
- **Automatic Downsampling**: Built-in data aggregation and retention
- **SQL-like Query Language**: InfluxQL and Flux for querying
- **Built-in Functions**: Time-series specific functions and operations

### 2. How does InfluxDB differ from traditional relational databases?
**Answer:**
- **Schema**: Schema-on-write vs. rigid schema
- **Time Focus**: Time as first-class citizen vs. regular column
- **Write Optimization**: Optimized for high-frequency writes
- **Compression**: Time-series specific compression algorithms
- **Retention**: Built-in data lifecycle management
- **Aggregation**: Native time-based aggregation functions

### 3. What are the main use cases for InfluxDB?
**Answer:**
- **IoT Monitoring**: Sensor data collection and analysis
- **Application Performance Monitoring**: Metrics and traces
- **Infrastructure Monitoring**: Server and network metrics
- **Financial Data**: Stock prices, trading volumes
- **Industrial Automation**: Manufacturing and process data
- **Real-time Analytics**: Live dashboards and alerting

### 4. Explain InfluxDB's position in the TICK stack.
**Answer:**
**TICK Stack Components:**
- **Telegraf**: Data collection agent
- **InfluxDB**: Time-series database storage
- **Chronograf**: Visualization and dashboarding
- **Kapacitor**: Real-time streaming data processing and alerting

### 5. What are the different versions of InfluxDB?
**Answer:**
- **InfluxDB 1.x**: Original version with InfluxQL
- **InfluxDB 2.x**: Unified platform with Flux query language
- **InfluxDB Cloud**: Fully managed cloud service
- **InfluxDB Enterprise**: Commercial version with clustering

## Data Model & Schema

### 6. Explain InfluxDB's data model components.
**Answer:**
- **Measurement**: Similar to table, container for related data
- **Tags**: Indexed metadata (key-value pairs)
- **Fields**: Actual data values (not indexed)
- **Timestamp**: Time when data point was recorded
- **Series**: Unique combination of measurement, tag set, and field key

### 7. What is the difference between tags and fields in InfluxDB?
**Answer:**
**Tags:**
- Indexed for fast queries
- String values only
- Used for grouping and filtering
- Limited cardinality recommended
- Metadata about the measurement

**Fields:**
- Not indexed by default
- Multiple data types (float, integer, string, boolean)
- Actual measured values
- Can have high cardinality
- The data you want to analyze

### 8. How do you design an efficient InfluxDB schema?
**Answer:**
```sql
-- Good schema design
measurement: cpu_usage
tags: host=server1, region=us-east, environment=prod
fields: usage_percent=75.5, cores=8
timestamp: 2023-01-15T10:30:00Z

-- Best practices:
-- 1. Use tags for metadata (low cardinality)
-- 2. Use fields for measured values
-- 3. Keep tag cardinality low (< 100K unique combinations)
-- 4. Choose appropriate measurement names
-- 5. Use consistent naming conventions
```

### 9. What is series cardinality and why is it important?
**Answer:**
Series cardinality is the number of unique tag combinations:
- **High Cardinality Problems**: Memory usage, slow queries, indexing overhead
- **Calculation**: Product of unique values across all tags
- **Best Practices**: Keep total series under 1 million per database
- **Monitoring**: Use `SHOW SERIES CARDINALITY` to monitor
- **Mitigation**: Redesign schema, use fields instead of tags

### 10. How do you handle high-cardinality data in InfluxDB?
**Answer:**
- **Schema Redesign**: Move high-cardinality data to fields
- **Bucketing**: Group similar values into buckets
- **Sampling**: Reduce data resolution for high-cardinality sources
- **Separate Measurements**: Split data across multiple measurements
- **Time-based Partitioning**: Use time-based measurement names

## InfluxQL & Flux Queries

### 11. What is InfluxQL and its basic syntax?
**Answer:**
InfluxQL is SQL-like query language for InfluxDB 1.x:
```sql
-- Basic query structure
SELECT <field_key> FROM <measurement_name> WHERE <conditions> GROUP BY <tag_key>

-- Example
SELECT mean(usage_percent) 
FROM cpu_usage 
WHERE time >= now() - 1h 
GROUP BY host, time(5m)
```

### 12. What is Flux and how does it differ from InfluxQL?
**Answer:**
Flux is a functional query language for InfluxDB 2.x:
- **Functional**: Data flows through functions
- **More Powerful**: Advanced data processing capabilities
- **Cross-Database**: Query multiple data sources
- **Scripting**: Support for variables and custom functions

```flux
from(bucket: "metrics")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "cpu_usage")
  |> aggregateWindow(every: 5m, fn: mean)
  |> group(columns: ["host"])
```

### 13. How do you perform aggregations in InfluxDB?
**Answer:**
**InfluxQL:**
```sql
-- Time-based aggregation
SELECT mean(value) FROM temperature 
WHERE time >= now() - 1d 
GROUP BY time(1h)

-- Tag-based aggregation
SELECT sum(bytes_sent) FROM network 
WHERE time >= now() - 1h 
GROUP BY host
```

**Flux:**
```flux
from(bucket: "sensors")
  |> range(start: -1d)
  |> filter(fn: (r) => r._measurement == "temperature")
  |> aggregateWindow(every: 1h, fn: mean)
```

### 14. What are continuous queries and how do you use them?
**Answer:**
Continuous queries automatically downsample data at regular intervals:
```sql
-- Create continuous query
CREATE CONTINUOUS QUERY "cq_mean_temp" ON "mydb"
BEGIN
  SELECT mean(temperature) 
  INTO "average_temp"
  FROM "raw_temp"
  GROUP BY time(1h), *
END

-- Benefits: Automatic downsampling, improved query performance
-- Use cases: Creating rollup data, reducing storage requirements
```

### 15. How do you handle missing data and interpolation?
**Answer:**
**InfluxQL:**
```sql
-- Fill missing values
SELECT mean(value) FROM measurement 
WHERE time >= now() - 1h 
GROUP BY time(5m) fill(linear)

-- Fill options: null, none, previous, linear, <value>
```

**Flux:**
```flux
from(bucket: "data")
  |> range(start: -1h)
  |> aggregateWindow(every: 5m, fn: mean, createEmpty: true)
  |> fill(usePrevious: true)
```

## Performance & Optimization

### 16. How do you optimize InfluxDB write performance?
**Answer:**
- **Batch Writes**: Write multiple points in single request
- **Line Protocol**: Use efficient line protocol format
- **Consistent Timestamps**: Write data in time order when possible
- **Appropriate Precision**: Use appropriate timestamp precision
- **Connection Pooling**: Reuse HTTP connections
- **Parallel Writes**: Use multiple writers for high throughput

### 17. What factors affect InfluxDB query performance?
**Answer:**
- **Time Range**: Smaller time ranges query faster
- **Series Cardinality**: Lower cardinality improves performance
- **Indexing**: Tags are indexed, fields are not
- **Memory**: Sufficient RAM for working set
- **Storage**: SSD storage for better I/O performance
- **Query Structure**: Efficient WHERE clauses and GROUP BY

### 18. How do you monitor InfluxDB performance?
**Answer:**
**Key Metrics:**
- **Write Throughput**: Points per second
- **Query Response Time**: Query execution duration
- **Memory Usage**: Heap and cache utilization
- **Disk I/O**: Read/write operations per second
- **Series Cardinality**: Number of unique series

**Monitoring Tools:**
```sql
-- Internal metrics
SHOW STATS
SHOW DIAGNOSTICS

-- Query performance
SHOW QUERIES
KILL QUERY <query_id>
```

### 19. What are the best practices for InfluxDB indexing?
**Answer:**
- **Tag Indexing**: Tags are automatically indexed
- **Selective Tags**: Only use tags for frequently queried dimensions
- **Cardinality Control**: Keep tag cardinality reasonable
- **Composite Indexes**: InfluxDB creates composite indexes automatically
- **Field Indexing**: Fields are not indexed (by design)
- **Time Indexing**: Time is always indexed efficiently

### 20. How do you handle large datasets in InfluxDB?
**Answer:**
- **Retention Policies**: Automatically delete old data
- **Downsampling**: Use continuous queries for aggregation
- **Sharding**: Distribute data across multiple databases
- **Compression**: Enable compression for storage efficiency
- **Partitioning**: Use measurement-based partitioning
- **Hardware Scaling**: Scale storage and memory appropriately

## Retention & Storage

### 21. What are retention policies in InfluxDB?
**Answer:**
Retention policies define how long data is kept:
```sql
-- Create retention policy
CREATE RETENTION POLICY "one_week" ON "mydb" 
DURATION 7d REPLICATION 1 DEFAULT

-- Show retention policies
SHOW RETENTION POLICIES ON "mydb"

-- Modify retention policy
ALTER RETENTION POLICY "one_week" ON "mydb" 
DURATION 14d DEFAULT
```

### 22. How does InfluxDB handle data compression?
**Answer:**
- **Automatic Compression**: Data compressed when written to disk
- **Time-Series Optimization**: Specialized compression for time-series
- **Snappy Compression**: Default compression algorithm
- **Compression Ratios**: Typically 10:1 to 100:1 compression
- **Trade-offs**: CPU usage vs. storage savings

### 23. What is the Time Structured Merge Tree (TSM) storage engine?
**Answer:**
TSM is InfluxDB's storage engine:
- **Write-Ahead Log (WAL)**: Temporary storage for incoming writes
- **Cache**: In-memory storage for recent data
- **TSM Files**: Compressed, immutable files on disk
- **Compaction**: Background process to optimize storage
- **Index**: Separate index files for fast lookups

### 24. How do you backup and restore InfluxDB?
**Answer:**
**Backup:**
```bash
# Full backup
influxd backup -portable /path/to/backup

# Database-specific backup
influxd backup -portable -database mydb /path/to/backup

# Incremental backup
influxd backup -portable -start 2023-01-01T00:00:00Z /path/to/backup
```

**Restore:**
```bash
# Restore from backup
influxd restore -portable /path/to/backup

# Restore specific database
influxd restore -portable -db mydb /path/to/backup
```

### 25. What are shard groups and how do they work?
**Answer:**
Shard groups organize data by time:
- **Time-based Partitioning**: Data partitioned by time ranges
- **Shard Duration**: Configurable time range per shard
- **Automatic Management**: InfluxDB manages shard lifecycle
- **Query Optimization**: Queries only access relevant shards
- **Retention**: Entire shards deleted when expired

## Clustering & High Availability

### 26. How does InfluxDB Enterprise clustering work?
**Answer:**
**Architecture:**
- **Data Nodes**: Store time-series data
- **Meta Nodes**: Store cluster metadata
- **Replication**: Data replicated across nodes
- **Consistency**: Eventually consistent system
- **Load Balancing**: Distribute queries across nodes

### 27. What are the high availability options for InfluxDB?
**Answer:**
- **InfluxDB Enterprise**: Built-in clustering and replication
- **InfluxDB Cloud**: Managed service with HA
- **Backup/Restore**: Regular backups for disaster recovery
- **Read Replicas**: Multiple read-only instances
- **Load Balancers**: Distribute traffic across instances

### 28. How do you handle failover in InfluxDB?
**Answer:**
- **Automatic Failover**: Enterprise edition supports automatic failover
- **Health Checks**: Monitor node health and availability
- **Client Configuration**: Configure clients for multiple endpoints
- **Data Replication**: Ensure data is replicated before failover
- **Recovery Procedures**: Document recovery processes

## Integration & Monitoring

### 29. How do you integrate InfluxDB with other systems?
**Answer:**
**Data Ingestion:**
- **Telegraf**: Agent-based data collection
- **HTTP API**: Direct writes via REST API
- **Client Libraries**: Official libraries for various languages
- **Kafka**: Stream data from Kafka topics
- **MQTT**: IoT device integration

**Data Export:**
- **Grafana**: Visualization and dashboarding
- **Kapacitor**: Stream processing and alerting
- **REST API**: Query data via HTTP
- **CSV Export**: Export data to CSV format

### 30. What is Telegraf and how does it work with InfluxDB?
**Answer:**
Telegraf is a plugin-driven agent for collecting metrics:
- **Input Plugins**: Collect data from various sources
- **Output Plugins**: Send data to InfluxDB and other destinations
- **Processor Plugins**: Transform data in transit
- **Aggregator Plugins**: Aggregate metrics before output
- **Configuration**: TOML-based configuration files

```toml
# Example Telegraf configuration
[[inputs.cpu]]
  percpu = true
  totalcpu = true

[[outputs.influxdb]]
  urls = ["http://localhost:8086"]
  database = "telegraf"
```

### 31. How do you set up alerting with InfluxDB?
**Answer:**
**Using Kapacitor:**
```javascript
// TICKscript for alerting
stream
  |from()
    .measurement('cpu_usage')
  |alert()
    .crit(lambda: "usage_percent" > 90)
    .message('High CPU usage detected')
    .email('admin@company.com')
```

**Using InfluxDB 2.x:**
- **Checks**: Define threshold-based checks
- **Notification Rules**: Configure alert destinations
- **Notification Endpoints**: Slack, email, webhooks
- **Task System**: Custom alerting logic with Flux

## Scenario-Based Questions

### 32. You need to monitor IoT sensors generating 1M data points per second. How do you design the solution?
**Answer:**
1. **Schema Design**: Use efficient tag/field structure
2. **Batch Writes**: Aggregate writes to reduce overhead
3. **Retention Strategy**: Implement tiered retention policies
4. **Downsampling**: Use continuous queries for aggregation
5. **Hardware**: Scale storage and memory appropriately
6. **Monitoring**: Track write performance and resource usage

```sql
-- Example schema
measurement: sensor_data
tags: sensor_id, location, type
fields: temperature, humidity, pressure
retention: raw(7d), hourly(30d), daily(1y)
```

### 33. Your InfluxDB queries are running slowly. How do you troubleshoot?
**Answer:**
1. **Check Series Cardinality**: High cardinality causes performance issues
2. **Analyze Query Patterns**: Identify expensive operations
3. **Review Time Ranges**: Large time ranges slow queries
4. **Monitor Resources**: Check memory and CPU usage
5. **Optimize Schema**: Redesign tags/fields if necessary
6. **Index Usage**: Ensure queries use indexed tags
7. **Hardware**: Consider scaling resources

### 34. How would you migrate time-series data from a relational database to InfluxDB?
**Answer:**
1. **Schema Analysis**: Map relational schema to InfluxDB model
2. **Data Extraction**: Export data with timestamps
3. **Transformation**: Convert to line protocol format
4. **Batch Import**: Use batch writes for efficiency
5. **Validation**: Verify data integrity and completeness
6. **Performance Testing**: Validate query performance
7. **Application Updates**: Modify applications to use InfluxDB

### 35. Design a real-time monitoring system for a web application using InfluxDB.
**Answer:**
```sql
-- Metrics schema
measurement: http_requests
tags: method, status_code, endpoint, server
fields: response_time, request_size, response_size

measurement: system_metrics  
tags: host, service
fields: cpu_percent, memory_percent, disk_usage

-- Alerting rules
SELECT mean(response_time) FROM http_requests 
WHERE time >= now() - 5m 
GROUP BY endpoint
HAVING mean(response_time) > 1000
```

**Architecture:**
1. **Data Collection**: Telegraf agents on servers
2. **Storage**: InfluxDB for metrics storage
3. **Processing**: Kapacitor for real-time alerting
4. **Visualization**: Grafana dashboards
5. **Alerting**: Multi-channel notifications

### 36. How would you implement data retention and lifecycle management?
**Answer:**
```sql
-- Multi-tier retention strategy
CREATE RETENTION POLICY "raw_data" ON "metrics" 
DURATION 7d REPLICATION 1

CREATE RETENTION POLICY "hourly_data" ON "metrics" 
DURATION 30d REPLICATION 1

CREATE RETENTION POLICY "daily_data" ON "metrics" 
DURATION 365d REPLICATION 1 DEFAULT

-- Continuous queries for downsampling
CREATE CONTINUOUS QUERY "downsample_hourly" ON "metrics"
BEGIN
  SELECT mean(*) INTO "metrics"."hourly_data".:MEASUREMENT
  FROM "metrics"."raw_data"./.*/ 
  GROUP BY time(1h), *
END
```

---

## Key Takeaways for Interviews

1. **Time-Series Focus**: Understand why InfluxDB is optimized for time-series data
2. **Data Model**: Master the concepts of measurements, tags, fields, and series
3. **Query Languages**: Know both InfluxQL and Flux capabilities
4. **Performance**: Understand cardinality impact and optimization techniques
5. **Retention**: Know how to implement data lifecycle management
6. **Integration**: Be familiar with TICK stack and common integrations
7. **Monitoring**: Understand how to monitor and troubleshoot InfluxDB
8. **Real-world Scenarios**: Practice designing solutions for IoT and monitoring use cases