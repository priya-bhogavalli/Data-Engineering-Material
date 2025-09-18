# Vertex AI Interview Questions

## Basic Concepts

### 1. What is Google Cloud Vertex AI and its key components?
**Answer:** Vertex AI is Google Cloud's unified ML platform for building, deploying, and scaling ML models. Key components:

- **Vertex AI Workbench**: Managed Jupyter notebooks
- **AutoML**: No-code ML model training
- **Custom Training**: Code-based model training
- **Model Registry**: Centralized model management
- **Endpoints**: Model serving infrastructure
- **Pipelines**: ML workflow orchestration
- **Feature Store**: Centralized feature management

```python
from google.cloud import aiplatform

# Initialize Vertex AI
aiplatform.init(project="my-project", location="us-central1")

# Create AutoML tabular dataset
dataset = aiplatform.TabularDataset.create(
    display_name="my-dataset",
    gcs_source="gs://my-bucket/data.csv"
)

# Train AutoML model
job = aiplatform.AutoMLTabularTrainingJob(
    display_name="my-automl-job",
    optimization_prediction_type="classification"
)

model = job.run(
    dataset=dataset,
    target_column="label",
    training_fraction_split=0.8,
    validation_fraction_split=0.1,
    test_fraction_split=0.1
)
```

### 2. How do you use Vertex AI AutoML for different ML tasks?
**Answer:** AutoML provides no-code solutions for various ML tasks.

```python
from google.cloud import aiplatform

# AutoML Image Classification
def train_automl_image_classification():
    dataset = aiplatform.ImageDataset.create(
        display_name="image-classification-dataset",
        gcs_source="gs://my-bucket/image_data.csv"
    )
    
    job = aiplatform.AutoMLImageTrainingJob(
        display_name="automl-image-training",
        prediction_type="classification"
    )
    
    model = job.run(
        dataset=dataset,
        model_display_name="image-classifier",
        training_fraction_split=0.8,
        validation_fraction_split=0.1,
        test_fraction_split=0.1,
        budget_milli_node_hours=8000
    )
    
    return model

# AutoML Text Classification
def train_automl_text_classification():
    dataset = aiplatform.TextDataset.create(
        display_name="text-classification-dataset",
        gcs_source="gs://my-bucket/text_data.jsonl"
    )
    
    job = aiplatform.AutoMLTextTrainingJob(
        display_name="automl-text-training",
        prediction_type="classification"
    )
    
    model = job.run(
        dataset=dataset,
        model_display_name="text-classifier"
    )
    
    return model

# AutoML Tabular Regression
def train_automl_tabular_regression():
    dataset = aiplatform.TabularDataset.create(
        display_name="tabular-regression-dataset",
        gcs_source="gs://my-bucket/tabular_data.csv"
    )
    
    job = aiplatform.AutoMLTabularTrainingJob(
        display_name="automl-tabular-training",
        optimization_prediction_type="regression",
        optimization_objective="minimize-rmse"
    )
    
    model = job.run(
        dataset=dataset,
        target_column="target_value",
        predefined_split_column_name="split"
    )
    
    return model

# AutoML Forecasting
def train_automl_forecasting():
    dataset = aiplatform.TimeSeriesDataset.create(
        display_name="forecasting-dataset",
        gcs_source="gs://my-bucket/timeseries_data.csv"
    )
    
    job = aiplatform.AutoMLForecastingTrainingJob(
        display_name="automl-forecasting-training",
        optimization_objective="minimize-rmse"
    )
    
    model = job.run(
        dataset=dataset,
        target_column="sales",
        time_column="date",
        time_series_identifier_column="store_id",
        forecast_horizon=30,
        data_granularity_unit="day",
        data_granularity_count=1
    )
    
    return model
```

### 3. How do you perform custom training in Vertex AI?
**Answer:** Custom training allows you to use your own training code and containers.

