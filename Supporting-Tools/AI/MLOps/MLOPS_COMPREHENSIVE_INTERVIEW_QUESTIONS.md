# MLOps Interview Questions for Data Engineering & Machine Learning

## 📋 Table of Contents

1. [Core Concepts Questions (1-15)](#core-concepts-questions-1-15)
2. [Model Development & Training (16-30)](#model-development--training-16-30)
3. [Model Deployment & Serving (31-45)](#model-deployment--serving-31-45)
4. [Monitoring & Observability (46-60)](#monitoring--observability-46-60)
5. [Data Management & Pipelines (61-75)](#data-management--pipelines-61-75)
6. [Infrastructure & Scaling (76-90)](#infrastructure--scaling-76-90)
7. [Governance & Compliance (91-100)](#governance--compliance-91-100)

---

## 🎯 **Introduction**

MLOps (Machine Learning Operations) combines machine learning, DevOps, and data engineering to streamline the ML lifecycle from development to production. For data engineers, MLOps provides essential frameworks for building scalable, reliable, and maintainable ML systems.

**Why MLOps is Critical for Data Engineers:**
- **Automation**: Automated ML pipelines and deployment processes
- **Scalability**: Infrastructure for large-scale ML workloads
- **Reliability**: Monitoring, testing, and quality assurance for ML systems
- **Collaboration**: Bridge between data science and engineering teams
- **Governance**: Model versioning, lineage, and compliance management

---

## Core Concepts Questions (1-15)

### 1. What are the key components of an MLOps architecture and how do they interact?
**Answer**: 
MLOps architecture encompasses the entire ML lifecycle with integrated tooling and processes.

**Key Components:**
- **Data Pipeline**: Data ingestion, processing, and feature engineering
- **Model Training**: Experiment tracking, hyperparameter tuning, model training
- **Model Registry**: Version control and metadata management for models
- **Model Serving**: Deployment infrastructure for model inference
- **Monitoring**: Performance, drift, and operational monitoring
- **Orchestration**: Workflow management and automation
- **Infrastructure**: Compute, storage, and networking resources

```python
# MLOps Pipeline Example using MLflow and Kubeflow
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from kubeflow import dsl
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

class MLOpsPipeline:
    def __init__(self, experiment_name="customer_churn_prediction"):
        self.experiment_name = experiment_name
        self.client = MlflowClient()
        mlflow.set_experiment(experiment_name)
    
    def data_preprocessing(self, data_path):
        """Data preprocessing component"""
        # Load and preprocess data
        df = pd.read_csv(data_path)
        
        # Feature engineering
        df['tenure_months'] = df['tenure'] * 12
        df['monthly_charges_per_service'] = df['monthly_charges'] / df['num_services']
        
        # Handle categorical variables
        categorical_features = ['gender', 'partner', 'dependents', 'phone_service']
        df_encoded = pd.get_dummies(df, columns=categorical_features)
        
        # Split features and target
        X = df_encoded.drop(['customer_id', 'churn'], axis=1)
        y = df_encoded['churn']
        
        return train_test_split(X, y, test_size=0.2, random_state=42)
    
    def train_model(self, X_train, y_train, X_test, y_test, hyperparameters):
        """Model training component with experiment tracking"""
        with mlflow.start_run() as run:
            # Log hyperparameters
            mlflow.log_params(hyperparameters)
            
            # Train model
            model = RandomForestClassifier(**hyperparameters)
            model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            
            # Log metrics
            mlflow.log_metrics({
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall
            })
            
            # Log model
            mlflow.sklearn.log_model(
                model, 
                "model",
                registered_model_name="customer_churn_classifier"
            )
            
            # Log artifacts
            feature_importance = pd.DataFrame({
                'feature': X_train.columns,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            feature_importance.to_csv("feature_importance.csv", index=False)
            mlflow.log_artifact("feature_importance.csv")
            
            return run.info.run_id, model
    
    def promote_model(self, model_name, version, stage="Production"):
        """Model promotion to different stages"""
        self.client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=stage
        )
        
        # Add model description and tags
        self.client.update_model_version(
            name=model_name,
            version=version,
            description=f"Model promoted to {stage} stage"
        )

# Kubeflow Pipeline Definition
@dsl.pipeline(
    name='MLOps Customer Churn Pipeline',
    description='End-to-end ML pipeline for customer churn prediction'
)
def mlops_pipeline(
    data_path: str = 'gs://ml-data/customer_data.csv',
    model_name: str = 'customer_churn_classifier',
    hyperparameters: dict = {'n_estimators': 100, 'max_depth': 10}
):
    # Data preprocessing component
    preprocess_op = dsl.ContainerOp(
        name='preprocess-data',
        image='gcr.io/project/data-preprocessing:latest',
        arguments=[
            '--data-path', data_path,
            '--output-path', '/tmp/processed_data'
        ],
        file_outputs={
            'train_data': '/tmp/processed_data/train.csv',
            'test_data': '/tmp/processed_data/test.csv'
        }
    )
    
    # Model training component
    train_op = dsl.ContainerOp(
        name='train-model',
        image='gcr.io/project/model-training:latest',
        arguments=[
            '--train-data', preprocess_op.outputs['train_data'],
            '--test-data', preprocess_op.outputs['test_data'],
            '--model-name', model_name,
            '--hyperparameters', str(hyperparameters)
        ],
        file_outputs={
            'model_path': '/tmp/model/model.pkl',
            'metrics': '/tmp/model/metrics.json'
        }
    )
    
    # Model validation component
    validate_op = dsl.ContainerOp(
        name='validate-model',
        image='gcr.io/project/model-validation:latest',
        arguments=[
            '--model-path', train_op.outputs['model_path'],
            '--test-data', preprocess_op.outputs['test_data'],
            '--threshold', '0.85'
        ]
    )
    
    # Model deployment component
    deploy_op = dsl.ContainerOp(
        name='deploy-model',
        image='gcr.io/project/model-deployment:latest',
        arguments=[
            '--model-path', train_op.outputs['model_path'],
            '--model-name', model_name,
            '--deployment-target', 'kubernetes'
        ]
    )
    
    # Set dependencies
    train_op.after(preprocess_op)
    validate_op.after(train_op)
    deploy_op.after(validate_op)

# Model serving with FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="Customer Churn Prediction API")

class PredictionRequest(BaseModel):
    tenure: float
    monthly_charges: float
    total_charges: float
    num_services: int
    gender: str
    partner: str
    dependents: str
    phone_service: str

class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    model_version: str

# Load model at startup
model = None
model_version = None

@app.on_event("startup")
async def load_model():
    global model, model_version
    try:
        # Load model from MLflow Model Registry
        client = MlflowClient()
        model_version_info = client.get_latest_versions(
            "customer_churn_classifier", 
            stages=["Production"]
        )[0]
        
        model_uri = f"models:/customer_churn_classifier/{model_version_info.version}"
        model = mlflow.sklearn.load_model(model_uri)
        model_version = model_version_info.version
        
    except Exception as e:
        raise RuntimeError(f"Failed to load model: {str(e)}")

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Prepare features
        features = np.array([[
            request.tenure,
            request.monthly_charges,
            request.total_charges,
            request.num_services,
            1 if request.gender == 'Male' else 0,
            1 if request.partner == 'Yes' else 0,
            1 if request.dependents == 'Yes' else 0,
            1 if request.phone_service == 'Yes' else 0
        ]])
        
        # Make prediction
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]
        
        return PredictionResponse(
            prediction=int(prediction),
            probability=float(probability),
            model_version=model_version
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model is not None}
```

### 2. How do you implement continuous integration and continuous deployment (CI/CD) for ML models?
**Answer**: ML CI/CD involves automated testing, validation, and deployment of both code and models.

```yaml
# .github/workflows/mlops-pipeline.yml
name: MLOps CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: 3.9
  MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
  AWS_DEFAULT_REGION: us-east-1

jobs:
  code-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run linting
        run: |
          flake8 src/ tests/
          black --check src/ tests/
          isort --check-only src/ tests/
      
      - name: Run type checking
        run: mypy src/
      
      - name: Run security scan
        run: bandit -r src/

  unit-tests:
    runs-on: ubuntu-latest
    needs: code-quality
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install dependencies
        run: pip install -r requirements.txt -r requirements-dev.txt
      
      - name: Run unit tests
        run: |
          pytest tests/unit/ -v --cov=src --cov-report=xml
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3

  data-validation:
    runs-on: ubuntu-latest
    needs: unit-tests
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run data validation tests
        run: |
          python -m pytest tests/data_validation/ -v
          python scripts/validate_data_schema.py
          python scripts/check_data_drift.py

  model-training:
    runs-on: ubuntu-latest
    needs: data-validation
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_DEFAULT_REGION }}
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Train model
        run: |
          python scripts/train_model.py \
            --experiment-name "customer_churn_ci_cd" \
            --data-path "s3://ml-data/customer_data.csv" \
            --model-name "customer_churn_classifier"
        env:
          MLFLOW_TRACKING_URI: ${{ env.MLFLOW_TRACKING_URI }}
      
      - name: Run model validation
        run: |
          python scripts/validate_model.py \
            --model-name "customer_churn_classifier" \
            --min-accuracy 0.85 \
            --max-drift-score 0.1

  integration-tests:
    runs-on: ubuntu-latest
    needs: model-training
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install dependencies
        run: pip install -r requirements.txt -r requirements-dev.txt
      
      - name: Run integration tests
        run: |
          pytest tests/integration/ -v
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test
          MLFLOW_TRACKING_URI: ${{ env.MLFLOW_TRACKING_URI }}

  build-and-push:
    runs-on: ubuntu-latest
    needs: integration-tests
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_DEFAULT_REGION }}
      
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
      
      - name: Build and push Docker image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: ml-model-serving
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          docker tag $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG $ECR_REGISTRY/$ECR_REPOSITORY:latest
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest

  deploy-staging:
    runs-on: ubuntu-latest
    needs: build-and-push
    environment: staging
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to staging
        run: |
          # Deploy to Kubernetes staging environment
          kubectl set image deployment/ml-model-serving \
            ml-model-serving=${{ steps.login-ecr.outputs.registry }}/ml-model-serving:${{ github.sha }} \
            --namespace=staging
          
          kubectl rollout status deployment/ml-model-serving --namespace=staging
      
      - name: Run smoke tests
        run: |
          python tests/smoke_tests.py --endpoint https://staging-api.company.com
      
      - name: Run performance tests
        run: |
          python tests/performance_tests.py --endpoint https://staging-api.company.com

  deploy-production:
    runs-on: ubuntu-latest
    needs: deploy-staging
    environment: production
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to production
        run: |
          # Blue-green deployment to production
          kubectl apply -f k8s/production/
          
          # Wait for deployment to be ready
          kubectl rollout status deployment/ml-model-serving-green --namespace=production
          
          # Switch traffic to green deployment
          kubectl patch service ml-model-serving \
            -p '{"spec":{"selector":{"version":"green"}}}' \
            --namespace=production
          
          # Clean up blue deployment after successful switch
          kubectl delete deployment ml-model-serving-blue --namespace=production
      
      - name: Notify deployment success
        uses: 8398a7/action-slack@v3
        with:
          status: success
          text: "🚀 ML model successfully deployed to production!"
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}

  post-deployment-monitoring:
    runs-on: ubuntu-latest
    needs: deploy-production
    steps:
      - name: Setup monitoring alerts
        run: |
          # Configure monitoring and alerting
          python scripts/setup_monitoring.py \
            --environment production \
            --model-name customer_churn_classifier
      
      - name: Run post-deployment validation
        run: |
          python scripts/post_deployment_validation.py \
            --endpoint https://api.company.com \
            --duration 300  # 5 minutes
```

### 3. How do you implement model versioning and experiment tracking?
**Answer**: Model versioning and experiment tracking are essential for reproducibility and model governance.

```python
# Comprehensive experiment tracking and model versioning
import mlflow
import mlflow.sklearn
import mlflow.pytorch
from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType
import pandas as pd
import numpy as np
from datetime import datetime
import hashlib
import json

class MLflowModelManager:
    def __init__(self, tracking_uri, registry_uri=None):
        mlflow.set_tracking_uri(tracking_uri)
        if registry_uri:
            mlflow.set_registry_uri(registry_uri)
        self.client = MlflowClient()
    
    def create_experiment(self, experiment_name, description=None, tags=None):
        """Create a new experiment with metadata"""
        try:
            experiment_id = mlflow.create_experiment(
                name=experiment_name,
                artifact_location=f"s3://ml-artifacts/{experiment_name}",
                tags=tags or {}
            )
            
            if description:
                self.client.update_experiment(experiment_id, description=description)
            
            return experiment_id
        except mlflow.exceptions.MlflowException:
            # Experiment already exists
            return mlflow.get_experiment_by_name(experiment_name).experiment_id
    
    def log_experiment_run(self, experiment_name, model, X_train, y_train, X_test, y_test, 
                          hyperparameters, preprocessing_steps=None, feature_names=None):
        """Comprehensive experiment logging"""
        mlflow.set_experiment(experiment_name)
        
        with mlflow.start_run() as run:
            # Log basic information
            mlflow.set_tags({
                "model_type": type(model).__name__,
                "training_date": datetime.now().isoformat(),
                "data_version": self._calculate_data_hash(X_train, y_train),
                "environment": "development"
            })
            
            # Log hyperparameters
            mlflow.log_params(hyperparameters)
            
            # Log dataset information
            mlflow.log_params({
                "train_samples": len(X_train),
                "test_samples": len(X_test),
                "num_features": X_train.shape[1],
                "target_classes": len(np.unique(y_train))
            })
            
            # Train model
            model.fit(X_train, y_train)
            
            # Make predictions
            y_pred_train = model.predict(X_train)
            y_pred_test = model.predict(X_test)
            y_prob_test = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
            
            # Calculate and log metrics
            metrics = self._calculate_metrics(y_train, y_pred_train, y_test, y_pred_test, y_prob_test)
            mlflow.log_metrics(metrics)
            
            # Log model
            model_info = mlflow.sklearn.log_model(
                model,
                "model",
                signature=mlflow.models.infer_signature(X_train, y_pred_train),
                input_example=X_train.iloc[:5] if hasattr(X_train, 'iloc') else X_train[:5]
            )
            
            # Log preprocessing steps
            if preprocessing_steps:
                with open("preprocessing_steps.json", "w") as f:
                    json.dump(preprocessing_steps, f)
                mlflow.log_artifact("preprocessing_steps.json")
            
            # Log feature importance if available
            if hasattr(model, 'feature_importances_'):
                feature_importance = pd.DataFrame({
                    'feature': feature_names or [f'feature_{i}' for i in range(len(model.feature_importances_))],
                    'importance': model.feature_importances_
                }).sort_values('importance', ascending=False)
                
                feature_importance.to_csv("feature_importance.csv", index=False)
                mlflow.log_artifact("feature_importance.csv")
            
            # Log confusion matrix and other plots
            self._log_evaluation_plots(y_test, y_pred_test, y_prob_test)
            
            return run.info.run_id, model_info
    
    def register_model(self, model_uri, model_name, description=None, tags=None):
        """Register model in MLflow Model Registry"""
        model_version = mlflow.register_model(
            model_uri=model_uri,
            name=model_name,
            tags=tags
        )
        
        if description:
            self.client.update_model_version(
                name=model_name,
                version=model_version.version,
                description=description
            )
        
        return model_version
    
    def promote_model(self, model_name, version, stage, description=None):
        """Promote model to different stage"""
        # Archive current production model
        if stage.lower() == "production":
            current_prod_versions = self.client.get_latest_versions(
                model_name, stages=["Production"]
            )
            for prod_version in current_prod_versions:
                self.client.transition_model_version_stage(
                    name=model_name,
                    version=prod_version.version,
                    stage="Archived"
                )
        
        # Promote new model
        self.client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=stage
        )
        
        if description:
            self.client.update_model_version(
                name=model_name,
                version=version,
                description=description
            )
    
    def compare_models(self, experiment_name, metric_name="accuracy", top_n=5):
        """Compare models from experiment runs"""
        experiment = mlflow.get_experiment_by_name(experiment_name)
        runs = mlflow.search_runs(
            experiment_ids=[experiment.experiment_id],
            order_by=[f"metrics.{metric_name} DESC"],
            max_results=top_n
        )
        
        comparison_df = runs[[
            'run_id', 'status', 'start_time',
            f'metrics.{metric_name}', 'metrics.precision', 'metrics.recall',
            'params.n_estimators', 'params.max_depth', 'params.learning_rate'
        ]].copy()
        
        return comparison_df
    
    def get_model_lineage(self, model_name, version):
        """Get model lineage and metadata"""
        model_version = self.client.get_model_version(model_name, version)
        run = self.client.get_run(model_version.run_id)
        
        lineage = {
            "model_name": model_name,
            "version": version,
            "run_id": model_version.run_id,
            "experiment_id": run.info.experiment_id,
            "creation_timestamp": model_version.creation_timestamp,
            "last_updated_timestamp": model_version.last_updated_timestamp,
            "stage": model_version.current_stage,
            "description": model_version.description,
            "tags": model_version.tags,
            "run_data": {
                "parameters": run.data.params,
                "metrics": run.data.metrics,
                "tags": run.data.tags
            },
            "artifacts": [f.path for f in self.client.list_artifacts(model_version.run_id)]
        }
        
        return lineage
    
    def _calculate_data_hash(self, X, y):
        """Calculate hash of training data for versioning"""
        data_string = str(X.values.tobytes()) + str(y.values.tobytes()) if hasattr(X, 'values') else str(X.tobytes()) + str(y.tobytes())
        return hashlib.md5(data_string.encode()).hexdigest()[:8]
    
    def _calculate_metrics(self, y_train, y_pred_train, y_test, y_pred_test, y_prob_test):
        """Calculate comprehensive metrics"""
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
        
        metrics = {
            "train_accuracy": accuracy_score(y_train, y_pred_train),
            "test_accuracy": accuracy_score(y_test, y_pred_test),
            "precision": precision_score(y_test, y_pred_test, average='weighted'),
            "recall": recall_score(y_test, y_pred_test, average='weighted'),
            "f1_score": f1_score(y_test, y_pred_test, average='weighted')
        }
        
        if y_prob_test is not None:
            metrics["auc_roc"] = roc_auc_score(y_test, y_prob_test)
        
        return metrics
    
    def _log_evaluation_plots(self, y_true, y_pred, y_prob):
        """Log evaluation plots as artifacts"""
        import matplotlib.pyplot as plt
        from sklearn.metrics import confusion_matrix, roc_curve, precision_recall_curve
        import seaborn as sns
        
        # Confusion Matrix
        plt.figure(figsize=(8, 6))
        cm = confusion_matrix(y_true, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.savefig('confusion_matrix.png')
        mlflow.log_artifact('confusion_matrix.png')
        plt.close()
        
        if y_prob is not None:
            # ROC Curve
            plt.figure(figsize=(8, 6))
            fpr, tpr, _ = roc_curve(y_true, y_prob)
            plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {roc_auc_score(y_true, y_prob):.2f})')
            plt.plot([0, 1], [0, 1], 'k--', label='Random')
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title('ROC Curve')
            plt.legend()
            plt.savefig('roc_curve.png')
            mlflow.log_artifact('roc_curve.png')
            plt.close()
            
            # Precision-Recall Curve
            plt.figure(figsize=(8, 6))
            precision, recall, _ = precision_recall_curve(y_true, y_prob)
            plt.plot(recall, precision)
            plt.xlabel('Recall')
            plt.ylabel('Precision')
            plt.title('Precision-Recall Curve')
            plt.savefig('precision_recall_curve.png')
            mlflow.log_artifact('precision_recall_curve.png')
            plt.close()

# Usage example
if __name__ == "__main__":
    # Initialize MLflow manager
    manager = MLflowModelManager(
        tracking_uri="http://mlflow-server:5000",
        registry_uri="http://mlflow-server:5000"
    )
    
    # Create experiment
    experiment_id = manager.create_experiment(
        experiment_name="customer_churn_v2",
        description="Customer churn prediction with feature engineering v2",
        tags={"team": "data-science", "project": "customer_retention"}
    )
    
    # Load data and train model (example)
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import make_classification
    
    X, y = make_classification(n_samples=1000, n_features=20, n_classes=2, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train and log model
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    hyperparameters = {"n_estimators": 100, "max_depth": 10, "random_state": 42}
    
    run_id, model_info = manager.log_experiment_run(
        experiment_name="customer_churn_v2",
        model=model,
        X_train=X_train,
        y_train=y_train,
        X_test=X_test,
        y_test=y_test,
        hyperparameters=hyperparameters,
        feature_names=[f"feature_{i}" for i in range(X.shape[1])]
    )
    
    # Register model
    model_version = manager.register_model(
        model_uri=model_info.model_uri,
        model_name="customer_churn_classifier",
        description="Random Forest model for customer churn prediction",
        tags={"algorithm": "random_forest", "version": "v2.0"}
    )
    
    # Promote to staging
    manager.promote_model(
        model_name="customer_churn_classifier",
        version=model_version.version,
        stage="Staging",
        description="Promoted to staging for validation"
    )
```

This comprehensive MLOps interview questions file covers core concepts, CI/CD, and model versioning. Would you like me to continue with the remaining sections and then create comprehensive interview questions for other tools like Grafana, Vector Databases, etc.?