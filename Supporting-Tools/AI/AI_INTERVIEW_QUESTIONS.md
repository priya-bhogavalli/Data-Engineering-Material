# AI Interview Questions for Data Engineering

## Basic Level (0-2 years experience)

### 1. What is the difference between supervised and unsupervised learning?
**Answer:**
- **Supervised Learning**: Uses labeled training data to learn patterns
  - Examples: Classification (spam detection), Regression (price prediction)
  - Algorithms: Linear Regression, Decision Trees, Random Forest, SVM
  - Goal: Predict outcomes for new, unseen data

- **Unsupervised Learning**: Finds patterns in data without labels
  - Examples: Clustering (customer segmentation), Dimensionality reduction
  - Algorithms: K-means, Hierarchical clustering, PCA
  - Goal: Discover hidden structures in data

**Data Engineering Context:**
```python
# Supervised: Predicting data quality scores
from sklearn.ensemble import RandomForestClassifier

# Features: null_percentage, duplicate_count, schema_violations
X = [[0.1, 5, 0], [0.3, 20, 2], [0.05, 1, 0]]
y = [1, 0, 1]  # 1 = good quality, 0 = poor quality

model = RandomForestClassifier()
model.fit(X, y)

# Unsupervised: Detecting anomalous data patterns
from sklearn.cluster import KMeans

# Cluster data points to find unusual patterns
kmeans = KMeans(n_clusters=3)
clusters = kmeans.fit_predict(data_features)
```

### 2. How would you use machine learning in a data pipeline?
**Answer:**
ML can enhance data pipelines in several ways:

1. **Data Quality Monitoring**: Predict and detect data quality issues
2. **Anomaly Detection**: Identify unusual patterns in data streams
3. **Automated Classification**: Categorize incoming data automatically
4. **Predictive Scaling**: Forecast resource needs for pipeline scaling

**Implementation Example:**
```python
class MLEnhancedPipeline:
    def __init__(self):
        self.quality_model = self.load_quality_model()
        self.anomaly_detector = self.load_anomaly_detector()
    
    def process_batch(self, data):
        # 1. Quality prediction
        quality_score = self.quality_model.predict(self.extract_features(data))
        
        if quality_score < 0.8:
            self.alert_low_quality(data)
        
        # 2. Anomaly detection
        anomalies = self.anomaly_detector.predict(data)
        clean_data = data[anomalies == 1]  # Keep normal data
        
        # 3. Continue with standard processing
        return self.transform_data(clean_data)
```

### 3. What is the purpose of feature engineering in ML?
**Answer:**
Feature engineering transforms raw data into meaningful inputs for ML models.

**Key Techniques:**
- **Scaling/Normalization**: Ensure features have similar ranges
- **Encoding**: Convert categorical variables to numerical
- **Feature Creation**: Derive new features from existing ones
- **Selection**: Choose most relevant features

**Data Engineering Example:**
```python
def engineer_data_quality_features(df):
    """Create features for data quality prediction."""
    features = {}
    
    # Basic statistics
    features['row_count'] = len(df)
    features['column_count'] = len(df.columns)
    
    # Quality indicators
    features['null_percentage'] = df.isnull().sum().sum() / (len(df) * len(df.columns))
    features['duplicate_percentage'] = df.duplicated().sum() / len(df)
    
    # Data type distribution
    numeric_cols = len(df.select_dtypes(include=['number']).columns)
    features['numeric_ratio'] = numeric_cols / len(df.columns)
    
    # Schema consistency
    features['schema_violations'] = count_schema_violations(df)
    
    return pd.DataFrame([features])
```

## Intermediate Level (2-5 years experience)

### 4. How would you implement real-time anomaly detection in a streaming data pipeline?
**Answer:**
Real-time anomaly detection requires online learning algorithms and streaming processing frameworks.

