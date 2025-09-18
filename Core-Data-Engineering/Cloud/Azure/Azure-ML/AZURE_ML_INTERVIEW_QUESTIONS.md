# Azure Machine Learning Interview Questions

## Basic Concepts

### 1. What is Azure Machine Learning and its key components?
**Answer:** Azure ML is Microsoft's cloud-based ML platform for building, training, and deploying ML models. Key components:

- **Workspace**: Central hub for ML resources
- **Compute**: Scalable compute resources
- **Datasets**: Data management and versioning
- **Experiments**: Track and manage ML runs
- **Models**: Model registry and management
- **Endpoints**: Model deployment and serving
- **Pipelines**: ML workflow orchestration

```python
from azureml.core import Workspace, Experiment, Dataset
from azureml.core.compute import ComputeTarget, AmlCompute

# Connect to workspace
ws = Workspace.from_config()
print(f"Workspace: {ws.name}, Location: {ws.location}")

# Create experiment
experiment = Experiment(workspace=ws, name="my-experiment")

# Create compute cluster
compute_config = AmlCompute.provisioning_configuration(
    vm_size="Standard_D2_v2",
    min_nodes=0,
    max_nodes=4,
    idle_seconds_before_scaledown=300
)

compute_target = ComputeTarget.create(
    ws, "my-compute-cluster", compute_config
)

# Register dataset
dataset = Dataset.Tabular.from_delimited_files(
    path="https://example.com/data.csv"
)
dataset = dataset.register(
    workspace=ws,
    name="my-dataset",
    description="Training dataset"
)
```

### 2. How do you create and manage Azure ML workspaces?
**Answer:** Workspaces are the top-level resource for Azure ML, containing all ML assets.

```python
from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication

# Create workspace
def create_workspace():
    ws = Workspace.create(
        name="my-ml-workspace",
        subscription_id="your-subscription-id",
        resource_group="my-resource-group",
        location="eastus",
        create_resource_group=True,
        sku="basic"
    )
    
    # Save workspace configuration
    ws.write_config(path=".", file_name="config.json")
    
    return ws

# Connect to existing workspace
def connect_to_workspace():
    # Method 1: From config file
    ws = Workspace.from_config()
    
    # Method 2: Direct connection
    ws = Workspace.get(
        name="my-ml-workspace",
        subscription_id="your-subscription-id",
        resource_group="my-resource-group"
    )
    
    # Method 3: Service principal authentication
    svc_pr = ServicePrincipalAuthentication(
        tenant_id="your-tenant-id",
        service_principal_id="your-client-id",
        service_principal_password="your-client-secret"
    )
    
    ws = Workspace.get(
        name="my-ml-workspace",
        auth=svc_pr,
        subscription_id="your-subscription-id",
        resource_group="my-resource-group"
    )
    
    return ws

# Workspace management
def manage_workspace(ws):
    # List compute targets
    compute_targets = ws.compute_targets
    for name, ct in compute_targets.items():
        print(f"Compute: {name}, Type: {type(ct)}")
    
    # List datasets
    datasets = ws.datasets
    for name, dataset in datasets.items():
        print(f"Dataset: {name}, Version: {dataset.version}")
    
    # List models
    models = ws.models
    for name, model_list in models.items():
        print(f"Model: {name}, Versions: {len(model_list)}")
    
    # Workspace details
    print(f"Subscription ID: {ws.subscription_id}")
    print(f"Resource Group: {ws.resource_group}")
    print(f"Location: {ws.location}")
    print(f"Storage Account: {ws.get_default_datastore().name}")
```

### 3. How do you work with Azure ML datasets?
**Answer:** Azure ML Datasets provide data abstraction and versioning capabilities.

