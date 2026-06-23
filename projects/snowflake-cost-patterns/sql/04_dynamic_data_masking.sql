-- Dynamic Data Masking: PII protection that doesn't require duplicating tables or data.
--
-- A masking policy is defined once and attached to a column; what a query returns
-- depends on the calling role, evaluated at query time. This avoids the common
-- anti-pattern of maintaining a separate "masked" copy of a table for analysts — which
-- doubles storage cost and inevitably drifts out of sync with the source.

-- ── Step 1: define the masking policy ─────────────────────────────────────────────────
-- CURRENT_ROLE() is checked at query execution time, not at policy-creation time, so
-- role membership changes take effect immediately without re-applying anything.
CREATE OR REPLACE MASKING POLICY mask_email AS (val STRING) RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() IN ('PII_VIEWER', 'ACCOUNTADMIN') THEN val
        ELSE REGEXP_REPLACE(val, '^(.)(.*)(@.*)$', '\\1***\\3')  -- j***@example.com
    END;

CREATE OR REPLACE MASKING POLICY mask_full AS (val STRING) RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() IN ('PII_VIEWER', 'ACCOUNTADMIN') THEN val
        ELSE '***MASKED***'
    END;

-- ── Step 2: attach to columns ──────────────────────────────────────────────────────────
ALTER TABLE dim_customers MODIFY COLUMN email
    SET MASKING POLICY mask_email;

ALTER TABLE dim_customers MODIFY COLUMN national_id
    SET MASKING POLICY mask_full;

-- ── Step 3: verify masking actually applies for an unprivileged role ────────────────
USE ROLE analyst_readonly;
SELECT customer_id, email, national_id FROM dim_customers LIMIT 5;
-- expected: email shows as "j***@example.com", national_id shows as "***MASKED***"

USE ROLE pii_viewer;
SELECT customer_id, email, national_id FROM dim_customers LIMIT 5;
-- expected: both columns unmasked

-- ── Tag-based masking: apply one policy to every column carrying a given tag ────────
-- For a table with many PII columns, tagging is more maintainable than attaching
-- policies column-by-column, and it scales to new columns/tables automatically as long
-- as whoever adds them also adds the tag — which is the actual operational risk: tag
-- governance, not the masking mechanism itself.
CREATE OR REPLACE TAG pii_classification;

ALTER TABLE dim_customers MODIFY COLUMN phone_number
    SET TAG pii_classification = 'contact_info';

ALTER TAG pii_classification SET MASKING POLICY mask_email;  -- conceptually; in practice
-- you'd associate the policy via ALTER TAG ... SET MASKING POLICY per data type, since
-- a single masking policy's return type must match every column it's attached to.

-- ── Auditing what's masked and for whom ───────────────────────────────────────────────
SELECT *
FROM TABLE(INFORMATION_SCHEMA.POLICY_REFERENCES(
    POLICY_NAME => 'mask_email'
));
