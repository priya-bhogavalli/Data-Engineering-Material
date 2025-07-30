# Embeddings Key Concepts

## 1. Vector Representations of Data
**What it is**: Dense numerical representations that capture semantic meaning of text, images, or other data in high-dimensional space.

**Core Properties**:
- **Dense Vectors**: Typically 100-1536 dimensions
- **Semantic Similarity**: Similar items have similar vectors
- **Mathematical Operations**: Support arithmetic operations
- **Distance Metrics**: Measurable similarity/dissimilarity

## 2. Types of Embeddings
**Text Embeddings**:
```python
# Word-level embeddings
word2vec: Skip-gram and CBOW models
GloVe: Global vectors for word representation
FastText: Subword information included

# Sentence/Document embeddings
Sentence-BERT: Sentence-level semantic representations
Universal Sentence Encoder: Google's sentence embeddings
OpenAI text-embedding-ada-002: Latest text embeddings
```

**Contextual Embeddings**:
```python
from transformers import AutoTokenizer, AutoModel
import torch

# BERT embeddings
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
model = AutoModel.from_pretrained('bert-base-uncased')

def get_bert_embeddings(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Use [CLS] token embedding for sentence representation
    sentence_embedding = outputs.last_hidden_state[:, 0, :]
    return sentence_embedding.numpy()

text = "Data engineering involves building robust data pipelines"
embedding = get_bert_embeddings(text)
print(f"Embedding shape: {embedding.shape}")  # (1, 768)
```

## 3. Creating Embeddings
**OpenAI Embeddings**:
```python
import openai
import numpy as np

def get_openai_embedding(text, model="text-embedding-ada-002"):
    response = openai.Embedding.create(
        input=text,
        model=model
    )
    return response['data'][0]['embedding']

# Batch processing
def get_batch_embeddings(texts, batch_size=100):
    embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        response = openai.Embedding.create(
            input=batch,
            model="text-embedding-ada-002"
        )
        
        batch_embeddings = [item['embedding'] for item in response['data']]
        embeddings.extend(batch_embeddings)
    
    return embeddings
```

**Sentence Transformers**:
```python
from sentence_transformers import SentenceTransformer

# Load pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Single text
text = "Machine learning models require quality data"
embedding = model.encode(text)
print(f"Embedding dimension: {len(embedding)}")  # 384

# Multiple texts
texts = [
    "Data preprocessing is crucial for ML",
    "Feature engineering improves model performance",
    "Cross-validation prevents overfitting"
]
embeddings = model.encode(texts)
print(f"Embeddings shape: {embeddings.shape}")  # (3, 384)
```

## 4. Similarity Calculations
**Distance Metrics**:
```python
import numpy as np
from scipy.spatial.distance import cosine, euclidean

def cosine_similarity(a, b):
    """Most common for text embeddings"""
    return 1 - cosine(a, b)

def euclidean_similarity(a, b):
    """Good for normalized embeddings"""
    return 1 / (1 + euclidean(a, b))

def dot_product_similarity(a, b):
    """Fast computation, assumes normalized vectors"""
    return np.dot(a, b)

# Example usage
embedding1 = model.encode("Python programming language")
embedding2 = model.encode("Python coding and development")
embedding3 = model.encode("Snake species in nature")

print(f"Python programming vs Python coding: {cosine_similarity(embedding1, embedding2):.3f}")
print(f"Python programming vs Snake species: {cosine_similarity(embedding1, embedding3):.3f}")
```

**Similarity Search**:
```python
def find_most_similar(query_embedding, candidate_embeddings, top_k=5):
    """Find top-k most similar embeddings"""
    similarities = []
    
    for i, candidate in enumerate(candidate_embeddings):
        similarity = cosine_similarity(query_embedding, candidate)
        similarities.append((i, similarity))
    
    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    return similarities[:top_k]

# Usage
query = "data pipeline architecture"
query_embedding = model.encode(query)

documents = [
    "Building ETL pipelines with Apache Airflow",
    "Database design principles and normalization", 
    "Real-time data streaming with Kafka",
    "Machine learning model deployment strategies"
]
doc_embeddings = model.encode(documents)

similar_docs = find_most_similar(query_embedding, doc_embeddings, top_k=3)
for idx, similarity in similar_docs:
    print(f"Document: {documents[idx]}")
    print(f"Similarity: {similarity:.3f}\n")
```

