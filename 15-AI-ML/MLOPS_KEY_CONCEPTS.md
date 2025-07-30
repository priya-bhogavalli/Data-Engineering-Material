# MLOps Key Concepts

## 1. Machine Learning Operations
**What it is**: Set of practices that combines ML, DevOps, and data engineering to deploy and maintain ML systems in production reliably and efficiently.

**Core Principles**:
- **Automation**: Automated ML pipelines and deployments
- **Monitoring**: Continuous model and data monitoring
- **Versioning**: Track models, data, and code versions
- **Reproducibility**: Consistent results across environments
- **Collaboration**: Bridge between data science and operations

## 2. ML Pipeline Architecture
**Training Pipeline**:
```python
# MLflow training pipeline
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def train_model(data_path, model_params):
    with mlflow.start_run():
        # Load and prepare data
        data = pd.read_csv(data_path)
        X = data.drop('target', axis=1)
        y = data['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        # Train model
        model = RandomForestClassifier(**model_params)
        model.fit(X_train, y_train)
        
        # Evaluate
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        
        # Log parameters and metrics
        mlflow.log_params(model_params)
        mlflow.log_metric("accuracy", accuracy)
        
        # Log model
        mlflow.sklearn.log_model(model, "model")
        
        return model, accuracy
```

**Inference Pipeline**:
```python
# Model serving with FastAPI
from fastapi import FastAPI
import mlflow.pyfunc
import pandas as pd

app = FastAPI()

# Load model
model = mlflow.pyfunc.load_model("models:/customer_churn/production")

@app.post("/predict")
async def predict(features: dict):
    # Convert to DataFrame
    input_data = pd.DataFrame([features])
    
    # Make prediction
    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)
    
    return {
        "prediction": int(prediction[0]),
        "probability": float(probability[0][1])
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_version": model.metadata.run_id}
```

## 3. Model Versioning and Registry
**MLflow Model Registry**:
```python
import mlflow
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Register model
model_name = "customer_churn_model"
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

# Promote to production after validation
client.transition_model_version_stage(
    name=model_name,
    version=model_version.version,
    stage="Production"
)

# Add model description and tags
client.update_model_version(
    name=model_name,
    version=model_version.version,
    description="Random Forest model for customer churn prediction"
)
```

**DVC for Data Versioning**:
```bash
# Initialize DVC
dvc init

# Track data files
dvc add data/raw/customers.csv
dvc add data/processed/features.csv

# Commit to git
git add data/raw/customers.csv.dvc data/processed/features.csv.dvc
git commit -m "Add data files"

# Push data to remote storage
dvc remote add -d storage s3://my-dvc-bucket
dvc push

# Create data pipeline
dvc run -n prepare_data \
    -d data/raw/customers.csv \
    -o data/processed/features.csv \
    python src/prepare_data.py

# Reproduce pipeline
dvc repro
```

## 4. Continuous Integration/Continuous Deployment
**GitHub Actions for ML**:
```yaml
# .github/workflows/ml-pipeline.yml
name: ML Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest tests/
    
    - name: Run data validation
      run: |
        python src/validate_data.py
    
    - name: Train model
      run: |
        python src/train_model.py
      env:
        MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
    
    - name: Model validation
      run: |
        python src/validate_model.py

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - name: Deploy to staging
      run: |
        docker build -t ml-model:latest .
        docker push ${{ secrets.REGISTRY_URL }}/ml-model:latest
```

**Model Deployment Pipeline**:
```python
# Automated deployment script
import mlflow
import docker
import kubernetes

def deploy_model(model_name, model_version, environment="staging"):
    # Get model from registry
    model_uri = f"models:/{model_name}/{model_version}"
    
    # Build Docker image
    mlflow.models.build_docker(
        model_uri=model_uri,
        name=f"{model_name}:{model_version}",
        install_mlflow=True
    )
    
    # Deploy to Kubernetes
    if environment == "production":
        deploy_to_k8s(model_name, model_version)
    else:
        deploy_to_staging(model_name, model_version)

def deploy_to_k8s(model_name, model_version):
    deployment_yaml = f"""
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: {model_name}-deployment
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: {model_name}
      template:
        metadata:
          labels:
            app: {model_name}
        spec:
          containers:
          - name: {model_name}
            image: {model_name}:{model_version}
            ports:
            - containerPort: 8000
    """
    
    # Apply deployment
    # kubectl_apply(deployment_yaml)
```

