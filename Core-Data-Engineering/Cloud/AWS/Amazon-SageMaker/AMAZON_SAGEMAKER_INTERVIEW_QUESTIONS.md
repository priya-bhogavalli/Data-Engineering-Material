# Amazon SageMaker Interview Questions

## Basic Concepts

### 1. What is Amazon SageMaker and its key components?
**Answer:** Amazon SageMaker is AWS's fully managed ML platform for building, training, and deploying ML models. Key components:

- **SageMaker Studio**: Integrated development environment
- **SageMaker Notebooks**: Managed Jupyter notebooks
- **SageMaker Training**: Scalable model training
- **SageMaker Endpoints**: Model hosting and inference
- **SageMaker Pipelines**: ML workflow orchestration
- **SageMaker Feature Store**: Centralized feature management
- **SageMaker Model Registry**: Model versioning and governance

```python
import boto3
import sagemaker
from sagemaker import get_execution_role
from sagemaker.sklearn.estimator import SKLearn

# Initialize SageMaker session
sagemaker_session = sagemaker.Session()
role = get_execution_role()
region = boto3.Session().region_name

print(f"SageMaker role: {role}")
print(f"Region: {region}")

# Create S3 bucket for data
bucket = sagemaker_session.default_bucket()
prefix = "sagemaker-demo"

print(f"Default bucket: {bucket}")
print(f"Prefix: {prefix}")

# Upload training data
train_data_path = sagemaker_session.upload_data(
    path="train.csv",
    bucket=bucket,
    key_prefix=f"{prefix}/data"
)

print(f"Training data uploaded to: {train_data_path}")
```

### 2. How do you train models using SageMaker built-in algorithms?
**Answer:** SageMaker provides optimized built-in algorithms for common ML tasks.

```python
from sagemaker import image_uris
from sagemaker.estimator import Estimator
from sagemaker.inputs import TrainingInput

# XGBoost built-in algorithm
def train_xgboost_model():
    # Get XGBoost container image
    container = image_uris.retrieve(
        framework="xgboost",
        region=region,
        version="1.5-1"
    )
    
    # Create estimator
    xgb_estimator = Estimator(
        image_uri=container,
        role=role,
        instance_count=1,
        instance_type="ml.m5.large",
        output_path=f"s3://{bucket}/{prefix}/output",
        sagemaker_session=sagemaker_session
    )
    
    # Set hyperparameters
    xgb_estimator.set_hyperparameters(
        objective="binary:logistic",
        num_round=100,
        max_depth=5,
        eta=0.2,
        subsample=0.8,
        colsample_bytree=0.8
    )
    
    # Define training input
    train_input = TrainingInput(
        s3_data=train_data_path,
        content_type="text/csv"
    )
    
    # Start training
    xgb_estimator.fit({"train": train_input})
    
    return xgb_estimator

# Linear Learner algorithm
def train_linear_learner():
    container = image_uris.retrieve(
        framework="linear-learner",
        region=region
    )
    
    linear_estimator = Estimator(
        image_uri=container,
        role=role,
        instance_count=1,
        instance_type="ml.m5.large",
        output_path=f"s3://{bucket}/{prefix}/linear-output"
    )
    
    linear_estimator.set_hyperparameters(
        feature_dim=784,
        predictor_type="binary_classifier",
        mini_batch_size=200
    )
    
    # Training with validation
    train_input = TrainingInput(train_data_path, content_type="text/csv")
    validation_input = TrainingInput(validation_data_path, content_type="text/csv")
    
    linear_estimator.fit({
        "train": train_input,
        "validation": validation_input
    })
    
    return linear_estimator

# Image Classification algorithm
def train_image_classification():
    container = image_uris.retrieve(
        framework="image-classification",
        region=region
    )
    
    ic_estimator = Estimator(
        image_uri=container,
        role=role,
        instance_count=1,
        instance_type="ml.p3.2xlarge",  # GPU instance for image training
        output_path=f"s3://{bucket}/{prefix}/ic-output"
    )
    
    ic_estimator.set_hyperparameters(
        num_classes=10,
        num_training_samples=50000,
        mini_batch_size=128,
        epochs=10,
        learning_rate=0.01,
        use_pretrained_model=1
    )
    
    # Training data in RecordIO format
    train_input = TrainingInput(
        s3_data="s3://bucket/train.rec",
        content_type="application/x-recordio"
    )
    
    ic_estimator.fit({"train": train_input})
    
    return ic_estimator

# Object Detection algorithm
def train_object_detection():
    container = image_uris.retrieve(
        framework="object-detection",
        region=region
    )
    
    od_estimator = Estimator(
        image_uri=container,
        role=role,
        instance_count=1,
        instance_type="ml.p3.2xlarge",
        output_path=f"s3://{bucket}/{prefix}/od-output"
    )
    
    od_estimator.set_hyperparameters(
        base_network="resnet-50",
        num_classes=20,
        mini_batch_size=16,
        epochs=30,
        learning_rate=0.001,
        lr_scheduler_step="10,20",
        lr_scheduler_factor=0.1
    )
    
    train_input = TrainingInput(
        s3_data="s3://bucket/train_annotation.json",
        content_type="application/x-image"
    )
    
    od_estimator.fit({"train": train_input})
    
    return od_estimator
```

