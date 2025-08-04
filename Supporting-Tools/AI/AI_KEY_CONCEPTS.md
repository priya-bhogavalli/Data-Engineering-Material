# AI Key Concepts for Data Engineering

## 1. Machine Learning Fundamentals
**What it is**: Algorithms that enable computers to learn and make decisions from data without explicit programming.

**Why important**: ML is increasingly integrated into data pipelines for automated data quality checks, anomaly detection, predictive analytics, and intelligent data processing.

**When to use**:
- Automated data quality monitoring
- Predictive maintenance of data pipelines
- Intelligent data classification and routing
- Anomaly detection in data streams

**Types of Machine Learning**:
```python
# Supervised Learning Example - Data Quality Prediction
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd

class DataQualityPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
    
    def prepare_features(self, df):
        """Extract features for data quality prediction."""
        features = {
            'null_percentage': df.isnull().sum().sum() / (len(df) * len(df.columns)),
            'duplicate_percentage': df.duplicated().sum() / len(df),
            'numeric_columns_ratio': len(df.select_dtypes(include=['number']).columns) / len(df.columns),
            'row_count': len(df),
            'column_count': len(df.columns),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024
        }
        return pd.DataFrame([features])
    
    def train(self, training_data, quality_labels):
        """Train the data quality prediction model."""
        X_train, X_test, y_train, y_test = train_test_split(
            training_data, quality_labels, test_size=0.2, random_state=42
        )
        
        self.model.fit(X_train, y_train)
        accuracy = self.model.score(X_test, y_test)
        self.is_trained = True
        
        print(f"Model trained with accuracy: {accuracy:.2f}")
        return accuracy
    
    def predict_quality(self, df):
        """Predict data quality score."""
        if not self.is_trained:
            raise ValueError("Model must be trained first")
        
        features = self.prepare_features(df)
        quality_score = self.model.predict_proba(features)[0][1]  # Probability of good quality
        return quality_score

# Unsupervised Learning Example - Anomaly Detection
from sklearn.ensemble import IsolationForest
import numpy as np

class DataAnomalyDetector:
    def __init__(self, contamination=0.1):
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.is_fitted = False
    
    def fit(self, normal_data):
        """Fit the anomaly detection model on normal data."""
        self.model.fit(normal_data)
        self.is_fitted = True
    
    def detect_anomalies(self, data):
        """Detect anomalies in new data."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted first")
        
        anomaly_scores = self.model.decision_function(data)
        anomalies = self.model.predict(data)
        
        # -1 indicates anomaly, 1 indicates normal
        anomaly_indices = np.where(anomalies == -1)[0]
        
        return {
            'anomaly_indices': anomaly_indices,
            'anomaly_scores': anomaly_scores,
            'anomaly_count': len(anomaly_indices)
        }

# Usage in data pipeline
def ml_enhanced_data_pipeline(df):
    """Data pipeline with ML-based quality checks and anomaly detection."""
    
    # 1. Predict data quality
    quality_predictor = DataQualityPredictor()
    # Assume model is pre-trained
    quality_score = quality_predictor.predict_quality(df)
    
    if quality_score < 0.8:
        print(f"Warning: Low data quality predicted (score: {quality_score:.2f})")
    
    # 2. Detect anomalies
    anomaly_detector = DataAnomalyDetector()
    # Fit on historical normal data (assume available)
    numeric_data = df.select_dtypes(include=[np.number])
    
    if len(numeric_data.columns) > 0:
        anomalies = anomaly_detector.detect_anomalies(numeric_data)
        
        if anomalies['anomaly_count'] > 0:
            print(f"Detected {anomalies['anomaly_count']} anomalies")
            # Handle anomalies (flag, remove, or investigate)
            df_clean = df.drop(df.index[anomalies['anomaly_indices']])
            return df_clean
    
    return df
```

## 2. Generative AI and Large Language Models
**What it is**: AI systems that can generate human-like text, code, and other content based on prompts and training data.

**Why important**: GenAI can automate documentation generation, code creation, data analysis explanations, and intelligent data processing workflows.