**Architecture:**
```python
from kafka import KafkaConsumer
from sklearn.ensemble import IsolationForest
import numpy as np
import json

class StreamingAnomalyDetector:
    def __init__(self, kafka_topic, model_update_interval=1000):
        self.consumer = KafkaConsumer(
            kafka_topic,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self.model = IsolationForest(contamination=0.1)
        self.buffer = []
        self.model_update_interval = model_update_interval
        self.processed_count = 0
        self.is_trained = False
    
    def process_stream(self):
        """Process streaming data for anomaly detection."""
        for message in self.consumer:
            data_point = self.extract_features(message.value)
            
            # Add to buffer
            self.buffer.append(data_point)
            
            # Initial training
            if not self.is_trained and len(self.buffer) >= 100:
                self.train_initial_model()
            
            # Detect anomaly if model is trained
            if self.is_trained:
                is_anomaly = self.detect_anomaly(data_point)
                
                if is_anomaly:
                    self.handle_anomaly(message.value, data_point)
            
            # Periodic model update
            self.processed_count += 1
            if self.processed_count % self.model_update_interval == 0:
                self.update_model()
    
    def train_initial_model(self):
        """Train initial model with buffered data."""
        X = np.array(self.buffer)
        self.model.fit(X)
        self.is_trained = True
        print("Initial model trained")
    
    def detect_anomaly(self, data_point):
        """Detect if data point is anomalous."""
        prediction = self.model.predict([data_point])
        return prediction[0] == -1  # -1 indicates anomaly
    
    def update_model(self):
        """Update model with recent data."""
        if len(self.buffer) > 1000:
            # Keep only recent data
            recent_data = self.buffer[-1000:]
            X = np.array(recent_data)
            self.model.fit(X)
            print("Model updated with recent data")
    
    def handle_anomaly(self, original_data, features):
        """Handle detected anomaly."""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'type': 'anomaly_detected',
            'data': original_data,
            'features': features.tolist(),
            'severity': self.calculate_severity(features)
        }
        
        # Send alert (to monitoring system, Slack, etc.)
        self.send_alert(alert)
    
    def extract_features(self, data):
        """Extract numerical features from data."""
        # Example feature extraction
        features = [
            data.get('value', 0),
            data.get('count', 0),
            len(str(data.get('text', ''))),
            data.get('timestamp', 0) % 86400  # Time of day
        ]
        return np.array(features)

# Usage
detector = StreamingAnomalyDetector('data-stream-topic')
detector.process_stream()
```

### 5. Explain how you would implement MLOps for a data quality model.
**Answer:**
MLOps ensures reliable deployment and maintenance of ML models in production.

