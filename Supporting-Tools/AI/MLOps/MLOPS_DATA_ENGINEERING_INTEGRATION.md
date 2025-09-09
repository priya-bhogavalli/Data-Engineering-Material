# MLOps Data Engineering Integration

## 1. ML Pipeline Orchestration

### Airflow ML Workflows
```python
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

def create_ml_pipeline_dag():
    """Complete ML pipeline orchestration with Airflow"""
    
    default_args = {
        'owner': 'ml-team',
        'depends_on_past': False,
        'start_date': datetime(2024, 1, 1),
        'email_on_failure': True,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5)
    }
    
    dag = DAG(
        'ml_training_pipeline',
        default_args=default_args,
        description='End-to-end ML training pipeline',
        schedule_interval='@daily',
        catchup=False
    )
    
    # Data extraction
    extract_data = PythonOperator(
        task_id='extract_data',
        python_callable=extract_training_data,
        dag=dag
    )
    
    # Data validation
    validate_data = PythonOperator(
        task_id='validate_data',
        python_callable=validate_data_quality,
        dag=dag
    )
    
    # Feature engineering
    create_features = PythonOperator(
        task_id='create_features',
        python_callable=engineer_features,
        dag=dag
    )
    
    # Model training
    train_model = PythonOperator(
        task_id='train_model',
        python_callable=train_ml_model,
        dag=dag
    )
    
    # Model validation
    validate_model = PythonOperator(
        task_id='validate_model',
        python_callable=validate_model_performance,
        dag=dag
    )
    
    # Model deployment
    deploy_model = PythonOperator(
        task_id='deploy_model',
        python_callable=deploy_to_staging,
        dag=dag
    )
    
    # Set dependencies
    extract_data >> validate_data >> create_features >> train_model >> validate_model >> deploy_model
    
    return dag

def extract_training_data(**context):
    """Extract data for ML training"""
    import pandas as pd
    from sqlalchemy import create_engine
    
    # Extract from data warehouse
    engine = create_engine('postgresql://user:pass@warehouse:5432/db')
    
    query = """
    SELECT 
        customer_id,
        feature1, feature2, feature3,
        target_variable,
        created_at
    FROM ml_training_view 
    WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
    """
    
    df = pd.read_sql(query, engine)
    
    # Store for next task
    df.to_parquet('/tmp/training_data.parquet')
    
    return f"Extracted {len(df)} records"

def validate_data_quality(**context):
    """Validate data quality for ML"""
    import pandas as pd
    import great_expectations as ge
    
    df = pd.read_parquet('/tmp/training_data.parquet')
    
    # Great Expectations validation
    gdf = ge.from_pandas(df)
    
    # Data quality checks
    assert gdf.expect_column_values_to_not_be_null('customer_id').success
    assert gdf.expect_column_values_to_be_between('feature1', 0, 100).success
    assert gdf.expect_table_row_count_to_be_between(1000, 1000000).success
    
    return "Data validation passed"
```

### DBT for ML Feature Engineering
```sql
-- models/ml_features/customer_features.sql
{{ config(materialized='table') }}

WITH customer_base AS (
    SELECT 
        customer_id,
        registration_date,
        customer_segment
    FROM {{ ref('dim_customers') }}
),

transaction_features AS (
    SELECT 
        customer_id,
        COUNT(*) as transaction_count,
        AVG(amount) as avg_transaction_amount,
        STDDEV(amount) as transaction_amount_std,
        MAX(transaction_date) as last_transaction_date,
        MIN(transaction_date) as first_transaction_date
    FROM {{ ref('fact_transactions') }}
    WHERE transaction_date >= CURRENT_DATE - INTERVAL '90 days'
    GROUP BY customer_id
),

behavioral_features AS (
    SELECT 
        customer_id,
        COUNT(DISTINCT DATE(event_timestamp)) as active_days,
        COUNT(*) as total_events,
        COUNT(DISTINCT event_type) as unique_event_types
    FROM {{ ref('fact_customer_events') }}
    WHERE event_timestamp >= CURRENT_DATE - INTERVAL '90 days'
    GROUP BY customer_id
)

SELECT 
    cb.customer_id,
    cb.customer_segment,
    EXTRACT(DAYS FROM CURRENT_DATE - cb.registration_date) as days_since_registration,
    
    -- Transaction features
    COALESCE(tf.transaction_count, 0) as transaction_count,
    COALESCE(tf.avg_transaction_amount, 0) as avg_transaction_amount,
    COALESCE(tf.transaction_amount_std, 0) as transaction_amount_std,
    EXTRACT(DAYS FROM CURRENT_DATE - tf.last_transaction_date) as days_since_last_transaction,
    
    -- Behavioral features
    COALESCE(bf.active_days, 0) as active_days_90d,
    COALESCE(bf.total_events, 0) as total_events_90d,
    COALESCE(bf.unique_event_types, 0) as unique_event_types_90d,
    
    -- Derived features
    CASE 
        WHEN tf.transaction_count > 0 
        THEN tf.avg_transaction_amount * tf.transaction_count 
        ELSE 0 
    END as total_transaction_value,
    
    CASE 
        WHEN bf.active_days > 0 
        THEN bf.total_events::FLOAT / bf.active_days 
        ELSE 0 
    END as avg_events_per_active_day

FROM customer_base cb
LEFT JOIN transaction_features tf ON cb.customer_id = tf.customer_id
LEFT JOIN behavioral_features bf ON cb.customer_id = bf.customer_id
```

