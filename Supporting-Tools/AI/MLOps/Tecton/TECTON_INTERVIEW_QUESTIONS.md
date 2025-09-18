# Tecton Interview Questions

## Basic Concepts

### 1. What is Tecton and its key features?
**Answer:** Tecton is an enterprise feature store platform for ML. Key features:

- **Feature Store**: Centralized feature management and serving
- **Real-time Features**: Low-latency feature serving
- **Feature Engineering**: Declarative feature definitions
- **Data Orchestration**: Automated feature pipeline management
- **Monitoring**: Feature drift and data quality monitoring
- **Governance**: Feature lineage and access control

```python
import tecton
from tecton import Entity, FeatureView, BatchSource, StreamSource
from datetime import datetime, timedelta

# Define entity
user = Entity(
    name="user",
    description="User entity for recommendation system",
    tags={"team": "ml-platform"}
)

# Batch feature view
@tecton.batch_feature_view(
    sources=[BatchSource.parquet("s3://bucket/user_data/")],
    entities=[user],
    mode="spark_sql",
    online=True,
    offline=True,
    feature_start_time=datetime(2023, 1, 1),
    batch_schedule=timedelta(hours=1)
)
def user_demographics(user_data):
    return f"""
        SELECT
            user_id,
            age,
            income,
            location,
            timestamp
        FROM {user_data}
        WHERE timestamp >= current_timestamp() - interval 30 days
    """

# Stream feature view
@tecton.stream_feature_view(
    source=StreamSource.kafka("user_events"),
    entities=[user],
    mode="python",
    online=True,
    feature_start_time=datetime(2023, 1, 1)
)
def user_activity_features(user_events):
    from tecton import materialization_context
    
    def transform(events_df):
        # Calculate real-time features
        features = events_df.groupby('user_id').agg({
            'page_views': 'sum',
            'clicks': 'sum',
            'session_duration': 'mean'
        }).reset_index()
        
        features['timestamp'] = materialization_context().end_time
        return features
    
    return transform
```

### 2. How do you define and manage feature views?
**Answer:** Feature views define how features are computed and served from data sources.

```python
from tecton import FeatureView, BatchSource, Entity, Aggregation
from tecton.types import Field, String, Int64, Float64
from datetime import datetime, timedelta

# Define entities
user = Entity(name="user", description="User entity")
product = Entity(name="product", description="Product entity")

# Batch source
transactions_source = BatchSource.parquet(
    "s3://data-lake/transactions/",
    timestamp_field="transaction_time"
)

# Aggregation feature view
@tecton.batch_feature_view(
    sources=[transactions_source],
    entities=[user],
    mode="spark_sql",
    aggregation_interval=timedelta(hours=1),
    aggregations=[
        Aggregation(column="amount", function="sum", time_window=timedelta(days=1)),
        Aggregation(column="amount", function="sum", time_window=timedelta(days=7)),
        Aggregation(column="amount", function="count", time_window=timedelta(days=30)),
        Aggregation(column="amount", function="mean", time_window=timedelta(days=30))
    ],
    online=True,
    offline=True,
    feature_start_time=datetime(2023, 1, 1)
)
def user_transaction_features(transactions):
    return f"""
        SELECT
            user_id,
            amount,
            transaction_time as timestamp
        FROM {transactions}
        WHERE amount > 0
    """

# Complex feature engineering
@tecton.batch_feature_view(
    sources=[transactions_source],
    entities=[user, product],
    mode="python",
    batch_schedule=timedelta(hours=6),
    online=True,
    offline=True
)
def user_product_affinity(transactions):
    def compute_affinity(df):
        import pandas as pd
        
        # Calculate user-product interaction features
        user_product_stats = df.groupby(['user_id', 'product_id']).agg({
            'amount': ['sum', 'count', 'mean'],
            'rating': 'mean'
        }).reset_index()
        
        # Flatten column names
        user_product_stats.columns = [
            'user_id', 'product_id', 'total_spent', 'purchase_count', 
            'avg_amount', 'avg_rating'
        ]
        
        # Calculate affinity score
        user_product_stats['affinity_score'] = (
            user_product_stats['total_spent'] * 0.4 +
            user_product_stats['purchase_count'] * 0.3 +
            user_product_stats['avg_rating'] * 0.3
        )
        
        user_product_stats['timestamp'] = pd.Timestamp.now()
        
        return user_product_stats
    
    return compute_affinity

# Real-time feature view
@tecton.stream_feature_view(
    source=StreamSource.kafka(
        "user_clicks",
        kafka_config={"bootstrap.servers": "localhost:9092"}
    ),
    entities=[user],
    mode="python",
    online=True
)
def real_time_user_behavior(click_stream):
    def process_clicks(events_df):
        import pandas as pd
        
        # Calculate sliding window features
        features = events_df.groupby('user_id').agg({
            'click_count': 'sum',
            'page_views': 'sum',
            'session_duration': 'mean'
        }).reset_index()
        
        # Add derived features
        features['click_rate'] = features['click_count'] / features['page_views']
        features['engagement_score'] = (
            features['click_rate'] * features['session_duration']
        )
        
        features['timestamp'] = pd.Timestamp.now()
        
        return features
    
    return process_clicks
```

