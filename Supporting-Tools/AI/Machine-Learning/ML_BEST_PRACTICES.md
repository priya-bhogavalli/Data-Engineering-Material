# Machine Learning Best Practices for Data Engineering

## Data Pipeline for ML

### Feature Engineering Pipeline
```python
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

class FeatureEngineeringPipeline:
    def __init__(self):
        self.numeric_features = ['age', 'income', 'credit_score']
        self.categorical_features = ['gender', 'education', 'employment']
        
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), self.numeric_features),
                ('cat', LabelEncoder(), self.categorical_features)
            ]
        )
    
    def fit_transform(self, df):
        return self.preprocessor.fit_transform(df)
    
    def transform(self, df):
        return self.preprocessor.transform(df)
```

### Data Validation
```python
import great_expectations as ge

def validate_training_data(df):
    expectation_suite = ge.core.ExpectationSuite(
        expectation_suite_name="training_data_validation"
    )
    
    df_ge = ge.from_pandas(df, expectation_suite=expectation_suite)
    
    # Validate data types and ranges
    df_ge.expect_column_to_exist("customer_id")
    df_ge.expect_column_values_to_not_be_null("customer_id")
    df_ge.expect_column_values_to_be_between("age", 18, 100)
    df_ge.expect_column_values_to_be_in_set("gender", ["M", "F"])
    
    return df_ge.validate()
```

## Model Training Pipeline

### Training Infrastructure
```python
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score

class ModelTrainingPipeline:
    def __init__(self, experiment_name):
        mlflow.set_experiment(experiment_name)
        
    def train_model(self, X, y, model_params=None):
        with mlflow.start_run():
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            model = RandomForestClassifier(**(model_params or {}))
            model.fit(X_train, y_train)
            
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted')
            recall = recall_score(y_test, y_pred, average='weighted')
            
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("recall", recall)
            mlflow.sklearn.log_model(model, "model")
            
            return model, {"accuracy": accuracy, "precision": precision, "recall": recall}
```

## Model Deployment

### Model Serving
```python
import joblib
from flask import Flask, request, jsonify

app = Flask(__name__)
model = joblib.load('model.pkl')
preprocessor = joblib.load('preprocessor.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        features = preprocessor.transform([data['features']])
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0].max()
        
        return jsonify({
            'prediction': int(prediction),
            'probability': float(probability),
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

## Model Monitoring

### Data Drift Detection
```python
from scipy import stats
import numpy as np

class DataDriftDetector:
    def __init__(self, reference_data):
        self.reference_data = reference_data
    
    def detect_drift(self, new_data, threshold=0.05):
        drift_detected = {}
        
        for i in range(new_data.shape[1]):
            ks_stat, p_value = stats.ks_2samp(
                self.reference_data[:, i],
                new_data[:, i]
            )
            
            drift_detected[f'feature_{i}'] = {
                'ks_statistic': ks_stat,
                'p_value': p_value,
                'drift_detected': p_value < threshold
            }
        
        return drift_detected
```

### Model Performance Monitoring
```python
import mlflow
from datetime import datetime

class ModelPerformanceMonitor:
    def __init__(self, model_name, stage="Production"):
        self.model_name = model_name
        self.stage = stage
        
    def calculate_performance_metrics(self, y_true, y_pred):
        return {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted'),
            'recall': recall_score(y_true, y_pred, average='weighted'),
            'timestamp': datetime.now()
        }
    
    def check_performance_degradation(self, current_metrics, baseline_metrics, threshold=0.05):
        degradation_alerts = {}
        
        for metric in ['accuracy', 'precision', 'recall']:
            current_value = current_metrics[metric]
            baseline_value = baseline_metrics[metric]
            
            degradation = (baseline_value - current_value) / baseline_value
            
            if degradation > threshold:
                degradation_alerts[metric] = {
                    'current_value': current_value,
                    'baseline_value': baseline_value,
                    'degradation_percentage': degradation * 100,
                    'alert': True
                }
        
        return degradation_alerts
```