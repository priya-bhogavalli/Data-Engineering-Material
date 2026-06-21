-- Delta Lake Time Travel — auditing, debugging, and recovering from bad writes.
--
-- Every write to a Delta table creates a new version with a transaction log entry.
-- Time travel lets you query (or restore) any prior version without needing a separate
-- backup/snapshot process — this is one of the concrete things to point to when an SA
-- conversation asks "what does Delta give you that plain Parquet doesn't."

-- ── Full version history ──────────────────────────────────────────────────────────────
DESCRIBE HISTORY lakehouse.silver.orders;

-- ── Query a specific version (e.g. to diff against current state) ────────────────────
SELECT *
FROM lakehouse.silver.orders VERSION AS OF 42;

-- ── Query as of a timestamp — useful when you know roughly when something broke ──────
SELECT *
FROM lakehouse.silver.orders TIMESTAMP AS OF '2026-06-10 09:00:00';

-- ── Worked example: a bad MERGE corrupted gold.customer_ltv this morning ─────────────
-- Step 1 — find the version immediately before the bad write
SELECT version, timestamp, operation, operationParameters
FROM (DESCRIBE HISTORY lakehouse.gold.customer_ltv)
WHERE timestamp < '2026-06-15 06:00:00'
ORDER BY version DESC
LIMIT 1;

-- Step 2 — diff row counts between the suspect version and the one before it, to
-- confirm the bad write is what you think it is before restoring
SELECT
    (SELECT COUNT(*) FROM lakehouse.gold.customer_ltv VERSION AS OF 17) AS before_count,
    (SELECT COUNT(*) FROM lakehouse.gold.customer_ltv VERSION AS OF 18) AS after_count;

-- Step 3 — restore. RESTORE rewrites the table back to that version's state and logs
-- the restore itself as a new version, so the bad write is still visible in history
-- (compliance-friendly: nothing is silently erased).
RESTORE TABLE lakehouse.gold.customer_ltv TO VERSION AS OF 17;

-- ── Guardrail: VACUUM removes old file versions, which breaks time travel ────────────
-- Default retention is 7 days. Don't run VACUUM with a shorter RETAIN period on tables
-- where time-travel-based recovery is part of your incident-response process.
VACUUM lakehouse.gold.customer_ltv RETAIN 168 HOURS;  -- 7 days, the safe default