```python
from azureml.core import Dataset, Datastore
from azureml.data.datapath import DataPath
import pandas as pd

# Create tabular dataset from CSV
def create_tabular_dataset(ws):
    # From web URL
    web_dataset = Dataset.Tabular.from_delimited_files(
        path="https://example.com/data.csv"
    )
    
    # From datastore
    datastore = ws.get_default_datastore()
    datastore_dataset = Dataset.Tabular.from_delimited_files(
        path=(datastore, "data/train.csv")
    )
    
    # From multiple files
    multi_file_dataset = Dataset.Tabular.from_delimited_files(
        path=[
            (datastore, "data/2021/*.csv"),
            (datastore, "data/2022/*.csv")
        ]
    )
    
    # Register dataset
    registered_dataset = web_dataset.register(
        workspace=ws,
        name="training-data",
        description="Training dataset for model",
        tags={"format": "CSV", "source": "web"},
        create_new_version=True
    )
    
    return registered_dataset

# Create file dataset
def create_file_dataset(ws):
    datastore = ws.get_default_datastore()
    
    file_dataset = Dataset.File.from_files(
        path=(datastore, "images/*.jpg")
    )
    
    file_dataset = file_dataset.register(
        workspace=ws,
        name="image-dataset",
        description="Image dataset for computer vision"
    )
    
    return file_dataset

# Dataset operations
def dataset_operations(dataset):
    # Take sample
    sample = dataset.take_sample(probability=0.1, seed=42)
    
    # Filter data
    filtered = dataset.filter(dataset["age"] > 18)
    
    # Select columns
    selected = dataset.keep_columns(["feature1", "feature2", "target"])
    
    # Drop columns
    dropped = dataset.drop_columns(["unnecessary_column"])
    
    # Convert to pandas DataFrame
    df = dataset.to_pandas_dataframe()
    
    # Dataset profile
    profile = dataset.profile()
    print(f"Row count: {profile.row_count}")
    print(f"Column count: {profile.column_count}")
    
    return df

# Dataset versioning
def dataset_versioning(ws):
    # Get latest version
    dataset = Dataset.get_by_name(ws, "training-data")
    
    # Get specific version
    dataset_v1 = Dataset.get_by_name(ws, "training-data", version=1)
    
    # List all versions
    all_versions = Dataset.get_all(ws, name="training-data")
    for version, dataset in all_versions.items():
        print(f"Version {version}: {dataset.description}")
    
    # Update dataset with new version
    new_data_path = "https://example.com/updated_data.csv"
    updated_dataset = Dataset.Tabular.from_delimited_files(path=new_data_path)
    
    updated_dataset = updated_dataset.register(
        workspace=ws,
        name="training-data",
        description="Updated training dataset",
        create_new_version=True
    )
    
    return updated_dataset

# Data drift monitoring
def setup_data_drift_monitoring(ws, baseline_dataset, target_dataset):
    from azureml.datadrift import DataDriftDetector
    
    # Create data drift detector
    drift_detector = DataDriftDetector.create_from_datasets(
        ws,
        "data-drift-detector",
        baseline_dataset,
        target_dataset,
        compute_target="my-compute-cluster",
        frequency="Week",
        feature_list=["feature1", "feature2", "feature3"],
        drift_threshold=0.3
    )
    
    # Run drift detection
    drift_detector.run(
        target_date=datetime.datetime.now(),
        services=["email"],
        emails=["admin@company.com"]
    )
    
    return drift_detector
```

### 4. How do you train models using Azure ML?
**Answer:** Azure ML supports various training approaches from AutoML to custom training scripts.

