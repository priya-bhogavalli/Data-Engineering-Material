# Feast Interview Questions

## Basic Concepts

### 1. What is Feast and its key components?
**Answer:** Feast is an open-source feature store for ML. Key components:

- **Feature Repository**: Git-based feature definitions
- **Registry**: Metadata store for features and data sources
- **Online Store**: Low-latency feature serving (Redis, DynamoDB)
- **Offline Store**: Historical features for training (BigQuery, Snowflake)
- **Feature Views**: Feature transformation definitions
- **Entities**: Primary keys for feature grouping

```python
from feast import Entity, FeatureView, Field, FileSource, FeatureStore
from feast.types import Float32, Int64, String
from datetime import timedelta

# Define entity
user = Entity(
    name="user_id",
    description="User identifier"
)

# Define data source
user_stats_source = FileSource(
    name="user_stats_source",
    path="data/user_stats.parquet",
    timestamp_field="event_timestamp"
)

# Define feature view
user_stats_fv = FeatureView(
    name="user_stats",
    entities=[user],
    ttl=timedelta(days=1),
    schema=[
        Field(name="daily_transactions", dtype=Int64),
        Field(name="total_spent", dtype=Float32),
        Field(name="avg_transaction_amount", dtype=Float32)
    ],
    source=user_stats_source,
    tags={"team": "ml-platform"}
)

# Initialize feature store
fs = FeatureStore(repo_path=".")

# Apply feature definitions
fs.apply([user, user_stats_source, user_stats_fv])
```

### 2. How do you configure different data sources and stores?
**Answer:** Feast supports multiple data sources and storage backends for flexibility.

```python
from feast import BigQuerySource, RedshiftSource, SnowflakeSource
from feast.infra.offline_stores.bigquery import BigQueryOfflineStoreConfig
from feast.infra.online_stores.redis import RedisOnlineStoreConfig

# BigQuery source
bigquery_source = BigQuerySource(
    name="transactions_bq",
    table="project.dataset.transactions",
    timestamp_field="transaction_time",
    created_timestamp_column="created_at"
)

# Snowflake source  
snowflake_source = SnowflakeSource(
    name="user_features_sf",
    database="ML_DB",
    schema="FEATURES", 
    table="USER_FEATURES",
    timestamp_field="event_timestamp"
)

# Feature store configuration
feature_store_yaml = """
project: ml_platform
registry: data/registry.db
provider: local
online_store:
    type: redis
    connection_string: "localhost:6379"
offline_store:
    type: file
"""

# Advanced configuration with cloud stores
cloud_config = """
project: production_ml
registry: s3://ml-registry/registry.db
provider: aws
online_store:
    type: dynamodb
    region: us-west-2
offline_store:
    type: bigquery
    project_id: my-gcp-project
    dataset_id: feast_offline_store
"""

# Multiple feature views with different sources
@FeatureView(
    entities=[user],
    ttl=timedelta(hours=2),
    source=bigquery_source
)
def user_transaction_features():
    return [
        Field("transaction_count_1h", Int64),
        Field("total_amount_1h", Float32),
        Field("avg_amount_1h", Float32)
    ]

@FeatureView(
    entities=[user], 
    ttl=timedelta(days=7),
    source=snowflake_source
)
def user_profile_features():
    return [
        Field("age", Int64),
        Field("income_bracket", String),
        Field("credit_score", Int64)
    ]
```

### 3. How do you serve features for online and offline scenarios?
**Answer:** Feast provides APIs for both real-time and batch feature serving.

