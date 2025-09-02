# 📈 InfluxDB Interview Questions for Data Engineering

## 📋 Table of Contents

1. [Core Concepts (1-25)](#core-concepts-1-25)
2. [Data Modeling (26-50)](#data-modeling-26-50)
3. [Queries & Analytics (51-75)](#queries--analytics-51-75)
4. [Operations & Scaling (76-100)](#operations--scaling-76-100)

---

## Core Concepts (1-25)

### 1. What is InfluxDB and why use it for time-series data?
**Answer**: InfluxDB is a purpose-built time-series database optimized for time-stamped data.

**Key Features:**
- **High Write Performance**: Millions of points per second
- **Compression**: Efficient storage of time-series data
- **Retention Policies**: Automatic data lifecycle management
- **Continuous Queries**: Real-time aggregation
- **Built-in Functions**: Time-series specific operations

```sql
-- Create database
CREATE DATABASE sensors

-- Create retention policy
CREATE RETENTION POLICY "one_week" ON "sensors" DURATION 7d REPLICATION 1 DEFAULT

-- Write data points
INSERT cpu,host=server1,region=us-east value=80.5 1609459200000000000
INSERT memory,host=server1,region=us-east value=65.2 1609459200000000000
INSERT disk,host=server1,region=us-east,device=sda1 value=45.8 1609459200000000000
```

### 2. Explain InfluxDB's data model
**Answer**: InfluxDB uses measurements, tags, fields, and timestamps.

```sql
-- Data structure: measurement,tag_key=tag_value field_key=field_value timestamp
-- measurement: table equivalent
-- tags: indexed metadata (string only)
-- fields: actual data values (various types)
-- timestamp: nanosecond precision

-- Example data points
temperature,sensor=sensor1,location=room1 value=23.5,humidity=45.2 1609459200000000000
temperature,sensor=sensor2,location=room2 value=24.1,humidity=43.8 1609459260000000000

-- Query structure
SELECT value, humidity 
FROM temperature 
WHERE sensor='sensor1' AND time > now() - 1h
```

### 3. How do you write data to InfluxDB?
**Answer**: Use line protocol, HTTP API, or client libraries.

```python
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# Initialize client
client = InfluxDBClient(url="http://localhost:8086", token="your-token", org="your-org")
write_api = client.write_api(write_option=SYNCHRONOUS)

# Write single point
point = Point("temperature") \
    .tag("sensor", "sensor1") \
    .tag("location", "room1") \
    .field("value", 23.5) \
    .field("humidity", 45.2) \
    .time(datetime.utcnow())

write_api.write(bucket="sensors", record=point)

# Batch write
points = []
for i in range(1000):
    point = Point("cpu_usage") \
        .tag("host", f"server{i%10}") \
        .tag("region", "us-east") \
        .field("value", random.uniform(0, 100)) \
        .time(datetime.utcnow() - timedelta(seconds=i))
    points.append(point)

write_api.write(bucket="metrics", record=points)
```

## Data Modeling (26-50)

### 26. How do you design schemas for time-series data?
**Answer**: Optimize for query patterns and cardinality.

```sql
-- Good schema design
-- measurement: metric type
-- tags: dimensions for filtering/grouping (low cardinality)
-- fields: actual measurements (high cardinality OK)

-- IoT sensor data
CREATE MEASUREMENT sensor_readings
-- Tags (indexed, low cardinality)
sensor_id,device_type,location,building
-- Fields (not indexed, high cardinality OK)  
temperature,humidity,pressure,battery_level

-- Application metrics
CREATE MEASUREMENT app_metrics
-- Tags
service_name,environment,instance_id,method
-- Fields
response_time,error_count,request_count,cpu_usage

-- Bad design (high cardinality tags)
-- DON'T DO: user_id as tag (millions of unique values)
-- DO: user_id as field, use other dimensions as tags
```

### 27. How do you handle high cardinality data?
**Answer**: Use field values instead of tags for high cardinality dimensions.

```sql
-- High cardinality example: user activity tracking
-- Instead of: user_id as tag (bad)
user_activity,event_type=login,platform=web user_id="user123",session_duration=300

-- Better approach: aggregate by time windows
user_activity_hourly,platform=web,event_type=login 
  unique_users=1250,total_sessions=2100,avg_duration=245

-- Use continuous queries for aggregation
CREATE CONTINUOUS QUERY "hourly_user_stats" ON "analytics"
BEGIN
  SELECT COUNT(DISTINCT(user_id)) AS unique_users,
         COUNT(user_id) AS total_sessions,
         MEAN(session_duration) AS avg_duration
  INTO "user_activity_hourly"
  FROM "user_activity"
  GROUP BY time(1h), platform, event_type
END
```

## Queries & Analytics (51-75)

### 51. How do you write complex InfluxQL queries?
**Answer**: Use aggregation functions, grouping, and time windows.

```sql
-- Time-based aggregation
SELECT MEAN(value) AS avg_temp, MAX(value) AS max_temp
FROM temperature
WHERE time > now() - 24h
GROUP BY time(1h), sensor
FILL(linear)

-- Moving averages
SELECT MOVING_AVERAGE(MEAN(value), 5) AS moving_avg
FROM cpu_usage
WHERE time > now() - 6h
GROUP BY time(5m), host

-- Percentiles and statistical functions
SELECT PERCENTILE(response_time, 95) AS p95,
       PERCENTILE(response_time, 99) AS p99,
       STDDEV(response_time) AS stddev
FROM api_metrics
WHERE time > now() - 1h
GROUP BY time(5m), service

-- Subqueries and transformations
SELECT DERIVATIVE(MEAN(bytes_sent), 1s) AS bytes_per_second
FROM network_stats
WHERE time > now() - 30m
GROUP BY time(10s), interface

-- Complex filtering and conditions
SELECT COUNT(value) AS error_count
FROM application_logs
WHERE level = 'ERROR' 
  AND time > now() - 1h
  AND (service = 'api' OR service = 'worker')
GROUP BY time(5m), service, error_type
```

### 52. How do you implement real-time analytics?
**Answer**: Use continuous queries and Kapacitor for stream processing.

```sql
-- Continuous query for real-time aggregation
CREATE CONTINUOUS QUERY "realtime_cpu_avg" ON "monitoring"
RESAMPLE EVERY 10s FOR 30s
BEGIN
  SELECT MEAN(value) AS avg_cpu
  INTO "cpu_averages"
  FROM "cpu_usage"
  GROUP BY time(10s), host
END

-- Downsampling for long-term storage
CREATE CONTINUOUS QUERY "downsample_hourly" ON "sensors"
BEGIN
  SELECT MEAN(temperature) AS avg_temp,
         MIN(temperature) AS min_temp,
         MAX(temperature) AS max_temp,
         COUNT(temperature) AS count
  INTO "sensors"."one_year"."temperature_hourly"
  FROM "sensors"."one_week"."temperature"
  GROUP BY time(1h), *
END
```

```python
# Real-time alerting with Python
from influxdb_client import InfluxDBClient
import time

def monitor_metrics():
    client = InfluxDBClient(url="http://localhost:8086", token="your-token")
    query_api = client.query_api()
    
    while True:
        # Check for high CPU usage
        query = '''
        from(bucket: "monitoring")
          |> range(start: -5m)
          |> filter(fn: (r) => r._measurement == "cpu_usage")
          |> mean()
          |> filter(fn: (r) => r._value > 90.0)
        '''
        
        result = query_api.query(query)
        
        for table in result:
            for record in table.records:
                print(f"ALERT: High CPU on {record.values['host']}: {record.get_value()}%")
                # Send alert notification
        
        time.sleep(30)  # Check every 30 seconds
```

## Operations & Scaling (76-100)

### 76. How do you optimize InfluxDB performance?
**Answer**: Configure retention policies, sharding, and hardware optimization.

```sql
-- Retention policies for data lifecycle
CREATE RETENTION POLICY "realtime" ON "sensors" DURATION 1h REPLICATION 1
CREATE RETENTION POLICY "recent" ON "sensors" DURATION 7d REPLICATION 1  
CREATE RETENTION POLICY "historical" ON "sensors" DURATION 365d REPLICATION 1 DEFAULT

-- Shard duration optimization
ALTER RETENTION POLICY "recent" ON "sensors" SHARD DURATION 1h
ALTER RETENTION POLICY "historical" ON "sensors" SHARD DURATION 7d

-- Index optimization
-- Limit series cardinality
SHOW CARDINALITY ON "sensors"
SHOW TAG KEY CARDINALITY ON "sensors"

-- Monitor shard statistics
SHOW SHARDS
SHOW SHARD GROUPS
```

### 77. How do you backup and restore InfluxDB?
**Answer**: Use backup/restore commands and continuous replication.

```bash
# Backup database
influxd backup -database sensors /backup/sensors/

# Backup with time range
influxd backup -database sensors -start 2023-01-01T00:00:00Z -end 2023-01-31T23:59:59Z /backup/sensors_january/

# Restore database
influxd restore -database sensors /backup/sensors/

# Online backup with retention policy
influxd backup -database sensors -retention recent /backup/sensors_recent/

# Incremental backup
influxd backup -database sensors -since 2023-01-01T00:00:00Z /backup/sensors_incremental/
```

### 78. How do you monitor InfluxDB performance?
**Answer**: Use internal statistics and external monitoring tools.

```sql
-- Internal statistics
SHOW STATS

-- Query performance
SHOW QUERIES
KILL QUERY 123

-- Series cardinality monitoring
SHOW SERIES CARDINALITY ON "sensors"
SHOW TAG KEY CARDINALITY ON "sensors" FROM "temperature"

-- Shard statistics
SHOW SHARDS
SELECT * FROM "_internal"."monitor"."shard" WHERE time > now() - 1h

-- Write statistics
SELECT * FROM "_internal"."monitor"."write" WHERE time > now() - 1h

-- Query statistics  
SELECT * FROM "_internal"."monitor"."queryExecutor" WHERE time > now() - 1h
```

### 79. How do you scale InfluxDB?
**Answer**: Use clustering, federation, and horizontal partitioning.

```bash
# InfluxDB Enterprise clustering
# Meta nodes configuration
[meta]
  dir = "/var/lib/influxdb/meta"
  bind-address = ":8088"
  http-bind-address = ":8091"

# Data nodes configuration  
[data]
  dir = "/var/lib/influxdb/data"
  wal-dir = "/var/lib/influxdb/wal"

# Add data node to cluster
influxd-ctl add-data server2:8088

# Add meta node to cluster
influxd-ctl add-meta server3:8091

# Check cluster status
influxd-ctl show
```

---

**Total Questions: 100** | **Coverage: Complete InfluxDB Ecosystem**