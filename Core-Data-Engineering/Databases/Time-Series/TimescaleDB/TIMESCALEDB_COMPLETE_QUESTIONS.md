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
### 6. What are TimescaleDB chunks?
**Answer**: Time-based partitions that store actual data.

```sql
-- View chunks
SELECT * FROM timescaledb_information.chunks;

-- Chunk statistics
SELECT 
  chunk_name,
  range_start,
  range_end,
  compressed_chunk_id
FROM timescaledb_information.chunks 
WHERE hypertable_name = 'metrics';
```

### 7. How do you query time-series data efficiently?
**Answer**: Use time-based indexes and proper WHERE clauses.

```sql
-- Efficient time-range query
SELECT * FROM metrics 
WHERE time >= NOW() - INTERVAL '1 hour'
  AND device_id = 'sensor_001';

-- Time bucketing
SELECT time_bucket('5 minutes', time) AS bucket,
       avg(temperature) AS avg_temp
FROM metrics 
WHERE time >= NOW() - INTERVAL '1 day'
GROUP BY bucket
ORDER BY bucket;
```

### 8. What is time_bucket function?
**Answer**: Groups timestamps into regular intervals.

```sql
-- 15-minute buckets
SELECT time_bucket('15 minutes', time) AS bucket,
       count(*) AS readings
FROM metrics
GROUP BY bucket;

-- Custom bucket alignment
SELECT time_bucket('1 hour', time, '2023-01-01 09:00:00') AS bucket,
       avg(temperature)
FROM metrics
GROUP BY bucket;
```

### 9. How do you handle missing data?
**Answer**: Use interpolation and gap-filling functions.

```sql
-- Linear interpolation
SELECT time_bucket_gapfill('1 hour', time) AS bucket,
       interpolate(avg(temperature)) AS temp
FROM metrics
WHERE time >= NOW() - INTERVAL '1 day'
GROUP BY bucket
ORDER BY bucket;

-- Locf (last observation carried forward)
SELECT time_bucket_gapfill('5 minutes', time) AS bucket,
       locf(avg(temperature)) AS temp
FROM metrics
GROUP BY bucket;
```

### 10. What are TimescaleDB data types?
**Answer**: Supports all PostgreSQL types plus time-series optimizations.

```sql
CREATE TABLE sensor_readings (
  time TIMESTAMPTZ NOT NULL,
  sensor_id INTEGER,
  temperature NUMERIC(5,2),
  humidity REAL,
  location POINT,
  metadata JSONB,
  tags TEXT[]
);
```

### 11. How do you implement data validation?
**Answer**: Use PostgreSQL constraints and triggers.

```sql
-- Add constraints
ALTER TABLE metrics 
ADD CONSTRAINT valid_temperature 
CHECK (temperature BETWEEN -50 AND 100);

-- Trigger for data validation
CREATE OR REPLACE FUNCTION validate_sensor_data()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.humidity < 0 OR NEW.humidity > 100 THEN
    RAISE EXCEPTION 'Invalid humidity: %', NEW.humidity;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### 12. What is first() and last() function?
**Answer**: Get first/last values in time order.

```sql
-- First and last readings
SELECT device_id,
       first(temperature, time) AS first_temp,
       last(temperature, time) AS last_temp
FROM metrics
WHERE time >= NOW() - INTERVAL '1 day'
GROUP BY device_id;
```

### 13. How do you handle time zones?
**Answer**: Store in UTC, convert for display.

```sql
-- Store in UTC
INSERT INTO metrics (time, device_id, temperature)
VALUES (NOW() AT TIME ZONE 'UTC', 'sensor_001', 23.5);

-- Query with timezone conversion
SELECT time AT TIME ZONE 'America/New_York' AS local_time,
       temperature
FROM metrics
WHERE time >= NOW() - INTERVAL '1 hour';
```

### 14. What are TimescaleDB indexes?
**Answer**: Automatic time-based indexing plus custom indexes.

```sql
-- View indexes
SELECT * FROM pg_indexes WHERE tablename = 'metrics';

-- Create custom index
CREATE INDEX idx_device_time ON metrics (device_id, time DESC);

-- Partial index for recent data
CREATE INDEX idx_recent_metrics ON metrics (device_id, temperature)
WHERE time >= NOW() - INTERVAL '7 days';
```

### 15. How do you use histogram() function?
**Answer**: Create frequency distributions of values.

```sql
-- Temperature distribution
SELECT histogram(temperature, 20, 25, 5) AS temp_histogram
FROM metrics
WHERE time >= NOW() - INTERVAL '1 day';

-- Custom bucket histogram
SELECT histogram(temperature, ARRAY[0, 10, 20, 30, 40]) AS buckets
FROM metrics;
```

### 16. What is approximate_row_count()?
**Answer**: Fast row count estimation for large tables.

```sql
-- Fast count estimation
SELECT approximate_row_count('metrics');

-- Compare with exact count
SELECT COUNT(*) FROM metrics; -- Slower for large tables
```

### 17. How do you implement downsampling?
**Answer**: Use continuous aggregates for automatic downsampling.

```sql
-- Create downsampled view
CREATE MATERIALIZED VIEW daily_averages
WITH (timescaledb.continuous) AS
SELECT time_bucket('1 day', time) AS day,
       device_id,
       avg(temperature) AS avg_temp,
       min(temperature) AS min_temp,
       max(temperature) AS max_temp
FROM metrics
GROUP BY day, device_id;

-- Refresh policy
SELECT add_continuous_aggregate_policy('daily_averages',
  start_offset => INTERVAL '1 month',
  end_offset => INTERVAL '1 hour',
  schedule_interval => INTERVAL '1 hour');
```

### 18. What are TimescaleDB functions for analytics?
**Answer**: Specialized functions for time-series analysis.

```sql
-- Moving averages
SELECT time,
       temperature,
       avg(temperature) OVER (
         ORDER BY time 
         ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
       ) AS moving_avg_5
FROM metrics
ORDER BY time;

-- Rate of change
SELECT time_bucket('1 minute', time) AS minute,
       avg(temperature) AS avg_temp,
       LAG(avg(temperature)) OVER (ORDER BY time_bucket('1 minute', time)) AS prev_temp
FROM metrics
GROUP BY minute
ORDER BY minute;
```

### 19. How do you handle duplicate data?
**Answer**: Use UPSERT and unique constraints.

```sql
-- Create unique constraint
ALTER TABLE metrics 
ADD CONSTRAINT unique_reading 
UNIQUE (time, device_id);

