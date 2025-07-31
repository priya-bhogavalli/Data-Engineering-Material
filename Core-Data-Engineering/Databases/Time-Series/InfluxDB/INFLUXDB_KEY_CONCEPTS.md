# InfluxDB Key Concepts

## 🎯 What is InfluxDB?
Purpose-built time-series database optimized for fast, high-availability storage and retrieval of time-series data.

## 🏗️ Core Concepts

### Data Model
```
measurement,tag1=value1,tag2=value2 field1=value1,field2=value2 timestamp
```

### Key Components
- **Measurement** - Similar to table (e.g., "temperature")
- **Tags** - Indexed metadata (e.g., location, sensor_id)
- **Fields** - Actual data values (e.g., temperature value)
- **Timestamp** - Time when data point was recorded

## 🔧 InfluxQL Queries

### Basic Operations
```sql
-- Insert data (Line Protocol)
temperature,location=office,sensor=A001 value=23.5 1609459200000000000

-- Select data
SELECT value FROM temperature 
WHERE location = 'office' 
AND time >= '2024-01-01T00:00:00Z'

-- Aggregation
SELECT MEAN(value) FROM temperature 
WHERE time >= now() - 1h 
GROUP BY time(10m), location
```

### Time-based Functions
```sql
-- Time range queries
SELECT * FROM cpu_usage 
WHERE time >= now() - 1d

-- Downsampling
SELECT MEAN(value) FROM metrics 
WHERE time >= now() - 7d 
GROUP BY time(1h)

-- Fill missing data
SELECT MEAN(value) FROM temperature 
WHERE time >= now() - 1d 
GROUP BY time(1h) fill(linear)
```

## 📊 Advanced Features

### Continuous Queries
```sql
-- Create continuous query for downsampling
CREATE CONTINUOUS QUERY "cq_mean_temp" ON "mydb"
BEGIN
  SELECT MEAN(value) INTO "average_temp" 
  FROM "temperature" 
  GROUP BY time(1h), *
END
```

### Retention Policies
```sql
-- Create retention policy
CREATE RETENTION POLICY "one_week" ON "mydb" 
DURATION 7d REPLICATION 1 DEFAULT

-- Show retention policies
SHOW RETENTION POLICIES ON "mydb"
```

## 🚀 Performance Optimization

### Schema Design
```sql
-- Good: Use tags for metadata
measurement,host=server1,region=us-east value=100

-- Bad: Don't use high-cardinality tags
measurement,user_id=12345 value=100  -- Too many unique values
```

### Indexing Strategy
- Tags are automatically indexed
- Keep tag cardinality low (<100K unique values)
- Use fields for high-cardinality data

## 🔧 Python Integration

### Basic Operations
```python
from influxdb import InfluxDBClient

client = InfluxDBClient(host='localhost', port=8086)
client.create_database('sensors')

# Write data
json_body = [
    {
        "measurement": "temperature",
        "tags": {
            "location": "office",
            "sensor": "A001"
        },
        "fields": {
            "value": 23.5
        },
        "time": "2024-01-01T00:00:00Z"
    }
]
client.write_points(json_body)

# Query data
result = client.query('SELECT value FROM temperature LIMIT 10')
```

### Batch Writing
```python
from influxdb import InfluxDBClient
import time

def write_batch_data(client, measurements):
    points = []
    for measurement in measurements:
        point = {
            "measurement": "metrics",
            "tags": measurement['tags'],
            "fields": measurement['fields'],
            "time": int(time.time() * 1000000000)  # nanoseconds
        }
        points.append(point)
    
    client.write_points(points, time_precision='n')
```

## 🎯 Use Cases & Patterns

### IoT Data Collection
```python
# Sensor data ingestion
def ingest_sensor_data(sensor_id, location, readings):
    points = []
    for reading in readings:
        points.append({
            "measurement": "sensor_data",
            "tags": {
                "sensor_id": sensor_id,
                "location": location,
                "type": reading['type']
            },
            "fields": {
                "value": reading['value'],
                "quality": reading['quality']
            },
            "time": reading['timestamp']
        })
    client.write_points(points)
```

### Application Monitoring
```python
# Metrics collection
def log_application_metrics(app_name, metrics):
    client.write_points([{
        "measurement": "app_metrics",
        "tags": {
            "application": app_name,
            "environment": "production"
        },
        "fields": {
            "response_time": metrics['response_time'],
            "error_rate": metrics['error_rate'],
            "throughput": metrics['throughput']
        }
    }])
```

## 🔒 Best Practices

### Schema Design
- Use meaningful measurement names
- Keep tag values consistent
- Avoid high-cardinality tags
- Use appropriate data types for fields

### Performance
- Batch writes when possible
- Use appropriate retention policies
- Monitor shard duration
- Implement proper indexing strategy

### Operations
- Regular backups
- Monitor disk usage
- Configure appropriate hardware
- Use clustering for high availability

## 🎯 Common Use Cases
- IoT sensor data
- Application performance monitoring
- Infrastructure metrics
- Financial market data
- Real-time analytics
- DevOps monitoring

## ⚠️ Limitations
- Not suitable for non-time-series data
- Limited JOIN capabilities
- Memory requirements for high cardinality
- Eventual consistency in clustered setup