```python
from google.cloud import aiplatform
from google.cloud.aiplatform import gapic as aip

# Custom training with pre-built container
def custom_training_prebuilt():
    job = aiplatform.CustomTrainingJob(
        display_name="custom-training-job",
        script_path="trainer/task.py",
        container_uri="gcr.io/cloud-aiplatform/training/tf-enterprise-2.8-cpu:latest",
        requirements=["pandas", "scikit-learn"],
        model_serving_container_image_uri="gcr.io/cloud-aiplatform/prediction/tf2-cpu.2-8:latest"
    )
    
    model = job.run(
        dataset=dataset,
        replica_count=1,
        machine_type="n1-standard-4",
        accelerator_type=aip.AcceleratorType.NVIDIA_TESLA_K80,
        accelerator_count=1,
        args=["--epochs", "100", "--batch-size", "32"],
        environment_variables={"MY_ENV_VAR": "value"}
    )
    
    return model

# Custom training with custom container
def custom_training_container():
    job = aiplatform.CustomContainerTrainingJob(
        display_name="custom-container-training",
        container_uri="gcr.io/my-project/my-training-image:latest",
        model_serving_container_image_uri="gcr.io/my-project/my-serving-image:latest"
    )
    
    model = job.run(
        args=["--model-dir", "/tmp/model", "--data-dir", "/tmp/data"],
        replica_count=1,
        machine_type="n1-highmem-2",
        sync=True
    )
    
    return model

# Distributed training
def distributed_training():
    job = aiplatform.CustomTrainingJob(
        display_name="distributed-training",
        script_path="trainer/distributed_task.py",
        container_uri="gcr.io/cloud-aiplatform/training/tf-enterprise-2.8-gpu:latest"
    )
    
    model = job.run(
        replica_count=4,  # Multiple replicas for distributed training
        machine_type="n1-standard-8",
        accelerator_type=aip.AcceleratorType.NVIDIA_TESLA_V100,
        accelerator_count=2,
        args=["--strategy", "MultiWorkerMirroredStrategy"]
    )
    
    return model

# Hyperparameter tuning
def hyperparameter_tuning():
    from google.cloud.aiplatform import hyperparameter_tuning as hpt
    
    job = aiplatform.CustomTrainingJob(
        display_name="hp-tuning-job",
        script_path="trainer/hp_task.py",
        container_uri="gcr.io/cloud-aiplatform/training/tf-enterprise-2.8-cpu:latest"
    )
    
    hp_job = aiplatform.HyperparameterTuningJob(
        display_name="hp-tuning",
        custom_job=job,
        metric_spec={
            "accuracy": "maximize",
        },
        parameter_spec={
            "learning_rate": hpt.DoubleParameterSpec(min=0.001, max=0.1, scale="log"),
            "batch_size": hpt.IntegerParameterSpec(min=16, max=128, scale="linear"),
            "hidden_units": hpt.DiscreteParameterSpec(values=[64, 128, 256], scale="linear")
        },
        max_trial_count=20,
        parallel_trial_count=5
    )
    
    hp_job.run()
    
    return hp_job
```

### 4. How do you deploy and serve models using Vertex AI Endpoints?
**Answer:** Vertex AI Endpoints provide scalable model serving infrastructure.

