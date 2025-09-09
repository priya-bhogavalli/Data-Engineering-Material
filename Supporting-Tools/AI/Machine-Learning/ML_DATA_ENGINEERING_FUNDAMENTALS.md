# ML Fundamentals for Data Engineers

## 1. ML in Data Engineering Context

### Data Pipeline Integration
```python
# ML-aware data pipeline
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

def ml_data_pipeline():
    """Data engineering pipeline optimized for ML workloads"""
    
    # Feature store integration
    def extract_features():
        # Extract features with ML requirements in mind
        features = extract_time_series_features()
        validate_feature_quality(features)
        return features
    
    def validate_feature_quality(features):
        # Data quality checks for ML
        assert features.isnull().sum().sum() == 0, "No null values allowed"
        assert features.dtypes.apply(lambda x: x.kind in 'biufc').all(), "Only numeric features"
        
    return extract_features

# Feature engineering pipeline
def create_ml_features(raw_data):
    """Transform raw data into ML-ready features"""
    
    # Temporal features
    raw_data['hour'] = raw_data['timestamp'].dt.hour
    raw_data['day_of_week'] = raw_data['timestamp'].dt.dayofweek
    
    # Aggregation features
    features = raw_data.groupby('customer_id').agg({
        'transaction_amount': ['mean', 'std', 'count'],
        'hour': lambda x: x.mode().iloc[0]  # Most common hour
    }).reset_index()
    
    return features
```

### Real-time ML Serving
```python
# Streaming ML inference
from kafka import KafkaConsumer, KafkaProducer
import json
import joblib

class RealTimeMLService:
    def __init__(self, model_path, kafka_config):
        self.model = joblib.load(model_path)
        self.consumer = KafkaConsumer('input_features', **kafka_config)
        self.producer = KafkaProducer('predictions', **kafka_config)
    
    def process_stream(self):
        for message in self.consumer:
            features = json.loads(message.value)
            prediction = self.model.predict([features['data']])[0]
            
            result = {
                'id': features['id'],
                'prediction': prediction,
                'timestamp': datetime.now().isoformat()
            }
            
            self.producer.send('predictions', json.dumps(result))
```

## 2. Mathematical Foundations

### Linear Algebra for ML
```python
import numpy as np

# Matrix operations fundamental to ML
def ml_linear_algebra():
    """Core linear algebra concepts for ML"""
    
    # Feature matrix (n_samples × n_features)
    X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    
    # Dot product (fundamental to neural networks)
    weights = np.array([0.1, 0.2, 0.3])
    output = np.dot(X, weights)  # Linear transformation
    
    # Eigenvalues/eigenvectors (PCA foundation)
    covariance_matrix = np.cov(X.T)
    eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)
    
    return {
        'linear_transformation': output,
        'eigenvalues': eigenvalues,
        'eigenvectors': eigenvectors
    }
```

### Statistical Foundations
```python
from scipy import stats
import pandas as pd

def statistical_foundations():
    """Statistical concepts essential for ML"""
    
    # Central Limit Theorem application
    sample_means = [np.random.normal(50, 10, 30).mean() for _ in range(1000)]
    
    # Hypothesis testing for model comparison
    model_a_scores = np.random.normal(0.85, 0.05, 100)
    model_b_scores = np.random.normal(0.87, 0.05, 100)
    
    t_stat, p_value = stats.ttest_ind(model_a_scores, model_b_scores)
    
    # Confidence intervals
    confidence_interval = stats.t.interval(
        0.95, len(model_a_scores)-1,
        loc=np.mean(model_a_scores),
        scale=stats.sem(model_a_scores)
    )
    
    return {
        'sample_distribution': sample_means,
        'hypothesis_test': {'t_stat': t_stat, 'p_value': p_value},
        'confidence_interval': confidence_interval
    }
```

## 3. Data Engineering Specific ML Patterns

