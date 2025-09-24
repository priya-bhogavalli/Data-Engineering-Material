# 🔥 Quick Examples Index - Interview Prep

> **Last-minute interview preparation with executable code snippets**

## 🎯 **Most Asked Interview Topics (2024)**

### 🐍 **Python Essentials** (5 minutes)
```python
# Data manipulation
import pandas as pd
df = pd.read_csv('data.csv')
df.groupby('category').agg({'sales': 'sum'})

# List comprehension
result = [x**2 for x in range(10) if x % 2 == 0]

# Error handling
try:
    result = 10 / 0
except ZeroDivisionError:
    result = None
```

### 📊 **SQL Quick Wins** (10 minutes)
```sql
-- Window functions
SELECT name, salary, 
       ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) as rank
FROM employees;

-- CTEs
WITH sales_summary AS (
    SELECT region, SUM(amount) as total
    FROM sales GROUP BY region
)
SELECT * FROM sales_summary WHERE total > 10000;

-- Joins
SELECT e.name, d.department_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id;
```

### ⚡ **Spark/PySpark** (15 minutes)
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg

spark = SparkSession.builder.appName("QuickExample").getOrCreate()

# Read data
df = spark.read.parquet("data.parquet")

# Transformations
result = df.groupBy("category").agg(
    sum("amount").alias("total"),
    avg("amount").alias("average")
).filter(col("total") > 1000)

# Write result
result.write.mode("overwrite").parquet("output/")
```

### ☁️ **AWS Services** (10 minutes)
```python
import boto3

# S3
s3 = boto3.client('s3')
s3.upload_file('local_file.csv', 'my-bucket', 'data/file.csv')

# Lambda function
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

# Glue job structure
job = glue.create_job(
    Name='etl-job',
    Role='GlueServiceRole',
    Command={'Name': 'glueetl', 'ScriptLocation': 's3://bucket/script.py'}
)
```

### 🌊 **Kafka Streaming** (10 minutes)
```python
from kafka import KafkaProducer, KafkaConsumer
import json

# Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)
producer.send('my-topic', {'key': 'value'})

# Consumer
consumer = KafkaConsumer(
    'my-topic',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)
for message in consumer:
    print(message.value)
```

### 🤖 **MLflow Tracking** (10 minutes)
```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Start MLflow run
with mlflow.start_run():
    # Train model
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    
    # Log parameters and metrics
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("accuracy", accuracy_score(y_test, model.predict(X_test)))
    
    # Log model
    mlflow.sklearn.log_model(model, "random_forest_model")
```

### 🏪 **Feature Store** (15 minutes)
```python
# Feast Feature Store
from feast import FeatureStore

store = FeatureStore(repo_path=".")

# Get features for training
training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "user_stats:avg_daily_trips",
        "driver_stats:conv_rate"
    ]
).to_df()

# Get features for inference
feature_vector = store.get_online_features(
    features=["user_stats:avg_daily_trips"],
    entity_rows=[{"user_id": 1001}]
).to_dict()
```

### 🔄 **MLOps Pipeline** (15 minutes)
```python
# Model deployment with MLflow
import mlflow.pyfunc

# Load model
model = mlflow.pyfunc.load_model("models:/my_model/Production")

# Batch prediction
predictions = model.predict(batch_data)

# Model monitoring
def monitor_model_drift():
    current_accuracy = evaluate_model(model, test_data)
    if current_accuracy < 0.85:
        trigger_retraining()
        
# CI/CD for ML
def ml_pipeline():
    # Data validation
    validate_data_quality(new_data)
    
    # Model training
    new_model = train_model(new_data)
    
    # Model validation
    if validate_model(new_model):
        promote_to_production(new_model)
```

## 🚀 **System Design Patterns** (20 minutes)

### Lambda Architecture
```
Raw Data → Batch Layer (Hadoop/Spark) → Batch Views
         → Speed Layer (Storm/Flink) → Real-time Views
         → Serving Layer (HBase/Cassandra) → Query Interface
```

### ETL Pipeline
```python
def etl_pipeline():
    # Extract
    raw_data = extract_from_source()
    
    # Transform
    cleaned_data = clean_data(raw_data)
    enriched_data = enrich_data(cleaned_data)
    
    # Load
    load_to_warehouse(enriched_data)
    
    return "Pipeline completed"
```

## 📋 **Interview Cheat Sheet**

### **Data Engineering Fundamentals**
- **CAP Theorem**: Consistency, Availability, Partition tolerance (pick 2)
- **ACID**: Atomicity, Consistency, Isolation, Durability
- **Data Lake vs Warehouse**: Schema-on-read vs Schema-on-write
- **Batch vs Stream**: Latency vs Throughput trade-offs

### **Performance Optimization**
- **Spark**: Partitioning, caching, broadcast variables
- **SQL**: Indexing, query optimization, execution plans
- **Storage**: Columnar formats (Parquet), compression
- **MLOps**: Model versioning, A/B testing, feature monitoring

### **Common Architectures**
- **Medallion**: Bronze (raw) → Silver (cleaned) → Gold (aggregated)
- **Microservices**: Independent, scalable, fault-tolerant
- **Event-driven**: Pub/Sub, message queues, event sourcing
- **ML Pipeline**: Data → Features → Training → Validation → Deployment → Monitoring

## 🎯 **Quick Links to Deep Dive**
- [Python Interview Questions](./Core-Data-Engineering/Programming-Languages/Python/PYTHON_INTERVIEW_QUESTIONS.md)
- [SQL Interview Questions](./Core-Data-Engineering/Programming-Languages/SQL/SQL_INTERVIEW_QUESTIONS.md)
- [Spark Complete Guide](./Core-Data-Engineering/Data-Processing/Apache-Spark/SPARK_INTERVIEW_QUESTIONS_COMPLETE.md)
- [AWS Services Reference](./Core-Data-Engineering/Cloud/AWS/AWS_ALL_SERVICES_REFERENCE.md)
- [MLOps Guide](./Supporting-Tools/AI/MLOps/MLOPS_KEY_CONCEPTS.md)
- [Feature Stores](./Emerging-Technologies/Feature-Stores/)
- [System Design Patterns](./Supporting-Tools/Systems/System-Design/SYSTEM_DESIGN_INTERVIEW_QUESTIONS.md)