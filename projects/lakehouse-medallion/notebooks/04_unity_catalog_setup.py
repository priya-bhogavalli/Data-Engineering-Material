# Databricks notebook source
# MAGIC %md
# MAGIC # Unity Catalog — Catalog, Schemas, External Location, Grants
# MAGIC
# MAGIC One-time setup notebook that provisions the `lakehouse` catalog used by every other
# MAGIC notebook in this project. Run once per environment (dev/staging/prod target in
# MAGIC `databricks.yml` each point at a separate catalog, so this is safe to re-run — every
# MAGIC statement is `IF NOT EXISTS`).

# COMMAND ----------

dbutils.widgets.text("catalog_name", "lakehouse")
dbutils.widgets.text("storage_credential", "lakehouse_storage_cred")
dbutils.widgets.text("external_location_url", "s3://my-org-lakehouse-bucket/")

catalog_name = dbutils.widgets.get("catalog_name")
storage_credential = dbutils.widgets.get("storage_credential")
external_location_url = dbutils.widgets.get("external_location_url")

# COMMAND ----------

# MAGIC %md
# MAGIC ## External location
# MAGIC
# MAGIC The storage credential (an IAM role for S3, or a managed identity for ADLS) is
# MAGIC created separately by a platform/infra team via Terraform — this notebook only
# MAGIC registers the *external location* that references it, since granting a notebook
# MAGIC the ability to create cloud IAM roles is a wider blast radius than a data engineer
# MAGIC should need.

# COMMAND ----------

spark.sql(f"""
    CREATE EXTERNAL LOCATION IF NOT EXISTS lakehouse_root
    URL '{external_location_url}'
    WITH (STORAGE CREDENTIAL `{storage_credential}`)
    COMMENT 'Root storage for the lakehouse-medallion project'
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Catalog + schemas
# MAGIC
# MAGIC One schema per medallion layer. Keeping bronze/silver/gold as separate schemas
# MAGIC (rather than separate catalogs) means a single `GRANT ... ON CATALOG` can cover
# MAGIC read access to all three for an analyst, while write access stays scoped per-schema
# MAGIC to the pipeline service principal that owns that layer.

# COMMAND ----------

spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog_name} MANAGED LOCATION 'lakehouse_root'")

for schema in ["bronze", "silver", "gold"]:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog_name}.{schema}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Grants
# MAGIC
# MAGIC `analysts` get read-only on Gold only — they should never query Bronze/Silver
# MAGIC directly, since those layers don't carry the data-quality guarantees Gold does.
# MAGIC `data_engineers` get full read/write across all three layers via the pipeline
# MAGIC service principal group.

# COMMAND ----------

spark.sql(f"GRANT USE CATALOG ON CATALOG {catalog_name} TO `analysts`")
spark.sql(f"GRANT USE SCHEMA ON SCHEMA {catalog_name}.gold TO `analysts`")
spark.sql(f"GRANT SELECT ON SCHEMA {catalog_name}.gold TO `analysts`")

spark.sql(f"GRANT ALL PRIVILEGES ON CATALOG {catalog_name} TO `data_engineers`")

# COMMAND ----------

display(spark.sql(f"SHOW GRANTS ON CATALOG {catalog_name}"))
