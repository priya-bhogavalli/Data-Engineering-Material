# Databricks Real-Project Interview Questions

> Grounded in an actual Kafka/Flink → Databricks migration delivered for a maritime IoT telemetry
> platform (1,000+ marine engines / ATUs). Unlike the concept-drill questions in
> [`DATABRICKS_INTERVIEW_QUESTIONS.md`](./DATABRICKS_INTERVIEW_QUESTIONS.md), these are the questions an
> interviewer asks when they want to hear about a real production engagement — "tell me about a project,"
> not "explain the API." Use this bank for PS/Solutions Architect, senior DE, and migration-focused
> interviews.

## Project Context (read this first)

**Client:** Maritime technology company (marine engine monitoring platform), Germany.
**Scale:** 1,000+ marine engines (ATUs — Asset Telemetry Units) streaming continuous sensor data.
**Problem:** A brittle, self-managed Kafka/Flink stack causing daily firefighting, ~1-hour data delays
across the fleet, and outages costing ~$20K/hour in vessel off-hire costs.
**Role:** Ingestion & Data Pipeline Architect — designed the target architecture, won the RFP, and led the
first 3 months of delivery (MVP).
**Migration:** Kafka/Flink (self-managed) + InfluxCloud/Kielo (hot/cold split) + Neo4j (metadata) →
AWS MSK (managed Kafka) + Databricks (Delta Lake, Unity Catalog, Structured Streaming).

---