-- Upsert operation
INSERT INTO metrics (time, device_id, temperature)
VALUES ('2023-01-01 10:00:00', 'sensor_001', 23.5)
ON CONFLICT (time, device_id)
DO UPDATE SET temperature = EXCLUDED.temperature;
```

### 20. What is TimescaleDB licensing?
**Answer**: Apache 2.0 for community, commercial for enterprise features.

**Community Features:**
- Hypertables and chunks
- Compression
- Continuous aggregates
- Basic functions

**Enterprise Features:**
- Multi-node clustering
- Advanced compression
- Data tiering
- Enhanced security

## Hypertables & Chunks (21-40)

### 21. How do you configure chunk time intervals?
**Answer**: Set chunk_time_interval during hypertable creation.

```sql
-- Create with custom chunk interval
SELECT create_hypertable('metrics', 'time', 
                        chunk_time_interval => INTERVAL '1 hour');

-- Modify existing hypertable
SELECT set_chunk_time_interval('metrics', INTERVAL '2 hours');
```

### 22. What is space partitioning?
**Answer**: Partition by non-time dimension for parallel processing.

```sql
-- Space partitioning by device_id
SELECT create_hypertable('sensor_data', 'time',
                        partitioning_column => 'device_id',
                        number_partitions => 8);

-- Hash partitioning
SELECT create_hypertable('events', 'time',
                        partitioning_column => 'user_id',
                        number_partitions => 4,
                        partitioning_func => 'hash');
```

### 23. How do you manage chunk size?
**Answer**: Balance between query performance and maintenance overhead.

```sql
-- Check chunk sizes
SELECT 
  chunk_name,
  pg_size_pretty(pg_total_relation_size(chunk_name)) AS size,
  range_start,
  range_end
FROM timescaledb_information.chunks
WHERE hypertable_name = 'metrics'
ORDER BY range_start DESC;

-- Optimal chunk size: 25% of memory
-- For 32GB RAM: ~8GB chunks = 1 week intervals for high-frequency data
```

### 24. What are chunk exclusion benefits?
**Answer**: Query planner skips irrelevant chunks automatically.

```sql
-- Query with time filter (chunk exclusion)
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM metrics 
WHERE time >= '2023-01-01' AND time < '2023-01-02';

-- Without time filter (scans all chunks)
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM metrics 
WHERE device_id = 'sensor_001';
```

### 25. How do you drop chunks manually?
**Answer**: Use drop_chunks() function for data management.

```sql
-- Drop chunks older than 30 days
SELECT drop_chunks('metrics', INTERVAL '30 days');

-- Drop specific chunk
SELECT drop_chunks('metrics', 
                   older_than => '2023-01-01'::timestamptz);

-- Dry run to see what would be dropped
SELECT show_chunks('metrics', older_than => INTERVAL '30 days');
```

### 26. What is chunk compression ratio?
**Answer**: Measure of storage savings from compression.

```sql
-- Check compression stats
SELECT 
  chunk_name,
  before_compression_total_bytes,
  after_compression_total_bytes,
  ROUND(
    (before_compression_total_bytes - after_compression_total_bytes)::numeric / 
    before_compression_total_bytes * 100, 2
  ) AS compression_ratio_percent
FROM timescaledb_information.chunk_compression_stats;
```

### 27. How do you reorder chunks?
**Answer**: Use cluster command for physical ordering.

```sql
-- Cluster chunk by time
CLUSTER _timescaledb_internal._hyper_1_1_chunk 
USING _hyper_1_1_chunk_metrics_time_idx;

-- Reorder all chunks
SELECT reorder_chunk(chunk, 'metrics_time_idx')
FROM timescaledb_information.chunks
WHERE hypertable_name = 'metrics';
```

### 28. What are chunk constraints?
**Answer**: Automatic constraints for chunk exclusion optimization.

```sql
-- View chunk constraints
SELECT 
  chunk_name,
  constraint_name,
  constraint_type
FROM timescaledb_information.chunk_constraints
WHERE hypertable_name = 'metrics';

-- Add custom constraint
ALTER TABLE _timescaledb_internal._hyper_1_1_chunk
ADD CONSTRAINT device_constraint 
CHECK (device_id IN ('sensor_001', 'sensor_002'));
```

### 29. How do you handle chunk creation?
**Answer**: Chunks created automatically based on time intervals.

```sql
-- Monitor chunk creation
SELECT 
  hypertable_name,
  chunk_name,
  created_at
FROM timescaledb_information.chunks
ORDER BY created_at DESC
LIMIT 10;

-- Pre-create chunks
SELECT add_dimension('metrics', 'device_id', number_partitions => 4);
```

### 30. What is chunk append optimization?
**Answer**: Optimized inserts when data arrives in time order.

```sql
-- Optimal insert pattern (time-ordered)
INSERT INTO metrics (time, device_id, temperature)
SELECT 
  generate_series(NOW() - INTERVAL '1 hour', NOW(), INTERVAL '1 minute'),
  'sensor_001',
  random() * 100;

-- Monitor insert performance
SELECT * FROM pg_stat_user_tables WHERE relname = 'metrics';
```

### 31. How do you implement chunk-wise operations?
**Answer**: Process chunks individually for large operations.

```sql
-- Process chunks in batches
DO $$
DECLARE
  chunk_name TEXT;
BEGIN
  FOR chunk_name IN 
    SELECT c.chunk_name 
    FROM timescaledb_information.chunks c
    WHERE c.hypertable_name = 'metrics'
    ORDER BY c.range_start
  LOOP
    EXECUTE format('ANALYZE %I', chunk_name);
    RAISE NOTICE 'Processed chunk: %', chunk_name;
  END LOOP;
END $$;
```

### 32. What are distributed hypertables?
**Answer**: Multi-node hypertables for horizontal scaling.

```sql
-- Create distributed hypertable (Enterprise)
SELECT create_distributed_hypertable('metrics', 'time', 'device_id');

-- Add data nodes
SELECT add_data_node('node1', host => 'node1.example.com');
SELECT add_data_node('node2', host => 'node2.example.com');
```

### 33. How do you monitor chunk health?
**Answer**: Check chunk statistics and performance metrics.

```sql
-- Chunk health metrics
SELECT 
  chunk_name,
  range_start,
  range_end,
  is_compressed,
  pg_size_pretty(pg_total_relation_size(chunk_name)) AS size
FROM timescaledb_information.chunks
WHERE hypertable_name = 'metrics'
ORDER BY range_start DESC;

-- Identify problematic chunks
SELECT chunk_name
FROM timescaledb_information.chunks
WHERE pg_total_relation_size(chunk_name) > 1073741824; -- > 1GB
```

### 34. What is chunk migration?
**Answer**: Moving chunks between storage tiers or nodes.

```sql
-- Move chunk to different tablespace
ALTER TABLE _timescaledb_internal._hyper_1_1_chunk 
SET TABLESPACE cold_storage;