## 5. Embedding Models Comparison
**Model Characteristics**:
```yaml
# OpenAI text-embedding-ada-002
Dimensions: 1536
Max tokens: 8191
Strengths: High quality, multilingual
Use case: Production applications

# Sentence-BERT models
all-MiniLM-L6-v2:
  Dimensions: 384
  Speed: Fast
  Quality: Good for general use

all-mpnet-base-v2:
  Dimensions: 768  
  Speed: Medium
  Quality: Higher quality, slower

# Specialized models
msmarco-distilbert-base-v4: Information retrieval
paraphrase-multilingual-MiniLM-L12-v2: Multilingual
```

**Model Selection**:
```python
def choose_embedding_model(use_case, performance_requirements):
    """Guide for model selection"""
    
    if use_case == "production_search":
        if performance_requirements == "high_quality":
            return "text-embedding-ada-002"  # OpenAI
        else:
            return "all-MiniLM-L6-v2"  # Fast and good
    
    elif use_case == "multilingual":
        return "paraphrase-multilingual-MiniLM-L12-v2"
    
    elif use_case == "code_search":
        return "microsoft/codebert-base"
    
    elif use_case == "scientific_papers":
        return "allenai/specter"
    
    else:
        return "all-mpnet-base-v2"  # General purpose
```

## 6. Fine-tuning Embeddings
**Custom Training**:
```python
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader

# Prepare training data
train_examples = [
    InputExample(texts=['Data pipeline', 'ETL process'], label=0.9),
    InputExample(texts=['Machine learning', 'Deep learning'], label=0.8),
    InputExample(texts=['Database', 'Cooking recipe'], label=0.1)
]

# Load base model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create data loader
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)

# Define loss function
train_loss = losses.CosineSimilarityLoss(model)

# Fine-tune
model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=1,
    warmup_steps=100
)

# Save fine-tuned model
model.save('./fine-tuned-embeddings')
```

**Domain Adaptation**:
```python
# Adapt embeddings for specific domain
def create_domain_embeddings(domain_texts, base_model):
    """Create domain-specific embeddings"""
    
    # Generate embeddings for domain texts
    domain_embeddings = base_model.encode(domain_texts)
    
    # Calculate domain centroid
    domain_centroid = np.mean(domain_embeddings, axis=0)
    
    # Adjust embeddings toward domain
    adapted_embeddings = []
    for embedding in domain_embeddings:
        # Weighted combination with domain centroid
        adapted = 0.8 * embedding + 0.2 * domain_centroid
        adapted_embeddings.append(adapted)
    
    return np.array(adapted_embeddings)
```

## 7. Dimensionality Reduction
**PCA for Visualization**:
```python
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def visualize_embeddings(embeddings, labels, n_components=2):
    """Reduce dimensions and visualize"""
    
    # Apply PCA
    pca = PCA(n_components=n_components)
    reduced_embeddings = pca.fit_transform(embeddings)
    
    # Plot
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], 
                         c=range(len(labels)), cmap='viridis')
    
    # Add labels
    for i, label in enumerate(labels):
        plt.annotate(label, (reduced_embeddings[i, 0], reduced_embeddings[i, 1]))
    
    plt.title('Embedding Visualization (PCA)')
    plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)')
    plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)')
    plt.show()

# Example usage
texts = ["Python", "Java", "JavaScript", "HTML", "CSS", "SQL"]
embeddings = model.encode(texts)
visualize_embeddings(embeddings, texts)
```

**t-SNE for Complex Patterns**:
```python
from sklearn.manifold import TSNE

def tsne_visualization(embeddings, labels, perplexity=30):
    """t-SNE for non-linear dimensionality reduction"""
    
    tsne = TSNE(n_components=2, perplexity=perplexity, random_state=42)
    reduced_embeddings = tsne.fit_transform(embeddings)
    
    plt.figure(figsize=(12, 8))
    plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1])
    
    for i, label in enumerate(labels):
        plt.annotate(label, (reduced_embeddings[i, 0], reduced_embeddings[i, 1]))
    
    plt.title('Embedding Visualization (t-SNE)')
    plt.show()
```