```python
from google.cloud import aiplatform

# Deploy model to endpoint
def deploy_model_to_endpoint(model):
    endpoint = aiplatform.Endpoint.create(
        display_name="my-endpoint",
        description="Endpoint for serving my model"
    )
    
    deployed_model = model.deploy(
        endpoint=endpoint,
        deployed_model_display_name="my-deployed-model",
        machine_type="n1-standard-2",
        min_replica_count=1,
        max_replica_count=10,
        accelerator_type=aip.AcceleratorType.NVIDIA_TESLA_T4,
        accelerator_count=1,
        traffic_percentage=100,
        sync=True
    )
    
    return endpoint, deployed_model

# Online prediction
def online_prediction(endpoint, instances):
    predictions = endpoint.predict(instances=instances)
    return predictions.predictions

# Batch prediction
def batch_prediction(model, input_uri, output_uri):
    batch_prediction_job = model.batch_predict(
        job_display_name="batch-prediction-job",
        gcs_source=input_uri,
        gcs_destination_prefix=output_uri,
        machine_type="n1-standard-4",
        accelerator_type=aip.AcceleratorType.NVIDIA_TESLA_K80,
        accelerator_count=1,
        sync=True
    )
    
    return batch_prediction_job

# A/B testing with traffic splitting
def ab_testing_deployment(model_a, model_b, endpoint):
    # Deploy model A with 50% traffic
    model_a.deploy(
        endpoint=endpoint,
        deployed_model_display_name="model-a",
        machine_type="n1-standard-2",
        traffic_percentage=50
    )
    
    # Deploy model B with 50% traffic
    model_b.deploy(
        endpoint=endpoint,
        deployed_model_display_name="model-b",
        machine_type="n1-standard-2",
        traffic_percentage=50
    )
    
    return endpoint

# Custom prediction routine
def deploy_custom_prediction():
    from google.cloud.aiplatform.prediction import LocalModel
    
    # Create local model with custom predictor
    local_model = LocalModel.build_cpr_model(
        "my_predictor",
        "predictor.py",
        requirements_path="requirements.txt",
        base_image="python:3.8-slim"
    )
    
    # Upload to Model Registry
    model = local_model.upload(
        display_name="custom-prediction-model"
    )
    
    # Deploy to endpoint
    endpoint = model.deploy(
        machine_type="n1-standard-2",
        min_replica_count=1,
        max_replica_count=5
    )
    
    return endpoint
```

## Intermediate Concepts

### 5. How do you use Vertex AI Pipelines for ML workflows?
**Answer:** Vertex AI Pipelines orchestrate ML workflows using Kubeflow Pipelines.

```python
from kfp.v2 import dsl
from kfp.v2.dsl import component, pipeline, Input, Output, Dataset, Model, Metrics
from google.cloud import aiplatform

# Define pipeline components
@component(
    packages_to_install=["pandas", "scikit-learn"],
    base_image="python:3.8"
)
def data_preprocessing(
    input_data: Input[Dataset],
    processed_data: Output[Dataset]
):
    import pandas as pd
    from sklearn.preprocessing import StandardScaler
    import pickle
    
    # Load data
    df = pd.read_csv(input_data.path)
    
    # Preprocessing
    scaler = StandardScaler()
    features = df.drop('target', axis=1)
    scaled_features = scaler.fit_transform(features)
    
    # Save processed data
    processed_df = pd.DataFrame(scaled_features, columns=features.columns)
    processed_df['target'] = df['target']
    processed_df.to_csv(processed_data.path, index=False)
    
    # Save scaler
    with open(processed_data.path + '_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

@component(
    packages_to_install=["pandas", "scikit-learn"],
    base_image="python:3.8"
)
def train_model(
    processed_data: Input[Dataset],
    model_artifact: Output[Model],
    metrics: Output[Metrics]
):
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, classification_report
    import pickle
    import json
    
    # Load processed data
    df = pd.read_csv(processed_data.path)
    X = df.drop('target', axis=1)
    y = df['target']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    # Save model
    with open(model_artifact.path, 'wb') as f:
        pickle.dump(model, f)
    
    # Log metrics
    metrics.log_metric("accuracy", accuracy)
    metrics.log_metric("num_features", len(X.columns))

@component(
    packages_to_install=["google-cloud-aiplatform"],
    base_image="python:3.8"
)
def deploy_model(
    model_artifact: Input[Model],
    project: str,
    location: str
) -> str:
    from google.cloud import aiplatform
    
    aiplatform.init(project=project, location=location)
    
    # Upload model to Vertex AI
    uploaded_model = aiplatform.Model.upload(
        display_name="pipeline-trained-model",
        artifact_uri=model_artifact.uri,
        serving_container_image_uri="gcr.io/cloud-aiplatform/prediction/sklearn-cpu.1-0:latest"
    )
    
    # Deploy to endpoint
    endpoint = uploaded_model.deploy(
        machine_type="n1-standard-2",
        min_replica_count=1,
        max_replica_count=3
    )
    
    return endpoint.resource_name

# Define pipeline
@pipeline(
    name="ml-training-pipeline",
    description="Complete ML training and deployment pipeline"
)
def ml_pipeline(
    input_data_uri: str,
    project: str = "my-project",
    location: str = "us-central1"
):
    # Data preprocessing step
    preprocess_task = data_preprocessing(
        input_data=input_data_uri
    )
    
    # Model training step
    train_task = train_model(
        processed_data=preprocess_task.outputs["processed_data"]
    )
    
    # Model deployment step
    deploy_task = deploy_model(
        model_artifact=train_task.outputs["model_artifact"],
        project=project,
        location=location
    )

# Compile and run pipeline
def run_pipeline():
    from kfp.v2 import compiler
    
    # Compile pipeline
    compiler.Compiler().compile(
        pipeline_func=ml_pipeline,
        package_path="ml_pipeline.json"
    )
    
    # Create pipeline job
    job = aiplatform.PipelineJob(
        display_name="ml-training-pipeline-run",
        template_path="ml_pipeline.json",
        parameter_values={
            "input_data_uri": "gs://my-bucket/training_data.csv",
            "project": "my-project",
            "location": "us-central1"
        }
    )
    
    # Submit pipeline
    job.submit()
    
    return job

# Pipeline with conditional logic
@pipeline(name="conditional-pipeline")
def conditional_pipeline(accuracy_threshold: float = 0.8):
    train_task = train_model()
    
    with dsl.Condition(
        train_task.outputs["metrics"].get_float_metric("accuracy") > accuracy_threshold,
        name="accuracy-check"
    ):
        deploy_task = deploy_model(
            model_artifact=train_task.outputs["model_artifact"]
        )
```