**MLOps Pipeline:**
```python
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
import joblib
from datetime import datetime

class DataQualityMLOps:
    def __init__(self, experiment_name="data_quality_models"):
        self.experiment_name = experiment_name
        self.client = MlflowClient()
        mlflow.set_experiment(experiment_name)
    
    def train_and_register_model(self, X_train, y_train, X_test, y_test):
        """Train model with full MLOps tracking."""
        with mlflow.start_run() as run:
            # Model training
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # Evaluation
            train_accuracy = model.score(X_train, y_train)
            test_accuracy = model.score(X_test, y_test)
            
            # Log metrics
            mlflow.log_metric("train_accuracy", train_accuracy)
            mlflow.log_metric("test_accuracy", test_accuracy)
            mlflow.log_metric("feature_count", X_train.shape[1])
            
            # Log parameters
            mlflow.log_param("n_estimators", 100)
            mlflow.log_param("random_state", 42)
            
            # Log model
            mlflow.sklearn.log_model(
                model, 
                "model",
                registered_model_name="data_quality_classifier"
            )
            
            # Log artifacts (feature importance, etc.)
            feature_importance = pd.DataFrame({
                'feature': [f'feature_{i}' for i in range(X_train.shape[1])],
                'importance': model.feature_importances_
            })
            feature_importance.to_csv("feature_importance.csv", index=False)
            mlflow.log_artifact("feature_importance.csv")
            
            return run.info.run_id
    
    def deploy_model_to_production(self, model_version):
        """Deploy model to production stage."""
        self.client.transition_model_version_stage(
            name="data_quality_classifier",
            version=model_version,
            stage="Production"
        )
    
    def monitor_model_performance(self, production_data, true_labels):
        """Monitor production model performance."""
        # Load production model
        model = mlflow.sklearn.load_model(
            "models:/data_quality_classifier/Production"
        )
        
        # Calculate current performance
        predictions = model.predict(production_data)
        current_accuracy = accuracy_score(true_labels, predictions)
        
        # Log monitoring metrics
        with mlflow.start_run():
            mlflow.log_metric("production_accuracy", current_accuracy)
            mlflow.log_metric("monitoring_timestamp", datetime.now().timestamp())
            mlflow.log_metric("sample_size", len(production_data))
        
        # Check for model drift
        if current_accuracy < 0.8:  # Threshold
            self.trigger_retraining_alert()
        
        return current_accuracy
    
    def automated_retraining_pipeline(self, new_data, labels):
        """Automated retraining when performance degrades."""
        print("Starting automated retraining...")
        
        # Prepare data
        X_train, X_test, y_train, y_test = train_test_split(
            new_data, labels, test_size=0.2, random_state=42
        )
        
        # Train new model
        run_id = self.train_and_register_model(X_train, y_train, X_test, y_test)
        
        # Get model version
        latest_version = self.client.get_latest_versions(
            "data_quality_classifier", 
            stages=["None"]
        )[0]
        
        # A/B test new model vs production
        if self.ab_test_model(latest_version.version):
            self.deploy_model_to_production(latest_version.version)
            print(f"New model version {latest_version.version} deployed")
        else:
            print("New model did not pass A/B test")

# Integration with data pipeline
class MLOpsDataPipeline:
    def __init__(self):
        self.mlops = DataQualityMLOps()
        self.model = self.load_production_model()
    
    def load_production_model(self):
        """Load current production model."""
        return mlflow.sklearn.load_model(
            "models:/data_quality_classifier/Production"
        )
    
    def process_with_ml_monitoring(self, data):
        """Process data with ML model and monitoring."""
        # Extract features
        features = self.extract_features(data)
        
        # Predict quality
        quality_predictions = self.model.predict_proba(features)[:, 1]
        
        # Log predictions for monitoring
        self.log_predictions(features, quality_predictions)
        
        # Filter based on quality threshold
        high_quality_mask = quality_predictions > 0.8
        return data[high_quality_mask]
    
    def log_predictions(self, features, predictions):
        """Log predictions for model monitoring."""
        # Store predictions for later performance evaluation
        prediction_log = {
            'timestamp': datetime.now().isoformat(),
            'features': features.tolist(),
            'predictions': predictions.tolist(),
            'model_version': self.get_current_model_version()
        }
        
        # Store in monitoring database or file
        self.store_prediction_log(prediction_log)
```

## Advanced Level (5+ years experience)

### 6. How would you design a RAG (Retrieval-Augmented Generation) system for data engineering documentation?
**Answer:**
A RAG system combines retrieval of relevant documents with generative AI to provide contextual answers.