## 5. Model Monitoring
**Performance Monitoring**:
```python
import logging
from datetime import datetime
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score

class ModelMonitor:
    def __init__(self, model_name, threshold=0.05):
        self.model_name = model_name
        self.threshold = threshold
        self.baseline_metrics = {}
        
    def log_prediction(self, features, prediction, actual=None):
        """Log individual predictions"""
        log_entry = {
            'timestamp': datetime.now(),
            'model_name': self.model_name,
            'features': features,
            'prediction': prediction,
            'actual': actual
        }
        
        # Store in database or logging system
        self._store_prediction(log_entry)
    
    def calculate_drift(self, current_data, reference_data):
        """Detect data drift using statistical tests"""
        from scipy.stats import ks_2samp
        
        drift_scores = {}
        for column in current_data.columns:
            if column in reference_data.columns:
                statistic, p_value = ks_2samp(
                    reference_data[column], 
                    current_data[column]
                )
                drift_scores[column] = {
                    'statistic': statistic,
                    'p_value': p_value,
                    'drift_detected': p_value < 0.05
                }
        
        return drift_scores
    
    def evaluate_model_performance(self, predictions, actuals):
        """Evaluate current model performance"""
        metrics = {
            'accuracy': accuracy_score(actuals, predictions),
            'precision': precision_score(actuals, predictions, average='weighted'),
            'recall': recall_score(actuals, predictions, average='weighted')
        }
        
        # Check for performance degradation
        alerts = []
        for metric, value in metrics.items():
            if metric in self.baseline_metrics:
                baseline = self.baseline_metrics[metric]
                if abs(value - baseline) > self.threshold:
                    alerts.append(f"{metric} degraded: {baseline:.3f} -> {value:.3f}")
        
        return metrics, alerts
```

**Alerting System**:
```python
import smtplib
from email.mime.text import MIMEText
import slack_sdk

class AlertManager:
    def __init__(self, slack_token=None, email_config=None):
        self.slack_client = slack_sdk.WebClient(token=slack_token) if slack_token else None
        self.email_config = email_config
    
    def send_alert(self, alert_type, message, severity="medium"):
        """Send alerts via multiple channels"""
        
        if severity == "high":
            self._send_email_alert(alert_type, message)
            self._send_slack_alert(alert_type, message, urgent=True)
        elif severity == "medium":
            self._send_slack_alert(alert_type, message)
        else:
            self._log_alert(alert_type, message)
    
    def _send_slack_alert(self, alert_type, message, urgent=False):
        if self.slack_client:
            channel = "#ml-alerts"
            if urgent:
                message = f"🚨 URGENT: {message}"
            
            self.slack_client.chat_postMessage(
                channel=channel,
                text=f"[{alert_type}] {message}"
            )
    
    def _send_email_alert(self, alert_type, message):
        if self.email_config:
            msg = MIMEText(message)
            msg['Subject'] = f"ML Alert: {alert_type}"
            msg['From'] = self.email_config['from']
            msg['To'] = self.email_config['to']
            
            # Send email logic here
```