### 3. How do you create custom training jobs in SageMaker?
**Answer:** SageMaker supports custom training scripts using various frameworks.

```python
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.tensorflow import TensorFlow
from sagemaker.pytorch import PyTorch

# Scikit-learn custom training
def custom_sklearn_training():
    sklearn_estimator = SKLearn(
        entry_point="train.py",
        source_dir="src",
        framework_version="0.23-1",
        py_version="py3",
        instance_type="ml.m5.large",
        role=role,
        hyperparameters={
            "n_estimators": 100,
            "max_depth": 5,
            "random_state": 42
        }
    )
    
    sklearn_estimator.fit({"train": train_data_path})
    
    return sklearn_estimator

# TensorFlow custom training
def custom_tensorflow_training():
    tf_estimator = TensorFlow(
        entry_point="tf_train.py",
        source_dir="tensorflow_src",
        framework_version="2.8",
        py_version="py39",
        instance_type="ml.p3.2xlarge",
        instance_count=1,
        role=role,
        hyperparameters={
            "epochs": 10,
            "batch_size": 32,
            "learning_rate": 0.001
        },
        distributions={
            "parameter_server": {
                "enabled": False
            }
        }
    )
    
    tf_estimator.fit({"training": train_data_path})
    
    return tf_estimator

# PyTorch custom training
def custom_pytorch_training():
    pytorch_estimator = PyTorch(
        entry_point="pytorch_train.py",
        source_dir="pytorch_src",
        framework_version="1.12",
        py_version="py38",
        instance_type="ml.p3.2xlarge",
        instance_count=2,  # Multi-instance training
        role=role,
        hyperparameters={
            "epochs": 20,
            "lr": 0.01,
            "batch_size": 64
        },
        distributions={
            "torch_distributed": {
                "enabled": True
            }
        }
    )
    
    pytorch_estimator.fit({"training": train_data_path})
    
    return pytorch_estimator

# Custom container training
def custom_container_training():
    from sagemaker.estimator import Estimator
    
    # Build and push custom Docker image
    custom_estimator = Estimator(
        image_uri="123456789012.dkr.ecr.us-east-1.amazonaws.com/my-custom-algorithm:latest",
        role=role,
        instance_count=1,
        instance_type="ml.m5.large",
        output_path=f"s3://{bucket}/{prefix}/custom-output",
        hyperparameters={
            "learning_rate": 0.01,
            "epochs": 50
        }
    )
    
    custom_estimator.fit({"train": train_data_path})
    
    return custom_estimator

# Training script example (train.py)
training_script = '''
import argparse
import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def model_fn(model_dir):
    """Load model for inference"""
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    return model

def train():
    parser = argparse.ArgumentParser()
    
    # SageMaker specific arguments
    parser.add_argument("--model-dir", type=str, default=os.environ.get("SM_MODEL_DIR"))
    parser.add_argument("--train", type=str, default=os.environ.get("SM_CHANNEL_TRAIN"))
    
    # Hyperparameters
    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--max_depth", type=int, default=5)
    parser.add_argument("--random_state", type=int, default=42)
    
    args = parser.parse_args()
    
    # Load training data
    train_df = pd.read_csv(os.path.join(args.train, "train.csv"))
    
    # Prepare features and target
    X = train_df.drop("target", axis=1)
    y = train_df["target"]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=args.random_state
    )
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
        random_state=args.random_state
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate model
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    print(f"Model accuracy: {accuracy}")
    print("Classification Report:")
    print(classification_report(y_test, predictions))
    
    # Save model
    joblib.dump(model, os.path.join(args.model_dir, "model.joblib"))

if __name__ == "__main__":
    train()
'''
```