**Architecture Design:**
```python
from sentence_transformers import SentenceTransformer
import faiss
import openai
from typing import List, Dict, Tuple
import numpy as np

class DataEngineeringRAG:
    def __init__(self, openai_api_key: str):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.openai_api_key = openai_api_key
        openai.api_key = openai_api_key
        
        # Vector store for documents
        self.dimension = self.embedding_model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatIP(self.dimension)
        self.documents = []
        self.metadata = []
    
    def ingest_documentation(self, docs: List[Dict]):
        """Ingest documentation into the RAG system."""
        for doc in docs:
            # Create chunks for long documents
            chunks = self.chunk_document(doc['content'])
            
            for i, chunk in enumerate(chunks):
                # Create embedding
                embedding = self.embedding_model.encode([chunk])
                faiss.normalize_L2(embedding)
                
                # Add to index
                self.index.add(embedding)
                self.documents.append(chunk)
                self.metadata.append({
                    **doc['metadata'],
                    'chunk_id': i,
                    'total_chunks': len(chunks)
                })
    
    def chunk_document(self, content: str, chunk_size: int = 500) -> List[str]:
        """Split document into chunks for better retrieval."""
        words = content.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
        
        return chunks
    
    def retrieve_relevant_context(self, query: str, top_k: int = 5) -> List[Tuple[str, Dict, float]]:
        """Retrieve relevant document chunks."""
        if self.index.ntotal == 0:
            return []
        
        # Create query embedding
        query_embedding = self.embedding_model.encode([query])
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding, min(top_k, self.index.ntotal))
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1:
                results.append((
                    self.documents[idx],
                    self.metadata[idx],
                    float(score)
                ))
        
        return results
    
    def generate_answer(self, question: str, context_docs: List[Tuple[str, Dict, float]]) -> str:
        """Generate answer using retrieved context."""
        # Prepare context
        context = "\n\n".join([
            f"Source: {meta.get('source', 'Unknown')} (relevance: {score:.3f})\n{doc}"
            for doc, meta, score in context_docs
        ])
        
        prompt = f"""
        You are a data engineering expert. Answer the following question based on the provided context.
        
        Context:
        {context}
        
        Question: {question}
        
        Instructions:
        1. Provide a comprehensive answer based on the context
        2. Include specific examples or code snippets when relevant
        3. If the context doesn't contain enough information, say so
        4. Cite the sources when possible
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful data engineering assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    def ask_question(self, question: str) -> Dict:
        """Main interface for asking questions."""
        # Retrieve relevant context
        context_docs = self.retrieve_relevant_context(question, top_k=5)
        
        if not context_docs:
            return {
                'answer': "I don't have enough information to answer this question.",
                'sources': [],
                'confidence': 0.0
            }
        
        # Generate answer
        answer = self.generate_answer(question, context_docs)
        
        # Calculate confidence based on retrieval scores
        avg_score = np.mean([score for _, _, score in context_docs])
        
        return {
            'answer': answer,
            'sources': [meta.get('source', 'Unknown') for _, meta, _ in context_docs],
            'confidence': float(avg_score),
            'retrieved_chunks': len(context_docs)
        }

# Usage example
rag_system = DataEngineeringRAG("your-openai-api-key")

# Ingest documentation
docs = [
    {
        'content': """
        Apache Spark performance optimization involves several key strategies:
        1. Use appropriate file formats like Parquet or Delta Lake
        2. Partition data based on query patterns
        3. Cache frequently accessed datasets
        4. Optimize join strategies using broadcast joins for small tables
        5. Tune Spark configuration parameters like executor memory and cores
        6. Use columnar storage formats for analytical workloads
        7. Minimize data shuffling through proper partitioning
        """,
        'metadata': {'source': 'spark_optimization_guide.md', 'topic': 'performance'}
    },
    {
        'content': """
        Data quality in pipelines can be ensured through:
        - Schema validation at ingestion points
        - Null value detection and handling strategies
        - Duplicate record identification and removal
        - Data type validation and conversion
        - Range and constraint checking
        - Referential integrity validation
        - Statistical anomaly detection
        - Data lineage tracking for root cause analysis
        """,
        'metadata': {'source': 'data_quality_best_practices.md', 'topic': 'quality'}
    }
]

rag_system.ingest_documentation(docs)

# Ask questions
result = rag_system.ask_question("How can I optimize Spark performance for large datasets?")
print(f"Answer: {result['answer']}")
print(f"Confidence: {result['confidence']:.3f}")
print(f"Sources: {result['sources']}")
```

### 7. How would you implement a vector database for semantic search in a data catalog?
**Answer:**
A vector database enables semantic search by storing and querying high-dimensional embeddings of data assets.