```python
from feast import FeatureStore
import pandas as pd
from datetime import datetime, timedelta

# Initialize feature store
fs = FeatureStore(repo_path=".")

# Online feature serving
def get_online_features(user_ids):
    """Get features for real-time inference"""
    
    # Define feature references
    features = [
        "user_stats:daily_transactions",
        "user_stats:total_spent", 
        "user_stats:avg_transaction_amount"
    ]
    
    # Get online features
    feature_vector = fs.get_online_features(
        features=features,
        entity_rows=[{"user_id": user_id} for user_id in user_ids]
    )
    
    return feature_vector.to_dict()

# Offline feature serving for training
def get_historical_features(start_date, end_date):
    """Get historical features for model training"""
    
    # Create entity dataframe (spine)
    entity_df = pd.DataFrame({
        "user_id": [1001, 1002, 1003, 1004, 1005],
        "event_timestamp": [
            datetime(2023, 1, 1, 12, 0, 0),
            datetime(2023, 1, 2, 12, 0, 0), 
            datetime(2023, 1, 3, 12, 0, 0),
            datetime(2023, 1, 4, 12, 0, 0),
            datetime(2023, 1, 5, 12, 0, 0)
        ]
    })
    
    # Get historical features
    training_df = fs.get_historical_features(
        entity_df=entity_df,
        features=[
            "user_stats:daily_transactions",
            "user_stats:total_spent",
            "user_stats:avg_transaction_amount"
        ]
    ).to_df()
    
    return training_df

# Batch feature materialization
def materialize_features():
    """Materialize features to online store"""
    
    # Materialize specific feature views
    fs.materialize(
        feature_views=["user_stats"],
        start_date=datetime.now() - timedelta(days=7),
        end_date=datetime.now()
    )
    
    print("Features materialized to online store")

# Feature serving with validation
def get_features_with_validation(user_ids, validate=True):
    """Get features with optional validation"""
    
    features = fs.get_online_features(
        features=[
            "user_stats:daily_transactions",
            "user_stats:total_spent"
        ],
        entity_rows=[{"user_id": uid} for uid in user_ids]
    )
    
    feature_dict = features.to_dict()
    
    if validate:
        # Validate feature values
        for i, user_id in enumerate(user_ids):
            daily_txns = feature_dict["daily_transactions"][i]
            total_spent = feature_dict["total_spent"][i]
            
            # Validation checks
            if daily_txns < 0:
                print(f"Warning: Negative transactions for user {user_id}")
            
            if total_spent < 0:
                print(f"Warning: Negative spending for user {user_id}")
    
    return feature_dict

# Real-time feature pipeline
class RealTimeFeatureService:
    def __init__(self, feature_store_path):
        self.fs = FeatureStore(repo_path=feature_store_path)
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes
    
    def get_features_cached(self, user_id):
        """Get features with caching"""
        import time
        
        current_time = time.time()
        
        # Check cache
        if user_id in self.cache:
            cached_features, timestamp = self.cache[user_id]
            if current_time - timestamp < self.cache_ttl:
                return cached_features
        
        # Fetch fresh features
        features = self.fs.get_online_features(
            features=[
                "user_stats:daily_transactions",
                "user_stats:total_spent",
                "user_stats:avg_transaction_amount"
            ],
            entity_rows=[{"user_id": user_id}]
        ).to_dict()
        
        # Update cache
        self.cache[user_id] = (features, current_time)
        
        return features
    
    def batch_get_features(self, user_ids, batch_size=100):
        """Get features in batches for efficiency"""
        
        all_features = {}
        
        for i in range(0, len(user_ids), batch_size):
            batch_ids = user_ids[i:i + batch_size]
            
            batch_features = self.fs.get_online_features(
                features=[
                    "user_stats:daily_transactions", 
                    "user_stats:total_spent",
                    "user_stats:avg_transaction_amount"
                ],
                entity_rows=[{"user_id": uid} for uid in batch_ids]
            ).to_dict()
            
            # Merge batch results
            for j, user_id in enumerate(batch_ids):
                all_features[user_id] = {
                    "daily_transactions": batch_features["daily_transactions"][j],
                    "total_spent": batch_features["total_spent"][j], 
                    "avg_transaction_amount": batch_features["avg_transaction_amount"][j]
                }
        
        return all_features
```

## Intermediate Concepts

### 4. How do you implement feature transformations and streaming features?
**Answer:** Feast supports feature transformations and real-time streaming through various mechanisms.