### 4. How do you deploy models using SageMaker endpoints?
**Answer:** SageMaker provides real-time and batch inference capabilities.

```python
from sagemaker.predictor import Predictor
from sagemaker.serializers import CSVSerializer
from sagemaker.deserializers import JSONDeserializer

# Real-time endpoint deployment
def deploy_realtime_endpoint(estimator):
    # Deploy model to endpoint
    predictor = estimator.deploy(
        initial_instance_count=1,
        instance_type="ml.m5.large",
        endpoint_name="my-model-endpoint"
    )
    
    return predictor

# Multi-model endpoint
def deploy_multi_model_endpoint():
    from sagemaker.multidatamodel import MultiDataModel
    
    # Create multi-model
    multi_model = MultiDataModel(
        name="multi-model-endpoint",
        model_data_prefix=f"s3://{bucket}/{prefix}/models/",
        image_uri=container_uri,
        role=role
    )
    
    # Deploy multi-model endpoint
    predictor = multi_model.deploy(
        initial_instance_count=1,
        instance_type="ml.m5.large"
    )
    
    return predictor, multi_model

# Auto-scaling endpoint
def deploy_autoscaling_endpoint(estimator):
    predictor = estimator.deploy(
        initial_instance_count=1,
        instance_type="ml.m5.large",
        endpoint_name="autoscaling-endpoint"
    )
    
    # Configure auto-scaling
    import boto3
    
    autoscaling_client = boto3.client("application-autoscaling")
    
    # Register scalable target
    autoscaling_client.register_scalable_target(
        ServiceNamespace="sagemaker",
        ResourceId=f"endpoint/{predictor.endpoint_name}/variant/AllTraffic",
        ScalableDimension="sagemaker:variant:DesiredInstanceCount",
        MinCapacity=1,
        MaxCapacity=10
    )
    
    # Create scaling policy
    autoscaling_client.put_scaling_policy(
        PolicyName="SageMakerEndpointInvocationScalingPolicy",
        ServiceNamespace="sagemaker",
        ResourceId=f"endpoint/{predictor.endpoint_name}/variant/AllTraffic",
        ScalableDimension="sagemaker:variant:DesiredInstanceCount",
        PolicyType="TargetTrackingScaling",
        TargetTrackingScalingPolicyConfiguration={
            "TargetValue": 70.0,
            "PredefinedMetricSpecification": {
                "PredefinedMetricType": "SageMakerVariantInvocationsPerInstance"
            },
            "ScaleOutCooldown": 300,
            "ScaleInCooldown": 300
        }
    )
    
    return predictor

# A/B testing with traffic splitting
def deploy_ab_testing_endpoint(model_a, model_b):
    from sagemaker.model import Model
    
    # Create models
    model_a_sm = Model(
        image_uri=container_uri,
        model_data=model_a.model_data,
        role=role,
        name="model-a"
    )
    
    model_b_sm = Model(
        image_uri=container_uri,
        model_data=model_b.model_data,
        role=role,
        name="model-b"
    )
    
    # Create endpoint configuration with traffic splitting
    from sagemaker.model import Model
    from sagemaker import ModelPackage
    
    endpoint_config_name = "ab-testing-config"
    
    # Deploy with traffic splitting
    predictor = model_a_sm.deploy(
        initial_instance_count=1,
        instance_type="ml.m5.large",
        endpoint_name="ab-testing-endpoint",
        variant_name="model-a-variant"
    )
    
    # Add second variant
    predictor.add_variant(
        model_name="model-b",
        initial_instance_count=1,
        instance_type="ml.m5.large",
        variant_name="model-b-variant",
        initial_weight=50  # 50% traffic
    )
    
    return predictor

# Batch transform job
def run_batch_transform(estimator, input_data_path):
    # Create transformer
    transformer = estimator.transformer(
        instance_count=1,
        instance_type="ml.m5.large",
        output_path=f"s3://{bucket}/{prefix}/batch-output"
    )
    
    # Run batch transform
    transformer.transform(
        data=input_data_path,
        content_type="text/csv",
        split_type="Line"
    )
    
    # Wait for completion
    transformer.wait()
    
    return transformer

# Serverless inference
def deploy_serverless_endpoint(estimator):
    from sagemaker.serverless import ServerlessInferenceConfig
    
    # Configure serverless inference
    serverless_config = ServerlessInferenceConfig(
        memory_size_in_mb=1024,
        max_concurrency=5
    )
    
    # Deploy serverless endpoint
    predictor = estimator.deploy(
        serverless_inference_config=serverless_config,
        endpoint_name="serverless-endpoint"
    )
    
    return predictor

# Async inference
def deploy_async_endpoint(estimator):
    from sagemaker.async_inference import AsyncInferenceConfig
    
    # Configure async inference
    async_config = AsyncInferenceConfig(
        output_path=f"s3://{bucket}/{prefix}/async-output",
        max_concurrent_invocations_per_instance=4,
        failure_path=f"s3://{bucket}/{prefix}/async-failures"
    )
    
    # Deploy async endpoint
    predictor = estimator.deploy(
        initial_instance_count=1,
        instance_type="ml.m5.large",
        async_inference_config=async_config,
        endpoint_name="async-endpoint"
    )
    
    return predictor

# Making predictions
def make_predictions(predictor):
    # Configure serializer and deserializer
    predictor.serializer = CSVSerializer()
    predictor.deserializer = JSONDeserializer()
    
    # Sample data for prediction
    test_data = [[1.0, 2.0, 3.0, 4.0], [2.0, 3.0, 4.0, 5.0]]
    
    # Make prediction
    predictions = predictor.predict(test_data)
    
    print(f"Predictions: {predictions}")
    
    return predictions

# Endpoint monitoring
def setup_endpoint_monitoring(endpoint_name):
    import boto3
    
    cloudwatch = boto3.client("cloudwatch")
    
    # Create custom metric alarm
    cloudwatch.put_metric_alarm(
        AlarmName=f"{endpoint_name}-high-latency",
        ComparisonOperator="GreaterThanThreshold",
        EvaluationPeriods=2,
        MetricName="ModelLatency",
        Namespace="AWS/SageMaker",
        Period=300,
        Statistic="Average",
        Threshold=1000.0,  # 1 second
        ActionsEnabled=True,
        AlarmActions=[
            "arn:aws:sns:us-east-1:123456789012:sagemaker-alerts"
        ],
        AlarmDescription="Alert when model latency is high",
        Dimensions=[
            {
                "Name": "EndpointName",
                "Value": endpoint_name
            }
        ]
    )
```

