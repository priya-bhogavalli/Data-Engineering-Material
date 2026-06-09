# Portfolio Repo Gap Analysis — Priya Bhogavalli
**Date:** 2026-06-09 | **Career targets:** SA at Databricks/Snowflake/dbt/Confluent · Head of Data at German scale-ups

---

## What Hiring Managers at Your Target Companies Look For

| Company | What their SA interviews focus on | What they want to see in a repo |
|---------|----------------------------------|--------------------------------|
| **Databricks** | Delta Lake internals, streaming, Unity Catalog, ML pipelines | Lakehouse from scratch, medallion architecture, MLflow experiments |
| **Snowflake** | Data sharing, Snowpark, performance tuning, cost governance | SnowPro-level patterns — clustering, materialization strategies, DAG orchestration |
| **dbt Labs** | Transformation patterns, testing, lineage, semantic layer | A real dbt project with docs, tests, and sources — not just models |
| **Confluent** | Kafka streams, schema registry, exactly-once semantics | Producer/consumer patterns, KSQL or Flink SQL examples |
| **Personio / German scale-ups (Path A)** | Architecture decisions, team patterns, cost transparency | ADR templates, runbooks, migration decision logs |

---

## What You Have (inferred from resume.md)

✅ 10+ years enterprise experience (real, credible)
✅ Databricks Professional cert 2026
✅ SnowPro Core 2024
✅ AWS SA Associate 2026
✅ Deep Snowflake production work (3.7B rows, 22% cost reduction)
✅ Greenfield Databricks lakehouse (Client 5)
✅ MLOps (SageMaker, Kubeflow)
✅ GenAI hackathon winner 2025

❌ No public code demonstrating any of this
❌ No visible architecture decisions or patterns
❌ No "SA-style" demos that recruiters can run or read in 5 minutes

---

## Priority Additions — Ranked by Impact on Hiring

### Tier 1 — Build these first (highest SA interview ROI)

#### 1. `lakehouse-medallion` — Databricks / Delta Lake reference project
**Why:** Every Databricks SA interview starts here. You built one at Client 5 — make a clean public version.

```
lakehouse-medallion/
├── notebooks/
│   ├── 01_bronze_ingestion.py      # Autoloader, streaming ingest
│   ├── 02_silver_transform.py      # Delta MERGE, schema evolution
│   ├── 03_gold_aggregates.py       # Business-level aggregations
│   └── 04_mlflow_experiment.py     # MLflow tracking + model registry
├── src/
│   ├── delta_utils.py              # Z-ORDER, VACUUM, OPTIMIZE helpers
│   └── schema_registry.py
├── data/                           # Sample synthetic dataset (<=10MB)
├── README.md                       # Architecture diagram + decisions
└── .github/workflows/ci.yml        # Lint + test on push
```

**Databricks-specific things to include:** Unity Catalog schema, Delta time travel query, liquid clustering vs Z-ORDER comparison, CDF (Change Data Feed) example.

---

#### 2. `snowflake-cost-governance` — Snowflake performance & cost patterns
**Why:** SnowPro cert + Client 6 proof points. Make the patterns public. This is what SA interviews at Snowflake test.

```
snowflake-cost-governance/
├── sql/
│   ├── clustering_analysis.sql     # Micro-partition pruning queries
│   ├── warehouse_sizing.sql        # Credit consumption by query type
│   ├── materialization_guide.sql   # Table vs view vs materialized view
│   ├── dynamic_data_masking.sql    # PII protection patterns
│   └── data_sharing_example.sql   # Secure data sharing setup
├── terraform/
│   └── snowflake_warehouse.tf      # IaC for warehouse config
├── dbt/                            # (link to dbt project or subfolder)
└── README.md                       # "22% cost reduction — here's how"
```

**Key angle:** Narrative in README: "On a 3.7B-row migration, we reduced infrastructure costs 22% using these patterns." That maps directly to your verified proof point.

---

#### 3. `dbt-enterprise-patterns` — dbt project with real engineering rigour
**Why:** dbt Labs SA roles and most Head of Data interviews ask about transformation governance. A repo with 0 dbt code is a gap for any SA in the modern data stack.