### Batch vs Stream Processing
```python
# Batch ML processing
def batch_ml_pipeline(data_path):
    """Traditional batch ML processing"""
    
    # Load large dataset
    df = pd.read_parquet(data_path)
    
    # Feature engineering
    features = create_features(df)
    
    # Model training
    model = train_model(features)
    
    # Batch predictions
    predictions = model.predict(features)
    
    return predictions

# Stream ML processing
def stream_ml_pipeline():
    """Real-time stream ML processing"""
    
    from kafka import KafkaConsumer
    
    consumer = KafkaConsumer('events')
    model = load_pretrained_model()
    
    for message in consumer:
        # Process single event
        event = json.loads(message.value)
        features = extract_features(event)
        prediction = model.predict([features])[0]
        
        # Immediate action
        if prediction > 0.8:
            trigger_alert(event, prediction)
```

### Feature Store Architecture
```python
class FeatureStore:
    """Centralized feature management for ML"""
    
    def __init__(self, storage_backend):
        self.storage = storage_backend
        self.feature_registry = {}
    
    def register_feature(self, name, computation_fn, dependencies):
        """Register feature computation logic"""
        self.feature_registry[name] = {
            'compute': computation_fn,
            'dependencies': dependencies,
            'last_updated': None
        }
    
    def compute_features(self, feature_names, entity_ids):
        """Compute features for given entities"""
        results = {}
        
        for feature_name in feature_names:
            if feature_name in self.feature_registry:
                compute_fn = self.feature_registry[feature_name]['compute']
                results[feature_name] = compute_fn(entity_ids)
        
        return results
    
    def get_training_data(self, features, labels, time_range):
        """Generate training dataset with point-in-time correctness"""
        
        training_data = []
        for timestamp in time_range:
            # Get features as they existed at this timestamp
            feature_values = self.get_historical_features(features, timestamp)
            label_values = self.get_historical_labels(labels, timestamp)
            
            training_data.append({
                'timestamp': timestamp,
                'features': feature_values,
                'labels': label_values
            })
        
        return pd.DataFrame(training_data)
```

## 4. ML Model Lifecycle in Production

### Model Versioning Strategy
```python
class ModelVersionManager:
    """Manage ML model versions in production"""
    
    def __init__(self, model_registry):
        self.registry = model_registry
        self.active_models = {}
    
    def deploy_model(self, model_name, version, traffic_percentage=0):
        """Deploy model version with traffic splitting"""
        
        model_artifact = self.registry.get_model(model_name, version)
        
        self.active_models[f"{model_name}:{version}"] = {
            'model': model_artifact,
            'traffic': traffic_percentage,
            'deployed_at': datetime.now(),
            'metrics': {}
        }
    
    def route_prediction(self, model_name, features):
        """Route prediction to appropriate model version"""
        
        # Get active versions for model
        active_versions = [
            k for k in self.active_models.keys() 
            if k.startswith(model_name)
        ]
        
        # Traffic-based routing
        random_value = np.random.random()
        cumulative_traffic = 0
        
        for version_key in active_versions:
            traffic = self.active_models[version_key]['traffic']
            cumulative_traffic += traffic
            
            if random_value <= cumulative_traffic:
                model = self.active_models[version_key]['model']
                return model.predict([features])[0]
        
        # Default to latest version
        return self.active_models[active_versions[-1]]['model'].predict([features])[0]
```

### Data Drift Detection
```python
from scipy.stats import ks_2samp
import numpy as np

class DataDriftDetector:
    """Detect data drift in production ML systems"""
    
    def __init__(self, reference_data, threshold=0.05):
        self.reference_data = reference_data
        self.threshold = threshold
    
    def detect_drift(self, current_data):
        """Detect statistical drift between reference and current data"""
        
        drift_results = {}
        
        for column in self.reference_data.columns:
            if column in current_data.columns:
                # Kolmogorov-Smirnov test
                statistic, p_value = ks_2samp(
                    self.reference_data[column].dropna(),
                    current_data[column].dropna()
                )
                
                drift_results[column] = {
                    'statistic': statistic,
                    'p_value': p_value,
                    'drift_detected': p_value < self.threshold
                }
        
        return drift_results
    
    def calculate_drift_score(self, current_data):
        """Calculate overall drift score"""
        
        drift_results = self.detect_drift(current_data)
        
        # Weighted drift score
        total_drift = sum([
            result['statistic'] for result in drift_results.values()
        ])
        
        return total_drift / len(drift_results)
```