```python
from azureml.core import ScriptRunConfig, Environment
from azureml.train.automl import AutoMLConfig
from azureml.core.runconfig import RunConfiguration

# AutoML training
def automl_training(ws, dataset):
    automl_config = AutoMLConfig(
        task="classification",
        primary_metric="accuracy",
        training_data=dataset,
        label_column_name="target",
        n_cross_validations=5,
        compute_target="my-compute-cluster",
        experiment_timeout_minutes=30,
        max_concurrent_iterations=4,
        preprocess=True,
        enable_early_stopping=True,
        validation_size=0.2,
        model_explainability=True
    )
    
    experiment = Experiment(ws, "automl-experiment")
    run = experiment.submit(automl_config, show_output=True)
    
    # Get best model
    best_run, fitted_model = run.get_output()
    
    return best_run, fitted_model

# Custom script training
def custom_script_training(ws):
    # Create environment
    env = Environment.from_conda_specification(
        name="training-env",
        file_path="environment.yml"
    )
    
    # Or create environment from scratch
    env = Environment("training-env")
    env.python.conda_dependencies.add_pip_package("scikit-learn")
    env.python.conda_dependencies.add_pip_package("pandas")
    env.python.conda_dependencies.add_pip_package("numpy")
    
    # Script run configuration
    script_config = ScriptRunConfig(
        source_directory="./src",
        script="train.py",
        arguments=[
            "--data-folder", dataset.as_mount(),
            "--learning-rate", 0.01,
            "--batch-size", 32
        ],
        compute_target="my-compute-cluster",
        environment=env
    )
    
    experiment = Experiment(ws, "custom-training")
    run = experiment.submit(script_config)
    
    return run

# Distributed training
def distributed_training(ws):
    from azureml.core.runconfig import MpiConfiguration
    
    # MPI configuration for distributed training
    mpi_config = MpiConfiguration(process_count_per_node=2, node_count=2)
    
    script_config = ScriptRunConfig(
        source_directory="./src",
        script="distributed_train.py",
        arguments=["--epochs", 100],
        compute_target="my-compute-cluster",
        distributed_job_config=mpi_config,
        environment=env
    )
    
    experiment = Experiment(ws, "distributed-training")
    run = experiment.submit(script_config)
    
    return run

# Hyperparameter tuning
def hyperparameter_tuning(ws):
    from azureml.train.hyperdrive import RandomParameterSampling, BanditPolicy
    from azureml.train.hyperdrive import HyperDriveConfig, PrimaryMetricGoal
    from azureml.train.hyperdrive import choice, uniform, loguniform
    
    # Parameter sampling
    param_sampling = RandomParameterSampling({
        "learning_rate": loguniform(-6, -1),
        "batch_size": choice(16, 32, 64, 128),
        "hidden_size": choice(50, 100, 200),
        "dropout_rate": uniform(0.1, 0.5)
    })
    
    # Early termination policy
    early_termination_policy = BanditPolicy(
        slack_factor=0.1,
        evaluation_interval=1,
        delay_evaluation=5
    )
    
    # HyperDrive configuration
    hyperdrive_config = HyperDriveConfig(
        run_config=script_config,
        hyperparameter_sampling=param_sampling,
        policy=early_termination_policy,
        primary_metric_name="accuracy",
        primary_metric_goal=PrimaryMetricGoal.MAXIMIZE,
        max_total_runs=20,
        max_concurrent_runs=4
    )
    
    experiment = Experiment(ws, "hyperparameter-tuning")
    hyperdrive_run = experiment.submit(hyperdrive_config)
    
    # Get best run
    best_run = hyperdrive_run.get_best_run_by_primary_metric()
    
    return hyperdrive_run, best_run

# Training script example (train.py)
training_script = '''
import argparse
import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
from azureml.core import Run

# Get run context
run = Run.get_context()

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--data-folder", type=str, dest="data_folder")
parser.add_argument("--learning-rate", type=float, dest="learning_rate", default=0.01)
parser.add_argument("--batch-size", type=int, dest="batch_size", default=32)
args = parser.parse_args()

# Load data
data_path = os.path.join(args.data_folder, "data.csv")
df = pd.read_csv(data_path)

# Prepare data
X = df.drop("target", axis=1)
y = df["target"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

# Log metrics
run.log("accuracy", accuracy)
run.log("learning_rate", args.learning_rate)
run.log("batch_size", args.batch_size)

# Save model
os.makedirs("outputs", exist_ok=True)
joblib.dump(model, "outputs/model.pkl")

print(f"Training completed. Accuracy: {accuracy}")
'''
```

