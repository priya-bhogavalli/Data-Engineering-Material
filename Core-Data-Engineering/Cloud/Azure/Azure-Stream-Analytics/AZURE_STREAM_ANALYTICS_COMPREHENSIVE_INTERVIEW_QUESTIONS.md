# Azure Stream Analytics - Comprehensive Interview Questions

## Table of Contents
1. [Core Concepts](#core-concepts)
2. [Query Language & Syntax](#query-language--syntax)
3. [Input & Output Configuration](#input--output-configuration)
4. [Windowing & Temporal Operations](#windowing--temporal-operations)
5. [Scaling & Performance](#scaling--performance)
6. [Monitoring & Troubleshooting](#monitoring--troubleshooting)
7. [Integration & Deployment](#integration--deployment)
8. [Real-World Scenarios](#real-world-scenarios)

---

## Core Concepts

### 1. What is Azure Stream Analytics and how does it differ from other stream processing platforms?

**Answer:**
Azure Stream Analytics (ASA) is a fully managed, serverless stream processing service for real-time analytics on Azure.

**Key Differentiators:**
- **SQL-based**: Uses familiar SQL syntax for stream processing
- **Serverless**: No infrastructure management required
- **Real-time**: Sub-second latency for streaming analytics
- **Integrated**: Native integration with Azure services
- **Scalable**: Automatic scaling based on workload

**Comparison:**
```
Traditional Stream Processing (Spark, Flink):
- Complex programming models (Java, Scala, Python)
- Cluster management required
- Custom windowing and state management

Azure Stream Analytics:
- SQL-based queries
- Fully managed service
- Built-in windowing functions
- Automatic scaling and fault tolerance
```

### 2. Explain the architecture and components of Azure Stream Analytics.

**Answer:**
**Core Components:**

1. **Inputs**: Data sources (Event Hubs, IoT Hub, Blob Storage)
2. **Query**: SQL-like transformation logic
3. **Outputs**: Destinations (SQL Database, Cosmos DB, Power BI)
4. **Functions**: User-defined functions for custom logic
5. **Job**: Complete streaming application

**Architecture Flow:**
```
Data Sources → Inputs → Query Engine → Outputs → Destinations
     ↓           ↓          ↓            ↓         ↓
Event Hubs → Stream → SQL Query → Results → Power BI
IoT Hub    → Data   → Processing → Stream  → SQL DB
Blob Store                                  → Cosmos DB
```

**Job Configuration:**
```sql
-- Input definition
CREATE INPUT EventHubInput
FROM EventHub
WITH (
    EventHubName = 'telemetry-hub',
    SharedAccessPolicyName = 'StreamAnalyticsPolicy',
    SharedAccessPolicyKey = 'your-key-here',
    ConsumerGroupName = 'streamanalytics'
);

-- Output definition  
CREATE OUTPUT SqlOutput
TO SqlDatabase
WITH (
    Server = 'myserver.database.windows.net',
    Database = 'analytics',
    Table = 'real_time_metrics',
    User = 'streamuser',
    Password = 'password'
);
```

### 3. What are the different input types supported by Azure Stream Analytics?

**Answer:**
**Streaming Inputs:**
1. **Azure Event Hubs**: High-throughput event ingestion
2. **Azure IoT Hub**: IoT device telemetry
3. **Azure Blob Storage**: File-based streaming data

**Reference Inputs:**
1. **Azure Blob Storage**: Static reference data
2. **Azure SQL Database**: Lookup tables and dimensions

**Input Configuration Examples:**
```sql
-- Event Hub streaming input
CREATE INPUT TelemetryStream
FROM EventHub
WITH (
    EventHubName = 'device-telemetry',
    SharedAccessPolicyName = 'ListenPolicy',
    SharedAccessPolicyKey = 'key',
    ConsumerGroupName = '$Default',
    EventSerializationFormat = 'JSON',
    Encoding = 'UTF8'
);

-- IoT Hub input
CREATE INPUT IoTDevices  
FROM IoTHub
WITH (
    IoTHubName = 'production-iot-hub',
    SharedAccessPolicyName = 'iothubowner',
    SharedAccessPolicyKey = 'key',
    ConsumerGroupName = 'streamanalytics',
    EventSerializationFormat = 'JSON'
);

-- Reference data from Blob Storage
CREATE INPUT DeviceMetadata
FROM BlobStorage
WITH (
    StorageAccount = 'mystorageaccount',
    StorageAccountKey = 'key',
    Container = 'reference-data',
    PathPattern = 'devices/{date}/devices.json',
    DateFormat = 'yyyy/MM/dd',
    EventSerializationFormat = 'JSON'
);
```

### 4. How do you handle different data formats in Azure Stream Analytics?

**Answer:**
**Supported Formats:**
- **JSON**: Most common format for streaming data
- **CSV**: Comma-separated values
- **Avro**: Binary serialization format

**Format Handling:**
```sql
-- JSON input with nested structure
SELECT 
    DeviceId,
    Temperature,
    Humidity,
    Location.Latitude,
    Location.Longitude,
    System.Timestamp AS EventTime
FROM TelemetryStream
WHERE Temperature > 25.0;

-- CSV input with custom delimiter
CREATE INPUT CsvStream
FROM BlobStorage  
WITH (
    EventSerializationFormat = 'CSV',
    FieldDelimiter = '|',
    Encoding = 'UTF8'
);

-- Avro input
CREATE INPUT AvroStream
FROM EventHub
WITH (
    EventSerializationFormat = 'Avro'
);

-- Handling malformed JSON
SELECT 
    DeviceId,
    TRY_CAST(Temperature AS FLOAT) AS Temperature,
    CASE 
        WHEN TRY_CAST(Temperature AS FLOAT) IS NULL 
        THEN 'Invalid Temperature'
        ELSE 'Valid'
    END AS DataQuality
FROM TelemetryStream;
```

---

## Query Language & Syntax

### 5. Explain the key SQL constructs used in Azure Stream Analytics queries.

**Answer:**
**Core SQL Constructs:**

1. **SELECT**: Project columns and expressions
2. **FROM**: Specify input streams
3. **WHERE**: Filter conditions
4. **GROUP BY**: Aggregate data
5. **HAVING**: Filter aggregated results
6. **JOIN**: Combine multiple streams
7. **UNION**: Combine result sets

**Basic Query Structure:**
```sql
-- Basic aggregation query
SELECT 
    DeviceId,
    AVG(Temperature) AS AvgTemperature,
    MAX(Temperature) AS MaxTemperature,
    COUNT(*) AS EventCount,
    System.Timestamp AS WindowEnd
FROM TelemetryStream TIMESTAMP BY EventTime
GROUP BY DeviceId, TumblingWindow(minute, 5)
HAVING AVG(Temperature) > 30;

-- Stream joining
SELECT 
    t.DeviceId,
    t.Temperature,
    d.DeviceType,
    d.Location
FROM TelemetryStream t TIMESTAMP BY EventTime
JOIN DeviceMetadata d
ON t.DeviceId = d.DeviceId;

-- Complex filtering and transformation
SELECT 
    DeviceId,
    Temperature,
    CASE 
        WHEN Temperature > 40 THEN 'Critical'
        WHEN Temperature > 30 THEN 'Warning'
        ELSE 'Normal'
    END AS AlertLevel,
    LAG(Temperature, 1) OVER (PARTITION BY DeviceId LIMIT DURATION(hour, 1)) AS PreviousTemp
FROM TelemetryStream TIMESTAMP BY EventTime
WHERE Temperature IS NOT NULL;
```

### 6. How do you implement user-defined functions in Azure Stream Analytics?

**Answer:**
**Types of UDFs:**
1. **JavaScript UDFs**: Custom scalar functions
2. **JavaScript UDAs**: User-defined aggregates
3. **Azure Machine Learning**: ML model integration

**JavaScript UDF Example:**
```javascript
// JavaScript UDF for temperature conversion
function celsiusToFahrenheit(celsius) {
    if (celsius === null || celsius === undefined) {
        return null;
    }
    return (celsius * 9/5) + 32;
}

// Complex data validation UDF
function validateSensorReading(temperature, humidity, pressure) {
    var result = {
        isValid: true,
        errors: []
    };
    
    if (temperature < -50 || temperature > 100) {
        result.isValid = false;
        result.errors.push("Temperature out of range");
    }
    
    if (humidity < 0 || humidity > 100) {
        result.isValid = false;
        result.errors.push("Humidity out of range");
    }
    
    if (pressure < 800 || pressure > 1200) {
        result.isValid = false;
        result.errors.push("Pressure out of range");
    }
    
    return result;
}
```

**Using UDFs in Queries:**
```sql
-- Using temperature conversion UDF
SELECT 
    DeviceId,
    Temperature AS CelsiusTemp,
    udf.celsiusToFahrenheit(Temperature) AS FahrenheitTemp,
    System.Timestamp AS EventTime
FROM TelemetryStream TIMESTAMP BY EventTime;

-- Using validation UDF
SELECT 
    DeviceId,
    Temperature,
    Humidity,
    Pressure,
    udf.validateSensorReading(Temperature, Humidity, Pressure) AS ValidationResult
FROM TelemetryStream TIMESTAMP BY EventTime
WHERE udf.validateSensorReading(Temperature, Humidity, Pressure).isValid = true;
```

---

## Windowing & Temporal Operations

### 7. Explain the different types of windows in Azure Stream Analytics.

**Answer:**
**Window Types:**

1. **Tumbling Window**: Non-overlapping, fixed-size windows
2. **Hopping Window**: Overlapping, fixed-size windows
3. **Sliding Window**: Event-driven windows
4. **Session Window**: Activity-based windows

**Window Implementations:**
```sql
-- Tumbling Window - 5 minute non-overlapping windows
SELECT 
    DeviceId,
    AVG(Temperature) AS AvgTemp,
    System.Timestamp AS WindowEnd
FROM TelemetryStream TIMESTAMP BY EventTime
GROUP BY DeviceId, TumblingWindow(minute, 5);

-- Hopping Window - 10 minute windows every 5 minutes
SELECT 
    DeviceId,
    AVG(Temperature) AS AvgTemp,
    System.Timestamp AS WindowEnd
FROM TelemetryStream TIMESTAMP BY EventTime  
GROUP BY DeviceId, HoppingWindow(minute, 10, 5);

-- Sliding Window - 1 hour window, triggered by each event
SELECT 
    DeviceId,
    AVG(Temperature) AS AvgTemp,
    System.Timestamp AS WindowEnd
FROM TelemetryStream TIMESTAMP BY EventTime
GROUP BY DeviceId, SlidingWindow(hour, 1);

-- Session Window - based on 30 minute inactivity
SELECT 
    DeviceId,
    COUNT(*) AS EventCount,
    MIN(EventTime) AS SessionStart,
    MAX(EventTime) AS SessionEnd
FROM TelemetryStream TIMESTAMP BY EventTime
GROUP BY DeviceId, SessionWindow(minute, 30);
```

### 8. How do you handle late-arriving events and out-of-order data?

**Answer:**
**Late Arrival Policies:**
1. **Arrival Time**: Use arrival time for processing
2. **Application Time**: Use event timestamp
3. **Late Arrival Tolerance**: Accept events within tolerance window
4. **Out-of-Order Tolerance**: Handle out-of-order events

**Configuration:**
```sql
-- Configure event ordering policy
ALTER JOB SET EventOrderingPolicy = 'Adjust';
ALTER JOB SET EventOrderingMaxDelay = '00:05:00';  -- 5 minutes
ALTER JOB SET LateArrivalMaxDelay = '00:10:00';    -- 10 minutes

-- Query with timestamp handling
SELECT 
    DeviceId,
    Temperature,
    EventTime,
    System.Timestamp AS ProcessingTime,
    DATEDIFF(second, EventTime, System.Timestamp) AS ProcessingDelay
FROM TelemetryStream TIMESTAMP BY EventTime
WHERE DATEDIFF(second, EventTime, System.Timestamp) < 300;  -- Within 5 minutes

-- Handling late events with separate output
SELECT 
    DeviceId,
    Temperature,
    EventTime,
    'OnTime' AS EventCategory
FROM TelemetryStream TIMESTAMP BY EventTime
WHERE DATEDIFF(second, EventTime, System.Timestamp) <= 60

UNION ALL

SELECT 
    DeviceId,
    Temperature, 
    EventTime,
    'Late' AS EventCategory
FROM TelemetryStream TIMESTAMP BY EventTime
WHERE DATEDIFF(second, EventTime, System.Timestamp) > 60;
```

### 9. How do you implement anomaly detection in Azure Stream Analytics?

**Answer:**
**Anomaly Detection Methods:**
1. **Built-in ML Functions**: AnomalyDetection_SpikeAndDip, AnomalyDetection_ChangePoint
2. **Statistical Methods**: Standard deviation, percentiles
3. **Custom Logic**: Business rule-based detection

**Implementation:**
```sql
-- Spike and Dip Detection
WITH AnomalyDetectionStep AS (
    SELECT
        DeviceId,
        Temperature,
        EventTime,
        AnomalyDetection_SpikeAndDip(Temperature, 95, 120, 'spikesanddips')
            OVER(PARTITION BY DeviceId LIMIT DURATION(hour, 2)) AS SpikeAndDipScores
    FROM TelemetryStream TIMESTAMP BY EventTime
)
SELECT
    DeviceId,
    Temperature,
    EventTime,
    CAST(GetRecordPropertyValue(SpikeAndDipScores, 'Score') AS FLOAT) AS Score,
    CAST(GetRecordPropertyValue(SpikeAndDipScores, 'IsAnomaly') AS BIGINT) AS IsAnomaly
FROM AnomalyDetectionStep
WHERE CAST(GetRecordPropertyValue(SpikeAndDipScores, 'IsAnomaly') AS BIGINT) = 1;

-- Change Point Detection
WITH ChangePointDetectionStep AS (
    SELECT
        DeviceId,
        Temperature,
        EventTime,
        AnomalyDetection_ChangePoint(Temperature, 80, 120) 
            OVER(PARTITION BY DeviceId LIMIT DURATION(hour, 2)) AS ChangePointScores
    FROM TelemetryStream TIMESTAMP BY EventTime
)
SELECT
    DeviceId,
    Temperature,
    EventTime,
    CAST(GetRecordPropertyValue(ChangePointScores, 'Score') AS FLOAT) AS Score,
    CAST(GetRecordPropertyValue(ChangePointScores, 'IsChangePoint') AS BIGINT) AS IsChangePoint
FROM ChangePointDetectionStep
WHERE CAST(GetRecordPropertyValue(ChangePointScores, 'IsChangePoint') AS BIGINT) = 1;

-- Custom anomaly detection using statistical methods
WITH StatsWindow AS (
    SELECT 
        DeviceId,
        Temperature,
        AVG(Temperature) OVER(PARTITION BY DeviceId LIMIT DURATION(hour, 1)) AS AvgTemp,
        STDEV(Temperature) OVER(PARTITION BY DeviceId LIMIT DURATION(hour, 1)) AS StdDevTemp,
        EventTime
    FROM TelemetryStream TIMESTAMP BY EventTime
)
SELECT 
    DeviceId,
    Temperature,
    AvgTemp,
    StdDevTemp,
    EventTime,
    CASE 
        WHEN ABS(Temperature - AvgTemp) > (2 * StdDevTemp) THEN 1
        ELSE 0
    END AS IsAnomaly
FROM StatsWindow
WHERE ABS(Temperature - AvgTemp) > (2 * StdDevTemp);
```

---

## Scaling & Performance

### 10. How do you scale Azure Stream Analytics jobs for high throughput?

**Answer:**
**Scaling Strategies:**

1. **Streaming Units (SUs)**: Increase compute resources
2. **Partitioning**: Distribute processing across partitions
3. **Query Optimization**: Optimize query performance
4. **Input Partitioning**: Partition input streams

**Scaling Configuration:**
```sql
-- Partition input for better parallelism
CREATE INPUT PartitionedEventHub
FROM EventHub
WITH (
    EventHubName = 'telemetry-hub',
    PartitionCount = 32,  -- Match Event Hub partitions
    ConsumerGroupName = 'streamanalytics'
);

-- Partitioned query for parallel processing
SELECT 
    DeviceId,
    AVG(Temperature) AS AvgTemp,
    System.Timestamp AS WindowEnd
FROM PartitionedEventHub PARTITION BY DeviceId TIMESTAMP BY EventTime
GROUP BY DeviceId, TumblingWindow(minute, 5);

-- Optimize with PARTITION BY
SELECT 
    DeviceType,
    COUNT(*) AS DeviceCount,
    AVG(Temperature) AS AvgTemp
FROM TelemetryStream PARTITION BY DeviceType TIMESTAMP BY EventTime
GROUP BY DeviceType, TumblingWindow(minute, 1);
```

**Performance Monitoring:**
```sql
-- Monitor processing metrics
SELECT 
    DeviceId,
    Temperature,
    EventTime,
    System.Timestamp AS ProcessingTime,
    DATEDIFF(millisecond, EventTime, System.Timestamp) AS ProcessingLatency
FROM TelemetryStream TIMESTAMP BY EventTime;
```

### 11. What are the best practices for optimizing Azure Stream Analytics queries?

**Answer:**
**Optimization Best Practices:**

1. **Use PARTITION BY**: Enable parallel processing
2. **Minimize Data Movement**: Reduce shuffling
3. **Efficient Joins**: Use reference data for lookups
4. **Window Optimization**: Choose appropriate window sizes
5. **Filter Early**: Apply WHERE clauses early

**Optimized Query Examples:**
```sql
-- Efficient partitioned aggregation
SELECT 
    DeviceId,
    AVG(Temperature) AS AvgTemp,
    COUNT(*) AS EventCount
FROM TelemetryStream PARTITION BY DeviceId TIMESTAMP BY EventTime
GROUP BY DeviceId, TumblingWindow(minute, 5)
HAVING COUNT(*) > 10;  -- Filter after aggregation

-- Optimized join with reference data
SELECT 
    t.DeviceId,
    t.Temperature,
    r.DeviceType,
    r.Location
FROM TelemetryStream t PARTITION BY DeviceId TIMESTAMP BY EventTime
JOIN DeviceReference r
ON t.DeviceId = r.DeviceId
WHERE t.Temperature > 30;  -- Filter before join

-- Avoid expensive operations in SELECT
WITH FilteredData AS (
    SELECT DeviceId, Temperature, EventTime
    FROM TelemetryStream TIMESTAMP BY EventTime
    WHERE Temperature BETWEEN 0 AND 100  -- Early filtering
)
SELECT 
    DeviceId,
    AVG(Temperature) AS AvgTemp,
    System.Timestamp AS WindowEnd
FROM FilteredData PARTITION BY DeviceId
GROUP BY DeviceId, TumblingWindow(minute, 5);
```

---

## Monitoring & Troubleshooting

### 12. How do you monitor and troubleshoot Azure Stream Analytics jobs?

**Answer:**
**Monitoring Tools:**

1. **Azure Portal**: Job metrics and monitoring
2. **Azure Monitor**: Custom metrics and alerts
3. **Activity Logs**: Job execution logs
4. **Resource Health**: Service health status

**Key Metrics to Monitor:**
```sql
-- Monitor input/output events
SELECT 
    COUNT(*) AS InputEvents,
    System.Timestamp AS WindowEnd
FROM TelemetryStream TIMESTAMP BY EventTime
GROUP BY TumblingWindow(minute, 1);

-- Monitor processing latency
SELECT 
    AVG(DATEDIFF(millisecond, EventTime, System.Timestamp)) AS AvgLatencyMs,
    MAX(DATEDIFF(millisecond, EventTime, System.Timestamp)) AS MaxLatencyMs,
    System.Timestamp AS WindowEnd
FROM TelemetryStream TIMESTAMP BY EventTime
GROUP BY TumblingWindow(minute, 1);

-- Monitor data quality
SELECT 
    COUNT(*) AS TotalEvents,
    COUNT(CASE WHEN Temperature IS NULL THEN 1 END) AS NullTemperature,
    COUNT(CASE WHEN Temperature < -50 OR Temperature > 100 THEN 1 END) AS OutOfRange,
    System.Timestamp AS WindowEnd
FROM TelemetryStream TIMESTAMP BY EventTime
GROUP BY TumblingWindow(minute, 5);
```

**Alert Configuration:**
```json
{
  "alertRule": {
    "name": "High Processing Latency",
    "description": "Alert when processing latency exceeds 30 seconds",
    "condition": {
      "metricName": "InputEventLatency",
      "operator": "GreaterThan",
      "threshold": 30000,
      "timeAggregation": "Average"
    },
    "actions": [
      {
        "actionType": "Email",
        "recipients": ["admin@company.com"]
      }
    ]
  }
}
```

### 13. What are common issues in Azure Stream Analytics and how do you resolve them?

**Answer:**
**Common Issues:**

1. **High Latency**: Processing delays
2. **Data Loss**: Missing events
3. **Memory Issues**: Out of memory errors
4. **Serialization Errors**: Data format issues
5. **Connectivity Issues**: Input/output connection problems

**Troubleshooting Solutions:**
```sql
-- Diagnose high latency
SELECT 
    DeviceId,
    EventTime,
    System.Timestamp AS ProcessingTime,
    DATEDIFF(second, EventTime, System.Timestamp) AS LatencySeconds
FROM TelemetryStream TIMESTAMP BY EventTime
WHERE DATEDIFF(second, EventTime, System.Timestamp) > 30
ORDER BY LatencySeconds DESC;

-- Handle serialization errors
SELECT 
    DeviceId,
    TRY_CAST(Temperature AS FLOAT) AS Temperature,
    CASE 
        WHEN TRY_CAST(Temperature AS FLOAT) IS NULL 
        THEN 'Serialization Error'
        ELSE 'Success'
    END AS ParseStatus
FROM TelemetryStream TIMESTAMP BY EventTime;

-- Monitor for data loss
WITH InputCount AS (
    SELECT COUNT(*) AS InputEvents
    FROM TelemetryStream TIMESTAMP BY EventTime
    GROUP BY TumblingWindow(minute, 1)
),
OutputCount AS (
    SELECT COUNT(*) AS OutputEvents  
    FROM ProcessedOutput
    GROUP BY TumblingWindow(minute, 1)
)
SELECT 
    i.InputEvents,
    o.OutputEvents,
    (i.InputEvents - o.OutputEvents) AS LostEvents
FROM InputCount i
JOIN OutputCount o ON DATEDIFF(minute, i, o) BETWEEN 0 AND 1;
```

---

## Real-World Scenarios

### 14. Design a real-time IoT monitoring solution using Azure Stream Analytics.

**Answer:**
**Architecture:**
```
IoT Devices → IoT Hub → Stream Analytics → Multiple Outputs
     ↓          ↓            ↓               ↓
Sensors → Telemetry → Processing → Power BI (Dashboard)
                                → SQL DB (Storage)
                                → Event Hub (Alerts)
                                → Cosmos DB (Archive)
```

**Implementation:**
```sql
-- Input from IoT Hub
CREATE INPUT IoTTelemetry
FROM IoTHub
WITH (
    IoTHubName = 'production-iot-hub',
    SharedAccessPolicyName = 'streamanalytics',
    SharedAccessPolicyKey = 'your-key',
    ConsumerGroupName = 'analytics'
);

-- Reference data for device metadata
CREATE INPUT DeviceMetadata
FROM BlobStorage
WITH (
    StorageAccount = 'iotmetadata',
    Container = 'devices',
    PathPattern = 'devices.json'
);

-- Real-time dashboard output
CREATE OUTPUT PowerBIDashboard
TO PowerBI
WITH (
    Dataset = 'IoTRealTimeMetrics',
    Table = 'DeviceMetrics',
    GroupId = 'your-workspace-id'
);

-- Alert output
CREATE OUTPUT AlertsOutput
TO EventHub
WITH (
    EventHubName = 'iot-alerts',
    SharedAccessPolicyName = 'SendPolicy'
);

-- Historical data storage
CREATE OUTPUT HistoricalData
TO SqlDatabase
WITH (
    Server = 'iot-analytics.database.windows.net',
    Database = 'IoTAnalytics',
    Table = 'TelemetryHistory'
);

-- Main processing query
WITH EnrichedTelemetry AS (
    SELECT 
        t.DeviceId,
        t.Temperature,
        t.Humidity,
        t.Pressure,
        t.EventTime,
        d.DeviceType,
        d.Location,
        d.CriticalTempThreshold,
        d.CriticalHumidityThreshold
    FROM IoTTelemetry t TIMESTAMP BY EventTime
    JOIN DeviceMetadata d ON t.DeviceId = d.DeviceId
),

RealTimeMetrics AS (
    SELECT 
        DeviceId,
        DeviceType,
        Location,
        AVG(Temperature) AS AvgTemperature,
        MAX(Temperature) AS MaxTemperature,
        AVG(Humidity) AS AvgHumidity,
        COUNT(*) AS EventCount,
        System.Timestamp AS WindowEnd
    FROM EnrichedTelemetry
    GROUP BY DeviceId, DeviceType, Location, TumblingWindow(minute, 1)
),

Alerts AS (
    SELECT 
        DeviceId,
        DeviceType,
        Location,
        Temperature,
        Humidity,
        CriticalTempThreshold,
        CriticalHumidityThreshold,
        EventTime,
        CASE 
            WHEN Temperature > CriticalTempThreshold THEN 'Critical Temperature'
            WHEN Humidity > CriticalHumidityThreshold THEN 'Critical Humidity'
            ELSE 'Normal'
        END AS AlertType
    FROM EnrichedTelemetry
    WHERE Temperature > CriticalTempThreshold 
       OR Humidity > CriticalHumidityThreshold
)

-- Output to Power BI for real-time dashboard
SELECT * INTO PowerBIDashboard FROM RealTimeMetrics;

-- Output alerts
SELECT * INTO AlertsOutput FROM Alerts WHERE AlertType != 'Normal';

-- Store historical data
SELECT 
    DeviceId,
    Temperature,
    Humidity,
    Pressure,
    EventTime,
    System.Timestamp AS ProcessedTime
INTO HistoricalData 
FROM EnrichedTelemetry;
```

### 15. How would you implement a fraud detection system using Azure Stream Analytics?

**Answer:**
**Fraud Detection Architecture:**
```
Transactions → Event Hub → Stream Analytics → Multiple Outputs
     ↓            ↓            ↓               ↓
Card/Online → Real-time → ML Models → Alerts (High Risk)
Payments    → Stream   → Rules     → Dashboard (Metrics)
                       → Scoring   → Database (History)
```

**Implementation:**
```sql
-- Transaction input
CREATE INPUT TransactionStream
FROM EventHub
WITH (
    EventHubName = 'payment-transactions',
    EventSerializationFormat = 'JSON'
);

-- Customer profile reference data
CREATE INPUT CustomerProfiles
FROM BlobStorage
WITH (
    Container = 'customer-data',
    PathPattern = 'profiles/{date}/profiles.json'
);

-- Fraud alerts output
CREATE OUTPUT FraudAlerts
TO EventHub
WITH (
    EventHubName = 'fraud-alerts'
);

-- Analytics dashboard
CREATE OUTPUT FraudMetrics
TO PowerBI
WITH (
    Dataset = 'FraudDetection',
    Table = 'RealTimeMetrics'
);

-- Main fraud detection query
WITH EnrichedTransactions AS (
    SELECT 
        t.TransactionId,
        t.CustomerId,
        t.Amount,
        t.MerchantId,
        t.Location,
        t.TransactionTime,
        c.AvgTransactionAmount,
        c.UsualLocations,
        c.RiskScore AS CustomerRiskScore
    FROM TransactionStream t TIMESTAMP BY TransactionTime
    JOIN CustomerProfiles c ON t.CustomerId = c.CustomerId
),

-- Velocity checks - multiple transactions in short time
VelocityChecks AS (
    SELECT 
        CustomerId,
        COUNT(*) AS TransactionCount,
        SUM(Amount) AS TotalAmount,
        System.Timestamp AS WindowEnd
    FROM EnrichedTransactions
    GROUP BY CustomerId, TumblingWindow(minute, 5)
    HAVING COUNT(*) > 10 OR SUM(Amount) > 10000
),

-- Amount anomaly detection
AmountAnomalies AS (
    SELECT 
        TransactionId,
        CustomerId,
        Amount,
        AvgTransactionAmount,
        TransactionTime,
        CASE 
            WHEN Amount > (AvgTransactionAmount * 5) THEN 'High Amount Anomaly'
            WHEN Amount > (AvgTransactionAmount * 3) THEN 'Medium Amount Anomaly'
            ELSE 'Normal'
        END AS AmountRisk
    FROM EnrichedTransactions
    WHERE Amount > (AvgTransactionAmount * 3)
),

-- Location-based fraud detection
LocationAnomalies AS (
    SELECT 
        TransactionId,
        CustomerId,
        Location,
        UsualLocations,
        TransactionTime,
        CASE 
            WHEN Location NOT IN (SELECT value FROM STRING_SPLIT(UsualLocations, ','))
            THEN 'Unusual Location'
            ELSE 'Normal Location'
        END AS LocationRisk
    FROM EnrichedTransactions
),

-- Combine all fraud indicators
FraudScoring AS (
    SELECT 
        t.TransactionId,
        t.CustomerId,
        t.Amount,
        t.Location,
        t.TransactionTime,
        COALESCE(v.TransactionCount, 0) AS VelocityCount,
        COALESCE(a.AmountRisk, 'Normal') AS AmountRisk,
        COALESCE(l.LocationRisk, 'Normal Location') AS LocationRisk,
        CASE 
            WHEN v.TransactionCount > 0 AND a.AmountRisk != 'Normal' THEN 'High Risk'
            WHEN v.TransactionCount > 0 OR a.AmountRisk != 'Normal' OR l.LocationRisk != 'Normal Location' THEN 'Medium Risk'
            ELSE 'Low Risk'
        END AS OverallRiskLevel
    FROM EnrichedTransactions t
    LEFT JOIN VelocityChecks v ON t.CustomerId = v.CustomerId 
        AND DATEDIFF(minute, t.TransactionTime, v.WindowEnd) BETWEEN 0 AND 5
    LEFT JOIN AmountAnomalies a ON t.TransactionId = a.TransactionId
    LEFT JOIN LocationAnomalies l ON t.TransactionId = l.TransactionId
)

-- Output high-risk transactions as alerts
SELECT 
    TransactionId,
    CustomerId,
    Amount,
    Location,
    OverallRiskLevel,
    AmountRisk,
    LocationRisk,
    VelocityCount,
    TransactionTime
INTO FraudAlerts 
FROM FraudScoring 
WHERE OverallRiskLevel IN ('High Risk', 'Medium Risk');

-- Output metrics for dashboard
SELECT 
    COUNT(*) AS TotalTransactions,
    COUNT(CASE WHEN OverallRiskLevel = 'High Risk' THEN 1 END) AS HighRiskCount,
    COUNT(CASE WHEN OverallRiskLevel = 'Medium Risk' THEN 1 END) AS MediumRiskCount,
    AVG(Amount) AS AvgTransactionAmount,
    System.Timestamp AS WindowEnd
INTO FraudMetrics
FROM FraudScoring
GROUP BY TumblingWindow(minute, 1);
```

This comprehensive set of Azure Stream Analytics interview questions covers all essential aspects from basic concepts to advanced real-world fraud detection and IoT monitoring scenarios, providing practical SQL-based examples for stream processing.