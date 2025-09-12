# MLflow - Comprehensive Interview Questions

## Table of Contents
1. [Core Concepts](#core-concepts)
2. [MLflow Tracking](#mlflow-tracking)
3. [MLflow Projects](#mlflow-projects)
4. [MLflow Models](#mlflow-models)
5. [MLflow Registry](#mlflow-registry)
6. [Data Engineering Integration](#data-engineering-integration)
7. [Deployment & Production](#deployment--production)
8. [Real-World Scenarios](#real-world-scenarios)

---

## Core Concepts

### 1. What is MLflow and how does it solve ML lifecycle management challenges?

**Answer:**
MLflow is an open-source platform for managing the complete machine learning lifecycle, including experimentation, reproducibility, deployment, and model registry.

**Key Components:**
- **MLflow Tracking**: Experiment tracking and metrics logging
- **MLflow Projects**: Reproducible ML code packaging
- **MLflow Models**: Model packaging and deployment
- **MLflow Registry**: Centralized model store with versioning

**ML Lifecycle Challenges Solved:**
```python
# Before MLflow - Manual tracking
experiment_results = {
    "model_v1": {"accuracy": 0.85, "params": {"lr": 0.01}},
    "model_v2": {"accuracy": 0.87, "params": {"lr": 0.001}},
    # Manual spreadsheet tracking, no reproducibility
}

# With MLflow - Automated tracking
import mlflow
import mlflow.sklearn

with mlflow.start_run():
    # Automatic parameter and metric logging
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_param("n_estimators", 100)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    
    # Log metrics
    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)
    
    # Log model
    mlflow.sklearn.log_model(model, "random_forest_model")
```

### 2. Explain MLflow's architecture and how it integrates with data engineering pipelines.

**Answer:**
**MLflow Architecture:**

```
Data Sources → Data Pipeline → MLflow Tracking → Model Registry → Deployment
     ↓             ↓              ↓                ↓              ↓
Raw Data → ETL/Feature → Experiments → Versioned → Production
          Engineering                   Models      Serving
```

**Integration Points:**
```python
# Data engineering pipeline with MLflow integration
import mlflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def feature_engineering_task():
    # Data processing
    features = process_raw_data()
    
    # Log data quality metrics
    with mlflow.start_run(run_name="feature_engineering"):
        mlflow.log_metric("feature_count", len(features.columns))
        mlflow.log_metric("data_quality_score", calculate_quality_score(features))
        
        # Save processed features
        mlflow.log_artifact("features.parquet")
    
    return features

def model_training_task():
    # Load features from MLflow
    features = mlflow.artifacts.download_artifacts("features.parquet")
    
    # Train and track model
    with mlflow.start_run(run_name="model_training"):
        model = train_model(features)
        mlflow.sklearn.log_model(model, "production_model")
        
        # Register model
        mlflow.register_model(
            model_uri=f"runs:/{mlflow.active_run().info.run_id}/production_model",
            name="customer_churn_model"
        )

# Airflow DAG integration
dag = DAG('ml_pipeline_with_mlflow')
feature_task = PythonOperator(task_id='feature_engineering', python_callable=feature_engineering_task)
training_task = PythonOperator(task_id='model_training', python_callable=model_training_task)
feature_task >> training_task
```

### 3. How do you set up MLflow tracking for experiment management?

**Answer:**
**MLflow Tracking Setup:**

```python
# Basic tracking setup
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Set tracking URI (local, remote, or cloud)
mlflow.set_tracking_uri("http://mlflow-server:5000")
mlflow.set_experiment("customer_segmentation")

def train_and_track_model(params):
    with mlflow.start_run():
        # Log parameters
        mlflow.log_params(params)
        
        # Train model
        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Log metrics
        mlflow.log_metric("accuracy", accuracy_score(y_test, y_pred))
        mlflow.log_metric("precision", precision_score(y_test, y_pred, average='weighted'))
        mlflow.log_metric("recall", recall_score(y_test, y_pred, average='weighted'))
        
        # Log model
        mlflow.sklearn.log_model(
            model, 
            "model",
            registered_model_name="customer_segmentation_model"
        )
        
        # Log artifacts
        mlflow.log_artifact("feature_importance.png")
        mlflow.log_artifact("confusion_matrix.png")
        
        return model

# Hyperparameter tuning with tracking
param_grid = [
    {"n_estimators": 50, "max_depth": 5},
    {"n_estimators": 100, "max_depth": 10},
    {"n_estimators": 200, "max_depth": 15}
]

for params in param_grid:
    train_and_track_model(params)
```

### 4. How do you use MLflow Projects for reproducible ML workflows?

**Answer:**
**MLflow Projects** package ML code in a reusable and reproducible format.

**Project Structure:**
```yaml
# MLproject file
name: customer_churn_prediction

conda_env: conda.yaml

entry_points:
  main:
    parameters:
      data_path: {type: string, default: "data/customers.csv"}
      max_depth: {type: int, default: 10}
      n_estimators: {type: int, default: 100}
    command: "python train.py --data-path {data_path} --max-depth {max_depth} --n-estimators {n_estimators}"
  
  evaluate:
    parameters:
      model_uri: {type: string}
      test_data: {type: string}
    command: "python evaluate.py --model-uri {model_uri} --test-data {test_data}"
```

```yaml
# conda.yaml
name: churn_prediction
channels:
  - conda-forge
dependencies:
  - python=3.8
  - scikit-learn=1.0
  - pandas=1.3
  - numpy=1.21
  - pip
  - pip:
    - mlflow>=1.20
```

```python
# train.py
import argparse
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", type=str, required=True)
    parser.add_argument("--max-depth", type=int, default=10)
    parser.add_argument("--n-estimators", type=int, default=100)
    args = parser.parse_args()
    
    with mlflow.start_run():
        # Load data
        data = pd.read_csv(args.data_path)
        X, y = prepare_features(data)
        
        # Log parameters
        mlflow.log_param("max_depth", args.max_depth)
        mlflow.log_param("n_estimators", args.n_estimators)
        
        # Train model
        model = RandomForestClassifier(
            max_depth=args.max_depth,
            n_estimators=args.n_estimators
        )
        model.fit(X, y)
        
        # Log model
        mlflow.sklearn.log_model(model, "model")

if __name__ == "__main__":
    main()
```

**Running Projects:**
```bash
# Run locally
mlflow run . -P max_depth=15 -P n_estimators=200

# Run from Git repository
mlflow run https://github.com/company/ml-project.git -P data_path=s3://bucket/data.csv

# Run on remote compute
mlflow run . --backend kubernetes --backend-config k8s-config.json
```

---

## MLflow Models

### 5. How do you package and deploy models using MLflow Models?

**Answer:**
**MLflow Models** provides a standard format for packaging ML models from any library.

**Model Packaging:**
```python
import mlflow
import mlflow.sklearn
import mlflow.pyfunc

# Standard model logging
with mlflow.start_run():
    model = train_sklearn_model()
    mlflow.sklearn.log_model(
        model, 
        "sklearn_model",
        registered_model_name="production_model"
    )

# Custom PyFunc model for complex preprocessing
class CustomerChurnModel(mlflow.pyfunc.PythonModel):
    def __init__(self, preprocessor, model):
        self.preprocessor = preprocessor
        self.model = model
    
    def predict(self, context, model_input):
        # Custom preprocessing
        processed_input = self.preprocessor.transform(model_input)
        
        # Model prediction
        predictions = self.model.predict(processed_input)
        
        # Post-processing
        return self.format_predictions(predictions)
    
    def format_predictions(self, predictions):
        return [{"churn_probability": float(p)} for p in predictions]

# Log custom model
with mlflow.start_run():
    custom_model = CustomerChurnModel(preprocessor, trained_model)
    mlflow.pyfunc.log_model(
        "custom_model",
        python_model=custom_model,
        artifacts={"preprocessor": "preprocessor.pkl"}
    )
```

**Model Deployment Options:**
```python
# Local serving
import mlflow.pyfunc

# Load model
model = mlflow.pyfunc.load_model("models:/production_model/1")

# Make predictions
predictions = model.predict(new_data)

# REST API serving
# mlflow models serve -m models:/production_model/1 -p 5000

# Docker deployment
# mlflow models build-docker -m models:/production_model/1 -n my-model

# Cloud deployment
import mlflow.deployments

# Deploy to AWS SageMaker
deployment = mlflow.deployments.create_deployment(
    name="churn-model",
    model_uri="models:/production_model/1",
    target_uri="sagemaker",
    config={
        "instance_type": "ml.m5.large",
        "instance_count": 1
    }
)
```

### 6. How do you implement MLflow Model Registry for model versioning and lifecycle management?

**Answer:**
**Model Registry** provides centralized model store with versioning, stage transitions, and annotations.

**Model Registration:**
```python
import mlflow
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Register model from run
model_uri = f"runs:/{run_id}/model"
model_version = mlflow.register_model(
    model_uri=model_uri,
    name="customer_churn_model"
)

# Add model description and tags
client.update_registered_model(
    name="customer_churn_model",
    description="Random Forest model for predicting customer churn"
)

client.set_registered_model_tag(
    name="customer_churn_model",
    key="team",
    value="data-science"
)
```

**Model Lifecycle Management:**
```python
# Transition model through stages
def promote_model(model_name, version, stage):
    client.transition_model_version_stage(
        name=model_name,
        version=version,
        stage=stage,
        archive_existing_versions=True
    )

# Model validation before promotion
def validate_and_promote_model(model_name, version):
    # Load model
    model_uri = f"models:/{model_name}/{version}"
    model = mlflow.pyfunc.load_model(model_uri)
    
    # Run validation tests
    validation_results = run_model_validation(model)
    
    if validation_results["accuracy"] > 0.85:
        # Promote to staging
        promote_model(model_name, version, "Staging")
        
        # Add validation annotations
        client.set_model_version_tag(
            name=model_name,
            version=version,
            key="validation_accuracy",
            value=str(validation_results["accuracy"])
        )
        
        # Run A/B testing
        if run_ab_test(model_uri):
            # Promote to production
            promote_model(model_name, version, "Production")
    else:
        # Archive poor performing model
        promote_model(model_name, version, "Archived")

# Automated model monitoring
def monitor_production_model():
    # Get current production model
    production_model = client.get_latest_versions(
        name="customer_churn_model",
        stages=["Production"]
    )[0]
    
    # Monitor performance
    current_performance = evaluate_model_performance(production_model.source)
    
    if current_performance["accuracy"] < 0.80:
        # Trigger model retraining
        trigger_model_retraining()
        
        # Alert team
        send_alert("Model performance degraded", current_performance)
```

---

## Data Engineering Integration

### 7. How do you integrate MLflow with Apache Airflow for ML pipeline orchestration?

**Answer:**
**MLflow + Airflow Integration** for end-to-end ML pipeline automation:

```python
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
import mlflow
from datetime import datetime, timedelta

# DAG configuration
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'ml_pipeline_with_mlflow',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
)

def extract_features(**context):
    """Extract and engineer features"""
    execution_date = context['execution_date']
    
    with mlflow.start_run(run_name=f"feature_extraction_{execution_date}"):
        # Extract features from data warehouse
        features = extract_from_warehouse(execution_date)
        
        # Feature engineering
        processed_features = engineer_features(features)
        
        # Log feature statistics
        mlflow.log_metric("feature_count", len(processed_features.columns))
        mlflow.log_metric("row_count", len(processed_features))
        
        # Save features as artifact
        feature_path = f"/tmp/features_{execution_date}.parquet"
        processed_features.to_parquet(feature_path)
        mlflow.log_artifact(feature_path)
        
        return feature_path

def train_model(**context):
    """Train ML model"""
    feature_path = context['task_instance'].xcom_pull(task_ids='extract_features')
    
    with mlflow.start_run(run_name=f"model_training_{context['execution_date']}"):
        # Load features
        features = pd.read_parquet(feature_path)
        X, y = prepare_training_data(features)
        
        # Train model
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X, y)
        
        # Evaluate model
        accuracy = model.score(X_test, y_test)
        mlflow.log_metric("accuracy", accuracy)
        
        # Log model
        model_info = mlflow.sklearn.log_model(
            model, 
            "model",
            registered_model_name="daily_churn_model"
        )
        
        return model_info.model_uri

def validate_model(**context):
    """Validate model performance"""
    model_uri = context['task_instance'].xcom_pull(task_ids='train_model')
    
    # Load model
    model = mlflow.pyfunc.load_model(model_uri)
    
    # Run validation
    validation_results = run_validation_suite(model)
    
    # Log validation results
    with mlflow.start_run(run_name=f"model_validation_{context['execution_date']}"):
        for metric, value in validation_results.items():
            mlflow.log_metric(f"validation_{metric}", value)
    
    # Decide on model promotion
    if validation_results["accuracy"] > 0.85:
        return "promote_model"
    else:
        return "archive_model"

def promote_model(**context):
    """Promote model to production"""
    model_uri = context['task_instance'].xcom_pull(task_ids='train_model')
    
    # Register model version
    model_version = mlflow.register_model(
        model_uri=model_uri,
        name="production_churn_model"
    )
    
    # Transition to production
    client = MlflowClient()
    client.transition_model_version_stage(
        name="production_churn_model",
        version=model_version.version,
        stage="Production"
    )

# Define tasks
extract_task = PythonOperator(
    task_id='extract_features',
    python_callable=extract_features,
    dag=dag
)

train_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag
)

validate_task = PythonOperator(
    task_id='validate_model',
    python_callable=validate_model,
    dag=dag
)

promote_task = PythonOperator(
    task_id='promote_model',
    python_callable=promote_model,
    dag=dag
)

# Set task dependencies
extract_task >> train_task >> validate_task >> promote_task
```

### 8. How do you implement MLflow with Spark for distributed ML training?

**Answer:**
**MLflow + Spark Integration** for scalable ML training:

```python
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
import mlflow
import mlflow.spark

# Initialize Spark session
spark = SparkSession.builder \
    .appName("MLflow_Spark_Training") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

def distributed_training_with_mlflow():
    with mlflow.start_run():
        # Load data from data lake
        df = spark.read.parquet("s3://data-lake/customer-data/")
        
        # Log data statistics
        mlflow.log_metric("total_records", df.count())
        mlflow.log_metric("feature_count", len(df.columns))
        
        # Feature engineering
        feature_cols = [col for col in df.columns if col != 'churn']
        assembler = VectorAssembler(
            inputCols=feature_cols,
            outputCol="features"
        )
        
        df_features = assembler.transform(df)
        
        # Split data
        train_df, test_df = df_features.randomSplit([0.8, 0.2], seed=42)
        
        # Train model
        rf = RandomForestClassifier(
            featuresCol="features",
            labelCol="churn",
            numTrees=100,
            maxDepth=10
        )
        
        # Log parameters
        mlflow.log_param("num_trees", 100)
        mlflow.log_param("max_depth", 10)
        mlflow.log_param("train_records", train_df.count())
        
        # Fit model
        model = rf.fit(train_df)
        
        # Make predictions
        predictions = model.transform(test_df)
        
        # Evaluate model
        evaluator = BinaryClassificationEvaluator(
            labelCol="churn",
            rawPredictionCol="rawPrediction",
            metricName="areaUnderROC"
        )
        
        auc = evaluator.evaluate(predictions)
        mlflow.log_metric("auc", auc)
        
        # Log model
        mlflow.spark.log_model(
            model,
            "spark_model",
            registered_model_name="spark_churn_model"
        )
        
        return model

# Hyperparameter tuning with MLflow
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator

def hyperparameter_tuning_with_tracking():
    # Create parameter grid
    param_grid = ParamGridBuilder() \
        .addGrid(rf.numTrees, [50, 100, 200]) \
        .addGrid(rf.maxDepth, [5, 10, 15]) \
        .build()
    
    # Cross validator
    cv = CrossValidator(
        estimator=rf,
        estimatorParamMaps=param_grid,
        evaluator=evaluator,
        numFolds=3
    )
    
    # Track each fold
    with mlflow.start_run(run_name="hyperparameter_tuning"):
        cv_model = cv.fit(train_df)
        
        # Log best parameters
        best_model = cv_model.bestModel
        mlflow.log_param("best_num_trees", best_model.getNumTrees())
        mlflow.log_param("best_max_depth", best_model.getMaxDepth())
        
        # Log best score
        mlflow.log_metric("best_cv_score", max(cv_model.avgMetrics))
        
        # Log model
        mlflow.spark.log_model(
            best_model,
            "best_model",
            registered_model_name="tuned_churn_model"
        )
```

---

## Real-World Scenarios

### 9. Design an end-to-end MLOps pipeline using MLflow for a recommendation system.

**Answer:**
**MLOps Architecture:**
```
Data Sources → Feature Store → MLflow Tracking → Model Registry → Deployment → Monitoring
     ↓             ↓              ↓                ↓              ↓           ↓
User Events → Features → Experiments → Versioned → A/B Testing → Performance
Product Data           → Training    → Models     → Serving     → Feedback
```

**Implementation:**
```python
# Feature engineering pipeline
class RecommendationFeaturePipeline:
    def __init__(self):
        self.mlflow_client = MlflowClient()
    
    def extract_features(self, start_date, end_date):
        with mlflow.start_run(run_name="feature_extraction"):
            # Extract user behavior features
            user_features = self.extract_user_features(start_date, end_date)
            item_features = self.extract_item_features()
            interaction_features = self.extract_interactions(start_date, end_date)
            
            # Log feature statistics
            mlflow.log_metric("user_count", len(user_features))
            mlflow.log_metric("item_count", len(item_features))
            mlflow.log_metric("interaction_count", len(interaction_features))
            
            # Save to feature store
            feature_store_path = self.save_to_feature_store(
                user_features, item_features, interaction_features
            )
            
            mlflow.log_artifact(feature_store_path)
            return feature_store_path

# Model training pipeline
class RecommendationModelTraining:
    def __init__(self):
        self.experiment_name = "recommendation_system"
        mlflow.set_experiment(self.experiment_name)
    
    def train_collaborative_filtering(self, feature_path, params):
        with mlflow.start_run(run_name="collaborative_filtering"):
            # Load features
            features = self.load_features(feature_path)
            
            # Log parameters
            mlflow.log_params(params)
            
            # Train model
            model = self.train_als_model(features, params)
            
            # Evaluate model
            metrics = self.evaluate_model(model, features)
            mlflow.log_metrics(metrics)
            
            # Log model
            mlflow.spark.log_model(
                model,
                "collaborative_filtering_model",
                registered_model_name="recommendation_cf_model"
            )
            
            return model
    
    def train_content_based(self, feature_path, params):
        with mlflow.start_run(run_name="content_based"):
            # Similar implementation for content-based model
            pass
    
    def train_hybrid_model(self, cf_model_uri, cb_model_uri, params):
        with mlflow.start_run(run_name="hybrid_model"):
            # Load individual models
            cf_model = mlflow.spark.load_model(cf_model_uri)
            cb_model = mlflow.spark.load_model(cb_model_uri)
            
            # Create hybrid model
            hybrid_model = HybridRecommendationModel(cf_model, cb_model, params)
            
            # Log hybrid model
            mlflow.pyfunc.log_model(
                "hybrid_model",
                python_model=hybrid_model,
                registered_model_name="recommendation_hybrid_model"
            )

# Model deployment and serving
class RecommendationModelServing:
    def __init__(self):
        self.client = MlflowClient()
    
    def deploy_model_for_ab_testing(self, model_name, version):
        # Deploy challenger model
        challenger_deployment = mlflow.deployments.create_deployment(
            name=f"{model_name}_challenger_v{version}",
            model_uri=f"models:/{model_name}/{version}",
            target_uri="kubernetes",
            config={
                "resources": {"requests": {"cpu": "500m", "memory": "1Gi"}},
                "replicas": 2
            }
        )
        
        # Configure traffic splitting
        self.configure_traffic_split(
            champion_deployment="recommendation_model_champion",
            challenger_deployment=challenger_deployment,
            traffic_split={"champion": 90, "challenger": 10}
        )
        
        return challenger_deployment
    
    def monitor_ab_test(self, champion_uri, challenger_uri):
        # Collect metrics from both models
        champion_metrics = self.collect_model_metrics(champion_uri)
        challenger_metrics = self.collect_model_metrics(challenger_uri)
        
        # Log comparison metrics
        with mlflow.start_run(run_name="ab_test_comparison"):
            mlflow.log_metrics({
                "champion_ctr": champion_metrics["ctr"],
                "challenger_ctr": challenger_metrics["ctr"],
                "champion_revenue": champion_metrics["revenue"],
                "challenger_revenue": challenger_metrics["revenue"]
            })
            
            # Statistical significance test
            significance_result = self.statistical_significance_test(
                champion_metrics, challenger_metrics
            )
            
            mlflow.log_metric("p_value", significance_result["p_value"])
            mlflow.log_param("is_significant", significance_result["significant"])
            
            # Promotion decision
            if significance_result["significant"] and challenger_metrics["ctr"] > champion_metrics["ctr"]:
                self.promote_challenger_to_champion(challenger_uri)

# Monitoring and feedback loop
class RecommendationModelMonitoring:
    def __init__(self):
        self.client = MlflowClient()
    
    def monitor_model_performance(self):
        # Get production model
        production_model = self.client.get_latest_versions(
            name="recommendation_hybrid_model",
            stages=["Production"]
        )[0]
        
        # Collect real-time metrics
        current_metrics = self.collect_production_metrics()
        
        # Log monitoring metrics
        with mlflow.start_run(run_name="model_monitoring"):
            mlflow.log_metrics(current_metrics)
            
            # Check for model drift
            drift_score = self.detect_model_drift(production_model.source)
            mlflow.log_metric("drift_score", drift_score)
            
            # Performance degradation check
            if current_metrics["ctr"] < 0.02 or drift_score > 0.3:
                self.trigger_model_retraining()
                self.send_alert("Model performance degraded")
    
    def trigger_model_retraining(self):
        # Trigger retraining pipeline
        airflow_trigger_dag("recommendation_model_training")
        
        # Log retraining trigger
        with mlflow.start_run(run_name="retraining_trigger"):
            mlflow.log_param("trigger_reason", "performance_degradation")
            mlflow.log_param("timestamp", datetime.now().isoformat())
```

This comprehensive MLflow interview guide covers all aspects from basic tracking to advanced MLOps pipelines, showing how MLflow integrates with data engineering workflows for complete ML lifecycle management.