-- Compress old chunks
SELECT compress_chunk(chunk)
FROM timescaledb_information.chunks
WHERE hypertable_name = 'metrics'
  AND range_end < NOW() - INTERVAL '7 days'
  AND NOT is_compressed;
```

### 35. How do you implement chunk archival?
**Answer**: Export chunks to external storage systems.

```sql
-- Export chunk data
COPY (
  SELECT * FROM _timescaledb_internal._hyper_1_1_chunk
) TO '/archive/chunk_data.csv' CSV HEADER;

-- Create external table reference
CREATE FOREIGN TABLE archived_metrics (
  time TIMESTAMPTZ,
  device_id TEXT,
  temperature DOUBLE PRECISION
) SERVER file_server
OPTIONS (filename '/archive/chunk_data.csv', format 'csv');
```

### 36. What are chunk statistics?
**Answer**: Metadata about chunk contents and performance.

```sql
-- Detailed chunk statistics
SELECT 
  c.chunk_name,
  c.range_start,
  c.range_end,
  s.n_tup_ins AS inserts,
  s.n_tup_upd AS updates,
  s.n_tup_del AS deletes,
  s.seq_scan AS sequential_scans,
  s.idx_scan AS index_scans
FROM timescaledb_information.chunks c
JOIN pg_stat_user_tables s ON s.relname = c.chunk_name
WHERE c.hypertable_name = 'metrics';
```

### 37. How do you handle chunk locks?
**Answer**: Manage concurrent access to chunks during operations.

```sql
-- Check for chunk locks
SELECT 
  l.locktype,
  l.mode,
  l.granted,
  c.chunk_name
FROM pg_locks l
JOIN timescaledb_information.chunks c ON l.relation = c.chunk_name::regclass
WHERE c.hypertable_name = 'metrics';

-- Lock chunk for maintenance
LOCK TABLE _timescaledb_internal._hyper_1_1_chunk IN ACCESS EXCLUSIVE MODE;
```

### 38. What is chunk pruning?
**Answer**: Automatic elimination of chunks from query plans.

```sql
-- Query with effective pruning
EXPLAIN (ANALYZE, BUFFERS)
SELECT device_id, avg(temperature)
FROM metrics
WHERE time >= '2023-01-01' AND time < '2023-01-02'
  AND device_id = 'sensor_001'
GROUP BY device_id;

-- Check pruning effectiveness
SELECT 
  query,
  chunks_excluded,
  chunks_scanned
FROM pg_stat_statements
WHERE query LIKE '%metrics%';
```

### 39. How do you implement chunk backup?
**Answer**: Backup individual chunks for granular recovery.

```sql
-- Backup specific chunk
pg_dump -t _timescaledb_internal._hyper_1_1_chunk mydb > chunk_backup.sql

-- Backup chunk with data only
pg_dump --data-only -t _timescaledb_internal._hyper_1_1_chunk mydb > chunk_data.sql

-- Restore chunk
psql mydb < chunk_backup.sql
```

### 40. What are chunk maintenance operations?
**Answer**: Regular operations to maintain chunk health and performance.

```sql
-- Vacuum chunks
VACUUM ANALYZE _timescaledb_internal._hyper_1_1_chunk;

-- Reindex chunks
REINDEX TABLE _timescaledb_internal._hyper_1_1_chunk;

-- Update statistics
ANALYZE _timescaledb_internal._hyper_1_1_chunk;

-- Automated maintenance
SELECT add_job('chunk_maintenance', '1 hour');
```
## Queries & Performance (41-60)

### 41. How do you optimize time-series queries?
**Answer**: Use proper indexing, time filters, and query patterns.

```sql
-- Efficient query pattern
SELECT time_bucket('1 hour', time) AS hour,
       device_id,
       avg(temperature) AS avg_temp
FROM metrics
WHERE time >= NOW() - INTERVAL '24 hours'  -- Always filter by time first
  AND device_id IN ('sensor_001', 'sensor_002')  -- Limit cardinality
GROUP BY hour, device_id
ORDER BY hour DESC;

-- Create optimal indexes
CREATE INDEX idx_metrics_device_time ON metrics (device_id, time DESC);
CREATE INDEX idx_metrics_time_temp ON metrics (time, temperature) 
WHERE temperature > 50;  -- Partial index for hot data
```

### 42. What are TimescaleDB-specific query optimizations?
**Answer**: Leverage chunk exclusion and parallel processing.

```sql
-- Enable parallel queries
SET max_parallel_workers_per_gather = 4;
SET parallel_tuple_cost = 0.1;

-- Use chunk-aware queries
SELECT * FROM show_chunks('metrics', 
  newer_than => NOW() - INTERVAL '1 day');

-- Parallel aggregation across chunks
SELECT device_id, 
       avg(temperature) AS avg_temp,
       count(*) AS readings
FROM metrics
WHERE time >= NOW() - INTERVAL '7 days'
GROUP BY device_id;
```

### 43. How do you implement sliding window queries?
**Answer**: Use window functions with time-based frames.

```sql
-- Moving average over time
SELECT time,
       device_id,
       temperature,
       avg(temperature) OVER (
         PARTITION BY device_id 
         ORDER BY time 
         ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
       ) AS moving_avg_5
FROM metrics
WHERE time >= NOW() - INTERVAL '1 day'
ORDER BY device_id, time;

-- Time-based sliding window
SELECT time,
       temperature,
       avg(temperature) OVER (
         ORDER BY time 
         RANGE BETWEEN INTERVAL '30 minutes' PRECEDING 
         AND CURRENT ROW
       ) AS sliding_avg_30min
FROM metrics
WHERE device_id = 'sensor_001';
```

### 44. How do you perform gap filling and interpolation?
**Answer**: Use time_bucket_gapfill with interpolation functions.

```sql
-- Linear interpolation for missing data
SELECT time_bucket_gapfill('5 minutes', time) AS bucket,
       device_id,
       interpolate(avg(temperature)) AS temperature,
       locf(avg(humidity)) AS humidity  -- Last observation carried forward
FROM metrics
WHERE time >= NOW() - INTERVAL '2 hours'
  AND device_id = 'sensor_001'
GROUP BY bucket, device_id
ORDER BY bucket;

-- Custom interpolation bounds
SELECT time_bucket_gapfill('1 hour', time,
         start => '2023-01-01 00:00:00',
         finish => '2023-01-02 00:00:00') AS bucket,
       interpolate(avg(temperature),
         prev => LAG(avg(temperature)) OVER (ORDER BY time_bucket('1 hour', time)),
         next => LEAD(avg(temperature)) OVER (ORDER BY time_bucket('1 hour', time))
       ) AS interpolated_temp
