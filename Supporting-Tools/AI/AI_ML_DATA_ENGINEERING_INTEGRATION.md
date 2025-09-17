# 🤖 AI/ML Integration with Data Engineering

## 🎯 **MLOps Pipeline for Data Engineers**

### **ML Model Training Pipeline**
```python
# src/ml_pipeline.py
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import joblib
from datetime import datetime

class MLPipeline:
    def __init__(self, experiment_name="data_quality_prediction"):
        mlflow.set_experiment(experiment_name)
        self.model = None
        
    def load_data(self, data_path):
        """Load and prepare data for training"""
        df = pd.read_csv(data_path)
        
        # Feature engineering
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
        
        # Select features and target
        features = ['record_count', 'null_percentage', 'duplicate_percentage', 
                   'hour', 'day_of_week']
        target = 'data_quality_score'
        
        X = df[features]
        y = df[target]
        
        return train_test_split(X, y, test_size=0.2, random_state=42)
    
    def train_model(self, X_train, y_train, X_test, y_test):
        """Train ML model with MLflow tracking"""
        with mlflow.start_run():
            # Model parameters
            params = {
                'n_estimators': 100,
                'max_depth': 10,
                'random_state': 42
            }
            
            # Train model
            self.model = RandomForestRegressor(**params)
            self.model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = self.model.predict(X_test)
            
            # Calculate metrics
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Log parameters and metrics
            mlflow.log_params(params)
            mlflow.log_metric("mse", mse)
            mlflow.log_metric("r2", r2)
            
            # Log model
            mlflow.sklearn.log_model(
                self.model, 
                "model",
                registered_model_name="data_quality_predictor"
            )
            
            print(f"Model trained - MSE: {mse:.4f}, R2: {r2:.4f}")
            
            return self.model
    
    def predict_data_quality(self, features):
        """Predict data quality score"""
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        return self.model.predict(features)

# Usage example
if __name__ == "__main__":
    pipeline = MLPipeline()
    X_train, X_test, y_train, y_test = pipeline.load_data("data/quality_metrics.csv")
    model = pipeline.train_model(X_train, y_train, X_test, y_test)
```

### **Real-time ML Inference Service**
```python
# src/ml_service.py
from flask import Flask, request, jsonify
import mlflow.pyfunc
import pandas as pd
import numpy as np
from datetime import datetime
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

class MLService:
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the latest model from MLflow"""
        try:
            model_name = "data_quality_predictor"
            stage = "Production"
            self.model = mlflow.pyfunc.load_model(f"models:/{model_name}/{stage}")
            logging.info(f"Loaded model {model_name} from {stage} stage")
        except Exception as e:
            logging.error(f"Failed to load model: {e}")
    
    def preprocess_features(self, data):
        """Preprocess input data for prediction"""
        df = pd.DataFrame([data])
        
        # Add time-based features
        now = datetime.now()
        df['hour'] = now.hour
        df['day_of_week'] = now.weekday()
        
        # Select required features
        features = ['record_count', 'null_percentage', 'duplicate_percentage', 
                   'hour', 'day_of_week']
        
        return df[features]
    
    def predict(self, data):
        """Make prediction"""
        if self.model is None:
            raise ValueError("Model not loaded")
        
        features = self.preprocess_features(data)
        prediction = self.model.predict(features)
        
        return {
            'data_quality_score': float(prediction[0]),
            'prediction_time': datetime.now().isoformat(),
            'status': 'success'
        }

ml_service = MLService()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'model_loaded': ml_service.model is not None})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        result = ml_service.predict(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 400

@app.route('/reload_model', methods=['POST'])
def reload_model():
    try:
        ml_service.load_model()
        return jsonify({'status': 'model_reloaded'})
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
```

## 🔄 **Automated ML Pipeline with Airflow**

