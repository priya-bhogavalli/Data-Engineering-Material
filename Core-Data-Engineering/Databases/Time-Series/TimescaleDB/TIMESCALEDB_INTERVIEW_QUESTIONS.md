# 📊 TimescaleDB Interview Questions & Answers

## 📋 Table of Contents
- [Basic Concepts](#basic-concepts)
- [Hypertables](#hypertables)
- [Chunks & Partitioning](#chunks--partitioning)
- [Continuous Aggregates](#continuous-aggregates)
- [Performance](#performance)
- [Operations](#operations)
- [Advanced Topics](#advanced-topics)

---

## Basic Concepts

### 1. What is TimescaleDB and how does it differ from PostgreSQL?
**Answer:**
TimescaleDB is a time-series database built as an extension to PostgreSQL.

**Key Differences:**
- **Hypertables**: Automatic partitioning for time-series data
- **Chunks**: Time-based data partitions
- **Continuous aggregates**: Materialized views for real-time analytics
- **Compression**: Native time-series compression
- **Time-series functions**: Built-in analytics functions

**Benefits:**
- Full SQL compatibility
- ACID transactions
- Rich ecosystem (PostGIS, etc.)
- Horizontal scaling (TimescaleDB 2.0+)

**Example:**
```sql
-- Regular PostgreSQL table
CREATE TABLE metrics (
    time TIMESTAMPTZ,
    device_id INTEGER,
    temperature DOUBLE PRECISION
);

-- TimescaleDB hypertable
SELECT create_hypertable('metrics', 'time');
```

### 2. What are hypertables in TimescaleDB?
**Answer:**
Hypertables are TimescaleDB's abstraction for partitioned tables optimized for time-series data.

**Characteristics:**
- **Automatic partitioning**: Based on time intervals
- **Transparent**: Appears as single table to applications
- **Scalable**: Can span multiple nodes
- **Optimized**: Time-series specific optimizations

**Creation:**
```sql
-- Create regular table first
CREATE TABLE sensor_data (
    time TIMESTAMPTZ NOT NULL,
    sensor_id INTEGER,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION
);

-- Convert to hypertable
SELECT create_hypertable('sensor_data', 'time');

-- With custom chunk interval
SELECT create_hypertable('sensor_data', 'time', chunk_time_interval => INTERVAL '1 day');
```

### 3. Explain TimescaleDB chunks and how they work.
**Answer:**
Chunks are the underlying partitions that store hypertable data.

**Chunk Properties:**
- **Time-based**: Each chunk covers specific time range
- **Automatic creation**: Created as data arrives
- **Independent**: Can be compressed, dropped, or moved independently
- **Optimized**: Indexes and constraints per chunk

**Chunk Management:**
```sql
-- View chunks
SELECT * FROM timescaledb_information.chunks 
WHERE hypertable_name = 'sensor_data';

-- Chunk details
SELECT chunk_name, range_start, range_end 
FROM timescaledb_information.chunks 
WHERE hypertable_name = 'sensor_data';

-- Drop old chunks
SELECT drop_chunks('sensor_data', INTERVAL '30 days');
```

### 4. What are continuous aggregates in TimescaleDB?
**Answer:**
Continuous aggregates are materialized views that automatically update as new data arrives.

**Purpose:**
- Pre-compute expensive aggregations
- Real-time analytics on large datasets
- Automatic refresh policies
- Query acceleration

**Example:**
```sql
-- Create continuous aggregate
CREATE MATERIALIZED VIEW hourly_avg
WITH (timescaledb.continuous) AS
SELECT 
    time_bucket('1 hour', time) AS hour,
    sensor_id,
    AVG(temperature) as avg_temp,
    MAX(temperature) as max_temp,
    MIN(temperature) as min_temp
FROM sensor_data
GROUP BY hour, sensor_id;

-- Add refresh policy
SELECT add_continuous_aggregate_policy('hourly_avg',
    start_offset => INTERVAL '1 day',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '30 minutes');
```

### 5. How does TimescaleDB handle compression?
**Answer:**
TimescaleDB provides native compression optimized for time-series data.

**Compression Features:**
- **Columnar storage**: Better compression ratios
- **Automatic**: Policy-based compression
- **Transparent**: No query changes needed
- **Selective**: Compress old data, keep recent data uncompressed

**Setup:**
```sql
-- Enable compression
ALTER TABLE sensor_data SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'sensor_id',
    timescaledb.compress_orderby = 'time DESC'
);

-- Add compression policy
SELECT add_compression_policy('sensor_data', INTERVAL '7 days');

-- Manual compression
SELECT compress_chunk(chunk_name) 
FROM timescaledb_information.chunks 
WHERE hypertable_name = 'sensor_data' 
AND NOT is_compressed;
```

---

## Hypertables

### 6. How do you design an optimal hypertable schema?
**Answer:**
**Design Principles:**

**1. Time Column:**
```sql
-- Use TIMESTAMPTZ for time column
CREATE TABLE metrics (
    time TIMESTAMPTZ NOT NULL,  -- Primary time dimension
    device_id INTEGER NOT NULL,
    metric_name TEXT,
    value DOUBLE PRECISION
);
```

**2. Partitioning Strategy:**
```sql
-- Choose appropriate chunk interval
SELECT create_hypertable('metrics', 'time', 
    chunk_time_interval => INTERVAL '1 day'  -- Based on data volume
);

-- Space partitioning (optional)
SELECT create_hypertable('metrics', 'time',
    partitioning_column => 'device_id',
    number_partitions => 4
);
```

**3. Indexing:**
```sql
-- Time-based index (automatic)
-- Additional indexes for common queries
CREATE INDEX ON metrics (device_id, time DESC);
CREATE INDEX ON metrics (metric_name, time DESC);
```

### 7. What are the best practices for hypertable partitioning?
**Answer:**
**Partitioning Guidelines:**

**1. Chunk Size:**
- Target 25% of available memory per chunk
- Balance between query performance and management overhead
- Consider data retention policies

**2. Time Intervals:**
```sql
-- High-frequency data (IoT sensors)
chunk_time_interval => INTERVAL '1 hour'

-- Medium-frequency data (application metrics)  
chunk_time_interval => INTERVAL '1 day'

-- Low-frequency data (daily reports)
chunk_time_interval => INTERVAL '1 week'
```

**3. Space Partitioning:**
```sql
-- Use when you have high cardinality dimension
SELECT create_hypertable('events', 'time',
    partitioning_column => 'user_id',
    number_partitions => 8  -- Based on parallelism needs
);
```

### 8. How do you migrate existing PostgreSQL tables to hypertables?
**Answer:**
**Migration Process:**

**1. Preparation:**
```sql
-- Analyze existing table
SELECT 
    schemaname, tablename, 
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE tablename = 'existing_metrics';

-- Check data distribution
SELECT 
    date_trunc('day', created_at) as day,
    count(*) as records
FROM existing_metrics
GROUP BY day
ORDER BY day;
```

**2. Migration Steps:**
```sql
-- Method 1: In-place conversion (requires downtime)
SELECT create_hypertable('existing_metrics', 'created_at');

-- Method 2: Create new hypertable and migrate data
CREATE TABLE new_metrics (LIKE existing_metrics);
SELECT create_hypertable('new_metrics', 'created_at');

-- Migrate data in batches
INSERT INTO new_metrics 
SELECT * FROM existing_metrics 
WHERE created_at >= '2024-01-01' AND created_at < '2024-01-02';
```

**3. Validation:**
```sql
-- Verify data integrity
SELECT count(*) FROM existing_metrics;
SELECT count(*) FROM new_metrics;

-- Check chunk creation
SELECT * FROM timescaledb_information.chunks 
WHERE hypertable_name = 'new_metrics';
```

### 9. How do you handle multi-dimensional partitioning?
**Answer:**
**Multi-dimensional Setup:**
```sql
-- Create hypertable with space and time partitioning
CREATE TABLE sensor_readings (
    time TIMESTAMPTZ NOT NULL,
    sensor_id INTEGER NOT NULL,
    location_id INTEGER,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION
);

-- Partition by time and space
SELECT create_hypertable('sensor_readings', 'time',
    partitioning_column => 'sensor_id',
    number_partitions => 4,
    chunk_time_interval => INTERVAL '1 day'
);
```

**Benefits:**
- Parallel query execution
- Better data locality
- Improved compression ratios
- Easier data management

**Query Optimization:**
```sql
-- Queries benefit from partition pruning
SELECT AVG(temperature) 
FROM sensor_readings 
WHERE sensor_id = 123  -- Space partition pruning
  AND time >= NOW() - INTERVAL '1 day';  -- Time partition pruning
```

### 10. What are distributed hypertables?
**Answer:**
**Distributed Hypertables (TimescaleDB 2.0+):**
Enable horizontal scaling across multiple nodes.

**Architecture:**
- **Access Node**: Query coordinator and metadata storage
- **Data Nodes**: Store chunks and execute queries
- **Automatic sharding**: Data distributed across nodes

**Setup:**
```sql
-- Add data nodes
SELECT add_data_node('data_node_1', host => 'node1.example.com');
SELECT add_data_node('data_node_2', host => 'node2.example.com');

-- Create distributed hypertable
SELECT create_distributed_hypertable('sensor_data', 'time',
    replication_factor => 2
);

-- Check distribution
SELECT * FROM timescaledb_information.data_nodes;
```

---

## Chunks & Partitioning

### 11. How do you manage chunk lifecycle and retention?
**Answer:**
**Chunk Lifecycle Management:**

**1. Automatic Retention:**
```sql
-- Drop chunks older than 30 days
SELECT add_retention_policy('sensor_data', INTERVAL '30 days');

-- Check retention policies
SELECT * FROM timescaledb_information.jobs 
WHERE proc_name = 'policy_retention';
```

**2. Manual Chunk Management:**
```sql
-- List chunks
SELECT chunk_schema, chunk_name, range_start, range_end
FROM timescaledb_information.chunks
WHERE hypertable_name = 'sensor_data'
ORDER BY range_start;

-- Drop specific chunks
SELECT drop_chunks('sensor_data', 
    older_than => TIMESTAMP '2024-01-01'
);

-- Show chunk sizes
SELECT 
    chunk_name,
    pg_size_pretty(pg_relation_size(chunk_schema||'.'||chunk_name)) as size
FROM timescaledb_information.chunks
WHERE hypertable_name = 'sensor_data';
```

### 12. How do you optimize chunk intervals for your workload?
**Answer:**
**Chunk Interval Considerations:**

**1. Data Volume Analysis:**
```sql
-- Analyze data insertion patterns
SELECT 
    date_trunc('hour', time) as hour,
    count(*) as records,
    pg_size_pretty(sum(pg_column_size(row(sensor_data)))) as size
FROM sensor_data
WHERE time >= NOW() - INTERVAL '1 day'
GROUP BY hour
ORDER BY hour;
```

**2. Query Pattern Analysis:**
```sql
-- Common query time ranges
SELECT 
    extract(epoch from (max(time) - min(time)))/3600 as hours_span,
    count(*) as query_count
FROM query_log
GROUP BY hours_span;
```

**3. Optimal Sizing:**
```sql
-- Adjust chunk interval based on analysis
SELECT set_chunk_time_interval('sensor_data', INTERVAL '6 hours');

-- For high-volume tables
SELECT set_chunk_time_interval('high_volume_metrics', INTERVAL '1 hour');

-- For low-volume tables  
SELECT set_chunk_time_interval('daily_reports', INTERVAL '1 month');
```

### 13. How do you handle chunk exclusion and constraint exclusion?
**Answer:**
**Constraint Exclusion:**
PostgreSQL's query planner uses constraints to eliminate chunks from queries.

**Automatic Constraints:**
```sql
-- TimescaleDB automatically creates time constraints
-- Check constraints on chunks
SELECT 
    schemaname, tablename, consrc
FROM pg_constraint c
JOIN pg_class t ON c.conrelid = t.oid
JOIN pg_namespace n ON t.relnamespace = n.oid
WHERE consrc LIKE '%time%';
```

**Custom Constraints:**
```sql
-- Add custom constraints for better exclusion
ALTER TABLE sensor_data_chunk_1 
ADD CONSTRAINT sensor_data_chunk_1_sensor_id_check 
CHECK (sensor_id >= 1 AND sensor_id <= 100);

-- Verify constraint exclusion in query plans
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM sensor_data 
WHERE time >= '2024-03-01' 
  AND time < '2024-03-02'
  AND sensor_id = 50;
```

### 14. What are chunk-wise operations and when to use them?
**Answer:**
**Chunk-wise Operations:**
Operations that work on individual chunks for better performance.

**Use Cases:**
- Bulk data operations
- Maintenance tasks
- Data archival
- Performance optimization

**Examples:**
```sql
-- Reindex specific chunks
REINDEX TABLE _timescaledb_internal._hyper_1_2_chunk;

-- Analyze specific chunks
ANALYZE _timescaledb_internal._hyper_1_2_chunk;

-- Vacuum specific chunks
VACUUM _timescaledb_internal._hyper_1_2_chunk;

-- Custom chunk operations
DO $$
DECLARE
    chunk_name TEXT;
BEGIN
    FOR chunk_name IN 
        SELECT format('%I.%I', chunk_schema, chunk_name)
        FROM timescaledb_information.chunks
        WHERE hypertable_name = 'sensor_data'
        AND range_start < NOW() - INTERVAL '7 days'
    LOOP
        EXECUTE format('VACUUM ANALYZE %s', chunk_name);
    END LOOP;
END $$;
```

### 15. How do you monitor chunk health and performance?
**Answer:**
**Chunk Monitoring:**

**1. Chunk Statistics:**
```sql
-- Chunk size and row count
SELECT 
    hypertable_name,
    chunk_name,
    pg_size_pretty(total_bytes) as size,
    pg_size_pretty(index_bytes) as index_size,
    pg_size_pretty(table_bytes) as table_size,
    row_estimate
FROM timescaledb_information.chunks c
JOIN timescaledb_information.hypertables h ON c.hypertable_name = h.hypertable_name;
```

**2. Compression Status:**
```sql
-- Check compression ratios
SELECT 
    chunk_name,
    before_compression_total_bytes,
    after_compression_total_bytes,
    ROUND(
        (before_compression_total_bytes::NUMERIC - after_compression_total_bytes::NUMERIC) 
        / before_compression_total_bytes::NUMERIC * 100, 2
    ) as compression_ratio
FROM timescaledb_information.chunk_compression_stats;
```

**3. Performance Monitoring:**
```sql
-- Query performance by chunk
SELECT 
    schemaname, tablename,
    seq_scan, seq_tup_read,
    idx_scan, idx_tup_fetch,
    n_tup_ins, n_tup_upd, n_tup_del
FROM pg_stat_user_tables 
WHERE schemaname = '_timescaledb_internal';
```

---

## Continuous Aggregates

### 16. How do you design effective continuous aggregates?
**Answer:**
**Design Principles:**

**1. Identify Common Queries:**
```sql
-- Analyze query patterns
-- Common: hourly averages, daily sums, etc.

-- Create continuous aggregate for hourly metrics
CREATE MATERIALIZED VIEW hourly_sensor_avg
WITH (timescaledb.continuous) AS
SELECT 
    time_bucket('1 hour', time) AS hour,
    sensor_id,
    AVG(temperature) as avg_temp,
    MAX(temperature) as max_temp,
    MIN(temperature) as min_temp,
    COUNT(*) as sample_count
FROM sensor_data
GROUP BY hour, sensor_id;
```

**2. Hierarchical Aggregates:**
```sql
-- Daily aggregate from hourly data
CREATE MATERIALIZED VIEW daily_sensor_avg
WITH (timescaledb.continuous) AS
SELECT 
    time_bucket('1 day', hour) AS day,
    sensor_id,
    AVG(avg_temp) as daily_avg_temp,
    MAX(max_temp) as daily_max_temp,
    MIN(min_temp) as daily_min_temp,
    SUM(sample_count) as total_samples
FROM hourly_sensor_avg
GROUP BY day, sensor_id;
```

### 17. How do you manage continuous aggregate refresh policies?
**Answer:**
**Refresh Policy Management:**

**1. Add Refresh Policies:**
```sql
-- Real-time refresh (small lag)
SELECT add_continuous_aggregate_policy('hourly_sensor_avg',
    start_offset => INTERVAL '1 day',
    end_offset => INTERVAL '5 minutes',
    schedule_interval => INTERVAL '5 minutes'
);

-- Batch refresh (larger intervals)
SELECT add_continuous_aggregate_policy('daily_sensor_avg',
    start_offset => INTERVAL '7 days',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour'
);
```

**2. Monitor Refresh Jobs:**
```sql
-- Check refresh policies
SELECT * FROM timescaledb_information.continuous_aggregate_stats;

-- View job status
SELECT * FROM timescaledb_information.jobs 
WHERE proc_name = 'policy_refresh_continuous_aggregate';

-- Manual refresh
CALL refresh_continuous_aggregate('hourly_sensor_avg', 
    '2024-03-01', '2024-03-02'
);
```

### 18. What are real-time aggregates and how do they work?
**Answer:**
**Real-time Aggregates:**
Combine materialized data with real-time data for up-to-date results.

**How it Works:**
1. Query materialized portion from continuous aggregate
2. Query real-time portion from raw hypertable  
3. Combine results automatically

**Configuration:**
```sql
-- Enable real-time aggregation (default in TimescaleDB 2.0+)
CREATE MATERIALIZED VIEW sensor_hourly_rt
WITH (timescaledb.continuous, timescaledb.materialized_only=false) AS
SELECT 
    time_bucket('1 hour', time) AS hour,
    sensor_id,
    AVG(temperature) as avg_temp
FROM sensor_data
GROUP BY hour, sensor_id;

-- Query automatically includes real-time data
SELECT * FROM sensor_hourly_rt 
WHERE hour >= NOW() - INTERVAL '2 hours';
```

### 19. How do you optimize continuous aggregate performance?
**Answer:**
**Optimization Strategies:**

**1. Proper Bucketing:**
```sql
-- Choose appropriate time buckets
-- Too small: Many small chunks, overhead
-- Too large: Less granular, larger refreshes

-- Good for high-frequency data
time_bucket('5 minutes', time)

-- Good for medium-frequency data  
time_bucket('1 hour', time)
```

**2. Selective Aggregation:**
```sql
-- Include WHERE clauses to reduce data
CREATE MATERIALIZED VIEW active_sensors_hourly
WITH (timescaledb.continuous) AS
SELECT 
    time_bucket('1 hour', time) AS hour,
    sensor_id,
    AVG(temperature) as avg_temp
FROM sensor_data
WHERE sensor_status = 'active'  -- Filter during aggregation
GROUP BY hour, sensor_id;
```

**3. Indexing:**
```sql
-- Add indexes on continuous aggregates
CREATE INDEX ON sensor_hourly_rt (sensor_id, hour);
CREATE INDEX ON sensor_hourly_rt (hour) WHERE avg_temp > 30;
```

### 20. How do you handle continuous aggregate maintenance?
**Answer:**
**Maintenance Tasks:**

**1. Monitor Storage:**
```sql
-- Check continuous aggregate sizes
SELECT 
    view_name,
    pg_size_pretty(total_bytes) as total_size,
    pg_size_pretty(table_bytes) as table_size,
    pg_size_pretty(index_bytes) as index_size
FROM timescaledb_information.continuous_aggregates ca
JOIN timescaledb_information.hypertables h ON ca.materialization_hypertable_name = h.hypertable_name;
```

**2. Refresh Management:**
```sql
-- Check refresh lag
SELECT 
    view_name,
    completed_threshold,
    invalidation_threshold,
    job_status
FROM timescaledb_information.continuous_aggregate_stats;

-- Adjust refresh policies if needed
SELECT alter_job(job_id, schedule_interval => INTERVAL '10 minutes')
FROM timescaledb_information.jobs 
WHERE proc_name = 'policy_refresh_continuous_aggregate';
```

---

## Performance

### 21. How do you optimize TimescaleDB query performance?
**Answer:**
**Query Optimization Strategies:**

**1. Time-based Filtering:**
```sql
-- Always include time bounds
SELECT AVG(temperature) 
FROM sensor_data 
WHERE time >= NOW() - INTERVAL '1 hour'  -- Essential for chunk exclusion
  AND sensor_id = 123;

-- Use appropriate time ranges
SELECT * FROM sensor_data 
WHERE time >= '2024-03-01 00:00:00'
  AND time < '2024-03-02 00:00:00';
```

**2. Proper Indexing:**
```sql
-- Time + dimension indexes
CREATE INDEX ON sensor_data (sensor_id, time DESC);
CREATE INDEX ON sensor_data (location_id, time DESC);

-- Partial indexes for common filters
CREATE INDEX ON sensor_data (time DESC) 
WHERE sensor_status = 'active';
```

**3. Use Time-series Functions:**
```sql
-- Use time_bucket for aggregations
SELECT 
    time_bucket('1 hour', time) as hour,
    AVG(temperature)
FROM sensor_data 
WHERE time >= NOW() - INTERVAL '1 day'
GROUP BY hour
ORDER BY hour;
```

### 22. How do you tune TimescaleDB configuration for performance?
**Answer:**
**Configuration Tuning:**

**1. Memory Settings:**
```sql
-- PostgreSQL settings in postgresql.conf
shared_buffers = '256MB'          -- 25% of RAM
effective_cache_size = '1GB'      -- 75% of RAM
work_mem = '4MB'                  -- Per query operation
maintenance_work_mem = '64MB'     -- For maintenance operations

-- TimescaleDB specific
timescaledb.max_background_workers = 8
```

**2. Parallel Query Settings:**
```sql
-- Enable parallel queries
max_parallel_workers_per_gather = 4
max_parallel_workers = 8
parallel_tuple_cost = 0.1
parallel_setup_cost = 1000.0
```

**3. Checkpoint and WAL:**
```sql
-- Optimize for write-heavy workloads
checkpoint_completion_target = 0.9
wal_buffers = '16MB'
checkpoint_timeout = '10min'
max_wal_size = '1GB'
```

### 23. How do you handle high-frequency data ingestion?
**Answer:**
**High-frequency Ingestion Strategies:**

**1. Batch Inserts:**
```sql
-- Use COPY for bulk inserts
COPY sensor_data(time, sensor_id, temperature, humidity) 
FROM '/path/to/data.csv' 
WITH (FORMAT csv, HEADER true);

-- Batch INSERT statements
INSERT INTO sensor_data VALUES 
    ('2024-03-01 10:00:00', 1, 25.5, 60.2),
    ('2024-03-01 10:00:01', 1, 25.6, 60.1),
    ('2024-03-01 10:00:02', 1, 25.4, 60.3);
```

**2. Connection Pooling:**
```python
# Use connection pooling
import psycopg2.pool

pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=1, maxconn=20,
    host='localhost', database='timeseries'
)

def insert_batch(data_batch):
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO sensor_data VALUES (%s, %s, %s, %s)",
                data_batch
            )
        conn.commit()
    finally:
        pool.putconn(conn)
```

**3. Asynchronous Processing:**
```python
# Async inserts with asyncpg
import asyncio
import asyncpg

async def insert_data_async(data):
    conn = await asyncpg.connect('postgresql://user:pass@localhost/db')
    
    await conn.executemany(
        "INSERT INTO sensor_data VALUES ($1, $2, $3, $4)",
        data
    )
    
    await conn.close()
```

### 24. How do you optimize TimescaleDB for analytical queries?
**Answer:**
**Analytical Query Optimization:**

**1. Use Continuous Aggregates:**
```sql
-- Pre-compute common aggregations
CREATE MATERIALIZED VIEW sensor_analytics
WITH (timescaledb.continuous) AS
SELECT 
    time_bucket('1 hour', time) AS hour,
    sensor_id,
    AVG(temperature) as avg_temp,
    STDDEV(temperature) as stddev_temp,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY temperature) as p95_temp
FROM sensor_data
GROUP BY hour, sensor_id;
```

**2. Compression for Historical Data:**
```sql
-- Compress old data for better scan performance
ALTER TABLE sensor_data SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'sensor_id',
    timescaledb.compress_orderby = 'time DESC'
);

SELECT add_compression_policy('sensor_data', INTERVAL '7 days');
```

**3. Parallel Processing:**
```sql
-- Enable parallel aggregation
SET max_parallel_workers_per_gather = 4;

-- Use parallel-friendly queries
SELECT 
    sensor_id,
    COUNT(*) as readings,
    AVG(temperature) as avg_temp
FROM sensor_data 
WHERE time >= NOW() - INTERVAL '1 month'
GROUP BY sensor_id;
```

### 25. What are TimescaleDB-specific performance monitoring techniques?
**Answer:**
**Performance Monitoring:**

**1. Chunk Statistics:**
```sql
-- Monitor chunk access patterns
SELECT 
    schemaname, tablename,
    seq_scan, seq_tup_read,
    idx_scan, idx_tup_fetch,
    n_tup_ins, n_tup_upd
FROM pg_stat_user_tables 
WHERE schemaname = '_timescaledb_internal'
ORDER BY seq_tup_read DESC;
```

**2. Query Performance:**
```sql
-- Enable query logging
-- In postgresql.conf:
-- log_statement = 'all'
-- log_min_duration_statement = 1000

-- Analyze slow queries
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements 
WHERE query LIKE '%sensor_data%'
ORDER BY total_time DESC;
```

**3. TimescaleDB Metrics:**
```sql
-- Check compression ratios
SELECT 
    hypertable_name,
    SUM(before_compression_total_bytes) as before_bytes,
    SUM(after_compression_total_bytes) as after_bytes,
    ROUND(
        (1 - SUM(after_compression_total_bytes)::NUMERIC / 
         SUM(before_compression_total_bytes)::NUMERIC) * 100, 2
    ) as compression_ratio
FROM timescaledb_information.chunk_compression_stats
GROUP BY hypertable_name;
```

---

## Operations

### 26. How do you backup and restore TimescaleDB?
**Answer:**
**Backup Strategies:**

**1. Full Database Backup:**
```bash
# Standard PostgreSQL backup
pg_dump -h localhost -U postgres -d timeseries > backup.sql

# Compressed backup
pg_dump -h localhost -U postgres -d timeseries | gzip > backup.sql.gz

# Custom format (faster restore)
pg_dump -h localhost -U postgres -Fc -d timeseries > backup.dump
```

**2. Selective Backup:**
```bash
# Backup specific hypertable
pg_dump -h localhost -U postgres -d timeseries -t sensor_data > sensor_backup.sql

# Backup with time range (using WHERE clause in custom script)
psql -d timeseries -c "
COPY (
    SELECT * FROM sensor_data 
    WHERE time >= '2024-01-01' AND time < '2024-02-01'
) TO '/backup/sensor_jan_2024.csv' WITH CSV HEADER;
"
```

**3. Continuous Backup:**
```bash
# Enable WAL archiving in postgresql.conf
archive_mode = on
archive_command = 'cp %p /backup/wal/%f'

# Base backup
pg_basebackup -h localhost -U postgres -D /backup/base -Ft -z -P
```

**Restore Process:**
```bash
# Create new database
createdb -h localhost -U postgres timeseries_restored

# Restore from backup
pg_restore -h localhost -U postgres -d timeseries_restored backup.dump

# Or from SQL dump
psql -h localhost -U postgres -d timeseries_restored < backup.sql
```

### 27. How do you upgrade TimescaleDB versions?
**Answer:**
**Upgrade Process:**

**1. Pre-upgrade Steps:**
```sql
-- Check current version
SELECT * FROM timescaledb_information.license;

-- Backup database
-- Test upgrade in staging environment
-- Review release notes
```

**2. Upgrade Steps:**
```bash
# Update TimescaleDB package
sudo apt-get update
sudo apt-get install timescaledb-2-postgresql-14

# Connect to database and upgrade
psql -d timeseries -c "ALTER EXTENSION timescaledb UPDATE;"

# Update TimescaleDB toolkit (if used)
psql -d timeseries -c "ALTER EXTENSION timescaledb_toolkit UPDATE;"
```

**3. Post-upgrade Verification:**
```sql
-- Verify version
SELECT * FROM timescaledb_information.license;

-- Check hypertables
SELECT * FROM timescaledb_information.hypertables;

-- Test basic operations
INSERT INTO sensor_data VALUES (NOW(), 1, 25.0, 60.0);
SELECT * FROM sensor_data ORDER BY time DESC LIMIT 1;
```

### 28. How do you implement TimescaleDB security?
**Answer:**
**Security Implementation:**

**1. Authentication:**
```sql
-- Create users with specific privileges
CREATE USER app_user WITH PASSWORD 'secure_password';
CREATE USER readonly_user WITH PASSWORD 'readonly_password';

-- Grant hypertable permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON sensor_data TO app_user;
GRANT SELECT ON sensor_data TO readonly_user;

-- Grant usage on schema
GRANT USAGE ON SCHEMA public TO app_user, readonly_user;
```

**2. Row Level Security:**
```sql
-- Enable RLS
ALTER TABLE sensor_data ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY sensor_isolation ON sensor_data
    FOR ALL TO app_user
    USING (sensor_id IN (
        SELECT sensor_id FROM user_sensors 
        WHERE user_name = current_user
    ));
```

**3. SSL/TLS Configuration:**
```bash
# In postgresql.conf
ssl = on
ssl_cert_file = '/path/to/server.crt'
ssl_key_file = '/path/to/server.key'
ssl_ca_file = '/path/to/ca.crt'

# Require SSL in pg_hba.conf
hostssl all all 0.0.0.0/0 md5
```

### 29. How do you monitor TimescaleDB in production?
**Answer:**
**Production Monitoring:**

**1. Database Metrics:**
```sql
-- Connection monitoring
SELECT 
    datname,
    numbackends,
    xact_commit,
    xact_rollback,
    blks_read,
    blks_hit
FROM pg_stat_database;

-- Lock monitoring
SELECT 
    mode,
    locktype,
    granted,
    count(*)
FROM pg_locks
GROUP BY mode, locktype, granted;
```

**2. TimescaleDB Specific:**
```sql
-- Hypertable statistics
SELECT 
    hypertable_name,
    num_chunks,
    table_bytes,
    index_bytes,
    total_bytes
FROM timescaledb_information.hypertables h
JOIN timescaledb_information.hypertable_detailed_size(h.hypertable_name) s ON true;

-- Job monitoring
SELECT 
    job_id,
    application_name,
    proc_name,
    last_run_status,
    next_start
FROM timescaledb_information.jobs;
```

**3. External Monitoring:**
```yaml
# Prometheus configuration
- job_name: 'timescaledb'
  static_configs:
    - targets: ['localhost:9187']
  metrics_path: /metrics
```

### 30. How do you troubleshoot TimescaleDB performance issues?
**Answer:**
**Troubleshooting Steps:**

**1. Identify Bottlenecks:**
```sql
-- Check slow queries
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    stddev_time
FROM pg_stat_statements 
ORDER BY total_time DESC 
LIMIT 10;

-- Check I/O statistics
SELECT 
    schemaname,
    tablename,
    heap_blks_read,
    heap_blks_hit,
    idx_blks_read,
    idx_blks_hit
FROM pg_statio_user_tables;
```

**2. Analyze Query Plans:**
```sql
-- Use EXPLAIN ANALYZE for problematic queries
EXPLAIN (ANALYZE, BUFFERS, VERBOSE) 
SELECT AVG(temperature) 
FROM sensor_data 
WHERE time >= NOW() - INTERVAL '1 day'
  AND sensor_id = 123;
```

**3. System-level Monitoring:**
```bash
# Check system resources
top -p $(pgrep postgres)
iostat -x 1
free -h

# Check PostgreSQL logs
tail -f /var/log/postgresql/postgresql-14-main.log
```

---

## Advanced Topics

### 31. How do you implement custom aggregates in TimescaleDB?
**Answer:**
**Custom Aggregate Functions:**

**1. Create Aggregate Function:**
```sql
-- Create state transition function
CREATE OR REPLACE FUNCTION weighted_avg_state(
    state NUMERIC[],
    value NUMERIC,
    weight NUMERIC
) RETURNS NUMERIC[] AS $$
BEGIN
    IF state IS NULL THEN
        RETURN ARRAY[value * weight, weight];
    ELSE
        RETURN ARRAY[state[1] + (value * weight), state[2] + weight];
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Create final function
CREATE OR REPLACE FUNCTION weighted_avg_final(state NUMERIC[])
RETURNS NUMERIC AS $$
BEGIN
    IF state[2] = 0 THEN
        RETURN NULL;
    ELSE
        RETURN state[1] / state[2];
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Create aggregate
CREATE AGGREGATE weighted_avg(NUMERIC, NUMERIC) (
    SFUNC = weighted_avg_state,
    STYPE = NUMERIC[],
    FINALFUNC = weighted_avg_final,
    INITCOND = NULL
);
```

**2. Use in Continuous Aggregates:**
```sql
CREATE MATERIALIZED VIEW sensor_weighted_avg
WITH (timescaledb.continuous) AS
SELECT 
    time_bucket('1 hour', time) AS hour,
    sensor_id,
    weighted_avg(temperature, reliability_score) as weighted_temp
FROM sensor_data
GROUP BY hour, sensor_id;
```

### 32. How do you integrate TimescaleDB with other systems?
**Answer:**
**Integration Patterns:**

**1. Kafka Integration:**
```python
# Kafka consumer to TimescaleDB
from kafka import KafkaConsumer
import psycopg2
import json

consumer = KafkaConsumer('sensor_data', 
                        bootstrap_servers=['localhost:9092'])

conn = psycopg2.connect("host=localhost dbname=timeseries")
cur = conn.cursor()

for message in consumer:
    data = json.loads(message.value)
    
    cur.execute("""
        INSERT INTO sensor_data (time, sensor_id, temperature, humidity)
        VALUES (%s, %s, %s, %s)
    """, (data['timestamp'], data['sensor_id'], 
          data['temperature'], data['humidity']))
    
    conn.commit()
```

**2. Grafana Integration:**
```json
{
  "datasource": {
    "type": "postgres",
    "url": "localhost:5432",
    "database": "timeseries",
    "user": "grafana_user"
  },
  "queries": [
    {
      "rawSql": "SELECT time_bucket('5m', time) as time, AVG(temperature) FROM sensor_data WHERE $__timeFilter(time) GROUP BY 1 ORDER BY 1"
    }
  ]
}
```

### 33. How do you implement data tiering with TimescaleDB?
**Answer:**
**Data Tiering Strategy:**

**1. Automatic Tiering:**
```sql
-- Hot tier: Recent uncompressed data
-- Warm tier: Compressed data
-- Cold tier: Archived to object storage

-- Set up compression for warm tier
ALTER TABLE sensor_data SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'sensor_id'
);

SELECT add_compression_policy('sensor_data', INTERVAL '7 days');
```

**2. Cold Storage Integration:**
```sql
-- Create foreign table for cold storage
CREATE EXTENSION postgres_fdw;

CREATE SERVER s3_server 
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host 's3-compatible-endpoint', dbname 'cold_storage');

CREATE FOREIGN TABLE sensor_data_cold (
    time TIMESTAMPTZ,
    sensor_id INTEGER,
    temperature DOUBLE PRECISION
) SERVER s3_server;

-- Archive old data
INSERT INTO sensor_data_cold 
SELECT * FROM sensor_data 
WHERE time < NOW() - INTERVAL '1 year';

-- Drop old chunks
SELECT drop_chunks('sensor_data', INTERVAL '1 year');
```

### 34. How do you implement multi-tenancy in TimescaleDB?
**Answer:**
**Multi-tenancy Approaches:**

**1. Schema-based Tenancy:**
```sql
-- Create schema per tenant
CREATE SCHEMA tenant_1;
CREATE SCHEMA tenant_2;

-- Create hypertables in tenant schemas
CREATE TABLE tenant_1.sensor_data (
    time TIMESTAMPTZ NOT NULL,
    sensor_id INTEGER,
    temperature DOUBLE PRECISION
);

SELECT create_hypertable('tenant_1.sensor_data', 'time');
```

**2. Row-level Tenancy:**
```sql
-- Single table with tenant_id
CREATE TABLE multi_tenant_data (
    time TIMESTAMPTZ NOT NULL,
    tenant_id INTEGER NOT NULL,
    sensor_id INTEGER,
    temperature DOUBLE PRECISION
);

-- Partition by tenant_id and time
SELECT create_hypertable('multi_tenant_data', 'time',
    partitioning_column => 'tenant_id',
    number_partitions => 4
);

-- Row Level Security
ALTER TABLE multi_tenant_data ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON multi_tenant_data
    FOR ALL TO app_user
    USING (tenant_id = current_setting('app.tenant_id')::INTEGER);
```

### 35. What are TimescaleDB 2.0+ new features and improvements?
**Answer:**
**TimescaleDB 2.0+ Features:**

**1. Distributed Hypertables:**
- Multi-node scaling
- Automatic data distribution
- Query parallelization across nodes

**2. Improved Continuous Aggregates:**
- Real-time aggregation
- Hierarchical continuous aggregates
- Better refresh policies

**3. Enhanced Compression:**
- Better compression algorithms
- Faster decompression
- Selective column compression

**4. Advanced Analytics:**
```sql
-- Time-weighted averages
SELECT time_weight('LOCF', time, temperature) 
FROM sensor_data;

-- Gap filling
SELECT time_bucket_gapfill('1 hour', time),
       interpolate(AVG(temperature))
FROM sensor_data 
GROUP BY 1;

-- Percentile approximation
SELECT approx_percentile(0.95, temperature) 
FROM sensor_data;
```

**5. Improved Tooling:**
- Better monitoring views
- Enhanced job scheduling
- Improved backup/restore tools

---

*This comprehensive guide covers 35+ essential TimescaleDB interview questions with detailed answers and practical examples for data engineering interviews.*