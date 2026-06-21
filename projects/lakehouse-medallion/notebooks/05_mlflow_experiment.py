# Databricks notebook source
# MAGIC %md
# MAGIC # MLflow — Churn Risk Model, Tracked + Registered
# MAGIC
# MAGIC Trains a simple churn-risk classifier on `gold.customer_ltv` (the `segment` column
# MAGIC built in notebook 03 is the label) and logs the run with MLflow Tracking, then
# MAGIC registers the model in Unity Catalog so the Gold pipeline can reference a stable
# MAGIC `models:/lakehouse.gold.churn_risk_model/Production` URI instead of a notebook-local
# MAGIC variable.

# COMMAND ----------

import mlflow
from pyspark.sql import functions as F
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

mlflow.set_registry_uri("databricks-uc")

dbutils.widgets.text("gold_table", "lakehouse.gold.customer_ltv")
dbutils.widgets.text("model_name", "lakehouse.gold.churn_risk_model")

gold_table = dbutils.widgets.get("gold_table")
model_name = dbutils.widgets.get("model_name")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Features
# MAGIC
# MAGIC `churned` is collapsed to a binary target from the 3-way `segment` field
# MAGIC (active/at_risk -> 0, churned -> 1) — for a first model iteration, a binary
# MAGIC classifier is easier to evaluate and compare against a trivial baseline than a
# MAGIC 3-class model, and the business question ("will this customer churn") is binary.

# COMMAND ----------

pdf = (
    spark.table(gold_table)
    .withColumn("churned", (F.col("segment") == "churned").cast("int"))
    .select(
        "lifetime_value",
        "lifetime_orders",
        "days_since_last_order",
        "churned",
    )
    .toPandas()
)

X = pdf[["lifetime_value", "lifetime_orders", "days_since_last_order"]]
y = pdf["churned"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Train + log
# MAGIC
# MAGIC `mlflow.sklearn.autolog()` captures params, the trained model, and a model
# MAGIC signature automatically — we still log custom metrics explicitly because autolog's
# MAGIC default metric set is tuned for regression/generic sklearn estimators and doesn't
# MAGIC include F1, which matters more than accuracy here given the class imbalance
# MAGIC (churned customers are a minority).

# COMMAND ----------

mlflow.sklearn.autolog(log_models=False)

with mlflow.start_run(run_name="churn_risk_rf_v1") as run:
    model = RandomForestClassifier(
        n_estimators=200, max_depth=6, class_weight="balanced", random_state=42
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    accuracy = accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds)

    mlflow.log_metric("test_accuracy", accuracy)
    mlflow.log_metric("test_f1", f1)

    signature = mlflow.models.infer_signature(X_train, model.predict(X_train))
    model_info = mlflow.sklearn.log_model(
        model, artifact_path="model", signature=signature
    )

    print(f"Run {run.info.run_id}: accuracy={accuracy:.3f} f1={f1:.3f}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Register in Unity Catalog
# MAGIC
# MAGIC Only promote to a registered version if F1 clears a minimum bar — this is a
# MAGIC placeholder gate; in production this threshold would be tracked over time and
# MAGIC re-validated, not hardcoded, but it illustrates the pattern: training logs every
# MAGIC run, registration is conditional on a model actually being good enough to serve.

# COMMAND ----------

MIN_F1 = 0.55

if f1 >= MIN_F1:
    registered = mlflow.register_model(model_info.model_uri, model_name)
    print(f"Registered {model_name} version {registered.version}")
else:
    print(f"F1 {f1:.3f} below threshold {MIN_F1} — not registering this run")
