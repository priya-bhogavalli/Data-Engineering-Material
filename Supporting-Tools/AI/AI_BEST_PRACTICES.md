# AI Best Practices for Data Engineering

## 1. ML Model Integration in Data Pipelines

### Model Versioning and Management
```python
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
import joblib
from datetime import datetime

class ModelManager:
    def __init__(self, experiment_name: str, model_name: str):
        self.experiment_name = experiment_name
        self.model_name = model_name
        self.client = MlflowClient()
        mlflow.set_experiment(experiment_name)
    
    def register_model(self, model, metrics: dict, params: dict):
        """Register model with proper versioning."""
        with mlflow.start_run() as run:
            # Log parameters and metrics
            mlflow.log_params(params)
            mlflow.log_metrics(metrics)
            
            # Log model with metadata
            mlflow.sklearn.log_model(
                model,
                "model",
                registered_model_name=self.model_name,
                metadata={
                    "training_date": datetime.now().isoformat(),
                    "data_version": params.get("data_version", "unknown"),
                    "purpose": "data_quality_prediction"
                }
            )
            
            return run.info.run_id
    
    def load_production_model(self):
        """Load current production model safely."""
        try:
            model_version = self.client.get_latest_versions(
                self.model_name, 
                stages=["Production"]
            )[0]
            
            model_uri = f"models:/{self.model_name}/{model_version.version}"
            model = mlflow.sklearn.load_model(model_uri)
            
            return model, model_version.version
        except Exception as e:
            print(f"Failed to load production model: {e}")
            return None, None
```

### Graceful Degradation
```python
class RobustMLPipeline:
    def __init__(self, model_manager: ModelManager):
        self.model_manager = model_manager
        self.model = None
        self.fallback_rules = self._load_fallback_rules()
        self._load_model()
    
    def _load_model(self):
        """Load model with error handling."""
        try:
            self.model, self.version = self.model_manager.load_production_model()
            if self.model:
                print(f"Loaded model version: {self.version}")
        except Exception as e:
            print(f"Model loading failed: {e}")
            self.model = None
    
    def process_data(self, df):
        """Process data with graceful degradation."""
        if self.model is not None:
            try:
                return self._ml_processing(df)
            except Exception as e:
                print(f"ML processing failed: {e}, falling back to rules")
                return self._rule_based_processing(df)
        else:
            print("No ML model available, using rule-based processing")
            return self._rule_based_processing(df)
    
    def _ml_processing(self, df):
        """ML-based data processing."""
        features = self._extract_features(df)
        quality_scores = self.model.predict_proba(features)[:, 1]
        
        # Apply ML-based filtering
        high_quality_mask = quality_scores > 0.8
        return df[high_quality_mask]
    
    def _rule_based_processing(self, df):
        """Fallback rule-based processing."""
        # Apply basic quality rules
        clean_df = df.dropna(subset=self.fallback_rules['required_columns'])
        clean_df = clean_df[clean_df['amount'] > 0]  # Business rule
        return clean_df
    
    def _load_fallback_rules(self):
        """Load fallback business rules."""
        return {
            'required_columns': ['customer_id', 'amount', 'date'],
            'min_amount': 0,
            'max_null_percentage': 0.1
        }
```

## 2. Data Quality with ML

