# MLflow Interview Questions

## Basic Concepts

### 1. What is MLflow and what are its main components?
**Answer:** MLflow is an open-source platform for managing the complete machine learning lifecycle. It has four main components:

- **MLflow Tracking**: Records and queries experiments (code, data, config, results)
- **MLflow Projects**: Packages ML code in a reusable, reproducible form
- **MLflow Models**: Manages and deploys models from various ML libraries
- **MLflow Model Registry**: Centralized model store for managing model lifecycle

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier

# Start MLflow run
with mlflow.start_run():
    # Train model
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    
    # Log parameters and metrics
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("accuracy", accuracy_score(y_test, predictions))
    
    # Log model
    mlflow.sklearn.log_model(model, "random_forest_model")
```

### 2. How do you set up MLflow tracking server?
**Answer:** MLflow tracking server can be set up in multiple ways:

**Local File Store:**
```bash
mlflow server --backend-store-uri file:///path/to/mlruns --default-artifact-root file:///path/to/artifacts --host 0.0.0.0 --port 5000
```

**Database Backend:**
```bash
mlflow server --backend-store-uri postgresql://user:password@host:port/database --default-artifact-root s3://bucket/artifacts --host 0.0.0.0 --port 5000
```

**Python Configuration:**
```python
import mlflow

# Set tracking URI
mlflow.set_tracking_uri("http://localhost:5000")

# Set experiment
mlflow.set_experiment("my_experiment")
```

### 3. What is the difference between MLflow Tracking and MLflow Projects?
**Answer:**

**MLflow Tracking:**
- Records experiment runs, parameters, metrics, and artifacts
- Provides UI for comparing runs
- Stores metadata about ML experiments

**MLflow Projects:**
- Packages ML code in reproducible format
- Defines dependencies and entry points
- Enables code sharing and collaboration

```yaml
# MLproject file
name: my_ml_project
conda_env: conda.yaml

entry_points:
  main:
    parameters:
      alpha: {type: float, default: 0.5}
      l1_ratio: {type: float, default: 0.1}
    command: "python train.py --alpha {alpha} --l1-ratio {l1_ratio}"
```

### 4. How do you log different types of artifacts in MLflow?
**Answer:** MLflow supports various artifact types:

```python
import mlflow
import matplotlib.pyplot as plt
import pandas as pd

with mlflow.start_run():
    # Log parameters
    mlflow.log_param("learning_rate", 0.01)
    
    # Log metrics
    mlflow.log_metric("rmse", 0.89)
    
    # Log artifacts
    # 1. Save and log plot
    plt.figure()
    plt.plot([1, 2, 3], [4, 5, 6])
    plt.savefig("plot.png")
    mlflow.log_artifact("plot.png")
    
    # 2. Log DataFrame as CSV
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    df.to_csv("data.csv", index=False)
    mlflow.log_artifact("data.csv")
    
    # 3. Log entire directory
    mlflow.log_artifacts("output_dir")
    
    # 4. Log model
    mlflow.sklearn.log_model(model, "model")
```

## Intermediate Concepts

### 5. How do you implement MLflow Model Registry for model lifecycle management?
**Answer:** MLflow Model Registry provides centralized model management:

```python
import mlflow
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Register model
model_name = "my_model"
model_version = mlflow.register_model(
    model_uri=f"runs:/{run_id}/model",
    name=model_name
)

# Transition model stages
client.transition_model_version_stage(
    name=model_name,
    version=model_version.version,
    stage="Staging"
)

# Add model description
client.update_model_version(
    name=model_name,
    version=model_version.version,
    description="This model version is a scikit-learn random forest"
)

# Get latest model version
latest_version = client.get_latest_versions(
    model_name, 
    stages=["Production"]
)[0]

# Load model from registry
model = mlflow.pyfunc.load_model(
    model_uri=f"models:/{model_name}/{latest_version.version}"
)
```

### 6. How do you set up MLflow with different storage backends?
**Answer:** MLflow supports various storage configurations:

**S3 Backend:**
```python
import mlflow
import os