**When to use**:
- Automated documentation generation for data pipelines
- Code generation for data transformations
- Natural language queries to data
- Intelligent data summarization and reporting

**LLM Integration Examples**:
```python
import openai
from typing import Dict, List, Any
import json

class DataPipelineAssistant:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.model = "gpt-4"
    
    def generate_data_documentation(self, schema: Dict, sample_data: Dict) -> str:
        """Generate documentation for a dataset."""
        prompt = f"""
        Generate comprehensive documentation for a dataset with the following schema and sample data:
        
        Schema: {json.dumps(schema, indent=2)}
        Sample Data: {json.dumps(sample_data, indent=2)}
        
        Include:
        1. Dataset overview
        2. Column descriptions
        3. Data types and constraints
        4. Potential use cases
        5. Data quality considerations
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a data engineering expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    def generate_sql_from_description(self, description: str, table_schema: Dict) -> str:
        """Generate SQL query from natural language description."""
        prompt = f"""
        Generate a SQL query based on this description: "{description}"
        
        Available table schema:
        {json.dumps(table_schema, indent=2)}
        
        Return only the SQL query, properly formatted.
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a SQL expert. Generate only valid SQL queries."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.1
        )
        
        return response.choices[0].message.content.strip()
    
    def explain_data_anomaly(self, anomaly_data: Dict, context: str) -> str:
        """Generate explanation for detected data anomalies."""
        prompt = f"""
        Analyze this data anomaly and provide a detailed explanation:
        
        Anomaly Data: {json.dumps(anomaly_data, indent=2)}
        Context: {context}
        
        Provide:
        1. Possible causes
        2. Impact assessment
        3. Recommended actions
        4. Prevention strategies
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a data quality expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.4
        )
        
        return response.choices[0].message.content

# Usage example
assistant = DataPipelineAssistant("your-api-key")

# Generate documentation
schema = {
    "customer_id": {"type": "integer", "primary_key": True},
    "name": {"type": "string", "max_length": 100},
    "email": {"type": "string", "unique": True},
    "created_at": {"type": "timestamp"}
}

sample_data = {
    "customer_id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2024-01-15T10:30:00Z"
}

documentation = assistant.generate_data_documentation(schema, sample_data)
print(documentation)
```

## 3. Vector Databases and Embeddings
**What it is**: Specialized databases for storing and querying high-dimensional vector representations of data, enabling semantic search and similarity matching.

**Why important**: Vector databases enable semantic search over data catalogs, intelligent data discovery, and similarity-based data matching for data engineering workflows.

**When to use**:
- Semantic search in data catalogs
- Similar dataset discovery
- Intelligent data matching and deduplication
- Content-based data classification