### **MLOps DAG**
```python
# dags/ml_pipeline_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.sensors.http import HttpSensor
from datetime import datetime, timedelta
import pandas as pd
import mlflow
import requests

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'ml_pipeline',
    default_args=default_args,
    description='ML Pipeline for Data Quality Prediction',
    schedule_interval='@daily',
    catchup=False,
    tags=['ml', 'data-quality']
)

def extract_data_quality_metrics(**context):
    """Extract data quality metrics from various sources"""
    # Connect to data warehouse
    from airflow.hooks.postgres_hook import PostgresHook
    
    pg_hook = PostgresHook(postgres_conn_id='data_warehouse')
    
    # Query data quality metrics
    sql = """
    SELECT 
        table_name,
        record_count,
        null_percentage,
        duplicate_percentage,
        completeness_score,
        timestamp
    FROM data_quality_metrics 
    WHERE DATE(timestamp) = CURRENT_DATE - INTERVAL '1 day'
    """
    
    df = pg_hook.get_pandas_df(sql)
    
    # Save to temporary location
    df.to_csv('/tmp/daily_metrics.csv', index=False)
    
    return '/tmp/daily_metrics.csv'

def train_model(**context):
    """Train ML model with new data"""
    import sys
    sys.path.append('/opt/airflow/dags/src')
    from ml_pipeline import MLPipeline
    
    # Load data
    data_path = context['task_instance'].xcom_pull(task_ids='extract_metrics')
    
    # Train model
    pipeline = MLPipeline(experiment_name="daily_training")
    X_train, X_test, y_train, y_test = pipeline.load_data(data_path)
    model = pipeline.train_model(X_train, y_train, X_test, y_test)
    
    # Get model metrics
    with mlflow.start_run():
        run_id = mlflow.active_run().info.run_id
    
    return run_id

def evaluate_model(**context):
    """Evaluate model performance and decide on deployment"""
    run_id = context['task_instance'].xcom_pull(task_ids='train_model')
    
    # Get model metrics from MLflow
    client = mlflow.tracking.MlflowClient()
    run = client.get_run(run_id)
    
    r2_score = float(run.data.metrics['r2'])
    mse = float(run.data.metrics['mse'])
    
    # Define thresholds
    R2_THRESHOLD = 0.8
    MSE_THRESHOLD = 0.1
    
    if r2_score >= R2_THRESHOLD and mse <= MSE_THRESHOLD:
        # Promote model to staging
        model_version = client.create_model_version(
            name="data_quality_predictor",
            source=f"runs:/{run_id}/model",
            run_id=run_id
        )
        
        client.transition_model_version_stage(
            name="data_quality_predictor",
            version=model_version.version,
            stage="Staging"
        )
        
        return "promote_to_staging"
    else:
        return "model_not_ready"

def deploy_model(**context):
    """Deploy model to production"""
    # Get latest staging model
    client = mlflow.tracking.MlflowClient()
    
    latest_versions = client.get_latest_versions(
        name="data_quality_predictor",
        stages=["Staging"]
    )
    
    if latest_versions:
        version = latest_versions[0].version
        
        # Transition to production
        client.transition_model_version_stage(
            name="data_quality_predictor",
            version=version,
            stage="Production"
        )
        
        # Trigger model reload in inference service
        response = requests.post('http://ml-service:8080/reload_model')
        
        if response.status_code == 200:
            print(f"Model version {version} deployed to production")
        else:
            raise Exception("Failed to reload model in inference service")

def send_alert(**context):
    """Send alert if model performance is poor"""
    # Implementation for sending alerts (Slack, email, etc.)
    print("Model performance below threshold - alert sent")

# Define tasks
extract_metrics = PythonOperator(
    task_id='extract_metrics',
    python_callable=extract_data_quality_metrics,
    dag=dag
)

train_model_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag
)

evaluate_model_task = PythonOperator(
    task_id='evaluate_model',
    python_callable=evaluate_model,
    dag=dag
)

deploy_model_task = PythonOperator(
    task_id='deploy_model',
    python_callable=deploy_model,
    dag=dag
)

send_alert_task = PythonOperator(
    task_id='send_alert',
    python_callable=send_alert,
    dag=dag,
    trigger_rule='one_failed'
)

# Check if ML service is healthy
health_check = HttpSensor(
    task_id='check_ml_service_health',
    http_conn_id='ml_service',
    endpoint='/health',
    timeout=20,
    poke_interval=5,
    dag=dag
)

# Define dependencies
extract_metrics >> train_model_task >> evaluate_model_task
evaluate_model_task >> deploy_model_task
evaluate_model_task >> send_alert_task
health_check >> deploy_model_task
```

## 🚀 **GenAI Integration for Data Engineering**