# Set AWS credentials
os.environ["AWS_ACCESS_KEY_ID"] = "your_access_key"
os.environ["AWS_SECRET_ACCESS_KEY"] = "your_secret_key"

# Configure MLflow
mlflow.set_tracking_uri("http://mlflow-server:5000")

# Log with S3 artifact store
with mlflow.start_run():
    mlflow.log_artifact("model.pkl", "s3://my-bucket/artifacts")
```

**Azure Blob Storage:**
```python
import mlflow
import os

# Set Azure credentials
os.environ["AZURE_STORAGE_CONNECTION_STRING"] = "connection_string"

# Start server with Azure backend
# mlflow server --default-artifact-root wasbs://container@account.blob.core.windows.net/path
```

**Google Cloud Storage:**
```python
import mlflow
import os

# Set GCS credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"

# Configure for GCS
# mlflow server --default-artifact-root gs://bucket/path
```

### 7. How do you implement custom MLflow models?
**Answer:** Create custom MLflow models using the `pyfunc` interface:

```python
import mlflow
import mlflow.pyfunc
import pandas as pd

class CustomModel(mlflow.pyfunc.PythonModel):
    def __init__(self, model, preprocessor):
        self.model = model
        self.preprocessor = preprocessor
    
    def predict(self, context, model_input):
        # Custom preprocessing
        processed_input = self.preprocessor.transform(model_input)
        
        # Make predictions
        predictions = self.model.predict(processed_input)
        
        # Custom postprocessing
        return pd.DataFrame(predictions, columns=["prediction"])

# Create and log custom model
custom_model = CustomModel(trained_model, preprocessor)

with mlflow.start_run():
    mlflow.pyfunc.log_model(
        artifact_path="custom_model",
        python_model=custom_model,
        conda_env={
            "channels": ["defaults"],
            "dependencies": [
                "python=3.8",
                "scikit-learn",
                "pandas"
            ]
        }
    )
```

### 8. How do you implement MLflow experiment comparison and analysis?
**Answer:** MLflow provides APIs for experiment comparison:

```python
import mlflow
from mlflow.tracking import MlflowClient
import pandas as pd

client = MlflowClient()

# Get experiment by name
experiment = client.get_experiment_by_name("my_experiment")

# Search runs with filters
runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    filter_string="metrics.accuracy > 0.8",
    order_by=["metrics.accuracy DESC"],
    max_results=10
)

# Create comparison DataFrame
comparison_data = []
for run in runs:
    run_data = {
        'run_id': run.info.run_id,
        'accuracy': run.data.metrics.get('accuracy'),
        'precision': run.data.metrics.get('precision'),
        'learning_rate': run.data.params.get('learning_rate'),
        'model_type': run.data.params.get('model_type')
    }
    comparison_data.append(run_data)

comparison_df = pd.DataFrame(comparison_data)
print(comparison_df.sort_values('accuracy', ascending=False))

# Get best run
best_run = runs[0]
best_model = mlflow.pyfunc.load_model(
    f"runs:/{best_run.info.run_id}/model"
)
```

## Advanced Concepts

### 9. How do you implement MLflow with Kubernetes for scalable ML workflows?
**Answer:** Deploy MLflow on Kubernetes for production scalability:

```yaml
# mlflow-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mlflow-server
spec:
  replicas: 2
  selector:
    matchLabels:
      app: mlflow-server
  template:
    metadata:
      labels:
        app: mlflow-server
    spec:
      containers:
      - name: mlflow-server
        image: mlflow-server:latest
        ports:
        - containerPort: 5000
        env:
        - name: BACKEND_STORE_URI
          value: "postgresql://user:pass@postgres:5432/mlflow"
        - name: DEFAULT_ARTIFACT_ROOT
          value: "s3://mlflow-artifacts"
        command:
        - mlflow
        - server
        - --backend-store-uri
        - $(BACKEND_STORE_URI)
        - --default-artifact-root
        - $(DEFAULT_ARTIFACT_ROOT)
        - --host
        - 0.0.0.0
        - --port
        - "5000"
