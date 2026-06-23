-- Secure Data Sharing: sharing data with another team/account without copying it.
--
-- A share grants read access to a live view of the data in the provider account — the
-- consumer never gets a physical copy, which means no ETL pipeline to keep two copies in
-- sync, no extra storage cost, and the provider can revoke access instantly by dropping
-- the share. This replaced a nightly "export to S3 -> re-load into partner's Snowflake"
-- pipeline that was both an ongoing compute cost and a sync-lag source of data
-- disagreements between teams.

-- ── Step 1: create a secure view — never share raw tables directly ──────────────────
-- A secure view hides its query definition from the consumer (DESCRIBE/GET_DDL on it
-- returns nothing useful to them) and only exposes the columns explicitly selected here,
-- which is also where row/column-level filtering for the specific consumer happens.
CREATE OR REPLACE SECURE VIEW v_shared_regional_summary AS
SELECT
    order_date,
    region_id,
    SUM(order_amount) AS gross_revenue,
    COUNT(*) AS order_count
FROM fact_orders
WHERE region_id = 'EU-WEST'   -- this share is scoped to one region's partner team
GROUP BY order_date, region_id;

-- ── Step 2: create the share and grant access to the object ─────────────────────────
CREATE OR REPLACE SHARE eu_west_partner_share;

GRANT USAGE ON DATABASE analytics TO SHARE eu_west_partner_share;
GRANT USAGE ON SCHEMA analytics.public TO SHARE eu_west_partner_share;
GRANT SELECT ON VIEW v_shared_regional_summary TO SHARE eu_west_partner_share;

-- ── Step 3: add the consumer account ──────────────────────────────────────────────────
ALTER SHARE eu_west_partner_share
    ADD ACCOUNTS = ('PARTNER_ORG_ACCOUNT');

-- ── Step 4 (consumer side, run from their account): create a database from the share ─
-- CREATE DATABASE eu_west_data FROM SHARE provider_account.eu_west_partner_share;
-- The consumer can then query eu_west_data.public.v_shared_regional_summary like any
-- other table — no warehouse credits are consumed in the provider's account for
-- consumer queries; the consumer pays for their own compute against the shared data.

-- ── Revoking access is instant and doesn't require a data deletion process ──────────
ALTER SHARE eu_west_partner_share
    REMOVE ACCOUNTS = ('PARTNER_ORG_ACCOUNT');

-- ── Auditing who has access to what ───────────────────────────────────────────────────
SHOW SHARES;
DESCRIBE SHARE eu_west_partner_share;
