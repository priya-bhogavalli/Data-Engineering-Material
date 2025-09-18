# Kubeflow Interview Questions

## Basic Concepts

### 1. What is Kubeflow and its key components?
**Answer:** Kubeflow is a machine learning toolkit for Kubernetes. Key components:

- **Kubeflow Pipelines**: ML workflow orchestration
- **Katib**: Hyperparameter tuning and AutoML
- **KFServing**: Model serving platform
- **Notebooks**: Jupyter notebook management
- **Training Operators**: Distributed training (TFJob, PyTorchJob)
- **Multi-tenancy**: Namespace isolation and resource management

```python
# Kubeflow Pipeline example
import kfp
from kfp import dsl
from kfp.components import create_component_from_func

@create_component_from_func
def preprocess_data(input_path: str, output_path: str):
    import pandas as pd
    df = pd.read_csv(input_path)
    # Preprocessing logic
    df.to_csv(output_path, index=False)

@create_component_from_func  
def train_model(data_path: str, model_path: str, learning_rate: float = 0.01):
    from sklearn.ensemble import RandomForestClassifier
    import pandas as pd
    import joblib
    
    df = pd.read_csv(data_path)
    X, y = df.drop('target', axis=1), df['target']
    
    model = RandomForestClassifier()
    model.fit(X, y)
    joblib.dump(model, model_path)

@dsl.pipeline(name='ml-pipeline', description='Basic ML pipeline')
def ml_pipeline(input_data: str, learning_rate: float = 0.01):
    preprocess_task = preprocess_data(input_data, '/tmp/processed.csv')
    train_task = train_model(preprocess_task.output, '/tmp/model.pkl', learning_rate)

# Submit pipeline
client = kfp.Client()
client.create_run_from_pipeline_func(ml_pipeline, arguments={'input_data': 's3://bucket/data.csv'})
```

### 2. How do you create and manage Kubeflow Pipelines?
**Answer:** Kubeflow Pipelines enable ML workflow orchestration with reusable components.

```python
import kfp
from kfp import dsl
from kfp.components import InputPath, OutputPath, create_component_from_func

# Component creation
@create_component_from_func
def data_validation(
    input_path: InputPath(),
    validation_report: OutputPath(),
    min_rows: int = 1000
):
    import pandas as pd
    import json
    
    df = pd.read_csv(input_path)
    
    validation_results = {
        'row_count': len(df),
        'column_count': len(df.columns),
        'missing_values': df.isnull().sum().sum(),
        'valid': len(df) >= min_rows
    }
    
    with open(validation_report, 'w') as f:
        json.dump(validation_results, f)

@create_component_from_func
def feature_engineering(
    input_path: InputPath(),
    output_path: OutputPath(),
    feature_config: dict
):
    import pandas as pd
    
    df = pd.read_csv(input_path)
    
    # Apply feature engineering
    if feature_config.get('normalize'):
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    
    df.to_csv(output_path, index=False)

# Pipeline with conditions
@dsl.pipeline(name='advanced-ml-pipeline')
def advanced_pipeline(
    data_source: str,
    model_type: str = 'random_forest',
    enable_validation: bool = True
):
    # Data validation step
    if enable_validation:
        validation_task = data_validation(data_source)
        
        # Conditional execution based on validation
        with dsl.Condition(validation_task.outputs['validation_report'], '==', 'valid'):
            feature_task = feature_engineering(
                validation_task.outputs['output_path'],
                feature_config={'normalize': True}
            )
    else:
        feature_task = feature_engineering(
            data_source,
            feature_config={'normalize': True}
        )
    
    # Model training with different algorithms
    if model_type == 'random_forest':
        train_task = train_rf_model(feature_task.outputs['output_path'])
    elif model_type == 'xgboost':
        train_task = train_xgb_model(feature_task.outputs['output_path'])
    
    # Model evaluation
    eval_task = evaluate_model(
        train_task.outputs['model_path'],
        feature_task.outputs['output_path']
    )
    
    return eval_task.outputs['metrics']
```

### 3. How do you perform hyperparameter tuning with Katib?
**Answer:** Katib provides automated hyperparameter optimization for ML models.