**Vector Database Implementation**:
```python
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import pickle
from typing import List, Dict, Tuple

class DataCatalogVectorDB:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity
        self.metadata = []
        self.is_trained = False
    
    def add_dataset(self, dataset_info: Dict):
        """Add a dataset to the vector database."""
        # Create text representation of dataset
        text_repr = self._create_dataset_text(dataset_info)
        
        # Generate embedding
        embedding = self.model.encode([text_repr])
        
        # Normalize for cosine similarity
        faiss.normalize_L2(embedding)
        
        # Add to index
        self.index.add(embedding)
        self.metadata.append(dataset_info)
        
        print(f"Added dataset: {dataset_info.get('name', 'Unknown')}")
    
    def _create_dataset_text(self, dataset_info: Dict) -> str:
        """Create text representation of dataset for embedding."""
        parts = []
        
        if 'name' in dataset_info:
            parts.append(f"Dataset name: {dataset_info['name']}")
        
        if 'description' in dataset_info:
            parts.append(f"Description: {dataset_info['description']}")
        
        if 'columns' in dataset_info:
            columns_text = ", ".join(dataset_info['columns'])
            parts.append(f"Columns: {columns_text}")
        
        if 'tags' in dataset_info:
            tags_text = ", ".join(dataset_info['tags'])
            parts.append(f"Tags: {tags_text}")
        
        return " | ".join(parts)
    
    def search_similar_datasets(self, query: str, top_k: int = 5) -> List[Tuple[Dict, float]]:
        """Search for similar datasets based on query."""
        if self.index.ntotal == 0:
            return []
        
        # Generate query embedding
        query_embedding = self.model.encode([query])
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding, min(top_k, self.index.ntotal))
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1:  # Valid index
                results.append((self.metadata[idx], float(score)))
        
        return results
    
    def find_similar_datasets(self, dataset_name: str, top_k: int = 5) -> List[Tuple[Dict, float]]:
        """Find datasets similar to a given dataset."""
        # Find the dataset
        target_dataset = None
        for dataset in self.metadata:
            if dataset.get('name') == dataset_name:
                target_dataset = dataset
                break
        
        if not target_dataset:
            return []
        
        # Use dataset description as query
        query = self._create_dataset_text(target_dataset)
        return self.search_similar_datasets(query, top_k + 1)[1:]  # Exclude self
    
    def save_index(self, filepath: str):
        """Save the vector index and metadata."""
        faiss.write_index(self.index, f"{filepath}.index")
        with open(f"{filepath}.metadata", 'wb') as f:
            pickle.dump(self.metadata, f)
    
    def load_index(self, filepath: str):
        """Load the vector index and metadata."""
        self.index = faiss.read_index(f"{filepath}.index")
        with open(f"{filepath}.metadata", 'rb') as f:
            self.metadata = pickle.load(f)

# Usage example
vector_db = DataCatalogVectorDB()

# Add datasets to the catalog
datasets = [
    {
        "name": "customer_transactions",
        "description": "Daily customer transaction data with payment methods and amounts",
        "columns": ["customer_id", "transaction_date", "amount", "payment_method"],
        "tags": ["finance", "transactions", "daily"]
    },
    {
        "name": "user_behavior_logs",
        "description": "Web application user behavior and click stream data",
        "columns": ["user_id", "session_id", "page_url", "timestamp", "action"],
        "tags": ["web", "behavior", "clickstream"]
    },
    {
        "name": "product_sales_data",
        "description": "Product sales information with categories and revenue",
        "columns": ["product_id", "category", "sales_amount", "quantity", "date"],
        "tags": ["sales", "products", "revenue"]
    }
]

for dataset in datasets:
    vector_db.add_dataset(dataset)

# Search for similar datasets
results = vector_db.search_similar_datasets("financial transaction data", top_k=3)
print("Similar datasets:")
for dataset, score in results:
    print(f"- {dataset['name']}: {score:.3f}")
```

## 4. MLOps for Data Engineering
**What it is**: Practices and tools for deploying, monitoring, and maintaining machine learning models in production data pipelines.

**Why important**: MLOps ensures ML models integrated into data pipelines are reliable, maintainable, and can be updated safely without disrupting data flows.

**When to use**:
- ML models for data quality monitoring
- Predictive data pipeline scaling
- Automated data classification
- Real-time anomaly detection in streams