FROM metrics
GROUP BY bucket;
```

### 45. What are advanced aggregation patterns?
**Answer**: Combine multiple aggregation functions and time windows.

```sql
-- Multi-level aggregations
WITH hourly_stats AS (
  SELECT time_bucket('1 hour', time) AS hour,
         device_id,
         avg(temperature) AS avg_temp,
         stddev(temperature) AS stddev_temp,
         count(*) AS readings
  FROM metrics
  WHERE time >= NOW() - INTERVAL '7 days'
  GROUP BY hour, device_id
)
SELECT device_id,
       avg(avg_temp) AS daily_avg,
       max(avg_temp) AS daily_max,
       min(avg_temp) AS daily_min,
       avg(stddev_temp) AS avg_variability
FROM hourly_stats
GROUP BY device_id;

-- Percentile aggregations
SELECT time_bucket('1 hour', time) AS hour,
       percentile_cont(0.5) WITHIN GROUP (ORDER BY temperature) AS median_temp,
       percentile_cont(0.95) WITHIN GROUP (ORDER BY temperature) AS p95_temp,
       percentile_cont(0.99) WITHIN GROUP (ORDER BY temperature) AS p99_temp
FROM metrics
WHERE time >= NOW() - INTERVAL '24 hours'
GROUP BY hour
ORDER BY hour;
```

### 46. How do you implement real-time analytics?
**Answer**: Use continuous aggregates with real-time refresh.

```sql
-- Real-time continuous aggregate
CREATE MATERIALIZED VIEW real_time_stats
WITH (timescaledb.continuous, timescaledb.materialized_only=false) AS
SELECT time_bucket('1 minute', time) AS minute,
       device_id,
       avg(temperature) AS avg_temp,
       max(temperature) AS max_temp,
       count(*) AS readings
FROM metrics
GROUP BY minute, device_id;

-- Enable real-time aggregation
ALTER MATERIALIZED VIEW real_time_stats SET (timescaledb.materialized_only=false);

-- Query includes both materialized and real-time data
SELECT * FROM real_time_stats 
WHERE minute >= NOW() - INTERVAL '1 hour'
ORDER BY minute DESC;
```

### 47. How do you perform time-series joins?
**Answer**: Join on time buckets and use proper indexing.

```sql
-- Time-aligned join
SELECT m.bucket,
       m.device_id,
       m.avg_temp,
       w.avg_humidity
FROM (
  SELECT time_bucket('5 minutes', time) AS bucket,
         device_id,
         avg(temperature) AS avg_temp
  FROM temperature_metrics
  WHERE time >= NOW() - INTERVAL '1 hour'
  GROUP BY bucket, device_id
) m
JOIN (
  SELECT time_bucket('5 minutes', time) AS bucket,
         device_id,
         avg(humidity) AS avg_humidity
  FROM humidity_metrics
  WHERE time >= NOW() - INTERVAL '1 hour'
  GROUP BY bucket, device_id
) w ON m.bucket = w.bucket AND m.device_id = w.device_id;

-- ASOF join for nearest time match
SELECT DISTINCT ON (t1.time, t1.device_id)
       t1.time,
       t1.device_id,
       t1.temperature,
       t2.humidity
FROM temperature_readings t1
LEFT JOIN LATERAL (
  SELECT humidity
  FROM humidity_readings t2
  WHERE t2.device_id = t1.device_id
    AND t2.time <= t1.time
  ORDER BY t2.time DESC
  LIMIT 1
) t2 ON true
WHERE t1.time >= NOW() - INTERVAL '1 hour';
```

### 48. What are query performance monitoring techniques?
**Answer**: Use PostgreSQL and TimescaleDB-specific monitoring.

```sql
-- Query performance statistics
SELECT query,
       calls,
       total_time,
       mean_time,
       rows
FROM pg_stat_statements
WHERE query LIKE '%metrics%'
ORDER BY total_time DESC;

-- Chunk exclusion analysis
EXPLAIN (ANALYZE, BUFFERS, COSTS OFF)
SELECT device_id, avg(temperature)
FROM metrics
WHERE time >= '2023-01-01' AND time < '2023-01-02'
GROUP BY device_id;

-- Index usage statistics
SELECT schemaname,
       tablename,
       indexname,
       idx_scan,
       idx_tup_read,
       idx_tup_fetch
FROM pg_stat_user_indexes
WHERE tablename LIKE '%metrics%'
ORDER BY idx_scan DESC;
```

### 49. How do you implement custom aggregation functions?
**Answer**: Create user-defined aggregate functions for specific needs.

```sql
-- Custom weighted average aggregate
CREATE OR REPLACE FUNCTION weighted_avg_state(state NUMERIC[], value NUMERIC, weight NUMERIC)
RETURNS NUMERIC[] AS $$
BEGIN
  IF state IS NULL THEN
    state := ARRAY[0, 0];
  END IF;
  state[1] := state[1] + (value * weight);
  state[2] := state[2] + weight;
  RETURN state;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION weighted_avg_final(state NUMERIC[])
RETURNS NUMERIC AS $$
BEGIN
  IF state[2] = 0 THEN
    RETURN NULL;
  END IF;
  RETURN state[1] / state[2];
END;
$$ LANGUAGE plpgsql;

CREATE AGGREGATE weighted_avg(NUMERIC, NUMERIC) (
  SFUNC = weighted_avg_state,
  STYPE = NUMERIC[],
  FINALFUNC = weighted_avg_final
);

-- Use custom aggregate
SELECT time_bucket('1 hour', time) AS hour,
       weighted_avg(temperature, confidence_score) AS weighted_temp
FROM sensor_readings
GROUP BY hour;
```

### 50. What are advanced time-series calculations?
**Answer**: Implement complex analytics like seasonality and trends.

```sql
-- Seasonal decomposition
WITH daily_avg AS (
  SELECT date_trunc('day', time) AS day,
         avg(temperature) AS avg_temp
  FROM metrics
  WHERE time >= NOW() - INTERVAL '365 days'
  GROUP BY day
),
trend AS (
  SELECT day,
         avg_temp,
         avg(avg_temp) OVER (
           ORDER BY day 
           ROWS BETWEEN 15 PRECEDING AND 15 FOLLOWING
         ) AS trend_component
  FROM daily_avg
)
SELECT day,
       avg_temp AS original,
       trend_component,
       avg_temp - trend_component AS seasonal_component
FROM trend
ORDER BY day;