## Intermediate Concepts

### 5. How do you use SageMaker Pipelines for ML workflows?
**Answer:** SageMaker Pipelines provide ML workflow orchestration with dependency management.

```python
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep, CreateModelStep
from sagemaker.workflow.step_collections import RegisterModel
from sagemaker.workflow.conditions import ConditionLessThanOrEqualTo
from sagemaker.workflow.condition_step import ConditionStep
from sagemaker.workflow.functions import JsonGet
from sagemaker.workflow.parameters import ParameterInteger, ParameterString, ParameterFloat

# Define pipeline parameters
def define_pipeline_parameters():
    processing_instance_count = ParameterInteger(
        name="ProcessingInstanceCount",
        default_value=1
    )
    
    processing_instance_type = ParameterString(
        name="ProcessingInstanceType",
        default_value="ml.m5.xlarge"
    )
    
    training_instance_type = ParameterString(
        name="TrainingInstanceType",
        default_value="ml.m5.xlarge"
    )
    
    model_approval_status = ParameterString(
        name="ModelApprovalStatus",
        default_value="PendingManualApproval"
    )
    
    accuracy_threshold = ParameterFloat(
        name="AccuracyThreshold",
        default_value=0.8
    )
    
    return {
        "processing_instance_count": processing_instance_count,
        "processing_instance_type": processing_instance_type,
        "training_instance_type": training_instance_type,
        "model_approval_status": model_approval_status,
        "accuracy_threshold": accuracy_threshold
    }

# Data processing step
def create_processing_step(parameters):
    from sagemaker.sklearn.processing import SKLearnProcessor
    from sagemaker.processing import ProcessingInput, ProcessingOutput
    
    # Create processor
    sklearn_processor = SKLearnProcessor(
        framework_version="0.23-1",
        instance_type=parameters["processing_instance_type"],
        instance_count=parameters["processing_instance_count"],
        base_job_name="preprocessing",
        role=role
    )
    
    # Processing step
    step_process = ProcessingStep(
        name="PreprocessData",
        processor=sklearn_processor,
        inputs=[
            ProcessingInput(
                source=f"s3://{bucket}/{prefix}/raw-data",
                destination="/opt/ml/processing/input"
            )
        ],
        outputs=[
            ProcessingOutput(
                output_name="train",
                source="/opt/ml/processing/train",
                destination=f"s3://{bucket}/{prefix}/processed/train"
            ),
            ProcessingOutput(
                output_name="validation",
                source="/opt/ml/processing/validation",
                destination=f"s3://{bucket}/{prefix}/processed/validation"
            ),
            ProcessingOutput(
                output_name="test",
                source="/opt/ml/processing/test",
                destination=f"s3://{bucket}/{prefix}/processed/test"
            )
        ],
        code="preprocessing.py"
    )
    
    return step_process

# Training step
def create_training_step(parameters, step_process):
    from sagemaker.sklearn.estimator import SKLearn
    from sagemaker.inputs import TrainingInput
    
    # Create estimator
    sklearn_estimator = SKLearn(
        entry_point="train.py",
        framework_version="0.23-1",
        instance_type=parameters["training_instance_type"],
        role=role,
        hyperparameters={
            "n_estimators": 100,
            "max_depth": 5
        }
    )
    
    # Training step
    step_train = TrainingStep(
        name="TrainModel",
        estimator=sklearn_estimator,
        inputs={
            "train": TrainingInput(
                s3_data=step_process.properties.ProcessingOutputConfig.Outputs["train"].S3Output.S3Uri
            ),
            "validation": TrainingInput(
                s3_data=step_process.properties.ProcessingOutputConfig.Outputs["validation"].S3Output.S3Uri
            )
        }
    )
    
    return step_train

# Model evaluation step
def create_evaluation_step(parameters, step_train, step_process):
    from sagemaker.sklearn.processing import SKLearnProcessor
    
    # Evaluation processor
    evaluation_processor = SKLearnProcessor(
        framework_version="0.23-1",
        instance_type="ml.m5.xlarge",
        instance_count=1,
        base_job_name="evaluation",
        role=role
    )
    
    # Evaluation step
    step_eval = ProcessingStep(
        name="EvaluateModel",
        processor=evaluation_processor,
        inputs=[
            ProcessingInput(
                source=step_train.properties.ModelArtifacts.S3ModelArtifacts,
                destination="/opt/ml/processing/model"
            ),
            ProcessingInput(
                source=step_process.properties.ProcessingOutputConfig.Outputs["test"].S3Output.S3Uri,
                destination="/opt/ml/processing/test"
            )
        ],
        outputs=[
            ProcessingOutput(
                output_name="evaluation",
                source="/opt/ml/processing/evaluation",
                destination=f"s3://{bucket}/{prefix}/evaluation"
            )
        ],
        code="evaluate.py",
        property_files=["evaluation.json"]
    )
    
    return step_eval

# Model registration step
def create_model_registration_step(parameters, step_train, step_eval):
    from sagemaker.model_metrics import MetricsSource, ModelMetrics
    from sagemaker.workflow.step_collections import RegisterModel
    
    # Model metrics
    model_metrics = ModelMetrics(
        model_statistics=MetricsSource(
            s3_uri=f"{step_eval.arguments['ProcessingOutputConfig']['Outputs'][0]['S3Output']['S3Uri']}/evaluation.json",
            content_type="application/json"
        )
    )
    
    # Register model step
    step_register = RegisterModel(
        name="RegisterModel",
        estimator=step_train.estimator,
        model_data=step_train.properties.ModelArtifacts.S3ModelArtifacts,
        content_types=["text/csv"],
        response_types=["text/csv"],
        inference_instances=["ml.t2.medium", "ml.m5.large"],
        transform_instances=["ml.m5.large"],
        model_package_group_name="my-model-package-group",
        approval_status=parameters["model_approval_status"],
        model_metrics=model_metrics
    )
    
    return step_register

# Conditional deployment step
def create_conditional_deployment_step(parameters, step_eval, step_register):
    from sagemaker.workflow.conditions import ConditionGreaterThanOrEqualTo
    from sagemaker.workflow.condition_step import ConditionStep
    from sagemaker.workflow.functions import JsonGet
    
    # Condition for model accuracy
    cond_gte = ConditionGreaterThanOrEqualTo(
        left=JsonGet(
            step_name=step_eval.name,
            property_file="evaluation.json",
            json_path="classification_metrics.accuracy.value"
        ),
        right=parameters["accuracy_threshold"]
    )
    
    # Conditional step
    step_cond = ConditionStep(
        name="CheckAccuracyCondition",
        conditions=[cond_gte],
        if_steps=[step_register],
        else_steps=[]
    )
    
    return step_cond

# Create complete pipeline
def create_ml_pipeline():
    # Define parameters
    parameters = define_pipeline_parameters()
    
    # Create steps
    step_process = create_processing_step(parameters)
    step_train = create_training_step(parameters, step_process)
    step_eval = create_evaluation_step(parameters, step_train, step_process)
    step_register = create_model_registration_step(parameters, step_train, step_eval)
    step_cond = create_conditional_deployment_step(parameters, step_eval, step_register)
    
    # Create pipeline
    pipeline = Pipeline(
        name="MLPipeline",
        parameters=[
            parameters["processing_instance_count"],
            parameters["processing_instance_type"],
            parameters["training_instance_type"],
            parameters["model_approval_status"],
            parameters["accuracy_threshold"]
        ],
        steps=[step_process, step_train, step_eval, step_cond]
    )
    
    return pipeline

# Execute pipeline
def execute_pipeline():
    pipeline = create_ml_pipeline()
    
    # Submit pipeline
    execution = pipeline.start()
    
    # Wait for completion
    execution.wait()
    
    # Get execution steps
    execution.list_steps()
    
    return execution

# Pipeline scheduling
def schedule_pipeline():
    import boto3
    
    events_client = boto3.client("events")
    
    # Create EventBridge rule
    rule_response = events_client.put_rule(
        Name="SageMakerPipelineSchedule",
        ScheduleExpression="rate(7 days)",  # Weekly execution
        Description="Weekly ML pipeline execution",
        State="ENABLED"
    )
    
    # Add target (SageMaker Pipeline)
    events_client.put_targets(
        Rule="SageMakerPipelineSchedule",
        Targets=[
            {
                "Id": "1",
                "Arn": f"arn:aws:sagemaker:{region}:{account_id}:pipeline/MLPipeline",
                "RoleArn": role,
                "SageMakerPipelineParameters": {
                    "PipelineParameterList": [
                        {
                            "Name": "ProcessingInstanceType",
                            "Value": "ml.m5.xlarge"
                        }
                    ]
                }
            }
        ]
    )
    
    return rule_response
```