```
dbt-enterprise-patterns/
├── models/
│   ├── staging/          # Source-aligned, 1:1 with raw tables
│   ├── intermediate/     # Business logic, joins
│   └── marts/            # Dimensional model, finance/product domains
├── tests/
│   ├── schema.yml        # not_null, unique, accepted_values
│   └── custom/           # Custom singular tests
├── macros/
│   └── generate_schema_name.sql   # Multi-env schema routing
├── docs/                 # dbt docs generate output (static site)
├── .github/workflows/
│   └── dbt_ci.yml        # dbt test + dbt docs on PR
└── README.md
```

**Power move:** Deploy `dbt docs serve` output as a GitHub Pages site — SA candidates who do this stand out.

---

### Tier 2 — Add after Tier 1 (differentiators for Path A / EM roles)

#### 4. `adr-templates` — Architecture Decision Records
**Why:** Head of Data / EM interviews at Personio, Zalando, Trade Republic ask "how do you document decisions?" Having a repo with real ADRs signals seniority.

```
adr-templates/
├── 001-lakehouse-vs-warehouse.md   # When to use Databricks vs Snowflake
├── 002-batch-vs-streaming.md       # Decision framework
├── 003-orchestration-choice.md     # Airflow vs Databricks Workflows vs dbt Cloud
├── 004-data-contract-approach.md   # Schema registry vs code-based contracts
└── template.md                     # Blank ADR template
```

---

#### 5. `data-platform-runbook` — Operational patterns for data teams
**Why:** Shows programme ownership, not just coding. Resonates with EM hiring at scale-ups.

```
data-platform-runbook/
├── oncall/
│   ├── pipeline-failure-playbook.md
│   ├── data-quality-incident.md
│   └── sla-breach-escalation.md
├── onboarding/
│   ├── new-engineer-checklist.md
│   └── data-consumer-guide.md
└── governance/
    ├── data-classification.md
    └── pii-handling-policy.md
```

---

#### 6. `kafka-data-pipelines` — Confluent / streaming patterns
**Why:** Confluent SA roles. Not your primary target, but a quick Kafka producer/consumer demo closes a visible gap in your stack.

```
kafka-data-pipelines/
├── python/
│   ├── producer.py       # Avro schema, Schema Registry
│   ├── consumer.py       # Consumer groups, offset management
│   └── ksql_examples.sql # Streaming aggregations
├── docker-compose.yml    # Local Kafka + Schema Registry + Kafka UI
└── README.md
```

---

### Tier 3 — Nice to have (aspirational / FAANG track)

| Project | Why | Effort |
|---------|-----|--------|
| `ml-feature-store` — Feast + SageMaker patterns | Closes MLOps gap for AWS SA interviews | High |
| `data-contracts-demo` — Great Expectations + Soda | Data quality tooling, trending topic | Medium |
| `genai-data-pipeline` — RAG over structured data | Ties to 2025 hackathon win, Databricks Genie relevance | Medium |
| `terraform-data-platform` — IaC for full stack | Shows infra ownership for EM roles | Medium |

---

## What NOT to Build

- A generic "ETL with Python" tutorial repo — already saturated, zero signal
- Kaggle-style ML notebooks — wrong audience for SA/EM roles
- Anything with fake metrics — authenticity is your edge, keep it real
- A repo that is 70% README and 10% code — interviewers clone repos, they expect to run things

---

## Suggested Sequence (6-week plan)

| Week | Action |
|------|--------|
| 1–2 | `lakehouse-medallion` — Databricks medallion + MLflow (Tier 1, highest impact) |
| 3 | `snowflake-cost-governance` — SQL patterns + README narrative linking to your proof points |
| 4 | `dbt-enterprise-patterns` — Transform layer + dbt docs site on GitHub Pages |
| 5 | `adr-templates` — 4–5 real decisions you have made in your career, anonymised |
| 6 | `kafka-data-pipelines` — Docker-compose local setup, Avro examples |

---

## One-Line Summary

Your CV is strong but has nothing for an interviewer to click on. The Tier 1 repos give Databricks and Snowflake SA interviewers concrete evidence of what you claim, in a format they can read in 10 minutes. Build those three first — everything else is a bonus.
