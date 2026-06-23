-- Micro-partition pruning: the single biggest lever on a 3.7B-row fact table.
--
-- Snowflake automatically organizes data into 50-500MB micro-partitions and tracks
-- min/max values per column per partition in metadata. A query that filters on a
-- well-clustered column can skip scanning partitions entirely — the difference between
-- this working and not working on a table this size is the difference between a
-- multi-minute query and a sub-second one.

-- ── Step 1: check current clustering health ───────────────────────────────────────────
-- clustering_depth close to 1 = well clustered. Anything climbing into double digits on
-- a frequently-filtered column means pruning is degrading and partitions are scattered.
SELECT SYSTEM$CLUSTERING_INFORMATION(
    'fact_orders',
    '(order_date, region_id)'
);

-- ── Step 2: confirm pruning is actually happening for the real query pattern ─────────
-- Run EXPLAIN and look at "partitionsScanned" vs "partitionsTotal" in the output —
-- this is the number that actually proves a clustering decision worked, not a guess.
EXPLAIN USING TEXT
SELECT region_id, SUM(order_amount)
FROM fact_orders
WHERE order_date BETWEEN '2026-06-01' AND '2026-06-30'
  AND region_id = 'EU-WEST'
GROUP BY region_id;

-- Query profile metadata (run after the query, via QUERY_HISTORY) gives the same
-- numbers historically, useful for a before/after comparison without re-running queries:
SELECT
    query_id,
    query_text,
    partitions_scanned,
    partitions_total,
    ROUND(partitions_scanned / NULLIF(partitions_total, 0) * 100, 1) AS pct_scanned,
    total_elapsed_time / 1000 AS elapsed_seconds,
    bytes_scanned / POWER(1024, 3) AS gb_scanned
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())
WHERE query_text ILIKE '%fact_orders%'
ORDER BY start_time DESC
LIMIT 20;

-- ── Step 3: add a clustering key when natural insert order doesn't match query pattern ─
-- This was the actual fix on the 3.7B-row migration: source data arrived ordered by
-- ingestion batch, not by order_date — every "last 30 days" query (the overwhelming
-- majority of traffic) was scanning the whole table. Re-clustering on (order_date,
-- region_id) cut scanned bytes for that query shape by ~90%, which was the largest
-- single contributor to the overall 22% warehouse-credit reduction.
ALTER TABLE fact_orders CLUSTER BY (order_date, region_id);

-- Automatic re-clustering runs as a background serverless task billed separately from
-- warehouse compute (shows up as "Automatic Clustering" in METERING_HISTORY) — factor
-- this into the cost comparison, it's not free, it's just billed differently.
SELECT *
FROM TABLE(INFORMATION_SCHEMA.AUTOMATIC_CLUSTERING_HISTORY(
    DATE_RANGE_START => DATEADD('day', -30, CURRENT_DATE()),
    TABLE_NAME => 'FACT_ORDERS'
));
