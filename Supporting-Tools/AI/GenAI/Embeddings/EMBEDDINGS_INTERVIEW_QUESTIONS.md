# Embeddings - Interview Questions

## Basic Questions

### 1. What are embeddings and why are they important in AI/ML?
**Answer:** Embeddings are dense vector representations of data (text, images, etc.) that capture semantic meaning in high-dimensional space. They're important because they:
- Convert discrete data into continuous vectors
- Capture semantic relationships and similarities
- Enable mathematical operations on text/images
- Power search, recommendation, and RAG systems
- Allow transfer learning across domains

### 2. How do text embeddings differ from traditional text representations like TF-IDF?
**Answer:**
- **Embeddings**: Dense vectors (768-1536 dimensions), capture semantic meaning, context-aware
- **TF-IDF**: Sparse vectors, keyword-based, no semantic understanding
- **Similarity**: Embeddings find "car" similar to "vehicle"; TF-IDF only matches exact words
- **Dimensionality**: Embeddings are fixed-size; TF-IDF varies with vocabulary size

### 3. What is the difference between word embeddings and sentence embeddings?
**Answer:**
- **Word embeddings**: Individual word vectors (Word2Vec, GloVe)
- **Sentence embeddings**: Entire sentence/document vectors
- **Composition**: Sentence embeddings consider word order and context
- **Use cases**: Word embeddings for NLP tasks; sentence embeddings for semantic search
- **Models**: BERT, Sentence-BERT for sentence embeddings

## Intermediate Questions

### 4. How would you evaluate the quality of embeddings?
**Answer:**
```python
# Similarity evaluation
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def evaluate_embeddings(embeddings, test_pairs):
    similarities = []
    for pair in test_pairs:
        emb1, emb2 = embeddings[pair[0]], embeddings[pair[1]]
        sim = cosine_similarity([emb1], [emb2])[0][0]
        similarities.append(sim)
    return np.mean(similarities)

# Clustering evaluation
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def cluster_quality(embeddings, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters)
    labels = kmeans.fit_predict(embeddings)
    return silhouette_score(embeddings, labels)
```

Methods:
- **Similarity tasks**: Compare known similar/dissimilar pairs
- **Clustering**: Measure cluster coherence
- **Downstream tasks**: Performance on specific applications
- **Visualization**: t-SNE/UMAP for visual inspection

### 5. What are the challenges with embedding models and how do you address them?
**Answer:**
**Challenges:**
- **Domain mismatch**: Pre-trained models may not work for specific domains
- **Language limitations**: Models trained on specific languages
- **Bias**: Embeddings can inherit training data biases
- **Dimensionality**: High-dimensional curse
- **Cold start**: No embeddings for new items

**Solutions:**
- **Fine-tuning**: Adapt models to specific domains
- **Multilingual models**: Use models trained on multiple languages
- **Bias detection**: Regular bias auditing and mitigation
- **Dimensionality reduction**: PCA, t-SNE for visualization
- **Hybrid approaches**: Combine multiple embedding sources

### 6. How do you handle embeddings for new or unseen data?
**Answer:**
```python
# Handle out-of-vocabulary words
def handle_oov(text, model, fallback_strategy='average'):
    tokens = text.split()
    embeddings = []
    
    for token in tokens:
        if token in model:
            embeddings.append(model[token])
        else:
            if fallback_strategy == 'zero':
                embeddings.append(np.zeros(model.vector_size))
            elif fallback_strategy == 'random':
                embeddings.append(np.random.normal(size=model.vector_size))
            elif fallback_strategy == 'average':
                embeddings.append(np.mean(list(model.vectors), axis=0))
    
    return np.mean(embeddings, axis=0)
```

Strategies:
- **Subword tokenization**: BPE, SentencePiece for handling rare words
- **Character-level**: Character-based embeddings
- **Fallback embeddings**: Use average or random vectors
- **Dynamic updates**: Retrain or fine-tune with new data

## Advanced Questions

### 7. How would you implement a semantic search system using embeddings?
**Answer:**
```python
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

class SemanticSearch:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []
    
    def build_index(self, documents):
        self.documents = documents
        embeddings = self.model.encode(documents)
        
        # Build FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # Inner product
        
        # Normalize for cosine similarity
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings.astype('float32'))
    
    def search(self, query, k=5):
        query_embedding = self.model.encode([query])
        faiss.normalize_L2(query_embedding)
        
        scores, indices = self.index.search(query_embedding.astype('float32'), k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            results.append({
                'document': self.documents[idx],
                'score': float(score)
            })
        return results
```

### 8. What are the trade-offs between different embedding models?
**Answer:**
**Model Comparison:**
- **OpenAI text-embedding-ada-002**: High quality, API-based, cost per usage
- **Sentence-BERT**: Good balance, self-hosted, moderate size
- **Universal Sentence Encoder**: Google's model, good for general use
- **Domain-specific**: Better for specialized domains, requires training

**Trade-offs:**
- **Quality vs Speed**: Larger models more accurate but slower
- **Cost vs Control**: API models vs self-hosted
- **Generalization vs Specialization**: General models vs domain-specific
- **Latency vs Accuracy**: Real-time requirements vs quality needs

### 9. How do you optimize embedding storage and retrieval for large-scale systems?
**Answer:**
```python
# Quantization for storage optimization
def quantize_embeddings(embeddings, bits=8):
    # Scalar quantization
    min_val, max_val = embeddings.min(), embeddings.max()
    scale = (2**bits - 1) / (max_val - min_val)
    quantized = ((embeddings - min_val) * scale).astype(np.uint8)
    return quantized, min_val, scale

# Approximate nearest neighbor search
import annoy

def build_annoy_index(embeddings, n_trees=10):
    dimension = embeddings.shape[1]
    index = annoy.AnnoyIndex(dimension, 'angular')
    
    for i, embedding in enumerate(embeddings):
        index.add_item(i, embedding)
    
    index.build(n_trees)
    return index
```

**Optimization strategies:**
- **Quantization**: Reduce precision to save storage
- **Compression**: Use PCA or other dimensionality reduction
- **Approximate search**: HNSW, LSH for faster retrieval
- **Caching**: Cache frequently accessed embeddings
- **Sharding**: Distribute across multiple nodes

### 10. How do you handle multilingual embeddings and cross-lingual search?
**Answer:**
```python
# Multilingual embedding approach
from sentence_transformers import SentenceTransformer

class MultilingualSearch:
    def __init__(self):
        # Use multilingual model
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    def encode_multilingual(self, texts, languages=None):
        # Model handles multiple languages automatically
        embeddings = self.model.encode(texts)
        return embeddings
    
    def cross_lingual_search(self, query, documents, query_lang='en'):
        # Query in one language, search in multiple languages
        query_emb = self.model.encode([query])
        doc_embs = self.model.encode(documents)
        
        # Cosine similarity works across languages
        similarities = cosine_similarity(query_emb, doc_embs)[0]
        
        # Return ranked results
        ranked_indices = np.argsort(similarities)[::-1]
        return [(documents[i], similarities[i]) for i in ranked_indices]
```

**Approaches:**
- **Multilingual models**: Single model for multiple languages
- **Language alignment**: Map embeddings to shared space
- **Translation**: Translate to common language first
- **Language-specific models**: Separate models per language