---
apiVersion: v1
kind: Service
metadata:
  name: mlflow-service
spec:
  selector:
    app: mlflow-server
  ports:
  - port: 5000
    targetPort: 5000
  type: LoadBalancer
```

**MLflow Project with Kubernetes:**
```yaml
# MLproject
name: kubernetes-training
kubernetes_job_template: kubernetes_job_template.yaml

entry_points:
  main:
    parameters:
      epochs: {type: int, default: 10}
    command: "python train.py --epochs {epochs}"
```

### 10. How do you implement MLflow model serving with different deployment targets?
**Answer:** MLflow supports multiple deployment options:

**Local Serving:**
```bash
# Serve model locally
mlflow models serve -m models:/my_model/Production -p 1234

# Test the endpoint
curl -X POST -H "Content-Type:application/json" \
  --data '{"inputs": [[1, 2, 3, 4]]}' \
  http://localhost:1234/invocations
```

**Docker Deployment:**
```bash
# Build Docker image
mlflow models build-docker -m models:/my_model/Production -n my-model

# Run Docker container
docker run -p 5000:8080 my-model
```

**AWS SageMaker Deployment:**
```python
import mlflow.sagemaker as mfs

# Deploy to SageMaker
mfs.deploy(
    app_name="my-model-app",
    model_uri="models:/my_model/Production",
    region_name="us-west-2",
    mode="create",
    execution_role_arn="arn:aws:iam::account:role/SageMakerRole",
    instance_type="ml.m4.xlarge",
    instance_count=1
)

# Make predictions
import boto3
runtime = boto3.client('sagemaker-runtime')
response = runtime.invoke_endpoint(
    EndpointName='my-model-app',
    ContentType='application/json',
    Body='{"inputs": [[1, 2, 3, 4]]}'
)
```

**Azure ML Deployment:**
```python
import mlflow.azureml as maz

# Deploy to Azure ML
maz.deploy(
    model_uri="models:/my_model/Production",
    workspace=workspace,
    model_name="my-model",
    service_name="my-model-service",
    deployment_config=deployment_config,
    inference_config=inference_config
)
```

### 11. How do you implement MLflow autologging with different ML frameworks?
**Answer:** MLflow provides automatic logging for popular ML libraries:

**Scikit-learn Autologging:**
```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

# Enable autologging
mlflow.sklearn.autolog()

with mlflow.start_run():
    # Model training automatically logged
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Cross-validation scores automatically logged
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)
```

**TensorFlow/Keras Autologging:**
```python
import mlflow
import mlflow.tensorflow
import tensorflow as tf

# Enable autologging
mlflow.tensorflow.autolog()

with mlflow.start_run():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Training automatically logged
    model.fit(X_train, y_train, epochs=10, validation_split=0.2)
```

**XGBoost Autologging:**
```python
import mlflow
import mlflow.xgboost
import xgboost as xgb

# Enable autologging
mlflow.xgboost.autolog()

with mlflow.start_run():
    # Training automatically logged
    model = xgb.XGBClassifier(n_estimators=100)
    model.fit(X_train, y_train)
```

### 12. How do you implement MLflow with CI/CD pipelines for MLOps?
**Answer:** Integrate MLflow with CI/CD for automated ML workflows:

**GitHub Actions Workflow:**
```yaml
# .github/workflows/ml-pipeline.yml
name: ML Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  train-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    
    - name: Install dependencies
      run: |
        pip install mlflow boto3 scikit-learn
    
    - name: Train Model
      env:
        MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      run: |
        python train.py
    
    - name: Register Model
      run: |
        python register_model.py
    
    - name: Deploy Model
      if: github.ref == 'refs/heads/main'
      run: |
        python deploy_model.py