### Automated Anomaly Detection
```python
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd

class DataQualityMonitor:
    def __init__(self, contamination=0.1):
        self.anomaly_detector = IsolationForest(
            contamination=contamination,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.is_fitted = False
        self.baseline_stats = {}
    
    def fit_baseline(self, df):
        """Establish baseline from historical good data."""
        # Extract quality features
        features = self._extract_quality_features(df)
        
        # Fit scaler and anomaly detector
        features_scaled = self.scaler.fit_transform(features)
        self.anomaly_detector.fit(features_scaled)
        
        # Store baseline statistics
        self.baseline_stats = {
            'row_count_mean': len(df),
            'null_percentage_mean': df.isnull().sum().sum() / (len(df) * len(df.columns)),
            'duplicate_percentage_mean': df.duplicated().sum() / len(df)
        }
        
        self.is_fitted = True
        print("Baseline established for data quality monitoring")
    
    def check_data_quality(self, df):
        """Check data quality and detect anomalies."""
        if not self.is_fitted:
            raise ValueError("Must fit baseline first")
        
        # Extract features
        features = self._extract_quality_features(df)
        features_scaled = self.scaler.transform(features)
        
        # Detect anomalies
        anomaly_scores = self.anomaly_detector.decision_function(features_scaled)
        is_anomaly = self.anomaly_detector.predict(features_scaled)[0] == -1
        
        # Calculate quality metrics
        quality_report = {
            'is_anomaly': is_anomaly,
            'anomaly_score': anomaly_scores[0],
            'row_count': len(df),
            'null_percentage': df.isnull().sum().sum() / (len(df) * len(df.columns)),
            'duplicate_percentage': df.duplicated().sum() / len(df),
            'schema_changes': self._detect_schema_changes(df),
            'quality_score': self._calculate_quality_score(df)
        }
        
        return quality_report
    
    def _extract_quality_features(self, df):
        """Extract features for quality assessment."""
        features = np.array([[
            len(df),  # Row count
            df.isnull().sum().sum() / (len(df) * len(df.columns)),  # Null percentage
            df.duplicated().sum() / len(df),  # Duplicate percentage
            len(df.columns),  # Column count
            len(df.select_dtypes(include=[np.number]).columns) / len(df.columns),  # Numeric ratio
            df.memory_usage(deep=True).sum() / 1024 / 1024  # Memory usage MB
        ]])
        
        return features
    
    def _calculate_quality_score(self, df):
        """Calculate overall quality score (0-100)."""
        null_penalty = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 50
        duplicate_penalty = (df.duplicated().sum() / len(df)) * 30
        
        base_score = 100
        quality_score = max(0, base_score - null_penalty - duplicate_penalty)
        
        return quality_score
```

### Predictive Data Quality
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd

class PredictiveQualityAssessment:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.feature_columns = [
            'source_system', 'file_size_mb', 'record_count', 
            'null_percentage', 'duplicate_percentage', 'schema_version'
        ]
        self.is_trained = False
    
    def train_quality_predictor(self, historical_data, quality_labels):
        """Train model to predict data quality issues."""
        # Prepare features
        X = historical_data[self.feature_columns]
        y = quality_labels  # 1 = good quality, 0 = poor quality
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate
        train_accuracy = self.model.score(X_train, y_train)
        test_accuracy = self.model.score(X_test, y_test)
        
        print(f"Quality prediction model trained:")
        print(f"Train accuracy: {train_accuracy:.3f}")
        print(f"Test accuracy: {test_accuracy:.3f}")
        
        self.is_trained = True
        return test_accuracy
    
    def predict_quality_issues(self, data_metadata):
        """Predict potential quality issues before processing."""
        if not self.is_trained:
            raise ValueError("Model must be trained first")
        
        # Prepare features
        features = pd.DataFrame([data_metadata])[self.feature_columns]
        
        # Predict
        quality_probability = self.model.predict_proba(features)[0][1]
        predicted_issues = self.model.predict(features)[0] == 0
        
        # Get feature importance for explanation
        feature_importance = dict(zip(
            self.feature_columns,
            self.model.feature_importances_
        ))
        
        return {
            'quality_probability': quality_probability,
            'predicted_issues': predicted_issues,
            'confidence': max(quality_probability, 1 - quality_probability),
            'important_features': sorted(
                feature_importance.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:3]
        }
```

## 3. GenAI Integration Best Practices

### Prompt Engineering for Data Tasks
```python
import openai
from typing import Dict, List, Optional
import json