-- Rate of change analysis
SELECT time_bucket('1 hour', time) AS hour,
       device_id,
       avg(temperature) AS current_temp,
       LAG(avg(temperature)) OVER (
         PARTITION BY device_id 
         ORDER BY time_bucket('1 hour', time)
       ) AS prev_temp,
       (avg(temperature) - LAG(avg(temperature)) OVER (
         PARTITION BY device_id 
         ORDER BY time_bucket('1 hour', time)
       )) AS temp_change
FROM metrics
WHERE time >= NOW() - INTERVAL '48 hours'
GROUP BY hour, device_id
ORDER BY device_id, hour;
```

### 51. How do you optimize continuous aggregates?
**Answer**: Configure refresh policies and materialization strategies.

```sql
-- Optimize continuous aggregate refresh
SELECT add_continuous_aggregate_policy('hourly_stats',
  start_offset => INTERVAL '1 month',
  end_offset => INTERVAL '1 hour',
  schedule_interval => INTERVAL '30 minutes');

-- Manual refresh for recent data
CALL refresh_continuous_aggregate('hourly_stats', 
  NOW() - INTERVAL '2 hours', 
  NOW());

-- Optimize materialization window
ALTER MATERIALIZED VIEW hourly_stats 
SET (timescaledb.materialized_only = true);

-- Check refresh statistics
SELECT * FROM timescaledb_information.continuous_aggregate_stats;
```

### 52. What are query optimization best practices?
**Answer**: Follow time-series specific optimization patterns.

```sql
-- Always filter by time first
SELECT device_id, avg(temperature)
FROM metrics
WHERE time >= NOW() - INTERVAL '1 day'  -- Time filter first
  AND device_id = 'sensor_001'          -- Then other filters
GROUP BY device_id;

-- Use appropriate time buckets
-- Good: reasonable bucket size
SELECT time_bucket('5 minutes', time), avg(temperature)
FROM metrics
WHERE time >= NOW() - INTERVAL '1 day'
GROUP BY 1;

-- Bad: too granular for large time range
-- SELECT time_bucket('1 second', time), avg(temperature)
-- FROM metrics
-- WHERE time >= NOW() - INTERVAL '1 year'  -- Don't do this

-- Limit result sets
SELECT time_bucket('1 hour', time) AS hour,
       avg(temperature)
FROM metrics
WHERE time >= NOW() - INTERVAL '7 days'
GROUP BY hour
ORDER BY hour DESC
LIMIT 168;  -- One week of hourly data
```

### 53. How do you implement anomaly detection?
**Answer**: Use statistical functions and window comparisons.

```sql
-- Z-score based anomaly detection
WITH stats AS (
  SELECT device_id,
         avg(temperature) AS mean_temp,
         stddev(temperature) AS stddev_temp
  FROM metrics
  WHERE time >= NOW() - INTERVAL '30 days'
  GROUP BY device_id
)
SELECT m.time,
       m.device_id,
       m.temperature,
       s.mean_temp,
       ABS(m.temperature - s.mean_temp) / s.stddev_temp AS z_score
FROM metrics m
JOIN stats s ON m.device_id = s.device_id
WHERE m.time >= NOW() - INTERVAL '1 day'
  AND ABS(m.temperature - s.mean_temp) / s.stddev_temp > 2.5  -- Anomaly threshold
ORDER BY z_score DESC;

-- Moving window anomaly detection
SELECT time,
       device_id,
       temperature,
       avg(temperature) OVER w AS window_avg,
       stddev(temperature) OVER w AS window_stddev,
       CASE 
         WHEN ABS(temperature - avg(temperature) OVER w) > 
              2 * stddev(temperature) OVER w 
         THEN 'ANOMALY'
         ELSE 'NORMAL'
       END AS status
FROM metrics
WHERE time >= NOW() - INTERVAL '1 day'
WINDOW w AS (
  PARTITION BY device_id 
  ORDER BY time 
  ROWS BETWEEN 50 PRECEDING AND CURRENT ROW
);
```

### 54. How do you perform correlation analysis?
**Answer**: Calculate correlations between different metrics.

```sql
-- Correlation between temperature and humidity
WITH aligned_data AS (
  SELECT time_bucket('5 minutes', time) AS bucket,
         device_id,
         avg(temperature) AS avg_temp,
         avg(humidity) AS avg_humidity
  FROM metrics
  WHERE time >= NOW() - INTERVAL '7 days'
  GROUP BY bucket, device_id
)
SELECT device_id,
       corr(avg_temp, avg_humidity) AS temp_humidity_correlation,
       count(*) AS data_points
FROM aligned_data
GROUP BY device_id
HAVING count(*) > 100;  -- Minimum data points for reliable correlation

-- Cross-correlation with time lags
SELECT lag_minutes,
       corr(temperature, lagged_humidity) AS correlation
FROM (
  SELECT time,
         temperature,
         LAG(humidity, lag_minutes) OVER (ORDER BY time) AS lagged_humidity
  FROM (
    SELECT time_bucket('1 minute', time) AS time,
           avg(temperature) AS temperature,
           avg(humidity) AS humidity
    FROM metrics
    WHERE device_id = 'sensor_001'
      AND time >= NOW() - INTERVAL '1 day'
    GROUP BY time_bucket('1 minute', time)
  ) bucketed_data
  CROSS JOIN generate_series(0, 60, 5) AS lag_minutes
) lagged_data
GROUP BY lag_minutes
ORDER BY lag_minutes;
```

### 55. What are time-series forecasting queries?
**Answer**: Implement trend analysis and simple forecasting models.

```sql
-- Linear trend forecasting
WITH historical_data AS (
  SELECT time_bucket('1 day', time) AS day,
         avg(temperature) AS avg_temp,
         extract(epoch from time_bucket('1 day', time)) AS day_epoch
  FROM metrics
  WHERE time >= NOW() - INTERVAL '30 days'
    AND device_id = 'sensor_001'
  GROUP BY day
),
trend_analysis AS (
  SELECT regr_slope(avg_temp, day_epoch) AS slope,
         regr_intercept(avg_temp, day_epoch) AS intercept
  FROM historical_data
)
SELECT generate_series(
         date_trunc('day', NOW()),
         date_trunc('day', NOW()) + INTERVAL '7 days',
         INTERVAL '1 day'
       ) AS forecast_day,
       (slope * extract(epoch from generate_series(
         date_trunc('day', NOW()),
         date_trunc('day', NOW()) + INTERVAL '7 days',
         INTERVAL '1 day'
       )) + intercept) AS forecasted_temp
FROM trend_analysis;

