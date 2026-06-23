-- Table vs View vs Materialized View: choosing the right one is a cost decision, not
-- just a modeling one. Each re-executes the underlying query on every read (view), pays
-- once at write time (table), or pays incrementally to stay in sync (materialized view).

-- ── View: cheap to maintain, expensive if queried often ───────────────────────────────
-- Fine for a report queried a handful of times a day. Bad for a dashboard polled every
-- few seconds, or for any query feeding into a wider warehouse-killing chain of joins.
CREATE OR REPLACE VIEW v_daily_region_revenue AS
SELECT
    order_date,
    region_id,
    SUM(order_amount) AS gross_revenue,
    COUNT(*) AS order_count
FROM fact_orders
GROUP BY order_date, region_id;

-- ── Materialized View: Snowflake keeps it incrementally up to date automatically ────
-- Right choice when: query is read-heavy relative to base-table write frequency, the
-- aggregation is simple enough for Snowflake to maintain incrementally, and staleness
-- of a few minutes is acceptable. This was used for the BI dashboard's top-line revenue
-- tile — queried constantly, recomputing it as a view on every page load was a
-- meaningful chunk of the BI warehouse's credit burn before the switch.
CREATE OR REPLACE MATERIALIZED VIEW mv_daily_region_revenue AS
SELECT
    order_date,
    region_id,
    SUM(order_amount) AS gross_revenue,
    COUNT(*) AS order_count
FROM fact_orders
GROUP BY order_date, region_id;

-- Materialized views bill for the background maintenance compute (visible in
-- METERING_HISTORY under "Materialized Views") — that cost only nets out as a win when
-- read frequency clearly outweighs base-table write frequency. Check both sides before
-- converting a view:
SELECT
    DATE_TRUNC('day', start_time) AS day,
    SUM(credits_used) AS mv_maintenance_credits
FROM TABLE(INFORMATION_SCHEMA.METERING_HISTORY(
    DATE_RANGE_START => DATEADD('day', -14, CURRENT_DATE())
))
WHERE service_type = 'MATERIALIZED_VIEW'
GROUP BY 1
ORDER BY 1;

-- ── Table (CTAS / scheduled task): right choice for expensive, infrequently-refreshed
-- aggregations where "good enough" staleness is hours, not minutes — e.g. a monthly
-- finance reconciliation table. Pay the compute once on a schedule, every read after
-- that is a flat table scan with zero recomputation cost.
CREATE OR REPLACE TABLE t_monthly_finance_recon AS
SELECT
    DATE_TRUNC('month', order_date) AS month,
    region_id,
    SUM(order_amount) AS gross_revenue,
    SUM(CASE WHEN status = 'refunded' THEN order_amount ELSE 0 END) AS refunded_amount
FROM fact_orders
GROUP BY 1, 2;

-- Refreshed by a scheduled task rather than a materialized view, since finance recon
-- only needs to run once a day and a daily TASK is simpler to audit/version than
-- relying on Snowflake's automatic MV refresh cadence.
CREATE OR REPLACE TASK refresh_monthly_finance_recon
    WAREHOUSE = etl_batch_wh
    SCHEDULE = 'USING CRON 0 6 * * * Europe/Berlin'
AS
    CREATE OR REPLACE TABLE t_monthly_finance_recon AS
    SELECT
        DATE_TRUNC('month', order_date) AS month,
        region_id,
        SUM(order_amount) AS gross_revenue,
        SUM(CASE WHEN status = 'refunded' THEN order_amount ELSE 0 END) AS refunded_amount
    FROM fact_orders
    GROUP BY 1, 2;

-- ── Decision summary ───────────────────────────────────────────────────────────────────
-- View                 : low read frequency, always-fresh required, simple/cheap query
-- Materialized View     : high read frequency, minutes-level freshness OK, simple agg
-- Table + scheduled task: high read frequency, hours-level freshness OK, complex/expensive query