### **LLM-Powered Data Quality Assistant**
```python
# src/genai_assistant.py
import openai
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import pandas as pd
import json

class DataQualityAssistant:
    def __init__(self, api_key):
        self.llm = OpenAI(openai_api_key=api_key, temperature=0.1)
        
    def analyze_data_quality_issues(self, df, table_name):
        """Use LLM to analyze data quality issues"""
        
        # Generate data profile
        profile = {
            'table_name': table_name,
            'row_count': len(df),
            'column_count': len(df.columns),
            'null_counts': df.isnull().sum().to_dict(),
            'duplicate_count': df.duplicated().sum(),
            'data_types': df.dtypes.astype(str).to_dict(),
            'sample_data': df.head(3).to_dict()
        }
        
        prompt_template = PromptTemplate(
            input_variables=["data_profile"],
            template="""
            As a data quality expert, analyze the following data profile and provide insights:
            
            Data Profile:
            {data_profile}
            
            Please provide:
            1. Key data quality issues identified
            2. Severity level (High/Medium/Low) for each issue
            3. Recommended actions to fix each issue
            4. SQL queries or Python code to implement fixes
            5. Overall data quality score (0-100)
            
            Format your response as JSON with the following structure:
            {{
                "overall_score": <score>,
                "issues": [
                    {{
                        "issue": "<description>",
                        "severity": "<High/Medium/Low>",
                        "recommendation": "<action>",
                        "fix_code": "<sql or python code>"
                    }}
                ],
                "summary": "<overall assessment>"
            }}
            """
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        
        try:
            response = chain.run(data_profile=json.dumps(profile, indent=2))
            return json.loads(response)
        except Exception as e:
            return {
                "error": f"Failed to analyze data quality: {str(e)}",
                "overall_score": 0,
                "issues": [],
                "summary": "Analysis failed"
            }
    
    def generate_data_documentation(self, df, table_name):
        """Generate documentation for data tables"""
        
        prompt_template = PromptTemplate(
            input_variables=["table_info"],
            template="""
            Generate comprehensive documentation for the following data table:
            
            Table: {table_info}
            
            Create documentation including:
            1. Table description and purpose
            2. Column descriptions with business meaning
            3. Data lineage and source systems
            4. Data quality rules and constraints
            5. Usage examples and common queries
            
            Format as Markdown.
            """
        )
        
        table_info = {
            'name': table_name,
            'columns': list(df.columns),
            'data_types': df.dtypes.astype(str).to_dict(),
            'sample_values': {col: df[col].dropna().head(3).tolist() 
                            for col in df.columns}
        }
        
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        return chain.run(table_info=json.dumps(table_info, indent=2))

# Usage example
def analyze_table_quality():
    """Example usage of GenAI assistant"""
    # Load data
    df = pd.read_csv('data/customer_data.csv')
    
    # Initialize assistant
    assistant = DataQualityAssistant(api_key="your-openai-api-key")
    
    # Analyze data quality
    quality_report = assistant.analyze_data_quality_issues(df, 'customer_data')
    
    print("Data Quality Analysis:")
    print(f"Overall Score: {quality_report['overall_score']}/100")
    
    for issue in quality_report['issues']:
        print(f"\nIssue: {issue['issue']}")
        print(f"Severity: {issue['severity']}")
        print(f"Recommendation: {issue['recommendation']}")
        print(f"Fix Code: {issue['fix_code']}")
    
    # Generate documentation
    documentation = assistant.generate_data_documentation(df, 'customer_data')
    
    with open('docs/customer_data.md', 'w') as f:
        f.write(documentation)
    
    return quality_report

if __name__ == "__main__":
    report = analyze_table_quality()
```