### 6. How do you use Vertex AI Feature Store?
**Answer:** Feature Store provides centralized feature management and serving.

```python
from google.cloud import aiplatform
from google.cloud.aiplatform import Feature, EntityType, Featurestore

# Create Feature Store
def create_feature_store():
    featurestore = aiplatform.Featurestore.create(
        featurestore_id="my_featurestore",
        online_store_fixed_node_count=1,
        labels={"environment": "production"}
    )
    
    return featurestore

# Create Entity Type
def create_entity_type(featurestore):
    entity_type = featurestore.create_entity_type(
        entity_type_id="user",
        description="User entity for recommendation system"
    )
    
    return entity_type

# Create Features
def create_features(entity_type):
    # User demographic features
    age_feature = entity_type.create_feature(
        feature_id="age",
        value_type="INT64",
        description="User age"
    )
    
    income_feature = entity_type.create_feature(
        feature_id="income",
        value_type="DOUBLE",
        description="User annual income"
    )
    
    category_feature = entity_type.create_feature(
        feature_id="preferred_category",
        value_type="STRING",
        description="User's preferred product category"
    )
    
    return [age_feature, income_feature, category_feature]

# Batch ingestion
def batch_ingest_features(entity_type):
    import pandas as pd
    
    # Prepare feature data
    feature_data = pd.DataFrame({
        'user_id': ['user_1', 'user_2', 'user_3'],
        'age': [25, 35, 45],
        'income': [50000.0, 75000.0, 100000.0],
        'preferred_category': ['electronics', 'books', 'clothing'],
        'feature_timestamp': ['2023-01-01T00:00:00Z'] * 3
    })
    
    # Save to GCS
    gcs_path = "gs://my-bucket/feature_data.csv"
    feature_data.to_csv(gcs_path, index=False)
    
    # Ingest features
    ingestion_job = entity_type.ingest_from_gcs(
        feature_ids=["age", "income", "preferred_category"],
        feature_time="feature_timestamp",
        gcs_source_uris=[gcs_path],
        gcs_source_type="csv",
        entity_id_field="user_id"
    )
    
    return ingestion_job

# Streaming ingestion
def stream_ingest_features(entity_type):
    # Write features directly
    entity_type.write_feature_values([
        {
            "entity_id": "user_4",
            "feature_values": {
                "age": {"int64_value": 30},
                "income": {"double_value": 60000.0},
                "preferred_category": {"string_value": "sports"}
            }
        }
    ])

# Online feature serving
def serve_features_online(entity_type):
    # Read features for online serving
    feature_values = entity_type.read_feature_values(
        entity_ids=["user_1", "user_2"],
        feature_selector=aiplatform.FeatureSelector(
            id_matcher=aiplatform.IdMatcher(ids=["age", "income", "preferred_category"])
        )
    )
    
    return feature_values

# Feature serving for training
def get_training_features(featurestore):
    # Create feature selector
    feature_selector = aiplatform.FeatureSelector(
        id_matcher=aiplatform.IdMatcher(
            ids=["user.age", "user.income", "user.preferred_category"]
        )
    )
    
    # Read historical features
    df = featurestore.batch_serve_to_df(
        serving_feature_ids={
            "user": ["age", "income", "preferred_category"]
        },
        read_instances_uri="gs://my-bucket/entity_ids.csv"
    )
    
    return df

# Point-in-time lookup
def point_in_time_lookup(featurestore):
    # Read features at specific timestamps
    df = featurestore.batch_serve_to_df(
        serving_feature_ids={
            "user": ["age", "income", "preferred_category"]
        },
        read_instances_uri="gs://my-bucket/entity_timestamps.csv",
        pass_through_fields=["timestamp", "label"]
    )
    
    return df
```