**MLOps Pipeline Implementation**:
```python
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
import joblib
import pandas as pd
from datetime import datetime
import logging

class MLModelManager:
    def __init__(self, experiment_name: str, model_name: str):
        self.experiment_name = experiment_name
        self.model_name = model_name
        self.client = MlflowClient()
        
        # Set up MLflow experiment
        try:
            experiment = mlflow.get_experiment_by_name(experiment_name)
            if experiment is None:
                mlflow.create_experiment(experiment_name)
        except Exception:
            mlflow.create_experiment(experiment_name)
        
        mlflow.set_experiment(experiment_name)
    
    def train_and_register_model(self, X_train, y_train, X_test, y_test, model, model_params=None):
        """Train model and register in MLflow."""
        with mlflow.start_run() as run:
            # Log parameters
            if model_params:
                mlflow.log_params(model_params)
            
            # Train model
            model.fit(X_train, y_train)
            
            # Evaluate model
            train_score = model.score(X_train, y_train)
            test_score = model.score(X_test, y_test)
            
            # Log metrics
            mlflow.log_metric("train_accuracy", train_score)
            mlflow.log_metric("test_accuracy", test_score)
            
            # Log model
            mlflow.sklearn.log_model(
                model, 
                "model",
                registered_model_name=self.model_name
            )
            
            print(f"Model registered with run_id: {run.info.run_id}")
            return run.info.run_id
    
    def promote_model_to_production(self, model_version: str):
        """Promote model version to production stage."""
        self.client.transition_model_version_stage(
            name=self.model_name,
            version=model_version,
            stage="Production"
        )
        print(f"Model version {model_version} promoted to Production")
    
    def load_production_model(self):
        """Load the current production model."""
        model_version = self.client.get_latest_versions(
            self.model_name, 
            stages=["Production"]
        )[0]
        
        model_uri = f"models:/{self.model_name}/{model_version.version}"
        model = mlflow.sklearn.load_model(model_uri)
        
        return model, model_version.version
    
    def monitor_model_performance(self, model, X_test, y_test, threshold=0.8):
        """Monitor model performance and trigger retraining if needed."""
        current_score = model.score(X_test, y_test)
        
        # Log monitoring metrics
        with mlflow.start_run():
            mlflow.log_metric("monitoring_accuracy", current_score)
            mlflow.log_metric("monitoring_timestamp", datetime.now().timestamp())
        
        if current_score < threshold:
            print(f"Model performance degraded: {current_score:.3f} < {threshold}")
            return False  # Trigger retraining
        
        return True  # Model performing well

class DataPipelineMLIntegration:
    def __init__(self, model_manager: MLModelManager):
        self.model_manager = model_manager
        self.model = None
        self.model_version = None
        self._load_model()
    
    def _load_model(self):
        """Load the production model."""
        try:
            self.model, self.model_version = self.model_manager.load_production_model()
            print(f"Loaded model version: {self.model_version}")
        except Exception as e:
            print(f"Failed to load model: {e}")
            self.model = None
    
    def process_data_with_ml(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process data using ML model for quality scoring."""
        if self.model is None:
            print("No model available, skipping ML processing")
            return df
        
        try:
            # Prepare features (simplified example)
            features = self._extract_features(df)
            
            # Predict data quality
            quality_scores = self.model.predict_proba(features)[:, 1]
            
            # Add quality scores to dataframe
            df['ml_quality_score'] = quality_scores
            
            # Filter based on quality threshold
            high_quality_data = df[df['ml_quality_score'] > 0.7]
            
            print(f"ML filtering: {len(df)} -> {len(high_quality_data)} records")
            return high_quality_data
            
        except Exception as e:
            print(f"ML processing failed: {e}")
            return df  # Return original data if ML fails
    
    def _extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extract features for ML model."""
        features = {
            'null_percentage': [df.isnull().sum().sum() / (len(df) * len(df.columns))],
            'duplicate_percentage': [df.duplicated().sum() / len(df)],
            'numeric_ratio': [len(df.select_dtypes(include=['number']).columns) / len(df.columns)],
            'row_count': [len(df)],
            'column_count': [len(df.columns)]
        }
        return pd.DataFrame(features)

# Usage example
model_manager = MLModelManager("data_quality_experiment", "data_quality_model")

# In production data pipeline
ml_integration = DataPipelineMLIntegration(model_manager)

def enhanced_data_pipeline(raw_data: pd.DataFrame) -> pd.DataFrame:
    """Data pipeline enhanced with ML capabilities."""
    
    # Standard data processing
    cleaned_data = raw_data.dropna()
    
    # ML-enhanced processing
    ml_processed_data = ml_integration.process_data_with_ml(cleaned_data)
    
    # Continue with rest of pipeline
    return ml_processed_data
```

## 5. Retrieval-Augmented Generation (RAG)
**What it is**: AI technique that combines retrieval of relevant information with generative models to produce more accurate and contextual responses.

**Why important**: RAG enables intelligent data discovery, automated documentation generation with context, and smart data pipeline assistance based on organizational knowledge.

