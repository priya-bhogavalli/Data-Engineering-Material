# Snowflake Cost Patterns — How We Reduced Costs 22%

Production SQL patterns from a 3.7B-row Snowflake migration where the post-migration
focus shifted from "does it work" to "what is this costing us" — resulting in a 22%
reduction in warehouse credit consumption. This project documents the specific queries
used to find and fix the cost drivers, not just the general concepts.

## The investigation, in order

Cost work on a table this size doesn't start with guessing — it starts with measuring.
The order below is the order the actual investigation happened in, because each step's
findings determined where to look next.

### 1. Where are the credits actually going? (`06_query_profiling.sql`)

Started with `QUERY_HISTORY`, ranked by `execution_count * avg_duration` rather than by
single-query duration. **The top cost driver wasn't the slow analyst queries everyone
assumed it was** — it was a dashboard refresh job mis-scheduled to run every 60 seconds
instead of every hour, each run a cheap query individually, but 1,440 cheap queries a day
adds up.

### 2. Is pruning even working? (`01_micro_partition_pruning.sql`)

`fact_orders` was clustered by ingestion order, not by the column nearly every query
filtered on (`order_date`). Every "last 30 days" query — the majority of traffic — was
scanning the full table. Adding a clustering key on `(order_date, region_id)` cut scanned
bytes for that query shape by roughly 90%. **This was the single largest contributor to
the 22% reduction.**

### 3. Is warehouse sizing matched to workload shape? (`02_warehouse_sizing_guide.sql`)

One shared warehouse was serving both the BI dashboard (many small, concurrent,
sub-second queries) and batch ETL (few large, compute-bound queries) — sized for the ETL
workload, which meant every dashboard query was paying Large-warehouse credit rates for
work that ran identically fast on Small. Splitting into workload-specific warehouses,
each multi-cluster-scaled instead of upsized, and tightening `AUTO_SUSPEND` on the bursty
BI warehouse from 600s to 60s, was the second-largest contributor.

### 4. Are we paying to recompute things we should be caching? (`03_materialization_strategy.sql`)

The dashboard's top-line revenue tile was a view re-aggregating the fact table on every
page load. Converting it to a materialized view (acceptable staleness: a few minutes)
moved that cost from "every page load" to "incremental background maintenance," which is
strictly cheaper once read frequency clearly exceeds write frequency — verified by
comparing `METERING_HISTORY` for the MV's maintenance cost against what the view's
recomputation was costing before.

### 5 & 6. Security patterns that came along for the ride (`04_dynamic_data_masking.sql`, `05_secure_data_sharing.sql`)

Not cost items directly, but part of the same migration: dynamic data masking replaced a
maintained "masked copy" table (extra storage + a sync pipeline that was itself a
recurring compute cost), and secure data sharing replaced a nightly export-and-reload
pipeline to a partner account with a live, zero-copy share.

### Snowpark example (`python/snowpark_dataframe_example.py`)

A cohort-retention report that used to pull the full fact table to a Python worker for
pandas processing — paying for both Snowflake warehouse compute *and* a separate compute
worker, plus the network transfer between them. Rewritten with the Snowpark DataFrame
API so the whole computation stays inside Snowflake; only the final aggregated result (a
few thousand rows) ever leaves.

## What's in here

```
sql/
├── 01_micro_partition_pruning.sql     Clustering health checks + the actual fix
├── 02_warehouse_sizing_guide.sql      Concurrency vs size diagnosis, auto-suspend tuning
├── 03_materialization_strategy.sql    View vs materialized view vs scheduled table
├── 04_dynamic_data_masking.sql        Role-based PII masking, column + tag-based
├── 05_secure_data_sharing.sql         Zero-copy sharing, replacing an export/reload pipeline
└── 06_query_profiling.sql             Where the credits actually go — the starting point

python/
└── snowpark_dataframe_example.py      In-warehouse cohort retention, no client-side pull
```

## Honest caveats

- The exact 22% figure is specific to that migration's workload mix and starting state —
  presented here as the outcome of this investigation, not as a number every Snowflake
  account should expect to replicate.
- Automatic clustering and materialized view maintenance both bill separately from
  warehouse compute. Every "fix" above was verified against `METERING_HISTORY` to confirm
  it was a net reduction, not a cost shifted from one line item to another.

## Related reference material in this repo

- [`Core-Data-Engineering/Data-Warehousing/Snowflake/`](../../Core-Data-Engineering/Data-Warehousing/Snowflake/) — concept docs and interview questions this project puts into practice