```yaml
# Katib Experiment YAML
apiVersion: kubeflow.org/v1beta1
kind: Experiment
metadata:
  name: hyperparameter-tuning
spec:
  algorithm:
    algorithmName: bayesianoptimization
  objective:
    type: maximize
    goal: 0.95
    objectiveMetricName: accuracy
  parameters:
  - name: learning_rate
    parameterType: double
    feasibleSpace:
      min: "0.001"
      max: "0.1"
  - name: batch_size
    parameterType: int
    feasibleSpace:
      min: "16"
      max: "128"
  - name: num_layers
    parameterType: int
    feasibleSpace:
      min: "2"
      max: "6"
  trialTemplate:
    primaryContainerName: training-container
    trialSpec:
      apiVersion: batch/v1
      kind: Job
      spec:
        template:
          spec:
            containers:
            - name: training-container
              image: my-training-image:latest
              command:
              - python
              - train.py
              - --learning_rate=${trialParameters.learningRate}
              - --batch_size=${trialParameters.batchSize}
              - --num_layers=${trialParameters.numLayers}
```

```python
# Python client for Katib
from kubeflow.katib import KatibClient

def create_katib_experiment():
    katib_client = KatibClient()
    
    experiment = {
        "apiVersion": "kubeflow.org/v1beta1",
        "kind": "Experiment",
        "metadata": {"name": "python-experiment"},
        "spec": {
            "algorithm": {"algorithmName": "random"},
            "objective": {
                "type": "maximize",
                "objectiveMetricName": "accuracy"
            },
            "parameters": [
                {
                    "name": "lr",
                    "parameterType": "double",
                    "feasibleSpace": {"min": "0.01", "max": "0.1"}
                }
            ],
            "trialTemplate": {
                "primaryContainerName": "training-container",
                "trialSpec": {
                    "apiVersion": "batch/v1",
                    "kind": "Job",
                    "spec": {
                        "template": {
                            "spec": {
                                "containers": [{
                                    "name": "training-container",
                                    "image": "training:latest",
                                    "command": ["python", "train.py"]
                                }]
                            }
                        }
                    }
                }
            }
        }
    }
    
    katib_client.create_experiment(experiment)
    return experiment
```

## Intermediate Concepts

### 4. How do you deploy models using KFServing?
**Answer:** KFServing provides serverless model serving on Kubernetes.

```yaml
# KFServing InferenceService
apiVersion: serving.kubeflow.org/v1beta1
kind: InferenceService
metadata:
  name: sklearn-model
spec:
  predictor:
    sklearn:
      storageUri: gs://bucket/sklearn-model
      resources:
        requests:
          cpu: 100m
          memory: 1Gi
        limits:
          cpu: 1
          memory: 2Gi
  transformer:
    custom:
      container:
        image: transformer:latest
        env:
        - name: STORAGE_URI
          value: gs://bucket/transformer
```

```python
# Python client for KFServing
from kfserving import KFServingClient, V1beta1InferenceService, V1beta1PredictorSpec

def deploy_model_kfserving():
    kfserving = KFServingClient()
    
    # Create InferenceService
    isvc = V1beta1InferenceService(
        api_version="serving.kubeflow.org/v1beta1",
        kind="InferenceService",
        metadata={"name": "pytorch-model"},
        spec={
            "predictor": {
                "pytorch": {
                    "storageUri": "gs://bucket/pytorch-model",
                    "resources": {
                        "requests": {"cpu": "100m", "memory": "1Gi"},
                        "limits": {"cpu": "1", "memory": "2Gi"}
                    }
                }
            }
        }
    )
    
    kfserving.create(isvc)
    
    # Wait for deployment
    kfserving.wait_isvc_ready("pytorch-model", timeout_seconds=300)
    
    return isvc

# Custom predictor
class CustomPredictor:
    def __init__(self):
        self.model = None
        
    def load(self):
        import joblib
        self.model = joblib.load('/mnt/models/model.pkl')
        
    def predict(self, request):
        inputs = request["instances"]
        predictions = self.model.predict(inputs)
        return {"predictions": predictions.tolist()}

# Model serving with custom logic
def create_custom_serving():
    serving_code = '''
from kfserving import KFModel, ModelServer
import joblib
import numpy as np

class CustomModel(KFModel):
    def __init__(self, name: str):
        super().__init__(name)
        self.model = None
        
    def load(self):
        self.model = joblib.load('/mnt/models/model.pkl')
        self.ready = True
        
    def predict(self, request):
        instances = request["instances"]
        predictions = self.model.predict(np.array(instances))
        return {"predictions": predictions.tolist()}

if __name__ == "__main__":
    model = CustomModel("custom-model")
    ModelServer().start([model])
    '''
    
    return serving_code
```

This focused Kubeflow interview questions set covers the essential components and workflows for ML on Kubernetes, providing practical examples for pipelines, hyperparameter tuning, and model serving.