**When to use**:
- Intelligent data catalog search
- Context-aware documentation generation
- Data pipeline troubleshooting assistance
- Automated data governance recommendations

**RAG Implementation for Data Engineering**:
```python
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Dict, Tuple
import openai

class DataEngineeringRAG:
    def __init__(self, openai_api_key: str, embedding_model: str = 'all-MiniLM-L6-v2'):
        self.embedding_model = SentenceTransformer(embedding_model)
        self.openai_api_key = openai_api_key
        openai.api_key = openai_api_key
        
        # Initialize vector store
        self.dimension = self.embedding_model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatIP(self.dimension)
        self.documents = []
        self.metadata = []
    
    def add_knowledge_document(self, content: str, metadata: Dict):
        """Add a knowledge document to the RAG system."""
        # Create embedding
        embedding = self.embedding_model.encode([content])
        faiss.normalize_L2(embedding)
        
        # Add to index
        self.index.add(embedding)
        self.documents.append(content)
        self.metadata.append(metadata)
    
    def retrieve_relevant_docs(self, query: str, top_k: int = 3) -> List[Tuple[str, Dict, float]]:
        """Retrieve relevant documents for a query."""
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
    
    def generate_answer(self, question: str, max_tokens: int = 500) -> str:
        """Generate answer using RAG approach."""
        # Retrieve relevant documents
        relevant_docs = self.retrieve_relevant_docs(question, top_k=3)
        
        if not relevant_docs:
            return "I don't have enough information to answer this question."
        
        # Prepare context from retrieved documents
        context = "\n\n".join([
            f"Document {i+1} (relevance: {score:.3f}):\n{doc}"
            for i, (doc, metadata, score) in enumerate(relevant_docs)
        ])
        
        # Generate answer using GPT
        prompt = f"""
        Based on the following context documents, answer the question about data engineering:

        Context:
        {context}

        Question: {question}

        Please provide a comprehensive answer based on the context provided. If the context doesn't contain enough information, say so.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a data engineering expert assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.3
        )
        
        return response.choices[0].message.content

# Initialize RAG system with data engineering knowledge
rag_system = DataEngineeringRAG("your-openai-api-key")

# Add knowledge documents
knowledge_docs = [
    {
        "content": """
        Apache Spark is a unified analytics engine for large-scale data processing. 
        It provides high-level APIs in Java, Scala, Python and R, and an optimized engine 
        that supports general execution graphs. Key features include:
        - In-memory computing for faster processing
        - Support for batch and streaming data
        - Machine learning library (MLlib)
        - Graph processing with GraphX
        - SQL support with Spark SQL
        """,
        "metadata": {"topic": "spark", "type": "overview"}
    },
    {
        "content": """
        Data quality issues in pipelines can be addressed through:
        1. Schema validation at ingestion
        2. Null value checks and handling
        3. Duplicate detection and removal
        4. Data type validation
        5. Range and constraint checks
        6. Referential integrity validation
        7. Statistical anomaly detection
        8. Data lineage tracking for root cause analysis
        """,
        "metadata": {"topic": "data_quality", "type": "best_practices"}
    },
    {
        "content": """
        Common Spark performance optimization techniques:
        - Use appropriate file formats (Parquet, Delta)
        - Partition data effectively
        - Cache frequently accessed datasets
        - Optimize join strategies (broadcast joins for small tables)
        - Tune Spark configuration parameters
        - Use columnar storage formats
        - Minimize shuffles through proper partitioning
        - Use appropriate cluster sizing
        """,
        "metadata": {"topic": "spark_optimization", "type": "performance"}
    }
]

for doc in knowledge_docs:
    rag_system.add_knowledge_document(doc["content"], doc["metadata"])

# Example usage
question = "How can I optimize Spark performance for large datasets?"
answer = rag_system.generate_answer(question)
print(f"Question: {question}")
print(f"Answer: {answer}")
```

These AI concepts provide powerful capabilities for enhancing data engineering workflows through intelligent automation, semantic understanding, and context-aware assistance, making data pipelines more robust, efficient, and maintainable.