```

**Model Training Script:**
```python
# train.py
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import os

def train_model():
    # Set MLflow tracking URI
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
    
    with mlflow.start_run():
        # Train model
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X_train, y_train)
        
        # Evaluate model
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        
        # Log metrics and model
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(model, "model")
        
        # Model validation gate
        if accuracy > 0.85:
            # Register model for production
            model_uri = f"runs:/{mlflow.active_run().info.run_id}/model"
            mlflow.register_model(model_uri, "production_model")
            print(f"Model registered with accuracy: {accuracy}")
        else:
            print(f"Model accuracy {accuracy} below threshold")
            exit(1)

if __name__ == "__main__":
    train_model()
```

## Real-World Applications

### 13. How would you design an MLflow-based ML platform for a large organization?
**Answer:** Design enterprise MLflow platform with scalability and governance:

**Architecture Components:**
```python
# Enterprise MLflow Configuration
import mlflow
from mlflow.tracking import MlflowClient
import logging

class EnterpriseMLflowPlatform:
    def __init__(self, config):
        self.config = config
        self.client = MlflowClient(tracking_uri=config['tracking_uri'])
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def create_experiment(self, name, team, project):
        """Create experiment with governance metadata"""
        experiment_name = f"{team}_{project}_{name}"
        
        try:
            experiment_id = self.client.create_experiment(
                name=experiment_name,
                tags={
                    "team": team,
                    "project": project,
                    "created_by": self.config['user'],
                    "environment": self.config['environment']
                }
            )
            self.logger.info(f"Created experiment: {experiment_name}")
            return experiment_id
        except Exception as e:
            self.logger.error(f"Failed to create experiment: {e}")
            raise
    
    def log_model_with_governance(self, model, model_name, metadata):
        """Log model with governance and compliance metadata"""
        with mlflow.start_run():
            # Log model
            mlflow.sklearn.log_model(model, "model")
            
            # Log governance metadata
            mlflow.set_tags({
                "data_source": metadata.get("data_source"),
                "data_version": metadata.get("data_version"),
                "model_owner": metadata.get("owner"),
                "compliance_status": metadata.get("compliance"),
                "approval_status": "pending"
            })
            
            # Log model lineage
            mlflow.log_param("training_data_hash", metadata.get("data_hash"))
            mlflow.log_param("code_version", metadata.get("git_commit"))
    
    def promote_model(self, model_name, version, stage, approver):
        """Promote model with approval workflow"""
        # Check approval permissions
        if not self._check_approval_permissions(approver, stage):
            raise PermissionError("Insufficient permissions for promotion")
        
        # Transition model stage
        self.client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=stage
        )
        
        # Log approval
        self.client.set_model_version_tag(
            name=model_name,
            version=version,
            key="approved_by",
            value=approver
        )
        
        self.logger.info(f"Model {model_name} v{version} promoted to {stage}")

# Usage
platform = EnterpriseMLflowPlatform({
    'tracking_uri': 'https://mlflow.company.com',
    'user': 'data_scientist',
    'environment': 'production'
})
```

### 14. How do you implement MLflow for A/B testing and model comparison in production?
**Answer:** Implement A/B testing framework with MLflow:

```python
import mlflow
import mlflow.pyfunc
import random
from datetime import datetime
import json

