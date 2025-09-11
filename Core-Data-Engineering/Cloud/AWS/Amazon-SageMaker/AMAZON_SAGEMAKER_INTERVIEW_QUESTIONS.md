# Amazon SageMaker - Interview Questions

## Table of Contents
1. [Basic (1-30)](#basic-1-30)
2. [Intermediate (31-60)](#intermediate-31-60)
3. [Advanced (61-90)](#advanced-61-90)
4. [Architecture & Performance (91-120)](#architecture--performance-91-120)
5. [Streaming & Real-time (121-150)](#streaming--real-time-121-150)
6. [Production & Operations (151-180)](#production--operations-151-180)
7. [Scenario-Based (181-200)](#scenario-based-181-200)

---

## Basic (1-30)

### 1. What is Amazon SageMaker and what are its core components?

**Answer:**
Amazon SageMaker is a fully managed machine learning platform that provides tools for the complete ML lifecycle.

**Core Components:**
- **SageMaker Studio**: Integrated development environment
- **Processing Jobs**: Data preprocessing and feature engineering
- **Training Jobs**: Model training with built-in or custom algorithms
- **Model Registry**: Model versioning and management
- **Endpoints**: Real-time and batch inference
- **Pipelines**: ML workflow orchestration

```python
import sagemaker
from sagemaker import get_execution_role

# Initialize SageMaker session
sagemaker_session = sagemaker.Session()
role = get_execution_role()
```

### 2. How do you create a SageMaker training job?

**Answer:**
```python
from sagemaker.tensorflow import TensorFlow

# Create estimator
estimator = TensorFlow(
    entry_point="train.py",
    role=role,
    instance_count=1,
    instance_type="ml.m5.xlarge",
    framework_version="2.8",
    py_version="py39",
    hyperparameters={
        "epochs": 100,
        "batch-size": 64
    }
)

# Start training
estimator.fit({"train": "s3://bucket/train/", "validation": "s3://bucket/val/"})
```

### 3. What are the different data input modes in SageMaker?

**Answer:**
**Three Input Modes:**

```python
from sagemaker.inputs import TrainingInput

# 1. File Mode - Downloads data to local storage
file_input = TrainingInput(
    s3_data="s3://bucket/data/",
    input_mode="File"
)

# 2. Pipe Mode - Streams data directly
pipe_input = TrainingInput(
    s3_data="s3://bucket/data/",
    input_mode="Pipe"
)

# 3. Fast File Mode - Optimized for large datasets
fast_file_input = TrainingInput(
    s3_data="s3://bucket/data/",
    input_mode="FastFile"
)
```

### 4. How do you deploy a model to a SageMaker endpoint?

**Answer:**
```python
# Deploy trained model
predictor = estimator.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large",
    endpoint_name="my-endpoint"
)

# Make predictions
result = predictor.predict(data)

# Clean up
predictor.delete_endpoint()
```

### 5. What is SageMaker Processing and when would you use it?

**Answer:**
SageMaker Processing runs data preprocessing, feature engineering, and model evaluation jobs.

```python
from sagemaker.processing import ProcessingInput, ProcessingOutput, ScriptProcessor

processor = ScriptProcessor(
    command=["python3"],
    image_uri="python:3.8",
    role=role,
    instance_count=1,
    instance_type="ml.m5.xlarge"
)

processor.run(
    code="preprocess.py",
    inputs=[ProcessingInput(source="s3://bucket/raw/", destination="/opt/ml/processing/input")],
    outputs=[ProcessingOutput(source="/opt/ml/processing/output", destination="s3://bucket/processed/")]
)
```

### 6. How do you handle different data formats in SageMaker?

**Answer:**
```python
# CSV data
csv_input = TrainingInput(
    s3_data="s3://bucket/data.csv",
    content_type="text/csv"
)

# Parquet data
parquet_input = TrainingInput(
    s3_data="s3://bucket/data.parquet",
    content_type="application/x-parquet"
)

# JSON Lines
jsonl_input = TrainingInput(
    s3_data="s3://bucket/data.jsonl",
    content_type="application/jsonlines"
)

# RecordIO-Protobuf (for built-in algorithms)
recordio_input = TrainingInput(
    s3_data="s3://bucket/data.recordio",
    content_type="application/x-recordio-protobuf"
)
```

### 7. What are SageMaker built-in algorithms?

**Answer:**
**Categories of Built-in Algorithms:**

```python
# 1. Supervised Learning
from sagemaker.xgboost import XGBoost
from sagemaker.linear_learner import LinearLearner

xgb = XGBoost(
    entry_point="train.py",
    framework_version="1.5-1",
    instance_type="ml.m5.xlarge"
)

# 2. Unsupervised Learning
from sagemaker.kmeans import KMeans

kmeans = KMeans(
    role=role,
    instance_count=1,
    instance_type="ml.m5.xlarge",
    k=10
)

# 3. Text Analysis
from sagemaker.blazingtext import BlazingText

blazingtext = BlazingText(
    role=role,
    instance_count=1,
    instance_type="ml.m5.xlarge",
    mode="supervised"
)
```

### 8. How do you implement hyperparameter tuning in SageMaker?

**Answer:**
```python
from sagemaker.tuner import HyperparameterTuner, ContinuousParameter, IntegerParameter

# Define hyperparameter ranges
hyperparameter_ranges = {
    "learning_rate": ContinuousParameter(0.001, 0.1),
    "batch_size": IntegerParameter(32, 256),
    "num_layers": IntegerParameter(2, 10)
}

# Create tuner
tuner = HyperparameterTuner(
    estimator=base_estimator,
    objective_metric_name="validation:accuracy",
    objective_type="Maximize",
    hyperparameter_ranges=hyperparameter_ranges,
    max_jobs=50,
    max_parallel_jobs=5
)

# Start tuning
tuner.fit({"train": train_data, "validation": val_data})
```

### 9. What is the SageMaker Model Registry?

**Answer:**
Model Registry provides model versioning, approval workflows, and deployment tracking.

```python
from sagemaker.model import Model

# Register model
model_package = model.register(
    content_types=["application/json"],
    response_types=["application/json"],
    inference_instances=["ml.m5.large"],
    transform_instances=["ml.m5.xlarge"],
    model_package_group_name="customer-churn-models",
    approval_status="PendingManualApproval",
    model_metrics={
        "accuracy": {"value": 0.95},
        "precision": {"value": 0.92}
    }
)
```

### 10. How do you perform batch inference in SageMaker?

**Answer:**
```python
# Create transformer
transformer = model.transformer(
    instance_count=1,
    instance_type="ml.m5.xlarge",
    output_path="s3://bucket/batch-output/"
)

# Run batch transform
transformer.transform(
    data="s3://bucket/batch-input/",
    content_type="text/csv",
    split_type="Line"
)

# Wait for completion
transformer.wait()
```

### 11. What are SageMaker instance types and how do you choose them?

**Answer:**
**Instance Categories:**

```python
# General Purpose
general_instances = [
    "ml.m5.large",    # 2 vCPU, 8 GB RAM
    "ml.m5.xlarge",   # 4 vCPU, 16 GB RAM
    "ml.m5.2xlarge"   # 8 vCPU, 32 GB RAM
]

# Compute Optimized
compute_instances = [
    "ml.c5.large",    # 2 vCPU, 4 GB RAM
    "ml.c5.xlarge",   # 4 vCPU, 8 GB RAM
    "ml.c5.2xlarge"   # 8 vCPU, 16 GB RAM
]

# Memory Optimized
memory_instances = [
    "ml.r5.large",    # 2 vCPU, 16 GB RAM
    "ml.r5.xlarge",   # 4 vCPU, 32 GB RAM
    "ml.r5.2xlarge"   # 8 vCPU, 64 GB RAM
]

# GPU Instances
gpu_instances = [
    "ml.p3.2xlarge",  # 1 V100 GPU
    "ml.p3.8xlarge",  # 4 V100 GPUs
    "ml.p3.16xlarge"  # 8 V100 GPUs
]
```

### 12. How do you use custom Docker containers in SageMaker?

**Answer:**
```python
# Build custom container
# Dockerfile
"""
FROM python:3.8-slim

RUN pip install scikit-learn pandas numpy

COPY train.py /opt/ml/code/train.py
COPY serve.py /opt/ml/code/serve.py

ENV SAGEMAKER_PROGRAM train.py
"""

# Use custom container
from sagemaker.estimator import Estimator

estimator = Estimator(
    image_uri="123456789012.dkr.ecr.us-east-1.amazonaws.com/my-algorithm:latest",
    role=role,
    instance_count=1,
    instance_type="ml.m5.xlarge",
    output_path="s3://bucket/models/"
)
```

### 13. What is SageMaker Autopilot?

**Answer:**
Autopilot is SageMaker's AutoML service that automatically builds, trains, and tunes ML models.

```python
from sagemaker.automl.automl import AutoML

# Create AutoML job
automl = AutoML(
    role=role,
    target_attribute_name="target",
    output_path="s3://bucket/autopilot-output/",
    sagemaker_session=sagemaker_session
)

# Fit AutoML
automl.fit(
    inputs="s3://bucket/training-data.csv",
    job_name="autopilot-job",
    wait=False
)

# Get best candidate
best_candidate = automl.best_candidate()
print(f"Best candidate: {best_candidate['CandidateName']}")
```

### 14. How do you implement data validation in SageMaker?

**Answer:**
```python
# Data validation script
def validate_data():
    import pandas as pd
    import numpy as np
    
    # Load data
    df = pd.read_csv("/opt/ml/processing/input/data.csv")
    
    # Validation checks
    validation_report = {
        "total_rows": len(df),
        "missing_values": df.isnull().sum().to_dict(),
        "data_types": df.dtypes.to_dict(),
        "duplicates": df.duplicated().sum(),
        "outliers": {}
    }
    
    # Outlier detection
    for col in df.select_dtypes(include=[np.number]).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
        validation_report["outliers"][col] = outliers
    
    # Save validation report
    import json
    with open("/opt/ml/processing/output/validation_report.json", "w") as f:
        json.dump(validation_report, f, indent=2)

# Processing job for validation
validation_processor = ScriptProcessor(
    command=["python3"],
    image_uri="python:3.8",
    role=role,
    instance_count=1,
    instance_type="ml.m5.large"
)

validation_processor.run(
    code="validate_data.py",
    inputs=[ProcessingInput(source="s3://bucket/raw-data/", destination="/opt/ml/processing/input")],
    outputs=[ProcessingOutput(source="/opt/ml/processing/output", destination="s3://bucket/validation-reports/")]
)
```

### 15. What are SageMaker Experiments and how do you use them?

**Answer:**
Experiments help organize, track, and compare ML training runs.

```python
from sagemaker.experiments import experiment

# Create experiment
my_experiment = experiment.Experiment.create(
    experiment_name="customer-churn-experiment",
    description="Experiment to predict customer churn"
)

# Create trial
from sagemaker.experiments import trial

my_trial = trial.Trial.create(
    trial_name="xgboost-trial-1",
    experiment_name=my_experiment.experiment_name
)

# Run training with experiment tracking
estimator = XGBoost(
    entry_point="train.py",
    framework_version="1.5-1",
    instance_type="ml.m5.xlarge",
    role=role
)

# Associate training job with trial
estimator.fit(
    inputs={"train": train_data},
    experiment_config={
        "ExperimentName": my_experiment.experiment_name,
        "TrialName": my_trial.trial_name,
        "TrialComponentDisplayName": "Training"
    }
)
```

### 16. How do you handle imbalanced datasets in SageMaker?

**Answer:**
```python
# Preprocessing for imbalanced data
def handle_imbalanced_data():
    import pandas as pd
    from sklearn.utils import resample
    from imblearn.over_sampling import SMOTE
    
    # Load data
    df = pd.read_csv("/opt/ml/processing/input/data.csv")
    
    # Separate features and target
    X = df.drop('target', axis=1)
    y = df['target']
    
    # Method 1: Undersampling majority class
    df_majority = df[df.target == 0]
    df_minority = df[df.target == 1]
    
    df_majority_downsampled = resample(
        df_majority,
        replace=False,
        n_samples=len(df_minority),
        random_state=42
    )
    
    df_balanced = pd.concat([df_majority_downsampled, df_minority])
    
    # Method 2: SMOTE oversampling
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)
    
    # Save balanced data
    df_balanced.to_csv("/opt/ml/processing/output/balanced_data.csv", index=False)

# Built-in algorithm with class weights
linear_learner = LinearLearner(
    role=role,
    instance_count=1,
    instance_type="ml.m5.xlarge",
    predictor_type="binary_classifier",
    positive_example_weight_mult=5.0  # Handle imbalanced classes
)
```

### 17. What is SageMaker Feature Store?

**Answer:**
Feature Store is a centralized repository for ML features with online and offline access.

```python
from sagemaker.feature_store.feature_group import FeatureGroup
from sagemaker.feature_store.feature_definition import FeatureDefinition, FeatureTypeEnum

# Define feature group
feature_group = FeatureGroup(
    name="customer-features",
    sagemaker_session=sagemaker_session
)

# Define features
feature_definitions = [
    FeatureDefinition(feature_name="customer_id", feature_type=FeatureTypeEnum.STRING),
    FeatureDefinition(feature_name="age", feature_type=FeatureTypeEnum.INTEGRAL),
    FeatureDefinition(feature_name="income", feature_type=FeatureTypeEnum.FRACTIONAL),
    FeatureDefinition(feature_name="event_time", feature_type=FeatureTypeEnum.STRING)
]

# Create feature group
feature_group.create(
    s3_uri="s3://bucket/feature-store/",
    record_identifier_name="customer_id",
    event_time_feature_name="event_time",
    role_arn=role,
    feature_definitions=feature_definitions,
    enable_online_store=True
)

# Ingest data
import pandas as pd

data = pd.DataFrame({
    "customer_id": ["1", "2", "3"],
    "age": [25, 35, 45],
    "income": [50000.0, 75000.0, 100000.0],
    "event_time": ["2024-01-01T00:00:00Z", "2024-01-01T00:00:00Z", "2024-01-01T00:00:00Z"]
})

feature_group.ingest(data_frame=data, max_workers=3, wait=True)
```

### 18. How do you implement A/B testing for ML models in SageMaker?

**Answer:**
```python
# Multi-variant endpoint for A/B testing
from sagemaker.model import Model

# Create models
model_a = Model(
    image_uri=training_image,
    model_data="s3://bucket/model-a/model.tar.gz",
    role=role,
    name="model-a"
)

model_b = Model(
    image_uri=training_image,
    model_data="s3://bucket/model-b/model.tar.gz",
    role=role,
    name="model-b"
)

# Deploy with traffic splitting
from sagemaker.multidatamodel import MultiDataModel

# Create endpoint configuration with variants
endpoint_config_name = "ab-test-config"

sagemaker_client = boto3.client('sagemaker')

sagemaker_client.create_endpoint_config(
    EndpointConfigName=endpoint_config_name,
    ProductionVariants=[
        {
            'VariantName': 'variant-a',
            'ModelName': 'model-a',
            'InitialInstanceCount': 1,
            'InstanceType': 'ml.m5.large',
            'InitialVariantWeight': 50  # 50% traffic
        },
        {
            'VariantName': 'variant-b',
            'ModelName': 'model-b',
            'InitialInstanceCount': 1,
            'InstanceType': 'ml.m5.large',
            'InitialVariantWeight': 50  # 50% traffic
        }
    ]
)

# Create endpoint
sagemaker_client.create_endpoint(
    EndpointName="ab-test-endpoint",
    EndpointConfigName=endpoint_config_name
)
```

### 19. What are SageMaker Clarify and its use cases?

**Answer:**
SageMaker Clarify provides bias detection and model explainability.

```python
from sagemaker.clarify import SageMakerClarifyProcessor, BiasConfig, DataConfig, ModelConfig

# Bias detection
clarify_processor = SageMakerClarifyProcessor(
    role=role,
    instance_count=1,
    instance_type="ml.m5.xlarge",
    sagemaker_session=sagemaker_session
)

# Data configuration
data_config = DataConfig(
    s3_data_input_path="s3://bucket/data.csv",
    s3_output_path="s3://bucket/clarify-output/",
    label="target",
    headers=["feature1", "feature2", "target"],
    dataset_type="text/csv"
)

# Bias configuration
bias_config = BiasConfig(
    label_values_or_threshold=[1],
    facet_name="gender",
    facet_values_or_threshold=["female"]
)

# Model configuration
model_config = ModelConfig(
    model_name="my-model",
    instance_type="ml.m5.large",
    instance_count=1,
    content_type="text/csv",
    accept_type="application/json"
)

# Run bias analysis
clarify_processor.run_bias(
    data_config=data_config,
    bias_config=bias_config,
    model_config=model_config
)
```

### 20. How do you monitor model performance in SageMaker?

**Answer:**
```python
from sagemaker.model_monitor import DefaultModelMonitor, DataCaptureConfig

# Enable data capture
data_capture_config = DataCaptureConfig(
    enable_capture=True,
    sampling_percentage=100,
    destination_s3_uri="s3://bucket/data-capture/"
)

# Deploy with data capture
predictor = model.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large",
    data_capture_config=data_capture_config
)

# Create model monitor
monitor = DefaultModelMonitor(
    role=role,
    instance_count=1,
    instance_type="ml.m5.xlarge",
    volume_size_in_gb=20,
    max_runtime_in_seconds=3600
)

# Create baseline
baseline_job = monitor.suggest_baseline(
    baseline_dataset="s3://bucket/baseline-data.csv",
    dataset_format={"csv": {"header": True}},
    output_s3_uri="s3://bucket/baseline-output/"
)

# Create monitoring schedule
monitor.create_monitoring_schedule(
    endpoint_input=predictor.endpoint_name,
    output_s3_uri="s3://bucket/monitoring-output/",
    statistics=baseline_job.baseline_statistics(),
    constraints=baseline_job.suggested_constraints(),
    schedule_cron_expression="cron(0 * * * ? *)",  # Hourly
    enable_cloudwatch_metrics=True
)
```

### 21. What is SageMaker Ground Truth and how is it used?

**Answer:**
Ground Truth is a data labeling service for creating training datasets.

```python
import boto3

# Create labeling job
sagemaker_client = boto3.client('sagemaker')

labeling_job = sagemaker_client.create_labeling_job(
    LabelingJobName="image-classification-job",
    LabelAttributeName="category",
    InputConfig={
        'DataSource': {
            'S3DataSource': {
                'ManifestS3Uri': 's3://bucket/manifest.json'
            }
        },
        'DataAttributes': {
            'ContentClassifiers': ['FreeOfPersonallyIdentifiableInformation']
        }
    },
    OutputConfig={
        'S3OutputPath': 's3://bucket/labeled-data/'
    },
    RoleArn=role,
    LabelCategoryConfigS3Uri='s3://bucket/label-categories.json',
    HumanTaskConfig={
        'WorkteamArn': 'arn:aws:sagemaker:region:account:workteam/private-crowd/team-name',
        'UiConfig': {
            'UiTemplateS3Uri': 's3://bucket/ui-template.html'
        },
        'PreHumanTaskLambdaArn': 'arn:aws:lambda:region:account:function:pre-labeling',
        'TaskTitle': 'Image Classification',
        'TaskDescription': 'Classify images into categories',
        'NumberOfHumanWorkersPerDataObject': 3,
        'TaskTimeLimitInSeconds': 3600,
        'AnnotationConsolidationConfig': {
            'AnnotationConsolidationLambdaArn': 'arn:aws:lambda:region:account:function:consolidation'
        }
    }
)
```

### 22. How do you implement custom metrics in SageMaker training?

**Answer:**
```python
# Training script with custom metrics
def train_model():
    import json
    import logging
    
    # Setup logging for metrics
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Training loop
    for epoch in range(num_epochs):
        train_loss = train_epoch(model, train_loader)
        val_loss, val_accuracy = validate_epoch(model, val_loader)
        
        # Log custom metrics (SageMaker will capture these)
        logger.info(f"Epoch: {epoch}")
        logger.info(f"train_loss: {train_loss:.4f}")
        logger.info(f"validation_loss: {val_loss:.4f}")
        logger.info(f"validation_accuracy: {val_accuracy:.4f}")
        
        # Custom business metrics
        precision = calculate_precision(model, val_loader)
        recall = calculate_recall(model, val_loader)
        f1_score = 2 * (precision * recall) / (precision + recall)
        
        logger.info(f"validation_precision: {precision:.4f}")
        logger.info(f"validation_recall: {recall:.4f}")
        logger.info(f"validation_f1: {f1_score:.4f}")

# Define metric definitions for hyperparameter tuning
metric_definitions = [
    {'Name': 'validation:accuracy', 'Regex': 'validation_accuracy: ([0-9\\.]+)'},
    {'Name': 'validation:loss', 'Regex': 'validation_loss: ([0-9\\.]+)'},
    {'Name': 'validation:precision', 'Regex': 'validation_precision: ([0-9\\.]+)'},
    {'Name': 'validation:recall', 'Regex': 'validation_recall: ([0-9\\.]+)'},
    {'Name': 'validation:f1', 'Regex': 'validation_f1: ([0-9\\.]+)'}
]

# Use in estimator
estimator = TensorFlow(
    entry_point="train.py",
    role=role,
    instance_type="ml.p3.2xlarge",
    framework_version="2.8",
    py_version="py39",
    metric_definitions=metric_definitions
)
```

### 23. What are SageMaker Spot instances and when should you use them?

**Answer:**
Spot instances offer up to 90% cost savings but can be interrupted.

```python
# Use Spot instances for training
estimator = TensorFlow(
    entry_point="train.py",
    role=role,
    instance_count=2,
    instance_type="ml.p3.2xlarge",
    framework_version="2.8",
    py_version="py39",
    use_spot_instances=True,
    max_wait=7200,  # Maximum wait time (2 hours)
    max_run=3600,   # Maximum training time (1 hour)
    checkpoint_s3_uri="s3://bucket/checkpoints/",  # For resuming interrupted jobs
    checkpoint_local_path="/opt/ml/checkpoints"
)

# Training script with checkpointing
def train_with_checkpoints():
    import os
    import torch
    
    checkpoint_dir = "/opt/ml/checkpoints"
    
    # Load checkpoint if exists
    start_epoch = 0
    if os.path.exists(f"{checkpoint_dir}/checkpoint.pth"):
        checkpoint = torch.load(f"{checkpoint_dir}/checkpoint.pth")
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        start_epoch = checkpoint['epoch'] + 1
        print(f"Resuming from epoch {start_epoch}")
    
    # Training loop with periodic checkpointing
    for epoch in range(start_epoch, num_epochs):
        train_loss = train_epoch(model, train_loader, optimizer)
        
        # Save checkpoint every 10 epochs
        if epoch % 10 == 0:
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': train_loss
            }, f"{checkpoint_dir}/checkpoint.pth")
```

### 24. How do you handle large datasets in SageMaker?

**Answer:**
**Strategies for Large Datasets:**

```python
# 1. Use Pipe Mode for streaming
pipe_input = TrainingInput(
    s3_data="s3://bucket/large-dataset/",
    input_mode="Pipe",
    content_type="application/x-recordio-protobuf"
)

# 2. Data sharding across multiple instances
distributed_estimator = TensorFlow(
    entry_point="distributed_train.py",
    role=role,
    instance_count=4,  # Multiple instances
    instance_type="ml.p3.2xlarge",
    distribution={"parameter_server": {"enabled": True}}
)

# 3. Use SageMaker Processing for data preprocessing
from sagemaker.spark.processing import PySparkProcessor

spark_processor = PySparkProcessor(
    base_job_name="spark-preprocessing",
    framework_version="3.1",
    role=role,
    instance_count=5,
    instance_type="ml.m5.xlarge",
    max_runtime_in_seconds=7200
)

spark_processor.run(
    submit_app="preprocess_large_data.py",
    inputs=[
        ProcessingInput(
            source="s3://bucket/raw-data/",
            destination="/opt/ml/processing/input"
        )
    ],
    outputs=[
        ProcessingOutput(
            source="/opt/ml/processing/output",
            destination="s3://bucket/processed-data/"
        )
    ]
)

# 4. Incremental training for continuously growing datasets
incremental_estimator = XGBoost(
    entry_point="incremental_train.py",
    framework_version="1.5-1",
    role=role,
    instance_type="ml.m5.xlarge"
)

# Train on new data while using previous model
incremental_estimator.fit(
    inputs={
        "train": "s3://bucket/new-training-data/",
        "model": "s3://bucket/previous-model/model.tar.gz"
    }
)
```

### 25. What is SageMaker Neo and when would you use it?

**Answer:**
SageMaker Neo optimizes ML models for specific hardware platforms.

```python
# Compile model with Neo
from sagemaker.neo import compile_model

# Compile for edge deployment
compiled_model = compile_model(
    role=role,
    model_data="s3://bucket/model.tar.gz",
    framework="tensorflow",
    framework_version="2.8",
    target_instance_family="ml_m5",  # Target hardware
    input_shape={"data": [1, 224, 224, 3]},
    output_path="s3://bucket/compiled-models/",
    compile_max_run=900
)

# Deploy compiled model
compiled_predictor = compiled_model.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large"
)

# For edge devices
edge_compiled_model = compile_model(
    role=role,
    model_data="s3://bucket/model.tar.gz",
    framework="tensorflow",
    framework_version="2.8",
    target_device="jetson_nano",  # Edge device
    input_shape={"data": [1, 224, 224, 3]},
    output_path="s3://bucket/edge-models/"
)
```

### 26. How do you implement model versioning and rollback in SageMaker?

**Answer:**
```python
# Model versioning with Model Registry
from sagemaker.model import Model
from sagemaker.model_package import ModelPackage

# Register new model version
model_package = model.register(
    content_types=["application/json"],
    response_types=["application/json"],
    inference_instances=["ml.m5.large"],
    model_package_group_name="production-models",
    approval_status="PendingManualApproval",
    model_metrics={
        "accuracy": {"value": 0.95},
        "version": {"value": "2.1"}
    },
    customer_metadata_properties={
        "training_date": "2024-01-15",
        "data_version": "v2.1",
        "algorithm": "xgboost"
    }
)

# List model versions
sagemaker_client = boto3.client('sagemaker')

model_packages = sagemaker_client.list_model_packages(
    ModelPackageGroupName="production-models",
    SortBy="CreationTime",
    SortOrder="Descending"
)

# Deploy specific version
model_package_arn = "arn:aws:sagemaker:region:account:model-package/production-models/1"

model_from_registry = ModelPackage(
    role=role,
    model_package_arn=model_package_arn,
    sagemaker_session=sagemaker_session
)

predictor = model_from_registry.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large",
    endpoint_name="production-endpoint-v2"
)

# Blue-Green deployment for rollback
def blue_green_deployment(new_model_arn, endpoint_name):
    # Create new endpoint configuration
    new_config_name = f"config-{int(time.time())}"
    
    sagemaker_client.create_endpoint_config(
        EndpointConfigName=new_config_name,
        ProductionVariants=[
            {
                'VariantName': 'green',
                'ModelName': new_model_arn,
                'InitialInstanceCount': 1,
                'InstanceType': 'ml.m5.large',
                'InitialVariantWeight': 100
            }
        ]
    )
    
    # Update endpoint
    sagemaker_client.update_endpoint(
        EndpointName=endpoint_name,
        EndpointConfigName=new_config_name
    )
    
    return new_config_name

# Rollback function
def rollback_model(endpoint_name, previous_config_name):
    sagemaker_client.update_endpoint(
        EndpointName=endpoint_name,
        EndpointConfigName=previous_config_name
    )
```

### 27. What are SageMaker Inference Recommender capabilities?

**Answer:**
Inference Recommender provides automated instance type and configuration recommendations.

```python
from sagemaker.inference_recommender import InferenceRecommender

# Create inference recommender job
recommender = InferenceRecommender(
    role=role,
    sagemaker_session=sagemaker_session
)

# Default recommendation job
default_job = recommender.run_inference_recommendations_job(
    job_name="recommendation-job",
    model_package_version_arn=model_package_arn,
    sample_payload_url="s3://bucket/sample-payload.json",
    supported_content_types=["application/json"],
    supported_response_mime_types=["application/json"]
)

# Advanced recommendation with custom requirements
advanced_job = recommender.run_inference_recommendations_job(
    job_name="advanced-recommendation-job",
    model_package_version_arn=model_package_arn,
    sample_payload_url="s3://bucket/sample-payload.json",
    supported_content_types=["application/json"],
    supported_response_mime_types=["application/json"],
    job_type="Advanced",
    traffic_pattern={
        "TrafficType": "PHASES",
        "Phases": [
            {
                "InitialNumberOfUsers": 1,
                "SpawnRate": 1,
                "DurationInSeconds": 300
            },
            {
                "InitialNumberOfUsers": 10,
                "SpawnRate": 2,
                "DurationInSeconds": 600
            }
        ]
    },
    resource_limit={
        "MaxNumberOfTests": 10,
        "MaxParallelOfTests": 2
    }
)

# Get recommendations
recommendations = recommender.describe_inference_recommendations_job(
    job_name="recommendation-job"
)

for rec in recommendations['InferenceRecommendations']:
    print(f"Instance Type: {rec['RecommendationId']}")
    print(f"Cost per hour: ${rec['CostPerHour']}")
    print(f"Cost per inference: ${rec['CostPerInference']}")
```

### 28. How do you implement data lineage tracking in SageMaker?

**Answer:**
```python
from sagemaker.lineage import context, artifact, association, action
from sagemaker.lineage.visualizer import LineageTableVisualizer

# Create lineage context
training_context = context.Context.create(
    context_name="training-pipeline-context",
    context_type="MLPipeline",
    description="End-to-end training pipeline",
    properties={"pipeline_version": "1.0", "environment": "production"}
)

# Create data artifact
training_data_artifact = artifact.Artifact.create(
    artifact_name="training-data-v1",
    artifact_type="Dataset",
    source_uri="s3://bucket/training-data/",
    properties={"format": "csv", "size": "10GB", "rows": "1000000"}
)

# Create model artifact
model_artifact = artifact.Artifact.create(
    artifact_name="trained-model-v1",
    artifact_type="Model",
    source_uri="s3://bucket/models/model.tar.gz",
    properties={"algorithm": "xgboost", "accuracy": "0.95"}
)

# Create training action
training_action = action.Action.create(
    action_name="model-training-action",
    action_type="Training",
    description="XGBoost model training",
    properties={"instance_type": "ml.m5.xlarge", "duration": "30min"}
)

# Create associations
association.Association.create(
    source_arn=training_data_artifact.artifact_arn,
    destination_arn=training_action.action_arn,
    association_type="ContributedTo"
)

association.Association.create(
    source_arn=training_action.action_arn,
    destination_arn=model_artifact.artifact_arn,
    association_type="Produced"
)

# Query lineage
viz = LineageTableVisualizer(sagemaker_session)
lineage_table = viz.show(pipeline_execution_arn=training_context.context_arn)
```

### 29. What is SageMaker Canvas and its use cases?

**Answer:**
SageMaker Canvas is a no-code ML service for business analysts.

```python
# Canvas is primarily a GUI tool, but you can interact programmatically
import boto3

# Create Canvas app (via API)
sagemaker_client = boto3.client('sagemaker')

# List Canvas apps
apps = sagemaker_client.list_apps(
    DomainId="domain-id",
    UserProfileName="user-profile",
    AppType="Canvas"
)

# Canvas use cases:
use_cases = {
    "business_forecasting": {
        "description": "Sales, demand, and revenue forecasting",
        "data_types": ["time_series", "tabular"],
        "algorithms": ["AutoML", "built_in_forecasting"]
    },
    "customer_analytics": {
        "description": "Churn prediction, segmentation",
        "data_types": ["tabular"],
        "algorithms": ["classification", "clustering"]
    },
    "operational_analytics": {
        "description": "Quality prediction, maintenance",
        "data_types": ["tabular", "time_series"],
        "algorithms": ["regression", "anomaly_detection"]
    }
}

# Canvas model deployment (programmatic)
def deploy_canvas_model(model_name, endpoint_name):
    # Canvas models can be deployed to SageMaker endpoints
    response = sagemaker_client.create_endpoint(
        EndpointName=endpoint_name,
        EndpointConfigName=f"{model_name}-config"
    )
    return response
```

### 30. How do you handle multi-class classification in SageMaker?

**Answer:**
```python
# Multi-class classification with built-in algorithms
from sagemaker.xgboost import XGBoost

# XGBoost for multi-class
xgb_multiclass = XGBoost(
    entry_point="multiclass_train.py",
    framework_version="1.5-1",
    role=role,
    instance_type="ml.m5.xlarge",
    hyperparameters={
        "objective": "multi:softprob",  # Multi-class objective
        "num_class": 5,  # Number of classes
        "max_depth": 6,
        "eta": 0.2,
        "subsample": 0.8
    }
)

# Custom multi-class training script
def multiclass_training_script():
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import LabelEncoder
    from sklearn.metrics import classification_report, confusion_matrix
    import xgboost as xgb
    
    # Load data
    train_data = pd.read_csv("/opt/ml/input/data/train/train.csv")
    
    # Prepare features and labels
    X_train = train_data.drop('target', axis=1)
    y_train = train_data['target']
    
    # Encode labels if they're strings
    if y_train.dtype == 'object':
        label_encoder = LabelEncoder()
        y_train = label_encoder.fit_transform(y_train)
        
        # Save label encoder
        import joblib
        joblib.dump(label_encoder, '/opt/ml/model/label_encoder.pkl')
    
    # Train XGBoost model
    dtrain = xgb.DMatrix(X_train, label=y_train)
    
    params = {
        'objective': 'multi:softprob',
        'num_class': len(np.unique(y_train)),
        'max_depth': 6,
        'eta': 0.2,
        'subsample': 0.8,
        'eval_metric': 'mlogloss'
    }
    
    model = xgb.train(
        params=params,
        dtrain=dtrain,
        num_boost_round=100
    )
    
    # Save model
    model.save_model('/opt/ml/model/xgboost-model')
    
    # Validation metrics
    val_data = pd.read_csv("/opt/ml/input/data/validation/validation.csv")
    X_val = val_data.drop('target', axis=1)
    y_val = val_data['target']
    
    if y_val.dtype == 'object':
        y_val = label_encoder.transform(y_val)
    
    dval = xgb.DMatrix(X_val)
    predictions = model.predict(dval)
    predicted_classes = np.argmax(predictions, axis=1)
    
    # Log metrics
    from sklearn.metrics import accuracy_score, f1_score
    
    accuracy = accuracy_score(y_val, predicted_classes)
    f1 = f1_score(y_val, predicted_classes, average='weighted')
    
    print(f"validation_accuracy: {accuracy:.4f}")
    print(f"validation_f1: {f1:.4f}")
    
    # Confusion matrix
    cm = confusion_matrix(y_val, predicted_classes)
    print(f"Confusion Matrix:\n{cm}")

# Linear Learner for multi-class
from sagemaker.linear_learner import LinearLearner

linear_multiclass = LinearLearner(
    role=role,
    instance_count=1,
    instance_type="ml.m5.xlarge",
    predictor_type="multiclass_classifier",
    num_classes=5
)

# Train models
xgb_multiclass.fit({"train": train_data, "validation": val_data})
linear_multiclass.fit({"train": train_data, "validation": val_data})
```

---

## Intermediate (31-60)

### 31. How do you implement distributed training with SageMaker's built-in distributed training libraries?

**Answer:**
```python
# SageMaker Distributed Data Parallel
from sagemaker.tensorflow import TensorFlow

distributed_estimator = TensorFlow(
    entry_point="distributed_train.py",
    role=role,
    instance_count=4,
    instance_type="ml.p3.2xlarge",
    framework_version="2.8",
    py_version="py39",
    distribution={
        "smdistributed": {
            "dataparallel": {
                "enabled": True
            }
        }
    }
)

# Training script with SageMaker distributed
def distributed_training_script():
    import tensorflow as tf
    import smdistributed.dataparallel.tensorflow as sdp
    
    # Initialize distributed training
    sdp.init()
    
    # Configure GPUs
    gpus = tf.config.experimental.list_physical_devices('GPU')
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
    if gpus:
        tf.config.experimental.set_visible_devices(gpus[sdp.local_rank()], 'GPU')
    
    # Create model
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    
    # Distributed optimizer
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001 * sdp.size())
    optimizer = sdp.DistributedOptimizer(optimizer)
    
    # Compile model
    model.compile(
        optimizer=optimizer,
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Callbacks
    callbacks = [
        sdp.callbacks.SMDataParallelCallback(),
        tf.keras.callbacks.ModelCheckpoint(
            filepath='/opt/ml/model/checkpoint-{epoch:02d}',
            save_best_only=True
        )
    ]
    
    # Train model
    model.fit(
        train_dataset,
        epochs=100,
        callbacks=callbacks,
        verbose=1 if sdp.rank() == 0 else 0
    )
    
    # Save model (only on rank 0)
    if sdp.rank() == 0:
        model.save('/opt/ml/model/1')

# Model Parallel for large models
model_parallel_estimator = TensorFlow(
    entry_point="model_parallel_train.py",
    role=role,
    instance_count=2,
    instance_type="ml.p3.16xlarge",
    framework_version="2.8",
    py_version="py39",
    distribution={
        "smdistributed": {
            "modelparallel": {
                "enabled": True,
                "parameters": {
                    "partitions": 2,
                    "microbatches": 4,
                    "optimize": "speed"
                }
            }
        }
    }
)
```

### 32. How do you implement custom algorithms with SageMaker Script Mode?

**Answer:**
```python
# Custom PyTorch algorithm
from sagemaker.pytorch import PyTorch

# Custom training script
def create_custom_pytorch_script():
    script_content = """
import argparse
import json
import logging
import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import pandas as pd
import numpy as np

class CustomDataset(Dataset):
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.features = self.data.drop('target', axis=1).values.astype(np.float32)
        self.targets = self.data['target'].values.astype(np.float32)
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return torch.tensor(self.features[idx]), torch.tensor(self.targets[idx])

class CustomModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(CustomModel, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, output_dim)
        self.dropout = nn.Dropout(0.2)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        return x

def train(args):
    # Load data
    train_dataset = CustomDataset(os.path.join(args.data_dir, 'train.csv'))
    val_dataset = CustomDataset(os.path.join(args.data_dir, 'validation.csv'))
    
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False)
    
    # Initialize model
    input_dim = train_dataset.features.shape[1]
    model = CustomModel(input_dim, args.hidden_dim, 1)
    
    # Loss and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=args.learning_rate)
    
    # Training loop
    for epoch in range(args.epochs):
        model.train()
        train_loss = 0.0
        
        for batch_idx, (data, target) in enumerate(train_loader):
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output.squeeze(), target)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
        
        # Validation
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for data, target in val_loader:
                output = model(data)
                val_loss += criterion(output.squeeze(), target).item()
        
        print(f'Epoch {epoch}: Train Loss: {train_loss/len(train_loader):.4f}, Val Loss: {val_loss/len(val_loader):.4f}')
    
    # Save model
    torch.save(model.state_dict(), os.path.join(args.model_dir, 'model.pth'))
    
    # Save model info
    model_info = {
        'input_dim': input_dim,
        'hidden_dim': args.hidden_dim,
        'output_dim': 1
    }
    with open(os.path.join(args.model_dir, 'model_info.json'), 'w') as f:
        json.dump(model_info, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch-size', type=int, default=64)
    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--learning-rate', type=float, default=0.001)
    parser.add_argument('--hidden-dim', type=int, default=128)
    parser.add_argument('--data-dir', type=str, default=os.environ['SM_CHANNEL_TRAINING'])
    parser.add_argument('--model-dir', type=str, default=os.environ['SM_MODEL_DIR'])
    
    args = parser.parse_args()
    train(args)
"""
    
    with open('custom_train.py', 'w') as f:
        f.write(script_content)

# Create custom PyTorch estimator
custom_pytorch = PyTorch(
    entry_point='custom_train.py',
    role=role,
    instance_count=1,
    instance_type='ml.m5.xlarge',
    framework_version='1.12',
    py_version='py38',
    hyperparameters={
        'batch-size': 64,
        'epochs': 100,
        'learning-rate': 0.001,
        'hidden-dim': 256
    }
)

# Train custom model
custom_pytorch.fit({'training': 's3://bucket/train/', 'validation': 's3://bucket/val/'})
```

### 33. How do you implement multi-model endpoints in SageMaker?

**Answer:**
```python
from sagemaker.multidatamodel import MultiDataModel
from sagemaker.model import Model

# Create base model
base_model = Model(
    image_uri="382416733822.dkr.ecr.us-east-1.amazonaws.com/sklearn-inference:0.23-1-cpu-py3",
    role=role,
    sagemaker_session=sagemaker_session
)

# Create multi-model endpoint
multi_model = MultiDataModel(
    name="multi-model-endpoint",
    model_data_prefix="s3://bucket/models/",
    model=base_model,
    sagemaker_session=sagemaker_session
)

# Deploy multi-model endpoint
predictor = multi_model.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large",
    endpoint_name="multi-model-endpoint"
)

# Add models dynamically
multi_model.add_model(
    model_data_source="s3://bucket/model-a/model.tar.gz",
    model_data_path="model-a"
)

multi_model.add_model(
    model_data_source="s3://bucket/model-b/model.tar.gz",
    model_data_path="model-b"
)

# Invoke specific models
result_a = predictor.predict(
    data=sample_data,
    target_model="model-a"
)

result_b = predictor.predict(
    data=sample_data,
    target_model="model-b"
)

# List models on endpoint
models = multi_model.list_models()
print(f"Models on endpoint: {models}")

# Remove model
multi_model.delete_model("model-a")

# Custom inference script for multi-model
def create_multi_model_inference_script():
    script_content = """
import json
import joblib
import os

def model_fn(model_dir):
    """Load model from model directory"""
    model_path = os.path.join(model_dir, "model.pkl")
    model = joblib.load(model_path)
    return model

def input_fn(request_body, request_content_type):
    """Parse input data"""
    if request_content_type == "application/json":
        input_data = json.loads(request_body)
        return input_data
    else:
        raise ValueError(f"Unsupported content type: {request_content_type}")

def predict_fn(input_data, model):
    """Make prediction"""
    prediction = model.predict(input_data)
    return prediction.tolist()

def output_fn(prediction, content_type):
    """Format output"""
    if content_type == "application/json":
        return json.dumps(prediction)
    else:
        raise ValueError(f"Unsupported content type: {content_type}")
"""
    
    with open('inference.py', 'w') as f:
        f.write(script_content)
```

### 34. How do you implement SageMaker Pipelines with conditional steps?

**Answer:**
```python
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep, CreateModelStep
from sagemaker.workflow.conditions import ConditionGreaterThanOrEqualTo, ConditionEquals
from sagemaker.workflow.condition_step import ConditionStep
from sagemaker.workflow.functions import JsonGet
from sagemaker.workflow.parameters import ParameterString, ParameterFloat

# Pipeline parameters
input_data_uri = ParameterString(name="InputDataUri", default_value="s3://bucket/input/")
accuracy_threshold = ParameterFloat(name="AccuracyThreshold", default_value=0.85)
model_approval_status = ParameterString(name="ModelApprovalStatus", default_value="PendingManualApproval")

# Data processing step
processing_step = ProcessingStep(
    name="DataProcessing",
    processor=processor,
    inputs=[
        ProcessingInput(source=input_data_uri, destination="/opt/ml/processing/input")
    ],
    outputs=[
        ProcessingOutput(output_name="train_data", source="/opt/ml/processing/train"),
        ProcessingOutput(output_name="validation_data", source="/opt/ml/processing/validation"),
        ProcessingOutput(output_name="test_data", source="/opt/ml/processing/test")
    ],
    code="preprocessing.py"
)

# Training step
training_step = TrainingStep(
    name="ModelTraining",
    estimator=estimator,
    inputs={
        "train": TrainingInput(s3_data=processing_step.properties.ProcessingOutputConfig.Outputs["train_data"].S3Output.S3Uri),
        "validation": TrainingInput(s3_data=processing_step.properties.ProcessingOutputConfig.Outputs["validation_data"].S3Output.S3Uri)
    }
)

# Model evaluation step
evaluation_step = ProcessingStep(
    name="ModelEvaluation",
    processor=evaluation_processor,
    inputs=[
        ProcessingInput(
            source=training_step.properties.ModelArtifacts.S3ModelArtifacts,
            destination="/opt/ml/processing/model"
        ),
        ProcessingInput(
            source=processing_step.properties.ProcessingOutputConfig.Outputs["test_data"].S3Output.S3Uri,
            destination="/opt/ml/processing/test"
        )
    ],
    outputs=[
        ProcessingOutput(output_name="evaluation_report", source="/opt/ml/processing/evaluation")
    ],
    code="evaluate.py",
    property_files=["evaluation.json"]
)

# Model registration step
from sagemaker.workflow.model_step import ModelStep

model_step = ModelStep(
    name="RegisterModel",
    step_args=model.register(
        content_types=["application/json"],
        response_types=["application/json"],
        inference_instances=["ml.m5.large"],
        transform_instances=["ml.m5.xlarge"],
        model_package_group_name="customer-churn-models",
        approval_status=model_approval_status
    )
)

# Deployment step
from sagemaker.workflow.lambda_step import LambdaStep

deploy_step = LambdaStep(
    name="DeployModel",
    lambda_func=deploy_lambda_function,
    inputs={
        "model_package_arn": model_step.properties.ModelPackageArn,
        "endpoint_name": "production-endpoint"
    }
)

# Conditional logic
accuracy_condition = ConditionGreaterThanOrEqualTo(
    left=JsonGet(
        step_name=evaluation_step.name,
        property_file="evaluation.json",
        json_path="metrics.accuracy.value"
    ),
    right=accuracy_threshold
)

# Data drift condition
data_drift_condition = ConditionEquals(
    left=JsonGet(
        step_name=evaluation_step.name,
        property_file="evaluation.json",
        json_path="data_drift.detected"
    ),
    right="false"
)

# Combined condition
from sagemaker.workflow.conditions import ConditionOr, ConditionAnd

combined_condition = ConditionAnd(
    conditions=[accuracy_condition, data_drift_condition]
)

# Conditional step
condition_step = ConditionStep(
    name="CheckModelQuality",
    conditions=[combined_condition],
    if_steps=[model_step, deploy_step],
    else_steps=[]  # Could add retraining or notification steps
)

# Create pipeline
pipeline = Pipeline(
    name="ConditionalMLPipeline",
    parameters=[input_data_uri, accuracy_threshold, model_approval_status],
    steps=[processing_step, training_step, evaluation_step, condition_step]
)

# Create/update pipeline
pipeline.upsert(role_arn=role)

# Execute pipeline
execution = pipeline.start(
    parameters={
        "InputDataUri": "s3://bucket/new-data/",
        "AccuracyThreshold": 0.90
    }
)
```

### 35. How do you implement feature engineering at scale using SageMaker Processing?

**Answer:**
```python
# Spark-based feature engineering
from sagemaker.spark.processing import PySparkProcessor

# Create Spark processor
spark_processor = PySparkProcessor(
    base_job_name="feature-engineering",
    framework_version="3.1",
    role=role,
    instance_count=5,
    instance_type="ml.m5.xlarge",
    max_runtime_in_seconds=7200
)

# Feature engineering script
def create_feature_engineering_script():
    script_content = """
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.ml.feature import VectorAssembler, StandardScaler, StringIndexer, OneHotEncoder
from pyspark.ml import Pipeline
import sys

def main():
    spark = SparkSession.builder.appName("FeatureEngineering").getOrCreate()
    
    # Read data
    df = spark.read.option("header", "true").csv("/opt/ml/processing/input/")
    
    # Data type conversions
    numeric_columns = ["age", "income", "credit_score"]
    for col in numeric_columns:
        df = df.withColumn(col, df[col].cast("double"))
    
    # Feature engineering
    # 1. Age groups
    df = df.withColumn("age_group", 
                      when(col("age") < 25, "young")
                      .when(col("age") < 45, "middle")
                      .otherwise("senior"))
    
    # 2. Income brackets
    df = df.withColumn("income_bracket",
                      when(col("income") < 30000, "low")
                      .when(col("income") < 70000, "medium")
                      .otherwise("high"))
    
    # 3. Credit score categories
    df = df.withColumn("credit_category",
                      when(col("credit_score") < 600, "poor")
                      .when(col("credit_score") < 700, "fair")
                      .when(col("credit_score") < 800, "good")
                      .otherwise("excellent"))
    
    # 4. Interaction features
    df = df.withColumn("income_age_ratio", col("income") / col("age"))
    df = df.withColumn("credit_income_ratio", col("credit_score") / col("income") * 1000)
    
    # 5. Aggregated features (assuming transaction data)
    if "transaction_amount" in df.columns:
        window_spec = Window.partitionBy("customer_id").orderBy("transaction_date")
        
        df = df.withColumn("avg_transaction_30d", 
                          avg("transaction_amount").over(window_spec.rowsBetween(-29, 0)))
        df = df.withColumn("transaction_count_30d", 
                          count("transaction_amount").over(window_spec.rowsBetween(-29, 0)))
        df = df.withColumn("max_transaction_30d", 
                          max("transaction_amount").over(window_spec.rowsBetween(-29, 0)))
    
    # Handle categorical variables
    categorical_columns = ["age_group", "income_bracket", "credit_category", "gender", "occupation"]
    
    # String indexing and one-hot encoding
    indexers = [StringIndexer(inputCol=col, outputCol=f"{col}_index") for col in categorical_columns]
    encoders = [OneHotEncoder(inputCol=f"{col}_index", outputCol=f"{col}_encoded") for col in categorical_columns]
    
    # Feature scaling
    feature_columns = numeric_columns + [f"{col}_encoded" for col in categorical_columns]
    assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
    scaler = StandardScaler(inputCol="features", outputCol="scaled_features")
    
    # Create pipeline
    pipeline = Pipeline(stages=indexers + encoders + [assembler, scaler])
    
    # Fit and transform
    pipeline_model = pipeline.fit(df)
    transformed_df = pipeline_model.transform(df)
    
    # Split data
    train_df, test_df = transformed_df.randomSplit([0.8, 0.2], seed=42)
    
    # Save processed data
    train_df.select("scaled_features", "target").write.mode("overwrite").parquet("/opt/ml/processing/output/train/")
    test_df.select("scaled_features", "target").write.mode("overwrite").parquet("/opt/ml/processing/output/test/")
    
    # Save feature metadata
    feature_metadata = {
        "numeric_features": numeric_columns,
        "categorical_features": categorical_columns,
        "feature_count": len(feature_columns)
    }
    
    import json
    with open("/opt/ml/processing/output/feature_metadata.json", "w") as f:
        json.dump(feature_metadata, f)
    
    spark.stop()

if __name__ == "__main__":
    main()
"""
    
    with open('feature_engineering.py', 'w') as f:
        f.write(script_content)

# Run feature engineering job
spark_processor.run(
    submit_app="feature_engineering.py",
    inputs=[
        ProcessingInput(
            source="s3://bucket/raw-data/",
            destination="/opt/ml/processing/input"
        )
    ],
    outputs=[
        ProcessingOutput(
            source="/opt/ml/processing/output/train",
            destination="s3://bucket/processed-data/train/"
        ),
        ProcessingOutput(
            source="/opt/ml/processing/output/test",
            destination="s3://bucket/processed-data/test/"
        ),
        ProcessingOutput(
            source="/opt/ml/processing/output/feature_metadata.json",
            destination="s3://bucket/metadata/"
        )
    ],
    arguments=["--input-path", "/opt/ml/processing/input",
               "--output-path", "/opt/ml/processing/output"]
)
```
