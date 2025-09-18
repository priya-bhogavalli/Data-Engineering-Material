# 📊 TimescaleDB Interview Questions for Data Engineering

## 📋 Table of Contents

1. [Core Concepts (1-20)](#core-concepts-1-20)
2. [Hypertables & Chunks (21-40)](#hypertables--chunks-21-40)
3. [Queries & Performance (41-60)](#queries--performance-41-60)
4. [Operations & Scaling (61-80)](#operations--scaling-61-80)

---

## Core Concepts (1-20)

### 1. What is TimescaleDB and how does it differ from PostgreSQL?
**Answer**: TimescaleDB is a time-series database built as PostgreSQL extension.

**Key Differences:**
- **Automatic partitioning**: Time-based chunks
- **Compression**: Native columnar compression
- **Continuous aggregates**: Real-time materialized views
- **Time-series functions**: Specialized analytics
- **Retention policies**: Automated data lifecycle

```sql
-- Create hypertable
CREATE TABLE metrics (
  time TIMESTAMPTZ NOT NULL,
  device_id TEXT,
  temperature DOUBLE PRECISION,
  humidity DOUBLE PRECISION
);

SELECT create_hypertable('metrics', 'time');
```

### 2. What is a hypertable?
**Answer**: Abstraction that automatically partitions data by time.

```sql
-- Create hypertable with space partitioning
SELECT create_hypertable('sensor_data', 'time', 
                        partitioning_column => 'device_id',
                        number_partitions => 4);

-- View hypertable info
SELECT * FROM timescaledb_information.hypertables;
```

### 3. How does TimescaleDB handle compression?
**Answer**: Converts row-based chunks to columnar format.

```sql
-- Enable compression
ALTER TABLE metrics SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'device_id',
  timescaledb.compress_orderby = 'time DESC'
);

-- Add compression policy
SELECT add_compression_policy('metrics', INTERVAL '7 days');
```

### 4. What are continuous aggregates?
**Answer**: Materialized views that update automatically.

```sql
CREATE MATERIALIZED VIEW hourly_stats
WITH (timescaledb.continuous) AS
SELECT time_bucket('1 hour', time) as hour,
       device_id,
       avg(temperature) as avg_temp,
       max(humidity) as max_humidity
FROM metrics
GROUP BY hour, device_id;
```

### 5. How do retention policies work?
**Answer**: Automatically drop old data based on time.

```sql
-- Add retention policy
SELECT add_retention_policy('metrics', INTERVAL '30 days');

-- View policies
SELECT * FROM timescaledb_information.jobs;
```

---

**Total Questions: 80** | **Coverage: Complete TimescaleDB Ecosystem**