## Table of Contents
1. [Tell me about a Databricks project](#1-tell-me-about-a-databricks-project)
2. [Have you built a medallion architecture?](#2-have-you-built-a-medallion-architecture)
3. [Where was Databricks deployed and how was it set up?](#3-where-was-databricks-deployed-and-how-was-it-set-up)
4. [How did you handle secrets in Databricks?](#4-how-did-you-handle-secrets-in-databricks)
5. [Walk me through your CI/CD approach on Databricks](#5-walk-me-through-your-cicd-approach-on-databricks)
6. [How did you use Unity Catalog?](#6-how-did-you-use-unity-catalog)
7. [How did you ingest data into bronze?](#7-how-did-you-ingest-data-into-bronze)
8. [Kafka vs Databricks Streaming — when do you use which?](#8-kafka-vs-databricks-streaming--when-do-you-use-which)

---

### 1. Tell me about a Databricks project

**Answer:**
I was the Ingestion & Data Pipeline Architect on a maritime transformation programme monitoring 1,000+
marine engines. The legacy platform ran on a self-managed Kafka/Flink stack that caused daily firefighting,
1-hour data delays across the fleet, and outages costing ~$20K/hour in vessel off-hire costs — the client's
first digital transformation attempt had already failed, so trust was low going in.

I designed the target architecture: replace the self-managed Kafka/Flink stack with AWS MSK (managed
Kafka) feeding Databricks, collapse the InfluxCloud/Kielo hot-cold storage split into a single Delta Lake
layer, and replace Neo4j metadata lookups with Unity Catalog. I won the RFP as lead architect for the
ingestion workstream, then led the first 3 months of delivery: full legacy assessment, Databricks
provisioned across dev/staging/prod, bronze ingestion live from the asset metadata system, and the first
Flink pipeline migrated to Databricks Structured Streaming with zero data loss.

The main lesson from that engagement: when a client's first transformation has already failed,
architectural decisions need to be justified by risk reduction and reversibility first, technical elegance
second. Leading with "here's why this won't fail like last time" mattered as much as the technical design
itself.

---

### 2. Have you built a medallion architecture?

**Answer:**
Yes — designed for maritime IoT time-series data specifically, not a generic template.

- **Bronze:** raw ATU telemetry (every sensor reading), asset configuration/engine metadata, and partner
  events. Append-only, exactly-once from the managed Kafka (MSK) source, full history retained — this
  layer is the immutable record of what was actually received.
- **Silver:** VDIs (Virtual Data Integrations) — cleaned, standardised, validated sensor readings with
  business rules applied. Written with idempotent MERGE so re-runs don't duplicate data, schema enforced,
  SLA-monitored since downstream consumers depend on freshness.
- **Gold:** ML-ready feature tables for predictive maintenance models, plus published, access-controlled
  data products consumed by downstream applications (a maintenance-assist tool, a data product API, and an
  AI assistant). Optimised for consumption and governed through Unity Catalog.

Medallion architecture matters here because it separates "what did we receive" (bronze, immutable, cheap
insurance against upstream mistakes) from "what can we trust" (silver, validated) from "what's ready to
serve" (gold, curated and access-controlled) — each layer has different SLAs, different consumers, and
different failure-recovery semantics. That separation is what let this specific programme replace two
fragmented storage systems (a hot/cold split plus a graph database for metadata) with one coherent layered
model.

---

### 3. Where was Databricks deployed and how was it set up?

**Answer:**
AWS, using the **workspace-per-environment** pattern — three separate workspaces (dev, staging, prod), each
with its own Unity Catalog metastore, IAM role bindings, and S3 bucket paths. That gives clean environment
isolation: a pipeline promoted from staging to prod shares no compute or metadata with staging, so a bad
UC grant or a runaway job in one environment can't touch another.

The reason a metastore-per-workspace (rather than one shared metastore across environments) mattered here:
governance configuration — grants, row filters, column masks — could be validated in staging before it
ever touched prod, the same way you'd test infrastructure-as-code changes before applying them live.

Cluster management was owned by a dedicated infrastructure team rather than the data engineering team — a
deliberate separation of concerns on an enterprise engagement. Pipelines consumed compute through **job
clusters** (spun up per Workflow run, terminated after) instead of always-on all-purpose clusters, so there
was no idle spend between runs. The workspace and cluster-policy baseline came from an internal Databricks
accelerator/CoE template, which gave a validated starting point rather than designing from zero.

---

### 4. How did you handle secrets in Databricks?

**Answer:**
Two layers working together: **AWS Secrets Manager** as the source of truth for secret values (with
rotation), and **Databricks Secret Scopes** backed by Secrets Manager references so pipeline code never
touches a raw credential.

Concretely: a secret scope is created against the AWS Secrets Manager backend, and pipeline code retrieves
values at runtime with `dbutils.secrets.get(scope="...", key="...")`. The actual secret value is redacted
in notebook output and logs automatically — Databricks replaces it with `[REDACTED]` if it's ever printed.
Rotation is AWS Secrets Manager's job, not the pipeline's; because the scope only holds a *reference*, a
rotated secret is picked up on the next `dbutils.secrets.get()` call with no pipeline redeploy needed.

The general principle this demonstrates: never let cloud-native secret storage and platform-native secret
access diverge — pick one system of record (Secrets Manager) and have the platform (Databricks) reference
it rather than duplicating secret values in two places.

---

### 5. Walk me through your CI/CD approach on Databricks

**Answer:**
Clean split between infrastructure and pipeline lifecycles, both orchestrated by GitLab CI:

- **Terraform** owned infrastructure provisioning — workspaces, Unity Catalog resources (catalogs,
  schemas, grants), S3 bucket permissions, IAM roles, cluster policies. Infrastructure-as-code checked into
  GitLab, applied via CI pipeline with a plan/apply gate.
- **Databricks Asset Bundles (DABs)** owned pipeline and job definitions — `databricks.yml` bundle files
  declaring Workflows, notebook paths, cluster references, and environment-variable overrides per target
  environment. DABs handled dev→staging→prod promotion of job configurations as versioned, reviewable
  YAML rather than click-ops changes in the workspace UI.
- **GitLab CI/CD** orchestrated both: a PR triggers a Terraform plan against staging and a DABs deploy to
  staging, automated tests run, then a manual approval gate before Terraform apply and DABs deploy to prod.

The separation matters: Terraform changes (a new IAM role, a UC grant) and pipeline changes (a new
Workflow task, a notebook edit) have different blast radii and different review needs, so keeping them as
two independent, composable CI stages — rather than one monolithic deploy script — let each be reviewed and
rolled back on its own.

---

### 6. How did you use Unity Catalog?

**Answer:**
Fully provisioned from day one, not retrofitted later — that's the recommendation I'd always make now,
since retrofitting governance onto a platform that's already running production pipelines is much harder
than building it in from the start.

Key elements:
- **Three-level namespace** (`catalog.schema.table`, e.g. `client_prod.silver.orders`) — this is Unity
  Catalog's core structural change from the legacy Hive metastore's two-level `schema.table` model. The
  extra `catalog` level lets you isolate environments or business domains inside a single metastore,
  cleanly separate PII/regulated data into its own catalog, and reference tables unambiguously across
  workspaces that share a metastore.
- **Row filters and column masks** applied at the gold layer for sensitive columns — governance enforced
  at the layer closest to consumption, not scattered across every downstream query.
- **Automatic lineage** captured across all Delta tables, end to end — no manual documentation of "what
  feeds what," which matters for both debugging (trace a bad value back to its source) and compliance
  audits.
- **Access controlled via UC grants**, not workspace-level ACLs — grants are metastore-scoped and follow
  the table wherever it's queried from, instead of being tied to a specific workspace's permission model.

---

### 7. How did you ingest data into bronze?

**Answer:**
Source data landed in S3, and bronze ingestion used **Auto Loader** (`cloudFiles` format) rather than a
manually scheduled batch read of the S3 prefix.

Auto Loader is Databricks' incremental file-ingestion mechanism: it uses cloud-native notification services
(or efficient directory listing as a fallback) to discover new files without re-listing the entire source
prefix on every run, tracks which files have already been processed via a checkpoint, and supports schema
inference plus schema evolution — new columns appearing in the source don't break the pipeline, they get
picked up automatically (or flagged, depending on configuration).

That combination is what made it the right fit here: at the scale of 1,000+ engines continuously emitting
telemetry, a full S3 listing on every run would get progressively slower and more expensive, and manual
file-tracking logic is exactly the kind of undifferentiated bookkeeping you don't want to own. Auto Loader
turns "ingest whatever new files landed since last time, exactly once, with schema drift handled" into a
few lines of streaming read configuration instead of a hand-rolled cursor/watermark system.

---

### 8. Kafka vs Databricks Streaming — when do you use which?

**Answer:**
They solve different problems, and this migration used both rather than one replacing the other outright.

**Kafka (AWS MSK, managed)** is the real-time **fan-out** layer: durable, ordered, replayable log that
lets many independent consumers read the same event stream at their own pace, decoupled from the producer
and from each other. That's the right tool when the requirement is "get this event to N different
downstream systems reliably and in order," regardless of what any one consumer does with it.

**Databricks Structured Streaming** solves a different problem: turning that stream into **queryable,
governed, ACID-consistent data** — i.e., taking events off the log and landing them in Delta tables with
exactly-once semantics, schema enforcement, time travel, and Unity Catalog governance, so analysts, ML
pipelines, and downstream data products can query "the current state of the data" rather than replaying a
raw event log themselves.

In this migration specifically: the client's *problem* wasn't Kafka — it was a self-managed, brittle
Kafka/Flink deployment where Flink jobs were the failure point (unstable, causing the data gaps that led to
1-hour delays and outages). The fix was to keep Kafka's fan-out role but make it managed (AWS MSK instead
of self-hosted), and replace the unstable Flink processing layer with Databricks Structured Streaming
writing to Delta Lake with exactly-once guarantees. So the practical framing for this question: Kafka
answers "how do multiple systems reliably receive this event stream," Databricks Structured Streaming
answers "how do we turn that stream into trustworthy, queryable, governed data" — most real architectures
need both, not one instead of the other.

---

## See Also
- [`DATABRICKS_INTERVIEW_QUESTIONS.md`](./DATABRICKS_INTERVIEW_QUESTIONS.md) — concept-level Q&A with code
  (Delta Lake mechanics, cluster types, Feature Store, monitoring, etc.)
- [`DATABRICKS_ADVANCED_INTERVIEW_QUESTIONS.md`](./DATABRICKS_ADVANCED_INTERVIEW_QUESTIONS.md) — advanced
  performance/troubleshooting scenarios
- [`DATABRICKS_KEY_CONCEPTS.md`](./DATABRICKS_KEY_CONCEPTS.md) — conceptual primer
- `Real-World-Architecture/Mock-Interviews/README.md` — mock interview practice framework