**Implementation:**
```python
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DataAsset:
    id: str
    name: str
    description: str
    schema: Dict
    tags: List[str]
    owner: str
    created_at: datetime
    last_updated: datetime

class SemanticDataCatalog:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.embedding_model = SentenceTransformer(model_name)
        self.dimension = self.embedding_model.get_sentence_embedding_dimension()
        
        # Initialize FAISS index
        self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity
        
        # Storage for metadata
        self.assets = {}  # id -> DataAsset
        self.id_to_index = {}  # asset_id -> faiss_index
        self.index_to_id = {}  # faiss_index -> asset_id
        
        self.next_index = 0
    
    def create_asset_embedding(self, asset: DataAsset) -> np.ndarray:
        """Create embedding for a data asset."""
        # Combine different aspects of the asset
        text_parts = [
            f"Dataset: {asset.name}",
            f"Description: {asset.description}",
            f"Owner: {asset.owner}",
            f"Tags: {', '.join(asset.tags)}"
        ]
        
        # Add schema information
        if asset.schema:
            schema_text = self.schema_to_text(asset.schema)
            text_parts.append(f"Schema: {schema_text}")
        
        # Combine all text
        full_text = " | ".join(text_parts)
        
        # Generate embedding
        embedding = self.embedding_model.encode([full_text])
        
        # Normalize for cosine similarity
        faiss.normalize_L2(embedding)
        
        return embedding[0]
    
    def schema_to_text(self, schema: Dict) -> str:
        """Convert schema to text representation."""
        if 'columns' in schema:
            columns = []
            for col in schema['columns']:
                col_text = f"{col['name']} ({col.get('type', 'unknown')})"
                if col.get('description'):
                    col_text += f": {col['description']}"
                columns.append(col_text)
            return ", ".join(columns)
        return str(schema)
    
    def add_asset(self, asset: DataAsset):
        """Add a data asset to the catalog."""
        # Create embedding
        embedding = self.create_asset_embedding(asset)
        
        # Add to FAISS index
        self.index.add(embedding.reshape(1, -1))
        
        # Update mappings
        self.assets[asset.id] = asset
        self.id_to_index[asset.id] = self.next_index
        self.index_to_id[self.next_index] = asset.id
        
        self.next_index += 1
        
        print(f"Added asset: {asset.name} (ID: {asset.id})")
    
    def search_assets(self, query: str, top_k: int = 10, min_score: float = 0.3) -> List[Tuple[DataAsset, float]]:
        """Search for assets using semantic similarity."""
        if self.index.ntotal == 0:
            return []
        
        # Create query embedding
        query_embedding = self.embedding_model.encode([query])
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding, min(top_k, self.index.ntotal))
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1 and score >= min_score:
                asset_id = self.index_to_id[idx]
                asset = self.assets[asset_id]
                results.append((asset, float(score)))
        
        return results
    
    def find_similar_assets(self, asset_id: str, top_k: int = 5) -> List[Tuple[DataAsset, float]]:
        """Find assets similar to a given asset."""
        if asset_id not in self.assets:
            return []
        
        asset = self.assets[asset_id]
        
        # Use asset information as query
        query_parts = [asset.name, asset.description] + asset.tags
        query = " ".join(query_parts)
        
        # Search and exclude the original asset
        results = self.search_assets(query, top_k + 1)
        return [(a, s) for a, s in results if a.id != asset_id][:top_k]
    
    def get_recommendations(self, user_query: str, user_context: Dict = None) -> Dict:
        """Get asset recommendations with explanations."""
        results = self.search_assets(user_query, top_k=10)
        
        if not results:
            return {
                'query': user_query,
                'recommendations': [],
                'total_found': 0
            }
        
        recommendations = []
        for asset, score in results:
            recommendation = {
                'asset': {
                    'id': asset.id,
                    'name': asset.name,
                    'description': asset.description,
                    'owner': asset.owner,
                    'tags': asset.tags,
                    'last_updated': asset.last_updated.isoformat()
                },
                'relevance_score': score,
                'explanation': self.generate_explanation(user_query, asset, score)
            }
            recommendations.append(recommendation)
        
        return {
            'query': user_query,
            'recommendations': recommendations,
            'total_found': len(results)
        }
    
    def generate_explanation(self, query: str, asset: DataAsset, score: float) -> str:
        """Generate explanation for why an asset was recommended."""
        explanations = []
        
        query_lower = query.lower()
        
        # Check name match
        if any(word in asset.name.lower() for word in query_lower.split()):
            explanations.append("name matches query terms")
        
        # Check description match
        if any(word in asset.description.lower() for word in query_lower.split()):
            explanations.append("description contains relevant terms")
        
        # Check tag match
        matching_tags = [tag for tag in asset.tags if any(word in tag.lower() for word in query_lower.split())]
        if matching_tags:
            explanations.append(f"tags match: {', '.join(matching_tags)}")
        
        # Score-based explanation
        if score > 0.8:
            explanations.append("high semantic similarity")
        elif score > 0.6:
            explanations.append("moderate semantic similarity")
        else:
            explanations.append("some semantic similarity")
        
        return "; ".join(explanations) if explanations else "semantic similarity detected"
    
    def save_catalog(self, filepath: str):
        """Save the catalog to disk."""
        # Save FAISS index
        faiss.write_index(self.index, f"{filepath}.index")
        
        # Save metadata
        metadata = {
            'assets': {aid: {
                'id': asset.id,
                'name': asset.name,
                'description': asset.description,
                'schema': asset.schema,
                'tags': asset.tags,
                'owner': asset.owner,
                'created_at': asset.created_at.isoformat(),
                'last_updated': asset.last_updated.isoformat()
            } for aid, asset in self.assets.items()},
            'id_to_index': self.id_to_index,
            'index_to_id': self.index_to_id,
            'next_index': self.next_index
        }
        
        with open(f"{filepath}.metadata", 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def load_catalog(self, filepath: str):
        """Load the catalog from disk."""
        # Load FAISS index
        self.index = faiss.read_index(f"{filepath}.index")
        
        # Load metadata
        with open(f"{filepath}.metadata", 'r') as f:
            metadata = json.load(f)
        
        # Reconstruct assets
        self.assets = {}
        for aid, asset_data in metadata['assets'].items():
            asset = DataAsset(
                id=asset_data['id'],
                name=asset_data['name'],
                description=asset_data['description'],
                schema=asset_data['schema'],
                tags=asset_data['tags'],
                owner=asset_data['owner'],
                created_at=datetime.fromisoformat(asset_data['created_at']),
                last_updated=datetime.fromisoformat(asset_data['last_updated'])
            )
            self.assets[aid] = asset
        
        self.id_to_index = metadata['id_to_index']
        self.index_to_id = {int(k): v for k, v in metadata['index_to_id'].items()}
        self.next_index = metadata['next_index']

# Usage example
catalog = SemanticDataCatalog()

# Add sample assets
assets = [
    DataAsset(
        id="customer_transactions",
        name="Customer Transaction Data",
        description="Daily customer transaction records with payment methods and amounts",
        schema={
            "columns": [
                {"name": "customer_id", "type": "integer", "description": "Unique customer identifier"},
                {"name": "transaction_date", "type": "date", "description": "Date of transaction"},
                {"name": "amount", "type": "decimal", "description": "Transaction amount in USD"},
                {"name": "payment_method", "type": "string", "description": "Payment method used"}
            ]
        },
        tags=["finance", "transactions", "customer", "daily"],
        owner="finance-team",
        created_at=datetime.now(),
        last_updated=datetime.now()
    ),
    DataAsset(
        id="user_behavior_logs",
        name="User Behavior Analytics",
        description="Web application user behavior tracking and clickstream data",
        schema={
            "columns": [
                {"name": "user_id", "type": "string", "description": "Anonymous user identifier"},
                {"name": "session_id", "type": "string", "description": "Session identifier"},
                {"name": "page_url", "type": "string", "description": "URL of visited page"},
                {"name": "timestamp", "type": "timestamp", "description": "Event timestamp"},
                {"name": "action", "type": "string", "description": "User action performed"}
            ]
        },
        tags=["web", "analytics", "behavior", "clickstream"],
        owner="analytics-team",
        created_at=datetime.now(),
        last_updated=datetime.now()
    )
]

for asset in assets:
    catalog.add_asset(asset)

# Search for assets
results = catalog.search_assets("customer payment data", top_k=5)
print("Search results:")
for asset, score in results:
    print(f"- {asset.name}: {score:.3f}")

# Get recommendations
recommendations = catalog.get_recommendations("financial transaction analysis")
print(f"\nRecommendations for 'financial transaction analysis':")
for rec in recommendations['recommendations']:
    print(f"- {rec['asset']['name']}: {rec['relevance_score']:.3f}")
    print(f"  Explanation: {rec['explanation']}")
```

These advanced AI concepts demonstrate how machine learning, generative AI, and semantic technologies can be integrated into data engineering workflows to create more intelligent, automated, and user-friendly data platforms.