class DataEngineeringAssistant:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.model = "gpt-4"
        self.system_prompts = self._load_system_prompts()
    
    def _load_system_prompts(self):
        """Load specialized system prompts for different tasks."""
        return {
            'sql_generation': """
            You are an expert SQL developer. Generate efficient, readable SQL queries.
            Always include comments explaining complex logic.
            Use appropriate indexes and optimization techniques.
            Follow SQL best practices and naming conventions.
            """,
            'documentation': """
            You are a technical documentation expert specializing in data engineering.
            Create comprehensive, clear documentation with examples.
            Include code snippets, diagrams descriptions, and best practices.
            Structure content with proper headings and formatting.
            """,
            'troubleshooting': """
            You are a data engineering troubleshooting expert.
            Analyze problems systematically and provide step-by-step solutions.
            Consider multiple root causes and provide preventive measures.
            Include monitoring and alerting recommendations.
            """
        }
    
    def generate_sql_query(self, description: str, schema: Dict, constraints: Optional[Dict] = None) -> str:
        """Generate SQL query from natural language description."""
        constraints_text = ""
        if constraints:
            constraints_text = f"\nConstraints: {json.dumps(constraints, indent=2)}"
        
        prompt = f"""
        Generate a SQL query for: {description}
        
        Available schema:
        {json.dumps(schema, indent=2)}
        {constraints_text}
        
        Requirements:
        1. Use proper SQL formatting and indentation
        2. Include comments for complex logic
        3. Optimize for performance
        4. Handle edge cases (nulls, empty results)
        5. Use appropriate joins and indexes
        
        Return only the SQL query with comments.
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompts['sql_generation']},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.1
        )
        
        return response.choices[0].message.content.strip()
    
    def generate_documentation(self, code: str, context: str) -> str:
        """Generate documentation for data engineering code."""
        prompt = f"""
        Generate comprehensive documentation for this data engineering code:
        
        Code:
        ```
        {code}
        ```
        
        Context: {context}
        
        Include:
        1. Overview and purpose
        2. Input/output specifications
        3. Key functions and their roles
        4. Configuration parameters
        5. Error handling approach
        6. Performance considerations
        7. Usage examples
        8. Troubleshooting guide
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompts['documentation']},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    def troubleshoot_pipeline_issue(self, error_description: str, logs: str, context: Dict) -> str:
        """Provide troubleshooting guidance for pipeline issues."""
        prompt = f"""
        Analyze this data pipeline issue and provide troubleshooting guidance:
        
        Error Description: {error_description}
        
        Recent Logs:
        {logs}
        
        Pipeline Context:
        {json.dumps(context, indent=2)}
        
        Provide:
        1. Root cause analysis
        2. Step-by-step troubleshooting steps
        3. Immediate fixes
        4. Long-term prevention strategies
        5. Monitoring improvements
        6. Code examples if applicable
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompts['troubleshooting']},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1200,
            temperature=0.4
        )
        
        return response.choices[0].message.content
```

### Safe AI Integration
```python
import re
import ast
from typing import Any, Dict, List

class SafeAIIntegration:
    def __init__(self):
        self.sql_injection_patterns = [
            r";\s*(drop|delete|truncate|alter)\s+",
            r"union\s+select",
            r"--\s*$",
            r"/\*.*\*/"
        ]
        self.allowed_sql_keywords = {
            'select', 'from', 'where', 'group by', 'order by', 
            'having', 'join', 'inner', 'left', 'right', 'on',
            'and', 'or', 'in', 'not', 'like', 'between'
        }
    
    def validate_generated_sql(self, sql: str) -> Dict[str, Any]:
        """Validate AI-generated SQL for safety."""
        validation_result = {
            'is_safe': True,
            'issues': [],
            'warnings': []
        }
        
        # Check for SQL injection patterns
        for pattern in self.sql_injection_patterns:
            if re.search(pattern, sql.lower()):
                validation_result['is_safe'] = False
                validation_result['issues'].append(f"Potential SQL injection pattern: {pattern}")
        
        # Check for dangerous keywords
        dangerous_keywords = ['drop', 'delete', 'truncate', 'alter', 'create', 'insert', 'update']
        for keyword in dangerous_keywords:
            if re.search(rf'\b{keyword}\b', sql.lower()):
                validation_result['is_safe'] = False
                validation_result['issues'].append(f"Dangerous keyword detected: {keyword}")
        
        # Check for proper structure
        if not re.search(r'\bselect\b', sql.lower()):
            validation_result['warnings'].append("Query doesn't appear to be a SELECT statement")
        
        return validation_result
    
    def sanitize_ai_output(self, output: str, output_type: str = 'text') -> str:
        """Sanitize AI-generated output."""
        if output_type == 'sql':
            # Remove comments that might contain injection
            output = re.sub(r'--.*$', '', output, flags=re.MULTILINE)
            output = re.sub(r'/\*.*?\*/', '', output, flags=re.DOTALL)
            
            # Validate and clean
            validation = self.validate_generated_sql(output)
            if not validation['is_safe']:
                raise ValueError(f"Unsafe SQL generated: {validation['issues']}")
        
        elif output_type == 'python':
            # Basic Python code validation
            try:
                ast.parse(output)
            except SyntaxError as e:
                raise ValueError(f"Invalid Python syntax: {e}")
        
        return output.strip()
    
    def rate_limit_ai_calls(self, user_id: str, max_calls_per_hour: int = 100) -> bool:
        """Implement rate limiting for AI API calls."""
        # Implementation would use Redis or similar for tracking
        # This is a simplified example
        current_calls = self.get_user_call_count(user_id)
        
        if current_calls >= max_calls_per_hour:
            return False
        
        self.increment_user_call_count(user_id)
        return True
```

## 4. Vector Database Best Practices

### Efficient Embedding Management
```python
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import pickle
from typing import List, Dict, Tuple, Optional

class OptimizedVectorStore:
    def __init__(self, dimension: int, index_type: str = 'flat'):
        self.dimension = dimension
        self.index_type = index_type
        self.index = self._create_index()
        self.metadata = []
        self.id_mapping = {}
        self.next_id = 0
    
    def _create_index(self):
        """Create appropriate FAISS index based on requirements."""
        if self.index_type == 'flat':
            # Exact search, good for small datasets
            return faiss.IndexFlatIP(self.dimension)
        elif self.index_type == 'ivf':
            # Approximate search, good for large datasets
            quantizer = faiss.IndexFlatIP(self.dimension)
            return faiss.IndexIVFFlat(quantizer, self.dimension, 100)
        elif self.index_type == 'hnsw':
            # Hierarchical NSW, good balance of speed and accuracy
            return faiss.IndexHNSWFlat(self.dimension, 32)
        else:
            raise ValueError(f"Unsupported index type: {self.index_type}")
    
    def add_embeddings(self, embeddings: np.ndarray, metadata: List[Dict]) -> List[int]:
        """Add embeddings with metadata efficiently."""
        if len(embeddings) != len(metadata):
            raise ValueError("Embeddings and metadata must have same length")
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Add to index
        if self.index_type == 'ivf' and not self.index.is_trained:
            # Train IVF index if needed
            if len(embeddings) >= 100:  # Minimum training data
                self.index.train(embeddings)
        
        self.index.add(embeddings)
        
        # Store metadata and create ID mapping
        ids = []
        for meta in metadata:
            self.metadata.append(meta)
            self.id_mapping[self.next_id] = len(self.metadata) - 1
            ids.append(self.next_id)
            self.next_id += 1
        
        return ids
    
    def search(self, query_embedding: np.ndarray, top_k: int = 10, 
               min_score: float = 0.0) -> List[Tuple[Dict, float, int]]:
        """Search for similar embeddings."""
        # Normalize query
        query_embedding = query_embedding.reshape(1, -1)
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1 and score >= min_score:
                metadata_idx = self.id_mapping.get(idx, idx)
                if metadata_idx < len(self.metadata):
                    results.append((
                        self.metadata[metadata_idx],
                        float(score),
                        int(idx)
                    ))
        
        return results
    
    def update_metadata(self, vector_id: int, new_metadata: Dict):
        """Update metadata for a specific vector."""
        if vector_id in self.id_mapping:
            metadata_idx = self.id_mapping[vector_id]
            self.metadata[metadata_idx] = new_metadata
        else:
            raise ValueError(f"Vector ID {vector_id} not found")
    
    def save_index(self, filepath: str):
        """Save index and metadata to disk."""
        # Save FAISS index
        faiss.write_index(self.index, f"{filepath}.index")
        
        # Save metadata and mappings
        with open(f"{filepath}.metadata", 'wb') as f:
            pickle.dump({
                'metadata': self.metadata,
                'id_mapping': self.id_mapping,
                'next_id': self.next_id,
                'dimension': self.dimension,
                'index_type': self.index_type
            }, f)
    
    def load_index(self, filepath: str):
        """Load index and metadata from disk."""
        # Load FAISS index
        self.index = faiss.read_index(f"{filepath}.index")
        
        # Load metadata and mappings
        with open(f"{filepath}.metadata", 'rb') as f:
            data = pickle.load(f)
            self.metadata = data['metadata']
            self.id_mapping = data['id_mapping']
            self.next_id = data['next_id']
            self.dimension = data['dimension']
            self.index_type = data['index_type']
```

### Embedding Quality Monitoring
```python
class EmbeddingQualityMonitor:
    def __init__(self, embedding_model: SentenceTransformer):
        self.embedding_model = embedding_model
        self.quality_metrics = {}
    
    def assess_embedding_quality(self, texts: List[str], embeddings: np.ndarray) -> Dict:
        """Assess quality of generated embeddings."""
        metrics = {}
        
        # 1. Dimensionality check
        metrics['dimension_consistency'] = all(
            emb.shape[0] == self.embedding_model.get_sentence_embedding_dimension() 
            for emb in embeddings
        )
        
        # 2. Magnitude distribution
        magnitudes = np.linalg.norm(embeddings, axis=1)
        metrics['magnitude_stats'] = {
            'mean': float(np.mean(magnitudes)),
            'std': float(np.std(magnitudes)),
            'min': float(np.min(magnitudes)),
            'max': float(np.max(magnitudes))
        }
        
        # 3. Similarity distribution
        if len(embeddings) > 1:
            similarity_matrix = np.dot(embeddings, embeddings.T)
            upper_triangle = similarity_matrix[np.triu_indices_from(similarity_matrix, k=1)]
            
            metrics['similarity_stats'] = {
                'mean': float(np.mean(upper_triangle)),
                'std': float(np.std(upper_triangle)),
                'min': float(np.min(upper_triangle)),
                'max': float(np.max(upper_triangle))
            }
        
        # 4. Text-embedding alignment check
        if len(texts) == len(embeddings):
            # Check if similar texts have similar embeddings
            text_similarities = self._calculate_text_similarities(texts)
            embedding_similarities = self._calculate_embedding_similarities(embeddings)
            
            correlation = np.corrcoef(text_similarities, embedding_similarities)[0, 1]
            metrics['text_embedding_correlation'] = float(correlation)
        
        return metrics
    
    def _calculate_text_similarities(self, texts: List[str]) -> List[float]:
        """Calculate pairwise text similarities using simple metrics."""
        similarities = []
        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                # Simple Jaccard similarity on words
                words_i = set(texts[i].lower().split())
                words_j = set(texts[j].lower().split())
                
                intersection = len(words_i & words_j)
                union = len(words_i | words_j)
                
                similarity = intersection / union if union > 0 else 0
                similarities.append(similarity)
        
        return similarities
    
    def _calculate_embedding_similarities(self, embeddings: np.ndarray) -> List[float]:
        """Calculate pairwise embedding similarities."""
        similarities = []
        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                similarity = np.dot(embeddings[i], embeddings[j])
                similarities.append(similarity)
        
        return similarities
```

These best practices ensure robust, secure, and efficient integration of AI capabilities into data engineering workflows, covering model management, quality monitoring, safe AI usage, and optimized vector operations.