## 6. Feature Stores
**Feature Store Implementation**:
```python
import pandas as pd
from datetime import datetime, timedelta

class FeatureStore:
    def __init__(self, storage_backend):
        self.storage = storage_backend
    
    def register_feature_group(self, name, features, primary_key):
        """Register a new feature group"""
        feature_group = {
            'name': name,
            'features': features,
            'primary_key': primary_key,
            'created_at': datetime.now()
        }
        
        self.storage.save_metadata(f"feature_groups/{name}", feature_group)
    
    def write_features(self, feature_group_name, data, timestamp=None):
        """Write features to the store"""
        if timestamp is None:
            timestamp = datetime.now()
        
        # Add timestamp column
        data['feature_timestamp'] = timestamp
        
        # Store features
        self.storage.write_data(f"features/{feature_group_name}", data)
    
    def get_features(self, feature_group_name, entity_ids, timestamp=None):
        """Retrieve features for given entities"""
        if timestamp is None:
            timestamp = datetime.now()
        
        # Get latest features before timestamp
        query = f"""
        SELECT * FROM features.{feature_group_name}
        WHERE entity_id IN ({','.join(map(str, entity_ids))})
        AND feature_timestamp <= '{timestamp}'
        ORDER BY feature_timestamp DESC
        """
        
        return self.storage.query(query)
    
    def create_training_dataset(self, feature_groups, entity_ids, start_time, end_time):
        """Create training dataset from multiple feature groups"""
        datasets = []
        
        for fg_name in feature_groups:
            features = self.get_historical_features(
                fg_name, entity_ids, start_time, end_time
            )
            datasets.append(features)
        
        # Join all feature groups
        result = datasets[0]
        for dataset in datasets[1:]:
            result = result.merge(dataset, on=['entity_id', 'feature_timestamp'])
        
        return result
```

## 7. A/B Testing for ML Models
**Model A/B Testing**:
```python
import random
from typing import Dict, Any

class ModelABTester:
    def __init__(self, models: Dict[str, Any], traffic_split: Dict[str, float]):
        self.models = models
        self.traffic_split = traffic_split
        self.results = {model_name: [] for model_name in models.keys()}
    
    def get_model_for_request(self, user_id: str) -> str:
        """Determine which model to use for this request"""
        # Use consistent hashing for user assignment
        hash_value = hash(user_id) % 100
        
        cumulative_percentage = 0
        for model_name, percentage in self.traffic_split.items():
            cumulative_percentage += percentage * 100
            if hash_value < cumulative_percentage:
                return model_name
        
        # Default to first model
        return list(self.models.keys())[0]
    
    def predict(self, user_id: str, features: Dict) -> Dict:
        """Make prediction using assigned model"""
        model_name = self.get_model_for_request(user_id)
        model = self.models[model_name]
        
        prediction = model.predict([list(features.values())])[0]
        
        # Log for analysis
        self.results[model_name].append({
            'user_id': user_id,
            'features': features,
            'prediction': prediction,
            'timestamp': datetime.now()
        })
        
        return {
            'prediction': prediction,
            'model_used': model_name
        }
    
    def analyze_results(self):
        """Analyze A/B test results"""
        from scipy.stats import ttest_ind
        
        # Compare conversion rates or other metrics
        model_names = list(self.models.keys())
        if len(model_names) == 2:
            model_a_results = [r['prediction'] for r in self.results[model_names[0]]]
            model_b_results = [r['prediction'] for r in self.results[model_names[1]]]
            
            # Statistical significance test
            statistic, p_value = ttest_ind(model_a_results, model_b_results)
            
            return {
                'model_a_mean': np.mean(model_a_results),
                'model_b_mean': np.mean(model_b_results),
                'p_value': p_value,
                'significant': p_value < 0.05
            }
```

## 8. Infrastructure as Code
**Terraform for ML Infrastructure**:
```hcl
# main.tf
provider "aws" {
  region = "us-west-2"
}

# S3 bucket for model artifacts
resource "aws_s3_bucket" "ml_artifacts" {
  bucket = "ml-model-artifacts-${random_id.bucket_suffix.hex}"
}

# ECS cluster for model serving
resource "aws_ecs_cluster" "ml_cluster" {
  name = "ml-serving-cluster"
}

# ECS service for model API
resource "aws_ecs_service" "model_service" {
  name            = "model-api"
  cluster         = aws_ecs_cluster.ml_cluster.id
  task_definition = aws_ecs_task_definition.model_task.arn
  desired_count   = 2

  load_balancer {
    target_group_arn = aws_lb_target_group.model_tg.arn
    container_name   = "model-api"
    container_port   = 8000
  }
}

# Application Load Balancer
resource "aws_lb" "model_lb" {
  name               = "model-api-lb"
  internal           = false
  load_balancer_type = "application"
  subnets            = var.public_subnet_ids
}
```