## 2. Real-time ML Infrastructure

### Kafka + ML Streaming
```python
from kafka import KafkaConsumer, KafkaProducer
import json
import joblib
import numpy as np
from datetime import datetime

class RealTimeMLProcessor:
    """Real-time ML inference with Kafka"""
    
    def __init__(self, model_path, kafka_config):
        self.model = joblib.load(model_path)
        self.consumer = KafkaConsumer(
            'raw_events',
            bootstrap_servers=kafka_config['servers'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_config['servers'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        
        # Feature cache for real-time enrichment
        self.feature_cache = {}
    
    def process_events(self):
        """Process streaming events for real-time ML"""
        
        for message in self.consumer:
            try:
                event = message.value
                
                # Extract features
                features = self.extract_features(event)
                
                # Make prediction
                prediction = self.model.predict([features])[0]
                probability = self.model.predict_proba([features])[0].max()
                
                # Create result
                result = {
                    'event_id': event['id'],
                    'customer_id': event['customer_id'],
                    'prediction': float(prediction),
                    'probability': float(probability),
                    'timestamp': datetime.now().isoformat(),
                    'model_version': self.model.metadata.get('version', 'unknown')
                }
                
                # Send to output topic
                self.producer.send('ml_predictions', result)
                
                # Trigger actions if needed
                if probability > 0.8:
                    self.trigger_high_confidence_action(result)
                    
            except Exception as e:
                self.handle_processing_error(message, e)
    
    def extract_features(self, event):
        """Extract features from raw event"""
        
        customer_id = event['customer_id']
        
        # Get cached features or compute
        if customer_id not in self.feature_cache:
            self.feature_cache[customer_id] = self.compute_customer_features(customer_id)
        
        # Combine event features with cached features
        features = [
            event.get('amount', 0),
            event.get('merchant_category', 0),
            len(event.get('description', '')),
            self.feature_cache[customer_id]['avg_transaction_amount'],
            self.feature_cache[customer_id]['transaction_count_30d']
        ]
        
        return features
    
    def compute_customer_features(self, customer_id):
        """Compute customer features from feature store"""
        
        # In production, this would query a feature store
        # For demo, return mock features
        return {
            'avg_transaction_amount': np.random.normal(50, 20),
            'transaction_count_30d': np.random.poisson(10)
        }
```

### Feature Store Integration
```python
import redis
import json
from datetime import datetime, timedelta

class ProductionFeatureStore:
    """Production-ready feature store"""
    
    def __init__(self, redis_config, batch_storage_config):
        self.redis_client = redis.Redis(**redis_config)
        self.batch_storage = batch_storage_config
        
    def get_online_features(self, feature_names, entity_ids):
        """Get features for online serving"""
        
        results = {}
        
        for entity_id in entity_ids:
            entity_features = {}
            
            for feature_name in feature_names:
                cache_key = f"feature:{feature_name}:{entity_id}"
                cached_value = self.redis_client.get(cache_key)
                
                if cached_value:
                    entity_features[feature_name] = json.loads(cached_value)
                else:
                    # Fallback to batch computation
                    value = self.compute_feature_fallback(feature_name, entity_id)
                    entity_features[feature_name] = value
                    
                    # Cache for future use
                    self.redis_client.setex(
                        cache_key, 
                        timedelta(hours=1).total_seconds(), 
                        json.dumps(value)
                    )
            
            results[entity_id] = entity_features
        
        return results
    
    def update_online_features(self, feature_updates):
        """Update online features from batch processing"""
        
        pipeline = self.redis_client.pipeline()
        
        for entity_id, features in feature_updates.items():
            for feature_name, value in features.items():
                cache_key = f"feature:{feature_name}:{entity_id}"
                pipeline.setex(
                    cache_key,
                    timedelta(hours=24).total_seconds(),
                    json.dumps(value)
                )
        
        pipeline.execute()
    
    def get_training_features(self, feature_names, entity_ids, timestamp_range):
        """Get historical features for training"""
        
        # Query batch storage for historical features
        query = f"""
        SELECT entity_id, feature_name, feature_value, timestamp
        FROM feature_store.features
        WHERE entity_id IN ({','.join(map(str, entity_ids))})
        AND feature_name IN ({','.join([f"'{f}'" for f in feature_names])})
        AND timestamp BETWEEN '{timestamp_range[0]}' AND '{timestamp_range[1]}'
        ORDER BY entity_id, timestamp
        """
        
        # Execute query and return structured data
        return self.execute_batch_query(query)
```

## 3. Model Deployment Patterns