### 3. How do you serve features for online and offline use cases?
**Answer:** Tecton provides both online (real-time) and offline (batch) feature serving.

```python
import tecton
from tecton import FeatureService

# Define feature service
feature_service = FeatureService(
    name="recommendation_features",
    features=[
        user_demographics,
        user_transaction_features,
        user_product_affinity,
        real_time_user_behavior
    ],
    description="Features for recommendation model"
)

# Online feature serving
def get_online_features(user_id, product_id):
    # Get features for real-time inference
    feature_vector = feature_service.get_online_features(
        join_keys={
            "user": user_id,
            "product": product_id
        }
    )
    
    return feature_vector.to_dict()

# Batch feature serving for training
def get_training_features(start_date, end_date):
    # Get historical features for model training
    training_data = feature_service.get_historical_features(
        spine_dataframe=get_training_spine(start_date, end_date),
        timestamp_key="timestamp"
    )
    
    return training_data.to_pandas()

def get_training_spine(start_date, end_date):
    """Create spine dataframe with entity keys and timestamps"""
    import pandas as pd
    
    # Generate training examples
    spine_data = []
    
    # Sample user-product pairs with timestamps
    for user_id in range(1, 1001):  # 1000 users
        for product_id in range(1, 101):  # 100 products
            # Random timestamps within date range
            timestamp = pd.Timestamp(start_date) + pd.Timedelta(
                days=np.random.randint(0, (end_date - start_date).days)
            )
            
            spine_data.append({
                'user': user_id,
                'product': product_id,
                'timestamp': timestamp
            })
    
    return pd.DataFrame(spine_data)

# Feature serving with caching
class CachedFeatureService:
    def __init__(self, feature_service, cache_ttl=300):
        self.feature_service = feature_service
        self.cache = {}
        self.cache_ttl = cache_ttl
    
    def get_features_with_cache(self, join_keys):
        import time
        
        cache_key = str(sorted(join_keys.items()))
        current_time = time.time()
        
        # Check cache
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if current_time - timestamp < self.cache_ttl:
                return cached_data
        
        # Fetch fresh features
        features = self.feature_service.get_online_features(join_keys)
        
        # Update cache
        self.cache[cache_key] = (features, current_time)
        
        return features

# Batch inference pipeline
def batch_inference_pipeline():
    """Run batch inference using historical features"""
    
    # Define inference spine
    inference_spine = pd.DataFrame({
        'user': [1, 2, 3, 4, 5],
        'product': [10, 20, 30, 40, 50],
        'timestamp': pd.Timestamp.now()
    })
    
    # Get features
    features_df = feature_service.get_historical_features(
        spine_dataframe=inference_spine,
        timestamp_key="timestamp"
    ).to_pandas()
    
    # Load model and make predictions
    model = load_model("s3://models/recommendation_model.pkl")
    predictions = model.predict(features_df.drop(['user', 'product', 'timestamp'], axis=1))
    
    # Combine with entity keys
    results = pd.DataFrame({
        'user': features_df['user'],
        'product': features_df['product'],
        'prediction': predictions,
        'timestamp': features_df['timestamp']
    })
    
    return results

def load_model(model_path):
    """Load trained model"""
    import joblib
    return joblib.load(model_path)
```

## Intermediate Concepts

### 4. How do you implement feature monitoring and data quality checks?
**Answer:** Tecton provides comprehensive monitoring for feature drift and data quality.