## 9. Model Governance
**Model Approval Workflow**:
```python
class ModelGovernance:
    def __init__(self):
        self.approval_stages = ["development", "testing", "staging", "production"]
        self.required_checks = {
            "testing": ["unit_tests", "integration_tests", "performance_tests"],
            "staging": ["bias_check", "fairness_check", "security_scan"],
            "production": ["business_approval", "compliance_check"]
        }
    
    def submit_for_approval(self, model_id, current_stage, next_stage):
        """Submit model for next stage approval"""
        
        # Validate stage transition
        if not self._valid_transition(current_stage, next_stage):
            raise ValueError(f"Invalid transition: {current_stage} -> {next_stage}")
        
        # Check requirements
        missing_checks = self._check_requirements(model_id, next_stage)
        if missing_checks:
            return {
                "approved": False,
                "missing_checks": missing_checks
            }
        
        # Create approval request
        approval_request = {
            "model_id": model_id,
            "from_stage": current_stage,
            "to_stage": next_stage,
            "submitted_at": datetime.now(),
            "status": "pending"
        }
        
        return self._create_approval_request(approval_request)
    
    def _check_requirements(self, model_id, stage):
        """Check if all requirements are met for stage"""
        required = self.required_checks.get(stage, [])
        completed = self._get_completed_checks(model_id)
        
        return [check for check in required if check not in completed]
```

## 10. Cost Optimization
**Resource Management**:
```python
import boto3
from datetime import datetime, timedelta

class MLResourceOptimizer:
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.sagemaker = boto3.client('sagemaker')
    
    def optimize_training_instances(self):
        """Optimize training instance usage"""
        
        # Get running training jobs
        training_jobs = self.sagemaker.list_training_jobs(
            StatusEquals='InProgress'
        )
        
        optimizations = []
        for job in training_jobs['TrainingJobSummaries']:
            job_name = job['TrainingJobName']
            
            # Check if job is running longer than expected
            start_time = job['TrainingJobStartTime']
            duration = datetime.now(start_time.tzinfo) - start_time
            
            if duration > timedelta(hours=6):  # Threshold
                optimizations.append({
                    'job_name': job_name,
                    'action': 'review_long_running_job',
                    'duration_hours': duration.total_seconds() / 3600
                })
        
        return optimizations
    
    def schedule_inference_scaling(self):
        """Schedule auto-scaling for inference endpoints"""
        
        # Get endpoint configurations
        endpoints = self.sagemaker.list_endpoints()
        
        for endpoint in endpoints['Endpoints']:
            endpoint_name = endpoint['EndpointName']
            
            # Configure auto-scaling
            self._setup_autoscaling(endpoint_name)
    
    def _setup_autoscaling(self, endpoint_name):
        """Setup auto-scaling for endpoint"""
        autoscaling = boto3.client('application-autoscaling')
        
        # Register scalable target
        autoscaling.register_scalable_target(
            ServiceNamespace='sagemaker',
            ResourceId=f'endpoint/{endpoint_name}/variant/AllTraffic',
            ScalableDimension='sagemaker:variant:DesiredInstanceCount',
            MinCapacity=1,
            MaxCapacity=10
        )
        
        # Create scaling policy
        autoscaling.put_scaling_policy(
            PolicyName=f'{endpoint_name}-scaling-policy',
            ServiceNamespace='sagemaker',
            ResourceId=f'endpoint/{endpoint_name}/variant/AllTraffic',
            ScalableDimension='sagemaker:variant:DesiredInstanceCount',
            PolicyType='TargetTrackingScaling',
            TargetTrackingScalingPolicyConfiguration={
                'TargetValue': 70.0,
                'PredefinedMetricSpecification': {
                    'PredefinedMetricType': 'SageMakerVariantInvocationsPerInstance'
                }
            }
        )
```