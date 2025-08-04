# AI Quick Reference for Data Engineering

## Machine Learning Basics

### Scikit-learn Common Operations
```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Data splitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Prediction
predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)

# Evaluation
accuracy = accuracy_score(y_test, predictions)
report = classification_report(y_test, predictions)
```

### Anomaly Detection
```python
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Prepare data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Anomaly detection
detector = IsolationForest(contamination=0.1, random_state=42)
detector.fit(X_scaled)

# Detect anomalies
anomalies = detector.predict(X_scaled)  # -1 = anomaly, 1 = normal
anomaly_scores = detector.decision_function(X_scaled)
```

## MLflow Operations

### Model Tracking
```python
import mlflow
import mlflow.sklearn

# Start experiment
mlflow.set_experiment("data_quality_models")

with mlflow.start_run():
    # Log parameters
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 10)
    
    # Log metrics
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("f1_score", 0.92)
    
    # Log model
    mlflow.sklearn.log_model(model, "model")
    
    # Log artifacts
    mlflow.log_artifact("feature_importance.png")
```

### Model Registry
```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Register model
mlflow.sklearn.log_model(
    model, 
    "model",
    registered_model_name="data_quality_classifier"
)

# Promote to production
client.transition_model_version_stage(
    name="data_quality_classifier",
    version="1",
    stage="Production"
)

# Load production model
model = mlflow.sklearn.load_model("models:/data_quality_classifier/Production")
```

## OpenAI API Usage

### Basic Chat Completion
```python
import openai

openai.api_key = "your-api-key"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a data engineering expert."},
        {"role": "user", "content": "How do I optimize Spark performance?"}
    ],
    max_tokens=500,
    temperature=0.3
)

answer = response.choices[0].message.content
```

### Function Calling
```python
functions = [
    {
        "name": "generate_sql",
        "description": "Generate SQL query from description",
        "parameters": {
            "type": "object",
            "properties": {
                "description": {"type": "string"},
                "tables": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["description"]
        }
    }
]

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Create a query to find top customers"}],
    functions=functions,
    function_call="auto"
)
```

## Vector Databases

### FAISS Operations
```python
import faiss
import numpy as np

# Create index
dimension = 384
index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity

# Add vectors
vectors = np.random.random((1000, dimension)).astype('float32')
faiss.normalize_L2(vectors)  # Normalize for cosine similarity
index.add(vectors)

# Search
query = np.random.random((1, dimension)).astype('float32')
faiss.normalize_L2(query)
scores, indices = index.search(query, k=5)
```

### Sentence Transformers
```python
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings
texts = ["Data pipeline", "ETL process", "Machine learning"]
embeddings = model.encode(texts)

# Calculate similarity
from sklearn.metrics.pairwise import cosine_similarity
similarity_matrix = cosine_similarity(embeddings)
```

## Data Quality with ML

### Feature Extraction for Quality
```python
def extract_quality_features(df):
    """Extract features for data quality prediction."""
    features = {
        'row_count': len(df),
        'column_count': len(df.columns),
        'null_percentage': df.isnull().sum().sum() / (len(df) * len(df.columns)),
        'duplicate_percentage': df.duplicated().sum() / len(df),
        'numeric_ratio': len(df.select_dtypes(include=['number']).columns) / len(df.columns),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024
    }
    return pd.DataFrame([features])
```

### Quality Scoring
```python
def calculate_quality_score(df):
    """Calculate data quality score (0-100)."""
    null_penalty = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 50
    duplicate_penalty = (df.duplicated().sum() / len(df)) * 30
    
    base_score = 100
    quality_score = max(0, base_score - null_penalty - duplicate_penalty)
    
    return quality_score
```

## Streaming ML

### Real-time Prediction
```python
from kafka import KafkaConsumer
import json
import joblib

# Load model
model = joblib.load('quality_model.pkl')

# Kafka consumer
consumer = KafkaConsumer(
    'data-stream',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    # Extract features
    features = extract_features(message.value)
    
    # Predict
    quality_score = model.predict_proba([features])[0][1]
    
    if quality_score < 0.8:
        send_alert(message.value, quality_score)
```

## Model Monitoring

### Performance Tracking
```python
from datetime import datetime
import pandas as pd

def monitor_model_performance(model, X_test, y_test):
    """Monitor model performance over time."""
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    # Log metrics
    metrics = {
        'timestamp': datetime.now(),
        'accuracy': accuracy,
        'sample_size': len(X_test),
        'model_version': get_model_version()
    }
    
    # Store in monitoring database
    save_metrics(metrics)
    
    # Check for drift
    if accuracy < 0.8:  # Threshold
        trigger_retraining_alert()
    
    return metrics
```

### Data Drift Detection
```python
from scipy import stats

def detect_data_drift(reference_data, current_data, threshold=0.05):
    """Detect data drift using statistical tests."""
    drift_results = {}
    
    for column in reference_data.columns:
        if reference_data[column].dtype in ['int64', 'float64']:
            # KS test for numerical data
            statistic, p_value = stats.ks_2samp(
                reference_data[column].dropna(),
                current_data[column].dropna()
            )
        else:
            # Chi-square test for categorical data
            ref_counts = reference_data[column].value_counts()
            curr_counts = current_data[column].value_counts()
            
            # Align categories
            all_categories = set(ref_counts.index) | set(curr_counts.index)
            ref_aligned = [ref_counts.get(cat, 0) for cat in all_categories]
            curr_aligned = [curr_counts.get(cat, 0) for cat in all_categories]
            
            statistic, p_value = stats.chisquare(curr_aligned, ref_aligned)
        
        drift_results[column] = {
            'statistic': statistic,
            'p_value': p_value,
            'drift_detected': p_value < threshold
        }
    
    return drift_results
```

## Common Patterns

### ML Pipeline Template
```python
class MLPipeline:
    def __init__(self, model_name):
        self.model_name = model_name
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def train(self, X, y):
        """Train the pipeline."""
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model = RandomForestClassifier()
        self.model.fit(X_scaled, y)
        
        self.is_trained = True
    
    def predict(self, X):
        """Make predictions."""
        if not self.is_trained:
            raise ValueError("Pipeline must be trained first")
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def save(self, filepath):
        """Save pipeline."""
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'is_trained': self.is_trained
        }, filepath)
    
    def load(self, filepath):
        """Load pipeline."""
        data = joblib.load(filepath)
        self.model = data['model']
        self.scaler = data['scaler']
        self.is_trained = data['is_trained']
```

### Error Handling
```python
def safe_ml_prediction(model, data, fallback_value=None):
    """Make ML prediction with error handling."""
    try:
        prediction = model.predict(data)
        return prediction
    except Exception as e:
        print(f"ML prediction failed: {e}")
        if fallback_value is not None:
            return fallback_value
        else:
            # Use rule-based fallback
            return rule_based_prediction(data)

def rule_based_prediction(data):
    """Fallback rule-based prediction."""
    # Simple rule-based logic
    if data['null_percentage'] > 0.1:
        return 0  # Poor quality
    else:
        return 1  # Good quality
```

This quick reference provides essential commands and patterns for integrating AI capabilities into data engineering workflows.