class ABTestingFramework:
    def __init__(self, experiment_name):
        self.experiment_name = experiment_name
        self.client = mlflow.tracking.MlflowClient()
        self.models = {}
        self.load_models()
    
    def load_models(self):
        """Load models for A/B testing"""
        # Load model A (control)
        self.models['A'] = mlflow.pyfunc.load_model(
            "models:/recommendation_model/Production"
        )
        
        # Load model B (treatment)
        self.models['B'] = mlflow.pyfunc.load_model(
            "models:/recommendation_model_v2/Staging"
        )
    
    def get_model_assignment(self, user_id):
        """Assign user to model variant"""
        # Consistent assignment based on user_id
        random.seed(hash(user_id) % 2**32)
        return 'A' if random.random() < 0.5 else 'B'
    
    def predict_with_logging(self, user_id, features):
        """Make prediction and log for A/B test analysis"""
        variant = self.get_model_assignment(user_id)
        model = self.models[variant]
        
        # Make prediction
        prediction = model.predict(features)
        
        # Log prediction for analysis
        with mlflow.start_run(experiment_id=self.experiment_name):
            mlflow.log_param("user_id", user_id)
            mlflow.log_param("variant", variant)
            mlflow.log_param("timestamp", datetime.now().isoformat())
            mlflow.log_metric("prediction", prediction[0])
            
            # Log features
            for i, feature in enumerate(features[0]):
                mlflow.log_param(f"feature_{i}", feature)
        
        return prediction, variant
    
    def log_outcome(self, user_id, variant, outcome):
        """Log user outcome for A/B test analysis"""
        with mlflow.start_run(experiment_id=self.experiment_name):
            mlflow.log_param("user_id", user_id)
            mlflow.log_param("variant", variant)
            mlflow.log_param("event_type", "outcome")
            mlflow.log_metric("conversion", outcome)
            mlflow.log_param("timestamp", datetime.now().isoformat())
    
    def analyze_ab_test(self):
        """Analyze A/B test results"""
        runs = self.client.search_runs(
            experiment_ids=[self.experiment_name],
            filter_string="params.event_type = 'outcome'"
        )
        
        results = {'A': [], 'B': []}
        for run in runs:
            variant = run.data.params.get('variant')
            conversion = float(run.data.metrics.get('conversion', 0))
            results[variant].append(conversion)
        
        # Calculate statistics
        stats = {}
        for variant in ['A', 'B']:
            conversions = results[variant]
            stats[variant] = {
                'count': len(conversions),
                'conversion_rate': sum(conversions) / len(conversions) if conversions else 0,
                'total_conversions': sum(conversions)
            }
        
        return stats

# Usage
ab_framework = ABTestingFramework("ab_test_experiment")

# Make prediction
prediction, variant = ab_framework.predict_with_logging(
    user_id="user_123",
    features=[[1.0, 2.0, 3.0]]
)

# Log outcome
ab_framework.log_outcome(
    user_id="user_123",
    variant=variant,
    outcome=1  # 1 for conversion, 0 for no conversion
)

# Analyze results
results = ab_framework.analyze_ab_test()
print(json.dumps(results, indent=2))
```

### 15. How do you implement MLflow for multi-model ensemble management and deployment?
**Answer:** Implement ensemble model management with MLflow:

```python
import mlflow
import mlflow.pyfunc
import numpy as np
import pandas as pd
from typing import List, Dict

class EnsembleModel(mlflow.pyfunc.PythonModel):
    def __init__(self, models: Dict[str, str], weights: Dict[str, float]):
        self.model_uris = models
        self.weights = weights
        self.models = {}
    
    def load_context(self, context):
        """Load all models in the ensemble"""
        for name, uri in self.model_uris.items():
            self.models[name] = mlflow.pyfunc.load_model(uri)
    
    def predict(self, context, model_input):
        """Make ensemble predictions"""
        predictions = {}
        
        # Get predictions from each model
        for name, model in self.models.items():
            predictions[name] = model.predict(model_input)
        
        # Weighted ensemble
        ensemble_pred = np.zeros_like(predictions[list(predictions.keys())[0]])
        
        for name, pred in predictions.items():
            weight = self.weights.get(name, 1.0)
            ensemble_pred += weight * pred
        
        # Normalize by total weights
        total_weight = sum(self.weights.values())
        ensemble_pred /= total_weight
        
        return ensemble_pred