## Intermediate Concepts

### 5. How do you deploy models using Azure ML?
**Answer:** Azure ML provides multiple deployment options for different scenarios.

```python
from azureml.core import Model
from azureml.core.webservice import AciWebservice, AksWebservice, Webservice
from azureml.core.model import InferenceConfig
from azureml.core.environment import Environment

# Register model
def register_model(ws, run):
    model = run.register_model(
        model_name="my-model",
        model_path="outputs/model.pkl",
        description="Random Forest Classifier",
        tags={"algorithm": "RandomForest", "framework": "scikit-learn"}
    )
    
    return model

# Create inference configuration
def create_inference_config():
    # Create environment
    env = Environment.from_conda_specification(
        name="inference-env",
        file_path="inference_env.yml"
    )
    
    # Inference configuration
    inference_config = InferenceConfig(
        entry_script="score.py",
        environment=env
    )
    
    return inference_config

# Deploy to Azure Container Instances (ACI)
def deploy_to_aci(ws, model, inference_config):
    # ACI deployment configuration
    aci_config = AciWebservice.deploy_configuration(
        cpu_cores=1,
        memory_gb=1,
        tags={"environment": "dev"},
        description="Development deployment"
    )
    
    # Deploy service
    service = Model.deploy(
        workspace=ws,
        name="my-model-aci",
        models=[model],
        inference_config=inference_config,
        deployment_config=aci_config
    )
    
    service.wait_for_deployment(show_output=True)
    
    return service

# Deploy to Azure Kubernetes Service (AKS)
def deploy_to_aks(ws, model, inference_config):
    from azureml.core.compute import AksCompute, ComputeTarget
    
    # Create AKS cluster
    aks_config = AksCompute.provisioning_configuration(
        vm_size="Standard_D3_v2",
        agent_count=3,
        location="eastus"
    )
    
    aks_target = ComputeTarget.create(
        workspace=ws,
        name="my-aks-cluster",
        provisioning_configuration=aks_config
    )
    
    aks_target.wait_for_completion(show_output=True)
    
    # AKS deployment configuration
    aks_config = AksWebservice.deploy_configuration(
        cpu_cores=1,
        memory_gb=1,
        autoscale_enabled=True,
        autoscale_min_replicas=1,
        autoscale_max_replicas=10,
        autoscale_refresh_seconds=10,
        autoscale_target_utilization=70,
        collect_model_data=True,
        auth_enabled=True
    )
    
    # Deploy service
    service = Model.deploy(
        workspace=ws,
        name="my-model-aks",
        models=[model],
        inference_config=inference_config,
        deployment_config=aks_config,
        deployment_target=aks_target
    )
    
    service.wait_for_deployment(show_output=True)
    
    return service

# Batch inference
def batch_inference(ws, model):
    from azureml.pipeline.steps import ParallelRunStep, ParallelRunConfig
    from azureml.pipeline.core import Pipeline
    
    # Parallel run configuration
    parallel_run_config = ParallelRunConfig(
        source_directory="./batch_inference",
        entry_script="batch_score.py",
        mini_batch_size="5",
        error_threshold=10,
        output_action="append_row",
        environment=env,
        compute_target="my-compute-cluster",
        node_count=2
    )
    
    # Parallel run step
    parallel_run_step = ParallelRunStep(
        name="batch-inference-step",
        parallel_run_config=parallel_run_config,
        inputs=[input_dataset.as_named_input("input_data")],
        output=output_dataset,
        allow_reuse=False
    )
    
    # Create pipeline
    pipeline = Pipeline(workspace=ws, steps=[parallel_run_step])
    
    # Submit pipeline
    experiment = Experiment(ws, "batch-inference")
    pipeline_run = experiment.submit(pipeline)
    
    return pipeline_run

# Real-time inference testing
def test_web_service(service):
    import json
    
    # Test data
    test_data = {
        "data": [
            [1.0, 2.0, 3.0, 4.0],
            [2.0, 3.0, 4.0, 5.0]
        ]
    }
    
    # Convert to JSON
    input_data = json.dumps(test_data)
    
    # Make prediction
    predictions = service.run(input_data)
    
    print(f"Predictions: {predictions}")
    
    return predictions

# Scoring script example (score.py)
scoring_script = '''
import json
import joblib
import numpy as np
from azureml.core.model import Model

def init():
    global model
    # Load model
    model_path = Model.get_model_path("my-model")
    model = joblib.load(model_path)

def run(raw_data):
    try:
        # Parse input data
        data = json.loads(raw_data)["data"]
        data = np.array(data)
        
        # Make predictions
        predictions = model.predict(data)
        
        # Return predictions
        return predictions.tolist()
    
    except Exception as e:
        error = str(e)
        return {"error": error}
'''

# Model monitoring and data drift
def setup_model_monitoring(ws, service, dataset):
    from azureml.monitoring import ModelDataCollector
    
    # Enable data collection
    service.update(collect_model_data=True)
    
    # Create data drift detector
    from azureml.datadrift import DataDriftDetector
    
    drift_detector = DataDriftDetector.create_from_datasets(
        ws,
        "model-drift-detector",
        baseline_dataset=dataset,
        target_dataset=None,  # Will use inference data
        compute_target="my-compute-cluster",
        frequency="Week",
        drift_threshold=0.3
    )
    
    return drift_detector
```