### **Vector Database for Data Lineage**
```python
# src/vector_lineage.py
import chromadb
from sentence_transformers import SentenceTransformer
import pandas as pd
import json

class DataLineageVectorDB:
    def __init__(self, persist_directory="./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name="data_lineage",
            metadata={"hnsw:space": "cosine"}
        )
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
    
    def add_table_metadata(self, table_name, schema, description, source_systems):
        """Add table metadata to vector database"""
        
        # Create searchable text
        metadata_text = f"""
        Table: {table_name}
        Description: {description}
        Schema: {', '.join([f"{col}:{dtype}" for col, dtype in schema.items()])}
        Source Systems: {', '.join(source_systems)}
        """
        
        # Generate embedding
        embedding = self.encoder.encode(metadata_text).tolist()
        
        # Store in vector database
        self.collection.add(
            embeddings=[embedding],
            documents=[metadata_text],
            metadatas=[{
                "table_name": table_name,
                "description": description,
                "schema": json.dumps(schema),
                "source_systems": json.dumps(source_systems)
            }],
            ids=[f"table_{table_name}"]
        )
    
    def search_similar_tables(self, query, n_results=5):
        """Search for similar tables based on query"""
        
        # Generate query embedding
        query_embedding = self.encoder.encode(query).tolist()
        
        # Search vector database
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        return results
    
    def find_data_lineage(self, table_name):
        """Find data lineage for a specific table"""
        
        # Search for related tables
        query = f"tables related to {table_name} data flow dependencies"
        results = self.search_similar_tables(query)
        
        lineage = {
            "table": table_name,
            "upstream_tables": [],
            "downstream_tables": [],
            "related_tables": []
        }
        
        for i, metadata in enumerate(results['metadatas'][0]):
            if metadata['table_name'] != table_name:
                lineage["related_tables"].append({
                    "table_name": metadata['table_name'],
                    "description": metadata['description'],
                    "similarity_score": 1 - results['distances'][0][i]
                })
        
        return lineage

# Usage example
def setup_lineage_tracking():
    """Setup vector database for data lineage tracking"""
    
    lineage_db = DataLineageVectorDB()
    
    # Add sample table metadata
    tables_metadata = [
        {
            "table_name": "customer_orders",
            "schema": {"customer_id": "int", "order_date": "date", "amount": "decimal"},
            "description": "Customer order transactions with payment amounts",
            "source_systems": ["ecommerce_db", "payment_gateway"]
        },
        {
            "table_name": "customer_profiles",
            "schema": {"customer_id": "int", "name": "varchar", "email": "varchar"},
            "description": "Customer demographic and contact information",
            "source_systems": ["crm_system", "registration_api"]
        },
        {
            "table_name": "order_analytics",
            "schema": {"customer_id": "int", "total_orders": "int", "avg_amount": "decimal"},
            "description": "Aggregated customer order analytics and metrics",
            "source_systems": ["customer_orders", "data_warehouse"]
        }
    ]
    
    for table in tables_metadata:
        lineage_db.add_table_metadata(**table)
    
    # Search for related tables
    results = lineage_db.search_similar_tables("customer purchase behavior")
    
    print("Similar tables found:")
    for i, doc in enumerate(results['documents'][0]):
        print(f"\nTable {i+1}:")
        print(doc)
        print(f"Similarity: {1 - results['distances'][0][i]:.3f}")
    
    return lineage_db

if __name__ == "__main__":
    db = setup_lineage_tracking()
```

## 📊 **ML Model Monitoring Dashboard**