class EnsembleManager:
    def __init__(self):
        self.client = mlflow.tracking.MlflowClient()
    
    def create_ensemble(self, ensemble_name: str, models: Dict[str, str], 
                       weights: Dict[str, float]):
        """Create and register ensemble model"""
        
        # Create ensemble model
        ensemble = EnsembleModel(models, weights)
        
        with mlflow.start_run():
            # Log ensemble configuration
            mlflow.log_param("ensemble_type", "weighted_average")
            mlflow.log_param("num_models", len(models))
            
            for name, uri in models.items():
                mlflow.log_param(f"model_{name}_uri", uri)
                mlflow.log_param(f"model_{name}_weight", weights.get(name, 1.0))
            
            # Log ensemble model
            mlflow.pyfunc.log_model(
                artifact_path="ensemble_model",
                python_model=ensemble,
                conda_env={
                    "channels": ["defaults"],
                    "dependencies": [
                        "python=3.8",
                        "mlflow",
                        "numpy",
                        "pandas",
                        "scikit-learn"
                    ]
                }
            )
            
            # Register ensemble
            run_id = mlflow.active_run().info.run_id
            model_uri = f"runs:/{run_id}/ensemble_model"
            mlflow.register_model(model_uri, ensemble_name)
    
    def optimize_ensemble_weights(self, models: Dict[str, str], 
                                 X_val: np.ndarray, y_val: np.ndarray):
        """Optimize ensemble weights using validation data"""
        from scipy.optimize import minimize
        
        # Load models
        loaded_models = {}
        for name, uri in models.items():
            loaded_models[name] = mlflow.pyfunc.load_model(uri)
        
        # Get individual predictions
        predictions = {}
        for name, model in loaded_models.items():
            predictions[name] = model.predict(X_val).flatten()
        
        def objective(weights):
            """Objective function for weight optimization"""
            ensemble_pred = np.zeros_like(y_val)
            
            for i, (name, pred) in enumerate(predictions.items()):
                ensemble_pred += weights[i] * pred
            
            # Normalize
            ensemble_pred /= np.sum(weights)
            
            # Return MSE
            return np.mean((ensemble_pred - y_val) ** 2)
        
        # Optimize weights
        n_models = len(models)
        initial_weights = np.ones(n_models) / n_models
        
        constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
        bounds = [(0, 1) for _ in range(n_models)]
        
        result = minimize(
            objective, 
            initial_weights, 
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        # Return optimized weights
        model_names = list(models.keys())
        optimized_weights = {
            name: weight for name, weight in zip(model_names, result.x)
        }
        
        return optimized_weights
    
    def deploy_ensemble(self, ensemble_name: str, stage: str = "Production"):
        """Deploy ensemble model"""
        # Get latest ensemble version
        latest_version = self.client.get_latest_versions(
            ensemble_name, 
            stages=[stage]
        )[0]
        
        # Deploy using MLflow serving
        import subprocess
        
        model_uri = f"models:/{ensemble_name}/{latest_version.version}"
        
        # Start serving process
        serve_cmd = [
            "mlflow", "models", "serve",
            "-m", model_uri,
            "-p", "5000",
            "--no-conda"
        ]
        
        process = subprocess.Popen(serve_cmd)
        return process

# Usage Example
ensemble_manager = EnsembleManager()

# Define models in ensemble
models = {
    "random_forest": "models:/rf_model/Production",
    "gradient_boost": "models:/gb_model/Production", 
    "neural_network": "models:/nn_model/Production"
}

# Optimize weights
optimized_weights = ensemble_manager.optimize_ensemble_weights(
    models, X_validation, y_validation
)

# Create ensemble
ensemble_manager.create_ensemble(
    ensemble_name="production_ensemble",
    models=models,
    weights=optimized_weights
)

# Deploy ensemble
process = ensemble_manager.deploy_ensemble("production_ensemble")
```

This comprehensive set of MLflow interview questions covers basic concepts through advanced enterprise implementations, providing practical examples for experiment tracking, model management, deployment strategies, and MLOps integration.