```python
from tecton import DataQualityCheck, FeatureMonitor
from tecton.types import Float64

# Data quality checks
@tecton.data_quality_check
def validate_user_features(df):
    """Validate user demographic features"""
    checks = []
    
    # Check for null values
    null_check = df['age'].isnull().sum() / len(df) < 0.05
    checks.append(('age_null_rate', null_check))
    
    # Check value ranges
    age_range_check = (df['age'] >= 18) & (df['age'] <= 100)
    checks.append(('age_range', age_range_check.all()))
    
    # Check income distribution
    income_check = df['income'].between(0, 1000000).all()
    checks.append(('income_range', income_check))
    
    return checks

# Feature monitoring
user_feature_monitor = FeatureMonitor(
    feature_view=user_demographics,
    metrics=[
        "null_rate",
        "mean",
        "std",
        "min",
        "max",
        "distinct_count"
    ],
    alert_thresholds={
        "null_rate": 0.05,
        "mean_drift": 0.1,
        "std_drift": 0.15
    }
)

# Custom monitoring function
def monitor_feature_drift():
    """Monitor feature drift over time"""
    
    # Get recent feature statistics
    current_stats = user_feature_monitor.get_current_stats()
    baseline_stats = user_feature_monitor.get_baseline_stats()
    
    drift_metrics = {}
    
    for feature in ['age', 'income']:
        # Calculate drift metrics
        mean_drift = abs(
            current_stats[f'{feature}_mean'] - baseline_stats[f'{feature}_mean']
        ) / baseline_stats[f'{feature}_mean']
        
        std_drift = abs(
            current_stats[f'{feature}_std'] - baseline_stats[f'{feature}_std']
        ) / baseline_stats[f'{feature}_std']
        
        drift_metrics[f'{feature}_mean_drift'] = mean_drift
        drift_metrics[f'{feature}_std_drift'] = std_drift
        
        # Check thresholds
        if mean_drift > 0.1:
            send_alert(f"High mean drift detected for {feature}: {mean_drift}")
        
        if std_drift > 0.15:
            send_alert(f"High std drift detected for {feature}: {std_drift}")
    
    return drift_metrics

def send_alert(message):
    """Send monitoring alert"""
    print(f"ALERT: {message}")
    # Integration with alerting system (Slack, PagerDuty, etc.)

# Feature freshness monitoring
def monitor_feature_freshness():
    """Monitor feature freshness and availability"""
    
    freshness_metrics = {}
    
    for fv in [user_demographics, user_transaction_features]:
        # Check last materialization time
        last_materialization = fv.get_last_materialization_time()
        current_time = datetime.now()
        
        freshness_hours = (current_time - last_materialization).total_seconds() / 3600
        
        freshness_metrics[f'{fv.name}_freshness_hours'] = freshness_hours
        
        # Alert if features are stale
        if freshness_hours > 24:  # 24 hour threshold
            send_alert(f"Stale features detected for {fv.name}: {freshness_hours} hours")
    
    return freshness_metrics

# Automated data validation pipeline
class FeatureValidationPipeline:
    def __init__(self, feature_views):
        self.feature_views = feature_views
        self.validation_results = {}
    
    def run_validation(self):
        """Run comprehensive feature validation"""
        
        for fv in self.feature_views:
            print(f"Validating {fv.name}...")
            
            # Get recent data
            recent_data = fv.get_recent_data(hours=24)
            
            # Run validation checks
            validation_results = {
                'completeness': self._check_completeness(recent_data),
                'consistency': self._check_consistency(recent_data),
                'accuracy': self._check_accuracy(recent_data),
                'timeliness': self._check_timeliness(fv)
            }
            
            self.validation_results[fv.name] = validation_results
            
            # Generate report
            self._generate_validation_report(fv.name, validation_results)
    
    def _check_completeness(self, df):
        """Check data completeness"""
        total_rows = len(df)
        complete_rows = df.dropna().shape[0]
        completeness_rate = complete_rows / total_rows if total_rows > 0 else 0
        
        return {
            'completeness_rate': completeness_rate,
            'passed': completeness_rate >= 0.95
        }
    
    def _check_consistency(self, df):
        """Check data consistency"""
        # Check for duplicate keys
        duplicate_rate = df.duplicated().sum() / len(df) if len(df) > 0 else 0
        
        return {
            'duplicate_rate': duplicate_rate,
            'passed': duplicate_rate <= 0.01
        }
    
    def _check_accuracy(self, df):
        """Check data accuracy"""
        # Domain-specific accuracy checks
        accuracy_checks = []
        
        if 'age' in df.columns:
            valid_age = df['age'].between(0, 120).all()
            accuracy_checks.append(valid_age)
        
        if 'income' in df.columns:
            valid_income = df['income'] >= 0
            accuracy_checks.append(valid_income.all())
        
        overall_accuracy = all(accuracy_checks) if accuracy_checks else True
        
        return {
            'accuracy_passed': overall_accuracy,
            'passed': overall_accuracy
        }
    
    def _check_timeliness(self, feature_view):
        """Check feature timeliness"""
        last_update = feature_view.get_last_materialization_time()
        hours_since_update = (datetime.now() - last_update).total_seconds() / 3600
        
        return {
            'hours_since_update': hours_since_update,
            'passed': hours_since_update <= 6  # 6 hour SLA
        }
    
    def _generate_validation_report(self, feature_view_name, results):
        """Generate validation report"""
        print(f"\n=== Validation Report for {feature_view_name} ===")
        
        for check_type, result in results.items():
            status = "✅ PASSED" if result['passed'] else "❌ FAILED"
            print(f"{check_type}: {status}")
            
            if not result['passed']:
                print(f"  Details: {result}")
        
        print("=" * 50)

# Usage
if __name__ == "__main__":
    # Run feature monitoring
    drift_metrics = monitor_feature_drift()
    freshness_metrics = monitor_feature_freshness()
    
    # Run validation pipeline
    validator = FeatureValidationPipeline([
        user_demographics,
        user_transaction_features
    ])
    validator.run_validation()
```

This focused Tecton interview questions set covers essential feature store concepts, providing practical examples for feature engineering, serving, and monitoring in production ML systems.