### 7. How do you implement MLOps practices with Vertex AI?
**Answer:** Vertex AI supports comprehensive MLOps workflows including monitoring, versioning, and automation.

```python
from google.cloud import aiplatform
from google.cloud.aiplatform import pipeline_jobs
import json

# Model versioning and registry
class ModelRegistry:
    def __init__(self, project, location):
        aiplatform.init(project=project, location=location)
        self.project = project
        self.location = location
    
    def register_model(self, model_path, model_name, version, metadata=None):
        # Upload model with version
        model = aiplatform.Model.upload(
            display_name=f"{model_name}-v{version}",
            artifact_uri=model_path,
            serving_container_image_uri="gcr.io/cloud-aiplatform/prediction/sklearn-cpu.1-0:latest",
            labels={
                "model_name": model_name,
                "version": str(version),
                "environment": "production"
            }
        )
        
        # Add metadata
        if metadata:
            model.update(labels=metadata)
        
        return model
    
    def get_latest_model(self, model_name):
        models = aiplatform.Model.list(
            filter=f'labels.model_name="{model_name}"',
            order_by="create_time desc"
        )
        
        return models[0] if models else None
    
    def promote_model(self, model, stage):
        # Update model stage
        current_labels = model.labels or {}
        current_labels["stage"] = stage
        model.update(labels=current_labels)
        
        return model

# Continuous training pipeline
def create_continuous_training_pipeline():
    @dsl.pipeline(name="continuous-training")
    def continuous_training_pipeline(
        training_data_uri: str,
        model_name: str,
        accuracy_threshold: float = 0.85
    ):
        # Data validation
        data_validation_task = data_validation_component(
            data_uri=training_data_uri
        )
        
        # Model training
        training_task = train_model_component(
            training_data=data_validation_task.outputs["validated_data"]
        )
        
        # Model evaluation
        evaluation_task = evaluate_model_component(
            model=training_task.outputs["model"],
            test_data=data_validation_task.outputs["test_data"]
        )
        
        # Conditional deployment
        with dsl.Condition(
            evaluation_task.outputs["accuracy"] > accuracy_threshold
        ):
            # Register model
            registration_task = register_model_component(
                model=training_task.outputs["model"],
                model_name=model_name,
                metrics=evaluation_task.outputs["metrics"]
            )
            
            # Deploy model
            deployment_task = deploy_model_component(
                model=registration_task.outputs["registered_model"]
            )
    
    return continuous_training_pipeline

# Model monitoring
def setup_model_monitoring(endpoint, dataset):
    # Create monitoring job
    monitoring_job = aiplatform.ModelDeploymentMonitoringJob.create(
        display_name="model-monitoring-job",
        endpoint=endpoint,
        logging_sampling_strategy=aiplatform.SamplingStrategy(
            random_sample_config=aiplatform.RandomSampleConfig(
                sample_rate=0.1
            )
        ),
        schedule_config=aiplatform.ScheduleConfig(
            cron="0 */6 * * *"  # Every 6 hours
        ),
        model_deployment_monitoring_objective_configs=[
            aiplatform.ModelDeploymentMonitoringObjectiveConfig(
                deployed_model_id=endpoint.list_models()[0].id,
                objective_config=aiplatform.ModelMonitoringObjectiveConfig(
                    training_dataset=aiplatform.ModelMonitoringObjectiveConfig.TrainingDataset(
                        dataset=dataset,
                        target_field="target"
                    ),
                    training_prediction_skew_detection_config=aiplatform.ModelMonitoringObjectiveConfig.TrainingPredictionSkewDetectionConfig(
                        skew_thresholds={
                            "feature1": 0.1,
                            "feature2": 0.2
                        }
                    ),
                    prediction_drift_detection_config=aiplatform.ModelMonitoringObjectiveConfig.PredictionDriftDetectionConfig(
                        drift_thresholds={
                            "feature1": 0.1,
                            "feature2": 0.2
                        }
                    )
                )
            )
        ]
    )
    
    return monitoring_job

# A/B testing framework
class ABTestingFramework:
    def __init__(self, endpoint):
        self.endpoint = endpoint
    
    def setup_ab_test(self, model_a, model_b, traffic_split=0.5):
        # Deploy model A
        model_a.deploy(
            endpoint=self.endpoint,
            deployed_model_display_name="model-a",
            traffic_percentage=int(traffic_split * 100),
            machine_type="n1-standard-2"
        )
        
        # Deploy model B
        model_b.deploy(
            endpoint=self.endpoint,
            deployed_model_display_name="model-b",
            traffic_percentage=int((1 - traffic_split) * 100),
            machine_type="n1-standard-2"
        )
    
    def analyze_ab_test(self, days=7):
        # Query prediction logs
        from google.cloud import bigquery
        
        client = bigquery.Client()
        
        query = f"""
        SELECT
            deployed_model_id,
            COUNT(*) as prediction_count,
            AVG(CAST(JSON_EXTRACT_SCALAR(prediction, '$.confidence') AS FLOAT64)) as avg_confidence
        FROM `{self.project}.{self.dataset}.predictions`
        WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {days} DAY)
        GROUP BY deployed_model_id
        """
        
        results = client.query(query).to_dataframe()
        return results
    
    def promote_winner(self, winning_model_id):
        # Update traffic to 100% for winning model
        deployed_models = self.endpoint.list_models()
        
        for model in deployed_models:
            if model.id == winning_model_id:
                model.update(traffic_percentage=100)
            else:
                model.undeploy()

# Automated retraining
def setup_automated_retraining():
    from google.cloud import scheduler
    
    # Create Cloud Scheduler job for retraining
    scheduler_client = scheduler.CloudSchedulerClient()
    
    job = {
        "name": f"projects/{project}/locations/{location}/jobs/retrain-model",
        "schedule": "0 2 * * 0",  # Weekly on Sunday at 2 AM
        "time_zone": "UTC",
        "http_target": {
            "uri": f"https://{location}-aiplatform.googleapis.com/v1/projects/{project}/locations/{location}/pipelineJobs",
            "http_method": "POST",
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "displayName": "automated-retraining",
                "templateUri": "gs://my-bucket/retraining_pipeline.json",
                "parameterValues": {
                    "training_data_uri": "gs://my-bucket/latest_training_data.csv"
                }
            }).encode()
        }
    }
    
    scheduler_client.create_job(
        parent=f"projects/{project}/locations/{location}",
        job=job
    )

# Usage example
if __name__ == "__main__":
    # Initialize MLOps components
    registry = ModelRegistry("my-project", "us-central1")
    
    # Register new model version
    model = registry.register_model(
        model_path="gs://my-bucket/model/",
        model_name="recommendation_model",
        version="1.2.0",
        metadata={"accuracy": "0.92", "f1_score": "0.89"}
    )
    
    # Promote to production
    registry.promote_model(model, "production")
```

This comprehensive Vertex AI interview questions set covers fundamental concepts through advanced MLOps implementations, providing practical examples for AutoML, custom training, pipelines, feature stores, and production deployment strategies.