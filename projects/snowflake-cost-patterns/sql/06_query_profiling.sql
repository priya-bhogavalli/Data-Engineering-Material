-- Query profiling: finding the actual expensive queries instead of guessing.
--
-- QUERY_HISTORY (and ACCESS_HISTORY for lineage) is the starting point for any cost
-- investigation. The instinct to "look at the slowest query" is usually wrong — a query
-- that runs in 2 seconds but executes 50,000 times a day can cost more in aggregate
-- credits than one slow query that runs once.

-- ── Step 1: top credit consumers by total impact, not by single-run duration ─────────
-- This is the query that found the actual top cost driver on the migration: not the
-- handful of slow analyst queries everyone assumed were the problem, but a
-- mis-scheduled dashboard refresh job firing every 60 seconds instead of every hour.
SELECT
    query_text,
    warehouse_name,
    COUNT(*) AS execution_count,
    SUM(total_elapsed_time) / 1000 AS total_seconds,
    AVG(total_elapsed_time) / 1000 AS avg_seconds,
    SUM(credits_used_cloud_services) AS total_cloud_services_credits
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY(
    RESULT_LIMIT => 10000
))
WHERE start_time >= DATEADD('day', -7, CURRENT_TIMESTAMP())
GROUP BY query_text, warehouse_name
ORDER BY execution_count * avg_seconds DESC
LIMIT 25;

-- ── Step 2: find queries that spilled to disk/remote storage — a clear sign of an
-- undersized warehouse or a join that needs restructuring ───────────────────────────
SELECT
    query_id,
    query_text,
    warehouse_size,
    bytes_spilled_to_local_storage / POWER(1024, 3) AS gb_spilled_local,
    bytes_spilled_to_remote_storage / POWER(1024, 3) AS gb_spilled_remote,
    total_elapsed_time / 1000 AS elapsed_seconds
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY(
    RESULT_LIMIT => 10000
))
WHERE bytes_spilled_to_remote_storage > 0
ORDER BY bytes_spilled_to_remote_storage DESC
LIMIT 25;
-- remote spilling is the expensive case: the warehouse ran out of local SSD cache and
-- spilled intermediate results to cloud storage, which is both slow and adds I/O cost
-- on top of the compute cost already being paid for the query.

-- ── Step 3: find queries blocked on queuing (a concurrency problem, not a query problem) ─
SELECT
    query_id,
    query_text,
    warehouse_name,
    queued_provisioning_time / 1000 AS queued_provisioning_seconds,
    queued_overload_time / 1000 AS queued_overload_seconds,
    execution_time / 1000 AS execution_seconds
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY(
    RESULT_LIMIT => 10000
))
WHERE queued_overload_time > 5000  -- queued more than 5s waiting for warehouse capacity
ORDER BY queued_overload_time DESC
LIMIT 25;

-- ── Step 4: full-table scans on a clustered table — pruning isn't engaging ───────────
SELECT
    query_id,
    query_text,
    partitions_scanned,
    partitions_total
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY(
    RESULT_LIMIT => 10000
))
WHERE partitions_total > 0
  AND partitions_scanned = partitions_total   -- scanned every partition, no pruning
  AND query_text ILIKE '%fact_orders%'
ORDER BY start_time DESC
LIMIT 25;

-- ── Putting it together: a weekly cost-review query worth scheduling as a dashboard ──
SELECT
    warehouse_name,
    DATE_TRUNC('week', start_time) AS week,
    SUM(credits_used_cloud_services + credits_used_compute) AS total_credits,
    COUNT(*) AS query_count,
    SUM(CASE WHEN bytes_spilled_to_remote_storage > 0 THEN 1 ELSE 0 END) AS spilled_queries,
    SUM(CASE WHEN queued_overload_time > 5000 THEN 1 ELSE 0 END) AS queued_queries
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY(RESULT_LIMIT => 10000))
GROUP BY 1, 2
ORDER BY 2 DESC, 3 DESC;