```python
from feast import FeatureView, Field, PushSource, RequestSource
from feast.types import Float32, Int64, String, Array
from feast.value_type import ValueType
import pandas as pd

# Push source for streaming features
user_activity_push_source = PushSource(
    name="user_activity_push_source",
    batch_source=FileSource(
        path="data/user_activity.parquet",
        timestamp_field="event_timestamp"
    )
)

# Streaming feature view
user_activity_fv = FeatureView(
    name="user_activity_features",
    entities=[user],
    ttl=timedelta(minutes=30),
    schema=[
        Field(name="page_views_1h", dtype=Int64),
        Field(name="clicks_1h", dtype=Int64),
        Field(name="session_duration_1h", dtype=Float32)
    ],
    source=user_activity_push_source,
    tags={"stream": "real-time"}
)

# On-demand feature transformations
user_request_source = RequestSource(
    name="user_request_source",
    schema=[
        Field(name="current_location", dtype=String),
        Field(name="device_type", dtype=String)
    ]
)

@FeatureView(
    entities=[user],
    sources=[user_stats_source, user_request_source],
    schema=[
        Field(name="location_spending_ratio", dtype=Float32),
        Field(name="device_preference_score", dtype=Float32)
    ]
)
def on_demand_user_features():
    """On-demand feature transformations"""
    
    def transform_features(inputs):
        # Access historical features
        total_spent = inputs["total_spent"]
        
        # Access request features  
        current_location = inputs["current_location"]
        device_type = inputs["device_type"]
        
        # Calculate derived features
        location_spending_ratio = calculate_location_ratio(total_spent, current_location)
        device_score = calculate_device_score(device_type)
        
        return pd.DataFrame({
            "location_spending_ratio": location_spending_ratio,
            "device_preference_score": device_score
        })
    
    return transform_features

def calculate_location_ratio(total_spent, location):
    """Calculate spending ratio by location"""
    location_multipliers = {
        "urban": 1.2,
        "suburban": 1.0, 
        "rural": 0.8
    }
    
    multiplier = location_multipliers.get(location, 1.0)
    return total_spent * multiplier

def calculate_device_score(device_type):
    """Calculate device preference score"""
    device_scores = {
        "mobile": 0.8,
        "desktop": 0.6,
        "tablet": 0.7
    }
    
    return device_scores.get(device_type, 0.5)

# Streaming feature ingestion
def push_streaming_features():
    """Push real-time features to Feast"""
    
    # Simulate streaming data
    streaming_data = pd.DataFrame({
        "user_id": [1001, 1002, 1003],
        "page_views_1h": [15, 8, 22],
        "clicks_1h": [3, 1, 7], 
        "session_duration_1h": [25.5, 12.3, 45.2],
        "event_timestamp": [datetime.now()] * 3
    })
    
    # Push to Feast
    fs.push("user_activity_push_source", streaming_data)
    
    print("Streaming features pushed successfully")

# Feature validation and monitoring
class FeatureValidator:
    def __init__(self, feature_store):
        self.fs = feature_store
        
    def validate_feature_freshness(self, feature_view_name, max_age_hours=24):
        """Validate feature freshness"""
        
        # Get feature view metadata
        fv = self.fs.get_feature_view(feature_view_name)
        
        # Check last materialization time
        # This would typically query the registry or online store
        last_update = self._get_last_materialization_time(fv)
        
        hours_since_update = (datetime.now() - last_update).total_seconds() / 3600
        
        if hours_since_update > max_age_hours:
            raise ValueError(f"Features are stale: {hours_since_update} hours old")
        
        return True
    
    def validate_feature_values(self, user_ids, feature_names):
        """Validate feature value ranges"""
        
        features = self.fs.get_online_features(
            features=feature_names,
            entity_rows=[{"user_id": uid} for uid in user_ids]
        ).to_dict()
        
        validation_results = {}
        
        for feature_name in feature_names:
            values = features[feature_name.split(":")[-1]]
            
            # Check for nulls
            null_count = sum(1 for v in values if v is None)
            null_rate = null_count / len(values)
            
            # Check value ranges (example for transaction features)
            if "transaction" in feature_name:
                invalid_count = sum(1 for v in values if v is not None and v < 0)
                invalid_rate = invalid_count / len(values)
            else:
                invalid_rate = 0
            
            validation_results[feature_name] = {
                "null_rate": null_rate,
                "invalid_rate": invalid_rate,
                "passed": null_rate < 0.1 and invalid_rate < 0.05
            }
        
        return validation_results
    
    def _get_last_materialization_time(self, feature_view):
        """Get last materialization timestamp"""
        # This would query the actual materialization metadata
        return datetime.now() - timedelta(hours=2)

# Usage examples
if __name__ == "__main__":
    # Apply feature definitions
    fs.apply([
        user,
        user_stats_source,
        user_stats_fv,
        user_activity_push_source,
        user_activity_fv
    ])
    
    # Materialize historical features
    materialize_features()
    
    # Push streaming features
    push_streaming_features()
    
    # Get online features
    online_features = get_online_features([1001, 1002, 1003])
    print("Online features:", online_features)
    
    # Validate features
    validator = FeatureValidator(fs)
    validation_results = validator.validate_feature_values(
        user_ids=[1001, 1002],
        feature_names=["user_stats:daily_transactions", "user_stats:total_spent"]
    )
    print("Validation results:", validation_results)
```

This focused Feast interview questions set covers essential open-source feature store concepts, providing practical examples for feature definition, serving, transformations, and streaming capabilities.