-- Exponential smoothing
WITH smoothed_data AS (
  SELECT time,
         temperature,
         CASE 
           WHEN ROW_NUMBER() OVER (ORDER BY time) = 1 
           THEN temperature
           ELSE 0.3 * temperature + 0.7 * LAG(temperature) OVER (ORDER BY time)
         END AS smoothed_temp
  FROM (
    SELECT time_bucket('1 hour', time) AS time,
           avg(temperature) AS temperature
    FROM metrics
    WHERE device_id = 'sensor_001'
      AND time >= NOW() - INTERVAL '7 days'
    GROUP BY time_bucket('1 hour', time)
    ORDER BY time
  ) hourly_data
)
SELECT time,
       temperature,
       smoothed_temp,
       LEAD(smoothed_temp) OVER (ORDER BY time) AS next_hour_forecast
FROM smoothed_data
ORDER BY time DESC
LIMIT 24;
```

### 56. How do you implement data quality monitoring?
**Answer**: Create queries to detect data quality issues.

```sql
-- Data completeness monitoring
SELECT time_bucket('1 hour', time) AS hour,
       device_id,
       count(*) AS actual_readings,
       60 AS expected_readings,  -- Expecting 1 reading per minute
       ROUND(count(*) * 100.0 / 60, 2) AS completeness_percent
FROM metrics
WHERE time >= NOW() - INTERVAL '24 hours'
GROUP BY hour, device_id
HAVING count(*) < 50  -- Alert if less than 50 readings per hour
ORDER BY completeness_percent ASC;

-- Outlier detection
WITH device_stats AS (
  SELECT device_id,
         percentile_cont(0.25) WITHIN GROUP (ORDER BY temperature) AS q1,
         percentile_cont(0.75) WITHIN GROUP (ORDER BY temperature) AS q3
  FROM metrics
  WHERE time >= NOW() - INTERVAL '7 days'
  GROUP BY device_id
)
SELECT m.time,
       m.device_id,
       m.temperature,
       'OUTLIER' AS flag
FROM metrics m
JOIN device_stats s ON m.device_id = s.device_id
WHERE m.time >= NOW() - INTERVAL '1 day'
  AND (m.temperature < s.q1 - 1.5 * (s.q3 - s.q1) OR
       m.temperature > s.q3 + 1.5 * (s.q3 - s.q1));

-- Duplicate detection
SELECT time,
       device_id,
       count(*) AS duplicate_count
FROM metrics
WHERE time >= NOW() - INTERVAL '1 day'
GROUP BY time, device_id
HAVING count(*) > 1;
```

### 57. How do you optimize large-scale aggregations?
**Answer**: Use parallel processing and efficient aggregation strategies.

```sql
-- Parallel aggregation configuration
SET max_parallel_workers_per_gather = 8;
SET parallel_tuple_cost = 0.1;
SET parallel_setup_cost = 1000;

-- Hierarchical aggregation
WITH hourly_agg AS (
  SELECT time_bucket('1 hour', time) AS hour,
         device_id,
         avg(temperature) AS hourly_avg,
         count(*) AS hourly_count
  FROM metrics
  WHERE time >= NOW() - INTERVAL '30 days'
  GROUP BY hour, device_id
),
daily_agg AS (
  SELECT time_bucket('1 day', hour) AS day,
         device_id,
         avg(hourly_avg) AS daily_avg,
         sum(hourly_count) AS daily_count
  FROM hourly_agg
  GROUP BY day, device_id
)
SELECT device_id,
       avg(daily_avg) AS monthly_avg,
       sum(daily_count) AS total_readings
FROM daily_agg
GROUP BY device_id;

-- Partitioned aggregation
SELECT device_id,
       avg(temperature) AS avg_temp,
       count(*) AS readings
FROM metrics
WHERE time >= NOW() - INTERVAL '7 days'
GROUP BY device_id
HAVING count(*) > 1000;  -- Only devices with sufficient data
```

### 58. What are advanced window functions?
**Answer**: Use sophisticated window operations for time-series analysis.

```sql
-- Cumulative statistics
SELECT time,
       device_id,
       temperature,
       sum(temperature) OVER (
         PARTITION BY device_id 
         ORDER BY time 
         ROWS UNBOUNDED PRECEDING
       ) AS cumulative_temp,
       row_number() OVER (
         PARTITION BY device_id 
         ORDER BY time
       ) AS reading_sequence,
       ntile(4) OVER (
         PARTITION BY device_id 
         ORDER BY temperature
       ) AS temperature_quartile
FROM metrics
WHERE time >= NOW() - INTERVAL '1 day'
ORDER BY device_id, time;

-- Advanced ranking and percentiles
SELECT time,
       device_id,
       temperature,
       percent_rank() OVER (
         PARTITION BY device_id 
         ORDER BY temperature
       ) AS temperature_percentile,
       cume_dist() OVER (
         PARTITION BY device_id 
         ORDER BY temperature
       ) AS cumulative_distribution,
       dense_rank() OVER (
         PARTITION BY date_trunc('day', time) 
         ORDER BY temperature DESC
       ) AS daily_temp_rank
FROM metrics
WHERE time >= NOW() - INTERVAL '7 days';
```

### 59. How do you implement event detection?
**Answer**: Identify patterns and events in time-series data.

```sql
-- Threshold crossing detection
WITH threshold_events AS (
  SELECT time,
         device_id,
         temperature,
         LAG(temperature) OVER (PARTITION BY device_id ORDER BY time) AS prev_temp,
         CASE 
           WHEN temperature > 30 AND 
                LAG(temperature) OVER (PARTITION BY device_id ORDER BY time) <= 30 
           THEN 'THRESHOLD_CROSSED_UP'
           WHEN temperature <= 30 AND 
                LAG(temperature) OVER (PARTITION BY device_id ORDER BY time) > 30 
           THEN 'THRESHOLD_CROSSED_DOWN'
         END AS event_type
  FROM metrics
  WHERE time >= NOW() - INTERVAL '1 day'
)
SELECT time,
       device_id,
       temperature,
       event_type
FROM threshold_events
WHERE event_type IS NOT NULL;

-- Pattern detection (consecutive high values)
WITH consecutive_high AS (
  SELECT time,
         device_id,
         temperature,
         CASE WHEN temperature > 35 THEN 1 ELSE 0 END AS is_high,
         sum(CASE WHEN temperature > 35 THEN 0 ELSE 1 END) 
           OVER (PARTITION BY device_id ORDER BY time) AS group_id
  FROM metrics
  WHERE time >= NOW() - INTERVAL '1 day'
),
high_periods AS (
  SELECT device_id,
         group_id,
         min(time) AS start_time,
         max(time) AS end_time,
         count(*) AS duration_minutes
  FROM consecutive_high
  WHERE is_high = 1
  GROUP BY device_id, group_id
  HAVING count(*) >= 5  -- At least 5 consecutive high readings
)
SELECT device_id,
       start_time,
       end_time,
       duration_minutes,
       'SUSTAINED_HIGH_TEMPERATURE' AS event_type