### **Model Performance Tracking**
```python
# src/model_monitoring.py
import streamlit as st
import mlflow
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

class ModelMonitoringDashboard:
    def __init__(self):
        self.client = mlflow.tracking.MlflowClient()
    
    def get_model_metrics(self, model_name, days=30):
        """Get model performance metrics over time"""
        
        # Get model versions
        versions = self.client.get_latest_versions(model_name, stages=["Production"])
        
        if not versions:
            return pd.DataFrame()
        
        # Get experiment runs
        experiment = self.client.get_experiment_by_name("model_monitoring")
        runs = self.client.search_runs(
            experiment_ids=[experiment.experiment_id],
            filter_string=f"tags.model_name = '{model_name}'",
            order_by=["start_time DESC"],
            max_results=100
        )
        
        metrics_data = []
        for run in runs:
            metrics_data.append({
                'timestamp': datetime.fromtimestamp(run.info.start_time / 1000),
                'accuracy': run.data.metrics.get('accuracy', 0),
                'precision': run.data.metrics.get('precision', 0),
                'recall': run.data.metrics.get('recall', 0),
                'f1_score': run.data.metrics.get('f1_score', 0),
                'data_drift': run.data.metrics.get('data_drift', 0),
                'prediction_count': run.data.metrics.get('prediction_count', 0)
            })
        
        return pd.DataFrame(metrics_data)
    
    def create_dashboard(self):
        """Create Streamlit dashboard"""
        
        st.title("🤖 ML Model Monitoring Dashboard")
        
        # Sidebar
        st.sidebar.header("Configuration")
        model_name = st.sidebar.selectbox(
            "Select Model",
            ["data_quality_predictor", "customer_churn_model", "fraud_detection_model"]
        )
        
        days = st.sidebar.slider("Days to Display", 1, 90, 30)
        
        # Get data
        df = self.get_model_metrics(model_name, days)
        
        if df.empty:
            st.warning("No data available for selected model")
            return
        
        # Metrics overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Current Accuracy",
                f"{df['accuracy'].iloc[0]:.3f}",
                f"{df['accuracy'].iloc[0] - df['accuracy'].iloc[1]:.3f}" if len(df) > 1 else None
            )
        
        with col2:
            st.metric(
                "Predictions Today",
                f"{df['prediction_count'].iloc[0]:,.0f}",
                f"{df['prediction_count'].iloc[0] - df['prediction_count'].iloc[1]:,.0f}" if len(df) > 1 else None
            )
        
        with col3:
            st.metric(
                "Data Drift Score",
                f"{df['data_drift'].iloc[0]:.3f}",
                f"{df['data_drift'].iloc[0] - df['data_drift'].iloc[1]:.3f}" if len(df) > 1 else None
            )
        
        with col4:
            avg_f1 = df['f1_score'].mean()
            st.metric("Avg F1 Score", f"{avg_f1:.3f}")
        
        # Performance trends
        st.subheader("📈 Performance Trends")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['accuracy'],
            mode='lines+markers',
            name='Accuracy',
            line=dict(color='blue')
        ))
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['precision'],
            mode='lines+markers',
            name='Precision',
            line=dict(color='green')
        ))
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['recall'],
            mode='lines+markers',
            name='Recall',
            line=dict(color='red')
        ))
        
        fig.update_layout(
            title="Model Performance Over Time",
            xaxis_title="Date",
            yaxis_title="Score",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Data drift monitoring
        st.subheader("🔍 Data Drift Monitoring")
        
        drift_fig = px.line(
            df,
            x='timestamp',
            y='data_drift',
            title='Data Drift Score Over Time'
        )
        drift_fig.add_hline(
            y=0.1,
            line_dash="dash",
            line_color="red",
            annotation_text="Drift Threshold"
        )
        
        st.plotly_chart(drift_fig, use_container_width=True)
        
        # Prediction volume
        st.subheader("📊 Prediction Volume")
        
        volume_fig = px.bar(
            df,
            x='timestamp',
            y='prediction_count',
            title='Daily Prediction Count'
        )
        
        st.plotly_chart(volume_fig, use_container_width=True)
        
        # Alerts
        st.subheader("🚨 Alerts")
        
        # Check for alerts
        latest_accuracy = df['accuracy'].iloc[0]
        latest_drift = df['data_drift'].iloc[0]
        
        if latest_accuracy < 0.8:
            st.error(f"⚠️ Model accuracy dropped to {latest_accuracy:.3f} (below 0.8 threshold)")
        
        if latest_drift > 0.1:
            st.error(f"⚠️ Data drift detected: {latest_drift:.3f} (above 0.1 threshold)")
        
        if latest_accuracy >= 0.8 and latest_drift <= 0.1:
            st.success("✅ All model metrics are within acceptable ranges")

# Run dashboard
if __name__ == "__main__":
    dashboard = ModelMonitoringDashboard()
    dashboard.create_dashboard()
```

## 🔧 **Quick Setup Commands**

### **MLflow Setup**
```bash
# Start MLflow server
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 0.0.0.0 --port 5000

# Set tracking URI
export MLFLOW_TRACKING_URI=http://localhost:5000
```

### **Docker Compose for ML Stack**
```yaml
# docker-compose.ml.yml
version: '3.8'

services:
  mlflow:
    image: python:3.9-slim
    command: >
      bash -c "pip install mlflow psycopg2-binary &&
               mlflow server --backend-store-uri postgresql://mlflow:password@postgres:5432/mlflow
               --default-artifact-root s3://mlflow-artifacts --host 0.0.0.0 --port 5000"
    ports:
      - "5000:5000"
    environment:
      AWS_ACCESS_KEY_ID: ${AWS_ACCESS_KEY_ID}
      AWS_SECRET_ACCESS_KEY: ${AWS_SECRET_ACCESS_KEY}
    depends_on:
      - postgres

  ml-service:
    build: .
    ports:
      - "8080:8080"
    environment:
      MLFLOW_TRACKING_URI: http://mlflow:5000
    depends_on:
      - mlflow

  jupyter:
    image: jupyter/datascience-notebook
    ports:
      - "8888:8888"
    volumes:
      - ./notebooks:/home/jovyan/work
      - ./data:/home/jovyan/data
    environment:
      MLFLOW_TRACKING_URI: http://mlflow:5000

  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: mlflow
      POSTGRES_USER: mlflow
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

*Updated: December 2024 | Focus: Production MLOps | Integration: Complete data engineering stack*