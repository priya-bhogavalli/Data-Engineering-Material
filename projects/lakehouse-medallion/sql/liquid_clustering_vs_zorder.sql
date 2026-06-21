-- Liquid Clustering vs Z-Order: when to use which, with measurable comparison queries.
--
-- Z-Order (OPTIMIZE ... ZORDER BY) co-locates related data within files based on the
-- column(s) given, but it's a one-shot operation: every time you run OPTIMIZE, it
-- rewrites the *entire* table (or partition) from scratch. That's fine for a table that
-- gets optimized occasionally and doesn't change clustering keys.
--
-- Liquid Clustering (CLUSTER BY) is incremental: new data gets clustered as it's written,
-- and re-clustering only touches files that need it. It also lets you change the
-- clustering columns later without rewriting history. For gold.daily_revenue, which gets
-- overwritten daily and is queried mostly by order_date + currency, Liquid Clustering is
-- the better fit because the clustering key won't need a full-table OPTIMIZE rewrite
-- every single day.

-- ── Liquid Clustering: gold.daily_revenue ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS lakehouse.gold.daily_revenue (
    order_date       DATE,
    currency         STRING,
    gross_revenue    DECIMAL(18,2),
    order_count      BIGINT,
    unique_customers BIGINT,
    avg_order_value  DECIMAL(18,2)
)
CLUSTER BY (order_date, currency);

-- Re-cluster on demand (DLT/streaming writers don't need to call this — it's a
-- maintenance command for tables written via overwrite/append jobs like notebook 03)
OPTIMIZE lakehouse.gold.daily_revenue;

-- ── Z-Order: lakehouse.silver.orders ──────────────────────────────────────────────────
-- Silver is append/merge-heavy with a stable, rarely-changing query pattern
-- (point lookups by customer_id, range scans by order_created_at). A periodic
-- OPTIMIZE ... ZORDER BY run (e.g. nightly, via a scheduled job) is simpler to operate
-- here than Liquid Clustering, and the table is small enough that a full rewrite is cheap.
OPTIMIZE lakehouse.silver.orders
ZORDER BY (customer_id, order_created_at);

-- ── Measuring the impact: files scanned before vs after ───────────────────────────────
-- Run EXPLAIN with a typical Gold query filter and check the "PartitionFilters" /
-- "files pruned" line in the physical plan to confirm clustering is being used for
-- file skipping rather than a full table scan.
EXPLAIN
SELECT *
FROM lakehouse.gold.daily_revenue
WHERE order_date = '2026-06-15' AND currency = 'EUR';

-- DESCRIBE DETAIL exposes clustering columns + file count, useful for a before/after
-- comparison when deciding whether re-clustering is worth the compute cost.
DESCRIBE DETAIL lakehouse.gold.daily_revenue;