## 5. Scalable ML Infrastructure

### Distributed Training
```python
# Spark MLlib for distributed training
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml import Pipeline

def distributed_ml_training():
    """Distributed ML training with Spark"""
    
    spark = SparkSession.builder.appName("DistributedML").getOrCreate()
    
    # Load large dataset
    df = spark.read.parquet("hdfs://large_dataset.parquet")
    
    # Feature preparation
    feature_cols = ['feature1', 'feature2', 'feature3']
    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
    
    # ML model
    rf = RandomForestClassifier(featuresCol="features", labelCol="label")
    
    # Pipeline
    pipeline = Pipeline(stages=[assembler, rf])
    
    # Distributed training
    model = pipeline.fit(df)
    
    return model

# Model serving at scale
def scalable_model_serving():
    """Scalable model serving architecture"""
    
    from flask import Flask, request, jsonify
    import redis
    
    app = Flask(__name__)
    redis_client = redis.Redis(host='redis-cluster')
    
    @app.route('/predict', methods=['POST'])
    def predict():
        # Get features
        features = request.json['features']
        
        # Check cache first
        cache_key = f"prediction:{hash(str(features))}"
        cached_result = redis_client.get(cache_key)
        
        if cached_result:
            return jsonify(json.loads(cached_result))
        
        # Load model (with caching)
        model = load_model_with_cache()
        prediction = model.predict([features])[0]
        
        result = {'prediction': prediction}
        
        # Cache result
        redis_client.setex(cache_key, 3600, json.dumps(result))
        
        return jsonify(result)
    
    return app
```

## 6. ML Monitoring and Observability

### Model Performance Monitoring
```python
import logging
from datetime import datetime

class MLModelMonitor:
    """Monitor ML model performance in production"""
    
    def __init__(self, model_name, alert_thresholds):
        self.model_name = model_name
        self.thresholds = alert_thresholds
        self.metrics_history = []
    
    def log_prediction(self, features, prediction, actual=None, metadata=None):
        """Log individual prediction for monitoring"""
        
        log_entry = {
            'timestamp': datetime.now(),
            'model_name': self.model_name,
            'features': features,
            'prediction': prediction,
            'actual': actual,
            'metadata': metadata or {}
        }
        
        # Store in time-series database
        self._store_prediction_log(log_entry)
        
        # Real-time monitoring
        if actual is not None:
            self._update_performance_metrics(prediction, actual)
    
    def _update_performance_metrics(self, prediction, actual):
        """Update real-time performance metrics"""
        
        # Calculate accuracy for recent predictions
        recent_predictions = self._get_recent_predictions(hours=1)
        
        if len(recent_predictions) >= 100:  # Minimum sample size
            accuracy = sum([
                1 for p in recent_predictions 
                if abs(p['prediction'] - p['actual']) < 0.1
            ]) / len(recent_predictions)
            
            # Check for performance degradation
            if accuracy < self.thresholds['accuracy']:
                self._trigger_alert('accuracy_degradation', accuracy)
    
    def _trigger_alert(self, alert_type, value):
        """Trigger alert for model issues"""
        
        alert_message = f"Model {self.model_name}: {alert_type} = {value}"
        logging.warning(alert_message)
        
        # Send to monitoring system
        # send_to_slack(alert_message)
        # send_to_pagerduty(alert_message)
```

This focused addition provides data engineering-specific ML fundamentals while complementing the existing comprehensive ML content. The emphasis is on production systems, scalability, and integration with data engineering workflows.