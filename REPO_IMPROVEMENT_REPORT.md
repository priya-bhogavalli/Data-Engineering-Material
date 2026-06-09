# Repo Improvement Report — Data-Engineering-Material
**Date:** 2026-06-09 | **Author:** Priya Bhogavalli | **Goal:** SA roles at Databricks/Snowflake/dbt Labs/Confluent · Head of Data at German scale-ups

---

## Executive Summary

The repo currently contains 300+ folders of markdown reference material — key concepts, interview questions, and tool guides. This is valuable as a personal study resource, but it does not function as a portfolio. A hiring manager or SA interviewer who opens this repo sees a reader, not a practitioner.

**The single most impactful change:** Add one working, end-to-end Databricks lakehouse project. That alone will do more for a Databricks SA application than all 300 existing markdown files combined.

---

## Current State Assessment

### What exists
- 300+ tool folders across Cloud, Databases, Data-Processing, Streaming, MLOps, Governance
- Every folder follows the same pattern: `KEY_CONCEPTS.md` + `INTERVIEW_QUESTIONS.md`
- A handful of `Real-World-Architecture` case study markdowns (Netflix, Ecommerce)
- No runnable code of any kind
- No working projects
- No architecture decision records
- No CI/CD pipelines

### What is missing
| Category | Gap |
|----------|-----|
| **Code** | Zero Python files, SQL files, notebooks, or scripts anywhere in the repo |
| **Projects** | No end-to-end runnable project in any technology |
| **Databricks** | No notebooks, no Delta Lake examples, no Unity Catalog, no DLT, no DABs |
| **Snowflake** | No SQL patterns, no Snowpark code, no cost governance queries |
| **dbt** | No dbt project at all — not a single model, test, or macro |
| **Streaming** | No Kafka producer/consumer code, no docker-compose local setup |
| **Architecture** | No ADRs, no runbooks, no diagrams |
| **CI/CD** | No GitHub Actions workflows |

---

## Problem 1 — No Working Code

### Current situation
Every technology in the repo has a `KEY_CONCEPTS.md` and `INTERVIEW_QUESTIONS.md`. There is no executable code anywhere. For example:

- `Core-Data-Engineering/Data-Processing/Databricks/` — 6 markdown files, 0 notebooks
- `Core-Data-Engineering/Data-Warehousing/Snowflake/` — 5 markdown files, 0 SQL files
- `Core-Data-Engineering/Data-Processing/Orchestration/DBT/` — 3 markdown files, 0 dbt models

### Why this is a problem
SA interviews at Databricks, Snowflake, and dbt Labs are hands-on. Interviewers want to see that you have actually built things with the product, not studied it. A repo with 300 "key concepts" docs and zero code signals that the candidate has read a lot but built nothing publicly.

### Fix
Add working code alongside the existing docs. Minimum viable additions:

```
Core-Data-Engineering/Data-Processing/Databricks/
├── existing docs (keep as-is)
└── examples/
    ├── 01_bronze_autoloader.py
    ├── 02_silver_merge.py
    ├── 03_gold_aggregates.py
    └── README.md

Core-Data-Engineering/Data-Warehousing/Snowflake/
├── existing docs (keep as-is)
└── examples/
    ├── clustering_analysis.sql
    ├── warehouse_sizing.sql
    ├── dynamic_data_masking.sql
    └── README.md
```

---

## Problem 2 — No dbt Project

### Current situation
`Core-Data-Engineering/Data-Processing/Orchestration/DBT/` contains:
- `DBT_CONCEPTUAL_OVERVIEW.md`
- `DBT_INTERVIEW_QUESTIONS.md`
- `DBT_KEY_CONCEPTS.md`

There is no dbt project anywhere in the repo — no `dbt_project.yml`, no models, no tests, no macros.

### Why this is a problem
dbt is the core transformation layer for every modern data stack. dbt Labs SA interviews, Databricks SA interviews, and every Head of Data interview at a German scale-up will ask "show me how you structure a dbt project." Having zero dbt code is a visible gap.

### Fix
Create a proper dbt project under a new `projects/` folder:

```
projects/dbt-enterprise-patterns/
├── dbt_project.yml
├── profiles.yml.example
├── models/
│   ├── staging/
│   │   ├── stg_orders.sql
│   │   ├── stg_customers.sql
│   │   └── schema.yml          # sources + not_null/unique tests
│   ├── intermediate/
│   │   └── int_order_items.sql
│   └── marts/
│       ├── fct_orders.sql
│       └── dim_customers.sql
├── tests/
│   └── assert_positive_revenue.sql
├── macros/
│   └── generate_schema_name.sql
└── README.md
```

**Power move:** Deploy `dbt docs generate` output as a GitHub Pages site so the docs are browsable at `priya-bhogavalli.github.io/Data-Engineering-Material/dbt-docs`.

---

## Problem 3 — Databricks Folder Has No Notebooks

### Current situation
The Databricks folder has 6 markdown files including a full feature reference and advanced interview questions. There are no notebooks, no Delta Lake code, and no Unity Catalog examples — despite Priya holding the **Databricks Certified Data Engineer Professional (2026)** certification.

### Why this is a problem
Every Databricks SA interview opens with "walk me through a lakehouse architecture you've built." A Databricks cert with zero visible Databricks code raises questions. The cert is a signal of knowledge — but SA roles require proof of application.

### Fix
Add a medallion architecture project:

```
projects/lakehouse-medallion/
├── notebooks/
│   ├── 01_autoloader_bronze.py       # Streaming ingest with Auto Loader
│   ├── 02_delta_merge_silver.py      # MERGE + schema evolution
│   ├── 03_gold_aggregates.py         # Business-level aggregations
│   ├── 04_unity_catalog_setup.py     # Unity Catalog schema + grants
│   ├── 05_mlflow_experiment.py       # MLflow tracking + model registry
│   └── 06_dlt_pipeline.py            # Delta Live Tables example
├── sql/
│   ├── liquid_clustering_vs_zorder.sql
│   ├── time_travel_queries.sql
│   └── cdf_change_data_feed.sql
├── databricks.yml                     # Databricks Asset Bundle config
└── README.md                          # Architecture diagram + decisions
```

---

## Problem 4 — Snowflake Folder Has No SQL

### Current situation
The Snowflake folder has 5 markdown files. There is no SQL code, no Snowpark example, and no cost governance queries — despite Priya holding **SnowPro Core (2024)** and having production experience managing a 3.7B-row Snowflake migration with 22% cost reduction.

### Why this is a problem
The 22% cost reduction proof point is one of Priya's strongest differentiators. Without supporting SQL patterns, it reads as a claim rather than a demonstration. Snowflake SA interviews expect candidates to show cost governance and performance tuning knowledge with actual queries.

### Fix
Add a cost governance SQL project:

```
projects/snowflake-cost-patterns/
├── sql/
│   ├── 01_micro_partition_pruning.sql    # Clustering analysis queries
│   ├── 02_warehouse_sizing_guide.sql     # Credit consumption by query type
│   ├── 03_materialization_strategy.sql   # Table vs view vs mat. view tradeoffs
│   ├── 04_dynamic_data_masking.sql       # PII protection patterns
│   ├── 05_secure_data_sharing.sql        # Data sharing setup
│   └── 06_query_profiling.sql            # QUERY_HISTORY analysis
├── python/
│   └── snowpark_dataframe_example.py     # Snowpark DataFrame API
└── README.md                             # "How we reduced costs 22%" narrative
```

---

## Problem 5 — Real-World-Architecture Has No Real Architecture

### Current situation
`Real-World-Architecture/` contains:
- `System-Designs/Netflix-Streaming/ARCHITECTURE.md` — a markdown description
- `Cost-Optimization/Ecommerce-Pipeline/CASE_STUDY.md` — a markdown case study
- `Mock-Interviews/README.md` — placeholder
- `Certifications/AWS-Data-Engineer/README.md` — cert study notes

### Why this is a problem
Architecture decision records (ADRs) are the clearest signal of senior engineering thinking. Head of Data and EM interviewers at German scale-ups (Personio, Zalando, Trade Republic) frequently ask "give me an example of a technical decision you've made and how you documented it." Having no ADRs is a gap for Path A roles.

### Fix
Add real ADRs based on decisions Priya has actually made (fully anonymised — no client names):