FROM high_periods;
```

### 60. How do you perform multi-dimensional analysis?
**Answer**: Analyze data across multiple dimensions and hierarchies.

```sql
-- Multi-dimensional OLAP-style queries
SELECT COALESCE(device_type, 'ALL') AS device_type,
       COALESCE(location, 'ALL') AS location,
       COALESCE(time_bucket('1 day', time)::text, 'ALL') AS day,
       avg(temperature) AS avg_temp,
       count(*) AS readings
FROM (
  SELECT time,
         CASE 
           WHEN device_id LIKE 'temp%' THEN 'temperature_sensor'
           WHEN device_id LIKE 'humid%' THEN 'humidity_sensor'
           ELSE 'other'
         END AS device_type,
         CASE 
           WHEN device_id LIKE '%_room1' THEN 'room1'
           WHEN device_id LIKE '%_room2' THEN 'room2'
           ELSE 'unknown'
         END AS location,
         temperature
  FROM metrics
  WHERE time >= NOW() - INTERVAL '7 days'
) categorized_data
GROUP BY ROLLUP(device_type, location, time_bucket('1 day', time))
ORDER BY device_type, location, day;

-- Pivot table style analysis
SELECT time_bucket('1 hour', time) AS hour,
       avg(CASE WHEN device_id = 'sensor_001' THEN temperature END) AS sensor_001_temp,
       avg(CASE WHEN device_id = 'sensor_002' THEN temperature END) AS sensor_002_temp,
       avg(CASE WHEN device_id = 'sensor_003' THEN temperature END) AS sensor_003_temp,
       avg(temperature) AS overall_avg
FROM metrics
WHERE time >= NOW() - INTERVAL '24 hours'
  AND device_id IN ('sensor_001', 'sensor_002', 'sensor_003')
GROUP BY hour
ORDER BY hour;
```
## Operations & Scaling (61-80)

### 61. How do you configure TimescaleDB for high availability?
**Answer**: Use PostgreSQL streaming replication and failover mechanisms.

```sql
-- Primary server configuration
-- postgresql.conf
wal_level = replica
max_wal_senders = 3
wal_keep_segments = 64

-- Create replication user
CREATE USER replicator REPLICATION LOGIN PASSWORD 'password';

-- Standby server setup
pg_basebackup -h primary_host -D /var/lib/postgresql/data -U replicator -P -W
```

### 62. How do you implement backup strategies?
**Answer**: Use pg_dump, continuous archiving, and point-in-time recovery.

```bash
# Full database backup
pg_dump -h localhost -U postgres -Fc timescaledb > backup.dump

# Hypertable-specific backup
pg_dump -h localhost -U postgres -t metrics -Fc timescaledb > metrics_backup.dump

# Continuous archiving setup
# postgresql.conf
archive_mode = on
archive_command = 'cp %p /backup/archive/%f'
```

### 63. What are distributed hypertable configurations?
**Answer**: Configure multi-node clusters for horizontal scaling.

```sql
-- Add data nodes (Enterprise feature)
SELECT add_data_node('node1', host => 'node1.example.com', port => 5432);
SELECT add_data_node('node2', host => 'node2.example.com', port => 5432);

-- Create distributed hypertable
SELECT create_distributed_hypertable('metrics', 'time', 'device_id', 
                                    data_nodes => ARRAY['node1', 'node2']);

-- Check distribution
SELECT * FROM timescaledb_information.data_nodes;
```

### 64. How do you monitor TimescaleDB performance?
**Answer**: Use built-in statistics and monitoring tools.

```sql
-- Hypertable statistics
SELECT * FROM timescaledb_information.hypertable_stats;

-- Compression statistics
SELECT * FROM timescaledb_information.compression_settings;

-- Job statistics
SELECT * FROM timescaledb_information.job_stats;

-- Query performance
SELECT * FROM pg_stat_statements WHERE query LIKE '%metrics%';
```

### 65. How do you implement data tiering?
**Answer**: Move old data to cheaper storage automatically.

```sql
-- Create tablespace for cold storage
CREATE TABLESPACE cold_storage LOCATION '/cold_storage';

-- Move old chunks to cold storage
SELECT move_chunk(chunk, 'cold_storage')
FROM timescaledb_information.chunks
WHERE hypertable_name = 'metrics'
  AND range_end < NOW() - INTERVAL '30 days';

-- Automated tiering policy
SELECT add_job('tier_old_chunks', '1 day');
```

### 66. What are connection pooling best practices?
**Answer**: Use PgBouncer or similar tools for connection management.

```bash
# PgBouncer configuration
[databases]
timescaledb = host=localhost port=5432 dbname=timescaledb

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
```

### 67. How do you optimize memory usage?
**Answer**: Configure PostgreSQL memory settings for time-series workloads.

```bash
# postgresql.conf optimizations
shared_buffers = 8GB                    # 25% of RAM
effective_cache_size = 24GB             # 75% of RAM
work_mem = 256MB                        # For sorting/hashing
maintenance_work_mem = 2GB              # For maintenance operations
max_connections = 200                   # Limit connections
```

### 68. How do you implement security measures?
**Answer**: Configure authentication, encryption, and access controls.

```sql
-- Row-level security
CREATE POLICY tenant_isolation ON metrics
  FOR ALL TO app_user
  USING (device_id = current_setting('app.tenant_id'));

ALTER TABLE metrics ENABLE ROW LEVEL SECURITY;

-- SSL configuration
# postgresql.conf
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file = 'server.key'
```

### 69. How do you handle schema migrations?
**Answer**: Use careful migration strategies for production systems.

```sql
-- Add column to hypertable
ALTER TABLE metrics ADD COLUMN pressure DOUBLE PRECISION;

-- Create new hypertable with updated schema
CREATE TABLE metrics_v2 (
  time TIMESTAMPTZ NOT NULL,
  device_id TEXT,
  temperature DOUBLE PRECISION,
  humidity DOUBLE PRECISION,
  pressure DOUBLE PRECISION
);

SELECT create_hypertable('metrics_v2', 'time');

-- Migrate data gradually
INSERT INTO metrics_v2 
SELECT time, device_id, temperature, humidity, NULL as pressure
FROM metrics
WHERE time >= '2023-01-01' AND time < '2023-01-02';
```

### 70. What are disaster recovery procedures?
**Answer**: Implement comprehensive backup and recovery strategies.

```bash
# Point-in-time recovery setup
# postgresql.conf
wal_level = replica
archive_mode = on
archive_command = 'cp %p /backup/wal/%f'