### 6. How do you use SageMaker Feature Store?
**Answer:** SageMaker Feature Store provides centralized feature management for ML workflows.

```python
from sagemaker.feature_store.feature_group import FeatureGroup
from sagemaker.feature_store.feature_definition import FeatureDefinition, FeatureTypeEnum
import pandas as pd
from datetime import datetime

# Create feature group
def create_feature_group():
    # Define feature definitions
    feature_definitions = [
        FeatureDefinition(feature_name="user_id", feature_type=FeatureTypeEnum.STRING),
        FeatureDefinition(feature_name="age", feature_type=FeatureTypeEnum.INTEGRAL),
        FeatureDefinition(feature_name="income", feature_type=FeatureTypeEnum.FRACTIONAL),
        FeatureDefinition(feature_name="credit_score", feature_type=FeatureTypeEnum.INTEGRAL),
        FeatureDefinition(feature_name="account_balance", feature_type=FeatureTypeEnum.FRACTIONAL),
        FeatureDefinition(feature_name="event_time", feature_type=FeatureTypeEnum.STRING)
    ]
    
    # Create feature group
    feature_group = FeatureGroup(
        name="customer-features",
        feature_definitions=feature_definitions,
        record_identifier_name="user_id",
        event_time_feature_name="event_time",
        role_arn=role,
        enable_online_store=True
    )
    
    # Create feature group
    feature_group.create(
        s3_uri=f"s3://{bucket}/{prefix}/feature-store",
        enable_online_store=True,
        tags=[
            {"Key": "Environment", "Value": "Production"},
            {"Key": "Team", "Value": "DataScience"}
        ]
    )
    
    # Wait for creation
    feature_group.describe()
    
    return feature_group

# Ingest features
def ingest_features(feature_group):
    # Sample feature data
    feature_data = pd.DataFrame({
        "user_id": ["user_001", "user_002", "user_003"],
        "age": [25, 35, 45],
        "income": [50000.0, 75000.0, 100000.0],
        "credit_score": [720, 680, 750],
        "account_balance": [5000.0, 15000.0, 25000.0],
        "event_time": [datetime.now().isoformat()] * 3
    })
    
    # Ingest data
    feature_group.ingest(
        data_frame=feature_data,
        max_workers=3,
        wait=True
    )
    
    return feature_data

# Batch ingestion from S3
def batch_ingest_from_s3(feature_group):
    # Upload data to S3
    feature_data_path = f"s3://{bucket}/{prefix}/feature-data/features.csv"
    
    # Ingest from S3
    feature_group.ingest(
        data_source=feature_data_path,
        max_workers=5,
        wait=True
    )

# Online feature serving
def get_online_features(feature_group):
    # Get record from online store
    record = feature_group.get_record(record_identifier_value="user_001")
    
    print(f"Online record: {record}")
    
    return record

# Offline feature serving
def get_offline_features(feature_group):
    # Build query for offline store
    query = feature_group.athena_query()
    
    # Execute query
    query_string = f"""
    SELECT user_id, age, income, credit_score, account_balance
    FROM "{query.table_name}"
    WHERE age > 30
    """
    
    query.run(
        query_string=query_string,
        output_location=f"s3://{bucket}/{prefix}/query-results/"
    )
    
    # Wait for completion and get results
    query.wait()
    df = query.as_dataframe()
    
    return df

# Feature engineering pipeline
def create_feature_engineering_pipeline():
    from sagemaker.sklearn.processing import SKLearnProcessor
    from sagemaker.processing import ProcessingInput, ProcessingOutput
    
    # Feature engineering processor
    feature_processor = SKLearnProcessor(
        framework_version="0.23-1",
        instance_type="ml.m5.xlarge",
        instance_count=1,
        base_job_name="feature-engineering",
        role=role
    )
    
    # Run feature engineering
    feature_processor.run(
        code="feature_engineering.py",
        inputs=[
            ProcessingInput(
                source=f"s3://{bucket}/{prefix}/raw-data/",
                destination="/opt/ml/processing/input"
            )
        ],
        outputs=[
            ProcessingOutput(
                output_name="features",
                source="/opt/ml/processing/output",
                destination=f"s3://{bucket}/{prefix}/engineered-features/"
            )
        ]
    )
    
    return feature_processor

# Feature monitoring and data quality
def setup_feature_monitoring(feature_group):
    from sagemaker.model_monitor import DataCaptureConfig
    
    # Create data quality monitoring
    data_quality_monitor = sagemaker.model_monitor.DefaultModelMonitor(
        role=role,
        instance_count=1,
        instance_type="ml.m5.xlarge",
        volume_size_in_gb=20,
        max_runtime_in_seconds=3600
    )
    
    # Suggest baseline
    baseline_job = data_quality_monitor.suggest_baseline(
        baseline_dataset=f"s3://{bucket}/{prefix}/baseline-data/baseline.csv",
        dataset_format=sagemaker.model_monitor.DatasetFormat.csv(header=True),
        output_s3_uri=f"s3://{bucket}/{prefix}/baseline-results"
    )
    
    return data_quality_monitor, baseline_job

# Cross-account feature sharing
def setup_cross_account_sharing(feature_group, target_account_id):
    import boto3
    
    # Create resource policy for cross-account access
    resource_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "CrossAccountAccess",
                "Effect": "Allow",
                "Principal": {
                    "AWS": f"arn:aws:iam::{target_account_id}:root"
                },
                "Action": [
                    "sagemaker:GetRecord",
                    "sagemaker:BatchGetRecord"
                ],
                "Resource": feature_group.describe()["FeatureGroupArn"]
            }
        ]
    }
    
    # Apply resource policy
    sagemaker_client = boto3.client("sagemaker")
    
    sagemaker_client.put_resource_policy(
        ResourceArn=feature_group.describe()["FeatureGroupArn"],
        Policy=json.dumps(resource_policy)
    )

# Feature lineage tracking
def track_feature_lineage(feature_group):
    from sagemaker.lineage import context, artifact, association
    
    # Create lineage context
    feature_context = context.Context.create(
        context_name="feature-engineering-context",
        context_type="FeatureEngineering",
        source_uri=f"s3://{bucket}/{prefix}/raw-data/"
    )
    
    # Create feature artifact
    feature_artifact = artifact.Artifact.create(
        artifact_name="customer-features-artifact",
        artifact_type="FeatureGroup",
        source_uri=feature_group.describe()["OfflineStoreConfig"]["S3StorageConfig"]["S3Uri"]
    )
    
    # Create association
    association.Association.create(
        source_arn=feature_context.context_arn,
        destination_arn=feature_artifact.artifact_arn,
        association_type="Produced"
    )
    
    return feature_context, feature_artifact

# Usage example
if __name__ == "__main__":
    # Create and populate feature group
    fg = create_feature_group()
    ingest_features(fg)
    
    # Get features
    online_record = get_online_features(fg)
    offline_df = get_offline_features(fg)
    
    print("Feature Store setup completed!")
```

This comprehensive Amazon SageMaker interview questions set covers fundamental concepts through advanced MLOps implementations, providing practical examples for training, deployment, pipelines, feature stores, and production monitoring.