## 8. Embedding Storage and Retrieval
**Efficient Storage**:
```python
import pickle
import numpy as np
from typing import Dict, List

class EmbeddingStore:
    def __init__(self):
        self.embeddings = {}
        self.metadata = {}
    
    def add_embedding(self, key: str, embedding: np.ndarray, metadata: Dict = None):
        """Store embedding with metadata"""
        self.embeddings[key] = embedding.astype(np.float32)  # Save memory
        self.metadata[key] = metadata or {}
    
    def get_embedding(self, key: str):
        """Retrieve embedding"""
        return self.embeddings.get(key)
    
    def batch_add(self, keys: List[str], embeddings: np.ndarray, metadatas: List[Dict] = None):
        """Batch add embeddings"""
        metadatas = metadatas or [{}] * len(keys)
        
        for key, embedding, metadata in zip(keys, embeddings, metadatas):
            self.add_embedding(key, embedding, metadata)
    
    def save(self, filepath: str):
        """Save to disk"""
        data = {
            'embeddings': self.embeddings,
            'metadata': self.metadata
        }
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
    
    def load(self, filepath: str):
        """Load from disk"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        self.embeddings = data['embeddings']
        self.metadata = data['metadata']
    
    def search_similar(self, query_embedding: np.ndarray, top_k: int = 5):
        """Find similar embeddings"""
        similarities = []
        
        for key, embedding in self.embeddings.items():
            similarity = cosine_similarity(query_embedding, embedding)
            similarities.append((key, similarity, self.metadata[key]))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
```

## 9. Evaluation Metrics
**Embedding Quality Assessment**:
```python
def evaluate_embeddings(embeddings, labels, test_queries):
    """Evaluate embedding quality"""
    
    # Intrinsic evaluation: clustering quality
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    
    kmeans = KMeans(n_clusters=len(set(labels)))
    cluster_labels = kmeans.fit_predict(embeddings)
    silhouette = silhouette_score(embeddings, cluster_labels)
    
    # Extrinsic evaluation: retrieval performance
    retrieval_scores = []
    for query, expected_results in test_queries:
        query_embedding = model.encode(query)
        similar_items = find_most_similar(query_embedding, embeddings, top_k=10)
        
        # Calculate precision@k
        retrieved_indices = [idx for idx, _ in similar_items]
        relevant_retrieved = len(set(retrieved_indices) & set(expected_results))
        precision = relevant_retrieved / len(retrieved_indices)
        retrieval_scores.append(precision)
    
    return {
        'silhouette_score': silhouette,
        'avg_precision': np.mean(retrieval_scores),
        'retrieval_scores': retrieval_scores
    }
```

## 10. Production Considerations
**Caching Strategy**:
```python
import hashlib
from functools import lru_cache

class EmbeddingCache:
    def __init__(self, max_size=10000):
        self.cache = {}
        self.max_size = max_size
        self.access_count = {}
    
    def _get_hash(self, text):
        return hashlib.md5(text.encode()).hexdigest()
    
    def get_embedding(self, text, embedding_func):
        """Get embedding with caching"""
        text_hash = self._get_hash(text)
        
        if text_hash in self.cache:
            self.access_count[text_hash] += 1
            return self.cache[text_hash]
        
        # Generate embedding
        embedding = embedding_func(text)
        
        # Cache management
        if len(self.cache) >= self.max_size:
            # Remove least accessed item
            least_accessed = min(self.access_count.items(), key=lambda x: x[1])
            del self.cache[least_accessed[0]]
            del self.access_count[least_accessed[0]]
        
        self.cache[text_hash] = embedding
        self.access_count[text_hash] = 1
        
        return embedding

# Usage
cache = EmbeddingCache()
embedding = cache.get_embedding("sample text", model.encode)
```

**Batch Processing**:
```python
def process_large_dataset(texts, batch_size=1000, model=None):
    """Process large datasets efficiently"""
    
    embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        
        # Process batch
        batch_embeddings = model.encode(batch, show_progress_bar=True)
        embeddings.extend(batch_embeddings)
        
        # Optional: Save intermediate results
        if i % (batch_size * 10) == 0:
            np.save(f'embeddings_checkpoint_{i}.npy', np.array(embeddings))
    
    return np.array(embeddings)
```