# Recovery procedure
pg_ctl stop -D /var/lib/postgresql/data
rm -rf /var/lib/postgresql/data/*
pg_basebackup -h backup_server -D /var/lib/postgresql/data -U postgres
# Create recovery.conf for PITR
pg_ctl start -D /var/lib/postgresql/data
```

### 71. How do you implement automated maintenance?
**Answer**: Schedule regular maintenance tasks using TimescaleDB jobs.

```sql
-- Automated compression job
SELECT add_compression_policy('metrics', INTERVAL '7 days');

-- Automated retention job  
SELECT add_retention_policy('metrics', INTERVAL '90 days');

-- Custom maintenance job
CREATE OR REPLACE FUNCTION maintenance_job()
RETURNS VOID AS $$
BEGIN
  -- Vacuum old chunks
  PERFORM vacuum_chunk(chunk)
  FROM timescaledb_information.chunks
  WHERE hypertable_name = 'metrics'
    AND range_end < NOW() - INTERVAL '1 day';
    
  -- Update statistics
  ANALYZE metrics;
END;
$$ LANGUAGE plpgsql;

SELECT add_job('maintenance_job', '1 day');
```

### 72. How do you scale write performance?
**Answer**: Optimize for high-throughput ingestion.

```sql
-- Batch inserts
INSERT INTO metrics (time, device_id, temperature, humidity)
VALUES 
  ('2023-01-01 10:00:00', 'sensor_001', 23.5, 65.2),
  ('2023-01-01 10:01:00', 'sensor_001', 23.7, 65.1),
  ('2023-01-01 10:02:00', 'sensor_001', 23.6, 65.3);

-- Use COPY for bulk loading
COPY metrics FROM '/data/sensor_data.csv' CSV HEADER;

-- Optimize checkpoint settings
# postgresql.conf
checkpoint_completion_target = 0.9
wal_buffers = 64MB
```

### 73. What are query optimization techniques?
**Answer**: Use TimescaleDB-specific optimizations.

```sql
-- Enable JIT compilation
SET jit = on;
SET jit_above_cost = 100000;

-- Use partial indexes
CREATE INDEX idx_recent_high_temp ON metrics (device_id, time)
WHERE time >= NOW() - INTERVAL '7 days' AND temperature > 30;

-- Optimize work_mem for queries
SET work_mem = '512MB';
```

### 74. How do you implement multi-tenancy?
**Answer**: Use schema separation or row-level security.

```sql
-- Schema-based multi-tenancy
CREATE SCHEMA tenant_001;
CREATE SCHEMA tenant_002;

CREATE TABLE tenant_001.metrics (
  time TIMESTAMPTZ NOT NULL,
  device_id TEXT,
  temperature DOUBLE PRECISION
);

SELECT create_hypertable('tenant_001.metrics', 'time');

-- Row-level security approach
CREATE POLICY tenant_policy ON metrics
  FOR ALL TO tenant_user
  USING (tenant_id = current_setting('app.current_tenant'));
```

### 75. How do you handle time zone issues?
**Answer**: Standardize on UTC and convert at application layer.

```sql
-- Set timezone to UTC
SET timezone = 'UTC';

-- Store all timestamps in UTC
INSERT INTO metrics (time, device_id, temperature)
VALUES (NOW() AT TIME ZONE 'UTC', 'sensor_001', 23.5);

-- Convert for display
SELECT time AT TIME ZONE 'America/New_York' AS local_time,
       temperature
FROM metrics;
```

### 76. What are capacity planning considerations?
**Answer**: Plan for data growth and resource requirements.

```sql
-- Estimate storage requirements
SELECT 
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables 
WHERE tablename LIKE '%metrics%';

-- Calculate growth rate
WITH daily_sizes AS (
  SELECT date_trunc('day', time) AS day,
         count(*) AS daily_records
  FROM metrics
  WHERE time >= NOW() - INTERVAL '30 days'
  GROUP BY day
)
SELECT avg(daily_records) AS avg_daily_records,
       avg(daily_records) * 365 AS projected_yearly_records
FROM daily_sizes;
```

### 77. How do you implement data archival?
**Answer**: Move old data to external storage systems.

```sql
-- Export old data
COPY (
  SELECT * FROM metrics 
  WHERE time < NOW() - INTERVAL '1 year'
) TO '/archive/old_metrics.csv' CSV HEADER;

-- Create foreign table for archived data
CREATE EXTENSION file_fdw;
CREATE SERVER archive_server FOREIGN DATA WRAPPER file_fdw;

CREATE FOREIGN TABLE archived_metrics (
  time TIMESTAMPTZ,
  device_id TEXT,
  temperature DOUBLE PRECISION
) SERVER archive_server
OPTIONS (filename '/archive/old_metrics.csv', format 'csv', header 'true');

-- Drop old chunks after archival
SELECT drop_chunks('metrics', INTERVAL '1 year');
```

### 78. What are upgrade procedures?
**Answer**: Follow careful upgrade paths for TimescaleDB versions.

```bash
# Backup before upgrade
pg_dump -Fc timescaledb > pre_upgrade_backup.dump

# Update TimescaleDB extension
ALTER EXTENSION timescaledb UPDATE;

# Check for issues
SELECT timescaledb_pre_restore();
SELECT timescaledb_post_restore();

# Verify upgrade
SELECT * FROM timescaledb_information.hypertables;
```

### 79. How do you implement cross-region replication?
**Answer**: Set up streaming replication across geographic regions.

```sql
-- Configure streaming replication
# postgresql.conf on primary
wal_level = replica
max_wal_senders = 5
wal_keep_segments = 100

# pg_hba.conf
host replication replicator 10.0.0.0/8 md5

-- Setup standby in different region
pg_basebackup -h primary.region1.com -D /var/lib/postgresql/data -U replicator -P -W

# recovery.conf on standby
standby_mode = 'on'
primary_conninfo = 'host=primary.region1.com port=5432 user=replicator'
```

### 80. What are troubleshooting techniques?
**Answer**: Use systematic approaches to diagnose and resolve issues.

```sql
-- Check system health
SELECT * FROM pg_stat_activity WHERE state = 'active';
SELECT * FROM pg_stat_replication;
SELECT * FROM pg_locks WHERE NOT granted;

-- Analyze slow queries
SELECT query, mean_time, calls, total_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Check chunk health
SELECT chunk_name, 
       pg_size_pretty(pg_total_relation_size(chunk_name)) AS size,
       is_compressed
FROM timescaledb_information.chunks
WHERE hypertable_name = 'metrics'
ORDER BY range_start DESC;

-- Monitor job execution
SELECT * FROM timescaledb_information.job_stats
WHERE last_run_status = 'ERROR';
```

---

**Total Questions: 80** | **Coverage: Complete TimescaleDB Ecosystem**