```
Real-World-Architecture/ADRs/
├── template.md
├── 001-lakehouse-vs-warehouse.md      # When Databricks vs Snowflake
├── 002-batch-vs-streaming.md          # Decision framework with real criteria
├── 003-orchestration-choice.md        # Airflow vs Databricks Workflows vs dbt Cloud
├── 004-data-contract-approach.md      # Schema registry vs code-first contracts
└── 005-unity-catalog-migration.md     # Hive metastore to Unity Catalog
```

Each ADR should follow the format:
- **Status:** Accepted / Superseded
- **Context:** What situation prompted this decision
- **Decision:** What was chosen and why
- **Consequences:** What became easier, what became harder

---

## Problem 6 — No CI/CD for Data Projects

### Current situation
There is a `Supporting-Tools/DevOps-Automation/CI-CD/` folder with CI/CD concept docs. There are no GitHub Actions workflows in the repo at all.

### Why this is a problem
SA and EM interviews increasingly test whether candidates treat data code like software — with tests, linting, and automated validation. A repo with no `.github/workflows/` signals that the candidate knows CI/CD theory but does not apply it to data work.

### Fix
Add minimal but real CI/CD:

```
.github/workflows/
├── dbt-ci.yml          # dbt test + dbt docs on every PR to dbt project
├── python-lint.yml     # Ruff/Black lint on Python files
└── sql-lint.yml        # sqlfluff on SQL files
```

---

## Problem 7 — README Does Not Surface the Right Things

### Current situation
The repo likely has a top-level README that lists all the folder categories. A recruiter who lands on this repo sees a table of contents for 300 study topics.

### Fix
Restructure the README so the first thing visible is the **Projects** section, not the reference library. Suggested README structure:

```markdown
# Data Engineering Portfolio — Priya Bhogavalli

## Projects (start here)
- lakehouse-medallion — Databricks medallion architecture with Delta Lake, Unity Catalog, MLflow
- snowflake-cost-patterns — Production SQL patterns for cost governance and performance tuning
- dbt-enterprise-patterns — Enterprise dbt project with staging/intermediate/marts + CI/CD
- kafka-streaming — Confluent Kafka producer/consumer with Schema Registry + docker-compose

## Reference Library
> 300+ notes on tools, concepts, and interview preparation
[Browse by category →](./Core-Data-Engineering/README.md)

## Certifications
- Databricks Certified Data Engineer Professional (2026)
- SnowPro Core (2024)
- AWS SA Associate (2026)
- Google Data Engineer (2024)
```

---

## Recommended Build Sequence (6 weeks)

| Week | Action | Impact |
|------|--------|--------|
| 1–2 | `projects/lakehouse-medallion/` — Databricks medallion + Unity Catalog + MLflow notebooks | Highest — covers Databricks SA interview opener |
| 3 | `projects/snowflake-cost-patterns/` — SQL patterns + Snowpark + README with "22% cost reduction" narrative | High — backs your strongest proof point with visible code |
| 4 | `projects/dbt-enterprise-patterns/` — dbt project with staging/marts/tests + GitHub Pages docs | High — closes the most visible gap across all SA targets |
| 5 | `Real-World-Architecture/ADRs/` — 4-5 ADRs from real career decisions, anonymised | Medium — differentiates for Path A (Head of Data / EM) interviews |
| 6 | `projects/kafka-streaming/` — docker-compose + Avro producer/consumer + `.github/workflows/` | Medium — closes streaming gap for Confluent conversations |

---

## What to Leave As-Is

The reference docs (KEY_CONCEPTS, INTERVIEW_QUESTIONS) are useful as personal study material. Do not delete them. Instead:
- Move them to a `reference/` subfolder so they do not dominate the first-impression view
- Or keep the structure but update the top-level README to lead with Projects

---

## Summary Table

| Issue | Severity | Effort to fix | Priority |
|-------|----------|---------------|----------|
| No working code anywhere in repo | Critical | Medium | 1 |
| No dbt project | Critical | Medium | 2 |
| Databricks folder has no notebooks | Critical | Medium | 3 |
| Snowflake folder has no SQL | High | Low | 4 |
| No ADRs or architecture decision docs | High | Low | 5 |
| No CI/CD workflows | Medium | Low | 6 |
| README leads with reference library, not projects | Medium | Very low | 7 |
| No Kafka working code | Medium | Medium | 8 |
