# Amazon SageMaker - Comprehensive Interview Questions

## Table of Contents
1. [Core Concepts](#core-concepts)
2. [Data Engineering Integration](#data-engineering-integration)
3. [Model Training & Development](#model-training--development)
4. [Model Deployment & Serving](#model-deployment--serving)
5. [SageMaker Pipelines & MLOps](#sagemaker-pipelines--mlops)
6. [Feature Store & Data Management](#feature-store--data-management)
7. [Monitoring & Optimization](#monitoring--optimization)
8. [Real-World Scenarios](#real-world-scenarios)

---

## Core Concepts

### 1. What is Amazon SageMaker and how does it integrate with AWS data services?

**Answer:**
Amazon SageMaker is a fully managed ML platform that provides tools for the complete ML lifecycle, with deep integration into AWS data ecosystem.

**Key Integration Points:**
- **S3**: Data storage and model artifacts
- **Glue**: Data cataloging and ETL
- **Athena**: Data querying and analysis
- **Redshift**: Data warehousing
- **Kinesis**: Real-time data streaming
- **Lambda**: Serverless inference

**Architecture Integration:**
```python
import boto3
import sagemaker
from sagemaker import get_execution_role

# Initialize SageMaker session
sagemaker_session = sagemaker.Session()
role = get_execution_role()

# Data pipeline integration
def integrated_ml_pipeline():
    # 1. Data extraction from Redshift
    redshift_data = extract_from_redshift(
        cluster="ml-cluster",
        database="analytics",
        query="SELECT * FROM customer_features WHERE date >= '2024-01-01'"
    )
    
    # 2. Data processing with Glue
    glue_job = trigger_glue_etl_job(
        job_name="feature-engineering",
        input_data=redshift_data,
        output_location="s3://ml-bucket/processed-features/"
    )
    
    # 3. Training data preparation
    training_data_uri = "s3://ml-bucket/processed-features/train/"
    
    # 4. SageMaker training
    estimator = sagemaker.estimator.Estimator(
        image_uri="382416733822.dkr.ecr.us-east-1.amazonaws.com/xgboost:latest",
        role=role,
        instance_count=1,
        instance_type="ml.m5.xlarge",
        output_path="s3://ml-bucket/models/"
    )
    
    estimator.fit({"train": training_data_uri})
    
    # 5. Model deployment
    predictor = estimator.deploy(
        initial_instance_count=1,
        instance_type="ml.m5.large"
    )
    
    return predictor
```

### 2. Explain SageMaker's architecture and core components.

**Answer:**
**SageMaker Architecture:**

```
Data Sources → SageMaker Studio → Training Jobs → Model Registry → Endpoints → Monitoring
     ↓              ↓                ↓              ↓              ↓          ↓
S3/Redshift → Notebooks → Algorithms → Models → Real-time → CloudWatch
Glue/Athena → Processing → Custom Code → Batch Transform → Batch → Model Monitor
```

**Core Components:**
```python
# 1. SageMaker Studio - Integrated development environment
import sagemaker.studio

# 2. Processing Jobs - Data preprocessing
from sagemaker.processing import ProcessingInput, ProcessingOutput, ScriptProcessor

processor = ScriptProcessor(
    command=["python3"],
    image_uri="python:3.8",
    role=role,
    instance_count=1,
    instance_type="ml.m5.xlarge"
)

processor.run(
    code="preprocessing.py",
    inputs=[ProcessingInput(source="s3://bucket/raw-data/", destination="/opt/ml/processing/input")],
    outputs=[ProcessingOutput(source="/opt/ml/processing/output", destination="s3://bucket/processed-data/")]
)

# 3. Training Jobs - Model training
from sagemaker.tensorflow import TensorFlow

tf_estimator = TensorFlow(
    entry_point="train.py",
    role=role,
    instance_count=2,
    instance_type="ml.p3.2xlarge",
    framework_version="2.8",
    py_version="py39",
    distribution={"parameter_server": {"enabled": True}}
)

# 4. Model Registry - Model versioning
from sagemaker.model import Model

model = Model(
    image_uri=tf_estimator.image_uri,
    model_data=tf_estimator.model_data,
    role=role
)

model_package = model.register(
    content_types=["application/json"],
    response_types=["application/json"],
    inference_instances=["ml.m5.large"],
    transform_instances=["ml.m5.xlarge"],
    model_package_group_name="customer-churn-models"
)

# 5. Endpoints - Model serving
predictor = model.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large",
    endpoint_name="churn-prediction-endpoint"
)
```

### 3. How do you handle different data formats and sources in SageMaker?

**Answer:**
**Data Input Modes and Formats:**

```python
# File Mode - Downloads data to local storage
from sagemaker.inputs import TrainingInput

# CSV data
csv_input = TrainingInput(
    s3_data="s3://bucket/data.csv",
    content_type="text/csv",
    input_mode="File"
)

# Parquet data
parquet_input = TrainingInput(
    s3_data="s3://bucket/data.parquet",
    content_type="application/x-parquet",
    input_mode="File"
)

# Pipe Mode - Streams data directly
pipe_input = TrainingInput(
    s3_data="s3://bucket/large-dataset/",
    content_type="application/x-recordio-protobuf",
    input_mode="Pipe"
)

# Fast File Mode - Optimized for large datasets
fast_file_input = TrainingInput(
    s3_data="s3://bucket/big-data/",
    input_mode="FastFile"
)

# Multiple data sources
estimator.fit({
    "train": csv_input,
    "validation": parquet_input,
    "test": pipe_input
})
```

**Custom Data Processing:**
```python
# Custom preprocessing script
def preprocess_data():
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import StandardScaler
    
    # Read from multiple sources
    customer_data = pd.read_csv("/opt/ml/processing/input/customers.csv")
    transaction_data = pd.read_parquet("/opt/ml/processing/input/transactions.parquet")
    
    # Feature engineering
    features = engineer_features(customer_data, transaction_data)
    
    # Data splitting
    train, validation, test = split_data(features)
    
    # Save processed data
    train.to_csv("/opt/ml/processing/output/train/train.csv", index=False)
    validation.to_csv("/opt/ml/processing/output/validation/validation.csv", index=False)
    test.to_csv("/opt/ml/processing/output/test/test.csv", index=False)

# Processing job with custom script
from sagemaker.processing import ScriptProcessor

processor = ScriptProcessor(
    command=["python3"],
    image_uri="python:3.8-slim",
    role=role,
    instance_count=1,
    instance_type="ml.m5.2xlarge"
)

processor.run(
    code="preprocess.py",
    inputs=[
        ProcessingInput(source="s3://bucket/raw/customers.csv", destination="/opt/ml/processing/input/"),
        ProcessingInput(source="s3://bucket/raw/transactions.parquet", destination="/opt/ml/processing/input/")
    ],
    outputs=[
        ProcessingOutput(source="/opt/ml/processing/output/train", destination="s3://bucket/processed/train/"),
        ProcessingOutput(source="/opt/ml/processing/output/validation", destination="s3://bucket/processed/validation/"),
        ProcessingOutput(source="/opt/ml/processing/output/test", destination="s3://bucket/processed/test/")
    ]
)
```

---

## Model Training & Development

### 4. How do you implement distributed training in SageMaker?

**Answer:**
**Distributed Training Strategies:**

```python
# Data Parallel Training
from sagemaker.tensorflow import TensorFlow

# Multi-GPU, single instance
tf_estimator = TensorFlow(
    entry_point="train.py",
    role=role,
    instance_count=1,
    instance_type="ml.p3.8xlarge",  # 4 GPUs
    framework_version="2.8",
    py_version="py39",
    hyperparameters={
        "epochs": 100,
        "batch-size": 64,
        "learning-rate": 0.001
    }
)

# Multi-instance distributed training
distributed_tf_estimator = TensorFlow(
    entry_point="distributed_train.py",
    role=role,
    instance_count=4,  # 4 instances
    instance_type="ml.p3.2xlarge",  # 1 GPU each
    framework_version="2.8",
    py_version="py39",
    distribution={
        "parameter_server": {
            "enabled": True
        }
    }
)

# Model Parallel Training for large models
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

**Training Script for Distributed Training:**
```python
# distributed_train.py
import tensorflow as tf
import smdistributed.dataparallel.tensorflow as sdp

# Initialize SageMaker distributed training
sdp.init()

# Configure GPU
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)
if gpus:
    tf.config.experimental.set_visible_devices(gpus[sdp.local_rank()], 'GPU')

def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    return model

def train_model():
    # Load and prepare data
    train_dataset = load_training_data()
    
    # Create model
    model = create_model()
    
    # Distributed optimizer
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001 * sdp.size())
    optimizer = sdp.DistributedOptimizer(optimizer)
    
    # Compile model
    model.compile(
        optimizer=optimizer,
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    # Callbacks for distributed training
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

if __name__ == "__main__":
    train_model()
```

### 5. How do you implement hyperparameter tuning in SageMaker?

**Answer:**
**SageMaker Automatic Model Tuning:**

```python
from sagemaker.tuner import HyperparameterTuner, IntegerParameter, ContinuousParameter, CategoricalParameter

# Define hyperparameter ranges
hyperparameter_ranges = {
    "learning_rate": ContinuousParameter(0.001, 0.1),
    "batch_size": CategoricalParameter([32, 64, 128, 256]),
    "num_layers": IntegerParameter(2, 10),
    "dropout_rate": ContinuousParameter(0.1, 0.5),
    "optimizer": CategoricalParameter(["adam", "sgd", "rmsprop"])
}

# Create base estimator
base_estimator = TensorFlow(
    entry_point="train.py",
    role=role,
    instance_count=1,
    instance_type="ml.p3.2xlarge",
    framework_version="2.8",
    py_version="py39",
    metric_definitions=[
        {"Name": "validation:accuracy", "Regex": "validation_accuracy: ([0-9\\.]+)"},
        {"Name": "validation:loss", "Regex": "validation_loss: ([0-9\\.]+)"}
    ]
)

# Create hyperparameter tuner
tuner = HyperparameterTuner(
    estimator=base_estimator,
    objective_metric_name="validation:accuracy",
    objective_type="Maximize",
    hyperparameter_ranges=hyperparameter_ranges,
    metric_definitions=[
        {"Name": "validation:accuracy", "Regex": "validation_accuracy: ([0-9\\.]+)"}
    ],
    max_jobs=50,
    max_parallel_jobs=5,
    strategy="Bayesian"
)

# Start tuning job
tuner.fit({
    "train": "s3://bucket/train/",
    "validation": "s3://bucket/validation/"
})

# Get best training job
best_training_job = tuner.best_training_job()
print(f"Best training job: {best_training_job}")

# Deploy best model
best_estimator = tuner.best_estimator()
predictor = best_estimator.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large"
)
```

**Advanced Tuning Strategies:**
```python
# Multi-objective optimization
from sagemaker.tuner import MultiObjectiveHyperparameterTuner

multi_objective_tuner = MultiObjectiveHyperparameterTuner(
    estimator=base_estimator,
    objective_metrics=[
        {"Name": "validation:accuracy", "Type": "Maximize"},
        {"Name": "training:time", "Type": "Minimize"}
    ],
    hyperparameter_ranges=hyperparameter_ranges,
    max_jobs=30,
    max_parallel_jobs=3
)

# Warm start tuning - continue from previous tuning job
warm_start_config = {
    "WarmStartType": "IdenticalDataAndAlgorithm",
    "Parents": ["previous-tuning-job-name"]
}

warm_start_tuner = HyperparameterTuner(
    estimator=base_estimator,
    objective_metric_name="validation:accuracy",
    objective_type="Maximize",
    hyperparameter_ranges=hyperparameter_ranges,
    max_jobs=20,
    max_parallel_jobs=3,
    warm_start_config=warm_start_config
)
```

---

## SageMaker Pipelines & MLOps

### 6. How do you create and manage ML pipelines using SageMaker Pipelines?

**Answer:**
**SageMaker Pipelines** provide workflow orchestration for ML:

```python
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep, CreateModelStep
from sagemaker.workflow.parameters import ParameterString, ParameterInteger
from sagemaker.workflow.conditions import ConditionGreaterThanOrEqualTo
from sagemaker.workflow.condition_step import ConditionStep

# Define pipeline parameters
input_data_uri = ParameterString(name="InputDataUri", default_value="s3://bucket/input/")
model_approval_status = ParameterString(name="ModelApprovalStatus", default_value="PendingManualApproval")
accuracy_threshold = ParameterFloat(name="AccuracyThreshold", default_value=0.85)

# Step 1: Data processing
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

# Step 2: Model training
training_step = TrainingStep(
    name="ModelTraining",
    estimator=estimator,
    inputs={
        "train": TrainingInput(s3_data=processing_step.properties.ProcessingOutputConfig.Outputs["train_data"].S3Output.S3Uri),
        "validation": TrainingInput(s3_data=processing_step.properties.ProcessingOutputConfig.Outputs["validation_data"].S3Output.S3Uri)
    }
)

# Step 3: Model evaluation
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
    code="evaluate.py"
)

# Step 4: Model registration
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

# Step 5: Conditional deployment
from sagemaker.workflow.lambda_step import LambdaStep

# Lambda function for deployment
deploy_lambda_step = LambdaStep(
    name="DeployModel",
    lambda_func=deploy_lambda_function,
    inputs={
        "model_package_arn": model_step.properties.ModelPackageArn,
        "endpoint_name": "churn-prediction-endpoint"
    }
)

# Condition for deployment based on model performance
accuracy_condition = ConditionGreaterThanOrEqualTo(
    left=JsonGet(
        step_name=evaluation_step.name,
        property_file="evaluation.json",
        json_path="metrics.accuracy.value"
    ),
    right=accuracy_threshold
)

condition_step = ConditionStep(
    name="CheckAccuracy",
    conditions=[accuracy_condition],
    if_steps=[model_step, deploy_lambda_step],
    else_steps=[]
)

# Create pipeline
pipeline = Pipeline(
    name="CustomerChurnPipeline",
    parameters=[input_data_uri, model_approval_status, accuracy_threshold],
    steps=[processing_step, training_step, evaluation_step, condition_step]
)

# Create/update pipeline
pipeline.upsert(role_arn=role)

# Execute pipeline
execution = pipeline.start()
```

### 7. How do you implement continuous integration and deployment for ML models?

**Answer:**
**CI/CD Pipeline for ML Models:**

```python
# CodePipeline integration with SageMaker
import boto3

def create_ml_cicd_pipeline():
    codepipeline = boto3.client('codepipeline')
    
    pipeline_definition = {
        "pipeline": {
            "name": "ml-model-cicd",
            "roleArn": "arn:aws:iam::account:role/CodePipelineRole",
            "artifactStore": {
                "type": "S3",
                "location": "ml-cicd-artifacts-bucket"
            },
            "stages": [
                {
                    "name": "Source",
                    "actions": [
                        {
                            "name": "SourceAction",
                            "actionTypeId": {
                                "category": "Source",
                                "owner": "AWS",
                                "provider": "CodeCommit",
                                "version": "1"
                            },
                            "configuration": {
                                "RepositoryName": "ml-model-repo",
                                "BranchName": "main"
                            },
                            "outputArtifacts": [{"name": "SourceOutput"}]
                        }
                    ]
                },
                {
                    "name": "Build",
                    "actions": [
                        {
                            "name": "BuildAction",
                            "actionTypeId": {
                                "category": "Build",
                                "owner": "AWS",
                                "provider": "CodeBuild",
                                "version": "1"
                            },
                            "configuration": {
                                "ProjectName": "ml-model-build"
                            },
                            "inputArtifacts": [{"name": "SourceOutput"}],
                            "outputArtifacts": [{"name": "BuildOutput"}]
                        }
                    ]
                },
                {
                    "name": "Deploy",
                    "actions": [
                        {
                            "name": "DeployAction",
                            "actionTypeId": {
                                "category": "Invoke",
                                "owner": "AWS",
                                "provider": "Lambda",
                                "version": "1"
                            },
                            "configuration": {
                                "FunctionName": "deploy-ml-model"
                            },
                            "inputArtifacts": [{"name": "BuildOutput"}]
                        }
                    ]
                }
            ]
        }
    }
    
    codepipeline.create_pipeline(**pipeline_definition)

# CodeBuild project for model training and testing
buildspec_yml = """
version: 0.2
phases:
  install:
    runtime-versions:
      python: 3.8
    commands:
      - pip install sagemaker boto3 pytest
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
  build:
    commands:
      - echo Build started on `date`
      - echo Running unit tests...
      - python -m pytest tests/
      - echo Training model...
      - python train_pipeline.py
      - echo Model training completed
  post_build:
    commands:
      - echo Build completed on `date`
artifacts:
  files:
    - '**/*'
"""

# Lambda function for model deployment
def deploy_ml_model(event, context):
    import json
    import boto3
    
    sagemaker = boto3.client('sagemaker')
    
    # Get model package ARN from pipeline execution
    model_package_arn = event['model_package_arn']
    
    # Create model
    model_name = f"deployed-model-{int(time.time())}"
    
    create_model_response = sagemaker.create_model(
        ModelName=model_name,
        Containers=[
            {
                'ModelPackageName': model_package_arn
            }
        ],
        ExecutionRoleArn=execution_role
    )
    
    # Create endpoint configuration
    endpoint_config_name = f"endpoint-config-{int(time.time())}"
    
    sagemaker.create_endpoint_config(
        EndpointConfigName=endpoint_config_name,
        ProductionVariants=[
            {
                'VariantName': 'primary',
                'ModelName': model_name,
                'InitialInstanceCount': 1,
                'InstanceType': 'ml.m5.large',
                'InitialVariantWeight': 1
            }
        ]
    )
    
    # Update or create endpoint
    endpoint_name = "production-endpoint"
    
    try:
        # Update existing endpoint
        sagemaker.update_endpoint(
            EndpointName=endpoint_name,
            EndpointConfigName=endpoint_config_name
        )
    except sagemaker.exceptions.ClientError:
        # Create new endpoint
        sagemaker.create_endpoint(
            EndpointName=endpoint_name,
            EndpointConfigName=endpoint_config_name
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Model deployed to endpoint: {endpoint_name}')
    }
```

---

## Real-World Scenarios

### 8. Design an end-to-end recommendation system using SageMaker integrated with AWS data services.

**Answer:**
**Recommendation System Architecture:**
```
User Events → Kinesis → Lambda → DynamoDB → SageMaker → API Gateway → Applications
     ↓          ↓        ↓        ↓           ↓           ↓            ↓
Real-time → Stream → Processing → Feature → Training → Serving → Recommendations
Data      → Data   → Functions → Store   → Pipeline → Layer  → Engine
```

**Implementation:**
```python
# Real-time feature engineering with Kinesis and Lambda
import json
import boto3
from decimal import Decimal

def lambda_feature_processor(event, context):
    dynamodb = boto3.resource('dynamodb')
    feature_table = dynamodb.Table('user-features')
    
    for record in event['Records']:
        # Parse Kinesis record
        payload = json.loads(base64.b64decode(record['kinesis']['data']))
        
        user_id = payload['user_id']
        item_id = payload['item_id']
        event_type = payload['event_type']
        timestamp = payload['timestamp']
        
        # Update user features
        response = feature_table.update_item(
            Key={'user_id': user_id},
            UpdateExpression='ADD view_count :inc, last_viewed_categories :cat SET last_activity = :ts',
            ExpressionAttributeValues={
                ':inc': 1,
                ':cat': {item_id},
                ':ts': timestamp
            },
            ReturnValues='UPDATED_NEW'
        )

# SageMaker training pipeline for recommendations
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep

def create_recommendation_pipeline():
    # Data preparation step
    data_prep_step = ProcessingStep(
        name="PrepareRecommendationData",
        processor=feature_processor,
        inputs=[
            ProcessingInput(source="s3://bucket/user-interactions/", destination="/opt/ml/processing/interactions"),
            ProcessingInput(source="s3://bucket/item-metadata/", destination="/opt/ml/processing/items")
        ],
        outputs=[
            ProcessingOutput(output_name="training_data", source="/opt/ml/processing/output/train"),
            ProcessingOutput(output_name="item_features", source="/opt/ml/processing/output/items")
        ],
        code="prepare_recommendation_data.py"
    )
    
    # Collaborative filtering training
    cf_training_step = TrainingStep(
        name="CollaborativeFilteringTraining",
        estimator=factorization_machines_estimator,
        inputs={
            "train": TrainingInput(s3_data=data_prep_step.properties.ProcessingOutputConfig.Outputs["training_data"].S3Output.S3Uri)
        }
    )
    
    # Content-based training
    cb_training_step = TrainingStep(
        name="ContentBasedTraining",
        estimator=neural_cf_estimator,
        inputs={
            "train": TrainingInput(s3_data=data_prep_step.properties.ProcessingOutputConfig.Outputs["training_data"].S3Output.S3Uri),
            "items": TrainingInput(s3_data=data_prep_step.properties.ProcessingOutputConfig.Outputs["item_features"].S3Output.S3Uri)
        }
    )
    
    # Model ensemble step
    ensemble_step = ProcessingStep(
        name="CreateEnsembleModel",
        processor=ensemble_processor,
        inputs=[
            ProcessingInput(source=cf_training_step.properties.ModelArtifacts.S3ModelArtifacts, destination="/opt/ml/processing/cf_model"),
            ProcessingInput(source=cb_training_step.properties.ModelArtifacts.S3ModelArtifacts, destination="/opt/ml/processing/cb_model")
        ],
        outputs=[
            ProcessingOutput(output_name="ensemble_model", source="/opt/ml/processing/output")
        ],
        code="create_ensemble.py"
    )
    
    # Create pipeline
    pipeline = Pipeline(
        name="RecommendationPipeline",
        steps=[data_prep_step, cf_training_step, cb_training_step, ensemble_step]
    )
    
    return pipeline

# Real-time inference with SageMaker multi-model endpoints
class RecommendationInference:
    def __init__(self, endpoint_name):
        self.runtime = boto3.client('sagemaker-runtime')
        self.endpoint_name = endpoint_name
        self.dynamodb = boto3.resource('dynamodb')
        self.feature_table = self.dynamodb.Table('user-features')
    
    def get_recommendations(self, user_id, num_recommendations=10):
        # Get user features from DynamoDB
        user_features = self.feature_table.get_item(Key={'user_id': user_id})['Item']
        
        # Prepare inference payload
        payload = {
            'user_id': user_id,
            'user_features': user_features,
            'num_recommendations': num_recommendations
        }
        
        # Call SageMaker endpoint
        response = self.runtime.invoke_endpoint(
            EndpointName=self.endpoint_name,
            ContentType='application/json',
            Body=json.dumps(payload)
        )
        
        # Parse recommendations
        recommendations = json.loads(response['Body'].read().decode())
        
        # Log recommendation for feedback loop
        self.log_recommendation(user_id, recommendations)
        
        return recommendations
    
    def log_recommendation(self, user_id, recommendations):
        # Log to Kinesis for model feedback
        kinesis = boto3.client('kinesis')
        
        log_data = {
            'user_id': user_id,
            'recommendations': recommendations,
            'timestamp': int(time.time()),
            'event_type': 'recommendation_served'
        }
        
        kinesis.put_record(
            StreamName='recommendation-feedback',
            Data=json.dumps(log_data),
            PartitionKey=user_id
        )

# API Gateway integration
def recommendation_api_handler(event, context):
    recommender = RecommendationInference('recommendation-endpoint')
    
    # Extract user ID from request
    user_id = event['pathParameters']['user_id']
    num_recommendations = int(event.get('queryStringParameters', {}).get('count', 10))
    
    try:
        # Get recommendations
        recommendations = recommender.get_recommendations(user_id, num_recommendations)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'user_id': user_id,
                'recommendations': recommendations
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# Model monitoring and retraining
def setup_recommendation_monitoring():
    # CloudWatch custom metrics
    cloudwatch = boto3.client('cloudwatch')
    
    def log_recommendation_metrics(click_through_rate, conversion_rate):
        cloudwatch.put_metric_data(
            Namespace='RecommendationSystem',
            MetricData=[
                {
                    'MetricName': 'ClickThroughRate',
                    'Value': click_through_rate,
                    'Unit': 'Percent'
                },
                {
                    'MetricName': 'ConversionRate',
                    'Value': conversion_rate,
                    'Unit': 'Percent'
                }
            ]
        )
    
    # Automated retraining trigger
    def trigger_retraining_if_needed():
        # Check model performance metrics
        current_ctr = get_current_click_through_rate()
        
        if current_ctr < 0.02:  # 2% threshold
            # Trigger pipeline execution
            pipeline = Pipeline.from_pipeline_definition_s3('recommendation-pipeline')
            execution = pipeline.start()
            
            # Send notification
            sns = boto3.client('sns')
            sns.publish(
                TopicArn='arn:aws:sns:region:account:ml-alerts',
                Message=f'Recommendation model retraining triggered due to low CTR: {current_ctr}',
                Subject='Model Retraining Alert'
            )
    
    # Schedule monitoring
    schedule_lambda_function(trigger_retraining_if_needed, rate='1 day')
```

This comprehensive SageMaker interview guide covers all aspects from basic concepts to advanced MLOps implementations, showing how SageMaker integrates with AWS data services for complete ML lifecycle management.