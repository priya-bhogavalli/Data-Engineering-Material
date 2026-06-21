# Lakehouse Medallion — Databricks Reference Project

A working bronze → silver → gold pipeline built on Delta Lake and Unity Catalog, with two
parallel implementations (hand-written notebooks and a declarative DLT pipeline) and
supporting Delta Lake patterns (Liquid Clustering, time travel, Change Data Feed).

## Why two implementations of the same pipeline?

Most lakehouse write-ups show one "correct" way to build a medallion pipeline. In
practice the right answer depends on the team:

| | Notebooks 01–03 | DLT Pipeline (06) |
|---|---|---|
| Orchestration | Databricks Workflow runs each notebook as a task | DLT manages task ordering and retries itself |
| Merge logic | Hand-written `foreachBatch` + `MERGE INTO` | `dlt.apply_changes` (built-in CDC primitive) |
| Data quality | Manual `.filter()` calls, no automatic metrics | Declarative `@dlt.expect_*`, surfaced in the DLT UI |
| Control | Full control over retry/merge semantics | Less boilerplate, less control |
| Best for | Teams that need fine-grained control (custom SCD logic, complex merge conditions) | Teams that want quality metrics + lineage out of the box with less code |

Being able to recommend either, and explain the tradeoff, is closer to what an SA
conversation actually requires than picking one and defending it as universally correct.

## Architecture

```
                 ┌─────────────────┐
  Cloud Storage  │   Auto Loader    │
  (JSON orders) ─┤  (cloudFiles)    │
                 └────────┬─────────┘
                          ▼
              ┌───────────────────────┐
              │   bronze.raw_orders   │  permissive, schema-evolving, append-only
              └───────────┬───────────┘
                          ▼ MERGE INTO (dedup on order_id, late-arrival aware)
              ┌───────────────────────┐
              │    silver.orders      │  enforced schema, quality-gated, one row/order_id
              └───────────┬───────────┘
                          ▼ batch overwrite (CREATE OR REPLACE)
              ┌───────────────────────┬───────────────────────┐
              │  gold.daily_revenue   │  gold.customer_ltv     │
              └───────────────────────┴───────────┬───────────┘
                                                    ▼
                                       MLflow churn-risk model
                                    (registered in Unity Catalog)
```

## What's in here

```
notebooks/
├── 01_autoloader_bronze.py      Streaming ingest, schema evolution
├── 02_delta_merge_silver.py     Dedup + idempotent MERGE upsert
├── 03_gold_aggregates.py        Daily revenue + customer LTV/segmentation
├── 04_unity_catalog_setup.py    Catalog/schema/external location/grants
├── 05_mlflow_experiment.py      Churn model, tracked + conditionally registered
└── 06_dlt_pipeline.py           Same medallion flow, DLT-declarative

sql/
├── liquid_clustering_vs_zorder.sql   When to use which, with EXPLAIN-based verification
├── time_travel_queries.sql            Audit/debug/restore workflow, worked incident example
└── cdf_change_data_feed.sql           Incremental downstream propagation pattern

databricks.yml    Asset Bundle: notebook job + DLT pipeline, 3 targets (dev/staging/prod)
```

## Key decisions (and why)

- **Auto Loader over a periodic batch job for Bronze** — incremental file discovery
  without listing the whole directory, and Bronze's own checkpoint means no separate
  state store is needed.
- **`MERGE INTO` over append-only for Silver** — makes job re-runs after a failure
  idempotent. The merge condition (`s.order_updated_at > t.order_updated_at`) also
  protects against an out-of-order replay overwriting a newer record.
- **Liquid Clustering for `gold.daily_revenue`, Z-Order for `silver.orders`** — Gold gets
  overwritten daily with an unpredictable row count per day (bad fit for static date
  partitioning); Liquid Clustering reclusters incrementally without a full rewrite.
  Silver's query pattern is stable, so a periodic `OPTIMIZE ... ZORDER BY` is simpler to
  operate and the table is cheap to fully rewrite.
- **Gold computed as full overwrite, not incremental** — at current volume, recomputing
  Gold from Silver on every run is simpler to reason about than maintaining incremental
  aggregate state. `cdf_change_data_feed.sql` shows the incremental alternative for when
  volume grows enough to justify the added complexity.
- **MLflow model registration gated on a metric threshold** — every training run is
  logged, but only models that clear a minimum F1 get registered, so the registry stays a
  list of "models that were good enough to consider serving," not every experiment.

## Running this locally / in a workspace

1. Deploy with the Databricks CLI: `databricks bundle deploy -t dev`
2. Run the setup notebook once: `databricks bundle run medallion_pipeline -t dev` (the
   `04_unity_catalog_setup` notebook is not yet wired into the job graph — run it manually
   the first time per environment, since catalog/schema provisioning is a one-time step,
   not part of the daily pipeline)
3. Run the pipeline: `databricks bundle run medallion_pipeline -t dev`
4. Or run the DLT alternative: `databricks bundle run dlt_medallion_pipeline -t dev`

## Related reference material in this repo

- [`Core-Data-Engineering/Data-Processing/Databricks/`](../../Core-Data-Engineering/Data-Processing/Databricks/) — concept docs and interview questions this project puts into practice
