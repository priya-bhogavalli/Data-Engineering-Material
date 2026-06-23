-- Warehouse sizing: the second-largest lever, and the easiest one teams get wrong.
--
-- The default instinct under load is "make the warehouse bigger." That fixes latency but
-- not throughput-per-credit — a query that doesn't parallelize well just finishes faster
-- on a bigger warehouse while burning the same (or more) total credits. Sizing should be
-- driven by measured concurrency and queue depth, not by gut feel during a slow query.

-- ── Step 1: find out if you have a concurrency problem or a per-query size problem ───
-- High queued_overload_time with normal-looking individual query times = you need more
-- concurrent capacity (multi-cluster warehouse), not a bigger warehouse.
SELECT
    warehouse_name,
    DATE_TRUNC('hour', start_time) AS hour,
    SUM(credits_used) AS credits_used,
    SUM(execution_time) / 1000 AS exec_seconds,
    SUM(queued_overload_time) / 1000 AS queued_seconds,
    COUNT(*) AS query_count
FROM TABLE(INFORMATION_SCHEMA.WAREHOUSE_METERING_HISTORY(
    DATE_RANGE_START => DATEADD('day', -7, CURRENT_DATE())
))
GROUP BY 1, 2
ORDER BY 1, 2;

-- ── Step 2: credits per query, by warehouse size — the number that actually matters ──
-- This was the comparison that justified splitting one oversized shared warehouse into
-- workload-specific ones on the migration: the BI dashboard workload (many small,
-- concurrent, sub-second queries) was paying Large-warehouse credit rates for queries
-- that ran identically fast on a Small warehouse. Compute-bound ETL stayed on Large.
SELECT
    warehouse_name,
    warehouse_size,
    COUNT(*) AS query_count,
    SUM(credits_used_cloud_services + credits_used_compute) AS total_credits,
    ROUND(SUM(credits_used_cloud_services + credits_used_compute) / COUNT(*), 4)
        AS avg_credits_per_query
FROM TABLE(INFORMATION_SCHEMA.WAREHOUSE_METERING_HISTORY(
    DATE_RANGE_START => DATEADD('day', -30, CURRENT_DATE())
))
GROUP BY 1, 2
ORDER BY avg_credits_per_query DESC;

-- ── Step 3: auto-suspend tuning ───────────────────────────────────────────────────────
-- Default AUTO_SUSPEND is 600s (10 min). For bursty interactive workloads (BI dashboards
-- queried in short bursts during business hours) this leaves a warehouse idling and
-- billing for most of its runtime. Dropping to 60s was worth roughly a third of the
-- BI warehouse's portion of the overall credit reduction, with no measurable user-facing
-- latency cost since warehouse resume is sub-second for warm caches.
ALTER WAREHOUSE bi_dashboard_wh SET
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE;

-- For the compute-bound ETL warehouse, leave suspend longer — jobs are scheduled close
-- together and frequent suspend/resume cycles would cost more in resume latency than
-- they'd save in idle credits.
ALTER WAREHOUSE etl_batch_wh SET
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE;

-- ── Step 4: multi-cluster for concurrency spikes, not single-warehouse upsizing ──────
-- Scales out (more clusters of the *same* size) rather than up, which keeps
-- credits-per-query constant as concurrency grows instead of paying Large-warehouse
-- rates for queries that don't need Large-warehouse compute.
ALTER WAREHOUSE bi_dashboard_wh SET
    WAREHOUSE_SIZE = 'SMALL'
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 4
    SCALING_POLICY = 'STANDARD';