### Blue-Green Deployment for ML
```python
import docker
import time
from typing import Dict, Any

class MLModelDeploymentManager:
    """Manage blue-green deployments for ML models"""
    
    def __init__(self, docker_client, load_balancer_config):
        self.docker = docker_client
        self.lb_config = load_balancer_config
        self.deployments = {}
    
    def deploy_new_version(self, model_name: str, model_version: str, 
                          docker_image: str, config: Dict[str, Any]):
        """Deploy new model version using blue-green strategy"""
        
        current_deployment = self.deployments.get(model_name)
        
        # Determine colors
        if current_deployment is None:
            new_color = 'blue'
            old_color = None
        else:
            current_color = current_deployment['color']
            new_color = 'green' if current_color == 'blue' else 'blue'
            old_color = current_color
        
        # Deploy new version
        container_name = f"{model_name}-{new_color}"
        
        container = self.docker.containers.run(
            docker_image,
            name=container_name,
            environment={
                'MODEL_NAME': model_name,
                'MODEL_VERSION': model_version,
                **config.get('environment', {})
            },
            ports={'8000/tcp': None},  # Dynamic port assignment
            detach=True
        )
        
        # Wait for health check
        if self.wait_for_health_check(container):
            # Update load balancer
            self.update_load_balancer(model_name, container, new_color)
            
            # Update deployment record
            self.deployments[model_name] = {
                'container': container,
                'color': new_color,
                'version': model_version,
                'deployed_at': time.time()
            }
            
            # Clean up old deployment
            if old_color and current_deployment:
                self.cleanup_old_deployment(current_deployment['container'])
            
            return True
        else:
            # Rollback on failure
            container.stop()
            container.remove()
            return False
    
    def wait_for_health_check(self, container, timeout=300):
        """Wait for container to pass health checks"""
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Get container port
                container.reload()
                port = container.attrs['NetworkSettings']['Ports']['8000/tcp'][0]['HostPort']
                
                # Health check
                response = requests.get(f"http://localhost:{port}/health")
                if response.status_code == 200:
                    return True
                    
            except Exception as e:
                print(f"Health check failed: {e}")
            
            time.sleep(10)
        
        return False
    
    def rollback_deployment(self, model_name: str):
        """Rollback to previous model version"""
        
        # Implementation would restore previous container
        # and update load balancer configuration
        pass
```

### Canary Deployment for ML
```python
class CanaryDeploymentManager:
    """Manage canary deployments for ML models"""
    
    def __init__(self, traffic_router):
        self.traffic_router = traffic_router
        self.canary_deployments = {}
    
    def start_canary_deployment(self, model_name: str, new_version: str, 
                               canary_percentage: float = 5.0):
        """Start canary deployment with traffic splitting"""
        
        # Deploy canary version
        canary_endpoint = self.deploy_canary_version(model_name, new_version)
        
        # Configure traffic splitting
        self.traffic_router.add_canary_route(
            model_name, 
            canary_endpoint, 
            canary_percentage
        )
        
        # Track canary deployment
        self.canary_deployments[model_name] = {
            'version': new_version,
            'endpoint': canary_endpoint,
            'traffic_percentage': canary_percentage,
            'start_time': time.time(),
            'metrics': {}
        }
    
    def monitor_canary_metrics(self, model_name: str):
        """Monitor canary deployment metrics"""
        
        canary = self.canary_deployments[model_name]
        
        # Collect metrics from both versions
        production_metrics = self.collect_metrics(f"{model_name}-production")
        canary_metrics = self.collect_metrics(f"{model_name}-canary")
        
        # Compare key metrics
        comparison = {
            'error_rate': {
                'production': production_metrics['error_rate'],
                'canary': canary_metrics['error_rate'],
                'threshold': 0.05  # 5% error rate threshold
            },
            'latency_p95': {
                'production': production_metrics['latency_p95'],
                'canary': canary_metrics['latency_p95'],
                'threshold': production_metrics['latency_p95'] * 1.2  # 20% increase
            },
            'prediction_accuracy': {
                'production': production_metrics.get('accuracy', 0),
                'canary': canary_metrics.get('accuracy', 0),
                'threshold': production_metrics.get('accuracy', 0) * 0.95  # 5% decrease
            }
        }
        
        # Automatic promotion/rollback decision
        should_promote = all([
            comparison['error_rate']['canary'] <= comparison['error_rate']['threshold'],
            comparison['latency_p95']['canary'] <= comparison['latency_p95']['threshold'],
            comparison['prediction_accuracy']['canary'] >= comparison['prediction_accuracy']['threshold']
        ])
        
        return comparison, should_promote
    
    def promote_canary(self, model_name: str):
        """Promote canary to full production"""
        
        canary = self.canary_deployments[model_name]
        
        # Gradually increase traffic
        for percentage in [10, 25, 50, 75, 100]:
            self.traffic_router.update_canary_traffic(model_name, percentage)
            time.sleep(300)  # Wait 5 minutes between increases
            
            # Monitor for issues
            _, should_continue = self.monitor_canary_metrics(model_name)
            if not should_continue:
                self.rollback_canary(model_name)
                return False
        
        # Complete promotion
        self.traffic_router.promote_canary_to_production(model_name)
        del self.canary_deployments[model_name]
        
        return True
```

This integration guide focuses on the critical intersection between MLOps and data engineering, providing practical patterns for production ML systems.