### 6. How do you create and manage Azure ML pipelines?
**Answer:** Azure ML Pipelines enable reproducible ML workflows with dependency management.

```python
from azureml.pipeline.core import Pipeline, PipelineData
from azureml.pipeline.steps import PythonScriptStep
from azureml.core.runconfig import RunConfiguration

# Create pipeline steps
def create_pipeline_steps(ws, compute_target):
    # Data preparation step
    data_prep_step = PythonScriptStep(
        name="data-preparation",
        script_name="data_prep.py",
        arguments=[
            "--input-data", dataset.as_named_input("raw_data"),
            "--output-data", PipelineData("prepared_data", datastore=ws.get_default_datastore())
        ],
        compute_target=compute_target,
        source_directory="./pipeline_steps",
        runconfig=RunConfiguration()
    )
    
    # Feature engineering step
    feature_eng_step = PythonScriptStep(
        name="feature-engineering",
        script_name="feature_engineering.py",
        arguments=[
            "--input-data", data_prep_step.outputs["prepared_data"],
            "--output-data", PipelineData("features", datastore=ws.get_default_datastore())
        ],
        compute_target=compute_target,
        source_directory="./pipeline_steps"
    )
    
    # Model training step
    training_step = PythonScriptStep(
        name="model-training",
        script_name="train_model.py",
        arguments=[
            "--training-data", feature_eng_step.outputs["features"],
            "--model-output", PipelineData("trained_model", datastore=ws.get_default_datastore())
        ],
        compute_target=compute_target,
        source_directory="./pipeline_steps"
    )
    
    # Model evaluation step
    evaluation_step = PythonScriptStep(
        name="model-evaluation",
        script_name="evaluate_model.py",
        arguments=[
            "--model-input", training_step.outputs["trained_model"],
            "--test-data", feature_eng_step.outputs["features"],
            "--evaluation-output", PipelineData("evaluation", datastore=ws.get_default_datastore())
        ],
        compute_target=compute_target,
        source_directory="./pipeline_steps"
    )
    
    return [data_prep_step, feature_eng_step, training_step, evaluation_step]

# Create and run pipeline
def create_and_run_pipeline(ws, steps):
    # Create pipeline
    pipeline = Pipeline(workspace=ws, steps=steps)
    
    # Validate pipeline
    pipeline.validate()
    
    # Submit pipeline
    experiment = Experiment(ws, "ml-pipeline")
    pipeline_run = experiment.submit(pipeline)
    
    # Wait for completion
    pipeline_run.wait_for_completion(show_output=True)
    
    return pipeline_run

# Conditional pipeline steps
def create_conditional_pipeline(ws, compute_target):
    from azureml.pipeline.core import PipelineParameter
    from azureml.pipeline.steps import PythonScriptStep
    
    # Pipeline parameters
    model_accuracy_threshold = PipelineParameter(name="accuracy_threshold", default_value=0.85)
    
    # Training step
    training_step = PythonScriptStep(
        name="training",
        script_name="train_with_validation.py",
        arguments=["--threshold", model_accuracy_threshold],
        compute_target=compute_target,
        source_directory="./steps"
    )
    
    # Conditional deployment step
    deployment_step = PythonScriptStep(
        name="conditional-deployment",
        script_name="conditional_deploy.py",
        arguments=[
            "--model-path", training_step.outputs["model"],
            "--accuracy-threshold", model_accuracy_threshold
        ],
        compute_target=compute_target,
        source_directory="./steps"
    )
    
    # Set dependency
    deployment_step.run_after(training_step)
    
    pipeline = Pipeline(workspace=ws, steps=[training_step, deployment_step])
    
    return pipeline

# Parallel pipeline steps
def create_parallel_pipeline(ws, compute_target):
    from azureml.pipeline.steps import ParallelRunStep, ParallelRunConfig
    
    # Parallel processing configuration
    parallel_run_config = ParallelRunConfig(
        source_directory="./parallel_steps",
        entry_script="parallel_process.py",
        mini_batch_size="10",
        error_threshold=10,
        output_action="append_row",
        compute_target=compute_target,
        node_count=4,
        process_count_per_node=2
    )
    
    # Parallel step
    parallel_step = ParallelRunStep(
        name="parallel-processing",
        parallel_run_config=parallel_run_config,
        inputs=[large_dataset.as_named_input("input_data")],
        output=PipelineData("processed_data", datastore=ws.get_default_datastore())
    )
    
    # Aggregation step
    aggregation_step = PythonScriptStep(
        name="aggregation",
        script_name="aggregate_results.py",
        arguments=["--input-data", parallel_step.outputs["processed_data"]],
        compute_target=compute_target,
        source_directory="./steps"
    )
    
    pipeline = Pipeline(workspace=ws, steps=[parallel_step, aggregation_step])
    
    return pipeline

# Pipeline scheduling
def schedule_pipeline(ws, pipeline):
    from azureml.pipeline.core.schedule import ScheduleRecurrence, Schedule
    
    # Create recurrence
    recurrence = ScheduleRecurrence(
        frequency="Week",
        interval=1,
        week_days=["Monday"],
        time_of_day="02:00"
    )
    
    # Create schedule
    schedule = Schedule.create(
        workspace=ws,
        name="weekly-training-schedule",
        pipeline_id=pipeline.id,
        experiment_name="scheduled-training",
        recurrence=recurrence,
        description="Weekly model retraining"
    )
    
    return schedule

# Pipeline monitoring
def monitor_pipeline_runs(ws, pipeline_id):
    from azureml.core import Experiment
    
    # Get pipeline runs
    experiment = Experiment(ws, "ml-pipeline")
    runs = experiment.get_runs()
    
    for run in runs:
        if hasattr(run, 'pipeline_run_id'):
            print(f"Run ID: {run.id}")
            print(f"Status: {run.status}")
            print(f"Start time: {run.start_time}")
            print(f"End time: {run.end_time}")
            
            # Get step runs
            step_runs = run.get_children()
            for step_run in step_runs:
                print(f"  Step: {step_run.name}, Status: {step_run.status}")
```

