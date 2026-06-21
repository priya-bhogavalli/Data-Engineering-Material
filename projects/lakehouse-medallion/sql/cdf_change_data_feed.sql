-- Change Data Feed (CDF) — row-level change tracking for downstream consumers.
--
-- CDF answers a different question than time travel. Time travel asks "what did the
-- whole table look like at version N." CDF asks "exactly which rows changed between
-- version N and N+1, and how (insert/update/delete)." That's what you need when a
-- downstream consumer (another team's pipeline, a reverse-ETL job, a cache invalidation
-- process) needs to react only to what changed, not reprocess the whole table.

-- ── Enable CDF on an existing table ───────────────────────────────────────────────────
ALTER TABLE lakehouse.silver.orders
SET TBLPROPERTIES (delta.enableChangeDataFeed = true);

-- New tables can enable it at creation time instead:
-- CREATE TABLE ... TBLPROPERTIES (delta.enableChangeDataFeed = true)

-- ── Read changes since a given version ────────────────────────────────────────────────
-- table_changes() returns one row per change, plus _change_type
-- ('insert' | 'update_preimage' | 'update_postimage' | 'delete') and _commit_version /
-- _commit_timestamp so a consumer can checkpoint where it left off.
SELECT *
FROM table_changes('lakehouse.silver.orders', 10, 20)
ORDER BY _commit_version, _commit_timestamp;

-- Or by timestamp range, for a consumer that checkpoints on time rather than version
SELECT *
FROM table_changes('lakehouse.silver.orders', '2026-06-14 00:00:00', '2026-06-15 00:00:00');

-- ── Worked example: propagate only changed customers to gold.customer_ltv ───────────
-- Instead of recomputing the full aggregate (notebook 03's approach, fine at current
-- volume), a CDF-based incremental version would look like this once customer count
-- grows large enough that a full recompute gets expensive:
WITH changed_orders AS (
    SELECT DISTINCT customer_id
    FROM table_changes('lakehouse.silver.orders', 10, 20)
    WHERE _change_type IN ('insert', 'update_postimage')
)
MERGE INTO lakehouse.gold.customer_ltv AS target
USING (
    SELECT
        o.customer_id,
        SUM(o.order_amount)      AS lifetime_value,
        COUNT(*)                 AS lifetime_orders,
        MAX(o.order_created_at)  AS last_order_at
    FROM lakehouse.silver.orders o
    INNER JOIN changed_orders c ON o.customer_id = c.customer_id
    GROUP BY o.customer_id
) AS recomputed
ON target.customer_id = recomputed.customer_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;

-- ── Caveat worth raising in an SA conversation ───────────────────────────────────────
-- CDF retains change data for the same period as the table's history (governed by
-- delta.logRetentionDuration / VACUUM). If a downstream consumer falls behind that
-- retention window, it loses the ability to resume incrementally and must re-snapshot
-- the table — this is the main operational risk to flag when recommending CDF.
