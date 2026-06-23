# dbt Enterprise Patterns

A staging → intermediate → marts dbt project demonstrating the structural patterns that
come up in every dbt Labs / Databricks / Head-of-Data interview: layered models, source
freshness, schema + singular tests, a custom schema-naming macro, and CI that runs
`dbt build` on every PR.

## Why this exists alongside the other two projects

This project is the SQL/dbt-native version of the same transformation logic built two
different ways elsewhere in this repo:

- `fct_orders` here is the same table referenced throughout
  [`../snowflake-cost-patterns`](../snowflake-cost-patterns/) — that project documents
  the cost/performance work done *on* this table; this project is what *builds* it.
- `dim_customers`'s `lifetime_value`/`segment` logic mirrors
  [`../lakehouse-medallion/notebooks/03_gold_aggregates.py`](../lakehouse-medallion/notebooks/03_gold_aggregates.py)
  — same business rule, expressed in dbt/SQL instead of PySpark, deliberately, to show
  the same problem solved on two different engines.

## Layer structure

```
models/
├── staging/              one model per source table, 1:1 with raw, light casting only
│   ├── stg_orders.sql
│   ├── stg_customers.sql
│   ├── stg_order_items.sql
│   ├── _sources.yml      source definitions + freshness checks
│   └── schema.yml        column tests: unique, not_null, accepted_values, relationships
│
├── intermediate/         ephemeral — exists to keep marts SQL readable, never queried directly
│   └── int_order_items_aggregated.sql
│
└── marts/                the contract with downstream consumers — materialized as tables
    ├── fct_orders.sql
    ├── dim_customers.sql
    └── schema.yml

tests/
└── assert_positive_revenue.sql   singular test: cross-column business rule that
                                   doesn't fit generic schema-test syntax

macros/
└── generate_schema_name.sql      custom schema naming so the same model lands in a
                                   predictably-named schema across every environment
```

## Key decisions (and why)

- **Staging = view, intermediate = ephemeral, marts = table** (set per-folder in
  `dbt_project.yml`, not per-model) — staging is a thin, frequently-changing
  pass-through that doesn't justify storage cost; intermediate exists purely for SQL
  readability and has no consumer of its own; marts are the stable contract other teams
  query, so predictable performance matters more than compute cost there.
- **`relationships` test from `stg_order_items` to `stg_orders` set to `severity: warn`,
  not error** — a late-arriving order header is an expected race condition in a
  streaming-ingested system, not a data-quality failure that should block a CI run.
- **`order_amount` kept as the revenue source of truth in `fct_orders`, with
  `line_items_total` alongside it as a reconciliation signal** — rather than picking
  whichever number is more convenient, both are exposed so a gap (discount, partial
  refund, upstream data issue) is visible to whoever queries the fact table, not silently
  reconciled away in the transformation layer.
- **Custom `generate_schema_name` macro** — dbt's default behavior concatenates target
  schema + custom schema, so the same model lands in a differently-named schema per
  environment. The override here makes the custom schema (`staging`, `marts`) the actual
  schema name everywhere except CI, where the default suffixed behavior is kept
  deliberately to avoid concurrent CI runs colliding on the same schema.

## Running it

```bash
cd projects/dbt-enterprise-patterns
cp profiles.yml.example ~/.dbt/profiles.yml   # then fill in real credentials
dbt deps
dbt build           # runs models + tests in dependency order
dbt docs generate && dbt docs serve
```

CI (`.github/workflows/dbt-ci.yml` at the repo root) runs `dbt build` against an
isolated, per-run schema on every PR touching this project, and publishes
`dbt docs generate` output to GitHub Pages on merge to `main`.

## Related reference material in this repo

- [`Core-Data-Engineering/Data-Processing/Orchestration/DBT/`](../../Core-Data-Engineering/Data-Processing/Orchestration/DBT/) — concept docs and interview questions this project puts into practice