### 7. How do you implement MLOps with Azure ML?
**Answer:** Azure ML provides comprehensive MLOps capabilities including CI/CD, monitoring, and governance.

```python
from azureml.core import Model, Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
import json

# Model registry and versioning
class ModelRegistry:
    def __init__(self, workspace):
        self.ws = workspace
    
    def register_model(self, run, model_name, model_path="outputs/model.pkl"):
        # Register model with metadata
        model = run.register_model(
            model_name=model_name,
            model_path=model_path,
            description=f"Model trained on {run.start_time}",
            tags={
                "algorithm": "RandomForest",
                "framework": "scikit-learn",
                "accuracy": run.get_metrics().get("accuracy", 0),
                "run_id": run.id
            },
            properties={
                "training_dataset": run.input_datasets.get("training_data", {}).get("name", "unknown"),
                "validation_accuracy": run.get_metrics().get("val_accuracy", 0)
            }
        )
        
        return model
    
    def get_latest_model(self, model_name, stage="Production"):
        models = Model.list(self.ws, name=model_name, tags=[["stage", stage]])
        if models:
            return max(models, key=lambda x: x.version)
        return None
    
    def promote_model(self, model, stage):
        # Update model tags
        model.add_tags({"stage": stage})
        
        # If promoting to production, demote previous production model
        if stage == "Production":
            current_prod_models = Model.list(
                self.ws, 
                name=model.name, 
                tags=[["stage", "Production"]]
            )
            
            for prod_model in current_prod_models:
                if prod_model.version != model.version:
                    prod_model.add_tags({"stage": "Archived"})

# CI/CD Pipeline integration
def create_azure_devops_pipeline():
    azure_pipeline_yaml = '''
    trigger:
    - main

    pool:
      vmImage: 'ubuntu-latest'

    variables:
      azureServiceConnectionId: 'azure-ml-connection'
      workspaceName: 'my-ml-workspace'
      resourceGroupName: 'my-resource-group'

    stages:
    - stage: DataValidation
      jobs:
      - job: ValidateData
        steps:
        - task: UsePythonVersion@0
          inputs:
            versionSpec: '3.8'
        
        - script: |
            pip install azureml-sdk pandas numpy
            python validate_data.py
          displayName: 'Validate Training Data'

    - stage: ModelTraining
      dependsOn: DataValidation
      condition: succeeded()
      jobs:
      - job: TrainModel
        steps:
        - script: |
            python train_model.py --experiment-name $(Build.BuildNumber)
          displayName: 'Train Model'
          env:
            AZURE_CLIENT_ID: $(AZURE_CLIENT_ID)
            AZURE_CLIENT_SECRET: $(AZURE_CLIENT_SECRET)
            AZURE_TENANT_ID: $(AZURE_TENANT_ID)

    - stage: ModelValidation
      dependsOn: ModelTraining
      jobs:
      - job: ValidateModel
        steps:
        - script: |
            python validate_model.py --model-name my-model --threshold 0.85
          displayName: 'Validate Model Performance'

    - stage: ModelDeployment
      dependsOn: ModelValidation
      condition: succeeded()
      jobs:
      - deployment: DeployModel
        environment: 'production'
        strategy:
          runOnce:
            deploy:
              steps:
              - script: |
                  python deploy_model.py --model-name my-model --environment production
                displayName: 'Deploy Model to Production'
    '''
    
    return azure_pipeline_yaml

# Model monitoring and alerting
def setup_model_monitoring(ws, service_name):
    from azureml.monitoring import ModelDataCollector
    from azureml.core.webservice import Webservice
    
    # Get deployed service
    service = Webservice(ws, service_name)
    
    # Enable application insights
    service.update(enable_app_insights=True)
    
    # Set up custom monitoring
    monitoring_script = '''
import json
import logging
from azureml.monitoring import ModelDataCollector
from azureml.core import Run

def init():
    global model, inputs_collector, predictions_collector
    
    # Initialize model data collectors
    inputs_collector = ModelDataCollector(
        "my-model", 
        designation="inputs", 
        feature_names=["feature1", "feature2", "feature3"]
    )
    
    predictions_collector = ModelDataCollector(
        "my-model",
        designation="predictions",
        feature_names=["prediction", "probability"]
    )

def run(raw_data):
    try:
        data = json.loads(raw_data)["data"]
        
        # Collect input data
        inputs_collector.collect(data)
        
        # Make prediction
        predictions = model.predict(data)
        probabilities = model.predict_proba(data)
        
        # Collect prediction data
        prediction_data = [[pred, prob.max()] for pred, prob in zip(predictions, probabilities)]
        predictions_collector.collect(prediction_data)
        
        return predictions.tolist()
        
    except Exception as e:
        logging.error(f"Error in scoring: {str(e)}")
        return {"error": str(e)}
    '''

# Automated model retraining
def setup_automated_retraining(ws):
    from azureml.pipeline.core.schedule import ScheduleRecurrence, Schedule
    
    # Create retraining pipeline
    retraining_pipeline = create_retraining_pipeline(ws)
    
    # Schedule weekly retraining
    recurrence = ScheduleRecurrence(
        frequency="Week",
        interval=1,
        week_days=["Sunday"],
        time_of_day="02:00"
    )
    
    schedule = Schedule.create(
        workspace=ws,
        name="automated-retraining",
        pipeline_id=retraining_pipeline.id,
        experiment_name="automated-retraining",
        recurrence=recurrence
    )
    
    return schedule

def create_retraining_pipeline(ws):
    # Data drift detection step
    drift_detection_step = PythonScriptStep(
        name="drift-detection",
        script_name="detect_drift.py",
        compute_target="my-compute-cluster",
        source_directory="./retraining_steps"
    )
    
    # Conditional retraining step
    retraining_step = PythonScriptStep(
        name="retrain-model",
        script_name="retrain_model.py",
        compute_target="my-compute-cluster",
        source_directory="./retraining_steps"
    )
    
    # Model validation step
    validation_step = PythonScriptStep(
        name="validate-retrained-model",
        script_name="validate_model.py",
        compute_target="my-compute-cluster",
        source_directory="./retraining_steps"
    )
    
    # Conditional deployment step
    deployment_step = PythonScriptStep(
        name="deploy-if-better",
        script_name="conditional_deploy.py",
        compute_target="my-compute-cluster",
        source_directory="./retraining_steps"
    )
    
    # Set dependencies
    retraining_step.run_after(drift_detection_step)
    validation_step.run_after(retraining_step)
    deployment_step.run_after(validation_step)
    
    pipeline = Pipeline(
        workspace=ws,
        steps=[drift_detection_step, retraining_step, validation_step, deployment_step]
    )
    
    return pipeline

# Model governance and compliance
class ModelGovernance:
    def __init__(self, workspace):
        self.ws = workspace
    
    def audit_model(self, model_name):
        models = Model.list(self.ws, name=model_name)
        
        audit_report = {
            "model_name": model_name,
            "total_versions": len(models),
            "versions": []
        }
        
        for model in models:
            version_info = {
                "version": model.version,
                "created_time": model.created_time,
                "tags": model.tags,
                "properties": model.properties,
                "datasets": model.datasets,
                "run_id": model.run_id
            }
            audit_report["versions"].append(version_info)
        
        return audit_report
    
    def compliance_check(self, model):
        compliance_status = {
            "model_documented": bool(model.description),
            "training_data_tracked": "training_dataset" in model.properties,
            "performance_metrics_logged": bool(model.tags.get("accuracy")),
            "approval_status": model.tags.get("approved", "pending")
        }
        
        compliance_status["compliant"] = all(compliance_status.values())
        
        return compliance_status

# Usage example
if __name__ == "__main__":
    # Initialize workspace
    ws = Workspace.from_config()
    
    # Set up model registry
    registry = ModelRegistry(ws)
    
    # Set up monitoring
    setup_model_monitoring(ws, "my-model-service")
    
    # Set up automated retraining
    schedule = setup_automated_retraining(ws)
    
    print("MLOps setup completed successfully!")
```

This comprehensive Azure ML interview questions set covers fundamental concepts through advanced MLOps implementations, providing practical examples for workspace management, model training, deployment, pipelines, and production monitoring.